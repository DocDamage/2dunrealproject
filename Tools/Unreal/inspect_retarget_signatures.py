import unreal


def log(message):
    unreal.log("[NocturneRetargetSignatures] " + str(message))


def show(name, member):
    obj = getattr(getattr(unreal, name), member, None)
    log(f"{name}.{member} doc={getattr(obj, '__doc__', None)}")


def main():
    checks = {
        "IKRigDefinitionFactory": ["create_new_ik_rig_asset", "create_new"],
        "IKRigController": [
            "get_controller",
            "apply_auto_generated_retarget_definition",
            "set_retarget_root",
            "add_retarget_chain",
        ],
        "IKRetargetFactory": ["create_new"],
        "IKRetargeterController": [
            "get_controller",
            "auto_map_chains",
            "set_source_chain",
            "add_retarget_op",
            "run_op_initial_setup",
        ],
        "IKRetargetBatchOperation": ["duplicate_and_retarget"],
        "AssetTools": ["create_asset"],
    }
    for cls_name, members in checks.items():
        for member in members:
            show(cls_name, member)


main()
