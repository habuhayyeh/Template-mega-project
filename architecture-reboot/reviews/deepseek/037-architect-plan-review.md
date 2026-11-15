# DeepSeek review — the architect plan

**Scope:** current A/B/C build, plus the Evidence Ledger ingestion alternative in
`reviews/deepseek/033-evidence-ledger-ingestion.md`.
**Status:** architecture review. No implementation.

## Verdict

The A/B/C direction is sound. The main risk is that **A is doing two jobs** — evidence preservation and
semantic reconciliation — and it has only been tested on three records. Do not build more of C until A is
tested on a full Scribe packet.

The Evidence Ledger plan has the better conceptual boundary. It is not ready to replace A as written,
because it puts reconciliation decisions inside ingestion.

## Current A/B/C: what is right

- Scribe packet remains canonical.
- A is a sparse semantic ledger, not an atomic-fact corpus.
- B owns problem identity, containment, role, causality and action ownership.
- C owns section allocation, chronology, evidence/counterevidence and action placement.
- C produces a blueprint before prose.
- No same-model validator.
- The three-record boundary test passes.

## Current A/B/C: what worries me

### 1. A is overloaded

A's contract is 315 lines and asks for:

- assertion type;
- referent/event identity;
- provenance;
- time/scope;
- polarity/certainty;
- duplicate/evolution/conflict reconciliation;
- action state;
- nonproblem preservation;
- unresolved register.

That is ingestion **and** reconciliation in one GPT-4o pass. On three records it works. On a 300-record
packet, it may truncate, over-merge, or produce a unit count that defeats the purpose.

### 2. A has no explicit source-view separation

A merges records into a unit. When sources disagree, it can store `relation=conflict`/`possible_overlap`,
but it does not preserve each source's view as a separate short fragment. The packet is available, so this
is recoverable, but the ledger may hide the disagreement from B/C.

### 3. A is measured on the wrong fixture

The three-record test proves boundaries, not scale. It does not test:

- multi-assertion records;
- 300 records;
- many speakers;
- action-state clusters;
- conflicting sources;
- medication lists;
- exam/workup material.

C is being built on top of an untested A.

## Evidence Ledger plan: what is better

- Separates ingestion from processing.
- Ingestion preserves source-grounded spans; processing reconciles.
- One event can hold multiple source views.
- `CORE`/`LABEL` is explicitly non-authoritative.
- `Q` class for questions.
- Limited relation vocabulary.
- 15–25 records, not 150–300.
- Explicit action-state fields.
- Test expects no count total, no stroke–falls relation, no residual deficit.

This is the right instinct: **do not make ingestion decide what the sources mean together.**

## Evidence Ledger plan: what is wrong

### 1. It puts reconciliation relations in ingestion

The relation list includes:

```text
SAME_EVENT_AS
PART_OF
SUPERSEDES
```

Those are reconciliation decisions. `SAME_EVENT_AS` is exactly the judgment the plan says processing owns.
`SUPERSEDES` is an action/state judgment. Keep only source-local links at ingestion:

```text
SOURCE_VIEW_OF
BEFORE / AFTER (only explicit chronology)
```

Move `SAME_EVENT_AS`, `PART_OF`, `SUPERSEDES` to processing.

### 2. `CORE` is still a claim surface

The correction says one-line orientation, but the example is still a synthesized clinical sentence. If
`CORE` exists, it must be a noun-phrase label only:

```text
LABEL=Thursday recurrent episodes
```

No count, no semiology summary, no diagnosis, no severity. Processing must use `SOURCE_VIEWS` + refs.

### 3. Source views can still paraphrase

“Short source-grounded fragment” is not a precise rule. Require:

- one or two sentences;
- exact qualifiers preserved;
- record ID + selector;
- no merging views into one sentence;
- no copied transcript blocks.

### 4. Processing bundles too much

The plan gives processing:

- reconciliation;
- episode model;
- problem architecture;
- note blueprint.

That is three or four jobs in one pass. If adopted, split processing into reconciliation/problem
architecture and note blueprint, as A/B/C already does.

### 5. 15–25 records may over-compress

A single event bundle can hide material differences in attribution, timing, count, or action state. The
record range `T099-T140` is too coarse; require selectors and source views for each materially different
account. Coverage must be tested, not assumed.

## Recommendation

Do not pivot the whole architecture now. Do this:

1. **Freeze C feature work.**
2. Run current A on one full real Scribe packet.
3. Measure:
   - completion/truncation;
   - unit count;
   - material coverage;
   - fatal fidelity errors;
   - whether B can build a correct map from A + cited records.
4. If A holds, continue B/C as built.
5. If A fails at scale, split A into:
   - A1 Evidence Ledger: classes, source views, refs, questions, action mentions;
   - A2 Reconciliation: merge/conflict/currentness/action state.
   Move `SAME_EVENT_AS`/`PART_OF`/`SUPERSEDES` to A2.

Adopt these Evidence Ledger ideas now, without adding a new pass:

- non-authoritative labels;
- `Q` class for questions;
- source views with selectors;
- no `SAME_EVENT_AS`/`PART_OF`/`SUPERSEDES` at ingestion;
- no copied transcript blocks.

## Decision rule

A is good enough to build on when a full packet passes:

- no truncation;
- every material distinction represented/cited;
- no fatal attribution/time/polarity/action errors;
- B can make problem decisions from A + cited records.

Until then, more C work is speculative.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
