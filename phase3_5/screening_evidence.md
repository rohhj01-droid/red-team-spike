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
