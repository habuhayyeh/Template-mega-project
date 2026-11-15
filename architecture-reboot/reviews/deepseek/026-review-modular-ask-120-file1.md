# DeepSeek review — modular Ask runtime 120 and File 1

**Reviewed:** `proposals/chatgpt/120-modular-ask-runtime-v0.md`,
`experiments/ask/modules/01-EVIDENCE-OBJECTS.md`
**Status:** review only; no implementation.

## Verdict

The seven-function direction is sound and is now the canonical modular runtime candidate. Keep F1–F7;
do not revert to the six-file grouping.

File 1 is the right first experiment, but it currently adds a **new unratified kind ontology** and
conflates two source-stance dimensions. Those are the material issues. F2/F3 boundaries also need one
sentence each to prevent them from becoming silent S1/S2 adjudication.

## F1 — EVIDENCE OBJECTS

### Accept

- one input record may split into multiple objects;
- one object derives from one input record;
- no cross-record merge, dedupe, entity clustering, adoption, problem identity, role, section or note;
- questions stay `QUERY`;
- action mentions stay atomic and unadjudicated;
- reasoning preserved as source reasoning;
- exact source IDs, attribution, negation, uncertainty, chronology and markers preserved;
- handoff-only output.

### Reject: the 14-label `KIND` taxonomy

The consensus architecture explicitly says the kind taxonomy is **not ratified**. File 1 introduces:

```text
DISEASE, SYMPTOM, EVENT, EXAM, TEST, MEDICATION, ACTION,
REASONING, FUNCTION, SOCIAL, FAMILY, PREFERENCE, QUERY, OTHER_CLINICAL
```

That is a new clinical ontology wearing an extraction label. It will:
- force GPT-4o to make a semantic classification before S1/S2;
- create cascading errors when the same proposition fits two kinds;
- diverge from the consensus candidate set (`IDENTIFIER`, `FACT`, `COURSE`, `REASONING`, `PLAN`);
- need its own calibration.

**Recommendation:** remove `KIND` from F1, or reduce it to a mechanical bridge:

```text
POLARITY=POSITIVE|NEGATIVE
CERTAINTY=ASSERTED|POSSIBLE|LIKELY|UNLIKELY|UNCLEAR
SPEECH_ACT=STATEMENT|QUESTION|ACTION_MENTION|REASONING
```

Clinical type belongs to F4 (problem/state/relations), not F1. If a type is needed for routing, use
`STATEMENT | QUESTION | ACTION_MENTION | REASONING` only. Do not add DISEASE/SYMPTOM/EVENT labels now.

### Fix `STANCE`

`STANCE=ASSERTED|NEGATED|POSSIBLE|LIKELY|UNLIKELY|UNCLEAR` mixes three axes:

- polarity: positive vs negated;
- certainty/modality: asserted vs possible/likely/unlikely;
- clarity: unclear.

“No seizure” and “seizure unlikely” must not collapse into one label. Use two fields:

```text
POLARITY=POSITIVE|NEGATIVE
CERTAINTY=ASSERTED|POSSIBLE|LIKELY|UNLIKELY|UNCLEAR
```

This is mechanical source annotation, not diagnosis.

### Keep `TIME` but define overlap

`CURRENT`, `CURRENT_EPISODE`, `ONGOING`, `HISTORICAL`, `FUTURE_CONDITIONAL`, `UNKNOWN` is acceptable as
a source-time hint, but `CURRENT`/`ONGOING`/`CURRENT_EPISODE` overlap. Define:

- `CURRENT_EPISODE` = this encounter/event;
- `ONGOING` = continuing state;
- `CURRENT` = current source assertion without finer boundary;
- `UNKNOWN` when not supported.

Do not infer current from source date.

### Parser and validation

F1 must begin with a **deterministic packet check**:

- `@@PACKET`/`@@END` present;
- source headers and record IDs unique;
- `id :: label :: text` parse;
- prechart `SEC=`/`VIA=` fields parse;
- no orphan record; no silent drop;
- exact text preserved.

If malformed, return `STATUS INVALID` with a record pointer; do not extract a partial semantic object
set. This validator can be deterministic code before the F1 prompt; it is not a new function.

### Line format

`TEXT=<proposition>` with `::`/`=` inside text is ambiguous. Define: split only the fixed leading
fields, `TEXT=` consumes the rest of the line; forbid newlines in one object; if text contains a
structural separator, escape or quote it. A strict parser is safer than model interpretation.

## F2/F3/F4 boundaries

### F2

“Identify records referring to the same disease/event/finding” and “distinguish durable disease identity”
is clinical identity, which can pre-empt S1. Restrict F2 to **source-reference reconciliation**:
same mention/entity candidates, explicit duplicates, longitudinal source evolution. Output candidate
links with uncertainty; F4 decides problem identity and final state. Do not let F2 produce a final
disease identity that F4 merely inherits.

### F3

Action-state adjudication is source-level only:
considered/recommended/planned/ordered/started/performed/completed/held/stopped **as stated by the
source**. Final encounter plan/adoption belongs to F4/S2. This is already implied; make it explicit.

### F4

Bundling S1/S2/S3 is acceptable for GPT-4o, but the internal order must be observable. Require three
sub-ledgers or checkpoints:
1. identity partition;
2. state/relations;
3. role/use.

F5 must consume all three. If F4 collapses them into one prose blob, failure localization disappears.
Do not split F4 preemptively; test it with checkpoints first.

## F5/F6/F7

- F5 note compiler is heavy but coherent; keep.
- F6 renderer must not repair semantics; keep.
- F7 output guard is diagnostic only; keep the restriction that it may not reopen F1–F5. Do not treat
  its self-check as acceptance evidence.

## Canonicalization

- **120 is the current modular runtime proposal.** D-037.
- **026 (DeepSeek six-file grouping) is superseded by 120.** Keep it only for the packet-to-index
  validation idea.
- 119/016 fold into F4; 024 P/N end-to-end is superseded.
- File 1 is the active experiment.

## Next

- revise File 1: remove/reduce `KIND`, split polarity/certainty, add packet validation and line-format
  rules;
- then run F1 only on the frozen Scribe packet;
- do not finalize F2–F7 prompts before F1 evidence.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
