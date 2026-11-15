# FIXTURE_INDEX — reference cases

Canonical for: **which cases exist, what each observed, on what evidence, and which predicates they reference.**

This is an index. Evidence, baselines and assertion sets live in their own records. A fixture row carries no predicate metadata — not even a kind — because that lives in `ACCEPTANCE_MODEL.md`.

---

## 1. Entry anatomy

| Part | Content |
|---|---|
| observation | what was seen |
| evidence | immutable path(s) |
| boundary | what the evidence does **not** establish |
| predicates | `PRD-` ids referenced |
| status | `ACTIVE` / `PENDING_DEPENDENCY` / `WITHDRAWN` |

## 2. Cases

### CASE-01 — fabrication under a weak envelope

**Observation:** a run produced `postictal confusion resolved`; no source supported it.
**Evidence:** `runs/2026-11-14-p003-doximity/run1.txt` — a deliberate control: no dispatcher, no standing items.
**Boundary:** does not establish that extraction alone failed. The call was under-specified; the event tests the envelope as much as the guard.
**Predicates:** `PRD-001` (span support, I3), `PRD-002` (package completeness, BUILD), `PRD-003` (no added content, R1).
**Status:** ACTIVE.

### CASE-02 — duplication, infarct block

**Observation:** the infarct rendered as one bullet in some runs and two in others within one problem block.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`.
**Boundary:** the duplicates had different object ids, so id-level checks alone would not have caught them.
**Predicates:** `PRD-010` (id uniqueness, S4), `PRD-011` (proposition identity, S2).
**Status:** ACTIVE.

### CASE-03 — duplication, CT findings

**Observation:** as CASE-02, for CT findings.
**Evidence:** same set.
**Predicates:** `PRD-010`, `PRD-011`.
**Status:** ACTIVE.

### CASE-04 — duplication, family memory concern

**Observation:** the family's memory concern rendered twice in one block.
**Evidence:** same set.
**Predicates:** `PRD-010`, `PRD-011`.
**Status:** ACTIVE.

### CASE-05 — missing required line

**Observation:** `Seizure precautions` was absent from the plan.
**Evidence:** `reviews/P003-implementation-doximity-original-branch.md` (packaging finding); the line present in `set2/run1–3.txt` and `set3/run1–3.txt` after the contract was added.
**Boundary:** packaging defect, not model judgement.
**Predicates:** `PRD-020` (package supplies standing-item contract, BUILD), `PRD-021` (unit exists when trigger satisfied, S4 — `PENDING_DEPENDENCY`: standing-item contract unfrozen).
**Status:** ACTIVE.

### CASE-06 — malformed output

**Observation:** a free-text `REUSE` line broke the output schema on a repeated run.
**Evidence:** `artifacts/06_doximity_run3.md`.
**Predicates:** `PRD-030` (unit typechecks, S4 — `PENDING_DEPENDENCY`: operator registry unfrozen), `PRD-031` (malformed unit fails closed, R1 — `PENDING_DEPENDENCY`: containment policy unfrozen).
**Status:** PENDING_DEPENDENCY.

### CASE-07 — prior recommendation presented as current

**Observation:** a prior `no further workup [2025-06]` appeared in the current plan.
**Evidence:** `set2/run1.txt`, `set2/run2.txt`, `set2/run3.txt` and their validation records.
**Boundary:** establishes the adoption error, not a general rule about historical content. Historical-source objects **may** render in the plan when adopted; the defect is adoption without a statement.
**Predicates:** `PRD-040` (adoption requires a statement, S2), `PRD-041` (plan unit members are adopted-current, S3/S4).
**Status:** ACTIVE.

### CASE-08 — voice

**Observation:** conversational first-person framing in the A/P.
**Evidence:** `set3/run3.txt`.
**Predicates:** `PRD-050` (A/P has no first-person token, R1 — MECHANICAL); `PRD-051` (no other person-framing in A/P, R1 — SEMANTIC_AUDIT, `PENDING_DEPENDENCY`: style contract unfrozen).
**Status:** ACTIVE.

### CASE-09 — conditional plan composition

**Observation:** apixaban hold and resume-condition rendered as two bullets in two runs and one conditional line in the third.
**Evidence:** `set3/validation.txt`.
**Predicates:** `PRD-060` (condition attached to its action, S2), `PRD-061` (one line per composite unit, S4 — `PENDING_DEPENDENCY`: operator contract unfrozen).
**Status:** PENDING_DEPENDENCY.

### CASE-10 — instability

**Observation:** identical input under identical conditions produced different acceptance-relevant structure across three runs.
**Evidence:** `set3/run1–3.txt`.
**Boundary:** establishes variation, not a failure rate. Three runs cannot support a population claim.
**Predicates:** `PRD-070` (structure identical across same-condition runs, PROCESS_GATE), `PRD-071` (differences recorded by decision id, PROCESS_GATE).
**Status:** ACTIVE.

### CASE-11 — contract contradiction

**Observation:** two rules in `05` governed one ordering decision — reasoning before facts in one clause, facts before reasoning in another.
**Evidence:** `proposals/P003-ap-render.md` §1, `pipeline/05_WRITE_AP.md` at the rewrite.
**Predicates:** `PRD-080` (no two rules govern one decision with exclusive outcomes, BUILD_GATE).
**Status:** ACTIVE.

### CASE-12 — faithful but semantically incomplete

**Observation:** the artifact rendered `The MRI to show.` — supported, grammatical, carrying none of the claim's purpose.
**Evidence:** `artifacts/doximity_bplus_operator_experiment_2026-11-15.md`.
**Boundary:** that wording is the historical artifact's. It is **not** D-017's signer-approved `MRI to show.`; the two must not be cited interchangeably.
**Predicates:** `PRD-090` (operator's required semantic roles present, S4 — `PENDING_DEPENDENCY`: operator registry), `PRD-091` (renderer does not infer a missing role, R1), `PRD-092` (operator adequacy, S4 — SEMANTIC_AUDIT).
**Status:** PENDING_DEPENDENCY.

---

## 3. Withdrawn

- **Referral under two problems.** Cannot be cited. If re-observed, it enters §2 with a path.
- **`O51` as non-local regression.** `O51` is a prior MMSE and the added clause governed prior-record results; the move was a **direct** effect. Not evidence for non-local regression. C14 has no case.
- **Residual aphasia as seizure evidence.** Exclusion was enforced by the object's absence, not a runtime rule. Not a runtime breach; the defect was contract contradiction (CASE-11).

---

## 4. Rules

1. A fixture references predicates by id; it never defines one.
2. A case without an evidence path is not in §2.
3. A case changes only via `ACCEPTANCE CHANGE`; the old entry is versioned, not rewritten.
4. A new defect is registered before it is fixed.
