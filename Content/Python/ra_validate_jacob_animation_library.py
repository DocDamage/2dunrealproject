from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import unreal


PROJECT_ROOT = Path(unreal.Paths.project_dir())
REPORT_PATH = PROJECT_ROOT / "Docs" / "ra_jacob_animation_library_validation.json"
JACOB_ROOT_DIR = "/Game/RealmArchitect/Art/Jacob"
RETARGETED_ANIM_DIR = "/Game/RealmArchitect/Art/Jacob/RetargetedAnimations"
JACOB_SKELETON_PATH = "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Skeleton.Jacob_NocturneCharacterOnly_Skeleton"


def package_dir(path: str) -> str:
    package = path.rsplit(".", 1)[0]
    return package.rsplit("/", 1)[0]


def main() -> None:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous([JACOB_ROOT_DIR], force_rescan=True)

    jacob_skeleton = unreal.load_asset(JACOB_SKELETON_PATH)
    failures = []
    animations = {}
    counts_by_dir = Counter()

    if not jacob_skeleton:
        failures.append({"key": "JacobSkeleton", "path": JACOB_SKELETON_PATH, "reason": "load_failed"})

    paths = unreal.EditorAssetLibrary.list_assets(JACOB_ROOT_DIR, recursive=True, include_folder=False)
    for path in sorted(paths):
        asset = unreal.load_asset(path)
        if not asset or asset.get_class().get_name() != "AnimSequence":
            continue

        skeleton = asset.get_skeleton() if hasattr(asset, "get_skeleton") else None
        play_length = asset.get_play_length() if hasattr(asset, "get_play_length") else 0.0
        package = path.rsplit(".", 1)[0]
        counts_by_dir[package_dir(path)] += 1

        animations[asset.get_name()] = {
            "path": path,
            "package": package,
            "directory": package_dir(path),
            "skeleton": skeleton.get_path_name() if skeleton else None,
            "play_length": play_length,
        }

        if skeleton != jacob_skeleton:
            failures.append({"key": asset.get_name(), "path": path, "reason": "wrong_skeleton"})
        elif play_length <= 0.0:
            failures.append({"key": asset.get_name(), "path": path, "reason": "empty_animation"})

    retargeted_count = sum(count for directory, count in counts_by_dir.items() if directory.startswith(RETARGETED_ANIM_DIR))
    report = {
        "root_directory": JACOB_ROOT_DIR,
        "retargeted_directory": RETARGETED_ANIM_DIR,
        "expected_skeleton": JACOB_SKELETON_PATH,
        "animation_count": len(animations),
        "retargeted_animation_count": retargeted_count,
        "counts_by_directory": dict(sorted(counts_by_dir.items())),
        "animations": animations,
        "failures": failures,
        "result": "passed" if not failures else "failed",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    unreal.log(f"Jacob animation library validation report written: {REPORT_PATH}")

    if failures:
        raise RuntimeError(f"Jacob animation library validation failed: {failures}")


if __name__ == "__main__":
    main()
