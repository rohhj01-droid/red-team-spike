"""The frozen verdict grammar (preregistration design Section 6; contract Section 8).

Decides the EN1-EN6 verdicts of every enumerator candidate the exploratory inventory
tool generates, for every survivor alike, BEFORE any survivor's tree is seen. A
candidate is decided either by a named GENERIC catalogue rule (element type, role
vocabulary of the symbol, generic file role, candidate class, dead code) or left
UNDECIDED for the analyst's quoted, located verdict. Every ADMIT and every quoted
verdict must cite file:line. Nothing here names a project-specific file or symbol.

Order of the catalogue is part of the grammar: the first matching rule decides.
"""
from __future__ import annotations

import os
import re
from typing import Callable

RULE_KINDS_FORBIDDEN = {"file_name", "symbol_exact"}
EN = ("en1", "en2", "en3", "en4", "en5", "en6")
CITE_RE = re.compile(r"[\w./-]+\.[A-Za-z]{1,4}:\d+")
QUALIFIERS = {"static", "const", "extern", "volatile", "register", "struct", "enum", "signed"}
NUMERIC_BASES = {"int", "unsigned", "short", "long", "float", "double", "char", "fixed_t", "byte", "angle_t",
                 "size_t", "boolean", "bool", "uint8_t", "uint16_t", "uint32_t", "uint64_t", "int8_t", "int16_t",
                 "int32_t", "int64_t", "fixed", "dboolean", "pixel_t"}
FILE_ROLE_DIRS = ("test", "tests", "t", "fixtures", "fixture", "examples", "example", "samples", "sample", "doc", "docs")
PRESENTATION_RE = re.compile(r"(label|msg|message|text|title|desc|hint|tip|menu|caption|help|lang|loc|banner|credit|quote)", re.I)
MAPPING_RE = re.compile(r"(lookup|xlat|translat|convert|rename|alias|mapping|_to_)", re.I)


class Rule:
    __slots__ = ("name", "kind", "test", "en", "reason")

    def __init__(self, name: str, kind: str, test: Callable[[dict, dict], bool], en: str, reason: str):
        self.name, self.kind, self.test, self.en, self.reason = name, kind, test, en, reason


# ---------------------------------------------------------------- context helpers (tree-dependent, optional)

def _file_text(ctx: dict, rel: str) -> str:
    tree = ctx.get("tree")
    if not tree:
        return ""
    cache = ctx.setdefault("_text", {})
    if rel not in cache:
        p = os.path.join(tree, rel)
        cache[rel] = open(p, "rb").read().decode("utf-8", errors="replace") if os.path.exists(p) else ""
    return cache[rel]


def dead_at(text: str, lineno: int) -> bool:
    """True when `lineno` (1-based) lies inside `#if 0` (before its #else) or inside a block comment."""
    depth_zero = []            # stack of booleans: True when the enclosing #if is a dead `#if 0` branch
    in_comment = False
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if n == lineno:
            return in_comment or any(depth_zero)
        if not in_comment:
            m = re.match(r"#\s*(if|ifdef|ifndef|elif|else|endif)\b\s*(.*)", s)
            if m:
                kw, rest = m.group(1), m.group(2).strip()
                if kw in ("if",):
                    depth_zero.append(rest.split("//")[0].strip() in ("0", "(0)"))
                elif kw in ("ifdef", "ifndef"):
                    depth_zero.append(False)
                elif kw == "elif":
                    if depth_zero:
                        depth_zero[-1] = False
                elif kw == "else":
                    if depth_zero:
                        depth_zero[-1] = not depth_zero[-1] if depth_zero[-1] else False
                elif kw == "endif":
                    if depth_zero:
                        depth_zero.pop()
                continue
        i = 0
        while i < len(line):
            if in_comment:
                j = line.find("*/", i)
                if j < 0:
                    break
                in_comment, i = False, j + 2
            else:
                j, k = line.find("/*", i), line.find("//", i)
                if k >= 0 and (j < 0 or k < j):
                    break
                if j < 0:
                    break
                in_comment, i = True, j + 2
    return False


def _base_tokens(element_type: str) -> list[str]:
    return [t for t in re.findall(r"[A-Za-z_]\w*", element_type) if t not in QUALIFIERS]


def _is_string_type(et: str) -> bool:
    return "*" in et and ("char" in et or "NSString" in et or "wchar_t" in et or "string" in et.lower())


def _is_numeric_type(et: str) -> bool:
    if "*" in et or "{" in et or "(" in et:
        return False
    toks = _base_tokens(et)
    return bool(toks) and all(t in NUMERIC_BASES for t in toks)


def _struct_has_fn_pointer(row: dict, ctx: dict) -> bool:
    et = row.get("element_type", "")
    if "(*" in et:
        return True
    if "{" in et:
        return "(*" in et
    tree = ctx.get("tree")
    if not tree:
        return False
    smap = ctx.get("_structs")
    if smap is None:
        try:
            import inventory  # exploratory tool, on sys.path through paths.use_exploratory_tools()
            smap = inventory.struct_map(tree)
        except Exception:
            smap = {}
        ctx["_structs"] = smap
    toks = _base_tokens(et)
    return any("(*" in smap.get(t, "") for t in toks)


def _file_role(row: dict) -> str | None:
    parts = row.get("file", "").replace("\\", "/").split("/")[:-1]
    return next((p for p in parts if p.lower() in FILE_ROLE_DIRS), None)


def _generated(row: dict, ctx: dict) -> bool:
    f = row.get("file", "")
    if f.endswith((".gen.c", ".gen.h", "_gen.c", "_gen.h")):
        return True
    head = _file_text(ctx, f).split("\n")[:3]
    return any("generated" in l.lower() for l in head)


# ---------------------------------------------------------------- the catalogue (first match decides)

CATALOGUE: list[Rule] = [
    Rule("dead-code", "dead_code", lambda r, c: dead_at(_file_text(c, r["file"]), int(r["line"])), "EN2",
         "the initializer lies in dead code (#if 0 or a block comment): not a set the program consults"),
    Rule("test-fixture", "file_role", lambda r, c: _file_role(r) is not None, "EN2",
         "a file under a test / fixture / example / documentation directory: test or example data, not an accepted-input set"),
    Rule("generated-code", "file_role", _generated, "EN2",
         "generated code: the set is a build product, identified as such by its file"),
    Rule("build-system", "file_role", lambda r, c: os.path.basename(r.get("file", "")) in ("CMakeLists.txt",) or r.get("file", "").endswith((".mk", "configure", "configure.ac")), "EN2",
         "a build-system file: not program input"),
    Rule("dispatch-table", "candidate_class", lambda r, c: r.get("class") == "K2" or _struct_has_fn_pointer(r, c), "EN2",
         "a dispatch table (function pointers): a mapping from a key to code, not a set of accepted values"),
    Rule("numeric-data", "element_type", lambda r, c: _is_numeric_type(r.get("element_type", "")), "EN2",
         "a numeric table (plain arithmetic element type): data, not an accepted-input set"),
    Rule("presentation-vocabulary", "vocabulary", lambda r, c: _is_string_type(r.get("element_type", "")) and bool(PRESENTATION_RE.search(r.get("symbol", ""))), "EN2",
         "a string table whose symbol names presentation (labels, messages, text, menus, help): display, not acceptance"),
    Rule("mapping-vocabulary", "vocabulary", lambda r, c: bool(MAPPING_RE.search(r.get("symbol", ""))), "EN2",
         "a table whose symbol names a mapping or translation (lookup, rename, alias, convert): a mapping, not an accepted-input set"),
]


def decide(row: dict, tree: str | None = None) -> dict:
    """Apply the catalogue to one inventory row. K1-K3 rows pass EN1, EN3, EN5, EN6 by construction (compiled-in
    arrays); K4 (document) rows are always UNDECIDED. Returns a new row with en1..en6, tag, reject_reason, decided_by."""
    out = dict(row)
    ctx = {"tree": tree}
    for k in EN:
        out[k] = ""
    out["tag"], out["reject_reason"], out["evidence"] = "", "", out.get("evidence", "")
    if row.get("class") == "K4":
        out["decided_by"] = "UNDECIDED"
        return out
    for k in ("en1", "en3", "en5", "en6"):
        out[k] = "PASS"
    for rule in CATALOGUE:
        try:
            hit = rule.test(row, ctx)
        except Exception:
            hit = False
        if hit:
            if rule.en == "EN2":
                out["en2"] = "FAIL"
            else:
                out["en2"], out["en4"] = "PASS", "FAIL"
            out["reject_reason"] = "%s: %s" % (rule.en, rule.reason)
            out["decided_by"] = "catalogue:" + rule.name
            return out
    out["decided_by"] = "UNDECIDED"
    return out


def apply_quoted(rows: list[dict], quoted: list[dict]) -> list[dict]:
    """Merge the analyst's quoted verdicts: {cand_id, verdict ADMIT | REJECT-EN2 | REJECT-EN4, tag, evidence}.
    Every quoted verdict must cite file:line; an ADMIT must carry tag enforced | asserted."""
    by_id = {q["cand_id"]: q for q in quoted}
    out = []
    for r in rows:
        q = by_id.get(r["cand_id"])
        if q is None:
            out.append(dict(r))
            continue
        if not CITE_RE.search(q.get("evidence", "")):
            raise ValueError("quoted verdict for %s cites no file:line" % r["cand_id"])
        n = dict(r)
        v = q["verdict"]
        if v == "ADMIT":
            if q.get("tag") not in ("enforced", "asserted"):
                raise ValueError("ADMIT for %s needs tag enforced | asserted" % r["cand_id"])
            for k in EN:
                n[k] = "PASS"
            n["tag"], n["reject_reason"] = q["tag"], ""
        elif v == "REJECT-EN2":
            n["en2"], n["en4"], n["tag"], n["reject_reason"] = "FAIL", "", "", "EN2: " + q["evidence"]
        elif v == "REJECT-EN4":
            n["en2"], n["en4"], n["tag"], n["reject_reason"] = "PASS", "FAIL", "", "EN4: " + q["evidence"]
        else:
            raise ValueError("unknown verdict %r for %s" % (v, r["cand_id"]))
        n["evidence"], n["decided_by"] = q["evidence"], "quoted"
        out.append(n)
    return out


def is_admitted(row: dict) -> bool:
    return all(row.get(k) == "PASS" for k in EN) and row.get("tag") in ("enforced", "asserted")


def class_of(rows: list[dict]) -> str:
    """A iff at least one admitted enforcement enumerator and every admitted one is `enforced`; else B."""
    admitted = [r for r in rows if is_admitted(r)]
    return "A" if admitted and all(r["tag"] == "enforced" for r in admitted) else "B"


def sensitivity(rows: list[dict]) -> list[dict]:
    """The rows whose reversal could move the class: admitted rows; EN2-PASS / EN4-FAIL rows; rows decided by quotation."""
    out = []
    for r in rows:
        why = []
        if is_admitted(r):
            why.append("admitted")
        if r.get("en2") == "PASS" and r.get("en4") == "FAIL":
            why.append("EN2 PASS, EN4 FAIL")
        if r.get("decided_by") == "quoted" and not is_admitted(r):
            why.append("decided by quotation")
        if why:
            out.append(dict(r, why="; ".join(why)))
    return out
