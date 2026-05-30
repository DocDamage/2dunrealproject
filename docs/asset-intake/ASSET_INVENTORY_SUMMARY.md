# Nocturne Signal — Asset Inventory Summary

**Generated:** 2026-05-30  
**Source:** Controlled decompression of uploaded zip archives into temporary intake storage outside Unreal `Content/`.

---

## 1. Intake Result

| Metric | Result |
|---|---:|
| Archives processed | 38 |
| Archives extracted successfully | 38 |
| Invalid/corrupt archives | 0 |
| Files found | 61 |
| Image files | 61 |
| Exact duplicate files detected | 0 |
| File format found | PNG only |

The uploaded packs are lightweight and mostly appear to be sprite-sheet or tile-sheet PNGs rather than large multi-file Unreal asset packs.

---

## 2. Archive Summary

| Archive | Files | Image Size Pattern | First-Slice Direction | Notes |
|---|---:|---|---|---|
| `Crimson Gothic Castle` | 4 | 619x619, 1024x1024 | Review | Strong Reliquary candidate |
| `Cimson Gothic Castle 2` | 6 | 1254x1254 | Review | Strong Reliquary candidate; upload typo preserved |
| `Crimson Gothic Castle 3` | 6 | 1254x1254 | Review | Strong Reliquary candidate |
| `Crimson Gothic Castle 4` | 6 | 1254x1254 | Review | Strong Reliquary candidate |
| `Crimson Gothic Castle 5` | 6 | 1254x1254 | Review | Strong Reliquary candidate |
| `Wall and floor details` | 1 | 1254x1254 | Review | Likely useful for Reliquary surface detail |
| `Floor tiles and wall tiles` | 1 | 1269x1239 | Review | Likely useful for first test rooms |
| `Wall tiles` | 1 | 1111x1416 | Review | Likely useful for vertical slice walls |
| `Special tiles` | 1 | 1300x1209 | Review | Candidate for gates, secrets, or special rooms |
| `Doors and Arches!` | 1 | 1332x1181 | Review | Strong room-transition candidate |
| `6. Doors and entrances` | 1 | 1672x941 | Review | Secondary door candidate; probably less gothic |
| `Structures and columns` | 1 | 1156x1360 | Review | Good for Reliquary identity and room silhouettes |
| `13. Lamps and torches` | 1 | 1672x941 | Review | Useful for lighting/readability tests |
| `Lightning and fx` | 1 | 1278x1231 | Review | Review carefully; may be VFX reference/import candidate |
| `Occult and horror elements` | 1 | 1254x1254 | Review | Fits tone; use sparingly to avoid visual clutter |
| `Decor and details` | 1 | 1216x1293 | Review | Candidate for room identity/details |
| `Patch 1` | 1 | 1536x1024 | Review | Contains `Corner tiles!.png`; likely useful for tile completion |
| `Statues and figures` | 1 | 1254x1254 | Review-Later | Strong lore candidate, but not needed for movement proof |
| `Traps and mechanism` | 1 | 1254x1254 | Review-Later | Later hazard/mechanism candidate |
| `Jars, pots and items` | 1 | 1190x1322 | Review-Later | Later Dirges/breakables candidate |
| `Barrels, crates and objects` | 1 | 1226x1283 | Defer | Generic props; not needed for Slice 1 |
| `11. Barrels, Crates and sacks` | 1 | 1672x941 | Defer | Generic props; not needed for Slice 1 |
| `Furniture and fixtures` | 1 | 1375x1144 | Defer | Later room dressing |
| `Psychological elements` | 1 | 1172x1342 | Defer | Use later after visual language is locked |
| `1. Cobblestone floor tiles` | 1 | 1254x1254 | Defer | More town/exterior than Reliquary |
| `2. Dirt path tiles` | 1 | 1672x941 | Defer | Not first-slice Reliquary |
| `3. Grass and ground tiles` | 1 | 1672x941 | Defer | Ash Gardens/town candidate later |
| `4. House wall tiles` | 1 | 1672x941 | Defer | Town candidate later |
| `5. Roof tiles` | 1 | 1672x941 | Defer | Town/exterior candidate later |
| `7. Windows and flower boxes` | 1 | 1672x941 | Defer | Town candidate later |
| `8. Market Stalls` | 1 | 1672x940 | Defer | Town candidate later |
| `9. Wells and water structures` | 1 | 1672x940 | Defer | Town/water candidate later |
| `10. Wooden fences and gates` | 1 | 1672x941 | Defer | Town/exterior candidate later |
| `12. Street Props` | 1 | 1293x1217 | Defer | Town/street candidate later |
| `14. Town square decorations` | 1 | 1608x978 | Defer | Town candidate later |
| `15. Trees and nature` | 1 | 1536x1024 | Defer | Ash Gardens/town candidate later |
| `16. Gardens and crops` | 1 | 1536x1024 | Defer | Ash Gardens/town candidate later |
| `17. Benches and seating` | 1 | 1536x1024 | Defer | Town/hub candidate later |

---

## 3. First-Slice Candidate Set

These assets should be reviewed first for the Reliquary of Waking and grapple test rooms:

```text
Crimson Gothic Castle.zip
Cimson Gothic Castle 2.zip
Crimson Gothic Castle 3.zip
Crimson Gothic Castle 4.zip
Crimson Gothic Castle 5.zip
Wall and floor details.zip
Floor tiles and wall tiles.zip
Wall tiles.zip
Special tiles.zip
Patch 1.zip
Doors and Arches!.zip
Structures and columns.zip
13. Lamps and torches.zip
Decor and details.zip
Occult and horror elements.zip
Lightning and fx.zip
```

Recommended use:

| Need | Candidate Archives |
|---|---|
| Test room walls/floors | `Wall tiles`, `Floor tiles and wall tiles`, `Wall and floor details`, `Patch 1` |
| Reliquary gothic identity | `Crimson Gothic Castle*`, `Structures and columns` |
| Doors/room transitions | `Doors and Arches!` |
| Grapple anchor visual exploration | `Special tiles`, `Structures and columns`, custom placeholder if no clear anchor exists |
| Lighting readability | `13. Lamps and torches`, `Lightning and fx` |
| Room dressing | `Decor and details`, `Occult and horror elements` |

---

## 4. Deferred Backlog

These archives are not bad assets, but they do not support the immediate Reliquary/player-grapple proof:

```text
Town square decorations
Market Stalls
Street Props
House wall tiles
Roof tiles
Grass and ground tiles
Dirt path tiles
Cobblestone floor tiles
Wooden fences and gates
Wells and water structures
Trees and nature
Gardens and crops
Benches and seating
Windows and flower boxes
Furniture and fixtures
Barrels/crates/sacks/object packs
```

Likely later uses:

| Future Area | Asset Families |
|---|---|
| Lower Nave / hub expansion | benches, street props, doors, lamps |
| Ash Gardens | trees, grass, gardens, crops |
| Town/civilian memory zones | house walls, roofs, market stalls, flower boxes |
| Breakables/economy | jars, pots, barrels, crates, sacks |

---

## 5. Import Warnings

1. The files appear to be PNG sheets, not pre-cut Unreal assets.
2. Tile slicing rules must be decided before import.
3. Pixel density must be standardized before collision/blockout work.
4. Grapple anchors should probably be custom-authored or clearly marked; do not hide them inside busy gothic detail.
5. First test rooms can use simple placeholder geometry plus selected tile sheets.
6. Avoid importing deferred town/nature assets until the Reliquary slice has passed movement and grapple gates.

---

## 6. Recommended Next Asset Step

Before Unreal import:

1. Open first-slice candidate sheets visually.
2. Identify tile size assumptions.
3. Pick one wall/floor sheet for the Slice 1 test room.
4. Pick one door/arch sheet for future room transitions.
5. Decide whether Architecture Nodes come from existing art or need a custom placeholder marker.

Do not import the full archive set into Unreal yet.
