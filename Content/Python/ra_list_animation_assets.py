import json
import os
import re
from collections import Counter, defaultdict

import unreal


PROJECT_ROOT = unreal.SystemLibrary.get_project_directory()
REPORT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "Docs", "ra_animation_asset_inventory.json"))


def asset_class_name(asset_data):
    class_path = asset_data.asset_class_path
    try:
        asset_name = str(class_path.asset_name)
        if asset_name and asset_name.lower() != "none":
            return asset_name
    except Exception:
        pass

    class_path_text = str(class_path)
    match = re.search(r'AssetName="([^"]+)"', class_path_text)
    if match:
        return match.group(1)
    return class_path_text.rsplit(".", 1)[-1]


def asset_object_path(asset_data):
    try:
        return str(asset_data.object_path)
    except Exception:
        return "{0}.{1}".format(asset_data.package_name, asset_data.asset_name)


def main():
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.search_all_assets(True)

    class_names = {
        "AnimSequence",
        "AnimBlueprint",
        "BlendSpace",
        "BlendSpace1D",
        "AimOffsetBlendSpace",
        "AimOffsetBlendSpace1D",
        "AnimMontage",
    }

    animation_assets = []
    package_counts = Counter()
    class_counts = Counter()
    examples_by_package = defaultdict(list)

    for asset_data in registry.get_assets_by_path("/Game", recursive=True):
        class_name = asset_class_name(asset_data)
        if class_name not in class_names:
            continue

        object_path = asset_object_path(asset_data)
        package_name = str(asset_data.package_name)
        parts = package_name.split("/")
        root = "/".join(parts[:3]) if len(parts) >= 3 else package_name

        animation_assets.append(
            {
                "name": str(asset_data.asset_name),
                "class": class_name,
                "object_path": object_path,
                "package_name": package_name,
                "root": root,
            }
        )
        class_counts[class_name] += 1
        package_counts[root] += 1
        if len(examples_by_package[root]) < 12:
            examples_by_package[root].append(object_path)

    report = {
        "total_animation_assets": len(animation_assets),
        "counts_by_class": dict(sorted(class_counts.items())),
        "counts_by_root": dict(package_counts.most_common()),
        "examples_by_root": dict(sorted(examples_by_package.items())),
        "assets": sorted(animation_assets, key=lambda item: item["object_path"]),
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    unreal.log("Animation asset inventory written to {0}".format(REPORT_PATH))
    unreal.log("Total animation assets: {0}".format(len(animation_assets)))
    for root, count in package_counts.most_common(20):
        unreal.log("{0}: {1}".format(root, count))


main()
