import os

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "SourceArt", "AnimationSources", "MotifectSword")

ANIMATION_FBX_FILES = [
    "sword_draw_stance.fbx",
    "sword_slash_horizontal.fbx",
    "sword_thrust_forward.fbx",
    "sword_parry_and_riposte.fbx",
]

DESTINATION_ROOT = "/Game/NocturneSignal/AnimationSources/MotifectSword"
ANIMATION_DESTINATION = DESTINATION_ROOT + "/Animations"
SOURCE_SKELETON_PATH = (
    "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/"
    "SK_MCO_TC_Sword_Mannequin_Skeleton.SK_MCO_TC_Sword_Mannequin_Skeleton"
)


def log(message):
    unreal.log("[NocturneMotifectSwordImport] " + str(message))


def require_file(path):
    if not os.path.exists(path):
        raise RuntimeError("Required Motifect sword source file is missing: " + path)


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


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


def load_imported_animation(name):
    asset_path = ANIMATION_DESTINATION + "/" + name + "." + name
    return unreal.EditorAssetLibrary.load_asset(asset_path)


def main():
    skeleton = load_asset(SOURCE_SKELETON_PATH)
    animation_paths = [os.path.join(SOURCE_ROOT, file_name) for file_name in ANIMATION_FBX_FILES]
    for animation_path in animation_paths:
        require_file(animation_path)

    unreal.EditorAssetLibrary.make_directory(DESTINATION_ROOT)
    unreal.EditorAssetLibrary.make_directory(ANIMATION_DESTINATION)

    tasks = [make_animation_import_task(path, skeleton) for path in animation_paths]
    import_error = None
    try:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    except RuntimeError as exc:
        # Motifect FBXs include facial tracks that the mannequin skeleton does not have.
        # Unreal still creates usable body animation assets; verify that before accepting.
        message = str(exc)
        expected_fragments = ["RightEye", "LeftEye", "Jaw"]
        if not all(fragment in message for fragment in expected_fragments):
            raise
        import_error = message

    imported = []
    for task in tasks:
        imported.extend(task.imported_object_paths)

    if import_error:
        imported = []
        missing = []
        for path in animation_paths:
            name = os.path.splitext(os.path.basename(path))[0]
            asset = load_imported_animation(name)
            if asset:
                imported.append(asset.get_path_name())
            else:
                missing.append(name)
        if missing:
            raise RuntimeError(
                "Motifect import reported facial-track warnings but these assets are missing: "
                + ", ".join(missing)
            )
        log("Accepted Motifect import with ignored facial-track warnings for Jaw/LeftEye/RightEye.")

    if len(imported) != len(animation_paths):
        raise RuntimeError(
            f"Expected {len(animation_paths)} Motifect imports, got {len(imported)}: {imported}"
        )

    unreal.EditorAssetLibrary.save_directory(DESTINATION_ROOT, only_if_is_dirty=False, recursive=True)

    log("Import complete:")
    for path in imported:
        log("  " + path)

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterMotifectSwordImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
