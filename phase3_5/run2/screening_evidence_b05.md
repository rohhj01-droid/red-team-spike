# Screening batch 05 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b05.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 33 | games/asciiquarium | PASS | C030 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 34 | games/astromenace | PASS | C031 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 35 | games/atomix | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |
| 36 | games/barrage | PASS | C032 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 37 | games/bass | PASS | C033 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 38 | games/bastet | PASS | C034 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 39 | games/batrachians | PASS | C035 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 40 | games/belooted | PASS | C036 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |

## rank 33 -- games/asciiquarium

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.robobunny.com/projects/asciiquarium/html/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://www.robobunny.com/projects/asciiquarium/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-30T04:15:36Z | 33 | https://github.com/rgoring/asciiquarium | landing page rendered a README (3406 chars of page text); not used | used: no |

## EV-C030-E1-01

Candidate: C030
Gate: E1
Source:   https://www.robobunny.com/projects/asciiquarium/html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C030-E2REP-02

Candidate: C030
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.robobunny.com/projects/asciiquarium/html/ -> observed
           https://www.robobunny.com/projects/asciiquarium/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/rgoring/asciiquarium; a label link leads to another work's source: "Russel Goring has updated J. Sommer's Windows screensaver, and has posted the source code on Github." at https://robobunny.com/projects/asciiquarium/html/ -> https://github.com/rgoring/asciiquarium

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 34 -- games/astromenace

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.viewizard.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/viewizard/astromenace/archive/refs/tags/v1.4.3/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/viewizard/astromenace | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T04:15:44Z | 34 | https://github.com/viewizard/astromenace | landing page rendered a README (8951 chars of page text); not used | used: no |

## EV-C031-E1-01

Candidate: C031
Gate: E1
Source:   https://github.com/viewizard/astromenace

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C031-E2REP-02

Candidate: C031
Gate: E2-REP
Source:   https://github.com/viewizard/astromenace

Surfaces:  http://www.viewizard.com/ -> observed
           https://github.com/viewizard/astromenace/archive/refs/tags/v1.4.3/ -> closed-by-class (forbidden class, never requested)
           https://github.com/viewizard/astromenace -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Source Code' at https://viewizard.com/ -> https://github.com/viewizard/astromenace | identifier 'astromenace' (the repository's name, contract 6) appears on https://viewizard.com/ | tree pinned at bbdb3ac5af2774c92b85c4d9b2a238f606911e66 (577 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C031-E2RULE-03

Candidate: C031
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           docs/CONTRIBUTING.md
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, docs/CONTRIBUTING.md

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 35 -- games/atomix

## EV-R035-UR-01

Candidate: (none: rank 35)
Gate: UR
Source:   games/atomix/Makefile

Observed: modules=['textproc/intltool'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED


## rank 36 -- games/barrage

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://lgames.sourceforge.net/?project=Barrage | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/lgames/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C032-E1-01

Candidate: C032
Gate: E1
Source:   https://lgames.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C032-E2REP-02

Candidate: C032
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://lgames.sourceforge.net/?project=Barrage -> observed
           https://downloads.sourceforge.net/sourceforge/lgames/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 37 -- games/bass

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://downloads.sourceforge.net/sourceforge/scummvm/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C033-E1-01

Candidate: C033
Gate: E1
Source:   https://downloads.sourceforge.net/sourceforge

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C033-E2REP-02

Candidate: C033
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://downloads.sourceforge.net/sourceforge/scummvm/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 38 -- games/bastet

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://fph.altervista.org/prog/bastet.html | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/fph/bastet/archive/refs/tags/0.43.2/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/fph/bastet | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T04:16:07Z | 38 | https://github.com/fph/bastet | landing page rendered a README (5191 chars of page text); not used | used: no |

## EV-C034-E1-01

Candidate: C034
Gate: E1
Source:   https://github.com/fph/bastet

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C034-E2REP-02

Candidate: C034
Gate: E2-REP
Source:   https://github.com/fph/bastet

Surfaces:  http://fph.altervista.org/prog/bastet.html -> observed
           https://github.com/fph/bastet/archive/refs/tags/0.43.2/ -> closed-by-class (forbidden class, never requested)
           https://github.com/fph/bastet -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'github' at http://fph.altervista.org/prog/bastet.html -> https://github.com/fph/bastet | identifier 'bastet' (the repository's name, contract 6) appears on http://fph.altervista.org/prog/bastet.html | tree pinned at 1b3e6922c1f7d72e87640ea4a58a52e1d36f01e1 (30 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C034-E2RULE-03

Candidate: C034
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README
           bastet.6
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README, bastet.6

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 39 -- games/batrachians

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://perso.b2b2c.ca/~sarrazip/dev/batrachians.html | HOMEPAGE | unmatched | unreachable |  |  |  |
| http://perso.b2b2c.ca/~sarrazip/dev/ | SITES | unmatched | unreachable |  |  |  |

## EV-C035-E1-01

Candidate: C035
Gate: E1
Source:   https://perso.b2b2c.ca/~sarrazip/dev/batrachians.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C035-E2REP-02

Candidate: C035
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://perso.b2b2c.ca/~sarrazip/dev/batrachians.html -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://perso.b2b2c.ca/~sarrazip/dev/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 40 -- games/belooted

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://gnomefiles.org/content/show.php/Belooted?content=131848 | HOMEPAGE | unmatched | unreachable |  | 526 |  |
| http://boby.joe.free.fr/dev/belooted/files/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |

## EV-C036-E1-01

Candidate: C036
Gate: E1
Source:   https://gnomefiles.org/content/show.php/belooted

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C036-E2REP-02

Candidate: C036
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://gnomefiles.org/content/show.php/Belooted?content=131848 -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://boby.joe.free.fr/dev/belooted/files/ -> observed (HTTP 403)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED
