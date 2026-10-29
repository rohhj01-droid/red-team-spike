"""X4b inventory tool (design Section 6): candidate generation only.

    python -I inventory.py sources <tree> <out.tsv>       S_doc + quarantined files
    python -I inventory.py enumerators <tree> <out.tsv>   K1-K4 candidates with member counts

Nothing here decides admissibility. Every candidate the committed
patterns produce is written with its EN1..EN6 cells empty; the analyst
fills them (Section 6.1 / 6.2) and `checks.py inventory` verifies the
filled table's shape.

Column 0 is the file-scope proxy for K1-K3 (Doom-era sources indent
function bodies). K1 also takes an anonymous struct element type
(`static struct { ... } name[] = {`); an initializer hidden behind a
macro (`name[] = SOME_MACRO;`) is not a candidate (XQA-04). K1 takes ANY element type, scalar and pointer
included -- wider than the design's parenthetical, recorded as an XQA
entry at X4b. Files are decoded as latin-1 for scanning, so Latin-1
bytes neither crash the scan nor shift line numbers.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import is_quarantined, walk_tree, write_tsv  # noqa: E402

S_DOC_EXT = {".md", ".txt", ".html", ".htm", ".rst", ".adoc", ".texi", ".1", ".5", ".6", ".man"}
CODE_EXT = {".c", ".h", ".cpp", ".hpp", ".m"}
SRC_FIELDS = ["path", "bytes", "decision", "reason"]
EN_FIELDS = ["cand_id", "file", "line", "symbol", "class", "element_type", "members", "absent", "conditional",
             "en1", "en2", "en3", "en4", "en5", "en6", "tag", "reject_reason", "evidence"]

# K1: `<type words> <name>[...]... = {` at column 0; `=` and `{` may sit on later lines.
K1_RE = re.compile(r"^((?:(?:static|const|extern)\s+)*struct\s*\{[^{}]*\}|[A-Za-z_][\w\s\*]*?)\s*\b([A-Za-z_]\w*)\s*\[[^\]]*\](?:\s*\[[^\]]*\])*\s*=\s*\{", re.M)
# direct function-pointer array: `type (*name[])(args) = {`
K2_FN_RE = re.compile(r"^([A-Za-z_][\w\s\*]*?)\s*\(\s*\*\s*([A-Za-z_]\w*)\s*\[[^\]]*\]\s*\)\s*\([^)]*\)\s*=\s*\{", re.M)
K3_DEFINE_RE = re.compile(r"^[ \t]*#[ \t]*define[ \t]+(\w+)(\([^)]*\))?[ \t]*\\[ \t]*$", re.M)
K3_CALL_RE = re.compile(r"^\s*(\w+)\s*\(.*\)\s*,?\s*\\?\s*$")
K4_RE = re.compile(r"\b(all|every|each)\b.{0,100}?\b(in|under|inside)\b", re.I | re.S)
TYPEDEF_STRUCT_RE = re.compile(r"typedef\s+struct\s*\w*\s*\{(.*?)\}\s*([A-Za-z_]\w*)\s*;", re.S)
STRUCT_RE = re.compile(r"\bstruct\s+([A-Za-z_]\w*)\s*\{(.*?)\}", re.S)


def read_text(path: str) -> str:
    with open(path, "rb") as f:
        return f.read().decode("latin-1")


def _collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- sources

def readme_links(tree: str) -> set[str]:
    readme = os.path.join(tree, "README.md")
    if not os.path.isfile(readme):
        return set()
    out = set()
    for m in re.finditer(r"\]\(([^)\s#]+)", read_text(readme)):
        target = m.group(1)
        if re.match(r"[a-z]+:", target):
            continue
        target = target[2:] if target.startswith("./") else target
        if os.path.isfile(os.path.join(tree, target)):
            out.add(target.replace("\\", "/"))
    return out


def is_s_doc(rel: str, links: set[str]) -> bool:
    parts = rel.split("/")
    name, dirs = parts[-1], parts[:-1]
    ext = os.path.splitext(name)[1].lower()
    if ext in S_DOC_EXT:
        return True
    if "." not in name and (not dirs or any(d.lower().startswith(("doc", "man")) for d in dirs)):
        return True
    return rel in links


def sources(tree: str) -> list[dict]:
    links = readme_links(tree)
    rows = []
    for rel in walk_tree(tree):
        q = is_quarantined(rel)
        if q or is_s_doc(rel, links):
            rows.append({"path": rel, "bytes": str(os.path.getsize(os.path.join(tree, rel))),
                         "decision": "QUARANTINED" if q else "", "reason": ""})
    return rows


# ---------------------------------------------------------------- members

def count_members(text: str, start: int) -> tuple[list[dict], list[str]]:
    """Members of the brace initializer whose `{` is at text[start].

    Returns (present_members, absent_texts); a present member is
    {"index", "text", "cond"}. Rules (design Section 6.3 and the plan's
    Task 3): `//` and `/* */` comments are not members, but a comment
    whose content begins with `{` is recorded as ABSENT; string and
    character literals are opaque; `#if 0` makes its block ABSENT; any
    other #if/#ifdef/#ifndef/#elif/#else is recorded as the member's
    condition; a `,` at depth 1 ends a member; the last member needs no
    comma; an empty member (trailing comma) is skipped.
    """
    assert text[start] == "{", "count_members must start at a brace"
    members: list[dict] = []
    absent: list[str] = []
    stack: list[tuple[str, str]] = []            # ("absent", directive) or ("cond", directive)
    cur: list[str] = []
    depth = 1
    i = start + 1
    n = len(text)
    at_line_start = False

    def in_absent() -> bool:
        return any(kind == "absent" for kind, _ in stack)

    def cond_text() -> str:
        return " && ".join(d for kind, d in stack if kind == "cond")

    def flush():
        t = _collapse("".join(cur))
        cur.clear()
        if not t:
            return
        if in_absent():
            absent.append(t)
        else:
            members.append({"index": len(members) + 1, "text": t, "cond": cond_text()})

    while i < n:
        c = text[i]
        if at_line_start:
            at_line_start = False
            j = i
            while j < n and text[j] in " \t":
                j += 1
            if j < n and text[j] == "#":
                k = text.find("\n", j)
                k = n if k == -1 else k
                d = _collapse(text[j:k])
                word = re.sub(r"^#\s*", "#", d).split()[0] if d else "#"
                if re.match(r"#if\s+0\b", re.sub(r"^#\s*", "#", d)):
                    flush()
                    stack.append(("absent", d))
                elif word in ("#if", "#ifdef", "#ifndef"):
                    flush()
                    stack.append(("cond", d))
                elif word == "#elif":
                    flush()
                    if stack:
                        stack[-1] = ("cond", d)
                elif word == "#else":
                    flush()
                    if stack:
                        kind, prev = stack[-1]
                        stack[-1] = ("cond", "#else of " + prev)
                elif word == "#endif":
                    flush()
                    if stack:
                        stack.pop()
                i = k + 1
                at_line_start = True
                continue
        if c == "\n":
            cur.append(c)
            at_line_start = True
            i += 1
            continue
        if text.startswith("//", i):
            k = text.find("\n", i)
            k = n if k == -1 else k
            content = text[i + 2:k].strip()
            if content.startswith("{"):
                absent.append(_collapse(content))
            i = k
            continue
        if text.startswith("/*", i):
            k = text.find("*/", i + 2)
            k = n if k == -1 else k + 2
            content = text[i + 2:k - 2].strip()
            if content.startswith("{"):
                absent.append(_collapse(content))
            i = k
            continue
        if c in "\"'":
            q = c
            k = i + 1
            while k < n and text[k] != q:
                k += 2 if text[k] == "\\" else 1
            cur.append(text[i:k + 1])
            i = k + 1
            continue
        if c == "{":
            depth += 1
            cur.append(c)
        elif c == "}":
            depth -= 1
            if depth == 0:
                flush()
                break
            cur.append(c)
        elif c == "," and depth == 1:
            flush()
        else:
            cur.append(c)
        i += 1
    return members, absent


# ---------------------------------------------------------------- enumerators

def struct_map(tree: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for rel in walk_tree(tree):
        if os.path.splitext(rel)[1].lower() in CODE_EXT:
            text = read_text(os.path.join(tree, rel))
            for m in TYPEDEF_STRUCT_RE.finditer(text):
                out[m.group(2)] = m.group(1)
            for m in STRUCT_RE.finditer(text):
                out.setdefault(m.group(1), m.group(2))
    return out


def _element_type(prefix: str) -> str:
    words = [w for w in _collapse(prefix).replace("*", " * ").split() if w not in ("static", "const", "extern")]
    return _collapse(" ".join(words)).replace(" *", " *").replace("* ", "*")


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _code_candidates(tree: str, rel: str, text: str, structs: dict[str, str]) -> list[dict]:
    rows = []
    seen_lines = set()
    for m in K2_FN_RE.finditer(text):
        brace = m.end() - 1
        present, absent = count_members(text, brace)
        rows.append(_row(rel, _line_of(text, m.start()), m.group(2), "K2", _collapse(m.group(1)) + " (*)()", present, absent))
        seen_lines.add(_line_of(text, m.start()))
    for m in K1_RE.finditer(text):
        line = _line_of(text, m.start())
        if line in seen_lines:
            continue
        brace = m.end() - 1
        present, absent = count_members(text, brace)
        if "{" in m.group(1):                      # anonymous struct element type
            etype = "struct {" + _collapse(m.group(1).split("{", 1)[1].rsplit("}", 1)[0]) + "}"
            klass = "K2" if "(*" in m.group(1) else "K1"
        else:
            etype = _element_type(m.group(1))
            base = etype.replace("*", "").replace("struct", "").strip().split()[-1] if etype.strip() else ""
            klass = "K2" if "(*" in structs.get(base, "") else "K1"
        rows.append(_row(rel, line, m.group(2), klass, etype, present, absent))
    for m in K3_DEFINE_RE.finditer(text):
        k = m.end()
        calls = []
        while True:
            e = text.find("\n", k)
            e = len(text) if e == -1 else e
            line = text[k:e]
            cm = K3_CALL_RE.match(line)
            if not cm:
                break
            calls.append(cm.group(1))
            k = e + 1
            if not line.rstrip().endswith("\\") or k >= len(text):
                break
        if len(calls) >= 2 and len(set(calls)) == 1:
            rows.append({"file": rel, "line": str(_line_of(text, m.start())), "symbol": m.group(1), "class": "K3",
                         "element_type": calls[0], "members": str(len(calls)), "absent": "0", "conditional": "0"})
    return rows


def _row(rel, line, symbol, klass, etype, present, absent) -> dict:
    return {"file": rel, "line": str(line), "symbol": symbol, "class": klass, "element_type": etype,
            "members": str(len(present)), "absent": str(len(absent)),
            "conditional": str(sum(1 for p in present if p["cond"]))}


def _doc_candidates(rel: str, text: str) -> list[dict]:
    rows = []
    for sentence_m in re.finditer(r"[^.!?\n][^.!?]*[.!?]?", text):
        sentence = sentence_m.group(0)
        if K4_RE.search(sentence):
            line = _line_of(text, sentence_m.start())
            rows.append({"file": rel, "line": str(line), "symbol": "doc:%s:%d" % (rel, line), "class": "K4",
                         "element_type": "", "members": "", "absent": "", "conditional": "",
                         "evidence": _collapse(sentence)})
    return rows


def enumerators(tree: str) -> list[dict]:
    structs = struct_map(tree)
    links = readme_links(tree)
    code, docs = [], []
    for rel in walk_tree(tree):
        if is_quarantined(rel):
            continue
        ext = os.path.splitext(rel)[1].lower()
        if ext in CODE_EXT:
            code += _code_candidates(tree, rel, read_text(os.path.join(tree, rel)), structs)
        elif is_s_doc(rel, links):
            docs += _doc_candidates(rel, read_text(os.path.join(tree, rel)))
    code.sort(key=lambda r: (r["file"], int(r["line"])))
    docs.sort(key=lambda r: (r["file"], int(r["line"])))
    rows = []
    for prefix, group in (("C", code), ("D", docs)):
        for k, r in enumerate(group, 1):
            full = {f: "" for f in EN_FIELDS}
            full.update(r)
            full["cand_id"] = "%s%03d" % (prefix, k)
            rows.append(full)
    return rows


# ---------------------------------------------------------------- CLI

def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "sources":
        rows = sources(argv[1])
        write_tsv(argv[2], rows, SRC_FIELDS)
        print("sources: %d rows, %d quarantined" % (len(rows), sum(r["decision"] == "QUARANTINED" for r in rows)))
        return 0
    if len(argv) == 3 and argv[0] == "enumerators":
        rows = enumerators(argv[1])
        write_tsv(argv[2], rows, EN_FIELDS)
        by = {k: sum(r["class"] == k for r in rows) for k in ("K1", "K2", "K3", "K4")}
        print("enumerators: %d rows -- %s" % (len(rows), " ".join("%s=%d" % kv for kv in by.items())))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
