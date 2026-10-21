"""Run inside Blender, not system Python. Build a neutral shot blockout."""
import argparse
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector


def material(name, color):
    item = bpy.data.materials.new(name)
    item.diffuse_color = color
    item.use_nodes = True
    bsdf = item.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.7
    return item


def cube(name, position, size, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    obj.data.materials.append(mat)
    return obj


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def main():
    argv = sys.argv[sys.argv.index('--') + 1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--mode', choices=['animation', 'still', 'build'], required=True)
    parser.add_argument('--threads', type=int, default=2)
    args = parser.parse_args(argv)
    cfg = json.loads(Path(args.config).read_text(encoding='utf-8'))
    output = Path(args.output).resolve()
    frames_dir = output / 'frames'
    frames_dir.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = cfg['samples']
    scene.cycles.use_denoising = False
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = args.threads
    scene.render.resolution_x = cfg['width']
    scene.render.resolution_y = cfg['height']
    scene.render.resolution_percentage = 100
    scene.render.fps = cfg['fps']
    scene.frame_start = 1
    scene.frame_end = cfg['frames']
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.use_file_extension = True
    scene.view_settings.view_transform = 'Standard'
    scene.world = bpy.data.worlds.new('World')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.25, 0.3, 0.4, 1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = 0.45
    ground = material('Road', (0.12, 0.15, 0.18, 1))
    concrete = material('Buildings', (0.42, 0.47, 0.53, 1))
    line = material('Lane marks', (0.8, 0.7, 0.4, 1))
    cube('Street', (0, 3, -0.15), (24, 34, 0.3), ground)
    for index, block in enumerate(cfg['buildings']):
        cube(f'Building_{index:02d}', block['position'], block['size'], concrete)
    for y in range(-12, 18, 4):
        cube(f'Lane_{y}', (0, y, 0.01), (0.13, 1.8, 0.02), line)
    for index, actor in enumerate(cfg['actors']):
        mat = material(f'ActorMaterial_{index}', actor['color'])
        holder = bpy.data.objects.new(actor['name'], None)
        scene.collection.objects.link(holder)
        body = cube(f'ActorBody_{index}', (0, 0, 0.85), (0.45, 0.3, 1.25), mat)
        body.parent = holder
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.23, location=(0, 0, 1.65))
        head = bpy.context.object
        head.name = f'ActorHead_{index}'
        head.data.materials.append(mat)
        head.parent = holder
        holder.location = actor['start']
        holder.keyframe_insert(data_path='location', frame=1)
        holder.location = actor['end']
        holder.keyframe_insert(data_path='location', frame=cfg['frames'])
    bpy.ops.object.light_add(type='SUN', location=(0, -6, 10))
    sun = bpy.context.object
    sun.data.energy = 2
    sun.rotation_euler = (0.45, -0.35, -0.4)
    bpy.ops.object.light_add(type='AREA', location=(1, -5, 9))
    area = bpy.context.object
    area.data.energy = 1400
    area.data.shape = 'DISK'
    area.data.size = 7
    aim(area, (0, 2, 0))
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = 'PrevisCamera'
    camera.data.lens = cfg['camera']['lens']
    camera.data.clip_end = 300
    scene.camera = camera
    for frame, position in [(1, cfg['camera']['start']), (cfg['frames'], cfg['camera']['end'])]:
        camera.location = position
        aim(camera, cfg['camera']['target'])
        camera.keyframe_insert(data_path='location', frame=frame)
        camera.keyframe_insert(data_path='rotation_euler', frame=frame)
    scene.frame_set(1)
    # Relative paths keep the saved scene portable between local and cloud hosts.
    scene.render.filepath = '//frames/frame_'
    bpy.ops.wm.save_as_mainfile(filepath=str(output / 'scene.blend'))
    if args.mode == 'animation':
        bpy.ops.render.render(animation=True)
    elif args.mode == 'still':
        scene.render.filepath = str(frames_dir / 'frame_0001.png')
        bpy.ops.render.render(write_still=True)
    (output / 'blender-result.json').write_text(json.dumps({
        'version': bpy.app.version_string, 'engine': 'CYCLES', 'device': 'CPU',
        'mode': args.mode, 'blend_file': 'scene.blend',
        'frames': cfg['frames'] if args.mode == 'animation' else (1 if args.mode == 'still' else 0)
    }, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
