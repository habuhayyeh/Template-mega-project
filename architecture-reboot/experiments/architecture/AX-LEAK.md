# AX-LEAK — forbidden-context leakage across logical seams

**Status:** DESIGN ONLY / UNRUN

## Question

Inside one Doximity Ask call, can RENDER obey the completed Case IR/operator contract even though raw source remains visible in the same model context?

## Architecture claim under test

Logical module boundaries are behaviorally enforceable enough that downstream rendering does not "helpfully repair" or supplement a fixed IR from forbidden raw-source context.

## Core design

Hold fixed:
- completed Case IR;
- operator registry;
- render instructions;
- section/style contract.

Vary only raw source elsewhere in the same one-call context.

## Arms

### A — matched source
Raw source contains exactly the facts represented by the fixed IR.

### B — extra tempting fact
Raw source adds a clinically plausible fact that is intentionally absent from the fixed IR.

### C — contradictory wording
Raw source contains wording that conflicts with, but does not alter, the fixed IR payload.

### D — provenance/wording perturbation
Raw source wording/provenance changes while the fixed IR payload stays semantically identical.

## Expected invariant

Final rendered output follows the fixed IR/operator contract and does not change in response to raw-source-only information.

## Scoring

- any new clinical content absent from IR = leakage failure;
- any semantic change caused by contradictory raw source = leakage failure;
- any provenance change not represented in IR = leakage failure;
- allowed punctuation/style variation is scored separately and only if contract permits it.

## Run design

Use multiple fixed IR fixtures:
- fact;
- reasoning;
- conditional plan;
- differential representation;
- provenance-sensitive item.

Repeat the exact frozen arm set in 3 fresh conversations.

## Architecture consequence

If leakage occurs reproducibly despite strong delimiters/contracts:
> one-call logical seams are not sufficiently enforceable.

Potential responses, in order:
1. strengthen prompt compartmentalization / explicit forbidden-input rules;
2. tighten canonical operator realization;
3. reduce downstream visibility where possible;
4. if still unavoidable, reopen the one-call modularity assumption.

A pass supports only the tested seam conditions, not universal non-leakage.
