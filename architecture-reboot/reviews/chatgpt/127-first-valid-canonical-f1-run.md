# Review 127 — first valid canonical File 1 run

## Provenance

This is the first execution produced from the actual runnable canonical `01-RECONCILED-EVIDENCE.md`
rather than from a review artifact.

D-041 supersedes the earlier D-040 empirical freeze claim.

## Verdict

**PARTIAL PASS — architecture is viable, but reference/action fidelity still requires one bounded rerun.**

## What worked

- complete handoff with closing marker;
- compact lazy decomposition rather than global atomization;
- event/timeline facts are mostly coherent and downstream-separable;
- source reasoning remains separate;
- unresolved items are limited and clinically relevant;
- no PRIMARY/BACKGROUND/problem rendering decisions.

## Material defects

### 1. Invalid/invented source ids

At least one item cites record ids that do not exist in the Scribe packet (e.g. `P1.132`, `P1.141`).

This is a hard reference-integrity failure.

### 2. Question-only refs used as answer support

Some facts cite transcript records that only contain the clinician's question, not the answer. A question
cannot support the truth of its presumed answer.

Example class:
- “ever had seizures before?” cannot itself support “no prior seizure history.”

### 3. Action-state upgrade

The handoff states that another Keppra load was received in ED/EMS. The source instead contains:
- reported prior doses;
- a neurology recommendation for a new 1500-mg load;
- later discontinuation of that load.

Administration of the new ED load is not established.

This is exactly the action-state error File 2 is meant to prevent, but F1 must not create it.

### 4. Attribution overreach

Some transcript summaries assign speaker roles (patient/family/etc.) more strongly than the raw SPK labels
safely establish.

F1 should use source-neutral wording when speaker identity is not explicitly supported in the relevant record.

### 5. Unresolved diagnostic interpretation leak

An UNRESOLVED item may summarize source disagreement/uncertainty, but should not create a new diagnostic
classification problem unless a source explicitly states that uncertainty.

## Bounded fix applied

Canonical File 1 now requires:
- every ref must exist verbatim in the input packet;
- no T/P1 transposition;
- every cited ref must support at least one clause;
- question-only refs cannot support answers;
- no action administration inferred from recommend/order/discontinue states;
- no stable SPK identity inferred without source support;
- UNRESOLVED stays source-level.

## Next

One rerun of the patched canonical File 1 on the same packet is justified.

If reference/action fidelity passes, freeze F1 behavior and move to File 2.

Do not run File 2 before that rerun.
