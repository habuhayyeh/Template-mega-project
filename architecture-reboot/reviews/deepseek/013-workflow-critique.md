# DeepSeek response 013 — two-LLM implementation workflow

**Verdict:** accept the shape. Five changes, one of them structural.

---

## 1. Structural — support systems cannot be Phase 5

`CHECK`, `AUDIT` and `BUILD` are not support. They are the definition of correct, and if they arrive after the pipeline they will describe whatever the pipeline happened to do.

On `main` this is exactly what happened: validators were written after the artifacts, so each validated the behaviour we had rather than the behaviour we wanted, and the real checks were discovered one failure at a time.

Minimum order:

- **BUILD lint at Phase 0**, before any runtime file. The moment two contract files exist they can contradict each other, and the lint is the only thing that notices. `05`'s "reasoning first / reasoning last" was two files of drift that no runtime check could see.
- **The IR checker immediately after the schema**, before RENDER exists. It defines what a valid IR is; writing RENDER first means the renderer defines it.
- **AUDIT can stay late** — it needs fixtures, not code, and it is the only one that is genuinely a review instrument.

## 2. Acceptance briefs — yes, with one constraint

Briefs before implementation are right: they force the reviewer to say what correct means before the engineer can rationalise.

The risk is duplication. A brief that restates the architecture becomes a second specification, and we have already paid for that once — the anchor drifted from its own example.

Constraint: a brief may contain only three things — the fixture input, the required IR properties, and the check that decides. It cites the frozen architecture by section reference and never restates it.

## 3. File order — add a vertical slice after Phase 1

Phase-by-phase authoring means nothing runs until four modules exist, and the seams are exactly where we have never tested. After the shared contracts, build **one tiny end-to-end slice** — one source, one span, one object, one unit, one line — and run it through CHECK. If the seams are wrong, that is the cheapest place to find out.

Then fill the phases outward.

## 4. Change control — a fourth category is missing

`PATCH / IMPLEMENTATION / DESIGN` is right, and it is missing the one that did the damage: **ACCEPTANCE CHANGE** — any alteration to a fixture, a check, or an expected property.

On `main`, several rounds moved the goalposts by editing what was being measured, and it was recorded as a patch. It needs its own category and the same scrutiny as a design change, because it silently redefines success.

## 5. Independent Doximity scoring — blind, and against the IR

Agreed in principle, three specifics:

- the scorer must not know which run is which, or the score follows expectation;
- score against **IR properties and mechanical checks**, not prose quality — otherwise the score measures taste;
- the person who ran Doximity should not be the sole scorer. That is how we ended up labelling a hand-edited run `reviewed` and treating it as generated.

## 6. Role division

Accept as written, with one note: the reviewer authors the fixtures, and fixtures should come from the historical failures we already have — there are ten on record. Invented fixtures encode the reviewer's imagination; historical ones encode defects that actually reached output.

---

## What I would not change

The one-artifact-at-a-time rule, the independent review before validation, and the freeze step. Those three are the parts that would have prevented most of last month.
