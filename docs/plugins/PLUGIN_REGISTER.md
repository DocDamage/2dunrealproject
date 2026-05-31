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
| Current status | Current `.uproject` plugin identifiers resolve locally; Pasma and other marketplace/editor helpers are enabled and still need compile/editor verification |

---

## 2. Core Intended Plugin Stack

| Plugin | Category | Required For Slice 0/1? | Status | Notes |
|---|---|---:|---|---|
| Paper2D | Unreal built-in / 2D rendering | Yes | Added to `.uproject` | Required for 2D sprites, flipbooks, tile/sprite assets |
| PaperZD | Animation framework | Yes | Enabled in `.uproject`; compile verification blocked by active Live Coding session | Exact plugin identifier: `PaperZD`; installed version 2.2.3 for UE 5.7 |
| Enhanced Input | Unreal built-in / input | Yes | Added to `.uproject` | Required for modern input mapping and controller support |
| Pasma Engine: Neural Hair Dynamics | FAB / ZOAZ | Yes, for tentacle/limb dynamics evaluation | Enabled locally; unverified | Exact plugin identifier: `Pasma_Engine_Neural_Hair_Dynamics`; experimental Win64 plugin; keep core gameplay independent |
| Tentacles VFX | FAB / Vefects | Yes, for grapple/tentacle presentation | Content found locally; plugin descriptor not found | `RogueCharacterModel\Content\Vefects\Tentacles_VFX` exists, but no `.uplugin` descriptor was found under UE 5.7 Marketplace plugins, VaultCache, or the nested content folder |
| Unreal Neural Network Engine / NNE | Unreal built-in dependency | Required if Pasma is used | Required dependency | Pasma depends on `NNERuntimeORT` |
| Niagara | Unreal built-in / VFX | Required by PaperZD plugin dependency | Enabled in `.uproject` | Also needed for 2D-compatible VFX after movement proof |
| MetaSounds | Unreal built-in / audio | Not Slice 1 | Planned | Needed for Choir Resonance beat clock and reactive score |
| World Partition | Unreal built-in / world streaming | No | Deferred | Do not enable for first tiny test rooms unless needed |

---

## 3. FAB / Marketplace Plugin Register

These are the known local plugin requirements from Doc and the installed UE 5.7 Marketplace descriptors.

| Plugin Name | Exact `.uproject` Name | Source | Enabled In `.uproject` | Version | UE 5.7 Compatible | Required For | Slice Priority | Risk | Decision |
|---|---|---|---:|---|---:|---|---|---|---|
| PaperZD | `PaperZD` | FAB / Critical Failure Studio | Yes | 2.2.3 | Descriptor targets 5.7.0 | 2D animation graph and notifies | Required-Slice-1 | Critical | Enabled; verify after Live Coding is closed |
| Pasma Engine: Neural Hair Dynamics | `Pasma_Engine_Neural_Hair_Dynamics` | FAB / ZOAZ | Yes | 1.0.0 | Descriptor targets 5.7.0 Win64 | Vestige Limb / tentacle dynamics evaluation | Required-Slice-1 | High | Enabled locally; verify before relying on it |
| Tentacles VFX | Unknown | FAB / Vefects | No | Unknown | Unknown | Grapple/tentacle VFX and limb presentation | Required-Slice-1 | High | Content found under `RogueCharacterModel\Content\Vefects\Tentacles_VFX`; descriptor not found, so do not add guessed plugin name |

## 3A. Current `.uproject` Enabled Plugins

| Plugin Name | Reason / Status |
|---|---|
| `Paper2D` | Core 2D sprite/flipbook support |
| `PaperZD` | Core 2D animation framework; verification pending Live Coding shutdown |
| `Niagara` | PaperZD dependency and planned VFX support |
| `EnhancedInput` | Input mapping and controller support |
| `ActorModifier` | Enabled locally; not a core gameplay dependency yet |
| `ActorModifierCore` | Enabled locally; not a core gameplay dependency yet |
| `ActorPalette` | Enabled locally; editor/asset workflow candidate |
| `GameplayBehaviors` | Enabled locally; not a first-slice dependency yet |
| `TargetingSystem` | Enabled locally; possible future combat targeting support |
| `SurfaceEffects` | Enabled locally; not a first-slice dependency yet |
| `SQLiteSupport` | Enabled locally; not a first-slice dependency yet |
| `Paper2DPlus` | Enabled locally; Paper2D helper plugin |
| `DayNightSystem` | Enabled locally; likely not needed for first interior slice |
| `Pasma_Engine_Neural_Hair_Dynamics` | Enabled locally; high-risk experimental runtime/editor plugin |
| `LingotionThespeon` | Enabled locally; TTS/audio plugin, not a first-slice dependency |
| `LocoHelperAI` | Enabled locally; editor helper plugin, not a runtime design dependency |
| `AnimationWarping` | Enabled locally; likely relevant only for 3D/retarget experiments |
| `UnrealMCPBridge` | Enabled locally; Unreal Editor TCP bridge for Codex/MCP tooling |

### Unreal MCP Bridge

Installed project plugin:

```text
F:\Nocturne Signal\2dunrealproject\Plugins\UnrealMCPBridge
```

Exact `.uproject` plugin name:

```json
{ "Name": "UnrealMCPBridge", "Enabled": true }
```

Editor bridge endpoint:

```text
127.0.0.1:30020
```

Local Codex MCP wrapper:

```text
C:\Users\Doc\.codex\external\ue5-mcp-bridge-mcp
```

Local Codex MCP command configured on this machine:

```toml
[mcp_servers.unreal-mcp-bridge]
command = "uv"
args = ["--directory", "C:\\Users\\Doc\\.codex\\external\\ue5-mcp-bridge-mcp", "run", "ue5_mcp_bridge_server.py"]
```

Notes:

- The bridge is a UE editor plugin, not a standalone stdio MCP server, so Codex uses a small local wrapper that forwards MCP tool calls to the editor TCP bridge.
- Unreal Editor must be restarted after enabling the plugin so it can compile/load and listen on port `30020`.
- Codex must be restarted before the new `unreal-mcp-bridge` MCP server appears in the active tool list.

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

Local status:

- Content exists under `F:\Nocturne Signal\2dunrealproject\RogueCharacterModel\Content\Vefects\Tentacles_VFX`.
- No `.uplugin` descriptor was found in the nested content folder, UE 5.7 Marketplace plugin folders, or VaultCache.
- Treat this as local VFX/content intake until a plugin descriptor is found.

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
| PR-001 | PaperZD | UE 5.7 compatibility or packaging issue | Critical | Verify in Slice 0 before animation-heavy work | In Progress |
| PR-002 | Unknown FAB plugins | Local install works but repo/project portability fails | High | Reconcile `.uproject`; document each plugin | In Progress |
| PR-003 | Asset-pack plugins | Content imports inflate repo or create broken references | Medium | Intake assets deliberately; do not dump all content | Open |
| PR-004 | Pasma Engine: Neural Hair Dynamics | Runtime dynamics plugin may not expose APIs suitable for 2D tentacle grapple | High | Verify module/API in IDE; use adapter layer; keep core grapple portable | In Progress |
| PR-005 | Tentacles VFX | Local content exists, but no plugin descriptor has been found and it may solve presentation but not gameplay collision/state | High | Treat as visual/content layer until runtime behavior is proven; do not add guessed `.uproject` plugin names | In Progress |
| PR-006 | Plugin identifier mismatch | Wrong `.uproject` plugin name will prevent project launch | Critical | Do not add guessed plugin IDs; copy exact identifier from local `.uplugin` | In Progress; PaperZD and Pasma identifiers confirmed |
| PR-007 | NNE dependency | Pasma requires `NNERuntimeORT` | High | Confirm compile/editor launch with Pasma enabled | In Progress |
| PR-008 | Unreal MCP bridge not attached | Plugin is installed but Codex may not expose the MCP tools until host config/reload and editor restart | Medium | Enable `UnrealMCPBridge`, configure the local Codex wrapper, restart Codex, then launch the editor and verify `127.0.0.1:30020` is listening | Verified; MCP ping, project query, and Jacob asset queries pass against UE 5.7.4 |

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

Close the active Unreal Live Coding/editor session, then rebuild `NocturneSignalEditor` to verify the current enabled plugin set, especially Pasma, Lingotion, Loco, Paper2DPlus, DayNightSystem, AnimationWarping, and UnrealMCPBridge. After the editor launches with UnrealMCPBridge enabled, restart Codex and verify the `unreal-mcp-bridge` MCP tools can ping the editor.
