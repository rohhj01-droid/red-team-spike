# Screening batch 13 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b13.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 97 | games/dsda-doom | PASS | C085 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 98 | games/duke3ddata | PASS | C086 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 99 | games/dunelegacy | PASS | C087 | PASS | PASS | PASS | PASS | PASS | ELIGIBLE | NONE | NONE |
| 100 | games/dungeon | PASS | C088 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 101 | games/dungeon-crawl | PASS | C089 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIABLE-SURFACE |
| 102 | games/dustrac | PASS | C090 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 103 | games/dxx-rebirth | PASS | C091 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 104 | games/easyrpg | PASS | C092 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |

## rank 97 -- games/dsda-doom

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/kraflab/dsda-doom | HOMEPAGE+DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T07:33:56Z | 97 | https://github.com/dsda-org/dsda-doom | landing page rendered a README (5806 chars of page text); not used | used: no |

## EV-C085-E1-01

Candidate: C085
Gate: E1
Source:   https://github.com/kraflab/dsda-doom

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C085-E2REP-02

Candidate: C085
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/kraflab/dsda-doom -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/dsda-org/dsda-doom

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 98 -- games/duke3ddata

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.3drealms.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| ftp://ftp.3drealms.com/share/ | SITES | unmatched | unreachable |  |  |  |

## EV-C086-E1-01

Candidate: C086
Gate: E1
Source:   https://www.3drealms.com

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C086-E2REP-02

Candidate: C086
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.3drealms.com/ -> observed
           ftp://ftp.3drealms.com/share/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 99 -- games/dunelegacy

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://dunelegacy.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://www.linklevel.net/distfiles/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-30T07:34:04Z | 99 | https://github.com/dunecity-project/dunecity | landing page rendered a README (16383 chars of page text); not used | used: no |

## EV-C087-E1-01

Candidate: C087
Gate: E1
Source:   https://dunelegacy.com

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C087-E2REP-02

Candidate: C087
Gate: E2-REP
Source:   https://github.com/ggtothemax/dunecity

Surfaces:  https://dunelegacy.com/ -> observed
           http://www.linklevel.net/distfiles/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitHub' at https://dunelegacy.com/ -> https://github.com/ggtothemax/dunecity | link label 'GitHub' at https://dunelegacy.com/ -> https://github.com/ggtothemax/dunecity | identifier 'dunecity' (the repository's name, contract 6) appears on https://dunelegacy.com/ | tree pinned at 3b2d555be44816ff45555f8504894997387bea59 (7531 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C087-E2RULE-03

Candidate: C087
Gate: E2-RULE
Source:   docs/formations.md:593

Observed: 'Load rejects a point off the map.'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C087-E3-04

Candidate: C087
Gate: E3
Source:   docs/formations.md:1164

Observed: 'ordinary ground passability rejects their occupied tiles'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C087-E4-05

Candidate: C087
Gate: E4
Source:   include/FormationPlanner.h:77 kShapes

Observed: EN2: include/FormationPlanner.h:61 'The shapes a group can be ordered into'; EN4: src/players/QuantBotConfig.cpp:471 'for (const FormationPlanner::Shape shape : FormationPlanner::kShapes)'; EN4: src/players/QuantBotConfig.cpp:473 'return fallback;'; EN4: src/players/QuantBotConfig.cpp:695 'const int parsed = parseWaveFormation(shape, INT_MIN);'; EN4: src/players/QuantBotConfig.cpp:696 "QuantBot config: unknown WaveFormation '%s', keeping %s"

Inference: one enumerator admitted under the frozen grammar with a quoted identification and refusal path (contract Section 8)

Decision: PASS


## rank 100 -- games/dungeon

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://mirror.ifarchive.org/if-archive/games/source/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| ftp://ftp.ifarchive.org/if-archive/games/source/ | SITES | unmatched | unreachable |  |  |  |
| ftp://ftp.funet.fi/pub/misc/if-archive/games/source/ | SITES | unmatched | unreachable |  |  |  |
| http://www.vaxdungeon.com/vax-dungeon/Archive/dungeon/ | SITES | unmatched | observed | distfile-location | 404 | distfile-location |
| http://ifarchive.flavorplex.com/if-archive/games/source/ | SITES | unmatched | observed | distfile-location | 404 | distfile-location |

## EV-C088-E1-01

Candidate: C088
Gate: E1
Source:   https://mirror.ifarchive.org/if-archive

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C088-E2REP-02

Candidate: C088
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://mirror.ifarchive.org/if-archive/games/source/ -> observed
           ftp://ftp.ifarchive.org/if-archive/games/source/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           ftp://ftp.funet.fi/pub/misc/if-archive/games/source/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://www.vaxdungeon.com/vax-dungeon/Archive/dungeon/ -> observed (HTTP 404)
           http://ifarchive.flavorplex.com/if-archive/games/source/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 101 -- games/dungeon-crawl

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.dungeoncrawl.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| ftp://ftp.dungeoncrawl.org/dev/4.0.x/src/ | SITES | unmatched | unclassifiable | unclassifiable |  |  |

## EV-C089-E1-01

Candidate: C089
Gate: E1
Source:   https://www.dungeoncrawl.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C089-E2REP-02

Candidate: C089
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.dungeoncrawl.org/ -> observed
           ftp://ftp.dungeoncrawl.org/dev/4.0.x/src/ -> unclassifiable
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIABLE-SURFACE

Decision: UNRESOLVED


## rank 102 -- games/dustrac

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://juzzlin.github.io/DustRacing2D/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/juzzlin/DustRacing2D/archive/refs/tags/1.13.0/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/juzzlin/DustRacing2D | GH | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T07:36:26Z | 102 | http://www.qt.io | step-2 link 'Qt development framework': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T07:36:27Z | 102 | https://github.com/juzzlin/DustRacing2D | landing page rendered a README (6867 chars of page text); not used | used: no |

## EV-C090-E1-01

Candidate: C090
Gate: E1
Source:   https://github.com/juzzlin/dustracing2d

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C090-E2REP-02

Candidate: C090
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://juzzlin.github.io/DustRacing2D/ -> observed
           https://github.com/juzzlin/DustRacing2D/archive/refs/tags/1.13.0/ -> closed-by-class (forbidden class, never requested)
           https://github.com/juzzlin/DustRacing2D -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/juzzlin/DustRacing2D

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 103 -- games/dxx-rebirth

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.dxx-rebirth.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://www.dxx-rebirth.com/download/dxx/rebirth/ | SITES | unmatched | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T07:36:30Z | 103 | https://www.dxx-rebirth.com/d1x-rebirth_v0.58.1-src.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T07:36:36Z | 103 | https://www.dxx-rebirth.com/d2x-rebirth_v0.58.1-src.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T07:36:42Z | 103 | https://github.com/dxx-rebirth/dxx-rebirth | landing page rendered a README (6781 chars of page text); not used | used: no |

## EV-C091-E1-01

Candidate: C091
Gate: E1
Source:   https://www.dxx-rebirth.com

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C091-E2REP-02

Candidate: C091
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.dxx-rebirth.com/ -> observed
           https://www.dxx-rebirth.com/download/dxx/rebirth/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/dxx-rebirth/dxx-rebirth; a label link leads to another work's source: 'There also exists a C++ fork of this project on GitHub' at https://www.dxx-rebirth.com/ -> https://github.com/dxx-rebirth/dxx-rebirth

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 104 -- games/easyrpg

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://easyrpg.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/EasyRPG/Player/archive/refs/tags/0.5.3/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/EasyRPG/Player | GH | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T07:36:50Z | 104 | https://github.com/EasyRPG/ | step-2 link 'Code': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T07:36:51Z | 104 | https://easyrpg.org/contribute/ | step-2 link 'Contribute code or assets': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T07:36:52Z | 104 | https://github.com/EasyRPG/Player | landing page rendered a README (7141 chars of page text); not used | used: no |

## EV-C092-E1-01

Candidate: C092
Gate: E1
Source:   https://github.com/easyrpg/player

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C092-E2REP-02

Candidate: C092
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://easyrpg.org/ -> observed
           https://github.com/EasyRPG/Player/archive/refs/tags/0.5.3/ -> closed-by-class (forbidden class, never requested)
           https://github.com/EasyRPG/Player -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/EasyRPG/Player

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED
