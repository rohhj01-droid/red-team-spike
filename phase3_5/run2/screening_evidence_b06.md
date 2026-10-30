# Screening batch 06 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b06.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 41 | games/beret | PASS | C037 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-TRANSPORT-INDETERMINATE |
| 42 | games/billyfrontier | PASS | C038 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 43 | games/blobby | PASS | C039 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 44 | games/blobwars | PASS | C040 | PASS | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | E4 | PI-UNCLASSIFIED-SHAPE |
| 45 | games/blockgame | PASS | C041 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 46 | games/blockrage | PASS | C042 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 47 | games/bluemoon | PASS | C043 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 48 | games/bomberclone | PASS | C044 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |

## rank 41 -- games/beret

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://kiwisauce.com/beret/ | HOMEPAGE | unmatched | unreachable |  |  |  |
| https://mirrors.nycbug.org/pub/distfiles/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

## EV-C037-E1-01

Candidate: C037
Gate: E1
Source:   https://kiwisauce.com/beret

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C037-E2REP-02

Candidate: C037
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://kiwisauce.com/beret/ -> unreachable (PI-TRANSPORT-INDETERMINATE after two retries)
           https://mirrors.nycbug.org/pub/distfiles/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-TRANSPORT-INDETERMINATE

Decision: UNRESOLVED


## rank 42 -- games/billyfrontier

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://pangeasoft.net/billy | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/jorio/BillyFrontier | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/jorio/Pomme | DIST_TUPLE | repository-root | observed | repository-root | 200 | admitted-starting-point |

| 2026-10-30T04:36:15Z | 42 | https://github.com/jorio/BillyFrontier | landing page rendered a README (5246 chars of page text); not used | used: no |
| 2026-10-30T04:36:16Z | 42 | https://github.com/jorio/Pomme | landing page rendered a README (5347 chars of page text); not used | used: no |

## EV-C038-E1-01

Candidate: C038
Gate: E1
Source:   https://github.com/jorio/billyfrontier

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C038-E2REP-02

Candidate: C038
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://pangeasoft.net/billy -> observed
           https://github.com/jorio/BillyFrontier -> observed
           https://github.com/jorio/Pomme -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/jorio/BillyFrontier, https://github.com/jorio/Pomme

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 43 -- games/blobby

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://blobbyvolley.de/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/danielknobe/blobbyvolley2/archive/refs/tags/v1.1.1/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/danielknobe/blobbyvolley2 | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T04:28:50Z | 43 | https://github.com/danielknobe/blobbyvolley2 | landing page rendered a README (5094 chars of page text); not used | used: no |
| 2026-10-30T04:28:51Z | 43 | http://sourceforge.net/projects/blobby/ | step-2 link 'Sourceforge': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C039-E1-01

Candidate: C039
Gate: E1
Source:   https://github.com/danielknobe/blobbyvolley2

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C039-E2REP-02

Candidate: C039
Gate: E2-REP
Source:   https://github.com/danielknobe/blobbyvolley2

Surfaces:  https://blobbyvolley.de/ -> observed
           https://github.com/danielknobe/blobbyvolley2/archive/refs/tags/v1.1.1/ -> closed-by-class (forbidden class, never requested)
           https://github.com/danielknobe/blobbyvolley2 -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Github' at https://blobbyvolley.de/ -> https://github.com/danielknobe/blobbyvolley2 | link label 'GitHub' at https://blobbyvolley.de/ -> https://github.com/danielknobe/blobbyvolley2 | identifier 'blobbyvolley2' (the repository's name, contract 6) appears on https://github.com/danielknobe/blobbyvolley2 | tree pinned at c28c5fa87872b7592f34f5f86196e93d127b6cf9 (439 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C039-E2RULE-03

Candidate: C039
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           test/
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, test/

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 44 -- games/blobwars

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://sourceforge.net/projects/blobwars/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/blobwars/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T04:28:58Z | 44 | https://sourceforge.net/directory/ | step-2 link 'Open Source Software': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:29:00Z | 44 | https://sourceforge.net/articles/category/sourceforge-podcast/ | step-2 link 'SourceForge Podcast': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:29:02Z | 44 | https://sourceforge.net/projects/blobwars/files/latest/download | step-2 link 'Download': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T04:32:16Z | 44 | https://x.com/share?url=https://sourceforge.net/projects/blobwars/&text=Download%20Blobwars%3A%20Metal%20Blob%20Solid%20on%20SourceForge%20for%20free%21%202D%20platform%20game | step-2 link 'Share Blobwars: Metal Blob Solid on SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:17Z | 44 | https://www.facebook.com/sharer/sharer.php?u=https://sourceforge.net/projects/blobwars/&title=Blobwars%3A%20Metal%20Blob%20Solid%20on%20SourceForge | step-2 link 'Share Blobwars: Metal Blob Solid on SourceForge on facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:17Z | 44 | https://www.linkedin.com/shareArticle?mini=true&url=https://sourceforge.net/projects/blobwars/&title=Blobwars%3A%20Metal%20Blob%20Solid%20on%20SourceForge&source=SourceForge.net | step-2 link 'Share Blobwars: Metal Blob Solid on SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:18Z | 44 | https://www.google.com/preferences/source?q=sourceforge.net | step-2 link 'Add to Preferred Sources': target is not a repository root (unclassifiable); observed once, not read | used: no |
| 2026-10-30T04:32:20Z | 44 | https://sourceforge.net/top | step-2 link 'Top Downloaded Projects': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:20Z | 44 | https://sourceforge.net/about/leadership | step-2 link 'Team': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:21Z | 44 | https://x.com/sourceforge | step-2 link 'SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:21Z | 44 | https://fosstodon.org/@sourceforge | step-2 link 'SourceForge on Mastodon': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:22Z | 44 | https://www.facebook.com/sourceforgenet/ | step-2 link 'SourceForge on Facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:22Z | 44 | https://www.linkedin.com/company/sourceforge.net | step-2 link 'SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:24Z | 44 | https://sourceforge.net/reviews | step-2 link 'SourceForge Reviews': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C040-E1-01

Candidate: C040
Gate: E1
Source:   https://sourceforge.net/projects/blobwars

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C040-E2REP-02

Candidate: C040
Gate: E2-REP
Source:   https://sourceforge.net/p/blobwars/code

Surfaces:  https://sourceforge.net/projects/blobwars/ -> observed
           https://downloads.sourceforge.net/sourceforge/blobwars/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Code' at https://sourceforge.net/projects/blobwars/ -> https://sourceforge.net/p/blobwars/code | identifier 'code' (the repository's name, contract 6) appears on https://sourceforge.net/projects/blobwars/ | tree pinned at 69c55522ddaa5712a9837a9bc67c4bc71045bac5 (971 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C040-E2RULE-03

Candidate: C040
Gate: E2-RULE
Source:   doc/manual.html:258

Observed: 'You must complete the mission within a set time'

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C040-E3-04

Candidate: C040
Gate: E3
Source:   doc/manual.html:258

Observed: 'You must complete the mission within a set time'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C040-E4-05

Candidate: C040
Gate: E4
Source:   the frozen grammar over 10 candidate rows

Surfaces:  doc/hacking:85
           doc/hacking:103
           doc/hacking:360
           doc/hacking:415
           doc/license:98
           doc/license:329
           doc/manual.html:229
           doc/readme:3
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: catalogue decided 2 rows, 8 undecided, none admitted

Inference: no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 45 -- games/blockgame

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/yukiisbored/Launcher | HOMEPAGE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/yukiisbored/Launcher/releases/download/0.6.14.1-bgl/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T04:32:41Z | 45 | https://github.com/yukiisbored/Launcher | landing page rendered a README (5414 chars of page text); not used | used: no |

## EV-C041-E1-01

Candidate: C041
Gate: E1
Source:   https://github.com/yukiisbored/launcher

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C041-E2REP-02

Candidate: C041
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/yukiisbored/Launcher -> observed
           https://github.com/yukiisbored/Launcher/releases/download/0.6.14.1-bgl/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/yukiisbored/Launcher

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 46 -- games/blockrage

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://blockrage.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/blockrage/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T04:32:42Z | 46 | https://sourceforge.net/directory/ | step-2 link 'Open Source Software': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:43Z | 46 | https://sourceforge.net/articles/category/sourceforge-podcast/ | step-2 link 'SourceForge Podcast': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:44Z | 46 | https://sourceforge.net/projects/blockrage/files/latest/download | step-2 link 'Download': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T04:32:45Z | 46 | https://x.com/share?url=https://sourceforge.net/projects/blockrage/&text=Download%20Block%20Rage%20on%20SourceForge%20for%20free%21%20 | step-2 link 'Share Block Rage on SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:46Z | 46 | https://www.facebook.com/sharer/sharer.php?u=https://sourceforge.net/projects/blockrage/&title=Block%20Rage%20on%20SourceForge | step-2 link 'Share Block Rage on SourceForge on facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:46Z | 46 | https://www.linkedin.com/shareArticle?mini=true&url=https://sourceforge.net/projects/blockrage/&title=Block%20Rage%20on%20SourceForge&source=SourceForge.net | step-2 link 'Share Block Rage on SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:47Z | 46 | https://www.google.com/preferences/source?q=sourceforge.net | step-2 link 'Add to Preferred Sources': target is not a repository root (unclassifiable); observed once, not read | used: no |
| 2026-10-30T04:32:47Z | 46 | https://sourceforge.net/top | step-2 link 'Top Downloaded Projects': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:47Z | 46 | https://sourceforge.net/about/leadership | step-2 link 'Team': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:48Z | 46 | https://x.com/sourceforge | step-2 link 'SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:48Z | 46 | https://fosstodon.org/@sourceforge | step-2 link 'SourceForge on Mastodon': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:48Z | 46 | https://www.facebook.com/sourceforgenet/ | step-2 link 'SourceForge on Facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:49Z | 46 | https://www.linkedin.com/company/sourceforge.net | step-2 link 'SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T04:32:50Z | 46 | https://sourceforge.net/reviews | step-2 link 'SourceForge Reviews': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C042-E1-01

Candidate: C042
Gate: E1
Source:   https://blockrage.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C042-E2REP-02

Candidate: C042
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://blockrage.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/blockrage/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 47 -- games/bluemoon

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.catb.org/~esr/bluemoon/ | HOMEPAGE+SITES | unmatched | observed | project-page | 200 | official-project-page |

| 2026-10-30T04:33:16Z | 47 | https://gitlab.com/esr/bluemoon | landing page rendered a README (289 chars of page text); not used | used: no |

## EV-C043-E1-01

Candidate: C043
Gate: E1
Source:   https://www.catb.org/~esr/bluemoon

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C043-E2REP-02

Candidate: C043
Gate: E2-REP
Source:   https://gitlab.com/esr/bluemoon

Surfaces:  http://www.catb.org/~esr/bluemoon/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'https://gitlab.com/esr/bluemoon' at http://www.catb.org/~esr/bluemoon/ -> https://gitlab.com/esr/bluemoon | identifier 'bluemoon' (the repository's name, contract 6) appears on http://www.catb.org/~esr/bluemoon/ | tree pinned at 91ff5db75d1eccf9731d2373c7617d6dc1ee6656 (10 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C043-E2RULE-03

Candidate: C043
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.adoc
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.adoc

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 48 -- games/bomberclone

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.bomberclone.de/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/bomberclone/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

## EV-C044-E1-01

Candidate: C044
Gate: E1
Source:   https://www.bomberclone.de

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C044-E2REP-02

Candidate: C044
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.bomberclone.de/ -> observed
           https://downloads.sourceforge.net/sourceforge/bomberclone/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED
