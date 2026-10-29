# Phase 3.5 Run 2 -- Execution QA log

This log belongs to Run 2 (preregistration design
`docs/superpowers/specs/2026-10-29-phase3-5-run2-preregistration-design.md`,
sealed `4c7e315`; contract `SCREENING_CONTRACT.md`). It is numbered
RQA-01, RQA-02, ... so that Run 1's QA-01..QA-43 and the exploratory
study's XQA-01..XQA-15 stay closed. Entries are written at the time, in
order found; nothing is deleted; a withdrawn sentence stays in place,
marked. Decision points D1-D5 are recorded here in the owner's words.

Entry template:
## RQA-NN -- <title> (<YYYY-MM-DD>)
**Step:** R..   **Clause(s):** <design section / contract section / sealed section>
**What happened or was decided:**
**Effect on the record:**

## RQA-01 -- the witness table carries a `tag` column; observation rows are per request (2026-10-29)
**Step:** R2 (Task 8, before any candidate is seen)   **Clause(s):** contract 9.4, 9.5, 8 (E4); design Section 6
**What happened or was decided:** Building `screen.py` showed two things the contract's schemas did not say. (a) An E4 `enumerator` witness must carry the enforced / asserted tag the frozen grammar needs for the admitted row (design Section 6, sealed 3.3); the contract's seven witness columns had no place for it. The witness table gains an eighth column, `tag`, used only on `enumerator` rows (`enforced` | `asserted`); every other row leaves it empty. (b) `observations.tsv` records one row per request actually made, so a redirect chain yields one row per hop with that hop's URL as `requested_url`, and a retried transport failure one row per attempt; the per-row `outcome` is `ok | definitive | transport` as 9.4 states (a 4xx answer is `definitive`). Neither changes what is read or decided.
**Effect on the record:** `tools/ledger.py` WITNESS_FIELDS and OBS_FIELDS carry these; the contract's 9.4 and 9.5 are read with this entry beside them. Recorded before the frame is re-fetched.
