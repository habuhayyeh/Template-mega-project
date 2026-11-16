# Coverage 6+2 minimal test

Use this in a fresh Ask turn with the packet pasted between the packet markers. No definitions, no extra
rules. This tests whether the model can emit all eight category names.

---

BEGIN COVERAGE INSTRUCTIONS

You are the coverage stage. Read the complete packet below. Then copy all eight lines in the template,
replacing only the `<IDs or NONE>` placeholders. Do not skip a line. Do not output anything else.

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
