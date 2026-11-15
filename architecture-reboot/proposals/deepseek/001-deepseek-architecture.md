# DeepSeek architecture 001 — state, projection, render, check

A competing design, reasoned independently of `proposals/chatgpt/001`. It agrees on the diagnosis and on roughly half the treatment, and disagrees on the size.

**One sentence:** a small semantic state, a deterministic projection that turns it into a render spec, a deliberately weak writer, and a checker that recomputes the projection from the output rather than trusting what the writer says it did.

---

## 1. What we are actually solving

Not "reinterpretation" in the abstract. Three concrete failures, each reproduced:

1. **The same input produced different facts.** Three runs, three fact sets: one or two infarct bullets, one or two CT bullets, apixaban hold and resume together or apart.
2. **Content appeared that no input contained.** `postictal confusion resolved`, from a run given no instructions.
3. **Content that a decision excluded came back.** O54 rendered repeatedly after D-014.

(1) is a selection problem, (2) is an instruction-envelope problem, (3) is a state-representation problem. No single abstraction fixes all three; the design should name which component owns each.

## 2. The design

```text
SOURCE  →  INGEST (model)  →  CASE STATE  →  PROJECT (deterministic)  →  RENDER (model)  →  CHECK (deterministic)
                                   │                                          │                    │
                                   └────────────── ledger ◄───────────────────┘────────────────────┘
```

Five parts, one of which is a data structure and two of which are code.

### 2.1 Case State

**Responsibility:** hold everything the encounter said, once, with identity and the four relationships that the renderer must not reinvent.

**Consumes:** source material (recording/transcript, dictation, prior records).
**Produces:** the state artifact — one JSON-ish document, human-readable.

```text
problem:
  id, label, claim_id, order

object:
  id                O#
  kind              IDENTIFIER | FACT | COURSE | REASONING | PLAN
  text              verbatim source wording, never rewritten
  provenance        [letter, source name, date]
  status            CURRENT | HISTORICAL | PROPOSED
  adopted           true | false        (REASONING: is this the current clinician's own claim?)
  role              REASONING only: claim | qualifier | etiology | uncertainty | adjudication
  speaker           optional, only when the source names one
  about             problem id

edge:
  type              SAME_AS | MODIFIES | CONDITIONS
  from, to          object ids
  canonical         SAME_AS only: which id renders
  basis             free text, required — why this edge exists, in the record's words
```

**Allowed:** create objects and these four edges; assign status and role; name the problem a proposition is about.
**Forbidden:** inventing clinical content; deleting an object; expressing a relationship that no edge type covers.
**Auditable:** every object is source text plus a marker; every edge carries a `basis` string a human can check against the source.
**Why it must exist:** because every alternative we tried let a later stage re-decide. There is no smaller carrier of "what was said" and "what relates to what".

**Deliberate omissions:** no `SUPPORTS`/`REFUTES`/`EXPLAINS` edges, no section fields, no render order, no bucket. Those are the projection's job, and encoding them in the state is how a state becomes a second note.

#### Five kinds, not six

`DIAGNOSTIC_FORMULATION` and `ETIOLOGY` collapse into `REASONING` with a `role`. The old split is what forced a second vocabulary at the organisational layer (`PRIMARY_CLAIM`, `CLAIM_QUALIFIER`, `ETIOLOGY`), and that duplication is where reasoning got flattened and where adjudication language had to be smuggled in as `MANAGEMENT` because no kind could hold it.

| Kind | Holds | Never holds |
|---|---|---|
| `IDENTIFIER` | age, sex, provenance of the person | any clinical claim |
| `FACT` | observations, exam, results, devices, history of disease | a plan, a formulation |
| `COURSE` | timing, tempo, trend, status of a fact | a new finding |
| `REASONING` | claim, qualifier, etiology, uncertainty, adjudication | evidence |
| `PLAN` | actions, orders, holds, decisions, conditions | results |

Five is not a target; it is what remains when each kind has to answer "what would be lost if this were merged into another?"

### 2.2 Projection

**Responsibility:** turn the state into a render spec, one spec per section, by fixed rules. No model.

**Consumes:** the state; a section list.
**Produces:** the render spec — ordered lines, each naming a head object, the folds to apply, and the class.

```text
SECTION A/P
PROBLEM P1
  LINE L1  class=FACT      head=O7  fold=O8(timing)         cover=[O53]
  LINE L2  class=FACT      head=O17                          cover=[O44]
  LINE L3  class=REASONING head=O39                          cover=[O23]
  LINE L4  class=REASONING head=O35                          role=etiology
  PLAN L5  head=O12 cond=O25 bucket=medication
```

Rules, all mechanical:

1. **Coverage.** For each problem, every object `about` it is placed in exactly one line, as head or cover, or is marked `OMITTED` with a reason.
2. **Duplicates.** `SAME_AS` collapses to `canonical`; the others become `cover`.
3. **Folds.** `MODIFIES` attaches the modifier's words to the head's line.
4. **Conditions.** `CONDITIONS` attaches the condition to the plan head.
5. **Class order.** Facts, then reasoning, then plan. Within a class, state order.
6. **Buckets.** Plan lines sort by the bucket declared on the plan object (`investigation | medication | other | follow_up`).
7. **Status.** `HISTORICAL` never enters the plan; `CURRENT`/`PROPOSED` may. `adopted=false` reasoning never becomes a claim.
8. **Views.** The same object may appear in several sections; within one section it appears once.

**Allowed:** ordering, coverage, bucket assignment, omission with a recorded reason.
**Forbidden:** inventing a line, changing wording, deciding that two objects are the same when no edge says so, or deciding relevance beyond the declared status.
**Auditable:** it is code; its output is a table.
**Why it exists:** because the ordering/coverage decisions are exactly the ones that drifted, and they are decidable without a model once the state carries the relationships.

**This replaces the stored "view plan".** The plan is not an artifact anyone authors or maintains; it is the projection's output, logged. Storing it would create two sources of truth for the same content, which is the failure the Handoff already demonstrated.

### 2.3 Render

**Responsibility:** turn one spec line into one line of prose.

**Consumes:** the spec line, the head text, the fold text, the section's style contract.
**Produces:** prose, one line per spec line, in spec order.

**Allowed:** capitalisation, terminal punctuation, the approved transformation table (number/unit, `about`→`~`, `x ago`→`x prior to presentation`, speaker attribution, provenance parenthetical, date display, impersonal voice), and folding exactly the text the spec marks as foldable.
**Forbidden:** selecting, omitting, merging, reordering, deciding equivalence, inferring a target, adding a word outside the table.

**Auditable:** every output line maps 1:1 to a spec line. That is the whole contract, and it is checkable.
**Why it exists:** language. Someone has to turn fragments into readable clinical prose, and the model is good at that and bad at everything else in §2.2.

### 2.4 Check

**Responsibility:** prove the output matches the spec, and recompute the ledger.

**Consumes:** state, spec, output prose.
**Produces:** pass/fail plus a ledger of disagreements.

Checks, all mechanical:

1. line count and order equal the spec;
2. every head's content words appear in its line;
3. every fold appears;
4. no word in a line is absent from its head, its fold, the transformation table, or the standing-item list;
5. voice rule (no first-person in the A/P);
6. every spec line accounted for; every state object accounted for exactly once;
7. `HISTORICAL` objects absent from the plan;
8. duplicate lines absent by head identity;
9. **source fidelity** — every proposition in the ledger appears in the source, and every source sentence is accounted for as used, merged, or explicitly not used. This is the check that separates a note from a well-formed hallucination.

**The ledger is recomputed, not trusted.** The renderer may also emit one; the checker derives its own from (state, spec, output). Where they disagree is the bug. A self-reported ledger alone is a claim, and claims are what we have been unable to verify.

### 2.5 The ledger

One row per object per section:

```text
O7  | P1 | HEAD    | L1 | RENDERED
O53 | P1 | COVER   | L1 | TRACED_ONLY
O18 | P1 | OMITTED | -  | NOT_SELECTED: not material to the seizure claim
```

It is the projection's output plus the checker's reconciliation. It answers: was this object rendered, covered, or dropped, and by which rule. It never contains reasoning about *why* the clinical content is right — that is the planner's judgement, recorded in the edge `basis` strings.

## 3. Decisions, sorted by where they must live

**Fixed before rendering (state or projection):**

- which objects exist;
- which are the same proposition, and which renders;
- which problem each belongs to;
- whether a `COURSE` entry modifies a fact or stands alone;
- whether a plan entry is current, historical, proposed;
- whether two plan entries are one decision;
- whether a reasoning object is the claim, a qualifier, an etiology, or an uncertainty;
- whether a standing item's trigger is met;
- section coverage and order.

**Left generative (render):**

- sentence shape within a line;
- punctuation and capitalisation;
- applying the transformation table;
- folding designated text.

**Deterministic (code):**

- coverage and omission accounting;
- ordering and bucketing;
- duplicate collapse;
- the ledger;
- every check in §2.4.

## 4. Doximity topology — declared, not assumed

The signer has now stated the operating workflow:

> copy chart material (imaging, labs, prior notes) into the ask field, add the scribe transcription, run the template.

That is **one call, one paste, all material inline**. It is not a multi-pass workflow, and it does not include a human carrying artifacts between stages. The architecture must fit that, not hope it changes.

Three consequences, and they are not small.

1. **"Deterministic" means "mechanically checkable afterwards", not "computed by code during generation".** Inside Doximity there is no code. The projection rules are executed by the model and verified by our checker outside. That is weaker than a real compiler pass, and pretending otherwise would be the same error as assuming Doximity behaves like a program.
2. **The state must be emitted, or there is nothing to check.** One call therefore produces two artifacts: the note, and the case state / execution ledger. The note is what the clinician sees; the ledger is what the engineer checks. Production can discard the ledger; testing keeps it.
3. **The checker must compare against the source, not only against the ledger's self-consistency.** A model can emit a ledger that agrees with its own output and disagrees with the encounter. So the checks are: every ledger proposition appears in the source, every source sentence is accounted for (entered, merged, or explicitly not used), every note line maps to a ledger line, and every ledger line maps to a source span.

That is what makes a single-call design auditable: the ledger is not evidence of correctness, it is the thing the checker tests against the source.

Two-pass remains possible as a *manual* option — pass 1 emits the state, the user pastes it back for pass 2. It is not the default, it is not required, and it costs the signer a paste per encounter. It becomes worth doing only if measurement shows the single call cannot hold state and note together.

## 5. Packaging

Development: many small modules, one responsibility each, each with its own tests.
Deployment: a compiled `ENGINE.md`, plus `STYLE.md` if the contract grows.

Compilation must include a **conflict lint** that fails on:

- two rules governing the same decision;
- a later rule contradicting an earlier one;
- a rule with no test;
- a rule whose scope is outside its stage.

The `05` failures were not caused by file count. They were caused by contradictory clauses accumulated inside one file. A build without a lint will reproduce that exactly.

## 6. Experiments, smallest first

**E1 — is the state reproducible?**
One source, two independent `INGEST` runs, same model, same mode. Compare object sets (by normalised text) and edge sets by Jaccard. Target: ≥0.95 object agreement, ≥0.9 edge agreement.
*Why first:* if the state is not stable, the graph is not the fix, and no renderer discipline saves it. This single experiment decides whether the whole proposal is viable.

**E2 — is the renderer stable given a spec?**
One frozen state, one frozen spec, five `RENDER` runs, Instant. Measure: line count, per-line head content, transformation conformance. Target: 5/5 identical structure; wording variation allowed only inside the table.
*Why:* it isolates the writer from the planner. We have never measured these separately.

**E3 — one call or two?**
Same source, one-call run vs two-call run. Compare final notes and ledgers. Target: no material difference → one call wins on operational cost.
*Why third:* it is the most expensive and only matters if E1 and E2 pass.

These are cheap. E1 and E2 are ten model calls between them and answer the questions the last six rounds argued about.

## 7. Where I disagree with the proposal, and why

| Point | ChatGPT | DeepSeek |
|---|---|---|
| View plan | stored artifact | computed projection, logged |
| Kinds | six, open question | five; formulation+etiology merge into `REASONING`+role |
| Relations | 13 proposed | 4 edges + 2 status fields |
| Ledger | emitted | emitted **and** recomputed; disagreement is the signal |
| Validators | three layers | one checker with eight concrete predicates |
| Who builds state | deferred | the experiment decides; design must not assume |
| Compile | concatenate modules | compile with a conflict lint |

## 8. What I am not claiming

- That this design is proven. It is a smaller bet on the same thesis, and E1 could falsify both.
- That the five kinds are final. They are the smallest set that survives the "what is lost if merged" test.
- That Doximity will do this in one call. It is the default to test, not an assumption.

## 9. For the user, not for the agents

Two things here are not mine to decide:

1. **Whether a two-pass workflow is acceptable** — it requires a human paste per encounter. That is a product decision, not an architecture one.
2. **Voice is section-scoped, and the signer has now settled it:** the body note may be personal, the A/P must be impersonal (D-017). So the transformation table is not global — it carries a scope column, and the impersonal-voice transform applies to the A/P only. The body renderer may keep first person where the source does.
