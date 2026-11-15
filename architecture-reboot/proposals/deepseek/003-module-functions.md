# DeepSeek proposal 003 — the function of each runtime module

Functional level. No schemas, no operator list.

---

## 0. The three interfaces

What passes between modules is as much a part of the function as what happens inside them.

| Seam | Passes | Must not pass |
|---|---|---|
| source → **INGEST** | the paste, verbatim | style rules, section list, note history |
| **INGEST** → **STRUCTURE** | spans + objects | any judgement about relevance or sections |
| **STRUCTURE** → **RENDER** | units + operator names + section labels | raw source, objects not in a unit, any instruction to choose |
| **RENDER** → note | prose, one line per unit | commentary, ledger, repairs |

Two consequences that are easy to lose:

- **RENDER never sees the source.** If it can read the transcript, it can quote it, and then the IR is no longer the complete instruction.
- **INGEST never sees the style table.** If it does, it starts producing units, and the ingest/structure boundary disappears.

---

## 1. INGEST — what was said, and where

**Function.** Convert the pasted source into spans and atomic objects, with provenance, and with nothing decided about the note.

**Consumes:** the paste. **Produces:** spans with ids; objects with id, text, kind, provenance, source temporality, speaker where named, span id; explicit adoption statements where the source makes one.

**Decides:**
- where spans begin and end, mechanically where the paste allows;
- how a span decomposes into objects;
- each object's kind;
- source temporality — when the source is *from*, not whether it is current;
- whether a sentence records an adoption ("continue the apixaban") as distinct from recommending one.

**Does not decide:** relevance to the note, section, problem, order, duplicate identity, adoption for this encounter, any wording.

**Failure behaviour:** high recall. It may over-produce objects. It may not drop a span; every span ends with at least one disposition (`OBJECTS(n)`, `NOT_CLINICAL`, `NOT_USED` with reason). A span with no disposition is a hard error.

**Audited by:** AUDIT, source → objects. The check is coverage and fidelity: every span accounted for, every object traceable to span text.

**Why it exists:** because everything downstream must reference text that was actually said. It is the only module allowed to read the raw paste.

---

## 2. STRUCTURE — what the note is about, and how each fact is rendered

**Function.** Take objects and produce the Case IR: the problems, and the render units that say exactly what each line of the note will contain.

**Consumes:** spans + objects. **Produces:** problems (id, label, claim, order) and render units (section, problem, class, operator, members with roles, order, bucket).

**Decides — all of it, once:**
- which problems exist and in what order;
- which reasoning object is the claim;
- which objects are the same proposition, and which renders;
- which problem each object is used for;
- each unit's membership, roles, class and operator;
- section assignment;
- adoption for this encounter;
- what is omitted, and why.

**Does not decide:** wording, formatting, or anything about the text of an object. It may not add a fact, split a fact into two for presentation, or drop an object without a disposition.

**Failure behaviour:** fail closed. An object neither used nor dispositioned is an error, not an omission. A unit that does not typecheck against its operator is an error. When uncertain between two operators, it must choose the one that renders less, not more.

**Audited by:** AUDIT (source → IR) for semantic fidelity; CHECK indirectly, because the IR is what the note is checked against.

**Why it exists:** it is the only module that makes semantic decisions, and concentrating them is the point. Every failure we measured came from these decisions being made in more than one place, or made implicitly during prose generation.

---

## 3. RENDER — how a unit reads

**Function.** Turn each unit into one line of prose, using the operator's fixed text and the style table.

**Consumes:** units, operator definitions, style table. **Produces:** note text, one line per unit, in unit order.

**Decides:** only surface realisation inside the operator's allowance — capitalisation, punctuation, approved abbreviations, number and time display, section-scoped voice, folding exactly the members the unit names.

**Does not decide:** which unit, which members, which operator, which section, what order, whether a unit is needed. It does not see the source and does not see objects outside its unit.

**Failure behaviour:** a malformed unit produces `CONTRACT_ERROR` in place of that line, and the run fails; it does not produce plausible prose. A unit it cannot render is an error, never a silent skip.

**Audited by:** CHECK, IR → note, mechanically: one line per unit, only allowed text, voice rule, order.

**Why it exists:** language. Fragments become readable clinical prose here, and this is the only place generative freedom is wanted.

---

## 4. What is deliberately in no module

- **Duplicate resolution as a stage.** It is a decision inside STRUCTURE and a check inside CHECK.
- **Section pipeline modules.** Section differences are a style table plus operators, not separate semantics. Evidence for splitting would be a section whose *decisions* differ, not whose wording does.
- **A self-check inside RENDER.** A model that checks itself is not an instrument; CHECK is.
- **Any module that only moves data.** If a module neither decides nor renders nor checks, it is a schema, and schemas are not modules.

---

## 5. The open functional question

**Where ingest ends and structure begins when one model performs both.**

The boundary I would hold: ingest may decide *what kind of thing* an object is, and structure decides *what to do with it*. The moment ingest starts deciding "this is relevant to the seizure problem", the audit can no longer tell a decomposition error from a selection error, and those need different fixes.

If E1 shows that holding the line costs accuracy — objects produced badly because ingest is guessing what structure will want — then the boundary moves, and that is evidence, not preference.
