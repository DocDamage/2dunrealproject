# Nocturne Signal — Project Manifest

**Repository:** `DocDamage/2dunrealproject`  
**Engine Target:** Unreal Engine 5.7  
**Game Type:** 2D Metroidvania / action RPG / gothic sci-fi exploration game  
**Primary Development Mode:** Documentation-first, then C++ core systems with Blueprint/PaperZD content wiring  
**Manifest Date:** 2026-05-30  
**Status:** Active pre-production / first playable slice setup

---

## 1. Canonical Source Documents

This repository is governed by the uploaded Nocturne Signal design documents:

1. `NOCTURNE_SIGNAL_ENHANCED_DESIGN_v0.2.md`
   - Base enhanced mission/design plan.
   - Defines world, story, phases, risk register, verification matrix, core systems, vertical slice scope, and production discipline.

2. `NOCTURNE_SIGNAL_AMENDMENT_0003_VESTIGE_LIMB.md`
   - Current mechanical amendment.
   - Introduces the Vestige Limb System as the central traversal, combat, progression, consume, and weapon-form mechanic.
   - Supersedes older Boneblade-centered combat assumptions wherever the two documents conflict.

**Authority Rule:**

- Use the Enhanced Design Document for the global world, story, production plan, audio direction, systems matrix, milestones, and vertical slice scope.
- Use the Vestige Limb Amendment as the current authority for player traversal, player combat, progression unlocks, consume mechanics, and weapon forms.
- If the documents conflict, the Vestige Limb Amendment wins unless a later signed design document replaces it.

---

## 2. Locked Development Decisions

These decisions are locked for the first implementation pass:

| Area | Decision |
|---|---|
| Architecture | C++ core systems with Blueprint/PaperZD content wiring |
| Movement Feel | Castlevania: Symphony of the Night style: grounded, weighty, readable, not floaty |
| Character Art | Character art will be added later by Doc in the IDE; prototype should support placeholder/silhouette art |
| Documentation | Add repo documentation scaffolding before Unreal code expands |
| First Target | Slice 0: toolchain + asset intake; Slice 1: player + Vestige Pull-to-Point grapple test room |
| Plugins | Additional FAB plugins are already installed by Doc and must be reconciled once the `.uproject` is visible |

---

## 3. Project North Star

The immediate goal is not to build the full game. The immediate goal is to prove the dream is mechanically and technically real.

The first playable slice must prove:

- Unreal Engine 5.7 can support the project’s 2D stack.
- PaperZD can drive reliable 2D player and enemy animation.
- SOTN-style player movement feels good.
- Vestige Limb traversal feels excellent.
- Pull-to-Point grapple works before room layouts are finalized.
- Combat has readable weight, hit pause, stagger, and commitment.
- Consume/Predator Protocol can drive permanent progression.
- Signal Corruption, Relics, Choir Resonance, SaveGame, and Null-Voice can coexist without becoming fragile.

---

## 4. Current Core Stack

| Layer | Target |
|---|---|
| Engine | Unreal Engine 5.7 |
| 2D Animation | PaperZD + Paper2D |
| Input | Enhanced Input |
| Visual Effects | Niagara, 2D-compatible effects |
| Audio | MetaSounds, reactive beat clock, zone BPM events |
| Persistence | Unreal SaveGame system |
| Content Definitions | Data Assets |
| Large Map Strategy | World Partition only after first slice architecture is stable |
| Source Control | GitHub repository: `DocDamage/2dunrealproject` |

---

## 5. Plugin Policy

Doc has additional FAB plugins installed locally. Do not assume their names or APIs until the Unreal project exists and the `.uproject` plugin list is available.

Plugin intake rule:

1. Capture every enabled plugin from the `.uproject` file.
2. Categorize plugins as:
   - Required for first playable slice
   - Useful but not required yet
   - Risky / unknown compatibility
   - Cosmetic or asset-only
3. Do not build core gameplay around a plugin unless it is confirmed compatible with Unreal Engine 5.7.
4. PaperZD is part of the intended core stack and must be verified early.
5. Plugin failures must be documented in the risk register before workarounds are implemented.

Planned plugin register path:

```text
docs/plugins/PLUGIN_REGISTER.md
```

---

## 6. Uploaded Asset Intake Policy

The uploaded zip archives contain castle, gothic, structure, prop, trap, decor, lighting, town, nature, tile, and environmental asset categories.

Asset archives must not be dumped blindly into the Unreal project.

Required intake sequence:

1. Decompress archives into a temporary intake folder.
2. Generate an asset inventory.
3. Identify sprite/tile resolution, naming patterns, and duplicates.
4. Separate first-slice assets from full-game backlog assets.
5. Decide import destination paths before moving files into `Content/`.
6. Record all accepted assets in an asset manifest.
7. Record rejected/deferred assets instead of deleting them silently.

Planned asset manifest path:

```text
docs/asset-intake/ASSET_INTAKE_MANIFEST.md
```

Recommended Unreal content paths:

```text
Content/NocturneSignal/Characters/
Content/NocturneSignal/Enemies/
Content/NocturneSignal/Environments/ReliquaryOfWaking/
Content/NocturneSignal/Props/
Content/NocturneSignal/VFX/
Content/NocturneSignal/Audio/
Content/NocturneSignal/Data/
Content/NocturneSignal/UI/
Content/NocturneSignal/Maps/TestRooms/
Content/NocturneSignal/Maps/ReliquaryOfWaking/
```

---

## 7. First Playable Slice Scope

The first playable slice is the Reliquary of Waking.

Required slice rooms from the design plan:

- Waking Coffin
- Corpse Drawer Hall
- Broken Lift Shaft
- First Still Chamber
- Reliquary Processing
- Candle Autopsy Room
- Bone Chute
- Undertaker’s Workshop
- Locked Ossuary Door
- Coffin Engine
- Return Shortcut
- Exit to Lower Nave

Do not expand beyond this slice until the movement, grapple, combat, save/load, and boss prototype gates pass.

---

## 8. First Implementation Roadmap

### Slice 0 — Repository, Toolchain, and Intake

Deliverables:

- Project manifest in repository.
- Documentation folders.
- Plugin register template.
- Asset intake manifest template.
- Unreal project setup notes.
- First-slice risk register.
- Verification checklist.

Exit criteria:

- Repo has a documented source of truth.
- Asset intake process is defined before extraction/import.
- Plugin list is ready to reconcile when the `.uproject` exists.

### Slice 1 — Player Feel and Pull-to-Point Grapple

Deliverables:

- Unreal player character scaffold.
- SOTN-style run/jump/fall tuning baseline.
- Placeholder player art support.
- `VestigeLimbComponent` or equivalent core gameplay component.
- `GrappleAnchor` actor.
- Pull-to-Point grapple test room.
- Camera behavior test during grapple.
- Debug display for target anchor, grapple state, velocity, and chain counter.

Exit criteria:

- Player can move, jump, fall, and land with readable weight.
- Player can grapple to visible architecture nodes.
- Pull-to-Point does not feel floaty or imprecise.
- Camera does not snap or disorient during grapple movement.

### Slice 2 — Swing, Chain Grapple, and Broken Lift Shaft Prototype

Deliverables:

- Swing grapple.
- Chain grapple up to 3 nodes.
- Architecture node placement rules.
- Broken Lift Shaft prototype layout.
- Basic limb extension/retraction visual.

Exit criteria:

- A 3-node chain can be completed without ground contact.
- Required traversal path remains solvable with Pull-to-Point alone.
- Swing path feels like a reward path, not a required precision wall.

### Slice 3 — Combat Room and Bonespike

Deliverables:

- Enemy dummy.
- Failed Waker prototype.
- Bonespike form.
- Basic attack startup/active/recovery windows.
- Hit pause and stagger.
- Consume threshold detection placeholder.

Exit criteria:

- Combat has weight.
- Bonespike is clearly stronger than Tendril Flail.
- Enemy health threshold can trigger a consume-ready state.

---

## 9. Core Gameplay Systems to Build First

Priority order:

1. Player movement controller
2. Vestige Limb component
3. Grapple anchor system
4. Pull-to-Point grapple
5. Swing grapple
6. Chain grapple
7. Combat state machine
8. Weapon form data assets
9. Bonespike form
10. Failed Waker enemy
11. Predator Protocol consume threshold
12. SaveGame persistence for consumed enemies and upgrades
13. Signal Corruption meter
14. Relic slot prototype
15. Choir Resonance beat detection prototype
16. Null-Voice trigger/audio/subtitle system

---

## 10. Proposed Core C++ Classes

Initial C++ class candidates:

```text
ANocturnePlayerCharacter
UNocturneMovementComponent
UVestigeLimbComponent
AGrappleAnchor
UNocturneCombatComponent
UNocturneHealthComponent
UNocturneCorruptionComponent
UNocturneSaveSubsystem
UNocturneInventoryComponent
UNocturneRelicComponent
UWeaponFormDataAsset
URelicDataAsset
ACombatTestEnemy
AFailedWakerEnemy
```

Blueprint/PaperZD should remain responsible for:

- Animation graph wiring
- Animation notifies
- Tunable animation timing
- Enemy presentation
- VFX hooks
- Audio hooks
- Room-specific trigger scripting
- Designer-facing Data Asset setup

---

## 11. Vestige Limb System Priority

The Vestige Limb System is the current center of the game.

First implementation targets:

- Stage 1: Proto limbs
- Two visible limbs at rest
- Pull-to-Point grapple
- Architecture anchors only
- Tendril Flail placeholder attack
- Bonespike unlock path stub
- Consume-ready state on Failed Waker

Not first-pass targets:

- Full multi-limb combat
- Full form wheel
- Signal anchors
- Penitent anchors
- Oria’s Form
- Dual enemy grip
- Late-game corruption scaling

These are full-game systems and should not block first-slice movement proof.

---

## 12. Hard Problem Protocol

When a hard technical or design problem blocks progress, stop implementation and research before committing to a solution.

Required comparison process:

1. Consult official Unreal Engine documentation where applicable.
2. Consult PaperZD documentation/community examples where applicable.
3. Consult academic or engineering references when the problem involves physics, AI, procedural systems, audio timing, control systems, or UX measurement.
4. Consult AAA/GDC-style production references when the problem involves game feel, combat readability, level design, animation pipelines, or content production.
5. Consult Reddit/community reports for practical engine/plugin failure cases.
6. Consult YouTube only when the source demonstrates implementation details that cannot be captured well in text.
7. Produce the best 3 viable solutions.
8. Select the one that best fits Nocturne Signal’s constraints.
9. Record the decision in the appropriate architecture or risk document.

Do not use research as an excuse to avoid implementation. Use it only when the problem is genuinely hard, risky, or unclear.

---

## 13. Risk Register Seed

| ID | Severity | Risk | Mitigation |
|---|---|---|---|
| R-001 | Critical | PaperZD / UE 5.7 compatibility issue | Compile/package test before production content |
| R-002 | High | Large asset library causes scope creep | Lock first slice assets before importing everything |
| R-003 | High | 2D collision instability in UE | Build movement/collision test rooms early |
| R-004 | Critical | Grapple feels floaty or imprecise | Prototype in dedicated test map before Reliquary layout |
| R-005 | High | FAB plugin assumptions break project portability | Reconcile plugins from `.uproject`; document required plugins |
| R-006 | Medium | Character art arrives later and changes proportions | Use placeholder capsule/sprite dimensions with configurable data |
| R-007 | High | Consume prompt is missed by players | Prototype limb pulse readability early |
| R-008 | Medium | Choir Resonance is invisible | Add clear audio/visual feedback and debug timing |
| R-009 | Critical | SaveGame bugs corrupt progression | Save/load stress tests begin with first consume prototype |

---

## 14. Verification Discipline

No system is complete until verified.

Use this status language:

- `Open` — not started
- `In Progress` — actively being built
- `Fixed` — implemented but not proven
- `Verified` — proven through build, test, runtime check, or clear manual inspection
- `Blocked` — cannot proceed until a dependency is resolved

Do not mark anything `Verified` because it looks correct.

---

## 15. Immediate Next Files to Add

Recommended next documentation files:

```text
docs/README.md
docs/plugins/PLUGIN_REGISTER.md
docs/asset-intake/ASSET_INTAKE_MANIFEST.md
docs/architecture/ARCHITECTURE_DECISIONS.md
docs/slice-00/SLICE_00_TOOLCHAIN_AND_INTAKE.md
docs/slice-01/SLICE_01_PLAYER_AND_GRAPPLE.md
docs/risks/RISK_REGISTER.md
docs/verification/VERIFICATION_MATRIX.md
```

Recommended first Unreal-side files after project creation:

```text
Source/NocturneSignal/NocturneSignal.Build.cs
Source/NocturneSignal/Public/NocturnePlayerCharacter.h
Source/NocturneSignal/Private/NocturnePlayerCharacter.cpp
Source/NocturneSignal/Public/VestigeLimbComponent.h
Source/NocturneSignal/Private/VestigeLimbComponent.cpp
Source/NocturneSignal/Public/GrappleAnchor.h
Source/NocturneSignal/Private/GrappleAnchor.cpp
```

---

## 16. Standing Rule

Nocturne Signal must be built like a mission, not a jam folder.

Every feature needs:

- A reason to exist
- A source document reference
- A first-slice priority decision
- A technical owner path
- A verification method
- A clear distinction between prototype, production, and polish

Build the Reliquary. Make Veyra feel excellent. Prove the Vestige Limb. Then scale.
