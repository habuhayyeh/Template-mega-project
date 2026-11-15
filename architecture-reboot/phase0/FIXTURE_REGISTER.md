# FIXTURE_REGISTER — the failures that reached output

Every fixture here is a defect that produced a wrong note, not a case someone imagined. Each names its failure class, the submodule that owns it, and how it is decided.

Derived fixtures are allowed only for an invariant no historical case covers, and must name the historical class they sit beside.

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

## 2. Mandatory historical fixtures

| ID | Class | Case | Required behaviour | Owner | Decides |
|---|---|---|---|---|---|
| F-01 | F1 | a run with no dispatcher invented `postictal confusion resolved` | no object without span support; extraction fails | I3 | mechanical (token containment) |
| F-02 | F2 | infarct rendered twice in one problem block | one unit per object per section+problem | S4 | mechanical |
| F-03 | F2 | CT rendered twice in one problem block | as F-02 | S4 | mechanical |
| F-04 | F2 | family memory concern rendered twice | as F-02 | S4 | mechanical |
| F-05 | F3 | infarct evidence dropped between runs | object used or dispositioned | S3 | mechanical |
| F-06 | F3 | `Seizure precautions` missing from the plan | required standing item present when triggered | S4 | mechanical |
| F-07 | F4 | free-text `REUSE` line on a repeated run | unit must typecheck; renderer emits `CONTRACT_ERROR` | R1 | mechanical |
| F-08 | F5 | three runs, three different fact sets | IR diff across runs is the measurement | S1–S4 | measured |
| F-09 | F6 | memory referral rendered under both problems | one home per section+problem | S3 | mechanical |
| F-10 | F7 | `2024-02` rendered as the infarct date | provenance parenthesis carries the date, not the event | S2 | semantic |
| F-11 | F8 | prior `no further workup` appeared in today's plan | historical never renders in plan without adoption | S2 | mechanical |
| F-12 | F9 | first person in the A/P | voice rule per section | R1 | mechanical |
| F-13 | F10 | a whole source block dropped | every span dispositioned | I2 | mechanical |
| F-14 | C12 | `MRI to show.` from a two-clause source claim | operator must render its payload | S4 | mechanical |
| F-15 | C13 | residual aphasia rendered as seizure evidence | object used only under the problem it explains | S3 | semantic |

## 3. Derived fixtures

Allowed only for invariants with no historical case. Format:

```text
D-01  invariant: zero-member unit only for closed-list standing item
      adjacent class: F-06
      required: unit with no members and non-standing operator is rejected
      owner: S4   decides: mechanical
      justification: F-06 covers a missing standing item, not an invented one
```

## 4. Rules for using the register

1. Every acceptance brief cites at least one historical fixture.
2. A fixture may change only via `ACCEPTANCE CHANGE`.
3. A fixture that no longer applies is marked withdrawn with the reason, never deleted.
4. When a new defect reaches output, it is added here before it is fixed. The fixture comes first; that is what stops a fix from being a guess.

## 5. What the register is not

It is not a test suite. It is the list of things that have gone wrong, each with the check that would have caught it. The test suite is generated from it.
