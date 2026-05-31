# Nocturne Signal

A 2D gothic science-fantasy metroidvania built for Unreal Engine 5.7.

The project targets a polished first playable slice proving SOTN-style player feel, Vestige Limb traversal/combat, PaperZD animation workflow, Signal Corruption, Relics, SaveGame persistence, and the Reliquary of Waking vertical slice.

---

## Current Status

Active pre-production / first playable slice setup.

The repository now contains the starter Unreal C++ project scaffold for Slice 1. Documentation remains the source of truth for scope, plugin intake, and asset intake decisions.

---

## Start Here

| File | Purpose |
|---|---|
| `PROJECT_MANIFEST.md` | Main repository source of truth |
| `docs/README.md` | Documentation index |
| `docs/plugins/PLUGIN_REGISTER.md` | Unreal/FAB plugin tracking |
| `docs/asset-intake/ASSET_INTAKE_MANIFEST.md` | Asset intake policy and archive register |
| `docs/asset-intake/ASSET_INVENTORY_SUMMARY.md` | Generated inventory summary from uploaded archives |
| `docs/architecture/ARCHITECTURE_DECISIONS.md` | Architecture decision record |
| `docs/slice-00/SLICE_00_TOOLCHAIN_AND_INTAKE.md` | Slice 0 plan |
| `docs/slice-01/SLICE_01_PLAYER_AND_GRAPPLE.md` | Slice 1 player/grapple plan |
| `docs/risks/RISK_REGISTER.md` | Active risk register |
| `docs/verification/VERIFICATION_MATRIX.md` | Verification gates |

---

## Locked Decisions

- Unreal Engine 5.7 target.
- C++ gameplay core with Blueprint/PaperZD content wiring.
- SOTN-style grounded movement feel.
- Vestige Limb system is the current traversal/combat/progression authority.
- Character art will be added later in IDE.
- FAB plugins are installed locally and must be reconciled from the `.uproject` file.
- First implementation target: Slice 0 toolchain/intake, then Slice 1 player movement + Pull-to-Point grapple.

---

## First Playable Slice

The first playable slice is the Reliquary of Waking.

Early focus:

1. Toolchain and plugin verification.
2. Controlled asset intake.
3. Player movement test room.
4. Vestige Pull-to-Point grapple.
5. Swing and chain grapple.
6. Combat test room with Failed Waker, Bonespike, and consume threshold.

---

## Repository Rule

Do not dump assets or plugin assumptions directly into production folders.

Every major addition needs:

- Purpose
- Source/design basis
- Slice priority
- Risk status
- Verification method

Build the Reliquary. Make Veyra feel excellent. Prove the Vestige Limb. Then scale.
