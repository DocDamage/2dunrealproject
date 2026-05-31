import unreal


def log(message):
    unreal.log("[NocturneRetargetInspect] " + str(message))


def main():
    names = [name for name in dir(unreal) if "Retarget" in name or "IKRig" in name or "IK" in name]
    log("API_NAMES_BEGIN")
    for name in sorted(names):
        log(name)
    log("API_NAMES_END")

    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    roots = [
        "/Game/RamsterZ_FreeAnims_Volume1",
        "/Game/A_Surface_Footstep",
        "/Game/Vefects",
        "/Game/NocturneSignal/Characters/Jacob",
        "/Game/Fab/Realistic_Combat_Moves_10_Mocap_Pack",
    ]
    for root in roots:
        assets = registry.get_assets_by_path(root, recursive=True)
        anims = [asset for asset in assets if str(asset.asset_class_path.asset_name) in ("AnimSequence", "AnimationSequence")]
        skeletons = [asset for asset in assets if str(asset.asset_class_path.asset_name) == "Skeleton"]
        skeletal_meshes = [asset for asset in assets if str(asset.asset_class_path.asset_name) == "SkeletalMesh"]
        log(f"ROOT {root}: assets={len(assets)} anims={len(anims)} skeletons={len(skeletons)} skeletal_meshes={len(skeletal_meshes)}")
        for asset in anims[:10]:
            log(f"  ANIM {asset.package_name} class={asset.asset_class_path.asset_name}")
        for asset in skeletons:
            log(f"  SKELETON {asset.package_name}")
        for asset in skeletal_meshes:
            log(f"  SKELMESH {asset.package_name}")


main()
