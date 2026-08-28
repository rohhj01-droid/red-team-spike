# Phase 3.5 Screening — Execution QA Log

Instrument defects and void measurements encountered while executing
the sealed screening protocol. Kept **separate from
`screening_evidence.md`**: nothing recorded here was used to decide any
candidate verdict. Its purpose is that a later reader can reconcile
"why does the ledger differ from the first HTTP results" and "why was
the automated repo classification not used."

None of these are protocol changes. They are measurement failures on
our side, fixed or discarded the same way the methodology treats `E?`:
a fact about our observation never becomes a fact about the system.

---

## QA-01 — CRLF-corrupted probe batch (VOID, discarded)

A bulk reachability probe of frame ranks 4-128 returned status `000000`
for all 123 HTTP targets in 18 seconds, while individually issued
requests to the same hosts had been succeeding.

**Cause.** The target list was generated on Windows and carried `\r` at
end of line, so every URL passed to the client had a trailing carriage
return and was malformed. Confirmed with `cat -A` (`^M$` on every line)
and by a clean single request to one of the same URLs returning 200.

**Disposition.** The entire batch is void. It was re-run after
stripping `\r` and protecting the loop's stdin, and only the re-run
appears in evidence. No candidate verdict cites the void batch.

## QA-02 — line-continuation artifact in metadata extraction (CORRECTED)

Frame rank 100 (`games/dungeon`) was initially probed at a URL ending
in a backslash and recorded unreachable. Its `SITES` value spans
multiple Makefile lines, and the extractor captured only the first
line, including the `\` continuation character.

**Disposition.** Corrected. The real URL responds 200, so rank 100 is
**not** transport-indeterminate and remains to be screened. A sweep for
the same artifact across all 125 extracted targets found no other
affected URL; three entries contain unexpanded make variables, which
are handled as a separate case, not as this defect.

## QA-03 — first metadata extractor missed two mechanisms (CORRECTED)

The first extractor read only `HOMEPAGE`, `DISTNAME`, `GH_ACCOUNT`,
`GH_PROJECT`, `SITES`/`MASTER_SITES` from each port's own Makefile. It
therefore missed:

- **`DIST_TUPLE`** (`github ACCOUNT PROJECT TAG SUBDIR`), which
  identifies upstream directly and is used by 13 of the 125 items;
- **`Makefile.inc` inheritance**, e.g. `games/colobot/data` inherits
  `HOMEPAGE` from `games/colobot/Makefile.inc`.

Uncorrected, 13 items would have been recorded as having no upstream
identifier when the metadata does identify one.

**Disposition.** Extractor rewritten to read `DIST_TUPLE` and to walk
ancestor `Makefile.inc` files. After correction every one of the 125
items has an identifier source and none has multiple primary tuples.
`DIST_TUPLE` entries whose target subdirectory is not `.` are vendored
dependencies rather than the packaged system, which is a mechanical
discriminator (`games/fallout1-ce` bundles `Loadmaster/fpattern` into
`third_party/fpattern`).

## QA-04 — automated repo-link classification (DIAGNOSTIC ONLY, not used)

An attempt was made to decide E2-REP's "exactly one externally
designated canonical source location" mechanically, by extracting link
structure from each reachable landing page and counting distinct
repository links and self-hosted source archives.

**The instrument is not verdict-grade, and its output was not used for
any candidate verdict.** Demonstrated failure modes:

```text
GitHub site chrome counted as repositories
  flycast 72, libchdr 52, 2048-cli 62 distinct "repos", consisting of
  /collections, /contact/report-content, /customer-stories, ...

account pages counted as repositories
  github.com/bjorn, github.com/joncampbell123

dependencies counted as alternative source locations
  advancemame's page links libdeflate and zopfli

auxiliary project repos counted as alternative source locations
  crispy-doom + its homepage repo; egoboo + its assets repo;
  endless-sky + its editor; fifengine + its tutorials
```

After filtering chrome and requiring owner/name paths, 13 items still
showed "multiple repos", and inspection showed these were almost
entirely system-repo-plus-auxiliary-repo, not several source locations
for one system. A further 32 showed "no repo and no tarball", which is
more plausibly under-detection than genuine absence.

**Finding.** Upstream *designation* is a qualitative fact that link
counting cannot stand in for. This is not a reason to change the
sealed criterion; it means the remaining items must be screened
individually, reading each project's own designation, as the contract
already requires.

## QA-05 — broken `getent`, and heterogeneous client-side failures

An initial DNS check using `getent hosts` reported every probed host as
non-resolving, including `nongnu.org`. Cross-checking with `nslookup`
showed `nongnu.org`, `crossfire.real-time.com`, and `kiwisauce.com` do
resolve, so `getent` is unreliable in this environment and its output
was discarded.

Capturing the client's actual error text showed the failures are not
one phenomenon:

```text
(6)  could not resolve host          DNS
(28) connection timed out            timeout
(35) schannel InitializeSecurityContext failed   TLS handshake
(60) schannel SNI/certificate check failed       TLS certificate
```

Two consequences, both recorded rather than acted on:

- A TLS failure means **no HTTP exchange occurred at all**, so the
  contract's "definitive HTTP answer" category cannot apply to it by
  construction; it falls on the transport-indeterminate side. This
  reading follows the contract's own wording and does not extend it.
- For `games/eliot` the metadata URL `https://nongnu.org/eliot/` fails
  certificate validation while `https://www.nongnu.org/eliot/` returns
  200. The `www.` form was **not** used: allowed starting points are
  limited to URLs present in the frozen metadata, and constructing a
  variant would be the analyst inventing an entry point.

## Contract gaps observed, deliberately NOT repaired mid-run

Recorded for the eventual results write-up. Repairing any of these now
would be tuning the rules to the run:

1. **NXDOMAIN vs DNS timeout.** The contract lists "DNS failure" as one
   transport-indeterminate category. `perso.b2b2c.ca` returns NXDOMAIN,
   an authoritative negative, which is closer to the contract's own
   "equivalent permanent absence" than to a timeout. Five frame items
   depend on this host.
2. **TLS failure is unenumerated.** It is classified above by the
   "no HTTP answer" reading, but the contract's list does not name it.
3. **`exactly one canonical source location`** cost `C002` its
   eligibility, and having both a repository and self-hosted release
   tarballs without labelling either canonical is ordinary practice. If
   this holds across the frame, eligibility may be very low — which is
   a legitimate result, not a defect, and must not be softened to avoid
   it.

## QA-06 — out-of-order screening (DEVIATION, recorded, not reversed)

The sealed methodology requires screening in the frozen rank order.
The batch committed as `d3aff92` did not follow it: ranks 21, 27, 39,
40, 41, 55, 70, 73, 79, 86, 105, 106, 109 and 110 were screened before
ranks 4-20.

**Cause.** Those ranks were the ones whose verdicts the network
contract already determined (three recorded attempts, no HTTP answer,
control succeeding), and they were grouped and recorded first as a way
of separating contract-determined outcomes from ones needing judgment.

**Why this is a deviation and not merely a reordering.** Selecting the
items to process first *by the shape of their outcome* is selective
inspection, the thing the frozen order exists to prevent. Screening
"the easy ones first" once invites doing it again — a proposed batch of
16 items whose HOMEPAGE happens to be a repository page was rejected
for exactly this reason, since that subset is defined by a property
discovered after looking.

**Impact assessment.** Bounded. The screening set was already frozen at
the first 128 items, every rank touched lies inside it, and neither the
denominator nor the budget changed. What was affected is the order of
observation, not the population.

**Disposition.** The affected evidence is kept as recorded and is not
re-observed: re-measuring would grant those endpoints a second
observation opportunity under different network state, which is worse
than the original deviation. Screening resumes at rank 4 in frozen
order, and a rank already sealed is passed over as such rather than
re-examined. Batch boundaries from here are contiguous rank ranges
only, never groupings by outcome type.

## QA-07 — measuring the wrong surface again, at E3 (caught, verdicts withheld)

While determining E3 for ranks 5, 8, 10 and 12, the check that was run
grepped **GitHub directory-listing pages and a wiki index**, not the
documentation those pages point at. The counts it produced (`timing` 2,
`sync` 1, and similar) are as likely to come from file names or site
chrome as from any documented validity requirement.

This is QA-04's failure repeating one gate later: an instrument aimed at
a surface that cannot carry the fact being asked about. It was caught
before any verdict was issued, and **no E3 verdict for ranks 5, 8, 10 or
12 was recorded from it**.

Where a real documentation surface was read, the signal is
qualitatively different and was used:

```text
mednafen  /documentation/   save states 21, netplay 28, movie 19,
                            rewind 7   -> temporal validity documented
fceux     documentation.html  movie 5  -> temporal validity documented
tiled     doc.mapeditor.org index      -> automapping, export,
                            preferences, scripting API; "session" 2;
                            no temporal validity topic
```

**Consequence for cost.** E3 and E4 cannot be settled from repository
structure or index pages. Each remaining candidate that reaches them
requires reading the project's actual designated documentation, which
is substantially more expensive per item than UR, E1, E2-REP or
E2-RULE were. Ranks 5, 8, 10 and 12 remain in flight at E3 for this
reason, not because the gate is ambiguous.

## QA-08 — E2-RULE applied on artifact existence rather than content (VERDICTS WITHDRAWN)

E2-RULE was passed for all seven E2-REP survivors in batch 4-13 on the
grounds that each designates documentation, a test suite, or both. That
is weaker than the sealed criterion, which requires the external
evidence to be *sufficient to determine* at least one validity
requirement, and whose example is "tests that explicitly state expected
validity" rather than tests in general.

**Disposition.** The C004 verdicts are withdrawn and the candidate
returns to in-flight; the retraction is recorded in
`screening_evidence.md` rather than deleted. No other candidate had
E2-RULE recorded, so nothing else needs withdrawing.

The corrected standard, applied from here: E2-RULE passes only with a
located witness -- a specific documented or tested statement of the form
"under condition X the result must be Y" or "state Z is invalid" -- cited
in the evidence entry. Existence of a docs/ or tests/ directory is not a
witness.

**Second defect, specific to C004.** Its E3 failure was determined from
the documentation index alone, while its E2-RULE had admitted the
repository's tests/ directory as validity evidence. A surface admitted
at one gate cannot be disregarded at the next; the tests were never
examined for a temporal validity witness before E3 was failed. Rule
carried forward: an E3 FAIL must survey every surface that E2-RULE
admitted, not a subset of it.

## QA-09 — the withdrawn C004 E3 verdict was not merely under-evidenced; it was wrong

QA-08 withdrew C004's E3 FAIL for being determined from too narrow a
surface. Re-determination on the proper surface reversed it: **E3
PASSES**, on a located witness in Tiled's own designated format
reference:

```text
nextlayerid — "Stores the next available ID for new layers. This number
is stored to prevent reuse of the same ID after layers have been
removed."
```

Whether a layer ID may be assigned is not decidable from the current
snapshot: the layers present do not reveal which IDs once existed. The
format carries a counter precisely because present state cannot answer
the question. That is history-dependent validity, structurally the same
shape as the properties Phase 3 was built around.

**What produced the wrong verdict.** The original check read the
documentation *index* and concluded from its section titles
(automapping, export, preferences, scripting) that no temporal validity
topic existed. The witness is one level below that index. Section
titles are a summary surface and cannot support a negative finding
about content.

**Rule carried forward, joining QA-04 and QA-07:** a negative verdict
requires surveying the surface that would carry the fact, not a surface
that would merely mention it. Index pages, directory listings, and
repository trees can support "found it" and cannot support "it is not
there."

This is the third instrument-surface error in this screening run and
the first that had actually reached a recorded verdict. It was caught
only because the verdict was re-opened rather than accepted.

## QA-10 — E4 negative claims exceeded their surfaces (WITHDRAWN, re-determined)

EV-C004-E4-01 failed E4 on two claims that outran their evidence, the
same error as QA-09 one gate later:

```text
claimed: the project does not designate an authoritative rules source
shown:   the reference page does not call ITSELF authoritative

claimed: no EN1-EN6 enforcement mechanism exists
shown:   the repository ROOT has no directory named "validators"
```

Both were withdrawn. Re-determination surveyed the surfaces where each
fact would actually appear -- five project-owned pages for the
designation, and the source tree's declared units for the mechanism --
and reached the same verdict on far better grounds.

The re-survey also found something the cheap version had missed
entirely: Tiled **does** have a declared, mechanically closed
enumeration mechanism, `src/plugins/`. It fails EN4 rather than EN3,
because the project connects it to map import/export rather than to
validation. A verdict of "no mechanism" would have been simply false.

**Rule carried forward.** "No directory named validators" is not
evidence of "no enforcement enumerator", and "the page does not call
itself authoritative" is not evidence of "the project designates no
authoritative source". Both are cheap negatives that would recur on
every remaining candidate if left standing. E4 negatives require
surveying the project's own designating surfaces and its declared
source units.

## QA-11 — a pre-named necessary surface cannot be filled by inference from another

C005's E2-REP was recorded PASS after one of the two surfaces named in
advance -- the SourceForge project hub -- proved unobservable across
three attempts with healthy controls. The gap was filled by reasoning
from the surface that HAD been read: /download routes this system to
GitHub and the family's other products to SourceForge, therefore the
hub is not a competing designation.

That substitutes a positive fact about one page for a negative claim
about another. The contract already classifies the situation directly:
no HTTP answer after two recorded retries is transport indeterminacy,
the gate is UNRESOLVED, later gates are NOT_REACHED.

**The new part, and the reason this is its own entry:** the
surface-naming discipline adopted after QA-10 was followed correctly
here. Both surfaces were named before investigating. The failure came
one step later -- when a surface we had ourselves declared necessary
became unobservable, its absence was reasoned around instead of
accepted. Naming surfaces in advance is only half the rule.

**Rule carried forward, in its corrected form.** An earlier draft of
this entry said "the pre-naming is what makes the surface necessary".
That is too strong, and opens the opposite discretion: an analyst could
declare any page necessary, find it dead, and make the candidate
UNRESOLVED at will. Naming is not what confers necessity.

```text
A surface does not become necessary because the analyst names it.

Necessity must be justified ex ante from
  the sealed criterion's actual question
  + the upstream link/designation structure already lawfully observed

Once justified on those grounds and recorded as necessary, transport
indeterminacy on that surface cannot later be bypassed by indirect
inference from a different surface.
```

C005 remains UNRESOLVED under the corrected form. The AdvanceMAME
landing page did expose a SourceForge project hub, and E2-REP asks
whether *exactly one* source location is designated -- so checking
whether that hub is a competing designation was grounded in the
criterion and in observed structure, not merely asserted. It was then
never observed.

**Evidence-format consequence.** From here, any negative component of a
gate determination records, alongside the surfaces, one line:

```text
Necessary because:
  [which question in the sealed criterion requires it]
  + [which already-observed upstream structure raises it]
  so the verdict cannot be settled without reading this surface.
```

That single line closes both of today's failures at once: it stops a
necessary surface being dropped after the fact (QA-11's original case),
and it stops an unnecessary surface being conscripted into necessity to
force an UNRESOLVED.

Consequence for C005: E2-REP UNRESOLVED, E2-RULE/E3/E4 NOT_REACHED,
their already-collected findings quarantined as post-stop exposure. The
sealed stop rule exists precisely to prevent looking further past an
unresolved gate, and having looked, the honest remedy is to record the
exposure and refuse to use it.

## QA-12 — a negative needs a JUSTIFIED CLOSED search surface, not a sample of it

C008's withdrawn E4 read the repository's top-level names, selected
"the two plausible candidates" among them, and concluded from those two
that no EN1-EN6 mechanism exists. Selecting which candidates are
plausible is analyst selection wearing a different hat, and the source
interior went unexamined -- exactly where C004's src/plugins/ turned up
after the same shortcut had missed it.

Naming surfaces in advance (QA-10) and refusing to abandon a necessary
one (QA-11) are not enough on their own. A negative also requires an
argument for why the surface set is CLOSED: why, if the fact existed,
it would have to appear inside what was searched.

Two closure arguments were available here and are worth reusing:

```text
the project's own enumeration
  DOSBox-X publishes List-of-Guide-Pages. That list is authored
  upstream, so it closes the set of documents in which the project
  could designate an authoritative source.

the criterion's own shape
  EN4 requires the PROJECT to connect a mechanism to validation. That
  is a fact about what the project SAYS, so project documents close
  the question. A registry may exist anywhere in src/; if no project
  document declares it as carrying validity rules, it fails EN4
  regardless.
```

The second is the more useful pattern: when a criterion asks what the
project declares, the search surface is the project's declarations, and
an exhaustive code walk is not owed. That has to be argued, though, not
assumed -- the withdrawn entry reached a similar conclusion with no
argument at all.

**Rule carried forward.** A negative verdict states its closure
argument. "I looked at these and found nothing" is not a negative;
"if it existed it would have to be here, and here is what here
contains" is.

## QA-13 — the existential gates' negative branch was never operationalized (POST-SEAL AMENDMENT)

Three successive attempts to fail a candidate at E4 were withdrawn, and
the third withdrawal showed the problem is not in the attempts.

```text
C004 first try   "no validators/ directory" -> absence            (QA-10)
C008 first try   top-level names, "two plausible candidates"      (QA-12)
C008 second try  docs-only closure argument                       (here)
```

Each was wider than its evidence, and the last failed in a new way: its
closure argument confined the search to prose documentation, which
quietly removes runtime construction -- registry contents, interface
dispatch, annotation collection -- that the sealed rules explicitly
admit. Narrowing what counts as evidence in order to make a negative
tractable is criterion change wearing procedural clothes.

The root cause is structural, not local. The sealed methodology defines
admissibility exhaustively (Section 3.1's designation requirement,
Section 3.2's EN1-EN6) and defines no discovery procedure at all. E4
PASS needs one positive construction and is therefore decidable; E4
FAIL quantifies over everything a project might contain and is not.

**Resolution: a post-seal corrective amendment**, recorded in
`SCREENING_PROTOCOL.md` and dated to its cause rather than backdated to
`401924d`. For this run E4 becomes asymmetric -- PASS on a positive
construction, UNRESOLVED otherwise, using the already-sealed
`PI-UNCLASSIFIED-SHAPE` rather than a code invented after seeing
results.

Alternatives considered and rejected:

```text
restrict admissibility to an external inventory
  -> narrows the criterion post hoc; the mirror image of loosening it
     after seeing results

preregister a mechanical source-tree discovery procedure now
  -> the right instrument, but no longer preregisterable: several
     candidates' structures have been seen, so the probe set would be
     fitted to them. Reserved for a future run, sealed before any
     candidate is examined.
```

Effects on this run, stated rather than buried: no new eligible
candidate, no relaxation of E4 PASS, one unsupported capability
removed, more UNRESOLVED outcomes. The amendment reduces what the run
claims. That direction is why it is admissible mid-run; the reverse
would not have been.

## QA-14 — the same gap is not E4-specific; E2-RULE and E3 share it

QA-13 asserted "the gap is specific to E4". That is wrong, and the
error is the same kind the amendment was written to correct: a claim
wider than what was checked.

E2-RULE and E3 are existential in exactly the same way.

```text
E2-RULE  PASS  one located externally-authored validity requirement
         FAIL  no such requirement exists anywhere in the project

E3       PASS  one located stateful/temporal validity question
         FAIL  no such question exists anywhere in the project
```

Both FAILs are universal absence claims, and neither gate has a sealed
discovery procedure. E2-REP is the genuine exception, and for a reason
worth naming: its network-access contract fixes starting points and a
navigation whitelist, so what there was to look at is bounded by
upstream's own link structure rather than by our choice.

**No existing verdict is affected.** The ledger carries four REJECTED
candidates, all stopped at E2-REP with
`E2REP-NO-SINGLE-CANONICAL-LOCATION`, which is positive in shape -- it
records finding several designations with no primary, not finding
nothing. No candidate has ever been failed at E2-RULE or E3; C004 and
C008 passed both on located witnesses, and every other candidate
stopped earlier. The correction is therefore preventive rather than
retroactive, which is the first time in this run that has been true.

The amendment in `SCREENING_PROTOCOL.md` is extended to all three
gates. Its effect is unchanged in direction: fewer claims, more
UNRESOLVED, no candidate made eligible, no PASS relaxed.

Also corrected there: EN1-EN6 live in Section 3.2, not Section 3.1.
Section 3.1 carries the authoritative-designation requirement. The
amendment had cited them as one.

## QA-15 — the candidate schema had no value for "inventory not built yet" (CLOSED)

C010 is the run's first ELIGIBLE candidate, and it is the first row to
reach the seven fields the schema places after `evidence_refs`. The
protocol says of them only that they are "inventory work that the sealed
methodology performs only for candidates surviving E1-E4", and that
"rejected candidates carry `NOT_REACHED` there". It says nothing about
what a survivor carries between passing E4 and the inventory stage
actually running.

Four of the seven are already determined by gates that have run, so
they are filled with their real values:

```text
canonical_source_location    https://github.com/flyinghead/flycast   (E2-REP)
external_target_identifier   Flycast                                 (E2-REP)
primary_snapshot             c3763d8fc4208dd6f8f0bc456383543b8406a8a0
tie_key                      (URL, identifier), computed from the two above
```

`primary_snapshot` is not a judgement: the sealed rule resolves it
mechanically to the commit the default branch pointed at at the
enumeration execution timestamp, 2026-08-26T19:23:05Z. Master had not
moved since 2026-08-23T11:29:03Z, so it resolves to c3763d8 -- which is
also the revision the E4 observations were read at.

The other three -- `authoritative_source_inventory_ref`,
`enumerator_inventory_ref`, `completeness_class` -- genuinely require
the inventory stage.

**Resolution: all survivor inventories are built after screening
completes**, and `PENDING_INVENTORY` is formalized in
`SCREENING_PROTOCOL.md` as a bounded lifecycle state rather than left
as a note here.

The ordering argument is stated at its actual strength, which is
narrower than this entry first put it. The sealed methodology requires
screening through the frozen frame/budget and requires every survivor
inventory to be frozen before ranking; performing all survivor
inventories only after screening is therefore the least discretionary
execution order for this run. It is **not** claimed that the sealed
text forbids mid-screening inventory in so many words -- an earlier
draft of this entry said the methodology "places that stage after
screening", which reads as a prohibition the document does not contain.

The independent reason is contamination, and it is the stronger one.
Building Flycast's inventory means reading its structure far deeper
than E4 required. Screening the remaining 104 items from that state
would let the first survivor's structure shape how witnesses are
searched for in later candidates. The explicit rules would stay fixed;
search habits are not covered by explicit rules. The path is avoidable
at no cost, so it is closed rather than argued about afterwards.

Two consequences follow, both recorded in the protocol:

```text
finding an eligible candidate does not stop screening
  later ranks may also be eligible, and may carry a higher
  completeness class

survivors are inventoried in ascending first_frame_rank
  fixed before the survivor set is known, so that "which survivor
  do we examine closely first" is not a live choice
```

`PENDING_INVENTORY` says nothing about the candidate, cannot be a
verdict, and appears in no gate vocabulary; it may not be used in
ranking, and must be replaced at the inventory stage. That is why it is
admissible where a new *outcome* code would not have been -- the
amendment's objection is to vocabulary that changes what a result says.

One note for the inventory stage: C010's E4 record already asserts a
354-entry universe. That number and the observation granularity behind
it are re-established mechanically at inventory time rather than
inherited from the screening entry.

## QA-16 — E4 as sealed is satisfied by a common idiom (OBSERVATION, no change made)

Three candidates have now reached E4 and all three passed, each on the
same structure:

```text
C010 flycast   Games[]            sentinel loop   -> "Unknown game"
C012 libchdr   codec_interfaces[] ARRAY_LENGTH    -> CHDERR_UNSUPPORTED_FORMAT
C014 snes9x    command_names[]    LAST_COMMAND    -> S9xBadMapping, mapping refused
```

Amended after QA-17: C014's E4 entry is quarantined as post-stop
exposure, so the admissible base for this observation is C010 and C012.
The C014 row is left in the table because the structure it found is what
this entry is about, and because a quarantined observation is recorded
and refused work rather than erased. It carries no weight below.

A static table, walked to its own declared bound at runtime, with a miss
producing a rejection the project itself executes. That is not a loose
reading of EN1-EN6; it is close to a transcription of them -- EN3 names
"all entries in a registry", EN5's first admissible case is "runtime
construction closes the set", and EN4 is met because the rejection is
executed rather than inferred from a name.

Two statements, separated deliberately by how well they are supported.

```text
CONFIRMED OBSERVATION
  every candidate that has reached E4 so far passed it, on the same
  table / declared-bound / executed-rejection idiom
  n = 2 admissible (C010, C012), plus C014 quarantined

HYPOTHESIS, not established
  that E4 will admit a large fraction of the C codebases in this frame
  because that idiom is ordinary practice in them
```

Amended twice since, and in opposite directions.

C010 and C012 were later withdrawn at E2-REP (QA-22), so their E4
entries are quarantined too. The full admissible E4 base is:

```text
C004   no positive construction obtained   -> UNRESOLVED
C008   no positive construction obtained   -> UNRESOLVED
C009   positive construction obtained      -> PASS
C013   positive construction obtained      -> PASS
C022   no positive construction obtained   -> UNRESOLVED
```

So the confirmed observation above -- that every admissible candidate
reaching E4 passed it -- is no longer true. A second draft of this
paragraph said C022 was the FIRST admissible candidate to reach E4
without yielding a positive construction. That is also wrong: C004's
and C008's final entries, EV-C004-E4-03 and EV-C008-E4-03, already read
"no positive construction was obtained" and close on UNRESOLVED. The
observation stopped holding when those two were re-determined, not when
C022 arrived.

C022's actual contribution is procedural. C004 and C008 were
RETROSPECTIVE re-determinations: both began as negative attempts under
the pre-amendment rule and were converted afterwards. C022 is the first
newly screened candidate whose E4 adjudication began with the
asymmetric post-seal rule already in force, so it is the cleaner example
that reaching E4 does not guarantee this run will obtain a positive
construction -- the rule was not applied to it after the fact.

It weakens the hypothesis that the table/bound/reject idiom will
commonly support E4 PASS, and C004 and C008 were already evidence in the
same direction.

**What C022 does not establish, and an earlier draft of this paragraph
wrongly said it did.** That draft read "the idiom is common, but it is
not universal, and a project can state and enforce validity rules
without exposing an enumerator at all". Both clauses convert an
UNRESOLVED into a negative fact, and they contradict C022's own E4
entry, which says in as many words that no preregistered discovery
procedure makes that universal claim decidable. "Not found" was
established; "not there" was not. Withdrawn.

What can be said stays inside what was examined: Aleph One visibly
states and executes validity rules through direct conditionals, and the
mechanisms actually examined -- its MML dispatch and its plugin loader
-- did not yield an admissible property-level enumerator.

Two admissible cases cannot support a proportion over 128 items, and the
frame-wide claim is written as a hypothesis so that the eventual number
tests it rather than confirms it.

What is firm about the earlier gates has to be stated more carefully
than an earlier draft of this entry managed. It said "the gates
eliminating candidates are earlier ones", counting every E2-REP stop as
an elimination. Most of them are not. As of rank 15:

```text
non-eligible terminal candidates      24
  stopped at E2-REP                   22
  stopped at E4                        2

of the 22 E2-REP stops
  REJECTED by the criterion            5   all
                                           E2REP-NO-SINGLE-CANONICAL-LOCATION
  UNRESOLVED, protocol/transport      17   16 PI-TRANSPORT-INDETERMINATE
                                            1 PI-UNCLASSIFIED-SHAPE (C014)
```

So E2-REP is the dominant STOP gate, and every criterion rejection in
the run so far occurred there -- but most E2-REP stops are protocol or
transport indeterminacy, which is a fact about our observation
conditions, not an elimination by the criterion. Conflating the two
would inflate what the gate is doing, in the same direction as the
withdrawn "large fraction" claim above.

**Nothing is changed in response to this.** Tightening E4 now, having
seen three passes, would be exactly the post-hoc criterion narrowing
this run has withdrawn verdicts over twice (QA-12, QA-13). The
observation is recorded so that it is on the record BEFORE the eligible
set is complete, rather than discovered afterwards as a surprise about
what the screening measured.

What it would mean for reporting, if the hypothesis holds: many eligible
candidates would be a finding about E4's discriminating power, not a
finding that these projects are unusually well-structured, and the
tie-break rather than the gate would be doing most of the selection work
-- which is precisely why it was sealed in advance. If it does not hold,
the record already says the expectation was a hypothesis.

## QA-17 — a criterion's wording cannot widen the search contract (VERDICT WITHDRAWN)

C014's E2-REP rested on two observations the sealed navigation contract
did not allow, and both failures share one shape: a rule was treated as
adjustable because following it looked like it would lose information.

```text
opened Downloads      justified from the criterion's phrase
                      "a repository or source distribution"

used the README's     justified by narrowing the read to a targeted
designation sentence  scan for designation vocabulary
```

**The contract governs execution; the criterion governs meaning.** When
they differ in reach, this run follows the contract. A criterion phrase
describes what would satisfy the gate; it does not enumerate where we
may look. Reading it as permission to open a surface the whitelist omits
turns every criterion into a general search warrant -- and the moment
that widening is triggered by a landing page not exposing what was
expected, the search scope has become a function of what was found,
which is the thing the whitelist exists to prevent.

**Narrowing a forbidden act is not permission to perform it.** The
contract forbids reading README prose and instructs that an incidentally
rendered README be quarantined. Scanning only for designation vocabulary
reduced how much prose was read; it did not make reading it allowed. The
entry's own care in describing the scan -- written to be transparent --
is what makes the breach legible now, which is the argument for
recording such steps rather than smoothing them.

**Why the re-determination is UNRESOLVED.** Stated so that no
quarantined observation does verdict work:

```text
PASS not established
  admissible evidence does not establish the required upstream
  designation. It gets close -- one upstream-controlled location, not
  a fork or mirror, holding the source tree, its website field naming
  the official site -- but affiliation is not designation.

FAIL not established
  admissible evidence does not establish that upstream designates no
  canonical source location either. Two surfaces came up empty; that
  is not a demonstration that the project designates nothing.

contamination
  forbidden exposure occurred at this gate, which independently
  prevents reconstructing a clean adjudication after the fact.

therefore  E2-REP = UNRESOLVED / PI-UNCLASSIFIED-SHAPE
```

An earlier draft of this entry ruled FAIL out differently -- by saying a
designation exists and this run has seen it. That is true, and it was
the wrong argument to make. The designation is quarantined evidence, and
using it to decide even a negative lets quarantined evidence do verdict
work through the back door. The quarantine holds only if the forbidden
observation is treated purely as **provenance** -- a fact about how this
run's observation process went -- and never as evidence about the
candidate. Both branches above rest only on admissible surfaces; the
contamination line records what happened to the process, and rules
nothing in or out on its own.

What contamination does add is that the question cannot simply be
re-argued. Whether the admissible metadata reaches "the project
identifies this as authoritative" is genuinely arguable, and any
argument assembled now would be assembled by an analyst already exposed
at this gate. The repair is to decline the verdict.

**The gap is the protocol's, not the candidate's.** Where a project's
official site exposes no Source/Code/Repository/Development link, the
sealed navigation terminates at step 1, and E2-REP must then be answered
from repository metadata alone. The contract neither declares that
sufficient nor declares it insufficient. C010 and C012 did not expose this because their
HOMEPAGE was the repository itself, making landing page and source
location one surface.

A future run can close it by preregistering, before any candidate is
seen, either a bounded README designation-scan as an allowed observation
(with the scan's vocabulary fixed in advance), or an explicit rule for
what repository metadata alone is sufficient to establish designation.
Adding either now, having seen which candidate it would rescue, would be
fitting the contract to a result.

**Effect on the ledger.** C014 becomes UNRESOLVED at E2-REP; its
E2-RULE, E3 and E4 entries are quarantined as post-stop exposure. The
eligible set returns to C010 and C012.

## QA-18 - two frame items were skipped in the frozen order (DEVIATION, correctable)

Ranks 9 (`emulators/fceux`) and 13 (`emulators/mednafen`) have no frame
row, no candidate row and no verdict. Screening ran 8 -> 10 -> 12 -> 14,
passing over both.

```text
terminal ranks   1 2 3 4 5 6 7 8 _ 10 11 12 _ 14 ...
missing                          9          13
```

Neither is absorbed by anything: no row carries them in `frame_items`,
and the only DUPLICATE in the ledger maps rank 106 to C105.

**Cause.** After the session resumed at rank 10, the next-rank pointer
was carried forward from what the previous turn named rather than
recomputed from the ledger. The even-numbered sequence looked
deliberate, and nothing checked it against the frozen list until now.

**What is recoverable and what is not.** These must not be run
together, and an earlier draft of this entry ran them together by
claiming the omission was "correctable at no methodological cost" and
that screening 9 and 13 now would "restore the frozen order". Neither
holds.

```text
RECOVERABLE
  coverage of all 128 frame items
  the two missing frame rows
  further order deviation from here on

NOT RECOVERABLE
  the frozen-order violation that has already occurred
  the fact that ranks 10, 12 and 14 were observed first
  the fact that those observations are already known to the analyst
  who will now screen ranks 9 and 13
```

Screening them now fills the two missing frame items and stops further
deviation. It does not retroactively restore the frozen order: the
actual screening history will read 8, 10, 12, 14, 9, 13, 15, not 8
through 15 in sequence. The order violation stands as a recorded
protocol deviation.

The methodological cost is therefore not zero -- order preregistration
was violated. Whether that cost invalidates any part of the Phase 3.5
result is deliberately NOT decided here. Inventing a penalty the sealed
rules do not contain would be a post-hoc rule addition, which is the
same class of move this run has withdrawn verdicts over. The obligation
now is to preserve the deviation in the record rather than to sentence
it.

Compared with QA-06: that was a reordering of items all eventually
screened, while this dropped two outright, and unnoticed it would have
reported 128 screened when 126 were. The difference in the other
direction is narrower than first written -- only that coverage can still
be completed without re-observing any rank that already reached a
terminal verdict.

**Disposition.** Screening resumes at rank 9. The frozen order is sealed
and takes precedence over the working assumption that everything below
15 was finished.

**Prior exposure to log.** Both ranks were touched during the voided
QA-07 batch: fceux's documentation.html and mednafen's /documentation/
were read while determining E3 for a group of candidates, and QA-07
records that no verdict was issued from that batch. Each candidate's
evidence must therefore carry:

```text
Prior exposure:  that docs surface was already read under QA-07
Use:             not used as a gate shortcut, and not used to choose
                 which surfaces to name; adjudicated from the start
                 under the current protocol
```

Recorded so it is visible where the gates are reached, rather than
surfacing later as an unexplained familiarity with the material.

**Rule carried forward.** After every candidate is closed, the next rank
is RECOMPUTED as the lowest rank in the frozen set with no terminal row
in the ledger. Not read from what the previous turn said, and not read
from this entry either -- "9, then 13, then 15" is a prediction, not a
pointer, and trusting it would reproduce exactly the failure being
recorded. A pointer carried in prose is not a pointer.

## QA-19 — the completeness gap survives one stage past E4, in ranking (POST-SEAL AMENDMENT)

C013's E4 entry ended with "the inventory stage should not have to
rediscover it". That sentence is wrong in the direction that matters,
and following it up is what exposed the gap.

The inventory stage must rediscover everything, and must look where E4
never went. E4 stops at the first positive construction; the inventory
has to be exhaustive, because Section 3.3's classes and the union rule
both depend on having found ALL admissible enumerators and authoritative
sources.

```text
E4          existential   one witness -> PASS -> stop looking
inventory   universal     needs the complete set
```

**Why this is not the same finding as QA-13.** QA-13 was about a gate's
negative branch, and the fix was available: make PASS positive-only and
send everything else to UNRESOLVED. Class A has no positive-only form,
because its second conjunct is an absence claim.

An earlier draft of this entry said "class B is NOT class A's
complement". That is wrong: the sealed definition makes B the
"otherwise" branch, so semantically it IS the complement. The correction
is about ROUTES. Determining B does not require proving the full
negation of A in every case, because B's first disjunct is existential:

```text
DECIDABLE BY WITNESS
  class A, first conjunct   one located enforcement enumerator
  class B, first disjunct   one located `asserted` enumerator
                            -- positive and stable; later discoveries
                            cannot undo it

NOT DECIDABLE without a complete inventory
  class A, second conjunct  no hidden `asserted` enumerator exists
  class B, second disjunct  no enforcement enumerator exists at all
```

So a candidate CAN be placed in class B, by one located `asserted`
enumerator -- positive and stable. What cannot be placed is a candidate
whose located enumerators are all `enforced`: class A would need the
absence proof, and class B's positive route lacks its witness.

```text
found an `asserted` enumerator  -> class B
otherwise                       -> UNRESOLVED
```

**"Located" means lawfully obtained.** A class B determination needs an
`asserted` enumerator that the run's permitted evidence process already
produced. Nothing here authorizes a fresh ad-hoc search through a
survivor for one. That search is exactly the discovery procedure whose
absence created this gap, and running it unpreregistered -- while
knowing that finding an `asserted` enumerator is what would make a
candidate classifiable -- would fit the inventory to the outcome. The
four current survivors' lawfully located E4 witnesses are all
`enforced`, so all four are UNRESOLVED.

The sealed methodology already treats an enumerator discovered after
selection as a protocol failure -- it knows the risk, it just never
operationalized the search. So the asymmetry contained at the gate is
load-bearing one stage later, where containment does not work.

**Resolution.** A second post-seal corrective amendment, in
`SCREENING_PROTOCOL.md`, dated to its cause.

```text
CLASS       located `asserted` enumerator -> B ; otherwise UNRESOLVED

THIS RUN    C009  UNRESOLVED      every located E4 witness is
            C010  UNRESOLVED      `enforced`, so none of the four has
            C012  UNRESOLVED      the positive class B route
            C013  UNRESOLVED

OUTCOME     multiple eligible + an undecided class boundary
              -> ranking NOT DECIDABLE
              -> primary target NOT SELECTED
              -> selection INCONCLUSIVE
```

With exactly one eligible candidate the outcome would differ in one
respect only: target identity would be settled, since there is nothing
to rank. `U_primary`, `P_raw` and E5 would still be unavailable, because
they depend on a complete frozen inventory rather than on the count of
candidates.

**Where the code goes.** `PI-UNCLASSIFIED-SHAPE` marks this at the run
and inventory level -- here and in the report -- and NOT in the
candidate ledger's `protocol_issue_code` column. That column is a
gate-level candidate outcome paired with `overall = UNRESOLVED`; putting
it on an ELIGIBLE row would assert a gate was left undetermined, which
is false. All six gates were determined for each survivor. Eligible rows
keep `protocol_issue_code = NONE`.

The tie-break is explicitly barred as a fallback. Using it across an
undecided class boundary assumes the survivors share a class — a claim
about them, not a simplification — and it would return a wrong candidate
while looking as principled as it does when used correctly.

**Already knowable, so stated now.** Four candidates are eligible and
every located E4 witness is `enforced`, so no survivor has class B's
positive route; ranking will be required across an undecided boundary
and the selection outcome is already determined to be inconclusive. Recording that at the moment it becomes knowable is
the same discipline QA-16 applied to E4's discriminating power.

**Screening still completes.** The 128-item result is the run's outcome
in its own right, and the coverage claim depends on finishing it.

**What the run becomes.** Not a target study. A screening-methodology
result: a protocol can be rigorous enough to ADMIT candidates and still
unable to SELECT among them, because admission is existential and
selection is universal. That is a finding about the design, obtained
because the design was written down before it was executed and its
verdicts were checked against it. It is worth more than a target chosen
by a rule that could not support the choice.

**Alternatives rejected:** writing the discovery procedure now (no
longer preregisterable — four registry idioms have been seen, and probes
would be fitted to them), and treating the screening-stage positive
enumerator as the inventory (nullifies the union rule and the
late-discovery failure rule together).

## QA-20 — the contract can establish repository identity but not repository content (VERDICT WITHDRAWN)

C016's E2-REP was determined by downloading the repository's own archive
of its default branch and listing its entries, because the allowed root
surface did not carry a file listing. That is one step past step 3, and
it is withdrawn.

The defence written into the entry was that the archive is generated by
the same repository and is therefore not a different canonical location.
True, and beside the point: the objection is navigational, not about
identity. The shape is C014's exactly.

```text
the fact the gate needed was not available at the allowed surface
  -> a further surface that could supply it was opened
```

C014 settled the principle: **the contract governs where we may look,
the criterion governs what would satisfy the gate.** Listing "that a
source tree is actually present" among allowed OBSERVATIONS says what
would satisfy the gate. It does not authorize a SURFACE the navigation
omits. Reading it as authorization makes every allowed observation a
warrant to go find it, which is the whitelist dissolved.

**The gap, stated as a capability rather than as a vendor quirk.**

```text
where the allowed repository root establishes repository IDENTITY --
name, owner, default branch, non-emptiness, fork/mirror/archive status
-- but does not itself expose enough to establish that an actual SOURCE
TREE is present, the sealed navigation contract provides no authorized
follow-up surface. Opening a generated archive, a tree endpoint or an
API would extend step 3 after seeing that the root was insufficient.
```

This is not "GitLab renders client-side". That is merely how the gap
surfaced first. Any host whose root surface omits a listing produces the
same shape, and the run's earlier candidates only avoided it because
their host happened to embed the tree in the served HTML -- an accident
of rendering, which is a poor thing for a verdict to depend on.

**Expect recurrence, conditionally.** The prediction has to be stated on
the shape, not on the host -- binding it to a vendor one sentence after
calling it a capability gap would undo the point.

```text
if a later candidate reaches an allowed repository root that
establishes IDENTITY but carries no source-tree evidence,
the same gap applies, whatever the hosting vendor
```

Hosting alone predicts nothing: a candidate on the same host may stop at
an earlier gate, may have a landing page that designates a source
distribution instead, or may have a root surface that does expose a
listing. What recurs is the shape.

Recording the expectation now, before the next such candidate arrives,
keeps it from looking like a rule discovered to suit a case.

**Why UNRESOLVED and not FAIL.** No E2-REP failure code applies.
Upstream designates exactly one location in as many words, at a stable
URL, with one target identifier. `E2REP-NO-SOURCE` is a claim about
access to the source representation, and nothing admissible supports
asserting it: what happened is that we could not make the observation
within the contract, not that the source is unavailable. Coding our own
navigational limit as a property of the candidate is the error this run
has withdrawn verdicts over repeatedly.

**Effect on the ledger.** C016 becomes UNRESOLVED at E2-REP; its
E2-RULE, E3 and E4 entries are quarantined as post-stop exposure. The
eligible set returns to C009, C010, C012 and C013. Selection remains
INCONCLUSIVE -- those four already make ranking undecidable, so nothing
about QA-19's conclusion moves.

**Future runs.** A run may close this by preregistering, before any
candidate is seen, one authorized follow-up surface for establishing
source-tree presence when the root does not carry it -- a tree endpoint,
a repository API listing, or a generated archive listed by name only --
with the choice fixed in advance rather than made when a root turns out
to be insufficient.

## QA-21 — arriving at a repository is not upstream designating it; and a gate-order slip

Two things, one of them mine.

**The adjudication.** C017's frozen metadata names no HOMEPAGE and no
SITES. The only upstream surface the contract reaches is the repository
that GH_ACCOUNT/GH_PROJECT point at. Its root establishes repository
identity, upstream affiliation and source-tree presence -- and stops
short of upstream designating it as canonical source.

That is C014's boundary applied unchanged: **affiliation is not
designation.** E2-REP is therefore UNRESOLVED / PI-UNCLASSIFIED-SHAPE.
FAIL is equally unavailable: not finding a designation at the one
reachable surface does not show none exists.

**Why C010 and C012 do not follow it down.** The distinction is
navigation topology, not evidential weight between metadata fields. An
earlier draft of this reasoning put it as HOMEPAGE being "a fact about
upstream" while GH_* is "a packaging instruction". That is wrong: both
are frozen OpenBSD starting points, and neither is upstream evidence in
itself.

```text
C010   frozen starting URL IS the project landing surface
       and IS the repository root      -> step 1 = step 3     PASS stands
C012   same                            -> step 1 = step 3     PASS stands
C014   a separate project site exists, designating no source    UNRESOLVED
C017   no project landing URL; a packaging identifier reaches
       a repository and nothing more                            UNRESOLVED
```

C010's and C012's execution records already say steps 1 and 3 collapse
onto one surface. C017 has no admissible upstream evidence making its
repository root a step-1 project surface. Reopening the two would
require newly holding that a frozen starting URL which IS the repository
root cannot count as the project landing surface -- a change to
navigation semantics applied throughout this run, made after the fact
and not required by anything C017 presents.

**`isArchived: true` is not a failure ground.** No sealed rule says an
archived repository cannot be a canonical source location. The URL is
stable and the source tree is present. It is recorded as an observation
and nothing more, because coding an incidental property as a criterion
failure is how gates quietly acquire rules nobody sealed.

**The gate-order slip, recorded as mine.** The sealed order is
UR -> E1 -> E2-REP -> E2-RULE -> E3 -> E4, and screening stops at the
first gate that is not determined. I recognised mid-way that C017's
E2-REP was genuinely hard, and then kept reading -- the man page, the
option constraints, highscore.c, the interface headers -- before
settling it. Those observations are quarantined as post-stop exposure
and logged by name in the evidence file.

The cost is concrete rather than theoretical. Among the material read
early is a line in man/2048.6 -- "All contributions can be found at
https://github.com/Tiehuis/2048-cli" -- that reads like exactly the
upstream designation E2-REP was asking for. Having seen it, I can no
longer claim an uncontaminated adjudication of that question even if the
contract had permitted the surface, which it does not. Reading ahead
does not merely waste effort; it can destroy the very verdict it looked
like it might help.

**Rule carried forward.** Difficulty at a gate is a reason to stop and
adjudicate it, not a reason to gather more elsewhere. If a gate cannot
be settled on its permitted surfaces, the next step is UNRESOLVED, not
the next gate's material.

## QA-22 — the exemption I carved for C010 and C012 was the withdrawn move in another shape

QA-21 established that repository identity, upstream affiliation and
source-tree presence do not amount to upstream designating a canonical
source. It then exempted C010 and C012 on the ground that their frozen
starting URL was simultaneously the project landing surface and the
repository root, so navigation steps 1 and 3 collapsed.

The exemption does not hold, and the reason is worth stating precisely
because the argument looked structural rather than convenient.

**`step 1 = step 3` answers a different question.** It settles WHICH
SURFACE may be looked at. It says nothing about whether upstream
designated that location. The sealed contract keeps these apart itself:
"whether upstream designates this location as its source" is listed as
its own allowed observation, beside repository identity and source-tree
presence. Collapsing the navigation does not collapse the questions.

**And what actually distinguished them was a field name.** C010 and
C012 qualified because their OpenBSD HOMEPAGE happened to contain a
repository URL. Letting that carry the designation lets an OpenBSD field
supply evidential force for an upstream fact -- withdrawn at C014, again
at C017, and reintroduced here under a structural-sounding label.

```text
C010/C012   OpenBSD HOMEPAGE           -> GitHub repository root
C017        OpenBSD GH_ACCOUNT/PROJECT -> GitHub repository root
```

Different routes, same kind of upstream evidence at the end of them.

**Both become UNRESOLVED / PI-UNCLASSIFIED-SHAPE**, and their E2-RULE,
E3 and E4 entries are quarantined as post-stop exposure.

**Why C009 and C013 are not touched.** Neither rests on inference from
repository existence. Each has an upstream-authored arrow on an upstream
surface:

```text
C009   fceux.com exposes a link whose destination IS the repository
       ("checking the commit browser"), so the project's own page
       points at the location -- the arrow C014 lacked

C013   mednafen.github.io presents the source tarball itself, on the
       project's own domain, with its SHA-256 published beside it
```

In both, an upstream surface performs the designation. That is what
C010 and C012 never had.

**What this costs and what it does not.** The eligible set drops to two.
Selection remains INCONCLUSIVE and for the same reason as before: C009's
and C013's lawfully located enumerators are all `enforced`, so neither
has class B's positive route, both are class UNRESOLVED, and ranking
across an undecided boundary is not available. QA-19's conclusion does
not move.

**The pattern to name.** This is the fourth E2-REP verdict withdrawn,
and all four failed the same way: something that was not upstream
designation was allowed to stand in for it -- a downloads page, a
README sentence, a generated archive, and now a field name. The gate
asks one narrow question, and nearly everything available at screening
depth is adjacent to it rather than an answer to it.

**Rule carried forward.** Before recording an E2-REP PASS or a
positive-shaped FAIL, name the upstream surface that performs the
designation and record its exact designation signal -- a sentence, a
label, a link relation, or a structured marking. Not every designation
arrives as prose: C009's is a link on the project's own page whose
destination IS the repository, and forcing that into a quoted sentence
would misdescribe it. If the answer is "the repository exists and is the
project's", that is affiliation, and the verdict is UNRESOLVED.

## QA-23 — record-only audit of every REJECTED verdict against QA-17 and QA-22

QA-22 named a pattern across four withdrawn E2-REP verdicts: something
that was not upstream designation was allowed to stand in for it. A rule
that only binds future verdicts leaves the ledger inconsistent with
itself, so the five standing REJECTED verdicts were audited against it.

**Method, and its limits, fixed before looking.**

```text
scope       the five REJECTED candidates only
material    the evidence file as already written
forbidden   any new upstream access, any new surface, any new fact

questions   1. was every designation signal the verdict needs
               observed at a permitted surface?
            2. did a forbidden Downloads page, hub expansion or extra
               hop do verdict work?
            3. does the positive multi-designation FAIL still stand on
               permitted evidence alone?

            any no -> UNRESOLVED
```

The prohibition on new access matters: re-visiting these endpoints to
shore up a verdict would grant them a second observation opportunity
under different conditions, which QA-06 already ruled worse than the
deviation it would repair.

**Withdrawn: C002 and C007.**

C002's path ran landing page -> download.html -> tarballs and hub ->
the hub's repository. QA-17 had already settled that `Downloads` is
outside step 2 and that the criterion's "source distribution" may not
widen the whitelist. Both designations came from past the contract.

C007's two locations were read off the SourceForge hub, not the landing
page, and a generic project hub is not a repository root either -- so
the finding needed a hop past step 3 as well.

**Standing: C006, C011, C015.** The batch header shared by C006, C007
and C011 says "and the pages it explicitly exposes", which is over-broad
and on its own would leave the provenance unclear. The timestamp line
settles it rather than charity does:

```text
observed_at_utc: ... (landing pages); 05:32:16Z (DOSBox SourceForge
hub, rank 7 only)
```

"rank 7 only" confines the hub visit to C007. C006 and C011 rest on
landing-page observations, and neither verdict cites content from a
linked page. C015's two designations are quoted verbatim from the
landing page body.

**Why this mattered more than fixing C002 alone.** Withdrawing these one
at a time as each was noticed had become the run's failure mode: four
E2-REP retractions, each triggered by review rather than by audit. An
audit converts the pattern into a sweep and ends the drip.

**Result.** ELIGIBLE 2 / REJECTED 3 / UNRESOLVED 25. Selection remains
INCONCLUSIVE for the unchanged reason.

**What the ledger now says about the gate, and what it does not.**

```text
run-to-date, 28 terminal non-eligible candidates
  stop at E2-REP    26      criterion REJECTED       3
                            UNRESOLVED              23
  stop at E4         2
```

The composition is worth recording: most E2-REP stops so far are
observation or protocol limitations -- transport failure, or a contract
that could not reach the fact -- rather than eliminations by the
criterion. That distinction is only visible because the two kinds were
kept apart (QA-16).

This is a descriptive run-to-date observation and NOT a prevalence
estimate for the frozen 128-item frame. The terminal set is neither a
complete sequential prefix nor a random sample: it mixes ranks 1-17 with
the QA-06 batch (21, 27, 39, 40, 41, 55, 70, 73, 79, 86, 105, 109, 110),
which were processed early precisely BECAUSE their outcomes were
transport-determined. Reading 26/28 as "about 93% stop at E2-REP" would
launder that selection into a rate.

Frame-wide proportions wait for completion, on the same footing as
QA-16's E4 hypothesis.

## QA-24 — an admitted surface cannot be declined for a reason that only bounds it

C018's first E2-REP entry reached the right verdict by an argument with
three defects, one of them structural enough to name.

The entry stated that no other allowed upstream path existed, and then
that the OpenOrphanage account page was an admissible starting point.
Both cannot hold. The second is correct: the contract admits "the URLs
and identifiers found in the frozen OpenBSD metadata", and the DIST_TUPLE
account token is one.

Having admitted it, the entry declined to open it, reasoning that
choosing a differently-named repository from that account would be our
adjudication of the target's identity. That reasoning is sound about
what must not be DONE at the surface. It is not a reason to leave the
surface unobserved.

```text
a reason that constrains WHAT MAY BE OBSERVED at a surface
  -> bound the observation, declare the bound first, then look

a reason that makes a surface UNNECESSARY
  -> the criterion no longer needs it, or already-observed structure
     has settled the question
```

QA-11 fixed necessity as the second of these. C018 met it: the gate was
unsettled and this was the remaining admitted identifier. So the surface
was necessary, and skipping it was the mirror image of the error QA-11
was written for -- there a necessary surface was pre-named and then
substituted for; here one was admitted and then skipped.

Bounding it costs little and is auditable. The scope written into
EV-C018-E2REP-02 was fixed before the request: account existence, an
explicit profile website or migration notice, an explicit designation of
where the source now lives -- and explicitly not selecting a repository
by name similarity or inferring a successor. As it happened the account
returns 404 as well, so the bounded observations had nothing to return
and the prohibited ones nothing to tempt with. The verdict is the same
UNRESOLVED, now closed on both admitted surfaces instead of one.

**Two smaller corrections, recorded because both were arguments the
verdict did not need.** The entry asserted the candidate "would have
been UNRESOLVED had the endpoint returned 200", which is not knowable
before opening it -- QA-23 had just generalised the designation signal
to include labels, link relations and structured markings, any of which
could have sat in owner-controlled metadata. And it argued from GitHub's
301-on-rename behaviour that no rename had occurred; two 404s and a
same-host control establish the endpoint's present state, which is all
the gate asks, and the platform-semantics claim is dropped.

**Rule carried forward, stated narrowly.** An earlier draft of this
entry read "when a surface is admitted and the gate is unsettled, it
gets observed". That is too strong, and it collides with a distinction
the contract and QA-11 already make: **admitted is not necessary.**

```text
admitted + necessary under QA-11  -> observe
  and if the surface carries a risk of analyst overreach:
    1. fix the allowed observation scope before opening it
    2. observe only within that scope

admitted alone                    -> no obligation to observe
```

QA-11 fixed necessity as the criterion's live question plus
already-observed structure leaving the verdict unsettled WITHOUT that
surface. Admission says where we may look, not where we must.

The run already relies on this. C010's frozen SITES was an admitted
starting point and was deliberately not opened, because the port
Makefile's own dist: target had already shown the host to be
packager-side -- observed structure had made it unnecessary to the
designation question. If admission alone created an obligation, that
decision would have been wrong, and it was not.

C018 holds under the narrower rule for the reason it always did:

```text
repository endpoint -> definitive 404
gate still unsettled
account token = the remaining admitted identifier
the criterion's question was still potentially answerable there
  -> necessary
  -> scope fixed in advance
  -> observed
```

## QA-25 — a designated ROUTE is not a designated LOCATION

C020's withdrawn E2-REP counted "You can also use anonymous cvs to get
the latest development sources" as a second canonical source location.
It is not one. It is an announcement that a route exists, with the
location one hop further on, in a page that was not opened.

E2-REP counts canonical source LOCATIONS, and requires each to sit at a
stable URL. A location that was never observed cannot be counted, in
either direction -- it cannot complete a multi-designation FAIL, and it
cannot be assumed absent.

The distinction is visible by comparison with the two candidates whose
arrows did complete on the permitted surface:

```text
C015  the landing page body carried the location itself
      "git clone http://shamusworld.gotdns.org/git/virtualjaguar"

C009  the link's DESTINATION was the repository
      "commit browser" -> github.com/TASEmulators/fceux/commits/master

C020  landing page -> cvs.html, an instructions page
      location unobserved
```

QA-23 generalised the designation signal to include a link relation
precisely so that C009's case would not have to be forced into prose.
That generalisation is about the FORM the signal may take. It does not
license treating a link to instructions as equivalent to a link whose
destination is the location.

**A second slip in the same entry, worth naming separately.** It
presented the download table's `source | CVS | "Unreleased snapshot of
CVS repository"` row next to `source | 1.4` as though they might be
distinct locations. By its own annotation that row is a source
DISTRIBUTION taken from the repository, served from the same path as the
versioned tarballs. Reading a row's CONTENTS as though they indicated a
different LOCATION is the same conflation one level down.

**cvs.html was not opened to repair this.** C020 had been recorded as a
terminal FAIL, and adding a fresh upstream observation to rescue a
terminal verdict is what QA-21 exists to stop. The gate is re-determined
on what was admissibly observed, and lands on UNRESOLVED.

**Rule carried forward.** Before counting a location toward E2-REP --
for a PASS or for a multi-designation FAIL -- record the location
itself: a URL, an endpoint, or a link whose destination is the location.
"Upstream says you can get source this way" establishes a route, and a
route is not a location.

## QA-26 — several repositories on one project page are not automatically competing designations

C024's withdrawn E2-REP counted both repositories liballeg.org exposes
as competing canonical source locations for one candidate, and failed it
for having no primary. The argument ran backwards.

E2-REP asks whether upstream designates a canonical source location **for
the system under examination**, not how many repositories the project
has. When upstream itself partitions its repositories and labels the
parts, applying that label is not analyst selection:

```text
upstream's own words
  "We've moved Allegro 4 sources to its own repository."  -> allegro4
  navigation "Git repository"                             -> allegro5

UR resolved the port to  allegro-4.2.3
```

The withdrawn entry treated "the candidate is Allegro 4, so allegro4 is
its location" as the C002-family error -- adjudicating which of several
repositories really holds the system. It is the mirror image of that
error. C002's fault was SUPPLYING a hierarchy upstream had not stated;
here upstream states the partition and the entry declined to use it.

**Rule carried forward.** Before counting a second location toward a
multi-designation FAIL, check whether upstream's own labels assign it to
a different delimited system or version line. Multiplicity has to be
multiplicity FOR THIS CANDIDATE.

**Why the corrected verdict is UNRESOLVED and not PASS.** E2-REP also
requires the designated location to hold a source tree, observed at its
root. The withdrawn entry stopped at step 1 on a FAIL and never opened
allegro4. Opening it now would be observation after a terminal verdict.
That restraint has cost the run a verdict before -- C020's cvs.html --
and it costs one here.

The two are worth contrasting, because they fail at different places:

```text
C020   a second ROUTE was announced; the location itself was never
       observed, so the multiplicity could not be established

C024   the candidate-specific LOCATION is designated and observed as a
       designation, but its step-3 source-tree property was never
       observed
```

**Effect.** C024 becomes UNRESOLVED / PI-UNCLASSIFIED-SHAPE. Its closing
claim -- that this was the run's first repository-versus-repository
E2REP FAIL -- is withdrawn with it; no such finding stands.

## QA-27 — a frozen SITES URL is an admitted starting point, not a navigation step

C026's first E2-REP entry called the frozen HOMEPAGE "the only
admissible surface" and stopped there. The frozen metadata also carried
`SITES=${HOMEPAGE}download/`, which the contract admits as a starting
point in its own words: "the URLs and identifiers found in the frozen
OpenBSD metadata".

The entry applied QA-24 to the landing page's links and not to the
metadata's own URL. The two are different, and keeping them apart is the
whole of this correction:

```text
landing page's "Other downloads" -> download.html
  a NAVIGATION step past step 1, to a label the whitelist omits
  -> forbidden by QA-17

frozen SITES /download/
  an ADMITTED STARTING POINT supplied by the metadata
  -> not navigation; needs no whitelist label to be observed
```

Both facts can hold at once, and here they do: download.html stays
closed, and /download/ had to be opened.

**Admitted was also necessary here**, which is the QA-24 test rather
than mere admission. The gate was unsettled after the landing page,
/download/ was the remaining admitted starting point, it sits on the
same upstream domain, and nothing had established it as packager-side.
That last clause is precisely what let C010's SITES go unopened: its
port Makefile's own dist: target had already shown the host to be the
packager's. C026 had no such finding, so the exemption did not transfer.

**Repairing rather than living with it.** C018 set the precedent -- a
necessary admitted surface that was skipped gets observed under a scope
fixed in advance, and that repair is where QA-24 came from. This is not
the C020/C024 situation, where a TERMINAL verdict would have been
rescued by fresh observation. There the observation would have been the
error; here the omission was.

**What the surface turned out to be.** 403 Forbidden on both GET and
HEAD, with the same-host landing page returning 200 at the control
moment. Transport completed and the server answered definitely, so this
is not the timeout / DNS / refused / 5xx family. It is equally not
evidence of absence, of designation, or of source-tree presence: the
response reveals nothing about the URL's contents.

Two things are deliberately NOT claimed. That the server distinguishes
this path from a missing one -- no nonexistent-path control was
requested, so the comparison was never available. And that the resource
exists -- what is established is that a request to this URL was answered
Forbidden, twice. The verdict code is unchanged, and the evidence base
now includes the surface that should have been observed the first time.

**Rule carried forward.** Before declaring the admissible-starting-point
set exhausted, enumerate every URL and identifier the frozen metadata
supplies and record what became of each:

```text
observed, because necessary under QA-11
lawfully skipped, because observed structure made it unnecessary
otherwise resolved under the protocol, with the reason named
```

Stated this way on purpose, so it does not re-inflate QA-24 into "every
admitted surface must be opened" -- the distinction QA-24 was itself
narrowed to preserve. The obligation is to account for each, not to open
each.

A URL in the metadata does not become inadmissible because the landing
page happens to reach the same place through a label the whitelist
omits.

## QA-28 — observation-time identity cannot reconstruct pointer or designation state at the sealed instant

C029 exposed a gap in how this run has been resolving `primary_snapshot`
for distribution candidates, and it is a firewall gap rather than a
bookkeeping one.

The sealed rule fixes which bytes get analysed BEFORE anything
downstream is read:

```text
distribution candidate
  the externally designated canonical artifact at the ENUMERATION
  EXECUTION TIMESTAMP, recorded by content hash
```

Screening observation happens later, on a separate time axis the
protocol insists must not merge with it. So resolving the snapshot needs
something that bounds the designation backwards to the enumeration
instant. Observing today's designation does not do that.

**What each distribution survivor actually had.**

```text
C013 mednafen
  landing page presents releases as a DATED News list, newest first
  top entry: "Mednafen 1.32.1, April 5, 2024", SHA-256 published

C029 angband
  landing page presents "Download version 4.2.6" with NO date, and no
  dated release list on the permitted surface
```

An earlier draft of this entry read C013's dating as closing the
question -- "the newest entry predates the enumeration timestamp by over
two years, so the designation could not have changed in between" -- and
declared its snapshot established. That is the same substitution C029
was withdrawn for, one gate later and in gentler clothing.

```text
a dated release entry establishes
  when that release was published
  what is designated AT OBSERVATION TIME

it does not establish
  what was designated at the sealed instant
```

A release date is not a designation interval. Nothing in either record
closes the window between the enumeration instant and observation, so
neither observation establishes the sealed-instant snapshot. Where that
leaves each candidate differs, and the difference is the stage they
reach:

```text
C013   E1-E4 screening verdicts remain active.
       primary_snapshot is UNRESOLVED at the survivor stage.

C029   never reaches snapshot resolution, because E2-REP is
       UNRESOLVED on uniqueness.
```

An earlier draft of this paragraph said both candidates' later gates
were quarantined and C013 withdrawn. That was RETRACTION 15's stage
error, corrected below and in RETRACTION 16.

**The same structure exists on the repository branch, and it does not
survive either.** The general form of the error is one substitution:

```text
object history  !=  designation / ref history

distribution   a release date fixes when a release was published,
               not the interval over which it was designated

repository     a commit date fixes when a commit was made, not where
               the default branch ref pointed at a given instant
```

A commit object is immutable; a branch ref is not. That C009's HEAD
predates the sealed instant shows the commit existed by then, and
nothing about where master pointed then. "Master had not moved since
2026-05-30" was never observed -- what was observed is where it points
now. The evidence is stronger than the distribution case, since a commit
chain is not silently replaceable the way a file at a URL is, but it is
not closed, and this run has consistently stopped at "not excluded".

**Where the failure belongs, which an earlier draft got wrong by one
level.** RETRACTION 15 withdrew C013's E2-REP over this. That was a
stage error. The E2-REP network contract states its own purpose --
location, designation, stable URL, one target identifier, actual source
tree -- and the snapshot is not among them. The schema files
`primary_snapshot` with the fields "performed only for candidates
surviving E1-E4".

```text
NOT   an E2-REP criterion failure
BUT   a survivor-stage primary_snapshot resolution failure
```

C013 is restored as a survivor, and its E2-RULE, E3 and E4 entries come
out of quarantine: those gates were determined on their own witnesses,
and screening gates are not conditioned on a survivor-stage field.

**What is blocked, and what is not.**

```text
E1-E4 survivors          C009, C013, C023 -- three, unchanged

primary_snapshot         UNRESOLVED for all three
candidate inventory      blocked; cannot begin without frozen bytes
U_primary, P_raw         not obtainable
completeness class       not obtainable
ranking                  not decidable
primary target           not selected
```

The survivor set is not empty. Three candidates survive screening and
all three are stopped at the same later checkpoint, which is a different
and more informative outcome than having nothing survive.

**No resolution procedure is invented now.** A rule like "take the
newest ancestor of current HEAD dated before the instant" would select
from today's commit graph, which is not the same as recovering the ref,
and it would be a procedure written after seeing the candidates -- the
objection that has already sunk two attempted repairs in this run.
Nothing about a candidate's contents may be used to choose it either.

**The third preregistration hole.** This joins the two the run has
already recorded, and they are the same species:

```text
QA-13/amendment   E4 admissibility defined; discovery never
                  operationalized
QA-19/amendment   inventory completeness required; discovery never
                  operationalized
QA-28             snapshot rule preregistered; RECONSTRUCTION of the
                  sealed-instant state never operationalized
```

Each preregistered what it wanted and left unspecified how to obtain it
for a candidate first examined afterwards. That is the pattern worth
reporting, more than any individual verdict.

**Not applied to C004, C008 and C022.** Those ended UNRESOLVED at E4 and
never reached the survivor stage where a snapshot is resolved. Their
entries use "primary snapshot" loosely for an observation-time revision,
which is imprecise wording rather than a verdict defect, and re-filing
their stop gates would assert a survivor-stage failure they never
reached.

**Why this could not be patched.** Two repairs suggest themselves and
both change the sealed rule. Taking 4.2.5 because the port packages it
substitutes OpenBSD's packaging metadata for upstream designation, which
E2-REP forbids outright. Assuming 4.2.6 was already current a day
earlier assumes precisely what is unestablished. The /release page might
carry dates, but "Releases" is not among the contract's four step-2
labels -- and reaching for it after finding the landing page
insufficient is the widening QA-17 settled.

**Consequences for C029.** The Primary snapshot requirement sits inside
the sealed spec's E2-REP section, so an unresolvable snapshot is an
E2-REP-section failure: E2-REP is the stop gate, and E2-RULE, E3 and E4
are quarantined as post-stop exposure. That last part is the point worth
sitting with -- those three were determined by reading inside the 4.2.6
tarball, and the methodology binds downstream work to the frozen
snapshot. Verdicts read out of bytes that were never established as the
selected ones cannot stand, however sound the reading was.

`primary_snapshot` is also not one of the three fields
`PENDING_INVENTORY` covers. It is meant to be mechanically resolved by
the sealed rule, not deferred, which is why "flag it as a caveat for the
inventory stage" was the wrong disposition.

**What this case actually tested.** Phase 3.5's central firewall is that
which bytes get analysed is fixed before their contents are seen. C029
is the first candidate where that ordering was violated in the direction
that matters: the artifact was chosen by looking, then interesting E3
and E4 findings were read out of it. The findings are not why it was
withdrawn -- they would have been withdrawn identically had they been
dull.

**Rule carried forward.** For a distribution candidate, record what
bounds the designation back to the enumeration execution timestamp
before recording a snapshot hash. A dated release entry on a permitted
surface does it. "This is what is designated today" does not.

## QA-29 — a subresource of an admitted surface is not part of that surface

Raised at C042, from the same root as QA-17, QA-20 and the C037 deviation.

The frozen HOMEPAGE was a frameset: a document whose only content is references to five other documents. Fetching those five was justified on the ground that they are what the landing page RENDERS -- not onward destinations, just the page assembled.

The reasoning is wrong for a reason worth stating precisely, because "it was still a widening" alone does not distinguish it from a legitimate reading of the contract.

```text
the contract enumerates surfaces by NAVIGATION RELATION
  1 the landing page
  2 a Source/Code/Repository/Development link IT EXPOSES
  3 the repository root reached that way

it says nothing about composition, inclusion, or rendering
```

So there is no clause a frames argument can be a reading OF. The premise -- "these are the same surface" -- has to come from somewhere, and it came from us: a model of how browsers assemble documents. That is the analyst supplying scope, which is the one thing the contract exists to prevent. Whether the model is correct about browsers is beside the point; C014's Downloads page and C037's host root were also each defensible in their own terms.

Recurrence condition, bound to the shape rather than to framesets (the QA-20 lesson). It recurs whenever the argument for reading further has the form "this other document is really part of the admitted one" -- frames, server-side includes, iframes, a page whose content is fetched by script, a landing page that is a redirect stub. In every such case the joining relation is supplied by us, and the answer is the same: only the contract may extend a surface.

What this costs, recorded rather than repaired. Under the sealed contract, a frameset landing page is observable only down to "it declares frames". Such a candidate's step 1 can never be settled, and it goes to UNRESOLVED for a reason that is about our instrument rather than about upstream. That is a real limitation and it belongs in the reportable result -- not in a mid-run amendment, which would be a post-hoc criterion change of exactly the kind the run forbids.

What it does NOT license, so that this does not re-inflate the way QA-24 did: nothing here says a surface is inadmissible because it is "derived" or "secondary". Surfaces are admitted by the contract's own list -- frozen URLs and identifiers, and the two navigation steps. QA-29 removes an argument for adding to that list; it removes nothing from it.

## QA-30 — whether a hosting platform's project navigation carries upstream designation force is not settled by the sealed criterion

Raised at C044, where the frozen HOMEPAGE is a SourceForge project page and the only source-role location the page exposes is reached through the "Code" item in the navigation strip the platform renders on every such page.

The criterion asks whether UPSTREAM designates a single canonical source location. Platform chrome is an awkward fit in both directions:

```text
reading it AS designation
  the project chose this host, enabled the code area, and the strip
  appears on the project's own page under its own name; the label is
  literally one of the contract's four words

reading it as NOT designation
  the strip is rendered for every project whether or not it uses the
  areas; its presence is the platform's doing, not a sentence anyone
  upstream wrote; and it says nothing about which location is canonical
```

The sealed criterion contains nothing that chooses. This QA does not choose either -- inventing the rule now, with a candidate's verdict visible, is precisely the post-hoc criterion change the run forbids. It records the gap.

The gap is between PASS and UNRESOLVED, not between FAIL and UNRESOLVED. An earlier draft had it the other way, on the ground that the strip's Files item was a competing source designation; that was withdrawn at RETRACTION 21, because a generic artifact-area label that was never opened establishes no source location. What the two readings actually separate:

```text
chrome designates      "Code" designates the repository as the
                       project's source, and nothing competing with
                       it has been established -> PASS could follow

chrome does not        identity and source-tree presence at that
                       repository are affiliation only -> UNRESOLVED
```

Consequence, which is why it matters beyond one candidate. The reading decides whether a whole class of candidates can pass at all: any frame item whose HOMEPAGE is a project-hosting hub, whose source-role location is exposed only by platform chrome, and which carries no project-authored designation sentence. Under one reading such candidates pass E2-REP routinely; under the other none of them ever can. They currently go to UNRESOLVED / PI-UNCLASSIFIED-SHAPE for a reason about the instrument rather than about upstream, and this is a CLASS, not an incident.

Note also the direction of the risk, since it is not symmetric with the rest of the run's failure modes. Here the undecided rule is what BLOCKS a positive verdict; the run's usual danger is a rule invented to permit one. Neither is a reason to decide it now.

What this does NOT disturb:

```text
C023  passed on upstream's own dated relocation sentence, which
      designated a location without needing chrome to carry force.
      Its Code and Files areas were already recorded as platform
      furniture doing no work.

C006  its step 1 was the project's own site, where the locations were
      on a page upstream authored. QA-30 is about platform-rendered
      navigation and leaves that verdict untouched.

step 2  remains authorized by a link whose label is one of the four
        words. QA-30 says such a link does not by itself establish
        that upstream designates that location as canonical; it does
        not withdraw the permission to follow it (QA-22).
```

## QA-31 — a metadata-supplied starting point may fall inside a separately forbidden E2-REP surface class

Raised at C045, whose frozen SITES is
`https://github.com/yukiisbored/Launcher/releases/download/0.6.14.1-bgl/`.

An earlier draft called this a conflict between two sealed clauses. It is not, and the correction matters because "the contract contradicts itself" would license choosing a reading, while what is actually true licenses nothing.

```text
Allowed starting points
  "ONLY the URLs and identifiers found in the frozen OpenBSD metadata
   that UR already resolved to one system."

Forbidden at E2-REP
  "reading README prose / opening any source file / browsing docs /
   issues / PRs / changelog / RELEASES / ..."
```

The first clause bounds where a run may BEGIN. Its force is "not in the metadata, not a starting point" -- a necessary condition for admission. It does not say that presence in the metadata overrides a prohibition written elsewhere, and reading it as a sufficient condition is the move QA-17 already refused: a permission stated in one place does not widen the forbidden set.

So the clauses compose, and the composition is:

```text
in the frozen metadata          -> enters the starting-point set
surface class = releases        -> not observable at E2-REP
                                -> metadata-supplied but unobservable
                                   under the sealed contract
```

QA-27 supplies the disposition. Its carried-forward rule requires every metadata URL to be accounted for in one of three ways -- "observed, because necessary under QA-11 / lawfully skipped, because observed structure made it unnecessary / otherwise resolved under the protocol, with the reason named" -- and states that "the obligation is to account for each, not to open each". A forbidden surface is the third branch, with the prohibition as the named reason.

**Where the gap actually is.** Not in whether the surface may be opened; that is settled against opening. The gap is that the sealed protocol does not operationalize how E2-REP COMPLETES when a starting point that might have been necessary is one the contract forbids inspecting. The gate's PASS needs a designation witness, its failure codes need positive evidence, and neither can come from a surface the protocol itself closes. Nothing says what verdict that produces.

```text
-> UNRESOLVED / PI-UNCLASSIFIED-SHAPE, on the code's sealed definition:
   "a real screening outcome that no sealed criterion describes"
```

This is the same family as QA-13, QA-19 and QA-28: each preregistered WHAT was wanted and never HOW to obtain it in a case first met afterwards. It is not the QA-30 family, where the sealed criterion is silent on an evidential question and either answer would be ours to invent.

**What is NOT claimed.** Nothing about the unobserved surface's contents. An earlier draft argued that a releases page could only move a candidate toward PASS and could never complete a failure code, and used that to choose. That argument is withdrawn at RETRACTION 22 -- it constrains a page nobody read, which is the C033 and C035 error. A releases surface might carry one designation, several, an explicit primary or mirror relation, or nothing.

**Scope.** A class, not an incident: OpenBSD ports commonly point SITES at a code host's release assets. Every such frame item whose gate is still open after step 1 reaches this same point, and loses its second starting point to the prohibition.

**What this does NOT do.** It does not withdraw QA-27, which still requires a frozen SITES to be observed where no forbidden class is named -- C026, C031, C035, C036, C037 and C044 are unaffected. It does not make an unobserved surface into an empty one: C045's UNRESOLVED records that the contract closed the surface, never that upstream designates nothing.

## QA-32 — the E3 witness is not connected to U_primary membership

Recorded during screening, changing nothing in this run. No rule is added, no verdict moves, and no survivor's gate result is revisited. It is written down now, before the remaining frame items are screened, so that it cannot later look like a rationalization invented after the run ended.

**The gap.** E3 asks for a located stateful or temporal validity witness. The primary universe is built elsewhere:

```text
spec:349   U_primary = U_normative union U_enforced
spec:368   "U_enforced may be generated only by external enforcement
            enumerators that satisfy all EN1-EN6"
spec:356   U_normative contains observations from rule sources the
            project has explicitly designated as authoritative
```

Nothing routes an E3 witness into either set. A candidate can therefore pass E3 on one mechanism and pass E4 on an entirely different one, and the frozen `U_primary` need contain no stateful or temporal observation at all.

**It is not hypothetical here.** All six survivors have this shape; the two sides were read off the ledger's own entries rather than recalled:

```text
C009  E3 movie/savestate documentation      E4 src/ines.cpp bmap[]
C013  E3 multiple-CD documentation           E4 MDFNSetting registry
C023  E3 README "Visual Mode"                E4 Plugins.cs reflection
C038  E3 HighScores::Qualifies               E4 options_description
C043  E3 GameLogic mSquish collision test    E4 TextManager string table
C049  E3 fog-filtered placement validity     E4 unit-type variable registry
```

Six of six. Even C038, whose two witnesses live in the same file, satisfies the gates through different mechanisms.

**Why it matters.** Phase 3's architecture is about `WorldState`, `MonitorState` and provenance. E3 exists to establish that the candidate system HAS stateful validity, and it does. But the confirmatory lane runs against the frozen `U_primary`, so a target could be selected on the strength of an E3 witness whose subject matter never enters the universe the architecture is then validated against. That is a construct-validity gap, not an execution error.

**Where it sits relative to the other recorded holes.**

```text
QA-13, QA-19, QA-28   operational holes -- what was wanted was
                      preregistered, how to obtain it was not
QA-30                 an evidential question the sealed criterion
                      leaves undecided, where either answer would be
                      ours to invent
QA-31                 a completion rule missing for a starting point
                      the contract itself closes

QA-32                 different again: every rule needed is present and
                      was followed. The gates do what they say. What is
                      missing is a connection BETWEEN two of them, so
                      the run can satisfy each and still not deliver
                      what the gates were jointly meant to secure
```

**Explicitly not acted on.** Connecting E3 to `U_primary` now would be a post-hoc criterion change with six candidates' witnesses already in view, and it could only ever add or remove observations from a universe this run has in any case not reached -- every survivor's `primary_snapshot` is UNRESOLVED and the inventory stage is NOT_REACHED. It belongs in a future preregistration, before any candidate is seen.
