# Primary-lane result -- EXPLORATORY C084 study (X11, the primary seal)

EXPLORATORY. This is the sealed result of the primary lane of the
exploratory study of C084 Crispy Doom at revision
`7775ef82d1e9dfd50eb9d2824acefaeff7247458`, under the sealed Phase 3.5
methodology's analysis lane with the two substitutions of the design
(Section 2.1). It is not the Phase 3.5 result and never stands in for
Run 2's (design anti-goal 1). Every number below is recomputed from
`P_raw.tsv`, `units.tsv` and the artifacts by `tools/checks.py`; the
known-failure lane (X12-X14) has not been opened at this commit.

## 1. Coverage (sealed §5.1, §8.2)

```text
resolved 1132 / P_raw 1132
E? 0 / P_raw 1132
O_raw 1132   linked units 0   enumerators 23, all tagged enforced
```

Every preregistered primary counting unit was analysed (sealed §8.6:
no optional stopping; design anti-goal 2). The E? list required by
sealed §8.2 is empty: no counting unit lacked a located answer to any
of the five sufficiency questions.

## 2. Findings per native case and per counting unit (sealed §7.0, §14 item 7)

| finding | native cases | counting units |
|---|---|---|
| R0 | 1 | 15 |
| F0 | 9 | 1061 |
| F1 | 3 | 41 |
| F2 | 0 | 0 |
| F3 | 1 | 15 |

A case carrying two findings would be counted under both and never
split; none does. No prevalence is inferred from either column
(sealed §5.1, §14).

```text
NC-01  F1      11 units  U001..U011  the launcher's IWAD slots, keyed by the standard IWAD filename (pkg/os
NC-02  F0      17 units  U012..U028  the IWAD registry: identifying the game's IWAD by its filename (src/d_
NC-03  R0      15 units  U029..U043  valid game mode/mission combinations, with their episode and map count
NC-04  F0      16 units  U044..U059  valid mission/version pairs for a network game (src/d_mode.c)
NC-05  F3      15 units  U060..U1128  the emulated game version: `-gameversion` against the supported list, 
NC-06  F0     946 units  U071..U1016  HHE text replacement: string offsets that are valid but unsupported, p
NC-07  F0       3 units  U1017..U1019  the HHE patch version: `-hhever` against the valid Heretic versions (s
NC-08  F1       9 units  U1020..U1028  which weapons may be selected in the Heretic shareware game (src/heret
NC-09  F0      15 units  U1031..U1045  the MAPINFO commands Hexen's map-information parser accepts (src/hexen
NC-10  F1      21 units  U1046..U1066  which sound devices each sound and music module supports, and how the 
NC-11  F0      26 units  U1067..U1092  game options a dedicated server refuses to accept on its own command l
NC-12  F0      30 units  U1093..U1122  known joysticks: which controllers the setup tool recognises and confi
NC-13  F0       4 units  U1123..U1126  the games the setup tool configures: `-game` against the four mission 
NC-14  F0       4 units  U1129..U1132  lumps unique to each game, used to refuse an IWAD run under the wrong 
```

## 3. The counterexamples and their basis (sealed §8.1, §8.3, §14 item 8)

A counterexample to the Phase 3 architecture exists in this target:
sealed §8.1 needs one valid F1/F2/F3 witness, and four native cases
carry one. Each rests on located native evidence (Artifact 1) and the
reasoning of Artifact 2:

```text
NC-01  F1  the launcher keeps a recognised IWAD as the slot's path; the
           launch judges only that a slot is selected -- provenance in
           ordinary state (pkg/osx/IWADController.m:425-431, :258-264;
           pkg/osx/LauncherManager.m:278-289)
NC-08  F1  the shareware weapon gate is a predicate over current state
           evaluated at the request; the judgment role collapses into a
           state predicate (src/heretic/p_user.c:662-675)
NC-10  F1  the sound module pointer carries the device selection's
           outcome; every later call judges on its presence
           (src/i_sound.c:133-203, :291-373)
NC-05  F3  Doom persists the version under which a save or demo was
           written as a fact, written by the action and judged only at
           consumption, owned by the artifact -- the reverse of Phase 3's
           judgment-written verdict (src/doom/p_saveg.c:1426-1476;
           src/doom/g_game.c:3209-3216, :3341-3366); scoped to U060-U070
```

One case retains a boundary against a named competitor (NC-03, R0:
the session-level record the connect judgment adopts and later
judgments read; competitor and discriminating evidence in Artifact 2).
Nine cases are input validations that pose no boundary question (F0).
No F2 was supported; sealed §13.2 (F2 may be under-observed in
systems with explicit enumeration mechanisms) applies to this target
as written.

## 4. Absence and retention wording (sealed §8.4, §8.5, §14 item 9)

Sealed §8.4 governs the case of NO counterexample; it does not apply:
counterexamples were observed. What may be said about retention is
scoped as sealed §8.2 requires: among the native cases recovered from
the 1132 / 1132 preregistered primary counting units that passed the
sufficiency gate, one case (NC-03) positively retains the provenance
boundary, nine neither retain nor contradict any boundary, and four
contradict one. Every admitted enumerator is tagged `enforced`, so no
absence wording needs weakening to an asserted scope (sealed §8.4,
§3.3). R0 is corroboration from one case, never proof of necessity
(sealed §7.1).

## 5. Correspondence and the collapsed count (sealed §4.3, §5.1, §14 item 6)

```text
matched                              0   (no normative source was admitted, XQA-07 b)
normative-only                       0
enforcement-only                  1132   every counting unit
divergent                            0
externally-linked                    0   (no cross-link edge; linked units 0)
analyst-inferred correspondence     14   many-to-one: units -> native cases, recorded in units.tsv
one-to-many                          0   no unit resolved into more than one native case
C (distinct native cases)           14
```

`C` never replaces `P_raw` as the denominator; it is reported beside
it. The largest collapse is NC-06: 946 counting units (83.6% of
P_raw) are one native case, because the three HHE lists segment by
offset (sealed §13.4: the external segmentation sets P_raw).

## 6. Counting units per enumerator (sealed §14 items 2 and 3)

```text
C013     11
C017     17
C022     15
C023     16
C034     11
C186    336
C187    305
C188    305
C191      3
C268      9
C313      2
C364     15
C403      1
C410      2
C412      1
C413      6
C414      6
C426      5
C434     26
C455     30
C464      4
C499      2
C595      4
```

The admitted enumerators, their EN1-EN6 evidence and their
`enforced` tags are in `inventory_enumerators.tsv`; the sources
examined and rejected for the normative route are in
`inventory_sources.tsv`; the frozen units in `P_raw.tsv` (`5f0f491`).

## 7. What this seal fixes

Artifacts 1 (`7b56ded`), 2 (`bc6361d`) and 3 (`3d44781`) and this
result are frozen before any known-failure item is opened (sealed §9,
§11; design Section 10). Nothing in `ARTIFACT_1_native.md`,
`ARTIFACT_2_mapping.md`, `ARTIFACT_3_judgment.md`, `units.tsv`,
`E_LOG.md` or this file is edited after this commit; a correction, if
one is ever needed, is a new entry in `EXECUTION_QA.md` and a new
file, never an edit here. The target was chosen by hand for the shape
of NC-05's mechanism (design L1): the F3 finding on that mechanism was
looked for, not found by chance, and is reported as such.
