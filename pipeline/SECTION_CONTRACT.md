# SECTION CONTRACT

## Scope
1. Governs every section except the A/P.
2. The A/P is governed by `AP_ANCHOR` verbatim — content, buckets, order, omission of empty components.
3. Sections read the original sources. The Handoff decides relevance and emphasis and is not printed.
4. Section order: reason for consult → HPI → review of systems → neurologic history → other past medical history → social history → family history → medications → examination → workup → A/P.
5. Every section is generated from this encounter's sources. Nothing is copied forward.

## Primary home
6. Each fact has a primary home, not an exclusive one.
7. Primary homes: story and chronology → HPI; examination findings → exam; results → workup; formulation, selected evidence, course, management → A/P.
8. The A/P may repeat a fact from HPI, exam, or workup when that fact is evidence for or against the claim. That repetition is intended, not a defect.
9. Outside the A/P, avoid redundant repetition. A fact may appear in more than one section when it serves a distinct section-specific function — alcohol use in the HPI as a seizure precipitant and in social history as baseline use; ciprofloxacin in the HPI as an MG precipitant and in the medication list.

## Reason for consult
10. One line, the presenting problem in the clinician's words.

## HPI
11. Opens with one identifying clause: age, sex, and the known disease or acuity that frames the encounter.
12. Then chronological narrative, earliest to latest.
13. No diagnostic impression or formulation sentence, at the start or the end.
14. No fixed sentence limit. Length follows the encounter.
15. After the chronology, an optional compact paragraph of presentation-specific triggers and risk factors, where clinically useful.
16. That paragraph is presentation-specific: seizure — sleep, substances, alcohol, prior head trauma, childhood seizures, family history, infection; headache — red flags, position, provocation, prior phenotype; MG — precipitant infection or drug exposure.
17. Patient's words in quotes only where the exact wording matters.
18. Important negatives that shape the presenting problem stay in the HPI and are not pushed to ROS.

## Review of systems
19. Name is "Review of systems".
20. Patient-reported positives and negatives not already adequately represented in the HPI or another history section.
21. Includes symptoms specifically elicited, not only those volunteered.
22. One compact line where possible. No system-by-system headings.
23. `Denies` only for a symptom actually assessed and denied. No fabricated negatives.
24. Omitted entirely when it adds nothing.

## History
25. Neurologic history and other past medical history are separate sections. Neurologic first.
26. Historical diagnoses and formulations are grounded in the available record. Source and date are stated when clinically important, when records conflict, or when the history is otherwise uncertain. Patient-reported history that could not be independently confirmed is identified as such when that distinction matters.
27. Neurologic and presentation-relevant history is expanded. Other established PMHx is retained compactly when useful for clinical context; trivial or irrelevant detail is omitted.
28. Social history: living situation, work, substance use, plus the occupational or exposure detail that bears on the problem.
29. Family history: one or two lines. Omitted when not obtained.

## Medications
30. Full active list, with dose, route, and frequency where known.
31. The medication list contains medication, dose, route, and frequency only. Indication belongs elsewhere when clinically relevant.
32. The medication list reflects the patient's active/home regimen at presentation. A medication subsequently held or discontinued may remain listed when it was part of the presenting regimen; its changed status belongs in the A/P. Recently stopped medications may be included when they materially affect the neurologic presentation.

## Examination
33. Default order: mental status → cranial nerves → motor → reflexes → sensation → coordination → gait.
34. Only examined and documented elements appear. Unexamined components are not marked "not examined".
35. Syndrome-specific elements are inserted where appropriate: MG — ptosis, fatigability, ocular motility, bulbar strength, neck flexion and extension; movement disorder — tone, bradykinesia, tremor; neuropathy — sensory distribution, reflexes, gait.
36. Vitals appear once, at the head of the examination.

## Workup
37. Results only. Orders belong in the plan.
38. Grouped: labs, imaging, other studies, historical disease-specific studies where relevant.
39. One line per study or group. Dates when the source gives them.
40. A result is included when it establishes or narrows the differential, excludes a mimic or precipitant, establishes treatment safety, or materially contextualises the problem.
41. Unrelated normal data are dropped. Routine neurologic/admission studies may remain when they establish baseline context or exclude common precipitants or mimics, even when normal.

## Unknowns and empty sections
42. In the template, placeholders are allowed where they mark information to be sought.
43. In a generated note, unused placeholders disappear.
44. Unknown dates are omitted — never invented, never bracketed.
45. Unknown facts never become `None`, `[unknown]`, or boilerplate. A clinical fact not supported by the encounter sources is not written.
46. A section with nothing in it is omitted, heading included.

## Formatting
47. `~` not "approximately"; `hrs`, `mins`; QD, Q6 hrs, W/WO and familiar shorthand.
48. Short sentences and short bullets. No repetitive prose.
49. No disposition footer. Disposition is a plan item when relevant; the note ends at the last plan bullet.
50. No boilerplate attestation, consent, or reassurance language. Counseling or consent language is included only when clinically relevant and actually documented.

## Organizing principles
51. Neurologic problems are the organizing unit. Non-neurologic information is included when it supports, refutes, contextualizes, precipitates, or changes management of a neurologic claim; it does not automatically become a separate problem.
52. Presentation-specific acquisition rules belong to the template logic, not necessarily to the rendered note. The generator may seek and extract syndrome-specific information, but only documented and relevant findings appear in the final note.
