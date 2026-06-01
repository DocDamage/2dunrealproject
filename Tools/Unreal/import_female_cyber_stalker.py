import os

import unreal


PROJECT_ROOT = os.path.abspath(unreal.Paths.project_dir())
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "FemaleCyberStalker")
BIPED_ROOT = os.path.join(SOURCE_ROOT, "biped")

DESTINATION_ROOT = "/Game/NocturneSignal/Characters/FemaleCyberStalker"
TEXTURE_DESTINATION = DESTINATION_ROOT + "/Textures"
ANIMATION_DESTINATION = DESTINATION_ROOT + "/Animations"

MESH_SOURCE = os.path.join(SOURCE_ROOT, "Character_output.fbx")
MESH_NAME = "SK_FemaleCyberStalker"
MESH_PATH = DESTINATION_ROOT + "/" + MESH_NAME + "." + MESH_NAME
SKELETON_PATH = DESTINATION_ROOT + "/" + MESH_NAME + "_Skeleton." + MESH_NAME + "_Skeleton"

ANIMATION_SOURCES = [
    ("FCS_Run", os.path.join(BIPED_ROOT, "Animation_Running_withSkin.fbx")),
    ("FCS_Walk", os.path.join(BIPED_ROOT, "Animation_Walking_withSkin.fbx")),
]

TEXTURE_SOURCES = [
    os.path.join(BIPED_ROOT, "texture_0_metallic.png"),
    os.path.join(BIPED_ROOT, "texture_0_normal.png"),
    os.path.join(BIPED_ROOT, "texture_0_roughness.png"),
]


def log(message):
    unreal.log("[NocturneFemaleCyberStalkerImport] " + str(message))


def require_file(path):
    if not os.path.exists(path):
        raise RuntimeError("Required Female Cyber Stalker source file is missing: " + path)


def make_mesh_import_task():
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("import_materials", True)
    options.set_editor_property("import_textures", True)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)

    task = unreal.AssetImportTask()
    task.filename = MESH_SOURCE
    task.destination_path = DESTINATION_ROOT
    task.destination_name = MESH_NAME
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def make_animation_import_task(name, path, skeleton):
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


def make_texture_import_task(path):
    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = TEXTURE_DESTINATION
    task.destination_name = os.path.splitext(os.path.basename(path))[0]
    task.automated = True
    task.replace_existing = True
    task.save = True
    return task


def import_tasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    imported = []
    for task in tasks:
        imported.extend(task.imported_object_paths)
    return imported


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load imported asset: " + path)
    return asset


def main():
    require_file(MESH_SOURCE)
    for _, animation_path in ANIMATION_SOURCES:
        require_file(animation_path)
    for texture_path in TEXTURE_SOURCES:
        require_file(texture_path)

    unreal.EditorAssetLibrary.make_directory(DESTINATION_ROOT)
    unreal.EditorAssetLibrary.make_directory(ANIMATION_DESTINATION)
    unreal.EditorAssetLibrary.make_directory(TEXTURE_DESTINATION)

    imported = import_tasks([make_mesh_import_task()])
    mesh = load_asset(MESH_PATH)
    skeleton = load_asset(SKELETON_PATH)
    if mesh.get_editor_property("skeleton") != skeleton:
        raise RuntimeError("Imported mesh did not bind to its expected skeleton.")

    animation_tasks = [
        make_animation_import_task(name, animation_path, skeleton)
        for name, animation_path in ANIMATION_SOURCES
    ]
    imported.extend(import_tasks(animation_tasks))
    imported.extend(import_tasks([make_texture_import_task(path) for path in TEXTURE_SOURCES]))

    unreal.EditorAssetLibrary.save_directory(DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)

    log("Import complete:")
    for path in imported:
        log("  " + path)

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterFemaleCyberStalkerImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
