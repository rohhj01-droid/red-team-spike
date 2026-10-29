# Phase 3.5 Run 2 -- preregistration design

Status: SEALED (R0). Written 2026-10-29, after the exploratory C084
study was sealed and pushed (`35255d6`); builder-checked the same day,
with the owner's four answers (Sections 6, 8, 9, 11) incorporated;
approved by the owner 2026-10-29 ("승인, 봉인하고 계획으로 넘어가") and
sealed by this docs-only commit before any Run 2 tool, contract or
record exists. A change to a rule here after this commit is an RQA
entry, never an edit.

This document preregisters the second run of the Phase 3.5 screening
approach: the same frozen frame, re-screened from rank 1 under rules
closed before any candidate is seen, an inventory procedure that can
actually decide the completeness class, and the analysis lane as the
exploratory study executed it. Its purpose is the confirmatory result
the sealed methodology was designed for -- an answer to Phase 3's
question ("do these boundaries appear when the system under test was
defined by someone else?", `phase3/RESULTS_C4.md` Section 6) from a
system a rule chose, not a hand.

It supplies, for Run 2, what Run 1's record said a Run 2
preregistration must supply (`phase3_5/RESULTS.md` Section 9: QA-19,
QA-28, QA-31, QA-35, QA-36, QA-37, QA-38, QA-39, QA-40, QA-41, QA-42,
QA-43) and uses the six inputs the exploratory study produced for it
(`phase3_5/exploratory/RESULTS.md` Section 5). It changes nothing in
the sealed methodology
(`docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`,
`401924d`); where a sealed rule proved unexecutable, the executable
form is stated here as a declared deviation with its reason, in the
QA-28 / XQA-01 manner.

Decisions marked **(owner)** are the owner's, quoted. Decisions marked
**(analyst's call)** were made while writing this document and can be
overturned by the owner before sealing.

---

## 1. Why this run exists, and what success is

**(owner)** The result the owner wants: "Phase 3 질문에 외부 시스템으로
답한 확정 결과를 포트폴리오에 넣는 장면" -- a confirmatory answer to
Phase 3's question, obtained on an external system, in the portfolio.

Run 1 (2026-08) reached step 3 of the sealed Section 15 and stopped:
28 of 128 frame items in, four candidates were eligible and the
ranking's first step, the enumeration completeness class, was
undecidable, because the class needs a complete inventory and no
inventory procedure had been preregistered (QA-19). Screening then
continued to 96 of 128 under rules that were being discovered as it
went (QA-30 to QA-42), with retractions moving eight of eleven ELIGIBLE
candidates to UNRESOLVED, and was terminated by decision (QA-43). The
exploratory C084 study (2026-10-29) then executed the analysis lane on
one hand-chosen candidate and produced, as inputs for this run, an
executed snapshot procedure, an executed inventory procedure with its
cost, a per-native-case cost distribution, a KF-0 rule applied to a
real tracker, and a termination rule that was preregistered and then
executed.

**(owner)** On what to change: "검토가 빡빡해지면서 한 건에 15커밋
걸리던 거" -- the per-item cost under review. The analyst's reading of
the record, which the owner did not dispute: rank 92 took fifteen
commits not because it was hard but because the rules were being found
during execution and each finding reopened earlier verdicts under
review. Hence the two changes this document makes: every rule is closed
before the first candidate is seen (Section 4), and a candidate's record
is produced in one pass by committed tools and reviewed as a table
(Section 5), the way the exploratory study's native cases were.

Success for this run is one of these reported outcomes, each a defined
result of the preregistered procedure:

```text
confirmatory  a target selected by the rule; the analysis lane run to
              its seal; RESULTS with the sealed Section 14 items
no target     the frame's 128 items screened, no eligible candidate, or
              the class boundary undecidable under Section 6 -- reported
              as the run's outcome (sealed Section 2: no re-framing)
stopped       a decision point exercised to stop (Section 9) -- reported
              as a partial screening with the claims Section 9 allows
```

A fourth outcome is a failure of the run: anything in Section 3's
anti-goals.

## 2. Goals, non-goals, anti-goals

**Goals.**

1. Re-screen the frozen frame from rank 1 under this document's rules,
   to the sealed budget of 128 or a preregistered stop.
2. For every candidate surviving E1-E4, freeze the candidate-level
   inventory with the exploratory study's procedure and decide the
   completeness class by that procedure (Section 6).
3. Select by the sealed ranking and tie-break, with the non-blindness of
   C084 and C065 declared, never acted on (Section 7).
4. Run the analysis lane on the selected target exactly as the
   exploratory study executed it, with that study's readings adopted as
   rules (Section 8), and write RESULTS from a committed generator with
   a regeneration check from the first draft.
5. Leave the sealed Phase 3.5 record and the sealed exploratory record
   byte-identical; Run 2 writes only under `phase3_5/run2/`, plus one
   README pointer.

**Non-goals.**

- No change to the sealed methodology; no second frame; no survey of
  several targets.
- No simulator, no search, no executable-witness claim (sealed Section
  10).
- No reuse of Run 1's verdicts as inputs **(owner)**: "새 규칙으로
  1번부터 다시 봐야지". Run 1's ledgers stay as Run 1's record and are
  compared with Run 2's after Run 2's screening is complete (Section 10).
- No reuse of any exploratory artifact's content for the selected
  target, even if the rule selects C084 (Section 7).

**Anti-goals** -- outcomes that make the run a failure even if every
step completes.

1. **A rule tuned toward or away from the exploratory findings.** Every
   rule below is derived from the sealed text and from Run 1's QA
   entries, which were written before the exploratory study; the
   exploratory study contributes procedures and costs, never a
   preference about what a target should show. A reviewer should be
   able to find, for each rule, the QA entry or sealed clause it answers.
2. **The exploratory result presented as, or merged into, this run's
   result** (the exploratory design's anti-goal 1, binding here).
3. **A target chosen by hand**, including by excluding a candidate by
   hand (L8 of the exploratory design) or by adjusting the tie-break
   after seeing the eligible set.
4. **The lane shrunk after it started**: every unit of the frozen
   `P_raw` analysed, every KF item attempted once T4 says so.
5. **A partial screening reported as coverage of the frame**: a stop
   before 128 forfeits the frame's eligible-set claim (Section 9).
6. **A verdict reopened by a rule found during execution.** A rule
   found missing during Run 2 is an RQA entry naming the gap and the
   reading taken, applied from that point on, with the candidates
   already decided listed as decided under the earlier reading -- never
   re-screened in flight. (The reading's effect on them is reported at
   the end, Section 10.)

## 3. The frame, re-executed

The frame is the sealed one (sealed Section 2, "The sealed frame
values"), unchanged:

```text
enumeration source   OpenBSD 7.9 ports.tar.gz,
                     https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz
membership identity  SHA256 937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db,
                     56386078 bytes -- verified against the retrieved
                     bytes and against OpenBSD's published SHA256 file
                     before any extraction
query                every port whose CATEGORIES include `games`
granularity          one frame item per port directory
order                ascending UTF-8 byte order of the port directory path
budget               128 frame items (sealed; not re-set here, see 9)
```

The artifact is retrieved again (Run 1's copy was not kept, QA-43),
hashed before extraction, and the enumeration re-executed with the
committed tool `tools/frame.py`; its result must equal Run 1's
`screening_set_128.txt` item for item, or the run stops with an RQA
entry (membership is fixed by the hash, so a difference is a tool
defect, not a frame change). The new enumeration execution timestamp is
recorded as provenance; it is **not** the snapshot instant (Section 7.3).

## 4. Screening rules, closed before the first candidate

Gate order, first-fail stop, gate states, the ledger schemas and the
controlled vocabularies are Run 1's (`phase3_5/SCREENING_PROTOCOL.md`,
with both post-seal amendments), reused as the Run 2 contract and copied
into `phase3_5/run2/SCREENING_CONTRACT.md` with the additions below.
Each addition names the QA entry it answers.

### 4.1 Frozen metadata and its resolution (QA-39, QA-40)

The frozen metadata of a frame item is the port's `Makefile`, `distinfo`
and `pkg/DESCR` as they stand in the frozen tree, **plus the values the
frozen infrastructure resolves from them**: `HOMEPAGE` and `SITES`
defaulted from `GH_ACCOUNT` / `GH_PROJECT` / `GH_TAGNAME` / `GH_COMMIT`
(`bsd.port.mk`) and from `DIST_TUPLE` (`dist-tuple.port.mk`). A
committed resolver (`tools/metadata.py`) applies those two mechanisms'
rules, as read from the frozen infrastructure files, to the Makefile
text and records, per field, the explicit line or the mechanism that
produced the value. A port whose `SITES` or `HOMEPAGE` comes through any
other module (Run 1 met `cpan`) is resolved only if that module is in
the resolver's declared list; otherwise UR records
`PI-METADATA-UNRESOLVED` and the item is UNRESOLVED at UR. The resolver
is not a `make` evaluation; its declared list and its limits are stated
in the contract before the first item.

### 4.2 Starting points (QA-38)

The E2-REP starting-point set is computed mechanically from the frozen
metadata: the resolved `HOMEPAGE`; each resolved `SITES` URL; the
repository root that `GH_ACCOUNT`/`GH_PROJECT` or a `DIST_TUPLE`'s
(host, account, project) components denote. **(analyst's call,
QA-38's reading B)** An identifier that appears only inside a URL's
path or query (an account or project name read off a `/releases/download/`
URL, say) is **not** a starting point; locations are taken from
structured fields only. Reason: a rule over URL shape is the move QA-25
refused, and structured fields are what the frozen tree actually
declares.

### 4.3 Surface classes, by kind, declared before any URL is seen (QA-31, QA-37)

Every starting-point URL is classified **before it is requested**, by a
table fixed in the contract:

```text
repository-root    the root of a repository on a code host
                   (github.com/<a>/<p>, gitlab.<host>/<a>/<p>,
                   codeberg.org/<a>/<p>, sr.ht/~<a>/<p>, a self-hosted
                   cgit / gitea / gitlab root)
project-page       a URL that is none of the other classes
release-assets     a code host's release or tag download area
                   (/releases, /releases/download/, /archive/<ref>,
                   /-/releases, /tags) and a code host's
                   /downloads area             -> FORBIDDEN at E2-REP
distfile-location  a directory serving source archives by project: a
                   project's own download directory, a SourceForge
                   /projects/<p>/files/ or /project/<p>/ tree, a
                   mirror directory (CPAN by-author, GNU, Savannah
                   releases directories, OpenBSD's own distfiles)
```

**(analyst's call, settling QA-37)** `distfile-location` is **not**
the forbidden `release-assets` class: it is observed (QA-27's standing
rule), with the single purpose of confirming that a source distribution
exists there, which is what a candidate without a repository needs for
E2-REP's "source distribution" form. The forbidden class is a code
host's release-asset area because what it renders beside the assets is
release notes -- the class the sealed contract names. A URL that
matches no table row is requested once (one GET of the URL itself,
nothing followed) and classified by what the response is: a directory
listing or an archive file is `distfile-location`; an HTML page is
`project-page`; anything else is recorded and the URL is accounted
for as `unclassifiable` (see 4.5).

### 4.4 Step-2 authorization and designation (QA-35, QA-36)

Allowed navigation stays the sealed three steps. **(analyst's call,
QA-35's first form)** Step 2 is authorized by the **visible label of
the link itself** -- its anchor text, button text, or the `title` /
`aria-label` the page attaches to it -- containing one of the words
Source, Code, Repository, Development (any letter case) or their
exact translations where the page is not in English. A heading over a
link, a sentence around it, or the URL's shape authorizes nothing. A
**designation signal** (text saying the location is the project's
official, canonical or primary source) is a witness for the gate's
PASS; it is **not** a navigation permission -- a link reached only
through a designation sentence is not followed.

**(analyst's call, QA-36)** Owner-controlled repository metadata can
perform a designation only in these fields: the hosting platform's
repository description field, its website field, and a primary/mirror
marking in either; the repository's name and owning account identify,
they do not designate. A README body is not read (sealed contract), so
nothing in it designates, and the exposure log records what the landing
page rendered of it.

### 4.5 How E2-REP completes (QA-31, QA-41)

E2-REP PASS requires: every admitted starting point accounted for as
`observed` or `closed by class` (4.3) or `unclassifiable`; every
admitted starting point not closed by class **observed** (QA-27 /
QA-41: necessity is the standing rule, not an argument per candidate);
and exactly one designated canonical source location with a stable
URL and exactly one external target identifier established on what was
observed. A failure code requires positive evidence on an observed
surface. Otherwise the gate is UNRESOLVED, with one of these protocol
issue codes added to Run 1's two:

```text
PI-STARTING-POINTS-CLOSED   every admitted starting point is closed by
                            class; nothing could be observed
PI-UNCLASSIFIABLE-SURFACE   an admitted starting point could not be
                            classified by 4.3's table or its one request
PI-METADATA-UNRESOLVED      4.1's resolver could not resolve the metadata
```

`evidence_role` gains two values (QA-42): `admitted-starting-point` (a
surface admitted as a starting point that is neither a project page nor
a source location, such as an account page) and `distfile-location`.

### 4.6 Transport, exposure, times

Run 1's rules stand: transport indeterminacy is `PI-TRANSPORT-INDETERMINATE`
after two recorded retries; incidental content is logged in the
exposure log and does no work; E2-REP observation time and snapshot time
never merge. The snapshot rule itself is Section 7.3.

### 4.7 The gates past E2-REP

E2-RULE, E3 and E4 are decided as Run 1's amendment decides them
(positive-only PASS with a quoted, located witness; otherwise
UNRESOLVED, never FAIL), inside the tarball or repository tree fetched
at the pinned snapshot (7.3), with Run 1's four operational lessons as
rules: an E2-RULE witness is a quoted, located validity statement; a
negative verdict must survey the surface that would carry the fact; an
E3 FAIL must survey every surface E2-RULE admitted; E4 negatives need
the project's designating surfaces and its declared source units.
**Reading at these gates is bounded to the surfaces the contract names
for each gate** (the contract lists them per gate before the first
candidate), and nothing read at them is used beyond the gate's question
(the candidate-screening firewall).

## 5. Screening execution: tools, batches, review

**(owner)** Review unit: "여덟 개씩 묶어서 받자". The 128 items are
screened in frozen order in **16 batches of 8**; one commit per batch;
the owner reviews the batch and says 통과 or names the item that fails
review. A failed item is corrected in its own commit with Run 1's
retraction convention (nothing deleted, the earlier wording kept and
marked); the other seven stand.

Per item, a committed tool (`tools/screen.py`) produces, in one pass,
the frame-ledger row, the candidate-ledger row (where UR passes), the
starting-point table (URL, class, action, observed_at, http_status,
final_url), and the evidence blocks with the quoted, located witnesses
the analyst supplies for each gate reached. The analyst's part is the
reading at steps 1-3 and at the gates past E2-REP, and the inference
lines; every other field is produced mechanically from the frozen
metadata and the recorded HTTP observations. The batch's review
document is the eight rows and their evidence blocks, nothing else.

Session time per item (first read to the batch commit, divided by eight
for the batch's items that reached each gate) and review time per batch
(commit to the owner's 통과) are logged in `screening_cost.tsv` from the
first batch; their conditions (the analyst is an AI model operating the
tools; the owner reviews) are stated in the contract, not left to be
inferred (XQA-15 d).

## 6. The inventory and the completeness class (QA-19, the central change)

For every candidate surviving E1-E4, before any ranking, the
exploratory study's inventory procedure is run on the candidate's pinned
tree exactly as committed (`phase3_5/exploratory/tools/` at `35255d6`:
`inventory.py` classes K1-K4 with XQA-02's K1 widening, the EN2 and EN4
tests of XQA-05, `universe.py` with the terminator rule of XQA-07 (c)
and the bound table of XQA-08, the quarantine class of the exploratory
design Section 5.1, a committed verdict script per candidate in the
form of `x4b_verdicts.py`). The tools are imported from that path, not
copied, so that "the procedure as committed" is literally the one that
ran; any change needed for a candidate is a Run 2 tool with its own
test and an RQA entry.

**(owner)** The reading that makes the class decidable, accepted
2026-10-29 ("진행해줘" to the question "등급 A를 「절차가 본 범위 안에서
전부 enforced」로 읽고 사각지대를 한계로 선언하는 것, 이걸 Run 2의 선택
근거로 받아들이시겠어요?"):

```text
class A   the preregistered procedure admits at least one enforcement
          enumerator AND every enumerator it admits is `enforced`
class B   otherwise (an admitted enumerator is `asserted`, or none is
          admitted)
```

Completeness is completeness **relative to the preregistered procedure**.
The procedure's known blind spots are declared limitations (L2 of this
run): initializers hidden behind a macro, tables built entirely of
macros (XQA-04), function-scope accepted-name lists (XQA-15, #655),
and whatever the classes K1-K4 cannot see by construction. An
enumerator found later in a blind spot is handled by the sealed
late-discovery rule (sealed Section 2, "Candidate inventories are
frozen before E5 and before ranking"): if it could have changed the
class or `P_raw`, the confirmatory conclusions drop to INCONCLUSIVE,
the analysis is relabelled exploratory, and counterexamples survive.
No search outside the procedure is made to find one.

**The verdict layer is frozen before any survivor's tree is seen
(owner, 2026-10-29: "1 (a)").** The exploratory study's EN verdicts
were a per-candidate script written after reading the candidate's
tree, with most EN2 rejections decided by class rules specific to that
tree (XQA-15 a). Because the verdicts decide the class and the class
decides the selection, Run 2 does not repeat that shape. Instead:

```text
R2   one committed verdict grammar, tools/en_verdicts.py, written from
     the sealed EN1-EN6 definitions and the exploratory XQA-05 tests,
     BEFORE the frame is re-fetched and before any survivor exists:
       - the EN2 test and the EN4 test, as XQA-05 states them
       - a catalogue of NAMED class rules, each over element type, the
         set's role vocabulary (text, presentation, mapping, dispatch,
         defaults, data, resources) or a GENERIC file role (test,
         fixture, build-system, generated-code, documentation
         directories) -- never over a project-specific file name or
         symbol
       - the tag rule for enforced / asserted (sealed Section 3.3)
R5   the same script decides every survivor; a row the catalogue cannot
     decide is decided by the analyst's quoted, located identification
     (EN2) or refusal path (EN4), recorded in the row; every ADMIT and
     every EN4 verdict is quoted
     per survivor, a CLASS-SENSITIVITY TABLE is committed beside the
     verdicts: the admitted rows with their tags; the rows that passed
     EN2 and were rejected at EN4; the rows rejected by quotation
     rather than by catalogue rule -- the rows whose reversal could
     move the survivor's class -- and the owner reviews that table
     a rule the catalogue lacks for a survivor is an RQA entry; the
     rule is added as a generic rule and the final grammar is re-applied
     by the script to EVERY survivor before the selection, with each
     survivor's verdict differences reported, so that all classes are
     decided under one grammar (the mechanical re-application is not
     the in-flight reopening anti-goal 6 forbids, which is about
     verdicts made by hand)
```

The split per survivor (rows decided by quotation / by catalogue
rule) is reported (XQA-15 a).

Each survivor's inventory is one commit, reviewed by the owner before
the next survivor's, the class-sensitivity table first; the inventory
stage's cost per candidate is logged (the exploratory measure: about 22
minutes from candidate generation to all verdicts for 618 candidates,
about 28 minutes to `P_raw`).

## 7. Selection, non-blindness, snapshot

### 7.1 Selection

The sealed two steps, unchanged: class A over class B; within a class,
the tie key (normalized canonical source-location URL, external target
identifier), ascending by UTF-8 bytes, first wins. Both key components
are established at E2-REP (4.5). The class of every survivor is decided
by Section 6 before any tie-break is computed, and the selection is one
commit that lists every survivor with its class and key.

### 7.2 Non-blindness of C084 and C065 (exploratory L8)

The analyst has analysed C084 (a fork of C065) in the exploratory
study. If the rule selects either:

```text
the selection stands; neither is excluded or demoted by hand
the limitation is declared in RESULTS Section 1, in the first paragraph
Artifacts 1-3, PRIMARY_RESULT, KF.md and RESULTS are written anew; no
  sentence, unit, case description, mapping or judgment is copied from
  the exploratory record; the exploratory artifacts are not opened
  during Run 2's lane (an RQA entry if they are, with what was seen)
the exploratory findings are not cited as evidence anywhere in Run 2's
  lane; Run 2's result is reported with the non-blindness limitation
  and never merged with the exploratory result
the limitation covers the INVENTORY and the CLASS as well as the lane:
  the frozen grammar (Section 6) decides C084's or C065's verdicts as it
  decides every survivor's, the tools are imported for every survivor
  alike, and the analyst's knowledge of C084's earlier verdicts is
  declared; the class-sensitivity table of that survivor is reviewed
  with that declaration in front of it
```

### 7.3 Snapshot (QA-28, XQA-01 -- a declared deviation)

The sealed snapshot rule ("the state of the designated canonical source
location at the enumeration execution timestamp") cannot be executed
after the fact: an observation made later cannot tell what the default
branch pointed at an earlier instant (QA-28), and the exploratory check
of the sealed instant returned a commit other than the pinned one
(XQA-01). Run 2 therefore pins **at observation time**, and says so:

```text
for each survivor, at the moment E2-REP passes:
  default branch name; its tip commit as a full hash (git ls-remote or
  the host's API); the fetch of that hash (depth 1, core.autocrlf=false);
  the archive at that hash with its byte count, sha256 and entry count;
  ten file digests chosen by a fixed rule (the ten largest .c/.h/.m/.py/
  .cpp files, by byte count, in path order) -- all recorded in the
  candidate's pin record with the observation timestamp
distribution candidate: the designated archive by sha256, likewise
```

Every later step is defined against that hash. The deviation from the
sealed wording is recorded once, in the contract, with this reason; the
enumeration timestamp is provenance only.

## 8. The analysis lane, as the exploratory study executed it

Sealed Section 15 steps 6-14 run on the selected target exactly as the
exploratory design (`2026-10-29-phase3-5-exploratory-c084-design.md`)
and its plan executed them, with these readings adopted as rules of
this run rather than rediscovered: XQA-01 (observation-time pin, 7.3),
XQA-02 (K1 any element type), XQA-03 and XQA-05 (the EN2 and EN4
tests), XQA-06 (scratch helpers obey the quarantine; every exposure
logged), XQA-07 (c) (terminators), XQA-08 (out-of-bound rows,
`enumerator_bounds.tsv`), XQA-14 (KF-3 reads: comments, timeline,
linked commits and pull requests by number, with the caps written as a
rule: first posts 3,000 characters, comments 1,200 each and 10,000 per
item, patches 700 per file -- a cut is noted per item), XQA-15 (a-e):
class rules declared, cost logged per native case **and** per unit by
the unit's commit, the RESULTS generator committed with a regeneration
check from the first draft, the analyst and the clock stated with every
cost figure.

The KF-0 rule is the exploratory design's Section 8 (the tracker the
project designates; `L` = labels whose name or project-written
description denotes a failure; every issue, open and closed, pull
requests excluded; no window, no filter), applied at the step the order
below names. **Native replay is N/A for the whole lane, declared in
advance (owner, 2026-10-29: "2 N/A")**: no build or execution of the
frozen revision is attempted for any item; the reasons are the
exploratory design's (no build environment for an arbitrary target on
the analyst's machine, and a replay gives no positive evidence that the
architecture is right). The access rules are the exploratory design's
Section 5.
The three artifacts, the primary seal, the KF lane's firewall and KF-3's
"nothing above the KF-3 lines" rule are as there. Review cadence in the
lane: per native case, per artifact, per KF batch of ten, as there.

## 9. Budget, decision points, and what a stop may claim (QA-43)

The screening budget is the sealed 128 and is not re-set: the sealed
frame forbids adjusting it, and QA-43's "a budget set against a measured
cost" is met instead by **decision points on measured cost**, the
termination rule the exploratory design preregistered, extended to the
screening:

```text
D1  after screening batch 1 (items 1-8): input = per-item session time
    and the batch's review time, projected over 128; the owner decides
    continue / stop
D2  after screening completes (128, or the frame exhausted): input =
    the number of survivors and the projected inventory cost (6); the
    owner decides continue / stop
D3  after every survivor's inventory and the selection: input = the
    selected target's P_raw count (the exploratory T1); continue / stop
D4  after KF-0 is applied: input = the KF count (the exploratory T2);
    attempt in full / not opened
D5  after the first accepted native case: input = measured cost per
    unit and per case, projected (the exploratory T3); continue / stop
```

Each decision is the owner's, recorded in their words in RQA. **What a
stop may claim.** A stop at D1 or during screening reports the verdicts
of the items screened, the batches reviewed, and forfeits the frame's
eligible-set claim: no selection is made and no target is analysed. A
stop at D2 reports the eligible set and forfeits the selection. A stop
at D3-D5 is the exploratory design's: the lane is reported as not run
or as partial, the primary conclusions are not drawn, and the stop is
named as optional stopping in the methodology's sense. No stop is
silent and no stop re-frames.

**(owner, 2026-10-29: "3 기한 없음")** There is no deadline for this
run. The decision points are the only places a stop can be decided,
and nothing stops the run by the clock.

## 10. Reporting, the Run 1 comparison, records

RESULTS for Run 2 (`phase3_5/run2/RESULTS.md`) carries the twelve
sealed Section 14 items, the non-blindness declaration if it applies,
the limitations (Section 11), the decision points as exercised, and
every RQA entry that chose a reading. It is written by a committed
generator (`tools/results_write.py`, the exploratory one adapted) with
`checks.py results` regenerating it from the tables from the first
draft (XQA-15 c). If Run 2 reaches a confirmatory result, that result
-- and not the exploratory study's -- is what `phase3_5/RESULTS.md`'s
Section 10 question is answered by, and the README's Phase 3.5 section
points at it.

After screening completes, a mechanical comparison table is written
(`run1_vs_run2.tsv`: frame rank, port, Run 1 terminal status and stop
gate, Run 2 terminal status and stop gate, the rule of Section 4 that
accounts for a difference where one does). It changes no verdict in
either run; it is a methodology output about what the closed rules did
to the same frame.

Records live under `phase3_5/run2/`: `SCREENING_CONTRACT.md` (Section 4
and the per-gate surface lists, committed before the frame is
re-fetched), `EXECUTION_QA.md` (RQA-01 ..), `frame_enumeration.md`,
`screening_frame_items.tsv`, `screening_candidates.tsv` (Run 1's
schemas plus the columns Section 4 adds), `screening_evidence_bNN.md`
(one per batch), `exposure_log.md`, `screening_cost.tsv`, per-survivor
`inventory/<candidate_id>/` directories, `selection.md`, the pin
records, and the lane's files in the exploratory layout. `tools/` holds
the Run 2 tools with assert-based tests in the project's style; the
exploratory tools are imported, never edited.

## 11. Limitations preregistered for this run

In addition to the sealed Section 13's five:

```text
R-L1  the inventory procedure was developed on C084 and tuned once
      against it (XQA-04); its classes and tests were seen to work on
      one tree; the completeness class is relative to it
R-L2  the procedure's blind spots (Section 6) bound every absence
      claim; the late-discovery rule is the only remedy. The classes
      K1-K4 see compiled-in tables of C-family source; a project whose
      accepted sets live in data files (JSON, YAML, scripts) may admit
      no enforcement enumerator and fall in class B for want of a
      visible one, and class B loses to class A. This bias is DECLARED
      and the classes are NOT extended for this run (owner, 2026-10-29:
      "4 선언만"): adding a data-file class now, with Run 1's eligible
      set known, would be the candidate-fitted probe QA-19 refused and
      anti-goal 1. Where it decides the selection, the selection commit
      says so.
R-L3  the analyst is an AI model that has read C084's tree, the
      exploratory artifacts and Run 1's record; non-blindness is
      declared for C084 and C065 (7.2) and the analyst's prior
      exposure is a limitation for every candidate screened in Run 1
R-L4  one analyst, one reviewer (the owner), review per batch of eight
      at screening and per case in the lane; no independent replication
R-L5  the snapshot is an observation-time pin, not the sealed instant
      (7.3)
R-L6  the frame is the sealed 128 of 477; the budget is a workload
      ceiling, not a sample; a stop before 128 forfeits the frame claim
R-L7  the surface-class table of 4.3 and the step-2 rule of 4.4 are the
      analyst's readings of Run 1's open questions; a candidate decided
      differently under another reading is a property of the rule,
      reported with the comparison of Section 10
R-L8  the metadata resolver (4.1) is not a make evaluation; modules
      outside its declared list leave an item UNRESOLVED at UR
R-L9  the decisions at D1-D5 are the owner's; what is preregistered is
      where they can be made, on what, and what follows
```

## 12. Order of operations and review cadence

```text
R0   this document approved and sealed (docs-only commit)
R1   implementation plan (superpowers:writing-plans), approved
R2   SCREENING_CONTRACT.md, the verdict grammar (tools/en_verdicts.py,
     Section 6), the tools and their tests committed before the frame
     is re-fetched
R3   frame re-fetched, hash verified, enumeration re-executed and
     compared with Run 1's 128; frame_enumeration.md committed
R4   screening, 16 batches of 8, one commit each, owner review per
     batch; D1 after batch 1
R5   D2; survivor inventories, one commit each, owner review per
     survivor; selection commit
R6   D3; the lane: snapshot pin record (already taken at E2-REP),
     P_raw freeze, E5 checkpoint, KF-0 (D4), analysis per native case,
     Artifacts 1-3, primary seal, KF-1/2/3 (D5 after the first case)
R7   run1_vs_run2.tsv; RESULTS.md with its regeneration check; README
     pointer; memory
```

Each step's output in its own commit, the SHA reported, review before
the next step. A deviation from this order or from any rule here is an
RQA entry written at the time, naming the clause.

## 13. Left to the builder

- The exact per-gate surface lists for E2-RULE, E3 and E4 inside the
  contract (which files of a repository are opened at each gate, in
  what order), within the sealed firewall and Run 1's lessons.
- The metadata resolver's implementation and its declared module list,
  read from the frozen `bsd.port.mk` and `dist-tuple.port.mk`.
- The surface-class table's host and path patterns (4.3), as a
  committed table with a test per row.
- The HTTP client (stdlib, no retries beyond the two recorded ones,
  no authentication, a fixed User-Agent), its evidence fields, and the
  exposure log's format.
- `screen.py`'s output layout, the batch review document's layout, and
  the schemas' added columns.
- The ten-digest rule's implementation and the pin record's format,
  following `phase3_5/exploratory/pin_record.md`.
- Test fixtures (a fake ports tree, canned HTTP responses) in the
  project's assert-based style.

## 14. Decisions made by the analyst in this document

Listed so the owner can check them while reading: reading B for
identifiers in URLs (4.2); the surface-class table and the placement of
`distfile-location` outside the forbidden class (4.3); the label form of
step-2 authorization and "designation is not permission" (4.4); the
repository metadata fields that can designate (4.4); the three new
protocol-issue codes and two `evidence_role` values (4.5); the
observation-time pin and the ten-digest rule (7.3); the five decision
points and what each stop may claim (9); the batch commit and
correction convention (5); the import-not-copy rule for the exploratory
tools (6); the records layout and file names (10); the form of the
frozen verdict grammar -- generic file roles only, the class-sensitivity
table's three row kinds, and the re-application of an amended grammar
to every survivor (6); the scope of the non-blindness declaration over
the inventory and class (7.2).

Owner decisions after the builder check (2026-10-29): the verdict layer
frozen before any survivor is seen, form (a) (6); native replay N/A for
the lane (8); no deadline (9); the C-bias of the classes declared, not
extended (11).
