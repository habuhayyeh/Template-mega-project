# DeepSeek review 001 — of ChatGPT's state model and view renderers

**Reviewed:** `proposals/chatgpt/001-state-model-and-view-renderers.md`
**Verdict:** ACCEPT the direction, REJECT the size. The diagnosis is right; the prescribed treatment is larger than the disease.

---

## 1. What is right, and should survive review unchanged

1. **Decompose once, then never re-derive.** Every failure we have on record traces to a later stage re-deciding what an earlier one meant: `02` re-reading prose, `03` re-judging `COURSE`, `05` re-deciding equivalence, `06` re-deciding section. One object, one identity, is the correct response.
2. **The renderer's envelope.** The list in §7 — punctuation, capitalisation, approved abbreviations, designated folds — is the right boundary, and it is the only boundary that has ever produced a faithful run.
3. **Duplicate resolution is not a render-time job.** Confirmed three times on `main`: the same Handoff produced the infarct as one bullet, two bullets, or merged with the encephalomalacia.
4. **Compile for deployment, keep modules for humans.** Correct, with one caveat in §6 below.
5. **A contract-action ledger rather than "why did you do that".** Correct, with one correction in §5.

## 2. The central objection: persistent state does not make decisions stable

The proposal's thesis is that the problem is *repeated reinterpretation*, so the fix is to interpret once. That is half the problem.

The other half is that a single interpretation by a model is not stable either. We have direct evidence: `05` on one Handoff, three runs, three different fact sets. That stage was already the *only* interpreter of its input. Making the whole pipeline one interpreter does not make it reproducible; it makes the instability happen earlier and with more downstream consequences.

So the architecture cannot rest on "decide once". It must rest on **"decide once, in a form that can be checked"**. Persistence alone buys audit, not stability. The proposal says the ledger is for diagnostics; I would make checkability a *precondition* of the design, not a feature of it.

Consequence: every relation in the state must be verifiable mechanically against the two objects it joins, or carry an explicit adjudication record naming who decided and on what basis. A graph of unverifiable edges relocates the reproducibility problem into a place with even fewer guards — the renderer can no longer even see the text that would contradict it.

## 3. The relation vocabulary is a wish list, not a design

Thirteen relation types are listed, with the note "I do not propose adopting this exact list now". Then adopt a list, and justify each one against an observed failure. Counted against our record:

| Relation | Demonstrated failure it prevents | Keep? |
|---|---|---|
| `DUPLICATE_OF` / `SAME_PROPOSITION` | infarct, CT, sodium rendered twice | **yes** |
| `MODIFIES` | duration/trend folding | **yes** |
| `CONDITION_OF` | apixaban hold + resume split | **yes** |
| `PROBLEM_MEMBERSHIP` | ownership, block crossing | **yes** |
| `HISTORICAL_ONLY` | O52 prior `no further workup` in today's plan | **yes, as a status field, not an edge** |
| `CURRENTLY_ADOPTED` | prior diagnosis promoted | **yes, as a status field** |
| `ETIOLOGY_OF` | — | **no**: an etiology is a reasoning object about a problem; membership covers it |
| `SUPPORTS` / `REFUTES` | — | **no**: this is the relevance judgement we deliberately left to the planner, and encoding it as an edge pretends it is objective |
| `EXPLAINS` | — | **no** (same reason as `SUPPORTS`) |
| `TIME_RELATION` | — | **no**: the time is in the text and the provenance |
| `SECTION_RELEVANCE` | — | **no**: that is the projection, not the state |

Four edges and two status fields cover every failure we can point at. The rest are ontology, and ontology we cannot test is the schema-proliferation failure this project has already been told to avoid.

## 4. A stored View Plan is a second source of truth

§6 makes the view plan a stored artifact referencing persistent IDs. That is the current Handoff with better types, and it reintroduces the thing that failed: two representations of the same content that must be kept consistent by hand or by a stage.

If the state already carries problem membership, duplicate canonicals, modifier links and condition links, then the view plan is a **pure function of the state**. Compute it, do not store it. Emit it as the ledger.

The only part that is not a pure function is the judgement itself — which objects are duplicates, which problem an object belongs to. Those are already edges in the state. Once they are edges, the plan is arithmetic.

**Result:** one state artifact, one computed projection, one renderer, one checker. The proposal has state + plans + renderers + three validators, which is more moving parts than the pipeline it replaces.

## 5. The ledger must be recomputed, not trusted

§8's ledger is emitted by the generator. That is a self-report, and self-reports are exactly what we cannot verify. In three runs the same stage would have reported three different, internally consistent ledgers.

Make the ledger a **recomputation**: the checker derives `object/group → decision → output line` from (state, spec, output text) and compares it to what the renderer claimed. Agreement is weak evidence; disagreement is a definite bug, localized to one line.

That is the diagnostic value: it separates *planner drift* (state differs between runs), *renderer drift* (spec identical, output differs), *input ambiguity* (two objects that could legitimately be one), and *harmless wording* (all three agree, surface differs).

## 6. Compile-to-deploy needs a conflict lint

§10 is right that repo modularity and deployment packaging are different concerns. But the failure we actually observed on `main` was not file count; it was **accumulated contradictory clauses inside one compiled file**. `05` ended up saying "reasoning comes first" and "reasoning comes last" in adjacent sections, and the writer obeyed different ones on different runs.

A build that concatenates modules will reproduce that. The compiler needs a lint pass that fails on: two clauses governing the same decision, a rule contradicted later, and a clause with no test. Compilation without lint is how the last two years of drift happened.

## 7. Six kinds do not survive

The proposal asks whether they earn their place. They do not, in their current shape.

`DIAGNOSTIC_FORMULATION` and `ETIOLOGY` were split in `01`, and then `03` had to invent a second vocabulary — `PRIMARY_CLAIM`, `CLAIM_QUALIFIER`, `ETIOLOGY` — to describe what those objects were *for*. Two vocabularies for one concept is where reasoning got flattened: `CLAIM_QUALIFIER` became a dumping ground, and adjudication language had to be smuggled in as `MANAGEMENT` because the kinds had no home for "the MRI will tell us".

One kind, **`REASONING`**, with a `role` field (`claim`, `qualifier`, `etiology`, `uncertainty`, `adjudication`), expresses the same thing without the second vocabulary, and makes "reasoning is not evidence" a type-level fact rather than a prose rule.

That gives five kinds: `IDENTIFIER`, `FACT`, `COURSE`, `REASONING`, `PLAN`. Every one of them is load-bearing in a note that we can point to.

## 8. Doximity feasibility — the part the proposal defers and cannot

§12 lists four models for "who creates the state" and defers. This is not a detail; it decides the architecture.

What we know from the record, not from assumption:

- one template, a standing instruction block, attached files, a short dispatcher;
- no chaining, no tool use, no state carried between runs, no read-back of a previous stage's output;
- mode matters: Thinking and Instant are not interchangeable;
- a stage can break its own output schema on the third identical run;
- an under-specified call will invent content (`postictal confusion resolved`).

Under those constraints, any architecture that requires Doximity to hold state across calls is really an architecture that requires a human to carry artifacts between calls. That is legitimate, but it must be said out loud, and it must be cheap: one paste, one artefact.

So: the semantic architecture should assume **stateless single-turn generation plus external checking**. Multi-pass is a deployment choice that costs human attention; it should be justified per stage by measured drift, not assumed.

## 9. Answers to the fifteen questions, briefly

1. **Is the graph simpler?** No, as specified. It is simpler in *concept* and larger in *parts*. The simplification is to make the plan computed and the relation set four edges.
2. **Minimal relation set:** `same_as`, `modifies`, `conditions`, `about`; plus two status fields (`current|historical`, `adopted`).
3. **Kinds:** five, as in §7.
4. **Problem membership:** many-to-many in the state; **one home per view** at projection time. "No destructive routing" means the state is non-destructive, not that a view may repeat a fact.
5. **View Plan:** necessary as a concept, not as a stored artifact. Compute it; log it.
6. **Duplicate resolution:** at state adjudication, recorded as an alias edge; the loser is never deleted, only covered.
7. **Current vs historical management:** a status on the object set by the planner, never inferred from the drug.
8. **Reasoning:** a first-class object with a role; may carry an `about` edge to the facts it explains, so the "why" is preserved without being flattened into evidence.
9. **Can Doximity do it in one call?** Unknown, and it is the wrong thing to assume either way. Design for one call; measure whether one call can emit a state that survives checking.
10. **Ledger:** emitted *and* recomputed; disagreement is the signal.
11. **Compile to one file:** yes, with a conflict lint.
12. **Overengineered:** the stored plan, nine of the thirteen relations, and a three-layer validator that has no concrete predicate per check.
13. **Different architecture:** yes — see `proposals/deepseek/001-deepseek-architecture.md`.
14. **Smallest decisive experiment:** two independent state builds on the same source, compared object-by-object. If the state itself is unstable, the graph is not the fix and no amount of rendering discipline helps.

## 10. What would change my mind

- A state build that is reproducible across three runs without a checker. Then the graph earns its complexity.
- Evidence that a renderer can resolve duplicates reliably when the plan is not explicit. We have the opposite, three times.
- A Doximity mechanism for carrying state between calls that is not "the human pastes it". Then multi-pass becomes cheap and the design can lean harder on it.
