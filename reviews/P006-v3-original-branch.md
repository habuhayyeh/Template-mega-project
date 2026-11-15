# P006 v3 review — original architecture branch

## Verdict

**REVISE — scope is correctly resolved by D-016, but v3 is not implementation-ready.**

D-016 is correctly recorded and STATUS now reflects the actual set-3 evidence. However, P006 v3 did not incorporate the concrete contract corrections from the previous review. The proposal still contains the same unresolved text.

## 1. Rhetorical class remains unresolved

P006 still defines:

> RENDER_GROUP — members express one factual proposition

but G4 groups O23 and O39, both CLAIM_QUALIFIER reasoning.

Required: encode rhetorical destination explicitly.

Either:

- separate `FACT_GROUP` / `REASON_GROUP` / `COMPOSE_GROUP`; or
- retain `RENDER_GROUP` with required `CLASS=FACT|REASONING`.

Management composition remains Plan/MANAGEMENT.

Grouping must never move an object across fact/reasoning/plan classes.

## 2. G4 still changes source wording without an authorized transformation

HEAD O23 is:

`but the MRI will tell us`

Target remains:

`The MRI will tell us.`

Dropping `but` is not authorized by the accepted transformation set.

Required target if O23 remains HEAD:

`But the MRI will tell us.`

Do not use P006 as a paraphrase license.

## 3. G5 still changes source wording without an authorized transformation

HEAD O34 is:

`family's concern about her memory is not today's issue`

Target remains:

`Family's concern about her memory, not today's issue.`

That deletes `is` and changes syntax.

Required target:

`Family's concern about her memory is not today's issue.`

unless a separate bounded transformation is proposed and reviewed.

## 4. Ungrouped-object behavior still conflicts with 05

P006 still says:

> an ungrouped object renders alone

That makes every retained ungrouped object mandatory prose and overrides existing 05 eligibility/relevance behavior.

Required:

> An ungrouped object remains subject to the existing 05 eligibility/rendering rules. P006 only fixes semantic equivalence/composition for explicitly grouped objects.

If render eligibility is later moved upstream, that is a separate proposal.

## 5. COVERED validation is still impossible as written

P006 still requires:

> every COVERED appears in the trace and nowhere in the output text

A COVERED duplicate can share the same words as the HEAD, so text-level absence cannot be mechanically checked.

Required:

> A COVERED member has no independent output-line trace/assignment. It is accounted for only through the group.

Word overlap with the HEAD is allowed.

## 6. Ordering still assumes all groups are facts

P006 still says:

> rendering order follows group order within the facts block

But G4 is reasoning and G2 is management.

Required:

- FACT groups follow existing facts order;
- REASONING groups follow existing reasoning order;
- COMPOSE groups follow existing Plan bucket/order;
- grouping creates no new cross-class ordering system.

## 7. One signer preference needs explicit resolution: O53 provenance display

There is a genuine product/style choice about G1.

Facts:
- O8 supplies the clinical timing: `left MCA infarct two years ago`.
- O53 supplies a prior-neurology duplicate with provenance date `2024-02`.
- That provenance date is a documentation/source date, not established as the infarct event date.

Two source-faithful options exist:

### A. Trace-only provenance
Render:

`Known left MCA infarct two years prior to presentation.`

Keep O53 and `2024-02` only in trace metadata.

### B. Explicit documentation provenance
Render the clinical fact from O7/O8, and separately preserve the source attribution without implying event timing, for example:

`Known left MCA infarct two years prior to presentation (also documented by prior neurology, 2024-02).`

This is more verbose but preserves the signer's earlier preference to expose the prior-neurology date.

This is not an architecture correctness question. It is a note-style/provenance preference and should be decided by the signer under D-013.

## Implementation gate

Do not implement P006 until items 1–6 are corrected and item 7 is resolved by the signer.

D-016 remains valid; no broader P007 work is authorized.
