# Screening batch 07 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b07.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 49 | games/boswars | PASS | C045 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 50 | games/braincurses | PASS | C046 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 51 | games/brogue | PASS | C047 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 52 | games/brumbrumrally | PASS | C048 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 53 | games/bugdom | PASS | C049 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 54 | games/bugdom2 | PASS | C050 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 55 | games/burgerspace | PASS | C051 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 56 | games/bzflag | PASS | C052 | PASS | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | E4 | PI-UNCLASSIFIED-SHAPE |

## rank 49 -- games/boswars

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.boswars.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://www.boswars.org/dist/releases/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |

| 2026-10-30T05:51:06Z | 49 | https://www.boswars.org/development.shtml | step-2 link 'Development': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T05:51:07Z | 49 | https://codeberg.org/boswars/boswars | landing page rendered a README (6757 chars of page text); not used | used: no |
| 2026-10-30T05:51:09Z | 49 | https://savannah.nongnu.org/projects/stratagus-bos/ | step-2 link 'Savannah': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T05:51:09Z | 49 | https://savannah.nongnu.org/projects/stratagus-bos/ | step-2 link 'Savannah Page': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C045-E1-01

Candidate: C045
Gate: E1
Source:   https://www.boswars.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C045-E2REP-02

Candidate: C045
Gate: E2-REP
Source:   https://codeberg.org/boswars/boswars

Surfaces:  https://www.boswars.org/ -> observed
           https://www.boswars.org/dist/releases/ -> observed (HTTP 403)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Codeberg' at https://www.boswars.org/ -> https://codeberg.org/boswars/boswars | identifier 'boswars' (the repository's name, contract 6) appears on https://www.boswars.org/ | tree pinned at e7f81b955486d94e77fb3806d109560775d984d1 (1846 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C045-E2RULE-03

Candidate: C045
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           doc/README-SDL.txt
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, doc/README-SDL.txt

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 50 -- games/braincurses

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/bderrly/braincurses | HOMEPAGE+GH | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/bderrly/braincurses/archive/refs/tags/v1.1.0/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T05:51:46Z | 50 | https://github.com/bderrly/braincurses | landing page rendered a README (4617 chars of page text); not used | used: no |

## EV-C046-E1-01

Candidate: C046
Gate: E1
Source:   https://github.com/bderrly/braincurses

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C046-E2REP-02

Candidate: C046
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/bderrly/braincurses -> observed
           https://github.com/bderrly/braincurses/archive/refs/tags/v1.1.0/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/bderrly/braincurses

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 51 -- games/brogue

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://sites.google.com/site/broguegame/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/tmewett/BrogueCE/archive/refs/tags/v1.15.1/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/tmewett/BrogueCE | GH | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T05:51:48Z | 51 | https://github.com/tmewett/BrogueCE | landing page rendered a README (6943 chars of page text); not used | used: no |

## EV-C047-E1-01

Candidate: C047
Gate: E1
Source:   https://github.com/tmewett/broguece

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C047-E2REP-02

Candidate: C047
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://sites.google.com/site/broguegame/ -> observed
           https://github.com/tmewett/BrogueCE/archive/refs/tags/v1.15.1/ -> closed-by-class (forbidden class, never requested)
           https://github.com/tmewett/BrogueCE -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/tmewett/BrogueCE

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 52 -- games/brumbrumrally

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://dataapa.net/brumbrumrally/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://dataapa.net/brumbrumrally/files/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

## EV-C048-E1-01

Candidate: C048
Gate: E1
Source:   https://dataapa.net/brumbrumrally

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C048-E2REP-02

Candidate: C048
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://dataapa.net/brumbrumrally/ -> observed
           http://dataapa.net/brumbrumrally/files/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 53 -- games/bugdom

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://pangeasoft.net/bug | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/jorio/Bugdom | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/jorio/Pomme | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T05:51:52Z | 53 | https://github.com/jorio/Bugdom | landing page rendered a README (5751 chars of page text); not used | used: no |
| 2026-10-30T05:51:52Z | 53 | https://github.com/jorio/Pomme | landing page rendered a README (5347 chars of page text); not used | used: no |

## EV-C049-E1-01

Candidate: C049
Gate: E1
Source:   https://github.com/jorio/bugdom

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C049-E2REP-02

Candidate: C049
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://pangeasoft.net/bug -> observed
           https://github.com/jorio/Bugdom -> observed
           https://github.com/jorio/Pomme -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/jorio/Bugdom, https://github.com/jorio/Pomme

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 54 -- games/bugdom2

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://pangeasoft.net/bug2 | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/jorio/Bugdom2 | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/jorio/Pomme | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T05:51:55Z | 54 | https://github.com/jorio/Bugdom2 | landing page rendered a README (4475 chars of page text); not used | used: no |
| 2026-10-30T05:51:55Z | 54 | https://github.com/jorio/Pomme | landing page rendered a README (5347 chars of page text); not used | used: no |

## EV-C050-E1-01

Candidate: C050
Gate: E1
Source:   https://github.com/jorio/bugdom2

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C050-E2REP-02

Candidate: C050
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://pangeasoft.net/bug2 -> observed
           https://github.com/jorio/Bugdom2 -> observed
           https://github.com/jorio/Pomme -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/jorio/Bugdom2, https://github.com/jorio/Pomme

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 55 -- games/burgerspace

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://perso.b2b2c.ca/~sarrazip/dev/burgerspace.html | HOMEPAGE | unmatched | unreachable |  |  |  |
| http://perso.b2b2c.ca/~sarrazip/dev/ | SITES | unmatched | unreachable |  |  |  |

## EV-C051-E1-01

Candidate: C051
Gate: E1
Source:   https://perso.b2b2c.ca/~sarrazip/dev/burgerspace.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C051-E2REP-02

Candidate: C051
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://perso.b2b2c.ca/~sarrazip/dev/burgerspace.html -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           http://perso.b2b2c.ca/~sarrazip/dev/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 56 -- games/bzflag

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.bzflag.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://download.bzflag.org/bzflag/source/2.4.22/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-30T05:51:58Z | 56 | https://download.bzflag.org/bzflag/source/2.4.30/bzflag-2.4.30.tar.bz2 | step-2 link 'Download for Source (.tar.bz2) .tar.bz2': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T05:52:04Z | 56 | https://download.bzflag.org/bzflag/source/2.4.30/bzflag-2.4.30.tar.gz | step-2 link 'Download for Source (.tar.gz) .tar.gz': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T05:52:21Z | 56 | https://download.bzflag.org/bzflag/source/2.4.30/bzflag-2.4.30.zip | step-2 link 'Download for Source (.zip) .zip': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T05:53:21Z | 56 | https://github.com/BZFlag-Dev/bzflag | landing page rendered a README (19631 chars of page text); not used | used: no |

## EV-C052-E1-01

Candidate: C052
Gate: E1
Source:   https://www.bzflag.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C052-E2REP-02

Candidate: C052
Gate: E2-REP
Source:   https://github.com/BZFlag-Dev/bzflag

Surfaces:  https://www.bzflag.org/ -> observed
           https://download.bzflag.org/bzflag/source/2.4.22/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitHub' at https://www.bzflag.org/ -> https://github.com/BZFlag-Dev/bzflag | identifier 'bzflag' (the repository's name, contract 6) appears on https://download.bzflag.org/bzflag/source/2.4.22/ | tree pinned at 0946efd9e405aa6e708341f6d0a7b8c187f5a4ad (1288 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C052-E2RULE-03

Candidate: C052
Gate: E2-RULE
Source:   README:332

Observed: 'be listed on the public list server must provide an authentication key'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C052-E3-04

Candidate: C052
Gate: E3
Source:   README:332

Observed: 'be listed on the public list server must provide an authentication key'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C052-E4-05

Candidate: C052
Gate: E4
Source:   the frozen grammar over 12 candidate rows

Surfaces:  tools/TextTool2/TextTool2.cpp:30
           AUTHORS:21
           DEVINFO:70
           DEVINFO:308
           README:113
           README:120
           README:180
           misc/multilingualSwearList.txt:1482
           plugins/autoFlagReset/README.autoFlagReset.txt:7
           plugins/bzfscron/README.bzfscron.txt:53
           plugins/chathistory/README.chathistory.txt:1
           plugins/wwzones/README.wwzones.txt:55
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: catalogue decided 0 rows, 12 undecided, none admitted

Inference: no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED
