# Review 139 — File A full-packet capability test against predeclared oracle

## Verdict

**FAIL — A survives the packet at scale, but does not yet survive semantically.**

This is **not** a truncation/unit-explosion failure.

Observed:
- output completed through `@@END`;
- 16 semantic units;
- 7 action entries;
- 6 unresolved entries;
- output size 18,950 bytes vs frozen Scribe packet 34,700 bytes;
- Wednesday and Thursday episodes remain distinct;
- baseline staring remains distinct;
- prospective EEG/MRI/CT/labs are not represented as completed results.

However the predeclared oracle contains fatal-failure criteria. Two are met:

1. **material action-state promotion/misclassification**;
2. **clinically important attribution inversion**.

Therefore current A does not pass the capability gate.

## Predeclared oracle score

- PASS: 39
- FAIL: 9
- N/A: 3

### FAIL items

| Oracle | Result | Finding |
|---|---|---|
| 4 | FAIL | X005 degrades to broad `T002-T294` speaker-range evidence instead of local selectors. |
| 12 | FAIL | patient prior-seizure history and family seizure history are collapsed into U008 rather than preserved as distinct semantic assertions. |
| 14 | FAIL | U011 states tobacco use is denied, while source only says smoking status is not on file. |
| 15 | FAIL — FATAL | U005 attributes semiology to “SPK3 patient recall,” but Scribe explicitly identifies SPK3 as the mother, Karina. |
| 26 | FAIL — FATAL | A001 merges prior reported Keppra administrations with the current-encounter load discussion into one cross-time action object, obscuring which dose/state belongs to which action. |
| 28 | FAIL — FATAL | action fields are separated structurally but state normalization is not reliable: planned CT/labs are labeled `ordered`; admission recommendation receives inferred `execution=pending`; P1.014 “started on drip” is labeled as an `ordered` decision rather than a reported execution. |
| 29 | FAIL | A001 actor becomes `Harmony of the Seas medical + ED/neurology` across several distinct action mentions without source-local ownership. |
| 44 | FAIL | U015 mixes diagnostic assessment/differential and the management decision to continue Keppra inside one `kind=diagnosis` unit; assertion types are not cleanly separated. |
| 51 | FAIL | material note-relevant semantic content is not consistently represented. Examples: ED initial differential P1.042 is absent; the explicit current plan to keep Keppra for now appears in U015 prose but is not represented as a structured ACTION. |

### N/A items

20, 23, 35: the frozen packet contains no established historical neurologic disease such as the earlier synthetic left-MCA-stroke example. These oracle items do not apply to this packet.

## Fatal finding 1 — speaker attribution inversion

Scribe establishes:
- SPK2 = fiance;
- SPK3 = mother Karina.

Current A U005 says:
> `attribution=SPK2 fiance + SPK0 paramedic brother (Logan/William) direct witness; SPK3 patient recall`

This converts mother/collateral into patient attribution for seizure semiology.

The same degradation appears elsewhere:
- U012 attribution says `SPK3 patient/family` despite SPK3 being identified as mother.

This is clinically material because patient recall vs witnessed collateral semiology are not interchangeable.

## Fatal finding 2 — action-state normalization

### CT/labs

Source:
- P1.045 says `Plan: CT head ... basic labs, urinalysis`.

A output:
- A002 `decision=ordered`;
- A003 `decision=ordered`.

The source establishes a plan, not an order-state field.

### Keppra

Source distinguishes:
- historical/reported administration: P1.009, P1.053;
- source-reported drip: P1.014 / T135;
- current neurology load recommendation: P1.054;
- later discontinuation of the 1500-mg load: P1.055;
- current neurology decision to keep patient on Keppra for now: T258.

A001 collapses these into one `Keppra loading/drip` action spanning cruise + ED/neurology.

It also maps:
- P1.014 `started on a Keppra drip` -> `decision=ordered`, even though that wording is a reported execution state.

The current “continue Keppra for now” management decision survives only in U015 free semantic text and is not represented as its own ACTION.

### Admission

Source says admission is favored/recommended.
A006 adds:
- `execution=pending`

without a source citation establishing execution-state acceptance.

## Other important failures

### Separate seizure-history assertions collapsed

U008 concept:
> `No prior history of seizures and no family history of seizures`

The patient-history assertion is supported independently by P1.010.
The family-history assertion comes from T154/T155.

These should remain separate because they answer different clinical questions and the oracle explicitly predeclared that separation.

### Negative invented from “not on file”

U011:
> `Denies alcohol, tobacco, illicit drug use and sexual activity`

Source supports patient denial of sexual activity, drug use and alcohol use.
Source says tobacco/smoking status is **not on file**, not denied.

This is exactly the absence-of-documentation -> negative conversion the oracle was designed to catch.

## What worked well

The failure should not obscure real progress.

### Scale behavior

A does **not** show the earlier atomic-F1 pathology:
- no 175-object explosion;
- no truncation;
- no copied near-full corpus;
- only 16 semantic units.

Output is roughly 55% of source byte size, much of which is schema overhead.

### Event organization

A successfully separates:
- Wednesday first event;
- Thursday recurrent cluster;
- baseline staring behavior.

It preserves:
- uncertainty in Wednesday timing;
- uncertainty in monitoring duration;
- uncertainty in head-version/eye-state details.

### Workup state

A keeps:
- CT/labs as non-executed actions;
- EEG/MRI as future/not performed;
- shipboard workup as reported outside results.

It does not turn future EEG/MRI into results.

### Boundaries

A does not create:
- PRIMARY/BACKGROUND;
- containment;
- problem causality;
- note sections;
- final note prose.

## Failure classification

The evidence does **not** support splitting A merely because the packet is too large.

Failure class is:

### Primary
**source-semantic normalization / attribution / action-state fidelity**

### Secondary
**mixed-assertion bundling**

### Not demonstrated
- context-window overload;
- output-size overload;
- global atomicization;
- inability to reconcile acute event chronology.

## Architectural implication

Do **not** reopen Evidence Ledger wholesale yet.

The full-packet run shows that the current A can handle the source volume. The defects occur in how A normalizes source assertions.

Before splitting A1/A2, determine whether the failures can be removed by narrowing A's local normalization contract:

1. speaker identity must come only from explicit identity evidence; no free-form role guessing;
2. action state needs a source-faithful vocabulary that distinguishes at least:
   - discussed/considered;
   - planned;
   - recommended;
   - ordered;
   - reported_performed;
   - performed;
   - held/discontinued;
   - result/response when explicit;
3. one ACTION object must represent one action episode/state trajectory, not all mentions of the same drug across different settings/times;
4. mixed diagnostic + action content must split by assertion type when the management distinction matters;
5. “not on file” must never normalize to a negative;
6. patient-history and family-history assertions remain semantically separate.

If those bounded changes make A pass, no A1/A2 split is needed.

If the same defects persist after a narrow A revision, then a source-semantic A1 / reconciliation A2 split becomes justified by evidence.

## Next peer question

The key decision for DeepSeek/ChatGPT is now:

> Are these failures best explained by an over-broad A task, or by insufficiently constrained local field semantics inside an otherwise scalable A?

My current view: **patch the local semantics once before splitting A.**

The packet-size hypothesis is not supported by this run.
