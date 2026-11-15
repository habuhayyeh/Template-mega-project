# ChatGPT review 101 — independent architecture simplification audit

## Scope and constraint

This audit was requested by the signer before any implementation or amendment of proposal 016.
It is independent of DeepSeek's simplification audit. No architecture, contract, schema, predicate,
fixture, scorer, or Gate-0 artifact is changed here.

Question: which current rules create more complexity/calibration burden than clinical or product value,
and could be replaced by a smaller generalized principle?

## Overall finding

The three-stage runtime architecture `INGEST -> STRUCTURE -> RENDER` remains sound. Most excess
complexity is inside STRUCTURE and in validation contracts that accumulated as responses to individual
failures. The strongest simplification strategy is to generalize around a few invariants:

1. **independent clinical identity vs contained information**;
2. **source-supported meaning vs note-use decision**;
3. **semantic content vs presentation realization**;
4. **one owner per decision, but not one bespoke field/predicate per failure mode**;
5. **account for clinically meaningful information, not every syntactic fragment**.

Below are candidate simplifications. They are not yet recommendations for implementation.

---

## Candidate 1 — Replace problem-specific retention exceptions with one problem-identity/containment rule

### Current burden
D-015, D-023 and D-030 form an exception/supersession chain:
- chronic block generally requires current management;
- major inactive neurologic diagnoses may still render;
- PRIMARY/BACKGROUND later becomes independent of retention;
- residual deficits and causal contribution are handled by additional special wording.

This is difficult to reason about because retention, encounter role, current adoption, and manifestation
identity are expressed through separate historical corrections.

### Generalized replacement
A/P blocks correspond to **clinically independent neurologic problem identities**.
For each independent problem:
- encounter role controls prominence/depth;
- source-supported descriptors/manifestations/consequences remain inside the problem unless they have
  independent problem identity;
- current management is one reason for prominence, not a prerequisite for existence;
- background problems may render compactly when clinically relevant to the neurologic note.

### What could disappear/merge
Much of the special-case logic in D-015/D-023/D-030 could collapse into:
- problem identity/containment;
- encounter role;
- rendering depth.

### Risk
Need a clear threshold for when a background diagnosis is relevant enough to render at all. Generalizing
too far could turn the A/P into a complete neurologic problem list.

### Classification
ARCHITECTURE/CONTRACT simplification.

---

## Candidate 2 — Collapse “adoption” into a broader source-supported assertion-state concept

### Current burden
The architecture separates:
- source temporality in I4;
- current adoption in S2;
- problem candidacy in S1;
- rendered use in S3.

That separation is conceptually defensible, but the word and machinery around `adoption` repeatedly
invite confusion with “current problem,” “problem block,” and “clinically important.”

It has required multiple corrective decisions and semantic packets.

### Generalized replacement
S2 should answer a simpler question:

> **What proposition/state does the current encounter endorse, reject, leave historical-only, or leave unresolved?**

This is proposition-level epistemic/current-encounter state, not block creation.

A minimal state model could potentially subsume today's `adoption` without changing S1/S3 ownership.

### What could disappear/merge
- special explanatory rules distinguishing “adopted residual deficit” from “background stroke”;
- some adoption-specific wording and tests;
- possibly the `adoption` term itself if a clearer state name is chosen.

### Risk
Do not collapse source temporality into encounter stance. “Documented historically” and “endorsed now”
remain distinct facts.

### Classification
CONTRACT simplification; likely no topology change.

---

## Candidate 3 — Replace special causal-subject rules with one source-fidelity relation rule

### Current burden
D-030/D-031 created detailed rules for:
- disease vs residual-deficit causal subject;
- relation noun;
- direction;
- strength;
- source support;
- positive calibration cases;
- special seeds for historical disease substitution and POSSIBLE->LIKELY.

The disease-vs-deficit rule is clinically useful but too specific as a governing principle.

### Generalized replacement
For every semantic relation:

> **Preserve the most specific relation and acting entity explicitly supported by the current source.
> Do not infer an unstated mediator, strengthen certainty, reverse direction, or replace a qualified
> formulation with a coarser one.**

This rule works for:
- stroke -> weakness -> falls;
- neuropathy -> sensory loss -> falls;
- medication -> parkinsonism;
- lesion -> seizure;
- disease -> downstream disorder.

### What could disappear/merge
The “residual deficit rather than historical disease” rule becomes an example, not a standalone
architectural law. Several causal calibration rules can be seen as instances of one relation-fidelity
predicate family.

### Risk
Some relations genuinely require normalization to a canonical subject for downstream logic. If so,
normalization must remain source-preserving and explicit.

### Classification
CONTRACT simplification.

---

## Candidate 4 — Reduce S2 “approved representation” + S3 “selection” ceremony

### Current burden
Current flow:
- S1 creates claim candidates;
- S2 may create zero or multiple approved representations;
- S3 selects exactly one representation;
- S4 receives only the selected representation;
- several predicates exist solely to police this handoff.

This protects ownership, but for many cases there is only one clinically defensible formulation, so the
architecture pays a substantial interface/calibration cost to preserve a choice that often does not exist.

### Generalized replacement
Distinguish two states:
1. **resolved formulation** — S2 emits the one defensible representation;
2. **genuinely choice-equivalent formulations** — only then expose a small approved set for S3 to choose
   by non-semantic criteria.

Default should be one resolved formulation, not a representation set.

### What could disappear/merge
Potentially:
- much of routine S3 representation-selection logic;
- some “approved set” machinery;
- some leakage predicates around S2-selection vs S3-selection.

S3 would still own **whether the problem/content renders**, while S2 owns **what it means**.

### Risk
Do not let S2 silently take over note-selection/product choices. Multiple equally valid phrasings may
still need a downstream selection surface.

### Classification
ARCHITECTURE/CONTRACT simplification candidate; requires experiments before change.

---

## Candidate 5 — Replace S1 `management_reference_spans[]` special salience field with generic source-grounded salience features

### Current burden
S1 currently carries a specifically named management-reference field to support later ordering/salience.
The schema and projection must preserve this exact field, even though management presence is only one
possible reason a problem is important.

This is a likely artifact of CASE-01 and ordering design history.

### Generalized replacement
S1 should expose only **source-grounded salience evidence**, with a small generic schema or computed
features sufficient for the eventual ordering contract.

Examples could include:
- current evaluation;
- current management;
- acuity/newness;
- reason-for-consult linkage.

The ordering contract, not S1, decides how these features weight order.

### What could disappear/merge
- bespoke `management_reference_spans[]` semantics;
- some projection-map specificity;
- some case-specific ordering scaffolding.

### Risk
A generic free-form salience blob would be worse. The replacement must remain small, typed, and
mechanically projectable.

### Classification
CONTRACT simplification.

---

## Candidate 6 — Relax the “renderer may add no lexical bridge token” rule; keep only “no new semantic relation”

### Current burden
R2 currently has an **empty bridge allowlist**: it may not add words such as “then,” “however,”
“because,” etc. This makes prose composition almost equivalent to concatenation and pushes ordinary
discourse structure upstream into S4/IR.

AX-R2 already anticipates the danger: signer-quality prose may require an upstream discourse graph more
complex than the content itself.

### Generalized replacement
R2 may perform **semantically neutral discourse realization** so long as it does not introduce a
relation not already encoded by unit order/content/section contract.

The invariant should be semantic:
> no new causal, temporal, contrastive, conditional, attribution, certainty, negation, or scope relation.

Not lexical:
> no new bridge words.

### What could disappear/merge
- empty bridge allowlist;
- some upstream micro-structure added only to permit natural prose;
- mechanical contiguous-span requirements that overconstrain legitimate realization.

### Risk
This is the highest-risk simplification because Doximity may hallucinate relations when given language
freedom. It should be experimentally tested, not assumed.

### Classification
ARCHITECTURE/RENDER contract simplification candidate.

---

## Candidate 7 — Replace “every source fragment must be dispositioned” with clinically meaningful coverage accounting

### Current burden
I1/I2 require every supplied fragment/span to be represented and dispositioned. This is maximally
auditable but can create huge bookkeeping volume for headers, duplicated boilerplate, irrelevant
administrative text, and low-value transcript fragments.

The architecture itself says the real invariant is that no clinically meaningful source content
silently disappears.

### Generalized replacement
Coverage should operate at the smallest **clinically meaningful source unit**:
- clinically meaningful span/proposition -> object(s) or explicit disposition;
- mechanically recognized nonclinical/administrative boilerplate may be covered by source-level
  exclusion categories rather than one record per fragment.

### What could disappear/merge
- some span-level dispositions;
- unnecessary coverage objects/records;
- calibration burden around purely syntactic completeness.

### Risk
If “clinically meaningful” is decided too early by the same model, important content can disappear.
Need a conservative rule or mechanical category for clearly nonclinical text.

### Classification
ARCHITECTURE/INGEST simplification candidate.

---

## Candidate 8 — Generalize object accounting and candidate accounting under one typed “decision closure” invariant

### Current burden
S3 separately requires:
- every S1 candidate gets exactly one outcome;
- every object is retained/used or dispositioned;
- rendered-set equality;
- reason registry;
- basis requirements;
- unknown-id checks.

These are valid checks, but the architecture has accumulated multiple specialized accounting
predicates and reason mechanics.

### Generalized replacement
Every decision-bearing entity entering a stage must leave with exactly one **typed terminal state**.

Examples:
- problem candidate -> rendered | not rendered(reason);
- clinical object -> used(problem/use) | dispositioned(reason);
- representation -> selected | unselected/not applicable.

Then generic closure/exclusivity mechanics can validate all entity classes, with semantic reason
correctness audited separately.

### What could disappear/merge
Potentially multiple bespoke coverage/exclusivity predicates and special reason checks could use one
generic closure engine/schema pattern.

### Risk
Do not collapse semantically different reasons into one generic “dropped” state. The generalization
should be mechanical infrastructure, not semantic flattening.

### Classification
CONTRACT/IMPLEMENTATION simplification.

---

## Candidate 9 — Reconsider the one-owner rule for shared actions as a special case of “one identity, multiple relations”

### Current burden
AX-SHARED spends an entire experiment on preserving:
- one action identity;
- one owning problem;
- secondary cross-problem relevance;
- possibly different rationales.

The difficult part may be the **one owner** requirement rather than the shared action itself.

### Generalized replacement
Separate:
- **identity cardinality**: one action object;
- **problem relationships**: zero, one, or multiple clinically meaningful links;
- **render placement**: one chosen home for presentation.

Then “owner” becomes presentation placement, not semantic ownership.

### What could disappear/merge
- some secondary-owner/reference schema experiments;
- the artificial need to encode one semantic owner plus secondary references.

### Risk
Without one presentation home, the note may duplicate the action or make plan ownership unclear.
Therefore semantic multi-linking and render-home selection must stay distinct.

### Classification
ARCHITECTURE candidate; should be tested before change.

---

## Candidate 10 — Reduce projection-map brittleness by projecting typed owner outputs, not every field path

### Current burden
S4_INPUT_VIEW currently freezes exact destination/source paths and per-field transforms. This gives
strong auditability but creates high maintenance cost: small schema wording/field changes alter hashes,
packets and projection rules even when semantic ownership is unchanged.

### Generalized replacement
Freeze **typed interface contracts** by owner:
- S1 problem/salience view;
- S2 selected semantic view;
- S3 render/use view;
- I3/I4 payload/provenance view.

Projection should remain mechanical and least-privilege, but field-level path pinning should be used
only where needed to prevent semantic invention, not as the default for every harmless representation
change.

### What could disappear/merge
- some exact-path projection rules;
- some hash churn;
- some projection-specific seeds that test packaging details rather than clinical architecture.

### Risk
Too loose a projection contract could reintroduce silent ownership drift. Need a typed schema boundary,
not an unstructured map.

### Classification
CONTRACT/IMPLEMENTATION simplification candidate.

---

## What I would preserve

I would **not** simplify away these core ideas:

1. `INGEST -> STRUCTURE -> RENDER` as the three logical runtime responsibilities.
2. Stable source-linked semantic objects.
3. One semantic decision has one owner.
4. S1 problem identity separate from S2 semantic meaning and S3 note-use.
5. Weak final rendering relative to upstream semantics.
6. Explicit separation of encounter role from causal certainty.
7. Mechanical vs semantic validation separation.
8. Synthetic/de-identified repository data only.

These are architectural load-bearing walls. The simplification target is the accumulated special-case
machinery around them.

## Priority order for comparison with DeepSeek

Most promising:
1. problem identity/containment replacing D-015/D-023/D-030 exceptions;
2. source-fidelity relation rule replacing causal-subject special cases;
3. resolved-formulation default reducing S2->S3 representation ceremony;
4. semantic rather than lexical R2 boundary;
5. generic decision-closure/accounting infrastructure.

Potentially useful but higher risk:
6. source coverage relaxation;
7. multi-link shared actions with separate render home;
8. projection-map relaxation.

## NEXT

Wait for DeepSeek's independently authored simplification audit. Then compare:
- overlaps (strong candidates);
- disagreements (valuable architecture questions);
- unique findings;
- simplifications that reduce schema/predicate/calibration surface without weakening source fidelity.

No implementation or contract amendment before the comparison.
