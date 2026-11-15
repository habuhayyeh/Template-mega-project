# Recommendation 002 — repair A, do not split it

**Status:** architect recommendation. Adopts the expert memo with four clarifications.

## Verdict

The memo is correct: the full-packet A failure is **contract weakness**, not ingestion overload.

A completed compactly and preserved major event boundaries. The failures were semantic promotions and
boundary violations:

- speaker identity became assertion identity;
- plan became order;
- reported execution became inferred decision;
- separate action episodes collapsed by shared target;
- missing documentation became a negative;
- patient history and family history merged;
- formulation and management bundled.

Do not split A into A1 extraction and A2 reconciliation. Reconciliation belongs to Processing. A stays
one ingestion pass with three internal lanes:

```text
A0 SOURCE REGISTRY
A1 SEMANTIC UNITS
A2 ACTION LANE
```

These are lanes in one run, not separate model calls.

## Adopt

### 1. Source registry and source-view attribution

Separate:

- `SUBJECT` — who/what the assertion is about;
- `SPEAKER` — who said it;
- `SPEAKER_ROLE` — explicit role, only when supported;
- `MODE` — patient report / caregiver report / witness / clinician / objective / chart.

Attribution belongs on the **source view**, not duplicated on the unit unless every view shares it.

Registry example:

```text
@@SOURCE_REGISTRY
T/SPK1 = current Neurology clinician
T/SPK2 = fiance / witness
T/SPK3 = mother / caregiver
T/SPK0 = local role varies by segment; preserve per-segment identification
@@END
```

Do not create a speaker object per utterance. Do not assign a stable real-world identity from `SPK#`
alone.

### 2. `ASSERTION_DOMAIN`

One unit answers one clinical question about one subject/entity during one relevant temporal frame.

Example:

```text
ASSERTION_DOMAIN=patient prior seizure history
```

versus:

```text
ASSERTION_DOMAIN=family seizure history
```

The domain is a non-assertive question label, not a diagnosis.

### 3. `EVIDENCE_STATE`

Make absence/documentation state first-class:

```text
reported_present
denied
not_on_file
not_asked
not_performed
unavailable
unknown
```

Hard rules:

```text
not_on_file != denied
not_performed != negative result
```

`not_asked` only when the source explicitly establishes it. Silence is not a negative.

Keep `EVIDENCE_STATE` separate from attribution/mode. “Not on file” is a documentation state; “patient
report” is attribution.

### 4. No mixed semantic types in one unit

A unit may contain several observations of the same event. It may not contain:

```text
diagnostic formulation + management decision
```

Split when the semantic type changes, even within one sentence.

### 5. Action lane

Fields:

```text
TARGET
OPERATION
ACTOR
TIME_SETTING
DECISION
EXECUTION
RESPONSE
RESULT_STATE
CONDITION
REFS
```

Rules:

- every field except target/refs is optional;
- empty is correct;
- never infer one state from another;
- `planned` is not `ordered`;
- `started` is execution evidence, not decision evidence;
- `pending` is not inferred from a recommendation;
- one action episode per actor + target + operation + time/setting;
- a drug's whole history is several action records, not one.

Examples:

```text
"Plan: CT head, basic labs"
-> TARGET=CT head; OPERATION=obtain; DECISION=planned; EXECUTION=
```

```text
"Patient was started on a Keppra drip"
-> TARGET=levetiracetam; OPERATION=start/administer; EXECUTION=started; ACTOR=cruise team
```

```text
"Keep on Keppra for now"
-> TARGET=levetiracetam; OPERATION=continue; ACTOR=current Neurology; DECISION=planned;
   EXECUTION=; CONDITION=for now
```

### 6. Unit boundary rule

> Keep material together only if it answers the same clinical question about the same subject/entity,
> same event or longitudinal state, and same semantic type. Otherwise split.

Concrete splits:

- patient history vs family history;
- diagnostic stance vs management;
- one event vs a different event/trajectory;
- one action episode vs a drug course;
- formulation vs action.

Keep together:

- observations of the same event evolving in time;
- source views of the same clinical question;
- duplicates of the same assertion.

### 7. Coverage invariants

A does not need every packet sentence. It must preserve every materially distinct:

- event identity/trajectory;
- patient vs family vs witness history;
- source attribution that changes evidentiary meaning;
- explicit diagnostic/formulation stance, including differential-only alternatives;
- action episode and state;
- objective result/result state relevant to the neurologic evaluation;
- explicit negative vs unavailable/not-documented distinction;
- material disagreement/uncertainty;
- current vs historical vs future scope.

Test with a hand-authored oracle of invariants, not another model audit.

## Clarifications to the memo

### 1. `ASSERTION_DOMAIN` must not become a diagnosis

Use a question/domain label, not a clinical conclusion. If it cannot be phrased as a non-assertive
question, split the unit or leave it in `SOURCE_VIEWS` without a domain.

### 2. Registry scope must be local

`SPK` labels are not global identities. The registry may assign a role only where the packet explicitly
supports it. If a speaker’s role changes by segment, preserve per-segment identification. Do not infer
“mother” from content.

### 3. `EVIDENCE_STATE` is not attribution

Keep documentation state separate from:

- who reported it;
- whether it is patient/caregiver/clinician/objective;
- certainty.

“Not on file” and “patient denies” are different axes.

### 4. `CORE` remains non-authoritative

If a `CORE` orientation is used, it is navigation only. It must not contain a diagnosis, count, causal
relation, resolved conflict or current/historical conclusion. Source views win.

## First test after repair

Use the same frozen packet. Check:

1. speaker role preserved (`mother` is not `patient`);
2. patient history and family history split;
3. `not on file` stays `not_on_file`;
4. `Plan: CT` is `decision=planned`, no execution;
5. `started on drip` is `execution=started`, not `ordered`;
6. cruise/ED/Neurology Keppra actions are separate episodes;
7. `continue Keppra for now` is a structured action;
8. ED differential survives as formulation;
9. mixed formulation/management sentences split;
10. no truncation and output remains compact.

If these pass, A is repaired. If they fail again, then consider a structural split.

## What not to add

- atomic proposition extraction;
- object per utterance;
- second fact corpus;
- pointer-only topic index;
- A2 reconciliation;
- source-authority ranking in ingestion;
- large action ontology;
- inferred `pending`;
- inferred negatives;
- automatic diagnosis from phenomenology;
- per-line coverage map;
- same-model validator;
- duplicated source text.

## Architecture

```text
SCRIBE PACKET
  -> A INGESTION
       source registry
       semantic units
       action lane
  -> B PROCESSING
       reconciliation
       problem architecture
       note blueprint
  -> C OUTPUT
       renderer
```

A preserves evidence. B reconciles and decides. C renders.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
