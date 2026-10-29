# Artifact 2 -- architectural mapping and outcomes -- EXPLORATORY C084 study

EXPLORATORY. Written after Artifact 1 was complete and committed
(`7b56ded`, X10a), per sealed §9 (Artifact 2) and design Section 10.
For each native case of `ARTIFACT_1_native.md`: the Phase 3 role each
native part maps to, or `no clean mapping`; the reasoning; and the
outcome -- R0 or F0, or every supported finding among F1, F2, F3
(sealed §7.0: a subset, nothing suppressed). Nothing here changes
Artifact 1.

## The architecture mapped onto, and the tests applied

The four roles, as the sealed record names them:

```text
WorldState                       the ordinary domain state (phase3/RESULTS_C1.md:21)
MonitorState                     separately maintained state tracking a validity
                                 condition over time (continuity), read by the
                                 judgment (phase3/RESULTS_C1.md:21-30)
transition-local violation       the verdict is computed at a specific transition
judgment                         from what is available there, not as a predicate
                                 over the state afterwards ("A violation can be
                                 transition-local, not state-local",
                                 phase3/RESULTS_C2.md:151)
persistent event provenance      a verdict, computed by the judgment at one
(EventProvenanceState)           transition, persisted as its own state bucket
                                 because a later judgment depends on it; written
                                 after the judgment, never before
                                 (phase3/DESIGN_C4.md:131-160; phase3/RESULTS_C4.md:31-40)
```

How a native case was placed against them -- the conventions this
document applies uniformly, stated here because they are the analyst's:

```text
a role is EXERCISED by a case when the native flow contains the
phenomenon the role exists for:
  continuity phenomenon   a validity condition that must hold over an
                          interval or sequence of transitions
  provenance phenomenon   a LATER JUDGMENT (not merely a later action or
                          lookup) depends on the outcome of an EARLIER
                          judgment
  judgment phenomenon     a verdict is computed about a transition or an
                          input
an exercised role maps to the native part that carries it; a role the
case does not exercise is "no clean mapping -- not exercised" and bears
on no finding

sealed §6.2, applied in order to each case: recoverable (all 14 are) ->
F0 if the evidence privileges no decomposition -> F1 if an exercised
role's information is represented without that role as a distinct
responsibility -> F2 if a required structure has no place -> F3 if the
responsibility exists but the native boundary is positively different;
an empty subset is R0 only against a named competitor that satisfies
the external validity semantics (design Section 9) and every unrelated
native fact and differs only at the boundary in question (sealed §7.1)

input validation: a judgment over an input that exists only at the
transition (a command line, a packet, a token, a patch line) has no real
competitor for the "transition-local versus state-predicate" question --
the input is not state -- so such a case does not pose that question;
unless another role is exercised, it is F0
```

Counting is by native case; the units behind each case are in
`units.tsv`. No prevalence is implied by any count (sealed §14).

## NC-01

roles: the eleven slots and the selection -> WorldState (the launcher's configuration state); the filename match at file-open (addIWADPath) -> transition-local violation judgment (an input validation); the launch's "No IWAD selected" check -> a later judgment that reads the earlier recognition's outcome; MonitorState -> no clean mapping -- not exercised; persistent event provenance -> no clean mapping -- collapsed: the recognition's outcome is the slot content itself
reasoning: the provenance phenomenon is present -- launch (pkg/osx/LauncherManager.m:278-289) depends on the recognition made at file-open (pkg/osx/IWADController.m:425-431): a filled slot is what a recognised IWAD leaves behind, the dropdown lists filled slots (:219-228), and the launch judges only that something is selected (:281-289), trusting the path without re-judging it. That outcome is kept as the slot's path in the launcher's ordinary configuration (and in NSUserDefaults across runs, :258-264), not as a separate record of "this was recognised"; nothing distinguishes a recognised slot from one typed by hand. This is the sealed F1 shape exactly: provenance that is part of the ordinary domain state rather than a separate persistent component. Continuity is not exercised. The boundary is not merely different (F3): there is no separate provenance owner at all, which is collapse. No structure lacks a place (F2).
outcome: F1

## NC-02

roles: gamemission, gamemode, gamevariant, iwadfile -> WorldState (the process's game identity); D_FindIWAD / IdentifyIWADByName / SearchDirectoryForIWAD / D_IdentifyVersion -> transition-local violation judgment (input validation at startup); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: the identification is one judgment at startup over inputs that exist only then (the -iwad argument, the search directories, the loaded lumps: src/d_iwad.c:925-972, src/doom/d_main.c:913-945); the result is a domain value used afterwards by behaviour selection, by directory naming and by the network (src/doom/d_main.c:2083, :1802; src/doom/d_net.c:197), where it is judged afresh as a value (NC-03), not trusted as an earlier verdict. No later judgment depends on the acceptance itself; a failed identification ends the program. The `none` carried from D_FindIWAD to D_IdentifyVersion (src/doom/d_main.c:921) is a hand-off inside the one startup sequence, not persistence across transitions. The case exercises WorldState and an input validation only; no competitor differing only at a boundary satisfies its semantics (judging the file name later would require keeping inputs the system discards). The evidence privileges no decomposition.
outcome: F0

## NC-03

roles: the valid_modes table -> part of the judgment's own definition; sv_gamemode / sv_gamemission (src/net_server.c:152, :753-759) -> persistent event provenance: a record adopted by the judgment at the first client's connect and consumed only by later judgments (:763-777 comparison; :1029 settings validation); sv_settings -> WorldState (the game's settings); D_ValidGameMode / D_ValidEpisodeMap at connect and at settings -> transition-local violation judgment; MonitorState -> not exercised
reasoning: the provenance phenomenon is present: every later client's connect is judged against the pair the first client's accepted connect established, and the controller's settings are judged against the same adopted mission (src/net_server.c:763-777, :1029). The adopted pair is kept as session-level state of the server, set once by the connect handler after it validated the pair (:753-759) and read only by judgments -- written by the judgment layer, read by the judgment layer, separate from any game world (none exists yet). That is the Phase 3 provenance boundary: a judgment's outcome persisted as its own state for later judgments. The multi-actor shape (one client's input becomes the rule for the others) is placeable: the adopted pair is the record, the comparison is the judgment, so F2 is not supported. The record holds the accepted value rather than a verdict flag; that is the content of the verdict here ("this is the session's game"), not a different owner or writer, so F3 is not supported. Continuity is not exercised.
outcome: R0
competitor: keep the game pair as ordinary per-client state (in each client record) and compare clients pairwise at start -- satisfies the external semantics (clients must play the same game, invalid pairs refused) and every unrelated native fact, and differs only in where the record lives and who owns it. Ruled out by the native flow: the pair is held once, at session level, in statics the connect handler sets from the first client and never per client (src/net_server.c:152, :753-759), and later clients are compared against it at connect, before any client record is allocated (:763-780).

## NC-04

roles: the controller's settings, once accepted -> WorldState (the game's start settings, distributed and loaded: src/net_client.c:308; src/doom/d_net.c:107-133); D_ValidGameVersion inside NET_ValidGameSettings -> transition-local violation judgment (input validation of a packet); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one judgment over a packet that exists only when it arrives (src/net_server.c:1018-1035); the accepted settings become ordinary state and are later applied, not judged -- the Doom client loads them without validating (src/doom/d_net.c:107-133) and does not even read the version they carry. No later judgment depends on the acceptance; a refused packet is dropped without reply (:1031-1032). Input validation only; the evidence privileges no decomposition. The carried-but-unread version is a native observation, not a finding: nothing in the four roles is contradicted by a field that no one reads.
outcome: F0

## NC-05

roles: gameversion -> WorldState (the emulated version; a domain value governing behaviour); the "version %i" header string in savegames and the version byte in demos -> persistent event provenance: a fact about the artifact's origin kept beside the state for a later judgment (src/doom/p_saveg.c:1436-1440; src/doom/g_game.c:3213-3216); P_ReadSaveGameHeader's comparison and the demo-playback check -> transition-local violation judgment at load / playback (src/doom/p_saveg.c:1470-1476; src/doom/g_game.c:3341-3366); the -gameversion match -> input validation at startup; MonitorState -> not exercised
reasoning: the provenance phenomenon is present and is the one C4 forced: a later judgment (may this save be loaded? may this demo be played?) depends on something about an earlier event (the version under which the artifact was written), and the native system persists that something as its own field, separate from the game state it accompanies, read and compared before the state is read. The responsibility therefore exists and has its own persistent place. What is positively different is the boundary on the write side: Phase 3's provenance is a VERDICT, computed by the judgment at the earlier transition and written after it (phase3/DESIGN_C4.md:131-160); the native record is a FACT written by the save and record actions themselves (P_WriteSaveGameHeader, G_BeginRecording) from a domain value, with no judgment at the writing transition at all -- saving and recording are never refused. The judgment happens only at consumption, over the persisted fact. Ownership differs with it: the record belongs to the artifact (file header; lifetime of the file), not to the game state's own provenance bucket. These are positive native facts (the cited writers and readers), not an absence of ours, which is the F3 test (sealed §6.2). The Hexen and Strife units of this case exercise only the version as WorldState (their artifacts carry fixed format texts: src/hexen/sv_save.c:1998-2000, :2124; src/strife/g_game.c:2693, :2765-2790); the finding rests on the Doom units U060-U070 and is scoped to them. Collapse (F1) is not supported: the record is separate, not folded into state. No structure lacks a place (F2).
outcome: F3
positive evidence: src/doom/p_saveg.c:1426-1452 writes the version string from the running gameversion inside the save routine, with no judgment; src/doom/g_game.c:3209-3216 does the same for demos; src/doom/p_saveg.c:1470-1476 and src/doom/g_game.c:3341-3366 read and compare it at load / playback before any state is consumed -- the provenance is written by the action and judged at consumption, the reverse of Phase 3's judgment-written, later-consumed verdict.

## NC-06

roles: the substitution table that accepted replacements go into -> WorldState (string state of the process); the per-version unsupported lists and StringIsUnsupported inside DEH_TextStart -> transition-local violation judgment (input validation of a patch line); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one judgment per patch line at parse time (src/heretic/deh_htext.c:796-799); a refused line leaves nothing and later lookups behave as if it had not existed; an accepted line's substitution is ordinary state read by non-judgments. No later judgment depends on the verdict. Input validation only; a competitor that judged at lookup time would have to keep what the native frees (:825-826) and would change the described behaviour (nothing records the refusal), so it does not satisfy the semantics; no decomposition is privileged.
outcome: F0

## NC-07

roles: deh_hhe_version -> WorldState (the version the loader reads patches as); SetHHEVersionByName -> transition-local violation judgment (input validation of -hhever at initialisation); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one judgment of a command-line value at initialisation (src/heretic/deh_htic.c:61-81); the resolved index is a domain value read by later lookups (src/heretic/deh_frame.c:233; src/heretic/deh_htext.c:678, :697), none of which judges whether the name was valid; an unknown name leaves the default and a message. Input validation only; no decomposition privileged.
outcome: F0

## NC-08

roles: gamemode and player->weaponowned[] -> WorldState; the gate at the weapon-change request (src/heretic/p_user.c:671) -> a predicate over current state evaluated at the request, see below; pendingweapon -> WorldState (the request's effect); MonitorState -> not exercised; persistent event provenance -> not exercised; transition-local violation judgment -> no clean mapping -- collapsed into a state predicate
reasoning: the judgment phenomenon is present (may this weapon be switched to?), but the verdict is a function of the current state alone -- the table, gamemode and ownership -- with nothing lost at the transition and no event-specific input beyond the weapon number (src/heretic/p_user.c:662-673). C2's boundary exists for verdicts that cannot be read off the state afterwards (phase3/RESULTS_C2.md:151); here "allowed(w) = owned[w] and (WeaponInShareware[w] or gamemode != shareware)" is a state predicate, and the native system computes it as one, at every request. The transition-local judgment role is therefore not needed as a distinct responsibility for this case: it collapses into a predicate over WorldState. No verdict persists (a refusal is silent, :671-675) and nothing is tracked over time, so provenance and continuity are not exercised. F3 is not supported -- there is no separate judgment boundary placed differently, there is none. The same rule copied into code elsewhere (the all-weapons cheat and the map loader, src/heretic/sb_bar.c:1421-1426; src/heretic/p_mobj.c:1200-1218) is a native observation about duplication, not a role.
outcome: F1

## NC-09

roles: the MapInfo table and cd_NonLevelTracks -> WorldState (per-map information for the process); SC_MustMatchString at each MAP-block token -> transition-local violation judgment (input validation of a script token); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one judgment per token at parse time (src/hexen/p_setup.c:1094); an unknown token ends the program (src/hexen/sc_man.c:444-451); a matched command's effect is a field of ordinary state read later by non-judgments (the P_GetMap* accessors). No later judgment depends on the match. Input validation only; no decomposition privileged.
outcome: F0

## NC-10

roles: snd_sfxdevice / snd_musicdevice -> WorldState (configuration); the per-module device lists with InitSfxModule / InitMusicModule -> transition-local violation judgment (input validation of a configured value at start); sound_module / music_module -> WorldState (the selected modules); the `module != NULL` guards on every later call -> later judgments reading the earlier selection's outcome; MonitorState -> not exercised; persistent event provenance -> no clean mapping -- collapsed: the outcome of the selection is the presence or absence of the module pointer
reasoning: the provenance phenomenon is present in the same shape as NC-01: every later sound and music call judges whether it may act (src/i_sound.c:291, :310, :318, :330, :335, :364, :373) and what it reads is the outcome of the start-up selection, carried as the module pointer itself -- NULL when the configured device was served by no module (:137, :164) -- not as a record that a device was accepted or refused. The outcome therefore lives in ordinary state; no separate provenance component exists, and nothing could tell a refused device from a module that failed to initialise. That is collapse (F1). The configured value's own persistence -- saved back unvalidated at exit (:547-548) -- means the refusal is re-made at every start from the same value, a native observation about lifetime that no role contradicts. Continuity is not exercised; no structure lacks a place.
outcome: F1

## NC-11

roles: the process's command line -> input; CheckForClientOptions -> transition-local violation judgment (input validation at server start); WorldState -> not exercised beyond the server's start; MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one scan of the command line at server start (src/net_dedicated.c:47-62); a listed option ends the program; otherwise nothing remains. The case has one transition and no state after a refusal; no later judgment exists. Input validation only; the system does not identify any boundary question.
outcome: F0

## NC-12

roles: the setup tool's binding variables and configuration file -> WorldState (configuration); GetJoystickType at the first button press -> transition-local violation judgment (an input validation of the device's name and shape); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one judgment at the calibration event over the device's reported name and shape (src/setup/joystick.c:701-726, :1035); a known type loads bindings that become ordinary configuration and persist as such, with nothing recording that they came from a known type; an unknown device is reported and configured by hand. No later judgment depends on the verdict. Input validation only; no decomposition privileged.
outcome: F0

## NC-13

roles: gamemission, the IWAD list, the executable name, the title and the configuration file names of the setup tool -> WorldState (the tool's run configuration); GetMissionForName for -game -> transition-local violation judgment (input validation of a command-line value); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one judgment of a command-line value at the tool's start (src/setup/mode.c:356-361), or a selection by executable name, dialog or fallback; the result is ordinary state used by non-judgments (which files to load and save, which executable to run). No later judgment depends on the verdict; a rejected value ends the program. Input validation only; no decomposition privileged.
outcome: F0

## NC-14

roles: the loaded WAD directory -> WorldState; W_CheckCorrectIWAD -> transition-local violation judgment (input validation at startup); MonitorState -> not exercised; persistent event provenance -> not exercised
reasoning: one check at startup after the IWAD is loaded (src/w_main.c:267-292); a marker lump of another game ends the program; otherwise nothing remains and no later judgment exists. Input validation only; the system does not identify any boundary question.
outcome: F0

## Not classified (E?)

None. Every unit of P_raw.tsv is RESOLVED (`7b56ded`).

## Summary by native case (counts are reported again, by counting unit, in PRIMARY_RESULT.md)

```text
F1   NC-01, NC-08, NC-10                                       3 cases
F2   --                                                        0
F3   NC-05                                                     1
R0   NC-03                                                     1
F0   NC-02, NC-04, NC-06, NC-07, NC-09, NC-11, NC-12, NC-13,   9
     NC-14
```

What the mapping does and does not say, in the sealed terms: three
cases represent a role's information without that role as a distinct
responsibility (two of them the provenance role, in the F1 example
shape; one the judgment role, which collapses into a state predicate);
one case persists provenance with a different writer and owner than
Phase 3's; one case retains the provenance boundary against a real
competitor; nine cases are input validations that do not pose the
boundary questions. None of this implies prevalence beyond this
target (sealed §14), and the target was chosen by hand for the shape
of one of these mechanisms (design L1).
