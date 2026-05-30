# Slice 1 — IDE Setup Guide

**Purpose:** Give the local IDE/Unreal setup steps needed to compile and test the current Slice 1 scaffold.

---

## 1. Required Manual Patch

The GitHub connector blocked creation of:

```text
Source/NocturneSignal/NocturneSignal.Build.cs
```

Create it manually before compiling. The exact content is in:

```text
docs/slice-01/MANUAL_BUILD_CS_PATCH.md
```

Without this file, Unreal project generation and C++ compile will fail.

---

## 2. Pull / Clone

Clone or pull:

```text
https://github.com/DocDamage/2dunrealproject
```

Open the repo root. Confirm these exist:

```text
NocturneSignal.uproject
Source/NocturneSignal.Target.cs
Source/NocturneSignalEditor.Target.cs
Source/NocturneSignal/Public/
Source/NocturneSignal/Private/
```

---

## 3. Regenerate Project Files

After adding `NocturneSignal.Build.cs` manually:

1. Right-click `NocturneSignal.uproject`.
2. Select `Generate Visual Studio project files` or the matching IDE generation option.
3. Open the generated solution/project.
4. Build `NocturneSignalEditor`.

---

## 4. First Compile Expectations

Current source scaffold includes:

```text
ANocturnePlayerCharacter
UVestigeLimbComponent
UVestigeTentacleVisualAdapter
AGrappleAnchor
```

The expected first compile result is not a playable game yet. It should prove:

- Module loads.
- C++ reflection succeeds.
- Player/grapple classes appear in Unreal.
- Blueprint subclasses can be created from these classes.

---

## 5. Plugin Setup Order

Use this order:

1. Compile without Fab tentacle plugins first.
2. Confirm `NocturneSignalEditor` builds.
3. Open Unreal.
4. Enable PaperZD locally if installed.
5. Enable Pasma Engine and Tentacles VFX locally.
6. Copy exact plugin identifiers into `docs/plugins/PLUGIN_REGISTER.md`.
7. Add exact plugin identifiers to `NocturneSignal.uproject` only after confirming them.
8. Rebuild.

Do not add guessed plugin names to `.uproject`.

---

## 6. Slice 1 Blueprint Setup

After compile:

### Player Blueprint

Create:

```text
Content/NocturneSignal/Characters/Veyra/BP_NocturnePlayerCharacter
```

Parent class:

```text
ANocturnePlayerCharacter
```

For placeholder art, use any temporary sprite/flipbook or a simple visible component. Final Veyra art can be added later.

### Grapple Anchor Blueprint

Create:

```text
Content/NocturneSignal/Blueprints/Grapple/BP_GrappleAnchor_Architecture
```

Parent class:

```text
AGrappleAnchor
```

Set:

```text
AnchorType = Architecture
RequiredStage = 1
RequiredCorruption = 0.0
bIsActive = true
```

### Visual Adapter Blueprint

Create:

```text
Content/NocturneSignal/Blueprints/Vestige/BP_VestigeTentacleVisualAdapter_Debug
```

Parent class:

```text
UVestigeTentacleVisualAdapter
```

Attach this component to the player Blueprint if you want fallback debug visual events before the Fab plugins are wired.

---

## 7. Test Map Setup

Create:

```text
Content/NocturneSignal/Maps/TestRooms/LV_Test_GrapplePullToPoint
```

Minimum layout:

- Flat floor.
- One low platform.
- One medium platform.
- One high platform.
- Three `BP_GrappleAnchor_Architecture` actors.
- Player start.

Do not use final art yet. Use simple blocks if needed.

---

## 8. Input Wiring

Slice 1 can bind input in Blueprint first.

Call these functions on the player:

```text
MoveHorizontal(float AxisValue)
StartJump()
StopJump()
TryVestigeGrapple()
```

Recommended temporary controls:

| Action | Keyboard | Controller |
|---|---|---|
| Move | A/D or Left/Right | Left Stick |
| Jump | Space | Face Button Bottom |
| Grapple | E or Right Mouse | Right Shoulder / Trigger |

Enhanced Input assets should eventually live under:

```text
Content/NocturneSignal/Input/
```

---

## 9. First Runtime Tests

Run these tests before adding enemies or combat:

| Test | Expected Result |
|---|---|
| Player spawn | Player appears and accepts movement input |
| Horizontal move | Character moves left/right on 2D plane |
| Jump | Character jumps and lands reliably |
| Grapple in range | Player pulls to nearest valid anchor |
| Grapple out of range | Grapple fails cleanly |
| Debug line | Limb/anchor debug line appears during grapple |
| Adapter event | Visual adapter receives state events if attached |
| Camera | No hard snap during pull |

---

## 10. Known Blockers

| Blocker | Impact | Action |
|---|---|---|
| `NocturneSignal.Build.cs` not committed | Compile fails | Create manually from patch doc |
| Exact Fab plugin IDs unknown | Cannot enable plugins safely in repo | Capture from local `.uplugin` files |
| Final Veyra art not in repo | Placeholder visuals only | Add in IDE later |
| No map assets committed yet | Test map must be made locally | Use placeholder geometry first |

---

## 11. Success Definition

Slice 1 succeeds when:

- The project compiles.
- A player Blueprint can be made from `ANocturnePlayerCharacter`.
- Grapple anchors can be placed.
- Pull-to-Point grapple works in a test map.
- The visual adapter receives events.
- The camera is stable enough to continue to swing grapple.
