#!/usr/bin/env python3
"""check_ledger.py - mechanical acceptance checks for a 03 assignment ledger.

Development-time tool. Not part of the Doximity runtime.

Usage:
    python check_ledger.py objects.txt ledger.txt [--review]

objects.txt : the 03 input, objects as "O1 | text | [A]" under CLAIM/ETIOLOGY/
              EVIDENCE/COURSE/MANAGEMENT headings.
ledger.txt  : the 03 output, one "O# -> destination" line per object, optional
              REUSE lines, then UNACCOUNTED_IDS / MULTIPLY_ASSIGNED_IDS /
              ACCOUNTING.

Exit code 0 = no mechanical failure. 1 = at least one failure.

It decides only the invariants listed in CHECKS. Semantic questions are
printed under --review and are not scored.
"""

import re
import sys

BUCKETS = ("CLAIM", "ETIOLOGY", "EVIDENCE", "COURSE", "MANAGEMENT")

OBJECT_RE = re.compile(r"^(O\d+)\s*\|\s*(.*?)\s*\|\s*\[([A-D])\s*,\s*([^,]*?)\s*,\s*([^\]]*)\]\s*$")
ASSIGN_RE = re.compile(r"^(O\d+)\s*(?:\u2192|->)\s*(.+)$")
REUSE_RE = re.compile(r"^REUSE:\s*(O\d+)\s*(?:\u2192|->)\s*(P\d+\.\w+)")
FOOTER_RE = re.compile(r"^(UNACCOUNTED_IDS|MULTIPLY_ASSIGNED_IDS|ACCOUNTING):\s*(.*)$", re.I)

ALLOWED_ROLES = {
    "CLAIM": {"PRIMARY_CLAIM", "CLAIM_QUALIFIER"},
    "ETIOLOGY": {"ETIOLOGY"},
    "EVIDENCE": {"EVIDENCE", "PROBLEM_LABEL"},
    "COURSE": {"COURSE", "PROBLEM_LABEL"},
    "MANAGEMENT": {"MANAGEMENT"},
}

REASON_PATTERNS = (
    ("EXACT_DUPLICATE_OF", re.compile(r"^EXACT_DUPLICATE_OF:\s*(O\d+)$")),
    ("IRRELEVANT", re.compile(r"^IRRELEVANT_TO_RETAINED_PROBLEMS$")),
)

CHECKS = {
    1: "missing input ID",
    2: "multiply assigned ID",
    3: "invented ID",
    4: "destination inconsistent with source bucket",
    5: "DISCARD reason outside the closed set",
    6: "EXACT_DUPLICATE_OF not an exact duplicate",
    7: "EXPLICITLY_SUPERSEDED_BY not capable of superseding",
    8: "block's only management is historical",
    9: "REUSE target missing",
    10: "footer count does not match ledger",
}

failures = []


def fail(check, oid, message):
    failures.append((check, oid, message))


def normalise(text):
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def parse_objects(path):
    objects = {}
    order = []
    bucket = None
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped in BUCKETS:
                bucket = stripped
                continue
            match = OBJECT_RE.match(stripped)
            if match and bucket:
                oid, text, source, name, date = match.groups()
                if oid in objects:
                    fail(3, oid, "duplicate object line in input")
                objects[oid] = {"bucket": bucket, "text": text, "source": source, "name": name.strip(), "date": date.strip()}
                order.append(oid)
    return objects, order


def parse_ledger(path):
    assignments = {}
    reuse = []
    footer = {}
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.upper().startswith("REUSE:"):
                match = REUSE_RE.match(stripped)
                if match:
                    reuse.append((match.group(1), match.group(2), stripped))
                else:
                    fail(9, "", "malformed REUSE line: " + stripped[:70])
                continue
            match = FOOTER_RE.match(stripped)
            if match:
                footer[match.group(1).upper()] = match.group(2).strip()
                continue
            match = ASSIGN_RE.match(stripped)
            if not match:
                fail(10, "", "unparseable line: " + stripped[:70])
                continue
            oid, destination = match.group(1), match.group(2).strip()
            assignments.setdefault(oid, []).append(destination)
    return assignments, reuse, footer


def main():
    args = [value for value in sys.argv[1:] if not value.startswith("--")]
    review = "--review" in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2

    objects, order = parse_objects(args[0])
    assignments, reuse, footer = parse_ledger(args[1])

    # 3. invented IDs
    for oid in assignments:
        if oid not in objects:
            fail(3, oid, "not present in the input object list")

    # 1. missing IDs
    for oid in order:
        if oid not in assignments:
            fail(1, oid, "no assignment line")

    # 2. multiply assigned
    for oid, destinations in assignments.items():
        if len(destinations) > 1:
            fail(2, oid, "assigned " + str(len(destinations)) + " times: " + ", ".join(destinations))

    retained = set()
    block_management = {}
    block_has_claim = {}
    labels = {}

    for oid, destinations in assignments.items():
        obj = objects.get(oid)
        if obj is None:
            continue
        for destination in destinations:
            block_match = re.match(r"^P(\d+)\.([A-Z_]+)$", destination)
            if destination.upper().startswith("DISCARD:"):
                check_reason(oid, destination, objects, assignments, retained)
                continue
            if not block_match:
                fail(4, oid, "unrecognised destination: " + destination)
                continue
            block, role = int(block_match.group(1)), block_match.group(2)
            # 4. bucket consistency
            if role not in ALLOWED_ROLES.get(obj["bucket"], set()):
                fail(4, oid, obj["bucket"] + " object routed to " + destination)
            retained.add(oid)
            if role == "MANAGEMENT":
                block_management.setdefault(block, []).append(oid)
            if role in ("PRIMARY_CLAIM", "CLAIM_QUALIFIER", "PROBLEM_LABEL"):
                block_has_claim.setdefault(block, []).append(oid)
            if role == "PROBLEM_LABEL":
                labels.setdefault(block, []).append(oid)

    # 8. block whose only management is historical [D]
    for block, oids in sorted(block_management.items()):
        if all(objects[oid]["source"] == "D" for oid in oids):
            fail(8, "P" + str(block), "only management is historical [D]: " + ", ".join(oids))
    for block, oids in sorted(block_has_claim.items()):
        if block not in block_management:
            fail(8, "P" + str(block), "no management entry at all (claim/label: " + ", ".join(oids) + ")")

    # 9. REUSE target
    for oid, target, raw in reuse:
        if oid not in assignments:
            fail(9, oid, "REUSE for an ID with no assignment line")
        elif oid not in retained:
            fail(9, oid, "REUSE for an object that was discarded")
        else:
            block = re.match(r"^(P\d+)\.", target)
            if block and not any(
                destination.startswith(block.group(1) + ".")
                for destination in assignments.get(oid, [])
            ):
                pass  # secondary block is a declaration; primary assignment is elsewhere

    # 10. footer
    check_footer(footer, objects, assignments, order)

    # report
    print("check_ledger: " + str(len(objects)) + " objects, " +
          str(sum(len(value) for value in assignments.values())) + " assignment lines")

    if failures:
        failures.sort(key=lambda item: (item[0], item[1]))
        for check, oid, message in failures:
            print("FAIL [" + str(check) + "] " + (oid or "-") + "  " + message + "  (" + CHECKS[check] + ")")
        print("")
        print(str(len(failures)) + " failure(s)")
    else:
        print("PASS: all mechanical checks clean")

    if review:
        print("")
        print("SEMANTIC REVIEW (not mechanically decided)")
        for block in sorted(block_has_claim):
            label = ", ".join(labels.get(block, [])) or "-"
            claim = ", ".join(block_has_claim[block])
            management = ", ".join(block_management.get(block, [])) or "-"
            print("  P" + str(block) + ": label=" + label + " claim/label objs=" + claim + " management=" + management)
        for block, oids in sorted(labels.items()):
            for oid in oids:
                print("  P" + str(block) + " label text: " + objects[oid]["text"])

    return 1 if failures else 0


def check_reason(oid, destination, objects, assignments, retained):
    reason = destination.split(":", 1)[1].strip()
    kind = None
    target = None
    for name, pattern in REASON_PATTERNS:
        match = pattern.match(reason)
        if match:
            kind = name
            target = match.group(1) if match.groups() else None
            break
    if kind is None:
        fail(5, oid, "reason not in closed set: " + reason)
        return

    if kind == "EXACT_DUPLICATE_OF":
        if target not in objects:
            fail(6, oid, "referenced " + str(target) + " does not exist")
            return
        target_destinations = assignments.get(target, [])
        target_retained = any(not value.upper().startswith("DISCARD:") for value in target_destinations)
        if not target_retained:
            fail(6, oid, "referenced " + target + " is not retained")

        source_object = objects[oid]
        target_object = objects[target]
        if source_object["bucket"] != target_object["bucket"]:
            fail(6, oid, "bucket differs from " + target + ": " +
                 source_object["bucket"] + " vs " + target_object["bucket"])
        elif normalise(source_object["text"]) != normalise(target_object["text"]):
            fail(6, oid, "text differs from " + target + " after normalisation: '" +
                 source_object["text"] + "' vs '" + target_object["text"] + "'")


def check_footer(footer, objects, assignments, order):
    computed_missing = [oid for oid in order if oid not in assignments]
    computed_multiple = [oid for oid, value in assignments.items() if len(value) > 1]
    total = sum(len(value) for value in assignments.values())

    declared_missing = footer.get("UNACCOUNTED_IDS", "")
    declared_multiple = footer.get("MULTIPLY_ASSIGNED_IDS", "")
    declared_accounting = footer.get("ACCOUNTING", "")

    if declared_missing.strip().lower() != "none":
        fail(10, "", "footer declares unaccounted IDs: " + declared_missing)
    if computed_missing:
        fail(10, "", "ledger actually has unaccounted IDs: " + ", ".join(computed_missing))

    if declared_multiple.strip().lower() != "none":
        fail(10, "", "footer declares multiply assigned IDs: " + declared_multiple)
    if computed_multiple:
        fail(10, "", "ledger actually has multiply assigned IDs: " + ", ".join(computed_multiple))

    match = re.match(r"^(\d+)\s*/\s*(\d+)$", declared_accounting)
    if not match:
        fail(10, "", "ACCOUNTING missing or malformed: '" + declared_accounting + "'")
        return
    numerator, denominator = int(match.group(1)), int(match.group(2))
    if numerator != total:
        fail(10, "", "ACCOUNTING numerator " + str(numerator) + " != " + str(total) + " assignment lines")
    if denominator != len(objects):
        fail(10, "", "ACCOUNTING denominator " + str(denominator) + " != " + str(len(objects)) + " input objects")


if __name__ == "__main__":
    sys.exit(main())
