# Screening batch 12 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b12.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 89 | games/dangerdeep | PASS | C079 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 90 | games/dd2 | PASS | C080 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 91 | games/defendguin | PASS | C081 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIABLE-SURFACE |
| 92 | games/devilutionx | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-METADATA-UNRESOLVED |
| 93 | games/dhewm3 | PASS | C082 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 94 | games/dmagnetic | PASS | C083 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 95 | games/doomdata/shareware | UNRESOLVED | NONE | - | - | - | - | - | UNRESOLVED | UR | PI-TRANSPORT-INDETERMINATE |
| 96 | games/dopewars | PASS | C084 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |

## rank 89 -- games/dangerdeep

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://dangerdeep.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/dangerdeep/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T06:58:54Z | 89 | https://sourceforge.net/directory/ | step-2 link 'Open Source Software': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:58:55Z | 89 | https://sourceforge.net/articles/category/sourceforge-podcast/ | step-2 link 'SourceForge Podcast': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:58:56Z | 89 | https://sourceforge.net/projects/dangerdeep/files/latest/download | step-2 link 'Download': target is not a repository root (distfile-location); observed once, not read | used: no |
| 2026-10-30T06:59:01Z | 89 | https://x.com/share?url=https://sourceforge.net/projects/dangerdeep/&text=Download%20Danger%20from%20the%20Deep%20on%20SourceForge%20for%20free%21%20WW2%20U-boat%20simulation | step-2 link 'Share Danger from the Deep on SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:02Z | 89 | https://www.facebook.com/sharer/sharer.php?u=https://sourceforge.net/projects/dangerdeep/&title=Danger%20from%20the%20Deep%20on%20SourceForge | step-2 link 'Share Danger from the Deep on SourceForge on facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:02Z | 89 | https://www.linkedin.com/shareArticle?mini=true&url=https://sourceforge.net/projects/dangerdeep/&title=Danger%20from%20the%20Deep%20on%20SourceForge&source=SourceForge.net | step-2 link 'Share Danger from the Deep on SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:03Z | 89 | https://www.google.com/preferences/source?q=sourceforge.net | step-2 link 'Add to Preferred Sources': target is not a repository root (unclassifiable); observed once, not read | used: no |
| 2026-10-30T06:59:05Z | 89 | https://sourceforge.net/top | step-2 link 'Top Downloaded Projects': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:05Z | 89 | https://sourceforge.net/about/leadership | step-2 link 'Team': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:05Z | 89 | https://x.com/sourceforge | step-2 link 'SourceForge on X': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:06Z | 89 | https://fosstodon.org/@sourceforge | step-2 link 'SourceForge on Mastodon': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:07Z | 89 | https://www.facebook.com/sourceforgenet/ | step-2 link 'SourceForge on Facebook': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:07Z | 89 | https://www.linkedin.com/company/sourceforge.net | step-2 link 'SourceForge on LinkedIn': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:09Z | 89 | https://sourceforge.net/reviews | step-2 link 'SourceForge Reviews': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C079-E1-01

Candidate: C079
Gate: E1
Source:   https://dangerdeep.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C079-E2REP-02

Candidate: C079
Gate: E2-REP
Source:   https://sourceforge.net/p/dangerdeep/code

Surfaces:  https://dangerdeep.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/dangerdeep/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: designated and observed, but the pin could not be taken: Command '['git', 'ls-remote', '--symref', 'https://git.code.sf.net/p/dangerdeep/code', 'HEAD']' returned non-zero exit status 128.

Inference: a designated repository that git cannot fetch is a shape no sealed criterion describes (contract Section 7)

Decision: UNRESOLVED


## rank 90 -- games/dd2

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.usebox.net/jjm/dd2 | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| http://www.usebox.net/jjm/dd2/releases/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |

| 2026-10-30T06:59:15Z | 90 | https://www.usebox.net/jjm/open-source/ | step-2 link 'Open Source': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:16Z | 90 | http://www.gp32x.de/cgi-bin/cfiles.cgi?0,0,0,0,30,927 | step-2 link 'download source code': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:18Z | 90 | http://www.symbioosi.net/English/projects.html | step-2 link 'binaries and the source code for IUQ3 here': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:59:20Z | 90 | http://omnimaga.org/index.php?topic=13589.msg247973 | step-2 link 'binaries and the source code here': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C080-E1-01

Candidate: C080
Gate: E1
Source:   https://www.usebox.net/jjm/dd2

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C080-E2REP-02

Candidate: C080
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.usebox.net/jjm/dd2 -> observed
           http://www.usebox.net/jjm/dd2/releases/ -> observed (HTTP 403)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 91 -- games/defendguin

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://www.newbreedsoftware.com/defendguin/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| ftp://ftp.tuxpaint.org/unix/x/defendguin/src/ | SITES | unmatched | unclassifiable | unclassifiable |  |  |

## EV-C081-E1-01

Candidate: C081
Gate: E1
Source:   https://www.newbreedsoftware.com/defendguin

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C081-E2REP-02

Candidate: C081
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://www.newbreedsoftware.com/defendguin/ -> observed
           ftp://ftp.tuxpaint.org/unix/x/defendguin/src/ -> unclassifiable
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIABLE-SURFACE

Decision: UNRESOLVED


## rank 92 -- games/devilutionx

## EV-R092-UR-01

Candidate: (none: rank 92)
Gate: UR
Source:   games/devilutionx/Makefile

Observed: modules=['devel/cmake'] unresolved=['${SITES_GITHUB}']

Inference: the resolver cannot resolve the frozen metadata (contract Section 2)

Decision: UNRESOLVED


## rank 93 -- games/dhewm3

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://dhewm3.org | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/dhewm/dhewm3/archive/refs/tags/1.5.4/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/dhewm/dhewm3 | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3 | landing page rendered a README (21452 chars of page text); not used | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.5 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:11Z | 93 | https://www.macsourceports.com/game/doom3 | step-2 link 'Mac Source Ports': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.5_RC3 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.5_RC2 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.5_RC1 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.4 | step-2 link 'download dhewm3 1.5.4 at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:11Z | 93 | https://github.com/dhewm/dhewm3-sdk | landing page rendered a README (23161 chars of page text); not used | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.4_RC3 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.4_RC2 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.4_RC1 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.3 | step-2 link 'download dhewm3 1.5.3 at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.3_RC2 | step-2 link 'dhewm3 1.5.3 RC2 at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.3_RC1 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.2 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.2_RC2 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.2_RC1 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:12Z | 93 | https://github.com/dhewm/iddevnet | landing page rendered a README (3580 chars of page text); not used | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.1 | step-2 link 'download dhewm3 1.5.1 at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.1_RC3 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.1_RC2 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.1_RC1 | step-2 link 'download it at Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.1_PRE1 | step-2 link 'dhewm3_1.5.1pre1_win32.zip available on Github' leads to a forbidden class; not followed | used: no |
| 2026-10-30T07:01:10Z | 93 | https://github.com/dhewm/dhewm3/releases/tag/1.5.0 | step-2 link 'at Github' leads to a forbidden class; not followed | used: no |

## EV-C082-E1-01

Candidate: C082
Gate: E1
Source:   https://github.com/dhewm/dhewm3

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C082-E2REP-02

Candidate: C082
Gate: E2-REP
Source:   https://github.com/dhewm/dhewm3

Surfaces:  https://dhewm3.org -> observed
           https://github.com/dhewm/dhewm3/archive/refs/tags/1.5.4/ -> closed-by-class (forbidden class, never requested)
           https://github.com/dhewm/dhewm3 -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: designation 'dhewm 3 (Doom3 sourceport) main repository' at https://github.com/dhewm/dhewm3 -> https://github.com/dhewm/dhewm3; a label link leads to another work's source: 'Updated the code of all mods hosted in dhewm3-sdk repository' at https://dhewm3.org -> https://github.com/dhewm/dhewm3-sdk | identifier 'dhewm3' (the repository's name, contract 6) appears on https://dhewm3.org | tree pinned at 455b88e8dff2be822f08eb498f51b383e851fa38 (1551 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C082-E2RULE-03

Candidate: C082
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           neo/sys/linux/setup/makeself/makeself.1
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, neo/sys/linux/setup/makeself/makeself.1

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 94 -- games/dmagnetic

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.dettus.net/dMagnetic/ | HOMEPAGE+SITES | unmatched | observed | project-page | 200 | official-project-page |

## EV-C083-E1-01

Candidate: C083
Gate: E1
Source:   https://www.dettus.net/dmagnetic

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C083-E2REP-02

Candidate: C083
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.dettus.net/dMagnetic/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 95 -- games/doomdata/shareware

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.gamers.org/pub/idgames/historic/ | SITES | unmatched | not-reached |  |  |  |
| https://www.gamers.org/pub/idgames/idstuff/doom/ | SITES.19 | unmatched | not-reached |  |  |  |

## EV-R095-UR-01

Candidate: (none: rank 95)
Gate: UR
Source:   games/doomdata/shareware/Makefile

Observed: homepage=None sites=['https://www.gamers.org/pub/idgames/historic/', 'https://www.gamers.org/pub/idgames/idstuff/doom/'] gh=None tuples=[]

Inference: no key from the other fields, and a SITES URL whose class would decide it failed in transport after two retries (contract Section 3; RQA-53)

Decision: UNRESOLVED


## rank 96 -- games/dopewars

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://dopewars.sourceforge.io/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/dopewars/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T07:03:27Z | 96 | https://sourceforge.net/projects/dopewars/ | step-2 link 'SourceForge project page': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T07:03:28Z | 96 | https://github.com/benmwebb/dopewars | landing page rendered a README (8047 chars of page text); not used | used: no |
| 2026-10-30T07:03:26Z | 96 | https://github.com/benmwebb/dopewars-website/blob/main/index.php | step-2 link 'Edit on GitHub' points at a file inside https://github.com/benmwebb/dopewars-website; the file is not opened, the root is | used: no |
| 2026-10-30T07:03:29Z | 96 | https://github.com/benmwebb/dopewars-website | landing page rendered a README (3373 chars of page text); not used | used: no |

## EV-C084-E1-01

Candidate: C084
Gate: E1
Source:   https://dopewars.sourceforge.io

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C084-E2REP-02

Candidate: C084
Gate: E2-REP
Source:   https://github.com/benmwebb/dopewars

Surfaces:  https://dopewars.sourceforge.io/ -> observed
           https://downloads.sourceforge.net/sourceforge/dopewars/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'development code at GitHub' at https://dopewars.sourceforge.io/ -> https://github.com/benmwebb/dopewars | identifier 'dopewars' (the repository's name, contract 6) appears on https://dopewars.sourceforge.io/ | tree pinned at 09d6424798ab3bf4df83699a3b825b871523ecef (209 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C084-E2RULE-03

Candidate: C084
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           doc/index.html
           CONTRIBUTING.md
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, doc/index.html, CONTRIBUTING.md

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED
