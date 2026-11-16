# DeepSeek review — gating patch and comparator result

## Gating patch

**ACCEPTED.**

The READ → EXTRACT → DECIDE → CHECK → EMIT gate, output lock, controller gate and final gate are consistent
with the contracts.

No semantic responsibility changes.

One nuance, not a blocker: the controller keeps intermediate handoffs internal until both stages finish,
but the A→B experiment legitimately returns both handoffs. The controller’s final gate explicitly requires
both, so the return package is correct.

## Comparator result

**ACCEPTED.**

INCONCLUSIVE is the correct verdict:

- both arms have pointer failures;
- direct-B has a blocking body/nonproblem coverage loss;
- A preserves body evidence but does not improve pointer fidelity;
- direct-B has a large burden advantage;
- different material failures mean no averaging.

A is not retired. Direct-B is not accepted yet.

## Follow-up

**BUILD DIRECT-B CLINICAL_UNIT FOLLOW-UP.**

The blocking question is:

> Can direct-B preserve clinically necessary nonproblem/body evidence without recreating A?

Use compact B `CLINICAL_UNIT`s, not a source-span ledger:

```text
CLINICAL_UNIT U001
  kind=current_event | baseline_comparator | neuro_history | medication_context |
       exam | workup | context
  label=<short>
  source_record=<exact>
  selector=<exact contiguous>
  chronology=<only when needed>
  relation_to_problem=<P handle or none>
```

Rules:

- no polarity/certainty registry;
- no exhaustive source-span ledger;
- no per-utterance atomicization;
- no final-note section decisions;
- no new stage/validator;
- every unit exact source record + exact selector;
- body/nonproblem coverage tested against the target note;
- pointer fidelity tested against the Scribe packet.

Run extended direct-B twice on the same clean packet.

Pass requires:

- required body evidence preserved;
- no more pointer errors than the A→B runs;
- action concepts preserved;
- problem architecture/stance preserved;
- burden still materially lower than A→B.

If pass, retire A. If fail, identify the exact preservation function A uniquely supplies.

Do not run C. Do not rebuild A.

No acceptance or production change.
