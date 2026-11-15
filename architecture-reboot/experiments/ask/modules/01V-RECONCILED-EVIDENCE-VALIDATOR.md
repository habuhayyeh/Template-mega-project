# FILE 1V — RECONCILED EVIDENCE VALIDATOR

**Experimental version:** F1V-RECONCILE-V2

## Function

Validate the output of **FILE 1 — RECONCILED EVIDENCE** against the original Scribe V2.2 packet.

This is a narrow runtime validator.

It does **not** perform a new clinical interpretation pass.
It does **not** build problems.
It does **not** choose the final encounter diagnosis or plan.
It does **not** write the note.

Its job is:

> detect concrete File-1 contract violations, then return a corrected File-1 handoff only when the correction is directly determined by the source.

## Inputs

Provide all three:

1. the unchanged `SCRIBE_EVIDENCE_V2_2` packet;
2. the current canonical `01-RECONCILED-EVIDENCE.md`;
3. the exact File-1 output to validate.

## Required execution pattern

Do not jump directly to `STATUS=PASS`.

First perform an explicit compact audit of **every** File-1 item.

For each FACT / SOURCE_REASONING / UNRESOLVED item, emit exactly one line:

```text
VERIFY <item id> :: REF=<PASS|FAIL> :: SUPPORT=<PASS|FAIL> :: QUESTION=<PASS|FAIL|NA> :: ACTION=<PASS|FAIL|NA> :: ATTR=<PASS|FAIL|NA> :: BOUNDARY=<PASS|FAIL> :: SEPARABILITY=<PASS|FAIL>
```

Definitions:

- `REF` — every cited id exists verbatim in the Scribe packet.
- `SUPPORT` — every meaningful clause is supported by at least one cited ref, and every cited ref is relevant to at least one clause.
- `QUESTION` — no question-only record is being used as evidence for an answer.
- `ACTION` — no action state was upgraded beyond the source.
- `ATTR` — no speaker/person role was invented beyond the source.
- `BOUNDARY` — FACT / SOURCE_REASONING / UNRESOLVED placement is correct and no downstream plan/classification was invented.
- `SEPARABILITY` — the item is one downstream-usable subject/event/state/trajectory rather than an omnibus bundle.

A validator run is invalid if any File-1 item is omitted from the VERIFY ledger.

A validator may return `STATUS=PASS` only if **every** applicable VERIFY field is PASS/NA.

If any field is FAIL:
1. repair the item from source when directly determined;
2. re-check the repaired item;
3. return the complete corrected F1 handoff.

Do not hide failures merely because the overall handoff looks clinically plausible.

## Validation checks

Check every FACT, SOURCE_REASONING, and UNRESOLVED item.

### V1 — reference existence

Every cited record id must exist verbatim in the Scribe packet.

FAIL examples:
- invented id;
- wrong numeric id;
- `T###` changed to `P1.###`;
- `P1.###` changed to `T###`.

### V2 — local reference support

Every independently meaningful clause must be supported by at least one ref listed in that same item.

Delete unrelated refs.

Do not use nearby records merely because they discuss the same topic.

### V3 — question-as-answer error

A question-only record cannot support the truth of an answer.

Example:

```text
T153: clinician asks whether prior seizures occurred
```

cannot support:

```text
No prior seizure history.
```

unless another cited record actually supplies that answer.

### V4 — action-state fidelity

Do not convert:

```text
CONSIDERED -> RECOMMENDED
RECOMMENDED -> ORDERED
ORDERED -> ADMINISTERED
PLANNED -> PERFORMED
PERFORMED -> RESULT_AVAILABLE
DISCONTINUED -> WAS_PREVIOUSLY_ADMINISTERED
```

unless the source explicitly establishes the later state.

If a FACT overstates an action state, rewrite it to the narrowest source-supported wording.

Do not decide the final plan.

### V5 — transcript attribution

Do not infer a stable real-world identity from `SPK0`, `SPK1`, etc. unless the relevant source record explicitly establishes that identity.

If identity is uncertain, use source-neutral wording such as:
- transcript reports;
- collateral report;
- one speaker reports.

### V6 — source reasoning vs fact

A source hypothesis, differential, diagnostic impression, causal interpretation, or uncertainty must stay in `SOURCE_REASONING` unless independently established as fact elsewhere.

Do not promote:
- possible;
- likely;
- favored;
- suspected;
- "could be";
- differential diagnosis;

into an unqualified FACT.

### V7 — unresolved scope

`UNRESOLVED` may preserve:
- source conflict;
- unclear timing;
- uncertain laterality;
- unavailable result;
- unclear attribution;
- incomplete source answer.

It may not invent:
- a new diagnostic question;
- a management recommendation;
- a test to obtain;
- a next step;
- a final classification.

### V8 — downstream separability

A FACT must still represent one clinical subject/event/state or one coherent trajectory.

Split only if the existing File-1 output combined propositions that later functions could reasonably treat differently for:
- problem membership;
- temporal stance;
- note placement;
- action handling;
- inclusion/disposition.

Do not globally atomize the packet.

### V9 — omission from reconciliation

Do **not** demand that every Scribe record appear in File 1.

Only flag omission if a clinically meaningful distinction was lost that could change later:
- neurologic problem identity;
- current state/certainty;
- causal reasoning;
- action state;
- exam/workup interpretation;
- functional/safety context;
- management.

## Repair policy

When a violation is directly correctable from the supplied Scribe packet:

- correct the File-1 item;
- remove unsupported wording;
- replace invalid refs;
- move source reasoning out of FACT when needed;
- split an overbundled FACT only when required.

Do not add new clinical content merely to make the handoff more complete.

When the source does not determine the correction:
- preserve the uncertainty as `UNRESOLVED`;
- do not guess.

## Output

Always begin with the complete VERIFY ledger.

If no material violations are found after the ledger:

```text
@@VALIDATION F1V_RECONCILE_V2
<VERIFY lines for every F1 item>
STATUS=PASS
@@END
```

If violations are found and can be repaired, return:

```text
@@VALIDATION F1V_RECONCILE_V2
<VERIFY lines for every original F1 item>
STATUS=REPAIRED

<complete corrected F1 handoff, beginning with @@HANDOFF F1_RECONCILE_V1 and ending with @@END>

@@VALIDATION_END
```

Return the **complete corrected handoff**, not a patch list.

If a material issue cannot be safely repaired from the source:

```text
@@VALIDATION F1V_RECONCILE_V2
<VERIFY lines completed up to the blocking item>
STATUS=BLOCKED
ITEM=<Fxxx/Rxxx/Uxxx>
ISSUE=<brief reason>
@@END
```

## Boundary

This validator is a runtime reliability aid.

Its PASS is **not acceptance evidence** and does not replace external engineering review, scorer calibration, or Phase-0 audit.

This validator is intended to run as a **separate companion file after File 1**, even when both execute sequentially in the same Ask call. Do not merge F1 and F1V into one prompt file for the active experiment.

The validator may repair only File-1 contract violations.

It may not perform File 2, File 3, or later semantic work.
