import re
from pathlib import Path

import unreal


INPUT_DIR = "/Game/NocturneSignal/Input"
MAPPING_CONTEXT = f"{INPUT_DIR}/IMC_Slice01.IMC_Slice01"

EXPECTED_ACTION_TYPES = {
    "IA_MoveHorizontal": unreal.InputActionValueType.AXIS1D,
    "IA_MoveLeft": unreal.InputActionValueType.BOOLEAN,
    "IA_MoveRight": unreal.InputActionValueType.BOOLEAN,
    "IA_Jump": unreal.InputActionValueType.BOOLEAN,
    "IA_Slide": unreal.InputActionValueType.BOOLEAN,
    "IA_TentacleGrapple": unreal.InputActionValueType.BOOLEAN,
    "IA_TentacleAttack": unreal.InputActionValueType.BOOLEAN,
    "IA_TentacleConsume": unreal.InputActionValueType.BOOLEAN,
    "IA_TentacleAlternateConsume": unreal.InputActionValueType.BOOLEAN,
}

EXPECTED_CONTEXT_MAPPINGS = {
    "IA_MoveHorizontal": {"Gamepad_LeftX"},
    "IA_MoveLeft": {"A", "Left", "Gamepad_DPad_Left"},
    "IA_MoveRight": {"D", "Right", "Gamepad_DPad_Right"},
    "IA_Jump": {"SpaceBar", "Gamepad_FaceButton_Bottom"},
    "IA_Slide": {"LeftShift", "Gamepad_FaceButton_Left", "Gamepad_LeftShoulder"},
    "IA_TentacleGrapple": {"E", "Gamepad_RightShoulder"},
    "IA_TentacleAttack": {"LeftMouseButton", "Gamepad_RightTrigger"},
    "IA_TentacleConsume": {"F", "Gamepad_FaceButton_Right"},
    "IA_TentacleAlternateConsume": {"R", "Gamepad_FaceButton_Top"},
}

EXPECTED_LEGACY_AXIS = {
    ("MoveHorizontal", "-1.000000", "A"),
    ("MoveHorizontal", "1.000000", "D"),
    ("MoveHorizontal", "-1.000000", "Left"),
    ("MoveHorizontal", "1.000000", "Right"),
    ("MoveHorizontal", "1.000000", "Gamepad_LeftX"),
    ("MoveHorizontal", "-1.000000", "Gamepad_DPad_Left"),
    ("MoveHorizontal", "1.000000", "Gamepad_DPad_Right"),
}

EXPECTED_LEGACY_ACTIONS = {
    ("Jump", "SpaceBar"),
    ("Jump", "Gamepad_FaceButton_Bottom"),
    ("Slide", "LeftShift"),
    ("Slide", "Gamepad_FaceButton_Left"),
    ("Slide", "Gamepad_LeftShoulder"),
    ("TentacleGrapple", "E"),
    ("TentacleGrapple", "Gamepad_RightShoulder"),
    ("TentacleAttack", "LeftMouseButton"),
    ("TentacleAttack", "Gamepad_RightTrigger"),
    ("TentacleConsume", "F"),
    ("TentacleConsume", "Gamepad_FaceButton_Right"),
    ("TentacleAlternateConsume", "R"),
    ("TentacleAlternateConsume", "Gamepad_FaceButton_Top"),
}


def fail(message):
    raise RuntimeError(f"Slice 01 input validation failed: {message}")


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        fail(f"missing asset {path}")
    return asset


def validate_actions():
    for action_name, expected_type in EXPECTED_ACTION_TYPES.items():
        action = load_asset(f"{INPUT_DIR}/{action_name}.{action_name}")
        actual_type = action.get_editor_property("value_type")
        if actual_type != expected_type:
            fail(f"{action_name} value_type is {actual_type}, expected {expected_type}")


def get_context_mappings(context):
    mapping_data = context.get_editor_property("default_key_mappings")
    mappings = mapping_data.get_editor_property("mappings")
    actual = {}

    for mapping in mappings:
        action = mapping.get_editor_property("action")
        key = mapping.get_editor_property("key")
        if not action or not key:
            continue

        action_name = action.get_name()
        key_name = str(key.get_editor_property("key_name"))
        actual.setdefault(action_name, set()).add(key_name)

    return actual


def validate_mapping_context():
    context = load_asset(MAPPING_CONTEXT)
    actual = get_context_mappings(context)

    for action_name, expected_keys in EXPECTED_CONTEXT_MAPPINGS.items():
        actual_keys = actual.get(action_name, set())
        missing = expected_keys - actual_keys
        extra = actual_keys - expected_keys
        if missing or extra:
            fail(
                f"{action_name} mapping mismatch; missing={sorted(missing)} extra={sorted(extra)}"
            )

    unexpected_actions = set(actual.keys()) - set(EXPECTED_CONTEXT_MAPPINGS.keys())
    if unexpected_actions:
        fail(f"unexpected actions in {MAPPING_CONTEXT}: {sorted(unexpected_actions)}")


def validate_legacy_input_config():
    config_path = Path(unreal.Paths.project_dir()) / "Config" / "DefaultInput.ini"
    text = config_path.read_text(encoding="utf-8-sig")

    axis_pattern = re.compile(
        r'AxisMappings=\(AxisName="([^"]+)",Scale=([-0-9.]+),Key=([^)]+)\)'
    )
    action_pattern = re.compile(
        r'ActionMappings=\(ActionName="([^"]+)".*?,Key=([^)]+)\)'
    )

    actual_axis = set(axis_pattern.findall(text))
    actual_actions = set(action_pattern.findall(text))

    missing_axis = EXPECTED_LEGACY_AXIS - actual_axis
    missing_actions = EXPECTED_LEGACY_ACTIONS - actual_actions
    if missing_axis:
        fail(f"missing legacy axis mappings: {sorted(missing_axis)}")
    if missing_actions:
        fail(f"missing legacy action mappings: {sorted(missing_actions)}")


def main():
    validate_actions()
    validate_mapping_context()
    validate_legacy_input_config()
    unreal.log("Slice 01 input validation passed.")


main()
