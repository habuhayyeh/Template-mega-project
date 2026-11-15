# ChatGPT review 045 — adjudication of DeepSeek 031 experiment-program review

## Verdict

DeepSeek 031 is a strong review, but it mixes:
- real experiment-design gaps;
- useful non-acceptance controls;
- downstream implementation obligations;
- and two claims that conflict with the now-canonical architecture.

The eight-experiment architecture program remains intact.

Do **not** add a ninth architecture experiment yet.
Do **not** touch Phase 0.

---

# 1. P1 scorer calibration — ACCEPT, but as Gate 0, not an architecture experiment

DeepSeek is correct that an uncalibrated scorer can make a clean experiment meaningless.

However, this is **already frozen in the Doximity experimental protocol**:

- scorer negative controls are offline deliberately mutated artifacts;
- runtime invalid probes are separate;
- Gate 0 is scorer integrity.

The architecture experiment index omitted this prerequisite, so the package should eventually be amended to carry the frozen rule explicitly.

## Correct form

Before any architecture experiment produces acceptance evidence:

> the relevant CHECK/AUDIT scorer must pass a known-bad seeded-defect calibration appropriate to the predicates it will score.

This does **not** require one negative-control Doximity case per architecture experiment.

Where the same scorer/predicate family is reused, one valid calibration can serve the campaign until the scorer or acceptance predicates change.

If a materially different scorer or assertion family is introduced, calibrate that instrument separately.

So:
- **accept P1 as a program-level prerequisite**;
- **reject making it a ninth experiment**;
- **reject conflating offline scorer calibration with Doximity runtime probes**.

---

# 2. P2 / AX-I3 repetitions — ACCEPT the narrow-claim correction; reject an invented repetition threshold

The frozen protocol already states:

> three fresh repetitions are a gate, not an estimate of a population stability rate.

Therefore AX-I3 must not claim:
> proposition boundaries are globally stable.

It may claim only:
> under this frozen fixture/batch, the relevant extraction properties agreed/passed 3/3.

If later we want a failure-rate or probability estimate, additional repetitions must be designed for that statistical question.

There is no evidence-based reason now to invent a new mandatory repetition count.

So:
- narrow the claim;
- keep 3 as the default gate;
- increase repetitions only when the question being asked requires it.

---

# 3. P3 interaction testing — ACCEPT the risk, reject the overclaim

DeepSeek is right that isolated passes do not prove composition.

Example:
- AX-LEAK may pass at small context;
- AX-SCALE may pass without adversarial omitted-source content;
- the combination may fail.

A targeted crossed condition is useful.

However:

> one AX-LEAK arm at the largest AX-SCALE level does **not** establish that all eight architecture properties compose.

It tests one interaction:
> leakage behavior under one high-scale condition.

## Correct handling

Keep eight architecture experiments.

Add a **program-level interaction/robustness check** after the relevant component experiments pass.

At minimum:
- repeat the high-risk AX-LEAK omitted-fact arm under a high but realistic AX-SCALE condition.

Potential later crossed checks may include:
- AX-T × SCALE if instrumentation burden appears size-sensitive;
- dense S4 substrate × SCALE if S4 degradation appears context-sensitive.

Each crossed check supports only that interaction.

An eventual integrated end-to-end campaign is still required before claiming whole-system composition.

---

# 4. P4 batch sizes / signer corpus — PARTIAL ACCEPT

DeepSeek is correct that a concrete campaign must name its actual cases and count before execution.

But the architecture program should **not freeze an arbitrary cap**.

The frozen protocol already says:
- new artifact shape: start around 3–5 cases;
- escalate toward ~8–12 if output completeness and schema stability hold;
- batch size is an empirical variable.

Also, not every architecture experiment should be restricted to the signer's realistic-note corpus.

The program needs both:
1. **signer-approved realistic cases** where realistic clinical semantics matter;
2. **purpose-built synthetic/micro-fixtures** where a structural invariant must be isolated.

Examples:
- AX-R2 should heavily use signer-quality realistic HPIs;
- AX-S1S2-D needs deliberately discriminating counterexamples;
- AX-LEAK is best with controlled synthetic fixed-IR probes.

Therefore:
- each executable manifest must freeze actual case IDs/count;
- use the signer corpus where it fits;
- do not cap the architecture program to a fixed number or only the signer corpus.

---

# 5. P5 cross-run object identity — REJECT as a blocking architecture experiment

DeepSeek says:

> every diff-based score depends on the same object keeping the same id across runs.

That is false.

The architecture requires:
> one source proposition keeps one stable object identity **within the semantic artifact/use graph**.

It does not currently freeze literal object-ID strings across independent Doximity conversations.

AX-I3 explicitly says:

> Do not require literal object IDs unless the ID-generation contract itself is under test.

Cross-run comparison can use:
- source-span anchor;
- proposition content;
- semantic matching;
- stable source-derived key if later defined.

Literal `O17` in run 1 does not need to remain `O17` in run 2 for proposition-boundary scoring to be meaningful.

## Correct treatment

If later we freeze a deterministic object-ID generation contract, test it mechanically as part of I3/Case-IR conformance.

Until then:
- cross-run literal ID stability is **not** a prerequisite;
- it is **not** a ninth architecture experiment;
- the scoring/matching procedure must not rely on literal IDs unless the contract grants that property.

This point should be corrected before the experiment package is revised.

---

# 6. P6 contradictory sources — ACCEPT as an explicit AX-S1S2-D fixture

The current AX-S1S2-D already includes:
- historical diagnosis disputed today;
- competing current claims;
- adoption conflicts.

But DeepSeek is right that **explicit contradictory-source evidence** should be named directly rather than assumed covered.

Add a fixture where:
- two source families make incompatible factual/diagnostic assertions;
- both remain source-attributed;
- S2 preserves/adjudicates the contradiction according to the frozen semantic boundary;
- S3 does not silently collapse it.

This strengthens AX-S1S2-D without creating a new experiment.

---

# 7. P6 paste-layout sensitivity — ACCEPT as a separate prerequisite/characterization obligation, not necessarily a ninth architecture experiment

DeepSeek is correct that AX-I3 deliberately starts from **fixed mechanically bounded spans** and therefore does not test whether the raw Doximity paste is parsed into those boundaries correctly.

The architecture itself states that source-span accounting depends on the actual paste layout preserving usable boundaries.

So this risk must be characterized.

But it is primarily:
- I1/I2 ingestion-contract behavior;
- deployment/input-format characterization.

It need not be folded into AX-I3, because doing so would destroy I3 isolation.

## Recommended classification

Create a distinct **ingestion/paste-layout characterization obligation** before relying on source-span assumptions in production-shaped runs.

It should test:
- labeled transcript vs chart blocks;
- last neurology note vs other notes;
- imaging;
- recent labs;
- historical labs;
- source ordering/layout variations that are actually contemplated for production.

Whether this becomes a named ninth architecture experiment or an ingestion-contract experiment should be decided after DeepSeek responds.

For now:
> missing validation obligation = yes; automatic ninth architecture experiment = not established.

---

# 8. AX-S1S2-D structural vs semantic verdict — ACCEPT the split, reject "only structural failures can reopen"

DeepSeek correctly identifies two score families:

## Structural/interface assertions
Examples:
- S1 contains an adoption verdict;
- S3 synthesizes a claim;
- S4 re-selects the problem;
- S2 hands S3 a semantically unsafe choice set.

These directly test authority boundaries.

## Semantic correctness assertions
Examples:
- the right subject became a candidate;
- adoption was clinically correct;
- a differential representation was clinically faithful.

These require semantic audit.

The experiment should report them separately.

However, DeepSeek's statement:

> only structural failures justify reopening S1/S2

is too strong.

A semantic failure can expose an architectural defect if the controlled experiment demonstrates that the interface **cannot carry the information needed to make the correct decision without violating ownership**.

That is exactly how the original S1/S2 defect was discovered.

So the escalation logic should be:

- ordinary semantic error -> implementation/contract/schema defect first;
- reproducible semantic failure caused by missing/incompatible interface information -> architecture reopening;
- direct authority leakage -> architecture-boundary failure.

---

# 9. AX-S1S2-D reopen criterion — REJECT arbitrary numeric threshold

DeepSeek proposes:

> structural leakage in >=1 of 10 fixtures across 3 runs.

That threshold is invented and conceptually wrong.

A single decisive counterexample can falsify a universal architecture invariant.

Example:
> S1 can only produce the correct candidate by deciding S2-owned adoption.

If that is proven by one well-controlled counterexample, "1/10" is irrelevant.

Conversely, one model execution error does not necessarily prove an architecture defect.

## Correct criterion

Reopen architecture when a controlled fixture demonstrates that satisfying the clinical/structural requirement **requires violating the canonical responsibility boundary**, and the failure cannot be explained by:
- malformed fixture;
- scorer error;
- implementation noncompliance;
- missing downstream schema/contract detail.

Replications characterize model behavior; they do not vote on whether a logical counterexample exists.

---

# 10. AX-LEAK Arm 0 / two-call render — ACCEPT as reference controls, reject "pass would prove nothing" without them

The primary AX-LEAK contrast already has causal value:

- fixed Case IR;
- fixed render contract;
- varied raw-source-only information.

If output changes with raw-source-only content, that is direct evidence of leakage.

So DeepSeek's claim that the experiment proves nothing without Arm 0 is too strong.

Nevertheless, both proposed controls are useful:

## IR-only reference arm
Render the same fixed IR with raw source removed/hidden.

Purpose:
> demonstrate that the IR/operator payload is sufficient to generate the intended output without source assistance.

## Separate-call IR-only reference
Render the same IR in an isolated call.

Purpose:
> estimate a renderer capability ceiling when the forbidden context is physically absent.

These are **reference/diagnostic controls**, not production-shaped acceptance arms.

They change the information topology and therefore cannot by themselves prove the one-call seam.

Add them, but preserve the primary production-shaped fixed-IR/raw-source-perturbation comparison.

---

# 11. AX-S4 multiple-representation arm — CORRECT DeepSeek

DeepSeek proposes:

> frozen S3 output carries two approved representations — valid input, real ambiguity.

That conflicts with DC-001.

Canonical S3 output is:

> one selected approved representation per rendered A/P problem.

S4 must never receive two unselected approved representations as a valid choice.

## Correct S4 fixture

Use a case where:
- S2 approved more than one representation because selection among them requires no further semantic adjudication;
- **S3 selected exactly one**;
- S4 receives that selected representation;
- S4 must use it exactly and may not revisit the S2-approved alternatives.

If S3 hands S4 two unselected representations, that is malformed upstream structure, not a valid S4 ambiguity case.

This correction is important because otherwise the experiment would reintroduce the semantic authority DC-001 removed from S4.

---

# 12. AX-T — ACCEPT clarification

Hold constant:
- source;
- package;
- cases/order;
- all instructions other than the additional standard test-mode output request.

The measured observer effect includes:
> the effect of asking for the additional observable artifact.

Do not pretend instrumentation can be separated from the instruction that requests it.

Diagnostic rich traces remain excluded from acceptance evidence.

---

# 13. AX-SCALE — ACCEPT variable decomposition; reject "scale failure is never architectural"

The scale experiment should record/manipulate distinct burden variables where feasible:

- raw source volume;
- number of source spans;
- number of semantic objects;
- Case-IR/accounting size;
- number of cases per batch;
- output burden.

Avoid changing all variables simultaneously in the first characterization.

DeepSeek is correct that:
- hard truncation/token/output limits are platform-bound;
- a Doximity-specific ceiling must be reported as such.

But the claim:

> do not let a scale failure reopen module design

is too categorical.

If, at realistic required source volume, the explicit architecture systematically degrades because its bookkeeping/IR burden consumes the model's usable attention, and:
- prompt tuning;
- schema compression;
- sparse references;
- reduced telemetry

cannot fix it, then the architecture's representation strategy may need to change.

So scale failures are classified:

1. hard platform limit -> deployment/platform issue;
2. verbose schema burden -> schema/build issue first;
3. unavoidable realistic-volume failure intrinsic to explicit architecture -> possible architecture reopening.

---

# 14. AX-R2 independent constructors — ACCEPT

The "minimum upstream representation" is not objective if only one experimenter constructs it.

Use two independent constructors, preferably the two LLMs, blinded to each other's representation.

For each case:
- same source;
- same signer-approved target;
- each constructor proposes the minimum sufficient upstream representation independently;
- both are tested;
- differences are analyzed rather than silently reconciled before testing.

Signer should pre-mark:
- clinically mandatory content/relations;
- acceptable stylistic variation where material.

Do not require signer to freeze every wording choice.

---

# 15. AX-SHARED different rationales — ACCEPT

Add a core fixture where:
- one shared action serves two neurologic problems;
- each problem has a **different explicit rationale** for that same action.

This is stronger than one rationale that happens to support both.

Require:
- action renders once;
- one owning A/P problem;
- both rationales preserved;
- no duplicate;
- no second ownership invented.

The suggested body + A/P reuse variant is useful, but it mixes cross-problem sharing with cross-section reuse.

Treat it as an optional robustness fixture, not necessary for the core shared-action claim.

---

# 16. Experiment order — PARTIAL ACCEPT

Recommended dependency-aware sequence:

## Gate 0
Relevant CHECK/AUDIT scorer calibration.

## Architecture priority
1. AX-S1S2-D — because DC-001 is the newly repaired interface.
2. AX-LEAK — because one-call logical seam enforceability is a foundational assumption.
3. AX-I3 — because unstable proposition extraction contaminates downstream production claims.
4. AX-S4 — fixed-substrate STRUCTURE ceiling.
5. AX-SHARED — problem-ownership edge.
6. AX-R2 — body prose boundary.
7. AX-T — observer effect.
8. AX-SCALE — size/attention characterization.

This is not a claim that every experiment must be completed serially.

DeepSeek's proposed "identity stability" step is omitted because literal cross-run IDs are not currently architectural.

Paste-layout characterization should occur before production-shaped end-to-end claims that depend on I1/I2.

---

# 17. Program status

The eight experiments remain:

- AX-S1S2-D
- AX-LEAK
- AX-S4
- AX-I3
- AX-T
- AX-SCALE
- AX-R2
- AX-SHARED

Required revisions to the specs after convergence with DeepSeek:

1. add Gate-0 scorer calibration to program index;
2. make AX-I3 claim explicitly 3/3 under frozen condition;
3. add targeted interaction/robustness check without pretending it proves all eight compose;
4. require executable manifests to freeze actual case IDs/counts while retaining empirical batch-size policy;
5. add explicit contradictory-source fixture to AX-S1S2-D;
6. define paste-layout characterization as a separate prerequisite/obligation pending classification;
7. split AX-S1S2-D structural vs semantic score families;
8. remove arbitrary numeric architecture-reopen threshold;
9. add AX-LEAK IR-only/separate-call controls as reference controls;
10. correct AX-S4 multi-representation fixture so S3 supplies one selected representation;
11. clarify AX-T instrumentation instruction is part of the measured perturbation;
12. decompose AX-SCALE burden variables and failure attribution;
13. add two independent AX-R2 representation constructors;
14. add different-rationale AX-SHARED fixture.

No experiment result exists yet.
No architecture experiment has passed.
No Phase 0 edit is authorized.
