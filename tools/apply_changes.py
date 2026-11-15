#!/usr/bin/env python3
"""apply_changes.py - applies 01V semantic corrections to a fixed candidate.

Development-time tool. Not part of the Doximity runtime.

Two modes:

  label   python apply_changes.py --label raw01.txt --out candidate_ids.txt
          Assigns temporary C1..Cn review IDs to the raw 01 output.

  apply   python apply_changes.py --candidate candidate_ids.txt --changes changes.txt \
                                 --source sources.txt --out validated.txt
          Validates every proposed change, applies the accepted ones to the
          candidate, assigns final O1..On IDs, and writes the validated table.

The model never writes the validated table. It proposes changes; this script
decides and composes.

Exit codes: 0 = clean, 1 = at least one rejected change or malformed input,
2 = usage error.
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
ALLOWED_OPS = {"RECLASSIFY", "COMPLETE_CONTEXT", "SPLIT", "RESTORE"}

CANDIDATE_RE = re.compile(
    r"^(C\d+)\s*\|\s*([A-Z_]+)\s*\|\s*(.*?)\s*\|\s*\[([A-D])\s*,\s*([^,]*?)\s*,\s*([^\]]*)\]\s*$"
)
RAW_RE = re.compile(
    r"^([A-Z_]+):\s*(.*?)\s*\[([A-D])\s*,\s*([^,]*?)\s*,\s*([^\]]*)\]\s*$"
)
SOURCE_RE = re.compile(r"^\[([A-D])\]\s*(.*)$")
RESULT_ITEM_RE = re.compile(r'^([A-Z_]+):\s*(.+)$')

problems = []


def problem(message):
    problems.append(message)


def normalise(text):
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def words(text):
    return normalise(text).split()


def is_subsequence(small, big):
    iterator = iter(big)
    return all(word in iterator for word in small)


PRONOUNS = {"that", "it", "this", "they", "them", "these", "those", "he", "she", "its"}


def anaphora_ok(candidate, new_text, body_words):
    """True when exactly one pronoun in the candidate is replaced by a verbatim span
    from the source sentence, with prefix and suffix otherwise identical."""
    old_words = words(candidate)
    new_words = words(new_text)
    positions = [index for index, word in enumerate(old_words) if word in PRONOUNS]
    if len(positions) != 1:
        return False
    index = positions[0]
    prefix = old_words[:index]
    suffix = old_words[index + 1:]
    if len(new_words) < len(prefix) + len(suffix):
        return False
    if new_words[:len(prefix)] != prefix:
        return False
    if suffix and new_words[len(new_words) - len(suffix):] != suffix:
        return False
    end = len(new_words) - len(suffix) if suffix else len(new_words)
    replacement = new_words[len(prefix):end]
    if not replacement:
        return False
    for start in range(len(body_words) - len(replacement) + 1):
        if body_words[start:start + len(replacement)] == replacement:
            return True
    return False


def variants(word):
    """Morphological variants, so a conjugated verb can match its source form."""
    out = {word}
    if word.endswith("ing"):
        base = word[:-3]
        out |= {base, base + "e"}
    if word.endswith("ed"):
        base = word[:-2]
        out |= {base, base + "e"}
    if word.endswith("es"):
        base = word[:-2]
        out |= {base, base + "e"}
    if word.endswith("s"):
        out.add(word[:-1])
    if word.endswith("e"):
        out.add(word[:-1])
    return out


def parse_sources(path):
    blocks = []
    current = None
    with open(path, encoding="utf-8-sig") as handle:
        for raw in handle:
            text = raw.strip()
            match = SOURCE_RE.match(text)
            if match:
                if current:
                    blocks.append(current)
                letter, rest = match.group(1), match.group(2)
                cut = len(rest)
                for char in (":", "."):
                    index = rest.find(char)
                    if index != -1:
                        cut = min(cut, index)
                header = rest[:cut].strip()
                body = rest[cut + 1:].strip() if cut < len(rest) else ""
                if "," in header:
                    name, date = header.split(",", 1)
                else:
                    name, date = header, ""
                current = {
                    "letter": letter,
                    "name": name.strip(),
                    "date": date.strip(),
                    "body": body,
                }
            elif current and text:
                current["body"] = (current["body"] + " " + text).strip()
    if current:
        blocks.append(current)
    return blocks


def label_mode(raw_path, out_path):
    rows = []
    with open(raw_path, encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            match = RAW_RE.match(stripped)
            if not match:
                problem("raw line does not parse: " + stripped[:80])
                continue
            kind, text, letter, name, date = match.groups()
            rows.append("C" + str(len(rows) + 1) + " | " + kind + " | " + text.strip()
                        + " | [" + letter + ", " + name.strip() + ", " + date.strip() + "]")
    if problems:
        report()
        return 1
    text = "\n".join(rows) + "\n"
    if out_path:
        open(out_path, "w", encoding="utf-8").write(text)
    else:
        sys.stdout.write(text)
    print("labeled " + str(len(rows)) + " candidate objects")
    return 0


def parse_candidate(path):
    items = []
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            match = CANDIDATE_RE.match(stripped)
            if not match:
                problem("candidate line does not parse: " + stripped[:80])
                continue
            cid, kind, text, letter, name, date = match.groups()
            items.append({
                "cid": cid,
                "kind": kind,
                "text": text.strip(),
                "letter": letter,
                "name": name.strip(),
                "date": date.strip(),
            })
    return items


def parse_changes(path):
    changes = []
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == "NO_CHANGE":
                changes.append({"op": "NO_CHANGE"})
                continue
            if stripped.startswith("CHANGES"):
                continue
            fields = {}
            parts = [part.strip() for part in stripped.split(" | ")]
            op = parts[0]
            for part in parts[1:]:
                if ":" not in part:
                    problem("change field has no key: " + part[:60])
                    continue
                key, value = part.split(":", 1)
                fields[key.strip().upper()] = value.strip()
            changes.append({"op": op, "fields": fields, "raw": stripped})
    return changes


def resolve_block(blocks, letter, name, date):
    """Return the authoritative block matching letter+name+date, case-insensitively."""
    for block in blocks:
        if block["letter"] != letter:
            continue
        if block["name"].casefold() == name.casefold() and block["date"].casefold() == date.casefold():
            return block
    return None


def parse_result_items(value):
    items = []
    for piece in [p.strip() for p in value.split(";") if p.strip()]:
        piece = piece.strip().strip('"').strip()
        match = RESULT_ITEM_RE.match(piece)
        if not match:
            problem("SPLIT result item does not parse: " + piece[:60])
            continue
        items.append((match.group(1), match.group(2).strip()))
    return items


def apply_mode(candidate_path, changes_path, source_path, out_path):
    blocks = parse_sources(source_path)
    candidate = parse_candidate(candidate_path)
    changes = parse_changes(changes_path)
    by_cid = {item["cid"]: item for item in candidate}

    targets = {}
    restores = []
    if any(change["op"] == "NO_CHANGE" for change in changes) and len(changes) > 1:
        problem("NO_CHANGE may not appear alongside other changes")

    for change in changes:
        op = change["op"]
        if op == "NO_CHANGE":
            continue
        if op == "DROP":
            problem("DROP is not an allowed operation")
            continue
        if op not in ALLOWED_OPS:
            problem("operation not allowed: " + op)
            continue
        fields = change["fields"]

        if op == "RESTORE":
            letter = fields.get("SOURCE", "").strip()
            quote = fields.get("QUOTE", "").strip().strip('"')
            new_text = fields.get("NEW_TEXT", "").strip().strip('"')
            after = fields.get("AFTER", "-").strip()
            if letter not in ("A", "B", "C", "D"):
                problem("RESTORE needs SOURCE: A-D")
                continue
            if not quote or not new_text:
                problem("RESTORE needs QUOTE and NEW_TEXT")
                continue
            if not is_subsequence(words(new_text), words(quote)):
                problem("RESTORE text is not supported by its quote: " + new_text[:60])
                continue
            matches = [block for block in blocks
                       if block["letter"] == letter and normalise(quote) in normalise(block["body"])]
            if len(matches) != 1:
                problem("RESTORE quote matches " + str(len(matches)) + " [" + letter + "] blocks; need exactly 1")
                continue
            block = matches[0]
            kind = fields.get("NEW_KIND", "OBSERVATION").strip()
            if kind not in ALLOWED_KINDS:
                problem("RESTORE NEW_KIND not allowed: " + kind)
                continue
            if after != "-" and after not in by_cid:
                problem("RESTORE AFTER names an unknown candidate: " + after)
                continue
            restores.append({"after": after, "kind": kind, "text": new_text, "block": block})
            continue

        cid = fields.get("CANDIDATE", "").strip()
        if cid not in by_cid:
            problem(op + " names an unknown candidate: " + cid)
            continue
        if cid in targets:
            problem("two changes target the same candidate: " + cid)
            continue
        source = by_cid[cid]
        quoted = fields.get("TEXT", "").strip().strip('"')
        if normalise(quoted) != normalise(source["text"]):
            problem(op + " " + cid + ": quoted text does not match the candidate object")
            continue
        block = resolve_block(blocks, source["letter"], source["name"], source["date"])
        if block is None:
            problem(op + " " + cid + ": candidate provenance does not match any source header")
            continue

        if op == "RECLASSIFY":
            kind = fields.get("NEW_KIND", "").strip()
            if kind not in ALLOWED_KINDS:
                problem("RECLASSIFY NEW_KIND not allowed: " + kind)
                continue
            if kind == source["kind"]:
                problem("RECLASSIFY " + cid + " does not change the kind")
                continue
            targets[cid] = {"op": op, "kind": kind}

        elif op == "COMPLETE_CONTEXT":
            new_text = fields.get("NEW_TEXT", "").strip().strip('"')
            if not new_text:
                problem("COMPLETE_CONTEXT needs NEW_TEXT")
                continue
            if not is_subsequence(words(source["text"]), words(new_text)):
                if not anaphora_ok(source["text"], new_text, words(block["body"])):
                    problem("COMPLETE_CONTEXT " + cid
                            + " neither preserves the candidate words nor resolves a pronoun to a source span")
                    continue
            else:
                body_words = set(words(block["body"]))
                source_set = set(words(source["text"]))
                added = [word for word in words(new_text) if word not in source_set]
                missing = [word for word in added if not (variants(word) & body_words)]
                if missing:
                    problem("COMPLETE_CONTEXT " + cid + " adds words absent from the source sentence: "
                            + ", ".join(missing))
                    continue
            new_kind = fields.get("NEW_KIND", "").strip()
            if new_kind:
                if new_kind not in ALLOWED_KINDS:
                    problem("COMPLETE_CONTEXT NEW_KIND not allowed: " + new_kind)
                    continue
                if new_kind == source["kind"]:
                    problem("COMPLETE_CONTEXT " + cid + " NEW_KIND does not change the kind")
                    continue
            targets[cid] = {"op": op, "text": new_text, "kind": new_kind or source["kind"]}

        elif op == "SPLIT":
            results = parse_result_items(fields.get("RESULT", ""))
            if len(results) < 2:
                problem("SPLIT " + cid + " must produce at least two objects")
                continue
            source_words = words(source["text"])
            body_words = words(block["body"])
            bad = False
            for kind, text in results:
                if kind not in ALLOWED_KINDS:
                    problem("SPLIT " + cid + " uses a kind not allowed: " + kind)
                    bad = True
                    continue
                if not (is_subsequence(words(text), source_words) or is_subsequence(words(text), body_words)):
                    problem("SPLIT " + cid + " part is not supported by the candidate or its source sentence: "
                            + text[:50])
                    bad = True
            if not bad:
                targets[cid] = {"op": op, "results": results}

    if problems:
        report()
        return 1

    # compose
    objects = []
    for item in candidate:
        block = resolve_block(blocks, item["letter"], item["name"], item["date"])
        entry = {
            "kind": item["kind"],
            "text": item["text"],
            "letter": block["letter"],
            "name": block["name"],
            "date": block["date"],
        }
        target = targets.get(item["cid"])
        if target and target["op"] == "RECLASSIFY":
            entry["kind"] = target["kind"]
        elif target and target["op"] == "COMPLETE_CONTEXT":
            entry["text"] = target["text"]
            entry["kind"] = target["kind"]
        elif target and target["op"] == "SPLIT":
            for kind, text in target["results"]:
                objects.append({
                    "kind": kind,
                    "text": text,
                    "letter": block["letter"],
                    "name": block["name"],
                    "date": block["date"],
                })
            objects.extend([])
            for restored in [r for r in restores if r["after"] == item["cid"]]:
                objects.append({
                    "kind": restored["kind"],
                    "text": restored["text"],
                    "letter": restored["block"]["letter"],
                    "name": restored["block"]["name"],
                    "date": restored["block"]["date"],
                })
            continue
        objects.append(entry)
        for restored in [r for r in restores if r["after"] == item["cid"]]:
            objects.append({
                "kind": restored["kind"],
                "text": restored["text"],
                "letter": restored["block"]["letter"],
                "name": restored["block"]["name"],
                "date": restored["block"]["date"],
            })

    for restored in [r for r in restores if r["after"] == "-"]:
        objects.insert(0, {
            "kind": restored["kind"],
            "text": restored["text"],
            "letter": restored["block"]["letter"],
            "name": restored["block"]["name"],
            "date": restored["block"]["date"],
        })

    rows = []
    for index, obj in enumerate(objects, start=1):
        rows.append("O" + str(index) + " | " + obj["kind"] + " | " + obj["text"]
                    + " | [" + obj["letter"] + ", " + obj["name"] + ", " + obj["date"] + "]")
    text = "\n".join(rows) + "\n"
    if out_path:
        open(out_path, "w", encoding="utf-8").write(text)
    else:
        sys.stdout.write(text)
    print("applied " + str(len(targets)) + " change(s), " + str(len(restores)) + " restore(s); "
          + str(len(objects)) + " validated objects")
    return 0


def report():
    for message in problems:
        print("REJECT " + message)
    print("")
    print(str(len(problems)) + " rejected")


def main():
    args = {"--label": None, "--candidate": None, "--changes": None,
            "--source": None, "--out": None}
    index = 1
    while index < len(sys.argv):
        value = sys.argv[index]
        if value in args:
            if index + 1 >= len(sys.argv):
                print(__doc__)
                return 2
            args[value] = sys.argv[index + 1]
            index += 2
        else:
            print(__doc__)
            return 2

    if args["--label"]:
        return label_mode(args["--label"], args["--out"])
    if args["--candidate"] and args["--changes"] and args["--source"]:
        return apply_mode(args["--candidate"], args["--changes"], args["--source"], args["--out"])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
