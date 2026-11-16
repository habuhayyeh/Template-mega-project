# DeepSeek review — second semicolon output

**Verdict:** structurally valid now. Semantically, the action lane is still contaminated.

## Structural pass

- exactly eight `@@COV` records, in order;
- `@@PROBLEM` has nine fields;
- `@@UNIT`, `@@ACTION`, `@@UNRESOLVED` field counts are correct;
- no pipes;
- one `@@END`;
- every action-bearing record has an action record.

The parser should accept this.

## Semantic failures

### 1. Diagnostic reasoning is being turned into actions

`T017`, `T018`, `T019` are neurology assessment/reasoning, not management actions. They are in
`action_bearing_records` and become:

- AV004 assessment of baseline staring;
- AV005 assessment of semiology;
- AV006 differential/diagnostic uncertainty counseling.

That is wrong. These belong in `context` / diagnostic stance, not the action lane.

### 2. CT status is being turned into an action

`T021` is a workup/result-availability statement. AV008 “CT head status acknowledgment” is not an action.

Keep CT in `workup` and `SYNTHESIS_UNRESOLVED`; remove AV008.

### 3. Counterevidence is misused

`PROBLEM P001 counterevidence=T018, T019` describes diagnostic uncertainty, not counterevidence to the
adopted problem claim.

Use `counterevidence=NONE` and put `T018,T019` in problem `evidence` for the diagnostic stance, or in
context.

### 4. T015 is miscategorized as workup

`T015` is treatment, not workup. It can stay in `medication_context` and `action_bearing`; remove it from
`workup_records`.

### 5. Action list should be

Keep:

- AV001 neurology evaluation (if you count consultation/evaluation as an action);
- AV002 ship evaluation/testing;
- AV003 levetiracetam treatment;
- AV007 EEG/MRI needed;
- AV009 levetiracetam continuation;
- AV010 inpatient workup preference;
- AV011 safety/driving counseling.

Remove AV004, AV005, AV006, AV008.

## Prompt fix

Define `action_bearing_records` as **management actions only**:

- tests/procedures;
- medications/treatments;
- consultations;
- admission/disposition;
- precautions;
- counseling/restrictions.

Exclude:

- diagnostic reasoning;
- assessment statements;
- result/status descriptions;
- problem-stance text.

Also add: diagnostic-stance evidence goes in `PROBLEM evidence`, not `counterevidence`.

## What is good

- P002 is gone.
- Baseline comparator is under P001.
- Patient/family history are split.
- Workup states are split.
- No selectors or copied text.
- Source IDs are record-level.

No C. No acceptance.
