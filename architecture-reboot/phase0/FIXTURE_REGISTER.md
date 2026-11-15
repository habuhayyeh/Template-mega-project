# FIXTURE_REGISTER — the failures that reached output

Each fixture records a defect, its evidence path, its owner, and how it is decided. A fixture whose evidence cannot be produced does not belong in §2.

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
| C14 | non-local regression after a contract change |

## 2. Mandatory fixtures

### F-01 — fabrication

**Defect:** a run produced `postictal confusion resolved`, which no source supported.
**Evidence:** `runs/2026-11-14-p003-doximity/run1.txt` — a deliberate control: no dispatcher, no standing items.
**Boundary:** this tests the **whole envelope**, not the extraction guard alone. Its cause was an under-specified call; it must not be cited as proof that I3 alone failed.
**Required:** nothing renders without span support.
**Owner:** I3 (guard), envelope (cause). **Decides:** mechanical.

### F-02, F-03, F-04 — duplication

**Defect:** the infarct (F-02), the CT findings (F-03), and the family memory concern (F-04) each rendered twice within one problem block.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`.
**Required, two levels:**

- mechanical — an object id appears in at most one unit per (section, problem);
- semantic — two distinct objects asserting the same proposition must not both render; the audit decides identity, not the checker.

**Owner:** S4 (mechanical), S2 (identity). **Decides:** MECHANICAL and SEMANTIC.

Both levels are needed because the old failures were *semantic* duplicates — the object ids differed, so an id-based rule alone would have passed them.

### F-06 — missing required line

**Defect:** `Seizure precautions` was absent from the plan.
**Evidence:** `PACKAGE.md` before and after the standing-item contract was added; presence confirmed in `runs/2026-11-14-p003-doximity/set2/run1.txt`, `set2/run2.txt`, `set2/run3.txt` and `set3/run1.txt`, `set3/run2.txt`, `set3/run3.txt`. The defect was packaging, not model judgement.
**Required:** a package declaring standing items must carry their contract; S4 emits the unit when the trigger is met.
**Owner:** BUILD (primary), S4 (secondary). **Decides:** mechanical.

### F-11 — prior recommendation promoted

**Defect:** a prior `no further workup [2025-06]` appeared in the current plan.
**Evidence:** `runs/2026-11-14-p003-doximity/set2/` raw runs and their validation records — not the oracle alone. The oracle recorded the disposition after the fact; the runtime behaviour is the evidence.
**Required:** a prior recommendation does not render in the plan without an adoption statement.
**Owner:** S2. **Decides:** semantic.

### F-12 — voice

**Defect:** first person and conversational framing in the A/P.
**Evidence:** `runs/2026-11-14-p003-doximity/set3/run3.txt`.
**Required:** section-scoped voice; the A/P is impersonal (D-017).
**Owner:** R1. **Decides:** mechanical.

### C-01 — contract contradiction

**Defect:** two clauses in `05` governed the same ordering decision — one put reasoning before the fact lines, the other put facts before reasoning. The writer obeyed a different one per run.
**Evidence:** `proposals/P003-ap-render.md` §1, and `pipeline/05_WRITE_AP.md` at the rewrite — one decision, two owners.
**Required:** the build fails when two rules own one decision.
**Owner:** BUILD. **Decides:** mechanical.

### C-02 — non-local regression

**Defect:** adding the `EVIDENCE_MODE` requirement for `COURSE` collided with an existing rule governing course text, and moved the `O51` statement, which had nothing to do with the change.
**Evidence:** `artifacts/06_doximity_run3.md` — the `EVIDENCE_MODE` requirement against `SECTION_CONTRACT` rule 38; the `O51` statement moved when the clause was added.
**Required:** after any contract change, re-run the frozen case and diff the IR.
**Owner:** process, not a module. **Decides:** measured.

### C-12 — faithful but clinically empty

**Defect:** the artifact rendered `The MRI to show.` — grammatical, supported, carrying none of the claim's payload.
**Evidence:** the B+ operator experiment, `artifacts/doximity_operator_stress_results_2026-11-15.md`.
**Boundary:** that is the historical artifact's exact wording. It is **not** D-017's signer-approved `MRI to show.`, which is a deliberate impersonal form. The two must not be cited interchangeably.
**Required:** an operator may not discard a member's payload; where a fuller operator exists, the thinner one is not selected.
**Owner:** S4 (operator choice), R1 (payload retention). **Decides:** mechanical for payload coverage, semantic for operator fit.

### F-07 — malformed output

**Defect:** a free-text `REUSE` line broke the output schema on a repeated run.
**Evidence:** `artifacts/06_doximity_run3.md` — not a local run. An earlier local observation was a different event and is not this evidence.
**Required:** the unit fails to typecheck; the renderer emits `CONTRACT_ERROR` and the run fails.
**Owner:** S4 (producer), R1 (fail-closed). **Decides:** mechanical.

## 3. Provisional — path required

| ID | Class | Defect | Missing |
|---|---|---|---|
| F-05 | F3 | infarct evidence absent in one run of a set | the specific run and diff line |
| F-10 | F7 | `2024-02` read as the infarct date | the exact run; the prior-note display case is known but not pinned to a file |
| F-13 | F10 | a whole source block absent from the IR | the run |

Not usable in a brief until the path exists.

## 4. Withdrawn

- **Referral rendered under two problems.** Cannot be cited. Withdrawn; if re-observed it enters §3 with a path.
- **Residual aphasia as seizure evidence.** Under the v4 ledger, exclusion was enforced by the object's absence, not a runtime rule. Not a runtime breach. The demonstrated defect was contract contradiction (C-01).

## 5. Derived fixtures

```text
D-01  invariant: zero-member unit legal only for a closed-list standing item
      adjacent: F-06
      required: a unit with no members and a non-standing operator is rejected
      owner: S4   decides: mechanical
      why derived: F-06 covers a missing standing item, not an invented one
```

## 6. Rules

1. A brief cites at least one fixture; historical preferred.
2. A fixture changes only via `ACCEPTANCE CHANGE`.
3. A fixture that stops applying is marked withdrawn with the reason, never deleted.
4. A new defect reaching output is registered **before** it is fixed.
5. Evidence is a path, not a recollection.
