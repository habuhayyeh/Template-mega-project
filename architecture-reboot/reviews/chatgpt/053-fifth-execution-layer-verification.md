# ChatGPT review 053 — fifth execution-layer verification

## Verdict

**EXECUTION SPECIFICATION: CONDITIONALLY CLOSED. BUILD PHASE MAY BEGIN.**

The fifth pass resolves the substantive execution-spec blockers from reviews 048–052.

No Doximity experiment may run yet because Gate 0 has not been built or calibrated, but the remaining work is now implementation/build work rather than another conceptual execution-spec redesign.

Architecture remains CLOSED / CONVERGED.
Phase 0 remains untouched.

---

# 1. Active pilot set is now coherent

The three-case pilot now has 13 active predicates:

- S1: `S1-CAND-01`, `S1-CAND-02`, `S1-AUTH-01`, `S1-AUTH-02`
- S2: `S2-REP-01`, `S2-TEMP-01`, `S2-ADOPT-01`
- S3: `S3-INC-01`, `S3-SEL-01`, `S3-ACCT-01`
- S4: `S4-INC-01`, `S4-MEM-01`, `S4-COMP-01`

This is appropriate for CASE-01/02/09.

The following are correctly inactive for this pilot:
- `S1-BODY-01`
- `S2-CONF-01`
- `S2-REP-02`
- `S4-REP-01`
- `S4-ORD-01`
- `S2-ADOPT-02`

No active predicate is now obviously vacuous for the adoption-discriminator trio.

---

# 2. Gate 0 coverage is now complete for the active set

The active map is coherent:

- 13 active predicates
- 15 active calibration seeds

Extra seeds for inactive/future predicates do not block the pilot.

The strengthened candidacy seed now uses a neurologic context-only subject rather than hypothyroidism, which calibrates the actual semantic boundary.

Specificity is now correctly defined as:

> only expected/whitelisted predicates may fire; every other active predicate must remain silent.

That is the correct calibration rule.

---

# 3. Experiment scoring semantics are now coherent

The exact file now correctly separates:

- Gate 0 calibration;
- experiment repetitions;
- run state;
- experiment verdict;
- architecture escalation.

A 2/3 semantic result is now:

> NONCONFORMANT + reproducibility disagreement

not UNSCORED and not a calibration failure.

Architecture escalation is case-local and adjudicative:
- reproducible structural failure opens adjudication;
- it does not itself prove architecture impossibility;
- implementation/schema/substrate/platform causes must be excluded first.

This matches the frozen experiment design.

---

# 4. Corpus/synthetic evidence distinction is now correct

The corpus now explicitly distinguishes:

- realistic signer corpus: blocked until source packages exist;
- derived synthetic architecture fixtures: may proceed, but support interface-conformance claims only.

This is the correct evidence boundary.

F-1 is now correctly framed as an open product/representation question:
- invention of unsupported content is a fidelity failure;
- omission versus explicit marker is not scoreable until the product behavior is decided;
- a schema change is justified only if the required behavior cannot be achieved with the current representation.

---

# 5. Two small exact-file corrections remain

These are local documentation/schema consistency issues, not blockers to beginning the Gate 0 build.

## 5a. S1 forbidden-field set differs between predicates.md and schema.md

`predicates.md` closes/version-controls this forbidden field set:

`{adopted, adoption, adoption_verdict, selected_claim, resolved, status_current}`

But `schema.md` currently says:

`adopted, adoption, selected_claim, current, resolved`

Those are not the same set.

### Required correction

Make `schema.md` reference the exact versioned set from `predicates.md` rather than maintaining a second copy, or make both copies textually identical.

Do not treat a field literally named `current` as forbidden unless that is actually in the versioned predicate set.

## 5b. schema.md field-to-predicate map is incomplete for activated/future-defined fields

The map does not list:
- `S1-CAND-01` because it is semantic;
- `S2-REP-02`;
- `S4-REP-01`.

That is acceptable if the table is explicitly described as a map for the pilot's active field-level checks only.

At present its heading is generic:
> Field -> predicate map

### Required correction

Either:
- rename it to clarify its scope; or
- add rows for the mechanically defined but currently inactive predicates.

This is documentation hygiene, not a design issue.

---

# 6. Gate 0 is still not executable yet — correctly acknowledged

There are still no durable:
- clean S1 parent;
- clean S2 parent;
- clean S3 parent;
- clean S4 parent;
- instantiated mutated seed artifacts;
- scorer implementation/prompt/package;
- Gate 0 run records.

That is now the correct next work item.

The Gate 0 design should not be revised again merely because these implementation artifacts do not yet exist.

---

# 7. Next build sequence

DeepSeek may now proceed with execution-layer implementation:

1. make the two local schema/documentation corrections above;
2. build one reviewed clean parent artifact per required layer for the derived synthetic pilot;
3. instantiate the 15 active seed artifacts from those parents;
4. implement/freeze the scorer for the 13 active predicates;
5. independently review:
   - clean parents;
   - seed single-mutation integrity;
   - scorer logic;
   - seed -> predicate mapping;
6. run Gate 0;
7. only if Gate 0 passes, package the three-case AX-S1S2-D Doximity pilot.

Do not run the pilot before Gate 0 passes.

---

# 8. Status

- DC-001: APPLIED / VERIFIED
- architecture experiment design: CLOSED / CONVERGED
- AX-S1S2-D execution specification: CONDITIONALLY CLOSED
- Gate 0 design: CLOSED ENOUGH TO BUILD
- Gate 0 implementation: NOT BUILT / UNRUN
- AX-S1S2-D pilot: UNRUN
- Phase 0: untouched / stale

No architecture redesign is requested.
