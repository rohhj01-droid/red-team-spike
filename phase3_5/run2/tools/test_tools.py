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
    m2 = dict(m, dist_tuples=[("github", "other", "thing", "1")])
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


# ---------------------------------------------------------------- runner

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
