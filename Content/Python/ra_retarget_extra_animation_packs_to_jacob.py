import json
import os
import traceback

import unreal


PROJECT_ROOT = unreal.SystemLibrary.get_project_directory()
REPORT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "Docs", "ra_jacob_extra_retarget_report.json"))

RETARGET_DIR = "/Game/RealmArchitect/Art/Jacob/Retargeting"
TARGET_MESH_PATH = "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly.Jacob_NocturneCharacterOnly"
TARGET_IKRIG_PATH = RETARGET_DIR + "/IKR_Jacob_Nocturne"

TARGET_CHAINS = [
    ("Spine", "DEF-CHEST", "DEF-HEAD"),
    ("Head", "DEF-NECK", "DEF-HEAD"),
    ("LeftArm", "DEF-SHOULDER_L", "DEF-HAND_L"),
    ("RightArm", "DEF-SHOULDER_R", "DEF-HAND_R"),
    ("LeftLeg", "DEF-ULEG_L", "DEF-FOOTFINGERS_L"),
    ("RightLeg", "DEF-ULEG_R", "DEF-FOOTFINGERS_R"),
]

PACKS = [
    {
        "name": "UE4_FightingAnimations",
        "source_mesh": "/Game/Mannequin/Character/Mesh/SK_Mannequin.SK_Mannequin",
        "source_root": "pelvis",
        "source_chains": [
            ("Spine", "spine_01", "spine_03"),
            ("Head", "neck_01", "head"),
            ("LeftArm", "clavicle_l", "hand_l"),
            ("RightArm", "clavicle_r", "hand_r"),
            ("LeftLeg", "thigh_l", "ball_l"),
            ("RightLeg", "thigh_r", "ball_r"),
        ],
        "animation_dir": "/Game/RealmArchitect/Art/InstalledPacks/FightingAnimations/Skeletal",
        "prefix": "JacobUE4_",
        "output_dir": "/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Combat",
        "ikrig": RETARGET_DIR + "/IKR_UE4_Mannequin",
        "retargeter": RETARGET_DIR + "/RTG_UE4_to_Jacob",
    },
    {
        "name": "FireTrailSwordActions",
        "source_mesh": "/Game/FIRETRAILOFTHESWORD/Demo/SKM_Man/SKM_Man.SKM_Man",
        "source_root": "Hips",
        "source_chains": [
            ("Spine", "Spine", "Spine2"),
            ("Head", "Neck", "Head"),
            ("LeftArm", "LeftShoulder", "LeftHand"),
            ("RightArm", "RightShoulder", "RightHand"),
            ("LeftLeg", "LeftUpLeg", "LeftToeBase"),
            ("RightLeg", "RightUpLeg", "RightToeBase"),
        ],
        "animation_dir": "/Game/FIRETRAILOFTHESWORD/Demo/Anims",
        "prefix": "JacobFire_",
        "output_dir": "/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Sword",
        "ikrig": RETARGET_DIR + "/IKR_FireTrail_Man",
        "retargeter": RETARGET_DIR + "/RTG_FireTrail_to_Jacob",
    },
    {
        "name": "VexaActionMagic",
        "source_mesh": "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/SK/SK_Vefects_Vexa.SK_Vefects_Vexa",
        "source_root": "Base-HumanPelvis",
        "source_chains": [
            ("Spine", "Base-HumanSpine1", "Base-HumanRibcage"),
            ("Head", "Base-HumanNeck", "Base-HumanHead"),
            ("LeftArm", "Base-HumanLCollarbone", "Base-HumanLPalm"),
            ("RightArm", "Base-HumanRCollarbone", "Base-HumanRPalm"),
            ("LeftLeg", "Base-HumanLThigh", "Base-HumanLToes"),
            ("RightLeg", "Base-HumanRThigh", "Base-HumanRToes"),
        ],
        "animation_dir": "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/Animations",
        "prefix": "JacobVexa_",
        "output_dir": "/Game/RealmArchitect/Art/Jacob/RetargetedAnimations/Magic",
        "ikrig": RETARGET_DIR + "/IKR_Vexa",
        "retargeter": RETARGET_DIR + "/RTG_Vexa_to_Jacob",
    },
]


def asset_name(path):
    return path.rsplit("/", 1)[-1].rsplit(".", 1)[0]


def object_path(package_path):
    return "{0}.{1}".format(package_path, asset_name(package_path))


def load_asset(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: {0}".format(path))
    return asset


def load_existing_asset(path):
    asset = unreal.load_asset(path)
    if asset:
        return asset

    return unreal.load_asset(object_path(path))


def ensure_directory(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def create_ikrig(path):
    existing = load_existing_asset(path)
    if existing:
        return existing

    ensure_directory(path.rsplit("/", 1)[0])
    factory = unreal.IKRigDefinitionFactory()
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        path.rsplit("/", 1)[0],
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

    ensure_directory(path.rsplit("/", 1)[0])
    factory = unreal.IKRetargetFactory()
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        path.rsplit("/", 1)[0],
        unreal.IKRetargeter,
        factory,
    )
    if not asset:
        raise RuntimeError("Could not create IK Retargeter: {0}".format(path))
    return asset


def bone_names(mesh):
    skeleton = mesh.get_editor_property("skeleton")
    if not skeleton:
        return []
    reference_pose = skeleton.get_reference_pose()
    if hasattr(reference_pose, "get_bone_names"):
        return [str(name) for name in reference_pose.get_bone_names()]
    return []


def validate_chain_bones(mesh, root_bone, chains):
    bones = set(bone_names(mesh))
    required = [root_bone]
    for _chain_name, start_bone, end_bone in chains:
        required.append(start_bone)
        required.append(end_bone)

    missing = [bone for bone in required if bone not in bones]
    if missing:
        raise RuntimeError(
            "Mesh {0} is missing retarget bones: {1}".format(
                mesh.get_path_name(),
                ", ".join(missing),
            )
        )

    return {"bone_count": len(bones), "required_bones": required}


def configure_ikrig(ikrig, mesh, root_bone, chains):
    validation = validate_chain_bones(mesh, root_bone, chains)
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
        added.append({"chain": chain_name, "start": start_bone, "end": end_bone, "result": str(result)})

    unreal.EditorAssetLibrary.save_loaded_asset(ikrig)
    return {
        "path": ikrig.get_path_name(),
        "mesh": mesh.get_path_name(),
        "autogenerated_before_manual_override": autogenerated,
        "root": str(controller.get_retarget_root()),
        "chains_added": added,
        "chain_count": len(controller.get_retarget_chains()),
        "validation": validation,
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


def list_anim_sequences(directory):
    paths = unreal.EditorAssetLibrary.list_assets(directory, recursive=True, include_folder=False)
    anim_paths = []
    for path in paths:
        asset = unreal.load_asset(path)
        if asset and asset.get_class().get_name() == "AnimSequence":
            anim_paths.append(asset.get_path_name())
    return sorted(anim_paths)


def delete_asset_if_exists(path):
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        if not unreal.EditorAssetLibrary.delete_asset(path):
            raise RuntimeError("Could not delete generated asset: {0}".format(path))


def prepare_retarget_outputs(pack, animation_paths):
    ensure_directory(pack["output_dir"])
    for source_path in animation_paths:
        destination_name = pack["prefix"] + asset_name(source_path)
        delete_asset_if_exists("/Game/{0}".format(destination_name))
        delete_asset_if_exists("{0}/{1}".format(pack["output_dir"], destination_name))


def move_retargeted_asset(asset, output_dir):
    old_package = asset.get_path_name().rsplit(".", 1)[0]
    name = asset.get_name()
    desired_package = "{0}/{1}".format(output_dir, name)

    if old_package == desired_package:
        unreal.EditorAssetLibrary.save_loaded_asset(asset)
        return asset

    if unreal.EditorAssetLibrary.does_asset_exist(desired_package):
        delete_asset_if_exists(desired_package)

    if not unreal.EditorAssetLibrary.rename_asset(old_package, desired_package):
        raise RuntimeError("Could not move retargeted asset from {0} to {1}".format(old_package, desired_package))

    moved = load_asset(object_path(desired_package))
    unreal.EditorAssetLibrary.save_loaded_asset(moved)
    return moved


def retarget_animations(pack, source_mesh, target_mesh, retargeter, animation_paths):
    prepare_retarget_outputs(pack, animation_paths)
    asset_data = [animation_asset_data(path) for path in animation_paths]
    new_assets = unreal.IKRetargetBatchOperation.duplicate_and_retarget(
        asset_data,
        source_mesh,
        target_mesh,
        retargeter,
        "",
        "",
        pack["prefix"],
        "",
        False,
        True,
    )

    results = []
    for data in new_assets:
        obj = data.get_asset()
        if obj:
            obj = move_retargeted_asset(obj, pack["output_dir"])
        path = obj.get_path_name().rsplit(".", 1)[0] if obj else str(data.package_name)
        results.append(
            {
                "package": path,
                "object": obj.get_path_name() if obj else None,
                "class": obj.get_class().get_name() if obj else None,
                "skeleton": obj.get_skeleton().get_path_name()
                if obj and hasattr(obj, "get_skeleton") and obj.get_skeleton()
                else None,
                "play_length": obj.get_editor_property("sequence_length") if obj else None,
            }
        )

    unreal.EditorAssetLibrary.save_directory(pack["output_dir"], only_if_is_dirty=False, recursive=True)
    return results


def process_pack(pack, target_mesh, target_ikrig):
    source_mesh = load_asset(pack["source_mesh"])
    source_ikrig = create_ikrig(pack["ikrig"])
    retargeter = create_retargeter(pack["retargeter"])
    animation_paths = list_anim_sequences(pack["animation_dir"])
    if not animation_paths:
        raise RuntimeError("No AnimSequence assets found in {0}".format(pack["animation_dir"]))

    report = {
        "source_mesh": source_mesh.get_path_name(),
        "target_mesh": target_mesh.get_path_name(),
        "animation_dir": pack["animation_dir"],
        "animation_count": len(animation_paths),
        "animation_paths": animation_paths,
        "source_ikrig": configure_ikrig(source_ikrig, source_mesh, pack["source_root"], pack["source_chains"]),
        "target_ikrig": configure_ikrig(target_ikrig, target_mesh, "DEF-PELVIS01", TARGET_CHAINS),
    }
    report["retargeter"] = configure_retargeter(retargeter, source_ikrig, target_ikrig, source_mesh, target_mesh)
    report["retargeted_assets"] = retarget_animations(pack, source_mesh, target_mesh, retargeter, animation_paths)
    report["result"] = "passed" if len(report["retargeted_assets"]) == len(animation_paths) else "partial"
    return report


def main():
    target_mesh = load_asset(TARGET_MESH_PATH)
    target_ikrig = create_ikrig(TARGET_IKRIG_PATH)
    report = {"target_mesh": target_mesh.get_path_name(), "packs": {}, "result": "passed"}

    for pack in PACKS:
        try:
            pack_report = process_pack(pack, target_mesh, target_ikrig)
        except Exception as exc:
            pack_report = {
                "result": "failed",
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
            report["result"] = "partial"
        else:
            if pack_report["result"] != "passed":
                report["result"] = "partial"
        report["packs"][pack["name"]] = pack_report

    total = 0
    for pack_report in report["packs"].values():
        total += len(pack_report.get("retargeted_assets", []))
    report["total_retargeted_assets"] = total

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    unreal.EditorAssetLibrary.save_directory(RETARGET_DIR, only_if_is_dirty=False, recursive=True)
    unreal.log("Jacob extra animation retarget report written to {0}".format(REPORT_PATH))
    unreal.log("Retargeted {0} extra animation assets for Jacob".format(total))


main()
