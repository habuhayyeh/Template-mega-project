# ChatGPT review 096 — positive causal branch adoption inconsistency

## Verdict

> **ONE LOCAL SEMANTIC FIX REQUIRED.**

Target: DeepSeek commit `fa0ea68`.

The positive causal Gate-0 branch now correctly tests:

- residual deficit vs historical disease as the acting causal subject;
- POSSIBLE vs LIKELY strength;
- clean positive causal relation vs isolated semantic mutations.

However, its clean S2 parent is internally inconsistent with D-030.

## Defect

Current source span `S05` states:

> Her chronic right-sided weakness from the prior stroke may contribute to the falls.

The clean parent creates object:

- `O02 = chronic right-sided weakness from prior stroke`
- provenance = current encounter;
- causal relation = `O02 -> O03 / CONTRIBUTOR / POSSIBLE / support S05`

but simultaneously records:

```json
{"object":"O02","adoption":false,"evidence":null}
```

That is incompatible with the accepted source-state rule.

The current encounter is explicitly using the chronic residual weakness in its formulation. Therefore
the residual weakness is currently adopted, even though the underlying historical stroke can remain a
background diagnosis and need not itself be newly adopted.

## Required correction

In `S2_CASE10_CAUSAL` and its generated descendants:

```json
{
  "object": "O02",
  "adoption": true,
  "evidence": ["S05"],
  "temporal": "chronic"
}
```

Keep:

- `O01` prior stroke: adoption false unless separately/currently adopted;
- `O03` falls: adoption true from S02;
- clean causal relation unchanged: O02 -> O03 / CONTRIBUTOR / POSSIBLE / S05.

Then regenerate all dependent artifacts/packet ids.

## Why this matters

The current clean positive parent produces an `S2-ADOPT-01` packet whose expected reference is SILENT.
With `O02 adoption:false`, a correct blinded clinician judge should instead flag the artifact.

So this is not editorial; it invalidates the clean semantic calibration branch.

## Scope

Do not change D-030, the causal relation, CASE-01, the predicate definitions, or architecture.

No additional version bump is needed if the current C3 run is superseded and regenerated before any
signer/evaluator evidence exists.

## NEXT

DeepSeek applies the single source-state correction, regenerates the C3 packet set, runs tests +
preflight + packets mode, and returns:

- exact diff;
- new packet ids/count;
- confirmation that the clean CASE-10 S2-ADOPT packet is now semantically SILENT;
- confirmation that G0-S2-09 and G0-S2-10 remain isolated S2-CAUSAL-01 semantic failures.

No signer references until this passes.
No Gate 0 acceptance. No Doximity. No Phase 0.
