# DeepSeek response 007 — the 4/4/3 tree

**Answer:** the decomposition is broadly right. Three boundaries need fixing before it is safe, and one demonstrated failure is currently unowned.

I am answering at the level you asked — responsibility decomposition, not schema.

---

## 1. Where the tree is right

- **INGEST's four** cover the two things ingest must guarantee: every source span is accounted for, and every object can be traced back to one. `Source Map` and `Span Accounting` are the mechanical half; `Object Extraction` and `Source-Annotation` are the semantic half. That split is correct because they fail differently — a coverage failure is an input problem, an annotation failure is a fidelity problem.
- **STRUCTURE's four** put every semantic decision in one module, which is the whole point of the design.
- **RENDER's three** keep realisation, composition and assembly separate, which is right because they fail differently: a realisation error is a wrong word, a composition error is a lost line, an assembly error is a missing section.

## 2. Boundary 1 — section list, order and omission belong to STRUCTURE

`Note Assembly` as described would decide which sections appear and in what order, and whether an empty section is omitted. That is a **structural** decision, not formatting: it depends on what the IR covers.

If RENDER owns it, then a note can lose a section and CHECK cannot tell whether the IR had nothing to say or the renderer dropped it.

Required: **STRUCTURE emits the section list, ordered, with empty sections already resolved.** RENDER assembles within the list it is given and may not add, omit, or reorder sections.

## 3. Boundary 2 — View Projection and Render-Unit Compilation are one decision

A unit's section and its operator are chosen together. Operators are section-sensitive (an HPI operator is not an A/P operator), so "which section" and "which operator" cannot be decided in different submodules without a seam that must be re-synchronised — the exact split-brain we removed at the top level.

Either merge them into one `Unit Composition`, or define the cut precisely:

- `View Projection` decides **which objects are used, and under which problem** — a set, not a shape.
- `Render-Unit Compilation` decides **membership, section, operator, order** — the shape.

The second is my preference, but the rule must be stated: projection may not choose an operator, and compilation may not add or drop an object.

## 4. Boundary 3 — Section Composition must be bounded to joining

`Section Composition` exists because HPI and history need paragraphs. That is real. But it is also the most dangerous submodule in the tree, because it is the first place where lines are merged into text.

Rules it must carry, or it becomes a second renderer:

- may join adjacent units of the same section in unit order;
- may add punctuation and connective whitespace;
- may **not** delete, reorder, or merge two units' content into a new sentence;
- may **not** introduce a temporal or causal connective that no unit contains.

Given those limits it is formatting. Without them it is semantic rewriting with a friendly name.

## 5. The unowned failure

**Who decides that a unit is required?**

Nothing in the tree owns completeness. `Object Adjudication` decides what objects mean; `Unit Compilation` builds units that are specified; `Note Assembly` assembles what it is given. So the failure we actually suffered — a problem with a claim and no reasoning bullet, or a plan item with no unit — is owned by nobody.

That failure is real: the missing `Seizure precautions` was exactly a unit that should have existed and did not.

Required: **STRUCTURE owns completeness**, as a check inside it — every problem has a claim unit; every current plan item has a plan unit; every reasoning object that survives adjudication has a unit; every section in the list has at least one unit or is omitted by rule. That is a submodule in all but name: `Coverage Completion`, or the last step of `Render-Unit Compilation`.

## 6. Verdict

Accept 4/4/3 with these changes:

1. section list/order/omission move from `Note Assembly` to STRUCTURE;
2. `View Projection` and `Render-Unit Compilation` are either merged or cut as in §3;
3. `Section Composition` is bounded to joining, in writing;
4. completeness becomes an owned STRUCTURE responsibility.

With those, no demonstrated failure is unowned. Without them, two are: a dropped section, and a required unit that never existed.
