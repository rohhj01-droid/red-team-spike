# Disclosure log -- EXPLORATORY C084 study

EXPLORATORY. Design Section 5.1: an in-source comment that discloses a
failure cause ("this crashed when ...", "fix for ...") is an unavoidable
exposure in the sense of the sealed KF-1, and is logged at the moment it
is read. Rows are appended as they happen, from X4b on; the log exists
whether or not anything is ever found.

| utc | step | location (file:line) | what was disclosed | unit/case under analysis |
|---|---|---|---|---|
| 2026-10-29T06:30Z | X4b | NEWS.md:302, NEWS.md:1009, NEWS.md:1406, NEWS.md:1279, NEWS.md:1476 (quarantined file) | A scratch helper that greps usage sites of candidate symbols searched `.md` files too and printed five NEWS.md lines matching the words `strings` and `drivers`: a UTF-8 strings note; "printf format strings. Some potential buffer overflows are also" (a fixed-failure class named, no location or mechanism); "Allow changing more startup strings"; an OPL drivers test-feature note; a drivers thanks note. Cause leakage: a bug class ("buffer overflows") without mechanism. | X4b verdicts; no unit yet |
| 2026-10-29T07:07:36Z | X9 | src/hexen/h2_main.c:349-352 (and :354-362) | An in-source comment read while tracing NC-02: "The v1.0 IWAD file is missing a bunch of lumps that can cause the game to crash, so we exit with an error if the user tries to play with it" -- a known failure (crash with the Hexen v1.0 IWAD) and its cause (missing lumps), with the guard (-v10override, CLUS1MSG check). Cause leakage: yes, for that failure. | NC-02 (U012-U028) |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #90, first post | title, labels, state, created_at, body read; cause leakage: no -- design suggestion only | KF item #90 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #92, first post | title, labels, state, created_at, body read; cause leakage: yes -- names the current pause/unpause demo-sync mechanism and MBF's alternative | KF item #92 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #174, first post | title, labels, state, created_at, body read; cause leakage: yes -- reporter's hypothesis: `if (gametic & 3)` in A_Tracer; suggested fix | KF item #174 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #250, first post | title, labels, state, created_at, body read; cause leakage: yes (speculative) -- reporter's rendering explanation; R_DrawPlanes / R_DrawSprite named | KF item #250 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #258, first post | title, labels, state, created_at, body read; cause leakage: yes -- cause stated: emulated vanilla bug at a g_game.c line; fix commit linked | KF item #258 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #318, first post | title, labels, state, created_at, body read; cause leakage: yes -- the fix diff itself (x -> y in A_VileTarget) | KF item #318 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #362, first post | title, labels, state, created_at, body read; cause leakage: no -- wiki page name only | KF item #362 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #365, first post | title, labels, state, created_at, body read; cause leakage: yes -- cause and change stated with a p_enemy.c line reference | KF item #365 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #408, first post | title, labels, state, created_at, body read; cause leakage: yes (partial) -- console output before a segfault (REJECT pad message); gdb session start; body cut at 3000 chars | KF item #408 |
| 2026-10-29T08:35:50Z | X12 (KF-1) | issue #454, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms, version 5.6+, hardware | KF item #454 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #457, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms, command lines | KF item #457 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #458, first post | title, labels, state, created_at, body read; cause leakage: yes -- reporter's finding: 5.5.2's SDL DLLs restore sound | KF item #458 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #462, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #462 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #463, first post | title, labels, state, created_at, body read; cause leakage: no -- feature idea | KF item #463 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #475, first post | title, labels, state, created_at, body read; cause leakage: yes -- component named: midiproc volume couples to WAD music | KF item #475 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #498, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms, tool chain | KF item #498 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #524, first post | title, labels, state, created_at, body read; cause leakage: yes (hypothesis) -- memory corruption at the switch moment | KF item #524 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #527, first post | title, labels, state, created_at, body read; cause leakage: no -- title only | KF item #527 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #528, first post | title, labels, state, created_at, body read; cause leakage: no -- title only | KF item #528 |
| 2026-10-29T08:37:54Z | X12 (KF-1) | issue #556, first post | title, labels, state, created_at, body read; cause leakage: no -- suggestion | KF item #556 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #646, first post | title, labels, state, created_at, body read; cause leakage: yes -- program diagnostics naming the failing texture checks; malformed lumps described | KF item #646 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #655, first post | title, labels, state, created_at, body read; cause leakage: yes -- triggering condition identified: mixed-case file name in the autoload directory | KF item #655 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #657, first post | title, labels, state, created_at, body read; cause leakage: yes (by class) -- named a vanilla limit (30 crushers) | KF item #657 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #677, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #677 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #703, first post | title, labels, state, created_at, body read; cause leakage: yes (partial) -- mechanism observed: gravity not applied while not moving horizontally | KF item #703 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #706, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #706 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #716, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #716 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #718, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #718 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #727, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #727 |
| 2026-10-29T08:39:01Z | X12 (KF-1) | issue #730, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms | KF item #730 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #780, first post | title, labels, state, created_at, body read; cause leakage: yes -- code quoted (midiproc start in i_sdlmusic.c), cause as the reporter sees it, proposed check | KF item #780 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #807, first post | title, labels, state, created_at, body read; cause leakage: yes -- cause stated with two g_game.c line links (G_RecordDemo's G_InitNew before demorecording) | KF item #807 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #814, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms, setup | KF item #814 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #886, first post | title, labels, state, created_at, body read; cause leakage: yes (partial) -- 'backwards memcpy' abort, gdb libc frames; Crispy frame beyond the 3000-char cut | KF item #886 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #890, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms; screenshots not opened | KF item #890 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #893, first post | title, labels, state, created_at, body read; cause leakage: no -- symptoms, comparison builds | KF item #893 |
| 2026-10-29T08:40:06Z | X12 (KF-1) | issue #1043, first post | title, labels, state, created_at, body read; cause leakage: yes (partial) -- bisected commit 5fd8c76; content not described | KF item #1043 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #90: comments, timeline, linked commits | 11 of 11 comments read; timeline (closed 2020-03-26, no commit); no commit fetched | KF item #90 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #92: comments, timeline, linked commits | 3 of 3 comments read; timeline (cross-referenced by #174; closed, no commit); no commit fetched | KF item #92 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #174: comments, timeline, linked commits | 14 of 14 comments read (two cut at 1,200 chars); timeline (referenced commit; closed, no commit); commit bradharding/doomretro 77fa1a2 fetched (message, two files with patches) | KF item #174 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #250: comments, timeline, linked commits | 16 of 16 comments read (one cut); timeline (referenced commit; closed, no commit); commit Russian-Doom/russian-doom b5eb9ec fetched (message, one file with patch) | KF item #250 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #258: comments, timeline, linked commits | 8 of 8 comments read; timeline (closed, no commit); no commit fetched | KF item #258 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #318: comments, timeline, linked commits | 31 of 49 comments read (item cap 10,000 chars; one cut); timeline (closed/reopened twice, closed 2019-11-08 no commit; cross-referenced by fabiangreffrath/test-wads#2); no commit fetched | KF item #318 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #362: comments, timeline, linked commits | 5 of 5 comments read; timeline (closed, no commit); no commit fetched | KF item #362 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #365: comments, timeline, linked commits | 2 of 2 comments read; timeline (closed, no commit); no commit fetched | KF item #365 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #408: comments, timeline, linked commits | 19 of 19 comments read (one cut); timeline (referenced commit; closed by commit); commit fabiangreffrath/crispy-doom 5e9069b fetched (message, first file's patch cut at 700 chars) | KF item #408 |
| 2026-10-29T09:01:26Z | X14 (KF-3) | issue #454: comments, timeline, linked commits | 29 of 31 comments read (item cap; three cut); timeline (closed, cross-referenced by #458 and libsdl-org/SDL#3396, reopened, closed, referenced commit); commit fabiangreffrath/crispy-doom f105d6b fetched (message, one file with patch) | KF item #454 |
