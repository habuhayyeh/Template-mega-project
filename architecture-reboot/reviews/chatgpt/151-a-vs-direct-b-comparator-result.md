# Review 151 — A vs direct-B comparator result

## Verdict

**INCONCLUSIVE by the predeclared comparator rule.**

Do not retire A yet.
Do not accept current A as necessary either.

The four-run comparator localized the disagreement:

- A->B preserves body/nonproblem evidence that direct-B's current output shape has nowhere to carry.
- A does **not** reliably improve source-pointer fidelity.
- Direct-B materially reduces representation burden and generally produces cleaner clinical synthesis.
- Both arms have blocking failures, but of different kinds.

This is exactly the comparator's predefined inconclusive condition.

## Runs

Same clean SCRIBE_EVIDENCE_V2_2 packet used in all four fresh sessions:

- A1 — Scribe -> A -> B
- A2 — Scribe -> A -> B
- D1 — Scribe -> direct-B
- D2 — Scribe -> direct-B

No patient-identifying source text is reproduced here.

## 1. Source pointer fidelity — both arms fail

### A1

At least one clear neighboring-record pointer error:
- a negative motor observation was attached to the clinician question record rather than the following answer record.

Additional exact-selector failures included:
- nonliteral pronoun substitution;
- noncontiguous selection from a longer source record.

### A2

Multiple clear neighboring-record pointer errors:
- one action/event statement attached to the following clinician question record;
- one baseline comparator statement attached to a different adjacent record;
- one clinician interpretation attached to the subsequent medication-management record.

Additional same-record nonliteral/noncontiguous selector failures occurred.

### D1

One clear neighboring-record pointer error:
- a negative motor observation was attached to the clinician question record rather than the answer record.

Several evidence strings were noncontiguous excerpts from the correct record.

### D2

Multiple neighboring-record pointer errors:
- motor-negative evidence attached to question records;
- baseline comparator evidence attached to the clinician question rather than the collateral answer;
- one event-description fragment attached to the wrong source turn.

One medication selector also changed the source spelling rather than copying literally.

### Conclusion

A is **not** earning its place by improving pointer fidelity.

Direct-B is not yet pointer-safe enough to retire A under the current rule.

## 2. Clinical coverage — A passes preservation; direct-B output shape fails

The target-note coverage contract requires preservation of:
- no prior seizure history;
- family seizure history;
- supplements/medication context;
- ED exam;
- outside reported labs;
- baseline comparator;
- event details;
- diagnostic stance;
- management actions.

A1/A2 preserve these body/nonproblem items in the A handoff even when B does not use them as problem evidence.

Current direct-B output has only:
- PROBLEM;
- ACTION_VIEW;
- SYNTHESIS_UNRESOLVED.

Therefore it has no stable home for clinically relevant nonproblem/body evidence.

Observed:
- D1 omitted at least family seizure history, supplement context, and no-prior-seizure history from the returned synthesis.
- D2 likewise omitted those items and also did not preserve the ED exam in a stable output field.

This is a **blocking direct-B coverage failure**, but it is also an output-contract mismatch rather than proof that a separate A stage is clinically necessary.

## 3. Action coverage — direct-B is stronger, but not fully reproducible

Both A runs retained the main target-note actions.

Direct-B represented actions more directly and with much lower representation burden.

However:
- D1 omitted one additional outside-testing action concept that D2 preserved.
- D1 and D2 differed in whether they preserved the "do not feel strongly about giving additional IV Keppra now" action.

The predeclared normalized target-note action list was mostly preserved, but direct-B is not perfectly reproducible across all source-local actions.

## 4. Problem architecture — all four substantially pass

All four runs produced:
- one PRIMARY current event problem;
- no separate BACKGROUND problem for baseline zoning-out spells;
- baseline spells treated as comparator/background evidence rather than an independent disease block.

This validates the counterfactual problem-threshold patch.

## 5. Diagnostic stance — direct-B is cleaner

All four preserve uncertainty.

Direct-B is generally more concise and closer to the desired current Neurology stance:
- not clearly epileptic;
- PNES considered/suspected but not established;
- epileptic seizure remains under evaluation.

A2 pulled an ED differential item into the main diagnostic stance that is source-supported but not central to the current Neurology formulation.

No architecture decision should rest on this alone, but direct-B shows no synthesis-quality disadvantage here.

## 6. Source-qualified management wording

Both arms preserve most major action-state distinctions.

A->B showed at least one important boundary leak:
- "shared decision" language appeared in B even though the relevant A evidence did not contain the downstream shared-decision source record.

A1 also reconstructed CT completion/review status in B from an A action representation that did not itself preserve that complete action state.

Direct-B avoided that specific A-omission/repair problem because it operated directly on the packet.

Direct-B still had smaller wording/citation defects, including one run attaching "will be done tonight or tomorrow" to a selector that only supported "EEG needed."

## 7. Representation burden

Observed outputs:

- A1: ~29.3k characters, 858 lines, 86 intermediate A records.
- A2: ~34.6k characters, 852 lines, 81 intermediate A records.
- D1: ~10.9k characters, 212 lines.
- D2: ~14.9k characters, 207 lines.

Direct-B reduces returned representation by roughly 50–70% and eliminates 81–86 intermediate semantic/action records.

This is a large burden advantage, but burden is nonblocking by contract.

## Comparator decision

Per the predeclared rule:

- A->B has blocking pointer-fidelity failures.
- direct-B has blocking pointer-fidelity failures.
- direct-B also has blocking body/nonproblem coverage loss because its current output shape lacks a preservation home.
- the arms therefore fail in different material ways.

**Result: INCONCLUSIVE.**

Do not average these failures.
Do not declare A necessary.
Do not retire A yet.

## Smallest targeted follow-up

The next test should isolate the one unresolved responsibility:

> Can direct-B preserve clinically necessary nonproblem/body evidence without recreating A?

Use the already-planned B decision-complete output extension rather than another ingestion stage.

Add compact B `CLINICAL_UNIT` output for source-backed units such as:
- current_event;
- baseline_comparator;
- neuro_history;
- medication_context;
- exam;
- workup;
- context.

Each unit must carry:
- exact source record;
- exact contiguous selector;
- chronology when clinically needed;
- relation to problem when applicable.

No polarity/certainty registry.
No source-local span ledger.
No new stage.
No validator.
No final-note section decisions.

Then run direct-B twice on the same clean packet.

Blocking question:
- does the extended direct-B preserve the required body evidence and maintain/improve pointer fidelity while retaining the burden advantage?

If yes, retire A.
If no, identify the exact preservation function A uniquely supplies.

## Do not advance C yet

C remains blocked until:
1. A necessity is decided;
2. B output is decision-complete;
3. B emits reconciled clinical units needed for chronology/body preservation.
