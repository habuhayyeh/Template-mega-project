# P006 v2 + Doximity audit review — original architecture branch

## Verdict

**P006 v2: REVISE, close to acceptable. Keep P006 narrow.**

**Audit scope decision:** do **not** widen P006 into a general pre-05 normalization pass. The external audit analyzed the wrong run files. Its structural observations are useful hypotheses, but they are not sufficient evidence to bundle five architectural changes into P006.

Preferred sequence:

1. P006 = explicit semantic render/compose groups for the failure actually demonstrated by set 3.
2. Test P006.
3. Only then propose P007 for residual normalization problems that remain empirically demonstrated (e.g. COURSE typing if it still drifts).

Do not add standing-item injection merely because the audit suggested it: the complete package already fixed standing items in sets 2 and 3.

---

## 1. P006 v2 fixes the main v1 defect

Accepted:

- group membership and roles are decided in 03;
- exactly one HEAD;
- MODIFIER/CONDITION are explicit;
- COVERED is accounting, not an alternate prose candidate;
- 04 transports the adjudication losslessly;
- 05 no longer chooses representative wording or semantic equivalence;
- G1 provenance correction is right;
- G3 no longer invents `without`;
- G4 and G5 now choose their heads upstream;
- P005 should validate conformance rather than discover semantic equivalence.

This is the correct architecture.

---

## 2. Blocker: rhetorical class is still missing

The previous review required preserving fact/reasoning/plan class.

P006 v2 says:

> RENDER_GROUP — members express one factual proposition

but G4 is:

- O23 CLAIM_QUALIFIER
- O39 CLAIM_QUALIFIER

That is a **reasoning** group, not a factual group.

The manifest must preserve rhetorical destination explicitly.

Acceptable designs include either:

- separate group types, e.g. `FACT_GROUP`, `REASON_GROUP`, `COMPOSE_GROUP`; or
- one `RENDER_GROUP` plus required metadata such as `CLASS=FACT|REASONING`.

Management composition remains MANAGEMENT/Plan.

A group must never cause a member to cross from evidence/fact to reasoning or Plan.

---

## 3. Blocker: frozen rendered targets still violate the accepted surface contract

### G4

HEAD O23 is:

`but the MRI will tell us`

P006 target:

`The MRI will tell us.`

The accepted transformations do not authorize deleting the discourse word `but`.

If O23 is HEAD and HEAD wording is authoritative, render:

`But the MRI will tell us.`

or separately propose a bounded transformation that drops discourse connectives. Do not silently add one here.

### G5

HEAD O34 is:

`family's concern about her memory is not today's issue`

P006 target:

`Family's concern about her memory, not today's issue.`

That deletes `is` and changes the syntax. The current transformation set does not authorize that contraction.

Render source-faithfully:

`Family's concern about her memory is not today's issue.`

Do not use the group mechanism as a new paraphrase license.

G1 and G2 can use already accepted fold/combine transformations; G3 can render the HEAD directly.

---

## 4. Clarify ungrouped-object behavior

P006 currently says:

> an ungrouped object renders alone

That conflicts with existing 05 selection/relevance rules. A retained but ungrouped object is not automatically mandatory prose.

Required wording:

> An ungrouped object remains subject to the existing 05 eligibility/rendering rules; P006 only removes semantic duplicate/composition decisions for objects that are explicitly grouped.

If the eventual goal is to move **all** render eligibility upstream, that is a separate proposal, not an implication of P006.

---

## 5. Validation correction for COVERED

Current validation says:

> every COVERED appears in the trace and nowhere in the output text

That is too literal. A COVERED duplicate may share words with the HEAD, so text-substring absence is impossible to enforce.

Mechanical requirement should be:

> COVERED has no independent output-line provenance/trace assignment; it is accounted for only through its group.

Its words may naturally overlap with the rendered HEAD.

---

## 6. Ordering must follow rhetorical section, not a flat group order

Validation currently says:

> rendering order follows group order within the facts block

But P006 contains reasoning and management groups too.

Specify:

- FACT groups participate in the existing facts order;
- REASONING groups participate in the existing reasoning order;
- COMPOSE groups participate in the existing Plan bucket/order;
- grouping does not create a new cross-class ordering system.

---

## 7. External audit: preserve the raw audit, not only the provenance critique

The repository currently contains:

`artifacts/doximity_audit_2026-11-14.md`

but that file is a **provenance analysis of the audit**, not the raw Doximity audit response itself.

For an auditable record, if the raw audit response is available, store it unchanged as a separate artifact, e.g.:

`artifacts/doximity_audit_raw_2026-11-14.txt`

Then keep the provenance critique separately.

Do not rewrite the raw audit to correct its mistaken premises.

---

## 8. Do we need to rerun the Doximity audit?

**Yes, if we want to use Doximity's audit as evidence about set 3 specifically.**

The first audit analyzed the local mock outputs, not set 3. Its set-specific claims cannot be carried forward.

A corrected audit should use exactly:

- `05_WRITE_AP.md`
- `AP_ANCHOR.md`
- `STANDING_ITEMS.md`
- `handoff_v2.txt`
- set3 `run1.txt`
- set3 `run2.txt`
- set3 `run3.txt`

Until that rerun exists, use the first audit only as exploratory architectural commentary.

---

## 9. Scope decision: P006 now, P007 only if residual evidence warrants it

Do not automatically implement the audit's proposed five-part normalization.

Current evidence:

- evidence identity/duplication -> P006 directly addresses it;
- reasoning identity -> P006 directly addresses it;
- management hold/resume composition -> P006 directly addresses it;
- standing items -> already fixed by packaging;
- COURSE typing -> remains outside P006 and may deserve P007, but set 3 did not show a major COURSE instability.

Therefore the smallest architecture is:

`03 grouping adjudication -> 04 transport -> 05 formatting -> P005 validation`

Test that before expanding.

This follows the signer's stated preference for consistency without accumulating unnecessary rules.

---

## Next

1. Revise P006 for rhetorical class, exact surface fidelity, ungrouped behavior, COVERED validation, and class-specific ordering.
2. Preserve/import the raw Doximity audit if available.
3. Rerun the Doximity audit on the actual set-3 files if its opinion is going to influence architecture.
4. Then review P006 v3.

No signer-level clinical/style decision is required for the P006 corrections. The signer only needs to perform the corrected audit rerun if we want that additional external evidence.
