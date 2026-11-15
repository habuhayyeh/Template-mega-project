# Gate 0 — seed corpus

Each seed is a single mutation of a clean parent. The parent must score zero; the seed must fire exactly the named predicate, in the named family, attributed to the named owner.

**Parent status:** hand-built clean cases marked `DERIVED_PARENT`. When the signer's notes arrive, real parents replace them and the seeds are re-run — a seed that only works on a toy parent does not calibrate anything.

---

## S1 — authority family (semantic, 3 runs)

| seed | mutation of parent | must fire | owner | must not fire |
|---|---|---|---|---|
| G0-S1-01 | add an adoption verdict string to S1 output ("current", "adopted") | `S1_NO_ADOPTION_VERDICT` | S1 | S2, S3 families |
| G0-S1-02 | S1 output carries a chosen final claim rather than candidates | `S1_NO_FINAL_CLAIM` | S1 | S2 |
| G0-S1-03 | promote a body-only historical fact into an A/P problem candidate | `S1_CANDIDACY_SOURCE_GROUNDED` | S1 | S3 |
| G0-S1-04 | invent a problem candidate with no source anchor | `S1_CANDIDACY_ANCHORED` | S1 | I3 |

## S2 — representation family (semantic, 3 runs)

| seed | mutation | must fire | owner | must not fire |
|---|---|---|---|---|
| G0-S2-01 | approved representation asserts content absent from every source object | `S2_REP_SOURCE_GROUNDED` | S2 | S1 |
| G0-S2-02 | two approved representations, non-equivalent, no recorded resolution | `S2_APPROVAL_SAFETY` | S2 | S3 |
| G0-S2-03 | S2 rewrites the temporality recorded at annotation | `S2_TEMPORALITY_CONSUMED` | S2 | I4 |
| G0-S2-04 | S2 marks a problem approved while its only candidate is contradicted | `S2_CONTRADICTION_HANDLED` | S2 | S3 |

## S3 — selection family (semantic, 3 runs)

| seed | mutation | must fire | owner | must not fire |
|---|---|---|---|---|
| G0-S3-01 | A/P problem rendered with no approved representation | `S3_INCLUSION_REQUIRES_APPROVAL` | S3 | S4 |
| G0-S3-02 | S3 selects a representation not in S2's approved set | `S3_SELECTION_FROM_APPROVED` | S3 | S2 |
| G0-S3-03 | S3 merges two approved representations into one | `S3_NO_SYNTHESIS` | S3 | S2 |
| G0-S3-04 | body-only object silently dropped from the retained set | `S3_ACCOUNTING_TOTAL` | S3 | S4 |

## S4 — blueprint family (mechanical + semantic)

| seed | mutation | must fire | owner | must not fire | layer |
|---|---|---|---|---|---|
| G0-S4-01 | S4 removes a problem that S3 marked rendered | `S4_INCLUSION_IMMUTABLE` | S4 | S3 | mechanical |
| G0-S4-02 | S4 adds a problem not in S3's rendered set | `S4_INCLUSION_IMMUTABLE` | S4 | S3 | mechanical |
| G0-S4-03 | S4 reorders problems ignoring the ordering contract | `S4_ORDER_CONTRACT` | S4 | S1 | mechanical |
| G0-S4-04 | unit references an object absent from the retained-use map | `S4_UNIT_MEMBERSHIP` | S4 | S3 | mechanical |
| G0-S4-05 | unit's operator contradicts the section contract | `S4_OPERATOR_SECTION_FIT` | S4 | R1 | mechanical |

## Generic fidelity (mechanical)

| seed | mutation | must fire | owner | must not fire |
|---|---|---|---|---|
| G0-X-01 | insert one clinical word absent from source and IR ("resolved") | `FIDELITY_NO_NEW_CONTENT` | R1 | S2 |
| G0-X-02 | render one proposition twice within a section+problem | `DUPLICATE_RENDER` | S4 | S2 |
| G0-X-03 | delete a required standing-item line | `COMPLETENESS_STANDING_ITEM` | S4 | S3 |
| G0-X-04 | A/P line uses first person | `VOICE_AP_IMPERSONAL` | R1 | S3 |

---

## Specificity controls

Three further cases exist to catch over-firing:

1. **Clean parent** — zero findings. Run first, every family.
2. **Harmless variation** — same content, different valid wording and punctuation. Zero findings. A scorer that flags this is measuring style, not correctness.
3. **Cross-family isolation** — each seed above names the families that must stay silent. A seed that trips a neighbour is a calibration failure even if it fires the right predicate.

## Attribution requirement

A finding attributed to the wrong submodule is a Gate 0 failure. It sends the fix to the wrong module, which costs more than the original defect.

## Current state

Seeds authored, parents derived, no runs. Gate 0 is `AUTHORED / UNRUN` until a scorer exists and every family has a recorded verdict.
