# Nocturne Signal — Plugin Register

**Purpose:** Track every Unreal Engine, PaperZD, Paper2D, FAB, marketplace, and project plugin used by Nocturne Signal.

**Rule:** Do not rely on any plugin until it is listed here with compatibility, purpose, risk, and slice priority.

---

## 1. Plugin Intake Status

| Field | Value |
|---|---|
| Engine Target | Unreal Engine 5.7 |
| Current `.uproject` available in repo | No |
| Local FAB plugins installed by Doc | Yes |
| Plugin reconciliation complete | No |
| Current status | Waiting for `.uproject` and enabled plugin list |

---

## 2. Core Intended Plugin Stack

| Plugin | Category | Required For Slice 0/1? | Status | Notes |
|---|---|---:|---|---|
| Paper2D | Unreal built-in / 2D rendering | Yes | Planned | Required for 2D sprites, flipbooks, tile/sprite assets |
| PaperZD | Animation framework | Yes | Planned | Core animation stack; must compile/package under UE 5.7 |
| Enhanced Input | Unreal built-in / input | Yes | Planned | Required for modern input mapping and controller support |
| Niagara | Unreal built-in / VFX | Not Slice 1 | Planned | Needed for 2D-compatible VFX after movement proof |
| MetaSounds | Unreal built-in / audio | Not Slice 1 | Planned | Needed for Choir Resonance beat clock and reactive score |
| World Partition | Unreal built-in / world streaming | No | Deferred | Do not enable for first tiny test rooms unless needed |

---

## 3. FAB / Marketplace Plugin Register

Add all locally installed plugins here after the `.uproject` is created or committed.

| Plugin Name | Source | Enabled In `.uproject` | Version | UE 5.7 Compatible | Required For | Slice Priority | Risk | Decision |
|---|---|---:|---|---:|---|---|---|---|
| TBD | FAB | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

### Slice Priority Values

- `Required-Slice-0`
- `Required-Slice-1`
- `Required-Slice-2`
- `Required-Slice-3`
- `Useful-Later`
- `Asset-Only`
- `Deferred`
- `Rejected`

### Risk Values

- `Low`
- `Medium`
- `High`
- `Critical`
- `Unknown`

---

## 4. Plugin Decision Rules

1. **Gameplay core cannot depend on unknown plugin behavior.**
   - Grapple, movement, combat, save/load, consume, and progression must remain portable.

2. **Art/content plugins may be used earlier than gameplay plugins.**
   - Asset packs and editor tooling are less risky than runtime systems.

3. **PaperZD is allowed to be core, but must be verified early.**
   - The first PaperZD proof must include compile, editor play, and packaging check.

4. **Do not leave experimental plugins enabled by default.**
   - If a plugin is only for testing, document it as such.

5. **Every required plugin needs an uninstall fallback note.**
   - If a plugin breaks on another machine, the project needs to explain what fails and what can be disabled.

---

## 5. Required Verification Per Plugin

| Verification | Pass Condition | Status |
|---|---|---|
| Plugin appears in `.uproject` | Enabled state is documented | Open |
| Editor launches | No plugin startup error | Open |
| C++ compile succeeds | No compile/link errors caused by plugin | Open |
| PIE test succeeds | Plugin does not crash during play-in-editor | Open |
| Package/build test succeeds | Plugin does not block packaged build | Open |
| Runtime dependency documented | Gameplay/content impact is known | Open |

---

## 6. Known Plugin Risks

| ID | Plugin | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|---|
| PR-001 | PaperZD | UE 5.7 compatibility or packaging issue | Critical | Verify in Slice 0 before animation-heavy work | Open |
| PR-002 | Unknown FAB plugins | Local install works but repo/project portability fails | High | Reconcile `.uproject`; document each plugin | Open |
| PR-003 | Asset-pack plugins | Content imports inflate repo or create broken references | Medium | Intake assets deliberately; do not dump all content | Open |

---

## 7. Next Action

Once the Unreal project is created, paste or commit the `.uproject` file. Then update this register with every plugin listed under the `.uproject` `Plugins` array.
