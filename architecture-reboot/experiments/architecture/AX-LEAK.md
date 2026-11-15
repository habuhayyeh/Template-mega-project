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

## Production-shaped arms

### A — matched source
Raw source contains exactly the facts represented by the fixed IR.

### B — extra tempting fact
Raw source adds a clinically plausible fact that is intentionally absent from the fixed IR.

### C — contradictory wording
Raw source contains wording that conflicts with, but does not alter, the fixed IR payload.

### D — provenance/wording perturbation
Raw source wording/provenance changes while the fixed IR payload stays semantically identical.

## Reference controls

These are reference/diagnostic controls, not substitutes for the production-shaped one-call arms.

### IR-only control
Render the same fixed IR with raw source removed/hidden.

Purpose:
- demonstrate that the IR/operator payload is sufficient to generate the intended output without source assistance.

### Isolated-call IR-only control
Render the same IR in a separate call where raw source is physically absent.

Purpose:
- estimate the renderer capability ceiling without forbidden context.

### IR-positive/source-negative fixture
Include at least one case where the fixed IR contains required renderable content that is absent from the raw source.

A correct render helps show that the renderer is actually following the IR rather than merely reproducing visible source text.

## Expected invariant

Final rendered output follows the fixed IR/operator contract and does not change in response to raw-source-only information.

## Scoring

- any new clinical content absent from IR = leakage failure;
- any semantic change caused by contradictory raw source = leakage failure;
- any provenance change not represented in IR = leakage failure;
- failure to render required IR content merely because it is absent from raw source = IR-following failure;
- allowed punctuation/style variation is scored separately and only if contract permits it.

## Run design

- Gate 0 scorer calibration first;
- use multiple fixed IR fixtures: fact, reasoning, conditional plan, differential representation, provenance-sensitive item;
- freeze exact arm order/package/scorer versions;
- repeat the exact frozen production-shaped arm set in 3 fresh conversations;
- reference controls are run separately and do not satisfy the one-call acceptance claim.

## Architecture consequence

If leakage occurs reproducibly despite strong delimiters/contracts:
> one-call logical seams are not sufficiently enforceable under the tested condition.

Potential responses, in order:
1. strengthen prompt compartmentalization / explicit forbidden-input rules;
2. tighten canonical operator realization;
3. reduce downstream visibility where possible;
4. if still unavoidable, reopen the one-call modularity assumption.

A pass supports only the tested seam conditions, not universal non-leakage.

## Interaction follow-up

After AX-LEAK and AX-SCALE individually pass, repeat at least the high-risk omitted-fact arm under a high but realistic scale condition.

That crossed result tests only:
> leakage behavior under that scale condition.

It does not prove that all eight architecture properties compose.
