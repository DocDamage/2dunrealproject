import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
LEVEL_PATH = "/Game/NocturneSignal/Slice01/Maps/L_Slice01GameplayTest"


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


def call(host, port, method, args=None, timeout=30.0, request_id=None):
    request = {
        "id": request_id or method,
        "kind": "call_function",
        "method": method,
        "args": args or {},
    }
    return send_request(host, port, request, timeout=timeout)


def exec_python(host, port, code, timeout=30.0, request_id=None):
    expression = "(exec({!r}), RESULT)[1]".format(code)
    request = {
        "id": request_id or "exec_python",
        "kind": "exec_python",
        "args": {"expression": expression},
    }
    result = send_request(host, port, request, timeout=timeout)
    try:
        return ast.literal_eval(result.get("repr", "None"))
    except (SyntaxError, ValueError):
        return result.get("repr")


def ensure_stopped(host, port):
    running = call(host, port, "pie.is_running")
    if running.get("running"):
        call(host, port, "pie.stop")
        deadline = time.monotonic() + 15.0
        while time.monotonic() < deadline:
            if not call(host, port, "pie.is_running").get("running"):
                time.sleep(1.5)
                return
            time.sleep(0.25)
        raise RuntimeError("PIE did not stop")


def wait_running(host, port):
    deadline = time.monotonic() + 30.0
    while time.monotonic() < deadline:
        if call(host, port, "pie.is_running").get("running"):
            return
        time.sleep(0.25)
    raise RuntimeError("PIE did not start")


def load_level(host, port):
    code = """
import unreal
subsystem_type = getattr(unreal, "LevelEditorSubsystem", None)
subsystem = unreal.get_editor_subsystem(subsystem_type) if subsystem_type else None
if subsystem:
    loaded = subsystem.load_level({level_path!r})
else:
    loaded = unreal.EditorLevelLibrary.load_level({level_path!r})
if not loaded:
    raise RuntimeError("Could not load level: {level_path}")
RESULT = True
""".format(level_path=LEVEL_PATH)
    exec_python(host, port, code, timeout=60.0, request_id="grabbable-load-level")


def setup_and_start_pull(host, port):
    code = """
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
anchor_class = unreal.load_class(None, "/Script/NocturneSignal.GrappleAnchor")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
anchors = unreal.GameplayStatics.get_all_actors_of_class(world, anchor_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
grabbables = []
for actor in anchors:
    should_pull = False
    if hasattr(actor, "should_pull_anchor_to_grappler"):
        should_pull = bool(actor.should_pull_anchor_to_grappler())
    if not should_pull:
        try:
            should_pull = bool(actor.get_editor_property("pull_anchor_to_grappler"))
        except Exception:
            should_pull = False
    if should_pull:
        grabbables.append(actor)
if not grabbables:
    raise RuntimeError("No grabbable GrappleAnchor in PIE world")
anchor = sorted(grabbables, key=lambda actor: abs(actor.get_actor_location().x - 360.0))[0]

player_start = unreal.Vector(0.0, 0.0, 57.5)
anchor_start = unreal.Vector(360.0, 0.0, anchor.get_actor_location().z)
player.set_actor_location(player_start, False, True)
anchor.set_actor_location(anchor_start, False, True)

movement = player.get_component_by_class(unreal.CharacterMovementComponent)
if movement:
    movement.stop_movement_immediately()

limb = player.get_vestige_limb_component()
if not limb:
    raise RuntimeError("Player has no VestigeLimbComponent")
limb.set_editor_property("max_grapple_range", 1000.0)
limb.set_editor_property("minimum_directional_dot", -0.2)
limb.set_editor_property("require_anchor_line_of_sight", False)
limb.set_preferred_grapple_direction(unreal.Vector(1.0, 0.0, 0.0))

started = bool(player.trigger_tentacle_grapple())
RESULT = {
    "started": started,
    "player_before": (player.get_actor_location().x, player.get_actor_location().y, player.get_actor_location().z),
    "anchor_before": (anchor.get_actor_location().x, anchor.get_actor_location().y, anchor.get_actor_location().z),
    "anchor_path": anchor.get_path_name(),
}
"""
    return exec_python(host, port, code, timeout=30.0, request_id="grabbable-start-pull")


def sample_pull_result(host, port, anchor_path):
    code = f"""
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
anchor = next((actor for actor in unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor) if actor.get_path_name() == {anchor_path!r}), None)
if not anchor:
    raise RuntimeError("Could not find grabbable anchor after pull: {anchor_path}")
limb = player.get_vestige_limb_component()
RESULT = {{
    "player_after": (player.get_actor_location().x, player.get_actor_location().y, player.get_actor_location().z),
    "anchor_after": (anchor.get_actor_location().x, anchor.get_actor_location().y, anchor.get_actor_location().z),
    "grapple_state": str(limb.get_grapple_state()) if limb else "<missing>",
}}
"""
    return exec_python(host, port, code, timeout=30.0, request_id="grabbable-sample-result")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--keep-pie-running", action="store_true")
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

    before = setup_and_start_pull(args.host, args.port)
    if not before.get("started"):
        raise RuntimeError("TriggerTentacleGrapple did not start on the grabbable prop")

    time.sleep(0.85)
    after = sample_pull_result(args.host, args.port, before["anchor_path"])

    player_delta_x = after["player_after"][0] - before["player_before"][0]
    anchor_delta_x = after["anchor_after"][0] - before["anchor_before"][0]
    result = {
        "before": before,
        "after": after,
        "player_delta_x": player_delta_x,
        "anchor_delta_x": anchor_delta_x,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    if not args.keep_pie_running:
        call(args.host, args.port, "pie.stop")

    if abs(player_delta_x) > 25.0:
        raise RuntimeError("Player moved too much while pulling prop: delta_x={}".format(player_delta_x))
    if anchor_delta_x >= -150.0:
        raise RuntimeError("Grabbable prop was not pulled toward the player enough: delta_x={}".format(anchor_delta_x))
    if after["anchor_after"][0] > 140.0:
        raise RuntimeError("Grabbable prop did not arrive near the player: x={}".format(after["anchor_after"][0]))


if __name__ == "__main__":
    main()

