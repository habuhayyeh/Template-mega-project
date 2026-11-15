# Gate 0 — seed corpus

Every seed names the layer of its parent, the exact field mutated, and the predicate it must fire. Predicate ids in the S1–S4 families are the ids defined in `AX-S1S2-D/predicates.md`; `NT-*` ids are defined here because they exist only for calibration.

**Parents** are `DERIVED_PARENT` artifacts: hand-built, layer-appropriate, reviewed. Signer target notes are **not** parents — they are final-note targets and cannot serve as S1/S2/S3/S4 inputs.

**Status** — `RUNNABLE` (scoreable today), `PENDING_SCHEMA` (needs a field the test schema does not expose), `PENDING_DEPENDENCY` (needs a frozen contract or oracle).

---

## S1 family — semantic, 3 runs, parent `S1_OUTPUT`

| seed | parent_type | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|---|
| G0-S1-01 | `S1_OUTPUT` | `candidates[0].adopted = true` | `S1-AUTH-01` | S1 | S2, S3 | RUNNABLE |
| G0-S1-02 | `S1_OUTPUT` | `candidates[0].selected_claim = "…"` | `S1-AUTH-02` | S1 | S2 | RUNNABLE |
| G0-S1-03 | `S1_OUTPUT` | append a candidate for a body-only historical fact | `S1-BODY-01` | S1 | S3 | RUNNABLE |
| G0-S1-04 | `S1_OUTPUT` | `candidates[0].anchors = []` | `S1-CAND-02` | S1 | S2 | RUNNABLE |

## S2 family — semantic, 3 runs, parent `S2_OUTPUT`

| seed | parent_type | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|---|
| G0-S2-01 | `S2_OUTPUT` | `representations[0].support_refs = []` | `S2-REP-01` | S2 | S1 | RUNNABLE |
| G0-S2-02 | `S2_OUTPUT` | approve two representations, neither marked selection-safe | `S2-REP-02` | S2 | S3 | PENDING_SCHEMA |
| G0-S2-03 | `S2_OUTPUT` | `adjudication[0].temporal` rewritten from the substrate value | `S2-TEMP-01` | S2 | I4 | RUNNABLE |
| G0-S2-04 | `S2_OUTPUT` | delete the non-selected assertion of a contradictory pair | `S2-CONF-01` | S2 | S3 | RUNNABLE |
| G0-S2-05 | `S2_OUTPUT` | `adjudication[0].adoption = true` with `evidence = null` | `S2-ADOPT-02` | S2 | S1 | PENDING_SCHEMA |

## S3 family — semantic, 3 runs, parent `S3_OUTPUT`

| seed | parent_type | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|---|
| G0-S3-01 | `S3_OUTPUT` | render an A/P problem whose `approved_representation = null` | `S3-INC-01` | S3 | S4 | RUNNABLE |
| G0-S3-02 | `S3_OUTPUT` | `rendered[0].selected_rep = "R-999"` (not in the approved set) | `S3-SEL-01` | S3 | S2 | RUNNABLE |
| G0-S3-03 | `S3_OUTPUT` | merge two approved representations into one selected | `S3-SEL-02` | S3 | S2 | RUNNABLE |
| G0-S3-04 | `S3_OUTPUT` | remove a retained object with no disposition entry | `S3-ACCT-01` | S3 | S4 | RUNNABLE |

## S4 family — mechanical, parent `S4_BLUEPRINT`

| seed | parent_type | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|---|
| G0-S4-01 | `S4_BLUEPRINT` | remove a problem present in S3's rendered set | `S4-INC-01` | S4 | S3 | RUNNABLE |
| G0-S4-02 | `S4_BLUEPRINT` | add a problem absent from S3's rendered set | `S4-INC-01` | S4 | S3 | RUNNABLE |
| G0-S4-03 | `S4_BLUEPRINT` | swap two problem orders | `S4-ORD-01` | S4 | S1 | PENDING_DEPENDENCY |
| G0-S4-04 | `S4_BLUEPRINT` | unit member id absent from the retained-use map | `S4-MEM-01` | S4 | S3 | RUNNABLE |
| G0-S4-05 | `S4_BLUEPRINT` | unit's representation id differs from S3's selected id | `S4-REP-01` | S4 | S3 | PENDING_SCHEMA |

## Note-level families — Gate 0 local ids, parent `NOTE`

| seed | parent_type | mutation_path | must fire | owner | must not fire | status |
|---|---|---|---|---|---|---|
| G0-X-01 | `NOTE` | insert `resolved` into a status phrase | `NT-FID-01` | R1 | S2 | RUNNABLE |
| G0-X-02 | `NOTE` | duplicate one A/P bullet within a problem block | `NT-DUP-01` | S4 | S2 | RUNNABLE |
| G0-X-03 | `NOTE` | delete the standing-item line | `NT-COMP-01` | S4 | S3 | RUNNABLE |
| G0-X-04 | `NOTE` | rewrite one A/P bullet in first person | `NT-VOICE-01` | R1 | S3 | RUNNABLE |

---

## Specificity controls

1. **Clean parent** per layer — score zero. Run first, every family.
2. **Harmless variation** — same content, different valid wording and punctuation. Score zero. A scorer that flags this measures style.
3. **Cross-family silence** — each seed names the families that must stay quiet; tripping a neighbour fails calibration even when the right predicate fires.

## Attribution

A finding attributed to the wrong submodule is a Gate 0 failure. It sends the fix to the wrong module, which costs more than the original defect.

## Current state

14 RUNNABLE, 3 PENDING_SCHEMA, 1 PENDING_DEPENDENCY. Gate 0 is `AUTHORED / UNRUN` until a scorer exists and every RUNNABLE seed has a recorded verdict.
