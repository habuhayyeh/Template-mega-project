# MODULE 03 — SELECT / ORGANIZE

## PURPOSE

Take the allocated output from:

- `01_DECOMPOSE.md`
- `02_ALLOCATE.md`

and organize it into clinically coherent problem blocks.

This module decides **what belongs together** and **what deserves to survive** into the final note structure.

It does not return to the raw source prose.
It does not redo decomposition.
It does not redo allocation.
It does not perform final prose compression.

---

## INPUT CONTRACT

Input consists only of allocated objects under:

- CLAIM
- ETIOLOGY [optional]
- EVIDENCE
- COURSE
- MANAGEMENT

Every input object carries an ID (`O1`, `O2`, …) assigned upstream. The ID, its bucket, its text, and its provenance marker are immutable. `03` refers to objects by ID. It does not retype, rewrite, re-bucket, or recreate any object.

These objects already preserve:

- diagnostic certainty
- temporal meaning
- management action state
- rationale/dependency
- complex diagnostic relationships

Treat those preserved meanings as authoritative unless there is an obvious internal contradiction.

## OUTPUT REPRESENTATION

`03` outputs one routing decision per input object, in input ID order, one line each:

```text
O1 → P1.CLAIM_QUALIFIER
O2 → P1.PRIMARY_CLAIM
O3 → P1.CLAIM_QUALIFIER
O4 → P1.ETIOLOGY
O6 → P1.EVIDENCE
O21 → P2.EVIDENCE
O31 → P2.PROBLEM_LABEL
O37 → DISCARD: IRRELEVANT_TO_RETAINED_PROBLEMS
```

Allowed destinations only: `P#.PRIMARY_CLAIM`, `P#.CLAIM_QUALIFIER`, `P#.ETIOLOGY`, `P#.EVIDENCE`, `P#.COURSE`, `P#.MANAGEMENT`, `P#.PROBLEM_LABEL`, `DISCARD: <reason>`.

A block has at most one `PRIMARY_CLAIM_REF` — the formulation the problem line is built from. Additional claim objects are `CLAIM_QUALIFIER_REFS`: further clinician formulation, uncertainty, excluded alternatives, or interpretation. A qualifier is not a second problem line, and it is not discarded because it does not fit the header.

`PROBLEM_LABEL` names a block that has no claim object. Prefer the proposition that names the problem; a concern, preference, or remark is not a label when a naming proposition exists.

The object's original bucket is immutable. A `CLAIM` object may not be routed to `EVIDENCE`, a `MANAGEMENT` object may not be routed to `EVIDENCE`, and so on. `PROBLEM_LABEL` is a role attached to an object that keeps its own bucket; it is not a retyping and not a move.

No new IDs. No object text. No grouped lists. Every input ID appears exactly once.

`DISCARD` reasons come from a closed set:

```text
EXACT_DUPLICATE_OF: O#
IRRELEVANT_TO_RETAINED_PROBLEMS
```

`absorbed`, `merged`, `subsumed`, and bare `redundant` are not reasons — an object is retained or discarded, never folded into another. A duplicate must name the retained ID and hold the same clinical text after trivial normalization of whitespace, case, and punctuation. A restatement in different words is not a duplicate: retain it and let `04` compress.

There is no supersession reason. A later or older statement about the same topic does not replace another source.

Historical provenance alone never justifies a discard. An old object stays eligible when it plausibly supports a retained problem. Discard only what is irrelevant to every retained problem. `03` does not optimize concision; `04` compresses.

If an object genuinely serves a second block, declare it after the ledger on a separate line — `REUSE: O21 → P2.EVIDENCE, distinct function: reported memory concern` — and leave its single assignment line unchanged. The stated function must be one the object actually performs. A `REUSE` line is a declaration for `04`, not a second assignment.

Close the ledger with three mechanical lines computed from what was emitted:

```text
UNACCOUNTED_IDS: none
MULTIPLY_ASSIGNED_IDS: none
ACCOUNTING: 55/55
```

`UNACCOUNTED_IDS` lists any input ID with no line. `MULTIPLY_ASSIGNED_IDS` lists any ID with more than one assignment line. `ACCOUNTING` is assigned lines over input IDs. Do not reply until all three are clean: first two `none`, count equal to the input count.

Rendering, for `05`: `PRIMARY_CLAIM_REF` becomes the `//` problem line; `CLAIM_QUALIFIER_REFS` become short reasoning or evidence bullets beneath it. `03` exposes the distinction; `05` renders it.


---

## 1. BUILD PARENT PROBLEMS

Group related allocated objects into the smallest clinically coherent problem blocks.

A problem block should represent a meaningful clinical issue such as:

- acute diagnosis
- active syndrome
- meaningful diagnostic competition
- complication
- independent neurologic problem
- consequential incidental finding with its own management or surveillance

Do not create a new problem merely because there is:

- a test result
- a medication
- a procedure
- a single symptom
- a risk factor
- a historical diagnosis
- a consultant recommendation

unless it represents an independent clinical issue.

`03` selects, groups, and orders. It does not move an object from one input bucket to another, except for the claim promotion in §2. An input COURSE item remains COURSE; an input MANAGEMENT item remains MANAGEMENT; an input EVIDENCE item remains EVIDENCE.

Every retained object's provenance marker is carried through unchanged.

An object may be retained in a problem block only if it has a direct semantic relationship to that block's claim. Do not attach a leftover or unrelated object to the nearest available problem to keep it somewhere. If an object is not relevant to any retained problem, discard it under §9.

When the same retained object is assigned to more than one problem block, keep it in multiple blocks only if it serves a distinct evidentiary or management function for each block. Otherwise retain it only in the semantically appropriate block.

---

## 2. USE CLAIM AS THE PRIMARY ORGANIZER

Where a CLAIM object exists, it defines the main problem block. A block does not require one.

Examples:

`Acute left MCA ischemic stroke favored over focal seizure`

should organize one problem.

`CIDP exacerbation`

should organize one problem.

`TIA vs focal seizure remains unresolved`

should remain one problem representing one diagnostic competition.

Do not split a weighted or unresolved diagnostic formulation into separate competing problem blocks unless they are truly independent problems.

A block holds one `PRIMARY_CLAIM_REF` and any number of `CLAIM_QUALIFIER_REFS`. The primary claim is the one the problem line is built from — the current diagnostic formulation, not the presenting event, where both exist. Qualifiers carry additional formulation, uncertainty, excluded alternatives, or interpretation, and stay with the block rather than being dropped.

A problem block does not require an existing diagnostic-formulation CLAIM object. When a clinically distinct problem has evidence or management but no claim ref, name the block with `PROBLEM_LABEL_REF` pointing at an existing documented proposition that directly names that problem. The referenced proposition must already exist in the input, must refer to the same subject as the evidence and management beneath it, must keep its original bucket, and may not invent a diagnosis or increase certainty.

`Progressive memory difficulty` is eligible for a chronic memory problem; `family's concern about memory` is a concern, not a problem name, and is not the label when a naming proposition exists. `Confusion today is postictal, not dementia` is not a label at all — it formulates today's event and belongs with the seizure as a claim qualifier.

A prior clinician's formulation stays evidence unless the current encounter adopts it.

---

## 3. ATTACH ETIOLOGY TO ITS PARENT CLAIM

ETIOLOGY should remain attached to the problem it explains.

Example:

- CLAIM: acute ischemic stroke
- ETIOLOGY: likely cardioembolic in the setting of atrial fibrillation

Do not make the etiology a separate problem unless it independently represents another active clinical issue.

---

## 4. ATTACH EVIDENCE TO THE CORRECT PROBLEM

Place EVIDENCE under the problem whose claim it bears on. Ownership is decided by what the object does to the claim, not by which note it came from.

**Eligibility is a test, not a preference.** An object is `P#.EVIDENCE` only if it materially does one of these for that specific claim:

- establishes the problem
- confirms the diagnosis
- provides localization
- refutes or opposes the current formulation
- discriminates between competing explanations
- explains an important uncertainty

Context, unrelated normals, patient preferences, and facts that do not bear on this claim are not evidence. They are discarded here, or they reach the note body through `06`. They never become an evidence bullet.

**Reasoning is not evidence and is never compressed away.**

- `ETIOLOGY` carries explicit causal attribution.
- `CLAIM_QUALIFIER` carries the differential, the uncertainty, and any reasoning that qualifies the claim.
- Neither is discarded because the facts it interprets already appear in `EVIDENCE`. Lexical overlap between a reasoning entry and an evidence entry is allowed and expected.

**Diagnostic adjudication is MANAGEMENT by kind and CLAIM_QUALIFIER by role.** An object such as `but the MRI will tell us` states how a test will adjudicate uncertainty. It is assigned `P#.CLAIM_QUALIFIER` — not `P#.MANAGEMENT`, and not `P#.EVIDENCE`. `MRI ordered` is management. `MRI will tell us whether this is old scar or a new lesion` is a qualifier.

---

## 5. ATTACH COURSE TO THE CORRECT PROBLEM

COURSE should describe the evolution and current state of the corresponding problem.

Examples:

- abrupt onset
- progressive over 3 weeks
- improved after treatment
- persistent deficit
- currently requires supervision for ambulation

Do not create a separate problem for course information.

COURSE carries only trajectories the allocation already recorded. Do not write a course phrase here that the allocation did not supply.

---

## 6. ATTACH MANAGEMENT TO THE CORRECT PROBLEM

Place each management object under the problem it addresses.

Preserve:

- action
- action state
- rationale
- dependency
- conditionality

Examples:

- thrombolysis withheld because of recent apixaban use
- thrombectomy performed
- MRI ordered
- no surgery indicated
- rehabilitation recommended
- anticoagulation held pending repeat CT

Do not split one management decision across multiple problems unless it genuinely serves multiple independent problems.

---

## 7. DECIDE WHICH PROBLEMS DESERVE SEPARATE BLOCKS

Keep a problem separate when removing or merging it would lose an important:

- diagnostic question
- clinical trajectory
- management branch
- complication
- surveillance obligation
- follow-up obligation

Merge when multiple objects represent manifestations of the same underlying problem.

Examples:

- aphasia + right arm weakness + M2 occlusion + thrombectomy
  → one stroke problem

- focal seizure favored over recurrent ischemia + antiseizure management
  → one seizure-related diagnostic problem

Do not atomize one syndrome into separate symptom, imaging, treatment, and mechanism problems.

---

## 8. HANDLE INCIDENTAL FINDINGS

Incidental findings should become their own problem only when this encounter changes or restates their management.

**A block needs at least one `MANAGEMENT` entry whose source is this encounter — `[A]`, `[B]`, or `[C]`.** A recommendation recorded in `[D]` is not one, however current it sounds. No such entry, no block.

A block with an empty `MANAGEMENT` field is not a problem. Delete the block; do not carry a finding forward on the strength of its claim.

Examples that may justify a separate problem:

- an unrelated mass whose follow-up is arranged during this encounter
- structural lesion with its own management branch opened today

If an incidental finding has no meaningful management, surveillance, or diagnostic consequence, retain it only if it materially affects the main problem.

---

## 9. REMOVE LOW-VALUE OBJECTS

Not every allocated object must survive.

One fact, one entry. When two sources state the same thing — the seizure witnessed in `[A]` and again in `[C]` — keep the fuller wording once and drop the other. Duplicates are not corroboration here; they are the same sentence twice.

Remove or subordinate items that add no meaningful clinical information.

Examples:

- `MRI completed` when the meaningful information is `MRI showed acute infarct`
- `PT evaluated` when the useful outputs are current function and disposition recommendation
- duplicate historical facts already represented elsewhere
- redundant restatements of the same deficit

Do not remove information that changes:

- diagnosis
- certainty
- trajectory
- treatment
- safety
- disposition
- follow-up

---

## 10. ORDER PROBLEMS

Order problems by current clinical relevance.

Default order:

1. active or urgent neurologic problem
2. other active neurologic problems
3. important complications
4. consequential incidental/surveillance problems

Do not preserve source-document order if it reduces clinical coherence.

---

## OUTPUT CONTRACT

Return the ledger, then `REUSE` lines if any, then the three validation lines. Nothing else — no object text, no problem headings, no prose, no commentary.

Rules:

- One line per input ID, ascending, no gaps and no repeats.
- A destination must match the object's own bucket. `PROBLEM_LABEL` replaces the need for a claim destination; it is not a move to `CLAIM`. A claim object goes to `PRIMARY_CLAIM` or `CLAIM_QUALIFIER`, never elsewhere.
- Exactly one `PRIMARY_CLAIM` per block, and only when the block has a claim object. Any other claim object is a qualifier.
- Problem numbers must be contiguous from `P1` and must reflect the ordering rules above.
- Discard reasons come from the closed set, verbatim. Free text is not a reason.
- `REUSE` declares a secondary block for an object that already has its one assignment. It never creates a second assignment line, and the stated function must be one the object performs.
- Emit the three validation lines from the ledger you actually wrote, not from the input list.

The next module dereferences these IDs and assembles the Handoff. It does not rewrite.
