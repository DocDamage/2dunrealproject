import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
PLAYER_CLASS = "/Script/NocturneSignal.NocturnePlayerCharacter"
EXPECTED_MESH = (
    "/Game/NocturneSignal/Characters/FemaleCyberStalker/"
    "SK_FemaleCyberStalker.SK_FemaleCyberStalker"
)
EXPECTED_SKELETON = (
    "/Game/NocturneSignal/Characters/FemaleCyberStalker/"
    "SK_FemaleCyberStalker_Skeleton.SK_FemaleCyberStalker_Skeleton"
)
EXPECTED_FALLBACKS = {
    "IdleAnimation": "FCS_MM_Idle.FCS_MM_Idle",
    "WalkAnimation": "FCS_Walk.FCS_Walk",
    "RunAnimation": "FCS_Run.FCS_Run",
    "JumpStartFallbackAnimation": "FCS_SK_UAL1_MannequinArmature_Jump_Start",
    "JumpLoopAnimation": "FCS_SK_UAL1_MannequinArmature_Jump_Loop",
    "JumpLandAnimation": "FCS_SK_UAL1_MannequinArmature_Jump_Land",
    "DoubleJumpStartFallbackAnimation": "FCS_SK_UAL2_MannequinArmature_NinjaJump_Start",
    "DoubleJumpLoopAnimation": "FCS_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop",
    "DoubleJumpLandFallbackAnimation": "FCS_SK_UAL2_MannequinArmature_NinjaJump_Land",
    "FallLoopAnimation": "FCS_MM_Fall_Loop.FCS_MM_Fall_Loop",
    "SlideStartFallbackAnimation": "FCS_SK_UAL2_MannequinArmature_Slide_Start",
    "SlideLoopAnimation": "FCS_SK_UAL2_MannequinArmature_Slide_Loop",
    "SlideExitFallbackAnimation": "FCS_SK_UAL2_MannequinArmature_Slide_Exit",
    "TentacleAttackFallbackAnimation": "FCS_Paired_ForceChoke_Att",
    "TentacleGrappleStartFallbackAnimation": "FCS_Paired_ForceChoke_Start_Att",
    "TentacleGrappleFallbackAnimation": "FCS_Paired_ForceChoke_Loop_Att",
    "TentacleGrappleReleaseFallbackAnimation": "FCS_Paired_ForceChoke_End_Att",
    "TentacleConsumeFallbackAnimation": "FCS_Paired_SneakNeckBreak_Att",
    "TentacleAlternateConsumeFallbackAnimation": "FCS_Paired_Knife_Stealth_KidneyAndNeck_Att",
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


def verify_active_player(host, port):
    code = """
import unreal

player_class = unreal.load_class(None, {player_class!r})
if not player_class:
    raise RuntimeError("Could not load player class")
player_default = unreal.get_default_object(player_class)
mesh_component = player_default.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh_component:
    raise RuntimeError("Player default has no SkeletalMeshComponent")

mesh = None
for accessor in ("get_skeletal_mesh_asset", "get_skeletal_mesh"):
    if hasattr(mesh_component, accessor):
        mesh = getattr(mesh_component, accessor)()
        break
if not mesh:
    mesh = mesh_component.get_editor_property("skeletal_mesh_asset")
skeleton = mesh.get_editor_property("skeleton") if mesh else None
relative_location = mesh_component.get_editor_property("relative_location")
relative_scale = mesh_component.get_editor_property("relative_scale3d")
anim_class = mesh_component.get_editor_property("anim_class")
animation_mode = str(mesh_component.get_editor_property("animation_mode"))

fallbacks = {{}}
expected_fallbacks = {expected_fallbacks!r}
for property_name in expected_fallbacks:
    asset = player_default.get_editor_property(property_name)
    asset_skeleton = None
    if asset:
        if hasattr(asset, "get_skeleton"):
            asset_skeleton = asset.get_skeleton()
        else:
            try:
                asset_skeleton = asset.get_editor_property("skeleton")
            except Exception:
                asset_skeleton = None
    fallbacks[property_name] = {{
        "path": asset.get_path_name() if asset else "",
        "class": asset.get_class().get_name() if asset else "",
        "skeleton": asset_skeleton.get_path_name() if asset_skeleton else "",
        "length": float(asset.get_play_length()) if asset and hasattr(asset, "get_play_length") else 0.0,
    }}

RESULT = {{
    "mesh": mesh.get_path_name() if mesh else "",
    "skeleton": skeleton.get_path_name() if skeleton else "",
    "relative_location": (float(relative_location.x), float(relative_location.y), float(relative_location.z)),
    "relative_scale": (float(relative_scale.x), float(relative_scale.y), float(relative_scale.z)),
    "anim_class": anim_class.get_path_name() if anim_class else "",
    "animation_mode": animation_mode,
    "fallbacks": fallbacks,
}}
""".format(player_class=PLAYER_CLASS, expected_fallbacks=EXPECTED_FALLBACKS)
    result = parse_repr_dict(exec_python(host, port, code, timeout=60.0, request_id="verify-active-fcs-player"))

    if result.get("mesh") != EXPECTED_MESH:
        raise RuntimeError("Active player mesh is wrong: " + result.get("mesh", ""))
    if result.get("skeleton") != EXPECTED_SKELETON:
        raise RuntimeError("Active player skeleton is wrong: " + result.get("skeleton", ""))
    if result.get("anim_class"):
        raise RuntimeError("Active player still has an anim blueprint class: " + result["anim_class"])
    if abs(result["relative_location"][2] + 88.0) > 0.01:
        raise RuntimeError("Active player mesh Z offset is wrong: {}".format(result["relative_location"]))
    if tuple(result.get("relative_scale", ())) != (1.0, 1.0, 1.0):
        raise RuntimeError("Active player mesh scale is wrong: {}".format(result.get("relative_scale")))

    for property_name, expected_fragment in EXPECTED_FALLBACKS.items():
        info = result["fallbacks"].get(property_name, {})
        path = info.get("path", "")
        if expected_fragment not in path:
            raise RuntimeError("{} points at wrong asset: {}".format(property_name, path))
        if "/Characters/Jacob/" in path:
            raise RuntimeError("{} still points at old character content: {}".format(property_name, path))
        if info.get("skeleton") != EXPECTED_SKELETON:
            raise RuntimeError("{} is bound to wrong skeleton: {}".format(property_name, info.get("skeleton", "")))
        if info.get("length", 0.0) <= 0.0:
            raise RuntimeError("{} has no playable length".format(property_name))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    result = verify_active_player(args.host, args.port)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
