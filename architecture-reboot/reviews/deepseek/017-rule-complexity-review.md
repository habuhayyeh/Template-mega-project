# DeepSeek independent review — rules that cost more than they return

**Scope:** current `GATE0-C3` package, no code/schema changes. This is my independent read; it is not
coordinated with ChatGPT's review.

## 1. One identity bump per wording change

`make_seeds.py:40-41` couples `PILOT-3`, `ACTIVE-PILOT-3`, `SCHEMA-4`, `ORACLE-4.0` and `GATE0-C3`.
A wording correction, a predicate addition, a fixture and a packet change all force the same
regenerate/invalidate cycle. We went SCHEMA-2→4 and GATE0-C1→C3 in one day, mostly for semantic prose.

**Cost:** every clarification invalidates packets, references and evidence hashes.
**Simplify:** separate three identities:
- **shape id** — changes only when a field/ownership/contract shape changes;
- **semantic-policy id** — changes when predicate wording changes;
- **packet-set id** — changes whenever packet bytes change.
Prose clarifications bump only the policy id; references are keyed to packet bytes plus semantic-policy
id, not to a whole-campaign rename.

## 2. Two scored predicates for one field

`S2-CAUSAL-01/02`, `S3-ROLE-01/02`, and `S4-ROLE-01` split shape and meaning into separate scored
predicates. That created gate special-cases, seed overlap, and structural-only seeds with no semantic
packet.

**Cost:** every new field needs two predicates, a gating rule, extra seeds and extra review.
**Simplify:** one field gets:
- one **validator** — non-scored shape/reference check that runs before review and can block it;
- one **semantic predicate** — the only scored question.
Shape failures are unit fixtures, not Gate-0 predicates/seeds.

## 3. Full silence across every active predicate

`00-GATE0-MANIFEST.md:8` requires every other active predicate in the layer to be silent. With five
semantic predicates, every seed now needs references for all of them; one clinical question pulls the
whole semantic family.

**Cost:** 44 packets and a large signer workload for five clinical questions.
**Simplify:** specificity should cover:
- all active mechanical predicates in the layer;
- the semantic predicate family actually under test.
Unrelated semantic `UNDECIDABLE` is out of scope, not a failure. If full-silence is required, score it
per family, not across every semantic axis at once.

## 4. One packet per predicate per artifact

`build_packet()` creates one packet per semantic finding. That produces 44 packets, many of which are
the same case context repeated with one question changed.

**Cost:** signer fatigue and duplicated context; most packets are `SILENT` on everything except one.
**Simplify:** one packet per artifact/layer carrying all semantic questions for that layer, with
per-predicate verdict slots. Expected packet count drops from 44 to roughly the number of S2/S3
artifacts (~29), and the judge sees one coherent case instead of near-duplicates.

## 5. One seed per predicate

`make_seeds.py:341` requires a seed for every active predicate. This produced artificial seeds
(`G0-S2-01`, `G0-S4-12/13`) that test plumbing, not clinical distinctions, and then had to be removed or
gated.

**Cost:** seed churn and specificity noise.
**Simplify:** Gate-0 seeds only for clinical/semantic distinctions. Projection, shape, hash and
dependency checks belong in unit fixtures. Keep seed mutations one-field, but do not require one per
predicate.

## 6. “Clean parent” is overloaded

`S3_CASE01_NOT_RENDERED_CLEAN` and `S2_CASE10_CAUSAL` are layer-specific fixtures, not full clean
cases. Supporting them required `case_oracle` and `dependency_context_by_parent`
(`gate0_harness.py:163,574,587`) — special cases that weaken the “clean parent” model.

**Cost:** harness branches, dependency exceptions, confusing counts.
**Simplify:** separate **campaign parents** (full four-layer cases) from **fixtures** (layer-local test
artifacts with explicit oracle/dependency context). The harness should model fixtures directly, not
pretend they are clean parents.

## 7. Governance grows faster than the architecture

`D-024` through `D-029` are five decisions to settle one approval; several are corrections of earlier
attestations. Normative wording is also duplicated in `DECISIONS.md`, `predicates.md`,
`scorer/registry.py`, packet instructions and `schema.md`.

**Cost:** every semantic change is a multi-file consistency exercise; agents spend turns on provenance.
**Simplify:** one **semantics registry** (machine-readable) holding predicate id, assertion, packet
instruction and decision reference; docs render from it. Decisions get `author`, `evidence`, `status`
(`active/superseded/void`) and a single supersession row, not repeated corrections.

## Target shape

- **5 semantic questions:** S1 candidacy, S2 adoption, S2 representation, S2 causality, S3 role.
- **~8–10 mechanical validators**, not scored predicates.
- **One packet per artifact/layer**, not per predicate.
- **~10–12 clinical seeds**, not 36.
- **One semantics registry**, generated docs, separate shape/policy/packet identities.
- Keep: module ownership, Option F signer anchor, D-028 delegation, immutable packet evidence.

No Gate-0 acceptance. No Doximity. No Phase 0.
