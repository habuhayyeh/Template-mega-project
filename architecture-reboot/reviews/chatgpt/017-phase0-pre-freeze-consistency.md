# ChatGPT review 017 — Phase 0 pre-freeze consistency check

## Verdict

**REVISE — final consistency corrections.**

The control plane is now close. The remaining issues are not architectural; they are internal contradictions, stale wording, and evidence/ownership mismatches that would undermine Phase 0 if frozen as-is.

No Phase 1 yet.

---

# 1. AUDIT_PROTOCOL — two consistency fixes

## A. Mode B description contradicts the sign-off rule

Mode B currently says it is used for:

> any run offered as acceptance evidence

But §5 correctly says:

> either mode may accept if every declared assertion is decidable from the available evidence.

Keep §5.

Revise the Mode B usage statement to something like:

> used whenever the declared acceptance assertions require source/IR/check evidence not available in artifact-only mode, and for disputed cases where fuller evidence is needed.

Do not imply Mode B is universally required for acceptance.

## B. Finding owner must be exactly one owner

The example records:

> OWNER STRUCTURE / S2

The frozen experiment protocol requires every scored assertion to have exactly one owner.

Use:
> OWNER S2

If two seams need testing, create two assertions.

---

# 2. ACCEPTANCE_BRIEF_TEMPLATE — C13 behavior should preserve reuse/accounting

Current:

> object is dispositioned NOT_USED with a reason

That can be wrong when the object is invalid for one proposed note use but valid elsewhere.

Use:

> reject the proposed note use; preserve the source object and its valid uses, or give it an explicit disposition if it has no valid use.

The failure is over-inclusion of a use, not destruction of the object.

No other blocker in this file.

---

# 3. CHANGE_CONTROL — still internally contradictory

This is the clearest remaining blocker.

Opening definition currently says IMPLEMENTATION CHANGE:

> does not alter any ... observable behaviour

Then the requirements correctly say:

> Observed outputs may change; frozen properties may not.

Both cannot be true.

Freeze the latter principle.

Definition should be:

> IMPLEMENTATION CHANGE changes how a frozen contract is implemented without changing its interface, semantic authority, contract, or acceptance properties.

Observed outputs may change within the allowed contract.

Also remove stale phrases:

- reviewer currently `confirms no ... observable behaviour changed`;
- table currently says reviewer `confirms locality`.

Replace with:

> reviewer confirms frozen contract/interface/acceptance properties are unchanged and required regression tests pass.

This matters because non-local output change is exactly the C14 risk.

---

# 4. FIXTURE_REGISTER — evidence and ownership corrections

## A. F-01 owner is not supported by the historical event

The historical `postictal confusion resolved` failure occurred in old `05` during an under-specified no-dispatcher call.

That does **not** establish I3 as the historical owner.

In the new architecture, unsupported final-note status could arise at multiple seams; if the Case IR is correct and R1 adds `resolved`, R1 owns it.

Therefore do not assign the historical fixture globally to I3.

Better:
- keep F-01 as an **execution-envelope/source-fidelity historical regression**;
- derive seam-specific assertions when used:
  - I3 lexical/source support assertion if testing extraction;
  - R1 no-unsupported-semantic-addition assertion if testing rendering.

Each derived assertion has one owner.

## B. F-02/F-03/F-04 must encode one-owner assertions explicitly

Current fixture says:
> Owner S4 (mechanical), S2 (identity)

This is conceptually correct but violates the one-assertion/one-owner protocol unless split.

Represent as two assertions:

1. **S2 / SEMANTIC_AUDIT**
   - duplicate/related/distinct identity is correct.
2. **S4 / MECHANICAL**
   - given the adjudication, canonical/covered/use representation and per-(section, problem) uniqueness are obeyed.

Do the same anywhere a fixture currently lists primary + secondary owners.

## C. F-06 must distinguish packaging and S4 assertions

Historical fact:
- initial standing-item omission was untestable because the package omitted the standing-item authority;
- once included, `Seizure precautions` appeared 3/3 in set2 and 3/3 in set3.

Evidence should cite exact paths:
- `PACKAGE.md`
- `reviews/P003-implementation-doximity-original-branch.md`
- `runs/2026-11-14-p003-doximity/set2/validation.txt`
- `runs/2026-11-14-p003-doximity/set3/validation.txt`

Split assertions:
- BUILD: required contract dependency is present in package;
- S4: given a satisfied structured trigger and available standing-item contract, required unit is represented.

One owner each.

Do not say `PACKAGE.md before and after`; the current file is the corrected canonical package, not both historical versions.

## D. C-01 is a contradiction fixture, not necessarily duplicate owner contracts

Current:
> one decision, two owners
> build fails when two rules own one decision

But `proposals/P003-ap-render.md §1` documents contradictory instructions inside old `05`, including:
- CLAIM_QUALIFIER then EVIDENCE vs reasoning renders last;
- ETIOLOGY line vs reasoning-bullet conflict.

That is primarily **L1 contradictory normative rules governing the same decision**, even if they share the same owner contract.

Required behavior:
> BUILD blocks contradictory rules for one decision, whether the contradiction occurs within one contract or across contracts.

Do not turn C-01 exclusively into L2 duplicate-authority.

## E. C-02 still misdescribes the evidence

Current:

> adding the EVIDENCE_MODE requirement for COURSE collided with an existing rule governing course text

This is not what `artifacts/06_doximity_run3.md` says.

Use the exact documented event:

> the added EVIDENCE_MODE clause said a prior-record result belongs with its finding in NEURO_HISTORY; SECTION_CONTRACT rule 38 said historical disease-specific studies belong in WORKUP. O51 moved from WORKUP in run 2 to NEURO_HISTORY in run 3 immediately after the conflicting clause was added.

This is both:
- C11 contract contradiction;
- C14 non-local regression after contract edit.

C-02 specifically tracks the regression process.

## F. C-12 cites the wrong source

Current evidence:
`artifacts/doximity_operator_stress_results_2026-11-15.md`

The exact `The MRI to show.` finding is documented in:

`artifacts/doximity_bplus_operator_experiment_2026-11-15.md`

Use that path.

The experiment explicitly says:
- T4 was identical in all three runs;
- it was an incomplete operator/input representation defect;
- T8 showed the complete TEST + PURPOSE pattern.

Keep the D-017 distinction.

## G. F-07 must use one-owner assertions

Current:
> Owner S4 (producer), R1 (fail-closed)

Split:

1. S4/CHECK assertion:
   - emitted structural artifact must typecheck.
2. R1 assertion:
   - if malformed structure reaches realization, fail closed with `CONTRACT_ERROR`; never repair.

## H. Fixture register rule conflicts with acceptance brief

Current §6:
> A brief cites at least one fixture; historical preferred.

Acceptance brief now correctly says:
> cite all relevant historical fixtures, plus justified derived fixtures where needed.

Make the register use the same rule.

---

# 5. Evidence path precision

For F-02/F-03/F-04, prefer full literal repository paths for each run rather than one full path followed by shortened `set3/run2.txt` references.

This is minor, but the register's own principle is:
> evidence is a path, not a recollection.

---

# 6. Freeze target

If these changes are applied, I expect no remaining conceptual blocker.

Final unit-read criteria:

- no contradictory definitions across the five Phase 0 files;
- every assertion has exactly one owner;
- fixture paths point to the exact evidence claimed;
- historical evidence is not overinterpreted;
- audit/brief/change-control rules agree with the frozen Doximity protocol.

After that, Phase 0 can be marked **ACCEPTED / FROZEN** and only then may Phase 1 begin.
