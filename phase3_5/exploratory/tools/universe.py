"""X6 universe tool (design Section 6.3; XQA-07 c).

    python -I universe.py members <tree> <inventory_enumerators.tsv> <observations.tsv> [enumerator_bounds.tsv]
    python -I universe.py units <observations.tsv> <crosslinks.tsv> <P_raw.tsv>

`members` enumerates, for every ADMIT row of class K1-K3, one source
observation per present member of its initializer; commented-out and
`#if 0` members are ABSENT (printed, not written), and a FINAL member
that is only a terminator (NULL, nil, 0, -1, or a brace row of those)
is a SENTINEL (printed, not written); rows beyond the bound the
consulting loop uses, when a committed enumerator_bounds.tsv names one
(cand_id, bound, evidence; XQA-08), are OUT-OF-BOUND (printed, not
written). `units` turns observations and
the externally declared cross-link edges into counting units: each
connected component is one unit (sealed Section 4.2).
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_tsv, write_tsv  # noqa: E402
from inventory import count_members, read_text  # noqa: E402

OBS_FIELDS = ["obs_id", "enum_id", "tag", "file", "line", "index", "text", "cond"]
UNIT_FIELDS = ["unit_id", "obs_ids", "enum_ids", "tags", "linked", "text"]
SENTINEL_TOKENS = {"NULL", "nil", "0", "-1"}


def is_sentinel(text: str) -> bool:
    toks = [t for t in re.split(r"[\s,{}]+", text) if t]
    return bool(toks) and all(t in SENTINEL_TOKENS for t in toks)


def _brace_after_line(text: str, line: int) -> int:
    start = 0
    for _ in range(line - 1):
        start = text.index("\n", start) + 1
    m = re.compile(r"=\s*\{").search(text, start)
    if m is None:
        raise ValueError("no initializer brace after line %d" % line)
    return m.end() - 1


def members_detail(tree: str, enumerators_tsv: str, bounds_tsv: str | None = None):
    rows, absent, sentinels, beyond = [], [], [], []
    bounds = {b["cand_id"]: int(b["bound"]) for b in read_tsv(bounds_tsv)} if bounds_tsv else {}
    for r in read_tsv(enumerators_tsv):
        if r.get("tag", "") not in ("enforced", "asserted") or r.get("class", "") not in ("K1", "K2", "K3"):
            continue
        text = read_text(os.path.join(tree, r["file"]))
        present, gone = count_members(text, _brace_after_line(text, int(r["line"])))
        absent += [(r["cand_id"], a) for a in gone]
        if present and is_sentinel(present[-1]["text"]):
            sentinels.append((r["cand_id"], present[-1]["text"]))
            present = present[:-1]
        bound = bounds.get(r["cand_id"])
        if bound is not None and len(present) > bound:
            beyond += [(r["cand_id"], m["text"]) for m in present[bound:]]
            present = present[:bound]
        for m in present:
            rows.append({"obs_id": "E%s-%03d" % (r["cand_id"][1:], m["index"]), "enum_id": r["cand_id"],
                         "tag": r["tag"], "file": r["file"], "line": str(text.count("\n", 0, m["pos"]) + 1),
                         "index": str(m["index"]), "text": m["text"], "cond": m["cond"]})
    return rows, absent, sentinels, beyond


def members(tree: str, enumerators_tsv: str, bounds_tsv: str | None = None) -> list[dict]:
    return members_detail(tree, enumerators_tsv, bounds_tsv)[0]


def units(observations_tsv: str, crosslinks_tsv: str, out_tsv: str) -> tuple[int, int, int]:
    obs = read_tsv(observations_tsv)
    by_id = {o["obs_id"]: o for o in obs}
    parent = {k: k for k in by_id}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in read_tsv(crosslinks_tsv):
        a, b = e["obs_a"], e["obs_b"]
        if a not in by_id or b not in by_id:
            raise ValueError("cross-link names an unknown observation: %s -- %s" % (a, b))
        parent[find(a)] = find(b)
    comps: dict[str, list[str]] = {}
    for k in by_id:
        comps.setdefault(find(k), []).append(k)
    ordered = sorted((sorted(v) for v in comps.values()), key=lambda c: c[0])
    rows = []
    for n, ids in enumerate(ordered, 1):
        members_ = [by_id[i] for i in ids]
        rows.append({"unit_id": "U%03d" % n, "obs_ids": ",".join(ids),
                     "enum_ids": ",".join(sorted({m["enum_id"] for m in members_})),
                     "tags": ",".join(sorted({m["tag"] for m in members_})),
                     "linked": "1" if len(ids) > 1 else "0",
                     "text": " || ".join(m["text"] for m in members_)})
    write_tsv(out_tsv, rows, UNIT_FIELDS)
    return len(obs), len(rows), sum(1 for r in rows if r["linked"] == "1")


def main(argv: list[str]) -> int:
    if len(argv) in (4, 5) and argv[0] == "members":
        rows, absent, sentinels, beyond = members_detail(argv[1], argv[2], argv[4] if len(argv) == 5 else None)
        write_tsv(argv[3], rows, OBS_FIELDS)
        for cand, t in absent:
            print("ABSENT %s %s" % (cand, t))
        for cand, t in sentinels:
            print("SENTINEL %s %s" % (cand, t))
        for cand, t in beyond:
            print("OUT-OF-BOUND %s %s" % (cand, t))
        print("observations=%d absent=%d sentinels=%d out_of_bound=%d enumerators=%d" % (
            len(rows), len(absent), len(sentinels), len(beyond), len({r["enum_id"] for r in rows})))
        return 0
    if len(argv) == 4 and argv[0] == "units":
        o, p, linked = units(argv[1], argv[2], argv[3])
        print("O_raw=%d P_raw=%d linked_units=%d" % (o, p, linked))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
