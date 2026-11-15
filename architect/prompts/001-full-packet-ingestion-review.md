# Prompt for the note-writing expert — full-packet ingestion result

Use this with the expert who proposed the Evidence Ledger ingestion model. Attach the current ingestion
contract, the frozen Scribe packet, and the A output. Do not attach patient identifiers.

---

You proposed the Evidence Ledger ingestion model: source-grounded semantic spans, not atomic facts, with
classes E/H/O/R/F/A/C/Q, source views, uncertainty and refs.

We ran it on the full frozen packet. It completed. It did not truncate. But it failed the predeclared
material-distinction oracle on semantics. I need your opinion on whether this is an ingestion task
overload or a field-contract weakness inside an otherwise scalable ingestion pass.

## What A is

A is the ingestion pass. It reads the canonical Scribe V2.2 packet and emits a compact Evidence Ledger.
It is not supposed to reconcile sources, decide problems, assign note sections, diagnose, or write prose.

## Result

- 16 units
- 7 actions
- 6 unresolved
- output ~18,950 bytes vs ~34,700-byte packet
- no truncation
- Wednesday/Thursday/baseline staring remained distinct
- future workup did not become results

So the failure is not context size or atomic explosion. It is semantic fidelity.

## Oracle score

- PASS 39
- FAIL 9
- N/A 3

Fatal or material failures:

1. **Attribution inversion**
   - The Scribe packet explicitly identifies one speaker as the patient's mother.
   - A labeled that speaker's recall as “patient recall.”
   - Another unit degraded the same speaker to “patient/family.”

2. **Action-state normalization**
   - A source line “Plan: CT ... basic labs ...” became `decision=ordered`.
   - A source statement “started on Keppra drip” became `decision=ordered` instead of reported
     execution.
   - One action object merged prior Keppra administration, a cruise-ship drip, the current ED load
     discussion, and different actors across time.
   - An admission recommendation acquired `execution=pending` by inference.
   - “Keep on Keppra for now” survived in free text but not as a structured action.

3. **Question-domain separation**
   - Patient prior-seizure history and family seizure history were combined into one unit.

4. **Absence became negative**
   - Source said smoking status “not on file.”
   - A said tobacco was denied.

5. **Mixed assertion types**
   - One `kind=diagnosis` unit bundled the diagnostic stance and the continued-Keppra management
     decision.

6. **Material coverage gap**
   - The ED initial differential was not represented.
   - The current continue-Keppra action was not structured.

## My current interpretation

I do not think this is scale overload. The pass completed compactly. The errors look like field-contract
weakness:

- speaker identity/role is not explicitly separated from the assertion;
- action state is too coarse and allows cross-time merging;
- unit boundaries permit mixed assertion types and mixed patient/family domains;
- “not on file” is not a first-class absence state;
- coverage is judged by completion, not by material distinctions.

But I want your clinical judgment, not mine.

## Questions

1. **Overload or contract weakness?**
   Is A trying to do too much in one pass, or are the fields/boundaries underspecified? Be specific.

2. **Should A split?**
   If yes, where exactly:
   - A1 source-semantic extraction and A2 reconciliation?
   - a separate action-state lane/pass?
   - a separate attribution/source-view pass?
   If no, what minimal contract change prevents these failures?

3. **Attribution**
   What is the minimum representation that prevents “mother” becoming “patient” without turning every
   speaker label into a separate object? Should role be a field on the source view, the unit, or both?

4. **Action state**
   What is the smallest action schema that preserves:
   - decision vs execution vs response vs result;
   - actor;
   - setting/time;
   - one action episode vs a drug’s whole history;
   - “started on drip” vs “plan: start”;
   - “keep on Keppra for now”?
   Do not give a theoretical action ontology; give the fields and boundary rule you would actually use.

5. **Unit boundaries**
   When should one unit split?
   - patient history vs family history;
   - diagnostic stance vs management decision;
   - one event vs a trajectory;
   - one action episode vs a drug course.
   Give a simple boundary rule that GPT-4o can apply.

6. **Absence**
   How should “not on file,” “not asked,” “not performed,” “unavailable,” and “denied” be represented so
   they never collapse into one another?

7. **Coverage**
   What material distinctions must the ledger preserve even if they never become problems or note
   sections? How should we test coverage without building another validator?

8. **What not to do**
   Where would a fix make things worse by recreating atomic facts, a topic index, a second fact corpus,
   or a same-model audit?

## Deliverable

A short memo:

1. verdict: overload vs contract weakness;
2. the minimum field/boundary changes;
3. whether to split A, and where;
4. the action schema and unit-boundary rule you would use;
5. the first three test cases that would catch these failures;
6. what you would explicitly not add.

No need to write note prose. I need the ingestion contract judgment.
