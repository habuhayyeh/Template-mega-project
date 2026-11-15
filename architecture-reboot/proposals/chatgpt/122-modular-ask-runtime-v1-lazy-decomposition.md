# Proposal 122 — modular Ask runtime v1: lazy decomposition

**Status:** PROPOSED replacement for proposal 120 after File 1 execution evidence.

## Core execution principle

The Scribe V2.2 packet is the canonical immutable evidence store.

Do **not** globally rewrite every supplied proposition into a second atomic-object corpus before clinical
organization.

Downstream Ask functions emit only the smallest intermediate representation needed by the next function,
primarily by referring back to stable Scribe record IDs.

Atomic splitting is **lazy**:
- split a source record only when two propositions inside it require materially different reconciliation,
  action state, problem membership, stance, relation, or note use;
- otherwise preserve the source record as the evidence unit.

## Candidate runtime

```text
Scribe V2.2 packet
      ↓
F1 Reconciled Evidence
      ↓
F2 Action State
      ↓
F3 Problem Architecture
   [identity -> state/relations -> role/use]
      ↓
F4 Note Compiler
      ↓
F5 Renderer
      ↓
F6 Output Guard
      ↓
Final note
```

## F1 — Reconciled Evidence

Consumes the Scribe packet directly.

Produces a **compact source-backed fact map**, not a rewritten atomic corpus.

Owns:
- obvious duplicate consolidation;
- source-reference/coreference candidates where needed for reconciliation;
- longitudinal evolution;
- true conflict preservation;
- source-specific negative/uncertain states;
- compact canonical wording sufficient for downstream reasoning;
- source IDs for every reconciled item.

Does not own:
- independent neurologic problem identity;
- current encounter adoption/final stance;
- PRIMARY/BACKGROUND;
- causal inference beyond explicit source reasoning;
- note inclusion/section;
- final action/plan adoption.

## F2 — Action State

Consumes F1 plus original Scribe packet as needed.

Preserves/reconciles source-level management/test action states:
- considered/recommended/planned/ordered/started/performed/completed/held/stopped;
- owner;
- timing/condition;
- patient response;
- result pending/final/unavailable.

It does not decide the final encounter plan.

## F3 — Problem Architecture

Core clinical structure function.

Must emit three observable checkpoints:

1. identity/containment partition;
2. current state + relations;
3. role/use.

Later checkpoints may not silently rewrite the earlier identity partition.

This is the execution bundling of S1 -> S2 -> S3.

## F4 — Note Compiler

S4-equivalent.

Build:
- episode timeline;
- longitudinal neurologic history;
- medication/exam/workup packets;
- A/P packets;
- evidence/counterevidence compression;
- action attachment;
- section allocation;
- permitted reuse;
- problem/unit order.

## F5 — Renderer

Language realization only.

No new semantic decision.

## F6 — Output Guard

Compare rendered note to F4 blueprint and repair only rendering drift.

Diagnostic/runtime hygiene only; never acceptance evidence.

## Why this supersedes global atomicization

The production surface is an LLM, not Python.

A fully materialized atomic corpus:
- duplicates much of the input;
- increases token/output burden before any useful compression;
- creates additional opportunities for wording drift;
- uses working memory on intermediate bookkeeping;
- truncated in the first observed Doximity run.

A sparse reference-based handoff keeps the source packet available as the truth substrate while each
function records only new decisions.

## Stronger-surface comparison

A stronger reasoning model remains useful for function-design diagnosis, but not as a clinical oracle.

The main comparison becomes:
- does the function itself produce a coherent compact handoff?
- does GPT-4o reproduce the material decisions?
- where does the first material divergence occur?

Do not demand identical wording or identical low-value source decomposition.
