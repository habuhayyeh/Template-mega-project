# Coverage minimal V2 — short template plus category rules

Use this in a fresh Ask turn with the Scribe packet pasted between the packet markers.

---

BEGIN COVERAGE INSTRUCTIONS

You are the coverage stage. Read the full packet below. Then copy all eight lines in the template, replacing
only the `<IDs or NONE>` placeholders. Do not skip a line. Do not output anything else.

BEGIN COVERAGE OUTPUT

@@COV;;current_event_records;;<IDs or NONE>
@@COV;;baseline_comparator_records;;<IDs or NONE>
@@COV;;neuro_history_records;;<IDs or NONE>
@@COV;;medication_context_records;;<IDs or NONE>
@@COV;;exam_records;;<IDs or NONE>
@@COV;;workup_records;;<IDs or NONE>
@@COV;;action_bearing_records;;<IDs or NONE>
@@COV;;context_records;;<IDs or NONE>
@@END

END COVERAGE OUTPUT

CATEGORY RULES

- current_event_records: records describing current events, episodes, spells, collapses or recurrent events.
- baseline_comparator_records: prior/baseline comparator symptoms.
- neuro_history_records: prior neurologic/seizure history and family neurologic history.
- medication_context_records: medications and supplements, including current treatment/continuation.
- exam_records: current neurologic exam.
- workup_records: tests, results and result-availability statements.
- action_bearing_records: management actions only — tests, treatments, consults, disposition, precautions,
  counseling. Include a record here even if it also belongs under workup or medication. Exclude records
  containing only reasoning, assessment statements or result/status descriptions.
- context_records: relevant context not better placed elsewhere.

A record may appear in more than one category when genuinely useful.

FORMAT

- record IDs only; no source text or selectors;
- commas between IDs;
- `;;` between fields; no `|`;
- exactly eight `@@COV` lines, in the order shown;
- first line must be current_event_records;
- exactly one `@@END`.

Do not synthesize. Do not output problems, units, actions or unresolved records.

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
