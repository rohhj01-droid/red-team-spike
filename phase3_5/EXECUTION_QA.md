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
