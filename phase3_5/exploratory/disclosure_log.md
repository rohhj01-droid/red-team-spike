# Disclosure log -- EXPLORATORY C084 study

EXPLORATORY. Design Section 5.1: an in-source comment that discloses a
failure cause ("this crashed when ...", "fix for ...") is an unavoidable
exposure in the sense of the sealed KF-1, and is logged at the moment it
is read. Rows are appended as they happen, from X4b on; the log exists
whether or not anything is ever found.

| utc | step | location (file:line) | what was disclosed | unit/case under analysis |
|---|---|---|---|---|
| 2026-10-29T06:30Z | X4b | NEWS.md:302, NEWS.md:1009, NEWS.md:1406, NEWS.md:1279, NEWS.md:1476 (quarantined file) | A scratch helper that greps usage sites of candidate symbols searched `.md` files too and printed five NEWS.md lines matching the words `strings` and `drivers`: a UTF-8 strings note; "printf format strings. Some potential buffer overflows are also" (a fixed-failure class named, no location or mechanism); "Allow changing more startup strings"; an OPL drivers test-feature note; a drivers thanks note. Cause leakage: a bug class ("buffer overflows") without mechanism. | X4b verdicts; no unit yet |
