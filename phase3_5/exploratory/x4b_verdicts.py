# -*- coding: utf-8 -*-
"""X4b verdicts for the EXPLORATORY C084 study (design Sections 6.1, 6.2;
XQA-03, XQA-05). This script is the record of how every row of
inventory_sources.tsv and inventory_enumerators.tsv (generation 2,
commit 93e76f7) was decided: explicit per-row verdicts for the admitted
enumerators and the notable rejections, batch rules by identified scope
for the rest. Every reason names the identified scope (EN2) or the
missing or present refusal path (EN4), with file:line at revision
7775ef82. Re-running it reproduces the committed tables.

    python -I phase3_5/exploratory/x4b_verdicts.py
"""
from __future__ import annotations

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tools"))
from common import read_tsv, write_tsv  # noqa: E402
from inventory import EN_FIELDS, SRC_FIELDS  # noqa: E402

PASS6 = dict(en1="PASS", en2="PASS", en3="PASS", en4="PASS", en5="PASS", en6="PASS")

# ---------------------------------------------------------------- ADMIT
DEV = ("EN2: i_sound.c:141-142 'Is the sfx device in the list of devices supported by this module?' "
       "(and :168-169 for music). EN4: InitSfxModule i_sound.c:133-157 and the music loop :166-189: a configured "
       "snd_sfxdevice / snd_musicdevice found in no module's list leaves sound_module / music_module NULL, so the "
       "configured value is not acted on. EN5: static array whose length is passed as num_sound_devices -> enforced.")
GV = ("EN2: the -gameversion comment names 'Valid values' ({c}); the miss path prints 'Supported game versions:'. "
      "EN4: {m}: the argument is matched against cmdline; a miss prints the supported list and I_Error('Unknown game "
      "version'). EN5: NULL-terminated static array, loop on description != NULL -> enforced. The NULL row is a "
      "sentinel, not a member.")
ADMIT = {
    ("src/d_iwad.c", "iwads"): ("enforced",
        "EN2: IdentifyIWADByName d_iwad.c:617-644 names the set's role (identify an IWAD by name); README.md:74 "
        "'Crispy Doom can play nearly all variants of Doom'. EN4: d_iwad.c:631 mask and :636-639 name match -> "
        "mission; a miss yields none, and on the Doom branch src/doom/d_main.c:913-944 tries a lump heuristic then "
        "I_Error('Unknown or invalid IWAD file.'); d_iwad.c:946-955 -iwad not found -> I_Error. EN5: static const "
        "array bounded by arrlen :625 -> enforced. 17 active rows; the commented row strife0.wad is ABSENT."),
    ("src/d_mode.c", "valid_modes"): ("enforced",
        "EN2: d_mode.c:23-24 'Valid game mode/mission combinations'; :50 'Check that a gamemode+gamemission received "
        "over the network is valid'. EN4: D_ValidGameMode :52-65 and D_ValidEpisodeMap :67-100 return false on a "
        "miss; src/net_server.c:706-713 refuses the connect data; src/net_common.c:451-452 refuses the settings; "
        "src/heretic/d_main.c:1506-1510 resets an invalid -warp to 1/1. EN5: arrlen-bounded static array -> enforced."),
    ("src/d_mode.c", "valid_versions"): ("enforced",
        "EN2: d_mode.c:119 'Table of valid versions'. EN4: D_ValidGameVersion :156-165 returns false on a miss; "
        "src/net_common.c:448-449 refuses the settings. EN5: arrlen-bounded static array -> enforced."),
    ("src/doom/d_main.c", "gameversions"): ("enforced", GV.format(c="d_main.c:1160-1162", m="d_main.c:1169-1188")),
    ("src/hexen/h2_main.c", "gameversions"): ("enforced", GV.format(c="h2_main.c (the -gameversion block above :421)", m="h2_main.c:426-446")),
    ("src/strife/d_main.c", "gameversions"): ("enforced", GV.format(c="d_main.c:1153", m="d_main.c:1161-1181")),
    ("src/w_main.c", "unique_lumps"): ("enforced",
        "EN2: w_main.c:253-255 'Lump names that are unique to particular game types. This lets us check the user is "
        "not trying to play with the wrong executable'. EN4: W_CheckCorrectIWAD :267-292 -> I_Error when a lump "
        "unique to another mission is present. EN5: arrlen-bounded static array -> enforced."),
    ("src/heretic/deh_htic.c", "hhe_versions"): ("enforced",
        "EN2: deh_htic.c:75 'Valid versions:'. EN4: SetHHEVersionByName :61-81: a name matching no entry leaves "
        "deh_hhe_version unchanged and prints 'Unknown Heretic version' with the valid list. EN5: arrlen-bounded "
        "static array -> enforced."),
    ("src/hexen/p_setup.c", "MapCmdNames"): ("enforced",
        "EN2: consumed through SC_MustMatchString (p_setup.c:1094): the MAPINFO commands that must match. EN4: "
        "src/hexen/sc_man.c:411-421 SC_MustMatchString -> SC_ScriptError (fatal) on no match. EN5: NULL-terminated "
        "static array -> enforced. The NULL row is a sentinel, not a member."),
    ("src/heretic/p_user.c", "WeaponInShareware"): ("enforced",
        "EN2: the name states which weapons are in the shareware game (eligibility by weapon). EN4: p_user.c:671 "
        "'if (WeaponInShareware[newweapon] || gamemode != shareware)': in shareware a weapon whose entry is false "
        "cannot become pendingweapon. EN5: fixed-size boolean array indexed by weapon number -> enforced."),
    ("src/net_dedicated.c", "not_dedicated_options"): ("enforced",
        "EN2: net_dedicated.c:33-36 'Bomb out with an error message if game options are specified to a dedicated "
        "server'. EN4: CheckForClientOptions :47-62 -> I_Error if any listed parameter is present. EN5: "
        "NULL-terminated static array -> enforced. The NULL row is a sentinel, not a member."),
    ("src/setup/mode.c", "mission_configs"): ("enforced",
        "EN2: mode.c:346-347 'Valid values are doom, heretic, hexen and strife'. EN4: GetMissionForName :229-242 "
        "and SetupMission :356-361 -> I_Error('Invalid parameter') on a miss. EN5: arrlen-bounded static array -> "
        "enforced."),
    ("pkg/osx/IWADController.m", "IWADFilenames"): ("enforced",
        "EN2: IWADController.m:419-420 'Find an IWAD file that matches the filename in the path that we have been "
        "given'. EN4: :425-443: a file whose name matches no entry is not configured as an IWAD ('No IWAD found with "
        "this name', return NO). EN5: fixed-size array NUM_IWAD_TYPES+1 with a trailing nil -> enforced. The nil row "
        "is a sentinel, not a member."),
    ("src/setup/joystick.c", "known_joysticks"): ("enforced",
        "EN2: the name 'known_joysticks' (recognised controllers). EN4: GetJoystickType joystick.c:701-733: a "
        "joystick matching no entry gets 'Unknown joystick ...' and NULL, and IsKnownJoystick :737-740 is false: "
        "ineligible for the known configuration sets. EN5: arrlen-bounded static array -> enforced."),
    ("src/i_sdlsound.c", "sound_sdl_devices"): ("enforced", DEV),
    ("src/i_sdlmusic.c", "music_sdl_devices"): ("enforced", DEV),
    ("src/i_oplmusic.c", "music_opl_devices"): ("enforced", DEV),
    ("src/i_pcsound.c", "sound_pcsound_devices"): ("enforced", DEV),
    ("src/i_flmusic.c", "music_fl_devices"): ("enforced", DEV),
    ("src/i_winmusic.c", "music_win_devices"): ("enforced", DEV),
}
UNSUP = ("EN2: the name says 'unsupported'; deh_htext.c:794 'We don't support all strings, but at least recognise "
         "them'. EN4: StringIsUnsupported :673-689; DEH_TextStart :796-799 -> DEH_Warning('Unsupported string "
         "replacement') and the replacement is not applied (the else-if chain at :803 is skipped). EN5: "
         "-1-terminated static array, loop :680 -> enforced. The -1 row is a sentinel, not a member.")
for v in ("1_0", "1_2", "1_3"):
    ADMIT[("src/heretic/deh_htext.c", "unsupported_strings_" + v)] = ("enforced", UNSUP)

# ---------------------------------------------------------------- explicit rejections
EN4_REJECT = {
    ("src/doom/deh_doom.c", "deh_signatures"), ("src/heretic/deh_htic.c", "deh_signatures"),
    ("src/strife/deh_strife.c", "deh_signatures"),
}
EN4_REASON = ("EN4: deh_main.c:319-323 -- a file whose first line matches no signature only prints 'This is not a "
              "valid dehacked patch file!' ('[crispy] make non-fatal') and parsing continues at :327: the input is "
              "accepted regardless. (EN2 passed on that message's wording.)")
EN4_EVIDENCE = "EN2: deh_main.c:322 names the set as the valid signatures. EN4 FAIL: see reject_reason."

EXPLICIT_EN2 = {
    ("src/doom/deh_doom.c", "deh_section_types"): "identified as 'List of section types' (deh_doom.c:30-32): a dispatch list of section parsers",
    ("src/heretic/deh_htic.c", "deh_section_types"): "identified as a list of section parsers (deh_htic.c:49): dispatch",
    ("src/strife/deh_strife.c", "deh_section_types"): "identified as a list of section parsers (deh_strife.c:34): dispatch",
    ("src/doom/deh_misc.c", "misc_settings"): "dehacked Misc field names mapped to variables (deh_misc.c:133-137, fields deh_name/value): a mapping",
    ("src/strife/deh_misc.c", "misc_settings"): "dehacked Misc field names mapped to variables (deh_misc.c:133-137): a mapping",
    ("src/doom/deh_cheat.c", "allcheats"): "dehacked cheat names mapped to cheat sequences (deh_cheat.c:29-35): a mapping",
    ("src/strife/deh_cheat.c", "allcheats"): "dehacked cheat names mapped to cheat sequences (deh_cheat.c:35): a mapping",
    ("src/doom/deh_bexptr.c", "bex_codeptrtable"): "BEX code-pointer mnemonics mapped to action functions (deh_bexptr.c:118-123): a mapping",
    ("src/doom/deh_bexstr.c", "bex_stringtable"): "identified :33 'mnemonic keys table' mapping BEX mnemonics to strings: a mapping",
    ("src/doom/deh_thing.c", "bex_thingbitstable"): "BEX thing-flag mnemonics mapped to bit values (deh_thing.c:30-35): a mapping",
    ("src/heretic/deh_frame.c", "action_pointers"): "identified :38 'Offsets of action pointers within the Heretic executables': offset-to-function mapping",
    ("src/heretic/deh_htext.c", "strings"): "identified :44-45 'Offsets / String': executable offsets mapped to strings",
    ("src/heretic/deh_htext.c", "unsupported_strings"): "an index of the three per-version lists by deh_hhe_version (:666-671, :678): selection by version, not a set of values",
    ("src/net_structrw.c", "protocol_names"): "identified :27-28 'String names for the enum values in net_protocol_t': a mapping",
    ("src/hexen/sv_save.c", "ThinkerInfo"): "identified :2816-2820 'used by ArchiveThinkers and UnarchiveThinkers': serialization dispatch by thinker class",
    ("src/doom/d_pwad.c", "masterlevels_wads"): "identified :647 as a check whether the 20 Master Levels PWADs are available: discovery of known files, not acceptance of input",
    ("src/doom/d_pwad.c", "master_lumps"): "lump rename table (lump_rename_t name -> new_name): a mapping",
    ("src/hexen/d_pwad.c", "hexdd_lumps"): "lump rename table (lump_rename_t): a mapping",
    ("src/i_musicpack.c", "known_filenames"): "identified :143-145 'Table of known hashes and filenames to look up for them': substitution lookup",
    ("src/setup/multiplayer.c", "fallback_iwads"): "identified :52 'Fallback IWADs to use if no IWADs are detected': defaults",
    ("src/setup/multiplayer.c", "wad_extensions"): "file-selector extension filter (multiplayer.c:660): presentation",
    ("src/p_mapformat.c", "bsp_names"): "display names for the nodes-format enum, used only in a printf (p_mapformat.c:148): a mapping",
    ("src/i_sound.c", "sound_modules"): "identified :84 'Compiled-in sound modules': implementation dispatch",
    ("src/i_sound.c", "music_modules"): "identified :95 'Compiled-in music modules': implementation dispatch",
    ("src/w_file.c", "wad_file_classes"): "WAD file implementations tried in order (w_file.c:61-63): implementation dispatch",
    ("opl/opl.c", "drivers"): "OPL driver implementations tried in order (opl.c:109-142): implementation dispatch",
    ("pcsound/pcsound.c", "drivers"): "PC speaker driver implementations tried in order (pcsound.c:69-82): implementation dispatch",
    ("opl/ioperm_sys.c", "dll_functions"): "DLL function names to resolve at load (ioperm_sys.c:77-81): binding",
    ("src/d_iwad.c", "root_path_subdirs"): "IWAD search locations under a registry root path: where to look, not what is accepted",
    ("src/d_iwad.c", "steam_install_subdirs"): "IWAD search locations under a Steam install: where to look",
    ("src/d_iwad.c", "root_path_keys"): "registry keys searched for install paths: where to look",
    ("src/d_iwad.c", "uninstall_values"): "registry uninstall values searched for install paths: where to look",
    ("pkg/osx/IWADController.m", "IWADLabels"): "display labels for the launcher's IWAD dropdown: presentation",
    ("src/hexen/p_setup.c", "MapCmdIDs"): "ids parallel to MapCmdNames, selected by the matched index (p_setup.c:1094): a mapping",
    ("src/m_config.c", "doom_defaults_list"): "default configuration variables (default_t: name, variable, default): data binding, identified by name as defaults",
    ("src/m_config.c", "extra_defaults_list"): "default configuration variables of the extra config file (default_t): data binding",
    ("src/setup/mainmenu.c", "cheat_sequence"): "a key sequence for a setup-tool easter egg: input mapping",
    ("src/hexen/p_things.c", "TranslateThingType"): "map-thing numbers translated to mobj types: a mapping",
    ("src/hexen/sn_sonix.c", "SequenceTranslate"): "sound sequence names mapped to script numbers: a mapping",
    ("src/hexen/p_acs.c", "PCodeCmds"): "ACS p-code opcode dispatch table: implementation dispatch",
    ("src/doom/hu_stuff.c", "crispy_statslines"): "HUD stats-line drawer functions: presentation dispatch",
    ("src/doom/hu_stuff.c", "speciallevels"): "levels with special names (speciallevel_t): level-naming data",
    ("src/doom/hu_stuff.c", "kex_masterlevels"): "level numbers of the KEX Master Levels: level-naming data",
    ("src/doom/p_setup.c", "skilltable"): "skill names for a message: display strings",
    ("src/doom/f_finale.c", "castorder"): "cast-sequence data (castinfo_t): presentation",
    ("src/strife/f_finale.c", "castorder"): "cast-sequence data (castinfo_t): presentation",
    ("src/doom/f_finale.c", "actionsounds"): "cast-sequence sounds: presentation data",
    ("src/doom/f_finale.c", "textscreens"): "finale text screens (textscreen_t): presentation data",
    ("src/strife/f_finale.c", "textscreens"): "finale text screens (textscreen_t): presentation data",
    ("src/doom/p_extsaveg.c", "extsavegdata"): "extended savegame data items with write/read handlers (p_extsaveg.c:461-471): serialization dispatch; the handlers' behaviour was not examined at this mechanical step",
    ("src/heretic/p_extsaveg.c", "extsavegdata"): "extended savegame data items with write/read handlers: serialization dispatch",
    ("src/hexen/sv_extsaveg.c", "extsavegdata"): "extended savegame data items with write/read handlers: serialization dispatch",
    ("src/strife/p_extsaveg.c", "extsavegdata"): "extended savegame data items with write/read handlers: serialization dispatch",
    ("src/doom/p_maputl.c", "intercepts_overrun"): "vanilla intercepts-overrun emulation data: engine data",
    ("src/strife/p_maputl.c", "intercepts_overrun"): "vanilla intercepts-overrun emulation data: engine data",
    ("src/i_system.c", "mem_dump_dos622"): "memory dump bytes for DOS emulation: engine data",
    ("src/i_system.c", "mem_dump_win98"): "memory dump bytes for Windows 98 emulation: engine data",
    ("src/i_system.c", "mem_dump_dosbox"): "memory dump bytes for DOSBox emulation: engine data",
    ("src/i_joystick.c", "joystick_physical_buttons"): "physical joystick button variables: input binding",
    ("src/setup/joystick.c", "joystick_physical_buttons"): "physical joystick button variables: input binding",
    ("src/setup/joystick.c", "empty_defaults"): "default joystick bindings (joystick_config_t): configuration data",
    ("src/setup/joystick.c", "modern_gamepad"): "default gamepad bindings: configuration data",
    ("src/setup/joystick.c", "classic_gamepad"): "default gamepad bindings: configuration data",
    ("src/setup/joystick.c", "classic_gamepad_plus"): "default gamepad bindings: configuration data",
    ("src/setup/display.c", "window_sizes_unscaled"): "window size presets (window_size_t): UI data",
    ("src/setup/display.c", "window_sizes_scaled"): "window size presets (window_size_t): UI data",
    ("src/net_petname.c", "adjectives"): "random player-name words: presentation",
    ("src/net_petname.c", "nouns"): "random player-name words: presentation",
    ("textscreen/examples/guitest.c", "extensions"): "example-program data: presentation",
    ("textscreen/examples/guitest.c", "radio_values"): "example-program data: presentation",
    ("textscreen/txt_fileselect.c", "TXT_DIRECTORY"): "file-selector directory-only extension marker: UI data",
    ("textscreen/txt_gui.c", "borders"): "GUI border glyph indices: presentation",
    ("textscreen/txt_sdl.c", "ega_colors"): "EGA palette colours: presentation",
    ("src/setup/sound.c", "opltype_strings"): "OPL type display strings: presentation",
    ("src/setup/sound.c", "cfg_extension"): "file-selector extension filter: UI data",
    ("src/setup/sound.c", "sf_extension"): "file-selector extension filter: UI data",
    ("src/doom/d_main.c", "loadparms"): "names of the parameters scanned for files to load (d_main.c:1903-1906, :2060-2063): a list of parameters to process, not accepted values",
    ("src/heretic/d_main.c", "loadparms"): "names of the parameters scanned for files to load (d_main.c:1216-1219): a list of parameters to process",
    ("src/hexen/h2_main.c", "loadparms"): "names of the parameters scanned for files to load (h2_main.c:858-861): a list of parameters to process",
    ("src/strife/d_main.c", "loadparms"): "names of the parameters scanned for files to load (d_main.c:1926-1929): a list of parameters to process",
    ("src/setup/mode.c", "mission_configs"): None,   # admitted; guard against accidental rule
}

# ---------------------------------------------------------------- batch rules (first match wins)
def rules(r):
    f, s, t = r["file"], r["symbol"], r["element_type"]
    base = f.rsplit("/", 1)[-1]
    if r["class"] == "K4":
        return None
    if t == "mline_t":
        return "automap vector shapes (mline_t): drawing data"
    if t in ("menuitem_t", "MenuItem_t", "menu_t *", "Menu_t *", "MenuType_t", "multiitem_t", "static void (*)()") or s == "dialogmenuitems":
        return "menu definitions and option labels (%s): presentation" % (t or "menu")
    if base == "r_bmaps.c" or t == "fullbright_t":
        return "brightmap colour tables (rendering)"
    if base == "v_trans.c" or s == "cr":
        return "colour translation tables (rendering)"
    if base in ("tables.c",) or s in ("finesine", "finetangent", "tantoangle", "gammatable", "gammalevels"):
        return "trigonometric / gamma lookup tables: numeric constants"
    if t in ("fixed_t", "angle_t") or s in ("forwardmove", "sidemove", "angleturn", "MaxPlayerMove", "xspeed", "yspeed", "FloatBobOffsets", "crispy_bobfactor"):
        return "movement and physics constants (%s): numeric game data" % s
    if base in ("opl3.c", "wf_rom.h", "aes_prng.c", "mus2mid.c", "midifallback.c", "i_pcsound.c", "i_oplmusic.c", "i_winmusic.c", "i_input.c") and s not in ("music_opl_devices", "sound_pcsound_devices", "music_win_devices"):
        return "emulator / MIDI / cipher / key-mapping constant tables (%s): engine data" % s
    if base == "m_config.c":
        return "configuration key mapping (%s): data binding" % s
    if s in ("rndtable",):
        return "pseudo-random number table: engine data"
    if s.endswith("_icon_data") or s.endswith("_font_data") or s == "crispness_background":
        return "image / font bitmap data: presentation"
    if base in ("sounds.c",) or t in ("musicinfo_t", "sfxinfo_t", "sfxenum_t", "altmusic_t", "subst_music_t"):
        return "sound and music resource tables (%s): engine resource data" % s
    if base == "info.c" or t in ("state_t", "mobjinfo_t"):
        return "actor state / thing definition tables (%s): engine data" % s
    if s == "sprnames":
        return "sprite name list: resource names"
    if t in ("weaponinfo_t",) or s in ("weapon_order_table", "WeaponValue", "GetWeaponAmmo", "GetAmmoChange", "GetAmmoChangePL1", "GetAmmoChangePL2", "WeaponAmmoUsePL1", "WeaponAmmoUsePL2", "WeaponManaUse", "maxammo", "clipammo", "ArmorIncrement", "AutoArmorSave", "ArmorMax", "recoil_values", "MonsterMissileInfo", "PStateNormal", "PStateRun", "PStateAttack", "PStateAttackEnd", "weapon_keys", "healthamounts"):
        return "weapon / ammo / armour / player-state game data (%s)" % s
    if s in ("pars", "cpars", "npars", "chexpars", "bex_pars", "bex_cpars", "doom1_par_times", "doom2_par_times"):
        return "par-time tables: game data"
    if t in ("animdef_t", "switchlist_t", "slidename_t", "terraintype_t", "lump_rename_t", "speciallevel_t") or s in ("TerrainTypeDefs", "AmbientSfx", "slideOpenSounds", "slideCloseSounds") or s.startswith("AmbSndSeq"):
        return "texture animation / switch / door / terrain / ambient-sound definition tables (%s): engine data" % s
    if base in ("wi_stuff.c", "in_lude.c") or t in ("anim_t", "anim_t *", "point_t", "patch_t *", "yahpt_t"):
        return "intermission screen data (%s): presentation" % s
    if t in ("Cheat_t", "cheatseq_t") or s in ("cheats", "Cheats", "cheat_kills"):
        return "cheat code sequences mapped to effects: input mapping"
    if t in ("dialogstateset_t", "rndmessage_t") or base == "p_dialog.c":
        return "Strife dialog data (%s): game data" % s
    if t in ("scale_values", ) or s in ("scale_values", "checkcoord", "fuzzoffset", "PhaseTable", "orbitTableX", "orbitTableY", "notchTable", "netnotchTable", "PieceX", "st_yforammo", "st_wforammo", "laserpatch_m", "crosshairpatch_m", "spriteoffsets", "PSpriteSY", "antialias_normal", "antialias_overlay", "aliasmax", "lnodes", "NUMANIMS", "anims", "yah", "splat", "quitsounds", "quitsounds2") or t in ("drawpatchpx_t *", "laserpatch_t", "crosshairpatch_t", "spriteoffset_t"):
        return "renderer / HUD / status-bar layout constants (%s): presentation" % s
    if base in ("keyboard.c", "mouse.c", "txt_joybinput.c") or t == "int *":
        return "configuration variable pointers / button name lists for the setup UI (%s): UI binding" % s
    if t == "joystick_config_t":
        return "per-controller default bindings (%s): configuration data" % s
    if t in ("snddevice_t",):
        return None   # admitted explicitly
    if t == "NSString *":
        return None
    if t == "char *" or t == "char" or t == "const char *":
        return "display strings / names (%s): presentation" % s
    if t in ("byte", "unsigned char", "uint8_t", "uint16_t", "uint32_t", "unsigned int", "unsigned short", "int", "int8_t", "float", "boolean", "SDL_Color", "byte *", "dirtype_t", "weapontype_t", "mobjtype_t", "sfxenum_t"):
        return "numeric / enum constant table (%s): engine data" % s
    return None


K4_REASONS = {
    "D001": "no closed set of enforcement items is declared; the sentence concerns the licensing of contributions",
    "D002": "no closed set declared; CMake package metadata",
    "D003": "no closed set declared; code of conduct",
    "D004": "no closed set declared; GPL licence text",
    "D005": "no closed set declared; GPL licence text",
    "D006": "no closed set of enforcement items declared; a table of C-library wrapper functions and a licensing rule for contributions",
    "D007": "no closed set declared; copyright statement",
    "D008": "no closed set declared; uninstall instructions",
    "D009": "no closed set declared; build instructions",
    "D010": "no closed set declared; advice on sharing savegames with Chocolate Doom (a requirement in prose, not an enumerable set)",
    "D011": "no closed set declared; description of a Crispness option",
    "D012": "no closed set declared; description of a sound option",
    "D013": "no closed set declared; description of a command-line parameter",
    "D014": "no closed set declared; description of a command-line parameter",
    "D015": "no closed set declared; description of a command-line parameter",
}

# ---------------------------------------------------------------- sources
NO_DESIG = ("no designation: no project statement names this file as stating the program's rules, requirements, "
            "valid configurations or accepted inputs -- README.md:91-98 (Documentation) points at wiki pages, "
            "README.md:55 points at the wiki for compatibility, man/CMDLINE.template.md:1-4 designates the generated "
            "manual as 'a full list of the supported command line parameters' (that file is not in the tree), "
            "PHILOSOPHY.md:6 is 'descriptive, not proscriptive'")
SRC_EXTRA = {
    "README.md": "; states a requirement itself (:74 an IWAD is needed) but designates no file and is prose (no segmentation)",
    "man/iwad_paths.man": "; states 'To play, an IWAD file is needed' and lists the standard IWAD names as .IR items, but no statement designates it",
    "man/CMDLINE.template.md": "; designates the generated manual, and itself carries no items (@content placeholder)",
    "docs/compatibility.md": "; README.md:55 and :97 designate the wiki page of this name, not this file",
    "docs/params.md": "; README.md:94 designates the wiki page of this name, not this file",
    "docs/cheats.md": "; README.md:93 designates the wiki page of this name, not this file",
    "docs/controls.md": "; README.md:95 designates the wiki page of this name, not this file",
    "docs/crispness.md": "; README.md:96 designates the wiki page of this name, not this file",
    "docs/faq.md": "; README.md:98 designates the wiki page of this name, not this file",
    "PHILOSOPHY.md": "; declares itself 'descriptive, not proscriptive' (:6)",
    "HACKING.md": "; coding style guidelines for contributors, not program rules",
    "CODE_OF_CONDUCT.md": "; conduct rules for contributors, not program rules",
    ".github/CONTRIBUTING.md": "; contribution guidelines",
    ".github/ISSUE_TEMPLATE.md": "; issue template",
    "COPYING.md": "; licence text",
    "AUTHORS": "; author list",
    "README.Music.md": "; music playback documentation, designated by nothing",
    "README.Strife.md": "; Chocolate Strife notes, designated by nothing",
    "man/environ.man": "; environment variable documentation, designated by nothing",
    "man/docgen": "; a script",
    "man/simplecpp": "; a script",
    "man/wikipages": "; a script",
    "pkg/style.html": "; a stylesheet",
}


def main() -> int:
    en = read_tsv(os.path.join(HERE, "inventory_enumerators.tsv"))
    src = read_tsv(os.path.join(HERE, "inventory_sources.tsv"))
    undecided = []
    for r in en:
        key = (r["file"], r["symbol"])
        for c in ("en1", "en2", "en3", "en4", "en5", "en6", "tag", "reject_reason"):
            r[c] = ""
        if r["class"] != "K4":
            r["evidence"] = ""
        if key in ADMIT:
            tag, ev = ADMIT[key]
            r.update(PASS6, tag=tag, evidence=ev)
            continue
        if key in EN4_REJECT:
            r.update(en1="PASS", en2="PASS", en3="PASS", en4="FAIL", reject_reason=EN4_REASON, evidence=EN4_EVIDENCE)
            continue
        if r["class"] == "K4":
            r.update(en1="PASS", en2="FAIL", reject_reason="EN2: " + K4_REASONS[r["cand_id"]])
            continue
        reason = EXPLICIT_EN2.get(key) or rules(r)
        if reason is None:
            undecided.append("%s %s:%s %s [%s]" % (r["cand_id"], r["file"], r["line"], r["symbol"], r["element_type"]))
            continue
        r.update(en1="PASS", en2="FAIL", reject_reason="EN2: " + reason)
    if undecided:
        print("UNDECIDED rows:")
        for u in undecided:
            print("  " + u)
        return 1
    for r in src:
        if r["decision"] == "QUARANTINED":
            continue
        base = r["path"].rsplit("/", 1)[-1]
        if base == "CMakeLists.txt":
            r.update(decision="REJECT", reason="no designation; a build file")
        else:
            r.update(decision="REJECT", reason=NO_DESIG + SRC_EXTRA.get(r["path"], ""))
    write_tsv(os.path.join(HERE, "inventory_enumerators.tsv"), en, EN_FIELDS)
    write_tsv(os.path.join(HERE, "inventory_sources.tsv"), src, SRC_FIELDS)
    adm = [r for r in en if r["tag"]]
    print("admitted enumerators: %d (%s members incl. sentinels)" % (len(adm), sum(int(r["members"]) for r in adm)))
    for r in adm:
        print("  %s %s:%s %s n=%s" % (r["cand_id"], r["file"], r["line"], r["symbol"], r["members"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
