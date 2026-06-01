import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020
LEVEL_PATH = "/Game/NocturneSignal/Slice01/Maps/L_Slice01GameplayTest"
PLAYER_CLASS = "/Script/NocturneSignal.NocturnePlayerCharacter"
EXPECTED_PACKAGE_BEAM_MESH = "Vefects/Tentacles_VFX/VFX/Goo/SM/SM_VFX_Arm"
EXPECTED_PACKAGE_BEAM_MATERIAL = "Vefects/Tentacles_VFX/VFX/Goo/Materials/MI_VFX_Goo_Arm"
EXPECTED_PACKAGE_IMPACT_MESH = "Vefects/Tentacles_VFX/VFX/Goo/SM/SM_VFX_Smooth_Sphere_01"
EXPECTED_PACKAGE_IMPACT_MATERIAL = "Vefects/Tentacles_VFX/VFX/Goo/Materials/MI_VFX_Goo"
EXPECTED_PACKAGE_GOO_ACTOR = "Vefects/Tentacles_VFX/VFX/Goo/BP/BP_Goo"


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


def parse_repr_dict(result):
    try:
        value = ast.literal_eval(result.get("repr", "{}"))
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError("Could not parse MCP result: {}".format(exc))
    if not isinstance(value, dict):
        raise RuntimeError("Unexpected MCP result: " + repr(value))
    return value


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
    result = parse_repr_dict(exec_python(host, port, code, timeout=120.0, request_id="load-tentacle-vfx-level"))
    if not result.get("loaded"):
        raise RuntimeError("Could not load level: " + LEVEL_PATH)


def trigger_grapple_and_sample(host, port):
    code = """
import unreal
player_class = unreal.load_class(None, {player_class!r})
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class) if world and player_class else []
if not players:
    raise RuntimeError("No Nocturne player found in PIE")
player = players[0]
limb = player.get_component_by_class(unreal.VestigeLimbComponent)
if limb:
    limb.set_editor_property("minimum_directional_dot", -0.2)
    limb.set_editor_property("require_anchor_line_of_sight", False)
    limb.set_preferred_grapple_direction(unreal.Vector(1.0, 0.0, 0.0))
started = bool(player.trigger_tentacle_grapple())
RESULT = {{"started": started}}
""".format(player_class=PLAYER_CLASS)
    result = parse_repr_dict(exec_python(host, port, code, timeout=30.0, request_id="trigger-tentacle-vfx-grapple"))
    if not result.get("started"):
        raise RuntimeError("Tentacle grapple did not start for VFX verification")
    time.sleep(0.25)
    return sample_vfx_state(host, port)


def trigger_action_and_sample(host, port, action_name):
    if action_name == "attack":
        action_expression = "player.trigger_tentacle_attack()"
    elif action_name == "consume":
        action_expression = "player.trigger_tentacle_consume(False)"
    elif action_name == "alternate_consume":
        action_expression = "player.trigger_tentacle_consume(True)"
    else:
        raise RuntimeError("Unknown tentacle VFX action: " + action_name)

    code = """
import unreal
player_class = unreal.load_class(None, {player_class!r})
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class) if world and player_class else []
if not players:
    raise RuntimeError("No Nocturne player found in PIE")
player = players[0]
started = bool({action_expression})
RESULT = {{"started": started}}
""".format(player_class=PLAYER_CLASS, action_expression=action_expression)
    result = parse_repr_dict(exec_python(host, port, code, timeout=30.0, request_id="trigger-tentacle-vfx-" + action_name))
    if not result.get("started"):
        raise RuntimeError("Tentacle {} did not start for VFX verification".format(action_name))
    time.sleep(0.08)
    return sample_vfx_state(host, port)


def sample_vfx_state(host, port):
    code = """
import math
import unreal
player_class = unreal.load_class(None, {player_class!r})
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
players = unreal.GameplayStatics.get_all_actors_of_class(world, player_class) if world and player_class else []
if not players:
    raise RuntimeError("No Nocturne player found in PIE")
player = players[0]
adapter = player.get_component_by_class(unreal.VestigeTentacleVisualAdapter)
if not adapter:
    raise RuntimeError("No VestigeTentacleVisualAdapter on player")

def component_info(component):
    if not component:
        return {{}}
    if hasattr(component, "get_component_location"):
        location = component.get_component_location()
    else:
        location = component.get_world_location()
    if hasattr(component, "get_component_scale"):
        scale = component.get_component_scale()
    else:
        scale = component.get_world_scale()
    info = {{
        "name": component.get_name(),
        "class": component.get_class().get_name(),
        "visible": bool(component.is_visible()),
        "hidden_in_game": bool(component.get_editor_property("hidden_in_game")),
        "location": (float(location.x), float(location.y), float(location.z)),
        "scale": (float(scale.x), float(scale.y), float(scale.z)),
    }}
    if hasattr(component, "get_static_mesh"):
        mesh = component.get_static_mesh()
        info["mesh"] = mesh.get_path_name() if mesh else ""
    elif component.get_class().get_name() == "StaticMeshComponent":
        try:
            mesh = component.get_editor_property("static_mesh")
            info["mesh"] = mesh.get_path_name() if mesh else ""
        except Exception:
            info["mesh"] = ""
    if hasattr(component, "get_skeletal_mesh_asset"):
        mesh = component.get_skeletal_mesh_asset()
        info["mesh"] = mesh.get_path_name() if mesh else ""
    try:
        material = component.get_material(0)
        info["material"] = material.get_path_name() if material else ""
    except Exception:
        pass
    return info

root = adapter.get_tentacle_visual_root()
skeletal = adapter.get_tentacle_skeletal_mesh_component()
fallback_beam = None
impact = None
for component in player.get_components_by_class(unreal.StaticMeshComponent):
    if component.get_name() == "VestigeTentacleFallbackBeam":
        fallback_beam = component
    elif component.get_name() == "VestigeTentacleImpact":
        impact = component
        break

goo_actors = []
for actor in unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor):
    class_path = actor.get_class().get_path_name()
    if "BP_Goo" in class_path:
        location = actor.get_actor_location()
        try:
            actor_hidden = bool(actor.is_hidden())
        except Exception:
            try:
                actor_hidden = bool(actor.get_editor_property("hidden"))
            except Exception:
                actor_hidden = False
        primitive_visible = any(
            comp.is_visible() and not comp.get_editor_property("hidden_in_game")
            for comp in actor.get_components_by_class(unreal.PrimitiveComponent)
        )
        goo_actors.append({{
            "class": class_path,
            "hidden": actor_hidden,
            "location": (float(location.x), float(location.y), float(location.z)),
            "primitive_visible": bool(primitive_visible),
        }})

RESULT = {{
    "player_visual_visible": bool(player.is_tentacle_visual_visible()),
    "root": component_info(root),
    "skeletal": component_info(skeletal),
    "fallback_beam": component_info(fallback_beam),
    "impact": component_info(impact),
    "goo_actors": goo_actors,
}}
""".format(player_class=PLAYER_CLASS)
    return parse_repr_dict(exec_python(host, port, code, timeout=30.0, request_id="sample-tentacle-vfx-state"))


def assert_vfx_state(label, result):
    if not result.get("player_visual_visible"):
        raise RuntimeError("{} tentacle visual root was not visible".format(label))

    beam = result.get("fallback_beam") or {}
    if not beam.get("visible") or beam.get("hidden_in_game"):
        raise RuntimeError("{} tentacle beam was not visible".format(label))
    if EXPECTED_PACKAGE_BEAM_MESH not in beam.get("mesh", ""):
        raise RuntimeError("{} tentacle beam is not using the Vefects arm mesh: {}".format(label, beam.get("mesh") or "<none>"))
    if EXPECTED_PACKAGE_BEAM_MATERIAL not in beam.get("material", ""):
        raise RuntimeError(
            "{} tentacle beam is not using the Vefects goo arm material: {}".format(label, beam.get("material") or "<none>")
        )
    if max(beam.get("scale", (0.0, 0.0, 0.0))) <= 0.05:
        raise RuntimeError("{} tentacle beam scale is too small to be readable: {}".format(label, beam.get("scale")))

    impact = result.get("impact") or {}
    if not impact.get("visible") or impact.get("hidden_in_game"):
        raise RuntimeError("{} tentacle impact was not visible".format(label))
    if EXPECTED_PACKAGE_IMPACT_MESH not in impact.get("mesh", ""):
        raise RuntimeError("{} tentacle impact is not using the Vefects goo mesh: {}".format(label, impact.get("mesh") or "<none>"))
    if EXPECTED_PACKAGE_IMPACT_MATERIAL not in impact.get("material", ""):
        raise RuntimeError(
            "{} tentacle impact is not using a Vefects goo material: {}".format(label, impact.get("material") or "<none>")
        )

    goo_actors = result.get("goo_actors") or []
    if any(EXPECTED_PACKAGE_GOO_ACTOR in actor.get("class", "") and not actor.get("hidden") for actor in goo_actors):
        raise RuntimeError("{} spawned noisy BP_Goo instead of the controlled impact component".format(label))


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
        "attack": trigger_action_and_sample(args.host, args.port, "attack"),
        "consume": trigger_action_and_sample(args.host, args.port, "consume"),
        "alternate_consume": trigger_action_and_sample(args.host, args.port, "alternate_consume"),
        "grapple": trigger_grapple_and_sample(args.host, args.port),
    }
    print(json.dumps(results, indent=2, sort_keys=True))

    if not args.keep_pie_running:
        call(args.host, args.port, "pie.stop")

    for label, result in results.items():
        assert_vfx_state(label, result)


if __name__ == "__main__":
    main()
