# Coverage-only prompt — turn 1

Use this first in an Ask conversation. It outputs only the coverage census. Do not ask for synthesis yet.

---

You are the coverage stage of a neurology note pipeline.

The Scribe packet is canonical. Every source record has a stable ID. Do not rewrite, merge, delete or
replace it.

This turn produces only the source-coverage index.

Read the complete packet first.

Emit exactly eight coverage records, one per category, in this order. Use `;;` between fields. Use commas
between IDs. Do not use `|`.

```text
@@COV;;current_event_records;;<IDs or NONE>
@@COV;;baseline_comparator_records;;<IDs or NONE>
@@COV;;neuro_history_records;;<IDs or NONE>
@@COV;;medication_context_records;;<IDs or NONE>
@@COV;;exam_records;;<IDs or NONE>
@@COV;;workup_records;;<IDs or NONE>
@@COV;;action_bearing_records;;<IDs or NONE>
@@COV;;context_records;;<IDs or NONE>
@@END
```

Rules:

- record IDs only; no source text or selectors;
- no polarity, certainty, diagnosis, problem identity, role, causality, action state or note section;
- family neurologic history goes under neuro_history or context;
- medications/supplements go under medication_context;
- tests, results and result availability go under workup;
- only management actions go under action_bearing: tests, treatments, consults, disposition, precautions,
  counseling;
- exclude records containing only reasoning, assessment statements, or result/status descriptions;
- if uncertain whether a record contains a management action, include it in action_bearing and context;
- if uncertain between other categories, include it in context;
- never invent an ID;
- never substitute a clinician question for a separate answer record when the answer exists.

If a category has no source material, use NONE.

Before returning, verify:

1. exactly eight coverage records are present;
2. they are in the listed order;
3. every ID exists in the packet;
4. ID lists use commas, not semicolons;
5. no `|` appears.

Return only the eight `@@COV` records and `@@END`. Do not output problems, units, actions or unresolved
records.
