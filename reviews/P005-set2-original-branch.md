# P005 + Doximity set 2 review — original architecture branch

## Doximity set 2

**Verdict: stability still FAILS. D-014 result is UNINTERPRETABLE until the signer confirms which Handoff was attached.**

### What is now established

The package correction for standing items worked:

- `Seizure precautions` appears in all three runs.
- The prior omission was a packaging defect, not a Doximity runtime failure.

Independent of O54, the three outputs remain materially unstable:

- O2 `admitted 11/12` renders in run1 only;
- CT findings merge/split differently;
- infarct + encephalomalacia merge/split differently;
- reasoning order changes;
- O8 timing is not rendered in the approved anchored form;
- O52 `no further workup` leaks from a prior-neurology record into today's Plan in runs 1 and 2, but not run3.

Therefore the complete package did not solve reproducibility.

### O54 / D-014 cannot yet be scored

All three runs contain `residual mild expressive aphasia`; run2 includes the exact O54 provenance `(prior neurology, February 2024)`.

That content is absent from `runs/2026-11-14-p003/handoff_v2.txt`.

Under the declared PACKAGE conditions (fresh conversation, only four files), the output cannot source O54 from `handoff_v2.txt`.

So one of the following is true:

1. the older `runs/2026-11-14-p002/handoff.txt` was attached;
2. the run was not actually fresh/isolated and Doximity retained other context;
3. some other unrecorded input contained O54.

Do not score D-014 until the signer confirms the actual Handoff used.

## New upstream selection finding: O52

The accepted rule in `05` is:

> A prior-record entry is not a current plan item unless a current-encounter entry re-adopts, continues, or restates it.

Yet `ap_ledger_v4.txt` still places O52 `no further workup [D, Prior neurology, 2025-06]` into `P2.MANAGEMENT`.

That reproduces the same boundary problem previously found with O54:

- upstream input makes the object available as management;
- downstream prose is expected to remember not to use it.

Runs 1 and 2 show that this is unstable.

**Recommendation:** move O52 out of current A/P MANAGEMENT upstream. For this baseline, unless a current encounter object re-adopts it, O52 should be DISCARD from the A/P ledger rather than left for 05 to suppress.

Do not add another special-case sentence to 05.

## O2 is the same class of problem

P003 itself classified O2 `admitted 11/12` as IRRELEVANT for the seizure A/P. Yet the ledger still passes O2 as `P1.COURSE`, leaving 05 to make that relevance judgment again.

Run1 rendered it; runs2-3 did not.

If the acceptance oracle already knows O2 is irrelevant, encode that upstream. The production principle should be:

> decisions already settled by selection/oracle should not be re-decided by prose rendering.

A later selection-hardening proposal should move settled relevance/exclusion decisions upstream rather than expanding 05.

---

# P005 checker

**Verdict: REVISE — direction accepted; several proposed checks are not mechanical as currently specified.**

Fail-only is correct. No auto-rewriting.

## Accepted checker principles

- post-output validation;
- exit clean/breach/usage;
- never repair output;
- distinguish contract breach from cross-run instability;
- do not judge clinical materiality;
- fixture for every check.

## Required corrections

### C1 unsupported line status — ACCEPT WITH TIGHTER SPEC

Do not rely on a generic "final comma segment" parser alone.

Conservatively detect status vocabulary on the problem line and require the corresponding status phrase to be explicitly supported by a COURSE entry in that same block.

If parsing is ambiguous, report UNVERIFIABLE rather than infer a status.

### C2 required standing item — REVISE INPUT FORMAT

The current `STANDING_ITEMS.md` triggers are prose, not machine-readable rules.

A checker cannot honestly "test the trigger's literal terms" for every future item without embedding semantic interpretation.

Create a small machine-readable standing-item manifest (or add explicit structured trigger fields) that provides:
- item ID;
- trigger terms/pattern;
- required output text/normalized signature;
- bucket.

The prose file remains human-readable authority; the checker consumes the structured companion.

### C3 block ownership — REVISE

"Trace words to MANAGEMENT" is not mechanically defined under transformations, merged management fragments, and formatting changes.

Define a deterministic normalization/matching algorithm and require a unique same-block source match.

If a plan line maps only to another block -> breach.
If it maps to no source or ambiguously to multiple incompatible sources -> report UNVERIFIABLE/BREACH according to the acceptance policy; do not guess.

### C4 forbidden IDs — CURRENT CLI CANNOT DO THIS

The proposed CLI receives Handoff + output + ledger. The ledger contains O# assignments but not the discarded object text.

Therefore C4 cannot detect text from a discarded O# unless the checker also receives the frozen substrate/object table (or an explicit forbidden-text manifest).

Either:
- add `--substrate substrate/acceptance_v2.txt`, or
- replace C4 with a manifest generated upstream.

Do not claim the current arguments can implement C4.

### C5 exact duplicate plan — ACCEPT

Casefold + punctuation + whitespace normalization is deterministic.

### C6 deterministic repeated proposition — NARROW

Remove "same head noun" semantic/linguistic heuristics.

Limit the checker to exact normalized duplicates and clearly defined prefix/subset cases that cannot change meaning.

The O23/O39 MRI hedge is semantically duplicate but not deterministically identical. It is acceptable for the checker to leave that to semantic review rather than pretend to solve it.

### C7 management in factual bullet — REVISE LIKE C3

This needs the same deterministic source-matching algorithm and must not infer semantic equivalence.

### Add a prior-record-plan check

The observed O52 leak is important and mechanically motivated.

If a Plan line maps only to a `MANAGEMENT` entry whose provenance is prior-record [D] and there is no current-encounter MANAGEMENT entry that explicitly re-adopts/continues/restates the same action, fail.

However, the preferred baseline fix is still upstream removal of O52. The checker is a guard, not permission to keep the contradiction.

## Checker scope

P005 can detect contract breaches, but it cannot make three valid outputs identical.

Even after a checker, merge/split choices, evidence selection, and reasoning order may still vary. Therefore a separate **selection/representation hardening proposal** will still be needed if stability remains a product requirement.

## Required next steps

1. Signer confirms which Handoff was used for set2.
2. Correct set2 validation based on that answer.
3. Revise P005 as above.
4. Move already-settled A/P exclusions/relevance upstream (at minimum O52; likely O2) in a separately reviewed ledger/selection change.
5. Then run a clean canonical set with recorded file hashes.

No new clinical/style decision is required. The only signer input currently needed is factual: which Handoff file was attached in set2.
