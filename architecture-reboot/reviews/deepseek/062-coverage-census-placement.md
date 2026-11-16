# DeepSeek adjudication — where the coverage census belongs

**Verdict:** neither Scribe nor a new A stage first.

Put a mandatory **coverage census at the start of B**, in the same B call, then synthesize.

This preserves A’s demonstrated useful function — source-record enumeration before synthesis — without
reintroducing A’s polarity/certainty/selector/state machinery or adding a runtime stage.

## Why not Scribe

Scribe owns source preservation, boundaries and IDs. It should not decide which records are
`current_event`, `baseline_comparator`, `neuro_history`, `exam`, `workup`, etc. Those are clinical/note-function
categories. Putting them in Scribe:

- violates the source-faithful boundary;
- adds a second semantic job to the ingestion surface;
- makes Scribe failures harder to localize.

Scribe may keep its source/section labels. It should not emit clinical coverage categories.

## Why not a new A stage first

A already demonstrated the useful function, but its cost was enormous:

- 81–86 intermediate records;
- polarity/certainty errors;
- pointer drift;
- selector copying;
- action-state leakage.

The evidence supports the **function**, not the old stage. Try the smallest version inside B before adding
runtime decomposition.

## B-internal coverage census

B phase 1:

```text
SOURCE_COVERAGE
  current_event_records=<IDs>
  baseline_comparator_records=<IDs>
  neuro_history_records=<IDs>
  medication_context_records=<IDs>
  exam_records=<IDs>
  workup_records=<IDs>
  action_bearing_records=<IDs>
  context_records=<IDs>
```

Rules:

- record IDs only;
- no selectors;
- no copied text;
- no polarity/certainty/assertion types;
- no action state;
- no problem architecture;
- no note sections;
- categories are navigation only;
- every clinically relevant record should appear in at least one category;
- uncertain category -> `context` or `unresolved`, not omission.

B phase 2: synthesize using the packet + census. B must check that body/action categories are represented
before returning.

## Test

Run B-with-census twice on the same clean packet.

Pass requires:

- every cited ID exists and supports the output;
- no uncited state/wording;
- no-prior-seizure history, family history, meds, exam, workup, actions, baseline comparator preserved;
- problem architecture/stance preserved;
- burden still below A→B, even with census.

If both pass, use B-with-census; retire old A.

If either fails on coverage, build a **minimal coverage A** with the same record-ID-only census; do not
restore old A semantics.

## Do not

- put clinical categories in Scribe;
- restore selectors;
- restore polarity/certainty;
- restore action-state enums;
- add a validator;
- run C.

No acceptance or production change.
