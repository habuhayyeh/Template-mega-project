# ChatGPT review 056 — reconciliation of DeepSeek 034 independent Gate 0 review

## Scope

This review reconciles:

- `reviews/deepseek/034-independent-review-gate0.md`
- reviewer state: HEAD `f47e47a`
- current branch state: HEAD `43042739da693db74652c467225982e14bb5e3aa`

The branch is two commits ahead of the state independently reviewed in 034. Therefore each 034 finding is classified against the **current exact files**, not accepted or dismissed merely because it predates HEAD.

## Verdict

> **DEEPSEEK 034 IS SUBSTANTIVELY VALID AND MATERIAL. GATE 0 IS STILL NOT READY FOR SCORER IMPLEMENTATION OR EXECUTION.**

Post-review patches fixed some important defects, but several blocking findings remain, and one current “fix” creates an unsupported semantic oracle rather than resolving the underlying ambiguity.

Architecture remains CLOSED / CONVERGED.
Experiment-design layer remains CLOSED / CONVERGED.
No Phase 0.
No Doximity pilot.

---

# A. Reconciliation of the nine blocking findings

## B1 — S2-TEMP-01 single ground truth
**034:** BLOCKING  
**Current status:** **PARTIALLY FIXED / STILL BLOCKING**

Good:
- O03 now preserves the en dash in `June–November`.
- O02 is now `2024-02`.

Still wrong:
- frozen substrate O01 = `2024-02 documented`;
- current oracle O01 = `2024-02`;
- current clean parent O01 = `2024-02`.

Therefore the clean parent still fails the written rule:

> S2 does not alter temporality recorded in the substrate.

Also:
- the frozen substrate uses **status current** for O05/O06/O07;
- oracle normalizes these to a `temporal` value `current`.

That may be a legitimate downstream normalization someday, but it is not “copied verbatim from FROZEN-SUBSTRATES.md” as the oracle currently claims.

### Required correction

The oracle must preserve source annotation dimensions rather than normalize them silently.

For CASE-01:
- O01 temporal = exactly `2024-02 documented`;
- O02 temporal = exactly `2024-02`;
- O03 temporal = exactly `June–November`;
- O04 temporal = exactly `now`;
- O05/O06/O07 carry source **status** `current`, not invented `temporal=current`, unless a separately frozen annotation-normalization contract says otherwise.

The clean parent must match the exact frozen substrate values for every S2 temporal field it emits.

---

## B2 — schema field→predicate map contradicts predicates
**034:** BLOCKING  
**Current status:** **FIXED**

The S1 authority families are now disjoint:
- S1-AUTH-01 = adoption/final-state fields;
- S1-AUTH-02 = selected/final-claim fields.

The current schema map reflects the split.

Keep this fixed.

---

## B3 — S4-INC-01 seeds collide with S4-COMP-01
**034:** BLOCKING  
**Current status:** **FIXED / ACCEPTED**

Current `S4-COMP-01` explicitly scopes its problem domain to:

> `S4.problems ∩ S3.rendered`

This makes:
- S4 problem addition/removal owned by S4-INC-01;
- completeness within mutually recognized problems owned by S4-COMP-01.

That is an acceptable experiment-local predicate decomposition and prevents the two S4-INC seeds from necessarily double-firing S4-COMP.

Keep this wording frozen unless a real counterexample appears.

---

## B4 — G0-S2-06 schema invalid / duplicates adoption-evidence defect
**034:** BLOCKING  
**Current status:** **STILL BLOCKING**

The current generator improved mutation atomicity:

> adoption `false -> true` only

But the resulting artifact is still:

```
adoption: true
evidence: null
```

while the local schema says:
> evidence is required when adoption is true.

So G0-S2-06 is now a single-field mutation but **schema-invalid**.

It also reproduces the same malformed state that G0-S2-05 was intended to test:
> adoption true without evidence.

Therefore it cannot cleanly calibrate S2-ADOPT-01.

### Preferred repair

For CASE-01, mutate:

> O01 adoption `false -> null`

and leave evidence null.

That is:
- one field;
- schema-valid;
- wrong against the frozen expected adoption `false`;
- isolated from the “true requires evidence” rule.

Alternative:
- build a separate CASE-02 clean S2 parent and design a schema-valid one-defect inversion there.

Do **not** use `false -> true` with null evidence.

---

## B5 — seed inventory false / S4-REP-01 exclusion
**034:** BLOCKING  
**Current status:** **PARTIALLY FIXED / ONE IMPORTANT ERROR REMAINS**

Good:
- current summary now says 15 generated seed artifacts.
- it no longer claims every listed future seed has an artifact.

Still wrong:
- rows such as G0-S1-03, G0-S2-02, G0-S2-04, G0-S3-03 and G0-S4-05 are still labeled `RUNNABLE` in the table even though the text says they are `NOT_IN_PILOT`.

These statuses must agree.

### More important: S4-REP-01 should be active

034 correctly noted that the stated reason for excluding S4-REP-01 was false.

CASE-01 already has:
- S3 `selected_rep = R1`;
- S4 units carrying `representation = R1`.

Therefore CASE-01 can directly test:

> S4 must consume the exact representation selected by S3.

This property does **not** require multiple approved representations.

The current exclusion is circular:
> G0-S4-05 is excluded because S4-REP-01 is inactive; S4-REP-01 is said to be inactive because no pilot case produces the condition.

But CASE-01 does produce the condition.

### Required correction

Reactivate:
- `S4-REP-01`;
- `G0-S4-05`.

The pilot should then have:
- 14 active predicates;
- 16 active seeds, assuming the rest of the current map remains unchanged.

Keep S2-REP-02 inactive until a multiple-approved-representation case exists.

---

## B6 — S2-ADOPT-01 undecidable for most objects
**034:** BLOCKING  
**Current status:** **NOT ACTUALLY FIXED; CURRENT ORACLE OVERREACHES**

The current oracle now assigns adoption expectations to all seven objects.

That does not by itself resolve 034's concern.

Several values were not frozen by the case and may conflate different concepts.

Most concerning:

> O07 = `adoption: false`

But O07 is:
> “aspirin 81 daily, unchanged”

from the current transcript.

The CASE-01 fixture says:
> O07 is a current medication fact and cannot **adopt the infarct**.

That is not the same proposition as:
> O07 itself has encounter-level adoption = false.

This risks conflating:
1. whether an object/source fact is current;
2. whether a historical diagnosis is adopted as a current neurologic problem/formulation;
3. whether a management action semantically links to a diagnosis.

Those must not be collapsed into one oracle boolean merely to make the predicate scoreable.

### Required correction

For this adoption-discriminator pilot, freeze only the adoption targets the case actually adjudicates.

Recommended:
- CASE-01: O01 prior infarct = false;
- CASE-02: O01 prior infarct = true, supported by the explicit current statement;
- CASE-09: O01 prior infarct = true, supported by the explicit management linkage relation.

Do not invent adoption values for O02–O07 unless the adoption contract explicitly defines what that boolean means for current facts, plans and medication records.

The oracle should expose something like:

```
expected.adoption_targets:
  O01: false
```

rather than pretending every object has a signer-frozen adoption truth.

This is an execution-schema/oracle clarification, not an architecture reopen.

---

## B7 — pass rule cannot distinguish predicate-level scorer from layer-level scorer
**034:** BLOCKING  
**Current status:** **STILL BLOCKING**

Current artifacts specify:
- expected predicate ids;
- owner/submodule.

But no scorer **finding record** is frozen.

A scorer that only says:
> “S2 defect”

could still satisfy an owner check without proving it distinguishes:
- S2-REP-01;
- S2-TEMP-01;
- S2-ADOPT-01.

### Required scorer output contract

At minimum, every finding must carry:

```json
{
  "predicate_id": "S2-TEMP-01",
  "owner": "S2",
  "artifact_paths": ["/s2/adjudication/0/temporal"],
  "oracle_refs": ["objects.O01.temporal"],
  "status": "FAIL"
}
```

For semantic predicates, a concise structured basis/evidence reference may also be required.

Gate 0 must compare **predicate ids**, not merely layer labels.

This finding schema must exist before scorer implementation.

---

## B8 — contradictory calibration run-count authorities
**034:** BLOCKING  
**Current status:** **STILL BLOCKING**

`G0-SEEDS.md` now correctly says calibration policy derives from each predicate's mode.

But `00-GATE0-MANIFEST.md` still contains:
- family-level mode labels;
- family-level run counts;
- procedure language that says “semantic families” repeat three times.

That conflicts with the predicate-level model.

### Required correction

Make one authority:

> Gate 0 reads the exact predicate mode from the frozen predicate registry.

Then Gate 0 maps:
- MECHANICAL -> deterministic calibration policy;
- SEMANTIC/HYBRID -> frozen semantic calibration policy.

Family headings are organizational only and carry no scoring mode or run count.

This does not contradict `predicates.md` saying experiment run count is not a predicate property; this is a separate Gate 0 mapping from **mode** to **calibration procedure**.

---

## B9 — required controls have no artifacts
**034:** BLOCKING  
**Current status:** **PARTIALLY FIXED / STILL BLOCKING EXECUTION**

Now present:
- one integrated clean parent spanning S1→S4;
- 15 seed artifacts;
- oracle;
- generator;
- generated manifest.

One integrated clean parent is acceptable for this pilot; separate physical parent files per layer are not necessary if the scorer evaluates the relevant layer independently.

Still absent:
- required harmless-variation control artifact(s);
- scorer implementation;
- Gate 0 run records.

The scorer being absent is expected at this build stage, but Gate 0 cannot be called executable until it exists.

### Required control before Gate 0 run

Materialize at least one frozen harmless valid variation appropriate to the active semantic scorer(s), with expected zero findings.

The variation must be nontrivial enough that a scorer which merely keys on exact surface form cannot pass.

---

# B. Important non-blocking findings from 034 that remain relevant

## N1 — predicate/active-set ids need durable authority
**Status:** OPEN

The generated manifest contains:
- `PILOT-1`;
- `PILOT-ACTIVE-1`;
- `FULL_SILENCE-1`.

These ids are useful, but their definitions are not themselves frozen in a source registry.

Prefer freezing hashes of the exact controlling files:
- `predicates.md`;
- `schema.md`;
- `G0-SEEDS.md`;
- `make_seeds.py`;
- oracle;
- parent.

At minimum add:
- predicate-registry full content hash;
- seed-spec hash;
- generator hash.

IDs can remain as human labels.

---

## N2 — “three predicates” names four
**Status:** OPEN / CLERICAL

Current `predicates.md` says:

> “and three predicates whose condition no pilot case produces”

then names:
- S2-REP-02;
- S4-REP-01;
- S1-BODY-01;
- S2-CONF-01.

After reactivating S4-REP-01, rewrite the sentence anyway.

---

## N3 — G0-S1-05 is still under-specified and its prose is stale
**Status:** OPEN

The executable seed now appends:

```
subject: old left MCA infarct
anchors: [S01]
candidate_claims: []
salience: {}
```

The semantic defect to detect is:
> context-only neurologic subject incorrectly promoted to an independent candidate.

But a weak scorer could fire because:
- candidate_claims is empty;
- salience is empty.

That would not calibrate the intended semantic boundary.

Also `G0-SEEDS.md` still says:
> “old infarct used only as evidence for the seizure claim”

even though the executable parent is CASE-01 falls, not seizure.

### Strengthen before semantic scorer calibration

Make the planted candidate structurally plausible:
- source-grounded candidate claim from S01;
- valid allowed salience shape;
- no embedded answer field.

The scorer should have to use the oracle/source context to decide:
> no independent assessment question exists.

Do not let it win on malformed/empty candidate structure.

---

## N4 — answer-key blindness
**Status:** MOSTLY FIXED, MUST BE ENFORCED IN HARNESS

Current written rule correctly separates:
- scorer input: artifact + oracle + predicate registry;
- harness-only input: seed manifest + expected predicate + mutation metadata.

Keep the physical/runtime packaging consistent with that rule.

The scorer process must not receive the generated seed manifest or filename-derived expected answer.

---

## N5 — seed/generator provenance
**Status:** PARTIALLY OPEN

Current manifest has full SHA-256 hashes for parent, oracle and seed artifacts using canonical JSON.

Good.

Still add/freeze:
- predicate registry hash;
- seed specification hash;
- generator hash.

This matters because changing any of those changes what Gate 0 means even if the seed JSON bytes are unchanged.

---

# C. Additional current-file issue not resolved by the post-034 patch

## Corpus F-1 still contradicts its own pending product decision

Current corpus correctly says:
> unknown-marker vs omission is blocked on a product decision.

But it still says:
> “a run that omits the slot entirely fails completeness.”

That is premature.

Until the signer decides the required behavior:
- unsupported invention = fidelity failure;
- omission vs explicit marker = not scoreable.

The proposed next action is also still too early:
> “No schema proposal until a run shows the current architecture failing at it.”

Correct sequence:
1. signer/product chooses the required unknown behavior;
2. test that requirement;
3. propose schema only if current representation cannot satisfy it.

A run cannot fail an undecided requirement.

---

# D. Revised readiness after reading the detailed independent report

## Architecture
**CLOSED / CONVERGED**

## Experiment design
**CLOSED / CONVERGED**

## AX-S1S2-D execution specification
**CONDITIONALLY CLOSED**

## Gate 0 build
**NOT READY FOR SCORER IMPLEMENTATION YET**

The remaining pre-scorer blockers are:

1. fix temporal source-of-truth mismatch;
2. repair G0-S2-06 to a schema-valid isolated adoption mismatch;
3. narrow/define the adoption oracle rather than inventing all-object truth;
4. reactivate S4-REP-01 and G0-S4-05;
5. define predicate-level finding output schema;
6. collapse Gate 0 run-count authority to predicate-mode mapping;
7. reconcile seed inventory statuses;
8. strengthen G0-S1-05 so it cannot be detected by structural shortcuts;
9. add/freeze harmless-variation control specification/artifact;
10. freeze registry/spec/generator identities.

The detailed 034 review therefore **does change the current readiness verdict**.

No scorer implementation yet.
No Gate 0 run.
No Doximity pilot.
No Phase 0.
