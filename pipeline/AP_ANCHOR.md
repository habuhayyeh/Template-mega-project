# A/P FORMAT — ANCHOR AND STRUCTURE

**Authority:** the example below. Where a description and the example disagree, the example wins.
**Source:** supplied by the signer, 2026-11-14, with three corrections applied at their direction (see changelog).

---

## The example

```text
//First-time seizure, generalized, related to alcohol withdrawal, returned to neurologic baseline.

- witnessed abrupt loss of consciousness with tonic stiffening followed by bilateral rhythmic shaking for ~90 seconds, lateral tongue bite, and ~20 minutes of postictal confusion.
- No prior seizures.
- Drinks heavily daily; last drink ~18 hours before the event after reducing intake.
- CT head without acute abnormality; glucose and sodium were normal.

Plan:

- EEG
- MRI B not indicated, no focal deficit, patient already back to baseline.
- No indication to start ASMs
- CIWA protocol per primary team
- Seizure precautions and driving restriction counseling
```

**Changelog.** At the signer's direction: `Returned` → `returned` (the capital was not a separator). The clause `no focal neurological deficit` was removed from the `MRI B` bullet as an artefact — it repeated `no focal deficit`.

2026-11-14, at the signer's direction after reviewing two of their notes: the status element is conditional and is the patient's condition, never a duration or a study's state; a level-of-care change leads the plan, above the buckets.

---

## STRUCTURE

```text
//<claim>, <descriptor>, <descriptor>[, <status>].

- <defining semiology or presenting feature>
- <pertinent positives and negatives>
- <risk factors and context>
- <decisive results>
- <reasoning>                                    optional, always last of the bullets

Plan:

- <investigations>
- <medications>
- <everything else>
- <follow-up>                                    when the encounter has a follow-up
```

### The problem line

Three elements, comma-joined, one line, terminal period:

1. **claim** — the formulation
2. **descriptors** — subtype, laterality, severity, tempo, and short stated cause
3. **status** — a short phrase, not a sentence

Status examples: `returned to neurologic baseline`, `resolved after repositioning`, `no residual deficit`, `unchanged`, `improved`.

**The status is the patient's condition, and appears only when the record states it.** A duration (`postictal confusion lasting an hour`), a study's state (`pending MRI`), or a further description of the finding is not a status. When the record states the condition as its own sentence — `Returned to neurologic baseline without focal deficit.` — that sentence stays a bullet and the line ends at the cause.

### Where descriptors come from

**Descriptors are recorded with the claim, not searched for later.** The problem line is built from two Handoff fields only: `CLAIM` and `COURSE`.

A qualifier belongs on the line only if it is already inside the Handoff's `CLAIM`. A qualifier that exists only in `EVIDENCE` — laterality known from an examination manoeuvre, severity known from a scale, a subtype known from imaging — stays in the evidence bullet and is not promoted into the line.

That is the noise control: no assembly-time retrieval, no cross-field promotion.

### Evidence and reasoning bullets

Plain `-` items, no heading.

Order: defining semiology → pertinent positives and negatives → risk factors and context → decisive results.

A reasoning bullet is used only when the Handoff states reasoning — a `favored over`, a stated basis, a why. Same `-` form, last of the bullets, omitted when the Handoff states none. Never write a reasoning bullet to explain a formulation the clinician did not explain.

### Plan buckets

Strict order. Inside a bucket, keep the order the Handoff gives.

**A change in level of care goes first, above the buckets.** Admission, ICU, transfer, discharge — the decision that sets where the patient is outranks the rest of the plan.

1. **Investigations** — ordered, requested, or explicitly not indicated
2. **Medications** — started, continued, held, stopped, or explicitly not indicated
3. **Everything else** — protocols, precautions, referrals, counseling
4. **Follow-up** — clinic interval, return precautions, who reviews

A negative decision stays in its bucket: `MRI B not indicated` is an investigation; `No indication to start ASMs` is a medication.

---

## Settled

| Item | Decision |
|---|---|
| Capital `R` | lower case; not a separator |
| `no focal neurological deficit` | artefact, removed; the no-duplication rule stands |
| Reasoning | a bullet, same form as evidence, last among bullets |
| Follow-up | last plan bucket, present only when the encounter has one |
| Descriptor provenance | from `CLAIM` only — never imported from `EVIDENCE` |
| Cause — both sources | `CLAIM`'s own cause and a separate `ETIOLOGY` both contribute to the line |

## Cause: both contribute

The claim's own short cause stays where the claim states it. The `ETIOLOGY` content is appended before the status. Where the `ETIOLOGY` is the fuller statement of a cause already named in the claim, the line carries the fuller form once — the phrase is not repeated twice in one line.

If literal repetition of the same cause is wanted, say so; that is not what this rule produces.

---

## Still open

None. `O1` is settled above.

