# Coverage-only prompt V2 — explicit begin/end boundaries

Use this as the **only** message in a fresh Ask turn. Paste the Scribe packet between the packet markers.

---

===== BEGIN COVERAGE INSTRUCTIONS =====

You are the coverage stage of a neurology note pipeline.

READ GATE

1. Read every line from `BEGIN COVERAGE INSTRUCTIONS` through `END COVERAGE INSTRUCTIONS`.
2. Read every line from `BEGIN SCRIBE PACKET` through `END SCRIBE PACKET`.
3. Do not generate, stream or emit anything until you have read `END SCRIBE PACKET`.
4. Do not emit analysis, reasoning, progress text or partial output.
5. After `END SCRIBE PACKET`, execute this instruction once.
6. If any earlier prompt or saved instruction conflicts with this block, this block wins.

SCOPE

This turn is coverage only. Do not synthesize. Do not output problems, units, actions, unresolved
records, note sections, or prose.

The Scribe packet is canonical. Every source record has a stable ID. Do not rewrite, merge, delete or
replace it.

If the packet is absent or unreadable, return only:

```text
===== BEGIN COVERAGE OUTPUT =====
@@COVERAGE_ERROR;;NO_PACKET
===== END COVERAGE OUTPUT =====
```

and stop.

COVERAGE OUTPUT

Return exactly eight `@@COV` records, in this order, between the output markers:

```text
===== BEGIN COVERAGE OUTPUT =====
@@COV;;current_event_records;;<IDs or NONE>
@@COV;;baseline_comparator_records;;<IDs or NONE>
@@COV;;neuro_history_records;;<IDs or NONE>
@@COV;;medication_context_records;;<IDs or NONE>
@@COV;;exam_records;;<IDs or NONE>
@@COV;;workup_records;;<IDs or NONE>
@@COV;;action_bearing_records;;<IDs or NONE>
@@COV;;context_records;;<IDs or NONE>
@@END
===== END COVERAGE OUTPUT =====
```

The first coverage line must be `@@COV;;current_event_records`. If the packet contains any current event,
episode, spell, collapse or recurrent-event record, that line must not be NONE.

RULES

- record IDs only; no source text or selectors;
- use commas between IDs;
- use `;;` between fields;
- no `|`;
- no polarity, certainty, diagnosis, problem identity, role, causality, action state or note section in the
  census;
- family neurologic history goes under neuro_history or context;
- medications and supplements go under medication_context;
- include current treatment/continuation records under medication_context as well as action_bearing;
- tests, results and result availability go under workup;
- management actions go under action_bearing: tests, treatments, consults, disposition, precautions,
  counseling; include a record there even when it also belongs under workup or medication;
- exclude records containing only reasoning, assessment statements or result/status descriptions from
  action_bearing;
- if uncertain whether a record is a management action, include it in action_bearing and context;
- if uncertain between other categories, include it in context;
- never invent an ID;
- never substitute a clinician question for a separate answer record when the answer exists.

FINAL CHECK BEFORE EMITTING

1. exactly eight `@@COV` lines;
2. in the listed order;
3. first line is current_event_records;
4. every ID exists in the packet;
5. IDs are comma-separated;
6. fields use `;;`, no `|`;
7. exactly one coverage block;
8. exactly one `@@END`;
9. no synthesis record appears;
10. nothing appears outside the output markers.

Return only the output block. Stop after `END COVERAGE OUTPUT`.

===== END COVERAGE INSTRUCTIONS =====

===== BEGIN SCRIBE PACKET =====
<paste the complete Scribe packet here>
===== END SCRIBE PACKET =====
