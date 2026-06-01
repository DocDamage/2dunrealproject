from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = PROJECT_ROOT / "Tools" / "Unreal" / "validate_jacob_animation_setup.py"


def test_active_player_validation_checks_female_cyber_stalker_mesh_and_fallbacks():
    source = VALIDATION_SCRIPT.read_text(encoding="utf-8")

    assert "ACTIVE_PLAYER_MESH_PATH" in source
    assert "SK_FemaleCyberStalker.SK_FemaleCyberStalker" in source
    assert "ACTIVE_PLAYER_SKELETON_PATH" in source
    assert "SK_FemaleCyberStalker_Skeleton" in source
    assert "ACTIVE_PLAYER_MESH_PATH" in source

    for fallback_property in (
        "IdleAnimation",
        "WalkAnimation",
        "RunAnimation",
        "JumpStartFallbackAnimation",
        "SlideLoopAnimation",
        "TentacleAttackFallbackAnimation",
        "TentacleConsumeFallbackAnimation",
    ):
        assert fallback_property in source

    assert "ACTIVE_PLAYER_SKELETON_PATH" in source
    assert "ABP_Jacob" not in source
