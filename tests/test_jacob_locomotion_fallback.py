import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYER_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "NocturnePlayerCharacter.cpp"
ANIMATION_VALIDATION = PROJECT_ROOT / "Tools" / "Unreal" / "validate_jacob_animation_setup.py"


def test_native_locomotion_fallback_reasserts_playback_when_component_is_not_playing():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "MeshComponent->IsPlaying()" in source
    assert "MeshComponent->PlayAnimation(Animation, bLoop);" in source
    assert "MeshComponent->SetPlayRate(1.0f);" in source
    assert "!MeshComponent || !Animation || CurrentFallbackAnimation == Animation" not in source


def test_missing_rogue_action_montages_have_nonblocking_animation_fallbacks():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "PlayJacobMontageOrFallback" in source
    assert "TentacleAttackFallbackAnimation" in source
    assert "TentacleGrappleFallbackAnimation" in source
    assert "TentacleConsumeFallbackAnimation" in source
    assert "TentacleAlternateConsumeFallbackAnimation" in source
    assert "FCS_Paired_ForceChoke_Att" in source
    assert "FCS_Paired_ForceChoke_Loop_Att" in source
    assert "FCS_Paired_SneakNeckBreak_Att" in source
    assert "FCS_Paired_Knife_Stealth_KidneyAndNeck_Att" in source
    assert re.search(r"PlayJacobMontageOrFallback\(\s*TentacleAttackMontage", source)
    assert re.search(r"PlayJacobMontageOrFallback\(\s*Montage", source)
    assert re.search(r"PlayJacobMontageOrFallback\(\s*TentacleGrappleLoopMontage", source)
    assert "bUseAlternateConsume ? TentacleAlternateConsumeFallbackAnimation.Get()" in source


def test_jacob_montages_use_single_node_playback_until_slots_are_repaired():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    body = re.search(
        r"float ANocturnePlayerCharacter::PlayJacobMontage\(.*?\n\}(?=\n\nfloat ANocturnePlayerCharacter::PlayJacobMontageOrFallback)",
        source,
        flags=re.S,
    )

    assert body
    assert "PlayAnimMontage(" not in body.group(0)
    assert "PlayJacobAnimationFallback(Montage, false);" in body.group(0)
    assert "bUsingSingleNodeAnimationFallback = true;" in source


def test_native_fallback_prefers_sequence_assets_before_malformed_montages():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    body = re.search(
        r"float ANocturnePlayerCharacter::PlayJacobMontageOrFallback\(.*?\n\}(?=\n\nvoid ANocturnePlayerCharacter::InitializeJacobAnimationFallback)",
        source,
        flags=re.S,
    )

    assert body
    assert "(bForceNativeAnimationFallback || bUsingSingleNodeAnimationFallback) && FallbackAnimation" in body.group(0)
    assert body.group(0).find("PlayJacobAnimationFallback(FallbackAnimation, bLoopFallback);") < body.group(0).find("PlayJacobMontage(Montage, StartSection);")


def test_tentacle_debug_lines_are_disabled_for_playable_slice():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "VestigeTentacleVisualAdapter->bDrawFallbackDebugLine = false;" in source


def test_animation_validation_checks_locomotion_skeletons_and_lengths():
    source = ANIMATION_VALIDATION.read_text(encoding="utf-8")

    assert "validate_locomotion_animation" in source
    assert "get_play_length" in source
    assert "ACTIVE_PLAYER_SKELETON_PATH" in source


def test_traversal_fallback_sequences_are_runtime_validated():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    validation = ANIMATION_VALIDATION.read_text(encoding="utf-8")

    for property_name, asset_name in (
        ("JumpStartFallbackAnimation", "FCS_SK_UAL1_MannequinArmature_Jump_Start"),
        ("JumpLoopAnimation", "FCS_SK_UAL1_MannequinArmature_Jump_Loop"),
        ("JumpLandAnimation", "FCS_SK_UAL1_MannequinArmature_Jump_Land"),
        ("DoubleJumpStartFallbackAnimation", "FCS_SK_UAL2_MannequinArmature_NinjaJump_Start"),
        ("DoubleJumpLoopAnimation", "FCS_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop"),
        ("DoubleJumpLandFallbackAnimation", "FCS_SK_UAL2_MannequinArmature_NinjaJump_Land"),
        ("SlideStartFallbackAnimation", "FCS_SK_UAL2_MannequinArmature_Slide_Start"),
        ("SlideLoopAnimation", "FCS_SK_UAL2_MannequinArmature_Slide_Loop"),
        ("SlideExitFallbackAnimation", "FCS_SK_UAL2_MannequinArmature_Slide_Exit"),
    ):
        assert property_name in source
        assert property_name in validation
        assert asset_name in source

    assert "HoldTraversalFallbackAnimation" in source
    assert "TraversalFallbackLockRemainingSeconds > 0.0f" in source
