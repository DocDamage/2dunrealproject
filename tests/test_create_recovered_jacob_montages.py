import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = PROJECT_ROOT / "Tools" / "Unreal" / "create_recovered_jacob_montages.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("create_recovered_jacob_montages", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_recovered_montage_plan_is_curated_and_uses_nocturne_assets():
    tool = load_tool()

    plan = tool.build_montage_plan()

    assert len(plan) == 8
    assert {item["category"] for item in plan} == {"FireTrailOfTheSword", "FightingAnimations"}
    assert len([item for item in plan if item["category"] == "FireTrailOfTheSword"]) == 3
    assert len([item for item in plan if item["category"] == "FightingAnimations"]) == 5

    names = {item["name"] for item in plan}
    assert "AM_Jacob_FireTrail_Action01" in names
    assert "AM_Jacob_Fighting_CrossPunch" in names
    assert "AM_Jacob_Fighting_Impact" in names

    for item in plan:
        assert item["asset"].startswith("/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/")
        assert item["destination"].startswith("/Game/NocturneSignal/Characters/Jacob/Montages/")
        assert "/Game/RealmArchitect" not in item["asset"]
        assert "/Game/RealmArchitect" not in item["destination"]
        assert item["sections"][0] == "Default"


def test_recovered_montage_tool_uses_editor_bridge_for_section_mutation():
    tool_source = TOOL_PATH.read_text(encoding="utf-8")
    header_path = PROJECT_ROOT / "Source" / "NocturneSignalEditor" / "Public" / "NocturneMontageEditorLibrary.h"

    assert "NocturneMontageEditorLibrary" in tool_source
    assert "set_montage_sections" in tool_source
    assert "get_montage_section_times" in tool_source
    assert header_path.exists()

    header = header_path.read_text(encoding="utf-8")
    assert "class NOCTURNESIGNALEDITOR_API UNocturneMontageEditorLibrary" in header
    assert "SetMontageSections" in header
    assert "GetMontageSectionTimes" in header
