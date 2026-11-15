# COVERAGE_LEDGER — obligations and corpus coverage

Canonical for: **what is owed downstream, and where the corpus is thin.**

It owns mappings and obligations. It references state from the manifest and the fixture index; it does not copy it.

---

## 1. Obligations

Each has one registered owner, a prerequisite, and the test that closes it. State: `OPEN` / `BLOCKED` / `CLOSED`.

| id | obligation | owner | prerequisite | closing test | state |
|---|---|---|---|---|---|
| OBL-01 | test and production agree on the properties production carries | RENDER | production mode defined | same case both modes; agreement on carried properties; omitted ones recorded | OPEN |
| OBL-02 | undeclared seam propagation is detected | STRUCTURE | seam probes | change one module's input; declared dependencies may propagate, undeclared ones must not | BLOCKED |
| OBL-03 | containment policy decided and demonstrated | RENDER | containment decision | a malformed unit's blast radius is defined and shown | BLOCKED |
| OBL-04 | one-call resource budget characterised | BUILD | package manifest | truncation threshold measured empirically | BLOCKED |
| OBL-05 | source→package fidelity | BUILD | payload hashing | hash match per payload | OPEN |
| OBL-06 | package-order sensitivity characterised | BUILD | lint | reorder files, rebuild, compare; sensitivity recorded, not forbidden | OPEN |
| OBL-07 | environment fingerprint recorded per run | PROCESS | packet | packet completeness check | OPEN |
| OBL-08 | identifier stability within a case | STRUCTURE | id scheme | two runs, same case, object identity comparable | OPEN |
| OBL-09 | case namespace isolation | BUILD | id scheme | two cases, disjoint ids | OPEN |
| OBL-10 | paste-order bias characterised | INGEST | fixtures | permute paste order, compare IR; bias recorded | OPEN |
| OBL-11 | contradictory-source handling | FIXTURES | signer case | both objects survive; adoption explicit; no silent preference | OPEN |
| OBL-12 | span and object accounting chain | PROCESS | packet | every span dispositioned **and** every object used-or-dispositioned | OPEN |
| OBL-13 | seam matrix | PROCESS | fixtures | no FROZEN decision without a case touching it | OPEN |
| OBL-14 | evidence hierarchy | PROCESS | manifest | no acceptance claim above its readiness state | OPEN |
| OBL-15 | corpus coverage across axes | FIXTURES | corpus | matrix below has no empty cell in a CRITICAL row | OPEN |
| OBL-16 | scorer calibration | SCORER | known-bad case | seeded defect localised to case and owner | OPEN |
| OBL-17 | control-plane meta-tests | PROCESS | this file | each control has a demonstration that it fails when it should | OPEN |
| OBL-18 | control-plane change governance | PROCESS | change ledger | every Phase 0 edit appears in the ledger | OPEN |
| OBL-19 | raw-evidence integrity | PROCESS | storage | hash at capture, verify before scoring | OPEN |
| OBL-20 | baseline versioning | PROCESS | corpus | each baseline carries version and date | OPEN |
| OBL-21 | typed absence and discovery | AUDIT | vocabulary | every finding is `UNDECIDABLE`, `DISCOVERY`, or `NOT_APPLICABLE` | OPEN |

**Nothing here is closed.** There are no packets yet.

---

## 2. Corpus coverage

Coverage is multidimensional. Failure class is one axis, not the definition, and there is no aggregate score.

| axis | values |
|---|---|
| failure class | F1–F10, C11–C14 |
| artifact | I1–I4, S1–S4, R1–R3 |
| seam | ingest→structure, structure→render, render→note |
| mode | PRODUCTION, TEST |
| source family | transcript, current note, prior note, study, lab |

Current state, all axes:

```text
cases: 12 total, 9 ACTIVE, 3 PENDING_DEPENDENCY
axes covered:  failure class 8/14 · artifact 5/11 · seam 1/3 · mode 1/2 · source family 2/5
```

The gap that matters most: **only one seam is covered**, and the seams are where the architecture has never been tested. That is OBL-02 and OBL-13.

---

## 3. Rules

1. An obligation with no registered owner id is invalid.
2. Coverage is read as a matrix, never summed into a number.
3. Closing an obligation requires a packet reference, not an opinion.
