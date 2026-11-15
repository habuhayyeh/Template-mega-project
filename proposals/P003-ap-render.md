# P003 v8 — `05_WRITE_AP`: COURSE by function, one render order, one etiology rule, reproducible acceptance

**Status:** v8, revised after `reviews/P003-v7-original-branch.md`. One mechanical fix: I10 now admits the split pattern that transformation 9 creates. Architecture accepted; awaiting implementation approval.
**Supersedes:** P003 v1 in this file's history.
**Affects:** `pipeline/05_WRITE_AP.md`, `pipeline/AP_ANCHOR.md`, `tests/acceptance/`, `runs/`, `CHANGELOG.md`, `DECISIONS.md` (one new entry after approval).
**Does not affect:** substrate, `01`, `02`, `03` semantics, `04`, `06`, `07`, the six kinds, either oracle.

---

## 1. What P002 exposed

1. **Unstable selection.** Two runs of `05` on one Handoff produced different regressions. Run 2 re-added O54, unmerged the apixaban hold from its resume condition, dropped `Seizure precautions`, and dropped the infarct and encephalomalacia evidence.
2. **COURSE payload never renders.** O4 `about two minutes`, O6 `lasting an hour`, O15 `now 131 after fluid restriction` are in the Handoff and absent from the A/P. `05` reads only `CLAIM_QUALIFIER` and `EVIDENCE` for bullets and uses `COURSE` only for line status.
3. **Internal contradictions.** `05` says bullets come from `CLAIM_QUALIFIER` then `EVIDENCE`, and also that reasoning renders last; it says `ETIOLOGY` may join the line and also that it survives as a reasoning bullet; and it says "formatting, not writing" while requiring attribution and normalisation decisions.

v1 of this proposal tried to solve 2 with a lexical subject test. It fails O14/O15 (`128` is not in `now 131`), O7/O8 (`known` appears only in the evidence entry) and O36 (no shared subject), so it would have dropped exactly the payload it was written to rescue. That heuristic is withdrawn.

---

## 2. COURSE by function

Each retained `COURSE` entry is classified by what it does for the problem, not by its grammar.

| Class | Definition | Rendering |
|---|---|---|
| **STATUS** | Describes the patient's or the problem's condition as a whole: `returned to baseline`, `improved`, `resolved`, `unchanged`, `worse`. Carries no duration, quantity, or trend. May be subject-bearing (`aphasia improved`). | May supply the line status. At most one. |
| **MODIFIER** | Names the same event or finding as a retained factual bullet and adds duration, tempo, quantity, evolution, or trend. | Folded into that bullet: the fact, then the added words. |
| **INDEPENDENT COURSE FACT** | Bears materially on the problem, but attaching it to one factual bullet would require an inference the Handoff does not make. | Its own factual bullet, in the facts block. |
| **IRRELEVANT** | Names nothing that bears on the claim. | Omitted. |

**Relevance gate first.** Before classification, ask whether the entry bears on this problem at all: does it change the claim, add to its evidence, change its course, or change its management? If it does none of these, it is IRRELEVANT and is not rendered. Only entries that pass the gate are classified as STATUS, MODIFIER, or INDEPENDENT.

**Do not use "has no subject" as the test for STATUS.** A status may be subject-bearing; what distinguishes it is that it answers *what is her condition now*, not *how long did the event last*.

**Rule of doubt, after the gate.** Between MODIFIER and INDEPENDENT, choose INDEPENDENT. An entry that passes the gate but cannot be folded renders as its own factual bullet. A visible extra bullet is correctable; a silently dropped relevant fact is not.

**Folding is permitted only when the relationship is clear from the Handoff** — the modifier's own words name the same event or finding as the bullet. No anchor is inferred from adjacency, from a shared source letter, or from clinical plausibility.

### Worked classification, frozen acceptance case

| Entries | Class | Rendering |
|---|---|---|
| O3 + O4 | MODIFIER | `Witnessed generalized tonic-clonic seizure at home, about two minutes.` |
| O5 + O6 | MODIFIER | `Postictal confusion lasting about an hour.` |
| O7 + O8 | MODIFIER | `Known left MCA infarct, two years ago.` |
| O14 + O15 | MODIFIER (trend) | `Sodium 128 on admission, now 131 after fluid restriction.` |
| O36 | INDEPENDENT | `Daughter reports memory has been getting worse for a year.` |
| O2 `admitted 11/12` | IRRELEVANT — fails the gate | It changes neither the seizure claim, its course, nor its management. |

Where a fold is rejected, the course entry renders on its own rather than disappearing. That is the whole difference from v1.

---

## 3. One render order

Per problem, and no other:

1. **Facts** — `EVIDENCE` entries with their folded modifiers, then independent `COURSE` facts, each block in Handoff order.
2. **Reasoning** — `CLAIM_QUALIFIER`, then a rendered `ETIOLOGY`, in Handoff order. Distinct propositions stay distinct.
3. **`Plan:`** — the buckets, unchanged.

The sentence "From `CLAIM_QUALIFIER`, then `EVIDENCE`" is deleted.

---

## 4. One etiology rule, and the anchor change it requires

**An etiology belongs to the problem it explains, not to the noun it mentions.** `Etiology of the seizure is likely the chronic infarct` sits under the seizure problem; `etiology of the infarct was unanticoagulated AF` would sit under the infarct problem. Routing on the predicate, not the subject, is already what the ledger does — O35 is on P1 — so this rule constrains rendering only.

**Both places are allowed, with different jobs:**

1. **The line** carries the claim's own short cause, as the claim states it. Nothing is imported into the line, and no reasoning is synthesised from evidence.
2. **The bullet** renders the etiology as reasoning, under the same problem, whenever it adds something the line does not say: degree of certainty, mechanism, a date, a rationale, a contrast, or an uncertainty.
3. **Suppressed** only when the etiology adds nothing at all — when the line already carries its full content. Duplication of the bare cause alone is what is forbidden, not the coexistence of a short cause and a fuller reason.

The judgment in branch 3 is narrow. D-004 protects the clinician’s reasoning, so a redundant etiology is cheaper than a deleted one. The guard is I4 — if one run renders an etiology and another suppresses it, the run set fails acceptance.

**Signer decision, 2026-11-14:** for the frozen case the etiology renders. The line keeps the short cause; the bullet carries the reason. Verbatim in `channel/to-chatgpt.md`, entry of 2026-11-14T21:35. No longer pending.

`pipeline/AP_ANCHOR.md` currently says a separate `ETIOLOGY` contributes to the line. Under this rule it does not: the line's cause comes from the claim, and the etiology is reasoning. Proposed edit:

- Settled-table row `| Cause — both sources | … both contribute to the line |` becomes
  `| Cause | the line carries the cause stated in CLAIM; a separate ETIOLOGY renders as the final reasoning bullet when it adds anything the line does not say |`.
- The section `## Cause: both contribute` is replaced by:

```text
## Cause

The line carries the cause the claim itself states, shortened if the claim allows it. A separate
ETIOLOGY entry renders as the final reasoning bullet — the mechanism, the date, the certainty, the
rationale — whenever it adds something the line does not say. It is suppressed only when it adds
nothing, that is, when it repeats the bare cause.

An etiology belongs to the problem it explains, not to the noun it mentions.
```

Frozen case: claim `post-stroke seizure from the old left MCA scar rather than a new lesion`; etiology `scar from your old stroke is the most likely cause of the seizure`. Under this rule the bullet renders, because `most likely cause` is an explicit certainty statement the line does not carry in those words. The line keeps the short cause.

---

## 5. Surface rendering versus clinical content

"Formatting, not writing" stays. The permitted list is now bounded and mechanical.

### Permitted

1. Capitalisation and terminal punctuation.
2. Folding a verified MODIFIER into its fact, removing only the repeated subject.
3. Suppressing a whole duplicate entry — never deleting words from inside a clinically meaningful phrase.
4. Rendering a structural speaker prefix as bounded attribution: `daughter: X` → `Daughter reports X`; `patient: X` → `Patient reports X`. A `clinician:` prefix is dropped, because the note is the clinician’s voice. A third party’s statement is never rendered as unattributed fact.
5. Rendering a provenance marker as a parenthetical using its name and date only: `(prior neurology, 2025-06)`.
6. Date display normalisation: `2025-06` → `June 2025`.
7. Combining compatible fragments already present — a held drug with its resume condition, one action stated twice — without adding a clinical word.
8. Unit and number display, and only this: a written number → numeral; `minutes`/`hours` → `mins`/`hrs`; `about`/`approximately` → `~`. No other synonym or abbreviation substitution.
9. **Line contraction.** The problem line may drop a trailing qualifier when that qualifier is rendered as a bullet in the same problem. The dropped words must appear in that bullet. No other word-level deletion from a claim is permitted. **Approved by the signer in the example of 2026-11-14**, where the line reads `from chronic L MCA infarct` and the comparator lives in the etiology bullet.
Transformation 10 of v6 is withdrawn. It rendered a provenance year as an event year — arithmetic on a record date, not a fact in the object. The infarct’s date reaches the note only as attribution, `(prior neurology, 2024-02)`, under transformation 5.

### Prohibited

No new noun, verb, number, quantity, negation, modality, causal connective, or inference. No etiology that is not an `ETIOLOGY` entry. No status that is not a `COURSE` entry. No plan item that is not a `MANAGEMENT` entry or a `STANDING_ITEMS` trigger. **No pronoun substitution**: the Handoff carries no demographic entry, so a pronoun it does not contain would be an addition.

**Test:** every word of the output is in the Handoff, produced by transformations 1–9, or an entry from `STANDING_ITEMS.md` whose trigger the claim satisfies. Anything else is a defect.

---

## 6. Reproducibility acceptance

### Protocol

1. Fixed input: one Handoff from `substrate/acceptance_v2.txt` + `oracles/ap_ledger_v3.txt`, recorded once and reused byte-identically.
2. Three independent runs of `05`, fresh context, same contract. No hand editing between runs.
3. Each run scored by a reader holding the Handoff, with a line-level trace table:

   ```text
   output line | source (O# set, or STANDING_ITEM + trigger) | transformation(s) | omitted retained O# + reason

   When transformation 9 is used, the `PRIMARY_CLAIM` `O#` is recorded on both the line and the reasoning bullet that carries the moved qualifier. That is the only permitted two-line trace for one `O#`.
   ```

   Every bullet maps to at least one `O#`. A bullet that maps to nothing fails I8.

### Invariants — identical across all three runs

| # | Invariant |
|---|---|
| I1 | problem count and order |
| I2 | set of `O#` rendered as facts |
| I3 | set of retained `O#` deliberately not rendered |
| I4 | number and content of distinct reasoning propositions |
| I5 | set of plan decisions |
| I6 | state and conditionality of each plan decision |
| I7 | historical attributions present |
| I8 | zero words outside the Handoff, transformations 1–9, and a `STANDING_ITEMS` entry whose trigger the claim satisfies |
| I9 | the same `O#` pairing — entries merged in one run are merged in all |
| I10 | the same placement pattern for every `O#` across runs. An `O#` normally has one class — line, factual bullet, reasoning bullet, or plan. A `PRIMARY_CLAIM` may use the split pattern `line + reasoning bullet` only under transformation 9, and the moved qualifier must be traceable to that same `O#` in every run |

### Pass

All ten invariants identical across three runs. Wording may vary only within transformations 1–9; if it does, the set is recorded as textually unstable and semantically stable, and that variance is reported, not hidden.

A single run is never the acceptance artifact. The artifact is the three-run set plus the invariant table.

---

## 7. Acceptance target

Present after P003: witnessed seizure with `~2 mins`; postictal confusion with `~1 hr`; no prior seizures; known left MCA infarct, recorded 2024-02 (prior neurology), and encephalomalacia; CT without hemorrhage or new lesion; sodium 128 → 131 after fluid restriction; distinct reasoning (postictal, not dementia; MRI adjudicates); MRI and EEG; apixaban held with resume condition; no antiseizure medication unless another event; driving restriction; amlodipine, atorvastatin, fluid restriction, seizure precautions; probable vascular dementia attributed to prior neurology 2025-06; daughter-reported memory decline over a year.

Absent: O54 as a seizure bullet; duplicate seizure, sodium, or CT statements; duplicate reasoning; O52 promoted into today's plan; invented linkage, etiology, or status.

---

## 8. Housekeeping

Corruption repaired in this commit: `DECISIONS.md` D-014 cell; `runs/2026-11-14-p002/validation.txt` three `0x07` bytes, stray newline, missing `r`; `STATUS.md` regenerated — the damaged fence, the `uns/` path, the stale O54-pending line and the "mock validated" contradiction are gone.

After implementation: `CHANGELOG.md` entry, and a decision recording the COURSE classes and the two-branch etiology rule. **Do not reserve an ID here** — D-015 is the signer-approved chronic-block rule. Take the next free `D-###` at the moment of recording.

---

## 9. Validation plan

```text
1. tools/allocate.py substrate/acceptance_v2.txt                    → runs/<date>-p003/allocation.txt
2. tools/check_ledger.py allocation.txt oracles/ap_ledger_v3.txt    → exit 0
3. 04 on substrate + ledger                                         → handoff.txt  (must equal P002's)
4. 05 ×3 on that Handoff                                            → ap_run1..3.txt
5. line-level trace table + ten invariants                          → validation.txt
6. STATUS update after the invariant table
```

Local execution by an LLM. Engineering mock; says nothing about Doximity.

---

## 10. Risks

- **Folding duplicates text.** Mitigated by I3 and I9: a folded modifier may not appear again, and pairing must be stable.
- **INDEPENDENT becomes a dumping ground.** Mitigated by I3 and I8: each independent bullet must map to its own `O#` and use only its words.
- **Three runs disagree.** That is the finding, not a protocol failure; no fourth run rescues it.
- **The anchor change is a format change.** It touches the signer's document. Approved by proposal, not by edit.

---

## Out of scope

`01`, `02`, `04`, `06`, `07`, the substrate, the six kinds, the oracles, O54, the body note, and any new tool.
