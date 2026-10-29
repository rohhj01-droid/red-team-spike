"""Tests for the exploratory C084 study's tools. Assert-based, in the
project's own style; no test framework.

Run (from the repository root):
    python -I phase3_5/exploratory/tools/test_tools.py

`-I` leaves this directory off sys.path, so it is added explicitly: the
tools are this project's code; the target tree under ../target/ is data.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tarfile
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FIX = os.path.join(HERE, "fixtures")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TMP = tempfile.mkdtemp(prefix="c084tools_")

from common import api_get, is_quarantined, read_tsv, sha256_file, strip, write_tsv  # noqa: E402
from snapshot import PINNED, archive, digest, sealed_instant  # noqa: E402

LATIN1 = b"/* caf\xe9 */\n"


# ---------------------------------------------------------------- Task 1

def test_sha256_bytes():          # Review Focus 4
    # fixtures/tree/src/latin1.c holds the bytes LATIN1
    assert sha256_file(FIX + "/tree/src/latin1.c") == hashlib.sha256(LATIN1).hexdigest()


def test_quarantine():            # Review Focus 3
    for p in ["NEWS.md", "news.txt", "ChangeLog", "docs/RELEASE_NOTES.md",
              "docs/release/notes.md", "src/TODO", "NOT-BUGS.md", "CHANGES"]:
        assert is_quarantined(p), p
    for p in ["README.md", "src/d_iwad.c", "docs/rules.md", "src/newsfeed.c"]:
        assert not is_quarantined(p), p
    # "newsfeed.c" is NOT quarantined: the pattern is a stem prefix, and
    # the stem "newsfeed" does not equal "news" -- prefix match applies to
    # the pattern's own stem followed by a non-letter or end


def test_tsv_roundtrip_and_reject():
    rows = [{"a": "1", "b": "x y"}]
    write_tsv(TMP + "/t.tsv", rows, ["a", "b"])
    assert read_tsv(TMP + "/t.tsv") == rows
    try:
        write_tsv(TMP + "/t.tsv", [{"a": "1\t2", "b": ""}], ["a", "b"])
        assert False, "a tab inside a cell must be rejected"
    except ValueError:
        pass


def test_strip_discards_message_and_title():
    assert strip({"sha": "x", "commit": {"message": "fix crash"}, "title": "t",
                  "labels": [{"name": "bug", "description": "d", "color": "f"}],
                  "pull_request": {"url": "u"}}, ("sha", "labels", "pull_request")) \
        == {"sha": "x", "labels": [{"name": "bug", "description": "d"}], "pull_request": True}


def test_api_get_rate_limit_raises():
    fetch = lambda url: (403, {"X-RateLimit-Reset": "1700000000"}, b"{}")  # noqa: E731
    try:
        api_get("https://api.github.com/x", fetch=fetch)
        assert False, "403 must raise"
    except RuntimeError as e:
        assert "1700000000" in str(e)


def test_pinned_table_matches_record():
    text = open(REPO_ROOT + "/phase3_5/screening_evidence.md", encoding="utf-8").read()
    block = text[text.index("## EV-C084-PIN-01"):text.index("## EV-C084-E2RULE-01")]
    found = dict((m.group(1), (int(m.group(2)), m.group(3))) for m in
                 re.finditer(r"^(\S+)\s+(\d+) bytes\n\s+([0-9a-f]{64})", block, re.M))
    assert found == PINNED and len(PINNED) == 10


def test_digest_flags_mismatch():
    pinned = {"src/latin1.c": (len(LATIN1), hashlib.sha256(LATIN1).hexdigest()),
              "README.md": (1, "0" * 64)}
    rows = digest(FIX + "/tree", pinned)
    assert [r[0] for r in rows] == ["src/latin1.c", "README.md"]
    assert rows[0][4] is True and rows[1][4] is False


def test_sealed_instant_discards_message():
    fetch = lambda url: (200, {}, open(FIX + "/commits.json", "rb").read())  # noqa: E731
    r = sealed_instant("o/r", "2026-08-26T19:23:05Z", fetch=fetch)
    assert set(r) == {"sha", "author_date", "committer_date"}
    assert "fix" not in json.dumps(r)        # commits.json's message is "fix crash on load"


def test_archive_counts_entries():
    # the test first builds TMP/small.tar.gz with tarfile: 3 members
    with tarfile.open(TMP + "/small.tar.gz", "w:gz") as tf:
        for name in ["a.txt", "b.txt", "c.txt"]:
            p = TMP + "/" + name
            open(p, "wb").write(b"x")
            tf.add(p, arcname="small/" + name)
    n, digest_hex, entries = archive("https://example.invalid/x.tar.gz", TMP + "/a.tgz",
                                     fetch=lambda url: (200, {}, open(TMP + "/small.tar.gz", "rb").read()))
    assert entries == 3 and len(digest_hex) == 64 and n == os.path.getsize(TMP + "/small.tar.gz")


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
