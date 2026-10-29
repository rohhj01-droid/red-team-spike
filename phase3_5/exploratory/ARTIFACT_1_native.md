# Artifact 1 -- native description -- EXPLORATORY C084 study

EXPLORATORY. One entry per native case, in the target's own vocabulary,
at revision `7775ef82d1e9dfd50eb9d2824acefaeff7247458` (pin_record.md).
No Phase 3 role name appears in this file; it is written in the target's
own vocabulary (sealed §9, Artifact 1). Each entry carries the nine
Artifact 1 fields, the lineage line (design L4), and the five
sufficiency questions of sealed §6 answered with a file and line at the
frozen revision or an evidenced N/A (sealed §6.0). A case is `E?` when
a question has no located answer (sealed §6.1), and its gaps are named.
Entries are added in `P_raw.tsv` order and committed per native case.

## NC-01 -- the launcher's IWAD slots, keyed by the standard IWAD filename (pkg/osx)
source observation ids: E013-001, E013-002, E013-003, E013-004, E013-005, E013-006, E013-007, E013-008, E013-009, E013-010, E013-011 (units U001-U011)
native state/data involved: eleven IWAD "slots", one per IWAD type of the launcher's enum (pkg/osx/IWADController.m:22-36), each an NSPathControl in the configuration window (IWADController.h:26-37; getIWADList pkg/osx/IWADController.m:71-84) holding a file URL or nothing; the dropdown iwadSelector listing the configured types by label (:204-241); and the persistent copy of every slot in NSUserDefaults under the key that is the type's standard filename (IWADFilenames[i], :258-264) plus the key "selected_iwad" holding the selected type's filename (:268-270)
writers / creation points: (1) setIWADConfig at nib load (:147-171) restores each slot's URL from user defaults keyed by the filename (:161-170); (2) addIWADPath (:410-444), reached from the application's openFile handler (pkg/osx/AppController.m:77-88): a file whose last path component equals, case-insensitively, one of the eleven filenames (:422-427) fills the matching slot (:431) and becomes the selection (:435-436); a file matching none is not an IWAD to the launcher (:441-443, return NO) and AppController treats it as a command-line file instead (:90-96); (3) the user editing a path control in the configuration window (AppKit behaviour, outside the tree) followed by closeConfigWindow (:286-291)
updates / invalidation paths: saveConfig (:243-271) writes all eleven slot paths and the selected filename to user defaults; it runs before every launch (pkg/osx/LauncherManager.m:276), before the setup tool (:306), before a terminal (:327), on configuration-window close (IWADController.m:289) and on quit (LauncherManager.m:22-24). No code path clears a slot; nothing in the launcher reads the file at the path or checks its content -- a slot holds whatever path was restored, dropped or typed. The filename test is applied only on the openFile route (:425-427), not to a path typed into a slot
readers / consumption points: getIWADLocation (:103-120) returns the selected type's slot path, nil when no type is selected (:110-113); launch: (LauncherManager.m:269-297) -- nil raises the panel "No IWAD selected ... You must configure and select a valid IWAD file" (:281-289), otherwise the path is written to the response file as -iwad "<path>" (pkg/osx/Execute.m:48-57) and the executable for the type (getGameName :142-145 -> NameForIWAD :122-138: heretic, hexen, strife, else doom) is exec'd (LauncherManager.m:291-296; Execute.m:92-116); doomWadPath (:312-361) joins every configured slot into DOOMWADPATH for the setup tool and the terminal (:387-405; LauncherManager.m:307, :329); autoloadPath (:363-382) uses the selected filename as an autoload directory name; selectGameByName (:446-479) selects a configured slot by game name; setDropdownList (:204-241) lists the slots that hold a path
lifetime / persistence / reset behavior: a slot's path lives in the UI object for the launcher process and in NSUserDefaults across launcher runs (written :258-264, read :161-170); it survives being consumed by a launch (saveConfig precedes the exec :276 and the launcher terminates :296 without clearing anything); the only reset is the user emptying a path control; the standard filename is the slot's identity in the defaults store, and the selected type is remembered by that filename (:268-270, :182-198)
relevant transitions: nib load -> slots restored from defaults; file opened with the application -> name matched against the eleven filenames, slot filled, selection set; configuration window closed -> saved, dropdown rebuilt; launch -> selected slot read, -iwad "<path>" and the per-type executable handed to the game process; setup tool / terminal -> DOOMWADPATH built from all configured slots
supporting source-code/docs evidence: pkg/osx/IWADController.h:21-54; pkg/osx/IWADController.m:22-67, :71-120, :122-171, :204-271, :286-307, :312-405, :410-444, :446-479; pkg/osx/LauncherManager.m:22-36, :269-297, :301-334, :399-407; pkg/osx/AppController.m:77-96; pkg/osx/Execute.m:48-62, :92-116
remaining native-level uncertainty: the NSPathControl editing behaviour and the .nib wiring are AppKit / binary, outside the tree; nothing was found that checks a slot's file content or re-checks a path at launch -- what the game process does with -iwad "<path>" is the engine's own identification (d_iwad.c), a different native case
lineage: inherited -- no [crispy] marker anywhere in pkg/osx/*.m or *.h; the package carries the parent project's launcher with PACKAGE_TARNAME / PROGRAM_PREFIX substituted at build (IWADController.m:380, LauncherManager.m:292)
### Sufficiency
Q1 created: the fact "the file at path P is the IWAD of type T" -- created when type T's slot receives a URL: on restore from defaults (pkg/osx/IWADController.m:161-170), on a name match in addIWADPath (:425-431), or on manual editing of the slot (AppKit); the eleven filenames are the recognised names (:53-67)
Q2 written: into type T's NSPathControl slot (pkg/osx/IWADController.m:73-83 maps type to control) and, at saveConfig, into NSUserDefaults under the key = the type's filename (:258-264); the selected type under "selected_iwad" (:268-270)
Q3 lifetime: persists across launcher runs in NSUserDefaults (written pkg/osx/IWADController.m:258-264, read :161-170); process lifetime in the slot object; no expiry, no re-validation
Q4 readers: getIWADLocation (pkg/osx/IWADController.m:103-120) for launch: (pkg/osx/LauncherManager.m:278-296, -iwad via pkg/osx/Execute.m:56); doomWadPath (IWADController.m:327-358) for setup/terminal; autoloadPath (:372-381); setDropdownList (:219-228); selectGameByName (:464-475)
Q5 after consumption: persists -- saveConfig runs before the launch (pkg/osx/LauncherManager.m:276), nothing clears the slot or the defaults, the launcher terminates (:296); the path migrates to the game process as the -iwad argument (pkg/osx/Execute.m:56), where it is no longer this fact but an input to the engine's own identification
Status: RESOLVED

Units resolving into this case, each with its own row and slot:

```text
unit  observation  row (IWADController.m)  slot (getIWADList)  type
U001  E013-001     :55  @"doom.wad"      :73  doom1      IWAD_DOOM1
U002  E013-002     :56  @"doom2.wad"     :74  doom2      IWAD_DOOM2
U003  E013-003     :57  @"tnt.wad"       :75  tnt        IWAD_TNT
U004  E013-004     :58  @"plutonia.wad"  :76  plutonia   IWAD_PLUTONIA
U005  E013-005     :59  @"chex.wad"      :77  chex       IWAD_CHEX
U006  E013-006     :60  @"heretic.wad"   :78  heretic    IWAD_HERETIC
U007  E013-007     :61  @"hexen.wad"     :79  hexen      IWAD_HEXEN
U008  E013-008     :62  @"strife.wad"    :80  strife     IWAD_STRIFE
U009  E013-009     :63  @"freedoom1.wad" :81  freedoom1  IWAD_FREEDOOM1
U010  E013-010     :64  @"freedoom2.wad" :82  freedoom2  IWAD_FREEDOOM2
U011  E013-011     :65  @"freedm.wad"    :83  freedm     IWAD_FREEDM
```

Each unit's fact, writers, readers and lifetime are the case's, with
the unit's own row (above) as the recognised name and the unit's own
slot as the written place; nothing distinguishes the eleven units
except the name, the slot and the executable chosen for the type
(NameForIWAD :122-138: heretic, hexen, strife, else doom).

## NC-02 -- the IWAD registry: identifying the game's IWAD by its filename (src/d_iwad.c)
source observation ids: E017-001 .. E017-017 (units U012-U028)
native state/data involved: the registry `iwads[]` (src/d_iwad.c:34-54): seventeen active rows of (name, mission, mode, description) and one commented-out row (strife0.wad, :52); the calling module's mask of admitted missions (src/d_iwad.h:24-32: IWAD_MASK_DOOM admits doom, doom2, pack_tnt, pack_plut, pack_chex, pack_hacx; IWAD_MASK_HERETIC, _HEXEN, _STRIFE one mission each); the IWAD search-directory list (BuildIWADDirList :787); the results of identification: the IWAD path `iwadfile` and the mission -- the Doom module's global `gamemission` (src/doom/d_main.c:1663), a local in Heretic's D_DoomMain (src/heretic/d_main.c:961), the Hexen and Strife module globals (src/hexen/h2_main.c:546, src/strife/d_main.c:1862); and, in the Doom module, what is derived from the mission: `gamemode` (d_main.c:947-973), `logical_gamemission` (src/doom/doomstat.h:68), `gamevariant` (d_main.c:1685-1700), the savegame directory name and the per-IWAD autoload directory name (D_SaveGameIWADName src/d_iwad.c:1015-1053 -> d_main.c:2083, :1802)
writers / creation points: D_FindIWAD (src/d_iwad.c:925-972). With `-iwad <file>`: D_FindWADByName (:846-900) locates the file as an absolute path or in the IWAD directories, I_Error("IWAD file '%s' not found!") if it does not exist (:950-953), then IdentifyIWADByName (:617-644) sets the mission from the row whose name equals the file's basename, case-insensitively, among the rows the mask admits (:631-639), else `none` (:623). Without `-iwad`: SearchDirectoryForIWAD (:589-612) walks the IWAD directories (:963-968) and takes the first admitted row whose name -- after DEH_String (:601): a dehacked patch can rename it -- exists in that directory (CheckDirectoryHasIWAD :560-584), setting the mission from the row (:605). Doom module only: D_IdentifyVersion (src/doom/d_main.c:913-945) resolves a `none` from the loaded lumps (MAP01 -> doom2, E1M1 -> doom, :925-937) or aborts with I_Error("Unknown or invalid IWAD file.") (:939-944); `-pack <name>` can override a Doom II mission (:979-991, SetMissionForPackName, error at :906). Strife: D_IdentifyVersion sets gamemission = strife unconditionally (src/strife/d_main.c:953-956). Hexen: D_IdentifyVersion (src/hexen/h2_main.c:336-362) reads lumps for gamemode only; the mission stays as D_FindIWAD left it. Heretic: the mission D_FindIWAD returns is never read again (src/heretic/d_main.c:961, :1130); Heretic's connect data hardcodes `heretic` (src/heretic/d_net.c:165)
updates / invalidation paths: the mission is set once at startup; the Doom module may rewrite it in D_IdentifyVersion (:929, :934) or by `-pack`; no later code path invalidates it. The IWAD file itself is then loaded (D_AddFile src/doom/d_main.c:1676 and the three module equivalents) and W_CheckCorrectIWAD (:1678; src/w_main.c:267-292, another native case) aborts if the loaded file carries another game's unique lump
readers / consumption points: Doom: D_IdentifyVersion (gamemode from lumps, d_main.c:947-973) and D_SetGameDescription (:997); D_SaveGameIWADName (src/d_iwad.c:1015-1053) maps the mission (and variant) back to a canonical row name -- "we match on gamemission rather than on IWAD name. This ensures that doom1.wad and doom.wad saves are stored in the same place" (:1022-1024) -- for the savegame directory (d_main.c:2083) and the per-IWAD autoload directory (:1802); the network: connect_data->gamemission = gamemission (src/doom/d_net.c:197), which the server validates against valid_modes (src/net_server.c:706-713; another native case) and compares with its own mission (:756-772); D_SuggestGameName / D_SuggestIWADName (src/d_iwad.c:1055-1084) turn a mission (and mode) back into a row's description or name for messages (src/w_main.c:283; src/setup/multiplayer.c:911); D_FindAllIWADs (:976-1010) lists installed rows for the setup tool (src/setup/mode.c:222, :298); D_IsIWADName (:56-69) answers whether a name is any registry name (callers not followed)
lifetime / persistence / reset behavior: the mission lives for the process and is re-derived from scratch at every start; no copy of it is stored. What persists on disk is derived from it: the savegame directory name and the autoload directory name are chosen by mission (and variant), not by the actual filename (src/d_iwad.c:1015-1053), so a later run with a differently named IWAD of the same mission finds the same saves (:1022-1024). The Heretic result does not outlive the call; the Strife result is replaced by a constant; the Hexen result is kept but not read for identification
relevant transitions: startup with `-iwad`: locate the file, identify by name under the module's mask -> mission or none; startup without `-iwad`: the first admitted registry name found in the search directories -> mission; Doom: none -> lump heuristic -> mission or abort; load the IWAD; Doom: gamemode from lumps, variant from the FREEDOOM / FREEDM lumps; savegame and autoload directories named from the mission; network connect: the mission copied into the connect data and checked by the server
supporting source-code/docs evidence: src/d_iwad.c:34-69, :560-612, :617-644, :846-870, :925-1010, :1015-1084; src/d_iwad.h:24-32; src/doom/d_main.c:913-993, :1655-1700, :1796-1806, :2078-2083; src/doom/doomstat.h:68; src/doom/d_net.c:197; src/heretic/d_main.c:961, :1126-1139; src/heretic/d_net.c:165; src/hexen/h2_main.c:336-362, :542-559; src/strife/d_main.c:940-957, :1858-1877; src/net_server.c:700-713, :756-772; README.md:74
remaining native-level uncertainty: BuildIWADDirList (:787-845) and the directory walk of D_FindWADByName (:860-900) were not read line by line (they decide where to look, not what is accepted); D_IsIWADName's callers were not followed; Hexen's handling of a `none` mission past D_IdentifyVersion, and its connect data, were not traced; SetMissionForPackName's body was not read past its error line (:906)
lineage: inherited, with rows the tree does not date -- src/d_iwad.c carries 7 [crispy] marker(s); the registry rows and the identification path carry none; which rows (e.g. rekkrsa.wad, rekkrsl.wad, doom2f.wad) are the fork's additions is not visible in the tree
### Sufficiency
Q1 created: the fact "the IWAD file F is mission M" -- created by the name match in IdentifyIWADByName (src/d_iwad.c:636-639) or SearchDirectoryForIWAD (:601-607), by the Doom module's lump heuristic (src/doom/d_main.c:925-937), or by Strife's constant (src/strife/d_main.c:955)
Q2 written: into `*mission`, i.e. the Doom module's global gamemission (src/doom/d_main.c:1663), Heretic's local (src/heretic/d_main.c:1130), Hexen's and Strife's globals (src/hexen/h2_main.c:546, src/strife/d_main.c:1862); `iwadfile` alongside; in Doom also gamemode (d_main.c:957-973), gamevariant (:1687-1700), savegamedir (:2083) and the autoload directory (:1802)
Q3 lifetime: process lifetime -- set once at startup (src/doom/d_main.c:1663), no invalidation path located; the names derived from it persist on disk across runs as directory names (src/d_iwad.c:1015-1053; src/doom/d_main.c:1802, :2083)
Q4 readers: D_IdentifyVersion and D_SetGameDescription (src/doom/d_main.c:913-997); the savegame and autoload directories (:2083, :1802); the connect data (src/doom/d_net.c:197) and the server's checks (src/net_server.c:706-713, :763-772); D_SaveGameIWADName, D_SuggestIWADName, D_SuggestGameName (src/d_iwad.c:1015-1084); D_FindAllIWADs (:976-1010, src/setup/mode.c:222)
Q5 after consumption: persists for the process; the mission itself is not stored, the directory names derived from it persist on disk and are re-derived identically next run (src/d_iwad.c:1022-1024); over the network it is copied into the connect data (src/doom/d_net.c:197) and checked, not re-identified, by the server (src/net_server.c:706, :763)
Status: RESOLVED

Units resolving into this case: one registry row each, admitted by one module's mask, consumed on that module's branch.

```text
unit  observation  row  name            mission     mode        mask      branch after a miss
U012  E017-001     :36  doom2.wad       doom2       commercial  DOOM     Doom
U013  E017-002     :37  plutonia.wad    pack_plut   commercial  DOOM     Doom
U014  E017-003     :38  tnt.wad         pack_tnt    commercial  DOOM     Doom
U015  E017-004     :39  doom.wad        doom        retail      DOOM     Doom
U016  E017-005     :40  doom1.wad       doom        shareware   DOOM     Doom
U017  E017-006     :41  doom2f.wad      doom2       commercial  DOOM     Doom
U018  E017-007     :42  chex.wad        pack_chex   retail      DOOM     Doom
U019  E017-008     :43  hacx.wad        pack_hacx   commercial  DOOM     Doom
U020  E017-009     :44  freedoom2.wad   doom2       commercial  DOOM     Doom
U021  E017-010     :45  freedoom1.wad   doom        retail      DOOM     Doom
U022  E017-011     :46  freedm.wad      doom2       commercial  DOOM     Doom
U023  E017-012     :47  rekkrsa.wad     doom        retail      DOOM     Doom
U024  E017-013     :48  rekkrsl.wad     doom        retail      DOOM     Doom
U025  E017-014     :49  heretic.wad     heretic     retail      HERETIC  Heretic
U026  E017-015     :50  heretic1.wad    heretic     shareware   HERETIC  Heretic
U027  E017-016     :51  hexen.wad       hexen       commercial  HEXEN    Hexen
U028  E017-017     :53  strife1.wad     strife      commercial  STRIFE   Strife
```

Branch notes (the part of the flow that differs by mask):

- Doom: a `none` goes to the lump heuristic, then abort (d_main.c:921-944)
- Heretic: the mission is a local of D_DoomMain, never read again (heretic/d_main.c:961, :1130)
- Hexen: kept as returned; D_IdentifyVersion reads lumps for gamemode only (h2_main.c:336-362)
- Strife: overwritten by the constant `strife` (strife/d_main.c:955)

Each unit's fact, writers, readers and lifetime are the case's, with
the unit's own row as the name matched (:636, :601) and the mission
written; the mode and description fields are read only by
D_SuggestIWADName / D_SuggestGameName (:1055-1084) and D_FindAllIWADs
(:976-1010), never by the identification itself. The thirteen rows
IWAD_MASK_DOOM admits are the only ones whose miss can be recovered by
contents (the lump heuristic); the other four are accepted or refused
by name alone.

## NC-03 -- valid game mode/mission combinations, with their episode and map counts (src/d_mode.c)
source observation ids: E022-001 .. E022-015 (units U029-U043)
native state/data involved: the table `valid_modes[]` (src/d_mode.c:26-48; the file describes itself as "Functions and definitions relating to the game type and operational mode", :15-17; the table as "Valid game mode/mission combinations, with the number of episodes/maps for each", :23-24): fifteen rows of (mission, mode, episodes, maps). Three functions read it: D_ValidGameMode (:52-65) -- "Check that a gamemode+gamemission received over the network is valid" (:50) -- true iff some row has the pair; D_ValidEpisodeMap (:67-100) -- true iff the pair has a row and 1 <= episode <= row.episode and 1 <= map <= row.map (:88-96), with two Heretic special cases written into the function rather than the table (:72-84: retail episode 6 has maps 1-3; registered episode 4 has map 1); D_GetNumEpisodes (:105-117) -- the largest episode for which D_ValidEpisodeMap holds with map 1. No value is stored by these functions; each returns a boolean or a count computed on the spot. What the callers then keep: the server's adopted `sv_gamemode` / `sv_gamemission` (src/net_server.c:152, :753-759) and `sv_settings` (:1035); Heretic's `startepisode` / `startmap` (src/heretic/d_main.c:1506-1510)
writers / creation points: the fact "the pair (mission, mode) is valid" is produced by D_ValidGameMode (src/d_mode.c:56-64); the fact "(episode, map) is valid for the pair" by D_ValidEpisodeMap (:72-100). Their inputs come from: a connecting client's connect data (src/net_server.c:700-713 -- data.gamemission / data.gamemode, sent by the client from its own identification, src/doom/d_net.c:197); the controlling client's game settings (src/net_server.c:1018-1033, through NET_ValidGameSettings src/net_common.c:433-455 which checks ticdup, extratics, deathmatch, skill, version and episode/map in that order, :436-452); Heretic's -warp parameters at startup (src/heretic/d_main.c:1504-1506); Heretic's warp cheat (src/heretic/sb_bar.c:1572-1574); the setup tool's warp menu (src/setup/multiplayer.c:411, :425, :458)
updates / invalidation paths: the table is compiled in and never modified; the verdicts are not stored and so are never invalidated. The server adopts the FIRST connecting client's pair as the session's (src/net_server.c:752-759) after validating it (:706-713), and every later client's pair is compared with it (:761-777) -- a mismatch is a reject ("Game mismatch: server is %s (%s), client is %s (%s)", :768-776). The controller's settings replace sv_settings only if valid (:1029-1035)
readers / consumption points: src/net_server.c:706-713 (refuse connect data: log and return, no slot allocated); :753-759 (adopt the pair); :763-777 (reject a client whose pair differs); :1029-1035 (refuse the controller's settings; otherwise store them -- they later reach every client as the game start settings, src/net_client.c:308, and the Doom client loads them into startepisode / startmap, src/doom/d_net.c:107-112); src/heretic/d_main.c:1504-1510 (an invalid -warp becomes episode 1 map 1); src/heretic/sb_bar.c:1574-1577 (an invalid cheat warp does nothing); src/setup/multiplayer.c:411 (number of episodes for the menu), :425-429 and :458-462 (invalid E/M buttons left out of the warp menu); D_GetNumEpisodes (src/d_mode.c:105-117)
lifetime / persistence / reset behavior: the verdict lives for the call; the table lives for the process; what the verdict gates persists for the network session -- sv_gamemode / sv_gamemission from the first client until the server's state changes (:153-156 region; not traced further) and sv_settings until the next valid settings packet -- or for the Heretic process (startepisode / startmap). Nothing is written to disk by this case
relevant transitions: client connect -> pair validated -> adopted or compared -> accepted or rejected; controller sends settings -> validated (version, then episode/map against the pair) -> stored and later distributed; Heretic startup with -warp -> validated or reset; Heretic cheat warp -> validated or ignored; setup tool opens the warp menu -> valid cells only
supporting source-code/docs evidence: src/d_mode.c:15-17, :23-48, :50-117; src/net_server.c:152, :700-713, :752-777, :1003-1036; src/net_common.c:431-455; src/net_client.c:308; src/doom/d_net.c:107-112, :197; src/heretic/d_main.c:1503-1511; src/heretic/sb_bar.c:1566-1579; src/setup/multiplayer.c:411, :418-429, :452-462
remaining native-level uncertainty: the Doom module's own -warp / -episode handling (src/doom/d_main.c:2264 region) does not consult this table and was not traced here; how long sv_gamemode / sv_gamemission survive a server reset was not traced; the Strife and Hexen modules' use of the table beyond the shared network code was not searched (no caller found by grep outside the files above); the client never validates settings it receives (no caller of NET_ValidGameSettings outside the server, grep)
lineage: inherited -- src/d_mode.c carries no [crispy] marker; the pack_nerve and pack_master rows (:41-42) are not datable from the tree
### Sufficiency
Q1 created: two transient facts -- "the pair (mission, mode) is a valid game" (src/d_mode.c:56-64) and "(episode, map) exists for the pair" (:72-100) -- each a boolean returned to the caller
Q2 written: N/A: no persistent value is created by the validators -- each returns its boolean immediately (src/d_mode.c:60, :64, :78, :82, :93-94, :100); what the callers write afterwards is their own state: sv_gamemode / sv_gamemission (src/net_server.c:755-756), sv_settings (:1035), startepisode / startmap (src/heretic/d_main.c:1508-1509)
Q3 lifetime: N/A: the verdict has no lifetime beyond the call (src/d_mode.c:52-65, :67-100); the table is compiled in (:26-48); the gated state lives for the network session (src/net_server.c:752-759, :1035) or the Heretic process (src/heretic/d_main.c:1508-1509)
Q4 readers: src/net_server.c:706 (connect), :763 (session pair comparison, indirectly), :1029 via src/net_common.c:448-452 (settings); src/heretic/d_main.c:1506; src/heretic/sb_bar.c:1574; src/setup/multiplayer.c:411, :425, :458; src/d_mode.c:111 (D_GetNumEpisodes)
Q5 after consumption: the verdict disappears with the call; a refused connect or settings packet is dropped (src/net_server.c:712, :1032) and a mismatching client is told why (:775); an accepted pair becomes the server's for the session (:755-756) and is thereafter compared, not re-validated (:763); accepted settings are distributed to the clients, which load them without validating (src/net_client.c:308, src/doom/d_net.c:107-112)
Status: RESOLVED

Units resolving into this case: one row each.

```text
unit  observation  row  mission      mode        episodes  maps
U029  E022-001     :33  pack_chex    retail      1         5
U030  E022-002     :34  doom         shareware   1         9
U031  E022-003     :35  doom         registered  3         9
U032  E022-004     :36  doom         retail      4         9
U033  E022-005     :37  doom2        commercial  1         32
U034  E022-006     :38  pack_tnt     commercial  1         32
U035  E022-007     :39  pack_plut    commercial  1         32
U036  E022-008     :40  pack_hacx    commercial  1         32
U037  E022-009     :41  pack_nerve   commercial  1         9
U038  E022-010     :42  pack_master  commercial  1         21
U039  E022-011     :43  heretic      shareware   1         9
U040  E022-012     :44  heretic      registered  3         9
U041  E022-013     :45  heretic      retail      5         9
U042  E022-014     :46  hexen        commercial  1         60
U043  E022-015     :47  strife       commercial  1         34
```

Each unit's facts, writers, readers and lifetime are the case's; the
unit's own row supplies the pair that D_ValidGameMode accepts and the
episode and map limits D_ValidEpisodeMap applies to it. The two Heretic
special cases (src/d_mode.c:72-84) extend U040 (registered: episode 4
map 1) and U041 (retail: episode 6 maps 1-3) beyond their rows'
limits; no other unit has an exception outside the table.

## NC-04 -- valid mission/version pairs for a network game (src/d_mode.c)
source observation ids: E023-001 .. E023-016 (units U044-U059)
native state/data involved: the "Table of valid versions" (src/d_mode.c:119-141): sixteen rows of (mission, version) naming which emulated executable versions a mission may run under; D_ValidGameVersion (:143-166), which first folds every Doom-family mission onto `doom` -- "All Doom variants can use the Doom versions" (:147-154: doom2, pack_plut, pack_tnt, pack_hacx, pack_chex, pack_nerve, pack_master) -- then returns true iff a row has the pair (:156-165). The validator stores nothing. The only caller is NET_ValidGameSettings (src/net_common.c:433-455), which checks a controller's settings in order -- ticdup, extratics, deathmatch, skill, then the version (:448-449), then episode/map (:451-452) -- and is itself called only by the server when the controlling client sends the game-start settings (src/net_server.c:1018-1035); on success the settings are kept as sv_settings (:1035)
writers / creation points: the fact "version V is valid for mission M" is produced by D_ValidGameVersion (src/d_mode.c:156-165) from the server's adopted mission (sv_gamemission, src/net_server.c:756, :1029) and the version in the controller's settings (settings->gameversion, src/net_common.c:448). The version in the settings is written by the controller from its own global: Doom and Strife put their running gameversion in (src/doom/d_net.c:148, src/strife/d_net.c:156); Heretic and Hexen put a constant in (src/heretic/d_net.c:144 exe_heretic_1_3; src/hexen/d_net.c:151 exe_hexen_1_1)
updates / invalidation paths: the table is compiled in and never modified; the verdict is not stored. Valid settings replace sv_settings (src/net_server.c:1035); invalid settings are dropped with a log line and no reply (:1029-1033) -- the server stays in the waiting state and the controller is not told
readers / consumption points: src/net_server.c:1029 (the only consumer of the verdict). After acceptance the settings go to every client at game start (src/net_client.c:308 NET_CL_StartGame; src/doom/d_net.c:259-261), but the Doom client's LoadGameSettings (src/doom/d_net.c:107-133) does not read settings->gameversion: it loads deathmatch, episode, map, skill, loadgame, lowres_turn, nomonsters, fast, respawn, timelimit, consoleplayer and the player count (:111-132) and leaves its own gameversion as it was. No other reader of the received version was found in src/doom/d_net.c, src/strife/d_net.c or src/net_client.c (grep)
lifetime / persistence / reset behavior: the verdict lives for the call; the accepted settings live in sv_settings for the server's session (src/net_server.c:1035) and are copied to clients at start; the version value inside them is carried but, on the Doom client, not applied. Nothing is written to disk
relevant transitions: controller sends game-start settings -> server validates version against its adopted mission (after the Doom-family fold) -> settings kept or silently dropped -> game start distributes the kept settings -> clients load everything but the version
supporting source-code/docs evidence: src/d_mode.c:119-166; src/net_common.c:431-455; src/net_server.c:1003-1036; src/net_client.c:308; src/doom/d_net.c:107-133, :138-150, :248-262; src/heretic/d_net.c:144; src/hexen/d_net.c:151; src/strife/d_net.c:156
remaining native-level uncertainty: whether a dropped settings packet is ever retried by the controller was not traced (src/net_client.c); the Strife client's LoadGameSettings was not read (its SaveGameSettings mirrors Doom's at :156); NET_CL_StartGame's handling of the settings between receipt and LoadGameSettings was not read line by line
lineage: inherited -- src/d_mode.c carries no [crispy] marker (grep: 0)
### Sufficiency
Q1 created: the transient fact "version V is valid for mission M (Doom-family missions folded to doom)" -- src/d_mode.c:149-165
Q2 written: N/A: the validator returns its boolean at once (src/d_mode.c:161, :165) and nothing records the verdict; the gated value -- the settings including the version -- is stored by the server at src/net_server.c:1035 only when the whole settings check passes (src/net_common.c:436-454)
Q3 lifetime: N/A: no lifetime beyond the call (src/d_mode.c:143-166); the accepted settings live for the server session (src/net_server.c:1035) and are handed to clients at start (src/net_client.c:308)
Q4 readers: src/net_common.c:448 inside NET_ValidGameSettings, from src/net_server.c:1029; the carried version is read by no client code found (src/doom/d_net.c:107-133 omits it; grep over src/doom/d_net.c, src/strife/d_net.c, src/net_client.c)
Q5 after consumption: the verdict disappears with the call; a failing settings packet is dropped without reply (src/net_server.c:1031-1032); a passing one is stored and later distributed (:1035, src/net_client.c:308), the version inside it travelling to clients that do not read it (src/doom/d_net.c:107-133)
Status: RESOLVED

Units resolving into this case: one row each.

```text
unit  observation  row  mission   version
U044  E023-001     :125  doom      exe_doom_1_2
U045  E023-002     :126  doom      exe_doom_1_5
U046  E023-003     :127  doom      exe_doom_1_666
U047  E023-004     :128  doom      exe_doom_1_7
U048  E023-005     :129  doom      exe_doom_1_8
U049  E023-006     :130  doom      exe_doom_1_9
U050  E023-007     :131  doom      exe_hacx
U051  E023-008     :132  doom      exe_ultimate
U052  E023-009     :133  doom      exe_final
U053  E023-010     :134  doom      exe_final2
U054  E023-011     :135  doom      exe_chex
U055  E023-012     :136  heretic   exe_heretic_1_3
U056  E023-013     :137  hexen     exe_hexen_1_1
U057  E023-014     :138  hexen     exe_hexen_1_1r2
U058  E023-015     :139  strife    exe_strife_1_2
U059  E023-016     :140  strife    exe_strife_1_31
```

Each unit's fact, writer, reader and lifetime are the case's; the
unit's own row is the pair D_ValidGameVersion accepts. The eleven
`doom` rows (U044-U054) serve every Doom-family mission through the
fold at src/d_mode.c:149-154; the other five serve their own mission
only.

## NC-05 -- the emulated game version: `-gameversion` against the supported list, and what the version then governs (src/doom/d_main.c)
source observation ids: E034-001 .. E034-011 (units U060-U070); the Hexen and Strife tables of the same shape (E313-*, E499-*) are later in P_raw order and will be added to this case when reached
native state/data involved: the Doom module's table of supported versions (src/doom/d_main.c:1125-1143): eleven rows of (description, cmdline, version) plus a NULL sentinel; the global `gameversion` (GameVersion_t); the vanilla version CODE derived from it by G_VanillaVersionCode (src/doom/g_game.c:3175-3189: 106, 107, 108, or 109 for 1.9 and "All other versions are variants on v1.9", :3186) -- which is what demos and savegames carry
writers / creation points: InitGameVersion (src/doom/d_main.c:1147-1291). With `-gameversion <value>` (:1165-1190): the value is compared with each row's cmdline (:1169-1176); a miss prints "Supported game versions:" with the table (:1178-1186) and aborts, I_Error("Unknown game version '%s'") (:1188). Without it (:1191-1269): the version is inferred -- chex and hacx from the mission (:1195-1206), shareware / registered / doom2 default to 1.9 and then take the version byte of the IWAD's own demo lumps demo1-demo3 (:1207-1253: byte 0-4 -> 1.2, 106 -> 1.666, 107 -> 1.7, 108 -> 1.8, 109 -> 1.9), retail -> ultimate (:1255-1258), other commercial -> final (:1259-1268, "has the crash in the demo loop; however ... plays back most demos correctly", :1261-1265). The chosen version then rewrites other facts: deathmatch 2 -> 1 before 1.4 (:1271-1275), retail -> registered before ultimate (:1277-1282), tnt/plutonia -> doom2 before final (:1284-1290)
updates / invalidation paths: set once in InitGameVersion (called from D_DoomMain after D_IdentifyVersion, :1683); no later writer found (grep over src/doom); the version is not changed by a demo or a savegame that carries a different code -- those are refused or warned about instead (below)
readers / consumption points: (1) compatibility branches throughout the Doom module, about eighty sites in fourteen files (grep `gameversion`, src/doom): item pickup rules (src/doom/p_inter.c:416-570 `> exe_doom_1_2`, :832, :1000), monster behaviour (src/doom/p_enemy.c:184, :701, :962-970, :1685), map specials (src/doom/p_spec.c:608, :1585, :1661), collision (src/doom/p_map.c:1533), lost-soul bounce (src/doom/p_mobj.c:372), menus, status bar, intermission, finale and HUD text (src/doom/m_menu.c, st_stuff.c, wi_stuff.c, f_finale.c, hu_stuff.c), brightmaps (src/doom/r_bmaps.c:960, :981), Crispness options (src/doom/m_crispy.c:219, :316), episode availability (src/doom/g_game.c:2812, :3509); (2) the version CODE written into every demo header (src/doom/g_game.c:3213-3216; longtics demos write DOOM_191_VERSION instead, :3209-3212) and into every savegame header as the string "version %i" (src/doom/p_saveg.c:1436-1440); (3) the checks on read: a demo whose byte differs from the running code is refused with "Demo is from a different game version!" -- fatal for a single demo, "[crispy] make non-fatal" (a warning, then the demo is treated as finished) otherwise (src/doom/g_game.c:3341-3366); a savegame whose version string differs is refused by P_ReadSaveGameHeader (src/doom/p_saveg.c:1470-1476, "bad version") and the load path shows the mismatch (src/doom/g_game.c:2526-2533, M_LoadGameVerMismatch); (4) the game's banner name (src/doom/d_main.c:856-858)
lifetime / persistence / reset behavior: `gameversion` lives for the process and is re-chosen at every start. The code derived from it persists in every demo (one byte, src/doom/g_game.c:3215) and every savegame (sixteen bytes "version %i", src/doom/p_saveg.c:1437-1440) the program writes, and is compared with the running code when such a file is read (:1474-1476; g_game.c:3341). Because G_VanillaVersionCode folds ultimate, final, final2, hacx and chex onto 109 (:3185-3187), a savegame written under any of those loads under any other of them; only 1.666, 1.7 and 1.8 are distinguished, and 1.2 and 1.5 write no version byte into demos (:3213)
relevant transitions: startup -> `-gameversion` matched or the version inferred from the mission, mode and the IWAD's demo lumps -> dependent facts downgraded; play -> compatibility branches; save / record -> the code written into the header; load / play back -> the header's code compared with the running code, mismatch refused (save; single demo) or warned (demo loop)
supporting source-code/docs evidence: src/doom/d_main.c:848-862, :1125-1143, :1147-1291, :1683; src/doom/g_game.c:2522-2533, :3174-3222, :3334-3366; src/doom/p_saveg.c:1426-1480; src/doom/m_menu.c:945-953; the grep listing of `gameversion` over src/doom (fourteen files)
remaining native-level uncertainty: the eighty-odd compatibility branches were listed, not each traced; M_LoadGameVerMismatch's body (src/doom/m_menu.c) was not read; DemoVersionDescription (src/doom/g_game.c) was not read; whether anything outside src/doom reads the Doom module's gameversion was not searched
lineage: inherited with fork changes at the checks -- the non-fatal demo-version mismatch is marked "[crispy] make non-fatal" (src/doom/g_game.c:3356) and the load-path mismatch indication "[crispy] indicate game version mismatch" (:2528); the table and InitGameVersion carry no marker
### Sufficiency
Q1 created: the fact "this process emulates executable version V" -- from the `-gameversion` match (src/doom/d_main.c:1169-1176) or the inference (:1191-1269); and, derived from it, the vanilla version code (src/doom/g_game.c:3175-3189)
Q2 written: into the global gameversion (src/doom/d_main.c:1173, :1199, :1205, :1211, :1230-1242, :1257, :1267); into demo headers as one byte (src/doom/g_game.c:3215) and savegame headers as "version %i" (src/doom/p_saveg.c:1437-1440)
Q3 lifetime: process lifetime for gameversion (no later writer, grep); the code persists in demos and savegames on disk for as long as those files exist (src/doom/g_game.c:3213-3216; src/doom/p_saveg.c:1436-1440)
Q4 readers: the compatibility branches (src/doom/p_inter.c:416-1000, p_enemy.c:184-1685, p_spec.c:608-1661, p_map.c:1533, p_mobj.c:372, m_menu.c:1329-3390, st_stuff.c:784-1669, wi_stuff.c:813-2028, hu_stuff.c:446-1120, f_finale.c:148, :1008, r_bmaps.c:960, :981, m_crispy.c:219, :316, g_game.c:1034-2812); the header writers (g_game.c:3213-3216; p_saveg.c:1437); the header checks (g_game.c:3341-3366; p_saveg.c:1474-1476 with g_game.c:2526-2533)
Q5 after consumption: the running version persists for the process; the code in a demo or savegame persists with the file and is compared, not adopted, on read -- a mismatch refuses the savegame (src/doom/p_saveg.c:1476; src/doom/g_game.c:2526-2533) or the single demo, and only warns for a demo in the demo loop (src/doom/g_game.c:3353-3365)
Status: RESOLVED

Units resolving into this case: one supported version each.

```text
unit  observation  row    cmdline   version         description
U060  E034-001     :1131  1.2       exe_doom_1_2    Doom 1.2
U061  E034-002     :1132  1.5       exe_doom_1_5    Doom 1.5
U062  E034-003     :1133  1.666     exe_doom_1_666  Doom 1.666
U063  E034-004     :1134  1.7       exe_doom_1_7    Doom 1.7/1.7a
U064  E034-005     :1135  1.8       exe_doom_1_8    Doom 1.8
U065  E034-006     :1136  1.9       exe_doom_1_9    Doom 1.9
U066  E034-007     :1137  hacx      exe_hacx        Hacx
U067  E034-008     :1138  ultimate  exe_ultimate    Ultimate Doom
U068  E034-009     :1139  final     exe_final       Final Doom
U069  E034-010     :1140  final2    exe_final2      Final Doom (alt)
U070  E034-011     :1141  chex      exe_chex        Chex Quest
```

Each unit's fact, writers, readers and lifetime are the case's; the
unit's own row is the cmdline value accepted and the version it
selects. U060 (1.2) and U061 (1.5) select versions that write no
version byte into demos (src/doom/g_game.c:3213); U067-U070 and U066
select versions whose savegame and demo code is 109, the same as 1.9
(src/doom/g_game.c:3185-3187).

## NC-06 -- HHE text replacement: string offsets that are valid but unsupported, per Heretic version (src/heretic/deh_htext.c)
source observation ids: E186-001 .. E186-336, E187-001 .. E187-305, E188-001 .. E188-305 (units U071-U1016; 946 units in one case)
native state/data involved: three compiled-in lists of executable string offsets, one per HHE version the port emulates -- "String offsets that are valid but we don't support." (src/heretic/deh_htext.c:531): unsupported_strings_1_0 (:533-578, 336 offsets), unsupported_strings_1_2 (:580-621, 305), unsupported_strings_1_3 (:623-671, 305), each -1-terminated, indexed by version through unsupported_strings[] (:666-671); the running HHE version deh_hhe_version (set by -hhever, src/heretic/deh_htic.c:61-81; a later native case); the main offset-to-string table strings[] (:44-529: "Offsets / String" per version, rejected at EN2 as a mapping) read by GetStringByOffset (:691-705); a patch's "Text <offset> <length>" section (:774); and the process-wide string substitution table that successful replacements go into (DEH_AddStringReplacement, src/deh_str.c:175-)
writers / creation points: StringIsUnsupported (:673-689) -- the running version's list is scanned for the offset (:678-686). DEH_TextStart (:767-829) parses the section header (:774-778), reads the replacement text (:780-792), and then decides in order: unsupported offset -> DEH_Warning("Unsupported string replacement: %i") and nothing else (:796-799); unknown offset -> SuggestOtherVersions (:732-765, which scans the main table AND the three unsupported lists for other versions holding the offset and prints "-hhever" advice, src/heretic/deh_htic.c:168-) then DEH_Error("Unknown string offset") (:803-807); replacement longer than the executable allows -> DEH_Error (:812-817); otherwise DEH_AddStringReplacement (:818-823). DEH_Warning prints to stderr and sets nothing (src/deh_io.c:365-376); DEH_Error prints and sets context->had_error (:378-391), which makes DEH_LoadFile abort the program after the file -- I_Error("Error parsing dehacked file") (src/deh_main.c:455-462)
updates / invalidation paths: the lists are compiled in and never modified; the verdict is not stored. The replacement text of an unsupported line is freed (:825-826) and the line has no further effect; the patch continues to parse. Replacements that succeed persist in the substitution table for the process (src/deh_str.c:175-197: an existing substitution for the same original is replaced)
readers / consumption points: DEH_TextStart :796 is the only reader of StringIsUnsupported (grep); SuggestOtherVersions :751-764 reads all three lists to advise a version when an offset is unknown. Nothing downstream can tell that a replacement was refused as unsupported: later DEH_String lookups of the original string return the original (src/deh_str.c), exactly as if the patch line had not existed
lifetime / persistence / reset behavior: the verdict lives for the call and leaves one stderr line; the lists live for the process; a refused line leaves no state; an accepted line's substitution lives for the process. Nothing is written to disk by this case
relevant transitions: patch file loaded -> "Text" section parsed -> offset classified (unsupported / unknown / too long / accepted) -> warning and skip, error and abort-after-file, error and abort-after-file, or substitution stored
supporting source-code/docs evidence: src/heretic/deh_htext.c:32-46, :44-529 (the main table's shape), :531-671, :673-689, :691-705, :732-765, :767-829; src/deh_io.c:365-391; src/deh_main.c:455-462; src/deh_str.c:175-197; src/heretic/deh_htic.c:61-81, :168-
remaining native-level uncertainty: what the offsets denote in the three Heretic executables is known only from the comment "valid but we don't support" (:531) -- the tree carries no map from these offsets to strings (the main table :44-529 holds the supported ones); the default value of deh_hhe_version when -hhever is absent was not read (src/heretic/deh_htic.c); the substitution table's lookup path (DEH_String) was not read line by line
lineage: inherited -- src/heretic/deh_htext.c carries 0 [crispy] marker(s); the lists, StringIsUnsupported and DEH_TextStart's decision chain carry none
### Sufficiency
Q1 created: the transient fact "offset O is a valid string offset of Heretic version V that the port does not support" -- src/heretic/deh_htext.c:678-686, for the running version V
Q2 written: N/A: the verdict is returned as a boolean (:684, :688) and acted on at once -- a stderr warning (:798, src/deh_io.c:365-376) -- and no field, flag or file records it; the replacement text is freed (:826)
Q3 lifetime: N/A: no persistent value is created (:796-799, :825-826); the lists themselves are compiled in (:533-671); an accepted replacement, the other branch, lives for the process in the substitution table (src/deh_str.c:175-197)
Q4 readers: DEH_TextStart, src/heretic/deh_htext.c:796 (the decision); SuggestOtherVersions, src/heretic/deh_htext.c:751-764 (advice when an offset is unknown); no other reader (grep StringIsUnsupported, unsupported_strings)
Q5 after consumption: the line disappears without trace -- the patch continues (:827-828), nothing marks the refusal, and later string lookups behave as if the line were absent (src/deh_str.c); the program does not abort for an unsupported offset (DEH_Warning sets no error, src/deh_io.c:365-376), in contrast with an unknown offset (DEH_Error, :390; src/deh_main.c:459-462)
Status: RESOLVED

Units resolving into this case: one offset each, grouped by the list (the version) they belong to. Each unit's own evidence is its row: the line of its offset in src/heretic/deh_htext.c, recorded per unit in observations.tsv (the `line` column) and summarised here by list.

```text
list                      version  units          count  rows (deh_htext.c)
unsupported_strings_1_0   1.0      U071-U406     336  :535-576 (declared :533)
unsupported_strings_1_2   1.2      U407-U711     305  :582-620 (declared :580)
unsupported_strings_1_3   1.3      U712-U1016    305  :625-663 (declared :623)
```

The three lists share every writer, reader and lifetime above; a unit
differs from its neighbours only in its offset and in which running
version makes its list the one scanned (:678). The same offset value
recurs across lists (e.g. 0, 4, 64, 104 open all three), so three units
may name one number; they stay three units, because each list is its
own source segmentation (sealed Section 4.1).

## NC-07 -- the HHE patch version: `-hhever` against the valid Heretic versions (src/heretic/deh_htic.c)
source observation ids: E191-001, E191-002, E191-003 (units U1017-U1019)
native state/data involved: the list of valid version names hhe_versions[] (src/heretic/deh_htic.c:35-38: "1.0", "1.2", "1.3"), parallel to the enum deh_hhe_version_t (src/heretic/deh_htic.h:26-32); the global deh_hhe_version, default deh_hhe_1_0 (src/heretic/deh_htic.c:42); the `-hhever <version>` parameter -- "Select the Heretic version number that was used to generate the HHE patch to be loaded. Patches for each of the Vanilla Heretic versions (1.0, 1.2, 1.3) can be loaded, but the correct version number must be specified" (:89-96)
writers / creation points: DEH_HereticInit (:85-116), reached from the frame section's initialisation (src/heretic/deh_frame.c:188): if `-hhever` is present, SetHHEVersionByName (:61-81) scans the three names (:65-72) and sets deh_hhe_version to the matching index (:69); a name matching none leaves the version as it was and prints "Unknown Heretic version: %s" followed by "Valid versions:" and the list (:74-80) -- no abort. Then, for a 1.0 patch, the states[] table is altered to cut the two burning-death frames added after 1.0 (:105-115)
updates / invalidation paths: set once at initialisation; no later writer (grep). Nothing invalidates it; a patch that turns out to be for another version is not re-interpreted -- the loader prints advice instead (DEH_SuggestHereticVersion :168-181: "This patch may be for version %s. You are currently running in Heretic %s mode. For %s mode, add this to your command line: -hhever %s")
readers / consumption points: the version selects which per-version offset column or list the patch is read against: action pointers by executable offset (src/heretic/deh_frame.c:233), string offsets (src/heretic/deh_htext.c:697) and the unsupported-string list (:678; NC-06); it also maps thing types and frames between the 1.0 and later tables (src/heretic/deh_htic.c:118-166: DEH_MapHereticThingType :125-131, the frame mapping :138-165); and it is printed in the version advice (:168-181)
lifetime / persistence / reset behavior: process lifetime; not written to disk, not carried in demos or savegames (grep deh_hhe_version: readers above only); an unknown `-hhever` leaves the default 1.0 in force for the whole run
relevant transitions: startup -> `-hhever` matched or ignored with a message -> the version column for every HHE section lookup fixed for the process -> states[] adjusted for 1.0
supporting source-code/docs evidence: src/heretic/deh_htic.c:35-42, :61-81, :85-116, :118-166, :168-181; src/heretic/deh_htic.h:26-32, :47-49; src/heretic/deh_frame.c:188, :233; src/heretic/deh_htext.c:678, :697
remaining native-level uncertainty: when DEH_HereticInit runs relative to the first patch section parsed (src/heretic/deh_frame.c:188 is inside the frame section's init; whether a patch whose first section is not a frame section is read before the version is set was not traced); the frame mapping (:138-165) was read only as far as its role
lineage: inherited -- src/heretic/deh_htic.c carries no [crispy] marker (grep: 0)
### Sufficiency
Q1 created: the fact "patches are read as Heretic version V" -- src/heretic/deh_htic.c:65-72 (a match) or :42 (the default when no match)
Q2 written: into the global deh_hhe_version (src/heretic/deh_htic.c:42, :69)
Q3 lifetime: process lifetime (src/heretic/deh_htic.c:42; no later writer, grep); nothing on disk
Q4 readers: src/heretic/deh_frame.c:233; src/heretic/deh_htext.c:678, :697; src/heretic/deh_htic.c:112, :125, :138, :168-181
Q5 after consumption: persists unchanged for the process; a refused name is reported (src/heretic/deh_htic.c:74-80) and the default stays; the version is never stored or transmitted
Status: RESOLVED

Units resolving into this case: one version name each (all three on the same line, src/heretic/deh_htic.c:37).

```text
unit   observation  row  name  enum value
U1017  E191-001     :37  1.0   deh_hhe_1_0
U1018  E191-002     :37  1.2   deh_hhe_1_2
U1019  E191-003     :37  1.3   deh_hhe_1_3
```

U1017 is also the default (src/heretic/deh_htic.c:42): a run with no
`-hhever`, or with an unknown one, reads patches as 1.0.

## NC-08 -- which weapons may be selected in the Heretic shareware game (src/heretic/p_user.c)
source observation ids: E268-001 .. E268-009 (units U1020-U1028)
native state/data involved: the table WeaponInShareware[] (src/heretic/p_user.c:39-49): one boolean per weapon number, in weapon order (staff, gold wand, crossbow, blaster true; skull rod, phoenix rod, mace false; gauntlets, beak true); the game mode `gamemode`, set at startup from the IWAD's lumps -- no E2M1 lump means shareware (src/heretic/d_main.c:1334-1338); the player's ownership flags player->weaponowned[] (set by pickups, src/heretic/p_inter.c:259-286, or by the all-weapons cheat, src/heretic/sb_bar.c:1417-1426); the per-tic command's weapon-change request (cmd->buttons, BT_CHANGE and the weapon bits, :657-662); the player's pendingweapon, which the weapon sprite consumes when it is ready (src/heretic/p_pspr.c:420-442)
writers / creation points: the gate in P_PlayerThink (src/heretic/p_user.c:652-676): when the command asks for a weapon change (:657), the requested weapon is read from the command (:662; staff is redirected to the gauntlets when owned, :663-667); if it is owned and not already ready (:668-669), then "if (WeaponInShareware[newweapon] || gamemode != shareware)" the weapon becomes pending (:671-673). A weapon marked false, in shareware, is silently not made pending even when owned. The verdict is computed every tic the request appears; nothing records it
updates / invalidation paths: the table is compiled in. The same three weapons are refused elsewhere by code rather than by the table: the all-weapons cheat grants every weapon and then, in shareware, clears ownership of the skull rod, phoenix rod and mace (src/heretic/sb_bar.c:1417-1426); the map loader does not place the non-shareware ammo, artifacts and the mace in shareware (src/heretic/p_mobj.c:1200-1218). The table itself is read nowhere else (grep WeaponInShareware: one site)
readers / consumption points: src/heretic/p_user.c:671 (the gate); downstream, pendingweapon is consumed by P_BringUpWeapon (src/heretic/p_pspr.c:420-442) once the weapon sprite is ready: it picks the up-state for the pending weapon (:432-439) and clears the pending value (:440)
lifetime / persistence / reset behavior: the verdict lives for the tic; the gated value, pendingweapon, lives until the weapon sprite consumes it (src/heretic/p_pspr.c:440) and is itself part of the player state saved and restored with the game (not traced here); gamemode lives for the process (src/heretic/d_main.c:1334-1350). Nothing of this case is written to disk
relevant transitions: each tic with a weapon-change request -> ownership checked -> shareware gate -> pending or ignored; the weapon sprite becomes ready -> the pending weapon is brought up
supporting source-code/docs evidence: src/heretic/p_user.c:39-49, :652-676; src/heretic/p_pspr.c:420-442; src/heretic/p_inter.c:259-286; src/heretic/sb_bar.c:1417-1426; src/heretic/p_mobj.c:1200-1218; src/heretic/d_main.c:1334-1350
remaining native-level uncertainty: how weaponowned and pendingweapon travel through savegames (src/heretic/p_saveg.c) was not traced; whether a non-shareware weapon can be owned in shareware through any path other than the cheat (which clears it) was not exhausted -- the pickup path has no gate (src/heretic/p_inter.c:259-286), but the non-shareware weapon things are not placed in shareware (src/heretic/p_mobj.c:1200-1218)
lineage: inherited -- src/heretic/p_user.c carries 8 [crispy] markers elsewhere in the file; the table (:39-49) and the gate (:671-673) carry none
### Sufficiency
Q1 created: the transient fact "weapon W may be switched to in the shareware game" -- src/heretic/p_user.c:671, from the table (:39-49) and gamemode
Q2 written: N/A: the verdict is used in the same statement (src/heretic/p_user.c:671-673) and not stored; the gated effect is player->pendingweapon = newweapon (:673)
Q3 lifetime: N/A: no persistent value is created by the gate (src/heretic/p_user.c:671-675); pendingweapon lives until P_BringUpWeapon clears it (src/heretic/p_pspr.c:440); the table is compiled in (:39-49)
Q4 readers: src/heretic/p_user.c:671 (the only reader of the table, grep); the pending value's reader, src/heretic/p_pspr.c:424-440
Q5 after consumption: the verdict disappears with the tic; a refused request leaves pendingweapon unchanged and no message (src/heretic/p_user.c:671-675); an accepted one is consumed and cleared when the weapon comes up (src/heretic/p_pspr.c:440)
Status: RESOLVED

Units resolving into this case: one weapon each.

```text
unit   observation  row  value  weapon
U1020  E268-001     :40  true   Staff
U1021  E268-002     :41  true   Gold wand
U1022  E268-003     :42  true   Crossbow
U1023  E268-004     :43  true   Blaster
U1024  E268-005     :44  false  Skull rod
U1025  E268-006     :45  false  Phoenix rod
U1026  E268-007     :46  false  Mace
U1027  E268-008     :47  true   Gauntlets
U1028  E268-009     :48  true   Beak
```

The three units marked false (U1024-U1026) are the ones the gate
refuses in shareware; the same three are cleared by the all-weapons
cheat in shareware (src/heretic/sb_bar.c:1421-1426), a second copy of
the rule kept in code rather than read from this table.
