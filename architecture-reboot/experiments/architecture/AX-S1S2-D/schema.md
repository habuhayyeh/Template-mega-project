# AX-S1S2-D — experiment-local typed test schema

The mechanical predicates need named fields to compare. This is the schema the pilot artifacts must conform to; it is local to the experiment and is not the production Case IR.

---

## S1 output

```yaml
candidates:
  - id: C1
    subject: "recurrent falls"
    anchors: [S02]
    salience: { acuity: MODERATE, managed_today: true }
    candidate_claims:
      - { id: CC1, text: "three falls since June", support: [S02] }
    relationships:                   # optional, canonical candidate-level relations only
      - { type: SUPPORTS, target: C2 }
```

Forbidden fields are defined **only** in `predicates.md` (`S1-AUTH-01` for adoption/final-state, `S1-AUTH-02` for selected-claim). This file never restates them: a second copy is a second authority, and the two drifted twice.

## S2 output

```yaml
adjudication:
  - object: O03
    temporal: "June–November"        # must equal the substrate value
    adoption: true | false | null
    evidence: [S02]                  # required when adoption is true; null otherwise
representations:
  - id: R1
    problem: C1
    members: [O03, O05]
    support_refs: [S02, S03]
    selection_safe: true | false     # required only when >1 approved for a problem
```

`temporal` is compared to the substrate verbatim. `support_refs` must be non-empty. `evidence` must be non-empty when `adoption: true`.

**`representations[]` is the approved set** — S2 emits only representations it approves, so anything present is approved by definition. `selection_safe` therefore describes whether that entry may coexist with another approved entry for the same problem.

## S3 output

```yaml
rendered:
  - problem: C1
    approved_representation: R1      # null means not approved, and the problem must not render
    selected_rep: R1                 # must be present in S2's approved set for C1
retained: [O03, O05]
dispositions:
  - { object: O04, disposition: NOT_USED }
```

`retained ∪ dispositions` must equal the substrate object set. No `reason` field is required.

## S4 blueprint

```yaml
sections: [AP]
problems:
  - { id: P1, source: C1, order: 1 }
units:
  - { id: U1, problem: P1, representation: R1, members: [O03, O05], operator: FACT, order: 10 }
```

Checks: every `P*` maps to an S3-rendered problem; no extra or missing problem; every `unit.representation` equals the S3 `selected_rep` for that problem; every `unit.members[]` exists in `retained`.

---

## Field → predicate map

| predicate | fields it reads |
|---|---|
| `S1-AUTH-01` | absence of `adopted`/`adoption`/`adoption_verdict`/`resolved`/`status_current` in `candidates[*]` |
| `S1-AUTH-02` | absence of `selected_claim`/`final_claim`/`chosen_claim` |
| `S1-CAND-01` | `candidates[*]` vs `oracle.expected.candidate_concepts_must_exclude`, by concept identity |
| `S1-CAND-02` | `candidates[*].anchors` non-empty |
| `S2-REP-01` | `representations[*].support_refs` non-empty |
| `S2-TEMP-01` | `adjudication[*].temporal` vs substrate |
| `S2-ADOPT-01` | `adjudication[*].adoption` vs case expectation |
| `S3-INC-01` | `rendered[*]` where `approved_representation is null` |
| `S3-SEL-01` | `selected_rep` ∈ S2 approved set |
| `S3-ACCT-01` | `retained ∪ dispositions` = substrate set |
| `S4-INC-01` | `problems[]` vs S3 rendered set |
| `S4-MEM-01` | `units[*].members` ⊆ `retained` |
| `S4-COMP-01` | every rendered problem has a claim-bearing unit; every S3-retained plan item has a plan unit |

**Map scope.** The table covers predicates ACTIVE in the pilot. `S2-REP-02` (`representations[*].selection_safe`) and `S4-REP-01` (`units[*].representation` vs S3 `selected_rep`) are defined by this schema but not scored yet — no pilot case produces their condition — so their rows are omitted rather than listed as if scored. `S2-ADOPT-02` is absent entirely: its missing dependency is explicit-link semantics, not a field.
