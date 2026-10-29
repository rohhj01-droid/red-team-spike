"""Ledgers, vocabularies, the batch review document and the contract-conformance check
(contract Sections 9 and 11; Run 1's file schemas plus this run's columns)."""
from __future__ import annotations

import io
import os
import re

FRAME_FIELDS = ["frame_rank", "port_path", "upstream_resolution", "candidate_id", "duplicate_of", "terminal_status",
                "stop_gate", "failure_code", "protocol_issue_code", "evidence_refs", "starting_points_ref", "pin_ref"]
CANDIDATE_FIELDS = ["candidate_id", "first_frame_rank", "frame_items", "external_upstream_name", "E1", "E2_REP", "E2_RULE",
                    "E3", "E4", "overall", "stop_gate", "failure_code", "protocol_issue_code", "evidence_refs",
                    "canonical_source_location", "external_target_identifier", "primary_snapshot",
                    "authoritative_source_inventory_ref", "enumerator_inventory_ref", "completeness_class", "tie_key",
                    "decided_by_grammar", "class_sensitivity_ref"]
SP_FIELDS = ["frame_rank", "url", "source", "klass", "action", "final_url", "final_class", "observed_at_utc",
             "http_status", "evidence_role", "note"]
OBS_FIELDS = ["observed_at_utc", "frame_rank", "step", "requested_url", "final_url", "http_status", "redirect_chain",
              "attempt", "outcome", "body_ref"]
COST_FIELDS = ["batch", "frame_rank", "gate_reached", "session_s", "review_s", "conditions"]
WITNESS_FIELDS = ["frame_rank", "candidate_id", "gate", "kind", "surface", "location", "quote", "tag"]
CONDITIONS = "analyst=AI model; session=first read of the batch to the batch commit; review=commit to the owner's 통과"

GATES = ["UR", "E1", "E2-REP", "E2-RULE", "E3", "E4"]
GATE_COLS = {"E1": "E1", "E2-REP": "E2_REP", "E2-RULE": "E2_RULE", "E3": "E3", "E4": "E4"}
GATE_STATES = {"PASS", "FAIL", "UNRESOLVED", "NOT_REACHED"}
UR_VALUES = {"PASS", "FAIL_NONE", "FAIL_AMBIGUOUS", "DUPLICATE", "UNRESOLVED"}
TERMINAL = {"ELIGIBLE", "REJECTED", "DUPLICATE", "UNRESOLVED"}
FAILURE_CODES = {"NONE", "UR-NONE", "UR-AMBIGUOUS", "E1-NONEXTERNAL", "E2REP-NO-SOURCE", "E2REP-NO-SINGLE-CANONICAL-LOCATION",
                 "E2REP-NO-STABLE-URL", "E2REP-NO-SINGLE-TARGET-ID", "E2RULE-NO-VALIDITY-EVIDENCE",
                 "E3-NO-STATEFUL-TEMPORAL-VALIDITY", "E4-NO-MECHANICAL-PRIMARY-UNIVERSE"}
PI_CODES = {"NONE", "PI-TRANSPORT-INDETERMINATE", "PI-UNCLASSIFIED-SHAPE", "PI-STARTING-POINTS-CLOSED",
            "PI-UNCLASSIFIABLE-SURFACE", "PI-METADATA-UNRESOLVED"}
EVIDENCE_ROLES = {"official-project-page", "official-source-location", "admitted-starting-point", "distfile-location", ""}
SP_ACTIONS = {"observed", "closed-by-class", "unclassifiable", "unreachable", "not-reached"}
WITNESS_KINDS = {"designation", "identifier", "source-tree", "validity", "stateful", "enumerator", "refusal-path", "absence-survey"}
EV_RE = re.compile(r"EV-(C\d{3}|R\d{3})-(UR|E1|E2REP|E2RULE|E3|E4)-\d{2}")


def _cell(v) -> str:
    return str(v if v is not None else "").replace("\t", " ").replace("\r", " ").replace("\n", " ")


def read_rows(path: str, fields: list[str]) -> list[dict]:
    if not os.path.exists(path):
        return []
    lines = [l for l in io.open(path, encoding="utf-8").read().splitlines() if l and not l.startswith("#")]
    if not lines:
        return []
    header = lines[0].split("\t")
    out = []
    for l in lines[1:]:
        cells = l.split("\t")
        cells += [""] * (len(header) - len(cells))
        out.append(dict(zip(header, cells)))
    return out


def append_rows(path: str, rows: list[dict], fields: list[str]) -> None:
    new = not os.path.exists(path)
    with io.open(path, "a", encoding="utf-8", newline="\n") as f:
        if new:
            f.write("\t".join(fields) + "\n")
        for r in rows:
            f.write("\t".join(_cell(r.get(k, "")) for k in fields) + "\n")


def write_rows(path: str, rows: list[dict], fields: list[str]) -> None:
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(fields) + "\n")
        for r in rows:
            f.write("\t".join(_cell(r.get(k, "")) for k in fields) + "\n")


def write_witnesses(run2_dir: str, batch: int, rows: list[dict]) -> str:
    p = os.path.join(run2_dir, "witness_b%02d.tsv" % batch)
    write_rows(p, rows, WITNESS_FIELDS)
    return p


def read_witnesses(run2_dir: str, batch: int) -> list[dict]:
    return read_rows(os.path.join(run2_dir, "witness_b%02d.tsv" % batch), WITNESS_FIELDS)


def batch_document(batch_no: int, items: list[dict]) -> str:
    """The review document: the batch table, then per item the starting points, exposure lines and evidence blocks."""
    L = ["# Screening batch %02d -- Run 2" % batch_no, "",
         "Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen",
         "metadata, the recorded observations and the witness table `witness_b%02d.tsv`; the owner answers" % batch_no,
         "통과 or names the rank that fails review.", "",
         "| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for it in items:
        f, c = it["frame_row"], it["candidate_row"] or {}
        code = f["failure_code"] if f["failure_code"] != "NONE" else f["protocol_issue_code"]
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            f["frame_rank"], f["port_path"], f["upstream_resolution"], f["candidate_id"], c.get("E1", "-"),
            c.get("E2_REP", "-"), c.get("E2_RULE", "-"), c.get("E3", "-"), c.get("E4", "-"), f["terminal_status"],
            f["stop_gate"], code))
    for it in items:
        f = it["frame_row"]
        L += ["", "## rank %s -- %s" % (f["frame_rank"], f["port_path"]), ""]
        if it["starting_points"]:
            L += ["| url | source | class | action | final class | status | role |", "|---|---|---|---|---|---|---|"]
            for sp in it["starting_points"]:
                L.append("| %s | %s | %s | %s | %s | %s | %s |" % (sp["url"], sp["source"], sp["klass"] or "unmatched",
                                                                   sp["action"], sp.get("final_class") or "", sp.get("http_status") or "", sp.get("evidence_role") or ""))
            L.append("")
        for line in it["exposure"]:
            L.append(line)
        if it["exposure"]:
            L.append("")
        for block in it["evidence_blocks"]:
            L += [block, ""]
    return "\n".join(L)


def check(run2_dir: str, expect_rows: int = 128) -> int:
    """Invariants of contract Section 9 and Run 1's protocol over the ledgers in run2_dir; 0 when clean."""
    problems = []
    frame = read_rows(os.path.join(run2_dir, "screening_frame_items.tsv"), FRAME_FIELDS)
    cands = read_rows(os.path.join(run2_dir, "screening_candidates.tsv"), CANDIDATE_FIELDS)
    sps = read_rows(os.path.join(run2_dir, "starting_points.tsv"), SP_FIELDS)
    obs = read_rows(os.path.join(run2_dir, "observations.tsv"), OBS_FIELDS)
    ranks = [int(r["frame_rank"]) for r in frame]
    if ranks != list(range(1, len(ranks) + 1)):
        problems.append("frame ranks are not 1..n contiguous")
    if len(frame) > expect_rows:
        problems.append("more than %d frame rows" % expect_rows)
    keys_pass = sum(1 for r in frame if r["upstream_resolution"] == "PASS")
    if keys_pass != len(cands):
        problems.append("candidate rows %d != UR-PASS frame rows %d" % (len(cands), keys_pass))
    for r in frame:
        if r["upstream_resolution"] not in UR_VALUES or r["terminal_status"] not in TERMINAL:
            problems.append("rank %s: vocabulary (%s, %s)" % (r["frame_rank"], r["upstream_resolution"], r["terminal_status"]))
        if r["failure_code"] not in FAILURE_CODES or r["protocol_issue_code"] not in PI_CODES:
            problems.append("rank %s: code vocabulary" % r["frame_rank"])
        if r["failure_code"] != "NONE" and r["protocol_issue_code"] != "NONE":
            problems.append("rank %s: both failure_code and protocol_issue_code set" % r["frame_rank"])
    for c in cands:
        states = [c[GATE_COLS[g]] for g in ("E1", "E2-REP", "E2-RULE", "E3", "E4")]
        if any(s not in GATE_STATES for s in states):
            problems.append("%s: gate state vocabulary %s" % (c["candidate_id"], states))
        stopped = False
        for g, s in zip(("E1", "E2-REP", "E2-RULE", "E3", "E4"), states):
            if stopped and s != "NOT_REACHED":
                problems.append("%s: %s evaluated after the stop gate" % (c["candidate_id"], g))
            if s in ("FAIL", "UNRESOLVED"):
                stopped = True
        if c["overall"] in ("ELIGIBLE", "REJECTED") or any(s in ("PASS", "FAIL") for s in states):
            if not EV_RE.search(c["evidence_refs"]):
                problems.append("%s: a PASS/FAIL without an EV reference" % c["candidate_id"])
    for sp in sps:
        if sp["action"] not in SP_ACTIONS:
            problems.append("rank %s: starting point %s action %r" % (sp["frame_rank"], sp["url"], sp["action"]))
        if re.search(r"\$[{A-Za-z_]", sp["url"]):
            problems.append("rank %s: unexpanded macro in %s" % (sp["frame_rank"], sp["url"]))
        if sp["evidence_role"] not in EVIDENCE_ROLES:
            problems.append("rank %s: evidence_role %r" % (sp["frame_rank"], sp["evidence_role"]))
    for o in obs:
        if o["outcome"] not in ("ok", "definitive", "transport"):
            problems.append("observation %s: outcome %r" % (o["requested_url"], o["outcome"]))
    for name in sorted(os.listdir(run2_dir)):              # the witness tables: one well-formed row per line (RQA-09)
        if name.startswith("witness_b") and name.endswith(".tsv"):
            for w in read_rows(os.path.join(run2_dir, name), WITNESS_FIELDS):
                if not w["frame_rank"].isdigit() or w["gate"] not in GATES[2:] or w["kind"] not in WITNESS_KINDS:
                    problems.append("%s: malformed witness row (rank %r, gate %r, kind %r)" % (name, w["frame_rank"], w["gate"], w["kind"]))
    for p in problems:
        print("PROBLEM " + p)
    return 1 if problems else 0


def record_review(run2_dir: str, batch: int, review_s: int) -> int:
    """Fill review_s on the batch's cost rows at the owner's acceptance; returns the rows changed."""
    p = os.path.join(run2_dir, "screening_cost.tsv")
    rows = read_rows(p, COST_FIELDS)
    n = 0
    for r in rows:
        if r["batch"] == str(batch) and not r["review_s"]:
            r["review_s"] = str(review_s)
            n += 1
    write_rows(p, rows, COST_FIELDS)
    return n
