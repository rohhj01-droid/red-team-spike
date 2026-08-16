"""Dev suite: five isolated environments, each E1-E5's original mechanism
plus 2-3 benign distractor items that provide comparable branching noise
but are verified (see verify_cases.py) never to be profitable, alone or
in combination. Not a reuse of ../economy.py or ../phase1/model.py -- see
CONTRACT.md "Every case is an isolated environment" for why.

Each case's MINIMAL_PATH is the known-correct exploit sequence, used by
verify_cases.py to confirm the case is wired correctly before it becomes
the frozen dev suite calibration runs against.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from engine import Action, GameData


@dataclass(frozen=True)
class Case:
    name: str
    data: GameData
    minimal_path: List[Action]
    mechanism: str
    distractor_items: List[str]  # items belonging only to the decoy path(s), for verify_cases.py's QA use only


CASE_E1 = Case(
    name="E1",
    mechanism="Direct price arbitrage: Trinket sells for more than it costs.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Trinket": 50, "Bauble": 30, "Charm": 40},
        shop_sell={"Trinket": 65, "Bauble": 25, "Charm": 35},
        recipes={},
        dismantle={},
    ),
    minimal_path=[Action("buy", "Trinket"), Action("sell", "Trinket")],
    distractor_items=["Bauble", "Charm"],
)

CASE_E2 = Case(
    name="E2",
    mechanism="Crafting margin: Plank sells for more than its ingredients cost.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Wood": 5, "Stone": 5, "Twine": 8, "Splinter": 8},
        shop_sell={"Plank": 40, "Nail": 12},
        recipes={"Plank": {"Wood": 1, "Stone": 1}, "Nail": {"Twine": 1, "Splinter": 1}},
        dismantle={},
    ),
    minimal_path=[Action("buy", "Wood"), Action("buy", "Stone"), Action("craft", "Plank"), Action("sell", "Plank")],
    distractor_items=["Twine", "Splinter", "Nail"],
)

CASE_E3 = Case(
    name="E3",
    mechanism="Dismantle duplication: Blade crafted from 1 Iron dismantles into 3.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Iron": 10, "Copper": 8},
        shop_sell={"Iron": 10, "Copper": 7},
        recipes={"Blade": {"Iron": 1}, "Rivet": {"Copper": 1}},
        dismantle={"Blade": {"Iron": 3}, "Rivet": {"Copper": 1}},  # Rivet's dismantle is honest (no duplication)
    ),
    minimal_path=[Action("buy", "Iron"), Action("craft", "Blade"), Action("dismantle", "Blade"), Action("sell", "Iron")],
    distractor_items=["Copper", "Rivet"],
)

CASE_E4 = Case(
    name="E4",
    mechanism="Byproduct type-change leak: Cog (2 Zinc) dismantles into sellable Slag.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Zinc": 8, "Tin": 6},
        shop_sell={"Slag": 20, "Tin": 5},
        recipes={"Cog": {"Zinc": 2}, "Washer": {"Tin": 2}},
        dismantle={"Cog": {"Slag": 1}, "Washer": {"Tin": 1}},  # Washer's dismantle is an honest partial refund
    ),
    minimal_path=[
        Action("buy", "Zinc"), Action("buy", "Zinc"), Action("craft", "Cog"),
        Action("dismantle", "Cog"), Action("sell", "Slag"),
    ],
    distractor_items=["Tin", "Washer"],
)

CASE_E5 = Case(
    name="E5",
    mechanism="Delayed accumulation: 5 Herb (only obtainable by dismantling Potion) -> Bundle, no partial profit until the last step.",
    data=GameData(
        starting_gold=300,
        shop_buy={"Potion": 10, "Bud": 12},
        shop_sell={"Bundle": 90},
        recipes={"Bundle": {"Herb": 5}},
        dismantle={"Potion": {"Herb": 1}, "Bud": {"Petal": 1}},  # Petal is a dead end: no sell price, no recipe uses it
    ),
    minimal_path=(
        [Action("buy", "Potion"), Action("dismantle", "Potion")] * 5
        + [Action("craft", "Bundle"), Action("sell", "Bundle")]
    ),
    distractor_items=["Bud", "Petal"],
)

ALL_DEV_CASES = [CASE_E1, CASE_E2, CASE_E3, CASE_E4, CASE_E5]
