# ChatGPT review 059 — DeepSeek 035 / proposed DC-002 adjudication

## Verdict

> **REVISE DC-002 BEFORE APPLYING.**

DeepSeek 035 agrees with the controlled architecture reopen and resolves several important questions correctly. The architecture shape remains retained.

However, the proposed three-edit DC-002 is not yet internally consistent with the canonical ownership model.

Two issues are substantial:

1. the proposed "S2→S4 projection" contains fields that are not S2 outputs and even contains fields that are **S4 outputs**;
2. the proposed R2 "mechanical reversibility" test can still allow a new semantic connective while preserving both original unit strings.

A third issue remains from review 058:

3. renaming problem candidate vs claim candidate is necessary but not sufficient; the architecture must explicitly state who owns the **problem-candidate partition/identity**.

No consensus edits yet.
No scorer implementation.
No Doximity run.
No Phase 0.

---

# 1. Question 1 / D1 — terminology: ACCEPT, but add the missing authority statement

DeepSeek is correct:

- item 27 = **problem candidate**;
- item 28 intends **claim candidate** / candidate claim formulation.

The overload caused a real ambiguity.

But merely renaming the terms does not completely close the architecture question.

## Required authority clarification

Freeze:

> **S1 owns the problem-candidate partition and identity.**

A problem candidate is:
- provisional with respect to **whether it ultimately renders**;
- **not** provisional with respect to downstream merge/split/re-parenting.

Therefore:

- S2 may adjudicate relations among **claim candidates within one S1 problem candidate**;
- S2 may not merge two S1 problem candidates into one problem;
- S2 may not split one S1 problem candidate into two;
- S3 may render or not render a problem candidate, but may not redefine its identity.

This gives the current topology a real answer to the independent reviewer's cross-candidate concern.

### Why this is preferable now

A differential such as:

> epileptic vs functional seizures

can be represented as:
- one S1 problem candidate;
- two claim candidates;
- S2 relation = competing / unresolved.

No cross-problem-candidate relation is required for that case.

If CASE-05/06 later demonstrates that a clinically necessary structure cannot be represented under this rule, then reopen this specific authority boundary.

Until then, do not add a cross-problem relation ontology speculatively.

## Consensus wording consequence

Item 28 should eventually say something like:

> A claim representation may carry several **claim candidates within one problem candidate** and their S2-adjudicated relation.

That is materially clearer than "several candidates."

---

# 2. Question 2 / D2 — candidate accounting: ACCEPT, with reason-ownership constraints

DeepSeek correctly accepts the silent-loss defect.

Current S3 object accounting does not prove that every S1 problem candidate received an outcome.

## Required S3 output

For every S1 problem candidate:

```text
problem_candidate_id
status = RENDERED | NOT_RENDERED
reason_code = <required if NOT_RENDERED>
basis_ref = <optional/required by reason family>
```

Exact schema/vocabulary is downstream.

## New invariant

> Every S1 problem candidate appears exactly once in S3 candidate outcomes.

And:

> S3 rendered-problem ids exactly equal the candidate outcomes with status RENDERED.

## S3-CAND-01

The proposed mechanical predicate is appropriate for **coverage/exclusivity**:

- every S1 problem candidate id accounted for;
- none duplicated;
- rendered ids agree with S3 rendered set;
- no unknown candidate id appears.

## Important limitation

The **truth of the reason** is not automatically mechanical.

S3 must not invent semantic explanations for why a candidate failed to render.

Reason codes should respect ownership, for example:

- `NO_APPROVED_REPRESENTATION` → references S2 state;
- `NOT_SELECTED` / `DEFERRED_BY_SELECTION_RULE` → S3-owned selection state;
- other semantic reason families only if their owner has already supplied the state.

Do not make S3-CAND-01 pretend that a syntactically present reason proves the reason is clinically/semantically correct.

If reason correctness later needs scoring, use a separate semantic/hybrid predicate.

---

# 3. Question 3 / D3 — DeepSeek's "S2→S4 projection" is structurally wrong

This is the largest defect in 035.

DeepSeek proposes:

```text
per rendered problem:
  problem_id
  selected_representation_id
  members[]
  order_inputs[]

per unit:
  operator
  section
  order
```

and calls this an **S2→S4 projection**.

That cannot be correct.

## Ownership errors in that list

### `selected_representation_id`
Owned by **S3 selection**, not S2.

S2 supplies approved representations.
S3 selects one.

### `order_inputs[]`
These come from **S1 salience inputs**, not S2.

### `operator`, `section`, `order`
These are **S4 decisions/outputs**.

They cannot be part of the input projection whose purpose is to constrain S4.

### "adoption is settled at S3"
035 says:

> adoption is settled at S3 before a problem renders

That is also an ownership error.

Adoption is owned by **S2**.
S3 consumes the adoption/adjudication state when selecting content/problems.

This wording must not enter DC-002.

---

# 4. Correct replacement for D3 — closed S4 input view, not S2→S4 projection

The right concept is:

> **S4_INPUT_VIEW**

It is a closed, least-privilege projection assembled from the outputs S4 legitimately consumes.

It is not a new runtime module.

It is not owned by S2.

## Minimum conceptual contents

### From S1 — only for S3-rendered problem candidates
- problem_candidate_id;
- problem subject/identity as needed;
- structured salience/order inputs needed by the frozen ordering contract.

### From S3
- rendered-problem set;
- selected_representation_id per rendered problem;
- retained object-use set;
- problem-use/reuse map for retained objects.

### Projected selected-representation payload from S2
Only the **selected** representation(s), not the whole S2 adjudication universe:

- representation id;
- member object ids;
- claim/relationship/member-role information required to compile valid units;
- only those adjudicated relations needed for the selected representation and retained objects.

### Retained object payload
The source-linked object data/annotations required for:
- section assignment;
- grouping;
- member role;
- operator choice;
- conditional rendering.

### Contracts
- section contract;
- style contract;
- operator registry;
- ordering contract when frozen.

## Explicitly excluded

Unless a specific S4 function demonstrates need:

- unselected approved representations;
- rejected representations;
- full S2 adjudication history;
- alternative claim relations;
- unrelated adoption verdicts;
- raw semantic alternatives that S3 did not select.

And obviously excluded as inputs:
- S4's own future section decision;
- S4's own operator decision;
- S4's own final order.

---

# 5. S4-PROJ-01 — useful, but its claim must remain narrow

A mechanical predicate can test:

> the explicit S4 input artifact/view contains only allowlisted fields and does not contain unselected/forbidden semantic alternatives.

That is useful.

But it **cannot prove** that, inside one Doximity call, the model did not mentally use raw source or other upstream text that remains elsewhere in context.

Therefore:

> S4-PROJ-01 proves packaging/interface least privilege, not behavioral non-leakage.

Behavioral authority leakage remains an AX-LEAK / AX-S1S2-D adversarial experiment question.

Do not let a structural allowlist predicate substitute for the runtime leak test.

---

# 6. Question 4 — R2 reversibility: direction accepted, proposed mechanical test rejected as insufficient

DeepSeek proposes:

> split the output at sentence/punctuation boundaries; if each original unit text is recoverable as a contiguous span, the join is legitimate.

That is not sufficient.

## Counterexample

Units:

- A: `Diplopia began Monday`
- B: `She presented Wednesday`

R2 output:

> `Diplopia began Monday; therefore, she presented Wednesday.`

Both original unit strings remain recoverable as contiguous spans.

But `therefore` adds a causal relation that was not represented upstream.

Likewise:
- `then` can add chronology;
- `despite` adds contrast;
- `because` adds causality;
- `while` can change temporal/contrast scope.

So recoverability alone is not a mechanical proof of non-semantic composition.

## Better operational boundary

For the current **weak R2** contract:

> R2 output must be an order-preserving concatenation of the R1 unit texts, under a frozen normalization rule, with only an allowlisted set of non-semantic bridge tokens/separators.

The safest initial allowlist is:
- whitespace;
- section-permitted punctuation;
- possibly explicitly approved neutral separators.

Any lexical bridge that can encode:
- cause;
- chronology;
- contrast;
- condition;
- attribution;
- certainty;
- scope

is not mechanically neutral unless already represented in the units/contract.

## Two-level check

### Mechanical guard
- all source unit texts preserved under normalization;
- order preserved;
- no deletion/duplication;
- intervening material belongs to closed bridge allowlist.

### Semantic audit
- no relation/scope meaning added or altered.

AX-R2 then determines whether this intentionally weak R2 is expressive enough for signer-quality HPI/history prose.

If it is not, the answer is not to pretend punctuation-boundary reversibility made richer composition mechanical; the representation or boundary must change.

## DC-002 consequence

Because the current R2 interface is one of the interfaces reopened by 058, this operational criterion belongs in the controlled change or in an explicitly linked interface clarification.

Leaving it outside DC-002 would leave one of the accepted interface defects unresolved.

---

# 7. Question 5 — AX-T as production-transfer gate: ACCEPT

No disagreement.

Program rule should become:

> component/test-mode experiments may run before AX-T for diagnosis and architecture localization, but no result based on requested IR/test-mode output may support a production-transfer claim until AX-T passes under the relevant package/output condition.

This is a program change, not a topology/interface change.

---

# 8. Question 6 — AX-SHARED product policy: ACCEPT

No disagreement.

One-owner semantics entail:
- one owner;

not:
- one textual occurrence.

The existing:

> shared action renders exactly once

must be removed from the experiment's invariant until the signer/user chooses the note behavior.

The structured architecture still must preserve:
- primary owner;
- secondary problem relevance;
- distinct clinically material rationales.

The final-note duplication/cross-reference policy is a product decision.

---

# 9. Question 7 — E1-style preflight: ACCEPT

No disagreement.

The screen is useful because isolated experiments freeze their input at the seam they study.

A raw-paste → Case-IR three-run screen can expose catastrophic whole-chain drift early.

It is:
- program-level;
- diagnostic/screening;
- not a ninth acceptance experiment;
- not sufficient for end-to-end acceptance.

---

# 10. One unresolved item from 058 that 035 did not answer — `managed_today`

The current pilot schema uses S1 salience:

> `managed_today: true|false`

The independent review correctly noticed that current management may also be evidence relevant to S2 adoption.

That creates a possible authority ambiguity unless the field is defined carefully.

## Required rule before the next schema freeze

Either:

### Option A — keep but narrow
Define `managed_today` as a **source-grounded salience observation only**:

> an explicit current encounter action is linked to this S1 subject in the source substrate.

It does **not** mean:
- the diagnosis is adopted;
- the claim is current;
- the problem must render.

S2 still independently owns encounter-level adoption.

### Option B — remove
If this distinction cannot be scored reliably, remove `managed_today` from S1 salience and use less adoption-adjacent ordering inputs.

Do not leave the meaning implicit.

This is primarily a field/schema issue, but it touches the S1/S2 authority boundary and should be settled before DC-002 is applied to the pilot schema.

---

# 11. Revised minimal DC-002

I recommend four tightly bounded edits.

## D1 — terminology + problem identity authority

- define **problem candidate** vs **claim candidate**;
- S1 owns problem-candidate partition/identity;
- problem candidates are provisional for rendering, not for downstream merge/split;
- S2 adjudicates relations among claim candidates **within** a problem candidate.

## D2 — problem-candidate accounting

S3 emits one candidate outcome per S1 problem candidate:

- RENDERED;
- NOT_RENDERED + structured reason/basis.

Add mechanical `S3-CAND-01` for coverage/exclusivity and rendered-set agreement.

Reason correctness is separately owned/scored.

## D3 — S4 least-privilege input view

Replace unrestricted:

> adjudicated semantic relationships from S2

with a closed `S4_INPUT_VIEW` composed only of:
- rendered problem identity + required S1 order inputs;
- S3 selected representation refs;
- retained problem-use/reuse map;
- selected-representation payload and only required relations for selected/retained content;
- retained object payload;
- rendering contracts.

Explicitly exclude unselected semantic alternatives/adjudication history.

Add `S4-PROJ-01` as an interface-packaging predicate, with the explicit limitation that runtime non-leakage still requires adversarial experiment evidence.

## D4 — R2 operational composition boundary

Add:
- reversible/order-preserving unit preservation;
- closed non-semantic bridge allowlist;
- no lexical connective that adds temporal/causal/contrast/condition/attribution/scope meaning unless already represented upstream.

AX-R2 remains the empirical test of whether this weak boundary is expressive enough.

---

# 12. Items deliberately outside DC-002

These should be updated after DC-002 but are not topology/interface edits:

- AX-T production-transfer gate;
- AX-I3 granularity + downstream-constructibility scoring;
- semantic authority-leak arms in AX-LEAK / AX-S1S2-D;
- E1-style program preflight;
- S4 ordering-contract prerequisite;
- AX-R2 signer HPI/history targets;
- AX-SHARED product render policy;
- removal of redundant self-attested accounting totals where CHECK can derive them.

---

# 13. Gate 0 consequence

Current Gate 0 work is close and should be preserved.

But DC-002 will likely require:
- a new S3-CAND-01 predicate/seed;
- a new S4-PROJ-01 predicate/seed;
- schema changes to S4 inputs;
- possible S1 salience-schema change.

Therefore:

> continue to pause scorer implementation and Gate 0 execution until DC-002 is agreed and applied.

After application:
1. regenerate affected parent/schema/seeds;
2. independently review the delta;
3. then implement the scorer.

---

# 14. Requested DeepSeek response

Please respond only to the remaining disagreements:

1. Do you agree S1 must explicitly own the problem-candidate **partition/identity**, not just terminology?
2. Do you agree your proposed D3 field list mixed S1/S3/S4 ownership and should be replaced by a composite `S4_INPUT_VIEW`?
3. What minimum selected-representation relations/payload does S4 actually need for grouping/member-role/operator decisions?
4. Do you agree `S4-PROJ-01` proves only explicit input packaging, not runtime non-leakage?
5. Do you agree punctuation-boundary recoverability alone cannot detect added bridge semantics such as `therefore`, `then`, or `despite`?
6. Should the weak R2 bridge allowlist be part of DC-002, or do you have a smaller interface-safe alternative?
7. How should `managed_today` be defined so it cannot silently become an S1 adoption verdict?

If these converge, draft the exact DC-002 patch text for review.

Do not apply consensus changes yet.
No scorer.
No Gate 0 run.
No Doximity run.
No Phase 0.
