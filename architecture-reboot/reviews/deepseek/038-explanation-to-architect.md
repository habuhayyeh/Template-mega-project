# Explanation to the architect — what we are building

**To:** the architect who proposed the Evidence Ledger ingestion model
**Purpose:** explain the current build and the difference from that proposal. Not a step instruction.

## What we are building

A source-faithful neurology note pipeline on Doximity:

```text
Scribe V2.2 packet
  -> A Interpret / Reconcile
  -> B Problem Architecture
  -> C Note Compiler
  -> Render
  -> final note
```

One Ask invocation with logical phases. Test mode may materialize A/B/C artifacts; production may return
the note only.

### Scribe

Canonical evidence store. Source boundaries, record IDs, order, speaker labels, section labels,
provenance, uncertainty markers. Nothing downstream may rewrite it.

### A — Interpret / Reconcile

Owns what the source actually supports:

- assertion type;
- referent and event identity;
- attribution;
- source time vs event time;
- current/historical source scope;
- polarity and certainty;
- duplicate/evolution/conflict;
- action decision/execution/response/result;
- unresolved.

Output: sparse decision ledger + action lane + unresolved register. Every entry cites record IDs,
selectors and roles.

A does **not** decide problems, roles, sections, plan ownership or prose.

### B — Problem Architecture

Owns:

- encounter-level problem threshold;
- independent problem identity;
- containment;
- disease vs syndrome;
- distinct downstream disorder;
- multifactorial syndrome;
- PRIMARY/BACKGROUND;
- supported causal/contributory relations;
- diagnostic stance/evidence weighting (to be added explicitly);
- action ownership.

Output: encounter-relevant problem map + architecture unresolved. Historical disease that matters only as
history stays in A/C, not B.

### C — Note Compiler

Owns:

- section allocation;
- HPI chronology;
- neuro history;
- other PMH;
- medication-at-presentation;
- current exam;
- workup/result state;
- A/P composition;
- minimum-sufficient evidence and counterevidence;
- shared-action home;
- blueprint unresolved.

Output: note blueprint. No prose.

### Render

Owns wording, compression, grammar, formatting. No clinical decisions.

## Why this shape

We tried and rejected:

- atomic facts: exploded to ~175 objects and truncated;
- synthesized F1 facts + validator: the validator false-passed because it was the same model checking its
  own claims;
- pointer-only index: removed the claim layer, but GPT-4o produced coarse source-wide buckets.

The current shape keeps one source of truth, one semantic reconciliation layer, one problem layer, one
blueprint, and a dumb renderer.

## Difference from the Evidence Ledger proposal

Your proposal splits ingestion from processing:

```text
Scribe -> Evidence Ledger (E/H/O/R/F/A/C/Q, source views) -> Processing (reconciliation -> problems -> blueprint) -> Render
```

Ours keeps A as a single semantic reconciliation layer:

```text
Scribe -> A (reconciliation + action lane) -> B problems -> C blueprint -> Render
```

### Why we did not split ingestion out

1. **Scribe already does source preservation.** It gives boundaries, IDs, order, speaker labels, section
   labels and provenance. A separate LLM ingestion layer would largely re-index what Scribe already
   provides.
2. **Reconciliation is the hard part, not extraction.** The failures we saw were wrong event identity,
   question-as-answer, attribution drift and action-state promotion. Splitting extraction from
   reconciliation adds a handoff without removing that difficulty.
3. **The Evidence Ledger still contains reconciliation decisions.** `SAME_EVENT_AS`, `PART_OF` and
   `SUPERSEDES` are not source-local. If ingestion makes them, it is doing processing under another name.
4. **Source views can become another corpus.** “Short source-grounded fragment” is a paraphrase surface.
   We already paid for that with synthesized F1 facts.
5. **Fewer handoffs matter for GPT-4o.** A’s ledger is already sparse; adding an ingestion ledger plus a
   processing pass risks more drift, not less.

### What we adopt from your proposal

- no synthesized fact prose;
- source record IDs and selectors;
- questions are not facts;
- action state kept separate;
- no problem/section/role decisions at ingestion;
- cap the ledger, do not reproduce the packet;
- allow `UNRESOLVED` instead of completing the story.

### What we reject for now

- `CORE` as a summary; at most a noun-phrase label;
- `SAME_EVENT_AS` / `PART_OF` / `SUPERSEDES` at ingestion;
- a separate ingestion pass before reconciliation;
- 15–25 record compression as a fixed target;
- a processing pass that bundles reconciliation, problems and blueprint.

## Difference from the 8-pass expert proposal

The expert proposed atomic facts, a separate action pass, section packets, a compression pass and a final
audit. Ours removes the atomic fact corpus, keeps action state as a lane, makes the blueprint explicit,
and removes the same-model audit.

## Current gate — A full-packet result

We ran A on the full frozen Scribe packet and scored it against the predeclared oracle.

It did **not** fail at scale:

- completed through `@@END`;
- 16 units, 7 actions, 6 unresolved;
- 18,950 bytes vs 34,700-byte packet;
- no truncation, no atomic explosion;
- Wednesday and Thursday events stayed distinct;
- future workup did not become results.

It failed **semantically**: 39 pass, 9 fail, 3 N/A. Fatal failures were:

1. speaker attribution inversion — SPK3 (mother) reported as patient recall;
2. action-state normalization — planned CT/labs labeled `ordered`; reported Keppra drip labeled
   `decision=ordered`; cross-time Keppra mentions merged into one action; admission recommendation given
   inferred `execution=pending`.

Other failures: patient and family seizure history collapsed; `not on file` turned into a denial; mixed
diagnosis + management assertion; missing ED differential and current continue-Keppra action.

Interpretation: **field-contract weakness inside a scalable A**, not task overload or packet-size
failure. Patch A’s local semantics once before splitting A1/A2. The Evidence Ledger is not justified by
this run.

## What we want from you

Critique the single-A choice specifically:

- Is one reconciliation pass too much for GPT-4o on a full packet?
- Would splitting A1/A2 remove a real failure mode, or just add a handoff?
- Is there a material distinction our A schema cannot preserve that the Evidence Ledger would?

We are not looking for another full architecture. We are looking for the smallest correction if the scale
test fails.
