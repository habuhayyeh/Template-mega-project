# AX-S1S2-D — experiment-local typed test schema

**Identities:** schema `SCHEMA-3` · registry `PILOT-2` · active set `ACTIVE-PILOT-2` · oracle `ORACLE-3.0`
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
  - id: C2
    subject: "prior left MCA infarct"
    anchors: [S01]
    salience: { acuity: LOW, management_reference_spans: [] }
    claim_candidates:
      - { id: CC2, text: "known left MCA infarct", support: [S01] }
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
claim_relations:                      # per selected representation; [] when none
  - { problem: C1, representation: R1, relation: COMPETING, claims: [CC1, CC2] }
duplicate_groups: []                  # [[O03, O04]] when equivalence holds
causal_relations:                     # separate from epistemic SUPPORTS
  - { from: O02, to: O03, relation: CONTRIBUTOR, strength: POSSIBLE, support: [S01, S02] }
representations:
  - id: R1
    problem: C1
    members: [O03, O04]
    support_refs: [S02]
    selection_safe: true
  - id: R2
    problem: C2
    members: [O01, O02]
    support_refs: [S01]
    selection_safe: true
```

`representations[]` is the approved set. `selection_safe` describes whether an entry may coexist with
another approved entry for the same problem. `claim_relations[].problem` and
`claim_relations[].representation` are the selectors used by the S4 projection; an entry without
either is a schema violation.

Approval is semantic support, not member existence. The representation's `problem` identifies the S1
candidate whose claim candidate(s) the members and relations must support; real object ids and support
refs are necessary but not sufficient. `S2-REP-01` assesses that semantic support.

## S3 output

```yaml
rendered:
  - { problem: C1, approved_representation: R1, selected_rep: R1, encounter_role: PRIMARY }
  - { problem: C2, approved_representation: R2, selected_rep: R2, encounter_role: BACKGROUND }
candidate_outcomes:                   # exactly one per S1 problem candidate
  - { candidate: C1, outcome: RENDERED }
  - { candidate: C2, outcome: RENDERED }
retained: [O01, O02, O03, O04, O05, O06]
use: { O01: C2, O02: C2, O03: C1, O04: C1, O05: C1, O06: C1 }
reuse: []                             # [{object: O04, problems: [C1, C7]}] when reused
dispositions:
  - { object: O07, disposition: MEDICATION_RECORD }
```

`NOT_RENDERED` requires a typed `reason` from `REASON-1` below. A null or absent reason is a missing
typed reason; `basis` is not evaluated in that case. `basis` is a set of source object ids required
only when the reason's registry entry says it is required. `retained ∪ dispositions` equals the
substrate object set.

### S3 reason registry — REASON-1

This is the experiment-local registry for Gate 0. It is not a production taxonomy. `S3-CAND-01` checks
membership, the reason→basis requirement, non-emptiness when required, uniqueness, and target
existence. It does not check whether the reason is semantically correct; that is the separate semantic
audit named in `predicates.md`.

<!-- BEGIN:REASON_REGISTRY -->
```json
{
  "registry": "REASON-1",
  "scope": "GATE0-C2, S3-CAND-01 only; experiment-local, not a production taxonomy",
  "outcomes": ["RENDERED", "NOT_RENDERED"],
  "reasons": [
    {
      "code": "NO_APPROVED_REPRESENTATION",
      "requires_basis": true,
      "basis_target": "object",
      "basis_min_items": 1,
      "basis_must_exist_in": "oracle.objects",
      "basis_unique": true,
      "meaning": "S2 approved no representation for the candidate; basis lists the source object ids whose adjudication state establishes the absence."
    },
    {
      "code": "NOT_CLINICAL",
      "requires_basis": false,
      "basis_target": null,
      "basis_min_items": 0,
      "basis_must_exist_in": null,
      "basis_unique": false,
      "meaning": "The candidate is outside the clinical scope of the note; no upstream state reference is required."
    }
  ],
  "rules": [
    "RENDERED carries no reason and no basis.",
    "NOT_RENDERED carries exactly one reason from this registry.",
    "a null or absent reason is a missing typed reason; basis is not evaluated when the reason is missing.",
    "when the reason is present, basis is required when requires_basis is true and must be absent otherwise.",
    "every basis item is an object id present in oracle.objects.",
    "basis is a set: duplicate entries are a violation.",
    "unknown candidate ids are a violation.",
    "reason correctness is a separate semantic audit, not an S3-CAND-01 finding."
  ]
}
```
<!-- END:REASON_REGISTRY -->

The clean NOT_RENDERED calibration parent `S3_CASE01_NOT_RENDERED_CLEAN` is the reference valid
output: `C1` and `C2` outcomes, `rendered: []`, reason `NO_APPROVED_REPRESENTATION`, bases
`[O03, O04]` and `[O01, O02]`, and otherwise unchanged object accounting. "Clean" means it yields no `S3-CAND-01` finding; it does not
assert that C1 should clinically fail to render. Semantic correctness of the reason is the separate
audit named in `predicates.md`, not a Gate 0 structural check.

## S4 input view — exact source map

`S4_INPUT_VIEW` is assembled at the seam. Every value is copied from the source named below. The
projection authors nothing. The map is the sole declared projection contract: `make_seeds.py` reads
this block, binds every rule to a frozen op contract, applies one `op` per destination, and fails if a
rule is missing, duplicated, unknown or mismatched.

Each `op` also has a frozen contract in `make_seeds.py::OP_CONTRACTS`. The build compares every map
rule field — destination, owner, source, source path, condition, requirement and transform — exactly
against that contract and fails on any mismatch. The map and code cannot drift on declared metadata.

**Gate 0 shape:** one or more rendered problems. `SCHEMA-3` makes the S4 view multi-problem: it carries
all rendered problems, their S1 salience, their S3 selected representations and their S2 approved
selections. A problem with no rendered entry is not in this view; it is an S3 outcome, not an S4 input.
`P` and `R` are per-rendered-problem variables.

- `P` = `S3_PARENT.s3.rendered[i].problem`
- `R` = `S3_PARENT.s3.rendered[i].selected_rep`
- `T` = `S3_PARENT.s3.retained`

<!-- BEGIN:PROJECTION_MAP -->
```json
{
  "schema": "SCHEMA-3",
  "view": "S4_INPUT_VIEW",
  "scope": "GATE0-C2: one or more rendered problems. Each rendered problem must have one S1 candidate, one S2 approved representation and one S3 selected representation.",
  "variables": {
    "P": "S3_PARENT.s3.rendered[i].problem",
    "R": "S3_PARENT.s3.rendered[i].selected_rep"
  },
  "groups": [
    "from_s1",
    "from_s3",
    "from_s2",
    "from_ingest",
    "from_contracts"
  ],
  "contracts": {
    "section": "AP",
    "sections": [
      "AP"
    ],
    "operator_set": "PILOT-OPERATORS-1",
    "operators": [
      "FACT",
      "REASONING",
      "CLAIM",
      "PLAN"
    ]
  },
  "rules": [
    {
      "dst": "/from_s1/problems",
      "op": "s1_problems",
      "owner": "S1",
      "source": "S1_PARENT.json",
      "source_path": "/s1/candidates[id in rendered]/{id,salience}",
      "condition": "one entry per rendered problem, S3 order",
      "required": "required",
      "transform": "collect objects"
    },
    {
      "dst": "/from_s3/selected_reps",
      "op": "s3_selected_reps",
      "owner": "S3",
      "source": "S3_PARENT.json",
      "source_path": "/s3/rendered[i]/{problem,selected_rep}",
      "condition": "all i, source order",
      "required": "required",
      "transform": "collect problem->rep map"
    },
    {
      "dst": "/from_s3/selected_roles",
      "op": "s3_selected_roles",
      "owner": "S3",
      "source": "S3_PARENT.json",
      "source_path": "/s3/rendered[i]/{problem,encounter_role}",
      "condition": "all i, source order",
      "required": "required",
      "transform": "collect problem->role map"
    },
    {
      "dst": "/from_s3/rendered",
      "op": "s3_rendered",
      "owner": "S3",
      "source": "S3_PARENT.json",
      "source_path": "/s3/rendered[i]/problem",
      "condition": "all i, source order",
      "required": "required",
      "transform": "collect problem ids"
    },
    {
      "dst": "/from_s3/retained",
      "op": "s3_retained",
      "owner": "S3",
      "source": "S3_PARENT.json",
      "source_path": "/s3/retained[i]",
      "condition": "all i, source order",
      "required": "required",
      "transform": "collect ids"
    },
    {
      "dst": "/from_s3/use",
      "op": "s3_use",
      "owner": "S3",
      "source": "S3_PARENT.json",
      "source_path": "/s3/use/{object}",
      "condition": "object keys must be a subset of T",
      "required": "required",
      "transform": "copy map"
    },
    {
      "dst": "/from_s3/reuse",
      "op": "s3_reuse",
      "owner": "S3",
      "source": "S3_PARENT.json",
      "source_path": "/s3/reuse[i]",
      "condition": "all i, source order",
      "required": "required",
      "transform": "copy list"
    },
    {
      "dst": "/from_s2/selections",
      "op": "s2_selections",
      "owner": "S2",
      "source": "S2_PARENT.json",
      "source_path": "/s2/representations[id=R]/members + /s2/relations + /s2/claim_relations + /s2/duplicate_groups",
      "condition": "one per rendered problem; R = selected_reps[P]; relations filtered to members; claim relations filtered P/R; duplicate groups intersect members",
      "required": "required",
      "transform": "collect objects"
    },
    {
      "dst": "/from_s2/causal_relations",
      "op": "s2_causal_relations",
      "owner": "S2",
      "source": "S2_PARENT.json",
      "source_path": "/s2/causal_relations[i]",
      "condition": "from or to in T; source order",
      "required": "required",
      "transform": "filter and copy"
    },
    {
      "dst": "/from_ingest",
      "op": "oracle_ingest",
      "owner": "I3/I4",
      "source": "fixtures/CASE-01/oracle.json",
      "source_path": "/objects[{object in T}]/{text,provenance,temporal|status}",
      "condition": "one entry per T; exactly one of temporal/status",
      "required": "payload and provenance required; exactly one of temporal/status",
      "transform": "text→payload; copy provenance; copy temporal or status",
      "expands": {
        "/from_ingest/{object}/payload": "/objects[{object in T}]/text",
        "/from_ingest/{object}/provenance": "/objects[{object in T}]/provenance",
        "/from_ingest/{object}/temporal": "/objects[{object in T}]/temporal when present",
        "/from_ingest/{object}/status": "/objects[{object in T}]/status when temporal is absent"
      }
    },
    {
      "dst": "/from_contracts/section",
      "op": "contract_section",
      "owner": "frozen contracts",
      "source": "SCHEMA-3 contracts block",
      "source_path": "#/contracts/section",
      "condition": "always",
      "required": "required",
      "transform": "copy constant"
    },
    {
      "dst": "/from_contracts/operator_set",
      "op": "contract_operator_set",
      "owner": "frozen contracts",
      "source": "SCHEMA-3 contracts block",
      "source_path": "#/contracts/operator_set",
      "condition": "always",
      "required": "required",
      "transform": "copy constant"
    }
  ]
}
```
<!-- END:PROJECTION_MAP -->

`from_contracts` is deliberately narrow for Gate 0: section `AP` and operator set
`PILOT-OPERATORS-1 = {FACT, REASONING, CLAIM, PLAN}`. No style contract is projected because this
campaign freezes none. No ordering contract is projected because `S4-ORD-01` is `PENDING_DEPENDENCY`.
`PILOT-2` is the predicate registry identity and is not used as an operator contract.

Any key outside the five mapped groups is a packaging violation. Any value that does not match its
mapped source path is a packaging violation. Ordering is absent from S4's input view.

## S4 blueprint

```yaml
sections: [AP]
problems:
  - { id: P1, source: C1, order: 1, encounter_role: PRIMARY }
  - { id: P2, source: C2, order: 2, encounter_role: BACKGROUND }
units:
  - id: U1
    problem: P1
    representation: R1
    members: [O03, O04]
    roles: { O03: HEAD, O04: MODIFIER }
    operator: FACT
    order: 10
  - id: U2
    problem: P1
    representation: R1
    members: [O05]
    roles: { O05: HEAD }
    operator: PLAN
    order: 20
  - id: U3
    problem: P1
    representation: R1
    members: [O06]
    roles: { O06: HEAD }
    operator: PLAN
    order: 30
  - id: U4
    problem: P2
    representation: R2
    members: [O01, O02]
    roles: { O01: HEAD, O02: MODIFIER }
    operator: FACT
    order: 40
```

## Field → predicate map

| predicate | reads |
|---|---|
| `S1-AUTH-01` | absence of adoption/final-state fields in `candidates[*]` |
| `S1-AUTH-02` | absence of selected-claim fields in `candidates[*]` |
| `S1-CAND-01` | `candidates[*]` vs oracle excluded concepts, by concept identity |
| `S1-CAND-02` | `candidates[*].anchors` non-empty |
| `S2-REP-01` | `representations[*]` members, relations and `support_refs` versus the problem's claim; semantic support, not ref existence alone |
| `S2-TEMP-01` | `adjudication[*].temporal` vs substrate |
| `S2-ADOPT-01` | `adjudication[*].adoption` vs oracle |
| `S3-CAND-01` | `candidate_outcomes` coverage, exclusivity, unknown ids, REASON-1 reason/basis, equality with `rendered` |
| `S3-INC-01` | `rendered[*]` with null `approved_representation` |
| `S3-SEL-01` | `selected_rep` in the approved set |
| `S3-ACCT-01` | `retained` ∪ `dispositions` = substrate set |
| `S4-INC-01` | `problems[]` vs S3 rendered set |
| `S4-MEM-01` | `units[*].members` subset of `retained` |
| `S4-COMP-01` | every problem in S4 ∩ S3 has a claim-bearing unit; every retained plan item has a plan unit |
| `S4-REP-01` | `units[*].representation` = `selected_reps[unit.problem→source]` |
| `S4-PROJ-01` | `s4_input_view`, including `selected_roles` and selected causal relations, against the exact PROJECTION_MAP above |
