# AX-S1S2-D — experiment-local typed test schema

**Identities:** schema `SCHEMA-2` · registry `PILOT-2` · active set `ACTIVE-PILOT-2` · oracle `ORACLE-2.0`
**Scope:** post-DC-002 only. No legacy fields, no dual schema.

---

## S1 output

```yaml
candidates:
  - id: C1
    subject: "falls since June"
    anchors: [S02]
    salience:
      acuity: MODERATE
      management_reference_spans: [S03]     # list of span ids; empty list when none
    claim_candidates:
      - { id: CC1, text: "three falls since June", support: [S02] }
    relationships: []                        # optional, canonical candidate-level only
```

Forbidden fields are a closed set defined only in `predicates.md`: adoption and final-state fields
(`S1-AUTH-01`), selected-claim fields (`S1-AUTH-02`).

## S2 output

```yaml
adjudication:
  - object: O03
    temporal: "June–November"        # copied verbatim from the substrate
    adoption: true | false | null
    evidence: [S02]                  # non-empty when adoption is true, else null
relations:                            # object-level, source-grounded
  - { type: SUPPORTS, from: O04, to: O03 }
claim_relations: []                   # among claim candidates; [] when none
duplicate_groups: []                  # [[O03, O04]] when equivalence holds
representations:
  - id: R1
    problem: C1
    members: [O03, O04]
    support_refs: [S02]
    selection_safe: true
```

`representations[]` is the approved set. `selection_safe` describes whether an entry may coexist with
another approved entry for the same problem.

## S3 output

```yaml
rendered:
  - { problem: C1, approved_representation: R1, selected_rep: R1 }
candidate_outcomes:                   # exactly one per S1 problem candidate
  - { candidate: C1, outcome: RENDERED }
  - { candidate: C2, outcome: NOT_RENDERED, reason: NO_APPROVED_REPRESENTATION, basis: [S02] }
retained: [O03, O04, O05, O06]
use: { O03: C1, O04: C1, O05: C1, O06: C1 }
reuse: []                             # [{object: O04, problems: [C1, C7]}] when reused
dispositions:
  - { object: O01, disposition: HISTORICAL_CONTEXT }
```

`NOT_RENDERED` requires a typed `reason`. `basis` is required when the reason family depends on
upstream state. `retained ∪ dispositions` equals the substrate object set.

## S4 input view — observable

Recorded as an artifact so `S4-PROJ-01` is scored, not asserted. Every field is **copied** from its
source; the projection authors nothing.

| group | fields | copied from |
|---|---|---|
| `from_s1` | `problem`, `salience` | S1 candidate |
| `from_s3` | `selected_rep`, `rendered`, `retained`, `use`, `reuse` | S3 output |
| `from_s2` | `members`, `relations`, `claim_relations`, `duplicate_groups` | S2 output |
| `from_ingest` | per object: `payload`, `provenance`, `temporal` or `status` | I3/I4 |
| `from_contracts` | `section`, `operator_set` | frozen contracts |

Any key outside these groups is a packaging violation. Ordering is absent: no ordering contract exists
yet, and `S4-ORD-01` is `PENDING_DEPENDENCY`.

## S4 blueprint

```yaml
sections: [AP]
problems:
  - { id: P1, source: C1, order: 1 }
units:
  - id: U1
    problem: P1
    representation: R1
    members: [O03, O04]
    roles: { O03: HEAD, O04: MODIFIER }
    operator: FACT
    order: 10
```

## Field → predicate map

| predicate | reads |
|---|---|
| `S1-AUTH-01` | absence of adoption/final-state fields in `candidates[*]` |
| `S1-AUTH-02` | absence of selected-claim fields in `candidates[*]` |
| `S1-CAND-01` | `candidates[*]` vs oracle excluded concepts, by concept identity |
| `S1-CAND-02` | `candidates[*].anchors` non-empty |
| `S2-REP-01` | `representations[*].support_refs` non-empty |
| `S2-TEMP-01` | `adjudication[*].temporal` vs substrate |
| `S2-ADOPT-01` | `adjudication[*].adoption` vs oracle |
| `S3-CAND-01` | `candidate_outcomes` coverage, exclusivity, unknown ids, reason, basis, equality with `rendered` |
| `S3-INC-01` | `rendered[*]` with null `approved_representation` |
| `S3-SEL-01` | `selected_rep` in the approved set |
| `S3-ACCT-01` | `retained` ∪ `dispositions` = substrate set |
| `S4-INC-01` | `problems[]` vs S3 rendered set |
| `S4-MEM-01` | `units[*].members` subset of `retained` |
| `S4-COMP-01` | every problem in S4 ∩ S3 has a claim-bearing unit; every retained plan item has a plan unit |
| `S4-REP-01` | `units[*].representation` = S3 `selected_rep` |
| `S4-PROJ-01` | `s4_input_view` keys within the five groups; values trace to their source |
