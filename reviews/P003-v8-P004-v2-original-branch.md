# P003 v8 / P004 v2 review — original architecture branch

## P003 v8
**Verdict: ACCEPT ARCHITECTURE; mechanical cleanup required before implementation**

The I10/trace correction is correct. P003 architecture is accepted.

Two mechanical cleanup items:

1. Header says `P003 v8` but Status still says `v7`. Fix version metadata.
2. Decision-ID collision: §8 still says P003 will record a new `D-015`, but `D-015` is now already the signer-approved chronic-block rule. Do not overwrite it. Allocate a fresh decision ID when P003 is implemented.

No further architecture change requested for P003.

## P004 v2
**Verdict: REVISE — the general rule and the frozen-case partition currently use different evidence standards**

D-015 is clear and accepted:

> a chronic neurologic block is created only when an encounter management decision is source-grounded as directed at that chronic problem; do not infer target from drug class or general knowledge.

But the proposed frozen partition moves:
- O11 `on apixaban`
- O30 `continue amlodipine`
- O31 `continue atorvastatin`
- O12/O25 apixaban hold/resume

into the chronic infarct block even though those atomic texts, as currently represented, do not themselves state that they are directed at the infarct.

The signer approved that grouping for this synthetic example, so the **acceptance oracle may encode that explicit signer adjudication**. But do not present the mapping as something the general production rule can derive from the current objects.

### Required distinction

P004 must separate:

**A. General production rule**
A chronic problem earns a block only when the representation contains a source-grounded link between management and that problem. If the target is not represented, `03` must not infer it from medication identity or general knowledge.

**B. Frozen acceptance-case adjudication**
For this synthetic case, the signer explicitly placed apixaban hold/resume, amlodipine, and atorvastatin in the chronic infarct block. The v4 oracle may encode that as a reviewed oracle decision even though the current atomic representation does not expose the target link.

That mismatch is a **representation gap**. Record it explicitly. Do not silently turn the oracle into the derivation rule.

### Consequence for future architecture

Do not solve the representation gap inside P004 by adding medication-specific heuristics. The likely durable solution is that a later representation/version carries a management-target relation or sufficiently explicit management text. That is outside P004 unless separately proposed.

### Decision IDs

P004 currently reserves `D-016` to supersede D-014. Because P003 also needs a fresh decision ID after implementation, assign IDs sequentially at the time of recording and update both proposals accordingly. Do not hard-code an ID that may collide.

### O10

O10 -> DISCARD remains accepted.

### O54 / D-014

The supersession logic is accepted: residual aphasia may render under the chronic infarct block while remaining excluded as seizure evidence.

No signer escalation is needed for these points. They are consistency/provenance issues.
