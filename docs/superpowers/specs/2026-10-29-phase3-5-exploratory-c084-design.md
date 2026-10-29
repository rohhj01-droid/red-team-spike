# Phase 3.5 Exploratory Study -- C084 Crispy Doom -- Design

**Status:** design for an exploratory single-target study, to be sealed
before any step of it is executed. It applies the analysis lane of the
sealed Phase 3.5 methodology
(`docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`,
sealed `401924d`, revision 3.5j; "the sealed methodology" below) to one
hand-chosen target. It does **not** amend the sealed methodology, does
not modify any file of the sealed Phase 3.5 record, and does not
preregister Run 2.

**Label:** EXPLORATORY. Every document this study produces carries that
word in its title and its first paragraph. Section 2 says exactly what
the label marks and what the firewall around it is.

**Owner's decision this document implements (2026-10-29):** finish the
project according to the plan sealed at the start of Phase 3.5 -- the
fifteen steps of the sealed methodology's Section 15 -- by this route:
first run the full analysis lane on C084, then run Run 2 of the
screening. This document covers the first part only.

**Owner's answers to the builder check (2026-10-29):** no deadline --
the lane runs to the end; a termination rule is preregistered all the
same (Section 7.1); review inside step 9 is per native case (Section
9).

---

## 1. Why this study exists

Phase 3's closing document left one question, in its words:

> do these boundaries appear when the system under test was defined by
> someone else?
> (`phase3/RESULTS_C4.md`, Section 6)

The sealed methodology was built to answer it without analyst
discretion in the choice of system. Its run reached step 3 of Section
15 and stopped there: target selection was determined INCONCLUSIVE at
QA-19, screening was terminated at 96 of 128 frame items (QA-43), and
the analysis lane -- steps 4 and 6 through 14 -- was never executed on
any external system (`phase3_5/RESULTS.md`, Section 2). The question
above therefore has no answer of any kind in the record, confirmatory
or otherwise.

This study executes that lane on one system. It contributes two
different things, which must be kept apart:

```text
1. Inputs Run 2 needs and the screening run could not produce
   - an executed snapshot procedure              (QA-28 asked for one)
   - an executed inventory procedure, with its   (QA-19: "never
     candidate list and every reject reason       operationalized")
   - the measured cost of analysing one counting (QA-43: a budget must
     unit and one native case under review        be set against a
                                                  measured cost)
   - a KF-0 rule applied to a real tracker, and
     whether the set it yields is bounded
   - a termination rule preregistered and then  (QA-43: "a
     executed                                     preregistered
                                                  termination rule")

2. An answer to the Section 1 question for ONE system, chosen by hand
   - labelled exploratory, firewalled from the sealed result, and
     never presented as the confirmatory Phase 3.5 result (Section 3,
     anti-goal 1)
```

The first list is why this study comes before Run 2 rather than after
it. The second is why it is worth doing at all.

---

## 2. What "exploratory" marks, and the firewall

### 2.1 The two substitutions

The sealed methodology's Section 15 is followed step by step with
exactly two substitutions:

```text
sealed step 5   rank the eligible candidates by Section 2's ranking and
                select one

this study      the project owner chose C084 by hand from the three
                candidates the screening run left ELIGIBLE (C059
                Cataclysm: DDA, C065 Chocolate Doom, C084 Crispy Doom)

sealed step 4   freeze the primary snapshot -- under QA-28's reading of
                the sealed rule, the canonical artifact at the
                ENUMERATION EXECUTION TIMESTAMP, 2026-08-26T19:23:05Z,
                which QA-28 found cannot be established from a later
                observation; the ledger carries C084's
                primary_snapshot as UNRESOLVED

this study      the revision is the observation-time pin the screening
                record made and hashed on 2026-08-30 (EV-C084-PIN-01).
                It is the object the screening evidence describes. It
                is not the sealed-instant snapshot, and this document
                does not claim it is; Section 4.2 adds a consistency
                check against the sealed instant and records the
                outcome either way
```

For the first substitution, the owner's stated reason, recorded as
the owner's discretion and nothing else: among the three, C084's
screening witness at E3 -- a savegame version header the program
writes on save and reads back on load, refusing the file on mismatch
(`EV-C084-E3-01`) -- is the closest in shape to the mechanism C4
forced, a verdict that has to persist as state. The reason is recorded
because it is itself a limitation (Section 13, L1): the target was
chosen because its witness resembled the architecture under test.

Everything else -- universe construction, atomicity, counting, the
sufficiency gate, the taxonomy, the interpretation rules, the three
artifacts, the known-failure lane, the reporting requirements -- is the
sealed methodology's text, applied unchanged. Where this document
operationalizes something the sealed text left unoperationalized
(Sections 4, 6, 7, 8), it says so and records the choice as the
analyst's.

### 2.2 Why the first substitution makes the result exploratory

The sealed RESULTS put it this way, and this study adopts the sentence
as its own boundary:

> the choosing is itself the discretion Phase 3.5 was built to remove
> -- so it can inform Run 2's preregistration and cannot stand in for
> its result.
> (`phase3_5/RESULTS.md`, Section 10)

### 2.3 The firewall

```text
outputs        everything under phase3_5/exploratory/ ; nothing else
               in phase3_5/ is created or changed

sealed record  phase3_5/RESULTS.md, EXECUTION_QA.md (QA-01..QA-43),
untouched      SCREENING_PROTOCOL.md, FRAME_ENUMERATION.md,
               screening_evidence.md, screening_candidates.tsv,
               screening_frame_items.tsv, screening_set_128.txt
               -- not edited by this study, for any reason

README         gains one pointer to this study's directory and its
               label; nothing else

QA log         phase3_5/exploratory/EXECUTION_QA.md, entries XQA-01,
               XQA-02, ... -- its own numbering, so QA-01..QA-43 stay
               the closed record of the screening run; same
               conventions: deviations recorded in place, retractions
               never deleted, observed values never dropped

Run 2          Run 2's preregistration may cite this study's executed
               procedures, measured costs, and XQA entries. It may not
               cite this study's architectural outcomes as evidence,
               and it may not be shaped by them.
```

---

## 3. Goals, non-goals, anti-goals

**Goals.**

1. Execute the sealed methodology's Section 15 steps 4 and 6 through
   15 on C084 at its recorded revision, producing every Section 14
   reporting item for this target (or an explicit N/A with its
   reason).
2. Produce the five Run 2 inputs listed in Section 1, each as a
   document or table a Run 2 preregistration can cite.
3. Leave the sealed Phase 3.5 record byte-identical.

**Non-goals.**

- No simulator of the target, no port of Random/Beam/MCTS to it, no
  search, no executable-witness claim (sealed methodology Section 10).
- No Run 2 preregistration. That is a separate document, written after
  this study's RESULTS is sealed.
- No re-screening of any candidate, and no second target. C065 is
  C084's parent project and shares most of its code; it is not analysed
  alongside C084 for comparison.
- No change to the sealed methodology. A rule this study finds missing
  or ambiguous is recorded in XQA with the reading chosen, as the
  screening run did; the sealed text is not edited.

**Anti-goals** -- outcomes that would make the study a failure even if
every step were completed.

1. **The exploratory result used as if it were Run 2's result** (the
   owner's anti-goal, stated 2026-10-29). Concretely: this study's R0 /
   F0 / F1 / F2 / F3 findings appearing in any summary of Phase 3.5 as
   "what Phase 3.5 found", or being merged with a later confirmatory
   result, or Run 2's preregistration being tuned to reproduce or avoid
   them.
2. **The lane shrunk after it started.** Every unit in the frozen
   `P_raw` is analysed. A unit left unanalysed is a recorded deviation
   (XQA, named as optional stopping, as QA-43 did), never a scope
   decision.
3. **An inventory that stops at the screening-stage enumerator.** QA-19
   rejected exactly that: "treating the screening-stage positive
   enumerator as the inventory (nullifies the union rule and the
   late-discovery failure rule together)". The IWAD registry is one
   candidate among all the candidates Section 6's procedure generates,
   and is re-decided by that procedure.
4. **Sufficiency declared without located evidence** (sealed Section
   6.0). Each of the five questions is answered with a file and line at
   the frozen revision, or an evidenced N/A, or the case is `E?`.

---

## 4. The target and its frozen revision (step 4, first half)

### 4.1 Identity, from the screening record

```text
candidate            C084, frame item games/crispy-doom
canonical source     https://github.com/fabiangreffrath/crispy-doom
location             (EV-C084-E2REP-01)
revision             7775ef82d1e9dfd50eb9d2824acefaeff7247458
                     (`master` resolved 2026-08-30T06:09:46Z; committed
                     2026-08-03T14:08:24Z; EV-C084-PIN-01)
archive as pinned    2648481 bytes, sha256
                     4edfcde1c4f6f9292d673116f81ba40df6cf04033f17346131b4f2fe72fbce55,
                     832 entries
pinned file digests  ten files, listed in EV-C084-PIN-01
parent project       C065 Chocolate Doom (a fork; EV-C084-PIN-01)
```

### 4.2 Snapshot procedure (the executed form QA-28 asked for)

```text
1. git init phase3_5/exploratory/target/crispy-doom
   git remote add origin https://github.com/fabiangreffrath/crispy-doom
   git -c core.autocrlf=false fetch --depth 1 origin <revision>
   git -c core.autocrlf=false checkout --detach FETCH_HEAD
   -- a depth-1 fetch of the one commit: no history is on disk, so no
      commit message (fix descriptions are known-failure material) can
      be read by accident; core.autocrlf=false keeps every byte as
      committed, so digests are comparable
   -- if the host refuses a depth-1 fetch of a bare commit id, the
      fallback is the archive of step 4 unpacked as the tree: it also
      carries no history. A full clone is not a fallback, because it
      would put every commit message on disk

2. record: fetch timestamp (UTC), `git rev-parse HEAD` (must equal the
   revision), file count of the checked-out tree

3. recompute sha256 of the ten files pinned in EV-C084-PIN-01 from the
   checkout. ALL TEN must match. Any mismatch stops the study at this
   step with an XQA entry: the object on disk is not the object the
   screening record describes, and nothing downstream may proceed on
   it.

4. separately, fetch the archive of the same commit
   (https://github.com/fabiangreffrath/crispy-doom/archive/<revision>.tar.gz)
   and record its size, sha256 and entry count beside the pinned
   values, MATCH or MISMATCH. A mismatch here is recorded, not treated
   as a failure: an archive's bytes are generated by the host and are
   not guaranteed stable, whereas the commit identity and the ten file
   digests are. Whether the archive reproduces is itself a Run 2
   input.

5. consistency check against the sealed instant: through the host's
   API, read the current `master` history's latest commit dated at or
   before 2026-08-26T19:23:05Z. The script keeps commit ids and dates
   and discards commit messages before anything is displayed. Record
   whether that commit is the revision above (COINCIDES) or not
   (DIFFERS). DIFFERS is an XQA entry; the study still proceeds on the
   revision above, because that is the object the screening record
   describes, and any other choice would be a new pin with no record
   behind it. Neither outcome closes QA-28's gap: a history rewritten
   after the sealed instant cannot be excluded by a later observation,
   which is QA-28's point.
```

The checkout directory is listed in a `.gitignore` inside
`phase3_5/exploratory/`, so that nothing outside that directory
changes. The repository records the revision and the digests; it does
not carry the target's source tree.

Downloaded content is data, not code this project runs: every tool
that reads the tree lives in `phase3_5/exploratory/tools/`, takes the
tree's path as an argument, and is run with `python -I`.

---

## 5. Access rules

The sealed methodology's Section 8.6 fixes what must be analysed, not
what may be inspected. This section fixes what may be inspected and
when, because the known-failure lane's blinding (Sections 11 and 12 of
the sealed methodology) depends on it.

### 5.1 During the primary lane (study steps X4 through X11)

```text
MAY be read
  every file of the frozen tree, except the quarantined class below
  the canonical repository on GitHub, for exactly three purposes:
    - the fetch in Section 4.2
    - the sealed-instant consistency check in Section 4.2 (commit ids
      and dates only; the script discards messages)
    - the KF-0 count in Section 8 (metadata only; the script discards
      titles and bodies before anything is displayed)

MUST NOT be read until step X12 (KF-1) or later
  in-tree files whose purpose is to record failures or deficiencies,
    identified BY FILENAME PATTERN before any of them is opened:
      NEWS*  CHANGELOG*  ChangeLog*  HISTORY*  RELEASE*  NOT-BUGS*
      BUGS*  KNOWN*  TODO*  CHANGES*  -- matched against the file
      name, any case -- and every file under a directory whose name
      matches one of them
    -- listed in inventory_sources.tsv at step X4 with decision
       QUARANTINED, so the list is committed before any is opened
  the repository's issue tracker and pull requests (contents)
  the repository's commit history (absent from disk by construction)
  any third-party source: wikis, forums, mailing lists, package
    trackers, the parent project's repository, search engines

network
  hosts github.com, api.github.com and codeload.github.com only; no
  search engine; no bot-detection or CAPTCHA bypass under any
  circumstances (standing rule of the project)
```

Why the quarantine class exists: a release-notes file is a list of
fixed failures, so reading it during the primary lane leaks causes
before KF-1 and lets known-failure material shape the universe (sealed
EN6) and cross-links (sealed Section 4.2). `NOT-BUGS*` and `TODO*` are
included because their membership is defined by what was reported or
considered deficient -- EN6's exclusion -- even though they also contain
statements of intended behaviour. If a quarantined file would have been
the only candidate for an authoritative rule source, that is reported
as a consequence of this rule, not avoided by opening the file.

In-source comments cannot be quarantined without being read. A comment
that discloses a failure cause ("this crashed when ...", "fix for ...")
is an unavoidable exposure in the sense of KF-1, and is logged at the
moment it is read in `disclosure_log.md`: location, what was disclosed,
which unit or native case was under analysis. The log is preregistered
here so that its existence does not depend on anything being found.

### 5.2 During KF-1 and KF-2 (steps X12 and X13)

For each challenge item, the issue's first post only. Comments,
linked commits and pull requests are withheld. If the first post
contains no symptom, comments are read in order until one appears, and
every comment read is logged as a potential cause exposure for that
item.

### 5.3 From KF-3 (step X14)

Maintainer discussion, fix commits (fetched individually by SHA),
pull requests, and third-party material may be read, as KF-3 evidence
only. Nothing read at this step may alter any sealed artifact.

---

## 6. The inventory procedure (step 4, second half) -- the QA-19 gap

QA-19 found that the sealed methodology "never operationalized the
search" for enumerators and authoritative sources, and that writing
the procedure after seeing registry idioms risks fitting it to them.
That risk cannot be removed for this study -- the analyst has seen
C084's IWAD registry at screening depth, and several others across the
screening run -- so it is accepted and recorded (Section 13, L2), and
the procedure is bound in the only way left: it is committed before it
is run, its candidate generation is stated as classes rather than as
the known examples, and every candidate it produces is recorded with
its verdict and the criterion it failed.

The inventory is mechanical enumeration under the sealed methodology's
already-fixed rules (Sections 3.1 to 3.4 and 4.1 to 4.2). It does not
trace information flow, map anything to Phase 3 roles, or form any
architectural judgment.

### 6.1 Authoritative-source inventory (U_normative, sealed Section 3.1)

```text
search space S_doc
  every non-quarantined file in the frozen tree that
    - has an extension in { .md .txt .html .htm .rst .adoc .texi
      .1 .5 .6 .man }, or
    - has no extension and sits in the tree root or in a directory
      whose name begins with doc or man, or
    - is linked from README.md
  each listed in inventory_sources.tsv: path, bytes, decision, reason
  (quarantined files appear in the same table with decision
  QUARANTINED and are not opened; Section 5.1)

admissibility test (sealed 3.1, operational form)
  a file is an authoritative rule source iff
    (a) a project-owned statement -- in the file's own title or opening,
        in README.md, or in another in-tree non-quarantined document --
        explicitly says that THIS file states the rules, requirements,
        valid configurations or accepted inputs that the program
        enforces or that users must satisfy; the statement is quoted
        and located
    (b) the file exposes mechanical segmentation: numbered items,
        headed entries, table rows, or option entries (sealed 4.1)
  a file failing (a) is NOT ADMISSIBLE: the project did not designate
    it. Ownership, relevance, or clarity do not substitute (sealed
    3.1: "We do not promote a project-owned source to authoritative
    on its behalf")
  a file passing (a) and failing (b) is NOT ADMISSIBLE: "an
    undifferentiated prose blob ... researchers do not rescue it by
    manually splitting it" (sealed 4.1)

inside an admitted source
  every atomic item the source itself exposes is one normative source
  observation, retained verbatim with its own identifier -- no
  per-item filtering by whether the item "looks like" a validity
  requirement, because the sealed text segments by the source's own
  structure and nothing else
```

If no file passes, the normative route is unavailable for C084, exactly
as sealed Section 3.1 provides, and the study proceeds on `U_enforced`
alone. That outcome is reported with the full `S_doc` listing so a
reader can see what was examined.

### 6.2 Enforcement-enumerator inventory (U_enforced, sealed Section 3.2)

```text
search space S_code
  every file in the frozen tree with extension .c .h .cpp .hpp .m,
  every build file (*.am, *.ac, CMakeLists.txt, meson.build), and
  S_doc (for declared conventions)

candidate classes -- generated mechanically by committed patterns;
the patterns are part of the tool and are committed before the tool
is run on the tree
  K1  file-scope array initializers of aggregate type
      (a registry/table idiom: `... name[] = {` at file scope with
      a struct or array element type, static or not, const or not)
  K2  file-scope tables whose element type contains a function
      pointer (dispatch / interface tables); recorded as a K1 row with
      kind = K2
  K3  X-macro style lists: a macro whose body is a sequence of
      invocations of one parameter macro
  K4  conventions declared in S_doc: any in-tree document statement
      claiming that a closed set of items lives in a named directory
      or follows a named pattern ("all X are in Y", "every X is a Y")

  NOT a candidate class, with the reason stated now
      an enum type, or a switch over one: an enum is a type, not an
      enumerator of enforcement observations; the sealed EN3 examples
      are registries, declared interfaces, collected annotations and
      declared directory conventions. This exclusion is an analyst
      choice and is listed in Section 13 (L2)

per candidate, recorded in inventory_enumerators.tsv
  file, line, symbol, class, element type, member count (K1-K3),
  and for EN1..EN6 in order: PASS or FAIL with the located evidence;
  the first FAIL ends the test for that row and is its reject reason

EN4 evidence standard
  the project itself must connect the mechanism to validation,
  eligibility, acceptance/refusal or an equivalent validity role:
  a quoted comment, an identifier in the project's own vocabulary, a
  documentation sentence, an error message, or the project's own code
  path in which the enumerated set decides the acceptance, refusal or
  eligibility of an input, a state or an action -- quoted and located.
  Selection alone does not qualify: a table consulted to pick a
  function, a sprite, a sound or a menu entry has no validity role
  unless a miss is a refusal or an ineligibility, and then it is the
  refusal that qualifies it. The analyst's reading that a table "is
  used for validation" is not evidence; the connecting text or code is

tags (sealed 3.3 / EN5)
  enforced   runtime construction closes the set (an array bounded by
             its own length, a dispatch table consulted as such)
  asserted   an unconditional current-state claim closes it
  a candidate whose closure basis is neither fails EN5

union (sealed 3.4)
  every candidate passing EN1..EN6 is admitted; none is dropped for
  being large, awkward or redundant with another
```

The IWAD registry (`src/d_iwad.c`, `iwads[]`) will appear as a K1
candidate. Its screening-time E4 verdict is not carried over; the
procedure decides it afresh, and the record notes whether the two
decisions agree.

### 6.3 Universe construction and `P_raw`

```text
source observations
  for each admitted enumerator, the tool enumerates its members by
  parsing the initializer (or the convention's directory), one
  enforcement source observation per member, retaining the externally
  segmented fields; commented-out members are ABSENT (EV-C084-E4-01's
  corrected count is the precedent); identifiers E<k>-<n>
  for each admitted normative source, one observation per atomic item;
  identifiers N<k>-<n>

cross-links (sealed 4.2)
  an edge exists between two observations iff an in-tree,
  non-quarantined, project-owned artifact explicitly states that the
  one corresponds to the other (a comment citing a document section by
  name, a document citing a table or function by name). Nothing read
  from a quarantined file or from the tracker may supply an edge.
  connected components of the edge graph are the counting units; a
  component of one observation is an ordinary unit

frozen outputs, committed before any unit is analysed
  P_raw.tsv       unit id, observation ids, source/enumerator id, tag,
                  retained fields
  O_raw, P_raw    the counts, and the number of linked units
```

---

## 7. Promotion and the E5 checkpoint (steps 6 and 7)

**Promotion (X6).** The commit that adds `P_raw.tsv` is the freeze. An
admissible source or enumerator discovered after it is recorded in XQA
as an inventory protocol failure with its effect on `P_raw` stated, and
is **not** added -- the sealed Section 2 rule. The study is already
exploratory, so the sealed rule's relabelling has no further effect;
the record still has to say that it happened.

**E5 (X7).** The sealed text requires that "the entire frozen primary
universe must be traceable to the evidence-sufficiency gate without
sampling or optional stopping" and admits that traceability cannot be
judged without tracing. The owner has set no deadline for this study,
so no unit count is too large by a calendar. What remains of E5 before
analysis is the finiteness the construction already guarantees, and a
decision the owner makes on the count alone:

```text
E5 PASS   iff  U_primary is finite and fully listed (true by
               construction once P_raw.tsv exists)
          and  at termination point T1 (Section 7.1) the owner does
               not declare the lane infeasible at that count

E5 FAIL   otherwise: a primary-lane boundedness failure. The study
          reports it, executes X8 (which does not depend on P_raw and
          is a Run 2 input in its own right), and stops after X8. No
          other target is selected (sealed E5: "A boundedness failure
          does not license selecting a different target").
```

For scale only: a unit under review has been estimated, not measured,
at one to three hours; measuring it is one of this study's outputs.
Non-traceability of an individual unit during analysis is not an E5
failure; it is `E?`, the sealed design's own mechanism.

### 7.1 The termination rule (preregistered)

The sealed RESULTS carries QA-43's requirement forward to Run 2 as "a
preregistered termination rule" (`phase3_5/RESULTS.md`, Section 9).
The owner asked for one in this study (2026-10-29); its shape is the
analyst's call (Section 16). Its purpose: if a stop ever comes, it is a
rule-governed outcome and not a deviation. There is no deadline, so the
rule has no automatic trigger. It fixes WHERE a stop may be decided, ON
WHAT, and WITH WHAT RESULT:

```text
T1  at X7, on P_raw alone -- no unit has been analysed
    proceed, or declare the primary lane infeasible at this count
    -> E5 FAIL as above

T2  at X8, on the KF count alone -- no item has been opened
    attempt the known-failure lane in full, or report it as a
    boundedness failure / N/A for the whole lane, with the count

T3  once, at X9, when the FIRST native case has been accepted under
    review, on cost alone: that case's measured cost (session time
    and elapsed-to-acceptance, cost_log.tsv), projected over P_raw
    and, if T2 chose to attempt the KF lane, over the KF count. The
    owner continues, or stops the lane here. A stop at T3 has this
    fixed status and no other:
      primary lane   boundedness failure determined at T3; the
                     accepted native case and the units resolving
                     into it are retained and so labelled; Artifacts
                     2 and 3 are then written for the retained case
                     only, in the order of Section 10; no coverage
                     figure and no absence or retention statement is
                     made; a counterexample finding on the retained
                     case stands as an existence finding (sealed 8.1)
      KF lane        not executed
      RESULTS        written, with whichever Run 2 inputs exist

anywhere else   no stop. A stop anywhere else is the deviation
                anti-goal 2 names, recorded as QA-43 was: as optional
                stopping, with the clauses it breaks

each T decision is recorded in XQA with its input (the count, the
projection) and the owner's grounds, before the next step begins

why a single T3 and not one per native case: a later checkpoint is
decided after more of the target has been seen, which is the exposure
sealed Section 8.6 exists to prevent. T1 and T2 see no native
description at all; T3 sees one, and no architectural classification,
because Artifact 2 is written only after Artifact 1 is complete
(Section 10)
```

---

## 8. The KF-0 rule (step 8), frozen before any unit is analysed

```text
tracker of record
  the issue tracker at the canonical source location
  (https://github.com/fabiangreffrath/crispy-doom/issues), unless an
  in-tree non-quarantined document designates a different tracker, in
  which case that one; the designation, if any, is quoted

failure set
  L = the set of labels the project has defined in that tracker whose
      NAME or project-written DESCRIPTION denotes a failure (bug,
      defect, crash, regression, error, or a synonym) -- decided from
      the label list alone, before any issue is listed; all such
      labels are taken, none chosen among
  if L is non-empty
      KF set = every issue (open and closed; pull requests excluded)
               carrying at least one label in L, as of the enumeration
               timestamp
  if L is empty
      KF set = every issue (open and closed; pull requests excluded)
               as of the enumeration timestamp
  no time window, no status filter, no component filter, no
  subsampling

why labels, and why not "all issues" when labels exist
  the sealed rule takes "the BROADEST externally defined failure set"
  -- a FAILURE set. Where the project labels failures, the labelled
  set is the project's own definition of failure; the set of all
  issues is an issue set,
  not a failure set, and would include requests and questions that
  the sealed KF-2 attribution would then have to discard one by one as
  scope mismatch. The alternative reading ("all issues, always") was
  considered and is recorded here as rejected; the choice is the
  analyst's and is made before the tracker is seen (Section 16).
  Its cost is stated with it: the project's labelling is not complete
  by construction, so the KF set is complete only within the
  project's own labelling -- the `asserted`-style weakness, reported
  as such

why pull requests are excluded
  a pull request is a proposed fix, which is KF-3 material, not a
  failure report

boundedness
  at X8 the count of the KF set is recorded through the tracker's API
  with titles and bodies discarded by the script before display. The
  owner then decides at termination point T2 (Section 7.1), on the
  count alone: attempt the lane in full, or report it as a boundedness
  failure / N/A for the whole lane with the count on the record, in
  which case steps X12-X14 are not executed (sealed KF-0: "do not
  select a convenient subset from it"). There is no numeric ceiling,
  because the owner set no deadline. For scale only: KF-1 plus KF-2
  for one item under review is estimated, not measured, at one to two
  hours

native replay (sealed 11.2.3)
  declared N/A for the whole lane, now, before any item is seen. The
  sealed text allows exactly this ("attempt replay for every challenge
  item satisfying it, or report native replay as N/A for the whole
  lane"); replay "provides no positive evidence that the Phase 3
  architecture is correct", and building the frozen revision with its
  data files is a cost this study does not take on. Analyst's call,
  listed in Section 16
```

The count is the only thing read from the tracker before X12 -- not
the item list. The sealed KF-0 says the qualifying items "are
enumerated only after the primary lane and all three primary artifacts
are frozen", so the ids are enumerated at X12, at their own recorded
timestamp, and X12's count is compared with X8's; a difference is
recorded. The labels' names and descriptions are read at X8 to decide
`L`; no issue title is displayed until X12.

---

## 9. Analysis of every unit (step 9)

The sealed methodology's Sections 5, 6, 7 and 8 apply without change.
What this section adds is the layout the work is recorded in, and one
process measurement.

```text
ARTIFACT_1_native.md
  one entry per native case NC-01, NC-02, ... in the target's own
  vocabulary: the sealed Artifact 1 fields (source observation ids;
  native state/data; writers; updates/invalidation; readers;
  lifetime/persistence/reset; transitions; evidence; remaining
  uncertainty), and the five sufficiency questions each answered with
  a file and line at the frozen revision, or an evidenced N/A
  -- no Phase 3 role name appears in this file

units.tsv
  unit id -> native case id(s) -> RESOLVED or E? -> for E?, the
  question numbers left as gaps

E_LOG.md
  every E? with the four items sealed Section 6.1 requires: the
  missing evidence, why recovery failed, opacity/tooling versus
  possible unmodeled structure, and the explicit F2 re-check

disclosure_log.md
  Section 5.1's in-source exposures, appended as they happen

cost_log.tsv
  per unit and per native case: the analysis sessions' start and end
  timestamps, the commit that first carried the work, and the commit
  or review message that accepted it -- so that both the analyst's
  session time and the elapsed time to acceptance under review are
  recoverable; the sealed RESULTS asks Run 2 for "a measured per-item
  cost under review" (phase3_5/RESULTS.md, Section 9). This is a
  process measurement, preregistered here; it is not an outcome
  measure and is never used in any verdict
```

Order inside step 9: units are analysed in `P_raw.tsv` order. A unit
whose native case is already described is linked to it (the unit-case
map is many-to-many, sealed 5.2) and its own sufficiency evidence is
still located and recorded.

Review inside step 9 is per native case (the owner's choice,
2026-10-29): when a native case's Artifact 1 entry is complete, it is
committed together with the units analysed so far that resolve into
it, and held for review; analysis continues only after acceptance. A
later unit that resolves into an already-accepted case is added to
that case and reviewed with the next case's batch (the batching is the
analyst's call). The first acceptance is termination point T3
(Section 7.1).

The external validity semantics that sealed Section 7.1's competitor
test refers to are, for this target: the admitted normative
observations, if any, and the accept/refuse behaviour of each admitted
enforcement mechanism as described in Artifact 1. A competing
representation that violates either does not qualify as the competitor
R0 must discriminate against.

---

## 10. The three artifacts and the primary seal (steps 10 and 11)

```text
X10a  ARTIFACT_1_native.md complete for every native case, committed
X10b  ARTIFACT_2_mapping.md -- written only after X10a is committed:
      per native role, its Phase 3 assignment or `no clean mapping`,
      with reasoning; per native case, R0 or F0, or the full supported
      subset of {F1, F2, F3} with no finding suppressed; for R0 the
      named competitor and the evidence that discriminates against it;
      for F3 the positive evidence for the alternative boundary
X10c  ARTIFACT_3_judgment.md -- written only after X10b is committed:
      the applicability domain first, by the sealed mechanical
      inclusion rule, then the decision procedure, total within the
      domain
X11   PRIMARY_RESULT.md: resolved/P_raw and E?/P_raw; the E? list with
      reasons in the main body; the per-case findings table; the
      unit<->case map; the correspondence matrix and the collapsed
      count C; the absence or INCONCLUSIVE wording under sealed
      Section 8.4, weakened to the asserted scope if any admitted
      enumerator is `asserted`
```

"Written only after ... is committed" is strict: Artifact 1 is
finished for all cases before any sentence of Artifact 2 exists, so
that Phase 3 vocabulary cannot shape the native description. Artifact
2's role assignments and outcomes are frozen before any challenge item
is opened (sealed Section 9: "the main contamination surface").

The Phase 3 architecture Artifact 2 maps onto is the one named in the
sealed methodology's carry-in and in `phase3/RESULTS_C4.md`:
`WorldState`, `MonitorState`, transition-local violation judgment,
persistent event provenance (`EventProvenanceState`, `phase3/DESIGN_C4.md`).

---

## 11. The known-failure lane (steps 12 to 14), if bounded

```text
X12  enumerate the KF set under the frozen rule at a recorded
     timestamp; store the issue ids; for each item, KF-1: read the
     first post (Section 5.2); record in KF.md the disclosure log
     (what was seen: id, title, labels, which fields; cause leakage
     yes/no and what leaked) and the symptom fields the sealed KF-1
     allows (expected, observed, documented reproduction, affected
     version)
X13  KF-2 per item, using the frozen artifacts only: representability
     (11.2.1); judgment applicability against Artifact 3's frozen
     domain, with in-domain concordant / in-domain DISCORDANT /
     in-domain indeterminate / out-of-domain kept as four results
     (11.2.2); the attribution class (sealed "KF-2 failure
     attribution"). Native replay: N/A for the lane (Section 8).
     Sealed by commit before X14
X14  KF-3 per item: open comments, linked commits and pull requests,
     and third-party material; compare; one coupled mapping->judgment
     finding where Artifact 2 was wrong and Artifact 3 inherited it.
     Nothing edits X10-X13
```

If the T2 decision at X8 reported the lane as a boundedness failure,
X12-X14 are not executed and `KF.md` records the rule, the count, the
decision and the N/A.

---

## 12. RESULTS and the inputs to Run 2 (step 15)

`phase3_5/exploratory/RESULTS.md` is written last, in the
consolidate-and-seal pattern of the phase RESULTS documents. Its title
and first paragraph carry EXPLORATORY and anti-goal 1 in full. It
contains:

1. The sealed Section 14's twelve items, each present or N/A with its
   reason. Item 1 (frame, screening, tie-break, snapshot) points to
   the sealed `phase3_5/RESULTS.md` and states the two substitutions
   of Section 2.1: the hand choice in place of the selection result,
   and the observation-time pin in place of the sealed-instant
   snapshot.
2. The owner's reason for the target, as discretion.
3. The limitations of Section 13 in addition to the sealed Section
   13's five.
4. **Inputs to Run 2**, as its own section:
   - the snapshot procedure as executed and what it returned (Section
     4.2 steps 2-5): a reproduction of a recorded pin and a
     sealed-instant consistency check -- not a closure of QA-28's
     gap, which this study does not claim;
   - the inventory procedure as executed: candidate counts per class,
     admitted and rejected counts by EN criterion, the time it took;
   - per-unit and per-native-case cost from `cost_log.tsv`, as a
     distribution, not an average alone;
   - the KF-0 rule as applied, `L`, the count, and the T2 decision;
   - the termination rule as executed: each T decision, its input and
     the owner's grounds, from XQA;
   - every XQA entry that names a rule the sealed text lacked, with the
     reading this study chose.
5. What this study does not establish -- sealed Section 14's closing
   rule applies: "No result table may imply prevalence of architectural
   outcomes from this single target."

---

## 13. Limitations specific to this study

In addition to the sealed methodology's Section 13 (13.1 to 13.5), all
of which apply:

```text
L1  hand-chosen target, chosen for witness shape
    the target was selected by the owner because its E3 witness
    resembles C4's persistent-provenance mechanism. Any R0 or F3 found
    on that mechanism is therefore partly selected for, and the study
    cannot claim the mechanism was found rather than looked for.

L2  the inventory procedure was written after registry idioms were seen
    (QA-19). Candidate classes K1-K4, and the exclusion of enum/switch,
    are the analyst's; the procedure's completeness is bounded by them.
    Mitigated only by committing the procedure before running it and
    recording every candidate with its verdict.

L3  the analyst's prior exposure
    at screening the analyst read, for C084, the IWAD registry and its
    identification path, and the savegame version-header writer and
    reader (EV-C084-E3-01, EV-C084-E4-01). The candidate-screening
    firewall is therefore already partly crossed for this target before
    step X4; Artifact 1 is not written by someone who has never seen
    those mechanisms.

L4  fork lineage
    C084 is a fork of C065 and shares most of its code. A finding about
    a shared mechanism is a finding about the lineage's design, not
    about C084's additions; the record states, per native case, whether
    the code is in C084's own changes or inherited, where the tree
    makes that visible. No claim is made about C065 itself.

L5  E5 before analysis is reduced to finiteness plus the owner's T1
    decision on the count (Section 7); the traceability the sealed
    text describes is only tested during analysis, unit by unit, as
    E?.

L6  the known-failure lane's size is unknown until X8, and whether it
    is attempted is the owner's T2 decision on the count, with no
    numeric ceiling preregistered -- a discretion this study records
    rather than removes.

L7  one analyst, one reviewer, as in the screening run; the review is
    visible in the commit record, not independent replication.

L8  consequence for Run 2
    if Run 2's rule selects C084, or C065 (same lineage), Run 2's
    analysis of that target is not blind to this study. Run 2's
    preregistration must state in advance how that is handled -- as a
    declared non-blind limitation on that target's conclusions -- and
    may not exclude the target by hand, which would be rule-picking.

L9  the termination rule's decisions are the owner's. What is
    preregistered is where they can be made, on what, and what
    follows; T3 is decided after one native case's description has
    been accepted, before any classification exists.
```

---

## 14. Order of operations and review cadence

```text
X0   this design sealed (committed, builder-checked, owner-approved)
X4a  snapshot: Section 4.2; commit the pin record
X4b  inventory tool committed (patterns, parsers, digest script);
     then run; commit inventory_sources.tsv, inventory_enumerators.tsv,
     the quarantine list
X6   P_raw.tsv committed -- the freeze
X7   E5 checkpoint recorded; termination point T1 (owner, on P_raw)
X8   KF-0 rule applied: tracker, L, count; termination point T2
     (owner, on the count); commit -- executed on E5 PASS and on E5
     FAIL alike; on FAIL the study stops after this step
X9   every unit, in P_raw order: Artifact 1 entry, units.tsv row,
     E_LOG / disclosure_log / cost_log as they arise; committed and
     reviewed per native case; termination point T3 (owner, on cost)
     once, after the first accepted native case
X10  Artifact 1 complete -> Artifact 2 -> Artifact 3, three commits
X11  PRIMARY_RESULT.md committed -- the primary seal
X12  KF-1 (if bounded)
X13  KF-2 sealed by commit
X14  KF-3
X15  RESULTS.md (exploratory) committed; README pointer; memory
```

Cadence, as in the screening run: each step's output in its own
commit, the SHA reported, review before the next step. The owner's
drafting checks (recompute every number from source; check each
referent; check that a superseded claim is not restated; check each
new sentence against its neighbours) apply to every document as a
non-record procedure. A deviation from this order, or from any sealed
rule, is an XQA entry written at the time, naming the clause.

---

## 15. Left to the builder

- The exact patterns implementing K1-K4 and the quarantine filename
  class, as code in `phase3_5/exploratory/tools/`, committed before
  running (Section 6.2). The classes are fixed here; their
  implementation is not.
- The member parser for each admitted enumerator (one per idiom
  found), with the commented-member rule.
- The digest script for Section 4.2, and the API script for Section 8
  that reads the label list and the count and discards item fields.
- A check script, run before each RESULTS-type document is committed,
  that recomputes every count in it from the TSVs (as
  `results_fixcheck.py` did for the sealed RESULTS).
- File naming inside `phase3_5/exploratory/` beyond the files named in
  this document.

---

## 16. Decisions made by the analyst in this document

Listed so the owner can check each one while reading; any can be
overridden before sealing.

```text
 1  target tree checked out inside the repository, git-ignored
    (phase3_5/exploratory/target/crispy-doom), not outside it
 2  depth-1 fetch of the one commit, so no history is on disk
 3  the archive is re-fetched and its digest recorded, match or
    mismatch, as a Run 2 input; a mismatch is not a failure
 4  the quarantine class is defined by filename pattern (Section 5.1)
    and includes NOT-BUGS* and TODO*
 5  third-party material is barred until KF-3, including the parent
    project's repository
 6  candidate classes K1-K4; enum/switch excluded as a class
 7  no per-item filtering inside an admitted normative source
 8  Artifact 1 is finished for all cases before Artifact 2 begins
 9  E5 before analysis is finiteness plus the owner's T1 decision on
    the count; no numeric ceiling, because the owner set no deadline
10  KF-0 reads "broadest failure set" as the union of the project's
    failure-denoting labels when any exist, otherwise all issues;
    pull requests excluded; whether the lane is attempted is the
    owner's T2 decision on the count, no numeric ceiling
11  native replay N/A for the whole lane, declared in advance
12  cost_log.tsv as a preregistered process measurement
13  a separate XQA numbering, and a README pointer as the only change
    outside phase3_5/exploratory/
14  the revision is the observation-time pin, declared as the second
    substitution (2.1), with the sealed-instant consistency check of
    4.2 step 5; a DIFFERS outcome does not change the revision
15  EN4's narrow reading (6.2): selection qualifies only where a miss
    is a refusal or an ineligibility
16  X8 is executed on E5 FAIL as well; the study stops after it
17  the KF count only at X8; the item ids at X12
18  cost_log.tsv records both session time and elapsed-to-acceptance
19  the termination rule's shape (7.1): three decision points T1-T3,
    a single T3 after the first accepted native case, fixed
    consequences for a stop; the owner asked for a rule, the shape is
    the analyst's
20  inside per-native-case review (the owner's choice), a later unit
    resolving into an accepted case is batched with the next case
```
