# Function Placement

## Purpose

This file defines **where a function belongs** in the Doximity workflow.

The placement rule is:

> Put a function at the earliest layer where all information needed for that function exists, but no earlier than necessary.

Also:

> If deferring the function would destroy provenance or state fidelity, it must be source-local.

---

# 1. Source-local Scribe functions

These must happen while processing the raw source unit.

## 1.1 Source boundary

Preserve:

- raw transcript-turn boundary;
- raw speaker label;
- direct prechart source;
- nested provenance;
- source order.

### Why local

Once source units are merged, provenance cannot be safely reconstructed.

---

## 1.2 KEEP / OMIT conversational noise

Decide whether one raw unit contains:

- clinical evidence;
- clinician interpretation;
- management;
- necessary context;

or only:

- acknowledgment;
- navigation;
- unanswered question;
- nonclinical logistics;
- immediate echo.

### Why local

The raw conversational form is available here.

---

## 1.3 Source-local splitting

Split one raw unit only when one output record would obscure an independently recoverable distinction.

Examples:

- different events;
- different time periods;
- assessment vs management;
- separate investigations;
- separate medication actions;
- disposition vs counseling;
- different polarity;
- different certainty.

### Why local

Later stages should not have to rediscover hidden clause boundaries from compressed prose.

---

## 1.4 Source-state preservation

Preserve distinctions explicitly stated by the source:

- considered;
- discussed;
- favored;
- recommended;
- needed;
- planned;
- ordered;
- canceled;
- administered;
- continued;
- stopped;
- performed;
- completed;
- reviewed;
- result available;
- result unavailable to the speaker;
- reported result.

Do not normalize beyond the source.

### Why local

State is anchored to exact wording and source context.

---

## 1.5 Unclear/verbatim preservation

If wording is genuinely unclear:

```text
[UNCLEAR: ...]
```

If clinically odd but clear:

preserve it.

Do not medically repair.

---

# 2. Whole-packet Scribe functions

These happen **after candidate evidence records exist**.

They should not contaminate each record with extra metadata unless downstream testing proves it necessary.

---

## 2.1 Coverage census

Classify retained record IDs into broad recovery buckets.

Candidate buckets:

- PRESENTING_EVENT
- BASELINE_OR_PRIOR_SYMPTOM
- NEURO_HISTORY
- FAMILY_NEURO_HISTORY
- MEDICATION_OR_SUPPLEMENT
- EXAM
- WORKUP_OR_RESULT
- CONTEXT
- ACTION_BEARING

### Function

Answer only:

> Where does potentially recoverable information live?

Do not answer:

> What does it mean?

---

## 2.2 Action census

For each ACTION_BEARING record, classify broad source-local action type:

- TEST_OR_PROCEDURE
- MEDICATION_OR_TREATMENT
- CONSULT
- DISPOSITION
- PRECAUTION
- SAFETY_COUNSELING
- DRIVING_OR_ACTIVITY_COUNSELING
- FOLLOWUP
- OTHER_MANAGEMENT

This does not decide:

- final plan;
- problem ownership;
- adoption;
- episode reconciliation.

---

## 2.3 Completeness audit

After the candidate packet exists, ask:

- Is presenting-event chronology recoverable?
- Is baseline/prior symptom material recoverable?
- Is prior neurologic/seizure history recoverable?
- Is family neurologic history recoverable?
- Are medications/supplements recoverable?
- Is the current neurologic exam recoverable?
- Is relevant workup/result state recoverable?
- Is every clinically meaningful action target recoverable?
- Did a question survive even though its answer is self-contained?
- Did template/scaffold material survive as patient evidence?

If a category is missing because the raw source has no such content, that is not a failure.

---

## 2.4 Final deletion sweep

Remove:

- redundant question records;
- acknowledgment-only records;
- navigation;
- immediate restatement;
- template residue;
- unsupported reconstructed fragments.

Do not delete clinically distinct source evidence merely because another source says something similar.

---

## 2.5 Serialization audit

Check:

- record grammar;
- delimiter spacing;
- valid IDs;
- valid source blocks;
- start/end markers;
- coverage/action index IDs exist in the emitted packet.

Mechanical validation belongs here.

---

# 3. B functions

B is the clinical synthesis owner.

B may:

- decide same vs distinct episode;
- reconcile duplicate/evolving/conflicting records;
- decide baseline comparator role;
- create neurologic problem architecture;
- assign PRIMARY/BACKGROUND when supported;
- build diagnostic stance;
- weigh evidence/counterevidence;
- reconcile action trajectories;
- assign action ownership;
- decide source-qualified management wording;
- emit reconciled clinical units for downstream compilation.

B should not:

- rediscover omitted source coverage if Scribe's census says it should exist;
- invent source state;
- manufacture provenance;
- repair malformed Scribe records;
- assign note sections.

---

# 4. C functions

C is the compiler.

C receives already-decided clinical content.

C may:

- assign note section;
- assign rhetorical class;
- group semantic content;
- choose HEAD / MODIFIER / CONDITION / COVERED;
- assign canonical operator;
- assign final order;
- create decision-complete render groups.

C should not:

- reopen diagnosis;
- rediscover source evidence;
- reconcile episodes;
- decide action state;
- infer problem ownership.

Raw source access, if allowed, should be mechanical dereference only.

---

# 5. Renderer functions

Renderer is a lexicalizer.

Renderer may:

- execute canonical operator;
- insert bounded punctuation/grammar;
- render in exact supplied order;
- suppress COVERED duplicates;
- fail closed on malformed group.

Renderer should not:

- merge/split clinical meaning;
- repair incomplete propositions;
- select a diagnosis;
- attach a condition;
- choose a HEAD;
- infer missing management state.

---

# 6. Why coverage belongs before B

Direct-B repeatedly showed:

- strong problem synthesis;
- appropriate diagnostic stance;
- lower representation burden;

while still omitting:

- history;
- exam;
- workup;
- actions;
- source records.

Therefore the model's problem was not inability to reason.

The problem was doing **coverage discovery and synthesis simultaneously**.

A pre-synthesis coverage census gives B a recovery map without recreating the old atomic evidence layer.

---

# 7. Where the coverage census should live

Current preferred hypothesis:

```text
SCRIBE
  source-local evidence records
  +
  packet-level coverage census
  +
  packet-level action census
        |
        v
B
```

This is preferable to restoring old A if Scribe can emit the census reliably.

Reason:

- Scribe already owns record boundaries;
- the census is nonreconciliatory;
- it can be performed after extraction in the same invocation;
- it avoids another generative pass.

This remains an architecture hypothesis until directly tested.

---

# 8. Function-placement test

Before adding a new function, ask:

### Question 1

Does it require comparing multiple source records?

- No -> probably source-local.
- Yes -> packet-level or B.

### Question 2

Does it require clinical interpretation across sources?

- Yes -> B.

### Question 3

Would deferring it destroy provenance/state fidelity?

- Yes -> Scribe local.

### Question 4

Is it only identifying where information exists?

- Yes -> packet-level census.

### Question 5

Is it deciding how already-decided content becomes note structure?

- Yes -> C.

### Question 6

Is it only converting a complete semantic payload into text?

- Yes -> renderer.

---

# 9. Minimal production target

```text
Scribe
  local source-faithful extraction
  packet-level coverage census
  packet-level action census
        |
        v
B
  reconciliation
  problem architecture
  diagnostic stance
  action reconciliation
  reconciled clinical units
        |
        v
C
  typed groups
  canonical operators
  order
        |
        v
renderer
  lexicalize
  fail closed
```
