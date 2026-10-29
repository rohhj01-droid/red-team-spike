# Phase 3.5 Exploratory Study (C084) -- Execution QA log

EXPLORATORY. This log belongs to the exploratory C084 study
(`docs/superpowers/specs/2026-10-29-phase3-5-exploratory-c084-design.md`,
sealed `984f0c5`). It is numbered XQA-01, XQA-02, ... so that the
screening run's QA-01..QA-43 stay closed. Entries are written at the
time, in order found; nothing is deleted; a withdrawn sentence stays in
place, marked.

Entry template:
## XQA-NN -- <title> (<YYYY-MM-DD>)
**Step:** X..   **Clause(s):** <design section / sealed section>
**What happened or was decided:**
**Effect on the record:**

## XQA-01 -- sealed-instant consistency check returned DIFFERS (2026-10-29)
**Step:** X4a   **Clause(s):** design 4.2 step 5; design 2.1 (second substitution); QA-28
**What happened or was decided:** `GET /repos/fabiangreffrath/crispy-doom/commits?sha=master&until=2026-08-26T19:23:05Z&per_page=1`, queried 2026-10-29T06:00:05Z with commit messages discarded, returned `3a39d0a53aaa52562f099a7c4fab649d8962d947` (author and committer date 2026-08-24T16:33:06Z), not the revision `7775ef82d1e9dfd50eb9d2824acefaeff7247458` (committed 2026-08-03T14:08:24Z). Per 4.2 step 5 the study proceeds on the revision: it is the object the screening record describes, and the ten pinned digests match the tree on disk (pin_record.md Section 3). The observation does not identify master's tip at the sealed instant -- a commit with an earlier committer date can enter master's history after that instant, and a later observation cannot tell the cases apart (QA-28). Ancestry between the two commits was not queried (5.1 admits the API for three purposes only).
**Effect on the record:** the revision is unchanged and the second substitution of 2.1 stands as declared. Run 2 input: an API query for "master at instant T" is not a snapshot procedure -- here it returned a commit other than the one the screening observed at master's tip four days after T (EV-C084-PIN-01). Any Run 2 snapshot rule must pin at observation time and say so, or not claim the sealed instant at all.
