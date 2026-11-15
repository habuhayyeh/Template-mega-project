# Proposal 026 — six Ask files, and the first handoff

**Status:** PROPOSED — decomposition and handoff contract only. No implementation, no patient data.

## Assumption to confirm

The six files are **logical modules/prompts inside one Ask call**, not six human-carried model calls.

- Scribe V2.2 produces the evidence packet.
- Ask consumes the packet + six module files + final template and returns one note.
- The modules are responsibility boundaries, like the eleven consensus submodules compressed into six
  execution files.

If the intent is six separate Ask calls, intermediate artifacts must be carried between calls. That is a
different topology from D-034's one Ask call and needs an explicit decision before implementation.

## The six files

| file | responsibility | consumes | produces | must not |
|---|---|---|---|---|
| `01_evidence_index` | parse/validate Scribe packet into a canonical source/record index | Scribe V2.2 packet | `EVIDENCE_INDEX` | infer problems, adoption, causality, role, note content |
| `02_problem_model` | independent problem identity and containment | evidence index | problem inventory with contained facts | decide current stance, role, causality, note text |
| `03_semantic_state` | current encounter stance, representations, relation fidelity | problem inventory + evidence | state/relation ledger | choose note sections or render prose |
| `04_selection_use` | what is retained, role, dispositions, template relevance | state/relation ledger | retained/role/use plan | add facts or rewrite source meaning |
| `05_blueprint` | render units, operators, order, sections | use plan | note blueprint | invent content or make new semantic decisions |
| `06_render` | final note from blueprint + template | blueprint + template | final note | change semantics, add facts, repair malformed units silently |

Mapping to the consensus submodules:

- `I1–I4` -> file 1 (packet already performs source-preserving extraction; file 1 indexes and validates)
- `S1` -> file 2
- `S2` -> file 3
- `S3` -> file 4
- `S4` -> file 5
- `R1–R3` -> file 6

## File 1 — `01_evidence_index`

### Job

Turn the Scribe packet into a canonical, lossless `EVIDENCE_INDEX` that every later file can cite.

File 1 is a **parser/validator**, not a reasoner. Preferred implementation is deterministic code. If it
must run as an Ask prompt, it is a strict copy-only parser and must fail closed on ambiguity.

### Input

Exact V2.2 packet:

```text
@@PACKET SCRIBE_EVIDENCE_V2_2
@@SOURCE T TRANSCRIPT CURRENT
T001 :: SPK2 :: Three falls since June.
@@SOURCE P1 ED NOTE 2026-11-14
P1.001 :: SEC=HPI :: VIA=EMS report :: Patient reports three falls.
@@END
```

### Output

```text
EVIDENCE_INDEX v1
STATUS VALID
SOURCE S1 id=T kind=transcript label=TRANSCRIPT CURRENT date=unknown order=0
SOURCE S2 id=P1 kind=prechart name=ED NOTE date=2026-11-14 order=1
RECORD T001 source=T label=SPK2 order=0 flags=[] text=Three falls since June.
RECORD P1.001 source=P1 label=P1.001 order=0 flags=[SEC=HPI,VIA=EMS report] text=Patient reports three falls.
CHECKSUM sources=2 records=2
END
```

### Parse rules

1. `@@PACKET` must start the packet; `@@END` must finish it.
2. Each `@@SOURCE <id> <name/type> <date>` creates one source; preserve supplied order.
3. Every record must be `<id> :: <label> :: <text>`.
4. For prechart records, optional `SEC=<value>` and `VIA=<value>` fields may precede text:
   `<id> :: SEC=<value> :: VIA=<value> :: <text>`.
5. Split only the first two structural separators; the remainder is exact text. Do not parse `::`
   inside the text.
6. `T` records must carry a raw `SPK` label; `P` records must carry their source prefix.
7. IDs must be unique. Never renumber, merge, split or rewrite records.
8. Preserve inline markers (`[UNCLEAR]`, `[VERBATIM...]`, `[NO ANSWER CAPTURED]`) in `text`; record their
   presence in `flags` without interpreting them.
9. Preserve source order and record order exactly.
10. Source date/author is copied only when stated; never inferred.
11. Unknown/malformed line -> `STATUS INVALID` with a record/line pointer. No silent drop.
12. If `@@TRUNCATED AFTER <id>` appears, record it as a warning/flag; downstream must know.
13. No semantic normalization: no spelling fixes, no speaker identity mapping, no section inference.

### Handoff to file 2

Only a `STATUS VALID` index is passed. File 2 may use only `SOURCE`/`RECORD` IDs and text from the
index. It must not see or re-read raw Scribe packet text.

The handoff is intentionally boring: sources, records, order, labels, markers, checksum. No problem
list, no summary, no semantic annotation.

## What Scribe does with this

Scribe does not execute file 1. Scribe produces the V2.2 packet; file 1 consumes it.

The first controlled check is a **packet-to-index fidelity test**:

1. Run Scribe V2.2 on one synthetic/de-identified case.
2. Feed the exact packet to file 1.
3. Compare:
   - source count and order;
   - record count and IDs;
   - exact text equality;
   - labels, SEC/VIA, inline markers;
   - no dropped, duplicated, merged or rewritten records.
4. If file 1 is a prompt, repeat the same check; prefer deterministic parser.

This tests the first handoff without asking file 1 to make any clinical decision.

## Canonicalization decisions

- `CONSENSUS_ARCHITECTURE_v0.1.md` and `CONSENSUS_SUBMODULE_INTERFACES_v1.md` remain canonical, but §1
  "one paste / one Ask call" needs the D-034 Scribe-first amendment.
- Scribe V2.2 is the provisional canonical input packet.
- Ask Contract 119 and containment proposal 016 are folded into files 2–4, not kept as separate
  contracts.
- Proposal 024's single-contract P/N form is superseded; keep its four-outcome scoring and failure
  localization for the six-file run.
- Proposal 020 remains the Option B roadmap.

## Open questions

1. Confirm six files inside one Ask call vs six calls.
2. Confirm file 1 deterministic parser vs Ask prompt.
3. Provide one representative note template/example so file 5/6 inputs are concrete.
4. Confirm whether `SEC=`/`VIA=` parsing is file 1 or file 2; this proposal puts mechanical parsing in
   file 1 and semantic interpretation in file 2/3.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
