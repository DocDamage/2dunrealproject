# Nocturne Signal — Risk Register

**Purpose:** Track risks that can block, damage, or distort the first playable slice.

**Status Values:** `Open`, `In Progress`, `Fixed`, `Verified`, `Blocked`

**Severity Values:** `Low`, `Medium`, `High`, `Critical`

---

## Active Risks

| ID | Severity | Feature/System | Risk | Mitigation | Status | Verification |
|---|---|---|---|---|---|---|
| R-001 | Critical | PaperZD / UE 5.7 | PaperZD may have compatibility or packaging issues with Unreal Engine 5.7 | Verify compile, editor play, and packaging before animation-heavy work | Open | Not verified |
| R-002 | High | Scope | Large asset library may cause uncontrolled scope creep | Intake assets first; approve only first-slice content | Open | Not verified |
| R-003 | High | 2D Collision | UE 2D collision may feel unstable or sticky | Build movement/collision test room early | Open | Not verified |
| R-004 | Critical | Vestige Grapple | Grapple may feel floaty, imprecise, or hard to read | Prototype Pull-to-Point before room layout; use guided velocity before full physics | Open | Not verified |
| R-005 | High | Plugins | FAB plugins may work locally but break repo portability | Reconcile `.uproject`; document every enabled plugin | Open | Not verified |
| R-006 | Medium | Character Art | Final Veyra art is not available in this session and may change proportions | Use configurable placeholder dimensions | Open | Not verified |
| R-007 | High | Predator Protocol | Consume prompt may be missed by players | Prototype readable limb pulse; playtest threshold discovery | Open | Not verified |
| R-008 | Medium | Choir Resonance | Rhythm reward may be invisible or confusing | Add clear audio/visual hit feedback and debug timing | Open | Not verified |
| R-009 | Critical | SaveGame | Save/load bugs may corrupt progression or consumed enemy state | Implement save/load tests as soon as consume prototype exists | Open | Not verified |
| R-010 | Medium | Relic System | Relic builds may dilute identity or overwhelm first slice | Limit Slice 1-3 to minimal relic scaffolding | Open | Not verified |
| R-011 | High | Combat Feel | Combat may feel weak without hit pause/stagger tuning | Add hit pause and stagger in first combat room | Open | Not verified |
| R-012 | Medium | Audio | MetaSounds beat clock may drift from gameplay timing | Research and prototype beat event accuracy early | Open | Not verified |
| R-013 | High | Level Design | Reliquary layout may become invalid if grapple scale changes later | Do not finalize rooms until Pull-to-Point and swing scale are known | Open | Not verified |
| R-014 | Medium | Visual Readability | Gothic detail assets may clutter gameplay silhouettes | Use asset intake review and gameplay readability checks | Open | Not verified |
| R-015 | High | Boss Prototype | Undertaker Frame may take too long if built as bespoke logic | Build reusable boss pattern framework before final boss polish | Open | Not verified |
| R-016 | High | Ending/Flag Systems | Ending requirements may become arbitrary or hard to track | Document ending flags before full-game progression work | Open | Not verified |
| R-017 | Medium | Repository Hygiene | Binary Unreal assets may bloat repo or require LFS unexpectedly | Decide LFS rules before committing large assets | Open | Not verified |
| R-018 | High | Plugin Lock-In | Unknown plugin APIs may leak into core systems | Keep gameplay core portable; adapter pattern for plugin-specific features | Open | Not verified |
| R-019 | Medium | Input | Grapple input may conflict with attack/consume/grip actions | Define Enhanced Input mappings early and test controller flow | Open | Not verified |
| R-020 | Medium | Camera | Grapple camera may snap or cause disorientation | Tune camera lag/offset in Slice 1 | Open | Not verified |

---

## Risk Handling Rules

1. Critical risks must be tested before related production content begins.
2. High risks must have mitigation before the feature is expanded.
3. Medium risks may remain open during prototyping but must be tracked.
4. No risk is closed without verification evidence.
5. If a risk requires research, document the three candidate solutions before implementation.

---

## Verification Evidence Examples

Acceptable verification evidence:

- Unreal editor opens project without plugin errors.
- C++ compile succeeds.
- PIE runtime test passes.
- Packaged build succeeds.
- Manual runtime test notes with clear pass/fail results.
- Automated test output.
- Asset inventory generated and committed.
- Screenshot/video evidence stored externally and referenced.

Unacceptable evidence:

- “Looks fine.”
- “Should work.”
- “Probably compatible.”
- “Worked in another project.”

---

## Next Risk Review

Risk review should happen after:

1. `.uproject` creation.
2. Plugin reconciliation.
3. Asset inventory generation.
4. First movement/grapple test room.
