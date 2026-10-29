"""URL normalization (sealed Section 2), the surface-class table (contract Section 5),
the starting-point set (contract Section 4) and the identity key (contract Section 3).
The table is data: one row per (host pattern, path pattern, class), first match wins;
a URL matching no row is `None` -- unmatched -- and screen.py classifies it by one request.
"""
from __future__ import annotations

import re
from urllib.parse import urlsplit

CLASSES = ("repository-root", "release-assets", "distfile-location", "project-page", "repository-file", "tracker-page")
FORBIDDEN = ("release-assets", "tracker-page")      # never requested at E2-REP (sealed contract: releases; issues / PRs / wiki)
CODE_HOST_RE = re.compile(r"^(github\.com|codeberg\.org|bitbucket\.org|salsa\.debian\.org|gitlab\.com|gitlab\..+)$")
IDENTIFYING_CLASSES = ("distfile-location", "project-page")
NON_IDENTIFYING_HOSTS = ("distfiles.openbsd.org", "ftp.openbsd.org", "mirrors.kernel.org", "www.kernel.org",
                         "registry.npmjs.org", "files.pythonhosted.org", "pypi.io", "pypi.org", "crates.io",
                         "static.crates.io", "www.cpan.org", "cpan.org", "cpan.metacpan.org")
TUPLE_HOSTS = {"github": "https://github.com/", "gitlab": "https://gitlab.com/", "codeberg": "https://codeberg.org/"}
ARCHIVE_EXT = r"\.(tar\.gz|tgz|tar\.bz2|tar\.xz|tar\.zst|zip|7z)$"

# (host regex, path regex, class) -- contract Section 5, first match wins
SURFACE_TABLE: list[tuple[str, str, str]] = [
    # release-assets (the only forbidden class)
    (r"^github\.com$", r"^/[^/]+/[^/]+/(releases|archive|tags|downloads)(/|$)", "release-assets"),
    (r"^(gitlab\.com|gitlab\..+)$", r"(/-/(releases|archive|tags)(/|$)|/uploads/)", "release-assets"),
    (r"^codeberg\.org$", r"^/[^/]+/[^/]+/(releases|archive)(/|$)", "release-assets"),
    (r"^bitbucket\.org$", r"^/[^/]+/[^/]+/downloads(/|$)", "release-assets"),
    # tracker-page (forbidden: issues / PRs / wiki / discussions, the sealed contract's own list) -- RQA-02 (g)
    (r"^(github\.com|codeberg\.org|bitbucket\.org)$", r"^/[^/]+/[^/]+/(issues|pulls|pull|discussions|wiki|projects|security|actions)(/|$)", "tracker-page"),
    (r"^(gitlab\.com|gitlab\..+)$", r"/-/(issues|merge_requests|wikis|boards|pipelines)(/|$)", "tracker-page"),
    # repository-file (a file or tree view inside a repository: designates its root, is not itself read) -- RQA-02 (f)
    (r"^(github\.com|codeberg\.org|bitbucket\.org|salsa\.debian\.org)$", r"^/[^/]+/[^/]+/(blob|tree|raw|src|commits?|branch)(/|$)", "repository-file"),
    (r"^(gitlab\.com|gitlab\..+)$", r"/-/(blob|tree|raw|commits?)(/|$)", "repository-file"),
    # repository-root
    (r"^sourceforge\.net$", r"^/p/[^/]+/[^/]+/?$", "repository-root"),                       # Allura code repository (RQA-03 j)
    (r"^sourceforge\.net$", r"^/p/[^/]+/[^/]+/(ci|tree|commit)(/|$)", "repository-file"),
    (r"^(github\.com|codeberg\.org|bitbucket\.org|salsa\.debian\.org)$", r"^/[^/]+/[^/]+/?$", "repository-root"),
    (r"^(gitlab\.com|gitlab\..+)$", r"^(/[^/]+){2,}/?$", "repository-root"),
    (r"^(sr\.ht|git\.sr\.ht)$", r"^/~[^/]+/[^/]+/?$", "repository-root"),
    (r"^(git|code)\..+$", r"^/[^/]+/[^/]+/?$", "repository-root"),
    (r".*", r"\.git/?$", "repository-root"),
    (r".*", r"^/(cgit|git)/[^/]+/?$", "repository-root"),
    # distfile-location
    (r"^(downloads\.sourceforge\.net|prdownloads\.sourceforge\.net|.+\.dl\.sourceforge\.net)$", r".*", "distfile-location"),
    (r"^sourceforge\.net$", r"^/(projects/[^/]+/files|project/[^/]+)(/|$)", "distfile-location"),
    (r"^(ftp\.gnu\.org|ftpmirror\.gnu\.org)$", r"^/gnu/", "distfile-location"),
    (r"^download\.savannah\.(non)?gnu\.org$", r"^/releases/", "distfile-location"),
    (r"^cpan\.metacpan\.org$", r"^/(authors/id|modules/by-module)/", "distfile-location"),
    (r"^(www\.cpan\.org|cpan\.org)$", r".*", "distfile-location"),
    (r"^(distfiles\.openbsd\.org|ftp\.openbsd\.org|.+\.openbsd\.org)$", r"/distfiles/", "distfile-location"),
    (r"^(files\.pythonhosted\.org|pypi\.io|pypi\.org)$", r"^/packages/", "distfile-location"),
    (r"^(crates\.io|static\.crates\.io)$", r"^/(api/v1/crates|crates)/", "distfile-location"),
    (r"^registry\.npmjs\.org$", r".*", "distfile-location"),
    (r"^hackage\.haskell\.org$", r"^/package/", "distfile-location"),
    (r"^(ftp\.debian\.org|deb\.debian\.org)$", r"^/debian/pool/", "distfile-location"),
    (r"^(mirrors\.kernel\.org|www\.kernel\.org)$", r".*", "distfile-location"),
    (r".*", ARCHIVE_EXT, "distfile-location"),
]
_COMPILED = [(re.compile(h), re.compile(p), c) for h, p, c in SURFACE_TABLE]


def normalize_url(url: str) -> str:
    """HTTPS form; scheme and host lowercased; no credentials, query or fragment; no trailing slash; no trailing .git."""
    u = urlsplit(url.strip())
    host = (u.hostname or "").lower()
    if u.port and u.port not in (80, 443):
        host += ":%d" % u.port
    path = u.path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return "https://" + host + path


def classify(url: str) -> str | None:
    u = urlsplit(url.strip())
    host, path = (u.hostname or "").lower(), u.path or "/"
    for h, p, c in _COMPILED:
        if h.match(host) and p.search(path):
            return c
    return None


def repository_root_of(url: str) -> str | None:
    """The repository root a code-host URL belongs to (https://host/<a>/<p>; gitlab: the path before /-/),
    or None for a URL that is not inside a repository on a code host."""
    u = urlsplit(url.strip())
    host = (u.hostname or "").lower()
    path = u.path or "/"
    if host == "sourceforge.net":                                   # RQA-03 (j): /p/<project>/<repo>
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 3 and parts[0] == "p":
            return "https://sourceforge.net/p/%s/%s" % (parts[1], parts[2])
        return None
    if not CODE_HOST_RE.match(host):
        return None
    if host == "gitlab.com" or host.startswith("gitlab."):
        before = path.split("/-/")[0]
        parts = [p for p in before.split("/") if p]
        if len(parts) < 2:
            return None
        return "https://" + host + "/" + "/".join(parts)
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        return None
    root = "https://" + host + "/" + parts[0] + "/" + parts[1]
    return root[:-4] if root.endswith(".git") else root


def git_url_of(root: str) -> str:
    """The URL `git ls-remote` / `git fetch` take for a repository root: the root itself on git hosts, the Allura
    git endpoint for a SourceForge code repository (RQA-03 j)."""
    u = urlsplit(root.strip())
    if (u.hostname or "").lower() == "sourceforge.net":
        parts = [p for p in (u.path or "/").split("/") if p]
        if len(parts) >= 3 and parts[0] == "p":
            return "https://git.code.sf.net/p/%s/%s" % (parts[1], parts[2])
    return root.rstrip("/")


def starting_points(meta: dict) -> list[dict]:
    """Ordered starting points: HOMEPAGE, each SITES URL, the GH root, each DIST_TUPLE root; one surface per
    normalized URL, its sources joined with '+' (contract Section 4)."""
    ordered: list[tuple[str, str]] = []
    if meta.get("homepage"):
        ordered.append((meta["homepage"], "HOMEPAGE"))
    for s in meta.get("sites", []):
        mech = meta.get("sites_mechanism", {}).get(s, "explicit")
        ordered.append((s, "SITES." + mech[6:] if mech.startswith("group:") else "SITES"))
    if meta.get("gh"):
        ordered.append(("https://github.com/%s/%s" % meta["gh"], "GH"))
    for site, a, p, _tag in meta.get("dist_tuples", []):
        if site in TUPLE_HOSTS:
            ordered.append((TUPLE_HOSTS[site] + a + "/" + p, "DIST_TUPLE"))
    out: list[dict] = []
    index: dict[str, int] = {}
    for url, source in ordered:
        key = normalize_url(url)
        if key in index:
            out[index[key]]["source"] += "+" + source
            continue
        index[key] = len(out)
        out.append(dict(url=url, source=source, klass=classify(url)))
    return out


def identity_key(meta: dict, classes: dict[str, str]) -> tuple[str, str]:
    """('PASS', key) | ('FAIL_NONE', '') | ('FAIL_AMBIGUOUS', ''); `classes` supplies classes of unmatched URLs."""
    roots = set()
    if meta.get("gh"):
        roots.add(normalize_url("https://github.com/%s/%s" % meta["gh"]).lower())
    for site, a, p, _tag in meta.get("dist_tuples", []):
        if site in TUPLE_HOSTS:
            roots.add(normalize_url(TUPLE_HOSTS[site] + a + "/" + p).lower())
    if len(roots) > 1:
        return ("FAIL_AMBIGUOUS", "")
    if roots:
        return ("PASS", roots.pop())
    if meta.get("homepage"):
        return ("PASS", normalize_url(meta["homepage"]).lower())
    for s in meta.get("sites", []):
        klass = classify(s) or classes.get(s)
        host = (urlsplit(s).hostname or "").lower()
        if klass in IDENTIFYING_CLASSES and host not in NON_IDENTIFYING_HOSTS:
            first = (urlsplit(s).path or "/").strip("/").split("/")[0]
            return ("PASS", "https://" + host + ("/" + first if first else ""))
    return ("FAIL_NONE", "")
