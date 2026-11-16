# Prompt — challenge the eight coverage buckets

Use this with the architect or a senior note writer. Attach the Scribe packet, the current coverage output,
and the target note. No patient identifiers.

---

You are reviewing an architecture decision. Do not write code or prompt text yet. Challenge the category
design and recommend the smallest correction.

## Context

Pipeline:

```text
Scribe packet
  -> coverage census (record IDs only)
  -> clinical synthesis
  -> note blueprint
  -> render
```

The coverage census is supposed to guarantee that the synthesis stage can find every clinically relevant
source record before it starts writing. It is an index, not evidence.

Current eight buckets:

```text
current_event_records
baseline_comparator_records
neuro_history_records
medication_context_records
exam_records
workup_records
action_bearing_records
context_records
```

A record may appear in more than one bucket.

These eight were chosen by the AI design loop, not by the signer. They were derived from an earlier
eight-class Evidence Ledger and mapped to note sections. They were not empirically validated.

## Observed failures

The model sometimes omits whole buckets, especially `current_event_records` and `action_bearing_records`.

Other times it over-tags:

- consult/evaluation records placed under `current_event`;
- treatment records placed under `current_event` and `workup`;
- baseline comparator records placed under `neuro_history`;
- medication history placed under `neuro_history`;
- diagnostic reasoning placed under `action_bearing`.

Examples from the current packet:

- `T001` neurology consult/evaluation -> tagged as current event.
- `T008` ship evaluation/testing/monitoring -> tagged as current event and workup.
- `T015` levetiracetam treatment -> tagged as current event and workup.
- `T016` longstanding baseline staring -> tagged as neuro history.
- `P1.005` no prior antiseizure medication -> tagged as neuro history.
- `T018/T019` diagnostic reasoning -> tagged as action-bearing in one run.

## The challenge

1. Are these eight categories a coherent clinical partition, or a mix of note sections and functions?
2. Which categories overlap by design, and does multi-label membership help or hurt?
3. Should each record have exactly one primary bucket? If yes, which bucket wins for overlapping cases?
4. Is `action_bearing` a content category or a flag on records that also belong to workup/medication?
5. Is `context` a real category or a failure bucket?
6. Is `baseline_comparator` separate from `current_event` and `neuro_history`, or a modifier?
7. What is the minimum category set that still guarantees coverage of:
   - current events and chronology;
   - baseline comparator;
   - prior neurologic/seizure history;
   - family history;
   - medications/supplements;
   - current exam;
   - workup/results;
   - management actions;
   - relevant context?
8. If you would replace the eight, give exact bucket names and definitions.
9. How would you test the bucket set with small synthetic fixtures, not model output?
10. Would you drop the census entirely and use a different coverage mechanism? Defend why.

## Constraints

- no new runtime stage unless evidence demands it;
- record IDs only; no selectors or copied text;
- no diagnosis/problem identity/role/section in the census;
- source packet remains canonical;
- no same-model validator;
- one or two Ask turns, not a micro-pipeline;
- prefer deletion/simplification over new ontology.

## Deliverable

A one-page decision:

1. keep the eight, revise them, collapse them, or drop the census;
2. exact recommended buckets and definitions;
3. one-primary vs multi-label rule;
4. how to handle action records that also belong to workup/medication;
5. minimum test fixtures and pass criteria;
6. what to delete or defer;
7. biggest risk and smallest mitigation.

Challenge the design where it would cause the wrong note, not where the wording is merely different.
