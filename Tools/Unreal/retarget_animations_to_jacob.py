import os

import unreal


TARGET_MESH_PATH = "/Game/NocturneSignal/Characters/Jacob/SK_Jacob.SK_Jacob"
RETARGETING_ROOT = "/Game/NocturneSignal/Characters/Jacob/Retargeting"
OUTPUT_ROOT = "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations"

SOURCE_SETS = [
    {
        "name": "RamsterZ",
        "mesh": "/Game/RamsterZ_FreeAnims_Volume1/Demo/Mannequin/Character/Mesh/SK_Mannequin.SK_Mannequin",
        "root": "/Game/RamsterZ_FreeAnims_Volume1/AnimationSequence",
        "output": OUTPUT_ROOT + "/RamsterZ",
    },
    {
        "name": "MCOTCSword",
        "mesh": "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/SK_MCO_TC_Sword_Mannequin.SK_MCO_TC_Sword_Mannequin",
        "root": "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/Animations",
        "output": OUTPUT_ROOT + "/MCO_TC_Sword",
    },
    {
        "name": "MotifectSword",
        "mesh": "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/SK_MCO_TC_Sword_Mannequin.SK_MCO_TC_Sword_Mannequin",
        "root": "/Game/NocturneSignal/AnimationSources/MotifectSword/Animations",
        "output": OUTPUT_ROOT + "/MotifectSword",
    },
    {
        "name": "MotifectMartialArts",
        "mesh": "/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/SK_MCO_TC_Sword_Mannequin.SK_MCO_TC_Sword_Mannequin",
        "root": "/Game/NocturneSignal/AnimationSources/MotifectMartialArts/Animations",
        "output": OUTPUT_ROOT + "/MotifectMartialArts",
    },
    {
        "name": "RealisticCombatMoves",
        "mesh": "/Game/NocturneSignal/AnimationSources/RealisticCombatMoves/SK_RealisticCombat_MaleLowpoly.SK_RealisticCombat_MaleLowpoly",
        "root": "/Game/NocturneSignal/AnimationSources/RealisticCombatMoves/Animations",
        "output": OUTPUT_ROOT + "/RealisticCombatMoves",
    },
    {
        "name": "AdvancedLocomotionMechanicsUE5",
        "mesh": "/Game/Mesh/Skeletal/Default/SKM_Manny.SKM_Manny",
        "root": "/Game/Animation/Assets",
        "output": OUTPUT_ROOT + "/AdvancedLocomotionMechanicsUE5",
    },
    {
        "name": "UniversalAnimationLibrary1",
        "mesh": "/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary1/SK_UAL1_Mannequin.SK_UAL1_Mannequin",
        "root": "/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary1",
        "output": OUTPUT_ROOT + "/UniversalAnimationLibrary1",
    },
    {
        "name": "UniversalAnimationLibrary2",
        "mesh": "/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary2/SK_UAL2_Mannequin.SK_UAL2_Mannequin",
        "root": "/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary2",
        "output": OUTPUT_ROOT + "/UniversalAnimationLibrary2",
    },
    {
        "name": "ActorCoreWalk",
        "mesh": "/Game/NocturneSignal/AnimationSources/ActorCore/SK_ActorCore_MotionDummyMale.SK_ActorCore_MotionDummyMale",
        "root": "/Game/NocturneSignal/AnimationSources/ActorCore/Walk/Animations",
        "output": OUTPUT_ROOT + "/ActorCoreWalk",
    },
    {
        "name": "ActorCoreTactical",
        "mesh": "/Game/NocturneSignal/AnimationSources/ActorCore/SK_ActorCore_MotionDummyMale.SK_ActorCore_MotionDummyMale",
        "root": "/Game/NocturneSignal/AnimationSources/ActorCore/Tactical/Animations",
        "output": OUTPUT_ROOT + "/ActorCoreTactical",
    },
    {
        "name": "GameAnimationSample",
        "mesh": "/Game/Mesh/Skeletal/Default/SKM_Manny.SKM_Manny",
        "root": "/Game/NocturneSignal/AnimationSources/GameAnimationSample/Animations",
        "output": OUTPUT_ROOT + "/GameAnimationSample",
    },
    {
        "name": "ParagonMannyCurated",
        "mesh": "/Game/Mesh/Skeletal/Default/SKM_Manny.SKM_Manny",
        "root": "/Game/NocturneSignal/AnimationSources/ParagonMannyCurated/Animations",
        "output": OUTPUT_ROOT + "/ParagonMannyCurated",
    },
    {
        "name": "FightAnimationMocapPack",
        "mesh": "/Game/NocturneSignal/AnimationSources/FightAnimationMocapPack/SK_FightMocap_MaleLowpoly.SK_FightMocap_MaleLowpoly",
        "root": "/Game/NocturneSignal/AnimationSources/FightAnimationMocapPack/Animations",
        "output": OUTPUT_ROOT + "/FightAnimationMocapPack",
    },
    {
        "name": "SurfaceFootstep",
        "mesh": "/Game/A_Surface_Footstep/Mannequin/Character/Mesh/SK_Mannequin.SK_Mannequin",
        "root": "/Game/A_Surface_Footstep/Mannequin/Animations",
        "output": OUTPUT_ROOT + "/SurfaceFootstep",
    },
    {
        "name": "VefectsVexa",
        "mesh": "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/SK/SK_Vefects_Vexa.SK_Vefects_Vexa",
        "root": "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/Animations",
        "output": OUTPUT_ROOT + "/VefectsVexa",
    },
    {
        "name": "FreeAnimationsPack",
        "mesh": "/Game/FreeAnimationsPack/Demo/Characters/Mannequins/Meshes/SKM_Manny.SKM_Manny",
        "root": "/Game/FreeAnimationsPack/Animations",
        "output": OUTPUT_ROOT + "/FreeAnimationsPack",
    },
    {
        "name": "RogueCharacter",
        "mesh": "/Game/RogueCharacter/Meshes/SKM_Rogue_Main.SKM_Rogue_Main",
        "mesh_candidates": [
            "/Game/RogueCharacter/Meshes/SKM_Rogue_Main.SKM_Rogue_Main",
            "/Game/RogueCharacter/Meshes/SK_Rogue_Main.SK_Rogue_Main",
        ],
        "root": "/Game/RogueCharacter/Animations/RogueAnimations",
        "output": OUTPUT_ROOT + "/RogueCharacter",
    },
]


def log(message):
    unreal.log("[NocturneJacobRetarget] " + str(message))


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


def ensure_dir(path):
    unreal.EditorAssetLibrary.make_directory(path)


def get_or_create_ik_rig(name, skeletal_mesh):
    ensure_dir(RETARGETING_ROOT)
    asset_path = RETARGETING_ROOT + "/" + name
    existing = unreal.EditorAssetLibrary.load_asset(asset_path + "." + name)
    if existing:
        rig = existing
    else:
        rig = unreal.IKRigDefinitionFactory().create_new_ik_rig_asset(RETARGETING_ROOT, name)
        if not rig:
            raise RuntimeError("Failed to create IK Rig: " + asset_path)

    controller = unreal.IKRigController.get_controller(rig)
    controller.set_skeletal_mesh(skeletal_mesh)
    controller.apply_auto_generated_retarget_definition()
    unreal.EditorAssetLibrary.save_loaded_asset(rig)
    return rig


def get_or_create_retargeter(name, source_rig, source_mesh, target_rig, target_mesh):
    ensure_dir(RETARGETING_ROOT)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_path = RETARGETING_ROOT + "/" + name
    existing = unreal.EditorAssetLibrary.load_asset(asset_path + "." + name)
    if existing:
        retargeter = existing
    else:
        retargeter = asset_tools.create_asset(name, RETARGETING_ROOT, unreal.IKRetargeter, unreal.IKRetargetFactory())
        if not retargeter:
            raise RuntimeError("Failed to create IK Retargeter: " + asset_path)

    controller = unreal.IKRetargeterController.get_controller(retargeter)
    controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_rig)
    controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)
    controller.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE, source_mesh)
    controller.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET, target_mesh)
    controller.add_default_ops()
    controller.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
    unreal.EditorAssetLibrary.save_loaded_asset(retargeter)
    return retargeter


def anim_assets_under(path):
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path(path, recursive=True)
    return [
        asset
        for asset in assets
        if str(asset.asset_class_path.asset_name) == "AnimSequence"
    ]


def resolve_source_mesh_path(source_set):
    candidates = source_set.get("mesh_candidates", [source_set["mesh"]])
    for candidate in candidates:
        if unreal.EditorAssetLibrary.does_asset_exist(candidate):
            return candidate
    return None


def retarget_set(source_set, target_rig, target_mesh, limit=0):
    source_mesh_path = resolve_source_mesh_path(source_set)
    if not source_mesh_path:
        candidates = ", ".join(source_set.get("mesh_candidates", [source_set["mesh"]]))
        log(f"{source_set['name']}: source mesh is missing, skipping: {candidates}")
        return []

    source_mesh = load_asset(source_mesh_path)
    source_rig = get_or_create_ik_rig("IK_" + source_set["name"], source_mesh)
    retargeter = get_or_create_retargeter(
        "RTG_" + source_set["name"] + "_To_Jacob",
        source_rig,
        source_mesh,
        target_rig,
        target_mesh,
    )

    ensure_dir(source_set["output"])
    anim_assets = anim_assets_under(source_set["root"])
    anim_name_filter = {
        item.strip().lower()
        for item in os.environ.get("NOCTURNE_RETARGET_ANIM_NAMES", "").split(",")
        if item.strip()
    }
    if anim_name_filter:
        anim_assets = [
            asset
            for asset in anim_assets
            if str(asset.asset_name).lower() in anim_name_filter
        ]
    if limit:
        anim_assets = anim_assets[:limit]

    log(f"{source_set['name']}: retargeting {len(anim_assets)} animations to {source_set['output']}")
    if not anim_assets:
        return []

    results = unreal.IKRetargetBatchOperation.duplicate_and_retarget(
        anim_assets,
        source_mesh,
        target_mesh,
        retargeter,
        "",
        "",
        "JAC_",
        "",
        False,
        True,
    )

    imported_paths = []
    for asset in results:
        generated_path = str(asset.package_name)
        target_path = source_set["output"] + "/" + str(asset.asset_name)
        if generated_path != target_path:
            if unreal.EditorAssetLibrary.does_asset_exist(target_path):
                unreal.EditorAssetLibrary.delete_asset(target_path)
            if not unreal.EditorAssetLibrary.rename_asset(generated_path, target_path):
                raise RuntimeError(f"Failed to move retargeted asset {generated_path} to {target_path}")
        imported_paths.append(target_path)

    for path in imported_paths:
        log("  " + path)
    unreal.EditorAssetLibrary.save_directory(source_set["output"], only_if_is_dirty=False, recursive=True)
    return imported_paths


def main():
    target_mesh = load_asset(TARGET_MESH_PATH)
    target_rig = get_or_create_ik_rig("IK_Jacob", target_mesh)

    limit_text = os.environ.get("NOCTURNE_RETARGET_LIMIT", "0").strip()
    limit = int(limit_text) if limit_text else 0
    source_filter = {
        item.strip().lower()
        for item in os.environ.get("NOCTURNE_RETARGET_SOURCES", "").split(",")
        if item.strip()
    }

    all_paths = []
    for source_set in SOURCE_SETS:
        if source_filter and source_set["name"].lower() not in source_filter:
            continue
        all_paths.extend(retarget_set(source_set, target_rig, target_mesh, limit=limit))

    unreal.EditorAssetLibrary.save_directory(RETARGETING_ROOT, only_if_is_dirty=False, recursive=True)
    unreal.EditorAssetLibrary.save_directory(OUTPUT_ROOT, only_if_is_dirty=False, recursive=True)
    log(f"Retarget complete. Created/updated {len(all_paths)} animation assets.")

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterJacobRetarget" in command_line:
        unreal.SystemLibrary.quit_editor()


main()
