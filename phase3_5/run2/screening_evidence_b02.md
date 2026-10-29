# Screening batch 02 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b02.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9 | emulators/fceux | PASS | C008 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 10 | emulators/flycast | PASS | C009 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 11 | emulators/frodo | PASS | C010 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 12 | emulators/libchdr | PASS | C011 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 13 | emulators/mednafen | PASS | C012 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 14 | emulators/snes9x | PASS | C013 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 15 | emulators/virtualjaguar | PASS | C014 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 16 | games/1oom | PASS | C015 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |

## rank 9 -- emulators/fceux

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://fceux.com/web/home.html | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/TASEmulators/fceux/archive/refs/tags/v2.6.6/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/TASEmulators/fceux | GH | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-29T18:33:52Z | 9 | https://github.com/TASEmulators/fceux | landing page rendered a README (4252 chars of page text); not used | used: no |

## EV-C008-E1-01

Candidate: C008
Gate: E1
Source:   https://github.com/tasemulators/fceux

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C008-E2REP-02

Candidate: C008
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://fceux.com/web/home.html -> observed
           https://github.com/TASEmulators/fceux/archive/refs/tags/v2.6.6/ -> closed-by-class (forbidden class, never requested)
           https://github.com/TASEmulators/fceux -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/TASEmulators/fceux

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 10 -- emulators/flycast

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/flyinghead/flycast | HOMEPAGE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://messagemode2.com/source/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-29T18:33:54Z | 10 | https://github.com/flyinghead/flycast | landing page rendered a README (5533 chars of page text); not used | used: no |

## EV-C009-E1-01

Candidate: C009
Gate: E1
Source:   https://github.com/flyinghead/flycast

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C009-E2REP-02

Candidate: C009
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/flyinghead/flycast -> observed
           https://messagemode2.com/source/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/flyinghead/flycast

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 11 -- emulators/frodo

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://frodo.cebix.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://frodo.cebix.net/downloads/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |
| ftp://sunsite.unc.edu/pub/micro/commodore/crossplatform/emulators/unix/ | SITES | unmatched | unreachable |  |  |  |

| 2026-10-29T18:34:05Z | 11 | http://frodo.cebix.net/downloads/Frodo-4.5.tar.gz | step-2 link 'Download Frodo V4.5 source distribution': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-29T18:34:07Z | 11 | https://github.com/cebix/frodo4 | landing page rendered a README (12395 chars of page text); not used | used: no |
| 2026-10-29T18:34:05Z | 11 | https://github.com/cebix/frodo4/zipball/master | step-2 link 'Download the most current source code as a zip file' leads to a forbidden class; not followed | used: no |
| 2026-10-29T18:34:09Z | 11 | http://frodo.cebix.net/downloads/FrodoV4_1b.Src.tar.gz | step-2 link 'Download Frodo V4.1b source distribution': target is not a repository root (distfile-location); observed once, not read | used: no |

## EV-C010-E1-01

Candidate: C010
Gate: E1
Source:   https://frodo.cebix.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C010-E2REP-02

Candidate: C010
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://frodo.cebix.net/ -> observed
           http://frodo.cebix.net/downloads/ -> observed (HTTP 403)
           ftp://sunsite.unc.edu/pub/micro/commodore/crossplatform/emulators/unix/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Main page of the GitHub repository' at http://frodo.cebix.net/ -> https://github.com/cebix/frodo4 | not observed: ftp://sunsite.unc.edu/pub/micro/commodore/crossplatform/emulators/unix/ (unreachable)

Inference: a PASS needs every admitted starting point not closed-by-class observed; an unobserved one leaves "exactly one" undecided (contract Section 7; Run 1 QA-41) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 12 -- emulators/libchdr

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/rtissera/libchdr | HOMEPAGE+GH | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/rtissera/libchdr/archive/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-29T18:34:14Z | 12 | https://github.com/rtissera/libchdr | landing page rendered a README (3658 chars of page text); not used | used: no |

## EV-C011-E1-01

Candidate: C011
Gate: E1
Source:   https://github.com/rtissera/libchdr

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C011-E2REP-02

Candidate: C011
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/rtissera/libchdr -> observed
           https://github.com/rtissera/libchdr/archive/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/rtissera/libchdr

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 13 -- emulators/mednafen

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://mednafen.github.io | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://mednafen.github.io/releases/files/ | SITES | unmatched | observed | distfile-location | 404 | distfile-location |

## EV-C012-E1-01

Candidate: C012
Gate: E1
Source:   https://mednafen.github.io

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C012-E2REP-02

Candidate: C012
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://mednafen.github.io -> observed
           https://mednafen.github.io/releases/files/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 14 -- emulators/snes9x

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.snes9x.com/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/snes9xgit/snes9x/archive/refs/tags/1.63/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/snes9xgit/snes9x | GH | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-29T18:34:17Z | 14 | https://github.com/snes9xgit/snes9x | landing page rendered a README (5375 chars of page text); not used | used: no |

## EV-C013-E1-01

Candidate: C013
Gate: E1
Source:   https://github.com/snes9xgit/snes9x

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C013-E2REP-02

Candidate: C013
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.snes9x.com/ -> observed
           https://github.com/snes9xgit/snes9x/archive/refs/tags/1.63/ -> closed-by-class (forbidden class, never requested)
           https://github.com/snes9xgit/snes9x -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/snes9xgit/snes9x

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 15 -- emulators/virtualjaguar

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://icculus.org/virtualjaguar/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://icculus.org/virtualjaguar/tarballs/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-29T18:34:19Z | 15 | https://icculus.org/virtualjaguar/tarballs/virtualjaguar-2.1.2.tar.bz2 | step-2 link 'Linux (source only*)': target is not a repository root (distfile-location); observed once, not read | used: no |

## EV-C014-E1-01

Candidate: C014
Gate: E1
Source:   https://icculus.org/virtualjaguar

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C014-E2REP-02

Candidate: C014
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://icculus.org/virtualjaguar/ -> observed
           https://icculus.org/virtualjaguar/tarballs/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 16 -- games/1oom

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://kilgoretroutmaskreplicant.gitlab.io/plain-html/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://gitlab.com/KilgoreTroutMaskReplicant/1oom/uploads/13d2d645650929c6f7f08be356b62f66/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-29T18:34:23Z | 16 | https://gitlab.com/KilgoreTroutMaskReplicant/1oom | landing page rendered a README (356 chars of page text); not used | used: no |

## EV-C015-E1-01

Candidate: C015
Gate: E1
Source:   https://kilgoretroutmaskreplicant.gitlab.io/plain-html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C015-E2REP-02

Candidate: C015
Gate: E2-REP
Source:   https://gitlab.com/KilgoreTroutMaskReplicant/1oom

Surfaces:  https://kilgoretroutmaskreplicant.gitlab.io/plain-html/ -> observed
           https://gitlab.com/KilgoreTroutMaskReplicant/1oom/uploads/13d2d645650929c6f7f08be356b62f66/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitLab' at https://kilgoretroutmaskreplicant.gitlab.io/plain-html/ -> https://gitlab.com/KilgoreTroutMaskReplicant/1oom | identifier '1oom' (the repository's name, contract 6) appears on https://kilgoretroutmaskreplicant.gitlab.io/plain-html/ | tree pinned at dedf0bbd57fe004e5d49c2b63c98a219cc1b906e (377 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C015-E2RULE-03

Candidate: C015
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README
           doc/format_gam.txt
           doc/format_lbx.txt
           doc/format_moo.txt
           doc/format_pbx.txt
           doc/format_save.txt
           HACKING
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README, doc/format_gam.txt, doc/format_lbx.txt, doc/format_moo.txt, doc/format_pbx.txt, doc/format_save.txt, HACKING

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED
