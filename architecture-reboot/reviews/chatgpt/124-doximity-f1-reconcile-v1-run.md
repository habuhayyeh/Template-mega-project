# Review 124 — Doximity F1-RECONCILE-V1 execution

## Verdict

**PARTIAL PASS — cardinality problem solved; reconciliation granularity still too coarse.**

The Doximity Ask/GPT-4o run completed successfully with a closing `@@END` and produced a compact handoff:
- 13 FACT items;
- 3 SOURCE_REASONING items;
- 4 UNRESOLVED items.

This is a major improvement over global atomicization, which truncated after 175 objects.

## What worked

1. **Completion**
   - full handoff returned;
   - no truncation;
   - no second near-copy of the entire source packet.

2. **Reference-backed compression**
   - facts cite Scribe record ids;
   - duplicates and event evolution were meaningfully consolidated.

3. **Conflict / uncertainty preservation**
   - episode-duration disagreement retained as UNRESOLVED;
   - uncertain head-version laterality retained;
   - unclear substance-use screening retained;
   - unavailable CT result retained.

4. **Source reasoning stayed separate**
   - neurologic/ED impressions and collateral suspicions were not simply converted into final encounter truth.

5. **No final problem architecture**
   - the run did not assign PRIMARY/BACKGROUND or render decisions.

## Material failure: overcompression

Several FACTs combine propositions that should remain separate downstream decision units.

Examples by structure, without patient content:
- one fact combined demographics/presentation + past medical/surgical history + allergy state + current exam;
- one fact combined unrelated gynecologic history + seizure history + family history;
- one fact combined supplements + substance-use screening + employment + residence.

These bundles cannot be passed unchanged to later problem/section/use decisions.

This violates the intended lazy-splitting rule: compression should merge duplicate/evolving statements about
the **same clinical subject**, not unrelated content merely to reduce item count.

## Reference-integrity defects

At least some FACT wording includes clauses whose supporting Scribe record ids are not listed in that
FACT's `refs`.

That means later functions cannot reliably dereference the exact support for every clause.

The handoff must satisfy:

> every independently meaningful clause in a FACT is supported by at least one listed ref.

## Support-label ambiguity

`support: AGREES | EVOLUTION | SINGLE_SOURCE | CONFLICT` is being applied to large heterogeneous bundles,
which makes the label poorly defined.

This is largely downstream of overcompression. Once one FACT is restricted to one clinical subject/
trajectory, the support relationship becomes meaningful again.

## Design correction

Keep lazy decomposition, but add three invariants:

### A. One subject / one trajectory

A FACT may combine multiple records only when they describe:
- the same event/clinical subject;
- the same longitudinal state/trajectory;
- or direct corroboration/evolution of that subject.

Do not combine facts merely because they belong to the same broad history section.

### B. Downstream-separability test

Before combining two propositions ask:

> Could a later function reasonably need to give these different problem membership, temporal stance,
> section placement, inclusion/disposition, or action handling?

If yes, keep them separate.

### C. Local reference completeness

Every independently meaningful clause in `fact:` must have at least one supporting id in that FACT's
`refs:`.

Do not borrow support from another FACT or from uncited packet context.

## Result interpretation

The execution evidence supports D-039 lazy decomposition.

It does **not** support freezing the current F1 output contract yet.

The next revision should be narrow: prevent heterogeneous bundling and enforce local reference completeness.
Do not return to global atomicization.

## Next empirical test

Run the revised F1 on the same packet.

Desired behavior:
- complete;
- still compact;
- more than 13 facts is acceptable;
- far fewer than the 175-object atomic corpus;
- each FACT is independently usable downstream;
- every clause has local supporting refs.
