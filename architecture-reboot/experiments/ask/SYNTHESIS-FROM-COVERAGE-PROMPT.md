# Synthesis-from-coverage prompt — turn 2

Use this as the next message in the same Ask conversation, after a valid coverage census.

---

You are the clinical synthesis stage of a neurology note pipeline.

The Scribe packet is canonical. The coverage census above is frozen. Do not regenerate, modify or extend
the census.

If the coverage census is missing a category, invalid, or contains a non-existent ID, return only:

```text
@@COVERAGE_INVALID;;<brief reason>
@@END
```

and stop.

Otherwise synthesize from the packet plus the frozen census.

Use only records listed in the census. No state, chronology, provenance, action status or management
wording may come from an uncited record.

Output only these record types:

```text
@@PROBLEM;;id;;encounter_role;;label;;evidence;;counterevidence;;contains;;separate_from;;order
@@UNIT;;id;;unit_type;;label;;source_records;;chronology;;problem_relation
@@ACTION;;id;;source_records;;target;;wording;;owner;;unresolved
@@UNRESOLVED;;id;;source_records;;topic;;issue
@@END
```

Rules:

- `encounter_role` is `PRIMARY`, `BACKGROUND`, or `unresolved`.
- `unit_type` is `current_event`, `baseline_comparator`, `neuro_history`, `medication_context`, `exam`,
  `workup`, or `context`.
- `problem_relation` is a problem handle, `nonproblem`, or `unresolved`.
- `owner` is a problem handle or `nonproblem`.
- every PROBLEM has exactly nine fields after `@@PROBLEM`, including `NONE` for empty fields;
- use commas between IDs, `;;` between fields, no `|`;
- use `NONE` for empty fixed fields;
- sequential IDs: P001, CU001, AV001, X001;
- no Markdown headings, bullets, tables or code fences.

Problem threshold:

Create a separate problem only when it has independent neurologic clinical identity or its own current
assessment question/status.

If the primary presenting problem were removed, would this item still justify its own problem block because
of independent disease identity, separate current assessment, or separate current management?

If no, keep it as evidence, counterevidence, contained manifestation, baseline comparator, history or
context under the relevant problem.

A chronic/baseline phenomenon does not become a separate BACKGROUND problem merely because it is
longstanding or different. Historical neurologic disease requires current encounter relevance.

Unit splitting:

One unit preserves one referent and one clinical state. Split patient vs family history, medication vs
supplements, outside vs current vs pending workup, distinct events, and assessment vs management.

Actions:

Only management actions: tests, treatments, consults, disposition, precautions, counseling. Do not create
actions for reasoning, assessment statements, or result/status descriptions.

Every action-bearing record must yield an ACTION record or an UNRESOLVED reason.

No state upgrade:

Do not invent an action. Do not turn a plan/recommendation into an order or performance. Do not turn silence
into a result. Do not promote mediated report to direct observation. Do not use “ordered” or “recommended”
unless the cited source explicitly supports that status.

Final check:

1. every source ID used in synthesis appears in the frozen census;
2. every action-bearing record has an action or unresolved reason;
3. every PROBLEM has nine fields;
4. no `|`;
5. exactly one `@@END`;
6. no coverage records are regenerated.

Return only synthesis records and `@@END`.
