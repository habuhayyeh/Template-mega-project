# DeepSeek review — unified source-local A contract

**Reviewed:** `01-SOURCE-LOCAL-INGESTION.md`, report `3b88d5c`.
**Status:** architecture review; no implementation.

## Verdict

**ACCEPT.** This is the right synthesis of the architect lanes and the A1/A2 failure evidence.

It keeps A source-local, removes cross-record reconciliation, and makes source-pointer fidelity
mechanically checkable. It also preserves C as the blueprint owner and does not add a mandatory episode
model.

## What is right

- one A pass with A1 semantic and A2 action lanes;
- A0 is the Scribe packet, not a second registry;
- exact `source_record`;
- literal selector from that record;
- no adjacent-record synthesis;
- no cross-record relations;
- no global SPK mapping;
- action state fields separate and source-local;
- unknown fields absent;
- `not on file` never becomes negative;
- coverage floor includes exam, meds, history, workup, safety and reasoning;
- no problem/section/prose decisions;
- no semantic validator.

## One clarification before the run

Define selector matching precisely:

- the selector must be an **exact contiguous substring** of the cited record;
- no ellipsis, paraphrase, merged turns, normalized wording or invented punctuation;
- preserve source whitespace/punctuation inside the selector;
- if a quote character is normalized, the lint must use the same normalization rule.

Otherwise the mechanical invariant will produce false failures or, worse, accept a paraphrased selector.

## One risk

The inclusion rule is still a preservation judgment. “If uncertain, include” helps, but the model can
still omit exam/safety material. The coverage floor is the right control; run it against the predeclared
oracle.

## Test

1. Run A alone on the frozen packet.
2. Lint:
   - every `source_record` exists;
   - every selector is an exact substring of that record;
   - no selector spans adjacent records;
   - action fields use allowed values;
   - unknown fields absent.
3. Score coverage against the existing oracle.
4. Inspect A1 and A2 separately.
5. Do not run B/C until A alone passes.

No acceptance, production change or Phase 0.
