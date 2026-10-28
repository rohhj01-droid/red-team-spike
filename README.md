# Game System Red Team

An experiment in finding exploits in game systems by automated search,
and -- as it turned out -- in how much of that work can be done without
analyst discretion. 298 commits, 2026-08-15 to 2026-08-31. Designs,
contracts and grading rules were committed *before* the code or run
they govern, so that the commit order itself can show whether a result
was tuned after being seen. Failures are sealed as produced;
corrections are recorded, never deleted.

The record is organised by phase. Each phase's results document is the
authority for that phase; this page only says where things ended up.

## Phase 0 -- feasibility spike (this file, below)

Economy + crafting only, four actions, five planted exploits E1-E5,
Random vs. Beam at a 100,000-expansion budget. Round 1 (Beam-Naive):
**AMBIGUOUS**. Round 2 (Beam-Diverse, novelty-weighted): **WEAK
SUCCESS**, not rounded up. E5 -- twelve actions with no partial-profit
signal -- resisted every one-step-lookahead method and was reserved,
untouched, as the first benchmark for a lookahead method. Two bugs found
mid-spike were oracle bugs, not search bugs. Decision: GO.

## Phase 1 -- minimal core (`phase1/`)

Phase 0's single game re-expressed as `model.py` / `search.py` /
`profit_check.py`, no generalisation. Its only completion criterion was
reproducing Phase 0's frozen Round 1 and Round 2 numbers exactly
(`phase1/verify.py`). Sealed in the same commit as Phase 0 (`a56d2d5`).

## Phase 2 -- held-out evaluation (`phase2/RESULTS.md`)

Contract (`CONTRACT.md`) and benchmark (`BENCHMARK.md`) sealed before any
algorithm code. E1-E5 became permanent calibration data; three held-out
categories H1-H3 were instantiated only after algorithms and parameters
were frozen. Five methods: Random, Beam-Naive, Beam-Diverse, MCTS, and a
deterministic graph-cycle baseline. One terminal run, never re-tuned.

- **RQ1** (structure-dependent method choice): mixed. The static cycle
  baseline detected profitable structure in all four cases it supports
  but produced an executable witness in only one; unsupported on the
  scarcity and multi-input held-out cases.
- **RQ2** (diversity): no evidence it helps in this suite -- a
  scope-narrowing of Phase 0's Round 2, not a refutation.
- **RQ3** (lookahead): strong evidence MCTS earns its cost on H2, the
  case built around a genuinely lossy intermediate step.

## Phase 3 -- cross-system cases C1-C4 (`phase3/RESULTS_C*.md`)

Four synthetic cases, each designed to force one representation
question, each with an exhaustive closure QA against an independently
written reference (0 mismatches on every transition; a negative control
confirmed the check is sensitive).

| Case | Planted mechanism | What it forced | Frozen search result |
|---|---|---|---|
| C1 | quest claim requires *continuous* equipment | `WorldState` + separate `MonitorState` | all four methods found it (9 states; no ranking reported) |
| C2 | + a Buff whose validity depends on its source | violation judged at a specific transition, not as a state predicate -- found via a real false positive in the minimality QA | all four (19 states) |
| C3 | + an Enchantment provenance chain | one monitor field's update needs a *sibling* monitor field; proven by a constructed indistinguishability pair | **FAIL** -- both Beam variants (`ecbd536`, sealed) |
| C4 | + `consume`, whose legitimacy depends on an earlier `claim`'s verdict | a violation verdict must persist as state (`EventProvenanceState`) | **FAIL** -- Beam-Naive (`2a10826`, sealed) |

Both FAILs were explained by single-variable post-hoc diagnostics that
never overwrote the sealed result. C3: legitimately completed `CLAIMED`
states kept being expanded and crowded out every exploit-capable branch;
excluding them restored discovery (`e3bdfeb`). C4: the correct tainted
candidate reached the beam but tied in score with five clean ones and
was cut as the sixth under `BEAM_WIDTH=5`; the official search with
`beam_width=6` and nothing else changed found it (`ee25b0a`). The two
mechanisms are different, and C3's fix would make C4 strictly worse --
recorded as a reason *not* to generalise either into a fixed policy.

`RESULTS_C4.md` closes the synthetic sequence with the question it could
not answer itself: an architecture that fits four cases by one author
may be fitting the author's habits. Do these boundaries appear in a
system this project did not design?

## Phase 3.5 -- external validation (`phase3_5/`)

Methodology sealed at `401924d` (revision 3.5j), in
`docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`.
Its stated success condition is methodological, not directional: the
protocol is followed and the outcome reported as produced, whichever
way it points.

**Frame** (`FRAME_ENUMERATION.md`, `1de4559`): the official OpenBSD 7.9
`ports.tar.gz` (SHA256 `937aef3d…`, checked against the published
value), enumerated at `2026-08-26T19:23:05Z`. 477 ports declare
`games` in `CATEGORIES` -- 79 of them outside the `games/` directory --
and the first 128 in byte order are the screening set
(`screening_set_128.txt`).

**Screening** (`SCREENING_PROTOCOL.md`, `screening_*.tsv`,
`screening_evidence.md`): gates `UR → E1 → E2-REP → E2-RULE → E3 → E4`,
first failure stops, a network-access contract fixing which upstream
surfaces may be read at E2-REP. State at termination (QA-43):

```text
frame items screened   96 / 128
candidates             94    UNRESOLVED 86   ELIGIBLE 3   REJECTED 5
duplicates             2
```

All three ELIGIBLE candidates (C059, C065, C084) carry
`primary_snapshot = UNRESOLVED` in the ledger. C059's and C065's records
ground that in QA-28; C084's records it as a survivor-stage field this
run never reached.

**Result.** Target selection is **INCONCLUSIVE**, and was determined to
be so at QA-19, with 28 of the 128 frame items screened: ranking
would have to cross a class boundary the sealed rules leave undecided,
and the tie-break is barred from doing that work. In the record's own
words, *"a protocol can be rigorous enough to ADMIT candidates and
still unable to SELECT among them, because admission is existential and
selection is universal."* The run is therefore a screening-methodology
result rather than a target study, and the analysis Phase 3.5 was built
to perform did not take place.

**What the execution record holds** (`EXECUTION_QA.md`, 42 entries;
36 retraction blocks in `screening_evidence.md`). The findings with the
widest reach came late:

- QA-39 / QA-40: the frozen ports infrastructure defaults `HOMEPAGE` and
  `SITES` for ports that set `GH_*` identifiers; earlier entries had
  read both off the port Makefile alone and denied them.
- QA-41, RETRACTION 31 and 32: an E2-REP PASS asserts *exactly one*
  designated source location, and the sealed protocol lets E2-REP decide
  that only because its bounded search can be closed. Where an admitted
  starting point was never opened, the search was not closed. Eight of
  the eleven candidates then ELIGIBLE moved to UNRESOLVED, with every
  observation preserved.
- QA-42: the sealed `evidence_role` enum cannot describe a code host's
  account surface, which the starting-point rules nonetheless admit.

The phase was run under external review, and the review is visible in
the record rather than only asserted here: 32 of the phase's 251 commit
messages cite it, QA-41 and QA-42 state that they were written to
review findings about the analyst's own earlier corrections -- QA-41
logs the analyst overshooting in both directions one commit apart --
and RETRACTION 31 and 32 carry out QA-41's audit.

## Status (2026-10-28)

Screening terminated at 96 of 128 frame items, recorded as QA-43: a
deviation from the sealed budget, taken by the project owner's decision
after a two-month pause, with the coverage claim forfeited and the 96
terminal verdicts, the QA record and the INCONCLUSIVE selection outcome
unchanged. The entry names the sealed clauses it breaks, including
QA-19's own "screening still completes", and calls the stop what it is.
Rank 93 (`games/dhewm3`) has UR and E1 entries and no ledger row; ranks
93-104, 107-108 and 111-128 were not screened. The last external
observation was made on 2026-08-31 and nothing was observed after it.
Any further work on the remaining items would be a new run against the
same frozen frame, not a continuation of this one.

## Where to read

```text
phase2/RESULTS.md                     Phase 2 terminal run
phase3/RESULTS_C1.md … RESULTS_C4.md  one sealed results document per case
phase3_5/EXECUTION_QA.md              QA-01 … QA-42, in order found
phase3_5/screening_evidence.md        every observation, retraction, and
                                      superseded sentence, in place
phase3_5/screening_candidates.tsv     per-candidate verdicts
phase3_5/screening_frame_items.tsv    per-frame-item verdicts
```

The original Phase 0 record follows, unchanged.

---

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
