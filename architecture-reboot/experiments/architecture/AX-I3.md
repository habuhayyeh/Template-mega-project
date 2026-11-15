# AX-I3 — proposition-boundary and object-extraction stability

**Status:** DESIGN ONLY / UNRUN

## Question

Can I3 reproducibly decompose fixed source spans into source-faithful clinical propositions without unstable merge/split, hedge, negation, or anchor behavior?

## Architecture claim under test

Stable source-linked semantic objects are a viable substrate for all downstream modules.

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

Do not require literal object IDs unless the ID-generation contract itself is under test.

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

Artifact-level I3 batch.
Repeat exact frozen spans in 3 fresh conversations.
For unstable cases, compare clause-level extraction and more source-anchored identity as candidate mitigations.

## Interpretation

If I3 is unstable, every downstream stability claim is contaminated.

Likely responses before changing topology:
1. stronger clause/source anchors;
2. conservative extraction;
3. allow related/duplicate objects and defer canonicalization to S2;
4. avoid forcing I3 to solve semantic equivalence.

Only reopen INGEST topology if those measures cannot produce a usable stable substrate.
