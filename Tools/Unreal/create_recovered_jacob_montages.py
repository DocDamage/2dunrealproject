from __future__ import annotations

import json
import os
import traceback
from pathlib import Path


JACOB_ROOT = "/Game/NocturneSignal/Characters/Jacob"
RETARGETED_ROOT = JACOB_ROOT + "/RetargetedAnimations"
MONTAGE_ROOT = JACOB_ROOT + "/Montages"
JACOB_MESH_PATH = JACOB_ROOT + "/SK_Jacob.SK_Jacob"
JACOB_SKELETON_PATH = JACOB_ROOT + "/SK_Jacob_Skeleton.SK_Jacob_Skeleton"
REPORT_RELATIVE = Path("docs/asset-intake/JACOB_RECOVERED_MONTAGE_REPORT.json")


MONTAGE_PLAN = [
    {
        "name": "AM_Jacob_FireTrail_Action01",
        "category": "FireTrailOfTheSword",
        "source_name": "JAC_Fire_A_NS_01",
        "sections": ["Default", "AttackStart", "Recover"],
        "section_fractions": [0.0, 0.18, 0.72],
    },
    {
        "name": "AM_Jacob_FireTrail_Action08",
        "category": "FireTrailOfTheSword",
        "source_name": "JAC_Fire_A_NS_08",
        "sections": ["Default", "AttackStart", "Recover"],
        "section_fractions": [0.0, 0.18, 0.72],
    },
    {
        "name": "AM_Jacob_FireTrail_Action16",
        "category": "FireTrailOfTheSword",
        "source_name": "JAC_Fire_A_NS_16",
        "sections": ["Default", "AttackStart", "Recover"],
        "section_fractions": [0.0, 0.18, 0.72],
    },
    {
        "name": "AM_Jacob_Fighting_CrossPunch",
        "category": "FightingAnimations",
        "source_name": "JAC_Fighting_Cross_Punch_Anim",
        "sections": ["Default", "StrikeStart", "Recover"],
        "section_fractions": [0.0, 0.16, 0.68],
    },
    {
        "name": "AM_Jacob_Fighting_HookPunch",
        "category": "FightingAnimations",
        "source_name": "JAC_Fighting_Hook_Punch",
        "sections": ["Default", "StrikeStart", "Recover"],
        "section_fractions": [0.0, 0.16, 0.68],
    },
    {
        "name": "AM_Jacob_Fighting_ElbowPunch",
        "category": "FightingAnimations",
        "source_name": "JAC_Fighting_Elbow_Punching",
        "sections": ["Default", "StrikeStart", "Recover"],
        "section_fractions": [0.0, 0.16, 0.68],
    },
    {
        "name": "AM_Jacob_Fighting_Impact",
        "category": "FightingAnimations",
        "source_name": "JAC_Fighting_Impact_mixamo_com",
        "sections": ["Default", "ReactStart", "Recover"],
        "section_fractions": [0.0, 0.12, 0.66],
    },
    {
        "name": "AM_Jacob_Fighting_Death",
        "category": "FightingAnimations",
        "source_name": "JAC_Fighting_Dying_mixamo_com",
        "sections": ["Default", "DeathStart", "Settle"],
        "section_fractions": [0.0, 0.18, 0.82],
    },
]


def build_montage_plan() -> list[dict[str, object]]:
    plan = []
    for item in MONTAGE_PLAN:
        planned = dict(item)
        planned["asset"] = (
            f"{RETARGETED_ROOT}/{planned['category']}/{planned['source_name']}."
            f"{planned['source_name']}"
        )
        planned["destination"] = f"{MONTAGE_ROOT}/{planned['name']}"
        planned["object_path"] = f"{planned['destination']}.{planned['name']}"
        plan.append(planned)
    return plan


def _unreal():
    import unreal

    return unreal


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[-1].rsplit(".", 1)[0]


def package_path(path: str) -> str:
    return path.rsplit(".", 1)[0] if "." in path.rsplit("/", 1)[-1] else path


def object_path(path: str) -> str:
    package = package_path(path)
    return f"{package}.{asset_name(package)}"


def load_asset(unreal, path: str):
    asset = unreal.load_asset(path) or unreal.load_asset(object_path(path))
    if not asset:
        raise RuntimeError(f"Could not load asset: {path}")
    return asset


def load_optional_asset(unreal, path: str):
    return unreal.load_asset(path) or unreal.load_asset(object_path(path))


def ensure_directory(unreal, path: str) -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def delete_asset_if_exists(unreal, path: str) -> None:
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        if not unreal.EditorAssetLibrary.delete_asset(path):
            raise RuntimeError(f"Could not delete existing generated montage: {path}")


def set_first_available_property(target, property_names: list[str], value) -> bool:
    for property_name in property_names:
        try:
            target.set_editor_property(property_name, value)
            return True
        except Exception:
            continue
    return False


def get_play_length(animation) -> float:
    for method_name in ("get_play_length", "get_play_length_for_trimmed_animation"):
        method = getattr(animation, method_name, None)
        if callable(method):
            try:
                return float(method())
            except Exception:
                pass
    for property_name in ("sequence_length", "play_length"):
        try:
            return float(animation.get_editor_property(property_name))
        except Exception:
            pass
    return 0.0


def section_times(item: dict[str, object], play_length: float) -> list[float]:
    fractions = [float(value) for value in item.get("section_fractions", [])]
    sections = list(item["sections"])
    if len(fractions) != len(sections):
        fractions = [index / max(len(sections), 1) for index in range(len(sections))]
    safe_length = max(play_length, 0.1)
    return [round(max(0.0, min(safe_length - 0.001, safe_length * fraction)), 4) for fraction in fractions]


def call_if_present(target, method_names: tuple[str, ...], *args):
    for method_name in method_names:
        method = getattr(target, method_name, None)
        if callable(method):
            return method(*args)
    return None


def montage_editor_bridge(unreal):
    bridge = getattr(unreal, "NocturneMontageEditorLibrary", None)
    if not bridge:
        raise RuntimeError("NocturneMontageEditorLibrary is not loaded; build the NocturneSignalEditor module.")
    return bridge


def section_names(unreal, montage) -> list[str]:
    try:
        return [str(name) for name in montage_editor_bridge(unreal).get_montage_section_names(montage)]
    except Exception:
        pass

    count = call_if_present(montage, ("get_num_sections", "get_num_composite_sections"))
    if count is not None:
        names = []
        for index in range(int(count)):
            name = call_if_present(montage, ("get_section_name",), index)
            names.append(str(name))
        return names

    sections = montage.get_editor_property("composite_sections") or []
    names = []
    for section in sections:
        names.append(str(section.get_editor_property("section_name")))
    return names


def section_report(unreal, montage) -> list[dict[str, object]]:
    try:
        bridge = montage_editor_bridge(unreal)
        names = [str(name) for name in bridge.get_montage_section_names(montage)]
        times = [float(time) for time in bridge.get_montage_section_times(montage)]
        if names and len(names) == len(times):
            return [
                {"index": index, "name": name, "next": "", "time": round(times[index], 4)}
                for index, name in enumerate(names)
            ]
    except Exception:
        pass

    try:
        sections = montage.get_editor_property("composite_sections") or []
    except Exception:
        sections = []
    report = []
    for index, section in enumerate(sections):
        time_value = call_if_present(section, ("get_time",))
        if time_value is None:
            try:
                time_value = section.get_editor_property("link_value")
            except Exception:
                time_value = None
        report.append(
            {
                "index": index,
                "name": str(section.get_editor_property("section_name")),
                "next": str(section.get_editor_property("next_section_name")),
                "time": float(time_value) if time_value is not None else None,
            }
        )
    if report:
        return report

    return [{"index": index, "name": name, "next": "", "time": None} for index, name in enumerate(section_names(unreal, montage))]


def configure_sections(unreal, montage, item: dict[str, object], animation, play_length: float) -> list[dict[str, object]]:
    requested = list(item["sections"])
    times = section_times(item, play_length)
    bridge = montage_editor_bridge(unreal)
    if not bridge.set_montage_sections(montage, [unreal.Name(name) for name in requested], times):
        raise RuntimeError(f"NocturneMontageEditorLibrary could not set sections on {montage.get_name()}")

    actual = section_names(unreal, montage)
    if actual != requested:
        raise RuntimeError(f"Expected montage sections {requested}, got {actual}")
    return section_report(unreal, montage)


def create_montage(unreal, item: dict[str, object], skeleton, preview_mesh) -> dict[str, object]:
    animation = load_asset(unreal, str(item["asset"]))
    play_length = get_play_length(animation)
    destination = str(item["destination"])
    destination_root = destination.rsplit("/", 1)[0]
    name = str(item["name"])

    ensure_directory(unreal, destination_root)
    delete_asset_if_exists(unreal, destination)

    factory = unreal.AnimMontageFactory()
    factory.set_editor_property("target_skeleton", skeleton)
    factory.set_editor_property("source_animation", animation)
    try:
        factory.set_editor_property("preview_skeletal_mesh", preview_mesh)
    except Exception:
        pass

    montage = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name,
        destination_root,
        unreal.AnimMontage,
        factory,
    )
    if not montage:
        raise RuntimeError(f"Could not create montage: {destination}")

    set_first_available_property(montage, ["blend_out_trigger_time"], -1.0)
    sections = configure_sections(unreal, montage, item, animation, play_length)
    unreal.EditorAssetLibrary.save_loaded_asset(montage)

    created = load_asset(unreal, object_path(destination))
    created_skeleton = created.get_skeleton() if hasattr(created, "get_skeleton") else None
    skeleton_path = created_skeleton.get_path_name() if created_skeleton else ""
    if skeleton_path != JACOB_SKELETON_PATH:
        raise RuntimeError(f"Montage {name} resolved to unexpected skeleton: {skeleton_path}")

    return {
        "name": name,
        "category": item["category"],
        "source_animation": animation.get_path_name(),
        "destination": destination,
        "object_path": created.get_path_name(),
        "skeleton": skeleton_path,
        "play_length": play_length,
        "sections_expected": item["sections"],
        "section_times_expected": section_times(item, play_length),
        "sections": sections,
        "result": "passed",
    }


def write_report(project_root: Path, report: dict[str, object]) -> Path:
    report_path = project_root / REPORT_RELATIVE
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def create_recovered_montages(project_root: Path) -> dict[str, object]:
    unreal = _unreal()
    skeleton = load_asset(unreal, JACOB_SKELETON_PATH)
    preview_mesh = load_asset(unreal, JACOB_MESH_PATH)

    report = {
        "plan": build_montage_plan(),
        "montages": [],
        "total_montages": 0,
        "result": "passed",
    }

    for item in build_montage_plan():
        try:
            montage_report = create_montage(unreal, item, skeleton, preview_mesh)
        except Exception as exc:
            montage_report = {
                "name": item["name"],
                "destination": item["destination"],
                "source_animation": item["asset"],
                "result": "failed",
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
            report["result"] = "partial"
        report["montages"].append(montage_report)

    report["total_montages"] = len([item for item in report["montages"] if item.get("result") == "passed"])
    report_path = write_report(project_root, report)
    unreal.log(f"Recovered Jacob montage report written to {report_path}")
    unreal.log(f"Created {report['total_montages']} recovered Jacob montages")
    return report


def main() -> None:
    project_root = Path(os.environ.get("NOCTURNE_PROJECT_ROOT", Path.cwd())).resolve()
    report = create_recovered_montages(project_root)

    if report["result"] != "passed":
        raise RuntimeError("Recovered Jacob montage creation completed partially; inspect report for failures.")

    try:
        command_line = _unreal().SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterRecoveredJacobMontages" in command_line or os.environ.get("NOCTURNE_QUIT_AFTER_RECOVERED_MONTAGES") == "1":
        _unreal().SystemLibrary.quit_editor()


if __name__ == "__main__":
    main()
