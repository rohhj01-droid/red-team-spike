# Phase 2 Benchmark Specification (Commit B)

Sealed per CONTRACT.md. Dev suite is fully concrete. Held-out suite is
category-only -- see the last section.

## Common action semantics

One shared engine (`engine.py`), not per-case code: `buy`, `sell`, `craft`,
`dismantle` over a `GameData` bundle (`starting_gold`, `shop_buy`,
`shop_sell`, `recipes`, `dismantle`). Identical rules for every case:

- `buy(item)`: legal if `gold >= shop_buy[item]`; spends the price, adds 1
  unit.
- `sell(item)`: legal if holding `>0` of an item in `shop_sell`; sells the
  **entire held quantity** in one action, adds `qty * price` gold.
- `craft(output)`: legal if holding enough of every input `recipes[output]`
  requires; consumes them, adds 1 unit of `output`.
- `dismantle(item)`: legal if holding `>=1`; consumes 1, adds
  `dismantle[item]`'s declared outputs (deliberately not required to be
  the inverse of any recipe -- that mismatch is where E3/E4's bugs live).

## Common exploit success predicate

`oracle.is_exploit_found(data, path)`: replay `path` from `initial_state`
using ONLY `engine.apply`; the exploit is found iff realized `gold` ends
strictly greater than `data.starting_gold`. **Never references any search
heuristic's estimated value** -- see `oracle.py`'s docstring for why that
separation is a hard rule, not a style preference.

## Dev suite (E1-E5), fully sealed

Five isolated environments (`cases_dev.py`), each E1-E5's original
mechanism plus 2-3 benign distractor items providing comparable branching
noise. All five pass exhaustive verification (`verify_cases.py`): the
declared minimal path is confirmed correct, nothing shorter exists, and no
distractor-only path is ever profitable (checked by full breadth-first
enumeration of reachable states, not sampling).

| Case | Mechanism | Real items | Distractor items | Minimal depth | Realized gain | Nominal action types |
|---|---|---|---|---|---|---|
| E1 | Trinket sells for more than it costs (50 buy / 65 sell) | Trinket | Bauble, Charm | 2 | +15 | 6 |
| E2 | Plank (1 Wood + 1 Stone, cost 10) sells for 40 | Wood, Stone, Plank | Twine, Splinter, Nail | 4 | +30 | 8 |
| E3 | Blade (1 Iron) dismantles into 3 Iron | Iron, Blade | Copper, Rivet | 4 | +20 | 8 |
| E4 | Cog (2 Zinc) dismantles into sellable Slag | Zinc, Cog, Slag | Tin, Washer | 5 | +4 | 8 |
| E5 | 5 Herb (only from dismantling Potion) -> Bundle, no profit until the last step | Potion, Herb, Bundle | Bud, Petal | 12 | +40 | 6 |

All five: `starting_gold = 300`. Exact `GameData` for each is in
`cases_dev.py`; do not hand-transcribe the numbers elsewhere -- import
`ALL_DEV_CASES`.

Note on distractor design: each distractor is either a strict-loss decoy
of the same shape as the real mechanism (E1-E4: buying/crafting something
that costs more than it sells for) or a dead end with the same *action
shape* as the real mechanism but no path to profit at all (E5's Bud/Petal
mirrors Potion/Herb's buy-then-dismantle pattern exactly, but Petal has no
recipe and no sell price -- verified, not assumed, to never pay off no
matter how long a search dwells there).

This is not a reuse of `../economy.py` or `../phase1/model.py` (both stay
frozen, historical). It is a new declaration of the same five mechanisms
under Phase 2's isolated-environment design -- see CONTRACT.md "Every case
is an isolated environment" for why dev had to be re-declared this way
instead of reused as-is.

## Held-out suite (H1-H3), category-only

**No concrete data exists for these. See `cases_heldout.py` -- it contains
only the category conditions, nothing that resembles a `GameData`.** Exact
instances are Commit D.5's job, after algorithm implementation and
calibration are frozen (CONTRACT.md).

| Category | Condition | Drives |
|---|---|---|
| H1 | Resource bottleneck: a profitable action is available only a limited number of times. | RQ1 (supporting only) |
| H2 | Genuinely lossy intermediate step: realized value drops at the step itself, payoff comes later from a separate combination. | RQ3 (sole verdict case) |
| H3 | Branching recipe choice: a shared input has two+ uses, only one profitable, wrong choice is unrecoverable. | RQ1 (supporting only) |
