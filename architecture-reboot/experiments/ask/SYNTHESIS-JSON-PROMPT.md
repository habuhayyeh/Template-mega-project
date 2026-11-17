# Synthesis JSON prompt â€” real packet

Use this in a fresh Ask turn. Attach the Scribe packet and paste the frozen coverage JSON below the prompt.

---

BEGIN SYNTHESIS INSTRUCTIONS

You are the clinical synthesis stage. The attached Scribe packet is canonical. The coverage JSON is frozen.
Do not regenerate, modify or extend coverage.

Return exactly one JSON object. No prose, no Markdown, no code fence, no `@@` records.

Shape:

{
  "problems": [],
  "units": [],
  "actions": [],
  "unresolved": []
}

PROBLEM FIELDS

Each problem:

{
  "id": "P001",
  "role": "PRIMARY | BACKGROUND | unresolved",
  "label": "short problem label",
  "evidence": ["record IDs"],
  "counterevidence": ["record IDs"],
  "contains": ["problem handles or short labels"],
  "separate_from": ["problem handles"],
  "order": 1
}

Create a separate problem only when it has independent neurologic identity or its own current assessment
question/status. Baseline/history/context stays under the relevant problem.

UNIT FIELDS

Each unit:

{
  "id": "CU001",
  "type": "current_event | baseline_comparator | neuro_history | medication_context | exam | workup | context",
  "label": "one referent, one clinical state",
  "source_records": ["record IDs"],
  "chronology": "short chronology or NONE",
  "problem": "problem handle or nonproblem",
  "order": 2
}

Split patient vs family history, medication vs supplements, outside vs current vs pending workup, distinct
events, and assessment vs management.

ACTION FIELDS

Each action:

{
  "id": "AV001",
  "source_records": ["record IDs"],
  "target": "source-local target",
  "wording": "source-qualified wording",
  "owner": "problem handle or nonproblem",
  "unresolved": null,
  "order": 3
}

Only management actions: tests, treatments, consults, disposition, precautions, counseling. Do not create an
action for reasoning, assessment or result status alone. Every action-bearing record needs an action or an
unresolved entry.

UNRESOLVED FIELDS

Each unresolved:

{
  "id": "X001",
  "source_records": ["record IDs"],
  "topic": "short topic",
  "issue": "short issue",
  "order": 4
}

RULES

- Use only record IDs listed in the frozen coverage, except `NONE` in an unresolved entry.
- Do not invent an action. Do not upgrade a plan or recommendation to an order or performance.
- Do not turn silence into a result.
- Do not use "ordered" or "recommended" unless the cited source explicitly says so.
- Do not promote a mediated report to direct observation.
- Assign unique integer `order` values across all problems, units, actions and unresolved, ascending.
- Keep labels short and source-faithful.
- No coverage records. No note text.

FINAL CHECK

1. exactly one JSON object;
2. arrays for problems, units, actions, unresolved;
3. every source ID appears in the coverage JSON;
4. every problem has all seven fields plus order;
5. every unit has all six fields plus order;
6. every action has all six fields plus order;
7. every unresolved has all four fields plus order;
8. unique numeric order values;
9. no prose, code fence, `@@`, `;;`, or Markdown table.

If the attached packet is unreadable, return only:

{"error":"NO_PACKET"}

END SYNTHESIS INSTRUCTIONS

BEGIN FROZEN COVERAGE

<paste the accepted coverage JSON here>

END FROZEN COVERAGE

