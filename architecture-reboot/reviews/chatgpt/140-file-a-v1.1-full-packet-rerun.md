# Review 140 — File A V1.1 full-packet rerun against the unchanged oracle

## Verdict

**FAIL again — and this rerun now provides evidence for splitting A.**

The V1.1 patch fixed several of the specific V1 defects:

- patient prior-seizure history and family seizure history are now separate;
- `not on file` is no longer converted into a negative;
- cruise Keppra, ED load, and current continuation are separated into distinct action episodes;
- the current `continue Keppra` decision is now a structured ACTION;
- mixed diagnosis/action content is less bundled.

However, the same frozen oracle still fails.

The important new pattern is that V1.1 **lost material content that V1 had preserved**, while still violating attribution/action/source-reference constraints.

This is no longer well explained by one or two underspecified field values.

## Scale behavior

Still good:

- output completes with `@@END`;
- 14 decision units;
- 7 action entries;
- 6 unresolved entries;
- output size 16,153 bytes;
- no truncation;
- no atomic explosion;
- Wednesday and Thursday events remain distinct;
- baseline zoning remains distinct;
- no final prose/problem-role leakage.

So packet size is still **not** the demonstrated failure.

## Oracle score

Using the same predeclared oracle:

- PASS: 39
- FAIL: 9
- N/A: 3

The numeric score is unchanged from V1, but the failure composition changed.

### FAIL items

| Oracle | Result | Finding |
|---|---|---|
| 4 | FAIL | A007 cites T133 with selector `they checked urine for infection everything was perfect`, but T133 is only a clinician question; the answer is T134. |
| 10 | FAIL — FATAL | T133 question is used as support for a result-like assertion. This recreates the question-as-answer failure through a bad selector/reference. |
| 15 | FAIL | Speaker-role attribution remains unreliable. SPK3 is globally treated as mother in some units but as patient in others; the packet's diarization label is not identity-stable enough for this rule. |
| 16 | FAIL | Unmapped/unstable speakers are still role-inferred: e.g. SPK0 `role unmapped paramedic brother`; SPK3 becomes patient contextually in U008/U013. |
| 28 | FAIL | Action fields remain semantically/schema inconsistent: unsupported `decision=planned` is added to P1.014 `started on drip`; `response=unavailable` and `execution=unavailable` are emitted even though those are not allowed values and unknown fields were required to stay absent; EEG/MRI have `execution=not_started` plus `result=pending`, which overstates result state for tests not yet performed. |
| 37 | FAIL — FATAL | Current ED neurologic examination P1.041/P1.043 is no longer represented anywhere in A, despite being preserved in V1. |
| 40 | FAIL | Safety/functional management content is dropped: seizure precautions P1.044 and the T258 driving/water/heights counseling do not survive. |
| 44 | FAIL | Different assertion types are still conflated at the evidence layer: T133 question is cited as if it were the result statement from T134. |
| 51 | FAIL — FATAL | Material note-relevant distinctions are silently omitted, especially current exam and safety/precaution content. |

### N/A items

20, 23, 35 remain not applicable because the frozen packet has no established historical neurologic disease such as the synthetic left-MCA-stroke case.

## What V1.1 genuinely fixed

### Separate referents

V1:
- patient prior seizure history + family seizure history combined.

V1.1:
- U009 = patient prior-seizure history;
- U010 = family seizure history.

This is correct.

### Missing-documentation rule

V1:
- tobacco `not on file` became denial.

V1.1:
- X003 correctly preserves tobacco/allergy as absence of documentation rather than negation.

This is correct.

### Keppra episode identity

V1:
- one large Keppra object spanning cruise and ED.

V1.1:
- A001 cruise administration;
- A002 ED load;
- A003 current continuation.

This is substantially better.

### Mixed diagnosis/action

V1 hid `continue Keppra` inside a diagnosis unit.

V1.1 gives `continue Keppra` its own ACTION A003.

This is correct.

## Why V1.1 still fails

### 1. Source-reference fidelity is still not reliable

A007 says:

```text
result=final@T133[selector=they checked urine for infection everything was perfect]
```

But the source is:

```text
T132: they did EKG and checked urine for infection
T133: clinician asked if they couldn't find anything
T134: they said everything was perfect
```

A fabricated selector was attached to the wrong record.

This is not merely a vocabulary problem.

It shows the model is compressing adjacent turns into a synthesized assertion and then assigning the wrong pointer.

### 2. Speaker identity rule exposed an upstream problem

V1.1 attempts to use explicit speaker mapping, but the transcript diarization labels are not identity-stable across the whole conversation.

Examples:
- early T005 explicitly identifies SPK3 as mother Karina;
- later T116 is first-person recall of the patient's own episode;
- later T186 is `I zone out a lot`;
- later T184 again reads like mother describing what the patient said.

Therefore a global rule such as:

```text
SPK3 -> mother
```

is unsafe.

V1.1 consequently oscillates:
- U002: `SPK3 mother Karina`;
- U008: `patient via T116`;
- U013: `patient via T186`;
- U014: `SPK3 mother/patient`.

The problem is no longer just A ignoring a mapping rule.
The **source packet does not provide a stable global speaker identity mapping**.

The safe source-local representation is raw speaker label + locally explicit identity/provenance when truly established; otherwise role unresolved.

### 3. The action schema is still not obeyed

We explicitly said unknown fields stay absent.

V1.1 nevertheless emits:
- `response=unavailable`;
- `result=unavailable`;
- `execution=unavailable`;
- `decision=unavailable`.

Several of these values are not even legal for those fields.

It also adds:
- `decision=planned` to P1.014 `started on Keppra drip`, although that source establishes reported execution, not a prior planning decision.

And:
- EEG/MRI `execution=not_started` with `result=pending`.

A test not yet started does not automatically have a pending result.

This indicates the model still wants to complete an action template rather than preserve only explicitly established states.

### 4. Sparse semantic selection is not stable across runs

V1 contained a current exam unit:
- normal current neurologic exam;
- no focal deficit;
- alert/oriented;
- no tongue bite.

V1.1 drops the current exam entirely.

The source still contains:
- P1.041 neurologic exam;
- P1.043 current ED presentation/exam.

V1.1 also drops:
- P1.044 seizure precautions;
- T258 loss-of-consciousness safety counseling;
- admission planning;
- some ED workup/action material.

This is important because those omissions are not caused by packet size.
The output is actually shorter than V1.

The issue is that the same pass is deciding:
1. what source material deserves representation;
2. how to normalize it;
3. how to reconcile it across records;
4. how aggressively to compress it.

Those goals compete.

## Architectural interpretation

The agreed criterion was:

> patch local semantics once; if attribution/action failures persist, then A1/A2 becomes justified.

That criterion is now met.

More importantly, V1.1 introduces a second class of evidence:
- source-local coverage is unstable across runs.

Therefore I now favor a split.

## Proposed split

### A1 — Source-semantic preservation

Purpose:
- create a **complete material source-local ledger**;
- preserve each material assertion before cross-record reconciliation.

Owns only:
- source record + selector;
- assertion type;
- raw speaker/source label;
- locally explicit identity/provenance only;
- source/event time when explicit;
- polarity when explicit;
- source-stated certainty;
- source-local action state exactly as stated;
- note-relevance class sufficient to preserve exam/history/meds/workup/safety;
- source-local unresolved/garbled state.

Must not:
- merge across records;
- assign same_event/evolution/conflict;
- globally map speaker labels;
- infer action intermediate states;
- decide problems;
- decide sections;
- summarize several adjacent turns into a new synthesized assertion with one pointer.

A1 should be **span-linked**, not free-form claim prose.

### A2 — Reconciliation

Input:
- A1 ledger + canonical packet for dereference.

Owns:
- same event/state;
- duplicate/corroboration;
- evolution;
- conflict;
- current longitudinal synthesis;
- cross-source reconciliation;
- action-episode grouping;
- unresolved cross-record conflicts.

A2 may compress A1 into the sparse semantic ledger used by B/C.

A2 may not alter A1 source-local assertion type, attribution, polarity, explicit action state, or source pointer.

## Why this is not reopening the old atomic-fact design

The old atomic F1 failed because it:
- globally exploded records into a second near-full fact corpus;
- synthesized claims;
- created support burden.

A1 should instead preserve **material source spans** with minimal typed metadata.

The unit of preservation is not "one fact per clause."
It is "one material source-local assertion/span that downstream note construction may need."

The goal is to guarantee coverage and source fidelity before reconciliation, not to maximize atom count.

## Speaker implication

Do not globally map `SPK3`, `SPK0`, etc.

A1 should preserve:
- raw speaker label;
- explicit local role evidence when present;
- unresolved role otherwise.

If speaker identity is essential and cannot be recovered source-locally, that is a Scribe/input limitation and should stay unresolved rather than be guessed downstream.

## Next peer question

I now think the evidence meets our previously agreed threshold for an A1/A2 split.

Question for DeepSeek:

> Do you agree that V1.1's combination of persistent source-pointer/action errors **plus new material omissions** demonstrates a real boundary failure between source-local preservation and reconciliation?

If yes, I would design the smallest A1/A2 contracts next and leave B/C untouched.

No Evidence Ledger wholesale adoption is required; this is an evidence-driven split of the current A only.
