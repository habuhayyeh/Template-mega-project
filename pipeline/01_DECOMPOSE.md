# MODULE 01 — DECOMPOSE

## PURPOSE

Convert source clinical prose into clinically meaningful objects and relationships.

This module does **not** write the final note.
It does **not** decide which problems deserve final inclusion.
It does **not** compress for style.
It does **not** allocate into final note fields.

Its only job is to preserve meaning while separating genuinely different clinical functions.

---

## 0. THE RULE

Objects keep the source's words. You may delete words, and you may split a sentence at its own clauses. You may not add, substitute, or reorder words.

If a meaning needs a word the source does not have, it does not become an object.

Every object carries its provenance as a three-part marker taken verbatim from the source header — `[letter, source_name, date]` — for example `[D, prior neurology, 2025-06]`. The letter is `A`, `B`, `C`, or `D`; the source name is the header's own wording (`prior neurology`, `prior radiology`, `neurology consult`, `transcript`, `ED note`); the date is the header's own date, if any. A missing name or date stays empty and is never inferred. `01` extracts provenance; it does not normalize, interpret, or rename it.

---

## 1. SPLIT, THEN CLASSIFY

Work in two steps. First identify the separable propositions in the source. Only then give each proposition a kind.

Classifying before splitting lets a phrase of one kind swallow a proposition of another — a duration eating an observation, a management clause eating a formulation.

Every sentence in the source becomes at least one object. Nothing is dropped here; deciding what matters is a later module.

### The six kinds

Apply the first definition that matches.

**`DEMOGRAPHIC`** — a patient identifier: age, sex, and other identifying facts. `68F`.

**`MANAGEMENT`** — an action, or a statement about action: treatment given, held, or stopped; a test ordered or requested; a restriction; a referral; follow-up; a medication; and a statement of how a planned test will adjudicate uncertainty (`but the MRI will tell us`). Attribution and conditionality travel with it.

**`ETIOLOGY`** — an explicit causal attribution: `scar from old stroke is most likely cause of the seizure`.

**`COURSE`** — a temporal relation only: a date anchor, a duration, a sequence, or an explicit change over time. `admitted 11/12`. A COURSE object must stand on its own — it names the subject it times (`memory difficulty worsening for a year`, `postictal confusion lasting about an hour`), never a bare fragment such as `for a year`.

**`DIAGNOSTIC_FORMULATION`** — the current clinician's interpretive judgment about this patient's diagnosis or differential, stated in `[A]` or in a clinician turn of `[B]`. `post-stroke seizure … rather than a new lesion`; `confusion today is not dementia — it's postictal`. A general remark about disease (`sometimes no cause found`) is not a formulation.

**`OBSERVATION`** — the default. Any factual content that is none of the above: symptoms, findings, test results, negatives, patient or family statements, and prior-record diagnoses. A diagnosis stated by anyone other than the current clinician is an attributed `OBSERVATION`, never a `DIAGNOSTIC_FORMULATION`.

### What follows

- `no prior seizures`, `known left MCA infarct`, `left MCA infarct` from a prior record, `progressive memory difficulty`, and `probable vascular dementia` from prior neurology are all `OBSERVATION`.
- `scar from old stroke is most likely cause` is `ETIOLOGY`.
- `sometimes no cause found` is `OBSERVATION`.
- `68F` is `DEMOGRAPHIC`; `admitted 11/12` is `COURSE`; `but the MRI will tell us` is `MANAGEMENT`.

### Atomicity

One independently useful proposition per object. Do not merge an event with its duration, a finding with a treatment response, a fact with its chronology, a preference with a counseling response, or a formulation with a test-adjudication clause.

Some lexical overlap between objects is expected. Atomicity is one proposition per object, not zero shared words.

Attribution that changes meaning belongs to the proposition: `doctor in clinic said dementia`, not `dementia`; `family's concern about memory`, not `memory concern`; `she wants to drive`, not `driving`.

---

## 2. SPLIT DIFFERENT FUNCTIONS

Split components when they perform genuinely different clinical functions.

Example:

`Neurology favored focal seizure over recurrent ischemia and increased levetiracetam.`

becomes:

- DIAGNOSTIC FORMULATION: focal seizure favored over recurrent ischemia
- MANAGEMENT: levetiracetam increased

Example:

`PT evaluated the patient, documented that she required a walker, and recommended inpatient rehabilitation.`

becomes:

- MANAGEMENT: PT evaluated the patient
- CURRENT FUNCTION: required a walker
- MANAGEMENT: recommended inpatient rehabilitation

---

## 3. PRESERVE MEANINGFUL RELATIONSHIPS

Do not split components when doing so would destroy one clinically meaningful relationship.

Preserve together:

- favored diagnosis vs less-likely alternative
- unresolved X vs Y differential
- diagnosis + necessary qualifier
- management action + action state
- management action + reason/rationale
- management action + condition/dependency
- finding + clinically necessary qualifier

Example:

`IV thrombolysis was considered but withheld because of recent apixaban use.`

remains one MANAGEMENT object containing:

- action: IV thrombolysis
- state: considered/withheld
- reason: recent apixaban use

Example:

`Focal motor seizure was favored over recurrent ischemia.`

remains one DIAGNOSTIC FORMULATION object.

---

## 4. SEPARATE FINDINGS FROM COURSE INFORMATION

When one statement contains both a clinical finding and information about its timing or evolution, split them — and make the COURSE object stand on its own by naming the subject it times.

Example:

`Abrupt aphasia and right arm weakness`

becomes:

- OBSERVATION: aphasia and right arm weakness
- COURSE: aphasia and right arm weakness, abrupt onset

Example:

`Right arm weakness improved from 2/5 to 4+/5`

becomes:

- OBSERVATION: right arm weakness
- COURSE: right arm weakness improved from 2/5 to 4+/5

Example:

`After thrombectomy, aphasia improved substantially but mild right arm weakness persisted.`

becomes:

- MANAGEMENT: thrombectomy
- COURSE: aphasia improved substantially after thrombectomy
- COURSE: mild right arm weakness persisted

A COURSE object never reduces to a bare relation such as `abrupt onset` or `after thrombectomy`. Some repeated wording across objects is expected.

---

## 5. PRESERVE COMPLEX DIAGNOSTIC FORMULATIONS

Complex diagnostic formulations are native objects.

Examples:

- `focal seizure favored over recurrent ischemia`
- `TIA vs focal seizure remains unresolved`
- `cervical stenosis is present but insufficient to explain the weakness`
- `CIDP exacerbation`

Do not convert these into unrelated separate diagnoses unless they are truly independent problems.

---

## 6. PRESERVE MANAGEMENT STATE

Management objects retain their action state when supplied.

Possible states include:

- considered
- performed/completed
- active/ongoing
- held
- withheld
- not indicated
- ordered
- recommended
- planned
- pending
- deferred
- conditional

Preserve management rationale and dependency when they change meaning.

Examples:

- `apixaban held`
- `MRI ordered`
- `surgery not indicated`
- `rehab recommended`
- `referral submitted; authorization pending`
- `restart anticoagulation after repeat CT if no hemorrhage`

---

## 7. PRESERVE CERTAINTY AND TEMPORAL MEANING

Do not change:

- established → suspected
- suspected → established
- favored → confirmed
- historical → current
- current → historical
- planned → completed
- considered → performed

Preserve clinically important uncertainty, chronology, laterality, and conditions.

---

## OUTPUT CONTRACT

Return decomposed clinical objects only, one per line:

```text
<kind>: <text> [<letter>, <source_name>, <date>]
```

`<kind>` is one of the six above. No other label is permitted.

Do not assign object IDs. IDs are frozen after `01V`; `01` produces a candidate decomposition.

Do not allocate into note fields — no `CLAIM`, `EVIDENCE`, `COURSE` field, `MANAGEMENT` field, or section heading.

Do not write polished note prose.
Do not add information.
Do not remove clinically meaningful propositions.

The next module validates the decomposition. `02` allocates and section routing comes later.
