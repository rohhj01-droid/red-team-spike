# Screening batch 03 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b03.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | games/2048-cli | PASS | C016 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 18 | games/2048-qt | PASS | C017 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 19 | games/abuse | PASS | C018 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 20 | games/ace | PASS | C019 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 21 | games/afternoonstalker | DUPLICATE | NONE | - | - | - | - | - | DUPLICATE | UR | NONE |
| 22 | games/alephone/alephone | PASS | C020 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 23 | games/alephone/weland | PASS | C021 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 24 | games/allegro | PASS | C022 | PASS | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | REJECTED | E2-REP | E2REP-NO-SINGLE-CANONICAL-LOCATION |

## rank 17 -- games/2048-cli

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/tiehuis/2048-cli | HOMEPAGE+GH | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/tiehuis/2048-cli/archive/refs/tags/v0.9.1/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T02:04:17Z | 17 | https://github.com/tiehuis/2048-cli | landing page rendered a README (4884 chars of page text); not used | used: no |

## EV-C016-E1-01

Candidate: C016
Gate: E1
Source:   https://github.com/tiehuis/2048-cli

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C016-E2REP-02

Candidate: C016
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/tiehuis/2048-cli -> observed
           https://github.com/tiehuis/2048-cli/archive/refs/tags/v0.9.1/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/tiehuis/2048-cli

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 18 -- games/2048-qt

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/OpenOrphanage/2048-Qt | HOMEPAGE+DIST_TUPLE | repository-root | observed | repository-root | 404 | admitted-starting-point |

## EV-C017-E1-01

Candidate: C017
Gate: E1
Source:   https://github.com/openorphanage/2048-qt

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C017-E2REP-02

Candidate: C017
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/OpenOrphanage/2048-Qt -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 19 -- games/abuse

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://abuse.zoy.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://abuse.zoy.org/raw-attachment/wiki/download/ | SITES | unmatched | observed | project-page | 200 | admitted-starting-point |
| http://www.linklevel.net/distfiles/ | SITES.sfx | unmatched | observed | distfile-location | 200 | distfile-location |

| 2026-10-30T02:04:21Z | 19 | http://abuse.zoy.org/wiki/dev | step-2 link 'Development…': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:21Z | 19 | http://abuse.zoy.org/wiki/dev | step-2 link 'development page': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C018-E1-01

Candidate: C018
Gate: E1
Source:   https://abuse.zoy.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C018-E2REP-02

Candidate: C018
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://abuse.zoy.org/ -> observed
           http://abuse.zoy.org/raw-attachment/wiki/download/ -> observed
           http://www.linklevel.net/distfiles/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 20 -- games/ace

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.delorie.com/store/ace/ | HOMEPAGE+SITES | unmatched | observed | project-page | 200 | official-project-page |

| 2026-10-30T02:04:25Z | 20 | https://www.delorie.com/store/ace/ace-src.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T02:04:27Z | 20 | https://www.delorie.com/store/ace/ace-1.4.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T02:04:30Z | 20 | https://www.delorie.com/store/ace/ace-1.3.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T02:04:34Z | 20 | https://www.delorie.com/store/ace/ace-1.2.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T02:04:36Z | 20 | https://www.delorie.com/store/ace/ace-1.1.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T02:04:38Z | 20 | https://www.delorie.com/store/ace/ace-1.0.tar.gz | step-2 link 'source': target is not a repository root (distfile-location); observed once, not read | used: no |

## EV-C019-E1-01

Candidate: C019
Gate: E1
Source:   https://www.delorie.com/store/ace

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C019-E2REP-02

Candidate: C019
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.delorie.com/store/ace/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 21 -- games/afternoonstalker

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html | HOMEPAGE | unmatched | not-reached |  |  |  |
| http://perso.b2b2c.ca/~sarrazip/dev/ | SITES | unmatched | not-reached |  |  |  |

## EV-R021-UR-01

Candidate: (none: rank 21)
Gate: UR
Source:   games/afternoonstalker/Makefile

Observed: identity key https://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html

Inference: the same upstream as C001 (contract Section 3)

Decision: DUPLICATE


## rank 22 -- games/alephone/alephone

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://alephone.lhowon.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/Aleph-One-Marathon/alephone/releases/download/release-20250829/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T02:04:42Z | 22 | https://github.com/Aleph-One-Marathon/alephone | landing page rendered a README (8138 chars of page text); not used | used: no |
| 2026-10-30T02:04:41Z | 22 | https://github.com/Aleph-One-Marathon/alephone/releases/download/release-20260930/AlephOne-20260930.tar.bz2 | step-2 link 'source code' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:04:43Z | 22 | https://aleph-one-marathon.github.io/ | step-2 link 'aleph-one-marathon.github.io': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C020-E1-01

Candidate: C020
Gate: E1
Source:   https://alephone.lhowon.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C020-E2REP-02

Candidate: C020
Gate: E2-REP
Source:   https://github.com/Aleph-One-Marathon/alephone

Surfaces:  https://alephone.lhowon.org/ -> observed
           https://github.com/Aleph-One-Marathon/alephone/releases/download/release-20250829/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitHub' at https://alephone.lhowon.org/ -> https://github.com/Aleph-One-Marathon/alephone | identifier 'alephone' (the repository's name, contract 6) appears on https://alephone.lhowon.org/ | tree pinned at 793e4322e5cd5cf7b9eb0147399514e6ebe25328 (986 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C020-E2RULE-03

Candidate: C020
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           docs/README.txt
           docs/alephone.6
           CONTRIBUTING.md
           tests/
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, docs/README.txt, docs/alephone.6, CONTRIBUTING.md, tests/

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 23 -- games/alephone/weland

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://sourceforge.net/projects/weland/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/weland/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T02:04:52Z | 23 | https://sourceforge.net/directory/ | step-2 link 'Open Source Software': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:53Z | 23 | https://sourceforge.net/articles/category/sourceforge-podcast/ | step-2 link 'SourceForge Podcast': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:56Z | 23 | https://x.com/share?url=https://sourceforge.net/projects/weland/&text=Download%20Weland%20on%20SourceForge%20for%20free%21%20 | step-2 link 'Share Weland on SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:56Z | 23 | https://www.facebook.com/sharer/sharer.php?u=https://sourceforge.net/projects/weland/&title=Weland%20on%20SourceForge | step-2 link 'Share Weland on SourceForge on facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:57Z | 23 | https://www.linkedin.com/shareArticle?mini=true&url=https://sourceforge.net/projects/weland/&title=Weland%20on%20SourceForge&source=SourceForge.net | step-2 link 'Share Weland on SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:58Z | 23 | https://www.google.com/preferences/source?q=sourceforge.net | step-2 link 'Add to Preferred Sources': target is not a repository root (unclassifiable); observed once, not read | used: no |
| 2026-10-30T02:04:58Z | 23 | https://sourceforge.net/top | step-2 link 'Top Downloaded Projects': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:59Z | 23 | https://sourceforge.net/about/leadership | step-2 link 'Team': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:04:59Z | 23 | https://x.com/sourceforge | step-2 link 'SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:05:00Z | 23 | https://fosstodon.org/@sourceforge | step-2 link 'SourceForge on Mastodon': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:05:01Z | 23 | https://www.facebook.com/sourceforgenet/ | step-2 link 'SourceForge on Facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:05:02Z | 23 | https://www.linkedin.com/company/sourceforge.net | step-2 link 'SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:05:03Z | 23 | https://sourceforge.net/reviews | step-2 link 'SourceForge Reviews': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C021-E1-01

Candidate: C021
Gate: E1
Source:   https://sourceforge.net/projects/weland

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C021-E2REP-02

Candidate: C021
Gate: E2-REP
Source:   https://sourceforge.net/p/weland/code

Surfaces:  https://sourceforge.net/projects/weland/ -> observed
           https://downloads.sourceforge.net/sourceforge/weland/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: designated and observed, but the pin could not be taken: Command '['git', 'ls-remote', '--symref', 'https://git.code.sf.net/p/weland/code', 'HEAD']' returned non-zero exit status 128.

Inference: a designated repository that git cannot fetch is a shape no sealed criterion describes (contract Section 7)

Decision: UNRESOLVED


## rank 24 -- games/allegro

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://liballeg.org/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/alleg/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T02:05:06Z | 24 | https://github.com/liballeg/allegro5 | landing page rendered a README (10686 chars of page text); not used | used: no |
| 2026-10-30T02:05:07Z | 24 | https://github.com/liballeg | step-2 link 'GitHub project': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.11.3/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.11.2/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.11.1/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.11.0/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:07Z | 24 | https://github.com/liballeg/allegro4 | landing page rendered a README (3078 chars of page text); not used | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.10.1/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.10.0/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.9.1/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:05Z | 24 | https://github.com/liballeg/allegro5/releases/5.2.9.0/ | step-2 link 'GitHub' leads to a forbidden class; not followed | used: no |
| 2026-10-30T02:05:08Z | 24 | https://github.com/dradtke/go-allegro | landing page rendered a README (5861 chars of page text); not used | used: no |

## EV-C022-E1-01

Candidate: C022
Gate: E1
Source:   https://liballeg.org

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C022-E2REP-02

Candidate: C022
Gate: E2-REP
Source:   https://github.com/liballeg/allegro4; https://github.com/liballeg/allegro5; https://liballeg.org/

Surfaces:  http://liballeg.org/ -> observed
           https://downloads.sourceforge.net/sourceforge/alleg/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: 'We have moved our official GIT repository over to GitHub.' at https://liballeg.org/ -> https://github.com/liballeg/allegro5 | 'The official Allegro 5 git repository.' at https://github.com/liballeg/allegro5 -> https://github.com/liballeg/allegro5 | 'The official Allegro 4 git repository.' at https://github.com/liballeg/allegro4 -> https://github.com/liballeg/allegro4 | 'Git repository' at https://liballeg.org/ -> https://github.com/liballeg/allegro5 | 'own repository' at https://liballeg.org/ -> https://github.com/liballeg/allegro4

Inference: two designations name different locations and neither marks a mirror (contract Section 7)

Decision: FAIL
