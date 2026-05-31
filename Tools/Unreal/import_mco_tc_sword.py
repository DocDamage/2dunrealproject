import os

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "AnimationSources", "MCO_TC_Sword")

SKELETAL_MESH_FBX = os.path.join(SOURCE_ROOT, "SK_Mannequin.fbx")
ANIMATION_FBX_FILES = [
    "KBS_Ready_Idle_001.fbx",
    "KBS_Walk_F_001_IP.fbx",
    "KBS_Run_F_001_IP.fbx",
    "KBS_Sword_ATK_Combo_01_001_IP.fbx",
]

DESTINATION_ROOT = "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword"
ANIMATION_DESTINATION = DESTINATION_ROOT + "/Animations"
SKELETAL_MESH_NAME = "SK_MCO_TC_Sword_Mannequin"
SKELETON_PATH = DESTINATION_ROOT + "/" + SKELETAL_MESH_NAME + "_Skeleton." + SKELETAL_MESH_NAME + "_Skeleton"


def log(message):
    unreal.log("[NocturneMcoTcSwordImport] " + str(message))


def require_file(path):
    if not os.path.exists(path):
        raise RuntimeError("Required MCO TC Sword source file is missing: " + path)


def make_skeletal_mesh_import_task():
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)

    task = unreal.AssetImportTask()
    task.filename = SKELETAL_MESH_FBX
    task.destination_path = DESTINATION_ROOT
    task.destination_name = SKELETAL_MESH_NAME
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def make_animation_import_task(path, skeleton):
    name = os.path.splitext(os.path.basename(path))[0]

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
    task.destination_path = ANIMATION_DESTINATION
    task.destination_name = name
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def import_tasks(tasks):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks(tasks)

    imported = []
    for task in tasks:
        imported.extend(task.imported_object_paths)
    return imported


def main():
    require_file(SKELETAL_MESH_FBX)
    animation_paths = [os.path.join(SOURCE_ROOT, file_name) for file_name in ANIMATION_FBX_FILES]
    for animation_path in animation_paths:
        require_file(animation_path)

    unreal.EditorAssetLibrary.make_directory(DESTINATION_ROOT)
    unreal.EditorAssetLibrary.make_directory(ANIMATION_DESTINATION)

    mesh_imported = import_tasks([make_skeletal_mesh_import_task()])
    skeleton = unreal.EditorAssetLibrary.load_asset(SKELETON_PATH)
    if not skeleton:
        raise RuntimeError("Could not load imported MCO TC Sword skeleton: " + SKELETON_PATH)

    animation_tasks = [make_animation_import_task(path, skeleton) for path in animation_paths]
    animation_imported = import_tasks(animation_tasks)

    imported = mesh_imported + animation_imported
    if not imported:
        raise RuntimeError("MCO TC Sword import completed without imported assets.")

    unreal.EditorAssetLibrary.save_directory(DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)

    log("Import complete:")
    for path in imported:
        log("  " + path)

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterMcoTcSwordImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
