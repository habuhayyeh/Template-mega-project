# DeepSeek architecture review — F1 reconciled evidence + F1V validator

**Reviewed:** `01-RECONCILED-EVIDENCE.md`, `01V-RECONCILED-EVIDENCE-VALIDATOR.md`,
escalation 131, D-039/D-042/D-044/D-045.
**Status:** architecture verdict only; no implementation.

## Verdict

F1V is not an independent validator. It is a second editor using the same model, same source, and largely
the same blind spots. F1 creates a new claim layer; F1V asks the model to bless that layer. The VERIFY
ledger made the failure more visible, not less likely.

The root problem is the **claim layer**, not the validator prompt.

## Q1 — root cause

Primary causes, in order:

1. **F1 synthesizes new `fact:` prose.** Those sentences are not source quotes. Every one creates a
   support obligation that only semantic interpretation can discharge. F1 then supplies refs, but refs
   do not prove the sentence.
2. **F1V is same-model self-review.** Same context, same source, same generation biases. It is anchored
   to F1's wording, not independent. A fresh session may reduce anchoring but not the claim-layer
   problem.
3. **Seven checks per item overloads GPT-4o.** With 50–150 items, the model must make hundreds of
   judgments. It emits plausible `PASS` tokens because the schema rewards completing the ledger, not
   because it dereferenced each ref.
4. **Weak local dereferencing.** The observed errors are topic-neighbor citations: question record for
   answer, T036 for T037, T133 for T134. The model checks "same topic," not "this record's text supports
   this clause."
5. **Responsibility overlap.** F1 already claims to enforce refs/action/attribution; F1V repeats it.
   Neither owns a mechanical substrate.
6. **Repair authority destroys independence.** F1V can rewrite F1, then validate its own rewrite.

GPT-4o limitation is real, but the architecture amplifies it. A better structure does not require the
model to verify its own paraphrases.

## Q2 — fresh-session hypothesis

Worth **one cheap experiment** only to measure anchoring. Do not make it the architecture.

A fresh session may help because F1V no longer sees its own prior answer. But it still has:
- the same long packet;
- the same seven-check overload;
- the same need to judge semantic support;
- the same model family and failure modes.

If fresh F1V still false-passes, the hypothesis is dead and you have spent one run. If it improves, it
still does not fix the claim layer.

## Q3 — validator architecture

**Choose G: remove the semantic validator as a separate function; make F1 produce quote-anchored
evidence, then use a narrow reference/quote audit.**

Not A/B: same-model semantic validator.
Not C as proposed: a deterministic checker cannot judge semantic support.
Not D: proof obligations become another ledger the model can fill superficially.
Not E: two generation passes are expensive and still correlated.
Not F alone: simplifying F1 without changing the claim layer leaves the same support problem.

The recommended shape:

```text
Scribe packet
  -> F1 evidence index (clusters + exact source anchors; no synthesized fact prose)
  -> F2 reconciliation / action state
  -> F3 problem architecture
  -> F4 note compiler
  -> F5 renderer
```

No F1V by default. A small `F1-QUOTE-CHECK` may verify that every cited anchor exists verbatim; it does
not judge clinical support.

## Q4 — what should be deterministic

Outside the Ask runtime (engineering validation), or as the narrowest possible runtime check:

- every ref exists verbatim in the packet;
- ref namespace is correct (`T###` vs `P1.###`);
- no duplicate IDs;
- exact anchor quote is a substring of the cited record;
- every cluster has at least one record;
- every record is either clustered or explicitly dispositioned (if coverage is required);
- action-state lexical transitions where the source words are unambiguous
  (`recommended` -> `received` is a red flag, not proof);
- question/answer record type only if the packet or F1 marks it mechanically.

Do not call semantic support deterministic. It is not.

## Q5 — what must remain semantic

- whether an exact quote actually supports a clause;
- source reasoning vs fact;
- whether a cluster is one subject or an omnibus bundle;
- ambiguous action-state meaning;
- downstream separability when time/polarity/attribution differ.

Keep those judgments **downstream**, where the model is doing real work, not in a separate validator
whose only job is to bless F1.

## Q6 — is F1 doing too much?

Yes. F1 currently does:

- extraction;
- reconciliation;
- compression;
- claim synthesis;
- citation;
- downstream-separability prediction;
- action-boundary policing;
- self-checking.

That is too much for one GPT-4o pass. Narrow F1 to **grouping and anchoring**:

- cluster source records by subject/event/trajectory;
- preserve exact source quotes for each cluster;
- preserve source IDs, time, attribution, polarity and uncertainty;
- do not write abstract `fact:` sentences;
- do not predict problem membership or note sections;
- leave action-state reconciliation to F2/F3 and problem identity to F4.

## Q7 — smallest practical runtime

```text
Scribe V2.2 packet
  -> F1 evidence index (clusters + exact anchors)
  -> F2 reconciliation + action state
  -> F3 problem architecture
  -> F4 note compiler
  -> F5 renderer
```

This removes F1V and the separate action-state function if F2 can own both reconciliation and action
state. If action-state errors remain high-impact, keep F2 and F3 separate; still no F1V.

## Critique of F1 — `01-RECONCILED-EVIDENCE.md`

### The central contradiction

The file says it is an **index/reconciliation layer** and "prefer references over copied prose" (lines
9, 62). But its output is `fact: <compact source-supported representation>` (line 31). That is new prose,
not an index. Every `fact:` sentence is a claim that needs support verification.

### No exact anchors

`refs:` lists record IDs, but no quoted source span. The validator cannot tell whether the cited record
actually contains the clause. This is exactly how T036/T037 and T133/T134 pass.

### It asks F1 to predict downstream decisions

The downstream-separability test (lines 86–93) asks F1 to guess future problem membership, temporal
stance, section placement, inclusion and action handling. That is S1/S3 work. F1 should split on
objective differences (subject, time, polarity, attribution), not predicted note use.

### Action boundary is porous

Line 221 allows executed interventions inside `fact:` "when needed to preserve chronology." That is how
prospective ED workup became a FACT. F1 should not put action-state content in `fact:` at all; it can
preserve the source record in the cluster and let F2/F3 adjudicate.

### "Compact" is unmeasured

Lines 64–66 say "somewhat larger complete handoff" is better than a smaller bundled one, but there is no
target. The model chooses compression arbitrarily.

### It is too long

299 lines, multiple overlapping rules, examples and self-checks. GPT-4o will satisfy the shape, not every
rule.

## Critique of F1V — `01V-RECONCILED-EVIDENCE-VALIDATOR.md`

### It is an editor, not a validator

Line 18 says it may return a corrected handoff. Line 188 says correct the item. A validator that repairs
its own findings and then validates the repair is not independent.

### Seven checks per item is schema theater

`REF/SUPPORT/QUESTION/ACTION/ATTR/BOUNDARY/SEPARABILITY` for every item is too many judgments. The model
can emit a complete ledger without dereferencing each record. V2 proved this empirically: full VERIFY
ledger, false PASS.

### `SUPPORT=PASS` is not checkable from the prompt

There is no requirement to quote the supporting text. The validator judges "support" from memory of the
packet. That is the same task F1 already failed.

### It validates F1's wording, not source truth

The validator sees F1's claim first and the packet second. It is anchored to the claim. More instructions
do not create independence.

### `BOUNDARY` and `SEPARABILITY` are downstream judgments

These require problem/role/note reasoning. A narrow F1 validator should not own them.

### Repair can introduce new errors

F1V can rewrite a FACT and output it as "corrected" without an independent check. That moves risk, not
removes it.

## Recommended different structure

### F1 output: clusters with exact anchors

```text
@@HANDOFF F1_EVIDENCE_INDEX_V1

CLUSTER C001 — prior seizure history
  records: T153,T154,P1.010
  anchors:
    T153: "Any previous seizures?"
    T154: "No."
    P1.010: "No prior seizure history."
  status: source-supported denial

CLUSTER C002 — current episode
  records: T037,T084,T089
  anchors:
    T037: "I've never had that before."
    T084: "It happened again last night."
  status: unresolved timing

@@END
```

No `fact:` sentence. The downstream reads exact quotes and decides what they mean.

If a short label is needed, it must be a **label**, not a clinical assertion. If an assertion is needed,
every clause must have its own exact anchor:

```text
CLAIM C001.1
  text: no prior similar episode
  anchor: T037:"I've never had that before."
```

Then a narrow check can verify the anchor exists and is quoted exactly. Support remains semantic and
belongs downstream.

### Remove F1V

Replace it with:

1. a deterministic external preflight for IDs/anchors/coverage, used in engineering only;
2. an optional runtime `F1-QUOTE-CHECK` that only verifies quote existence, never clinical support;
3. downstream F2/F3/F4 reading the Scribe packet directly when the index is insufficient.

### Keep the useful F1 rules

- one cluster = one subject/event/trajectory;
- do not merge unrelated domains;
- preserve time, polarity, attribution and uncertainty;
- questions are not answers;
- action mentions are not action-state adjudication;
- source reasoning stays separate;
- lazy splitting, not global atomicization.

## Experiment

1. Rewrite F1 as a quote-anchored index; no `fact:` prose.
2. Run it once on the frozen V2.2 packet.
3. Check only:
   - every cluster has records;
   - every anchor quote exists verbatim;
   - no question-only anchor supports an answer;
   - no action-state claim appears;
   - coverage of material subjects.
4. If F1 index is stable, run F2/F3/F4 directly from it. Do not build another validator until a real
   downstream failure appears.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
