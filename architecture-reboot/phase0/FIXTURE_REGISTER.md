# FIXTURE_REGISTER — the failures that reached output

Each fixture records a defect, its evidence path, and its **assertions**. Every assertion has exactly one owner: if a property spans two submodules, it is two assertions.

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

### F-02, F-03, F-04 — duplication

**Defect:** the infarct (F-02), the CT findings (F-03), and the family memory concern (F-04) each rendered twice within one problem block.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`.
**Assertions:**

- A-02a `MECHANICAL` — an object id appears in at most one unit per (section, problem). Owner: **S4**.
- A-02b `SEMANTIC_AUDIT` — two objects asserting the same proposition do not both render. Owner: **S2**.

Both are needed: the old duplicates had different object ids, so the id rule alone would have passed them.

### F-06 — missing required line

**Defect:** `Seizure precautions` was absent from the plan.
**Evidence:** `PACKAGE.md` before and after the standing-item contract was added; presence in `set2/run1–3.txt` and `set3/run1–3.txt`.
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
**Evidence:** `runs/2026-11-14-p003-doximity/set2/` raw runs and validation records — not the oracle alone.
**Assertions:**

- A-11a `SEMANTIC_AUDIT` — a prior recommendation does not render in the plan without an adoption statement. Owner: **S2**.

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

- A-C01a `MECHANICAL` — the build fails when two rules own one decision with incompatible normative fields. Owner: **BUILD**.

### C-02 — non-local regression

**Defect:** the `EVIDENCE_MODE` requirement added for `COURSE` conflicted with the existing `SECTION_CONTRACT` rule 38 governing the same text, and the `O51` statement moved as an unrelated effect.
**Evidence:** `artifacts/06_doximity_run3.md`.
**Assertions:**

- A-C02a `MEASURED` — after any contract change, the frozen case is re-run and the IR diffed. Owner: **process**.

### C-12 — faithful but clinically empty

**Defect:** the artifact rendered `The MRI to show.` — grammatical, supported, carrying none of the claim's payload.
**Evidence:** `artifacts/doximity_bplus_operator_experiment_2026-11-15.md`.
**Boundary:** that is the historical artifact's wording. It is **not** D-017's signer-approved `MRI to show.`; the two must not be cited interchangeably.
**Assertions:**

- A-C12a `MECHANICAL` — a rendered line carries every content token of its head member. Owner: **R1**.
- A-C12b `SEMANTIC_AUDIT` — a fuller operator is not passed over in favour of a thinner one. Owner: **S4**.

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
