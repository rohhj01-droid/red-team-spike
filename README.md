# Phase 0 Feasibility Spike -- Game System Red Team

Status: **frozen**. This is an experiment record, not a codebase to keep
extending. Phase 1 (Minimal Core) starts as new code informed by what's
below, not as a refactor of these files.

## Question this spike answered

Can automated search find hand-planted exploits in a small economy+crafting
system, and does Beam Search show a real advantage over Random on the
delayed-reward cases?

## Spike Contract (sealed before any code was written)

- **Environment**: Economy + Crafting only (no quest/equipment/buff/combat).
- **Actions**: `Buy`, `Sell`, `Craft`, `Dismantle` (4 kinds).
- **Algorithms**: Random Search, Beam Search. No MCTS, no RL.
- **Budget**: 100,000 state expansions -- same cap for Beam and for EACH
  Random seed (not split across seeds).
- **Random fairness**: 10 seeds, median cost used for comparison (a single
  seed run is not trusted -- Random has luck).
- **Metrics**: Exploit Recall, Search Cost (state expansions), Time-to-Exploit.
- **Forbidden**: adapters, config system, CLI, UI, plugin architecture,
  generalizing beyond this one synthetic game.

### Exploits (sealed before the code that finds them was written)

| ID | Mechanism | Minimal actions |
|----|-----------|-----------------|
| E1 | Trinket priced wrong: sell price (65) > buy price (50). Buy -> Sell loop. | 2 |
| E2 | Plank recipe (1 Wood + 1 Stone, cost 10) sells for 40. Craft margin. | 4 |
| E3 | Blade craft consumes 1 Iron; Dismantle(Blade) returns 3 Iron (bug, not the inverse of craft). Duplication loop. | 4 |
| E4 | Gear craft consumes 2 Copper; Dismantle(Gear) returns 1 Coal (byproduct type-change leak, sellable for more than the Copper cost). Cross economy/crafting loop. | 5 |
| E5 | Potion -> Dismantle -> 1 Herb. Herb has no shop entry. Bundle recipe needs 5 Herb; Bundle sells for 90. No partial profit until all 5 Herb are collected -- delayed-reward / long-horizon case. | 12 |

### Round 1 grading (sealed)

- **PASS**: Recall >= 4/5 AND Beam beats Random on E4 or E5 (cost <= 50% of
  Random's median, or Random fails within budget while Beam succeeds).
- **AMBIGUOUS**: Recall == 3/5, OR Recall >= 4/5 but no Beam advantage on E4/E5.
- **FAIL**: Recall <= 2/5.
- "Recall" = an exploit counts as found if EITHER algorithm found it at all.

## Two implementation bugs found and fixed mid-spike

Both were caught by refusing to trust results that looked too good, tracing
the actual discovered action paths, and checking they causally match the
claimed mechanism -- not just by eyeballing the summary numbers.

1. **Exploit attribution false positive.** The first grading pass credited
   an exploit as "found" whenever its items merely appeared anywhere in a
   profitable path -- e.g. a path whose profit came entirely from flipping
   Trinket (E1) also got credited for E5 because it happened to buy a
   Potion along the way, with no `craft(Bundle)` or `sell(Bundle)` anywhere
   in it. Fixed in `economy.discovered_exploits`: isolate each exploit
   family's own actions (original relative order), replay them ALONE from
   a fresh `initial_state`, and credit the family only if that isolated
   replay is itself profitable.

2. **Value heuristic double-counting.** `estimate_values()` propagated a
   craftable item's full sell value back to *every* required input
   independently. Plank (sells for 40) needs both Wood and Stone, so each
   got credited the full 40 -- meaning a single `buy(Wood)` looked like a
   +35 score gain on its own, with nothing ever crafted or sold. This
   flooded Beam-Naive's beam with Wood-buying states. Fixed by propagating
   value only through single-input recipes; multi-input recipes are
   skipped rather than apportioned, since under-crediting is a safe
   spike shortcut and over-crediting silently corrupts the search.

## Round 1: Beam-Naive

Selection: pure economic `score()` = gold + estimated liquidation value of
inventory. Top-`beam_width` by that score survive each layer.

| exploit | beam_found | beam_cost | random_found | random_median_cost |
|---|---|---|---|---|
| E1 | True | 13 | 10/10 | 17 |
| E2 | True | 259 | 10/10 | 48 |
| E3 | True | 302 | 10/10 | 73 |
| E4 | **False** | -- | 10/10 | 1,255 |
| E5 | **False** | -- | 6/10 | 40,012 |

**ROUND 1 VERDICT: AMBIGUOUS** (Recall 5/5, but no Beam advantage on E4/E5 --
Beam-Naive found neither.)

### Diagnosis: mode collapse (verified, not assumed)

Tracked which sealed exploit families were represented in the top-50 beam
at each layer (diagnostic only -- this label was never available to the
search itself):

```
layer 5:  E1=49/50  E3=14  E2=22  E5=11  E4=6
layer 6:  E1=50/50  E3=14  E2=21  E5=8   E4=7
layer 10: E1=50/50  E3=8   E2=17  E5=11  E4=5
```

By layer 6, every single beam slot includes a Trinket purchase (+15
score/action, cheaper and more reliable than any other branch). The beam
converges onto one dominant strategy and starves the branches that need to
survive several unprofitable-looking steps before paying off (E4, E5).

## Round 2 (H2): Beam-Diverse

**Hypothesis**: Beam-Naive's failure is diversity collapse, not a
fundamental search limit. A selection rule that also rewards behavioral
difference -- using ONLY generic, exploit-agnostic descriptors -- should
recover E4/E5 without ever being told which items belong to which sealed
exploit (that would leak the answer key into the algorithm).

**Behavior descriptor** (`search.behavior_descriptor`, never references
`FAMILY`/E1..E5): action-kind ratios (buy/sell/craft/dismantle fraction of
the path), distinct item types held, total units held, gold as a fraction
of starting gold, fraction of recipes currently craftable, path length
fraction. Novelty = mean distance to the `k=8` nearest neighbors in the
current candidate pool.

**Combination rule**: rank-normalized sum, not a raw-magnitude weighted
sum. A first attempt (`objective_score + weight * novelty`) failed even at
large weights: raw economic score grows every layer for a dominant
strategy (unbounded), while novelty distance is bounded by the descriptor
space, so any fixed-magnitude weight eventually gets swamped -- it only
delays the collapse, verified by testing weight=30 and still seeing E1
saturate the beam by layer 7. Fixed by ranking both the objective score and
the novelty score onto `[0, 1]` before combining, so the trade-off stays
meaningful regardless of how large raw scores get.

**`novelty_weight = 3.0`**: chosen by checking the family-diversity
diagnostic (the same kind used to diagnose Round 1, NOT the sealed
PASS/AMBIGUOUS/FAIL success metric) at weight = 1, 2, 3, 5, and picking the
value with the healthiest spread. This calibration happened before looking
at whether E4 or E5 were actually found, so it is not after-the-fact
benchmark-score tuning -- but it is **not** exploit-ID-free either: the
diagnostic it was calibrated against is literally `FAMILY` (E1..E5). See
"What this does and doesn't prove" below -- the runtime algorithm never
sees `FAMILY`, but the human calibration step did, and that distinction
matters for what Round 2 can honestly be claimed to show.

### Round 2 grading (sealed before this run)

- **STRONG SUCCESS**: Beam-Diverse finds E4 or E5 with cost <= 50% of
  Random's median (or Random fails within budget while Diverse succeeds),
  AND E1/E2/E3 recall is not sacrificed.
- **WEAK SUCCESS**: E4 or E5 found but no cost advantage over Random.
- **FAILURE**: neither E4 nor E5 found. Beam is not tuned further after
  this -- MCTS/QD become later-phase questions, not more knob-turning here.

### Round 2 result

| exploit | beam_found | beam_cost | random_found | random_median_cost |
|---|---|---|---|---|
| E1 | True | 21 | 10/10 | 17 |
| E2 | True | 245 | 10/10 | 48 |
| E3 | True | 237 | 10/10 | 73 |
| **E4** | **True** | **718** | 10/10 | 1,255 |
| E5 | False | -- | 6/10 | 40,012 |

**ROUND 2 VERDICT: WEAK SUCCESS.** E4 recovered (718 vs Random's median
1,255 -- genuinely cheaper, ~43% fewer expansions, but short of the
pre-sealed 50%-of-median bar of 627.5). E1-E3 unaffected. E5 still
unsolved by either Beam variant.

### What this does and doesn't prove

`behavior_descriptor()` and the selection rule (`obj_rank + novelty_weight *
novelty_rank`) never reference `FAMILY`/E1..E5 at runtime -- that part of
the exploit-ID-leakage guard held. But `novelty_weight = 3.0` was picked by
a human (me) looking at a family-diversity diagnostic across weight = 1, 2,
3, 5, and `FAMILY` **is** the sealed answer key. So the honest claim is:

- The search algorithm's features contain no exploit-identity information. ✅
- The overall Round 2 *experiment*, including hyperparameter selection,
  used exploit-family labels indirectly. ⚠️

This does not invalidate the WEAK SUCCESS verdict -- Phase 0 is a
feasibility spike, not a generalization claim. But Round 2 must not be
cited later as "Beam-Diverse generalizes to unseen exploits without any
information about where they are." It is an exploratory result, calibrated
on the same benchmark it was evaluated against. Phase 2 fixes this by
splitting a calibration set from a held-out evaluation set, and by
calibrating hyperparameters with answer-key-free diagnostics (descriptor
entropy, average pairwise novelty, occupied behavior bins, unique reachable
states) instead of family-diversity counts.

No further tuning was done after this run (no weight/`k` re-sweeps chasing
E4 over the strong-success line or chasing E5) -- that was the point of
sealing the grading bands in advance.

## What Phase 0 actually proved

1. The `State -> Action -> Transition -> exploit oracle` structure works:
   all 5 exploits were found by at least one method.
2. Algorithm choice measurably changes outcomes -- Beam-Naive is strictly
   worse than Random on the hard cases; adding diversity measurably (not
   just anecdotally) improves it on E4.
3. E5 (12 specific actions, no partial profit signal until the last step)
   resists every 1-step-lookahead method tried, including the
   diversity-preserving one. This is now a *verified*, not assumed, reason
   to bring in a lookahead method (MCTS) in a later phase -- and E5 is kept
   exactly as-is as that method's first benchmark case:

   | Algorithm | E5 |
   |---|---|
   | Random | 6/10, median 40,012 |
   | Beam-Naive | FAIL |
   | Beam-Diverse | FAIL |
   | MCTS | *(future phase)* |

4. The exploit oracle is a real, nontrivial part of the system, not
   plumbing -- both bugs found here were oracle/heuristic bugs, not search
   bugs, and one of them (false-positive attribution) is exactly the
   "did we find a real exploit or an artifact of our own detector" problem
   this whole project exists to take seriously.

## Final verdict

- Round 1: **AMBIGUOUS** (sealed, unchanged).
- Round 2: **WEAK SUCCESS** (sealed, unchanged) -- does not get rounded up
  to PASS; the pre-committed STRONG bar was not cleared.
- **Engineering decision: GO to Phase 1.** The spike's real question --
  "is this worth investing further in?" -- has a clear yes: the simulator
  works, algorithm choice matters and is measurable, and the one failure
  (E5) points at a specific, already-planned next technique (MCTS) instead
  of an open-ended unknown.
- MCTS is deliberately **not** added now -- E5 stays reserved as its first
  benchmark case instead of being used to rescue Phase 0's grade.
- **Round 2 is an exploratory result, not a generalization claim.** Its
  runtime features never used `FAMILY`, but `novelty_weight` was calibrated
  against a `FAMILY`-based diagnostic, so it must not later be cited as
  "generalizes to unseen exploits." Phase 2 separates calibration from
  held-out evaluation. See "What this does and doesn't prove" above.
