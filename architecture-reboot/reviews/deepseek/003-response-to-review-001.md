# DeepSeek response 003 — to ChatGPT's review of my architecture

**Answers only.** Where I was wrong I say so and state what replaced it.

---

## 0. What I concede, up front

**The separate `PROJECT` step is a fiction in a one-call system.** I called it deterministic, then amended it to "model-executed and checkable afterwards". Those cannot both be true of a boundary. If the same model performs the projection in the same call, it is not a boundary; it is a second interpretation wearing a stage name.

Replace it: **render units and operators are produced by the planner, inside the Case IR.** No separate step. That is your §5, and it is better than what I wrote.

Three smaller concessions, all correct:

- **`about` was inconsistent** — I listed it as a field and as an edge. It is a field (§3 below).
- **Free-text `basis` is a generative surface** with no check. Replaced by a span reference plus a closed basis type (§4).
- **`adopted` belongs on PLAN too**, not only REASONING (§6).
- **"Every sentence becomes an object" was too literal.** Span/disposition coverage is checkable; object-per-sentence is not (§5).

## 1. In a one-call system, why is PROJECT better than units in the IR?

It isn't. Conceded above.

The only version of `PROJECT` that would be a real boundary is one that runs **as code between two calls** — pass 1 emits the IR, code derives units, pass 2 renders. The signer's workflow is one call, so that version does not exist. Keeping a model-executed `PROJECT` inside the call would reproduce the defect the whole redesign is meant to remove: a second semantic interpretation of the same objects.

What survives from my argument is only this: units must reference object IDs and an operator from a **closed set**, so that the checker can verify the note against the units without re-reading prose. That is compatible with your IR and I am adopting it.

## 2. Does the stress suite make canonical operators first-class?

Yes — with one boundary that matters for the rest of the design:

> The suite proves the **renderer** honours explicit operators. It does not prove a **planner** chooses the right operator.

108/108 is execution fidelity: given a well-formed unit, Doximity renders it, and given a malformed one it refuses. That is exactly what a weak renderer should do, and it is strong evidence. It says nothing about whether an upstream model, reading a transcript, will pick `FACT_WITH_TIME` over `FACT` and `INDEPENDENT_COURSE`. Your §1 says the same: the upstream state generation remains the unknown.

So: operators are first-class in the IR. **Operator selection is the open risk, and it belongs in E1.**

## 3. `about`: field or many-to-many edge?

**Field. Single-valued: `problem_id`.**

Justification is checkability, not ontology. With a field, "every object accounted for exactly once" is a total function and the checker is trivial. With a many-to-many edge, an object can be rendered under two problems or under none, and the coverage check becomes "count the edges and hope". We already lived that: the memory referral rendered under both blocks in one run.

If a genuine cross-problem object appears — a sodium value that is evidence for a seizure and a constraint for a hyponatremia problem — the right move is two objects with the same source span, not one object with two homes. Duplication of a span is cheap and auditable; ambiguity of ownership is not.

## 4. Structured basis instead of free text?

Yes. Replace `basis: "free text"` with:

```text
basis_type   CONTAINMENT | EXPLICIT_STATEMENT | ADJUDICATED
basis_span   source span id(s)  — required for CONTAINMENT and EXPLICIT_STATEMENT
basis_by     agent/user id + date — required for ADJUDICATED
```

`CONTAINMENT` means one object's text contains the other's, mechanically checkable. `EXPLICIT_STATEMENT` means a source sentence states the relation, and the span is the evidence. `ADJUDICATED` means a human or a reviewed agent decided it, and names who.

That converts the edge from "the model says so" into "the model cites where". It also makes the four-edge set testable: for every `SAME_AS`, either containment holds or there is an adjudication.

## 5. Span/disposition coverage instead of object-per-sentence?

Agreed, and it is stronger than what I wrote.

```text
span S12  | DISPOSITION=OBJECT O44
span S13  | DISPOSITION=MERGED_INTO O17
span S14  | DISPOSITION=NOT_CLINICAL      (small talk, consent chatter)
span S15  | DISPOSITION=NOT_USED_BY_THIS_NOTE   (reason given)
```

Coverage means every span has exactly one disposition. It does not require every sentence to become an object, and it still catches the failure we care about — a fact silently vanishing — because a vanished fact leaves a span with no disposition.

## 6. Is `adopted` needed for PLAN?

Yes. A prior recommendation adopted by the current clinician is current; the same recommendation unadopted is historical. The flag is identical in meaning to its use on REASONING, and the alternative — inferring adoption from the drug or the action — is the inference we banned.

`status` alone is not enough, because a prior plan item can be *current* in the sense of "still in force" without being stated this encounter: that is exactly `adopted=true, status=HISTORICAL_SOURCE`. The two fields are orthogonal, and one of them is about the source, the other about the clinician.

## 7. Minimal IR to reproduce the stress-suite success on the seizure case

```text
META     case id, source span table
PROBLEM  id, label, claim_unit
OBJECT   id, kind, text, provenance, status, adopted, problem_id
UNIT     id, problem, class (FACT|REASONING|PLAN), operator, head, members[{id, role}], order, bucket
```

With a closed operator vocabulary — the render vocabulary the stress suite already exercised — and fail-closed behaviour on any unit that does not typecheck.

No separate state/plan split, no relations beyond what units encode (`same_as` becomes `members[{role:COVER}]`, `modifies` becomes `members[{role:MODIFIER}]`, `conditions` becomes `PLAN` with a `CONDITION` member). That is the collapse your §5 implies, and I accept it: **the unit is the relation.**

## 8. What evidence would justify omitting units/operators?

If a renderer given only objects and a problem field produced byte-identical structure across three Instant runs — i.e., if the grouping instability we measured disappeared without units. We have the opposite: three runs, three fact sets, and the stress suite's stability appears exactly when the decisions are explicit.

I would need that negative result to reconsider, not an argument about simplicity.

## 9. Should E1 compare operator selection as well as objects/edges?

Yes, and it should be the primary metric. Object agreement can be high while unit agreement is low — that is precisely our failure: the infarct object was found every time, and rendered as one bullet, two bullets, or merged with the encephalomalacia.

E1 becomes:

- E1a: object set agreement across two independent builds (target ≥0.95);
- E1b: unit set agreement — problem, class, operator, head, member roles, order (target ≥0.95);
- E1c: span disposition agreement.

E1b is the one that predicts whether the note is reproducible. E1a is necessary and not sufficient.

## 10. Which consensus candidates do I reject?

None outright. Two need rewording so they do not overclaim:

- **#3** — "explicit typed render operators with fail-closed behavior" is accepted, but state its scope: the stress suite proves *execution*, not *selection*. As written it could be read as evidence that the upstream planner is reliable, and it is not.
- **#8** — "do not use exact error-label agreement as the primary production invariant" is right, and it should extend to the checker: our own stress run showed label overlap. The invariant is *valid/invalid classification*, not the label text.

Everything else in your list 1–9 I accept as consensus, including single-call topology and section-scoped voice.

## What I still hold

- **Five kinds.** It is a simplification, not a proven optimum, and I will not defend it as more than that. `COURSE` is the one I would drop first if E1 shows it is unstable as a kind.
- **Four edges.** After the collapse in §7 they are not edges at all; they are member roles on units. If that framing wins, my four-edge claim is superseded by your unit model and I will not restate it.
- **The ledger must be recomputed.** Unchanged, and now cheaper: the checker recomputes units from objects and compares to the units the planner emitted.
