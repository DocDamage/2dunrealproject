# Nocturne Signal — Verification Matrix

**Purpose:** Define proof requirements for every first-slice system.

**Rule:** A feature is not done until it has a verification method and passes it.

**Status Values:** `Open`, `In Progress`, `Fixed`, `Verified`, `Blocked`

---

## 1. Project / Toolchain Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-001 | Repo manifest | File inspection | `PROJECT_MANIFEST.md` exists | Fixed | Repo file exists |
| V-002 | Docs index | File inspection | `docs/README.md` exists | Fixed | Repo file exists |
| V-003 | Plugin register | File inspection | `docs/plugins/PLUGIN_REGISTER.md` exists | Fixed | Repo file exists |
| V-004 | Asset intake manifest | File inspection | `docs/asset-intake/ASSET_INTAKE_MANIFEST.md` exists | Fixed | Repo file exists |
| V-005 | Architecture decisions | File inspection | `docs/architecture/ARCHITECTURE_DECISIONS.md` exists | Fixed | Repo file exists |
| V-006 | Risk register | File inspection | `docs/risks/RISK_REGISTER.md` exists | Fixed | Repo file exists |
| V-007 | Unreal project opens | Editor launch | UE 5.7 opens project without fatal plugin errors | Verified | Live editor is open on 2026-05-30; Unreal MCP bridge reports UE `5.7.4-51494982+++UE5+Release-5.7` |
| V-008 | C++ compile | Build in IDE or Unreal | Project compiles cleanly | Verified | Non-MCP UBT build succeeded on 2026-05-31 after the editor was closed: `NocturneSignalEditor Win64 Development`; updated Jacob/tentacle C++ and UnrealMCPBridge plugin compiled successfully. Later UBT builds on 2026-05-31 also passed after directional grapple targeting, line-of-sight filtering, `LineBlocked` failure reporting, and debug telemetry were added |
| V-009 | Packaged build | Unreal package | Package succeeds with required plugins | Open | Not tested |

---

## 2. Plugin Verification

| ID | Plugin/System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-010 | Paper2D | Editor/plugin check | Plugin enabled and sprites render | Open | Not tested |
| V-011 | PaperZD / current plugin set | Compile + PIE + package | Animation framework and enabled plugins work without blocking package | In Progress | Plugin ids resolve locally; non-MCP editor-target compile succeeds. PIE and packaging still need validation |
| V-012 | Enhanced Input | PIE input test | Keyboard/controller actions fire correctly | In Progress | Enhanced Input assets created under `/Game/NocturneSignal/Input`; `IMC_Slice01` maps keyboard/mouse and modern controller actions. `ANocturnePlayerCharacter` now adds the mapping context at BeginPlay and binds through `UEnhancedInputComponent`, with legacy input mappings retained as fallback. `Tools/Unreal/validate_slice01_input.py` passed through `UnrealEditor-Cmd` on 2026-05-31; PIE controller validation still required |
| V-013 | Niagara | PIE VFX test | 2D-compatible test effect renders correctly | Open | Not tested |
| V-014 | MetaSounds | Beat clock test | Beat event timing is reliable enough for Choir Resonance | Open | Not tested |
| V-015 | Enabled plugin reconciliation | `.uproject` reconciliation | Every enabled plugin documented in plugin register | Fixed | Current `.uproject` enabled plugin list is documented; compile verification pending Live Coding shutdown |
| V-016 | Unreal MCP bridge | Codex MCP config + editor bridge status | Codex exposes Unreal MCP bridge tools and attaches to the open UE project | Verified | Verified on 2026-05-30: `unreal_mcp_ping`, `editor.engine_version`, `editor.project_name`, `level.current_map`, and `asset.exists` all return successfully against UE `5.7.4` on `127.0.0.1:30020`. Previous timeout was reproduced as a broad/incorrectly shaped query issue, not a dead bridge; use paginated `asset.list` filter objects and narrow `anim.list_sequences` `path_prefix` calls |

---

## 3. Asset Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-020 | Archive decompression | Controlled extraction | All selected archives extract without corruption | Verified | 135 zips extracted successfully to `F:\Nocturne Signal\asset_intake\extracted` on 2026-05-30 |
| V-021 | Asset inventory | Generated report | Inventory includes paths, types, image dimensions, categories | Verified | `docs/asset-intake/GENERATED_ASSET_INVENTORY.csv` generated with 158 PNG rows and dimensions |
| V-022 | First-slice selection | Manifest review | Required Reliquary categories identified | Open | Not selected |
| V-023 | Import path policy | Manual inspection | Assets use `Content/NocturneSignal/...` paths | In Progress | Jacob imported under `Content/NocturneSignal/Characters/Jacob`; other content imports still need review |
| V-024 | Visual readability | In-editor review | Collision edges and interactables are readable | Open | Not tested |
| V-025 | Jacob temporary character import | Unreal import + file inspection | Skeletal mesh, skeleton, animations, materials, and textures exist under approved path | Verified | Imported on 2026-05-30 to `/Game/NocturneSignal/Characters/Jacob`; source and attribution stored under `SourceArt/Jacob` |
| V-026 | Jacob retargeted animation set | Unreal retarget + asset registry check | Retargeted Jacob animation sequences exist under approved path and use Jacob skeleton | Verified | 44 RamsterZ `JAC_*` AnimSequences created under `/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/RamsterZ`; `JAC_Standing_Idle` resolves to `SK_Jacob_Skeleton` |
| V-027 | Jacob Animation Blueprint | Asset creation + state-machine inspection | Animation Blueprint exists and has a validated locomotion state machine | In Progress | `/Game/NocturneSignal/Characters/Jacob/ABP_Jacob` created and saved; `ANocturnePlayerCharacter` now exposes slide, jump, double-jump, tentacle attack, grapple, and consume animation hooks; state machine wiring still open |
| V-028 | Jacob sword animation source import | Unreal import + asset registry check | Sword source skeleton and selected animations exist under approved intake namespace | Verified | MCO TC Sword source skeleton and 4 AnimSequences imported under `/Game/NocturneSignal/AnimationSources/MCO_TC_Sword` on 2026-05-30 |
| V-029 | Jacob sword retargeted animation set | Unreal retarget + asset registry check | Retargeted sword clips exist under approved Jacob path and use Jacob skeleton | Verified | 4 MCO TC Sword `JAC_*` AnimSequences created under `/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MCO_TC_Sword`; all resolve to `SK_Jacob_Skeleton`; no stray root `JAC_*` assets found |
| V-030 | Jacob sword combo montage | Montage creation + asset inspection | Combo montage exists, uses Jacob skeleton, and has named sections for gameplay triggering | Verified | `/Game/NocturneSignal/Characters/Jacob/Montages/AM_Jacob_SwordCombo` created; skeleton is `SK_Jacob_Skeleton`; sections are `Default`, `ComboStart`, `ComboRecover`; length is 5.4667s |
| V-031 | Jacob animation preview level | Level creation + actor summary | Preview map exists with labeled actors for selected Jacob sword/traversal/tentacle visual clips | Verified | `/Game/NocturneSignal/Characters/Jacob/Maps/L_JacobAnimationPreview` rebuilt and saved through non-MCP `UnrealEditor-Cmd` on 2026-05-31; curated preview now includes 17 Jacob animation rows plus 3 robotic tentacle mesh rows. Use command-line editor/full editor for this script; `-nullrhi` crashes inside engine/editor scripting while spawning skeletal preview actors |
| V-032 | Jacob Motifect sword import | Unreal import + asset registry check | Selected Motifect sword clips import under approved intake namespace | Verified | 4 Motifect sword AnimSequences imported under `/Game/NocturneSignal/AnimationSources/MotifectSword`; known Jaw/LeftEye/RightEye track warnings accepted after asset verification |
| V-033 | Jacob Motifect sword retarget/montage set | Unreal retarget + montage inspection | Retargeted Motifect sword clips and gameplay montages exist and use Jacob skeleton | Verified | 4 Motifect `JAC_*` AnimSequences created under `/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/MotifectSword`; 3 montages created under `/Game/NocturneSignal/Characters/Jacob/Montages`; all resolve to `SK_Jacob_Skeleton` |

---

## 4. Player Movement Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-034 | Player spawn | PIE test | Player spawns in test room and accepts input | Open | Not tested |
| V-035 | Run movement | 30-second movement test | No jitter, sticking, or unintended acceleration | Open | Not tested |
| V-036 | Jump/fall | Repeated jump test | Jump arc is consistent and readable | Open | Not tested |
| V-037 | Landing | Landing event test | Landing state triggers consistently | Open | Not tested |
| V-038 | Platform collision | Platform test room | No ledge sticking beyond intended behavior | Open | Not tested |
| V-039 | Placeholder art | Sprite swap test | Movement survives placeholder/final art swap | Open | Not tested |
| V-039A | Modern controller movement | PIE controller test | Left stick and D-pad move, bottom face button jumps, left face/left shoulder slides, right shoulder grapples, right trigger attacks, right face consumes, top face alternate-consumes | In Progress | `Tools/Unreal/validate_slice01_input.py` validates `IA_MoveHorizontal`, `IA_MoveLeft`, `IA_MoveRight`, `IA_Jump`, `IA_Slide`, `IA_TentacleGrapple`, `IA_TentacleAttack`, `IA_TentacleConsume`, `IA_TentacleAlternateConsume`, `IMC_Slice01`, and legacy fallback mappings; commandlet passed on 2026-05-31. Runtime controller pass still required |

---

## 5. Vestige Grapple Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-040 | Grapple component | PIE/debug test | Component attaches to player and reports state | In Progress | `UVestigeLimbComponent` compiles on the player and exposes state, current anchor, failure reason, candidate counts, best score, and last selection debug text; PIE runtime inspection still required |
| V-041 | Grapple anchor actor | Placement test | Anchor can be placed and detected | In Progress | `L_JacobGameplayTest` generation script places right, left, high, blocked, and consume-dummy `AGrappleAnchor` actors in the Sakura Temple test room; commandlet inspection found 5 anchor actors, 33 Sakura sprite actors, 6 hidden collision actors, and playable Jacob; PIE runtime detection still required |
| V-042 | Anchor range | In/out range test | Only anchors in range are valid | In Progress | C++ filters by `MaxGrappleRange` before scoring and records in-range candidate count; manual near/far runtime test still required |
| V-043 | Pull-to-Point | Grapple all test nodes | Player reaches target without orbiting or jitter | Open | Not tested |
| V-044 | Release behavior | Arrival test | Release occurs cleanly within arrival radius | Open | Not tested |
| V-045 | Exit velocity | Repeated release test | Exit feels controlled and predictable | Open | Not tested |
| V-046 | Camera | Repeated grapple test | No harsh snap or disorientation | Open | Not tested |
| V-047 | Debug display | Runtime inspection | State, anchor, distance, velocity visible | In Progress | Selected anchor line/arrival radius draw in-world; component exposes state, current anchor, candidate counts, selected score, and last selection debug text. `bDrawDebugOverlay` adds an on-screen state/failure/anchor/distance/speed/candidate readout; PIE readability pass still required |
| V-048 | Swing grapple | Test room sequence | Swing arc can be completed without clipping | Open | Future slice |
| V-049 | Chain grapple | 3-node sequence | Chain can be completed without ground contact | Open | Future slice |

---

## 6. Combat Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-060 | Combat component | PIE/debug test | Player can enter attack state | Open | Future slice |
| V-061 | Hitbox timing | Debug hitbox view | Startup/active/recovery windows are visible/tunable | Open | Future slice |
| V-062 | Hit pause | Runtime impact test | Impact freezes briefly and improves feel | Open | Future slice |
| V-063 | Enemy health | Damage test | Enemy receives damage and dies | Open | Future slice |
| V-064 | Stagger | Hit reaction test | Enemy stagger triggers correctly | Open | Future slice |
| V-065 | Bonespike form | Attack test | Bonespike has intended range/damage/readability | Open | Future slice |
| V-066 | Choir Blade form | Attack test | Choir Blade supports basic 3-hit arc later | Open | Future slice |
| V-067 | Jacob tentacle montage coverage | Montage inspection + code hook inspection | Tentacle attack, grapple, and consume montage placeholders exist, resolve to Jacob skeleton, and have player-callable trigger hooks | Verified | `AM_Jacob_TentacleAttack_ForceChoke`, `AM_Jacob_TentacleGrapple_Start/Loop/End`, and `AM_Jacob_TentacleConsume_SneakNeckBreak/KidneyNeck` exist; all resolve to `SK_Jacob_Skeleton`; `ANocturnePlayerCharacter` exposes `TriggerTentacleAttack`, `TriggerTentacleGrapple`, and `TriggerTentacleConsume` |
| V-068 | Jacob traversal animation coverage | Asset inventory + code hook inspection | Slide, jump, and true double-jump traversal clips are identified or explicitly marked missing and have player-callable hooks | Verified | UAL1 jump start/loop/land, UAL2 slide start/loop/exit, and UAL2 NinjaJump start/loop/land are retargeted to Jacob and documented in `docs/asset-intake/JACOB_ABILITY_ANIMATION_COVERAGE.md`; all resolve to `SK_Jacob_Skeleton`; `ANocturnePlayerCharacter` exposes `StartSlide`, `StopSlide`, and double-jump montage selection through `StartJump` |
| V-069 | Jacob expanded animation library coverage | Unreal import/retarget + asset registry check | Useful provided libraries are imported/retargeted or explicitly deferred with reason | In Progress | Full UAL1/UAL2 retarget counts are 45/43; Motifect Martial Arts imports/retargets 40; Realistic Combat imports/retargets 10; Advanced Locomotion Mechanics UE5 imports 296 source AnimSequences and retargets 296 to Jacob. After editor restart, MCP verified additional Jacob retargets: VefectsVexa 25, FreeAnimationsPack 10, RogueCharacter 7, all resolving to `SK_Jacob_Skeleton`. ActorCore, Game Animation Sample, Paragon Manny, and Fight Mocap remain staged/scripted for later source import |
| V-069A | Jacob robotic tentacle visual source | Source inspection + Unreal import + runtime attachment test | Real tentacle mesh/animations/VFX are imported or staged, assigned to `VestigeTentacleVisualAdapter`, and visible during grapple/attack/consume hooks | In Progress | `SourceArt/Tentacles/RoboticTentacleHands/hand_18.glb` imported through the live editor into `/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands`; 32 imported assets exist including 6 skeletal meshes and 3 AnimSequences. `ANocturnePlayerCharacter` now defaults `UVestigeTentacleVisualAdapter` to the imported `Cylinder` skeletal mesh and toggles/clears it for tentacle attack, consume, and failed grapple. Non-MCP UBT compile succeeds, and the preview map includes three robotic tentacle mesh rows; PIE/runtime visual validation remains open |

---

## 7. Predator Protocol Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-070 | Consume threshold | Enemy health test | 15% health threshold triggers consume-ready state | Open | Future slice |
| V-071 | Consume visual | Runtime review | Limb pulse/flash is readable without HUD text | Open | Future slice |
| V-072 | Consume action | Runtime action test | Grapple on eligible enemy consumes instead of drags | Open | Future slice |
| V-073 | Upgrade application | Runtime stat test | Failed Waker consume grants +15 Max HP | Open | Future slice |
| V-074 | Consume persistence | Save/load test | Consumed enemy state and upgrade persist after reload | Open | Future slice |
| V-075 | Consume cap | Repeated consume test | Per-enemy-type cap prevents infinite farming | Open | Future slice |

---

## 8. SaveGame Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-080 | Player state save | Save/load test | Health, Ether, corruption restore correctly | Open | Future slice |
| V-081 | Room flags | Save/load test | Defeated enemies/items stay resolved | Open | Future slice |
| V-082 | Progression state | Save/load test | Abilities/forms/relics persist | Open | Future slice |
| V-083 | Corruption persistence | Reload test | Corruption persists and derived state recalculates | Open | Future slice |

---

## 9. Audio / Choir Resonance Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-090 | MetaSounds test loop | Audio test | 72 BPM loop plays in test room | Open | Future slice |
| V-091 | Beat event output | Debug timing test | Beat events received by gameplay system | Open | Future slice |
| V-092 | Beat accuracy | 5-minute timing test | Beat event within acceptable timing tolerance | Open | Future slice |
| V-093 | Resonance hit | Combat timing test | On-beat hit triggers feedback and bonus | Open | Future slice |
| V-094 | Feedback readability | Player review | Resonance hit is noticeable but not cluttered | Open | Future slice |

---

## 10. Slice Exit Gates

### Slice 0 Exit Gate

Required before closing Slice 0:

- Manifest exists.
- Docs scaffold exists.
- Asset intake manifest exists.
- Plugin register exists.
- Risk register exists.
- Verification matrix exists.
- Asset inventory generated or explicitly deferred with reason.
- `.uproject` plugin reconciliation complete or blocked with reason.

### Slice 1 Exit Gate

Required before closing Slice 1:

- Player moves, jumps, falls, and lands reliably.
- Pull-to-Point grapple works on visible Architecture Nodes.
- Camera remains stable during grapple.
- Debug display exists.
- Anchor spacing recommendations are documented.
- Known movement/grapple issues are entered into the risk register.

---

## 11. Verification Rule

A row may only move to `Verified` when proof exists.

Acceptable proof:

- Build result
- PIE runtime test
- Packaged build
- Automated test output
- Manual test notes with exact conditions
- Asset inventory report
- File inspection for documentation-only deliverables

Do not mark gameplay systems Verified based only on expected behavior.
