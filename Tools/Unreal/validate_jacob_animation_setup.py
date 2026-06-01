import unreal


PLAYER_CLASS_PATH = "/Script/NocturneSignal.NocturnePlayerCharacter"
ACTIVE_PLAYER_MESH_PATH = (
    "/Game/NocturneSignal/Characters/FemaleCyberStalker/"
    "SK_FemaleCyberStalker.SK_FemaleCyberStalker"
)
ACTIVE_PLAYER_SKELETON_PATH = (
    "/Game/NocturneSignal/Characters/FemaleCyberStalker/"
    "SK_FemaleCyberStalker_Skeleton.SK_FemaleCyberStalker_Skeleton"
)

BASE_REQUIRED_PROPERTIES = (
    "IdleAnimation",
    "WalkAnimation",
    "RunAnimation",
    "JumpStartFallbackAnimation",
    "JumpLoopAnimation",
    "SlideLoopAnimation",
    "JumpLandAnimation",
    "DoubleJumpStartFallbackAnimation",
    "DoubleJumpLoopAnimation",
    "DoubleJumpLandFallbackAnimation",
    "SlideStartFallbackAnimation",
    "SlideExitFallbackAnimation",
    "TentacleAttackFallbackAnimation",
    "TentacleGrappleStartFallbackAnimation",
    "TentacleGrappleFallbackAnimation",
    "TentacleGrappleReleaseFallbackAnimation",
    "TentacleConsumeFallbackAnimation",
    "TentacleAlternateConsumeFallbackAnimation",
)

RECOVERED_MONTAGE_SECTIONS = {}

REQUIRED_PROPERTIES = BASE_REQUIRED_PROPERTIES + tuple(RECOVERED_MONTAGE_SECTIONS.keys())


def log(message):
    unreal.log("[NocturnePlayerAnimationValidation] " + str(message))


def fail(message):
    raise RuntimeError(message)


def montage_section_names(montage):
    if not montage:
        return []
    return [str(montage.get_section_name(index)) for index in range(montage.get_num_sections())]


def validate_jacob_montage(property_name, montage, expected_sections):
    if not montage:
        fail("Missing recovered combat montage: " + property_name)

    skeleton = montage.get_skeleton() if hasattr(montage, "get_skeleton") else None
    skeleton_path = skeleton.get_path_name() if skeleton else ""
    if skeleton_path != ACTIVE_PLAYER_SKELETON_PATH:
        fail(property_name + " uses unexpected skeleton: " + skeleton_path)

    actual_sections = montage_section_names(montage)
    if actual_sections != expected_sections:
        fail(
            property_name
            + " sections mismatch. Expected "
            + ", ".join(expected_sections)
            + "; got "
            + ", ".join(actual_sections)
        )

    log(property_name + ": " + montage.get_path_name() + " sections=" + ", ".join(actual_sections))


def get_animation_skeleton(animation):
    if not animation:
        return None
    if hasattr(animation, "get_skeleton"):
        return animation.get_skeleton()
    try:
        return animation.get_editor_property("skeleton")
    except Exception:
        return None


def validate_locomotion_animation(property_name, animation):
    if not animation:
        fail("Missing active player locomotion animation: " + property_name)

    skeleton = get_animation_skeleton(animation)
    skeleton_path = skeleton.get_path_name() if skeleton else ""
    if skeleton_path != ACTIVE_PLAYER_SKELETON_PATH:
        fail(property_name + " uses unexpected skeleton: " + skeleton_path)

    if hasattr(animation, "get_play_length"):
        play_length = float(animation.get_play_length())
        if play_length <= 0.0:
            fail(property_name + " has no playable duration.")


def main():
    player_class = unreal.load_class(None, PLAYER_CLASS_PATH)
    if not player_class:
        fail("Could not load player class: " + PLAYER_CLASS_PATH)

    player_default = unreal.get_default_object(player_class)
    mesh_component = player_default.get_component_by_class(unreal.SkeletalMeshComponent)
    if not mesh_component:
        fail("Nocturne player default has no SkeletalMeshComponent.")

    skeletal_mesh = None
    for accessor in ("get_skeletal_mesh_asset", "get_skeletal_mesh"):
        if hasattr(mesh_component, accessor):
            skeletal_mesh = getattr(mesh_component, accessor)()
            break

    if not skeletal_mesh:
        skeletal_mesh = mesh_component.get_editor_property("skeletal_mesh_asset")
    if not skeletal_mesh:
        fail("Active player skeletal mesh is not assigned on the player default.")

    if skeletal_mesh.get_path_name() != ACTIVE_PLAYER_MESH_PATH:
        fail("Active player is using the wrong skeletal mesh: " + skeletal_mesh.get_path_name())

    mesh_skeleton = skeletal_mesh.get_editor_property("skeleton")
    mesh_skeleton_path = mesh_skeleton.get_path_name() if mesh_skeleton else ""
    if mesh_skeleton_path != ACTIVE_PLAYER_SKELETON_PATH:
        fail("Active player mesh uses unexpected skeleton: " + mesh_skeleton_path)

    anim_class = mesh_component.get_editor_property("anim_class")

    missing = []
    for property_name in REQUIRED_PROPERTIES:
        if not player_default.get_editor_property(property_name):
            missing.append(property_name)

    if missing:
        fail("Missing active player animation fallback assets: " + ", ".join(missing))

    log("Active player mesh: " + skeletal_mesh.get_path_name())
    log("Anim class: " + (anim_class.get_path_name() if anim_class else "<single-node fallback>"))
    for property_name in REQUIRED_PROPERTIES:
        asset = player_default.get_editor_property(property_name)
        log(property_name + ": " + asset.get_path_name())

    for property_name in BASE_REQUIRED_PROPERTIES:
        validate_locomotion_animation(property_name, player_default.get_editor_property(property_name))

    for property_name, expected_sections in RECOVERED_MONTAGE_SECTIONS.items():
        validate_jacob_montage(
            property_name,
            player_default.get_editor_property(property_name),
            expected_sections,
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
