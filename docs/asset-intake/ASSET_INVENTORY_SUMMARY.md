# Nocturne Signal — Asset Inventory Summary

**Generated:** 2026-05-30  
**Source:** `F:\Nocturne Signal\assets`
**Extraction path:** `F:\Nocturne Signal\asset_intake\extracted`
**Detailed inventory:** `docs/asset-intake/GENERATED_ASSET_INVENTORY.csv`

---

## 1. Intake Result

| Metric | Result |
|---|---:|
| Zip archives found | 135 |
| Zip archives extracted successfully | 135 |
| Invalid/corrupt archives | 0 |
| Extracted files | 158 |
| Extracted size | 292.91 MB |
| File format found | PNG only |
| Largest extracted file | 3.36 MB |
| MCP-named files found | 0 |

The raw asset archives are GitHub-safe by individual file size. The extracted PNG sheets are also GitHub-safe by individual file size, but they should still be imported selectively into Unreal rather than dumped into production `Content/`.

---

## 2. Category Summary

| Category | Files | Size | First-Slice Review | Deferred |
|---|---:|---:|---:|---:|
| Crimson Gothic Castle | 28 | 69.37 MB | 28 | 0 |
| Dungeon Asset Pack | 15 | 24.39 MB | 15 | 0 |
| Magic Forest Asset Pack | 17 | 33.55 MB | 6 | 11 |
| Magic wizard academy | 20 | 37.92 MB | 6 | 14 |
| Medieval village town | 21 | 31.60 MB | 5 | 16 |
| Psychological Horror Dungeon | 16 | 31.55 MB | 16 | 0 |
| Sakura Temple Asset Pack | 20 | 30.71 MB | 4 | 16 |
| Volcanic | 21 | 33.83 MB | 4 | 17 |

---

## 3. Image Size Patterns

| Size | Count |
|---|---:|
| 1536 x 1024 | 67 |
| 1672 x 941 | 37 |
| 1254 x 1254 | 30 |
| 619 x 619 | 3 |
| 1672 x 940 | 3 |
| Other one-off sizes | 18 |

The set is mostly sprite/tile sheets. Tile slicing, pixel density, and collision policy should be decided before Unreal import.

---

## 4. First-Slice Priority

Review these first for Reliquary of Waking and Slice 1-3 prototype needs:

| Need | Candidate Categories |
|---|---|
| Reliquary walls/floors | Crimson Gothic Castle, Dungeon Asset Pack, Psychological Horror Dungeon |
| Gothic room identity | Crimson Gothic Castle, Psychological Horror Dungeon, Dungeon statues/columns |
| Doors and room transitions | Psychological Horror Dungeon, Dungeon Asset Pack, Magic wizard academy |
| Grapple anchor visual exploration | Special tiles, structures/columns, custom placeholder markers |
| Lighting readability | Lamps/torches, lightning/fx, LightShaftGenie local content |
| Combat/Vestige impact VFX | Vefects local content, occult/horror sheets |

Defer most town, forest, sakura, and volcanic sheets until the movement/grapple proof is stable.

---

## 5. Current Unreal Content Policy

| Content Folder | Size | Git Policy |
|---|---:|---|
| `Content/A_Surface_Footstep` | 348.44 MB | Local-only unless Git LFS is introduced |
| `Content/Vefects` | 131.64 MB | Local-only unless Git LFS is introduced |
| `Content/RamsterZ_FreeAnims_Volume1` | 23.23 MB | GitHub commit candidate |
| `Content/LightShaftGenie` | 1.95 MB | GitHub commit candidate |
| `Content/Fab` | 1.23 MB | GitHub commit candidate, but should be reviewed because path is generic |
| `Content/NocturneSignal/Characters/Jacob` | ~5.35 MB | GitHub commit candidate; temporary/reference player character |
| `SourceArt/Jacob` | ~9.74 MB | GitHub commit candidate; includes CC BY 4.0 license and cleaned import FBX |
| `RogueCharacterModel/Content` | 1,708.46 MB | Local-only nested intake source; ignored by git |

Nested `RogueCharacterModel/Content` highlights:

| Folder | Size | Intake Decision |
|---|---:|---|
| `RogueCharacter` | 656.97 MB | Local-only character/reference content |
| `VelocityReflectLaunchSystemUE5` | 391.71 MB | Local-only movement sample; evaluate mechanics only |
| `A_Surface_Footstep` | 349.46 MB | Local-only duplicate/related VFX demo content |
| `Vefects` | 265.06 MB | Local-only VFX content; includes `Tentacles_VFX` assets, but no `.uplugin` descriptor |
| `RamsterZ_FreeAnims_Volume1` | 23.23 MB | Commit candidate only if migrated selectively |
| `SurfaceWrap2D` | 16.91 MB | Candidate for selective 2D prototype evaluation |
| `2dActorPlusFiles` | 4.38 MB | Candidate for selective 2D prototype evaluation |
| `TetherAndTow` | 0.42 MB | Candidate for selective mechanic review |

---

## 6. Import Warnings

1. Do not import all 158 PNG sheets into production paths at once.
2. Pick a small first-slice candidate set, then import under `Content/NocturneSignal/...`.
3. Keep large demo/plugin packs local until there is a deliberate LFS policy.
4. The search found no MCP-named files in `F:\Nocturne Signal\assets` or the extracted intake folder.
5. If an MCP plugin is expected, its descriptor likely lives outside this asset folder and needs a separate path or exact plugin name.
6. `RogueCharacterModel/Content` is a nested sample-project payload and should stay local unless selected assets are migrated into approved project paths.
7. Jacob is imported as a temporary/reference skeletal character under `Content/NocturneSignal/Characters/Jacob`; preserve CC BY 4.0 attribution from `SourceArt/Jacob/License.txt`.
