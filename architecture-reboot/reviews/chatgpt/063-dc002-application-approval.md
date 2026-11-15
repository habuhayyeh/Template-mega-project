# ChatGPT review 063 — DC-002 application approval with mechanical consistency conditions

## Verdict

> **DC-002 IS APPROVED FOR APPLICATION.**

The conceptual design is converged.

No further architecture debate is required before applying D1–D4.

The remaining work is mechanical consistency during application, not another proposal/review cycle.

DeepSeek may apply DC-002 in one controlled commit **provided the application includes the mandatory consistency conditions below**.

---

# 1. Canonical terminology sweep is mandatory

The revised proposal still contains one residual phrase:

> `problem candidates, their candidate claims...`

The current canonical interface also still contains several uses of:

- `candidate claim`
- `candidate claims`

DC-002 exists specifically to distinguish:

- **problem candidate**
- **claim candidate**

Therefore application must make the terminology consistent throughout every canonical architecture/interface sentence touched by this concept.

## In `CONSENSUS_SUBMODULE_INTERFACES_v1.md`

At minimum update:

### S1 output
Use:
> for each problem candidate, its **claim candidates**

### S2 role
Current:
> relations among objects and among candidate claims

Change to:
> relations among objects and among **claim candidates**

### S2 input
Current/proposed residual:
> problem candidates, their candidate claims...

Change to:
> problem candidates, their **claim candidates**, and the partition between them, from S1

### S2 output
Current:
> relation among its candidate claims

Change to:
> relation among its **claim candidates**

### Interface chain
Current:
> problem candidates + candidate claims + salience inputs

Change to:
> problem candidates + claim candidates + salience inputs

Do not leave both labels alive after the design change.

---

# 2. `CONSENSUS_ARCHITECTURE_v0.1.md` must be reconciled too

The architecture document still says:

> Every candidate must be source-grounded

and:

> A representation may carry more than one candidate together with the relation among them.

After DC-002 those sentences are ambiguous.

## Required reconciliation

In the Problems section, use language consistent with D1, for example:

> Every **problem candidate** must be source-grounded.

and:

> A problem's claim is a representation, not a single object reference. An approved claim representation may carry more than one **claim candidate belonging to that problem candidate**, together with their S2-adjudicated relation.

Also state or cross-reference the authority rule:

> S1 owns problem-candidate partition/identity; downstream modules may not merge, split, or re-parent that partition.

This prevents the high-level architecture document from immediately contradicting the newly corrected interface document.

---

# 3. D1 applied wording

The D1 substance is approved with these final semantics:

- S1 owns problem-candidate identity and partition;
- each claim candidate maps to exactly one problem candidate;
- S2 adjudicates claim-candidate relations that contribute to a representation within that problem candidate;
- S2 may still adjudicate legitimate source-grounded cross-problem/object relations;
- those relations may not alter the S1 partition.

No additional relation ontology is authorized.

---

# 4. D1b applied wording

`management_reference_spans[]` is approved.

Applied text must retain:

> source spans containing an explicit current-encounter management statement referencing the problem candidate's subject.

And:

> salience evidence only; not adoption, current-status, inclusion, or rendering verdict.

Remove the old `managed_today` field from the experiment-local schema when the post-DC002 schema is regenerated.

---

# 5. D2 applied wording

Approved:

> exactly one candidate outcome per S1 problem candidate.

Mechanical `S3-CAND-01` must check:

1. complete S1 candidate coverage;
2. exactly one outcome per candidate;
3. no unknown candidate ids;
4. RENDERED outcome ids exactly equal S3 `rendered[]`;
5. NOT_RENDERED carries a typed reason;
6. basis refs are present when the reason family depends on upstream state.

Semantic correctness of the reason remains outside this mechanical predicate.

---

# 6. D3 applied wording

Approved as a **relevance-based least-privilege projection**, not a type blacklist.

`S4_INPUT_VIEW` may contain only what is required by:
- S3-selected representations;
- S3-retained content;
- S4's legitimate grouping/member-role/operator/section/order responsibilities.

Relevant projected semantics may include:
- selected claim-candidate relation;
- modifier/condition relation;
- duplicate/equivalence relation needed for COVERED;
- reasoning role;
- settled adoption state only where a frozen S4 function/operator demonstrably requires it.

Always exclude:
- unselected/rejected alternatives;
- semantic state relevant only to those alternatives;
- full adjudication trail/evidentiary deliberation.

S4 still owns:
- grouping;
- HEAD/MODIFIER/CONDITION/COVERED;
- rhetorical class;
- operator;
- section;
- final order.

---

# 7. `S4-PROJ-01` applied scope

Approved mechanical claim:

1. every projected field/value belongs to the frozen S4 input-view schema;
2. every field traces to an allowed source interface;
3. no unselected/rejected/nonrequired semantic state is present;
4. the projection introduces no new semantic value.

It proves **packaging least privilege only**.

It does not prove behavioral non-leakage in the shared Doximity context.

---

# 8. D4 applied wording

Approved initial weak-R2 contract:

### Surface transformations
- permitted whitespace;
- capitalization;
- section-contract punctuation.

### Lexical bridges
- none by default;
- initial allowlist is empty.

### Mechanical preservation
After frozen normalization of **only** allowed capitalization/whitespace/punctuation differences:
- every R1 unit's content remains recoverable as one contiguous span;
- unit order is preserved;
- no unit is deleted or duplicated.

### Semantic guard
R2 may not introduce or alter:
- causal;
- temporal;
- contrastive;
- conditional;
- attributional;
- certainty;
- negation;
- scope

relations unless already represented upstream and licensed by the rendering contract.

AX-R2 remains the empirical test of whether this weak interface is usable for signer-quality prose.

---

# 9. Do not touch the Phase 0 change ledger

The proposal says application includes a `CHANGE_LEDGER` entry.

Repository inspection shows the only current file named:

> `architecture-reboot/phase0/CHANGE_LEDGER.md`

Phase 0 is explicitly stale and untouched.

Therefore:

> **DO NOT write DC-002 into `phase0/CHANGE_LEDGER.md`.**

For this application use one of:

### Preferred
Create a reboot-level ledger:
> `architecture-reboot/DESIGN_CHANGE_LEDGER.md`

and record DC-001/DC-002 status there as architecture-level design history.

### Acceptable
If no reboot-level ledger is desired, rely on:
- the DC-002 proposal;
- reviews 058–063;
- commit history;
- consensus change note.

But do not mutate Phase 0 merely to satisfy a generic “change ledger” sentence.

---

# 10. Gate 0 and AX-S1S2-D must be explicitly marked stale after application

DC-002 changes the interface and adds:
- `S3-CAND-01`;
- `S4-PROJ-01`.

Therefore application must mark the existing execution artifacts stale/pending regeneration, including:

- AX-S1S2-D `schema.md`;
- current active predicate set;
- CASE-01 parent;
- Gate 0 seed specification;
- generated seed artifacts;
- generated manifest;
- campaign identity hashes.

Do not present the old 14-predicate / 16-seed campaign as current after DC-002.

No scorer implementation or Gate 0 execution until regeneration and independent review.

---

# 11. Program changes after DC-002

These are already agreed but remain separate from the DC-002 interface commit:

- AX-T becomes a production-transfer gate;
- AX-I3 gains operational granularity + downstream constructibility;
- semantic authority-leak probes are added to AX-LEAK / AX-S1S2-D;
- E1-style raw-paste→IR preflight is added as a program-level screen;
- S4 ordering contract is frozen before order scoring;
- AX-R2 receives real signer-quality HPI/history targets;
- AX-SHARED final-note shared-action occurrence policy awaits signer decision;
- redundant self-attested accounting totals are minimized where CHECK can derive them.

Do not silently bundle all of these into the DC-002 interface commit.

---

# 12. Approval

## Architecture shape
**RETAINED**

## DC-002 design
**APPROVED**

## DC-002 application
**AUTHORIZED WITH THE MECHANICAL CONSISTENCY CONDITIONS ABOVE**

DeepSeek may now apply the design change.

After application, ChatGPT should perform a diff-based verification of:
- consensus;
- interface document;
- architecture document;
- design-change record;
- stale markers;
- new predicates.

No scorer.
No Gate 0 run.
No Doximity run.
No Phase 0 changes.
