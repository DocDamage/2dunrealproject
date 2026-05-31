# Slice 0 — Toolchain and Asset Intake

**Project:** Nocturne Signal  
**Slice:** 0  
**Status:** In Progress
**Goal:** Establish the repo, documentation, plugin, and asset intake foundation before Unreal gameplay work expands.

---

## 1. Objective

Slice 0 exists to prevent the project from becoming a messy Unreal folder.

This slice proves that the project has:

- A documented source of truth.
- A clean plugin intake process.
- A controlled asset intake process.
- A first-slice scope boundary.
- A verification discipline before gameplay coding begins.

Slice 0 does not need polished gameplay. It prepares the conditions for reliable gameplay work.

---

## 2. Deliverables

| ID | Deliverable | Status | Verification |
|---|---|---|---|
| S0-D001 | `PROJECT_MANIFEST.md` | Fixed | File exists in repo |
| S0-D002 | Documentation index | Fixed | `docs/README.md` exists |
| S0-D003 | Plugin register template | Fixed | `docs/plugins/PLUGIN_REGISTER.md` exists |
| S0-D004 | Asset intake manifest template | Fixed | `docs/asset-intake/ASSET_INTAKE_MANIFEST.md` exists |
| S0-D005 | Architecture decision record | Fixed | `docs/architecture/ARCHITECTURE_DECISIONS.md` exists |
| S0-D006 | Risk register | Fixed | `docs/risks/RISK_REGISTER.md` exists |
| S0-D007 | Verification matrix | Fixed | `docs/verification/VERIFICATION_MATRIX.md` exists |
| S0-D008 | Controlled asset decompression | Open | Archives extracted outside Unreal `Content/` |
| S0-D009 | Asset inventory report | Open | Inventory generated and linked here |
| S0-D010 | `.uproject` plugin reconciliation | Fixed | Starter `.uproject` exists; enabled plugins are documented, FAB plugin identifiers still pending |

---

## 3. Inputs

Required inputs:

- Uploaded design documents.
- Uploaded asset archives.
- GitHub repository access.
- Unreal Engine 5.7 project scaffold.
- Local FAB plugin list once exact plugin identifiers are available.

---

## 4. Current Locked Decisions

| Area | Decision |
|---|---|
| Core architecture | C++ gameplay core, Blueprint/PaperZD content wiring |
| Movement target | SOTN-style grounded movement |
| Character art | Doc will add character art later in IDE |
| First prototype | Player movement + Pull-to-Point Vestige grapple |
| Asset workflow | Inventory first; import only selected first-slice assets |
| Plugin workflow | Reconcile plugins from `.uproject`; do not assume unknown FAB plugin APIs |

---

## 5. Asset Intake Work Package

### Step 1 — Decompress to Temporary Intake Folder

Recommended session/local structure:

```text
nocturne_asset_intake/
  raw_archives/
  extracted/
  inventory/
  first_slice_candidates/
```

Do not extract into the Unreal project.

### Step 2 — Generate Inventory

Inventory must capture:

- Archive name
- Relative path
- File type
- Image dimensions
- Asset category guess
- Duplicate/similarity notes
- First-slice candidate flag
- Proposed Unreal import path

### Step 3 — Select First-Slice Assets

Required first-slice categories:

- Gothic walls/floors
- Doors/arches
- Coffin/reliquary props
- Columns/structures
- Grapple anchor candidates
- Basic lighting props
- Workshop/mechanism pieces

Defer:

- Town square props
- Nature/gardens/crops
- Market stalls
- Roof tiles
- Dirt paths
- Outdoor street props

### Step 4 — Import Decision

Before Unreal import, decide:

- Texture group
- Pixels-per-unit policy
- Collision policy
- Flipbook/tilemap usage
- Folder path
- Naming convention

---

## 6. Plugin Intake Work Package

Starter `.uproject` reconciliation is complete for currently enabled plugins: Paper2D and Enhanced Input.

For additional local FAB plugins:

1. Read the `.uproject` `Plugins` array.
2. Add every plugin to `docs/plugins/PLUGIN_REGISTER.md`.
3. Mark each plugin as required, useful later, asset-only, risky, deferred, or rejected.
4. Confirm editor launch.
5. Confirm C++ compile.
6. Confirm PIE test.
7. Confirm packaged build when practical.

No core system may depend on an unverified plugin except PaperZD, which is a known planned dependency and must be verified early.

---

## 7. Exit Criteria

Slice 0 can close when:

- Repo manifest exists.
- Documentation scaffold exists.
- Plugin register exists.
- Asset intake manifest exists.
- Risk register exists.
- Verification matrix exists.
- Asset inventory is generated.
- First-slice asset candidates are identified.
- `.uproject` plugin reconciliation is complete or explicitly marked blocked.

---

## 8. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Asset library causes scope creep | High | Only approve first-slice assets initially |
| FAB plugins create portability issues | High | Document and verify from `.uproject` |
| Asset scale inconsistency | Medium | Inventory dimensions before import |
| Unreal folder clutter | Medium | Use `Content/NocturneSignal/...` only |
| PaperZD compatibility unknown | Critical | Compile/package test early |

---

## 9. Handoff to Slice 1

Slice 1 should not begin serious code expansion until Slice 0 has at least:

- Manifest
- Plugin register
- Asset intake manifest
- Risk register
- Verification matrix
- Unreal project created locally or planned clearly

Slice 1 may start with placeholder art and no final character sprites.
