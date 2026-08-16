# Phase 2 Commit D: Calibration Plan (declared before any results exist)

Sealed per CONTRACT.md: everything below is decided using dev (E1-E5)
evidence only, and is frozen once chosen -- never revisited after D.5.

## MCTS `c`: not swept, frozen at `sqrt(2)`

Not a default-by-convention choice -- a mathematical one. `mcts_search`
stops at the FIRST discovery (`while budget.remaining() and best is None`),
so at every point `_uct_select` is actually called, every candidate
child's `reward` is still 0 (the one non-zero backprop happens on the
winning iteration, after which no further selection occurs). With
`reward/visits == 0` for every candidate, UCT's score reduces to
`c * sqrt(log(N)/n)` -- and multiplying every candidate's score by the
same positive constant `c` never changes which one has the highest score.
**Any positive `c` produces an identical selection trace for a fixed
seed.** Sweeping `c` would not be calibration; it would be re-running the
same computation and calling the identical results "tuning." `c = sqrt(2)`
(CONTRACT.md's literature default) is used because there is nothing to
tune it against, not because it was validated as the best value.

No consequence for RQ3: the question is whether tree-structured
exploration + multi-step rollout lookahead beats 1-step Beam, not whether
a reward-gradient-tuned MCTS does -- and this MCTS structurally can't have
a reward gradient before its first success either way.

## No new MCTS knobs

Rollout policy, progressive widening, reward shaping, or any other change
to `search.py`'s MCTS beyond parameter values would be algorithm
development, not calibration -- out of scope for Commit D, which only
selects among parameters that already existed at the end of Commit C2.

## `BUDGET` / `MAX_DEPTH`: set by policy, not swept

Per CONTRACT.md: `MAX_DEPTH` comfortably exceeds the longest dev minimal
sequence (E5, 12 actions). Set to **36** (3x). `BUDGET` stays large enough
for Random to have a realistic shot at dev's hardest case; Phase 0's
reference point for a comparable delayed-reward case was ~40,000
evaluations, so keeping the same order of magnitude as Phase 0/1,
**`BUDGET = 100,000`**, same cap for every algorithm and for each Random/
MCTS seed individually (not split across seeds). These are declared now
and verified sufficient by the dev run below, not adjusted afterward to
fit whatever the dev run produces.

## Beam calibration: grid declared before running

**Stage 1 -- `beam_width`, decided on Beam-Naive alone** (no novelty
confound): grid = `{25, 50, 100}`. Selection rule: maximize dev Exploit
Recall (5/5 preferred) first; tie-break by minimizing the sum of costs
over the cases found. The winning `beam_width` is then used for **both**
Beam-Naive and Beam-Diverse -- picking it separately per algorithm would
confound RQ2's Naive-vs-Diverse comparison with a beam-width difference
instead of a diversity difference.

**Stage 2 -- `novelty_weight` x `novelty_k`, decided on Beam-Diverse**
with `beam_width` already fixed from Stage 1: grid = `{1, 2, 3, 5} x
{4, 8, 16}` (12 combinations). Same selection rule: maximize dev recall,
tie-break by minimizing summed cost over cases found, tie-break further
(if still tied) by the lowest `novelty_weight` value in grid order --
no reason to carry more diversity pressure than dev evidence justifies.

## What happens after this plan runs

The chosen values get written to `frozen_params.py` and this document's
"Results" section (appended, not edited into the plan above) records the
full grid output and the dev regression table (all 5 algorithms x all 5
dev cases) under the frozen settings. Nothing above this line changes
after that run, regardless of what it shows.

---

## Results (Commit D, executed via `run_calibration.py`)

### Stage 1 -- `beam_width` (Beam-Naive, dev E1-E5)

| beam_width | recall | summed cost |
|---|---|---|
| 25 | 5/5 | 734 |
| 50 | 5/5 | 1079 |
| 100 | 5/5 | 1327 |

All three achieve full dev recall, so the tie-break (minimum summed cost)
decides it: **`beam_width = 25`**.

### Stage 2 -- `novelty_weight` x `novelty_k` (Beam-Diverse, `beam_width=25`)

All 12 grid combinations also reach 5/5 dev recall (range: summed cost
736-753). **`novelty_weight = 1`, `novelty_k = 4`** wins on the same
tie-break.

### Honest reading of the calibration signal

Dev recall does not discriminate between ANY of the tested settings here
-- Beam-Naive alone already solves all 5 isolated dev cases at every
`beam_width` tried, and every novelty setting is redundant on top of
that. This is a direct, expected consequence of isolating each case
(CONTRACT.md): removing the multi-exploit reward confound also removed
most of what made Phase 0's shared environment hard for Beam-Naive in the
first place (E1 no longer crowds out anything, because there is nothing
else in E1's environment to crowd out). **The values above are the
cheapest settings that clear a bar every candidate cleared, not settings
validated as better at finding anything dev couldn't already find.** The
real test of whether `beam_width`/diversity matters is the held-out suite
(H1-H3), by design -- that is exactly why CONTRACT.md requires a held-out
suite instead of trusting dev-only evidence.

### Dev regression, frozen settings, all 5 algorithms x all 5 dev cases

| case | graph | random (10 seeds) | beam-naive | beam-diverse | mcts (10 seeds) |
|---|---|---|---|---|---|
| E1 | exploit_found | 10/10, med=12 | cost=7 | cost=7 | 10/10, med=12 |
| E2 | N/A | 10/10, med=29 | cost=67 | cost=67 | 10/10, med=29 |
| E3 | cycle_only | 10/10, med=31 | cost=37 | cost=37 | 10/10, med=31 |
| E4 | cycle_only | 10/10, med=186 | cost=50 | cost=52 | 10/10, med=193 |
| E5 | cycle_only | 10/10, med=384 | cost=573 | cost=573 | 10/10, med=517 |

Every search algorithm (Random, Beam-Naive, Beam-Diverse, MCTS) reaches
100% recall on every dev case under these frozen settings -- the dev
suite is now confirmed easy across the board for all four. A held-out
failure is less likely to be caused by already-exercised core search
plumbing (legal_actions/apply/budget accounting/oracle checks against
empty initial_inventory, all run thousands of times above without issue)
-- **though held-out-only engine features remain a possible implementation
confound.** In particular, `initial_inventory` (added for H1/H3) is never
exercised by any dev case above, since all five use the default `()` --
so nothing here has actually tested that code path yet. That gets tested
for the first time in D.5, not before.

Graph baseline: `exploit_found` on E1 (as in Commit C), `N/A` on E2
(multi-input, as designed), `cycle_only` (structural signal, not exploit
recall) on E3/E4/E5, unchanged from Commit C2's finding and expected --
Commit D did not touch the graph baseline.

Note for RQ1 interpretation later: Random beats both Beam variants and
MCTS on E5's median cost (384 vs 573/517) in this isolated environment,
the opposite of Phase 0's original (non-isolated) result. This is
consistent with isolation removing the shared-environment action/reward
competition that made blind search expensive in Phase 0 -- not a
controlled-experiment-verified causal claim (no A/B holding everything
else constant was run), just the most plausible explanation on hand.
Worth remembering when comparing across the two designs, worth stating
carefully if it comes up in a results writeup.

