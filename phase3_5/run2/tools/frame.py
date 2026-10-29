"""The frame, re-executed (preregistration design Section 3; contract Section 2):
verify the sealed archive by hash and size, extract only what the screening reads,
enumerate the ports whose CATEGORIES include `games`, cut the screening set at the
sealed budget, and check the result against Run 1's list item by item.

Run (from the repository root):
    python -I phase3_5/run2/tools/frame.py verify <archive>
    python -I phase3_5/run2/tools/frame.py extract <archive> <dest>
    python -I phase3_5/run2/tools/frame.py enumerate <ports_root> <out_all> <out_128> <run1_list>
"""
from __future__ import annotations

import hashlib
import io
import os
import re
import sys
import tarfile

FRAME_URL = "https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz"
SHA256_URL = "https://cdn.openbsd.org/pub/OpenBSD/7.9/SHA256"
FRAME_SHA256 = "937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db"
FRAME_SIZE = 56386078
BUDGET = 128
CATEGORIES_RE = re.compile(r"^CATEGORIES[ \t]*=(.*)$", re.M)      # FRAME_ENUMERATION.md: ^CATEGORIES[[:space:]]*=
WANTED_TAILS = ("/Makefile", "/distinfo", "/pkg/DESCR")


def verify_archive(path: str) -> tuple[bool, str, int]:
    """(match, sha256, size): match iff both the sealed hash and the sealed size."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()
    size = os.path.getsize(path)
    return (sha == FRAME_SHA256 and size == FRAME_SIZE), sha, size


def _wanted(name: str) -> bool:
    n = name[2:] if name.startswith("./") else name
    parts = n.split("/")
    if not parts or parts[0] != "ports" or any(p in ("", "..") for p in parts) or n.startswith("/"):
        return False
    if len(parts) >= 2 and parts[1] == "infrastructure":
        return True
    return n.endswith(WANTED_TAILS)


def extract_selected(archive: str, dest: str) -> int:
    """Extract only port Makefiles, distinfo, pkg/DESCR and infrastructure/**; returns the file count.
    Members with an absolute path or a `..` component are never extracted."""
    count = 0
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(archive, "r:gz") as t:
        for m in t:
            if not _wanted(m.name) or not (m.isfile() or m.isdir()):
                continue
            if hasattr(tarfile, "data_filter"):
                t.extract(m, dest, filter="data")
            else:  # older Python: the name was already screened by _wanted
                t.extract(m, dest)
            if m.isfile():
                count += 1
    return count


def read_text(path: str) -> str:
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def enumerate_games(ports_root: str) -> list[str]:
    """Port directories whose Makefile assigns CATEGORIES with the token `games`, byte-wise ascending."""
    items = set()
    for dirpath, dirnames, filenames in os.walk(ports_root):
        dirnames.sort()
        if "Makefile" not in filenames:
            continue
        rel = os.path.relpath(dirpath, ports_root).replace(os.sep, "/")
        if rel == "." or rel.split("/")[0] == "infrastructure":
            continue
        text = read_text(os.path.join(dirpath, "Makefile"))
        for m in CATEGORIES_RE.finditer(text):
            if "games" in m.group(1).split():
                items.add(rel)
                break
    return sorted(items, key=lambda s: s.encode("utf-8"))


def screening_set(items: list[str], budget: int = BUDGET) -> list[str]:
    return list(items[:budget])


def check_against_run1(items: list[str], run1_file: str) -> list[tuple[int, str, str]]:
    """Differences against Run 1's list as (rank, run1, run2); empty when identical."""
    run1 = [l.strip() for l in io.open(run1_file, encoding="utf-8").read().splitlines() if l.strip()]
    out = []
    for i in range(max(len(run1), len(items))):
        a = run1[i] if i < len(run1) else ""
        b = items[i] if i < len(items) else ""
        if a != b:
            out.append((i + 1, a, b))
    return out


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "verify":
        ok, sha, size = verify_archive(argv[1])
        print("sha256=%s size=%d %s" % (sha, size, "MATCH" if ok else "MISMATCH"))
        return 0 if ok else 1
    if len(argv) == 3 and argv[0] == "extract":
        print("extracted %d files" % extract_selected(argv[1], argv[2]))
        return 0
    if len(argv) == 5 and argv[0] == "enumerate":
        items = enumerate_games(argv[1])
        io.open(argv[2], "w", encoding="utf-8", newline="\n").write("\n".join(items) + "\n")
        s = screening_set(items)
        io.open(argv[3], "w", encoding="utf-8", newline="\n").write("\n".join(s) + "\n")
        diffs = check_against_run1(s, argv[4])
        print("items=%d outside_games=%d screening_set=%d differences=%d" % (
            len(items), sum(1 for i in items if not i.startswith("games/")), len(s), len(diffs)))
        for d in diffs:
            print("  rank %d: run1=%r run2=%r" % d)
        return 0 if not diffs else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
