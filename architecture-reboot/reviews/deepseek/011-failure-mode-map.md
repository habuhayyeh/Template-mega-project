# DeepSeek 011 — the failures we actually had, mapped to modules

Recalled from the record, not from memory of intent. Each is a defect that reached an output.

| Code | Failure | Evidence |
|---|---|---|
| F1 | **Fabrication** — a word or status the source never said | `postictal confusion resolved` on a no-dispatcher run |
| F2 | **Duplication** — one fact rendered twice | infarct, CT, family concern, twice each, in clean set 3 |
| F3 | **Silent omission** — a fact or line gone | infarct evidence dropped in run 2; missing `Seizure precautions` |
| F4 | **Contract break** — malformed output | free-text `REUSE` on the third identical run |
| F5 | **Instability** — different decisions on identical input | 12 / 6 / 9 differences; three runs, three fact sets |
| F6 | **Cross-problem leakage** | memory referral in both blocks; O53/O54 attached to the memory problem |
| F7 | **Provenance misuse** | `2024-02` rendered as the infarct date; attribution dropped |
| F8 | **Prior promoted to current** | `no further workup [2025-06]` in today's plan |
| F9 | **Voice violation** | first person in the A/P |
| F10 | **Truncation** — a whole block or section missing | `04` dropped a block on run 4 |

## Where each module can admit each failure

**● primary** (this module creates the defect) · **○ secondary** (it can pass one through)

| | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 |
|---|---|---|---|---|---|---|---|---|---|---|
| I1 Source Map | ● | | ○ | | ○ | | ● | | | ○ |
| I2 Span Registry | | | ● | | | | | | | ○ |
| I3 Extraction | ● | ○ | ● | | ● | | | | | ○ |
| I4 Annotation | ● | | | | ○ | | ● | | | |
| S1 Problem Model | | ● | ○ | | ● | ● | | | | ○ |
| S2 Adjudication | | ● | | | ● | ○ | ○ | ● | | |
| S3 Selection | | | ● | | ● | ● | | | | |
| S4 Blueprint | | ● | ● | ● | ● | ● | | ○ | | ● |
| R1 Realization | ● | ○ | ○ | ● | ○ | | ○ | | ● | |
| R2 Composition | ○ | | ● | | | | | | ● | |
| R3 Assembly | | | | ● | | | | | | ● |

## The four that deserve attention

**F1 has four entry points** — I1, I3, I4, R1. That is why the token-containment guard matters: it is the only check that sits on all of I3's output, and R1's operator-fixed text is the only thing stopping the renderer adding connective prose. Two of the four entry points are still unguarded by construction (I1's family classification, I4's metadata).

**F3 has five** — I2, I3, S3, S4, R2. Silent loss is the failure with the most doors. The design's answer is total accounting at S3 and completeness at S4, but note that neither catches R2 dropping a unit during composition; that needs the join-order check.

**F5 is not localised anywhere.** It is the *variance* of the decisions made in S1, S2, S3 and S4 across runs. No module can be blamed, which is exactly why it went undiagnosed for so long. It can only be measured: run the same input three times and diff the IR.

**F6 and F8 are the same mistake in two costumes** — treating an object's subject as its owner. `Etiology of the seizure is likely the chronic infarct` belongs to the seizure because of what it explains, not to the infarct because of what it names. S1 and S3 are where that is decided, and both are `L`-control.

## What the map shows that the module list did not

The blueprint (S4) is the single highest-risk submodule: it is primary for five failure classes and secondary for two more. That is not an argument for splitting it — it is the argument for it being the most heavily validated, which it is: typing, completeness, section list, zero-member rule, and per-section uniqueness all live there.

The renderer is much less dangerous than it was in the old architecture, because it is now forbidden from making any decision that could produce F2, F3 or F5. Its remaining exposures are F1 (adding words), F4 (malformed input) and F9 (voice), and all three are mechanically checkable.
