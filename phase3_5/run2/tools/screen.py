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
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:                      # `python -I` leaves the script's own directory off sys.path
    sys.path.insert(0, HERE)
import paths  # noqa: E402

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

def _cache_path(ctx: dict, url: str) -> str:
    import hashlib
    d = os.path.join(ctx["state"]["target"], "cache", "%03d" % ctx["rank"])
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, hashlib.sha1(url.encode("utf-8")).hexdigest())


def _observe(ctx: dict, step: str, url: str) -> dict:
    """Fetch once per (rank, url): a cached observation (target/cache) is reused on every later run of the
    same item, so the final run of a batch makes no request the preview run did not make."""
    cp = _cache_path(ctx, url)
    if os.path.exists(cp + ".json"):
        rec = json.load(io.open(cp + ".json", encoding="utf-8"))
        rec["attempts"] = [tuple(a) for a in rec["attempts"]]
        rec["body"] = open(cp + ".bin", "rb").read() if os.path.exists(cp + ".bin") else b""
    else:
        rec = net.fetch(url, fetch=ctx["fetch"], clock=ctx["clock"])
        meta = {k: v for k, v in rec.items() if k != "body"}
        io.open(cp + ".json", "w", encoding="utf-8", newline="\n").write(json.dumps(meta, indent=1))
        if rec["body"]:
            with open(cp + ".bin", "wb") as f:
                f.write(rec["body"])
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


def _class_by_response(rec: dict, source: str = "") -> str:
    """Class of an unmatched URL from its one response (contract Section 5); a definitive error answer is an
    observation of the surface the field named (RQA-02 b): distfile-location for a SITES URL, else project-page."""
    ct = rec.get("content_type", "")
    if rec["outcome"] == "definitive":
        return "distfile-location" if source.startswith("SITES") else "project-page"
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
            classes[sp["url"]] = _class_by_response(rec, sp["source"])
            sp["pre_classified"] = classes[sp["url"]]
    ur, key = surfaces.identity_key(meta, classes)
    return ur, key


def _e2rep(ctx: dict) -> dict:
    """Returns dict(state, failure_code, pi_code, canonical, identifier, snapshot, block)."""
    sps = ctx["sps"]
    observed_roots: list[str] = []
    label_designations: list[dict] = []          # RQA-02 (e)(f): a label-authorized step-2 link into a repository
    rank = ctx["rank"]

    def observe_root(root: str, step: str = "E2REP-3") -> dict:
        rec = ctx["bodies"].get(root) or _observe(ctx, step, root)
        if rec["outcome"] == "ok" and (surfaces.classify(rec["final_url"]) == "repository-root"):
            n = surfaces.normalize_url(rec["final_url"])
            if n not in observed_roots:
                observed_roots.append(n)
            if "readme" in rec["body"][:200000].decode("utf-8", "replace").lower():
                ctx["exposure"].append("| %s | %d | %s | landing page rendered a README (%d chars of page text); not used | used: no |" % (rec["observed_at_utc"], rank, rec["final_url"], len(net.text_of(rec["body"]))))
        return rec

    for sp in sps:
        klass = sp["klass"] or sp.get("pre_classified")
        sp.update(action="", final_url="", final_class="", observed_at_utc="", http_status="", evidence_role="", note="")
        if klass in surfaces.FORBIDDEN:
            sp.update(action="closed-by-class", final_class=klass, note="forbidden class, never requested")
            continue
        rec = ctx["bodies"].get(sp["url"]) or _observe(ctx, "E2REP-1" if klass != "repository-root" else "E2REP-3", sp["url"])
        sp.update(final_url=rec["final_url"], observed_at_utc=rec["observed_at_utc"], http_status=rec["http_status"] or "")
        if rec["outcome"] == "transport":
            sp.update(action="unreachable", note="PI-TRANSPORT-INDETERMINATE after two retries")
            continue
        table_class = surfaces.classify(rec["final_url"]) or (klass if klass and klass != "project-page" else None)
        if rec["outcome"] == "definitive":        # RQA-02 (b): a definitive error answer is an observation of that surface
            final_class = table_class or ("distfile-location" if sp["source"].startswith("SITES") else "project-page")
            sp.update(final_class=final_class, note="HTTP %s" % rec["http_status"])
            if final_class in surfaces.FORBIDDEN:
                sp.update(action="closed-by-class", note="final URL is a forbidden class; revealed by the one request")
            else:
                sp["action"] = "observed"
                sp["evidence_role"] = {"repository-root": "official-source-location", "project-page": "official-project-page",
                                       "distfile-location": "distfile-location"}.get(final_class, "admitted-starting-point")
            continue
        final_class = table_class or _class_by_response(rec)
        sp["final_class"] = final_class
        if final_class in surfaces.FORBIDDEN:
            sp.update(action="closed-by-class", note="final URL is a forbidden class; revealed by the one request")
            continue
        if final_class == "unclassifiable":
            sp.update(action="unclassifiable")
            continue
        sp["action"] = "observed"
        sp["evidence_role"] = {"repository-root": "official-source-location", "project-page": "official-project-page",
                               "distfile-location": "distfile-location"}.get(final_class, "admitted-starting-point")
        if final_class == "repository-root":
            observe_root(sp["url"])
        if final_class == "project-page":
            for link in net.step2_links(net.links(rec["body"], rec["final_url"])):
                lk = surfaces.classify(link["href"])
                label = link["label"] or link.get("title") or link.get("aria_label") or ""
                if lk in surfaces.FORBIDDEN:
                    ctx["exposure"].append("| %s | %d | %s | step-2 link %r leads to a forbidden class; not followed | used: no |" % (rec["observed_at_utc"], rank, link["href"], label))
                    continue
                root = surfaces.repository_root_of(link["href"]) if lk in ("repository-root", "repository-file") else None
                if root is None:
                    if surfaces.normalize_url(link["href"]) in [surfaces.normalize_url(s["url"]) for s in sps]:
                        continue
                    r2 = _observe(ctx, "E2REP-2", link["href"])              # one request, to learn its class
                    fc = surfaces.classify(r2["final_url"]) or _class_by_response(r2)
                    root = surfaces.repository_root_of(r2["final_url"]) if fc in ("repository-root", "repository-file") else None
                    if root is None:
                        ctx["exposure"].append("| %s | %d | %s | step-2 link %r: target is not a repository root (%s); observed once, not read | used: no |" % (r2["observed_at_utc"], rank, link["href"], label, fc))
                        ctx["step2"].append(dict(url=link["href"], label=label, final_url=r2["final_url"], final_class=fc, outcome=r2["outcome"]))
                        continue
                if lk == "repository-file" or surfaces.normalize_url(link["href"]) != surfaces.normalize_url(root):
                    ctx["exposure"].append("| %s | %d | %s | step-2 link %r points at a file inside %s; the file is not opened, the root is | used: no |" % (rec["observed_at_utc"], rank, link["href"], label, root))
                r3 = observe_root(root)
                ctx["step2"].append(dict(url=link["href"], label=label, final_url=r3["final_url"], final_class="repository-root", outcome=r3["outcome"]))
                if r3["outcome"] == "ok":
                    label_designations.append(dict(quote=label, surface=rec["final_url"], location=root, kind="label"))
    accounting = ["%s -> %s%s" % (sp["url"], sp["action"], (" (%s)" % sp["note"]) if sp["note"] else "") for sp in sps]
    # designations: the analyst's quoted witnesses, and the project page's own labelled pointers (RQA-02 e)
    designations = [dict(w, kind="witness") for w in _witnesses(ctx, "E2-REP", "designation")]
    for w in designations:
        _verify_page_quote(ctx, w)
    designations += label_designations
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
    # pin at observation time (contract Section 10): the source tree is established by the fetch;
    # a pin already taken for this candidate (the preview run) is reused, never re-taken
    host = canonical.split("/")[2]
    pin_json = os.path.join(ctx["state"]["target"], ctx["cid"], "pin.json")
    if os.path.exists(pin_json):
        recpin = json.load(io.open(pin_json, encoding="utf-8"))
    else:
        try:
            recpin = pin.pin_repository(ctx["cid"], surfaces.git_url_of(canonical), ctx["state"]["target"], ARCHIVE_FMT.get(host),
                                        git=ctx["git"], fetch=ctx["fetch"], clock=ctx["clock"])
        except Exception as ex:                   # RQA-03 (j): a designated repository the tools cannot fetch
            return dict(state="UNRESOLVED", failure_code="NONE", pi_code="PI-UNCLASSIFIED-SHAPE", canonical=canonical, identifier=identifier, snapshot="",
                        block=_block(ctx, "E2-REP", canonical, "designated and observed, but the pin could not be taken: %s" % str(ex).splitlines()[0][:160],
                                     "a designated repository that git cannot fetch is a shape no sealed criterion describes (contract Section 7)", "UNRESOLVED", accounting))
    ctx["tree"] = os.path.join(ctx["state"]["target"], ctx["cid"], "tree")
    if recpin.get("tracked_files", 0) == 0 and not recpin.get("digests"):
        return dict(state="FAIL", failure_code="E2REP-NO-SOURCE", pi_code="NONE", canonical=canonical, identifier=identifier, snapshot=recpin["sha"],
                    block=_block(ctx, "E2-REP", canonical, "the fetched tree at %s holds no files" % recpin["sha"], "no source tree at the designated location (contract Section 7)", "FAIL", accounting))
    observed = " | ".join("%s %r at %s -> %s" % ("link label" if w.get("kind") == "label" else "designation", w["quote"], w["surface"], w["location"]) for w in designations)
    observed += "".join(" | identifier %r at %s" % (w["quote"], w["surface"]) for w in ids)
    return dict(state="PASS", failure_code="NONE", pi_code="NONE", canonical=canonical, identifier=identifier, snapshot=recpin["sha"],
                block=_block(ctx, "E2-REP", canonical, observed + " | tree pinned at %s (%s tracked files)" % (recpin["sha"], recpin.get("tracked_files")),
                             "exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)",
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
    survey = _witnesses(ctx, "E4", "absence-survey")
    for w in survey:
        _verify_tree_quote(ctx, w)
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
                                "no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)", "UNRESOLVED",
                                [w["surface"] for w in survey] or ["(none)"]), rows


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

def _replace_rows(path: str, fields: list[str], rank_field: str, ranks: list[int], new_rows: list[dict]) -> None:
    """Rewrite a ledger with this batch's rows replacing any earlier rows of the same ranks (idempotent runs)."""
    keep = [r for r in ledger.read_rows(path, fields) if int(r[rank_field]) not in ranks] if os.path.exists(path) else []
    if keep or new_rows:
        ledger.write_rows(path, keep + new_rows, fields)


def run_batch(k: int, run2_dir: str, ports_root: str, fetch=None, clock=None, git=None, state: dict | None = None, commit: bool = True):
    """Screen batch k (ranks 8k-7..8k). commit=False is the preview: observations are made and cached, nothing is
    written to the ledgers and no state is saved -- the analyst then writes witness_bNN.tsv from the cached
    bodies. commit=True starts from the state as it stood before batch k, reuses every cached observation,
    replaces the batch's own rows in every ledger, writes the review document and saves the state after k."""
    items = [l.strip() for l in io.open(os.path.join(run2_dir, "screening_set_128.txt"), encoding="utf-8").read().splitlines() if l.strip()]
    state = state or load_state(run2_dir, before_batch=k)
    start_file = os.path.join(run2_dir, "target", "batch_b%02d_start" % k)       # the session clock: first read of the batch
    if os.path.exists(start_file):
        started = float(io.open(start_file, encoding="utf-8").read().strip() or time.time())
    else:
        started = time.time()
        os.makedirs(os.path.dirname(start_file), exist_ok=True)
        io.open(start_file, "w", encoding="utf-8", newline="\n").write("%f\n" % started)
    witnesses = ledger.read_witnesses(run2_dir, k)
    ranks = list(range(8 * k - 7, min(8 * k, len(items)) + 1))
    results = []
    for rank in ranks:
        results.append(screen_item(rank, items[rank - 1], ports_root, witnesses, state, fetch=fetch, clock=clock, git=git))
    if not commit:
        return results
    session_s = int(time.time() - started)
    frame_rows = [r["frame_row"] for r in results]
    cand_rows = [r["candidate_row"] for r in results if r["candidate_row"]]
    sp_rows = [sp for r in results for sp in r["starting_points"]]
    obs_rows = [o for r in results for o in r["observations"]]
    cost_rows = []
    for r in results:
        c = dict(r["cost_row"]); c["batch"] = k; c["session_s"] = session_s
        cost_rows.append(c)
    _replace_rows(os.path.join(run2_dir, "screening_frame_items.tsv"), ledger.FRAME_FIELDS, "frame_rank", ranks, frame_rows)
    _replace_rows(os.path.join(run2_dir, "screening_candidates.tsv"), ledger.CANDIDATE_FIELDS, "first_frame_rank", ranks, cand_rows)
    _replace_rows(os.path.join(run2_dir, "starting_points.tsv"), ledger.SP_FIELDS, "frame_rank", ranks, sp_rows)
    _replace_rows(os.path.join(run2_dir, "observations.tsv"), ledger.OBS_FIELDS, "frame_rank", ranks, obs_rows)
    _replace_rows(os.path.join(run2_dir, "screening_cost.tsv"), ledger.COST_FIELDS, "frame_rank", ranks, cost_rows)
    xp = os.path.join(run2_dir, "exposure_log.md")
    old = io.open(xp, encoding="utf-8").read().splitlines() if os.path.exists(xp) else []
    kept = [l for l in old if not (l.startswith("| ") and len(l.split("|")) > 2 and l.split("|")[2].strip().isdigit() and int(l.split("|")[2].strip()) in ranks)]
    with io.open(xp, "w", encoding="utf-8", newline="\n") as f:
        for line in kept + [line for r in results for line in r["exposure"]]:
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
    save_state(run2_dir, state, after_batch=k)
    return p


def _state_file(run2_dir: str, after_batch: int) -> str:
    return os.path.join(run2_dir, "target", "state_b%02d.json" % after_batch)


def load_state(run2_dir: str, before_batch: int = 1) -> dict:
    """The run state as it stood before batch `before_batch` (keys and ids of batches 1..before_batch-1)."""
    st = new_state(run2_dir)
    p = _state_file(run2_dir, before_batch - 1)
    if before_batch > 1 and os.path.exists(p):
        st.update(json.load(io.open(p, encoding="utf-8")))
    elif before_batch > 1:
        raise RuntimeError("no state after batch %d: run the batches in order" % (before_batch - 1))
    return st


def save_state(run2_dir: str, state: dict, after_batch: int) -> None:
    os.makedirs(os.path.join(run2_dir, "target"), exist_ok=True)
    io.open(_state_file(run2_dir, after_batch), "w", encoding="utf-8", newline="\n").write(
        json.dumps({k: v for k, v in state.items() if k in ("keys", "next_id")}, indent=1))


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] in ("preview", "batch"):
        out = run_batch(int(argv[1]), paths.RUN2, argv[2], commit=(argv[0] == "batch"))
        if argv[0] == "batch":
            print("written", out)
        else:
            for r in out:
                f = r["frame_row"]
                print("rank %s %s: UR=%s cand=%s terminal=%s stop=%s" % (f["frame_rank"], f["port_path"], f["upstream_resolution"], f["candidate_id"], f["terminal_status"], f["stop_gate"]))
                for sp in r["starting_points"]:
                    print("   %-18s %-10s %s -> %s %s %s" % (sp["source"], sp["action"], sp["url"], sp.get("final_url", ""), sp.get("final_class", ""), sp.get("http_status", "")))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
