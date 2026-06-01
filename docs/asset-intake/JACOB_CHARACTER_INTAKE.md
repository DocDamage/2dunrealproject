# Jacob Character Intake

**Source path:** `F:\Nocturne Signal\assets\Jacob`
**Project source-art path:** `SourceArt/Jacob`
**Unreal destination:** `/Game/NocturneSignal/Characters/Jacob`
**Imported:** 2026-05-30

---

## Intake Decision

Jacob is usable as the temporary player character/reference character.

| Check | Result |
|---|---|
| Source format | `.blend`, `.fbx`, `.png`, `.txt` |
| License | Creative Commons Attribution 4.0 |
| Creator | jupifox |
| Source size | ~5.6 MB before generated clean FBX |
| Commit policy | GitHub-safe; no Git LFS needed |
| Production status | Temporary/reference character until the Nocturne Signal player identity is locked |

Attribution must remain with the project:

```text
Jacob - Game Ready OC v1.00
Created by jupifox
https://sketchfab.com/jupifox3
https://jupifox.itch.io/
License: Creative Commons Attribution 4.0
https://creativecommons.org/licenses/by/4.0/
```

---

## Source Prep

The original FBX included demo scene objects in addition to the character. A cleaned FBX was generated at:

```text
SourceArt/Jacob/Jacob_NocturneCharacterOnly.fbx
```

The cleaned FBX contains:

| Asset | Result |
|---|---:|
| Armatures | 1 |
| Bones | 162 |
| Character/outfit/claymore meshes | 10 |
| Imported animation takes | 2 |

Animation takes:

| Animation | Frames |
|---|---:|
| `Jacob_Idle` | 1-209 |
| `Jacob_ReadySword` | 1-125 |

Excluded from the cleaned FBX:

```text
Cube
Light
Camera
Rocks
Ground
Grass
```

---

## Unreal Import

Imported assets:

| Unreal Asset | Type |
|---|---|
| `/Game/NocturneSignal/Characters/Jacob/SK_Jacob` | Skeletal Mesh |
| `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` | Skeleton |
| `/Game/NocturneSignal/Characters/Jacob/SK_JacobArmature_Jacob_Idle` | Anim Sequence |
| `/Game/NocturneSignal/Characters/Jacob/SK_JacobArmature_Jacob_ReadySword` | Anim Sequence |
| `/Game/NocturneSignal/Characters/Jacob/Jacob_Body` | Material instance |
| `/Game/NocturneSignal/Characters/Jacob/Jacob_PropsAtlas` | Material instance |
| `/Game/NocturneSignal/Characters/Jacob/Outline` | Material instance |
| `/Game/NocturneSignal/Characters/Jacob/Textures/T_JacobColor` | Texture |
| `/Game/NocturneSignal/Characters/Jacob/Textures/T_PropsAtlas` | Texture |

Repeatable import script:

```text
Tools/Unreal/import_jacob.py
```

Known import warning:

- Unreal reported missing FBX smoothing groups on the low-poly meshes. This is acceptable for temporary use, but should be corrected if Jacob remains beyond placeholder/reference status.

---

## Animation Retargeting

Retargeted on 2026-05-30 using:

```text
Tools/Unreal/retarget_animations_to_jacob.py
```

Retarget source:

```text
/Game/RamsterZ_FreeAnims_Volume1/AnimationSequence
```

Retarget destination:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RamsterZ
```

Result:

| Asset Set | Count | Skeleton |
|---|---:|---|
| RamsterZ retargeted `JAC_*` animation sequences | 44 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| MCO TC Sword retargeted `JAC_*` animation sequences | 4 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Motifect Sword retargeted `JAC_*` animation sequences | 4 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Motifect Martial Arts retargeted `JAC_*` animation sequences | 40 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Realistic Combat Moves retargeted `JAC_*` animation sequences | 10 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Universal Animation Library 1 retargeted `JAC_*` animation sequences | 45 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Universal Animation Library 2 retargeted `JAC_*` animation sequences | 43 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Advanced Locomotion Mechanics UE5 retargeted `JAC_*` animation sequences | 296 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| VefectsVexa retargeted `JAC_*` animation sequences | 25 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| FreeAnimationsPack retargeted `JAC_*` animation sequences | 10 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| RogueCharacter retargeted `JAC_*` animation sequences | 7 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| FireTrailOfTheSword retargeted `JAC_*` animation sequences | 26 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| FightingAnimations retargeted `JAC_*` animation sequences | 11 | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |

RealmArchitect reconciliation on 2026-06-01 recovered only the missing Jacob animation deltas from the accidental RealmArchitect import. Nocturne remains the canonical Jacob destination; the `/Game/RealmArchitect/Art/Jacob` mesh, skeleton, materials, and duplicate Vexa clips were not copied into this project.

Repeatable reconciliation script and report:

```text
Tools/Unreal/reconcile_realmarchitect_jacob_assets.py
docs/asset-intake/JACOB_REALMARCHITECT_RECONCILIATION.json
```

Recovered source and destination paths:

```text
SourceArt/AnimationSources/FightingAnimations
/Game/NocturneSignal/AnimationSources/FightingAnimations/Animations
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FightingAnimations
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FireTrailOfTheSword
```

Verification result: 37 recovered retargeted assets, all resolving to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton`.

MCO TC Sword source import:

```text
Tools/Unreal/import_mco_tc_sword.py
SourceArt/AnimationSources/MCO_TC_Sword
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword
```

MCO TC Sword retarget destination:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword
```

Motifect Sword source import:

```text
Tools/Unreal/import_motifect_sword.py
SourceArt/AnimationSources/MotifectSword
/Game/NocturneSignal/AnimationSources/MotifectSword
```

Motifect Sword retarget destination:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword
```

Full Fab combat source import:

```text
Tools/Unreal/import_fab_combat_libraries.py
SourceArt/AnimationSources/MotifectMartialArts
SourceArt/AnimationSources/RealisticCombatMoves
/Game/NocturneSignal/AnimationSources/MotifectMartialArts
/Game/NocturneSignal/AnimationSources/RealisticCombatMoves
```

Full Fab combat retarget destinations:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectMartialArts
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RealisticCombatMoves
```

Universal Animation Library source import and full retarget destinations:

```text
Tools/Unreal/import_universal_animation_libraries.py
/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary1
/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary2
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2
```

Advanced Locomotion Mechanics UE5 source copy and retarget destination:

```text
Repository: https://github.com/DocDamage/Advanced-Locomotion-Mechanics-UE5
Source package paths: /Game/Animation, /Game/Mesh/Skeletal/Default
Source mesh: /Game/Mesh/Skeletal/Default/SKM_Manny
Retarget destination: /Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/AdvancedLocomotionMechanicsUE5
```

Import note: this repository provides Unreal `.uasset` packages, not FBX files. The source assets were kept at their original package paths so the copied animation packages can resolve their Manny skeleton references.

License note: `F:\Nocturne Signal\2dunrealproject\license.txt` declares the assets CC0 1.0/public-domain dedicated, with a royalty-free, non-exclusive, irrevocable, worldwide fallback license if the public-domain dedication is not valid in a jurisdiction. Attribution is optional.

Animation Blueprint:

```text
/Game/NocturneSignal/Characters/Jacob/ABP_Jacob
```

Gameplay montage:

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordCombo
```

The montage uses `JAC_KBS_Sword_ATK_Combo_01_001_IP`, resolves to `SK_Jacob_Skeleton`, and has sections:

```text
Default
ComboStart
ComboRecover
```

Additional sword montages:

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordSlashHorizontal
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordThrustForward
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordParryRiposte
```

The slash and thrust montages have `Default`, `AttackStart`, and `Recover` sections. The parry/riposte montage has `Default`, `ParryStart`, `Riposte`, and `Recover` sections.

Recovered FireTrail/Fighting candidate montages:

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_FireTrail_Action01
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_FireTrail_Action08
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_FireTrail_Action16
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Fighting_CrossPunch
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Fighting_HookPunch
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Fighting_ElbowPunch
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Fighting_Impact
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Fighting_Death
```

These were created on 2026-06-01 from the RealmArchitect reconciliation outputs with `Tools/Unreal/create_recovered_jacob_montages.py`. They resolve to `SK_Jacob_Skeleton` and have named montage sections applied through the `NocturneSignalEditor` editor bridge.

Recovered montage report:

```text
docs/asset-intake/JACOB_RECOVERED_MONTAGE_REPORT.json
```

Ability animation coverage:

```text
docs/asset-intake/JACOB_ABILITY_ANIMATION_COVERAGE.md
```

Current coverage summary:

- Tentacle attack has `AM_Jacob_TentacleAttack_ForceChoke`.
- Tentacle grapple has `AM_Jacob_TentacleGrapple_Start`, `AM_Jacob_TentacleGrapple_Loop`, and `AM_Jacob_TentacleGrapple_End`.
- Tentacle consume has `AM_Jacob_TentacleConsume_SneakNeckBreak` and `AM_Jacob_TentacleConsume_KidneyNeck`.
- Jump has start/loop/land clips from Universal Animation Library 1.
- Slide has start/loop/exit clips from Universal Animation Library 2.
- Double jump has NinjaJump start/loop/land clips from Universal Animation Library 2.
- Additional attack, stagger, hurt, consume, sword, cast, unarmed, and utility candidates are now available from the full Universal, Motifect Martial Arts, Realistic Combat, VefectsVexa, FreeAnimationsPack, and RogueCharacter retarget sets.
- Additional locomotion start/stop/pivot/crouch/jump and weapon-ready movement variants are now available from Advanced Locomotion Mechanics UE5.
- FireTrail sword actions and FightingAnimations punch/hit/death clips now have eight curated Jacob montages for candidate review.
- `ANocturnePlayerCharacter` exposes `TriggerRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId)` and `GetRecoveredCombatMontage(...)` so Blueprint/C++ can play the recovered combat candidates by selector.

Robotic tentacle visual import:

```text
Tools/Unreal/import_robotic_tentacle_hands.py
SourceArt/Tentacles/RoboticTentacleHands/hand_18.glb
/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands
```

Import result on 2026-05-30/2026-05-31 editor session:

| Asset Type | Count | Notes |
|---|---:|---|
| Skeletal meshes | 6 | Primary current C++ default: `hand_18/SkeletalMeshes/Cylinder` |
| Skeletons | 6 | Generated by GLB import; not Jacob skeletons |
| Physics assets | 6 | Generated by GLB import |
| AnimSequences | 3 | Imported GLB actions on generated sub-skeletons |
| Material instances | 10 | Generated from GLB materials |
| Texture2D | 1 | Generated from GLB source |

`ANocturnePlayerCharacter` now assigns the primary robotic `Cylinder` skeletal mesh to `UVestigeTentacleVisualAdapter`, hides the visual while idle, shows it during tentacle attack/consume, clears visibility on failed grapple, and leaves the fallback debug line enabled for target readability. `UVestigeLimbComponent` also routes `Failed` grapple state to the visual adapter cancellation hook so failed searches clean up outside Jacob-specific code. Final compile/PIE validation is still blocked until Live Coding accepts a compile or the editor is closed for a normal UBT build.

Preview level:

```text
/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobAnimationPreview
```

Repeatable preview build script:

```text
Tools/Unreal/build_jacob_animation_preview.py
```

The preview level contains Jacob skeletal mesh actors playing the MCO sword-ready idle, walk, run, and combo attack clips; Motifect sword draw, slash, thrust, and parry/riposte clips; Universal Animation Library jump, slide, and double-jump traversal clips; and three static robotic tentacle mesh preview actors for `Cylinder`, `Cylinder_041`, and `Cylinder_082`. It remains a curated preview map, not a display of every retargeted clip.

Command-line preview rebuild note: `UnrealEditor-Cmd` successfully rebuilt and saved the map on 2026-05-31 without `-nullrhi`. The same script path under `-nullrhi` crashed inside engine/editor scripting while spawning skeletal preview actors, so use the normal command-line editor or full editor for this preview script.

Current ABP status:

- Created and bound to Jacob's skeleton/preview mesh.
- `ANocturnePlayerCharacter` now exposes Blueprint-callable animation hooks for slide, jump, double jump, tentacle attack, tentacle grapple, and tentacle consume.
- State machine wiring is still open. The Unreal MCP bridge can modify an existing state machine but did not create one in the empty Anim Blueprint, so the next pass should either create the initial AnimGraph/state machine in-editor or add a focused script/tool path for initial AnimGraph construction.

Additional animation sources identified on 2026-05-30:

```text
docs/asset-intake/ANIMATION_SOURCE_INVENTORY.md
```

The next animation task is selection and Anim Blueprint/gameplay wiring, not raw asset intake. FBX files were sufficient for the latest Unreal retarget passes. GLB files can still be inspected or imported if needed, and `.blend` source files are only required if rig cleanup, pose fixes, or export repair is needed.

---

## Usage Notes

1. Use Jacob as a temporary 3D reference/player stand-in, not as the final Nocturne Signal protagonist.
2. Keep Nocturne's 2D gameplay architecture independent of this skeletal mesh.
3. If a 2D sprite workflow is chosen, use Jacob as a pose/animation reference or render source rather than binding core movement to this rig.
4. Preserve `SourceArt/Jacob/License.txt` and this attribution note in any public distribution.
