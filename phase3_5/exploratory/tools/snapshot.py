"""X4a snapshot tool (design Section 4.2).

    python -I snapshot.py digest <tree>            the ten pinned digests
    python -I snapshot.py archive <url> <out>      archive size/sha256/entries vs the pin
    python -I snapshot.py sealed-instant           master's latest commit at the sealed instant

`digest` exits 1 on any mismatch; the study stops there (Section 4.2
step 3). `archive` and `sealed-instant` record MATCH/MISMATCH and
COINCIDES/DIFFERS without failing (steps 4 and 5).
"""
from __future__ import annotations

import os
import sys
import tarfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import api_get, http_fetch, sha256_file  # noqa: E402
import hashlib  # noqa: E402

REVISION = "7775ef82d1e9dfd50eb9d2824acefaeff7247458"
SEALED_INSTANT = "2026-08-26T19:23:05Z"
REPO = "fabiangreffrath/crispy-doom"
ARCHIVE_URL = "https://github.com/%s/archive/%s.tar.gz" % (REPO, REVISION)

# EV-C084-PIN-01, phase3_5/screening_evidence.md: path -> (bytes, sha256).
# test_pinned_table_matches_record compares this table with the record.
PINNED = {
    "README.md": (13111, "583bbc60755242bcb97ade06666f90e1544240d41f4d9739514eb7cc6511d6d0"),
    "src/d_iwad.c": (26304, "1cc2f0575aa23314de779ade8841c92fc619780caa5e9a982229407ddbb60b5e"),
    "src/d_iwad.h": (1745, "6b66d804248617e3955737ace60e07894abc4eae612ac76a298e42da013de615"),
    "src/doom/d_main.c": (65708, "6dd3658604fc1c093562bbb9c2d2e5a92401d81944e3a186745af85396ac17f6"),
    "src/doom/g_game.c": (94495, "09afab2ea0147fcfa6bb58ff99f87e6a47b7e4e8a8a30a36b8f68f7fd4674cb9"),
    "src/doom/m_menu.c": (88348, "79e528eea3b40aa92e2461953aea257b6afa087fbc7936bd5ec96cc291e6a9a7"),
    "src/doom/p_saveg.c": (39855, "391525093535a2e893fa1873cb2a3e833f8ce8e82c6ee9b9c97d78f3b1dc1ae4"),
    "src/heretic/d_main.c": (37580, "f189aef7e934a7a9569a8527374d6f51446adf703571a8746f1d70090bc40e84"),
    "src/hexen/h2_main.c": (38148, "29118382638044d7d5ebb7641a38280eee23e1ae7b99221ab86a3387ea20c610"),
    "src/strife/d_main.c": (63255, "5080ef9009672089b478850c929ac79320d73f909e8967d9c23e87368508da2e"),
}
ARCHIVE_PIN = (2648481, "4edfcde1c4f6f9292d673116f81ba40df6cf04033f17346131b4f2fe72fbce55", 832)


def digest(tree: str, pinned: dict = PINNED) -> list[tuple[str, int, str, str, bool]]:
    rows = []
    for path, (_pin_bytes, pin_sha) in pinned.items():
        full = os.path.join(tree, path)
        if os.path.isfile(full):
            size, sha = os.path.getsize(full), sha256_file(full)
        else:
            size, sha = 0, ""
        rows.append((path, size, sha, pin_sha, sha == pin_sha))
    return rows


def archive(url: str, out_path: str, fetch=None) -> tuple[int, str, int]:
    status, _headers, body = (fetch or http_fetch)(url)
    if status != 200:
        raise RuntimeError("HTTP %d for %s" % (status, url))
    with open(out_path, "wb") as f:
        f.write(body)
    with tarfile.open(out_path, "r:gz") as tf:
        entries = len(tf.getmembers())          # listed, never extracted
    return len(body), hashlib.sha256(body).hexdigest(), entries


def sealed_instant(repo: str, until: str, fetch=None) -> dict:
    url = "https://api.github.com/repos/%s/commits?sha=master&until=%s&per_page=1" % (repo, until)
    data = api_get(url, fetch=fetch)
    first = data[0]
    return {"sha": first["sha"],
            "author_date": first["commit"]["author"]["date"],
            "committer_date": first["commit"]["committer"]["date"]}


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "digest":
        rows = digest(argv[1])
        print("| file | bytes | sha256 | pinned sha256 | match |")
        print("|---|---|---|---|---|")
        for path, size, sha, pin, ok in rows:
            print("| %s | %d | %s | %s | %s |" % (path, size, sha or "(missing)", pin, "True" if ok else "False"))
        print("%d of %d match" % (sum(r[4] for r in rows), len(rows)))
        return 0 if all(r[4] for r in rows) else 1
    if len(argv) >= 3 and argv[0] == "archive":
        size, sha, entries = archive(argv[1], argv[2])
        pin_size, pin_sha, pin_entries = ARCHIVE_PIN
        print("bytes=%d (%s pinned %d) sha256=%s (%s pinned %s) entries=%d (%s pinned %d)" % (
            size, "MATCH" if size == pin_size else "MISMATCH", pin_size,
            sha, "MATCH" if sha == pin_sha else "MISMATCH", pin_sha,
            entries, "MATCH" if entries == pin_entries else "MISMATCH", pin_entries))
        return 0
    if argv and argv[0] == "sealed-instant":
        r = sealed_instant(REPO, SEALED_INSTANT)
        print("sha=%s author_date=%s committer_date=%s -> %s revision %s" % (
            r["sha"], r["author_date"], r["committer_date"],
            "COINCIDES" if r["sha"] == REVISION else "DIFFERS", REVISION))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
