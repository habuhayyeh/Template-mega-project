# AX-S1S2-D — executable manifest

**Status: AUTHORED / PARTIALLY FROZEN.** Three cases have frozen substrates; eight case slots are declared but empty. The harness can run the three.

---

## 1. What is frozen

| item | value |
|---|---|
| experiment | `AX-S1S2-D` |
| contract | `CONSENSUS_SUBMODULE_INTERFACES_v1.md` as amended by DC-001 |
| control plane | not used; this experiment does not depend on Phase 0 |
| input layer | **frozen ingest substrate**, hand-built per case (`fixtures/`) |
| artifact under test | S1 output → S2 output → S3 output → S4 blueprint |
| repetitions | 3 fresh conversations, identical order |
| scorer | external, per `predicates.md`; Gate 0 calibration required per family |

The substrate is frozen so a failure cannot be blamed on ingest. That is the whole point of testing STRUCTURE in isolation, and it is also the experiment's main limitation — see §7.

## 2. Cases

| slot | family | substrate | expected adoption |
|---|---|---|---|
| `CASE-01` | prior diagnosis, not adopted today | **frozen** | infarct **not** current |
| `CASE-02` | historical diagnosis explicitly re-adopted | **frozen** | infarct **current** |
| `CASE-09` | K2 rebuilt: explicit linkage to management | **frozen** | infarct **current**, linkage explicit |
| `CASE-03` | historical diagnosis disputed today | PENDING | — |
| `CASE-04` | current symptom/question, no diagnosis | PENDING | — |
| `CASE-05` | explicit two-alternative differential | PENDING | — |
| `CASE-06` | nested/more-specific claim | PENDING | — |
| `CASE-07` | body-only historical fact | PENDING | — |
| `CASE-08` | historical condition as etiology only | PENDING | — |
| `CASE-10` | candidate mentioned, explicitly deferred | PENDING | — |
| `CASE-11` | contradictory sources | PENDING | — |

`CASE-01/02/09` are `DERIVED_SYNTHETIC`: constructed architecture fixtures, not reconstructions of a real encounter and not derived from any supplied baseline.

## 3. Frozen artifact format

Each case emits four artifacts in one run, in this order:

```text
S1  candidates[]     id, subject, anchors[], salience, candidate_claims[]
S2  adjudication[]   object relations, adoption{object, verdict, evidence}, representations[]
S3  rendered[]       problem set, selected representation per problem, retained use, dispositions
S4  blueprint        sections, problems in final order, units, operators, membership
```

A run missing an artifact is **`EXECUTION_INVALID`**, not a content failure: a truncated run is a platform or harness problem, and scoring it as semantic failure would misattribute it to the architecture. `BLOCKED` is reserved for a missing prerequisite — no substrate, no calibration, no scorer — and is never an outcome of an attempted run.

## 4. Run procedure

1. Freeze the substrate files and hash them.
2. One fresh conversation per repetition; identical prompt, identical order.
3. Capture all four artifacts verbatim; hash them.
4. Score with the declared predicates, blind — the scorer does not know which repetition it is reading.
5. Record first divergence by predicate id and owning submodule.

## 5. Verdict rules

Three things are recorded separately and are not the same claim:

**Run state** — per repetition: `COMPLETED`, `EXECUTION_INVALID` (artifacts truncated or absent), or `PREREQUISITE_MISSING` (no substrate, no calibration, no scorer).

**Experiment verdict** — per case: `PASS` (all required predicates true 3/3), `NONCONFORMANT` (a required predicate false), `UNSCORED` (fewer than 3 valid runs).

**Architecture escalation** — the only level at which the interface may be reopened, and even then only by adjudication:
- a reproducible structural failure in a **single controlled case** is sufficient to open adjudication; vote counts across cases are not the trigger, and a single counterexample is not dismissed for being alone;
- before escalation, four alternative causes must be excluded and recorded: implementation noncompliance, missing contract or schema, substrate defect, platform or execution cause;
- what remains after exclusion is a responsibility-boundary impossibility, adjudicated by both agents and the signer;
- a structural miss in one run of three is a model nonconformance finding. It never escalates.

This separation exists because the first version of this table treated one bad run as an architecture verdict, and the second treated three as proof.


## 6. Predicates

Defined in `predicates.md`, with modes, owners, and the cases each expects to fire on.

Gate 0 calibration is required for **every ACTIVE predicate and its scorer** before any verdict is recorded. Partial calibration produces a partial verdict, never a whole one.

## 7. What this experiment cannot show

- It cannot show that ingest produces a correct substrate — the substrate is frozen by hand.
- It cannot show production behaviour: the four artifacts are not what a one-call run emits.
- It cannot show stability beyond 3/3 under this frozen condition.
- It cannot show that S4 is not overloaded (AX-S4) or that seams do not leak (AX-LEAK).

A pass here says the STRUCTURE interfaces can be honoured. It does not say the system works.

## 8. Blinding and independence

**The scorer receives four things and nothing else:** the target artifact, the read-only dependency
context required by the frozen dependency graph, the case oracle, and the frozen predicate/contract
rules. It does not receive the seed manifest, the expected predicate, mutation metadata, or the
specificity answer key — those belong to the harness, which selects the artifact and records which
predicate *should* fire. The scorer evaluates only the target artifact's `parent_type`.

A scorer that can see the expected answer is not a scorer; it is a lookup.

The primary scorer must not be the author of the substrates or of the artifacts under test. The author may score as a secondary challenger; disagreements are recorded, not averaged.

## 9. Frozen campaign identity

Every campaign record carries, at minimum:

```text
campaign_id, control_plane_version
predicate_registry {id, version}, active_set id, specificity_policy id
case, oracle_hash, parent_hash
package_version, model, mode
per-run: artifact hash, verdict, findings
```

Hashes are **SHA-256 over canonical JSON** (sorted keys, compact separators), not over bytes. Byte hashing makes a digest depend on formatting; content hashing makes it depend on content. The method is recorded in the manifest so a later run can tell which was used.
