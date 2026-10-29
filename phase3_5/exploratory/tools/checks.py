"""Structural checks on the study's tables and documents.

    python -I checks.py <sub> <dir>      dir = phase3_5/exploratory

Subcommands (exit code 0 = pass, 1 = a problem was printed):
    inventory   inventory_sources.tsv and inventory_enumerators.tsv are fully decided
    units       every P_raw unit has one units.tsv row (RESOLVED or E?); E? rows have an E_LOG entry;
                named native cases exist in Artifact 1; prints coverage (units not yet analysed: pending)
    artifact1   Artifact 1 carries no Phase 3 role name; every NC section has the ten field lines,
                five cited sufficiency answers and a Status line
    artifact2   every RESOLVED native case has an Artifact 2 section with roles/reasoning/outcome,
                R0 with a competitor, F3 with positive evidence; E? cases listed as not classified;
                prints per-finding counts (native cases, counting units)
    artifact3   Artifact 3 has the applicability domain before the decision procedure, and totality:
    primary     PRIMARY_RESULT.md carries the coverage lines and the finding counts verbatim; no pending
    cost        cost_log.tsv has a complete row for every native case
    results     RESULTS.md is labelled EXPLORATORY, names Run 2 in its first paragraph, has 14.1..14.12
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_tsv  # noqa: E402

EN_COLS = ["en1", "en2", "en3", "en4", "en5", "en6"]
PHASE3_NAMES = ["WorldState", "MonitorState", "EventProvenanceState", "violation judgment", "event provenance"]
A1_FIELDS = ["source observation ids:", "native state/data involved:", "writers / creation points:",
             "updates / invalidation paths:", "readers / consumption points:",
             "lifetime / persistence / reset behavior:", "relevant transitions:",
             "supporting source-code/docs evidence:", "remaining native-level uncertainty:", "lineage:"]
Q_LINES = ["Q1 created:", "Q2 written:", "Q3 lifetime:", "Q4 readers:", "Q5 after consumption:"]
CITE_RE = re.compile(r"[\w./-]+\.[A-Za-z]{1,4}:\d+")
FINDINGS = ["R0", "F0", "F1", "F2", "F3"]
OUTCOME_RE = re.compile(r"^(R0|F0|(F[123])(\s*,\s*F[123])*)$")


def _read(d: str, name: str) -> str:
    with open(os.path.join(d, name), encoding="utf-8") as f:
        return f.read()


def _sections(text: str, prefix: str = "## ") -> list[tuple[str, str]]:
    """(heading, body) for every `## ` section."""
    out, head, buf = [], None, []
    for line in text.split("\n"):
        if line.startswith(prefix) and not line.startswith(prefix + "#"):
            if head is not None:
                out.append((head, "\n".join(buf)))
            head, buf = line[len(prefix):].strip(), []
        elif head is not None:
            buf.append(line)
    if head is not None:
        out.append((head, "\n".join(buf)))
    return out


def _nc_sections(text: str) -> dict[str, str]:
    return {h.split()[0]: b for h, b in _sections(text) if h.startswith("NC-")}


def _line_value(body: str, label: str) -> str | None:
    for line in body.split("\n"):
        if line.startswith(label):
            return line[len(label):].strip()
    return None


# ---------------------------------------------------------------- inventory

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


# ---------------------------------------------------------------- units / coverage

def _coverage(d: str):
    """Returns (problems, resolved, e_unresolved, p_raw, pending, units_rows)."""
    problems = []
    p_raw = read_tsv(os.path.join(d, "P_raw.tsv"))
    units = read_tsv(os.path.join(d, "units.tsv")) if os.path.exists(os.path.join(d, "units.tsv")) else []
    a1 = _nc_sections(_read(d, "ARTIFACT_1_native.md")) if os.path.exists(os.path.join(d, "ARTIFACT_1_native.md")) else {}
    elog = _read(d, "E_LOG.md") if os.path.exists(os.path.join(d, "E_LOG.md")) else ""
    elog_entries = {h.split()[1]: b for h, b in _sections(elog) if h.startswith("E? ")}
    by_unit: dict[str, list] = {}
    for u in units:
        by_unit.setdefault(u["unit_id"], []).append(u)
    ids = {r["unit_id"] for r in p_raw}
    for uid in by_unit:
        if uid not in ids:
            problems.append("units.tsv names %s, which is not in P_raw.tsv" % uid)
    resolved = e_unres = pending = 0
    for uid in sorted(ids):
        rows = by_unit.get(uid, [])
        if not rows:
            pending += 1
            continue
        if len(rows) > 1:
            problems.append("%s has %d rows in units.tsv" % (uid, len(rows)))
            continue
        u = rows[0]
        if u["status"] == "RESOLVED":
            resolved += 1
        elif u["status"] == "E?":
            e_unres += 1
            gaps = [g.strip() for g in u.get("e_gaps", "").split(",") if g.strip()]
            if not gaps or any(g not in ("Q1", "Q2", "Q3", "Q4", "Q5") for g in gaps):
                problems.append("%s: E? without gaps drawn from Q1..Q5 (%r)" % (uid, u.get("e_gaps", "")))
            entry = elog_entries.get(uid)
            if entry is None:
                problems.append("%s: E? without an E_LOG.md entry '## E? %s'" % (uid, uid))
            else:
                for lab in ("missing evidence:", "why recovery failed:", "opacity/tooling vs unmodeled structure:", "F2 re-check:"):
                    if not (_line_value(entry, lab) or ""):
                        problems.append("%s: E_LOG entry lacks '%s'" % (uid, lab))
        else:
            problems.append("%s: status %r is neither RESOLVED nor E?" % (uid, u["status"]))
        for nc in [n.strip() for n in u.get("native_cases", "").split(",") if n.strip()]:
            if nc not in a1:
                problems.append("%s names %s, which has no '## %s' section in Artifact 1" % (uid, nc, nc))
    return problems, resolved, e_unres, len(p_raw), pending, units


def _units(d: str) -> int:
    problems, r, u, m, pending, _ = _coverage(d)
    for p in problems:
        print("PROBLEM " + p)
    print("resolved %d / P_raw %d" % (r, m))
    print("E? %d / P_raw %d" % (u, m))
    if pending:
        print("pending %d (units with no units.tsv row yet)" % pending)
    return 1 if problems else 0


# ---------------------------------------------------------------- artifacts

def _artifact1(d: str) -> int:
    problems = []
    text = _read(d, "ARTIFACT_1_native.md")
    for name in PHASE3_NAMES:
        if name in text:
            problems.append("Artifact 1 contains the Phase 3 name %r" % name)
    secs = _nc_sections(text)
    if not secs:
        problems.append("Artifact 1 has no '## NC-' section")
    for nc, body in secs.items():
        for lab in A1_FIELDS:
            if _line_value(body, lab) is None:
                problems.append("%s: missing field line '%s'" % (nc, lab))
        for q in Q_LINES:
            v = _line_value(body, q)
            if v is None:
                problems.append("%s: missing '%s'" % (nc, q))
            elif not CITE_RE.search(v):
                problems.append("%s: '%s' has no file:line citation" % (nc, q))
        st = _line_value(body, "Status:")
        if st is None or not (st == "RESOLVED" or re.match(r"^E\? \((Q[1-5])(,\s*Q[1-5])*\)$", st)):
            problems.append("%s: Status line must be RESOLVED or 'E? (Q..)' -- got %r" % (nc, st))
    for p in problems:
        print("PROBLEM " + p)
    print("Artifact 1: %d native cases" % len(secs))
    return 1 if problems else 0


def _a2_counts(d: str):
    """Returns (problems, cases_per_finding, units_per_finding, outcomes_by_nc)."""
    problems = []
    a1 = _nc_sections(_read(d, "ARTIFACT_1_native.md"))
    a2_text = _read(d, "ARTIFACT_2_mapping.md")
    a2 = _nc_sections(a2_text)
    not_classified = ""
    for h, b in _sections(a2_text):
        if h.lower().startswith("not classified"):
            not_classified = b
    outcomes: dict[str, list[str]] = {}
    for nc, body in a1.items():
        status = _line_value(body, "Status:") or ""
        if status == "RESOLVED":
            if nc not in a2:
                problems.append("%s is RESOLVED in Artifact 1 but has no section in Artifact 2" % nc)
                continue
            sec = a2[nc]
            for lab in ("roles:", "reasoning:"):
                if not (_line_value(sec, lab) or ""):
                    problems.append("%s: Artifact 2 section lacks '%s'" % (nc, lab))
            out = _line_value(sec, "outcome:") or ""
            if not OUTCOME_RE.match(out):
                problems.append("%s: outcome must be R0, F0 or a list over F1,F2,F3 -- got %r" % (nc, out))
                continue
            findings = [f.strip() for f in out.split(",")]
            outcomes[nc] = findings
            if "R0" in findings and not (_line_value(sec, "competitor:") or ""):
                problems.append("%s: R0 without a named competitor" % nc)
            if "F3" in findings and not (_line_value(sec, "positive evidence:") or ""):
                problems.append("%s: F3 without positive evidence" % nc)
        else:
            if nc not in not_classified:
                problems.append("%s is E? in Artifact 1 but not listed under '## Not classified (E?)' in Artifact 2" % nc)
    units = read_tsv(os.path.join(d, "units.tsv")) if os.path.exists(os.path.join(d, "units.tsv")) else []
    cases = {f: 0 for f in FINDINGS}
    unit_sets = {f: set() for f in FINDINGS}
    for nc, fs in outcomes.items():
        for f in fs:
            cases[f] += 1
            for u in units:
                if nc in [n.strip() for n in u.get("native_cases", "").split(",")]:
                    unit_sets[f].add(u["unit_id"])
    return problems, cases, {f: len(s) for f, s in unit_sets.items()}, outcomes


def _artifact2(d: str) -> int:
    problems, cases, units, _ = _a2_counts(d)
    for p in problems:
        print("PROBLEM " + p)
    print("native cases: " + ", ".join("%s %d" % (f, cases[f]) for f in FINDINGS))
    print("counting units: " + ", ".join("%s %d" % (f, units[f]) for f in FINDINGS))
    return 1 if problems else 0


def _artifact3(d: str) -> int:
    problems = []
    text = _read(d, "ARTIFACT_3_judgment.md")
    i = text.find("## Applicability domain")
    j = text.find("## Decision procedure")
    if i < 0 or j < 0 or not i < j:
        problems.append("Artifact 3 needs '## Applicability domain' before '## Decision procedure'")
    elif "totality:" not in text[j:]:
        problems.append("Artifact 3's decision procedure lacks a 'totality:' line")
    for p in problems:
        print("PROBLEM " + p)
    return 1 if problems else 0


def _primary(d: str) -> int:
    problems, r, u, m, pending, _ = _coverage(d)
    if pending:
        problems.append("%d units are still pending; the primary result cannot be sealed" % pending)
    text = _read(d, "PRIMARY_RESULT.md")
    for line in ("resolved %d / P_raw %d" % (r, m), "E? %d / P_raw %d" % (u, m)):
        if line not in text:
            problems.append("PRIMARY_RESULT.md lacks the line %r" % line)
    a2_problems, cases, units, _ = _a2_counts(d)
    problems += a2_problems
    rows = {mm.group(1): (int(mm.group(2)), int(mm.group(3)))
            for mm in re.finditer(r"^\|\s*(R0|F0|F1|F2|F3)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", text, re.M)}
    for f in FINDINGS:
        if f not in rows:
            problems.append("PRIMARY_RESULT.md findings table lacks a row for %s" % f)
        elif rows[f] != (cases[f], units[f]):
            problems.append("PRIMARY_RESULT.md row %s = %s, Artifact 2 says (%d, %d)" % (f, rows[f], cases[f], units[f]))
    for p in problems:
        print("PROBLEM " + p)
    return 1 if problems else 0


def _cost(d: str) -> int:
    problems = []
    a1 = _nc_sections(_read(d, "ARTIFACT_1_native.md"))
    rows = read_tsv(os.path.join(d, "cost_log.tsv"))
    fields = ["id", "session_start_utc", "session_end_utc", "first_commit", "accepted_by", "accepted_utc"]
    for nc in a1:
        mine = [r for r in rows if r.get("id") == nc]
        if not mine:
            problems.append("cost_log.tsv has no row for %s" % nc)
        for r in mine:
            for f in fields:
                if not r.get(f, "").strip():
                    problems.append("cost_log.tsv %s: empty %s" % (nc, f))
    for p in problems:
        print("PROBLEM " + p)
    print("cost_log: %d rows, %d native cases" % (len(rows), len(a1)))
    return 1 if problems else 0


def _results(d: str) -> int:
    problems = []
    text = _read(d, "RESULTS.md")
    lines = text.split("\n")
    if "EXPLORATORY" not in (lines[0] if lines else ""):
        problems.append("RESULTS.md's first line lacks EXPLORATORY")
    para = []
    for line in lines[1:]:
        if line.strip() == "" and para:
            break
        if line.strip() and not line.startswith("#"):
            para.append(line)
    if "Run 2" not in " ".join(para):
        problems.append("RESULTS.md's first paragraph does not name Run 2")
    pos = -1
    for k in range(1, 13):
        h = "### 14.%d" % k
        i = text.find(h + " ")
        if i < 0:
            i = text.find(h + "\n")
        if i < 0 or i < pos:
            problems.append("RESULTS.md lacks heading %s in order" % h)
        else:
            pos = i
    import results_write  # local import: results_write imports this module
    if results_write.can_render(d) and results_write.check(d) != 0:
        problems.append("RESULTS.md differs from its regeneration from the tables (run tools/results_write.py)")
    for p in problems:
        print("PROBLEM " + p)
    return 1 if problems else 0


SUBS = {"inventory": _inventory, "units": _units, "artifact1": _artifact1, "artifact2": _artifact2,
        "artifact3": _artifact3, "primary": _primary, "cost": _cost, "results": _results}


def run(sub: str, d: str) -> int:
    if sub not in SUBS:
        print("unknown check %r; known: %s" % (sub, sorted(SUBS)))
        return 2
    return SUBS[sub](d)


if __name__ == "__main__":
    sys.exit(run(sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else 2)
