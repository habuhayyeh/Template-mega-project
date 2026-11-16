# Decision 005 — patch B relationships before C

**Status:** architect decision. Amends decision 004. No C run yet.

## Decision

Accept the expert review.

Do not run C on the current B output. B fails the new threshold and has relationship-label errors
that C is forbidden to repair.

Order:

1. Patch B problem threshold.
2. Patch B relationship contract.
3. Quarantine A polarity from the B->C interface.
4. Freeze B.
5. Run C.
6. Gate C.
7. Render.

## 1. B problem threshold

P002 (baseline staring spells) should not be a separate problem.

- baseline spells have no independent disease identity in this encounter;
- they are used to distinguish the current events;
- they belong inside P001 as comparator evidence.

Required B change:

```text
DELETE P002 as a problem.
LINK baseline spans -> P001 role=comparator
```

Do not create a special “baseline phenomenon” category. The rule is the counterfactual independence
test from decision 004.

## 2. B relationship contract

B must emit explicit item-to-problem relationships, not parallel evidence buckets.

Allowed roles:

```text
evidence
counterevidence
comparator
context
plan
```

Conceptually:

```text
LINK S005 -> P001 role=evidence
LINK S023 -> P001 role=comparator
LINK S035 -> P001 role=context
```

Rules:

1. Evidence direction is relative to the **adopted problem claim**, not to an unstated disease
   hypothesis.
2. Do not label a finding `counterevidence` merely because it is atypical for one possible diagnosis.
3. Normal current exam, unrevealing labs, or no prior ASM are not automatically counterevidence to a
   seizure-like event syndrome.
4. Absence of limb convulsions characterizes semiology; it does not by itself oppose epilepsy in
   general.
5. Clinician diagnostic reasoning belongs in `diagnostic_stance`; it should not be duplicated as raw
   counterevidence.
6. A span may be left unlinked if no relationship is supported. Do not force every span into a link.
7. If a relationship requires assuming an unstated diagnosis, use `evidence`, `context` or `comparator`
   rather than `counterevidence`.

For the current primary problem, the explicit counterevidence set may legitimately be empty.

## 3. A polarity quarantine

Do not patch the full A polarity model.

Remove `polarity` from the **B->C consumable interface**. C should not receive a field it must ignore.

A may keep the field for telemetry. Mixed assertions may remain imperfect in A; the selector and typed
assertion remain usable.

This is interface minimization, not a new stage.

## 4. Freeze B

After the two B patches:

- P002 is gone;
- baseline spans are comparator links under P001;
- every retained link has an authorized role;
- no unjustified counterevidence;
- action lane unchanged;
- diagnostic stance retains its provenance.

Freeze that B output. Do not micro-tune B during C.

## 5. C gate

C must preserve:

- exactly one B problem remains exactly one problem;
- baseline spans remain comparator, never a problem;
- diagnostic stance unchanged;
- context not reclassified as counterevidence;
- action owners unchanged;
- no polarity-derived semantic transformation;
- no new problem, role, causality, certainty, currentness or action state.

C may only place, order, link to an authorized role, repeat, group, compress or cross-reference.

## 6. Biggest risk

B assigns clinically plausible but incorrect relationships, and a properly constrained C faithfully
preserves them.

This is now a larger risk than C inventing problems.

Smallest mitigation:

> A relationship label must describe the item’s function relative to the actual adopted problem claim.
> If it requires assuming an unstated diagnosis, do not use `counterevidence`.

## 7. Delete/defer

Do not:

- patch the full A polarity model;
- add another B category;
- add a special baseline problem type;
- let C decide comparator/counterevidence/ownership;
- add a repair operator;
- add a validator or stage.

Defer:

- full A polarity redesign;
- render until C passes.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
