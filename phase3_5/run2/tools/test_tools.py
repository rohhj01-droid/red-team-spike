"""Tests for the Run 2 screening tools. Assert-based, in the project's own
style; no test framework.

Run (from the repository root):
    python -I phase3_5/run2/tools/test_tools.py

`-I` leaves this directory off sys.path, so it is added explicitly; the
exploratory tools are added through paths.use_exploratory_tools().
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FIX = os.path.join(HERE, "fixtures")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TMP = tempfile.mkdtemp(prefix="run2tools_")

import paths  # noqa: E402
paths.use_exploratory_tools()
import frame  # noqa: E402
import metadata  # noqa: E402
import surfaces  # noqa: E402
import net  # noqa: E402
import en_verdicts  # noqa: E402
import pin  # noqa: E402
import ledger  # noqa: E402
import screen  # noqa: E402
import inventory  # noqa: E402  (exploratory tool)


def make_tree(root, sizes):
    """Files of the given byte sizes under root/<name>; returns root."""
    for rel, n in sizes.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(b"x" * n)
    return root

INFRA = FIX + "/ports/infrastructure"
CTREE = FIX + "/ctree"
TIMEOUT = "TIMEOUT"


def canned(seq):
    """A fetch callable returning (status, headers, body) per call; the TIMEOUT sentinel raises like a transport failure."""
    items = list(seq)

    def fetch(url):
        item = items.pop(0)
        if item == TIMEOUT:
            raise TimeoutError("canned timeout")
        return item
    return fetch


def fixed_clock():
    return "2026-10-29T12:00:00Z"


# ---------------------------------------------------------------- Task 2: frame

def test_exploratory_tools_unchanged():
    r = subprocess.run(["git", "diff", "--quiet", "35255d6", "--", "phase3_5/exploratory/tools"], cwd=REPO_ROOT)
    assert r.returncode == 0


def test_enumerate_games_tokens():                 # Review Focus: token, not substring
    items = frame.enumerate_games(FIX + "/ports")
    assert items == ["devel/beta", "games/alpha", "games/delta/sub"], items


def test_screening_set_budget():
    assert frame.screening_set(["b", "a", "c"], budget=2) == ["b", "a"]      # order preserved, cut at budget


def test_check_against_run1_reports_differences():
    tmp = os.path.join(TMP, "set.txt")
    open(tmp, "w").write("games/alpha\ngames/zeta\n")
    assert frame.check_against_run1(["games/alpha", "games/beta"], tmp) == [(2, "games/zeta", "games/beta")]


def test_verify_archive_mismatch():
    p = os.path.join(TMP, "x.tar.gz")
    open(p, "wb").write(b"not the frame")
    ok, sha, size = frame.verify_archive(p)
    assert not ok and size == 13 and len(sha) == 64


def test_extract_selected_filters_members():
    import io as _io
    import tarfile
    p = os.path.join(TMP, "mini.tar.gz")
    with tarfile.open(p, "w:gz") as t:
        for name, data in [("ports/games/x/Makefile", b"CATEGORIES = games\n"), ("ports/games/x/README", b"no"),
                           ("ports/games/x/pkg/DESCR", b"d"), ("ports/infrastructure/mk/bsd.port.mk", b"mk"),
                           ("ports/../evil", b"x")]:
            info = tarfile.TarInfo(name); info.size = len(data)
            t.addfile(info, _io.BytesIO(data))
    dest = os.path.join(TMP, "extract")
    n = frame.extract_selected(p, dest)
    assert n == 3, n
    assert os.path.exists(os.path.join(dest, "ports", "games", "x", "Makefile"))
    assert not os.path.exists(os.path.join(dest, "ports", "games", "x", "README"))
    assert not os.path.exists(os.path.join(TMP, "evil")) and not os.path.exists(os.path.join(dest, "evil"))


# ---------------------------------------------------------------- Task 3: metadata

def test_explicit_homepage_and_sites_macro_expansion():          # Review Focus 1
    m = metadata.resolve(FIX + "/ports/games/alpha", INFRA)
    assert m["homepage"] == "https://alpha.example.org/" and m["homepage_mechanism"] == "explicit"
    assert m["sites"] == ["https://downloads.sourceforge.net/sourceforge/alpha/",
                          "https://netix.dl.sourceforge.net/project/alpha/"], m["sites"]
    assert m["sites_mechanism"][m["sites"][0]] == "explicit" and m["issue"] is None
    assert m["comment"] == "alpha game" and m["descr"].startswith("Alpha") and m["distname"] == "alpha-1.0"


def test_gh_defaults_homepage_and_sites():
    m = metadata.resolve(FIX + "/ports/devel/beta", INFRA)
    assert m["homepage"] == "https://github.com/acme/Beta" and m["homepage_mechanism"] == "gh"
    assert m["sites"] == ["https://github.com/acme/Beta/archive/refs/tags/v1.2/"]
    assert m["sites_mechanism"][m["sites"][0]] == "gh-tagname" and m["gh"] == ("acme", "Beta")


def test_dist_tuple_homepage_and_empty_bare_sites():
    m = metadata.resolve(FIX + "/ports/games/delta/sub", INFRA)
    assert m["homepage"] == "https://github.com/acme/gamma" and m["homepage_mechanism"] == "dist-tuple"
    assert m["sites"] == [] and m["dist_tuples"] == [("github", "acme", "gamma", "1.0")]


def test_module_is_unresolved():
    assert metadata.resolve(FIX + "/ports/games/modport", INFRA)["issue"] == "PI-METADATA-UNRESOLVED"


def test_unknown_macro_is_unresolved():                         # Review Focus 1
    m = metadata.resolve(FIX + "/ports/games/eps", INFRA)
    assert m["issue"] == "PI-METADATA-UNRESOLVED" and all("${" not in s for s in m["sites"])


def test_tag_and_distname_macros_expand():                      # batch 1: rank 8 GH_TAGNAME = dosbox-x-v${VERSION}; rank 5 SITES = ...v$V/
    m = metadata.resolve(FIX + "/ports/games/tagmac", INFRA)
    assert m["sites"] == ["https://github.com/acme/tagmac/archive/refs/tags/v1.2/", "https://example.org/dl/v1.2/"], m["sites"]
    assert m["distname"] == "tagmac-1.2" and m["issue"] is None, m


def test_unknown_tag_macro_is_unresolved():
    m = metadata.resolve(FIX + "/ports/games/tagbad", INFRA)
    assert m["issue"] == "PI-METADATA-UNRESOLVED" and m["sites"] == [], m


def test_ledger_check_flags_single_char_macro():
    root = os.path.join(TMP, "run2m")
    os.makedirs(root, exist_ok=True)
    open(os.path.join(root, "screening_set_128.txt"), "w").write("games/alpha\n")
    screen.run_batch(1, root, FIX + "/ports", fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    assert ledger.check(root, expect_rows=1) == 0
    sps = ledger.read_rows(os.path.join(root, "starting_points.tsv"), ledger.SP_FIELDS)
    bad = dict(sps[0])
    bad["url"] = "https://example.org/dl/v$V/"
    ledger.write_rows(os.path.join(root, "starting_points.tsv"), sps + [bad], ledger.SP_FIELDS)
    assert ledger.check(root, expect_rows=1) == 1


def test_ledger_check_flags_malformed_witness_row():
    root = os.path.join(TMP, 'run2w')
    os.makedirs(root, exist_ok=True)
    TAB, NL, BS = chr(9), chr(10), chr(92)
    open(os.path.join(root, 'screening_set_128.txt'), 'w').write('games/alpha' + NL)
    screen.run_batch(1, root, FIX + '/ports', fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    path = os.path.join(root, 'witness_b01.tsv')
    head = TAB.join(ledger.WITNESS_FIELDS) + NL
    good = ['1', 'C001', 'E4', 'refusal-path', 'EN:C001', 'src/a.c:3', 'puts("bad' + BS + 'n");', '']
    open(path, 'w', encoding='utf-8', newline=NL).write(head + TAB.join(good) + NL)
    assert ledger.check(root, expect_rows=1) == 0
    split = ['1', 'C001', 'E4', 'refusal-path', 'EN:C001', 'src/a.c:3', 'puts("bad' + NL + '");', '']
    open(path, 'w', encoding='utf-8', newline=NL).write(head + TAB.join(split) + NL)
    assert ledger.check(root, expect_rows=1) == 1


# ---------------------------------------------------------------- Task 4: surfaces

def test_normalize_url():
    assert surfaces.normalize_url("HTTP://GitHub.com/Acme/Beta.git/?x=1#f") == "https://github.com/Acme/Beta"
    assert surfaces.normalize_url("https://user:pw@example.org/p/") == "https://example.org/p"


def test_classify_table():
    c = surfaces.classify
    assert c("https://github.com/acme/beta") == "repository-root"
    assert c("https://github.com/acme/beta/releases/download/v1/x.tgz") == "release-assets"
    assert c("https://github.com/acme/beta/archive/refs/tags/v1.2/") == "release-assets"
    assert c("https://gitlab.com/grp/sub/proj/-/releases") == "release-assets"
    assert c("https://gitlab.com/grp/sub/proj") == "repository-root"
    assert c("https://git.example.org/acme/beta") == "repository-root"
    assert c("https://example.org/src/beta.git") == "repository-root"
    assert c("https://downloads.sourceforge.net/sourceforge/alpha/") == "distfile-location"
    assert c("https://sourceforge.net/projects/alpha/files/") == "distfile-location"
    assert c("https://ftp.gnu.org/gnu/alpha/") == "distfile-location"
    assert c("https://example.org/dl/alpha-1.0.tar.gz") == "distfile-location"
    assert c("https://alpha.example.org/") is None          # unmatched: one request decides (Task 8)
    assert all(len(row) == 3 and row[2] in surfaces.CLASSES for row in surfaces.SURFACE_TABLE)


def test_starting_points_from_gh_port():                       # contract 4: one surface, two sources
    sp = surfaces.starting_points(metadata.resolve(FIX + "/ports/devel/beta", INFRA))
    assert [(s["url"], s["source"], s["klass"]) for s in sp] == [
        ("https://github.com/acme/Beta", "HOMEPAGE+GH", "repository-root"),
        ("https://github.com/acme/Beta/archive/refs/tags/v1.2/", "SITES", "release-assets")], sp


def test_starting_points_each_sites_url():                     # Task 3 ruling: every mirror word is a starting point
    sp = surfaces.starting_points(metadata.resolve(FIX + "/ports/games/alpha", INFRA))
    assert [s["source"] for s in sp] == ["HOMEPAGE", "SITES", "SITES"] and sp[0]["klass"] is None and sp[1]["klass"] == "distfile-location"


def test_identity_key_and_ambiguity():
    m = metadata.resolve(FIX + "/ports/devel/beta", INFRA)
    assert surfaces.identity_key(m, {}) == ("PASS", "https://github.com/acme/beta")
    m2 = dict(m, dist_tuples=[("github", "other", "thing", "1")], tuple_dirs=["."])
    assert surfaces.identity_key(m2, {})[0] == "FAIL_AMBIGUOUS"
    a = metadata.resolve(FIX + "/ports/games/alpha", INFRA)
    assert surfaces.identity_key(a, {}) == ("PASS", "https://alpha.example.org")
    none = dict(a, homepage=None, sites=["https://distfiles.openbsd.org/x/alpha-1.0.tar.gz"])
    assert surfaces.identity_key(none, {})[0] == "FAIL_NONE"


# ---------------------------------------------------------------- Task 5: net

def test_redirect_chain_recorded():                             # Review Focus 2
    seq = [(301, {"Location": "https://new.example.org/"}, b""), (200, {"Content-Type": "text/html"}, b"<html></html>")]
    r = net.fetch("http://old.example.org/", fetch=canned(seq), clock=fixed_clock)
    assert r["final_url"] == "https://new.example.org/" and r["redirect_chain"] == ["http://old.example.org/"]
    assert r["http_status"] == 200 and r["outcome"] == "ok" and r["content_type"] == "text/html"


def test_transport_retries_then_pi():                           # Review Focus 4
    r = net.fetch("https://x.example.org/", fetch=canned([TIMEOUT, TIMEOUT, TIMEOUT]), clock=fixed_clock)
    assert r["outcome"] == "transport" and [a[1] for a in r["attempts"]] == ["transport"] * 3


def test_5xx_is_transport_and_recovers():
    r = net.fetch("https://x.example.org/", fetch=canned([(503, {}, b""), (200, {}, b"ok")]), clock=fixed_clock)
    assert r["outcome"] == "ok" and [a[1] for a in r["attempts"]] == ["transport", "ok"]


def test_definitive_404_is_not_transport():
    r = net.fetch("https://x.example.org/", fetch=canned([(404, {}, b"")]), clock=fixed_clock)
    assert r["outcome"] == "definitive" and r["http_status"] == 404 and len(r["attempts"]) == 1


def test_step2_whole_word_only():                               # Review Focus 3
    ls = net.links(open(FIX + "/html/project.html", "rb").read(), "https://alpha.example.org/")
    assert [l["href"] for l in net.step2_links(ls)] == ["https://github.com/acme/beta", "https://alpha.example.org/dev"]
    assert net.is_step2(dict(label="Quellcode", title="", aria_label="", href="x"))
    assert not net.is_step2(dict(label="Barcode", title="", aria_label="", href="x"))


def test_designation_is_not_permission():
    ls = net.links(open(FIX + "/html/project.html", "rb").read(), "https://alpha.example.org/")
    assert all("official" not in l["label"].lower() for l in net.step2_links(ls))
    assert net.designation_signals("Our official repository is on GitHub. Have fun.") == ["Our official repository is on GitHub."]
    assert "Alpha README" in net.text_of(open(FIX + "/html/repo.html", "rb").read())


# ---------------------------------------------------------------- Task 6: en_verdicts

def _decided():
    return {r["symbol"]: en_verdicts.decide(r, tree=CTREE) for r in inventory.enumerators(CTREE)}


def _cid(rows, symbol):
    return [r for r in rows if r["symbol"] == symbol][0]["cand_id"]


def test_catalogue_has_no_project_specific_rule():
    assert all(r.kind not in en_verdicts.RULE_KINDS_FORBIDDEN for r in en_verdicts.CATALOGUE)
    assert all(not re.search(r"\.(c|h|m)\b", r.name) for r in en_verdicts.CATALOGUE)   # no file names in rule names
    assert all(r.en in ("EN2", "EN4") for r in en_verdicts.CATALOGUE)


def test_decide_by_catalogue_and_undecided():
    d = _decided()
    assert d["sine_table"]["decided_by"] == "catalogue:numeric-data" and d["sine_table"]["en2"] == "FAIL"
    assert d["dispatch"]["decided_by"] == "catalogue:dispatch-table"
    assert d["menu_labels"]["decided_by"] == "catalogue:presentation-vocabulary"
    assert d["valid_modes"]["decided_by"] == "UNDECIDED" and d["valid_modes"]["en2"] == ""   # acceptance vocabulary: quotation needed
    assert d["expected_values"]["decided_by"] == "catalogue:test-fixture"
    assert d["old_names"]["decided_by"] == "catalogue:dead-code"
    assert all(v["en1"] == "PASS" and v["en3"] == "PASS" for v in d.values())


def test_apply_quoted_requires_citation_for_admit():
    rows = [en_verdicts.decide(r, tree=CTREE) for r in inventory.enumerators(CTREE)]
    cid = _cid(rows, "valid_modes")
    try:
        en_verdicts.apply_quoted(rows, [dict(cand_id=cid, verdict="ADMIT", tag="enforced", evidence="no citation")])
        assert False, "an ADMIT without a file:line citation must be refused"
    except ValueError:
        pass
    out = en_verdicts.apply_quoted(rows, [dict(cand_id=cid, verdict="ADMIT", tag="enforced",
                                               evidence="EN2: src/modes.c:4 'the valid modes'; EN4: src/modes.c:22 miss -> I_Error")])
    vm = [r for r in out if r["symbol"] == "valid_modes"][0]
    assert vm["tag"] == "enforced" and vm["decided_by"] == "quoted" and all(vm[k] == "PASS" for k in ("en1", "en2", "en3", "en4", "en5", "en6"))


def test_class_and_sensitivity():
    rows = [en_verdicts.decide(r, tree=CTREE) for r in inventory.enumerators(CTREE)]
    cid = _cid(rows, "valid_modes")
    rows = en_verdicts.apply_quoted(rows, [dict(cand_id=cid, verdict="ADMIT", tag="enforced", evidence="EN2: src/modes.c:4; EN4: src/modes.c:22")])
    assert en_verdicts.class_of(rows) == "A"
    rows2 = [dict(r, tag="asserted") if r["symbol"] == "valid_modes" else r for r in rows]
    assert en_verdicts.class_of(rows2) == "B"
    assert en_verdicts.class_of([r for r in rows if r["symbol"] != "valid_modes"]) == "B"      # nothing admitted
    s = en_verdicts.sensitivity(rows)
    assert any(r["symbol"] == "valid_modes" and r["why"] == "admitted" for r in s)
    assert all(r["decided_by"] != "catalogue:numeric-data" for r in s)


# ---------------------------------------------------------------- Task 7: pin

def test_ten_digests_largest_source_files_in_path_order():
    tree = make_tree(os.path.join(TMP, "pintree"), {"a.c": 300, "b.h": 300, "c.txt": 999, "d.py": 10, "e/f.c": 300, ".git/x.c": 5000})
    rows = pin.ten_digests(tree)
    assert [p for p, _, _ in rows] == ["a.c", "b.h", "e/f.c", "d.py"], rows      # .txt and .git excluded; size desc; ties by path
    assert all(len(sha) == 64 for _, _, sha in rows) and rows[0][1] == 300


def test_ls_remote_parses_symref():
    out = "ref: refs/heads/main\tHEAD\nabc123\tHEAD\n"
    assert pin.ls_remote("https://x", git=lambda args: out) == ("main", "abc123")


def test_fetch_by_hash_sets_autocrlf_false():
    calls = []
    pin.fetch_by_hash("https://x", "abc123", os.path.join(TMP, "t"), git=lambda args: calls.append(args) or "")
    assert ["config", "core.autocrlf", "false"] in [c[-3:] for c in calls]
    assert any("--depth" in c and "abc123" in c for c in calls) and ["checkout", "--detach", "FETCH_HEAD"] in [c[-3:] for c in calls]


def test_write_record_files():
    d = os.path.join(TMP, "pinrec")
    rec = dict(candidate_id="C001", url="https://github.com/acme/alpha", branch="main", sha="abc123", observed_at_utc="2026-10-29T12:00:00Z",
               archive=dict(url="https://github.com/acme/alpha/archive/abc123.tar.gz", bytes=10, sha256="f" * 64, entries=3),
               digests=[("a.c", 300, "e" * 64)], tracked_files=4)
    pin.write_record(d, rec)
    assert os.path.exists(os.path.join(d, "pin_record.md")) and os.path.exists(os.path.join(d, "pin.json"))
    text = open(os.path.join(d, "pin_record.md"), encoding="utf-8").read()
    assert "abc123" in text and "a.c" in text and "observation time" in text.lower()


# ---------------------------------------------------------------- Task 8: screen + ledger

def _html(path):
    return open(os.path.join(FIX, "html", path), "rb").read()


def _tiny_targz():
    import io as _io
    import tarfile
    buf = _io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for name, data in [("alpha-abc123/src/modes.c", b"x"), ("alpha-abc123/README", b"r")]:
            info = tarfile.TarInfo(name); info.size = len(data)
            t.addfile(info, _io.BytesIO(data))
    return buf.getvalue()


def canned_map(mapping):
    """fetch(url) -> (status, headers, body); a list value is consumed in order; a missing url is a 404."""
    m = {k: (list(v) if isinstance(v, list) else [v]) for k, v in mapping.items()}

    def fetch(url):
        seq = m.get(url)
        if not seq:
            return (404, {"Content-Type": "text/html"}, b"<html>missing</html>")
        return seq.pop(0) if len(seq) > 1 else seq[0]
    return fetch


HTML = {"Content-Type": "text/html"}
LISTING = (200, HTML, b"<html><head><title>Index of /alpha</title></head><body><a href='alpha-1.0.tar.gz'>alpha-1.0.tar.gz</a></body></html>")
ALPHA_MAP = {
    "https://alpha.example.org/": (200, HTML, _html("alpha_project.html")),
    "https://downloads.sourceforge.net/sourceforge/alpha/": LISTING,
    "https://netix.dl.sourceforge.net/project/alpha/": LISTING,
    "https://github.com/acme/alpha": (200, HTML, _html("repo.html")),
    "https://github.com/acme/alpha/archive/abc123.tar.gz": (200, {"Content-Type": "application/x-gzip"}, _tiny_targz()),
}
ALPHA_WITNESSES = [
    dict(frame_rank="1", candidate_id="", gate="E2-REP", kind="designation", surface="https://github.com/acme/alpha",
         location="https://github.com/acme/alpha", quote="Official repository.", tag=""),
    dict(frame_rank="1", candidate_id="", gate="E2-REP", kind="identifier", surface="https://github.com/acme/alpha",
         location="https://github.com/acme/alpha", quote="acme/alpha", tag=""),
]


def fake_git_factory(calls=None):
    import shutil
    calls = [] if calls is None else calls

    def git(args):
        calls.append(list(args))
        if args[0] == "ls-remote":
            return "ref: refs/heads/main\tHEAD\nabc123\tHEAD\n"
        if "checkout" in args:
            dest = args[args.index("-C") + 1]
            shutil.copytree(CTREE, dest, dirs_exist_ok=True)
        if "ls-files" in args:
            return "src/modes.c\nsrc/strings.c\n"
        return ""
    return git


def _state(name):
    root = os.path.join(TMP, name)
    os.makedirs(root, exist_ok=True)
    return screen.new_state(root)


def test_alpha_passes_e2rep_with_one_designation():
    out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state=_state("s1"),
                             fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert c["E2_REP"] == "PASS" and c["canonical_source_location"] == "https://github.com/acme/alpha", c
    assert c["external_target_identifier"] == "acme/alpha" and c["primary_snapshot"] == "abc123"
    assert all(sp["action"] in ("observed", "closed-by-class") for sp in out["starting_points"]), out["starting_points"]
    assert c["E2_RULE"] == "UNRESOLVED" and c["E3"] == "NOT_REACHED" and c["overall"] == "UNRESOLVED"   # no witnesses past E2-REP
    assert any(b.startswith("## EV-C001-E2REP-") for b in out["evidence_blocks"])


def test_unreachable_starting_point_blocks_e2rep_pass():
    # contract 7 / Run 1 QA-41: a PASS needs every admitted starting point not closed-by-class observed (RQA-11)
    base = canned_map(ALPHA_MAP)

    def fetch(url):
        if url == "https://downloads.sourceforge.net/sourceforge/alpha/":
            raise TimeoutError("canned timeout")
        return base(url)
    out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state=_state("s16"),
                             fetch=fetch, clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert "unreachable" in [sp["action"] for sp in out["starting_points"]], out["starting_points"]
    assert c["E2_REP"] == "UNRESOLVED" and c["failure_code"] == "NONE" and c["protocol_issue_code"] == "PI-TRANSPORT-INDETERMINATE", c
    assert c["primary_snapshot"] == "NOT_REACHED" and c["E2_RULE"] == "NOT_REACHED", c


def test_undesignated_repository_root_is_an_admitted_starting_point():   # contract 7's roles (RQA-16)
    beta = {"https://github.com/acme/Beta": (200, HTML, b"<html><body><p>Beta, a library.</p></body></html>")}
    out = screen.screen_item(2, "devel/beta", FIX + "/ports", witnesses=[], state=_state("s18"),
                             fetch=canned_map(beta), clock=fixed_clock, git=fake_git_factory())
    assert out["candidate_row"]["E2_REP"] == "UNRESOLVED", out["candidate_row"]
    roots = [sp for sp in out["starting_points"] if sp["final_class"] == "repository-root"]
    assert roots and all(sp["action"] == "observed" and sp["evidence_role"] == "admitted-starting-point" for sp in roots), roots


def test_batch_commits_pin_records_under_inventory():            # contract 10 (RQA-18)
    root = os.path.join(TMP, "run2pin")
    os.makedirs(root, exist_ok=True)
    open(os.path.join(root, "screening_set_128.txt"), "w").write("games/alpha" + chr(10))
    ledger.write_witnesses(root, 1, ALPHA_WITNESSES)
    screen.run_batch(1, root, FIX + "/ports", fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    frame = ledger.read_rows(os.path.join(root, "screening_frame_items.tsv"), ledger.FRAME_FIELDS)[0]
    assert frame["pin_ref"] == "inventory/C001/pin.json", frame
    for name in ("pin.json", "pin_record.md"):
        assert open(os.path.join(root, "inventory", "C001", name), "rb").read() == open(os.path.join(root, "target", "C001", name), "rb").read(), name


def test_pin_archive_request_is_an_observation():                 # contract 9.4: step `pin` (RQA-18)
    for _ in range(2):                                             # the second run reuses the pin and still reports its request
        out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state=_state("s20"),
                                 fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
        pins = [o for o in out["observations"] if o["step"] == "pin"]
        assert [o["requested_url"] for o in pins] == ["https://github.com/acme/alpha/archive/abc123.tar.gz"], out["observations"]
        assert pins[0]["outcome"] == "ok" and pins[0]["http_status"] == 200, pins


def test_sites_page_is_an_admitted_starting_point():              # contract 7's roles: only HOMEPAGE is the project page (RQA-23)
    tag = {"https://example.org/dl/v1.2/": (200, HTML, b"<html><body><p>Downloads for tagmac.</p></body></html>"),
           "https://github.com/acme/tagmac": (200, HTML, b"<html><head><title>acme/tagmac</title></head><body><p>tagmac</p></body></html>")}
    out = screen.screen_item(1, "games/tagmac", FIX + "/ports", witnesses=[], state=_state("s24"),
                             fetch=canned_map(tag), clock=fixed_clock, git=fake_git_factory())
    page = [sp for sp in out["starting_points"] if sp["source"] == "SITES.extra"]
    assert page and page[0]["final_class"] == "project-page" and page[0]["evidence_role"] == "admitted-starting-point", out["starting_points"]


def test_404_does_not_fail_candidate_alone():                   # Review Focus 4
    out = screen.screen_item(2, "devel/beta", FIX + "/ports", witnesses=[], state=_state("s2"),
                             fetch=canned_map({}), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert c["E2_REP"] == "UNRESOLVED" and c["failure_code"] == "NONE" and c["protocol_issue_code"] == "PI-UNCLASSIFIED-SHAPE", c
    assert any(o["http_status"] == 404 for o in out["observations"])
    assert [sp["action"] for sp in out["starting_points"]] == ["observed", "closed-by-class"]


def test_redirect_into_forbidden_class_closes():                # Review Focus 2
    m = dict(ALPHA_MAP)
    m["https://alpha.example.org/"] = (301, {"Location": "https://github.com/acme/alpha/releases"}, b"")
    out = screen.screen_item(3, "games/alpha", FIX + "/ports", witnesses=[], state=_state("s3"),
                             fetch=canned_map(m), clock=fixed_clock, git=fake_git_factory())
    sp = [s for s in out["starting_points"] if s["source"] == "HOMEPAGE"][0]
    assert sp["action"] == "closed-by-class" and sp["final_class"] == "release-assets", sp
    assert len([o for o in out["observations"] if o["requested_url"] == sp["url"]]) == 1


def test_duplicate_upstream_one_candidate():                    # Review Focus 5
    st = _state("s4")
    a = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state=st,
                           fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    g = screen.screen_item(2, "games/alpha2", FIX + "/ports", witnesses=[], state=st,
                           fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    assert g["frame_row"]["upstream_resolution"] == "DUPLICATE" and g["frame_row"]["duplicate_of"] == a["frame_row"]["candidate_id"]
    assert g["candidate_row"] is None and g["frame_row"]["terminal_status"] == "DUPLICATE"


def test_batch_document_and_check():
    root = os.path.join(TMP, "run2")
    os.makedirs(root, exist_ok=True)
    open(os.path.join(root, "screening_set_128.txt"), "w").write("games/alpha\ndevel/beta\ngames/alpha2\ngames/modport\n")
    ledger.write_witnesses(root, 1, ALPHA_WITNESSES)
    p = screen.run_batch(1, root, FIX + "/ports", fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    text = open(p, encoding="utf-8").read()
    assert text.count("## EV-") >= 3 and "| rank |" in text, text[:400]
    assert ledger.check(root, expect_rows=4) == 0
    rows = ledger.read_rows(os.path.join(root, "screening_frame_items.tsv"), ledger.FRAME_FIELDS)
    assert [r["terminal_status"] for r in rows] == ["UNRESOLVED", "UNRESOLVED", "DUPLICATE", "UNRESOLVED"]
    assert rows[3]["protocol_issue_code"] == "PI-METADATA-UNRESOLVED" and rows[3]["stop_gate"] == "UR"


# ---------------------------------------------------------------- Task 10 support: cache, preview, idempotent re-run

def counting_fetch(mapping):
    base = canned_map(mapping)
    calls = []

    def fetch(url):
        calls.append(url)
        return base(url)
    fetch.calls = calls
    return fetch


def test_run_batch_preview_writes_no_ledger_and_caches_observations():
    root = os.path.join(TMP, "run2p")
    os.makedirs(root, exist_ok=True)
    open(os.path.join(root, "screening_set_128.txt"), "w").write("games/alpha\ndevel/beta\n")
    f = counting_fetch(ALPHA_MAP)
    results = screen.run_batch(1, root, FIX + "/ports", fetch=f, clock=fixed_clock, git=fake_git_factory(), commit=False)
    assert isinstance(results, list) and len(results) == 2
    assert not os.path.exists(os.path.join(root, "screening_frame_items.tsv")) and not os.path.exists(os.path.join(root, "screening_evidence_b01.md"))
    first = len(f.calls)
    assert first > 0
    ledger.write_witnesses(root, 1, ALPHA_WITNESSES)
    p = screen.run_batch(1, root, FIX + "/ports", fetch=f, clock=fixed_clock, git=fake_git_factory())
    extra = f.calls[first:]                                                  # the final run re-used every cached observation;
    assert all("/archive/" in u for u in extra), extra                       # at most the pin's archive, taken when E2-REP passes, is new
    rows = ledger.read_rows(os.path.join(root, "screening_candidates.tsv"), ledger.CANDIDATE_FIELDS)
    assert rows[0]["E2_REP"] == "PASS" and os.path.exists(p)


def test_run_batch_rerun_replaces_its_own_rows():
    root = os.path.join(TMP, "run2r")
    os.makedirs(root, exist_ok=True)
    open(os.path.join(root, "screening_set_128.txt"), "w").write("games/alpha\ndevel/beta\n")
    kw = dict(fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    screen.run_batch(1, root, FIX + "/ports", **kw)
    screen.run_batch(1, root, FIX + "/ports", **kw)
    frame_rows = ledger.read_rows(os.path.join(root, "screening_frame_items.tsv"), ledger.FRAME_FIELDS)
    obs_rows = ledger.read_rows(os.path.join(root, "observations.tsv"), ledger.OBS_FIELDS)
    assert [r["frame_rank"] for r in frame_rows] == ["1", "2"]
    assert len({(o["requested_url"], o["attempt"]) for o in obs_rows}) == len(obs_rows)   # no duplicated observation rows
    assert ledger.check(root, expect_rows=2) == 0


def test_decide_builds_struct_map_once_per_tree():              # performance only: the catalogue's decisions do not change
    calls = []
    real = inventory.struct_map

    def counting(tree):
        calls.append(tree)
        return real(tree)
    inventory.struct_map = counting
    try:
        rows = [en_verdicts.decide(r, tree=CTREE) for r in inventory.enumerators(CTREE)]
    finally:
        inventory.struct_map = real
    assert len(rows) >= 5 and len(calls) == 1, (len(rows), len(calls))


# ---------------------------------------------------------------- contract 8: E4 UNRESOLVED lists the surfaces read

PAST_E2REP = ALPHA_WITNESSES + [
    dict(frame_rank="1", candidate_id="", gate="E2-RULE", kind="validity", surface="src/modes.c", location="src/modes.c:4",
         quote="the valid modes a player may ask for", tag=""),
    dict(frame_rank="1", candidate_id="", gate="E3", kind="stateful", surface="src/modes.c", location="src/modes.c:9",
         quote='{ "easy", 1 },', tag=""),
]


def test_e4_unresolved_block_lists_absence_survey():
    ws = PAST_E2REP + [dict(frame_rank="1", candidate_id="", gate="E4", kind="absence-survey", surface="src/strings.c:1",
                            location="src/strings.c:1", quote="const char *menu_labels[] = {", tag="")]
    out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ws, state=_state("s9"),
                             fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert c["E2_RULE"] == "PASS" and c["E3"] == "PASS" and c["E4"] == "UNRESOLVED", c
    block = [b for b in out["evidence_blocks"] if "Gate: E4" in b][0]
    assert "src/strings.c:1" in block, block


def test_e4_absence_survey_quote_is_verified():
    ws = PAST_E2REP + [dict(frame_rank="1", candidate_id="", gate="E4", kind="absence-survey", surface="src/strings.c:1",
                            location="src/strings.c:1", quote="not a line of that file", tag="")]
    try:
        screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ws, state=_state("s10"),
                           fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    except screen.Witness:
        return
    assert False, "an absence-survey quote that is not in the pinned tree was accepted"


def test_e2rule_absence_survey_quote_is_verified():               # contract 9.5: every witness quote is checked (RQA-13)
    ws = ALPHA_WITNESSES + [dict(frame_rank="1", candidate_id="", gate="E2-RULE", kind="absence-survey", surface="src/modes.c",
                                 location="src/modes.c:1", quote="not a line of that file", tag="")]
    try:
        screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ws, state=_state("s17"),
                           fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    except screen.Witness:
        return
    assert False, "an E2-RULE absence-survey quote that is not in the pinned tree was accepted"


def test_survey_block_cites_the_gate_surfaces_not_starting_points():   # RQA-17
    ws = ALPHA_WITNESSES + [dict(frame_rank="1", candidate_id="", gate="E2-RULE", kind="absence-survey", surface="src/modes.c",
                                 location="src/modes.c:4", quote="the valid modes a player may ask for", tag="")]
    out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ws, state=_state("s19"),
                             fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    block = [b for b in out["evidence_blocks"] if "Gate: E2-RULE" in b][0]
    assert "Section 8" in block and "admitted starting point" not in block, block


def test_directory_names_survey_row_is_verified():               # contract 8: the names under test/ (RQA-21)
    def run(quote, state):
        ws = ALPHA_WITNESSES + [dict(frame_rank="1", candidate_id="", gate="E2-RULE", kind="absence-survey", surface="test/",
                                     location="test/", quote=quote, tag="")]
        return screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ws, state=_state(state),
                                  fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
    out = run("data.c", "s22")
    assert any("test/" in b for b in out["evidence_blocks"] if "Gate: E2-RULE" in b), out["evidence_blocks"]
    try:
        run("nope.c", "s23")
    except screen.Witness:
        return
    assert False, "a directory survey row naming an absent entry was accepted"


def test_unresolved_past_e2rep_carries_unclassified_shape():
    # design 4.7: E2-RULE, E3 and E4 are decided as Run 1's amendment decides them -- UNRESOLVED / PI-UNCLASSIFIED-SHAPE (RQA-10)
    for name, ws, gate in (("s14", ALPHA_WITNESSES, "E2-RULE"), ("s15", PAST_E2REP, "E4")):
        out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ws, state=_state(name),
                                 fetch=canned_map(ALPHA_MAP), clock=fixed_clock, git=fake_git_factory())
        c, f = out["candidate_row"], out["frame_row"]
        assert c["overall"] == "UNRESOLVED" and c["stop_gate"] == gate and c["failure_code"] == "NONE", c
        assert c["protocol_issue_code"] == "PI-UNCLASSIFIED-SHAPE" and f["protocol_issue_code"] == "PI-UNCLASSIFIED-SHAPE", (c, f)


# ---------------------------------------------------------------- RQA-02 readings (before any verdict)

def test_modules_matter_only_when_they_supply_a_field():        # RQA-02 (a)
    assert metadata.resolve(FIX + "/ports/games/qmaker", INFRA)["issue"] is None            # GH pair resolves both fields; the module is a build tool
    assert metadata.resolve(FIX + "/ports/games/pyport", INFRA)["issue"] == "PI-METADATA-UNRESOLVED"   # SITES would come from the module
    assert metadata.resolve(FIX + "/ports/games/modport", INFRA)["issue"] == "PI-METADATA-UNRESOLVED"  # nothing resolved, module present


def test_code_host_archive_endpoints_are_release_assets():      # RQA-12: zipball / tarball / codeload are archive areas
    for u in ("https://github.com/cebix/frodo4/zipball/master", "https://github.com/acme/beta/tarball/v1.2",
              "https://codeload.github.com/cebix/frodo4/legacy.zip/main"):
        assert surfaces.classify(u) == "release-assets", u
    assert surfaces.classify("https://github.com/acme/zipball") == "repository-root"   # a repository named zipball is still a root


def test_classify_repository_file_and_root():                    # RQA-02 (f)
    assert surfaces.classify("https://github.com/acme/gamma/blob/main/BUILD.md") == "repository-file"
    assert surfaces.classify("https://gitlab.com/grp/proj/-/blob/main/README.md") == "repository-file"
    assert surfaces.repository_root_of("https://github.com/acme/gamma/blob/main/BUILD.md") == "https://github.com/acme/gamma"
    assert surfaces.repository_root_of("https://github.com/acme/gamma") == "https://github.com/acme/gamma"
    assert surfaces.repository_root_of("https://gamma.example.org/dev.html") is None


GAMMA_MAP = {
    "https://gamma.example.org/": (200, HTML, _html("gamma_project.html")),
    "https://gamma.example.org/dev.html": (200, HTML, b"<html><body><p>Development builds here.</p></body></html>"),
    "https://github.com/acme/gamma/blob/main/BUILD.md": (200, HTML, b"<html><body><p>Build with make.</p></body></html>"),
    "https://github.com/acme/gamma": (200, HTML, b"<html><head><title>acme/gamma: Gamma</title></head><body><p class='about'>Gamma, the game.</p><div class='readme'>README text</div></body></html>"),
    "https://github.com/acme/gamma/archive/abc123.tar.gz": (200, {"Content-Type": "application/x-gzip"}, _tiny_targz()),
}


def test_label_link_to_repository_is_a_designation():           # RQA-02 (e)(f)
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=_state("s5"),
                             fetch=canned_map(GAMMA_MAP), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert c["E2_REP"] == "PASS" and c["canonical_source_location"] == "https://github.com/acme/gamma", c
    block = [b for b in out["evidence_blocks"] if "Gate: E2-REP" in b][0]
    assert "Source code building instructions" in block                      # the label is the quoted designation
    assert any("not a repository root" in line and "dev.html" in line for line in out["exposure"])   # RQA-02 (d): quarantined
    assert any("BUILD.md" in line for line in out["exposure"])


def test_error_response_is_an_observation():                     # RQA-02 (b)
    m = dict(ALPHA_MAP)
    m["https://downloads.sourceforge.net/sourceforge/alpha/"] = (403, HTML, b"<html>403 Forbidden</html>")
    m["https://netix.dl.sourceforge.net/project/alpha/"] = (403, HTML, b"<html>403 Forbidden</html>")
    out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state=_state("s6"),
                             fetch=canned_map(m), clock=fixed_clock, git=fake_git_factory())
    sps = [s for s in out["starting_points"] if s["source"] == "SITES"]
    assert all(s["action"] == "observed" and s["final_class"] == "distfile-location" and str(s["http_status"]) == "403" for s in sps), sps
    assert out["candidate_row"]["E2_REP"] == "PASS"


# ---------------------------------------------------------------- RQA-03 readings (before any verdict)

def test_host_name_label_authorizes_step2():                     # RQA-03 (i)
    assert net.is_step2(dict(label="GitHub", title="", aria_label="", href="x"))
    assert net.is_step2(dict(label="this project on SourceForge", title="", aria_label="", href="x"))
    assert not net.is_step2(dict(label="Download", title="", aria_label="", href="x"))


def test_sourceforge_code_repository_root_and_git_url():         # RQA-03 (j)
    assert surfaces.classify("https://sourceforge.net/p/dgen/dgen/") == "repository-root"
    assert surfaces.classify("https://sourceforge.net/projects/dgen/files/dgen/") == "distfile-location"
    assert surfaces.repository_root_of("https://sourceforge.net/p/dgen/dgen/ci/master/tree/") == "https://sourceforge.net/p/dgen/dgen"
    assert surfaces.git_url_of("https://sourceforge.net/p/dgen/dgen") == "https://git.code.sf.net/p/dgen/dgen"
    assert surfaces.git_url_of("https://github.com/acme/alpha") == "https://github.com/acme/alpha"


def test_unfetchable_repository_is_unresolved():                 # RQA-03 (j): a pin that cannot be taken
    def git_no_remote(args):
        if args[0] == "ls-remote":
            raise RuntimeError("fatal: repository not found")
        return ""
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=_state("s7"),
                             fetch=canned_map(GAMMA_MAP), clock=fixed_clock, git=git_no_remote)
    c = out["candidate_row"]
    assert c["E2_REP"] == "UNRESOLVED" and c["protocol_issue_code"] == "PI-UNCLASSIFIED-SHAPE", c


# ---------------------------------------------------------------- runner

TWIN_MAP = dict(GAMMA_MAP)
TWIN_MAP["https://gamma.example.org/"] = (200, HTML, b"<html><body><h1>Gamma</h1><p><a href='https://github.com/acme/gamma'>Source code</a></p>"
                                                     b"<p><a href='https://github.com/acme/gamma'>Source code</a></p></body></html>")


def test_exposure_lines_are_not_repeated_within_a_run():        # two identical label links -> one landing-page line
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=_state("s11"),
                             fetch=canned_map(TWIN_MAP), clock=fixed_clock, git=fake_git_factory())
    landing = [l for l in out["exposure"] if "landing page rendered" in l]
    assert out["candidate_row"]["E2_REP"] == "PASS" and len(landing) == 1, out["exposure"]


def test_derived_identifier_is_located_on_an_observed_surface():   # contract 6: the identifier row quotes where it appears
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=_state("s12"),
                             fetch=canned_map(GAMMA_MAP), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    block = [b for b in out["evidence_blocks"] if "Gate: E2-REP" in b][0]
    assert c["E2_REP"] == "PASS" and c["external_target_identifier"] == "gamma", c
    assert "identifier 'gamma'" in block.split("Observed:")[1], block


NAMELESS_MAP = dict(GAMMA_MAP)
NAMELESS_MAP["https://gamma.example.org/"] = (200, HTML, b"<html><head><title>a game</title></head><body><p><a href='https://github.com/acme/gamma'>Source code</a></p></body></html>")
NAMELESS_MAP["https://github.com/acme/gamma"] = (200, HTML, b"<html><head><title>a repository</title></head><body><p>code lives here</p></body></html>")


def test_identifier_on_no_observed_surface_is_unresolved():
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=_state("s13"),
                             fetch=canned_map(NAMELESS_MAP), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert c["E2_REP"] == "UNRESOLVED" and c["protocol_issue_code"] == "PI-UNCLASSIFIED-SHAPE", c


BINDING_MAP = dict(GAMMA_MAP)
BINDING_MAP["https://gamma.example.org/"] = (200, HTML, b"<html><body><p><a href='https://github.com/acme/gamma'>Source code</a></p>"
                                                       b"<p>Go bindings: <a href='https://github.com/other/gamma-go'>GitHub</a></p></body></html>")
BINDING_MAP["https://github.com/other/gamma-go"] = (200, HTML, b"<html><head><title>other/gamma-go</title></head><body><p>Go bindings.</p></body></html>")


def test_host_label_link_does_not_designate_beside_a_word_label():   # RQA-20
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=_state("s21"),
                             fetch=canned_map(BINDING_MAP), clock=fixed_clock, git=fake_git_factory())
    c = out["candidate_row"]
    assert c["E2_REP"] == "PASS" and c["canonical_source_location"] == "https://github.com/acme/gamma", c


def test_links_only_body_is_a_directory_listing():               # contract 5's third listing test (RQA-25)
    rec = dict(outcome="ok", content_type="text/html", final_url="https://example.org/files/",
               body=b"<html><body><a href='a-1.0.tar.gz'>a-1.0.tar.gz</a><br><a href='a-1.1.tar.gz'>a-1.1.tar.gz</a></body></html>")
    assert screen._class_by_response(rec) == "distfile-location"
    rec["body"] = b"<html><body><p>Downloads</p><a href='a-1.0.tar.gz'>a-1.0.tar.gz</a></body></html>"
    assert screen._class_by_response(rec) == "project-page"
    rec["body"] = b"<html><body><div id='app'></div></body></html>"      # a script-rendered shell: no link, no text
    assert screen._class_by_response(rec) == "unclassifiable"


OTHER_MAP = dict(GAMMA_MAP)
OTHER_MAP["https://gamma.example.org/"] = (200, HTML, b"<html><body><h1>Gamma</h1><p>Jane Roe has ported Gamma to Windows, and has posted the "
                                                     b"<a href='https://github.com/jroe/gamma-win'>source code on GitHub</a>.</p></body></html>")
OTHER_MAP["https://github.com/jroe/gamma-win"] = (200, HTML, b"<html><head><title>jroe/gamma-win</title></head><body><p>Gamma for Windows.</p></body></html>")
OTHER_MAP["https://github.com/jroe/gamma-win/archive/abc123.tar.gz"] = (200, {"Content-Type": "application/x-gzip"}, _tiny_targz())


def test_label_link_to_another_works_source_is_not_a_designation():   # RQA-28
    w = dict(frame_rank="1", candidate_id="", gate="E2-REP", kind="designation", surface="https://gamma.example.org/",
             location="https://github.com/jroe/gamma-win", tag="other-work",
             quote="Jane Roe has ported Gamma to Windows, and has posted the source code on GitHub.")
    out = screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[w], state=_state("s25"),
                             fetch=canned_map(OTHER_MAP), clock=fixed_clock, git=fake_git_factory())
    assert out["candidate_row"]["E2_REP"] == "UNRESOLVED", out["candidate_row"]
    block = [b for b in out["evidence_blocks"] if "Gate: E2-REP" in b][0]
    assert "Jane Roe has ported Gamma" in block, block


def test_tuple_moved_into_a_subdirectory_is_not_a_second_identity():   # RQA-31
    m = metadata.resolve(FIX + "/ports/games/zeta", INFRA)
    assert m["tuple_dirs"] == [".", "extern/zlib"], m
    assert surfaces.identity_key(m, {}) == ("PASS", "https://github.com/acme/zeta")
    assert surfaces.identity_key(dict(m, tuple_dirs=[".", "."]), {})[0] == "FAIL_AMBIGUOUS"   # two main trees still disagree


def test_pin_of_another_repository_under_the_id_is_not_reused():   # RQA-32
    import json
    st = _state("s26")
    d = os.path.join(st["target"], "C001")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "pin.json"), "w", encoding="utf-8") as f:
        json.dump(dict(candidate_id="C001", url="https://github.com/other/thing", sha="0" * 40, tracked_files=1), f)
    try:
        screen.screen_item(1, "x11/gamma", FIX + "/ports", witnesses=[], state=st,
                           fetch=canned_map(GAMMA_MAP), clock=fixed_clock, git=fake_git_factory())
    except RuntimeError as ex:
        assert "other/thing" in str(ex), ex
    else:
        raise AssertionError("a pin of another repository was reused")


def test_sourcehut_refs_and_archive_are_release_assets():      # RQA-37: sourcehut's tag, download and archive areas
    for u in ("https://git.sr.ht/~someone/proj/refs/download/v2.2.0/", "https://git.sr.ht/~someone/proj/refs/v2.2.0",
              "https://git.sr.ht/~someone/proj/refs", "https://git.sr.ht/~someone/proj/archive/v2.2.0.tar.gz"):
        assert surfaces.classify(u) == "release-assets", u
    assert surfaces.classify("https://git.sr.ht/~someone/proj") == "repository-root"


def test_step2_takes_web_links_only():                          # RQA-38: a mailto: link labelled with a host's name is not requested
    page = (b"<html><body><a href='https://github.com/acme/beta'>Source</a>"
            b"<a href='mailto:someone@sourceforge.net'>someone@sourceforge.net</a></body></html>")
    assert [l["href"] for l in net.step2_links(net.links(page, "https://beta.example.org/"))] == ["https://github.com/acme/beta"]


def test_tree_citation_accepts_any_path_characters():            # RQA-41: a path such as doc/c++/X.md is cited as file:line
    tree = os.path.join(TMP, "citetree")
    os.makedirs(os.path.join(tree, "doc", "c++"), exist_ok=True)
    with open(os.path.join(tree, "doc", "c++", "STYLE.md"), "w", encoding="utf-8") as f:
        f.write("All of the code is styled.")
    screen._verify_tree_quote(dict(tree=tree, rank=1), dict(location="doc/c++/STYLE.md:1", quote="All of the code is styled."))


def test_distfile_mirror_identifies_nothing():                   # RQA-44: contract 3's "bare mirror host such as distfiles.openbsd.org"
    a = metadata.resolve(FIX + "/ports/games/alpha", INFRA)
    for u in ("https://distfiles.example.net/", "https://example.org/openbsd/distfiles/"):
        m = dict(a, homepage=None, sites=[u])
        assert surfaces.identity_key(m, {u: "project-page"})[0] == "FAIL_NONE", u
    u = "https://example.org/files/"
    assert surfaces.identity_key(dict(a, homepage=None, sites=[u]), {u: "distfile-location"}) == ("PASS", "https://example.org/files")


def test_sourcecode_written_as_one_word_is_a_label_word():       # RQA-49: "Sourcecode" is "source code" written as one word
    page = b"<html><body><a href='https://github.com/acme/beta'>Sourcecode</a><a href='https://example.org/bar'>Barcode</a></body></html>"
    ls = net.links(page, "https://beta.example.org/")
    assert [l["href"] for l in net.step2_links(ls)] == ["https://github.com/acme/beta"]
    assert net.is_word_label(ls[0])


def test_ftp_answer_without_http_status_is_an_observation():     # RQA-52: an ftp:// server answers with no HTTP status
    rec = net.fetch("ftp://ftp.example.org/pub/x/", fetch=lambda u: (None, {"Content-Type": "text/plain"}, b"x-1.0.tar.gz"),
                    clock=fixed_clock)
    assert rec["outcome"] == "ok" and rec["http_status"] is None and rec["body"] == b"x-1.0.tar.gz", rec


if __name__ == "__main__":
    tests = [(n, f) for n, f in list(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("PASS  " + name)
        except Exception:
            failed += 1
            print("FAIL  " + name)
            traceback.print_exc()
    print("%d tests, %d failed" % (len(tests), failed))
    sys.exit(1 if failed else 0)
