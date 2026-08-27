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

## QA-15 — the candidate schema has no value for "inventory not built yet" (FLAGGED, provisional)

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
the inventory stage, and the sealed methodology places that stage after
screening: Section 2 has screening run until the frame is exhausted or
the budget is reached, and the inventory is built between screening and
selection, with a discovery made *after* target selection recorded as a
protocol failure. Building inventories mid-screening would also let the
first survivor's structure inform how later candidates are read.

**Provisional disposition, flagged rather than settled.** Those three
carry `PENDING_INVENTORY`. `NOT_REACHED` was rejected because the
protocol defines it as "never evaluated", which would be false here --
the fields are not-yet, not never, and recording a false permanence to
avoid an unlisted token is the wrong trade.

`PENDING_INVENTORY` is a stage marker, not an outcome. It says nothing
about the candidate, cannot be a verdict, and appears in no gate
vocabulary. That is the reason it is admissible where a new *outcome*
code would not have been -- the amendment's objection to minting
vocabulary after seeing results is an objection to vocabulary that
changes what a result says.

This is recorded as flagged rather than closed: the choice governs
every future ELIGIBLE row, and if the run instead builds each
survivor's inventory as it is found, the token disappears and these
three fields are filled at screening time.
