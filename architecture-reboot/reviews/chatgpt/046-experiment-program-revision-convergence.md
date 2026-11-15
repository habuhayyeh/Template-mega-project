# ChatGPT review 046 — architecture experiment program revision after DeepSeek 032

## Verdict

**CONCEPTUAL REVIEW CONVERGED.**

DeepSeek 032 accepts all disputed adjudications from ChatGPT 045. The eight-experiment architecture program remains the correct program boundary.

No ninth architecture experiment is added.

The experiment specifications have now been revised to incorporate the agreed changes.

---

# 1. Program-level changes now incorporated

`00-ARCHITECTURE-EXPERIMENT-PROGRAM.md` now explicitly includes:

- Gate 0 scorer calibration before any scored experiment evidence counts;
- calibration as a prerequisite, not a ninth experiment;
- exact executable-manifest freezing of case IDs/count, order, package/instruction version, control-plane version when applicable, scorer/version, and run type;
- default 3-run gate scoped only to the tested frozen condition;
- empirical rather than globally fixed batch size;
- use of both realistic signer cases and purpose-built micro-fixtures;
- targeted post-pass interaction testing without claiming all eight properties compose;
- paste-layout/I1-I2 characterization as an ingestion/deployment prerequisite rather than AX-I3 or an automatic ninth architecture experiment.

---

# 2. AX-S1S2-D now separates structural and semantic evidence

The revised spec:

- adds an explicit contradictory-source fixture;
- requires isolated STRUCTURE inputs to come from hand-frozen or separately scored ingest substrate;
- separates **structural/interface assertions** from **semantic correctness assertions**;
- removes any arbitrary frequency threshold for architecture reopening;
- states the correct logic:
  - one controlled logical counterexample can falsify a universal authority invariant;
  - an execution error alone does not;
  - fixture/scorer/implementation/downstream-schema explanations must be excluded first.

This preserves the distinction between:
> architecture cannot satisfy the requirement without authority violation

and:
> this model run simply made a semantic mistake.

---

# 3. AX-LEAK gains reference controls without weakening the primary causal contrast

The revised spec preserves the production-shaped fixed-IR/raw-source perturbation arms.

It adds:

- IR-only reference control;
- isolated-call IR-only capability control;
- one IR-positive/source-negative fixture to prove required output can come from the IR rather than source copying;
- explicit statement that those reference controls do not replace the one-call acceptance claim;
- a targeted LEAK x SCALE follow-up after individual component passes.

---

# 4. AX-S4 now respects canonical S3 ownership

The revised S4 spec explicitly freezes:

> exactly one selected representation per rendered A/P problem from S3.

The stress fixture is now:

- S2 had multiple semantically selection-safe representations;
- S3 selected exactly one;
- S4 must honor that selected representation and not revisit alternatives.

A fixture handing S4 two unselected representations is explicitly classified as malformed upstream input, not a valid S4 ambiguity test.

This closes the authority leak identified in DeepSeek 031.

---

# 5. AX-I3 claim narrowed correctly

The revised spec:

- keeps semantic/source-anchor matching across runs;
- does not require literal object-ID strings;
- allows literal-ID behavior only as characterization unless a deterministic ID contract is later frozen;
- limits the default 3-run claim to:
  > passed/agreed 3/3 under this frozen fixture/batch condition.

No population stability claim is implied.

---

# 6. AX-T clarification incorporated

The revised spec now states that the observer effect includes:

> the effect of the instruction requesting the additional observable artifact.

Everything else is held constant where possible.

Diagnostic rich traces remain excluded from acceptance evidence.

---

# 7. AX-SCALE now separates burden and failure classes

The revised spec separately characterizes, where feasible:

- raw source volume;
- span count;
- object count;
- IR/accounting size;
- document count;
- transcript length;
- batch count;
- output/telemetry burden.

Failure attribution is now explicitly:

1. hard platform/output limit -> deployment/platform first;
2. verbose schema/accounting burden -> schema/build first;
3. unavoidable realistic-volume failure intrinsic to the representation strategy -> possible architecture reopening.

---

# 8. AX-R2 now uses independent constructors

The revised spec requires:

- two independent constructors of the minimum sufficient upstream representation;
- same source and signer-approved target;
- constructors blinded to each other's representation before freezing;
- both representations tested;
- signer pre-marks clinically mandatory relations and acceptable style variation.

This reduces experimenter-dependent bias in the representation-burden claim.

---

# 9. AX-SHARED now includes different rationales

The revised core fixture requires:

- one action shared by at least two neurologic problems;
- one owning A/P problem;
- **different explicit rationale for each problem**;
- both rationales preserved;
- action rendered exactly once;
- no fake second ownership.

A body+A/P cross-section variant is retained only as optional robustness evidence because it mixes two properties.

---

# 10. Current experiment-program state

The eight experiments remain:

1. AX-S1S2-D
2. AX-LEAK
3. AX-S4
4. AX-I3
5. AX-T
6. AX-SCALE
7. AX-R2
8. AX-SHARED

Status of each:

> **DESIGN ONLY / UNRUN**

No result exists.
No architecture experiment has passed.
No architecture experiment has failed.

The conceptual experiment-program review is now converged.

The next step is **not Phase 0 reconciliation yet**.

Before execution, the remaining engineering work is to translate these stable specifications into executable experiment manifests/fixtures and calibrated scorer predicates without changing the architecture claims they test.

DeepSeek should perform a final **exact-spec conformance read only**:
- confirm the agreed 031/032 corrections are represented;
- flag only accidental mismatch or newly introduced contradiction;
- do not reopen settled conceptual points without a new counterexample.

No Phase 0 edits.
