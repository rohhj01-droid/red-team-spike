# Phase 3.5 Exploratory C084 Study -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute the sealed design's steps X4a through X15 on C084 Crispy Doom at `7775ef82`, producing the tools, the frozen universe, the per-case analysis, the three artifacts, the known-failure lane and the exploratory RESULTS, each in its own reviewed commit.

**Architecture:** Seven small stdlib-only Python tools under `phase3_5/exploratory/tools/` do the mechanical parts (digests, tree walks, candidate generation, member parsing, GitHub API reads that discard what must not be seen, structural checks on the analysis documents). Everything else is analysis written by the analyst into fixed-format documents and TSVs under `phase3_5/exploratory/`, in the order the design fixes, with the owner's three decision points recorded in the study's own QA log.

**Tech Stack:** Python 3.11 stdlib only (`re`, `hashlib`, `tarfile`, `json`, `urllib.request`, `csv`), git 2.55, assert-based test script in the project's own style (`python -I tools/test_tools.py`; no pytest in this repo).

**Spec:** `docs/superpowers/specs/2026-10-29-phase3-5-exploratory-c084-design.md` (sealed `984f0c5`). Section numbers below without a prefix are this spec's; "sealed §" means the sealed methodology `docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`.

## Global Constraints

- Outputs: "everything under phase3_5/exploratory/ ; nothing else in phase3_5/ is created or changed" (§2.3). The only file outside it this plan touches is `README.md`, one pointer, at Task 13.
- The sealed record is not edited "for any reason": `phase3_5/RESULTS.md, EXECUTION_QA.md (QA-01..QA-43), SCREENING_PROTOCOL.md, FRAME_ENUMERATION.md, screening_evidence.md, screening_candidates.tsv, screening_frame_items.tsv, screening_set_128.txt` (§2.3).
- Every tool "takes the tree's path as an argument, and is run with `python -I`" (§4.2); the target checkout is data, never imported or executed.
- Network: "hosts github.com, api.github.com and codeload.github.com only; no search engine; no bot-detection or CAPTCHA bypass under any circumstances" (§5.1). Any API read discards titles, bodies and commit messages before display, except at the steps §5.2/§5.3 allow.
- Quarantine class, by file name, any case: `NEWS* CHANGELOG* ChangeLog* HISTORY* RELEASE* NOT-BUGS* BUGS* KNOWN* TODO* CHANGES*` and every file under a directory whose name matches one of them (§5.1). Not opened before X12.
- Third-party sources (wikis, forums, the parent project's repository, search engines) are not read before X14 (§5.1, §5.3).
- Artifact 1 is complete and committed for every native case before any sentence of Artifact 2 exists; Artifact 3 only after Artifact 2 is committed (§10).
- Cadence: "each step's output in its own commit, the SHA reported, review before the next step" (§14); review inside X9 is per native case (§9). A deviation is an XQA entry "written at the time, naming the clause" (§14).
- Every study document carries EXPLORATORY in its title and first paragraph (status block, §12).
- Files are written with LF line endings and UTF-8; TSVs are tab-separated with a header row, no quoting, no tabs or newlines inside a cell.
- Commit messages end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- The owner's decision points T1 (X7), T2 (X8), T3 (first accepted native case) are each recorded in `EXECUTION_QA.md` with input and grounds before the next step begins (§7.1).

## Review Focus

1. Initializer rows that are commented out (`//`, `/* */`), inside `#if 0`, or inside another preprocessor conditional: the member count must treat the first two as ABSENT and the third as PRESENT with its condition recorded (§6.3, EV-C084-E4-01's precedent); a `{` or `,` inside a string literal must not split or nest. Pinned in Task 3's `test_members_*`.
2. The GitHub issues endpoint returns pull requests as issues and pages at 100: PRs must be excluded by the `pull_request` key, every page read, and a 403/429 must stop with the reset time rather than return a partial count. Pinned in Task 7's `test_kf_*`.
3. Quarantine matching must be case-insensitive and apply to any directory component as well as the file name (`RELEASE_NOTES.md`, `docs/release/notes.md`). Pinned in Task 1's `test_quarantine`.
4. Doom-era sources contain Latin-1 bytes; scanning must neither crash nor shift line numbers, and digests are on raw bytes. Pinned in Task 1's `test_sha256_bytes` and Task 3's `test_latin1_scan`.
5. A CRLF-converting checkout would change every C file's digest: the target repository must have `core.autocrlf=false` set before checkout, and the ten-digest match at Task 2 is the verification that it did.

---

## File structure

```text
phase3_5/exploratory/
  .gitignore                 target/
  EXECUTION_QA.md            XQA-01 ... (Task 1 creates the header)
  pin_record.md              Task 2 (X4a)
  inventory_sources.tsv      Task 4 (X4b)
  inventory_enumerators.tsv  Task 4 (X4b)
  disclosure_log.md          Task 4 onward (§5.1)
  observations.tsv           Task 5 (X6, tool output)
  crosslinks.tsv             Task 5 (X6, analyst)
  P_raw.tsv                  Task 5 (X6, the freeze)
  E5.md                      Task 6 (X7)
  KF0.md                     Task 7 (X8)
  ARTIFACT_1_native.md       Task 9 (X9)
  units.tsv                  Task 9
  E_LOG.md                   Task 9
  cost_log.tsv               Task 9
  ARTIFACT_2_mapping.md      Task 10 (X10b)
  ARTIFACT_3_judgment.md     Task 10 (X10c)
  PRIMARY_RESULT.md          Task 11 (X11)
  kf_items.tsv               Task 12 (X12, only if T2 = attempt)
  KF.md                      Task 12 (X12-X14, or the N/A record)
  RESULTS.md                 Task 13 (X15)
  target/crispy-doom/        git-ignored checkout (Task 2)
  tools/
    common.py                tsv io, sha256, tree walk, quarantine test, api_get
    snapshot.py              digest | archive | sealed-instant        (Task 1)
    inventory.py             sources | enumerators                    (Task 3)
    universe.py              members | units                          (Task 5)
    kf_api.py                labels | count | list | first-post | comments (Task 7)
    checks.py                inventory | units | artifact1 | artifact2 | artifact3 | primary | cost | results (Tasks 3, 8)
    test_tools.py            assert-based tests, one file
    fixtures/                a small fake tree and canned API responses
```

Every tool is a CLI: `python -I phase3_5/exploratory/tools/<tool>.py <subcommand> <args>`; each prints a markdown-ready block or writes a TSV, and exits non-zero on any failed check so that a reviewer can re-run it.

---

### Task 1: Scaffold, `common.py`, `snapshot.py`

**Files:**
- Create: `phase3_5/exploratory/.gitignore`, `phase3_5/exploratory/EXECUTION_QA.md`
- Create: `phase3_5/exploratory/tools/common.py`, `phase3_5/exploratory/tools/snapshot.py`
- Create: `phase3_5/exploratory/tools/test_tools.py`, `phase3_5/exploratory/tools/fixtures/` (see Task 3 for the tree; this task adds `commits.json`)

**Interfaces:**
- Produces, `common.py`:
  - `sha256_file(path: str) -> str` (hex, raw bytes)
  - `walk_tree(root: str) -> list[str]` POSIX-style paths relative to `root`, sorted, `.git/` excluded
  - `is_quarantined(relpath: str) -> bool` per the Global Constraints pattern list, case-insensitive, tested against the file name and every directory component (prefix match on the name's stem, e.g. `release_notes.md` matches `RELEASE*`)
  - `read_tsv(path: str) -> list[dict[str, str]]`, `write_tsv(path: str, rows: list[dict[str, str]], fields: list[str]) -> None` (raises `ValueError` on a tab or newline inside a cell)
  - `api_get(url: str, fetch=None) -> object` -- GET with header `Accept: application/vnd.github+json`, JSON-decoded; `fetch(url) -> (status: int, headers: dict, body: bytes)` is injectable for tests; on status 403 or 429 raises `RuntimeError("rate limited until <X-RateLimit-Reset>")`; never retries
  - `strip(obj: dict, keep: tuple[str, ...]) -> dict` -- returns a new dict with only `keep` keys; for key `labels` keeps each label's `name` and `description` only; for key `pull_request` keeps `True`
- Produces, `snapshot.py`:
  - `REVISION = "7775ef82d1e9dfd50eb9d2824acefaeff7247458"`, `SEALED_INSTANT = "2026-08-26T19:23:05Z"`, `REPO = "fabiangreffrath/crispy-doom"`
  - `PINNED: dict[str, tuple[int, str]]` -- the ten `(path -> (bytes, sha256))` entries of EV-C084-PIN-01, copied verbatim from `phase3_5/screening_evidence.md`
  - `ARCHIVE_PIN = (2648481, "4edfcde1c4f6f9292d673116f81ba40df6cf04033f17346131b4f2fe72fbce55", 832)`
  - `digest(tree: str, pinned: dict = PINNED) -> list[tuple[str, int, str, str, bool]]` -- `(path, bytes, sha256, pinned_sha256, match)` in `pinned` order
  - `archive(url: str, out_path: str, fetch=None) -> tuple[int, str, int]` -- `(bytes, sha256, entry_count)`; the tarball is listed with `tarfile`, never extracted by this function
  - `sealed_instant(repo: str, until: str, fetch=None) -> dict` -- keys `sha`, `author_date`, `committer_date` from `GET https://api.github.com/repos/{repo}/commits?sha=master&until={until}&per_page=1`; the `message` field is discarded inside the function and never returned

- [ ] **Step 1: Write the scaffold files**

`.gitignore` contains the single line `target/`. `EXECUTION_QA.md` begins:

```markdown
# Phase 3.5 Exploratory Study (C084) -- Execution QA log

EXPLORATORY. This log belongs to the exploratory C084 study
(`docs/superpowers/specs/2026-10-29-phase3-5-exploratory-c084-design.md`,
sealed `984f0c5`). It is numbered XQA-01, XQA-02, ... so that the
screening run's QA-01..QA-43 stay closed. Entries are written at the
time, in order found; nothing is deleted; a withdrawn sentence stays in
place, marked.

Entry template:
## XQA-NN -- <title> (<YYYY-MM-DD>)
**Step:** X..   **Clause(s):** <design section / sealed section>
**What happened or was decided:**
**Effect on the record:**
```

- [ ] **Step 2: Write the failing tests for `common.py` and `snapshot.py`**

In `test_tools.py` (assert-based, `if __name__ == "__main__": run every function named test_*`, printing each name and PASS):

```python
def test_sha256_bytes():          # Review Focus 4
    # fixtures/tree/src/latin1.c holds the bytes b"/* caf\xe9 */\n"
    assert sha256_file(FIX + "/tree/src/latin1.c") == hashlib.sha256(b"/* caf\xe9 */\n").hexdigest()

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
    write_tsv(TMP + "/t.tsv", rows, ["a", "b"]); assert read_tsv(TMP + "/t.tsv") == rows
    try: write_tsv(TMP + "/t.tsv", [{"a": "1\t2", "b": ""}], ["a", "b"]); assert False
    except ValueError: pass

def test_strip_discards_message_and_title():
    assert strip({"sha": "x", "commit": {"message": "fix crash"}, "title": "t",
                  "labels": [{"name": "bug", "description": "d", "color": "f"}],
                  "pull_request": {"url": "u"}}, ("sha", "labels", "pull_request")) \
        == {"sha": "x", "labels": [{"name": "bug", "description": "d"}], "pull_request": True}

def test_api_get_rate_limit_raises():
    fetch = lambda url: (403, {"X-RateLimit-Reset": "1700000000"}, b"{}")
    try: api_get("https://api.github.com/x", fetch=fetch); assert False
    except RuntimeError as e: assert "1700000000" in str(e)

def test_pinned_table_matches_record():
    text = open(REPO_ROOT + "/phase3_5/screening_evidence.md", encoding="utf-8").read()
    block = text[text.index("## EV-C084-PIN-01"):text.index("## EV-C084-E2RULE-01")]
    found = dict((m.group(1), (int(m.group(2)), m.group(3))) for m in
                 re.finditer(r"^(\S+)\s+(\d+) bytes\n\s+([0-9a-f]{64})", block, re.M))
    assert found == PINNED and len(PINNED) == 10

def test_digest_flags_mismatch():
    pinned = {"src/latin1.c": (12, hashlib.sha256(b"/* caf\xe9 */\n").hexdigest()),
              "README.md": (1, "0" * 64)}
    rows = digest(FIX + "/tree", pinned)
    assert [r[0] for r in rows] == ["src/latin1.c", "README.md"]
    assert rows[0][4] is True and rows[1][4] is False

def test_sealed_instant_discards_message():
    fetch = lambda url: (200, {}, open(FIX + "/commits.json", "rb").read())
    r = sealed_instant("o/r", "2026-08-26T19:23:05Z", fetch=fetch)
    assert set(r) == {"sha", "author_date", "committer_date"}
    assert "fix" not in json.dumps(r)        # commits.json's message is "fix crash on load"

def test_archive_counts_entries():
    # the test first builds TMP/small.tar.gz with tarfile: 3 members
    n, digest_hex, entries = archive("https://example.invalid/x.tar.gz", TMP + "/a.tgz",
                                     fetch=lambda url: (200, {}, open(TMP + "/small.tar.gz", "rb").read()))
    assert entries == 3 and len(digest_hex) == 64 and n == os.path.getsize(TMP + "/small.tar.gz")
```

`fixtures/commits.json` is a one-element list in the GitHub commits-list shape with `sha`, `commit.author.date`, `commit.committer.date`, `commit.message: "fix crash on load"`.

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python -I phase3_5/exploratory/tools/test_tools.py`
Expected: ImportError / AssertionError before any PASS line.

- [ ] **Step 4: Implement `common.py` and `snapshot.py` to the interfaces above**

`is_quarantined`: split the path on `/`; for each component take its stem (text before the first `.`), upper-case it, and match `^(NEWS|CHANGELOG|HISTORY|RELEASE|NOT-BUGS|BUGS|KNOWN|TODO|CHANGES)([^A-Z]|$)`. `PINNED` is typed in from EV-C084-PIN-01; `test_pinned_table_matches_record` is what makes a typo impossible.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python -I phase3_5/exploratory/tools/test_tools.py`
Expected: every `test_*` printed with PASS, exit 0.

- [ ] **Step 6: Commit**

```bash
git add phase3_5/exploratory/.gitignore phase3_5/exploratory/EXECUTION_QA.md phase3_5/exploratory/tools
git commit -m "exploratory C084: scaffold, common and snapshot tools (before X4a)"
```

---

### Task 2: X4a -- the snapshot

**Files:**
- Create: `phase3_5/exploratory/pin_record.md`; the git-ignored checkout `phase3_5/exploratory/target/crispy-doom/`
- Modify: `phase3_5/exploratory/EXECUTION_QA.md` only if a step below says so

**Interfaces:**
- Consumes: `snapshot.py digest|archive|sealed-instant` (Task 1)
- Produces: the frozen tree at `phase3_5/exploratory/target/crispy-doom/` that every later task reads; `pin_record.md`

- [ ] **Step 1: Fetch the one commit, with no history and no line-ending conversion** (§4.2 step 1)

```bash
git init phase3_5/exploratory/target/crispy-doom
git -C phase3_5/exploratory/target/crispy-doom config core.autocrlf false
git -C phase3_5/exploratory/target/crispy-doom remote add origin https://github.com/fabiangreffrath/crispy-doom
git -C phase3_5/exploratory/target/crispy-doom fetch --depth 1 origin 7775ef82d1e9dfd50eb9d2824acefaeff7247458
git -C phase3_5/exploratory/target/crispy-doom checkout --detach FETCH_HEAD
```

If the fetch is refused for a bare commit id: do NOT clone; use the archive of Step 3 unpacked into that directory instead (§4.2 step 1 fallback) and record the fallback in `pin_record.md`.

- [ ] **Step 2: Record identity and run the ten-digest check**

Run: `git -C phase3_5/exploratory/target/crispy-doom rev-parse HEAD` -- Expected: `7775ef82d1e9dfd50eb9d2824acefaeff7247458`.
Run: `python -I phase3_5/exploratory/tools/snapshot.py digest phase3_5/exploratory/target/crispy-doom`
Expected: ten rows, every `match` True, exit 0. On any False: write XQA-01 (clause §4.2 step 3) and stop the study; nothing downstream proceeds.
Also record the UTC fetch timestamp and `git -C ... ls-files | wc -l`.

- [ ] **Step 3: Fetch the archive and record MATCH/MISMATCH** (§4.2 step 4)

Run: `python -I phase3_5/exploratory/tools/snapshot.py archive https://github.com/fabiangreffrath/crispy-doom/archive/7775ef82d1e9dfd50eb9d2824acefaeff7247458.tar.gz phase3_5/exploratory/target/archive.tar.gz`
Expected: a line `bytes=... sha256=... entries=...` beside `pinned 2648481 4edfcde1... 832`, each marked MATCH or MISMATCH. A MISMATCH is recorded in `pin_record.md`, not treated as a failure.

- [ ] **Step 4: Sealed-instant consistency check** (§4.2 step 5)

Run: `python -I phase3_5/exploratory/tools/snapshot.py sealed-instant`
Expected: `sha=<40 hex> author_date=... committer_date=...` and `COINCIDES` or `DIFFERS` against `REVISION`. On DIFFERS: XQA entry (clause §4.2 step 5); the revision does not change.

- [ ] **Step 5: Write `pin_record.md`**

Title `# Pin record -- EXPLORATORY C084 study (X4a)`; first paragraph names the study and the label; then, in this order: the fetch commands as run and the UTC timestamp; `rev-parse` output; file count; the ten-digest table as printed; the archive line with MATCH/MISMATCH per field; the sealed-instant line with COINCIDES/DIFFERS; whether the depth-1 fetch or the archive fallback produced the tree.

- [ ] **Step 6: Verify the record against the tools**

Run the three `snapshot.py` subcommands again and diff their output against the blocks pasted in `pin_record.md`. Expected: identical.

- [ ] **Step 7: Commit**

```bash
git add phase3_5/exploratory/pin_record.md phase3_5/exploratory/EXECUTION_QA.md
git commit -m "X4a: C084 snapshot pinned at 7775ef82 (digests, archive, sealed-instant check)"
```

Report the SHA; hold for review before Task 3.

---

### Task 3: Inventory tools (`inventory.py`, `checks.py inventory`), committed before they run

**Files:**
- Create: `phase3_5/exploratory/tools/inventory.py`, `phase3_5/exploratory/tools/checks.py`
- Create: `phase3_5/exploratory/tools/fixtures/tree/...` (below)
- Modify: `phase3_5/exploratory/tools/test_tools.py`

**Interfaces:**
- Produces, `inventory.py`:
  - `S_DOC_EXT = {".md", ".txt", ".html", ".htm", ".rst", ".adoc", ".texi", ".1", ".5", ".6", ".man"}`
  - `sources(tree: str) -> list[dict]` fields `path, bytes, decision, reason` -- rows for every S_doc member (§6.1 rule: extension in `S_DOC_EXT`, or no extension and in the root or under a directory whose name starts with `doc` or `man`, or linked from `README.md` by a `](relative/path)` link that exists) plus every quarantined file anywhere in the tree; `decision` is `QUARANTINED` for those, else empty; `reason` empty
  - `enumerators(tree: str) -> list[dict]` fields `cand_id, file, line, symbol, class, element_type, members, absent, conditional, en1, en2, en3, en4, en5, en6, tag, reject_reason, evidence` -- one row per candidate; `cand_id` = `C001...` for the code classes K1-K3 in file-then-line order, and `D001...` for K4 document candidates in the same order, so that a K4 row never shifts a code row's id; a K4 row has `symbol` = `doc:<file>:<line>` and the tool fills its `evidence` with the matched sentence; `members`/`absent`/`conditional` are counts from `count_members` (defined in Step 4 below; Task 5 reuses it)
  - `K1_RE` (multiline) matching, at column 0, `[static ][const ]<type words> <name>[<size>][...]* = {` with `=` and `{` allowed on the next line; `K2` = a K1 row whose element type's struct body (collected from `typedef struct {...} name;` and `struct name {...}` over all `.c/.h`) contains `(*`, or a direct function-pointer array `type (*name[])(...) = {`; `K3_RE` = a `#define` whose continuation lines are two or more invocations of one macro name; `K4_RE` = over non-quarantined S_doc text, a sentence containing `(all|every|each)` then within 100 characters `(in|under|inside)`, case-insensitive
  - K1 breadth: ANY element type, scalar and pointer included (`const char *names[] = {...}`). This is broader than §6.2's parenthetical "with a struct or array element type", on purpose: a string-list registry is the commonest registry idiom after the struct table, and the narrower pattern would miss it. The owner approves this widening by approving this plan; it is still recorded as **XQA-01 (design amendment before execution, clause §6.2 K1)** at Task 4 Step 1, because it departs from the sealed text
- Produces, `checks.run(sub: str, d: str) -> int` in `checks.py` (CLI `python -I checks.py <sub> <dir>`, exit code = return value), this task adding `sub = "inventory"`: returns 0 iff in `inventory_sources.tsv` every row's `decision` is `ADMIT`, `REJECT` or `QUARANTINED` and every ADMIT/REJECT has a non-empty `reason`; and in `inventory_enumerators.tsv` every row has `en1..en6` each in `{PASS, FAIL, ""}`, a REJECT row has exactly one FAIL with all earlier EN = PASS and later EN empty, an ADMIT row has six PASS, a `tag` in `{enforced, asserted}` and non-empty `evidence`

- [ ] **Step 1: Write the fixture tree** `tools/fixtures/tree/`

```text
README.md            "See [the rules](docs/rules.md) and [notes](docs/NOTES.txt)."
NEWS.md              "1.0: fixed a crash"                       (quarantined)
INSTALL              "build with make"                           (root, no extension -> S_doc)
docs/rules.md        "All IWADs are in the wads directory."      (K4 candidate)
docs/NOTES.txt       "notes"
docs/RELEASE_NOTES.md "x"                                        (quarantined by name)
docs/release/notes.md "x"                                        (quarantined by directory)
man/prog.6           "man page"
src/noext            "x"                                         (not S_doc)
src/latin1.c         bytes b"/* caf\xe9 */\n"
src/a.h              typedef struct { const char *name; int mission; } iwad_t;
                     typedef struct { const char *name; void (*fn)(void); } cmd_t;
src/a.c              static const iwad_t iwads[] =
                     {
                         { "doom2.wad", 2 },
                         //{ "strife0.wad", 9 },
                         { "plutonia.wad", 3 },   /* not a row, { brace */
                     #ifdef HAVE_X
                         { "x.wad", 4 },
                     #endif
                         { "a,b{c}.wad", 5 },
                     };
                     const char *names[] = { "a", "b" };
                     int nums[3] = { 1, 2, 3 };
                     static char grid[2][3] = { {1,2,3}, {4,5,6} };
                     void (*fns[])(void) = { f, g };
                     static const cmd_t cmds[] = { { "x", f } };
                     void h(void) { int loc[] = { 1 }; }
src/b.c              static const iwad_t t2[] = {
                     #if 0
                         { "dead.wad", 1 },
                     #endif
                         { "live.wad", 2 },
                     };
```

- [ ] **Step 2: Write the failing tests**

```python
def test_sources_membership():
    rows = {r["path"]: r for r in sources(FIX + "/tree")}
    assert set(rows) == {"README.md", "NEWS.md", "INSTALL", "docs/rules.md", "docs/NOTES.txt",
                         "docs/RELEASE_NOTES.md", "docs/release/notes.md", "man/prog.6"}
    assert rows["NEWS.md"]["decision"] == "QUARANTINED" == rows["docs/release/notes.md"]["decision"]
    assert rows["README.md"]["decision"] == ""

def test_enumerator_candidates():
    rows = {r["symbol"]: r for r in enumerators(FIX + "/tree")}
    assert set(rows) >= {"iwads", "names", "nums", "grid", "fns", "cmds", "t2"} and "loc" not in rows
    assert rows["iwads"]["class"] == "K1" and rows["cmds"]["class"] == "K2" and rows["fns"]["class"] == "K2"
    assert rows["iwads"]["element_type"] == "iwad_t" and rows["iwads"]["line"] == "1"

def test_members_absent_and_conditional():     # Review Focus 1
    r = {r["symbol"]: r for r in enumerators(FIX + "/tree")}
    assert (r["iwads"]["members"], r["iwads"]["absent"], r["iwads"]["conditional"]) == ("4", "1", "1")
    assert (r["t2"]["members"], r["t2"]["absent"]) == ("1", "1")
    assert r["grid"]["members"] == "2" and r["names"]["members"] == "2"

def test_k4_sentence():
    rows = [r for r in enumerators(FIX + "/tree") if r["class"] == "K4"]
    assert rows and rows[0]["file"] == "docs/rules.md" and "wads directory" in rows[0]["evidence"]

def test_latin1_scan():                        # Review Focus 4
    assert all(r["file"] != "src/latin1.c" for r in enumerators(FIX + "/tree"))  # scanned, no crash, no rows

def test_checks_inventory():
    src_ok = [{"path": "README.md", "bytes": "1", "decision": "REJECT", "reason": "no designation"},
              {"path": "NEWS.md", "bytes": "1", "decision": "QUARANTINED", "reason": ""}]
    en_ok = [dict(cand_id="C001", file="src/a.c", line="1", symbol="iwads", **{"class": "K1"}, element_type="iwad_t",
                  members="4", absent="1", conditional="1", en1="PASS", en2="PASS", en3="PASS", en4="PASS",
                  en5="PASS", en6="PASS", tag="enforced", reject_reason="", evidence="src/a.c:1 ..."),
             dict(cand_id="C002", file="src/a.c", line="9", symbol="names", **{"class": "K1"}, element_type="char *",
                  members="2", absent="0", conditional="0", en1="PASS", en2="FAIL", en3="", en4="", en5="", en6="",
                  tag="", reject_reason="EN2: no declared scope", evidence="")]
    write_tsv(TMP + "/inventory_sources.tsv", src_ok, SRC_FIELDS); write_tsv(TMP + "/inventory_enumerators.tsv", en_ok, EN_FIELDS)
    assert checks.run("inventory", TMP) == 0
    en_bad = [dict(en_ok[1], en3="PASS")]                 # a FAIL followed by a PASS
    write_tsv(TMP + "/inventory_enumerators.tsv", en_bad, EN_FIELDS); assert checks.run("inventory", TMP) == 1
    src_bad = [dict(src_ok[0], decision="")]              # an undecided source row
    write_tsv(TMP + "/inventory_sources.tsv", src_bad, SRC_FIELDS); assert checks.run("inventory", TMP) == 1
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python -I phase3_5/exploratory/tools/test_tools.py` -- Expected: the new tests fail with ImportError.

- [ ] **Step 4: Implement `inventory.py` and `checks.py inventory`**

Member counting (shared with Task 5 as `inventory.count_members(text: str, start: int) -> tuple[list[dict], list[str]]` returning `(present_members, absent_texts)`; each present member is `{"index", "text", "cond"}`): from the `{` at `start`, scan characters with a depth counter; `//` to end of line and `/* ... */` are comment text and are collected as ABSENT candidates when a comment's content, stripped, begins with `{`; string literals (`"..."` with backslash escapes) are opaque; a line beginning with `#` is a preprocessor line: `#if 0` pushes ABSENT until its `#endif`/`#else`, any other `#if/#ifdef/#ifndef/#elif` pushes its text as the current `cond`, `#else` keeps the condition marked `else`, `#endif` pops; a `,` at depth 1 ends an element; the element before the closing `}` ends without a comma; an empty element (trailing comma) is skipped. Files are decoded as `latin-1` for scanning.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python -I phase3_5/exploratory/tools/test_tools.py` -- Expected: all PASS.

- [ ] **Step 6: Commit (before the tools touch the target tree)**

```bash
git add phase3_5/exploratory/tools
git commit -m "exploratory C084: inventory tools and checks, committed before X4b runs"
```

---

### Task 4: X4b -- run the inventory, then decide every row

**Files:**
- Create: `phase3_5/exploratory/inventory_sources.tsv`, `phase3_5/exploratory/inventory_enumerators.tsv`, `phase3_5/exploratory/disclosure_log.md`
- Modify: `phase3_5/exploratory/EXECUTION_QA.md`

**Interfaces:**
- Consumes: `inventory.py sources|enumerators`, `checks.py inventory` (Task 3)
- Produces: the two TSVs with every row decided; `cand_id` values that Task 5 uses as enumerator ids

- [ ] **Step 1: Record XQA-01 (K1 widened to any element type; clause §6.2) and create `disclosure_log.md`**

`disclosure_log.md` header: title with EXPLORATORY, then a table `utc | step | location (file:line) | what was disclosed | unit/case under analysis`, initially empty. From this step on, any in-source comment that discloses a failure cause is appended at the moment it is read (§5.1).

- [ ] **Step 2: Generate the raw tables**

Run: `python -I phase3_5/exploratory/tools/inventory.py sources phase3_5/exploratory/target/crispy-doom phase3_5/exploratory/inventory_sources.tsv`
Run: `python -I phase3_5/exploratory/tools/inventory.py enumerators phase3_5/exploratory/target/crispy-doom phase3_5/exploratory/inventory_enumerators.tsv`
Expected: both files written; the tool prints row counts per class (K1/K2/K3/K4) and the quarantined count. Note the counts for RESULTS §12 item 4.

- [ ] **Step 3: Commit the raw tables before any verdict is written**

```bash
git add phase3_5/exploratory/inventory_sources.tsv phase3_5/exploratory/inventory_enumerators.tsv phase3_5/exploratory/disclosure_log.md phase3_5/exploratory/EXECUTION_QA.md
git commit -m "X4b: inventory candidate tables as generated (no verdicts yet)"
```

- [ ] **Step 4: Decide `inventory_sources.tsv`** (§6.1)

For each non-quarantined row: open the file; `decision` = `ADMIT` only if (a) a project-owned statement, quoted in `reason` with `file:line`, says this file states the rules/requirements/valid configurations/accepted inputs, and (b) the file exposes mechanical segmentation (name the segmentation in `reason`); otherwise `REJECT` with `reason` = `no designation` (and where the statement was looked for: the file's opening, README.md, other in-tree docs) or `no segmentation`. Quarantined rows stay as generated and are not opened.

- [ ] **Step 5: Decide `inventory_enumerators.tsv`** (§6.2)

For each row, in `cand_id` order, fill `en1..en6` in order and stop at the first FAIL; `reject_reason` = that criterion and one sentence; `evidence` = for an ADMIT, the located EN4 connection quoted (`file:line`, the comment/identifier/error message/code path in which the set decides acceptance, refusal or eligibility) and the EN5 closure basis; `tag` = `enforced` or `asserted`. A table consulted only to pick something, with no refusal on a miss, FAILS EN4 (§6.2 narrow reading). Record in XQA whether the IWAD registry row's decision agrees with EV-C084-E4-01.

- [ ] **Step 6: Run the consistency check**

Run: `python -I phase3_5/exploratory/tools/checks.py inventory phase3_5/exploratory`
Expected: exit 0, printing `sources: N rows, A admitted, R rejected, Q quarantined` and `enumerators: N rows, A admitted (enforced E, asserted S), rejected by EN1..EN6: [...]`.

- [ ] **Step 7: Commit the verdicts**

```bash
git add phase3_5/exploratory/inventory_sources.tsv phase3_5/exploratory/inventory_enumerators.tsv phase3_5/exploratory/disclosure_log.md phase3_5/exploratory/EXECUTION_QA.md
git commit -m "X4b: inventory verdicts (authoritative sources, enumerators EN1-EN6, tags)"
```

Report the SHA; hold for review before Task 5.

---

### Task 5: `universe.py` (tested, committed first), then X6 -- `P_raw` frozen

**Files:**
- Create: `phase3_5/exploratory/tools/universe.py`
- Create: `phase3_5/exploratory/observations.tsv`, `phase3_5/exploratory/crosslinks.tsv`, `phase3_5/exploratory/P_raw.tsv`
- Modify: `phase3_5/exploratory/tools/test_tools.py`

**Interfaces:**
- Consumes: `inventory.count_members` (Task 3); the ADMIT rows of `inventory_enumerators.tsv` (Task 4)
- Produces, `universe.py`:
  - `members(tree: str, enumerators_tsv: str) -> list[dict]` fields `obs_id, enum_id, file, line, index, text, cond` -- for every ADMIT row of class K1/K2/K3, one row per present member, `enum_id = cand_id`, `obs_id = f"E{cand_id[1:]}-{index:03d}"` (e.g. `C017` -> `E017-001`), `text` whitespace-collapsed; ABSENT members are printed to stdout as `ABSENT <enum_id> <text>` and not written
  - `units(observations_tsv: str, crosslinks_tsv: str, out_tsv: str) -> tuple[int, int, int]` -- returns `(O_raw, P_raw, linked_units)`; `crosslinks.tsv` fields `obs_a, obs_b, artifact, quote` (every row an edge from an in-tree, non-quarantined artifact, quoted); connected components by union-find; `P_raw.tsv` fields `unit_id, obs_ids, enum_ids, tags, linked, text` with `unit_id = U001...` in order of each component's smallest `obs_id`, `obs_ids` comma-joined, `text` the members' texts joined by ` || `
  - a K4 (declared-convention) enumerator's members, and any admitted normative source's items (`N<k>-<n>`), are not produced by the tool: the analyst appends them to `observations.tsv` by hand, one row per item at the source's own segmentation, with `file` and `line` of each item; the tool's `units` subcommand accepts those rows unchanged

- [ ] **Step 1: Write the failing tests**

```python
def test_members_from_fixture():
    # fixtures/enumerators_admit.tsv: ADMIT rows for iwads (C001) and t2 (C007) of the fixture tree
    rows = members(FIX + "/tree", FIX + "/enumerators_admit.tsv")
    assert [r["obs_id"] for r in rows if r["enum_id"] == "C001"] == ["E001-001", "E001-002", "E001-003", "E001-004"]
    assert [r["text"] for r in rows if r["enum_id"] == "C007"] == ['{ "live.wad", 2 }']
    assert [r["cond"] for r in rows if r["enum_id"] == "C001"][2] == "#ifdef HAVE_X"

def test_units_components():
    # observations o1..o5; crosslinks o1-o2, o2-o3 -> one unit of three, two singletons
    o, p, linked = units(FIX + "/obs5.tsv", FIX + "/links2.tsv", TMP + "/P.tsv")
    assert (o, p, linked) == (5, 3, 1)
    rows = read_tsv(TMP + "/P.tsv")
    assert rows[0]["unit_id"] == "U001" and rows[0]["obs_ids"] == "o1,o2,o3" and rows[0]["linked"] == "1"

def test_units_no_links():
    o, p, linked = units(FIX + "/obs5.tsv", FIX + "/links0.tsv", TMP + "/P.tsv")
    assert (o, p, linked) == (5, 5, 0)
```

- [ ] **Step 2: Run the tests to verify they fail** -- `python -I phase3_5/exploratory/tools/test_tools.py`, Expected: ImportError on `universe`.

- [ ] **Step 3: Implement `universe.py`** to the interfaces; `members` re-reads each ADMIT row's `file:line` from the tree and calls `inventory.count_members`.

- [ ] **Step 4: Run the tests to verify they pass** -- Expected: all PASS.

- [ ] **Step 5: Commit the tool**

```bash
git add phase3_5/exploratory/tools
git commit -m "exploratory C084: universe tool (members, units), committed before X6 runs"
```

- [ ] **Step 6: Run `members`, add hand-segmented rows if any, write `crosslinks.tsv`**

Run: `python -I phase3_5/exploratory/tools/universe.py members phase3_5/exploratory/target/crispy-doom phase3_5/exploratory/inventory_enumerators.tsv phase3_5/exploratory/observations.tsv`
Expected: `observations.tsv` written; every `ABSENT` line printed is copied into `P_raw.tsv`'s commit message body. Then append K4/normative rows by hand if Task 4 admitted any. `crosslinks.tsv`: header only unless an in-tree non-quarantined artifact explicitly links two observations (§6.3); each edge carries its quote and location.

- [ ] **Step 7: Run `units` -- the freeze**

Run: `python -I phase3_5/exploratory/tools/universe.py units phase3_5/exploratory/observations.tsv phase3_5/exploratory/crosslinks.tsv phase3_5/exploratory/P_raw.tsv`
Expected: `O_raw=<n> P_raw=<m> linked_units=<k>` printed; re-running produces a byte-identical `P_raw.tsv` (check with `git diff --stat` after a second run: no change).

- [ ] **Step 8: Commit**

```bash
git add phase3_5/exploratory/observations.tsv phase3_5/exploratory/crosslinks.tsv phase3_5/exploratory/P_raw.tsv
git commit -m "X6: P_raw frozen -- O_raw=<n>, P_raw=<m>, linked units=<k>; ABSENT members listed below"
```

Report the SHA; hold for review before Task 6.

---

### Task 6: X7 -- E5 checkpoint and decision point T1

**Files:**
- Create: `phase3_5/exploratory/E5.md`
- Modify: `phase3_5/exploratory/EXECUTION_QA.md`

- [ ] **Step 1: Write `E5.md`**

Title with EXPLORATORY; the two conditions of §7: `U_primary finite and fully listed: YES -- P_raw.tsv, <m> units, commit <sha of Task 5>`; then the T1 input for the owner: `P_raw = <m>`, `enumerators admitted = <a> (enforced <e>, asserted <s>)`, and the scale note copied from §7 ("a unit under review has been estimated, not measured, at one to three hours"). No projection of outcomes, no reading of any unit.

- [ ] **Step 2: Decision point T1 -- the owner decides on the count alone** (§7.1)

Present `E5.md` to the owner. Record the answer as `XQA-NN -- T1 decision (X7)`: input (`P_raw`), decision (`proceed` or `infeasible at this count`), the owner's grounds in their words. On `infeasible`: `E5.md` ends with `E5: FAIL -- primary-lane boundedness failure`; Task 7 is still executed (§7), then the study goes to Task 13 with Tasks 8-12 marked not executed.

- [ ] **Step 3: Commit**

```bash
git add phase3_5/exploratory/E5.md phase3_5/exploratory/EXECUTION_QA.md
git commit -m "X7: E5 checkpoint -- P_raw=<m>; T1 decision recorded"
```

---

### Task 7: `kf_api.py` (tested, committed first), then X8 -- KF-0 applied and decision point T2

**Files:**
- Create: `phase3_5/exploratory/tools/kf_api.py`, `phase3_5/exploratory/tools/fixtures/labels.json`, `.../issues_p1.json`, `.../issues_p2.json`
- Create: `phase3_5/exploratory/KF0.md`
- Modify: `phase3_5/exploratory/tools/test_tools.py`, `phase3_5/exploratory/EXECUTION_QA.md`

**Interfaces:**
- Consumes: `common.api_get`, `common.strip` (Task 1)
- Produces, `kf_api.py` (every function takes `fetch=None` for injection):
  - `labels(repo: str) -> list[tuple[str, str]]` -- `(name, description)` from `GET /repos/{repo}/labels?per_page=100&page=N` until a short page
  - `issue_numbers(repo: str, label: str | None) -> set[int]` -- from `GET /repos/{repo}/issues?state=all&per_page=100&page=N[&labels=<label>]`, every page until a short page; objects carrying a `pull_request` key are excluded; nothing but `number` is kept
  - `count(repo: str, label_set: list[str]) -> int` -- `len` of the union of `issue_numbers` over `label_set`, or over `[None]` when the list is empty; prints nothing but the count and the UTC timestamp
  - `list_ids(repo: str, label_set: list[str], out_tsv: str) -> int` -- same union, written sorted to `out_tsv` (fields `number`) with the UTC timestamp in a header comment line; used only at X12
  - `first_post(repo: str, number: int) -> dict` -- keys `number, title, state, created_at, labels, body` from `GET /repos/{repo}/issues/{number}`; comments are NOT fetched (that endpoint is separate; §5.2)
  - `comments(repo: str, number: int) -> list[dict]` -- keys `created_at, body` from `GET /repos/{repo}/issues/{number}/comments`; X14 only

- [ ] **Step 1: Write the fixtures and the failing tests**

`labels.json`: two labels `bug` ("Something isn't working") and `enhancement`. `issues_p1.json`: 100 objects numbered 1..100 where number 50 carries `pull_request`; `issues_p2.json`: 3 objects 101..103. The injected `fetch` serves p1 for `page=1`, p2 for `page=2`, and `[]` after.

```python
def test_labels(): assert labels("o/r", fetch=F) == [("bug", "Something isn't working"), ("enhancement", "")]

def test_issue_numbers_excludes_prs_and_paginates():    # Review Focus 2
    nums = issue_numbers("o/r", None, fetch=F)
    assert len(nums) == 102 and 50 not in nums and 103 in nums

def test_count_union():
    # fetch serving label=bug -> numbers {1,2}, label=crash -> {2,3}
    assert count("o/r", ["bug", "crash"], fetch=F2) == 3

def test_rate_limit_stops_count():                      # Review Focus 2
    try: count("o/r", [], fetch=lambda u: (403, {"X-RateLimit-Reset": "1"}, b"[]")); assert False
    except RuntimeError: pass

def test_first_post_has_no_comments_key():
    r = first_post("o/r", 7, fetch=F3)
    assert set(r) == {"number", "title", "state", "created_at", "labels", "body"}
```

- [ ] **Step 2: Run the tests to verify they fail** -- Expected: ImportError on `kf_api`.

- [ ] **Step 3: Implement `kf_api.py`**; `strip` is applied to every object before anything else touches it.

- [ ] **Step 4: Run the tests to verify they pass** -- Expected: all PASS.

- [ ] **Step 5: Commit the tool**

```bash
git add phase3_5/exploratory/tools
git commit -m "exploratory C084: KF API tool (labels, count, list, first-post, comments), committed before X8"
```

- [ ] **Step 6: Tracker of record** (§8)

Grep the non-quarantined tree for `issues`, `bug report`, `report bugs`, `tracker` in `README.md`, `CONTRIBUTING*`, `.github/` and `docs/`; quote any designation found in `KF0.md`. Absent one, the tracker is `https://github.com/fabiangreffrath/crispy-doom/issues`.

- [ ] **Step 7: Decide `L` from the label list alone**

Run: `python -I phase3_5/exploratory/tools/kf_api.py labels fabiangreffrath/crispy-doom`
Expected: the `(name, description)` list. In `KF0.md`, list every label with its description verbatim and mark each `L` or `not L` with the word that decided it (bug, defect, crash, regression, error, or a synonym -- or none). No issue has been listed at this point.

- [ ] **Step 8: Count**

Run: `python -I phase3_5/exploratory/tools/kf_api.py count fabiangreffrath/crispy-doom <label1> <label2> ...` (no labels if `L` is empty)
Expected: `count=<c> at <UTC>`; copy into `KF0.md` with the rule as applied (labels or all-issues branch, PRs excluded).

- [ ] **Step 9: Decision point T2 -- the owner decides on the count alone** (§7.1, §8)

Record `XQA-NN -- T2 decision (X8)`: input (`c`, the `L` branch), decision (`attempt in full` or `N/A -- boundedness failure`), grounds. On N/A, Task 12 writes `KF.md` as the N/A record only.

- [ ] **Step 10: Commit**

```bash
git add phase3_5/exploratory/KF0.md phase3_5/exploratory/EXECUTION_QA.md
git commit -m "X8: KF-0 applied -- tracker, L=<...>, count=<c>; T2 decision recorded"
```

If T1 was `infeasible`, go to Task 13 now.

---

### Task 8: `checks.py` for the analysis documents, committed before X9

**Files:**
- Modify: `phase3_5/exploratory/tools/checks.py`, `phase3_5/exploratory/tools/test_tools.py`
- Create: `phase3_5/exploratory/tools/fixtures/docs_ok/` and `fixtures/docs_bad/` (small ARTIFACT/units/P_raw samples)

**Interfaces:**
- Produces, `checks.py <sub> <dir>` with `<dir>` = `phase3_5/exploratory`, exit 0 iff:
  - `units`: every `unit_id` of `P_raw.tsv` has exactly one row in `units.tsv` with `status` in `{RESOLVED, E?}`; an `E?` row has non-empty `e_gaps` (comma list drawn from `Q1..Q5`) and a heading `## E? <unit_id>` in `E_LOG.md` whose entry has the four labelled lines `missing evidence:`, `why recovery failed:`, `opacity/tooling vs unmodeled structure:`, `F2 re-check:` non-empty; every `NC-nn` named in `native_cases` has a heading `## NC-nn` in `ARTIFACT_1_native.md`; prints `resolved R / P_raw M`, `E? U / P_raw M`
  - `artifact1`: `ARTIFACT_1_native.md` contains none of `WorldState`, `MonitorState`, `EventProvenanceState`, `violation judgment`, `event provenance`; every `## NC-` section contains the ten field lines (`source observation ids:`, `native state/data involved:`, `writers / creation points:`, `updates / invalidation paths:`, `readers / consumption points:`, `lifetime / persistence / reset behavior:`, `relevant transitions:`, `supporting source-code/docs evidence:`, `remaining native-level uncertainty:`, `lineage:` -- the last for L4) and five lines `Q1 created:` .. `Q5 after consumption:` each containing a `<path>:<digits>` citation (an `N/A:` answer included), and a `Status:` line of `RESOLVED` or `E? (Q..)`
  - `artifact2`: every `## NC-nn` of Artifact 1 has a `## NC-nn` section in `ARTIFACT_2_mapping.md` with an `outcome:` line matching `R0`, `F0`, or a comma list over `{F1,F2,F3}`; an `R0` section has a non-empty `competitor:` line; a section listing `F3` has a non-empty `positive evidence:` line; every section has `roles:` and `reasoning:` lines; prints the per-finding counts `R0 n, F0 n, F1 n, F2 n, F3 n` as native cases and, via `units.tsv`, as counting units
  - `artifact3`: `ARTIFACT_3_judgment.md` has `## Applicability domain` before `## Decision procedure`, and a line `totality:` under the latter
  - `primary`: the lines `resolved R / P_raw M` and `E? U / P_raw M` printed by `units` appear verbatim in `PRIMARY_RESULT.md`, and its findings table rows equal the `artifact2` counts
  - `cost`: `cost_log.tsv` (fields `id, session_start_utc, session_end_utc, first_commit, accepted_by, accepted_utc`) has at least one row per `NC-nn` in Artifact 1 with every field non-empty
  - `results`: `RESULTS.md`'s first line contains `EXPLORATORY`, its first paragraph contains `Run 2`, and headings `### 14.1` .. `### 14.12` all exist in order

- [ ] **Step 1: Write `docs_ok/` (one unit, one NC, consistent files) and `docs_bad/` (an NC with `MonitorState` in Artifact 1; a unit missing from `units.tsv`; an R0 with empty `competitor:`) and the failing tests**

```python
def test_checks_docs_ok():
    for sub in ["units", "artifact1", "artifact2", "artifact3", "primary", "cost", "results"]:
        assert checks.run(sub, FIX + "/docs_ok") == 0, sub
def test_checks_docs_bad():
    assert checks.run("artifact1", FIX + "/docs_bad") == 1
    assert checks.run("units", FIX + "/docs_bad") == 1
    assert checks.run("artifact2", FIX + "/docs_bad") == 1
```

- [ ] **Step 2: Run the tests to verify they fail** -- Expected: AttributeError (`checks.run` has no such subcommands).

- [ ] **Step 3: Implement the subcommands** as `checks.run(sub: str, d: str) -> int`, one function per subcommand, section parsing by `## ` headings.

- [ ] **Step 4: Run the tests to verify they pass** -- Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add phase3_5/exploratory/tools
git commit -m "exploratory C084: document checks (units, artifacts, primary, cost, results), committed before X9"
```

---

### Task 9: X9 -- every unit, per native case, reviewed per native case; decision point T3 once

**Files:**
- Create: `phase3_5/exploratory/ARTIFACT_1_native.md`, `phase3_5/exploratory/units.tsv`, `phase3_5/exploratory/E_LOG.md`, `phase3_5/exploratory/cost_log.tsv`
- Modify: `phase3_5/exploratory/disclosure_log.md`, `phase3_5/exploratory/EXECUTION_QA.md`

**Interfaces:**
- Consumes: `P_raw.tsv` (Task 5), the frozen tree (Task 2), `checks.py units|artifact1|cost` (Task 8)
- Produces: `units.tsv` fields `unit_id, obs_ids, native_cases, status, e_gaps, commit`; `ARTIFACT_1_native.md` with one `## NC-nn -- <native name>` section per native case in the fixed format `checks.py artifact1` reads; `cost_log.tsv` as `checks.py cost` reads it

- [ ] **Step 1: Create the four files with their headers**

`ARTIFACT_1_native.md` title `# Artifact 1 -- native description -- EXPLORATORY C084 study`, first paragraph: the label, the revision, and the sentence "No Phase 3 role name appears in this file; it is written in the target's own vocabulary (sealed §9, Artifact 1)." `E_LOG.md` and `cost_log.tsv` likewise headed. Commit: `git commit -m "X9: analysis files opened (no unit analysed yet)"`.

- [ ] **Step 2: For the next unit in `P_raw.tsv` order -- record the session start in `cost_log.tsv`, then recover its native flow**

Read the unit's observation(s) and follow the code from the enumerator outward, anywhere in the frozen tree (sealed §8.6), never outside it (§5.1). Any failure-cause comment met on the way goes to `disclosure_log.md` now. An admissible enumerator or authoritative source met on the way is an inventory protocol failure: XQA entry (clause §7, promotion), its effect on `P_raw` stated, and it is NOT added. Decide which native case(s) this unit resolves into: an existing `NC-nn` if its writers/readers/lifetime are the same code paths, otherwise a new one.

- [ ] **Step 3: Write or extend the `NC-nn` section** in the fixed format (one line per field, the five questions answered in the sealed §6 wording):

```text
## NC-nn -- <native name, the target's own words>
source observation ids: E017-001, E017-002, ...
native state/data involved: ...
writers / creation points: <file:line> ...
updates / invalidation paths: ...
readers / consumption points: ...
lifetime / persistence / reset behavior: ...
relevant transitions: ...
supporting source-code/docs evidence: ...
remaining native-level uncertainty: ...
lineage: C084-own | inherited | not visible in the tree -- <what in the tree shows it, e.g. a "[crispy]" marker comment at file:line, or its absence>
### Sufficiency
Q1 created: <what value/fact is created> -- <file:line>
Q2 written: <where it is written or updated> -- <file:line>
Q3 lifetime: <its lifetime/persistence behavior> -- <file:line>   | or  N/A: <reason> -- <file:line>
Q4 readers: <which transitions/components read or consume it> -- <file:line>
Q5 after consumption: <persists / resets / migrates / disappears> -- <file:line>
Status: RESOLVED        | or  Status: E? (Q3, Q5)
```

An answer without a located citation is a gap (sealed §6.0): the Status becomes `E?` naming the question(s), and `E_LOG.md` gets `## E? <unit_id> (NC-nn)` with the four labelled lines of sealed §6.1.

- [ ] **Step 4: Add the unit's row to `units.tsv`** (`status` = `RESOLVED` only if every native case it resolves into is RESOLVED; else `E?` with the gaps), record the session end in `cost_log.tsv`, run the checks

Run: `python -I phase3_5/exploratory/tools/checks.py units phase3_5/exploratory && python -I phase3_5/exploratory/tools/checks.py artifact1 phase3_5/exploratory`
Expected: exit 0 (the `units` check is allowed to report units not yet in `units.tsv` as `pending` while X9 is open; it fails only on inconsistency).

- [ ] **Step 5: When a native case's section is complete, commit it with the units analysed so far that resolve into it, and hold for review** (§9)

```bash
git add phase3_5/exploratory/ARTIFACT_1_native.md phase3_5/exploratory/units.tsv phase3_5/exploratory/E_LOG.md phase3_5/exploratory/cost_log.tsv phase3_5/exploratory/disclosure_log.md
git commit -m "X9: NC-nn <native name> -- units U..., U...; status ..."
```

Report the SHA. On acceptance, fill `accepted_by` and `accepted_utc` in `cost_log.tsv` (the reviewer's message or the commit that accepted it). On a correction, the correction is a new commit; the superseded sentence stays in place, marked.

- [ ] **Step 6: Decision point T3 -- once, after the FIRST accepted native case** (§7.1)

Compute from `cost_log.tsv`: session hours and elapsed-to-acceptance for NC-01; project both over `P_raw` and, if T2 chose `attempt`, over the KF count. Present the two projections to the owner. Record `XQA-NN -- T3 decision (X9)`: inputs, decision (`continue` or `stop`), grounds. On `stop`: write Artifacts 2 and 3 for the retained case only (Task 10 as written), then Task 11 with the T3 status of §7.1, then Task 13; Task 12 is not executed.

- [ ] **Step 7: Repeat Steps 2-5 until every `unit_id` of `P_raw.tsv` has a `units.tsv` row**

Run: `python -I phase3_5/exploratory/tools/checks.py units phase3_5/exploratory`
Expected: `resolved R / P_raw M`, `E? U / P_raw M`, no `pending`, exit 0. A later unit resolving into an already-accepted case is added to that case and reviewed with the next case's batch (§9).

---

### Task 10: X10 -- Artifact 1 complete, then Artifact 2, then Artifact 3

**Files:**
- Modify: `phase3_5/exploratory/ARTIFACT_1_native.md` (completion commit only)
- Create: `phase3_5/exploratory/ARTIFACT_2_mapping.md`, `phase3_5/exploratory/ARTIFACT_3_judgment.md`

**Interfaces:**
- Consumes: Artifact 1 and `units.tsv` (Task 9); `checks.py artifact1|artifact2|artifact3` (Task 8); the four Phase 3 roles named in §10 (`WorldState`, `MonitorState`, transition-local violation judgment, persistent event provenance -- `phase3/RESULTS_C4.md` §2, `phase3/DESIGN_C4.md` "`EventProvenanceState`")
- Produces: Artifact 2 sections in the format `checks.py artifact2` reads; Artifact 3 with the two headings `checks.py artifact3` reads

- [ ] **Step 1: X10a -- declare Artifact 1 complete**

Run: `python -I phase3_5/exploratory/tools/checks.py artifact1 phase3_5/exploratory && python -I phase3_5/exploratory/tools/checks.py units phase3_5/exploratory` -- Expected: exit 0, no `pending`.
Commit: `git commit -m "X10a: Artifact 1 complete -- <n> native cases, <R> resolved units, <U> E?"`. Hold for review. No sentence of Artifact 2 exists before this commit (§10).

- [ ] **Step 2: X10b -- write `ARTIFACT_2_mapping.md`**, one section per `NC-nn`:

```text
## NC-nn
roles: <native role> -> WorldState | MonitorState | transition-local violation judgment | persistent event provenance | no clean mapping ; one line per native role, with the reason
reasoning: <why the evidence of Artifact 1 supports the outcome below; sealed §6.2 decision logic applied in order>
outcome: R0 | F0 | F1[,F2][,F3]        (every supported finding; none suppressed; sealed §7.0)
competitor: <for R0: the named competing representation, satisfying the external validity semantics of §9 and every unrelated native fact, and the evidence that discriminates against it; sealed §7.1>
positive evidence: <for F3: the native evidence for the alternative boundary; sealed §6.2>
```

An `E?` unit's native case carries no outcome line: it is listed under `## Not classified (E?)` with the unit ids.

Run: `python -I phase3_5/exploratory/tools/checks.py artifact2 phase3_5/exploratory` -- Expected: exit 0 and the per-finding counts.
Commit: `git commit -m "X10b: Artifact 2 -- mapping and outcomes per native case (R0 n, F0 n, F1 n, F2 n, F3 n)"`. Hold for review.

- [ ] **Step 3: X10c -- write `ARTIFACT_3_judgment.md`**

`## Applicability domain`: every class of transition/history that the frozen external validity evidence (the admitted normative observations, if any, and Artifact 1's accept/refuse behaviour) decides, each with the Artifact 1 citation that decides it (sealed §9: inclusion is mechanical, not discretionary). `## Decision procedure`: for each class, the inputs and the verdict (`valid` / `invalid`), then a line `totality: every case inside the domain receives a determinate verdict by the rules above` with any known exception named. No case outside the domain is decided.

Run: `python -I phase3_5/exploratory/tools/checks.py artifact3 phase3_5/exploratory` -- Expected: exit 0.
Commit: `git commit -m "X10c: Artifact 3 -- applicability domain and decision procedure"`. Hold for review.

---

### Task 11: X11 -- `PRIMARY_RESULT.md`, the primary seal

**Files:**
- Create: `phase3_5/exploratory/PRIMARY_RESULT.md`

**Interfaces:**
- Consumes: `checks.py units|artifact2|primary|cost` (Task 8)

- [ ] **Step 1: Write the document** with, in order: the label and revision; the two coverage lines exactly as `checks.py units` prints them; the `E?` list with each unit's gaps and `E_LOG.md` reason in the main body (sealed §8.2); the findings table (`finding | native cases | counting units`) with the `artifact2` counts; the unit<->case map (from `units.tsv`); the correspondence matrix (sealed §4.3 categories: matched, normative-only, enforcement-only, divergent, externally-linked, analyst-inferred, one-to-many/many-to-one) and the collapsed count `C` = number of distinct native cases; the absence/INCONCLUSIVE wording under sealed §8.4 -- `U == 0`: "no counterexample was observed in all preregistered primary slices of this target"; `U > 0`: INCONCLUSIVE with respect to absence/retention -- weakened to the asserted scope if any admitted enumerator is `asserted`; if T3 was `stop`, the §7.1 T3 status instead of coverage and absence wording.

- [ ] **Step 2: Verify**

Run: `python -I phase3_5/exploratory/tools/checks.py primary phase3_5/exploratory && python -I phase3_5/exploratory/tools/checks.py cost phase3_5/exploratory`
Expected: exit 0.

- [ ] **Step 3: Commit -- the primary seal**

```bash
git add phase3_5/exploratory/PRIMARY_RESULT.md
git commit -m "X11: primary-lane result sealed -- resolved R/M, E? U/M; findings R0 n F0 n F1 n F2 n F3 n"
```

Hold for review. Nothing in Tasks 9-11's files is edited after this commit.

---

### Task 12: X12-X14 -- the known-failure lane (only if T2 = attempt), else the N/A record

**Files:**
- Create: `phase3_5/exploratory/KF.md`; `phase3_5/exploratory/kf_items.tsv` (attempt branch only)

**Interfaces:**
- Consumes: `kf_api.py list|first-post|comments` (Task 7); the frozen Artifacts 1-3 (Task 10)

- [ ] **Step 0 (N/A branch):** write `KF.md` with the rule, `L`, the X8 count, the T2 decision and `known-failure lane: N/A -- boundedness failure`; commit `git commit -m "X12: known-failure lane N/A (T2)"`; go to Task 13.

- [ ] **Step 1: X12 -- enumerate**

Run: `python -I phase3_5/exploratory/tools/kf_api.py list fabiangreffrath/crispy-doom <labels...> phase3_5/exploratory/kf_items.tsv`
Expected: `kf_items.tsv` with the ids and the UTC timestamp; its count compared with X8's in `KF.md` (a difference recorded, §8). Commit the id list before any item is opened: `git commit -m "X12: KF items enumerated -- <c2> ids (X8 count <c>)"`.

- [ ] **Step 2: X12 -- KF-1 per item, in id order**

Run: `python -I phase3_5/exploratory/tools/kf_api.py first-post fabiangreffrath/crispy-doom <number>` (never `comments` at this step). Append to `KF.md`:

```text
## KF item #<number>
disclosure: fields seen = title, labels, state, created_at, body; cause leakage = yes|no -- <what leaked, if yes>
symptom: expected = ... ; observed = ... ; reproduction = ... | none documented ; affected version = ... | not stated
```

If the body carries no symptom, fetch comments one at a time until one appears; log each comment read under `disclosure` (§5.2).

- [ ] **Step 3: X13 -- KF-2 per item, from the frozen artifacts only**

Append under the item:

```text
KF-2 representability: representable | not representable -- <which Artifact 1 case / Artifact 2 role, or what is missing>
KF-2 domain: in-domain concordant | in-domain DISCORDANT | in-domain indeterminate | out-of-domain -- <Artifact 3 class and verdict>
KF-2 attribution: measurement insufficiency | F2-like architectural limitation | judgment-layer limitation | reproduction/environment issue | scope mismatch
native replay: N/A (declared in advance, §8)
```

Commit per item: `git commit -m "X13: KF item #<n> -- KF-1 symptom, KF-2 <domain result>"`. After the last item: `git commit -m "X13: KF-2 sealed -- <k> items: concordant a, DISCORDANT b, indeterminate c, out-of-domain d"`. Hold for review.

- [ ] **Step 4: X14 -- KF-3 per item**

Run: `python -I phase3_5/exploratory/tools/kf_api.py comments fabiangreffrath/crispy-doom <number>`; read linked commits/PRs (fetched individually) and third-party material as needed (§5.3). Append `KF-3: agreement | partial agreement | different causal explanation | previously hidden native information | scope mismatch | insufficient external causal evidence -- <comparison>`; where Artifact 2 was wrong and Artifact 3 inherited it, one `coupled mapping->judgment finding:` line. Nothing above the `KF-3:` lines is edited. Commit: `git commit -m "X14: KF-3 comparison -- <k> items"`.

---

### Task 13: X15 -- `RESULTS.md`, the README pointer, memory

**Files:**
- Create: `phase3_5/exploratory/RESULTS.md`
- Modify: `README.md` (one pointer line in the "Where to read" block and one sentence in "Status")

**Interfaces:**
- Consumes: every file above; `checks.py results|primary|cost` (Task 8)

- [ ] **Step 1: Write `RESULTS.md`** in the consolidate-and-seal pattern of `phase3_5/RESULTS.md`: title `# Phase 3.5 Exploratory Study (C084 Crispy Doom) -- RESULTS -- EXPLORATORY`; first paragraph: the label, anti-goal 1 of §3 quoted in full ("The exploratory result used as if it were Run 2's result ..."), the revision; then `## 1 ..` sections as §12 lists them -- the twelve sealed §14 items as `### 14.1` .. `### 14.12` (14.1 points at `phase3_5/RESULTS.md` and states the two substitutions of §2.1); the owner's reason for the target; the limitations L1-L9 plus the sealed §13's five; `## Inputs to Run 2` with the six bullets of §12 item 4 (snapshot as executed; inventory counts per class and per EN criterion with the time it took; cost distribution per unit and per native case from `cost_log.tsv`; KF-0 as applied with `L`, count and T2; the T decisions from XQA; every XQA that chose a reading); `## What this study does not establish`, ending with the sealed §14 closing rule quoted.

- [ ] **Step 2: Verify every number from source**

Run: `python -I phase3_5/exploratory/tools/checks.py results phase3_5/exploratory && python -I phase3_5/exploratory/tools/checks.py primary phase3_5/exploratory && python -I phase3_5/exploratory/tools/checks.py cost phase3_5/exploratory`
Expected: exit 0. Then the owner's four drafting checks by hand (recompute; referents; superseded claims; neighbours), as a non-record procedure.

- [ ] **Step 3: Commit RESULTS**

```bash
git add phase3_5/exploratory/RESULTS.md
git commit -m "X15: exploratory C084 RESULTS sealed"
```

- [ ] **Step 4: README pointer and memory**

Add to README's "Where to read" block the line `phase3_5/exploratory/RESULTS.md     exploratory C084 study (hand-chosen target; not the Phase 3.5 result)` and one sentence to "Status" naming the study, its label and its commit. Run `git diff --stat README.md` -- Expected: README.md only, a few lines. Commit: `git commit -m "README: pointer to the exploratory C084 study"`. Update the project memory file with the seal SHA and the Run 2 inputs' location.

---

## Self-review notes

- Spec coverage: §2.3 firewall -> Global Constraints and Task 13 (README only); §4 -> Tasks 1-2; §5 -> Global Constraints, Task 4 Step 1 (disclosure log), Task 12 Steps 2/4; §6 -> Tasks 3-5; §7 and §7.1 -> Tasks 6, 7 (T2), 9 Step 6 (T3); §8 -> Task 7; §9 -> Tasks 8-9; §10 -> Task 10; §11 -> Task 12; §12 -> Task 13; §13 -> Task 13 Step 1; §14 cadence -> every task's commit-and-hold step; §15 builder items -> Tasks 1, 3, 5, 7, 8; §16 items are honoured where each applies (item 1 Task 2, 2 Task 2, 3 Task 2, 4 Task 1, 5 Global, 6 Task 3, 7 Task 4, 8 Task 10, 9 Task 6, 10 Task 7, 11 Task 12, 12 Task 9, 13 Task 1, 14 Task 2, 15 Task 4, 16 Task 7 last line, 17 Tasks 7/12, 18 Task 9, 19 Tasks 6/7/9, 20 Task 9).
- One departure from the spec's text, made visible rather than silent: K1 widened to any element type (Task 3), approved with this plan and recorded as XQA-01 at X4b.
- Names used across tasks: `cand_id`/`enum_id` (Tasks 3-5), `obs_id` (Tasks 5, 9), `unit_id` (Tasks 5, 8, 9, 11), `NC-nn` (Tasks 8-12), `checks.run(sub, dir)` (Tasks 8-13), `fetch=` injection (Tasks 1, 7).
