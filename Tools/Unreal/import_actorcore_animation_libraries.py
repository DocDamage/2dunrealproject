import os
import re

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "AnimationSources")

ACTORCORE_DESTINATION_ROOT = "/Game/NocturneSignal/AnimationSources/ActorCore"
ACTORCORE_MESH_NAME = "SK_ActorCore_MotionDummyMale"
ACTORCORE_MESH_PATH = (
    ACTORCORE_DESTINATION_ROOT
    + "/"
    + ACTORCORE_MESH_NAME
    + "."
    + ACTORCORE_MESH_NAME
)
ACTORCORE_SKELETON_PATH = (
    ACTORCORE_DESTINATION_ROOT
    + "/"
    + ACTORCORE_MESH_NAME
    + "_Skeleton."
    + ACTORCORE_MESH_NAME
    + "_Skeleton"
)

SOURCE_SETS = [
    {
        "name": "ActorCoreWalk",
        "source": os.path.join(SOURCE_ROOT, "ActorCoreWalk"),
        "destination": ACTORCORE_DESTINATION_ROOT + "/Walk",
        "expected_count": 3,
    },
    {
        "name": "ActorCoreTactical",
        "source": os.path.join(SOURCE_ROOT, "ActorCoreTactical"),
        "destination": ACTORCORE_DESTINATION_ROOT + "/Tactical",
        "expected_count": 11,
    },
]


def log(message):
    unreal.log("[NocturneActorCoreImport] " + str(message))


def require_file(path):
    if not os.path.exists(path):
        raise RuntimeError("Required source file is missing: " + path)


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


def sanitized_asset_name(path):
    name = os.path.splitext(os.path.basename(path))[0]
    name = re.sub(r"[^0-9A-Za-z_]+", "_", name).strip("_")
    return name or "ActorCoreAnimation"


def actor_mesh_path(source_root):
    actor_root = os.path.join(source_root, "Actor")
    for root, _, files in os.walk(actor_root):
        for item in files:
            if item.lower().endswith(".fbx"):
                return os.path.join(root, item)
    raise RuntimeError("Could not find ActorCore actor FBX under " + actor_root)


def motion_fbx_files(source_root):
    motion_root = os.path.join(source_root, "Motion")
    if not os.path.isdir(motion_root):
        raise RuntimeError("ActorCore motion directory is missing: " + motion_root)

    paths = []
    for root, _, files in os.walk(motion_root):
        for item in files:
            if item.lower().endswith(".fbx"):
                paths.append(os.path.join(root, item))
    return sorted(paths)


def make_mesh_import_task(path):
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)

    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = ACTORCORE_DESTINATION_ROOT
    task.destination_name = ACTORCORE_MESH_NAME
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def make_animation_import_task(path, destination, skeleton):
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", False)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    options.set_editor_property("skeleton", skeleton)

    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = destination
    task.destination_name = sanitized_asset_name(path)
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def imported_animation_paths(destination):
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path(destination, recursive=True)
    return sorted(
        str(asset.package_name) + "." + str(asset.asset_name)
        for asset in assets
        if str(asset.asset_class_path.asset_name) == "AnimSequence"
    )


def import_source_mesh():
    source_mesh = actor_mesh_path(os.path.join(SOURCE_ROOT, "ActorCoreWalk"))
    require_file(source_mesh)

    unreal.EditorAssetLibrary.make_directory(ACTORCORE_DESTINATION_ROOT)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([make_mesh_import_task(source_mesh)])
    mesh = load_asset(ACTORCORE_MESH_PATH)
    load_asset(ACTORCORE_SKELETON_PATH)
    log("ActorCore source mesh imported/available: " + ACTORCORE_MESH_PATH)
    return mesh


def import_source_set(source_set, skeleton):
    source_paths = motion_fbx_files(source_set["source"])
    expected_count = source_set["expected_count"]
    if len(source_paths) != expected_count:
        raise RuntimeError(
            f"Expected {expected_count} {source_set['name']} motion FBXs, found {len(source_paths)}"
        )
    for path in source_paths:
        require_file(path)

    animation_destination = source_set["destination"] + "/Animations"
    unreal.EditorAssetLibrary.make_directory(source_set["destination"])
    unreal.EditorAssetLibrary.make_directory(animation_destination)

    tasks = [
        make_animation_import_task(path, animation_destination, skeleton)
        for path in source_paths
    ]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    imported = imported_animation_paths(animation_destination)
    if len(imported) != len(source_paths):
        raise RuntimeError(f"Expected {len(source_paths)} imports, got {len(imported)} for {source_set['name']}")

    unreal.EditorAssetLibrary.save_directory(source_set["destination"], only_if_is_dirty=False, recursive=True)
    log(f"{source_set['name']}: imported/available {len(imported)} AnimSequences")


def main():
    import_source_mesh()
    skeleton = load_asset(ACTORCORE_SKELETON_PATH)

    for source_set in SOURCE_SETS:
        import_source_set(source_set, skeleton)

    unreal.EditorAssetLibrary.save_directory(ACTORCORE_DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterActorCoreImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
