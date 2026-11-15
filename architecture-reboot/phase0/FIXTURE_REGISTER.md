# FIXTURE_REGISTER — the failures that reached output

Each fixture names its class, the defect it encodes, the evidence, and who owns it. **A fixture without a citable evidence path is not mandatory** — it moves to §3 and cannot be used in an acceptance brief until the path is supplied.

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

## 2. Mandatory fixtures — evidence cited

| ID | Class | Defect | Evidence | Required behaviour | Owner | Decides |
|---|---|---|---|---|---|---|
| F-02 | F2 | infarct rendered as one bullet in some runs, two in others | `runs/2026-11-14-p003/set3/run1–3.txt` | one unit per object per section+problem | S4 | mechanical |
| F-03 | F2 | CT findings duplicated the same way | same set | as F-02 | S4 | mechanical |
| F-04 | F2 | family memory concern rendered twice in one block | same set | as F-02 | S4 | mechanical |
| F-06 | F3 | `Seizure precautions` absent from the plan | `PACKAGE.md` shipped without the standing-item list; present 3/3 in `set2` and `set3` once it was added | package must include the standing-item contract; the unit exists when triggered | BUILD (primary), S4 (secondary) | mechanical |
| F-11 | F8 | prior `no further workup [2025-06]` appeared in today's plan | `oracles/ap_ledger_v4.txt`, O52 disposition | historical never renders in plan without adoption | S2 | semantic |
| F-12 | F9 | conversational first-person phrasing in the A/P | D-017; the MRI adjudication bullet in `set3` | section-scoped voice | R1 | mechanical |
| C-01 | C11 | `05` carried "reasoning before facts" and "reasoning after facts" in adjacent sections | `pipeline/05_WRITE_AP.md` history, `proposals/P003-ap-render.md` | build lint fails; no artifact produced | BUILD | mechanical |
| C-02 | C14 | adding a clause for one statement moved an unrelated one | the O51 statement after the O57 clause was added | re-run the frozen case after any contract change; diff the IR | process, not a module | measured |

## 3. Provisional — evidence path still required

Real failures I can describe but cannot yet cite. **Not usable in an acceptance brief** until the path is filled. This is the honest state, not a placeholder.

| ID | Class | Defect | What is missing | Owner if confirmed |
|---|---|---|---|---|
| F-01 | F1 | a run invented `postictal confusion resolved` | it is `set1/run1`, but the condition was a deliberate control — no dispatcher, no standing items. As a fixture it tests the **execution envelope**, not the extraction guard. Restate before use | I3 (envelope) |
| F-05 | F3 | infarct evidence absent in one run of a set | the specific run and diff line | S3 |
| F-07 | F4 | a free-text `REUSE` line broke the output schema | observed in a local run of `05`; Doximity reproduction not established | S4 (producer), R1 (fail-closed) |
| F-10 | F7 | `2024-02` read as the infarct date | the run | S2 |
| F-13 | F10 | a whole source block absent from the IR | the run | I2 |

## 4. Withdrawn as unverified

- **Referral rendered under two problems.** Proposed as F-09; I cannot cite it in the canonical artifacts. Withdrawn. If re-observed, it enters §3 with a path.
- **Residual aphasia as seizure evidence (old F-15).** Under the v4 ledger the exclusion was enforced by the object's absence, not by a runtime rule. That was **not** a runtime breach; the demonstrated defect was contract contradiction (C11), and it now belongs there.

## 5. Derived fixtures

Allowed only for an invariant no historical case covers, and must name the historical class beside it.

```text
D-01  invariant: zero-member unit legal only for a closed-list standing item
      adjacent: F-06
      required: a unit with no members and a non-standing operator is rejected
      owner: S4   decides: mechanical
      why derived: F-06 covers a missing standing item, not an invented one
```

## 6. Rules

1. Every acceptance brief cites at least one mandatory fixture.
2. A fixture changes only via `ACCEPTANCE CHANGE`.
3. A fixture that stops applying is marked withdrawn with the reason, never deleted.
4. When a new defect reaches output, it is registered **before** it is fixed.
5. A fixture whose evidence cannot be produced is not evidence, and does not belong in §2.
