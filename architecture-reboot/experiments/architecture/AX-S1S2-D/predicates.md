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
| `S1-AUTH-01` | MECHANICAL | S1 | no candidate carries any **adoption or final-state** field: `{adopted, adoption, adoption_verdict, resolved, status_current}`. Final-claim fields are `S1-AUTH-02`'s alone — the two sets are disjoint so no seed can be required to fire both. Scored on field presence, never vocabulary | all |
| `S1-AUTH-02` | MECHANICAL | S1 | no candidate carries a **selected/final-claim** field: `{selected_claim, final_claim, chosen_claim}`; claims appear as candidates only. Owns this field family exclusively | all |
| `S1-BODY-01` | SEMANTIC | S1 | a subject that only contextualises another problem does not become a candidate | 07,08,10 |

`S1-CAND-01` is the one predicate here that is genuinely judgemental. It is also the one that carries the candidacy rule, so it must not be softened into a vocabulary check.

## S2 family

| id | mode | owner | asserts | cases |
|---|---|---|---|---|
| `S2-ADOPT-01` | SEMANTIC | S2 | for objects the oracle names in `expected.adoption`, the verdict matches. Objects not named are not scored — an unlisted object has no adoption expectation to violate | 01,02,09 |
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
| `S3-CAND-01` | MECHANICAL | S3 | coverage: every S1 problem-candidate id has an outcome; exclusivity: exactly one outcome per candidate; equality: the RENDERED set equals `rendered[]`. NOT_RENDERED requires a reason from `REASON-1`; basis is required exactly when the registry says so, must be non-empty, unique, and target object ids present in the oracle; unknown candidate ids are a violation; the correctness of a reason is a separate semantic audit | all |
| `S3-BODY-01` | MECHANICAL | S3 | body-only objects are retained without being promoted to A/P problems | 07,08,10 |

## S4 family

| id | mode | owner | asserts | cases |
|---|---|---|---|---|
| `S4-INC-01` | MECHANICAL | S4 | S4 adds or removes no problem relative to S3's rendered set | all |
| `S4-REP-01` | MECHANICAL | S4 | every `units[].representation` equals the S3 `selected_rep` for that problem, compared by id | all |
| `S4-ORD-01` | MECHANICAL · `PENDING_DEPENDENCY` | S4 | problem and unit order follow the ordering contract using S1 salience inputs. No frozen ordering oracle or salience value set exists yet; not scoreable until both are frozen | all |
| `S4-MEM-01` | MECHANICAL | S4 | every unit member exists in the retained-use map | all |
| `S4-PROJ-01` | MECHANICAL | S4 | every field S4 reads is in the frozen `S4_INPUT_VIEW` projection for selected/retained content; the projection schema and exact source map are frozen in `schema.md::PROJECTION_MAP`; every field must match its mapped source path and owner; no unselected or non-required state; no semantic value may be introduced by the projection. Proves packaging only, not runtime non-leakage | all |
| `S4-COMP-01` | MECHANICAL | S4 | domain is **S4.problems ∩ S3.rendered** — the intersection, not either set alone. Within it, every problem has a unit whose operator is a claim-bearing operator (`FACT`, `REASONING`, `CLAIM`); every plan item S3 retained has a `PLAN` unit. S4 completeness is measured against S3's retained set, not against the source — otherwise the predicate re-decides retention and steals S3's authority | all |

---

## Expected outcomes per frozen case

| case | must be true | must be false |
|---|---|---|
| `CASE-01` | infarct **not** adopted and **not rendered as an A/P problem**; it may appear only as attributed body/history context if S3 selects it; the medication line does **not** create an infarct claim | adoption of the infarct, in any form, including a rendered A/P problem for it |
| `CASE-02` | infarct adopted on the explicit statement; claim representation carries attribution | adoption from anything other than the statement |
| `CASE-09` | infarct adopted on the explicit secondary-prevention linkage in `O02`; the plan line names the infarct as its indication | adoption inferred from drug class alone |

These three cases exist to separate "adoption from evidence" from "adoption from convenience". A run that gets `CASE-02` right and `CASE-01` wrong has inferred adoption rather than found it.

## Pilot ACTIVE_PREDICATE_SET (PILOT-2, post-DC-002)

```text
S1-CAND-01, S1-CAND-02, S1-AUTH-01, S1-AUTH-02
S2-REP-01, S2-TEMP-01, S2-ADOPT-01
S3-CAND-01, S3-INC-01, S3-SEL-01, S3-ACCT-01
S4-INC-01, S4-MEM-01, S4-COMP-01, S4-REP-01, S4-PROJ-01
```

Sixteen predicates. `S3-CAND-01` and `S4-PROJ-01` are new under DC-002; both are mechanical and both
have seeds in this pilot.

Not active: `S1-BODY-01`, `S2-REP-02`, `S2-CONF-01` (no pilot case produces the condition),
`S2-ADOPT-02` (PENDING_SCHEMA), `S4-ORD-01` (PENDING_DEPENDENCY — no ordering oracle).

## Scoring rules

1. A predicate is scored per case, per repetition.
2. `MECHANICAL` disagreement between repetitions is a defect, not variance.
3. `SEMANTIC` predicates require 3/3 agreement. Two of three is **`NONCONFORMANT` with a reproducibility disagreement** recorded alongside it — the model's answer is wrong in at least one run and unstable across runs. `UNSCORED` is reserved for insufficient valid runs or a pending prerequisite, never for disagreement. Calibration is a separate artifact and is not re-run here.
4. A false positive on any other active predicate in the same layer voids that predicate's result — over-firing is not evidence.
5. First divergence is recorded by predicate id and owner; a run with two divergences reports both.

## Not yet scoreable

Predicates referencing `PENDING` cases are declared but cannot run. They are listed so the manifest is complete, not so they can be scored early.

## Execution mode per predicate

A predicate labelled SEMANTIC needs a frozen execution mode before a scorer can implement it. "Model-
or human-judged" is not an implementation.

| predicate | mode | how it is decided |
|---|---|---|
| `S1-CAND-01` | SEMANTIC / HUMAN_REVIEW | reviewer compares candidate concepts to the oracle's excluded list; recorded with the reviewer id |
| `S2-ADOPT-01` | SEMANTIC / HUMAN_REVIEW | reviewer compares adoption verdicts to the oracle; no model self-judgement |
| `S2-REP-01` | SEMANTIC / HUMAN_REVIEW | reviewer judges whether each representation's members and their relations semantically support the problem's claim, not merely that ids and support refs exist; real objects and refs are necessary but not sufficient, and a representation assembled from real objects into an unsupported claim or relation fails |
| `S3-SEL-01` | MECHANICAL | id membership in the approved set |
| `S4-COMP-01` | MECHANICAL | domain S4 ∩ S3, operator class check |

No semantic predicate is scored by the model that produced the artifact. Where a human judge is used,
the finding records judge id and the rule applied; where a mechanical check exists, it never defers to
a judgement.

**Gate 0 repetition for HUMAN_REVIEW.** A semantic judgment cannot be manufactured by deterministic
preprocessing. The frozen policy is:

- **three independent, blinded human judgments** per seed;
- each judge sees artifact + case oracle + predicate rule, never the seed id, expected predicate,
  mutation metadata or specificity answer key;
- **all three** must detect the seeded defect **and** satisfy `FULL_SILENCE-WITHIN-LAYER`;
- two of three is a calibration failure; there is no majority rule;
- a single judge repeating is recorded as `1 judge × 3 passes` and is not calibration evidence;
- a mechanical pre-filter may prepare evidence, but it is not a judgment and cannot substitute for any
  of the three. If it fully decides the branch, that branch is mechanical and must be reclassified.

Three independent judges who all detect the seed but one over-fires another predicate in the layer also
fail: detection without specificity is not calibration.
