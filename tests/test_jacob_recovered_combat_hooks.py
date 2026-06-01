from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HEADER = PROJECT_ROOT / "Source" / "NocturneSignal" / "Public" / "NocturnePlayerCharacter.h"
SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "NocturnePlayerCharacter.cpp"


def test_player_character_exposes_recovered_combat_montage_selector():
    header = HEADER.read_text(encoding="utf-8")
    source = SOURCE.read_text(encoding="utf-8")

    assert "enum class ENocturneJacobRecoveredCombatMontage" in header
    for value in (
        "FireTrailAction01",
        "FireTrailAction08",
        "FireTrailAction16",
        "FightingCrossPunch",
        "FightingHookPunch",
        "FightingElbowPunch",
        "FightingImpact",
        "FightingDeath",
    ):
        assert value in header

    assert "RecoveredCombat" in header
    assert "TriggerRecoveredCombatMontage" in header
    assert "GetRecoveredCombatMontage" in header

    for montage_assignment in (
        "FireTrailAction01Montage = nullptr;",
        "FireTrailAction08Montage = nullptr;",
        "FireTrailAction16Montage = nullptr;",
        "FightingCrossPunchMontage = nullptr;",
        "FightingHookPunchMontage = nullptr;",
        "FightingElbowPunchMontage = nullptr;",
        "FightingImpactMontage = nullptr;",
        "FightingDeathMontage = nullptr;",
    ):
        assert montage_assignment in source

    assert "AM_Jacob_" not in source

    assert "TEXT(\"AttackStart\")" in source
    assert "TEXT(\"StrikeStart\")" in source
    assert "TEXT(\"ReactStart\")" in source
    assert "TEXT(\"DeathStart\")" in source
