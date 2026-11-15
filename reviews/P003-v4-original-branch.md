# P003 v4 review — original architecture branch

**Reviewer:** ChatGPT (original architecture branch)  
**Proposal:** `proposals/P003-ap-render.md` v4  
**Verdict:** **ACCEPT ARCHITECTURE — one user-level frozen-case decision remains before implementation**

## Accepted

P003 v4 resolves the remaining architecture objection.

Accepted without further change:

- COURSE-by-function architecture;
- relevance gate before COURSE classification;
- STATUS / MODIFIER / INDEPENDENT COURSE FACT / IRRELEVANT;
- facts before reasoning;
- separate ETIOLOGY never imported into the problem line;
- ETIOLOGY suppression only when it adds no distinct reasoning beyond what PRIMARY_CLAIM already fully states;
- ETIOLOGY retained as reasoning when it adds certainty, mechanism, rationale, contrast, or uncertainty;
- bounded surface transformations 1–8;
- traced STANDING_ITEMS;
- speaker attribution preservation;
- signer-style duration normalization (`about two minutes -> ~2 mins`);
- three fresh-context runs;
- I1–I10, including pairing and placement stability;
- AP_ANCHOR update in scope;
- O54 remains body-only;
- no reopening of 01/02/04/06/07.

## One user-level decision remains

The frozen case is intentionally ambiguous under the accepted general rule:

PRIMARY_CLAIM:
`post-stroke seizure from the old left MCA scar rather than a new lesion`

ETIOLOGY:
`scar from your old stroke is the most likely cause of the seizure`

Question:

**Should the ETIOLOGY render as a separate reasoning bullet, or be suppressed as redundant with the problem line?**

Both are defensible from the text alone:

- **Suppress:** the line already says the seizure is from the old scar rather than a new lesion; `most likely cause` may add no material reasoning.
- **Render:** `most likely cause` is an explicit clinician certainty statement and D-004 favors preserving explicit reasoning.

This affects what the note says to the reader and cannot be settled mechanically. Under D-013, the signer decides.

My recommendation for this exact frozen case: **suppress it**, because the PRIMARY_CLAIM already contains both the causal attribution and the comparative alternative (`rather than a new lesion`). The ETIOLOGY adds no mechanism, rationale, or uncertainty beyond that line. This does **not** weaken the general rule: richer ETIOLOGY such as `the chronic left MCA infarct is a plausible epileptogenic substrate` would render when the claim does not carry that distinct reasoning.

Once the signer decides, pin that outcome in the acceptance record so I4 tests stage stability rather than rule ambiguity.

## DOXIMITY.md

The revised evidence split is accepted.

It now correctly distinguishes:
- actual Doximity evidence: the three 06 runs;
- local/mock evidence: the repeated 05 runs;
- historical recollections without raw artifacts: not canonical evidence.

The coverage-gap statement and the design conclusion that more prompt prose is not automatically a fix should remain.

## Next step

Do not implement P003 until the signer resolves the frozen ETIOLOGY case and explicitly approves implementation.

After that decision:
1. record it as the next D-###;
2. implement P003;
3. run the three-run mock protocol;
4. review actual diffs + invariant table;
5. only then request Doximity acceptance.
