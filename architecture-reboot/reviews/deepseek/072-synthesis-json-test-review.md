# Review — real-packet synthesis JSON test

**Verdict:** the old test is not valid for exact determinism. It asks the model to do four jobs at once and
has no gold specification.

## Why the old test is invalid

1. **No gold output.** Three different JSONs cannot be scored as right/wrong without an adjudicated
   reference. The test only shows drift, not which run is correct.
2. **Baseline problem rule is contradictory.** The prompt says baseline/history stays under the relevant
   problem, but also allows `BACKGROUND`. All three runs create `P002` for longstanding staring. The test
   never says whether that is forbidden.
3. **`contains` / `separate_from` are ambiguous.** `contains` allows “problem handles or short labels”;
   `separate_from` allows handles. Runs use unit IDs, event labels and problem IDs interchangeably.
4. **`counterevidence` is undefined.** Diagnostic uncertainty (`T018/T019`) is not counterevidence to the
   problem claim. Runs put it there anyway.
5. **Action coverage is underspecified.** `T001` (consult), `T008` (ship evaluation/testing), `T020`
   (EEG/MRI needed), `T022` (continuation), `T023` (disposition) and `T024` (counseling) are not given a
   required action shape. Runs produce 5, 6 and 7 actions.
6. **Unresolved is underspecified.** Runs produce 0, 2, 3, 4 and 5 unresolved entries. CT result,
   supplements, etiology, EEG/MRI status and disposition appear inconsistently.
7. **Global `order` has no rule.** The model invents a unique order across four arrays. Variation in order
   is not a synthesis failure, but it breaks D-S.
8. **Unit splitting is prose, not a map.** Patient/family, no-prior-ASM/treatment, and workup states are
   merged inconsistently because the prompt does not say which source payloads must be separate.

## Consequence

This test cannot distinguish:

- model drift;
- prompt ambiguity;
- a genuinely wrong clinical decision.

Exact determinism is the wrong target for free semantic synthesis. The valid targets are:

1. **invariants** — problem count/role, unit types, action coverage, unresolved set, containment;
2. **frozen facts JSON** — one adjudicated object used for D-S/D-T;
3. **determinism tests** — run only on the frozen JSON.

## What a valid test must fix

- one problem only; baseline never a separate problem;
- `contains`/`separate_from` empty unless a separate problem exists; handles only;
- `counterevidence` only direct contradiction;
- exact action-bearing record set and one action per record;
- exact unresolved set;
- explicit unit split map;
- explicit order rule based on source record order.

## Not the fix

More prose warnings in the same all-in-one prompt. That is what produced the ambiguity.
