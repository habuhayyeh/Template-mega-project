# Stress-suite architecture review — original architecture branch

## Verdict

**The B+ operator boundary survives adversarial testing.**

Across 36 trials × 3 fresh conversations:

- 63/63 valid renders were correct;
- 45/45 malformed inputs were rejected;
- 108/108 trials respected the valid/invalid boundary;
- valid outputs were stable across all three fresh runs;
- no malformed input was silently repaired into clinical prose.

The remaining defect is primarily the error taxonomy.

## What should change in P006

1. Keep canonical render operators.
2. Make required operator payload fields explicit.
3. Fail closed on malformed/under-specified groups.
4. Do not ask 05 to repair group defects.
5. Do not over-engineer diagnostic error labels.

### Error taxonomy

T2, T10, T24 and T32 were rejected correctly but received a different plausible error code from the preferred answer key.

T34 varied between two labels that the answer key itself considered acceptable.

Therefore exact error-label agreement is not the important production invariant.

The important invariant is:

> invalid semantic structure never reaches prose rendering.

If a detailed taxonomy is retained, add deterministic precedence or dedicated codes for object reuse/group accounting.

Otherwise simplify production failure to a generic `CONTRACT_ERROR` and reserve detailed diagnosis for a separate validation/audit artifact.

## Important evidence distinction

This result is materially different from the earlier natural-language runs.

The malformed cases did not trigger helpful clinical improvisation.

That is strong evidence that an explicit typed operator contract can create a useful execution boundary inside Doximity even without Python execution.

## Next

P006 should be revised around the accumulated gradient + B+ + stress-suite evidence, then the next meaningful test should be the actual canonical seizure case, not another synthetic challenge.
