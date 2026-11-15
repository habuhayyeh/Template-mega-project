# MODULE 02 — ALLOCATE

## PURPOSE

Map already-decomposed clinical objects into the note functions:

- CLAIM
- ETIOLOGY [optional]
- EVIDENCE
- COURSE
- MANAGEMENT

This module operates **only** on objects produced by MODULE 01 — DECOMPOSE.

Do not allocate directly from the original source prose.

Copy each object's text into the field unchanged. Allocation adds no words and removes none.

This module does not perform final note compression, prioritization, or polished rewriting.

---

## 1. CLAIM

Use CLAIM for the current diagnostic formulation.

**Record the CLAIM in assembly order: the formulation, then its own qualifiers, then any short stated cause.**

Keep a qualifier inline and verbatim when the source states it as part of the formulation — subtype, laterality, severity, tempo, short cause. Example: `first-time generalized seizure, probably related to alcohol withdrawal`.

Do not move a qualifier into CLAIM from an examination finding, an imaging result, or a scale. A laterality known only from a manoeuvre, or a severity known only from a score, stays in EVIDENCE. The downstream writer assembles the A/P problem line from the CLAIM as recorded; a qualifier that is not in the CLAIM does not reach that line.

CLAIM may natively encode complex diagnostic relationships.

Examples:

- `acute left MCA ischemic stroke`
- `focal motor seizure favored over recurrent ischemia`
- `TIA vs focal seizure remains unresolved`
- `cervical stenosis present but insufficient to explain the weakness`
- `CIDP exacerbation`

Do not split one weighted or competing diagnostic formulation into multiple unrelated claims unless they are truly independent problems.

CLAIM holds the formulation this note works from. A rejected alternative may appear inside that formulation — `X favored over Y` — but never as a second CLAIM entry. If it will not fold in, it goes to EVIDENCE with its rejection intact.

Historical diagnoses do not automatically become CLAIM.

Example:

`History of focal epilepsy`

usually serves as EVIDENCE/context unless focal epilepsy itself is the current problem being assessed.

---

## 2. ETIOLOGY

ETIOLOGY is optional.

Use it only when a causal mechanism or attribution adds independent clinical meaning.

Examples:

- `cardioembolic mechanism favored in the setting of atrial fibrillation`
- `seizure likely acute symptomatic from cortical infarction`

Preserve certainty.

Do not invent an etiology.
Omit ETIOLOGY when unknown, redundant, or not useful.

---

## 3. EVIDENCE

Use EVIDENCE for observations and results that establish, support, oppose, or contextualize the CLAIM or ETIOLOGY.

Examples:

- presenting symptoms or semiology
- examination findings
- imaging results
- EEG/EMG/CSF/laboratory results
- relevant historical diagnostic facts
- diagnostic support or opposition

Examples:

- `aphasia and right arm weakness`
- `CTA showed left M2 occlusion`
- `MRI confirmed acute left MCA infarct`
- `prior EMG showed acquired demyelinating neuropathy`

A diagnostic test **result** belongs in EVIDENCE.

A diagnostic test **order/recommendation/pending workup** belongs in MANAGEMENT.

---

## 4. COURSE

Use COURSE for temporal evolution and the patient's current clinical or functional state.

**Record a trajectory only when a source states it. The list below is vocabulary, not a menu — never select a word from it to fill the field.** If no source states the trajectory or the current state, omit COURSE.

Never write `stable`, `resolved`, `unchanged`, `improved`, or `back to baseline` on the strength of a normal examination finding, a nursing observation of orientation, or the absence of a documented deterioration. An orientation described as "person and place" is not a return to baseline. A lesion not re-imaged is not stable.

An assertion of absence is also a trajectory, and needs a sentence that asserts it. `No recurrent events` is not established by an interval in which nothing was recorded. That is absence of documentation, not documented absence.

A formulation that appears only in a prior note carries its source, name, and date verbatim — the full provenance marker — and is not written as the current CLAIM unless the current clinician adopts it. `Probable vascular dementia [D, prior neurology, 2025-06]` is evidence or attributed context; `probable vascular dementia` in CLAIM is the prior clinician's conclusion presented as this one's. The provenance marker is carried opaquely; `02` does not infer, rename, or normalize it.

Examples:

- abrupt onset
- progressive over 3 weeks
- improving
- worsening
- persistent
- recurrent
- resolved
- current residual deficit
- current function
- change from an earlier state

Examples:

- `abrupt onset`
- `aphasia improved substantially`
- `mild right arm weakness persisted`
- `strength improved from 2/5 to 4+/5`
- `currently requires supervision for ambulation`

When a finding is both diagnostically important and part of the trajectory, avoid copying the same full statement into both EVIDENCE and COURSE.

Prefer:

- EVIDENCE: `aphasia and right arm weakness`
- COURSE: `abrupt onset; aphasia improved, mild right arm weakness persisted`

Do not infer causation from chronology alone.

---

## 5. MANAGEMENT

Use MANAGEMENT for all management actions and decisions, regardless of whether they are completed, active, future, negative, deferred, or conditional.

Includes:

- treatment given
- procedure performed
- treatment considered but not given
- treatment held or withheld
- intervention determined not indicated
- diagnostic workup ordered
- consultation
- referral
- recommendation
- disposition action
- surveillance
- follow-up
- pending authorization
- deferred action
- conditional rescue treatment

Preserve the action state explicitly when it matters.

Examples:

- `IV thrombolysis considered but withheld because of recent apixaban use`
- `mechanical thrombectomy performed`
- `apixaban held`
- `MRI ordered`
- `no acute neurosurgical intervention indicated`
- `rehab recommended`
- `referral submitted; authorization pending`
- `repeat CTA recommended in 12 months`

Do not compute an obligation from a recommendation's interval. A 2024 recommendation to image in two years is a dated recommendation, not a current obligation. `Due` and `overdue` are arithmetic, and the arithmetic is not in the source. Carry the date and stop.

Keep management rationale attached when it explains the decision.

Example:

`IV thrombolysis considered but withheld because of recent apixaban use`

should remain one MANAGEMENT relationship.

---

## 6. ONE OBJECT MAY SERVE MORE THAN ONE FUNCTION

Do not require every decomposed object to map to exactly one note function.

A clinical observation may legitimately contribute to both:

- EVIDENCE
- COURSE

Example:

`Right arm weakness improved from 2/5 to 4+/5`

contains:

- a neurologic finding relevant to EVIDENCE
- a trajectory relevant to COURSE

However, do not mechanically duplicate the entire statement across fields.

Map the information where it is most useful and preserve the distinct function.

---

## 7. ALLOCATE EVERY OBJECT

`02` allocates every object produced by `01`. It does not perform relevance selection or omission. Selection belongs exclusively to `03`.

Provenance, uncertainty, conditionality, and relationships are preserved through allocation.

---

## 8. ALLOCATION RULES

Apply these rules after decomposition:

Allocate every object once. Do not group objects into problems, do not name a problem, and do not decide what belongs with what — `03` does all of that, and doing it here hides the loss.

MANAGEMENT holds what this encounter does: ordered, requested, started, stopped, held, resumed, referred, continued, admitted. A diagnosis the patient carries and the medication they take for it are EVIDENCE, not management — `Atrial fibrillation on apixaban, held since admission` states the patient's situation and stays in EVIDENCE, with the held state intact in its wording.

1. Diagnostic formulation → CLAIM.
2. Useful causal mechanism → ETIOLOGY.
3. Observation/test result/supporting fact → EVIDENCE.
4. Temporal evolution/current clinical or functional state → COURSE.
5. Management action/decision/workup/referral/disposition/follow-up → MANAGEMENT.

Special cases:

- Diagnostic test RESULT → EVIDENCE.
- Diagnostic test ORDER/RECOMMENDATION/PENDING WORKUP → MANAGEMENT.
- Historical diagnosis → usually EVIDENCE/context unless it is the current diagnostic problem.
- Favored diagnosis vs alternative → one CLAIM relationship.
- Unresolved X vs Y → one CLAIM relationship.
- Management action + reason → one MANAGEMENT relationship.
- Management action + condition/dependency → one MANAGEMENT relationship.
- Current finding may contribute to EVIDENCE and COURSE, but minimize duplication.
- A `DEMOGRAPHIC` object has no A/P field. It is not allocated; it is listed under `NOT_ALLOCATED` verbatim so the omission is explicit, never silent.

---

## OUTPUT CONTRACT

Return allocated content under:

## CLAIM

## ETIOLOGY
Only if supported and useful.

## EVIDENCE

## COURSE

## MANAGEMENT

## NOT_ALLOCATED
Objects with no A/P field — `DEMOGRAPHIC`, and any object `02` cannot route to one of the five fields. Listed verbatim, with provenance. Omit this heading when empty.

Do not use:

- INTERVENTION
- STATUS
- PLAN
- TODAY

Do not produce polished final-note prose.
Do not add unsupported information.
Do not change certainty, chronology, action state, or rationale.

Nothing before the first heading and nothing after the last entry. Do not narrate the work, name the file or the stage, or report that the allocation is complete.

The next modules select and organize. `05` compresses and writes.
