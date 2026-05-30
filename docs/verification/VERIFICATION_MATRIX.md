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
| V-007 | Unreal project opens | Editor launch | UE 5.7 opens project without fatal plugin errors | Open | Not tested |
| V-008 | C++ compile | Build in IDE or Unreal | Project compiles cleanly | Open | Not tested |
| V-009 | Packaged build | Unreal package | Package succeeds with required plugins | Open | Not tested |

---

## 2. Plugin Verification

| ID | Plugin/System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-010 | Paper2D | Editor/plugin check | Plugin enabled and sprites render | Open | Not tested |
| V-011 | PaperZD | Compile + PIE + package | Animation framework works without blocking package | Open | Not tested |
| V-012 | Enhanced Input | PIE input test | Keyboard/controller actions fire correctly | Open | Not tested |
| V-013 | Niagara | PIE VFX test | 2D-compatible test effect renders correctly | Open | Not tested |
| V-014 | MetaSounds | Beat clock test | Beat event timing is reliable enough for Choir Resonance | Open | Not tested |
| V-015 | FAB plugins | `.uproject` reconciliation | Every enabled plugin documented in plugin register | Blocked | Waiting for `.uproject` |

---

## 3. Asset Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-020 | Archive decompression | Controlled extraction | All selected archives extract without corruption | Open | Not tested |
| V-021 | Asset inventory | Generated report | Inventory includes paths, types, image dimensions, categories | Open | Not generated |
| V-022 | First-slice selection | Manifest review | Required Reliquary categories identified | Open | Not selected |
| V-023 | Import path policy | Manual inspection | Assets use `Content/NocturneSignal/...` paths | Open | Not tested |
| V-024 | Visual readability | In-editor review | Collision edges and interactables are readable | Open | Not tested |

---

## 4. Player Movement Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-030 | Player spawn | PIE test | Player spawns in test room and accepts input | Open | Not tested |
| V-031 | Run movement | 30-second movement test | No jitter, sticking, or unintended acceleration | Open | Not tested |
| V-032 | Jump/fall | Repeated jump test | Jump arc is consistent and readable | Open | Not tested |
| V-033 | Landing | Landing event test | Landing state triggers consistently | Open | Not tested |
| V-034 | Platform collision | Platform test room | No ledge sticking beyond intended behavior | Open | Not tested |
| V-035 | Placeholder art | Sprite swap test | Movement survives placeholder/final art swap | Open | Not tested |

---

## 5. Vestige Grapple Verification

| ID | System | Verification Method | Pass Condition | Status | Evidence |
|---|---|---|---|---|---|
| V-040 | Grapple component | PIE/debug test | Component attaches to player and reports state | Open | Not tested |
| V-041 | Grapple anchor actor | Placement test | Anchor can be placed and detected | Open | Not tested |
| V-042 | Anchor range | In/out range test | Only anchors in range are valid | Open | Not tested |
| V-043 | Pull-to-Point | Grapple all test nodes | Player reaches target without orbiting or jitter | Open | Not tested |
| V-044 | Release behavior | Arrival test | Release occurs cleanly within arrival radius | Open | Not tested |
| V-045 | Exit velocity | Repeated release test | Exit feels controlled and predictable | Open | Not tested |
| V-046 | Camera | Repeated grapple test | No harsh snap or disorientation | Open | Not tested |
| V-047 | Debug display | Runtime inspection | State, anchor, distance, velocity visible | Open | Not tested |
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
