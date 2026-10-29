# Disclosure log -- EXPLORATORY C084 study

EXPLORATORY. Design Section 5.1: an in-source comment that discloses a
failure cause ("this crashed when ...", "fix for ...") is an unavoidable
exposure in the sense of the sealed KF-1, and is logged at the moment it
is read. Rows are appended as they happen, from X4b on; the log exists
whether or not anything is ever found.

| utc | step | location (file:line) | what was disclosed | unit/case under analysis |
|---|---|---|---|---|
