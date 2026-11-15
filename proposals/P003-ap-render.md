# P003 — `05_WRITE_AP`: COURSE by function, one render order, one etiology rule, reproducible acceptance

**Status:** draft, awaiting review. Not implemented.
**Supersedes:** nothing. Extends P002.
**Affects:** `pipeline/05_WRITE_AP.md`, `tests/acceptance/`, `runs/`, `STATUS.md`, `CHANGELOG.md`.
**Does not affect:** substrate, `01`, `02`, `03` semantics, `04`, `06`, `07`, the six kinds, the A/P oracle, the section oracle.

---

## 1. What P002 exposed

Three separate defects, from the same frozen Handoff:

1. **Unstable selection.** Two runs of `05` produced different regressions. Run 2 re-added O54 as a bullet, unmerged the apixaban hold from its resume condition, dropped `Seizure precautions`, and dropped the infarct and encephalomalacia evidence — the entries that establish the substrate the claim names.
2. **COURSE payload never renders.** The Handoff carries durations and a trend that the A/P does not: O4 `about two minutes`, O6 `lasting an hour`, O15 `now 131 after fluid restriction`. `05` reads only `CLAIM_QUALIFIER` and `EVIDENCE` for bullets and uses `COURSE` only for line status. The anchor's own first bullet carries `~90 seconds` and `~20 minutes`, so this is not optional detail.
3. **Internal contradictions.** `05` says bullets come "from `CLAIM_QUALIFIER`, then `EVIDENCE`" and also that reasoning renders last; it says `ETIOLOGY` may join the line and also that it survives as a reasoning bullet; and it says "formatting, not writing" while requiring attribution and normalisation decisions.

The instability is not separable from 3. A stage that is told two different orders will produce different orders.

---

## 2. COURSE by function

`COURSE` is not one thing. `05` classifies each retained `COURSE` entry by what it does to a retained fact, using only the Handoff.

### 2.1 Link test

Normalise both texts: lowercase, strip punctuation, collapse whitespace. For a `COURSE` entry C and an `EVIDENCE` entry E in the same problem:

1. **Shared subject.** If E's subject phrase — its leading content words up to the first verb or preposition — appears in C, then C carries the same subject and step 2 applies. Otherwise step 3.
2. **Modifier.** If C adds timing, quantity, or trend material to that subject — a duration, an interval, a change verb, a delta — C is a **modifier** of E. Render one bullet: E's text, then the added material from C with the repeated subject removed.

   ```text
   E  witnessed generalized tonic-clonic seizure at home
   C  witnessed generalized tonic-clonic seizure about two minutes
   →  Witnessed generalized tonic-clonic seizure at home, about two minutes.

   E  sodium 128 on admission
   C  sodium now 131 after fluid restriction
   →  Sodium 128 on admission, now 131 after fluid restriction.
   ```

3. **Status.** If C has no factual subject — a pure state phrase such as `returned to baseline`, `improved`, `resolved`, `unchanged`, `worse` — C is a **status candidate** for the problem line. At most one is used. If there is none, the line ends at the claim.
4. **Unlinked.** If C has a subject that no retained `EVIDENCE` entry shares, C is **not rendered**. No anchor is inferred, no subject is borrowed from another problem, and nothing is added to make the sentence work.

The linkage is therefore never invented: either the subject phrase is literally present in both entries, or the entry is not rendered. The test is lexical containment plus an explicit timing or change marker. A judge who reads the Handoff can check every link by eye.

### 2.2 What does not change

`01` keeps splitting event from duration (D-001 and split-before-classify stand). The merge happens at rendering, in `05`, exactly as the apixaban hold is merged with its resume condition.

### 2.3 Duplicates

One bullet per fact. If two `EVIDENCE` entries state the same fact — O3 and O43, O14 and O45, O17 and O44 — the first is rendered and the second is suppressed. If a modifier has already been folded into its evidence bullet, it is not rendered a second time.

---

## 3. One render order

Per problem, in this order and no other:

1. **Factual evidence** — `EVIDENCE` entries, each with its `COURSE` modifier folded in, in Handoff order.
2. **Clinician reasoning** — `CLAIM_QUALIFIER` entries, then `ETIOLOGY` when it renders as reasoning (§4), in Handoff order. Distinct propositions stay distinct; two reasoning propositions are two bullets.
3. **`Plan:`** — the four buckets, as today.

The sentence "From `CLAIM_QUALIFIER`, then `EVIDENCE`" is deleted. It is the direct cause of the contradiction.

A reasoning bullet is never placed above a factual one, and factual bullets are never reordered to make a narrative.

---

## 4. One ETIOLOGY rule

For a retained `ETIOLOGY` entry E and the problem's claim X:

1. **Suppressed.** If X already names the same cause — the claim contains a causal construction (`from`, `due to`, `secondary to`, `related to`, `after`) and E names that same cause — E is suppressed entirely. It appears neither on the line nor as a bullet.
2. **On the line.** If X names no cause and E is a short causal phrase (eight words or fewer), E is appended to the line before the status, and is not repeated as a bullet.
3. **As a bullet.** Otherwise E renders as the final reasoning bullet, after `CLAIM_QUALIFIER`, and does not touch the line.

Never both. When the same-cause test is genuinely uncertain, prefer branch 3: a visible bullet is correctable, an unexplained line element is not.

Worked case: X `post-stroke seizure from the old left MCA scar rather than a new lesion`; E `scar from your old stroke is the most likely cause of the seizure`. X names the cause; E names the same cause → suppressed. The current output renders both, which is the duplication this rule removes.

---

## 5. Surface rendering versus clinical content

"Formatting, not writing" stays. What changes is that the permitted transformations are enumerated, so the stage is not asked to decide what counts as formatting.

### Permitted — surface rendering only

1. Capitalise the first word after `//` and the first word of a sentence.
2. Delete redundant words: articles, repeated subjects, a repeated fact.
3. Fold a `COURSE` modifier into its evidence entry, and fold a state into its action (`apixaban held, to resume once MRI excludes hemorrhage`), when both parts are already in the Handoff.
4. Strip structural speaker prefixes — `clinician:`, `daughter:`, `patient:` — while keeping material attribution already in the text (`per family`, `daughter reports`).
5. Render a provenance marker as a parenthetical using its name and date only: `(prior neurology, 2025-06)`.
6. Normalise a date for reading: `2025-06` → `June 2025`. The marker itself is not altered upstream; this is display only.
7. Lowercase a mid-sentence proper noun only where the source already does.

Pronoun substitution is **not** permitted: the Handoff contains no demographic entry, so a pronoun the Handoff does not carry would be an addition.

### Prohibited — new clinical content

No new noun, verb, number, quantity, negation, modality, causal connective, or inference. No etiology that is not an `ETIOLOGY` entry. No status that is not a `COURSE` entry. No plan item that is not a `MANAGEMENT` entry or a `STANDING_ITEMS` trigger.

**Test:** every word in the output is either in the Handoff or produced by one of the seven transformations above. A word that is neither is a defect.

---

## 6. Reproducibility acceptance

One good run proves nothing; P002 already produced two different ones. `05` is accepted only when repeated runs on the same frozen Handoff agree on what the A/P says.

### Protocol

1. Fixed input: `substrate/acceptance_v2.txt` + `oracles/ap_ledger_v3.txt` → one Handoff, recorded once and reused byte-identically.
2. Three independent runs of `05`, fresh context each, same contract, same Handoff. No hand editing between runs.
3. Each run scored against the invariant set below by a reader who has the Handoff open.
4. A trace table per run: every rendered bullet maps to a Handoff `O#`. Any bullet that maps to nothing is a failure.

### Invariants — must be identical across all three runs

| # | Invariant |
|---|---|
| I1 | problem count and order |
| I2 | set of `O#` rendered as facts |
| I3 | set of retained `O#` deliberately not rendered |
| I4 | number and content of distinct reasoning propositions |
| I5 | set of plan decisions |
| I6 | state and conditionality of each plan decision |
| I7 | historical attributions present |
| I8 | zero words outside the Handoff and the seven transformations |

### Pass criteria

- **PASS:** I1–I8 identical in all three runs. Wording may differ only in ways the seven transformations allow; if it does, the run set is recorded as textually unstable but semantically stable.
- **FAIL:** any invariant differs, or any run contains a word that fails I8, or any bullet maps to no `O#`.

A single run is never the acceptance artifact. The artifact is the three-run set plus the invariant table; if they agree, the run set *is* the output and no reviewed rewrite is needed.

---

## 7. Acceptance target for the acceptance case

Must be present after P003:

- witnessed generalized tonic-clonic seizure, `~2 mins`;
- postictal confusion, `~1 hr`;
- no prior seizures;
- known left MCA infarct, old left MCA encephalomalacia;
- CT head without hemorrhage or new focal lesion;
- sodium 128 → 131 after fluid restriction;
- distinct clinician reasoning: confusion is postictal, not dementia; MRI will adjudicate;
- MRI and EEG;
- apixaban held, resume once MRI excludes hemorrhage;
- no antiseizure medication unless another event;
- driving restriction;
- current plan items (amlodipine, atorvastatin, fluid restriction, seizure precautions);
- probable vascular dementia attributed to prior neurology 2025-06;
- family-reported memory decline.

Must remain absent:

- O54 as a seizure bullet;
- duplicate seizure, sodium, or CT statements;
- duplicate reasoning;
- O52 `no further workup` promoted into today's plan;
- any invented linkage, etiology, or status.

---

## 8. State and housekeeping

After implementation, not before:

1. `STATUS.md` — `05` is recorded as **unstable pending P003**, not `engineering/mock validated`; the stale "signer decision pending on O54" line is removed because D-014 settles it; `Doximity acceptance: PENDING` and `Canonical acceptance: NOT YET ESTABLISHED` stay.
2. `CHANGELOG.md` — P003 entry.
3. A `D-015` recording the COURSE-by-function rule and the three-branch etiology rule once approved.

Already repaired in this commit, non-semantic:

- `DECISIONS.md` D-014 cell: `O54 esidual … aphasia\ stays out` → `O54 residual mild expressive aphasia stays out`.
- `runs/2026-11-14-p002/validation.txt`: three `0x07` bytes restored to `a` (`ap_run1.txt`, `ap_run2.txt`, `ap_reviewed.txt`), a stray newline removed, and the missing `r` restored.

---

## 9. Validation plan

```text
1. tools/allocate.py substrate/acceptance_v2.txt            → runs/<date>-p003/allocation.txt
2. tools/check_ledger.py allocation.txt oracles/ap_ledger_v3.txt   → exit 0
3. 04 on substrate + ledger                                 → runs/<date>-p003/handoff.txt  (must equal P002's)
4. 05 ×3 on that Handoff                                    → ap_run1..3.txt
5. trace table + invariant score                            → runs/<date>-p003/validation.txt
6. STATUS update after the invariant table, never before
```

Executed locally by an LLM. This is an engineering mock; it does not speak to Doximity behaviour.

---

## 10. Risks

- **COURSE folding may duplicate text.** Mitigated by the shared-subject test and by I3: a modifier that rendered inside a bullet must not appear again.
- **Etiology suppression may hide a distinct cause.** Mitigated by branch 3's bias: uncertain cases render as a bullet.
- **Three runs may not agree.** That is a finding, not a failure of the protocol. If they do not, the stage is not acceptance-ready and no fourth run rescues it.
- **The A/P now says more than it did.** Durations and the sodium delta become visible. That is a change in what the note tells a reader and is flagged for the user.

---

## Out of scope

`01`, `02`, `04`, `06`, `07`, the substrate, the six kinds, the oracles, O54's status, the body note, and any new tool.
