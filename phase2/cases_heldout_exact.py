"""D.5: exact held-out instances. Authored AFTER algorithm implementation
(Commit C/C2) and calibration (Commit D/D2) were frozen -- git history is
the evidence, not this comment. cases_heldout.py (category-only, sealed
back in Commit B) is untouched; this is a new, separate file.

Numbers here were NOT chosen by asking "would MCTS/Beam do well on this."
They were chosen by asking "does this satisfy H1/H2/H3's sealed category
condition, fit inside frozen MAX_DEPTH, and pass the same QA
verify_cases.py already applied to dev" -- see verify_heldout.py, which
never imports search.py or graph_baseline.py.
"""
from __future__ import annotations

from cases_dev import Case
from engine import Action, GameData

# --- H1: resource bottleneck --------------------------------------------
# 4 Seed, given only via initial_inventory (no shop_buy entry -- can never
# buy more). Sprout requires ALL 4 at once, so partial use is impossible;
# a single dismantle(Seed) permanently forfeits the only path to profit
# (Husk is a dead end: no recipe, no sell price). Seed itself has no
# shop_sell entry and no path to gold other than craft(Sprout) -- the
# oracle-validity constraint from cases_heldout.py H1 holds by construction.
CASE_H1 = Case(
    name="H1",
    mechanism="Resource bottleneck: exactly 4 Seed (never purchasable) required all at once to craft the only sellable output.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Gadget": 20},
        shop_sell={"Sprout": 50, "Gadget": 15},
        recipes={"Sprout": {"Seed": 4}},
        dismantle={"Seed": {"Husk": 1}},
        initial_inventory=(("Seed", 4),),
    ),
    minimal_path=[Action("craft", "Sprout"), Action("sell", "Sprout")],
    distractor_items=["Gadget"],
)

# --- H2: genuinely lossy intermediate step (RQ3 sole verdict case) ------
# Omega needs 2 Alpha + 2 Beta (multi-input recipe). Neither Alpha nor
# Beta has a shop_sell entry, and single-input-only value propagation
# (fixed in Phase 0) assigns NO derived value to an item that's only used
# by a multi-input recipe -- so every gold spent buying them is a pure
# drop in Beam-Diverse's frozen score() with nothing to offset it, all the
# way until Omega (which DOES have direct sell value) is actually crafted.
CASE_H2 = Case(
    name="H2",
    mechanism="Multi-input payoff (2 Alpha + 2 Beta -> Omega); neither ingredient has any heuristic-visible value until the craft itself resolves it.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Alpha": 15, "Beta": 15, "Ember": 18},
        shop_sell={"Omega": 100, "Ember": 14},
        recipes={"Omega": {"Alpha": 2, "Beta": 2}},
        dismantle={},
    ),
    minimal_path=[
        Action("buy", "Alpha"), Action("buy", "Alpha"),
        Action("buy", "Beta"), Action("buy", "Beta"),
        Action("craft", "Omega"), Action("sell", "Omega"),
    ],
    distractor_items=["Ember"],
)

# --- H3: branching recipe choice -----------------------------------------
# 3 Gem, given only via initial_inventory. Two recipes consume Gem: Amulet
# (profitable) and Trinket3 (a real recipe that's a net loss once its
# Scrap cost is included). Committing a Gem to Trinket3 forfeits it
# permanently -- Gem is never purchasable again. Gem has no shop_sell
# entry and no dismantle rule, so its only two possible fates are the two
# recipes; the oracle-validity constraint holds because Trinket3, while a
# "real" path, is a loss on its own (verified below), not a free liquidation.
CASE_H3 = Case(
    name="H3",
    mechanism="3 Gem (never purchasable); Amulet (profitable) and Trinket3 (a real recipe, net loss) both consume Gem -- wrong choice is unrecoverable per unit.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Scrap": 10, "Widget2": 12},
        shop_sell={"Amulet": 40, "Trinket3": 5, "Widget2": 9},
        recipes={"Amulet": {"Gem": 1}, "Trinket3": {"Gem": 1, "Scrap": 1}},
        dismantle={},
        initial_inventory=(("Gem", 3),),
    ),
    minimal_path=[Action("craft", "Amulet"), Action("sell", "Amulet")],
    distractor_items=["Scrap", "Trinket3", "Widget2"],
)

ALL_HELDOUT_CASES = [CASE_H1, CASE_H2, CASE_H3]
