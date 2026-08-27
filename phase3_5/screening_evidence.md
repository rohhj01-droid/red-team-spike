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

Positive construction exhibited, via U_enforced. All observations are at the primary snapshot: master had not moved since 2026-05-30T00:35:55Z, so raw reads of master on 2026-08-27 resolve to commit a62b868e9247c4aafd66f597cdfa8d2609704087, the revision the snapshot rule fixes.

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

Positive construction exhibited, via U_enforced. All observations are made in the primary snapshot itself: this is a distribution candidate, so the snapshot is the designated canonical artifact by content hash, sha256:de7eb94ab66212ae7758376524368a8ab208234b33796625ca630547dbc83832, verified against the value upstream publishes. The paths below are paths inside that verified artifact, which removes the usual gap between "the revision the rule fixes" and "the bytes actually read".

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

The designated location itself, svn://svn.zoy.org/abuse/abuse/trunk, was not observed either: no Subversion client is available in this environment. That is a tooling limit on our side, recorded as such rather than folded into the network result.

Adjudication:

```text
DESIGNATION established
  upstream states, under its own "Source code" heading, that
  development takes place in a Subversion repository, and gives the
  checkout URL. Exactly one source location is designated; the
  Download page is a release announcement target and no allowed
  surface designates it as a source location.

PASS not established
  E2-REP also asks that the location actually hold a source tree.
  The repository's only HTTP view returned 5xx three times, and its
  native endpoint could not be reached with the tooling available
  here. The observation was not made.

FAIL not established
  the contract is explicit that 5xx is transport indeterminacy and
  NOT evidence of absence, and that such an item takes a protocol
  issue rather than a failure code. A broken Trac plugin and a
  missing local client are facts about the observation, not about
  the candidate.
```

Both unmet conditions are observation limits. Neither is coded as a property of Abuse.

Decision: UNRESOLVED (PI-TRANSPORT-INDETERMINATE)

Gates after E2-REP are NOT_REACHED. Screening stopped here rather than
continuing to read, per QA-21.
