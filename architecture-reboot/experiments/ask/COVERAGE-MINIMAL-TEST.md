# Coverage minimal test — isolate the omission

Use this in a fresh Ask turn with the Scribe packet pasted between the markers. It has no rules beyond the
output template.

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

Do not synthesize. Do not output problems, units, actions or unresolved records.

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
