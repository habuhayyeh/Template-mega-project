# File A Full-Packet Capability Test — Predeclared Coverage Oracle

**Status:** FIXED BEFORE A OUTPUT  
**Purpose:** Human-scored development oracle for the first full-packet File A capability test.  
**Not:** a runtime validator, acceptance gate, production artifact, or same-model audit.

## Test question

Can current File A process the complete frozen `SCRIBE_EVIDENCE_V2_2` packet without truncation,
material omission, semantic upgrading, or loss of the distinctions needed by B/C?

The standalone A run tests **A capability only**. It does not prove the one-call A -> B -> C -> Render
integration.

## Scoring rule

Score each item after seeing the A output as:

- `PASS` — materially preserved;
- `FAIL` — materially lost, merged, upgraded, contradicted, or misattributed;
- `N/A` — oracle item is not actually present/applicable in the frozen source packet.

Do not generate new oracle items from the A output.

A completed `@@END` is necessary but not sufficient.

## A. Completion / scale

1. Output completes with `@@END`; no truncation.
2. Output remains sparse enough that it does not recreate a near-full second copy of the Scribe packet.
3. Late-source material is represented where material; coverage does not visibly collapse near the end.
4. Selectors/references remain usable throughout the output rather than degrading into vague source-wide citations.

## B. Event identity / chronology

5. Wednesday and Thursday acute events remain distinguishable where the source distinguishes them.
6. Repeated documentation of the same event is not automatically counted as an additional event.
7. Baseline staring behavior remains distinct from the acute seizure-like events.
8. Cruise chronology is preserved without inventing exact timing where the source is unclear.
9. Similar wording across records is not enough by itself to force `same_event` / `same_state`.

## C. Questions, negatives, and uncertainty

10. Question-only records do not become answers.
11. Patient prior-seizure history is not inferred from family-seizure questions.
12. Family seizure history remains separate from the patient's own seizure history.
13. Garbled/unclear transcript material remains uncertain rather than becoming a clean clinical fact.
14. Absence of documentation is not converted into denial/normality.

## D. Attribution / provenance

15. Patient, mother, fiance, EMS, ED documentation, ship/cruise sources, and other collateral remain attributed to the correct source chain where material.
16. Unknown/unmapped speaker roles remain unknown rather than being guessed.
17. A source-mediated statement (e.g. ED note via EMS/patient report) is not promoted to an objective finding.
18. Cruise/previous-workup statements preserve who reported them.
19. Provenance needed later for neurologic interpretation is not discarded as nonclinical noise.

## E. Temporal scope / currentness

20. Historical neurologic diagnoses remain historical unless current evidence separately supports present activity.
21. Longitudinal baseline phenomena remain distinct from current-episode findings.
22. Future/planned states are not promoted to current/performed states.
23. Current encounter mentions do not automatically make an old disease a current active problem.

## F. Action state

24. Keppra recommendation is not upgraded to an order or administration without source support.
25. Keppra order is not upgraded to execution without source support.
26. Prior administration/report of administration is not conflated with a newly recommended load.
27. Discontinued/held status is not used to infer that a dose was necessarily administered.
28. Decision, execution, response, and result remain separate when present.
29. Actor/owner of an action is preserved when established and left unresolved when not.

## G. Workup / result state

30. Prospective ED workup is not represented as completed testing.
31. Ordered/planned tests remain distinct from performed tests.
32. Performed tests remain distinct from available results.
33. Outside/reported results remain attributed to their source.
34. Unavailable/pending results are not normalized into reassuring findings.

## H. History-only and nonproblem material needed downstream

35. Historical left MCA stroke or other established neurologic history survives in A even if it may not belong in B's encounter-level PROBLEM_MAP.
36. Medication-at-presentation material needed by C survives even if it is not a problem.
37. Current examination material needed by C survives even if it is not a problem.
38. Workup/result material needed by C survives even if it is not a problem.
39. Relevant non-neurologic history/context that affects neurologic interpretation or management is not silently dropped.
40. Functional/safety context that changes note content or management is not silently dropped.

## I. Reconciliation quality

41. Duplicate/corroborative records can reconcile without erasing source differences.
42. Conflicting records remain conflicts/unresolved when the source does not resolve them.
43. Evolution over time is not mislabeled as contradiction.
44. Different assertion types (question vs report vs result vs diagnosis vs action) are not falsely reconciled as equivalent statements.
45. A does not globally atomize every clause into a separate unit.

## J. Boundary fidelity

46. A does not create PRIMARY/BACKGROUND roles.
47. A does not decide containment/problem architecture.
48. A does not invent causal/contributory problem relations.
49. A does not decide note sections.
50. A does not write final note prose.
51. A does not silently exclude a material note-relevant distinction solely because it is not a candidate problem.

## Fatal failures

Any of the following is a **fatal A capability failure** even if most oracle items pass:

- truncation before `@@END`;
- material action-state promotion;
- material question-as-answer conversion;
- clinically important attribution inversion;
- historical/current promotion that changes later problem interpretation;
- merger of distinct acute events that changes diagnostic reasoning;
- loss of a material history/exam/workup/medication distinction needed by B or C.

## Interpretation

### A holds at scale
Use when:
- no fatal failure;
- completion is intact;
- material distinctions above are preserved with acceptable sparsity.

Then:
- patch the already-agreed B semantics:
  - PROBLEM_MAP = encounter-level A/P problems only;
  - B owns explicit diagnostic stance/reasoning;
- add C `BLUEPRINT_UNRESOLVED`;
- proceed to same-call A -> B -> C integration testing.

### A fails at scale
Do not automatically add a new pass.

First classify the failure:
- source-semantic extraction/coverage;
- cross-record reconciliation;
- action-state handling;
- context/output size.

Only then consider splitting A along the failing boundary.

A possible split, only if evidence justifies it:

```text
A1 source-semantic ledger
  -> A2 reconciliation
```

Do not move cross-record relations such as same-event/evolution/conflict into A1.

## Production-model note

Current peer consensus:

```text
Production target:
one Doximity Ask invocation with logical
A -> B -> C -> Render phases.

Development mode:
standalone capability tests plus same-call materialized A/B/C artifacts.
```

A/B/C are semantic ownership boundaries, not true runtime-isolation boundaries.
