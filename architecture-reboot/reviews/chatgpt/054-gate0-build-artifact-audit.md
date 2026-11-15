# ChatGPT review 054 — Gate 0 build artifact audit

## Verdict

**REVISE THE GATE 0 BUILD BEFORE IMPLEMENTING OR RUNNING THE SCORER.**

The execution specification remains conditionally closed. The fifth-pass design corrections stand.

This review is of the newly built artifacts:
- CASE-01 clean parent;
- generated Gate 0 seeds;
- seed generator;
- generated manifest.

The major issue is no longer the experiment design. It is that the current "clean parent" is not yet demonstrably clean under the canonical S1→S4 interfaces, and the scorer input/oracle contract is not yet defined.

No Doximity run.
No Phase 0.

---

# 1. Parent→seed mutation audit

I independently diffed all 15 active generated seeds against `PARENT-CLEAN.json`.

Fourteen are clean single conceptual mutations:

- G0-S1-01 — add `adopted`
- G0-S1-02 — add `selected_claim`
- G0-S1-04 — remove the one anchor
- G0-S1-05 — append one candidate object
- G0-S1-06 — add `status_current`
- G0-S2-01 — clear `support_refs`
- G0-S2-03 — alter one temporal value
- G0-S3-01 — null approved representation
- G0-S3-02 — replace selected representation id
- G0-S3-04 — remove one retained object
- G0-S4-01 — remove one problem
- G0-S4-02 — add one problem
- G0-S4-04 — add one invalid member id
- G0-S4-06 — remove one plan-unit object from the units array

The apparent multiple JSON-path differences for clearing an array or removing an array element are consequences of one conceptual mutation.

## Exception — G0-S2-06

The generator changes two independent fields:

- `adoption: false -> true`
- `evidence: null -> [S02]`

That is not the one-field mutation described by the Gate 0 discipline.

This can be repaired either by:
1. using a clean CASE-02 S2 parent where adoption is true with evidence and mutating only `adoption -> false`; or
2. explicitly defining an **atomic adoption-decision mutation** as a coupled record change and changing the Gate 0 rule from "one field/change" to "one defect, with only required integrity-preserving companion fields."

The first option is cleaner.

---

# 2. The current clean parent is not yet clean under S1 source-grounding

Current S1 candidate claim:

> `gait instability, cause undetermined`

with support:
> `S02, S03`

But the frozen source says:
- S02: three falls since June; no new weakness or speech trouble;
- S03: check vitamin D and refer to PT for gait training.

The canonical S1 interface permits:

> candidate claim formulations **present in the source**

It does not authorize S1 to synthesize:
> "gait instability, cause undetermined"

as a new claim formulation.

## Required repair

For CASE-01 S1, use a source-faithful candidate formulation, for example:
- subject: recurrent falls;
- candidate claim: "three falls since June" anchored to S02;

or leave candidate claims empty if the subject is sufficient and no source claim formulation exists.

Do not let the clean parent already violate the S1 boundary that the experiment is meant to test.

---

# 3. S2 representation support in the clean parent is also questionable

R1 currently has:

- members: O03, O04
- support_refs: S02, S03

But S03 is the management sentence:
> check vitamin D / PT gait training.

It is not needed to support the falls representation carried by O03/O04.

A Gate 0 clean parent should contain no gratuitous support reference that a semantic scorer might reasonably call unsupported.

## Required repair

For the simple falls representation, prefer:
> `support_refs: [S02]`

unless the intended representation explicitly includes a management-linked semantic relation requiring S03.

---

# 4. S3 retained set and S4 blueprint are inconsistent

The clean parent marks **all seven objects** retained:

> O01–O07

but S4 contains only A/P units for:
- O03
- O04
- O05
- O06

There is:
- no body section;
- no unit for O01/O02;
- no unit for O07.

Canonical S3 defines retained content as content the note uses, and S4 must convert the retained problem-linked content into the complete executable blueprint.

Therefore the clean parent currently appears to retain content that the blueprint never renders.

This matters because Gate 0 requires the parent to produce **zero findings**.

## Preferred repair

For this A/P-only synthetic parent:

- retain only O03/O04/O05/O06;
- disposition O01/O02/O07 as `NOT_USED` or another allowed typed disposition;
- keep the infarct out of the A/P problem;
- keep aspirin from creating adoption.

That produces complete accounting and lets S4 fully cover the retained content.

If body rendering is intentionally part of the clean parent, then add the corresponding body section/units instead. Do not retain body/history content without a render path.

---

# 5. The scorer input/oracle contract is currently missing

The generated parent contains only:

> `substrate_objects: [O01 ... O07]`

It does not contain the source spans/text or a machine-readable case oracle.

Several active predicates cannot be scored correctly from the artifact alone:

### S1-CAND-01
Requires knowing whether a candidate subject has its own assessment question.

### S2-REP-01
Requires knowing whether the representation is source-grounded.

### S2-TEMP-01
Requires the frozen substrate temporal value.

### S2-ADOPT-01
Requires the frozen expected adoption decision.

### S4-COMP-01
Requires knowing which retained objects are PLAN items.

A scorer should not infer these from artifact output or scrape them ad hoc from prose markdown.

## Required build artifact

Add a frozen machine-readable scorer context/oracle for CASE-01, for example:

`fixtures/CASE-01/oracle.json`

containing only pre-adjudicated test facts such as:
- source span ids/text or normalized source payload;
- object id -> kind;
- object id -> frozen temporal value;
- expected independent S1 candidates / forbidden context-only candidate;
- expected adoption states relevant to the case;
- allowed support refs for the simple representation;
- retained PLAN object ids required by S4 completeness.

The scorer input bundle should then be explicitly:

> artifact under score + frozen case oracle + predicate registry/version

This is an experiment-local oracle, not production architecture.

---

# 6. G0-S1-05 currently leaks the answer into the artifact

The added candidate contains:

> `"has_assessment_question": false`

That field is not part of the experiment-local S1 schema.

More importantly, it tells the scorer the exact semantic verdict that `S1-CAND-01` is supposed to determine.

A scorer could simply read that boolean and "detect" the planted defect without understanding the candidacy rule.

## Required repair

Remove `has_assessment_question: false` from the seed artifact.

The scorer must determine that the old infarct lacks an independent current assessment question from the frozen case oracle/source context, not from an answer key embedded in the model artifact.

---

# 7. G0-S2-06 definition and generated artifact are still mismatched

`G0-SEEDS.md` still describes:

> adoption false where CASE-02 expects adopted

But the generator uses CASE-01 and mutates O01:

> false -> true

with evidence added.

DeepSeek already identified this mismatch in the handoff; it remains unresolved in the exact files.

## Required repair

Pick one canonical seed and make these agree:
- `G0-SEEDS.md`;
- `make_seeds.py`;
- generated artifact;
- generated manifest;
- scorer oracle.

Do not leave the textual definition and executable seed testing opposite directions.

---

# 8. The generator should not be the sole authority on seed meaning

The code says:

> "The generator is the authority on what changed"

That is unsafe as a control-plane principle.

If the generator itself is wrong, regenerating byte-identical wrong artifacts does not establish conformance.

## Better authority hierarchy

1. frozen seed specification / predicate registry;
2. clean parent + oracle;
3. generator implementation;
4. generated seed artifact;
5. independent diff validation.

The generator should **implement** the seed specification, not define it.

## Required addition

For each active seed, the generated manifest should record:
- parent id/hash;
- seed artifact hash;
- expected predicate;
- expected mutation path(s);
- expected before/after value or mutation description;
- full-silence rule reference;
- predicate-set version.

Then an independent validator can confirm:
> generated artifact = parent + exactly the declared mutation.

---

# 9. Gate 0 manifest mode labels are now stale

`00-GATE0-MANIFEST.md` still classifies broad families as:
- S1 authority = semantic;
- S2 representation = semantic;
- S3 selection = semantic;
- etc.

But the actual active predicates mix:
- MECHANICAL;
- SEMANTIC.

The fifth-pass predicate registry correctly moved scoring mode to the predicate level.

## Required repair

Make Gate 0 calibration counts derive from the **predicate mode**, not the broad family label.

A family can remain an organizational grouping, but it should not determine repetition count when its predicates have mixed modes.

---

# 10. S1 forbidden-field map has one remaining stale partial copy

`schema.md` correctly points the forbidden-field authority to `predicates.md`.

But its field→predicate table still describes `S1-AUTH-01` as checking only:

> adopted / adoption / selected_claim

while the closed versioned set is:

> adopted, adoption, adoption_verdict, selected_claim, resolved, status_current

## Required repair

The map row should say:

> absence of the versioned forbidden-field set defined by `S1-AUTH-01`

rather than restating a partial copy.

---

# 11. Corpus F-1 still contains one premature completeness claim

The file now correctly says omission vs marker is a pending product decision.

But it still says:

> a run that omits the slot entirely fails completeness.

That contradicts the pending product decision.

## Required repair

Until product behavior is frozen:

- unsupported invention = fidelity failure;
- omission vs explicit marker = **not yet scoreable**.

Remove the completeness-failure statement.

---

# 12. Corpus next-action wording is also too early

It says:

> No schema proposal until a run shows the current architecture failing at it.

The correct sequence is:

1. product behavior is decided;
2. the required behavior is tested;
3. schema is proposed only if the current representation cannot satisfy that requirement.

A run cannot "fail" an undecided product requirement.

---

# 13. Current state

## Architecture
CLOSED / CONVERGED.

## Experiment design
CLOSED / CONVERGED.

## AX-S1S2-D execution specification
CONDITIONALLY CLOSED.

## Gate 0 build
**IN PROGRESS / REVISE BEFORE SCORER IMPLEMENTATION**

Built:
- one CASE-01 parent;
- 15 generated active seeds;
- seed generator;
- generated manifest.

Still required before scorer implementation:
1. repair clean parent semantics/accounting;
2. add machine-readable case oracle/scorer input contract;
3. remove S1 candidacy answer leakage;
4. resolve G0-S2-06 direction + atomicity;
5. enrich generated manifest / independent diff validation;
6. clean stale mode/schema/corpus text.

## Scorer
NOT BUILT.

## Gate 0
UNRUN.

## Doximity pilot
DO NOT RUN.

## Phase 0
Do not touch.
