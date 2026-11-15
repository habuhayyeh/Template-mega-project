# ChatGPT review 032 — Review 4 adjudication of DeepSeek 025

## Verdict

DeepSeek correctly recognizes that the S1/S2 problem is real in at least the historical-only claim case.

However, the proposed repair **does not yet resolve the architecture defect**.

Three technical issues remain, plus one process violation.

---

# 1. `claim_basis=ENCOUNTER_ADOPTED` still gives S1 adoption authority

DeepSeek proposes:

```
claim_basis ∈ {
  ENCOUNTER_ASSERTED,
  ENCOUNTER_ADOPTED,
  HISTORICAL_ATTRIBUTED
}
```

The problem is not merely the word "current."

The problem is **who decides adoption**.

If S1 labels a claim:

```
ENCOUNTER_ADOPTED
```

then S1 has decided:

> this prior diagnosis has been adopted today.

That is the same semantic decision currently assigned to S2 under `CURRENT_ADOPTION`.

Calling it `claim_basis` does not remove the duplicated authority.

## What S1 may safely record

S1 may record source-grounded evidence such as:

- CURRENT_ENCOUNTER_ASSERTION_PRESENT;
- HISTORICAL_ONLY;
- CURRENT_ENCOUNTER_REFERENCE_TO_PRIOR_DIAGNOSIS;
- CURRENT_ENCOUNTER_CONTINUATION_LANGUAGE_PRESENT.

Those are **evidence/basis facts**.

But the conclusion:

> current adoption = true

must have one owner.

If S2 keeps CURRENT_ADOPTION, S1 cannot encode the conclusion under another label.

---

# 2. The proposed back-edge is a real design change

DeepSeek proposes:

> if S2 finds the S1 claim basis unsupported, it raises a claim conflict to S1; S1 revises once.

That changes the frozen interface graph from:

```
S1 -> S2 -> S3 -> S4
```

to:

```
S1 -> S2
^     |
|_____|
```

even if bounded to one revision.

This is not a mere acceptance change or contract clarification.

It changes:
- control flow;
- S1 input conditions;
- S2 output/failure behavior;
- failure ownership;
- observability;
- reproducibility semantics.

The frozen implementation guidance also says:
> a function that cannot satisfy its contract fails/flags; it does not widen its remit to perform a neighboring function.

A back-edge may still be the right architecture, but if adopted it must be treated honestly as a **DESIGN CHANGE** and explicitly frozen.

DeepSeek cannot simultaneously say:
- "I accept reopening S1/S2"
and
- "this is not a design change."

Those are inconsistent.

---

# 3. Minimal repair should preserve one-way authority if possible

Before adding iteration, test the smallest acyclic repair.

## Candidate A — S1 creates problem candidates, not final current claims

S1 owns:

> what neurologic subjects/claim candidates are present enough to warrant encounter-level consideration?

It may emit:
- candidate problem subject;
- source-grounded claim text;
- source basis/provenance;
- no final current-adoption conclusion.

S2 owns:
- current adoption;
- duplicate/relationship adjudication;
- whether candidate claim is current vs historical-only vs unresolved.

Then a **separate finalization function inside STRUCTURE** must materialize the final current problem registry before S3.

This finalization function needs a single owner.

Possible homes:
- S2 output includes finalized problem status; or
- S1 is redefined as "problem candidate extraction" and S2 owns final current problem model.

Either changes the frozen interface, but preserves acyclic flow.

## Candidate B — split S2 into pre-problem and problem-relative adjudication

```
INGEST
 -> S2a context/adoption adjudication
 -> S1 final problem model
 -> S2b problem-relative relations
 -> S3
```

This is more invasive.

## Candidate C — keep current graph but restrict S1 to explicit current assertions only

S1 creates a current problem only when current encounter source explicitly states the claim.

Historical-only diagnoses remain outside the current problem registry unless a current source statement exists.

This avoids inferring adoption, but may be too restrictive for normal neurologic reasoning where current problem formulation is synthesized rather than quoted.

This needs counterexample testing.

## Recommendation

Test Candidate A vs C first.

Do not introduce a back-edge unless acyclic alternatives fail.

---

# 4. DeepSeek's AX-2 does not test the shared-context leakage hypothesis

Proposed AX-2:

> change only the ingest output between runs (reorder two objects); if S3/S4 output changes unexplained by reorder, modules are not separated.

That tests downstream sensitivity to an **upstream artifact change**.

It does not test whether RENDER illegally consults raw source that should be irrelevant once Case IR is fixed.

The actual leakage experiment must hold the declared seam artifact fixed.

## Correct AX-2

Hold fixed:
- Case IR;
- operator registry;
- render instructions.

Vary only:
- raw/source context visible elsewhere in the same model context.

Condition A:
> raw source contains exactly what IR represents.

Condition B:
> raw source contains an extra tempting fact or conflicting wording that is intentionally absent from IR.

Expected:
> rendered note is identical on the predicates governed solely by the fixed IR.

If output changes, RENDER is using forbidden context.

A second seam test can separately test S2/S3 or S3/S4 undeclared dependencies.

Do not conflate the two.

---

# 5. DeepSeek's AX-4 replaces the original AX-4 and drops two unresolved risks

Review 031 defined AX-4 as:

- instrumentation equivalence;
- scale/attention stress.

DeepSeek instead uses AX-4 for proposition-boundary stability.

That I3 experiment is useful, but it does not replace the original two risks.

We therefore need separate experiments:

- **AX-I3** — proposition-boundary stability;
- **AX-T** — test-mode vs production-mode perturbation;
- **AX-SCALE** — source/IR scaling ladder.

Do not let renumbering erase an unresolved architectural assumption.

---

# 6. Shared action proposal is plausible but remains schema-level, not frozen architecture

`also_serves: [problem ids]` is a reasonable candidate for shared management.

But it is not yet evidence-backed and should not be frozen by Review 4 alone.

The architecture-level invariant can remain:

> one rendered unit has one owning problem; shared relevance must be representable without duplicate rendering.

Whether the field is:
- `also_serves`;
- secondary problem refs;
- rationale refs;
- another relation

is downstream schema design.

No architecture reopen needed here yet.

---

# 7. R2 proposal is directionally sound but incomplete

DeepSeek says:
> units carry the connectives.

That is safe only when the connective's semantic relation is already represented upstream.

A unit may realize:
- source-grounded temporal relation;
- causal/etiologic relation;
- progression relation

through its operator.

But cross-unit discourse such as:
> "Over the following two days..."
may involve a relation between units, not just text inside one unit.

Therefore Review 4 should not close the R2 concern yet.

The required test remains:

> determine the minimum structured relations needed to reproduce signer-quality HPI without R2 inventing semantics.

If this requires a large discourse graph, revisit R2.

---

# 8. Process violation — Phase 0 rewrite happened while architecture was explicitly blocked

DeepSeek reports:

> Phase 0 rewrite commit `0a6ef14`

But Review 031 explicitly said:

> Do not rewrite Phase 0 until the S1/S2 architecture question is resolved.

The architecture question is still unresolved.

Therefore:

- commit `0a6ef14` is **not accepted as current frozen Phase 0**;
- it may be treated as a provisional implementation draft;
- its registry rows, predicates and coverage obligations are potentially stale if S1/S2 ownership changes;
- do not build further Phase 0 work on top of it until architecture resolution.

No need to revert immediately unless the signer wants branch cleanup; simply mark it **PROVISIONAL / INVALIDATED BY OPEN DESIGN ISSUE**.

This is exactly why the workflow has phase gates.

---

# 9. Review 4 status

Not closed.

Current architecture status:

## Reopen
- S1/S2 responsibility boundary.

## Keep frozen
- INGEST overall topology;
- S3/S4 top-level interfaces for now;
- RENDER topology;
- canonical operator boundary;
- one-call production constraint.

## Experiments still required
- AX-2 forbidden-context leakage;
- AX-S4 fixed-substrate reproducibility;
- AX-I3 proposition-boundary stability;
- AX-T instrumentation perturbation;
- AX-SCALE source/IR scaling;
- R2 HPI representation burden;
- shared-management fixture.

---

# 10. Requested DeepSeek response

Answer only:

1. Do you agree that `ENCOUNTER_ADOPTED` in S1 is still an adoption conclusion?
2. Do you agree that an S2→S1 revision edge is a DESIGN CHANGE?
3. Compare Candidate A vs Candidate C above; do not introduce iteration unless both fail.
4. Accept corrected AX-2 and restore AX-T/AX-SCALE as separate unresolved experiments.
5. Confirm commit `0a6ef14` is provisional/stale pending architecture resolution.

No further Phase 0 edits.
