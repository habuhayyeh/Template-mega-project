# SUPERSEDED — DO NOT RUN

Superseded by D-037 modular Ask-function design. Retained only as design history.

# First Doximity Ask P/N run

## Case

Use the original controlled seizure-like-event case because:
- its exact raw transcript/prechart is available for later audit;
- a V2.2 Scribe packet already exists;
- the final USF General Neurology H&P/Consult Note template is known.

Do not commit case content or identifiers to the repository.

## Isolation

Run N and P in separate fresh Doximity Ask sessions.

Run **N first, then P**. This prevents the no-contract baseline from being contaminated by exposure to the semantic contract if Doximity retains any hidden session state.

Use the same Ask model/settings, the exact same packet bytes, and the exact same template bytes in both sessions.

## Condition N

Provide:
- COMMON-TASK.md instructions;
- Scribe V2.2 packet;
- final USF template;
- N-PROMPT.md.

Do not provide Ask Semantic Contract V1.

Capture the entire output unchanged.

## Condition P

Provide:
- COMMON-TASK.md instructions;
- the identical Scribe V2.2 packet;
- Ask Semantic Contract V1;
- the identical final USF template;
- P-PROMPT.md.

Capture the entire output unchanged.

## After both runs

Return both outputs to ChatGPT.

ChatGPT will score only:
1. problem identity/containment;
2. current stance/role;
3. source/uncertainty/relation fidelity;
4. final-note adequacy/template fit.

Failures are localized to Scribe, Ask contract, realization, or template.

Do not tune between N and P.
Do not correct either output before returning it.
