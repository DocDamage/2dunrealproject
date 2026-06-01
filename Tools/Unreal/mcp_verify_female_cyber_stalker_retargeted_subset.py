import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
EXPECTED_SKELETON = (
    "/Game/NocturneSignal/Characters/FemaleCyberStalker/"
    "SK_FemaleCyberStalker_Skeleton.SK_FemaleCyberStalker_Skeleton"
)

EXPECTED_ANIMATIONS = {
    "native_walk": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Walk.FCS_Walk",
    "native_run": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Run.FCS_Run",
    "idle": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RogueCharacter/FCS_MM_Idle.FCS_MM_Idle",
    "jump_single": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RogueCharacter/FCS_MM_Jump.FCS_MM_Jump",
    "fall_loop": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RogueCharacter/FCS_MM_Fall_Loop.FCS_MM_Fall_Loop",
    "land": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RogueCharacter/FCS_MM_Land.FCS_MM_Land",
    "jump_start": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary1/FCS_SK_UAL1_MannequinArmature_Jump_Start.FCS_SK_UAL1_MannequinArmature_Jump_Start",
    "jump_loop": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary1/FCS_SK_UAL1_MannequinArmature_Jump_Loop.FCS_SK_UAL1_MannequinArmature_Jump_Loop",
    "jump_land": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary1/FCS_SK_UAL1_MannequinArmature_Jump_Land.FCS_SK_UAL1_MannequinArmature_Jump_Land",
    "slide_start": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_Slide_Start.FCS_SK_UAL2_MannequinArmature_Slide_Start",
    "slide_loop": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_Slide_Loop.FCS_SK_UAL2_MannequinArmature_Slide_Loop",
    "slide_exit": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_Slide_Exit.FCS_SK_UAL2_MannequinArmature_Slide_Exit",
    "double_jump_start": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_NinjaJump_Start.FCS_SK_UAL2_MannequinArmature_NinjaJump_Start",
    "double_jump_loop": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop.FCS_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop",
    "double_jump_land": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/UniversalAnimationLibrary2/FCS_SK_UAL2_MannequinArmature_NinjaJump_Land.FCS_SK_UAL2_MannequinArmature_NinjaJump_Land",
    "tentacle_attack": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_Att.FCS_Paired_ForceChoke_Att",
    "tentacle_grapple_start": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_Start_Att.FCS_Paired_ForceChoke_Start_Att",
    "tentacle_grapple_loop": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_Loop_Att.FCS_Paired_ForceChoke_Loop_Att",
    "tentacle_grapple_release": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_ForceChoke_End_Att.FCS_Paired_ForceChoke_End_Att",
    "tentacle_consume": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_SneakNeckBreak_Att.FCS_Paired_SneakNeckBreak_Att",
    "tentacle_consume_alternate": "/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/RamsterZ/FCS_Paired_Knife_Stealth_KidneyAndNeck_Att.FCS_Paired_Knife_Stealth_KidneyAndNeck_Att",
}


def send_request(host, port, request, timeout=30.0):
    request_name = request.get("method") or request.get("kind") or "mcp_request"
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall((json.dumps(request, separators=(",", ":")) + "\n").encode("utf-8"))
        data = bytearray()
        deadline = time.monotonic() + timeout
        while b"\n" not in data:
            if time.monotonic() > deadline:
                raise TimeoutError(request_name)
            data.extend(sock.recv(65536))
    response = json.loads(bytes(data).split(b"\n", 1)[0].decode("utf-8"))
    if response.get("ok") is not True:
        raise RuntimeError("{} failed: {}".format(request_name, response.get("error")))
    return response["result"]


def exec_python(host, port, code, timeout=30.0, request_id=None):
    return send_request(
        host,
        port,
        {
            "id": request_id or "exec_python",
            "kind": "exec_python",
            "args": {"expression": "exec(" + repr(code) + ") or RESULT"},
        },
        timeout=timeout,
    )


def parse_repr_dict(result):
    try:
        value = ast.literal_eval(result.get("repr", "{}"))
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError("Could not parse MCP result: {}".format(exc))
    if not isinstance(value, dict):
        raise RuntimeError("Unexpected MCP result: " + repr(value))
    return value


def verify_retargeted_subset(host, port):
    code = """
import unreal

expected_skeleton = {expected_skeleton!r}
expected_animations = {expected_animations!r}
results = {{}}

for label, path in expected_animations.items():
    anim = unreal.EditorAssetLibrary.load_asset(path)
    if not anim:
        raise RuntimeError("Missing Female Cyber Stalker animation for " + label + ": " + path)
    try:
        skeleton = anim.get_editor_property("skeleton")
    except Exception:
        skeleton = anim.get_skeleton() if hasattr(anim, "get_skeleton") else None
    try:
        length = float(anim.get_play_length())
    except Exception:
        try:
            length = float(anim.get_editor_property("sequence_length"))
        except Exception:
            length = 0.0
    results[label] = {{
        "path": path,
        "class": anim.get_class().get_name(),
        "skeleton": skeleton.get_path_name() if skeleton else "",
        "length": length,
    }}

RESULT = results
""".format(expected_skeleton=EXPECTED_SKELETON, expected_animations=EXPECTED_ANIMATIONS)
    result = parse_repr_dict(exec_python(host, port, code, timeout=60.0, request_id="verify-fcs-retargeted-subset"))

    for label, info in result.items():
        if EXPECTED_SKELETON not in info.get("skeleton", ""):
            raise RuntimeError("{} is bound to the wrong skeleton: {}".format(label, info.get("skeleton", "")))
        if info.get("length", 0.0) <= 0.0:
            raise RuntimeError("{} has no playable length".format(label))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    result = verify_retargeted_subset(args.host, args.port)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
