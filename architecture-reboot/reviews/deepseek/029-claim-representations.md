# DeepSeek response 029 — refined D, claim representations

All four accepted. One has a data-model consequence that should be recorded while it is cheap.

---

## 1. S3 must not prefer the current assertion — accepted

My rule would have been wrong in the most clinically common case. A note reading "seizure versus syncope, EEG pending" has two candidates; preferring the current assertion collapses a differential that the clinician deliberately left open. The same applies to nested formulations ("post-stroke epilepsy, left MCA territory") and to explicit uncertainty ("probable", "cannot exclude").

To be precise about what my rule would have done: it would have suppressed exactly the content that distinguishes a neurologist's assessment from a summary. Triage-style notes collapse differentials; consultant-style notes preserve them. The signer's notes are the second kind.

## 2. S2 owns the relations and produces approved representations — accepted

S2 classifies the relation among candidate claims: `EQUIVALENT`, `NESTED`, `COMPLEMENTARY`, `COMPETING`, `CONTRADICTORY`, `UNRESOLVED`. It then emits one or more **approved representations**, and S3 selects only among those.

**The data-model consequence:** a claim is not an object id. It is a *representation* with a kind:

```text
REPRESENTATION R1
  kind: SINGLE        | NESTED | DIFFERENTIAL | UNRESOLVED
  members: [O31]                        # SINGLE / UNRESOLVED
  head: O31, qualifier: O33             # NESTED
  alternatives: [O31, O37]              # DIFFERENTIAL
  relation: COMPETING
  rationale: "clinician left both open pending EEG"
```

Without this, the IR would force every claim to a single object and either drop the differential or smuggle it into prose — which is precisely the flattening we started this rebuild to remove.

S3 then selects a representation, not a claim, and may not:
- synthesise a representation from ungrouped candidates;
- promote an `UNRESOLVED` relation to `SINGLE`;
- merge two representations.

## 3. Unresolved candidates stay S2's problem — accepted

This removes the fail-closed tie rule I proposed, and that is an improvement. An unresolved relation is not an S3 deadlock; it is a legitimate output (`DIFFERENTIAL` or `UNRESOLVED`), because the note may honestly say the question is open.

Fail-closed still applies where it belongs: if S2 cannot even classify the relation, no approved representation exists, and the problem renders without a claim — which the completeness predicate catches.

## 4. Salience schema downstream — accepted

S1 supplies inspectable features; S4 applies the ordering contract; the exact fields are downstream. The only commitment I would keep is that features are declared values rather than adjectives, since "severe" is not an order input a second reader can reproduce.

---

## 5. Consequence for the design change record

The S1/S2 `DESIGN CHANGE` now has three parts, not one:

1. S1 no longer emits current claims;
2. S2 emits approved claim **representations**, with relations;
3. S3 selects a representation and cannot construct one.

Part 2 is the part that will be easy to lose in implementation, because a single-claim shortcut will look like a simplification and will work for most cases. It is worth an explicit assertion: a case with a documented differential must render a differential representation, not a single claim.

## 6. What this does and does not close

**Closes:** the interface-design portion of Review 4 — S1, S2, S3, S4 boundaries are now defensible, acyclic, and each has one question.

**Does not close:** the architecture experiments, all still unrun:
- AX-2 seam leakage, corrected form;
- AX-T test-mode observer effect;
- AX-SCALE IR and accounting at realistic case size;
- AX-I3 proposition-boundary stability;
- and the rebuilt K2 with explicit linkage, which is now a claim for whether S4's ordering and S3's selection hold under a continued problem.

**Still missing from the architecture, not fixed by this boundary:** the rule for when a problem may exist at all. K4 showed symptom and question problems are valid, so "requires management or a diagnosis" is too strict; but nothing yet says what makes a candidate problem real rather than a passing mention. That is the next question I would put to the architecture, after the experiments rather than before.

Recorded as a `DESIGN CHANGE`, not a clarification.
