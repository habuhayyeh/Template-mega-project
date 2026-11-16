# Coverage prompt — 6 primary buckets + 2 flags

Use this in a fresh Ask turn. Paste the Scribe packet between the packet markers.

---

BEGIN COVERAGE INSTRUCTIONS

You are the coverage stage of a neurology note pipeline.

Read the complete packet below before producing output. The packet is the only source of record IDs.

This turn produces a record-ID census only. Do not synthesize. Do not output problems, units, actions,
unresolved records, note sections, or prose.

If the packet is absent or unreadable, return only:

```text
@@COVERAGE_ERROR;;NO_PACKET
@@END
```

and stop.

PRIMARY BUCKETS

Every record gets one primary bucket by default.

- `current_episode_records` — current symptoms/events: phenotype, onset, timing, recurrence, progression,
  triggers, associated features, current-event chronology. Do not put consultation, testing, treatment or
  diagnostic reasoning here merely because it happened during the episode.
- `background_records` — positively identified prior neurologic disease/events, baseline phenotype/function,
  family neurologic history, relevant social/exposure context, and relevant non-neurologic history. Never a
  fallback for material that fits nowhere else.
- `medication_records` — home/recent medications, supplements, prior medication exposure or nonexposure,
  and medication treatment/change records.
- `exam_records` — clinician-observed examination findings, including materially relevant earlier or serial
  examinations.
- `investigation_records` — laboratory, imaging, EEG/EMG, monitoring, or other diagnostic investigation
  records: orders, status, completion, results.
- `reasoning_records` — explicit source-stated diagnosis, differential, causal interpretation, or clinician
  reasoning. Raw findings and management actions do not enter merely because they support reasoning.

FLAGS

Flags are properties, not competing primary buckets. They may overlap any primary bucket.

- `action_records` — records containing an explicit management decision, directive, execution state,
  patient response, counseling, referral/follow-up, level-of-care action, or medication/investigation
  action.
- `baseline_comparator_records` — records explicitly establishing a baseline/prior pattern or comparing the
  current episode with baseline/prior events.

CLASSIFICATION RULES

- One primary bucket per record by default.
- `action_records` and `baseline_comparator_records` may freely overlap any primary bucket.
- A record may receive more than one primary bucket only when the literal record contains multiple
  independent semantic payloads that would remain separate facts if split.
- A record whose only clinically relevant content is a management action gets **zero primary buckets plus
  `action_records`**. Do not force it into `background_records`.
- A pure consult/logistics record with no independent clinical content may be left uncensused.
- Do not classify by future note section, problem identity, diagnosis, role, causality, or action state.
- Do not invent an ID. Do not substitute a clinician question for a separate answer when the answer exists.

BOUNDARY EXAMPLES

- “Neurology evaluated the patient” -> not `current_episode_records`; uncensused if no independent content.
- “Ship medical tested and monitored” -> `investigation_records` + `action_records`.
- “Levetiracetam started” -> `medication_records` + `action_records`.
- “Longstanding brief staring at baseline” -> `background_records` + `baseline_comparator_records`.
- “Today’s spell was longer than usual” -> `current_episode_records` + `baseline_comparator_records`.
- “No prior antiseizure medication” -> `medication_records`.
- “Semiology favors syncope” -> `reasoning_records`.
- “Counseled on driving restriction” -> `action_records` only.
- “Admit for workup” -> `action_records` only.

OUTPUT

Use `;;` between fields. Use commas between IDs. No spaces inside ID lists. Do not use `|`.

Emit exactly these eight records, in this order. Do not skip a line.

```text
BEGIN COVERAGE OUTPUT

@@COV;;current_episode_records;;<IDs or NONE>
@@COV;;background_records;;<IDs or NONE>
@@COV;;medication_records;;<IDs or NONE>
@@COV;;exam_records;;<IDs or NONE>
@@COV;;investigation_records;;<IDs or NONE>
@@COV;;reasoning_records;;<IDs or NONE>
@@COV;;action_records;;<IDs or NONE>
@@COV;;baseline_comparator_records;;<IDs or NONE>
@@END

END COVERAGE OUTPUT
```

- Use NONE when a bucket has no material.
- Do not output a second `@@END`.
- Do not output anything outside the output block.
- Stop after `END COVERAGE OUTPUT`.

FINAL CHECK

1. exactly eight `@@COV` lines;
2. all eight bucket names appear once, in the order shown;
3. every ID exists in the packet;
4. IDs are comma-separated with no spaces;
5. fields use `;;` and no `|` appears;
6. every record has at most one primary bucket, except the compound-record exception;
7. action-only records appear in `action_records`, not `background_records`;
8. no synthesis record appears;
9. exactly one `@@END`.

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
