# DeepSeek review — architect lanes vs A1/A2 split

**Scope:** `architect/CURRENT-MAP.md`, `architect/recommendations/002-a-contract-repair.md`,
review 141, and the first combined A1/A2 run.
**Status:** peer architecture review. No implementation.

## Verdict

The architect’s A0/A1/A2 are **lanes inside one A**, not separate stages. I was wrong to treat them as
separate passes and add A3.

The A1/A2 split and the architect’s lanes are the **same separation packaged differently**:

- source-local preservation;
- action episodes;
- reconciliation.

The combined A1/A2 run failed, but it failed because the contracts were not strict enough, not because the
separation is wrong. The architect’s packaging is the better production shape; the split is still useful
for development testing.

## What the run actually proves

A1:
- improved exam/safety/differential coverage;
- kept action episodes source-local;
- still synthesized adjacent records under one pointer;
- still missed family history and seizure precautions;
- still bundled multi-action records.

A2:
- used a question as support for a negative;
- invented speaker identities A1 did not provide;
- added execution/result states absent from A1;
- invented a Keppra episode from mismatched spans;
- had invalid disposition accounting.

This is a **contract/isolation failure**, not proof that source-local preservation + reconciliation is the
wrong boundary.

## Adopted production shape

```text
Scribe V2.2
  -> A INGESTION (one pass, three lanes)
       A0 SOURCE_REGISTRY (mechanical/local)
       A1 SEMANTIC_SPANS (source-local)
       A2 ACTION_SPANS (source-local episodes)
  -> B CLINICAL SYNTHESIS
       B1 RECONCILIATION_LEDGER
       B2 PROBLEM_MAP + DIAGNOSTIC_STANCE
  -> C NOTE COMPILER
       NOTE_BLUEPRINT
  -> RENDER
```

No A3. No A1/A2 split in production. Test A1/A2 separately in development to prove the boundaries.

## Correction to the architect

The architect’s ingestion ledger still allows:

```text
SAME_EVENT_AS
PART_OF
SUPERSEDES
```

Those are reconciliation decisions. A may only group source views when the packet itself explicitly
establishes the same event/state. Move the relations to B1. Keep only `SOURCE_VIEW_OF` and explicit
`BEFORE`/`AFTER` in A.

## Correction to ChatGPT

B should not own `NOTE_BLUEPRINT`. That is C’s job, and it is a large allocation decision.

Keep:

- B1 reconciliation;
- B2 problem architecture + diagnostic stance;
- C blueprint;
- render.

Do not make `EPISODE_MODEL` a mandatory checkpoint. Put episode structure inside B1 when the case needs
it; promote it only if a later run shows it fails independently.

## What must be fixed before another run

A1:

1. `source_record=<exact ID>` mandatory;
2. `selector=<literal substring from that one record>`;
3. no span may combine text from adjacent records;
4. split multi-action/multi-assertion records when downstream handling differs;
5. preserve source wording + unresolved when action state is ambiguous;
6. coverage floor for current neuro exam, safety actions, patient/family seizure history, workup state;
7. mechanical selector-to-record lint in development.

A2/B1:

1. attribution only from A1 tokens;
2. every action state must cite an A1 span with that exact state;
3. question spans never support statements;
4. no rereading source to repair A1;
5. disposition must point to a unit that actually contains the span;
6. no cross-setting action episode.

## Next experiment

1. Patch A1 only.
2. Run A1 alone on the frozen packet.
3. Validate pointer/selector fidelity, coverage and span locality.
4. Freeze that A1 artifact.
5. Run A2/B1 on the frozen artifact.
6. Only then touch B2/C.

No combined A1/A2 run until A1 alone passes.

No acceptance, production change or Phase 0.
