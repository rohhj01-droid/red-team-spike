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
