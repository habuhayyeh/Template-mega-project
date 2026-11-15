# AX-S1S2-D — scorer predicates

Exact predicates. Each has one owning submodule, one mode, and the cases it is expected to fire on.

**Mode** describes how a predicate is scored: `MECHANICAL` (deterministic), `SEMANTIC` (judged against a written rule), `HYBRID` (mechanically gated, semantically confirmed).

**Run count is not a property of the predicate.** The experiment protocol fixes 3 repetitions for every predicate; Gate 0 fixes its own calibration counts. The two are never derived from each other, and a disagreement between experiment repetitions is not a calibration result.

All are calibrated by Gate 0 before use. A predicate that has no Gate 0 seed is not yet scoreable.

---

## S1 family

| id | mode | owner | asserts | cases |
|---|---|---|---|---|
| `S1-CAND-01` | SEMANTIC | S1 | every candidate names a neurologic subject for which the encounter poses its own assessment question | 01,02,03,04,05,06,07,08,09,10,11 |
| `S1-CAND-02` | MECHANICAL | S1 | every candidate carries ≥1 source anchor | all |
| `S1-AUTH-01` | HYBRID | S1 | S1 output contains no adoption **field** — no `adopted`, no adoption verdict, no resolved/current status. A candidate may still carry candidate claims and any canonical candidate-level explicit relationships. Scored on schema presence, not vocabulary; a lexical ban on words like `current` would fail on legitimate uses | all |
| `S1-AUTH-02` | MECHANICAL | S1 | S1 emits no single selected claim; claims appear as candidates only | all |
| `S1-BODY-01` | SEMANTIC | S1 | a subject that only contextualises another problem does not become a candidate | 07,08,10 |

`S1-CAND-01` is the one predicate here that is genuinely judgemental. It is also the one that carries the candidacy rule, so it must not be softened into a vocabulary check.

## S2 family

| id | mode | owner | asserts | cases |
|---|---|---|---|---|
| `S2-ADOPT-01` | SEMANTIC | S2 | adoption verdict per object matches the case's frozen expectation | 01,02,09,03 |
| `S2-ADOPT-02` | HYBRID · `PENDING_SCHEMA` | S2 | no adoption is inferred from medication, drug class, or convention; an adoption must cite a source span. Not mechanical until explicit-link semantics are represented structurally — an adoption citing any span proves nothing | all |
| `S2-REP-01` | SEMANTIC | S2 | every approved representation is supported by source objects, including representations assembled from relations rather than quoted claims | all |
| `S2-REP-02` | MECHANICAL | S2 | within `representations[]` (the approved set) for one problem, at most one entry unless every entry has `selection_safe: true` | all |
| `S2-TEMP-01` | MECHANICAL | S2 | S2 does not alter the temporality recorded in the substrate | all |
| `S2-CONF-01` | SEMANTIC | S2 | contradictory sources are adjudicated, not collapsed: the non-selected assertion remains recoverable with attribution | 11 |

## S3 family

| id | mode | owner | asserts | cases |
|---|---|---|---|---|
| `S3-SEL-01` | MECHANICAL | S3 | every selected representation exists in S2's approved set for that problem | all |
| `S3-SEL-02` | SEMANTIC | S3 | S3 synthesises no representation and merges none | 05,06 |
| `S3-INC-01` | MECHANICAL | S3 | no A/P problem is rendered without an approved representation — applies to **every rendered A/P problem in every case**, not only the cases expected to trip it | all |
| `S3-ACCT-01` | MECHANICAL | S3 | every substrate object is either used or carries a disposition entry | all |
| `S3-BODY-01` | MECHANICAL | S3 | body-only objects are retained without being promoted to A/P problems | 07,08,10 |

## S4 family

| id | mode | owner | asserts | cases |
|---|---|---|---|---|
| `S4-INC-01` | MECHANICAL | S4 | S4 adds or removes no problem relative to S3's rendered set | all |
| `S4-REP-01` | MECHANICAL | S4 | every `units[].representation` equals the S3 `selected_rep` for that problem, compared by id | all |
| `S4-ORD-01` | MECHANICAL · `PENDING_DEPENDENCY` | S4 | problem and unit order follow the ordering contract using S1 salience inputs. No frozen ordering oracle or salience value set exists yet; not scoreable until both are frozen | all |
| `S4-MEM-01` | MECHANICAL | S4 | every unit member exists in the retained-use map | all |
| `S4-COMP-01` | MECHANICAL | S4 | every rendered problem has a claim-bearing unit; every plan item **S3 retained** has a plan unit. S4 completeness is measured against S3's retained set, not against the source — otherwise the predicate re-decides retention and steals S3's authority | all |

---

## Expected outcomes per frozen case

| case | must be true | must be false |
|---|---|---|
| `CASE-01` | infarct **not** adopted and **not rendered as an A/P problem**; it may appear only as attributed body/history context if S3 selects it; the medication line does **not** create an infarct claim | adoption of the infarct, in any form, including a rendered A/P problem for it |
| `CASE-02` | infarct adopted on the explicit statement; claim representation carries attribution | adoption from anything other than the statement |
| `CASE-09` | infarct adopted on the explicit secondary-prevention linkage in `O02`; the plan line names the infarct as its indication | adoption inferred from drug class alone |

These three cases exist to separate "adoption from evidence" from "adoption from convenience". A run that gets `CASE-02` right and `CASE-01` wrong has inferred adoption rather than found it.

## Pilot ACTIVE_PREDICATE_SET

Only these predicates are calibrated and scored in the three-case pilot. They are the ones the pilot cases can actually exercise.

```text
S1-CAND-01, S1-CAND-02, S1-AUTH-01, S1-AUTH-02
S2-REP-01, S2-REP-02, S2-TEMP-01, S2-ADOPT-01
S3-INC-01, S3-SEL-01, S3-ACCT-01
S4-INC-01, S4-MEM-01, S4-COMP-01, S4-REP-01
```

`S1-BODY-01` (body-only subject) and `S2-CONF-01` (contradictory sources) are **not** active: the pilot cases do not exercise them. They belong to CASE-07/08/10 and CASE-11.

**Excluded from the pilot verdict:** `S2-ADOPT-02` (late `PENDING_SCHEMA`) and `S4-ORD-01` (`PENDING_DEPENDENCY`). Neither is scored nor counted as unmet.

`S2-REP-02` and `S4-REP-01` are now **active**: the test schema defines `representations[]` as the approved set, with `selection_safe` on each entry, and carries `representation.id` and `unit.representation`. That is the field set both predicates need, so keeping them pending would have meant claiming a missing dependency that no longer exists.

## Scoring rules

1. A predicate is scored per case, per repetition.
2. `MECHANICAL` disagreement between repetitions is a defect, not variance.
3. `SEMANTIC` predicates require 3/3 agreement. Two of three is **`NONCONFORMANT` with a reproducibility disagreement** recorded alongside it — the model's answer is wrong in at least one run and unstable across runs. `UNSCORED` is reserved for insufficient valid runs or a pending prerequisite, never for disagreement. Calibration is a separate artifact and is not re-run here.
4. A false positive on an unrelated family voids that predicate's result — over-firing is not evidence.
5. First divergence is recorded by predicate id and owner; a run with two divergences reports both.

## Not yet scoreable

Predicates referencing `PENDING` cases are declared but cannot run. They are listed so the manifest is complete, not so they can be scored early.
