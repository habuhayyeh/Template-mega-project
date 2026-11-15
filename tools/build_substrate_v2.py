#!/usr/bin/env python3
"""build_v2.py - regenerate the frozen substrate with EVIDENCE_MODE and speaker.

Reads the v1 frozen table and the original sources. Adds, per object:

  EVIDENCE_MODE  on OBSERVATION and COURSE only, from source review
  speaker prefix on [B] objects, only where the transcript names the speaker

Object wording is otherwise untouched; every other line must round-trip byte for byte.
"""

import re

SRC_TABLE = "step7/ORACLE_frozen_objects.txt"
SRC_TEXT = "step7/sources.txt"
OUT = "step9/frozen_objects_v2.txt"

OPEN_KINDS = {"OBSERVATION", "COURSE"}
ALLOWED = {"REPORTED", "EXAMINED", "TEST_RESULT", "CLINICIAN_COMMENT", "UNKNOWN"}

# modality as established in sources.txt
MODE = {
    # [A] consult
    "O2": "UNKNOWN",            # admitted 11/12 - administrative, no modality stated
    "O3": "REPORTED",           # witnessed event, recounted
    "O4": "REPORTED",           # about two minutes, recounted
    "O5": "REPORTED",           # postictal confusion, recounted
    "O6": "REPORTED",           # lasting an hour, recounted
    "O7": "REPORTED",           # known left MCA infarct
    "O8": "REPORTED",           # two years ago
    "O9": "REPORTED",           # mild residual expressive aphasia
    "O10": "REPORTED",          # atrial fibrillation
    "O13": "REPORTED",          # no prior seizures
    "O14": "TEST_RESULT",       # sodium 128
    "O17": "TEST_RESULT",       # CT head no hemorrhage
    "O18": "TEST_RESULT",       # old encephalomalacia
    "O19": "TEST_RESULT",       # no new focal lesion
    "O26": "EXAMINED",          # no fever, stated by the clinician in the examination sequence
    "O27": "EXAMINED",          # no neck stiffness, same sentence
    "O28": "REPORTED",          # she wants to drive
    "O32": "REPORTED",          # family's concern
    "O34": "CLINICIAN_COMMENT", # is not today's issue
    # [B] transcript
    "O36": "REPORTED",          # daughter
    "O37": "REPORTED",          # daughter
    "O40": "CLINICIAN_COMMENT", # clinician aside
    "O41": "REPORTED",          # patient
    # [C] ED note
    "O43": "REPORTED",
    "O44": "TEST_RESULT",
    "O45": "TEST_RESULT",
    "O47": "EXAMINED",
    "O48": "REPORTED",          # at baseline per family
    # [D] prior records
    "O49": "REPORTED",
    "O50": "REPORTED",
    "O51": "TEST_RESULT",
    "O53": "REPORTED",
    "O54": "REPORTED",
    "O56": "TEST_RESULT",
    "O15": "TEST_RESULT",       # sodium now 131
    "O60": "REPORTED",          # propranolol stopped 2025-03
}

# speaker, only where sources.txt labels the utterance
SPEAKER = {
    "O35": "clinician",
    "O36": "daughter",
    "O37": "daughter",
    "O38": "clinician",
    "O39": "clinician",
    "O40": "clinician",
    "O41": "patient",
    "O42": "clinician",
}

rows = []
with open(SRC_TABLE, encoding="utf-8") as handle:
    for raw in handle:
        raw = raw.rstrip("\n")
        if not raw.strip():
            continue
        oid, kind, text, prov = [part.strip() for part in raw.split("|", 3)]
        original_text = text
        if oid in SPEAKER:
            text = SPEAKER[oid] + ": " + text
        if kind in OPEN_KINDS:
            mode = MODE[oid]
            assert mode in ALLOWED, (oid, mode)
            rows.append((oid, kind, text, prov, mode, original_text))
        else:
            assert oid not in MODE, "mode given for closed-routing kind " + oid
            rows.append((oid, kind, text, prov, None, original_text))

assert len(rows) == 60, len(rows)
assert [r[0] for r in rows] == ["O" + str(i) for i in range(1, 61)]

with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    for oid, kind, text, prov, mode, _ in rows:
        line = oid + " | " + kind + " | " + text + " | " + prov
        if mode:
            line += " | " + mode
        handle.write(line + "\n")

print("wrote", OUT)
print("objects:", len(rows),
      "| modes:", sum(1 for r in rows if r[4]),
      "| speakers:", sum(1 for r in rows if r[0] in SPEAKER))
print("mode counts:",
      {m: sum(1 for r in rows if r[4] == m) for m in sorted(ALLOWED)})
