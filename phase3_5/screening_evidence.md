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
