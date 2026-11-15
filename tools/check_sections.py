#!/usr/bin/env python3
"""check_sections.py - mechanical checks for a 06 section-routing ledger.

Development-time tool. Not part of the Doximity runtime.

Usage:
    python check_sections.py objects.txt ledger.txt

objects.txt : frozen table, O# | KIND | text | [letter, source_name, date]
ledger.txt  : 06 output, O# -> SECTION | DISCARD: reason, plus REUSE lines and footer

Structural checks only:
    - every input ID accounted for exactly once
    - no invented IDs, no malformed lines
    - allowed destinations
    - closed-set discard reasons (AP_ONLY, IRRELEVANT_TO_RETAINED_SECTIONS)
    - REUSE names a retained object, a valid section, and a distinct function
    - no duplicate primary assignments
    - structural rules: DEMOGRAPHIC -> HPI; FORMULATION/ETIOLOGY -> AP_ONLY
    - footer counts match

It cannot judge whether a section assignment is semantically right.
Exit 0 = clean, 1 = failure, 2 = usage error.
"""

import re
import sys

SECTIONS = {
    "REASON_FOR_CONSULT", "HPI", "ROS", "NEURO_HISTORY", "OTHER_PMH",
    "SOCIAL", "FAMILY", "MEDICATIONS", "EXAM", "WORKUP",
}
DISCARD_REASONS = {"AP_ONLY", "IRRELEVANT_TO_RETAINED_SECTIONS"}

OBJECT_RE = re.compile(
    r"^(O\d+)\s*\|\s*([A-Z_]+)\s*\|\s*(.*?)\s*\|\s*\[([A-D])\s*,\s*([^,]*?)\s*,\s*([^\]]*)\]\s*(?:\|\s*[A-Z_]+\s*)?$"
)
ASSIGN_RE = re.compile(r"^(O\d+)\s*(?:\u2192|->)\s*(.+?)\s*$")
REUSE_RE = re.compile(
    r"^REUSE:\s*(O\d+)\s*(?:\u2192|->)\s*([A-Z_]+)\s*,\s*distinct function:\s*(.+?)\s*$"
)
FOOTER_RE = re.compile(r"^(UNACCOUNTED_IDS|MULTIPLY_ASSIGNED_IDS|ACCOUNTING):\s*(.+)$", re.I)

failures = []


def fail(check, ref, message):
    failures.append((check, ref, message))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    # ledger lines contain arrows; a cp1252 console must not swallow the failure list
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    objects_path, ledger_path = sys.argv[1], sys.argv[2]

    objects = {}
    with open(objects_path, encoding="utf-8-sig") as handle:
        for line in handle:
            match = OBJECT_RE.match(line.strip())
            if not match:
                continue
            oid, kind, text, letter, name, date = match.groups()
            objects[oid] = {"kind": kind, "text": text.strip()}

    primary = {}
    reuse = []
    footer = {}
    order = []
    with open(ledger_path, encoding="utf-8-sig") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            footer_match = FOOTER_RE.match(raw)
            if footer_match:
                footer[footer_match.group(1).upper()] = footer_match.group(2).strip()
                continue
            if raw.upper().startswith("REUSE:"):
                match = REUSE_RE.match(raw)
                if not match:
                    fail(5, "", "malformed REUSE line: " + raw[:80])
                    continue
                oid, section, function = match.groups()
                if not function.strip():
                    fail(5, oid, "REUSE has no distinct-function statement")
                reuse.append((oid, section, function.strip()))
                continue
            match = ASSIGN_RE.match(raw)
            if not match:
                fail(8, "", "malformed ledger line: " + raw[:80])
                continue
            oid, destination = match.groups()
            if oid in primary:
                fail(1, oid, "duplicate primary assignment")
                continue
            if oid not in objects:
                fail(2, oid, "ID not present in the object table")
                continue
            primary[oid] = destination
            order.append(oid)

    # accounting
    missing = [oid for oid in objects if oid not in primary]
    for oid in missing:
        fail(1, oid, "input object has no assignment")

    # destinations and discard reasons
    for oid, destination in primary.items():
        if destination.startswith("DISCARD:"):
            reason = destination.split(":", 1)[1].strip()
            if reason not in DISCARD_REASONS:
                fail(4, oid, "discard reason not in the closed set: " + reason)
        elif destination not in SECTIONS:
            fail(3, oid, "destination not allowed: " + destination)

    # structural rules
    for oid, destination in primary.items():
        kind = objects[oid]["kind"]
        if kind == "DEMOGRAPHIC" and destination != "HPI":
            fail(7, oid, "DEMOGRAPHIC must route to HPI, got " + destination)
        if kind in ("DIAGNOSTIC_FORMULATION", "ETIOLOGY") and destination != "DISCARD: AP_ONLY":
            fail(7, oid, kind + " must discard as AP_ONLY, got " + destination)

    # reuse
    seen_reuse = set()
    for oid, section, function in reuse:
        if oid not in primary:
            fail(6, oid, "REUSE names an object with no primary assignment")
        elif primary[oid].startswith("DISCARD:"):
            fail(6, oid, "REUSE names a discarded object")
        if section not in SECTIONS:
            fail(6, oid, "REUSE target is not a valid section: " + section)
        elif oid in primary and primary[oid] == section:
            fail(6, oid, "REUSE repeats the primary destination")
        if (oid, section) in seen_reuse:
            fail(6, oid, "duplicate REUSE into " + section)
        seen_reuse.add((oid, section))

    # footer
    declared_missing = footer.get("UNACCOUNTED_IDS", "").lower()
    declared_multiple = footer.get("MULTIPLY_ASSIGNED_IDS", "").lower()
    if declared_missing != "none":
        fail(9, "", "footer declares unaccounted IDs: " + footer.get("UNACCOUNTED_IDS", ""))
    if declared_multiple != "none":
        fail(9, "", "footer declares multiply assigned IDs: " + footer.get("MULTIPLY_ASSIGNED_IDS", ""))
    accounting = footer.get("ACCOUNTING", "")
    match = re.match(r"^(\d+)\s*/\s*(\d+)$", accounting)
    if not match:
        fail(9, "", "ACCOUNTING missing or malformed: '" + accounting + "'")
    else:
        if int(match.group(1)) != len(primary):
            fail(9, "", "ACCOUNTING numerator does not match assignment count")
        if int(match.group(2)) != len(objects):
            fail(9, "", "ACCOUNTING denominator does not match input object count")

    print("check_sections: " + str(len(objects)) + " objects, "
          + str(len(primary)) + " assignments, " + str(len(reuse)) + " reuse lines")
    if failures:
        for check, ref, message in failures:
            print("FAIL [" + str(check) + "] " + (ref or "-") + "  " + message)
        print("")
        print(str(len(failures)) + " failure(s)")
        return 1
    print("PASS: accounting, destinations, reasons, reuse and structure are clean")
    print("NOTE: section placement itself is semantic and is not checked here")
    return 0


if __name__ == "__main__":
    sys.exit(main())
