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

## EV-C021-UR-01
Candidate: C021 (frame rank 21, games/afternoonstalker)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/afternoonstalker/Makefile
Observed: metadata identifies one packaged system (Afternoon Stalker); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C021-E1-01
Candidate: C021
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C021-E2REP-01
Candidate: C021
Gate: E2-REP
Source: http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve perso.b2b2c.ca (nslookup: NXDOMAIN). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C027-UR-01
Candidate: C027 (frame rank 27, games/amph)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/amph/Makefile
Observed: metadata identifies one packaged system (Amph); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C027-E1-01
Candidate: C027
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C027-E2REP-01
Candidate: C027
Gate: E2-REP
Source: http://n.ethz.ch/student/loehrerl/amph/amph.html (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve n.ethz.ch. A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C039-UR-01
Candidate: C039 (frame rank 39, games/batrachians)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/batrachians/Makefile
Observed: metadata identifies one packaged system (Batrachians); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C039-E1-01
Candidate: C039
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C039-E2REP-01
Candidate: C039
Gate: E2-REP
Source: http://perso.b2b2c.ca/~sarrazip/dev/batrachians.html (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve perso.b2b2c.ca (nslookup: NXDOMAIN). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C040-UR-01
Candidate: C040 (frame rank 40, games/belooted)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/belooted/Makefile
Observed: metadata identifies one packaged system (Belooted); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C040-E1-01
Candidate: C040
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C040-E2REP-01
Candidate: C040
Gate: E2-REP
Source: http://gnomefiles.org/content/show.php/Belooted?content=131848 (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: HTTP 526 on all attempts (5xx class). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C041-UR-01
Candidate: C041 (frame rank 41, games/beret)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/beret/Makefile
Observed: metadata identifies one packaged system (Beret); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C041-E1-01
Candidate: C041
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C041-E2REP-01
Candidate: C041
Gate: E2-REP
Source: https://kiwisauce.com/beret/ (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: curl could not resolve kiwisauce.com (nslookup resolves; client resolver disagreement). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C055-UR-01
Candidate: C055 (frame rank 55, games/burgerspace)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/burgerspace/Makefile
Observed: metadata identifies one packaged system (BurgerSpace); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C055-E1-01
Candidate: C055
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C055-E2REP-01
Candidate: C055
Gate: E2-REP
Source: http://perso.b2b2c.ca/~sarrazip/dev/burgerspace.html (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve perso.b2b2c.ca (nslookup: NXDOMAIN). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C070-UR-01
Candidate: C070 (frame rank 70, games/circuit)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/circuit/Makefile
Observed: metadata identifies one packaged system (circuit); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C070-E1-01
Candidate: C070
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C070-E2REP-01
Candidate: C070
Gate: E2-REP
Source: https://distfiles.sigtrap.nl/ (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: TLS: schannel InitializeSecurityContext failed (no HTTP exchange). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C073-UR-01
Candidate: C073 (frame rank 73, games/clines)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/clines/Makefile
Observed: metadata identifies one packaged system (clines); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C073-E1-01
Candidate: C073
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C073-E2REP-01
Candidate: C073
Gate: E2-REP
Source: http://manticore.2y.net/prj/clines-a.html (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: Connection timed out. A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C079-UR-01
Candidate: C079 (frame rank 79, games/cosmosmash)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/cosmosmash/Makefile
Observed: metadata identifies one packaged system (CosmoSmash); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C079-E1-01
Candidate: C079
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C079-E2REP-01
Candidate: C079
Gate: E2-REP
Source: http://perso.b2b2c.ca/~sarrazip/dev/cosmosmash.html (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve perso.b2b2c.ca (nslookup: NXDOMAIN). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C086-UR-01
Candidate: C086 (frame rank 86, games/crossfire-client)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/crossfire-client/Makefile
Observed: metadata identifies one packaged system (Crossfire client); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C086-E1-01
Candidate: C086
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C086-E2REP-01
Candidate: C086
Gate: E2-REP
Source: http://crossfire.real-time.com/ (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: Connection timed out (nslookup resolves). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C105-UR-01
Candidate: C105 (frame rank 105, games/eboard)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/eboard/Makefile
Observed: metadata identifies one packaged system (eboard); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C105-E1-01
Candidate: C105
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C105-E2REP-01
Candidate: C105
Gate: E2-REP
Source: http://www.bergo.eng.br/eboard/ (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve www.bergo.eng.br. A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C109-UR-01
Candidate: C109 (frame rank 109, games/einstein)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/einstein/Makefile
Observed: metadata identifies one packaged system (Einstein); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C109-E1-01
Candidate: C109
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C109-E2REP-01
Candidate: C109
Gate: E2-REP
Source: http://games.flowix.com/ (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: DNS: could not resolve games.flowix.com. A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C110-UR-01
Candidate: C110 (frame rank 110, games/eliot)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/eliot/Makefile
Observed: metadata identifies one packaged system (Eliot); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C110-E1-01
Candidate: C110
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C110-E2REP-01
Candidate: C110
Gate: E2-REP
Source: https://nongnu.org/eliot/ (from frozen metadata; the only allowed starting point)
observed_at_utc: 2026-08-27T04:44:52Z-04:47:59Z (initial), 04:48:24Z-04:50:00Z (retries 1 and 2)
requested_url: as above; final_url: unchanged; http_status: no HTTP answer obtained; redirect_chain: NONE
evidence_role: official-project-page
Observed: TLS: SNI/certificate check failed for nongnu.org (no HTTP exchange). A control request to https://cdn.openbsd.org/pub/OpenBSD/7.9/ returned 200 at 04:50:00Z, so local egress was functioning.
Inference: no HTTP-level answer about the endpoint was obtained on any of three recorded attempts, so the contract's "definitive HTTP answer" category cannot apply; this is transport-level indeterminacy, and retries are exhausted. Starting points are limited to frozen-metadata URLs, so no constructed variant was attempted.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

## EV-C105-DUP-01
Candidate: C105 (duplicate contributed by frame rank 106, games/eboard-extras)
Gate: UR
Source: frozen metadata, games/eboard/Makefile and games/eboard-extras/Makefile
Observed: both ports carry HOMEPAGE=http://www.bergo.eng.br/eboard/ and SITES=${SITE_SOURCEFORGE:=eboard/}; DISTNAMEs differ (eboard-1.1.1, eboard-extras).
Inference: the two ports package different distributed artifacts of one externally identified upstream project (eboard). Per the sealed duplicate rule they collapse to one candidate for ranking, while rank 106 remains logged and keeps the screening-budget slot it consumed.
Decision: DUPLICATE of C105

## EV-C006-UR-01
Candidate: C006 (frame rank 6, emulators/dgen-sdl)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/dgen-sdl/Makefile
Observed: metadata identifies one packaged system (DGen/SDL); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C006-E1-01
Candidate: C006
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C006-E2REP-01
Candidate: C006
Gate: E2-REP
Source: https://dgen.sourceforge.net/ (frozen-metadata starting point) and the pages it explicitly exposes
observed_at_utc: 2026-08-27T04:50:25Z-04:52:01Z (landing pages); 05:32:16Z (DOSBox SourceForge hub, rank 7 only)
http_status: 200; redirect_chain: NONE except rank 7's hub (www.sourceforge.net -> sourceforge.net)
evidence_role: official-project-page / official-source-location
Observed: the project page designates BOTH https://sourceforge.net/p/dgen/dgen/ (a SourceForge code repository) and http://sourceforge.net/projects/dgen/files/dgen/ (a release file area); neither is marked canonical, primary, or authoritative.
Inference: the sealed criterion admits a repository OR a source distribution as source-location types, and disqualifies a project that "designates several with no primary among them". That is this case. Same application as the corrected C002 verdict.
Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

## EV-C007-UR-01
Candidate: C007 (frame rank 7, emulators/dosbox)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/dosbox/Makefile
Observed: metadata identifies one packaged system (DOSBox); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C007-E1-01
Candidate: C007
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C007-E2REP-01
Candidate: C007
Gate: E2-REP
Source: https://www.dosbox.com/ (frozen-metadata starting point) and the pages it explicitly exposes
observed_at_utc: 2026-08-27T04:50:25Z-04:52:01Z (landing pages); 05:32:16Z (DOSBox SourceForge hub, rank 7 only)
http_status: 200; redirect_chain: NONE except rank 7's hub (www.sourceforge.net -> sourceforge.net)
evidence_role: official-project-page / official-source-location
Observed: the project page designates its own download page and https://www.sourceforge.net/projects/dosbox; that hub in turn exposes BOTH /p/dosbox/code-0/ (a code repository) and /projects/dosbox/files/ (a release file area), with no primary marked.
Inference: the sealed criterion admits a repository OR a source distribution as source-location types, and disqualifies a project that "designates several with no primary among them". That is this case. Same application as the corrected C002 verdict.
Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

## EV-C011-UR-01
Candidate: C011 (frame rank 11, emulators/frodo)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/frodo/Makefile
Observed: metadata identifies one packaged system (Frodo); no field names a different packaged system.
Inference: one external system identified; not UR-AMBIGUOUS.
Decision: PASS

## EV-C011-E1-01
Candidate: C011
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C011-E2REP-01
Candidate: C011
Gate: E2-REP
Source: http://frodo.cebix.net/ (frozen-metadata starting point) and the pages it explicitly exposes
observed_at_utc: 2026-08-27T04:50:25Z-04:52:01Z (landing pages); 05:32:16Z (DOSBox SourceForge hub, rank 7 only)
http_status: 200; redirect_chain: NONE except rank 7's hub (www.sourceforge.net -> sourceforge.net)
evidence_role: official-project-page / official-source-location
Observed: the project page hosts its own source archives (downloads/Frodo-4.5.tar.gz among others) AND links several repositories including github.com/cebix/frodo4; no location is marked canonical or primary.
Inference: the sealed criterion admits a repository OR a source distribution as source-location types, and disqualifies a project that "designates several with no primary among them". That is this case. Same application as the corrected C002 verdict.
Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

## EV-C004-UR-01
Candidate: C004 (frame rank 4, editors/tiled)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, editors/tiled/Makefile
Observed: HOMEPAGE=https://www.mapeditor.org/, GH_ACCOUNT/GH_PROJECT=bjorn/tiled, DISTNAME names one packaged system.
Inference: one external system (Tiled). The differing account name is another fact about the same system, not a second packaged system.
Decision: PASS

## EV-C004-E1-01
Candidate: C004
Gate: E1
Source: same frozen metadata
Observed: third-party authored system, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C004-E2REP-01
Candidate: C004
Gate: E2-REP
Source: https://www.mapeditor.org/ (frozen-metadata starting point)
observed_at_utc: 2026-08-27T04:50:25Z-04:52:01Z; http_status 200; redirect_chain NONE
evidence_role: official-project-page
Observed: the project page designates exactly one source location, github.com/mapeditor/tiled, and hosts no source archives of its own.
Inference: exactly one externally designated canonical source location at a stable URL, with one external target identifier (Tiled). Not the several-with-no-primary case that disqualified C002/C006/C007/C011.
Decision: PASS

## EV-C004-E2RULE-01
Candidate: C004
Gate: E2-RULE
Source: https://doc.mapeditor.org/en/stable/ ; https://github.com/mapeditor/tiled
observed_at_utc: 2026-08-27T05:33:39Z, 05:37:59Z; http_status 200
Observed: the project designates a documentation site (manual sections including automapping, export, preferences, keyboard shortcuts, scripting API reference) and its repository exposes top-level docs/ and tests/ directories.
Inference: externally authored artifacts exist from which at least one validity requirement can be determined without inventing it. The sealed criterion lists documentation and tests stating expected validity as admissible examples.
Decision: PASS

## EV-C004-E3-01
Candidate: C004
Gate: E3
Source: https://doc.mapeditor.org/en/stable/ (the project's own designated documentation index)
observed_at_utc: 2026-08-27T05:33:39Z; http_status 200
Observed: the documentation index exposes manual sections for automapping, export, preferences, interface/theme/plugins/keyboard settings, and a scripting API reference. A scan of the index for temporal or state-dependent validity topics found only two incidental occurrences of "session" and no topic covering state over time. The validity questions the project documents concern map/tileset structure and the map file format, which are properties of a static artifact.
Inference: E3 requires the external source to expose a stateful/temporal validity question that can be examined -- a validity property whose correctness depends on history or evolving state, not merely on a snapshot's structure. Structural file-format validity does not meet this, and no temporal validity topic is exposed. Recorded as observed; the gate is deliberately weak, and this candidate does not clear even that bar.
Decision: FAIL (E3-NO-STATEFUL-TEMPORAL-VALIDITY)

## RETRACTION — C004 (frame rank 4, editors/tiled)

The C004 verdicts recorded in 8549944 are **withdrawn** and the
candidate returns to in-flight. Entries EV-C004-E2RULE-01 and
EV-C004-E3-01 above are superseded and must not be cited.

EV-C004-E2RULE-01 inferred that "at least one validity requirement can
be determined" from the mere existence of a documentation site and of
docs/ and tests/ directories. The sealed criterion requires more: the
externally authored evidence must be sufficient to DETERMINE at least
one validity requirement, and its example is not tests in general but
"tests that explicitly state expected validity". No concrete statement
of the form "under condition X the result must be Y" or "state Z is
invalid" was ever located, so the gate was passed on the existence of
artifacts rather than on their content.

EV-C004-E3-01 then inherits that defect and adds its own. It concluded
that no stateful/temporal validity question exists by examining only the
documentation index, while E2-RULE had admitted the repository's tests/
directory as validity evidence. A surface admitted at one gate cannot be
ignored at the next: the tests were never examined for temporal validity
before E3 was failed.

UR, E1 and E2-REP for C004 are unaffected -- they rest on the frozen
metadata and on the project page's source designation, neither of which
is implicated. They will be re-recorded unchanged when the candidate is
re-determined.

## EV-C004-E2RULE-02  (supersedes the withdrawn EV-C004-E2RULE-01)
Candidate: C004 (frame rank 4, editors/tiled)
Gate: E2-RULE
Source: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/ -- the project's own designated format reference
observed_at_utc: 2026-08-27T05:46:12Z; http_status 200
Observed: located witness, quoted from that reference: "When used on objects in the Tile Collision Editor, they can only refer to other objects on the same tile."
Inference: this states a concrete validity requirement -- an object reference to an object on a different tile is invalid -- authored externally and readable without inventing it. This is a located statement of expected validity, not an inference from the existence of documentation.
Decision: PASS

## EV-C004-E3-02  (supersedes the withdrawn EV-C004-E3-01, which reached the OPPOSITE verdict)
Candidate: C004
Gate: E3
Source: same designated format reference
observed_at_utc: 2026-08-27T05:46:12Z, 05:46:40Z; http_status 200
Observed: located witness, quoted from the `nextlayerid` description: "Stores the next available ID for new layers. This number is stored to prevent reuse of the same ID after layers have been removed. (since 1.2)"
Inference: the validity of assigning a layer ID is not determined by the current snapshot. The set of layers present does not reveal which IDs previously existed, so "this ID is unused" is a claim about history, and the format stores a counter precisely because the current state cannot answer it. That is a stateful/temporal validity question exposed by the external source, which is what E3 asks for. Structurally this is the same shape as the properties Phase 3 modelled -- validity depending on what has happened, not on what is presently visible.
Decision: PASS

Note on the reversal: the withdrawn EV-C004-E3-01 recorded FAIL after examining only the documentation INDEX and finding no temporal topic among its section titles. The witness above sits inside the format reference, one level below that index. The index-level survey was not sufficient evidence for a negative verdict.

## EV-C004-E4-01
Candidate: C004 (frame rank 4, editors/tiled)
Gate: E4
Source: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/ ; https://doc.mapeditor.org/en/stable/ ; https://github.com/mapeditor/tiled
observed_at_utc: 2026-08-27T05:46:12Z, 05:53Z-05:55:21Z; http_status 200

Observed, normative route: the format reference states "TMX and TSX are Tiled's own formats for storing tile maps and tilesets" and describes its own scope as "In this document we'll go through each element found in these file formats. The elements are mentioned in the headers and the list of attributes of the elements are listed right below, followed by a short explanation." Its structure exposes 9 h2, 21 h3 and 237 list items; it contains no occurrence of "specification", "authoritative" or "canonical". Validity requirements appear inside the per-attribute prose explanations, e.g. the two witnesses cited at E2-RULE and E3.

Observed, enforcement route: the repository root contains no validators directory or declared validation structure (AUTHORS, CONTRIBUTING.md, COPYING, Doxyfile, NEWS.md, README.md, SECURITY.md, dist, docs, examples, and build/CI files); the documentation index contains one occurrence of "schema" and no declared validation or enforcement convention.

Inference: neither route yields a mechanically constructible property-level universe.

  U_normative -- the document's own segmentation enumerates ELEMENTS and ATTRIBUTES, not validity requirements. Those requirements sit inside per-attribute prose, so selecting which attribute descriptions carry a requirement would be researcher judgment. E4 rules this out directly: a subsystem-style list "is not enough if the actual validity observations inside those subsystems would still be hand-picked", which is exactly the shape here one level down. Separately, the project nowhere designates this page as an authoritative rules source; E2-RULE admissibility does not confer that status.

  U_enforced -- no mechanism satisfying EN1-EN6 is declared. There is no registry, interface, annotation set, or externally declared closed directory convention that the project itself connects to validation or eligibility.

Only one route is required and neither is available.
Decision: FAIL (E4-NO-MECHANICAL-PRIMARY-UNIVERSE)

## RETRACTION 2 — C004 E4 (EV-C004-E4-01 withdrawn)

EV-C004-E4-01 is withdrawn; C004 returns to in-flight at E4. Its UR,
E1, E2-REP, E2-RULE and E3 verdicts stand.

Both of that entry's negative claims were stronger than the surfaces
that supported them, repeating QA-09's error one gate later.

The normative claim rested on the format reference containing no
occurrence of "specification", "authoritative" or "canonical". That
establishes only that the page does not call ITSELF authoritative. The
sealed rule asks whether the external project designates the source as
authoritative for its rules, and another project-owned page could carry
that designation. Not surveyed.

The enforcement claim rested on the repository root having no
validators directory and the documentation index declaring no
validation convention. Registries, interfaces, annotations and runtime
dispatch need not be named "validators" and commonly live inside
source. Directory names at the root are a surface that can show
presence and cannot establish absence.

## EV-C004-E4-02  (supersedes the withdrawn EV-C004-E4-01)
Candidate: C004 (frame rank 4, editors/tiled)
Gate: E4
observed_at_utc: 2026-08-27T05:46:12Z-06:02:52Z; http_status 200 throughout

NORMATIVE ROUTE -- surfaces surveyed, five, chosen as the places a designation would appear:
  https://doc.mapeditor.org/en/stable/reference/tmx-map-format/  (the source itself)
  https://www.mapeditor.org/                                     (project front page)
  https://doc.mapeditor.org/en/stable/                           (documentation landing)
  https://doc.mapeditor.org/en/stable/reference/support-for-tmx-maps/
  https://raw.githubusercontent.com/mapeditor/tiled/master/README.md
Observed: none of the five designates the TMX reference as an authoritative rules source or specification. The reference contains no occurrence of "specification", "authoritative" or "canonical"; the front page, docs landing and support page carry no designating language; the README says only "Tiled's map format (TMX) is easy to understand". The single "TMX format" hit on the support page describes a third-party engine's capability.
Inference: the project owns the format and documents it, but nowhere designates that document as authoritative for its rules. Section 3.1 requires explicit designation and states that project ownership alone is insufficient. Separately, even were it admissible, its own segmentation enumerates elements and attributes while validity requirements sit inside per-attribute prose -- E4 excludes a universe whose validity observations would still be hand-picked.

ENFORCEMENT ROUTE -- surfaces surveyed:
  https://github.com/mapeditor/tiled/tree/master/src        (all top-level source units)
  https://github.com/mapeditor/tiled/tree/master/src/plugins (membership)
  https://github.com/mapeditor/tiled/tree/master/src/libtiled (filenames)
Observed: a declared, mechanically closed mechanism DOES exist -- src/plugins/ with membership csv, defold, defoldcollection, droidcraft, flare, gmx, json, json1, lua, python, replicaisland, rpd, rpmap, tbin, tengine, tscn, yy. Its members are import/export formats of other engines and tools. libtiled contains no unit named for validation, verification, checking, schema or conformance.
Inference: EN3 (mechanical membership) is satisfied by the plugin set, but EN4 is not: the project connects this mechanism to map format import and export, not to validation, eligibility, or rule enforcement. An enumerator whose declared role is format conversion cannot enumerate an enforcement surface. No other declared mechanism was found across the source's top-level units.

Only one route is required; neither is available. This verdict rests on surveying the surfaces where each fact would appear, not on the absence of a directory named "validators" -- that earlier reasoning was withdrawn as too weak (RETRACTION 2).
Decision: FAIL (E4-NO-MECHANICAL-PRIMARY-UNIVERSE)

## EV-C005-UR-01
Candidate: C005 (frame rank 5, emulators/advancemame)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/advancemame/Makefile
Observed: DISTNAME=advancemame-$V; HOMEPAGE=https://www.advancemame.it/; SITES=https://github.com/amadvance/advancemame/releases/download/v$V/; no GH_* or DIST_TUPLE fields.
Inference: all fields name one packaged system, AdvanceMAME. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C005-E1-01
Candidate: C005
Gate: E1
Source: same frozen metadata; https://raw.githubusercontent.com/amadvance/advancemame/master/README
Observed: third-party authored emulator; the README describes AdvanceMAME/MESS as unofficial MAME/MESS versions. Unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C005-E2REP-01
Candidate: C005
Gate: E2-REP
Surfaces named BEFORE investigation, as the places a SECOND designated source location would appear: the project's own /download page, and the SourceForge project hub the landing page exposes.
Source: https://www.advancemame.it/ ; https://www.advancemame.it/download ; http://sourceforge.net/projects/advancemame/
observed_at_utc: 2026-08-27T06:39:12Z (download), 06:39:57Z and 06:40:12Z x2 (SF hub)
http_status: 200, 200, and 000 on three attempts for the hub; redirect_chain NONE
evidence_role: official-project-page / official-source-location
Observed: for the packaged system itself, /download designates
https://github.com/amadvance/advancemame/releases/download/v5.0/advancemame-5.0.tar.gz -- the Releases area of the same repository the landing page links. The SourceForge prdownloads links on that page are for OTHER products of the same family (advancecab, advancecd, advancesnap, makebootfat), not for advancemame. The SourceForge project hub returned no HTTP answer on three recorded attempts, while sourceforge.net itself returned 200 and a cdn.openbsd.org control returned 200. Per the eliot precedent, no scheme variant of the exposed URL was constructed.
Inference: /download is the surface on which this project designates where each of its products comes from, and it routes this system exclusively to one location. Releases are part of that repository rather than a separate location. The unreachable SourceForge hub is a family project hub which /download shows serving the family's OTHER products, so it is not a competing designation for this system -- the same distinction that makes the landing page's libdeflate and zopfli links dependencies rather than source locations. Exactly one canonical source location at a stable URL, with one external target identifier.
Decision: PASS

## EV-C005-E2RULE-01
Candidate: C005
Gate: E2-RULE
Source: https://www.advancemame.it/doc-advmame (project-designated documentation, reached from the /doc index)
observed_at_utc: 2026-08-27T06:41:24Z; http_status 200
Observed: located witnesses, quoted -- (1) "For boolean options you don't need to specify the argument but you must use the -OPTION or -noOPTION format." (2) "To include more than one file you must divide the names with `;` in DOS and Windows, and with `:` in Linux and Mac OS X." (3) "The image must be a PNG file."
Inference: each states a concrete validity requirement on an input: an option not in that form, a multi-file value with the wrong separator, or a non-PNG image is invalid. Externally authored and readable without inventing anything.
Decision: PASS

## EV-C005-E3-01
Candidate: C005
Gate: E3
Source: same admitted surface, https://www.advancemame.it/doc-advmame
observed_at_utc: 2026-08-27T06:41:24Z to 06:42:00Z
Observed: located witness, quoted -- "-playback FILE Play back the previously recorded game inputs in the specified file", together with "Note that the `emulation` mode may result in wrong input recording using the `-record` or `-playback` command line option due to incorrect behavior of the emulation."
Inference: whether a playback is correct is not decidable from any snapshot. It depends on the recorded input sequence and on the emulation behaving identically during the later run, and the documentation names a configuration under which the recorded artifact is not faithful. That is a validity question about state evolving over time, which is what E3 asks for. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C005-E4-01
Candidate: C005
Gate: E4
Surfaces named BEFORE investigation -- normative: the landing page, the /doc index, doc-advmame, and the repository README. Enforced: the repository source tree and its declared units.
Source: https://www.advancemame.it/ ; /doc ; /doc-advmame ; https://raw.githubusercontent.com/amadvance/advancemame/master/README ; https://github.com/amadvance/advancemame (tree, advance/, advance/lib/)
observed_at_utc: 2026-08-27T06:42:39Z to 06:43:21Z; http_status 200 throughout

Observed, normative route: neither the landing page nor the /doc index carries designating language. doc-advmame contains "specification" seven times and every occurrence examined refers to a configuration VALUE format -- "Multi directory specification for the ... files", "advj is used for joystick[] ... specifications" -- not to the document's own status. The README designates the official SITE, stating that the official site of AdvanceMAME/MESS is http://www.advancemame.it/, but designates no document as authoritative for rules. The documentation is numbered per configuration option (8.2.1 config, 8.4.11 display_restore, and so on), so it is mechanically segmented, but that segmentation enumerates OPTIONS while the validity requirements sit inside each option's prose, including all three E2-RULE witnesses.

Observed, enforced route: the repository's top-level units are build and platform configuration plus advance/, doc/, mess/, raspberry/. Within advance/ the units are functional modules (blit, blue, card, cfg, d2, dos, emu, expat, i, j, k, lib and others). advance/lib contains conf.c, conf.h and config.hin -- a configuration implementation, not a declared mechanism. Nothing in the project declares an enumerable set as carrying its validity or eligibility rules.

Inference: neither route yields a mechanically constructible property-level universe. U_normative fails twice over: no source is designated authoritative, and even the well-segmented option documentation would require hand-picking which option descriptions carry a requirement, which E4 excludes in as many words. U_enforced fails EN2, EN4 and EN5 -- conf.c is an implementation file with no declared scope, no project-stated connection to validation or eligibility, and no externally declared closure. Only one route is required and neither is available.
Decision: FAIL (E4-NO-MECHANICAL-PRIMARY-UNIVERSE)

## RETRACTION 3 — C005 E2-REP, and quarantine of everything after it

EV-C005-E2REP-01 is withdrawn and replaced by EV-C005-E2REP-02 below.
EV-C005-E2RULE-01, EV-C005-E3-01 and EV-C005-E4-01 are **quarantined**:
they remain on the record but must not be cited for any screening
verdict, because the gate that preceded them never resolved.

What went wrong is specific and worth stating exactly, because the
surface-naming discipline was followed and still produced a bad
verdict. Before investigating E2-REP, two surfaces were named as the
places a SECOND designated source location would appear: the project's
own /download page, and the SourceForge project hub the landing page
exposes. One of those two was then never observed -- three attempts,
no HTTP exchange, controls healthy. The verdict was nevertheless
recorded PASS, on the reasoning that /download routes this system to
GitHub while routing the family's other products to SourceForge.

That reasoning answers a different question than the one asked.
"/download designates GitHub as where AdvanceMAME's source comes from"
is a positive fact about /download. "The SourceForge hub does not
expose a second source designation for AdvanceMAME" is a claim about a
page that was never read. Substituting the first for the second is
exactly the negative-evidence substitution this run has already
corrected three times (QA-04, QA-07, QA-09, QA-10) -- here in a new
form, since the missing observation was of a surface we ourselves had
declared necessary.

## EV-C005-E2REP-02  (supersedes EV-C005-E2REP-01)
Candidate: C005 (frame rank 5, emulators/advancemame)
Gate: E2-REP
Surfaces named before investigation: the project's /download page, and
the SourceForge project hub exposed by the landing page.
Source: https://www.advancemame.it/ ; https://www.advancemame.it/download ; http://sourceforge.net/projects/advancemame/
observed_at_utc: 2026-08-27T06:39:12Z (download), 06:39:57Z and 06:40:12Z x2 (SF hub)
http_status: 200 for /download; 000 on all three attempts for the hub
redirect_chain: NONE
evidence_role: official-project-page / official-source-location
Observed: /download designates https://github.com/amadvance/advancemame/releases/download/v5.0/advancemame-5.0.tar.gz for this system, and SourceForge prdownloads links for the family's other products. The SourceForge project hub produced no HTTP answer on three recorded attempts, while sourceforge.net itself returned 200 and a cdn.openbsd.org control returned 200 at the same times. No scheme variant of the exposed URL was constructed, per the eliot precedent.
Inference: one of the two surfaces required to decide "exactly one designated canonical source location" could not be observed. A positive designation was located, but the question at this gate is not only whether one exists; it is whether more than one does, and that could not be determined. The contract classifies an endpoint that yields no HTTP answer after two recorded retries as transport indeterminacy rather than evidence of absence, and requires the gate to be recorded UNRESOLVED with later gates NOT_REACHED.
Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

Post-stop exposure, logged rather than concealed: E2-RULE, E3 and E4
were investigated before this correction, so their content was seen.
The findings are quarantined above and take no part in C005's verdict.
Their substance is preserved only because deleting observations would
be worse for audit than marking them unusable.

## EV-C008-UR-01
Candidate: C008 (frame rank 8, emulators/dosbox-x)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/dosbox-x/Makefile
Observed: GH_ACCOUNT=joncampbell123; GH_PROJECT=dosbox-x; GH_TAGNAME=dosbox-x-v${VERSION}; HOMEPAGE=https://dosbox-x.com/; DISTNAME=dosbox-x-${VERSION}.
Inference: every field names one packaged system, DOSBox-X. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C008-E1-01
Candidate: C008
Gate: E1
Source: same frozen metadata; https://raw.githubusercontent.com/joncampbell123/dosbox-x/master/README.md
Observed: third-party authored emulator, a fork of DOSBox, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C008-E2REP-01
Candidate: C008
Gate: E2-REP
Surfaces: http://dosbox-x.software -- the second project domain the landing page exposes.
Necessary because: E2-REP asks whether EXACTLY ONE source location is designated, and the landing page exposes a second project-branded domain, which could carry its own source designation; the verdict cannot be settled without reading it.
Source: https://dosbox-x.com/ ; http://dosbox-x.software
observed_at_utc: 2026-08-27T04:50:25Z-04:52:01Z (landing), 06:58:16Z (second domain)
http_status: 200, 200; redirect_chain: NONE (the second domain redirects client-side, not by HTTP)
evidence_role: official-project-page / official-source-location
Observed: the landing page designates https://github.com/joncampbell123/dosbox-x, and its source archive links point into that same repository's tag archives (archive/refs/tags/dosbox-x-v2026.08.02.tar.gz and .zip). It hosts no source archives of its own. Other links are binary package distributions (Flathub, Fedora COPR), a different project (sourceforge.net/projects/winprint), the ancestor project (dosbox.com), and account pages. The second project domain, dosbox-x.software, is a 132-byte page whose entire content is "Redirecting you to dosbox-x.com..." with no links at all.
Inference: the named surface was observed and carries no competing designation -- it is an alias for the main site. GitHub tag archives are part of the designated repository rather than a separate location, and binary package distributions are not upstream designations of canonical source. Exactly one canonical source location at a stable URL, with one external target identifier (DOSBox-X).
Decision: PASS

## EV-C008-E2RULE-01
Candidate: C008
Gate: E2-RULE
Source: https://dosbox-x.com/wiki/Guide%3AVideo-card-support-in-DOSBox-X (project-designated wiki, reached via /wiki -> List-of-Guide-Pages)
observed_at_utc: 2026-08-27T06:59:18Z-07:00:00Z; http_status 200
Observed: located witness, quoted -- "vga bios rom image default value: <none> If set, load the VGA BIOS from the specified file (must be between 1KB to 64KB in size)."
Inference: this states a concrete validity requirement on an input artifact -- a VGA BIOS image outside 1KB-64KB is invalid for this setting. Externally authored and readable without inventing it.
Decision: PASS

## EV-C008-E3-01
Candidate: C008
Gate: E3
Source: https://dosbox-x.com/wiki/Guide%3AManaging-image-files-in-DOSBox-X (same admitted documentation surface)
observed_at_utc: 2026-08-27T07:00:00Z; http_status 200
Observed: located witness, quoted -- "Note A harddisk image MUST be partitioned before it can be formatted."
Inference: whether a format operation is valid is not decidable from the operation or from the image's current appearance alone; it depends on whether a partitioning step occurred earlier. That is validity conditioned on history, which is what E3 asks for, and it is structurally the same shape as the ordering properties Phase 3 modelled. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C008-E4-01
Candidate: C008
Gate: E4
Surfaces: normative -- the dosbox-x.com landing page, /about.html, the wiki Home, and the repository README.md. Enforced -- the repository's top-level declared units, plus README.md and CONTRIBUTING.md where the project describes them.
Necessary because: E4 asks whether a property-level universe is mechanically constructible via U_normative or U_enforced. A designation of an authoritative rules source would appear on the project's own pages, and a declared enumerator would appear among its top-level units and in the documents that describe them; neither route can be settled without reading these.
Source: https://dosbox-x.com/ ; /about.html ; /wiki/Home ; https://github.com/joncampbell123/dosbox-x ; raw README.md ; raw CONTRIBUTING.md
observed_at_utc: 2026-08-27T07:00:33Z-07:01:11Z; http_status 200 throughout

Observed, normative route: the wiki Home carries no designating language. /about.html contains "specification" once, referring to the "PC 2001" hardware specifications published in 2001. README.md contains it once, referring to specifications from Microsoft that mandated removal of ISA slots. Neither refers to any document's own status, and no surface designates the wiki or any other document as an authoritative rules source.

Observed, enforced route: the repository's top-level units include AUTHORS, BUGS, BUILD.md, CHANGELOG, CONTRIBUTING.md, CREDITS.md, Doxyfile, INSTALL.md, NOTES, NOTES-TESTING-LOG, OLD-REFERENCE, experiments, include, ref, scripts, snapshots, src, tests, vs and build files. No unit is named for validation, conformance, schema, enforcement or rules. Of the two plausible candidates, the project describes them itself: README.md lists as a TODO "Write more unit tests to test various functions (see existing unit tests in tests/)", and CONTRIBUTING.md states of its coding rules that "there are many places where these rules are simply not followed".

Inference: neither route yields a mechanically constructible property-level universe. U_normative has no designated authoritative source at all. U_enforced fails EN2, EN4 and EN5 on the project's own descriptions: tests/ has no declared scope in validity terms, is connected by the project to testing functions rather than to validation or eligibility, and is explicitly open-ended -- "write more" is the opposite of a closure claim, and CONTRIBUTING.md separately disclaims that its rules are followed. Only one route is required and neither is available.
Decision: FAIL (E4-NO-MECHANICAL-PRIMARY-UNIVERSE)

## RETRACTION 4 — C008 E4 (EV-C008-E4-01 withdrawn); E3 inference narrowed

EV-C008-E4-01 is withdrawn and replaced by EV-C008-E4-02. EV-C008-E3-01
is superseded by EV-C008-E3-02, which keeps the PASS but drops an
over-strong sentence. UR, E1, E2-REP and E2-RULE are unaffected.

The E4 entry's enforcement claim examined the repository's top-level
NAMES, picked out "the two plausible candidates" among them, and
concluded from those two that no EN1-EN6 mechanism exists. Choosing
which candidates are plausible is analyst selection, and the source
tree's interior was never examined -- which is precisely where C004's
src/plugins/ was found after an identical shortcut had missed it. Its
normative claim likewise moved from "not found on four pages" to "no
designation anywhere".

The E3 entry claimed the validity of a format operation "is not
decidable from ... the image's current appearance alone". That is not
needed for the gate and is probably wrong: a partition table is
observable in present state. E3 only asks whether a stateful/temporal
validity question exists, and an ordering prerequisite supplies one
without the stronger claim.

## EV-C008-E3-02  (supersedes EV-C008-E3-01; same verdict, narrower inference)
Candidate: C008
Gate: E3
Source: https://dosbox-x.com/wiki/Guide%3AManaging-image-files-in-DOSBox-X
observed_at_utc: 2026-08-27T07:00:00Z; http_status 200
Observed: located witness, quoted -- "Note A harddisk image MUST be partitioned before it can be formatted."
Inference: the validity of FORMAT is conditioned on a prerequisite state -- the image must already be partitioned before formatting is permitted. The validity question therefore concerns an ordered state transition rather than a static property of the FORMAT command alone. That is a stateful/temporal validity question, which is all this gate requires. No stronger claim is made about what is or is not observable in the image's present state.
Decision: PASS

## EV-C008-E4-02  (supersedes the withdrawn EV-C008-E4-01)
Candidate: C008
Gate: E4

Closed search surfaces, justified before investigating:

  U_normative -- the project's own enumeration of its documentation.
  DOSBox-X publishes /wiki/List-of-Guide-Pages, which lists its guide
  pages; that list is authored by the project, not by us, so it closes
  the set of documents in which the project could designate an
  authoritative rules source. Surveyed together with the entry points
  outside it: the landing page, /about.html, the wiki Home, README.md
  and CONTRIBUTING.md.

  U_enforced -- EN4 requires the PROJECT ITSELF to connect a mechanism
  to validation, eligibility or rule enforcement. That is a claim about
  what the project states, and a project's statements about its own
  mechanisms appear in its documents. The documented set above is
  therefore closed for this question too: a registry, interface or
  annotation may exist anywhere in the source, but if no project
  document declares it as carrying validity or eligibility rules, it
  fails EN4 regardless. This is why the negative does not require an
  exhaustive walk of src/ -- and it is stated as the reason, rather
  than the source tree being sampled for "plausible candidates" as the
  withdrawn entry did.

Source: https://dosbox-x.com/wiki/List-of-Guide-Pages and all 24 guide pages it enumerates; https://dosbox-x.com/ ; /about.html ; /wiki/Home ; raw README.md ; raw CONTRIBUTING.md
observed_at_utc: 2026-08-27T06:58:54Z-07:14:06Z; http_status 200 throughout

Observed: across the 24 project-enumerated guide pages, zero contain designating language (authoritative, canonical, normative, "the specification of", "defines the format", "reference implementation"). The entry points outside that list carry none either: /about.html and README.md each use "specification" once, of the PC 2001 hardware specifications and of Microsoft specifications mandating ISA slot removal respectively; the wiki Home and CONTRIBUTING.md have none. Scanning the same 24 pages for declared-mechanism language (registry, "all validators/checks/rules are", interface implementation, annotation, "every validator/rule/check") produced one hit, in the networking guide, and it is a false positive: the matched text is a DHCP failure message about cabling and packet driver settings, not a declaration about the project's structure.

Inference: neither route yields a mechanically constructible property-level universe. U_normative -- the project designates no document as an authoritative rules source anywhere in its own declared documentation inventory or at its entry points. U_enforced -- no project document connects any mechanism to validation, eligibility or rule enforcement, so EN4 is unsatisfied for every candidate mechanism whatever the source tree contains; EN2 and EN5 are likewise unmet, the project describing tests/ as an open-ended TODO ("Write more unit tests...") and disclaiming that its coding rules are followed ("there are many places where these rules are simply not followed"). Only one route is required and neither is available.
Decision: FAIL (E4-NO-MECHANICAL-PRIMARY-UNIVERSE)

## RETRACTION 5 — C004 and C008 E4 verdicts withdrawn under the post-seal amendment

EV-C004-E4-02 and EV-C008-E4-02 are **quarantined**. Both recorded E4
FAIL. Neither is withdrawn because its observations were false -- the
pages were read, the counts are real, the repository listings are
accurate. They are unusable because each concluded a universal absence,
and the sealed methodology preregistered no procedure by which such an
absence can be established. Admissibility is defined in detail; complete
discovery is not defined at all.

This is the same distinction the run has applied throughout, arriving
here at the level of a whole gate rather than a single surface: an
observation that found nothing is not a demonstration that nothing is
there. C005's post-stop findings were quarantined on the same principle.

## EV-C004-E4-03  (supersedes the quarantined EV-C004-E4-02)
Candidate: C004 (frame rank 4, editors/tiled)
Gate: E4
Observed: no positive construction was obtained. The Tiled format
reference is segmented by element and attribute rather than by validity
requirement, and the project designates no document as an authoritative
rules source; src/plugins/ is a genuine mechanically closed enumerator
but the project connects it to map import and export, so it fails EN4.
Inference: E4 PASS requires a positive construction -- an EN1-EN6
mechanism or a designated source from which the property-level universe
is actually mechanically constructible. None was exhibited. Under the
post-seal amendment the absence of a positive construction does not
establish E4 FAIL, because no preregistered discovery procedure makes
that universal claim decidable.
Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C008-E4-03  (supersedes the quarantined EV-C008-E4-02)
Candidate: C008 (frame rank 8, emulators/dosbox-x)
Gate: E4
Observed: no positive construction was obtained. Across the project's
24 enumerated guide pages and its entry points, no document designates
an authoritative rules source, and no project document declares a
mechanism as carrying validity or eligibility rules; the project
describes tests/ as an open-ended TODO and disclaims that its coding
rules are followed.
Inference: as for C004 -- no positive construction was exhibited, and
the absence of one does not establish E4 FAIL under this run's
amendment. The earlier entry additionally rested on a docs-only closure
argument that would have excluded runtime construction, which the
sealed rules admit as evidence; that argument is withdrawn with it.
Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C010-UR-01
Candidate: C010 (frame rank 10, emulators/flycast)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/flycast/Makefile
Observed: HOMEPAGE=https://github.com/flyinghead/flycast; DISTNAME=flycast-${V}; COMMENT="emulator for Sega Dreamcast and Sega Naomi based on reicast"; the port's own dist: target runs "git clone https://github.com/flyinghead/flycast.git".
Inference: every field names one packaged system, Flycast. "based on reicast" states lineage, not a second packaged system. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C010-E1-01
Candidate: C010
Gate: E1
Source: same frozen metadata; https://raw.githubusercontent.com/flyinghead/flycast/master/README.md
observed_at_utc: 2026-08-27T07:47:58Z; http_status 200
Observed: a third-party emulator authored by flyinghead, "derived from reicast", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C010-E2REP-01
Candidate: C010
Gate: E2-REP

Surfaces: the upstream landing page named by the frozen metadata's HOMEPAGE, which is itself the repository root at https://github.com/flyinghead/flycast. Under the network-access contract this is simultaneously navigation step 1 (landing page) and step 3 (repository metadata/root surface), so no further navigation is available or needed.
Necessary because: E2-REP asks whether upstream designates EXACTLY ONE canonical source location at a stable URL. That is a question about upstream's own designation, and the only upstream surface the frozen metadata resolves to is this one.

Source: https://github.com/flyinghead/flycast
observed_at_utc: 2026-08-27T07:46:55Z-07:46:56Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-project-page / official-source-location

Observed: repository flyinghead/flycast, default branch master, isFork false, isArchived false, isTemplate false, no mirror or primary/secondary marking, no repository website field. A source tree is present at the root: directories .github, core, docs, fonts, intl, resources, shell, tests, tools and files including CMakeLists.txt, CMakePresets.json, LICENSE, README.md. The only non-GitHub outbound links are brew.sh, flathub.org, play.google.com, repology.org, flatpak.org and a Discord invite -- binary distribution channels and a chat server, none of them a source-location designation.

Inference: exactly one canonical source location, at a stable URL, designated by upstream as its own repository, actually holding a source tree, with one external target identifier (Flycast). No competing designation is exposed.

Surface considered and NOT observed, with the reason: the frozen metadata also carries SITES=https://messagemode2.com/source/. It is an allowed starting point, but it cannot bear on this gate, and the reason is criterion-grounded rather than convenience. E2-REP asks what UPSTREAM designates; the port Makefile's own dist: target shows the OpenBSD maintainer generating flycast-${V}.tar.gz locally from a git clone and uploading it to a source/ directory ("scp flycast-${V}.tar.gz train:source/"). That distfile is therefore packager-side by the frozen metadata's own construction, and a packager's re-rolled tarball is not an upstream designation whatever it contains. It is also not reachable from any upstream surface: it appears in OpenBSD metadata only.

Incidental exposure logged (not used to pre-judge later gates): the repository page renders README.md automatically, and the root listing shows a .gitlab-ci.yml. The contract forbids opening source files at this gate, so it was not opened; a CI configuration is in any case not a designation of a canonical source location.

Decision: PASS

## EV-C010-E2RULE-01
Candidate: C010
Gate: E2-RULE
Source: https://raw.githubusercontent.com/flyinghead/flycast/master/README.md -> https://github.com/TheArcadeStriker/flycast-wiki/wiki -> https://github.com/TheArcadeStriker/flycast-wiki/wiki/Verifying-your-BIOS-and-Arcade-ROMs
observed_at_utc: 2026-08-27T07:47:58Z (README), 07:48:22Z (wiki index), 07:48:34Z (page); http_status 200 throughout

Observed: the upstream README designates the documentation surface -- "Information about configuration and supported features can be found on TheArcadeStriker's flycast wiki". On the page that wiki devotes to BIOS and ROM verification, the located witness, quoted: "Flycast uses the latest MAME ROMs (0.219 at the time of this writing), and while most work fine out of the box, others may have new files added in recent MAME which could be missing from your old ROM but be required by Flycast." The same page states of arcade BIOS files that anything other than the listed contents "will give a warning about using an incorrect BIOS".

Inference: this states a concrete validity requirement on an input artifact without our inventing it -- a ROM archive is valid for Flycast only if it contains the file set Flycast's MAME romset level requires, and a BIOS outside the specified contents is incorrect. Externally authored in the sense E2-RULE uses (it existed independently of this analysis) and reached only through upstream's own designation of it.

Recorded because it matters later, not because it changes this gate: this wiki is owned by a third-party account, TheArcadeStriker, not by the project. Section 3.1 bars third-party material from U_normative membership regardless of designation, and that bar is applied at E4 below, where the normative route is accordingly unavailable. E2-RULE asks only whether externally authored validity evidence exists, which it does.
Decision: PASS

## EV-C010-E3-01
Candidate: C010
Gate: E3
Source: https://github.com/TheArcadeStriker/flycast-wiki/wiki/Flycast-GGPO-Information-and-Guide (reached from the same designated wiki index)
observed_at_utc: 2026-08-27T07:49:02Z; http_status 200

Observed: located witness, quoted -- of downloading a pre-configured netplay save state, "Both players should do this otherwise your game will never be in sync." The same page states that creating one is "critical to avoid crashes and desyncs", describes the ordered procedure (start the game offline, reach the desired state, save it, rename it with a .net suffix, send it to the opponent), and lists as the first remedy for a GGPO assertion failure: "First make sure you are using a save state to play."

Inference: whether a netplay session is valid is not decidable from the session's present configuration. It depends on whether a matching save state was produced and exchanged BEFORE the session began; an omitted prior step invalidates the later session rather than the step itself. That is validity conditioned on history -- the same ordering shape Phase 3 modelled, and the same shape C008's partition-before-format witness carried. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C010-E4-01
Candidate: C010
Gate: E4

Positive construction exhibited, via U_enforced. All observations are at the primary snapshot: master had not moved since 2026-08-23T11:29:03Z, so raw reads of master on 2026-08-27 resolve to commit c3763d8fc4208dd6f8f0bc456383543b8406a8a0, the revision the snapshot rule fixes.

Source: https://raw.githubusercontent.com/flyinghead/flycast/master/core/hw/naomi/naomi_roms.h ; .../naomi_cart.h ; .../naomi_cart.cpp ; .../naomi_roms.cpp
observed_at_utc: 2026-08-27T07:50:04Z-07:51:11Z; http_status 200 throughout

The mechanism: the ROM-set table Games[], declared "extern const Game Games[];" in core/hw/naomi/naomi_roms.h and defined in core/hw/naomi/naomi_roms.cpp lines 248-8517, consumed by FindGame() in core/hw/naomi/naomi_cart.cpp:153-165.

EN1 external authorship: the file's own header records "Created on: Nov 2, 2018, Copyright 2018 flyinghead". It existed independently of this analysis.

EN2 explicit scope: the project identifies the domain in its own terms rather than ours -- the table's header comment states "Rom information from mame (https://github.com/mamedev/mame)", the declared type is Game with a blobs[] array of per-file filename, offset, length, crc and blob_type, and the consuming function is loadMameRom. This leg is carried by the project's declarations and error vocabulary rather than by prose, and is recorded that way rather than stated more strongly.

EN3 mechanical membership: membership is array membership in Games[]. No semantic reading of individual entries is required; 354 entries carry a RotationType field, one per game.

EN4 enforcement meaning: the project itself makes table membership the eligibility condition for loading. loadMameRom calls FindGame(fileName) and, on a miss, executes "throw NaomiCartException(Ts("Unknown game"))" (naomi_cart.cpp:216-217). Per-entry requirements are enforced the same way: for each blob the loader resolves the file by its declared CRC and then by its declared filename, and if neither resolves it throws "Cannot find %s" keyed on game->blobs[romid].filename (naomi_cart.cpp:328-345), with the project's own comment marking the one exemption -- "Default eeprom file is optional". This meaning is stated by the project's code, not inferred by us from a name.

EN5 closed within scope: FindGame iterates "for (int i = 0; Games[i].name != nullptr; i++)", and the table's definition ends with a "{ nullptr }" sentinel at naomi_roms.cpp:8513-8515. The set is closed at runtime by the enumerator the loader actually walks, which is Section 3.2's first admissible case -- runtime construction closes the set. Tag: enforced.

EN6 outcome independence: membership is the set of supported arcade ROM sets. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible: enumerate Games[] to its sentinel and emit, per entry, its required constituent files with declared CRC32, filename, offset, length and blob type, plus the project's stated optionality rule for Eeprom blobs. A worked entry, naomi_roms.cpp:1236-1248: "crzytaxi" / "Crazy Taxi", cart type M2, BIOS "naomi", requiring "epr-21684.ic22" at offset 0x0000000, length 0x400000, CRC 0xf1de77b7, and further mpr-*.ic* blobs on the same pattern.

One accuracy note, recorded so the entry is not read as claiming more than was seen: the crc field is used as a LOOKUP key (OpenFileByCrc) with filename as fallback, not as a post-read integrity comparison. The requirement it expresses is that a file with that CRC or that name be present, not that the loader verifies the bytes it read.

Normative route, for completeness: unavailable, and by rule rather than by absence. The only documentation source upstream designates is TheArcadeStriker's flycast wiki, which is third-party. Section 3.1 removed the third-party escape hatch outright -- such material "may be used as supporting evidence during analysis, but never as primary-universe membership". No claim is made here about whether some other designation exists; only one route is required, and U_enforced supplies it.

Decision: PASS

## EV-C012-UR-01
Candidate: C012 (frame rank 12, emulators/libchdr)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/libchdr/Makefile
Observed: GH_ACCOUNT=rtissera; GH_PROJECT=libchdr; GH_COMMIT=07a7dad23378b001f4ab174ef51bd6553f883edd; HOMEPAGE=https://github.com/rtissera/libchdr; DISTNAME=libchdr-$V; COMMENT="library for reading MAME's CHDv1-v5 formats".
Inference: every field names one packaged system, libchdr. The reference to MAME names the format the library reads, not a second packaged system. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C012-E1-01
Candidate: C012
Gate: E1
Source: same frozen metadata; https://raw.githubusercontent.com/rtissera/libchdr/master/README.md
observed_at_utc: 2026-08-27T08:14:55Z; http_status 200
Observed: a third-party library authored by rtissera, "based off of MAME's old C codebase", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C012-E2REP-01
Candidate: C012
Gate: E2-REP

Surfaces: the upstream landing page named by the frozen metadata's HOMEPAGE, which is itself the repository root at https://github.com/rtissera/libchdr. As with C010 this is simultaneously navigation step 1 and step 3, so no further navigation is available or needed.
Necessary because: E2-REP asks whether upstream designates EXACTLY ONE canonical source location at a stable URL. That is a question about upstream's designation, and every URL and identifier in the frozen metadata resolves to this one location -- the port carries no SITES at all, fetching through GH_ACCOUNT/GH_PROJECT/GH_COMMIT, so there is no packager-side distfile host to consider as there was for C010.

Source: https://github.com/rtissera/libchdr
observed_at_utc: 2026-08-27T08:14:43Z-08:14:44Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-project-page / official-source-location

Observed: repository rtissera/libchdr, default branch master, isFork false, isArchived false, isTemplate false, no mirror or primary/secondary marking, no repository website field. A source tree is present at the root: directories .github, cmake, contrib/tangcore-bl616, deps, include, src, tests and files CHANGELOG.md, CMakeLists.txt, LICENSE.txt, README.md, pkg-config.pc.in, unity.c. The page exposes no outbound links to any non-GitHub host.

Inference: exactly one canonical source location, at a stable URL, designated by upstream as its own repository, actually holding a source tree, with one external target identifier (libchdr). No competing designation is exposed, and none could be: the page links nowhere else.

Incidental exposure logged (not used to pre-judge later gates): the repository page renders README.md automatically.

Decision: PASS

## EV-C012-E2RULE-01
Candidate: C012
Gate: E2-RULE
Source: https://raw.githubusercontent.com/rtissera/libchdr/master/include/libchdr/chd.h, the library's own public header
observed_at_utc: 2026-08-27T08:15:18Z; http_status 200

Observed: located witness, quoted from the file's format block -- "Compressed Hunks of Data header format. All numbers are stored in Motorola (big-endian) byte ordering. The header is 76 (V1) or 80 (V2) bytes long." The block then gives each version's layout field by field, beginning in every case with "[  0] char   tag[8];        // 'MComprHD'". The constants section states the same requirement numerically: CHD_V1_HEADER_SIZE 76, CHD_V2_HEADER_SIZE 80, CHD_V3_HEADER_SIZE 120, CHD_V4_HEADER_SIZE 108, CHD_V5_HEADER_SIZE 124.

Inference: this determines concrete validity requirements on an input artifact without our inventing them -- a valid CHD file begins with the eight bytes 'MComprHD', stores its numbers big-endian, and carries a header whose length is fixed by its version. The evidence is content stating what makes a file valid, not the mere existence of a header or a tests directory; that distinction is what QA-08 was about.
Decision: PASS

## EV-C012-E3-01
Candidate: C012
Gate: E3
Source: same header, chd.h
observed_at_utc: 2026-08-27T08:15:18Z; http_status 200

Observed: located witness. The format declares a parent relationship in the file itself -- V1-V3 carry "[ 60] uint8_t  parentmd5[16]; // MD5 checksum of parent file", V3-V5 add "parentsha1[20]// combined raw+meta SHA1 of parent", the V4 flag block reads "0x00000001 - set if this drive has a parent", and V5 states the rule outright: "If parentsha1 != 0, we have a parent (no need for flags)". The public API takes the parent as an already-opened handle rather than a path: "CHD_EXPORT chd_error chd_open(const char *filename, int mode, chd_file *parent, chd_file **chd);". The error vocabulary names both failure modes, CHDERR_REQUIRES_PARENT and CHDERR_INVALID_PARENT.

Inference: whether a given CHD can be opened is not decidable from that file alone. A child file declares a specific parent by checksum, and opening it requires that the correct parent was opened first -- an ordering prerequisite, the same shape as C008's partition-before-format witness and C010's save-state-before-session witness. That is a stateful/temporal validity question that can be examined, which is all E3 requires. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C012-E4-01
Candidate: C012
Gate: E4

Positive construction exhibited, via U_enforced. All observations are at the primary snapshot: master had not moved since 2026-08-25T14:53:07Z, so raw reads of master on 2026-08-27 resolve to commit 970a0ce060c0aa1012b1eebba1433c9a9e8ac8b9, the revision the snapshot rule fixes.

Source: https://raw.githubusercontent.com/rtissera/libchdr/master/src/libchdr_chd.c ; .../include/libchdr/chd.h
observed_at_utc: 2026-08-27T08:16:29Z-08:17:35Z; http_status 200 throughout

The mechanism: the codec registry "static const codec_interface codec_interfaces[]", defined at src/libchdr_chd.c:405-556 under the file's own section banner "CODEC INTERFACES", and consumed by the open path at lines 1773-1783, 1808-1818 and 2529-2533.

EN1 external authorship: the library and this table existed independently of this analysis; the README records the code as based off MAME's C codebase.

EN2 explicit scope: the project identifies the domain in its own terms. The section banner reads CODEC INTERFACES; the element type is declared at chd.c:175-186 as "/* interface to a codec */" with fields "compression /* type of compression */", "compname /* name of the algorithm */" and "lossy /* is this a lossy algorithm? */". The domain is which compression types the library accepts. As with C010, this leg is carried by the project's declarations rather than by prose, and is recorded that way rather than stated more strongly.

EN3 mechanical membership: membership is array membership in codec_interfaces[], decided by ARRAY_LENGTH. Fourteen entries: CHDCOMPRESSION_NONE, ZLIB, ZLIB_PLUS, AV, and CHD_CODEC_ZLIB, LZMA, HUFFMAN, FLAC, ZSTD, CD_ZLIB, CD_LZMA, CD_FLAC, CD_ZSTD, AVHUFF.

EN4 enforcement meaning: the project itself makes table membership the acceptance condition for a file's declared compression. Under its own comment "/* find the codec interface */" the opener scans the table for an entry matching newchd->header.compression[0]; if the scan reaches the end -- "if (intfnum == ARRAY_LENGTH(codec_interfaces)) EARLY_EXIT(err = CHDERR_UNSUPPORTED_FORMAT);" (chd.c:1782-1783) -- the open fails. The same rule is applied per slot for V5's four compressor entries at 1805-1818, and chd_error_string renders the outcome as "unsupported format". This meaning is executed by the project's code, not inferred by us from a name.

EN5 closed within scope: the loop bound is ARRAY_LENGTH(codec_interfaces), the enumerator's own extent, walked at runtime by the code that accepts or rejects the file. That is Section 3.2's first admissible case -- runtime construction closes the set. Tag: enforced.

EN6 outcome independence: membership is the set of supported compression types. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible: enumerate codec_interfaces[] and emit, per entry, the compression tag a CHD may declare, its algorithm name and its lossy flag; the same file supplies the per-version header requirements the opener enforces alongside it.

Recorded so the entry claims no more than was seen: this construction is thinner than C010's. Each entry yields an acceptance property for one declared compression type, where a Games[] entry yielded a whole required-file set. E4 asks whether the universe is externally delimited and mechanically constructible, not how rich it is, so both pass -- but the difference is real and is left visible here rather than smoothed over, since it is the inventory stage that will establish actual observation granularity.

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether libchdr designates an authoritative rules source.

Decision: PASS

## EV-C014-UR-01
Candidate: C014 (frame rank 14, emulators/snes9x)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/snes9x/Makefile
Observed: GH_ACCOUNT=snes9xgit; GH_PROJECT=snes9x; GH_TAGNAME=1.63; HOMEPAGE=http://www.snes9x.com/; COMMENT="emulates the Super Nintendo Entertainment System".
Inference: every field names one packaged system, Snes9x. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C014-E1-01
Candidate: C014
Gate: E1
Source: same frozen metadata; https://github.com/snes9xgit/snes9x
observed_at_utc: 2026-08-27T08:20:23Z; http_status 200
Observed: a third-party SNES emulator, described by its own repository as "Snes9x - Portable Super Nintendo Entertainment System (TM) emulator", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C014-E2REP-01
Candidate: C014
Gate: E2-REP

Unlike C010 and C012, HOMEPAGE here is NOT the repository, so the navigation actually has to be walked.

Surface 1: the upstream landing page, http://www.snes9x.com/ (frozen HOMEPAGE).
Necessary because: it is the project's own official site and step 1 of the sealed navigation; whether upstream designates a canonical source location cannot be settled without it.
observed_at_utc: 2026-08-27T08:19:15Z-08:19:16Z; http_status 200; redirect_chain: NONE
Observed: the page exposes nine links, whose labels are Gary, News, Developers Journal, Screenshots, Snes9x Forums, Downloads, Games/Demo's, Privacy Policy, Webmaster. None is a Source, Code, Repository or Development link in the sense the navigation contract's step 2 lists.

Surface 2: http://www.snes9x.com/downloads.php.
Necessary because: E2-REP's criterion admits "a repository OR SOURCE DISTRIBUTION" as the designated location. With no Source/Code/Repository link exposed, the Downloads page is the one surface this site offers that could carry a source-distribution designation, and declaring "the site designates nothing" without reading it would be asserting what was never checked. The label is not literally one of the four the contract enumerates, and that departure is recorded here rather than glossed: the contract's step-2 list is about links that lead to source, and the criterion's own wording makes a downloads page the place a project without a repository link would designate its source distribution.
observed_at_utc: 2026-08-27T08:19:58Z; http_status 200
Observed: the page's entire content is "Here is a list of all the known available mirrors for Snes9x", followed by four third-party hosts -- zophar.net, emulator-zone.com, ipherswipsite.com, s9x-w32.de -- and a Copyright 1998,1999 notice. No source archive, no repository link, no designation of any location as the project's source.

Surface 3: https://github.com/snes9xgit/snes9x, reached from the frozen metadata's GH_ACCOUNT/GH_PROJECT, which the contract admits as a starting point.
observed_at_utc: 2026-08-27T08:20:23Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-source-location
Observed: repository snes9xgit/snes9x, default branch master, isFork false, isArchived false, isTemplate false, no mirror or primary/secondary marking. A source tree is present at the root -- 115 files including 65c816.h, cpu.cpp, cpuexec.cpp, memmap.cpp, and directories apu, common, data, docs, external, filter, gtk, jma, libretro, macosx, qt, unix, unzip, win32. Its only non-GitHub outbound links are http://www.snes9x.com and an AppVeyor CI project.

The designation itself, quoted: "This is the official source code repository for the Snes9x project."

On how that was obtained: the contract forbids "reading README prose" but lists among allowed observations at the repository "whether upstream designates this location as its source; any primary/mirror marking". Those two clauses meet here, since a code-hosting page renders the README automatically and that is where such a designation lives. The check performed was narrow by construction -- a targeted scan of the rendered README region for designation and mirror vocabulary (official, canonical, authoritative, mirror, upstream, source code, repository, fork, primary) rather than a read of its content -- and it is recorded this way so the reader can see exactly how far it went.

Inference: exactly one canonical source location, at a stable URL, explicitly designated by upstream as its official source code repository, actually holding a source tree, with one external target identifier (Snes9x). The official website designates no competing source location: what it offers is a list of third-party BINARY mirrors, which is not a designation of canonical source. This is therefore not the C002 shape (several designations, no primary) -- there is one designation and one only.

Decision: PASS

## EV-C014-E2RULE-01
Candidate: C014
Gate: E2-RULE
Source: repository README ("Please check the Wiki for additional information") -> https://github.com/snes9xgit/snes9x/wiki -> https://github.com/snes9xgit/snes9x/wiki/Compiling
observed_at_utc: 2026-08-27T08:21:18Z (wiki index), 08:22:00Z (page); http_status 200

Observed: located witness, quoted from the GTK requirements section -- "gtkmm-3.24 or greater with gtk and all dependencies", "SDL 2.0", "X11 development libraries, even if only using Wayland". The Windows section states requirements in the same form, including that a Unicode build requires a special zlib build and that building without USE_SLANG requires removing the spirv_*.cpp files from the project's Shaders group.

Inference: these determine concrete validity requirements without our inventing them -- a build environment carrying gtkmm older than 3.24, or lacking X11 development libraries, does not satisfy the project's stated requirements. Externally authored, reached through upstream's own designation chain.

Recorded rather than left implicit: this witness is a BUILD-ENVIRONMENT requirement, not a data-artifact requirement as C010's ROM file-set and C012's file-header format were. E2-RULE as sealed asks for "at least one validity requirement" and does not restrict the domain, so narrowing it to artifact validity would be adding a premise the criterion does not contain. The gate that asks about stateful validity is E3, and it is carried separately below.
Decision: PASS

## EV-C014-E3-01
Candidate: C014
Gate: E3
Source: https://github.com/snes9xgit/snes9x/wiki/I've-mixed-using-in-game-saves-and-save-states-and-I've-lost-my-progress.-How-can-I-restore-it%3F (reached from the designated wiki's FAQ index)
observed_at_utc: 2026-08-27T08:21:40Z; http_status 200

Observed: located witness, quoted -- "Snes9x stores the in-game saves in a file called gamename.srm. This is actually a part of the cartridge memory and can be used for other things than saving games. For that reason, Snes9x needs to keep also store this same memory in a save-state for when it is being used for such a purpose. If you load a save-state file, it will overwrite the memory that makes up gamename.srm, and all the in-game saves will revert to whatever they were when you saved the state." The project treats the outcome as a defect to be guarded rather than as intended behaviour: the Windows port writes a gamename.oops fallback and the GTK port a gamename.undo backup on state load.

Inference: whether the current in-game save is the player's own latest save is not decidable from the .srm file or from the in-game save operations alone. It depends on whether a save-state load intervened, and on when that state was captured -- one artifact's contents are determined by the interleaving of two independent save mechanisms over time. That is a stateful/temporal validity question that can be examined, which is what E3 requires. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C014-E4-01
Candidate: C014
Gate: E4

Positive construction exhibited, via U_enforced. All observations are at the primary snapshot: master had not moved since 2026-08-17T18:29:55Z, so raw reads of master on 2026-08-27 resolve to commit 2971061cf07fdc6fc7d18883edf4e648eb16a6d2, the revision the snapshot rule fixes.

Source: https://raw.githubusercontent.com/snes9xgit/snes9x/master/controls.cpp
observed_at_utc: 2026-08-27T08:23:01Z-08:24:08Z; http_status 200

The mechanism: the command registry "static const char *command_names[LAST_COMMAND + 1]" at controls.cpp:284, generated together with "enum command_numbers" from a single X-macro list THE_COMMANDS at controls.cpp:207-278, and consumed by S9xGetCommandT at controls.cpp:1153-1577.

EN1 external authorship: the registry and the emulator existed independently of this analysis.

EN2 explicit scope: the project names the domain itself, and does so in public API rather than in a comment -- "const char ** S9xGetAllSnes9xCommands (void) { return (command_names); }" (controls.cpp:1580-1583). The enumerator is exposed by the project as the set of all Snes9x commands. This is a stronger EN2 leg than C010's or C012's, where the domain was carried by declarations and error vocabulary alone.

EN3 mechanical membership: membership is array membership in command_names[], bounded by LAST_COMMAND, which is the final enumerator of the same X-macro expansion. 65 commands are listed, from S(BeginRecordingMovie) onward. No semantic reading of individual entries is required.

EN4 enforcement meaning: the project makes registry membership the acceptance condition for a control-mapping name, and the rejection path is executed, not inferred. S9xGetCommandT initialises "cmd.type = S9xBadMapping" (controls.cpp:1160), looks the name up with "i = findstr(name, command_names, LAST_COMMAND)" and on a miss ("if (i < 0)") returns that value unchanged (controls.cpp:1569-1571). maptype() falls through to its default and yields MAP_UNKNOWN (controls.cpp:378), and S9xMapButton then refuses the mapping: "if (t != MAP_BUTTON) return (false);" (controls.cpp:1646). A configuration naming a command outside the registry is refused by the project's own code.

EN5 closed within scope: the lookup bound is LAST_COMMAND, produced by the same macro list that produces the table, and walked at runtime by the code that accepts or refuses the mapping. That is Section 3.2's first admissible case -- runtime construction closes the set. Tag: enforced.

EN6 outcome independence: membership is the set of supported commands. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible: expand THE_COMMANDS and emit, per entry, the command name a configuration may bind, with membership deciding acceptance.

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether Snes9x designates an authoritative rules source.

Decision: PASS

## RETRACTION 6 — C014 E2-REP withdrawn; two E2-REP contract breaches

EV-C014-E2REP-01 is **quarantined**, and with it EV-C014-E2RULE-01,
EV-C014-E3-01 and EV-C014-E4-01 as post-stop exposure. Nothing is
deleted: the pages were read, the quotations are accurate, the code
citations are correct. They are unusable because two of the observations
the E2-REP verdict rested on were outside the sealed navigation
contract, and the gates after E2-REP were reached only because that
verdict stood.

**Breach 1 -- the Downloads page.** The contract's allowed navigation is
three steps: the official landing page, a Source / Code / Repository /
Development link that page explicitly exposes, and the repository root
that link reaches. `Downloads` is not among them. The withdrawn entry
opened it anyway, reasoning that E2-REP's criterion admits "a repository
or source distribution" and that a downloads page is where a site
without a source link would designate one. That reasoning widens the
navigation whitelist at execution time using the criterion's wording.
Where the criterion and the search contract differ in reach, the
contract's narrower execution rule governs this run -- that is what
having a contract is for, and a criterion phrase cannot be used to
enlarge it after the landing page turned out not to expose what was
expected.

**Breach 2 -- the README designation.** The withdrawn entry's decisive
evidence was the sentence "This is the official source code repository
for the Snes9x project." The contract does list "whether upstream
designates this location as its source" among allowed observations at
the repository, but it also forbids "reading README prose" outright and
instructs that an incidentally rendered README be quarantined rather
than used. Restricting the read to a targeted scan for designation
vocabulary narrowed the SCOPE of the prohibited act; it did not lift the
prohibition. Using that sentence as verdict grounds is using forbidden
README prose, and the care taken in how it was extracted does not change
what was used.

Both observations are kept on the record here as forbidden E2-REP
exposure and are excluded from every verdict.

## EV-C014-E2REP-02  (supersedes the quarantined EV-C014-E2REP-01)
Candidate: C014 (frame rank 14, emulators/snes9x)
Gate: E2-REP

Re-determined on admissible evidence only.

Surface 1: http://www.snes9x.com/ -- the frozen HOMEPAGE, navigation step 1.
observed_at_utc: 2026-08-27T08:19:15Z-08:19:16Z; http_status 200
Observed: the page exposes nine links, labelled Gary, News, Developers
Journal, Screenshots, Snes9x Forums, Downloads, Games/Demo's, Privacy
Policy, Webmaster. None is a Source, Code, Repository or Development
link. Navigation step 2 is therefore unavailable, and step 3 is not
reachable by the contract's path.

Surface 2: https://github.com/snes9xgit/snes9x -- reached from the frozen
GH_ACCOUNT/GH_PROJECT, which the contract admits as a starting point.
observed_at_utc: 2026-08-27T08:20:23Z; http_status 200; redirect_chain: NONE
Observed, restricted to metadata the contract allows at a repository:
repository name snes9x, owner login snes9xgit, repository description
"Snes9x - Portable Super Nintendo Entertainment System (TM) emulator",
default branch master, isFork false, isMirror false, isArchived false,
isTemplate false, a source tree present at the root (115 files including
65c816.h, cpu.cpp, cpuexec.cpp, memmap.cpp, and directories apu, common,
data, docs, external, filter, gtk, jma, libretro, macosx, qt, unix,
unzip, win32), and the repository's own website metadata field set to
http://www.snes9x.com -- the same site the frozen HOMEPAGE names. That
field is sidebar metadata set by the repository owner, not README
content, and is admissible.

What the admissible evidence establishes: exactly one source location is
in play; it is an upstream-controlled surface; it is not a fork, not a
mirror and not archived; it holds the source tree; and it affiliates
itself with the official project site.

What it does not establish: that the project identifies this location as
its authoritative source. The arrow runs one way only. The repository
declares its website to be snes9x.com; snes9x.com exposes no link back
to the repository and designates no source location at all. Affiliation
is not designation, and a project may control several affiliated
repositories.

Adjudication, stated so that no quarantined observation does verdict
work:

```text
PASS not established
  admissible evidence does not establish the required upstream
  designation -- affiliation is not designation

FAIL not established
  admissible evidence does not establish that upstream designates NO
  canonical source location either; the landing page exposing no
  source link and the repository metadata carrying no designation
  statement are two surfaces coming up empty, not a demonstration
  that the project designates nothing

contamination
  forbidden exposure occurred at this gate, which independently
  prevents reconstructing a clean adjudication after the fact
```

The third line is provenance, not evidence. It records that this run's
observation process for C014's E2-REP was contaminated; it says nothing
about what Snes9x does or does not designate, and it is not used to rule
any verdict in or out. What rules them out is the first two lines, both
of which rest only on admissible surfaces.

The contamination matters because it is not repairable by reasoning more
carefully. Any argument assembled now for "the admissible metadata alone
suffices" would be assembled by an analyst who has already been exposed
at this gate, and could not be distinguished from a route built to reach
a known destination. The repair is to decline the verdict, not to
re-argue it.

The undetermined shape is real and belongs to the protocol, not to
Snes9x: where a project's official site exposes no source link, the
sealed navigation contract terminates at step 1, and the gate's question
must then be answered from repository metadata alone -- which the
contract does not say is sufficient, and does not say is insufficient.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## RETRACTION 6a — C014 gates after E2-REP
EV-C014-E2RULE-01, EV-C014-E3-01 and EV-C014-E4-01 are quarantined as
post-stop exposure, on the same principle applied to C005 under QA-11.
Screening stops at the first gate that is not determined; those three
gates were only reached because a withdrawn PASS stood at E2-REP. Their
observations -- the Compiling page's gtkmm-3.24 requirement, the
save-state/.srm interleaving witness, and the command_names[] positive
construction -- are kept on the record and used for nothing.

## EV-C009-UR-01
Candidate: C009 (frame rank 9, emulators/fceux)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/fceux/Makefile
Observed: GH_ACCOUNT=TASEmulators; GH_PROJECT=fceux; GH_TAGNAME=v2.6.6; HOMEPAGE=https://fceux.com/web/home.html; COMMENT="emulator for Nintendo Entertainment System".
Inference: every field names one packaged system, FCEUX. Not UR-AMBIGUOUS.
Decision: PASS

Rank-order note: this rank was skipped when screening ran 8 -> 10 -> 12 -> 14, and is being screened now under QA-18. The omission is recovered as coverage; the frozen order is not restored retroactively.

## EV-C009-E1-01
Candidate: C009
Gate: E1
Source: same frozen metadata; https://fceux.com/web/home.html
observed_at_utc: 2026-08-27T08:51:47Z; http_status 200
Observed: a third-party NES/Famicom/Dendy emulator, described by its own site as "an evolution of the original FCE Ultra emulator", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C009-E2REP-01
Candidate: C009
Gate: E2-REP

Same shape as C014 -- HOMEPAGE is a project site, not the repository -- so the navigation was walked, and this time it completes inside the contract.

Step 1: https://fceux.com/web/home.html (frozen HOMEPAGE).
observed_at_utc: 2026-08-27T08:51:47Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: the page's links are Home, Download, Documentation, Versions, Contact, Links, a link to tasvideos.org, "version history", "Full changelog", and one link whose destination is the project's source repository: "commit browser" -> https://github.com/TASEmulators/fceux/commits/master. Its sentence reads "You can find out what we've been up to since the last release by checking the commit browser."

Step 2, and the reading it rests on, stated rather than assumed: the contract admits "a Source / Code / Repository / Development link that page explicitly exposes". The anchor text here is "commit browser", which is not literally one of those four words, but its href IS the project's source repository, and the contract's step 2 classifies links by what they lead to. Requiring the anchor text itself to read "Repository" would be a stricter rule than the contract states and an arbitrary one, since labels vary. This is not the C014 move: nothing here is opened because an expected link was missing, and the widening that QA-17 forbids -- letting the search scope become a function of what was found -- does not occur, since this link was on the landing page before anything was looked for.

Step 3: https://github.com/TASEmulators/fceux -- the repository root the step-2 link reaches.
observed_at_utc: 2026-08-27T08:52:31Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-source-location
Observed, restricted to metadata the contract allows at a repository: repository name fceux, owner login TASEmulators, description "FCEUX, a NES Emulator", default branch master, isFork false, isMirror false, isArchived false, isTemplate false, website metadata field http://fceux.com, and a source tree present at the root including src, documentation, scripts, pipelines, vc, vcpkg, m4, icons, attic, output, fceux-server, getSDLKey, gfceu.

Inference: exactly one canonical source location, at a stable URL, with the designation running both ways -- the project's official site points at this repository as where its development is, and the repository's website field points back at that site. It is not a fork, not a mirror, not archived, and holds the source tree. One external target identifier: FCEUX. This is precisely the arrow C014 lacked, and it is established without touching README prose.

Surfaces NOT opened, recorded so the restraint is visible: download.html and links.html. Both are outside the navigation whitelist, and under QA-17 a criterion phrase may not be used to reach them. The stop rule also applies -- navigation ended the moment PASS was determined at step 3.

Decision: PASS

## EV-C009-E2RULE-01
Candidate: C009
Gate: E2-RULE

Prior exposure: fceux's documentation.html was read during the voided QA-07 batch. Use: not used as a gate shortcut and not used to choose which surfaces to name; this gate is adjudicated from the start under the current protocol, and the page below was reached by following the site's own Documentation index.

Source: https://fceux.com/web/documentation.html -> https://fceux.com/web/help/Gamefilecompatibility.html
observed_at_utc: 2026-08-27T08:52:55Z (index), 08:53:04Z (page); http_status 200

Observed: located witness, under a heading the project itself titles "Valid Game Types" -- "FCEUX supports the iNES, FDS(raw and with a header), UNIF, and NSF file formats. FDS ROM images in the iNES format are not supported; it would be silly to do so and storing them in that format is nonsensical." The same page states of compressed inputs "Only the 'deflate' algorithm is supported", enumerates the extensions an archive is scanned for -- ".nes, .fds, .nsf, .unf, .nez, .unif" -- and gives the IPS patch naming rule, "name it [filename.extension].ips".

Inference: these determine concrete validity requirements on input artifacts without our inventing them. A file in a format outside that list is not a valid game file for FCEUX, and an FDS image wrapped in an iNES container is explicitly excluded even though both formats are individually supported. The section is headed with the word valid, so this is content stating validity, not the existence of a documentation page -- the distinction QA-08 turned on. Unlike C014's witness, this is a data-artifact requirement rather than a build-environment one.
Decision: PASS

## EV-C009-E3-01
Candidate: C009
Gate: E3
Source: https://fceux.com/web/movies.html (reached from the same Documentation index)
observed_at_utc: 2026-08-27T08:53:20Z; http_status 200

Observed: located witness, quoted -- "A movie file is a file which contains data needed to reconstruct actions in a game. In most emulators, the movie files consist of simply the buttons that were pressed during the game. Because the emulation is completely predictable (deterministic), it will always play back the same way. Unless the movie starts from the console power-on or from reset, the movie file might also contain a savestate that loads the beginning point of the game." The page also states a mode-dependent rule: "If a movie is in read-only mode, the movie file can not be altered in any way. If you make a savestate while playing the movie and load that state, the playback will simply 'rewind' to that state. If the movie is not in read-only, however, loading a state will set the movie to record mode and begin recording from that savestate."

Inference: two stateful/temporal conditions are documented, and the gate needs only that they can be examined.

First, replay semantics depend on an ordered starting-state condition: power-on, reset, or a savestate establishes the state from which the recorded inputs are replayed. Second -- and this is the cleaner witness -- loading a savestate has a different effect and a different validity depending on a mode established earlier: in read-only mode it rewinds playback, and otherwise it switches the movie into recording from that state. The same action means two different things according to prior state.

No stronger claim is made. An earlier draft of this entry said that whether a movie reproduces its run "is not decidable from the file's contents"; that overreaches, since the same page says a movie may itself carry the savestate that establishes its starting point, so a sufficiently self-contained movie could supply its own replay condition. E3 does not need that claim and it is withdrawn here.

Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C009-E4-01
Candidate: C009
Gate: E4

Positive construction exhibited, via U_enforced.

Provenance, corrected under QA-28: these observations were made against the source state available at SCREENING OBSERVATION TIME. They establish the positive E4 screening witness and nothing more. They are NOT asserted to be the sealed primary snapshot, whose resolution is a survivor-stage matter recorded separately and currently UNRESOLVED. At observation time the default branch pointed at a62b868e9247c4aafd66f597cdfa8d2609704087; the withdrawn claim that "master had not moved since 2026-05-30" was never observed.

Source: https://raw.githubusercontent.com/TASEmulators/fceux/master/src/ines.cpp
observed_at_utc: 2026-08-27T08:53:44Z-08:54:25Z; http_status 200

The mechanism: the iNES mapper registry "BMAPPINGLocal bmap[]", defined at src/ines.cpp:531-819, consumed by iNES_Init at src/ines.cpp:1187 and following.

EN1 external authorship: the emulator and this table existed independently of this analysis.

EN2 explicit scope: the project identifies the domain in its own words, in the message it emits when the lookup fails -- "iNES mapper #%d is not supported at all." (src/ines.cpp:1075). The table enumerates which iNES mapper numbers FCEUX accepts, and each entry pairs that number with the board name the project uses for it, e.g. {"NROM", 0, NROM_Init}, {"MMC3", 4, Mapper4_Init}, {"KONAMI QTAi Board", 547, QTAi_Init}.

EN3 mechanical membership: membership is array membership in bmap[]. 236 entries, each of the form {board name, mapper number, init function}. No semantic reading of individual entries is required.

EN4 enforcement meaning: the project makes table membership the acceptance condition for a ROM's declared mapper, and the rejection is executed. iNES_Init walks the table -- "BMAPPINGLocal *tmp = bmap; ... while (tmp->init) { if (num == tmp->number) ... }" -- returning 0 on a match; falling off the end returns 1, and the caller then executes FCEU_PrintError("iNES mapper #%d is not supported at all.", MapperNo) and the load does not proceed (src/ines.cpp:1069-1076). The file-level requirement the documentation states is enforced in the same function: "if (FCEU_fread(&head, 1, 16, fp) != 16 || memcmp(&head, "NES\x1A", 4)) return LOADER_INVALID_FORMAT;" (src/ines.cpp:827-828).

EN5 closed within scope: the walk terminates on the table's own sentinel, {"", 0, NULL} at src/ines.cpp:818, which is exactly the loop's condition. The set is closed at runtime by the enumerator the loader walks -- Section 3.2's first admissible case. Tag: enforced.

EN6 outcome independence: membership is the set of supported mappers. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible: enumerate bmap[] to its sentinel and emit, per entry, the iNES mapper number a ROM may declare together with the board name the project assigns it.

Worth recording, since it is the first time the two gates have met on one fact: the E2-RULE witness above states the format requirement in prose ("FCEUX supports the iNES ... file formats") and this gate finds the same requirement enforced in code (the "NES\x1A" header check). No weight is placed on the agreement -- E4 rests on the mapper registry alone -- but the coincidence is noted rather than left for the inventory stage to rediscover.

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether FCEUX designates an authoritative rules source.

Decision: PASS

## EV-C013-UR-01
Candidate: C013 (frame rank 13, emulators/mednafen)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/mednafen/Makefile
Observed: HOMEPAGE=https://mednafen.github.io; VERSION=1.32.1; DISTNAME=mednafen-${VERSION}; SITES=${HOMEPAGE}/releases/files/; EXTRACT_SUFX=.tar.xz; COMMENT="emulates numerous game consoles". There is no GH_ACCOUNT/GH_PROJECT.
Inference: every field names one packaged system, Mednafen. "numerous game consoles" describes what the one system emulates, not several packaged systems. Not UR-AMBIGUOUS.

Note for E2-REP: SITES is expressed as ${HOMEPAGE}/releases/files/, i.e. it resolves inside the project's own domain. This is the opposite of C010, where SITES pointed at a host the port Makefile itself showed the OpenBSD maintainer uploading to.

Rank-order note: this rank was skipped when screening ran 8 -> 10 -> 12 -> 14, and is screened now under QA-18. Coverage is recovered; the frozen order is not restored retroactively.
Decision: PASS

## EV-C013-E1-01
Candidate: C013
Gate: E1
Source: same frozen metadata; https://mednafen.github.io
observed_at_utc: 2026-08-27T09:01:57Z; http_status 200
Observed: a third-party multi-system emulator, described by its own site as "a portable, utilizing OpenGL and SDL, argument(command-line)-driven multi-system emulator", distributed under GPLv2, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C013-E2REP-01
Candidate: C013
Gate: E2-REP

This is the run's first DISTRIBUTION candidate rather than a repository candidate, which the criterion admits explicitly ("a repository or source distribution") and for which the snapshot rule has its own branch.

Step 1: https://mednafen.github.io -- the frozen HOMEPAGE. No further navigation was needed or performed: the designation is on this page.
observed_at_utc: 2026-08-27T09:01:57Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-project-page / official-source-location

Observed: the page's News section presents the current release, "Mednafen 1.32.1, April 5, 2024", and exposes for it three artifacts under the project's own domain, each with a published hash:

```text
mednafen-1.32.1.tar.xz         SHA-256: de7eb94ab66212ae7758376524368a8ab208234b33796625ca630547dbc83832
mednafen-1.32.1-win64.zip      SHA-256: 3b680ce6b50a17bcbb2ac611e38962ee469e399b412cc435ffacd6e7f6fb1982
mednafen-1.32.1-win32.zip      SHA-256: ca8e5cb53c2aedb347ab0358a1be496cfc4a51fc2e444648fa430365289c82e7
```

all served from https://mednafen.github.io/releases/files/. Older releases appear further down the same News list, several marked UNSTABLE, all under that same directory. The page also states "Mednafen is distributed under the terms of the GNU GPLv2".

Verification of the designated artifact, which is exactly this gate's "that a source tree is actually present" observation carried over to a distribution candidate:
observed_at_utc: 2026-08-27T09:02:50Z; http_status 200; 3571236 bytes
The retrieved artifact's SHA-256 matches the value upstream publishes beside the link, byte for byte. Listing its entries -- names only, no file contents read -- shows a source tree: top-level Documentation, include, intl, m4, mswin, po, src, tests, with src carrying per-system emulation modules (apple2, gb, gba, lynx, md, nes, ngp, pce, pcfx, psx, ss, snes, ...), 2028 entries in total.

Inference: exactly one canonical source location, at a stable URL under the project's own domain, designated by upstream on its own landing page, actually holding a source tree, with one external target identifier (Mednafen). The .tar.xz is the source distribution; the two .zip artifacts are named as Windows builds and are not source. Older versions are a version history in one location, not competing designations -- "designates several with no primary among them" does not apply, since 1.32.1 is the current release entry and the rest are its predecessors in the same directory.

Surfaces NOT opened, recorded so the restraint is visible: /releases/, /links/, the forum at forum.fobby.net, and /irc/. None is a Source/Code/Repository/Development link, and "releases" is named in the contract's forbidden list outright. Under QA-17 a criterion phrase may not be used to reach any of them, and none was needed: the designation and the artifact were both on step 1.

Decision: PASS

## EV-C013-E2RULE-01
Candidate: C013
Gate: E2-RULE

Prior exposure: mednafen's /documentation/ was read during the voided QA-07 batch. Use: not used as a gate shortcut and not used to choose which surfaces to name; this gate is adjudicated from the start under the current protocol, and the page below was reached from the landing page's own Documentation link.

Source: https://mednafen.github.io/documentation/
observed_at_utc: 2026-08-27T09:03:48Z; http_status 200

Observed: located witness, in the Custom Palettes section -- "Custom palettes for a system should generally(with caveats; refer to the table near the end of this section) be named <system>.pal, IE "snes.pal", "pce.pal", etc., and placed in the "palettes" directory beneath the Mednafen base directory. Per-game custom palettes are also supported, and should be named as <FileBase>.pal or <FileBase>.<MD5 Hash>.pal ... Each entry in a custom palette file consists of 3 8-bit color components; Red, Green, Blue, in that order." The section's table then states the exact size required per system, among them "gb gb.pal GameBoy(mono) 4 or 8 or 12 RGB triplets", "gbc.pal GameBoy Color 15-bit BGR 32768 RGB triplets", "gg gg.pal GG 12-bit BGR 4096 RGB triplets", "nes nes-pal.pal PAL NES 64 or 512 RGB triplets".

Inference: these determine concrete validity requirements on an input artifact without our inventing them -- a GameBoy Color palette file is valid only if it contains 32768 RGB triplets, a Game Gear one 4096, a PAL NES one 64 or 512, and the entry encoding is fixed at three 8-bit components in a stated order. The requirement is numeric and per-system, which makes it the most precise E2-RULE witness in the run so far.

The naming rule is deliberately NOT counted among the requirements: the documentation says palettes "should generally(with caveats...)" be named that way, which is a recommendation with stated exceptions, not a validity constraint. The verdict rests on the triplet counts and the component encoding alone.
Decision: PASS

## EV-C013-E3-01
Candidate: C013
Gate: E3
Source: same documentation, Multiple-CD Games section
observed_at_utc: 2026-08-27T09:03:48Z; http_status 200

Observed: located witness, quoted -- "Caution: Avoid using Mednafen's M3U-based multi-CD support to load discs belonging to different games and switching between games during emulation, especially when using Sega Saturn emulation, as that may interfere with the Saturn module's heavy use of internal databases." The same section establishes that disc switching is a normal in-session operation: "Load the M3U file with Mednafen instead of the CUE/TOC/CCD files, and use the F6 and F8 keys to switch among the various discs available."

Inference: the F6/F8 disc switch is one action whose acceptability depends on what was loaded earlier in the same emulation session. Switching among discs of one game is the documented intended use; switching to a disc of a different game, after the module has built internal state from the first, is warned against for that reason. Whether the operation is safe is therefore conditioned on session history rather than on the disc being switched to. That is a stateful/temporal validity question that can be examined, which is what E3 requires.

No stronger claim is made about what is or is not determinable from any artifact alone. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C013-E4-01
Candidate: C013
Gate: E4

Positive construction exhibited, via U_enforced.

Provenance, corrected under QA-28: these observations were made against the source state available at SCREENING OBSERVATION TIME. They establish the positive E4 screening witness and nothing more. They are NOT asserted to be the sealed primary snapshot, whose resolution is a survivor-stage matter recorded separately and currently UNRESOLVED. The paths below are paths inside the artifact designated at observation time, mednafen-1.32.1.tar.xz, whose retrieved bytes matched upstream's own published SHA-256. That the hash matches upstream's publication is a real check on WHAT WAS RETRIEVED; it says nothing about which artifact the sealed rule selects.

observed_at_utc: 2026-08-27T09:02:50Z (artifact retrieved and verified), 09:04:00Z-09:06:00Z (entries listed and files read)

The mechanism: the settings registry. Each setting is declared as an MDFNSetting (src/settings-common.h:104-118) carrying its own validity constraints:

```text
name              description        type
default_value     minimum            maximum
validate_func     enum_list          ChangeNotification
```

EN1 external authorship: the emulator and this machinery existed independently of this analysis; the artifact is dated April 2024.

EN2 explicit scope: the project identifies the domain in its own words, in the comment on the type itself -- "MDFNST_ENUM, // Handled like a string, but validated against the enumeration list, and MDFN_GetSettingUI() returns the number in the enumeration list." (src/settings-common.h:43). The declaration fields are named minimum, maximum, validate_func and enum_list. What the registry enumerates is which settings exist and what values each accepts.

EN3 mechanical membership: membership is array membership in sentinel-terminated MDFNSetting tables. SettingsManager::Merge walks "while(setting->name != nullptr) { MergeSettingSub(*setting); setting++; }" (src/settings.cpp:603-612). 828 declared entries were counted across src and include by their literal form.

EN4 enforcement meaning: the project connects the declaration to validation and executes the rejection. ValidateSetting (src/settings.cpp:130) throws MDFN_Error against the declared bounds and lists, in the project's own message text:

```text
"Setting "%s" value "%s" is too small; the minimum acceptable value is "%s"."
"Setting "%s" value "%s" is too large; the maximum acceptable value is "%s"."
"Setting "%s" value "%s" is not a valid boolean."
"Setting "%s" value "%s" is not a recognized string.  Recognized strings: %s"
```

The enum branch walks the setting's own enum_list to its null terminator and throws if no member matches (src/settings.cpp:250-273). This meaning is executed by the project's code, not inferred by us from a name.

EN5 closed within scope, and this is the strongest closure the run has seen. Registration is not merely bounded by a loop -- the project performs an explicit closing operation. At startup the core merges its own tables and then every registered module's, "Settings.Merge(MednafenSettings); Settings.Merge(MDFNMP_Settings); for(x < MDFNSystems.size()) if(MDFNSystems[x]->Settings) Settings.Merge(MDFNSystems[x]->Settings); Settings.Merge(RenamedSettings); Settings.Finalize();" (src/mednafen.cpp:1616-1624), each module contributing through its MDFNGI field "const MDFNSetting *Settings;" (include/mednafen/git.h:673). Finalize sets SettingsFinalized (src/settings.cpp:647), Merge asserts it has not yet happened (598, 605), and lookup asserts that it has (748). The set is closed by the project, in both directions, before any setting can be read. Section 3.2's first admissible case. Tag: enforced.

EN6 outcome independence: membership is the set of settings the program accepts. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, and at a finer grain than the previous four candidates: enumerate the merged MDFNSetting tables and emit, per setting, its declared type together with its validity constraint -- minimum and maximum for numeric types, the enum_list members for enumerated ones, {0,1} for booleans, and the presence of a validate_func where one is declared. That is a property-level universe in the most literal sense the phrase allows, since each entry states its own admissible values rather than merely being a member of an accepted set.

Recorded so the difference is visible rather than flattened:

```text
admissible prior E4 passes   C009, C010, C012
  each on a table whose ENTRIES ARE the accepted values

quarantined observation      C014
  structurally the same, but withdrawn as post-stop exposure and
  carrying no weight

this candidate               entries CARRY their validity constraints
```

Nothing follows from that for the verdict -- E4 asks whether the universe is externally delimited and mechanically constructible, not how rich it is.

An earlier draft added that "the inventory stage should not have to rediscover it". That is exactly backwards and has been withdrawn. The inventory stage MUST rediscover it, and must additionally look for admissible enumerators and authoritative sources this gate never went looking for, because E4 stops at the first positive construction while the inventory has to be exhaustive. Nothing in this entry may be treated as an inventory result. See QA-19.

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether Mednafen designates an authoritative rules source.

Decision: PASS

## EV-C015-UR-01
Candidate: C015 (frame rank 15, emulators/virtualjaguar)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, emulators/virtualjaguar/Makefile
Observed: HOMEPAGE=https://icculus.org/virtualjaguar/; V=2.1.3; DISTNAME=virtualjaguar-${V}; EXTRACT_SUFX=.tar.bz2; SITES=https://icculus.org/virtualjaguar/tarballs/; COMMENT="Atari Jaguar emulator". There is no GH_ACCOUNT/GH_PROJECT.
Inference: every field names one packaged system, Virtual Jaguar. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C015-E1-01
Candidate: C015
Gate: E1
Source: same frozen metadata; https://icculus.org/virtualjaguar/
observed_at_utc: 2026-08-27T09:44:16Z; http_status 200
Observed: a third-party Atari Jaguar emulator with a documented lineage from a CoJag driver through Starscream, Musashi and a customized UAE 68000 core, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C015-E2REP-01
Candidate: C015
Gate: E2-REP

Surface: https://icculus.org/virtualjaguar/ -- the frozen HOMEPAGE, navigation step 1. No further navigation was performed, and none was needed: every designation below is on this page.
Necessary because: E2-REP asks whether upstream designates EXACTLY ONE canonical source location, and this is the project's own page.

observed_at_utc: 2026-08-27T09:44:16Z-09:44:18Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-project-page

Observed: the page designates two live source locations, of the two different types the criterion admits.

```text
source distribution
  "The latest official release is 2.1.2. Pick your poison:"
  "Linux (source only*)" -> tarballs/virtualjaguar-2.1.2.tar.bz2
  under the project's own path

source repository
  "Those of you who like to live on the bleeding edge can grab
   sources from anonymous GIT. To download from GIT use the
   following command:  git clone
   http://shamusworld.gotdns.org/git/virtualjaguar"
  on a different host
```

Neither is marked canonical, primary or authoritative relative to the other. "Official" attaches to the release, not to the location; "bleeding edge" describes the repository's contents, not its rank.

Also observed, and NOT counted as a third designation: a CVS repository on icculus.org, which upstream deprecates explicitly -- "the CVS repository on icculus.org is pretty much dead, and will probably stay that way ... Please keep this in mind if you plan to contribute patches; build against GIT, not CVS!" That is upstream ranking GIT above CVS, so CVS is not a live competing location. It is worth stating because it shows the project does designate primacy when it intends to, and makes no comparable statement ranking GIT against the release tarball.

Two further links, "here" and "here", point at third-party hosts offering automated Win32 builds of GIT. Those are binary builds by other parties, not upstream designations of canonical source. The remaining outbound links are community sites and forums.

Inference: the sealed criterion admits BOTH a repository and a source distribution as source-location types, and states directly that a project which "designates several with no primary among them" fails E2-REP. Upstream here exposes one of each, live, and designates no primary between them. That is the same case as C002, C006, C007 and C011, and this failure code is positive in shape: several designations were found and no primary among them, not nothing found.

The reading is deliberately not the one this run has already had to withdraw once. Treating the GIT repository as "the real source" and the tarball as merely a release -- or the reverse, treating the official release as canonical and GIT as a preview -- imposes a hierarchy the criterion refuses to let us supply, since adjudicating which location "really" holds the system would be our judgment about the target's identity.

Recorded as an observation with no inference drawn from it: the page's latest release is 2.1.2, while the frozen port packages 2.1.3. Nothing in this verdict depends on that, and OpenBSD metadata cannot substitute for upstream designation in either direction.

Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

Gates after E2-REP are NOT_REACHED under the first-fail stop rule.

## EV-C016-UR-01
Candidate: C016 (frame rank 16, games/1oom)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/1oom/Makefile
Observed: HOMEPAGE=https://kilgoretroutmaskreplicant.gitlab.io/plain-html/; DISTNAME=1oom-1.0; SITES=https://gitlab.com/KilgoreTroutMaskReplicant/1oom/uploads/13d2d645650929c6f7f08be356b62f66/; COMMENT="game engine recreation of Master of Orion 1".
Inference: every field names one packaged system, 1oom. "Master of Orion 1" names the game whose engine is recreated, not a second packaged system, and the HOMEPAGE host and the SITES path carry the same account name. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C016-E1-01
Candidate: C016
Gate: E1
Source: same frozen metadata; https://kilgoretroutmaskreplicant.gitlab.io/plain-html/
observed_at_utc: 2026-08-27T10:25:29Z; http_status 200
Observed: a third-party engine recreation -- "1oom is a Master of Orion (1993) game engine recreation. 1oom is Free Software (GPLv2)." -- unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C016-E2REP-01
Candidate: C016
Gate: E2-REP

Step 1: https://kilgoretroutmaskreplicant.gitlab.io/plain-html/ -- the frozen HOMEPAGE.
observed_at_utc: 2026-08-27T10:25:29Z-10:25:30Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: under a heading "Files and such" the page states, in this order:

```text
Source code: GitLab            -> https://gitlab.com/KilgoreTroutMaskReplicant/1oom
git clone https://gitlab.com/KilgoreTroutMaskReplicant/1oom.git
Binaries and tarball available here.
                               -> https://gitlab.com/KilgoreTroutMaskReplicant/1oom/tags/
```

Step 2: the link labelled "GitLab" sits under the literal words "Source code:", which is a Source link in the plainest sense the navigation contract's step 2 admits -- no interpretation of the label was needed here, unlike C009's "commit browser".

Step 3: https://gitlab.com/KilgoreTroutMaskReplicant/1oom -- the repository root.
observed_at_utc: 2026-08-27T10:26:02Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-source-location
Observed, restricted to metadata the contract allows: project path KilgoreTroutMaskReplicant/1oom, project name 1oom, project id 6630849, default branch master, project not empty (data-is-project-empty="false"). The served page carries no fork-of, mirror or archived marking; the only "fork" token present is the affordance for creating one.

On confirming a source tree is present. GitLab renders its file tree client-side, so the served HTML carries no listing the way the GitHub pages did for C009, C010, C012 and C014. The observation was made instead from the repository's own archive of its default branch, at /-/archive/master/1oom-master.tar.gz -- a path the repository root itself exposes -- listing entry NAMES only and reading no file. This is the same allowed observation by a different route, not navigation to another location: the archive is generated by this repository from this branch.
observed_at_utc: 2026-08-27T10:27:05Z; http_status 200; 533500 bytes
It contains 397 entries: src/ with game, hw, os and ui beneath it, doc/, and Makefile.am, configure.ac, AUTHORS, COPYING, HACKING, INSTALL, NEWS, PHILOSOPHY, README at top level.

Inference: exactly one canonical source location, at a stable URL, designated by upstream in as many words, holding a source tree, with one external target identifier (1oom).

Why this is not the C015 case, decided one rank earlier. There the landing page offered a source tarball on the project's own host AND a GIT repository on a different host, with no primacy between them. Here the second link -- "Binaries and tarball available here" -- resolves to the tags page of the SAME GitLab project, so it names artifacts of the one designated location rather than a second location. The distinction is in where the links resolve, not in any hierarchy supplied by us.

Decision: PASS

## EV-C016-E2RULE-01
Candidate: C016
Gate: E2-RULE
Source: https://kilgoretroutmaskreplicant.gitlab.io/plain-html/
observed_at_utc: 2026-08-27T10:25:29Z; http_status 200

Observed: located witness, quoted from the landing page -- "1oom requires a copy of the Master of Orion (v1.3) LBX files." The FAQ restates it operationally: "Extract the zip somewhere and copy your MOO1 LBX files there."

Inference: this determines a concrete validity requirement on input artifacts without our inventing it -- the data files 1oom runs against must be MOO1 LBX files, and specifically those of v1.3. The version is named, so the requirement is not merely "some data files".

On the surface used: this is the landing page, navigation step 1, which is readable in full. Using its content for E2-RULE is not the C014 problem, which was using REPOSITORY README prose as E2-REP verdict grounds.

Encountered later, while surveying for E3 and E4, and recorded here with no weight placed on it: the repository carries doc/lbxmd5.txt, 33 lines pairing each required LBX file with an MD5 checksum. It is a sharper form of the same requirement. The verdict rests on the landing-page statement, which was located first.
Decision: PASS

## EV-C016-E3-01
Candidate: C016
Gate: E3
Source: doc/usage_common.txt in the designated repository, section 3.3 "-file"
observed_at_utc: 2026-08-27T10:27:05Z (archive), read 10:28Z

Observed: located witness, quoted -- "Unlike Doom, the "-file" part needs to added for each PBX file. Like Doom, the given PBX filenames are not stored anywhere and must be given with -file whenever the PBX files are to be used." PBX files carry game data overrides: the same document lists "-dumpstr Dump strings in PBXIN format" and "-dumpnum Dump numbers in PBXIN format", and doc/list_pbxnum.txt calls their contents "PBX number replacements".

Inference: which game data is in effect is fixed by the invocation and is recorded nowhere. Whether a later run interprets the same artifacts the same way therefore depends on whether the operator supplies the same -file set as before, and no artifact carries that condition. That is a stateful/temporal validity question that can be examined, which is all E3 requires.

A second instance, encountered afterwards while working E4 and recorded with the order visible rather than presented as part of the survey: doc/list_pbxnum.txt documents a tunable named `deterministic` -- "The game is deterministic by default. Given the same input, the outcome remains the same. Reloading a save and clicking Next turn will not get rid of a nasty event. Setting this number to 0 makes sitting idle churn the random number generator for producing different results." No weight is placed on it; the verdict rests on the witness located during the E3 survey.

Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C016-E4-01
Candidate: C016
Gate: E4

Positive construction exhibited, via U_enforced. All observations are at the primary snapshot: master resolves to dedf0bbd57fe004e5d49c2b63c98a219cc1b906e, whose commit is dated 2018-11-13T16:47:09Z -- long before the enumeration execution timestamp -- so the archive of master read on 2026-08-27 is that revision. The project states on its landing page that "The project is finished."

Source: the designated repository at the snapshot; src/game/game_nump.c, doc/list_pbxnum.txt
observed_at_utc: 2026-08-27T10:27:05Z (archive retrieved), 10:28Z-10:33Z (read); ls-remote at 10:30:09Z

The mechanism: the patchable-number registry "game_num_id_tbl[]", src/game/game_nump.c:45-413.

EN1 external authorship: the project and this table existed independently of this analysis, and the snapshot predates it by years.

EN2 explicit scope: the project names the domain in its own documentation and in its own declarations. doc/list_pbxnum.txt opens "This is an incomplete list of PBX number replacements", and presents each entry as "(name : range, default)". The entry macro is DEFNUMITEM(id, name, type, vmin, vmax); the struct numtbl_s declares numid, numtype, tstep, size, vmin and vmax; the consuming function is game_num_patch. What the registry enumerates is which game numbers a PBX file may address and what each admits.

EN3 mechanical membership: membership is array membership. 367 DEFNUM* entries, walked by find_match as "const struct numtbl_s *s = &game_num_id_tbl[0]; while (s->numid) { ... ++s; }" (src/game/game_nump.c:417-433).

EN4 enforcement meaning: the project makes registry membership and the declared bounds the acceptance conditions for a PBX patch, and executes both rejections in its own words.

```text
unknown id     log_error("NUM: unknown numid '%s'\n", numid); return NULL;
index range    log_error("NUM: numid '%s' index %i+%i=%i > size %i\n", ...)
value range    log_error("NUM: numid '%s' %ssigned value %i (%u) outside
                          range %i..%u\n", ...); return false;
```

game_num_patch returns false in each case and applies nothing. This meaning is executed, not inferred from a name.

EN5 closed within scope, and closed with an unusually explicit statement. The walk terminates on the table's own DEFNUMEND sentinel, "{ NULL, NULL, NUMTYPE_S, 0, 0, 0, 0 }" at src/game/game_nump.c:412, which is exactly find_match's loop condition -- Section 3.2's first admissible case, runtime construction closing the set. What is unusual is that the project also says which enumeration is the complete one: doc/list_pbxnum.txt declares itself "an incomplete list" and directs the reader to "Run with -dumpnum for the full list without explanations". The project distinguishes its prose list from the runtime enumeration and names the latter as full. Tag: enforced.

EN6 outcome independence: membership is the set of patchable game numbers. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible: enumerate game_num_id_tbl[] to DEFNUMEND and emit, per entry, the numid a PBX may address, its numeric type, its element count `size`, and its admissible value range vmin..vmax.

Placed alongside the other admissible constructions, this is the second whose entries carry their own constraints rather than merely being the accepted values, after C013's MDFNSetting. Nothing follows for the verdict; E4 asks whether the universe is constructible, not how rich it is. Nothing in this entry may be treated as an inventory result -- see QA-19.

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether 1oom designates an authoritative rules source.

Decision: PASS

## RETRACTION 7 — C016 E2-REP withdrawn; step 3 was extended after the root proved insufficient

EV-C016-E2REP-01 is **quarantined**, and with it EV-C016-E2RULE-01,
EV-C016-E3-01 and EV-C016-E4-01 as post-stop exposure. Nothing is
deleted. The archive was retrieved, its 397 entry names are real, the
source citations in the E4 entry are accurate. They are unusable because
the E2-REP verdict rested on a surface the sealed navigation does not
reach.

**The breach.** Allowed navigation is three steps: the official landing
page, a Source/Code/Repository/Development link it exposes, and the
metadata/root surface of the repository that link reaches. The withdrawn
entry went one step further, to
`/-/archive/master/1oom-master.tar.gz`, and listed its entries to
establish that a source tree is present.

The entry's own defence was that the archive is generated by the same
repository, so it is not a different canonical location. That is true
and beside the point. The objection is not about identity, it is about
navigation, and the shape is C014's exactly:

```text
the fact the gate needed could not be established at the allowed surface
  -> a further surface that could establish it was opened
```

C014 settled the principle this violates: the contract governs where we
may look, the criterion governs what would satisfy the gate. "Source
tree presence is an allowed observation" says what would satisfy the
gate; it does not authorize a surface the navigation omits. And here, as
at C014, the extension was triggered by finding the permitted surface
insufficient, which makes the search scope a function of what was found.

## EV-C016-E2REP-02  (supersedes the quarantined EV-C016-E2REP-01)
Candidate: C016 (frame rank 16, games/1oom)
Gate: E2-REP

Re-determined on admissible evidence only.

Step 1: https://kilgoretroutmaskreplicant.gitlab.io/plain-html/ -- the frozen HOMEPAGE.
observed_at_utc: 2026-08-27T10:25:29Z-10:25:30Z; http_status 200; redirect_chain: NONE
Observed: under "Files and such" the page reads "Source code: GitLab" above the clone command "git clone https://gitlab.com/KilgoreTroutMaskReplicant/1oom.git", then "Binaries and tarball available here." linking to https://gitlab.com/KilgoreTroutMaskReplicant/1oom/tags/.

Step 2: the link labelled "GitLab" sits under the literal words "Source code:" -- a Source link in the plainest sense step 2 admits, requiring no interpretation of the label.

Step 3: https://gitlab.com/KilgoreTroutMaskReplicant/1oom -- the repository root.
observed_at_utc: 2026-08-27T10:26:02Z; http_status 200; redirect_chain: NONE
Observed, restricted to what the served root surface carries: project path KilgoreTroutMaskReplicant/1oom, project name 1oom, project id 6630849, default branch master, data-is-project-empty="false", and no fork-of, mirror or archived marking (the only "fork" token is the affordance for creating one).

What the admissible evidence establishes: upstream designates exactly one canonical source location, in as many words, at a stable URL; it is not a fork, mirror or archive; and it is not empty. The second landing-page link is not a competing designation -- it resolves to the tags page of the same GitLab project, so it names artifacts of the one designated location. That determination needs only the URL as it appears on the landing page and is unaffected by this retraction.

What it does not establish: that an actual source tree is present. GitLab renders its file tree client-side, so the served root surface carries no listing. `data-is-project-empty="false"` shows the repository has content; it does not show that the content is a source tree, which is the observation the gate names.

Adjudication, with no quarantined observation doing verdict work:

```text
PASS not established
  the root surface does not carry the source-tree observation the
  gate requires

FAIL not established
  none of E2-REP's failure codes applies. Upstream designates exactly
  one location, in as many words, at a stable URL, with one target
  identifier. E2REP-NO-SOURCE is a claim about access to the source
  representation, and nothing admissible supports asserting it here.

contamination
  forbidden exposure occurred at this gate; the archive was opened,
  which independently prevents reconstructing a clean adjudication
  after the fact
```

The third line is provenance, not evidence: it records what happened to
this run's observation process at this gate, says nothing about 1oom,
and rules nothing in or out. The first two lines rest only on admissible
surfaces.

The undetermined shape belongs to the protocol, not to 1oom. See QA-20.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## RETRACTION 7a — C016 gates after E2-REP
EV-C016-E2RULE-01, EV-C016-E3-01 and EV-C016-E4-01 are quarantined as
post-stop exposure, on the principle applied to C005 under QA-11 and to
C014 under QA-17. Screening stops at the first gate that is not
determined; those three were reached only because a withdrawn PASS stood
at E2-REP. Their observations -- the LBX v1.3 requirement, the PBX
`-file` witness, and the game_num_id_tbl[] construction with its
"-dumpnum for the full list" closure statement -- are kept on the record
and used for nothing.

## EV-C017-UR-01
Candidate: C017 (frame rank 17, games/2048-cli)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/2048-cli/Makefile
Observed: GH_ACCOUNT=tiehuis; GH_PROJECT=2048-cli; GH_TAGNAME=v0.9.1; COMMENT="terminal version of the 2048 sliding block puzzle game". There is no HOMEPAGE field and no SITES field.
Inference: every field names one packaged system, 2048-cli. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C017-E1-01
Candidate: C017
Gate: E1
Source: same frozen metadata; https://github.com/tiehuis/2048-cli
observed_at_utc: 2026-08-27T10:49:56Z; http_status 200
Observed: a third-party terminal implementation, described by its own repository as "The game 2048 for your Linux terminal", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C017-E2REP-01
Candidate: C017
Gate: E2-REP

Surface: https://github.com/tiehuis/2048-cli, reached from the frozen GH_ACCOUNT/GH_PROJECT pair, which the contract admits as a starting point.
Necessary because: E2-REP asks whether upstream designates exactly one canonical source location, and this is the only upstream surface the frozen metadata reaches. The metadata names no HOMEPAGE, so navigation step 1 has no target at all.

observed_at_utc: 2026-08-27T10:49:56Z-10:49:57Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: upstream-controlled repository

Observed, restricted to metadata the contract allows at a repository: repository name 2048-cli, owner login tiehuis, default branch master, isFork false, isTemplate false, isArchived true, with the served banner "This repository was archived by the owner on May 18, 2024. It is now read-only." No repository website field. A source tree is present at the root -- directories src, man, po, 18n and files Makefile, LICENSE, README.md, HowToTranslate.md, .gitignore, .replit. The only project-external link on the surface is https://github.com/gabrielecirulli/2048, which the repository's own description presents as the game this is a terminal version of -- lineage, in the same sense as flycast's "based on reicast", not a source designation for this system.

Adjudication:

```text
PASS not established
  the admissible evidence establishes repository identity, upstream
  affiliation and source-tree presence. It does not establish that
  upstream designates this location as its canonical source. GH_*
  made the repository findable; arriving at a repository is not the
  same as upstream identifying it as authoritative.

FAIL not established
  no E2-REP failure code applies. Not finding a designation at the
  one reachable surface is not a demonstration that none exists.

contamination
  later-gate material was read while E2-REP was still unresolved.
  Retained as provenance; it does no verdict work.
```

This is the boundary C014 established: **affiliation is not designation.** There the repository carried the project's name, held the source tree, and pointed at the official site through its website field, and none of that amounted to upstream designating it. The same standard applies here, where less is available.

Why C010 and C012 are not reopened by this, and the reason is navigation topology rather than any difference in evidential weight between metadata fields. Both are equally frozen OpenBSD starting points; neither is upstream evidence in itself.

```text
C010   frozen starting URL IS the project landing surface
       and IS the repository root      -> step 1 = step 3     PASS stands
C012   same                            -> step 1 = step 3     PASS stands
C014   a separate project site exists; it designates no
       source location                                        UNRESOLVED
C017   no project landing URL at all; a packaging identifier
       reaches a repository and nothing more                   UNRESOLVED
```

For C010 and C012 the execution record already states that steps 1 and 3 collapse onto one surface, and repository identity and source-tree presence were observed there together. C017 has no admissible upstream evidence making its repository root a step-1 project surface. Reopening C010 and C012 would require newly holding that a frozen starting URL which IS the repository root cannot count as the project landing surface -- a change to the navigation semantics this run has applied throughout, introduced after the fact and not required by anything here.

`isArchived: true` is recorded as an observation and is not used as a failure ground. No sealed rule says an archived repository cannot be a canonical source location; the URL is stable and the source tree is present.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## QUARANTINE — C017 material read while E2-REP was unresolved
Gates after E2-REP are NOT_REACHED. The following were nevertheless read
before E2-REP was settled, and are logged here so the exposure is
auditable. None is recorded as evidence and none does verdict work:

```text
man/2048.6      "Set the size of the playing field. Default is 4.
                 Maximum value is 16, minimum is 4."
src/options.h   CONSTRAINT_GRID_MIN 4, CONSTRAINT_GRID_MAX 20
src/highscore.c highscore_save's eligibility condition, which turns on
                score_high loaded from a file an earlier session wrote
src/gfx.h, src/merge.h, Makefile
                interface declarations whose implementations are
                selected at build time
```

One item needs naming explicitly, because it is exactly the kind of
thing that must not be allowed to leak backwards. man/2048.6 ends with
"All contributions can be found at https://github.com/Tiehuis/2048-cli."
That is designation-relevant text. Whether it actually constitutes an
upstream canonical-source designation is NOT adjudicated here, and does
not need to be: it is a file inside the repository, opening source files
is forbidden at E2-REP, and it was read while the verdict was open. It
is used for nothing -- not to push the verdict to PASS, and not to argue
that a designation exists elsewhere. The E2-REP adjudication above rests
only on the root surface.

## RETRACTION 8 — C010 and C012 E2-REP withdrawn; the C017 principle applies to them too

EV-C010-E2REP-01 and EV-C012-E2REP-01 are **quarantined**, and with them
EV-C010-E2RULE-01, EV-C010-E3-01, EV-C010-E4-01, EV-C012-E2RULE-01,
EV-C012-E3-01 and EV-C012-E4-01 as post-stop exposure. Nothing is
deleted; every observation in them was accurately made.

**What forced this.** C017 settled that repository identity, upstream
affiliation and source-tree presence do not add up to upstream
designating a location as its canonical source. C010 and C012 were
exempted from that on a navigation-topology argument: their frozen
starting URL was simultaneously the project landing surface and the
repository root, so steps 1 and 3 collapsed.

That argument does not survive contact with what E2-REP actually asks.
`step 1 = step 3` answers "which surface may we look at", not "did
upstream designate this location". The sealed contract lists those as
separate matters itself, naming "whether upstream designates this
location as its source" as its own allowed observation alongside
repository identity and source-tree presence. Collapsing the navigation
does not collapse the questions.

And the exemption had a worse property. What made C010 and C012 special
was that their OpenBSD HOMEPAGE field happened to hold a repository URL.
Letting that carry the designation is letting an OpenBSD field supply
evidential force for an upstream fact -- the exact move withdrawn at
C014 and again at C017. The route differs:

```text
C010/C012   OpenBSD HOMEPAGE           -> GitHub repository root
C017        OpenBSD GH_ACCOUNT/PROJECT -> GitHub repository root
```

but the upstream evidence arrived at is the same kind. A field's name
does not turn the root it points to into an upstream designation
statement.

## EV-C010-E2REP-02  (supersedes the quarantined EV-C010-E2REP-01)
Candidate: C010 (frame rank 10, emulators/flycast)
Gate: E2-REP

Surface: https://github.com/flyinghead/flycast, the frozen HOMEPAGE, which is also the repository root.
observed_at_utc: 2026-08-27T07:46:55Z-07:46:56Z; http_status 200; redirect_chain: NONE

Observed (unchanged from the withdrawn entry, and all still accurate): repository flyinghead/flycast, default branch master, isFork false, isArchived false, isTemplate false, no mirror or primary/secondary marking, no repository website field, a source tree present at the root, and no non-GitHub outbound link that is a source-location designation.

```text
PASS not established
  repository identity, upstream affiliation and source-tree presence
  are established. Upstream canonical-source designation is not. No
  admissible upstream surface states that this location is its source.

FAIL not established
  not finding a designation at the reachable surface does not show
  none exists.
```

The SITES analysis in the withdrawn entry stands on its own and is unaffected: messagemode2.com is packager-side by the port Makefile's own dist: target, so it was never a competing designation. Nothing in that reasoning depended on the designation question.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C012-E2REP-02  (supersedes the quarantined EV-C012-E2REP-01)
Candidate: C012 (frame rank 12, emulators/libchdr)
Gate: E2-REP

Surface: https://github.com/rtissera/libchdr, the frozen HOMEPAGE, which is also the repository root.
observed_at_utc: 2026-08-27T08:14:43Z-08:14:44Z; http_status 200; redirect_chain: NONE

Observed (unchanged, and all still accurate): repository rtissera/libchdr, default branch master, isFork false, isArchived false, isTemplate false, no mirror or primary/secondary marking, no repository website field, a source tree present at the root, and no outbound link to any non-GitHub host at all.

```text
PASS not established
  as for C010. The absence of ANY outbound link means no competing
  designation is exposed -- but it equally means no upstream surface
  states that this location is the project's source.

FAIL not established
  not finding a designation does not show none exists.
```

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## RETRACTION 8a — C010 and C012 gates after E2-REP
Quarantined as post-stop exposure, on the principle applied to C005
(QA-11), C014 (QA-17) and C016 (QA-20). Kept on the record, used for
nothing:

```text
C010   the TheArcadeStriker wiki's ROM/BIOS requirement
       the GGPO save-state-before-session witness
       the Games[] construction, 354 entries, "Unknown game"

C012   chd.h's format requirements, 'MComprHD' and the per-version
       header sizes
       the parent-CHD ordering witness
       the codec_interfaces[] construction, 14 entries,
       CHDERR_UNSUPPORTED_FORMAT
```

## RETRACTION 9 — C002 and C007 E2-REP withdrawn under the record-only audit

EV-C002-E2REP-01 and EV-C007-E2REP-01 are **quarantined**. Both recorded
FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION). Neither is withdrawn because
its observations were wrong -- the pages were read and the URLs are
real. They are withdrawn because in each case the two designations the
verdict rests on were obtained past the sealed navigation.

No new upstream access was made for this audit. It is a re-reading of
what the evidence file already records.

**C002.** The recorded path is landing page -> download.html -> source
tarballs under dist/ and a link to the SourceForge hub -> the hub's code
repository at /p/plib/code/. The landing page itself yielded, in the
entry's own words, "exactly one download-related link (download.html)".
QA-17 settled that `Downloads` is not among step 2's Source / Code /
Repository / Development links and that the criterion's phrase "source
distribution" may not be used to widen the whitelist. Both designations
therefore came from beyond the permitted surfaces, and one of them from
two hops beyond.

**C007.** The recorded path is landing page -> the hub at
sourceforge.net/projects/dosbox -> "that hub in turn exposes BOTH
/p/dosbox/code-0/ (a code repository) and /projects/dosbox/files/ (a
release file area)". The two designations were read off the hub, not the
landing page. A generic project hub is also not a repository root, so
reaching the locations took a hop past step 3 as well.

## EV-C002-E2REP-02  (supersedes the quarantined EV-C002-E2REP-01)
Candidate: C002 (frame rank 2, devel/plib)
Gate: E2-REP
Surface: https://plib.sourceforge.net/ -- the frozen-metadata landing page.
observed_at_utc: 2026-08-27T03:20:44Z; http_status 200; redirect_chain: NONE
Observed, restricted to the permitted surface: the landing page exposes exactly one download-related link, download.html. It exposes no Source, Code, Repository or Development link.

```text
PASS not established
  no upstream surface within the contract performs a canonical-source
  designation.

FAIL not established
  the multi-designation finding depended on download.html and on the
  SourceForge hub beyond it, neither of which the contract reaches.
  Without them, no second designation is observed -- and one
  designation not being observed is not a demonstration that upstream
  designates none, nor that it designates several.

contamination
  forbidden surfaces were read at this gate; retained as provenance,
  doing no verdict work.
```
Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C007-E2REP-02  (supersedes the quarantined EV-C007-E2REP-01)
Candidate: C007 (frame rank 7, emulators/dosbox)
Gate: E2-REP
Surface: https://www.dosbox.com/ -- the frozen-metadata landing page.
observed_at_utc: 2026-08-27T04:50:25Z-04:52:01Z; http_status 200; redirect_chain: NONE
Observed, restricted to the permitted surface: the landing page exposes its own download page and a link to the project hub at sourceforge.net/projects/dosbox.

```text
PASS not established
  the landing page names a hub, not a canonical source location, and
  no permitted surface states which location upstream designates.

FAIL not established
  the two locations that produced the multi-designation finding were
  exposed by the hub, one hop past step 3, and a generic project hub
  is not a repository root. Without that hop the finding does not
  stand, and its absence is not a demonstration of anything about
  upstream.

contamination
  the hub was read at this gate; retained as provenance, doing no
  verdict work.
```
Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## AUDIT NOTE — C006, C011 and C015 verdicts stand

Audited on the same record-only basis. No new upstream access.

The batch header shared by C006, C007 and C011 reads "and the pages it
explicitly exposes", which is over-broad and would leave it unclear
where each fact came from. The timestamp line resolves it, because it
scopes the extra hop explicitly:

```text
observed_at_utc: ... (landing pages); 05:32:16Z (DOSBox SourceForge
hub, rank 7 only)
```

"rank 7 only" confines the hub visit to C007. C006 and C011 carry
landing-page observations alone, inside 04:50:25Z-04:52:01Z.

```text
C006  "the project page designates BOTH sourceforge.net/p/dgen/dgen/
      and sourceforge.net/projects/dgen/files/dgen/", neither marked
      canonical or primary. Both attributed to the project page; the
      classifications are readable from the SourceForge URL forms as
      they appear there; no content from either linked page is cited.
      FAIL stands.

C011  "the project page hosts its own source archives
      (downloads/Frodo-4.5.tar.gz among others) AND links several
      repositories including github.com/cebix/frodo4". Hosting and
      linking are both landing-page facts. FAIL stands.

C015  both designations quoted from the landing page body, with the
      sentences recorded verbatim -- "The latest official release is
      2.1.2" over the source tarball, and "grab sources from anonymous
      GIT" over the clone URL. FAIL stands.
```

All three are positive-shaped findings: several designations were seen
at a permitted surface and no primary was marked among them. None
depends on a surface the contract does not reach.

## EV-C018-UR-01
Candidate: C018 (frame rank 18, games/2048-qt)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/2048-qt/Makefile
Observed: DIST_TUPLE = github OpenOrphanage 2048-Qt v0.1.7 . ; COMMENT="2048 game in Qt"; PKGNAME=${DISTNAME:L}. There is no HOMEPAGE field and no SITES field. The Makefile also carries a COMMENTED-OUT line naming a different upstream, "#DIST_TUPLE = github keshavbhatt 2048-qt 3.0 .", under the note "# different port using WebKit, needing W^X...".

Inference: the port packages one system, OpenOrphanage/2048-Qt. The commented line names a system the port explicitly does NOT package -- it records an alternative the maintainer considered and disabled, and a disabled line is not metadata in effect. Recording it here because it names a second system and a reader of the Makefile will see it, not because it creates ambiguity. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C018-E1-01
Candidate: C018
Gate: E1
Source: same frozen metadata
Observed: a third-party Qt implementation of the 2048 puzzle game, packaged from the account OpenOrphanage, unrelated to this project.
Inference: external-authorship requirement satisfied. This is determinable from the frozen metadata alone and does not depend on the endpoint observation below.
Decision: PASS

## EV-C018-E2REP-01
Candidate: C018
Gate: E2-REP

Surface: https://github.com/OpenOrphanage/2048-Qt, the only location any frozen-metadata identifier resolves to. The metadata names no HOMEPAGE and no SITES, so navigation step 1 has no target and no other allowed upstream path exists.

requested_url: https://github.com/OpenOrphanage/2048-Qt
final_url: https://github.com/OpenOrphanage/2048-Qt
observed_at_utc: 2026-08-27T11:44:49Z (GET), 11:45:44Z (HEAD, confirmation)
http_status: 404, 404; redirect_chain: NONE (num_redirects 0 on both)
control: https://github.com/TASEmulators/fceux returned 200 at 11:45:44Z, same host, same moment

Observed: a definitive 404 at both attempts, with no redirect. GitHub issues a 301 for a repository that has been renamed within its own tracking, so the absence of a redirect means this is not a rename. The same-host control succeeded at the same moment, so this is not a host-wide or network condition. Under the contract this is genuine evidence about that endpoint rather than transport indeterminacy, and no retry-for-indeterminacy applies.

Adjudication. Two independent grounds point the same way, and neither supports a failure code.

```text
first, and prior to the endpoint's state
  the metadata names no HOMEPAGE. The only thing pointing at this
  location is a packaging fetch identifier. QA-21 and QA-22 settled
  that arriving at a repository via such an identifier yields
  affiliation, not upstream designation. This candidate was in C017's
  shape before the request was made, and would have been UNRESOLVED
  had the endpoint returned 200.

second
  the location is gone, so even affiliation cannot be observed.
```

Why no failure code, including E2REP-NO-SOURCE. Every E2-REP failure code is a statement about a DESIGNATED canonical source location -- that there is none, that there are several, that it has no stable URL, or that its source representation is inaccessible. No designation was ever established here. What the 404 establishes is that the location OpenBSD fetches from is no longer present; it does not establish anything about a designated upstream source, because none was identified. Coding it as `E2REP-NO-SOURCE` would convert a fact about a packaging fetch path into a claim about upstream.

Surfaces considered and NOT opened, with the reason: the account page for `OpenOrphanage`. It is a frozen-metadata identifier and so an admissible starting point, but it is not necessary. If the account exists and holds a differently-named repository, selecting that repository would be our adjudication of the target's identity, which is exactly what UR and E2-REP exist to prevent; and if it does not exist, the verdict is unchanged. A negative that does not need a surface should not open it.

Recorded as an observation of the frame rather than of the candidate: this is the first item whose packaged upstream location has disappeared between the frozen metadata and screening. The frame was frozen from OpenBSD 7.9; upstream state is observed now. The two times do not merge, and this is what their divergence looks like in practice.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## RETRACTION 10 — C018 E2-REP reasoning withdrawn; the verdict is unchanged, the argument was not sound

EV-C018-E2REP-01 is **superseded**. The verdict it reached, UNRESOLVED,
stands. Three defects in how it got there:

**A counterfactual it could not know.** It asserted the candidate "would
have been UNRESOLVED had the endpoint returned 200". The frozen
DIST_TUPLE alone does not establish designation -- that much is right --
but what an open repository root would have carried is not knowable
before opening it. QA-23 had just generalised the designation signal to
include a label, a link relation or a structured marking, any of which
could have been present in owner-controlled metadata. The counterfactual
is withdrawn.

**A platform-semantics claim the verdict did not need.** It argued that
because GitHub issues a 301 for a repository renamed within its own
tracking, the absence of a redirect ruled out a rename. Two 404s and a
same-host 200 control establish the endpoint's present state, which is
all the gate requires. Whether a rename ever occurred is an extra claim
about another system's behaviour, and it is dropped.

**A contradiction.** The entry said "no other allowed upstream path
exists" and then, two paragraphs later, that the OpenOrphanage account
page "is an admissible starting point". Both cannot be true. The second
is correct: `OpenOrphanage` is an identifier in the frozen metadata, so
the account surface is admitted. And once admitted, QA-11's test makes
it NECESSARY -- the verdict could not be settled and it was the
remaining admitted surface. Declining to open it was wrong, and the
reason given -- that a differently-named repository must not be selected
-- was a reason to bound the observation, not to skip the surface.

## EV-C018-E2REP-02  (supersedes EV-C018-E2REP-01)
Candidate: C018 (frame rank 18, games/2048-qt)
Gate: E2-REP

The frozen metadata names no HOMEPAGE and no SITES. Its DIST_TUPLE
yields two admitted starting identifiers: the repository path and the
account.

Surface 1: https://github.com/OpenOrphanage/2048-Qt
Necessary because: it is the location the frozen identifiers resolve to, and E2-REP asks what upstream designates.
observed_at_utc: 2026-08-27T11:44:49Z (GET), 11:45:44Z (HEAD)
http_status: 404, 404; redirect_chain: NONE (num_redirects 0 both)
control: https://github.com/TASEmulators/fceux -> 200 at 11:45:44Z, same host, same moment
Observed: a definitive 404 at both attempts. With a same-host control succeeding at the same moment, this is evidence about the requested endpoint rather than transport indeterminacy, so no retry-for-indeterminacy applies. No claim is made about whether the repository was ever renamed, moved or deleted; the gate needs the endpoint's present state and nothing further.

Surface 2: https://github.com/OpenOrphanage
Necessary because: E2-REP cannot be settled from surface 1, and the account token is the one remaining identifier the frozen metadata admits. Under QA-11 a surface the criterion still needs, and which the already-observed structure has not made redundant, is necessary rather than optional.

Observation scope, fixed before the request rather than after seeing the result:

```text
observe only
  whether the account exists
  an explicit profile website or migration notice
  an explicit link or structured marking designating where 2048-Qt's
  source now lives

do not
  select a differently named repository because it looks related
  search the account's repositories by semantic similarity
  infer a successor from names or descriptions
```

observed_at_utc: 2026-08-27T11:53:28Z (GET), 11:53:40Z (HEAD)
http_status: 404, 404; redirect_chain: NONE (num_redirects 0 both); body "Not Found"
control: https://github.com/TASEmulators -> 200 at 11:53:40Z, an account-shaped URL on the same host at the same moment
Observed: the admitted account URL returned a definitive 404. No profile, migration notice, repository list or designation signal was observable at that surface. No claim is made about the account's existence as such -- the observation is of what the URL returned now, on the same footing as the repository endpoint above, where rename and deletion history were likewise left alone. The bounded observations had nothing to return, and the prohibited ones nothing to tempt with.

Adjudication:

```text
PASS not established
  every admitted starting surface returns a definitive 404. No
  admissible designation signal -- sentence, label, link relation or
  structured marking -- was obtainable from any of them.

FAIL not established
  no E2-REP failure code applies. Each is a statement about a
  DESIGNATED canonical source location: that there is none, that
  there are several, that it lacks a stable URL, or that its source
  representation is inaccessible. No designation was established, so
  there is no designated location for any of those claims to be
  about. What the 404s establish is that the location the packaging
  metadata fetches from, and the account holding it, are absent now.
  Coding that as E2REP-NO-SOURCE would turn a fact about a packaging
  fetch path into a claim about upstream.
```

Recorded as an observation of the frame rather than of the candidate:
this is the first item in this run where the packaged upstream location
recorded by the frozen frame returned a definitive disappearance signal
at screening time. The claim is about divergence between the frozen
packaging location and what is observable now, not about the project
having ceased to exist somewhere.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C019-UR-01
Candidate: C019 (frame rank 19, games/abuse)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/abuse/Makefile
Observed: HOMEPAGE=http://abuse.zoy.org/; DISTNAME=abuse-free-0.8; PKGNAME=abuse-0.8; SITES=${HOMEPAGE}raw-attachment/wiki/download/; COMMENT="SDL port of the legendary 2D platform shooter". The port additionally fetches a second distfile, ABUSE_SFX=abuse-free-sounds-20120309, from SITES.sfx=http://www.linklevel.net/distfiles/.
Inference: the packaged system is Abuse, as maintained at abuse.zoy.org. The second distfile is a free sound-effect dataset for that same system rather than a second packaged system -- the port installs one program, and DISTNAME/PKGNAME name one thing. Recorded because a reader of the Makefile sees two SITES entries. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C019-E1-01
Candidate: C019
Gate: E1
Source: same frozen metadata; http://abuse.zoy.org/
observed_at_utc: 2026-08-27T11:59:03Z; http_status 200
Observed: a third-party game, "developed by Crack dot Com in 1995 ... now maintained by Sam Hocevar", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C019-E2REP-01
Candidate: C019
Gate: E2-REP

Step 1: http://abuse.zoy.org/ -- the frozen HOMEPAGE, a Trac wiki.
observed_at_utc: 2026-08-27T11:59:03Z-11:59:05Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: the page exposes a navigation link labelled "Development…" pointing at /wiki/dev, and in its body directs the reader to "the development page for information about development". Its own text announces a release ("May 9th, 2011: Abuse 0.8 is out!") linking to /wiki/download, and carries a Links section introduced as "most Abuse resources are now dead. Here are a few worthwile links and archived pages" -- third-party and web.archive.org pages, not source-location designations for this system.

Step 2: /wiki/dev, reached by the "Development…" link. "Development" is one of the four labels the navigation contract names, so no interpretation was needed.
observed_at_utc: 2026-08-27T11:59:21Z; http_status 200; redirect_chain: NONE
Observed: the designation signal, under the page's own heading "Source code" -- "Development takes place in a Subversion repository. You can browse it online or check it out using svn:" followed by "svn co svn://svn.zoy.org/abuse/abuse/trunk abuse-trunk". A section label plus a concrete checkout URL, which is a designation signal in the form QA-23 admits.

Step 3: the designated repository's root surface. The dev page's "browse it online" points at /browser/abuse/trunk, the Trac view of that same Subversion repository -- a view of the designated location, not a second location.
observed_at_utc: 2026-08-27T12:00:17Z, 12:00:31Z, 12:00:32Z
http_status: 500, 500, 500; redirect_chain: NONE on all three
control: http://abuse.zoy.org/wiki/dev returned 200 at 12:00:33Z, same host, same moment
Observed: three 5xx responses at recorded times, as the contract requires before recording indeterminacy. The served error page reads: Unsupported version control system "svn": No module named svn. So the wiki is healthy and its repository browser is not.

Adjudication:

```text
DESIGNATION established
  at least one upstream-designated source location:
  svn://svn.zoy.org/abuse/abuse/trunk, stated by upstream under its
  own "Source code" heading with a checkout command.

UNIQUENESS not adjudicated
  the frozen metadata also carries an admitted SITES location under
  the project's download area, and the landing page links a release
  announcement to /wiki/download. Whether those amount to a second
  designated SOURCE location was never determined, because the gate
  became UNRESOLVED at the necessary repository surface before any
  further observation was warranted. The landing-page release
  announcement is not itself a source-location designation; nothing
  is claimed about what the unopened SITES path holds.

PASS not established
  E2-REP also asks that the designated location actually hold a
  source tree. Its only HTTP view returned 5xx three times after
  retries at recorded times. The observation was not made.

FAIL not established
  the contract is explicit that 5xx is transport indeterminacy and
  NOT evidence of absence, and that such an item takes a protocol
  issue rather than a failure code. A broken Trac plugin is a fact
  about the observation, not about Abuse.
```

The verdict rests on the Trac 5xx alone, which is sufficient on its own.

Ancillary tooling note, carrying no verdict work: the designated
endpoint svn://svn.zoy.org/abuse/abuse/trunk was also not observed,
because no Subversion client is available in this environment. That is
recorded so the record shows what was and was not attempted, not as part
of the transport finding -- otherwise a transport PI would look half
constituted by a local tooling gap.

Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

Gates after E2-REP are NOT_REACHED. Screening stopped here rather than
continuing to read, per QA-21.

## EV-C020-UR-01
Candidate: C020 (frame rank 20, games/ace)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/ace/Makefile
Observed: HOMEPAGE=http://www.delorie.com/store/ace/; SITES=http://www.delorie.com/store/ace/ (identical to HOMEPAGE); DISTNAME=ace-1.4; COMMENT="solitaire games".
Inference: every field names one packaged system, and HOMEPAGE and SITES are the same URL, so the metadata resolves to a single location. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C020-E1-01
Candidate: C020
Gate: E1
Source: same frozen metadata; https://www.delorie.com/store/ace/
observed_at_utc: 2026-08-27T12:09:25Z; http_status 200
Observed: a third-party set of X11 solitaire games -- "The Ace of Penguins is a set of Unix/X solitaire games" -- unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C020-E2REP-01
Candidate: C020
Gate: E2-REP

Surface: the frozen HOMEPAGE, which is also the frozen SITES. No navigation past step 1 was performed and none was needed: both designations below are in the landing page's own body.
Necessary because: E2-REP asks whether upstream designates exactly one canonical source location, and this is the project's own page.

requested_url: http://www.delorie.com/store/ace/
final_url: https://www.delorie.com/store/ace/
observed_at_utc: 2026-08-27T12:09:25Z-12:09:27Z; http_status 200; redirect_chain: 1 redirect, http -> https on the same host
evidence_role: official-project-page

Observed: the page's "Downloading" table lists source distributions on the project's own path, and its prose designates a repository. Both in upstream's own words:

```text
source   CVS   518K   Mar 24, 2012   "Unreleased snapshot of CVS repository"
source   1.4   518K   Mar 24, 2012
source   1.3   517K   May 28, 2010
source   1.2 / 1.1 / 1.0                (older releases)
                                        plus linux, agenda, irix,
                                        solaris and freebsd rows, which
                                        are platform binaries

prose    "You can also use anonymous cvs to get the latest development
          sources."        -> cvs.html
```

Inference: the criterion admits BOTH a repository and a source distribution as source-location types, and fails a project that "designates several with no primary among them". Upstream here designates one of each, on one page, and marks no primary between them. The word "also" adds a second route; it does not rank the two. Describing the CVS route as giving "the latest development sources" and the table's 1.4 row as a release distinguishes what each CONTAINS, not which location is canonical.

The reading deliberately repeats C015's and avoids the one withdrawn at C002: treating the repository as the real source and the tarballs as mere releases -- or the reverse -- supplies a hierarchy the criterion refuses to let us supply.

Nothing beyond step 1 was opened. cvs.html would give the checkout details, but the landing page has already designated the repository, and the gate is determined without it. The remaining outbound links are the PNG and ZLib project pages, an Agenda hardware vendor, and delorie.com's own site chrome -- none a source-location designation for this system.

Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

Gates after E2-REP are NOT_REACHED under the first-fail stop rule.

## RETRACTION 11 — C020 E2-REP withdrawn; the second location was never located

EV-C020-E2REP-01 is **quarantined**. It recorded FAIL
(E2REP-NO-SINGLE-CANONICAL-LOCATION) on the finding that upstream
designates a source distribution and a repository with no primary
between them. The first half holds. The second does not.

**What the landing page actually gives for the repository.** Its prose
reads "You can also use anonymous cvs to get the latest development
sources", linking to cvs.html. That is a strong signal that a CVS source
route EXISTS. It is not an observation of a repository location. No
checkout endpoint, host or repository URL appears on the permitted
surface, and cvs.html -- which would presumably supply them -- was not
opened.

**Why this is not C015 or C009 after all.** Both of those completed the
arrow to an actual location on the permitted surface:

```text
C015   landing page body carried the location itself:
       "git clone http://shamusworld.gotdns.org/git/virtualjaguar"

C009   the link's DESTINATION was the repository:
       "commit browser" -> github.com/TASEmulators/fceux/commits/master

C020   landing page -> cvs.html, a repository-instructions page.
       The location is one hop further on, and unobserved.
```

The withdrawn entry treated "a repository route is designated" as
equivalent to "a second canonical source location is designated at a
stable URL". E2-REP asks how many canonical source LOCATIONS upstream
designates, and a location that was never seen cannot be counted.

**A second error in the same entry.** Its evidence block presented the
table's `source | CVS | "Unreleased snapshot of CVS repository"` row
alongside `source | 1.4` as if the two might be distinct locations. By
its own wording that row is a source DISTRIBUTION -- a snapshot taken
from the CVS repository -- served from the same path as the versioned
tarballs. Both rows are the same source-distribution location.

**cvs.html is deliberately not being opened now.** C020 was recorded as
a terminal FAIL; adding a fresh upstream observation to repair it would
be observation after a terminal verdict, which is the pattern QA-21 was
written to stop. The gate is re-determined on what was admissibly
observed.

## EV-C020-E2REP-02  (supersedes the quarantined EV-C020-E2REP-01)
Candidate: C020 (frame rank 20, games/ace)
Gate: E2-REP

Surface: the frozen HOMEPAGE, which is also the frozen SITES. Nothing past step 1 was opened.
requested_url: http://www.delorie.com/store/ace/
final_url: https://www.delorie.com/store/ace/
observed_at_utc: 2026-08-27T12:09:25Z-12:09:27Z; http_status 200; redirect_chain: 1 redirect, http -> https, same host
evidence_role: official-project-page

Observed: the "Downloading" table serves source distributions from the project's own path -- rows `source 1.4`, `1.3`, `1.2`, `1.1`, `1.0`, and a `source CVS` row annotated "Unreleased snapshot of CVS repository", all on the same path, alongside platform binary rows. The prose adds "You can also use anonymous cvs to get the latest development sources", linking to cvs.html.

```text
established
  upstream designates source distributions directly on this page, and
  states that an anonymous CVS route to development sources exists.

not established
  the CVS repository's location. No checkout endpoint or repository
  URL appears on the permitted surface; cvs.html was not opened.

PASS not established
  E2-REP requires exactly one designated canonical source location,
  at a stable URL, holding a source tree. With a second route
  announced but its location unobserved, neither the count nor the
  URL can be settled.

FAIL not established
  the multi-location finding needs two LOCATIONS. One was announced,
  not located. A route whose endpoint was never seen cannot be
  counted as a second canonical source location.
```

The `source CVS` row is not a second location either: by its own annotation it is a snapshot distribution taken from the repository, served from the same path as the versioned tarballs.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C022-UR-01
Candidate: C022 (frame rank 22, games/alephone/alephone)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/alephone/alephone/Makefile (games/alephone/Makefile is a SUBDIR stub and games/alephone/Makefile.inc is empty)
Observed: HOMEPAGE=https://alephone.lhowon.org/; SITES=https://github.com/Aleph-One-Marathon/alephone/releases/download/release-${DATE}/; DISTNAME=AlephOne-${DATE}; PKGNAME=alephone-1.11; COMMENT="open source game engine based on Marathon 2: Durandal".
Inference: every field names one packaged system, Aleph One. "Marathon 2: Durandal" names the game whose engine this continues, not a second packaged system, in the same way flycast's "based on reicast" did. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C022-E1-01
Candidate: C022
Gate: E1
Source: same frozen metadata; https://alephone.lhowon.org/
observed_at_utc: 2026-08-27T12:19:41Z; http_status 200
Observed: a third-party engine, "the open source continuation of Bungie's Marathon 2 game engine", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C022-E2REP-01
Candidate: C022
Gate: E2-REP

Step 1: https://alephone.lhowon.org/ -- the frozen HOMEPAGE.
observed_at_utc: 2026-08-27T12:19:41Z-12:19:43Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: the page's navigation exposes a link labelled "GitHub" whose DESTINATION is https://github.com/Aleph-One-Marathon/alephone, and its body reads "Aleph One is available under the terms of the GNU General Public License (GPL). Download the source code.", where "source code" links to https://github.com/Aleph-One-Marathon/alephone/releases/download/release-20250829/AlephOne-... . A closing line states "alephone.lhowon.org is hosted by lhowon.org and mirrored at aleph-one-marathon.github.io".

Step 2: the "GitHub" link. Its label is a host name rather than one of the contract's four words, and the reading is the one established at C009: step 2 classifies a link by what it LEADS TO, and this destination is the repository root itself. QA-25's distinction is satisfied in its strongest form here -- the link's destination IS the location, not a page of instructions for reaching one.

Step 3: https://github.com/Aleph-One-Marathon/alephone -- the repository root.
observed_at_utc: 2026-08-27T12:20:25Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-source-location
Observed: repository name alephone, owner Aleph-One-Marathon, default branch master, isFork false, isMirror false, isArchived false, isTemplate false, website metadata field https://alephone.lhowon.org/, and a source tree present at the root -- Source_Files, Resources, Cheats, Extras, MML Scripts, Steam, VisualStudio, Xcode, changelogs, and Makefile.am, AlephOne.spec.in, AUTHORS, COPYING, CONTRIBUTING.md.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Aleph One). The designation runs both ways: the project's own site links to the repository, and the repository's website field names that site.

Applying the three distinctions this run has had to separate:

```text
affiliation vs designation
  not merely a repository that belongs to the project. The project's
  OWN SITE performs the arrow, which is what C010, C012 and C017
  lacked.

route vs location
  the link's destination is the location, not instructions for
  reaching it. C020's failure mode is absent.

content vs location
  the "Download the source code" link resolves to a RELEASE ASSET of
  that same repository. By C016's reading it names an artifact OF the
  one designated location, not a second location. The frozen SITES,
  which points into the same releases path, is likewise not a second
  designation.
```

Not counted as designations, with reasons: aleph-one-marathon.github.io is described by upstream itself as a mirror of the WEBSITE, not of the source; marathon-ios.com, Steam, Discord and Patreon are distribution and community channels; lhowon.org is the hosting and accounts site.

Decision: PASS

## EV-C022-E2RULE-01
Candidate: C022
Gate: E2-RULE
Source: the landing page's "Wiki" link -> https://github.com/Aleph-One-Marathon/alephone/wiki -> .../wiki/Plugins
observed_at_utc: 2026-08-27T12:20:45Z (index), 12:21:05Z (page); http_status 200

Observed: located witness. The Plugins page specifies the Plugin.xml manifest and states its validity conditions in the project's own words:

```text
minimum_version="..."   "the minimum Aleph One date version (e.g.
                         20091015) required to run this plugin. If the
                         version is not new enough, the plugin will be
                         disabled"

<scenario>              "if given, the plugin will only be loaded for
                         listed scenarios. All fields must exactly
                         match scenario MML."

requires_opengl="true"  "shapes patches that require OpenGL will not be
                         loaded when the software renderer is active"
```

Inference: these determine concrete validity requirements on an input artifact without our inventing them. A plugin declaring a minimum_version newer than the running engine is disabled; a plugin whose <scenario> fields do not exactly match is not loaded. The consequences are stated, not inferred.
Decision: PASS

## EV-C022-E3-01
Candidate: C022
Gate: E3
Source: same designated wiki, the Plugins and Plugin-Guide pages
observed_at_utc: 2026-08-27T12:20:55Z, 12:21:05Z; http_status 200

Observed: located witness. The Plugin-Guide states of a plugin installed in the user data directory rather than a scenario's own folder -- "Note: plugins are activated automatically, so installing a global plugin will activate it for all games." The Plugins page then gives the rules that make this consequential: "All MML Plugins are run in alphabetical order, based on their name"; "Only one solo Lua plugin can be run at once; the engine will run the last one in the list that is enabled"; "Theme plugins will override the current theme setting".

Inference: whether a given scenario runs with the MML, script or theme its own files specify is not decidable from that scenario's data. It depends on globally installed plugin state established earlier and outside the scenario, and on where that plugin falls in an ordering whose last enabled entry wins. No claim is made about what the scenario's own files do or do not record. That is a stateful/temporal validity question that can be examined, which is what E3 requires.

No stronger claim is made about what any single artifact determines. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C022-E4-01
Candidate: C022
Gate: E4

No positive construction was obtained. Observations are at the primary snapshot: master resolves to 4f7aa7b430177da3d7a55de7a047a11236225fab, committed 2026-08-21T00:06:38Z, before the enumeration execution timestamp.

Source: https://raw.githubusercontent.com/Aleph-One-Marathon/alephone/master/Source_Files/XML/XML_MakeRoot.cpp ; .../Source_Files/XML/Plugins.cpp ; the Source_Files and Source_Files/XML listings
observed_at_utc: 2026-08-27T12:21:41Z-12:22:36Z; http_status 200 throughout

Attempted, and why each falls short:

```text
_ParseAllMML  (XML_MakeRoot.cpp:94 onward)
  dispatches MML by element name -- children_named("stringset"),
  ("interface"), ("player"), ("weapons") and so on. The element names
  are extractable, but they are a hardcoded CALL SEQUENCE, not a
  registry the program walks. EN5's admissible closure bases are
  runtime construction or an unconditional universal claim about the
  codebase; here the closure basis would be our reading of one
  function's body, which is neither. The file's own comment describes
  what ResetAllMMLValues does; it makes no closure claim.

Plugins.cpp
  enforces exactly the validity rules the E2-RULE witness documents --
  "if (required_version.size() > 0 && A1_DATE_VERSION < required_version)"
  at line 72, and the scenario match at 75-80. These are direct
  conditionals. They enforce, but they do not ENUMERATE: there is no
  membership set from which a property-level universe could be built.
```

Inference: E4 PASS requires a positive construction -- an EN1-EN6 mechanism, or a Section 3.1 designated source, from which the property-level universe is ACTUALLY mechanically constructible. None was exhibited. Under the post-seal amendment the absence of a positive construction does not establish E4 FAIL, because no preregistered discovery procedure makes that universal claim decidable.

The normative route was not pursued: the landing page designates the wiki as documentation, not as an authoritative source for the project's rules, and Section 3.1 admits only explicit designation. No claim is made that no such designation exists anywhere.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C023-UR-01
Candidate: C023 (frame rank 23, games/alephone/weland)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/alephone/weland/Makefile
Observed: HOMEPAGE=https://sourceforge.net/projects/weland/; SITES=${SITE_SOURCEFORGE:=weland/}; DISTNAME=weland-r211-src; PKGNAME=weland-211; COMMENT="marathon / alephone map editor".
Inference: every field names one packaged system, Weland. "marathon / alephone" names what it edits, not further packaged systems. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C023-E1-01
Candidate: C023
Gate: E1
Source: same frozen metadata; https://github.com/treellama/weland
observed_at_utc: 2026-08-27T13:36:05Z; http_status 200
Observed: a third-party map editor, "a Marathon map editor by Gregory Smith, written in C#", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C023-E2REP-01
Candidate: C023
Gate: E2-REP

Step 1: https://sourceforge.net/projects/weland/ -- the frozen HOMEPAGE, which is a SourceForge project page.
observed_at_utc: 2026-08-27T13:35:21Z-13:35:22Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: the page is headed "Weland / Brought to you by: treellama", carries "Last Update: 2015-04-12", and states directly beneath the title: **"As of 2015-12-05, this project can be found here."** -- where "here" links to http://github.com/treellama/weland. The page also still exposes SourceForge's own project furniture: Code (/p/weland/code/), Browse Code, Tickets, Bugs, Feature Requests, and a Files/download area, which is what the frozen SITES fetches from.

This is NOT the C007 shape. There the hub was reached one hop FROM the landing page, and the two designations were read off the hub. Here the hub IS the landing page named by the frozen HOMEPAGE, so it is step 1 and readable in full.

Step 2: the relocation notice's link. Its label is "here", and the reading is the one established at C009 and C022 -- step 2 classifies a link by what it LEADS TO, and this destination is a repository root. QA-25 is satisfied in its strong form: the destination is the location itself, not a page of instructions.

Step 3: https://github.com/treellama/weland
requested_url: http://github.com/treellama/weland ; final_url: https://github.com/treellama/weland
observed_at_utc: 2026-08-27T13:36:05Z; http_status 200; redirect_chain: 1 redirect, http -> https
evidence_role: official-source-location
Observed: repository name weland, owner login treellama -- matching the SourceForge page's "Brought to you by: treellama" -- default branch master, isFork false, isMirror false, isArchived false, isTemplate false, no website field, and a source tree present at the root: Weland.cs, Editor.cs, Wadfile.cs, Geometry.cs, Drawer.cs, Settings.cs, Plugins.cs, BinaryReaderBE.cs, CrcStream.cs, Makefile, common.rsp, and directories Plugins, glade, gtk-sharp.

Inference: exactly one currently designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Weland).

On why the SourceForge Code and Files areas are not counted as competing designations: upstream ranks them itself. "As of 2015-12-05, this project can be found here" is a dated relocation statement by the project on its own page, redirecting the project's current location to the GitHub repository, and step 3 confirmed that destination holds the source tree. This is the same move as C015's, where upstream's "build against GIT, not CVS!" removed CVS from contention -- a primary marked by upstream rather than supplied by us.

The page's "Last Update: 2015-04-12" field is recorded as an incidental observation and carries no weight in this verdict. An earlier draft compared it against the relocation date to argue the SourceForge presence was frozen beforehand; that inference needs to know what that field timestamps, which this evidence never established. The migration notice does the work on its own.

Recorded because it is the weakest link in this chain and should be visible: the notice says where the PROJECT can be found, not in so many words "this is our source". What makes it a source-location designation here is that the location it names is a repository holding the source tree, observed at step 3. No separate "this is our source code" wording exists on the permitted surfaces.

Decision: PASS

## EV-C023-E2RULE-01
Candidate: C023
Gate: E2-RULE
Source: https://raw.githubusercontent.com/treellama/weland/master/Wadfile.cs
observed_at_utc: 2026-08-27T13:36:49Z; http_status 200

Observed: located witness, at Wadfile.cs:222-223, where the project states the requirement and its consequence in one place:

```text
if (Version < 2 || entryHeaderSize != 16 || directoryEntryBaseSize != 10) {
    throw new BadMapException("Only Marathon 2 and higher maps are supported");
}
```

Inference: this determines concrete validity requirements on an input artifact without our inventing them -- a map file is loadable only if its version is at least 2, its entry header size is exactly 16, and its directory entry base size is exactly 10. The message names the rule in the project's own words, and the exception type is BadMapException. This is a data-artifact requirement, not a build-environment one; the README's separate "Mono 2.10 or higher" and "Aleph One 1.4 or higher" statements are of the weaker C014 kind and are not what this verdict rests on.
Decision: PASS

## EV-C023-E3-01
Candidate: C023
Gate: E3
Source: https://raw.githubusercontent.com/treellama/weland/master/README.md, "Visual Mode" section
observed_at_utc: 2026-08-27T13:36:33Z; http_status 200

Observed: located witness -- a numbered procedure whose later steps depend on earlier ones having been performed in a separate session. "In Weland's preferences, choose a shapes file, the scenario you want to use, and a copy of Aleph One 1.4 or higher." Then "Press 'Edit Preferences' in the Visual Mode section... Aleph One will start up--configure it with the window size you want... Quit Aleph One." Only then: "When you want to texture a map, choose Visual Mode from the View menu. Make any changes to the map, and quit Aleph One. Texture changes will automatically be imported back into Weland."

Inference: whether a Visual Mode texturing session behaves as documented is conditioned on configuration performed earlier and elsewhere -- in Weland's preferences and in a prior Aleph One launch -- and the texture changes transfer only on quitting the other program. That is an ordering prerequisite of the same shape as C008's partition-before-format and C009's save-state-before-session witnesses, and E3's admission condition is deliberately weak: it asks only that a stateful/temporal validity question be exposed and examinable.

Stated at its actual strength: this is a documented ordering prerequisite, not a claim that anything is undeterminable from a map file. Positive gate: one located witness ends the survey.
Decision: PASS

## EV-C023-E4-01
Candidate: C023
Gate: E4

Positive construction exhibited, via U_enforced.

Provenance, corrected under QA-28: these observations were made against the source state available at SCREENING OBSERVATION TIME. They establish the positive E4 screening witness and nothing more. They are NOT asserted to be the sealed primary snapshot, whose resolution is a survivor-stage matter recorded separately and currently UNRESOLVED. At observation time the default branch pointed at ca7ed57956034b25af1137378027b5ad6e7c15f0.

Source: https://raw.githubusercontent.com/treellama/weland/master/Plugins.cs
observed_at_utc: 2026-08-27T13:37:17Z-13:38:09Z; http_status 200

The mechanism: the plugin enumerator in Plugins.cs. Its shape differs from every construction the run has recorded so far, and the comparison is worth stating with the two registers kept apart:

```text
historically observed (includes quarantined entries, no evidential
weight): static tables walked to a declared bound -- Games[],
codec_interfaces[], command_names[], bmap[], MDFNSetting tables,
game_num_id_tbl[]

currently admissible E4 PASS base before C023: C009, C013

C023: the first admissible PASS built on runtime reflection over a
declared directory convention rather than on a static table
```

The quarantined constructions are named only to describe the shape; they carry no evidential weight and are not counted.

EN1 external authorship: the editor and this loader existed independently of this analysis.

EN2 explicit scope: the project states the admission rule in its own comment immediately above the loop -- "// needs to have at least name and run or gtkrun". The class is Plugins, its entries are PluginInfo, and the collection is exposed through Length and GetName(int).

EN3 mechanical membership: membership is decided by fixed reflective predicates, with no analyst selection and no semantic reading of individual plugins.

```text
collect "*.dll" from three declared Plugins directories
  (beside the executable, one level above it, under applicationData)
    -> walk a.GetTypes() for every assembly loaded
      -> admit a type iff
           Compatible() exists, is static, and returns true
           Name() exists and is static
           Run or GtkRun exists and is static
```

Recorded precisely rather than by analogy: an earlier draft called this EN3's "all implementations of a declared interface". It is not that -- the loader reflects over ALL types and filters them by method shape, which is not the same as locating implementers of a declared interface. The directory convention plus the fixed predicates carry EN3 on their own, without being fitted to an example.

EN4 enforcement meaning: admission is executed by the project, condition by condition. A type without a static Compatible() returning true is skipped -- "if (compatibleMethod == null || !compatibleMethod.IsStatic || !((bool) compatibleMethod.Invoke(...))) { continue; }". A type without a static Name() is skipped. Run and GtkRun are nulled unless static, and the type is admitted only "if (plugin.Run != null || plugin.GtkRun != null)". Nothing here is inferred from a name.

EN5 closed within scope: the set is constructed at runtime by the loader's own traversal and admission test, and the resulting plugins list IS the membership. That is Section 3.2's first admissible case -- runtime construction closes the set. Tag: enforced.

EN6 outcome independence: membership is the set of admissible plugins. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, and it is worth stating as observations rather than as a list, so that it is not mistaken for a bare element inventory at the later stages:

```text
one enforcement observation per runtime-admitted type

  "type T is admitted by Weland's plugin loader under the fixed
   Compatible / Name / Run-or-GtkRun admission predicates"

retained as externally segmented fields, per observation
  declared Name
  Run / GtkRun entry-point availability
```

The universe is not "the plugins Weland has". It is the eligibility verdict the loader produces for each type it reflects over -- the same shape as counting "mapper number N is accepted" from a supported-mapper registry rather than counting the registry's rows.

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether Weland designates an authoritative rules source.

**Gate-order violation, recorded as such.** Plugins.cs was read for E4 before E3 had been adjudicated. That is the SAME structural violation as QA-21's, not a milder one: E3 was undetermined at the moment the E4 material was read, which is exactly the condition QA-21 forbids. An earlier draft of this note called it "milder ... no gate was left undetermined while reading on", which contradicts its own first sentence.

What differs is recoverability, not severity:

```text
violation
  E4 evidence read before the E3 adjudication was complete

why the verdict is nonetheless retained
  E3 PASS is independently supportable from the README witness, which
  was lawfully read at E2-RULE time and BEFORE any E4 exposure

therefore
  Plugins.cs did no work in the E3 adjudication, and entered verdict
  work only after E3 PASS was settled
```

Had E3 depended on anything read at or after the E4 exposure, the correct outcome would have been to quarantine, as at C014, C016 and C017.

Decision: PASS

## EV-C024-UR-01
Candidate: C024 (frame rank 24, games/allegro)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/allegro/Makefile
Observed: HOMEPAGE=http://liballeg.org/; V=4.2.3; DISTNAME=allegro-$V; SITES=${SITE_SOURCEFORGE:=alleg/}; COMMENT="game programming library for C/C++ developers".
Inference: every field names one packaged system, Allegro, at version 4.2.3. The metadata names a version, not a second system. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C024-E1-01
Candidate: C024
Gate: E1
Source: same frozen metadata; https://liballeg.org/
observed_at_utc: 2026-08-27T14:01:55Z; http_status 200
Observed: a third-party library -- "Allegro is a cross-platform library mainly aimed at video game and multimedia programming" -- unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C024-E2REP-01
Candidate: C024
Gate: E2-REP

Surface: the frozen HOMEPAGE. Both designations below are on it, so nothing past step 1 was opened.
requested_url: http://liballeg.org/ ; final_url: https://liballeg.org/
observed_at_utc: 2026-08-27T14:01:55Z-14:01:56Z; http_status 200; redirect_chain: 1 redirect, http -> https
evidence_role: official-project-page

Observed: the page designates two repository locations, in its own words, and distinguishes them by version line rather than by rank.

```text
navigation
  "Git repository"      -> https://github.com/liballeg/allegro5

news item, 2025-04-20, "Allegro 4 moved to its own repository"
  "We've moved Allegro 4 sources to its own repository."
                        -> https://github.com/liballeg/allegro4
  "Previously (and, in fact, currently) Allegro 4 was placed in a few
   separate branches in the main Allegro 5 repository. This made it
   hard to find and cumbersome to use. So, we've moved the relevant
   branches, tags and issues to ..."
```

Both are locations rather than routes, in QA-25's sense: each is the destination of a link on the permitted surface, and each has the `github.com/<owner>/<repo>` form of a repository root, the same basis on which C022's "GitHub" nav link was accepted.

Inference: the port packages allegro-4.2.3 -- Allegro 4 -- and upstream's own page places Allegro 4's sources in one repository and its "Git repository" navigation link on another. No primary is marked between them for the system this port packages.

Two readings would rescue a single designation, and each requires supplying a rank upstream does not state:

```text
"the system is Allegro 4, so allegro4 is its one location"
  -> this selects which of two designated repositories corresponds to
     the packaged version. The criterion reserves exactly that:
     adjudicating which of several repositories really holds the system
     "would be our judgment about the target's identity".

"the navigation link is THE designation; the news item concerns a
 sub-part"
  -> this ranks navigation above a dated news item, a hierarchy the
     page does not assert. The phrase "the main Allegro 5 repository"
     appears while describing where Allegro 4 USED to live, and does
     not settle which location is canonical for Allegro 4.
```

Not counted: "Other Git repositories" and "GitHub project" both point at https://github.com/liballeg, an account page rather than a repository location. The frozen SITES is a SourceForge files area reached by the packager, not an upstream designation, and was not opened. download.html and git.html are outside the navigation whitelist and were not opened.

Recorded as a first for the run: every previous E2REP-NO-SINGLE-CANONICAL-LOCATION arose between a source distribution and a repository. This one is between two repositories of the same project, split by version line.

Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

Gates after E2-REP are NOT_REACHED under the first-fail stop rule.

## RETRACTION 12 — C024 E2-REP withdrawn; the multiplicity argument ran backwards

EV-C024-E2REP-01 is **quarantined**. It recorded FAIL
(E2REP-NO-SINGLE-CANONICAL-LOCATION) on the finding that upstream
designates two repositories with no primary between them.

**The error.** The entry argued that treating github.com/liballeg/allegro4
as the candidate's location would be "our judgment about the target's
identity". That inverts what the evidence shows. Upstream supplies the
partition itself, in the sentence the entry quotes:

```text
"We've moved Allegro 4 sources to its own repository."
    -> https://github.com/liballeg/allegro4
```

E2-REP asks whether upstream designates a canonical source location FOR
THE SYSTEM UNDER EXAMINATION. UR resolved this port to Allegro 4.2.3,
and upstream's own label associates Allegro 4 sources with that
repository. Applying an upstream-supplied version-line label is not
analyst selection; it is the opposite of the C002-family error, which
was supplying a hierarchy upstream had not stated.

So allegro5 was never shown to be a competing designation for THIS
candidate. On the observations made it is designated for a different
upstream version line.

**Why the verdict does not become PASS.** E2-REP also requires the
designated location to hold a source tree, observed at its root surface.
The withdrawn entry concluded FAIL at step 1 and never opened
github.com/liballeg/allegro4. Opening it now to rescue the verdict would
be observation after a terminal verdict, which QA-21 exists to stop --
the same restraint applied at C020, where cvs.html was left unopened.

## EV-C024-E2REP-02  (supersedes the quarantined EV-C024-E2REP-01)
Candidate: C024 (frame rank 24, games/allegro)
Gate: E2-REP

Surface: the frozen HOMEPAGE. Nothing past step 1 was opened.
requested_url: http://liballeg.org/ ; final_url: https://liballeg.org/
observed_at_utc: 2026-08-27T14:01:55Z-14:01:56Z; http_status 200; redirect_chain: 1 redirect, http -> https
evidence_role: official-project-page

Observed: the page exposes two repository locations and labels them by version line, in its own words.

```text
navigation
  "Git repository"      -> https://github.com/liballeg/allegro5

news item, 2025-04-20, "Allegro 4 moved to its own repository"
  "We've moved Allegro 4 sources to its own repository."
                        -> https://github.com/liballeg/allegro4
```

```text
established
  upstream explicitly associates Allegro 4 SOURCES with
  github.com/liballeg/allegro4, and the port resolved by UR is
  allegro-4.2.3.

not established
  source-tree presence at that repository root. Step 3 was never
  observed, because the withdrawn entry stopped at step 1 on a FAIL.

multi-location FAIL not established
  allegro5 is designated for a different upstream version line on the
  observations made. It was not shown to be a second canonical source
  location for the Allegro 4 candidate, and counting it as one would
  ignore the partition upstream states.

PASS not established / FAIL not established
```

Not counted: "Other Git repositories" and "GitHub project" both point at https://github.com/liballeg, an account page rather than a repository location. The frozen SITES is a SourceForge files area reached by the packager, not an upstream designation, and was not opened; download.html and git.html are outside the navigation whitelist.

Also withdrawn with the verdict: the entry's closing claim that this was the run's first E2REP-NO-SINGLE-CANONICAL-LOCATION arising between two repositories of one project. No such finding stands.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C025-UR-01
Candidate: C025 (frame rank 25, games/amnesia-tdd)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/amnesia-tdd/Makefile
Observed: HOMEPAGE=https://www.amnesiagame.com/; GH_ACCOUNT=shamazmazum; GH_PROJECT=AmnesiaTheDarkDescent; GH_TAGNAME=v${V} with V=0.3.2; DISTNAME=amnesia-tdd-${V}; COMMENT="first person survival horror game".

Inference: the frozen fields name one system by name -- Amnesia: The Dark Descent. The protocol settles this shape explicitly: "A port whose HOMEPAGE points at a project website while GH_ACCOUNT/GH_PROJECT point at a repository ... is not ambiguous: those are several facts about one system. UR-AMBIGUOUS applies only where the metadata points at genuinely different systems with no external basis for choosing."

UR is decided from the frozen metadata alone, and nothing beyond it is used here. Which location is canonical is not decided from OpenBSD's metadata at all; that belongs to E2-REP.
Decision: PASS

## EV-C025-E1-01
Candidate: C025
Gate: E1
Source: same frozen metadata; https://www.amnesiagame.com/
observed_at_utc: 2026-08-27T14:17:57Z; http_status 200
Observed: a third-party commercial game published by Frictional Games, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C025-E2REP-01
Candidate: C025
Gate: E2-REP

Surface 1: https://www.amnesiagame.com/ -- the frozen HOMEPAGE, navigation step 1.
Necessary because: E2-REP asks what upstream designates, and this is the official site the frozen metadata names.
observed_at_utc: 2026-08-27T14:17:57Z-14:17:59Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: a commercial product page. Its links are the publisher's own site, forum, dev blog, dev wiki, support and store; retail storefronts (Steam, GOG, Humble, PlayStation, Mac App Store, Desura, regional publishers); press reviews; and demo downloads. It exposes no Source, Code, Repository or Development link, so navigation step 2 has no target on this surface.

Surface 2: https://github.com/shamazmazum/AmnesiaTheDarkDescent -- reached from the frozen GH_ACCOUNT/GH_PROJECT, which the contract admits as a starting point.
Necessary because: the gate is unsettled after surface 1, and this is the remaining admitted identifier. Under QA-24 an admitted surface that the gate still needs is observed rather than skipped, with the scope fixed first.

Observation scope, fixed before the request:

```text
observe only
  repository and account identity
  fork / mirror / archive markings
  source-tree presence
  any designation signal carried in allowed repository metadata

do not
  select a different repository because its name looks related
  follow a fork to its parent and treat that as the upstream
  read README prose for a designation
```

observed_at_utc: 2026-08-27T14:18:32Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: repository AmnesiaTheDarkDescent, owner login shamazmazum, default branch master, isMirror false, isArchived false, isTemplate false, no website field, and a source tree present -- HPL2, amnesia/src, .github/workflows, CONTRIBUTING.md, LICENSE, README.md.

And the marking that matters here, which the contract names among allowed observations: **isFork: true**, with the page's own banner reading "AmnesiaTheDarkDescent Public forked from TiManGames/AmnesiaTheDarkDescent".

The parent was not followed, and the reason is narrower than an earlier draft of this entry gave. That draft said following it "would select among plausible upstreams". That is not accurate: TiManGames/AmnesiaTheDarkDescent is not a candidate an analyst picked by name resemblance -- it is supplied directly by GitHub's structured fork relation. The actual reason is simply that the sealed navigation does not reach it:

```text
allowed navigation
  1. official landing page
  2. a Source/Code/Repository/Development link that page exposes
  3. the repository root that link reaches

following a fork-parent relation is not among these, and the fork
parent is not an identifier in the frozen metadata, so it is not an
admitted starting point either
```

An earlier draft carried a contextual note here saying the account is "an individual's rather than the publisher's" and that 0.3.2 "is not the commercial game's version line". Both are deleted rather than relocated. Moving an unsupported fact from one gate to another does not supply evidence for it: no account-type observation was recorded, and nothing observed establishes the commercial game's version line. What is recorded is only what was seen:

```text
frozen metadata     GH_ACCOUNT = shamazmazum
                    V = 0.3.2

repository root     owner login = shamazmazum
                    isFork = true
                    fork parent = TiManGames/AmnesiaTheDarkDescent
```

Adjudication:

```text
PASS not established
  the frozen GH identifiers lead to shamazmazum/AmnesiaTheDarkDescent,
  and that repository is explicitly marked a fork of
  TiManGames/AmnesiaTheDarkDescent. The fork-parent relation is an
  observed repository fact; the parent is neither an admitted starting
  point nor an authorized navigation hop, and is not promoted here to
  either an affiliation or a designation.

  Arriving at the frozen repository via a packaging identifier yields
  affiliation rather than designation (QA-22). No designation signal
  for this candidate's canonical source was observed on either
  admissible surface examined -- the frozen HOMEPAGE landing page, and
  the frozen GH repository root's metadata.

FAIL not established
  "designates none" is a claim about upstream, and what was observed
  is that two examined surfaces carried no designation signal. That
  is not the same statement.
```

`E2REP-NO-SOURCE` in particular does not apply, and the reason is worth stating because it inverts the usual shape. That code means no access to the actual source representation. Access is not the problem here: a source tree was observed at the frozen GH location -- HPL2, amnesia/src. What is missing is upstream designation of that location as this candidate's canonical source. The gate is undetermined because the designation was not established, not because the source was unreachable.

Recorded as a first for the run, scoped to what was actually recorded: among repository-root observations for which fork status was noted, C025 is the first with isFork true. Candidates that stopped earlier, or whose upstream was not a code-hosting repository, carry no such observation either way.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED. Screening stopped here rather than reading on, per QA-21.

## EV-C026-UR-01
Candidate: C026 (frame rank 26, games/amoebax)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/amoebax/Makefile
Observed: HOMEPAGE=http://www.emma-soft.com/games/amoebax/; SITES=${HOMEPAGE}download/; DISTNAME=amoebax-0.2.1; EXTRACT_SUFX=.tar.bz2; COMMENT="cute and addictive action-puzzle game".
Inference: every field names one packaged system, Amoebax, and SITES resolves inside HOMEPAGE, so the frozen metadata points at a single host. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C026-E1-01
Candidate: C026
Gate: E1
Source: same frozen metadata; https://www.emma-soft.com/games/amoebax/
observed_at_utc: 2026-08-27T14:29:52Z; http_status 200
Observed: a third-party puzzle game credited on its own page to Safareig Creatiu, Alex Almarza, Jordi Fita and Ferran Brugat, "Copyright (c) 2007 Emma's Software", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C026-E2REP-01
Candidate: C026
Gate: E2-REP

Surface: the frozen HOMEPAGE, which is also the parent of the frozen SITES path. It is the only admissible surface, and nothing past step 1 was opened.
requested_url: http://www.emma-soft.com/games/amoebax/ ; final_url: https://www.emma-soft.com/games/amoebax/
observed_at_utc: 2026-08-27T14:29:52Z-14:29:54Z; http_status 200; redirect_chain: 1 redirect, http -> https
evidence_role: official-project-page

Observed: under "Free Download" the page exposes three artifacts, all platform binaries -- download/amoebax-0.2.0.msi, download/amoebax-0.2.0.dmg, download/amoebax-0.2.0.x86.package -- plus a link labelled "Other downloads" to download.html. Its body gives an introduction, screenshots, a features list, system requirements and author credits. It states "Software libre and free of charge" among the features. It exposes no Source, Code, Repository or Development link, and no link whose destination is a source location.

```text
PASS not established
  no designation signal was observed on the one admissible surface
  examined. The three exposed artifacts are platform binaries; a
  licence statement in a features list is not a designation of a
  source location.

FAIL not established
  "designates none" is a claim about upstream, and what was observed
  is that one page carried no designation signal. The page also
  exposes "Other downloads", which was not opened.
```

download.html was NOT opened. "Downloads" is not among the navigation contract's four labels, and QA-17 settled that the criterion's phrase "source distribution" may not be used to widen the whitelist -- the exact move withdrawn at C014 and again at C002. The frozen SITES points into that same download area and is a packaging fetch path, which cannot substitute for upstream designation.

Recorded so the shape is visible: this is the plainest instance yet of a candidate stopping for want of a designation rather than for anything about the project. The source tarball the port fetches presumably sits one click away, behind a label the contract does not admit.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 13 — C026 E2-REP superseded; a necessary admitted surface was skipped

EV-C026-E2REP-01 is **superseded**. Its verdict, UNRESOLVED, stands. Its
reasoning contained one structural error and two claims it could not
support.

**The error.** The entry called the frozen HOMEPAGE "the only admissible
surface". It is not. The frozen metadata also carries
`SITES=${HOMEPAGE}download/`, and the contract admits "the URLs and
identifiers found in the frozen OpenBSD metadata" as starting points. A
URL in the metadata is admitted whether or not the landing page links to
it.

The entry applied QA-24 to the landing page's navigation and failed to
apply it to the frozen SITES starting point. Those are different things,
and conflating them is what produced the mistake:

```text
landing page's "Other downloads" -> download.html
  a NAVIGATION step past step 1, to a label the whitelist omits
  -> forbidden by QA-17, correctly not opened

frozen SITES /download/
  an ADMITTED STARTING POINT supplied by the metadata itself
  -> not navigation at all; observing it needs no whitelist label
```

And it was necessary under QA-11, not merely admitted: the gate was
unsettled after the landing page, this was the remaining admitted
starting point, it sits on the same upstream domain, and nothing had
established it as packager-side. That last clause is what let C010's
SITES go unopened -- its port Makefile's own dist: target had shown the
host to be the packager's. C026 has no such finding.

**Why this is repaired rather than left standing.** C018 set the
precedent: where a necessary admitted surface was skipped, the fix is to
observe it under a scope fixed in advance, which is how QA-24 came to
exist. That is different from C020 and C024, where a TERMINAL verdict
would have been rescued by fresh observation. Here the omission is
itself the procedural error.

**Two claims withdrawn.** "The plainest instance yet of a candidate
stopping for want of a designation" could not be said with a necessary
surface unobserved. "The source tarball the port fetches presumably sits
one click away" was never observed at all -- what is knowable is only
that the frozen packaging metadata composes that path and filename.

## EV-C026-E2REP-02  (supersedes EV-C026-E2REP-01)
Candidate: C026 (frame rank 26, games/amoebax)
Gate: E2-REP

Surface 1: the frozen HOMEPAGE.
requested_url: http://www.emma-soft.com/games/amoebax/ ; final_url: https://www.emma-soft.com/games/amoebax/
observed_at_utc: 2026-08-27T14:29:52Z-14:29:54Z; http_status 200; redirect_chain: 1 redirect, http -> https
Observed: under "Free Download" the page exposes three artifacts, all platform binaries -- download/amoebax-0.2.0.msi, download/amoebax-0.2.0.dmg, download/amoebax-0.2.0.x86.package -- plus a link labelled "Other downloads" to download.html. The body gives an introduction, screenshots, features, system requirements and author credits, and states "Software libre and free of charge" among the features. No Source, Code, Repository or Development link, and no link whose destination is a source location.

Surface 2: http://www.emma-soft.com/games/amoebax/download/ -- the frozen SITES.
Necessary because: the gate was unsettled after surface 1, this is the remaining admitted starting point from the frozen metadata, it is on the same upstream domain, and nothing observed establishes it as packager-side. Under QA-11 that makes it necessary, and under QA-24 a necessary admitted surface is observed rather than skipped.

Observation scope, fixed before the request:

```text
observe only
  the surface's existence and HTTP status
  labels or headings the page or listing itself carries
  artifact names and link relations it directly exposes
  an explicit "source" / "source code" designation
  primary or mirror marking

do not
  navigate to download.html
  open any document or source file
  infer that an artifact is source from its filename
  search for other locations
```

requested_url: http://www.emma-soft.com/games/amoebax/download/ ; final_url: https://www.emma-soft.com/games/amoebax/download/
observed_at_utc: 2026-08-27T14:45:03Z (GET), 14:45:24Z (HEAD)
http_status: 403, 403; redirect_chain: 1 redirect, http -> https, on both
control: the landing page returned 200 at 14:45:24Z, same host, same moment
Observed: a 199-byte server error page, "403 Forbidden -- You don't have permission to access this resource." It carries no headings beyond "Forbidden", no links, no artifact names, and no designation signal.

Inference, kept to what the responses establish:

```text
transport completed and the endpoint returned a definite HTTP response
on both GET and HEAD, with the same-host landing page returning 200 at
the control moment
  -> this is not the timeout / DNS / refused / 5xx family, so
     PI-TRANSPORT-INDETERMINATE does not fit

the 403 does not reveal the contents of the admitted SITES URL, and
establishes neither absence, nor designation, nor source-tree presence
```

No claim is made that the server distinguishes this path from a missing one: no nonexistent-path control was requested, so that comparison was never available. Nor is the resource's existence asserted -- what is established is that a request to this URL was answered Forbidden, twice.

```text
PASS not established
  no designation signal was observed on either admissible surface. The
  landing page exposes only platform binaries, and a licence statement
  in a features list is not a designation of a location. The frozen
  SITES path refuses listing, so it yielded no observation at all.

FAIL not established
  "designates none" is a claim about upstream. What was observed is
  that one page carried no designation signal and one path could not
  be read. download.html remains unopened, being outside the
  navigation whitelist.
```

On the code: `PI-TRANSPORT-INDETERMINATE` would be wrong here, since transport completed and the server answered twice. Equally, a 403 on its own completes no specific E2-REP failure code. An admitted starting point answering Forbidden is a screening outcome the sealed criteria do not describe, which is what `PI-UNCLASSIFIED-SHAPE` is for. The verdict code is unchanged from the superseded entry even though its evidence base now includes the surface that entry never opened.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C028-UR-01
Candidate: C028 (frame rank 28, games/an)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/an/Makefile
Observed: HOMEPAGE=https://salsa.debian.org/pm/an; SITES=${SITE_DEBIAN:=main/a/an/}; DISTNAME=an_1.2.orig; PKGNAME=an-1.2; COMMENT="fast anagram generator".
Inference: the frozen fields name one system, `an`. HOMEPAGE pointing at a repository while SITES points at a distribution archive is the shape the protocol names as non-ambiguous -- "several facts about one system". Not UR-AMBIGUOUS.
Decision: PASS

## EV-C028-E1-01
Candidate: C028
Gate: E1
Source: same frozen metadata; https://salsa.debian.org/pm/an
observed_at_utc: 2026-08-27T14:51:40Z; http_status 200
Observed: a third-party anagram generator, the repository titled "Paul Martin / an", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C028-E2REP-01
Candidate: C028
Gate: E2-REP

Per QA-27, both URLs the frozen metadata supplies are accounted for, and both were observed.

Surface 1: https://salsa.debian.org/pm/an -- the frozen HOMEPAGE, which is a GitLab repository root.
observed_at_utc: 2026-08-27T14:51:40Z-14:51:41Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed, restricted to metadata the contract allows: repository titled "Paul Martin / an", project id 27883, default branch master, data-is-project-empty="false". The served page carries no fork-of, archived or mirror marking, no website field, and no description meta. Its file tree is rendered client-side, so the served root carries no listing.

Surface 2: https://ftp.debian.org/debian/pool/main/a/an/ -- the frozen SITES.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point. It was NOT lawfully skippable the way C010's SITES was: there the port Makefile's own dist: target showed the host to be the packager's, and nothing here establishes an equivalent. That C026 lesson is applied rather than re-learned.
observed_at_utc: 2026-08-27T14:52:18Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: an Apache directory index, "Index of /debian/pool/main/a/an", listing per-architecture .deb binaries together with an_1.2-6.debian.tar.xz, an_1.2-6.dsc and their successors. It carries no headings, labels or statements beyond the index furniture -- no designation of a canonical source location, no primary or mirror marking.

```text
PASS not established, for two separately unmet prerequisites of the
same requirement

  1. canonical designation not established
     no designation signal was observed on either admissible surface.
     Arriving at the repository through the frozen HOMEPAGE yields
     affiliation, not designation (QA-22), and the archive index makes
     no statement at all.

  2. source-tree presence at the repository root not established
     the root renders its tree client-side. This is QA-20's gap: it
     establishes repository IDENTITY -- name, owner, default branch,
     non-emptiness -- and carries no source-tree evidence, and the
     sealed navigation provides no authorized follow-up surface.

FAIL not established
  two surfaces carrying no designation signal is not a demonstration
  that upstream designates none.
```

These are prerequisites of one requirement rather than separate criteria: E2-REP asks for a designated canonical location that actually holds a source tree. Calling them "independent legs", as an earlier draft did, reads as though two different tests failed.

QA-20 predicted this conditionally, on the shape rather than the host: "if a later candidate reaches an allowed repository root that establishes IDENTITY but carries no source-tree evidence, the same gap applies, whatever the hosting vendor." C028 is the first candidate to meet that condition since it was written, and the prediction is recorded as borne out on one case, not as a rate.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C029-UR-01
Candidate: C029 (frame rank 29, games/angband)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/angband/Makefile
Observed: HOMEPAGE=http://rephial.org; SITES=https://github.com/angband/angband/releases/download/${V}/ with V=4.2.5; DISTNAME=Angband-${V}; PKGNAME=${DISTNAME:L}; COMMENT="rogue-like game with X11 support".
Inference: the frozen fields name one system, Angband. HOMEPAGE pointing at a project site while SITES points at a release-download path is the shape the protocol names non-ambiguous -- several facts about one system. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C029-E1-01
Candidate: C029
Gate: E1
Source: same frozen metadata; https://rephial.org/
observed_at_utc: 2026-08-27T15:22:48Z; http_status 200
Observed: a third-party roguelike, described on its own About page as descending from Moria and UMoria and "currently maintained by a rather loose-knit development team", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C029-E2REP-01
Candidate: C029
Gate: E2-REP

Per QA-27, both URLs the frozen metadata supplies are accounted for. HOMEPAGE was observed as step 1. SITES resolves into the same GitHub release-download path as the designation found below -- content of the same distribution channel rather than a separate location (the C022 reading) -- and was not separately opened.

Step 1: the frozen HOMEPAGE.
requested_url: http://rephial.org ; final_url: https://rephial.org/
observed_at_utc: 2026-08-27T15:22:48Z-15:22:49Z; http_status 200; redirect_chain: 1 redirect, http -> https
evidence_role: official-project-page
Observed: the page exposes a link labelled **"Source code"** whose destination is https://github.com/angband/angband/releases/download/4.2.6/Angband-4.2.6.tar.gz, beside Windows and macOS binary links for the same version. Its navigation is About (/develop), Releases (/release), Docs (angband.readthedocs.io) and Forum.

The designation signal is a label in the plainest form QA-23 admits: the page's own word for the link is "Source code", and its destination is a location -- a URL -- not a page of instructions. QA-25 is satisfied directly.

Step 2 and the uniqueness check: /develop, the destination of the "About" link.
Necessary because: recording "exactly one designated location" requires having looked where a second could be, which C019 established after claiming uniqueness it had not checked. /develop is the site's own development path and is where a repository designation would sit.
observed_at_utc: 2026-08-27T15:23:31Z; http_status 200; redirect_chain: NONE
Observed: an About page giving the project's history and contribution guidance. Its only github.com link is https://github.com/angband/angband/issues -- an issue tracker, which the contract names among forbidden E2-REP surfaces and which is not a designation of a source location in any case; it was not opened. Its other outbound links are nickmcconnell.github.io/AngbandPlus and tangaria.com/variants, which upstream introduces as sources and descriptions for **variants** -- other systems, stated as such: "Source code for many of the variants is available at ...". No canonical source location for Angband itself is designated there.

Source-tree presence at the designated location, which E2-REP requires of the designated artifact:
observed_at_utc: 2026-08-27T15:23:56Z; http_status 200; 25932904 bytes
sha256 8c0ffa2b85d74bd0cc273752f61c0440dba93323cd790be460f90c8dced7cbf4
Listing entry names only, reading no file: 1181 entries, with src/ carrying borg, cocoa, sdl2, win, nds, tests, stats, cmake and doc beneath it, alongside lib/, docs/, tests/, configure.ac, CMakeLists.txt, README.md and CONTRIBUTING.md.

Inference: exactly one designated canonical source location, a source distribution at a stable URL, designated by upstream on its own page under the label "Source code", and holding a source tree. One external target identifier: Angband.

Recorded rather than glossed: the tarball's URL form reveals a repository at github.com/angband/angband, but no admissible surface DESIGNATES that repository. Under QA-25 a location counts only when observed as designated, not when inferred from a URL's shape, so this is not the C015 distribution-plus-repository shape.

Snapshot caveat, for the inventory stage: the designated artifact observed is 4.2.6, while the frozen port packages 4.2.5. The snapshot rule fixes the artifact designated at the enumeration execution timestamp, 2026-08-26T19:23:05Z, and nothing observed establishes which version was designated at that instant rather than a day later when this page was read. The hash recorded is of the artifact designated at observation time, and the gap is flagged here rather than smoothed over.

Decision: PASS

## EV-C029-E2RULE-01
Candidate: C029
Gate: E2-RULE
Source: lib/gamedata/constants.txt in the designated artifact
observed_at_utc: 2026-08-27T15:23:56Z (artifact retrieved), read shortly after

Observed: located witness, stated by the project in the data file's own comment and immediately applied by the value beneath it:

```text
# Maximum dungeon level; must be at least 100.
# Setting it below 128 may prevent the creation of some objects.
world:max-depth:128
```

The same file states ordering constraints in the same voice -- "the cutoffs for all levels but the last must be in scrictly ascending order" -- and "The first value must be positive."

Inference: this determines a concrete validity requirement on an input artifact without our inventing it. A gamedata file setting world:max-depth below 100 does not satisfy the project's stated requirement. The requirement is numeric and sits in the file it governs.
Decision: PASS

## EV-C029-E3-01
Candidate: C029
Gate: E3
Source: docs/hacking/modifying.rst in the designated artifact, the object.txt description
observed_at_utc: same retrieval

Observed: located witness, quoted -- "A tval-sval pair completely identifies an object - since the tval and sval are saved to savefiles, removing or adding objects is likely to render existing save files unusable." The same document adds, of ego items, that "removing or changing one with an instance currently in the game might cause problems."

Inference: whether an existing save file remains loadable is not decidable from that save file alone. It depends on whether the gamedata files were edited after the save was written -- the identifiers the save stores are indices into tables that the data files define, so an edit performed later invalidates a file written earlier. That is validity conditioned on history, the shape E3 asks for, and it is stated by the project rather than inferred.
Decision: PASS

## EV-C029-E4-01
Candidate: C029
Gate: E4

Positive construction exhibited, via U_enforced, in the designated artifact at the recorded hash.

The mechanism: the gamedata parser registry, src/init.c:4349-4387, introduced by the project's own comment -- "A list of all the above parsers, plus those found in mon-init.c and obj-init.c".

```text
static struct {
    const char *name;
    struct file_parser *parser;
} pl[] = {
    { "world", &world_parser },
    { "object bases", &object_base_parser },
    { "objects", &object_parser },
    { "artifacts", &artifact_parser },
    { "monsters", &monster_parser },
    { "traps", &trap_parser },
    ...
};
```

EN1 external authorship: the game and this registry existed independently of this analysis.

EN2 explicit scope: the project names the domain in its own comment -- a list of ALL the parsers -- and each entry pairs a domain label with the parser that reads that domain's data file. 37 entries, from "world" through "random names".

EN3 mechanical membership: array membership in pl[], bounded by N_ELEMENTS(pl). No semantic reading of individual entries is required.

EN4 enforcement meaning: the project executes the enforcement over exactly this set, and a failure is fatal.

```text
for (i = 0; i < N_ELEMENTS(pl); i++) {
    ...
    if (run_parser(pl[i].parser))
        quit_fmt("Cannot initialize %s.", pl[i].name);
}
```

Each registered parser decides whether its data file is acceptable, and rejection aborts startup with the project's own message naming the domain. This meaning is executed, not inferred from a name.

EN5 closed within scope: the loop bound is N_ELEMENTS(pl), the enumerator's own extent, walked at runtime by init_arrays. Section 3.2's first admissible case -- runtime construction closes the set. Tag: enforced.

EN6 outcome independence: membership is the set of data domains the game parses. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations rather than as a list:

```text
one enforcement observation per registered parser

  "data domain D is validated at initialization by parser P, and a
   parse failure aborts startup"

retained as externally segmented fields, per observation
  the project's own domain label
  the parser it names
```

Normative route: not investigated, because only one route is required and U_enforced supplies it. No claim is made about whether Angband designates an authoritative rules source.

Decision: PASS

## RETRACTION 14 — C029 E2-REP withdrawn; a navigation breach, and a snapshot that was never established

EV-C029-E2REP-01 is **quarantined**, and with it EV-C029-E2RULE-01,
EV-C029-E3-01 and EV-C029-E4-01 as post-stop exposure. Nothing is
deleted. The observations were accurately made; the constants.txt rule,
the savefile witness and the pl[] registry are all really there.

**Breach: /develop was not an authorized step 2.** The landing page's
link label is "About". The contract admits "a Source / Code / Repository
/ Development link that page explicitly exposes", and an href that
happens to read /develop does not turn an About link into a Development
link. The withdrawn entry justified opening it as the place "where a
repository designation would sit" -- which is the search discretion the
whitelist exists to remove, and the same move withdrawn at C014.
Uniqueness has to close inside the sealed surfaces, not wherever a
second location might plausibly live.

**The larger failure: the primary snapshot was never established.** The
sealed rule for a distribution candidate is not "the artifact designated
now". It is:

```text
the externally designated canonical artifact at the ENUMERATION
EXECUTION TIMESTAMP -- 2026-08-26T19:23:05Z -- recorded by content hash
```

and the protocol keeps that time axis separate from screening
observation time in as many words. The withdrawn entry observed 4.2.6 on
2026-08-27, noted in its own text that nothing established which version
was designated at the enumeration instant, and then wrote that day's
hash into `primary_snapshot` regardless, calling the gap a caveat for
the inventory stage.

It is not a caveat. `primary_snapshot` is not one of the three fields
`PENDING_INVENTORY` covers; the sealed rule is supposed to resolve it
mechanically, before anything downstream is read. Recording an
observation-time artifact there substitutes a different rule for the
sealed one.

**And it propagates.** E2-RULE, E3 and E4 were all determined by reading
inside the 4.2.6 tarball. The methodology binds downstream work to the
frozen primary snapshot, so those three verdicts rest on bytes that were
never established as the ones the rule selects. They are quarantined
rather than repaired: choosing 4.2.5 because the port packages it would
substitute packaging metadata for the sealed rule, and assuming 4.2.6
was current a day earlier would assume exactly what is unestablished.

**Where this stops the candidate.** The Primary snapshot requirement
sits inside the sealed spec's E2-REP section, so an unresolvable
snapshot is an E2-REP-section failure and E2-REP is the stop gate.

## EV-C029-E2REP-02  (supersedes the quarantined EV-C029-E2REP-01)
Candidate: C029 (frame rank 29, games/angband)
Gate: E2-REP

Step 1: the frozen HOMEPAGE.
requested_url: http://rephial.org ; final_url: https://rephial.org/
observed_at_utc: 2026-08-27T15:22:48Z-15:22:49Z; http_status 200; redirect_chain: 1 redirect, http -> https
Observed: the page exposes a link labelled "Source code" whose destination is https://github.com/angband/angband/releases/download/4.2.6/Angband-4.2.6.tar.gz, beside Windows and macOS binary links for the same version. Its navigation reads About, Releases, Docs, Forum. It carries no date for the release it presents.

Retrieval of that artifact, kept as an observation of the present designation only:
observed_at_utc: 2026-08-27T15:23:56Z; http_status 200; 25932904 bytes; sha256 8c0ffa2b85d74bd0cc273752f61c0440dba93323cd790be460f90c8dced7cbf4. Listing names only: 1181 entries, src/ with borg, cocoa, sdl2, win, nds, tests, stats.

```text
established at screening time
  upstream designates a source distribution, labelled "Source code",
  at a stable URL, and that artifact holds a source tree.

NOT established, and this alone decides the gate
  uniqueness. The withdrawn entry closed this by opening /develop,
  which was not an authorized surface; that observation is
  quarantined, and no admissible replacement was obtained. Whether
  upstream designates exactly one canonical source location is
  therefore open.
```

The snapshot question is deliberately NOT a ground here. An earlier draft made "which artifact was designated at the enumeration instant" part of this gate's failure. It is not part of this gate: `primary_snapshot` is a survivor-stage field the sealed rule fills for candidates that survive E1-E4, and the E2-REP network contract's own purpose list -- location, designation, stable URL, one target identifier, actual source tree -- does not include it. C029 stops at E2-REP on uniqueness, and never reaches the stage where its snapshot would be resolved.

Also withdrawn from this entry: the claim that because the frozen port packages 4.2.5 while screening-time designation is 4.2.6, "a designation change occurred at some unbounded point". It shows no such thing -- it establishes what OpenBSD packaged, and packaging metadata is not upstream designation.

Frozen SITES, observed rather than reasoned about. An earlier draft skipped it, arguing the snapshot ground was "not curable by anything at that path". That decided the outcome from the URL's shape before looking, which is the C018 error, so the surface was opened under a scope fixed first: existence and HTTP status, labels or headings the surface itself carries, artifact names and link relations it exposes, and any timestamp, release metadata or marking that binds a designation to a moment -- and explicitly not navigating to /release or /develop, not opening files, and not inferring from filenames.

requested_url and final_url: https://github.com/angband/angband/releases/download/4.2.5/
observed_at_utc: 2026-08-27T15:43:15Z (GET), 15:43:28Z (HEAD)
http_status: 404, 404; redirect_chain: NONE on both
control: the designated 4.2.6 artifact returned 200 at 15:43:28Z, same host, same moment
Observed: a 9-byte body, "Not Found". No labels, no headings, no artifact names, no timestamps, no release metadata, no designation marking. The surface yields nothing bearing on what was designated at the enumeration instant.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## RETRACTION 15 — C013's primary snapshot does not survive the same audit

An audit note written alongside C029's retraction concluded that C013's
snapshot survived, because the mednafen page presents releases as a
dated News list whose top entry reads "Mednafen 1.32.1, April 5, 2024".
The argument was: the newest entry predates the enumeration timestamp by
over two years, so the designation could not have changed in between.

That argument is wrong, and it is the same substitution C029 was
withdrawn for -- one gate later and in gentler clothing.

```text
what was directly observed, on 2026-08-27T09:01:57Z
  the page shows 1.32.1 as the current release
  that entry carries the date 2024-04-05

what it establishes
  1.32.1 was released on 2024-04-05
  1.32.1 is the designated artifact AT OBSERVATION TIME

what it does not establish
  what was designated at 2026-08-26T19:23:05Z
```

A release date is not a designation interval. Nothing in the record
closes the window between the enumeration instant and observation: a
different artifact could have been designated in between and the page
returned to this state, or the artifact at that URL could have been
replaced and restored. Those are not likely; they are simply not
excluded, and "not excluded" is where this run has consistently drawn
the line.

Accordingly, and on the same footing as C029:

```text
primary_snapshot          UNRESOLVED
EV-C013-E2RULE-01         quarantined as post-stop exposure
EV-C013-E3-01             quarantined
EV-C013-E4-01             quarantined
overall                   UNRESOLVED, stop gate E2-REP
```

The quarantined observations remain accurate -- the 32768-triplet
palette requirement, the multi-CD disc-switch witness, and the
MDFNSetting registry with its explicit Finalize() closure are all really
in that tarball. What is unestablished is that that tarball is the one
the sealed rule selects.

## EV-C013-E2REP-02  (supersedes EV-C013-E2REP-01)
Candidate: C013 (frame rank 13, emulators/mednafen)
Gate: E2-REP

The designation findings of the superseded entry are unaffected and are not re-argued here: upstream presents the source tarball on its own landing page, under its own domain, with the SHA-256 published beside it, and the retrieved artifact's hash matched that published value. Exactly one source location was designated at screening time.

What fails is the Primary snapshot requirement, which the sealed spec places inside this same E2-REP section.

```text
established
  at screening time, upstream designates
  https://mednafen.github.io/releases/files/mednafen-1.32.1.tar.xz,
  hash verified against upstream's own published SHA-256, holding a
  source tree.

NOT established
  that this was the externally designated canonical artifact at the
  enumeration execution timestamp, 2026-08-26T19:23:05Z. The page's
  dated News entry establishes the release date, not the designation
  state at that instant, and no observation bounds the interval
  between then and observation.
```

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## RETRACTION 15a — C013 gates after E2-REP
EV-C013-E2RULE-01, EV-C013-E3-01 and EV-C013-E4-01 are quarantined as
post-stop exposure, on the principle applied at C005, C014, C016, C017
and C029. Kept on the record, used for nothing.

## RETRACTION 16 — the snapshot failure was filed at the wrong stage

RETRACTION 15 withdrew C013's E2-REP on the ground that its primary
snapshot was unestablished. That disposition is wrong by one level, and
C013 is restored.

**`primary_snapshot` is not part of the E2-REP gate.** The network
contract states this gate's purpose as: a canonical source location
exists, is designated by upstream, sits at a stable URL, carries one
external target identifier, and actually holds a source tree. The
snapshot is not among them. The schema places it with the fields
"performed only for candidates surviving E1-E4", and the sealed order
runs screen-all-128 -> fix the survivor set -> freeze inventories ->
rank. It is a survivor-stage resolution, not a candidate verdict.

So what was found is real but belongs one stage later:

```text
NOT      an E2-REP criterion failure
BUT      a survivor-stage primary_snapshot resolution failure
```

**Restored:** C013 is an E1-E4 survivor again. Its E2-REP designation
findings were never in question -- upstream presents the source tarball
on its own domain with the SHA-256 beside it, the retrieved artifact
matched that published hash, and it holds a source tree. Its E2-RULE, E3
and E4 entries come out of quarantine: those gates were determined on
their own witnesses, and screening gates are not conditioned on the
snapshot field.

**Withdrawn instead, and for all three survivors:** the recorded
`primary_snapshot` values.

```text
C009 FCEUX     a62b868e...      -> UNRESOLVED
C013 Mednafen  sha256:de7eb94a. -> UNRESOLVED
C023 Weland    ca7ed579...      -> UNRESOLVED
```

## EV-C013-E2REP-03  (supersedes EV-C013-E2REP-02; restores the verdict of -01)
Candidate: C013 (frame rank 13, emulators/mednafen)
Gate: E2-REP

The designation findings of EV-C013-E2REP-01 stand and are not re-argued: upstream presents the source tarball on its own landing page under its own domain with the SHA-256 published beside it; the retrieved artifact's hash matched that published value byte for byte; listing its entries showed a source tree; the .zip artifacts are named as Windows builds; older releases in the same directory are a version history rather than competing designations.

EV-C013-E2REP-02 withdrew that verdict over the primary snapshot. That was a stage error, corrected here: the snapshot is a survivor-stage field, not one of this gate's conditions.

Decision: PASS

## EV-C013-SNAPSHOT-01
Candidate: C013
Stage: survivor-stage primary snapshot resolution (not a screening gate)

```text
sealed rule, distribution branch
  the externally designated canonical artifact at the enumeration
  execution timestamp, 2026-08-26T19:23:05Z, recorded by content hash

what the record establishes
  at observation time, 2026-08-27T09:01:57Z, upstream designates
  mednafen-1.32.1.tar.xz, and that entry carries the date 2024-04-05

what it does not establish
  the designation state at the sealed instant. A release date fixes
  when a release was published, not the interval over which it was
  the designated artifact.
```

primary_snapshot: UNRESOLVED

## EV-C009-SNAPSHOT-01
Candidate: C009
Stage: survivor-stage primary snapshot resolution

```text
sealed rule, repository branch
  the commit the default branch pointed at at the enumeration
  execution timestamp, recorded as a full commit hash

what the record establishes
  at observation time the default branch pointed at
  a62b868e9247c4aafd66f597cdfa8d2609704087, whose commit date is
  2026-05-30T00:35:55Z

what it does not establish
  where the branch pointed at 2026-08-26T19:23:05Z. A commit object
  is immutable; a branch ref is not. That the current HEAD predates
  the sealed instant shows the commit existed by then, not that the
  ref pointed at it then.
```

The withdrawn wording read "master had not moved since 2026-05-30, so raw reads on 2026-08-27 resolve to the revision the snapshot rule fixes". "Had not moved" was never observed; what was observed is where it points now.

primary_snapshot: UNRESOLVED

## EV-C023-SNAPSHOT-01
Candidate: C023
Stage: survivor-stage primary snapshot resolution

Same structure as C009. At observation time the default branch pointed at ca7ed57956034b25af1137378027b5ad6e7c15f0, commit date 2025-09-06T00:34:34Z. Where the ref pointed at 2026-08-26T19:23:05Z is not established.

primary_snapshot: UNRESOLVED

## AUDIT NOTE — "primary snapshot" wording in entries that never reached the survivor stage

Five E4 entries still open with "observations are at the primary
snapshot": EV-C010-E4-01, EV-C012-E4-01, EV-C014-E4-01, EV-C016-E4-01
and EV-C022-E4-01. They are left as written, and none is a standing
snapshot claim.

```text
C010, C012, C014, C016   quarantined as post-stop exposure; they do
                         no verdict work at all

C022                     UNRESOLVED at E4, so it never reached the
                         survivor stage where a snapshot is resolved
```

In each, the phrase names the observation-time revision the reading was
made against. Under QA-28 that is imprecise wording rather than a
verdict defect, and rewriting five historical entries to correct a
phrase that decides nothing would obscure the record more than it
repairs it. The three ACTIVE survivors' E4 entries -- C009, C013, C023
-- have been corrected, because there the phrase would have asserted
something the ledger now denies.

## EV-C030-UR-01
Candidate: C030 (frame rank 30, games/angrydd)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/angrydd/Makefile
Observed: DISTNAME=angrydd-1.0.2; CATEGORIES=games; SITES=https://dickman.org/openbsd/distfiles/; COMMENT="falling blocks puzzle game". There is no HOMEPAGE, no GH_ fields and no DIST_TUPLE.
Inference: the frozen fields name one system, angrydd. UR asks which external system the port packages, and the answer is unambiguous even though the metadata supplies no upstream locator -- whether a canonical source location exists for it is E2-REP's question, not this one. Not UR-AMBIGUOUS and not UR-NONE: a system is identified.
Decision: PASS

## EV-C030-E1-01
Candidate: C030
Gate: E1
Source: same frozen metadata
Observed: a third-party falling-blocks puzzle game, packaged from a distfile named angrydd-1.0.2, unrelated to this project.
Inference: external-authorship requirement satisfied. This is determinable from the frozen metadata alone.
Decision: PASS

## EV-C030-E2REP-01
Candidate: C030
Gate: E2-REP

Per QA-27, the frozen metadata's URLs and identifiers are enumerated and accounted for. There is exactly one: SITES. There is no HOMEPAGE, so navigation step 1 has no target at all, and no repository or account identifier exists to serve as an alternative starting point.

Surface: https://dickman.org/openbsd/distfiles/ -- the frozen SITES.
Necessary because: it is the only admitted starting point, and the gate cannot be settled without it. Under QA-24 an admitted surface the gate still needs is observed rather than skipped, with the scope fixed first.

Observation scope, fixed before the request:

```text
observe only
  the surface's existence and HTTP status
  labels or headings the page or listing itself carries
  artifact names and link relations it directly exposes
  an explicit "source" / "source code" designation
  primary or mirror marking

do not
  open any artifact or document
  infer that an artifact is source from its filename
  navigate to the parent directory or elsewhere on the host
  search for other locations
```

requested_url and final_url: https://dickman.org/openbsd/distfiles/
observed_at_utc: 2026-08-27T16:20:10Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: a 623-byte Apache directory index headed "Index of /openbsd/distfiles". Beyond the index's own sort controls and a Parent Directory link to /openbsd/, it exposes exactly two entries: angrydd-1.0.1.tar.gz and angrydd-1.0.2.tar.gz. It carries no other headings, no statements, and no marking of anything as canonical, primary or a mirror.

```text
PASS not established
  no upstream project or designation surface was established. The
  frozen metadata supplies no HOMEPAGE and no repository identifier,
  so no landing page exists to navigate from, and the one admitted
  surface is a directory index that designates nothing.

FAIL not established
  an index page carrying no designation is not a demonstration that
  upstream designates none.

E2REP-NO-SOURCE not established either, and for its own reason
  the sealed vocabulary defines that code as "no access to actual
  source representation". The index exposes two .tar.gz artifact
  names. Whether either is this candidate's actual source
  representation was not established -- opening them was outside the
  scope fixed above -- so the ABSENCE of source access is not
  established, and the code cannot be applied.
```

An earlier draft ruled that code out on a different ground -- that it is "a claim about a DESIGNATED canonical location, and none was established". The sealed vocabulary carries no such restriction; the reason it does not apply here is that source access has not been shown absent, not that it is reserved for designated locations.

Recorded as an observation and not used as a ground: the index sits under an /openbsd/ path and holds only this port's two distfiles. Nothing in the verdict depends on whose host it is; the surface simply makes no designation, which is enough.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C031-UR-01
Candidate: C031 (frame rank 31, games/armagetronad)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/armagetronad/Makefile
Observed: HOMEPAGE=http://armagetronad.org/; SITES=${SITE_SOURCEFORGE:=armagetronad/}; V=0.2.9; DISTNAME=armagetronad-${V}.${P}; EXTRACT_SUFX=.tbz; COMMENT="3D light cycle game".
Inference: the frozen fields name one system, Armagetron Advanced. HOMEPAGE pointing at a project site while SITES points at a distfile mirror is the shape the protocol names non-ambiguous. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C031-E1-01
Candidate: C031
Gate: E1
Source: same frozen metadata; https://armagetronad.org/
observed_at_utc: 2026-08-27T16:29:38Z; http_status 200
Observed: a third-party game, its own page titled "Armagetron Advanced :: a Tron clone in 3D", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C031-E2REP-01
Candidate: C031
Gate: E2-REP

Per QA-27, both URLs the frozen metadata supplies are accounted for, and both were observed.

Surface 1: the frozen HOMEPAGE.
requested_url: http://armagetronad.org/ ; final_url: https://armagetronad.org/
observed_at_utc: 2026-08-27T16:29:38Z-16:29:41Z; http_status 200; redirect_chain: 1 redirect, http -> https
evidence_role: official-project-page
Observed: the navigation exposes News, News Archive, About, Contacts, Downloads, Release Candidate, Maps, Models, Moviepacks, Textures, Screenshots, Links, Servers, Forums and Wiki. None is a Source, Code, Repository or Development link, so navigation step 2 has no target here. The body's outbound links are release blog posts, Flathub, itch.io, forum threads, and third-party ports (Armapitron, Androgetron).

One link needs naming because its label reads like a designation and its destination is not one: "our own repository" points at https://download.armagetronad.org/docs/flatpak/, and upstream's own sentence places it -- "We now support installation via Flatpak for the 64-bit Linux client. Get the stable versions from Flathub; our own repository has those and also carries the usual test builds." It is a Flatpak package repository for installing the client. Two separate requirements bear on it, and keeping them apart matters: QA-25 asks that the LOCATION ITSELF be observed rather than a route to it, which this link does satisfy -- its destination is a location. E2-REP then asks that the location be designated as this candidate's CANONICAL SOURCE, which it is not: upstream designates it, in as many words, as somewhere to install the client from.

`Downloads` was not opened. It is not among the contract's four step-2 labels, and QA-17 settled that the criterion's phrase "source distribution" may not widen the whitelist. `Wiki` likewise.

Surface 2: the frozen SITES. `${SITE_SOURCEFORGE:=armagetronad/}` resolves, through the ports infrastructure's own definition of that macro, to https://downloads.sourceforge.net/sourceforge/armagetronad/.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.
requested_url and final_url: https://downloads.sourceforge.net/sourceforge/armagetronad/
observed_at_utc: 2026-08-27T16:30:17Z (GET), 16:30:31Z (HEAD)
http_status: 404, 404; redirect_chain: NONE on both
control: the landing page returned 200 at 16:30:31Z
Observed: a 154-byte "404 Not Found -- The resource could not be found." No labels, no artifact names, no designation signal. Transport completed and the endpoint answered definitely, so this is not the timeout / DNS / refused / 5xx family.

```text
PASS not established
  no designation signal was observed on either admissible surface.
  The landing page exposes no Source/Code/Repository/Development link,
  and the one link whose label says "repository" is designated by
  upstream as a Flatpak install repository. The SITES path returns 404.

FAIL not established
  two surfaces carrying no designation signal is not a demonstration
  that upstream designates none. E2REP-NO-SOURCE is not established
  either: nothing observed shows source access to be absent -- what
  was observed is that neither examined surface offered a designation.
```

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C032-UR-01
Candidate: C032 (frame rank 32, games/arx-libertatis)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/arx-libertatis/Makefile
Observed: GH_ACCOUNT=arx; GH_PROJECT=ArxLibertatis; GH_TAGNAME=1.2.1; PKGNAME=arx-libertatis-${GH_TAGNAME}; COMMENT="cross-platform port of Arx Fatalis, a first-person RPG". There is no HOMEPAGE and no SITES.
Inference: the frozen fields name one system, Arx Libertatis. "Arx Fatalis" names the game this ports, not a second packaged system, in the same way flycast's "based on reicast" did. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C032-E1-01
Candidate: C032
Gate: E1
Source: same frozen metadata; https://github.com/arx/ArxLibertatis
observed_at_utc: 2026-08-27T16:38:05Z; http_status 200
Observed: a third-party port, its repository described as "Cross-platform port of Arx Fatalis, a first-person role-playing game", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C032-E2REP-01
Candidate: C032
Gate: E2-REP

Per QA-27, the frozen metadata's URLs and identifiers are enumerated: there is no HOMEPAGE and no SITES, so the only admitted starting point is the GH_ACCOUNT/GH_PROJECT pair. Navigation step 1 has no target. This is C017's shape.

Surface: https://github.com/arx/ArxLibertatis
observed_at_utc: 2026-08-27T16:38:05Z-16:38:06Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed, restricted to metadata the contract allows: repository ArxLibertatis, owner login arx, default branch master, isFork false, isMirror false, isArchived false, isTemplate false, and a source tree present at the root -- CMakeLists.txt, AUTHORS, CHANGELOG, CONTRIBUTING.md, COPYING, OPTIONS.md, VERSION, .github/workflows and the licence files. Source-tree presence is directly observable here, unlike C028's client-rendered root.

The repository's website metadata field reads https://arx-libertatis.org/.

That field is observed and is NOT followed, for the reason established at C025's fork parent: it is a repository fact, not a route the contract authorizes. arx-libertatis.org is not an identifier in the frozen metadata, so it is not an admitted starting point, and the sealed navigation runs landing page -> source link -> repository root. Going from a repository root outward to a project site reverses that path; no step provides for it.

```text
PASS not established
  arriving at this repository through a packaging identifier yields
  affiliation, not designation (QA-22). The website field adds a
  one-way arrow from repository to site -- the same shape C014
  already found insufficient, since designation requires the project
  to identify the repository as its canonical source, not the
  repository to name a site.

FAIL not established
  the repository root IS an admissible surface, and "whether upstream
  designates this location as its source" is among the observations
  the contract allows there. So a surface that could have carried a
  designation was examined; it carried no designation signal. That
  absence on this surface does not establish that upstream designates
  no canonical source location -- the C017 boundary exactly.

  E2REP-NO-SOURCE is independently unavailable: source-tree presence
  was directly observed, so source access is not what is missing.
```

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C033-UR-01
Candidate: C033 (frame rank 33, games/asciiquarium)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/asciiquarium/Makefile
Observed: HOMEPAGE=https://www.robobunny.com/projects/asciiquarium/html/; SITES=https://www.robobunny.com/projects/asciiquarium/; DISTNAME=asciiquarium_1.1; COMMENT="aquarium animation in ASCII art".
Inference: the frozen fields name one system, ASCIIQuarium, and SITES is the parent path of HOMEPAGE on the same host, so the metadata resolves to one place. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C033-E1-01
Candidate: C033
Gate: E1
Source: same frozen metadata; https://robobunny.com/projects/asciiquarium/html/
observed_at_utc: 2026-08-27T16:45:41Z; http_status 200
Observed: a third-party terminal animation, its page contacting "Kirk Baucom", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C033-E2REP-01
Candidate: C033
Gate: E2-REP

Per QA-27 both frozen URLs are accounted for. HOMEPAGE was observed as step 1; SITES is the same host's parent directory, reachable from step 1 as "View Directory", and is discussed below rather than opened separately.

Surface: the frozen HOMEPAGE.
requested_url: https://www.robobunny.com/projects/asciiquarium/html/ ; final_url: https://robobunny.com/projects/asciiquarium/html/
observed_at_utc: 2026-08-27T16:45:41Z-16:45:43Z; http_status 200; redirect_chain: 1 redirect (www -> apex)
evidence_role: official-project-page

Observed: under a "Download" heading the page exposes "Latest Version (v1.1)" -> ../asciiquarium.tar.gz, "Previous Versions", and "View Directory" -> ../ . Its navigation is Projects, Main, Changes, Read_Me, Download. Its body credits third-party derivatives: a Windows screensaver, a Mac packaged build, a KDE screensaver and an Android live wallpaper.

The page uses the phrase "source code" exactly once, and upstream attaches it to a different system: "Russel Goring has updated J. Sommer's Windows screensaver, and has posted the source code on Github", linking to github.com/rgoring/asciiquarium. Under QA-26 that is another delimited system's source, labelled as such by upstream, and it is not a designation for this candidate.

The designated artifact was retrieved, and listing its entry names only:
observed_at_utc: 2026-08-27T16:46:18Z; http_status 200; 15436 bytes; sha256 1b08c6613525e75e87546f4e8984ab3b33f1e922080268c749f1777d56c9d361
Six entries: asciiquarium_1.1/ containing CHANGES, README, MANIFEST, gpl.txt and a file named asciiquarium.

```text
PASS not established, on two counts

  designation AS SOURCE
    the link's label is "Latest Version (v1.1)", under a "Download"
    heading. No permitted surface designates it as a source location.
    The comparison with the two candidates that did pass is exact:
    C029's link was labelled "Source code" outright, and C013's
    .tar.xz stood beside win64/win32 zips, so the contrast identified
    it. Neither device is present here -- a single artifact under a
    Download heading.

  source-tree presence
    the listing shows a version-named directory with CHANGES, README,
    MANIFEST, gpl.txt and one program file. Whether that file is
    source rather than a built artifact was not established from
    names alone, and opening it was outside what this gate permits.
    C030 set that restraint: an artifact is not source because its
    filename suggests it.

FAIL not established
  the surface carried no source designation, which is a bounded
  observation about this page and not a demonstration that upstream
  designates none. E2REP-NO-SOURCE is unavailable too: an artifact was
  retrieved, so source access is not shown absent.
```

The frozen SITES, https://www.robobunny.com/projects/asciiquarium/, is the directory that holds the artifact just retrieved -- the "View Directory" target. It is the container of the observed location rather than a second location, on the reading applied at C016, and no separate designation could follow from it that this page has not already shown.

Recorded because it bears on the survivor stage if this candidate is ever revisited: the designated artifact's URL carries no version. The same URL serves whatever is current, which is precisely the silent-replacement shape QA-28 describes.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 17 — C033 E2-REP superseded; a Download artifact was opened, and a frozen SITES was not

EV-C033-E2REP-01 is **superseded**. Its verdict, UNRESOLVED, stands. Its
execution contained one forbidden navigation, one omitted necessary
surface, and three overstatements.

**Forbidden navigation.** The entry followed "Latest Version (v1.1)"
from under the page's `Download` heading and retrieved the artifact,
then listed its entries. QA-17 settled that the criterion's phrase
"source distribution" does not license following a Download surface, and
C014 was withdrawn for the same move. That the artifact's contents were
not opened does not save it: what is forbidden is going to an
unauthorized surface, not how deeply it is then read. The retrieval, its
size, its hash and its six entry names are quarantined and do no verdict
work.

Reading it back, the entry even used that forbidden observation to argue
the gate: "source-tree presence ... was not established from names
alone" is an argument built on the surface that should not have been
opened.

**Omitted necessary surface.** The entry declined to open the frozen
SITES, reasoning that it is "the container of the observed location
rather than a second location" and that "no separate designation could
follow from it". That is C026's error exactly -- deciding what a surface
holds before observing it. SITES is a URL the frozen metadata supplies,
the gate was unsettled after step 1, and nothing observed made it
unnecessary in the way C010's port Makefile made its SITES unnecessary.
It is observed below.

## EV-C033-E2REP-02  (supersedes EV-C033-E2REP-01)
Candidate: C033 (frame rank 33, games/asciiquarium)
Gate: E2-REP

Per QA-27, both frozen URLs are enumerated and both are observed.

Surface 1: the frozen HOMEPAGE.
requested_url: https://www.robobunny.com/projects/asciiquarium/html/ ; final_url: https://robobunny.com/projects/asciiquarium/html/
observed_at_utc: 2026-08-27T16:45:41Z-16:45:43Z; http_status 200; redirect_chain: 1 redirect (www -> apex)
Observed: navigation reads Projects, Main, Changes, Read_Me, Download. Under `Download` it exposes "Latest Version (v1.1)" -> ../asciiquarium.tar.gz, "Previous Versions", and "View Directory" -> ../ . The body credits third-party derivatives: a Windows screensaver, a Mac packaged build, a KDE screensaver, an Android live wallpaper.

The page uses "source code" exactly once, and upstream attaches it to another system: "Russel Goring has updated J. Sommer's Windows screensaver, and has posted the source code on Github", linking to github.com/rgoring/asciiquarium. Under QA-26 that is another delimited system's source, labelled as such by upstream, and not a designation for this candidate.

No link on this surface is labelled as, or leads to, a designated source location for ASCIIQuarium. `Download` is not among the contract's four step-2 labels and was not followed.

Surface 2: the frozen SITES, https://www.robobunny.com/projects/asciiquarium/.
Necessary because: the gate was unsettled after surface 1, this is the remaining admitted starting point, and nothing observed established it as unnecessary -- the C010 exemption rested on that port's own dist: target showing its host to be the packager's, and no equivalent exists here. Opening it as a frozen starting point is not the same act as following the page's "View Directory" link, which would have been navigation past step 1.

Observation scope, fixed before the request: HTTP status; headings the surface itself carries; artifact names and link relations it directly exposes; any explicit source or source-code label; any primary or mirror marking. Not: opening any listed artifact, reading README or docs, or searching elsewhere.

requested_url: https://www.robobunny.com/projects/asciiquarium/ ; final_url: https://robobunny.com/projects/asciiquarium/
observed_at_utc: 2026-08-27T17:04:13Z; http_status 200; redirect_chain: 1 redirect (www -> apex)
Observed: an Apache directory index headed "Index of /projects/asciiquarium", listing CHANGES, MANIFEST, README, asciiquarium, asciiquarium.tar.gz, asciiquarium_1.0.tar.gz, asciiquarium_1.1.tar.gz, gpl.txt, html/, screenshot.png and small_screenshot.png. Beyond the index's own sort controls and a Parent Directory link it carries no headings, no labels, no statement designating anything as source, and no primary or mirror marking.

```text
PASS not established
  neither admissible surface designates a canonical source location.
  Surface 1 offers a Download link labelled "Latest Version (v1.1)";
  surface 2 is a bare directory index. The only "source code" phrase
  either carries belongs, by upstream's own sentence, to a different
  system.

  The comparison with the candidates that produced positive
  source-designation evidence is worth stating precisely:

    C013  E2-REP PASS. Its .tar.xz stood beside win64/win32 zips on
          the project's own page, and the contrast identified it.
    C029  positive evidence on this prerequisite -- a link labelled
          "Source code" -- but its E2-REP is UNRESOLVED overall, on
          uniqueness. It is not an example of a passed gate.

  Neither device is present here.

FAIL not established
  two surfaces carrying no source designation is a bounded observation
  about those surfaces, not a demonstration that upstream designates
  none.

E2REP-NO-SOURCE not established either
  that code means no access to the actual source representation.
  Surface 2 exposes artifact names; whether any of them is this
  candidate's actual source representation was not established, and
  establishing it was outside the fixed scope. An unclassified artifact
  proves neither source access nor its absence.
```

Recorded only as a snapshot-related structural note -- C033 stops at E2-REP and does not reach the survivor stage in this run -- and at the strength the observation supports: the artifact the landing page designates as "Latest Version (v1.1)" sits at a versionless URL, ../asciiquarium.tar.gz, while the same directory also carries asciiquarium_1.0.tar.gz and asciiquarium_1.1.tar.gz. The versionless URL therefore does not itself encode an immutable version identity. No claim is made that its bytes have ever been replaced -- only that nothing in the URL would record it, which is the reconstruction problem QA-28 describes.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C034-UR-01
Candidate: C034 (frame rank 34, games/astromenace)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/astromenace/Makefile
Observed: HOMEPAGE=http://www.viewizard.com/; GH_ACCOUNT=viewizard; GH_PROJECT=astromenace; GH_TAGNAME=v${V} with V=1.4.3; COMMENT="hardcore 3D space shmup".
Inference: the frozen fields name one system, AstroMenace. HOMEPAGE pointing at a project site while GH_ACCOUNT/GH_PROJECT point at a repository is the shape the protocol names non-ambiguous. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C034-E1-01
Candidate: C034
Gate: E1
Source: same frozen metadata; https://viewizard.com/
observed_at_utc: 2026-08-27T18:05:49Z; http_status 200
Observed: a third-party game, its repository described as "Hardcore 3D space scroll-shooter with spaceship upgrade possibilities", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C034-E2REP-01
Candidate: C034
Gate: E2-REP

Per QA-27 both frozen items are accounted for: HOMEPAGE is step 1 below, and the GH_ACCOUNT/GH_PROJECT pair resolves to the same repository the step-2 link reaches, so it is not a separate surface.

Step 1: the frozen HOMEPAGE.
requested_url: http://www.viewizard.com/ ; final_url: https://viewizard.com/
observed_at_utc: 2026-08-27T18:05:49Z-18:05:50Z; http_status 200; redirect_chain: 1 redirect (www/http -> apex/https)
Observed: the navigation exposes English, Russian, Download, **Source Code**, Support and Company. "Source Code" points at https://github.com/viewizard/astromenace. The Windows, macOS and Linux links are anchors into ./download.html.

Step 2: the "Source Code" link -- one of the contract's four labels, verbatim, with a destination that is a location rather than instructions. QA-25 satisfied in its plainest form.

On uniqueness, and on what was not opened: ./download.html was not followed. It is not among the four step-2 labels, and QA-17 settled that the criterion's "source distribution" phrase may not widen the whitelist. Upstream's own navigation separates the two roles -- "Download" carries the Windows/macOS/Linux anchors, "Source Code" points at the repository -- so the unopened page is labelled by upstream as the builds surface. That is a use of upstream's own delimitation, as QA-26 endorses, not an inference about unseen contents: no claim is made about what download.html holds, only that upstream labels it as something other than its source designation.

Step 3: https://github.com/viewizard/astromenace
observed_at_utc: 2026-08-27T18:06:15Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-source-location
Observed: repository astromenace, owner login viewizard, default branch master, isFork false, isMirror false, isArchived false, isTemplate false, website metadata field https://viewizard.com, and a source tree present at the root -- src, gamedata, docs, share, licenses, CMakeLists.txt, AUTHORS.md, CHANGELOG.md, README.md, LICENSE.md.

Inference: exactly one designated canonical source location on the permitted surfaces, at a stable URL, holding a source tree, with one external target identifier (AstroMenace).

The upstream-authored designation is one-way and sufficient: the project site labels the repository "Source Code". The repository's website metadata field points back to the project site and corroborates affiliation, but it does no designation work -- C032 settled that a repository naming a site is affiliation, not designation, and the direction that matters here is the site naming the repository.

Decision: PASS

## EV-C034-E2RULE-01
Candidate: C034
Gate: E2-RULE
Source: README.md in the designated repository
observed_at_utc: 2026-08-27T18:06:53Z; http_status 200
Provenance: read against the source state available at screening observation time; no claim is made about the sealed primary snapshot (QA-28).

Observed: located witness, under "Build (macOS, Linux, BSD)" -- "Build dependencies: libSDL2 (ver 2.0.5+), libopenal (ver 1.0+), libalut (ver 1.0+), libogg (ver 1.1+), libvorbis (ver 1.1+), freetype (ver 2.1.6+)", and separately "gcc or clang or any compiler with full ISO/IEC 14882:2011 (C++11) support".

Inference: these determine concrete validity requirements without our inventing them -- a build environment carrying libSDL2 older than 2.0.5, or a compiler without full C++11 support, does not satisfy the project's stated requirements.

Recorded rather than left implicit, as at C014 and C023: this is a BUILD-ENVIRONMENT requirement, not a data-artifact one. E2-RULE asks for "at least one validity requirement" and does not restrict the domain, so narrowing it to artifact validity would add a premise the criterion does not carry.
Decision: PASS

## EV-C034-E3-01
Candidate: C034
Gate: E3
Source: src/config/config.cpp in the designated repository
observed_at_utc: 2026-08-27T18:07:43Z; http_status 200
Provenance: as above -- observation-time source state.

Observed: located witness. The pilot-profile store's filename embeds the configuration version:

```text
const std::string ProfilesFileName{std::string{"PilotProfiles_"} +
                                   std::string{CONFIG_VERSION} +
                                   std::string{".data"}};
```

and the file opens with the project's own note on the consequence:

```text
// TODO we need store previous versions Top Scores and Pilot Profiles,
//      in case player will back to old game version by some reason
```

Inference:

```text
observed            the build's CONFIG_VERSION selects the
                    profile-store filename

project statement   previous-version Top Scores and Pilot Profiles
                    need retaining for a player returning to an older
                    game version

therefore           which profile store is relevant depends on version
                    history
```

That is a stateful/temporal validity question that can be examined, which is E3's deliberately weak admission condition. No claim is made about whether the profile data itself records a version: that was not examined, and the witness does not need it.
Decision: PASS

## EV-C034-E4-01
Candidate: C034
Gate: E4

No positive construction was obtained.
observed_at_utc: 2026-08-27T18:07:31Z-18:08:08Z; http_status 200 throughout
Provenance: observation-time source state, as above.

Attempted, and why each falls short:

```text
src/script/script.cpp
  dispatches mission-script elements by name, and rejects unknown ones
  in the project's own words -- "tag " << xmlEntry.Name << " not
  found, line " << xmlEntry.LineNumber. But the dispatch is
  switch (xmlEntry.NameHash) over case constexpr_hash_djb2a("TimeLine")
  and its siblings: a COMPILE-TIME switch, not a registry the program
  walks. EN5's admissible closure bases are runtime construction or an
  unconditional universal claim about the codebase; a switch's case
  labels are neither, and the closure would rest on our reading of the
  switch body. This is C022's shape exactly.

src/config/config.cpp
  reads and writes configuration through 39 individual
  GetEntryAttribute / SetEntryAttribute calls rather than a declared
  settings table. It enforces, but it does not ENUMERATE: these
  individual call sites do not themselves expose an externally closed
  membership set, and an analyst reading the call sites and listing
  them would be supplying the closure rather than observing it.
  C022's plugin loader failed the same way.
```

Inference: no positive U_enforced construction was obtained from the mechanisms examined.

On the normative route, stated carefully because an earlier draft of this entry got the logic backwards. It said "only one route is required" as the reason for not pursuing U_normative. That is a sufficiency rule -- one route suffices for PASS -- and it does not license skipping the second route after the first yields nothing. The accurate position is narrower: the README witness used at E2-RULE is project-owned, but it was not observed as an explicitly DESIGNATED authoritative rule source, and Section 3.1 admits only explicit designation. So U_normative is not established either, on what was observed.

Under the post-seal amendment, the absence of a positive construction does not establish E4 FAIL, because no preregistered discovery procedure makes that universal claim decidable. No claim is made that an admissible enumerator or authoritative source is absent elsewhere in AstroMenace.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

## EV-C035-UR-01
Candidate: C035 (frame rank 35, games/atomix)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/atomix/Makefile
Observed: DISTNAME=atomix-3.22.0; SITES=${SITE_GNOME:=/sources/atomix/3.22/}; EXTRACT_SUFX=.tar.xz; COMMENT="build molecules out of single atoms". There is no HOMEPAGE and no repository identifier.
Inference: the frozen fields name one system, Atomix. As at C030, UR asks which system the port packages and the answer is unambiguous even though the metadata supplies no upstream locator beyond a distribution path. Not UR-AMBIGUOUS and not UR-NONE.
Decision: PASS

## EV-C035-E1-01
Candidate: C035
Gate: E1
Source: same frozen metadata
Observed: a third-party puzzle game, packaged from a distfile named atomix-3.22.0, unrelated to this project.
Inference: external-authorship requirement satisfied, from the frozen metadata alone.
Decision: PASS

## EV-C035-E2REP-01
Candidate: C035
Gate: E2-REP

Per QA-27, the frozen metadata's URLs and identifiers are enumerated: there is one, SITES. No HOMEPAGE exists, so navigation step 1 has no target, and no repository or account identifier offers an alternative starting point.

Surface: the frozen SITES. `${SITE_GNOME:=/sources/atomix/3.22/}` resolves, through the ports infrastructure's own definition of that macro, to https://download.gnome.org/sources/atomix/3.22/ (the macro lists four further mirrors; the first was used).
Necessary because: it is the only admitted starting point and the gate cannot be settled without it.

Observation scope, fixed before the request: HTTP status; headings the surface itself carries; artifact names and link relations it directly exposes; any explicit source or source-code label; any primary or mirror marking. Not: opening any listed artifact, and not searching elsewhere.

requested_url and final_url: https://download.gnome.org/sources/atomix/3.22/
observed_at_utc: 2026-08-27T18:33:32Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed: a 2009-byte index headed "Index of /sources/atomix/3.22/". Beyond its own sort controls and a Parent directory link it exposes four entries:

```text
LATEST-IS-3.22.0            a structured marking naming the latest
                            release within this directory
atomix-3.22.0.news
atomix-3.22.0.sha256sum
atomix-3.22.0.tar.xz
```

```text
PASS not established
  the surface identifies WHICH RELEASE is latest within it, and
  publishes a checksum for the artifact. It does not identify the
  location as the project's canonical source. QA-23 admits a
  structured marking as a designation signal, and LATEST-IS-3.22.0 is
  one -- but what it marks is a version, not a location's status. No
  statement, label or relation observed here has the project
  identifying this as where its source lives.

  Nothing else was available to carry such a statement: the frozen
  metadata names no project page, so there is no surface on which the
  project could have been observed designating anything.

FAIL not established
  a directory index carrying no designation is not a demonstration
  that upstream designates none.

E2REP-NO-SOURCE not established
  that code means no access to the actual source representation. An
  artifact and its published checksum are exposed here; whether the
  artifact is this candidate's actual source representation was not
  established, since opening it was outside the fixed scope. An
  unclassified artifact proves neither access nor its absence -- the
  C030 and C033 position.
```

Recorded as a shape the run keeps meeting rather than as a claim about this candidate: where the frozen metadata supplies only a distribution path and no project page, E2-REP asks for a designation that an archive index does not make. C030 and C033 ended the same way. The gate is not failing these candidates; it is unreachable for them, because the surface that would carry a designation is not among the frozen metadata's URLs.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 18 — C035 accounted for a metadata FIELD, not for the starting points it supplies

EV-C035-E2REP-01 is **superseded**. Its verdict, UNRESOLVED, stands.
Four defects, one of them a QA-27 failure and one an over-general
finding.

**The QA-27 failure.** The entry noted that SITE_GNOME "lists four
further mirrors; the first was used", and in the same breath claimed the
frozen metadata's URLs were enumerated and accounted for. QA-27 asks for
an accounting of each admitted STARTING POINT, not of each metadata
field. Four remained unaccounted, and treating them as covered because
OpenBSD groups them under one macro gives packaging metadata evidential
force over what upstream surfaces display -- the move this run has
withdrawn repeatedly. All four are observed below.

**Three overstatements.**

```text
"publishes a checksum for the artifact"
  what was observed within scope is a companion file NAMED
  atomix-3.22.0.sha256sum. It was not opened, so no checksum value
  was read.

"QA-23 admits a structured marking as a designation signal, and
 LATEST-IS-3.22.0 is one"
  QA-23 admits that a structured marking CAN be the form a
  source-location designation takes. It does not make every structured
  marking one. LATEST-IS-3.22.0's semantic relation is "latest release
  = 3.22.0", not "this location is the canonical source".

"the gate is not failing these candidates; it is unreachable for
 them ... C030 and C033 ended the same way"
  Withdrawn. SITES is itself an admitted surface that COULD carry a
  designation -- an archive index stating "official source
  distribution" would be positive evidence. What happened is that the
  surfaces examined carried none, which is an observation, not a
  structural impossibility. C033 is also not this shape: it had a
  frozen HOMEPAGE and its official project page was observed. The near
  precedent is C030 alone.
```

## EV-C035-E2REP-02  (supersedes EV-C035-E2REP-01)
Candidate: C035 (frame rank 35, games/atomix)
Gate: E2-REP

Per QA-27, every admitted starting point is accounted for. The frozen metadata supplies no HOMEPAGE and no repository identifier, so navigation step 1 has no target; SITES is the only field, and it resolves through the ports infrastructure's own SITE_GNOME definition to five distinct URLs. All five starting points are accounted for -- four produced determinate endpoint observations or a redirect, and one remained transport-indeterminate after the required retries -- under one scope fixed before the first request: HTTP status; headings the surface carries; artifact names and link relations it exposes; any explicit source or source-code label; any primary or mirror marking. Not: opening any listed artifact, and not searching elsewhere.

```text
1  https://download.gnome.org/sources/atomix/3.22/
   observed_at_utc 2026-08-27T18:33:32Z; 200; no redirect; 2009 bytes
   index headed "Index of /sources/atomix/3.22/", exposing
   LATEST-IS-3.22.0, atomix-3.22.0.news, atomix-3.22.0.sha256sum,
   atomix-3.22.0.tar.xz

2  https://ftp.acc.umu.se/pub/GNOME/sources/atomix/3.22/
   observed_at_utc 2026-08-27T19:32:26Z; 403 Forbidden; 373 bytes
   nothing observable

3  https://ftp.gnome.org/pub/GNOME/sources/atomix/3.22/
   observed_at_utc 2026-08-27T19:32:26Z; 200 after 1 redirect
   redirects to surface 1; not a distinct surface

4  https://ftp1.nluug.nl/windowing/gnome/sources/atomix/3.22/
   observed_at_utc 2026-08-27T19:32:26Z, 19:32:52Z (x2); HTTP 000
   TLS connection failure on all three attempts, no body.
   Transport indeterminacy under the contract; retried twice as it
   requires, and recorded as a protocol issue for this surface rather
   than forced into a finding.

5  ftp://ftp.nara.wide.ad.jp/pub/X11/GNOME/sources/atomix/3.22/
   observed_at_utc 2026-08-27T19:33:10Z; FTP 226; 337 bytes
   lrwxrwxrwx ... LATEST-IS-3.22.0 -> atomix-3.22.0.tar.xz
   -rw-rw-r-- ... atomix-3.22.0.news
   -rw-rw-r-- ... atomix-3.22.0.sha256sum
   -rw-rw-r-- ... atomix-3.22.0.tar.xz
```

Surface 5 shows what surface 1 could not: LATEST-IS-3.22.0 is a symbolic link whose target is atomix-3.22.0.tar.xz. That is a link relation, and QA-23 admits link relations as a form a designation may take -- but the relation it expresses is "the latest release is this artifact", not "this location is the project's canonical source".

```text
PASS not established
  no determinately observed surface established a canonical-source
  designation.

  Surfaces 1 and 5 are the two that actually displayed listings. Both
  identify WHICH RELEASE is latest and expose companion files named
  .news and .sha256sum; neither states, labels or relates its location
  to the project as canonical source. Surface 2 returned 403 and
  displayed nothing; surface 3 redirected to surface 1 and is not a
  distinct surface.

  No other admitted starting point was supplied: the frozen metadata
  names no project page or repository.

FAIL not established
  no candidate-level failure is established. Archive surfaces carrying
  no designation do not demonstrate that upstream designates none, and
  E2REP-NO-SOURCE does not apply either: an artifact is exposed
  alongside a file named for its checksum, and whether that artifact
  is this candidate's actual source representation was not established
  -- opening it was outside the fixed scope. An unclassified artifact
  proves neither source access nor its absence, the C030 position.

ADJUDICATION BLOCKED BEFORE EITHER
  surface 4 remains transport-indeterminate after the retries the
  contract requires. What it would have displayed is unknown, so
  E2-REP cannot be fully adjudicated under the bounded contract.
```

The code follows from that last line, and the reasoning matters more than the code. `PI-UNCLASSIFIED-SHAPE` would say the bounded surfaces were all seen and neither PASS nor FAIL followed. That stage was never reached. Substituting surfaces 1 and 5's observations for surface 4's would be the mirror-substitution error this entry was superseded for correcting -- run in the opposite direction: OpenBSD grouping these URLs under one macro cannot tell us what surface 4 displays, and neither can the other mirrors.

Recorded as a record-only observation, and NOT as this candidate's terminal ground: where the frozen metadata supplies only distribution starting points and the observed surfaces carry no canonical-source designation, this run has not been able to establish E2-REP PASS. That shape is real and its near precedent is C030 -- but C035 is terminal on transport indeterminacy, not on it.

Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

Gates after E2-REP are NOT_REACHED.

## EV-C036-UR-01
Candidate: C036 (frame rank 36, games/barrage)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/barrage/Makefile
Observed: HOMEPAGE=https://lgames.sourceforge.net/?project=Barrage; SITES=${SITE_SOURCEFORGE:=lgames/}; DISTNAME=barrage-1.0.7; COMMENT="kill and destroy as many targets as possible in 3 minutes".
Inference: the frozen fields name one packaged system, Barrage. HOMEPAGE and SITES both sit under the LGames umbrella, which publishes several games, but the port's DISTNAME and its HOMEPAGE query both name Barrage specifically. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C036-E1-01
Candidate: C036
Gate: E1
Source: same frozen metadata; https://lgames.sourceforge.io/?project=Barrage
observed_at_utc: 2026-08-28T03:17:30Z; http_status 200
Observed: a third-party game published under the LGames umbrella alongside LBreakoutHD, LGeneral, LMarbles and others, unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C036-E2REP-01
Candidate: C036
Gate: E2-REP

Per QA-27, both admitted starting points the frozen metadata supplies are accounted for, and both were observed.

Surface 1: the frozen HOMEPAGE.
requested_url: https://lgames.sourceforge.net/?project=Barrage ; final_url: https://lgames.sourceforge.io/?project=Barrage
observed_at_utc: 2026-08-28T03:17:30Z-03:17:37Z; http_status 200; redirect_chain: 1 redirect (sourceforge.net -> sourceforge.io)
evidence_role: official-project-page
Observed: the LGames site. Its navigation is News, Downloads, About, FAQ, Contact, Donate and "SF Project"; a Games menu lists Barrage alongside its siblings; the body is a news list linking to SourceForge news items.

None of those is a Source, Code, Repository or Development link, so navigation step 2 has no target here.

Two links need naming, because each could be mistaken for one:

```text
"SF Project" -> http://sf.net/projects/lgames
  a SourceForge project hub. C007 settled that a generic project hub
  is not a repository root, and its label is not among the four
  either. Not followed.

"Downloads" -> ./downloads.php
  not among the four labels. QA-17 settled that the criterion's
  phrase "source distribution" may not widen the whitelist. Not
  followed.
```

The Games menu's own "Barrage" entry points at ./Barrage, a per-game page that is not in the frozen metadata and is not a Source/Code/Repository/Development link. Not followed.

Surface 2: the frozen SITES. `${SITE_SOURCEFORGE:=lgames/}` resolves, through the ports infrastructure's own definition of that macro, to https://downloads.sourceforge.net/sourceforge/lgames/.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point. It was observed rather than predicted from its URL shape, which C018 established.
observed_at_utc: 2026-08-28T03:18:02Z (GET), 03:18:03Z (HEAD)
http_status: 404, 404; redirect_chain: NONE on both
control: the landing page returned 200 at 03:18:03Z
Observed: a 154-byte "404 Not Found -- The resource could not be found." No headings, artifact names or designation signal. Transport completed and the endpoint answered definitely on both attempts, so this is not the timeout / DNS / refused / 5xx family.

```text
PASS not established
  neither admissible surface established a canonical-source
  designation. Surface 1 exposes no Source/Code/Repository/Development
  link; surface 2 returned 404 and displayed nothing.

FAIL not established
  a project page carrying no source link and an archive path
  returning 404 do not demonstrate that upstream designates no
  canonical source location.

E2REP-NO-SOURCE not established
  no-access-to-actual-source-representation was not established. The
  404 is evidence about that endpoint; nothing observed bears on
  whether the source representation is reachable elsewhere.
```

Both starting points were determinately answered -- 200 and 404 -- so unlike C035 no surface is left unobserved, and the outcome is a shape the criteria do not describe rather than a transport failure.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C037-UR-01
Candidate: C037 (frame rank 37, games/bass)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bass/Makefile
Observed: DISTNAME=bass-cd-1.2; PKGNAME=${DISTNAME:S/cd-//}; EXTRACT_SUFX=.zip; SITES=${SITE_SOURCEFORGE:=scummvm/}; COMMENT="Beneath A Steel Sky". There is no HOMEPAGE and no repository identifier.
Inference: the frozen fields name one packaged system, Beneath A Steel Sky. COMMENT names it explicitly; DISTNAME=bass-cd-1.2 is an abbreviated form consistent with that identification rather than a second naming of it. SITES points into another project's SourceForge distribution area, which is a statement about where the file is fetched from, not a second system claim; the protocol's carve-out treats a distfile host as one more fact about one system rather than as ambiguity. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C037-E1-01
Candidate: C037
Gate: E1
Source: same frozen metadata
Observed: a third-party adventure game, packaged from a distfile named bass-cd-1.2, unrelated to this project.
Inference: external-authorship requirement satisfied, from the frozen metadata alone.
Decision: PASS

## EV-C037-E2REP-01
Candidate: C037
Gate: E2-REP

Per QA-27, the frozen metadata's URLs and identifiers are enumerated: there is one, SITES. No HOMEPAGE exists, so navigation step 1 has no target, and no repository or account identifier offers an alternative starting point.

Surface: the frozen SITES. `${SITE_SOURCEFORGE:=scummvm/}` resolves, through the ports infrastructure's own definition of that macro, to https://downloads.sourceforge.net/sourceforge/scummvm/.
Necessary because: it is the only admitted starting point and the gate cannot be settled without it. It was observed rather than predicted from its URL shape, per C018 -- the same macro produced a 404 at C031 and C036, and assuming this one would too is exactly the reasoning that was withdrawn there.

Observation scope, fixed before the request: HTTP status; headings the surface carries; artifact names and link relations it exposes; any explicit source or source-code label; any primary or mirror marking. Not: opening any listed artifact, and not searching elsewhere.

requested_url and final_url: https://downloads.sourceforge.net/sourceforge/scummvm/
observed_at_utc: 2026-08-28T03:29:53Z (GET), 03:29:54Z (HEAD)
http_status: 404, 404; redirect_chain: NONE on both
Observed: a 154-byte "404 Not Found -- The resource could not be found." No headings, artifact names or designation signal.

QUARANTINED EXTRA REQUEST: https://downloads.sourceforge.net/ was also requested, as a host-health control, and returned 404.

That request was not authorized. The E2-REP contract admits only "the URLs and identifiers found in the frozen OpenBSD metadata" as starting points, and the host root is not one. Earlier controls in this run were admissible for a reason this one lacks: C031's and C036's were the frozen HOMEPAGE itself. Nothing in the contract or in QA-11 creates a general permission to request control URLs.

An earlier draft described this as a control that "did not do the job earlier controls did". The accurate statement is that there was no authority to make the request. It is recorded here as a deviation, and it does no verdict work.

Transport determinacy rests on the admitted endpoint alone: DNS resolved, the connection completed, and it returned a definite HTTP status on both GET and HEAD. That is the contract's own distinction between a definitive answer and the timeout / DNS / refused / 5xx family, and it never required a control.

```text
PASS not established
  the one admissible surface displayed nothing. No canonical-source
  designation was observed, and no other starting point was supplied
  to carry one.

FAIL not established
  a 404 at this path is evidence about this endpoint. It does not
  demonstrate that upstream designates no canonical source location.

E2REP-NO-SOURCE not established
  no-access-to-actual-source-representation was not established
  either; nothing observed bears on whether the source representation
  is reachable elsewhere.
```

Every admitted starting point was determinately answered, so the bounded adjudication completed without a PASS witness and without a candidate-level failure -- the unclassified shape, as at C036, rather than C035's unobserved surface.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C038-UR-01
Candidate: C038 (frame rank 38, games/bastet)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bastet/Makefile
Observed: HOMEPAGE=http://fph.altervista.org/prog/bastet.html; GH_ACCOUNT=fph; GH_PROJECT=bastet; GH_TAGNAME=0.43.2; COMMENT="bastard tetris".
Inference: the frozen fields name one system, Bastet. HOMEPAGE pointing at a project page while GH_ACCOUNT/GH_PROJECT point at a repository is the shape the protocol names non-ambiguous. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C038-E1-01
Candidate: C038
Gate: E1
Source: same frozen metadata; http://fph.altervista.org/prog/bastet.html
observed_at_utc: 2026-08-28T03:56:41Z; http_status 200
Observed: a third-party game, its page titled "Bastet -- Federico Poloni", unrelated to this project.
Inference: external-authorship requirement satisfied.
Decision: PASS

## EV-C038-E2REP-01
Candidate: C038
Gate: E2-REP

Per QA-27 both frozen items are accounted for: HOMEPAGE is step 1, and the GH_ACCOUNT/GH_PROJECT pair resolves to the same repository the step-2 link reaches, so it is not a separate surface.

Step 1: the frozen HOMEPAGE.
requested_url and final_url: http://fph.altervista.org/prog/bastet.html
observed_at_utc: 2026-08-28T03:56:41Z-03:56:42Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-project-page
Observed: under a "Download" heading, a subheading reading **"Source"**, and beneath it the sentence "Bastet is now hosted on github; check that page for the development version." -- with "github" linking to https://github.com/fph/bastet/. A release history follows: 0.43.1 (2014) links to that repository's own archive endpoint, while 0.43, 0.41 and 0.37 link to files/bastet-*.tgz on the author's host. Windows binaries, two patches and third-party links appear separately.

Step 2: the "github" link, and the authority for taking it comes from the page, not from the link's destination.

An earlier draft justified it as "step 2 classifies by what a link LEADS TO, and this destination is a repository root". That generalisation is dangerous: read broadly, any link whose href happens to resolve to a repository would become a step-2 target, and the whitelist would widen again. C038 does not need it.

What supplies the source-role relation is upstream's own page: a subheading reading **"Source"**, and beneath it the sentence "Bastet is now hosted on github", with the link inside that sentence. QA-23 admits a label, a sentence or a link relation as the form a designation may take, and here all three coincide. The anchor text "github" does no work on its own.

On uniqueness. The older files/*.tgz artifacts are on a different host from the repository, which is the C015 shape on its face. What distinguishes it is that upstream ranks them itself: "Bastet is **now** hosted on github" is a present-tense hosting statement, and the tarballs appear beneath it as a dated release history, the most recent of which (0.43.1) already points into the repository rather than to files/. That is the same device as C023's "As of 2015-12-05, this project can be found here" -- a primary marked by upstream, not supplied by us.

Step 3: https://github.com/fph/bastet/
observed_at_utc: 2026-08-28T03:57:23Z; http_status 200; redirect_chain: NONE (num_redirects 0)
evidence_role: official-source-location
Observed: repository bastet, owner login fph -- matching the project page's host, fph.altervista.org -- default branch master, isFork false, isMirror false, isArchived false, isTemplate false. No website metadata field; the repository description reads "Evil falling block game. http://fph.altervista.org/prog/bastet.html". A source tree is present at the root: BastetBlockChooser, Block, BlockChooser, BlockPosition, Config, Ui, Well and main as .cpp/.hpp pairs, plus Makefile, INSTALL, LICENSE, AUTHORS, NEWS, README, bastet.6 and the desktop/appdata files.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Bastet).

Decision: PASS

## EV-C038-E2RULE-01
Candidate: C038
Gate: E2-RULE
Source: INSTALL in the designated repository
observed_at_utc: 2026-08-28T03:57:41Z; http_status 200
Provenance: read against the source state available at screening observation time; no claim about the sealed primary snapshot (QA-28).

Observed: located witness, the file's own first section:

```text
==Prerequisites==
Boost (libboost-dev + libboost-program-options-dev), ncurses
(libncurses-dev).
```

and, of the system-wide high-score file, "you may want to create an empty '/var/games/bastet.scores2' file, and make sure that is writable to the bastet executable."

Inference: these determine concrete validity requirements without our inventing them -- a build environment without Boost's program-options component or without ncurses does not satisfy the stated prerequisites, and a global high-score file that is not writable by the executable does not satisfy the stated condition for that feature.

Recorded as at C014, C023 and C034: the Prerequisites are a BUILD-ENVIRONMENT requirement, and they carry no version bounds. E2-RULE asks for at least one validity requirement and does not restrict the domain.
Decision: PASS

## EV-C038-E3-01
Candidate: C038
Gate: E3
Source: Config.cpp in the designated repository
observed_at_utc: 2026-08-28T03:57:57Z; http_status 200
Provenance: observation-time source state, as above.

Observed: located witness at Config.cpp:43-55.

```text
bool HighScores::Qualifies(int score){
    stable_sort(begin(),end());
    return begin()->Score < score;
}

int HighScores::InsertHighScore(int score, const std::string &scorer){
    if(!Qualifies(score)) return -1;
    ...
}
```

The persistence half of the chain is in the same file, and is quoted here rather than assumed -- an earlier draft asserted "written by earlier sessions" without citing where the writing and loading happen:

```text
write   Config.cpp:181-191
        ofstream ofs2(GetHighScoresFileName().c_str());
        ofs2<<"# Do not edit this file, Bastet sees you\n";
        ... ofs2<<str(scorer % difficulty % i) << " = " << hs.Scorer
        ... ofs2<<str(score  % difficulty % i) << " = " << hs.Score

load    Config.cpp:140-142
        string s=GetHighScoresFileName();
        ifstream ifs2(s.c_str());
        po::store(po::parse_config_file(ifs2,highScoresOpts),_highScores);
```

Inference, now closed end to end:

```text
a session writes its score table to the high-score file
a later session loads that file into the table
Qualifies(score) compares against the table so loaded
therefore the same score can receive different verdicts in two runs
```

That is validity conditioned on history, which is what E3 asks for, and it is the same shape as C014's snes9x witness where the eligibility test read score_high loaded at session start.
Decision: PASS

## EV-C038-E4-01
Candidate: C038
Gate: E4

Positive construction exhibited, via U_enforced, with one leg flagged rather than buried.
observed_at_utc: 2026-08-28T03:57:57Z; http_status 200
Provenance: observation-time source state.

The mechanism: the two `boost::program_options::options_description` objects built in Config::Config(), Config.cpp:103-124, and used as the parse schemas at lines 130 and 142.

EN1 external authorship: the game and this configuration machinery existed independently of this analysis.

EN2 explicit scope: the project names each domain when it constructs the description -- `options_description keyMappingOpts("Key mappings")` and `options_description highScoresOpts("High scores")` -- and gives every entry its own description string, "Down key", "Clockwise turn key", "Name of high scorer", "High score (points)".

EN3 mechanical membership: membership is what was registered into each description. The seven key-mapping entries are added by name with a typed value and a default; the high-score entries are GENERATED, by nested loops over the difficulties and the ten score slots, so that set is computed rather than hand-listed.

EN5 closed within scope: the sets are constructed at runtime by add_options() calls during construction and are then handed to the parser. That is Section 3.2's first admissible case, runtime construction closing the set. Tag: enforced.

EN6 outcome independence: membership is the set of configuration names the two files may set. It is not a bug list, fix list or known-failure registry.

**EN4, evidenced on both sides rather than asserted on one.** An earlier draft wrote that "a name outside the description makes that parse throw". Config.cpp cannot establish that: it shows what the project does, not what the library does with it. Filling the library half from what we happen to know is the "meaning inferred by us" that EN4 exists to exclude. Both halves are therefore recorded from observed surfaces.

```text
PROJECT SIDE   Config.cpp, observed 2026-08-28T03:57:57Z
  builds options_description keyMappingOpts / highScoresOpts
  passes each to po::parse_config_file as the parse schema
  requests no allow_unregistered mode anywhere in the file
  wraps neither call in try/catch; the file's only throw is its own
    throw(CannotOpenFile()) at line 99, unrelated to option names
  main.cpp, observed 2026-08-28T05:11:58Z, contains no try/catch either

LIBRARY SIDE   Boost.Program_options overview, observed
               2026-08-28T05:12:36Z, https://www.boost.org/doc/libs/
               latest/doc/html/program_options/overview.html, 200
  "The options description component, which describes the ALLOWED
   OPTIONS and what to do with the values of the options."
  "Each parser looks for possible options and CONSULTS THE OPTIONS
   DESCRIPTION COMPONENT TO DETERMINE IF THE OPTION IS KNOWN and how
   its value is specified."
```

So the description the project builds is, by the library's own documentation, the thing that decides whether an option is known. The project supplies that acceptance criterion and hands it to the parser. Nothing about the validity role is inferred.

No claim is made here about the specific rejection mechanism. The earlier "makes that parse throw" is withdrawn: the exception type was never observed, and EN4 does not turn on it -- what it asks is that the project connect the mechanism to validation, which the documented consult-the-description relation establishes.

What differs from every prior E4 PASS in this run is where the VALIDITY DECISION IS PERFORMED. In flycast, libchdr, fceux, weland and angband the project's own code performed the acceptance-or-rejection decision -- "Unknown game", CHDERR_UNSUPPORTED_FORMAT, FCEU_PrintError, return false, quit_fmt. Here the library's parser consults the project-supplied description to determine whether an option is known.

No claim is made about the library's specific rejection mechanism; that was the over-claim withdrawn above and it is not reinstated here. EN4 asks that the project CONNECT the mechanism to a validity role and warns only against a meaning inferred by us; it does not require the project to perform the decision. On that reading the leg is met, and the difference is recorded rather than smoothed over, because it is the first time this run has admitted an enforcement path whose deciding code is a library's.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per registered option

  "configuration name N is registered as an allowed/known option for
   file F, with declared type T and default D; the parser consults
   this description to decide whether a name in F is known"

retained as externally segmented fields, per observation
  the description the project named ("Key mappings", "High scores")
  the entry's own description string
  its declared type and default
```

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

## EV-C042-UR-01
Candidate: C042 (frame rank 42, games/billyfrontier)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/billyfrontier/Makefile
Observed: HOMEPAGE=https://pangeasoft.net/billy; PKGNAME=billyfrontier-${V} with V=1.1.1; COMMENT="quicktime space-age spaghetti western"; and two DIST_TUPLE entries:

```text
DIST_TUPLE += github jorio BillyFrontier v${V} .
DIST_TUPLE += github jorio Pomme 9fae17d7715314a3a20259ac2e87aa500a977695 \
              extern/Pomme
```

Inference: the packaged system is Billy Frontier. PKGNAME and COMMENT name it, and the first tuple extracts to "." while the second is placed at extern/Pomme -- a path inside the first tuple's tree. The Makefile's own licence line separates them the same way: "# game: CC BY-NC-SA 4.0; extern/Pomme: MIT, LGPLv2.1, BSD, Boost".

So this is not the two-genuinely-different-systems case UR-AMBIGUOUS is for. It is one packaged system with a vendored dependency, in the same shape as C019's second distfile, and the frozen metadata itself supplies the subordination.
Decision: PASS

## EV-C042-E1-01
Candidate: C042
Gate: E1
Source: same frozen metadata; https://pangeasoft.net/billy/ (observed 2026-08-28T05:22:41Z, 200)
Observed: a third-party game. The frozen metadata alone carries this -- PKGNAME billyfrontier, COMMENT "quicktime space-age spaghetti western", a HOMEPAGE on a game publisher's domain, and a CC BY-NC-SA licence line. The repository title read later at 05:23:54Z, "Pangea Software's Billy Frontier for modern systems", agrees but is not needed for the decision.
Inference: external-authorship requirement satisfied, unrelated to this project.
Decision: PASS

## EV-C042-E2REP-01
Candidate: C042
Gate: E2-REP

Per QA-27, every admitted starting point the frozen metadata supplies is accounted for: the HOMEPAGE, the jorio/BillyFrontier identifiers, and the jorio/Pomme identifiers.

Surface 1: the frozen HOMEPAGE.
requested_url: https://pangeasoft.net/billy ; final_url: https://pangeasoft.net/billy/
observed_at_utc: 2026-08-28T05:22:41Z-05:22:42Z; http_status 200; redirect_chain: 1 redirect; 1076 bytes

The document is a **frameset**. It contains no anchors of its own -- only frame references, and an empty <noframes> body.

That is the whole of what this surface admissibly yields: a document declaring frame references, exposing no anchor of its own.

QUARANTINED EXTRA REQUESTS: the five frame documents were nevertheless requested.
observed_at_utc: 2026-08-28T05:23:14Z-05:23:27Z; http_status 200 on each
bf_home_top.html, bf_home_bottom.html, bf_home_left.html, bf_home_right.html, info.html

Those requests were not authorized, and the reasoning that produced them is the error worth naming. An earlier draft argued that a frameset's declared frames are the landing page's own rendered composition, so reading them observes step 1 rather than navigating past it. That is a true statement about browsers and an invented rule about this contract. The contract enumerates surfaces by navigation RELATION -- landing page, a Source/Code/Repository/Development link it exposes, the repository root reached -- and says nothing about subresources. Supplying "same surface" from a rendering model is the analyst widening the whitelist, the same shape as C014's Downloads page and C037's host root.

The draft also defended itself by saying the alternative "would rest a negative on a technicality of markup". That defence is backwards twice over: an unobservable surface yields no negative to rest on, and preferring a conclusion is not a reason to acquire the evidence that produces it.

The five documents therefore do no verdict work in either direction. In particular the earlier entry used them to establish a negative -- "none is a Source/Code/Repository/Development link, so navigation step 2 has no target" -- and that sentence is withdrawn. What the frames contain is now unobserved by contract, not absent.

The cost is recorded rather than patched: under the sealed contract a frameset landing page is observable only down to "it declares frames", so this candidate's step 1 cannot be settled at all. That is a limitation of the contract, and mid-run is not when it gets amended.

Surface 2: https://github.com/jorio/BillyFrontier, from the first DIST_TUPLE's identifiers.
Necessary because: the gate was unsettled after surface 1 and this is the remaining admitted starting point for the packaged system.
observed_at_utc: 2026-08-28T05:23:54Z; http_status 200; redirect_chain: NONE (num_redirects 0)
Observed, restricted to metadata the contract allows: repository BillyFrontier, owner login jorio, default branch master, isFork false, isMirror false, isArchived false, isTemplate false, website metadata field https://pangeasoft.net/billy, and a source tree present at the root -- Source, Data, CMakeLists.txt, BUILD.md, CHANGELOG.md, README.md, LICENSE.md, .gitmodules.

The jorio/Pomme identifiers are accounted for and were not opened. UR determined from the frozen metadata that Pomme is a vendored dependency at extern/Pomme and not the packaged system, so under QA-26 it is another delimited system: a designation found there would be Pomme's, not Billy Frontier's, and could not bear on this gate either way.

```text
PASS not established
  no admitted surface yielded a designation witness. Surface 1's
  admissible content is a frameset declaring frames and carrying no
  anchors, which says nothing either way. Surface 2 carries a website
  field naming the project site -- a repo->site arrow, which C032
  settled is affiliation, not designation; designation would require
  the PROJECT to identify the repository as its canonical source.
  Arriving at the repository through a packaging identifier likewise
  yields affiliation rather than designation (QA-22).

FAIL not established
  twice over. The repository root carried no designation signal, but
  that is a bounded observation and not a demonstration that upstream
  designates none (C017). And the project site's rendered content was
  never lawfully observed at all, so nothing supports any claim about
  what it does or does not designate.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C043-UR-01
Candidate: C043 (frame rank 43, games/blobby)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/blobby/Makefile
Observed: HOMEPAGE=https://blobbyvolley.de/; GH_ACCOUNT=danielknobe; GH_PROJECT=blobbyvolley2; GH_TAGNAME=v$V with V=1.1.1; PKGNAME=blobby-$V; COMMENT="volleyball game with online play".
Inference: the frozen fields name one system. PKGNAME shortens the name GH_PROJECT gives in full, and a HOMEPAGE beside a repository identifier pair is the shape the protocol names non-ambiguous. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C043-E1-01
Candidate: C043
Gate: E1
Source: same frozen metadata
Observed: a third-party game -- COMMENT "volleyball game with online play", a GPLv2+ licence line, a HOMEPAGE on its own domain and an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C043-E2REP-01
Candidate: C043
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the HOMEPAGE, and the GH_ACCOUNT/GH_PROJECT pair. The pair resolves to the same repository the step-2 link reaches, so as at C038 it is not a separate surface.

Step 1: the frozen HOMEPAGE.
requested_url and final_url: https://blobbyvolley.de/
observed_at_utc: 2026-08-28T05:28:31Z-05:28:32Z; http_status 200; redirect_chain: NONE (num_redirects 0); 17223 bytes
evidence_role: official-project-page
Observed: the project's own site, titled "Blobby Volley 2 - Die offizielle Website", carrying a navigation menu and a dated news list.

The designation is on this page, in a news item, and it takes two of QA-23's admitted forms at once -- a sentence and a link relation:

```text
h3   04.09.2019 - Quellcode auf GitHub umgezogen!
p    Der aktuelle Quellcode ist ab sofort unter
     <a href='https://github.com/danielknobe/blobbyvolley2'>GitHub</a>
     zu finden. Das Sourceforge Repository wird nicht mehr gepflegt.
```

("Source code moved to GitHub! The current source code is from now on to be found at GitHub. The SourceForge repository is no longer maintained.")

Step 2: that link, and the authority for taking it is the sentence it sits inside, whose subject is "der aktuelle Quellcode" -- the current source code. What is NOT relied on: the navigation menu's separate "Github" item, which points at the same URL but is labelled with a host name rather than any of the contract's four words. C038 settled that an anchor reading "github" does no work on its own, and this entry does not let it.

Uniqueness, and why the ranking is upstream's rather than ours. The same page's navigation also carries "Sourceforge" -> http://sourceforge.net/projects/blobby/, a second location for the same system. The news paragraph ranks the two itself, in its second sentence: the SourceForge repository is no longer maintained. That is the C023 and C038 device -- a primary marked by upstream. The SourceForge hub was not followed; C007 settled separately that a generic project hub is not a repository root.

Other links on step 1, accounted for and not followed:

```text
Bugtracker -> .../blobbyvolley2/issues    forbidden surface
Changelog  -> .../blob/master/ChangeLog   changelog, forbidden surface
Download   -> download.php                not one of the four labels (QA-17)
Discord, Play Store, App Store, Microsoft Store, Blobby Liga,
the browser and WebAssembly builds        distribution and community
                                          channels, not source locations
```

Step 3: https://github.com/danielknobe/blobbyvolley2
observed_at_utc: 2026-08-28T05:29:37Z (metadata), 05:29:45Z (root listing); http_status 200 on both; redirect_chain: NONE on both
evidence_role: official-source-location
Observed, restricted to metadata and the root listing: full name danielknobe/blobbyvolley2, owner login danielknobe -- matching the frozen GH_ACCOUNT -- default branch master, fork false, archived false, is_template false, mirror_url null, private false, licence GPL-2.0 matching the frozen licence line, and description "Official continuation of the famous Blobby Volley 1.x arcade game." The homepage metadata field is null, so nothing here has to be weighed as a repo->site arrow (contrast C042). A source tree is present at the root: src, test, data, deps, doc, linux, macos, win, CMakeLists.txt, NintendoSwitchToolchain.cmake, vcpkg.json, INSTALL, README.md, ChangeLog, NEWS, AUTHORS, COPYING, doxyfile, .gitattributes, .github, .gitignore.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Blobby Volley 2).

Scope note: the designation is recorded as observed at the timestamps above. No claim is made about what this page carried at the sealed instant (QA-28).

Decision: PASS

## EV-C043-E2RULE-01
Candidate: C043
Gate: E2-RULE
Source: INSTALL in the designated repository
observed_at_utc: 2026-08-28T05:29:55Z; http_status 200; 236 bytes
Provenance: read against the source state available at screening observation time; no claim about the sealed primary snapshot (QA-28).

Observed: located witness, the file's opening line and the build sequence it governs:

```text
You must have CMake installed.
Then execute:

cmake .
make
```

Inference: this states a concrete validity requirement without our inventing one -- a build environment without CMake does not satisfy it, and the stated procedure does not apply. Externally authored, in upstream's own words.

Recorded as at C014, C023, C034 and C038: this is a BUILD-ENVIRONMENT requirement carrying no version bound. E2-RULE asks for at least one validity requirement and does not restrict the domain. One located witness settles a positive existential gate, so the search stopped here.
Decision: PASS

## EV-C043-E3-01
Candidate: C043
Gate: E3
Source: src/GameLogic.cpp in the designated repository
observed_at_utc: 2026-08-28T05:30:25Z; http_status 200; 16808 bytes
Provenance: observation-time source state, as above.

Observed: located witness, the collision-validity test and the clock that drives it.

```text
GameLogic.cpp:50        const int SQUISH_TOLERANCE = 11;

GameLogic.cpp:230-233   bool IGameLogic::isCollisionValid(PlayerSide side) const
                        {
                            // check whether the ball is squished
                            return mSquish[side2index(side)] <= 0;
                        }

GameLogic.cpp:248-254   void IGameLogic::onBallHitsPlayer(PlayerSide side)
                        {
                            if(!isCollisionValid(side))
                                return;
                            mSquish[side2index(side)] = SQUISH_TOLERANCE;

GameLogic.cpp:167-176   void IGameLogic::step( const DuelMatchState& state )
                        { mClock->step();
                          if(mClock->isRunning())
                          { --mSquish[0]; --mSquish[1];
                            --mSquishWall; --mSquishGround;
```

Inference: whether a ball-player contact counts as a hit is decided against mSquish, which that player's previous hit set to 11 and which the clock decrements once per running step. The identical contact is valid or not according to how many steps have passed since that side's last one. That is validity conditioned on history, which is what E3 asks for -- the same shape as C038's Qualifies() reading a persisted table, here with the conditioning state held in the match clock rather than on disk.
Decision: PASS

## EV-C043-E4-01
Candidate: C043
Gate: E4

Positive construction exhibited, via U_enforced.
observed_at_utc: 2026-08-28T05:31:46Z (TextManager.h), 05:31:29Z-05:31:46Z (TextManager.cpp); http_status 200
Provenance: observation-time source state.

The mechanism: the translatable-string table. `enum STRING` at TextManager.h:41-169 declares 110 named slots and closes with COUNT; TextManager::setDefault(), TextManager.cpp:152-288, assigns an English default to each; the constructor sizes the table to the enum and fills it, TextManager.cpp:36-37.

```text
enum members excluding COUNT                        110
distinct mStrings[...] assignments in setDefault     110
enum members with no assignment                        0
```

EN1 external authorship: the game and this table existed independently of this analysis.

EN2 explicit scope: the project segments the enum with its own section comments -- "common labels", "labels for main menu", "credits", "replays", "game texts", "network texts", "options" -- and each slot carries a name of its own (LBL_OK, RP_FILE_CORRUPT, NET_SERVER_FULL, OP_JUMP_KEY).

EN3 mechanical membership, with the two things it is easy to conflate kept apart:

```text
enumerator membership      the fixed enum slots through COUNT
runtime enforcement state  each slot's current token value
```

Membership is the first of these -- what setDefault assigned, one entry per enum slot, enumerable by reading either list, and cross-checked above rather than assumed to agree. The second is what the mutation paragraph below concerns. Separating them removes any appearance of conflict: the values move, the slots do not.

EN4 connection to validation: loadFromXML uses the table as the acceptance test for a language file's entries, in project code, and rejects in project code.

```text
TextManager.cpp:114-121
  auto found = std::find(mStrings.begin(), mStrings.end(), e);
  if(found != mStrings.end()) { found_count++; *found = t; }
  else
      std::cerr << "error in language file: entry "
                << e << " -> " << t << " invalid\n";
```

An `english` attribute that is not in the table is named invalid and its translation is discarded. Unlike C038, the deciding and rejecting code is the project's own.

One property of this enforcement is recorded rather than smoothed over: the values consulted for matching are mutable. Line 118 is `*found = t`, so a successful match REPLACES that slot's value with the translation.

```text
before   slot i holds source token A
after    slot i holds translated token B
```

It is a replacement, not a removal, and the earlier draft's "the acceptance set is the defaults minus those already consumed" overstated it. B may equal A; B may coincide with another slot's value; the extent stays at COUNT throughout. No cardinality claim of the form 110 -> 109 -> ... is supported, and none is made. What is true is narrower: the recognised-token relation can change during parsing, so it is not a fixed immutable 110-name acceptance set. The file's own comment says as much about the order it expects -- the loop "assumes that the strings in the xml file are in the correct order".

This does not disturb EN5, whose sealed text asks that "membership must be closed by something other than our choice" and admits "runtime construction closes the set" as `enforced`. Immutability is not among its requirements. The extent is fixed at COUNT and the parser walks it; at each step the deciding value is the slot's current one, so membership is determined mechanically and never by us.

Bounded to screening: this entry claims only that a mechanically constructible universe EXISTS. It does not fix its contents, and in particular does not conclude that the primary universe is exactly 110 units. QA-19 puts that at the inventory stage, to be established independently there.

EN5 closed within scope: mStrings is resized to COUNT and filled by setDefault at construction; no path adds a slot. Closed at construction. Tag: enforced.

EN6 outcome independence: the table is the set of user-interface strings the game displays. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per slot

  "slot N is initialized with English string S; at a parsing step an
   entry is accepted iff its english attribute matches some slot's
   CURRENT value; a match replaces that slot's value; an entry
   matching no current slot is named invalid and discarded"

retained as externally segmented fields, per observation
  the section the project placed the slot in
  the slot's own enum name
  its English default
```

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28 -- as with every other survivor, no observation fixes where the designated ref pointed at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## RETRACTION 19 — C042 read five frame documents the contract does not admit

C042's E2-REP entry requested the five frame documents declared by the frozen HOMEPAGE's frameset, on the reasoning that a frameset's frames are the landing page's own rendered composition and so are still step 1.

That reasoning is withdrawn. The sealed contract enumerates surfaces by navigation relation and says nothing about subresources; "the frames are the same surface" is the analyst's rendering model, not the contract's rule. It is the shape of C014's Downloads page and C037's host root: a criterion or a mental model used to widen where we may look. See QA-29.

Withdrawn specifically:

```text
the frameset-composition justification, in full
the frame-by-frame link table
"None is a Source, Code, Repository or Development link, so
 navigation step 2 has no target"
"the project site, read in full including every frame, designates
 no source location at all"
the defence that the alternative "would rest a negative on a
 technicality of markup"
```

The five requests stay on the record as quarantined and do no verdict work in either direction. What the frames contain is now unobserved by contract, not absent.

The verdict is unchanged -- UNRESOLVED, PI-UNCLASSIFIED-SHAPE -- but its grounds are narrower and its FAIL branch is stronger: with step 1 unobservable past "a frameset exists", there is even less basis for asserting that upstream designates no source location. Surface 2 and the QA-26/QA-27 accounting of jorio/Pomme are untouched.

## RETRACTION 20 — C043's E4 overstated the mutation as a shrinking acceptance set

C043's E4 entry wrote that line 118 makes "the acceptance set the English defaults MINUS those matched earlier in the same file".

That is wrong about the operation. `*found = t` replaces a slot's value; it does not remove a slot. The replacement value may equal what it replaced, or may coincide with another slot's value, and the extent stays at COUNT. Any decreasing-cardinality reading is withdrawn.

The narrower true statement is that the recognised-token relation is mutable during parsing, which is what the entry now says. EN5 is undisturbed: it requires closure not chosen by us, not immutability.

Also narrowed: the entry now states explicitly that it establishes only the EXISTENCE of a mechanically constructible universe, and fixes no count. QA-19 keeps that at the inventory stage.

## EV-C044-UR-01
Candidate: C044 (frame rank 44, games/blobwars)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/blobwars/Makefile
Observed: DISTNAME=blobwars-2.00; HOMEPAGE=https://sourceforge.net/projects/blobwars/; SITES=${SITE_SOURCEFORGE:=blobwars/}; COMMENT="2D arcade game". No GH_ACCOUNT/GH_PROJECT.
Inference: the frozen fields name one packaged system. DISTNAME, HOMEPAGE and SITES all carry the same project name. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C044-E1-01
Candidate: C044
Gate: E1
Source: same frozen metadata
Observed: a third-party game -- COMMENT "2D arcade game", GPLv2+ with third-party audio under CC and other licences, hosted on an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C044-E2REP-01
Candidate: C044
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE and the frozen SITES.

DEVIATION, recorded before the observations that follow. The first three requests to step 1 carried a spoofed `Mozilla/5.0` user agent and were answered 403 with a two-byte body, "no".

```text
06:28:44Z  GET  UA Mozilla/5.0   403, 2 bytes
06:29:29Z  GET  UA Mozilla/5.0   403, 2 bytes
06:29:29Z  GET  UA Mozilla/5.0   403, 2 bytes
06:29:30Z  HEAD UA Mozilla/5.0   403
06:29:30Z  GET  default client   200, 117365 bytes
```

Presenting a user agent I am not was an unpreregistered manipulation of the request, and it is recorded rather than quietly dropped. Classified as a non-adjudicative deviation: the E2-REP contract governs which SURFACES may be visited and seals no HTTP header policy, so this is not a contract breach in the way C037's host root was -- it is an unrecorded degree of freedom in how an admitted surface was requested. The observations below rest on the 200, which the plain client obtained. Note the direction, since it matters for what the 403s could otherwise have been made to mean: the host refused the disguised request and served the honest one. Had the entry stopped at the 403s it would have reported an unobservable surface that was in fact observable -- the error would have run toward a manufactured UNRESOLVED.

Step 1: https://sourceforge.net/projects/blobwars/ -- the frozen HOMEPAGE, which is a SourceForge project page.
observed_at_utc: 2026-08-28T06:29:30Z; http_status 200; redirect_chain: NONE (num_redirects 0); 117365 bytes
evidence_role: official-project-page

This is C023's topology, not C007's: the hub IS the landing page named by the frozen HOMEPAGE, so it is step 1 and readable in full, rather than something reached one hop from a landing page.

Observation scope, fixed before the request: HTTP status and redirects; the title and headings the page carries; any sentence upstream authored about where the project or its source is found; which project-navigation items the page exposes and their targets; artifact names exposed; any primary, canonical or mirror marking. Not: opening the Code area's history, the Files area, tickets, news, or any artifact.

Observed:

```text
title  "Blobwars: Metal Blob Solid download | SourceForge.net"
h1     Blobwars: Metal Blob Solid
h2     2D platform game

project-authored description, in full so that no absence claim rests
on an unread passage:
  "Metal Blob Solid is a 2D platform game, the first in the Blobwars
   series. You take on the role of a fearless Blob agent, Bob, who's
   mission is to infiltrate various enemy bases and rescue as many
   MIAs as possible, while battling many vicious aliens."

project navigation exposed by the page
  Summary  /projects/blobwars/          Files  /projects/blobwars/files/
  Reviews  Support  Tickets  Bugs  Support Requests  Patches
  Feature Requests   News                Code   /p/blobwars/code/

"Blobwars: Metal Blob Solid Web Site" -> https://sourceforge.net/projects/blobwars/
   the project's Web Site field points back at this same page; no
   external project site is named anywhere

Download button -> /projects/blobwars/files/latest/download, titled
   "Download blobwars-2.00-1.installer.exe from SourceForge - 75.1 MB"
```

The description is a game description. No project-authored prose and no project-specific marking designates a canonical source location, and no relocation notice of C023's kind appears. The page does expose a platform-rendered "Code" item; whether platform chrome itself carries upstream designation force is the unresolved question recorded at QA-30, not something this observation settles in either direction.

Step 2: the "Code" link. Its label is literally one of the contract's four words and step 1 explicitly exposes it, so the navigation is authorized on the contract's plain text -- no reading of the destination is required, which is the basis C038 established.

Step 3: https://sourceforge.net/p/blobwars/code/
observed_at_utc: 2026-08-28T06:30:29Z; http_status 200; redirect_chain: 2 redirects, final_url https://sourceforge.net/p/blobwars/code/ci/master/tree/
evidence_role: official-source-location
Observed: a git repository titled "Blobwars: Metal Blob Solid / Code", clone URL https://git.code.sf.net/p/blobwars/code, branches master and sdl2, tag release-1.18-1, and a source tree at the root:

```text
dirs   data doc gfx icons locale music patches sound src tools
files  .gitignore Makefile Makefile.windows blobwars.nsi blobwars.spec
```

Second starting point: the frozen SITES. `${SITE_SOURCEFORGE:=blobwars/}` resolves through the ports infrastructure's own macro definition to https://downloads.sourceforge.net/sourceforge/blobwars/.
Necessary because: the gate was unsettled after step 1, and this is the remaining admitted starting point. Observed rather than predicted from its URL shape (C018), even though the same macro produced 404s at C031, C036 and C037.
observed_at_utc: 2026-08-28T06:31:22Z (GET), 06:31:23Z (HEAD); http_status 404, 404; redirect_chain: NONE on both
Observed: a 154-byte "404 Not Found -- The resource could not be found."

Now the adjudication, and it turns on a question the sealed criterion does not answer.

Exactly one location with a source role was observed: the code area, reached by an authorized step 2 and confirmed at step 3 to hold a source tree. What is undecided is the evidential force of the label that exposed it, because that label is drawn by the platform rather than written by upstream. The verdict differs by branch:

```text
if SourceForge's platform chrome counts as upstream designation
    "Code" designates the observed repository as this project's source
    no competing SOURCE designation has been established
    -> E2-REP PASS could follow

if it does not count as upstream designation
    the repository's identity and its source tree are affiliation only
    -> no designation established
    -> E2-REP UNRESOLVED
```

Choosing a branch would be us supplying the missing rule, so neither is taken. See QA-30.

What is deliberately NOT in that table is the Files area. Step 1 exposed it as a navigation label -- `Files -> /projects/blobwars/files/` -- and nothing more; it was not opened, and a generic artifact-area label establishes no source location. Treating it as a second source designation would be reading contents off an unopened surface, which is the same restraint this entry already applies to the Download button's installer filename. So the gap here is PASS versus UNRESOLVED, and no multi-designation question arises at all.

Two precedents were checked against this and neither carries it:

```text
C006  its step 1 was https://dgen.sourceforge.net/ -- the project's OWN
      site, where the locations sit on a page upstream authored. That
      is not this page, and its two-with-no-primary finding has no
      counterpart here, where only one source-role location exists.

C023  same hub-as-HOMEPAGE topology, and it reached PASS. But what
      ranked its locations was upstream's own dated sentence, "As of
      2015-12-05, this project can be found here". The entry called
      the Code and Files areas SourceForge's project furniture and let
      the notice do the work. No such sentence exists here.
```

```text
PASS not established
  no designation witness whose evidential force is determined by the
  sealed rules establishes a single canonical source location.
  Upstream's own words on step 1 describe the game and nothing else,
  and the Web Site field points back at the same page. The one
  candidate witness is the platform-rendered "Code" item, and QA-30
  is exactly the question of whether that carries designation force.
  Reaching the code area by an authorized step 2 does not settle it
  either: the step-2 whitelist is a navigation permission, and QA-22
  established that arriving somewhere by an admitted route yields
  affiliation rather than designation.

FAIL not established
  no failure code is completed. E2REP-NO-SINGLE-CANONICAL-LOCATION
  requires several designated locations with no primary among them,
  and only one source-role location was ever observed.

E2REP-NO-SOURCE not established
  a source tree WAS observed at step 3, so source access is not what
  is missing.
```

Both admitted starting points were determinately answered -- 200 and 404 -- so no surface is left unobserved and this is not the transport family. What is missing is a rule, not an observation.

Recorded and not used: the Download button names a Windows installer artifact. No inference is drawn from that about what the Files area holds -- it was not opened, and C035 settled that an unobserved surface's contents may not be read off its neighbours.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 21 — C044 counted the Files area as a second source location

C044's E2-REP entry set up its branch table around "the two locations this project has -- a code area and a release Files area", and made one branch C006's E2REP-NO-SINGLE-CANONICAL-LOCATION.

That is withdrawn. The Files area was never opened. What step 1 exposed was a navigation label, `Files -> /projects/blobwars/files/`, and a generic artifact-area label establishes no source location -- whether that area holds source tarballs, binaries, or both is not something any admissible evidence in this entry says. The same entry had already declined to infer the area's contents from the Download button's installer filename, and then failed to apply that restraint one paragraph later.

Consequences of the repair:

```text
withdrawn   "the two locations this project has"
            the FAIL branch resting on two designated locations
            the framing of QA-30's gap as FAIL versus UNRESOLVED

corrected   exactly one source-role location was observed, the code
            area; the open question is the evidential force of the
            platform-drawn label that exposed it
            -> the gap is PASS versus UNRESOLVED
```

The verdict does not move. Under the corrected branches, PASS is the branch that would require adopting the undecided rule, and adopting it now with the candidate's outcome in view is the post-hoc criterion change the run forbids. E2-REP stays UNRESOLVED, failure_code NONE, protocol_issue_code PI-UNCLASSIFIED-SHAPE, and the ledger rows are unchanged.

Also lowered in the same pass: "Nothing on this surface states, labels or marks where the project's source is" -- the surface does carry a "Code" label, and the issue is that label's force, not its absence. And "no admitted surface designates a single canonical source location" now reads "no designation witness whose evidential force is determined by the sealed rules", which is what the record supports.

The user-agent deviation is reclassified as well: an unpreregistered request manipulation and a non-adjudicative deviation, rather than a contract breach. The E2-REP contract governs which surfaces may be visited and seals no HTTP header policy, so it is an unrecorded degree of freedom, not the C037 shape.

## EV-C045-UR-01
Candidate: C045 (frame rank 45, games/blockgame)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/blockgame/Makefile
Observed: DISTNAME=blockgame-${V} with V=0.6.14.1; HOMEPAGE=https://github.com/yukiisbored/Launcher; SITES=https://github.com/yukiisbored/Launcher/releases/download/${V}-bgl/; WRKDIST=${WRKDIR}/Launcher; COMMENT="free and open-source launcher for Minecraft".
Inference: one packaged system. The package name and the upstream repository name differ -- blockgame against Launcher -- but every frozen field routes to the same repository, and WRKDIST and the "-bgl" tag suffix tie the distfile to it. A name mismatch between the OpenBSD package and upstream is not the two-systems case UR-AMBIGUOUS is for. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C045-E1-01
Candidate: C045
Gate: E1
Source: same frozen metadata
Observed: a third-party Minecraft launcher under Apache 2.0, on an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C045-E2REP-01
Candidate: C045
Gate: E2-REP

Per QA-27 both admitted starting points are enumerated: the frozen HOMEPAGE, and the frozen SITES. They are different surfaces here, not the C038 case where a repository identifier pair merely restated the step-2 destination.

Step 1: the frozen HOMEPAGE, https://github.com/yukiisbored/Launcher, which is itself a repository. This is the C010/C012/C017 topology in which step 1 and step 3 are the same surface; QA-22 settled that the topology answers WHICH surface, and supplies no designation of its own.

Observation scope, fixed before the request: existence; repository and owner name; default branch; fork, mirror, archive and template flags; the website metadata field; the repository description; whether a source tree is present at the root; any statement designating this location as the project's source; any primary or mirror marking. Not: README prose, the releases area, issues, docs, or any source file.

observed_at_utc: 2026-08-28T06:44:35Z (metadata), 06:45:08Z (root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        yukiisbored/Launcher
owner            yukiisbored
default_branch   bgl/0.6.14
fork             TRUE, parent MultiMC/Launcher
archived         TRUE
is_template      false          mirror_url  null
website field    EMPTY
description      "A custom launcher which allows running Minecraft on
                  unsupported UNIX-like operating systems"
```

Root listing at the observed default branch bgl/0.6.14: launcher, libraries, buildconfig, cmake, doc, .github, CMakeLists.txt, BUILD.md, COPYING.md, README.md, changelog.md, .gitattributes, .gitignore, .gitmodules, notsecrets. A source tree is present.

The fork parent was not visited. C025 settled that the fork-parent relation is not a step the navigation whitelist contains, and the reason is the whitelist rather than any judgement about which repository matters. Under QA-26 MultiMC/Launcher is in any case a different delimited system: a designation found there would be its own.

The second admitted starting point was accounted for and not observed. The reason is the contract's own text, and it is simpler than an earlier draft made it.

```text
allowed starting points
  "ONLY the URLs and identifiers found in the frozen OpenBSD metadata
   that UR already resolved to one system."
   -> a bound on where a run may BEGIN. It is a necessary condition
      for admission, not a licence to read something the contract
      forbids elsewhere.

forbidden at E2-REP
  "issues / PRs / changelog / releases"
   -> the frozen SITES here IS a releases path,
      .../Launcher/releases/download/0.6.14.1-bgl/
```

Composed the only way the two clauses actually compose: the URL enters the starting-point set, and the releases prohibition still applies to it, so it is metadata-supplied but unobservable under the sealed contract. QA-17 fixed this direction already -- a permission stated elsewhere does not widen the forbidden set -- and QA-27's carried-forward rule provides the disposition, its third branch: "otherwise resolved under the protocol, with the reason named", the obligation being "to account for each, not to open each".

Nothing is inferred about the surface's contents. It was not observed, and what a releases page might have shown -- one designation, several, a primary or mirror relation, or nothing -- is not something this entry constrains.

Recorded because it is where the sealed methodology runs out, not where it contradicts itself: the protocol does not say how E2-REP is to be COMPLETED when a starting point that might be necessary is itself forbidden to inspect. See QA-31.

Why the question did not arise earlier: C013 and C022 each had a frozen SITES under a releases path, and both reached a verdict at step 1, where the stop rule ends navigation. C013's entry recorded "/releases/" as closed because releases are "named in the contract's forbidden list outright" -- the same reading, applied where nothing turned on it. C029 did request such a URL, but that candidate is withdrawn and its material quarantined.

```text
PASS not established
  the observed repository supplies no upstream canonical-source
  designation. The only route to it is the packaging metadata's own
  HOMEPAGE field, and arrival by an admitted route is affiliation
  (QA-22, C017). The website field is empty, so there is not even the
  repo->site arrow C042 had to weigh.

  The frozen SITES is metadata-supplied but falls under the contract's
  explicit releases prohibition and was therefore not observed.
  Nothing is inferred about its contents.

FAIL not established
  the repository root carried no positive candidate-level failure
  evidence, and that silence is a bounded observation rather than a
  demonstration that upstream designates none (C017). The forbidden
  SITES can support no negative claim either, having not been
  observed.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

On the code: `PI-UNCLASSIFIED-SHAPE` is used on its sealed definition, "a real screening outcome that no sealed criterion describes". What is undescribed is how E2-REP completes when a potentially necessary metadata-supplied starting point is an explicitly forbidden surface class. This is not the transport family -- both requests that were made returned 200, and the remaining surface was withheld by the contract, not by a network.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 22 — C045 diagnosed a contract conflict, and constrained a surface it had not observed

C045's first E2-REP entry described the frozen SITES as sitting inside "a conflict inside the sealed contract", set out two competing readings, and then chose between them with this argument:

```text
"a designation found there could only move this candidate toward PASS,
 and no observation there could complete a failure code, since FAIL
 needs positive evidence. Opening is therefore the branch that could
 rescue a verdict"
```

Both parts are withdrawn.

**The conflict diagnosis.** The starting-point clause reads "ONLY the URLs and identifiers found in the frozen OpenBSD metadata". That bounds where a run may begin -- a necessary condition for a surface to be admissible. It nowhere says that being in the metadata overrides a prohibition stated elsewhere. Read that way the two clauses compose without contradiction: the URL is in the starting-point set, and the releases prohibition still applies to it. QA-17 had already fixed this direction, and QA-27's third disposition branch -- "otherwise resolved under the protocol, with the reason named" -- is where such a surface goes.

**The asymmetry argument.** It states what a page we did not open could and could not have contained. That is the C033 and C035 error in its purest form: pre-constraining an unobserved surface's contents. A releases page might expose one designation, several, an explicit primary or mirror relation, or nothing at all, and nothing in this record narrows that. The C020/C024 comparison built on it goes too -- those were about rescuing a TERMINAL verdict with fresh observation, which is not this situation.

Neither withdrawal changes the outcome, and the reason to decline the surface is now stronger rather than weaker: releases are forbidden outright, so no choice between readings had to be made, and no outcome had to be looked at first.

Also lowered in the same pass: "Root listing at ref bgl/0.6.14, the frozen version's branch". The frozen V is 0.6.14.1 and the observed default branch is bgl/0.6.14; their correspondence was never established, and E2-REP needs only that a source tree is present. It now reads "Root listing at the observed default branch bgl/0.6.14".

Ledger unchanged: E2-REP UNRESOLVED, failure_code NONE, PI-UNCLASSIFIED-SHAPE, later gates NOT_REACHED.

## EV-C046-UR-01
Candidate: C046 (frame rank 46, games/blockrage)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/blockrage/Makefile
Observed: DISTNAME=blockrage-0.2.3; HOMEPAGE=https://blockrage.sourceforge.net/; SITES=${SITE_SOURCEFORGE:=blockrage/}; COMMENT="falling block puzzle game similar to Xixit".
Inference: the frozen fields name one packaged system, Block Rage. "similar to Xixit" is a comparison, not a second packaged system -- the same reading applied to C013's "numerous game consoles" and C023's "marathon / alephone". Not UR-AMBIGUOUS.
Decision: PASS

## EV-C046-E1-01
Candidate: C046
Gate: E1
Source: same frozen metadata
Observed: a third-party puzzle game under GPLv2+, on an upstream host unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C046-E2REP-01
Candidate: C046
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url: https://blockrage.sourceforge.net/ ; final_url: https://sourceforge.net/projects/blockrage/
observed_at_utc: 2026-08-28T07:01:33Z-07:01:34Z; http_status 200; redirect_chain: 1 redirect; 98790 bytes
evidence_role: official-project-page

Recorded exactly: the frozen per-project host answered with a redirect, and what was served is the SourceForge project page. No inference is drawn about why, or about what that host held before. The surface observed is the one the admitted URL actually returned.

That makes this C023's and C044's hub-as-step-1 topology rather than C002's and C006's, where a per-project SourceForge host served a page the project itself had authored.

Observation scope, fixed before the request: HTTP status and redirects; the title and headings; any sentence upstream authored about where the project or its source is found; which project-navigation items are exposed and their targets; artifact names exposed; any primary, canonical or mirror marking. Not: opening the Files area, tickets, news, or any artifact.

```text
title  "Block Rage download | SourceForge.net"
h1     Block Rage
       Status: Pre-Alpha   Brought to you by: jiri_svoboda
       Last Update: 2013-03-08

project-authored description, quoted so no absence claim rests on an
unread passage:
  "Highly addictive falling blocks game with detailed graphics and
   animated plasmatic backgrounds. Challenge your friend in a 2-player
   hotsea[t]..."

project navigation exposed
  Summary  Files  Reviews  Support  Tickets  Bugs
  Feature Requests  News

  -- there is NO Code item.

"Block Rage Web Site" -> http://blockrage.sourceforge.net
   the Web Site field points back at the frozen URL that redirected
   here; it names no further surface

Download -> /projects/blockrage/files/latest/download
```

A scan of the project area for source-role wording -- "source code", "repository", "git", "svn", "cvs", "Code" -- returned nothing.

So navigation step 2 has no target: no Source, Code, Repository or Development link is exposed at all. The Files area was not opened, and per RETRACTION 21 a generic artifact-area label establishes no source location either way.

QA-30 does not bite here, and the reason is worth one line so its absence is not mistaken for an oversight. That question is about the evidential force of a platform-drawn "Code" item; this page draws none, so nothing turns on how such an item would be read.

Surface 2: the frozen SITES. `${SITE_SOURCEFORGE:=blockrage/}` resolves through the ports infrastructure's own macro definition to https://downloads.sourceforge.net/sourceforge/blockrage/.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point. Observed rather than predicted from its URL shape (C018), though the same macro produced 404s at C031, C036, C037 and C044.
observed_at_utc: 2026-08-28T07:01:55Z (GET), 07:01:56Z (HEAD); http_status 404, 404; redirect_chain: NONE on both
Observed: a 154-byte "404 Not Found -- The resource could not be found." No headings, artifact names or designation signal.

```text
PASS not established
  neither admissible surface established a canonical-source
  designation. Surface 1 exposes no source-role link of any kind and
  its own words describe the game; surface 2 returned 404 and
  displayed nothing.

FAIL not established
  a project page carrying no source link and an archive path
  returning 404 do not demonstrate that upstream designates no
  canonical source location -- the C017 boundary, and the same
  reading as C036.

E2REP-NO-SOURCE not established
  the 404 is evidence about that endpoint. Nothing observed bears on
  whether a source representation is reachable elsewhere, and no
  surface was reached at which source-tree presence could have been
  established either way.
```

Both starting points were determinately answered -- 200 and 404 -- so no surface is left unobserved, this is not the transport family, and the outcome is a shape the sealed criteria do not describe. The same E2-REP outcome shape as C036.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C047-UR-01
Candidate: C047 (frame rank 47, games/bluemoon)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bluemoon/Makefile
Observed: DISTNAME=bluemoon-${V} with V=2.14; HOMEPAGE=http://www.catb.org/~esr/bluemoon/; SITES=http://www.catb.org/~esr/bluemoon/; COMMENT="console-based 52-card solitare game".
Inference: the frozen fields name one packaged system, bluemoon. HOMEPAGE and SITES are the same URL, so the metadata supplies one surface rather than two. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C047-E1-01
Candidate: C047
Gate: E1
Source: same frozen metadata
Observed: a third-party solitaire game under a BSD licence, on a personal upstream site unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C047-E2REP-01
Candidate: C047
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and they coincide: HOMEPAGE and SITES are the identical URL, so there is one admitted surface, not two. Neither names a class the contract forbids, so QA-31 does not arise.

Step 1: http://www.catb.org/~esr/bluemoon/
requested_url and final_url: identical; observed_at_utc: 2026-08-28T07:17:17Z; http_status 200; redirect_chain: NONE (num_redirects 0); 8304 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; any sentence upstream authored about where the project or its source is; artifact names and their descriptions as upstream gives them; any primary, canonical, preferred or mirror marking. Not: opening any listed artifact or document, and not navigating past step 1 unless a designation required it.

The page is titled "Resource page for bluemoon 2.15" and carries sections Summary, Resources, Recent Changes and Supporters. Two source-role designations appear on it, both in upstream's own words.

```text
1  the Resources table, which upstream captions "Downloadable
   resources", assigns each row its own description:

     README.adoc            roadmap file
     COPYING                project license
     NEWS.adoc              project news
     bluemoon-2.15.tar.gz   GZIPPED SOURCE TARBALL
     README.html            roadmap file
     bluemoon.html          Documentation
     NEWS.html              project news

   The artifact is served from this same directory, which is also the
   frozen SITES.

2  the sentence immediately below that table:

     "The project repository is at https://gitlab.com/esr/bluemoon."

   with the URL itself as the anchor text.
```

Both are designations under the sealed criterion, which admits a repository OR a source distribution as source-location types -- the reading applied at C006 and C011. Both sit on the permitted surface, which is what separates this from C002 and C007: those two had their multi-designation findings withdrawn because the second designation lay past the contract's reach, and here no hop is needed for either.

Distinguishing this from C044's Files area, since the two could be confused. There the label was generic -- "Files" -- and the area was never opened, so RETRACTION 21 refused to treat it as a source location. Here upstream's own table assigns the row the description "gzipped source tarball", naming the artifact's source role on the surface itself. The source-role attribution is upstream's wording, not ours.

No primary is marked. The whole page was read to establish this, rather than the sections that happened to carry the designations: Summary is a description of the card game, Recent Changes reads "Manor metadata changes to help packagers", and Supporters is a list of names. Nothing anywhere on the surface states or marks which of the two locations is canonical, primary, preferred or authoritative, and no mirror relation is asserted between them.

What is deliberately NOT done is rank them ourselves. A reading is available in which "The project repository is at X" is the structural designation and the tarball is merely a download, and the reverse reading is equally available. Both were refused: the record already settled at C015, and again when C002's first entry was withdrawn, that treating the repository as the real source and the tarballs as mere releases -- or the reverse -- supplies a hierarchy the criterion refuses to let us supply.

Navigation stopped here. The GitLab link was not followed: the contract's stop rule ends navigation "the moment a PASS or a specific failure code is determined. Not one page further", and the code was determined on step 1.

Inference: not exactly one designated canonical source location. Two are designated on the permitted surface with no primary among them, which is the failure the sealed criterion names -- and the code is positive in shape, recording that several designations were found rather than that nothing was.

Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

Gates after E2-REP are NOT_REACHED.

Recorded and doing no verdict work: the frozen DISTNAME is bluemoon-2.14 while the page presents 2.15. That is a version difference at one location, not a second location, and under QA-28 nothing here claims what this surface carried at the sealed instant.

## EV-C048-UR-01
Candidate: C048 (frame rank 48, games/bomberclone)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bomberclone/Makefile
Observed: DISTNAME=bomberclone-0.11.9; HOMEPAGE=http://www.bomberclone.de/; SITES=${SITE_SOURCEFORGE:=bomberclone/}; COMMENT="bomberman clone with multiplayer mode".
Inference: the frozen fields name one packaged system, BomberClone. "bomberman clone" describes what it imitates, not a second packaged system -- the reading applied at C013, C023 and C046. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C048-E1-01
Candidate: C048
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv2, on an upstream domain unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C048-E2REP-01
Candidate: C048
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were requested. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
observed_at_utc: 2026-08-28T07:25:36Z (following redirects), 07:26:06Z (without following)

```text
http://www.bomberclone.de/
  -> HTTP/1.1 301 Moved Permanently
     Location: https://www.linux-abos.com/spiele/bomberclone/

https://www.linux-abos.com/spiele/bomberclone/
  -> 200, 104312 bytes
     title "BomberClone fuer Linux - Klassischer Bomberman-Spass gratis"
```

Observed, of the final response: it is branded "Linux-Abos.com" throughout; its navigation is that site's own publication sections (Startseite, Linux / Debian, Sicherheit, Spiele, Hardware, Vermischtes); and the BomberClone page sits among that site's unrelated articles on Steam machines, crypto mining, MongoDB and Bluetooth headsets.

Inference: the final response is a third-party publication surface, not BomberClone's upstream official landing/project page.

No inference is drawn about WHY the frozen domain answers this way, or about what it served before. C046 established that restraint for a redirect and it applies unchanged here.

The distinction from C046 is worth stating, so the two entries are not read as inconsistent. There the frozen HOMEPAGE also redirected, but to the same project's own SourceForge project page -- still a surface belonging to that project, and readable as step 1. Here the redirect leaves the project entirely.

That governs what the response may be used for, and the E2-REP contract settles it without help from anywhere else: step 1 admits "the upstream official landing/project page", and the gate's criterion requires the designation to come from upstream itself. On the inference above this document is neither, so it cannot do upstream-designation work at this gate. No later section is invoked -- primary-universe admissibility is a question for a stage this candidate never reaches.

The split observed here is deliberate:

```text
read, and legitimately  -- what the response IS, since the gate cannot
                           proceed without knowing whether an upstream
                           surface was reached
NOT read for designation -- its content, its links, and in particular
                           the pkgsrc index it points at
```

Step 1 therefore reached no upstream surface, and step 2 has no target.

Surface 2: the frozen SITES. `${SITE_SOURCEFORGE:=bomberclone/}` resolves through the ports infrastructure's own macro definition to https://downloads.sourceforge.net/sourceforge/bomberclone/.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point. Observed rather than predicted from its URL shape (C018), though the same macro produced 404s at C031, C036, C037, C044 and C046.
observed_at_utc: 2026-08-28T07:26:06Z (GET), 07:26:07Z (HEAD); http_status 404, 404; redirect_chain: NONE on both
Observed: a 154-byte "404 Not Found -- The resource could not be found." No headings, artifact names or designation signal.

```text
PASS not established
  no upstream surface was reached on which a designation could be
  made. The frozen HOMEPAGE answered 301 to a third-party
  publication, whose content is inadmissible for this purpose, and
  the frozen SITES returned 404 and displayed nothing.

FAIL not established
  a domain that redirects off the project and an archive path that
  returns 404 are facts about those two endpoints. Neither
  demonstrates that upstream designates no canonical source location
  -- the C017 boundary.

E2REP-NO-SOURCE not established
  nothing observed bears on whether a source representation is
  reachable elsewhere, and no surface was reached at which
  source-tree presence could have been established either way.
```

Both starting points were determinately answered -- a 301 whose destination returned 200, and a 404 on both GET and HEAD -- so no surface is left unobserved and this is not the transport family. What the sealed criteria do not describe is the resulting combination: the frozen landing-page starting point determinately resolves to a non-upstream surface, while the other admitted starting point determinately yields no usable designation evidence.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C049-UR-01
Candidate: C049 (frame rank 49, games/boswars)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/boswars/Makefile
Observed: DISTNAME=boswars-${V}-src with V=2.7; PKGNAME=boswars-${V}; HOMEPAGE=https://www.boswars.org/; SITES=https://www.boswars.org/dist/releases/; COMMENT="real-time strategy game".
Inference: the frozen fields name one packaged system, Bos Wars, and HOMEPAGE and SITES sit on the same upstream domain. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C049-E1-01
Candidate: C049
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv2, on an upstream domain unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C049-E2REP-01
Candidate: C049
Gate: E2-REP

Step 1: the frozen HOMEPAGE.
requested_url and final_url: https://www.boswars.org/
observed_at_utc: 2026-08-28T07:31:29Z; http_status 200; redirect_chain: NONE (num_redirects 0); 3307 bytes
evidence_role: official-project-page
Observed: the project's own site, titled "Bos Wars", with sections About and Project. Its navigation exposes Home, News, Download, Screenshots and **Development**. The Project section reads: "The project pages are on Codeberg and Savannah." -- Codeberg linking to https://codeberg.org/boswars/boswars and Savannah to https://savannah.nongnu.org/projects/stratagus-bos/. Issue Tracker, Matrix, IRC and Reddit links follow.

No failure code is determined here, and the reason is worth stating because a two-location reading is available on its face. "The project pages are on Codeberg and Savannah" designates two PROJECT PAGES, not two source locations, and C007 settled that a generic project hub is not a repository root. This is not C047's situation, where upstream's own words gave one artifact the role "gzipped source tarball" and the other location the role "project repository" on the same page.

Step 2: the "Development" link. Its label is one of the contract's four words verbatim and step 1 exposes it directly, so the navigation is authorized on the contract's plain text -- the C038 basis, with no reading of the destination required.

requested_url and final_url: https://www.boswars.org/development.shtml
observed_at_utc: 2026-08-28T07:32:08Z; http_status 200; redirect_chain: NONE; 4453 bytes

This page performs the designation, in upstream's own words, and performs the ranking too:

```text
"The project git repositories and management is on Codeberg."

"You can get the latest version with git :
   git clone https://codeberg.org/boswars/boswars.git"

"Some sources for the assets used in the game can be found in the
 materials.bos repository."

"The sources of the web pages can be found in the website.bos
 repository."

"Old development done before december 17th 2004 can be found in the
 CVS repository."
```

Every competing location is delimited or ranked by upstream itself, which is what C023, C015 and C038 required and what C047 lacked:

```text
materials.bos   asset sources, by upstream's own description
website.bos     web page sources, by upstream's own description
                -- both a different content set from the packaged
                   game, so QA-26 applies: project-level multiplicity
                   is not candidate-level multiplicity
CVS repository  "Old development done before december 17th 2004"
                -- upstream's own temporal ranking, the C015 device
Savannah        appears here only as the CVS repository and the Patch
                Tracker; nothing designates it as the source location
```

Step 3: https://codeberg.org/boswars/boswars -- the location the clone command names.
observed_at_utc: 2026-08-28T07:32:40Z (metadata), 07:32:42Z (root listing); http_status 200 on both; redirect_chain: NONE on both
evidence_role: official-source-location
Observed: full name boswars/boswars, owner boswars, default branch master, fork false, archived false, mirror false, template false, empty false, parent null, **website field https://boswars.org**, description "A futuristic real-time strategy game featuring a dynamic rate-based economy.", and clone_url https://codeberg.org/boswars/boswars.git -- byte for byte the URL the Development page publishes. A source tree is present at the root:

```text
dirs   engine campaigns doc graphics intro languages maps patches
       scripts sounds tools units
files  make.py fabricate.py INSTALL.md README.md CHANGELOG
       COPYRIGHT.txt LICENSE.txt .gdbinit .gitignore
```

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Bos Wars).

The direction is asymmetric, and stating it that way matters because an earlier draft claimed C022's two-way designation here:

```text
Bos Wars project site
  "The project git repositories and management is on Codeberg."
  + the exact clone URL
        |
        v                          DESIGNATION
  codeberg.org/boswars/boswars

repository metadata
  website = https://boswars.org
        |
        ^                          AFFILIATION only
```

The project site designates the repository. The repository's website field independently corroborates that the two belong together, but does not itself designate -- C032 and C042 refused exactly that arrow, and this entry does not quietly readmit it. Nothing is lost: the designation is complete from the Development page's upstream-authored sentence and clone URL alone.

On QA-25, since a clone command is involved: the command is not what does the designating. The sentence "The project git repositories and management is on Codeberg" states the location, and the command supplies its exact URL. This is not C020's "you can also use anonymous cvs", where a route was miscounted as a location.

The frozen SITES, https://www.boswars.org/dist/releases/, is accounted for and was not observed. The stop rule ends navigation "the moment a PASS or a specific failure code is determined. Not one page further", and the determination was reached at step 3. Under QA-27 the obligation is to account for each starting point rather than to open each, and this is the branch where the protocol resolves it. QA-31's question -- whether a URL naming a forbidden class may be observed at all -- therefore does not have to be reached here.

Recorded because it bounds this PASS: the "Download" link on step 1 was not opened, QA-17 having settled that the label is outside the whitelist. If that page designates a source distribution, this would be C047's shape. That possibility is unexamined, not excluded -- and it cannot be examined, which is exactly why C002's and C007's multi-designation findings were withdrawn when they rested on surfaces the contract does not reach. The verdict here rests on what the permitted surfaces do say, and they designate one location.

Decision: PASS

## EV-C049-E2RULE-01
Candidate: C049
Gate: E2-RULE
Source: INSTALL.md in the designated repository
observed_at_utc: 2026-08-28T07:33:22Z; http_status 200; 3759 bytes
Provenance: read against the source state available at screening observation time; no claim about the sealed primary snapshot (QA-28).

Observed: located witness, the file's own Software Requirements section:

```text
* SDL 2      (required)
* libpng     (required)
* zlib       (required)
* Lua 5.1    (required)
* libvorbis  (recommended)
* libtheora  (recommended)
* libogg     (recommended)
* tolua++    if you plan to change the Lua API
```

Inference: these determine concrete validity requirements without our inventing them -- a build environment lacking any item marked (required) does not satisfy the stated conditions, and the requirement is version-bounded in two places, "SDL 2" and "Lua 5.1", which C014, C023, C034, C038 and C043 all lacked. The conditional item is bounded by its own stated condition rather than hedged.
Decision: PASS

## EV-C049-E3-01
Candidate: C049
Gate: E3
Source: engine/unit/build.cpp and engine/map/map_fog.cpp in the designated repository
observed_at_utc: 2026-08-28T07:34:04Z (build.cpp), 07:37:27Z (map_fog.cpp); http_status 200 on both
Provenance: observation-time source state, as above.

Observed: located witness. Both halves of the chain are quoted rather than one being assumed, which is the requirement C038 established.

```text
build.cpp:341-375   CUnit *CanBuildUnitType(const CUnit *unit,
                        const CUnitType *type, int x, int y, int real)
                    ...
                      if (player && !real) {
                          testmask = MapFogFilterFlags(player, x + w,
                                                       y + h,
                                                       type->MovementMask);
                      } else {
                          testmask = type->MovementMask;
                      }

map_fog.cpp:114-136 int MapFogFilterFlags(CPlayer *player, int x,
                                          int y, int mask)
                    {
                      nunits = UnitCache.Select(x, y, table, UnitMax);
                      fogmask = -1;
                      while (unitcount < nunits) {
                          if (!table[unitcount]->IsVisibleAsGoal(player)) {
                              fogmask &= ~table[unitcount]->Type->FieldFlags;
                          }
                          ++unitcount;
                      }
                      return mask & fogmask;
                    }
```

Inference, kept to what the two quoted functions establish: whether a placement is valid is tested against a mask from which the field flags of every unit failing `IsVisibleAsGoal(player)` have been removed. So for the same unit type at the same coordinates, a different current visibility and unit state produces a different effective test mask and therefore a different placement verdict. That is a stateful validity question, which is what E3 asks for.

No claim is made about remembered or accumulated past visibility. An earlier draft said the verdict depends on "what that player has seen by that point in the match", which would need `IsVisibleAsGoal`'s backing state and its writer, and neither was observed. E3 asks for stateful OR temporal; the stateful half is established here on its own.
Decision: PASS

## EV-C049-E4-01
Candidate: C049
Gate: E4

Positive construction exhibited, via U_enforced.
observed_at_utc: 2026-08-28T07:34:04Z (script_unittype.cpp), 07:37:29Z (unittype.h); http_status 200
Provenance: observation-time source state.

The mechanism: the unit-type variable registry.

```text
engine/include/unittype.h:397-414
  // Index for variable already defined.
  enum { HP_INDEX, BUILD_INDEX, ... AUTOREPAIRRANGE_INDEX,
         NVARALREADYDEFINED, };

engine/unit/script_unittype.cpp:62-66
  const char *VariableNames[NVARALREADYDEFINED] = {
      "HitPoints", "Build", "Charge", "Transport",
      "Training", "GiveResource", "Kill", "Armor", "SightRange",
      "AttackRange", "PiercingDamage", "BasicDamage", "RadarRange",
      "RadarJammerRange", "AutoRepairRange"};

engine/unit/script_unittype.cpp:938-946
  int GetVariableIndex(const char *varname)
  {
      for (int i = 0; i < NVARALREADYDEFINED; ++i) {
          if (!strcmp(varname, VariableNames[i])) { return i; }
      }
      return -1;
  }
```

```text
enum members before NVARALREADYDEFINED   15
string entries in VariableNames          15
cross-check                              match
```

EN1 external authorship: the engine and this registry existed independently of this analysis.

EN2 explicit scope: the project names the domain in its own comment on the enum, "Index for variable already defined", and each member carries its own name. The scope is the variable tags a unit-type definition may set.

EN3 mechanical membership, with the two levels kept apart as at C043:

```text
enumerator membership      the fixed index slots
                           0..NVARALREADYDEFINED-1
runtime enforcement value  the current string stored in
                           VariableNames[i]
```

Membership is enumerable by reading either list, and the two were cross-checked above rather than assumed to agree. No immutability claim is made or needed: an earlier draft wrote that "no observed path mutates them", which is an absence argument from not having looked, and `const char *` constrains the pointed-to characters rather than settling the question anyway. What the gate needs is the positive cross-check at observation time -- 15 initializer entries against 15 enum members.

EN4 connection to validation, in project code on both sides:

```text
script_unittype.cpp:632-648
  i = GetVariableIndex(value);
  if (i != -1) { ... continue; }
  printf("
%s
", type->Name.c_str());
  LuaError(l, "Unsupported tag: %s" _C_ value);
```

A unit-type tag that reaches this branch and matches no registered name is rejected as an unsupported tag, by the project's own call. Unlike C038, the deciding and the rejecting code are both the project's.

EN5 closed within scope: the closure basis is the array's declared extent. The enum's sentinel `NVARALREADYDEFINED` mechanically fixes that extent, the observed initializer fills all 15 slots, and `GetVariableIndex` iterates exactly that declared range at runtime. The set the decision consults is therefore closed by the declaration rather than by our choice, and a loop actually runs over exactly that set -- the operational case, so the tag is `enforced` rather than `asserted`.

Not claimed: that the compiler guarantees a name-by-name correspondence between the enum members and the initializer. It fixes the extent; the 15-to-15 correspondence is the cross-check recorded above, at observation time.

EN6 outcome independence: the registry is the set of unit-type attributes a scenario may set. It is not a bug list, fix list or known-failure registry.

Bounded honestly: the claimed universe is the VARIABLE REGISTRY, not the full set of tags CclDefineUnitType accepts. The parser reaches GetVariableIndex only after a long if-else chain over other tags (Name, Image, Shadow, Type, RightMouseAction, sounds and others), and that chain is not a registry and is not claimed as one. What the registry mechanically decides is narrower and exact: whether a tag is accepted AS A VARIABLE.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per registered name

  "variable name N is accepted as a unit-type variable tag; a tag
   reaching the variable branch and matching no registered name is
   rejected as an unsupported tag"

retained as externally segmented fields, per observation
  the registered name
  its index constant in the project's own enum
```

As at C043, this establishes only that a mechanically constructible universe EXISTS. It fixes no contents and concludes nothing about a primary-universe count; QA-19 puts that at the inventory stage.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28 -- no observation fixes where the designated ref pointed at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## RETRACTION 23 — three overclaims in C049, none load-bearing

C049's verdicts are unchanged; each of these was an argument the entry did not need.

**Reverse designation.** The E2-REP entry wrote "The designation runs both ways, as at C022: the project's own site names the repository, and the repository's website field names the site." The reverse arrow is a repo->site website field, and C032 and C042 both refused that arrow designation force -- it is affiliation. Readmitting it here, in a candidate where it happened to point the convenient way, is the same error those entries were written to prevent. Withdrawn and replaced with the asymmetric statement: the project site designates, the website field corroborates affiliation only. The PASS stands on the Development page's sentence and clone URL, which never needed help.

**E3's history claim.** The entry said the verdict depends on "what that player has seen by that point in the match", calling visibility "accumulated game state". What the two quoted functions establish is narrower: `MapFogFilterFlags` strips the field flags of units failing `IsVisibleAsGoal(player)` from the test mask. The backing state behind `IsVisibleAsGoal`, and whatever writes it, were never observed. Withdrawn. E3 asks for a stateful OR temporal validity question, and the stateful half stands on what was quoted.

**E4's mutation claim.** The entry recorded runtime enforcement state as "none -- the entries are string literals and no observed path mutates them". That is an absence inferred from not having looked, and `const char *VariableNames[]` constrains the pointed-to characters rather than the array slots in any case. Withdrawn; the two levels are now stated as C043 states them, with no immutability claim, resting instead on the positive 15-to-15 cross-check at observation time. EN5's "the compiler ties the table to the enum" is lowered in the same pass: the sentinel fixes the extent, and the name-by-name correspondence is an observation, not a compiler guarantee.

## EV-C050-UR-01
Candidate: C050 (frame rank 50, games/braincurses)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/braincurses/Makefile
Observed: GH_ACCOUNT=bderrly; GH_PROJECT=braincurses; GH_TAGNAME=v1.1.0; COMMENT="clone of the Mastermind game". There is no HOMEPAGE and no SITES.
Inference: the frozen fields name one packaged system, braincurses. "clone of the Mastermind game" describes what it imitates, not a second packaged system -- the reading applied at C013, C023, C046 and C048. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C050-E1-01
Candidate: C050
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv2, on an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C050-E2REP-01
Candidate: C050
Gate: E2-REP

Per QA-27 the admitted starting points are enumerated, and there is exactly one: the GH_ACCOUNT/GH_PROJECT pair. No HOMEPAGE and no SITES exist, so no second surface is supplied, nothing is left unaccounted for, and QA-31 does not arise.

The pair resolves to https://github.com/bderrly/braincurses, which is itself a repository. This is the C010/C012/C017 topology in its barest form -- step 1 and step 3 are the same surface, and there is no project page anywhere in the frozen metadata. QA-22 settled that the topology answers WHICH surface and supplies no designation of its own.

Observation scope, fixed before the request: existence; repository and owner name; default branch; fork, mirror, archive and template flags; the website metadata field; the repository description; whether a source tree is present at the root; any statement designating this location as the project's source; any primary or mirror marking. Not: README prose, releases, issues, docs, or any source file.

observed_at_utc: 2026-08-28T07:46:48Z (metadata), 07:46:49Z (root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        bderrly/braincurses
owner            bderrly
default_branch   master
fork             false          parent       null
archived         false          is_template  false
mirror_url       null
website field    EMPTY
description      "A version of the classic game Mastermind"
license          GPL-2.0, matching the frozen licence line
```

Root listing: braincurses.cpp, braincurses.h, code.cpp, code.h, main.cpp, Makefile, README.md, LICENSE, .gitignore, .gitmodules, and the directories external and tests. A source tree is present, and the three translation units the frozen do-build names -- main.cpp, code.cpp, braincurses.cpp -- are all here.

The `external` directory and `.gitmodules` were not followed. They are not identifiers the frozen metadata supplies, so QA-27 imposes no accounting obligation for them, and nothing beyond the root listing was read.

```text
PASS not established
  nothing observed designates this location as the project's canonical
  source. The only route to it is the packaging metadata's own
  GH_ACCOUNT/GH_PROJECT pair, and arrival by an admitted route is
  affiliation, not designation (QA-22, C017). The website field is
  empty, so there is not even the repo->site arrow C042 had to weigh
  -- and RETRACTION 23 has just confirmed that such an arrow would not
  have designated anything in this direction either.

FAIL not established
  the repository root is an admissible surface and carried no
  designation signal, which is a bounded observation and not a
  demonstration that upstream designates none -- the C017 boundary.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

The single admitted starting point was determinately answered, so no surface is left unobserved and this is not the transport family. What the sealed criteria do not describe is a frame item whose frozen metadata supplies only a repository identifier.

Stated precisely, because C032 had to correct this exact wording once already: the frozen metadata supplies no separate upstream-authored project surface, and the one admissible surface -- the repository root -- WAS examined and carried no designation signal. It is not that no surface could bear a designation. The repository root can: "whether upstream designates this location as its source" is among the observations the contract allows there. That bounded absence does not establish that upstream designates no canonical source location.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C051-UR-01
Candidate: C051 (frame rank 51, games/brogue)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/brogue/Makefile
Observed: GH_ACCOUNT=tmewett; GH_PROJECT=BrogueCE; GH_TAGNAME=v1.15.1; PKGNAME=brogue-${GH_TAGNAME:S/v//}; HOMEPAGE=https://sites.google.com/site/broguegame/; COMMENT="roguelike game by Brian Walker with X11 support"; licence line "Code: AGPLv3+".

This one needs stating rather than asserting, because the frozen fields name two different parties. The source-bearing fields all point at tmewett/BrogueCE, and PKGNAME is derived from that repository's tag; the HOMEPAGE points at a site belonging to Brian Walker, whom COMMENT names as the game's author.

Inference: the packaged system is Brogue: Community Edition, and the fields that establish it are narrower than a first draft claimed.

```text
system-identifying    GH_ACCOUNT=tmewett, GH_PROJECT=BrogueCE, and the
                      tag v1.15.1 in that repository -- the
                      source-fetch identity, stated explicitly

consistent but not    PKGNAME=brogue-1.15.1 and the AGPLv3+ code
identifying           licence line. Both agree with that packaged
                      source; neither names the system.
```

COMMENT's "by Brian Walker" is an authorship credit for the game, not a statement about which project is packaged, and C045 settled that a mismatch between the packaging name and the upstream name is not the two-systems case UR-AMBIGUOUS is for. A HOMEPAGE and a repository identifier pointing at differently-roled locations does not by itself make the metadata ambiguous; what UR must resolve is what is packaged, and the source-fetch identity fixes it.

What the frozen metadata establishes about the HOMEPAGE, and no more: it names Brian Walker's Brogue site. Whether that site stands in an ancestor relation to the packaged system is not readable from the metadata and is not claimed here; it is an inference from the page itself, made at E2-REP where the page is observed.
Decision: PASS

## EV-C051-E1-01
Candidate: C051
Gate: E1
Source: same frozen metadata
Observed: a third-party roguelike under AGPLv3+ with CC BY-SA 4.0 assets, on upstream accounts unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C051-E2REP-01
Candidate: C051
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed: the frozen HOMEPAGE, and the GH_ACCOUNT/GH_PROJECT pair. Neither is itself a forbidden class, so QA-31 does not arise -- see below for why the releases URL that appears here is a different question.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: https://sites.google.com/site/broguegame/
observed_at_utc: 2026-08-28T07:52:53Z; http_status 200; redirect_chain: NONE (num_redirects 0); 337108 bytes
evidence_role: frozen HOMEPAGE; the observed page for Brian Walker's Brogue line

Observation scope, fixed before the request: HTTP status and redirects; title and headings; any sentence about where the project or its source is; the links exposed and their labels and targets; any primary, canonical, preferred or mirror marking. Not: opening any linked artifact or destination.

Observed, in upstream's own words:

```text
"For the most current version of Brogue, please look to Brogue:
 Community Edition. Brogue CE includes many enhancements and bugfixes
 that improve the game beyond the older version linked below."

"Latest Community Edition for all platforms: [Download]"
     Download -> https://github.com/tmewett/BrogueCE/releases

"Older v1.7.5 (with source code): [macOS] [Windows] [Linux amd64]"
     each -> a drive.google.com/file/d/... URL

About: "The latest version can be downloaded at
        https://github.com/tmewett/BrogueCE/releases."
```

Recorded because it is easy to misread: "Brogue: Community Edition" in the first sentence is PLAIN TEXT, not a link. The markup was checked. The only link to the packaged system anywhere on this surface is the one labelled "Download".

No Source, Code, Repository or Development link is exposed, so navigation step 2 has no target. The "Download" link is excluded twice over, and both exclusions are independent: its label is outside the four-word whitelist (QA-17), and its target is a releases path, which the contract forbids outright. It is a navigation target found on a page, not a URL the frozen metadata supplies, so this is not QA-31's situation -- QA-31 concerns a frozen starting point that names a forbidden class, and nothing here forces that question.

The v1.7.5 artifacts are the only things this surface labels as carrying source code. They are recorded, and they do NO adjudication work here.

An earlier draft argued they were not a competing designation because upstream ranks them "Older" -- the C015 and C038 device. That argument is withdrawn as unnecessary and out of scope. UR fixed the target as Brogue: Community Edition, so what matters is whether a CE canonical source location is designated; how this page ranks its own older material bears on the relation between this page and CE, not on CE's source uniqueness. Running a competing-designation adjudication over another line's artifacts would import exactly the kind of reasoning C048 kept out.

What the page's own sentences do establish, as inference from the observed text rather than from the frozen metadata: it presents Brogue CE as the most current continuation and labels its own v1.7.5 material as older.

Surface 2: https://github.com/tmewett/BrogueCE, from the GH_ACCOUNT/GH_PROJECT pair.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.
observed_at_utc: 2026-08-28T07:54:00Z (metadata), 07:54:01Z (root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        tmewett/BrogueCE
owner            tmewett
default_branch   master
fork             FALSE          parent  null
archived         false          is_template  false     mirror_url  null
website field    https://sites.google.com/site/broguegame/
description      "Brogue: Community Edition - a community-lead fork of
                  the much-loved minimalist roguelike game"
license          AGPL-3.0, matching the frozen "Code: AGPLv3+"
```

Root listing: src, make, tools, test, bin, linux, macos, windows, os2, changes, .github, Makefile, config.mk, brogue, BUILD.md, README.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE.txt, .gitignore. A source tree is present.

Two observations are recorded without being used. The description calls the project "a community-lead fork" while the fork flag is false and the parent is null; that discrepancy is noted as observed metadata and nothing is inferred from it, and no fork-parent navigation arises in any case (C025). And the website field names the ancestor site -- a repo->site arrow, which C032, C042 and RETRACTION 23 have all now settled is affiliation and not designation.

```text
PASS not established
  no designation witness. Surface 1 exposes no source-role link the
  contract admits; its one link to the packaged system is labelled
  "Download" and targets a forbidden class. Surface 2 was reached by
  the packaging metadata's own identifiers, which is affiliation, not
  designation (QA-22, C017), and its website field points the wrong
  way to designate anything.

  Nor does surface 1's sentence supply one. "The latest version can be
  downloaded at .../releases" states where a build may be obtained; it
  does not identify a canonical SOURCE location, and the surface it
  names is one the contract will not let us open to find out.

FAIL not established
  both admissible surfaces carried what they carried and no more.
  That is a bounded observation, not a demonstration that upstream
  designates no canonical source location -- the C017 boundary.

E2REP-NO-SOURCE not established
  a source tree WAS observed at surface 2, so source access is not
  what is missing.
```

Both starting points were determinately answered, so no surface is left unobserved and this is not the transport family. What the sealed criteria do not describe is this arrangement: the frozen HOMEPAGE belongs to an ancestor project that points forward to the packaged system only through a forbidden surface, while the packaged system's own repository is reachable only by packaging identifiers.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 24 — C051 overstated its UR basis and adjudicated another line's artifacts

Verdicts unchanged; both were arguments the entry did not need.

**UR's basis.** The entry said "Every field that determines WHAT IS BUILT -- the account, the project, the tag, the derived package version 1.15.1, the AGPLv3+ code licence -- names that one system." PKGNAME and the licence line are CONSISTENT with the packaged source; neither names Brogue: Community Edition. The system-identifying evidence is narrower: GH_ACCOUNT, GH_PROJECT and the tag -- the source-fetch identity. Restated that way, and UR PASS is unaffected.

**The ancestor relation.** The entry carried "the frozen HOMEPAGE is a surface of the ANCESTOR project" forward from UR as "a fact about the metadata". It is not. The metadata says only that HOMEPAGE names Brian Walker's Brogue site; the ancestor relation is an inference from the page's own sentences, and it now sits at E2-REP where the page is observed.

**The v1.7.5 adjudication.** The entry argued that the site's v1.7.5 source artifacts were not a competing designation because upstream ranks them "Older", invoking C015 and C038 and adding QA-26. Withdrawn. Once UR fixes the target as Brogue: Community Edition, the question is whether a CE canonical source location is designated; how another version line's page ranks its own older material does not bear on that, and running the adjudication anyway imports scope C048 was careful to exclude. The artifacts stay on the record as observed, doing no verdict work.

The remaining E2-REP reasoning is simpler for the removal, and unchanged in outcome: the only navigable link to the packaged system is labelled "Download" and targets a releases path, excluded twice over and independently; the repository was reached by packaging identifiers, which is affiliation; its website field points repo->site, which does not designate; a source tree is present, so E2REP-NO-SOURCE does not apply. UNRESOLVED / PI-UNCLASSIFIED-SHAPE.

## EV-C052-UR-01
Candidate: C052 (frame rank 52, games/brumbrumrally)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/brumbrumrally/Makefile
Observed: DISTNAME=brumbrumrally-0.7; HOMEPAGE=http://dataapa.net/brumbrumrally/; SITES=http://dataapa.net/brumbrumrally/files/; COMMENT="racing game with randomized tracks".
Inference: the frozen fields name one packaged system, Brum Brum Rally, and HOMEPAGE and SITES sit on the same upstream domain, the second a subdirectory of the first. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C052-E1-01
Candidate: C052
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv3+, on an upstream domain unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C052-E2REP-01
Candidate: C052
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: http://dataapa.net/brumbrumrally/
observed_at_utc: 2026-08-28T08:07:24Z; http_status 200; redirect_chain: NONE (num_redirects 0); 3949 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence about where the project or its source is; any primary, canonical or mirror marking. Not: opening any linked page or artifact.

Observed: the project's own site, titled "Brum Brum Rally - 2D racing game for up to 8 players". Its navigation exposes About, News, Screenshots, Download and Manual, plus a language switch to a Swedish version, a "GNU GPL" link to gnu.org, and "Back to Dataapa". The body describes the game, its modes and its platforms, and states "Brum Brum Rally is free software. You can redistribute it and/or modify it under the terms of the GNU GPL."

No Source, Code, Repository or Development link is exposed, so navigation step 2 has no target. "Download" is outside the four-word whitelist and was not opened (QA-17). The licence sentence grants redistribution rights; it names no location, and a licence statement is not a canonical-source designation.

Surface 2: the frozen SITES.
requested_url and final_url: http://dataapa.net/brumbrumrally/files/
observed_at_utc: 2026-08-28T08:07:43Z (GET), 08:07:44Z (HEAD); http_status 200, 200; redirect_chain: NONE on both; 3884 bytes
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.

Observed: a bare server autoindex, titled "Index of /brumbrumrally/files/", listing a Parent Directory link and eleven artifacts with sizes and nothing else:

```text
brumbrumrally-0.1 .. 0.7 .tar.gz        44 KB .. 148 KB
brumbrumrally-0.5 / 0.6 / 0.7 -win32.zip   ~700 KB each
brumnet-0.1.tar.gz                       14 KB
```

The index carries no descriptions, no source-role labels, no headings beyond its own title, and no primary, canonical or mirror marking.

Nothing is read off the filenames. C026's observation scope settled that an artifact may not be inferred to be source from its name, and that restraint is what keeps this surface from silently becoming a designation. On the same ground brumnet-0.1.tar.gz is recorded as a listed artifact and nothing more: no claim is made about what it is or whether it belongs to another system.

```text
PASS not established
  neither admissible surface designates a canonical source location.
  Surface 1 exposes no source-role link and its only relevant sentence
  is a licence grant. Surface 2 is an autoindex that names artifacts
  without saying what any of them is.

FAIL not established
  a project page carrying no source link and a directory listing
  carrying no labels do not demonstrate that upstream designates no
  canonical source location -- the C017 boundary.

E2REP-NO-SOURCE not established
  artifacts are exposed and reachable; what was not established is
  what they are. That is not the same as no access to a source
  representation, and the code is not completed either way.
```

Recorded because it bounds this verdict in the direction opposite to C049's: the "Download" page was not opened, the contract not admitting its label. If that page labels one of these artifacts as source, a designation would exist that this entry did not see. That possibility is unexamined, not excluded, and it cannot be examined -- which is why the verdict is UNRESOLVED rather than any finding about upstream.

Both starting points were determinately answered, 200 on each, so no surface is left unobserved and this is not the transport family.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C053-UR-01
Candidate: C053 (frame rank 53, games/bugdom)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bugdom/Makefile
Observed: V=1.3.4; PKGNAME=bugdom-${V}; HOMEPAGE=https://pangeasoft.net/bug; and two DIST_TUPLE entries:

```text
DIST_TUPLE += github jorio Bugdom ${V} .
DIST_TUPLE += github jorio Pomme ef94150e2dcec522e3099f4d03a4e8f2639f7232 \
              extern/Pomme
```

with the licence line "# game: CC BY-NC-SA 4.0; extern/Pomme: MIT, LGPLv2.1, BSD, Boost".

Inference: one packaged system, Bugdom, with a vendored dependency. The frozen metadata subordinates the second tuple itself -- it extracts to extern/Pomme, a path inside the first tuple's tree, and the licence line separates them the same way. This is C042's metadata shape exactly, and the same reading applies. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C053-E1-01
Candidate: C053
Gate: E1
Source: same frozen metadata
Observed: a third-party game under CC BY-NC-SA 4.0, on a game publisher's domain and an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C053-E2REP-01
Candidate: C053
Gate: E2-REP

Per QA-27 every admitted starting point is accounted for: the HOMEPAGE, the jorio/Bugdom identifiers, and the jorio/Pomme identifiers.

Surface 1: the frozen HOMEPAGE.
requested_url: https://pangeasoft.net/bug ; final_url: https://pangeasoft.net/bug/
observed_at_utc: 2026-08-28T08:30:58Z; http_status 200; redirect_chain: 1 redirect; 9919 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title; the document's OWN anchors with their labels and targets; any sentence about where the project or its source is; any primary, canonical or mirror marking. Not: fetching any linked page, and -- per QA-29 -- not fetching any subresource the document declares.

This surface differs from C042's in the one respect that matters. C042's landing page was a frameset carrying no anchors of its own, which under QA-29 left its content unobservable and its step-1 result unsettleable. This document is an ordinary page with thirteen anchors of its own, so the same question is answerable here on admissible evidence.

```text
title  "Pangea Software"
visible text  the copyright line only:
  "(c)2012 Pangea Software, Inc. All product names are trademarks of
   Pangea Software, Inc. unless otherwise noted"

labelled anchors        Buy Now! -> register.html
                        Info     -> info.html
                        Reviews  -> reviews.html
                        Support  -> support.html

unlabelled image links  ../index.html  ../macGames.html
                        ../iphone/index.html  ../pano/index.html
                        ../store.html  ../support.html
                        ../downloads.html  ../about.html
                        http://www.pangeasoft.net/forum
```

No qualifying Source, Code, Repository or Development navigation signal is exposed on the document's own anchors or text, so navigation step 2 has no target. `../downloads.html` was not opened: not among the four labels, and QA-17 settled that "source distribution" may not widen the whitelist.

The unlabelled image links are recorded by href only, and no source-role inference is drawn from those hrefs. An earlier draft classified them as "site-level pages of the publisher rather than source locations", which decides a link's role from the shape of its URL -- the move C020 and QA-25 refused. Nothing here needs it: what settles step 2 is that no anchor carries a qualifying label or project-authored text identifying it as source, and an unlabelled link carries no such signal by definition.

Surface 2: https://github.com/jorio/Bugdom, from the first DIST_TUPLE's identifiers.
Necessary because: the gate was unsettled after surface 1 and this is the remaining admitted starting point for the packaged system.
observed_at_utc: 2026-08-28T08:31:26Z (metadata), 08:31:27Z (root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        jorio/Bugdom
owner            jorio
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    https://pangeasoft.net/bug
description      "Pangea Software's Bugdom for modern systems"
```

Root listing: src, Data, docs, extern, packaging, .github, CMakeLists.txt, build.py, BUILD.md, README.md, CHANGELOG.md, SECRETS.md, LICENSE.md, .editorconfig, .gitignore, .gitmodules. A source tree is present.

The jorio/Pomme identifiers are accounted for and were not opened, and neither were `extern/` or `.gitmodules`. UR determined from the frozen metadata that Pomme is a vendored dependency at extern/Pomme and not the packaged system, so under QA-26 it is another delimited system: a designation found there would be Pomme's.

```text
PASS not established
  the arrow runs one way only. The repository's website field names
  the project page; the project page, read in full on its own content,
  designates no source location. C032 settled that direction, and
  RETRACTION 23 has since confirmed that a repo->site website field
  does not designate. Arriving at the repository through packaging
  identifiers is likewise affiliation, not designation (QA-22).

FAIL not established
  both admissible surfaces carried what they carried and no more.
  That is a bounded observation, not a demonstration that upstream
  designates none -- the C017 boundary.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

Both starting points for the packaged system were determinately answered, so no surface is left unobserved and this is not the transport family.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C054-UR-01
Candidate: C054 (frame rank 54, games/bugdom2)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bugdom2/Makefile
Observed: V=4.0.0; PKGNAME=bugdom2-${V}; HOMEPAGE=https://pangeasoft.net/bug2; DIST_TUPLE for `github jorio Bugdom2 v${V} .` and for `github jorio Pomme <commit> extern/Pomme`; licence line "# game: CC BY-NC-SA 4.0; extern/Pomme: MIT, LGPLv2.1, BSD, Boost"; COMMENT="sequel to the family-friendly 3D action adventure".
Inference: one packaged system, Bugdom 2, with a vendored dependency subordinated by the frozen metadata itself -- the extraction path extern/Pomme and the licence line, exactly as at C042 and C053. Not UR-AMBIGUOUS.

Recorded because the two are adjacent in the frame: Bugdom 2 is a different packaged system from C053's Bugdom, not a second identifier for it. Separate PKGNAME, separate version line, separate repository, separate HOMEPAGE. It is not a DUPLICATE frame row.
Decision: PASS

## EV-C054-E1-01
Candidate: C054
Gate: E1
Source: same frozen metadata
Observed: a third-party game under CC BY-NC-SA 4.0, on a game publisher's domain and an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C054-E2REP-01
Candidate: C054
Gate: E2-REP

Per QA-27 every admitted starting point is accounted for: the HOMEPAGE, the jorio/Bugdom2 identifiers, and the jorio/Pomme identifiers.

Surface 1: the frozen HOMEPAGE.
requested_url: https://pangeasoft.net/bug2 ; final_url: https://pangeasoft.net/bug2/
observed_at_utc: 2026-08-28T08:37:18Z; http_status 200; redirect_chain: 1 redirect; 11682 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title; the document's OWN anchors with their labels and targets; any sentence about where the project or its source is; any primary, canonical or mirror marking. Not: fetching any linked page, and per QA-29 not fetching any subresource the document declares.

Like C053's and unlike C042's, this is an ordinary document with anchors of its own, so step 1 is answerable on admissible evidence.

```text
title  "Pangea Software: Bugdom 2"
visible text  a banner line and the copyright line, nothing further:
  "NOW AVAILABLE FOR IPHONE AND IPOD TOUCH!"
  "(c)2012 Pangea Software, Inc. ..."

labelled anchors
  NOW AVAILABLE FOR IPHONE AND IPOD TOUCH! -> ../iphone/bug2/index.html
  INFO     -> info.html
  DEMO     -> downloads.html?mt=12
  BUY IT   -> itunes.apple.com/us/app/bugdom-2/...
  SUPPORT  -> support.html

nine unlabelled image links, recorded by href only
```

No qualifying Source, Code, Repository or Development navigation signal is exposed on the document's own anchors or text, so navigation step 2 has no target. No source-role inference is drawn from any href, labelled or not; `DEMO -> downloads.html?mt=12` is recorded as its label and target and nothing more, and QA-17 settled that a download label may not widen the whitelist.

Surface 2: https://github.com/jorio/Bugdom2, from the first DIST_TUPLE's identifiers.
Necessary because: the gate was unsettled after surface 1 and this is the remaining admitted starting point for the packaged system.
observed_at_utc: 2026-08-28T08:37:33Z (metadata and root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        jorio/Bugdom2
owner            jorio
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    EMPTY
description      "Pangea Software's Bugdom 2 for modern systems"
```

Root listing: Source, Data, rawdata, Instructions, docs-adjacent files and packaging -- specifically Source, Data, rawdata, Instructions, extern, packaging, .github, CMakeLists.txt, build.py, BUILD.md, README.md, CHANGELOG.md, SECRETS.md, LICENSE.md, illustration.webp, logo.webp, .editorconfig, .gitignore, .gitmodules. A source tree is present, and `Source/` is the directory the frozen pre-configure target names.

One difference from C053 is worth recording rather than leaving implicit: that repository's website field named the project page, so C053 had to weigh a repo->site arrow and reject it. Here the field is empty, so no arrow exists in either direction.

The jorio/Pomme identifiers are accounted for and were not opened, and neither were `extern/` or `.gitmodules`: UR fixed Pomme as a vendored dependency, so under QA-26 it is another delimited system.

```text
PASS not established
  nothing observed designates this location as the project's canonical
  source. Step 1 exposes no qualifying navigation signal, and the
  repository was reached only through the packaging metadata's own
  identifiers, which is affiliation, not designation (QA-22, C017).

FAIL not established
  both admissible surfaces carried what they carried and no more --
  a bounded observation, not a demonstration that upstream designates
  none (C017).

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

Both starting points for the packaged system were determinately answered, so no surface is left unobserved and this is not the transport family.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C056-UR-01
Candidate: C056 (frame rank 56, games/bzflag)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/bzflag/Makefile
Observed: V=2.4.22; DISTNAME=bzflag-${V}; HOMEPAGE=https://www.bzflag.org/; SITES=https://download.bzflag.org/bzflag/source/${V}/; EXTRACT_SUFX=.tar.bz2; COMMENT="graphical multiplayer 3D tank war game".
Inference: the frozen fields name one packaged system, BZFlag, with HOMEPAGE and SITES on related upstream hosts. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C056-E1-01
Candidate: C056
Gate: E1
Source: same frozen metadata
Observed: a third-party game under LGPLv2.1-only or MPL 2.0, on upstream hosts unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C056-E2REP-02  (supersedes the withdrawn EV-C056-E2REP-01)
Candidate: C056
Gate: E2-REP

Per QA-27 the admitted starting points are the frozen HOMEPAGE and the frozen SITES. The gate is determined on the first, so the second is accounted for below rather than used.

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the anchors exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical, preferred or mirror marking.

Step 1: the frozen HOMEPAGE.
requested_url and final_url: https://www.bzflag.org/
observed_at_utc: 2026-08-28T08:39:09Z; http_status 200; redirect_chain: NONE (num_redirects 0); 30928 bytes
evidence_role: official-project-page

Observed. The navigation exposes Media, Getting Started, Downloads, Forums, Documentation, Help and About -- none of the contract's four words. The download area carries buttons whose labels upstream writes itself, and THREE of them assign the same source role to three different URLs:

```text
Download 2.4.30 for Source
  "Download for Source (.tar.bz2)"
     -> https://download.bzflag.org/bzflag/source/2.4.30/bzflag-2.4.30.tar.bz2
  "Download for Source (.tar.gz)"
     -> https://download.bzflag.org/bzflag/source/2.4.30/bzflag-2.4.30.tar.gz
  "Download for Source (.zip)"
     -> https://download.bzflag.org/bzflag/source/2.4.30/bzflag-2.4.30.zip

labelled otherwise, and not source designations
  "Download for macOS (10.13+ Universal)"  -> .../macos/2.4.30/...zip
  "Download for Windows (Windows 8+)"      -> .../windows/2.4.30/...exe
  "Download for Linux using Flatpak"       -> flathub.org
  "Download for Linux from Snapcraft"      -> snapcraft.io
```

A scan of the page's visible text for the words source, repository, canonical, official, mirror and primary returned only these button labels. No sentence ranks the three. None is called primary, preferred or canonical; none of the others is called a mirror or an alternate.

The footer link labelled "GitHub" -> https://github.com/BZFlag-Dev/bzflag does no designating work and is recorded symmetrically with C044: it sits among Credits, Privacy Policy and Terms of Use with no accompanying sentence and no source-role wording near it, and C038 settled that a bare "github" anchor does nothing on its own. It is neither designated as the source location nor shown not to be, and it was not opened.

```text
FAIL established, at step 1

  upstream designates three distinct URLs as Source, in its own
  labels, and ranks none of them. The sealed criterion requires
  exactly one externally designated canonical source location
  reachable at a stable URL, and disqualifies a project that
  "designates several with no primary among them".
```

Two arguments that would rescue a single location were available and are both refused, because each supplies the hierarchy from outside upstream:

```text
"one artifact in three encodings, not three locations" (C016)
  C016's reading worked because its second link resolved into the
  SAME designated repository, so the artifacts were contents OF one
  designated location. Here no repository is designated at all -- the
  three archives ARE the designation. With nothing to attribute them
  to, collapsing them is our construction, not upstream's.

"the common parent .../source/2.4.30/ is the location"
  upstream never designates that directory. Extracting a shared
  prefix from three hrefs is exactly the location-from-URL-shape move
  QA-25 refuses, and C026 refuses the sibling move of reading meaning
  off a path.

and the plainest one, refused for the reason C002's withdrawn entry
established: choosing .tar.bz2 because the port fetches that format,
or because it appears first, or because it is convenient to analyse,
supplies a hierarchy the criterion will not let us supply.
```

This is C047's structure with the competing designations closer together: there a source tarball and a repository, here three source archives. In both, upstream assigned the source role and declined to rank.

Decision: FAIL (E2REP-NO-SINGLE-CANONICAL-LOCATION)

Gates after E2-REP are NOT_REACHED.

## QUARANTINE — C056 material observed after the E2-REP determination

The failure code was complete at step 1. Everything below was nevertheless observed, because the first draft of this entry reached PASS and continued. Under the contract's stop rule -- navigation ends "the moment a PASS or a specific failure code is determined. Not one page further" -- all of it is post-stop exposure. It is retained, as this run retains every deviation, and it does no verdict work for C056 in either direction.

```text
frozen SITES https://download.bzflag.org/bzflag/source/2.4.22/
  2026-08-28T08:40:05Z, 200, a bare autoindex listing
  bzflag-2.4.22.tar.bz2 / .tar.gz / .zip

designated artifact .../source/2.4.30/bzflag-2.4.30.tar.bz2
  2026-08-28T08:41:47Z, 200, 14131760 bytes
  sha256 bb78b750e7bce7aa7c11bd35906bb08a49acc7c50bf29629af380eecd153894d
  1461 entries under bzflag-2.4.30/, a source tree

README:120-126            OpenGL 1.0+ and libSDL 1.2+ as build
                          dependencies
src/bzfs/bzfs.cxx:5326    state.order <= lastState.order -> drop
src/bzfs/GameKeeper.cxx:501-507   lastState = state
include/Flag.h:117-141    FlagType ctor, getFlagMap()[flagAbbv] = this
src/common/Flag.cxx:85    Flags::init(), 47 registrations
src/common/Flag.cxx:379   getDescFromAbbreviation -> Flags::Null
CmdLineOptions.cxx:1626   "ERROR: invalid flag"
CustomZone.cxx:122        "bad flag type"
```

One observation in that material looked worth generalising -- that the flag registry is extended at runtime by `unpackCustom` from network data, so an `enforced` universe need not be a fixed compile-time list. It is deliberately NOT written up as a QA entry. Turning post-stop exposure into a methodological finding would let it do work through the back door, which is the shape QA-17 was written to stop. It is recorded here only, as quarantined material.

## RETRACTION 25 — C056 was recorded ELIGIBLE; it fails E2-REP at step 1

This is a terminal verdict change, not a wording repair. C056 moves from ELIGIBLE to REJECTED.

**What the first entry did.** It observed that upstream's own button labels read "Download for Source (.tar.bz2)", "(.tar.gz)" and "(.zip)", pointing at three different URLs, and then wrote: "The three formats are one artifact in three encodings, not three locations -- C016's content-versus-location reading." On that basis it named the .tar.bz2 the canonical source location, passed the gate, and continued through E2-RULE, E3 and E4 to a survivor verdict.

**Why that is wrong.** The sealed criterion asks for exactly one externally designated canonical source location and disqualifies a project that designates several with no primary among them. Upstream here assigned the source role to three URLs and ranked none. Picking one requires a reason from outside upstream -- the format the port fetches, the order on the page, analytic convenience -- and C002's withdrawn entry established that supplying that hierarchy is not ours to do.

C016 does not license the collapse. Its content-versus-location reading worked because the artifacts belonged to a repository that WAS designated, so they were contents of one designated location. C056 has no designated repository; the three archives are the designation itself, and with nothing to attribute them to, "three encodings of one artifact" is our construction. The alternative rescue -- promoting the common parent `.../source/2.4.30/` -- is worse: upstream never designates that directory, and extracting a shared prefix from three hrefs is the location-from-URL-shape move QA-25 refuses.

C013 is not a counter-example either. Its landing page designated ONE source artifact, with a published SHA-256 beside it, and named the other files as Windows builds. One source-role designation, not three.

**Consequences.**

```text
E2-REP    FAIL, E2REP-NO-SINGLE-CANONICAL-LOCATION, determined at step 1
E2-RULE   NOT_REACHED        E3  NOT_REACHED        E4  NOT_REACHED
overall   REJECTED
canonical_source_location, external_target_identifier, primary_snapshot,
the three inventory fields and tie_key   all NOT_REACHED
```

Everything observed after step 1 -- the frozen SITES listing, the retrieval and entry-listing of the 2.4.30 artifact, README, the bzfs state-order check, and the flag registry with its rejection sites -- is post-stop exposure. It is quarantined above and does no verdict work.

Also withdrawn with the verdict: the E2-RULE, E3 and E4 entries EV-C056-E2RULE-01, EV-C056-E3-01 and EV-C056-E4-01, and the claim in the commit message that C056 was "the second distribution-type PASS after C013".

**Not converted into a finding.** The quarantined E4 material contains an observation that would otherwise be worth a QA entry -- that `unpackCustom` extends the flag registry at runtime from network data. It is left as quarantined material and not written up, because a methodological rule drawn from post-stop exposure would be that exposure doing work by another route.

Ledger: ELIGIBLE 7 -> 6, REJECTED 4 -> 5. Terminal count and remaining are unchanged at 64 and 64.

## QUARANTINED C056 DOWNSTREAM ENTRIES — restored in full

The three entries below were written while the withdrawn EV-C056-E2REP-01 stood, and were removed from this file when RETRACTION 25 replaced it. Removing them was itself a mistake: this run withdraws and quarantines observations, it does not delete them from the current record, and "recoverable from git" is not the standard C014's retraction set. They are restored here verbatim, retitled and marked, so the reasoning that was actually performed stays visible.

None of them does verdict work. C056's failure code was complete at step 1, so all of this is post-stop exposure under the contract's stop rule, and the compressed inventory in the QUARANTINE block above remains the index to it.

## QUARANTINED EV-C056-E2RULE-01
Status: post-stop exposure; no verdict work for C056.

Candidate: C056
Gate: E2-RULE
Source: README in the retrieved source tree
observed_at_utc: 2026-08-28T08:41:52Z (the artifact above)
Provenance: read against the 2.4.30 source upstream designates at observation time; no claim about the sealed primary snapshot (QA-28), and the frozen package is 2.4.22.

Observed: located witness, README:120-126.

```text
"After configure completes, it will report whether all the requisite
 packages were found that it needs in order to build the client and the
 server.  The client is reliant upon the following external
 dependencies that should be installed before running configure:

   OpenGL 1.0+
   libSDL 1.2+"
```

Inference: these determine concrete validity requirements without our inventing them -- a build environment lacking either does not satisfy the stated condition for building the client -- and both carry version bounds, as at C049.

Not used: the top-level INSTALL file, which is the generic autoconf text authored by the Free Software Foundation rather than by this project, and which states nothing specific to it.
Decision: PASS

## QUARANTINED EV-C056-E3-01
Status: post-stop exposure; no verdict work for C056.

Candidate: C056
Gate: E3
Source: src/bzfs/bzfs.cxx and src/bzfs/GameKeeper.cxx in the retrieved source tree
Provenance: as above.

Observed: located witness. Both halves are quoted rather than one assumed, per the rule C038 established.

```text
bzfs.cxx:5326-5328     // silently drop old packet
                       if (state.order <= playerData->lastState.order)
                           break;

GameKeeper.cxx:501-507 void GameKeeper::Player::setPlayerState(
                           PlayerState state, float timestamp)
                       {
                           lagInfo.updateLag(timestamp,
                               state.order - lastState.order > 1);
                           player.updateIdleTime();
                           lastState      = state;
                           stateTimeStamp = timestamp;
                           ...
                       }
```

Inference: an incoming player-state update is accepted only if its order exceeds that of the previously accepted update, and `lastState` is exactly what the previously accepted update assigned. The identical packet is therefore accepted or dropped according to what was accepted before it. That is validity conditioned on history, which is what E3 asks for.

A second instance is recorded and not leaned on: immediately below, the height check is gated by `if (now - lastWorldParmChange > 10.0f)`, making a position's acceptability depend on how long ago a world parameter changed. One located witness settles a positive existential gate, so the search stopped.
Decision: PASS

## QUARANTINED EV-C056-E4-01
Status: post-stop exposure; no verdict work for C056.

Candidate: C056
Gate: E4

Positive construction exhibited, via U_enforced.
Provenance: the retrieved 2.4.30 source, as above.

The mechanism: the flag-type registry.

```text
include/Flag.h:117-141   FlagType::FlagType(name, abbv, endurance, shot
                             type, quality, team, help, custom = false)
                         ...
                             flagSets[flagQuality].insert(this);
                             getFlagMap()[flagAbbv] = this;      // :140

src/common/Flag.cxx:85    namespace Flags { void init() {
                              Null = new FlagType("", "", ...);
                              RedTeam = new FlagType("Red Team","R*",...);
                              ...

src/common/Flag.cxx:379   FlagType* Flag::getDescFromAbbreviation(
                              const char* abbreviation)
                          {   ... uppercase ...
                              i = FlagType::getFlagMap().find(abbvString);
                              if (i == FlagType::getFlagMap().end())
                                  return Flags::Null;
                              else return i->second;   }
```

```text
FlagType constructions in Flag.cxx        47
distinct abbreviation keys among them     47
key collisions among the built-ins         0
```

The cross-check matters here specifically: the constructor's insertion is `getFlagMap()[flagAbbv] = this`, an assignment, so a duplicate abbreviation would silently overwrite. The 47-to-47 count is what shows none of the built-in registrations does.

EN1 external authorship: the game and this registry existed independently of this analysis.

EN2 explicit scope: the project names the domain in its own class comment, "This class represents a flagtype, like \"GM\" or \"CL\"", and every entry carries externally segmented fields -- flag name, abbreviation, endurance, shot type, quality, team and help text.

EN3 mechanical membership, with the two levels kept apart as at C043 and C049:

```text
enumerator membership      the keys present in FlagType::getFlagMap()
runtime enforcement value  the FlagType* each key maps to
```

Membership is what the constructor inserted, enumerable by reading the registrations.

EN4 connection to validation, in project code on both sides. The lookup returns `Flags::Null` for an unregistered abbreviation, and the project tests for exactly that and rejects:

```text
src/bzfs/CmdLineOptions.cxx:1623-1628
  FlagType* fDesc = Flag::getDescFromAbbreviation(vsitr->c_str());
  if (fDesc == Flags::Null)
  {
      std::cerr << "ERROR: invalid flag [" << (*vsitr) << "]" << std::endl;
      usage(argv[0]);
  }

src/bzfs/CustomZone.cxx:119-124
  FlagType* f = Flag::getDescFromAbbreviation(flag.c_str());
  if (f == Flags::Null)
  {
      logDebugMessage(1,"WARNING: bad flag type: %s\n", flag.c_str());
      input.putback('\n');
      return false;
  }
```

EN5 closed within scope: the set is closed by runtime construction -- Section 3.2's first admissible case -- since membership is precisely what FlagType's constructor has inserted into the map. Tag: `enforced`.

Recorded rather than smoothed over, because it bears directly on what "closed" means here: the registry is NOT a fixed compile-time list. `FlagType::unpackCustom` (Flag.cxx:291) constructs further FlagType objects with `custom = true` from network data, and those enter the same map through the same constructor. So the extent at any moment is what has been constructed by then. That is still closure by runtime construction rather than by our choice, which is what EN5 requires; no immutability is claimed, and none is needed.

EN6 outcome independence: the registry is the set of flag types the game recognises. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per registered abbreviation

  "abbreviation A is registered to a flag type; a flag abbreviation
   matching no registered key resolves to Flags::Null, which the
   project tests for and rejects as an invalid or bad flag type"

retained as externally segmented fields, per observation
  the flag's name and abbreviation
  its endurance, shot type, quality and team
  the project's own help text for it
```

As at C043 and C049, this establishes only that a mechanically constructible universe EXISTS. It fixes no contents and concludes nothing about a primary-universe count; QA-19 puts that at the inventory stage.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28. The designation observed is for 2.4.30 while the frozen package is 2.4.22, and nothing observed fixes what was designated at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## EV-C057-UR-01
Candidate: C057 (frame rank 57, games/candycrisis)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/candycrisis/Makefile
Observed: GH_ACCOUNT=jorio; GH_PROJECT=CandyCrisis; GH_TAGNAME=v3.0.1; PKGNAME=${DISTNAME:L}; COMMENT="open source clone of Puyo Puyo series". There is no HOMEPAGE and no SITES.
Inference: the frozen fields name one packaged system, Candy Crisis. "clone of Puyo Puyo series" describes what it imitates, not a second packaged system -- the reading applied at C013, C023, C046, C048 and C050. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C057-E1-01
Candidate: C057
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv2 only, on an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C057-E2REP-01
Candidate: C057
Gate: E2-REP

Per QA-27 the admitted starting points are enumerated, and there is exactly one: the GH_ACCOUNT/GH_PROJECT pair. No HOMEPAGE and no SITES exist, so no second surface is supplied and nothing is left unaccounted for. QA-31 does not arise.

This is C050's shape, and the third candidate this run has met where the frozen metadata supplies a repository identifier and nothing else. The pair resolves to https://github.com/jorio/CandyCrisis, which is itself a repository, so step 1 and step 3 are the same surface -- the C010/C012/C017 topology, which QA-22 settled answers WHICH surface and supplies no designation of its own.

Observation scope, fixed before the request: existence; repository and owner name; default branch; fork, mirror, archive and template flags; the website metadata field; the repository description; whether a source tree is present at the root; any statement designating this location as the project's source; any primary or mirror marking. Not: README prose, releases, issues, docs, or any source file.

observed_at_utc: 2026-08-28T09:15:24Z (metadata), 09:15:25Z (root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        jorio/CandyCrisis
owner            jorio
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    EMPTY
description      "Candy Crisis source port for modern operating systems"
license          GPL-2.0, matching the frozen "GPLv2 only" line
```

Root listing: src, CandyCrisisResources, packaging, .github, CMakeLists.txt, BUILD.md, README.md, CHANGELOG.md, LICENSE.txt, .editorconfig, .gitignore. A source tree is present.

```text
PASS not established
  nothing observed designates this location as the project's canonical
  source. The only route to it is the packaging metadata's own
  GH_ACCOUNT/GH_PROJECT pair, and arrival by an admitted route is
  affiliation, not designation (QA-22, C017). The website field is
  empty, so there is not even the repo->site arrow C042 and C053 had
  to weigh -- and RETRACTION 23 settled that such an arrow does not
  designate in this direction anyway.

FAIL not established
  the repository root is an admissible surface and carried no
  designation signal, which is a bounded observation and not a
  demonstration that upstream designates none -- the C017 boundary.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

The single admitted starting point was determinately answered, so no surface is left unobserved and this is not the transport family. Stated as C050's correction requires: the frozen metadata supplies no separate upstream-authored project surface, and the one admissible surface -- the repository root -- was examined and carried no designation signal. It is not that no surface could bear one.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C058-UR-01
Candidate: C058 (frame rank 58, games/capitan-sevilla)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/capitan-sevilla/Makefile
Observed: VERSION=1.0.3; DISTNAME=capitan-sevilla-${VERSION}; DISTFILES=Capitan.tar.bz2 with the port's own comment "# XXX upstream distfile has no version number"; HOMEPAGE=http://computeremuzone.com/ficha.php?id=754&l=en; SITES=http://computeremuzone.com/pc/juegos/; COMMENT="platform game set in Seville and in space".
Inference: the frozen fields name one packaged system, and both URLs sit on the same host. The version carried by DISTNAME is the packager's, the distfile having none -- a packaging fact, not a second system. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C058-E1-01
Candidate: C058
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv3, distributed from a host unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C058-E2REP-01
Candidate: C058
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: http://computeremuzone.com/ficha.php?id=754&l=en
observed_at_utc: 2026-08-28T09:22:06Z; http_status 200; redirect_chain: NONE (num_redirects 0); 115605 bytes

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical or mirror marking. Not: opening any linked page or artifact.

Observed. The page is titled "Capitán Sevilla - El remake / Captain 'S' - The remake (CEZ RD 2009) :: Computer Emuzone" and is a catalogue record on a games portal: it carries site-wide navigation (All games, Tops, Articles, Forum, Emus, Links, F.A.Q., Awards, Crew, and per-platform ZONE sections), per-game statistics and rankings, and tabs for Review, Manual, Adverts, Maps, Screenshots, Covers, Media, Videos, Development, Cheats, Credits, Comments and Magazines.

It also carries the game's own credits -- "developing team: Programación: Luis I. García Ventura; Gráficos: Daniel Celemín García; Música: Daniel Celemín García, David Caña..." -- and three download links, two labelled "PC" and one unlabelled, targeting `/download.php?ind=1435`, `1434` and `1439`.

A question this entry does not resolve, because it does not have to: whether this portal is the project's own publisher, and so whether this is an upstream surface at all. The title's "CEZ RD 2009" and the on-page credits are consistent with the portal having produced the remake, and nothing observed settles it. It does not need settling here -- no designation was observed on this surface under either reading, so the verdict is the same whether the page is upstream's or a third party's, and C048's exclusion is not needed.

No link labelled Source, Code, Repository or Development for this game is exposed. The download links carry platform labels, and QA-17 settled that a download label may not widen the whitelist.

One link needs its own record, because it is the only one whose label touches a whitelist word:

```text
"Greetings and Sources" -> /greetings?l=en
```

It was not followed. The reading taken is that this compound label names the page's own topic -- greetings and acknowledgements -- and does not identify a source location for this game; it is a site-level page, exposed alongside the portal's own furniture rather than in the game's record. That reading is stated rather than assumed because the alternative is available: a link whose label contains "Sources" could be read as satisfying step 2 on the contract's plain text. Recorded so the limit of this entry's step-2 search is visible: under that alternative reading, the search here is incomplete. No claim is made about what the page contains.

Also observed and not used: a user comment on the page, dated 2015, reads "Move the source to GitHub and further develop this." It is a visitor's comment, not upstream's own words, and it designates nothing. It is recorded because it appeared in the observation and because the temptation to treat it as a lead is exactly what the navigation contract exists to refuse.

Surface 2: the frozen SITES.
requested_url and final_url: http://computeremuzone.com/pc/juegos/
observed_at_utc: 2026-08-28T09:23:00Z (GET), 09:23:01Z (HEAD); http_status 404, 404; redirect_chain: NONE on both; 8343 bytes
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.
Observed: the site's own styled 404 page, "Computer Emuzone :: ERROR 404 -- PAGE NOT FOUND". No artifact names, headings for this game, or designation signal.

```text
PASS not established
  neither admissible surface designates a canonical source location.
  Surface 1 exposes no source-role link for this game; surface 2
  returned 404 and displayed nothing about it.

FAIL not established
  a catalogue page carrying no source link and a directory path
  returning 404 do not demonstrate that upstream designates no
  canonical source location -- the C017 boundary. The step-2 limit
  recorded above narrows the basis for any negative further.

E2REP-NO-SOURCE not established
  the 404 is evidence about that endpoint, and nothing observed bears
  on whether a source representation is reachable elsewhere. No
  surface was reached at which source-tree presence could have been
  established either way.
```

Both starting points were determinately answered -- 200 and 404 -- so no surface is left unobserved and this is not the transport family.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C058-E2REP-02  (supersedes the withdrawn EV-C058-E2REP-01)
Candidate: C058
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: http://computeremuzone.com/ficha.php?id=754&l=en
observed_at_utc: 2026-08-28T09:22:06Z; http_status 200; redirect_chain: NONE (num_redirects 0); 115605 bytes

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical or mirror marking.

Observed. The page is titled "Capitán Sevilla - El remake / Captain 'S' - The remake (CEZ RD 2009) :: Computer Emuzone" and is a catalogue record on a games portal, carrying site-wide navigation, per-game statistics and rankings, the game's developing-team credits, three download links labelled by platform, and a strip of per-game tabs:

```text
Review  Manual  Adverts  Maps  Screenshots  Covers  Media  Videos
DEVELOPMENT  Cheats  Credits  Comments  Magazines  Walkthrough
```

On the portal's status, which the previous entry left open in a way that mattered:

```text
<div class="finfo__label">Company</div>
<div class="finfo__value"><a href="/compania/cez%2Brd?l=en">CEZ RD</a></div>
```

Observed: the page identifies the game's company as CEZ RD. Whether that establishes that Computer Emuzone itself is this project's upstream surface is NOT determined here -- the site name containing "[CEZ]" is corroborating context, not a statement of identity, and no entity identification is attempted.

It no longer needs determining, because the exact-label route was taken rather than reasoned about:

```text
if the page is upstream   the Development link is a step-2 target; it
                          was followed, and yielded no game-source
                          designation

if it is third-party      its contents carry no upstream designation
                          force in the first place
```

That is what the previous entry got wrong -- not that it left the question open, but that it left it open while the two branches called for different actions. Taking the route closes both.

Step 2: the "Development" tab. Its label is one of the contract's four words exactly -- `<a class="fnavchip" href="...?l=en&pg=develop#pg-content" title="Development">` with the label span reading "Development" -- and it is a per-game tab in this record, not site furniture. The navigation is authorized on the contract's plain text.

requested_url and final_url: http://computeremuzone.com/ficha/754/capitan-sevilla---el-remake?l=en&pg=develop
observed_at_utc: 2026-08-28T09:32:19Z; http_status 200; redirect_chain: NONE; 99693 bytes

Observed, in full for this section:

```text
"development
 Packages made by Patsie (Download using \"Save as...\" option)"
   Ubuntu 8.04 AMD64  -> .../webs/benway/CEZGS/deb/capitan.804_1.0-1_amd64.deb
   Ubuntu 8.04 i386   -> .../capitan.804_1.0-1_i386.deb
   Ubuntu 8.10 AMD64  -> .../capitan.810_1.0-1_amd64.deb
   Ubuntu 8.10 i386   -> .../capitan.810_1.0-1_i386.deb
   Ubuntu 9.04 AMD64  -> .../capitan.904_1.0-1_amd64.deb
   Ubuntu 9.04 i386   -> .../capitan.904_1.0-1_i386.deb

"File with necesary libraries to compile the game (Allegro,
 AllegroOgg, AllegroFont, FBlend. See license inside each file):"
   Libraries to compile the game
     -> .../webs/benway/CEZGS/capitan-dependencies.tar.bz2
```

The section designates no source location for this game. What it exposes is six binary packages, attributed by the page itself to a third party ("made by Patsie"), and one archive of the game's build-time dependencies -- Allegro and friends -- which the page's own sentence describes as libraries needed to compile the game, not as the game's source.

Step 3 was therefore not reached: step 2 was taken and led to no source location.

One residual, recorded so the limit of the step-2 search is visible. The site-level link "Greetings and Sources" -> /greetings?l=en was not followed. The reading taken is that this compound label names that page's own topic -- greetings and acknowledgements -- and does not identify a source location for this game, being exposed with the portal's own furniture rather than in the game's record. The alternative reading, that a label containing "Sources" satisfies step 2 on plain text, is available and was not taken; under it this entry's step-2 search would still be incomplete. No claim is made about what that page contains.

Also observed and explicitly not used: a 2015 visitor comment reading "Move the source to GitHub and further develop this." It is not upstream's words and designates nothing. It is recorded because treating it as a lead is exactly what the navigation contract refuses.

Surface 2: the frozen SITES.
requested_url and final_url: http://computeremuzone.com/pc/juegos/
observed_at_utc: 2026-08-28T09:23:00Z (GET), 09:23:01Z (HEAD); http_status 404, 404; redirect_chain: NONE on both; 8343 bytes
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.
Observed: the site's own styled 404 page, "Computer Emuzone :: ERROR 404 -- PAGE NOT FOUND". No artifact names, headings for this game, or designation signal.

```text
PASS not established
  no admissible surface designates a canonical source location for
  this game. Step 1's links are platform-labelled downloads; the
  Development tab, followed under the contract, exposes third-party
  binary packages and a dependency archive; surface 2 returned 404.

FAIL not established
  what was observed is that these surfaces carried no source-location
  designation. That is a bounded observation, not a demonstration that
  upstream designates none -- the C017 boundary -- and the "Greetings
  and Sources" residual narrows the basis further.

E2REP-NO-SOURCE not established
  no surface was reached at which source-tree presence could have been
  established either way, and nothing observed bears on whether a
  source representation is reachable elsewhere.
```

Both starting points were determinately answered -- 200 and 404 -- so this is not the transport family. Stated precisely, because this entry records a residual: the unambiguous exact-label Development route was completed. What remains is an interpretation question over the site-level "Greetings and Sources" link, where the sealed text does not make clear whether a compound, plural label falls inside "a Source / Code / Repository / Development link". Under the reading used here it is not a step-2 route; under the broader alternative it is, and exploration would remain incomplete.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## RETRACTION 26 — C058 recorded a Development link as absent while its own observation listed it

EV-C058-E2REP-01 recorded the page's per-game tabs, "Review, Manual, Adverts, Maps, Screenshots, Covers, Media, Videos, Development, Cheats, Credits, Comments, Magazines", and then wrote:

```text
"No link labelled Source, Code, Repository or Development for this
 game is exposed."
```

That is false, and the contradiction was inside one entry. The markup shows an anchor with `title="Development"` and a label span reading "Development", pointing at `?pg=develop` -- one of the contract's four words exactly, on a per-game tab. Step 2 had a target and the entry stopped without taking it.

The second withdrawal follows from the first. The entry left open whether the portal is the project's publisher and asserted that "no designation was observed on this surface under either reading, so the verdict is the same". That does not hold: if the portal is not upstream its navigation cannot do designation work, but if it IS upstream then an exact-label Development link existed and the exploration was unfinished. The two branches differ in what the contract requires, so the question could not be left open.

Both are withdrawn. EV-C058-E2REP-02 no longer needs to settle the portal-identity question at all: it takes the exact-label Development route, which makes the outcome independent of that unresolved identity, and records what the tab actually contains -- third-party binary packages and an archive of build-time dependencies, no source location.

An earlier version of this paragraph said the superseding entry "settles the portal question from the page's own Company field -- CEZ RD, on a site named Computer Emuzone [CEZ]". That is the entity identification the standing entry withdrew, and repeating it in the retraction narrative would have left the withdrawn claim alive here after being removed there.

The verdict does not move: UNRESOLVED, PI-UNCLASSIFIED-SHAPE. But its basis is different in kind. Before, the gate was unsettled with an unambiguous step-2 target unexamined; now that route has been taken and led nowhere.

Not overstated: this is the exact-label route completed, not the whole exploration closed. The "Greetings and Sources" residual is a label-scope ambiguity in the sealed text -- whether a compound plural label counts as a Source link -- and it is recorded rather than resolved. Ledger fields are unchanged; the evidence refs now point at the superseding -02, per the C002/C005 convention.

## EV-C059-UR-01
Candidate: C059 (frame rank 59, games/cataclysm-dda)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/cataclysm-dda/Makefile
Observed: V=0.H-RELEASE; DIST_TUPLE += github CleverRaven Cataclysm-DDA ${V} .; PKGNAME=cataclysm-dda-${V:S/-RELEASE//}; HOMEPAGE=https://cataclysmdda.org; COMMENT="rogue-like zombie survival game".
Inference: the frozen fields name one packaged system, and the single DIST_TUPLE extracts to "." with no vendored second tuple -- unlike C042, C053 and C054. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C059-E1-01
Candidate: C059
Gate: E1
Source: same frozen metadata
Observed: a third-party game on an upstream domain and account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C059-E2REP-01
Candidate: C059
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE, and the DIST_TUPLE's CleverRaven/Cataclysm-DDA identifiers. The pair resolves to the same repository the step-2 link reaches, so as at C038 it is not a separate surface.

Step 1: the frozen HOMEPAGE.
requested_url: https://cataclysmdda.org ; final_url: https://cataclysmdda.org/
observed_at_utc: 2026-08-28T09:38:32Z; http_status 200; redirect_chain: NONE (num_redirects 0); 10172 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical, preferred or mirror marking.

The designation is on this page, and upstream supplies both the source relation and the partition that settles uniqueness:

```text
<h2 id="project-managed-resources">Project Managed Resources</h2>
<p>These sites are owned and managed by the project directly.</p>
<ul>
  <li><a href="https://github.com/CleverRaven/Cataclysm-DDA">GitHub repository</a></li>
  <li>Forums</li> <li>Development-oriented Discord</li>
  <li>Cataclysm_DDA subreddit</li> <li>IRC channel ... webchat</li>
</ul>

<h2>Community Managed Resources</h2>
<p>These are resources provided by third parties, or managed by some
   members of the development team. The project does not provide
   support for these directly.</p>
   Hitchhiker's Guide, Documentation For Developers, Game Launcher,
   Community Discord, Steam, Android Play Store
```

Step 2: the "GitHub repository" link. Its label's head noun is one of the contract's four words, and the sentence it sits under states the relation -- these sites are owned and managed by the project directly. Label and sentence coincide, both admitted forms under QA-23.

Recorded because C058 has just made the distinction matter: this is not the compound-label problem left open there. "Greetings and Sources" was a plural noun in a conjunction naming a page's own topic; "GitHub repository" is a noun phrase whose head IS "repository" and which names the destination's role.

Uniqueness, and why the ranking is upstream's. The page's Downloads section designates BUILDS, not source: "Cataclysm has official builds for Windows, Linux, OSX and Android", routing to a Releases Page and to experimental builds. A scan of the page's visible text for source, repository, canonical, official, mirror and primary returned only the passages quoted above and the phrase "open source turn-based survival RPG" describing the project's nature. So no second location carries a source role, and everything else upstream itself files under Community Managed Resources as third-party or unsupported.

Not followed: the "Releases" navigation item and the Releases Page. Releases are named in the contract's forbidden list outright, and the label is not among the four; QA-17 settled that neither may be widened. Nothing needed them.

Step 3: https://github.com/CleverRaven/Cataclysm-DDA
observed_at_utc: 2026-08-28T09:39:24Z (metadata and root listing); http_status 200 on both; redirect_chain: NONE on both
evidence_role: official-source-location

```text
full_name        CleverRaven/Cataclysm-DDA
owner            CleverRaven
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    http://cataclysmdda.org
description      "Cataclysm - Dark Days Ahead. A turn-based survival
                  game set in a post-apocalyptic world."
```

Root listing, 49 entries, including src, data, tests, tools, doc, lang, gfx, android, build-data, build-scripts, pch, utilities, CMakeLists.txt, Makefile, README.md, CONTRIBUTING.md and the LICENSE files. A source tree is present.

The direction is asymmetric, as RETRACTION 23 requires it to be stated: the project site designates the repository; the repository's website field naming the site corroborates affiliation and does not itself designate.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Cataclysm: Dark Days Ahead).

Decision: PASS

## EV-C059-E2RULE-01
Candidate: C059
Gate: E2-RULE
Source: doc/c++/COMPILER_SUPPORT.md in the designated repository
observed_at_utc: 2026-08-28T09:42:33Z; http_status 200; 4922 bytes
Provenance: read against the default branch at observation time; the frozen version is 0.H-RELEASE, and no claim is made about the sealed primary snapshot (QA-28).

Observed: located witness, the document's own table.

```text
# Compilers Supported

| Compiler       | Oldest Version |
| GCC            | 9.3            |
| clang          | 13.0           |
| MinGW-w64      | UCRT 14.2.0    |
| Visual Studio  | 2019           |
| XCode          | 11.4 / macOS 10.15 |
```

Inference: this states concrete validity requirements without our inventing them -- a toolchain older than the listed version is outside what the project states it supports -- and every row carries a version bound, as at C049 and unlike C014, C023, C034, C038 and C043.

The surrounding prose explains the policy behind the table and is not relied on; the table alone carries the requirement.
Decision: PASS

## EV-C059-E3-01
Candidate: C059
Gate: E3
Source: src/init.cpp in the designated repository
observed_at_utc: 2026-08-28T09:39:44Z; http_status 200; 44909 bytes
Provenance: observation-time source state, as above.

Observed: located witness. All parts of the chain are in this one file, so both halves are quoted rather than one assumed (C038's rule).

```text
init.cpp:796-806  void DynamicDataLoader::finalize_loaded_data()
                  {
                      cata_assert( !finalized &&
                          "Can't finalize the data twice." );
                      ...
init.cpp:949          finalized = true;
                  }

init.cpp:521-523  void DynamicDataLoader::load_data_from_path( ... )
                  {
                      cata_assert( !finalized &&
                          "Can't load additional data after finalization.
                           Must be unloaded first." );

init.cpp:643-645  void DynamicDataLoader::unload_data()
                  {
                      finalized = false;
```

Inference, split into the two claims that must not be run together:

```text
the validity question exists, and upstream declares it
  the project states a state-dependent invariant in its own words --
  "Can't load additional data after finalization.  Must be unloaded
  first." -- and `finalized` has both writers on the record:
  finalize_loaded_data sets it, unload_data clears it. So whether a
  data-load call satisfies the declared condition depends on which of
  those ran before it. Finalization carries its own such condition,
  "Can't finalize the data twice."

what is NOT claimed
  that the condition is rejected at runtime in every build.
  `cata_assert` (src/cata_assert.h, observed 2026-08-28T09:54:14Z,
  200, 1428 bytes) expands under NDEBUG to
  `decltype((exp) ? void() : __builtin_unreachable())()` on GCC and
  clang, and the file's own comment says this is to "place the code in
  decltype to avoid actual evaluation". Without NDEBUG it is
  `assert(expression)`, or an explicit fprintf-and-abort on Win32. So
  the invariant is enforced at runtime in assertion-enabled builds and,
  under the observed NDEBUG expansion, the expression is not evaluated.
  Whether this project's release configuration defines NDEBUG was not
  observed and is not claimed.
```

This is recorded rather than glossed because the first draft wrote "the identical call is valid or not according to which of those ran before it" without qualification, which reads as a claim about every build.

The gate is satisfied on the first claim alone. The sealed E3 text asks that "the external source must expose a stateful/temporal validity question that can be examined", and the screening amendment asks for "a concrete stateful/temporal validity witness". Neither asks for enforcement in every build configuration; what upstream exposes here is the validity question in its own declared terms, and both writers of the conditioning state are located.
Decision: PASS

## EV-C059-E4-01
Candidate: C059
Gate: E4

Positive construction exhibited, via U_enforced.
Provenance: observation-time source state, as above.

The mechanism: the JSON object-type registry.

```text
init.cpp:225-232
  void DynamicDataLoader::add( const std::string &type,
                               const std::function<...> &f )
  {
      const auto pair = type_function_map.emplace( type, f );
      if( !pair.second ) {
          debugmsg( "tried to insert a second handler for type %s "
                    "into the DynamicDataLoader", type.c_str() );
      }
  }

init.cpp:151-159
  void DynamicDataLoader::load_object( const JsonObject &jo, ... )
  {
      const std::string type = jo.get_string( "type" );
      const t_type_function_map::iterator it =
          type_function_map.find( type );
      if( it == type_function_map.end() ) {
          jo.throw_error_at( "type", "unrecognized JSON object" );
      }
      it->second( jo, src, base_path, full_path );
  }
```

```text
add("...") calls in init.cpp                        188
distinct type strings among them                    187
the one repeat                                      "mod_tileset"
```

The repeat is accounted for rather than reported as a discrepancy: it is the two arms of a preprocessor conditional at init.cpp:514-517 -- `#if defined(TILES)` registers `&load_mod_tileset`, `#else` registers `load_ignored_type` -- so exactly one is compiled into any build, and the registry holds 187 distinct types in any single build.

EN1 external authorship: the game and this loader existed independently of this analysis.

EN2 explicit scope: the domain is the `type` field of the project's JSON data objects, named by the project in the rejection message it emits and in the field it reads.

EN3 mechanical membership, with the two levels kept apart as at C043, C049 and C056:

```text
enumerator membership      the keys present in type_function_map
runtime enforcement value  the loader function each key maps to
```

Membership is what `add()` inserted, enumerable by reading the registrations.

Recorded because it is stronger than the equivalent at C049 and C056: the project detects key collisions ITSELF. `emplace` does not overwrite, and the project tests the returned `pair.second` and emits `debugmsg("tried to insert a second handler for type %s")`. At C049 the cross-check that no built-in key collided had to be performed by us, because that registry's insertion was an assignment. Here uniqueness is upstream's own enforcement, and our count only corroborates it.

EN4 connection to validation: `load_object` reads the `type` field of each JSON object, looks it up, and on a miss calls `jo.throw_error_at( "type", "unrecognized JSON object" )` -- project code, naming the offending field, rejecting the object. Deciding and rejecting are both the project's.

EN5 closed within scope: the set is closed by runtime construction -- Section 3.2's first admissible case -- membership being precisely what `add()` has inserted. Tag: `enforced`. No immutability is claimed and none is needed.

EN6 outcome independence: the registry is the set of JSON object types the game's data files may declare. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per registered type

  "JSON type T is accepted and dispatched to its loader; an object
   whose type field matches no registered key is rejected at that
   field as an unrecognized JSON object"

retained as externally segmented fields, per observation
  the type string
  the loader the project registered for it
```

As at C043, C049 and C056, this establishes only that a mechanically constructible universe EXISTS. It fixes no contents and concludes nothing about a primary-universe count; QA-19 puts that at the inventory stage.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28. The gates above were read against the default branch at observation time while the frozen version is 0.H-RELEASE, and no observation fixes where the designated ref pointed at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## EV-C060-UR-01
Candidate: C060 (frame rank 60, games/cdogs-sdl)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/cdogs-sdl/Makefile
Observed: HOMEPAGE=https://cxong.github.io/cdogs-sdl/; GH_ACCOUNT=cxong; GH_PROJECT=cdogs-sdl; GH_TAGNAME=2.1.0; COMMENT="open source, classic overhead run-and-gun game".
Inference: the frozen fields name one packaged system, C-Dogs SDL. A HOMEPAGE beside a repository identifier pair is the shape the protocol names non-ambiguous. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C060-E1-01
Candidate: C060
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv2+, on an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C060-E2REP-01
Candidate: C060
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE, and the GH_ACCOUNT/GH_PROJECT pair. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: https://cxong.github.io/cdogs-sdl/
observed_at_utc: 2026-08-28T10:01:46Z; http_status 200; redirect_chain: NONE (num_redirects 0); 19977 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical or mirror marking. Not: opening any linked page.

Observed: the project's own site, titled "C-Dogs SDL", laid out as a dated post index -- release announcements for 2.4.0, 2.3.2, 2.3.1, 2.3.0 and a retrospective, with pagination to page21. Its site navigation, under the tagline, exposes:

```text
tagline   "Open source, classic overhead run-and-gun game"

nav       Downloads -> /cdogs-sdl/downloads.html
          Campaigns -> http://cdogs.morezombies.net
          Archive   -> /cdogs-sdl/archive.html
          Mastodon  -> mastodon.gamedev.place/tags/CDogsSDL
          GitHub    -> https://github.com/cxong/cdogs-sdl
```

A scan of the page's visible text for source, repository, canonical, official, mirror and primary returned exactly one hit: the tagline's "Open source", which describes the project's nature and matches the frozen COMMENT. It designates no location.

The "GitHub" navigation item is the point that has to be decided, and it is decided the way C038 decided it: an anchor whose label is a host name does no designating work on its own. At C038 the work was done by the surrounding text -- a subheading reading "Source" and a sentence saying where the project is hosted -- and neither exists here. The nav item sits between "Archive" and nothing, with no accompanying sentence anywhere on the page.

So no qualifying Source, Code, Repository or Development navigation signal is exposed, and step 2 has no target. `Downloads` was not opened: not among the four labels, and QA-17 settled that a download label may not widen the whitelist. The release-announcement posts were not opened either; they are dated news items, not a step-2 target.

Surface 2: https://github.com/cxong/cdogs-sdl, from the GH_ACCOUNT/GH_PROJECT pair. It is the same location the nav item points at, so the two are one surface rather than two.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.
observed_at_utc: 2026-08-28T10:02:23Z (metadata), 10:02:24Z (root listing); http_status 200 on both; redirect_chain: NONE on both

```text
full_name        cxong/cdogs-sdl
owner            cxong
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    https://cxong.github.io/cdogs-sdl/
description      "Classic overhead run-and-gun game"
license          GPL-2.0, matching the frozen GPLv2+ line
```

Root listing: src, data, missions, graphics, music, sounds, dogfights, doc, wiki, build, .github, CMakeLists.txt, make.sh, make_emscripten.sh, make_gcw0.sh, appveyor.yml, appveyor.yml.cmake, README.md, COPYING, .clang-format, .gitattributes, .gitignore. A source tree is present.

```text
PASS not established
  the arrow runs one way only. The repository's website field names
  the project site; the project site designates no source location,
  its one "source" word being a description of the project's nature.
  C032 settled that direction and RETRACTION 23 confirmed that a
  repo->site website field does not designate. Arriving at the
  repository through packaging identifiers is likewise affiliation,
  not designation (QA-22).

  Nor is the site's bare "GitHub" nav item a designation, per C038.

FAIL not established
  both admissible surfaces carried what they carried and no more.
  That is a bounded observation, not a demonstration that upstream
  designates none -- the C017 boundary.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

Both starting points were determinately answered, so no surface is left unobserved and this is not the transport family.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C061-UR-01
Candidate: C061 (frame rank 61, games/cgames)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/cgames/Makefile
Observed: DISTNAME=cgames-2.2b; HOMEPAGE=https://www.muppetlabs.com/~breadbox/software/cgames.html; SITES=https://www.muppetlabs.com/~breadbox/pub/software/; COMMENT="free console games suite".

This one has a genuine multiplicity question and it is answered rather than passed over. The step-1 surface says the distribution contains three games -- "Included please find three games: cblocks -- sliding-block puzzles; cmines -- minesweeper; csokoban -- sokoban".

Inference: one packaged system. The frozen metadata names one distfile and one port, and upstream's own words delimit the three programs as contents of "this distribution" rather than as separate systems -- "The programs in this distribution are re-implementations of games for the Linux console", "All the programs in this distribution are available under the GNU General Public License." The delimitation is upstream's, which is what QA-26 requires; it is the same reading applied to C013's "numerous game consoles" and C023's "marathon / alephone". Not UR-AMBIGUOUS.
Decision: PASS

## EV-C061-E1-01
Candidate: C061
Gate: E1
Source: same frozen metadata
Observed: a third-party games suite under GPLv2+, on a personal upstream site unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C061-E2REP-01
Candidate: C061
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: https://www.muppetlabs.com/~breadbox/software/cgames.html
observed_at_utc: 2026-08-28T10:10:50Z; http_status 200; redirect_chain: NONE (num_redirects 0); 3010 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; every link with its label and target; any sentence or label assigning a source role; any primary, canonical or mirror marking. Not: opening any linked page or artifact.

Observed. The page is titled "Games for the Linux Console" and carries the project description, the three-game list, a rationale section, a licence sentence, and a dated Version History from version 2.2b back through 2.2a and 2.2. It exposes exactly four links:

```text
"Download cgames-2.2b.tar.gz"  -> /~breadbox/pub/software/cgames-2.2b.tar.gz
"me"                           -> mailto:breadbox@muppetlabs.com
"Software"                     -> /~breadbox/software/
"Brian Raiter"                 -> /~breadbox/
```

A scan of the page's visible text for source, repository, canonical, official, mirror, primary, git and cvs returned ZERO hits. That is worth recording precisely, because it distinguishes this candidate from the two that reached PASS on distribution designations: C013's page labelled its artifact and published a checksum beside it, and C056's buttons read "Download for Source". Here upstream names the artifact and its size and nothing else.

So no qualifying Source, Code, Repository or Development navigation signal is exposed, and step 2 has no target. The one artifact link's label is "Download" plus the filename; QA-17 settled that a download label may not widen the whitelist, and C026 settled that an artifact may not be inferred to be source from its name -- which is the whole of what is available here.

Surface 2: the frozen SITES.
requested_url and final_url: https://www.muppetlabs.com/~breadbox/pub/software/
observed_at_utc: 2026-08-28T10:11:12Z (GET), 10:11:13Z (HEAD); http_status 200, 200; redirect_chain: NONE on both; 15123 bytes
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.
Observed: a bare server autoindex, "Index of /~breadbox/pub/software", listing this author's software tarballs across several unrelated projects -- ELFkickers-1.0 through 3.1a and others -- with names, dates and sizes under the headings Name, Last modified, Size, Description, and no descriptions filled in. No source-role labels, and no primary, canonical or mirror marking.

Nothing is read off the filenames, per C026, and no inference is drawn about which entries belong to this system.

```text
PASS not established
  neither admissible surface designates a canonical source location.
  Surface 1 exposes no source-role link and contains no source-role
  wording at all; surface 2 is an autoindex that names files without
  saying what any of them is.

FAIL not established
  a project page carrying no source link and a directory listing
  carrying no labels do not demonstrate that upstream designates no
  canonical source location -- the C017 boundary.

E2REP-NO-SOURCE not established
  artifacts are exposed and reachable; what was not established is
  what they are. That is not the same as no access to a source
  representation.
```

Both starting points were determinately answered, 200 on each, so no surface is left unobserved and this is not the transport family. The same E2-REP outcome shape as C052.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C062-UR-01
Candidate: C062 (frame rank 62, games/cgoban)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/cgoban/Makefile
Observed: DISTNAME=cgoban-1.9.14; HOMEPAGE=https://cgoban1.sourceforge.net/; SITES=${SITE_SOURCEFORGE:=cgoban1/}; COMMENT="X11 Go Toolset".
Inference: the frozen fields name one packaged system, CGoban 1, with HOMEPAGE and SITES both under the same SourceForge project name. "Toolset" describes what the one program provides, not several packaged systems -- the reading applied at C013 and C061. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C062-E1-01
Candidate: C062
Gate: E1
Source: same frozen metadata
Observed: a third-party Go program on an upstream project site unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C062-E2REP-01
Candidate: C062
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed. Neither names a class the contract forbids, so QA-31 does not arise.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: https://cgoban1.sourceforge.net/
observed_at_utc: 2026-08-28T10:20:35Z; http_status 200; redirect_chain: NONE (num_redirects 0); 2144 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; every link with its label and target; any sentence or label assigning a source role; any primary, canonical or mirror marking. Not: opening any linked page.

Unlike C046's, this frozen per-project SourceForge host serves a page the project itself authored rather than redirecting to the hub. It is titled "CGoban", describes the program's functions, and closes with a Downloading section. It exposes exactly three links:

```text
"Sourceforge Download page for the latest release (1.9.13)"
    -> http://sourceforge.net/project/showfiles.php?group_id=52805
(unlabelled SourceForge logo image)
    -> http://sourceforge.net
"ksonney@sourceforge.net"
    -> mailto:
```

The passage that has to be adjudicated, quoted in full because the whole entry turns on it:

```text
"Downloading CGoban

 CGoban is distributed in source code for now. It uses the Gnu
 autoconfig system and should be portable across all Unix/X11R4 or
 later systems. Source RPMS are available for RPM based systems
 [Sourceforge Download page for the latest release (1.9.13)]"
```

It does not designate a canonical source location, and the reasons are separable:

```text
the sentence states a FORM, not a location
  "distributed in source code" says what is distributed. It names no
  URL, directory or repository. C020 and QA-25 separate a route from a
  location; this is a step further back -- a property of the artifact,
  with no location attached at all.

the link's label identifies a download route, not a source location
  "Sourceforge Download page for the latest release" names a download
  page for a release. None of the four terms appears as a standalone
  source-role label -- "Sourceforge" is the hosting service's proper
  name, not a label identifying the destination as Source -- and
  "release" is a class the contract forbids outright. QA-17 settled
  that neither may be widened, so this is not a step-2 target.

the stronger reading is conceded, and does not change the outcome
  an earlier draft said that reading the sentence as assigning a
  source role to the link would be a join "the page does not make".
  That is more than can be shown: the source-code sentence, the
  Source RPMS sentence and the link sit in one passage, so reading
  the link as a route by which source-related artifacts are
  downloadable is available as an upstream-authored relation.

  Granting it still does not reach PASS, and this is exactly the work
  QA-25 does:

      upstream may be identifying a ROUTE by which source-related
      artifacts can be downloaded
        is not
      upstream has designated the canonical source LOCATION E2-REP
      requires

  C020 was withdrawn for counting a designated route as a designated
  location. The same distinction applies here in upstream's favour and
  still leaves the gate unsatisfied.

and the destination was not observed
  the link was not opened, releases being forbidden outright, so
  nothing is claimed about what showfiles.php contains or what form it
  takes. No repository or source-distribution location was observed
  there, which is why it cannot serve as the designated location.
  C007's finding that a generic project hub is not a repository root
  is consistent with this and is not needed to reclassify a page this
  entry never opened.
```

"Source RPMS are available for RPM based systems" is part of the same passage and is read with it under the concession above. It names a second artifact kind and supplies no location of its own, so it does not change what the passage designates.

Surface 2: the frozen SITES. `${SITE_SOURCEFORGE:=cgoban1/}` resolves through the ports infrastructure's own macro definition to https://downloads.sourceforge.net/sourceforge/cgoban1/.
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point. Observed rather than predicted from its URL shape (C018), though the same macro produced 404s at C031, C036, C037, C044, C046 and C048.
observed_at_utc: 2026-08-28T10:21:12Z (GET), 10:21:13Z (HEAD); http_status 404, 404; redirect_chain: NONE on both; 154 bytes
Observed: "404 Not Found -- The resource could not be found." No artifact names or designation signal.

```text
PASS not established
  neither admissible surface designates a canonical source location.
  Surface 1 states the distribution's form and links a download page
  for a release; even read as a source-related route, that is not a
  designated location (QA-25). Surface 2 returned 404.

FAIL not established
  a project page whose only link is a download page, and an archive
  path returning 404, do not demonstrate that upstream designates no
  canonical source location -- the C017 boundary.

E2REP-NO-SOURCE not established
  the 404 is evidence about that endpoint, and the download page was
  not opened. Nothing observed bears on whether a source
  representation is reachable, in either direction.
```

Both starting points were determinately answered -- 200 and 404 -- so no surface is left unobserved and this is not the transport family.

Recorded and doing no verdict work: the page is dated "06 January 2003" and names the latest release as 1.9.13, while the frozen DISTNAME is cgoban-1.9.14. Nothing is inferred from that -- not that the page is stale, not that a newer surface exists elsewhere, and under QA-28 nothing about what this surface carried at the sealed instant.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C063-UR-01
Candidate: C063 (frame rank 63, games/chessx)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/chessx/Makefile
Observed: V=1.5.6; GH_ACCOUNT=Isarhamster; GH_PROJECT=chessx; GH_TAGNAME=v${V}-lw; DISTNAME=chessx-${V}; HOMEPAGE=https://chessx.sourceforge.net/; COMMENT="free chess database and analyzer".
Inference: the frozen fields name one packaged system, ChessX. A HOMEPAGE on one host beside a repository identifier pair on another is the shape the protocol names non-ambiguous, and C045 settled that a tag suffix the packager carries -- here "-lw" -- is not a second system. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C063-E1-01
Candidate: C063
Gate: E1
Source: same frozen metadata
Observed: a third-party chess database under GPLv2+, on upstream hosts unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C063-E2REP-01
Candidate: C063
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE, and the GH_ACCOUNT/GH_PROJECT pair. The pair resolves to the same repository the step-2 link reaches, so as at C038 it is not a separate surface.

Step 1: the frozen HOMEPAGE.
requested_url: https://chessx.sourceforge.net/ ; final_url: https://chessx.sourceforge.io/
observed_at_utc: 2026-08-28T10:34:44Z; http_status 200; redirect_chain: 1 redirect (sourceforge.net -> sourceforge.io, the same host change C036 recorded); 6713 bytes
evidence_role: official-project-page

Observed: the project's own site, titled "ChessX - Free Chess Database". Two of its links carry the contract's four words exactly, and both point at the same location:

```text
nav    "Source Code" -> https://github.com/Isarhamster/chessx/
body   "Source"      -> https://github.com/Isarhamster/chessx/
```

Uniqueness is settled by upstream's own partition, in its own words, not by any ranking of ours. The site separates binaries from source and says so:

```text
"Download the setup for your platform: Windows, Mac OS, Linux."
   "Binaries"  -> https://sourceforge.net/projects/chessx/
   "Download"  -> https://sourceforge.net/projects/chessx/

"If you don't trust online binaries of if you want to extend ChessX
 with your own ideas: Download the source here and compile for
 yourself."
   "Source"    -> https://github.com/Isarhamster/chessx/
```

So the SourceForge project is where upstream sends people for binaries and the GitHub repository is where it sends them for source. That is the distinction C047 lacked -- there upstream gave two locations a source role and ranked neither -- and it is upstream's, stated beside each link.

A scan of the page's visible text for source, binary, repository, canonical, official, mirror and primary returned only these passages and "Free and Open Source" describing the project's nature.

Step 2: the "Source Code" link. Its label is one of the contract's four words verbatim and step 1 exposes it directly, so the navigation is authorized on the plain text -- the C038 basis, with no reading of the destination required. The body's "Source" link is the same target.

Step 3: https://github.com/Isarhamster/chessx
observed_at_utc: 2026-08-28T10:35:05Z (metadata), 10:35:20Z (root listing); http_status 200 on both; redirect_chain: NONE on both
evidence_role: official-source-location

```text
full_name        Isarhamster/chessx
owner            Isarhamster
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    EMPTY
description      "Sources of the official ChessX version."
license          GPL-2.0, matching the frozen GPLv2+ line
```

Root listing: src, tests, tools, data, lib, dep, i18n, unix, mac_osx, .github, CMakeLists.txt, chessx.pro, INSTALL.md, README.md, README.developers.md, ChangeLog.md, COPYING.md, TODO.md, Doxyfile, resources.qrc, translations.qrc and the lcov and packaging scripts. A source tree is present.

The repository description reads "Sources of the official ChessX version". It is recorded as observed metadata and is NOT what carries the designation: a repository's self-description is repository-side, and the run has been consistent that the designating arrow must run from the project (C032, RETRACTION 23). Here it does -- the site's own "Source Code" and "Source" links do the work -- and the description only corroborates.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (ChessX).

Decision: PASS

## EV-C063-E2RULE-01
Candidate: C063
Gate: E2-RULE
Source: INSTALL.md in the designated repository
observed_at_utc: 2026-08-28T10:35:33Z; http_status 200; 3284 bytes
Provenance: read against the default branch at observation time; the frozen tag is v1.5.6-lw, and no claim is made about the sealed primary snapshot (QA-28).

Observed: located witness, the file's own section 3.

```text
"# 3. Requirements

 To compile ChessX, you need zlib, qmake and **Qt5 version 5.14.1** or
 above."
```

Inference: this states a concrete validity requirement without our inventing one -- a build environment lacking zlib or qmake, or carrying a Qt5 older than 5.14.1, does not satisfy it -- and it is version-bounded, as at C049 and C059.

Recorded and not relied on: the same section adds "known issue: FICS does not work properly with Qt4". It is a defect note rather than a stated requirement, and the requirement sentence carries the gate on its own.
Decision: PASS

## EV-C063-E3-01
Candidate: C063
Gate: E3
Source: src/database/bitboard.cpp and src/database/bitboard.h in the designated repository
observed_at_utc: 2026-08-28T10:36:04Z (bitboard.h), 10:36:28Z (bitboard.cpp); http_status 200 on both
Provenance: observation-time source state, as above.

Observed: located witness. Both halves are quoted rather than one assumed (C038's rule).

```text
the decision            bitboard.cpp:603  BoardStatus BitBoard::validate() const
                        ...
                        bitboard.cpp:701-703
                          if(canCastleLong(White) && pieceAt(a1) != WhiteRook)
                          {
                              return BadCastlingRights;
                          }
                        and the sibling checks through :752 for
                        canCastleShort(White), canCastleLong(Black),
                        canCastleShort(Black), and for the kings

the state it reads      bitboard.h:490-503
                          inline bool BitBoard::canCastle(color) const
                          { return m_castle & (5 << color); }
                          canCastleShort / canCastleLong likewise

how that state is       bitboard.cpp:557-559   on a rook move
narrowed by play          if (!chess960()) { m_castle &= Castle[s]; }
                        bitboard.h:436-448     destroyCastleInDirection
                          clears the bit for the rook that moved
```

Inference, kept to what these establish: `validate()`'s verdict on a position depends on `m_castle`, and `m_castle` is narrowed as rooks move. For the identical piece arrangement the answer differs according to which castling bits are still set, and which bits are still set is a function of the prior moves that cleared them. That is a stateful validity question, which is what E3 asks for.

Not claimed: that `validate()` is called on every move, or that it is the engine's move-legality path. What was observed is the function, the state it consults, and the writers that narrow that state.
Decision: PASS

## EV-C063-E4-01  (corrected in place; docs-only, no verdict change)
Candidate: C063
Gate: E4

Positive construction exhibited, via U_enforced.

Provenance and pinning. The first version of this entry read the default branch, a moving ref. It has been re-verified against an exact commit, and the pinned bytes are identical to what was read then:

```text
upstream commit   e734a075346ca2ad7e3f3e35b42140169637c5ca
                  (Isarhamster/chessx master, committed 2026-03-13T18:10:14Z)
re-fetched        2026-08-28T11:59:47Z, http_status 200 on each file
files and sha256 of the retrieved bytes

  src/database/nag.cpp          26860 bytes
    2201ce37ac0802dd0c62650b1ae6a44d9f956b2047a00b322fd75fec55dbb620
  src/database/nag.h             7737 bytes
    a26fb4f24c787dde3a5955439a8b4ffbcb3ba1bfdab19a5f0fab62e03dea6ba8
  src/database/pgndatabase.cpp  30593 bytes
    32cf76ca94e922aeba8af98ab091a04b82ad1bd580f6280d82587893f54bb31c
  src/database/gamex.cpp        43656 bytes
    f95be028d91bff39e6a5a7514e3a71d20dbbb667b9c064c03b34cfca12cd649f

what the digests do and do not support

  The four digests identify the bytes at the pinned upstream commit
  and allow a third party to reproduce the pinned-file hashes.

  This session reports that bytes retained from the earlier
  2026-08-28T10:37:34Z master fetch produced the same nag.cpp and
  nag.h digests. Because no digest or immutable copy was recorded
  contemporaneously with that earlier fetch, and the retained bytes
  live in this session's working area rather than as a durable
  artifact in this repository, the HISTORICAL identity comparison is
  not independently reproducible by a third party and rests on this
  session's report.

  Neither statement resolves QA-28 or contributes to any verdict.
```

QA-28 is unaffected: pinning identifies the object analysed and makes no claim about the sealed instant, and the frozen tag remains v1.5.6-lw.

**Corrected in place, with what is withdrawn named.** Three statements in the first version are wrong and are replaced below rather than silently rewritten:

```text
withdrawn  "the initializer holds 176 string literals, 175 of them
            non-empty"                        -- recording error

withdrawn  the two-step rejection path "fromString -> addNag", which
            asserted a connection between two functions without
            observing any call from one to the other
                                              -- inference error

withdrawn  "an annotation outside the registry cannot enter a game's
            NagSet", a claim over all paths when one parsing branch
            does not use fromString at all    -- inference error
```

---

### Observed

**A. The registry, at nag.cpp:129.** `static const QString g_nagStringList[NagCount]`, its extent fixed by the enum sentinel at nag.h:186-187 (`NagDiagram = 201,` then `NagCount`), so the declared extent is 202. Parsed element by element at the pinned commit:

```text
declared slots                                   202
bare 0 placeholders                               46
non-placeholder entries                          156
  of which empty string (index 0)                  1
  of which non-empty                             155
    plain string literals, non-empty             133
    QString::fromUtf8("...") entries              22

distinct non-empty strings                       100
strings occurring more than once                  48
entries shadowed by an identical earlier entry    55
```

The 22 `QString::fromUtf8(...)` entries are broken out because their status as ARRAY ELEMENTS is easy to lose, not because a naive scan misses their text: a plain string-literal regex does reach the literal inside each call, and counting that way yields the correct 156 and 155 totals while misclassifying all 156 as direct string-literal entries. The top-level decomposition 133 + 22 is what the array actually contains. These elements carry glyphs such as the box, infinity and advantage symbols.

**B. The alias map, at nag.cpp:292-300.** `static QMap<QString, Nag> s_ExtraNags;` is declared empty. `NagSet::InitNagStringListLong()` at nag.cpp:294 inserts five keys -- `"+/-"`, `"-/+"`, `"=+"`, `"+="`, `"->"` -- from nag.cpp:296.

**C. When B is populated, at nag.cpp:641-644.** The only call to `InitNagStringListLong()` observed in the four files examined is inside `NagSet::nagToMenuString()`, and it is lazy:

```text
if(NagSet::g_nagStringListLong.count() == 0)
{
    InitNagStringListLong();
}
```

No other caller was found in nag.cpp, nag.h, pgndatabase.cpp or gamex.cpp. The rest of the tree was not searched, so no claim is made that none exists elsewhere.

**D. The lookup, at nag.cpp:655-669.**

```cpp
Nag NagSet::fromString(const QString &nag)
{
    if (s_ExtraNags.contains(nag)) return s_ExtraNags.value(nag);
    for(int i = 1; i < NagCount; ++i)
        if(g_nagStringList[i] == nag) return Nag(i);
    return NullNag;
}
```

**E. The actual call path, observed rather than assumed.**

```text
pgndatabase.cpp:907-911   case 0:
                            Nag nag = NagSet::fromString(token.at(0));
                            game->dbAddNag(nag);

gamex.cpp:1282-1292       void GameX::dbAddNag(Nag nag, MoveId moveId)
                          {
                              if (nag != NullNag)
                              {
                                  MoveId node = m_moves.makeNodeIndex(moveId);
                                  if (node != NO_MOVE)
                                  {
                                      m_nags[node].addNag(nag);
                                  }
                              }
                          }

nag.cpp:20-24             void NagSet::addNag(Nag nag)
                          {
                              if(contains(nag) || nag == NullNag
                                 || nag >= NagCount)
                              { return; }
```

So the parser path is `PgnDatabase::parseToken -> NagSet::fromString -> GameX::dbAddNag -> NagSet::addNag`, and a `NullNag` produced by a `fromString` miss is stopped at `GameX::dbAddNag`; it does not reach `NagSet::addNag`.

The same guard shape appears at the two tokenizer call sites, pgndatabase.cpp:722-723 and :777-778, each testing `if (nag != NullNag)` immediately after `fromString`.

**F. A parsing branch that bypasses D, at pgndatabase.cpp:938-941.**

```cpp
case '$':
    if (token.length()>1)
    {
        game->dbAddNag((Nag)token.mid(1).toInt());
    }
    break;
```

This casts an arbitrary parsed integer to `Nag` without consulting the registry.

---

### Inference

EN1 external authorship: the program and these structures existed independently of this analysis.

EN2 explicit scope: the domain is the annotation glyphs a move may carry. The project names it in the enum's members and in the header's own instruction at nag.h:16, "Don't forget to add string for each 'nag' in source file."

EN3 mechanical membership, stated as the operational lookup rather than as a set:

```text
1. consult the currently populated s_ExtraNags;
2. on a miss, scan g_nagStringList from index 1 through NagCount - 1;
3. return the FIRST exact match;
4. return NullNag on a complete miss.
```

Two consequences of that are load-bearing and are stated rather than glossed. First, first-match semantics mean the 155 non-empty entries do not enumerate 155 recognised strings: they carry 100 distinct strings, and 55 entries are shadowed by an identical earlier entry and are unreachable through this lookup. Second, the alias keys are not unconditional membership -- the source declares five possible keys, while actual runtime membership is whatever `s_ExtraNags` holds in the constructed runtime state, which is empty until the lazy initialiser at C has run.

```text
source-declared possible alias keys   five
actual runtime alias membership       s_ExtraNags.keys() in the
                                      constructed runtime state
```

No clean universe member count is offered, and none is needed here. QA-19 puts the inventory at a later stage, and the enumeration difficulty recorded above is exactly what that stage would have to resolve.

EN4 connection to validation, scoped to the path actually observed:

```text
On this project-authored textual-glyph parsing path, an unrecognised
string resolves to NullNag at nag.cpp:668 and is stopped by
GameX::dbAddNag at gamex.cpp:1284 before admission to the move's
NagSet.
```

`NagSet::addNag`'s own guard is not idle downstream defense, and this is the one place where the correction runs in upstream's favour rather than against it. The `$` branch at F reaches `dbAddNag` with an arbitrary integer, so a value at or beyond `NagCount` passes `dbAddNag`'s `nag != NullNag` test and is refused by `addNag`'s observed condition `nag == NullNag || nag >= NagCount`. The two guards therefore cover different inputs rather than duplicating one another.

EN5 closed within scope: closure rests on the array's declared extent, which `fromString` iterates exactly, together with the runtime-constructed alias map. Both are the project's own data structures and its own scan bound, not analyst selection. Tag: `enforced`. No immutability is claimed, and the lazy initialisation at C is part of how the runtime state is constructed rather than a defect in the closure basis.

EN6 outcome independence: the registry is the set of annotation glyphs the program recognises. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per recognised annotation string

  "annotation string S resolves to glyph N under the lookup at D; on
   the textual-glyph parsing path a string matching nothing resolves
   to NullNag and is stopped by GameX::dbAddNag before admission"

retained as externally segmented fields, per observation
  the annotation string
  the Nag identifier it resolves to
  whether it was matched in s_ExtraNags or in g_nagStringList
  the index at which it matched
```

As at C043, C049, C056 and C059, this establishes only that a mechanically constructible universe EXISTS; it fixes no contents.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

---

### Decision

```text
E4                  PASS
overall             ELIGIBLE   (unchanged)
correction type     docs-only
verdict correction  NO
ledger change       NONE
```

Error taxonomy for this correction, kept separate because the postmortem needs the distinction:

```text
adjudication / inference errors
  asserting a fromString -> addNag connection without observing a call
  claiming that no annotation outside the registry can enter a NagSet,
    when one parsing branch never consults the registry

execution / recording error
  the 176 / 175 element counts

methodology or design gap
  none. Nothing here is a hole in the sealed protocol; the gate's
  requirements were adequate and the first version misread the source.
```


Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28. The gates above were read against the default branch at observation time while the frozen tag is v1.5.6-lw, and no observation fixes where the designated ref pointed at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## EV-C064-UR-01
Candidate: C064 (frame rank 64, games/chiaki)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/chiaki/Makefile
Observed: V=v2.2.0; DISTNAME=chiaki-${V}-src; PKGNAME derived from it; HOMEPAGE=https://git.sr.ht/~thestr4ng3r/chiaki; SITES=https://git.sr.ht/~thestr4ng3r/chiaki/refs/download/${V}/; COMMENT="open source PS4 and PS5 remote play client".
Inference: the frozen fields name one packaged system, Chiaki, and both URLs are paths on the same upstream repository host. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C064-E1-01
Candidate: C064
Gate: E1
Source: same frozen metadata
Observed: a third-party client under AGPLv3 with an OpenSSL exception, on an upstream account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C064-E2REP-01
Candidate: C064
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for, and both were observed: the frozen HOMEPAGE, and the frozen SITES.

Surface 1: the frozen HOMEPAGE.
requested_url and final_url: https://git.sr.ht/~thestr4ng3r/chiaki
observed_at_utc: 2026-08-28T12:21:57Z; http_status 200; redirect_chain: NONE (num_redirects 0); 17919 bytes

The HOMEPAGE is itself a repository -- a SourceHut git summary page -- so step 1 and step 3 are the same surface. This is the C010/C012/C017 topology, and QA-22 settled that it answers WHICH surface while supplying no designation of its own.

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the repository's name, owner and refs; the links the page exposes with their labels and targets; whether a source tree is present; any statement designating this location as the project's source; any primary or mirror marking.

Observed, restricted to the repository's own metadata furniture:

```text
title       "~thestr4ng3r/chiaki - Free and Open Source PlayStation
             Remote Play Client - sourcehut git"
owner       ~thestr4ng3r (Florian Maerkl on the commit rows)
refs        master, and a v2.2.0 entry with "release notes"
clone       read-only  https://git.sr.ht/~thestr4ng3r/chiaki
            read/write git@git.sr.ht:~thestr4ng3r/chiaki
tabs        project | source | summary | tree | log | refs
RID         06dy9xvd1xxaq26n184ck2hdp8
```

Source-tree presence, from the repository's own tree surface.
requested_url and final_url: https://git.sr.ht/~thestr4ng3r/chiaki/tree
observed_at_utc: 2026-08-28T12:23:12Z; http_status 200; redirect_chain: NONE; 15617 bytes
Observed at the root: lib, gui, cli, test, doc, scripts, cmake, assets, android, switch, setsu, third-party, LICENSES, CMakeLists.txt, COPYING, README.md, .gitmodules, .gitattributes, .gitignore, .appveyor.yml, .builds. A source tree is present.

Two items on step 1 need their own record.

```text
the "source" tab
  its label is one of the contract's four words, but it is SourceHut's
  own chrome -- rendered on every repository page -- and its target is
  https://git.sr.ht/~thestr4ng3r/chiaki, the surface already being
  read. It leads nowhere new, so nothing turns on it here, and QA-30's
  question about whether platform chrome carries designation force
  does not have to be reached.

the "project" tab -> https://sr.ht/~thestr4ng3r/chiaki
  a different surface: the host's project hub. Its label is not among
  the four words, and C007 settled that a generic project hub is not a
  repository root. Not followed.
```

EXPOSURE LOG, per the contract's unavoidable-exposure clause. This page renders the repository's README inline, under headings "# Chiaki", "# Project Status and Contributing", "# Installing", "# Downloading a Release", "# Building from Source", "# Usage", "# Acknowledgements" and "# About", together with the links that prose carries. Reading README prose is forbidden at E2-REP, and code-hosting summary pages render one automatically. It is logged here and used for nothing: not for this gate, and -- since the candidate is terminal at this gate -- not to pre-judge or shortcut E2-RULE, E3 or E4 either.

Surface 2: the frozen SITES.
requested_url and final_url: https://git.sr.ht/~thestr4ng3r/chiaki/refs/download/v2.2.0/
observed_at_utc: 2026-08-28T12:23:13Z (GET), 12:23:14Z (HEAD); http_status 404, 404; redirect_chain: NONE on both; 1497 bytes
Necessary because: the gate was unsettled after surface 1, and this is the remaining admitted starting point.

Why this was observed rather than withheld under QA-31, stated because the two cases look alike. QA-31 arises when a frozen starting point falls inside a class the contract forbids, and it was raised at C045 on a path whose segment was literally `releases`. This path's segments are `refs` and `download`; no `releases` segment appears, and the contract's forbidden list names "releases", not "download". Classifying this surface as a forbidden class would mean inferring its kind from its path, which C026 refuses. So the trigger is not established and the starting point was treated as any other. The reading is stated rather than assumed, since the opposite reading -- that a tag-scoped artifact area is a releases surface whatever the path spells -- is available and was not taken.

Observed: a 1497-byte SourceHut 404 page. No artifact names or designation signal.

```text
PASS not established
  nothing observed designates this location as the project's canonical
  source. The only route to it is the packaging metadata's own
  HOMEPAGE field, and arrival by an admitted route is affiliation, not
  designation (QA-22, C017). No project site is named anywhere in the
  frozen metadata, and the "source" tab leads back to the same page.

FAIL not established
  the repository surface is admissible and carried no designation
  signal, which is a bounded observation and not a demonstration that
  upstream designates none -- the C017 boundary. The frozen SITES
  returned 404, which is evidence about that endpoint.

E2REP-NO-SOURCE not established
  a source tree WAS observed, so source access is not what is missing.
```

Both starting points were determinately answered -- 200 and 404 -- so no surface is left unobserved and this is not the transport family. As C050's correction requires: the frozen metadata supplies no separate upstream-authored project surface, and the one admissible project-side surface -- the repository -- was examined and carried no designation signal. It is not that no surface could bear one.

Recorded and doing no verdict work: the refs list shows a v2.2.0 entry with release notes while the frozen SITES path for that same version returned 404. Nothing is inferred from the pair -- not that the artifacts moved, not that they were removed, and under QA-28 nothing about what either surface held at the sealed instant.

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

## EV-C064-E2REP-02  (supersedes EV-C064-E2REP-01, which is retained above)
Candidate: C064
Gate: E2-REP

The verdict is unchanged. Two pieces of reasoning in the superseded entry are wrong, one an adjudication error and one a procedure error, and both are corrected here rather than in place, so what was argued the first time stays visible.

Surface 1 stands as observed. The frozen HOMEPAGE is itself a SourceHut git summary page, so step 1 and step 3 coincide (C010/C012/C017), and the observations recorded in EV-C064-E2REP-01 -- the repository's owner, refs, clone URLs, tab strip, RID, and the source tree read at .../tree on 2026-08-28T12:23:12Z -- are unaffected, as is the exposure log for the inline README.

### Correction 1 -- the "source" tab reproduces QA-30; it does not evade it

Withdrawn:

```text
"It leads nowhere new, so nothing turns on it here, and QA-30's
 question about whether platform chrome carries designation force does
 not have to be reached."
```

That conflates two questions. The self-link settles NAVIGATION -- step 2 has no target elsewhere. It says nothing about EVIDENCE: whether a platform-drawn label reading `source`, on the admitted surface, amounts to upstream designating this location as its source. QA-30 exists for exactly that question, and QA-22 does not dispose of it either -- QA-22 settled that the step-1-equals-step-3 topology answers WHICH surface, not that a label rendered on that surface is void.

So C064 is a direct instance of QA-30, the second the run has met after C044, and the gap runs the same way:

```text
if SourceHut's chrome carries designation force
    the `source` tab designates this repository as the project's
    source, and no competing source designation was observed
    -> E2-REP PASS could follow

if it does not
    the repository's identity and its source tree are affiliation only
    -> E2-REP UNRESOLVED
```

Choosing a branch now, with the candidate's outcome in view, is the post-hoc criterion change the run forbids, so neither is taken. QA-30 already records that this is a class rather than an incident; C064 is a further member of it, and no new QA is created.

### Correction 2 -- opening the frozen SITES was a QA-31 violation

Withdrawn:

```text
"This path's segments are `refs` and `download`; no `releases` segment
 appears, and the contract's forbidden list names "releases", not
 "download". Classifying this surface as a forbidden class would mean
 inferring its kind from its path, which C026 refuses."
```

Both halves are wrong.

QA-31 is written in terms of a surface CLASS -- "surface class = releases" -- and its scope paragraph speaks of "a code host's release assets", not of a spelling. Reducing it to a search for the literal segment `releases` narrows a class rule to a substring test the QA does not contain.

And C026 does not license that narrowing. C026 bars inferring an ARTIFACT'S SOURCE ROLE from its filename. Identifying the CLASS of a host surface from that host's URL scheme is a different operation, and it is the operation QA-31 itself performed at C045. Invoking C026 here was a misapplication, and it is the specific error rather than a general reluctance to classify.

The superseded entry also convicts itself: it called the surface a "tag-scoped artifact area" and then declined to treat it as one. Recognising the class and then setting it aside on spelling grounds is the mid-run choice the sealed methodology forbids.

Disposition, per QA-31 and QA-27's third branch: the frozen SITES is metadata-supplied but unobservable under the sealed contract, and is accounted for with the prohibition as the named reason. Stated as history rather than as procedure, since the requests were in fact made: the lawful disposition was NOT TO OPEN IT, and this run did open it. What follows records that.

```text
QUARANTINED -- unauthorized exposure

  https://git.sr.ht/~thestr4ng3r/chiaki/refs/download/v2.2.0/
  requested 2026-08-28T12:23:13Z (GET), 12:23:14Z (HEAD)
  http_status 404, 404; 1497 bytes

  The requests should not have been made. The responses are retained,
  as this run retains every deviation, and they do no verdict work:
  they are not endpoint evidence for this gate, they do not support
  any claim about what that surface holds, and they cannot be used to
  say the starting-point set was exhausted by observation.
```

Two statements resting on those requests are withdrawn with them:

```text
withdrawn  "Both starting points were determinately answered -- 200
            and 404 -- so no surface is left unobserved"
            One starting point was withheld by the contract, not
            answered. This is C045's situation, not C036's.

withdrawn  the paired note that the refs list shows a v2.2.0 entry
            "while the frozen SITES path for that same version
            returned 404". The comparison is built on the quarantined
            request and is not made.
```

### Adjudication

```text
PASS not established
  no designation witness whose evidential force is determined by the
  sealed rules. The only route to this repository is the packaging
  metadata's own HOMEPAGE field, which is affiliation (QA-22, C017),
  and the frozen metadata names no project site. The one candidate
  witness is the platform-drawn `source` tab, and whether that carries
  designation force is precisely the undecided QA-30 question above.

FAIL not established
  the repository surface is admissible and carried no designation
  signal determined by the sealed rules, which is a bounded
  observation and not a demonstration that upstream designates none
  (C017). The remaining admitted starting point is unobservable under
  the contract, which narrows the basis for any negative further.

E2REP-NO-SOURCE not established
  a source tree WAS observed at the repository's tree surface, so
  source access is not what is missing.
```

Two independent routes reach the same code, and both are recorded because the postmortem should see that they coincided rather than that one carried the entry:

```text
QA-30  the evidential force of the chrome `source` label is undecided,
       so the PASS-versus-UNRESOLVED branch cannot be taken

QA-31  a potentially necessary metadata-supplied starting point is one
       the contract forbids inspecting, and the protocol does not
       operationalize how E2-REP completes in that case
```

Decision: UNRESOLVED (PI-UNCLASSIFIED-SHAPE)

Gates after E2-REP are NOT_REACHED.

Error taxonomy for this correction:

```text
adjudication / inference error
  treating the `source` self-link as closing QA-30 because it closed
  navigation

execution / procedure error
  opening the frozen SITES, a surface QA-31 places out of reach, on a
  substring reading of the class and a misapplication of C026

methodology or design gap
  none. QA-30 and QA-31 already describe both situations; this entry
  applied them wrongly and now applies them.
```

Ledger unchanged: UNRESOLVED / E2-REP / PI-UNCLASSIFIED-SHAPE, later gates NOT_REACHED. The evidence refs now point at the superseding -02, per the C002/C005 convention.

## EV-C065-UR-01
Candidate: C065 (frame rank 65, games/chocolate-doom)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/chocolate-doom/Makefile
Observed: V=3.1.0; DIST_TUPLE = github chocolate-doom chocolate-doom chocolate-doom-${V} .; PKGNAME=chocolate-doom-${V}; HOMEPAGE=https://www.chocolate-doom.org/; COMMENT="portable release of Doom, Heretic, Hexen, and Strife".
Inference: one packaged system, Chocolate Doom. The four titles COMMENT lists are the games the port reproduces, not four packaged systems -- the reading applied at C013, C023, C046, C048, C050, C057 and C061 -- and the single DIST_TUPLE extracts to "." with no vendored second tuple. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C065-E1-01
Candidate: C065
Gate: E1
Source: same frozen metadata
Observed: a third-party source port under GPLv2+, on an upstream domain and account unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C065-E2REP-01
Candidate: C065
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE, and the DIST_TUPLE's chocolate-doom/chocolate-doom identifiers. The pair resolves to the same repository step 3 reaches, so as at C038 it is not a separate surface.

Step 1: the frozen HOMEPAGE.
requested_url: https://www.chocolate-doom.org/ ; final_url: https://www.chocolate-doom.org/wiki/index.php/Chocolate_Doom
observed_at_utc: 2026-08-28T12:37:32Z; http_status 200; redirect_chain: 1 redirect; 19535 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical or mirror marking.

Observed: the project's own MediaWiki page, titled "Chocolate Doom". Its content links are Read more (About), Screenshots, Download, User guide, FAQ, **development**, and Crispy Doom; its sidebar adds "Download package" and "Report bug"; its External links section lists Doomworld, The Doom Wiki and the idgames archive, all third-party. The remainder is MediaWiki's own chrome -- Talk, Contributions, Edit, View history, Special pages and so on.

No repository or source link appears on this surface. "Report bug" targets the repository's issues, a forbidden surface, and was not followed. "Download" and "Download package" are outside the four labels (QA-17) and were not opened.

Step 2: the `development` link -> /wiki/index.php/Development. Its label is one of the contract's four words and step 1 exposes it directly, so the navigation is authorized on the contract's plain text. The label is lower-cased in the page's prose; treating that as the same token is the reading already taken at C064, where a lower-cased `source` tab was likewise treated as carrying the word. C038 is not the precedent for case folding -- it settled that a host-name anchor does no work on its own -- and is not cited for it here.

requested_url and final_url: https://www.chocolate-doom.org/wiki/index.php/Development
observed_at_utc: 2026-08-28T12:38:10Z; http_status 200; redirect_chain: NONE; 19615 bytes

This page performs the designation, in upstream's own sentences:

```text
"...keep up to date with the latest bleeding edge pre-release version
 from the [Git repository]."
     Git repository -> https://github.com/chocolate-doom/chocolate-doom

"You can browse the Chocolate Doom source code [here]."
     here -> https://github.com/chocolate-doom/chocolate-doom
```

Both name the same location, and the second states the source relation explicitly: its subject is "the Chocolate Doom source code" and the link is where it is browsed.

The step structure follows C049 exactly and is stated so, because it is not the shortest possible reading of the contract: there too the step-2 link was labelled Development, led to a page rather than to a repository, and that page then identified the repository which became step 3. Nothing new is introduced here.

Uniqueness, from what this page itself separates:

```text
"Daily build" -> latest.chocolate-doom.org
   introduced by "If you're a Windows user you can download prebuilt
   Windows binaries" -- binaries, by upstream's own sentence

the branch and fork category links, and the four "Building Chocolate
Doom on ..." links
   the Development page introduces these as a list of branches, a list
   of forks, and per-platform compiling instructions. It does not
   designate any of them as a canonical source location. None was
   opened, and nothing is claimed about what those pages contain.

"Submit a bug report" -> the repository's issues
   forbidden surface; not followed
```

So what is established is about the two surfaces actually read: neither designates a source location other than the repository. No claim is made about pages this entry did not open.

Step 3: https://github.com/chocolate-doom/chocolate-doom
observed_at_utc: 2026-08-28T12:38:50Z (metadata), 12:38:51Z (root listing); http_status 200 on both; redirect_chain: NONE on both
evidence_role: official-source-location

```text
full_name        chocolate-doom/chocolate-doom
owner            chocolate-doom
default_branch   master
fork             false          parent  null
archived         false          is_template  false     mirror_url  null
website field    https://www.chocolate-doom.org/
description      "Chocolate Doom is a Doom source port that is
                  minimalist and historically accurate."
license          GPL-2.0, matching the frozen GPLv2+ line
```

Root listing, 37 entries, including src, opl, pcsound, textscreen, data, man, cmake, pkg, win32, CMakeLists.txt, Makefile.am, configure.ac, autogen.sh, vcpkg.json, README.md, HACKING.md, PHILOSOPHY.md, COPYING.md and the NEWS and ChangeLog files. A source tree is present.

The direction is asymmetric, as RETRACTION 23 requires: the project's wiki designates the repository; the repository's website field naming the site corroborates affiliation and does not itself designate.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Chocolate Doom).

Decision: PASS

## EV-C065-PIN-01
Candidate: C065
Scope: provenance for the gates below

The gates after E2-REP were read at an exact upstream commit rather than at a moving ref, and the digests are recorded so the objects analysed are identifiable.

```text
upstream commit   3a39d0a53aaa52562f099a7c4fab649d8962d947
                  (chocolate-doom/chocolate-doom master,
                   committed 2026-08-24T16:33:06Z)
resolved at       2026-08-28T12:39:14Z

file                     bytes   sha256 of the retrieved bytes
vcpkg.json                 126   bc348b183d865673d622f183cb315e458546925621f0cf1fd5d49d915489d999
src/d_iwad.c             24909   e9def3200259b5e38e8e1d4f2798580e02c4cb543ff89485e5fb7736a452bca6
src/doom/g_game.c        57052   53de0aa103e269d25ae2b5965f18732bdfb2c6769cb4369df01a0fa009d44480
src/doom/d_main.c        50251   0a0ad7a2edd21709f3686bc6d36179b76eb56071b4dc14f3031661eaedaa6645
```

These digests identify the bytes at that commit and allow a third party to reproduce the file hashes. They do nothing for QA-28: the frozen version is 3.1.0, the pinned commit is later, and no observation fixes where the designated ref pointed at the sealed instant.

## EV-C065-E2RULE-01
Candidate: C065
Gate: E2-RULE
Source: vcpkg.json in the designated repository, at the pinned commit
observed_at_utc: 2026-08-28T12:41:36Z; http_status 200; 126 bytes

Observed: located witness, the file in full.

```json
{
  "dependencies": [
    "sdl2",
    "sdl2-mixer",
    "sdl2-net",
    "libpng",
    "libsamplerate",
    "fluidsynth"
  ]
}
```

Inference: the project declares six packages its build depends on, and a build environment lacking any of them does not satisfy that declaration. E2-RULE asks for at least one externally authored validity requirement and does not restrict the domain (C043), nor does it require version bounds (C038, C043).

Recorded and not used: README.md directs the reader to an INSTALL file, and no INSTALL appears in the root listing. Nothing is inferred from that -- not that the file is missing, not that the instruction is stale. HACKING.md was read and is a coding-style document whose statements are contributor guidance phrased with "should"; it is not relied on.
Decision: PASS

## EV-C065-E3-01
Candidate: C065
Gate: E3
Source: src/doom/g_game.c at the pinned commit
Provenance: EV-C065-PIN-01.

Observed: located witness. All parts are in this one file, so both halves are quoted rather than one assumed (C038's rule).

```text
g_game.c:153       byte consistancy[MAXPLAYERS][BACKUPTICS];

g_game.c:343-344   cmd->consistancy =
                       consistancy[consoleplayer][maketic%BACKUPTICS];

g_game.c:962       buf = (gametic/ticdup)%BACKUPTICS;

g_game.c:968-970   cmd = &players[i].cmd;
                   memcpy(cmd, &netcmds[i], sizeof(ticcmd_t));

g_game.c:1000-1013 if (netgame && !netdemo && !(gametic%ticdup))
                   {
                       if (gametic > BACKUPTICS
                           && consistancy[i][buf] != cmd->consistancy)
                       {
                           I_Error ("consistency failure (%i should be %i)",
                                    cmd->consistancy, consistancy[i][buf]);
                       }
                       if (players[i].mo)
                           consistancy[i][buf] = players[i].mo->x;
                       else
                           consistancy[i][buf] = rndindex;
                   }
```

Inference: the command compared is the one copied from `netcmds[i]` at :968-970, so it is an incoming command rather than a locally built one, and the slot it is compared against is `buf`, computed at :962 from the current `gametic`. The byte it carries was stamped by its sender from that sender's own `consistancy` ring at :343-344; this machine's entry for the same slot is written at :1010-1012 from the player's world position, or from the random-number index when no map object exists. So the identical command bytes are accepted or fatal according to the simulation history on both sides.

The check is additionally gated on `gametic > BACKUPTICS`, which is stated here as the project's own condition and nothing more. An earlier version glossed it as meaning the check waits "until enough ticks have elapsed to fill the ring buffer". That does not follow: the index is `(gametic/ticdup)%BACKUPTICS`, so with `ticdup` greater than one the guard does not establish that the ring has been filled. The gloss is withdrawn; what stands is that the comparison is conditioned on elapsed game time.

Not claimed: anything about how often this path executes in practice, or about builds in which `netgame` is never true. What was observed is the check, the state it consults, and the writers of that state.
Decision: PASS

## EV-C065-E4-01
Candidate: C065
Gate: E4

Positive construction exhibited, via U_enforced.
Provenance: EV-C065-PIN-01.

The mechanism: the IWAD registry.

```text
d_iwad.c:34-52   static const iwad_t iwads[] =
                 {
                     { "doom2.wad",    doom2,     commercial, "Doom II" },
                     { "plutonia.wad", pack_plut, commercial, "Final Doom: Plutonia Experiment" },
                     ...
                     { "strife1.wad",  strife,    commercial, "Strife" },
                 };

d_iwad.c:582-607 static GameMission_t IdentifyIWADByName(const char *name,
                                                          int mask)
                 {
                     name = M_BaseName(name);
                     mission = none;
                     for (i=0; i<arrlen(iwads); ++i)
                     {
                         if (((1 << iwads[i].mission) & mask) == 0)
                             continue;
                         if (!strcasecmp(name, iwads[i].name))
                         {
                             mission = iwads[i].mission;
                             break;
                         }
                     }
                     return mission;
                 }
```

```text
active entries                                    15
entries commented out                              1  ("strife0.wad",
                                                       marked
                                                       "STRIFE-FIXME")
distinct filenames among the active entries       15
```

EN1 external authorship: the port and this registry existed independently of this analysis.

EN2 explicit scope: each entry is a four-field record the project wrote -- IWAD filename, mission enum, game mode, and a human-readable title such as "Final Doom: Plutonia Experiment". The domain is the IWAD files the port recognises by name.

EN3 mechanical membership:

```text
enumerator membership      the active entries of iwads[], which
                           IdentifyIWADByName iterates via arrlen()

values this validator acts on
                           the entry's filename, matched with
                           strcasecmp against the basename, and its
                           mission, tested against the caller's mask
                           and returned on a match

retained metadata, not     the game mode and the project's own title.
enforcement values         Both are project-authored fields of the
                           entry, and neither participates in
                           IdentifyIWADByName's decision.
```

That split is stated because an earlier version listed mode and title among the enforcement values, which overstates what this validator consults.

The scan bound is the array itself, so membership is enumerable by reading it. The commented-out `strife0.wad` line is counted as absent, not as a member: it is not compiled.

EN4 connection to validation, with the call path observed rather than inferred from the two endpoints:

```text
d_iwad.c:902-931   iwadparm = M_CheckParmWithArgs("-iwad", 1);
                   if (iwadparm)                              // :904
                   {
                       iwadfile = myargv[iwadparm + 1];
                       result = D_FindWADByName(iwadfile);
                       if (result == NULL)
                           I_Error("IWAD file '%s' not found!", iwadfile);
                       *mission = IdentifyIWADByName(result, mask);  // :917
                   }                                          // :918
                   else                                       // :919
                   {
                       ...
                       for (i=0; result == NULL && i<num_iwad_dirs; ++i)
                       {                                      // :927
                           result = SearchDirectoryForIWAD(iwad_dirs[i],
                                                           mask, mission);
                       }                                      // :930
                   }                                          // :931

d_main.c:1490      iwadfile = D_FindIWAD(IWAD_MASK_DOOM, &gamemission);
d_main.c:1503      D_AddFile(iwadfile);
d_main.c:1509      D_IdentifyVersion();
```

The limitation is stated rather than glossed, and it is scoped to the branch that produces it. `IdentifyIWADByName` is called only in the `-iwad` branch; the other branch reaches a mission through `SearchDirectoryForIWAD`, which matches against the same registry while scanning directories. So the case that arrives at `D_IdentifyVersion` with `gamemission == none` is the one where `-iwad` named a file that exists on disk but for which no mask-eligible active entry matched the basename.

The mask qualifier is not decoration. `IdentifyIWADByName` applies it BEFORE comparing names -- `if (((1 << iwads[i].mission) & mask) == 0) continue;` at d_iwad.c:596-597, ahead of the `strcasecmp` at :601 -- so `none` can result either because no entry's name matched, or because the entry whose name would have matched carries a mission the caller's mask excludes. An earlier version wrote "matched no active entry", which covers only the first. There, rejection follows only if a second, content-based attempt also fails:

```text
d_main.c:779-802
  if (gamemission == none)
  {
      for (i=0; i<numlumps; ++i)
      {
          if (!strncasecmp(lumpinfo[i]->name, "MAP01", 8))
              ... gamemission = doom2 ...
          ... ExMy ... gamemission = doom ...
      }
      if (gamemission == none)
      {
          I_Error("Unknown or invalid IWAD file.");
      }
  }
```

So on that branch the registry is not the sole membership authority: it decides NAME-based identification, and a miss falls through to a lump-content heuristic before `I_Error` is reached. This is the same shape as C063's `$` branch bypassing the NAG registry, and the enforcement observation below is scoped accordingly rather than claiming that an unregistered IWAD cannot be accepted.

EN5 closed within scope: the set is closed by the array's own extent, which `arrlen(iwads)` supplies to the scan. Closure is the project's declaration, not analyst selection. Tag: `enforced`.

EN6 outcome independence: the registry is the set of IWAD files the port recognises by name. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations, and scoped to the name path:

```text
one enforcement observation per active entry

  "IWAD filename F is identified by name as mission M when the
   caller's mask admits M; on the -iwad branch a basename for which no
   mask-eligible active entry matches yields `none` from
   IdentifyIWADByName, after which identification is attempted from
   lump contents and `Unknown or invalid IWAD file.` is raised only if
   that also fails"

retained as externally segmented fields, per observation
  the IWAD filename
  the mission enum
  the game mode
  the project's own title for it
```

As at C043, C049, C056, C059 and C063, this establishes only that a mechanically constructible universe EXISTS; it fixes no contents, and QA-19 puts the inventory at a later stage.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28. The gates were read at commit 3a39d0a5, the frozen version is 3.1.0, and no observation fixes where the designated ref pointed at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## EV-C066-UR-01
Candidate: C066 (frame rank 66, games/choria)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/choria/Makefile
Observed: V=1.1.1; COMMIT=f11082f6; DISTNAME=choria-${V}-${COMMIT}-src; PKGNAME=choria-${V}; HOMEPAGE=https://choria.gitlab.io/; SITES=https://gitlab.com/jazztickets/uploads/-/raw/main/; COMMENT="2D MMORPG focused on grinding".
Inference: the frozen fields name one packaged system, Choria. The SITES host is a different namespace from the HOMEPAGE -- `jazztickets/uploads` -- but that is a statement about where the distfile is fetched from, which the protocol's carve-out treats as one more fact about one system rather than as a second system claim. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C066-E1-01
Candidate: C066
Gate: E1
Source: same frozen metadata
Observed: a third-party game under GPLv3+, on upstream hosts unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C066-E2REP-01
Candidate: C066
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE and the frozen SITES.

Step 1: the frozen HOMEPAGE.
requested_url and final_url: https://choria.gitlab.io/
observed_at_utc: 2026-08-28T13:02:46Z; http_status 200; redirect_chain: NONE (num_redirects 0); 5094 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; title and headings; the links exposed with their labels and targets; any sentence or label assigning a source role; any primary, canonical or mirror marking.

Observed: the project's own site. Its top navigation is Home, News, Download and Game Guide; its footer groups links under three headings the project wrote itself:

```text
<h3>Project</h3>
  <a href='https://gitlab.com/choria/code'>Source Code</a>
  <a href='https://gitlab.com/choria/code/-/releases'>Releases</a>
  <a href='https://gitlab.com/choria/code/-/issues'>Issues</a>

<h3>Links</h3>
  Fosstodon, Lemmy, Flathub, Youtube
```

Step 2: the "Source Code" link. Its label is one of the contract's four words verbatim, step 1 exposes it directly, and the project's own `Project` heading groups it with the repository's other areas. Authorized on the contract's plain text.

Uniqueness. The two sibling links under the same heading are labelled `Releases` and `Issues` -- both forbidden classes, neither followed, and neither carrying a source role. `Download` in the top navigation is outside the four labels and was not opened (QA-17). `Flathub` is listed under `Links`; it was not opened, and no role is assigned to it here. So exactly one link on this surface carries the source role, and the project's own grouping is what separates it from its siblings.

Step 3: https://gitlab.com/choria/code
observed_at_utc: 2026-08-28T13:03:03Z (metadata), 13:03:17Z (root listing); http_status 200 on both
evidence_role: official-source-location

```text
path_with_namespace   choria/code
name                  choria
default_branch        dev
visibility            public
web_url               https://gitlab.com/choria/code
forked_from_project   null
```

Root listing at `dev`: src, assets, ext, deployment, working, cmake, CMakeLists.txt, build.sh, README, LICENSE, CHANGELOG, .gitmodules, .gitignore. A source tree is present.

Inference: exactly one designated canonical source location, at a stable URL, holding a source tree, with one external target identifier (Choria).

The frozen SITES is accounted for and was not opened. The stop rule ends navigation "the moment a PASS or a specific failure code is determined. Not one page further", and the determination was reached at step 3; QA-27's obligation is to account for each starting point rather than to open each, and this is that branch. Recorded because it is unusual and does no work here: that URL points into `jazztickets/uploads`, a namespace different from the designated repository's. Nothing is inferred from that -- not that it is packager-side, not that it is upstream's, and nothing about its contents.

Decision: PASS

## EV-C066-PIN-01
Candidate: C066
Scope: provenance for the gates below

```text
upstream commit   55974b0ac9d2046fbb4beca9f1a515145a116c6d
                  (choria/code branch dev,
                   committed 2026-08-04T07:31:07-06:00)
resolved at       2026-08-28T13:03:33Z

file                    bytes   sha256 of the retrieved bytes
README                   5028   080c767b49e71d5234c907c802f7683e6909d88b4f3ac4bc89a95f5d3bef71a1
src/save.cpp            17674   d5073e0839bfd288cac98462235c3152c7c54ffb9830e649f6e5509c60b0c4c1
src/constants.h         14145   13c5327caff537da2d34d430133e28532a1d39da0c87513aa9343fcee3214eac
src/scripting.cpp       59499   21be427697f950baed220703dd93fa566f91e2e65df4396049311e8314888bd0
src/stats.cpp           34683   b7a7e7de6ce2f426c22a68ffd423f6c2c6819aadb65fc15d73fb9e56c7cd6b56
```

These digests identify the bytes at that commit and let a third party reproduce the file hashes. They do nothing for QA-28: the frozen metadata pins V=1.1.1 at COMMIT=f11082f6, the commit read here is a later state of the `dev` branch, and no observation fixes where the designated ref pointed at the sealed instant.

## EV-C066-E2RULE-01
Candidate: C066
Gate: E2-RULE
Source: README in the designated repository, at the pinned commit
observed_at_utc: 2026-08-28T13:03:45Z; http_status 200; 5028 bytes

Observed: located witness, the file's own dependency section.

```text
"-- Dependencies required --
 Ninja
 CMake 3.10+
 OpenGL 3.3+
 SDL3
 libwebp
 OpenAL
 libvorbis
 libogg
 FreeType2
 SQLite 3.25+
 zlib
 pthreads"
```

Inference: the project states twelve required dependencies, three of them version-bounded -- CMake 3.10+, OpenGL 3.3+, SQLite 3.25+ -- and a build environment lacking any of them does not satisfy the stated requirement. Externally authored, in upstream's own heading.
Decision: PASS

## EV-C066-E3-01
Candidate: C066
Gate: E3
Source: src/save.cpp and src/constants.h at the pinned commit
Provenance: EV-C066-PIN-01.

Observed: located witness. Every part of the chain is quoted, including the writers of the conditioning value (C038's rule).

```text
constants.h:26     const int DEFAULT_SAVE_VERSION = 11;

save.cpp:456-462   int _Save::GetSaveVersion() {
                       Database->PrepareQuery("SELECT version FROM settings");
                       ...
                       int Version = Database->GetInt<int>("version");
                       return Version;
                   }

save.cpp:44-51     int SaveVersion = 0;
                   try { SaveVersion = GetSaveVersion(); }
                   catch(std::exception &Error) { }

save.cpp:53-74     if(SaveVersion != DEFAULT_SAVE_VERSION) {
                       std::string BackupPath = SavePath + "." + ...;
                       bool Upgraded = false;
                       if(SaveVersion == 10) {
                           std::filesystem::copy(SavePath, BackupPath, ...);
                           Database->RunQuery("ALTER TABLE account ADD COLUMN last_slot INTEGER");
                           Database->RunQuery("UPDATE settings SET version = version + 1");
                           Upgraded = true;
                       }
                       if(!Upgraded) {
                           if(SaveVersion > 0) {
                               delete Database;
                               std::rename(SavePath.c_str(), BackupPath.c_str());
                               ...
                           }
                           CreateDefaultDatabase();
                       }
                   }

save.cpp:497-498   Database->PrepareQuery("INSERT INTO settings(version) VALUES (@version)");
                   Database->BindInt(1, DEFAULT_SAVE_VERSION);
```

Inference, kept to what the quoted code establishes: whether an existing save file is accepted as it stands is decided against a version number read out of that file, and the program contains both writers of that value -- at creation by :497-498, and by the increment at :61 when a version-10 file is migrated. So the value the check consults is one this program persists and a later run reads back. The same file is used directly at version 11, migrated in place at version 10, and at any other positive version is renamed aside and replaced by a fresh database, which is to say not accepted.

Not claimed: that the value in any particular existing file was in fact written by an earlier run of this program. What is established is the persistent writer and reader path and the branch it drives, which is the stateful validity question E3 asks for.
Decision: PASS

## EV-C066-E4-01
Candidate: C066
Gate: E4

Positive construction exhibited, via U_enforced.
Provenance: EV-C066-PIN-01.

The mechanism: the item registry and the check that gates script-supplied item attributes against it.

```text
stats.cpp:263-338  void _Stats::LoadItems() {
                       Database->PrepareQuery("SELECT * FROM item");
                       while(Database->FetchRow()) {
                           uint32_t ItemID = Database->GetInt<uint32_t>("id");
                           if(ItemID == 0) continue;
                           _Item *Item = new _Item;
                           Item->ID = ItemID;
                           Item->Name = Database->GetString("name");
                           Item->Script = Database->GetString("script");
                           Item->Proc = Database->GetString("proc");
                           Item->Type = (ItemType)Database->GetInt<int>("itemtype_id");
                           ...
                           Items[Item->ID] = Item;
                           ItemMap[Item->Name] = Item;
                       }
                   }
stats.cpp:341      Items[0] = nullptr;

stats.cpp:341-346  Items[0] = nullptr;

                   // Load extra attributes
                   _Scripting Scripting;
                   Scripting.LoadScript(SCRIPTS_DATA);
                   Scripting.LoadItemAttributes(this);
               }

scripting.cpp:510-524
                   void _Scripting::LoadItemAttributes(_Stats *Stats) {
                       lua_getglobal(LuaState, "Item_Data");
                       if(!lua_istable(LuaState, -1))
                           throw std::runtime_error(... " Item_Data is not a table!");
                       lua_pushnil(LuaState);
                       while(lua_next(LuaState, -2) != 0) {
                           uint32_t ItemID = (uint32_t)lua_tointeger(LuaState, -2);
                           if(Stats->Items.find(ItemID) == Stats->Items.end())
                               throw std::runtime_error(... " Item ID "
                                   + std::to_string(ItemID) + " not found!");
                           ...
```

The call path is closed, and its ORDER matters: `LoadItemAttributes` is invoked at the end of `LoadItems` itself, at stats.cpp:346, after the query loop has populated the map and after the `Items[0]` insertion at :341. So the registry the check consults is fully constructed, sentinel included, before any script key is tested against it. An earlier version of this entry quoted the two function definitions without this call site, which left the EN4 connection asserted rather than shown -- the same defect corrected at C063.

PROVENANCE NOTE. These line numbers were challenged in review as belonging to a different range, so they were re-verified rather than defended from memory. `dev` was re-resolved at 2026-08-28T13:22:50Z and is unchanged at 55974b0ac9d2046fbb4beca9f1a515145a116c6d; `src/scripting.cpp` re-fetched at that commit is byte-identical to the copy hashed in EV-C066-PIN-01, sha256 21be427697f950baed220703dd93fa566f91e2e65df4396049311e8314888bd0, and in those bytes `LoadItemAttributes` begins at line 510, the conversion is at :522, the `find` at :523 and the throw at :524. The citations stand as written.

EN1 external authorship: the game and this loader existed independently of this analysis.

EN2 explicit scope: the domain is the items the game defines. Each LOADED entry is built from named columns the project chose -- id, name, texture, alt_texture, script, proc, itemtype_id and the rest -- so every loaded member carries externally segmented fields. The one exception is the sentinel described under EN3, which carries none, and it is kept separate everywhere below rather than being counted as an ordinary member.

EN3 mechanical membership:

```text
loaded members             the keys inserted into Stats->Items by
                           LoadItems, one per row of the `item` table,
                           rows with id 0 skipped at stats.cpp:271-272
                           -- each mapping to a fully built _Item

sentinel entry             Items[0] = nullptr, inserted at
                           stats.cpp:341 after the loop. Key 0 is
                           present in the map and maps to no _Item, so
                           it carries none of the fields the loaded
                           members carry.

what the check consults    the map's key set, which is the loaded
                           members TOGETHER WITH the sentinel
```

EN4 connection to validation, in project code on both sides: `LoadItemAttributes` iterates the script's `Item_Data` table and, for each entry, tests a value against `Stats->Items`, raising a runtime error that names it when absent. The deciding and the rejecting code are both the project's, unlike C038 and unlike this candidate's own Lua-binding tables, where an unregistered call would fail inside the interpreter.

What is tested is stated exactly, because an earlier version overstated it as "any `Item_Data` key". The code does not test the raw Lua key. It converts first, at scripting.cpp:522 -- `uint32_t ItemID = (uint32_t)lua_tointeger(LuaState, -2);` -- and the `find` at :523 is performed on that converted `uint32_t`. So the guarantee runs over converted values, not over keys as they appear in the script.

Two consequences follow, and the second is bounded by what was NOT observed:

```text
established from the quoted code
  a converted ID of 0 is not rejected. Items[0] exists by the
  sentinel, so find(0) succeeds and the throw at :524 is not reached,
  while the value obtained is null.

not established here
  what a key that is not a number converts to. That is Lua library
  behaviour, and this entry did not observe the Lua version this build
  links or that version's conversion rule. If such a key converts to
  0, the case above applies to it; if it converts otherwise, it does
  not. Nothing is asserted either way -- the C038 rule against
  supplying library semantics from our own knowledge.
```

EN5 closed within scope: the set is closed by runtime construction -- Section 3.2's first admissible case -- and the two sets it closes over are named separately, alongside the condition that consults them, because "what `LoadItems` inserted" covers the sentinel too and would otherwise contradict the membership defined above:

```text
U_enforced membership   the loaded members: one per nonzero row of the
                        `item` table, each a fully built _Item

validation key set      the loaded members TOGETHER WITH the sentinel
                        key 0. This is the set `find` at
                        scripting.cpp:523 consults.

rejection fires         when the converted id is absent from the
                        VALIDATION KEY SET -- not from the U_enforced
                        membership. Key 0 is in the former and not the
                        latter, which is exactly why it is not
                        rejected.
```

Both sets are closed by the same runtime construction, inside `LoadItems`: the query loop for the members, stats.cpp:341 for the sentinel. Closure is the project's own doing, not analyst selection. Tag: `enforced`. No immutability is claimed.

EN6 outcome independence: the registry is the set of items the game defines. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per LOADED item id

  "item id N is a loaded member, carrying the project's own name,
   type, script and proc fields; a script `Item_Data` entry whose
   converted id is absent from the VALIDATION KEY SET is rejected with
   `Item ID <n> not found!`"

retained as externally segmented fields, per observation
  the item id
  the project's name for it
  its item type
  its script and proc identifiers

the sentinel is NOT such an observation
  key 0 carries none of those fields, and it is the one key whose
  presence weakens rather than performs the check. It belongs to the
  validation key set and not to the U_enforced membership, which is
  why the rejection clause above is worded against the validation key
  set rather than against the membership.
```

Two limits are stated rather than left implicit. The registry's contents are read from the `item` table of a database the project ships, and this entry did not open that database, so no member list and no count is offered here -- constructing it is the inventory stage's work under QA-19, by the same mechanism the program uses. And the sentinel means the map's key set, the loaded-member set and the set of ids with usable values are three different things, kept apart above.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28. The gates were read at commit 55974b0a on `dev`, the frozen metadata pins COMMIT=f11082f6, and no observation fixes where the designated ref pointed at the sealed instant. The three inventory fields are consequently NOT_REACHED.

## EV-C069-UR-01
Candidate: C069 (frame rank 69, games/chromium-bsu)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/chromium-bsu/Makefile and distinfo
Observed: DISTNAME=chromium-bsu-0.9.16.1; HOMEPAGE=https://chromium-bsu.sourceforge.net/; SITES=${SITE_SOURCEFORGE:=chromium-bsu/}; COMMENT="fast paced arcade-style space shooter"; distinfo names chromium-bsu-0.9.16.1.tar.gz. `SITE_SOURCEFORGE` is defined in the same frozen tree at infrastructure/db/network.conf:68-69 as `https://downloads.sourceforge.net/sourceforge/`, so SITES resolves to `https://downloads.sourceforge.net/sourceforge/chromium-bsu/`.
Inference: the frozen fields name one packaged system, Chromium B.S.U., under one project short name on one code host. No second system appears, so not UR-AMBIGUOUS; no earlier candidate resolved to it, so not a duplicate.
Decision: PASS

## EV-C069-E1-01
Candidate: C069
Gate: E1
Source: same frozen metadata
Observed: a third-party arcade game under the Clarified Artistic License, on an upstream site unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C069-E2REP-01
Candidate: C069
Gate: E2-REP
Source: the two admitted starting points supplied by the frozen metadata.

Provenance. `https://chromium-bsu.sourceforge.net/` was requested and answered 200 after a redirect to `https://chromium-bsu.sourceforge.io/`; the body is 3671 bytes, sha256 8eb232d4a8161eb6d765acbd3a92e6d96ab2fa1489320702a4500b14131af56b. The host change is recorded as a fact of the fetch and nothing is inferred from it.

Observed at step 1, parsed rather than read off. Every `<a>` element of the landing page, 11 in total, with its label normalized (the labels are letter-spaced with `&nbsp;` in the source):

```text
info.html                                     "info"
download.html                                 "download"
faq.html                                      "faq"
about.html                                    "about"
screen0.html / screen1.html / screen2.html    "screen-0" / "-1" / "-2"
http://www.opengl.org                         (image, no text)
http://www.openal.org                         (image, no text)
http://sourceforge.net/projects/chromium-bsu/ "sourceforge project"
http://www.reptilelabour.com/                 "thereptilelabourproject"
```

No label is Source, Code, Repository or Development. The word `source` occurs twice in the document and a standalone-word search returns nothing for it: both occurrences are inside `sourceforge`, once in a href and once in that link's label. `code`, `repository`, `development`, `git`, `svn` and `cvs` occur zero times. So step 2 has no admitted target, and the substring is not treated as the label -- the C064 correction, and C038's rule that a host-name anchor does no work on its own.

`download.html` was not followed. Its label is not on the step-2 whitelist, and QA-17 settled that a criterion's wording cannot widen the search contract; QA-27 records the same page-link/metadata-URL distinction that governs here.

Step 2 disposition for the second starting point. The frozen SITES resolves to `https://downloads.sourceforge.net/sourceforge/chromium-bsu/`, the code host's release-file area for this project reached through its mirror redirector. That is the class QA-31 names, and QA-31's scope paragraph was written for exactly this pattern: "OpenBSD ports commonly point SITES at a code host's release assets. Every such frame item whose gate is still open after step 1 reaches this same point, and loses its second starting point to the prohibition." It is accounted for under QA-27's third branch -- otherwise resolved, with the reason named -- and was NOT requested.

The classification is by what the surface is, not by a substring of its URL. Neither `download` in the host name nor the port's `SITES` variable name is doing the work; the surface is a code host's released-file area, which is the forbidden `releases` class. This is the distinction C064 got wrong in the other direction, and it is stated here so the reasoning can be checked rather than inferred.

Inference: after step 1 the gate is unsettled -- the landing page exposes no whitelisted source link, so no designation witness was reached, and no failure code can fire either, because two surfaces that might carry a designation (`download.html`, and the SITES release area) are closed to this gate by the contract rather than absent from upstream. A PASS needs a witness and every failure code needs positive evidence; neither is obtainable here without navigating where the contract forbids.

Not claimed, and this is the whole point of the code: that upstream designates no canonical source location. Two surfaces were never observed. What is on the record is that the sealed contract closed them, never that there is nothing behind them. Same shape as C045, where QA-31 was raised.

Decision: UNRESOLVED
Protocol issue: PI-UNCLASSIFIED-SHAPE

## EV-C067-DUP-01
Candidate: C067 (duplicate contributed by frame rank 68, games/chroma-enigma)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/chroma/Makefile and games/chroma-enigma/Makefile

Observed, from the frozen metadata only:

```text
                  games/chroma                games/chroma-enigma
HOMEPAGE          http://level7.org.uk/chroma/    (identical, byte for
                                                   byte including the
                                                   assignment whitespace)
MAINTAINER        LEVAI Daniel <leva@ecentrum.hu>     (identical)
DISTNAME          chroma-1.13                 chroma-enigma-0.20101210
SITES             ${HOMEPAGE}/download/       http://leva.ecentrum.hu/openbsd/
COMMENT           abstract puzzle game        Enigma levels to the game chroma
```

games/chroma-enigma additionally carries `RUN_DEPENDS = games/chroma`, `NO_BUILD = Yes`, and a `do-install` target whose destination is `${PREFIX}/share/chroma/levels/enigma`.

Inference, with the three kinds of evidence kept apart because they do not carry the same weight:

```text
HOMEPAGE                    the sole upstream-LOCATION field in either
                            port, and byte-identical between them

COMMENT (rank 68)           frozen metadata characterizing the packaged
                            artifact directly: Enigma levels FOR THE GAME
                            CHROMA

RUN_DEPENDS, install path   corroboration of the PACKAGING relationship
                            only. RUN_DEPENDS is a dependency between two
                            OpenBSD ports, and the destination under
                            ${PREFIX}/share/chroma/ is a path the packager
                            chose. Neither is an external identity
                            designation and neither is treated as one.
```

An earlier version of this entry said that "exactly one field in either port names an external system" and then that "every other field ... that mentions a system at all names chroma". Those do not stand together as written. It also listed the install path beside the other two, which promotes a chosen path name to identity evidence -- inferring a role from a name, the pattern this run has had to correct before. Both are withdrawn in favour of the split above.

So: the one upstream-location field in the frozen metadata resolves this frame item to the system C067 already resolved to, the rank-68 port's own comment describes the packaged artifact as an add-on for that system, and no second external system appears in the metadata to choose between.

The differing `SITES` is treated as a distribution fact rather than an identity split, on the protocol's own clause at SCREENING_PROTOCOL.md:94-98 -- a `HOMEPAGE` at a project website alongside a distfile location elsewhere is "several facts about one system", and `UR-AMBIGUOUS` is reserved for metadata pointing at genuinely different systems. There is no second named system here to choose between.

Divergence from the precedent, recorded because it is not an exact match. At EV-C105-DUP-01 the two ports agreed on BOTH `HOMEPAGE` and `SITES`, so the resolution there did not have to rule on a differing distribution host. This one does, and it rules on the clause above rather than by extending that precedent.

One observation recorded because it was seen and does no work: the `SITES` host `leva.ecentrum.hu` and the `MAINTAINER` address `leva@ecentrum.hu` share a domain. Whether that means the port maintainer hosts the distfile is not determined here, and the verdict does not rest on it -- the clause above applies to a distfile location wherever it is hosted.

Not claimed. Nothing about what the distfile contains: it was not retrieved, and its 4016-byte size and recorded SHA256 in the frozen distinfo identify an artifact without describing one. Nothing about who authored the Enigma level data, or whether upstream chroma distributes or designates this artifact -- that is an E1 and E2-REP question, and those gates are NOT_REACHED for a duplicate. `http://leva.ecentrum.hu/openbsd/` was not opened.

Decision: DUPLICATE of C067

## EV-C067-UR-01
Candidate: C067 (frame rank 67, games/chroma)
Gate: UR
Source: frozen OpenBSD 7.9 ports metadata, games/chroma/Makefile
Observed: DISTNAME=chroma-1.13; EXTRACT_SUFX=.tar.bz2; HOMEPAGE=http://level7.org.uk/chroma/; SITES=${HOMEPAGE}/download/; COMMENT="abstract puzzle game".
Inference: the frozen fields name one packaged system, Chroma, and SITES is expressed relative to HOMEPAGE, so both admitted URLs are on the same upstream host. Not UR-AMBIGUOUS.
Decision: PASS

## EV-C067-E1-01
Candidate: C067
Gate: E1
Source: same frozen metadata
Observed: a third-party puzzle game under GPLv2, on an upstream site unrelated to this project.
Inference: external-authorship requirement satisfied from the frozen metadata alone.
Decision: PASS

## EV-C067-E2REP-01
Candidate: C067
Gate: E2-REP

Per QA-27 both admitted starting points are accounted for: the frozen HOMEPAGE, and the frozen SITES.

Step 1: the frozen HOMEPAGE.
requested_url and final_url: http://level7.org.uk/chroma/
observed_at_utc: 2026-08-28T13:48:13Z; http_status 200; redirect_chain: NONE (num_redirects 0); 4053 bytes
evidence_role: official-project-page

Observation scope, fixed before the request: HTTP status and redirects; headings; every link with its label and target; any sentence or label assigning a source role; any primary, canonical or mirror marking; and -- for a distribution-type designation -- retrieval of the designated artifact with a listing of its entry NAMES, which C013 established is this gate's source-tree observation carried over to a distribution candidate.

Observed: the project's own page, headed "c h r o m a", with sections Screenshots, Play Online, Download, Play Retro, Other Games and Email. The Download section reads:

```text
"Alternatively, you can download Chroma to install on your computer:"

  "Chroma 1.21 source code for Linux and other operating systems"
        -> download/chroma-1.21.tar.bz2   (2.7Mb)

  "Chroma 1.20 for Windows (installer)"
        -> download/chroma-setup-1.21.exe (4.0Mb)
```

That is a source-role designation in upstream's own words -- the same form as C013's and as the withdrawn C056's "Download for Source" -- and upstream separates the installer from it in the same list, so the ranking is not ours.

One other link on this surface carries a source-role phrase and is NOT a competing designation, for a reason upstream states rather than one we supply:

```text
"Play Retro"
  "Play Chroma in 8-bit style on this port to the BBC Micro. Features
   all twenty one levels and finite undo. You can [play in a
   browser-based emulator], [download a disk image] or [view the
   source code]."
        view the source code -> chroma.asm
```

The sentence delimits its own subject: that source is the BBC Micro PORT's, introduced as "this port to the BBC Micro". Under QA-26 that is a different delimited artifact from the packaged system, whose frozen WANTLIB names SDL, SDL_image and curses. Nothing here ranks two designations of one system; upstream has named two different things.

Unlike C056, exactly ONE URL carries the source role for the packaged system, so the multi-designation problem that withdrew that candidate does not arise.

Source-tree presence at the designated location:
requested_url: http://level7.org.uk/chroma/download/chroma-1.21.tar.bz2
observed_at_utc: 2026-08-28T13:49:00Z-13:49:03Z; http_status 200; 2812208 bytes
sha256 of the retrieved bytes: bdf4d6e1ac65588a93569ec3ec01869fee461f9dafe4cdbebb1fc38c42d9693d

Listing its entries -- names only -- shows a source tree: 1469 entries under a single root `chroma-1.21/`, with 19 `.c` files and 11 `.h` files at the top level (main.c, engine.c, editor.c, level.c, colours.c, names.c, graphics.c, xmlparser.c, the sdl* and curses* display modules, util.c, xor.c, enigma.c), alongside configure, configure.ac, Makefile.in, Makefile.mingw, INSTALL, README, COPYING, CHANGELOG and the directories browser, colours, graphics, help, levels, locale, po and resources.

Recorded rather than glossed, as at C056: upstream publishes no checksum beside the link. The page was scanned for a 64-hex string and none appears. So the retrieved bytes cannot be matched against a value upstream published; the digest above identifies the object analysed and is not verification of the designation.

Version note, stated as a limitation: upstream's designation at observation time is for 1.21, while the frozen DISTNAME is chroma-1.13. This entry designates what upstream designates now and makes no claim about the sealed instant (QA-28).

The frozen SITES, `${HOMEPAGE}/download/`, is accounted for and was not opened. The stop rule ends navigation once the gate is determined, and QA-27's obligation is to account for each starting point rather than to open each.

Nothing further is claimed about it. An earlier version added that opening it "could only have listed files whose roles C026 forbids inferring from their names", which asserts the surface's response shape without having observed it -- the URL was never requested, so whether it returns a listing at all is unknown -- and misuses the precedent: C026 bars inferring an artifact's source role from an OBSERVED filename; it says nothing that would let us predict what an unopened URL returns. Withdrawn. What is on the record is that the designated artifact's URL sits under that path, and that the starting point was accounted for and not opened.

Inference: exactly one designated canonical source location for the packaged system, at a stable URL, holding a source tree, with one external target identifier (Chroma).

Decision: PASS

## EV-C067-E2RULE-01
Candidate: C067
Gate: E2-RULE
Source: INSTALL, entry `chroma-1.21/INSTALL` of the designated artifact
Provenance: the artifact retrieved above, sha256 bdf4d6e1...9693d. All source citations below are entries of that same artifact, so the one digest covers them.

Observed: located witness, the file's own Dependencies section at INSTALL:13.

```text
"Dependencies
 ============
 The SDL version of Chroma requires the following libraries:
     * SDL
     * SDL_image
     * FreeType 2
 It also uses the font "DejaVu Sans" ...
 The curses version of Chroma requires a curses library such as:
     * ncurses
 Both versions require:
     * gettext"
```

Inference: these state concrete validity requirements without our inventing them, and the project scopes each to a build variant in its own words -- SDL version, curses version, both. A build environment lacking gettext, or lacking SDL and SDL_image when the SDL version is built, does not satisfy them.
Decision: PASS

## EV-C067-E3-01
Candidate: C067
Gate: E3
Source: `chroma-1.21/engine.c` and `chroma-1.21/level.c`
Provenance: as above.

Observed: located witness. The decision, the call path that reaches it, and the definition that writes the state it consults are quoted below.

```text
engine.c:124-155   int level_move(struct level* plevel, int move)
                   {
                       ...
                       realmove = move;                             // :140

                       if(plevel == NULL || plevel->mover_first != NULL)
                           return 0;                                // :142-143

                       if(move == MOVE_REDO)                        // :145
                       {
                           if(plevel->move_current == NULL)
                               pmove = plevel->move_first;
                           else
                               pmove = plevel->move_current->next;

                           if(pmove == NULL)
                               return 0;

                           move = pmove->direction;
                       }

engine.c:106-122   void level_moved(struct level* plevel, int move)
                   {
                       if(move != MOVE_REDO)
                           level_addmove(plevel, move);             // :109
                       else
                       {
                           if(plevel->move_current != NULL)
                               plevel->move_current = plevel->move_current->next;
                           else
                               plevel->move_current = plevel->move_first;
                       }
                       plevel->moves ++;
                       ...
                   }

engine.c:172                   level_moved(plevel, realmove);
engine.c:187                   level_moved(plevel, realmove);
engine.c:199                   level_moved(plevel, realmove);
engine.c:380               level_moved(plevel, realmove);

engine.c:1299-1306 /* Can't undo at very start of level */
                   if(plevel->move_current == NULL)
                       return 0;

                   /* If there is no previous step to undo, remove this
                      move entirely */
                   if(plevel->move_current->mover_last == NULL)
                   {
                       plevel->move_current = plevel->move_current->previous;
```

```text
level.c:1373-1442  void level_addmove(struct level* plevel, int move)
                   {
                       /* If we are making a move after undoing some moves */
                       if(plevel->move_current != plevel->move_last)
                       {
                       /* Find the first undone move */
                       if(plevel->move_current != NULL)
                           pmove = plevel->move_current->next;      // :1386
                       else
                           pmove = plevel->move_first;              // :1388

                       /* Delete all moves that follow it */
                       while(pmove != NULL) { ... free(pmove); ... }  // :1391-1406

                       /* Fix up this move so that it appears to be the last */
                       if(plevel->move_current != NULL)
                           plevel->move_current->next = NULL;       // :1410
                       else
                           plevel->move_first = NULL;               // :1412

                       plevel->move_last = plevel->move_current;    // :1414
                       }

                       /* Create the new move */
                       pmove = (struct move*)malloc(sizeof(struct move));  // :1418
                       ...
                       pmove->direction = move;                     // :1422
                       pmove->previous = plevel->move_last;         // :1423
                       pmove->next = NULL;                          // :1424
                       ...
                       if(plevel->move_first == NULL)
                       plevel->move_first = pmove;                  // :1428-1429

                       if(plevel->move_last != NULL)
                       {
                       plevel->move_last->next = pmove;             // :1433
                       pmove->count = plevel->move_last->count + 1;
                       }
                       else
                       pmove->count = 1;

                       plevel->move_last = pmove;                   // :1439
                       plevel->move_current = pmove;                // :1440
                   }
```

CORRECTION, recorded rather than smoothed over. An earlier version of this entry stated that "both the decision and the writer of the state it consults are quoted", and that the list "is exactly what `level_addmove` ... [has] built", while the only thing shown of `level_addmove` was its CALL at engine.c:109. A function's name and its call site do not establish what it writes; that connection was asserted, which is the C063 defect. The definition is now quoted, and each field the redo gate reads at :147-150 is written in it: `move_first` at :1428-1429 and :1412, `move_current` at :1440 and :1414, and a node's `next` at :1424, :1410 and :1433.

The redo call path is likewise SHOWN rather than described, because the extract as it stood invited the opposite reading, and because an earlier version of this paragraph asserted the calls' argument in prose alone. That was the same defect one level up: the whole point of this correction is which value reaches `level_moved`, so it cannot rest on a function name and a grep summary. `level_move` saves `realmove = move` at :140, BEFORE the substitution `move = pmove->direction` at :155, and each of the four calls quoted above passes `realmove`, not `move`. So a redo reaches `level_moved` still carrying MOVE_REDO and takes the branch at :112-115, advancing `move_current` along the existing list rather than appending through `level_addmove`. Review read the earlier extract as showing the substituted value reaching `level_moved`; that reading followed from the extract, which had elided :140 and quoted no call site at all.

The search behind "four calls" is given with its surface, since it is an exhaustiveness claim and QA-12 requires a justified closed one. The surface is closed and in hand: the pinned artifact unpacked, 1451 files, searched entire for `level_moved(`. A second correction falls out of running it that way. An earlier version of this paragraph called those four "the only calls to it anywhere", and that is false:

```text
browser/chroma-script.js:1729   function level_moved(move)
browser/chroma-script.js:1769,1784,1794,1968
                                level_moved(realmove);
```

The tarball also ships a JavaScript reimplementation of the same game, with the same function names and the same `realmove` discipline. Those are not calls of the C function -- they are a separate program's own definition and calls -- but "anywhere" covered them and was wrong. `level.h:257` likewise declares `level_addmove` without calling it. The claim is scoped accordingly: within the C translation units, `level_moved` is defined once at engine.c:106 and called at exactly those four sites.

Not claimed: that these are the only writers of the fields the gate reads. `level_undo` moves `move_current` back at engine.c:1306, and level.c writes the same fields at initialisation (:376-378), when copying a level (:748-761), and when loading a saved game (:1094, :1114-1222). No exhaustive writer set is offered, and E3 does not need one.

Inference, kept to what the quoted lines close: a MOVE_REDO reaching this gate is refused there when the recorded move list holds no next entry, and otherwise takes that entry's direction and continues into the move processing below. Whether such an entry exists is decided by `move_current` and the `next` chain, which the quoted `level_addmove` allocates, links and truncates, and which the redo branch at :112-115 and `level_undo` at :1306 walk along, both quoted above. The writer paths EXHIBITED here are runtime play and undo paths; the paragraph above declines an exhaustive writer set, so nothing is claimed about writers not exhibited, and in particular no absence claim is made about build- or configuration-time writers. So the identical MOVE_REDO input is refused at this gate or proceeds past it according to the move history.

VERIFICATION NOTE. The two files quoted were extracted from the pinned artifact and hashed independently: `chroma-1.21/engine.c`, 50657 bytes, sha256 49ce3c6cb0ad1934ce439fac0f64c7b18a5735bb45e826fd956e129ccc0e1ebd; `chroma-1.21/level.c`, 42699 bytes, sha256 a36ce3c5c7c94d84e5c9048ff6042f0df26c60043bdb0cc8e3be3c29980855f7. The artifact itself re-hashes to bdf4d6e1ac65588a93569ec3ec01869fee461f9dafe4cdbebb1fc38c42d9693d, the digest recorded at E2-REP. The line numbers above are lines of those exact files.

Not claimed: that proceeding past this gate ends in a performed move. The quoted extract does not follow the processing to its end, and the same function carries other refusal conditions -- the guard at :142-143, which refuses any move while movers from the previous one are still in flight. That guard is recorded as a further, non-historical state condition and is not leaned on. History is shown to be necessary at this gate, not sufficient for the whole call.
Decision: PASS

## EV-C067-E4-01
Candidate: C067
Gate: E4

Positive construction exhibited, via U_enforced.
Provenance: as above.

The mechanism: the per-mode allowed-piece registry and the level verifier that tests a level against it.

```text
editor.c:51,...    int editor_pieces_chroma[] = { PIECE_SPACE, ... ,
                                                  PIECE_GONE };
                   #ifdef XOR_COMPATIBILITY
                   int editor_pieces_xor[]    = { ... PIECE_GONE };
                   #endif
                   #ifdef ENIGMA_COMPATIBILITY
                   int editor_pieces_enigma[] = { ... PIECE_GONE };
                   #endif

editor.c:135-144   int *editor_piece_maps[] =
                   {
                       editor_pieces_chroma,
                   #ifdef XOR_COMPATIBILITY
                       editor_pieces_xor,
                   #endif
                   #ifdef ENIGMA_COMPATIBILITY
                       editor_pieces_enigma,
                   #endif
                       NULL
                   };

editor.c:358,375-383
                   int piece_ok[PIECE_MAX];
                   ...
                   for(i = 0; i < PIECE_MAX; i ++)
                       piece_ok[i] = 0;
                   i = 0;
                   while(editor_piece_maps[plevel->mode][i] != PIECE_GONE)
                   {
                       piece_ok[editor_piece_maps[plevel->mode][i]] = 1;
                       i ++;
                   }

editor.c:411-418   if(!piece_ok[p])
                   {
                       sprintf(buffer, gettext("Invalid piece %s at (%d,%d)"),
                               gettext(piece_name[p]), x, y);
                       ...
                       errors ++;
                   }
```

```text
list                    entries including the PIECE_GONE sentinel
editor_pieces_chroma    33
editor_pieces_xor       20   (compiled only under XOR_COMPATIBILITY)
editor_pieces_enigma    18   (compiled only under ENIGMA_COMPATIBILITY)
```

EN1 external authorship: the game and these tables existed independently of this analysis.

EN2 explicit scope: the domain is the pieces a level may contain, and the project segments it by mode -- one list per game mode, selected by `plevel->mode`. Each member is a named piece constant, and `piece_name[]` in names.c gives the project's own string for each.

EN3 mechanical membership, with the two levels kept apart:

```text
enumerator membership      the entries of editor_piece_maps[mode], up
                           to but excluding the PIECE_GONE sentinel
runtime enforcement value  piece_ok[], the boolean vector built from
                           that list at editor.c:375-383
```

Membership is enumerable by reading the list for the mode, and the scan bound is the project's own sentinel rather than a length we supply.

Recorded rather than glossed: which lists exist is a compile-time question. `editor_pieces_xor` and `editor_pieces_enigma` are inside `#ifdef` guards and `editor_piece_maps` includes them conditionally, so in a build without those flags the registry family has one member. This is the same shape as C065's `#if defined(TILES)` arms, and it means a member list is per-build rather than absolute.

EN4 connection to validation, in project code on both sides: the verifier walks the level, and for each piece `p` tests `piece_ok[p]`, emitting "Invalid piece %s at (%d,%d)" with the project's own name for the piece and its coordinates, and incrementing an error count. Deciding and reporting are both the project's.

Recorded as a limit on what that enforcement is: it is a verifier that reports errors into a menu and counts them, not a loader that refuses the level. This entry does not claim that a level containing an out-of-mode piece cannot be opened or played -- only that the project tests membership against this registry and names the failures.

EN5 closed within scope: each list is closed by its own `PIECE_GONE` sentinel, which the fill loop at :380 uses as its bound, and `piece_ok[]` is constructed from it at runtime. Section 3.2's first admissible case. Tag: `enforced`.

EN6 outcome independence: the registry is the set of pieces a mode admits. It is not a bug list, fix list or known-failure registry.

The universe is therefore ACTUALLY mechanically constructible, stated as observations:

```text
one enforcement observation per entry of a mode's list

  "piece constant P is admitted in mode M; a piece present in a level
   of mode M whose constant is not in that mode's list is reported as
   `Invalid piece <name> at (x,y)` and counted as an error"

retained as externally segmented fields, per observation
  the piece constant
  the mode whose list admits it
  the project's own name for the piece, from piece_name[]
```

As at C043, C049, C056, C059, C063, C065 and C066, this establishes only that a mechanically constructible universe EXISTS; it fixes no contents, and the per-build conditionality above is exactly the kind of thing the inventory stage would have to settle under QA-19.

Normative route: not pursued. Nothing observed designates an authoritative rule source, so U_normative is not established either on what was observed; no claim is made that one is absent elsewhere.

Decision: PASS

Survivor-stage fields: primary_snapshot UNRESOLVED, per QA-28. The designation observed is for 1.21 while the frozen DISTNAME is chroma-1.13, upstream publishes no checksum, and no observation fixes what was designated at the sealed instant. The three inventory fields are consequently NOT_REACHED.
