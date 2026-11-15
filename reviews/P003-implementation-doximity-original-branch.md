# P003 implementation + Doximity runtime review — original architecture branch

**Scope:** implemented `05_WRITE_AP.md`, `AP_ANCHOR.md`, local P003 runs, and `runs/2026-11-14-p003-doximity/`

## Verdict

**P003 architecture remains ACCEPTED. P003 implementation/runtime is NOT ACCEPTED.**

The runtime findings are real, but the current Doximity validation overstates what the three files prove because the test conditions were not identical.

## 1. The current Doximity "three-run set" is not one reproducibility set

`run1.txt` had **no dispatcher**.

`run2.txt` and `run3.txt` used the dispatcher.

Therefore run1 is not one of three identical-condition repetitions. Preserve it as evidence of what Doximity may do when the task is under-specified, but label it as a **no-dispatcher control / setup failure**, not as one member of the canonical P003 reproducibility set.

The fabricated line:

`postictal confusion resolved`

is serious evidence that an under-specified Doximity call may invent a status. It does **not** establish that the dispatcher-qualified P003 contract itself fabricated a status, because runs 2 and 3 did not do so.

A valid Doximity reproducibility test still requires three fresh runs with the **same dispatcher and same attached files**.

## 2. The missing `Seizure precautions` is not yet a valid runtime failure

The dispatcher supplied to the signer instructed Doximity to read:

1. `05_WRITE_AP.md`
2. `AP_ANCHOR.md`
3. `handoff.txt`

It did **not** instruct the signer to attach/read `STANDING_ITEMS.md`.

But `05_WRITE_AP.md` permits standing items by reference to that external file; the actual text `Seizure precautions` is not contained in `05_WRITE_AP.md`.

Therefore Doximity could not be expected to render that item from the test package it was given.

This was a test-packaging defect, not evidence that Doximity ignored the standing-item rule.

The corrected dispatcher/package must include `STANDING_ITEMS.md`.

## 3. Dispatcher-qualified runs still fail P003

Even after removing the invalid conclusions above, runs 2 and 3 are not acceptable.

### Run 2
- renders O54 residual aphasia, contrary to D-014;
- renders both MRI-hedge formulations, duplicating one reasoning proposition;
- substitutes provenance for the O8 timing instead of preserving the COURSE timing.

### Run 3
- duplicates the family-memory concern;
- omits the O8 infarct timing.

So the implementation/runtime is still **FAIL** on source selection/deduplication and reproducibility.

## 4. D-014 exposes an upstream contract contradiction, not merely a missing checker

`05_WRITE_AP.md` states:

> The Handoff is the whole population.

But the frozen Handoff contains O54, while D-014 says O54 must stay out of the A/P.

`05` does not read `DECISIONS.md`, and under D-002 it should not return to external clinical sources/state to discover a hidden exclusion.

Therefore the present architecture is internally inconsistent at the stage boundary:

- the Handoff says O54 is available;
- the permanent decision says O54 is unavailable for A/P.

The durable fix is to make the A/P input encode the decision upstream — i.e. the selected ledger/Handoff for this baseline must exclude O54. Do **not** add a hidden D-014 exception sentence to `05`.

When P004 later supersedes D-014 for the chronic-infarct block, the upstream representation/ledger can change explicitly.

## 5. Checker vs more prose

**Recommendation: build a checker before adding more prose, but only after fixing the input/package contradictions above.**

Do not ask prose `05` to enforce facts it was never given (standing items file) or exclusions contradicted by its input (O54).

A post-output checker should initially be **fail-only**, not an auto-rewriter. It should detect contract breaches and force review/rerun rather than silently repair a note.

High-value deterministic checks include:

1. **Unsupported line status:** any line status must map to an explicit COURSE status.
2. **Required standing item:** when a closed-list trigger is satisfied and `STANDING_ITEMS.md` is part of the package, required item must be present.
3. **Block ownership:** a rendered MANAGEMENT item must come from the same input problem block.
4. **Forbidden/omitted input IDs:** only if those exclusions are explicitly carried in the stage input or an acceptance manifest.
5. **Duplicate exact/normalized plan items or repeated source propositions** where deterministically detectable.

Do not pretend a checker can deterministically solve all semantic near-duplicate reasoning. Use it for enforceable invariants first.

## 6. Required next sequence

1. Correct the Doximity validation narrative:
   - run1 = no-dispatcher control, not canonical repetition;
   - standing-item omission = untestable with the incomplete package.
2. Fix the baseline A/P input so D-014 is represented upstream (O54 not available to P003 `05`).
3. Define a complete Doximity package:
   - `05_WRITE_AP.md`
   - `AP_ANCHOR.md`
   - `STANDING_ITEMS.md`
   - frozen Handoff
   - identical dispatcher
4. Build a **fail-only output checker proposal** for the mechanically enforceable invariants.
5. Then run three fresh Doximity repetitions under identical conditions.

## 7. STATUS implication

Current Doximity acceptance should not be described as merely pending.

The implemented stage has already produced unacceptable dispatcher-qualified outputs. Record it as **FAILED / new canonical three-run protocol required after packaging/input corrections**.

No signer-level clinical or stylistic decision is required for these corrections.
