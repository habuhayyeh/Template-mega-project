# FILE A — SOURCE-LOCAL INGESTION

**Experimental version:** A-SOURCE-LOCAL-INGESTION-V2.1

## Purpose

Transform one complete canonical `SCRIBE_EVIDENCE_V2_2` packet into a **source-local ingestion handoff**
that preserves every material clinical assertion and action without cross-record reconciliation.

A is ingestion only.

It answers:

> What does each source record actually say, locally, with what exact source pointer and source-local wording?

A does **not** decide whether different records describe:
- the same event;
- the same state;
- evolution;
- conflict;
- duplicate/corroboration;
- one action trajectory;
- one problem.

Those decisions begin in downstream clinical synthesis.

## Runtime packaging

A is one logical ingestion phase with three lanes:

```text
A0 source registry — mechanical metadata already present in Scribe
A1 semantic spans — source-local non-action assertions
A2 action spans — source-local action assertions
```

A0 is not a separate model pass.

Use the Scribe packet's existing:
- record IDs;
- source boundaries;
- section labels;
- raw speaker labels;
- nested provenance markers;
- source order.

Do not create a new global speaker map or source index.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

## Output

```text
@@HANDOFF A_SOURCE_LOCAL_INGESTION_V2_1

SEMANTIC_SPANS

SPAN S001
  source_record=<exact record ID>
  selector=<literal substring from that exact record>
  assertion_type=<statement|question|observation|result|diagnosis|reasoning>
  material_role=<current_episode|neuro_history|other_history|medication|exam|workup|safety_function|reasoning|context>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established by this source-local record>
  provenance=<explicit nested provenance if stated in this record>
  time=<explicit source-local time if stated>
  polarity=<affirmed|negated|unresolved>
  certainty=<possible|likely|suspected|unlikely|unstated>
  unresolved=<source-local ambiguity/garble/limitation>

ACTION_SPANS

ACTION_SPAN A001
  source_record=<exact record ID>
  selector=<literal substring from that exact record>
  target=<source-local target>
  operation=<source-local action wording>
  action_phrase=<exact substring of selector expressing this action>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established by this source-local record>
  provenance=<explicit nested provenance if stated in this record>
  setting=<explicit source-local setting if stated>
  time=<explicit source-local time if stated>
  condition=<explicit source-local condition if stated>
  unresolved=<source-local action identity/wording ambiguity>

@@END
```

Use only supported fields.
Unknown fields stay absent.

---

# A0 — source registry

A0 is the Scribe packet itself.

Do not generate a second registry.

Treat as authoritative:
- exact record IDs;
- source boundaries;
- section labels;
- raw speaker labels;
- explicit nested provenance;
- source-local chronology/order.

Do not:
- globally map SPK labels to people;
- infer patient/family/clinician/witness roles;
- create cross-record event IDs;
- create SAME_EVENT_AS/PART_OF/SUPERSEDES/SOURCE_VIEW_OF relations.

If one source record explicitly names a local identity, that identity may be carried only for that span.

---

# A1 — semantic spans

## Inclusion rule

A1 is a preservation lane.

Include every source-local assertion that could materially affect:
- current neurologic episode;
- neurologic history;
- other history relevant to neurologic interpretation/management;
- medication-at-presentation;
- current examination;
- workup/result state;
- safety/function;
- diagnostic/problem-relevant reasoning;
- a material uncertainty downstream may need.

If uncertain whether a clinical assertion matters, **include it**.

Exclude only:
- greetings;
- empty acknowledgements;
- conversational repair with no usable assertion;
- clearly nonclinical logistics;
- exact repetition within the same source record when no distinction would be lost.

Do not use:
- candidate-problem status;
- perceived importance;
- likely final note placement;

as an inclusion gate.

## One span = one source-local material assertion

Every SEMANTIC_SPAN must contain:

```text
source_record=<one exact record ID>
selector=<literal substring from that same record>
```

Hard rule:

> The selector must be text that actually appears inside the cited source record.

Do not:
- combine text from adjacent records;
- paraphrase several turns into one selector;
- attach a synthesized assertion to one record;
- move a selector to a nearby record.

If one record contains multiple materially distinct assertions, create multiple spans from that same record.

A split is **required** when clauses would need different:
- polarity;
- certainty;
- attribution/provenance;
- assertion type;
- material role.

Do not assign one polarity/certainty/provenance field across a selector containing clauses with different
values.

**Safety fallback:** if a selector still contains multiple propositions with different polarity and you have
not split them, set `polarity=unresolved` and explain the mixed propositions in `unresolved`. Never assign
one global `affirmed` or `negated` value across a selector that contains both a negated finding and a separate
affirmed finding.

Examples requiring a split when clinically relevant:
- question + answer-like statement in one record;
- a negated finding + a separate affirmed finding;
- result + management action;
- several different historical referents;
- several action targets;
- separate current exam domains when downstream use differs materially.

This is not global atomicization.
Split only when failing to split would lose or invert a clinically meaningful distinction.

## Assertion type

Use only:
- `statement`
- `question`
- `observation`
- `result`
- `diagnosis`
- `reasoning`

Questions remain questions.

A question never supplies the answer to a later span.

## Speaker/source

Always preserve the raw source label.

Examples:
- `SPK0`
- `SPK3`
- `P1`

Populate `local_identity` only when the same source-local record explicitly establishes it.

Do not globally map SPK labels across the transcript.

Do not infer:
- patient;
- mother;
- fiance;
- clinician;
- witness;

from conversational context alone.

## Provenance

Preserve explicit source-local nested provenance only.

Examples:
- `EMS report`
- `ship paperwork via ED note`
- `family report of another witness`

Do not promote mediated report to objective finding.

## Time

Preserve only time stated locally in that source record.

Examples:
- Wednesday;
- 18:55;
- two days ago;
- prior;
- tonight/tomorrow.

Do not create cross-record chronology in A.

Do not emit:
- BEFORE/AFTER edges;
- SAME_EVENT_AS;
- evolution;
- conflict.

Those belong to B1 reconciliation.

## Polarity

Use:
- `affirmed`
- `negated`
- `unresolved`

Rules:
- question != negative;
- silence != negative;
- `not on file` != negative;
- `not documented` != negative;
- garbled source remains unresolved.

## Certainty

Use only explicit/source-stated epistemic certainty:

- `possible`
- `likely`
- `suspected`
- `unlikely`
- `unstated`

Do not strengthen certainty from:
- section title;
- repetition;
- management intensity;
- clinical plausibility;
- the fact that a diagnosis/topic was mentioned, discussed, or "brought up."

A topic mention without an epistemic qualifier has `certainty=unstated`.

Hedging a quantity or duration (for example "maybe 1-2 minutes," "about," "roughly") does not by itself
make the underlying clinical assertion `possible`; preserve the estimate wording and keep epistemic
certainty `unstated` unless the speaker separately qualifies whether the event/diagnosis itself is
possible/likely/suspected/unlikely.

## Material role

`material_role` is a preservation class only.

Use:
- `current_episode`
- `neuro_history`
- `other_history`
- `medication`
- `exam`
- `workup`
- `safety_function`
- `reasoning`
- `context`

It does not determine:
- final note section;
- problem eligibility;
- PRIMARY/BACKGROUND;
- containment;
- final inclusion.

---

# A2 — action spans

A2 is a lane inside the same A handoff.

It preserves each **source-local clinical action assertion** separately.

A2 does not consume or rewrite A1.

### Action inclusion gate

Include source-local clinical actions in these classes:
- diagnostic/workup tests and procedures;
- medication/treatment actions;
- consultations;
- admission/disposition decisions or actions;
- precautions and safety restrictions;
- driving/activity counseling;
- other clinical management actions.

Exclude only clearly nonclinical transport/logistics, administrative coordination, social coordination,
and conversational repair with no clinical management content.

Do not use subjective "materiality" to skip an action within the include classes.

If uncertain whether a source-local action is clinical management rather than logistics, include it and
use `unresolved`.

## One action span = one source-local action assertion

Traverse the Scribe packet **record by record, in source order**.

For every record containing clinical action wording, enumerate each distinct source-local action target /
operation before moving to the next record.

Do not skip an action-bearing record because another action elsewhere appears more important.

Every ACTION_SPAN must point to exactly one source record and one literal selector.

If one source record contains multiple distinct clinical actions, create separate ACTION_SPAN entries.

Example:

```text
Plan: CT head, basic labs, urinalysis; consult neurology; likely admission for EEG
```

should be split into separate action spans when downstream action identity differs:
- CT plan;
- labs plan;
- UA plan;
- neurology consult plan/action;
- admission/EEG plan.

Do not combine them merely because they are in one source sentence.

## Action wording only — no normalized state in A

A2 preserves the source-local action identity and wording. It does **not** classify that wording into
decision/execution/response/result state.

Required action wording fields:
- `selector` — exact source substring containing the action;
- `target` — source-local action target;
- `operation` — source-local action wording;
- `action_phrase` — exact substring of `selector` expressing this one action.

Do not emit:
- `decision=`;
- `execution=`;
- `response=`;
- `result=`;
- `raw_state_phrases=`;
- any equivalent normalized action-state field.

Words such as `plan`, `need`, `recommend`, `started`, `continue`, `hold`, `stop`, or
`discontinue` remain source wording inside `selector` / `action_phrase`. A does not map them to a
state category.

If the source-local action identity or wording is ambiguous:
- preserve the exact selector and action phrase when possible;
- describe only that source-local ambiguity in `unresolved`;
- do not resolve it through a state enum.

Normalized action-state interpretation and cross-record action episode grouping belong to B1.

## Hard action invariants

- one ACTION_SPAN = one source-local action identity;
- distinct targets/actions in one record must be split before advancing to the next record;
- a shared verb governing a coordinate list of distinct tests/procedures/targets must yield one ACTION_SPAN per target;
- distinct diagnostic tests/procedures in one record remain separate actions when their downstream identities differ;
- distinct medication actions in one record remain separate when their targets or operations differ;
- administration, loading, continuation, hold, discontinuation, and other materially different medication actions remain separate when separately stated;
- when a source says a future medication decision depends on tests, the action target is the medication decision and the tests belong in `condition`, not as the action target;
- safety/driving/activity counseling is action content and belongs in A2 rather than being duplicated as a non-action semantic span;
- `action_phrase` must be an exact contiguous substring of `selector`;
- no cross-record action episode grouping occurs in A.

---

# Coverage floor

Before returning, specifically verify that A has preserved source-local spans for every material occurrence of:

1. current neurologic examination;
2. material general exam qualifiers affecting neurologic interpretation;
3. current medications/supplements relevant to the encounter;
4. explicit prior neurologic history;
5. patient seizure-history questions/answers;
6. family seizure-history questions/answers;
7. current and outside workup/results;
8. management actions;
9. seizure/safety precautions;
10. driving/activity counseling;
11. diagnostic reasoning/differential statements;
12. material non-neurologic context that changes neurologic interpretation or management.

This is a preservation checklist, not a final-note checklist.

---

# What A must not do

A must not:
- reconcile records;
- decide duplicate/corroboration;
- decide same event/state;
- decide evolution/conflict;
- create cross-source chronology;
- group action episodes across records;
- globally map speaker identities;
- decide candidate-problem status;
- decide problem identity;
- decide PRIMARY/BACKGROUND;
- decide containment;
- decide causal/contributory relationships;
- decide final note sections;
- write final note prose.

All cross-record clinical synthesis begins in B.

---

# Mechanical source-fidelity invariant

Development-time invariant:

```text
for every SEMANTIC_SPAN and ACTION_SPAN:
  source_record must exist in the Scribe packet
  selector must be a literal substring of that exact source_record
```

Failure of this invariant means the A handoff is invalid.

This is mechanically checkable and does not require a semantic validator.

---

# Structural checks

Before returning:

1. every entry has one exact `source_record`;
2. every selector is a literal substring of that exact record;
3. no entry contains text synthesized from adjacent records;
4. questions remain questions;
5. raw speaker/source labels are preserved;
6. no global SPK identity mapping appears;
7. `not on file` / `not documented` is never converted to negation;
8. action spans contain source-local action identity/wording only and no normalized state enums;
9. every action_phrase is a literal substring of its selector;
10. materially distinct actions in one record are split;
11. current exam/workup/meds/history/safety/reasoning are preserved when material;
12. no cross-record relationship is asserted;
13. no problem/role/section/prose decision appears;
14. output ends with `@@END`.

Return the handoff only.
