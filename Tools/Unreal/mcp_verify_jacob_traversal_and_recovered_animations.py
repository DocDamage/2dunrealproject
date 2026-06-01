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
    request = {
        "id": request_id or "exec_python",
        "kind": "exec_python",
        "args": {"expression": "(exec({!r}), RESULT)[1]".format(code)},
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
loaded = subsystem.load_level({level_path!r}) if subsystem else unreal.EditorLevelLibrary.load_level({level_path!r})
if not loaded:
    raise RuntimeError("Could not load level: {level_path}")
RESULT = True
""".format(level_path=LEVEL_PATH)
    exec_python(host, port, code, timeout=60.0, request_id="jacob-traversal-load-level")


def sample_player(host, port, label):
    code = """
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
mesh = player.get_component_by_class(unreal.SkeletalMeshComponent)
movement = player.get_component_by_class(unreal.CharacterMovementComponent)
inst = mesh.get_anim_instance() if mesh and hasattr(mesh, "get_anim_instance") else None
asset = inst.get_animation_asset() if inst and hasattr(inst, "get_animation_asset") else None
location = player.get_actor_location()
is_sliding_attr = getattr(player, "is_sliding", False)
is_double_jumping_attr = getattr(player, "is_double_jumping", False)
is_sliding_value = is_sliding_attr() if callable(is_sliding_attr) else bool(is_sliding_attr)
is_double_jumping_value = is_double_jumping_attr() if callable(is_double_jumping_attr) else bool(is_double_jumping_attr)
RESULT = {
    "label": %r,
    "animation": asset.get_path_name() if asset else "",
    "ability": str(player.get_current_ability_animation()),
    "is_sliding": bool(is_sliding_value),
    "is_double_jumping": bool(is_double_jumping_value),
    "is_falling": bool(movement.is_falling()) if movement else False,
    "location": (float(location.x), float(location.y), float(location.z)),
}
""" % label
    return exec_python(host, port, code, timeout=30.0, request_id="jacob-sample-" + label)


def reset_player(host, port, request_id):
    code = """
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
movement = player.get_component_by_class(unreal.CharacterMovementComponent)
if movement:
    movement.stop_movement_immediately()
    movement.set_movement_mode(unreal.MovementMode.MOVE_WALKING)
player.set_actor_location(unreal.Vector(0.0, 0.0, 57.5), False, True)
is_sliding_attr = getattr(player, "is_sliding", False)
is_sliding_value = is_sliding_attr() if callable(is_sliding_attr) else bool(is_sliding_attr)
if is_sliding_value:
    player.stop_slide()
player.stop_jump()
RESULT = True
"""
    exec_python(host, port, code, timeout=30.0, request_id=request_id)
    time.sleep(0.25)


def trigger_player_call(host, port, expression, request_id):
    code = """
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
RESULT = bool(%s)
""" % expression
    return exec_python(host, port, code, timeout=30.0, request_id=request_id)


def wait_until_animation_contains(host, port, fragment, timeout_seconds, label):
    deadline = time.monotonic() + timeout_seconds
    samples = []
    while time.monotonic() < deadline:
        sample = sample_player(host, port, label)
        samples.append(sample)
        if fragment in sample.get("animation", ""):
            return sample, samples
        time.sleep(0.05)
    return None, samples


def probe_slide(host, port):
    reset_player(host, port, "jacob-slide-reset")
    started = trigger_player_call(host, port, "player.start_slide()", "jacob-slide-start")
    immediate = sample_player(host, port, "slide-immediate")
    loop, loop_samples = wait_until_animation_contains(host, port, "Slide_Loop", 1.0, "slide-loop")
    trigger_player_call(host, port, "player.stop_slide() or True", "jacob-slide-stop")
    exit_sample = sample_player(host, port, "slide-exit")
    return {
        "started": started,
        "immediate": immediate,
        "loop": loop,
        "loop_samples": loop_samples[-5:],
        "exit": exit_sample,
    }


def probe_jump(host, port):
    reset_player(host, port, "jacob-jump-reset")
    trigger_player_call(host, port, "player.start_jump() or True", "jacob-jump-start")
    immediate = sample_player(host, port, "jump-immediate")
    loop, loop_samples = wait_until_animation_contains(host, port, "Jump_Loop", 0.7, "jump-loop")
    land, land_samples = wait_until_animation_contains(host, port, "Jump_Land", 1.8, "jump-land")
    return {
        "immediate": immediate,
        "loop": loop,
        "loop_samples": loop_samples[-5:],
        "land": land,
        "land_samples": land_samples[-5:],
    }


def probe_double_jump(host, port):
    reset_player(host, port, "jacob-double-jump-reset")
    trigger_player_call(host, port, "player.start_jump() or True", "jacob-double-first-jump")
    time.sleep(0.22)
    trigger_player_call(host, port, "player.start_jump() or True", "jacob-double-second-jump")
    immediate = sample_player(host, port, "double-jump-immediate")
    loop, loop_samples = wait_until_animation_contains(host, port, "NinjaJump_Idle_Loop", 0.7, "double-jump-loop")
    return {
        "immediate": immediate,
        "loop": loop,
        "loop_samples": loop_samples[-5:],
    }


def require_fragment(section, sample, fragment):
    animation = sample.get("animation", "")
    if fragment not in animation:
        raise RuntimeError("{} expected {} but got {}".format(section, fragment, animation or "<none>"))


def assert_results(results):
    if not results["slide"].get("started"):
        raise RuntimeError("Slide did not start")
    require_fragment("Slide start", results["slide"]["immediate"], "Slide_Start")
    if not results["slide"].get("loop"):
        raise RuntimeError("Slide loop clip was never observed; tail samples: {}".format(results["slide"]["loop_samples"]))
    require_fragment("Slide loop", results["slide"]["loop"], "Slide_Loop")
    require_fragment("Slide exit", results["slide"]["exit"], "Slide_Exit")

    require_fragment("Jump start", results["jump"]["immediate"], "Jump_Start")
    if not results["jump"].get("loop"):
        raise RuntimeError("Jump loop clip was never observed; tail samples: {}".format(results["jump"]["loop_samples"]))
    require_fragment("Jump loop", results["jump"]["loop"], "Jump_Loop")
    if not results["jump"].get("land"):
        raise RuntimeError("Jump land clip was never observed; tail samples: {}".format(results["jump"]["land_samples"]))

    require_fragment("Double-jump start", results["double_jump"]["immediate"], "NinjaJump_Start")
    if not results["double_jump"].get("loop"):
        raise RuntimeError(
            "Double-jump loop clip was never observed; tail samples: {}".format(results["double_jump"]["loop_samples"])
        )
    require_fragment("Double-jump loop", results["double_jump"]["loop"], "NinjaJump_Idle_Loop")


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

    results = {
        "slide": probe_slide(args.host, args.port),
        "jump": probe_jump(args.host, args.port),
        "double_jump": probe_double_jump(args.host, args.port),
    }
    print(json.dumps(results, indent=2, sort_keys=True))

    if not args.keep_pie_running:
        call(args.host, args.port, "pie.stop")

    assert_results(results)


if __name__ == "__main__":
    main()

