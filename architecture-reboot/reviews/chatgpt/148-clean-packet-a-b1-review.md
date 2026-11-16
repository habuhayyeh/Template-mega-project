# Review 148 — Clean Scribe packet A -> B1 run

## Verdict

**The cleaner Scribe packet is sufficient for the intended note. Stage A is mostly usable; B1 normalized
action-state remains structurally brittle and should not be patched again without architectural review.**

This run used a much cleaner, concise `SCRIBE_EVIDENCE_V2_2` packet and still reproduced the exact state
completion errors D-049 was designed to eliminate.

## Intended downstream note

The signer supplied a target note demonstrating the practical requirement:
- concise HPI chronology;
- baseline staring separated from current events;
- source-qualified outside workup;
- current neurologic diagnostic stance;
- EEG/MRI;
- continue levetiracetam for now and reassess after EEG/MRI;
- favor inpatient workup;
- safety/driving counseling.

The clean Scribe packet directly supports that target without needing speculative state completion.

## Stage A

A is substantially improved and mostly useful.

### Good

- no prior seizure history and family history preserved;
- current events separated from baseline staring spells;
- outside workup remains source-mediated;
- PNES suspicion and epileptic seizure under evaluation preserved;
- exam split into orientation and focal-deficit findings;
- current actions for EEG, MRI, levetiracetam continuation, inpatient workup, safety and driving preserved.

### Remaining provenance defect

One source pointer drifts:
- S007 cites `T005`;
- selector is `her eyelids began fluttering/opening and closing with abnormal eye movements`;
- that wording belongs to T006 in the clean packet.

This is a real source-fidelity defect, but it is isolated and does not explain the B1 failures.

## B1 — repeated normalized-state failure

B1 again fills unsupported state dimensions despite explicit prohibitions.

### 1. Reported normal outside result becomes `result=unavailable`

For blood testing:
- source says they were told it was normal;
- B1 emits `result=unavailable`.

The source contains a reported result; the enum schema cannot represent “reported normal / not directly reviewed”
cleanly.

### 2. Unspecified additional testing gets invented `result=unavailable`

`obtained additional testing` has no result statement.

B1 nevertheless emits `result=unavailable`.

### 3. EEG/MRI need -> not_started + unavailable

For `EEG and MRI brain are needed`, B1 emits:
- decision=recommended;
- execution=not_started;
- result=unavailable.

Only the decision/recommendation is supported.

This exactly reproduces the prior A-level schema-completion failure, now inside B1.

### 4. CT “not yet reviewed” becomes `result=pending`

The source says CT was completed but not yet reviewed by Neurology and no CT result was available to Neurology.

B1 maps that to `result=pending`.

That conflates:
- test completion;
- result existence/finality;
- result availability to this clinician;
- review status.

The current enum cannot represent this distinction safely.

### 5. Continue levetiracetam -> `execution=not_started`

`will be continued for now` supports a continuation decision.

B1 again invents execution=not_started.

### 6. Favor inpatient workup -> `execution=not_started`

`favored completing the workup inpatient` supports a recommendation/preference.

B1 again invents execution=not_started.

## Interpretation

This is no longer a prompt-tuning problem.

The same completion behavior has survived:
- optional state slots;
- exact-phrase asserted states;
- moving normalization from A2 to B1;
- repeated explicit prohibitions;
- bare-shorthand rules;
- a much cleaner source packet.

The representation itself continues to invite completion.

## Recommended architecture review

Do **not** add another rule or validator.

Two plausible simplifications:

### Preferred

Retire normalized decision/execution/response/result enums.

Let the action layer preserve:
- source-local action identity;
- source-qualified exact wording;
- episode grouping only when supported;
- source/setting/time/condition;
- unresolved relationship.

Then let problem architecture choose which current source-qualified actions belong in the plan.

### More aggressive

If B1 has no independent job after state enums are removed, fold supported action reconciliation into B2/problem
architecture and remove B1 as a separate runtime stage.

The signer’s target note does not require explicit state enums. It requires reliable distinctions in final wording:
“reportedly received,” “needed,” “continue for now,” “reassess after,” “favored inpatient,” “counseled.”

Those distinctions are already present in the source packet/A action wording.

## Stage A provenance issue

The isolated T005/T006 pointer drift still needs handling, but should not be used to justify preserving B1 state
normalization.

No further Doximity run recommended until architecture adjudication.
