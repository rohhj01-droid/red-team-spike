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

INFRA = FIX + "/ports/infrastructure"


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
