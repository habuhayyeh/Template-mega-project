# Gate 0 — seed corpus

Every seed names its parent layer, the exact field mutated, and predicate **ids** for both the fire and the silence check. S1–S4 ids are defined in `AX-S1S2-D/predicates.md`.

**Parents:** `DERIVED_PARENT` — hand-built, layer-appropriate, reviewed. Signer notes are final-note targets and cannot serve as S1/S2/S3/S4 parents.

**Scope:** only predicates in the pilot `ACTIVE_PREDICATE_SET` (`AX-S1S2-D/predicates.md` §Pilot) are calibrated now. `NT-*` note-level seeds are **excluded from this pilot**, because this experiment never produces a note.

**Calibration policy is derived from each predicate's own mode**, not from the family heading. The `semantic` / `mechanical` labels on the section headings are descriptive; the run count and pass rule come from `predicates.md` for that exact predicate id.

---

## S1 family — semantic, parent `S1_OUTPUT`

| seed | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|
| G0-S1-01 | `candidates[0].adopted = true` | `S1-AUTH-01` | S1 | `S2-ADOPT-01`, `S3-INC-01` | RUNNABLE |
| G0-S1-02 | `candidates[0].selected_claim = "…"` | `S1-AUTH-02` | S1 | `S2-REP-01` | RUNNABLE |
| G0-S1-03 | append a candidate for a body-only historical fact | `S1-BODY-01` | S1 | `S3-BODY-01` | RUNNABLE |
| G0-S1-04 | `candidates[0].anchors = []` | `S1-CAND-02` | S1 | `S2-REP-01` | RUNNABLE |
| G0-S1-05 | append a candidate for the old infarct used only as evidence for the seizure claim, with no assessment question of its own | `S1-CAND-01` | S1 | `S2-REP-01` | RUNNABLE |
| G0-S1-06 | `candidates[0].status_current = true` (a field in the forbidden set, not `adopted`) | `S1-AUTH-01` | S1 | `S2-REP-01` | RUNNABLE |

## S2 family — semantic, parent `S2_OUTPUT`

| seed | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|
| G0-S2-01 | `representations[0].support_refs = []` | `S2-REP-01` | S2 | `S1-AUTH-01` | RUNNABLE |
| G0-S2-02 | `representations[1].selection_safe = false` on a second approved entry | `S2-REP-02` | S2 | `S3-SEL-01` | RUNNABLE |
| G0-S2-03 | `adjudication[0].temporal` rewritten from the substrate value | `S2-TEMP-01` | S2 | `S1-AUTH-01` | RUNNABLE |
| G0-S2-04 | delete the non-selected assertion of a contradictory pair | `S2-CONF-01` | S2 | `S3-ACCT-01` | RUNNABLE |
| G0-S2-05 | `adjudication[0].adoption = true`, `evidence = null` | `S2-ADOPT-02` | S2 | `S1-AUTH-01` | PENDING_SCHEMA |
| G0-S2-06 | `adjudication[0].adoption = false` where the case expectation is adopted (CASE-02) | `S2-ADOPT-01` | S2 | `S1-AUTH-01` | RUNNABLE |

## S3 family — semantic, parent `S3_OUTPUT`

| seed | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|
| G0-S3-01 | render an A/P problem with `approved_representation = null` | `S3-INC-01` | S3 | `S4-INC-01` | RUNNABLE |
| G0-S3-02 | `rendered[0].selected_rep = "R-999"` | `S3-SEL-01` | S3 | `S2-REP-01` | RUNNABLE |
| G0-S3-03 | merge two approved representations into one selected | `S3-SEL-02` | S3 | `S2-REP-01` | RUNNABLE |
| G0-S3-04 | remove a retained object with no disposition entry | `S3-ACCT-01` | S3 | `S4-MEM-01` | RUNNABLE |

## S4 family — mechanical, parent `S4_BLUEPRINT`

| seed | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|
| G0-S4-01 | remove a problem present in S3's rendered set | `S4-INC-01` | S4 | `S3-INC-01` | RUNNABLE |
| G0-S4-02 | add a problem absent from S3's rendered set | `S4-INC-01` | S4 | `S3-INC-01` | RUNNABLE |
| G0-S4-03 | swap two problem orders | `S4-ORD-01` | S4 | `S1-AUTH-01` | PENDING_DEPENDENCY |
| G0-S4-04 | unit member id absent from the retained-use map | `S4-MEM-01` | S4 | `S3-ACCT-01` | RUNNABLE |
| G0-S4-05 | `units[0].representation = "R-999"` while S3 selected `R1` | `S4-REP-01` | S4 | `S3-SEL-01` | RUNNABLE |
| G0-S4-06 | delete the plan unit for a plan item S3 retained | `S4-COMP-01` | S4 | `S3-ACCT-01` | RUNNABLE |

## Note-level — excluded from this pilot

`NT-FID-01`, `NT-DUP-01`, `NT-COMP-01`, `NT-VOICE-01` and their four seeds belong to note-level experiments. Not calibrated here: a STRUCTURE-only pilot never produces a note, so calibrating those scorers on this artifact teaches nothing.

---

## Specificity controls

1. **Clean parent** per layer — zero findings, run first.
2. **Harmless variation** — same content, different valid wording — zero findings.
3. **Full silence set** — the silence requirement is *every active predicate except the expected one*, not the single neighbour named in the table. A seed passes specificity only if no other active predicate fires. The `must not fire` column is an illustrative neighbour, not the requirement.

That is a stricter rule than one hand-picked neighbour, and it catches a scorer that fires broadly for reasons nobody anticipated.

## Attribution

Wrong-submodule attribution is a calibration failure.

## Current state

**20 RUNNABLE · 1 PENDING_SCHEMA · 1 PENDING_DEPENDENCY**, plus 4 note-level seeds excluded from this pilot.

## ACTIVE_PREDICATE → SEED map

Every active predicate has at least one seed. A predicate in the active set without a seed is a calibration gap, not an oversight to be absorbed later.

| predicate | seed(s) |
|---|---|
| `S1-CAND-01` | G0-S1-05 |
| `S1-CAND-02` | G0-S1-04 |
| `S1-AUTH-01` | G0-S1-01, G0-S1-06 |
| `S1-AUTH-02` | G0-S1-02 |
| `S2-REP-01` | G0-S2-01 |
| `S2-TEMP-01` | G0-S2-03 |
| `S2-ADOPT-01` | G0-S2-06 |
| `S3-INC-01` | G0-S3-01 |
| `S3-SEL-01` | G0-S3-02 |
| `S3-ACCT-01` | G0-S3-04 |
| `S4-INC-01` | G0-S4-01, G0-S4-02 |
| `S4-MEM-01` | G0-S4-04 |
| `S4-COMP-01` | G0-S4-06 |

**15 seeds calibrate 13 active predicates** for CASE-01/02/09.

`S1-AUTH-01` has two seeds because one mutation proves one forbidden field is detected, not that the forbidden set is. The set itself is closed and versioned in `predicates.md`.

Predicates with seeds but not active in this pilot: `S1-BODY-01` (G0-S1-03), `S2-REP-02` (G0-S2-02), `S2-CONF-01` (G0-S2-04), `S4-ORD-01` (G0-S4-03), `S4-REP-01` (G0-S4-05). They are not scored here; the cases that would exercise them are CASE-05/06/07/11.
