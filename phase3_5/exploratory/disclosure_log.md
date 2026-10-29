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
