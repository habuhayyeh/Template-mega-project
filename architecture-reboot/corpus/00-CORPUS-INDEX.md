# Corpus — index and observations

**Status:** four baselines received. They are **targets**, not source packages — the encounter material that produced them has not been supplied. Fixtures stay blocked; assertion sets and the style contract are unblocked.

---

## 1. What exists

| id | case | claim shape | notable |
|---|---|---|---|
| BASELINE-01 | Numbness | single diagnosis + residual differential | synthesis bullet is truncated and misspelled |
| BASELINE-02 | Syncope | single diagnosis | negative workup stated as findings |
| BASELINE-03 | MG exacerbation | diagnosis + severity + concern | many unresolved placeholders |
| BASELINE-04 | First seizure | hedged diagnosis ("likely acute symptomatic") | placeholders inside quotations |

## 2. Two findings that affect the architecture

### F-1 — Placeholders are part of the target

BASELINE-03 and BASELINE-04 contain unresolved slots: `[date]`, `[confirm]`, `[titer/date]`, `[Add details here]`, `[x]`, `"[Insert radiology impression verbatim]"`.

These are not defects in the note; they are the note marking what it does not know. The current Case IR has no way to express this. Its only options are to omit or to invent, and inventing is the failure we have spent weeks removing.

**Status: observation, and the logic runs the other way.** A model that correctly marks an unknown value is not evidence that new schema is needed — it is evidence the current representation is sufficient for that behaviour. The sequence is: decide product behaviour first (should a note show markers, or omit?), then test whether the current representation can produce that behaviour. Schema is proposed only if it cannot.

It also settles a scoring question: a run that invents a value where the target has `[date]` fails fidelity; a run that omits the slot entirely fails completeness. Both are checkable.

### F-2 — A baseline can itself be wrong

BASELINE-01's final bullet reads "…other differentials inlcuding radiculopathy and" — truncated, misspelled, mid-sentence.

So the signer-approved target is imperfect in a way that a literal scorer would reward reproducing. Two consequences:

- assertions must be **property-based**, not text-matching;
- the corpus needs a register of known baseline defects, so a run that writes a complete sentence is not penalised for disagreeing with the target.

## 3. Derived properties (assertion candidates)

From four notes, these hold in all of them and are checkable now:

| id | property | check |
|---|---|---|
| P-01 | A/P block opens with a claim line before any bullet | mechanical |
| P-02 | no first-person or "we" anywhere in A/P | mechanical |
| P-03 | approximate quantities use `~` | mechanical |
| P-04 | times are anchored to presentation, admission, or the event — never bare "ago" | mechanical |
| P-05 | explicit negatives preserved as bullets, not summarised away | semantic |
| P-06 | plan bullets are actions, not narrative | semantic |
| P-07 | hedging preserved ("likely", "highly suggestive of", "concern for") | semantic |
| P-08 | unknown values are never invented — the note either omits them or marks the gap, **per a product decision not yet made** | `PENDING_PRODUCT_DECISION` |
| P-09 | one proposition appears once per problem block | mechanical |
| P-10 | labs summarised honestly ("otherwise without significant abnormality") rather than omitted or invented | semantic |

## 4. Style contract, draft

Observed, not invented:

- **Structure:** SUBJECTIVE / OBJECTIVE / ASSESSMENT AND PLAN; A/P has one block per problem, opened by `// <claim>`.
- **Bullets:** short declaratives; exam and lab facts stated as findings, not as sentences about the patient.
- **Abbreviations in use:** `~`, `s/p`, `W/O`, `QD`, `Q6 hrs`, `PO`, `IV`, `BLEs`, `LOC`, `ASM`, `PLEX`, `W/WO`, `FVC`, `NIF`.
- **Time:** "3 days prior to presentation"; "~8 hrs before the seizure" — anchored to an event, not to now.
- **Negatives:** listed explicitly, often with "No indication for…" in the plan.
- **Dose/route formatting:** `60 mg PO Q6 hrs`, `0.4 g/kg/day × 5 days`.

Two things the contract must **not** do: standardise the signer's abbreviations into full words, or expand the terse negative bullets into prose. Both would make the note more correct and less like the signer's.

## 5. What is still blocked

- **Fixtures** need source packages. Without them, a case has a target and no input, so nothing can be run.
- **Gate 0 parents** stay `DERIVED_PARENT` until at least one case has a source package.
- **Scorer predicates** can be drafted from §3 now, but cannot be calibrated without seeds built on real parents.

## 6. Proposed next actions

1. Carry F-1 as an **open question with a stated evidence requirement**, not a design change. No schema proposal until a run shows the current architecture failing at it.
2. Draft the ten predicates from §3 into an assertion set, marked `PENDING_SOURCE_CASES`.
3. Hold fixtures until source packages arrive; do not invent them.
