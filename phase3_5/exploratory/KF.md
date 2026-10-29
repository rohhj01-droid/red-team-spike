# Known-failure lane -- EXPLORATORY C084 study (X12-X14)

EXPLORATORY. The challenge lane of the sealed methodology (§11),
opened after the primary seal (`6da6a50`) by the owner's decision
(XQA-13). Rule and set: `KF0.md` -- the issue tracker of record,
`L = {bug, maybe-critical, sound-issues-on-windows}`, every issue
carrying one of them, pull requests excluded; counted 37 at X8
(2026-10-29T06:48:11Z) and enumerated 37 at X12 (2026-10-29T08:35:29Z,
`kf_items.tsv`, `4a79e22`): the two counts agree. Items are taken in
id order.

Reading rule (design 5.2): each item's FIRST POST only -- number,
title, state, created_at, labels, body -- through `tools/kf_api.py
first-post`; bodies are read up to 3,000 characters and a cut is noted
in the item's disclosure line; comments are not fetched before X14.
Every exposure is logged per item here and in `disclosure_log.md`.

KF-2 is decided from the frozen artifacts only (Artifacts 1-3,
`PRIMARY_RESULT.md`), on the sealed axes:

```text
representability   can the reported symptom / history be expressed with
                   Artifact 1's native description and Artifact 2's
                   mapping without adding or reassigning a role
domain             placed against Artifact 3's frozen classes D1-D14:
                   in-domain concordant / in-domain DISCORDANT /
                   in-domain indeterminate / out-of-domain (N/A)
attribution        measurement insufficiency | F2-like architectural
                   limitation | judgment-layer limitation |
                   reproduction/environment issue | scope mismatch
native replay      N/A for the whole lane, declared in advance (design
                   Section 8, decision 11)
```

KF-3 (cause / fix comparison) is appended per item only after KF-2 is
sealed (X14); nothing above an item's `KF-3:` line is edited then.

## KF item #90
disclosure: fields seen = title, labels (wontfix, maybe-critical), state (closed), created_at (2016-03-06), body (353 chars); cause leakage = no -- a design suggestion (invulnerable players' blood colour), no failure mechanism
symptom: expected = none stated as a failure (the reporter proposes that invulnerable players bleed white) ; observed = players with invulnerability bleed normally ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- blood splats and player powers are game-world behaviour outside every native case of Artifact 1; nothing in the four roles is asked to hold them
KF-2 domain: out-of-domain -- no class of Artifact 3 decides blood or invulnerability; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #92
disclosure: fields seen = title, labels (wontfix, maybe-critical), state (closed), created_at (2016-03-07), body (457 chars); cause leakage = yes -- the body names the current mechanism it would replace ("the current pause/unpause dance that happens when a menu is opened while recording a demo") and MBF's basetic/gametic distinction; no failure is reported, a reminder to the maintainer
symptom: expected = none stated ; observed = none stated (a note that the pause/unpause handling while recording is error-prone) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- demo recording's tic bookkeeping is outside every native case (Artifact 3 lists a demo's contents as out of domain)
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #174
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2017-03-28), body (865 chars); cause leakage = yes -- the reporter's hypothesis names code: "I believe this is because of `if (gametic & 3)` in `A_Tracer`", and a suggested fix (store `dest`, or save gametic); a video link not opened
symptom: expected = Revenant missiles keep homing after a saved game is loaded ; observed = after loading, missiles sometimes lose homing, randomly ; reproduction = save during homing missiles, load (video linked) ; affected version = not stated
KF-2 representability: partly -- the savegame's header and its load judgment are NC-05 (Artifact 1), but the fidelity of the restored game state (what the save body carries) is outside every native case; the symptom concerns the body, not the header
KF-2 domain: out-of-domain -- D5 decides only whether a Doom savegame is LOADABLE (its version string); this save loads, and what the frozen evidence does not define is the restored state's validity; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #250
disclosure: fields seen = title, labels (bug, rendering), state (closed), created_at (2018-01-03), body (812 chars); cause leakage = yes, speculative -- the reporter's "possible explanation" (the far line of a sector leaving the top screen bound) and two renderer functions named as candidates; screenshots not opened
symptom: expected = items hidden by floors stay hidden ; observed = with mouse look, items "shine" through floors on E1M1 ; reproduction = E1M1 Hangar, mouse look, two screenshot positions ; affected version = not stated
KF-2 representability: not representable -- rendering is outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #258
disclosure: fields seen = title, labels (wontfix, maybe-critical), state (closed), created_at (2018-01-19), body (1072 chars); cause leakage = yes -- the cause is stated (an emulated vanilla bug at a named line of g_game.c) with a fix commit in another project linked and a test map attached (not opened)
symptom: expected = respawn fog appears at every deathmatch spot ; observed = no fog at spots facing angle 180 ; reproduction = the attached map with -solo-net -deathmatch -warp 01 ; affected version = not stated
KF-2 representability: not representable -- deathmatch spawn effects are game-world behaviour outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #318
disclosure: fields seen = title, labels (patch, maybe-critical, help wanted), state (closed), created_at (2018-05-14), body (610 chars); cause leakage = yes -- the body IS the fix: a diff replacing `actor->target->x` with `->y` in A_VileTarget, with the wiki page named
symptom: expected = Arch-Vile fire spawns at the target's position ; observed = spawned at the wrong location (x used for y) ; reproduction = none documented beyond the wiki ; affected version = not stated
KF-2 representability: not representable -- monster behaviour outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #362
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2018-12-02), body (208 chars); cause leakage = no -- a wiki page name only ("Lopsided final boss explosions"), the question whether it can be fixed without breaking demos or dehacked
symptom: expected = none stated beyond the wiki's title ; observed = final boss explosions lopsided (by title) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #365
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2018-12-18), body (894 chars); cause leakage = yes -- the cause and the proposed change are stated with a line reference into p_enemy.c (the alive-player check in the boss death action)
symptom: expected = the episode ends when the ExM8 boss dies even if every player is dead (coop) ; observed = the ending is not triggered; players are stuck ; reproduction = Doom 1 coop, boss dies while all players are dead (rare) ; affected version = not stated
KF-2 representability: not representable -- level-end logic outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #408
disclosure: fields seen = title, labels (bug, pending, patch), state (closed), created_at (2019-04-24), body (4308 chars, CUT at 3000); cause leakage = yes, partial -- the console output shows "PadRejectArray: REJECT lump too short to pad!" before a segmentation fault and the start of a gdb session (the backtrace itself lies beyond the cut); the log also shows "This is not a valid dehacked patch file!" followed by a loaded DEHACKED lump -- the non-fatal signature path of deh_main.c:319-323 (XQA-07 d) seen in the wild
symptom: expected = Sunder.wad's maps load ; observed = crash after loading any of its 14 maps ; reproduction = ./crispy-doom -file sunder.wad -warp 01 ; affected version = 5.5.2 (released and git), Windows 10 x64 and Debian x32
KF-2 representability: not representable -- PWAD map loading is outside every native case (the one native mechanism visible in the log, the dehacked signature check, is a rejected enumerator, not a unit)
KF-2 domain: out-of-domain -- Artifact 3 lists PWAD and map validity as outside; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #454
disclosure: fields seen = title, labels (SDL-related, sound-issues-on-windows), state (closed), created_at (2019-09-10), body (870 chars); cause leakage = no -- symptoms, version and hardware only
symptom: expected = music and sound as in 5.5.2 ; observed = since 5.6, with the OPL (Adlib/Soundblaster) music device no music is heard while GUS (emulated) plays; "Digital sound effects" are high-pitched ; reproduction = select those devices on Win7 SP1 x64 with a Sound Blaster X-Fi ; affected version = 5.6+
KF-2 representability: representable for its setting -- the configured music and sfx devices are NC-10's inputs (snd_musicdevice = an OPL device, U1047-U1048; snd_sfxdevice = the SDL sound module's, U1056-U1061) and the module selection is NC-10's flow; the failure itself (silence from a served module; pitch) is behaviour inside the module, outside the native description
KF-2 domain: in-domain concordant for the part the rule decides -- D10: an OPL device value is SERVED(music_opl_module) and the digital sfx device SERVED(sound_sdl_module), provided their Init succeeds (an input the report leaves unstated and the rule does not decide); the external expectation (these are valid choices that should produce sound) agrees. The reported failure past the selection -- no audible music, wrong pitch -- is not decided by any class: for that part, out-of-domain
KF-2 attribution: scope mismatch -- the failure is not a validity phenomenon within the frozen scope; the device selection it depends on is concordant
native replay: N/A (declared in advance, design Section 8)

## KF item #457
disclosure: fields seen = title, labels (OS-specific, SDL-related, sound-issues-on-windows), state (closed), created_at (2019-09-22), body (1121 chars); cause leakage = no -- symptoms, two command lines, version and OS
symptom: expected = the same music volume whether or not SDL_SOUNDFONTS is set ; observed = music from a WAD is much quieter without the soundfont variable; music-pack playback unaffected ; reproduction = the two batch files quoted ; affected version = 5.6.2, Windows 7 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (music volume through the Windows MIDI process; the device selection of NC-10 is not in question)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #458
disclosure: fields seen = title, labels (duplicate, sound-issues-on-windows), state (closed), created_at (2019-09-22), body (1043 chars); cause leakage = yes -- the reporter's finding that copying 5.5.2's SDL2, SDL2_mixer and SDL2_net DLLs over 5.6's restores sound (a cause located in the library versions)
symptom: expected = sounds playing normally ; observed = since 5.6, no music with any settings and sound effects pitched up ; reproduction = original DOOM/DOOM2 WADs on Windows 10 x64, Sound Blaster Z ; affected version = 5.6 to 5.6.2
KF-2 representability: representable for its setting, as #454 -- the configured devices are NC-10's inputs; the failure (silence, pitch) is inside the modules, outside the native description
KF-2 domain: in-domain concordant for what D10 decides (a listed device is SERVED by its module, Init permitting); the failure past the selection is out-of-domain -- as #454, of which this is a declared duplicate
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #462
disclosure: fields seen = title, labels (OS-specific, SDL-related, sound-issues-on-windows), state (closed), created_at (2019-09-25), body (614 chars); cause leakage = no
symptom: expected = the music slider controls the volume of a virtual MIDI synth ; observed = the slider has no effect with that synth; it works with music packs and with the MS GS Wavetable synth ; reproduction = set VirtualMIDISynth as the default MIDI player ; affected version = 5.6.2, Windows 10 1903
KF-2 representability: not representable -- outside every native case of Artifact 1 (volume control of an external MIDI device)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #463
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2019-09-27), body (188 chars); cause leakage = no -- a feature idea (pause demo playback with the Pause key) with a side note that pausing mutes rather than pauses music
symptom: expected = none stated as a failure ; observed = demo playback cannot be paused ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case of Artifact 1 (demo playback control)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #475
disclosure: fields seen = title, labels (upstream, sound-issues-on-windows), state (closed), created_at (2019-10-10), body (1050 chars); cause leakage = yes -- the reporter names the component (midiproc's volume influences MP3/OGG/FLAC played from WADs) and shows the Windows mixer; the screenshot was not opened
symptom: expected = the MIDI process's volume does not influence music the main program plays ; observed = after setting music volume to 1 and relaunching with a music WAD, the music is almost inaudible ; reproduction = the four steps quoted ; affected version = 5.6.3, Windows 7 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (which process plays non-MIDI music)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #498
disclosure: fields seen = title, labels (OS-specific, SDL-related, sound-issues-on-windows), state (closed), created_at (2019-11-25), body (953 chars); cause leakage = no -- symptoms and the reporter's tool chain; two audio links not opened
symptom: expected = SIGIL's MIDI plays at an even volume as in PrBoom+ ; observed = a passage of the first SIGIL level's MIDI plays very quietly through VST MIDI players ; reproduction = SIGIL E5M1 with a VSTi MIDI player ; affected version = 5.6.3, Windows 10
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI rendering by an external synth)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #524
disclosure: fields seen = title, labels (bug, pending, patch), state (closed), created_at (2020-02-21), body (812 chars); cause leakage = yes, a hypothesis -- the reporter attributes the corruption to switching widescreen at the moment memory is being rearranged ("at the moment it would corrupt memory"); the screenshot was not opened
symptom: expected = switching widescreen on at that moment is disallowed or harmless ; observed = wall textures become 'Tutti-Frutti' when widescreen is switched on exactly as the intro music stops and the demo's map loads ; reproduction = the steps quoted ; affected version = 5.7, Windows 10
KF-2 representability: not representable -- outside every native case of Artifact 1 (rendering / screen reallocation timing)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #527
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-02-24), body (26 chars: "Bug report from the forum."); cause leakage = no
symptom: expected = none stated beyond the title ; observed = the MAP/WAD automap text widget placed badly in widescreen mode (by title) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case of Artifact 1 (automap HUD layout)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #528
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-02-24), body (26 chars); cause leakage = no
symptom: expected = none stated beyond the title ; observed = automap markers do not transform well in rotate mode in widescreen (by title) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case of Artifact 1 (automap rendering)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #556
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2020-03-23), body (347 chars); cause leakage = no -- a suggestion about weapon-key double tapping, with the reporter unsure of demo/network safety
symptom: expected = none stated as a failure (a suggestion: fast double tap of 3 selects the shotgun at once) ; observed = tapping 3 selects SSG first, shotgun second ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- Doom weapon selection; the only weapon-change case in Artifact 1 is Heretic's shareware gate (NC-08), which does not cover Doom's key handling
KF-2 domain: out-of-domain -- D8 decides Heretic weapon-change requests only; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #646
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-08-03), body (1374 chars); cause leakage = yes -- the program's own diagnostics (R_GenerateLookup: column without a patch; P_InitPicAnims: bad cycle from DBRAIN1 to DBRAIN4) and the reporter's description of the malformed TEXTURE1/PNAMES lumps
symptom: expected = the PWAD loads, as in Chocolate Doom and PrBoom+ ; observed = Crispy refuses it after texture lookup warnings with 'P_InitPicAnims: bad cycle' ; reproduction = crispy-doom -file reticue1.wad ; affected version = latest git at the time
KF-2 representability: not representable -- outside every native case of Artifact 1 (PWAD texture and animation validity; Artifact 3 lists PWAD validity as outside)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #655
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-08-26), body (335 chars); cause leakage = yes -- the triggering condition is identified (a mixed-case file name in the autoload directory is not loaded; all-lower or all-upper is)
symptom: expected = SIGIL auto-loads from the autoload directory as in 5.8.0 ; observed = since 5.9.0 it does not unless the file name is all lower- or upper-case; -file works ; reproduction = place SIGIL_v1_21.wad in the autoload directory ; affected version = 5.9.0 and git
KF-2 representability: partly -- the autoload directory's NAME is derived from the identified IWAD (NC-02: D_SaveGameIWADName, src/doom/d_main.c:1802), but which files in it are loaded, and how their names are matched, is outside every native case
KF-2 domain: out-of-domain -- D2 decides the IWAD's identification, not the loading of files from the autoload directory; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #657
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2020-08-28), body (1737 chars); cause leakage = yes, by class -- the reporter names it a vanilla limit (crusher stop affecting only the 30 lowest-numbered sectors of a tag); a test WAD attached, not opened
symptom: expected = a crusher-stop action stops every crusher sharing the tag ; observed = only the 30 lowest-numbered crusher sectors stop; the rest keep crushing ; reproduction = the attached 32crushers.wad with the quoted command line ; affected version = 5.9.0, Windows 8.1
KF-2 representability: not representable -- outside every native case of Artifact 1 (map special actions and a vanilla limit)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #677
disclosure: fields seen = title, labels (sound-issues-on-windows), state (closed), created_at (2020-10-06), body (747 chars); cause leakage = no
symptom: expected = MIDI music plays correctly ; observed = sometimes some instruments play at a higher pitch through a Roland JV-1010 over USB MIDI ; reproduction = none documented beyond the setup ; affected version = 5.9.1, Windows 10 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI output to external hardware)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #703
disclosure: fields seen = title, labels (bug, duplicate), state (open), created_at (2020-12-20), body (1605 chars); cause leakage = yes, partial -- the reporter states the mechanism observed ('If player is not moving horizontally, gravity isn't applied when the monster the player was standing on has moved'); a test map with a DEHACKED lump and a video attached, not opened
symptom: expected = the player falls when the monster beneath moves (the reporter notes vanilla has no over/under, so 'correct' is unclear) ; observed = with Walk Over/Under Monsters on, the player stays mid-air until a movement key is tapped ; reproduction = the seven steps quoted ; affected version = 5.10.0, Ubuntu 18.04
KF-2 representability: not representable -- outside every native case of Artifact 1 (movement physics of a Crispness feature)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #706
disclosure: fields seen = title, labels (duplicate, maybe-critical), state (closed), created_at (2021-01-09), body (609 chars); cause leakage = no
symptom: expected = the Pause key pauses demo playback as it pauses play ; observed = in Doom it does nothing during playback; in Heretic it opens the menu ; reproduction = press Pause during a demo ; affected version = 5.9.2, Windows 10
KF-2 representability: not representable -- outside every native case of Artifact 1 (demo playback control; a declared duplicate of the idea in #463)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #716
disclosure: fields seen = title, labels (sound-issues-on-windows), state (open), created_at (2021-02-07), body (883 chars); cause leakage = no
symptom: expected = MIDI music plays correctly ; observed = sometimes some instruments play at higher pitches through a Roland JV-1010; not seen in PrBoom+ ; reproduction = none documented beyond the setup ; affected version = 5.9.2 and 5.10.0, Windows 10 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI output to external hardware; the same symptom as #677)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #718
disclosure: fields seen = title, labels (sound-issues-on-windows), state (open), created_at (2021-02-16), body (451 chars); cause leakage = no
symptom: expected = the item pickup sound plays ; observed = on the 2021-02-15 win32 nightly build, ammo and health pickups are silent while music and most effects play; the 5.10.0 release is fine ; reproduction = DOOM1.WAD, default settings, Windows 10 ; affected version = nightly 20210215 (not 5.10.0)
KF-2 representability: not representable -- a single sound effect missing while the selected modules play everything else; NC-10's device selection is not in question
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #727
disclosure: fields seen = title, labels (bug, question, patch), state (open), created_at (2021-03-28), body (962 chars); cause leakage = no -- symptoms; two screenshots not opened
symptom: expected = the Windows mixer volume is unchanged by the program ; observed = after a demo recording completes and the program closes, the Windows mixer volume for it is set to 0, so the next launch is silent ; reproduction = the shortcut and command line quoted (-longtics -record) ; affected version = 5.10.0, Windows 10 19042
KF-2 representability: not representable -- outside every native case of Artifact 1 (the program's interaction with the Windows mixer)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #730
disclosure: fields seen = title, labels (bug), state (open), created_at (2021-04-02), body (941 chars); cause leakage = no -- symptoms and the loaded mods
symptom: expected = no crashes ; observed = four silent exits in three to four hours of BTSX E1 with several autoloaded WADs and a DEHACKED patch; no specific area ; reproduction = none reproducible ; affected version = 5.10.1, Windows 10 20H2
KF-2 representability: not representable -- outside every native case of Artifact 1 (an unlocalised crash)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #780
disclosure: fields seen = title, labels (sound-issues-on-windows), state (closed), created_at (2021-11-08), body (1804 chars); cause leakage = yes -- the reporter quotes the code (the `#if defined(_WIN32)` block of src/i_sdlmusic.c that starts midiproc for every music device but GUS, linked at another revision), names the cause as they see it (midiproc started although libfluidsynth is compiled into SDL2_mixer) and proposes a check
symptom: expected = with SDL2_mixer built against libfluidsynth and a soundfont configured, MIDI music plays through FluidSynth ; observed = crispy-midiproc is started with the Windows MS GS synth instead; removing crispy-midiproc.exe makes FluidSynth play ; reproduction = a MinGW 32-bit build of 5.10.3 / master with such an SDL2_mixer, Windows 10 64-bit ; affected version = 5.10.3 and latest master
KF-2 representability: partly -- the configured music device and its selection into a module are NC-10 (the SDL music module's devices, U1050-U1055; the frozen tree also lists a FluidSynth module of its own, music_fl_module serving SNDDEVICE_FSYNTH, U1046, a value the report does not mention); the midiproc start is a second decision on the same configured value inside the SDL music module's Init, as the reporter quotes it, which the native description covers only as 'able to initialise' (not checked against the frozen tree: KF-2 is decided from the frozen artifacts only)
KF-2 domain: in-domain concordant for what D10 decides -- a MIDI-class device value is SERVED by the first compiled-in module listing it whose Init succeeds, and SNDDEVICE_FSYNTH by the FluidSynth module (U1046); which synthesiser the SDL music module's Init then starts on Windows is decided by no class (Artifact 3 places even an Init failing for reasons outside the list out of domain) -- out-of-domain for the reported failure
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #807
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2022-01-04), body (1225 chars); cause leakage = yes -- the cause is stated with two line links into src/heretic/g_game.c at another revision (G_RecordDemo's own G_InitNew call reaches CheckCrispySingleplayer in G_DoLoadLevel before demorecording is set)
symptom: expected = Heretic refuses to record a demo with a singleplayer-only option such as -wandstart and exits with an error ; observed = recording starts and completes normally ; reproduction = crispy-heretic.exe -wandstart -record wandstart ; affected version = latest master (MSYS2 32-bit), Windows 10 64-bit
KF-2 representability: not representable -- outside every native case of Artifact 1 (the admission of demo recording under Crispy-only options; Artifact 1's Heretic cases are the HHE patch strings and versions, NC-06 and NC-07, and the shareware weapon gate, NC-08)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #814
disclosure: fields seen = title, labels (sound-issues-on-windows), state (closed), created_at (2022-01-12), body (842 chars); cause leakage = no -- symptoms and the setup; a video could not be uploaded
symptom: expected = MIDI music plays correctly ; observed = MIDI music plays incorrectly through a Roland JV-1010 (Doom 2, no mods, launched through ZDL); not in vanilla Doom or PrBoom+ ; reproduction = none documented beyond the setup ; affected version = 5.10.3 and the latest release, Windows 11
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI output to external hardware; the same symptom as #677 and #716)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #886
disclosure: fields seen = title, labels (bug, non-doom), state (closed), created_at (2022-05-31), body (7853 chars, CUT at 3000); cause leakage = yes, partial -- OpenBSD's 'backwards memcpy' abort is named and a gdb backtrace begins; within the cut only the libc frames (thrkill, _libc_abort, memcpy) appear, the Crispy frame lies beyond it
symptom: expected = no crash ; observed = crispy-heretic aborts (SIGABRT, 'backwards memcpy') shortly after E1M1 starts, walking toward the outside area ; reproduction = crispy-heretic 5.11.1 on OpenBSD 7.1-current amd64, E1M1 ; affected version = 5.11.1
KF-2 representability: not representable -- outside every native case of Artifact 1 (an overlapping memcpy somewhere in Heretic's level play, not localised within the cut; Artifact 1's Heretic cases NC-06, NC-07 and NC-08 do not reach level play)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #890
disclosure: fields seen = title, labels (bug, non-doom, pending, rendering), state (closed), created_at (2022-06-06), body (1030 chars); cause leakage = no -- symptoms; two screenshots not opened
symptom: expected = the widescreen armor widgets stay in place as in 4:3 ; observed = in 16:9 the armor display breaks once the armor class drops below 7 (Cleric with all four armor items), the widgets moving with every point lost ; reproduction = Hexen, Cleric, four armor items, take damage in widescreen ; affected version = a local build from eb016d4, Windows 10 32-bit
KF-2 representability: not representable -- outside every native case of Artifact 1 (status-bar rendering)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #893
disclosure: fields seen = title, labels (bug, pending), state (closed), created_at (2022-06-08), body (819 chars); cause leakage = no -- symptoms and the comparison builds; the reporter has not tracked it down
symptom: expected = the second internal demo (the Mage on Guardian of Fire) plays in sync ; observed = it desyncs in the latest builds, with vanilla settings too; not in the latest stable Crispy Hexen nor in the latest Chocolate Hexen builds ; reproduction = run Hexen built from e89cc04 and watch the second internal demo ; affected version = built from e89cc04, Windows 10 32-bit
KF-2 representability: partly -- Hexen's emulated version is NC-05's Hexen units (U1029-U1030), and Artifact 1 records that Hexen never persists the chosen version into its demos or savegames; the demo's contents and the simulation that must replay them are outside every native case
KF-2 domain: out-of-domain -- D5 decides only whether a -gameversion string is ACCEPTED (Hexen U1029-U1030), and Artifact 3 lists the loadability of Hexen savegames and demos (their fixed format text) as out of domain; a desync of a demo that loaded is further outside; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)

## KF item #1043
disclosure: fields seen = title, labels (bug), state (closed), created_at (2023-04-06), body (735 chars); cause leakage = yes, partial -- the reporter bisected the hang to one commit (5fd8c7627adffdad220afd8fd7371bdf7a5d3eb2, whose revert on 6.0 fixes it); the commit's content is not described in the first post
symptom: expected = a new game starts ; observed = the game hangs on New Game (the E1M1 music keeps playing) until the process is killed ; reproduction = Doom shareware (doom1.wad), New Game, on Linux ppc64le 6.1.20 ; affected version = since 5.12, 6.0
KF-2 representability: not representable -- outside every native case of Artifact 1 (a platform-specific hang at the start of a new game whose mechanism the first post does not give, a bisected commit only; the IWAD identification of NC-02 completed and the game reached its menu)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch (the first post gives a commit, not a mechanism; the environment, Linux ppc64le, is noted)
native replay: N/A (declared in advance, design Section 8)
