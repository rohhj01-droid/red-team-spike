# Phase 3.5 Run 2 -- Screening Record Contract

Status: committed before any Run 2 tool runs and before the frame is
re-fetched (preregistration design
`docs/superpowers/specs/2026-10-29-phase3-5-run2-preregistration-design.md`,
sealed `4c7e315`, Section 12 step R2). This contract REUSES Run 1's
`phase3_5/SCREENING_PROTOCOL.md` -- its two ledger levels, gate order and
first-fail stop, the UR / E2-REP distinction, the E2-REP network-access
contract, its two post-seal amendments (the asymmetric existential gates;
survivor inventory completeness), its controlled vocabularies, file
schemas, evidence log format and invariants -- and ADDS the rules below.
Each addition names the Run 1 QA entry it answers. Nothing here changes
the sealed methodology (`401924d`); Section 10 records the one place a
sealed rule is executed in a different form, with its reason.

A rule found missing while screening is an RQA entry in
`EXECUTION_QA.md` naming the gap and the reading taken; it applies from
that item on, and the items already decided are listed as decided under
the earlier reading (design anti-goal 6). No verdict is reopened in
flight.

---

## 1. What the tools do and what the analyst does

Every ledger row, starting-point row, observation row, exposure line and
evidence block is produced by the committed tools under `tools/` from the
frozen metadata and the recorded HTTP observations. The analyst's only
inputs are:

```text
witness_bNN.tsv         per screening batch: quoted, located witnesses
                        (Section 9.5), which the tools validate against
                        the fetched surfaces and turn into gate decisions
quoted_verdicts.tsv     per survivor: quoted EN verdicts for the rows the
                        frozen grammar leaves undecided (design Section 6)
```

The analyst is an AI model operating the tools; the owner reviews each
batch and each survivor (Section 11).

## 2. Frozen metadata and its resolution (QA-39, QA-40)

The frozen metadata of a frame item is, from the frozen ports tree
(`ports.tar.gz`, SHA256
`937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db`):

```text
<port>/Makefile       HOMEPAGE, SITES, SITES.<group>, GH_ACCOUNT, GH_PROJECT,
                      GH_TAGNAME, GH_COMMIT, DIST_TUPLE, MODULES, DISTNAME,
                      PKGNAME, COMMENT, CATEGORIES
<port>/distinfo       the distfile names and checksums (identity of the
                      fetched archive, not a starting point)
<port>/pkg/DESCR      the port's description text
```

plus the values the frozen infrastructure resolves from them. The
resolver (`tools/metadata.py`) applies exactly these mechanisms, in this
order, and records per field the explicit line or the mechanism:

```text
HOMEPAGE   1. an explicit HOMEPAGE line
           2. else, with GH_ACCOUNT and GH_PROJECT both set
              (infrastructure/mk/bsd.port.mk:1280,1295):
                HOMEPAGE ?= https://github.com/${GH_ACCOUNT}/${GH_PROJECT}
           3. else, with a DIST_TUPLE whose site template is github
              (infrastructure/mk/dist-tuple.port.mk:42-43,
               infrastructure/db/dist-tuple.pattern):
                TEMPLATE_HOMEPAGE = <site><account>/<project>
                SITES.github = https://github.com/
                -> https://github.com/<account>/<project>
              (gitlab and codeberg templates likewise, from the pattern
               file's SITES.<template> line)

SITES      1. explicit SITES and SITES.<group> lines, with ${SITE_*}
              macros expanded from
              infrastructure/templates/network.conf.template and the
              `${NAME:=suffix}` modifier expanded as "each word of NAME
              with suffix appended"
           2. else, with GH_ACCOUNT and GH_PROJECT (bsd.port.mk:1280-1301):
                GH_TAGNAME set -> https://github.com/<a>/<p>/archive/refs/tags/<tag>/
                GH_COMMIT set  -> https://github.com/<a>/<p>/archive/
                then SITES ?= ${SITES_GITHUB}          (the BARE SITES is set)
           3. a DIST_TUPLE port sets SITES.<template> and never the bare
              SITES (QA-40); its repository root enters the starting-point
              set through the tuple itself (Section 4), not through SITES
```

Continuation lines (a trailing backslash) are joined before parsing;
`CATEGORIES` never continues (FRAME_ENUMERATION.md) and the resolver does
not rely on that. The resolver is not a `make` evaluation.

**Declared modules: none.** `DECLARED_MODULES = []`. A port whose
`MODULES` line names anything (Run 1 met `cpan`), or whose `HOMEPAGE` or
`SITES` still contains an unexpanded `${...}` after the macro table is
applied, is `UNRESOLVED` at UR with `protocol_issue_code =
PI-METADATA-UNRESOLVED` (Section 7). Nothing is guessed for it.

## 3. Upstream resolution, identity, and E1

UR resolves a frame item to one external system by a mechanical identity
key computed from the resolved metadata (analyst's call, recorded here):

```text
identity key, first that exists:
  1. the normalized repository root (Section 5 normalization) denoted by
     GH_ACCOUNT/GH_PROJECT, or by a DIST_TUPLE whose template is github,
     gitlab or codeberg
  2. else the normalized HOMEPAGE
  3. else, for a resolved SITES URL whose class (Section 5) is
     distfile-location or project-page:
     https://<host>/<first path component>

upstream_resolution
  PASS            exactly one key
  FAIL_NONE       no key (no HOMEPAGE, no repository root, no SITES URL of
                  an identifying class -- a bare mirror host such as
                  distfiles.openbsd.org identifies nothing)
  FAIL_AMBIGUOUS  two repository roots naming different
                  (host, account, project) -- e.g. a GH pair and a
                  DIST_TUPLE that disagree
  DUPLICATE       the key equals an earlier frame item's key (case-folded)
  UNRESOLVED      PI-METADATA-UNRESOLVED (Section 2); a fifth value added
                  to Run 1's vocabulary for this run
```

A HOMEPAGE on a different host from the repository root does not make
the item ambiguous: a project page and its repository are the normal
shape, and both enter the starting-point set.

**E1 (external authorship)**: PASS unless the identity key's host and
first path component are this project's own (`github.com/rohhj01-droid`),
in which case `E1-NONEXTERNAL`.

## 4. Starting points (QA-38)

The E2-REP starting-point set of an item is computed mechanically:

```text
the resolved HOMEPAGE                                        source HOMEPAGE
each resolved SITES URL                                      source SITES
each resolved SITES.<group> URL                              source SITES.<group>
the repository root https://<site>/<account>/<project>
  denoted by GH_ACCOUNT/GH_PROJECT                           source GH
  or by a DIST_TUPLE (github, gitlab, codeberg templates)    source DIST_TUPLE
```

**Reading B (QA-38):** an identifier that appears only inside a URL's
path or query -- an account or project name read off a
`/releases/download/` URL, say -- is NOT a starting point. Locations come
from structured fields only. A URL present twice (HOMEPAGE equal to the
GH root) is one surface with two sources.

## 5. Surface classes, declared before any URL is requested (QA-31, QA-37)

Normalization (sealed Section 2): the HTTPS form; scheme and host
lowercased; no credentials, query or fragment; no trailing slash; no
trailing `.git`. The path's case is kept.

Every starting-point URL is classified BEFORE it is requested, by the
first matching row of this table (`tools/surfaces.py` carries it as data,
with a test per row). `<a>` and `<p>` stand for one path component each.

```text
class              host                              path
repository-root    github.com                        /<a>/<p>
                   gitlab.com, gitlab.<any>          /<a>/<p>  (also /<a>/<b>/<p>, no /-/ segment)
                   codeberg.org                      /<a>/<p>
                   sr.ht, git.sr.ht                  /~<a>/<p>
                   bitbucket.org                     /<a>/<p>
                   salsa.debian.org                  /<a>/<p>
                   git.<any>, code.<any>             /<a>/<p>
                   any host                          a path ending in .git
                   any host                          /cgit/<p> or /git/<p>
release-assets     github.com                        /<a>/<p>/releases..., /<a>/<p>/archive..., /<a>/<p>/tags..., /<a>/<p>/downloads...
  (FORBIDDEN)      gitlab.com, gitlab.<any>          .../-/releases..., .../-/archive..., .../-/tags..., .../uploads/...
                   codeberg.org                      /<a>/<p>/releases..., /<a>/<p>/archive...
                   bitbucket.org                     /<a>/<p>/downloads...
distfile-location  downloads.sourceforge.net, prdownloads.sourceforge.net, *.dl.sourceforge.net   any
                   sourceforge.net                   /projects/<p>/files..., /project/<p>/...
                   ftp.gnu.org, ftpmirror.gnu.org    /gnu/...
                   download.savannah.gnu.org, download.savannah.nongnu.org   /releases/...
                   cpan.metacpan.org                 /authors/id/..., /modules/by-module/...
                   www.cpan.org, cpan.org            any
                   distfiles.openbsd.org, ftp.openbsd.org, *.openbsd.org   .../distfiles/...
                   files.pythonhosted.org, pypi.io, pypi.org   /packages/...
                   crates.io, static.crates.io       /api/v1/crates/..., /crates/...
                   registry.npmjs.org                any
                   hackage.haskell.org               /package/...
                   ftp.debian.org, deb.debian.org    /debian/pool/...
                   mirrors.kernel.org, www.kernel.org   any
                   any host                          a path ending in .tar.gz .tgz .tar.bz2 .tar.xz .tar.zst .zip .7z
```

A URL matching no row is `unmatched` and is requested ONCE (one GET of
the URL itself, nothing followed) and classified by the response:

```text
an archive file (Content-Type application/x-gzip, application/zip,
  application/x-xz, application/x-bzip2, application/zstd,
  application/octet-stream with an archive extension)      distfile-location
a directory listing (text/plain, or HTML whose <title> starts
  with "Index of" or whose body is an <a>-only listing)    distfile-location
any other HTML (text/html)                                 project-page
anything else, or no definitive response                   unclassifiable
```

**`release-assets` is the only forbidden class** (the sealed contract's
"releases"): a code host's release, tag, archive and download areas,
which render release notes beside the assets. It is never requested; a
starting point of that class is accounted for as `closed-by-class`.
**`distfile-location` is NOT forbidden** (analyst's call settling
QA-37): a directory that serves source archives by project is observed
under QA-27's standing rule, for the one purpose of confirming that a
source distribution exists there -- what a candidate without a repository
needs for E2-REP's "source distribution" form. Nothing in such a
directory is opened beyond its listing.

A redirect is followed and its chain recorded; the FINAL URL's class
decides what may be read. A request whose final URL falls in the
forbidden class is accounted for as `closed-by-class` after that one
request, which is logged as the request that revealed the class.

## 6. Step-2 authorization and designation (QA-35, QA-36)

Allowed navigation is the sealed three steps: (1) the upstream official
landing/project page, (2) a link that page explicitly exposes, (3) the
metadata/root surface of the official source repository reached.

**Step 2 is authorized by the visible label of the link itself** -- its
anchor text, its `title` attribute, or its `aria-label` -- containing, as
a whole word after Unicode NFKC normalization and case folding, one of:

```text
Source   Code   Repository   Development
```

or one of these translations: German `Quellcode`, `Quelltext`, `Code`,
`Repositorium`, `Entwicklung`; French `source`, `code source`, `dépôt`,
`développement`; Spanish `código`, `código fuente`, `repositorio`,
`desarrollo`; Portuguese `código`, `repositório`, `desenvolvimento`;
Italian `codice`, `sorgente`, `repository`, `sviluppo`; Russian
`исходный код`, `исходники`, `репозиторий`, `разработка`; Japanese
`ソース`, `ソースコード`, `リポジトリ`, `開発`; Korean `소스`, `소스 코드`,
`저장소`, `개발`. A heading over a link, a sentence around it, an image
without a label, or the URL's shape authorizes nothing. `Barcode` does
not contain the word `Code`.

**Designation is a witness, not a permission.** A designation signal is a
sentence on an observed surface saying the location is the project's
source: it contains `official`, `canonical`, `primary`, `main
repository`, `our repository`, `the source`, or marks a `mirror`. It
supports the gate's PASS (quoted in a `designation` witness row); it
never authorizes following a link that the label rule does not.

**Owner-controlled repository metadata designates only in these
fields** (QA-36): the hosting platform's repository description field,
its website field, and a primary/mirror marking in either. The repository
name and owning account identify; they do not designate. The repository's
README body is not read (sealed contract); what the landing page rendered
of it goes to `exposure_log.md` and does no work.

**The external target identifier** is the repository's name (the last
path component of the canonical location) when the canonical location is
a repository, else the first segment of the project page's `<title>`;
the `identifier` witness row quotes where it appears.

## 7. How E2-REP completes (QA-31, QA-41, QA-42)

Every admitted starting point is accounted for in exactly one state:

```text
observed          requested; a definitive response was recorded
closed-by-class   release-assets, never requested (or revealed by its
                  final URL after one request)
unclassifiable    unmatched, requested once, response of no listed kind
unreachable       PI-TRANSPORT-INDETERMINATE after two recorded retries
```

**PASS** requires all of: every admitted starting point not
`closed-by-class` is `observed` (QA-27 / QA-41: necessity is the standing
rule); exactly one designated canonical source location with a stable
URL and exactly one external target identifier are established on the
observed surfaces (a `designation` row, an `identifier` row and a
`source-tree` row -- the repository root or archive listing shows a
source tree); the navigation stayed within the three steps.

**A failure code needs positive evidence on an observed surface:**

```text
E2REP-NO-SOURCE                      the designated location was observed and
                                     holds no source tree (an empty repository,
                                     a page without any source archive)
E2REP-NO-SINGLE-CANONICAL-LOCATION   two designations observed naming different
                                     locations, with no primary/mirror marking
E2REP-NO-STABLE-URL                  the designated location returned a definitive
                                     404 / 410 (not a transport failure)
E2REP-NO-SINGLE-TARGET-ID            the observed surfaces name no single system
                                     (a page listing several systems without
                                     naming this one as delimited)
```

**Otherwise UNRESOLVED**, with Run 1's two protocol-issue codes or these
three added for this run:

```text
PI-STARTING-POINTS-CLOSED    every admitted starting point is closed-by-class;
                             nothing could be observed (QA-31's open case)
PI-UNCLASSIFIABLE-SURFACE    an admitted starting point is unclassifiable
PI-METADATA-UNRESOLVED       Section 2 (this one lands at UR)
```

`evidence_role` takes four values: `official-project-page`,
`official-source-location`, `admitted-starting-point` (a surface
admitted as a starting point that is neither, such as an account page or
a SITES directory), `distfile-location`.

Transport, exposure and the two times are Run 1's rules (the network
contract): two recorded retries, then `PI-TRANSPORT-INDETERMINATE`;
incidental content logged and unused; the E2-REP observation time is
never the snapshot time (Section 10).

## 8. The gates past E2-REP: surfaces and readings

E2-RULE, E3 and E4 are decided inside the pinned tree (Section 10) under
Run 1's amendment: a positive-only PASS with a quoted, located witness;
otherwise UNRESOLVED, never FAIL, with the surfaces read listed in an
`absence-survey` row. Reading is bounded to these surfaces, opened in
this order, and stops at the first witness:

```text
E2-RULE   README* at the root; files under docs/ or doc/ named index.*,
          README*, rules*, manual*, spec*, format*, design*, with
          extensions .md .rst .txt .adoc .html; man/** ; CONTRIBUTING*,
          HACKING*; the NAMES (not the contents) of entries under test/,
          tests/, t/, spec/
          witness kind `validity`: a quoted statement of the form
          "under X the result must be Y" / "Z is invalid" with file:line
E3        the E2-RULE surfaces, plus the source files the E2-RULE
          witness names (by path or by the symbol it quotes, located by
          grep), opened only at the cited region
          witness kind `stateful`: a quoted validity question that
          depends on earlier state or time, with file:line
E4        the candidate rows `inventory.enumerators` (exploratory tool)
          produces for the pinned tree, decided by the frozen grammar
          `tools/en_verdicts.py`; for the quoted ADMIT, the enumerator's
          defining lines and its consulting path
          witness kind `enumerator` (the identification, EN2) and
          `refusal-path` (EN4), both with file:line; PASS iff one row
          becomes ADMIT through `en_verdicts.apply_quoted`
```

The candidate-screening firewall (sealed Section 2) binds every reading:
nothing read at a gate is used beyond that gate's question; no root
cause, fix diff, information-flow trace or architectural mapping is
formed; no "interesting-looking validity behaviour" picks units.

## 9. File schemas and vocabularies

Run 1's schemas stand (`SCREENING_PROTOCOL.md`, "File schemas"), with
these additions.

### 9.1 `screening_frame_items.tsv` (128 rows at the end)

Run 1's columns, plus `starting_points_ref` (the item's rows in
`starting_points.tsv`, by rank) and `pin_ref` (`inventory/<cid>/pin.json`
or `NONE`). `upstream_resolution` adds `UNRESOLVED`.

### 9.2 `screening_candidates.tsv`

Run 1's columns, with `overall` in `ELIGIBLE | REJECTED | UNRESOLVED`,
plus `decided_by_grammar` (`<n> catalogue / <m> quoted`, filled at the
inventory stage) and `class_sensitivity_ref`
(`inventory/<cid>/class_sensitivity.md` or `PENDING_INVENTORY`).
`completeness_class` is `PENDING_INVENTORY` until Section 11's inventory
step, then `A` or `B`.

### 9.3 `starting_points.tsv`

```text
frame_rank  url  source  klass  action  final_url  final_class  observed_at_utc
http_status  evidence_role  note
```

`action` in `observed | closed-by-class | unclassifiable | unreachable |
not-reached` (the gate stopped before this point was due).

### 9.4 `observations.tsv` (one row per HTTP request, retries included)

```text
observed_at_utc  frame_rank  step  requested_url  final_url  http_status
redirect_chain  attempt  outcome  body_ref
```

`step` in `UR-classify | E2REP-1 | E2REP-2 | E2REP-3 | pin`; `outcome` in
`ok | definitive | transport`; `body_ref` names the stored body under
`target/bodies/<rank>/<n>.bin` (git-ignored) that the analyst reads.

### 9.5 `witness_bNN.tsv` (the analyst's input per batch)

```text
frame_rank  candidate_id  gate  kind  surface  location  quote
```

`gate` in `E2-REP | E2-RULE | E3 | E4`; `kind` in `designation |
identifier | source-tree | validity | stateful | enumerator |
refusal-path | absence-survey`; `surface` is a URL from
`starting_points.tsv` / `observations.tsv` or a path in the pinned tree;
`location` is `final_url#<css-less text anchor>` for a page or
`file:line` for a tree file; `quote` is text that must occur verbatim in
the stored body or the file, or the tool rejects the row.

### 9.6 `screening_cost.tsv`

```text
batch  frame_rank  gate_reached  session_s  review_s  conditions
```

`conditions` is the constant `analyst=AI model; session=first read of the
batch to the batch commit; review=commit to the owner's 통과`.

### 9.7 `exposure_log.md`

One line per incidental exposure: `| observed_at | rank | surface | what
was rendered (README excerpt, release note, issue count) | used: no |`.

### 9.8 Evidence blocks

Run 1's EV format (`## EV-C<id>-<GATE>-<nn>`, Candidate, Gate, Source,
Observed, Inference, Decision; `Surfaces` and `Necessary because` lines
for negative components), generated by the tools from the rows above and
the witness table; `Observed` holds only quoted text and recorded
responses, `Inference` the rule of this contract that the decision
applies.

## 10. The snapshot rule as executed (QA-28, XQA-01) -- a declared deviation

The sealed snapshot rule names "the state of the designated canonical
source location at the enumeration execution timestamp". Run 1 found it
cannot be executed after the fact (QA-28), and the exploratory study's
check of the sealed instant returned a commit other than the pinned one
(XQA-01). Run 2 pins **at observation time**, at the moment E2-REP
passes, and records the deviation here, once:

```text
repository candidate
  default branch name and its tip commit as a full hash
    (git ls-remote --symref <url> HEAD), with observed_at_utc
  fetch of that hash: git init; core.autocrlf=false; fetch --depth 1
    origin <hash>; checkout --detach FETCH_HEAD   -> target/<cid>/tree
  the archive at that hash (the host's archive URL for the hash): byte
    count, sha256, entry count (listed, not extracted)
  ten digests: the ten largest files with extensions
    .c .h .m .py .cpp .hpp .cc .rs .go .js .ts .java .lua, ties by path,
    each as (relative path, bytes, sha256)
distribution candidate
  the designated archive: byte count, sha256, entry count; the ten
  digests over its extracted tree
record
  inventory/<cid>/pin_record.md (the exploratory pin record's form) and
  inventory/<cid>/pin.json
```

Every later step is defined against that hash. The enumeration execution
timestamp of Run 2's frame is provenance only.

## 11. Batches, review, corrections, decision points

Batch k (k = 1..16) is frame ranks 8k-7 .. 8k in the frozen order. One
commit per batch, holding the ledgers, the starting-point and observation
rows, the exposure lines, the cost rows, the witness table and
`screening_evidence_bNN.md` (the eight rows and their evidence blocks).
The owner reviews the batch document and answers 통과, or names the rank
that fails review; that item is corrected in its own commit with Run 1's
retraction convention (the earlier wording kept in place, marked
`[CORRECTED under review: ...]`), and the other seven stand. Decision
point D1 follows batch 1 and D2 the sixteenth batch (design Section 9):
inputs recorded in RQA, the owner's decision in their words, continue only
on `continue`.

The survivor inventory (design Section 6) is one commit per survivor,
reviewed by the owner with the class-sensitivity table first; the
selection is one commit; D3 follows it.

Costs: `screening_cost.tsv` rows are written at each batch commit (session
seconds) and completed at the owner's acceptance (review seconds), under
the conditions stated in 9.6.

## 12. Exposure before this contract

The analyst has read, in Run 1 and in the exploratory study, the records
of candidates C001-C094 (their frozen metadata and screening evidence),
the whole tree of C084 and its tracker, and Run 1's QA entries. This is
declared as a limitation (design R-L3) and is why every rule above is
mechanical or quotation-bound: nothing in the analyst's memory of a
candidate may enter a verdict except through a quoted, located witness
that the tools verify against the surface.
