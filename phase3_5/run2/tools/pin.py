"""The observation-time pin (contract Section 10; preregistration design Section 7.3).

At the moment E2-REP passes, the default branch's tip is recorded as a full hash, that
hash is fetched (depth 1, core.autocrlf=false), the host's archive for it is listed and
hashed, and the ten largest source files are digested. Every later step is defined
against that hash. `git` is injectable (a callable taking the argument list and
returning stdout) so that the tests never touch the network.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess

import paths

paths.use_exploratory_tools()
from common import sha256_file  # noqa: E402  (exploratory tool)
from snapshot import archive as _archive  # noqa: E402  (exploratory tool: lists a tarball, never extracts)

SOURCE_EXT = {".c", ".h", ".m", ".py", ".cpp", ".hpp", ".cc", ".rs", ".go", ".js", ".ts", ".java", ".lua"}
TEN = 10


def _git(args: list[str]) -> str:
    return subprocess.run(["git"] + list(args), capture_output=True, text=True, encoding="utf-8", check=True).stdout


def ls_remote(url: str, git=None) -> tuple[str, str]:
    """(default branch, tip sha) from `git ls-remote --symref <url> HEAD`."""
    out = (git or _git)(["ls-remote", "--symref", url, "HEAD"])
    branch, sha = "", ""
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].startswith("ref: ") and parts[1] == "HEAD":
            branch = parts[0][len("ref: "):].split("/", 2)[-1]
        elif len(parts) >= 2 and parts[1] == "HEAD" and not parts[0].startswith("ref:"):
            sha = parts[0]
    if not sha:
        raise RuntimeError("ls-remote gave no HEAD hash for %s" % url)
    return branch, sha


def fetch_by_hash(url: str, sha: str, dest: str, git=None) -> None:
    """init; core.autocrlf=false; fetch --depth 1 origin <sha>; checkout --detach FETCH_HEAD."""
    g = git or _git
    os.makedirs(dest, exist_ok=True)
    g(["init", dest])
    g(["-C", dest, "config", "core.autocrlf", "false"])
    g(["-C", dest, "remote", "add", "origin", url])
    g(["-C", dest, "fetch", "--depth", "1", "origin", sha])
    g(["-C", dest, "checkout", "--detach", "FETCH_HEAD"])


def ten_digests(tree: str) -> list[tuple[str, int, str]]:
    """The ten largest files with a source extension (ties by path), as (relative path, bytes, sha256)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(tree):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in SOURCE_EXT:
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, tree).replace(os.sep, "/")
                found.append((rel, os.path.getsize(p)))
    found.sort(key=lambda t: (-t[1], t[0].encode("utf-8")))
    return [(rel, size, sha256_file(os.path.join(tree, rel))) for rel, size in found[:TEN]]


def archive_pin(url: str, out_path: str, fetch=None) -> tuple[int, str, int]:
    """(bytes, sha256, entries) of the host's archive for the pinned hash, listed and never extracted."""
    return _archive(url, out_path, fetch=fetch)


def tracked_count(tree: str, git=None) -> int:
    out = (git or _git)(["-C", tree, "ls-files"])
    return len([l for l in out.splitlines() if l.strip()])


def write_record(dest_dir: str, record: dict) -> None:
    """pin_record.md (the exploratory pin record's form) and pin.json."""
    os.makedirs(dest_dir, exist_ok=True)
    io.open(os.path.join(dest_dir, "pin.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(record, indent=1, sort_keys=True) + "\n")
    L = ["# Pin record -- Run 2, candidate %s" % record.get("candidate_id", "?"), "",
         "Pinned at OBSERVATION TIME, the moment E2-REP passed (contract Section 10; a declared",
         "deviation from the sealed instant, QA-28 / XQA-01). Every later step for this candidate",
         "is defined against the hash below.", "",
         "```text",
         "observed_at_utc  %s" % record.get("observed_at_utc", ""),
         "location         %s" % record.get("url", ""),
         "default branch   %s" % record.get("branch", ""),
         "tip hash         %s" % record.get("sha", ""),
         "tracked files    %s" % record.get("tracked_files", ""),
         "```", ""]
    a = record.get("archive") or {}
    if a:
        L += ["## Archive (listed, not extracted)", "", "```text",
              "url      %s" % a.get("url", ""), "bytes    %s" % a.get("bytes", ""),
              "sha256   %s" % a.get("sha256", ""), "entries  %s" % a.get("entries", ""), "```", ""]
    L += ["## Ten digests (the ten largest source files; ties by path)", "", "| file | bytes | sha256 |", "|---|---|---|"]
    for rel, size, sha in record.get("digests", []):
        L.append("| %s | %s | %s |" % (rel, size, sha))
    L.append("")
    io.open(os.path.join(dest_dir, "pin_record.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L))


def pin_repository(candidate_id: str, url: str, dest_root: str, archive_url_fmt: str | None = None,
                   git=None, fetch=None, clock=None) -> dict:
    """The whole pin for a repository candidate: ls-remote, fetch by hash, tree digests, archive, record."""
    import net
    branch, sha = ls_remote(url, git=git)
    tree = os.path.join(dest_root, candidate_id, "tree")
    fetch_by_hash(url, sha, tree, git=git)
    rec = dict(candidate_id=candidate_id, url=url, branch=branch, sha=sha,
               observed_at_utc=(clock or net.utc_now)(), digests=ten_digests(tree),
               tracked_files=tracked_count(tree, git=git))
    if archive_url_fmt:
        aurl = archive_url_fmt.format(url=url.rstrip("/"), sha=sha)
        n, h, e = archive_pin(aurl, os.path.join(dest_root, candidate_id, "archive.tar.gz"), fetch=fetch)
        rec["archive"] = dict(url=aurl, bytes=n, sha256=h, entries=e)
    write_record(os.path.join(dest_root, candidate_id), rec)
    return rec
