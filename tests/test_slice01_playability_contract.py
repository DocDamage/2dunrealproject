import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYER_HEADER = PROJECT_ROOT / "Source" / "NocturneSignal" / "Public" / "NocturnePlayerCharacter.h"
PLAYER_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "NocturnePlayerCharacter.cpp"
GAME_MODE_HEADER = PROJECT_ROOT / "Source" / "NocturneSignal" / "Public" / "NocturneGameMode.h"
GAME_MODE_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "NocturneGameMode.cpp"
LEVEL_BUILDER = PROJECT_ROOT / "Tools" / "Unreal" / "build_jacob_gameplay_test.py"
LEVEL_VALIDATION = PROJECT_ROOT / "Tools" / "Unreal" / "validate_slice01_level_and_movement.py"
GRAPPLE_HEADER = PROJECT_ROOT / "Source" / "NocturneSignal" / "Public" / "GrappleAnchor.h"
GRAPPLE_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "GrappleAnchor.cpp"
VESTIGE_HEADER = PROJECT_ROOT / "Source" / "NocturneSignal" / "Public" / "VestigeLimbComponent.h"
VESTIGE_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "VestigeLimbComponent.cpp"
TENTACLE_VISUAL_HEADER = PROJECT_ROOT / "Source" / "NocturneSignal" / "Public" / "VestigeTentacleVisualAdapter.h"
TENTACLE_VISUAL_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "VestigeTentacleVisualAdapter.cpp"


def test_jacob_gameplay_test_spawns_player_on_main_floor_capsule_height():
    source = LEVEL_BUILDER.read_text(encoding="utf-8")

    assert "MAIN_FLOOR_LOCATION_Z = -50.0" in source
    assert "BASIC_CUBE_HALF_EXTENT = 50.0" in source
    assert "DEFAULT_CHARACTER_CAPSULE_HALF_HEIGHT = 88.0" in source
    assert "PLAYER_START_Z" in source
    assert re.search(
        r"PLAYER_START_Z\s*=\s*\(?\s*MAIN_FLOOR_LOCATION_Z\s*\+\s*"
        r"BASIC_CUBE_HALF_EXTENT\s*\*\s*COLLISION_SCALE_FLOOR_MAIN\.z\s*\+\s*"
        r"DEFAULT_CHARACTER_CAPSULE_HALF_HEIGHT\s*\+\s*PLAYER_GROUND_CLEARANCE",
        source,
    )
    assert re.search(
        r"spawn_actor_from_class\(\s*player_class\s*,\s*side_location\(0\.0,\s*PLAYER_START_Z\)",
        source,
        re.DOTALL,
    )
    assert "side_location(0.0, 120.0)" not in source


def test_jacob_gameplay_test_has_visible_floor_and_backdrop_coverage():
    source = LEVEL_BUILDER.read_text(encoding="utf-8")

    assert 'PARALLAX_LAYER_CLASS_PATH = "/Script/NocturneSignal.NocturneParallaxLayer"' in source
    assert "PARALLAX_TILE_OFFSETS = (0,)" in source
    assert "tuple(range(-4, 5))" not in source
    assert "configure_parallax_actor" in source
    assert "horizontal_follow_factor" in source
    assert '"scale_x"' in source
    assert '"scale_z"' in source
    assert "VISIBLE_FLOOR_TILE_EXTENT_X = 1900.0" in source
    assert "def spawn_visible_floor_tiles" in source
    assert "GroundTile_" in source
    assert "spawn_visible_floor_tiles(sakura_sprites)" in source
    assert "PLAYABLE_BOUNDS_MIN_X = -1500.0" in source
    assert "PLAYABLE_BOUNDS_MAX_X = 1500.0" in source
    assert "def spawn_playable_bounds" in source
    assert "spawn_playable_bounds(cube)" in source
    assert "not placed" not in source


def test_slice01_stage_has_tentacle_grabbable_props():
    builder = LEVEL_BUILDER.read_text(encoding="utf-8")
    grapple_header = GRAPPLE_HEADER.read_text(encoding="utf-8")
    grapple_source = GRAPPLE_SOURCE.read_text(encoding="utf-8")
    vestige_header = VESTIGE_HEADER.read_text(encoding="utf-8")
    vestige_source = VESTIGE_SOURCE.read_text(encoding="utf-8")

    assert "AnchorDisplayMesh" in grapple_header
    assert "bPullAnchorToGrappler" in grapple_header
    assert "ShouldPullAnchorToGrappler" in grapple_header
    assert "SetStaticMesh(nullptr)" not in grapple_source
    assert "TickPullAnchorToOwner" in vestige_header
    assert "CurrentAnchor->ShouldPullAnchorToGrappler()" in vestige_source
    assert "TickPullAnchorToOwner(DeltaTime);" in vestige_source
    assert "FinishGrappleRelease(false);" in vestige_source
    assert "def spawn_grabbable_prop" in builder
    assert "pull_anchor_to_grappler" in builder
    assert "Slice01_Grabbable_" in builder
    assert "SP_SakuraLantern" in builder
    assert "translucency_sort_priority" in builder
    assert "CollisionEnabled.NO_COLLISION" in builder
    assert "AnchorDisplayMesh" in builder


def test_grapple_state_machine_holds_extend_and_release_animations():
    vestige_header = VESTIGE_HEADER.read_text(encoding="utf-8")
    vestige_source = VESTIGE_SOURCE.read_text(encoding="utf-8")

    assert "GrappleExtendDuration" in vestige_header
    assert "GrappleReleaseDuration" in vestige_header
    assert "TickTimedGrappleState" in vestige_header
    assert "SetTimedGrappleState(EVestigeGrappleState::Extending, GrappleExtendDuration)" in vestige_source
    assert "SetTimedGrappleState(EVestigeGrappleState::Releasing, GrappleReleaseDuration)" in vestige_source
    assert "AdvanceFromExtendingState" in vestige_source
    assert "AdvanceFromReleasingState" in vestige_source
    assert "SetGrappleState(EVestigeGrappleState::Extending);\n    SetGrappleState(EVestigeGrappleState::Anchored);" not in vestige_source


def test_native_animation_fallback_does_not_stomp_action_clips():
    header = PLAYER_HEADER.read_text(encoding="utf-8")
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "TentacleGrappleStartFallbackAnimation" in header
    assert "TentacleGrappleReleaseFallbackAnimation" in header
    assert "bIsGrappleActionActive" in source
    assert "CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::TentacleGrapple" in source
    assert "bIsRecoveredCombatActionActive" in source
    assert "CurrentAbilityAnimation == ENocturneJacobAbilityAnimation::RecoveredCombat" in source
    assert "|| bIsGrappleActionActive" in source
    assert "|| bIsRecoveredCombatActionActive" in source
    assert "CurrentFallbackAnimation == TentacleGrappleFallbackAnimation" not in source


def test_active_player_uses_female_cyber_stalker_assets():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "SK_FemaleCyberStalker.SK_FemaleCyberStalker" in source
    assert "SK_Jacob.SK_Jacob" not in source
    assert "ABP_Jacob" not in source
    assert "GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -88.0f));" in source
    assert "GetMesh()->SetRelativeScale3D(FVector(1.0f));" in source
    assert "FCS_MM_Idle.FCS_MM_Idle" in source
    assert "FCS_Walk.FCS_Walk" in source
    assert "FCS_Run.FCS_Run" in source
    assert "FCS_Paired_ForceChoke_Att" in source
    assert "Characters/Jacob" not in source


def test_tentacle_vfx_package_is_wired_into_runtime_visual_adapter():
    header = TENTACLE_VISUAL_HEADER.read_text(encoding="utf-8")
    source = TENTACLE_VISUAL_SOURCE.read_text(encoding="utf-8")

    assert "bUseTentaclesVfxPackage" in header
    assert "TentaclesVfxBeamMesh" in header
    assert "TentaclesVfxGooActorClass" in header
    assert "bSpawnTentaclesVfxGooActor = false" in header
    assert "TentaclesVfxImpactMesh" in header
    assert "TentaclesVfxImpactMaterial" in header
    assert "TentacleImpactComponent" in header
    assert "LoadTentaclesVfxPackageDefaults" in source
    assert "SM_VFX_Arm_Double_01" in source
    assert "MI_VFX_Goo_Arm_Dark_01" in source
    assert "SM_VFX_Smooth_Sphere_01" in source
    assert "MI_VFX_Goo_Dark_01" in source
    assert "BP_Goo.BP_Goo_C" in source
    assert "bSpawnTentaclesVfxGooActor && !TentaclesVfxGooActorClass" in source
    assert "!bSpawnTentaclesVfxGooActor || !TentaclesVfxGooActorClass" in source
    assert "NewObject<UStaticMeshComponent>(Owner, TEXT(\"VestigeTentacleImpact\"))" in source
    assert "UpdateTentaclesVfxActor(WorldEnd);" in source
    assert "ShowTentacleActionVisualCue" in PLAYER_SOURCE.read_text(encoding="utf-8")
    assert "VestigeTentacleVisualAdapter->UpdateLimbTarget" in PLAYER_SOURCE.read_text(encoding="utf-8")


def test_side_view_camera_frames_player_below_center():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "CameraBoom->SetRelativeLocation(FVector(0.0f, 0.0f, 320.0f));" in source


def test_side_view_camera_clamps_vertical_frame_during_grapples():
    header = PLAYER_HEADER.read_text(encoding="utf-8")
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "void UpdateSliceCameraFrame();" in header
    assert "SliceCameraMinWorldZ" in header
    assert "SliceCameraMaxWorldZ" in header
    assert "UpdateSliceCameraFrame();" in source
    assert "FMath::Clamp(DesiredWorldZ, SliceCameraMinWorldZ, SliceCameraMaxWorldZ)" in source


def test_player_character_forces_player_controller_to_side_view_camera():
    header = PLAYER_HEADER.read_text(encoding="utf-8")
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "void RefreshSliceCameraViewTarget();" in header
    assert "void ANocturnePlayerCharacter::RefreshSliceCameraViewTarget()" in source
    assert "SideViewCamera->SetActive(true);" in source
    assert "PlayerController->SetViewTarget(this);" in source
    assert re.search(
        r"void ANocturnePlayerCharacter::BeginPlay\(\)"
        r"\s*\{(?:(?!\n\}).)*RefreshSliceCameraViewTarget\(\);",
        source,
        re.DOTALL,
    )
    assert re.search(
        r"void ANocturnePlayerCharacter::PossessedBy\(AController\* NewController\)"
        r"\s*\{(?:(?!\n\}).)*RefreshSliceCameraViewTarget\(\);",
        source,
        re.DOTALL,
    )
    assert re.search(
        r"void ANocturnePlayerCharacter::OnRep_Controller\(\)"
        r"\s*\{(?:(?!\n\}).)*RefreshSliceCameraViewTarget\(\);",
        source,
        re.DOTALL,
    )


def test_game_mode_reuses_the_level_placed_player0_character():
    header = GAME_MODE_HEADER.read_text(encoding="utf-8")
    source = GAME_MODE_SOURCE.read_text(encoding="utf-8")

    assert "HandleStartingNewPlayer_Implementation(APlayerController* NewPlayer) override;" in header
    assert "TActorIterator<ANocturnePlayerCharacter>" in source
    assert "AutoPossessPlayer == EAutoReceiveInput::Player0" in source
    assert "NewPlayer->Possess(PlacedPlayer);" in source


def test_player_character_adds_slice_input_mapping_when_possessed():
    header = PLAYER_HEADER.read_text(encoding="utf-8")
    source = PLAYER_SOURCE.read_text(encoding="utf-8")

    assert "virtual void PossessedBy(AController* NewController) override;" in header
    assert "virtual void OnRep_Controller() override;" in header
    assert re.search(
        r"void ANocturnePlayerCharacter::PossessedBy\(AController\* NewController\)"
        r"\s*\{[^{}]*Super::PossessedBy\(NewController\);[^{}]*AddSliceInputMappingContext\(\);",
        source,
        re.DOTALL,
    )
    assert re.search(
        r"void ANocturnePlayerCharacter::OnRep_Controller\(\)"
        r"\s*\{[^{}]*Super::OnRep_Controller\(\);[^{}]*AddSliceInputMappingContext\(\);",
        source,
        re.DOTALL,
    )


def test_slice01_level_validation_checks_grounding_and_current_project_source():
    source = LEVEL_VALIDATION.read_text(encoding="utf-8")

    assert "unreal.Paths.project_dir()" in source
    assert "validate_playable_player_grounding" in source
    assert "validate_visible_floor_tiles" in source
    assert "validate_playable_bounds" in source
    assert "validate_single_plate_parallax" in source
    assert "get_scaled_capsule_half_height" in source
    assert "auto_possess_player" in source
    assert "unreal.AutoReceiveInput.PLAYER0" in source

