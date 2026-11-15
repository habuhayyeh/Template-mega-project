# ChatGPT review 064 — DC-002 applied-diff verification

## Verdict

> **DC-002 DESIGN REMAINS APPROVED, BUT APPLICATION COMMIT `a856e39` IS NOT YET VERIFIED. A CORRECTIVE COMMIT IS REQUIRED.**

The problem is not DC-002 conceptually.

The problem is that the application commit mixed the intended design change with several unintended deletions/weakening edits in previously frozen interface text, and did not fully instantiate all stale markers/predicate requirements from review 063.

Do **not** revert DC-002.

Make one narrow corrective commit restoring the old protections while retaining the approved D1–D4 changes.

No scorer.
No Gate 0 run.
No Doximity.
No Phase 0.

---

# 1. Critical regression — S4 standing-item exception was deleted

Before DC-002, S4 contained the frozen standing-item exception:

> A render unit may have zero source-object members only for a closed-list standing item whose explicit trigger conditions are satisfied by the structured Case IR/problem state. Such units participate in the same completeness accounting as other units.

The DC-002 commit deleted this entire section.

DC-002 did not supersede it.

## Required correction

Restore the standing-item exception verbatim or semantically identically under S4 output/boundary.

This is a previously frozen rule and must not disappear as collateral editing.

---

# 2. Critical regression — S2 safety boundary was weakened

Pre-DC002 S2 explicitly said:

> S2 answers "what do these objects mean here, and which claim formulations are defensible?"  
> It does not select content, choose sections, or order.

and the approval rule ended with:

> Documenting an unresolved choice does not make it safe.

The application replaced this with the new partition language but silently removed those existing limits.

DC-002 did not transfer any of those decisions away from S2/S3/S4.

## Required correction

Keep the new DC-002 partition rule **and restore** the preexisting S2 boundary:

- S2 does not select content;
- S2 does not choose sections;
- S2 does not order;
- unresolved semantic choice cannot be made "safe" merely by documenting it;
- if multiple approved representations require a clinically meaningful semantic choice, S2 resolves it before S3.

Do not simplify away an older safety invariant merely because D1 adds new text to the same paragraph.

---

# 3. Critical regression — S3 safety boundary was weakened

Pre-DC002 S3 explicitly said:

- **S3 does not resolve semantic ambiguity**;
- it may not render an A/P problem without an S2-approved representation;
- if another governing requirement mandates such a problem, **the seam fails/flags rather than rendering a claimless block**;
- if multiple approved representations remain and the choice is not semantically free, that is an S2 defect, not an S3 choice.

The application retained only a shortened subset.

DC-002 candidate accounting does not supersede any of those rules.

## Required correction

Restore all of the above while keeping the new candidate-outcome/accounting text.

D2 adds candidate accounting. It does not broaden S3 authority.

---

# 4. S4 distinctive boundary also lost frozen statements

Pre-DC002 S4 explicitly answered:

> "exactly what must render, where, in what unit, with which operator, and in what order?"

and stated:

> It does not write prose.

Those statements disappeared when D3 was applied.

They remain true.

## Required correction

Restore them alongside the new `S4_INPUT_VIEW` language.

DC-002 narrows S4's input; it does not change S4's unique question or give it prose-writing authority.

---

# 5. Canonical terminology sweep is incomplete

Review 063 required removal of residual `candidate claim(s)` terminology from canonical interface text.

The current interface still has at least:

> interface chain: `problem candidates + candidate claims + salience inputs`

This must become:

> `problem candidates + claim candidates + salience inputs`

Also inspect the entire canonical interface for any remaining `candidate claim` / `candidate claims` phrase and replace it with `claim candidate` / `claim candidates` where it means the DC-002 concept.

Do not leave two labels alive.

---

# 6. `CONSENSUS_ARCHITECTURE_v0.1.md` was only partially reconciled

Review 063 required the Problems section itself to stop using ambiguous `candidate`.

The commit added a new clarifying sentence, but retained the old ambiguous statements:

> Every candidate must be source-grounded

and:

> A representation may carry more than one candidate together with the relation among them.

Those now conflict with the point of D1.

## Required correction

Use:

> Every **problem candidate** must be source-grounded...

and:

> An approved claim representation may carry more than one **claim candidate belonging to that problem candidate**, together with their S2-adjudicated relation.

Do not merely add a glossary sentence while leaving the old ambiguous invariant in place.

---

# 7. R2 application contains a textual defect and should be integrated cleanly

Current applied text says:

> `Leftover a bridge must be licensed by an upstream relation plus the contract.`

This is malformed text.

More importantly, D4 was appended after the old R2 hard boundary rather than cleanly integrated into it.

The old text says:
- join adjacent units;
- add punctuation/whitespace;
- no temporal/causal connective not represented.

The new text says:
- normalization guard;
- empty lexical bridge allowlist;
- no-new-relation audit.

These are compatible, but the canonical interface should contain **one coherent R2 contract**, not an old rule plus an appended patch block.

## Required correction

Integrate the approved D4 wording into the R2 Hard boundary:

### Allowed
- join ordered R1 units without semantic synthesis;
- whitespace;
- capitalization;
- section-contract punctuation;
- no lexical bridge tokens initially.

### Mechanical guard
After frozen normalization of allowed capitalization/whitespace/punctuation:
- every unit content recoverable as a contiguous span;
- order preserved;
- no deletion or duplication.

### Semantic guard
No introduced/altered:
- causal;
- temporal;
- contrastive;
- conditional;
- attributional;
- certainty;
- negation;
- scope

relation.

Remove the malformed sentence.

---

# 8. `S3-CAND-01` predicate is weaker than the approved contract

Current row checks:
- coverage;
- exclusivity;
- equality of RENDERED set;
- typed reason on NOT_RENDERED.

Review 063 also required:

- no unknown candidate ids;
- basis refs where a reason family depends on upstream state.

The interface now requires basis refs, but the predicate does not check them.

## Required predicate wording

`S3-CAND-01` mechanical checks:

1. every S1 problem-candidate id appears exactly once in candidate outcomes;
2. no outcome references an id absent from S1;
3. ids with `status=RENDERED` equal S3 `rendered[]` exactly;
4. every NOT_RENDERED outcome has a typed reason code;
5. where that reason family depends on an upstream state, required basis refs are present.

Semantic truth of the reason remains separately audited.

---

# 9. `S4-PROJ-01` predicate is also weaker than the approved contract

Current row says essentially:

> every field S4 reads is in the frozen view; anything outside is a packaging violation.

Review 063 approved four mechanical checks:

1. field/value belongs to the frozen projection schema;
2. field traces to an allowed source interface;
3. no unselected/rejected/nonrequired semantic state is present;
4. projection introduces no new semantic value.

## Required correction

Make those four checks explicit in `S4-PROJ-01`.

Otherwise the predicate does not actually test the provenance/no-new-semantics properties that define a mechanical projection.

---

# 10. The old active predicate set is not visibly marked stale in `predicates.md`

The file now contains new predicates:
- `S3-CAND-01`;
- `S4-PROJ-01`;

but its old Pilot `ACTIVE_PREDICATE_SET` remains present and does not include them.

The ledger says the active set is stale, but the predicate registry itself still presents an apparently current active set.

## Required correction

At the active-set section itself, add an unmistakable marker:

> **STALE — PENDING REGENERATION AFTER DC-002. DO NOT SCORE THIS SET.**

Do not yet invent the replacement active set in the corrective commit unless the regenerated experiment is being deliberately performed.

---

# 11. CASE-01 parent was named stale in the ledger but not marked at its artifact location

Review 063 required the old CASE-01 parent to be explicitly stale.

The application did not modify the parent or add a CASE-01-local stale marker.

The generated-artifact `STALE.md` does not cover the source parent clearly enough.

## Required correction

Add a local marker such as:

> `experiments/architecture/AX-S1S2-D/fixtures/CASE-01/STALE.md`

stating that `parent.json` predates DC-002 and must be regenerated/reviewed before Gate 0.

Do not edit a JSON artifact merely to insert prose.

---

# 12. Gate 0 staleness should be visible at the campaign manifest too

The seed spec is marked stale and generated artifacts have `STALE.md`.

But `experiments/gate0/00-GATE0-MANIFEST.md` still appears current.

Because Gate 0's active set/campaign identity changed, the campaign manifest itself should carry:

> **STALE — PENDING REGENERATION AFTER DC-002**

until rebuilt.

This prevents an operator from following a manifest that points to a stale campaign.

---

# 13. `CONSENSUS_ARCHITECTURE_v0.1.md` and interface should not be left at mixed generations

DC-002 altered the interface substantially.

The high-level architecture must be updated only enough to stay semantically consistent:
- problem candidate vs claim candidate;
- S1 partition authority;
- selected/retained least-privilege S4 input concept where the high-level document discusses planning;
- weak R2 remains non-semantic.

Do not rewrite unrelated architecture sections.

The goal is consistency, not another redesign.

---

# 14. Design-change ledger

The new reboot-level ledger is correct in location and Phase 0 was not touched.

Good.

After the corrective commit and verification:
- replace `this commit` with the actual DC-002 application commit hash `a856e39` or the corrected commit range;
- update DC-002 status from `APPLIED / PENDING VERIFICATION` to `APPLIED / VERIFIED` only after this review closes.

Do not mark verified yet.

---

# 15. What passed

The following parts of the application are correct and should not be reopened:

- D1 problem-candidate / claim-candidate authority concept;
- `management_reference_spans[]` concept;
- D2 candidate outcome concept;
- relevance-based `S4_INPUT_VIEW`;
- S4 ownership of render member roles;
- packaging-vs-runtime-leak distinction;
- D4 normalization-before-check concept;
- new reboot-level design-change ledger;
- Phase 0 remained untouched;
- schema and Gate 0 seed corpus were marked stale;
- generated artifacts/hashes were marked stale.

---

# 16. Current status

## Architecture shape
**RETAINED**

## DC-002 design
**APPROVED**

## DC-002 application
**APPLIED BUT NOT VERIFIED — CORRECTIVE COMMIT REQUIRED**

## Gate 0
STALE / UNRUN.

## Scorer
Do not build yet.

## Doximity
No architecture run.

## Phase 0
Untouched.

---

# 17. Next action

DeepSeek should make **one corrective commit only**, containing:

1. restoration of frozen S2/S3/S4 safeguards;
2. restoration of the S4 standing-item exception;
3. canonical terminology cleanup;
4. architecture §6 ambiguity cleanup;
5. clean integrated R2 text;
6. strengthened `S3-CAND-01` and `S4-PROJ-01`;
7. explicit stale markers on active set, CASE-01 parent, and Gate 0 manifest;
8. ledger commit-reference cleanup.

Do not regenerate Gate 0 yet.
Do not build scorer.
Do not run Doximity.
Do not touch Phase 0.

Return the corrective commit and changed-file list for diff verification.
