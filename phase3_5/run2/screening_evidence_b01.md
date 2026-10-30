# Screening batch 01 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b01.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | devel/flatzebra | PASS | C001 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 2 | devel/plib | PASS | C002 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 3 | devel/pygame | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |
| 4 | editors/tiled | PASS | C003 | PASS | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | E4 | NONE [CORRECTED after review: PI-UNCLASSIFIED-SHAPE, RQA-10] [CORRECTED after review, RQA-40: E2-RULE UNRESOLVED, E3 and E4 NOT_REACHED, stop gate E2-RULE] |
| 5 | emulators/advancemame | PASS | C004 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 6 | emulators/dgen-sdl | PASS | C005 | PASS | PASS | PASS | PASS | PASS | ELIGIBLE | NONE | NONE |
| 7 | emulators/dosbox | PASS | C006 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 8 | emulators/dosbox-x | PASS | C007 | PASS | PASS | PASS | PASS | PASS | ELIGIBLE | NONE | NONE |

## rank 1 -- devel/flatzebra

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html | HOMEPAGE | unmatched | unreachable |  |  |  |
| http://perso.b2b2c.ca/~sarrazip/dev/ | SITES | unmatched | unreachable |  |  |  |

## EV-C001-E1-01

Candidate: C001
Gate: E1
Source:   https://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C001-E2REP-02

Candidate: C001
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://perso.b2b2c.ca/~sarrazip/dev/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 2 -- devel/plib

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://plib.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://plib.sourceforge.net//dist/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |

## EV-C002-E1-01

Candidate: C002
Gate: E1
Source:   https://plib.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C002-E2REP-02

Candidate: C002
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://plib.sourceforge.net/ -> observed
           https://plib.sourceforge.net//dist/ -> observed (HTTP 403)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 3 -- devel/pygame

## EV-R003-UR-01

Candidate: (none: rank 3)
Gate: UR
Source:   devel/pygame/Makefile

Observed: modules=['lang/python'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED


## rank 4 -- editors/tiled

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.mapeditor.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/bjorn/tiled/archive/refs/tags/v1.8.6/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/bjorn/tiled | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-29T13:20:29Z | 4 | https://github.com/mapeditor/tiled | landing page rendered a README (7843 chars of page text); not used | used: no |
| 2026-10-29T13:15:01Z | 4 | https://www.gnu.org/philosophy/free-sw.html | step-2 link 'free and open source': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-29T13:15:02Z | 4 | https://doc.mapeditor.org/en/stable/reference/support-for-tmx-maps/ | step-2 link 'game development frameworks': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-29T13:15:03Z | 4 | https://www.mapeditor.org/donate | step-2 link 'Support Tiled Development': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-29T13:15:03Z | 4 | https://github.com/mapeditor/tiled | landing page rendered a README (7843 chars of page text); not used | used: no |

## EV-C003-E1-01

Candidate: C003
Gate: E1
Source:   https://github.com/bjorn/tiled

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C003-E2REP-02

Candidate: C003
Gate: E2-REP
Source:   https://github.com/mapeditor/tiled

Surfaces:  https://www.mapeditor.org/ -> observed
           https://github.com/bjorn/tiled/archive/refs/tags/v1.8.6/ -> closed-by-class (forbidden class, never requested)
           https://github.com/bjorn/tiled -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitHub' at https://www.mapeditor.org/ -> https://github.com/mapeditor/tiled | link label 'GitHub' at https://www.mapeditor.org/ -> https://github.com/mapeditor/tiled | link label 'GitHub' at https://www.mapeditor.org/ -> https://github.com/mapeditor/tiled | identifier 'tiled' (the repository's name, contract 6) appears on https://www.mapeditor.org/ | tree pinned at 83e4cfd9faa653e543e64d1af3b1010f8d5794da (1715 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C003-E2RULE-03 [CORRECTED after review, RQA-40]

Candidate: C003
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           docs/README.md
           docs/index.rst
           docs/scripting-doc/README.md
           man/tiled.1
           man/tiled.1.ronn
           man/tmxrasterizer.1
           man/tmxrasterizer.1.ronn
           man/tmxviewer.1
           man/tmxviewer.1.ronn
           CONTRIBUTING.md
           tests/
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, docs/README.md, docs/index.rst, docs/scripting-doc/README.md, man/tiled.1, man/tiled.1.ronn, man/tmxrasterizer.1, man/tmxrasterizer.1.ronn, man/tmxviewer.1, man/tmxviewer.1.ronn, CONTRIBUTING.md, tests/

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED

## EV-C003-E2RULE-03

[CORRECTED after review, RQA-40: this block quoted `docs/reference/tmx-map-format.rst`, which is not an E2-RULE surface under RQA-39 (its name does not start with "format"); the block below the corrected one is kept as read in batch 1.]

Candidate: C003
Gate: E2-RULE
Source:   docs/reference/tmx-map-format.rst:53

Observed: 'Valid values are ``right-down`` (the default), ``right-up``,'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C003-E3-04

[CORRECTED after review, RQA-40: NOT_REACHED; E2-RULE is UNRESOLVED under RQA-39, so this gate is not evaluated. Kept as read in batch 1.]

Candidate: C003
Gate: E3
Source:   docs/reference/tmx-map-format.rst:80

Observed: 'number is stored to prevent reuse of the same ID after layers have'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C003-E4-05

[CORRECTED after review, RQA-40: NOT_REACHED; E2-RULE is UNRESOLVED under RQA-39, so this gate is not evaluated. Kept as read in batch 1.]

Candidate: C003
Gate: E4
Source:   the frozen grammar over 92 candidate rows

Surfaces:  src/libtiled/propertytype.cpp:419
           src/libtiled/wangset.cpp:391
           src/tiled/wangbrush.cpp:513
           src/tiled/wangfiller.cpp:34
           src/tiled/worldmovemaptool.cpp:57
           src/plugins/python/pythonbind.cpp:375
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.
  [CORRECTED after review, RQA-17: for E4 the lines above are surfaces read under contract Section 8, not starting points]

Observed: catalogue decided 1 rows, 91 undecided, none admitted

Inference: no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 5 -- emulators/advancemame

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.advancemame.it/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/amadvance/advancemame/releases/download/v5.0/ | SITES | release-assets | closed-by-class | release-assets |  |  |

## EV-C004-E1-01

Candidate: C004
Gate: E1
Source:   https://www.advancemame.it

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C004-E2REP-02

Candidate: C004
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.advancemame.it/ -> observed
           https://github.com/amadvance/advancemame/releases/download/v5.0/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 6 -- emulators/dgen-sdl

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://dgen.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/dgen/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-29T13:20:43Z | 6 | http://sourceforge.net/projects/dgen/ | step-2 link 'this project on SourceForge': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-29T13:20:44Z | 6 | http://sourceforge.net/projects/dgen/files/dgen/ | step-2 link 'http://sourceforge.net/projects/dgen/files/dgen/': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-29T13:20:47Z | 6 | https://sourceforge.net/projects/dgen/support | step-2 link 'SourceForge Tracker': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C005-E1-01

Candidate: C005
Gate: E1
Source:   https://dgen.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C005-E2REP-02

Candidate: C005
Gate: E2-REP
Source:   https://sourceforge.net/p/dgen/dgen

Surfaces:  https://dgen.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/dgen/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'https://sourceforge.net/p/dgen/dgen/' at https://dgen.sourceforge.net/ -> https://sourceforge.net/p/dgen/dgen | identifier 'dgen' (the repository's name, contract 6) appears on https://dgen.sourceforge.net/ | tree pinned at a6f61a594b996840110a6c4bc0347a9d8e4f81e7 (190 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C005-E2RULE-03

Candidate: C005
Gate: E2-RULE
Source:   dgen.1:106

Observed: 'XFACT must be a positive'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C005-E3-04

Candidate: C005
Gate: E3
Source:   dgenrc.5:214

Observed: 'This currently has no effect when OpenGL is'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C005-E4-05

Candidate: C005
Gate: E4
Source:   rc.cpp:27 ctv_names

Observed: EN2: rc.cpp:27 'const char *ctv_names[] = {'; EN4: rc.cpp:492 'if(!strcasecmp(value, ctv_names[i])) return i;'; EN4: rc.cpp:1082 '/* If we got a bad value, discard and warn user */'; EN4: rc.cpp:1085 '"rc: %s:%u:%u: invalid value for key"'

Inference: one enumerator admitted under the frozen grammar with a quoted identification and refusal path (contract Section 8)

Decision: PASS


## rank 7 -- emulators/dosbox

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.dosbox.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/dosbox/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C006-E1-01

Candidate: C006
Gate: E1
Source:   https://www.dosbox.com

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C006-E2REP-02

Candidate: C006
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.dosbox.com/ -> observed
           https://downloads.sourceforge.net/sourceforge/dosbox/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 8 -- emulators/dosbox-x

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://dosbox-x.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/joncampbell123/dosbox-x/archive/refs/tags/dosbox-x-v2025.05.03/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/joncampbell123/dosbox-x | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-29T13:07:52Z | 8 | https://dosbox-x.com/newdosdevelopment.html | step-2 link 'aid in new DOS development': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-29T13:07:54Z | 8 | https://github.com/joncampbell123/dosbox-x | landing page rendered a README (30900 chars of page text); not used | used: no |
| 2026-10-29T13:07:51Z | 8 | https://github.com/joncampbell123/dosbox-x/blob/master/BUILD.md | step-2 link 'Source code building instructions' points at a file inside https://github.com/joncampbell123/dosbox-x; the file is not opened, the root is | used: no |
| 2026-10-29T13:07:53Z | 8 | https://dosbox-x.com/devel-build.html | step-2 link 'Development (preview/testing) builds': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-29T13:20:54Z | 8 | http://pages.github.com | step-2 link 'GitHub Pages': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C007-E1-01

Candidate: C007
Gate: E1
Source:   https://github.com/joncampbell123/dosbox-x

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C007-E2REP-02

Candidate: C007
Gate: E2-REP
Source:   https://github.com/joncampbell123/dosbox-x

Surfaces:  https://dosbox-x.com/ -> observed
           https://github.com/joncampbell123/dosbox-x/archive/refs/tags/dosbox-x-v2025.05.03/ -> closed-by-class (forbidden class, never requested)
           https://github.com/joncampbell123/dosbox-x -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'our project website on GitHub' at https://dosbox-x.com/ -> https://github.com/joncampbell123/dosbox-x | link label 'View Project on GitHub' at https://dosbox-x.com/ -> https://github.com/joncampbell123/dosbox-x | link label 'Source code building instructions' at https://dosbox-x.com/ -> https://github.com/joncampbell123/dosbox-x | identifier 'dosbox-x' (the repository's name, contract 6) appears on https://dosbox-x.com/ | tree pinned at 997f616e0886a835fc3660f2b935688f17f20d42 (7833 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C007-E2RULE-03

Candidate: C007
Gate: E2-RULE
Source:   README.debugger:171

Observed: '`STEPIN` is rejected unless the debugger is already stopped in its loop'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C007-E3-04

Candidate: C007
Gate: E3
Source:   README.debugger:171

Observed: 'is rejected unless the debugger is already stopped'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C007-E4-05

Candidate: C007
Gate: E4
Source:   src/hardware/serialport/serialport.cpp:1470 serialTypes

Observed: EN2: src/hardware/serialport/serialport.cpp:1470 'static const char *serialTypes[SERIAL_TYPE_COUNT] = {'; EN4: src/hardware/serialport/serialport.cpp:1545 'if (!strcasecmp(temp_line.c_str(), serialTypes[x])) {'; EN4: src/hardware/serialport/serialport.cpp:1552 'WriteOut("Type must be one of the following:'

Inference: one enumerator admitted under the frozen grammar with a quoted identification and refusal path (contract Section 8)

Decision: PASS
