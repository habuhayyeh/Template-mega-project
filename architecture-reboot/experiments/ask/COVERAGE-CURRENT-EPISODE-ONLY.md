# Coverage one category — current episode only

Use this in a fresh Ask turn with the packet pasted between the packet markers.

---

BEGIN COVERAGE INSTRUCTIONS

Read the complete packet below.

Output only one coverage record:

@@COV;;current_episode_records;;<IDs or NONE>

INCLUDE only records that describe the current event or symptom itself:

- onset, timing, duration, recurrence, progression;
- semiology: what the patient did, awareness, responsiveness, eyes, speech, motor activity;
- associated symptoms, triggers, recovery;
- witness description of the event;
- patient memory of the event;
- current-event chronology.

EXCLUDE:

- consultation/evaluation statements;
- testing, results, orders, monitoring, disposition;
- medications, treatments, supplements;
- examination findings;
- diagnostic reasoning or differential;
- baseline/prior patterns;
- family or social history;
- counseling, precautions or restrictions.

If a record contains both an event description and excluded content, include it only if the event
description is the clinically material payload.

Do not include a record merely because it occurred during the episode.

OUTPUT

BEGIN COVERAGE OUTPUT

@@COV;;current_episode_records;;<comma-separated IDs or NONE>
@@END

END COVERAGE OUTPUT

No other records. No synthesis. No commentary.

END COVERAGE INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
