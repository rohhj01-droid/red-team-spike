# Phase 2 Contract

Status: **draft, not yet executed (revision A2).** No benchmark data, no
algorithm code exists for Phase 2 yet. This document is Commit A in the
sequence below -- it is meant to be reviewed and locked *before* any of
that is written. A2 revises the original Commit A after review caught a
reverse-leakage risk in the commit order and several grading/definition
issues; see the Commit sequence table for what changed.

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
document. **Commit B fixes only the categories above (H1/H2/H3's
conditions) -- not exact instances.** Exact instances are authored in a
separate step (D.5, see Commit sequence) *after* algorithm implementation
and calibration are frozen, not before. The original plan here (write
exact H1-H3 numbers in Commit B, before Commit C's Graph/MCTS code) had a
reverse-leakage risk: an implementer who has just read H2's exact "looks
lossy" numbers could unconsciously shape MCTS's reward/rollout to handle
it well. Sealing only the category first, and generating exact numbers
after the algorithms are already frozen, closes that direction too.

One limitation stays honest rather than hidden: the same author (me)
writes both the algorithm code (Commit C) and the exact held-out instances
(D.5) in the same continuous session, so this is category-level blinding,
not the full blinding a separate benchmark author would give. When
reporting Phase 2, the accurate phrase is "held-out instances from
predeclared novel mechanism categories," never "unseen mechanism
generalization" -- the mechanism *category* was known in advance by
design; only the exact instance parameters were decided after the freeze.

## Algorithms

| Algorithm | What it is | Primarily informs |
|---|---|---|
| Random | Unchanged from Phase 0/1. | Baseline for all three RQs. |
| **Static Conversion-Cycle Baseline** (new; not "Graph/Cycle" -- see below) | Deterministic: models *single-input* item conversions as a weighted directed graph, detects positive-value cycles (Bellman-Ford-style). | RQ1 -- is search even necessary for the simple cases, and where exactly does that stop being true? |
| Beam-Naive | Unchanged from Phase 1. | RQ1, RQ2 (as the thing Beam-Diverse must beat). |
| Beam-Diverse | Unchanged from Phase 1, but its hyperparameters get re-calibrated under the new rules below -- not reused as-is from Phase 0. | RQ2. |
| **MCTS** (new) | Standard UCT: selection/expansion/simulation/backpropagation, rollouts under the same action model. | RQ3. |

No RL, no QD framework, no additional algorithms this phase -- five is
already enough to answer three RQs without turning this into a survey.

### Static Conversion-Cycle Baseline is deliberately narrow

A plain directed graph edge (`A -> B`) cannot represent a multi-input
recipe like `Wood + Stone -> Plank` (E2) without becoming a hypergraph /
stoichiometric-flow problem -- real scope, not a detail. Rather than build
that (a general hypergraph optimizer has no business in Phase 2), the
baseline is scoped to single-input transformations only. Multi-input
recipes (E2) and stateful/finite-resource rules (H1) are reported as
`N/A -- unsupported`, not force-fit into a graph they can't represent. This
is not a weakness to work around; it's the point -- RQ1's answer table
should show exactly where "just do graph cycle detection" stops being
sufficient and real search has to take over.

## Budget and seeds

**Common unit: one transition evaluation = one `apply(state, action)` call
that produces a successor state.** This was ambiguous in the Phase 0 code
(fine there, since only Random and Beam existed and both happened to cost
1 `apply()` per unit already) but MCTS makes the ambiguity real: a single
simulation does selection + expansion + a multi-step rollout, and if
rollout steps aren't counted the same as tree-expansion steps, MCTS gets
an uncosted advantage by construction, not by being a better algorithm.
Fixed mapping, no exceptions:

- Random: 1 action taken = 1 evaluation.
- Beam (Naive/Diverse): 1 candidate successor generated = 1 evaluation.
- MCTS: every `apply()` call counts the same whether it happens during
  tree expansion or during rollout -- 1 evaluation each, summed across
  both.

- Same fairness principle as Phase 0: every algorithm gets the same
  transition-evaluation budget (Random and MCTS get it per-seed, not split
  across seeds).
- Exact numbers are set once Commit B's categories are turned into
  instances (D.5), using the rule: budget stays large enough that Random
  has a realistic chance on the *dev* set's hardest case (E5's
  40,012-evaluation median is the current reference point), and
  `MAX_DEPTH` >= 2x the longest known minimal sequence in either suite.
- Random and MCTS: 10 seeds, same as Phase 0. Median AND IQR reported (see
  Metrics).
- Beam variants stay deterministic, one run each.
- **Static Conversion-Cycle Baseline is not budget-comparable** -- it's not
  a search algorithm in this sense. Report it separately: supported /
  unsupported per case, wall-clock time, and number of graph
  nodes/transformations inspected. Do not force it into the same
  transition-evaluation number just to fit one table.

## Metrics

Carried over from Phase 0:
- Exploit Recall
- Search Cost (transition evaluations to first discovery -- see Budget and
  seeds for the common unit definition)
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

This is the section Phase 0 got wrong -- but Phase 0's actual mistake was
narrower than "used exploit labels." It was: **E1-E5 was simultaneously
the calibration set and the only evaluation set**, so calibrating against
`FAMILY` and then reporting the result as evidence conflated tuning
performance with generalization evidence. Now that dev (E1-E5) and
held-out (H1-H3) are genuinely separate, using dev labels to tune is just
normal validation-set practice -- it is not the thing to avoid.

1. **The only hard rule: held-out information never touches calibration.**
   `novelty_weight`, `beam_width`, `novelty_k`, MCTS's simulation count /
   rollout depth, and any Static Conversion-Cycle Baseline threshold are
   all selected using E1-E5 only. H1-H3 stay unseen by any calibration
   step, full stop, through Commit D.
2. **Using E1-E5's actual exploit recall/cost to tune is explicitly fine,
   and often the more honest choice.** Task-oriented calibration (pick the
   `novelty_weight` that finds the most dev exploits fastest) is standard
   practice on a real validation set -- Phase 0's problem was the missing
   held-out split, not the use of labels per se.
3. **Label-free diagnostics (descriptor entropy, average pairwise novelty,
   occupied behavior bins, unique reachable states) are a secondary tool**
   for cases where dev-label signal is too sparse to discriminate between
   candidate values (e.g. two settings tie on dev recall) -- not the
   mandated primary method.
4. **MCTS reward is defined as binary and pre-normalized to `[0, 1]`**:
   1 if a rollout beneath a node reaches a profitable state, 0 otherwise
   (the standard win/loss-style UCT reward, not raw gold). This is what
   makes the standard UCT exploration constant `c = sqrt(2)` a legitimate
   default rather than an arbitrary one -- `sqrt(2)` is only a principled
   choice when reward is bounded in `[0, 1]`. If a later phase needs a
   continuous reward instead, `c` must be calibrated on dev at that point,
   not assumed.
5. Every calibration choice gets one sentence in the results doc on *how*
   it was picked, in the same spirit as Phase 0's README -- so the next
   reviewer doesn't have to reconstruct it from git blame.

## Success criteria (sealed before Commit E)

Not a single PASS/FAIL like Phase 0 -- three separate verdicts, one per RQ,
each STRONG / WEAK / NO EVIDENCE, evaluated on the **held-out suite only**:

- **RQ2 (diversity)**: Beam-Naive and Beam-Diverse are both deterministic
  (one run each) -- no median exists for either, so "win" is defined
  per-case, not by cost margin alone. A case counts as a **Diverse win**
  if either (a) Diverse finds it and Naive doesn't, or (b) both find it
  and Diverse's cost <= 75% of Naive's (25% reduction, not 50% -- RQ2 is
  about whether diversity broadens what's found at all, not about a 2x
  speed bar). STRONG: Diverse wins on >= 2 of the 3 held-out cases AND
  never loses recall on a case Naive found. WEAK: exactly 1 win, no
  regressions. NO EVIDENCE: 0 wins, or Diverse loses recall anywhere.
  Note for the results doc: with only 3 held-out cases, even a STRONG
  verdict is suite-internal evidence, not a general scientific claim.
- **RQ3 (lookahead)**: the RQ asks whether MCTS beats 1-step heuristic
  search -- so the comparison target is **Beam-Diverse**, not Random
  (Random stays in the results table for context, but does not drive this
  verdict). STRONG: on H2 (or any held-out case Beam-Diverse fails), MCTS
  success rate >= 8/10 seeds AND (Beam-Diverse fails within budget OR
  MCTS's median cost <= 50% of Beam-Diverse's cost). WEAK: MCTS finds it
  but success rate < 8/10 or no cost advantage over Beam-Diverse.
  NO EVIDENCE: MCTS also fails.
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
| A | This contract (A2 revision: commit order fixed to prevent reverse leakage, baseline scope narrowed, RQ2/RQ3 grading corrected, cost unit defined, calibration rule corrected, UCT reward normalized). | Needs review before B. |
| B | Dev suite re-declared (E1-E5, referencing Phase 0/1 code) + held-out **categories only** (H1/H2/H3 conditions, no exact item/price/path). Sealed on commit -- no algorithm code exists yet. | Needs review before C. |
| C | Static Conversion-Cycle Baseline + MCTS implementations, Beam-Naive/Beam-Diverse ported unchanged from Phase 1. Implemented against the dev suite and the H-category *descriptions* only -- no exact held-out instance exists yet. | -- |
| D | Calibration run: all hyperparameters selected on the dev suite only, per the rules above. Every algorithm and parameter frozen at the end of this commit. | Frozen before D.5. |
| D.5 | Exact H1-H3 instances authored (item names, prices, recipes, stock caps) and committed. No algorithm or parameter changes after this point, for any reason. | Frozen before E. |
| E | Held-out evaluation: run once, grade RQ1-3, write results. No further tuning afterward regardless of outcome. | Terminal. |

## Explicit non-goals (unchanged from Phase 0/1)

No cross-system exploits (Phase 3), no LLM, no UI, no adapters/plugin
system, no config framework, no RL, no QD framework, no real-game
integration. Five algorithms and eight benchmark cases is the entire
scope of Phase 2.
