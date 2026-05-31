import os
import runpy

import unreal


SCRIPT_DIR = os.path.dirname(__file__)
NEW_RETARGET_SOURCES = ",".join(
    [
        "ActorCoreWalk",
        "ActorCoreTactical",
        "GameAnimationSample",
        "ParagonMannyCurated",
        "FightAnimationMocapPack",
        "VefectsVexa",
        "FreeAnimationsPack",
        "RogueCharacter",
    ]
)


def log(message):
    unreal.log("[NocturneNewJacobFabAssets] " + str(message))


def run_script(script_name):
    path = os.path.join(SCRIPT_DIR, script_name)
    log("Running " + path)
    runpy.run_path(path, run_name="__main__")


def main():
    run_script("import_actorcore_animation_libraries.py")
    run_script("import_fab_jacob_candidate_animations.py")
    run_script("import_robotic_tentacle_hands.py")

    previous_sources = os.environ.get("NOCTURNE_RETARGET_SOURCES")
    os.environ["NOCTURNE_RETARGET_SOURCES"] = NEW_RETARGET_SOURCES
    try:
        run_script("retarget_animations_to_jacob.py")
    finally:
        if previous_sources is None:
            os.environ.pop("NOCTURNE_RETARGET_SOURCES", None)
        else:
            os.environ["NOCTURNE_RETARGET_SOURCES"] = previous_sources

    try:
        command_line = unreal.SystemLibrary.get_command_line()
    except Exception:
        command_line = ""
    if "QuitAfterNewJacobFabAssetsImport" in command_line:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise
