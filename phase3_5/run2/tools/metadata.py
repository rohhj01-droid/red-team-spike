"""The frozen-metadata resolver (contract Section 2; QA-39, QA-40).

Reads a port's Makefile, distinfo and pkg/DESCR from the frozen tree and resolves
HOMEPAGE and SITES by exactly the mechanisms the contract lists: explicit lines
(with SITE_* macros expanded from the frozen network.conf.template and the
`${NAME:=suffix}` modifier), GH_ACCOUNT/GH_PROJECT defaults (bsd.port.mk), and
DIST_TUPLE templates (dist-tuple.port.mk + dist-tuple.pattern). Not a `make`
evaluation. A `MODULES` line, or a `${...}` left unexpanded, makes the item
PI-METADATA-UNRESOLVED; nothing is guessed.
"""
from __future__ import annotations

import io
import os
import re

DECLARED_MODULES: list[str] = []            # contract Section 2: no module beyond bsd.port.mk / dist-tuple is resolved
ASSIGN_RE = re.compile(r"^([A-Za-z_][\w.]*)[ \t]*(\?=|\+=|:=|=)[ \t]*(.*)$")
MACRO_RE = re.compile(r"\$\{([A-Za-z_][\w.]*)(?::=([^}]*))?\}")
PI_METADATA = "PI-METADATA-UNRESOLVED"
TUPLE_SITES = {"github": "https://github.com/", "gitlab": "https://gitlab.com/", "codeberg": "https://codeberg.org/"}


def _read(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def _join_continuations(text: str) -> list[str]:
    out, buf = [], ""
    for line in text.splitlines():
        if line.rstrip().endswith("\\"):
            buf += line.rstrip()[:-1] + " "
            continue
        out.append(buf + line)
        buf = ""
    if buf:
        out.append(buf)
    return out


def parse_assignments(text: str) -> dict[str, str]:
    """NAME = value lines (continuations joined); `+=` appends, the others replace. Comments stripped."""
    vals: dict[str, str] = {}
    for line in _join_continuations(text):
        line = line.split("#", 1)[0] if not line.lstrip().startswith("#") else ""
        m = ASSIGN_RE.match(line.strip())
        if not m:
            continue
        name, op, value = m.group(1), m.group(2), m.group(3).strip()
        if op == "+=":
            vals[name] = (vals.get(name, "") + " " + value).strip()
        elif op == "?=" and name in vals:
            continue
        else:
            vals[name] = value
    return vals


MACRO_FILES = (os.path.join("db", "network.conf"), os.path.join("templates", "network.conf.template"))


def macro_table(infra_root: str) -> dict[str, str]:
    """SITE_* macros from the frozen tree's macro file (infrastructure/db/network.conf in the 7.9 tree; the
    template path the contract named does not exist there -- RQA-02), each as its whitespace-joined word list."""
    for rel in MACRO_FILES:
        text = _read(os.path.join(infra_root, rel))
        if text:
            return {k: v for k, v in parse_assignments(text).items() if k.startswith("SITE")}
    return {}


def tuple_sites(infra_root: str) -> dict[str, str]:
    """SITES.<template> from the frozen dist-tuple.pattern, falling back to the contract's three."""
    text = _read(os.path.join(infra_root, "db", "dist-tuple.pattern"))
    out = dict(TUPLE_SITES)
    for k, v in parse_assignments(text).items():
        if k.startswith("SITES."):
            out[k[len("SITES."):]] = v
    return out


def expand(value: str, macros: dict[str, str]) -> str:
    """Expand ${NAME} and ${NAME:=suffix} (each word of NAME with suffix appended); unknown names stay as written."""
    def sub(m: re.Match) -> str:
        name, suffix = m.group(1), m.group(2)
        if name not in macros:
            return m.group(0)
        words = macros[name].split()
        return " ".join(w + (suffix or "") for w in words)
    prev, cur = None, value
    for _ in range(8):                      # nested references, bounded
        if prev == cur:
            break
        prev, cur = cur, MACRO_RE.sub(sub, cur)
    return cur


def resolve(port_dir: str, infra_root: str) -> dict:
    mk = parse_assignments(_read(os.path.join(port_dir, "Makefile")))
    macros = dict(macro_table(infra_root))
    macros.update({k: v for k, v in mk.items() if "${" not in v})          # port-local simple values
    tsites = tuple_sites(infra_root)
    out: dict = dict(homepage=None, homepage_mechanism=None, sites=[], sites_mechanism={}, gh=None,
                     dist_tuples=[], modules=[], distname=None, comment=None, descr="", issue=None, unresolved=[])
    out["modules"] = mk.get("MODULES", "").split()
    out["distname"] = mk.get("DISTNAME") or None
    out["comment"] = mk.get("COMMENT") or None
    out["descr"] = _read(os.path.join(port_dir, "pkg", "DESCR"))
    acct, proj = mk.get("GH_ACCOUNT", ""), mk.get("GH_PROJECT", "")
    if acct and proj:
        out["gh"] = (acct, proj)
    words = mk.get("DIST_TUPLE", "").split()
    while len(words) >= 4:
        out["dist_tuples"].append(tuple(words[:4]))
        words = words[5:] if len(words) >= 5 else []
    unresolved = out["unresolved"]
    # HOMEPAGE
    if "HOMEPAGE" in mk:
        hp = expand(mk["HOMEPAGE"], macros)
        if "${" in hp:
            unresolved.append(hp)
        else:
            out["homepage"], out["homepage_mechanism"] = hp, "explicit"
    elif out["gh"]:
        out["homepage"], out["homepage_mechanism"] = "https://github.com/%s/%s" % out["gh"], "gh"
    elif out["dist_tuples"] and out["dist_tuples"][0][0] in tsites:
        site, a, p, _tag = out["dist_tuples"][0]
        out["homepage"], out["homepage_mechanism"] = tsites[site] + a + "/" + p, "dist-tuple"
    # SITES
    if "SITES" in mk:
        for w in expand(mk["SITES"], macros).split():
            if "${" in w:
                unresolved.append(w)
            else:
                out["sites"].append(w); out["sites_mechanism"][w] = "explicit"
    elif out["gh"]:
        base = "https://github.com/%s/%s/" % out["gh"]
        if mk.get("GH_TAGNAME"):
            url = base + "archive/refs/tags/%s/" % mk["GH_TAGNAME"]
            out["sites"].append(url); out["sites_mechanism"][url] = "gh-tagname"
        elif mk.get("GH_COMMIT"):
            url = base + "archive/"
            out["sites"].append(url); out["sites_mechanism"][url] = "gh-commit"
    for k, v in mk.items():
        if k.startswith("SITES."):
            for w in expand(v, macros).split():
                if "${" in w:
                    unresolved.append(w)
                else:
                    out["sites"].append(w); out["sites_mechanism"][w] = "group:" + k[len("SITES."):]
    # RQA-02 (a): a module makes the item unresolved only where it could be SUPPLYING a field the port's own
    # lines and the two bsd.port.mk / dist-tuple mechanisms did not resolve (HOMEPAGE missing, or SITES
    # missing with no GH pair and no DIST_TUPLE); a build-tool module beside explicit fields resolves nothing
    undeclared = [m for m in out["modules"] if m not in DECLARED_MODULES]
    field_gap = out["homepage"] is None or (not out["sites"] and not out["gh"] and not out["dist_tuples"])
    if (undeclared and field_gap) or unresolved:
        out["issue"] = PI_METADATA
    return out
