import json
import sys

import bpy


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_asset(path):
    lower = path.lower()
    if lower.endswith(".fbx"):
        bpy.ops.import_scene.fbx(filepath=path)
    elif lower.endswith(".glb") or lower.endswith(".gltf"):
        bpy.ops.import_scene.gltf(filepath=path)
    elif lower.endswith(".blend"):
        bpy.ops.wm.open_mainfile(filepath=path)
    else:
        raise RuntimeError("Unsupported asset type: " + path)


def action_summary(path):
    reset_scene()
    import_asset(path)
    objects = [
        {
            "name": obj.name,
            "type": obj.type,
            "data": obj.data.name if getattr(obj, "data", None) else None,
        }
        for obj in bpy.context.scene.objects
    ]
    actions = []
    for action in bpy.data.actions:
        frame_start, frame_end = action.frame_range
        actions.append(
            {
                "name": action.name,
                "frame_start": frame_start,
                "frame_end": frame_end,
                "length_frames": frame_end - frame_start,
                "fcurves": len(action.fcurves),
            }
        )
    return {"path": path, "objects": objects, "actions": actions}


def main():
    paths = sys.argv[sys.argv.index("--") + 1 :]
    result = [action_summary(path) for path in paths]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
