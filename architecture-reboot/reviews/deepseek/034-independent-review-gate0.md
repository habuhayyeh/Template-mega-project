# Independent adverse review — Gate 0 / AX-S1S2-D

**Reviewer:** separate agent, no context from the authoring session. Read-only. HEAD `f47e47a`.
**Method:** recomputed all hashes; recursively diffed all 15 seeds against the parent; implemented the 13 active predicates independently and ran them over parent and seeds.

**Verdict: NOT EXECUTABLE.**

## Blocking

1. **S2-TEMP-01 has no single ground truth, and the clean parent already fails it.** The substrate records O03 temporal as `June–November` (en dash); the oracle and parent use `June-November`. The schema says "compared to the substrate verbatim", so the parent rewrites it and the oracle blesses the rewrite — the predicate can never catch the thing it exists for. Four of seven objects disagree between substrate and oracle (O02 `2024-02` vs `2024-02 documented`; O05/O06/O07 `status current` vs `now`).
2. **`schema.md`'s field→predicate map contradicts `predicates.md`.** It still lists `selected_claim` under S1-AUTH-01, so a scorer built from it double-fires on G0-S1-02 and never fires on G0-S1-06 (`status_current`). It also lists an inactive predicate and omits an active one.
3. **The two S4-INC-01 seeds cannot both isolate S4-INC-01**, because S4-COMP-01's domain ("every rendered problem") is undefined — S3's rendered set or S4's problems list. Under either written reading, one of the two seeds also trips S4-COMP-01. Only an intersection domain isolates both, and it is written nowhere.
4. **G0-S2-06 is schema-invalid, duplicates G0-S2-05, and its spec names the wrong case.** It flips adoption to true while leaving `evidence: null`, which the schema forbids, and that is exactly the mutation G0-S2-05 is defined as. Also: no single-field adoption flip can be schema-valid in either direction.
5. **Seed inventory is false.** The file says 20 runnable; 15 artifacts exist and the same file later says 15. Five seeds are listed RUNNABLE and simultaneously described as not active, and three of them cannot be built on the one CASE-01 parent at all. The stated reason for excluding S4-REP-01 is factually wrong — the parent already has three units carrying representation ids, so that seed is constructible.
6. **S2-ADOPT-01 is undecidable for five of seven objects**, including the aspirin-line adoption the case exists to catch.
7. **Gate 0's pass rule cannot distinguish a predicate-level scorer from a layer-level one.** Attribution is checked at submodule granularity, so a scorer emitting only "S2" passes every seed without distinguishing S2-REP-01 from S2-TEMP-01. No finding record is defined anywhere.
8. **The calibration run count is defined three contradictory ways** — per family, per mode, and per predicate id — while `predicates.md` says run count is explicitly not a predicate property.
9. **Gate 0's own required controls have no artifacts.** No per-layer clean parents, no harmless-variation artifact, no scorer.

## Non-blocking

- Mutation records use prose rather than JSON values, and pointer style is inconsistent.
- `predicate_registry.version` and `active_set` ids are invented by the generator and appear in no document.
- `predicates.md` says "three predicates" and names four.
- Unit members extend beyond their representation's member list; no active predicate catches it.
- `G0-S1-05` is under-specified in the exact dimension S1-CAND-01 tests — the appended candidate has no claims and no salience, so a scorer firing on "no claims" passes without judging assessment relevance.
- `G0-S1-05`'s written spec describes the seizure case, which does not exist in CASE-01.
- The answer key sits in the same directory as the artifacts it keys.
- Nothing hashes the seed spec or the generator.

## Verified as sound

- All 15 artifacts differ from the parent by exactly one logical mutation, and all 17 recorded hashes reproduce.
- The parent is clean on every mechanical predicate the reviewer implemented, bar the en-dash case. Every retained object is reachable from a unit; retained ∪ dispositions = all seven objects.
- The full-silence rule is stated explicitly and correctly.
- The disjoint forbidden-field split, with a second seed for a different field of the same set, is the right construction.
