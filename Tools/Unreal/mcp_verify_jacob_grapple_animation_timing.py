import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
LEVEL_PATH = "/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobGameplayTest"


def send_request(host, port, request, timeout=30.0):
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall((json.dumps(request, separators=(",", ":")) + "\n").encode("utf-8"))
        data = bytearray()
        deadline = time.monotonic() + timeout
        while b"\n" not in data:
            if time.monotonic() > deadline:
                raise TimeoutError(request.get("method") or request.get("kind") or "mcp_request")
            data.extend(sock.recv(65536))
    response = json.loads(bytes(data).split(b"\n", 1)[0].decode("utf-8"))
    if response.get("ok") is not True:
        raise RuntimeError("{} failed: {}".format(request.get("method") or request.get("kind"), response.get("error")))
    return response["result"]


def call(host, port, method, args=None, timeout=30.0):
    return send_request(
        host,
        port,
        {"id": method, "kind": "call_function", "method": method, "args": args or {}},
        timeout=timeout,
    )


def exec_python(host, port, code, timeout=30.0, request_id="exec_python"):
    request = {
        "id": request_id,
        "kind": "exec_python",
        "args": {"expression": "(exec({!r}), RESULT)[1]".format(code)},
    }
    result = send_request(host, port, request, timeout=timeout)
    try:
        return ast.literal_eval(result.get("repr", "None"))
    except (SyntaxError, ValueError):
        return result.get("repr")


def ensure_stopped(host, port):
    if call(host, port, "pie.is_running").get("running"):
        call(host, port, "pie.stop")
        time.sleep(1.5)


def load_level(host, port):
    code = """
import unreal
subsystem_type = getattr(unreal, "LevelEditorSubsystem", None)
subsystem = unreal.get_editor_subsystem(subsystem_type) if subsystem_type else None
loaded = subsystem.load_level({level_path!r}) if subsystem else unreal.EditorLevelLibrary.load_level({level_path!r})
if not loaded:
    raise RuntimeError("Could not load level: {level_path}")
RESULT = True
""".format(level_path=LEVEL_PATH)
    exec_python(host, port, code, timeout=60.0, request_id="grapple-timing-load-level")


def wait_running(host, port):
    deadline = time.monotonic() + 30.0
    while time.monotonic() < deadline:
        if call(host, port, "pie.is_running").get("running"):
            return
        time.sleep(0.25)
    raise RuntimeError("PIE did not start")


def trigger_and_sample(host, port):
    code = """
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
anchor_class = unreal.load_class(None, "/Script/NocturneSignal.GrappleAnchor")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
player.set_actor_location(unreal.Vector(0.0, 0.0, 57.5), False, True)
limb = player.get_vestige_limb_component()
limb.set_editor_property("max_grapple_range", 1000.0)
limb.set_editor_property("pull_speed", 300.0)
limb.set_editor_property("pull_acceleration", 1000.0)
limb.set_editor_property("minimum_directional_dot", -0.2)
limb.set_editor_property("require_anchor_line_of_sight", False)
limb.set_preferred_grapple_direction(unreal.Vector(1.0, 0.0, 0.0))
selected_static_anchor = None
for anchor in unreal.GameplayStatics.get_all_actors_of_class(world, anchor_class):
    if bool(anchor.should_pull_anchor_to_grappler()):
        anchor.set_actor_location(unreal.Vector(-5000.0, 0.0, -5000.0), False, True)
        continue
    if not selected_static_anchor:
        selected_static_anchor = anchor
        selected_static_anchor.set_actor_location(unreal.Vector(470.0, 0.0, 330.0), False, True)
if not selected_static_anchor:
    raise RuntimeError("No static grapple anchor available")
started = bool(player.trigger_tentacle_grapple())
mesh = player.get_component_by_class(unreal.SkeletalMeshComponent)
inst = mesh.get_anim_instance() if mesh and hasattr(mesh, "get_anim_instance") else None
asset = inst.get_animation_asset() if inst and hasattr(inst, "get_animation_asset") else None
RESULT = {
    "started": started,
    "animation": asset.get_path_name() if asset else "",
    "grapple_state": str(limb.get_grapple_state()),
}
"""
    return exec_python(host, port, code, timeout=30.0, request_id="grapple-timing-trigger")


def sample_animation(host, port):
    code = """
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
player = players[0]
mesh = player.get_component_by_class(unreal.SkeletalMeshComponent)
inst = mesh.get_anim_instance() if mesh and hasattr(mesh, "get_anim_instance") else None
asset = inst.get_animation_asset() if inst and hasattr(inst, "get_animation_asset") else None
limb = player.get_vestige_limb_component()
RESULT = {
    "animation": asset.get_path_name() if asset else "",
    "grapple_state": str(limb.get_grapple_state()),
}
"""
    return exec_python(host, port, code, timeout=30.0, request_id="grapple-timing-sample")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    ensure_stopped(args.host, args.port)
    load_level(args.host, args.port)
    call(
        args.host,
        args.port,
        "pie.start",
        {"mode": "selected_viewport", "viewport_size": [1280, 720], "player_count": 1},
    )
    wait_running(args.host, args.port)
    time.sleep(1.0)

    immediate = trigger_and_sample(args.host, args.port)
    time.sleep(0.7)
    after_extend = sample_animation(args.host, args.port)
    result = {"immediate": immediate, "after_extend": after_extend}
    print(json.dumps(result, indent=2, sort_keys=True))

    call(args.host, args.port, "pie.stop")

    if not immediate.get("started"):
        raise RuntimeError("Grapple did not start")
    if "JAC_Paired_ForceChoke_Start_Att" not in immediate.get("animation", ""):
        raise RuntimeError("Grapple did not expose start clip first: {}".format(immediate.get("animation")))
    if "JAC_Paired_ForceChoke_Loop_Att" not in after_extend.get("animation", ""):
        raise RuntimeError("Grapple did not advance to loop clip: {}".format(after_extend.get("animation")))


if __name__ == "__main__":
    main()
