import os

import unreal


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_FILE = os.path.join(PROJECT_ROOT, "SourceArt", "Tentacles", "RoboticTentacleHands", "hand_18.glb")
DESTINATION = "/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands"


def log(message):
    unreal.log("[NocturneTentacleImport] " + str(message))


def main():
    if not os.path.exists(SOURCE_FILE):
        raise RuntimeError("Missing robotic tentacle GLB source file: " + SOURCE_FILE)

    unreal.EditorAssetLibrary.make_directory(DESTINATION)

    task = unreal.AssetImportTask()
    task.filename = SOURCE_FILE
    task.destination_path = DESTINATION
    task.destination_name = "RoboticTentacleHands"
    task.automated = True
    task.replace_existing = True
    task.save = True

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.EditorAssetLibrary.save_directory(DESTINATION, only_if_is_dirty=False, recursive=True)

    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path(DESTINATION, recursive=True)
    log(f"Robotic Tentacle Hands import finished with {len(assets)} assets under {DESTINATION}")
    for asset in assets:
        log(f"  {asset.package_name} ({asset.asset_class_path.asset_name})")

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterTentacleImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
