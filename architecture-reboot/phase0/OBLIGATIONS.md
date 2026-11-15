# OBLIGATIONS — downstream duties that must not vanish

Each obligation is a thing Phase 0 knows it does not do. Owner, prerequisite, and the test that will close it. An obligation without a future test is a wish.

State: `OPEN` (acknowledged), `BLOCKED` (prerequisite missing), `CLOSED` (test passed).

| ID | Obligation | Owner | Prerequisite | Closing test | State |
|---|---|---|---|---|---|
| O-01 | Test-mode vs production equivalence — a test-mode run must represent what production would emit | RENDER | production mode decision | same case, both modes, IR identical except the trace block | OPEN |
| O-02 | Module-boundary behaviour inside one shared context — seams may bleed when one model runs all three modules | STRUCTURE | three-module prompt exists | seam probes: change one module's input, assert no other module's output changes | BLOCKED |
| O-03 | Failure propagation and containment — one bad unit must not corrupt the rest of the note | RENDER | unit-level isolation | inject one malformed unit; assert only that line fails | OPEN |
| O-04 | One-call package and resource budget — what fits in one Ask call | BUILD | package manifest | measure truncation threshold empirically; no fixed byte target | BLOCKED |
| O-05 | Source→package fidelity — what the compiler embedded equals what the rule referenced | BUILD | payload hashing | hash match per rule payload | OPEN |
| O-06 | Package-order sensitivity — reordering files must not change output | BUILD | lint | shuffle file order, rebuild, diff output | OPEN |
| O-07 | Environment fingerprint — model, mode, date, package version recorded per run | PROCESS | packet | packet completeness check | OPEN |
| O-08 | Cross-run ID matching — the same object keeps the same id across runs of the same case | STRUCTURE | id scheme | two runs, same case, compare id sets | OPEN |
| O-09 | Case namespace isolation — ids from one case cannot collide with another | BUILD | id scheme | build two cases, assert disjoint | OPEN |
| O-10 | Paste-layout and source-order bias — output must not depend on where a fact was pasted | INGEST | fixtures | permute paste order, compare IR | OPEN |
| O-11 | Contradictory-source fixtures — the corpus has no case where sources disagree | FIXTURES | signer case | add a case with conflicting notes; assert both objects survive and adoption is explicit | OPEN |
| O-12 | Full source→output coverage chain — every span reaches a disposition or a line | PROCESS | packet | chain check across spans→objects→units→lines | OPEN |
| O-13 | Seam matrix — which seams are tested by which fixture | PROCESS | fixtures | matrix has no empty cell for a FROZEN decision | OPEN |
| O-14 | Evidence hierarchy — unit evidence cannot imply integrated acceptance | PROCESS | manifest | readiness states enforced in packet | OPEN |
| O-15 | Corpus coverage — the ten-note corpus covers each failure class | FIXTURES | signer notes | coverage table per class | OPEN |
| O-16 | Scorer calibration — the scorer must be shown to fail when it should | PROCESS | known-bad case | seed a defect; require localisation | OPEN |
| O-17 | Control-plane meta-tests — who tests the tests | PROCESS | this file | each control has at least one failing-fixture demonstration | OPEN |
| O-18 | Control-plane self-change governance — Phase 0 changes are governed | PROCESS | change ledger | every Phase 0 edit appears in the ledger | OPEN |
| O-19 | Raw-evidence integrity — runs and notes are immutable and hashed | PROCESS | storage | hash recorded at capture; verify before scoring | OPEN |
| O-20 | Baseline versioning — a signer-approved note has a version | PROCESS | corpus | each baseline carries a version and a date | OPEN |
| O-21 | Typed absence and unresolved semantics — `UNDECIDABLE`, `DISCOVERY`, `ABSENT_BY_CONTRACT` are distinct | AUDIT | vocabulary | every finding carries one of the three | OPEN |
| O-22 | Readiness states — a local artifact is not a system | PROCESS | manifest | no acceptance claim above `ACCEPTED` | OPEN |

## The one that limits every claim

**O-21 is the honest boundary.** Mechanical predicates can be decided; identity, grouping, and operator adequacy cannot. Any reproducibility claim is scoped to the mechanical subset, and the proportion is measured, not asserted.

## Rules

1. An obligation may be added by anyone; it may only be closed by a recorded passing test.
2. An obligation with no owner is a defect in this file.
3. Closing an obligation requires a packet, not an opinion.
