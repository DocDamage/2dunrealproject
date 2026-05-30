# Slice 1 — Player Movement and Pull-to-Point Grapple

**Project:** Nocturne Signal  
**Slice:** 1  
**Status:** Open  
**Goal:** Prove SOTN-style player movement and the first Vestige Limb traversal mechanic in a controlled test room.

---

## 1. Objective

Slice 1 proves the first real game-feel pillar:

> Veyra must feel excellent to control before the Reliquary of Waking is laid out.

The first target is not full combat, full animation, or a finished room. The first target is a reliable player controller and a readable Pull-to-Point Vestige grapple using visible Architecture Nodes.

---

## 2. Design Authority

Current authority:

- Enhanced design document for phase discipline and vertical slice scope.
- Vestige Limb amendment for traversal, combat, progression, and weapon identity.

The Vestige Limb amendment requires grapple traversal to be proven before the Reliquary layout is finalized.

---

## 3. Required Feel

Base movement target:

- Castlevania: Symphony of the Night style
- Grounded
- Readable
- Slightly weighty
- Responsive without becoming floaty
- Strong landing feel
- Clear jump arcs
- Combat-ready movement commitment

Grapple target:

- Precise
- Deliberate
- Readable
- Fast enough to feel powerful
- Not simulation-floaty
- Camera-safe
- Supports future swing and chain systems

---

## 4. Deliverables

| ID | Deliverable | Status | Verification |
|---|---|---|---|
| S1-D001 | Unreal player character scaffold | Open | Player actor spawns in test map |
| S1-D002 | SOTN-style run movement | Open | Run acceleration/deceleration feels grounded |
| S1-D003 | Jump/fall/landing baseline | Open | Jump arc readable; landing event fires |
| S1-D004 | Placeholder player art support | Open | Character works without final Veyra art |
| S1-D005 | `VestigeLimbComponent` scaffold | Open | Component attaches to player and exposes state |
| S1-D006 | `GrappleAnchor` actor | Open | Anchor can be placed in test room |
| S1-D007 | Pull-to-Point grapple | Open | Player travels to selected architecture node |
| S1-D008 | Grapple targeting | Open | Nearest/valid anchor can be detected in range |
| S1-D009 | Grapple debug display | Open | Shows state, anchor, distance, velocity |
| S1-D010 | Camera behavior test | Open | No disorienting snap during grapple |
| S1-D011 | Test room map | Open | Contains floor, walls, and multiple architecture nodes |

---

## 5. Proposed C++ Classes

Initial candidates:

```text
ANocturnePlayerCharacter
UNocturneMovementComponent
UVestigeLimbComponent
AGrappleAnchor
```

Do not overbuild the class tree. Slice 1 only needs the smallest viable architecture that can survive expansion.

---

## 6. Grapple States

Initial Pull-to-Point state machine:

```text
Idle
  -> SearchingForAnchor
  -> Extending
  -> Anchored
  -> PullingPlayer
  -> Releasing
  -> Retracting
  -> Idle
```

Failure states:

```text
NoValidAnchor
OutOfRange
LineBlocked
Interrupted
```

Slice 1 can begin without LineBlocked if collision testing is not ready yet, but it must be added before real rooms.

---

## 7. Grapple Anchor Rules

Initial `GrappleAnchor` properties:

| Property | Type | Notes |
|---|---|---|
| `AnchorType` | Enum | Slice 1 only needs Architecture |
| `RequiredStage` | Integer | Default 1 |
| `RequiredCorruption` | Float | Default 0 |
| `bIsActive` | Bool | Runtime enable/disable |
| `GrappleRadius` | Float | Targeting radius |
| `ArrivalRadius` | Float | Distance at which pull releases |
| `DebugColor` | Color | For development only |

Initial anchor types:

```text
Architecture
Organic
Signal
Enemy
Penitent
```

Only `Architecture` should be implemented in Slice 1.

---

## 8. Pull-to-Point Rules

Prototype behavior:

1. Player presses Grapple.
2. `VestigeLimbComponent` searches for valid Architecture anchors in range.
3. Best anchor is selected.
4. Limb visual/debug line extends to anchor.
5. Player velocity is directed toward anchor.
6. Player arrives within arrival radius.
7. Player releases with preserved/controlled exit velocity.
8. Limb retracts.

Important tuning variables:

| Variable | Purpose |
|---|---|
| `MaxGrappleRange` | Prevents overreach |
| `PullSpeed` | Primary feel control |
| `PullAcceleration` | Prevents instant/robotic motion |
| `ArrivalRadius` | Prevents jitter at anchor |
| `ExitVelocityScale` | Controls momentum after release |
| `CooldownAfterRelease` | Prevents accidental double-fire |
| `AssistWindowFrames` | Helps input near valid node |

---

## 9. Debug Requirements

Slice 1 must expose enough debug information to tune movement quickly.

Required debug display:

- Current movement mode
- Current grapple state
- Selected anchor name
- Distance to anchor
- Player velocity
- Pull speed
- Anchor in range: yes/no
- Last release reason

Recommended debug visuals:

- Anchor range circles
- Line from player to selected anchor
- Different color for valid/invalid anchor
- Arrival radius marker

---

## 10. Test Room Requirements

The Slice 1 test room should include:

- Flat floor
- Basic wall
- Low platform
- Medium platform
- High platform
- 3 Architecture Nodes
- One pull-only required path
- One optional faster path
- Empty landing space after grapple

No enemies are required in Slice 1.

No final art is required in Slice 1.

---

## 11. Verification Tests

| Test | Method | Pass Condition | Status |
|---|---|---|---|
| Spawn test | PIE start | Player spawns and accepts input | Open |
| Run test | Move left/right for 30 seconds | No jitter, no collision instability | Open |
| Jump test | Repeated jumps on flat ground | Consistent arc and landing | Open |
| Platform test | Jump between platforms | No sticking on ledges beyond intended collision | Open |
| Anchor detection | Stand near/far from nodes | Only valid in-range nodes are selected | Open |
| Pull-to-Point | Grapple all test anchors | Arrives cleanly without orbiting/jitter | Open |
| Release behavior | Release at anchor | Exit velocity feels controlled | Open |
| Camera behavior | Grapple repeatedly | No harsh snap or nausea-inducing movement | Open |
| Placeholder art | Swap placeholder sprite | Movement still works | Open |

---

## 12. Known Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Base movement feels stiff | High | Tune acceleration, jump apex, landing recovery early |
| Grapple feels floaty | Critical | Use guided velocity, not full physics simulation |
| Anchor selection feels wrong | High | Add debug display and clear selection priority |
| Camera snaps during pull | High | Tune camera lag and max offset early |
| Placeholder dimensions mismatch final art | Medium | Use configurable collision dimensions |

---

## 13. Out of Scope

Do not build these in Slice 1:

- Swing grapple
- Chain grapple
- Enemy grapple
- Combat Grip
- Predator Protocol
- Bonespike
- Form wheel
- Full PaperZD animation set
- Final Veyra art
- Boss room
- Reliquary production layout

These start in later slices.

---

## 14. Handoff to Slice 2

Slice 2 begins only after Pull-to-Point is stable enough to inform room scale.

Required handoff evidence:

- Player movement test notes.
- Pull-to-Point tuning values.
- Camera settings.
- Anchor spacing recommendations.
- Known movement/collision issues.
