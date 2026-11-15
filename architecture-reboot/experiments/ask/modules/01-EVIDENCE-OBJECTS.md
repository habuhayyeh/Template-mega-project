# SUPERSEDED — DO NOT RUN

Superseded after Doximity execution showed global atomicization cardinality/truncation. See review 121 and `01-RECONCILED-EVIDENCE.md`.

# FILE 1 — EVIDENCE OBJECTS

**Experimental version:** F1-EVIDENCE-V2

## Function

Transform a Scribe V2.2 evidence packet into atomic source-aware clinical evidence objects for the next function.

This file performs **source-faithful extraction/normalization only**.

Do not write a note.

## Input

One complete `SCRIBE_EVIDENCE_V2_2` packet.

The packet already provides:
- source boundaries;
- ordered source record ids;
- transcript speaker labels;
- prechart section labels;
- nested attribution such as `VIA=`;
- inline `[UNCLEAR]` / `[VERBATIM]` markers.

Treat those as source data. Do not recreate or reinterpret the source hierarchy.

## Step 0 — packet precheck

Before extracting evidence objects, verify the packet shape:

- one opening `@@PACKET SCRIBE_EVIDENCE_V2_2`;
- one closing `@@END`;
- each `@@SOURCE` header precedes its records;
- record ids are unique;
- every record belongs to one source block;
- every record can be read as `<record id> :: <source/speaker label> :: <text>`;
- `SEC=` and `VIA=` remain source text/metadata when present;
- no record is silently skipped because its syntax is unusual.

If the packet is structurally unusable, output only:

```text
@@HANDOFF F1_EVIDENCE_V2
STATUS=INVALID
RECORD=<record id or PACKET>
REASON=<brief structural reason>
@@END
```

Do not emit a partial evidence set after declaring the packet invalid.

This is a fail-closed runtime instruction. Deterministic external parsing may be used during engineering validation, but Doximity Ask itself has no native code execution; do not pretend this LLM precheck is deterministic proof.

## Valid output

If the packet is usable, output only:

```text
@@HANDOFF F1_EVIDENCE_V2
STATUS=VALID
<evidence objects>
@@END
```

Use one line per evidence object:

```text
E0001 :: SRC=<input record id> :: ACT=<speech act> :: POL=<polarity> :: CERT=<certainty> :: TIME=<fact time/scope> :: ATTR=<source attribution> :: TEXT=<one atomic clinical proposition>
```

Use sequential evidence ids in source order.

One input record may produce multiple evidence objects.

Each evidence object must derive from **one input record only**.

### Parsing rule

Only the first six literal ` :: ` separators after the evidence id are structural.

After `TEXT=`, the rest of the line is literal evidence text even if it contains `::`, `=`, punctuation, quotation marks, brackets, or source wording.

Do not insert line breaks inside one evidence object.

## ACT — speech act only

Use only:

```text
STATEMENT
QUESTION
ACTION_MENTION
REASONING
```

This is not a disease/symptom/test ontology.

Do not classify clinical content as DISEASE, SYMPTOM, EVENT, EXAM, TEST, etc. File 1 does not own that clinical categorization.

### ACT definitions

- `STATEMENT` — source states a clinical fact, observation, history, symptom, finding, functional/social/family fact, medication fact, or other proposition.
- `QUESTION` — clinically meaningful question whose answer is not part of this same source record.
- `ACTION_MENTION` — explicit management/test action or action-state statement.
- `REASONING` — source explicitly states diagnostic, causal, localization, differential, or other clinical reasoning.

If a source record contains more than one speech act, split it into separate evidence objects.

## POL — polarity

Use:

```text
POSITIVE
NEGATIVE
NA
```

- `POSITIVE` — proposition is affirmed.
- `NEGATIVE` — proposition is explicitly negated.
- `NA` — use for questions or where positive/negative polarity is not meaningful.

Do not convert absence of mention into `NEGATIVE`.

## CERT — source certainty

Use:

```text
ASSERTED
POSSIBLE
LIKELY
UNLIKELY
UNSPECIFIED
NA
```

This records only the certainty expressed in the source proposition.

- `ASSERTED` — source states the proposition without an uncertainty qualifier.
- `POSSIBLE` — possible/may/could or equivalent.
- `LIKELY` — likely/probable/favored or equivalent.
- `UNLIKELY` — unlikely/doubtful or equivalent.
- `UNSPECIFIED` — a statement exists but its certainty cannot be safely classified.
- `NA` — use for questions where certainty is not applicable.

Do not strengthen certainty because a proposition is repeated.

Do not use `UNCLEAR` as a certainty value. Preserve `[UNCLEAR: ...]` or `[VERBATIM: ...]` inside `TEXT` when present in the packet.

## TIME — fact time/scope

Use:

```text
CURRENT_EPISODE
ONGOING
CURRENT
HISTORICAL
FUTURE_CONDITIONAL
UNKNOWN
```

Definitions:

- `CURRENT_EPISODE` — belongs to the current encounter/event or its immediate evolution.
- `ONGOING` — continuing state/regimen/deficit/disease course extending across time and still explicitly supported as ongoing by the source.
- `CURRENT` — current source assertion when a more specific temporal category is not supported.
- `HISTORICAL` — fact/event/state explicitly belongs to the past and is not itself a current episode fact.
- `FUTURE_CONDITIONAL` — proposed/conditional future state or action condition.
- `UNKNOWN` — fact time cannot be supported from the record.

Record the time of the **fact**, not merely the source date.

Do not convert a fact to CURRENT only because it appears in a current note.

Do not infer that an old status remains ongoing unless the source explicitly supports persistence.

## ATTR — attribution

Preserve attribution mechanically.

Examples:

```text
ATTR=SPK2
ATTR=P1
ATTR=VIA:prior neurology note
ATTR=patient-reported
ATTR=collateral-reported
```

If the packet gives only a raw speaker label, preserve the raw speaker label. Do not infer a stable real-person identity from `SPK#`.

If no additional attribution exists beyond the source record, use `ATTR=-`.

Do not infer that two different speaker labels are the same person.

## Atomicity

One evidence object = one clinical proposition.

Split a composite input record when it contains separable propositions with different meaning, time, polarity, certainty, speech act, attribution, or downstream use.

Example:

```text
Input:
T010 :: SPK2 :: Prior stroke in 2022 with residual right weakness; weakness became worse yesterday.

Output:
E0001 :: SRC=T010 :: ACT=STATEMENT :: POL=POSITIVE :: CERT=ASSERTED :: TIME=HISTORICAL :: ATTR=SPK2 :: TEXT=Prior stroke occurred in 2022.
E0002 :: SRC=T010 :: ACT=STATEMENT :: POL=POSITIVE :: CERT=ASSERTED :: TIME=ONGOING :: ATTR=SPK2 :: TEXT=Residual right-sided weakness persisted after the prior stroke.
E0003 :: SRC=T010 :: ACT=STATEMENT :: POL=POSITIVE :: CERT=ASSERTED :: TIME=CURRENT_EPISODE :: ATTR=SPK2 :: TEXT=Right-sided weakness was reported worse yesterday.
```

Do not add laterality, localization, diagnosis, causal wording, or other detail not present in the input record.

Do not merge propositions from different input records.

## Clinical questions

A question is not a fact.

Preserve a clinically meaningful question as `ACT=QUESTION`, `POL=NA`, `CERT=NA`.

Never convert a question, silence, or ambiguous response into a denial, normal finding, patient statement, diagnosis, or answer.

Later functions may reconcile a question with an answer from another record.

## Actions

Represent an explicit management/test action as `ACT=ACTION_MENTION`.

Preserve the action state actually stated in the source, for example:
- considered;
- recommended;
- planned;
- ordered;
- given;
- performed;
- completed;
- held;
- stopped;
- pending.

Do **not** reconcile repeated action statements or infer a later/final action state here. File 3 owns source-level action-state reconciliation.

Do not decide whether the action is the final encounter plan.

## Reasoning

If a source explicitly states diagnostic, causal, localization, differential, or other clinical reasoning, preserve it as `ACT=REASONING`.

Do not decide whether that reasoning is correct or ultimately adopted.

Do not invent a causal relationship from coexistence.

## Fidelity rules

Preserve:
- negation;
- uncertainty;
- laterality;
- chronology;
- source attribution;
- patient vs clinician/collateral distinction where supplied;
- clinically meaningful negatives;
- explicit absent/unavailable test/result states;
- explicit source reasoning;
- `[UNCLEAR]` and `[VERBATIM]` meaning.

Do not:
- correct medically odd source wording;
- silently normalize a diagnosis;
- resolve contradictions;
- deduplicate across records;
- cluster entities across records;
- decide final disease/event identity across sources;
- decide current encounter adoption;
- decide problem identity;
- decide PRIMARY/BACKGROUND;
- decide note relevance;
- assign note sections;
- write summary prose.

## Compression

Remove only wording that carries no clinical proposition after the Scribe packet has already been processed.

Do not drop a proposition merely because it seems unimportant.

The next functions, not File 1, own cross-source reconciliation and relevance.

## End condition

Before returning the handoff, check:

1. every evidence object traces to one Scribe record;
2. every line contains one proposition only;
3. no cross-record synthesis occurred;
4. no question became a fact;
5. no polarity, certainty, or fact-time was strengthened;
6. no clinical-type ontology was introduced;
7. no problem/note-use decision was made.

Return the handoff only. No explanation before or after it.
