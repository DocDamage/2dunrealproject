# Female Cyber Stalker Intake

**Source:** `D:/VaultCache/FabLibrary/Female_Cyber_Stalker-7307bdc1/fbx/female_cyber_stalker_extracted`  
**Fab listing UID:** `7307bdc1-d973-4787-8308-3d36df365f00`  
**Seller:** `SolarSnail`  
**Intake date:** 2026-06-01

## Decision

Female Cyber Stalker is the active Slice01 playable pawn as of 2026-06-01.

Use only the low-poly rigged files staged under:

```text
SourceArt/FemaleCyberStalker/
```

Do not import the high-poly unrigged texture variant for gameplay.

## Inspection Summary

| Item | Result |
|---|---:|
| Gameplay mesh | `Character_output.fbx` |
| Triangles | 23,925 |
| Vertices | 12,114 |
| Armature | 24-bone humanoid |
| Height | ~1.8 m |
| Bundled animation clips | Walk, Run |
| Texture maps staged | Metallic, Normal, Roughness |

## Fit

The character is a stronger tonal fit than the current temporary harness: faceless, armored, cybernetic, and readable as an infiltrator/host for the Signal/Vestige fantasy.

## Risks

| Risk | Mitigation |
|---|---|
| AI-generated asset imperfections | Inspect deformation in PIE before final commitment |
| Only walk/run provided | Retargeted traversal and tentacle-action smoke-test clips now cover the Slice01 verbs |
| Simple 24-bone rig | Keep PIE visual inspection on the remaining polish checklist |
| High-poly unrigged variant exists | Keep excluded from the gameplay import |
| Recovered combat montages were tied to the old player skeleton | Disabled on the active pawn until a new Cyber Stalker combat set is chosen |

## Planned Unreal Paths

```text
/Game/NocturneSignal/Characters/FemaleCyberStalker/SK_FemaleCyberStalker
/Game/NocturneSignal/Characters/FemaleCyberStalker/SK_FemaleCyberStalker_Skeleton
/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Walk
/Game/NocturneSignal/Characters/FemaleCyberStalker/Animations/FCS_Run
/Game/NocturneSignal/Characters/FemaleCyberStalker/Textures/
/Game/NocturneSignal/Characters/FemaleCyberStalker/RetargetedAnimations/
/Game/NocturneSignal/Slice01/Maps/L_Slice01GameplayTest
```

## Verification

Passed on 2026-06-01:

```text
Tools/Unreal/import_female_cyber_stalker.py
Tools/Unreal/mcp_verify_female_cyber_stalker_import.py
Tools/Unreal/mcp_verify_female_cyber_stalker_retargeted_subset.py
Tools/Unreal/mcp_verify_active_player_female_cyber_stalker.py
Tools/Unreal/validate_slice01_level_and_movement.py
Tools/Unreal/mcp_verify_jacob_pie_movement.py
Tools/Unreal/mcp_verify_jacob_traversal_and_recovered_animations.py
Tools/Unreal/mcp_verify_grabbable_prop_pull.py
Tools/Unreal/mcp_verify_slice01_parallax_stability.py
Tools/Unreal/mcp_verify_tentacle_vfx_runtime.py
```

Key verified results:

| Check | Result |
|---|---|
| Active pawn mesh | `/Game/NocturneSignal/Characters/FemaleCyberStalker/SK_FemaleCyberStalker` |
| Active pawn animation mode | Single-node fallback, no old anim blueprint |
| Grounding | Player actor at `Z=57.5`, capsule half-height `88`, mesh offset `Z=-88` |
| PIE movement | Player moved `+525.9 X`, idle `FCS_MM_Idle`, run `FCS_Run` |
| Traversal | Slide, jump, double-jump all observed Cyber Stalker clips |
| Grabbable prop | Prop moved from `X=360` to `X=95`; player stayed at `X=0` |
| Parallax | Layers tracked player/camera X with `0` Y/Z drift |
| Tentacle VFX | Vefects beam/impact visible for attack, consume, alternate consume, grapple; no `BP_Goo` spawned |
