# KF-0 rule applied -- EXPLORATORY C084 study (X8)

EXPLORATORY. Design Section 8, applied at X8 after the P_raw freeze
(`5f0f491`) and before any unit is analysed. Nothing here opens an
issue: the tracker was read for its label list and for counts, through
`tools/kf_api.py` (commit `5e6d902`), which discards titles and bodies
before anything is displayed. The issue numbers themselves are
enumerated at X12 (sealed KF-0: "enumerated only after the primary lane
and all three primary artifacts are frozen").

## 1. Tracker of record

The project designates its tracker in its own front page:

> Please report any bugs, glitches or crashes that you encounter to the
> GitHub [Issue Tracker](https://github.com/fabiangreffrath/crispy-doom/issues).
> (`README.md:106`)

`CMakeLists.txt:17` sets `PACKAGE_BUGREPORT` to the same URL. One
in-tree file points elsewhere: `.github/CONTRIBUTING.md:15-21` and `:60`
name the parent project's tracker (`chocolate-doom/chocolate-doom`);
that file is the parent's text carried into the fork ("Thanks for
contributing to Chocolate Doom!", `:1`), and the README's own
designation prevails. Tracker of record:
`https://github.com/fabiangreffrath/crispy-doom/issues`.

## 2. Labels and the failure set L (read 2026-10-29T06:47:42Z)

Eighteen labels; every description the API returned was empty, so each
decision rests on the name alone (design Section 8: "whose NAME or
project-written DESCRIPTION denotes a failure (bug, defect, crash,
regression, error, or a synonym)").

| label | in L | the word that decided |
|---|---|---|
| `:warning: submitter action required` | no | a process state, not a failure |
| `bug` | **yes** | bug |
| `duplicate` | no | a ticket relation |
| `enhancement` | no | a request, not a failure |
| `good first issue` | no | a contributor hint |
| `help wanted` | no | a contributor hint |
| `invalid` | no | a ticket judged invalid, not a program failure |
| `maybe-critical` | **yes** | critical: a (possibly) critical defect; a severity word applied to failures |
| `non-doom` | no | an area (the non-Doom games) |
| `OS-specific` | no | an area |
| `patch` | no | a fix being offered |
| `pending` | no | a process state |
| `question` | no | not a failure |
| `rendering` | no | an area |
| `SDL-related` | no | an area / origin |
| `sound-issues-on-windows` | **yes** | issues (problems): a failure class in an area |
| `upstream` | no | origin of a failure, not the failure |
| `wontfix` | no | a resolution |

`L = {bug, maybe-critical, sound-issues-on-windows}`. All three are
taken; none is chosen among (Section 8). Two of the three are
judgment calls on a single word (`maybe-critical`, `sound-issues-on-
windows`) and are recorded as such; the reading not taken -- `bug`
alone -- would give the `bug` count below.

## 3. The rule as applied

`L` is non-empty, so:

```text
KF set = every issue of the tracker of record, open and closed, pull
         requests excluded, carrying at least one label in L, as of the
         enumeration timestamp
no time window, no status filter, no component filter, no subsampling
```

## 4. Count (X8; the only thing read before X12)

```text
2026-10-29T06:48:11Z  count=37  labels=bug,maybe-critical,sound-issues-on-windows
per label              bug 14   maybe-critical 12   sound-issues-on-windows 11
                       (the three sets are disjoint: 14 + 12 + 11 = 37)
```

The count was produced by `kf_api.py count` with every object stripped
to its number and pull-request marker; no title, body or id was
displayed. For scale (design Section 8, estimated, not measured): KF-1
plus KF-2 for one item under review, one to two hours.

Recorded beside the count, as the design's own caveat: the KF set is
complete only within the project's labelling. A project with this many
issues and fourteen `bug` labels labels sparsely; failure reports that
carry no label in `L` are outside the set by the rule, not by their
nature.

## 5. Decision T2

T2 -- pending the owner's decision, on the count alone: `attempt in
full` (X12-X14 run on all 37 items) or `N/A -- boundedness failure`
(the lane reports the rule, `L`, the count and this decision, and
X12-X14 are not executed).
