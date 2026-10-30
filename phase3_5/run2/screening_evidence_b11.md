# Screening batch 11 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b11.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 81 | games/cpat | PASS | C072 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 82 | games/crack-attack | PASS | C073 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 83 | games/crimson | PASS | C074 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIABLE-SURFACE |
| 84 | games/crispy-doom | PASS | C075 | PASS | PASS | PASS | PASS | PASS | ELIGIBLE | NONE | NONE |
| 85 | games/cromagrally | PASS | C076 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 86 | games/crossfire-client | PASS | C077 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 87 | games/csmash | PASS | C078 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 88 | games/cubiomes-viewer | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |

## rank 81 -- games/cpat

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://cpat.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/cpat/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T06:48:40Z | 81 | https://sourceforge.net/project/showfiles.php?group_id=160188 | step-2 link 'source code': target is not a repository root (distfile-location); observed once, not read | used: no |

## EV-C072-E1-01

Candidate: C072
Gate: E1
Source:   https://cpat.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C072-E2REP-02

Candidate: C072
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://cpat.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/cpat/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 82 -- games/crack-attack

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.nongnu.org/crack-attack/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://download.savannah.nongnu.org/releases/crack-attack/ | SITES | distfile-location | observed | distfile-location | 200 | distfile-location |
| https://download-mirror.savannah.nongnu.org/releases/crack-attack/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| https://ftp.cc.uoc.gr/mirrors/nongnu.org/crack-attack/ | SITES+SITES | unmatched | unreachable |  |  |  |
| https://mirror.ossplanet.net/nongnu/crack-attack/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| https://mirror.csclub.uwaterloo.ca/nongnu/crack-attack/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| https://nongnu.askapache.com/crack-attack/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| http://savannah.c3sl.ufpr.br/crack-attack/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-30T06:50:04Z | 82 | http://www.livejournal.com/users/gnu_lorien/ | step-2 link 'Development Journal': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C073-E1-01

Candidate: C073
Gate: E1
Source:   https://www.nongnu.org/crack-attack

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C073-E2REP-02

Candidate: C073
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.nongnu.org/crack-attack/ -> observed
           https://download.savannah.nongnu.org/releases/crack-attack/ -> observed
           https://download-mirror.savannah.nongnu.org/releases/crack-attack/ -> observed
           https://ftp.cc.uoc.gr/mirrors/nongnu.org/crack-attack/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           https://mirror.ossplanet.net/nongnu/crack-attack/ -> observed
           https://mirror.csclub.uwaterloo.ca/nongnu/crack-attack/ -> observed
           https://nongnu.askapache.com/crack-attack/ -> observed
           http://savannah.c3sl.ufpr.br/crack-attack/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 83 -- games/crimson

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://crimson.seul.org/ | HOMEPAGE | unmatched | unclassifiable | unclassifiable | 200 |  |
| http://crimson.seul.org/files/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

## EV-C074-E1-01

Candidate: C074
Gate: E1
Source:   https://crimson.seul.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C074-E2REP-02

Candidate: C074
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://crimson.seul.org/ -> unclassifiable
           http://crimson.seul.org/files/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIABLE-SURFACE

Decision: UNRESOLVED


## rank 84 -- games/crispy-doom

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://fabiangreffrath.github.io/crispy-homepage/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/fabiangreffrath/crispy-doom | DIST_TUPLE | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T06:50:15Z | 84 | https://github.com/fabiangreffrath/crispy-doom | landing page rendered a README (12983 chars of page text); not used | used: no |

## EV-C075-E1-01

Candidate: C075
Gate: E1
Source:   https://github.com/fabiangreffrath/crispy-doom

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C075-E2REP-02

Candidate: C075
Gate: E2-REP
Source:   https://github.com/fabiangreffrath/crispy-doom

Surfaces:  https://fabiangreffrath.github.io/crispy-homepage/ -> observed
           https://github.com/fabiangreffrath/crispy-doom -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Sourcecode' at https://fabiangreffrath.github.io/crispy-homepage/ -> https://github.com/fabiangreffrath/crispy-doom | identifier 'crispy-doom' (the repository's name, contract 6) appears on https://github.com/fabiangreffrath/crispy-doom | tree pinned at fdeabe4c23a833534b70aa84a22f1685aae7125d (800 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C075-E2RULE-03

Candidate: C075
Gate: E2-RULE
Source:   man/default.cfg.template:38

Observed: 'Invalid lines or comments in the file will be ignored, but it is advisable'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C075-E3-04

Candidate: C075
Gate: E3
Source:   man/default.cfg.template:40

Observed: 'the game exits, so any invalid lines or comments will be lost.'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C075-E4-05

Candidate: C075
Gate: E4
Source:   src/d_mode.c:26 valid_modes

Observed: EN2: src/d_mode.c:23 'Valid game mode/mission combinations, with the number of'; EN4: src/d_mode.c:50 'Check that a gamemode+gamemission received over the network is valid.'; EN4: src/net_server.c:706 'if (!D_ValidGameMode(data.gamemission, data.gamemode)'; EN4: src/net_server.c:709 'server: error: invalid connect data'; EN4: src/net_common.c:451 'if (!D_ValidEpisodeMap(mission, mode, settings->episode, settings->map))'

Inference: one enumerator admitted under the frozen grammar with a quoted identification and refusal path (contract Section 8)

Decision: PASS


## rank 85 -- games/cromagrally

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://pangeasoft.net/cromag | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/jorio/CroMagRally | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/jorio/Pomme | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T06:50:17Z | 85 | https://github.com/jorio/CroMagRally | landing page rendered a README (5833 chars of page text); not used | used: no |
| 2026-10-30T06:50:18Z | 85 | https://github.com/jorio/Pomme | landing page rendered a README (5347 chars of page text); not used | used: no |

## EV-C076-E1-01

Candidate: C076
Gate: E1
Source:   https://github.com/jorio/cromagrally

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C076-E2REP-02

Candidate: C076
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://pangeasoft.net/cromag -> observed
           https://github.com/jorio/CroMagRally -> observed
           https://github.com/jorio/Pomme -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/jorio/CroMagRally, https://github.com/jorio/Pomme

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 86 -- games/crossfire-client

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://crossfire.real-time.com/ | HOMEPAGE | unmatched | unreachable |  |  |  |
| https://downloads.sourceforge.net/sourceforge/crossfire/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C077-E1-01

Candidate: C077
Gate: E1
Source:   https://crossfire.real-time.com

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C077-E2REP-02

Candidate: C077
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://crossfire.real-time.com/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           https://downloads.sourceforge.net/sourceforge/crossfire/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 87 -- games/csmash

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://cannonsmash.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/cannonsmash/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C078-E1-01

Candidate: C078
Gate: E1
Source:   https://cannonsmash.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C078-E2REP-02

Candidate: C078
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://cannonsmash.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/cannonsmash/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 88 -- games/cubiomes-viewer

## EV-R088-UR-01

Candidate: (none: rank 88)
Gate: UR
Source:   games/cubiomes-viewer/Makefile

Observed: modules=['devel/qmake', 'x11/qt5'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED
