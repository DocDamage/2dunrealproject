import re
from pathlib import Path

import unreal


PROJECT_ROOT = Path(unreal.Paths.project_dir())
PLAYER_SOURCE = PROJECT_ROOT / "Source" / "NocturneSignal" / "Private" / "NocturnePlayerCharacter.cpp"
LEVEL_PATH = "/Game/NocturneSignal/Slice01/Maps/L_Slice01GameplayTest"
PLAYER_LABEL = "Slice01_PlayablePlayer"
BASIC_CUBE_HALF_EXTENT = 50.0
GROUNDING_TOLERANCE = 5.0
VISIBLE_FLOOR_LABEL_PREFIX = "Slice01_Sakura_GroundTile_"
VISIBLE_FLOOR_MIN_EXTENT_X = 1750.0
VISIBLE_FLOOR_ALIGNMENT_TOLERANCE = 8.0
PLAYABLE_BOUNDS_MIN_X = -1500.0
PLAYABLE_BOUNDS_MAX_X = 1500.0
PLAYABLE_BOUND_TOLERANCE = 2.0
PARALLAX_LABELS = (
    "Slice01_Sakura_Parallax_SkyClouds",
    "Slice01_Sakura_Parallax_DistantTemples",
    "Slice01_Sakura_Parallax_MidgroundGarden",
    "Slice01_Sakura_Parallax_ForegroundRuins",
)
PARALLAX_MIN_WORLD_WIDTH = 5000.0


def log(message):
    unreal.log("[NocturneSlice01LevelMovementValidation] " + str(message))


def fail(message):
    raise RuntimeError(message)


def get_level_editor_subsystem():
    subsystem_type = getattr(unreal, "LevelEditorSubsystem", None)
    return unreal.get_editor_subsystem(subsystem_type) if subsystem_type else None


def load_level():
    subsystem = get_level_editor_subsystem()
    if subsystem:
        if not subsystem.load_level(LEVEL_PATH):
            fail("Could not load level: " + LEVEL_PATH)
        return

    if not unreal.EditorLevelLibrary.load_level(LEVEL_PATH):
        fail("Could not load level: " + LEVEL_PATH)


def get_actor_label(actor):
    try:
        return actor.get_actor_label()
    except Exception:
        return actor.get_name()


def find_actor(label):
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in actor_subsystem.get_all_level_actors():
        if get_actor_label(actor) == label:
            return actor
    return None


def validate_runtime_axis_contract():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    required_patterns = {
        "movement input uses screen X axis": r"AddMovementInput\s*\(\s*FVector::ForwardVector\s*,\s*AxisValue\s*\)",
        "grapple direction uses screen X axis": r"SetPreferredGrappleDirection\s*\(\s*FVector::ForwardVector\s*\*\s*FMath::Sign\(AxisValue\)\s*\)",
        "plane constraint keeps X/Z playable": r"SetPlaneConstraintNormal\s*\(\s*FVector::RightVector\s*\)",
    }
    missing = [name for name, pattern in required_patterns.items() if not re.search(pattern, source)]
    if missing:
        fail("Movement source does not satisfy axis contract: " + ", ".join(missing))


def get_scaled_capsule_half_height(player):
    capsule_component = player.get_component_by_class(unreal.CapsuleComponent)
    if not capsule_component:
        fail("Playable player has no CapsuleComponent for grounding validation.")

    try:
        return float(capsule_component.get_scaled_capsule_half_height())
    except Exception as exc:
        fail("Could not inspect playable player capsule half height: " + str(exc))


def validate_player_autopossess(player):
    try:
        auto_possess_player = player.get_editor_property("auto_possess_player")
    except Exception as exc:
        fail("Could not inspect playable player auto_possess_player: " + str(exc))

    if auto_possess_player != unreal.AutoReceiveInput.PLAYER0:
        fail(
            "Playable player must auto-possess Player 0 for PIE input; actual value is "
            + str(auto_possess_player)
        )


def validate_playable_player_grounding(player, floor):
    player_location = player.get_actor_location()
    floor_location = floor.get_actor_location()
    floor_scale = floor.get_actor_scale3d()
    floor_top_z = floor_location.z + BASIC_CUBE_HALF_EXTENT * floor_scale.z
    capsule_bottom_z = player_location.z - get_scaled_capsule_half_height(player)

    if abs(capsule_bottom_z - floor_top_z) > GROUNDING_TOLERANCE:
        fail(
            "Playable player capsule is not grounded on the main floor; "
            "player={}, capsule_bottom_z={:.2f}, floor_top_z={:.2f}".format(
                player_location,
                capsule_bottom_z,
                floor_top_z,
            )
        )


def validate_visible_floor_tiles(floor):
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    floor_tiles = [
        actor
        for actor in actor_subsystem.get_all_level_actors()
        if get_actor_label(actor).startswith(VISIBLE_FLOOR_LABEL_PREFIX)
    ]
    if not floor_tiles:
        fail("Missing visible Sakura gameplay floor tiles.")

    tile_locations = [actor.get_actor_location() for actor in floor_tiles]
    min_x = min(location.x for location in tile_locations)
    max_x = max(location.x for location in tile_locations)
    if min_x > -VISIBLE_FLOOR_MIN_EXTENT_X or max_x < VISIBLE_FLOOR_MIN_EXTENT_X:
        fail("Visible floor tiles do not cover the hold-right playtest range: {:.2f}..{:.2f}".format(min_x, max_x))

    floor_location = floor.get_actor_location()
    floor_scale = floor.get_actor_scale3d()
    floor_top_z = floor_location.z + BASIC_CUBE_HALF_EXTENT * floor_scale.z
    center_tile = min(floor_tiles, key=lambda actor: abs(actor.get_actor_location().x))
    center_tile_location = center_tile.get_actor_location()
    center_tile_scale = center_tile.get_actor_scale3d()
    center_tile_top_z = center_tile_location.z + BASIC_CUBE_HALF_EXTENT * center_tile_scale.y
    if abs(center_tile_top_z - floor_top_z) > VISIBLE_FLOOR_ALIGNMENT_TOLERANCE:
        fail(
            "Visible floor tile surface is not aligned with collision floor; "
            "tile_top_z={:.2f}, floor_top_z={:.2f}".format(center_tile_top_z, floor_top_z)
        )


def validate_playable_bounds():
    expected_bounds = {
        "Slice01_Collision_Bounds_Left": PLAYABLE_BOUNDS_MIN_X,
        "Slice01_Collision_Bounds_Right": PLAYABLE_BOUNDS_MAX_X,
    }
    for label, expected_x in expected_bounds.items():
        actor = find_actor(label)
        if not actor:
            fail("Missing playable bounds collision actor: " + label)

        location = actor.get_actor_location()
        if abs(location.x - expected_x) > PLAYABLE_BOUND_TOLERANCE or abs(location.y) > 1.0:
            fail("{} is not on the playable bounds contract: {}".format(label, location))


def validate_single_plate_parallax():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_labels = [get_actor_label(actor) for actor in actor_subsystem.get_all_level_actors()]
    for label in PARALLAX_LABELS:
        actor = find_actor(label)
        if not actor:
            fail("Missing parallax plate: " + label)

        tiled_labels = [
            actor_label
            for actor_label in all_labels
            if actor_label.startswith(label + "_Left") or actor_label.startswith(label + "_Right")
        ]
        if tiled_labels:
            fail("Parallax plate is still being repeated with non-seamless artwork: " + ", ".join(tiled_labels))

        scale = actor.get_actor_scale3d()
        world_width = scale.x * 100.0
        if world_width < PARALLAX_MIN_WORLD_WIDTH:
            fail("{} is too narrow for the bounded slice camera: {:.2f}".format(label, world_width))


def validate_level_contract():
    load_level()

    player = find_actor(PLAYER_LABEL)
    if not player:
        fail("Missing playable player actor: " + PLAYER_LABEL)

    player_location = player.get_actor_location()
    if abs(player_location.y) > 1.0:
        fail("Playable player is not on the side-view Y plane: " + str(player_location))

    required_anchors = {
        "Slice01_Anchor_Grapple_Right_Near": 470.0,
        "Slice01_Anchor_Grapple_Left_Near": -470.0,
        "Slice01_Anchor_Grapple_High": 820.0,
        "Slice01_Anchor_Consume_Dummy": -1120.0,
    }
    for label, expected_x in required_anchors.items():
        actor = find_actor(label)
        if not actor:
            fail("Missing anchor actor: " + label)
        location = actor.get_actor_location()
        if abs(location.x - expected_x) > 2.0 or abs(location.y) > 1.0:
            fail("{} is not on the X/Z side-view contract: {}".format(label, location))

    floor = find_actor("Slice01_Collision_Floor_Main")
    if not floor:
        fail("Missing main collision floor.")
    floor_scale = floor.get_actor_scale3d()
    if floor_scale.x <= floor_scale.y:
        fail("Main floor must span X more than Y for side-view play: " + str(floor_scale))

    validate_player_autopossess(player)
    validate_playable_player_grounding(player, floor)
    validate_visible_floor_tiles(floor)
    validate_playable_bounds()
    validate_single_plate_parallax()

    log("Loaded " + LEVEL_PATH)
    log("Playable player: " + str(player_location))
    log("Main floor scale: " + str(floor_scale))


def main():
    validate_runtime_axis_contract()
    validate_level_contract()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise

