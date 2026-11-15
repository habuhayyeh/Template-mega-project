# ChatGPT pre-sync failure analysis — frozen 11-submodule architecture

**Purpose:** independently map the demonstrated failure modes of the prior architecture onto the current frozen architecture before reading DeepSeek's next proposal.

This is a failure-oriented review, not a redesign.

The historical lessons used here include:
- Doximity section-routing instability across identical inputs;
- schema non-compliance despite prior successful runs;
- non-local prompt sensitivity;
- old 05 merge/split drift;
- duplicate rendering and duplicate suppression drift;
- conditional-management split/merge drift;
- historical/current provenance and adoption errors;
- missing required content such as seizure precautions;
- writer-level voice drift and source-person leakage;
- stable bad output from incomplete operator payload;
- overlapping error taxonomy;
- final-writer repair of malformed structure.

---

# 0. Cross-cutting failure pattern from the old architecture

The old architecture repeatedly failed in seven systemic ways:

1. **Repeated semantic reinterpretation**
   - later stages rediscovered grouping, relevance, duplication, condition scope, section placement, and wording.
   - consequence: the same source produced different structures across runs.

2. **Prompt-rule accumulation and contradiction**
   - adding one clause fixed one object and moved another.
   - explicit example: a prior-record rule conflicted with a WORKUP rule and changed O51 routing.

3. **Silent repair instead of explicit failure**
   - malformed or incomplete inputs were turned into plausible prose.
   - this hid upstream representation defects.

4. **Semantic and structural validation were conflated**
   - format validity could pass while clinical meaning was wrong.
   - conversely, a semantically reasonable output could violate schema.

5. **Coverage and relevance were conflated**
   - content disappeared because "not selected" was indistinguishable from "never extracted" or "misrouted."

6. **The final writer had too much freedom**
   - it decided merge/split, duplicate suppression, condition composition, wording, voice, and order simultaneously.

7. **One good run was easy to over-trust**
   - instability only became visible across repeated fresh runs.

The new architecture should be judged by whether each submodule contains these failure modes rather than merely relocating them.

---

# 1. I1 Source Map

## Likely failures
- two pasted sources merged into one;
- one source split into several falsely;
- current note misclassified as prior note or vice versa;
- transcript vs chart material confused;
- source order changed;
- unlabeled material guessed instead of preserved as uncertain.

## Historical analogue
The old system repeatedly confused provenance-sensitive content and historical/current material. If source identity is wrong at I1, every later provenance/adoption decision can be internally consistent yet clinically wrong.

## Defenses
- explicit pasted headings/labels dominate classification;
- preserve raw source boundaries and order;
- use UNLABELLED/UNKNOWN rather than guess;
- source classification does not decide authority/relevance.

## Detect
Mechanical:
- every raw character/block covered once;
- no overlap/gap;
- source order preserved.

Semantic:
- source-family classification audit on synthetic fixtures.

## Failure behavior
If family cannot be supported:
> preserve source block as UNLABELLED; do not infer.

Do not let I2/I3 reinterpret the source family later.

---

# 2. I2 Span Registry

## Likely failures
- semantic splitting disguised as "span cutting";
- two speaker turns merged;
- clinically meaningful text dropped between spans;
- unstable span boundaries across runs;
- later renumbering breaks provenance.

## Historical analogue
The old pipeline repeatedly made semantic decisions during routing/decomposition that later stages treated as fixed facts. If I2 semantically atomizes, instability begins before object extraction.

## Defenses
- approved mechanical boundaries only;
- line/utterance/turn/explicit fragment boundaries;
- uncuttable block remains one flagged span;
- stable position-based identity/order.

## Detect
Mechanical:
- spans contiguous where applicable;
- ordered;
- non-overlapping;
- complete source coverage;
- every span points to one source.

## Failure behavior
If safe segmentation is impossible:
> one larger span + flag.

Never "solve" ambiguity by semantic splitting.

---

# 3. I3 Object Extraction

## Likely failures
- proposition omitted;
- two propositions merged;
- one proposition unnecessarily duplicated;
- hedge/negation/certainty removed;
- new clinical word introduced;
- "cleaner" note language replaces source meaning;
- object count/boundaries drift across runs;
- relevance judgment contaminates extraction.

## Historical analogue
Examples of invented/normalized content such as a source being converted into a stronger statement; downstream disappearance of facts; reasoning flattened or lost.

## Defenses
- high-recall extraction;
- one independently useful proposition per object;
- exact source anchor;
- preserve negation, uncertainty, attribution, numbers;
- lexically conservative source-faithful normalization only;
- closed morphology/abbreviation/source-preserving normalization map;
- no note relevance here.

## Detect
Mechanical/hybrid:
- every object has a valid span anchor;
- lexical-support guard on content tokens after closed normalization;
- every clinical span has object/disposition accounting.

Semantic:
- oracle review of proposition completeness and boundaries;
- repeated-run object-set comparison.

## Failure behavior
Unsupported object candidate:
> reject candidate + EXTRACTION_ERROR / UNRESOLVED.

Never convert extraction failure into NOT_CLINICAL.

---

# 4. I4 Source Annotation

## Likely failures
- source date treated as event date;
- prior diagnosis treated as current adoption;
- speaker guessed;
- current clinician reasoning attributed to prior clinician or vice versa;
- provenance invented from context;
- historical medication event mislabeled as current regimen.

## Historical analogue
O53 timing/provenance confusion; prior recommendations leaking into current plan; active vs stopped medication routing failures.

## Defenses
- source date, event time, source temporality, speaker, and current adoption remain distinct;
- only explicit source-grounded metadata here;
- encounter-level adoption remains S2;
- absent metadata stays absent.

## Detect
Mechanical:
- valid IDs/dates/enums;
- explicit speaker copied exactly when present.

Semantic:
- support of inferred source family/temporality/stance.

## Failure behavior
If metadata is unsupported:
> leave absent / unresolved.

Never infer event date from provenance date.

---

# 5. S1 Problem Model

## Likely failures
- too many problems because every diagnosis becomes a block;
- too few problems because distinct neurologic claims are collapsed;
- wrong claim chosen;
- prior diagnosis promoted to current claim;
- chronic neurologic problem gets a separate A/P block without encounter management;
- non-neurologic problem becomes co-equal despite only contextual relevance;
- problem order drifts.

## Historical analogue
The old A/P architecture sometimes organized around source categories rather than the neurologist's actual claims, and chronic/background material could leak into active A/P.

## Defenses
- neurologic claims are organizing unit;
- group by clinical subject, not object count;
- prior diagnoses remain attributed unless adopted;
- chronic separate block requires source-grounded encounter-level management/reasoning;
- centralized ordering contract later, not ad hoc prose sorting.

## Detect
Semantic audit:
- problem count;
- claim correctness;
- problem granularity;
- chronic-block justification.

Mechanical shell:
- each retained problem has required claim representation;
- no duplicate problem IDs;
- explicit order key.

## Failure behavior
If no defensible claim:
> unresolved problem model / fail STRUCTURE rather than inventing a diagnosis.

Do not create a problem from medication class alone.

---

# 6. S2 Semantic Adjudication

## Likely failures
- duplicate identity drift: same vs related vs distinct;
- conflicting numeric/time facts collapsed as duplicates;
- modifier attached to wrong head;
- condition attached to wrong action;
- historical diagnosis incorrectly adopted;
- current clinician reasoning flattened into fact/plan;
- reasoned conversational statement loses its missing semantic payload;
- uncertainty converted into certainty.

## Historical analogue
CT merge/split drift; infarct duplicate drift; MRI hedge duplication; apixaban hold/resume split/merge; historical/current management confusion.

## Defenses
- closed typed relation/status vocabulary;
- preserve original object text/identity;
- safe mechanical duplicate subset only;
- ambiguous semantic equivalence may remain unresolved;
- adoption requires source support;
- no drug-class heuristics;
- condition/modifier links explicit.

## Detect
Mechanical:
- relation shape;
- one canonical per duplicate group;
- no illegal membership;
- valid object IDs.

Semantic:
- actual duplicate identity;
- modifier/condition correctness;
- adoption correctness;
- reasoning-role correctness.

## Failure behavior
If relation cannot be justified:
> unresolved / conflict.

Do not force a simplifying relation merely to make S4 easier.

---

# 7. S3 Content Selection & Problem Use

## Likely failures
- clinically important object silently dropped;
- irrelevant object retained because it is medically interesting;
- non-neurologic information overrepresented;
- object cloned to serve two problems;
- cross-problem reuse omitted;
- prior recommendation selected as current plan;
- background meds/current medical issues flood A/P;
- source coverage mistaken for note inclusion.

## Historical analogue
Objects vanished between stages; body/AP routing varied; amlodipine/atorvastatin/fluid restriction could appear in neurologic A/P despite weak relevance; chronic concern and driving preference landed in wrong buckets.

## Defenses
- every object must be retained for >=1 use or explicitly dispositioned;
- neurologic-claim relevance policy;
- same stable object reused across problems;
- omission reason explicit;
- duplicate coverage is not source deletion;
- no section/operator decision yet.

## Detect
Mechanical:
- total object accounting;
- no orphan objects;
- no cloned source proposition for reuse.

Semantic:
- relevance;
- problem fit;
- omission appropriateness.

## Failure behavior
If relevance/problem fit is uncertain:
> explicit unresolved/review disposition rather than silent drop.

---

# 8. S4 Note Blueprint / Render-Unit Compilation

## Likely failures
- wrong section assignment;
- wrong operator selected;
- duplicate object rendered twice in same section/problem;
- a retained plan/reasoning item never receives a unit;
- unsupported zero-member unit created;
- condition split from action;
- merge/split drift reappears at unit construction;
- malformed unit nevertheless passed to R1;
- order inconsistent or recalculated later;
- standing item omitted despite satisfied trigger;
- structurally valid Case IR that is semantically wrong.

## Historical analogue
This is where most old 03/04/05/06 failure classes converge: merge/split drift, duplicate bullets, missing seizure precautions, routing instability, apixaban split vs merge, MRI hedge duplication, ordering changes.

## Defenses
- typed unit schema;
- explicit HEAD/MODIFIER/CONDITION/COVERED/etc.;
- explicit operator and order;
- centralized ordering contract;
- completeness checks;
- per-section+problem object uniqueness;
- supported-unit rules;
- standing items closed and trigger-based;
- fail closed on type error.

## Detect
Mechanical:
- typecheck;
- member IDs exist;
- roles permitted;
- completeness;
- section list/order;
- uniqueness;
- zero-member standing-item rule.

Semantic:
- correct section;
- correct operator;
- correct grouping;
- correct rhetorical class.

## Failure behavior
Malformed/underspecified:
> no render; CONTRACT_ERROR / STRUCTURE_ERROR.

Do not let R1 repair.

---

# 9. R1 Unit Realization

## Likely failures
- wording drift;
- incomplete proposition rendered as grammatical nonsense;
- first-person leakage into A/P;
- patient-address leakage ("your old stroke");
- source text consulted to repair unit;
- conditional scope altered;
- covered member independently rendered;
- malformed unit silently repaired;
- operator-fixed wording extended beyond payload.

## Historical analogue
"The MRI to show."; "We'll see what the MRI shows."; "I am not starting..."; "your old stroke"; apixaban hold/resume variations; duplicate CT/infarct lines.

## Defenses
- canonical operators;
- no raw-source access;
- exact operator payload requirements;
- section-scoped voice;
- output cardinality fixed;
- only object payload + operator-fixed text + allowed surface transforms;
- fail closed.

## Detect
Mechanical-heavy:
- one output per unit as required;
- no unlicensed content;
- line-to-unit mapping;
- covered suppression;
- voice rules;
- order.

## Failure behavior
Invalid unit:
> CONTRACT_ERROR, not prose.

Stable wrong output:
> operator/schema defect upstream; do not loosen prose.

---

# 10. R2 Section Composition

## Likely failures
- units reordered to improve narrative;
- one unit dropped as redundant;
- adjacent units merged into a new proposition;
- new causal/temporal connective invented;
- uncertainty altered;
- pronoun creates wrong referent;
- A/P accidentally converted into prose;
- "polish" changes meaning.

## Historical analogue
The old writer merged/split clinically meaningful content while trying to make prose natural. Non-local stylistic freedom became semantic freedom.

## Defenses
- only prose-enabled sections;
- A/P bypass;
- preserve unit order and payload;
- local punctuation/whitespace/minimal grammatical continuity only;
- no causal/temporal connective unless represented;
- conservative pronoun use;
- fallback to unit-per-line if safe composition cannot be maintained.

## Detect
Mechanical:
- all unit payloads present;
- order preserved.

Semantic:
- no new relation/meaning introduced.

## Failure behavior
Unsafe composition:
> fallback to faithful uncomposed output, record fallback.

Never "improve" semantics.

---

# 11. R3 Note Assembly

## Likely failures
- section omitted;
- extra section added;
- section order changed;
- heading changed;
- conversational wrapper before/after note;
- final global polish rewrites content;
- empty section emitted contrary to IR;
- A/P/body content moved across headings.

## Historical analogue
Schema/wrapper non-compliance and section-routing/assembly drift.

## Defenses
- IR-specified ordered section list;
- fixed headings/furniture;
- no content editing;
- no global polish;
- no output outside note envelope.

## Detect
Mechanical:
- section order exactly equals IR;
- headings exact;
- no extra/missing section;
- no extra text before/after note;
- section payload bijection.

## Failure behavior
Assembly mismatch:
> refuse/fail rather than rewrite.

---

# 12. Cross-module failure modes that require explicit safeguards

## A. Contract contradiction
Historical example:
a new provenance rule contradicted the existing WORKUP rule and moved O51.

Defense:
- BUILD conflict lint;
- one decision owner;
- centralized contracts for ordering/style/standing items;
- no duplicate policy definitions across modules.

## B. Non-local prompt sensitivity
A prose fix can move unrelated decisions.

Defense:
- avoid large global prose exception lists;
- typed outputs at decision-complete boundaries;
- regression suite across all known cases after any rule change.

## C. "Helpful" downstream repair
Historical pattern:
later writer guesses missing semantics.

Defense:
- every module has explicit fail behavior;
- downstream module must not read broader context to rescue upstream structure.

## D. Semantic correctness vs mechanical correctness
A perfect schema can encode the wrong clinical judgment.

Defense:
- MECHANICAL CHECK and SEMANTIC AUDIT remain separate;
- E1 measures semantic reproducibility, not just validator pass rate.

## E. One-run optimism
Defense:
- repeated fresh-conversation runs;
- compare object set, adjudication, use map, units/operators, rendered note separately;
- never promote a hand-picked good run as proof.

## F. Error taxonomy overlap
Defense:
- small mutually exclusive error classes or generic CONTRACT_ERROR;
- behavioral fail-closed property matters more than exact error label.

---

# 13. What this suggests for the next concrete implementation layer

Every submodule specification should include four things, not just instructions:

1. **DO**
2. **AVOID**
3. **DETECT**
4. **FAILURE BEHAVIOR**

The old architecture usually had only #1 and #2.

The new design should treat #3 and #4 as first-class because many prior failures were not caused by lack of instruction; they were caused by the absence of an observable failure state.

The question for every implementation rule should be:

> If Doximity violates or cannot satisfy this rule, how will we know, and what prevents the next submodule from silently compensating?
