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
      - { id: CC1, text: "gait instability from deconditioning", support: [S02, S03] }
```

Forbidden fields: `adopted`, `adoption`, `selected_claim`, `current`, `resolved`.

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
| `S1-AUTH-01` | absence of `adopted`/`adoption`/`selected_claim` in `candidates[*]` |
| `S1-AUTH-02` | absence of `selected_claim` |
| `S1-CAND-02` | `candidates[*].anchors` non-empty |
| `S2-REP-01` | `representations[*].support_refs` non-empty |
| `S2-TEMP-01` | `adjudication[*].temporal` vs substrate |
| `S2-ADOPT-01` | `adjudication[*].adoption` vs case expectation |
| `S2-CONF-01` | non-selected assertion still present in `adjudication` |
| `S3-INC-01` | `rendered[*]` where `approved_representation is null` |
| `S3-SEL-01` | `selected_rep` ∈ S2 approved set |
| `S3-ACCT-01` | `retained ∪ dispositions` = substrate set |
| `S4-INC-01` | `problems[]` vs S3 rendered set |
| `S4-MEM-01` | `units[*].members` ⊆ `retained` |
| `S4-COMP-01` | every rendered problem has a claim-bearing unit; every S3-retained plan item has a plan unit |

Predicates marked `PENDING_SCHEMA` in `predicates.md` are absent here on purpose: the schema does not yet expose `selection_safe` and `representation id` well enough for those checks, and inventing fields to make a predicate pass is how a schema stops meaning anything.
