#!/usr/bin/env python3
"""check_decompose.py - mechanical checks for a frozen object table.

Development-time tool. Not part of the Doximity runtime.

Usage:
    python check_decompose.py validated.txt --source sources.txt

validated.txt : the table produced by apply_changes.py, one record per object:
                O1 | OBSERVATION | witnessed seizure | [A, Neurology consult, 2026-11-14]
sources.txt   : the original [A]-[D] material, headers included.

Checks only what is mechanical:
    - allowed kinds
    - non-empty text
    - well-formed provenance triple
    - source name and date match the header exactly, including case
    - sequential unique O# IDs
    - no malformed records

It does not judge coverage, atomicity, kind correctness, or attribution.
Exit code 0 = clean, 1 = failure, 2 = usage error.
"""

import re
import sys

ALLOWED_KINDS = {
    "DEMOGRAPHIC",
    "MANAGEMENT",
    "ETIOLOGY",
    "COURSE",
    "DIAGNOSTIC_FORMULATION",
    "OBSERVATION",
}

# EVIDENCE_MODE is required on the two kinds whose body section is genuinely open,
# and forbidden on the four that route structurally or are themselves a mode.
OPEN_KINDS = {"OBSERVATION", "COURSE"}
ALLOWED_MODES = {"REPORTED", "EXAMINED", "TEST_RESULT", "CLINICIAN_COMMENT", "UNKNOWN"}

RECORD_RE = re.compile(
    r"^(O\d+)\s*\|\s*([A-Z_]+)\s*\|\s*(.*?)\s*\|\s*\[([A-D])\s*,\s*([^,]*?)\s*,\s*([^\]]*)\]\s*(?:\|\s*([A-Z_]+)\s*)?$"
)
SOURCE_RE = re.compile(r"^\[([A-D])\]\s*(.*)$")

failures = []


def fail(check, oid, message):
    failures.append((check, oid, message))


def parse_sources(path):
    headers = {}
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            match = SOURCE_RE.match(line.strip())
            if not match:
                continue
            letter, rest = match.group(1), match.group(2)
            cut = len(rest)
            for char in (":", "."):
                index = rest.find(char)
                if index != -1:
                    cut = min(cut, index)
            header = rest[:cut].strip()
            if "," in header:
                name, date = header.split(",", 1)
            else:
                name, date = header, ""
            headers.setdefault(letter, set()).add((name.strip(), date.strip()))
    return headers


def main():
    path = None
    source = None
    index = 1
    while index < len(sys.argv):
        value = sys.argv[index]
        if value == "--source":
            if index + 1 >= len(sys.argv):
                print(__doc__)
                return 2
            source = sys.argv[index + 1]
            index += 2
        else:
            path = value
            index += 1
    if path is None or source is None:
        print(__doc__)
        return 2

    headers = parse_sources(source)
    records = []
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            match = RECORD_RE.match(raw)
            if not match:
                fail(1, "", "malformed record: " + raw[:90])
                continue
            oid, kind, text, letter, name, date, mode = match.groups()
            name, date = name.strip(), date.strip()
            records.append(oid)

            if kind not in ALLOWED_KINDS:
                fail(2, oid, "kind not allowed: " + kind)
            if not text.strip():
                fail(3, oid, "empty text")

            if kind in OPEN_KINDS:
                if not mode:
                    fail(6, oid, "missing EVIDENCE_MODE on " + kind)
                elif mode not in ALLOWED_MODES:
                    fail(6, oid, "EVIDENCE_MODE not allowed: " + mode)
            elif mode:
                fail(6, oid, "EVIDENCE_MODE on a kind whose section is structural: " + kind)

            expected = headers.get(letter)
            if expected is None:
                fail(4, oid, "no source header for letter " + letter)
            elif (name, date) not in expected:
                folded = {(n.casefold(), d.casefold()) for n, d in expected}
                if (name.casefold(), date.casefold()) in folded:
                    fail(4, oid, "provenance differs only in case from the header: '"
                         + name + "', '" + date + "'")
                else:
                    fail(4, oid, "provenance does not match any [" + letter + "] header: '"
                         + name + "', '" + date + "'")

    for position, oid in enumerate(records, start=1):
        if oid != "O" + str(position):
            fail(5, oid, "expected O" + str(position) + " at position " + str(position))
            break
    duplicates = {oid for oid in records if records.count(oid) > 1}
    for oid in sorted(duplicates):
        fail(5, oid, "duplicate ID")

    print("check_decompose: " + str(len(records)) + " objects")
    if failures:
        for check, oid, message in failures:
            print("FAIL [" + str(check) + "] " + (oid or "-") + "  " + message)
        print("")
        print(str(len(failures)) + " failure(s)")
        return 1
    print("PASS: kinds, text, provenance, and IDs are mechanically clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
