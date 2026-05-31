import os
import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "Jacob")
FBX_PATH = os.path.join(SOURCE_ROOT, "Jacob_NocturneCharacterOnly.fbx")
TEXTURE_PATHS = [
    os.path.join(SOURCE_ROOT, "textures", "T_JacobColor.png"),
    os.path.join(SOURCE_ROOT, "textures", "T_PropsAtlas.png"),
]

CHARACTER_DESTINATION = "/Game/NocturneSignal/Characters/Jacob"
TEXTURE_DESTINATION = CHARACTER_DESTINATION + "/Textures"


def require_file(path):
    if not os.path.exists(path):
        raise RuntimeError("Required Jacob source file is missing: " + path)


def import_texture(path):
    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = TEXTURE_DESTINATION
    task.automated = True
    task.replace_existing = True
    task.save = True
    return task


def import_character_fbx():
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("import_materials", True)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)

    task = unreal.AssetImportTask()
    task.filename = FBX_PATH
    task.destination_path = CHARACTER_DESTINATION
    task.destination_name = "SK_Jacob"
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def main():
    require_file(FBX_PATH)
    for texture_path in TEXTURE_PATHS:
        require_file(texture_path)

    unreal.EditorAssetLibrary.make_directory(CHARACTER_DESTINATION)
    unreal.EditorAssetLibrary.make_directory(TEXTURE_DESTINATION)

    tasks = [import_texture(path) for path in TEXTURE_PATHS]
    tasks.append(import_character_fbx())

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks(tasks)

    imported = []
    for task in tasks:
        imported.extend(task.imported_object_paths)

    if not imported:
        raise RuntimeError("Jacob import completed without imported assets.")

    unreal.EditorAssetLibrary.save_directory(CHARACTER_DESTINATION, only_if_is_dirty=False, recursive=True)

    unreal.log("Jacob import complete:")
    for path in imported:
        unreal.log("  " + path)

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""

    if "QuitAfterJacobImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
