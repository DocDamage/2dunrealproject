import json
import os

import unreal


PROJECT_ROOT = unreal.SystemLibrary.get_project_directory()
REPORT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "Docs", "ra_easycheckpoint_jacob_retarget_report.json"))

RETARGET_DIR = "/Game/RealmArchitect/Art/Jacob/Retargeting"
RETARGETED_ANIM_DIR = "/Game/RealmArchitect/Art/Jacob/RetargetedAnimations"
SOURCE_IKRIG_PATH = RETARGET_DIR + "/IKR_EasyCheckpoint_Manny"
TARGET_IKRIG_PATH = RETARGET_DIR + "/IKR_Jacob_Nocturne"
RETARGETER_PATH = RETARGET_DIR + "/RTG_EasyCheckpoint_to_Jacob"

SOURCE_MESH_PATH = "/Game/EasyCheckpointSystem/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"
TARGET_MESH_PATH = "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly.Jacob_NocturneCharacterOnly"

ANIMATION_PATHS = [
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/MM_Idle.MM_Idle",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Fwd.MF_Unarmed_Walk_Fwd",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Bwd.MF_Unarmed_Walk_Bwd",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Left.MF_Unarmed_Walk_Left",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Right.MF_Unarmed_Walk_Right",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Fwd_Left.MF_Unarmed_Walk_Fwd_Left",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Fwd_Right.MF_Unarmed_Walk_Fwd_Right",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Bwd_Left.MF_Unarmed_Walk_Bwd_Left",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Bwd_Right.MF_Unarmed_Walk_Bwd_Right",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd.MF_Unarmed_Jog_Fwd",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Bwd.MF_Unarmed_Jog_Bwd",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Left.MF_Unarmed_Jog_Left",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Right.MF_Unarmed_Jog_Right",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd_Left.MF_Unarmed_Jog_Fwd_Left",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd_Right.MF_Unarmed_Jog_Fwd_Right",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Bwd_Left.MF_Unarmed_Jog_Bwd_Left",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Bwd_Right.MF_Unarmed_Jog_Bwd_Right",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jump/MM_Jump.MM_Jump",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jump/MM_Fall_Loop.MM_Fall_Loop",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jump/MM_Land.MM_Land",
    "/Game/EasyCheckpointSystem/Characters/Mannequins/Anims/Unarmed/Jump/MM_WallJump.MM_WallJump",
]

SOURCE_CHAINS = [
    ("Spine", "spine_01", "spine_05"),
    ("Head", "neck_01", "head"),
    ("LeftArm", "clavicle_l", "hand_l"),
    ("RightArm", "clavicle_r", "hand_r"),
    ("LeftLeg", "thigh_l", "ball_l"),
    ("RightLeg", "thigh_r", "ball_r"),
]

TARGET_CHAINS = [
    ("Spine", "DEF-CHEST", "DEF-HEAD"),
    ("Head", "DEF-NECK", "DEF-HEAD"),
    ("LeftArm", "DEF-SHOULDER_L", "DEF-HAND_L"),
    ("RightArm", "DEF-SHOULDER_R", "DEF-HAND_R"),
    ("LeftLeg", "DEF-ULEG_L", "DEF-FOOTFINGERS_L"),
    ("RightLeg", "DEF-ULEG_R", "DEF-FOOTFINGERS_R"),
]


def asset_name(long_path):
    return long_path.rsplit("/", 1)[-1]


def load_asset(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: {0}".format(path))
    return asset


def delete_generated_asset(path):
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        if not unreal.EditorAssetLibrary.delete_asset(path):
            raise RuntimeError("Could not delete generated asset: {0}".format(path))


def load_existing_asset(path):
    asset = unreal.load_asset(path)
    if asset:
        return asset

    name = asset_name(path)
    return unreal.load_asset("{0}.{1}".format(path, name))


def create_ikrig(path):
    existing = load_existing_asset(path)
    if existing:
        return existing

    factory = unreal.IKRigDefinitionFactory()
    package_path = path.rsplit("/", 1)[0]
    name = asset_name(path)
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name,
        package_path,
        unreal.IKRigDefinition,
        factory,
    )
    if not asset:
        raise RuntimeError("Could not create IK Rig: {0}".format(path))
    return asset


def create_retargeter(path):
    existing = load_existing_asset(path)
    if existing:
        return existing

    factory = unreal.IKRetargetFactory()
    package_path = path.rsplit("/", 1)[0]
    name = asset_name(path)
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name,
        package_path,
        unreal.IKRetargeter,
        factory,
    )
    if not asset:
        raise RuntimeError("Could not create IK Retargeter: {0}".format(path))
    return asset


def configure_ikrig(ikrig, mesh, root_bone, chains):
    controller = unreal.IKRigController.get_controller(ikrig)
    if not controller.set_skeletal_mesh(mesh):
        raise RuntimeError("Could not set IK Rig skeletal mesh: {0}".format(mesh.get_path_name()))

    autogenerated = False
    try:
        autogenerated = bool(controller.apply_auto_generated_retarget_definition())
    except Exception:
        autogenerated = False

    for chain_name, _start, _end in chains:
        try:
            controller.remove_retarget_chain(chain_name)
        except Exception:
            pass

    if not controller.set_retarget_root(root_bone):
        raise RuntimeError("Could not set retarget root '{0}' on {1}".format(root_bone, ikrig.get_path_name()))

    added = []
    for chain_name, start_bone, end_bone in chains:
        result = controller.add_retarget_chain(chain_name, start_bone, end_bone, "")
        added.append(str(result))

    unreal.EditorAssetLibrary.save_loaded_asset(ikrig)
    return {
        "path": ikrig.get_path_name(),
        "mesh": mesh.get_path_name(),
        "autogenerated_before_manual_override": autogenerated,
        "root": str(controller.get_retarget_root()),
        "chains_added": added,
        "chain_count": len(controller.get_retarget_chains()),
    }


def configure_retargeter(retargeter, source_ikrig, target_ikrig, source_mesh, target_mesh):
    controller = unreal.IKRetargeterController.get_controller(retargeter)
    controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_ikrig)
    controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_ikrig)
    controller.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE, source_mesh)
    controller.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET, target_mesh)
    controller.add_default_ops()
    controller.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, source_ikrig)
    controller.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, target_ikrig)
    controller.auto_map_chains(unreal.AutoMapChainType.EXACT, True)
    # UE 5.7 asserts in AutoAlignAllBones when a custom skeleton has facial/prop
    # bones outside mapped retarget chains. Jacob has many such bones, so keep
    # the explicit chain map and avoid the crashing auto-align pass.

    unreal.EditorAssetLibrary.save_loaded_asset(retargeter)
    mappings = {}
    for chain_name, _start, _end in TARGET_CHAINS:
        mappings[chain_name] = str(controller.get_source_chain(chain_name))

    return {
        "path": retargeter.get_path_name(),
        "num_ops": controller.get_num_retarget_ops(),
        "mappings": mappings,
    }


def animation_asset_data(path):
    asset_data = unreal.EditorAssetLibrary.find_asset_data(path)
    if not asset_data or not asset_data.is_valid():
        raise RuntimeError("Could not find animation asset data: {0}".format(path))
    return asset_data


def prepare_retarget_output_dir():
    if not unreal.EditorAssetLibrary.does_directory_exist(RETARGETED_ANIM_DIR):
        unreal.EditorAssetLibrary.make_directory(RETARGETED_ANIM_DIR)

    for source_path in ANIMATION_PATHS:
        name = "JacobRTG_" + asset_name(source_path.rsplit(".", 1)[0])
        for candidate in [
            "/Game/{0}".format(name),
            "{0}/{1}".format(RETARGETED_ANIM_DIR, name),
        ]:
            if unreal.EditorAssetLibrary.does_asset_exist(candidate):
                unreal.EditorAssetLibrary.delete_asset(candidate)


def move_retargeted_asset(asset):
    old_package = asset.get_path_name().rsplit(".", 1)[0]
    name = asset.get_name()
    desired_package = "{0}/{1}".format(RETARGETED_ANIM_DIR, name)

    if old_package == desired_package:
        unreal.EditorAssetLibrary.save_loaded_asset(asset)
        return asset

    if not unreal.EditorAssetLibrary.rename_asset(old_package, desired_package):
        raise RuntimeError("Could not move retargeted asset from {0} to {1}".format(old_package, desired_package))

    moved = load_asset("{0}.{1}".format(desired_package, name))
    unreal.EditorAssetLibrary.save_loaded_asset(moved)
    return moved


def retarget_animations(source_mesh, target_mesh, retargeter):
    prepare_retarget_output_dir()
    asset_data = [animation_asset_data(path) for path in ANIMATION_PATHS]
    new_assets = unreal.IKRetargetBatchOperation.duplicate_and_retarget(
        asset_data,
        source_mesh,
        target_mesh,
        retargeter,
        "",
        "",
        "JacobRTG_",
        "",
        False,
        True,
    )

    results = []
    for data in new_assets:
        obj = data.get_asset()
        if obj:
            obj = move_retargeted_asset(obj)
        path = obj.get_path_name().rsplit(".", 1)[0] if obj else str(data.package_name)
        results.append(
            {
                "package": path,
                "object": obj.get_path_name() if obj else None,
                "class": obj.get_class().get_name() if obj else None,
                "skeleton": obj.get_skeleton().get_path_name()
                if obj and hasattr(obj, "get_skeleton") and obj.get_skeleton()
                else None,
            }
        )
    unreal.EditorAssetLibrary.save_directory(RETARGETED_ANIM_DIR, only_if_is_dirty=False, recursive=True)
    return results


def main():
    source_mesh = load_asset(SOURCE_MESH_PATH)
    target_mesh = load_asset(TARGET_MESH_PATH)

    source_ikrig = create_ikrig(SOURCE_IKRIG_PATH)
    target_ikrig = create_ikrig(TARGET_IKRIG_PATH)
    retargeter = create_retargeter(RETARGETER_PATH)

    report = {
        "source_mesh": source_mesh.get_path_name(),
        "target_mesh": target_mesh.get_path_name(),
        "source_ikrig": configure_ikrig(source_ikrig, source_mesh, "pelvis", SOURCE_CHAINS),
        "target_ikrig": configure_ikrig(target_ikrig, target_mesh, "DEF-PELVIS01", TARGET_CHAINS),
    }
    report["retargeter"] = configure_retargeter(retargeter, source_ikrig, target_ikrig, source_mesh, target_mesh)
    report["retargeted_assets"] = retarget_animations(source_mesh, target_mesh, retargeter)
    report["result"] = "passed" if report["retargeted_assets"] else "failed"

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    unreal.log("EasyCheckpoint to Jacob retarget report written to {0}".format(REPORT_PATH))
    unreal.log("Retargeted {0} assets".format(len(report["retargeted_assets"])))


main()
