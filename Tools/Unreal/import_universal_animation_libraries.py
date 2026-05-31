import os

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

IMPORTS = [
    {
        "name": "UniversalAnimationLibrary1",
        "fbx": os.path.join(
            PROJECT_ROOT,
            "SourceArt",
            "AnimationSources",
            "UniversalAnimationLibrary1",
            "UAL1_Standard.fbx",
        ),
        "destination": "/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary1",
        "mesh_name": "SK_UAL1_Mannequin",
    },
    {
        "name": "UniversalAnimationLibrary2",
        "fbx": os.path.join(
            PROJECT_ROOT,
            "SourceArt",
            "AnimationSources",
            "UniversalAnimationLibrary2",
            "UAL2_Standard.fbx",
        ),
        "destination": "/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary2",
        "mesh_name": "SK_UAL2_Mannequin",
    },
]


def log(message):
    unreal.log("[NocturneUniversalAnimImport] " + str(message))


def require_file(path):
    if not os.path.exists(path):
        raise RuntimeError("Required Universal Animation Library source file is missing: " + path)


def make_import_task(item):
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)

    task = unreal.AssetImportTask()
    task.filename = item["fbx"]
    task.destination_path = item["destination"]
    task.destination_name = item["mesh_name"]
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = options
    return task


def imported_anim_names(destination):
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path(destination, recursive=True)
    return sorted(
        str(asset.asset_name)
        for asset in assets
        if str(asset.asset_class_path.asset_name) == "AnimSequence"
    )


def main():
    for item in IMPORTS:
        require_file(item["fbx"])
        unreal.EditorAssetLibrary.make_directory(item["destination"])

    tasks = [make_import_task(item) for item in IMPORTS]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    for item in IMPORTS:
        unreal.EditorAssetLibrary.save_directory(item["destination"], only_if_is_dirty=False, recursive=True)
        names = imported_anim_names(item["destination"])
        log(f"{item['name']}: imported/available {len(names)} AnimSequences")
        for name in names:
            if any(token in name.lower() for token in ["jump", "slide"]):
                log("  traversal candidate: " + name)

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterUniversalAnimImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
