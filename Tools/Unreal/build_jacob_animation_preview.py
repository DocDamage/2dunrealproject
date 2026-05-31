import unreal


LEVEL_PATH = "/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobAnimationPreview"
JACOB_MESH_PATH = "/Game/NocturneSignal/Characters/Jacob/SK_Jacob.SK_Jacob"
COMMAND_LINE = unreal.SystemLibrary.get_command_line().lower()
IS_HEADLESS_RUN = "-nullrhi" in COMMAND_LINE or "unrealeditor-cmd" in COMMAND_LINE

TENTACLE_MESH_ROWS = [
    (
        "Tentacle Cylinder Primary",
        "/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/hand_18/SkeletalMeshes/Cylinder.Cylinder",
        unreal.Vector(0.0, 1850.0, 95.0),
    ),
    (
        "Tentacle Cylinder 041",
        "/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/hand_18/SkeletalMeshes/Cylinder_041.Cylinder_041",
        unreal.Vector(300.0, 1850.0, 95.0),
    ),
    (
        "Tentacle Cylinder 082",
        "/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/hand_18/SkeletalMeshes/Cylinder_082.Cylinder_082",
        unreal.Vector(600.0, 1850.0, 95.0),
    ),
]

ANIMATION_ROWS = [
    (
        "MCO Sword Ready Idle",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Ready_Idle_001.JAC_KBS_Ready_Idle_001",
        unreal.Vector(0.0, 0.0, 95.0),
    ),
    (
        "MCO Sword Walk In Place",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Walk_F_001_IP.JAC_KBS_Walk_F_001_IP",
        unreal.Vector(250.0, 0.0, 95.0),
    ),
    (
        "MCO Sword Run In Place",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Run_F_001_IP.JAC_KBS_Run_F_001_IP",
        unreal.Vector(500.0, 0.0, 95.0),
    ),
    (
        "MCO Sword Combo Attack",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Sword_ATK_Combo_01_001_IP.JAC_KBS_Sword_ATK_Combo_01_001_IP",
        unreal.Vector(750.0, 0.0, 95.0),
    ),
    (
        "Motifect Sword Draw Stance",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_draw_stance.JAC_sword_draw_stance",
        unreal.Vector(0.0, 350.0, 95.0),
    ),
    (
        "Motifect Sword Slash",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_slash_horizontal.JAC_sword_slash_horizontal",
        unreal.Vector(250.0, 350.0, 95.0),
    ),
    (
        "Motifect Sword Thrust",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_thrust_forward.JAC_sword_thrust_forward",
        unreal.Vector(500.0, 350.0, 95.0),
    ),
    (
        "Motifect Sword Parry Riposte",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_parry_and_riposte.JAC_sword_parry_and_riposte",
        unreal.Vector(750.0, 350.0, 95.0),
    ),
    (
        "UAL1 Jump Start",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1/JAC_SK_UAL1_MannequinArmature_Jump_Start.JAC_SK_UAL1_MannequinArmature_Jump_Start",
        unreal.Vector(0.0, 700.0, 95.0),
    ),
    (
        "UAL1 Jump Loop",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1/JAC_SK_UAL1_MannequinArmature_Jump_Loop.JAC_SK_UAL1_MannequinArmature_Jump_Loop",
        unreal.Vector(250.0, 700.0, 95.0),
    ),
    (
        "UAL1 Jump Land",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1/JAC_SK_UAL1_MannequinArmature_Jump_Land.JAC_SK_UAL1_MannequinArmature_Jump_Land",
        unreal.Vector(500.0, 700.0, 95.0),
    ),
    (
        "UAL2 Slide Start",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_Slide_Start.JAC_SK_UAL2_MannequinArmature_Slide_Start",
        unreal.Vector(0.0, 1050.0, 95.0),
    ),
    (
        "UAL2 Slide Loop",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_Slide_Loop.JAC_SK_UAL2_MannequinArmature_Slide_Loop",
        unreal.Vector(250.0, 1050.0, 95.0),
    ),
    (
        "UAL2 Slide Exit",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_Slide_Exit.JAC_SK_UAL2_MannequinArmature_Slide_Exit",
        unreal.Vector(500.0, 1050.0, 95.0),
    ),
    (
        "UAL2 Double Jump Start",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_NinjaJump_Start.JAC_SK_UAL2_MannequinArmature_NinjaJump_Start",
        unreal.Vector(0.0, 1400.0, 95.0),
    ),
    (
        "UAL2 Double Jump Loop",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop.JAC_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop",
        unreal.Vector(250.0, 1400.0, 95.0),
    ),
    (
        "UAL2 Double Jump Land",
        "/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_NinjaJump_Land.JAC_SK_UAL2_MannequinArmature_NinjaJump_Land",
        unreal.Vector(500.0, 1400.0, 95.0),
    ),
]


def log(message):
    unreal.log("[NocturneJacobAnimPreview] " + str(message))


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


def set_label(actor, label):
    try:
        actor.set_actor_label(label)
    except Exception:
        pass


def spawn_text(label, location):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.TextRenderActor,
        location,
        unreal.Rotator(0.0, 180.0, 0.0),
    )
    set_label(actor, "TXT_" + label.replace(" ", "_"))
    component = actor.get_component_by_class(unreal.TextRenderComponent)
    if component:
        component.set_editor_property("text", label)
        component.set_editor_property("horizontal_alignment", unreal.HorizTextAligment.EHTA_CENTER)
        component.set_editor_property("world_size", 24.0)
    return actor


def spawn_preview_actor(label, animation, mesh, location):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkeletalMeshActor,
        location,
        unreal.Rotator(0.0, 180.0, 0.0),
    )
    set_label(actor, "JacobPreview_" + label.replace(" ", "_"))
    component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if not component:
        raise RuntimeError("Spawned actor has no SkeletalMeshComponent: " + label)

    component.set_skeletal_mesh_asset(mesh)
    component.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    component.set_animation(animation)
    component.set_play_rate(1.0)
    if not IS_HEADLESS_RUN:
        component.play(True)
        component.set_update_animation_in_editor(True)
    component.set_editor_property("enable_update_rate_optimizations", False)
    return actor


def spawn_mesh_preview_actor(label, mesh, location):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkeletalMeshActor,
        location,
        unreal.Rotator(0.0, 180.0, 0.0),
    )
    set_label(actor, "JacobPreview_" + label.replace(" ", "_"))
    component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if not component:
        raise RuntimeError("Spawned actor has no SkeletalMeshComponent: " + label)

    component.set_skeletal_mesh_asset(mesh)
    component.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    if not IS_HEADLESS_RUN:
        component.set_update_animation_in_editor(True)
    component.set_editor_property("enable_update_rate_optimizations", False)
    return actor


def spawn_lighting_and_camera():
    light = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(300.0, -450.0, 700.0),
        unreal.Rotator(-45.0, -35.0, 0.0),
    )
    set_label(light, "Preview_KeyLight")
    light_component = light.get_component_by_class(unreal.DirectionalLightComponent)
    if light_component:
        light_component.set_editor_property("intensity", 4.0)

    camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(375.0, -1250.0, 560.0),
        unreal.Rotator(-18.0, 0.0, 0.0),
    )
    set_label(camera, "Preview_Camera")
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(
        unreal.Vector(375.0, -1250.0, 560.0),
        unreal.Rotator(-18.0, 0.0, 0.0),
    )


def open_or_create_level():
    if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        if not unreal.EditorLevelLibrary.load_level(LEVEL_PATH):
            raise RuntimeError("Failed to load preview level: " + LEVEL_PATH)
        return

    if not unreal.EditorLevelLibrary.new_level(LEVEL_PATH):
        raise RuntimeError("Failed to create preview level: " + LEVEL_PATH)


def clear_preview_actors():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in actor_subsystem.get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            label = actor.get_name()
        if label.startswith("JacobPreview_") or label.startswith("TXT_") or label.startswith("Preview_"):
            actor_subsystem.destroy_actor(actor)


def main():
    unreal.EditorAssetLibrary.make_directory("/Game/NocturneSignal/Characters/Jacob/Maps")
    mesh = load_asset(JACOB_MESH_PATH)
    rows = [(label, load_asset(path), location) for label, path, location in ANIMATION_ROWS]
    tentacle_rows = [(label, load_asset(path), location) for label, path, location in TENTACLE_MESH_ROWS]

    open_or_create_level()
    clear_preview_actors()

    spawn_lighting_and_camera()

    for label, animation, location in rows:
        spawn_preview_actor(label, animation, mesh, location)
        spawn_text(label, location + unreal.Vector(0.0, -90.0, -10.0))

    for label, tentacle_mesh, location in tentacle_rows:
        spawn_mesh_preview_actor(label, tentacle_mesh, location)
        spawn_text(label, location + unreal.Vector(0.0, -90.0, -10.0))

    unreal.EditorLevelLibrary.save_current_level()
    log("Built preview level: " + LEVEL_PATH)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
