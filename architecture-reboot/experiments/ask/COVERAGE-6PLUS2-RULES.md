# Coverage 6+2 — minimal template plus boundary rules

Use this in a fresh Ask turn with the packet pasted between the packet markers.

---

BEGIN COVERAGE INSTRUCTIONS

You are the coverage stage. Read the complete packet below. Then copy all eight lines in the template,
replacing only the `<IDs or NONE>` placeholders. Do not skip a line. Do not output anything else.

BOUNDARY RULES

- `current_episode_records` is event descriptions only. Do not put consultation, testing, treatment or
  diagnostic reasoning here merely because it happened during the episode.
- `background_records` includes prior neurologic disease/events, baseline patterns/function, family history,
  and relevant social/non-neurologic history. A `baseline_comparator_records` flag never replaces its
  primary bucket.
- `investigation_records` includes needed, ordered, completed, pending and resulted investigations. If the
  record also states an explicit management action, add `action_records`.
- Medication treatment/start/continuation records go in `medication_records` and also get
  `action_records`.
- A record whose only clinically relevant content is counseling, disposition or another management action
  may have zero primary buckets plus `action_records`. Do not put it in `background_records`.
- One primary bucket per record by default. Flags may overlap any primary.
- Use record IDs only, commas between IDs, `;;` between fields, no `|`.

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

Do not synthesize. Do not output problems, units, actions or unresolved records.

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
