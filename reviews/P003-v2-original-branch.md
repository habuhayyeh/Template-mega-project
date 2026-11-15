# P003 v2 review — original architecture branch

**Reviewer:** ChatGPT (original architecture branch)  
**Proposal:** `proposals/P003-ap-render.md` v2  
**Verdict:** **REVISE — narrow contract corrections only; architecture otherwise accepted**

P003 v2 resolves the major objections from v1. COURSE-by-function, reasoning-last, the two-branch ETIOLOGY rule, and three-run semantic stability are the right architecture. Four bounded inconsistencies remain before implementation.

## Accepted architecture

- COURSE classes: STATUS / MODIFIER / INDEPENDENT COURSE FACT / IRRELEVANT.
- STATUS is defined by clinical function, not grammar.
- When modifier linkage is uncertain, preserve a clinically relevant COURSE fact independently rather than inventing a link.
- Facts precede explicit clinician reasoning.
- Separate ETIOLOGY never enters the problem line merely because it is short.
- Same-cause ETIOLOGY may be suppressed when the PRIMARY_CLAIM already carries the same causal meaning.
- Otherwise ETIOLOGY renders as reasoning.
- Three fresh-context runs are required.
- I9 grouping/pairing and I10 placement class are appropriate stability invariants.
- O54 remains body-only.
- The anchor change is consistent with the user's already stated preferred A/P style: the current claim may contain its own cause, while separate explicit etiologic reasoning belongs in the reasoning bullets. No additional user adjudication is needed for that point.

## Must change 1 — relevance gate must precede the COURSE rule of doubt

The current rule says:

> Between INDEPENDENT and IRRELEVANT, choose INDEPENDENT whenever the entry names a clinical event, amount, or interval.

That makes IRRELEVANT nearly unreachable and contradicts the worked O2 example. O2 `admitted 11/12` names both an event and an interval/date, so the rule as written pushes it to INDEPENDENT even though the proposal says admission date alone does not bear on the seizure problem.

Use this order instead:

1. **Relevance gate:** does this COURSE entry materially bear on the retained problem's diagnosis, certainty, chronology, severity, trajectory, or management interpretation?
   - No -> IRRELEVANT.
   - Yes -> continue.
2. If it describes overall current condition -> STATUS.
3. If it clearly modifies a specific retained factual item -> MODIFIER.
4. Otherwise -> INDEPENDENT COURSE FACT.

The rule of doubt applies only **after relevance is established**:
- MODIFIER vs INDEPENDENT -> INDEPENDENT.
- Do not use "names an event/amount/interval" to override irrelevance.

This keeps O2 omittable without reopening silent-loss risk for O15/O36.

## Must change 2 — I8 must explicitly allow STANDING_ITEMS

P003 says:

> every word of the output is either in the Handoff or produced by transformations 1–7

but the accepted A/P may contain `Seizure precautions` from `STANDING_ITEMS.md`, which is intentionally not in the Handoff.

Revise the provenance rule and I8:

> Every output word must trace to either:
> - a Handoff entry;
> - a permitted surface transformation;
> - or an explicitly triggered entry in `STANDING_ITEMS.md`.

The line-level trace table must identify standing-item provenance and the triggering CLAIM.

Otherwise the proposal's own acceptance target fails its invariant.

## Must change 3 — speaker-prefix rendering must preserve material attribution

Transformation 4 currently says to strip `clinician:`, `daughter:`, `patient:` while retaining attribution already present in the remaining text.

That loses attribution for O36:

`daughter: memory has been getting worse for a year`

After stripping the prefix, no daughter/family attribution remains.

Use a bounded rule:

- current-clinician structural prefix (`clinician:`) may be omitted;
- non-clinician speaker prefixes that materially identify the source of a statement must be retained or mechanically rendered as attribution;
- e.g. `daughter: X` -> `Daughter reports X` is a permitted surface transformation;
- do not infer a relationship or speaker not named by the prefix.

Likewise, `patient:` may be rendered as `Patient reports` when attribution is material.

This is not new clinical content; it is natural rendering of an explicit speaker label.

## Must change 4 — acceptance target and style transformation disagree on "~2 mins"

The proposal requires the output to preserve `~2 mins`, while the Handoff contains `about two minutes`. Under transformations 1–7, `~`, `2`, and `mins` are not permitted replacements.

The user's preferred note style explicitly uses `~`, `mins`, and `hrs`, so add one bounded style-normalization transformation rather than weakening no-invention:

- written cardinal number -> equivalent numeral when meaning is unchanged;
- `minutes` -> `mins`, `hours` -> `hrs`;
- `about` / `approximately` -> `~`.

Examples:
- `about two minutes` -> `~2 mins`
- `an hour` -> `1 hr` (without adding `~` unless approximation is present)

Do not generalize this into unrestricted synonym replacement.

If you do not want this transform in P003, then change the acceptance target to the literal Handoff wording. Given the user's stated style, I recommend the bounded normalization.

## Fact ordering

The proposed deterministic ordering — EVIDENCE facts first, then independent COURSE facts — is acceptable for v3. Do not add semantic reordering yet. If the actual three-run output reads badly, that is a visible downstream defect to evaluate then.

For O36 specifically, independent placement after the memory evidence is acceptable provided the daughter attribution survives.

## Reproducibility

Keep all three runs. The trace table is sufficient; no new checker is required in P003.

Add these source classes to the trace:
- Handoff O#;
- transformation ID;
- STANDING_ITEM + trigger claim, when applicable.

## Required P003 v3

Revise only:

1. relevance gate before COURSE classification / doubt handling;
2. I8 and trace support for STANDING_ITEMS;
3. speaker-prefix attribution transformation;
4. bounded duration/approximation style normalization, or revise the target to literal wording.

Everything else in P003 v2 is accepted.

Return v3 for final review. Do not implement `05` or `AP_ANCHOR.md` yet.
