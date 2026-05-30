# Tentacle Plugin Reconciliation Guide

**Purpose:** Capture the exact local Unreal plugin identifiers for the two Fab plugins Doc identified as required for the Vestige Limb grapple presentation layer.

Known products:

| Product | Seller | Fab URL | Project Role |
|---|---|---|---|
| Pasma Engine: Neural Hair Dynamics | ZOAZ | `https://www.fab.com/listings/3e707339-09bf-416d-838b-bd91777267b7` | Candidate dynamics/secondary motion layer for Vestige Limbs |
| Tentacles VFX | Vefects | `https://www.fab.com/listings/2301965d-18e8-4df5-8613-a4cebd7915de` | Candidate tentacle/limb VFX presentation layer |

---

## 1. Required Local Information

Do not guess plugin names. Unreal needs the exact internal plugin identifier from the `.uplugin` file or from the local `.uproject` after enabling the plugin.

For each plugin, record:

```text
Display Name:
Fab Product Name:
Plugin Folder Name:
.uplugin File Name:
Exact .uproject Plugin Name:
Installed Engine Version:
Installed Plugin Version:
Engine-Level or Project-Level:
Contains Runtime Module: Yes/No
Contains Editor Module: Yes/No
Contains Content: Yes/No
Requires Additional Plugins:
```

---

## 2. How to Find the Exact Plugin Name

### Option A — From Unreal Editor

1. Open the project in Unreal.
2. Go to `Edit > Plugins`.
3. Search for the plugin display name.
4. Enable the plugin.
5. Restart Unreal if prompted.
6. Open `NocturneSignal.uproject` in a text editor.
7. Copy the exact value under the `Plugins` array.

Example format:

```json
{
  "Name": "ExactPluginIdentifierHere",
  "Enabled": true
}
```

### Option B — From Plugin Folder

Look in likely locations:

```text
C:/Program Files/Epic Games/UE_5.7/Engine/Plugins/Marketplace/
<YourProject>/Plugins/
```

Open the plugin’s `.uplugin` file and copy the top-level `FriendlyName`, `VersionName`, and module names.

The `.uproject` usually uses the `.uplugin` file name without extension, but verify this locally instead of assuming.

---

## 3. Nocturne Integration Rule

These plugins must not own the gameplay state machine.

Core gameplay remains in:

```text
UVestigeLimbComponent
AGrappleAnchor
ANocturnePlayerCharacter
```

Plugin presentation belongs behind:

```text
UVestigeTentacleVisualAdapter
```

Blueprint subclasses can connect Pasma/Tentacles VFX to adapter events:

```text
OnGrappleSearchStarted
OnGrappleAnchorSelected
OnGrappleExtendStarted
OnGrapplePullStarted
OnGrappleReleased
OnGrappleCancelled
UpdateLimbTarget
```

---

## 4. First Verification Pass

After enabling each plugin, run this checklist:

| Check | Pass Condition | Status |
|---|---|---|
| Editor launch | Project opens without plugin error | Open |
| Plugin appears in `.uproject` | Exact plugin identifier captured | Open |
| C++ compile | `NocturneSignalEditor` builds | Open |
| PIE smoke test | Empty map runs | Open |
| Blueprint subclass | Can create a subclass of `UVestigeTentacleVisualAdapter` | Open |
| Runtime event test | Adapter receives grapple events | Open |
| Package check | Plugin does not block packaging | Open |

---

## 5. Fallback Plan

If either plugin fails:

1. Keep core grapple gameplay active.
2. Use `UVestigeTentacleVisualAdapter` fallback debug line.
3. Replace with a simple spline/mesh visual adapter.
4. Revisit plugin integration after Slice 1 movement proof.

The project should never become blocked because the visual tentacle layer fails. The grapple must still work.
