import argparse
import ast
import json
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 30020

MESH_PATH = "/Game/NocturneSignal/Characters/FemaleCyberStalker/SK_FemaleCyberStalker.SK_FemaleCyberStalker"
SKELETON_PATH = (
    "/Game/NocturneSignal/Characters/FemaleCyberStalker/"
    "SK_FemaleCyberStalker_Skeleton.SK_FemaleCyberStalker_Skeleton"
)
ANIMATION_PATHS = {
    "walk": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Walk.FCS_Walk",
    "run": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Run.FCS_Run",
}
TEXTURE_PATHS = {
    "metallic": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Textures/texture_0_metallic.texture_0_metallic",
    "normal": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Textures/texture_0_normal.texture_0_normal",
    "roughness": "/Game/NocturneSignal/Characters/FemaleCyberStalker/Textures/texture_0_roughness.texture_0_roughness",
}
EXPECTED_BONES = {
    "Hips",
    "Spine",
    "Spine01",
    "Spine02",
    "Head",
    "LeftArm",
    "LeftForeArm",
    "LeftHand",
    "RightArm",
    "RightForeArm",
    "RightHand",
    "LeftLeg",
    "LeftFoot",
    "RightLeg",
    "RightFoot",
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


def verify_candidate(host, port):
    code = """
import unreal

mesh_path = {mesh_path!r}
skeleton_path = {skeleton_path!r}
animation_paths = {animation_paths!r}
texture_paths = {texture_paths!r}

def load(path):
    return unreal.EditorAssetLibrary.load_asset(path)

mesh = load(mesh_path)
skeleton = load(skeleton_path)
if not mesh:
    raise RuntimeError("Missing Female Cyber Stalker mesh: " + mesh_path)
if not skeleton:
    raise RuntimeError("Missing Female Cyber Stalker skeleton: " + skeleton_path)

mesh_skeleton = mesh.get_editor_property("skeleton")
bone_names = []
try:
    bone_names = [str(name) for name in skeleton.get_reference_pose().get_bone_names()]
except Exception:
    try:
        bone_names = [str(name) for name in skeleton.get_reference_skeleton().get_raw_bone_names()]
    except Exception:
        bone_names = []

animations = {{}}
for label, path in animation_paths.items():
    anim = load(path)
    if not anim:
        raise RuntimeError("Missing Female Cyber Stalker animation: " + path)
    anim_skeleton = anim.get_editor_property("skeleton")
    try:
        length = float(anim.get_play_length())
    except Exception:
        try:
            length = float(anim.get_editor_property("sequence_length"))
        except Exception:
            length = 0.0
    animations[label] = {{
        "path": path,
        "class": anim.get_class().get_name(),
        "skeleton": anim_skeleton.get_path_name() if anim_skeleton else "",
        "length": length,
    }}

textures = {{}}
for label, path in texture_paths.items():
    texture = load(path)
    if not texture:
        raise RuntimeError("Missing Female Cyber Stalker texture: " + path)
    textures[label] = {{
        "path": path,
        "class": texture.get_class().get_name(),
    }}

RESULT = {{
    "mesh": {{
        "path": mesh_path,
        "class": mesh.get_class().get_name(),
        "skeleton": mesh_skeleton.get_path_name() if mesh_skeleton else "",
    }},
    "skeleton": {{
        "path": skeleton_path,
        "class": skeleton.get_class().get_name(),
        "bone_count": len(bone_names),
        "bones": bone_names,
    }},
    "animations": animations,
    "textures": textures,
}}
""".format(
        mesh_path=MESH_PATH,
        skeleton_path=SKELETON_PATH,
        animation_paths=ANIMATION_PATHS,
        texture_paths=TEXTURE_PATHS,
    )
    result = parse_repr_dict(exec_python(host, port, code, timeout=60.0, request_id="verify-female-cyber-stalker"))

    mesh_skeleton = result.get("mesh", {}).get("skeleton", "")
    if "SK_FemaleCyberStalker_Skeleton" not in mesh_skeleton:
        raise RuntimeError("Female Cyber Stalker mesh is bound to the wrong skeleton: " + mesh_skeleton)

    bones = set(result.get("skeleton", {}).get("bones", []))
    if len(bones) < 20:
        raise RuntimeError("Female Cyber Stalker skeleton has too few bones: {}".format(len(bones)))
    missing_bones = sorted(EXPECTED_BONES - bones)
    if missing_bones:
        raise RuntimeError("Female Cyber Stalker skeleton is missing expected humanoid bones: " + ", ".join(missing_bones))

    for label, animation in result.get("animations", {}).items():
        if "SK_FemaleCyberStalker_Skeleton" not in animation.get("skeleton", ""):
            raise RuntimeError("{} animation is bound to the wrong skeleton: {}".format(label, animation.get("skeleton")))
        if animation.get("length", 0.0) <= 0.0:
            raise RuntimeError("{} animation has no playable length".format(label))

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    result = verify_candidate(args.host, args.port)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
