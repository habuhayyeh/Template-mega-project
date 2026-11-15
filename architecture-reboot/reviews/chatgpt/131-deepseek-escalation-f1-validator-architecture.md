# Escalation 131 — F1/F1V validator architecture

## Request to DeepSeek

Treat this as an **architecture escalation**, not a prompt-edit review.

We now have empirical evidence that Doximity GPT-4o can generate a clinically useful F1 reconciliation
handoff, but its same-context companion validator can execute all requested checks and still return a
false PASS.

Please independently diagnose the failure mechanism and recommend the smallest architecture that is likely
to work in production.

Do **not** assume ChatGPT's current "fresh Ask session" hypothesis is correct.

## Current runtime

```text
SCRIBE_EVIDENCE_V2_2
  -> F1 Reconciled Evidence
  -> F1V Reconciled Evidence Validator
  -> F2 Action State
  -> ...
```

Scribe remains the canonical evidence store.

F1 emits compact source-ID-backed FACT / SOURCE_REASONING / UNRESOLVED records.

F1V is intended as a runtime reliability guard, not acceptance evidence.

## Empirical sequence

### 1. Global atomic F1
- exploded to ~175 objects;
- truncated before packet completion.
- Result: abandoned global atomicization.

### 2. Lazy reconciliation F1
- completed compactly;
- useful clinical grouping;
- bounded source-reference/action-state defects remained.

### 3. F1V V1, same Ask context
- validator visibly executed;
- returned PASS/REPAIRED;
- still missed obvious defects.

### 4. F1V V2, same Ask context
V2 forced one VERIFY line for every F1 item:
- REF
- SUPPORT
- QUESTION
- ACTION
- ATTR
- BOUNDARY
- SEPARABILITY

It emitted the full ledger and still returned STATUS=PASS.

Known false-PASS examples:

1. **Question-only refs**
   - F002 cited T153/T154 while asserting no prior seizure history.
   - Those T records are clinician questions, not answers.
   - P1.010 independently supports the no-prior-seizure statement, but the cited question refs remain invalid.
   - Validator marked QUESTION=PASS and SUPPORT=PASS.

2. **Wrong local support**
   - F005 cited T036 for "no prior similar throat-closing episode."
   - T036 is only "Okay."
   - T037 contains the actual "never had that before" statement.
   - Validator marked SUPPORT=PASS.

3. **Question-only test-result support**
   - F015 cited T133 to support normal ship testing.
   - T133 is a clinician question.
   - T134 is the answer that "everything was perfect."
   - Validator marked SUPPORT=PASS.

4. **Action-state upgrade**
   - F017 said an additional ED Keppra load was received.
   - Sources establish prior reported doses, neurology recommendation for a new 1500-mg load, then discontinuation.
   - They do not establish administration of that new ED load.
   - Validator marked ACTION=PASS.

5. **Boundary leak**
   - F021 retained prospective ED planned workup as FACT despite F1 contract assigning prospective action-state reconciliation to F2.
   - Validator marked ACTION=PASS and BOUNDARY=PASS.

## Current interpretation from ChatGPT

Tentative hypothesis:
- same-context self-validation is anchored to the immediately preceding F1 output;
- forcing a ledger improves observability but not independence;
- next experiment would be unchanged F1V V2 in a fresh Ask session.

This is **not accepted yet**. Challenge it.

## Questions for DeepSeek

Please answer these directly.

### Q1 — Root cause
What is the most likely failure mechanism?
Distinguish among:
- same-context anchoring/self-confirmation;
- validator task overload;
- weak source-dereferencing behavior;
- schema-induced superficial checking;
- F1/F1V responsibility overlap;
- GPT-4o limitation;
- another mechanism.

### Q2 — Fresh-session hypothesis
Is a fresh Ask session a sound next experiment, or is it unlikely to materially improve validation?

### Q3 — Validator architecture
Which architecture should we prefer?

A. F1 -> F1V same context  
B. F1 -> F1V fresh context  
C. F1 -> deterministic/mechanical validator -> semantic validator only for ambiguous failures  
D. F1 emits its own evidence ledger/proof obligations, validator checks only deltas  
E. two independent generation passes compared against each other  
F. remove F1V and simplify F1 further  
G. another architecture

Choose and justify.

### Q4 — What should be deterministic?
Which checks can/should be made mechanical rather than LLM semantic?
Examples:
- ref existence;
- T/P namespace validity;
- duplicate IDs;
- question-record detection;
- action-state lexical transitions;
- every ref cited in source packet.

Do not propose deterministic checks that require unsupported clinical interpretation.

### Q5 — What should remain semantic?
What genuinely requires an LLM?
Examples:
- whether a ref supports a clause;
- source reasoning vs fact;
- downstream separability;
- action-state meaning when wording is ambiguous.

### Q6 — F1 responsibility
Are we asking F1 to do too much?
Should F1 become narrower so that fewer things need validation?

### Q7 — Production implications
Given Doximity constraints, what is the **smallest practical runtime** likely to be robust enough without
turning into another over-engineered pipeline?

## Constraints

- Do not reintroduce global atomicization.
- Do not assume validators are acceptance evidence.
- Do not add a new mechanism merely because it is theoretically cleaner.
- Favor the smallest empirically testable design.
- The user explicitly wants to avoid architecture bureaucracy and excessive modularity.
- Patient/source text is not committed to GitHub; reason from the failure examples above and repository contracts.
