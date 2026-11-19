# Test-to-prompt traceability

**Purpose:** tie each reported test result to the prompt file that produced it. No mixed or invented results.

**Scope:** only tests with a known prompt file and an observed output. Raw outputs live in the conversation,
not in the repo. â€œOne runâ€ is not determinism.

| ID | Test | Prompt file | Runs | Observed result | Status |
|---|---|---|---:|---|---|
| T01 | Eight-category coverage | `../experiments/ask/COVERAGE-ONLY-PROMPT.md` | multiple | Missing `current_event` and/or `action_bearing`; sometimes 6/8 | FAIL |
| T02 | Current-event only | `../experiments/ask/COVERAGE-ONE-CATEGORY-TEST.md` | 1 | Only current-event category returned, but almost every record included | FORMAT PASS / SEMANTIC FAIL |
| T03 | Current + investigation | `../experiments/ask/COVERAGE-TWO-MISSING-TEST.md` | 1 | Returned only `@@END` | FAIL |
| T04 | JSON coverage | `../experiments/ask/COVERAGE-JSON-PROMPT.md` | 1 | Valid JSON, 8 keys; `T015` in current/workup; actions missing `T008,T015,T022` | FORMAT PASS / SEMANTIC FAIL |
| T05 | CSV coverage | `../experiments/ask/COVERAGE-CSV-PROMPT.md` | 1 | Valid table, 8 buckets; baseline included `T002,P1.002` | FORMAT PASS / SEMANTIC FAIL |
| T06 | YAML coverage | `../experiments/ask/COVERAGE-YAML-PROMPT.md` | 1 | Buckets not nested under `coverage` | FAIL |
| T07 | Keyed one-item synthesis | `../experiments/ask/SYNTHESIS-KEYED-ONE-ITEM-TEST.md` | 1 | `P001` and `CU001` truncated; action sources/wording generic | FAIL |
| T08 | Free synthesis | `../experiments/ask/SYNTHESIS-JSON-PROMPT.md` | 3 | 12/14/12 units; 5/6/7 actions; 0/5/3 unresolved; `P002` baseline problem; `contains` misuse | FAIL |
| T09 | Constrained synthesis invariants | `../experiments/ask/SYNTHESIS-INVARIANTS-PROMPT.md` | 3 | One `P001`, 13 units, 7 actions, 2 unresolved, order 1â€“23; labels vary | PASS |
| T10 | Handoff V1 | `../experiments/ask/DOXIMITY-HANDOFF-TEST.md` | 3 | Stage A shape drift; Stage B correct after rereading `FACTS` | INCONCLUSIVE |
| T11 | Handoff V2 | `../experiments/ask/DOXIMITY-HANDOFF-TEST-V2.md` | 3 | Exact Stage A; six Stage B lines; all carried `[A]` | PASS |
| T12 | D-S/D-T simple 1â€“4 | `../experiments/ask/DOXIMITY-DSDT-TESTS.md` | 3 | Exact routing, sentence, combined note, error | PASS |
| T13 | D-S/D-T complex 5 | `../experiments/ask/DOXIMITY-DSDT-COMPLEX-TESTS.md` | 1 pre-fix + 4 post-fix | First run wrong order because test was ambiguous; after explicit `order`, four identical | PASS AFTER TEST FIX |
| T14 | D-S/D-T complex 6â€“8 | `../experiments/ask/DOXIMITY-DSDT-COMPLEX-TESTS.md` | 1 | Exact multi-line, extra/missing key, duplicate-ID error | ONE RUN ONLY |
| T15 | Mega D-S/D-T | `../experiments/ask/DOXIMITY-MEGA-DSDT-TEST.md` | 3 | Attachment OK; exact 6-section route; exact 19 lines | PASS |
| T16 | Code execution | `../experiments/ask/DOXIMITY-CODE-EXECUTION-TEST.md` | 1 each | `NO_RUNTIME` / refusals; no SHA-256 hash | FAIL / NO RUNTIME |
| T17 | Multi-language execution | `../experiments/ask/DOXIMITY-MULTILANGUAGE-TEST.md` | 1 each | Explanations/refusals; no hash | FAIL / NO RUNTIME |
| T18 | Pipeline tools 4â€“6 | `../experiments/ask/DOXIMITY-PIPELINE-TOOL-TESTS.md` | 1 each | Schema valid but semantic gaps; state carried wrong census; clinical tools disclosed | MIXED |

## Not claimed

- Exact failing text for every edited coverage prompt is not preserved; the current file may differ from the
  run.
- Raw outputs are not saved as repo artifacts; this table records only observed results.
- T14 has one run, so it is not determinism evidence.
- T18 is one run per part; it is capability evidence, not stability evidence.
- No external parser was used to certify the JSON; checks were manual.

## Rule

Every future test entry must link the exact prompt file and state the run count. If either is missing, mark
it unverified.


## November 18, 2026: source-packet / worksheet development record

These entries preserve project status; they do not extend the empirical pass table above.

| ID | Component | Exact prompt artifact | Runs established in this update | Status |
|---|---|---|---|---|
| N01 | Step 1 V2 source-preserving packet | Not archived: exact prompt was not recoverable during this update; identifier NEUROLOGY_SOURCE_PACKET_V2_CANDIDATE | Exact per-version total not established | Development baseline frozen by agreement; observed output structure only; fidelity, completeness, and reproducibility not certified |
| N02 | Step 2 V1 physician-review worksheet | [Full candidate prompt](prompts/NEUROLOGY_REVIEW_WORKSHEET_V1_CANDIDATE.txt) | No execution of this exact candidate established | CANDIDATE / UNVERIFIED; not approved, frozen, or deterministically validated |

See [16-SOURCE-PACKET-AND-REVIEW-WORKSHEET.md](16-SOURCE-PACKET-AND-REVIEW-WORKSHEET.md) for the agreed boundaries and open items. Raw patient material is intentionally excluded.
