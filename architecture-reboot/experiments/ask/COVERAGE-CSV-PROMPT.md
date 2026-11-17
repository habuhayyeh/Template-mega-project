# Coverage prompt — CSV only

Use this in a fresh Ask turn with the complete Scribe packet pasted after the prompt.

---

BEGIN COVERAGE INSTRUCTIONS

You are the coverage stage. Read the complete packet below.

Return exactly one CSV table with this header:

```csv
bucket,record_id
```

Emit one row per record ID. Do not quote IDs. Do not add spaces after commas.

Every one of these eight bucket names must appear at least once:

```text
current_event_records
background_records
medication_records
exam_records
workup_records
reasoning_records
action_records
baseline_comparator_records
```

If a bucket has no material, emit one row with `NONE` as the record ID.

RULES

- `current_event_records`: event descriptions only; no consult, testing, treatment or reasoning.
- `background_records`: prior neurologic disease/events, baseline, family, social/non-neurologic history.
  Never a fallback.
- `medication_records`: medications, supplements, prior exposure/nonexposure, treatment/change.
- `exam_records`: clinician-observed findings.
- `workup_records`: needed, ordered, completed, pending, resulted investigations.
- `reasoning_records`: explicit source diagnosis, differential, causal interpretation or reasoning.
- `action_records`: explicit management actions. This is a flag; it may overlap any primary bucket.
- `baseline_comparator_records`: explicit baseline/prior comparison. This is a flag; it may overlap any
  primary bucket.
- One primary bucket per record by default.
- Action-only records get `action_records` only; do not put them in `background_records`.
- IDs only, no source text, no problem identity, diagnosis, role, causality, action state or note section.
- Do not invent an ID.

FINAL CHECK

1. exactly one header row;
2. all eight bucket names appear;
3. every row has exactly two fields;
4. every ID exists in the packet or is `NONE`;
5. no prose, code fence, Markdown table, `@@`, `;;`, YAML or JSON.

If the packet is absent or unreadable, return only:

```csv
ERROR,NO_PACKET
```

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
