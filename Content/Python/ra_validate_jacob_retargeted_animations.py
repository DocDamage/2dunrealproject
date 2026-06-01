from __future__ import annotations

import json
from pathlib import Path

import unreal


PROJECT_ROOT = Path(unreal.Paths.project_dir())
REPORT_PATH = PROJECT_ROOT / "Docs" / "ra_jacob_retargeted_animation_validation.json"
RETARGETED_ANIM_DIR = "/Game/RealmArchitect/Art/Jacob/RetargetedAnimations"
JACOB_SKELETON_PATH = "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Skeleton.Jacob_NocturneCharacterOnly_Skeleton"

REQUIRED_ANIMATIONS = [
    "JacobRTG_MM_Idle",
    "JacobRTG_MF_Unarmed_Walk_Fwd",
    "JacobRTG_MF_Unarmed_Jog_Fwd",
    "JacobRTG_MM_Jump",
    "JacobRTG_MM_Fall_Loop",
    "JacobRTG_MM_Land",
]


def animation_path(name: str) -> str:
    return f"{RETARGETED_ANIM_DIR}/{name}.{name}"


def main() -> None:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous([RETARGETED_ANIM_DIR], force_rescan=True)

    jacob_skeleton = unreal.load_asset(JACOB_SKELETON_PATH)
    failures = []
    animations = {}

    if not jacob_skeleton:
        failures.append({"key": "JacobSkeleton", "path": JACOB_SKELETON_PATH, "reason": "load_failed"})

    for name in REQUIRED_ANIMATIONS:
        path = animation_path(name)
        asset = unreal.load_asset(path)
        skeleton = asset.get_skeleton() if asset and hasattr(asset, "get_skeleton") else None
        play_length = asset.get_play_length() if asset and hasattr(asset, "get_play_length") else 0.0

        animations[name] = {
            "path": path,
            "loaded": asset is not None,
            "class": asset.get_class().get_name() if asset else None,
            "skeleton": skeleton.get_path_name() if skeleton else None,
            "play_length": play_length,
        }

        if not asset:
            failures.append({"key": name, "path": path, "reason": "load_failed"})
        elif asset.get_class().get_name() != "AnimSequence":
            failures.append({"key": name, "path": path, "reason": "not_anim_sequence"})
        elif skeleton != jacob_skeleton:
            failures.append({"key": name, "path": path, "reason": "wrong_skeleton"})
        elif play_length <= 0.0:
            failures.append({"key": name, "path": path, "reason": "empty_animation"})

    report = {
        "directory": RETARGETED_ANIM_DIR,
        "expected_skeleton": JACOB_SKELETON_PATH,
        "animations": animations,
        "failures": failures,
        "result": "passed" if not failures else "failed",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    unreal.log(f"Jacob retargeted animation validation report written: {REPORT_PATH}")

    if failures:
        raise RuntimeError(f"Jacob retargeted animation validation failed: {failures}")


if __name__ == "__main__":
    main()
