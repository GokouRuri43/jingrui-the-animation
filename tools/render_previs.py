"""Build/render a shot with Blender, then assemble and validate an MP4."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def project_path(value):
    path = Path(value)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='previs/demo.json')
    parser.add_argument('--output', default='outputs/previs-demo')
    parser.add_argument('--mode', choices=['animation', 'still', 'build'], default='animation')
    parser.add_argument('--smoke', action='store_true', help='Three frames at 160x90, one sample')
    parser.add_argument('--threads', type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.threads <= 64:
        parser.error('threads must be in 1..64')
    output = project_path(args.output)
    if not output.is_relative_to(ROOT / 'outputs') or output == ROOT / 'outputs':
        parser.error('output must be a subdirectory of this repository outputs/')
    cfg = json.loads(project_path(args.config).read_text(encoding='utf-8'))
    if args.smoke:
        cfg.update(width=160, height=90, frames=3, fps=3, samples=1)
    for name in ['width', 'height', 'frames', 'fps', 'samples']:
        if type(cfg[name]) is not int or cfg[name] <= 0:
            parser.error(f'{name} must be a positive integer')
    if cfg['width'] % 2 or cfg['height'] % 2:
        parser.error('width/height must be even for yuv420p MP4')
    if cfg['frames'] < 2:
        parser.error('frames must be at least 2 for camera animation')
    blender = shutil.which(os.environ.get('BLENDER_BIN', 'blender'))
    if not blender:
        parser.error('Blender missing; install it or set BLENDER_BIN')
    if args.mode == 'animation' and any(not shutil.which(x) for x in ['ffmpeg', 'ffprobe']):
        parser.error('Animation requires ffmpeg and ffprobe')
    output.mkdir(parents=True, exist_ok=True)
    resolved_config = output / 'shot.json'
    resolved_config.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    command = [blender, '--background', '--factory-startup', '--threads', str(args.threads),
        '--python-exit-code', '1', '--python', str(ROOT / 'tools/blender_scene.py'), '--',
        '--config', str(resolved_config), '--output', str(output), '--mode', args.mode, '--threads', str(args.threads)]
    with (output / 'blender.log').open('w', encoding='utf-8') as log:
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
    blend = output / 'scene.blend'
    if not blend.is_file() or blend.stat().st_size == 0:
        raise RuntimeError('Blender did not create scene.blend')
    expected = cfg['frames'] if args.mode == 'animation' else (1 if args.mode == 'still' else 0)
    for frame in range(1, expected + 1):
        image = output / 'frames' / f'frame_{frame:04d}.png'
        if not image.is_file() or image.stat().st_size == 0:
            raise RuntimeError(f'Missing rendered frame: {image}')
    result = json.loads((output / 'blender-result.json').read_text(encoding='utf-8'))
    if args.mode == 'animation':
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', str(cfg['fps']),
            '-start_number', '1', '-i', str(output / 'frames/frame_%04d.png'), '-frames:v', str(cfg['frames']),
            '-c:v', 'libx264', '-threads', str(args.threads), '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            str(output / 'preview.mp4')], check=True)
        probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
            '-show_entries', 'stream=width,height,nb_read_frames', '-of', 'json', str(output / 'preview.mp4')],
            capture_output=True, text=True, check=True)
        stream = json.loads(probe.stdout)['streams'][0]
        if (stream['width'], stream['height'], int(stream['nb_read_frames'])) != (cfg['width'], cfg['height'], cfg['frames']):
            raise RuntimeError(f'Unexpected video properties: {stream}')
        result['video'] = stream
    result['output'] = str(output)
    (output / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())
