# ChatGPT review 062 — revised DC-002 patch verification

## Verdict

> **DC-002 REMAINS CONCEPTUALLY CONVERGED. THE REVISED PATCH STILL NEEDS ONE FINAL LOCAL TEXT PASS BEFORE APPLICATION.**

DeepSeek instantiated almost all corrections from review 061 correctly.

The remaining issues are not a redesign. They are exact contract inconsistencies that would create ambiguity if committed into consensus.

Do not apply the proposal yet.

---

# 1. D1 terminology is still inconsistent inside the patch

The proposal alternates between:

- `candidate claims`
- `claim candidates`

DC-002 exists partly to eliminate this exact ambiguity.

## Required correction

Use one term everywhere:

> **claim candidate**

For S1 output:

```text
- for each problem candidate, its claim candidates — source-grounded formulations that could become,
  or contribute to, an approved claim representation;
- the partition mapping each claim candidate to exactly one problem candidate.
```

Do not reintroduce `candidate claim` as a second label.

---

# 2. D1 still overstates what cross-problem semantic comparison means

Current text says:

> S2 relates claim candidates within one problem candidate; it does not compare across problem candidates, because a cross-candidate comparison is a partition change.

The first clause is correct for **claim-candidate relations that form one claim representation**.

The second clause is too broad.

A semantic relation across two problem subjects does not automatically change the S1 partition.

Examples:
- one neurologic problem is etiologically related to another;
- a shared diagnostic action serves two rendered problems;
- an object retained for one problem also contextualises another.

The architecture already permits cross-problem object reuse and semantic relations.

## Required authority wording

Use:

> S2 adjudicates relations among claim candidates that contribute to a claim representation **within one problem candidate**. S2 may also adjudicate source-grounded semantic relations among objects/problem subjects when needed, but may not use any relation to merge, split, or re-parent S1 problem candidates or their claim candidates.

This preserves S1 partition authority without accidentally prohibiting legitimate cross-problem semantics.

---

# 3. Consensus item 28 still needs the words “within one problem candidate”

Current proposed consensus wording remains:

> A claim is a representation that may carry several claim candidates and their relation.

That is exactly the ambiguity DC-002 is supposed to remove.

## Required wording

> A **claim candidate** is a source-grounded formulation attached by S1 to exactly one problem candidate that may become, or contribute to, a claim. An approved claim representation may carry several claim candidates **within that problem candidate** and their S2-adjudicated relation.

This makes the authority boundary visible in the canonical consensus, not only in rationale prose.

---

# 4. D1b is good, but identify the referenced entity precisely

Current:

> management statement that references this candidate

Use:

> management statement that explicitly references this **problem candidate's subject**

because `candidate` is now deliberately split into two terms.

Also retain the rule:

> `management_reference_spans[]` is source-grounded salience evidence only; it is not an adoption/current-status/rendering verdict.

That sentence should appear in the applied interface text, not only the proposal rationale.

---

# 5. D2 candidate-accounting structure is now acceptable

The revised D2 correctly requires:
- one outcome per S1 problem candidate;
- coverage;
- exclusivity;
- equality between RENDERED outcomes and `rendered[]`;
- typed NOT_RENDERED reason;
- reason correctness outside the mechanical accounting predicate.

## One precision addition

The output contract should allow/require:

> basis reference(s) where the chosen reason family depends on an upstream state.

Example:
- `NO_APPROVED_REPRESENTATION` should point to the corresponding S2 no-approved-representation state.

This avoids turning a typed reason code into an unsupported S3 assertion.

The exact reason vocabulary remains downstream.

---

# 6. D3 has a direct contradiction: duplicate groups are excluded although S4 owns COVERED

Current D3 says S4 receives:

> semantic relations or reasoning attributes those members carry

and the S4 boundary says:

> S4 assigns HEAD, MODIFIER, CONDITION and COVERED from the semantic relations in the view.

But the exclusion list globally excludes:

> duplicate groups

That cannot all be true.

To assign `COVERED` correctly, S4 may need S2's duplicate/equivalence relation among **retained selected members**.

Likewise modifier/condition render roles require the corresponding upstream semantic relation.

## Required correction

Do not blacklist semantic relation **types** that may be needed by the selected/retained payload.

Use a relevance rule:

### Project
Only semantic states/relations required for:
- the S3-selected representation;
- S3-retained content;
- grouping/member-role/operator/section decisions S4 legitimately owns.

This may include, where relevant:
- duplicate/equivalence relation for retained members;
- modifier/condition relation;
- selected claim-candidate relation;
- reasoning role;
- encounter-level adoption state **only if** a retained item's rendering contract actually requires that settled state.

### Exclude
- unselected representations;
- rejected alternatives;
- semantic relations belonging only to unselected alternatives;
- unrelated adoption states;
- full adjudication history / evidentiary deliberation not required by the selected/retained payload.

Least privilege must be dependency-based, not a global type blacklist.

---

# 7. D3 should not globally exclude all adoption verdicts before proving S4 never needs one

The proposal excludes:

> adoption verdicts

categorically.

That may be correct for many S4 decisions, but it has not yet been proven for every retained historical item/operator/section contract.

If S3 has already converted adoption into a complete retained-use/representation state, S4 may not need the verdict.

But if an operator or section realization depends on whether a retained historical recommendation is currently adopted, S4 may need the **settled verdict**, not the reasoning that produced it.

## Safer contract

> Adoption verdicts are excluded by default and projected only when a frozen S4 function/contract demonstrates that the settled verdict is required for selected/retained content. The adjudication history/evidence trail remains excluded.

This is still least privilege.

Do not make an irreversible field-level claim before the field-level Case IR schema and operator vocabulary are frozen.

---

# 8. D3 selected-representation relation example is misleading

Current proposal says:

> the selected representation's own claim relation ... e.g. whether the claim is epileptic or functional

But “epileptic” and “functional” are claim candidates/alternatives, not the relation.

The relation might be:

- COMPETING;
- UNRESOLVED;
- DIFFERENTIAL;
- another downstream vocabulary term.

## Better example

> the selected representation's own relation among its claim candidates — e.g. that epileptic and functional seizure formulations are COMPETING/UNRESOLVED.

The exact relation vocabulary remains downstream.

---

# 9. D3 “rendered-problem identity from S1” remains slightly misleading

Current:

> from S1: rendered-problem identity ... projected for the ids S3 rendered

Use:

> from S1: the S1-owned problem-candidate identity/subject and structured salience/order inputs, projected only for candidate ids S3 marked RENDERED.

Rendering is S3-owned.
Identity is S1-owned.

The wording should preserve both facts.

---

# 10. S4-PROJ-01 wording is still too broad

Current:

> An adjudication field present in S4 input is a packaging violation.

But D3 legitimately projects selected S2-adjudicated semantic relations/reasoning attributes.

So “adjudication field” cannot itself be forbidden.

## Correct predicate scope

`S4-PROJ-01` should mechanically verify:

1. every field/value in `S4_INPUT_VIEW` belongs to the frozen allowlisted projection schema;
2. every projected field traces to an allowed source interface;
3. no unselected/rejected alternative or nonrequired adjudication state is present;
4. the projection introduces no new semantic value.

A field is not a violation merely because S2 adjudicated it.

The violation is:
> it is outside the permitted selected/retained projection.

---

# 11. D4 is close, but the mechanical preservation rule needs normalization

The patch allows:
- capitalization changes;
- punctuation changes;
- whitespace changes.

It then requires:

> each unit's text appears as a contiguous span.

Literal contiguous matching will falsely fail allowed transformations.

## Required wording

> after a frozen normalization that removes only the explicitly allowed surface differences (permitted capitalization, whitespace and punctuation), each R1 unit's content remains recoverable as one contiguous span, in unit order.

Do not normalize lexical tokens or semantic connectives.

This keeps the guard mechanical without contradicting the allowed transformations.

---

# 12. D4 lexical bridge policy is acceptable

The revised separation is good:

- punctuation = surface transform;
- lexical bridge allowlist = empty initially;
- relation-bearing bridges are not stylistic composition;
- semantic no-new-relation audit remains separate.

I would retain the strong initial contract:

> no added lexical bridge tokens.

AX-R2 can later demonstrate whether the boundary is too weak.

---

# 13. Application consequence needs one more explicit stale marker

The proposal correctly says DC-002 makes Gate 0 stale.

When applied, explicitly mark as stale/pending regeneration:
- AX-S1S2-D experiment-local `schema.md`;
- `predicates.md` active set;
- CASE-01 clean parent;
- Gate 0 seed specification;
- generated seed artifacts/manifest;
- campaign hashes.

Do not merely add the two new predicates to the old active campaign and leave existing parent/schema artifacts appearing current.

---

# 14. Status

## Architecture shape
RETAINED.

## DC-002 conceptual design
**CONVERGED.**

## DC-002 exact patch
**ONE FINAL LOCAL TEXT PASS REQUIRED.**

The remaining issues are:
- terminology consistency;
- cross-problem relation wording;
- selected/retained semantic projection scope;
- S4-PROJ predicate precision;
- normalization in R2's mechanical guard.

None requires another architecture redesign.

## Next action

Revise `proposals/deepseek/012-dc002-patch.md` in place.

If the revised patch reflects sections 1–11 above, it should be ready for **application approval** on the next review.

Do not apply yet.
No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.
