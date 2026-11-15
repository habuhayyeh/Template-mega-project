# DeepSeek architecture review — old architecture and ingestion

**Scope:** architecture critique and ingestion recommendation. No implementation.

## Verdict

The old architecture is no longer valid as an **execution** design. Its conceptual ownership boundaries are
still useful. Its assumption that GPT-4o can execute many small semantic stages, validate itself, and
carry a large structured IR through one call is not supported by the runs.

The friend's proposal has the right instinct — fewer passes, explicit structure, no prose until the
structure is stable — but Pass 1 recreates the exact problem we just removed: a new atomic-fact claim
layer. Do not adopt his 8-pass pipeline as written.

The best digestion is:

```text
Scribe V2.2 packet (source of truth)
  -> F1 pointer-only index (navigation, no claims)
  -> F2 semantic reconciliation + action state
  -> F3 problem architecture
  -> F4 note compiler
  -> F5 renderer
```

No F1V, no separate audit pass, no atomic-fact corpus.

## What is dead in the old architecture

1. **One paste / one Ask call.** D-034 and D-037 moved production to Scribe packet -> modular Ask. The
   old production constraint in `CONSENSUS_ARCHITECTURE` §1 is obsolete.
2. **Eleven model-executed micro-stages.** GPT-4o does not reliably preserve ownership, references and
   state across that many transformations. More stages increased drift, not control.
3. **Global atomicization.** The first F1 run produced ~175 objects and truncated. A second corpus of
   facts is not a safe intermediate.
4. **Synthesized fact prose as the handoff.** Every `fact:` sentence creates a support obligation. The
   model then needs another pass to verify it.
5. **Same-model semantic validation.** F1V emitted a complete VERIFY ledger and still false-passed. The
   validator was a second editor, not an independent check.
6. **Deterministic validation inside Ask.** Doximity Ask has no native code execution. Deterministic
   checks are engineering tools, not runtime guarantees.
7. **A large explicit Case IR carried through one call.** It is too heavy for GPT-4o and creates more
   places for paraphrase drift.

## What survives

Keep these as constraints, not as separate prompts:

- Scribe packet is the canonical, immutable evidence store.
- Source provenance, record IDs, speaker labels and source order.
- Current vs historical; disease identity vs current status.
- Patient report vs objective finding.
- Diagnosis vs evidence; problem vs manifestation.
- Contained manifestation vs distinct disorder.
- PRIMARY vs BACKGROUND.
- Certainty and negation.
- Action decision vs execution; test performed vs result available.
- Counterevidence and unresolved conflict.
- No prose until structure is stable.

These are semantic safeguards. They do not each need a stage.

## Ingestion approaches we have tried or proposed

### 1. Old I1–I4 ingestion modules inside Ask

Scribe already performs most source-boundary, ordering and provenance work. Re-running I1–I4 inside Ask
duplicates Scribe and adds failure surface. Do not do it.

### 2. Scribe V2.2 source packet

Current best foundation. It preserves source boundaries, turn order, IDs, raw speaker labels, nested
provenance, uncertainty markers and absent/unavailable states. Keep it canonical.

### 3. Global atomic F1

Failed empirically: ~175 objects, truncation, second corpus. Abandon.

### 4. Lazy reconciled F1 with `fact:` prose

Compact and clinically useful, but it creates a new claim layer. F1V then tries to verify claims with
the same model and false-passes. This is the current failure.

### 5. Pointer-only F1

Current best candidate. F1 groups source record IDs under non-assertive topic labels; downstream
dereferences the packet. No claim layer, no support validator, no source duplication.

### 6. Friend's 8-pass pipeline

Right direction on pass count; wrong on Pass 1. See below.

### 7. No F1 at all

Scribe packet -> semantic reconciliation directly. This is the smallest possible runtime. It may be
better than a pointer index if the packet is short enough. Keep it as the fallback if F1 pointer index
does not materially help navigation.

## Critique of the friend's proposal

### What is right

- Fewer passes.
- Explicit intermediate representations.
- No prose drafting until structure is stable.
- Source/provenance retained.
- Actions separated because action-state errors are high-impact.
- Problem architecture after reconciliation.
- Section allocation after problem resolution.
- Renderer introduces no new clinical claims.
- The semantic-safeguards list is good.

### What is wrong

#### Pass 1 recreates the claim layer

His atomic `FACT` has `content`, `type`, `source`, `time`, `currentness`, `certainty`, `attribution`.
That is not neutral extraction. It is a semantic assertion with a type and a temporal stance. Every fact
then needs support verification. This is the same trap as F1 `fact:` prose, just more fields.

If you keep Pass 1, it must be **pointer-only**: source record IDs plus a non-assertive topic label, not
fact content. The friend's example (`prior left MCA stroke`, `residual right hemiparesis`, `worsened
yesterday`) is already an interpretation of the source.

#### Eight passes is still too many for GPT-4o

Each pass output becomes context for the next. Reconciliation over all atomic facts, then problem
architecture, then section packets, then compression, then audit — that is a large working set. The
model will drift and summarize.

#### Section packets duplicate source

Pass 5 redistributes facts into HPI/history/med/exam/workup/A/P packets. That is a second copy of the
evidence. Use pointers to source records and problem IDs instead.

#### Pass 6 compression can delete counterevidence

A separate compression pass optimizes for brevity after the problem model is built. That is exactly
where material counterevidence disappears. Compress inside the problem packet, with explicit keep rules.

#### Pass 8 audit is the same-model false-pass trap

A final checklist is useful for a human reviewer. It is not a reliable runtime validator for GPT-4o.
The F1V experiment already showed full checklist compliance with false PASS.

#### It assumes more model reliability than Doximity gives

The friend is not wrong clinically; he is designing for a model that can carry eight structured passes.
GPT-4o inside Ask cannot reliably do that.

## Recommended digestion

### Pass 0 — Scribe

Scribe V2.2 produces the canonical packet. No Ask re-ingestion.

### Pass 1 — pointer-only index

F1 groups source records by topic. No claims, no polarity, no certainty, no action state, no copied
quotes. Every record is clustered or explicitly unclustered. This is navigation, not evidence.

If the packet is short or the index is not useful, skip this pass.

### Pass 2 — semantic reconciliation + action state

One semantic pass over the packet + index. It produces a source-linked ledger:

- durable disease/event identity vs source-specific state;
- duplicates vs evolution vs conflict;
- current vs historical;
- action decision vs execution vs result;
- unresolved issues.

Every entry cites Scribe record IDs. Do not synthesize a parallel fact corpus.

Action state can be split into its own pass if empirical errors justify it. Do not pre-build the split.

### Pass 3 — problem architecture

One pass for:

- independent problem identity;
- containment;
- current stance/certainty;
- PRIMARY/BACKGROUND/NOT_RENDERED;
- causal/contributory relations;
- source-supported status and descriptors.

Keep an observable ledger: identity -> state/relations -> role/use.

### Pass 4 — note compiler

Map problems and evidence to template sections and units. Use pointers to source records, not copied
facts. No prose yet.

### Pass 5 — renderer

Write the note from the compiler output. No new diagnosis, relation, status or action state.

No F1V. No separate audit pass. Audit is human/external, or a narrow mechanical check for IDs and
coverage.

## Why this is better

- one source of truth: Scribe packet;
- no atomic-fact corpus;
- no claim layer to validate;
- no same-model validator;
- fewer passes, each with a coherent job;
- pointers instead of copied source;
- action state gets its own pass only if needed;
- problem architecture remains the main semantic pass;
- renderer is constrained.

## Test plan

1. Freeze one representative Scribe V2.2 packet.
2. Run F1 pointer-only. Check: every record clustered or unclustered; labels non-assertive; no claims;
   output size.
3. Run F2 reconciliation/action on packet + index. Check: record IDs, current/historical, action state,
   conflicts.
4. Run F3 problem architecture. Check: independent problems, containment, role, relations.
5. Run F4 compiler and F5 renderer. Check: no new claims, template fit, source fidelity.
6. Compare with a direct Scribe -> F2 run. If the pointer index does not help, remove F1.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
