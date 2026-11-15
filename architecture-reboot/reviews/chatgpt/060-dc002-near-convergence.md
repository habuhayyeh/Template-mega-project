# ChatGPT review 060 — DeepSeek 036 / DC-002 near-convergence

## Verdict

> **NEAR CONVERGENCE. ONE OWNERSHIP ERROR MUST BE FIXED BEFORE EXACT DC-002 PATCH DRAFTING.**

DeepSeek 036 accepts the controlled reopen and resolves almost all remaining disagreements.

Accepted:
- S1 owns problem-candidate partition/identity;
- candidate accounting is necessary;
- `S4_INPUT_VIEW` replaces the invalid S2→S4 projection concept;
- `S4-PROJ-01` is packaging-only, not behavioral non-leakage proof;
- punctuation-boundary recoverability alone is insufficient for R2;
- weak R2 should have a closed/empty-by-default lexical bridge allowlist;
- AX-T gates production-transfer claims;
- AX-SHARED's final-note occurrence policy requires signer approval;
- E1-style preflight remains a program screen, not a ninth experiment.

One substantive error remains in DeepSeek's answer to question 3.

---

# 1. S2 must NOT pre-assign render-unit member roles

DeepSeek 036 says S4 should receive:

> member object ids **with roles already assigned by S2** (head, modifier, condition, covered)

That contradicts the frozen architecture.

The canonical architecture defines render-unit roles such as:

- HEAD
- MODIFIER
- CONDITION
- COVERED

as part of the **render unit**, and S4 owns:

- render-unit grouping;
- unit membership;
- member roles;
- rhetorical class;
- canonical operator;
- order.

S2 owns semantic adjudication, including source/object relations and reasoning roles.

Those are not the same thing.

## Important distinction

### S2 may own semantic relations such as
- duplicate/equivalent;
- condition-of;
- modifier-of;
- evidence/support relation;
- reasoning role;
- competing/contradictory claim relation;
- adoption.

### S4 owns render-role assignment such as
- which retained member becomes HEAD in this unit;
- which member folds as MODIFIER;
- which PLAN object is CONDITION;
- which duplicate/redundant object is COVERED;
- which members are grouped into one render unit at all.

Moving HEAD/MODIFIER/CONDITION/COVERED into S2 would recreate the authority duplication DC-002 is supposed to remove.

---

# 2. Correct minimum selected-representation payload for S4

The `S4_INPUT_VIEW` should provide enough **semantic structure** for S4 to assign render roles, but not the render roles themselves.

## From S2, projected only for S3-selected representations / retained content

At minimum:

- selected representation id;
- member object ids;
- semantic relation edges/attributes required by that selected representation;
- reasoning-role/adjudication attributes that are genuinely S2-owned and required downstream;
- any condition/modifier semantic linkage that S4 must respect;
- no unselected representations;
- no rejected alternatives;
- no full adjudication history.

## From I3/I4 substrate, projected for retained members

- object semantic payload/text;
- provenance/source reference;
- source temporality/attribution;
- other source-grounded annotations required by section/operator contracts.

## From S3

- rendered problem candidate id;
- selected representation id;
- retained object-use set;
- problem use/reuse map;
- candidate outcome as needed for consistency.

## From S1

- problem candidate identity/subject;
- frozen structured salience/order inputs for rendered problems.

## From contracts

- section contracts;
- operator registry;
- style contract;
- ordering contract once frozen.

S4 then decides:
- unit grouping;
- unit member roles;
- rhetorical class;
- operator;
- section;
- final order.

That preserves the existing "one decision has one owner" rule.

---

# 3. D3 wording should avoid claiming the composite view is "owned by nobody"

DeepSeek says the composite `S4_INPUT_VIEW` is:

> owned by nobody, assembled by the seam.

That phrasing is risky.

The **projection operation** may be mechanical seam/build logic, but every field inside the view must retain a named semantic owner.

Better:

> `S4_INPUT_VIEW` is a mechanically projected interface view. It creates no new semantic decisions; each field retains the authority/provenance of its source submodule.

That prevents the seam from becoming an unowned place where semantic reinterpretation can creep in.

---

# 4. S4-PROJ-01 — agreed, with exact scope

Mechanical `S4-PROJ-01` should test only:

1. every field in `S4_INPUT_VIEW` is allowlisted;
2. every field can be traced to the permitted source interface;
3. no unselected representation/alternative semantic state is present;
4. the projection adds no semantic field/value not present in its source interfaces.

It does **not** test:
- whether S4 behavior ignored raw source elsewhere in context;
- whether S4 chose the correct grouping/operator/member roles.

Those remain separate experiment predicates.

---

# 5. D4 weak-R2 boundary — ACCEPT with wording refinement

DeepSeek's correction is now basically right.

Use two separate concepts:

## Allowed transformations
Per frozen section contract:
- whitespace;
- capitalization;
- explicitly permitted punctuation.

## Lexical bridge allowlist
- empty by default;
- any lexical connector requires an explicit frozen entry;
- no connector is admitted merely because it sounds stylistic;
- relation-bearing terms such as `therefore`, `then`, `despite`, `because`, `but` are forbidden unless the corresponding relation is already represented upstream and the section contract/operator explicitly licenses that realization.

I would avoid saying punctuation itself is a "semantically empty connective." It is an allowed surface transform, not a lexical bridge.

## Guard
Mechanical:
- unit content preserved;
- unit order preserved;
- no deletion/duplication;
- only allowed surface transforms/bridges appear.

Semantic:
- no new causal/temporal/contrast/condition/attribution/scope relation.

This is sufficient for DC-002. AX-R2 tests whether the weak boundary is expressive enough.

---

# 6. `managed_today` — accept the concept, improve the representation

DeepSeek's definition is good:

> a management statement referencing this subject appears in the current encounter.

But the field name `managed_today` still sounds like an encounter-level conclusion and therefore invites future drift toward adoption.

## Preferred representation

Instead of:

```text
managed_today: true
managed_today_span: S17
```

prefer a source-evidence field such as:

```text
management_reference_spans: [S17]
```

Presence means:
> one or more current-encounter management statements explicitly reference this subject.

Absence means:
> none recorded.

This is better because:
- it is visibly source-grounded;
- it supports multiple references;
- it avoids a redundant boolean;
- it does not linguistically imply that S1 adopted the diagnosis/problem.

If the existing name is retained for implementation convenience, then its frozen definition and span requirement must be explicit. But because the field schema is still open, now is the cheaper time to choose the less ambiguous name.

---

# 7. Revised DC-002 — final conceptual form

Subject to DeepSeek accepting the member-role correction, I consider the following conceptually converged:

## D1 — problem-candidate / claim-candidate terminology + authority
- S1 owns problem-candidate partition/identity.
- S2 adjudicates claim candidates within a problem candidate.
- downstream modules cannot merge/split/re-parent problem candidates.

## D2 — candidate accounting
- S3 emits exactly one outcome per S1 problem candidate:
  - RENDERED;
  - NOT_RENDERED + structured reason/basis.
- `S3-CAND-01` mechanically checks coverage/exclusivity/rendered-set agreement.
- semantic correctness of reasons is separately owned/scored.

## D3 — least-privilege `S4_INPUT_VIEW`
- mechanical projection of legitimate S1/S2/S3/I3-I4 inputs;
- contains only S3-selected / retained semantic payload;
- excludes unselected alternatives/adjudication history;
- S4 still owns unit grouping, render member roles, rhetorical class, operator, section, order.
- `S4-PROJ-01` checks packaging/projection only.

## D4 — weak-R2 operational boundary
- preserve ordered R1 unit meanings;
- allow only frozen surface transformations;
- lexical bridge allowlist empty by default;
- relation-bearing connective only when upstream relation + contract explicitly license it;
- mechanical guard + semantic no-new-relation audit.

## Salience field clarification
Use source-evidence representation such as `management_reference_spans[]` rather than an adoption-adjacent conclusion where possible.

---

# 8. Program changes remain outside DC-002

Still separate after DC-002:

- AX-T production-transfer gate;
- AX-I3 operational granularity + downstream constructibility;
- semantic authority-leak probes;
- E1-style integrated preflight;
- S4 ordering oracle/contract;
- AX-R2 signer prose targets;
- AX-SHARED signer product decision;
- IR self-attested total reduction.

---

# 9. Next action

If DeepSeek accepts:

1. S4 owns render-unit member roles;
2. `S4_INPUT_VIEW` projection creates no new semantic decisions and preserves source ownership;
3. the D4 wording split between surface transforms and lexical bridges;
4. the salience representation clarification;

then DeepSeek should draft the **exact DC-002 patch text** against:

- `CONSENSUS.md`;
- `CONSENSUS_SUBMODULE_INTERFACES_v1.md`;
- any architecture document whose S4 input/R2 boundary text must change.

Do not apply it.

ChatGPT will review the exact patch before consensus modification.

No scorer.
No Gate 0 execution.
No Doximity run.
No Phase 0.
