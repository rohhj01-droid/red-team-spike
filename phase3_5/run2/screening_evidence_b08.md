# Screening batch 08 -- Run 2

Reviewed as one unit (contract Section 11). Rows are produced by `tools/screen.py` from the frozen
metadata, the recorded observations and the witness table `witness_b08.tsv`; the owner answers
통과 or names the rank that fails review.

| rank | port | UR | candidate | E1 | E2-REP | E2-RULE | E3 | E4 | terminal | stop gate | code |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 57 | games/candycrisis | PASS | C053 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 58 | games/capitan-sevilla | PASS | C054 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 59 | games/cataclysm-dda | PASS | C055 | PASS | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | E4 | PI-UNCLASSIFIED-SHAPE |
| 60 | games/cdogs-sdl | PASS | C056 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 61 | games/cgames | PASS | C057 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 62 | games/cgoban | PASS | C058 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |
| 63 | games/chessx | PASS | C059 | PASS | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-RULE | PI-UNCLASSIFIED-SHAPE |
| 64 | games/chiaki | PASS | C060 | PASS | UNRESOLVED | NOT_REACHED | NOT_REACHED | NOT_REACHED | UNRESOLVED | E2-REP | PI-UNCLASSIFIED-SHAPE |

## rank 57 -- games/candycrisis

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://github.com/jorio/CandyCrisis | HOMEPAGE+GH | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://github.com/jorio/CandyCrisis/archive/refs/tags/v3.0.1/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T06:00:36Z | 57 | https://github.com/jorio/CandyCrisis | landing page rendered a README (4343 chars of page text); not used | used: no |

## EV-C053-E1-01

Candidate: C053
Gate: E1
Source:   https://github.com/jorio/candycrisis

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C053-E2REP-02

Candidate: C053
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://github.com/jorio/CandyCrisis -> observed
           https://github.com/jorio/CandyCrisis/archive/refs/tags/v3.0.1/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://github.com/jorio/CandyCrisis

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 58 -- games/capitan-sevilla

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| http://computeremuzone.com/ficha.php?id=754&l=en | HOMEPAGE | unmatched | observed | project-page | 403 | official-project-page |
| http://computeremuzone.com/pc/juegos/ | SITES | unmatched | observed | distfile-location | 403 | distfile-location |

## EV-C054-E1-01

Candidate: C054
Gate: E1
Source:   https://computeremuzone.com/ficha.php

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C054-E2REP-02

Candidate: C054
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  http://computeremuzone.com/ficha.php?id=754&l=en -> observed (HTTP 403)
           http://computeremuzone.com/pc/juegos/ -> observed (HTTP 403)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 59 -- games/cataclysm-dda

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://cataclysmdda.org | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/CleverRaven/Cataclysm-DDA | DIST_TUPLE | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T06:00:40Z | 59 | https://github.com/CleverRaven/Cataclysm-DDA | landing page rendered a README (8340 chars of page text); not used | used: no |
| 2026-10-30T06:00:40Z | 59 | https://discord.gg/jFEc7Yp | step-2 link 'Development-oriented Discord': target is not a repository root (project-page); observed once, not read | used: no |
| 2026-10-30T06:00:38Z | 59 | https://github.com/CleverRaven/Cataclysm-DDA/issues/ | step-2 link 'our GitHub page' leads to a forbidden class; not followed | used: no |

## EV-C055-E1-01

Candidate: C055
Gate: E1
Source:   https://github.com/cleverraven/cataclysm-dda

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C055-E2REP-02

Candidate: C055
Gate: E2-REP
Source:   https://github.com/CleverRaven/Cataclysm-DDA

Surfaces:  https://cataclysmdda.org -> observed
           https://github.com/CleverRaven/Cataclysm-DDA -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitHub repository' at https://cataclysmdda.org -> https://github.com/CleverRaven/Cataclysm-DDA | identifier 'Cataclysm-DDA' (the repository's name, contract 6) appears on https://github.com/CleverRaven/Cataclysm-DDA | tree pinned at a82c4a73acc322383fbf4b26227c284856785731 (10468 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C055-E2RULE-03

Candidate: C055
Gate: E2-RULE
Source:   doc/design-balance-lore/design-balance.md:107

Observed: "Melee combat will always place the player in harm's way"

Inference: a quoted, located validity witness (contract Section 8)

Decision: PASS

## EV-C055-E3-04

Candidate: C055
Gate: E3
Source:   doc/design-balance-lore/design-balance.md:150

Observed: 'over time this will lead to decay of its structure that cannot be restored to mint condition'

Inference: a quoted, located stateful witness (contract Section 8)

Decision: PASS

## EV-C055-E4-05

Candidate: C055
Gate: E4
Source:   the frozen grammar over 328 candidate rows

Surfaces:  src/cata_imgui.cpp:47
           src/sdltiles.cpp:4769
           src/third-party/flatbuffers/idl_parser.cpp:43
           src/third-party/imgui/imgui.cpp:3690
           src/third-party/imgui/imgui.cpp:4223
           src/third-party/imgui/imgui.cpp:6950
           src/third-party/imgui/imgui.cpp:6965
           src/third-party/imgui/imgui.cpp:9587
           src/third-party/imgui/imgui_demo.cpp:2556
           src/third-party/imgui/imgui_draw.cpp:2657
           src/third-party/imgui/imgui_draw.cpp:5516
           src/third-party/imgui/imgui_draw.cpp:5517
           src/third-party/imgui/imgui_widgets.cpp:2383
           src/third-party/imgui/imgui_widgets.cpp:2388
           src/third-party/imtui/imtui-impl-ncurses.cpp:427
           src/third-party/zstd/common/zstd_internal.h:67
           src/third-party/zstd/common/zstd_internal.h:81
           src/third-party/zstd/common/zstd_internal.h:82
           src/third-party/zstd/common/zstd_internal.h:121
           src/third-party/zstd/common/zstd_internal.h:128
           src/third-party/zstd/common/zstd_internal.h:138
           src/third-party/zstd/common/zstd_internal.h:147
           src/third-party/zstd/common/zstd_internal.h:159
           src/third-party/zstd/compress/clevels.h:27
           src/third-party/zstd/compress/zstd_ldm_geartab.h:17
           src/third-party/zstd/decompress/huf_decompress.c:1794
           src/third-party/zstd/decompress/zstd_decompress_block.c:364
           src/third-party/zstd/decompress/zstd_decompress_block.c:402
           src/third-party/zstd/decompress/zstd_decompress_block.c:425
           src/third-party/zstd/decompress/zstd_decompress_internal.h:30
           src/third-party/zstd/decompress/zstd_decompress_internal.h:37
           src/third-party/zstd/decompress/zstd_decompress_internal.h:43
           src/third-party/zstd/decompress/zstd_decompress_internal.h:49
           CONTRIBUTING.md:276
           CONTRIBUTING.md:372
           ISSUES.md:11
           LICENSE-Apache-Robot-Font.txt:11
           Makefile:83
           Makefile:1498
           SIGNOFF:1
           build-data/osx/LICENSE-libiconv.txt:170
           build-data/osx/LICENSE-libiconv.txt:276
           build-data/osx/LICENSE-libiconv.txt:495
           data/json/LOADING_ORDER.md:1
           data/json/LOADING_ORDER.md:32
           data/mods/BombasticPerks/docs/contributing.md:18
           data/mods/DinoMod/DESIGN.md:56
           data/mods/Magiclysm/magic_balance.md:75
           data/mods/MindOverMatter/GainingPowerSpoilers.md:35
           data/mods/MindOverMatter/NewPowerGuide.md:11
           data/mods/MindOverMatter/PowerDescriptionSpoilers.md:231
           data/mods/MindOverMatter/PowerDescriptionSpoilers.md:672
           data/mods/MindOverMatter/PowerDescriptionSpoilers.md:695
           data/mods/MindOverMatter/PowerDescriptionSpoilers.md:849
           data/mods/MindOverMatter/PowerDescriptionSpoilers.md:993
           data/mods/MindOverMatter/PowerDescriptionSpoilers.md:1008
           data/mods/No_Hope/CONTRIBUTING.md:12
           data/mods/Sky_Island/README.md:18
           data/mods/Sky_Island/README.md:58
           data/mods/Sorcerer/README.md:44
           data/mods/Xedra_Evolved/README.md:1
           data/mods/Xedra_Evolved/README.md:2
           data/mods/Xedra_Evolved/design_doc_spoilers.md:81
           data/mods/aftershock_exoplanet/doc/lore/factions.md:3
           data/mods/aftershock_exoplanet/doc/lore/factions.md:69
           data/mods/aftershock_exoplanet/doc/lore/organizations.md:1
           data/mods/aftershock_exoplanet/doc/lore/organizations.md:25
           data/mods/aftershock_exoplanet/doc/lore/ranged_weapon_balance.md:1
           data/mods/aftershock_exoplanet/items/armor/exosuit/exosuit_guide.md:11
           data/mods/classic_zombies/design-doc.md:23
           data/mods/hunvre/documentation/lore.md:37
           doc/DEVELOPER_FAQ.md:120
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:77
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:109
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:133
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:312
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:333
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:339
           doc/FREQUENTLY_MADE_SUGGESTIONS.md:379
           doc/GUN_NAMING_AND_INCLUSION.md:68
           doc/GUN_NAMING_AND_INCLUSION.md:123
           doc/JSON/ARTIFACTS.md:79
           doc/JSON/ARTIFACTS.md:142
           doc/JSON/BASECAMP.md:61
           doc/JSON/BASECAMP.md:259
           doc/JSON/DIMENSIONS.md:69
           doc/JSON/EFFECTS_JSON.md:149
           doc/JSON/EFFECTS_JSON.md:435
           doc/JSON/EFFECTS_JSON.md:622
           doc/JSON/EFFECT_ON_CONDITION.md:1427
           doc/JSON/EFFECT_ON_CONDITION.md:1840
           doc/JSON/EFFECT_ON_CONDITION.md:1843
           doc/JSON/EFFECT_ON_CONDITION.md:2212
           doc/JSON/EFFECT_ON_CONDITION.md:2219
           doc/JSON/EFFECT_ON_CONDITION.md:2393
           doc/JSON/EFFECT_ON_CONDITION.md:2654
           doc/JSON/EFFECT_ON_CONDITION.md:2850
           doc/JSON/EFFECT_ON_CONDITION.md:2902
           doc/JSON/EFFECT_ON_CONDITION.md:2982
           doc/JSON/EFFECT_ON_CONDITION.md:3684
           doc/JSON/EFFECT_ON_CONDITION.md:3719
           doc/JSON/EFFECT_ON_CONDITION.md:4212
           doc/JSON/EFFECT_ON_CONDITION.md:4465
           doc/JSON/EFFECT_ON_CONDITION.md:5124
           doc/JSON/EFFECT_ON_CONDITION.md:5216
           doc/JSON/EFFECT_ON_CONDITION.md:5700
           doc/JSON/EXAMINE.md:140
           doc/JSON/EXAMINE.md:168
           doc/JSON/EXAMINE.md:174
           doc/JSON/ITEM.md:191
           doc/JSON/ITEM.md:283
           doc/JSON/ITEM.md:284
           doc/JSON/ITEM.md:623
           doc/JSON/ITEM.md:680
           doc/JSON/ITEM.md:825
           doc/JSON/ITEM.md:845
           doc/JSON/ITEM.md:857
           doc/JSON/ITEM.md:860
           doc/JSON/ITEM.md:905
           doc/JSON/ITEM.md:972
           doc/JSON/ITEM.md:1021
           doc/JSON/ITEM.md:1022
           doc/JSON/ITEM.md:1161
           doc/JSON/ITEM.md:1309
           doc/JSON/ITEM.md:1316
           doc/JSON/ITEM.md:1570
           doc/JSON/ITEM_CRAFT_AND_DISASSEMBLY.md:195
           doc/JSON/ITEM_CRAFT_AND_DISASSEMBLY.md:371
           doc/JSON/ITEM_CRAFT_AND_DISASSEMBLY.md:504
           doc/JSON/ITEM_CRAFT_AND_DISASSEMBLY.md:759
           doc/JSON/ITEM_SPAWN.md:23
           doc/JSON/ITEM_SPAWN.md:56
           doc/JSON/ITEM_SPAWN.md:58
           doc/JSON/ITEM_SPAWN.md:177
           doc/JSON/JSON_FLAGS.md:1514
           doc/JSON/JSON_INFO.md:260
           doc/JSON/JSON_INFO.md:269
           doc/JSON/JSON_INFO.md:430
           doc/JSON/JSON_INFO.md:675
           doc/JSON/JSON_INFO.md:1009
           doc/JSON/JSON_INFO.md:1012
           doc/JSON/JSON_INFO.md:1620
           doc/JSON/JSON_INFO.md:1865
           doc/JSON/JSON_INFO.md:2343
           doc/JSON/JSON_INFO.md:2438
           doc/JSON/JSON_INFO.md:2450
           doc/JSON/JSON_INFO.md:2765
           doc/JSON/JSON_INFO.md:3572
           doc/JSON/JSON_INFO.md:4135
           doc/JSON/JSON_INFO.md:4375
           doc/JSON/JSON_INFO.md:4429
           doc/JSON/JSON_INFO.md:4450
           doc/JSON/JSON_INFO.md:4592
           doc/JSON/JSON_INFO.md:4617
           doc/JSON/JSON_INHERITANCE.md:81
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:21
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:46
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:57
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:93
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:223
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:223
           doc/JSON/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md:252
           doc/JSON/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md:22
           doc/JSON/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md:149
           doc/JSON/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md:270
           doc/JSON/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md:371
           doc/JSON/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md:598
           doc/JSON/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md:604
           doc/JSON/JSON_STYLE.md:63
           doc/JSON/JSON_STYLE.md:74
           doc/JSON/JSON_STYLE.md:97
           doc/JSON/JSON_TOOLS.md:25
           doc/JSON/JSON_TOOLS.md:138
           doc/JSON/JSON_TOOLS.md:142
           doc/JSON/MAGIC.md:155
           doc/JSON/MAGIC.md:207
           doc/JSON/MAGIC.md:209
           doc/JSON/MAPGEN.md:100
           doc/JSON/MAPGEN.md:101
           doc/JSON/MAPGEN.md:310
           doc/JSON/MAPGEN.md:621
           doc/JSON/MAPGEN.md:659
           doc/JSON/MAPGEN.md:681
           doc/JSON/MAPGEN.md:778
           doc/JSON/MAPGEN.md:1194
           doc/JSON/MAPGEN.md:1527
           doc/JSON/MAP_SMASHING.md:7
           doc/JSON/MAP_SMASHING.md:17
           doc/JSON/MARTIALART_JSON.md:274
           doc/JSON/MISSIONS_JSON.md:156
           doc/JSON/MISSIONS_JSON.md:273
           doc/JSON/MONSTER_SPECIAL_ATTACKS.md:27
           doc/JSON/MONSTER_SPECIAL_ATTACKS.md:236
           doc/JSON/MOVE_MODE.md:141
           doc/JSON/MUTATIONS.md:40
           doc/JSON/MUTATIONS.md:64
           doc/JSON/MUTATIONS.md:66
           doc/JSON/MUTATIONS.md:83
           doc/JSON/MUTATIONS.md:93
           doc/JSON/MUTATIONS.md:101
           doc/JSON/NPCs.md:84
           doc/JSON/NPCs.md:247
           doc/JSON/NPCs.md:293
           doc/JSON/NPCs.md:893
           doc/JSON/NPCs.md:924
           doc/JSON/NPCs.md:926
           doc/JSON/NPCs.md:949
           doc/JSON/NPCs.md:952
           doc/JSON/NPCs.md:956
           doc/JSON/NPCs.md:998
           doc/JSON/NPCs.md:1412
           doc/JSON/NPCs.md:1431
           doc/JSON/NPCs.md:1432
           doc/JSON/NPCs.md:1473
           doc/JSON/OBSOLETION_AND_MIGRATION.md:41
           doc/JSON/OVERMAP.md:152
           doc/JSON/OVERMAP.md:163
           doc/JSON/OVERMAP.md:287
           doc/JSON/OVERMAP.md:337
           doc/JSON/OVERMAP.md:498
           doc/JSON/OVERMAP.md:499
           doc/JSON/OVERMAP.md:586
           doc/JSON/OVERMAP.md:655
           doc/JSON/OVERMAP.md:665
           doc/JSON/OVERMAP.md:869
           doc/JSON/OVERMAP.md:1054
           doc/JSON/PROFICIENCY.md:141
           doc/JSON/REGION_LAYOUT.md:103
           doc/JSON/REGION_SETTINGS.md:17
           doc/JSON/REGION_SETTINGS.md:81
           doc/JSON/REGION_SETTINGS.md:404
           doc/JSON/VEHICLES_JSON.md:40
           doc/JSON/VEHICLES_JSON.md:119
           doc/JSON/VEHICLES_JSON.md:122
           doc/JSON/VITAMIN.md:100
           doc/JSON/VITAMIN.md:101
           doc/JSON/VITAMIN.md:105
           doc/JSON/VITAMIN.md:106
           doc/JSON/VITAMIN.md:111
           doc/JSON/WOUNDS.md:43
           doc/MANUAL_OF_STYLE.md:14
           doc/MODDING.md:33
           doc/MODDING.md:196
           doc/MODDING.md:366
           doc/PLAYER_ACTIVITY.md:25
           doc/SOUNDPACKS.md:182
           doc/TILESET.md:185
           doc/TILESET.md:224
           doc/TILESET.md:489
           doc/TILESET.md:674
           doc/TILESET.md:698
           doc/TILESET.md:786
           doc/TRANSLATING.md:155
           doc/TRANSLATING.md:414
           doc/TRANSLATING_MOD.md:33
           doc/WIDGETS.md:63
           doc/WIDGETS.md:169
           doc/WIDGETS.md:610
           doc/WIDGETS.md:718
           doc/c++/CODE_STYLE.md:1
           doc/c++/COMPILING-DEVCONTAINER.md:84
           doc/c++/COMPILING.md:341
           doc/c++/COMPILING.md:724
           doc/c++/DEVELOPER_TOOLING.md:130
           doc/c++/JSON_INTERFACE.md:253
           doc/c++/JSON_INTERFACE.md:657
           doc/c++/TESTING.md:92
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:175
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:193
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:239
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:317
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:361
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:655
           doc/design-balance-lore/ARMOR_BALANCE_AND_DESIGN.md:789
           doc/design-balance-lore/CONSTRUCTION_BALANCE.md:37
           doc/design-balance-lore/GAME_BALANCE.md:273
           doc/design-balance-lore/LORE_FAQ.md:62
           doc/design-balance-lore/design-balance.md:81
           doc/design-balance-lore/design-balance.md:104
           doc/design-balance-lore/design-user-experience.md:214
           doc/design-balance-lore/lore-background.md:41
           doc/design-balance-lore/lore-background.md:101
           doc/design-balance-lore/lore-factions.md:439
           doc/design-balance-lore/lore-factions.md:513
           doc/design-balance-lore/lore-factions.md:553
           doc/design-balance-lore/lore-factions.md:565
           doc/design-balance-lore/lore-factions.md:602
           doc/design-balance-lore/melee_weapons/MELEE_BALANCE_SPREADSHEET.md:57
           doc/design-balance-lore/melee_weapons/MELEE_BALANCE_SPREADSHEET.md:84
           doc/development_process.md:187
           doc/reviewing_PR_guide.md:34
           doc/reviewing_PR_guide.md:54
           doxygen_doc/doxygen_conf.txt:4
           doxygen_doc/doxygen_conf.txt:13
           doxygen_doc/doxygen_conf.txt:61
           doxygen_doc/doxygen_conf.txt:69
           doxygen_doc/doxygen_conf.txt:96
           doxygen_doc/doxygen_conf.txt:109
           doxygen_doc/doxygen_conf.txt:418
           doxygen_doc/doxygen_conf.txt:427
           doxygen_doc/doxygen_conf.txt:434
           doxygen_doc/doxygen_conf.txt:439
           doxygen_doc/doxygen_conf.txt:473
           doxygen_doc/doxygen_conf.txt:866
           doxygen_doc/doxygen_conf.txt:929
           doxygen_doc/doxygen_conf.txt:1525
           doxygen_doc/doxygen_conf.txt:1616
           doxygen_doc/doxygen_conf.txt:1626
           doxygen_doc/doxygen_conf.txt:1706
           doxygen_doc/doxygen_conf.txt:1712
           doxygen_doc/doxygen_conf.txt:1718
           lang/notes/README_all_translators.md:78
           lang/notes/README_all_translators.md:97
           src/third-party/snmalloc/README.md:4
           src/third-party/zstd/README.md:58
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: catalogue decided 13 rows, 315 undecided, none admitted

Inference: no quoted ADMIT -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 60 -- games/cdogs-sdl

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://cxong.github.io/cdogs-sdl/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/cxong/cdogs-sdl/archive/refs/tags/2.1.0/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/cxong/cdogs-sdl | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T06:02:11Z | 60 | https://github.com/cxong/cdogs-sdl | landing page rendered a README (6222 chars of page text); not used | used: no |
| 2026-10-30T06:02:11Z | 60 | https://github.com/cxong/cdogs-sdl/releases/tag/2.5.0 | step-2 link 'https://github.com/cxong/cdogs-sdl/releases/tag/2.5.0' leads to a forbidden class; not followed | used: no |
| 2026-10-30T06:02:11Z | 60 | https://github.com/cxong/cdogs-sdl/releases/tag/2.4.0 | step-2 link 'https://github.com/cxong/cdogs-sdl/releases/tag/2.4.0' leads to a forbidden class; not followed | used: no |
| 2026-10-30T06:02:11Z | 60 | https://github.com/cxong/cdogs-sdl/releases/tag/2.3.2 | step-2 link 'https://github.com/cxong/cdogs-sdl/releases/tag/2.3.2' leads to a forbidden class; not followed | used: no |
| 2026-10-30T06:02:11Z | 60 | https://github.com/cxong/cdogs-sdl/releases/tag/2.3.1 | step-2 link 'https://github.com/cxong/cdogs-sdl/releases/tag/2.3.1' leads to a forbidden class; not followed | used: no |

## EV-C056-E1-01

Candidate: C056
Gate: E1
Source:   https://github.com/cxong/cdogs-sdl

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C056-E2REP-02

Candidate: C056
Gate: E2-REP
Source:   https://github.com/cxong/cdogs-sdl

Surfaces:  https://cxong.github.io/cdogs-sdl/ -> observed
           https://github.com/cxong/cdogs-sdl/archive/refs/tags/2.1.0/ -> closed-by-class (forbidden class, never requested)
           https://github.com/cxong/cdogs-sdl -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'GitHub' at https://cxong.github.io/cdogs-sdl/ -> https://github.com/cxong/cdogs-sdl | identifier 'cdogs-sdl' (the repository's name, contract 6) appears on https://cxong.github.io/cdogs-sdl/ | tree pinned at c70d1feaf9d89cf80e23265b256d9a364848e6ea (4661 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C056-E2RULE-03

Candidate: C056
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.md
           doc/README_DATA.md
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.md, doc/README_DATA.md

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 61 -- games/cgames

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://www.muppetlabs.com/~breadbox/software/cgames.html | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://www.muppetlabs.com/~breadbox/pub/software/ | SITES | unmatched | observed | distfile-location | 200 | distfile-location |

## EV-C057-E1-01

Candidate: C057
Gate: E1
Source:   https://www.muppetlabs.com/~breadbox/software/cgames.html

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C057-E2REP-02

Candidate: C057
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://www.muppetlabs.com/~breadbox/software/cgames.html -> observed
           https://www.muppetlabs.com/~breadbox/pub/software/ -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 62 -- games/cgoban

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://cgoban1.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://downloads.sourceforge.net/sourceforge/cgoban1/ | SITES | distfile-location | observed | distfile-location | 404 | distfile-location |

| 2026-10-30T06:02:41Z | 62 | http://sourceforge.net/project/showfiles.php?group_id=52805 | step-2 link 'Sourceforge Download page for the latest release (1.9.13)': target is not a repository root (distfile-location); observed once, not read | used: no |

## EV-C058-E1-01

Candidate: C058
Gate: E1
Source:   https://cgoban1.sourceforge.net

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C058-E2REP-02

Candidate: C058
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://cgoban1.sourceforge.net/ -> observed
           https://downloads.sourceforge.net/sourceforge/cgoban1/ -> observed (HTTP 404)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: none

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED


## rank 63 -- games/chessx

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://chessx.sourceforge.net/ | HOMEPAGE | unmatched | observed | project-page | 200 | official-project-page |
| https://github.com/Isarhamster/chessx/archive/refs/tags/v1.5.6-lw/ | SITES | release-assets | closed-by-class | release-assets |  |  |
| https://github.com/Isarhamster/chessx | GH | repository-root | observed | repository-root | 200 | official-source-location |

| 2026-10-30T06:02:44Z | 63 | https://github.com/Isarhamster/chessx | landing page rendered a README (4825 chars of page text); not used | used: no |
| 2026-10-30T06:02:44Z | 63 | https://chessx.sourceforge.io | step-2 link 'Sourceforge': target is not a repository root (project-page); observed once, not read | used: no |

## EV-C059-E1-01

Candidate: C059
Gate: E1
Source:   https://github.com/isarhamster/chessx

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C059-E2REP-02

Candidate: C059
Gate: E2-REP
Source:   https://github.com/Isarhamster/chessx

Surfaces:  https://chessx.sourceforge.net/ -> observed
           https://github.com/Isarhamster/chessx/archive/refs/tags/v1.5.6-lw/ -> closed-by-class (forbidden class, never requested)
           https://github.com/Isarhamster/chessx -> observed
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: link label 'Source Code' at https://chessx.sourceforge.io/ -> https://github.com/Isarhamster/chessx | link label 'Source' at https://chessx.sourceforge.io/ -> https://github.com/Isarhamster/chessx | identifier 'chessx' (the repository's name, contract 6) appears on https://chessx.sourceforge.io/ | tree pinned at c7d815796e977c1ededef515d6db00bff326bd8d (764 tracked files)

Inference: exactly one designated canonical location and one identifier on observed surfaces; the source tree is present (contract Section 7); step-2 links followed by the label rule only (Section 6; a label-authorized link into the repository is the project's own designation, RQA-02)

Decision: PASS

## EV-C059-E2RULE-03

Candidate: C059
Gate: E2-RULE
Source:   the contract's E2-RULE surfaces

Surfaces:  README.developers.md
           README.md
           tests/
Necessary because: a positive-only gate is left UNRESOLVED only after the surfaces the contract names
  for it are read (contract Section 8); each line above is a surface read.

Observed: no validity witness quoted; surfaces read: README.developers.md, README.md, tests/

Inference: positive-only PASS; nothing located -> UNRESOLVED, never FAIL (Run 1's amendment)

Decision: UNRESOLVED


## rank 64 -- games/chiaki

| url | source | class | action | final class | status | role |
|---|---|---|---|---|---|---|
| https://git.sr.ht/~thestr4ng3r/chiaki | HOMEPAGE | repository-root | observed | repository-root | 200 | admitted-starting-point |
| https://git.sr.ht/~thestr4ng3r/chiaki/refs/download/v2.2.0/ | SITES | release-assets | closed-by-class | release-assets |  |  |

| 2026-10-30T06:02:55Z | 64 | https://git.sr.ht/~thestr4ng3r/chiaki | landing page rendered a README (5462 chars of page text); not used | used: no |

## EV-C060-E1-01

Candidate: C060
Gate: E1
Source:   https://git.sr.ht/~thestr4ng3r/chiaki

Observed: identity key outside this project's namespace

Inference: E1 external authorship (contract Section 3)

Decision: PASS

## EV-C060-E2REP-02

Candidate: C060
Gate: E2-REP
Source:   the starting-point set (contract Section 4)

Surfaces:  https://git.sr.ht/~thestr4ng3r/chiaki -> observed
           https://git.sr.ht/~thestr4ng3r/chiaki/refs/download/v2.2.0/ -> closed-by-class (forbidden class, never requested)
Necessary because: the gate's question needs every admitted starting point accounted for
  (contract Section 7); each line above is its accounting.

Observed: no designation witness on any observed surface; observed roots: https://git.sr.ht/~thestr4ng3r/chiaki

Inference: the gate cannot complete: a PASS needs a designation witness and a failure code needs positive evidence (contract Section 7) -> PI-UNCLASSIFIED-SHAPE

Decision: UNRESOLVED
