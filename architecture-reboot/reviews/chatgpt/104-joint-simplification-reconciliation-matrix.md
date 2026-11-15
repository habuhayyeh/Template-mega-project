# ChatGPT review 104 — joint simplification reconciliation matrix

## Scope

This reconciles:
- DeepSeek 017 independent rule-complexity audit;
- ChatGPT 101 independent architecture simplification audit;
- ChatGPT 102 cross-review of DeepSeek 017;
- DeepSeek 018 review of ChatGPT 101;
- DeepSeek 019 response to ChatGPT 102;
- ChatGPT 103 review of DeepSeek 018/019;
- DeepSeek proposal 020 as revised after review 103.

No contract, schema, predicate, seed, scorer, packet, decision, or runtime implementation is changed here.

## High-level conclusion

The three-stage runtime architecture remains sound:

```
INGEST -> STRUCTURE -> RENDER
```

The simplification target is not another topology rewrite. The excess is in two layers:

- **Layer A — semantic architecture:** accumulated clinical exceptions and overlapping concepts;
- **Layer B — specification/calibration:** too many predicates, seeds, packets, identities, fixture hacks and duplicated normative text.

The two agents now agree that Layer A should be simplified conceptually first, while semantics-agnostic
Layer-B redesign may be specified in parallel but not implemented until the semantic target is frozen.

---

# A. Load-bearing invariants to preserve

| invariant | status | rationale |
|---|---|---|
| INGEST -> STRUCTURE -> RENDER | KEEP | No evidence justifies a topology rewrite. |
| Stable source-linked objects with provenance/temporality | KEEP | Core source-fidelity substrate. |
| One semantic decision has one owner | KEEP | Prevents duplicated authority and downstream reinterpretation. |
| S1 problem identity distinct from S2 meaning and S3 note-use | KEEP | Separation remains useful even if interfaces simplify. |
| S4 compiles render-affecting decisions before RENDER | KEEP | Supported by Doximity operator evidence. |
| Weak final renderer relative to upstream semantics | KEEP | Prevents prose stage from silently changing clinical meaning. |
| Encounter role independent from causal certainty | KEEP | Clinically correct and already signer-supported. |
| Mechanical validation distinct from semantic judgment | KEEP, simplify implementation | The distinction is sound; current predicate implementation is overbuilt. |
| Option F signer + 2 blinded evaluators | KEEP | Calibration governance remains accepted. |
| Synthetic/de-identified repository data only | KEEP | Governance/safety requirement. |

---

# B. Layer-A semantic reconciliation

## B1. Problem identity / containment / relevance / role

| field | reconciliation |
|---|---|
| Current rules causing burden | D-015 chronic-management block rule; D-023 inactive-major-problem exception; D-030 PRIMARY/BACKGROUND correction and residual-deficit wording; S1 candidacy wording |
| Root problem | Retention, problem identity, encounter role and manifestation containment became an exception chain. |
| General principle | **Independent clinical identity** determines whether an entity can be a problem. A finding/manifestation fully explained by a parent remains contained unless it has independent disorder/syndrome identity. **Encounter relevance** determines whether the independent problem is represented in this note. **Encounter role** then determines PRIMARY vs BACKGROUND and therefore prominence/depth. |
| Consensus | **YES — first-wave semantic generalization.** |
| Current rules potentially retired/merged | D-015 and D-023 special-case wording; the containment-specific portion of D-030; S1 examples that encode individual disease exceptions |
| Still unresolved | Define the threshold for when an independent BACKGROUND problem is relevant enough to render. Current management must not be the sole gate. |
| Action | **CHANGE after signer ratification of the generalized rule.** |

### Proposed semantic questions

1. Does the entity have independent neurologic problem identity?
2. If yes, is it relevant enough to this neurologic encounter/note to represent?
3. If represented, is its encounter role PRIMARY or BACKGROUND?

These questions are distinct from whether contained manifestations are currently true or causally relevant.

---

## B2. Current-encounter proposition state (“adoption”)

| field | reconciliation |
|---|---|
| Current burden | `adoption=true/false/null` is repeatedly confused with “current problem,” “problem block,” or “important enough to render.” |
| General principle | At proposition/object level, S2 records whether the current encounter **endorses the proposition as currently applicable/operative, does not currently adopt it, or leaves it unresolved**, while source temporality remains separate. |
| Consensus | **YES on semantic clarification; NO on immediate schema expansion.** |
| Current rules potentially simplified | S2-ADOPT wording, proposal-016 adoption clarification, several special explanations about historical disease vs current residual deficit |
| Schema | Keep current shape provisionally; do not build a larger assertion-state enum unless evidence requires it. |
| Naming | Rename `adoption` only if testing shows the term itself causes errors after semantics are clarified. Packet preservation is not a reason to retain a bad concept. |
| Action | **CHANGE semantic definition; schema rename/state expansion DEFER.** |

---

## B3. General source-fidelity relation rule

| field | reconciliation |
|---|---|
| Current burden | D-030/D-031 contain disease-specific causal-subject rules; seeds separately test old stroke vs residual weakness and POSSIBLE vs LIKELY. |
| General principle | For every semantic relation, preserve the **source-supported relation type, direction, strength/certainty and most specific stated participants**. Do not invent an unstated mediator, strengthen certainty, reverse direction, or replace a qualified formulation with a coarser one. |
| Consensus | **YES — strongest first-wave simplification.** |
| What becomes example rather than law | “Residual weakness rather than historical stroke” becomes one example of the general rule. |
| Current rules potentially retired/merged | Rigid causal-subject paragraph in D-030; stroke-specific causal wording in D-031; several relation-specific explanatory clauses |
| Action | **CHANGE.** |

This applies beyond causality: contributor, etiology, mechanism, cause, manifestation-of, consequence-of,
and other source-supported relations should obey the same fidelity rule.

---

## B4. S2 resolved formulation vs S3 representation selection

| field | reconciliation |
|---|---|
| Current burden | S2 may expose multiple approved representations; S3 formally selects one; several predicates protect the handoff even when S2 has only one defensible formulation. |
| Existing contract evidence | S2 already must resolve any choice that would change clinical meaning before exposing alternatives to S3. |
| Candidate simplification | When S2 has exactly one semantically resolved representation, S3 need not perform a meaningful “selection”; it may mechanically carry the sole representation. S3 retains choice only when multiple semantically equivalent/product-equivalent options legitimately remain. |
| Consensus | **Plausible but not yet proven.** |
| Ownership effect | May reduce ceremony without transferring semantic authority, but must be demonstrated. |
| Action | **TEST as a focused contract simplification.** |
| Potential benefit | Reduce approved-set/selection plumbing and some leakage predicates. |

---

## B5. Salience / ordering inputs

| field | reconciliation |
|---|---|
| Current smell | `management_reference_spans[]` is a highly specific S1 salience field before the actual S4 ordering contract is frozen. |
| Candidate generalization | Small typed source-grounded salience inputs, potentially current evaluation, current management, acuity/newness, reason-for-consult linkage, or less explicit metadata if S4 can order safely without new semantic inference. |
| Consensus | Do not freeze replacement now. |
| Sequencing | Must be tested **inside the S4 ordering experiment before the ordering contract freezes**, not afterward. |
| Action | **TEST with ordering.** |

---

## B6. R2 lexical bridge prohibition

| field | reconciliation |
|---|---|
| Current rule | Empty bridge allowlist; R2 may add no lexical connective. |
| General semantic invariant | R2 must not introduce a new causal, temporal, contrastive, conditional, attribution, certainty, negation or scope relation. |
| Concern | Doximity may not reliably respect that semantic boundary without lexical restrictions. |
| Consensus | Principle is cleaner; implementation freedom is high risk. |
| Action | **EXPERIMENT in AX-R2. Keep current restriction until evidence supports relaxation.** |

---

## B7. Source coverage accounting

| field | reconciliation |
|---|---|
| Current burden | Every source fragment/span is individually accounted/dispositioned, creating bookkeeping for headers, boilerplate and duplicates. |
| Safe generalization | Preserve full source-span coverage, but allow grouped/mechanical disposition for clearly nonclinical, administrative or duplicated boilerplate; retain proposition-level accounting for clinically interpretable content. |
| Consensus | Directionally useful but unsafe as an immediate semantic relaxation. |
| Action | **EXPERIMENT / infrastructure refinement.** |
| Guardrail | The model must not get an early unrestricted “not clinically meaningful” deletion authority. |

---

## B8. Shared actions across problems

| field | reconciliation |
|---|---|
| Current architecture | One action identity + one owner + secondary cross-problem relevance. |
| Candidate abstraction | Separate action identity, semantic problem relations, and render home. |
| Consensus | Conceptually attractive but genuinely reopens ownership architecture. |
| Action | **DEFER to AX-SHARED experiment.** |

---

# C. Layer-B specification/calibration reconciliation

## C1. Validator before semantic question

| current problem | agreed replacement |
|---|---|
| Shape and meaning are parallel scored predicates for the same field (e.g. S2-CAUSAL-01/02, S3-ROLE-01/02), creating gates and overlapping seeds. | Deterministic **validator** runs first. Semantic judgment occurs only if validators pass. Validator failure does not create a separate signer semantic packet. |
| Status | **CONSENSUS — first-wave Layer-B design.** |

Validators still require tests and evidence; “non-scored” means not a separate human semantic calibration target.

---

## C2. Combined semantic packets

| current problem | agreed replacement |
|---|---|
| One packet per predicate per artifact creates 44 near-duplicate packets. | One packet per artifact/layer can carry multiple independent semantic questions, each with its own verdict slot and context slice. |
| Guardrails | Expected answers blinded; question identities remain separate; one answer cannot satisfy another; changed question invalidates only that question/reference. |
| Status | **CONSENSUS — first-wave Layer-B design.** |

---

## C3. Intended-impact seed model

| current problem | agreed replacement |
|---|---|
| Full-silence across every semantic predicate and one-seed-per-predicate create plumbing seeds and repetitive signer workload. | Each mutation declares an **intended semantic impact set**. Mechanical validators pass unless intentionally negative. Semantic calibration targets meaningful failure modes; unrelated axes receive a cheap collateral-change check rather than repetitive signer review. |
| Seed rule | One seed per **meaningful failure mode**, not per registry entry. |
| Status | **CONSENSUS — first-wave Layer-B design.** |

---

## C4. Scenario vs fixture

| current problem | agreed replacement |
|---|---|
| Layer-local artifacts masquerade as “clean parents,” requiring `case_oracle` and parent-specific dependency hacks. | **Scenario/case** = coherent multi-layer clinical truth. **Fixture** = deliberate layer-local artifact with explicit dependencies. |
| Status | **CONSENSUS — first-wave Layer-B design.** |

---

## C5. Dependency-scoped identity/versioning

| current problem | agreed replacement |
|---|---|
| SCHEMA/PILOT/ORACLE/GATE identities churn together for wording, fixture and shape changes. | Invalidate only the smallest dependency that changed. At minimum distinguish structural/interface shape, semantic policy, source/oracle truth and concrete packet bytes/evidence. |
| Guardrail | Do not proliferate labels unnecessarily; dependency model is the invariant. |
| Status | **CONSENSUS — first-wave Layer-B design.** |

---

## C6. Current semantics registry + governance history

| current problem | agreed replacement |
|---|---|
| Normative wording duplicated across DECISIONS, predicates, registry, packet instructions and schema. | One machine-readable **current semantic contract registry** containing assertion, review question, prerequisite validators and decision/provenance reference; operational copies generated where possible. DECISIONS remains governance/provenance history with active/superseded/void status/index. |
| Status | **CONSENSUS — first-wave Layer-B design.** |

---

## C7. Generic typed decision closure

| current problem | agreed replacement |
|---|---|
| Candidate accounting, object accounting, rendered equality, reasons/bases and representation outcomes use several bespoke closure checks. | Generic mechanical invariant: every decision-bearing entity entering a stage exits with exactly one typed terminal state. Semantic reasons remain typed and distinct. |
| Status | **CONSENSUS — infrastructure design after semantic target, compatible with Layer-B redesign.** |

---

## C8. Projection/hash brittleness

| current problem | agreed replacement |
|---|---|
| Exact hashes over prose and broad campaign coupling create churn; but loosening semantic field paths risks ownership drift. | Keep exact semantic paths where they enforce authority. Hash normative machine blocks rather than incidental prose. Allow additive non-semantic metadata without campaign churn. Use dependency-scoped identities. |
| Status | **CONSENSUS — infrastructure cleanup.** |

---

# D. Consolidated five-domain semantic target

This is a **conceptual decomposition**, not a schema:

1. **IDENTITY**  
   Independent problem vs contained manifestation/consequence/context.

2. **RELEVANCE / ROLE**  
   Whether an independent problem belongs in this encounter/note; if represented, PRIMARY vs BACKGROUND.

3. **STATE**  
   What the current encounter endorses, rejects, leaves historical-only, or leaves unresolved at proposition level.

4. **RELATIONS**  
   Source-supported relationships, participants, direction and certainty/strength.

5. **USE / REALIZATION**  
   Which content is used, under which problem/section, and how it is compiled/rendered.

### Current module mapping

- S1 primarily owns IDENTITY.
- S2 primarily owns STATE + RELATIONS and resolves semantic formulation.
- S3 primarily owns RELEVANCE/ROLE + note-use.
- S4 compiles USE/REALIZATION into executable render units.
- RENDER realizes the already-decided blueprint.

This preserves one-decision-one-owner while giving us a smaller semantic vocabulary than the accumulated exception chain.

---

# E. What can likely be retired if the target is ratified

## Likely retirement/merger candidates

1. **D-015 chronic-management prerequisite** as a general retention law.
2. **D-023 inactive-major-neurologic exception** as a separate exception.
3. The **rigid residual-deficit-vs-disease causal-subject clause** of D-030.
4. Disease-specific explanatory examples promoted to governing rules.
5. Parallel scored shape predicates where deterministic validators suffice.
6. One-seed-per-predicate requirement.
7. Cross-family full-silence signer burden.
8. One-packet-per-predicate packaging.
9. “Clean parent” terminology for layer-local fixtures.
10. Broad prose-sensitive identity/hash coupling.
11. Duplicated current predicate wording across several hand-maintained files.

## Not retired

- PRIMARY/BACKGROUND as encounter role;
- causal certainty/strength as separate from role;
- source temporality as separate from current-encounter state;
- S1/S2/S3/S4 ownership boundaries;
- source-linked provenance;
- weak rendering boundary;
- semantic-vs-mechanical validation distinction.

---

# F. Experiment-only / deferred questions

| item | disposition | experiment/dependency |
|---|---|---|
| Sole S2 representation carried mechanically by S3 | TEST | Focused S2/S3 contract experiment |
| Generic salience instead of management-reference field | TEST BEFORE FREEZE | S4 ordering experiment |
| Relax R2 lexical bridge prohibition | EXPERIMENT | AX-R2 |
| Grouped nonclinical source coverage | EXPERIMENT | INGEST/coverage fixture |
| Multi-link shared actions + separate render home | EXPERIMENT / DEFER | AX-SHARED |
| Larger assertion-state enum / rename adoption | DEFER unless evidence | After semantic clarification |
| Looser typed-output projection replacing exact semantic paths | REJECT for now | Ownership risk |

---

# G. Recommended scope choice

## Option A — minimal
Containment/adoption/causal wording plus measurement cleanup, leaving most exception history intact.

**Assessment:** lower immediate change, but likely preserves concepts already identified as root causes.

## Option B — staged two-layer
Freeze the five-domain semantic target and retire the main exception chain, while designing Layer-B
simplification in parallel; implement in controlled stages after semantic ratification.

**Assessment:** **recommended by both agents after cross-review.** Fixes root causes without a big-bang rewrite.

## Option C — big-bang
Rewrite semantic and measurement systems together.

**Assessment:** not recommended. High attribution risk and unnecessary evidence destruction.

---

# H. Proposed staged sequence if Option B is selected

### Stage 1 — semantic contract freeze
- ratify five-domain decomposition as the governing conceptual model;
- define BACKGROUND relevance threshold;
- rewrite problem identity/containment, current-encounter state and source-fidelity relation rules;
- determine which clauses of D-015/D-023/D-030 are superseded;
- re-evaluate proposal 016 against this target rather than implementing it verbatim.

### Stage 2 — Layer-B contract design
- validators before semantic questions;
- combined artifact/layer packets;
- intended-impact seed model + collateral checks;
- scenario vs fixture;
- dependency-scoped identities;
- current semantics registry.

### Stage 3 — infrastructure
- generic decision-closure validation;
- projection/hash cleanup;
- regenerate packet set once;
- re-collect signer references/evaluators against the simplified semantics.

### Stage 4 — experiments
- S2/S3 representation plurality;
- S4 salience/ordering;
- R2 bridge freedom;
- source coverage grouping;
- shared-action relationship/render-home model.

---

# I. Decision required

The reconciliation is now complete enough to choose scope.

**Recommendation: Option B — staged two-layer simplification.**

This is an architecture/product choice, not a mechanical implementation detail, so it should be explicitly
ratified before contract changes begin.

No implementation, proposal-016 amendment, signer-reference expansion, Gate-0 acceptance, Doximity, or Phase 0 before that decision.
