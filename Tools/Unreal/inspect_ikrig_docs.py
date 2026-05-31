import unreal


def log(message):
    unreal.log("[NocturneIKRigDocs] " + str(message))


def dump_class(cls_name, contains=None):
    cls = getattr(unreal, cls_name, None)
    log(f"CLASS {cls_name}")
    for name in sorted(n for n in dir(cls) if not n.startswith("_")):
        if contains and not any(token.lower() in name.lower() for token in contains):
            continue
        obj = getattr(cls, name, None)
        doc = getattr(obj, "__doc__", "")
        log(f"  {name}: {doc}")


def dump_props(asset_path):
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    log(f"ASSET {asset_path} class={asset.get_class().get_name()}")
    for prop in sorted(asset.get_editor_property_names() if hasattr(asset, "get_editor_property_names") else []):
        log(f"  prop {prop}")


def main():
    dump_class("IKRigController", ["skeletal", "mesh", "preview", "bone", "goal", "solver", "chain", "root", "hierarchy"])
    dump_class("IKRetargeterController", ["source", "target", "rig", "chain", "mesh", "op", "pose"])
    dump_class("IKRigDefinitionFactory", None)
    dump_class("IKRetargetFactory", None)


main()
