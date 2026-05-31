import os
import re

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "AnimationSources")

MOTIFECT_SOURCE_ROOT = os.path.join(SOURCE_ROOT, "MotifectMartialArts")
REALISTIC_SOURCE_ROOT = os.path.join(SOURCE_ROOT, "RealisticCombatMoves")

MOTIFECT_DESTINATION_ROOT = "/Game/NocturneSignal/AnimationSources/MotifectMartialArts"
MOTIFECT_ANIMATION_DESTINATION = MOTIFECT_DESTINATION_ROOT + "/Animations"
MCO_SKELETON_PATH = (
    "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/"
    "SK_MCO_TC_Sword_Mannequin_Skeleton.SK_MCO_TC_Sword_Mannequin_Skeleton"
)

REALISTIC_DESTINATION_ROOT = "/Game/NocturneSignal/AnimationSources/RealisticCombatMoves"
REALISTIC_ANIMATION_DESTINATION = REALISTIC_DESTINATION_ROOT + "/Animations"
REALISTIC_MESH_FILE = "Male_Lowpoly.fbx"
REALISTIC_MESH_NAME = "SK_RealisticCombat_MaleLowpoly"
REALISTIC_SKELETON_PATH = (
    REALISTIC_DESTINATION_ROOT
    + "/"
    + REALISTIC_MESH_NAME
    + "_Skeleton."
    + REALISTIC_MESH_NAME
    + "_Skeleton"
)


def log(message):
    unreal.log("[NocturneFabCombatImport] " + str(message))


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
    return name or "ImportedAnimation"


def fbx_files(path):
    if not os.path.isdir(path):
        raise RuntimeError("Source directory is missing: " + path)
    return sorted(
        os.path.join(path, item)
        for item in os.listdir(path)
        if item.lower().endswith(".fbx")
    )


def make_animation_import_task(path, destination, skeleton):
    name = sanitized_asset_name(path)

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
    task.destination_name = name
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


def imported_animation_paths(destination):
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path(destination, recursive=True)
    return sorted(
        str(asset.package_name) + "." + str(asset.asset_name)
        for asset in assets
        if str(asset.asset_class_path.asset_name) == "AnimSequence"
    )


def import_motifect():
    skeleton = load_asset(MCO_SKELETON_PATH)
    paths = fbx_files(MOTIFECT_SOURCE_ROOT)
    if len(paths) != 40:
        raise RuntimeError(f"Expected 40 Motifect FBXs, found {len(paths)}")
    for path in paths:
        require_file(path)

    unreal.EditorAssetLibrary.make_directory(MOTIFECT_DESTINATION_ROOT)
    unreal.EditorAssetLibrary.make_directory(MOTIFECT_ANIMATION_DESTINATION)

    tasks = [make_animation_import_task(path, MOTIFECT_ANIMATION_DESTINATION, skeleton) for path in paths]
    import_error = None
    try:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    except RuntimeError as exc:
        message = str(exc)
        expected_fragments = ["RightEye", "LeftEye", "Jaw"]
        if not all(fragment in message for fragment in expected_fragments):
            raise
        import_error = message

    imported = imported_animation_paths(MOTIFECT_ANIMATION_DESTINATION)
    if len(imported) != len(paths):
        raise RuntimeError(f"Expected {len(paths)} Motifect imports, got {len(imported)}")
    if import_error:
        log("Accepted Motifect import with ignored facial-track warnings for Jaw/LeftEye/RightEye.")

    unreal.EditorAssetLibrary.save_directory(MOTIFECT_DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)
    log(f"Motifect Martial Arts imported/available {len(imported)} AnimSequences")


def import_realistic():
    mesh_path = os.path.join(REALISTIC_SOURCE_ROOT, REALISTIC_MESH_FILE)
    require_file(mesh_path)
    animation_paths = [
        path
        for path in fbx_files(REALISTIC_SOURCE_ROOT)
        if os.path.basename(path).lower() != REALISTIC_MESH_FILE.lower()
    ]
    if len(animation_paths) != 10:
        raise RuntimeError(f"Expected 10 Realistic Combat animation FBXs, found {len(animation_paths)}")

    unreal.EditorAssetLibrary.make_directory(REALISTIC_DESTINATION_ROOT)
    unreal.EditorAssetLibrary.make_directory(REALISTIC_ANIMATION_DESTINATION)

    mesh_task = make_mesh_import_task(mesh_path, REALISTIC_DESTINATION_ROOT, REALISTIC_MESH_NAME)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([mesh_task])
    skeleton = load_asset(REALISTIC_SKELETON_PATH)

    tasks = [
        make_animation_import_task(path, REALISTIC_ANIMATION_DESTINATION, skeleton)
        for path in animation_paths
    ]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    imported = imported_animation_paths(REALISTIC_ANIMATION_DESTINATION)
    if len(imported) != len(animation_paths):
        raise RuntimeError(f"Expected {len(animation_paths)} Realistic Combat imports, got {len(imported)}")

    unreal.EditorAssetLibrary.save_directory(REALISTIC_DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)
    log(f"Realistic Combat Moves imported/available {len(imported)} AnimSequences")


def main():
    import_motifect()
    import_realistic()

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterFabCombatImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
