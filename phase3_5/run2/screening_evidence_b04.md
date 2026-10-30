# Screening batch 04 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b04.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | games/amnesia-tdd | PASS | C023 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 26 | games/amoebax | PASS | C024 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 27 | games/amph | PASS | C025 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 28 | games/an | PASS | C026 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 29 | games/angband | PASS | C027 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 30 | games/angrydd | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |
| 31 | games/armagetronad | PASS | C028 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 32 | games/arx-libertatis | PASS | C029 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |

## rank 25 -- games/amnesia-tdd

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.amnesiagame.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/shamazmazum/AmnesiaTheDarkDescent/archive/refs/tags/v0.3.2/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/shamazmazum/AmnesiaTheDarkDescent | GH | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T04:01:43Z | 25 | http://frictionalgames.blogspot.com | step-2 link 'Dev Blog': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:01:46Z | 25 | https://github.com/shamazmazum/AmnesiaTheDarkDescent | landing page rendered a README (4489 chars of page text); not used | used: no |

## EV-C023-E1-01

Candidate: C023
Gate: E1
Source:   https://github.com/shamazmazum/amnesiathedarkdescent

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C023-E2REP-02

Candidate: C023
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.amnesiagame.com/ -> observed
           https://github.com/shamazmazum/AmnesiaTheDarkDescent/archive/refs/tags/v0.3.2/ -> closed-by-class (forbidden class, never requested)
           https://github.com/shamazmazum/AmnesiaTheDarkDescent -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/shamazmazum/AmnesiaTheDarkDescent

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 26 -- games/amoebax

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.emma-soft.com/games/amoebax/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://www.emma-soft.com/games/amoebax/download/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |

## EV-C024-E1-01

Candidate: C024
Gate: E1
Source:   https://www.emma-soft.com/games/amoebax

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C024-E2REP-02

Candidate: C024
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.emma-soft.com/games/amoebax/ -> observed
           http://www.emma-soft.com/games/amoebax/download/ -> observed (HTTP 403)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 27 -- games/amph

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://n.ethz.ch/student/loehrerl/amph/amph.html | HOMEPAGE | unmatched | unreachable |  |  |  |
| http://n.ethz.ch/student/loehrerl/amph/files/ | SITES | unmatched | unreachable |  |  |  |

## EV-C025-E1-01

Candidate: C025
Gate: E1
Source:   https://n.ethz.ch/student/loehrerl/amph/amph.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C025-E2REP-02

Candidate: C025
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://n.ethz.ch/student/loehrerl/amph/amph.html -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://n.ethz.ch/student/loehrerl/amph/files/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 28 -- games/an

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://salsa.debian.org/pm/an | HOMEPAGE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://deb.debian.org/debian/pool/main/a/an/ | SITES | distfile-location | observed | distfile-location | 200 | distfile-location |
| http://ftp.debian.org/debian/pool/main/a/an/ | SITES | distfile-location | observed | distfile-location | 200 | distfile-location |
| http://ftp.au.debian.org/debian/pool/main/a/an/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| http://ftp.de.debian.org/debian/pool/main/a/an/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| http://ftp.fr.debian.org/debian/pool/main/a/an/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| http://ftp.nl.debian.org/debian/pool/main/a/an/ | SITES | unmatched | observed | project-page | 200 | admitted-starting-point |
| http://ftp.uk.debian.org/debian/pool/main/a/an/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |
| http://ftp.us.debian.org/debian/pool/main/a/an/ | SITES | unmatched | observed | project-page | 200 | admitted-starting-point |

## EV-C026-E1-01

Candidate: C026
Gate: E1
Source:   https://salsa.debian.org/pm/an

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C026-E2REP-02

Candidate: C026
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://salsa.debian.org/pm/an -> observed
           https://deb.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.au.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.de.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.fr.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.nl.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.uk.debian.org/debian/pool/main/a/an/ -> observed
           http://ftp.us.debian.org/debian/pool/main/a/an/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://salsa.debian.org/pm/an

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 29 -- games/angband

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://rephial.org | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/angband/angband/releases/download/4.2.5/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T04:01:58Z | 29 | https://github.com/angband/angband/releases/download/4.2.6/Angband-4.2.6.tar.gz | step-2 link 'Source code' leads to a forbidden class; not followed | used: no |

## EV-C027-E1-01

Candidate: C027
Gate: E1
Source:   https://rephial.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C027-E2REP-02

Candidate: C027
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://rephial.org -> observed
           https://github.com/angband/angband/releases/download/4.2.5/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 30 -- games/angrydd

## EV-R030-UR-01

Candidate: (none: rank 30)
Gate: UR
Source:   games/angrydd/Makefile

Observed: modules=['lang/python'] unresolved=[]

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED


## rank 31 -- games/armagetronad

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://armagetronad.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/armagetronad/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T04:02:02Z | 31 | https://download.armagetronad.org/docs/flatpak/ | step-2 link 'our own repository': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C028-E1-01

Candidate: C028
Gate: E1
Source:   https://armagetronad.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C028-E2REP-02

Candidate: C028
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://armagetronad.org/ -> observed
           https://downloads.sourceforge.net/sourceforge/armagetronad/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 32 -- games/arx-libertatis

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/arx/ArxLibertatis | HOMEPAGE+GH | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/arx/ArxLibertatis/archive/refs/tags/1.2.1/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T04:02:04Z | 32 | https://github.com/arx/ArxLibertatis | landing page rendered a README (13214 chars of page text); not used | used: no |

## EV-C029-E1-01

Candidate: C029
Gate: E1
Source:   https://github.com/arx/arxlibertatis

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C029-E2REP-02

Candidate: C029
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/arx/ArxLibertatis -> observed
           https://github.com/arx/ArxLibertatis/archive/refs/tags/1.2.1/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/arx/ArxLibertatis

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED
