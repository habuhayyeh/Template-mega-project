# ChatGPT review 102 — cross-review of DeepSeek 017 rule-complexity audit

## Scope

This is a review of `reviews/deepseek/017-rule-complexity-review.md` after both agents completed their
independent audits. No architecture, contract, schema, predicate, seed, scorer, or packet is changed.

## Overall verdict

**ACCEPT WITH MODIFICATIONS.**

DeepSeek found a real class of complexity that my independent review underweighted: the Gate-0
measurement system itself has accumulated too much ceremony around identities, predicate granularity,
seed requirements, packet multiplication, fixture modeling, and duplicated normative wording.

However, DeepSeek's audit is **too narrow to serve as the architecture simplification audit by itself**.
Its declared scope is the current GATE0-C3 package, so it largely misses the runtime/clinical semantic
rules that are generating the underlying contract churn. Simplifying only the harness would make
calibration cheaper without necessarily making the architecture simpler.

The right synthesis is:
- DeepSeek 017 = strong audit of **measurement/governance complexity**;
- ChatGPT 101 = audit of **runtime/semantic complexity**;
- both layers need simplification, but semantic architecture should be simplified first enough that the
  measurement system is not optimized around rules we plan to delete.

---

## 1. Separate shape / semantic-policy / packet identities

### Verdict
**ACCEPT, with one qualification.**

DeepSeek is right that SCHEMA/PILOT/GATE/campaign identities have become coupled more tightly than the
meaning of the changes requires. A wording-only semantic clarification should not pretend the schema
shape changed.

### Modification
Do not define the exact identity taxonomy by target count yet. The invariant should be:

> identity invalidation follows the smallest semantic dependency that actually changed.

At minimum distinguish:
- structural/interface shape;
- semantic policy/predicate meaning;
- oracle/source truth;
- concrete packet bytes/evidence instance.

A signer reference must still invalidate whenever the **question meaning or packet content relevant to
that judgment changes**. The goal is to stop unnecessary campaign/schema churn, not weaken evidence
binding.

### Risk
Too many fine-grained identities can itself become another bookkeeping system. Prefer a dependency
model over an arbitrary proliferation of version labels.

---

## 2. Mechanical shape checks should not be parallel semantic predicates

### Verdict
**STRONGLY ACCEPT.**

The S2-CAUSAL-01/02 and S3-ROLE-01/02 gating history is direct evidence that we modeled prerequisite
validity as peer findings instead of as validation before semantic judgment.

### Modification
I would phrase the target as:
- **validator**: deterministic prerequisite, pass/fail/undecidable as applicable;
- **semantic question**: human/LLM judged only if validators pass.

Mechanical validators still need tests and acceptance evidence. “Non-scored” should mean **not a
separate human semantic calibration target**, not “unmeasured.”

This aligns with my review-101 candidate 8: a generic typed decision-closure / validation framework can
replace several bespoke predicate pairs.

---

## 3. Full silence across every active semantic predicate

### Verdict
**ACCEPT THE PROBLEM; MODIFY THE PROPOSED FIX.**

DeepSeek is right that full cross-family silence created 44 packets for five questions. But simply
declaring unrelated semantic axes out of scope risks hiding collateral semantic damage from a mutation.

### Better generalized rule
Every mutation declares an **intended semantic impact set**.

- Mechanical validators must all pass unless the mutation is explicitly a mechanical negative fixture.
- Semantic questions in the intended impact set receive direct calibration.
- Other semantic axes need a **collateral-change check**, but not necessarily a fresh signer question on
  every packet.

Possible ways to implement that later:
- compare against the clean-parent semantic state;
- ask all layer questions once in a combined artifact packet;
- use invariant inheritance where unchanged source/fields make the answer mechanically reusable.

So the simplification target is **no repetitive signer review**, not “we no longer care whether a seed
breaks another semantic axis.”

---

## 4. One packet per artifact/layer rather than per predicate

### Verdict
**STRONGLY ACCEPT.**

This directly addresses the user's concern about repetitive micro-questions. One coherent source/context
packet can carry several independent semantic questions with separate verdict slots.

### Required safeguards
- expected answers remain blinded;
- each question retains its own predicate/version identity;
- one answer cannot satisfy another by implication;
- evaluator output remains per-question even when context is shared;
- packet-level reuse must not silently reuse a changed question.

This should probably be designed together with item 3, because combined packets are one way to retain
collateral semantic checking without 44 near-duplicates.

---

## 5. Remove the one-seed-per-predicate requirement

### Verdict
**STRONGLY ACCEPT.**

A requirement that every predicate have a mutation seed has encouraged artificial “plumbing” seeds.
Mechanical contract checks belong primarily in unit/property tests and focused invalid fixtures.

### Modification
Do not freeze “~10–12 clinical seeds” yet. Seed count should emerge from the number of **distinct
semantic failure modes we actually need to discriminate**, including positive/negative boundaries where
clinically material.

The rule should be qualitative:
> one seed per meaningful failure mode, not one seed per registry entry.

---

## 6. Separate full campaign scenarios from layer-local fixtures

### Verdict
**STRONGLY ACCEPT.**

Calling layer-local artifacts “clean parents” overloaded the concept and forced harness exceptions such
as parent-specific dependency context.

### Generalized replacement
Use:
- **scenario/case** for coherent multi-layer clinical truth;
- **fixture** for a deliberately bounded layer-local artifact with explicit dependencies.

A fixture does not need to pretend to be a complete case.

This is mostly experiment/harness architecture, not runtime architecture.

---

## 7. One semantics registry / reduce duplicated normative wording

### Verdict
**ACCEPT WITH GOVERNANCE CAUTION.**

DeepSeek correctly identifies duplicated normative text across DECISIONS, predicates, registry,
schema, packet instructions, and generated artifacts.

### Modification
Use a single current **semantic contract registry** as the machine-readable source for:
- predicate id;
- current assertion;
- plain-language review question;
- prerequisite validators;
- decision/provenance reference.

Generate operational copies from it where possible.

But do **not** collapse DECISIONS.md into the registry. Decisions are governance/provenance history;
the registry is current executable policy. The solution to D-024→D-029 is not merely generation—it is
clear active/superseded/void state and a current-decision index so old corrections cannot masquerade as
current policy.

---

## Review of DeepSeek's target numbers

DeepSeek proposes:
- 5 semantic questions;
- ~8–10 validators;
- one packet per artifact/layer;
- ~10–12 clinical seeds;
- one semantics registry;
- separate shape/policy/packet identities.

### Verdict
**Directionally good, not yet a contract.**

The five current semantic families are a useful starting set, but after the runtime semantic
simplification audit we may merge or redefine some of them. For example:
- adoption may become a more general current-encounter assertion-state question;
- causal subject may become part of a general relation-fidelity question;
- S2 representation and S3 selection may shrink if resolved-formulation becomes the default.

Therefore we should not optimize the Gate-0 package around exactly five current questions until the
semantic architecture review is reconciled.

---

# What DeepSeek 017 missed

These omissions are not defects relative to its declared GATE0-C3 scope, but they matter relative to the
signer's broader request to simplify the architecture.

## A. Clinical exception chain
It does not address D-015/D-023/D-030 and the accumulated special rules for chronic/background problem
retention, encounter role, residual deficits and containment.

## B. “Adoption” semantic confusion
It treats adoption as one of five stable questions rather than asking whether the concept/name itself is
causing architectural confusion.

## C. Causal rule over-specialization
It does not question the stroke/residual-deficit-specific causal-subject rule or generalize it to
source-faithful relation preservation.

## D. S2 -> S3 representation ceremony
It does not ask whether “multiple approved representations then S3 selection” is routinely necessary
or whether a resolved formulation should be the default.

## E. S1 salience field specificity
It does not question `management_reference_spans[]` as a case-specific ordering/salience device.

## F. R2 lexical prohibition
It does not examine whether the empty bridge allowlist pushes ordinary discourse planning upstream and
over-structures the IR.

## G. Source-fragment accounting
It does not examine whether dispositioning every mechanical fragment is more bookkeeping than value.

## H. Shared-action one-owner semantics
It does not question whether semantic ownership and render placement are being conflated.

## I. Field-path projection brittleness
It identifies identity churn but not the deeper possibility that exact per-path projection contracts
are themselves too brittle.

---

# What ChatGPT 101 missed, revealed by DeepSeek 017

My independent audit underweighted:
1. campaign/schema/policy identity coupling;
2. shape-vs-semantic predicate duplication;
3. full-silence cross-family calibration burden;
4. packet-per-predicate multiplication;
5. seed-per-predicate artificiality;
6. “clean parent” fixture overloading;
7. duplicated normative wording and governance state.

These are substantive omissions. DeepSeek's report materially improves the audit.

---

# Combined interpretation

There are **two different simplification layers**:

### Layer A — simplify the actual semantic architecture
Examples:
- problem identity/containment;
- current-encounter proposition state;
- generalized relation fidelity;
- representation/selection boundary;
- salience;
- rendering freedom;
- shared-action relationships.

### Layer B — simplify how we specify and test it
Examples:
- validators before semantic questions;
- combined packets;
- meaningful seeds only;
- explicit fixtures;
- semantic registry;
- dependency-scoped identities.

We should simplify **Layer A first conceptually**, then design Layer B around the smaller rule set.
Otherwise we risk building an elegant calibration harness for semantics we are about to replace.

## NEXT

1. DeepSeek reviews ChatGPT 101 item-by-item using the same standard:
   ACCEPT / MODIFY / REJECT; identify risks and missing counterexamples.
2. DeepSeek explicitly comments on the nine runtime/semantic items it did not cover.
3. After both cross-reviews exist, ChatGPT produces a reconciliation matrix:
   - consensus simplifications;
   - disagreements requiring experiments;
   - items to defer;
   - load-bearing rules to preserve.
4. No implementation or proposal-016 amendment before that reconciliation.
