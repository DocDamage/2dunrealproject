# Nocturne Signal — Architecture Decision Record

**Purpose:** Record project-level engineering decisions, tradeoffs, and constraints.

**Rule:** Architecture decisions must be explicit. Do not let random prototype choices silently become production architecture.

---

## ADR-0001 — Core Gameplay Architecture

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | Use C++ core systems with Blueprint/PaperZD content wiring |

### Context

Nocturne Signal needs precise movement, grapple traversal, combat state management, save/load reliability, and scalable data-driven content. Pure Blueprint would be fast at first but risks becoming fragile as systems grow. Pure C++ would slow iteration for animation, VFX, room triggers, and designer tuning.

### Decision

Use a hybrid approach:

- C++ for core gameplay systems and persistent state.
- Blueprint for tuning, animation hookup, VFX/audio triggers, and room scripting.
- PaperZD for sprite animation state machines and animation notifies.
- Data Assets for forms, relics, enemy definitions, and tunable gameplay data.

### Consequences

Positive:

- Better long-term maintainability.
- Easier save/load discipline.
- Cleaner component boundaries.
- Stronger debugging for movement/combat.

Negative:

- Requires early project structure discipline.
- Requires IDE/C++ compile loop.
- Slightly slower than pure Blueprint for first prototypes.

---

## ADR-0002 — Movement Feel Target

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | Target Castlevania: Symphony of the Night style grounded movement |

### Context

The game is inspired by Symphony of the Night and Super Metroid, but the design documents call for weight, commitment, and deliberate motion. The Vestige Limb system supplies high-mobility traversal, so base player movement should not be floaty.

### Decision

Base movement should feel:

- Grounded
- Readable
- Slightly weighty
- Responsive but not frictionless
- More SOTN than Super Metroid

Air control should exist but should not erase commitment. Grapple traversal provides the high-speed/momentum fantasy.

### Consequences

Positive:

- Combat reads better.
- Hit pause/stagger will feel stronger.
- Vestige grapple becomes the special traversal identity.

Negative:

- Movement tuning must avoid feeling stiff.
- Grapple must be excellent or traversal may feel too conservative.

---

## ADR-0003 — Vestige Limb Supersedes Boneblade as Core Weapon

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | The Vestige Limb system is the current combat/traversal/progression authority |

### Context

The enhanced design document originally defined Boneblade-centered combat. The Vestige Limb amendment revises the design and makes the limbs the central mechanic.

### Decision

The player’s primary system is now Vestige Limb based:

- Tether Traversal
- Combat Grip
- Predator Protocol
- Weapon Shaping

The Boneblade is not discarded as lore. It is absorbed into limb weapon forms, especially Choir Blade.

### Consequences

Positive:

- Stronger original identity.
- Traversal, combat, and progression are unified.
- Consume mechanics become mechanically central instead of side content.

Negative:

- Higher animation/VFX burden.
- Grapple/game-feel risk becomes critical.
- More complex player state machine.

---

## ADR-0004 — Asset Intake Before Unreal Import

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | Inventory and classify uploaded assets before importing into Unreal |

### Context

The project has many uploaded zip archives across gothic castle, town, props, traps, lighting, nature, and detail categories. Importing everything immediately would create clutter, broken references, unclear scale, and scope creep.

### Decision

Use a controlled intake process:

1. Extract outside the project.
2. Inventory contents.
3. Identify first-slice candidates.
4. Decide paths.
5. Import only selected assets into `Content/NocturneSignal/...`.
6. Track deferred assets.

### Consequences

Positive:

- Cleaner Unreal project.
- Better slice discipline.
- Easier asset scale/readability review.

Negative:

- Slower before visible level art appears.
- Requires maintaining the asset manifest.

---

## ADR-0005 — Placeholder Player Art Until IDE Character Integration

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | Use placeholder/silhouette player art until Doc adds character art in IDE |

### Context

Doc has character art but cannot upload it in this session. The first movement and grapple prototypes should not wait for final player art.

### Decision

Build the player architecture so art can be swapped later:

- Configurable sprite dimensions.
- Placeholder capsule/collision dimensions.
- PaperZD-ready animation hooks.
- No hard dependency on a specific spritesheet in C++.

### Consequences

Positive:

- Movement prototype can start immediately.
- Character art can be integrated later without rewriting core movement.

Negative:

- Final animation timing may need retuning after real art is added.
- Collision dimensions must be revisited with final sprite proportions.

---

## ADR-0006 — Plugin Dependency Discipline

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | Reconcile local FAB plugins from `.uproject` before relying on them |

### Context

Doc has additional FAB plugins installed locally. Their names, versions, and UE 5.7 compatibility are not yet visible in the repository.

### Decision

Do not build core gameplay around unknown plugins. Once the `.uproject` exists, list every plugin in `docs/plugins/PLUGIN_REGISTER.md` with compatibility and purpose.

### Consequences

Positive:

- Fewer portability failures.
- Cleaner handoff into IDE.
- Easier diagnosis if plugins fail to load.

Negative:

- Some potentially useful plugin features will remain deferred until verified.

---

## ADR-0007 — First Implementation Target

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-05-30 |
| Decision | Build Slice 0 intake/toolchain first, then Slice 1 player + Pull-to-Point grapple |

### Context

The design documents repeatedly emphasize proving game feel first and avoiding uncontrolled content scale.

### Decision

The first implementation sequence is:

1. Slice 0 — repo, docs, plugin register, asset intake, verification scaffolding.
2. Slice 1 — SOTN-style player controller and Pull-to-Point Vestige grapple in a test room.
3. Slice 2 — swing and chain grapple.
4. Slice 3 — combat room, Failed Waker, Bonespike, consume threshold.

### Consequences

Positive:

- Grapple scale informs level blockout.
- Avoids wasted room design.
- Produces a clean, testable first prototype.

Negative:

- Story/visual content will appear later than raw mechanics.

---

## Pending Architecture Decisions

| ID | Topic | Status | Notes |
|---|---|---|---|
| ADR-0008 | Exact Unreal module/project name | Open | Waiting for `.uproject` creation |
| ADR-0009 | 2D collision strategy | Open | Needs movement test room |
| ADR-0010 | Grapple math approach | Open | Pull-to-Point can start simple; swing may require research/tuning |
| ADR-0011 | SaveGame schema | Open | Needed before consume persistence |
| ADR-0012 | PaperZD animation notify conventions | Open | Needed after character art integration |
| ADR-0013 | MetaSounds beat clock implementation | Open | Needs official/audio timing research before production use |
