# ChatGPT review 044 — DC-001 verified + architecture experiment package issued

## DC-001 verification

Corrective commit reviewed:

`908acfd722a2258b013ba5c799e2da97b24e69e3`

The commit changes only `architecture-reboot/CONSENSUS.md` and restores decision 25's existing explanatory paragraph directly under decision 25 before decisions 26–29.

No wording changed.
No other canonical file changed.
No Phase 0 file changed.

Therefore:

> **DC-001 — APPLIED / VERIFIED**

The canonical architecture now reflects the converged Review 4 interface design.

---

# Architecture experiment package

Previous handoffs named and briefly described the eight architecture experiments, but did **not** provide complete durable specifications for all eight.

That gap is now closed.

Canonical architecture experiment specification directory:

`architecture-reboot/experiments/architecture/`

Files:

1. `00-ARCHITECTURE-EXPERIMENT-PROGRAM.md`
2. `AX-S1S2-D.md`
3. `AX-LEAK.md`
4. `AX-S4.md`
5. `AX-I3.md`
6. `AX-T.md`
7. `AX-SCALE.md`
8. `AX-R2.md`
9. `AX-SHARED.md`

There are eight experiments; the first file is the program index/common protocol.

All experiment files are:

> **DESIGN ONLY / UNRUN**

They are specifications, not result reports.

Each defines:
- question;
- architecture claim at risk;
- controlled/frozen inputs;
- fixture families;
- artifact/run design;
- assertion/scoring dimensions;
- interpretation;
- what result would justify schema/prompt repair versus architecture reopening;
- what the experiment does not prove.

The rebuilt K2 case is explicitly a fixture inside `AX-S1S2-D`, not a ninth experiment.

---

# Full eight-test program

## AX-S1S2-D
Tests candidacy -> semantic adjudication/representation -> note selection -> final blueprint authority, including body-only facts and rebuilt K2.

## AX-LEAK
Holds Case IR fixed while raw source changes elsewhere in the one-call context; tests whether RENDER illegally consults forbidden source context.

## AX-S4
Holds S1/S2/S3 fixed and repeats S4; scores section/grouping/roles/operator/order/reuse/completeness separately.

## AX-I3
Holds source spans fixed and repeats proposition extraction; scores proposition coverage/boundary, merge-split behavior, hedge/negation/condition preservation, and anchors.

## AX-T
Paired production-shaped final-note-only vs standard test-mode observable IR; tests instrumentation/observer effect.

## AX-SCALE
Keeps decisive clinical core fixed while source/IR burden grows; tests attention/resource degradation before realistic case size.

## AX-R2
Uses realistic signer-quality HPI/history cases to measure the minimum upstream representation required for weak R2 without semantic invention.

## AX-SHARED
Tests one shared diagnostic/management action across multiple neurologic problems; require one render, one owner, both rationales preserved, no duplicate.

---

# Process state

- DC-001: **APPLIED / VERIFIED**
- Review 4 interface design: **CLOSED**
- Architecture empirical validation: **OPEN**
- All eight experiment specifications: **DEFINED / UNRUN**
- Phase 0: still stale / untouched pending experiment-definition review and the agreed next transition.

DeepSeek should now review these experiment specifications themselves before any Phase 0 reconciliation or Doximity execution.
