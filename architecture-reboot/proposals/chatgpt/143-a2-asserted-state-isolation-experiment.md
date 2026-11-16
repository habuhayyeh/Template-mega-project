# Proposal 143 — A2 action-lane asserted-state isolation experiment

**Status:** bounded experimental proposal for peer review  
**Scope:** A2 representation only  
**Does not change:** active unified A, B, C, production topology, oracle semantics

## Evidence

Review 142 showed that the accepted unified A contract completes at scale but GPT-4o still fills unsupported action-state slots despite explicit rules to omit them.

DeepSeek review 043 classifies this as **schema completion inside A2**, not a missing prose rule, and proposes an asserted-state representation.

## Question

Is the four-slot action representation itself causing GPT-4o to invent unsupported state fields?

## Experiment

Run two A2-only tests on the identical frozen `SCRIBE_EVIDENCE_V2_2` packet in fresh Ask sessions:

1. **Current-schema condition**
   - `01A-ACTION-LANE-CURRENT-SCHEMA-TEST.md`
   - preserves the current `decision/execution/response/result` representation.

2. **Asserted-state condition**
   - `01B-ACTION-LANE-ASSERTED-STATE-TEST.md`
   - replaces optional state slots with zero-or-more `ASSERTED_STATE` triples.

All other action-lane responsibilities are held as constant as possible.

## Asserted-state representation

Each action span carries source-local identity plus:

```text
ASSERTED_STATE field=<decision|execution|response|result> value=<allowed value> phrase=<exact supporting substring of selector>
```

Rules:
- no state line exists unless a source phrase explicitly supports it;
- every state line must include exact supporting `phrase`;
- `phrase` must be a contiguous substring of `selector`;
- absence is represented by no state line, not `unavailable`, `not_started`, or another filler value;
- action identity may still be preserved when exact state is ambiguous, with `unresolved`.

## Controlled comparison

Score both outputs only against `A2-ACTION-STATE-ORACLE.md`, which is a frozen subset/operationalization of the existing A full-packet oracle and accepted A contract.

Interpretation:
- current fails + asserted passes -> schema-completion hypothesis supported; asserted-state becomes candidate A2 representation;
- both fail -> representation remains insufficient; simplify further;
- both pass alone while unified A fails -> same-pass lane interference becomes the leading explanation.

## Mechanical checks

For asserted-state output:
- every source record exists;
- selector is exact contiguous substring of that record;
- every asserted-state phrase is exact contiguous substring of selector;
- no empty state fields;
- no state value without phrase;
- no semantic/non-action lane is emitted.

## Boundary

This experiment does not:
- change B/C;
- add reconciliation;
- decide problem identity;
- change the production call count;
- modify the active `01-SOURCE-LOCAL-INGESTION.md` before evidence.

No Gate-0 acceptance. No production change.
