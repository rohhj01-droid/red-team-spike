# Screening batch 09 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b09.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 65 | games/chocolate-doom | PASS | C061 | PASS | PASS | PASS | PASS | PASS | ELIGIBLE | NONE | NONE |
| 66 | games/choria | PASS | C062 | PASS | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | E4 | PI-UNCLASSIFIED-SHAPE |
| 67 | games/chroma | PASS | C063 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 68 | games/chroma-enigma | DUPLICATE | NONE | - | - | - | - | - | DUPLICATE | UR | NONE |
| 69 | games/chromium-bsu | PASS | C064 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 70 | games/circuit | FAIL_NONE | NONE | - | - | - | - | - | REJECTED | UR | UR-NONE |
| 71 | games/classicube | PASS | C065 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 72 | games/clidle | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |

## rank 65 -- games/chocolate-doom

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.chocolate-doom.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/chocolate-doom/chocolate-doom | DIST_TUPLE | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T06:27:29Z | 65 | https://www.chocolate-doom.org/wiki/index.php/Development | step-2 link 'Development': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:27:29Z | 65 | https://www.chocolate-doom.org/wiki/index.php/Development | step-2 link 'development': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:27:30Z | 65 | https://github.com/chocolate-doom/chocolate-doom | landing page rendered a README (7801 chars of page text); not used | used: no |

## EV-C061-E1-01

Candidate: C061
Gate: E1
Source:   https://github.com/chocolate-doom/chocolate-doom

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C061-E2REP-02

Candidate: C061
Gate: E2-REP
Source:   https://github.com/chocolate-doom/chocolate-doom

Surfaces:  https://www.chocolate-doom.org/ -> observed
           https://github.com/chocolate-doom/chocolate-doom -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Source code' at https://www.chocolate-doom.org/wiki/index.php/Chocolate_Doom -> https://github.com/chocolate-doom/chocolate-doom | identifier 'chocolate-doom' (the repository's name, contract 6) appears on https://www.chocolate-doom.org/wiki/index.php/Chocolate_Doom | tree pinned at a2dfd51fcc00d272dc8a17a97ccd6683333ff4ea (734 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C061-E2RULE-03

Candidate: C061
Gate: E2-RULE
Source:   README.md:51

Observed: '‘-file’ will not work.'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C061-E3-04

Candidate: C061
Gate: E3
Source:   man/default.cfg.template:40

Observed: 'the game exits, so any invalid lines or comments will be lost.'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C061-E4-05

Candidate: C061
Gate: E4
Source:   src/d_mode.c:26 valid_modes

Observed: EN2: src/d_mode.c:23 'Valid game mode/mission combinations, with the number of'; EN4: src/d_mode.c:48 'Check that a gamemode+gamemission received over the network is valid.'; EN4: src/net_server.c:706 'if (!D_ValidGameMode(data.gamemission, data.gamemode)'; EN4: src/net_server.c:709 'server: error: invalid connect data'; EN4: src/net_common.c:451 'if (!D_ValidEpisodeMap(mission, mode, settings->episode, settings->map))'

Inference: one enumerator admitted under the frozen grammar with a quoted identification and refusal path (contract Section 8)

Decision: PASS


## rank 66 -- games/choria

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://choria.gitlab.io/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://gitlab.com/jazztickets/uploads/-/raw/main/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T06:27:38Z | 66 | https://gitlab.com/choria/code | landing page rendered a README (281 chars of page text); not used | used: no |

## EV-C062-E1-01

Candidate: C062
Gate: E1
Source:   https://choria.gitlab.io

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C062-E2REP-02

Candidate: C062
Gate: E2-REP
Source:   https://gitlab.com/choria/code

Surfaces:  https://choria.gitlab.io/ -> observed
           https://gitlab.com/jazztickets/uploads/-/raw/main/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Source Code' at https://choria.gitlab.io/ -> https://gitlab.com/choria/code | identifier 'code' (the repository's name, contract 6) appears on https://choria.gitlab.io/ | tree pinned at 94cb88ea5aa3510e41ccac66e4c26c97ce570a53 (1133 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C062-E2RULE-03

Candidate: C062
Gate: E2-RULE
Source:   README:118

Observed: "All skills must be equipped to your action bar before they're activated."

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C062-E3-04

Candidate: C062
Gate: E3
Source:   README:118

Observed: "All skills must be equipped to your action bar before they're activated."

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C062-E4-05

Candidate: C062
Gate: E4
Source:   the frozen grammar over 41 candidate rows

Surfaces:  ext/lua/lauxlib.c:509
           ext/lua/lbaselib.c:509
           ext/lua/lcorolib.c:124
           ext/lua/lcorolib.c:207
           ext/lua/lctype.c:28
           ext/lua/ldblib.c:452
           ext/lua/linit.c:28
           ext/lua/liolib.c:754
           ext/lua/liolib.c:773
           ext/lua/liolib.c:788
           ext/lua/ljumptab.h:19
           ext/lua/llex.c:45
           ext/lua/lmathlib.c:647
           ext/lua/lmathlib.c:706
           ext/lua/loadlib.c:684
           ext/lua/loadlib.c:697
           ext/lua/lopcodes.c:22
           ext/lua/lopnames.h:15
           ext/lua/loslib.c:409
           ext/lua/lparser.c:1354
           ext/lua/lstrlib.c:252
           ext/lua/lstrlib.c:332
           ext/lua/lstrlib.c:1856
           ext/lua/ltablib.c:412
           ext/lua/ltm.c:30
           ext/lua/lutf8lib.c:276
           ext/picosha2/picosha2.h:50
           ext/picosha2/picosha2.h:63
           src/menu.cpp:79
           src/scripting.cpp:65
           LICENSE:1
           LICENSE:2
           LICENSE:91
           LICENSE:163
           LICENSE:204
           LICENSE:264
           LICENSE:494
           LICENSE:621
           LICENSE:990
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: catalogue decided 2 rows, 39 undecided, none admitted

Inference: no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 67 -- games/chroma

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://level7.org.uk/chroma/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://level7.org.uk/chroma//download/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-30T06:27:49Z | 67 | http://level7.org.uk/chroma/chroma.asm | step-2 link 'view the source code': target is not a repository root (unclassifiable); observed once, not read | used: no |

## EV-C063-E1-01

Candidate: C063
Gate: E1
Source:   https://level7.org.uk/chroma

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C063-E2REP-02

Candidate: C063
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://level7.org.uk/chroma/ -> observed
           http://level7.org.uk/chroma//download/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 68 -- games/chroma-enigma

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://level7.org.uk/chroma/ | HOMEPAGE | unmatched | not-reached |  |  |  |
| http://leva.ecentrum.hu/openbsd/ | SITES | unmatched | not-reached |  |  |  |

## EV-R068-UR-01

Candidate: (none: rank 68)
Gate: UR
Source:   games/chroma-enigma/Makefile

Observed: identity key https://level7.org.uk/chroma

Inference: the same upstream as C063 (contract Section 3)

Decision: DUPLICATE


## rank 69 -- games/chromium-bsu

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://chromium-bsu.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/chromium-bsu/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T06:27:51Z | 69 | http://sourceforge.net/projects/chromium-bsu/ | step-2 link 'sourceforge project': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C064-E1-01

Candidate: C064
Gate: E1
Source:   https://chromium-bsu.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C064-E2REP-02

Candidate: C064
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://chromium-bsu.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/chromium-bsu/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 70 -- games/circuit

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://distfiles.sigtrap.nl/ | SITES | unmatched | not-reached |  |  |  |

## EV-R070-UR-01

Candidate: (none: rank 70)
Gate: UR
Source:   games/circuit/Makefile

Observed: homepage=None sites=['https://distfiles.sigtrap.nl/'] gh=None tuples=[]

Inference: identity key rule (contract Section 3): FAIL_NONE

Decision: FAIL


## rank 71 -- games/classicube

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/ClassiCube/ClassiCube | HOMEPAGE+DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T06:27:54Z | 71 | https://github.com/ClassiCube/ClassiCube | landing page rendered a README (20585 chars of page text); not used | used: no |

## EV-C065-E1-01

Candidate: C065
Gate: E1
Source:   https://github.com/classicube/classicube

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C065-E2REP-02

Candidate: C065
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/ClassiCube/ClassiCube -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/ClassiCube/ClassiCube

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 72 -- games/clidle

## EV-R072-UR-01

Candidate: (none: rank 72)
Gate: UR
Source:   games/clidle/Makefile

Observed: modules=['lang/go'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED
