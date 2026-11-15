# STATUS — 06 AND THE BODY BRANCH

2026-11-14. Records the accepted state so it is not inferred from the files later.

| Item | State |
|---|---|
| `06_SECTION_ROUTE` contract | architecturally adequate |
| `check_sections.py` | accepted mechanical validator |
| reviewed v2 `06` oracle (`step9/ORACLE_ledger_06_v2.txt`) | accepted routing target, frozen |
| Doximity `06` execution | **not production-reliable** — 3 runs, 12 / 6 / 9 unacceptable differences, non-converging; run 3 also malformed the reuse schema |
| production `06` | **unresolved** |
| `07_WRITE_SECTIONS` | may proceed, using the reviewed oracle only |

`06` is not frozen as an implementation. Only its contract and its oracle are accepted.

Frozen oracle, verified against the audit: O26/O27 EXAM; O28 AP_ONLY; O32, O36 NEURO_HISTORY; O40 AP_ONLY; O51 WORKUP; O55, O56, O57, O58, O59, O60 NEURO_HISTORY. All thirteen confirmed, `check_sections.py` PASS.

Section counts in the frozen ledger: HPI 8, NEURO_HISTORY 17, WORKUP 8, EXAM 3, MEDICATIONS 3, OTHER_PMH 1, SOCIAL 1, AP_ONLY 19, plus reuse O3 → REASON_FOR_CONSULT and O8 → HPI. ROS and FAMILY have no objects and are omitted.

## Future engineering task, not started

Redesign production `06` as a hybrid deterministic/semantic router: move structurally or metadata-determined routing into code, keep semantic routing only where genuinely necessary. Not to be started until the body-note writer is shown to work when fed correct routing.
