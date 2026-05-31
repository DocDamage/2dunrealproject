import unreal


CHARACTER_ROOT = "/Game/NocturneSignal/Characters/Jacob"
SKELETON_PATH = CHARACTER_ROOT + "/SK_Jacob_Skeleton.SK_Jacob_Skeleton"
MESH_PATH = CHARACTER_ROOT + "/SK_Jacob.SK_Jacob"
ANIM_BP_NAME = "ABP_Jacob"
ANIM_BP_PATH = CHARACTER_ROOT + "/" + ANIM_BP_NAME + "." + ANIM_BP_NAME


def log(message):
    unreal.log("[NocturneJacobAnimBP] " + str(message))


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


def main():
    existing = unreal.EditorAssetLibrary.load_asset(ANIM_BP_PATH)
    if existing:
        log("Animation Blueprint already exists: " + ANIM_BP_PATH)
        unreal.EditorAssetLibrary.save_loaded_asset(existing)
        return

    skeleton = load_asset(SKELETON_PATH)
    mesh = load_asset(MESH_PATH)

    factory = unreal.AnimBlueprintFactory()
    factory.set_editor_property("target_skeleton", skeleton)
    factory.set_editor_property("preview_skeletal_mesh", mesh)
    factory.set_editor_property("parent_class", unreal.AnimInstance)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    anim_bp = asset_tools.create_asset(ANIM_BP_NAME, CHARACTER_ROOT, unreal.AnimBlueprint, factory)
    if not anim_bp:
        raise RuntimeError("Failed to create Animation Blueprint: " + ANIM_BP_PATH)

    unreal.EditorAssetLibrary.save_loaded_asset(anim_bp)
    log("Created Animation Blueprint: " + ANIM_BP_PATH)


main()
