# ChatGPT review 095 — D-031 nearly accepted; positive causal calibration still missing

## Verdict

> **NEAR-PASS. One substantive blocker remains: the required positive causal calibration is not in Gate 0.**

Target: DeepSeek commit `220d32b`.

## Accepted

The following D-031 corrections are accepted:

- identities bumped to `SCHEMA-4 / PILOT-3 / ACTIVE-PILOT-3 / ORACLE-4.0 / GATE0-C3`;
- `S2-CAUSAL-01` semantic predicate exists;
- `S2-CAUSAL-02` mechanical causal-shape/reference predicate exists;
- `S3-ROLE-01` semantic role predicate exists;
- `S3-ROLE-02` mechanical role-shape predicate exists;
- `S4-ROLE-01` checks role propagation;
- causal projection requires both endpoints retained;
- CASE-01 now encodes falls PRIMARY, prior infarct BACKGROUND, no causal relation;
- role semantic calibration has a valid positive clean state plus a structurally valid semantic flip:
  `G0-S3-11` changes the infarct BACKGROUND -> PRIMARY.

DeepSeek validation is otherwise strong:
- 49 tests OK;
- preflight PASS 7/7;
- deterministic regeneration;
- 35 seeds / 21 active predicates;
- no answer-key leakage.

## Blocking defect — positive causal branch is not calibrated

D-031 explicitly required:

> a separate positive causal calibration fixture for residual-deficit-vs-historical-disease subject
> and LIKELY/POSSIBLE strength.

The implementation says the positive fixture exists only in `tests/test_scorer_more.py`.

That is not sufficient.

A unit-test fixture never becomes a blinded signer/evaluator packet, so it cannot calibrate
`S2-CAUSAL-01`.

The current Gate-0 causal evidence only contains:

1. CASE-01 clean: `causal_relations=[]` — tests **do not invent causality**;
2. `G0-S2-07`: adds a history-only relation from `O01` old stroke to falls — semantic FIRED;
3. `G0-S2-08`: uses invalid strength `CERTAIN` — mechanical FIRED.

This does **not** test the two clinically important positive distinctions:

- correct acting subject:
  `chronic right-sided weakness from prior stroke`
  versus
  `prior stroke`;

- calibrated strength:
  `POSSIBLE`
  versus an overstatement to structurally valid `LIKELY`.

Both `POSSIBLE` and `LIKELY` are valid schema values. A mechanical enum test cannot adjudicate that
semantic difference.

### Required fix

Add the smallest **actual Gate-0 positive causal parent/case**, not merely a unit-test fixture.

Its source should explicitly support something equivalent to:

> chronic right-sided weakness from prior L MCA stroke may contribute to the falls.

Clean S2 causal truth:

- `from` = residual-weakness object;
- `to` = falls object;
- `relation = CONTRIBUTOR`;
- `strength = POSSIBLE`;
- support = current source span that states the relationship.

Add isolated semantic mutations from that clean parent:

1. **wrong causal subject** — substitute the historical stroke object for the residual-deficit object,
   while keeping everything structurally valid -> `S2-CAUSAL-01 FIRED`;

2. **overstated strength** — `POSSIBLE -> LIKELY`, structurally valid -> `S2-CAUSAL-01 FIRED`.

The clean positive parent itself must produce a blinded `S2-CAUSAL-01` signer packet with expected
reference SILENT.

Do not alter CASE-01; it remains the negative/no-inference branch.

## Stale wording

`predicates.md` still says:

> "Under D-023, a major established primary neurologic diagnosis is a valid candidate even when inactive"

This now conflicts with D-030 terminology.

Replace it with wording that separates candidacy/A-P representation from encounter role, e.g.:

> a major established neurologic diagnosis may remain a valid A/P candidate even when BACKGROUND and
> inactive; candidacy does not imply PRIMARY encounter role.

## Identity handling

Because GATE0-C3 has not been accepted and has zero signer/evaluator evidence, this focused correction
may remain within the provisional SCHEMA-4/PILOT-3/GATE0-C3 package **if**:

- the current `gate0-packets-c3-d031` run is explicitly marked superseded;
- regenerated packet ids/hashes replace it;
- no evidence is reused.

No further version bump is required solely for completing an already-authorized D-031 requirement.

## NEXT

DeepSeek adds the positive causal Gate-0 parent + two semantic mutations, fixes the stale wording,
regenerates, runs tests/preflight/packets mode, and returns the exact diff and new signer packet count.

Do not broaden the review or modify architecture.
No signer references until this passes.
No Gate 0 acceptance. No Doximity. No Phase 0.
