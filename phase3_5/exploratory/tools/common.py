"""Shared helpers for the exploratory C084 study's tools.

Every tool is run as `python -I <tool>.py ...` with the target tree's
path as an argument; the tree is data and is never imported. Network
reads go through `api_get`, which decodes JSON and nothing else; what a
caller may keep from a response is decided by `strip`, so that titles,
bodies and commit messages are discarded before anything is displayed
(design Sections 4.2 and 5.1).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request

# Design Section 5.1: in-tree files whose purpose is to record failures or
# deficiencies, by file-name stem, any case, on the file name and on every
# directory component.
QUARANTINE_RE = re.compile(r"^(NEWS|CHANGELOG|HISTORY|RELEASE|NOT-BUGS|BUGS|KNOWN|TODO|CHANGES)([^A-Z]|$)")

USER_AGENT = "red-team-spike-exploratory-c084 (python urllib)"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_tree(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        for name in filenames:
            out.append(name if rel == "." else rel + "/" + name)
    return sorted(out)


def is_quarantined(relpath: str) -> bool:
    for comp in relpath.replace("\\", "/").split("/"):
        if QUARANTINE_RE.match(comp.split(".", 1)[0].upper()):
            return True
    return False


def read_tsv(path: str) -> list[dict[str, str]]:
    with open(path, encoding="utf-8", newline="\n") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    lines = [l for l in lines if not l.startswith("#")]
    if not lines:
        return []
    fields = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cells = line.split("\t")
        cells += [""] * (len(fields) - len(cells))
        rows.append(dict(zip(fields, cells)))
    return rows


def write_tsv(path: str, rows: list[dict[str, str]], fields: list[str], comment: str = "") -> None:
    lines = []
    if comment:
        lines.append("# " + comment)
    lines.append("\t".join(fields))
    for row in rows:
        cells = [str(row.get(f, "")) for f in fields]
        for c in cells:
            if "\t" in c or "\n" in c or "\r" in c:
                raise ValueError("tab or newline inside a cell: %r" % c[:60])
        lines.append("\t".join(cells))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def http_fetch(url: str) -> tuple[int, dict, bytes]:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def _header(headers: dict, name: str) -> str:
    for k, v in headers.items():
        if k.lower() == name.lower():
            return str(v)
    return "?"


def api_get(url: str, fetch=None) -> object:
    status, headers, body = (fetch or http_fetch)(url)
    if status in (403, 429):
        raise RuntimeError("rate limited until %s (HTTP %d for %s)" % (_header(headers, "X-RateLimit-Reset"), status, url))
    if status != 200:
        raise RuntimeError("HTTP %d for %s" % (status, url))
    return json.loads(body.decode("utf-8"))


def strip(obj: dict, keep: tuple[str, ...]) -> dict:
    out = {}
    for k in keep:
        if k not in obj:
            continue
        v = obj[k]
        if k == "labels":
            out[k] = [{"name": lab.get("name", ""), "description": lab.get("description") or ""} for lab in v]
        elif k == "pull_request":
            out[k] = True
        else:
            out[k] = v
    return out
