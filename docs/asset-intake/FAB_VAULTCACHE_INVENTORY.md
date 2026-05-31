# Fab VaultCache Inventory

**Source path:** `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\FabLibrary`
**Inventory date:** 2026-05-30
**Rule:** This folder is an intake source only. Do not commit whole VaultCache packs or copied sample projects directly into Nocturne Signal.

---

## 1. Summary

| Source | Count / Size | Notes |
|---|---:|---|
| FabLibrary entries | 25 folders | Mix of FBX assets, animation packs, content packs, and plugin manifests |
| Readable FBX metadata entries | 5 packs | Metadata files include listing title, category, seller, AI flags, and format |
| Expanded VaultCache content projects | 9 folders | Includes RamsterZ, Rogue Character, SurfaceWrap2D, 2d Actor Plus, VFX, and related sample content |
| `.uplugin` files under VaultCache | 0 | Plugin identifiers must come from installed UE plugin folders |
| Current local nested sample project | `RogueCharacterModel/` | Present in repo root as local intake material; ignored by git |
| Current nested sample content | `RogueCharacterModel/Content` | 1,369 files / ~1.67 GB; content-only, no `.uplugin` descriptors found |
| Current direct Fab import | `Content/Fab/Realistic_Combat_Moves_10_Mocap_Pack` | Present locally; small enough for GitHub, but path should be reviewed before commit |
| Current direct content imports | `Content/A_Surface_Footstep`, `Content/LightShaftGenie`, `Content/Vefects`, `Content/RamsterZ_FreeAnims_Volume1` | Present locally; not namespaced under `Content/NocturneSignal` |
| Dedicated animation inventory | `docs/asset-intake/ANIMATION_SOURCE_INVENTORY.md` | Tracks new root animation archives and Fab animation candidates for Jacob |

---

## 2. FabLibrary Folders

| Folder | Type Guess | Size | First-Slice Use | Decision |
|---|---|---:|---|---|
| `2d_Actor_Plus_-_Beta-dcac02ac` | Fab manifest / install metadata | 0.03 MB | Medium | Expanded VaultCache content exists; evaluate through Unreal only |
| `Blend_Poses_By_Gameplay_Tag_-_Gameverse-d0d16502` | Fab manifest / plugin metadata | 0.02 MB | Low | Defer; not needed for current Jacob retarget pass |
| `Crystal_Arsenal_Vol_1_-_24_models-6d0d6074` | FBX weapon models | 377.29 MB | Low | Defer; mostly guns/crystal weaponry, may fit later relic/prop work |
| `Easy_Impact_Frames-15cb7c95` | Fab manifest / VFX content metadata | 0.05 MB | Medium | Expanded VaultCache content exists; local-only until selected |
| `Game_Ready_Stylized_Fantasy_Sword___Curved_Dark_Fantasy_Blade___Low_Poly-74a819ca` | FBX melee weapon | 0.29 MB | Medium | Candidate for placeholder melee prop only |
| `GIFT__Fantasy_Dao_Sword__Kryven_Blade_-_PBR_Game_Ready-0191eee4` | Sword asset package | 33.09 MB | Medium | Candidate for later weapon-form visual reference |
| `Greatsword_of_Ruin-50c22e29` | FBX melee weapon | 0.87 MB | Medium | Candidate for Bonespike/weapon-form visual reference |
| `Lightweight_Day_and_Night_Manager-8700611f` | Unreal plugin/content manifest | 0.02 MB | Low | Defer; not needed for interior slice |
| `Lingotion_Thespeon_-_Real-Time_On-Device_AI_Voice_Acting_Engine__TTS_-7eed6434` | Unreal plugin manifest | 0.20 MB | Low | Defer; audio prototype can use simpler tooling first |
| `Loco_AI_-_AI_assistant_that_builds_Blueprints_inside_UE5-5b1ed262` | Unreal plugin manifest | 0.04 MB | Low | Defer; editor tool, not runtime slice dependency |
| `LOOMLE_MCP_for_Unreal_-_Claude___Codex_for_Blueprint__PCG__Material__Debugging-f0fb545c` | Fab manifest / editor tool metadata | 0.02 MB | Low | Loomle is uninstalled from Codex/project; leave VaultCache cache alone |
| `MatrixRainRuntime_-_Matrix_Rain-9beebfe9` | Unreal plugin manifest | 0.02 MB | Low | Defer; possible later signal/VFX reference |
| `Motifect_Martial_Arts_Motion_Pack-95f5f297` | FBX combat animations | 28.35 MB | High | Candidate after sword locomotion baseline; 40 FBX clips |
| `Niagara_Footstep_VFX__Footstep_VFX__Footstep_Particles_-49dc53b7` | Fab manifest / VFX metadata | 0.20 MB | Medium | Expanded VaultCache content exists; local-only until selected |
| `Paper2D_-7600dc00` | Unreal plugin manifest | 0.07 MB | High | Core 2D dependency already enabled through engine plugin |
| `PaperZD-6664e3b5` | Unreal plugin manifest | 0.08 MB | High | Core animation dependency; exact plugin id confirmed from installed descriptor |
| `Pasma_Engine__Neural_Hair_Dynamics_____AI-3e707339` | Unreal plugin manifest | 0.03 MB | Medium | Candidate Vestige visual/dynamics layer; currently enabled locally and must be compile-verified |
| `RamsterZ_Free_Anims_Volume_1-9319491d` | Animation pack manifest | 0.02 MB | Medium | Candidate for 3D reference/retarget tests, not core 2D animation |
| `Realistic_Combat_Moves___10_Mocap_Pack-6abe0677` | FBX combat animations | 24.19 MB | Medium | Candidate combat reference only; likely not direct 2D production asset |
| `Revolvers___Game_ready_asset__-ca731dc2` | FBX gun models | 14.06 MB | Low | Defer |
| `Rogue_Character_Model-15e2afd1` | Unreal content manifest | 0.12 MB | Medium | Local expanded project exists; evaluate as character reference only |
| `SurfaceWrap2D_2D-on-3D_Game_System-35c04512` | Fab manifest / 2D-on-3D content metadata | 0.01 MB | Medium | Expanded VaultCache content exists; evaluate for prototype support only |
| `Tentacles_VFX-2301965d` | Fab manifest / VFX metadata | 0.04 MB | Medium | Expanded VaultCache content exists; evaluate as selected VFX only |
| `Tether___Tow_Force_Manager-da0efe5b` | Fab manifest / mechanic content metadata | <0.01 MB | Low | Expanded VaultCache content exists; defer |
| `Velocity_Reflect_Launch_System__Blueprint__-_UE5-621cba9c` | Fab manifest / movement mechanic metadata | 0.07 MB | Low | Expanded VaultCache content exists; defer |

---

## 3. Expanded VaultCache Projects

| Path | Contents | Decision |
|---|---|---|
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\2dActorP241a00be4b0aV7` | Unreal content, 128 `.uasset` files | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\EasyImpa76514c37f081V1` | Unreal VFX/content project, 195 `.uasset`, 5 maps | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\NiagaraF1b5e3057df60V2` | Unreal footstep VFX/content project, 322 `.uasset`, 1 `.fbx`, 1 map | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\RamsterZc56ed5072951V1` | Unreal animation pack content | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\RogueCha8adc47a66883V3` | Unreal project/content with `RogueCharacter`, mannequin assets, animations, maps | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\SurfaceW7fe8332053f8V1` | Unreal content, 45 `.uasset`, 2 maps | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\Tentacle377218dbca29V1` | Unreal VFX/content, 117 `.uasset`, 2 maps | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\TetherTo05d694c8559bV1` | Unreal mechanic/content, 7 `.uasset`, 1 map | Intake source only |
| `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\Velocitya7d3676a81d5V1` | Unreal movement/mechanic content, 154 `.uasset`, 2 maps | Intake source only |
| `F:\Nocturne Signal\2dunrealproject\RogueCharacterModel` | Local nested sample project copied into repo root | Ignored by git; do not use as production folder |
| `F:\Nocturne Signal\2dunrealproject\RogueCharacterModel\Content` | Local nested content payload; 1,347 `.uasset`, 16 `.umap`, 5 `.tga`, 1 `.fbx`; no `.uplugin` descriptors | Local-only unless selected assets are migrated intentionally |
| `F:\Nocturne Signal\2dunrealproject\Content\Fab\Realistic_Combat_Moves_10_Mocap_Pack` | Direct Fab import with six `.uasset` files | Small enough for GitHub, but review generic path before commit |

---

## 4. Nested RogueCharacterModel Content

This folder is an intake source inside the repo root, but `RogueCharacterModel/` is ignored by git. Do not commit it as a nested project. Migrate selected assets through Unreal into approved project paths only after they are chosen for a slice.

| Nested Content Folder | Files | Size | Likely Purpose | Intake Decision |
|---|---:|---:|---|---|
| `RogueCharacter` | 223 | 656.97 MB | Character model/reference content | Local-only unless LFS is introduced |
| `VelocityReflectLaunchSystemUE5` | 156 | 391.71 MB | Movement/launch mechanic sample content | Local-only; evaluate mechanics only |
| `A_Surface_Footstep` | 329 | 349.46 MB | Surface footstep/VFX demo content | Local-only; duplicate/related to direct project import |
| `Vefects` | 319 | 265.06 MB | VFX content including `Tentacles_VFX` assets | Local-only; content found, plugin descriptor still not found |
| `RamsterZ_FreeAnims_Volume1` | 72 | 23.23 MB | Animation samples | Commit candidate only if migrated out selectively |
| `SurfaceWrap2D` | 47 | 16.91 MB | 2D surface/wrap support content | Candidate for selective 2D prototype evaluation |
| `2dActorPlusFiles` | 128 | 4.38 MB | 2D actor/helper content | Candidate for selective 2D prototype evaluation |
| `TetherAndTow` | 8 | 0.42 MB | Tether/tow mechanic sample content | Candidate for selective mechanic review |
| `__ExternalActors__` | 75 | 0.30 MB | World partition/external actor data | Keep with source sample only |
| `__ExternalObjects__` | 12 | 0.03 MB | External object data | Keep with source sample only |

Nested content file-type totals:

| Extension | Count | Size |
|---|---:|---:|
| `.uasset` | 1,347 | 1,696.81 MB |
| `.umap` | 16 | 2.84 MB |
| `.tga` | 5 | 0.83 MB |
| `.fbx` | 1 | 7.98 MB |

---

## 5. Current Direct Project Imports

These folders currently exist under `Content/` in the local project. They are useful as evaluation material, but they are not yet organized under the approved `Content/NocturneSignal/...` namespace.

| Content Folder | Files | Size | Likely Purpose | Intake Decision |
|---|---:|---:|---|---|
| `Content/A_Surface_Footstep` | 329 | 348.44 MB | Surface footstep Niagara/VFX demo content and environment test assets | Local-only unless Git LFS is introduced |
| `Content/Vefects` | 200 | 131.64 MB | Easy Impact Frames VFX, shockwaves, demo character/materials/maps | Local-only unless Git LFS is introduced |
| `Content/RamsterZ_FreeAnims_Volume1` | 72 | 23.23 MB | Mannequin combat/gesture animation samples | GitHub commit candidate; reference or retarget test material only |
| `Content/LightShaftGenie` | 23 | 1.95 MB | Light shaft Blueprint/material demo content | GitHub commit candidate |
| `Content/Fab` | 6 | 1.23 MB | Realistic Combat Moves partial import | GitHub commit candidate, but review generic path before commit |

Current imported file-type totals:

| Extension | Count |
|---|---:|
| `.uasset` | 616 |
| `.umap` | 8 |
| `.tga` | 5 |
| `.fbx` | 1 |

---

## 6. Immediate Intake Decisions

| Asset Area | Decision |
|---|---|
| PaperZD | Enable in `.uproject`; verify compile/editor launch once Live Coding is closed |
| Pasma | Exact plugin id found; currently enabled locally, high-risk until compile/editor launch is verified |
| Rogue Character Model | Do not commit nested sample project; migrate only selected assets later through Unreal's migration flow |
| RogueCharacterModel `Vefects/Tentacles_VFX` | Content exists locally; no `.uplugin` descriptor was found, so treat as asset/VFX content rather than an enabled plugin |
| SurfaceWrap2D / 2dActorPlusFiles / TetherAndTow | Small enough to review for 2D mechanics, but still migrate selectively instead of committing the nested source folder |
| RamsterZ / mocap animation packs | Use as movement/combat reference or retarget test material only; see `ANIMATION_SOURCE_INVENTORY.md` for Jacob candidate order |
| Motifect / Realistic Combat Moves | Keep as Fab source FBX until selected clips are imported into an intake namespace |
| Weapon FBX packs | Defer unless a specific placeholder prop is needed for Slice 1-3 |
