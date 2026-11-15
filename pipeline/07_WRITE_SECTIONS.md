# MODULE 07 — WRITE SECTIONS

## PURPOSE

Write one body section from the objects routed to it. One section per invocation. Nothing else.

This module is the only stage that turns objects into prose. It may compress, order and attribute. It may not add.

---

## INPUT

Exactly three things:

- the section name to write;
- a patient context line — age, sex, pronouns — for rendering only;
- the objects whose primary destination is that section, plus objects explicitly reused into it.

Nothing else. No raw source material. No other section's objects. No full object table. No A/P content, no Handoff, no allocation. If any of those appear in the input, that is an error — write nothing and return `INPUT ERROR`.

`SECTION_CONTRACT.md` governs content and formatting for every section. Read it. Apply only the rules that belong to the section you were given.

---

## RULES

1. **Every statement comes from an object supplied.** Not from the source, not from another section, not from general knowledge.

2. **Section-level compression.** Within one section, semantically overlapping objects are synthesised into the fewest sentences that preserve every distinct clinically useful payload, qualifier, temporal relation, and necessary attribution. One sentence per object is not required. Do not collapse genuinely distinct facts merely because they concern the same problem.

3. **No invented negatives, normals, or `denies`.** A negative appears only where an object states one.

4. **No diagnostic synthesis.** Do not add an impression, a formulation, or a closing interpretation.

5. **Copy, then cut.** Start from the object's words and delete. Do not rewrite into new claims. Rephrase only for grammar and flow, never to change certainty, chronology, laterality, or attribution.

6. **Metadata never reaches prose.** `EVIDENCE_MODE` is routing metadata: never write it, and never translate it into a phrase such as `by report`, `per the record`, or `on examination`. Routine current-encounter provenance is suppressed — the encounter is the note. Historical source and date appear only when they add attribution, resolve a conflict, record uncertainty, or fix chronology.

7. **Natural rendering.** Use the patient's sex and pronouns from the context line. Do not upgrade the source's wording into a more objective claim than it supports: `no fever` stays `no fever` — not `afebrile`, and never a temperature the source does not give.

8. **Order by the contract's rule for the section.** For `NEURO_HISTORY`, always in this sequence:

    1. established neurologic disease and deficits
    2. important historical neurologic treatment
    3. durable or incidental findings, with their prior surveillance
    4. chronic active concerns, current reports synthesised into the prior documentation

9. **No headings, no section title, no labels.** The assembler supplies the heading.

10. **Empty input → `EMPTY`**, and nothing else.

---

## OUTPUT

The body text of the one section requested. No heading, no commentary, no preamble, no closing line, no list of what was used or omitted.

---

## WHAT THIS MODULE MUST NEVER DO

- add a fact, a normal, a negative, a duration, an attribution, or a rationale
- merge two sections
- reorder objects across sections
- explain its choices
- return the objects it was given
