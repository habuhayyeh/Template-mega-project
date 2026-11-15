# Review 138 — independent review of DeepSeek A/B/C architecture

## Verdict

**KEEP THE CORE ARCHITECTURE, BUT DO NOT FREEZE IT YET.**

The current direction is substantially better than the prior execution designs:

```text
Scribe V2.2
  -> A Interpret/Reconcile
  -> B Problem Architecture
  -> C Note Blueprint
  -> Render
```

The decomposition now follows the real semantic dependencies:
1. preserve source;
2. decide what the source means;
3. decide what the neurologic problems are;
4. decide what belongs where;
5. express it in prose.

Removing the pointer index, atomic fact corpus, semantic F1V, and final same-model audit was correct.

I would **not add more stages**.

However, the architecture still has several unresolved ownership/execution questions. These should be settled before the contracts are treated as frozen.

---

# What is strong

## 1. Scribe remains the canonical evidence store

This is the right architectural center.

The downstream system points back to source records instead of generating a second source corpus.

That directly avoids the earlier:
- atomic explosion;
- copied-quote drift;
- synthesized-fact support burden;
- validator loop.

## 2. A/B/C corresponds to distinct clinical transformations

The current boundaries are directionally correct:

### A
What does the source actually support?

### B
What neurologic problem structure follows from that supported meaning?

### C
How should the supported material be allocated into the note?

These are different questions and should remain different ownership domains.

## 3. Action state is treated orthogonally

Keeping:
- decision;
- execution;
- response;
- result;

separate is important and should survive.

Making it a lane inside A rather than a mandatory additional pass is a good simplification.

## 4. Blueprint before prose is essential

The note should not discover its structure while writing prose.

C producing an explicit blueprint before rendering is one of the strongest parts of the architecture.

## 5. Uncertainty is becoming first-class

A has semantic `UNRESOLVED`.

B has `ARCHITECTURE_UNRESOLVED`.

This is better than forcing a decision merely to satisfy a schema.

---

# Blocking architecture questions

## 1. The execution model is still not actually defined

This is the largest big-picture issue.

The contracts are written as if:

```text
A produces a materialized handoff
  -> B consumes it
  -> C consumes A+B
  -> renderer consumes blueprint
```

But the intended production surface is Doximity Ask with multiple modular files.

Those uploaded files are instructions/context unless Doximity actually executes them as isolated sequential
functions.

Therefore the architect must explicitly decide:

### Model 1 — real sequential invocations

```text
Ask call A -> saved A output
Ask call B -> saved B output
Ask call C -> blueprint
render call -> note
```

This gives real handoff boundaries but increases operational burden and repeated context.

### Model 2 — one Ask invocation with logical internal phases

```text
one model context
  internally performs A -> B -> C -> render
  returns note
```

This is operationally simpler, but A/B/C are then **conceptual ownership boundaries, not actual runtime isolation**.

The current architecture mixes these two models.

That matters because:
- error isolation differs;
- handoff schemas have different value;
- context size differs;
- intermediate outputs may or may not exist;
- later phases may silently reopen earlier decisions in a one-call model.

This must be settled before optimizing the contracts further.

---

## 2. A is sparse, but C is expected to recover content A did not carry

This is the most important semantic-boundary problem.

A says:

> Create a UNIT only when semantic reconciliation or downstream preservation requires one.

C says nonproblem evidence must survive, and the architecture says C may reread the packet if A did not carry it.

But C is also prohibited from reinterpretation.

Those rules cannot all be true simultaneously.

If A omits a clinically relevant exam/history/medication/workup assertion, C has only two choices:

1. ignore it and lose note content; or
2. reread the packet and interpret it itself.

Choice 2 duplicates A's semantic job.

The architecture needs one explicit answer:

### Either

A is responsible for **complete note-relevant semantic coverage**, while remaining sparse through reconciliation rather than atomicization.

### Or

C is explicitly allowed a narrow source-extraction function for nonproblem sections.

At present the ownership is ambiguous.

My preference is the first:
- A does not need one unit per sentence;
- but every assertion that could materially affect the final note must be represented or intentionally excluded.

Otherwise A is not a reliable semantic handoff.

---

## 3. Diagnostic/assessment reasoning has no clear owner

The final neurologic A/P requires more than identity and placement.

It may require:
- competing explanations;
- evidence weighting;
- why one diagnosis is favored;
- why another remains possible;
- why a manifestation belongs under a disease;
- why a contributor is plausible but not causal.

Current ownership is incomplete:

- A distinguishes source fact/reasoning conceptually, but its current `kind` schema has no explicit
  `reasoning` representation.
- B owns problem identity, containment, certainty and causal/contributory relations.
- C has a `reasoning=` field but is forbidden from making new clinical decisions.

Therefore C can easily become the place where assessment reasoning is invented.

The architect should explicitly place **diagnostic stance / differential reasoning / evidence weighting**.

I would place it in **B**, because it is part of problem architecture rather than note layout.

C should only select/render reasoning already approved by A/B.

This does not require another stage.

---

## 4. A and B still overlap on currentness/adoption

A owns:
- current vs historical;
- durable identity vs source-specific state.

DeepSeek 032 also described A as owning:
- current adoption vs outside/historical formulation.

B then outputs:
- `adoption=current_adopted|longitudinal|reported|historical|unresolved`;
- certainty/currentness.

This can produce two semantic owners for the same decision.

The distinction should be explicit:

### A
source-level state:
- what each source says;
- when it applies;
- whether the assertion is current/historical;
- who is asserting it;
- whether an outside diagnosis is being reported.

### B
problem-level encounter status:
- whether the reconciled disease identity is adopted as a problem;
- whether it is longitudinal/historical;
- what role it has in this encounter.

B may derive problem-level status from A, but may not reinterpret source-level temporality or attribution.

The terminology should make that distinction obvious.

---

## 5. PROBLEM_MAP currently risks becoming “all neurologic diagnoses”

The current threshold allows an established neurologic disease with independent identity to become a problem.

The three-record test therefore placed historical left MCA stroke into `PROBLEM_MAP` despite not knowing
whether it mattered to the encounter.

That exposes a gap.

There are three distinct things:

1. **a neurologic disease exists historically;**
2. **it is relevant enough to this encounter to preserve in history;**
3. **it deserves an A/P problem representation.**

Those are not identical.

If every independently established neurologic disease enters B, B may become a list of historical diagnoses
rather than an encounter problem map.

The architect should decide whether `PROBLEM_MAP` means:

> every independent neurologic disease identity

or:

> every neurologic problem that deserves encounter-level problem representation.

Given the user's note philosophy, I think it should be the second.

Historical neurologic diseases that matter only as history can remain available to C from A without becoming
an A/P problem.

This avoids needing a `NOT_RENDERED` pseudo-problem category.

---

## 6. C has no structured place for blueprint-level uncertainty

A has `UNRESOLVED`.

B has `ARCHITECTURE_UNRESOLVED`.

C says that if placement cannot be decided safely it should preserve the gap, but the output schema has no
explicit blueprint-unresolved structure.

That creates pressure to either:
- omit the material; or
- force a placement.

A small `BLUEPRINT_UNRESOLVED` register would solve this without adding another stage.

This is a schema fix, not an architectural expansion.

---

# Major empirical risk

## A has not been tested at realistic scale

The three-record tests are useful for boundary correctness.

They do **not** answer the most important runtime question:

> Can GPT-4o execute A over the full Scribe packet without recreating a near-full second corpus, omitting
> important material, or drifting on action/provenance semantics?

A currently owns many difficult operations at once:
- assertion type;
- referent/event identity;
- attribution;
- temporal scope;
- polarity;
- certainty;
- reconciliation;
- action state;
- unresolved detection;
- preservation of nonproblem note evidence.

That is reasonable as one conceptual layer, but it may still be too much for one Doximity execution.

Before further architecture is frozen, the full frozen Scribe packet should eventually test A for:

- output size;
- completion/truncation;
- material omissions;
- event over-merging;
- attribution fidelity;
- question-as-answer errors;
- action-state promotion;
- current/historical errors;
- nonproblem coverage;
- unresolved behavior.

If A fails at scale, the correct response is not automatically “add another stage.”

First determine *which responsibility causes the failure*.

Only then consider splitting it.

---

# Renderer question

The architecture should preserve **Render as a separate conceptual ownership boundary** even if it is
operationally executed inside the same Doximity call/file as C.

The renderer's only job is:

- wording;
- compression;
- syntax;
- formatting.

It may not reopen:
- problem identity;
- certainty;
- currentness;
- role;
- causality;
- action state.

Whether C and Render require separate **calls** should be empirical.

Do not collapse their conceptual ownership merely to reduce file count.

---

# Validation

Removing the same-model semantic validator is correct.

The architecture should distinguish:

### Semantic validation
Do not add a separate LLM PASS/FAIL stage.

### Mechanical validation
Still useful where available:
- required delimiters;
- unique IDs;
- valid references;
- allowed enum values;
- unresolved references;
- action IDs that actually exist.

These are parser/lint checks, not another semantic function.

If Doximity cannot run them, they remain development-time checks rather than runtime stages.

---

# Recommended architecture after clarification

I would preserve the same stage count:

```text
Scribe V2.2
   |
   v
A — Interpret / Reconcile
    complete note-relevant semantic ledger
    + action-state lane
    + semantic unresolved
   |
   v
B — Problem Architecture
    encounter-relevant neurologic problem map
    + diagnostic stance/reasoning
    + containment/relations/role/action ownership
    + architecture unresolved
   |
   v
C — Note Compiler
    note blueprint only
    + blueprint unresolved
   |
   v
Render
    prose only
```

No pointer index.
No atomic fact corpus.
No semantic validator.
No audit pass.
No extra stage by default.

---

# Priority order

Before freezing the architecture, resolve these in order:

1. **Actual Doximity execution model:** real sequential calls vs one-call logical phases.
2. **A completeness contract:** can C recover omitted source material or not?
3. **Owner of diagnostic reasoning/differential synthesis.**
4. **Definition of PROBLEM_MAP:** all disease identities vs encounter A/P problems.
5. **A/B source-currentness vs problem-adoption ownership.**
6. **Blueprint unresolved representation.**
7. **Full-scale A execution test before further runtime optimization.**

## Overall assessment

The architect has found the right **shape**.

The remaining risk is no longer stage proliferation.

The remaining risk is **boundary ambiguity inside the reduced stage count**.

If those ambiguities are resolved, this is the first architecture in the project that looks both clinically
natural and operationally defensible.
