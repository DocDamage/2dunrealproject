import inspect

import unreal


def log(message):
    unreal.log("[NocturneSkeletonInspect] " + str(message))


ASSETS = [
    "/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton",
    "/Game/RamsterZ_FreeAnims_Volume1/Demo/Mannequin/Character/Mesh/UE4_Mannequin_Skeleton.UE4_Mannequin_Skeleton",
    "/Game/A_Surface_Footstep/Mannequin/Character/Mesh/UE4_Mannequin_Skeleton.UE4_Mannequin_Skeleton",
    "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/SK/Vefects_Vexa_Skeleton.Vefects_Vexa_Skeleton",
]


def object_methods(name):
    cls = getattr(unreal, name, None)
    if cls is None:
        return
    log(f"METHODS {name} BEGIN")
    for method in sorted(item for item in dir(cls) if not item.startswith("_")):
        if any(token in method.lower() for token in ("retarget", "export", "asset", "source", "target", "chain", "create", "controller", "duplicate", "batch", "run")):
            log(f"  {method}")
    log(f"METHODS {name} END")


def skeleton_bones(asset_path):
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    log(f"ASSET {asset_path}: loaded={bool(asset)} class={asset.get_class().get_name() if asset else 'None'}")
    if not asset:
        return

    try:
        ref = asset.get_reference_skeleton()
        count = ref.get_num()
        names = [str(ref.get_bone_name(i)) for i in range(count)]
        log(f"  bone_count={count}")
        log("  first_80=" + ", ".join(names[:80]))
    except Exception as exc:
        log("  get_reference_skeleton failed: " + repr(exc))

    for attr in ("get_bone_tree", "get_bone_names"):
        try:
            value = getattr(asset, attr)()
            log(f"  {attr}: {value[:20] if hasattr(value, '__getitem__') else value}")
        except Exception as exc:
            log(f"  {attr} failed: {repr(exc)}")


def main():
    for name in [
        "IKRigController",
        "IKRetargeterController",
        "IKRetargetBatchOperation",
        "IKRigDefinitionFactory",
        "IKRetargetFactory",
        "AssetTools",
    ]:
        object_methods(name)

    for asset_path in ASSETS:
        skeleton_bones(asset_path)


main()
