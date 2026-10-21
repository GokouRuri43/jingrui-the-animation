"""Check executable availability and Blender's embedded Cycles support."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = {'python': sys.version.split()[0], 'errors': []}
    if sys.version_info < (3, 10):
        report['errors'].append('Python 3.10+ required')
    for name in ['blender', 'ffmpeg', 'ffprobe']:
        executable = shutil.which(os.environ.get('BLENDER_BIN', name) if name == 'blender' else name)
        report[name] = executable
        if not executable:
            report['errors'].append(f'Missing executable: {name}')
            continue
        if name == 'blender':
            expression = (
                "import bpy, json; "
                "assert bpy.app.version >= (3, 4, 0), 'Blender 3.4+ required'; "
                "bpy.context.scene.render.engine='CYCLES'; "
                "bpy.context.scene.cycles.device='CPU'; "
                "print('ECHO_PROBE=' + json.dumps({'version':bpy.app.version_string,'engine':'CYCLES','device':'CPU'}))"
            )
            command = [executable, '--background', '--factory-startup', '--python-exit-code', '1', '--python-expr', expression]
        else:
            command = [executable, '-version']
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', check=True, timeout=90)
            if name == 'blender':
                probe = next(line for line in result.stdout.splitlines() if line.startswith('ECHO_PROBE='))
                report['blender_probe'] = json.loads(probe.split('=', 1)[1])
        except (OSError, subprocess.SubprocessError, StopIteration, ValueError) as exc:
            report['errors'].append(f'{name}: {exc}')
    for document in ['某某-基础设定.md', 'ECHO-基础设定.md']:
        try:
            if not (ROOT / document).read_text(encoding='utf-8').strip():
                raise ValueError('Empty document')
        except (OSError, UnicodeError, ValueError) as exc:
            report['errors'].append(f'{document}: {exc}')
    output = ROOT / 'outputs'
    output.mkdir(exist_ok=True)
    (output / 'environment.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
