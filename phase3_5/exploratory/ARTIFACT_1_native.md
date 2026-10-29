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
