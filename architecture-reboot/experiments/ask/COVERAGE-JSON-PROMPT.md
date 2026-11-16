# Coverage prompt — JSON only

Use this in a fresh Ask turn with the complete Scribe packet pasted after the prompt.

---

BEGIN COVERAGE INSTRUCTIONS

You are the coverage stage of a neurology note pipeline.

Read the complete Scribe packet below before producing output.

Return exactly one JSON object. No prose, no Markdown, no code fence, no `@@` records, no `;;` fields.

The object must have exactly this shape:

```json
{
  "coverage": {
    "current_event_records": [],
    "background_records": [],
    "medication_records": [],
    "exam_records": [],
    "workup_records": [],
    "reasoning_records": [],
    "action_records": [],
    "baseline_comparator_records": []
  }
}
```

Fill each array with source record IDs. Use an empty array when the bucket has no material. Use only IDs
that appear in the packet. Do not include source text, selectors, problem identity, diagnosis, role,
causality, action state, note section, or prose.

CATEGORY RULES

- `current_event_records`: event descriptions only — current symptoms/events, semiology, onset, timing,
  recurrence, progression, triggers, associated features, current-event chronology. Do not include
  consultation, testing, treatment or diagnostic reasoning merely because it occurred during the episode.
- `background_records`: prior neurologic disease/events, baseline patterns/function, family neurologic
  history, relevant social/exposure or non-neurologic history. Never use this as a fallback.
- `medication_records`: home/recent medications, supplements, prior exposure or nonexposure, medication
  treatment/change records.
- `exam_records`: clinician-observed examination findings, including relevant serial exams.
- `workup_records`: needed, ordered, completed, pending and resulted investigations.
- `reasoning_records`: explicit source diagnosis, differential, causal interpretation or clinician
  reasoning. Not raw findings or management actions.
- `action_records`: explicit management decision, directive, execution, response, counseling, referral,
  disposition, medication or investigation action.
- `baseline_comparator_records`: explicit baseline/prior pattern or current-vs-baseline comparison.

CLASSIFICATION RULES

- One primary bucket per record by default.
- `action_records` and `baseline_comparator_records` may overlap any primary bucket.
- A record may have more than one primary bucket only when the literal record contains multiple independent
  semantic payloads that would remain separate facts if split.
- A record whose only clinically relevant content is a management action gets zero primary buckets plus
  `action_records`. Do not put it in `background_records`.
- A pure consult/logistics record with no independent clinical content may be left out.
- Do not classify by future note section, problem identity, diagnosis, role, causality or action state.
- Do not invent an ID.
- Do not substitute a clinician question for a separate answer when the answer exists.

BOUNDARY EXAMPLES

- “Neurology evaluated the patient” -> no bucket unless it contains independent clinical content; if an
  action is stated, `action_records`.
- “Ship medical tested and monitored” -> `workup_records` + `action_records`.
- “Levetiracetam started” -> `medication_records` + `action_records`.
- “Longstanding brief staring at baseline” -> `background_records` + `baseline_comparator_records`.
- “Today’s spell was longer than usual” -> `current_event_records` + `baseline_comparator_records`.
- “No prior antiseizure medication” -> `medication_records`.
- “Semiology favors syncope” -> `reasoning_records`.
- “Counseled on driving restriction” -> `action_records` only.
- “Admit for workup” -> `action_records` only.

FINAL CHECK

1. exactly one JSON object;
2. exactly eight `coverage` keys, no extras;
3. every value is an array of ID strings;
4. every ID exists in the packet;
5. no prose or code fence;
6. no `@@`, `;;`, or Markdown table;
7. no synthesis decisions.

If the packet is absent or unreadable, return only:

```json
{"error":"NO_PACKET"}
```

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
