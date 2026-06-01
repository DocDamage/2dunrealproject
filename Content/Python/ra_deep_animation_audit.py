from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import unreal


PROJECT_ROOT = Path(unreal.Paths.project_dir())
REPORT_PATH = PROJECT_ROOT / "Docs" / "ra_deep_animation_audit.json"

ANIMATION_CLASSES = {
    "AnimSequence",
    "AnimMontage",
    "BlendSpace",
    "BlendSpace1D",
    "AimOffsetBlendSpace",
    "AimOffsetBlendSpace1D",
    "AnimBlueprint",
}

KEYWORDS = {
    "attack": ["attack", "slash", "sword", "hit", "punch", "kick", "combat", "melee", "shoot"],
    "damage": ["damage", "hurt", "gothit", "hitreact", "impact"],
    "death": ["death", "die", "dying", "dead"],
    "locomotion": ["idle", "walk", "run", "jog", "sprint", "jump", "fall", "land", "crouch", "roll", "dodge", "strafe"],
    "magic": ["spell", "cast", "magic", "aura", "fire", "zap", "ns_"],
}


def asset_class_name(asset_data: unreal.AssetData) -> str:
    return str(asset_data.asset_class_path.asset_name)


def object_path(asset_data: unreal.AssetData) -> str:
    try:
        return str(asset_data.object_path)
    except Exception:
        return f"{asset_data.package_name}.{asset_data.asset_name}"


def top_folder(package_name: str) -> str:
    parts = package_name.split("/")
    return "/".join(parts[:4]) if len(parts) >= 4 else package_name


def categories_for(path: str) -> list[str]:
    text = path.lower()
    categories = []
    for category, words in KEYWORDS.items():
        if any(word in text for word in words):
            categories.append(category)
    return categories or ["other"]


def asset_skeleton(asset) -> str | None:
    if hasattr(asset, "get_skeleton"):
        skeleton = asset.get_skeleton()
        return skeleton.get_path_name() if skeleton else None
    return None


def asset_play_length(asset) -> float | None:
    if hasattr(asset, "get_play_length"):
        try:
            return float(asset.get_play_length())
        except Exception:
            return None
    return None


def main() -> None:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.search_all_assets(True)

    assets = []
    counts_by_class = Counter()
    counts_by_skeleton = Counter()
    counts_by_root = Counter()
    counts_by_category = Counter()
    examples_by_skeleton = defaultdict(list)

    for asset_data in registry.get_assets_by_path("/Game", recursive=True):
        class_name = asset_class_name(asset_data)
        package_name = str(asset_data.package_name)
        name = str(asset_data.asset_name)
        path = object_path(asset_data)

        likely_animation_name = any(word in path.lower() for words in KEYWORDS.values() for word in words)
        if class_name not in ANIMATION_CLASSES and not likely_animation_name:
            continue

        asset = None
        skeleton = None
        play_length = None
        if class_name in ANIMATION_CLASSES:
            asset = asset_data.get_asset()
            skeleton = asset_skeleton(asset) if asset else None
            play_length = asset_play_length(asset) if asset else None

        categories = categories_for(path)
        root = top_folder(package_name)
        item = {
            "name": name,
            "class": class_name,
            "object_path": path,
            "package_name": package_name,
            "root": root,
            "skeleton": skeleton,
            "play_length": play_length,
            "categories": categories,
        }
        assets.append(item)

        counts_by_class[class_name] += 1
        counts_by_root[root] += 1
        if skeleton:
            counts_by_skeleton[skeleton] += 1
            if len(examples_by_skeleton[skeleton]) < 20:
                examples_by_skeleton[skeleton].append(path)
        for category in categories:
            counts_by_category[category] += 1

    report = {
        "total_candidates": len(assets),
        "counts_by_class": dict(counts_by_class.most_common()),
        "counts_by_root": dict(counts_by_root.most_common()),
        "counts_by_skeleton": dict(counts_by_skeleton.most_common()),
        "counts_by_category": dict(counts_by_category.most_common()),
        "examples_by_skeleton": dict(sorted(examples_by_skeleton.items())),
        "assets": sorted(assets, key=lambda item: item["object_path"]),
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    unreal.log(f"Deep animation audit written: {REPORT_PATH}")


if __name__ == "__main__":
    main()
