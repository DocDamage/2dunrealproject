# Jacob Ability Animation Coverage

**Date:** 2026-05-30
**Character:** `/Game/NocturneSignal/Characters/Jacob/SK_Jacob`
**Skeleton:** `/Game/NocturneSignal/Characters/Jacob/SK_Jacob_Skeleton`

This tracks whether Jacob has usable animation coverage for the current required player abilities. `Ready` means an Unreal asset exists and resolves to Jacob's skeleton. It does not mean gameplay code or Anim Blueprint wiring is complete.

---

## Required Ability Coverage

| Ability | Status | Current Asset | Notes |
|---|---|---|---|
| Slide | Ready | `JAC_SK_UAL2_MannequinArmature_Slide_Start`, `Slide_Loop`, `Slide_Exit` | Imported from Universal Animation Library 2. Start/exit montages exist; loop sequence is ready for Anim Blueprint state use. |
| Jump | Ready | `JAC_SK_UAL1_MannequinArmature_Jump_Start`, `Jump_Loop`, `Jump_Land` | Imported from Universal Animation Library 1. Start/land montages exist; loop sequence is ready for Anim Blueprint state use. |
| Double jump | Ready | `JAC_SK_UAL2_MannequinArmature_NinjaJump_Start`, `NinjaJump_Idle_Loop`, `NinjaJump_Land` | Imported from Universal Animation Library 2. Start/land montages exist; loop sequence is ready for airborne double-jump state use. |
| Attack - tentacles | Ready | `/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleAttack_ForceChoke` | Uses ForceChoke attacker animation as tentacle-cast placeholder. Sections: `Default`, `CastStart`, `Hold`, `Release`. |
| Grapple - tentacles | Ready | `AM_Jacob_TentacleGrapple_Start`, `AM_Jacob_TentacleGrapple_Loop`, `AM_Jacob_TentacleGrapple_End` | Uses ForceChoke start/loop/end attacker clips. Suitable for a tentacle reach/hold/release gameplay sequence. |
| Consume - tentacles | Ready | `AM_Jacob_TentacleConsume_SneakNeckBreak`, `AM_Jacob_TentacleConsume_KidneyNeck` | Two consume placeholders from paired stealth takedown clips. Both have `ConsumeStart` and `ConsumeResolve` sections. |

---

## Tentacle Montage Assets

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleAttack_ForceChoke
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleGrapple_Start
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleGrapple_Loop
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleGrapple_End
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleConsume_SneakNeckBreak
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_TentacleConsume_KidneyNeck
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_AerialAttack_DoubleJumpPlaceholder
```

Verification result: all listed montage assets exist, resolve to `SK_Jacob_Skeleton`, and have named gameplay sections.

---

## Traversal Assets

Jump, slide, and double-jump traversal coverage was added from Universal Animation Library sources on 2026-05-30. The full Universal Animation Library 1 and 2 source sets are now retargeted, but the clips below remain the primary traversal picks.

Source imports:

```text
Tools/Unreal/import_universal_animation_libraries.py
SourceArt/AnimationSources/UniversalAnimationLibrary1
SourceArt/AnimationSources/UniversalAnimationLibrary2
/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary1
/Game/NocturneSignal/AnimationSources/UniversalAnimationLibrary2
```

Retargeted Jacob sequences:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1/JAC_SK_UAL1_MannequinArmature_Jump_Start
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1/JAC_SK_UAL1_MannequinArmature_Jump_Loop
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1/JAC_SK_UAL1_MannequinArmature_Jump_Land
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_Slide_Start
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_Slide_Loop
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_Slide_Exit
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_NinjaJump_Start
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_NinjaJump_Idle_Loop
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2/JAC_SK_UAL2_MannequinArmature_NinjaJump_Land
```

Traversal montages:

```text
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Jump_Start
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Jump_Land
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Slide_Start
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_Slide_Exit
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_DoubleJump_Start
/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_DoubleJump_Land
```

Verification result: all listed traversal sequences and montages exist, resolve to `SK_Jacob_Skeleton`, and have named gameplay sections where applicable. The broadened Universal retarget pass contains 45 UAL1 clips and 43 UAL2 clips, all resolving to `SK_Jacob_Skeleton`.

---

## Gameplay Hook Status

`ANocturnePlayerCharacter` now exposes Blueprint-callable hooks for the required Jacob ability animations:

```text
StartJump()
StopJump()
StartSlide()
StopSlide()
TriggerTentacleAttack()
TriggerTentacleGrapple()
TriggerTentacleConsume(bool bUseAlternateConsume)
TriggerRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId)
TryVestigeGrapple()
```

Runtime animation state exposed for Blueprint/AnimBP binding:

```text
IsSliding()
IsDoubleJumping()
IsTentacleActionActive()
GetCurrentAbilityAnimation()
GetRecoveredCombatMontage(ENocturneJacobRecoveredCombatMontage MontageId)
```

The C++ hook layer loads the existing Jacob montages for jump, land, double jump, slide, tentacle attack, tentacle grapple, tentacle consume, and the eight recovered FireTrail/Fighting combat candidates. One-shot tentacle attack/consume and recovered combat hooks clear their active state after montage playback; grapple clears when `UVestigeLimbComponent` returns to `Idle` or `Failed`.

`ANocturnePlayerCharacter` now also owns a default `UVestigeTentacleVisualAdapter` component. The adapter can attach an imported skeletal or static tentacle mesh to Jacob's mesh/root, play configurable idle/extend/pull/release animation assets, and still draws the fallback debug line until a real mesh is assigned.

---

## Robotic Tentacle Visual Asset

The new Fab tentacle source was staged on 2026-05-30:

```text
SourceArt/Tentacles/RoboticTentacleHands/hand_18.glb
SourceArt/Tentacles/RoboticTentacleHands/metadata.json
SourceArt/Tentacles/RoboticTentacleHands/thumbnail.png
Tools/Unreal/import_robotic_tentacle_hands.py
```

GLB inspection result:

| Property | Count |
|---|---:|
| Nodes | 353 |
| Meshes | 180 |
| Materials | 10 |
| Skins | 10 |
| Embedded animations | 17 |

Planned Unreal destination:

```text
/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands
```

Import status: imported through the live editor on 2026-05-30/2026-05-31. Unreal created 32 assets under `/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands`: 6 skeletal meshes, 6 skeletons, 6 physics assets, 3 AnimSequences, 10 material instances, and 1 texture. The current C++ default assigns `hand_18/SkeletalMeshes/Cylinder` to `VestigeTentacleVisualAdapter`, toggles visibility during tentacle attack/consume, and clears the visual on failed grapple. The imported GLB animations are on generated sub-skeletons, so they are not yet treated as full tentacle motion for the primary `Cylinder` mesh.

---

## Expanded Candidate Libraries

Additional Jacob retarget sets now available:

```text
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary1
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/UniversalAnimationLibrary2
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectMartialArts
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RealisticCombatMoves
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/AdvancedLocomotionMechanicsUE5
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/VefectsVexa
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FreeAnimationsPack
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RogueCharacter
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FireTrailOfTheSword
/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/FightingAnimations
```

Additional candidate sets staged for next import/retarget pass:

```text
SourceArt/AnimationSources/ActorCoreWalk
SourceArt/AnimationSources/ActorCoreTactical
SourceArt/AnimationSources/GameAnimationSample
SourceArt/AnimationSources/ParagonMannyCurated
SourceArt/AnimationSources/FightAnimationMocapPack
Content/Vefects/Tentacles_VFX
```

The restarted editor sees the copied `FreeAnimationsPack`, `RogueCharacter`, and `Vefects` packages. Current verified additions are 25 VefectsVexa spell/action clips, 10 FreeAnimationsPack gesture/cast clips, 7 RogueCharacter locomotion/jump clips, 26 FireTrail sword-action clips, and 11 FightingAnimations punch/hit/death clips, all retargeted to Jacob's skeleton.

RealmArchitect reconciliation report:

```text
docs/asset-intake/JACOB_REALMARCHITECT_RECONCILIATION.json
```

Recovered FireTrail/Fighting montages created from the reconciliation pass:

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

Recovered montage report:

```text
docs/asset-intake/JACOB_RECOVERED_MONTAGE_REPORT.json
```

Verification result: all eight recovered montages exist, resolve to `SK_Jacob_Skeleton`, and expose the requested named sections. The section mutation is handled by the `NocturneSignalEditor` editor bridge because UE 5.7 Python does not expose `UAnimMontage::AddAnimCompositeSection` directly.

Useful ability-adjacent candidates:

| Need | Candidate Source |
|---|---|
| Alternate consume | `JAC_SK_UAL2_MannequinArmature_Consume` |
| Hit/stagger | UAL1 `Hit_Chest`, `Hit_Head`; UAL2 `Hit_Knockback`; Realistic Combat `Hit_*`, `hurted`, `hit_tired` |
| Attack variants | Motifect Martial Arts sword, staff, spear, muay thai, taekwondo, judo, and wrestling clips |
| Sword trail attacks | FireTrailOfTheSword `JAC_Fire_A_NS_01` through `JAC_Fire_A_NS_26` |
| Punch/death reactions | FightingAnimations `JAC_Fighting_Cross_Punch_Anim`, `Hook_Punch`, `Elbow_Punching`, `Impact_mixamo_com`, `Dying*`, `Punching*` |
| Movement variants | UAL1 walk/jog/sprint/crouch/roll/swim; UAL2 climb/roll/shield dash/sword dash |
| Locomotion polish | Advanced Locomotion Mechanics UE5 unarmed/pistol/rifle walk, jog, start, stop, pivot, crouch, and jump variants |
| New jump/slide/traversal options | Game Animation Sample staged Jump/Traversal/Slide subset |
| New melee/monster/cast options | Paragon curated Manny subset from minions, Grux, Fey, and Serath |
| Additional fight reactions | Fight Animation Mocap Pack staged hit, beaten, stomp, and taunt clips |
| Alternate cast/levitation poses | FreeAnimationsPack `AS_AttackInLevitation2`, `AS_ComboHands`, `AS_FlyingUp` |
| Alternate rogue locomotion/props | RogueCharacter `MM_*` locomotion/jump clips, `SM_Knife`, `SM_Shield` |
| Tentacle visual effects | Vefects `Tentacles_VFX` goo/tentacle VFX and audio support assets |
| Robotic tentacle mesh | `RoboticTentacleHands` imported `Cylinder` skeletal mesh assigned through `UVestigeTentacleVisualAdapter` |

---

## Next Animation Wiring Need

Priority wiring tasks:

1. Compile/reload the updated `ANocturnePlayerCharacter` module if Live Coding was not active during the latest edit.
2. Wire `ABP_Jacob` states for jump start, jump loop, jump land using the new exposed state accessors.
3. Wire slide start, slide loop, slide exit states or triggerable montage flow.
4. Wire double jump start, double jump loop, double jump land.
5. Decide whether `AM_Jacob_AerialAttack_DoubleJumpPlaceholder` remains as an aerial attack or gets retired.

The current limitation is not asset coverage; it is final Anim Blueprint graph wiring, C++ compile after the active Live Coding session, and PIE validation.
