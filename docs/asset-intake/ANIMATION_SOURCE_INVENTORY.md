# Animation Source Inventory

**Inventory date:** 2026-05-30
**Project:** `F:\Nocturne Signal\2dunrealproject`
**Current Jacob retarget destination:** `/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations`

This file tracks animation sources that are available locally but not necessarily imported into Unreal yet. Keep raw archives and Fab cache payloads as intake sources. Import or extract only the selected clips needed for a slice.

---

## Current Jacob Status

| Area | Status |
|---|---|
| Jacob skeletal mesh | Imported at `/Game/NocturneSignal/Characters/Jacob/SK_Jacob` |
| Jacob skeleton | `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton` |
| Existing retargeted set | 44 RamsterZ animations |
| MCO TC Sword retargeted set | 4 sword locomotion/combat animations |
| Motifect Sword retargeted set | 4 sword action/pose animations |
| Motifect Martial Arts full set | 40 combat animations |
| Realistic Combat Moves full set | 10 idle/hit reaction animations |
| Universal Animation Library 1 full set | 45 animations |
| Universal Animation Library 2 full set | 43 animations |
| Advanced Locomotion Mechanics UE5 full set | 296 locomotion/action animations |
| VefectsVexa full set | 25 dash/jump/spell/sword/hit animations |
| FreeAnimationsPack full set | 10 cast/levitation/gesture/action animations |
| RogueCharacter full set | 7 locomotion/jump animations |
| Sword combo montage | `/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordCombo` |
| Additional sword montages | 3 Motifect slash/thrust/parry montages |
| Animation preview level | `/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobAnimationPreview` |
| Animation Blueprint | `/Game/NocturneSignal/Characters/Jacob/ABP_Jacob` exists, state machine wiring still open |

For Unreal retargeting, the most useful source format is FBX animation plus a known source skeleton or source skeletal mesh. GLB files are acceptable for inspection and possible import, but FBX is the safer first path for UE animation retargeting. Blend source files are useful when the rig, scale, pose, or animation channels need repair, but they are not required for a normal retarget pass.

---

## Newly Dropped Root Archives

| Archive | Size | Useful Source Files | Intake Decision |
|---|---:|---:|---|
| `F:\Nocturne Signal\Actorcore-Unreal-0530-593952.zip` | 24.09 MB | 12 `.fbx`, 12 `.json` | Staged as ActorCore tactical movement; import script added |
| `F:\Nocturne Signal\Actorcore-Unreal-0530-584214.zip` | 8.85 MB | 4 `.fbx`, 4 `.json` | Staged as ActorCore walk set; import script added |
| `F:\Nocturne Signal\MCO_TC_Sword_Free_Pack_01.zip` | 55.42 MB | 18 `.fbx`, 32 `.uasset` | Best next candidate for Jacob sword locomotion/combat |
| `F:\Nocturne Signal\Universal Animation Library[Standard].zip` | 8.33 MB | 1 `.fbx`, 1 `.glb` | Inspect skeleton before import; broad library source |
| `F:\Nocturne Signal\Universal Animation Library 2[Standard].zip` | 9.79 MB | 2 `.fbx`, 2 `.glb`, 1 `.blend` | Inspect skeleton before import; broad library source |
| `F:\Nocturne Signal\HumanMageRAW.zip` | 73.81 MB | 1 `.fbx` | Character/mesh candidate, not clearly an animation pack |
| `F:\Nocturne Signal\StandardAnimationshowcaseWin64.zip` | 154.54 MB | 0 source animation files found | Packaged demo/reference only; do not import as animation source |

### ActorCore Root Archives

Staged on 2026-05-30:

```text
SourceArt/AnimationSources/ActorCoreWalk
SourceArt/AnimationSources/ActorCoreTactical
Tools/Unreal/import_actorcore_animation_libraries.py
```

Source clips:

```text
ActorCoreWalk: walk-1start-378927, walk-2loop-379004, walk-3end-378983
ActorCoreTactical: against_wall_turn_l_to_sneakwalk, b083-runtoblastb, c08_low_hold_gun_turn180_l, crouch_walk_r_againstwall, dual_gun_draw_gun_behind_back_279371, dual_gun_muzdn_end_pose_279349, dual_gun_muzdn_mov_cool_shoot_279383, e07_low_hide_wall_reload, hold_gun_fastrun_forward_start/loop/end
```

The import script creates `/Game/NocturneSignal/AnimationSources/ActorCore` and the retarget script now has `ActorCoreWalk` and `ActorCoreTactical` source sets ready for Jacob once the editor bridge or commandlet path is healthy.

---

## New Fab Library Additions

Source root checked:

```text
C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\FabLibrary
```

High-value new animation sources:

| Source | Raw FBX Count | Intake Decision |
|---|---:|---|
| Game Animation Sample Animations Retargeted to UE5 Mannequin | 1374 | Staged first-pass Jump/Traversal/Slide subset: 260 FBXs |
| Paragon animations retargeted to Manny | 5385 | Staged curated character/action subset: 545 FBXs from `minionsManny`, `GruxManny`, `FeyManny`, and `SerathManny` |
| Fight Animation Mocap Pack | 11 | Staged full pack: 1 source mesh + 10 fight/hit/taunt animations |
| Free Crockscrew Animation | 1 | Deferred; single acrobatic candidate |
| Multiple Backflip V2 | 1 | Deferred; single acrobatic candidate |

Staged paths:

```text
SourceArt/AnimationSources/GameAnimationSample
SourceArt/AnimationSources/ParagonMannyCurated
SourceArt/AnimationSources/FightAnimationMocapPack
Tools/Unreal/import_fab_jacob_candidate_animations.py
```

Retarget script source sets added:

```text
GameAnimationSample
ParagonMannyCurated
FightAnimationMocapPack
```

Import/retarget status: staged and scripted; not yet imported into Unreal. The editor bridge is now healthy, so these remain the next source-import candidates after the copied `.uasset` packages below.

---

## RogueCharacterModel Project Intake

Source checked:

```text
F:\Nocturne Signal\2dunrealproject\RogueCharacterModel
```

This is a full UE 5.7 copied project. The useful packages below were copied into the main project at their original `/Game/...` package paths so `.uasset` dependencies can resolve after an editor restart or asset registry rescan.

| Source Package | Main Project Path | Useful Content | Intake Decision |
|---|---|---|---|
| `FreeAnimationsPack` | `Content/FreeAnimationsPack` | 10 root `AS_*` AnimSequences plus Manny/Quinn mannequin rigs | Copied; added retarget source `FreeAnimationsPack` |
| `RogueCharacter` | `Content/RogueCharacter` | Rogue skeletal meshes, modular parts, knife/shield props, basic locomotion/jump clips | Copied; added retarget source `RogueCharacter` |
| `Vefects/Tentacles_VFX` | `Content/Vefects/Tentacles_VFX` | Tentacle VFX, audio, goo materials, demo mannequin support assets | Copied as visual/VFX support for Jacob tentacle abilities |
| `A_Surface_Footstep` | `Content/A_Surface_Footstep` | UE4 mannequin idle/run/walk/jump clips and surface footstep VFX | Already present; no new copy needed |
| `Vefects/Easy_Impact_Frames` | `Content/Vefects/Easy_Impact_Frames` | Vexa dash, jump, spell, stomp, sword, hit, and death animations | Already present; retarget source `VefectsVexa` was already configured |

High-value newly available clips:

```text
FreeAnimationsPack: AS_AttackInLevitation2, AS_ComboHands, AS_FlyingUp, AS_RightLegKick2, AS_EatingOnParty
RogueCharacter: MM_Idle, MM_Walk_Fwd, MM_Run_Fwd, MM_Jump, MM_Fall_Loop, MM_Land
VefectsVexa: Dash, AirDash, AirStomp, HandsSpell, SnappySpell, SummonCreature, Jump01-03, SwordAttack, SwordSlash, hit reactions
```

Retarget script source sets added:

```text
FreeAnimationsPack
RogueCharacter
```

`VefectsVexa` and `SurfaceFootstep` were already present in the retarget script. `VefectsVexa`, `FreeAnimationsPack`, and `RogueCharacter` have now been retargeted after the restarted editor picked up the copied packages.

Retargeted on 2026-05-30 after editor restart and asset-registry rescan:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/VefectsVexa      25 AnimSequences
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FreeAnimationsPack 10 AnimSequences
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RogueCharacter     7 AnimSequences
```

Verification result: MCP `anim.list_sequences` resolves all three folders to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton`.

### MCO TC Sword Free Pack FBX Entries

| Entry | Size |
|---|---:|
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Ready_Idle_001.fbx` | 1.90 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Run_F_001.fbx` | 1.84 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Run_F_001_IP.fbx` | 1.84 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Sword_ATK_Combo_01_001.fbx` | 1.99 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Sword_ATK_Combo_01_001_IP.fbx` | 1.99 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Walk_F_001.fbx` | 1.85 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/KBS_Walk_F_001_IP.fbx` | 1.85 MB |
| `TC_Sword_Free_Pack/FBX_Pack/Animation/MotusMan_v50 FBX T Pose.fbx` | 1.95 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/In_Place/KBS_Run_F_001_IP.fbx` | 1.91 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/In_Place/KBS_Sword_ATK_Combo_01_001_IP.fbx` | 2.08 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/In_Place/KBS_Walk_F_001_IP.fbx` | 2.01 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/Root_Motion/KBS_Ready_Idle_001.fbx` | 2.07 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/Root_Motion/KBS_Run_F_001.fbx` | 1.91 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/Root_Motion/KBS_Sword_ATK_Combo_01_001.fbx` | 2.08 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/FBX/Root_Motion/KBS_Walk_F_001.fbx` | 2.01 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/Motionbuilder/SK_Mannequin_Edit_Template.fbx` | 3.19 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/SKMannequin_A_Pose/SK_Mannequin.fbx` | 2.19 MB |
| `TC_Sword_Free_Pack/UE4_Pack/TC_Sword/Source/SKMannequin_T_Pose/SK_Mannequin.fbx` | 2.18 MB |

Imported on 2026-05-30 using:

```text
Tools/Unreal/import_mco_tc_sword.py
```

SourceArt staging path:

```text
SourceArt/AnimationSources/MCO_TC_Sword
```

Imported Unreal source assets:

```text
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/SK_MCO_TC_Sword_Mannequin
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/SK_MCO_TC_Sword_Mannequin_Skeleton
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/Animations/KBS_Ready_Idle_001
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/Animations/KBS_Walk_F_001_IP
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/Animations/KBS_Run_F_001_IP
/Game/NocturneSignal/AnimationSources/MCO_TC_Sword/Animations/KBS_Sword_ATK_Combo_01_001_IP
```

Retargeted Jacob output:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Ready_Idle_001
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Walk_F_001_IP
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Run_F_001_IP
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword/JAC_KBS_Sword_ATK_Combo_01_001_IP
```

Verification: all four retargeted clips resolve to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton`, and no generated `JAC_*` assets remain in `/Game` root.

Gameplay/preview assets created on 2026-05-30:

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordCombo
/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobAnimationPreview
Tools/Unreal/build_jacob_animation_preview.py
```

The montage uses `JAC_KBS_Sword_ATK_Combo_01_001_IP`, is bound to `SK_Jacob_Skeleton`, has a play length of 5.4667 seconds, and includes `Default`, `ComboStart`, and `ComboRecover` sections. The preview level contains Jacob skeletal mesh actors for side-by-side review of selected sword clips.

---

## Fab Library Animation Candidates

| Fab Folder | Size | Source Files | Current Decision |
|---|---:|---:|---|
| `Motifect_Martial_Arts_Motion_Pack-95f5f297` | 28.35 MB | 40 `.fbx` | Fully staged, imported, and retargeted to Jacob |
| `Realistic_Combat_Moves___10_Mocap_Pack-6abe0677` | 24.19 MB | 11 `.fbx` | Fully staged, imported, and 10 animation clips retargeted to Jacob |
| `RamsterZ_Free_Anims_Volume_1-9319491d` | Manifest only in FabLibrary; expanded VaultCache content exists separately | Unreal `.uasset` content | Already retargeted to Jacob from direct project content |

### Motifect Martial Arts Motion Pack

Available FBX clips:

```text
judo_ankle_sweep
judo_hip_throw
muay_thai_body_kick
muay_thai_combination
muay_thai_elbow_cut
muay_thai_guard_stance
muay_thai_knee_clinch
muay_thai_push_kick_defense
muay_thai_roundhouse
muay_thai_teep
spear_thrust_sequence
staff_block
staff_combo
staff_overhead_strike
staff_spin_guard
staff_sweep_legs
staff_thrust
sword_block_high
sword_combo_slash_thrust
sword_draw_stance
sword_overhead_strike
sword_parry_and_riposte
sword_sheathe
sword_slash_diagonal_down
sword_slash_horizontal
sword_spinning_slash
sword_thrust_forward
tkd_axe_kick
tkd_back_kick
tkd_front_kick_high
tkd_jump_front_kick
tkd_jump_spinning_kick
tkd_roundhouse_high
tkd_side_kick
tkd_spinning_heel_kick
wrestling_body_slam
wrestling_double_leg_takedown
wrestling_guard_position
wrestling_single_leg_takedown
wrestling_stand_up_defense
```

Recommended use: keep the original four sword clips as named montage candidates, but the full 40-clip library is now available for combat move selection.

Imported on 2026-05-30 using:

```text
Tools/Unreal/import_motifect_sword.py
SourceArt/AnimationSources/MotifectSword
/Game/NocturneSignal/AnimationSources/MotifectSword
```

Import note: Motifect FBXs include `Jaw`, `LeftEye`, and `RightEye` tracks. The selected clips import against the MCO mannequin skeleton with those facial-track warnings ignored only after verifying all expected AnimSequences were created.

Retargeted Jacob output:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_draw_stance
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_slash_horizontal
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_thrust_forward
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword/JAC_sword_parry_and_riposte
```

Montages:

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordSlashHorizontal
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordThrustForward
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordParryRiposte
```

Verification: all four retargeted clips and all three montages resolve to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton`. `L_JacobAnimationPreview` now contains eight Jacob skeletal mesh actors and eight labels.

Full-library import and retarget pass added on 2026-05-30:

```text
SourceArt/AnimationSources/MotifectMartialArts
Tools/Unreal/import_fab_combat_libraries.py
/Game/NocturneSignal/AnimationSources/MotifectMartialArts/Animations
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectMartialArts
```

Result: 40 source AnimSequences and 40 retargeted Jacob `JAC_*` AnimSequences. All retargeted clips resolve to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton`.

### Realistic Combat Moves - 10 Mocap Pack

Available FBX files:

```text
05_01_002_Hit_punch_R_01
05_01_005_Hit_punch_L
05_01_009_Hit_punch_L_01
05_01_010_Hit_punch_L_02
05_01_016_hit_tired_L
05_01_022_hurted
05_04_001_idle
05_04_002_idle_R
05_04_003_idle_L
05_04_009_single hand idle
Male_Lowpoly
```

The project also has the mesh/material subset under:

```text
Content/Fab/Realistic_Combat_Moves_10_Mocap_Pack
```

Full-library import and retarget pass added on 2026-05-30:

```text
SourceArt/AnimationSources/RealisticCombatMoves
Tools/Unreal/import_fab_combat_libraries.py
/Game/NocturneSignal/AnimationSources/RealisticCombatMoves/SK_RealisticCombat_MaleLowpoly
/Game/NocturneSignal/AnimationSources/RealisticCombatMoves/Animations
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RealisticCombatMoves
```

Result: 10 source AnimSequences and 10 retargeted Jacob `JAC_*` AnimSequences. All retargeted clips resolve to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton`.

Recommended use: damage reactions, stagger, hurt, and alternate idle/readiness poses.

---

## Universal Animation Libraries

Universal Animation Library 1 and 2 were broadened from the initial traversal-only pass to full-library retargeting on 2026-05-30.

```text
Tools/Unreal/import_universal_animation_libraries.py
Tools/Unreal/retarget_animations_to_jacob.py
/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary1
/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary2
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2
```

| Library | Retargeted Count | Useful Jacob Categories |
|---|---:|---|
| Universal Animation Library 1 | 45 | jump, crouch, idle, walk/jog/sprint, roll, hits, death, pickup, pistol, punch, sword, swim, utility idles |
| Universal Animation Library 2 | 43 | slide, ninja/double-jump, consume, climb, hit knockback, sword combo/block/dash, shield dash, throw, zombie references, utility/farming idles |

Verification: all 88 Universal `JAC_*` clips resolve to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton`.

---

## Advanced Locomotion Mechanics UE5

Repository checked: `https://github.com/DocDamage/Advanced-Locomotion-Mechanics-UE5`

Decision: useful animation source; imported and retargeted to Jacob on 2026-05-30.

The repository is a UE 5.4 project. The useful content is `.uasset` animation content rather than FBX source, so the source packages were copied into the project at their original package paths to preserve hard references:

```text
Content/Animation
Content/Mesh/Skeletal/Default
/Game/Animation/Assets
/Game/Mesh/Skeletal/Default/SKM_Manny
```

Retarget source and destination:

```text
Tools/Unreal/retarget_animations_to_jacob.py
/Game/Animation/Assets
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/AdvancedLocomotionMechanicsUE5
```

| Source Category | Source Assets |
|---|---:|
| Action | 8 |
| AimOffset | 77 |
| Pistol | 70 |
| Rifle | 75 |
| Shotgun | 2 |
| Unarmed | 68 |

Unreal registry result: 296 source `AnimSequence` assets and 4 source `AnimMontage` assets under `/Game/Animation/Assets`. The 296 `AnimSequence` assets were retargeted to Jacob. The source montages were retained as source references; gameplay-ready Jacob montages should be created explicitly from selected retargeted clips when needed.

Useful Jacob categories: unarmed idle/crouch/walk/jog/start/stop/pivot/jump, pistol/rifle locomotion and aim offsets, weapon equip/fire motions, and general action clips. This is a strong source for polished locomotion transitions and directional movement variants.

License: local license file at `F:\Nocturne Signal\2dunrealproject\license.txt` declares the assets CC0 1.0/public-domain dedicated, with a royalty-free, non-exclusive, irrevocable, worldwide fallback license if the public-domain dedication is not valid in a jurisdiction. Attribution is optional.

Verification: all 296 retargeted `JAC_*` clips resolve to `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton.SK_Jacob_Skeleton`.

---

## ozz-animation Repository Check

Repository checked: `https://github.com/DocDamage/ozz-animation`

Decision: do not import this into the Unreal project for Jacob animation coverage right now.

Reason: ozz-animation is a C++ skeletal animation runtime/toolset, not an animation content pack. It provides runtime playback, sampling, blending, and conversion tooling for formats such as glTF, FBX, Collada, Obj, 3ds, and dxf. The repository includes sample media under `media/`, but those are runtime/toolchain examples rather than game-ready Jacob movement/combat clips. Unreal already provides the runtime animation system and IK Retargeter we are using, so adding ozz would duplicate runtime responsibilities and increase integration cost.

Potential later use: offline animation compression/conversion research only, if Nocturne Signal later needs a custom non-Unreal animation runtime.

---

## Recommended Jacob Animation Order

1. Wire `ABP_Jacob` with the already-retargeted RamsterZ clips so Jacob has a working idle/locomotion/combat preview baseline.
2. MCO TC Sword in-place clips are imported and retargeted for sword-ready idle, walk, run, and combo attack.
3. Sword combo montage and side-by-side preview level are created.
4. Motifect sword subset is imported, retargeted, and converted into slash/thrust/parry montages.
5. Universal Animation Library 1 and 2 are fully imported and retargeted; use the traversal subset first for jump, slide, and double jump.
6. Motifect Martial Arts and Realistic Combat Moves are fully imported and retargeted; choose specific clips for attack, hit reaction, stagger, and consume variants.
7. Advanced Locomotion Mechanics UE5 is fully imported and retargeted; use it for locomotion start/stop/pivot/crouch/jump polish and weapon-ready movement variants.
8. Wire the traversal and sword locomotion clips into `ABP_Jacob` once the initial state machine exists.
9. Treat HumanMage, StandardAnimationShowcase, and ozz-animation as reference/tooling unless a specific need emerges.

---

## Verification Checklist For Next Import

| Check | Expected Result |
|---|---|
| Source FBX imports into an intake namespace | Assets land outside `/Game/NocturneSignal/Characters/Jacob` until validated |
| Source skeleton/mesh exists | Retargeter has a stable source rig |
| Retargeted clips use Jacob skeleton | Retargeted output skeleton is `SK_Jacob_Skeleton` |
| Asset registry count matches selected clips | No stray generated `JAC_*` assets remain in `/Game` root |
| ABP compile result | `ABP_Jacob` compiles with no errors before use |
