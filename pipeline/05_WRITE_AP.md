# MODULE 05 — WRITE A/P

## WHAT THIS IS

Formatting, not writing.

The Handoff is final. Every word in your output comes from it. You choose what to include, what order it goes in, and which words to delete. You do not add a word.

`AP_ANCHOR.md` is the shape. Read it and match it. Do not describe it or restate it.

---

## INPUT

Problem blocks, in order, each with `PRIMARY_CLAIM` or `PROBLEM_LABEL`, plus `CLAIM_QUALIFIER`, `ETIOLOGY`, `EVIDENCE`, `COURSE`, `MANAGEMENT`.

The Handoff is the entire clinical input. Do not return to the sources.

---

## THE LINE

One per problem, comma-joined, terminal period, starting at `//`.

```text
//<PRIMARY_CLAIM or PROBLEM_LABEL>, <ETIOLOGY if present>, <status from COURSE if present>.
```

- Copy `PRIMARY_CLAIM` as recorded. Add nothing to it — no laterality, severity, or subtype that lives only in `EVIDENCE`.
- A block with `PROBLEM_LABEL` and no `PRIMARY_CLAIM` uses the label for the line, verbatim, **without** its provenance. The label is a symptom-level proposition, not a current formulation. A historical diagnosis in that block is attributed evidence, not part of the line, unless the current clinician explicitly adopted it.
- Append `ETIOLOGY` only when it adds a cause the claim does not already state. Do not repeat a cause.
- The status is one short phrase from `COURSE`: `improved`, `resolved`, `unchanged`, `returned to baseline` — but only if `COURSE` says it. The status is the patient's condition. If `COURSE` holds a description, a duration, or a study's state, the line ends without a status. Never fill that slot with management (`pending MRI`), with a duration, or with a restatement of the finding. If the record states the condition as its own sentence, that sentence stays a bullet and the line ends at the cause.
- A prior-record fact (`[D, name, date]`) is rendered with its attribution in parentheses — `probable vascular dementia (prior neurology, 2025-06)` — using only the name and date the marker supplies. Do not invent, rename, normalize, or reinterpret them. A current-encounter marker (`[A]`, `[B]`, `[C]`) is omitted from prose.

---

## THE BULLETS

From `CLAIM_QUALIFIER`, then `EVIDENCE`, in the order the Handoff gives. Same `-` form, no heading.

- A `CLAIM_QUALIFIER` entry becomes a reasoning or interpretation bullet beneath the line: an excluded alternative, an additional formulation, a stated clarification. Do not delete it, and do not rewrite it as a second problem line.
- **Evidence eligibility.** A bullet from `EVIDENCE` survives only if it materially supports, refutes, discriminates, or qualifies the problem line. Context, unrelated normals, preferences, and facts the line already carries are dropped.
- **Reasoning renders last**, after the decisive factual evidence and before `Plan:`, in the clinician's own words. `ETIOLOGY` and `CLAIM_QUALIFIER` survive even when they partially restate evidence.
- **Strip structural speaker prefixes** — `clinician:`, `daughter:`, `patient:` — from prose. Keep the attribution itself where it is clinically material (`per family`, `daughter reports`).
- Delete words. Do not add, substitute, or reorder them.
- Never restate the line. The claim appears once, on the line.
- Never put a management action in a bullet — a study ordered, a drug given, a procedure performed. It belongs in the plan.
- Never assert a modality the Handoff does not name. `Small infarct` does not establish `imaging showed`.
- A reasoning bullet — `favored over`, a stated basis — is allowed only when the Handoff states one, and goes last. Use the Handoff's words, not your own.

---

## THE PLAN

From `MANAGEMENT`. Four buckets, this order, Handoff order inside each:

**A change in level of care goes first, above the buckets** — admission, ICU, transfer, discharge.

1. investigations — ordered, requested, pending, or explicitly not indicated
2. medications — started, continued, held, stopped, or explicitly not indicated
3. everything else — protocols, precautions, referrals, counseling
4. follow-up — an appointment, an interval, a return precaution

- Bare phrases, as on a plan list.
- Every state word survives: `ordered`, `pending`, `held`, `not started`, `unless`, `once`, `recommended`, `declined`.
- `Not starting` stays `not starting`. It does not become `not indicated`, and `not indicated` does not become `not ordered`.
- A conditional stays conditional.
- A patient preference stays attributed to the patient.
- Omit `Plan:` entirely when the block has no management. Never leave it empty.

---

## CHECK BEFORE YOU RETURN

For each line of output, find its words in the Handoff. If a line contains a word the Handoff does not contain, delete the line. That includes a precaution, a counseling line, a follow-up that sounds standard for the diagnosis.

The only additions allowed are the items in `STANDING_ITEMS.md`, and only when that item's trigger is satisfied by the block's `CLAIM`. A diagnosis in the differential is not the working diagnosis. Nothing else may be added, however standard it is.

If you cannot point to the Handoff entry a bullet or plan item came from, delete it.

A bullet whose words all appear on its problem line is a restatement. Delete it — `progressive memory difficulty` under a line that already opens with those words is the claim said twice.

---

## OUTPUT

- Start at the first `//`. End at the last plan bullet, or the last support bullet when there is no plan.
- No commentary, no summary, no self-check, no closing line, nothing naming a file or a stage.
- No `Plan:` when there is no plan.
- One block per problem, in the Handoff's order. Never merge, split, or reorder.
