# Review 143 — A2 asserted-state isolated run

## Verdict

**FAIL — asserted-state representation does not prevent action-state invention.**

The returned `A2_ASSERTED_STATE_V1` handoff is a valid experimental output for the asserted-state arm.

The accompanying `A2_CURRENT_SLOT_V1` block is **not** a valid control run. Doximity explicitly states that the canonical `SCRIBE_EVIDENCE_V2_2` packet was not provided and that it translated the asserted-state handoff into the current-slot schema. Therefore it cannot be used as the independent current-schema condition.

The asserted-state arm alone is sufficient to reject the candidate fix as currently specified because it contains multiple fatal action-state promotions.

## Decisive finding

The asserted-state representation changed the failure form, not the failure mechanism.

Requiring:

```text
ASSERTED_STATE field=<...> value=<...> phrase=<exact phrase>
```

does ensure that the model supplies a lexical anchor.

It does **not** ensure that the lexical anchor semantically entails the chosen state.

The model can still attach an incorrect state to an exact phrase.

## Fatal action-state promotions

### A007 — EEG

Selector/action phrase:

```text
need EEG
```

Output:

```text
ASSERTED_STATE field=decision value=recommended phrase=need EEG
ASSERTED_STATE field=execution value=not_started phrase=need EEG
```

`need EEG` does not explicitly state an execution state. `execution=not_started` is invented.

### A009 — continue Keppra

Selector:

```text
will keep on Keppra for now
```

Output:

```text
ASSERTED_STATE field=decision value=continue phrase=will keep on Keppra for now
ASSERTED_STATE field=execution value=reported_performed phrase=keep on Keppra
```

The continue decision is supported.

`reported_performed` is not. The phrase does not establish a source-mediated administration event; it expresses continuation.

### A010 — MRI plan

Selector:

```text
plan MRI either tonight or tomorrow
```

Output:

```text
ASSERTED_STATE field=decision value=planned phrase=plan MRI
ASSERTED_STATE field=execution value=not_started phrase=plan MRI
```

The plan is supported. The execution state is not.

### A014 — ED CT/labs/UA plan

Selector begins:

```text
Plan: CT head without contrast, basic labs, urinalysis
```

Output includes:

```text
ASSERTED_STATE field=decision value=planned phrase=Plan: CT head without contrast
ASSERTED_STATE field=execution value=ordered phrase=Plan
```

This directly violates the accepted invariant `plan != ordered`.

The exact supporting phrase requirement did not prevent the model from mapping the word `Plan` to `execution=ordered`.

### A018 — Keppra load shorthand

Selector:

```text
Neuro: Keppra load 1500; will come evaluate.
```

Output:

```text
ASSERTED_STATE field=decision value=recommended phrase=Keppra load 1500
ASSERTED_STATE field=execution value=ordered phrase=Keppra load 1500
```

The same phrase is used to justify two different state dimensions. The source shorthand does not explicitly distinguish recommendation from order. Under the accepted A contract, ambiguous state should remain absent/unresolved rather than being forced.

This is a material action-state promotion.

## Action identity / splitting failures

The isolated A2 arm also violates the one-action-per-source-local-action rule.

Examples:

- A004 groups blood tests, urine tests, and monitoring in one action span.
- A005 groups EKG and urine testing in one action span.
- A014 groups CT head, basic labs, and urinalysis in one action span.

The module explicitly required splitting materially distinct action targets.

Therefore the A2 failure is not limited to state-slot completion.

## Additional source-local drift

Several fields suggest local semantic inference beyond the exact record:

- A001 says `setting on cruise ship medical implied by prior turn`, which explicitly relies on adjacent-turn context rather than the cited record alone.
- `provenance=deemed necessary` and `provenance=said everything was fine` use claim/action wording as provenance rather than nested source attribution.

These are secondary to the fatal state errors but reinforce that source-local typing remains unstable.

## Invalid current-slot control

The appended current-slot output must not be scored as the control condition.

Doximity states:

> No SCRIBE_EVIDENCE_V2_2 packet was provided ... Above is a schema translation of your 19 spans into A2_CURRENT_SLOT_V1 format.

Therefore:
- it did not independently inspect the frozen packet;
- it inherited the asserted-state arm's selected actions and semantic decisions;
- any apparent similarity between the two outputs is expected and non-independent.

## Experiment interpretation

The predeclared interpretation was:

- current FAIL + asserted PASS -> asserted-state representation supported;
- both FAIL -> representation insufficient;
- both PASS alone + unified A FAIL -> lane interference.

The asserted arm already **fails fatally**.

Therefore the candidate asserted-state fix is rejected in its current form regardless of how the independent current-slot control would perform.

A clean current-slot run could still help causal attribution, but it is no longer necessary to decide whether this asserted-state representation should replace active A2: it should not.

## Architectural implication

Do not patch active A with asserted-state triples.

The new evidence narrows the failure:

> The problem is not merely empty slots inviting completion. GPT-4o can satisfy an exact-phrase constraint while still assigning an unsupported semantic state to that phrase.

So a mechanical phrase-substring invariant is insufficient for semantic state fidelity.

The next architecture question belongs to DeepSeek under D-047:

1. Is typed action-state extraction itself too semantically brittle for this model at this stage?
2. Should A preserve source-local action wording without assigning normalized state enums, leaving state interpretation to B1?
3. Or is there another representation that makes semantic state promotion materially harder without adding a same-model validator?

Do not add another prose-only warning.
Do not advance to B/C.
Do not adopt asserted-state A2.
Do not treat the translated current-slot block as experiment evidence.

No acceptance. No production change. No Phase 0.
