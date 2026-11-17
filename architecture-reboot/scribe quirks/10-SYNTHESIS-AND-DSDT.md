# Synthesis and D-S/D-T determinism

**Evidence class:** REPRODUCED / OBSERVED
**Date:** 2026-11-16
**Scope:** Doximity-only synthesis, routing and transformation.

## 1. Free synthesis is not deterministic

The same packet, coverage JSON and free-synthesis prompt produced:

| Run | Units | Actions | Unresolved |
|---|---:|---:|---:|
| 1 | 12 | 5 | 0 |
| 2 | 14 | 6 | 5 |
| 3 | 12 | 6 | 3 |

All were valid JSON. Content drifted:

- `P002` longstanding staring became a separate BACKGROUND problem in every run.
- `contains` and `separate_from` used unit IDs, event labels and problem IDs interchangeably.
- `counterevidence` contained diagnostic uncertainty (`T018/T019`), not contradictory evidence.
- Action coverage varied; `T008` was missing in some runs.
- Unresolved coverage varied from 0 to 5.
- Global `order` changed without a rule.

That test was invalid for exact determinism because it had no gold output and left the rules ambiguous.

## 2. Constrained synthesis is stable

A constrained prompt fixed:

- exactly one problem, `P001`;
- baseline staring as a unit under `P001`, not a problem;
- empty `contains` / `separate_from` / `counterevidence`;
- 13 fixed units with fixed source records;
- 7 fixed actions, one per source record;
- 2 fixed unresolved entries;
- fixed order 1–23.

Three runs matched on all IDs, types, source records, action set, unresolved set and order. Only labels and
wording varied.

Conclusion: free semantic synthesis is not deterministic; a constrained invariant test is.

## 3. D-S / D-T can be deterministic

D-S = deterministic structure/routing. D-T = deterministic transformation.

Observed:

- simple routing and transformation: 3/3 identical;
- complex multi-section routing: 3/3 identical after adding explicit `order`;
- mega 19-line test with 3 problems, 10 units, 4 actions, 2 unresolved: 3/3 identical;
- attachment ingestion worked: `ATTACHMENT_OK;;first_record=T001`.

Conditions:

- JSON input;
- explicit `order` on every item;
- fixed section mapping;
- fixed sentence templates;
- no clinical reasoning inside D-S/D-T;
- frozen facts JSON.

Without explicit order, cross-array routing drifted. “Preserve input order” is not a rule when items come
from separate arrays.

## 4. Attachment delivery works

Doximity read the attached Scribe packet and returned the first record. Attaching the packet is valid for
tests. Pasting is only a fallback.

## 5. Rules

1. Do not test free synthesis by exact label match. Test fixed invariants or a frozen JSON.
2. A baseline/prior pattern is never a separate problem. It is a `baseline_comparator` unit under the
   problem it informs.
3. `contains` and `separate_from` contain problem handles only, and stay empty when there is no separate
   problem.
4. `counterevidence` contains only direct contradiction. Diagnostic uncertainty belongs in a reasoning unit
   or unresolved entry.
5. Fix the unit map, action set and unresolved set before calling a synthesis test valid.
6. Give every routed item an explicit numeric `order`. Do not rely on array position across separate arrays.
7. Run D-S/D-T only on a frozen facts JSON.
8. Attach the packet when testing attachment; otherwise paste it in the same message.

## 6. What not to do

- Do not add more prose warnings to the free-synthesis prompt and call it deterministic.
- Do not compare free-synthesis labels exactly.
- Do not run D-S/D-T on a fresh, drifting synthesis output.
- Do not use “preserve input order” without a numeric order field.
