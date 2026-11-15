# MODULE 05 — WRITE A/P

## WHAT THIS IS

Formatting, not writing.

The Handoff is final. Every word in your output comes from it, or from one of the ten surface transformations in this file. You choose what to include, what order it goes in, and which words to delete. You do not add clinical content.

`AP_ANCHOR.md` is the shape. Read it and match it. Do not describe it or restate it.

---

## INPUT

Problem blocks, in order, each with `PRIMARY_CLAIM` or `PROBLEM_LABEL`, plus `CLAIM_QUALIFIER`, `ETIOLOGY`, `EVIDENCE`, `COURSE`, `MANAGEMENT`.

The Handoff is the entire clinical input. Do not return to the sources.

The Handoff is also the whole population. An object the ledger discarded is not in it, is not available to you, and its absence is not a reason to keep, drop, rename or explain anything. Select only among the entries you were given.

---

## THE LINE

One per problem, comma-joined, terminal period, starting at `//`.

```text
//<PRIMARY_CLAIM or PROBLEM_LABEL>, <status from COURSE if present>.
```

- Copy `PRIMARY_CLAIM` as recorded, and carry its own cause if it states one. **Nothing is imported into the line** — not from `EVIDENCE`, not from `ETIOLOGY`. No laterality, severity or subtype that lives only in another field.
- **Capitalise the first word after `//`.**
- **Line contraction.** You may drop a trailing qualifier from the claim when you render that qualifier as a bullet under the same problem. The dropped words must appear in that bullet. No other word-level deletion from a claim.
- A block with `PROBLEM_LABEL` and no `PRIMARY_CLAIM` uses the label for the line, without its provenance. A historical diagnosis in that block is attributed evidence, not part of the line, unless the current clinician adopted it.
- The status is one short phrase from `COURSE` status — `improved`, `resolved`, `unchanged`, `returned to baseline` — and only when `COURSE` says it. If the block has no status entry, the line ends at the claim. Never fill that slot with management, a duration, or a restatement of the finding.
- A prior-record fact (`[D, name, date]`) is rendered with its attribution in parentheses — `probable vascular dementia (prior neurology, 2025-06)` — using only the name and date the marker supplies. A current-encounter marker (`[A]`, `[B]`, `[C]`) is omitted from prose.

---

## COURSE: WHAT IT DOES, NOT WHAT IT IS

A retained `COURSE` entry is exactly one of four things. Ask first whether it bears on this problem at all — does it change the claim, add to its evidence, describe its course, or change its management? If none, it is **IRRELEVANT** and does not render.

If it does bear, classify it:

| Class | What it looks like | What you do |
|---|---|---|
| **STATUS** | the patient's or problem's condition as a whole: `returned to baseline`, `improved`, `resolved`, `unchanged`, `worse` | may supply the line status; at most one |
| **MODIFIER** | names the same event or finding as a retained `EVIDENCE` entry and adds duration, tempo, quantity, evolution or trend | fold into that bullet |
| **INDEPENDENT COURSE FACT** | bears on the problem, but attaching it to one bullet would take an inference the Handoff does not make | its own factual bullet, in the facts block |
| **IRRELEVANT** | names nothing that bears on this problem | omit |

- A status may be subject-bearing — `aphasia improved` is a status if it answers *what is her condition now*. Do not use "has no subject" as the test.
- **Rule of doubt.** Between MODIFIER and INDEPENDENT, choose INDEPENDENT. A visible extra bullet is correctable; a silently dropped fact is not.
- Fold only when the modifier's own words name the same event or finding. Never fold on adjacency, on a shared source letter, or on clinical plausibility.

```text
E  witnessed generalized tonic-clonic seizure at home
C  witnessed generalized tonic-clonic seizure about two minutes
→  Witnessed generalized tonic-clonic seizure at home, about two minutes.

E  sodium 128 on admission
C  sodium now 131 after fluid restriction
→  Sodium 128 on admission, now 131 after fluid restriction.

C  daughter: memory has been getting worse for a year      (no matching evidence entry)
→  Daughter reports memory has been getting worse for a year.
```

---

## THE BULLETS

Two groups, in this order and no other.

### 1. Facts

`EVIDENCE` entries in Handoff order, each with its folded `MODIFIER`; then `INDEPENDENT COURSE FACTS` in Handoff order.

- **Evidence eligibility.** A bullet survives only if it materially supports, refutes, discriminates or qualifies the problem line. Context, unrelated normals, preferences, and facts the line already carries are dropped.
- **One fact, one bullet.** Where two entries state the same fact, render it once, using the entry that best represents the encounter.
- Never restate the line.
- Never put a management action in a bullet — a study ordered, a drug given, a procedure performed.
- Never assert a modality the Handoff does not name.

### 2. Reasoning

`CLAIM_QUALIFIER`, then a rendered `ETIOLOGY`, in Handoff order. Reasoning always follows the facts and always precedes `Plan:`.

- A `CLAIM_QUALIFIER` becomes a reasoning bullet: an excluded alternative, an additional formulation, a stated clarification. Do not delete it; do not rewrite it as a second problem line.
- **No duplicated reasoning, no lost reasoning.** Every distinct proposition survives once. Never merge distinct propositions to shorten the output.
- Use the Handoff's words. Do not import an interpretation the clinician did not state.

---

## ETIOLOGY

**An etiology belongs to the problem it explains, not to the noun it mentions.** `etiology of the seizure is likely the chronic infarct` sits under the seizure problem. Under the stroke problem sits the stroke's own etiology, if the encounter states one.

1. **Suppressed** — only when it adds nothing beyond what the line already says. Repeating the bare cause is what is forbidden.
2. **Reasoning bullet** — whenever it adds degree of certainty, mechanism, a date, a rationale, a contrast, or an uncertainty. It renders last among the bullets, under the same problem.

Never on the line. Never synthesised from evidence.

---

## SURFACE TRANSFORMATIONS

These ten are the only changes you may make to the words. Anything else is added content.

1. Capitalisation and terminal punctuation.
2. Folding a verified `MODIFIER` into its fact, removing only the repeated subject.
3. Suppressing a whole duplicate entry — never deleting words from inside a clinically meaningful phrase.
4. Rendering a speaker prefix as bounded attribution: `daughter: X` → `Daughter reports X`; `patient: X` → `Patient reports X`. A `clinician:` prefix is dropped, because the note is the clinician's voice.
5. Rendering a provenance marker as a parenthetical using its name and date only: `(prior neurology, 2025-06)`.
6. Date display: `2025-06` → `June 2025`.
7. Combining compatible fragments already present — a held drug with its resume condition, one action stated twice — without adding a clinical word.
8. Number and unit display: written number → numeral; `minutes`/`hours` → `mins`/`hrs`; `about`/`approximately` → `~`.
9. **Line contraction**, as defined under *The line*.
10. **Anchored relative time.** `X ago` may render as `X prior to presentation`, with the interval unchanged. Reference wording only — no date arithmetic, no absolute date inferred from provenance or from a record date.

Never substitute a pronoun. The Handoff carries no demographic entry, so a pronoun it does not contain is an addition.

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
- **One decision, one bullet.** Where two entries describe the same action, keep the one that represents the current clinician's plan. A later or longer statement is not automatically better. Never merge distinct conditions, rationales, or incompatible states.
- **A prior-record entry is not a current plan item.** It appears only when a current-encounter entry re-adopts, continues, or restates it. Never infer that an old recommendation is still in force.
- Omit `Plan:` entirely when the block has no management. Never leave it empty.

---

## CHECK BEFORE YOU RETURN

For every word of output, ask which Handoff entry or which of the ten transformations produced it. If neither, delete the line.

The only additions allowed beyond those are items in `STANDING_ITEMS.md`, and only when the item's trigger is satisfied by the block's `CLAIM`. A diagnosis in the differential is not the working diagnosis.

A bullet whose words all appear on its problem line is a restatement. Delete it.

---

## OUTPUT

- Start at the first `//`. End at the last plan bullet, or the last support bullet when there is no plan.
- No commentary, no summary, no self-check, no closing line, nothing naming a file or a stage.
- No `Plan:` when there is no plan.
- One block per problem, in the Handoff's order. Never merge, split, or reorder.
