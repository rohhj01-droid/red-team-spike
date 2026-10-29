"""Known-failure lane reads of the GitHub API (design Sections 5, 8, 11).

    python -I kf_api.py labels <repo>                         label names and descriptions (X8)
    python -I kf_api.py count <repo> [label ...]              size of the KF set, nothing else (X8)
    python -I kf_api.py list <repo> <out.tsv> [label ...]     the KF set's issue numbers (X12 only)
    python -I kf_api.py first-post <repo> <number>            one issue's first post, no comments (X12, KF-1)
    python -I kf_api.py comments <repo> <number>              one issue's comments (X14, KF-3 only)

Every object is passed through `common.strip` before anything else
touches it: `count` keeps only issue numbers and the pull_request
marker; `first-post` keeps number, title, state, created_at, labels and
body; `comments` keeps created_at and body. A 403/429 raises -- no
partial count is ever returned (Review Focus 2).
"""
from __future__ import annotations

import datetime
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import api_get, strip, write_tsv  # noqa: E402

API = "https://api.github.com"
PER_PAGE = 100


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _pages(url: str, fetch=None):
    page = 1
    while True:
        data = api_get("%s&page=%d" % (url, page), fetch=fetch)
        if not data:
            return
        for obj in data:
            yield obj
        if len(data) < PER_PAGE:
            return
        page += 1


def labels(repo: str, fetch=None) -> list[tuple[str, str]]:
    url = "%s/repos/%s/labels?per_page=%d" % (API, repo, PER_PAGE)
    return [(s["name"], s.get("description") or "")
            for s in (strip(o, ("name", "description")) for o in _pages(url, fetch))]


def issue_numbers(repo: str, label: str | None, fetch=None) -> set[int]:
    url = "%s/repos/%s/issues?state=all&per_page=%d" % (API, repo, PER_PAGE)
    if label:
        url += "&labels=" + urllib.parse.quote(label, safe="")
    nums = set()
    for obj in _pages(url, fetch):
        s = strip(obj, ("number", "pull_request"))
        if "pull_request" in s:
            continue
        nums.add(int(s["number"]))
    return nums


def _union(repo: str, label_set: list[str], fetch=None) -> set[int]:
    nums: set[int] = set()
    for label in (label_set or [None]):
        nums |= issue_numbers(repo, label, fetch)
    return nums


def count(repo: str, label_set: list[str], fetch=None) -> int:
    return len(_union(repo, label_set, fetch))


def list_ids(repo: str, label_set: list[str], out_tsv: str, fetch=None) -> int:
    nums = sorted(_union(repo, label_set, fetch))
    write_tsv(out_tsv, [{"number": str(n)} for n in nums], ["number"],
              comment="enumerated %s from %s labels=%s" % (_utc(), repo, ",".join(label_set) or "(all issues)"))
    return len(nums)


def first_post(repo: str, number: int, fetch=None) -> dict:
    obj = api_get("%s/repos/%s/issues/%d" % (API, repo, number), fetch=fetch)
    return strip(obj, ("number", "title", "state", "created_at", "labels", "body"))


def comments(repo: str, number: int, fetch=None) -> list[dict]:
    url = "%s/repos/%s/issues/%d/comments?per_page=%d" % (API, repo, number, PER_PAGE)
    return [strip(o, ("created_at", "body")) for o in _pages(url, fetch)]


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "labels":
        for name, desc in labels(argv[1]):
            print("%s\t%s" % (name, desc))
        return 0
    if len(argv) >= 2 and argv[0] == "count":
        print("count=%d labels=%s at %s" % (count(argv[1], argv[2:]), ",".join(argv[2:]) or "(all issues)", _utc()))
        return 0
    if len(argv) >= 3 and argv[0] == "list":
        n = list_ids(argv[1], argv[3:], argv[2])
        print("ids=%d written to %s at %s" % (n, argv[2], _utc()))
        return 0
    if len(argv) == 3 and argv[0] == "first-post":
        r = first_post(argv[1], int(argv[2]))
        for k in ("number", "title", "state", "created_at", "labels"):
            print("%s: %s" % (k, r[k]))
        print("body:\n%s" % (r["body"] or ""))
        return 0
    if len(argv) == 3 and argv[0] == "comments":
        for c in comments(argv[1], int(argv[2])):
            print("--- %s\n%s" % (c["created_at"], c["body"] or ""))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
