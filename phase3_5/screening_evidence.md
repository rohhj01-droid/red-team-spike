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
