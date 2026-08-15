# Phase 2 Contract

Status: **draft, not yet executed.** No benchmark data, no algorithm code
exists for Phase 2 yet. This document is Commit A in the sequence below --
it is meant to be reviewed and locked *before* any of that is written.

## Research questions

Phase 0 asked one yes/no question (can search find planted exploits at
all). Phase 2 asks three comparative questions, and stops there --
cross-system questions (Quest x Equipment x Buff) belong to Phase 3, not
here.

- **RQ1**: Across economy/crafting exploits with different structures,
  which search method is most efficient, and does the best method change
  with the exploit's structure?
- **RQ2**: Does diversity-preserving search (Beam-Diverse) find a broader,
  more reliable set of exploits than single-objective search (Beam-Naive),
  beyond what Phase 0 already showed on E4?
- **RQ3**: Does lookahead search (MCTS) show a real advantage over 1-step
  heuristic search on delayed-reward / long-horizon exploits, the question
  E5 raised but Phase 0 deliberately left unanswered?

## Benchmark policy

### E1-E5 are permanently development/calibration data, never held-out again

We know their mechanisms, we know which method fails where, and we already
formed the hypothesis that motivates RQ3 from watching E5 specifically.
Reusing any of E1-E5 as a "held-out" case in Phase 2 would be testing
memorization, not generalization. They stay in the suite as regression
cases (e.g. "MCTS vs Beam-Naive vs Beam-Diverse on E5" is a legitimate
development-set comparison) but never appear in a held-out verdict.

### New held-out suite: structurally different, not just re-skinned

A held-out case that is just E1 with different item names (buy 15 / sell
30 instead of buy 10 / sell 20) tests nothing new. The held-out suite must
contain mechanism *types* absent from E1-E5. Three are committed here,
each targeting a different weakness E1-E5 couldn't expose:

- **H1 -- Resource bottleneck.** A profitable action is only available a
  limited number of times (capped stock, or a one-time source), forcing
  the algorithm to plan around scarcity instead of repeating one action
  indefinitely. E1-E5 are all infinitely repeatable cycles; nothing in
  Phase 0 tested finite-resource planning at all.
- **H2 -- Genuinely lossy intermediate step.** A step that reduces the
  *estimated* value (not just raw gold) at the point it's taken, and only
  pays off through a later, separate combination. E5 was long, but its
  intermediate Herb-accumulation steps still looked non-negative under the
  value heuristic (Herb had derived value). H2 must not have that
  cushion -- this is the most direct test of RQ3 / whether lookahead earns
  its cost.
- **H3 -- Branching recipe choice.** A shared input item is consumable by
  two or more recipes, only one of which leads anywhere profitable, and
  choosing wrong burns the resource with no easy recovery. E1-E5 had no
  forks -- every recipe had exactly one use for its inputs.

No exact item names, prices, or minimal action counts are fixed by this
document -- that's Commit B, written and sealed *before* Commit C (the
Graph/MCTS implementations), specifically so the held-out benchmark cannot
be shaped, even unconsciously, around a known algorithm's blind spots.

## Algorithms

| Algorithm | What it is | Primarily informs |
|---|---|---|
| Random | Unchanged from Phase 0/1. | Baseline for all three RQs. |
| **Graph/Cycle baseline** (new) | Deterministic: model item conversions as a weighted graph, detect positive-value cycles (Bellman-Ford-style). No learning, no search budget in the same sense. | RQ1 -- is search even necessary for the simple cases? |
| Beam-Naive | Unchanged from Phase 1. | RQ1, RQ2 (as the thing Beam-Diverse must beat). |
| Beam-Diverse | Unchanged from Phase 1, but its hyperparameters get re-calibrated under the new rules below -- not reused as-is from Phase 0. | RQ2. |
| **MCTS** (new) | Standard UCT: selection/expansion/simulation/backpropagation, rollouts under the same action model. | RQ3. |

No RL, no QD framework, no additional algorithms this phase -- five is
already enough to answer three RQs without turning this into a survey.

## Budget and seeds

- Same fairness principle as Phase 0: every algorithm gets the same state-
  expansion budget (Random and MCTS get it per-seed, not split across
  seeds).
- Exact numbers are set once Commit B exists, using the rule: budget stays
  large enough that Random has a realistic chance on the *dev* set's
  hardest case (E5's 40,012-expansion median is the current reference
  point), and `MAX_DEPTH` >= 2x the longest known minimal sequence in
  either suite.
- Random and MCTS: 10 seeds, same as Phase 0. Median AND IQR reported (see
  Metrics).
- Graph baseline and Beam variants stay deterministic, one run each.

## Metrics

Carried over from Phase 0:
- Exploit Recall
- Search Cost (state expansions to first discovery)
- Time-to-Exploit (wall clock)

New this phase:
- **Success Rate**: for stochastic algorithms (Random, MCTS), fraction of
  seeds that find a given exploit at all, not just the median cost among
  the seeds that did.
- **Unique Exploits Per Run**: within a single run/seed, how many distinct
  exploits does it stumble onto, not just whether the union across seeds
  eventually covers everything. Distinguishes "reliably broad" from
  "occasionally gets lucky on one, over and over."
- **Cost distribution**: median *and* IQR for stochastic algorithms, not
  median alone -- a tight IQR and a wide one with the same median are
  different reliability stories.

## Hyperparameter calibration rules

This is the section Phase 0 got wrong and is fixing:

1. **Dev-set only.** Every hyperparameter (`novelty_weight`, `beam_width`,
   `novelty_k`, MCTS's exploration constant / simulation count / rollout
   depth, Graph baseline's cycle-detection threshold if any) is selected
   using E1-E5 and E1-E5 alone. The held-out suite is never touched until
   Commit E.
2. **Prefer answer-key-free diagnostics over exploit-family diagnostics.**
   Where a diagnostic is needed to pick a value, use ones that don't
   require knowing which exploit is which: descriptor entropy, average
   pairwise novelty in the beam, number of occupied behavior bins, count
   of unique reachable states. `FAMILY`-based diagnostics (what Phase 0
   Round 2 actually used) are avoided this time, not just re-labeled.
3. **Prefer literature defaults over any tuning at all.** MCTS's UCT
   exploration constant defaults to the standard `sqrt(2)` unless there's
   a concrete reason to sweep it; a parameter that doesn't need tuning
   can't leak anything.
4. Every calibration choice gets one sentence in the results doc on *how*
   it was picked, in the same spirit as Phase 0's README -- so the next
   reviewer doesn't have to reconstruct it from git blame.

## Success criteria (sealed before Commit E)

Not a single PASS/FAIL like Phase 0 -- three separate verdicts, one per RQ,
each STRONG / WEAK / NO EVIDENCE, evaluated on the **held-out suite only**:

- **RQ2 (diversity)**: STRONG if Beam-Diverse beats Beam-Naive on held-out
  recall, or matches recall with lower median cost, on at least 2 of 3
  held-out cases. WEAK if it wins on exactly 1. NO EVIDENCE if it never
  wins or loses recall anywhere it previously won.
- **RQ3 (lookahead)**: STRONG if MCTS finds H2 (or any held-out case
  Beam-Diverse fails) with cost <= 50% of Random's median, or Random fails
  within budget while MCTS succeeds. WEAK if MCTS finds it but without
  that cost advantage. NO EVIDENCE if MCTS also fails.
- **RQ1 (structure-dependent method choice)**: not a pass/fail -- a
  results table across all 5 algorithms x all 8 cases (5 dev + 3
  held-out), reported as-is. The "ideal" outcome described earlier
  (Graph wins the simple cases, Diverse Beam wins the cross-verb ones,
  MCTS wins the delayed-reward ones) is a hope, not a requirement -- if
  Graph wins everything, that's a valid and reportable answer to RQ1 too.

As in Phase 0: if a held-out result disappoints, it does not get
re-tuned. A disappointing but honest result closes Phase 2 with a written
verdict; it does not trigger a Round 3.

## Commit sequence

| Commit | Content | Gate |
|---|---|---|
| A | This contract. | Needs review before B. |
| B | Held-out benchmark (H1-H3) + dev suite re-declared (E1-E5, referencing Phase 0/1 code). Sealed on commit -- no algorithm code exists yet. | Needs review before C. |
| C | Graph baseline + MCTS implementations, Beam-Naive/Beam-Diverse ported unchanged from Phase 1. | -- |
| D | Calibration run: all hyperparameters selected on the dev suite only, per the rules above. | Frozen before E. |
| E | Held-out evaluation: run once, grade RQ1-3, write results. No further tuning afterward regardless of outcome. | Terminal. |

## Explicit non-goals (unchanged from Phase 0/1)

No cross-system exploits (Phase 3), no LLM, no UI, no adapters/plugin
system, no config framework, no RL, no QD framework, no real-game
integration. Five algorithms and eight benchmark cases is the entire
scope of Phase 2.
