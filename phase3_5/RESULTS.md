# Phase 3.5 Results (sealed)

Consolidates what the methodology design
(`docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`,
sealed at `401924d`, revision 3.5j), `FRAME_ENUMERATION.md` (`1de4559`),
`SCREENING_PROTOCOL.md` (`9c255aa`, its network-access contract at
`b16fed3`, and two post-seal corrective amendments), the two ledgers,
`screening_evidence.md` and `EXECUTION_QA.md` (QA-01 through QA-43)
each separately established. Phase 3.5 is closed as of this document:
its screening run was terminated at QA-43, no target was selected, and
nothing downstream of selection was performed. Written 2026-10-28,
after the record and from it; no observation was made for this
document. It is step 15 of the design's own order of operations
(Section 15), reached with step 4 and steps 6 through 14 not performed
and step 5 determined INCONCLUSIVE at QA-19.

## 1. Question

`RESULTS_C4.md` Section 6 closed the synthetic sequence with the
question it could not answer itself: C1-C4's architecture --
`WorldState` / `MonitorState` / transition-local violation judgment /
persistent event provenance -- was forced by four cases the same author
designed, so "this architecture is necessary" rested on four cases with
a common author. The question, in its words: **"do these boundaries
appear when the system under test was defined by someone else?"**

Phase 3.5 was designed to answer that against one external system,
chosen with no analyst discretion: a sealed candidate frame, admission
gates E1-E4, a sealed ranking rule, a frozen primary universe, a
sufficiency gate, and the R0/F0/F1/F2/F3 taxonomy -- selection removed
from the analyst's hands as rigorously as C1-C4 removed tuning. Its
success condition was methodological, not directional (Section 1):
"Phase 3.5 is successful if the protocol is followed, regardless of
whether the external evidence retains, collapses, extends, contradicts,
or underdetermines the Phase 3 architecture."

The question is not answered by this run. What the run established
instead is in Section 6.

## 2. What was executed, against the sealed order of operations

Section 15 of the design lists fifteen steps. This run reached step 3,
reached step 5 with an outcome the design did not anticipate, and
stopped.

```text
 1  seal the methodology              DONE   401924d, 2026-08-27
 2  run the frozen query; screen in frozen order until the frame
    is exhausted or the budget is reached, "and record which
    occurred"
                                      DONE / TERMINATED
                                      1de4559: 477 frame items, 128
                                      budget. Which occurred: NEITHER.
                                      Screening was terminated at 96
                                      items (QA-43).
 3  screen candidates against E1-E4  DONE for 96 frame items / 94
                                             candidates. Protocol sealed
                                             before any item (9c255aa,
                                             b16fed3).
 4  freeze each survivor's primary    NOT REACHED. QA-19: the inventory
    snapshot and inventory                   stage was never
                                             operationalized. QA-28: the
                                             snapshot cannot be fixed
                                             from observation-time
                                             evidence.
 5  rank and select                   INCONCLUSIVE (QA-19). No target.
 6  promote U_primary / P_raw         NOT REACHED
 7  E5                                NOT REACHED
 8  KF-0 selection rule               NOT REACHED; the known-failure
                                             lane was never opened
 9  analyze every primary unit        NOT REACHED
10  freeze Artifacts 1-3              NOT REACHED
11  seal primary-lane result          NOT REACHED
12-14  KF-1..3                        NOT REACHED
15  write RESULTS                     this document
```

No simulator was built and no search was run, as Section 10 of the
design requires.

## 3. The frame

Reported per Section 14, item 1.

```text
enumeration source       official OpenBSD 7.9 ports.tar.gz
                         https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz
frame source revision    SHA256 937aef3d19bc288a838bfa168733872c1a33064d
                         b7fe00caf60ea29d9476c6db, checked against
                         OpenBSD's published value
enumeration timestamp    2026-08-26T19:23:05Z
exact query              every port directory whose Makefile defines
                         CATEGORIES including `games`, read from the
                         variable rather than the directory
membership               477 ports; 79 of them outside games/
screening order          ascending UTF-8 byte order of the port path
screening budget         128 (screening_set_128.txt)
frame exhausted or       NEITHER. 96 screened; 32 not screened
budget reached?          (ranks 93-104, 107-108, 111-128); QA-43
tie-break rule           sealed in the design, Section 2: ascending
                         byte order of the pair (normalized canonical
                         source-location URL, external target
                         identifier). Recorded per candidate as
                         tie_key and, per the protocol's second
                         amendment, used for nothing.
```

Two deviations from the frozen order are on the record and were not
reversed: QA-06 (fourteen ranks screened ahead of ranks 4-20, grouped
by outcome shape) and QA-18 (two frame items skipped, then screened).
QA-43 is the third deviation and the terminal one.

## 4. Screening result

The ledger at termination, unchanged by this document.

```text
frame items     96     94 candidates + 2 duplicates
                       (rank 68 -> C067, rank 106 -> C105)

                UNRESOLVED   ELIGIBLE   REJECTED
candidates          86           3          5

by gate         E1       PASS 94
                E2-REP   PASS 6    FAIL 5    UNRESOLVED 83
                E2-RULE  PASS 6    NOT_REACHED 88
                E3       PASS 6    NOT_REACHED 88
                E4       PASS 3    UNRESOLVED 3    NOT_REACHED 88

stop gate       E2-REP 88    E4 3    none 3

protocol-issue  PI-TRANSPORT-INDETERMINATE   18
codes           PI-UNCLASSIFIED-SHAPE        68
                NONE                          8   (5 REJECTED + 3 ELIGIBLE)

failure codes   E2REP-NO-SINGLE-CANONICAL-LOCATION   5
                every other sealed code               0
```

**ELIGIBLE, three.** C059 Cataclysm: Dark Days Ahead
(`https://github.com/CleverRaven/Cataclysm-DDA`), C065 Chocolate Doom
(`https://github.com/chocolate-doom/chocolate-doom`), C084 Crispy Doom
(`https://github.com/fabiangreffrath/crispy-doom`). All three carry
`primary_snapshot = UNRESOLVED` and every inventory field
`NOT_REACHED`. Each is an ELIGIBLE row whose enumeration of admitted
starting points was later found short by the ACCOUNT surface
RETRACTION 10 admits (QA-41, group 3); that is a recorded enumeration
error, and QA-41 found no ground on which necessity for that surface
could be established, so the verdicts stand.

**REJECTED, five, all on the same code.** C006 DGen/SDL, C011 Frodo,
C015 Virtual Jaguar, C047 bluemoon, C056 BZFlag: each exposed several
source designations with no primary among them, on a surface the
contract admits (`E2REP-NO-SINGLE-CANONICAL-LOCATION`). No candidate
was rejected on any other sealed code.

**UNRESOLVED at E4, three.** C004 Tiled, C008 DOSBox-X, C034
AstroMenace passed E2-REP, E2-RULE and E3 and produced no positive
`U_enforced` construction; under the protocol's first post-seal
amendment the absence of a construction does not establish E4 FAIL,
because no preregistered discovery procedure makes that universal
claim (QA-13).

**UNRESOLVED at E2-REP, eighty-three.** The record gives three routes,
and does not say which dominates because no such count was made:

```text
transport            18   no HTTP answer after the recorded retries,
                          with a healthy control (PI-TRANSPORT-
                          INDETERMINATE; the protocol's "Transport
                          failure is not criterion failure")
affiliation is not   --   the admitted starting points reach a code-host
designation               repository, and arriving at a repository
                          through packaging metadata establishes
                          affiliation, not upstream's designation of it
                          (QA-21, QA-22, C014/C017 boundary)
the bounded search   --   an admitted starting point that the contract
could not be closed       forbids opening (QA-31), or that was never
                          opened (QA-41, RETRACTION 31-32), leaves
                          exactly-one undecidable; a PASS cannot rest
                          on it
```

**The run's own history, from the ledger's git record.** Peak ELIGIBLE
count 12, on 2026-08-29; final count 3. 26 of the 94 candidates carried
more than one terminal status at some point -- 17 ELIGIBLE at some
point and UNRESOLVED now, 8 REJECTED at some point and UNRESOLVED now,
and one (C056) ELIGIBLE then REJECTED (RETRACTION 25). The evidence file holds 395 evidence blocks, 36 retraction
blocks and 28 quarantine headings; every withdrawn verdict's
observations remain in place.

**No coverage claim.** These are results about the 96 items screened,
in frozen order with QA-06's and QA-18's recorded exceptions. They are
not treated as a sample of the 128-item set, and nothing is inferred
about the 32 items not screened (QA-43).

## 5. Selection result: INCONCLUSIVE

Determined at QA-19, with 28 of 128 frame items screened, and
unchanged by anything after it. Ranking's first step is the enumeration
completeness class, which the design defines over a candidate's frozen
inventory; the inventory stage was never operationalized (QA-19's
amendment to the protocol), so the class boundary is undecided for every
survivor, and the tie-break is barred from being used across an
undecided boundary. The protocol's second amendment fixes what follows:

```text
REPORTED IN FULL
  the frozen frame and its enumeration
  every screening verdict with its grounds
  the eligible set, each survivor with its located enumerator witness
  every deviation, retraction and quarantine on the record

REPORTED AS NOT OBTAINED
  a primary target
  U_primary and P_raw
  E5 and everything downstream of it
```

This outcome does not depend on completion. QA-19 recorded it when
four candidates were eligible, and recorded that it would have differed
"in one respect only" with exactly one eligible candidate -- target
identity would be settled -- while "`U_primary`, `P_raw` and E5 would
still be unavailable, because they depend on a complete frozen
inventory rather than on the count of candidates." A 97th item could
not have made the boundary decidable.

## 6. The methodology result (the central result)

What the run established is about the sealed design, obtained because
the design was written before execution and its verdicts were checked
against it. Each item below is a recorded finding with a QA number,
not a reflection written for this document.

### 6.1 Admission is existential; selection is universal

QA-13 and QA-14: three of the four screening gates ask whether at
least one thing exists -- a validity requirement, a stateful question,
a constructible universe -- and their negative branches were never
operationalized. The seal specified admissibility in detail and no
discovery procedure by which an absence could be established. The
post-seal amendment made those gates asymmetric: a located witness
passes; anything else is UNRESOLVED, never FAIL.

QA-19: the same gap survives one stage past E4, in ranking. The
completeness class is a universal statement over a candidate's
enumerators, and nothing sealed says how to show that the enumerators
in hand are all of them. In the record's words, *"a protocol can be
rigorous enough to ADMIT candidates and still unable to SELECT among
them, because admission is existential and selection is universal."*
C004's and C008's E4 FAILs became UNRESOLVED under it (RETRACTION 5),
and C034 was recorded UNRESOLVED at E4 directly; the E2-REP moves in
Section 4 have their own ground, in 6.2.

### 6.2 E2-REP: exactly one, on a search the contract must close

E2-REP is the one gate the design let decide a negative component. The
protocol's first amendment gives the reason, quoted:

```text
its network-access contract fixes the starting points and the navigation whitelist, so "what was there to look at" is defined by upstream's own link structure rather than by us.
```
 The run found, one case at a time, what that clause
requires and what it does not permit:

```text
QA-11, QA-12   a negative needs a justified, closed search surface; a
               pre-named necessary surface cannot be filled by
               inference from another
QA-17          a criterion's wording cannot widen the navigation
               whitelist
QA-21, QA-22   arriving at a repository through packaging metadata is
               affiliation, not designation; the exemption carved for
               step 1 = step 3 was the same move in another shape
QA-24, QA-25   an admitted surface cannot be declined for a reason that
               only bounds it; a designated route is not a designated
               location
QA-27          a frozen SITES URL is an admitted starting point, not a
               navigation step; admission plus necessity is the test
QA-31          a metadata-supplied starting point can fall inside a
               class the contract forbids opening -- admitted but
               unobservable, and the gate has no way to complete over it
QA-35          step-2 authorization rests on three incompatible readings
               the seal never chose between; verdicts that hold under
               only one were withdrawn (RETRACTION 28)
QA-41          an E2-REP PASS asserts exactly one; a witness gives at
               least one; the negative half is decidable only on a
               closed bounded search. Eight of eleven ELIGIBLE
               candidates had an admitted starting point never opened
               and moved to UNRESOLVED (RETRACTION 31, 32), every
               observation preserved.
```

The stop rule -- navigation ends "the moment a PASS or a specific
failure code is determined" -- fires after determination and cannot
license skipping a surface the determination needs; QA-41 records the
run applying it backwards in five entries before the order was
corrected.

### 6.3 Frozen metadata is infrastructure-resolved

QA-39 and QA-40: for ports carrying `GH_*` identifiers the frozen
infrastructure defaults `HOMEPAGE` (`bsd.port.mk:1295`) and `SITES`
(`:1294`), and the records had read those fields off the port Makefile alone --
six denying a HOMEPAGE, six denying a SITES, four of them the same
records. The run had treated other
infrastructure-resolved values (`SITE_SOURCEFORGE`, `SITE_PERL_CPAN`,
`SITE_SAVANNAH`) as frozen metadata throughout, so the inconsistency
was the run's, not the seal's -- but the seal never said which
resolved values count as "the frozen OpenBSD metadata", and Run 2 must.

### 6.4 Observation time cannot reconstruct the sealed instant

QA-28: a distribution candidate's primary snapshot is "the externally
designated canonical artifact at the ENUMERATION EXECUTION TIMESTAMP",
and observing today's designation does not bound it backwards to that
instant; a dated release entry establishes when a release was published
and what is designated at observation time, not what was designated at
the sealed instant. Every survivor's snapshot is UNRESOLVED on this
ground or because the stage was never reached. The protocol's "Two
times that must never merge" was honoured by recording both, and the
record shows that recording both is not the same as being able to
connect them.

### 6.5 Vocabulary and schema gaps met in execution

QA-15 (no value for "inventory not built yet"), QA-33 (a row omitted
a contributing rank; repaired), QA-42 (the sealed `evidence_role` enum
has no value for a code host's account surface, which the
starting-point rules nonetheless admit), QA-30, QA-36 and QA-38
(designation force of platform navigation, of a repository's
self-description, and of identifiers inside a metadata URL -- each
recorded as unsettled by the seal, none decided). QA-37 records the
run answering one surface-class question two ways before noticing.

### 6.6 Corrections needed correcting

The record logs its own repair work. QA-39, QA-40 and QA-41 each
withdraw at least one statement made in an earlier version of the same
entry; QA-41's classification lists an undercorrection and an
overcorrection one commit apart, both by the author, both caught by
review. QA-23 is a record-only audit of every REJECTED verdict against
two later findings. The practice that made this visible is the one
C1-C4 used: nothing withdrawn is deleted, and a superseded sentence is
marked where it stands.

## 7. What this does and does not establish

- **No architectural outcome.** No R0, F0, F1, F2 or F3 was assigned
  to anything, because the taxonomy applies to counting units of a
  frozen primary universe and none exists. Nothing here says whether
  the C1-C4 boundaries appear in an external system.
- **No prevalence claim**, about game systems or about OpenBSD ports.
  Section 14's closing rule -- "No result table may imply prevalence
  of architectural outcomes from this single target" -- applies with nothing to tabulate, and
  Section 4's distribution of screening outcomes is a fact about this
  protocol meeting these 96 items.
- **The pre-registered limitations stand**, and 13.1 is stronger than
  written: the design noted that requiring source-level E2-REP selects
  for open, inspectable systems; this run's screening added a further
  filter in front of it: of 94 candidates, 6 passed E2-REP, so whatever
  a later run selects will come from systems whose packaging metadata
  reaches a surface the contract can close. 13.5 is unchanged:
  no executable-search or automatic-discovery claim is made.
- **The methodology result is confirmatory in the design's own sense.**
  Section 1 made "report the observed result exactly as produced" the
  success condition. The result produced was underdetermination at
  selection, and it is reported as that.

## 8. Reporting requirements (Section 14), item by item

```text
 1  frame, query, order, budget, exhausted-or-budget   Section 3 --
    eligibility evidence per candidate                 the ledgers and
    primary snapshot revision                          NOT OBTAINED
    full screened-candidate log                        the ledgers
    tie-break rule                                     Section 3
 2  admitted universe sources and enforced/asserted    NOT OBTAINED
 3  frozen P_raw with provenance                       NOT OBTAINED
 4  P_resolved / P_raw and E? / P_raw coverage         NOT OBTAINED
 5  reason log for every E?                            NOT OBTAINED
 6  correspondence matrix and C                        NOT OBTAINED
 7  per native case, supported {F1,F2,F3} or R0/F0     NOT OBTAINED
 8  counterexamples with their evidence basis          NONE; nothing
                                                       analyzed
 9  explicit absence/inconclusive wording               Sections 5, 7
10  three frozen primary artifacts                     NOT OBTAINED
11  known-failure lane                                 NOT OPENED
12  pre-registered limitations                         Section 7
```

## 9. Decisions and limitations carried forward

**Operational rules the run established, each from a withdrawn
verdict.** An E2-RULE pass needs a quoted, located validity witness,
not the existence of a `docs/` or `tests/` tree (QA-08). A positive
gate needs one witness; a negative verdict must survey the surface that
would carry the fact, and an index, a listing or a repository tree can
support "found" but never "not there" (QA-10, QA-12). An E3 FAIL must
survey every surface E2-RULE admitted (QA-07, QA-09). A necessary
surface is one the criterion's question and the observed structure make
necessary, never one the analyst names (QA-11, QA-24), and the same
rule stops an unnecessary surface being conscripted to force an
UNRESOLVED (QA-41, group 3).

**What a Run 2 preregistration must supply, consolidated from the
record's own "what Run 2 needs" notes.**

```text
QA-31, QA-37   forbidden surface classes named by what they are, so a
               distfile mirror and a code host's release-asset area
               are distinguishable before any surface is seen
QA-35          one reading of step-2 authorization, chosen in advance
QA-30, QA-36,  rules for platform navigation, repository
QA-38          self-description, and identifiers inside metadata URLs
QA-39, QA-40   which infrastructure-resolved values are frozen metadata
QA-42          an evidence_role value, or a rule, for admitted surfaces
               that are neither project page nor source location
QA-19, QA-28   an inventory procedure and a snapshot procedure that can
               actually be executed, or a design that does not need
               them
QA-43          a screening budget set against a measured per-item cost
               under review, and a preregistered termination rule
```

**What held.** Designs and contracts committed before the work they
govern; no verdict re-tuned after being seen, withdrawals made against
the sealed criteria and recorded as retractions; observed values never
deleted; the phase run under external review, with the holds and the
corrections they forced on the record. **What did not.** The
no-optional-stopping rule, in the end: the run stopped short of its
sealed budget by decision, and QA-43 names that rather than excusing
it.

## 10. What the next step must actually test (open question, not a decision)

The question in Section 1 is exactly where `RESULTS_C4.md` left it.
Phase 3.5 did not reach a system defined by someone else; it reached
the discovery that the mechanism built to choose one could admit
candidates and not select among them.

Two routes are visible from the record, stated as options and not
chosen here:

```text
Run 2 of the screening approach
  the same frozen frame, a preregistration carrying Section 9's list,
  and a budget it can afford. This is the only route that can produce
  the confirmatory result Phase 3.5 was designed for.

an exploratory single-target study
  one of C059, C065, C084, chosen by the analyst, labelled
  exploratory, and firewalled from this run's sealed results in the
  way C3's and C4's post-hoc diagnostics were. It would put the
  Section 1 question to a real external system sooner, and the
  choosing is itself the discretion Phase 3.5 was built to remove --
  so it can inform Run 2's preregistration and cannot stand in for
  its result.
```

Neither is decided by this document.
