"""Per-item screening (contract Sections 2-8) and batch execution (Section 11).

screen_item() takes one frame item from its frozen metadata to its gate decisions: UR and E1
mechanically; E2-REP by classifying and observing the starting points, following step-2 links
by the label rule, verifying the analyst's quoted witnesses against the stored bodies, pinning the
designated repository at observation time; E2-RULE, E3 and E4 by verifying quoted witnesses
against the pinned tree (E4 through the frozen grammar). Everything it returns is written by
run_batch() into the ledgers and the batch review document. `fetch`, `clock` and `git` are
injectable so the tests never touch the network.
"""
from __future__ import annotations

import io
import json
import os
import re
import time

import paths

paths.use_exploratory_tools()
import en_verdicts  # noqa: E402
import ledger  # noqa: E402
import metadata  # noqa: E402
import net  # noqa: E402
import pin  # noqa: E402
import surfaces  # noqa: E402
import inventory  # noqa: E402  (exploratory tool)

OWN_NAMESPACE = "https://github.com/rohhj01-droid"
ARCHIVE_FMT = {"github.com": "{url}/archive/{sha}.tar.gz", "gitlab.com": "{url}/-/archive/{sha}/archive.tar.gz",
               "codeberg.org": "{url}/archive/{sha}.tar.gz"}
CITE_RE = re.compile(r"^([\w./-]+):(\d+)$")


def new_state(root: str) -> dict:
    """Run state: candidate ids and identity keys across items; where bodies and pinned trees go."""
    return dict(keys={}, next_id=1, root=root, bodies=os.path.join(root, "target", "bodies"),
                target=os.path.join(root, "target"), batch_start=None)


class Witness(ValueError):
    pass


# ---------------------------------------------------------------- observation bookkeeping

def _observe(ctx: dict, step: str, url: str) -> dict:
    rec = net.fetch(url, fetch=ctx["fetch"], clock=ctx["clock"])
    n = len(ctx["observations"]) + 1
    body_ref = ""
    if rec["body"]:
        d = os.path.join(ctx["state"]["bodies"], "%03d" % ctx["rank"])
        os.makedirs(d, exist_ok=True)
        body_ref = os.path.join(d, "%02d.bin" % n)
        with open(body_ref, "wb") as f:
            f.write(rec["body"])
        body_ref = os.path.relpath(body_ref, ctx["state"]["root"]).replace(os.sep, "/")
    for i, (t, outcome, requested, status) in enumerate(rec["attempts"], 1):   # one row per request made
        ctx["observations"].append(dict(observed_at_utc=t, frame_rank=ctx["rank"], step=step, requested_url=requested,
                                        final_url=rec["final_url"], http_status=status if status is not None else "",
                                        redirect_chain=" > ".join(rec["redirect_chain"]) or "NONE", attempt=i, outcome=outcome,
                                        body_ref=body_ref if i == len(rec["attempts"]) else ""))
    ctx["bodies"][url] = rec
    ctx["bodies"][rec["final_url"]] = rec
    return rec


def _class_by_response(rec: dict) -> str:
    ct = rec.get("content_type", "")
    if rec["outcome"] != "ok":
        return "unclassifiable"
    if ct in ("application/x-gzip", "application/gzip", "application/zip", "application/x-xz", "application/x-bzip2", "application/zstd") \
            or (ct == "application/octet-stream" and re.search(surfaces.ARCHIVE_EXT, rec["final_url"])):
        return "distfile-location"
    text = net.text_of(rec["body"])
    if ct.startswith("text/plain") or re.search(r"<title>\s*Index of", rec["body"].decode("utf-8", "replace"), re.I):
        return "distfile-location"
    if ct.startswith("text/html") or "<html" in rec["body"][:2000].decode("utf-8", "replace").lower():
        return "project-page" if text else "unclassifiable"
    return "unclassifiable"


def _text_at(ctx: dict, url: str) -> str:
    rec = ctx["bodies"].get(url)
    return net.text_of(rec["body"]) if rec and rec.get("body") else ""


def _ev_id(ctx: dict, gate: str) -> str:
    ctx["ev_n"] = ctx.get("ev_n", 0) + 1
    who = ctx["cid"] if ctx.get("cid") else "R%03d" % ctx["rank"]
    return "EV-%s-%s-%02d" % (who, gate.replace("-", ""), ctx["ev_n"])


def _block(ctx: dict, gate: str, source: str, observed: str, inference: str, decision: str, surfaces_lines: list[str] | None = None) -> str:
    ev = _ev_id(ctx, gate)
    ctx["evidence_refs"].append(ev)
    L = ["## " + ev, "", "Candidate: %s" % (ctx.get("cid") or "(none: rank %d)" % ctx["rank"]), "Gate: %s" % gate,
         "Source:   %s" % source, ""]
    if surfaces_lines:
        L += ["Surfaces:  " + surfaces_lines[0]] + ["           " + s for s in surfaces_lines[1:]]
        L += ["Necessary because: the gate's question needs every admitted starting point accounted for", "  (contract Section 7); each line above is its accounting.", ""]
    L += ["Observed: %s" % observed, "", "Inference: %s" % inference, "", "Decision: %s" % decision]
    return "\n".join(L)


# ---------------------------------------------------------------- witnesses

def _witnesses(ctx: dict, gate: str, kind: str) -> list[dict]:
    return [w for w in ctx["witnesses"] if str(w.get("frame_rank")) == str(ctx["rank"]) and w.get("gate") == gate and w.get("kind") == kind]


def _verify_page_quote(ctx: dict, w: dict) -> None:
    text = _text_at(ctx, w["surface"])
    if not text:
        raise Witness("rank %s: witness surface %s was not observed" % (ctx["rank"], w["surface"]))
    if w["quote"] not in text:
        raise Witness("rank %s: quote %r not found on %s" % (ctx["rank"], w["quote"], w["surface"]))


def _verify_tree_quote(ctx: dict, w: dict) -> None:
    m = CITE_RE.match(w.get("location", ""))
    if not m:
        raise Witness("rank %s: location %r is not file:line" % (ctx["rank"], w.get("location")))
    p = os.path.join(ctx["tree"], m.group(1))
    if not os.path.exists(p):
        raise Witness("rank %s: %s not in the pinned tree" % (ctx["rank"], m.group(1)))
    lines = open(p, "rb").read().decode("utf-8", "replace").split("\n")
    ln = int(m.group(2))
    window = "\n".join(lines[max(0, ln - 3):ln + 2])
    if w["quote"] not in window:
        raise Witness("rank %s: quote %r not at %s" % (ctx["rank"], w["quote"], w["location"]))


# ---------------------------------------------------------------- gates

def _ur(ctx: dict, meta: dict) -> tuple[str, str]:
    classes = {}
    for sp in ctx["sps"]:
        if sp["klass"] is None and sp["source"].startswith("SITES"):
            rec = _observe(ctx, "UR-classify", sp["url"])
            classes[sp["url"]] = _class_by_response(rec)
            sp["pre_classified"] = classes[sp["url"]]
    ur, key = surfaces.identity_key(meta, classes)
    return ur, key


def _e2rep(ctx: dict) -> dict:
    """Returns dict(state, failure_code, pi_code, canonical, identifier, snapshot, block)."""
    sps = ctx["sps"]
    observed_roots: list[str] = []
    for sp in sps:
        klass = sp["klass"] or sp.get("pre_classified")
        sp.update(action="", final_url="", final_class="", observed_at_utc="", http_status="", evidence_role="", note="")
        if klass == "release-assets":
            sp.update(action="closed-by-class", final_class=klass, note="forbidden class, never requested")
            continue
        rec = ctx["bodies"].get(sp["url"]) or _observe(ctx, "E2REP-1" if klass != "repository-root" else "E2REP-3", sp["url"])
        sp.update(final_url=rec["final_url"], observed_at_utc=rec["observed_at_utc"], http_status=rec["http_status"] or "")
        if rec["outcome"] == "transport":
            sp.update(action="unreachable", note="PI-TRANSPORT-INDETERMINATE after two retries")
            continue
        final_class = surfaces.classify(rec["final_url"]) or (klass if klass and klass != "project-page" else None) or _class_by_response(rec)
        sp["final_class"] = final_class
        if final_class == "release-assets":
            sp.update(action="closed-by-class", note="final URL is the forbidden class; revealed by the one request")
            continue
        if final_class == "unclassifiable":
            sp.update(action="unclassifiable")
            continue
        sp["action"] = "observed"
        sp["evidence_role"] = {"repository-root": "official-source-location", "project-page": "official-project-page",
                               "distfile-location": "distfile-location"}.get(final_class, "admitted-starting-point")
        if final_class == "repository-root" and rec["outcome"] == "ok":
            observed_roots.append(surfaces.normalize_url(rec["final_url"]))
        if final_class == "project-page" and rec["outcome"] == "ok":
            for link in net.step2_links(net.links(rec["body"], rec["final_url"])):
                lk = surfaces.classify(link["href"])
                if lk == "release-assets":
                    ctx["exposure"].append("| %s | %d | %s | step-2 link to a forbidden class, not followed | used: no |" % (rec["observed_at_utc"], ctx["rank"], link["href"]))
                    continue
                if surfaces.normalize_url(link["href"]) in [surfaces.normalize_url(s["url"]) for s in sps] or link["href"] in ctx["bodies"]:
                    continue
                r2 = _observe(ctx, "E2REP-2", link["href"])
                fc = surfaces.classify(r2["final_url"]) or _class_by_response(r2)
                ctx["step2"].append(dict(url=link["href"], label=link["label"], final_url=r2["final_url"], final_class=fc, outcome=r2["outcome"]))
                if fc == "repository-root" and r2["outcome"] == "ok":
                    observed_roots.append(surfaces.normalize_url(r2["final_url"]))
        if final_class == "repository-root" and rec["outcome"] == "ok":
            t = net.text_of(rec["body"])
            if "readme" in rec["body"][:200000].decode("utf-8", "replace").lower():
                ctx["exposure"].append("| %s | %d | %s | landing page rendered a README (%d chars of page text); not used | used: no |" % (rec["observed_at_utc"], ctx["rank"], rec["final_url"], len(t)))
    accounting = ["%s -> %s%s" % (sp["url"], sp["action"], (" (%s)" % sp["note"]) if sp["note"] else "") for sp in sps]
    # the analyst's designation witnesses
    designations = _witnesses(ctx, "E2-REP", "designation")
    for w in designations:
        _verify_page_quote(ctx, w)
    targets = {surfaces.normalize_url(w["location"]) for w in designations}
    if len(targets) > 1:
        mirror = any("mirror" in w["quote"].lower() for w in designations)
        if not mirror:
            return dict(state="FAIL", failure_code="E2REP-NO-SINGLE-CANONICAL-LOCATION", pi_code="NONE", canonical="", identifier="", snapshot="",
                        block=_block(ctx, "E2-REP", "; ".join(sorted({w["surface"] for w in designations})),
                                     " | ".join("%r at %s -> %s" % (w["quote"], w["surface"], w["location"]) for w in designations),
                                     "two designations name different locations and neither marks a mirror (contract Section 7)",
                                     "FAIL", accounting))
    if not targets:
        if all(sp["action"] == "closed-by-class" for sp in sps):
            pi = "PI-STARTING-POINTS-CLOSED"
        elif any(sp["action"] == "unclassifiable" for sp in sps):
            pi = "PI-UNCLASSIFIABLE-SURFACE"
        elif any(sp["action"] == "unreachable" for sp in sps):
            pi = "PI-TRANSPORT-INDETERMINATE"
        else:
            pi = "PI-UNCLASSIFIED-SHAPE"
        return dict(state="UNRESOLVED", failure_code="NONE", pi_code=pi, canonical="", identifier="", snapshot="",
                    block=_block(ctx, "E2-REP", "the starting-point set (contract Section 4)",
                                 "no designation witness on any observed surface; observed roots: %s" % (", ".join(observed_roots) or "none"),
                                 "the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> %s" % pi,
                                 "UNRESOLVED", accounting))
    canonical = targets.pop()
    rec = ctx["bodies"].get(canonical) or next((r for u, r in ctx["bodies"].items() if surfaces.normalize_url(u) == canonical), None)
    if rec is None:
        rec = _observe(ctx, "E2REP-3", canonical)
    if rec["outcome"] == "definitive" and rec["http_status"] in (404, 410):
        return dict(state="FAIL", failure_code="E2REP-NO-STABLE-URL", pi_code="NONE", canonical=canonical, identifier="", snapshot="",
                    block=_block(ctx, "E2-REP", canonical, "HTTP %s at the designated location" % rec["http_status"],
                                 "the designated canonical location has no stable URL (definitive absence, contract Section 7)", "FAIL", accounting))
    if rec["outcome"] != "ok":
        return dict(state="UNRESOLVED", failure_code="NONE", pi_code="PI-TRANSPORT-INDETERMINATE", canonical=canonical, identifier="", snapshot="",
                    block=_block(ctx, "E2-REP", canonical, "transport indeterminacy at the designated location", "retries exhausted (contract Section 7)", "UNRESOLVED", accounting))
    # identifier
    ids = _witnesses(ctx, "E2-REP", "identifier")
    for w in ids:
        _verify_page_quote(ctx, w)
    identifier = ids[0]["quote"] if ids else canonical.rstrip("/").split("/")[-1]
    # pin at observation time (contract Section 10): the source tree is established by the fetch
    host = canonical.split("/")[2]
    recpin = pin.pin_repository(ctx["cid"], canonical, ctx["state"]["target"], ARCHIVE_FMT.get(host), git=ctx["git"], fetch=ctx["fetch"], clock=ctx["clock"])
    ctx["tree"] = os.path.join(ctx["state"]["target"], ctx["cid"], "tree")
    if recpin.get("tracked_files", 0) == 0 and not recpin.get("digests"):
        return dict(state="FAIL", failure_code="E2REP-NO-SOURCE", pi_code="NONE", canonical=canonical, identifier=identifier, snapshot=recpin["sha"],
                    block=_block(ctx, "E2-REP", canonical, "the fetched tree at %s holds no files" % recpin["sha"], "no source tree at the designated location (contract Section 7)", "FAIL", accounting))
    observed = " | ".join("%r at %s" % (w["quote"], w["surface"]) for w in designations + ids)
    return dict(state="PASS", failure_code="NONE", pi_code="NONE", canonical=canonical, identifier=identifier, snapshot=recpin["sha"],
                block=_block(ctx, "E2-REP", canonical, observed + " | tree pinned at %s (%s tracked files)" % (recpin["sha"], recpin.get("tracked_files")),
                             "exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6)",
                             "PASS", accounting))


def _witness_gate(ctx: dict, gate: str, kind: str, surfaces_read: list[str]) -> tuple[str, str]:
    """E2-RULE / E3: PASS on one verified quoted witness; else UNRESOLVED with the surfaces read listed."""
    ws = _witnesses(ctx, gate, kind)
    for w in ws:
        _verify_tree_quote(ctx, w)
    survey = [w["surface"] for w in _witnesses(ctx, gate, "absence-survey")]
    if ws:
        w = ws[0]
        return "PASS", _block(ctx, gate, w["location"], "%r" % w["quote"], "a quoted, located %s witness (contract Section 8)" % kind, "PASS")
    return "UNRESOLVED", _block(ctx, gate, "the contract's %s surfaces" % gate, "no %s witness quoted; surfaces read: %s" % (kind, ", ".join(survey) or "none listed"),
                                "positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)", "UNRESOLVED",
                                surfaces_read or ["(none)"])


def _e4(ctx: dict) -> tuple[str, str, list[dict]]:
    rows = [en_verdicts.decide(r, tree=ctx["tree"]) for r in inventory.enumerators(ctx["tree"])]
    ws = _witnesses(ctx, "E4", "enumerator")
    quoted = []
    for w in ws:
        _verify_tree_quote(ctx, w)
        rp = [r for r in _witnesses(ctx, "E4", "refusal-path") if r["surface"] == w["surface"]]
        for r in rp:
            _verify_tree_quote(ctx, r)
        cand = w["surface"].split(":", 1)[-1] if w["surface"].startswith("EN:") else w["surface"]
        ev = "EN2: %s %r" % (w["location"], w["quote"]) + "".join("; EN4: %s %r" % (r["location"], r["quote"]) for r in rp)
        quoted.append(dict(cand_id=cand, verdict="ADMIT", tag=w.get("tag") or "", evidence=ev))
    rows = en_verdicts.apply_quoted(rows, quoted) if quoted else rows
    admitted = [r for r in rows if en_verdicts.is_admitted(r)]
    if admitted:
        a = admitted[0]
        return "PASS", _block(ctx, "E4", "%s:%s %s" % (a["file"], a["line"], a["symbol"]), a["evidence"],
                              "one enumerator admitted under the frozen grammar with a quoted identification and refusal path (contract Section 8)", "PASS"), rows
    return "UNRESOLVED", _block(ctx, "E4", "the frozen grammar over %d candidate rows" % len(rows),
                                "catalogue decided %d rows, %d undecided, none admitted" % (sum(1 for r in rows if r["decided_by"].startswith("catalogue")), sum(1 for r in rows if r["decided_by"] == "UNDECIDED")),
                                "no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)", "UNRESOLVED"), rows


# ---------------------------------------------------------------- the item

def screen_item(rank: int, port_path: str, ports_root: str, witnesses: list[dict], state: dict,
                fetch=None, clock=None, git=None) -> dict:
    ctx = dict(rank=rank, state=state, fetch=fetch, clock=clock or net.utc_now, git=git, witnesses=witnesses,
               observations=[], bodies={}, exposure=[], step2=[], evidence_refs=[], cid="", tree="")
    meta = metadata.resolve(os.path.join(ports_root, port_path), os.path.join(ports_root, "infrastructure"))
    frame = dict(frame_rank=rank, port_path=port_path, upstream_resolution="", candidate_id="NONE", duplicate_of="NONE",
                 terminal_status="", stop_gate="NONE", failure_code="NONE", protocol_issue_code="NONE", evidence_refs="",
                 starting_points_ref="", pin_ref="NONE")
    result = dict(frame_row=frame, candidate_row=None, starting_points=[], observations=ctx["observations"],
                  evidence_blocks=[], exposure=ctx["exposure"], cost_row=None, e4_rows=[], meta=meta)
    gate_reached = "UR"
    if meta["issue"]:
        frame.update(upstream_resolution="UNRESOLVED", terminal_status="UNRESOLVED", stop_gate="UR", protocol_issue_code=meta["issue"])
        result["evidence_blocks"].append(_block(ctx, "UR", "%s/Makefile" % port_path,
                                                "modules=%s unresolved=%s" % (meta["modules"], meta["unresolved"]),
                                                "the resolver cannot resolve the frozen metadata (contract Section 2)", "UNRESOLVED"))
    else:
        ctx["sps"] = surfaces.starting_points(meta)
        result["starting_points"] = ctx["sps"]
        for sp in ctx["sps"]:
            sp.update(frame_rank=rank, action="not-reached", final_url="", final_class="", observed_at_utc="", http_status="", evidence_role="", note="")
        ur, key = _ur(ctx, meta)
        if ur == "PASS" and key in state["keys"]:
            ur = "DUPLICATE"
        frame["upstream_resolution"] = ur
        if ur == "DUPLICATE":
            frame.update(duplicate_of=state["keys"][key], terminal_status="DUPLICATE", stop_gate="UR")
            result["evidence_blocks"].append(_block(ctx, "UR", "%s/Makefile" % port_path, "identity key %s" % key,
                                                    "the same upstream as %s (contract Section 3)" % state["keys"][key], "DUPLICATE"))
        elif ur != "PASS":
            frame.update(terminal_status="REJECTED", stop_gate="UR", failure_code="UR-NONE" if ur == "FAIL_NONE" else "UR-AMBIGUOUS")
            result["evidence_blocks"].append(_block(ctx, "UR", "%s/Makefile" % port_path, "homepage=%s sites=%s gh=%s tuples=%s" % (meta["homepage"], meta["sites"], meta["gh"], meta["dist_tuples"]),
                                                    "identity key rule (contract Section 3): %s" % ur, "FAIL"))
        else:
            cid = "C%03d" % state["next_id"]
            state["next_id"] += 1
            state["keys"][key] = cid
            ctx["cid"] = cid
            frame.update(candidate_id=cid)
            cand = dict(candidate_id=cid, first_frame_rank=rank, frame_items=str(rank),
                        external_upstream_name=meta.get("distname") or port_path.split("/")[-1],
                        E1="NOT_REACHED", E2_REP="NOT_REACHED", E2_RULE="NOT_REACHED", E3="NOT_REACHED", E4="NOT_REACHED",
                        overall="", stop_gate="NONE", failure_code="NONE", protocol_issue_code="NONE", evidence_refs="",
                        canonical_source_location="NOT_REACHED", external_target_identifier="NOT_REACHED", primary_snapshot="NOT_REACHED",
                        authoritative_source_inventory_ref="NOT_REACHED", enumerator_inventory_ref="NOT_REACHED",
                        completeness_class="NOT_REACHED", tie_key="NOT_REACHED", decided_by_grammar="", class_sensitivity_ref="NOT_REACHED")
            result["candidate_row"] = cand
            # E1
            gate_reached = "E1"
            if key.startswith(OWN_NAMESPACE):
                cand.update(E1="FAIL", overall="REJECTED", stop_gate="E1", failure_code="E1-NONEXTERNAL")
                result["evidence_blocks"].append(_block(ctx, "E1", key, "the identity key lies in this project's own namespace", "E1 external authorship (contract Section 3)", "FAIL"))
            else:
                cand["E1"] = "PASS"
                result["evidence_blocks"].append(_block(ctx, "E1", key, "identity key outside this project's namespace", "E1 external authorship (contract Section 3)", "PASS"))
                gate_reached = "E2-REP"
                e2 = _e2rep(ctx)
                result["evidence_blocks"].append(e2["block"])
                cand.update(E2_REP=e2["state"], failure_code=e2["failure_code"], protocol_issue_code=e2["pi_code"])
                if e2["canonical"]:
                    cand.update(canonical_source_location=e2["canonical"], external_target_identifier=e2["identifier"] or "NOT_REACHED",
                                primary_snapshot=e2["snapshot"] or "NOT_REACHED")
                if e2["state"] == "PASS":
                    cand.update(tie_key="(%s, %s)" % (e2["canonical"], e2["identifier"]))
                    frame["pin_ref"] = "inventory/%s/pin.json" % cid
                    for gate, kind, col in (("E2-RULE", "validity", "E2_RULE"), ("E3", "stateful", "E3")):
                        gate_reached = gate
                        st, blk = _witness_gate(ctx, gate, kind, [w["surface"] for w in _witnesses(ctx, gate, "absence-survey")])
                        result["evidence_blocks"].append(blk)
                        cand[col] = st
                        if st != "PASS":
                            cand.update(overall="UNRESOLVED", stop_gate=gate)
                            break
                    else:
                        gate_reached = "E4"
                        st, blk, rows = _e4(ctx)
                        result["evidence_blocks"].append(blk)
                        result["e4_rows"] = rows
                        cand["E4"] = st
                        if st == "PASS":
                            cand.update(overall="ELIGIBLE", completeness_class="PENDING_INVENTORY",
                                        authoritative_source_inventory_ref="PENDING_INVENTORY", enumerator_inventory_ref="PENDING_INVENTORY",
                                        class_sensitivity_ref="PENDING_INVENTORY")
                        else:
                            cand.update(overall="UNRESOLVED", stop_gate="E4")
                elif e2["state"] == "FAIL":
                    cand.update(overall="REJECTED", stop_gate="E2-REP")
                else:
                    cand.update(overall="UNRESOLVED", stop_gate="E2-REP")
            cand["evidence_refs"] = ";".join(ctx["evidence_refs"])
            frame.update(terminal_status=cand["overall"], stop_gate=cand["stop_gate"], failure_code=cand["failure_code"],
                         protocol_issue_code=cand["protocol_issue_code"])
    frame["evidence_refs"] = ";".join(ctx["evidence_refs"])
    frame["starting_points_ref"] = "starting_points.tsv#rank=%d" % rank if result["starting_points"] else "NONE"
    result["cost_row"] = dict(batch="", frame_rank=rank, gate_reached=gate_reached, session_s="", review_s="", conditions=ledger.CONDITIONS)
    return result


# ---------------------------------------------------------------- the batch

def run_batch(k: int, run2_dir: str, ports_root: str, fetch=None, clock=None, git=None, state: dict | None = None) -> str:
    items = [l.strip() for l in io.open(os.path.join(run2_dir, "screening_set_128.txt"), encoding="utf-8").read().splitlines() if l.strip()]
    state = state or load_state(run2_dir)
    if not state.get("batch_start"):
        state["batch_start"] = time.time()
    witnesses = ledger.read_witnesses(run2_dir, k)
    ranks = list(range(8 * k - 7, min(8 * k, len(items)) + 1))
    results = []
    for rank in ranks:
        results.append(screen_item(rank, items[rank - 1], ports_root, witnesses, state, fetch=fetch, clock=clock, git=git))
    session_s = int(time.time() - state["batch_start"])
    frame_rows = [r["frame_row"] for r in results]
    cand_rows = [r["candidate_row"] for r in results if r["candidate_row"]]
    sp_rows = [sp for r in results for sp in r["starting_points"]]
    obs_rows = [o for r in results for o in r["observations"]]
    cost_rows = []
    for r in results:
        c = dict(r["cost_row"]); c["batch"] = k; c["session_s"] = session_s
        cost_rows.append(c)
    ledger.append_rows(os.path.join(run2_dir, "screening_frame_items.tsv"), frame_rows, ledger.FRAME_FIELDS)
    if cand_rows:
        ledger.append_rows(os.path.join(run2_dir, "screening_candidates.tsv"), cand_rows, ledger.CANDIDATE_FIELDS)
    if sp_rows:
        ledger.append_rows(os.path.join(run2_dir, "starting_points.tsv"), sp_rows, ledger.SP_FIELDS)
    if obs_rows:
        ledger.append_rows(os.path.join(run2_dir, "observations.tsv"), obs_rows, ledger.OBS_FIELDS)
    ledger.append_rows(os.path.join(run2_dir, "screening_cost.tsv"), cost_rows, ledger.COST_FIELDS)
    with io.open(os.path.join(run2_dir, "exposure_log.md"), "a", encoding="utf-8", newline="\n") as f:
        for r in results:
            for line in r["exposure"]:
                f.write(line + "\n")
    for r in results:
        if r["e4_rows"] and r["candidate_row"]:
            d = os.path.join(run2_dir, "inventory", r["candidate_row"]["candidate_id"])
            os.makedirs(d, exist_ok=True)
            ledger.write_rows(os.path.join(d, "e4_candidates.tsv"), r["e4_rows"], inventory.EN_FIELDS + ["decided_by"])
    doc = ledger.batch_document(k, results)
    p = os.path.join(run2_dir, "screening_evidence_b%02d.md" % k)
    io.open(p, "w", encoding="utf-8", newline="\n").write(doc)
    state["batch_start"] = None
    save_state(run2_dir, state)
    return p


def load_state(run2_dir: str) -> dict:
    p = os.path.join(run2_dir, "target", "state.json")
    st = new_state(run2_dir)
    if os.path.exists(p):
        st.update(json.load(io.open(p, encoding="utf-8")))
    return st


def save_state(run2_dir: str, state: dict) -> None:
    os.makedirs(os.path.join(run2_dir, "target"), exist_ok=True)
    io.open(os.path.join(run2_dir, "target", "state.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({k: v for k, v in state.items() if k in ("keys", "next_id", "batch_start")}, indent=1))


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "batch":
        print("written", run_batch(int(argv[1]), paths.RUN2, argv[2]))
        return 0
    if len(argv) == 2 and argv[0] == "start":
        st = load_state(paths.RUN2); st["batch_start"] = time.time(); save_state(paths.RUN2, st)
        print("batch session started"); return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
