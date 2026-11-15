# FIXTURE_REGISTER — evidence-grounded reference cases

This is an **index**. Case evidence, baselines and assertion sets live in per-case packets (`PACKET.md`); this file holds the summary, the status and the pointer.

Each entry carries seven parts, and the split matters because merging them lets a symptom become an invented diagnosis:

1. **OBSERVATION** — what was seen;
2. **EVIDENCE** — the immutable path;
3. **BOUNDARY** — what the evidence does *not* establish;
4. **ASSERTIONS** — guards inspired by the observation;
5. **PREREQUISITES** — contracts needed before an assertion is executable;
6. **SEVERITY** — CRITICAL / MATERIAL / COSMETIC;
7. **STATUS** — ACTIVE / PROVISIONAL / WITHDRAWN / PENDING_DEPENDENCY.

Every assertion has exactly one owner.

## 1. Failure classes

| Code | Class |
|---|---|
| F1 | fabrication — content the source never said |
| F2 | duplication — one fact rendered twice |
| F3 | silent omission — a fact or line gone |
| F4 | contract break — malformed output |
| F5 | instability — different decisions on identical input |
| F6 | cross-problem leakage |
| F7 | provenance misuse |
| F8 | prior promoted to current |
| F9 | voice violation |
| F10 | truncation |
| C11 | contract contradiction |
| C12 | stable bad output — faithful but clinically empty |
| C13 | over-inclusion / wrong note use |
| C14 | non-local regression |

## 2. Mandatory fixtures

### F-01 — fabrication

**Defect:** a run produced `postictal confusion resolved`; no source supported it.
**Evidence:** `runs/2026-11-14-p003-doximity/run1.txt` — a deliberate control: no dispatcher, no standing items.
**Boundary:** the historical event does not establish that I3 alone failed. The call was under-specified.
**Assertions:**

- A-01a `MECHANICAL` — no object's content token is absent from its span. Owner: **I3**.
- A-01b `MECHANICAL` — the package supplies every contract the template requires. Owner: **BUILD**.
- A-01c `MECHANICAL` — the renderer adds no content outside object payload, operator text and the transformation table. Owner: **R1**.

### F-02, F-03, F-04 — duplication

**Defect:** the infarct (F-02), the CT findings (F-03), and the family memory concern (F-04) each rendered twice within one problem block.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`.
**Assertions:**

- A-02a `MECHANICAL` — an object id appears in at most one unit per (section, problem). Owner: **S4**.
- A-02b `SEMANTIC_AUDIT` — two objects asserting the same proposition do not both render. Owner: **S2**.

Both are needed: the old duplicates had different object ids, so the id rule alone would have passed them.

### F-06 — missing required line

**Defect:** `Seizure precautions` was absent from the plan.
**Evidence:** `reviews/P003-implementation-doximity-original-branch.md` (packaging finding), current `PACKAGE.md`, and the line present in `runs/2026-11-14-p003-doximity/set2/run1.txt`, `set2/run2.txt`, `set2/run3.txt`, `set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`.
**Boundary:** the defect was packaging, not model judgement.
**Assertions:**

- A-06a `MECHANICAL` — the package declares and supplies the standing-item contract. Owner: **BUILD**.
- A-06b `MECHANICAL` — when the trigger is satisfied, the unit exists. Owner: **S4**.

### F-07 — malformed output

**Defect:** a free-text `REUSE` line broke the output schema on a repeated run.
**Evidence:** `artifacts/06_doximity_run3.md`.
**Assertions:**

- A-07a `MECHANICAL` — every unit typechecks against its operator. Owner: **S4**.
- A-07b `MECHANICAL` — a malformed unit yields `CONTRACT_ERROR` and the run fails. Owner: **R1**.

### F-11 — prior recommendation promoted

**Defect:** a prior `no further workup [2025-06]` appeared in the current plan.
**Evidence:** `runs/2026-11-14-p003-doximity/set2/run1.txt`, `set2/run2.txt`, `set2/run3.txt`, and their validation records — not the oracle alone.
**Assertions:**

- A-11a `SEMANTIC_AUDIT` — a prior recommendation is not treated as adopted unless a statement supports it. Owner: **S2**.
- A-11b `MECHANICAL` — a `HISTORICAL` object does not appear in a plan unit. Owner: **S4**.
- A-11c `MECHANICAL` — a plan unit's members are all `CURRENT` or `PROPOSED`. Owner: **S3**.

### F-12 — voice

**Defect:** first person and conversational framing in the A/P.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run3.txt`.
**Assertions:**

- A-12a `MECHANICAL` — the A/P carries no first-person token. Owner: **R1**.

### C-01 — contract contradiction

**Defect:** two rules in `05` governed one ordering decision — one put reasoning before the fact lines, the other put facts before reasoning. The writer obeyed a different one per run.
**Class:** **L1 contradiction** — two rules, one decision, incompatible outcomes. The L2 duplicate-authority framing is weaker and did not catch it.
**Evidence:** `proposals/P003-ap-render.md` §1, and `pipeline/05_WRITE_AP.md` at the rewrite.
**Assertions:**

- A-C01a `MECHANICAL` — the build fails when two rules govern one decision with incompatible normative fields. Owner: **BUILD**.

### C-02 — withdrawn as the non-local exemplar

**Observation:** adding a clause for prior-record results moved the `O51` statement.
**Why withdrawn:** `O51` is a prior MMSE, and the added clause governed prior-record results. The move was a **direct** consequence of the change, not a non-local one. Using it as evidence for C14 was wrong.
**Consequence:** C14 has **no mandatory fixture**. That is the honest state; it is recorded in `OBLIGATIONS.md` O-10 and O-06 as an obligation to demonstrate, not a defect with evidence.

### C-12 — faithful but clinically empty

**Defect:** the artifact rendered `The MRI to show.` — grammatical, supported, carrying none of the claim's payload.
**Evidence:** `artifacts/doximity_bplus_operator_experiment_2026-11-15.md`.
**Boundary:** that is the historical artifact's wording. It is **not** D-017's signer-approved `MRI to show.`; the two must not be cited interchangeably.
**Assertions:**

- A-C12a `MECHANICAL` — the operator's required semantic roles are all present in the unit. Owner: **S4**.
- A-C12b `MECHANICAL` — the renderer neither infers nor supplies a missing semantic role; a unit lacking a required role fails closed. Owner: **R1**.

### F-14 — conditional plan composition

**Observation:** apixaban hold and resume-condition rendered as two separate bullets in two runs and as one conditional line in the third.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/validation.txt`.
**Boundary:** this is the same-condition family as F-02, but a different decision — composition, not duplication.
**Assertions:**

- A-14a `MECHANICAL` — a plan unit with a `CONDITION` member produces one line, not two. Owner: **S4**.
- A-14b `SEMANTIC_AUDIT` — the condition is attached to the action it modifies. Owner: **S2**.

**Severity:** MATERIAL. **Status:** ACTIVE.

### F-15 — instability

**Observation:** within one set under identical conditions, the same input produced different acceptance-relevant structures across three runs.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`.
**Boundary:** three runs establish that the structure varies; they do **not** establish a failure rate. No population claim is made.
**Assertions:**

- A-15a `MECHANICAL` — the acceptance-relevant structure of three same-condition runs is identical. Owner: **PROCESS**.
- A-15b `SEMANTIC_AUDIT` — where they differ, the difference is recorded by decision id, not by prose. Owner: **PROCESS**.

**Severity:** CRITICAL. **Status:** ACTIVE.

## 3. Provisional — path required

| ID | Class | Defect | Missing |
|---|---|---|---|
| F-05 | F3 | infarct evidence absent in one run of a set | the specific run and diff line |
| F-10 | F7 | `2024-02` read as the infarct date | the exact run |
| F-13 | F10 | a whole source block absent from the IR | the run |

Not usable in a brief until the path exists.

## 4. Withdrawn

- **Referral rendered under two problems.** Cannot be cited. Withdrawn; if re-observed it enters §3 with a path.
- **Residual aphasia as seizure evidence.** Under the v4 ledger, exclusion was enforced by the object's absence, not a runtime rule. Not a runtime breach; the demonstrated defect was contract contradiction (C-01).

## 5. Derived fixtures

```text
D-01  invariant: zero-member unit legal only for a closed-list standing item
      adjacent: F-06
      assertion: a unit with no members and a non-standing operator is rejected — owner S4, mechanical
      why derived: F-06 covers a missing standing item, not an invented one
```

## 6. Rules

1. A brief cites **all relevant historical fixtures** for the artifact.
2. A fixture changes only via `ACCEPTANCE CHANGE`.
3. A fixture that stops applying is marked withdrawn with the reason, never deleted.
4. A new defect reaching output is registered **before** it is fixed.
5. Evidence is a path, not a recollection.
6. Every assertion has exactly one owner.
