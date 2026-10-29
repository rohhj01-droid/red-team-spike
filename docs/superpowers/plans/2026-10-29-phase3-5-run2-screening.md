# Phase 3.5 Run 2 -- screening, inventories and selection (R2-R5) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute steps R2-R5 of the sealed Run 2 preregistration -- the screening contract and tools, the frame re-fetched and checked, 128 frame items screened in 16 reviewed batches, every survivor's inventory frozen under the frozen verdict grammar, and one target selected by the sealed ranking -- plus the Run 1 comparison table.

**Architecture:** Everything lives under `phase3_5/run2/`. Committed stdlib-only tools (`tools/`) produce every ledger row, starting-point table, observation record and evidence block mechanically from the frozen ports metadata and recorded HTTP observations; the analyst supplies only quoted, located witnesses in a per-batch witness table, which the tools validate and turn into gate decisions. The exploratory study's tools (`phase3_5/exploratory/tools/`) are imported unchanged for the inventory; a new frozen verdict grammar (`tools/en_verdicts.py`) decides EN verdicts for every survivor alike. The analysis lane (R6-R7) is a second plan, written from the exploratory plan once the target is known.

**Tech Stack:** Python 3.11+ standard library only (`urllib`, `html.parser`, `tarfile`, `hashlib`, `re`, `json`, `subprocess` for git); assert-based tests run with `python -I`; git for pins; no third-party packages, no authentication.

**Spec:** `docs/superpowers/specs/2026-10-29-phase3-5-run2-preregistration-design.md` (sealed `4c7e315`, R0). It applies `docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md` (`401924d`) and reuses `phase3_5/SCREENING_PROTOCOL.md` (Run 1's contract with both amendments).

## Global Constraints

- Frame identity: `ports.tar.gz` SHA256 `937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db`, size `56386078` bytes, verified against the bytes and against `https://cdn.openbsd.org/pub/OpenBSD/7.9/SHA256` before extraction; budget `128`; order ascending UTF-8 byte order of the port directory path (spec 3).
- The screening order and the batch membership are fixed before item 1 is opened: batch k = ranks 8k-7 .. 8k, k = 1..16 (spec 5).
- Every rule in `SCREENING_CONTRACT.md` and every tool is committed before the frame is re-fetched (spec 12, R2 before R3); the exploratory tools are imported from `phase3_5/exploratory/tools/` and never edited (spec 6) -- `test_exploratory_tools_unchanged` guards it.
- HTTP: stdlib `urllib`, User-Agent `red-team-spike-run2 (python urllib)`, no authentication, timeout 60 s, exactly two recorded retries on transport indeterminacy, then `PI-TRANSPORT-INDETERMINATE` (spec 4.6; protocol "Transport failure").
- Forbidden at E2-REP: README prose, any source file, docs, issues, PRs, changelog, releases (protocol); the `release-assets` class is never requested (spec 4.3).
- Gate order and first-fail stop: `UR, E1, E2-REP, E2-RULE, E3, E4`; gate states `PASS | FAIL | UNRESOLVED | NOT_REACHED`; failure codes from the protocol's vocabulary, no `OTHER`; protocol issue codes `NONE | PI-TRANSPORT-INDETERMINATE | PI-UNCLASSIFIED-SHAPE | PI-STARTING-POINTS-CLOSED | PI-UNCLASSIFIABLE-SURFACE | PI-METADATA-UNRESOLVED` (spec 4.5); `evidence_role` values `official-project-page | official-source-location | admitted-starting-point | distfile-location`.
- Step-2 words: `Source`, `Code`, `Repository`, `Development`, whole words after NFKC + casefold, plus the contract's translation table; a designation signal never authorizes navigation (spec 4.4).
- Tie key: `(normalized canonical source-location URL, external target identifier)`, each ascending by UTF-8 bytes; normalization = HTTPS form, scheme and host lowercased, no credentials/query/fragment, no trailing slash, no trailing `.git` (sealed Section 2).
- Snapshot: observation-time pin at the moment E2-REP passes -- default branch tip as a full hash, depth-1 fetch with `core.autocrlf=false`, archive byte count / sha256 / entry count, ten digests = the ten largest files with extensions `.c .h .m .py .cpp .hpp .cc .rs .go .js .ts .java .lua` in path order among ties (spec 7.3); the sealed-instant wording is a declared deviation, recorded once in the contract.
- Verdict grammar: committed in R2, no rule keyed on a project-specific file name or symbol (spec 6); every ADMIT and every EN4 verdict quoted with `file:line`.
- Decision points D1 (after batch 1) and D2 (after screening) and D3 (after selection) are the owner's, recorded in `EXECUTION_QA.md` in the owner's words before the next step; nothing stops by the clock (spec 9).
- Record discipline: nothing deleted; a correction keeps the earlier wording in place, marked; one commit per batch, per survivor, per step; the SHA reported; review before the next step (spec 12). Commit messages end with the attribution line used throughout this repository.
- Costs are logged with their conditions: the analyst is an AI model operating the tools; session time = first read of a batch's items to the batch commit; review time = commit to the owner's 통과 (spec 5).

## Review Focus

1. A `SITES` line using a macro with the `:=` modifier (`${SITE_SOURCEFORGE:=foo/}`) or several `SITES.<group>` lines: the resolver must expand from the frozen macro table or declare the item `PI-METADATA-UNRESOLVED`, never emit a URL with `${` in it. Pinned in Task 3's `test_sites_macro_expansion` and `test_unknown_macro_is_unresolved`.
2. A HOMEPAGE that redirects to another host or to a forbidden class: the observation records the chain, the final URL's class decides what may be read, a forbidden final class is `closed by class` after the one request that revealed it, and identity uses the final URL. Pinned in Task 5's `test_redirect_chain_recorded` and Task 8's `test_redirect_into_forbidden_class_closes`.
3. A link label where a step-2 word is a substring of another word (`Barcode`, `Codex`, `Developments`): whole-word matching after NFKC casefold, so `Barcode` does not authorize and `Source code` does. Pinned in Task 5's `test_step2_whole_word_only`.
4. A dead repository (definitive 404) versus a timeout: the first is evidence about that endpoint and the other starting points are still followed; the second becomes `PI-TRANSPORT-INDETERMINATE` after two recorded retries. Pinned in Task 5's `test_transport_retries_then_pi` and Task 8's `test_404_does_not_fail_candidate_alone`.
5. Two frame items resolving to one upstream (`games/foo` and `games/foo-data`, or an identity key equal after normalization): the second is `DUPLICATE` with `duplicate_of`, consumes its budget slot, and the candidate ledger has one row. Pinned in Task 8's `test_duplicate_upstream_one_candidate`.

---

## File structure

```text
phase3_5/run2/
  SCREENING_CONTRACT.md          Run 2's contract: spec 4 + identity key + per-gate surfaces + translation
                                 table + schemas + vocabularies + pin rule + the snapshot deviation + cost
                                 conditions (Task 1, docs-only)
  EXECUTION_QA.md                RQA-01 .. (Task 1 creates the header and template)
  frame_enumeration.md           R3 record (Task 9)
  raw_frame_all.txt, screening_set_128.txt   Run 2's own copies (Task 9)
  screening_frame_items.tsv      128 rows, Run 1 schema + starting_points_ref, pin_ref (Task 8 writer; Task 10 fills)
  screening_candidates.tsv       Run 1 schema + decided_by_grammar, class_sensitivity_ref (Task 8; Tasks 10-11)
  starting_points.tsv            one row per (rank, url): class, action, observed_at, status, final_url, evidence_role
  observations.tsv               one row per HTTP request: observed_at_utc, requested_url, final_url, http_status,
                                 redirect_chain, attempt, outcome
  exposure_log.md                incidental content seen at E2-REP, per item
  screening_cost.tsv             batch, rank, gate_reached, session_s, review_s, conditions
  witness_bNN.tsv                the analyst's quoted witnesses per batch (input to screen.py)
  screening_evidence_bNN.md      batch review document: the eight rows and their evidence blocks
  inventory/<cid>/               pin_record.md, inventory_sources.tsv, inventory_enumerators.tsv (grammar
                                 verdicts), quoted_verdicts.tsv (analyst input), class_sensitivity.md,
                                 observations.tsv, P_raw.tsv (universe, for the class and for the lane)
  selection.md                   every survivor with class, tie key and the selected target (Task 11)
  run1_vs_run2.tsv               the comparison (Task 12)
  target/                        git-ignored: ports/ (extracted selectively), <cid>/ pinned trees and archives
  tools/
    paths.py        EXPLORATORY_TOOLS, RUN2, TARGET constants; sys.path insertion for the exploratory tools
    frame.py        archive fetch/verify, selective extraction, CATEGORIES enumeration, screening set, check
    metadata.py     frozen-metadata resolver (explicit lines, GH_* and DIST_TUPLE mechanisms, SITE_ macros)
    surfaces.py     normalize_url, classify (the surface-class table), starting_points, identity_key
    net.py          fetch with recorded retries, links (label, href, title/aria-label), step2_links
    en_verdicts.py  the frozen verdict grammar: catalogue, decide, apply_quoted, class_of, sensitivity
    pin.py          ls_remote, pin_tree (depth-1 by hash, archive, ten digests), pin record
    screen.py       per-item orchestration from metadata to gate decisions; batch documents; cost rows
    ledger.py       TSV schemas, writers, batch review document, contract-conformance checks
    compare.py      run1_vs_run2.tsv
    test_tools.py   assert-based tests; fixtures/ (fake ports tree, canned HTML and HTTP sequences, a C tree)
```

Tasks 1-8 are R2 (committed before the frame is re-fetched). Task 9 is R3. Task 10 is R4. Task 11 is R5. Task 12 is the comparison and the hand-off to the lane plan.

---

### Task 1: `SCREENING_CONTRACT.md` and `EXECUTION_QA.md` (docs-only, R2 begins)

**Files:**
- Create: `phase3_5/run2/SCREENING_CONTRACT.md`, `phase3_5/run2/EXECUTION_QA.md`, `phase3_5/run2/.gitignore` (`target/`)

**Interfaces:**
- Produces: the contract every later task implements; its tables are the source of `surfaces.py`'s `SURFACE_TABLE`, `net.py`'s `STEP2_WORDS` and `TRANSLATIONS`, `metadata.py`'s `DECLARED_MODULES`, `screen.py`'s per-gate surface lists, `ledger.py`'s schemas and vocabularies.

- [ ] **Step 1: Write the contract.** Sections, in order, each copied or derived from the spec section named:
  1. Status and lineage: Run 2 contract, reuses `phase3_5/SCREENING_PROTOCOL.md` with both amendments; what it adds; nothing here changes the sealed methodology.
  2. Frozen metadata and its resolution (spec 4.1): fields read (`HOMEPAGE`, `SITES`, `SITES.<group>`, `GH_ACCOUNT`, `GH_PROJECT`, `GH_TAGNAME`, `GH_COMMIT`, `DIST_TUPLE`, `MODULES`, `DISTNAME`, `COMMENT`, `CATEGORIES`, `pkg/DESCR`); mechanisms, with the QA-39/40 lines quoted: `HOMEPAGE ?= https://github.com/${GH_ACCOUNT}/${GH_PROJECT}` (bsd.port.mk), `SITES ?= ${SITES_GITHUB}` with `https://github.com/<a>/<p>/archive/refs/tags/<tag>/` (GH_TAGNAME) or `.../archive/` (GH_COMMIT); DIST_TUPLE: `TEMPLATE_HOMEPAGE = <site><account>/<project>`, `SITES.github = https://github.com/`, bare `SITES` empty; `SITE_*` macros expanded from the frozen `infrastructure/templates/network.conf.template`; `${VAR:=suffix}` expands to each word with the suffix appended; `DECLARED_MODULES = []` (no module beyond bsd.port.mk and dist-tuple is resolved; `MODULES` naming anything -> `PI-METADATA-UNRESOLVED` at UR).
  3. Upstream resolution and identity (analyst's call, recorded here): `identity_key` = the normalized repository root from `GH_ACCOUNT/GH_PROJECT` or a `DIST_TUPLE` whose site is github/gitlab/codeberg, else the normalized `HOMEPAGE`, else the normalized `SITES` URL's `https://<host>/<first path component>` when its class is `distfile-location` or `project-page`; `FAIL_NONE` when no key exists; `FAIL_AMBIGUOUS` when two repository roots name different `(host, account, project)`; `DUPLICATE` when the key equals an earlier item's key.
  4. Starting points (spec 4.2): the resolved `HOMEPAGE`, each resolved `SITES` / `SITES.<group>` URL, the repository root denoted by the GH pair or DIST_TUPLE; reading B stated.
  5. The surface-class table (spec 4.3), as the literal rows `surfaces.py` will carry (host pattern, path pattern, class), the one-request classification of unmatched URLs, and `release-assets` as the only forbidden class.
  6. Step-2 authorization and designation (spec 4.4): the four words, whole-word after NFKC casefold; the translation table (German `Quellcode`, `Quelltext`, `Code`, `Repositorium`; French `source`, `code source`, `dépôt`, `développement`; Spanish `código`, `código fuente`, `repositorio`, `desarrollo`; Portuguese `código`, `repositório`; Italian `codice`, `sorgente`, `repository`; Russian `исходный код`, `исходники`, `репозиторий`, `разработка`; Japanese `ソース`, `ソースコード`, `リポジトリ`, `開発`; Korean `소스`, `소스 코드`, `저장소`, `개발`); designation signals (`official`, `canonical`, `primary`, `main repository`, `our repository`, `mirror`) are witnesses, never permissions; the repository fields that designate.
  7. How E2-REP completes (spec 4.5): the accounting states `observed | closed-by-class | unclassifiable | unreachable`, the PASS conditions, the three new PI codes, the two new `evidence_role` values.
  8. Per-gate surface lists past E2-REP (analyst's call): E2-RULE reads, in this order and only these: `README*`, `docs/**/*.md|.rst|.txt` index pages (`index`, `README`, files named `rules`, `manual`, `spec`, `format`), `man/**`, `CONTRIBUTING*`, `HACKING*`, and the names (not contents) of `test*/` directories; E3 reads the E2-RULE surfaces plus the source files the E2-RULE witness names; E4 reads the candidate rows `inventory.enumerators` produces and, for the quoted ADMIT, the enumerator's defining lines and its consulting path; the firewall sentence from sealed Section 2.
  9. Schemas: Run 1's two ledgers plus the new columns; `starting_points.tsv`, `observations.tsv`, `screening_cost.tsv`, `witness_bNN.tsv` (`rank, candidate_id, gate, kind, surface, location, quote`; `kind` in `designation | identifier | source-tree | validity | stateful | enumerator | refusal-path | absence-survey`); vocabularies.
  10. The snapshot rule as executed (spec 7.3) and the declared deviation from the sealed instant, with QA-28 and XQA-01 cited once.
  11. Batches and review (spec 5): batch k = ranks 8k-7..8k; one commit per batch; a review failure corrects one item in its own commit with Run 1's retraction convention.
  12. Cost conditions (spec 5) and the decision points D1-D3 with their inputs (spec 9).
- [ ] **Step 2: Write `EXECUTION_QA.md`** with the exploratory log's header and entry template, numbered `RQA-NN`.
- [ ] **Step 3: Verify** `git diff --stat` shows only the three new files. Expected: three files, no tool code.
- [ ] **Step 4: Commit**

```bash
git add phase3_5/run2/SCREENING_CONTRACT.md phase3_5/run2/EXECUTION_QA.md phase3_5/run2/.gitignore
git commit -m "Run 2 R2: screening contract and RQA log, before any tool or frame fetch"
```

---

### Task 2: `paths.py`, `frame.py` -- archive verification, selective extraction, enumeration, check

**Files:**
- Create: `phase3_5/run2/tools/paths.py`, `phase3_5/run2/tools/frame.py`, `phase3_5/run2/tools/test_tools.py`, `phase3_5/run2/tools/fixtures/ports/` (a fake ports tree: `games/alpha/Makefile` with `CATEGORIES = games`, `devel/beta/Makefile` with `CATEGORIES = devel games`, `x11/gamma/Makefile` with `CATEGORIES = x11 games-extra` (not a member), `games/delta/sub/Makefile` depth 3 with `CATEGORIES = games`, `games/parent/Makefile` without CATEGORIES, plus `infrastructure/templates/network.conf.template` with `SITE_SOURCEFORGE = https://downloads.sourceforge.net/sourceforge/` and `SITE_GNU = https://ftp.gnu.org/gnu/`)

**Interfaces:**
- Produces: `paths.EXPLORATORY_TOOLS: str`, `paths.RUN2: str`, `paths.TARGET: str`, and `paths.use_exploratory_tools() -> None` (inserts `EXPLORATORY_TOOLS` into `sys.path`); `frame.FRAME_SHA256 = "937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db"`, `frame.FRAME_SIZE = 56386078`, `frame.BUDGET = 128`; `frame.verify_archive(path: str) -> tuple[bool, str, int]` (match, sha256, size); `frame.extract_selected(archive: str, dest: str) -> int` (members matching `ports/**/Makefile`, `ports/**/distinfo`, `ports/**/pkg/DESCR`, `ports/infrastructure/**`, extracted with `filter="data"`; returns the count); `frame.enumerate_games(ports_root: str) -> list[str]` (CATEGORIES token `games`, byte-wise sorted unique port paths); `frame.screening_set(items: list[str], budget: int = BUDGET) -> list[str]`; `frame.check_against_run1(items: list[str], run1_file: str) -> list[tuple[int, str, str]]` (differences as (rank, run1, run2), empty when equal).

- [ ] **Step 1: Write the failing tests** in `test_tools.py` (runner copied from the exploratory suite):

```python
def test_exploratory_tools_unchanged():
    r = subprocess.run(["git", "diff", "--quiet", "35255d6", "--", "phase3_5/exploratory/tools"], cwd=REPO_ROOT)
    assert r.returncode == 0

def test_enumerate_games_tokens():                 # Review Focus: token, not substring
    items = frame.enumerate_games(FIX + "/ports")
    assert items == ["devel/beta", "games/alpha", "games/delta/sub"]

def test_screening_set_budget():
    assert frame.screening_set(["b", "a", "c"], budget=2) == ["b", "a"]      # order preserved, cut at budget

def test_check_against_run1_reports_differences():
    tmp = os.path.join(TMP, "set.txt"); open(tmp, "w").write("games/alpha\ngames/zeta\n")
    assert frame.check_against_run1(["games/alpha", "games/beta"], tmp) == [(2, "games/zeta", "games/beta")]

def test_verify_archive_mismatch():
    p = os.path.join(TMP, "x.tar.gz"); open(p, "wb").write(b"not the frame")
    ok, sha, size = frame.verify_archive(p)
    assert not ok and size == 13 and len(sha) == 64
```

- [ ] **Step 2: Run** `python -I phase3_5/run2/tools/test_tools.py`. Expected: FAIL, `frame` not importable.
- [ ] **Step 3: Implement** `paths.py` and `frame.py` with the signatures above; `enumerate_games` parses only lines matching `^CATEGORIES[ \t]*=` (single-line, per FRAME_ENUMERATION) and splits on whitespace; `extract_selected` refuses members with `..` or absolute paths even before the filter.
- [ ] **Step 4: Run** the suite. Expected: `5 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: frame tools (verify, selective extraction, enumeration, Run 1 check)"`.

---

### Task 3: `metadata.py` -- the frozen-metadata resolver

**Files:**
- Create: `phase3_5/run2/tools/metadata.py`; fixtures: `fixtures/ports/games/alpha/Makefile` (explicit `HOMEPAGE = https://alpha.example.org/` and `SITES = ${SITE_SOURCEFORGE:=alpha/}`), `games/beta/Makefile` (`GH_ACCOUNT = acme`, `GH_PROJECT = Beta`, `GH_TAGNAME = v1.2`), `games/gamma/Makefile` (`DIST_TUPLE = github acme gamma 1.0 .`), `games/delta/Makefile` (`MODULES = cpan`), `games/eps/Makefile` (`SITES = ${SITE_NOWHERE:=eps/}`), each with `pkg/DESCR` and `distinfo`.

**Interfaces:**
- Consumes: `paths.TARGET`.
- Produces: `metadata.resolve(port_dir: str, infra_root: str) -> dict` with keys `homepage: str | None`, `homepage_mechanism: "explicit" | "gh" | "dist-tuple" | None`, `sites: list[str]`, `sites_mechanism: dict[str, str]` (url -> `"explicit" | "gh-tagname" | "gh-commit" | "group:<name>"`), `gh: tuple[str, str] | None`, `dist_tuples: list[tuple[str, str, str, str]]` (site, account, project, tag), `modules: list[str]`, `distname: str | None`, `comment: str | None`, `descr: str`, `issue: str | None` (`"PI-METADATA-UNRESOLVED"` when a `${...}` cannot be expanded or `modules` is non-empty); `metadata.expand(value: str, macros: dict[str, str]) -> str` (handles `${NAME}` and `${NAME:=suffix}`); `metadata.macro_table(infra_root: str) -> dict[str, str]` (from `templates/network.conf.template`, `SITE_* = ...` lines).

- [ ] **Step 1: Write the failing tests**

```python
def test_explicit_homepage_and_sites_macro_expansion():          # Review Focus 1
    m = metadata.resolve(FIX + "/ports/games/alpha", FIX + "/ports/infrastructure")
    assert m["homepage"] == "https://alpha.example.org/" and m["homepage_mechanism"] == "explicit"
    assert m["sites"] == ["https://downloads.sourceforge.net/sourceforge/alpha/"] and m["issue"] is None

def test_gh_defaults_homepage_and_sites():
    m = metadata.resolve(FIX + "/ports/games/beta", FIX + "/ports/infrastructure")
    assert m["homepage"] == "https://github.com/acme/Beta" and m["homepage_mechanism"] == "gh"
    assert m["sites"] == ["https://github.com/acme/Beta/archive/refs/tags/v1.2/"]
    assert m["sites_mechanism"][m["sites"][0]] == "gh-tagname"

def test_dist_tuple_homepage_and_empty_bare_sites():
    m = metadata.resolve(FIX + "/ports/games/gamma", FIX + "/ports/infrastructure")
    assert m["homepage"] == "https://github.com/acme/gamma" and m["homepage_mechanism"] == "dist-tuple"
    assert m["sites"] == [] and m["dist_tuples"] == [("github", "acme", "gamma", "1.0")]

def test_module_is_unresolved():
    assert metadata.resolve(FIX + "/ports/games/delta", FIX + "/ports/infrastructure")["issue"] == "PI-METADATA-UNRESOLVED"

def test_unknown_macro_is_unresolved():                         # Review Focus 1
    m = metadata.resolve(FIX + "/ports/games/eps", FIX + "/ports/infrastructure")
    assert m["issue"] == "PI-METADATA-UNRESOLVED" and all("${" not in s for s in m["sites"])
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `metadata` not importable.
- [ ] **Step 3: Implement** `metadata.py`: read the Makefile, parse `NAME = value` / `NAME ?= value` / `NAME += value` lines (single-line; a trailing `\` continuation joined), apply the mechanisms of the contract Section 2 in the order explicit > gh > dist-tuple; expansion failures set `issue`.
- [ ] **Step 4: Run** the suite. Expected: `10 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: frozen-metadata resolver (explicit, GH_*, DIST_TUPLE, SITE_ macros)"`.

---

### Task 4: `surfaces.py` -- normalization, the surface-class table, starting points, identity

**Files:**
- Create: `phase3_5/run2/tools/surfaces.py`

**Interfaces:**
- Consumes: `metadata.resolve` output.
- Produces: `surfaces.normalize_url(url: str) -> str`; `surfaces.SURFACE_TABLE: list[tuple[str, str, str]]` (host regex, path regex, class) with classes `repository-root | project-page | release-assets | distfile-location`; `surfaces.classify(url: str) -> str | None` (None = no row matched); `surfaces.starting_points(meta: dict) -> list[dict]` (`url`, `source` in `HOMEPAGE | SITES | SITES.<group> | GH | DIST_TUPLE`, `klass`); `surfaces.identity_key(meta: dict, classes: dict[str, str]) -> tuple[str, str]` (`("PASS", key)` or `("FAIL_NONE", "")` or `("FAIL_AMBIGUOUS", "")`).

- [ ] **Step 1: Write the failing tests**

```python
def test_normalize_url():
    assert surfaces.normalize_url("HTTP://GitHub.com/Acme/Beta.git/?x=1#f") == "https://github.com/Acme/Beta"
    assert surfaces.normalize_url("https://user:pw@example.org/p/") == "https://example.org/p"

def test_classify_table():
    assert surfaces.classify("https://github.com/acme/beta") == "repository-root"
    assert surfaces.classify("https://github.com/acme/beta/releases/download/v1/x.tgz") == "release-assets"
    assert surfaces.classify("https://github.com/acme/beta/archive/refs/tags/v1.2/") == "release-assets"
    assert surfaces.classify("https://downloads.sourceforge.net/sourceforge/alpha/") == "distfile-location"
    assert surfaces.classify("https://sourceforge.net/projects/alpha/files/") == "distfile-location"
    assert surfaces.classify("https://ftp.gnu.org/gnu/alpha/") == "distfile-location"
    assert surfaces.classify("https://alpha.example.org/") is None          # unmatched: one request decides (Task 8)

def test_starting_points_from_gh_port():
    sp = surfaces.starting_points(metadata.resolve(FIX + "/ports/games/beta", FIX + "/ports/infrastructure"))
    assert [(s["url"], s["source"], s["klass"]) for s in sp] == [
        ("https://github.com/acme/Beta", "HOMEPAGE", "repository-root"),
        ("https://github.com/acme/Beta/archive/refs/tags/v1.2/", "SITES", "release-assets"),
        ("https://github.com/acme/Beta", "GH", "repository-root")]

def test_identity_key_and_ambiguity():
    m = metadata.resolve(FIX + "/ports/games/beta", FIX + "/ports/infrastructure")
    assert surfaces.identity_key(m, {}) == ("PASS", "https://github.com/acme/beta")
    m2 = dict(m, dist_tuples=[("github", "other", "thing", "1")])
    assert surfaces.identity_key(m2, {})[0] == "FAIL_AMBIGUOUS"
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `surfaces` not importable.
- [ ] **Step 3: Implement** `surfaces.py` with `SURFACE_TABLE` as the contract's Section 5 rows (github/gitlab/codeberg/sr.ht/bitbucket roots and their release, tag, archive and download paths; sourceforge project files and mirror hosts; GNU, Savannah, CPAN by-author, OpenBSD distfiles); the identity key lowercases the whole URL for comparison only.
- [ ] **Step 4: Run** the suite. Expected: `14 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: URL normalization, surface-class table, starting points, identity key"`.

---

### Task 5: `net.py` -- fetch with recorded retries, links, step-2 authorization

**Files:**
- Create: `phase3_5/run2/tools/net.py`; fixtures: `fixtures/html/project.html` (links: `<a href="/download">Download</a>`, `<a href="https://github.com/acme/beta">Source code</a>`, `<a href="/barcode">Barcode tools</a>`, `<a href="/dev" title="Development">Hack on it</a>`, a sentence "Our official repository is on GitHub" with no link), `fixtures/html/repo.html` (a repository landing page with a description meta tag and a README rendering)

**Interfaces:**
- Produces: `net.USER_AGENT = "red-team-spike-run2 (python urllib)"`; `net.fetch(url: str, fetch=None, clock=None) -> dict` with keys `observed_at_utc, requested_url, final_url, http_status (int | None), redirect_chain (list[str]), body (bytes), attempts (list[tuple[str, str]])` (observed_at, outcome in `ok | http | transport`), `outcome` in `ok | definitive | transport` -- a transport failure is retried twice (three attempts in all) and `outcome == "transport"` only after the third; `net.links(html: bytes, base_url: str) -> list[dict]` (`label` = anchor text, `title`, `aria_label`, `href` resolved absolute); `net.STEP2_WORDS`, `net.TRANSLATIONS`; `net.is_step2(link: dict) -> bool` (whole-word match on label, title or aria-label after NFKC casefold); `net.step2_links(links: list[dict]) -> list[dict]`; `net.designation_signals(text: str) -> list[str]` (sentences containing `official | canonical | primary | main repository | our repository | mirror`).

- [ ] **Step 1: Write the failing tests** (a canned `fetch` callable in the test returns `(status, headers, body)` sequences; a canned `clock` returns fixed timestamps):

```python
def test_redirect_chain_recorded():                             # Review Focus 2
    seq = [(301, {"Location": "https://new.example.org/"}, b""), (200, {}, b"<html></html>")]
    r = net.fetch("http://old.example.org/", fetch=canned(seq), clock=fixed_clock)
    assert r["final_url"] == "https://new.example.org/" and r["redirect_chain"] == ["http://old.example.org/"] and r["http_status"] == 200

def test_transport_retries_then_pi():                           # Review Focus 4
    r = net.fetch("https://x.example.org/", fetch=canned([TIMEOUT, TIMEOUT, TIMEOUT]), clock=fixed_clock)
    assert r["outcome"] == "transport" and [a[1] for a in r["attempts"]] == ["transport"] * 3

def test_definitive_404_is_not_transport():
    r = net.fetch("https://x.example.org/", fetch=canned([(404, {}, b"")]), clock=fixed_clock)
    assert r["outcome"] == "definitive" and r["http_status"] == 404 and len(r["attempts"]) == 1

def test_step2_whole_word_only():                               # Review Focus 3
    ls = net.links(open(FIX + "/html/project.html", "rb").read(), "https://alpha.example.org/")
    assert [l["href"] for l in net.step2_links(ls)] == ["https://github.com/acme/beta", "https://alpha.example.org/dev"]

def test_designation_is_not_permission():
    ls = net.links(open(FIX + "/html/project.html", "rb").read(), "https://alpha.example.org/")
    assert all("official" not in l["label"].lower() for l in net.step2_links(ls))
    assert net.designation_signals("Our official repository is on GitHub. Have fun.") == ["Our official repository is on GitHub."]
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `net` not importable.
- [ ] **Step 3: Implement** `net.py`: `urllib.request` with a `HTTPRedirectHandler` subclass that records the chain; `html.parser.HTMLParser` collecting `<a>` text, `title`, `aria-label`; whole-word matching with `re.search(r"(?<!\w)%s(?!\w)" % re.escape(word), text)` on the NFKC-casefolded label; `TRANSLATIONS` from the contract's Section 6.
- [ ] **Step 4: Run** the suite. Expected: `19 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: HTTP client with recorded retries, link labels, step-2 rule, designation signals"`.

---

### Task 6: `en_verdicts.py` -- the frozen verdict grammar

**Files:**
- Create: `phase3_5/run2/tools/en_verdicts.py`; fixtures: `fixtures/ctree/` (a small C tree: `src/modes.c` with `static const struct { const char *name; int n; } valid_modes[] = {...}` consulted by a loop that errors on a miss; `src/strings.c` with `const char *menu_labels[] = {...}`; `src/tables.c` with `static const int sine_table[] = {...}` and `static void (*dispatch[])(void) = {...}`; `test/data.c` with an array; `src/dead.c` with an array inside `#if 0`), reused from the exploratory fixtures where they fit.

**Interfaces:**
- Consumes: `inventory.enumerators(tree) -> list[dict]` (rows with `cand_id, file, line, symbol, class, element_type, members, absent, conditional`) and `inventory.EN_FIELDS` from the exploratory tools (`paths.use_exploratory_tools()`).
- Produces: `en_verdicts.Rule` (fields `name: str`, `kind: "element_type" | "vocabulary" | "file_role" | "candidate_class" | "dead_code"`, `test: Callable[[dict], bool]`, `en: str` (`"EN2"` or `"EN4"`), `reason: str`); `en_verdicts.CATALOGUE: list[Rule]`; `en_verdicts.decide(row: dict) -> dict` (returns the row with `en1..en6`, `tag`, `reject_reason`, `decided_by` = `"catalogue:<name>"` or `"UNDECIDED"`); `en_verdicts.apply_quoted(rows: list[dict], quoted: list[dict]) -> list[dict]` (quoted rows carry `cand_id, verdict (ADMIT | REJECT-EN2 | REJECT-EN4), tag (enforced | asserted | ""), evidence` with a `file:line`; an ADMIT or EN4 verdict without a citation raises `ValueError`); `en_verdicts.class_of(rows: list[dict]) -> str` (`"A"` iff at least one ADMIT and every ADMIT tagged `enforced`, else `"B"`); `en_verdicts.sensitivity(rows: list[dict]) -> list[dict]` (the admitted rows; rows with `en2 == PASS` and `en4 == FAIL`; rows whose `decided_by` is not `catalogue:*`); `en_verdicts.RULE_KINDS_FORBIDDEN = {"file_name", "symbol_exact"}`.

- [ ] **Step 1: Write the failing tests**

```python
def test_catalogue_has_no_project_specific_rule():
    assert all(r.kind not in en_verdicts.RULE_KINDS_FORBIDDEN for r in en_verdicts.CATALOGUE)
    assert all(not re.search(r"\.(c|h|m)\b", r.name) for r in en_verdicts.CATALOGUE)   # no file names in rule names

def test_decide_by_catalogue_and_undecided():
    rows = inventory.enumerators(FIX + "/ctree")
    d = {r["symbol"]: en_verdicts.decide(r) for r in rows}
    assert d["sine_table"]["decided_by"] == "catalogue:numeric-data" and d["sine_table"]["en2"] == "FAIL"
    assert d["dispatch"]["decided_by"] == "catalogue:dispatch-table"
    assert d["menu_labels"]["decided_by"] == "catalogue:presentation-vocabulary"
    assert d["valid_modes"]["decided_by"] == "UNDECIDED"                       # acceptance vocabulary: quotation needed
    assert any(v["decided_by"] == "catalogue:test-fixture" for v in d.values())
    assert any(v["decided_by"] == "catalogue:dead-code" for v in d.values())

def test_apply_quoted_requires_citation_for_admit():
    rows = [en_verdicts.decide(r) for r in inventory.enumerators(FIX + "/ctree")]
    try:
        en_verdicts.apply_quoted(rows, [dict(cand_id=cid_of(rows, "valid_modes"), verdict="ADMIT", tag="enforced", evidence="no citation")])
        assert False
    except ValueError:
        pass
    out = en_verdicts.apply_quoted(rows, [dict(cand_id=cid_of(rows, "valid_modes"), verdict="ADMIT", tag="enforced", evidence="EN2: src/modes.c:12 'valid modes'; EN4: src/modes.c:30 miss -> I_Error")])
    assert [r for r in out if r["symbol"] == "valid_modes"][0]["tag"] == "enforced"

def test_class_and_sensitivity():
    rows = quoted_fixture_rows()                                               # helper: the rows after apply_quoted above
    assert en_verdicts.class_of(rows) == "A"
    rows2 = [dict(r, tag="asserted") if r["symbol"] == "valid_modes" else r for r in rows]
    assert en_verdicts.class_of(rows2) == "B"
    s = en_verdicts.sensitivity(rows)
    assert any(r["symbol"] == "valid_modes" for r in s) and all(r["decided_by"] != "catalogue:numeric-data" for r in s)
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `en_verdicts` not importable.
- [ ] **Step 3: Implement** the catalogue, in this order (first match decides): `dead-code` (row `conditional` marks `#if 0`, or the candidate's line is inside a block comment -- from `inventory`'s `absent`/`conditional` fields), `test-fixture` (file under `test/`, `tests/`, `fixtures/`, `examples/`, `samples/`, `doc/`, `docs/`), `generated-code` (file name ends `.gen.c` or the file's first 3 lines contain `generated`), `build-system` (`CMakeLists.txt`, `*.mk`, `configure*`), `dispatch-table` (K2, or a struct element whose struct has a function-pointer member), `numeric-data` (element type in a declared numeric set: `int`, `unsigned`, `short`, `long`, `float`, `double`, `fixed_t`, `byte`, `uint8_t` .. `int64_t`, `angle_t`, `char` with no `*`), `presentation-vocabulary` (string element type and the symbol matches `label|msg|message|text|title|desc|name|string|str|hint|tip|menu|caption|help|lang|loc`), `mapping-vocabulary` (symbol matches `map|lookup|table|xlat|translate|convert|rename|alias`) -- any other row is `UNDECIDED`. EN1, EN3, EN5, EN6 are `PASS` for K1-K3 rows (compiled-in arrays) and `UNDECIDED` for K4.
- [ ] **Step 4: Run** the suite. Expected: `23 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: frozen EN verdict grammar (catalogue, quoted verdicts, class, sensitivity)"`.

---

### Task 7: `pin.py` -- observation-time pin

**Files:**
- Create: `phase3_5/run2/tools/pin.py`; fixture: a tiny local git repository built by the test in `TMP` (two commits, a default branch, files of different sizes with the listed extensions)

**Interfaces:**
- Consumes: `common.sha256_file`, `common.walk_tree` (exploratory tools).
- Produces: `pin.SOURCE_EXT = {".c", ".h", ".m", ".py", ".cpp", ".hpp", ".cc", ".rs", ".go", ".js", ".ts", ".java", ".lua"}`; `pin.ls_remote(url: str, git=None) -> tuple[str, str]` (default branch, tip sha, via `git ls-remote --symref <url> HEAD`); `pin.fetch_by_hash(url: str, sha: str, dest: str, git=None) -> None` (init, `core.autocrlf=false`, `fetch --depth 1 origin <sha>`, `checkout --detach FETCH_HEAD`); `pin.ten_digests(tree: str) -> list[tuple[str, int, str]]` (the ten largest `SOURCE_EXT` files, ties by path, as (relpath, bytes, sha256)); `pin.archive_pin(url: str, out: str, fetch=None) -> tuple[int, str, int]` (the exploratory `snapshot.archive` reused); `pin.write_record(dest_dir: str, record: dict) -> None` (`pin_record.md` in the exploratory format plus `pin.json`).

- [ ] **Step 1: Write the failing tests**

```python
def test_ten_digests_largest_source_files_in_path_order():
    tree = make_tree(TMP, {"a.c": 300, "b.h": 300, "c.txt": 999, "d.py": 10, "e/f.c": 300})
    names = [p for p, _, _ in pin.ten_digests(tree)]
    assert names == ["a.c", "b.h", "e/f.c", "d.py"]                # .txt excluded; ties by path; size descending

def test_ls_remote_parses_symref():
    out = "ref: refs/heads/main\tHEAD\nabc123\tHEAD\n"
    assert pin.ls_remote("https://x", git=lambda args: out) == ("main", "abc123")

def test_fetch_by_hash_sets_autocrlf_false():
    calls = []
    pin.fetch_by_hash("https://x", "abc123", os.path.join(TMP, "t"), git=lambda args: calls.append(args) or "")
    assert ["config", "core.autocrlf", "false"] in [c[-3:] for c in calls] and any("--depth" in c for c in calls)
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `pin` not importable.
- [ ] **Step 3: Implement** `pin.py` (git via `subprocess.run(["git", ...])` behind the injectable `git` callable).
- [ ] **Step 4: Run** the suite. Expected: `26 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: observation-time pin (ls-remote, depth-1 fetch by hash, ten digests, record)"`.

---

### Task 8: `ledger.py`, `screen.py` -- per-item orchestration, batch documents, conformance checks

**Files:**
- Create: `phase3_5/run2/tools/ledger.py`, `phase3_5/run2/tools/screen.py`; fixtures: canned HTTP sequences for three fake items (alpha: project page with a step-2 link to a repository root that designates itself in its description; beta: GH port whose only non-forbidden starting point 404s; gamma: a DIST_TUPLE port whose identity key equals alpha's after normalization)

**Interfaces:**
- Consumes: Tasks 2-7.
- Produces: `ledger.FRAME_FIELDS`, `ledger.CANDIDATE_FIELDS` (Run 1's plus `starting_points_ref, pin_ref, decided_by_grammar, class_sensitivity_ref`), `ledger.SP_FIELDS`, `ledger.OBS_FIELDS`, `ledger.COST_FIELDS`, `ledger.WITNESS_FIELDS`; `ledger.append_rows(path, rows, fields)`; `ledger.batch_document(batch_no: int, items: list[dict]) -> str`; `ledger.check(run2_dir: str) -> int` (invariants: 128 frame rows at the end, candidate rows == distinct UR-PASS keys, gates after the first FAIL `NOT_REACHED`, every PASS/FAIL cites an EV id, every admitted starting point accounted, codes in vocabulary, no `${` in any URL); `screen.screen_item(rank: int, port_path: str, ports_root: str, witnesses: list[dict], state: dict, fetch=None, clock=None, git=None) -> dict` returning `frame_row, candidate_row | None, starting_points, observations, evidence_blocks, exposure, cost_row`; `screen.decide_gates(meta, sps, observations, witnesses) -> dict` (gate states and codes per the contract); `screen.run_batch(k: int, run2_dir: str, ports_root: str, fetch=None, clock=None, git=None) -> str` (writes the batch's rows and `screening_evidence_bNN.md`, returns its path).

- [ ] **Step 1: Write the failing tests**

```python
def test_alpha_passes_e2rep_with_one_designation():
    out = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state={}, fetch=canned_alpha, clock=fixed_clock, git=fake_git)
    c = out["candidate_row"]
    assert c["E2_REP"] == "PASS" and c["canonical_source_location"] == "https://github.com/acme/alpha"
    assert all(sp["action"] in ("observed", "closed-by-class") for sp in out["starting_points"])

def test_404_does_not_fail_candidate_alone():                   # Review Focus 4
    out = screen.screen_item(2, "games/beta", FIX + "/ports", witnesses=[], state={}, fetch=canned_beta_404, clock=fixed_clock, git=fake_git)
    c = out["candidate_row"]
    assert c["E2_REP"] == "UNRESOLVED" and c["protocol_issue_code"] == "PI-STARTING-POINTS-CLOSED" or c["E2_REP"] == "FAIL"
    assert c["failure_code"] != "E2REP-NO-STABLE-URL" or any(o["http_status"] == 404 for o in out["observations"])

def test_redirect_into_forbidden_class_closes():                # Review Focus 2
    out = screen.screen_item(3, "games/alpha", FIX + "/ports", witnesses=[], state={}, fetch=canned_redirect_to_releases, clock=fixed_clock, git=fake_git)
    sp = [s for s in out["starting_points"] if s["source"] == "HOMEPAGE"][0]
    assert sp["action"] == "closed-by-class" and sp["final_class"] == "release-assets" and len([o for o in out["observations"] if o["requested_url"] == sp["url"]]) == 1

def test_duplicate_upstream_one_candidate():                    # Review Focus 5
    state = {}
    a = screen.screen_item(1, "games/alpha", FIX + "/ports", witnesses=ALPHA_WITNESSES, state=state, fetch=canned_alpha, clock=fixed_clock, git=fake_git)
    g = screen.screen_item(2, "games/gamma", FIX + "/ports", witnesses=[], state=state, fetch=canned_alpha, clock=fixed_clock, git=fake_git)
    assert g["frame_row"]["upstream_resolution"] == "DUPLICATE" and g["frame_row"]["duplicate_of"] == a["frame_row"]["candidate_id"] and g["candidate_row"] is None

def test_batch_document_and_check():
    p = screen.run_batch(1, TMP_RUN2, FIX + "/ports", fetch=canned_all, clock=fixed_clock, git=fake_git)   # a 3-item fixture set is padded to 8 by FAIL_NONE ports
    text = open(p, encoding="utf-8").read()
    assert text.count("## EV-") >= 3 and "| rank |" in text
    assert ledger.check(TMP_RUN2) == 0
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `screen` not importable.
- [ ] **Step 3: Implement** `ledger.py` and `screen.py`. `screen_item`: `metadata.resolve` -> UR (`surfaces.identity_key`; `DUPLICATE` via `state["keys"]`) -> E1 (PASS unless the identity key's host and account are this project's own, `github.com/rohhj01-droid`) -> E2-REP: starting points classified; `release-assets` closed; unmatched URLs requested once and classified by response; allowed ones fetched in the contract's order (project page, step-2 links, repository root), each observation recorded; designation witnesses and the identifier taken from `witnesses` rows of kind `designation` / `identifier` / `source-tree` (validated: the quoted text must occur in the fetched body of the named surface, else `ValueError`); PASS when exactly one designated canonical location and one identifier; failure codes only with positive evidence; else UNRESOLVED with the PI code -> on PASS, `pin.ls_remote` + `pin.fetch_by_hash` + `pin.archive_pin` + `pin.ten_digests` -> E2-RULE, E3 from `validity` / `stateful` witnesses (quote must occur in the named file at the pinned tree, `file:line` checked) -> E4: `inventory.enumerators` on the pinned tree, `en_verdicts.decide` on every row, PASS iff an `enumerator` witness quotes an ADMIT (applied through `en_verdicts.apply_quoted`); evidence blocks in the protocol's EV format with `Observed` and `Inference` separate and the `Surfaces / Necessary because` lines for negative components; exposure log lines for README renderings seen.
- [ ] **Step 4: Run** the suite. Expected: `31 tests, 0 failed`.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R2: screen.py and ledger.py -- per-item screening, batch documents, conformance checks"`. R2 is complete: every tool exists before the frame is fetched.

---

### Task 9: R3 -- the frame re-fetched, verified, enumerated, checked

**Files:**
- Create: `phase3_5/run2/frame_enumeration.md`, `phase3_5/run2/raw_frame_all.txt`, `phase3_5/run2/screening_set_128.txt`; `phase3_5/run2/target/ports/` (git-ignored)

**Interfaces:**
- Consumes: `frame.*`.

- [ ] **Step 1: Fetch** `https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz` to `phase3_5/run2/target/ports.tar.gz` with `net.fetch` streaming (record `observed_at_utc`), fetch `.../7.9/SHA256`, and run `frame.verify_archive`. Expected: `(True, "937aef3d...", 56386078)` and the published line matches. If not: stop, RQA-01 with the observed values; nothing extracted.
- [ ] **Step 2: Extract selectively** with `frame.extract_selected`, record the member count; then `frame.enumerate_games(target/ports/ports)`. Expected: 477 items, 79 outside `games/`.
- [ ] **Step 3: Check** `frame.check_against_run1(items, "phase3_5/screening_set_128.txt")`. Expected: `[]`. If not empty: stop, RQA entry naming the differences (a tool defect by construction, since the hash matched).
- [ ] **Step 4: Write** `frame_enumeration.md` (provenance: hash, size, served Last-Modified, the Run 2 enumeration timestamp as provenance only; the command as executed; the counts; the budget boundary; the check result) and the two list files.
- [ ] **Step 5: Commit** `git commit -m "Run 2 R3: frame re-fetched (hash MATCH), 477 items enumerated, screening set equals Run 1's 128"`. Hold for the owner's review.

---

### Task 10: R4 -- screening, 16 batches of 8, decision point D1 after batch 1

**Files:**
- Create/append: the ledgers, `starting_points.tsv`, `observations.tsv`, `exposure_log.md`, `screening_cost.tsv`, `witness_bNN.tsv`, `screening_evidence_bNN.md` for NN = 01..16; `EXECUTION_QA.md` entries

**Interfaces:**
- Consumes: `screen.run_batch`, `ledger.check`.

Per batch k (in order, never two at once):

- [ ] **Step 1: Mechanical pass.** Run `screen.run_batch(k, ...)` with an empty witness table first: every item's metadata, UR, starting points, classifications and allowed observations are recorded; items whose gate stops at UR/E1 or whose E2-REP is determined without a witness are complete.
- [ ] **Step 2: The analyst's reading**, bounded to the contract's surfaces: for each item still open, read the fetched allowed pages (stored bodies) and, past E2-REP, the pinned tree's per-gate surfaces; write `witness_bNN.tsv` rows (quoted, located). No surface outside the contract's lists; a surface the gate's question needs and the contract lacks is an RQA entry, not an extra read.
- [ ] **Step 3: Decide.** Re-run `screen.run_batch(k, ...)` with the witness table (observations are reused from `observations.tsv`, not re-fetched); run `ledger.check`. Expected: exit 0; the batch document lists eight rows.
- [ ] **Step 4: Cost rows** for the batch (session time from the first read to this commit, per item by gate reached). **Commit** `git commit -m "Run 2 R4: batch NN (ranks a-b) screened -- <counts by terminal status>"`. Hold for the owner's review: 통과, or the failing item's rank.
- [ ] **Step 5 (after batch 1 only): D1.** Write RQA with the inputs (per-item session time, the batch's review time, the projection over 128) and the owner's decision in their words. Continue only on `continue`.
- [ ] **Step 6: Review correction** (when the owner names an item): correct that item in its own commit, keeping the earlier wording in place marked `[CORRECTED under review: ...]`; re-run `ledger.check`; the other seven are untouched.

After batch 16: `ledger.check` must report 128 frame rows; **Step 7: D2.** RQA with the survivor count and the projected inventory cost; the owner's decision. Commit `git commit -m "Run 2 R4: screening complete -- 128 items; ELIGIBLE n, REJECTED r, UNRESOLVED u, DUPLICATE d; D2 <decision>"`.

---

### Task 11: R5 -- survivor inventories under the frozen grammar, selection, D3

**Files:**
- Create: `phase3_5/run2/inventory/<cid>/` per survivor (`inventory_sources.tsv`, `inventory_enumerators.tsv`, `quoted_verdicts.tsv`, `class_sensitivity.md`, `observations.tsv`, `P_raw.tsv`, `enumerator_bounds.tsv` when needed); `phase3_5/run2/selection.md`; `EXECUTION_QA.md` entries

**Interfaces:**
- Consumes: `inventory.sources`, `inventory.enumerators`, `universe.members_detail`, `universe.units` (exploratory, imported); `en_verdicts.*`; the pinned trees under `target/<cid>/`.

Per survivor, in candidate-id order:

- [ ] **Step 1: Generate** `inventory.sources(tree)` and `inventory.enumerators(tree)`; decide sources by the exploratory design's Section 6.1 test (a quoted designation or REJECT with the reason; quarantine class never opened); run `en_verdicts.decide` on every enumerator row and write the table with `decided_by`.
- [ ] **Step 2: Quote** every `UNDECIDED` row and every row the analyst would ADMIT: `quoted_verdicts.tsv` rows with `file:line` evidence; `en_verdicts.apply_quoted`; a `ValueError` (an ADMIT or EN4 verdict without a citation) is fixed before anything is written.
- [ ] **Step 3: Universe and class.** `universe.members_detail` with a bounds table where a consulting loop's bound excludes rows (the XQA-08 rule); `universe.units`; `en_verdicts.class_of`; `en_verdicts.sensitivity` written as `class_sensitivity.md` (three sections: admitted rows with tags; EN2-PASS/EN4-FAIL rows; rows decided by quotation).
- [ ] **Step 4: Commit** `git commit -m "Run 2 R5: <cid> inventory -- <n> candidates, <a> admitted (<e> enforced / <s> asserted), class <A|B>; sensitivity table"`. Hold for the owner's review of the sensitivity table first.
- [ ] **Step 5 (if the grammar lacked a rule):** RQA entry; add the generic rule to `CATALOGUE` with a test; re-run `en_verdicts.decide` on every earlier survivor; report each survivor's verdict differences in the RQA entry; commit before continuing.

After the last survivor:

- [ ] **Step 6: Selection.** `selection.md`: every survivor with its class, its tie key (normalized URL, identifier), the ordering, the selected target; if the selected target is C084 or C065 (the exploratory lineage), the non-blindness declaration of spec 7.2 is written here and carried into the lane. Commit `git commit -m "Run 2 R5: selection -- <cid> <name> (class <A|B>, tie key ...)"`.
- [ ] **Step 7: D3.** RQA with the selected target's `P_raw` count and the owner's decision.

---

### Task 12: the Run 1 comparison, and the hand-off to the lane plan

**Files:**
- Create: `phase3_5/run2/tools/compare.py`, `phase3_5/run2/run1_vs_run2.tsv`

**Interfaces:**
- Consumes: `phase3_5/screening_frame_items.tsv` (Run 1), `phase3_5/run2/screening_frame_items.tsv`.
- Produces: `compare.table(run1_tsv: str, run2_tsv: str) -> list[dict]` with fields `frame_rank, port_path, run1_status, run1_stop_gate, run1_code, run2_status, run2_stop_gate, run2_code, differs (yes|no), run2_rule` (the contract section that accounts for a difference, filled by the analyst where `differs == yes`).

- [ ] **Step 1: Write the failing test**

```python
def test_compare_marks_differences():
    rows = compare.table(FIX + "/run1_items.tsv", FIX + "/run2_items.tsv")
    assert [r["differs"] for r in rows] == ["no", "yes", "yes"] and rows[1]["run2_rule"] == ""
```

- [ ] **Step 2: Run** the suite. Expected: FAIL, `compare` not importable.
- [ ] **Step 3: Implement**, run on the real ledgers, fill `run2_rule` per differing row (a contract section number), commit `git commit -m "Run 2: run1_vs_run2 comparison -- <n> of 128 differ"`.
- [ ] **Step 4: Hand-off.** Write the lane plan `docs/superpowers/plans/<date>-phase3-5-run2-lane.md` from the exploratory plan's Tasks 2 and 5-13 with the selected target's names, the non-blindness declaration if it applies, native replay N/A, D4 and D5, and the RESULTS generator with its regeneration check from the first draft; hold for the owner's approval before R6 starts.

---

## Self-review notes

- Spec coverage: 3 -> Task 9; 4.1 -> Task 3; 4.2-4.3 -> Task 4; 4.4 -> Task 5; 4.5-4.7 -> Task 8 (+ contract Task 1); 5 -> Tasks 8, 10; 6 -> Tasks 6, 11; 7.1-7.2 -> Task 11; 7.3 -> Task 7; 8 -> the lane plan (Task 12 Step 4), by the scope decision in the header; 9 -> Tasks 10, 11 (D1-D3; D4-D5 in the lane plan); 10 -> Task 12 and the lane plan; 11 -> the contract (Task 1) and RESULTS (lane plan); 12 -> the task order.
- Names used across tasks: `paths.use_exploratory_tools`, `metadata.resolve`, `surfaces.classify/normalize_url/starting_points/identity_key`, `net.fetch/links/step2_links`, `en_verdicts.decide/apply_quoted/class_of/sensitivity`, `pin.ls_remote/fetch_by_hash/ten_digests`, `screen.screen_item/run_batch`, `ledger.check`, `compare.table`; injection parameters `fetch=`, `clock=`, `git=` throughout.
- The analyst's inputs are one table per batch (`witness_bNN.tsv`) and one per survivor (`quoted_verdicts.tsv`); everything else is produced by the tools, so a reviewer reads a table and its evidence blocks, never prose with retractions.
- One departure from the spec's letter, visible rather than silent: E4's witness is produced by running the frozen grammar at screening time and quoting one ADMIT, so the survivor inventory (Task 11) completes the same procedure rather than restarting it -- the sealed firewall allows establishing the existence of enumeration mechanisms at screening, and the grammar is frozen before any candidate is seen.
