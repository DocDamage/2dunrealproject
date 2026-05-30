# Nocturne Signal — Plugin Register

**Purpose:** Track every Unreal Engine, PaperZD, Paper2D, FAB, marketplace, and project plugin used by Nocturne Signal.

**Rule:** Do not rely on any plugin until it is listed here with compatibility, purpose, risk, and slice priority.

---

## 1. Plugin Intake Status

| Field | Value |
|---|---|
| Engine Target | Unreal Engine 5.7 |
| Current `.uproject` available in repo | Yes |
| Local FAB plugins installed by Doc | Yes |
| Plugin reconciliation complete | Partial |
| Current status | Starter `.uproject` committed; waiting for exact local plugin identifiers for FAB plugins |

---

## 2. Core Intended Plugin Stack

| Plugin | Category | Required For Slice 0/1? | Status | Notes |
|---|---|---:|---|---|
| Paper2D | Unreal built-in / 2D rendering | Yes | Added to `.uproject` | Required for 2D sprites, flipbooks, tile/sprite assets |
| PaperZD | Animation framework | Yes | Required, not yet added | Core animation stack; exact plugin identifier must be confirmed locally before adding |
| Enhanced Input | Unreal built-in / input | Yes | Added to `.uproject` | Required for modern input mapping and controller support |
| Pasma Engine: Neural Hair Dynamics | FAB / ZOAZ | Yes, for tentacle/limb dynamics evaluation | Required-unresolved | Listing says it uses Unreal NNE and exposes Blueprint control; exact `.uproject` plugin `Name` unknown |
| Tentacles VFX | FAB / Vefects | Yes, for grapple/tentacle presentation | Required-unresolved | Listing describes semi-procedural tentacle Blueprint behaviours and customizable VFX; exact `.uproject` plugin `Name` unknown |
| Unreal Neural Network Engine / NNE | Unreal built-in dependency | Required if Pasma is used | Required-unresolved | Pasma listing says it requires Unreal's native NNE plugin; exact `.uproject` plugin `Name` must be confirmed locally |
| Niagara | Unreal built-in / VFX | Not Slice 1 unless plugin needs it | Planned | Needed for 2D-compatible VFX after movement proof |
| MetaSounds | Unreal built-in / audio | Not Slice 1 | Planned | Needed for Choir Resonance beat clock and reactive score |
| World Partition | Unreal built-in / world streaming | No | Deferred | Do not enable for first tiny test rooms unless needed |

---

## 3. FAB / Marketplace Plugin Register

These are the known local plugin requirements from Doc. The exact Unreal plugin identifiers still need to be copied from the local project or plugin `.uplugin` files.

| Plugin Name | Source | Listing URL | Enabled In `.uproject` | Version | UE 5.7 Compatible | Required For | Slice Priority | Risk | Decision |
|---|---|---|---:|---|---:|---|---|---|---|
| Pasma Engine: Neural Hair Dynamics | FAB / ZOAZ | `https://www.fab.com/listings/3e707339-09bf-416d-838b-bd91777267b7` | No | Unknown | Unknown | Vestige Limb / tentacle dynamics evaluation | Required-Slice-1 | High | Required, but do not add until exact plugin identifier is known |
| Tentacles VFX | FAB / Vefects | `https://www.fab.com/listings/2301965d-18e8-4df5-8613-a4cebd7915de` | No | Unknown | Unknown | Grapple/tentacle VFX and limb presentation | Required-Slice-1 | High | Required, but do not add until exact plugin identifier is known |

### Confirmed Listing Notes

#### Pasma Engine: Neural Hair Dynamics

Source listing notes:

- Built for Unreal Engine.
- Uses Unreal's native Neural Network Engine / NNE.
- Provides a Pasma Hair Dynamics Component.
- Exposes Blueprint controls.
- Supports Windows PC according to the listing.
- Code type is listed as C++ and Blueprints.

Implication for Nocturne Signal:

- Treat Pasma as a candidate secondary-motion/dynamics layer for Vestige Limbs.
- Do not make grapple targeting or movement dependent on Pasma.
- Verify whether the hair dynamics component can be repurposed for limb/tentacle behavior before production reliance.

#### Tentacles VFX

Source listing notes:

- Describes a semi-procedural tentacle anomaly.
- Includes Blueprint behaviours.
- Includes sound effects.
- Customizable shapes, colors, speeds, and materials.
- Intended as VFX/content and learning material.

Implication for Nocturne Signal:

- Treat Tentacles VFX as the first candidate for Vestige Limb visual presentation.
- Do not assume it solves gameplay collision, grapple state, or traversal physics.
- Best early use is as a visual adapter/fallback candidate for limb extension, coiling, and contact VFX.

---

## 4. Information Needed From Local IDE

For each plugin, capture:

```text
Plugin display name
Plugin folder name
.uplugin file name
Exact .uproject Plugins[].Name value
Installed version
Whether the plugin is Engine-level or Project-level
Whether it contains runtime modules, editor modules, content only, or both
```

The most important field is the exact value Unreal expects here:

```json
{ "Name": "ExactPluginIdentifier", "Enabled": true }
```

Do not guess this value.

---

## 5. Slice Priority Values

- `Required-Slice-0`
- `Required-Slice-1`
- `Required-Slice-2`
- `Required-Slice-3`
- `Useful-Later`
- `Asset-Only`
- `Deferred`
- `Rejected`

## 6. Risk Values

- `Low`
- `Medium`
- `High`
- `Critical`
- `Unknown`

---

## 7. Plugin Decision Rules

1. **Gameplay core cannot depend on unknown plugin behavior.**
   - Grapple, movement, combat, save/load, consume, and progression must remain portable.

2. **Tentacle plugin support should be integrated through an adapter boundary.**
   - Core grapple targeting, movement, and state transitions should live in Nocturne code.
   - Plugin-specific tentacle simulation/VFX should be called from a wrapper/component layer after compatibility is proven.

3. **Art/content plugins may be used earlier than gameplay plugins.**
   - Asset packs and editor tooling are less risky than runtime systems.

4. **PaperZD is allowed to be core, but must be verified early.**
   - The first PaperZD proof must include compile, editor play, and packaging check.

5. **Do not leave experimental plugins enabled by default.**
   - If a plugin is only for testing, document it as such.

6. **Every required plugin needs an uninstall fallback note.**
   - If a plugin breaks on another machine, the project needs to explain what fails and what can be disabled.

---

## 8. Required Verification Per Plugin

| Verification | Pass Condition | Status |
|---|---|---|
| Plugin appears in `.uproject` | Enabled state is documented | Partial |
| Editor launches | No plugin startup error | Open |
| C++ compile succeeds | No compile/link errors caused by plugin | Open |
| PIE test succeeds | Plugin does not crash during play-in-editor | Open |
| Package/build test succeeds | Plugin does not block packaged build | Open |
| Runtime dependency documented | Gameplay/content impact is known | Open |

---

## 9. Known Plugin Risks

| ID | Plugin | Risk | Severity | Mitigation | Status |
|---|---|---|---|---|---|
| PR-001 | PaperZD | UE 5.7 compatibility or packaging issue | Critical | Verify in Slice 0 before animation-heavy work | Open |
| PR-002 | Unknown FAB plugins | Local install works but repo/project portability fails | High | Reconcile `.uproject`; document each plugin | In Progress |
| PR-003 | Asset-pack plugins | Content imports inflate repo or create broken references | Medium | Intake assets deliberately; do not dump all content | Open |
| PR-004 | Pasma Engine: Neural Hair Dynamics | Runtime dynamics plugin may not expose APIs suitable for 2D tentacle grapple | High | Verify module/API in IDE; use adapter layer; keep core grapple portable | Open |
| PR-005 | Tentacles VFX | VFX plugin may solve presentation but not gameplay collision/state | High | Treat as visual layer until runtime behavior is proven | Open |
| PR-006 | Plugin identifier mismatch | Wrong `.uproject` plugin name will prevent project launch | Critical | Do not add guessed plugin IDs; copy exact identifier from local `.uplugin` | In Progress |
| PR-007 | NNE dependency | Pasma may require a specific Unreal NNE plugin/module that is not enabled by default | High | Confirm exact NNE plugin identifier locally; enable only after verified | Open |

---

## 10. Tentacle Plugin Integration Plan

The Vestige Limb grapple should be split into two layers:

### Core Gameplay Layer

Owned by Nocturne code:

- Anchor detection
- Range validation
- Grapple state machine
- Pull-to-Point movement
- Swing movement
- Chain counter
- Consume/grip routing
- SaveGame/progression interaction

### Plugin Presentation/Dynamics Layer

Owned by plugin adapter components after verification:

- Tentacle mesh/spline deformation
- Limb extension/retraction presentation
- Hair/tentacle secondary motion
- Impact/contact visual behavior
- Niagara/VFX hooks if needed

This prevents the project from becoming blocked if a visual plugin fails to package or lacks the expected runtime API.

Planned adapter concept:

```text
UVestigeLimbComponent
  -> owns gameplay state
  -> calls UVestigeTentacleVisualAdapter when present

UVestigeTentacleVisualAdapter
  -> wraps Pasma/Tentacles plugin-specific calls
  -> can be replaced by a simple spline/debug-line fallback
```

---

## 11. Next Action

Open the local plugin folder or `.uproject` after enabling the two FAB plugins and record the exact plugin identifiers. Then update `NocturneSignal.uproject` with the correct plugin names.
