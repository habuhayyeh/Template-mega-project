# P003 review — original architecture branch

**Reviewer:** ChatGPT (original architecture branch)  
**Proposal:** `proposals/P003-ap-render.md`  
**Verdict:** **REVISE — narrow architectural corrections, no implementation yet**

P003 is directionally correct: COURSE must survive by function, reasoning must have one render order, `04` stays lossless, and repeated-run acceptance is the right response to P002's instability. The proposal is not ready to implement because the current COURSE linker fails the frozen acceptance case and the ETIOLOGY rule conflicts with the current descriptor boundary and the signer's stated preferred style.

## Accepted as direction

- COURSE is not blanket-rendered.
- Fact-bearing COURSE should be able to modify factual content instead of disappearing.
- Patient-condition status may contribute to the problem line.
- Factual evidence precedes explicit clinician reasoning.
- Distinct reasoning propositions remain distinct.
- `05` retains the strict no-invention boundary.
- Three independent runs is an appropriate mock-stability bar.
- A per-run trace artifact is appropriate; no new checker is required yet if the trace is complete and auditable.
- O54 remains out of the A/P.
- P003 stays scoped to rendering; do not reopen `01`, `02`, `04`, `06`, or `07`.

## Blocking issue 1 — the shared-subject lexical test fails the acceptance case

The proposed rule says an EVIDENCE subject phrase must literally appear in COURSE.

That fails at least these retained objects:

1. **O14/O15**
   - E: `sodium 128 on admission`
   - C: `sodium now 131 after fluid restriction`
   - The proposed E subject phrase includes the value `128`; it is not literally present in C.
   - Yet P003's own acceptance target requires `sodium 128 -> 131`.

2. **O7/O8**
   - E: `known left MCA infarct`
   - C: `left MCA infarct two years ago`
   - Literal containment can fail because `known` is present only in E.
   - The timing is clinically useful and appears in the signer's preferred A/P style.

3. **P2 memory COURSE**
   - E: `family's concern about her memory`
   - C: `daughter: memory has been getting worse for a year`
   - The proposed lexical subject rule does not link them.
   - Yet P003's own acceptance target requires family-reported memory decline.

The heuristic therefore cannot be tuned around O4/O6/O15. Replace it with a general rule.

### Required revision

Define COURSE relationships by **clinical function**, with a conservative fallback:

- **STATUS:** describes the current state of the problem/patient as a whole and may supply the line status.
- **MODIFIER:** describes the same clinical event/finding as a retained factual item and adds duration, tempo, quantity, evolution, or trend.
- **INDEPENDENT COURSE FACT:** materially supports/qualifies the problem but cannot be safely attached to one factual item; render it as its own factual bullet rather than dropping it.
- **IRRELEVANT COURSE:** does not materially bear on the problem; omit it.

A modifier may be folded only when the relationship is clear from the Handoff. If the relationship is uncertain, do **not** invent the linkage; keep the clinically useful COURSE as an independent bullet.

Do not use "has no subject" as the definition of STATUS. A legitimate status can be subject-bearing. Define status by function, not grammar.

This preserves split-before-classify without silently losing information.

## Blocking issue 2 — ETIOLOGY branch 2 should be removed

P003 currently proposes:

- same cause already in claim -> suppress;
- short ETIOLOGY <=8 words -> append to line;
- otherwise -> reasoning bullet.

The eight-word threshold is arbitrary and creates a new descriptor-import rule.

More importantly, the signer has already clarified the preferred style in this branch: a problem line may contain etiology when the **current formulation itself states it**, while separate explicit etiologic reasoning belongs with the reasoning bullets. The desired seizure example had the etiologic discussion as the final reasoning bullet, not imported from a separate field merely because it was short.

Use this rule instead:

1. If the PRIMARY_CLAIM already expresses the same causal meaning as ETIOLOGY, suppress the duplicate ETIOLOGY.
2. Otherwise, a separate ETIOLOGY entry renders as clinician reasoning after factual evidence / claim qualifiers.
3. Never import a separate ETIOLOGY entry into the problem line solely because it is short.

This restores one clean provenance boundary: **the line gets causal wording from the current claim; separate etiologic reasoning stays reasoning.**

Because `AP_ANCHOR.md` currently says separate ETIOLOGY contributes to the line, P003 must include the corresponding anchor update. Do not leave `05` and the anchor in conflict.

No new user escalation is needed for this point: the user already supplied the preferred A/P pattern in this conversation.

## Blocking issue 3 — permitted transformations are still too broad / unclear

The surface/content distinction is correct, but tighten the list.

Problematic wording:

- `Delete redundant words: articles, repeated subjects, a repeated fact.`
  This is too broad. "Delete words" can change clinical meaning.

- `Lowercase a mid-sentence proper noun only where the source already does.`
  This is unclear and not needed.

Revise the permitted operations to bounded transformations, e.g.:

- capitalization / punctuation;
- removal of a repeated subject **only when combining a verified modifier with its fact**;
- suppression of a duplicate entry, not arbitrary deletion inside a clinically meaningful phrase;
- stripping structural speaker prefixes while retaining material attribution;
- provenance parenthetical rendering;
- date display normalization;
- combining already-present compatible fragments without introducing new clinical words or causal/temporal meaning.

Keep pronoun substitution prohibited when the Handoff lacks the pronoun/demographic fact.

## Reproducibility — keep three runs, strengthen invariants

Three independent runs is the right bar. Do not reduce to two.

The trace table is enough for I8 **if it is line-level and explicit**:
- output line/bullet;
- source O# or O# set;
- transformation rule(s) used;
- any omitted retained O# with reason.

Add invariants for:
- **same O# grouping/pairing** into bullets (e.g. O14+O15 should not be merged in one run and split in another);
- **same placement class** (problem line vs factual bullet vs reasoning bullet vs plan).

Otherwise the current I1-I8 can call semantically different renderings "stable" while the structure moves.

## Acceptance-target consistency

After revising COURSE, explicitly demonstrate that the rule can produce from the frozen Handoff without invention:

- O3 + O4 -> seizure with ~2 min duration;
- O5 + O6 -> postictal confusion with ~1 hr duration;
- O7 + O8 -> prior left MCA infarct with its timing when retained as useful;
- O14 + O15 -> sodium 128 -> 131 after fluid restriction;
- O36 -> family/daughter-reported memory decline over a year, either attached when unambiguous or as an independent COURSE fact.

The proposal's current lexical rule cannot satisfy all five.

## STATUS housekeeping

Do this now as non-architectural state correction, not after P003 implementation:

- D-014 already settles O54; remove the stale "signer decision pending" language.
- Replace `P002 implementation: engineering/mock validated; 05 not stable across runs` with a non-contradictory state such as:
  `P002 implementation complete; mock acceptance BLOCKED by 05 instability`.
- Doximity remains PENDING; canonical acceptance remains not established.

The D-014 / validation-byte corruption repair is accepted as housekeeping.

## Required P003 v2

Revise only:

1. COURSE classification/linking as above; no brittle lexical-subject heuristic.
2. ETIOLOGY: duplicate-of-claim suppress; otherwise reasoning bullet; no short-cause promotion.
3. Update `AP_ANCHOR.md` in the proposal scope so it matches the ETIOLOGY rule.
4. Tighten permitted surface transformations.
5. Add pairing/placement invariants to the three-run reproducibility protocol.
6. Correct STATUS now.

Then return P003 v2 for review. Do not implement `05` yet.
