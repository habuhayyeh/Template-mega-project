# AX-I3 — proposition-boundary and object-extraction stability

**Status:** DESIGN ONLY / UNRUN

## Question

Can I3 reproducibly decompose fixed source spans into source-faithful clinical propositions without unstable merge/split, hedge, negation, or anchor behavior?

## Architecture claim under test

Stable source-linked semantic objects are a viable substrate for downstream modules under the tested frozen conditions.

## Frozen input

Use fixed mechanically bounded spans:
- chart line;
- transcript utterance;
- speaker turn;
- multi-proposition sentence;
- conditional sentence;
- negated statement;
- hedged statement;
- mixed current/historical content.

Do not vary source boundaries across repetitions.

Paste-layout/I1-I2 behavior is intentionally outside this experiment and must be characterized separately before production-shaped claims rely on it.

## Artifact under test

I3 object extraction only.

I4 annotation should not be required unless a scoring property genuinely belongs there.

## Scoring dimensions

- proposition coverage/recall;
- unsupported proposition fabrication;
- proposition boundary agreement;
- merge/split consistency;
- negation preservation;
- hedge/uncertainty preservation;
- condition preservation;
- source-span anchor correctness;
- semantic identity matching across runs.

Do not require literal object IDs across fresh conversations unless a deterministic ID-generation contract is separately frozen and under test.

Cross-run matching should use source anchors plus proposition/semantic matching.

Literal-ID behavior may be characterized descriptively, but it is not currently an architecture acceptance requirement.

## Fixture design

Include:
- one span -> one proposition;
- one span -> several propositions;
- repeated near-duplicate propositions;
- same clinical proposition in two sources;
- attribution-sensitive proposition;
- temporal qualifier;
- conditional management;
- reasoning statement containing claim + qualifier/etiology.

## Run design

- Gate 0 scorer calibration first;
- artifact-level I3 batch;
- freeze exact case/span IDs, order, package/scorer versions;
- repeat exact frozen spans in 3 fresh conversations;
- for unstable cases, compare clause-level extraction and more source-anchored identity as candidate mitigations.

## Claim scope

The default gate supports only a narrow statement such as:

> the scored I3 properties passed/agreed 3/3 under this frozen fixture/batch condition.

It does **not** estimate a population stability rate or prove general proposition-boundary stability.

If a later question requires a frequency/probability estimate, design additional repetitions for that question rather than silently extending the 3-run gate.

## Interpretation

If I3 is unstable, downstream reproducibility claims using model-generated I3 artifacts are contaminated.

Likely responses before changing topology:
1. stronger clause/source anchors;
2. conservative extraction;
3. allow related/duplicate objects and defer canonicalization to S2;
4. avoid forcing I3 to solve semantic equivalence.

Only reopen INGEST topology if those measures cannot produce a usable stable substrate.

## Operational granularity and downstream constructibility

Two questions, scored separately:

1. **Granularity** — is the object set stable and at an operationally useful size? Report objects per
   span, split rate, merge rate. A boundary that is stable but produces unusable granularity has failed
   for a different reason than one that is unstable.
2. **Constructibility** — can valid units be built from the I3 objects **without splitting or merging
   them downstream**? If S4 must re-split an I3 object to build a correct unit, the granularity is wrong
   even when it is stable.

Constructibility is the check that matters: stability alone is achievable by emitting one object per
sentence, which no downstream module can use.

## Operational proposition-boundary rule

Split a clause into separate objects when the propositions can vary independently in **truth,
temporality, negation, condition, attribution, certainty/hedge, or downstream use**. Keep scoped
qualifiers attached to the proposition they qualify unless the qualifier is independently meaningful.

**Constructibility, restated:** downstream modules may group objects into units; they may not repair
object boundaries by splitting or fusing source propositions. If a correct unit requires re-cutting an
I3 object, that is an ingest defect surfaced by S4, not an S4 problem to solve.
