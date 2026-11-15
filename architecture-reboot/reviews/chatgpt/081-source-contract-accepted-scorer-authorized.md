# ChatGPT review 081 — source contract accepted for scorer construction

## Verdict

> **ACCEPT — execution source contract is sufficient to authorize scorer construction. Gate 0 remains UNRUN and has one separate operational prerequisite: the three-independent-human-review requirement must be practically satisfied before semantic Gate 0 execution.**

DeepSeek commit `1a0b5f7` resolves the three remaining review-080 source-contract blockers without reopening the frozen architecture.

The source-contract review cycle is therefore closed.

This does **not** mean Gate 0 passes. It means the scorer may now be implemented against the accepted contract.

---

# 1. PASS — PROJECTION_MAP and executable projection semantics are now bound

Review 080's concern was duplicate authority:

- schema map said one thing;
- hard-coded `OPS` could silently do another.

The new `OP_CONTRACTS` table closes that gap for this Gate 0 implementation.

For every projection op, the build now requires exact agreement on:

- destination;
- owner;
- source;
- source path;
- condition;
- requirement;
- transform;
- expansion map where applicable.

The build also requires:

- `OPS` and `OP_CONTRACTS` to cover exactly the same op set;
- the projection map's op set to equal the implemented op set.

Therefore changing the written map metadata without changing its executable contract fails the build.

This is sufficient for the experiment-local source contract.

PASS.

---

# 2. PASS — HUMAN_REVIEW policy is now internally coherent

The prior invalid equivalence:

> three independent judges **or** one judge + mechanical pre-filter

is gone.

The frozen semantic calibration rule is now:

- three independent blinded human judgments;
- each judge sees artifact + oracle + predicate rule only;
- all three must detect the defect;
- all three must satisfy FULL_SILENCE-WITHIN-LAYER;
- 2/3 fails;
- one judge × three repeats is not independent evidence;
- mechanical preprocessing cannot substitute for semantic judgment.

The Gate 0 manifest and predicate registry now agree.

PASS as a contract.

---

# 3. PASS — S2-REP-01 now has a genuinely semantic calibration branch

The predicate claims more than reference existence:

> approved representations must be semantically supported by source objects/relations.

The new `G0-S2-02` preserves structural validity:

- representation id remains valid;
- problem id remains valid;
- support ref remains `S02`;
- all member object ids exist.

The sole mutation adds:

`O07 = aspirin 81 daily, unchanged`

to the falls representation.

That object is real but does not semantically support the falls problem/claim represented by R1.

Therefore the branch distinguishes:

> **real ids / real refs**

from:

> **semantically supported representation membership**.

This is exactly the distinction review 080 required.

The existing `G0-S2-01` remains useful as the structural support-ref branch.

PASS.

---

# 4. PASS — S4-PROJ branch descriptions now match the corpus

The human summary now correctly distinguishes:

- `G0-S4-09` = true wrong-owner-group violation;
- `G0-S4-11` = valid-field fabricated duplicate-group value.

PASS.

---

# 5. PASS — generator integrity remains intact

The accepted package retains the review-079 protections:

- mutation executed for every seed;
- no-op seeds fail;
- multi-diff seeds fail;
- checked parent→seed diff becomes manifest mutation record;
- non-noop seed hash differs from parent;
- second-run zero diff required.

Current claimed campaign count:

- 5 clean parents;
- 4 parent types;
- 28 seeds;
- 16 active predicates.

No source-contract reason remains to block scorer implementation.

---

# 6. Source-contract acceptance boundary

This acceptance means DeepSeek may now build the scorer/harness against:

- `GATE0-C1`;
- `PILOT-2`;
- `ACTIVE-PILOT-2`;
- `SCHEMA-2`;
- `ORACLE-2.0`;
- `REASON-1`;
- `PILOT-OPERATORS-1`;
- current five clean-parent identities;
- current 28-seed manifest;
- FULL_SILENCE-WITHIN-LAYER.

The scorer must not redefine any of those.

If implementation exposes an actual contradiction in the accepted source contract, stop and reopen that specific contract item. Do not silently compensate in scorer code.

---

# 7. Separate operational prerequisite — three human judges

This is **not a source-contract rejection**.

The accepted Gate 0 semantic policy requires three independent human judgments.

Our ordinary project workflow has:

- signer;
- ChatGPT;
- DeepSeek.

ChatGPT and DeepSeek are not human judges.

Therefore before semantic Gate 0 is actually executed, the operator must have a practical way to obtain three independent human reviews, or the signer must deliberately authorize a different reviewer model/policy through the appropriate governed change.

Do not quietly count ChatGPT/DeepSeek as humans.

Do not weaken the rule inside the scorer implementation.

This operational dependency does **not** block scorer construction; it blocks semantic Gate 0 completion.

---

# 8. Scorer-construction constraints

DeepSeek is now authorized to implement the scorer, with these constraints:

1. **scorer blindness**
   - scorer receives artifact + oracle + predicate registry/rules;
   - no seed id;
   - no expected predicate;
   - no mutation metadata;
   - no answer key.

2. **mechanical predicates**
   - deterministic implementation;
   - no semantic fallback;
   - one run.

3. **HUMAN_REVIEW predicates**
   - scorer/harness prepares the blinded review packet;
   - records judge identity and judgment;
   - does not auto-convert a mechanical heuristic into the semantic verdict;
   - Gate 0 aggregation requires three independent accepted judgments.

4. **specificity**
   - expected predicate must fire;
   - every other ACTIVE predicate in that parent_type must remain silent.

5. **clean controls**
   - every clean parent must produce zero findings.

6. **UNDECIDABLE**
   - must remain explicit;
   - cannot be silently converted to PASS.

7. **evidence**
   - immutable per-run scorer outputs;
   - scorer version/hash;
   - governing campaign identities/hashes;
   - exact artifact hash;
   - judgment records for human predicates.

8. **no Doximity yet**
   - scorer must pass Gate 0 before architecture experiment outputs can become acceptance evidence.

---

# 9. Next review target

The next artifact for ChatGPT review should be:

> **the scorer implementation + Gate 0 harness, before Gate 0 is run.**

Review focus will be:

- predicate implementation fidelity;
- scorer blindness;
- answer-key separation;
- exact specificity computation;
- clean-parent handling;
- semantic-review packet generation;
- human-judgment recording;
- aggregation logic;
- UNDECIDABLE handling;
- immutable evidence output;
- version/hash capture;
- negative tests proving the scorer cannot see the answer key.

Do not combine scorer construction and Gate 0 execution in one unreviewed step.

---

# 10. Current canonical state

- Architecture: **CLOSED / VERIFIED**
- DC-002: **APPLIED / VERIFIED**
- Experiment program: **FROZEN / UNRUN**
- Build/generator: **PASS**
- Execution source contract: **ACCEPTED**
- Scorer construction: **AUTHORIZED**
- Scorer: **NOT YET BUILT / NOT YET REVIEWED**
- Gate 0 mechanical execution: **NOT RUN**
- Gate 0 semantic execution: **NOT RUN; operational three-human-review prerequisite outstanding**
- Doximity architecture experiments: **UNRUN**
- Phase 0: **UNTOUCHED**

The next task is scorer/harness construction, not another source-contract rewrite.
