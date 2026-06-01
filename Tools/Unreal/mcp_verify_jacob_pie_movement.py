import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
PLAYER_CLASS = "/Script/NocturneSignal.NocturnePlayerCharacter"
MOVE_KEY = "D"
IDLE_ANIMATION_SUFFIXES = ("FCS_MM_Idle.FCS_MM_Idle",)
RUN_ANIMATION_SUFFIXES = ("FCS_Run.FCS_Run",)
WALK_ANIMATION_SUFFIXES = ("FCS_Walk.FCS_Walk",)


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


def exec_python(host, port, expression, timeout=30.0, request_id=None):
    request = {
        "id": request_id or "exec_python",
        "kind": "exec_python",
        "args": {"expression": expression},
    }
    return send_request(host, port, request, timeout=timeout)


def ensure_stopped(host, port):
    running = call(host, port, "pie.is_running")
    if running.get("running"):
        call(host, port, "pie.stop")
        deadline = time.monotonic() + 15.0
        while time.monotonic() < deadline:
            state = call(host, port, "pie.is_running")
            if not state.get("running"):
                return
            time.sleep(0.25)
        raise RuntimeError("PIE did not stop")


def wait_running(host, port):
    deadline = time.monotonic() + 30.0
    while time.monotonic() < deadline:
        state = call(host, port, "pie.is_running")
        if state.get("running"):
            return
        time.sleep(0.25)
    raise RuntimeError("PIE did not start")


def get_player_actor(host, port):
    world = call(host, port, "pie.dump_world_state", {"class_filter": PLAYER_CLASS})
    actors = world.get("actors") or []
    if not actors:
        raise RuntimeError("No Nocturne player actor found in PIE world")
    actor = actors[0]
    return actor, actor["transform"]


def get_player_current_animation(host, port, actor_path):
    expression = (
        "(lambda unreal, actor_path, class_path: "
        "(lambda world, player_class: "
        "(lambda actors: "
        "(lambda actor: "
        "(lambda mesh: "
        "(lambda inst: "
        "(lambda asset: asset.get_path_name() if asset else '')"
        "((inst.get_animation_asset() if hasattr(inst, 'get_animation_asset') else None) if inst else None)"
        ")"
        "(mesh.get_anim_instance() if mesh else None)"
        ")"
        "(actor.get_component_by_class(unreal.SkeletalMeshComponent) if actor else None)"
        ")"
        "(next((a for a in actors if a.get_path_name() == actor_path), actors[0] if actors else None))"
        ")"
        "(unreal.GameplayStatics.get_all_actors_of_class(world, player_class) if world and player_class else [])"
        ")"
        "(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(), unreal.load_class(None, class_path))"
        ")(__import__('unreal'), {}, {})"
    ).format(repr(actor_path), repr(PLAYER_CLASS))
    result = exec_python(
        host,
        port,
        expression,
        request_id="player-current-animation",
    )
    try:
        value = ast.literal_eval(result.get("repr", "''"))
    except (SyntaxError, ValueError):
        value = result.get("repr", "")
    return value if isinstance(value, str) else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--keep-pie-running", action="store_true")
    args = parser.parse_args()

    ensure_stopped(args.host, args.port)
    call(
        args.host,
        args.port,
        "pie.start",
        {"mode": "selected_viewport", "viewport_size": [1280, 720], "player_count": 1},
    )
    wait_running(args.host, args.port)
    time.sleep(1.0)

    actor, before = get_player_actor(args.host, args.port)
    idle_anim = get_player_current_animation(args.host, args.port, actor["actor_path"])
    call(args.host, args.port, "pie.simulate_key", {"key": MOVE_KEY, "action": "press"})
    time.sleep(1.25)
    run_anim = get_player_current_animation(args.host, args.port, actor["actor_path"])
    call(args.host, args.port, "pie.simulate_key", {"key": MOVE_KEY, "action": "release"})
    time.sleep(0.25)
    _, after = get_player_actor(args.host, args.port)

    delta_x = after["loc_x"] - before["loc_x"]
    result = {
        "actor_path": actor["actor_path"],
        "before": before,
        "after": after,
        "delta_x": delta_x,
        "idle_anim_to_play": idle_anim,
        "run_anim_to_play": run_anim,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    if not args.keep_pie_running:
        call(args.host, args.port, "pie.stop")

    if delta_x <= 10.0:
        raise RuntimeError("Player did not move far enough on X after holding {}: delta_x={}".format(MOVE_KEY, delta_x))
    if not idle_anim.endswith(IDLE_ANIMATION_SUFFIXES):
        raise RuntimeError("Player idle animation was not bound in PIE: {}".format(idle_anim or "<none>"))
    if not (run_anim.endswith(RUN_ANIMATION_SUFFIXES) or run_anim.endswith(WALK_ANIMATION_SUFFIXES)):
        raise RuntimeError("Player locomotion animation was not bound after holding {}: {}".format(MOVE_KEY, run_anim or "<none>"))


if __name__ == "__main__":
    main()
