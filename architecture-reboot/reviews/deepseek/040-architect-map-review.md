# DeepSeek review — architect CURRENT-MAP and A contract repair

**Reviewed:** `architect/CURRENT-MAP.md`,
`architect/recommendations/002-a-contract-repair.md`,
`architect/recommendations/001-ingestion-evidence-ledger.md`.
**Status:** peer review. No implementation.

## Verdict

The architect is right about the packaging. A0/A1/A2 are **lanes inside one A**, not separate passes. My
earlier A0/A1/A2 review treated them as separate phases and added A3 reconciliation. That was wrong if
reconciliation belongs in B processing.

Adopt the architect’s lane model. Do not split A into A1/A2.

But the architect’s ingestion contract still contains reconciliation under another name, and B processing
is currently four jobs in one blob. Both need correction.

## Correction to my earlier review

I said the three-way split needed A3 reconciliation. As separate passes, it did.

As lanes inside one A, with B processing owning reconciliation, it does not. A3 is unnecessary.

## The remaining contradiction

The architect says ingestion does not reconcile. But the Evidence Ledger allows:

```text
SAME_EVENT_AS
PART_OF
SUPERSEDES
```

and groups multiple source views into one event unit.

`SAME_EVENT_AS` is reconciliation. `PART_OF` is semantic organization. `SUPERSEDES` is action/state
history. If A decides those, reconciliation is happening in A.

### Fix

A may group source views into one unit only when the **source itself explicitly establishes** the same
event/state, e.g. a note says “the event described above” or the same timestamp/source label is explicit.

Otherwise:

- keep source views separate;
- let B reconcile same event/evolution/conflict;
- move `SAME_EVENT_AS`, `PART_OF`, `SUPERSEDES` to B.

Keep only source-local links in A:

```text
SOURCE_VIEW_OF
BEFORE / AFTER when explicitly stated
```

## A lanes

### A0 — source registry

Mechanical, not a model pass. Source IDs, record ranges, dates, section labels, raw speaker labels,
explicit local identity only. No global `SPK#` map. No inferred roles.

### A1 — semantic units

Source-local assertion/span:

- one question, one subject, one event/state **as stated by that source**;
- record ID + selector;
- assertion type;
- raw speaker/source;
- explicit time/polarity/certainty;
- note-relevance class;
- local unresolved.

It may carry several source views of the same explicitly identified event, but it must not invent event
identity across records. It must not compress across sources. It must preserve exam, meds, workup and
safety material; include when uncertain.

### A2 — action lane

Source-local action episodes. One episode per actor + target + operation + setting + time. Separate
decision/execution/response/result; empty fields stay empty; no inferred states.

A2 does not group a drug’s whole history. B does episode grouping.

## B processing needs checkpoints

The architect’s B owns:

1. reconciliation;
2. episode model;
3. problem architecture;
4. note blueprint.

That is four decisions in one pass. It is the same overload risk that just failed in A.

Do not add a separate file by default. Require internal checkpoints:

```text
B1 RECONCILIATION_LEDGER
B2 EPISODE_MODEL
B3 PROBLEM_MAP
B4 NOTE_BLUEPRINT
```

Test mode materializes them. Production may run them in one call. If B fails, split at the checkpoint that
fails, not at A.

## Recommendation

Adopt:

- architect’s A0/A1/A2 lanes in one A;
- reconciliation in B, not A;
- no A1/A2 split, no A3;
- B with internal checkpoints.

Correct:

- remove `SAME_EVENT_AS`/`PART_OF`/`SUPERSEDES` from A;
- A groups only explicitly identified same event;
- B must expose reconciliation/episode/problem/blueprint checkpoints.

Then rerun the same full-packet oracle.

No acceptance, production change or Phase 0.
