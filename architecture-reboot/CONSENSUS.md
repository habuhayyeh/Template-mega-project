# Architecture Reboot V2 — Consensus

## Ratified structural decisions

These points have been explicitly proposed and accepted by both ChatGPT and DeepSeek, or settled by the user.

1. **Production topology is one call / one paste.**
   Chart material and transcription are supplied together; no human carries intermediate artifacts between model calls.

2. **Decompose once and preserve stable source-object identity.**
   Later note construction references objects rather than repeatedly recreating their clinical meaning.

3. **Do not repeatedly reinterpret or destructively route objects.**
   Semantic decisions that affect rendering should not be rediscovered at the final writer.

4. **REASONING is a first-class semantic family.**
   Claim, etiology, qualifier, uncertainty, and adjudication are reasoning roles rather than generic evidence. The exact full top-level kind taxonomy is still open.

5. **Keep semantic structure minimal and evidence-driven.**
   Do not add ontology, relations, stages, or fields without a demonstrated need.

6. **Every render-affecting semantic decision must be explicit before final rendering.**

7. **Render units/operators belong directly in the Case IR.**
   There is no separate model-executed PROJECT stage in the one-call architecture.

8. **Canonical typed operators are first-class for execution.**
   The Doximity B+/operator stress evidence supports explicit operators as the final render boundary.

9. **The operator stress suite validates execution, not selection.**
   Stable 108/108 valid-vs-invalid behavior does not establish that the upstream planner will choose the correct operator/group from raw source material.

10. **Malformed or underspecified render units fail closed.**
    The renderer must not silently repair malformed semantic structure into plausible clinical prose.

11. **Exact diagnostic error labels are secondary.**
    The production invariant is correct valid/invalid classification and fail-closed behavior, not exact error-code wording.

12. **Development modularity and deployment packaging are separate.**
    Source modules may be small and responsibility-specific; deployment should compile to a small Doximity-compatible package.

13. **The deployment build requires conflict linting.**
    It should fail on contradictory rules, duplicate authority over one decision, out-of-scope rules, and untested rules.

14. **Test mode emits an observable Case IR / execution trace.**
    The trace is an auditable artifact, not hidden chain-of-thought and not proof of correctness by itself.

15. **Mechanical validation and semantic fidelity are different jobs.**
    A deterministic checker may verify Case-IR-to-note conformance. Source-to-IR semantic correctness requires a separate semantic audit unless a predicate is genuinely mechanical.

16. **Source temporality and current adoption are separate concepts.**

17. **Current adoption applies to PLAN as well as REASONING when relevant.**
    Historical provenance does not by itself determine whether a recommendation is currently adopted.

18. **Relationship justification uses structured evidence references.**
    Prefer source-span/adjudication references over mandatory free-text rationale.

19. **Source coverage is proposition/span-disposition based, not sentence-count based.**
    The invariant is that clinically meaningful source content does not silently disappear.

20. **Style rules are section-scoped.**
    In particular, final A/P prose uses an impersonal clinical voice; body sections may follow different voice rules.

## Explicitly superseded

- A separate model-executed `PROJECT` stage after Case State is withdrawn.
- A required free-text `basis` field for semantic relations is withdrawn.
- The earlier large relation wish-list is not adopted.
- The Scribe-primary execution topology in ChatGPT Proposal 002 is void under the user's actual Ask-based one-call workflow.

21. **Mechanical checking is Case-IR-to-note only.**
    A deterministic checker verifies unit references, operator validity, unit↔line mapping, allowed transformations, voice, ordering, and accounting. It does not reconstruct semantic units from objects.

22. **Source-to-Case-IR correctness is a separate semantic audit.**
    Kind, role, problem use, operator selection, duplicate/condition/modifier judgments, and other clinical-semantic choices require semantic review unless a specific predicate is genuinely mechanical.

23. **One source proposition keeps one stable object identity.**
    The same object may be reused explicitly by multiple render units/problems. Do not clone a proposition solely to give it multiple problem homes. An optional primary problem may exist for accounting only.

24. **Object accounting is usage/disposition based.**
    Every object must appear in at least one render unit or carry an explicit disposition. Coverage is not defined as assignment to exactly one problem.

25. **Source spans are mechanically bounded, not semantically atomized.**
    A span is a line, utterance, speaker turn, or equivalent boundary preserved by the paste format. One span may yield multiple objects. Every span has at least one disposition, and every object points back to its source span.

## Still open

The following are not yet consensus:

- exact top-level kind taxonomy;
- whether `COURSE` remains a separate kind;
- exact canonical operator vocabulary;
- exact field-level Case IR schema;
- exact semantic-audit instrument/test protocol;
- whether Case IR is visible only in test mode or can be hidden/suppressed in production;
- the concrete paste-layout/provenance contract, which depends on an actual example of how chart material + transcript are pasted into Doximity Ask.

## Next decisive experiment

After the remaining schema questions are resolved, test **Case IR reproducibility** from identical raw source material across fresh Doximity runs.

Compare separately:
- object coverage/identity;
- kind/role;
- problem membership/use;
- render-unit membership;
- operator selection;
- member roles;
- order;
- source-span disposition.

Operator/render-unit agreement is a primary metric because prior failures occurred despite stable discovery of the underlying facts.
