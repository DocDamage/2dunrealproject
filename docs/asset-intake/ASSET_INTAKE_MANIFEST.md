# Nocturne Signal — Asset Intake Manifest

**Purpose:** Track every uploaded archive, extracted asset category, accepted first-slice asset, deferred asset, rejected asset, and Unreal import decision.

**Rule:** Assets must be inventoried before they are imported into Unreal. Do not dump entire archives into `Content/`.

---

## 1. Intake Status

| Field | Value |
|---|---|
| Uploaded archives available | Yes |
| Fab VaultCache available | Yes |
| Archives decompressed | Yes |
| Inventory generated | Yes |
| First-slice assets selected | Partial |
| Unreal import paths approved | Partial |
| Current status | Uploaded archive inventory generated; Fab VaultCache and direct project content inventories captured; Jacob imported as temporary/reference character with expanded retargeted animation libraries; restarted editor sees copied RogueCharacterModel packages and Jacob retarget outputs |

---

## 2. Uploaded Archive Register

The following archives are available in the session and should be inventoried during Slice 0.

| Archive | Expected Category | Intake Priority | Status | Notes |
|---|---|---|---|---|
| `Crimson Gothic Castle.zip` | Gothic castle environment | High | Open | Likely first-slice candidate |
| `Cimson Gothic Castle 2.zip` | Gothic castle environment | High | Open | Name typo preserved from upload |
| `Crimson Gothic Castle 3.zip` | Gothic castle environment | High | Open | Compare with other castle packs |
| `Crimson Gothic Castle 4.zip` | Gothic castle environment | High | Open | Compare with other castle packs |
| `Crimson Gothic Castle 5.zip` | Gothic castle environment | High | Open | Compare with other castle packs |
| `Wall and floor details.zip` | Walls/floors/detail tiles | High | Open | Likely first-slice candidate |
| `Floor tiles and wall tiles.zip` | Floors/walls | High | Open | Likely first-slice candidate |
| `Wall tiles.zip` | Wall tiles | High | Open | Likely first-slice candidate |
| `Special tiles.zip` | Special/environmental tiles | Medium | Open | Candidate for gates/secret rooms |
| `Doors and Arches!.zip` | Doors/arches | High | Open | Required for slice room transitions |
| `Decor and details.zip` | Decor/detail props | Medium | Open | Use sparingly for readability |
| `Jars, pots and items.zip` | Breakables/items | Medium | Open | Useful for Dirges/pickups later |
| `Traps and mechanism.zip` | Traps/mechanisms | Medium | Open | Later slice unless simple hazard needed |
| `Structures and columns.zip` | Architecture/columns | High | Open | Good for Reliquary identity |
| `Statues and figures.zip` | Statues/figures | Medium | Open | Lore/environmental storytelling |
| `Furniture and fixtures.zip` | Furniture/fixtures | Low | Open | Likely deferred unless room identity needs it |
| `Psychological elements.zip` | Horror/psychological props | Medium | Open | Use carefully; do not clutter first room |
| `Barrels, crates and objects.zip` | Generic objects | Low | Open | Defer unless needed for collision tests |
| `Lightning and fx.zip` | Lighting/VFX | Medium | Open | Review for 2D readability |
| `Occult and horror elements.zip` | Occult/horror props | Medium | Open | Good fit but must not overpower sci-fi identity |
| `Patch 1.zip` | Patch/unknown | Unknown | Open | Must identify contents before use |
| `13. Lamps and torches.zip` | Lighting props | Medium | Open | Useful for Lumen/candlelight tests |
| `14. Town square decorations.zip` | Town props | Low | Open | Likely not first-slice Reliquary content |
| `11. Barrels, Crates and sacks.zip` | Generic objects | Low | Open | Defer unless needed for collision/destruction |
| `15. Trees and nature.zip` | Nature | Low | Open | Full-game Ash Gardens candidate, not first slice |
| `7. Windows and flower boxes.zip` | Town windows/flower boxes | Low | Open | Likely not Reliquary first slice |
| `4. House wall tiles.zip` | Town walls | Low | Open | Likely not Reliquary first slice |
| `6. Doors and entrances.zip` | Town doors/entrances | Low | Open | Compare against gothic doors/arches |
| `1. Cobblestone floor tiles.zip` | Ground/cobblestone | Low | Open | Could support exterior/town later |
| `2. Dirt path tiles.zip` | Dirt paths | Low | Open | Not first-slice Reliquary |
| `10. Wooden fences and gates.zip` | Fences/gates | Low | Open | Not first-slice Reliquary |
| `17. Benches and seating.zip` | Seating | Low | Open | Later hub/town candidate |
| `9. Wells and water structures.zip` | Wells/water structures | Low | Open | Later zone candidate |
| `8. Market Stalls.zip` | Market props | Low | Open | Not first-slice Reliquary |
| `12. Street Props.zip` | Street props | Low | Open | Not first-slice Reliquary |
| `5. Roof tiles.zip` | Roofs | Low | Open | Not first-slice Reliquary |
| `3. Grass and ground tiles.zip` | Grass/ground | Low | Open | Later Ash Gardens/town candidate |
| `16. Gardens and crops.zip` | Gardens/crops | Low | Open | Later Ash Gardens/town candidate |

---

## 3. Controlled Extraction Plan

Temporary extraction path should be outside the Unreal `Content/` tree.

Recommended local/session paths:

```text
/mnt/data/nocturne_asset_intake/raw_archives/
/mnt/data/nocturne_asset_intake/extracted/
/mnt/data/nocturne_asset_intake/inventory/
/mnt/data/nocturne_asset_intake/first_slice_candidates/
```

Do not import directly from zip archives.

Generated inventory files:

```text
docs/asset-intake/ASSET_INVENTORY_SUMMARY.md
docs/asset-intake/GENERATED_ASSET_INVENTORY.csv
docs/asset-intake/FAB_VAULTCACHE_INVENTORY.md
docs/asset-intake/JACOB_CHARACTER_INTAKE.md
docs/asset-intake/JACOB_ABILITY_ANIMATION_COVERAGE.md
docs/asset-intake/ANIMATION_SOURCE_INVENTORY.md
```

The local `RogueCharacterModel/` folder is a copied sample/content project. Do not treat the whole copied project as source-of-truth gameplay content; migrate only selected packages. For Unreal `.uasset` packages, preserve their original `Content/<PackageName>/...` paths when references require it.

Jacob has been imported intentionally as a temporary/reference character:

```text
SourceArt/Jacob/
Content/NocturneSignal/Characters/Jacob/
```

The Jacob source asset is CC BY 4.0; preserve attribution from `SourceArt/Jacob/License.txt`.

Expanded Jacob animation source staging has been added intentionally:

```text
SourceArt/AnimationSources/MCO_TC_Sword/
SourceArt/AnimationSources/MotifectSword/
SourceArt/AnimationSources/MotifectMartialArts/
SourceArt/AnimationSources/RealisticCombatMoves/
SourceArt/AnimationSources/UniversalAnimationLibrary1/
SourceArt/AnimationSources/UniversalAnimationLibrary2/
SourceArt/AnimationSources/ActorCoreWalk/
SourceArt/AnimationSources/ActorCoreTactical/
SourceArt/AnimationSources/GameAnimationSample/
SourceArt/AnimationSources/ParagonMannyCurated/
SourceArt/AnimationSources/FightAnimationMocapPack/
```

These are imported into `/Game/NocturneSignal/AnimationSources/...` first, then retargeted into `/Game/NocturneSignal/Characters/Jacob/RetargetedAnimations/...`.

Robotic tentacle visual source staging has also been added intentionally:

```text
SourceArt/Tentacles/RoboticTentacleHands/hand_18.glb
SourceArt/Tentacles/RoboticTentacleHands/metadata.json
SourceArt/Tentacles/RoboticTentacleHands/thumbnail.png
Tools/Unreal/import_robotic_tentacle_hands.py
```

Planned Unreal destination:

```text
Content/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/
```

Imported Unreal destination:

```text
Content/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/
```

The live editor import produced 32 `.uasset` files. The current primary mesh assignment is:

```text
/Game/NocturneSignal/Characters/Jacob/Tentacles/RoboticTentacleHands/hand_18/SkeletalMeshes/Cylinder
```

Advanced Locomotion Mechanics UE5 is the exception because it ships Unreal `.uasset` packages rather than FBX source. Its source packages are copied at their original package paths so dependencies resolve:

```text
Content/Animation/
Content/Mesh/Skeletal/Default/
```

Retargeted Jacob output remains namespaced:

```text
Content/NocturneSignal/Characters/Jacob/RetargetedAnimations/AdvancedLocomotionMechanicsUE5/
```

Selected `RogueCharacterModel` packages have also been copied at their original package paths:

```text
Content/FreeAnimationsPack/
Content/RogueCharacter/
Content/Vefects/Tentacles_VFX/
```

Retargeted Jacob output for those animation candidates remains namespaced:

```text
Content/NocturneSignal/Characters/Jacob/RetargetedAnimations/FreeAnimationsPack/
Content/NocturneSignal/Characters/Jacob/RetargetedAnimations/RogueCharacter/
Content/NocturneSignal/Characters/Jacob/RetargetedAnimations/VefectsVexa/
```

Verified post-restart retarget counts:

```text
FreeAnimationsPack: 10 Jacob AnimSequences
RogueCharacter: 7 Jacob AnimSequences
VefectsVexa: 25 Jacob AnimSequences
```

---

## 4. Inventory Fields

Each extracted asset should be inventoried with:

| Field | Description |
|---|---|
| Source Archive | Zip file the asset came from |
| Relative Path | Path inside archive |
| File Type | PNG, JPG, JSON, TXT, etc. |
| Pixel Size | Width x height for image assets |
| Sprite/Tile Guess | Sprite, tile, prop, sheet, VFX, UI, unknown |
| Category | Environment, prop, door, trap, light, enemy, etc. |
| First-Slice Candidate | Yes/No |
| Import Destination | Planned Unreal path |
| Collision Needed | None, simple, custom, tilemap |
| Notes | Duplicate, quality issue, scaling issue, etc. |

---

## 5. First-Slice Asset Needs

Reliquary of Waking first-slice minimum asset categories:

| Need | Required? | Notes |
|---|---:|---|
| Wall tiles | Yes | Gothic/sci-fi reliquary walls |
| Floor tiles | Yes | Readable collision edges |
| Architecture nodes | Yes | Grapple anchors must be visually obvious |
| Doors/arches | Yes | Room transitions and shortcuts |
| Coffin/sarcophagus assets | Yes | Waking Coffin, Coffin Engine boss arena |
| Columns/supports | Medium | Helps gothic cathedral identity |
| Candle/torch/lamp props | Medium | Lighting tests and room readability |
| Machinery/mechanisms | Medium | Undertaker Workshop and Coffin Engine support |
| Statues/religious props | Medium | Environmental storytelling |
| Breakables | Low | Defer until Dirges/pickups are implemented |
| Traps | Low | Defer unless needed for a simple hazard room |
| Town/nature assets | No | Full-game backlog, not first slice |

---

## 6. Unreal Import Destination Rules

Use project-specific namespaced paths:

```text
Content/NocturneSignal/Environments/ReliquaryOfWaking/Tiles/
Content/NocturneSignal/Environments/ReliquaryOfWaking/Props/
Content/NocturneSignal/Environments/ReliquaryOfWaking/Doors/
Content/NocturneSignal/Environments/ReliquaryOfWaking/GrappleAnchors/
Content/NocturneSignal/Characters/Veyra/
Content/NocturneSignal/Characters/Jacob/
Content/NocturneSignal/Enemies/Reliquary/
Content/NocturneSignal/VFX/VestigeLimb/
Content/NocturneSignal/Audio/NullVoice/
Content/NocturneSignal/Data/Forms/
Content/NocturneSignal/Data/Relics/
Content/NocturneSignal/Maps/TestRooms/
Content/NocturneSignal/Maps/ReliquaryOfWaking/
```

Avoid generic paths like:

```text
Content/Assets/
Content/Sprites/
Content/NewFolder/
Content/Marketplace/
```

---

## 7. Acceptance Criteria

An asset is accepted for first-slice use only when:

- It supports a specific first-slice room or system.
- It has a clear import destination.
- Its resolution/scale is understood.
- It does not create visual noise that harms gameplay readability.
- It fits the gothic sci-fi Reliquary identity.
- It does not depend on unknown runtime plugins unless documented.

---

## 8. Deferred Asset Policy

Deferred does not mean rejected.

Assets should be deferred when they belong to:

- Ash Gardens
- Lower Nave town/hub expansion
- Outdoor/town areas
- Later secrets
- Full-game decorative backlog
- Systems not being built in Slice 0-3

Deferred assets remain tracked here so they can be used later without repeating the intake process.

---

## 9. Next Action

Select the first small set of Reliquary sheets from `GENERATED_ASSET_INVENTORY.csv`, then import only those assets into approved `Content/NocturneSignal/...` paths. For VaultCache content, migrate only selected assets through Unreal after a destination path and slice purpose are approved. Jacob can be used immediately as the temporary/reference character while the final 2D player identity is still unresolved.
