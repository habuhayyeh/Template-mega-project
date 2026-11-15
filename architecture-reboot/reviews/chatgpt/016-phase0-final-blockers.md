# ChatGPT review 016 — Phase 0 final blockers

## Verdict

**REVISE — narrow final blockers only.**

The second revision is materially better and resolves most of review 015. Remaining issues are now localized. No architecture reopening is required.

Do not start Phase 1 until these are corrected.

---

# 1. AUDIT_PROTOCOL — still the main blocker

## A. Remove the fixed ten-item clinical rubric

The document says the ten questions are "not a fixed rubric," but they still encode permanent artifact-specific clinical rules:

- no two problems are the same thing;
- duplicate identity rule;
- adoption rule;
- placement rule;
- operator-thinner-than-payload rule;
- standing-item completeness;
- voice rule.

Those belong in frozen contracts / fixture assertions / acceptance briefs.

The Phase 0 audit procedure should instead be:

1. identify the artifact/seam under test;
2. load the frozen acceptance assertions for that artifact;
3. determine which assertions are decidable from the supplied evidence;
4. evaluate each assertion using its declared validation mode;
5. record PASS / FAIL / BLOCKED;
6. for every failure record evidence + single owning submodule/process;
7. collect every independently interpretable finding;
8. stop only when a prerequisite/integrity failure makes dependent assertions undecidable;
9. escalate genuine semantic ambiguity to the signer.

Generic integrity checks may be procedural, but clinical expectations must come from the referenced fixture/contract.

## B. Acceptance cannot require "Mode B" universally

Current:

> A Mode A audit may reject or report, but may not sign an acceptance decision. Acceptance requires Mode B.

This conflicts with the frozen artifact-level batch protocol.

Examples:
- fixed valid Case IR -> R1/R3 render acceptance may be decidable from Case IR + rendered artifact + checks, without raw source;
- BUILD or schema artifacts may have no "final note";
- artifact-level acceptance may be fully decidable at its seam.

Correct rule:

> An audit may sign acceptance only when **all acceptance assertions declared for that artifact are decidable from the supplied frozen inputs/evidence**.

If source fidelity is one of the assertions, source is required.
If the seam is Case-IR -> rendered output, the frozen Case IR may be sufficient.

Rename modes if useful, but do not make "full source + IR + note" a universal acceptance prerequisite.

## C. Artifact inputs should be seam-defined

Mode A should not predeclare "consistency, placement, completeness, voice" as answerable. The acceptance brief determines what is answerable.

---

# 2. ACCEPTANCE_BRIEF_TEMPLATE — two remaining corrections

## A. Fixture rule still risks ceremonial fixtures

Current:

> A brief cites at least one fixture; historical preferred.

Use the already-agreed rule:

> A brief cites **all relevant mandatory historical fixtures**. If no historical fixture covers the invariant, use a justified derived fixture.

Do not require an unrelated historical fixture.

## B. Examples contain stale/nonexistent ids and noncanonical mode names

Current examples reference:
- F-09 standing item;
- F-12 as a derived fixture.

Those do not match the current register.

Use real ids or generic placeholders.

Validation mode vocabulary should match the frozen terminology:
- MECHANICAL
- SEMANTIC_AUDIT
- HYBRID

not generic `SEMANTIC`.

---

# 3. CHANGE_CONTROL — implementation change definition is still too strict

Current:

> does not alter ... observable behaviour

That is not appropriate for an LLM implementation change.

A prompt/operator implementation change may intentionally change actual outputs while preserving the **same frozen contract and acceptance properties**.

Correct definition:

> IMPLEMENTATION CHANGE changes how a frozen contract is implemented without changing the contract, interface, semantic authority, or acceptance properties.

Then:
- targeted acceptance tests must still pass;
- relevant regression suite runs to detect non-local side effects.

Do not classify by "no observable behavior change."

## Signer approval for acceptance changes

Current table still says signer merely "informed" for ACCEPTANCE CHANGE.

Required distinction:
- acceptance change to a signer-approved clinical/style/product baseline -> **signer approval required**;
- purely mechanical engineering expectation -> independent reviewer approval may suffice, signer informed per project policy.

Make that explicit in the table/rule.

---

# 4. FIXTURE_REGISTER — remaining evidence corrections

## F-01 path is wrong

Current:
`runs/2026-11-14-p003-doximity/set1/run1.txt`

There is no `set1/` directory.

Correct:
- `runs/2026-11-14-p003-doximity/run1.txt`
- `runs/2026-11-14-p003-doximity/validation.txt`
- `reviews/P003-implementation-doximity-original-branch.md`

Keep the no-dispatcher boundary.

## F-02/F-03/F-04 path is not a real literal path

Current:
`runs/2026-11-14-p003-doximity/set3/run1–3.txt`

Use actual paths:
- `.../set3/run1.txt`
- `.../set3/run2.txt`
- `.../set3/run3.txt`
- and/or `.../set3/validation.txt`

The two-level semantic/mechanical ownership is now correct.

## F-06 needs exact evidence paths

Add:
- `PACKAGE.md`
- `reviews/P003-implementation-doximity-original-branch.md`
- `runs/2026-11-14-p003-doximity/set2/validation.txt`
- `runs/2026-11-14-p003-doximity/set3/validation.txt`

Phrase the defect as **incomplete package made standing-item behavior untestable**, not "Doximity omitted a required line."

## C-01 evidence is still imprecise

Current:
> pipeline/05_WRITE_AP.md at the rewrite, against AP_ANCHOR

Use the preserved evidence that explicitly documents the historical contradiction:

`proposals/P003-ap-render.md` §1:
- old 05 said bullets come from CLAIM_QUALIFIER then EVIDENCE;
- also said reasoning renders last;
- etiology rules also conflicted.

This is stronger than citing the current rewritten 05.

## C-02 description is still wrong

Current describes:
> EVIDENCE_MODE requirement for COURSE collided with an existing rule governing course text

Canonical evidence says something else.

Use exactly:
- `artifacts/06_doximity_run3.md`
- added `EVIDENCE_MODE` clause said a prior-record result belongs with its finding in `NEURO_HISTORY`;
- `SECTION_CONTRACT` rule 38 said historical disease-specific studies belong in `WORKUP`;
- O51 moved from WORKUP in run 2 to NEURO_HISTORY in run 3.

That is the C11 contradiction plus C14 non-local regression evidence.

## C-12 needs an evidence path

Add:
`artifacts/doximity_bplus_operator_experiment_2026-11-15.md`

Use the experiment's interpretation:
- T4 repeatedly rendered `The MRI to show.`;
- stable 3/3;
- incomplete conversational proposition / operator-input defect;
- T8 demonstrated the complete structured TEST + PURPOSE pattern.

Keep the explicit distinction from signer-approved D-017 `MRI to show.`.

## F-07 needs exact evidence path

Use:
`artifacts/06_doximity_run3.md`

The malformed REUSE is actual Doximity evidence.

## F-10 should not be mandatory without an exact evidence path

Current:
> same run family

That violates the register's own rule:
> evidence is a path, not a recollection.

Either:
- provide exact raw/review path and quote the relevant behavior;
- or move F-10 to provisional.

Also keep seam ownership explicit:
- I4 if annotation confuses provenance date vs event time;
- R1 if correct annotation is rendered as event time;
- S2 is not the generic owner of provenance assignment.

## F-11 is now acceptable
The runtime evidence is correctly tied to set2.

## F-12 is now acceptable
The exact raw run is identified.

---

# 5. BUILD_LINT — essentially acceptable, one wording cleanup

The structural changes are correct:
- decision authority belongs to owner_contract;
- BUILD/SHARED scopes exist;
- serialization not frozen;
- unresolved authority blocks build.

One wording statement is too strong:

> if a machine cannot decide whether two statements conflict, a reader cannot either

A human reviewer may be able to resolve it.

Use:

> if the machine cannot establish compatibility, compilation blocks until the authority is resolved by review or the rules are rewritten into comparable structured form.

This preserves fail-closed behavior without claiming human undecidability.

No other Phase 0 blocker here.

---

# 6. Phase 0 freeze criteria

After these changes I expect Phase 0 to be freezeable if a final unit re-read confirms:

- BUILD_LINT is internally consistent;
- AUDIT is procedure-only and seam/assertion-driven;
- ACCEPTANCE_BRIEF uses relevant fixtures and canonical validation modes;
- CHANGE_CONTROL distinguishes implementation behavior from acceptance-contract changes correctly;
- every mandatory fixture has an exact valid evidence path and accurate evidence boundary.

No new design proposals are requested.

---

# 7. Requested response

Please revise the five files and return a short point-by-point disposition.

If all items are applied, I will perform a final unit read and either:
- **ACCEPT / FREEZE PHASE 0**, or
- identify only a concrete remaining contradiction/evidence error.

No Phase 1 before that verdict.
