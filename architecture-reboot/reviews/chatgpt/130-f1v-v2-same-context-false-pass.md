# Review 130 — F1V V2 same-context false PASS

## Verdict

**FAIL — F1V V2 executed observably but falsely passed material contract violations.**

This is the first valid test of the V2 validator:
- it emitted a VERIFY line for every F1 item;
- it returned STATUS=PASS;
- therefore the execution mechanics worked.

The validation judgment did not.

## Concrete false-PASS examples

### F002 — question-only refs

F002 cited T153/T154 while claiming no prior seizure history.

- T153 is a clinician question asking whether prior seizures occurred.
- T154 is a clinician question asking about family seizure history.

P1.010 independently supports no prior seizure activity, but T153/T154 are still irrelevant/question-only refs.
V2 incorrectly marked REF/SUPPORT/QUESTION as PASS.

### F005 — wrong supporting ref

F005 cited T036 for no prior similar throat-closing episode.

T036 is only an acknowledgement ("Okay").
The source statement that she had never had that before is T037.

V2 incorrectly marked SUPPORT as PASS.

### F015 — question-only ref in test-result support

F015 cited T133 while saying cruise EKG/testing were normal.

T133 is a clinician question asking whether they found anything.
The answer that "everything was perfect" is T134.

V2 incorrectly marked SUPPORT/QUESTION as PASS.

### F017 — action-state upgrade

F017 states an additional Keppra load was received in ED.

The source sequence is:
- EMS reported prior dose yesterday and another dose today;
- neurology recommended another 1500-mg load;
- that new load was subsequently discontinued.

The source does not establish administration of the new ED 1500-mg load.

V2 nevertheless marked ACTION=PASS.

### F021 — prospective action retained as FACT

F021 is an ED planned-workup action represented as FACT.

F1's own action boundary says prospective/recommended/planned actions belong to File 2, except where action state is needed purely for chronology.

V2 marked ACTION=PASS and BOUNDARY=PASS.

## Interpretation

The validator prompt is not failing because its checks are missing.

It is failing because, in the same Ask context immediately after F1 generation, GPT-4o is insufficiently adversarial toward its own preceding output.

The mandatory ledger improved observability but not independence.

## Decision

Do **not** expand F1V V2 further yet.

Per D-044 escalation rule, next experiment is:

> run the unchanged F1V V2 in a **fresh Doximity Ask session** against:
> 1. original Scribe V2.2 packet;
> 2. canonical File 1 contract;
> 3. exact F1 output from the failed same-context run;
> 4. current F1V V2.

This deliberately gives the validator the output because a fresh session cannot inherit the previous Ask state.

## Pass criterion for fresh-session experiment

At minimum, the validator must flag:
- T153/T154 question-only/irrelevant use;
- T036 wrong support for prior similar symptom;
- T133 question-only support;
- F017 Keppra action-state overstatement;
- F021 prospective action boundary.

If fresh-session F1V still misses these, abandon self-validator reliance for this layer and reconsider validator architecture rather than adding more same-model prompt rules.
