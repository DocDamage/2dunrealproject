import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
LEVEL_PATH = "/Game/NocturneSignal/Slice01/Maps/L_Slice01GameplayTest"
PLAYER_CLASS = "/Script/NocturneSignal.NocturnePlayerCharacter"
MOVE_KEY = "D"
PARALLAX_LABELS = (
    "Slice01_Sakura_Parallax_SkyClouds",
    "Slice01_Sakura_Parallax_DistantTemples",
    "Slice01_Sakura_Parallax_MidgroundGarden",
    "Slice01_Sakura_Parallax_ForegroundRuins",
)
PLAYER_MOVE_MIN_X = 300.0
PARALLAX_TRACK_TOLERANCE = 18.0
PARALLAX_DEPTH_TOLERANCE = 1.0


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
    return send_request(
        host,
        port,
        {
            "id": request_id or method,
            "kind": "call_function",
            "method": method,
            "args": args or {},
        },
        timeout=timeout,
    )


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


def ensure_stopped(host, port):
    running = call(host, port, "pie.is_running")
    if running.get("running"):
        call(host, port, "pie.stop")
        deadline = time.monotonic() + 15.0
        while time.monotonic() < deadline:
            if not call(host, port, "pie.is_running").get("running"):
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
level_path = {level_path!r}
subsystem_type = getattr(unreal, "LevelEditorSubsystem", None)
subsystem = unreal.get_editor_subsystem(subsystem_type) if subsystem_type else None
loaded = subsystem.load_level(level_path) if subsystem else unreal.EditorLevelLibrary.load_level(level_path)
RESULT = {{"loaded": bool(loaded), "level_path": level_path}}
""".format(level_path=LEVEL_PATH)
    result = exec_python(host, port, code, timeout=120.0, request_id="load-slice01-parallax-level")
    parsed = parse_repr_dict(result)
    if not parsed.get("loaded"):
        raise RuntimeError("Could not load level: " + LEVEL_PATH)


def parse_repr_dict(result):
    try:
        value = ast.literal_eval(result.get("repr", "{}"))
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError("Could not parse MCP result: {}".format(exc))
    if not isinstance(value, dict):
        raise RuntimeError("Unexpected MCP result: " + repr(value))
    return value


def sample_state(host, port):
    code = """
import unreal
labels = {labels!r}
player_class = unreal.load_class(None, {player_class!r})
editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world = editor_subsystem.get_game_world()
if not world:
    raise RuntimeError("No PIE game world")

def actor_label(actor):
    try:
        return actor.get_actor_label()
    except Exception:
        return actor.get_name()

layers = {{}}
all_actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
for actor in all_actors:
    label = actor_label(actor)
    if label in labels:
        location = actor.get_actor_location()
        layers[label] = (float(location.x), float(location.y), float(location.z))

players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE")
player_location = players[0].get_actor_location()
RESULT = {{
    "player": (float(player_location.x), float(player_location.y), float(player_location.z)),
    "layers": layers,
}}
""".format(labels=PARALLAX_LABELS, player_class=PLAYER_CLASS)
    return parse_repr_dict(exec_python(host, port, code, timeout=30.0, request_id="sample-parallax-state"))


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

    before = sample_state(args.host, args.port)
    call(args.host, args.port, "pie.simulate_key", {"key": MOVE_KEY, "action": "press"})
    time.sleep(1.25)
    call(args.host, args.port, "pie.simulate_key", {"key": MOVE_KEY, "action": "release"})
    time.sleep(0.25)
    after = sample_state(args.host, args.port)

    if not args.keep_pie_running:
        call(args.host, args.port, "pie.stop")

    player_delta_x = after["player"][0] - before["player"][0]
    result = {
        "before": before,
        "after": after,
        "player_delta_x": player_delta_x,
        "layer_deltas": {},
    }
    for label in PARALLAX_LABELS:
        if label not in before["layers"] or label not in after["layers"]:
            raise RuntimeError("Missing parallax layer in PIE: " + label)
        layer_before = before["layers"][label]
        layer_after = after["layers"][label]
        result["layer_deltas"][label] = (
            layer_after[0] - layer_before[0],
            layer_after[1] - layer_before[1],
            layer_after[2] - layer_before[2],
        )

    print(json.dumps(result, indent=2, sort_keys=True))

    if player_delta_x < PLAYER_MOVE_MIN_X:
        raise RuntimeError("Player did not move enough to stress parallax: {:.2f}".format(player_delta_x))

    for label, delta in result["layer_deltas"].items():
        if abs(delta[0] - player_delta_x) > PARALLAX_TRACK_TOLERANCE:
            raise RuntimeError(
                "{} did not track the side-view camera/player X. player_delta_x={:.2f}, layer_delta_x={:.2f}".format(
                    label,
                    player_delta_x,
                    delta[0],
                )
            )
        if abs(delta[1]) > PARALLAX_DEPTH_TOLERANCE or abs(delta[2]) > PARALLAX_DEPTH_TOLERANCE:
            raise RuntimeError("{} drifted in depth/height: {}".format(label, delta))


if __name__ == "__main__":
    main()

