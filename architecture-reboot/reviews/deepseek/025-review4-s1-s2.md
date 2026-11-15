# DeepSeek response 025 — Review 4, S1/S2 and the four edges

## 1. Is the S1↔S2 cycle real?

**Partly.** It is real in one case and not in the others, and the difference is whether the claim is *adopted* or *attributed*.

- **Not a cycle:** the claim is what the current encounter asserts. A clinician saying "seizure from the old infarct" has stated a claim; adoption of other objects does not change it.
- **A genuine cycle:** a problem whose only claim candidate is a *prior* diagnosis with no current restatement. S1 must decide "is this the claim?" — which is an adoption question — before S2 decides adoption.

The proposal's own shape hides the fix: S1's output is described as "current problem-level claims", and "current" is doing adoption work inside a module that is not allowed to do adoption.

## 2. Minimal repair — type the claim's provenance, do not reorder the pipeline

**Repair:** every claim carries `claim_basis ∈ {ENCOUNTER_ASSERTED, ENCOUNTER_ADOPTED, HISTORICAL_ATTRIBUTED}`.

- `ENCOUNTER_ASSERTED` — the clinician stated it today. No adoption question.
- `ENCOUNTER_ADOPTED` — the clinician today adopted a prior diagnosis ("continue", "known", "still"). The adoption act is itself a statement, captured by ingest. No S2 question.
- `HISTORICAL_ATTRIBUTED` — neither: the only support is a prior note. The problem renders with explicit attribution (`Known left MCA infarct, documented 2024-02`) and is **not** presented as a current formulation.

With this, S2's adoption decision never determines *which object is the claim*; it determines only whether other objects are used under it. The cycle disappears because "current" stops being inferred and becomes a recorded basis.

**One bounded back-edge remains, and it should be explicit.** If S2 finds that a claim's basis is unsupported — for example an `ENCOUNTER_ADOPTED` with no adoption statement in the source — it raises a **claim conflict** to S1. S1 may revise once, and the revision is recorded. This is a recorded correction, not a silent loop: one back-edge, one revision, logged with the reason.

**Rejected alternative: merging S1 and S2.** It removes the seam by removing the audit boundary. The claim decision and the use decision fail differently — an unsupported claim is a clinical error, a bad use is a placement error — and merging them makes first-divergence attribution guesswork. The repair is cheaper and keeps the audit.

## 3. One problem per unit, with shared action

Real edge case: a management action that serves two problems (e.g. an anticoagulation decision serving both stroke prevention and atrial fibrillation).

**Repair:** a unit renders under exactly one `problem` and may carry `also_serves: [problem ids]`. The line appears once, under the primary problem; the other problems record the reference but do not render it. A problem that only "also serves" gets no unit of its own for that action.

This keeps the uniqueness invariant that catches duplication while allowing a shared action to be honest about what it serves. Splitting the unit would print it twice, which is the failure we already measured.

## 4. R2 expressivity

The tension is real but bounded: R2 may join lines, and HPI reads as a sequence of joined sentences rather than discourse.

I would not widen R2. **Instead, units carry the connectives.** If a section needs "Because she had two episodes, we started levetiracetam", the causal phrasing belongs to the reasoning unit's own text, taken from the source, not manufactured by a composition pass.

Consequence: where the source does not supply discourse, the note reads plainer. That is the correct trade — plainer prose over invented causality. If a specific section genuinely cannot be written this way, that is evidence for a section-specific composition contract, and it should be proposed as one rather than granted to R2 by default.

## 5. Smallest experiments

**AX-2 — seam leakage (smallest, do first).** One case, three runs, changing only the *ingest output* between runs (reorder two objects). If S3/S4 output changes for reasons not explained by the reorder, the modules are not separated inside the shared call. Cost: 3 runs.

**AX-3 — S4 concentration.** One case, five runs. Attribute each difference to a decision id. If differences concentrate in S4, the module is overloaded and splitting should be considered. Cost: 5 runs.

**AX-4 — proposition boundary stability.** One span containing two propositions, five runs, compare object sets. This is the smallest test with the largest downstream consequence: if I3's split is unstable, every unit downstream inherits the variance. Cost: 5 runs.

**AX-2 before AX-3 before AX-4.** AX-2 decides whether the module boundaries exist at all; AX-4 only matters if they do.

---

## What I am not accepting

The review says "reopen only S1/S2". I accept reopening S1/S2, and I reject reopening the operator layer, which the stress evidence supports. But I also want to record that **the S1/S2 repair is not a design change to the frozen architecture** — it types an existing field (`adopted` already exists on objects). It is an `ACCEPTANCE CHANGE` plus a contract clarification, not a redesign.
