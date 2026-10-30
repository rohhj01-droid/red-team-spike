"""The HTTP side of screening (contract Sections 6 and 7; Run 1's network-access contract):
one request at a time with every attempt recorded, redirects followed and listed,
two recorded retries on transport indeterminacy, link labels read as the page gives
them, the step-2 word rule, and designation signals. No authentication, no caching,
stdlib only.
"""
from __future__ import annotations

import datetime
import re
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

USER_AGENT = "red-team-spike-run2 (python urllib)"
TIMEOUT_S = 60
MAX_REDIRECTS = 10
RETRIES = 2                                   # two recorded retries after the first attempt
STEP2_WORDS = ("source", "code", "repository", "development")
TRANSLATIONS = ("quellcode", "quelltext", "repositorium", "entwicklung",
                "code source", "dépôt", "développement",
                "código", "código fuente", "repositorio", "desarrollo",
                "repositório", "desenvolvimento",
                "codice", "sorgente", "sviluppo",
                "исходный код", "исходники", "репозиторий", "разработка",
                "ソース", "ソースコード", "リポジトリ", "開発",
                "소스", "소스 코드", "저장소", "개발")
DESIGNATION_WORDS = ("official", "canonical", "primary", "main repository", "our repository", "the source", "mirror")
HOST_LABELS = ("github", "gitlab", "codeberg", "bitbucket", "sourceforge", "sr.ht", "savannah")   # RQA-03 (i)


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401 - urllib hook
        return None


def http_get(url: str) -> tuple[int, dict, bytes]:
    """One request, redirects NOT followed (the caller records the chain). Transport failures raise."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT_S) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read() if e.fp else b""


def _header(headers: dict, name: str) -> str:
    for k, v in headers.items():
        if k.lower() == name.lower():
            return str(v)
    return ""


def fetch(url: str, fetch=None, clock=None) -> dict:
    """Observation record for one URL: redirects followed (chain listed), transport indeterminacy
    (exception or 5xx) retried twice at recorded times; outcome ok | definitive | transport."""
    do, now = fetch or http_get, clock or utc_now
    rec = dict(observed_at_utc=now(), requested_url=url, final_url=url, http_status=None, redirect_chain=[],
               body=b"", attempts=[], outcome="transport", content_type="")
    current, hops = url, 0
    while True:
        transport_failures = 0
        while True:
            t = now()
            try:
                status, headers, body = do(current)
            except Exception as ex:  # timeout, DNS, refused, reset: all transport-level
                rec["attempts"].append((t, "transport", current, None))
                transport_failures += 1
                if transport_failures > RETRIES:
                    rec["outcome"], rec["final_url"] = "transport", current
                    rec["error"] = "%s: %s" % (type(ex).__name__, ex)
                    return rec
                continue
            if status >= 500:
                rec["attempts"].append((t, "transport", current, status))
                transport_failures += 1
                if transport_failures > RETRIES:
                    rec["outcome"], rec["final_url"], rec["http_status"] = "transport", current, status
                    return rec
                continue
            rec["attempts"].append((t, "ok" if status < 400 else "definitive", current, status))
            break
        rec["http_status"], rec["final_url"] = status, current
        rec["content_type"] = _header(headers, "Content-Type").split(";")[0].strip().lower()
        if status in (301, 302, 303, 307, 308) and _header(headers, "Location") and hops < MAX_REDIRECTS:
            rec["redirect_chain"].append(current)
            current, hops = urljoin(current, _header(headers, "Location")), hops + 1
            continue
        rec["body"] = body
        rec["outcome"] = "ok" if status < 400 else "definitive"
        return rec


class _Links(HTMLParser):
    def __init__(self, base: str):
        super().__init__()
        self.base, self.links, self._open = base, [], None
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._open = dict(label="", title=a.get("title") or "", aria_label=a.get("aria-label") or "",
                              href=urljoin(self.base, a["href"]))
        if tag in ("p", "li", "div", "h1", "h2", "h3", "br", "tr"):
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "a" and self._open is not None:
            self._open["label"] = " ".join(self._open["label"].split())
            self.links.append(self._open)
            self._open = None

    def handle_data(self, data):
        self.text_parts.append(data)
        if self._open is not None:
            self._open["label"] += data


def links(html: bytes, base_url: str) -> list[dict]:
    p = _Links(base_url)
    p.feed(html.decode("utf-8", errors="replace"))
    return p.links


def text_of(html: bytes) -> str:
    """Visible text of a page, for quote verification and designation search (scripts and styles dropped)."""
    cleaned = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", " ", html.decode("utf-8", errors="replace"))
    p = _Links("")
    p.feed(cleaned)
    text = "".join(p.text_parts)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s or "").casefold()


def _label_has(link: dict, words) -> bool:
    for field in ("label", "title", "aria_label"):
        text = _norm(link.get(field, ""))
        for word in words:
            if re.search(r"(?<!\w)%s(?!\w)" % re.escape(_norm(word)), text):
                return True
    return False


def is_step2(link: dict) -> bool:
    """Whole-word match of a step-2 word or translation on the label, title or aria-label (contract Section 6)."""
    return _label_has(link, STEP2_WORDS + TRANSLATIONS + HOST_LABELS)


def is_word_label(link: dict) -> bool:
    """A step-2 label with one of the four words or a translation, not only a code host's name (RQA-20)."""
    return _label_has(link, STEP2_WORDS + TRANSLATIONS)


def step2_links(links_: list[dict]) -> list[dict]:
    return [l for l in links_ if is_step2(l)]


def designation_signals(text: str) -> list[str]:
    """Sentences carrying a designation word; witnesses, never permissions."""
    out = []
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
        s = sentence.strip()
        if s and any(w in s.casefold() for w in DESIGNATION_WORDS):
            out.append(s)
    return out
