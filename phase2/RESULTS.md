# Phase 2 Commit E: Held-out Evaluation (terminal, run once)

Executed via `run_evaluation.py`, reading every parameter from
`frozen_params.py` (no number re-declared here or in the script). This is
the first and only run of any search algorithm against H1/H2/H3. **These
results are not re-tuned regardless of outcome** -- that was the entire
point of freezing everything before this commit existed.

```
BUDGET=100,000  MAX_DEPTH=36  BEAM_WIDTH=25
NOVELTY_WEIGHT=1  NOVELTY_K=4  MCTS_C=sqrt(2)  SEEDS=10
```

One representative successful witness per stochastic algorithm/case
(Random, MCTS -- the first seed that found it), plus every deterministic
witness (Beam-Naive, Beam-Diverse, Graph), was independently replayed
through `oracle.is_exploit_found` before any result below was recorded --
this is an integrity check on the run, not a tuning step; the script
would have raised `AssertionError` on the first mismatch, and didn't.
(Not all 10 seeds' individual witnesses per stochastic algorithm were
separately re-validated -- `Discovery` is only ever constructed when the
search itself already confirmed profitability via the same
`is_profitable_state` predicate the oracle uses, so this is a narrower
claim than "every witness of every seed," not a gap in what actually
happened.)

## RQ1 -- structure-dependent method choice (descriptive, no verdict)

| case | graph | random (10 seeds) | beam-naive | beam-diverse | mcts (10 seeds) |
|---|---|---|---|---|---|
| E1 | exploit_found | 10/10, med=12.0, IQR=8.0 | cost=7 | cost=7 | 10/10, med=12.0, IQR=8.0 |
| E2 | N/A | 10/10, med=29.5, IQR=34.75 | cost=67 | cost=67 | 10/10, med=29.5, IQR=34.75 |
| E3 | cycle_only | 10/10, med=31.0, IQR=26.25 | cost=37 | cost=37 | 10/10, med=31.0, IQR=26.25 |
| E4 | cycle_only | 10/10, med=186.5, IQR=382.25 | cost=50 | cost=52 | 10/10, med=193.0, IQR=109.75 |
| E5 | cycle_only | 10/10, med=384.5, IQR=472.25 | cost=573 | cost=573 | 10/10, med=517.5, IQR=2814.75 |
| **H1** | N/A | 10/10, med=4.5, IQR=3.75 | cost=5 | cost=9 | 10/10, med=4.5, IQR=3.75 |
| **H2** | N/A | 10/10, med=42.0, IQR=53.0 | cost=180 | cost=180 | 10/10, med=42.5, IQR=53.0 |
| **H3** | N/A | 10/10, med=24.5, IQR=62.5 | cost=6 | cost=6 | 10/10, med=23.0, IQR=36.5 |

(IQR values above were computed and printed during the single evaluation
run and are transcribed from that run's captured output, not recomputed
by a second run -- the run is not repeated to backfill anything.)

Graph baseline is `N/A` on all three held-out cases -- H1/H3 have finite
`initial_inventory` (excluded by design), H2 is multi-input (excluded by
design). This is the predicted boundary from CONTRACT.md, not a surprise:
"where exactly does static cycle detection stop being sufficient" was
part of RQ1's question, and the answer for this suite is "everywhere
scarcity or multi-input combination is the mechanism." Separately, within
the cases it does support: it produced an oracle-valid **executable**
witness (`exploit_found`) on only E1. E3-E5 register as `cycle_only` --
Bellman-Ford correctly detects a mathematically profitable rate cycle in
all three, but the naive one-edge-per-step reconstruction isn't a legal
action sequence there (see `graph_baseline.py`'s docstring: a pure
item-duplication cycle that never touches gold, or a craft step needing
more than one prior purchase). **Detecting profitable structure and
producing an executable exploit are two different capabilities with two
different success rates here (4/4 supported cases vs. 1/4).**

## RQ2 -- diversity (held-out H1-H3 only)

**VERDICT: NO EVIDENCE**

| case | naive | diverse | win? |
|---|---|---|---|
| H1 | found, cost=5 | found, cost=9 | No (diverse is *slower*, not <=75%) |
| H2 | found, cost=180 | found, cost=180 | No (tied, not <=75%) |
| H3 | found, cost=6 | found, cost=6 | No (tied) |

0/3 wins, no recall regression either. Beam-Diverse never loses to
Beam-Naive here, but never meaningfully beats it -- on H1 it is
measurably worse (cost 9 vs 5). This is consistent with what
`CALIBRATION.md` already flagged as a risk: every dev/held-out case here
is small enough (few distractor items, isolated single-mechanism
environments) that Beam-Naive's mode-collapse failure mode from Phase 0
never gets triggered -- there's no dominant easy strategy in these
environments crowding out width the way Trinket did in Phase 0's shared
economy, so there's nothing for diversity preservation to rescue here.
**This does not contradict Phase 0's Round 2 finding** (diversity helped
E4 there): the result is consistent with the hypothesis that Phase 0's
diversity benefit depended on crowding/mode collapse, but Phase 2 did not
run a controlled comparison isolating that variable, so it does not
independently establish crowding as the causal explanation -- only that
no benefit was observed in an environment design that happens to lack it.

## RQ3 -- lookahead (H2 only, sole verdict-driving case)

**VERDICT: STRONG**

```
MCTS success rate on H2:  10/10 (>= 8/10 threshold)
MCTS median cost:         42.5
Beam-Diverse on H2:       found, cost=180
Threshold: 42.5 <= 0.5 * 180 = 90  ->  TRUE
```

Both conditions for STRONG hold. Beam-Diverse is deterministic (one run,
no success-rate concept), so "reliability" isn't a comparable axis
between them -- the precise statement is: **MCTS met the predeclared
10-seed reliability bar (10/10) and was ~4.2x cheaper than deterministic
Beam-Diverse on H2** (42.5 vs 180 transition evaluations).

**Why, in one paragraph (a plausible account consistent with the design,
not something separately proven beyond what's shown above):** H2 was
built so that accumulating Alpha/Beta strictly lowers Beam's `score()`
below baseline -- meaning Beam's greedy top-K selection actively
*deprioritizes* the exact states that lead to the payoff, since they look
worse than doing nothing. Beam only reaches H2 once better-looking
branches are exhausted within budget, which is slow. MCTS's rollout +
backpropagation structure doesn't rank candidates by an immediate score
at all; a rollout either stumbles into profit or it doesn't, so the
valley that actively repels Beam is invisible to MCTS's selection
mechanism -- it isn't being avoided in the first place.

**What this does NOT establish:** "MCTS beats Beam-Diverse" as a general
claim. The precise, honest claim is: *on a predeclared held-out instance
specifically constructed to require crossing a negative Beam-score
valley, tree exploration + multi-step rollout lookahead substantially
outperformed 1-step greedy heuristic search.* Per `search.py`'s
documented caveat, this MCTS's reward is binary and first-hit, so the
result reflects exploration structure, not a learned reward gradient.

## Bottom line

Phase 2 answers its three questions with a genuinely mixed, not
uniformly positive, result -- which is the more credible outcome, not a
disappointing one:

- **RQ1**: static graph cycle detection *detects profitable structure* in
  several single-input, infinite-supply cases, but only produced an
  oracle-valid **executable** exploit on E1 -- E3-E5 remained structural
  signals (`cycle_only`), and it is entirely unsupported on the held-out
  scarcity/multi-input cases. Detection and executable-witness generation
  are two separate capabilities with two different success rates here
  (4/4 vs. 1/4) -- search is "necessary" both past the detection boundary
  and, within it, for turning a detected cycle into something runnable.
- **RQ2**: no evidence diversity preservation helps in this suite. None
  of these smaller, isolated environments reproduce the crowding/
  mode-collapse dynamic diversity addressed in Phase 0 -- plausibly why,
  though Phase 2 didn't isolate that variable to prove it. Not a
  refutation of Phase 0 Round 2 -- a scope-narrowing of when a benefit
  was observed.
- **RQ3**: strong evidence that lookahead search earns its cost
  specifically on the class of problem it was built to address (a
  negative-score valley a greedy heuristic actively avoids).

No further tuning follows this. Phase 2 is closed.
