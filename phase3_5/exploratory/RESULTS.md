# Phase 3.5 Exploratory Study (C084 Crispy Doom) -- RESULTS -- EXPLORATORY

EXPLORATORY. This document consolidates and seals the exploratory
study of C084 Crispy Doom at revision `7775ef82d1e9dfd50eb9d2824acefaeff7247458`,
executed under the sealed Phase 3.5 methodology's analysis lane with
the two substitutions of its design (Section 2.1, below). The design's
anti-goal 1, in full: "**The exploratory result used as if it were
Run 2's result** (the owner's anti-goal, stated 2026-10-29).
Concretely: this study's R0 / F0 / F1 / F2 / F3 findings appearing in
any summary of Phase 3.5 as "what Phase 3.5 found", or being merged
with a later confirmatory result, or Run 2's preregistration being
tuned to reproduce or avoid them." Nothing below is the Phase 3.5
result: that is `phase3_5/RESULTS.md` (`8344da1`), unchanged by this
study. Written 2026-10-29, after the record and from it; every number is
recomputed from the frozen tables, `KF.md`, `EXECUTION_QA.md` and the
commit record by the script that wrote this file, and no observation of
the target was made for this document.

Design: `docs/superpowers/specs/2026-10-29-phase3-5-exploratory-c084-design.md`
(sealed `984f0c5`). Plan: `docs/superpowers/plans/2026-10-29-phase3-5-exploratory-c084.md`
(`573c19c`). Record: this directory, `phase3_5/exploratory/`, with its own
QA log (`EXECUTION_QA.md`, XQA-01 .. XQA-14) kept apart from the
screening run's QA-01 .. QA-43.

## 1. The question, and the two substitutions (design Section 2.1)

Phase 3's closing question -- "do these boundaries appear when the
system under test was defined by someone else?" (`phase3/RESULTS_C4.md`,
Section 6) -- had no answer of any kind in the record, because the
screening run never reached a target (`phase3_5/RESULTS.md`, Section
2). This study puts the question to one system. It is exploratory, not
the confirmatory Phase 3.5 result, for two reasons that are recorded
rather than argued away:

```text
substitution 1  the target was chosen by the owner's hand (C084, one of
                the three ELIGIBLE candidates), in place of sealed
                Section 15 step 5's ranking and selection -- which the
                screening run determined INCONCLUSIVE (QA-19)
substitution 2  the revision is the screening's observation-time pin
                (EV-C084-PIN-01, 2026-08-30), in place of the snapshot
                at the sealed instant 2026-08-26T19:23:05Z that QA-28
                found unobtainable; the sealed-instant check executed
                here returned DIFFERS (XQA-01, Section 14.1)
```

Everything else -- the inventory, the universe, the sufficiency gate,
the taxonomy, the three artifacts, the known-failure lane and its
firewall -- was executed as the sealed methodology states it, with
every reading the sealed text left open recorded in XQA at the time.

## 2. What was executed, against the order of operations

Sealed Section 15 steps 4 and 6 through 15, as the design's X-steps
(Section 14), each in its own commit (committer times as recorded,
UTC+09:00):

```text
X0    984f0c5  2026-10-29T14:32  design sealed
      573c19c  2026-10-29T14:55  implementation plan
X4a   8919675  2026-10-29T15:02  snapshot pinned, digests 10/10, archive MATCH, sealed instant DIFFERS
X4b   3c22d50  2026-10-29T15:09  inventory: candidate tables, regeneration (XQA-04), verdicts
      93e76f7  2026-10-29T15:16
      089e520  2026-10-29T15:29
X6    5f0f491  2026-10-29T15:34  P_raw frozen
X7    8ab2928  2026-10-29T15:35  E5 checkpoint; T1 = proceed (XQA-09)
      66dd3fc  2026-10-29T15:43
X8    310f368  2026-10-29T15:48  KF-0 applied, count 37; T2 = attempt in full (XQA-10)
      6ad1658  2026-10-29T15:51
X9    3a1010e .. 7789904  14 native cases, each committed and accepted by the owner; T3 = continue after NC-01 (XQA-11)
X10a  7b56ded  2026-10-29T17:26  Artifact 1 complete
X10b  bc6361d  2026-10-29T17:28  Artifact 2
X10c  3d44781  2026-10-29T17:31  Artifact 3; Artifact 2 accepted (XQA-12)
X11   6da6a50  2026-10-29T17:32  PRIMARY_RESULT.md -- the primary seal
X12   4a79e22  2026-10-29T17:35  KF items enumerated: 37 (X8 count 37); lane opened by the owner (XQA-13)
X12/13 d9e0f20 .. f5b3299  KF-1 and KF-2 per item, four batch commits
X13   504d302  2026-10-29T17:59  KF-2 sealed
X14   e8ee098 .. 24d6dbd  KF-3 per item, 4 batch commits; completion recorded as XQA-14 (172102c)
X15   this document
```

Steps 1-3 and 5 of sealed Section 15 are the screening run's and are
not re-executed (`phase3_5/RESULTS.md`, Sections 3-5). No step was
skipped, shortened or reordered; the one deviation from the plan's
commit granularity (KF items committed per batch of about ten rather
than one by one) is a ruling in the execution ledger, not a change to
what was read or written per item.

## 3. Reporting requirements (sealed Section 14), item by item

### 14.1 Frame, screening, tie-break, snapshot

The frame, the screening order and budget, the eligibility evidence,
the screened-candidate log and the tie-break rule are the screening
run's and are reported in `phase3_5/RESULTS.md`, Sections 3-5; this
study adds none and changes none. Its target is substitution 1 above,
its revision substitution 2. The snapshot as executed (`pin_record.md`,
design Section 4.2):

```text
fetch          depth-1 fetch of the bare commit id succeeded; archive fallback not needed
identity       7775ef82d1e9dfd50eb9d2824acefaeff7247458, 801 tracked files
digests        10 of 10 pinned file digests match the tree on disk
archive        2648481 bytes, sha256 4edfcde1c4f6..., 832 entries -- all MATCH the screening's pin, 60 days later
sealed instant DIFFERS: master's history at 2026-08-26T19:23:05Z holds 3a39d0a5 (dated 2026-08-24), not the revision (XQA-01)
```

The DIFFERS result is QA-28's gap met in the data, not closed: an
observation made later cannot tell whether that commit entered master
before or after the instant, and ancestry was not queried (design
Section 5.1 admits the API for three purposes only).

### 14.2 Admitted universe sources and enforced/asserted tags

```text
U_normative   EMPTY -- 42 in-tree document candidates (S_doc): 36 REJECT (no project
              statement designates the file as stating rules, requirements or
              accepted inputs), 6 QUARANTINED (NEWS/CHANGELOG/RELEASE/NOT-BUGS/TODO
              class, never opened in the study apart from the five NEWS.md lines a
              scratch helper printed, XQA-06); nearest cases in XQA-07 (b)
U_enforced    23 enumerators admitted of 618 candidates, every one tagged `enforced`
              (compiled-in arrays bounded by arrlen, a terminator or a fixed index
              range); asserted 0
```

The normative route is unavailable for this target as sealed Section
3.1 provides; the universe is `U_enforced` alone, and no cross-link
edge exists. The inventory that produced these counts is Section 5's
second input to Run 2.

### 14.3 Frozen P_raw with provenance

`P_raw.tsv` (`5f0f491`): 1132 counting units, one per source observation,
each row carrying its observation id, enumerator id, `enforced` tag,
linked flag (0 throughout) and the initializer row's text; the
observation's file, line and index are in `observations.tsv` under the
same id. Externally-linked units 0; no observation is retained inside
another. From the 1141 initializer rows
of the admitted arrays, 8 terminator rows (XQA-07 c) and 1 row beyond
the consulting loop's bound (XQA-08, `enumerator_bounds.tsv`) are not
members. Units per enumerator:

```text
C186    336  src/heretic/deh_htext.c  unsupported_strings_1_0
C187    305  src/heretic/deh_htext.c  unsupported_strings_1_2
C188    305  src/heretic/deh_htext.c  unsupported_strings_1_3
C455     30  src/setup/joystick.c  known_joysticks
C434     26  src/net_dedicated.c  not_dedicated_options
C017     17  src/d_iwad.c  iwads
C023     16  src/d_mode.c  valid_versions
C022     15  src/d_mode.c  valid_modes
C364     15  src/hexen/p_setup.c  MapCmdNames
C013     11  pkg/osx/IWADController.m  IWADFilenames
C034     11  src/doom/d_main.c  gameversions
C268      9  src/heretic/p_user.c  WeaponInShareware
C413      6  src/i_sdlmusic.c  music_sdl_devices
C414      6  src/i_sdlsound.c  sound_sdl_devices
C426      5  src/i_winmusic.c  music_win_devices
C464      4  src/setup/mode.c  mission_configs
C595      4  src/w_main.c  unique_lumps
C191      3  src/heretic/deh_htic.c  hhe_versions
C313      2  src/hexen/h2_main.c  gameversions
C410      2  src/i_oplmusic.c  music_opl_devices
C499      2  src/strife/d_main.c  gameversions
C403      1  src/i_flmusic.c  music_fl_devices
C412      1  src/i_pcsound.c  sound_pcsound_devices
```

### 14.4 Coverage

```text
P_resolved / P_raw   1132 / 1132
E? / P_raw           0 / 1132
```

Every preregistered unit was analysed in P_raw order (sealed 8.6, no
optional stopping; design anti-goal 2).

### 14.5 Reason log for every E?, and the explicit F2 re-check

`E_LOG.md` has no entry: no unit lacked a located answer to any of the
five sufficiency questions (every native case's five answers cite a
file and line, `ARTIFACT_1_native.md`; `checks.py artifact1` enforces
the citation). The explicit F2 re-check that sealed Section 6.1
attaches to each E? entry therefore has nothing to attach to; the F2
test itself was applied to every native case inside Artifact 2's
decision chain ("F2 if a required structure has no place") and
supported none -- see 14.7 and sealed 13.2 in 14.12.

### 14.6 Correspondence matrix and the collapsed count C

```text
matched / normative-only / divergent / externally-linked   0 / 0 / 0 / 0
enforcement-only                                            1132   every unit
analyst-inferred correspondence (units -> native cases)     14   many-to-one, in units.tsv
one-to-many                                                 0
C (distinct native cases)                                   14
```

`C` is reported beside `P_raw`, never in its place. The largest
collapse is NC-06: 946 units (83.6% of P_raw) are one native case,
because the three HHE lists segment by executable offset (sealed 13.4).

### 14.7 Findings per native case, and the unit-to-case map

```text
case   finding  units  range          native case (Artifact 1 title, shortened)
NC-01  F1         11  U001..U011  the launcher's IWAD slots, keyed by the standard IWAD filena
NC-02  F0         17  U012..U028  the IWAD registry: identifying the game's IWAD by its filena
NC-03  R0         15  U029..U043  valid game mode/mission combinations, with their episode and
NC-04  F0         16  U044..U059  valid mission/version pairs for a network game (src/d_mode.c
NC-05  F3         15  U060..U1128  the emulated game version: `-gameversion` against the suppor
NC-06  F0        946  U071..U1016  HHE text replacement: string offsets that are valid but unsu
NC-07  F0          3  U1017..U1019  the HHE patch version: `-hhever` against the valid Heretic v
NC-08  F1          9  U1020..U1028  which weapons may be selected in the Heretic shareware game 
NC-09  F0         15  U1031..U1045  the MAPINFO commands Hexen's map-information parser accepts 
NC-10  F1         21  U1046..U1066  which sound devices each sound and music module supports, an
NC-11  F0         26  U1067..U1092  game options a dedicated server refuses to accept on its own
NC-12  F0         30  U1093..U1122  known joysticks: which controllers the setup tool recognises
NC-13  F0          4  U1123..U1126  the games the setup tool configures: `-game` against the fou
NC-14  F0          4  U1129..U1132  lumps unique to each game, used to refuse an IWAD run under 

native cases    R0 1   F0 9   F1 3   F2 0   F3 1
counting units  R0 15   F0 1061   F1 41   F2 0   F3 15
```

Each case carries its full supported subset of {F1, F2, F3}, or R0/F0
where that subset is empty; no case carries two findings and none is
suppressed (`ARTIFACT_2_mapping.md`). NC-03's R0 names its competitor
(per-client state in place of the session-level record the connect
judgment adopts) and the evidence that discriminated against it. The
many-to-one map is `units.tsv` (every unit names its case); NC-05
gathers the Doom, Hexen and Strife version tables, its F3 scoped to the
Doom units U060-U070 only.

### 14.8 Counterexamples and their evidence basis

Four native cases carry a counterexample to the Phase 3 architecture;
sealed 8.1 needs one. Each rests on located native evidence:

```text
NC-01  F1  the launcher keeps a recognised IWAD as the slot's path and the launch
           judges only that a slot is selected: provenance in ordinary state
           (pkg/osx/IWADController.m:425-431, :258-264; LauncherManager.m:278-289)
NC-08  F1  the shareware weapon gate is a predicate over current state evaluated
           at the request: the judgment role collapses into a state predicate
           (src/heretic/p_user.c:662-675)
NC-10  F1  the sound module pointer carries the device selection's outcome and
           every later call judges on its presence (src/i_sound.c:133-203, :291-373)
NC-05  F3  Doom persists the version under which a save or demo was written as a
           fact, written by the action and judged only at consumption, owned by
           the artifact -- the reverse of Phase 3's judgment-written verdict
           (src/doom/p_saveg.c:1426-1476; src/doom/g_game.c:3209-3216, :3341-3366)
```

The F3 carries the study's first limitation on its face: the target was
chosen for the shape of this mechanism (L1), so the finding was looked
for, not found by chance, and is reported as such.

### 14.9 Absence and inconclusive wording

Sealed 8.4 governs the case of no counterexample and does not apply.
Retention is scoped as 8.2 requires: among the 14 native cases
recovered from 1132 / 1132 preregistered units, one (NC-03) positively
retains the provenance boundary against a named competitor, 9 neither
retain nor contradict any boundary (input validations over a
transition-only input, Artifact 2's stated convention), and 4
contradict one. Every admitted enumerator is `enforced`, so no absence
wording needs weakening to an asserted scope. R0 is corroboration from
one case, never proof of necessity (sealed 7.1). No F2 was supported;
sealed 13.2 applies to this target as written.

### 14.10 The three frozen primary artifacts

```text
Artifact 1  ARTIFACT_1_native.md    7b56ded   native description, 14 cases, five located answers each
Artifact 2  ARTIFACT_2_mapping.md   bc6361d   mapping and outcomes; accepted by the owner (XQA-12)
Artifact 3  ARTIFACT_3_judgment.md  3d44781   applicability domain (D1-D14 and the out-of-domain list)
                                           stated before the decision procedure; totality line
primary     PRIMARY_RESULT.md       6da6a50   sealed before any known-failure item was opened
```

### 14.11 The known-failure lane

```text
KF-0 rule      every issue of the tracker of record (README.md:106), open and closed,
               pull requests excluded, carrying a label whose name denotes a failure:
               L = {bug, maybe-critical, sound-issues-on-windows}; no window, no filter
count          37 at X8 (14 + 12 + 11, disjoint); 37 enumerated at X12 -- equal
T2             attempt in full (XQA-10)
disclosure     1 X4b row (XQA-06), 37 X12 rows (one per item, first post only, cause
               leakage yes 18 / no 19), 37 X14 rows (comments, timelines, linked commits)
KF-2 domain    in-domain concordant 3   DISCORDANT 0   indeterminate 0   out-of-domain 34
KF-2 repr.     representable 2   partly 4   not representable 31
attribution    scope mismatch 37
native replay  N/A for the lane, declared in advance (design Section 8)
KF-3           37 of 37 compared: scope mismatch 33; insufficient external causal evidence 4
               post-hoc observations #174, #408, #646, #655, #780, #807; coupled mapping->judgment findings none
```

The three concordant results (#454, #458, #780) hold for the sound-
device selection each report rests on (D10), with the reported failure
itself outside every class; no item was in-domain DISCORDANT or
indeterminate. The lane's firewall held: no comment, linked commit or
third-party source was read before X13 was sealed (`504d302`), and
nothing in Artifacts 1-3, `units.tsv`, `E_LOG.md` or
`PRIMARY_RESULT.md` was edited after the primary seal. Per item, in id
order (`KF.md`):

```text
item   KF-2 domain              KF-2 representability   KF-3
#90    out-of-domain            not representable       scope mismatch
#92    out-of-domain            not representable       scope mismatch
#174   out-of-domain            partly                  scope mismatch (observation)
#250   out-of-domain            not representable       scope mismatch
#258   out-of-domain            not representable       scope mismatch
#318   out-of-domain            not representable       scope mismatch
#362   out-of-domain            not representable       scope mismatch
#365   out-of-domain            not representable       scope mismatch
#408   out-of-domain            not representable       scope mismatch (observation)
#454   in-domain concordant     representable           scope mismatch
#457   out-of-domain            not representable       scope mismatch
#458   in-domain concordant     representable           scope mismatch
#462   out-of-domain            not representable       scope mismatch
#463   out-of-domain            not representable       scope mismatch
#475   out-of-domain            not representable       insufficient external causal evidence
#498   out-of-domain            not representable       scope mismatch
#524   out-of-domain            not representable       scope mismatch
#527   out-of-domain            not representable       scope mismatch
#528   out-of-domain            not representable       scope mismatch
#556   out-of-domain            not representable       scope mismatch
#646   out-of-domain            not representable       scope mismatch (observation)
#655   out-of-domain            partly                  scope mismatch (observation)
#657   out-of-domain            not representable       scope mismatch
#677   out-of-domain            not representable       insufficient external causal evidence
#703   out-of-domain            not representable       scope mismatch
#706   out-of-domain            not representable       scope mismatch
#716   out-of-domain            not representable       insufficient external causal evidence
#718   out-of-domain            not representable       scope mismatch
#727   out-of-domain            not representable       scope mismatch
#730   out-of-domain            not representable       insufficient external causal evidence
#780   in-domain concordant     partly                  scope mismatch (observation)
#807   out-of-domain            not representable       scope mismatch (observation)
#814   out-of-domain            not representable       scope mismatch
#886   out-of-domain            not representable       scope mismatch
#890   out-of-domain            not representable       scope mismatch
#893   out-of-domain            partly                  scope mismatch
#1043  out-of-domain            not representable       scope mismatch
```

How the reveal compared. The frozen account named no cause for any
item -- 34 were outside every class's domain and 3 concordant only for
the sound-device selection their report rests on -- so cause agreement
was N/A throughout and the comparison asked one thing: does the
external cause lie inside the frozen scope? In no item does it. Where
a cause is given it is: the SDL libraries and Windows audio drivers
(#454, #457, #458, #498, #718); external MIDI synthesisers and hosts
(#462; #677 and #716 undiagnosed; #814 resolved by the redesigned
native Windows MIDI, the frozen tree's music_win_module); the renderer
(#250, #524, #527, #528, #886, #890; #730 undiagnosed); game rules
kept for demo and network compatibility (#174, #258, #318, #362, #365,
#556, #657, #703); PWAD content (#408, #646); file-name case (#655);
demo and pause handling (#92, #463, #706, #727; #475 undiagnosed); a
check run before the state it reads was written (#807); the SDL music
module's own Init branch (#780); the fork's Hexen mouselook change
(#893); and a compiler (#1043). Nothing read contradicted Artifact 1's
description of any native case (previously hidden native information
0), and Artifact 3 inherited no error from Artifact 2 (coupled
mapping->judgment finding 0). Six post-hoc observations are recorded
in `KF.md`, each marked as creating no unit, edge or finding (sealed
4.3, 8.6): #174 the savegame does not persist a fact (gametic parity)
that the restore then decides anew; #408 a kind-blind lump-name
lookup; #646 a second fork 'make non-fatal' instance beside
deh_signatures (XQA-07 d); #655 a function-scope accepted-names list
that class K1 cannot see, whose nearest file-scope kin was rejected at
EN2 as discovery (an L2 instance); #780 the SDL music module's Init
branching on the device value a second time, where the frozen tree has
a device value of its own (U1046); #807 a validity check evaluated at a
transition before the action under way had written the state it
reads. The reveal edited nothing above the KF-3 lines (XQA-14).

### 14.12 Pre-registered limitations

The sealed methodology's five (Section 13) all apply: 13.1 the
open-source / inspectability selection effect (the target is an open
source port, chosen among open-source candidates); 13.2 F2 may be
especially under-observed (none was supported here); 13.3 asserted-
enumerator missingness is directional (no asserted enumerator was
admitted, so the direction did not arise); 13.4 external segmentation
and cross-links determine P_raw (the HHE offset lists set 83.6% of it);
13.5 no executable-search generalisation claim (no simulator, no search).
The study's own nine (design Section 13), with how each played out:

```text
L1  hand-chosen target, chosen for witness shape -- the one F3 is on that
    mechanism (NC-05) and is reported as looked for, not found
L2  inventory classes K1-K4 are the analyst's -- widened once before the run
    (XQA-02) and corrected once against its own class (XQA-04); two idioms
    the classes cannot see are recorded and not added
L3  the analyst's prior exposure -- the XQA-04 defect was found by looking for
    a table the analyst already knew; without that knowledge it would have been
    found later or not at all
L4  fork lineage -- every native case's lineage line reads `inherited`; the four
    counterexamples are in inherited mechanisms, two with fork changes beside
    the mechanism (NC-10) or at its checks (NC-05), none in Crispy's own
    additions; nothing is claimed about C065
L5  E5 reduced to finiteness plus T1 on the count -- E5 PASS (E5.md); E? was
    tested unit by unit and stayed empty
L6  the KF lane's size unknown until X8 -- 37, attempted in full by the owner's
    T2, with no numeric ceiling preregistered
L7  one analyst, one reviewer -- every native case, Artifact 2 and the primary
    seal accepted by the owner in the commit record; no independent replication
L8  consequence for Run 2 -- if Run 2's rule selects C084 or C065, its analysis
    of that target is not blind to this study; the preregistration must say how
    that is handled and may not exclude the target by hand
L9  the termination rule's decisions are the owner's -- T1, T2, T3 each recorded
    with the owner's words (XQA-09, 10, 11); all three continued
```

## 4. The owner's reason for the target, as discretion

C084 was chosen by the owner because its E3 witness -- the savegame
version header written by `src/doom/p_saveg.c` and read back by
`src/doom/g_game.c` (EV-C084-E3-01) -- is the closest of the three
ELIGIBLE candidates to C4's persistent-provenance mechanism. That is
discretion, recorded as such (design Section 2.1, L1), and the study's
F3 is the finding that discretion was most likely to produce. The
other two ELIGIBLE candidates (C059, C065) were not analysed.

## 5. Inputs to Run 2

Each of the five inputs design Section 1 promised, as a Run 2
preregistration can cite it; none is a Run 2 result.

**5.1 The snapshot procedure as executed** (`pin_record.md`; design
4.2 steps 2-5). A depth-1 fetch of a bare commit id reproduced the
tree; ten pinned digests and the archive's byte count, sha256 and entry
count all matched the screening's pin after sixty days; the sealed-
instant check (`commits?sha=master&until=T`) returned a commit other
than the one the screening observed at master's tip four days after T.
Run 2 input (XQA-01): an API query for "master at instant T" is not a
snapshot procedure; a Run 2 snapshot rule must pin at observation time
and say so, or not claim the sealed instant at all. QA-28's gap is met
in the data, not closed.

**5.2 The inventory procedure as executed** (design Section 6;
`inventory_sources.tsv`, `inventory_enumerators.tsv`, `x4b_verdicts.py`,
`enumerator_bounds.tsv`):

```text
sources (S_doc)      42 candidates: REJECT 36, QUARANTINED 6, ADMIT 0 -- U_normative empty
enumerators          618 candidates: K1 525, K2 78, K3 0, K4 15 (generation 1: 596;
                     +22 anonymous-struct arrays after XQA-04)
admitted             23, all K1, all `enforced`
rejected             595: first failed criterion EN2 592, EN4 3
members              1141 initializer rows -> 1132 units (8 terminators, 1 out-of-bound)
time                 tools committed 15:06; candidates generated +2 min; regenerated
                     +10 min; all 618 verdicts written +22 min; P_raw frozen +28 min
                     (committer times; the inventory's reading of code for EN4
                     evidence is inside these minutes)
```

What Run 2 can take from it (XQA-05, 07, 08): the EN2 test rejected
592 of 618 candidates by the project's own identification of the set,
and would in any C codebase of this kind; the candidate-to-admission
ratio (618 : 23) is the cost of a registry-idiom inventory; membership
needs three exclusions a parser cannot see alone -- commented rows,
terminator rows, rows beyond the consulting loop's bound -- and the
third needs the loop read at inventory time; a pattern committed before
the run can still be wrong against its own class (XQA-04).

**5.3 Per-unit and per-native-case cost** (`cost_log.tsv`: session
time between the case's first reading and its commit, as logged; the
owner's review time is outside it):

```text
case    session s  units   s/unit   accepted (UTC)
NC-01       125     11    11.36   07:03:59
NC-02       216     17    12.71   07:08:44
NC-03        88     15     5.87   07:10:57
NC-04        63     16     3.94   07:12:50
NC-05        89     15     5.93   07:23:03
NC-06        90    946     0.10   07:48:54
NC-07        54      3    18.00   07:50:38
NC-08        74      9     8.22   07:55:07
NC-09        90     15     6.00   07:57:49
NC-10        77     21     3.67   08:01:17
NC-11        37     26     1.42   08:02:52
NC-12        72     30     2.40   08:07:12
NC-13        92      4    23.00   08:26:23
NC-14        92      4    23.00   08:26:23

session seconds   total 1259   min 37   median 88   max 216
seconds per unit  min 0.10   median 5.97   max 23.00   overall 1.11 (1259 s / 1132 units)
wall time of X9   06:55 .. 08:26, 14 cases, review included
```

The design's estimate was one to three hours per unit; the measured
grain is the native case, not the unit: a case cost a median 88 s of
session time whatever its unit count (NC-06's 946 units and NC-07's 3
cost 90 s and 54 s), because the units of one enumerator share one
consulting path. A Run 2 budget should be set per native case, with
the number of cases bounded above by the number of admitted
enumerators (here 14 cases from 23), and the per-unit figure read as a
distribution (0.10 to 23.00 s) rather than its 1.11 s mean.

**5.4 The KF-0 rule as applied** (`KF0.md`): tracker of record from
the project's own README; L from the label names alone (every API
description was empty), with the two single-word judgment calls
recorded; count 37, bounded; T2 attempt in full. Measured: KF-1 and
KF-2 for 37 items took 24 min of wall time (`4a79e22` .. `504d302`),
against the design's estimate of one to two hours per item. KF-3 for
37 items: 4 batches, each read (comments, timeline, linked commits)
and written in 4, 2, 4, 3 min (first read to the batch's commit), 13 min in
all, inside a wall time of 102 min whose remainder was spent waiting
on the tracker's unauthenticated API limit of 60 requests per hour.
The set is complete only within the project's labelling (fourteen
`bug` labels among issue numbers that reach #1043, numbers shared with
pull requests).

**5.5 The termination rule as executed** (design 7.1; XQA-09, 10, 11):

```text
T1  X7   input P_raw = 1132 (946 of them HHE offsets)          owner: proceed
         "진행, 끝까지 하기로 했으니까"
T2  X8   input KF count = 37                                  owner: attempt in full
         "전부 시도, 끝까지 하기로 했으니까"
T3  X9   input NC-01: 125 s / 11 units = 11.4 s per unit,     owner: continue
         projection 3.6 h over P_raw (a lower bound)          "통과, T3도 진행"
```

The rule was executable: each point had a defined input available
before anything downstream was read, and each decision is the owner's
in their own words. The projection at T3 overestimated by a factor of
about 10 (measured 1.11 s per unit against 11.4), for the reason in 5.3.

**5.6 Readings the sealed text left open.** The XQA entries that name
a rule the sealed text lacked, each recording the reading taken and
the one not taken, in place:

```text
XQA-02  candidate class K1 widened to any element type
XQA-03  reading of EN2 against EN4 fixed before any candidate is decided
XQA-05  the EN2 test and the EN4 test, stated before the first verdict; one XQA-03 example withdrawn
XQA-07  X4b outcome: 23 enumerators admitted, no authoritative source; sentinel rows; two observations
XQA-08  rows beyond the consulting loop's bound are not members; one X4b evidence sentence corrected
```

The other entries are a check result (XQA-01), a defect against a
committed pattern (XQA-04), an exposure incident (XQA-06), the three
termination decisions (XQA-09, 10, 11) and two acceptances (XQA-12,
13):

```text
XQA-01  sealed-instant consistency check returned DIFFERS
XQA-04  K1 pattern missed anonymous-struct arrays; candidate table regenerated
XQA-06  a scratch helper read five lines of a quarantined file
XQA-09  T1 decision: proceed
XQA-10  T2 decision: attempt the known-failure lane in full
XQA-11  T3 decision: continue
XQA-12  Artifact 2 accepted; Artifact 3 written
XQA-13  the owner opened the known-failure lane
XQA-14  X14 outcome: KF-3 compared for all 37 items; nothing above the KF-3 lines edited
```

## 6. What this study does not establish

It does not establish the Phase 3.5 result: the target was chosen by
hand and the revision is an observation-time pin (Section 1), so its
findings are what one hand-chosen system shows under the sealed
procedure, and Run 2's preregistration may cite its inputs (Section 5)
and may not be tuned to reproduce or avoid its findings (anti-goal 1).
It establishes nothing about C065, the parent project, although most
of the analysed code is inherited (L4). It makes no claim about
necessity from its one R0 (sealed 7.1), none about F2 (none supported;
13.2), none about the sealed instant (14.1), and none about search,
exploit discovery or executable witnesses (sealed Section 10). The
known-failure lane's 34 out-of-domain items say that the frozen
domain is narrow against this tracker's failures, not that the
judgment is wrong where it applies; its three concordant results are
three, not a rate. In the sealed methodology's closing words, which
bind this document as they bind the Phase 3.5 result:

> No result table may imply prevalence of architectural outcomes from
> this single target.
