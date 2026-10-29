"""Structural checks on the study's tables and documents.

    python -I checks.py <sub> <dir>      dir = phase3_5/exploratory

Subcommands (exit code 0 = pass, 1 = a problem was printed):
    inventory   inventory_sources.tsv and inventory_enumerators.tsv are fully decided
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_tsv  # noqa: E402

EN_COLS = ["en1", "en2", "en3", "en4", "en5", "en6"]


def _inventory(d: str) -> int:
    problems = []
    src = read_tsv(os.path.join(d, "inventory_sources.tsv"))
    n_adm = n_rej = n_q = 0
    for r in src:
        dec = r.get("decision", "")
        if dec == "QUARANTINED":
            n_q += 1
        elif dec in ("ADMIT", "REJECT"):
            n_adm += dec == "ADMIT"
            n_rej += dec == "REJECT"
            if not r.get("reason", "").strip():
                problems.append("sources %s: %s without a reason" % (r["path"], dec))
        else:
            problems.append("sources %s: undecided (decision=%r)" % (r["path"], dec))
    en = read_tsv(os.path.join(d, "inventory_enumerators.tsv"))
    admitted = {"enforced": 0, "asserted": 0}
    rejected_by = [0] * 6
    for r in en:
        vals = [r.get(c, "") for c in EN_COLS]
        if any(v not in ("PASS", "FAIL", "") for v in vals):
            problems.append("enumerators %s: EN cell outside {PASS, FAIL, ''}: %r" % (r["cand_id"], vals))
            continue
        if "FAIL" in vals:
            k = vals.index("FAIL")
            if vals.count("FAIL") != 1 or any(v != "PASS" for v in vals[:k]) or any(v != "" for v in vals[k + 1:]):
                problems.append("enumerators %s: a REJECT row needs PASS..PASS FAIL ''..'' -- got %r" % (r["cand_id"], vals))
                continue
            if not r.get("reject_reason", "").strip():
                problems.append("enumerators %s: FAIL without reject_reason" % r["cand_id"])
            rejected_by[k] += 1
        elif all(v == "PASS" for v in vals):
            if r.get("tag", "") not in admitted:
                problems.append("enumerators %s: ADMIT row needs tag enforced|asserted -- got %r" % (r["cand_id"], r.get("tag", "")))
                continue
            if not r.get("evidence", "").strip():
                problems.append("enumerators %s: ADMIT row without evidence" % r["cand_id"])
            admitted[r["tag"]] += 1
        else:
            problems.append("enumerators %s: undecided -- %r" % (r["cand_id"], vals))
    for p in problems:
        print("PROBLEM " + p)
    print("sources: %d rows, %d admitted, %d rejected, %d quarantined" % (len(src), n_adm, n_rej, n_q))
    print("enumerators: %d rows, %d admitted (enforced %d, asserted %d), rejected by EN1..EN6: %s" % (
        len(en), sum(admitted.values()), admitted["enforced"], admitted["asserted"], rejected_by))
    return 1 if problems else 0


SUBS = {"inventory": _inventory}


def run(sub: str, d: str) -> int:
    if sub not in SUBS:
        print("unknown check %r; known: %s" % (sub, sorted(SUBS)))
        return 2
    return SUBS[sub](d)


if __name__ == "__main__":
    sys.exit(run(sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else 2)
