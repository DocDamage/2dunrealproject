from __future__ import annotations

import json
import os
import re
import shutil
import traceback
from pathlib import Path


PROJECT_UNREAL_ROOT = "/Game/NocturneSignal"
JACOB_ROOT = PROJECT_UNREAL_ROOT + "/Characters/Jacob"
RETARGETING_ROOT = JACOB_ROOT + "/Retargeting"
OUTPUT_ROOT = JACOB_ROOT + "/RetargetedAnimations"
TARGET_MESH_PATH = JACOB_ROOT + "/SK_Jacob.SK_Jacob"
TARGET_IKRIG_PATH = RETARGETING_ROOT + "/IK_Jacob_Reconcile"

FIGHTING_SOURCE_RELATIVE = Path(
    "ExternalAssets/assetingest/PluginInstallExtracted/Fighting_Animations/Animations"
)
FIGHTING_STAGED_RELATIVE = Path("SourceArt/AnimationSources/FightingAnimations")
FIGHTING_IMPORT_DESTINATION = PROJECT_UNREAL_ROOT + "/AnimationSources/FightingAnimations/Animations"

REPORT_RELATIVE = Path("docs/asset-intake/JACOB_REALMARCHITECT_RECONCILIATION.json")

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
        "name": "FireTrailOfTheSword",
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
        "prefix": "JAC_Fire_",
        "output_dir": OUTPUT_ROOT + "/FireTrailOfTheSword",
        "ikrig": RETARGETING_ROOT + "/IK_FireTrailOfTheSword",
        "retargeter": RETARGETING_ROOT + "/RTG_FireTrailOfTheSword_To_Jacob",
    },
    {
        "name": "FightingAnimations",
        "source_mesh": (
            "/Game/RamsterZ_FreeAnims_Volume1/Demo/Mannequin/Character/Mesh/"
            "SK_Mannequin.SK_Mannequin"
        ),
        "source_skeleton": (
            "/Game/RamsterZ_FreeAnims_Volume1/Demo/Mannequin/Character/Mesh/"
            "UE4_Mannequin_Skeleton.UE4_Mannequin_Skeleton"
        ),
        "source_root": "pelvis",
        "source_chains": [
            ("Spine", "spine_01", "spine_03"),
            ("Head", "neck_01", "head"),
            ("LeftArm", "clavicle_l", "hand_l"),
            ("RightArm", "clavicle_r", "hand_r"),
            ("LeftLeg", "thigh_l", "ball_l"),
            ("RightLeg", "thigh_r", "ball_r"),
        ],
        "animation_dir": FIGHTING_IMPORT_DESTINATION,
        "import_destination": FIGHTING_IMPORT_DESTINATION,
        "prefix": "JAC_Fighting_",
        "output_dir": OUTPUT_ROOT + "/FightingAnimations",
        "ikrig": RETARGETING_ROOT + "/IK_FightingAnimations_UE4Mannequin",
        "retargeter": RETARGETING_ROOT + "/RTG_FightingAnimations_To_Jacob",
    },
]


def fbx_files(path: Path) -> list[Path]:
    if not path.is_dir():
        return []
    return sorted(item for item in path.iterdir() if item.suffix.lower() == ".fbx")


def firetrail_source_files(project_root: Path) -> list[Path]:
    source_root = project_root / "Content/FIRETRAILOFTHESWORD/Demo/Anims"
    return sorted(source_root.glob("A_NS_*.uasset"))


def fighting_source_files(realm_root: Path) -> list[Path]:
    return fbx_files(realm_root / FIGHTING_SOURCE_RELATIVE)


def unreal_asset_references(pack: dict[str, object]) -> list[str]:
    references = []
    for key in ("source_mesh", "source_skeleton", "animation_dir", "import_destination", "output_dir", "ikrig", "retargeter"):
        value = pack.get(key)
        if isinstance(value, str) and value.startswith("/Game/"):
            references.append(value)
    return references


def build_reconciliation_plan(project_root: Path | str, realm_root: Path | str) -> dict[str, object]:
    project_root = Path(project_root)
    realm_root = Path(realm_root)

    firetrail_count = len(firetrail_source_files(project_root))
    fighting_count = len(fighting_source_files(realm_root))

    packs = []
    for pack in PACKS:
        planned = dict(pack)
        if pack["name"] == "FireTrailOfTheSword":
            planned["source_animation_count"] = firetrail_count
        elif pack["name"] == "FightingAnimations":
            planned["source_animation_count"] = fighting_count
            planned["source_file_root"] = str((realm_root / FIGHTING_SOURCE_RELATIVE).resolve())
            planned["staged_source_root"] = str((project_root / FIGHTING_STAGED_RELATIVE).resolve())
        packs.append(planned)

    return {
        "project_root": str(project_root.resolve()),
        "realm_root": str(realm_root.resolve()),
        "packs": packs,
        "expected_retarget_count": firetrail_count + fighting_count,
    }


def sanitized_asset_name(path: Path | str) -> str:
    name = Path(path).stem
    name = re.sub(r"[^0-9A-Za-z_]+", "_", name).strip("_")
    return name or "ImportedAnimation"


def stage_fighting_sources(project_root: Path, realm_root: Path) -> list[str]:
    source_root = realm_root / FIGHTING_SOURCE_RELATIVE
    destination_root = project_root / FIGHTING_STAGED_RELATIVE
    sources = fighting_source_files(realm_root)
    if len(sources) != 11:
        raise RuntimeError(f"Expected 11 FightingAnimations FBXs, found {len(sources)} in {source_root}")

    destination_root.mkdir(parents=True, exist_ok=True)
    copied = []
    for source in sources:
        destination = destination_root / source.name
        shutil.copy2(source, destination)
        copied.append(str(destination))

    readme = source_root / "READ ME.txt"
    if readme.exists():
        shutil.copy2(readme, destination_root / readme.name)

    return copied


def _unreal():
    import unreal

    return unreal


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[-1].rsplit(".", 1)[0]


def object_path(package_path: str) -> str:
    return f"{package_path}.{asset_name(package_path)}"


def load_asset(unreal, path: str):
    asset = unreal.load_asset(path) or unreal.load_asset(object_path(path))
    if not asset:
        raise RuntimeError(f"Could not load asset: {path}")
    return asset


def load_existing_asset(unreal, path: str):
    return unreal.load_asset(path) or unreal.load_asset(object_path(path))


def ensure_directory(unreal, path: str) -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def create_ikrig(unreal, path: str):
    existing = load_existing_asset(unreal, path)
    if existing:
        return existing

    ensure_directory(unreal, path.rsplit("/", 1)[0])
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        path.rsplit("/", 1)[0],
        unreal.IKRigDefinition,
        unreal.IKRigDefinitionFactory(),
    )
    if not asset:
        raise RuntimeError(f"Could not create IK Rig: {path}")
    return asset


def create_retargeter(unreal, path: str):
    existing = load_existing_asset(unreal, path)
    if existing:
        return existing

    ensure_directory(unreal, path.rsplit("/", 1)[0])
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        path.rsplit("/", 1)[0],
        unreal.IKRetargeter,
        unreal.IKRetargetFactory(),
    )
    if not asset:
        raise RuntimeError(f"Could not create IK Retargeter: {path}")
    return asset


def bone_names(mesh) -> list[str]:
    skeleton = mesh.get_editor_property("skeleton")
    if not skeleton:
        return []
    reference_pose = skeleton.get_reference_pose()
    if hasattr(reference_pose, "get_bone_names"):
        return [str(name) for name in reference_pose.get_bone_names()]
    return []


def validate_chain_bones(mesh, root_bone: str, chains: list[tuple[str, str, str]]) -> dict[str, object]:
    bones = set(bone_names(mesh))
    required = [root_bone]
    for _chain_name, start_bone, end_bone in chains:
        required.extend([start_bone, end_bone])

    missing = [bone for bone in required if bone not in bones]
    if missing:
        raise RuntimeError(f"Mesh {mesh.get_path_name()} is missing retarget bones: {', '.join(missing)}")

    return {"bone_count": len(bones), "required_bones": required}


def configure_ikrig(unreal, ikrig, mesh, root_bone: str, chains: list[tuple[str, str, str]]) -> dict[str, object]:
    validation = validate_chain_bones(mesh, root_bone, chains)
    controller = unreal.IKRigController.get_controller(ikrig)
    if not controller.set_skeletal_mesh(mesh):
        raise RuntimeError(f"Could not set IK Rig skeletal mesh: {mesh.get_path_name()}")

    try:
        controller.apply_auto_generated_retarget_definition()
    except Exception:
        pass

    for chain_name, _start, _end in chains:
        try:
            controller.remove_retarget_chain(chain_name)
        except Exception:
            pass

    if not controller.set_retarget_root(root_bone):
        raise RuntimeError(f"Could not set retarget root '{root_bone}' on {ikrig.get_path_name()}")

    added = []
    for chain_name, start_bone, end_bone in chains:
        result = controller.add_retarget_chain(chain_name, start_bone, end_bone, "")
        added.append({"chain": chain_name, "start": start_bone, "end": end_bone, "result": str(result)})

    unreal.EditorAssetLibrary.save_loaded_asset(ikrig)
    return {
        "path": ikrig.get_path_name(),
        "mesh": mesh.get_path_name(),
        "root": str(controller.get_retarget_root()),
        "chain_count": len(controller.get_retarget_chains()),
        "chains_added": added,
        "validation": validation,
    }


def configure_retargeter(unreal, retargeter, source_ikrig, target_ikrig, source_mesh, target_mesh) -> dict[str, object]:
    controller = unreal.IKRetargeterController.get_controller(retargeter)
    controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_ikrig)
    controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_ikrig)
    controller.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE, source_mesh)
    controller.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET, target_mesh)
    controller.add_default_ops()
    try:
        controller.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, source_ikrig)
        controller.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, target_ikrig)
    except Exception:
        pass
    controller.auto_map_chains(unreal.AutoMapChainType.EXACT, True)

    unreal.EditorAssetLibrary.save_loaded_asset(retargeter)
    mappings = {}
    for chain_name, _start, _end in TARGET_CHAINS:
        mappings[chain_name] = str(controller.get_source_chain(chain_name))

    return {"path": retargeter.get_path_name(), "num_ops": controller.get_num_retarget_ops(), "mappings": mappings}


def make_animation_import_task(unreal, source: Path, destination: str, skeleton):
    options = unreal.FbxImportUI()
    options.set_editor_property("automated_import_should_detect_type", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    options.set_editor_property("import_mesh", False)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("skeleton", skeleton)
    options.anim_sequence_import_data.set_editor_property(
        "animation_length",
        unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME,
    )

    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(source))
    task.set_editor_property("destination_path", destination)
    task.set_editor_property("destination_name", sanitized_asset_name(source))
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("replace_existing_settings", False)
    task.set_editor_property("options", options)
    return task


def import_fighting_sources(unreal, project_root: Path, pack: dict[str, object]) -> dict[str, object]:
    sources = fbx_files(project_root / FIGHTING_STAGED_RELATIVE)
    if len(sources) != 11:
        raise RuntimeError(f"Expected 11 staged FightingAnimations FBXs, found {len(sources)}")

    skeleton = load_asset(unreal, str(pack["source_skeleton"]))
    ensure_directory(unreal, str(pack["import_destination"]))
    unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")

    tasks = [
        make_animation_import_task(unreal, source, str(pack["import_destination"]), skeleton)
        for source in sources
    ]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    imported = []
    failed = []
    for task in tasks:
        paths = list(task.get_editor_property("imported_object_paths") or [])
        source = str(task.get_editor_property("filename"))
        if paths:
            imported.append({"source": source, "imported": paths})
        else:
            failed.append(source)

    unreal.EditorAssetLibrary.save_directory(str(pack["import_destination"]), only_if_is_dirty=False, recursive=True)
    if failed:
        raise RuntimeError(f"FightingAnimations import failed for {len(failed)} files: {failed}")

    return {"imported_sources": len(imported), "failed_sources": failed, "imported": imported}


def list_anim_sequences(unreal, directory: str) -> list[str]:
    paths = unreal.EditorAssetLibrary.list_assets(directory, recursive=True, include_folder=False)
    anim_paths = []
    for path in paths:
        asset = unreal.load_asset(path)
        if asset and asset.get_class().get_name() == "AnimSequence":
            anim_paths.append(asset.get_path_name().rsplit(".", 1)[0])
    return sorted(anim_paths)


def delete_asset_if_exists(unreal, path: str) -> None:
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        if not unreal.EditorAssetLibrary.delete_asset(path):
            raise RuntimeError(f"Could not delete generated asset: {path}")


def prepare_retarget_outputs(unreal, pack: dict[str, object], animation_paths: list[str]) -> None:
    ensure_directory(unreal, str(pack["output_dir"]))
    for source_path in animation_paths:
        destination_name = str(pack["prefix"]) + asset_name(source_path)
        delete_asset_if_exists(unreal, f"/Game/{destination_name}")
        delete_asset_if_exists(unreal, f"{pack['output_dir']}/{destination_name}")


def find_asset_data(unreal, package_path: str):
    asset_data = unreal.EditorAssetLibrary.find_asset_data(package_path)
    if not asset_data or not asset_data.is_valid():
        raise RuntimeError(f"Could not find animation asset data: {package_path}")
    return asset_data


def result_to_asset(data):
    if hasattr(data, "get_asset"):
        asset = data.get_asset()
        if asset:
            return asset
    return data


def move_retargeted_asset(unreal, asset, output_dir: str):
    old_package = asset.get_path_name().rsplit(".", 1)[0]
    desired_package = f"{output_dir}/{asset.get_name()}"

    if old_package == desired_package:
        unreal.EditorAssetLibrary.save_loaded_asset(asset)
        return asset

    delete_asset_if_exists(unreal, desired_package)
    if not unreal.EditorAssetLibrary.rename_asset(old_package, desired_package):
        raise RuntimeError(f"Could not move retargeted asset from {old_package} to {desired_package}")

    moved = load_asset(unreal, object_path(desired_package))
    unreal.EditorAssetLibrary.save_loaded_asset(moved)
    return moved


def retarget_animations(unreal, pack: dict[str, object], source_mesh, target_mesh, retargeter) -> list[dict[str, object]]:
    animation_paths = list_anim_sequences(unreal, str(pack["animation_dir"]))
    if not animation_paths:
        raise RuntimeError(f"No AnimSequence assets found in {pack['animation_dir']}")

    prepare_retarget_outputs(unreal, pack, animation_paths)
    asset_data = [find_asset_data(unreal, path) for path in animation_paths]
    new_assets = unreal.IKRetargetBatchOperation.duplicate_and_retarget(
        asset_data,
        source_mesh,
        target_mesh,
        retargeter,
        "",
        "",
        str(pack["prefix"]),
        "",
        False,
        True,
    )

    results = []
    for data in new_assets:
        asset = result_to_asset(data)
        if asset:
            asset = move_retargeted_asset(unreal, asset, str(pack["output_dir"]))
        path = asset.get_path_name().rsplit(".", 1)[0] if asset else str(data.package_name)
        results.append(
            {
                "package": path,
                "object": asset.get_path_name() if asset else None,
                "class": asset.get_class().get_name() if asset else None,
                "skeleton": asset.get_skeleton().get_path_name()
                if asset and hasattr(asset, "get_skeleton") and asset.get_skeleton()
                else None,
                "play_length": asset.get_editor_property("sequence_length") if asset else None,
            }
        )

    unreal.EditorAssetLibrary.save_directory(str(pack["output_dir"]), only_if_is_dirty=False, recursive=True)
    return results


def process_pack(unreal, pack: dict[str, object], target_mesh, target_ikrig) -> dict[str, object]:
    source_mesh = load_asset(unreal, str(pack["source_mesh"]))
    source_ikrig = create_ikrig(unreal, str(pack["ikrig"]))
    retargeter = create_retargeter(unreal, str(pack["retargeter"]))
    animation_paths = list_anim_sequences(unreal, str(pack["animation_dir"]))

    report = {
        "source_mesh": source_mesh.get_path_name(),
        "target_mesh": target_mesh.get_path_name(),
        "animation_dir": pack["animation_dir"],
        "animation_count": len(animation_paths),
        "source_ikrig": configure_ikrig(
            unreal,
            source_ikrig,
            source_mesh,
            str(pack["source_root"]),
            pack["source_chains"],
        ),
        "target_ikrig": configure_ikrig(unreal, target_ikrig, target_mesh, "DEF-PELVIS01", TARGET_CHAINS),
    }
    report["retargeter"] = configure_retargeter(
        unreal,
        retargeter,
        source_ikrig,
        target_ikrig,
        source_mesh,
        target_mesh,
    )
    report["retargeted_assets"] = retarget_animations(unreal, pack, source_mesh, target_mesh, retargeter)
    report["result"] = "passed" if len(report["retargeted_assets"]) == len(animation_paths) else "partial"
    return report


def write_report(project_root: Path, report: dict[str, object]) -> Path:
    report_path = project_root / REPORT_RELATIVE
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def run_reconciliation(project_root: Path, realm_root: Path) -> dict[str, object]:
    unreal = _unreal()

    plan = build_reconciliation_plan(project_root, realm_root)
    staged_fighting_sources = stage_fighting_sources(project_root, realm_root)

    report = {
        "plan": plan,
        "staged_fighting_sources": staged_fighting_sources,
        "packs": {},
        "result": "passed",
    }

    target_mesh = load_asset(unreal, TARGET_MESH_PATH)
    target_ikrig = create_ikrig(unreal, TARGET_IKRIG_PATH)

    for pack in PACKS:
        try:
            if pack["name"] == "FightingAnimations":
                report["fighting_import"] = import_fighting_sources(unreal, project_root, pack)
            pack_report = process_pack(unreal, pack, target_mesh, target_ikrig)
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

    report_path = write_report(project_root, report)
    unreal.EditorAssetLibrary.save_directory(RETARGETING_ROOT, only_if_is_dirty=False, recursive=True)
    unreal.log(f"Jacob RealmArchitect reconciliation report written to {report_path}")
    unreal.log(f"Retargeted {total} missing Jacob animation assets")
    return report


def main() -> None:
    project_root = Path(os.environ.get("NOCTURNE_PROJECT_ROOT", Path.cwd())).resolve()
    realm_root = Path(os.environ.get("REALMARCHITECT_ROOT", "G:/RealmArchitect")).resolve()
    report = run_reconciliation(project_root, realm_root)

    try:
        command_line = _unreal().SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterJacobReconciliation" in command_line or os.environ.get("NOCTURNE_QUIT_AFTER_RECONCILE") == "1":
        _unreal().SystemLibrary.quit_editor()

    if report["result"] != "passed":
        raise RuntimeError("Jacob RealmArchitect reconciliation completed partially; inspect report for failures.")


if __name__ == "__main__":
    main()
