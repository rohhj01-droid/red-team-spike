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
KF-3: scope mismatch -- the external record is a design decision, not a cause: the maintainer marked the request wontfix because an invulnerability tell would hand an advantage to the Crispy player in games with Chocolate Doom clients (comment 2016-03-07) and closed it as irrelevant (2020-03-26); nothing read touches a native case, and KF-2's out-of-domain placement stands; cause agreement N/A (no failure, no fix)

## KF item #92
disclosure: fields seen = title, labels (wontfix, maybe-critical), state (closed), created_at (2016-03-07), body (457 chars); cause leakage = yes -- the body names the current mechanism it would replace ("the current pause/unpause dance that happens when a menu is opened while recording a demo") and MBF's basetic/gametic distinction; no failure is reported, a reminder to the maintainer
symptom: expected = none stated ; observed = none stated (a note that the pause/unpause handling while recording is error-prone) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- demo recording's tic bookkeeping is outside every native case (Artifact 3 lists a demo's contents as out of domain)
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- declined rather than diagnosed: the maintainer would not change the gametic bookkeeping because it breaks network compatibility with Chocolate Doom and older Crispy (comment 2016-05-26); closed 2020-03-26; cross-referenced from #174; KF-2's placement stands; cause agreement N/A

## KF item #174
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2017-03-28), body (865 chars); cause leakage = yes -- the reporter's hypothesis names code: "I believe this is because of `if (gametic & 3)` in `A_Tracer`", and a suggested fix (store `dest`, or save gametic); a video link not opened
symptom: expected = Revenant missiles keep homing after a saved game is loaded ; observed = after loading, missiles sometimes lose homing, randomly ; reproduction = save during homing missiles, load (video linked) ; affected version = not stated
KF-2 representability: partly -- the savegame's header and its load judgment are NC-05 (Artifact 1), but the fidelity of the restored game state (what the save body carries) is outside every native case; the symptom concerns the body, not the header
KF-2 domain: out-of-domain -- D5 decides only whether a Doom savegame is LOADABLE (its version string); this save loads, and what the frozen evidence does not define is the restored state's validity; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is identified (comments 2017-03-30 and 2017-04-04): whether a Revenant rocket homes depends on the parity of gametic when A_Tracer first runs, and a restored game calls every rocket's A_Tracer on the restore tic, so the parity is re-decided; Doom's savegame does not carry gametic. Doom Retro fixed it by writing gametic into its savegame header (bradharding/doomretro 77fa1a2, 2017-03-29); Crispy left it for network and demo compatibility (comments 2017-04-10, 2017-06-16) and closed it 2020-03-26. The cause lies in what the save body does not persist, outside D5's header check, where KF-2 placed it; cause agreement N/A (the frozen account named no cause)
KF-3 post-hoc observation: the artifact whose header NC-05 covers (a fact written by the save and judged at load) here fails for a fact the save does not write; an observation only -- it creates no unit, edge or finding (sealed Section 4.3)

## KF item #250
disclosure: fields seen = title, labels (bug, rendering), state (closed), created_at (2018-01-03), body (812 chars); cause leakage = yes, speculative -- the reporter's "possible explanation" (the far line of a sector leaving the top screen bound) and two renderer functions named as candidates; screenshots not opened
symptom: expected = items hidden by floors stay hidden ; observed = with mouse look, items "shine" through floors on E1M1 ; reproduction = E1M1 Hangar, mouse look, two screenshot positions ; affected version = not stated
KF-2 representability: not representable -- rendering is outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external record locates the symptom in the renderer's sprite clipping behind two-sided lines when the view looks down (R_StoreWallRange's silhouette conditions, comments 2018-01-08 to 2018-03-09); a partial patch exists only in Russian Doom (Russian-Doom/russian-doom b5eb9ec, 2018-01-09, src/doom/r_segs.c) and its author withdrew it as wrong on MAP19; closed unfixed 2020-03-26; KF-2's placement stands; cause agreement N/A

## KF item #258
disclosure: fields seen = title, labels (wontfix, maybe-critical), state (closed), created_at (2018-01-19), body (1072 chars); cause leakage = yes -- the cause is stated (an emulated vanilla bug at a named line of g_game.c) with a fix commit in another project linked and a test map attached (not opened)
symptom: expected = respawn fog appears at every deathmatch spot ; observed = no fog at spots facing angle 180 ; reproduction = the attached map with -solo-net -deathmatch -warp 01 ; affected version = not stated
KF-2 representability: not representable -- deathmatch spawn effects are game-world behaviour outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the cause was in the first post (an emulated vanilla bug); the external record adds only the decision: the fog's corrected position would differ between a Crispy and a Chocolate Doom client, so it was left as is (wontfix 2018-02-15; closed 2020-03-26); nothing touches a native case; cause agreement N/A

## KF item #318
disclosure: fields seen = title, labels (patch, maybe-critical, help wanted), state (closed), created_at (2018-05-14), body (610 chars); cause leakage = yes -- the body IS the fix: a diff replacing `actor->target->x` with `->y` in A_VileTarget, with the wiki page named
symptom: expected = Arch-Vile fire spawns at the target's position ; observed = spawned at the wrong location (x used for y) ; reproduction = none documented beyond the wiki ; affected version = not stated
KF-2 representability: not representable -- monster behaviour outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the cause (the x-for-y typo in A_VileTarget) was in the first post; the discussion (comments 2018-05-15 to 2018-05-22) weighed demo compatibility, with full-run demo tests reported in sync, and the issue was closed 2019-11-08 without a commit id in its timeline (comments 32-49 lie beyond the item cap, so the closing change is not identified here); outside every native case; cause agreement N/A

## KF item #362
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2018-12-02), body (208 chars); cause leakage = no -- a wiki page name only ("Lopsided final boss explosions"), the question whether it can be fixed without breaking demos or dehacked
symptom: expected = none stated beyond the wiki's title ; observed = final boss explosions lopsided (by title) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- not diagnosed beyond the wiki page: moving the exploding spawns is judged unsafe for demos and kill counts (comments 2018-12-03, 2019-10-15) and the issue was closed as irrelevant (2020-03-26); cause agreement N/A

## KF item #365
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2018-12-18), body (894 chars); cause leakage = yes -- the cause and the proposed change are stated with a line reference into p_enemy.c (the alive-player check in the boss death action)
symptom: expected = the episode ends when the ExM8 boss dies even if every player is dead (coop) ; observed = the ending is not triggered; players are stuck ; reproduction = Doom 1 coop, boss dies while all players are dead (rare) ; affected version = not stated
KF-2 representability: not representable -- level-end logic outside every native case
KF-2 domain: out-of-domain -- N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the cause was in the first post; the maintainer declined because level progression must stay identical to vanilla and Chocolate Doom for demos and network games (2018-12-19) and the reporter accepted it; cause agreement N/A

## KF item #408
disclosure: fields seen = title, labels (bug, pending, patch), state (closed), created_at (2019-04-24), body (4308 chars, CUT at 3000); cause leakage = yes, partial -- the console output shows "PadRejectArray: REJECT lump too short to pad!" before a segmentation fault and the start of a gdb session (the backtrace itself lies beyond the cut); the log also shows "This is not a valid dehacked patch file!" followed by a loaded DEHACKED lump -- the non-fatal signature path of deh_main.c:319-323 (XQA-07 d) seen in the wild
symptom: expected = Sunder.wad's maps load ; observed = crash after loading any of its 14 maps ; reproduction = ./crispy-doom -file sunder.wad -warp 01 ; affected version = 5.5.2 (released and git), Windows 10 x64 and Debian x32
KF-2 representability: not representable -- PWAD map loading is outside every native case (the one native mechanism visible in the log, the dehacked signature check, is a rejected enumerator, not a unit)
KF-2 domain: out-of-domain -- Artifact 3 lists PWAD and map validity as outside; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is identified and fixed in the tracker's repository (fabiangreffrath/crispy-doom 5e9069b, 2019-04-26, 'prevent flat lumps from being mistaken as patches', src/doom/r_data.c): sunder.wad carries a flat named BODIES, the patch-name lookup of R_InitTextures (W_CheckNumForName) returned that flat, and composing a texture from it read past the lump once composites were precached for every texture (c8abc70); the fix skips lumps in the flat range and moves R_InitFlats first. The dehacked signature line noted at KF-1 was unrelated. The cause lies in PWAD content handling, outside every native case, as KF-2 placed it; cause agreement N/A
KF-3 post-hoc observation: the cause is a lump-name lookup that ignores the lump's kind (the maintainer's own diagnosis of 2019-04-26: no namespaces for lumps); recorded as an observation only (sealed Section 4.3)

## KF item #454
disclosure: fields seen = title, labels (SDL-related, sound-issues-on-windows), state (closed), created_at (2019-09-10), body (870 chars); cause leakage = no -- symptoms, version and hardware only
symptom: expected = music and sound as in 5.5.2 ; observed = since 5.6, with the OPL (Adlib/Soundblaster) music device no music is heard while GUS (emulated) plays; "Digital sound effects" are high-pitched ; reproduction = select those devices on Win7 SP1 x64 with a Sound Blaster X-Fi ; affected version = 5.6+
KF-2 representability: representable for its setting -- the configured music and sfx devices are NC-10's inputs (snd_musicdevice = an OPL device, U1047-U1048; snd_sfxdevice = the SDL sound module's, U1056-U1061) and the module selection is NC-10's flow; the failure itself (silence from a served module; pitch) is behaviour inside the module, outside the native description
KF-2 domain: in-domain concordant for the part the rule decides -- D10: an OPL device value is SERVED(music_opl_module) and the digital sfx device SERVED(sound_sdl_module), provided their Init succeeds (an input the report leaves unstated and the rule does not decide); the external expectation (these are valid choices that should produce sound) agrees. The reported failure past the selection -- no audible music, wrong pitch -- is not decided by any class: for that part, out-of-domain
KF-2 attribution: scope mismatch -- the failure is not a validity phenomenon within the frozen scope; the device selection it depends on is concordant
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause lies in the SDL libraries, not the source port: with SDL2 2.0.10 / SDL2_mixer 2.0.4 on Windows and a 5.1 or 7.1 speaker layout, sound effects cut out or pitch up and music is silent; the older DLLs (SDL2 2.0.5, SDL2_mixer 2.0.1), a stereo layout or Windows Sonic restore sound (comments 2019-09-10 to 2020-04-17; reported upstream as SDL bug 4799, cross-referenced from libsdl-org/SDL#3396); the maintainer: 'solely an SDL issue and nothing that could be fixed in the source port' (2019-09-10). The one referenced commit (f105d6b, 2020-04-24) reverts an OPL stereo-channel change and is not the cause. KF-2's concordance for the device selection (D10) is untouched and its out-of-domain placement of the failure is confirmed; cause agreement N/A (the frozen account named no cause)

## KF item #457
disclosure: fields seen = title, labels (OS-specific, SDL-related, sound-issues-on-windows), state (closed), created_at (2019-09-22), body (1121 chars); cause leakage = no -- symptoms, two command lines, version and OS
symptom: expected = the same music volume whether or not SDL_SOUNDFONTS is set ; observed = music from a WAD is much quieter without the soundfont variable; music-pack playback unaffected ; reproduction = the two batch files quoted ; affected version = 5.6.2, Windows 7 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (music volume through the Windows MIDI process; the device selection of NC-10 is not in question)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the reporter located the cause outside the port: the quieter music came from the SDL2 2.0.5 / SDL2_mixer 2.0.1 pair they were running (under which midiproc does not start when FluidSynth is in use, while under 2.0.10 it starts either way) and the rest was the Windows mixer (comments 2019-09-24, 2019-09-25); 'in fact this is a Choco issue' (2019-09-27); closed. The library-version and mixer causes are outside the frozen scope, as KF-2 placed the failure; cause agreement N/A

## KF item #458
disclosure: fields seen = title, labels (duplicate, sound-issues-on-windows), state (closed), created_at (2019-09-22), body (1043 chars); cause leakage = yes -- the reporter's finding that copying 5.5.2's SDL2, SDL2_mixer and SDL2_net DLLs over 5.6's restores sound (a cause located in the library versions)
symptom: expected = sounds playing normally ; observed = since 5.6, no music with any settings and sound effects pitched up ; reproduction = original DOOM/DOOM2 WADs on Windows 10 x64, Sound Blaster Z ; affected version = 5.6 to 5.6.2
KF-2 representability: representable for its setting, as #454 -- the configured devices are NC-10's inputs; the failure (silence, pitch) is inside the modules, outside the native description
KF-2 domain: in-domain concordant for what D10 decides (a listed device is SERVED by its module, Init permitting); the failure past the selection is out-of-domain -- as #454, of which this is a declared duplicate
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- closed on its one comment as a duplicate of #454 (SDL2 2.0.10 with a 5.1 audio configuration; the old-DLL pack offered); the external cause is #454's, in the SDL libraries, outside the port; KF-2's concordance for the device selection (D10) is untouched and its placement of the failure confirmed; cause agreement N/A

## KF item #462
disclosure: fields seen = title, labels (OS-specific, SDL-related, sound-issues-on-windows), state (closed), created_at (2019-09-25), body (614 chars); cause leakage = no
symptom: expected = the music slider controls the volume of a virtual MIDI synth ; observed = the slider has no effect with that synth; it works with music packs and with the MS GS Wavetable synth ; reproduction = set VirtualMIDISynth as the default MIDI player ; affected version = 5.6.2, Windows 10 1903
KF-2 representability: not representable -- outside every native case of Artifact 1 (volume control of an external MIDI device)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- not diagnosed: the slider also fails with the Chocolate Doom daily build, and the maintainer closed it as 'nothing that can be fixed by the source port' (2019-09-27); the volume of an external virtual MIDI synth lies outside every native case, as KF-2 placed it; cause agreement N/A (no mechanism given)

## KF item #463
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2019-09-27), body (188 chars); cause leakage = no -- a feature idea (pause demo playback with the Pause key) with a side note that pausing mutes rather than pauses music
symptom: expected = none stated as a failure ; observed = demo playback cannot be paused ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case of Artifact 1 (demo playback control)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- a feature request, not a failure: the maintainer's one concern was basetic / leveltime drift (2019-09-27); the timeline shows three pull requests cross-referencing it (#798 and #799 'Demo pause and fast-forward', #802 'Enable demo pause', all closed 2021-12-27 to 2022-01-02) and the issue closed 2022-01-04 without a commit id; the pull requests were not fetched (request budget), so the resolution is recorded from the timeline only. Demo playback control stays outside every native case; cause agreement N/A

## KF item #475
disclosure: fields seen = title, labels (upstream, sound-issues-on-windows), state (closed), created_at (2019-10-10), body (1050 chars); cause leakage = yes -- the reporter names the component (midiproc's volume influences MP3/OGG/FLAC played from WADs) and shows the Windows mixer; the screenshot was not opened
symptom: expected = the MIDI process's volume does not influence music the main program plays ; observed = after setting music volume to 1 and relaunching with a music WAD, the music is almost inaudible ; reproduction = the four steps quoted ; affected version = 5.6.3, Windows 7 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (which process plays non-MIDI music)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: insufficient external causal evidence -- the thread (fourteen comments, 2019-10-10 to 2019-10-16) never establishes why the in-game volume stops controlling midiproc when a WAD's music lump is MP3/OGG/FLAC: the reporter proposes playing non-MIDI lumps in the main process, the maintainer refuses a workaround without the underlying reason ('I hate "I don't know why, but it works this way" kind of solutions', 2019-10-14), a volume-resync patch did not help, and the issue was closed as orphaned (2022-02-02). The symptom (which process plays a lump, and the mixer coupling) stays outside the frozen scope, as KF-2 placed it; cause agreement N/A

## KF item #498
disclosure: fields seen = title, labels (OS-specific, SDL-related, sound-issues-on-windows), state (closed), created_at (2019-11-25), body (953 chars); cause leakage = no -- symptoms and the reporter's tool chain; two audio links not opened
symptom: expected = SIGIL's MIDI plays at an even volume as in PrBoom+ ; observed = a passage of the first SIGIL level's MIDI plays very quietly through VST MIDI players ; reproduction = SIGIL E5M1 with a VSTi MIDI player ; affected version = 5.6.3, Windows 10
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI rendering by an external synth)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the maintainer could not reproduce it ('I will never be able to reproduce this', 2019-11-26); the reporter later made the passage play by hosting the Sound Canvas VA plugin in a 64-bit host and by resetting the MIDI player before the SIGIL episode (comments 2019-11-27, 2019-12-01), which places the cause in the external MIDI host and its plugins; the thread also ties the reporter's baseline to the old-DLL workaround of #454. Outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #524
disclosure: fields seen = title, labels (bug, pending, patch), state (closed), created_at (2020-02-21), body (812 chars); cause leakage = yes, a hypothesis -- the reporter attributes the corruption to switching widescreen at the moment memory is being rearranged ("at the moment it would corrupt memory"); the screenshot was not opened
symptom: expected = switching widescreen on at that moment is disallowed or harmless ; observed = wall textures become 'Tutti-Frutti' when widescreen is switched on exactly as the intro music stops and the demo's map loads ; reproduction = the steps quoted ; affected version = 5.7, Windows 10
KF-2 representability: not representable -- outside every native case of Artifact 1 (rendering / screen reallocation timing)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is identified and fixed in the tracker's repository: the widescreen (and high-resolution) toggle is applied by a post-rendering hook, and when it ran during a screen wipe the wipe's buffers, allocated at the old size, were overrun -- zone-memory corruption, a silent crash on Windows (comments 2020-02-24 to 2020-02-28; 'Yep, it's the wipe!', 2020-02-28); fix fabiangreffrath/crispy-doom d62113a (2020-03-02, 'never change screen resolution during a wipe', src/doom/d_main.c: the hook is skipped while a wipe is in progress). The reporter's first-post hypothesis (memory being rearranged at that moment) was right in substance. Rendering timing, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #527
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-02-24), body (26 chars: "Bug report from the forum."); cause leakage = no
symptom: expected = none stated beyond the title ; observed = the MAP/WAD automap text widget placed badly in widescreen mode (by title) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case of Artifact 1 (automap HUD layout)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- no comments; closed by commit fabiangreffrath/crispy-doom 6c5a3a6 (2020-02-24, 'don't draw the obtrusive MAP/WAD automap text widget in widescreen mode', src/doom/hu_stuff.c: the line is not drawn when widescreen is on). HUD layout, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #528
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-02-24), body (26 chars); cause leakage = no
symptom: expected = none stated beyond the title ; observed = automap markers do not transform well in rotate mode in widescreen (by title) ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- outside every native case of Artifact 1 (automap rendering)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- no comments; closed by commit fabiangreffrath/crispy-doom 4a64201 (2020-02-24, 'fix horizontal coordinates of automap markers in widescreen mode', src/doom/am_map.c: the marker's x coordinate now subtracts DELTAWIDTH). Automap rendering, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #556
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2020-03-23), body (347 chars); cause leakage = no -- a suggestion about weapon-key double tapping, with the reporter unsure of demo/network safety
symptom: expected = none stated as a failure (a suggestion: fast double tap of 3 selects the shotgun at once) ; observed = tapping 3 selects SSG first, shotgun second ; reproduction = none documented ; affected version = not stated
KF-2 representability: not representable -- Doom weapon selection; the only weapon-change case in Artifact 1 is Heretic's shareware gate (NC-08), which does not cover Doom's key handling
KF-2 domain: out-of-domain -- D8 decides Heretic weapon-change requests only; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external record explains Doom's weapon-key resolution and rejects the change: the key for the shotgun selects it only when the super shotgun is not owned or is already the ready weapon (src/doom/p_user.c, comments 2020-03-26), what a tic records for demos and network games is 'player pressed 3', not the weapon, and the engine decides from that (2020-03-27); closed as game mechanics not to be refactored (2020-04-16). Doom weapon selection stays outside every native case (the only weapon-change case is Heretic's shareware gate, NC-08), as KF-2 placed it; cause agreement N/A

## KF item #646
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-08-03), body (1374 chars); cause leakage = yes -- the program's own diagnostics (R_GenerateLookup: column without a patch; P_InitPicAnims: bad cycle from DBRAIN1 to DBRAIN4) and the reporter's description of the malformed TEXTURE1/PNAMES lumps
symptom: expected = the PWAD loads, as in Chocolate Doom and PrBoom+ ; observed = Crispy refuses it after texture lookup warnings with 'P_InitPicAnims: bad cycle' ; reproduction = crispy-doom -file reticue1.wad ; affected version = latest git at the time
KF-2 representability: not representable -- outside every native case of Artifact 1 (PWAD texture and animation validity; Artifact 3 lists PWAD validity as outside)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is identified and fixed in the tracker's repository: Crispy merges texture definitions from every PNAMES and TEXTURE1/2 lump, so it still knew DBRAIN1 from the IWAD when the PWAD's own TEXTURE1 lacked it, and tried to build the animation cycle that vanilla and Chocolate Doom silently skip (comments 2020-08-10); fix fabiangreffrath/crispy-doom 3911122 (2020-08-10, 'skip invalid animation sequences', src/doom/p_spec.c: the I_Error in P_InitPicAnims becomes a stderr warning and the sequence is skipped, marked '[crispy] make non-fatal'). PWAD texture validity, outside every native case, as KF-2 placed it; cause agreement N/A
KF-3 post-hoc observation: a second instance of the shape XQA-07 (d) recorded for deh_signatures -- the fork turns a refusing validity check into a warning that lets the input through ('[crispy] make non-fatal'); an observation only, outside P_raw (sealed Sections 4.3, 8.6)

## KF item #655
disclosure: fields seen = title, labels (bug), state (closed), created_at (2020-08-26), body (335 chars); cause leakage = yes -- the triggering condition is identified (a mixed-case file name in the autoload directory is not loaded; all-lower or all-upper is)
symptom: expected = SIGIL auto-loads from the autoload directory as in 5.8.0 ; observed = since 5.9.0 it does not unless the file name is all lower- or upper-case; -file works ; reproduction = place SIGIL_v1_21.wad in the autoload directory ; affected version = 5.9.0 and git
KF-2 representability: partly -- the autoload directory's NAME is derived from the identified IWAD (NC-02: D_SaveGameIWADName, src/doom/d_main.c:1802), but which files in it are loaded, and how their names are matched, is outside every native case
KF-2 domain: out-of-domain -- D2 decides the IWAD's identification, not the loading of files from the autoload directory; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is identified and fixed: the autoload looked for the Sigil WADs under upper-case names only, while the files ship mixed-case, which a case-sensitive file system does not match ('Sigh, mixed-case file names on case-sensitive file systems', 2020-08-27); fix fabiangreffrath/crispy-doom 7b30ea0 (2020-08-27, 'consider Sigil's mixed case file names', src/doom/d_pwad.c: the three names of sigil_wads[] re-cased). Which files the autoload loads stays outside every native case, as KF-2 placed it; cause agreement N/A
KF-3 post-hoc observation: the list the fix edits is an enumerator of the inventory's kind -- accepted file names matched against the file system -- and at the frozen revision it is a function-scope initializer (src/doom/d_pwad.c:45, inside LoadSigilWad :38, consulted :93-103), which class K1 (file-scope initializers) cannot generate; K1's three d_pwad.c candidates (C036, C037; Hexen's C306) do not include it, and the nearest of them, masterlevels_wads (C037), was rejected at EN2 as 'discovery of known files, not acceptance of input', so the same test would likely have rejected this list as well. An L2 instance recorded for Run 2 beside XQA-04's two idioms; it creates no candidate, unit or finding (sealed Sections 4.3, 8.6)

## KF item #657
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2020-08-28), body (1737 chars); cause leakage = yes, by class -- the reporter names it a vanilla limit (crusher stop affecting only the 30 lowest-numbered sectors of a tag); a test WAD attached, not opened
symptom: expected = a crusher-stop action stops every crusher sharing the tag ; observed = only the 30 lowest-numbered crusher sectors stop; the rest keep crushing ; reproduction = the attached 32crushers.wad with the quoted command line ; affected version = 5.9.0, Windows 8.1
KF-2 representability: not representable -- outside every native case of Artifact 1 (map special actions and a vanilla limit)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the cause (MAXCEILINGS, a vanilla limit) was in the first post; the maintainer asked what removing it would do to demos exchanged with vanilla (2020-08-28) and the reporter withdrew the request as a limit Crispy respects, like the lost-soul limit; closed unfixed the same day; cause agreement N/A

## KF item #677
disclosure: fields seen = title, labels (sound-issues-on-windows), state (closed), created_at (2020-10-06), body (747 chars); cause leakage = no
symptom: expected = MIDI music plays correctly ; observed = sometimes some instruments play at a higher pitch through a Roland JV-1010 over USB MIDI ; reproduction = none documented beyond the setup ; affected version = 5.9.1, Windows 10 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI output to external hardware)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: insufficient external causal evidence -- closed the same day as outside the port ('it's not the port's responsibility to actually render the MIDI music content', 2020-10-14); a later comment (2020-10-23) hypothesises that no GM/GS reset is sent between songs so parameters carry over from one song to the next, and went unanswered. No cause was established; the symptom stays outside every native case, as KF-2 placed it (see #716 for the later note on native Windows MIDI)

## KF item #703
disclosure: fields seen = title, labels (bug, duplicate), state (open), created_at (2020-12-20), body (1605 chars); cause leakage = yes, partial -- the reporter states the mechanism observed ('If player is not moving horizontally, gravity isn't applied when the monster the player was standing on has moved'); a test map with a DEHACKED lump and a video attached, not opened
symptom: expected = the player falls when the monster beneath moves (the reporter notes vanilla has no over/under, so 'correct' is unclear) ; observed = with Walk Over/Under Monsters on, the player stays mid-air until a movement key is tapped ; reproduction = the seven steps quoted ; affected version = 5.10.0, Ubuntu 18.04
KF-2 representability: not representable -- outside every native case of Artifact 1 (movement physics of a Crispness feature)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the maintainer acknowledged the over/under feature's vertical movement as still broken, tied to #381 (2020-12-21); the issue is open. A 2026 fork (Paf2020/crispy-doom-zaxis-fix, commits 906a636 and d6ca5b4) proposes re-syncing things standing on a supporter that moved and updating heights in P_XYMovement, offered as pull request fabiangreffrath/crispy-doom#1370 'Z Axis Fix' (open at the time of reading, so not in the frozen revision; a Woof port, #2932, closed 2026-10-01); the pull requests were not fetched (request budget). Physics of a fork feature, outside every native case, as KF-2 placed it; cause agreement N/A (a proposed cause from a fork, not a maintainer diagnosis)

## KF item #706
disclosure: fields seen = title, labels (duplicate, maybe-critical), state (closed), created_at (2021-01-09), body (609 chars); cause leakage = no
symptom: expected = the Pause key pauses demo playback as it pauses play ; observed = in Doom it does nothing during playback; in Heretic it opens the menu ; reproduction = press Pause during a demo ; affected version = 5.9.2, Windows 10
KF-2 representability: not representable -- outside every native case of Artifact 1 (demo playback control; a declared duplicate of the idea in #463)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- closed as a duplicate of #463 on the reporter's own confirmation (2021-01-09); nothing further; cause agreement N/A

## KF item #716
disclosure: fields seen = title, labels (sound-issues-on-windows), state (open), created_at (2021-02-07), body (883 chars); cause leakage = no
symptom: expected = MIDI music plays correctly ; observed = sometimes some instruments play at higher pitches through a Roland JV-1010; not seen in PrBoom+ ; reproduction = none documented beyond the setup ; affected version = 5.9.2 and 5.10.0, Windows 10 x64
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI output to external hardware; the same symptom as #677)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: insufficient external causal evidence -- never diagnosed: comments place the symptom with external MIDI modules across several ports (2021-08-06), suggest a VST host feature (2022-02-23), and a later comment says it is 'likely resolved with the current native Windows MIDI support' (2022-02-23) -- the module the frozen tree carries as music_win_module (NC-10, U1062-U1066) -- without a cause stated; the issue is open. Outside every native case, as KF-2 placed it

## KF item #718
disclosure: fields seen = title, labels (sound-issues-on-windows), state (open), created_at (2021-02-16), body (451 chars); cause leakage = no
symptom: expected = the item pickup sound plays ; observed = on the 2021-02-15 win32 nightly build, ammo and health pickups are silent while music and most effects play; the 5.10.0 release is fine ; reproduction = DOOM1.WAD, default settings, Windows 10 ; affected version = nightly 20210215 (not 5.10.0)
KF-2 representability: not representable -- a single sound effect missing while the selected modules play everything else; NC-10's device selection is not in question
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the maintainer's diagnosis, hedged: the nightly build is compiled against an SDL2 built without DirectX support while the release is full-featured, 'so this is pretty sure a driver problem' (2021-02-16); a later comment surveys the Windows audio backends and SDL_AUDIODRIVER; cross-referenced from chocolate-doom/chocolate-doom#1311; open, unfixed. Build library and audio driver, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #727
disclosure: fields seen = title, labels (bug, question, patch), state (open), created_at (2021-03-28), body (962 chars); cause leakage = no -- symptoms; two screenshots not opened
symptom: expected = the Windows mixer volume is unchanged by the program ; observed = after a demo recording completes and the program closes, the Windows mixer volume for it is set to 0, so the next launch is silent ; reproduction = the shortcut and command line quoted (-longtics -record) ; affected version = 5.10.0, Windows 10 19042
KF-2 representability: not representable -- outside every native case of Artifact 1 (the program's interaction with the Windows mixer)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the mechanism is identified in substance: opening the menu or pausing while recording a demo pauses the game and mutes audio, the mute reaches the Windows mixer through midiproc (MIDI playback only; OPL and GUS unaffected), and Windows keeps that per-application volume across runs; a one-line patch (S_ResumeSound before 'Demo recorded') helped in game but not when a new game follows the finished recording (comments 2021-04-06 to 2021-05-15); open, unfixed. Demo-recording pause handling and the OS mixer, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #730
disclosure: fields seen = title, labels (bug), state (open), created_at (2021-04-02), body (941 chars); cause leakage = no -- symptoms and the loaded mods
symptom: expected = no crashes ; observed = four silent exits in three to four hours of BTSX E1 with several autoloaded WADs and a DEHACKED patch; no specific area ; reproduction = none reproducible ; affected version = 5.10.1, Windows 10 20H2
KF-2 representability: not representable -- outside every native case of Artifact 1 (an unlocalised crash)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: insufficient external causal evidence -- one crash caught under gdb in R_DrawColumn's brightmap lookup (r_draw.c:173) after thirty minutes of play with four autoloaded PWADs, never reproduced again (Valgrind clean, 2021-04-04); a 2026 comment withdrew a claimed fix; cross-referenced from Russian-Doom/russian-doom#272; open. Outside every native case, as KF-2 placed it

## KF item #780
disclosure: fields seen = title, labels (sound-issues-on-windows), state (closed), created_at (2021-11-08), body (1804 chars); cause leakage = yes -- the reporter quotes the code (the `#if defined(_WIN32)` block of src/i_sdlmusic.c that starts midiproc for every music device but GUS, linked at another revision), names the cause as they see it (midiproc started although libfluidsynth is compiled into SDL2_mixer) and proposes a check
symptom: expected = with SDL2_mixer built against libfluidsynth and a soundfont configured, MIDI music plays through FluidSynth ; observed = crispy-midiproc is started with the Windows MS GS synth instead; removing crispy-midiproc.exe makes FluidSynth play ; reproduction = a MinGW 32-bit build of 5.10.3 / master with such an SDL2_mixer, Windows 10 64-bit ; affected version = 5.10.3 and latest master
KF-2 representability: partly -- the configured music device and its selection into a module are NC-10 (the SDL music module's devices, U1050-U1055; the frozen tree also lists a FluidSynth module of its own, music_fl_module serving SNDDEVICE_FSYNTH, U1046, a value the report does not mention); the midiproc start is a second decision on the same configured value inside the SDL music module's Init, as the reporter quotes it, which the native description covers only as 'able to initialise' (not checked against the frozen tree: KF-2 is decided from the frozen artifacts only)
KF-2 domain: in-domain concordant for what D10 decides -- a MIDI-class device value is SERVED by the first compiled-in module listing it whose Init succeeds, and SNDDEVICE_FSYNTH by the FluidSynth module (U1046); which synthesiser the SDL music module's Init then starts on Windows is decided by no class (Artifact 3 places even an Init failing for reasons outside the list out of domain) -- out-of-domain for the reported failure
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the one comment names the fix, fabiangreffrath/crispy-doom 5582295 (2021-11-19, a merge from chocolate-doom carrying src/i_sdlmusic.c): I_SDL_InitMusic now records whether a FluidSynth soundfont is configured and present, and the Windows MIDI path is opened only 'if (snd_musicdevice != SNDDEVICE_GUS && !fluidsynth_sf_is_set)' -- the branch inside the module's Init gained a configuration predicate; the device selection that D10 decides is untouched. That confirms KF-2's placement: concordant for the selection, out-of-domain for the Init's own branch; cause agreement N/A (the frozen account named no cause)
KF-3 post-hoc observation: the fix decides inside the SDL music module's Init, on the device value and a path setting, which synthesiser serves MIDI; the frozen tree carries a FluidSynth module of its own (music_fl_module serving SNDDEVICE_FSYNTH, U1046), which this 2021 fix does not have -- a choice made inside Init there is a device value the selection decides here; an observation only, outside P_raw (sealed Sections 4.3, 8.6)

## KF item #807
disclosure: fields seen = title, labels (maybe-critical), state (closed), created_at (2022-01-04), body (1225 chars); cause leakage = yes -- the cause is stated with two line links into src/heretic/g_game.c at another revision (G_RecordDemo's own G_InitNew call reaches CheckCrispySingleplayer in G_DoLoadLevel before demorecording is set)
symptom: expected = Heretic refuses to record a demo with a singleplayer-only option such as -wandstart and exits with an error ; observed = recording starts and completes normally ; reproduction = crispy-heretic.exe -wandstart -record wandstart ; affected version = latest master (MSYS2 32-bit), Windows 10 64-bit
KF-2 representability: not representable -- outside every native case of Artifact 1 (the admission of demo recording under Crispy-only options; Artifact 1's Heretic cases are the HHE patch strings and versions, NC-06 and NC-07, and the shareware weapon gate, NC-08)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the maintainers confirmed the first post's cause (the check runs at level load, before G_RecordDemo has set demorecording: 'the checks in the code should get moved a bit in order to error out as soon as possible', 2022-01-06; the preferred fix: factor the checks out and call them at D_ConnectNetGame, G_RecordDemo, G_DoPlayDemo and G_TimeDemo, 2022-01-07) and closed it on the merge of pull request #796 'Custom difficulty parameters' (fabiangreffrath/crispy-doom 8bb1ccf, 2022-02-04; its commit list includes 'Disable demo recording with -autohealth in Heretic and Hexen', 'Demo reel checks for critical params', 'Custom parameters fixes'; 21 files, the Heretic change not among the five displayed). The admission of demo recording under singleplayer-only options stays outside every native case, as KF-2 placed it; cause agreement N/A
KF-3 post-hoc observation: the failure is a validity check evaluated at a transition (level load) before the action under way (record) had written the state the check reads (demorecording) -- the ordering that Phase 3's transition-local judgment role exists to fix, met here in a mechanism outside every native case; an observation only (sealed Sections 4.3, 8.6)

## KF item #814
disclosure: fields seen = title, labels (sound-issues-on-windows), state (closed), created_at (2022-01-12), body (842 chars); cause leakage = no -- symptoms and the setup; a video could not be uploaded
symptom: expected = MIDI music plays correctly ; observed = MIDI music plays incorrectly through a Roland JV-1010 (Doom 2, no mods, launched through ZDL); not in vanilla Doom or PrBoom+ ; reproduction = none documented beyond the setup ; affected version = 5.10.3 and the latest release, Windows 11
KF-2 representability: not representable -- outside every native case of Artifact 1 (MIDI output to external hardware; the same symptom as #677 and #716)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- resolved without a stated cause: 'Recently, Windows MIDI support has been redesigned' (2022-01-12) and the reporter confirmed 'The MIDI bug is fixed in the latest daily build' (2022-01-13); closed. The MIDI rendering path is outside every native case, as KF-2 placed it; the redesigned module is in the frozen tree as NC-10's music_win_module (U1062-U1066), whose selection D10 decides and whose rendering no class does; cause agreement N/A (fixed by a redesign, no cause stated)

## KF item #886
disclosure: fields seen = title, labels (bug, non-doom), state (closed), created_at (2022-05-31), body (7853 chars, CUT at 3000); cause leakage = yes, partial -- OpenBSD's 'backwards memcpy' abort is named and a gdb backtrace begins; within the cut only the libc frames (thrkill, _libc_abort, memcpy) appear, the Crispy frame lies beyond it
symptom: expected = no crash ; observed = crispy-heretic aborts (SIGABRT, 'backwards memcpy') shortly after E1M1 starts, walking toward the outside area ; reproduction = crispy-heretic 5.11.1 on OpenBSD 7.1-current amd64, E1M1 ; affected version = 5.11.1
KF-2 representability: not representable -- outside every native case of Artifact 1 (an overlapping memcpy somewhere in Heretic's level play, not localised within the cut; Artifact 1's Heretic cases NC-06, NC-07 and NC-08 do not reach level play)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is identified and fixed: Crispy Heretic's sprite-clipping copy used sizeof(lastopening), the size of a pointer, where sizeof(*lastopening), the size of an int, was meant (src/heretic/r_segs.c, two lines), so a 64-bit build copies twice the bytes and the regions overlap -- which OpenBSD's memcpy turns into an abort; a typo from the 2017 Crispy Heretic implementation (pull request #242), fixed by pull request #887 'Heretic: refer to pointer, not to integer' (closed 2022-05-31; the reporter confirmed on commit c14260f). Renderer, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #890
disclosure: fields seen = title, labels (bug, non-doom, pending, rendering), state (closed), created_at (2022-06-06), body (1030 chars); cause leakage = no -- symptoms; two screenshots not opened
symptom: expected = the widescreen armor widgets stay in place as in 4:3 ; observed = in 16:9 the armor display breaks once the armor class drops below 7 (Cleric with all four armor items), the widgets moving with every point lost ; reproduction = Hexen, Cleric, four armor items, take damage in widescreen ; affected version = a local build from eb016d4, Windows 10 32-bit
KF-2 representability: not representable -- outside every native case of Artifact 1 (status-bar rendering)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- 'I see the cause of this issue and will submit a fix this evening' (2022-06-06); fixed by pull request #891 'Make V_DrawAltTLPatch() widescreen-compatible' (closed 2022-06-07; the issue closed the same day): a translucent patch drawer that did not take the widescreen offset into account, by its title; the pull request was not fetched. Status-bar rendering, outside every native case, as KF-2 placed it; cause agreement N/A

## KF item #893
disclosure: fields seen = title, labels (bug, pending), state (closed), created_at (2022-06-08), body (819 chars); cause leakage = no -- symptoms and the comparison builds; the reporter has not tracked it down
symptom: expected = the second internal demo (the Mage on Guardian of Fire) plays in sync ; observed = it desyncs in the latest builds, with vanilla settings too; not in the latest stable Crispy Hexen nor in the latest Chocolate Hexen builds ; reproduction = run Hexen built from e89cc04 and watch the second internal demo ; affected version = built from e89cc04, Windows 10 32-bit
KF-2 representability: partly -- Hexen's emulated version is NC-05's Hexen units (U1029-U1030), and Artifact 1 records that Hexen never persists the chosen version into its demos or savegames; the demo's contents and the simulation that must replay them are outside every native case
KF-2 domain: out-of-domain -- D5 decides only whether a -gameversion string is ACCEPTED (Hexen U1029-U1030), and Artifact 3 lists the loadability of Hexen savegames and demos (their fixed format text) as out of domain; a desync of a demo that loaded is further outside; N/A
KF-2 attribution: scope mismatch
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the cause is the fork's own: the new Heretic/Hexen mouselook code (9ab1e67e) did not apply the MLOOKUNIT factor everywhere ('I'm guessing this is my fault', 2022-06-08); fixed by pull request #894, merged as fabiangreffrath/crispy-doom 83d50fc (2022-06-08, 'Heretic/Hexen: Further mouselook and mouselook-adjacent improvements', first item 'HH: Simplify usage of MLOOKUNIT'), confirmed by the reporter on the branch. A desync of the demo's simulation under playback, outside every native case, as KF-2 placed it (D5 decides only the -gameversion string, and Artifact 3 lists Hexen demo loadability as outside); cause agreement N/A

## KF item #1043
disclosure: fields seen = title, labels (bug), state (closed), created_at (2023-04-06), body (735 chars); cause leakage = yes, partial -- the reporter bisected the hang to one commit (5fd8c7627adffdad220afd8fd7371bdf7a5d3eb2, whose revert on 6.0 fixes it); the commit's content is not described in the first post
symptom: expected = a new game starts ; observed = the game hangs on New Game (the E1M1 music keeps playing) until the process is killed ; reproduction = Doom shareware (doom1.wad), New Game, on Linux ppc64le 6.1.20 ; affected version = since 5.12, 6.0
KF-2 representability: not representable -- outside every native case of Artifact 1 (a platform-specific hang at the start of a new game whose mechanism the first post does not give, a bisected commit only; the IWAD identification of NC-02 completed and the game reached its menu)
KF-2 domain: out-of-domain -- no class of Artifact 3 decides it; N/A
KF-2 attribution: scope mismatch (the first post gives a commit, not a mechanism; the environment, Linux ppc64le, is noted)
native replay: N/A (declared in advance, design Section 8)
KF-3: scope mismatch -- the external cause is the compiler: clang on ppc64le miscompiles a tail-recursive angle-difference function so that its branch is always taken (a minimal reproducer loops forever; confirmed with an LLVM developer; llvm/llvm-project#62294), and the Crispy commit the reporter had bisected to (5fd8c76) only exposed it; the reporter closed it as 'a compiler bug and not crispy-doom bug' (2023-04-22). Outside the port, as KF-2 placed the hang; cause agreement N/A

## X13 seal -- KF-2 sealed

sealed at 2026-10-29T08:59:32Z. 37 items (#90 .. #1043), in id order, each with its
disclosure line, KF-1 symptom fields and KF-2 lines; the set equals
`kf_items.tsv` (X12). No comment, linked commit, pull request or
third-party source was read for any item (design 5.2); the bodies of
#408 and #886 were cut at 3,000 characters. Counts recomputed from the
item lines above:

```text
in-domain concordant        3   #454, #458, #780
in-domain DISCORDANT        0   --
in-domain indeterminate     0   --
out-of-domain              34   #90, #92, #174, #250, #258, #318, #362, #365, #408, #457, #462, #463, #475, #498, #524, #527, #528, #556, #646, #655, #657, #677, #703, #706, #716, #718, #727, #730, #807, #814, #886, #890, #893, #1043

representable               2   #454, #458
partly                      4   #174, #655, #780, #893
not representable          31   the rest

attribution: scope mismatch 37

cause leakage yes          18   #92, #174, #250, #258, #318, #365, #408, #458, #475, #524, #646, #655, #657, #703, #780, #807, #886, #1043
cause leakage no           19
```

The three in-domain concordant results (#454, #458, #780) are each
concordant for the device selection the report rests on (D10) with the
reported failure itself out-of-domain; no item is in-domain DISCORDANT
or indeterminate. Nothing above this line is edited after this commit;
KF-3 lines are appended per item at X14 (design 5.3), below each
item's `native replay` line, and nothing else changes.
