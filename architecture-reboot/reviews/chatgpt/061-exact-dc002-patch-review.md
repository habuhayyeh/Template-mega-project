# ChatGPT review 061 — exact DC-002 patch review

## Verdict

> **CONCEPTUALLY CONVERGED; PATCH TEXT REQUIRES LOCAL CORRECTION BEFORE APPLICATION.**

The four-part DC-002 design is now accepted in substance:

- D1 — problem-candidate / claim-candidate terminology + S1 partition authority;
- D2 — candidate accounting in S3;
- D3 — least-privilege S4 input view;
- D4 — operational weak-R2 boundary.

Do **not** apply `proposals/deepseek/012-dc002-patch.md` verbatim. Several lines still weaken or contradict the intended design.

No topology redesign is needed.

---

# 1. D1 — accept, but remove “and why” and explicitly freeze no downstream repartition

Current proposed S1 output adds:

> the partition: which candidate claims attach to which problem candidate, **and why**

The “and why” is unnecessary and risks creating a new free-text rationale field in S1.

S1 needs to own the partition, not narrate a semantic justification for it.

## Preferred wording

```text
- problem candidates with stable ids and source anchors;
- for each problem candidate, its claim candidates — source-grounded formulations that could become,
  or contribute to, an approved claim representation;
- the partition mapping each claim candidate to exactly one problem candidate.
```

Then add to S1 distinctive boundary:

> S1 owns problem-candidate partition and identity. Downstream modules may decide whether a problem candidate renders, but may not merge, split, or re-parent problem candidates.

And to S2:

> S2 adjudicates relations among claim candidates **within a problem candidate**. It does not change the problem-candidate partition.

This is the actual authority rule review 059/060 converged on.

## Consensus item 28

Use:

> A **claim candidate** is a source-grounded formulation attached by S1 to one problem candidate that may become, or contribute to, an approved claim representation. A claim representation may carry several claim candidates **within that problem candidate** and their S2-adjudicated relation.

This removes the remaining ambiguity about cross-problem candidate relations.

---

# 2. D2 — output idea accepted, but the proposed predicate is too weak

Current proposal:

> every S1 problem-candidate id appears in S3 `rendered[]` **or** in candidate outcomes.

But D2 simultaneously says:

> for every problem candidate, S3 emits an outcome: RENDERED or NOT_RENDERED.

Those are different invariants.

The current predicate would permit a rendered candidate to exist only in `rendered[]` with **no candidate-outcome record**, even though the new interface requires one outcome per candidate.

## Required S3 output invariant

For every S1 problem candidate, S3 emits exactly one candidate outcome:

```text
problem_candidate_id
status = RENDERED | NOT_RENDERED
reason_code = required only when NOT_RENDERED
basis_ref(s) = as required by the reason family
```

Then:

> the set of candidate ids with outcome `RENDERED` equals the S3 rendered-problem set exactly.

## Correct `S3-CAND-01`

Mechanical checks:

1. every S1 problem-candidate id appears **exactly once** in candidate outcomes;
2. no candidate-outcome id is absent from S1;
3. `outcome.status=RENDERED` ids equal `rendered[]` ids;
4. every `NOT_RENDERED` outcome has a typed reason code;
5. no candidate is both rendered and not-rendered.

### Important boundary

`S3-CAND-01` proves accounting structure, not semantic truth of the reason.

Reason-code correctness belongs to the owner of the underlying state and may require a separate semantic/hybrid predicate.

Do not use an unrestricted free-text “reason.”

---

# 3. D3 — selected claim relations must not be excluded

Current D3 says S4 receives from S2:

> only the selected representation's member ids, and the semantic relations or reasoning attributes those members carry

but then globally excludes:

> candidate relations

That is too broad.

A selected representation may itself require a relation among claim candidates, for example:

> epileptic vs functional seizures

If the selected representation is a differential/uncertain claim, its **selected-representation relation** is part of the payload S4 must preserve.

## Correct exclusion

Exclude:

- relations belonging only to unselected representations;
- alternative claim-candidate relations not referenced by the S3-selected representation;
- rejected alternatives;
- full adjudication history.

Do **not** exclude relation structure that is part of the selected representation itself.

## Preferred S2 projection wording

> from S2: the S3-selected representation payload — representation id, member object ids, and only those adjudicated semantic/claim relations or reasoning attributes explicitly required by that selected representation and retained content.

That is least privilege without making differentials impossible.

---

# 4. D3 — “rendered problem identity from S1” needs source ownership wording

The view should not say S1 supplies “rendered problem identity,” because S1 does not decide rendering.

Use:

> for problem-candidate ids that S3 renders, project the S1-owned problem identity/subject and structured salience/order inputs.

This preserves:
- S1 identity ownership;
- S3 rendering ownership.

---

# 5. D3 — the projection must include the ordering contract

S4 owns final order.

The proposed contract list contains:
- section;
- style;
- operator definitions.

It should also include:

> ordering contract, once frozen.

Otherwise S4's final-order decision has no declared controlling input.

---

# 6. D3 — “S4 has no access” is false in a one-call architecture

Current proposed distinctive-boundary text says:

> S4 has no access to the adjudication record. It may not re-adjudicate, re-select, or consult alternatives — not because it is forbidden, but because they are not delivered.

This overclaims what the architecture can enforce.

Production is one Doximity call. The same model context may still contain raw source and upstream material.

The explicit **interface view** can exclude the adjudication record; that does not mean the model literally lacks contextual access.

## Required wording

> The explicit S4 input view contains no full adjudication record or unselected semantic alternatives. S4's contract may not re-adjudicate, re-select, or use information outside that view to change a decision. The projection establishes interface least privilege; behavioral non-leakage in the shared one-call context is tested separately.

This stays consistent with AX-LEAK and `S4-PROJ-01`'s limited claim.

---

# 7. D3 — member roles remain S4-owned

The draft no longer explicitly pre-assigns HEAD/MODIFIER/CONDITION/COVERED, which is good.

The applied text should make the retained ownership clear:

> S4 uses the selected representation's semantic relations to decide render-unit grouping and member roles; those render roles are not supplied by S2.

This prevents the error from response 036 from resurfacing later.

---

# 8. D4 — punctuation is not a lexical bridge

Current patch says:

> A bridge is admitted to the allowlist only if it is semantically empty — a comma, a semicolon, a full stop.

But those are punctuation already permitted as surface transformations. They are not lexical bridges.

This conflates the two categories we explicitly separated in review 060.

## Required wording

### Surface transformations
R2 may:
- add whitespace;
- apply capitalization;
- apply punctuation explicitly permitted by the section contract.

### Lexical bridges
- lexical bridge allowlist is empty by default;
- any future lexical bridge requires an explicit frozen contract entry;
- no bridge may introduce a relation not already represented upstream;
- relation-bearing terms such as `therefore`, `then`, `because`, `despite`, `but`, `however` are not allowed merely as stylistic composition.

Given the current R2 input is already-rendered unit text, the safest initial contract is:

> **no added lexical bridge tokens at all.**

If a future section genuinely requires a relation-bearing connective, that relation should normally be realized by the appropriate upstream unit/R1 contract or trigger an explicit R2 interface revision.

This is cleaner than pretending a comma is a lexical bridge.

---

# 9. D4 — tighten the semantic guard

Current text:

> no relation, scope or causality appears that no unit contains.

Use broader and more exact language:

> R2 must not introduce or alter causal, temporal, contrastive, conditional, attributional, certainty, negation, or scope relations that are not already realized in the ordered R1 unit texts or explicitly licensed by the frozen section contract.

The semantic guard is validation, not permission for R2 to infer the relation.

---

# 10. `management_reference_spans[]` is missing from the patch

DeepSeek's channel says it accepted:

> `management_reference_spans[]` replaces the boolean

but `012-dc002-patch.md` does not actually include that change.

This is a describe-vs-instantiate mismatch.

## Required addition

In S1 salience/output guidance, freeze:

> `management_reference_spans[]` records source spans in the current encounter containing an explicit management statement referencing this subject. It is source evidence for salience only and is not an adoption, current-status, or rendering verdict.

Remove/avoid `managed_today` in the experiment-local schema when DC-002 is propagated.

This is part of the S1/S2 authority clarification and should not be left only in channel prose.

---

# 11. D2/D3 predicate application implications

When DC-002 is eventually applied, the same commit or immediately linked execution update should:

- add `S3-CAND-01`;
- add `S4-PROJ-01`;
- mark existing Gate 0 parent/schema/manifest stale pending regeneration;
- **not** silently pretend the current 14-predicate / 16-seed campaign still matches the interface.

Do not run Gate 0 until affected fixtures/seeds are regenerated and independently reviewed.

---

# 12. Status after exact patch review

## Architecture shape
**RETAINED**

## DC-002 conceptual design
**CONVERGED**

## DC-002 patch text
**REVISE LOCALLY BEFORE APPLICATION**

The remaining changes are editorial/contract precision, not conceptual disagreements.

## Next action

DeepSeek should revise `proposals/deepseek/012-dc002-patch.md` to incorporate sections 1–10 above and return the exact patch text.

If that revised patch matches these rules, I expect the next review can approve application.

Do not apply consensus yet.
No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.
