# MODULE 06 — SECTION ROUTE

## PURPOSE

Route the frozen object substrate into the note-body sections.

It selects and assigns. It does not write, compress, reorder, or resolve duplicates. One primary home per object, with explicit reuse where a proposition genuinely serves two sections.

---

## INPUT

Exactly the frozen object table:

```text
O1 | DEMOGRAPHIC | 68F | [A, Neurology consult, 2026-11-14]
O22 | DIAGNOSTIC_FORMULATION | post-stroke seizure … | [A, Neurology consult, 2026-11-14]
O26 | OBSERVATION | no fever | [A, Neurology consult, 2026-11-14] | EXAMINED
```

`OBSERVATION` and `COURSE` objects carry a fifth field, `EVIDENCE_MODE`. The other four kinds do not.

It does **not** consume the `02` allocation, the `03`/`03V` ledger, or the A/P Handoff. The two branches are independent consumers of the same validated substrate.

---

## EVIDENCE_MODE

`REPORTED`, `EXAMINED`, `TEST_RESULT`, `CLINICIAN_COMMENT`, or `UNKNOWN`. It records how the proposition was established. **It never names a section.**

- `REPORTED` does not mean `HPI`. A report that shapes the presenting problem and its chronology is `HPI`; a report that is background review is `ROS`, or the history section its subject belongs to. A chronic concern already under neurologic care is history, not review of systems.
- `EXAMINED` supports `EXAM`.
- `TEST_RESULT` supports `WORKUP` when the test belongs to this encounter. A result carried in from a prior record belongs with the finding it describes, in `NEURO_HISTORY`.
- `CLINICIAN_COMMENT` is the clinician's own framing. It never enters `HPI`, `ROS`, or a history section.
- `UNKNOWN` is routed from the proposition alone.

---

## OUTPUT

An ID ledger only:

```text
O1 → HPI
O3 → HPI
O22 → DISCARD: AP_ONLY
REUSE: O3 → REASON_FOR_CONSULT, distinct function: presenting problem

UNACCOUNTED_IDS: none
MULTIPLY_ASSIGNED_IDS: none
ACCOUNTING: 60/60
```

- one line per object, ascending by ID, no gaps, no repeats;
- `REUSE` lines after the ledger;
- the three validation lines last.

No text, no prose, no section headings, no note writing.

---

## DESTINATIONS

`REASON_FOR_CONSULT`, `HPI`, `ROS`, `NEURO_HISTORY`, `OTHER_PMH`, `SOCIAL`, `FAMILY`, `MEDICATIONS`, `EXAM`, `WORKUP`, or `DISCARD: <reason>`.

---

## ONE PRIMARY HOME, EXPLICIT REUSE

Every retained object has exactly one primary destination. A second section use requires its own line:

```text
REUSE: O3 → REASON_FOR_CONSULT, distinct function: presenting problem
```

The function must be genuinely different from the primary one. Silent multiple mapping is not permitted, and a `REUSE` never replaces the assignment line.

For presenting-problem objects, prefer primary `HPI` and reuse into `REASON_FOR_CONSULT`. The reason for consult is one line drawn from the same proposition; it is not a second copy of the story.

Two reuses are load-bearing rather than optional:

- the prior disease that frames the encounter is reused into `HPI` so the identifying clause can name it;
- a concern the source explicitly sets aside as not current is not `HPI` and not `REASON_FOR_CONSULT`; it stays where its own function puts it.

---

## DISCARD REASONS — CLOSED SET

- `AP_ONLY` — formulation, etiology, plan action, order, or recommendation made in this encounter, or clinician framing, that belongs to the A/P branch and never to the note body. A recommendation carried in from a prior record is history and stays with the problem it belongs to.
- `IRRELEVANT_TO_RETAINED_SECTIONS` — a fact no section of this note uses. Not a substitute for `AP_ONLY` when the material belongs to the plan or the formulation

Do **not** use `EXACT_DUPLICATE_OF`. `06` does not deduplicate.

---

## HIGH RECALL, NO CONCISION

Where several objects carry the same clinical fact — from different sources or split by atomicity — route them to their proper sections and let `07` compress within the section. Dropping one here would remove the writer's ability to choose the better wording, and would recreate the optional-dedup nondeterminism already observed in `04`.

---

## STRUCTURAL RULES

These are fixed and are checked mechanically:

- `DEMOGRAPHIC` → `HPI`
- `DIAGNOSTIC_FORMULATION` → `DISCARD: AP_ONLY`
- `ETIOLOGY` → `DISCARD: AP_ONLY`

Nothing else routes from kind.

---

## SEMANTIC ROUTING

Everything else is a judgement about the proposition's function, not its kind and not its provenance letter.

| Function | Section |
|---|---|
| presenting event, onset, evolution, trigger; important negatives that shape the presenting problem | `HPI` |
| patient-reported positive or negative not already in the HPI or another history section | `ROS` |
| established neurologic disease, deficit, or prior study-defined finding. Not a current symptom, a clinician hedge, or a reported baseline | `NEURO_HISTORY` |
| established non-neurologic disease | `OTHER_PMH` |
| living, work, substances, exposures, functional baseline | `SOCIAL` |
| family disease history | `FAMILY` |
| the active home regimen — drug, dose, route, frequency — and a recently stopped drug that still bears on the presentation. A status change made this encounter (held, stopped, resumed, started in hospital) is `AP_ONLY` | `MEDICATIONS` |
| observed or examined finding, including assessed negatives such as afebrile, no nuchal rigidity, no focal deficit | `EXAM` |
| completed test or result. A treatment, order, restriction, or recommendation is never `WORKUP` | `WORKUP` |

Kind alone does not decide these. A `COURSE` object may be presenting chronology or may belong to a problem's history — `propranolol stopped 2025-03` is not HPI. A `MANAGEMENT` object naming a drug may be a medication-list fact or a plan action — `Apixaban to resume once MRI excludes hemorrhage` is a plan, not a medication entry. An `OBSERVATION` may be story, negative, history, social, exam, or result.

Provenance stays attached and shapes attribution and current-versus-historical reading. It does not choose the section.

---

## WHAT THIS MODULE DOES NOT DO

- no chronological ordering — `07` orders the HPI
- no deduplication or deletion of restatements — `07` compresses within a section
- no section titles, headers, or prose
- no A/P content
