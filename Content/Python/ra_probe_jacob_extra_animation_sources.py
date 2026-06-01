import json
import os

import unreal


PROJECT_ROOT = unreal.SystemLibrary.get_project_directory()
REPORT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "Docs", "ra_jacob_extra_animation_source_probe.json"))

SOURCES = {
    "UE4_FightingAnimations": {
        "mesh": "/Game/Mannequin/Character/Mesh/SK_Mannequin.SK_Mannequin",
        "sample_anim": "/Game/RealmArchitect/Art/InstalledPacks/FightingAnimations/Skeletal/Punching.Punching",
    },
    "FireTrail": {
        "mesh": "/Game/FIRETRAILOFTHESWORD/Demo/SKM_Man/SKM_Man.SKM_Man",
        "sample_anim": "/Game/FIRETRAILOFTHESWORD/Demo/Anims/A_NS_01.A_NS_01",
    },
    "Vexa": {
        "mesh": "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/SK/SK_Vefects_Vexa.SK_Vefects_Vexa",
        "sample_anim": "/Game/Vefects/Easy_Impact_Frames/Demo/Stylized_Female_Character_Vexa/Animations/SwordAttack_Vexa.SwordAttack_Vexa",
    },
    "Jacob": {
        "mesh": "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly.Jacob_NocturneCharacterOnly",
        "sample_anim": "/Game/RealmArchitect/Art/Jacob/Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_Idle.Jacob_NocturneCharacterOnly_Anim_Armature_Jacob_Idle",
    },
}


def load_asset(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: {0}".format(path))
    return asset


def reference_bones(mesh):
    skeleton = mesh.get_editor_property("skeleton")
    bones = []
    debug = {}
    for accessor in ("get_all_bone_names", "get_bone_names"):
        if bones or not hasattr(mesh, accessor):
            continue
        try:
            bones = [str(name) for name in getattr(mesh, accessor)()]
        except Exception:
            bones = []

    if not bones and skeleton and hasattr(skeleton, "get_reference_pose"):
        try:
            reference_pose = skeleton.get_reference_pose()
            debug["reference_pose_methods"] = [name for name in dir(reference_pose) if "bone" in name.lower()]
            if hasattr(reference_pose, "get_bone_names"):
                bones = [str(name) for name in reference_pose.get_bone_names()]
            elif hasattr(reference_pose, "get_bone_name") and hasattr(reference_pose, "get_num_bones"):
                bones = [str(reference_pose.get_bone_name(index)) for index in range(reference_pose.get_num_bones())]
        except Exception as exc:
            debug["reference_pose_error"] = str(exc)
            bones = []

    if not bones:
        debug["mesh_bone_methods"] = [name for name in dir(mesh) if "bone" in name.lower()]
        debug["skeleton_bone_methods"] = [name for name in dir(skeleton) if "bone" in name.lower()] if skeleton else []

    return skeleton, bones, debug


def contains_bone(bones, *needles):
    lower = [bone.lower() for bone in bones]
    return {needle: any(needle.lower() in bone for bone in lower) for needle in needles}


def main():
    report = {}
    for name, source in SOURCES.items():
        entry = {"mesh_path": source["mesh"], "sample_anim_path": source["sample_anim"]}
        try:
            mesh = load_asset(source["mesh"])
            anim = load_asset(source["sample_anim"])
            skeleton, bones, debug = reference_bones(mesh)
            entry.update(
                {
                    "mesh": mesh.get_path_name(),
                    "skeleton": skeleton.get_path_name() if skeleton else None,
                    "sample_anim": anim.get_path_name(),
                    "sample_anim_skeleton": anim.get_skeleton().get_path_name() if anim.get_skeleton() else None,
                    "bone_count": len(bones),
                    "bones": bones,
                    "debug": debug,
                    "bone_keyword_hits": contains_bone(
                        bones,
                        "root",
                        "pelvis",
                        "hips",
                        "spine",
                        "chest",
                        "neck",
                        "head",
                        "clavicle",
                        "shoulder",
                        "upperarm",
                        "lowerarm",
                        "hand",
                        "thigh",
                        "calf",
                        "foot",
                        "ball",
                        "toe",
                    ),
                }
            )
        except Exception as exc:
            entry["error"] = str(exc)
        report[name] = entry

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    unreal.log("Jacob extra animation source probe written to {0}".format(REPORT_PATH))


main()
