"""D.5: exact held-out instances. Authored AFTER algorithm implementation
(Commit C/C2) and calibration (Commit D/D2) were frozen -- git history is
the evidence, not this comment. cases_heldout.py (category-only, sealed
back in Commit B) is untouched; this is a new, separate file.

PRECISE CLAIM (D.5b correction -- an earlier commit message overstated
this): exact instances were not shaped around OBSERVED held-out algorithm
OUTCOMES -- no Random/Beam/MCTS/Graph result on H1-H3 existed anywhere
before this file did, and none is looked at while writing it. That is a
narrower claim than "algorithm-agnostic." H2 in particular is explicitly
built around a KNOWN, FROZEN algorithmic property (Beam-Diverse's
single-input-only value propagation rule assigns 0 derived value to
multi-input recipe ingredients) -- using that by design is exactly what
CONTRACT.md's H2 operational definition calls for, and is not the thing
being avoided. What's avoided is peeking at how H1-H3 actually turn out
under search and adjusting numbers to fit.
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
# Corrected in D.5b: the first version sold Trinket3 for 5 gold (a net
# loss once its Scrap cost is included, but still a REAL gold-liquidation
# path for Gem outside the intended mechanism -- a loss is still a
# liquidation, and the sealed oracle-validity constraint says NO
# legitimate liquidation path exists other than the intended one, full
# stop, not "no profitable one"). Fixed by removing Trinket3 from
# shop_sell entirely -- it is now a genuine dead end, like H1's Husk.
# Also reduced Gem from 3 to 1: with 3, a search could waste a Gem on
# Trinket3 and still recover via the other 2, which undercuts what
# "irreversible branching" is supposed to test. With exactly 1, the first
# choice is the only choice -- get it right or the exploit is permanently
# gone, matching the category condition ("wrong choice burns the resource
# with no easy recovery") much more literally.
CASE_H3 = Case(
    name="H3",
    mechanism="1 Gem (never purchasable, all-or-nothing); Amulet (profitable) and Trinket3 (a real recipe leading nowhere -- no sell path) both consume the single Gem.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Scrap": 10, "Widget2": 12},
        shop_sell={"Amulet": 40, "Widget2": 9},
        recipes={"Amulet": {"Gem": 1}, "Trinket3": {"Gem": 1, "Scrap": 1}},
        dismantle={},
        initial_inventory=(("Gem", 1),),
    ),
    minimal_path=[Action("craft", "Amulet"), Action("sell", "Amulet")],
    distractor_items=["Scrap", "Trinket3", "Widget2"],
)

ALL_HELDOUT_CASES = [CASE_H1, CASE_H2, CASE_H3]
