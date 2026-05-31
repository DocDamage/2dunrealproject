import os
import re

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "AnimationSources")

MANNY_MESH_PATH = "/Game/Mesh/Skeletal/Default/SKM_Manny.SKM_Manny"

GAME_SAMPLE_SOURCE_ROOT = os.path.join(SOURCE_ROOT, "GameAnimationSample")
GAME_SAMPLE_DESTINATION = "/Game/NocturneSignal/AnimationSources/GameAnimationSample/Animations"

PARAGON_SOURCE_ROOT = os.path.join(SOURCE_ROOT, "ParagonMannyCurated")
PARAGON_DESTINATION = "/Game/NocturneSignal/AnimationSources/ParagonMannyCurated/Animations"

FIGHT_SOURCE_ROOT = os.path.join(SOURCE_ROOT, "FightAnimationMocapPack")
FIGHT_DESTINATION_ROOT = "/Game/NocturneSignal/AnimationSources/FightAnimationMocapPack"
FIGHT_ANIMATION_DESTINATION = FIGHT_DESTINATION_ROOT + "/Animations"
FIGHT_MESH_FILE = "Male_Lowpoly.fbx"
FIGHT_MESH_NAME = "SK_FightMocap_MaleLowpoly"
FIGHT_MESH_PATH = FIGHT_DESTINATION_ROOT + "/" + FIGHT_MESH_NAME + "." + FIGHT_MESH_NAME


def log(message):
    unreal.log("[NocturneFabJacobCandidateImport] " + str(message))


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


def sanitized_asset_name(path):
    name = os.path.splitext(os.path.basename(path))[0]
    name = re.sub(r"[^0-9A-Za-z_]+", "_", name).strip("_")
    return name or "ImportedAnimation"


def fbx_files(root):
    if not os.path.isdir(root):
        raise RuntimeError("Source directory is missing: " + root)

    paths = []
    for folder, _, files in os.walk(root):
        for item in files:
            if item.lower().endswith(".fbx"):
                paths.append(os.path.join(folder, item))
    return sorted(paths)


def unreal_relative_destination(source_root, source_file, destination_root):
    rel_dir = os.path.dirname(os.path.relpath(source_file, source_root))
    if rel_dir in ("", "."):
        return destination_root

    parts = [re.sub(r"[^0-9A-Za-z_]+", "_", part).strip("_") for part in rel_dir.split(os.sep)]
    parts = [part for part in parts if part]
    return destination_root + "/" + "/".join(parts)


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


def make_mesh_import_task(path, destination, mesh_name):
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)

    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = destination
    task.destination_name = mesh_name
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def imported_animation_count(destination):
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path(destination, recursive=True)
    return len([asset for asset in assets if str(asset.asset_class_path.asset_name) == "AnimSequence"])


def import_manny_animation_set(name, source_root, destination_root, skeleton, expected_minimum):
    paths = fbx_files(source_root)
    if len(paths) < expected_minimum:
        raise RuntimeError(f"{name}: expected at least {expected_minimum} FBXs, found {len(paths)}")

    tasks = []
    for path in paths:
        destination = unreal_relative_destination(source_root, path, destination_root)
        unreal.EditorAssetLibrary.make_directory(destination)
        tasks.append(make_animation_import_task(path, destination, skeleton))

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    imported_count = imported_animation_count(destination_root)
    if imported_count < len(paths):
        raise RuntimeError(f"{name}: expected {len(paths)} imported animations, got {imported_count}")

    unreal.EditorAssetLibrary.save_directory(destination_root, only_if_is_dirty=False, recursive=True)
    log(f"{name}: imported/available {imported_count} AnimSequences")


def import_fight_pack():
    mesh_path = os.path.join(FIGHT_SOURCE_ROOT, FIGHT_MESH_FILE)
    if not os.path.exists(mesh_path):
        raise RuntimeError("Missing Fight pack source mesh: " + mesh_path)

    unreal.EditorAssetLibrary.make_directory(FIGHT_DESTINATION_ROOT)
    unreal.EditorAssetLibrary.make_directory(FIGHT_ANIMATION_DESTINATION)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(
        [make_mesh_import_task(mesh_path, FIGHT_DESTINATION_ROOT, FIGHT_MESH_NAME)]
    )
    fight_mesh = load_asset(FIGHT_MESH_PATH)
    skeleton = fight_mesh.get_editor_property("skeleton")

    paths = [
        path for path in fbx_files(FIGHT_SOURCE_ROOT)
        if os.path.basename(path).lower() != FIGHT_MESH_FILE.lower()
    ]
    if len(paths) != 10:
        raise RuntimeError(f"Fight pack: expected 10 animation FBXs, found {len(paths)}")

    tasks = [make_animation_import_task(path, FIGHT_ANIMATION_DESTINATION, skeleton) for path in paths]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    imported_count = imported_animation_count(FIGHT_ANIMATION_DESTINATION)
    if imported_count != len(paths):
        raise RuntimeError(f"Fight pack: expected {len(paths)} imported animations, got {imported_count}")

    unreal.EditorAssetLibrary.save_directory(FIGHT_DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)
    log(f"FightAnimationMocapPack: imported/available {imported_count} AnimSequences")


def main():
    manny_mesh = load_asset(MANNY_MESH_PATH)
    manny_skeleton = manny_mesh.get_editor_property("skeleton")

    import_manny_animation_set("GameAnimationSample", GAME_SAMPLE_SOURCE_ROOT, GAME_SAMPLE_DESTINATION, manny_skeleton, 200)
    import_manny_animation_set("ParagonMannyCurated", PARAGON_SOURCE_ROOT, PARAGON_DESTINATION, manny_skeleton, 500)
    import_fight_pack()

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterFabJacobCandidateImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
