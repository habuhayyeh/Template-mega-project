# DeepSeek architecture verdict — minimum ingestion and runtime

**Status:** architecture verdict. No implementation.

## Verdict

Remove the semantic F1 pointer index.

Scribe V2.2 already provides source boundaries, stable record IDs, source order, speaker labels, section
labels and provenance. A separate LLM stage that groups those records by topic is not ingestion. It is a
semantic routing decision that adds bias, a handoff and a failure surface without reducing the text the
next semantic pass must read.

The pointer-only run proved the claim layer can be removed. It also showed that GPT-4o produces coarse,
source-wide buckets. That is enough evidence that F1 is not earning its place.

Minimum runtime:

```text
Scribe V2.2 packet
  -> F1 semantic reconciliation + action state
  -> F2 problem architecture
  -> F3 note compiler
  -> F4 renderer
```

Four passes. No F1V. No F7 audit. No atomic-fact corpus. No topic index.

If the packet is too large for one reconciliation pass, split **action state** into its own pass before
adding any navigation layer:

```text
Scribe -> reconciliation -> action state -> problem architecture -> compiler -> renderer
```

## What the system is fundamentally trying to accomplish

Turn a source-faithful encounter packet into a neurologically correct note without inventing, upgrading,
decontextualizing or losing clinically material information.

The hard part is not extracting more facts. It is preserving the distinctions that change the note:

- current vs historical;
- disease identity vs current status;
- patient report vs objective finding;
- diagnosis vs evidence;
- problem vs manifestation;
- contained manifestation vs distinct disorder;
- PRIMARY vs BACKGROUND;
- certainty and negation;
- action decision vs execution;
- test performed vs result available;
- attribution and counterevidence.

## Which transformations are actually necessary

1. **Scribe source preservation** — required.
2. **Semantic reconciliation and action state** — required.
3. **Problem architecture** — required.
4. **Note compilation** — required.
5. **Rendering** — required.

Everything else is optional and must earn its cost. Topic indexing, atomic fact extraction, semantic
validation and final audit do not.

## Q1 — Is F1 needed at all?

No, not as a semantic topic index.

The Scribe packet is already an index in the useful sense:
- source blocks;
- ordered record IDs;
- speaker/source labels;
- section labels;
- dates and provenance;
- full text available for dereference.

A second index does not add evidence. It adds a model's interpretation of which records belong together.
That interpretation can be wrong, coarse or biased, and downstream must still read the original records.

If navigation metadata is needed, make it **mechanical**:
- source ID;
- record range;
- date/author;
- section labels;
- counts.

That is not a separate semantic function. It can be generated from the packet.

## Q2 — If F1 exists, what is its purpose?

Only a mechanical source map:
- sources and record ranges;
- dates/authors;
- section labels;
- record counts;
- no topic grouping;
- no claims;
- no compression.

Do not give an LLM a semantic routing job at ingestion. That job belongs to reconciliation/problem
architecture, where the model is already reasoning about the clinical meaning.

## Q3 — Should F1 make cross-source semantic grouping decisions?

No.

Cross-source grouping is reconciliation. It requires deciding that two records concern the same disease,
event, finding or trajectory. That is exactly the semantic work that belongs in the reconciliation pass.
Moving it earlier:
- hides the decision in a label;
- creates coarse buckets;
- biases downstream problem identity;
- makes errors harder to audit.

If cross-source grouping is useful, do it inside reconciliation and cite the source records explicitly.

## Q4 — Preserve or dissolve source boundaries?

Preserve source identity as a first-class axis.

Do not dissolve the ED note, transcript, prior note and collateral report into topic buckets. Source
identity is part of the evidence: who said it, when, in what document, and with what provenance.

Topic grouping can be a view inside reconciliation, but it must not replace source identity.

## Q5 — What happens to provenance/source identity?

It stays in the Scribe packet and flows through every semantic handoff.

Do not put speaker/witness/collateral identity in `NONCLINICAL`. It is provenance context, not clinical
noise. If an index is ever used, provenance gets its own non-assertive category, never a discard bucket.

## Q6 — Does the five-stage candidate remain right?

No. Remove the pointer index:

```text
Scribe V2.2
  -> reconciliation + action state
  -> problem architecture
  -> note compiler
  -> renderer
```

If action-state errors justify a split:

```text
Scribe V2.2
  -> reconciliation
  -> action state
  -> problem architecture
  -> note compiler
  -> renderer
```

That is the maximum useful granularity. Do not add a navigation stage, a validator stage or an audit
stage.

## Q7 — Minimum architecture

### Stage 0 — Scribe V2.2

Owns source preservation only:
- direct sources;
- turn boundaries;
- record IDs;
- raw speaker labels;
- nested provenance;
- source order;
- explicit absence/unavailable states;
- no problem, adoption, causality or note decisions.

### Stage 1 — Semantic reconciliation + action state

Owns:
- duplicate vs evolution vs conflict;
- durable disease/event identity vs source-specific state;
- current vs historical;
- patient report vs objective finding;
- action decision vs execution vs result;
- source reasoning vs fact;
- unresolved issues.

Output: source-linked ledger with Scribe record IDs. No parallel fact corpus.

### Stage 2 — Problem architecture

Owns:
- independent problem identity;
- containment;
- current stance/certainty;
- PRIMARY/BACKGROUND/NOT_RENDERED;
- causal/contributory relations;
- source-supported status and descriptors.

Output: problem ledger with record IDs.

### Stage 3 — Note compiler

Owns:
- section/unit selection;
- problem-to-section mapping;
- ordering;
- pointer-based evidence references.

No prose.

### Stage 4 — Renderer

Owns prose only. No new diagnosis, relation, status or action state.

## What to delete or supersede

- F1 atomic facts: dead.
- F1 reconciled `fact:` prose: dead.
- F1V semantic validator: dead.
- F7 final semantic audit as a runtime pass: dead.
- Pointer-only F1 as a semantic stage: remove after this verdict.
- Old one-paste/one-call execution: dead under D-034/D-037.
- Eleven model-executed micro-stages: dead as execution; keep only as conceptual ownership boundaries.

## Critique of the friend's 8-pass proposal

His instinct is right: fewer passes and no prose before structure. His Pass 1 is wrong.

`FACT` with content, type, source, time, currentness, certainty and attribution is already an
interpretation. It creates a new claim layer that needs support. That is the same failure as F1
`fact:` prose, with more fields.

His Pass 8 audit is also the same-model false-pass trap. A checklist cannot make GPT-4o independent of
its own output.

Keep from his proposal:
- source/provenance;
- current vs historical;
- action state as a distinct concern;
- problem architecture after reconciliation;
- section allocation after problem resolution;
- renderer introduces no new claims;
- semantic safeguards.

Drop:
- atomic fact corpus;
- eight passes;
- duplicated section packets;
- separate compression pass;
- same-model audit.

## What good digestion looks like

Do not digest the source into a second corpus. Digest it **once**, semantically, in the reconciliation
pass, with pointers back to the Scribe packet.

The sequence is:

1. preserve source;
2. reconcile meaning and action state;
3. build problems;
4. compile note inputs;
5. render.

That is enough.

## Test

1. Run reconciliation directly on the frozen Scribe packet, without the pointer index.
2. Compare with the pointer-index run on the same packet.
3. Check:
   - source fidelity;
   - current/historical;
   - action state;
   - problem identity/containment;
   - counterevidence;
   - note quality.
4. If direct reconciliation is equal or better, delete F1.
5. If it is worse because the packet is too large, add a **mechanical source map**, not a semantic topic
   index.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
