import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REALM_ROOT = Path("G:/RealmArchitect")
TOOL_PATH = PROJECT_ROOT / "Tools" / "Unreal" / "reconcile_realmarchitect_jacob_assets.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("reconcile_realmarchitect_jacob_assets", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reconciliation_plan_targets_only_missing_nocturne_deltas():
    tool = load_tool()

    plan = tool.build_reconciliation_plan(PROJECT_ROOT, REALM_ROOT)

    assert plan["expected_retarget_count"] == 37
    assert {pack["name"] for pack in plan["packs"]} == {"FireTrailOfTheSword", "FightingAnimations"}

    firetrail = next(pack for pack in plan["packs"] if pack["name"] == "FireTrailOfTheSword")
    fighting = next(pack for pack in plan["packs"] if pack["name"] == "FightingAnimations")

    assert firetrail["source_animation_count"] == 26
    assert firetrail["output_dir"] == "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FireTrailOfTheSword"
    assert firetrail["source_mesh"] == "/Game/FIRETRAILOFTHESWORD/Demo/SKM_Man/SKM_Man.SKM_Man"

    assert fighting["source_animation_count"] == 11
    assert fighting["import_destination"] == "/Game/NocturneSignal/AnimationSources/FightingAnimations/Animations"
    assert fighting["output_dir"] == "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FightingAnimations"

    unreal_references = []
    for pack in plan["packs"]:
        unreal_references.extend(tool.unreal_asset_references(pack))

    assert unreal_references
    assert all("/Game/RealmArchitect" not in reference for reference in unreal_references)
