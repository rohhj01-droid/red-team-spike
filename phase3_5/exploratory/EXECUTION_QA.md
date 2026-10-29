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

## XQA-02 -- candidate class K1 widened to any element type (2026-10-29)
**Step:** X4b   **Clause(s):** design 6.2 (K1); design 13 (L2)
**What happened or was decided:** The design's K1 reads "file-scope array initializers of aggregate type (... with a struct or array element type ...)". The committed tool (`inventory.py`, commit `b88868c`) generates K1 candidates from ANY file-scope array initializer, scalar and pointer element types included, so that a string-list registry (`const char *names[] = { ... }`) is a candidate. The widening was proposed in the implementation plan (`docs/superpowers/plans/2026-10-29-phase3-5-exploratory-c084.md`, Task 3) and approved by the owner with the plan (`573c19c`), before the tool touched the target tree. Direction: wider, never narrower -- a candidate the design would also have produced is still produced; the extra candidates are decided by EN1..EN6 like every other row.
**Effect on the record:** `inventory_enumerators.tsv` may contain K1 rows the design's parenthetical would have excluded; each carries its own verdict. L2's statement that the candidate classes are the analyst's stands, with this widening added to it.

## XQA-03 -- reading of EN2 against EN4 fixed before any candidate is decided (2026-10-29)
**Step:** X4b   **Clause(s):** sealed 3.2 EN2, EN4; design 3 (non-goals: an ambiguous rule gets its reading recorded here); design 6.2
**What happened or was decided:** The sealed EN2 reads "The external project identifies what enforcement domain the mechanism enumerates, e.g. quest eligibility conditions, effect requirements, transfer guards", and EN4 "The external project itself connects the mechanism to validation, eligibility, rule enforcement, or an equivalent validity role". With 596 candidates to decide, the first FAIL is also a statistic (design 12 item 4), so the line between the two is fixed now: EN2 asks WHAT the set is a set of, in the project's own naming, comment or document, and passes only if that scope is a domain of acceptance, refusal, eligibility, validity, compatibility or support -- a set the project identifies as menu items, graphics, sounds, text, timing or data layout fails EN2 with that scope named; EN4 asks whether the project OPERATIONALLY connects a set that passed EN2 to enforcement -- a code path in which the set decides acceptance, refusal or eligibility, or project text saying so, quoted and located (design 6.2, narrow reading). Under this reading a table of accepted command-line values whose miss raises an error passes both; a table of recognised configuration names whose miss is silently skipped passes EN2 and fails EN4.
**Effect on the record:** every REJECT at EN2 names the identified scope; every REJECT at EN4 names the missing connection. The alternative reading (EN2 = any named scope, all validity questions at EN4) would move most EN2 rejections to EN4 and change nothing else; it is recorded as the reading not taken.
