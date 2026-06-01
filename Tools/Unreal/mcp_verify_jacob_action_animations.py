import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
LEVEL_PATH = "/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobGameplayTest"


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
    exec_python(host, port, code, timeout=60.0, request_id="jacob-actions-load-level")


def run_action_probe(host, port, action_name):
    code = f"""
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
player_class = unreal.load_class(None, "/Script/NocturneSignal.NocturnePlayerCharacter")
anchor_class = unreal.load_class(None, "/Script/NocturneSignal.GrappleAnchor")
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class)
if not players:
    raise RuntimeError("No Nocturne player in PIE world")
player = players[0]
mesh = player.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh:
    raise RuntimeError("No player mesh component in PIE world")

movement = player.get_component_by_class(unreal.CharacterMovementComponent)
if movement:
    movement.stop_movement_immediately()

if {action_name!r} == "grapple":
    player.set_actor_location(unreal.Vector(0.0, 0.0, 57.5), False, True)
    for anchor in unreal.GameplayStatics.get_all_actors_of_class(world, anchor_class):
        should_pull = False
        if hasattr(anchor, "should_pull_anchor_to_grappler"):
            should_pull = bool(anchor.should_pull_anchor_to_grappler())
        if should_pull:
            anchor.set_actor_location(unreal.Vector(360.0, 0.0, anchor.get_actor_location().z), False, True)
            break
    limb = player.get_vestige_limb_component()
    limb.set_editor_property("max_grapple_range", 1000.0)
    limb.set_editor_property("minimum_directional_dot", -0.2)
    limb.set_editor_property("require_anchor_line_of_sight", False)
    limb.set_preferred_grapple_direction(unreal.Vector(1.0, 0.0, 0.0))
    started = bool(player.trigger_tentacle_grapple())
elif {action_name!r} == "attack":
    started = bool(player.trigger_tentacle_attack())
elif {action_name!r} == "consume":
    started = bool(player.trigger_tentacle_consume(False))
elif {action_name!r} == "alternate_consume":
    started = bool(player.trigger_tentacle_consume(True))
else:
    raise RuntimeError("Unknown action probe")

inst = mesh.get_anim_instance() if hasattr(mesh, "get_anim_instance") else None
asset = inst.get_animation_asset() if inst and hasattr(inst, "get_animation_asset") else None
skeletal_mesh = mesh.get_skeletal_mesh_asset() if hasattr(mesh, "get_skeletal_mesh_asset") else None
asset_bounds = skeletal_mesh.get_bounds() if skeletal_mesh and hasattr(skeletal_mesh, "get_bounds") else None
try:
    component_scale = mesh.get_editor_property("relative_scale3d")
except Exception:
    component_scale = unreal.Vector(1.0, 1.0, 1.0)
mesh_radius = (
    float(asset_bounds.sphere_radius) * max(component_scale.x, component_scale.y, component_scale.z)
    if asset_bounds
    else 0.0
)
RESULT = {{
    "started": started,
    "action": {action_name!r},
    "animation": asset.get_path_name() if asset else "",
    "mesh": skeletal_mesh.get_path_name() if skeletal_mesh else "",
    "mesh_visible": bool(mesh.is_visible()),
    "mesh_hidden_in_game": bool(mesh.get_editor_property("hidden_in_game")),
    "player_location": (player.get_actor_location().x, player.get_actor_location().y, player.get_actor_location().z),
    "mesh_radius": mesh_radius,
}}
"""
    return exec_python(host, port, code, timeout=30.0, request_id="jacob-action-" + action_name)


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

    results = {}
    for action_name in ("attack", "consume", "alternate_consume", "grapple"):
        results[action_name] = run_action_probe(args.host, args.port, action_name)
        time.sleep(0.65)

    print(json.dumps(results, indent=2, sort_keys=True))

    if not args.keep_pie_running:
        call(args.host, args.port, "pie.stop")

    expected = {
        "attack": "JAC_Paired_ForceChoke_Att",
        "consume": "JAC_Paired_SneakNeckBreak_Att",
        "alternate_consume": "JAC_Paired_Knife_Stealth_KidneyAndNeck_Att",
        "grapple": "JAC_Paired_ForceChoke",
    }
    for action_name, asset_fragment in expected.items():
        result = results[action_name]
        if not result.get("started"):
            raise RuntimeError("{} did not start".format(action_name))
        if asset_fragment not in result.get("animation", ""):
            raise RuntimeError("{} played wrong animation: {}".format(action_name, result.get("animation") or "<none>"))
        if not result.get("mesh", "").endswith("SK_Jacob.SK_Jacob"):
            raise RuntimeError("{} used wrong mesh: {}".format(action_name, result.get("mesh") or "<none>"))
        if not result.get("mesh_visible") or result.get("mesh_hidden_in_game"):
            raise RuntimeError("{} mesh is hidden".format(action_name))
        if result.get("mesh_radius", 0.0) < 50.0:
            raise RuntimeError("{} mesh bounds look collapsed: {}".format(action_name, result.get("mesh_radius")))


if __name__ == "__main__":
    main()
