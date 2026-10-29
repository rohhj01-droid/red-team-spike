# Artifact 3 -- derived judgment specification -- EXPLORATORY C084 study

EXPLORATORY. Written after Artifact 2 was committed (`bc6361d`, X10b),
per sealed §9 (Artifact 3) and design Section 10. Two things are frozen
here, the domain first: which transitions and histories this
specification claims to decide, bounded by what the frozen external
validity evidence (the accept/refuse behaviour of the 23 admitted
enumerators as described in Artifact 1; no normative source was
admitted, XQA-07 b) actually decides; and a decision procedure that is
total within that domain. Inclusion is mechanical (sealed §9): where
the frozen evidence supplies a verdict for a case, the case is inside;
where it does not define the case's validity, the case is outside and
is reported as out-of-domain, never decided by invention. This is a
specification, not a simulator (sealed §10): it states enough to
determine a verdict on a described history without consulting anything
revealed later.

## Applicability domain

Each class names the transition or history it decides, the native case
whose evidence decides it, and the inputs a described case must supply.
A described case is IN the domain when it is one of these and supplies
the inputs; it is OUT when it is none of these, when it concerns a game
module the class does not cover, or when it lacks an input the rule
needs.

```text
D1   (NC-01) macOS launcher: a file opened with the launcher application
     inputs: the file's last path component
     also: a launch attempt; input: whether a configured slot is selected
D2   (NC-02) engine startup: identification of the IWAD
     inputs: the module (doom / heretic / hexen / strife); whether -iwad
     was given and, if so, whether the named file exists and its
     basename; otherwise which registry names exist in the search
     directories; for the Doom module, whether the loaded lumps contain
     MAP01 or E1M1
D3   (NC-03) network: a connect request's (mission, mode); a later
     client's (mission, mode) against the session's adopted pair; the
     controller's (episode, map) for the adopted pair; Heretic's -warp
     and warp cheat (episode, map) under its gamemode
     inputs: mission, mode, episode, map; for a later client, the pair
     adopted from the first client
D4   (NC-04) network: the controller's game version for the adopted
     mission
     inputs: mission, version (and the other settings the same check
     reads first: ticdup, extratics, deathmatch, skill, episode, map)
D5   (NC-05) the -gameversion argument of the Doom, Hexen and Strife
     modules; a Doom-module savegame's loadability; a Doom-module
     demo's playability
     inputs: the argument string and the module; for a savegame, its
     header's version string and the running version; for a demo, its
     first byte, the running version, and whether it is a single demo
     or part of the demo loop
D6   (NC-06) Heretic HHE patch: a "Text <offset> <length>" section
     inputs: the offset, the running HHE version, the replacement
     length, the original string's length (from the main table), and
     whether long strings are allowed
D7   (NC-07) Heretic: the -hhever argument
     inputs: the argument string
D8   (NC-08) Heretic: a weapon-change request
     inputs: the requested weapon, the ready weapon, the player's
     ownership flags, gamemode
D9   (NC-09) Hexen MAPINFO: a token inside a MAP block
     inputs: the token
D10  (NC-10) sound: a configured sfx or music device value
     inputs: the value, which modules are compiled in and their order,
     and whether a module's Init succeeds
D11  (NC-11) a dedicated server's command line
     inputs: the set of parameters present
D12  (NC-12) setup tool: a joystick pressed during calibration that SDL
     does not report as a game controller
     inputs: its reported name, axes, buttons, hats
D13  (NC-13) setup tool: the -game argument
     inputs: the argument string
D14  (NC-14) engine startup: the loaded WAD directory under module M
     inputs: M and whether each of the other three games' marker lumps
     is present
```

Outside the domain, by the same rule, and so never decided here: the
loadability of Hexen and Strife savegames and demos (their fixed format
texts belong to no admitted enumerator); the validity of a PWAD, a map,
a demo's contents, a network protocol version, or any game-rule
transition other than D8; any Doom-module -warp or -episode value (the
Doom module does not consult valid_modes for it); a device value's
behaviour when the module's Init fails for reasons outside the list;
anything about a version of the target other than `7775ef82`.

## Decision procedure

Each rule reads only the frozen tables (the units of `P_raw.tsv`, by
enumerator) and the inputs listed above, and returns one of the
verdicts named. Where the native system distinguishes degrees of
refusal, the verdict names the degree, because the external evidence
does.

```text
D1   RECOGNISED(type T) iff the file's last path component equals,
     case-insensitively, the row of IWADFilenames for T (U001-U011);
     else NOT-AN-IWAD (treated as a command-line file)
     LAUNCH-PERMITTED iff a configured slot is selected; else REFUSED
     ("No IWAD selected")
D2   with -iwad F: NOT-FOUND (abort) if F does not exist; else
     IDENTIFIED(M) if F's basename equals a registry row (U012-U028)
     whose mission the module's mask admits; else, Doom module only,
     IDENTIFIED(doom2) if the lumps contain MAP01, IDENTIFIED(doom) if
     E1M1, else INVALID (abort); for the Heretic, Hexen and Strife
     modules a non-matching basename yields UNIDENTIFIED(none) and no
     abort from this rule (what follows is outside this class)
     without -iwad: IDENTIFIED(M) for the first admitted registry row
     whose name exists in the search directories; else NOT-FOUND (abort)
D3   connect: VALID iff (mission, mode) is a row of valid_modes
     (U029-U043); else REFUSED (dropped)
     later client: ACCEPTED iff its pair equals the adopted pair; else
     REJECTED ("Game mismatch")
     episode/map: VALID iff a row has the pair and 1 <= episode <=
     row.episode and 1 <= map <= row.map, or (heretic, retail, 6, 1..3),
     or (heretic, registered, 4, 1); else INVALID (settings refused;
     Heretic -warp reset to 1/1; cheat ignored)
D4   VALID iff, after folding doom2 / pack_plut / pack_tnt / pack_hacx /
     pack_chex / pack_nerve / pack_master to doom, (mission, version)
     is a row of valid_versions (U044-U059) and the earlier settings
     checks pass; else REFUSED (dropped, no reply)
D5   -gameversion: ACCEPTED(V) iff the string equals a row's cmdline of
     the module's table (Doom U060-U070; Hexen U1029-U1030; Strife
     U1127-U1128); else ABORT
     Doom savegame: LOADABLE iff the header string equals "version C"
     where C is the running version's code (106, 107, 108, else 109);
     else REFUSED (version mismatch)
     Doom demo: PLAYABLE iff its first byte equals the running code, or
     equals the 1.91 longtics marker; else MISMATCH -- FATAL for a
     single demo, WARNING-AND-SKIP in the demo loop
D6   UNSUPPORTED (warning, no effect) iff the offset is in the running
     version's list (1.0: U071-U406; 1.2: U407-U711; 1.3: U712-U1016);
     else UNKNOWN (error, file aborts) iff the offset is not in the
     main table for the running version; else TOO-LONG (error) iff the
     replacement is longer than the executable allows and long strings
     are not allowed; else ACCEPTED (substitution stored)
D7   SET(V) iff the string is one of "1.0", "1.2", "1.3" (U1017-U1019);
     else IGNORED (message; default 1.0 remains)
D8   PENDING(w) iff owned[w] and w != ready and (WeaponInShareware[w]
     (U1020-U1028) or gamemode != shareware); else NO-CHANGE (silent)
D9   COMMAND(C) iff the token equals one of the fifteen names
     (U1031-U1045); else FATAL (script error)
D10  SERVED(M) for the first compiled-in module, in order, whose list
     (U1046-U1066) contains the value and whose Init succeeds; else
     NO-MODULE (silent; every later sound call a no-op)
D11  VALID iff none of the twenty-six options (U1067-U1092) is present;
     else FATAL
D12  KNOWN(T) iff the name equals a row's name, or begins with it when
     the row's name ends in `*`, and axes, buttons and hats equal the
     row's (U1093-U1122); else UNKNOWN (message; manual calibration)
D13  SELECTED(G) iff the string is one of doom, heretic, hexen, strife
     (U1123-U1126); else FATAL ("Invalid parameter")
D14  VALID iff, for each of the other three games' rows (U1129-U1132),
     the marker lump is absent; else FATAL (wrong executable)
```

totality: every case inside the domain receives a determinate verdict by the rules above -- each rule is a membership or equality test over a frozen table together with the stated conditions, and each ends in an `else` branch; the one known limit is D2 for the Heretic, Hexen and Strife modules, where a non-matching -iwad basename is decided only as UNIDENTIFIED(none), because the frozen evidence (Artifact 1, NC-02) stops there for those modules -- a case that turns on what those modules do next is out of domain, not indeterminate.

## Dependence on Artifact 2

The rules above read Artifact 1's native facts, not Artifact 2's
mapping; the only place the mapping enters is the naming of degrees of
refusal, which follows the native evidence. If KF-3 later shows an
Artifact 2 mapping to be wrong, the coupled finding rule of sealed §9
applies to whatever verdict that mapping underlies; by construction
that would be none of the rules above, which is recorded here so the
coupling question has an answer in advance.
