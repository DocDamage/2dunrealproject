# Nocturne Signal — Documentation Index

This folder contains project control documents for the Nocturne Signal Unreal Engine 5.7 vertical slice.

The repository must stay documentation-first. Gameplay systems, assets, plugins, and level content should be added only after their purpose, risk, and verification path are recorded.

---

## Source of Truth

Primary authority documents are currently stored outside the repo as uploaded design files:

1. `NOCTURNE_SIGNAL_ENHANCED_DESIGN_v0.2.md`
2. `NOCTURNE_SIGNAL_AMENDMENT_0003_VESTIGE_LIMB.md`

Until a combined `NS-MP-0004` document exists, use this rule:

- Enhanced Design Document = world, story, production plan, phase structure, audio direction, systems list.
- Vestige Limb Amendment = current player traversal, combat, progression, consume, and weapon-form authority.
- Amendment wins wherever the two conflict.

---

## Documentation Map

| Path | Purpose |
|---|---|
| `../PROJECT_MANIFEST.md` | Repo-level source of truth, locked decisions, and first-slice direction |
| `plugins/PLUGIN_REGISTER.md` | Required, optional, risky, and deferred Unreal/FAB plugin tracking |
| `asset-intake/ASSET_INTAKE_MANIFEST.md` | Zip intake, classification, first-slice asset selection, and import decisions |
| `architecture/ARCHITECTURE_DECISIONS.md` | Engineering decisions and accepted tradeoffs |
| `slice-00/SLICE_00_TOOLCHAIN_AND_INTAKE.md` | Toolchain, repo, plugin, and asset intake work package |
| `slice-01/SLICE_01_PLAYER_AND_GRAPPLE.md` | Player controller and Vestige Pull-to-Point grapple work package |
| `risks/RISK_REGISTER.md` | Active risk tracking |
| `verification/VERIFICATION_MATRIX.md` | System verification gates and proof requirements |

---

## Production Rules

1. Do not import every asset blindly.
2. Do not build level content before movement scale and grapple scale are tested.
3. Do not mark systems Verified without a build, runtime test, automated test, packaging pass, or clear manual inspection.
4. Do not build core gameplay around a plugin until the plugin is confirmed compatible with Unreal Engine 5.7.
5. Keep prototype, production, and polish work separated.
6. Every new gameplay system needs a verification method before it is considered complete.

---

## Current First Pass

The immediate sequence is:

1. Slice 0 — Toolchain and asset intake.
2. Slice 1 — Player movement and Pull-to-Point Vestige grapple.
3. Slice 2 — Swing and chain grapple.
4. Slice 3 — Combat room, Failed Waker, Bonespike, and consume threshold.

The priority is game feel. The first real proof of the project is whether Veyra feels excellent to control.
