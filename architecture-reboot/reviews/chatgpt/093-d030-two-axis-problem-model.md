# ChatGPT review 093 — D-030 two-axis neurologic problem model

## Signer policy

The signer supplied a general rule that supersedes the earlier one-dimensional treatment of chronic
neurologic diagnoses.

### Axis 1 — encounter role

Every neurologic problem represented in the A/P is one of:

- `PRIMARY` — actively evaluated/managed now, or an active neurologic disorder independently driving
  current neurologic assessment/management;
- `BACKGROUND` — established or suspected neurologic disease/finding that is not itself a primary
  current problem.

A background neurologic problem still receives compact A/P representation when useful, including
disease, residual deficit/course, treatment, and follow-up when supplied.

Historical relevance alone does not make a problem PRIMARY.

### Axis 2 — causal relationship to a current syndrome

Causal relation is separately adjudicated:

- `LIKELY`
- `POSSIBLE`
- `UNLIKELY`

with relation noun chosen clinically from `CONTRIBUTOR`, `ETIOLOGY`, `MECHANISM`, or `CAUSE`.

These axes are independent. BACKGROUND disease may be a LIKELY contributor to a PRIMARY syndrome.

### Historical disease vs active residual deficit

When prior disease contributes through a persistent deficit, the causal edge should point to the
current acting deficit/mechanism, not merely the historical disease event.

Preferred:
> chronic right-sided weakness from prior L MCA stroke contributes to falls

Not:
> L MCA stroke contributes to falls

unless the disease process itself is the intended causal entity.

No causal link is inferred from historical presence alone.

## Architecture assessment

This does **not** require changing the 11-module architecture or reallocating decision ownership.

The existing owners are sufficient:

- **I3/I4** preserve separate disease and residual-deficit propositions and source state.
- **S2** already owns semantic relations and is the correct owner for causal relation type/strength.
- **S3** already owns problem use/selection and is the correct owner for encounter role
  `PRIMARY/BACKGROUND`.
- **S4** consumes the selected role/relation state to order and compile a compact background block vs
  fuller primary block.
- **RENDER** remains semantically weak.

However, current contracts/fixtures do not explicitly encode both axes. This is a **bounded interface /
contract extension**, not an architecture redesign.

## Required contract work

1. Add an S3 per-rendered-problem `encounter_role: PRIMARY|BACKGROUND`.
2. Require S3 to preserve a compact BACKGROUND problem when governing policy requires it, even without
   current management.
3. Extend S2 semantic relation payload to carry:
   - relation noun/type;
   - strength `LIKELY|POSSIBLE|UNLIKELY`;
   - source-grounded support;
   - actor/cause object that may be a residual deficit rather than historical disease label.
4. S4 projection must carry `encounter_role` and the selected causal relations needed for rendering.
5. Ordering/blueprint behavior should preserve greater prominence for PRIMARY problems; BACKGROUND
   problems remain condensed unless independently active.
6. Update CASE-01 truth:
   - falls = PRIMARY;
   - prior L MCA infarct = BACKGROUND;
   - no causal contribution from chronic weakness to falls unless the current source explicitly
     supports/formulates that relation.
7. Update predicates/seeds so they test:
   - primary/background separation;
   - no historical->primary promotion by relevance alone;
   - no causal inference from history alone;
   - correct residual-deficit vs disease causal subject;
   - preservation of likely/possible/unlikely strength.

## Gate 0 reference consequences

Fresh F-2 Packet 1 remains SILENT, but rationale is refined: both deserve A/P representation, with falls
PRIMARY and old infarct BACKGROUND.

Fresh F-2 Packet 2 is SILENT: historical stroke/residual weakness are not newly adopted current claims
merely because prior records contain them, while the current falls are adopted.

Do not continue signer packet collection against the current CASE-01 contract until D-030 contract
fields are incorporated, because packet identities/semantic truth may change.

## NEXT

DeepSeek drafts the smallest D-030 contract extension within existing S2/S3/S4 ownership, updates the
CASE-01 source contract/fixtures/seeds, regenerates, runs preflight + packets mode only, and returns the
exact diff for ChatGPT review.

No architecture reopening unless implementation proves the two-axis model cannot fit existing ownership.
No Gate 0 acceptance. No Doximity. No Phase 0.
