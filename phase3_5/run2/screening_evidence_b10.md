# Screening batch 10 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b10.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 73 | games/clines | PASS | C066 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 74 | games/clonekeen | PASS | C067 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 75 | games/cmatrix | PASS | C068 | PASS | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | E4 | PI-UNCLASSIFIED-SHAPE |
| 76 | games/colobot/data | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |
| 77 | games/corewars | PASS | C069 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 78 | games/corsixth | PASS | C070 | PASS | PASS | PASS | UNRESOLVED | NOT_REACHED | UNRESOLVED | E3 | PI-UNCLASSIFIED-SHAPE |
| 79 | games/cosmosmash | PASS | C071 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 80 | games/cowsay | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |

## rank 73 -- games/clines

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://manticore.2y.net/prj/clines-a.html | HOMEPAGE | unmatched | unreachable |  |  |  |
| http://manticore.2y.net/cgi-bin/dlwct.sh?f=clines/ | SITES | unmatched | unreachable |  |  |  |

## EV-C066-E1-01

Candidate: C066
Gate: E1
Source:   https://manticore.2y.net/prj/clines-a.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C066-E2REP-02

Candidate: C066
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://manticore.2y.net/prj/clines-a.html -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://manticore.2y.net/cgi-bin/dlwct.sh?f=clines/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 74 -- games/clonekeen

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://clonekeen.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/clonekeen/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T06:42:33Z | 74 | https://clonekeen.sourceforge.net/index.html@nav=download | step-2 link 'source code': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C067-E1-01

Candidate: C067
Gate: E1
Source:   https://clonekeen.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C067-E2REP-02

Candidate: C067
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://clonekeen.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/clonekeen/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 75 -- games/cmatrix

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.asty.org/cmatrix/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://www.asty.org/cmatrix//dist/ | SITES | unmatched | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T06:42:37Z | 75 | https://github.com/abishekvashok/cmatrix | landing page rendered a README (7660 chars of page text); not used | used: no |
| 2026-10-30T06:42:37Z | 75 | http://www.sourceforge.net/ | step-2 link 'SourceForge': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:42:38Z | 75 | http://sourceforge.net/project/?group_id=4055 | step-2 link 'http://sourceforge.net/project/?group_id=4055': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C068-E1-01

Candidate: C068
Gate: E1
Source:   https://www.asty.org/cmatrix

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C068-E2REP-02

Candidate: C068
Gate: E2-REP
Source:   https://github.com/abishekvashok/cmatrix

Surfaces:  http://www.asty.org/cmatrix/ -> observed
           http://www.asty.org/cmatrix//dist/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'https://github.com/abishekvashok/cmatrix' at https://www.asty.org/cmatrix/ -> https://github.com/abishekvashok/cmatrix | identifier 'cmatrix' (the repository's name, contract 6) appears on https://www.asty.org/cmatrix/ | tree pinned at 5c082c64a1296859a11bee60c8c086655953a416 (28 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C068-E2RULE-03

Candidate: C068
Gate: E2-RULE
Source:   cmatrix.1:64

Observed: 'Valid colors are green, red, blue, white, yellow, cyan, magenta and black.'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C068-E3-04

Candidate: C068
Gate: E3
Source:   cmatrix.1:33

Observed: 'Locks cmatrix, Unable to quit'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C068-E4-05

Candidate: C068
Gate: E4
Source:   the frozen grammar over 10 candidate rows

Surfaces:  CODE_OF_CONDUCT.md:37
           CONTRIBUTING.md:77
           COPYING:84
           COPYING:156
           COPYING:197
           COPYING:257
           COPYING:487
           COPYING:614
           INSTALL:50
           INSTALL:65
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: catalogue decided 0 rows, 10 undecided, none admitted

Inference: no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 76 -- games/colobot/data

## EV-R076-UR-01

Candidate: (none: rank 76)
Gate: UR
Source:   games/colobot/data/Makefile

Observed: modules=['devel/cmake', 'lang/python'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED


## rank 77 -- games/corewars

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://corewars.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/corewars/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C069-E1-01

Candidate: C069
Gate: E1
Source:   https://corewars.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C069-E2REP-02

Candidate: C069
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://corewars.org/ -> observed
           https://downloads.sourceforge.net/sourceforge/corewars/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 78 -- games/corsixth

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://corsixth.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/CorsixTH/CorsixTH/archive/refs/tags/v0.69.2/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/CorsixTH/CorsixTH | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T06:42:43Z | 78 | https://github.com/CorsixTH/CorsixTH | landing page rendered a README (7859 chars of page text); not used | used: no |

## EV-C070-E1-01

Candidate: C070
Gate: E1
Source:   https://github.com/corsixth/corsixth

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C070-E2REP-02

Candidate: C070
Gate: E2-REP
Source:   https://github.com/CorsixTH/CorsixTH

Surfaces:  https://corsixth.com/ -> observed
           https://github.com/CorsixTH/CorsixTH/archive/refs/tags/v0.69.2/ -> closed-by-class (forbidden class, never requested)
           https://github.com/CorsixTH/CorsixTH -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Source code' at https://corsixth.com/ -> https://github.com/CorsixTH/CorsixTH | identifier 'CorsixTH' (the repository's name, contract 6) appears on https://corsixth.com/ | tree pinned at 9bf665ac2a985c1c643c45cec93aa2b7e7edb1df (657 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C070-E2RULE-03

Candidate: C070
Gate: E2-RULE
Source:   CorsixTH/corsix-th.6:74

Observed: 'must include the .sav extension.'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C070-E3-04

Candidate: C070
Gate: E3
Source:   the contract's E3 surfaces

Surfaces:  README.md
           README.txt
           CorsixTH/corsix-th.6
           CONTRIBUTING.md
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no stateful witness quoted; surfaces read: README.md, README.txt, CorsixTH/corsix-th.6, CONTRIBUTING.md

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 79 -- games/cosmosmash

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://perso.b2b2c.ca/~sarrazip/dev/cosmosmash.html | HOMEPAGE | unmatched | unreachable |  |  |  |
| http://perso.b2b2c.ca/~sarrazip/dev/ | SITES | unmatched | unreachable |  |  |  |

## EV-C071-E1-01

Candidate: C071
Gate: E1
Source:   https://perso.b2b2c.ca/~sarrazip/dev/cosmosmash.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C071-E2REP-02

Candidate: C071
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://perso.b2b2c.ca/~sarrazip/dev/cosmosmash.html -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://perso.b2b2c.ca/~sarrazip/dev/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 80 -- games/cowsay

## EV-R080-UR-01

Candidate: (none: rank 80)
Gate: UR
Source:   games/cowsay/Makefile

Observed: modules=['cpan'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED
