from __future__ import annotations

import json
from pathlib import Path

import unreal


PROJECT_ROOT = Path(unreal.Paths.project_dir())
DESTINATION = "/Game/RealmArchitect/Art/Jacob"
REPORT_PATH = PROJECT_ROOT / "Docs" / "ra_jacob_validation.json"

REQUIRED_ASSETS = {
    "JacobMesh": "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly.Jacob_NocturneCharacterOnly",
    "JacobSkeleton": "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Skeleton.Jacob_NocturneCharacterOnly_Skeleton",
    "JacobIdle": "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_Idle.Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_Idle",
    "JacobReadySword": "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_ReadySword.Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_ReadySword",
}

ANIMATION_NAME_HINTS = [
    "Idle",
    "ReadySword",
]


def main() -> None:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous([DESTINATION], force_rescan=True)
    assets = registry.get_assets_by_path(DESTINATION, recursive=True)

    counts_by_class: dict[str, int] = {}
    animation_assets = []
    for asset in assets:
        class_name = str(asset.asset_class_path.asset_name)
        package_name = str(asset.package_name)
        counts_by_class[class_name] = counts_by_class.get(class_name, 0) + 1
        if class_name == "AnimSequence":
            animation_assets.append(package_name)

    loaded_assets = {}
    failures = []
    for key, path in REQUIRED_ASSETS.items():
        loaded = unreal.load_asset(path)
        loaded_assets[key] = {
            "path": path,
            "loaded": loaded is not None,
            "class": loaded.get_class().get_name() if loaded else None,
        }
        if loaded is None:
            failures.append({"key": key, "path": path, "reason": "load_failed"})

    for hint in ANIMATION_NAME_HINTS:
        if not any(hint.lower() in asset.lower() for asset in animation_assets):
            failures.append({"key": hint, "path": DESTINATION, "reason": "missing_animation_hint"})

    report = {
        "destination": DESTINATION,
        "counts_by_class": dict(sorted(counts_by_class.items())),
        "loaded_assets": loaded_assets,
        "animation_assets": sorted(animation_assets),
        "failures": failures,
        "result": "passed" if not failures else "failed",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    unreal.log(f"Jacob validation report written: {REPORT_PATH}")

    if failures:
        raise RuntimeError(f"Jacob validation failed: {failures}")


if __name__ == "__main__":
    main()
