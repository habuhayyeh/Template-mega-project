# DeepSeek review — human-review gate and B1 advance

**Reviewed:** D-050/D-051, A V2.1, B1 reviewed-input contract, reviews 145.
**Status:** peer review. No implementation.

## Verdict

Proceed to B1 with a physician-reviewed, frozen A2 handoff.

Do not keep optimizing A2 for autonomous reproducibility. The signer has defined the acceptance standard:
reviewably good enough, with physician review at every gate.

One condition: the review must be **structured enough to see omissions**. Otherwise “reviewably good” is
not met for A2.

## Why the condition matters

Run 2 is materially better, but it still:

- omitted the T258 MRI plan;
- misidentified the future continue/stop medication decision as an EEG/MRI target;
- selected only CBC from a compound cruise workup;
- may have omitted a disposition action.

A physician reading a list of spans may not notice what is missing from a 300-record packet. Missing
precautions, discontinuations, or compound targets are exactly the errors that are hard to see in a
compact list.

Human review is a valid gate. It is not a substitute for a reviewable artifact.

## Review aid — not a validator

Before freezing A2, give the physician a one-page **action coverage checklist**:

1. list source records containing clinical action wording;
2. for each, show the source phrases and the A2 spans produced;
3. flag records with zero spans;
4. separately list the high-risk items:
   - compound test/workup lists;
   - medication start/load/continue/stop/discontinue;
   - precautions;
   - safety/driving counseling;
   - disposition/admission;
   - future decisions conditioned on tests.
5. physician marks each captured / missing / wrong target.

This is a review worksheet, not a runtime validator and not another model pass. It makes the human gate
real.

## Freeze

- Use the physician-corrected A2 output as the frozen artifact.
- Record its hash and the reviewed action set.
- B1 consumes only that frozen artifact.
- B1 still may not discover or repair A2 omissions; it surfaces `A_ACTION_GAP`.

## B1

The B1 contract is correct:

- reviewed A2 is authoritative;
- packet only for dereference of cited records;
- no action creation/repair;
- state triples with exact phrase and span;
- no problem/section/prose.

Run B1 against the frozen reviewed A2.

## Downstream constraint

The signer’s final-writer rule is consistent:

- C emits typed groups/units and canonical render operators;
- render lexicalizes only;
- no late grouping, action interpretation, section reassignment or clinical decision in render.

Record it for C, not now.

## What not to do

- do not run another A2 prompt optimization cycle;
- do not pick/union runs without physician review;
- do not run B1 on an unreviewed A2;
- do not add a validator stage.

No acceptance, production change or Phase 0.
