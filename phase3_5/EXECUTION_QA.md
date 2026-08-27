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

**Expect recurrence.** Every remaining GitLab-hosted candidate in the
frame will reach this same point. Recording the expectation now, before
the next one arrives, keeps it from looking like a rule discovered to
suit a case.

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
