# DeepSeek review — architect decisions 003/004/005

**Verdict:** the direction is right. Decision 005 is the one to follow: patch B threshold and
relationships, quarantine A polarity, freeze B, then C.

Three interface gaps remain, and one prompt is stale.

## What is right

- P002 should collapse into P001 as comparator evidence.
- The counterfactual independence test is a good B threshold.
- B must emit explicit item-to-problem roles: evidence, counterevidence, comparator, context, plan.
- C should not infer support/opposition or action ownership.
- Closed operator set is the right C constraint.
- Blueprint before prose; renderer lexicalizes only.
- B relationship correctness is the biggest risk.

## Gap 1 — polarity quarantine starts too late

Decision 005 removes `polarity` from the B->C interface. But B still receives A polarity. If B uses the
bad field to assign evidence/counterevidence, C faithfully preserves a wrong B.

Quarantine must start at A->B:

- either remove `polarity` from B’s consumable input;
- or state that A polarity is non-operative telemetry and B must derive direction from the selector and
  assertion wording.

Do not wait until B->C. The damage is already done in B.

Also update the “mixed polarity” A representation to `MIXED`/`UNSPECIFIED`, not `affirmed`/`negated`, if
the field remains.

## Gap 2 — C include/omit lacks B disposition for nonproblem content

Decision 004 says C may include/omit according to B’s disposition. But B has no disposition field for
nonproblem exam, meds, history, workup, or safety content.

Without that, C must decide clinical relevance to include/omit nonproblem material. That is the clinical
judgment C is forbidden to make.

Smallest fix: B emits a disposition for every note-relevant nonproblem item:

```text
LINK S040 -> nonproblem role=context
LINK S041 -> nonproblem role=body_material
LINK S042 -> nonproblem role=omit reason=redundant
```

or an explicit `ITEM_DISPOSITION`. C then includes/omits only by B disposition.

## Gap 3 — no gate for B relationship correctness

The 005 rules are good, but the gates test problem identity, not whether B labeled evidence,
counterevidence, comparator and context correctly.

Because C preserves B faithfully, a wrong B relationship passes C.

Add a small B relationship fixture:

1. normal exam does not become counterevidence to a seizure-like event syndrome;
2. absence of limb convulsions characterizes semiology, not counterevidence to epilepsy in general;
3. baseline spells -> comparator, not problem;
4. outside normal labs -> context/evidence, not counterevidence;
5. clinician reasoning stays in diagnostic_stance, not duplicated as counterevidence.

Gate B on those before freezing.

## Gap 4 — C gate does not protect counterevidence

`problem IDs`, class and claim equality are not enough. C could omit B counterevidence through
`INCLUDE/OMIT` or `COMPRESS`.

Add:

- every B counterevidence item appears in C or has an explicit B-authorized omit;
- every C `LINK` role matches a B role;
- no C-created comparator/context.

## Gap 5 — prompt 002 is stale

`architect/prompts/002-challenge-next-step.md` still says:

- defer A polarity;
- patch A only if C produces an inversion.

That was decision 003. Decisions 004/005 changed to quarantine. If the expert receives prompt 002, he will
review the wrong decision.

Update the prompt to 005:

- B threshold + relationship contract first;
- quarantine polarity before B;
- no C until B frozen;
- C no-new-meaning gate;
- render last.

## Minor

- `problem IDs(C) == problem IDs(B)` is good, but normalize ID spaces before comparison.
- `INCLUDE/OMIT` needs a reason field; omission without a B-authorized reason is a gate failure.
- Renderer may reread packet for exact wording; gate that it cannot add content not in blueprint.

## Recommendation

Adopt 005 with these corrections:

1. quarantine A polarity at A->B, not only B->C;
2. B disposition for nonproblem content;
3. B relationship fixture before freeze;
4. C counterevidence/omission gate;
5. update prompt 002 to 005.

Then patch B, freeze, run C.

No new stage, no enum, no validator. No acceptance or production change.
