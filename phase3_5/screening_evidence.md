# Phase 3.5 Screening Evidence Log

Grounds for every screening verdict recorded in
`screening_frame_items.tsv` and `screening_candidates.tsv`. Format and
rules fixed in `SCREENING_PROTOCOL.md`.

Each entry keeps `Observed` (what was directly seen at a named source)
separate from `Inference` (why that entails the verdict), so a later
reader can tell external fact from our reading of it.

Entries for frame ranks 1-3.

---
## EV-C001-UR-01
Candidate: C001 (frame rank 1, devel/flatzebra)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, devel/flatzebra/Makefile and distinfo
Observed: DISTNAME=flatzebra-${VERSION} with VERSION=0.2.0; SITES=http://perso.b2b2c.ca/~sarrazip/dev/; distinfo names flatzebra-0.2.0.tar.gz; HOMEPAGE=http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html; no GH_* fields present.
Inference: DISTNAME, SITES and the distfile all name one packaged system, flatzebra 0.2.0, served from one directory. HOMEPAGE points at a documentation page in that same directory; per SCREENING_PROTOCOL.md a documentation pointer is another fact about one system, not a second packaged system, so this is not UR-AMBIGUOUS.
Decision: PASS

## EV-C001-E1-01
Candidate: C001
Gate: E1
Source: same frozen metadata
Observed: the packaged system is authored and distributed by a third party (sarrazip), unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C001-E2REP-01
Candidate: C001
Gate: E2-REP
Source: http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html (HOMEPAGE) and http://perso.b2b2c.ca/~sarrazip/dev/ (SITES), both from frozen metadata
observed_at_utc: 2026-08-27T03:19:44Z (initial), 03:19:58Z (retry 1), 03:20:27Z (retry 2)
requested_url: as above; final_url: unchanged; http_status: 000 (no HTTP exchange); redirect_chain: NONE
evidence_role: official-project-page / official-source-location
Observed: DNS resolution failed for host perso.b2b2c.ca on all three attempts ("Could not resolve host"); an explicit DNS probe returned Non-existent domain. A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 03:19:59Z, so local network egress was functioning.
Inference: no HTTP-level answer about the endpoint was ever obtained. The sealed network contract classifies DNS failure as transport-level indeterminacy, not evidence of absence, and requires two recorded retries before recording a protocol issue. Both retries are exhausted. Note recorded, not acted on: the probe returned NXDOMAIN, an authoritative negative rather than a timeout, which the contract's wording does not distinguish -- see the checkpoint report; the rule was applied as written rather than adjusted mid-run.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C002-UR-01
Candidate: C002 (frame rank 2, devel/plib)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, devel/plib/Makefile
Observed: DISTNAME=plib-1.8.5; HOMEPAGE=https://plib.sourceforge.net/; COMMENT="suite of portable game libraries"; no GH_* fields.
Inference: one packaged system, PLIB 1.8.5, with a single project page. No field names a different system.
Decision: PASS

## EV-C002-E1-01
Candidate: C002
Gate: E1
Source: same frozen metadata
Observed: third-party authored library (S. J. Baker), unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C002-E2REP-01
Candidate: C002
Gate: E2-REP
Source: https://plib.sourceforge.net/ , https://plib.sourceforge.net/download.html , https://sourceforge.net/projects/plib/
observed_at_utc: 2026-08-27T03:20:44Z, 03:20:54Z, 03:21:27Z
http_status: 200, 200, 200; redirect_chain: NONE, NONE, 3 redirects http://sf.net/projects/plib -> https://sourceforge.net/projects/plib/
evidence_role: official-project-page / official-source-location
Observed: the project's own landing page exposes exactly one download-related link (download.html). That page exposes source distribution tarballs under dist/ (including dist/plib-1.8.5.tar.gz, matching the packaged DISTNAME) and a link to the project's SourceForge hub. The SourceForge project page exposes a code repository at /p/plib/code/. Neither the project pages nor the hub marks either location as canonical, primary, or authoritative relative to the other.
Inference: the sealed E2-REP criterion admits BOTH a repository and a source distribution as source-location types, and states directly that a project which "designates several with no primary among them" fails E2-REP. Upstream here exposes one of each and designates no primary, which is that case exactly.
Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

CORRECTION (recorded, not silently replaced): this entry first recorded
UNRESOLVED / PI-UNCLASSIFIED-SHAPE, on the reasoning that the criterion
allowed a second reading -- repository-is-source, tarballs-are-releases
-- and so did not determine the verdict. That was a misapplication, not
a gap in the spec. Treating the repository as the "real" source and the
tarballs as derived imposes a semantic hierarchy between the two; the
sealed criterion deliberately avoids that judgment by admitting both
types equally and disqualifying on the absence of an upstream-designated
primary. The observed facts are unchanged; only the application of the
rule to them was wrong.

## EV-C003-UR-01
Candidate: C003 (frame rank 3, devel/pygame)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, devel/pygame/Makefile
Observed: DISTNAME=pygame-${MODPY_DISTV}; PKGNAME=py-game-${MODPY_DISTV}; HOMEPAGE=https://www.pygame.org/; no GH_* fields.
Inference: one packaged system, pygame; PKGNAME is an OpenBSD Python-module naming convention, not a second system.
Decision: PASS

## EV-C003-E1-01
Candidate: C003
Gate: E1
Source: same frozen metadata
Observed: third-party authored project, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C003-E2REP-01
Candidate: C003
Gate: E2-REP
Source: https://www.pygame.org/ (HOMEPAGE, from frozen metadata)
observed_at_utc: 2026-08-27T03:22:00Z (initial), 03:22:11Z (retry 1), 03:22:12Z (retry 2)
requested_url: https://www.pygame.org/ ; final_url: https://www.pygame.org/news ; http_status: 502 on all three; redirect_chain: 1 redirect to /news
evidence_role: official-project-page
Observed: the official project page returned 502 Bad Gateway on all three attempts. A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 03:22:12Z, so local network egress was functioning. No source-location link could be read from the page.
Inference: 5xx is transport-level indeterminacy under the sealed contract, not evidence that no canonical source location exists; retries are exhausted. The contract restricts allowed starting points to URLs present in the frozen OpenBSD metadata, so no alternative entry point was attempted -- reaching the project by other means known outside that metadata would have violated the navigation whitelist.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)
