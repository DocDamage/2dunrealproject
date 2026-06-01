from __future__ import annotations

import json
import os
from pathlib import Path

import unreal


PROJECT_ROOT = Path(unreal.Paths.project_dir())
SOURCE_ROOT = Path(r"G:\Nocturne Signal\2dunrealproject\SourceArt\Jacob")
SOURCE_FBX = SOURCE_ROOT / "Jacob_NocturneCharacterOnly.fbx"
DESTINATION = "/Game/RealmArchitect/Art/Jacob"
REPORT_PATH = PROJECT_ROOT / "Docs" / "ra_jacob_import_report.json"


TEXTURE_SOURCES = [
    SOURCE_ROOT / "textures" / "Scene.png",
    SOURCE_ROOT / "textures" / "T_JacobColor.png",
    SOURCE_ROOT / "textures" / "T_PropsAtlas.png",
]


def make_fbx_options() -> unreal.FbxImportUI:
    options = unreal.FbxImportUI()
    options.set_editor_property("automated_import_should_detect_type", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("import_materials", True)
    options.set_editor_property("import_textures", True)
    options.set_editor_property("create_physics_asset", True)
    options.skeletal_mesh_import_data.set_editor_property("import_meshes_in_bone_hierarchy", True)
    options.anim_sequence_import_data.set_editor_property(
        "animation_length",
        unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME,
    )
    return options


def make_fbx_task() -> unreal.AssetImportTask:
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(SOURCE_FBX))
    task.set_editor_property("destination_path", DESTINATION)
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("replace_existing_settings", False)
    task.set_editor_property("options", make_fbx_options())
    return task


def main() -> None:
    unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")

    if not SOURCE_FBX.exists():
        raise RuntimeError(f"Jacob source FBX was not found: {SOURCE_FBX}")

    # Texture AssetImportTask uses Interchange in UE 5.7 and tries to sync the
    # Content Browser, which is not available in commandlet mode. The legacy FBX
    # importer is safe headlessly, so this pass imports the FBX and reports the
    # texture sources it was allowed to reference.
    texture_sources = [str(path) for path in TEXTURE_SOURCES if path.exists()]
    missing_textures = [str(path) for path in TEXTURE_SOURCES if not path.exists()]

    tasks = [make_fbx_task()]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    imported = []
    failed = []
    for task in tasks:
        source = str(task.get_editor_property("filename"))
        paths = list(task.get_editor_property("imported_object_paths") or [])
        if paths:
            imported.append({"source": source, "imported": paths})
        else:
            failed.append(source)

    unreal.EditorAssetLibrary.save_directory(DESTINATION, only_if_is_dirty=False, recursive=True)

    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous([DESTINATION], force_rescan=True)
    assets = registry.get_assets_by_path(DESTINATION, recursive=True)
    counts_by_class: dict[str, int] = {}
    discovered_assets = []
    for asset in assets:
        class_name = str(asset.asset_class_path.asset_name)
        counts_by_class[class_name] = counts_by_class.get(class_name, 0) + 1
        discovered_assets.append(
            {
                "asset": str(asset.package_name),
                "class": class_name,
            }
        )

    report = {
        "source_fbx": str(SOURCE_FBX),
        "texture_sources": texture_sources,
        "missing_texture_sources": missing_textures,
        "destination": DESTINATION,
        "tasks": len(tasks),
        "imported_sources": len(imported),
        "failed_sources": failed,
        "counts_by_class": dict(sorted(counts_by_class.items())),
        "imported": imported,
        "discovered_assets": sorted(discovered_assets, key=lambda item: item["asset"]),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    unreal.log(f"Jacob import report written: {REPORT_PATH}")

    if failed:
        raise RuntimeError(f"Jacob import failed for {len(failed)} source files")

    if os.environ.get("RA_QUIT_AFTER_SCRIPT") == "1":
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    main()
