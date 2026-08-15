"""Phase 1 Minimal Core: the Synthetic RPG's state/action/transition model.

Ported from Phase 0 (../economy.py) as-is -- nothing generalized. We still
have exactly one game, so there is no second example to generalize FROM yet
("Generalize from evidence, not imagination"). This is not a GameModel
interface; it IS the one game, concretely.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

STARTING_GOLD = 300

SHOP_BUY: Dict[str, int] = {
    "Trinket": 50,   # E1: priced wrong, sells for more than it costs
    "Wood": 5,
    "Stone": 5,
    "Iron": 10,
    "Copper": 8,
    "Potion": 10,
}

SHOP_SELL: Dict[str, int] = {
    "Trinket": 65,   # E1
    "Plank": 40,     # E2
    "Iron": 10,      # E3 (sell the duplicated iron)
    "Coal": 20,      # E4
    "Bundle": 90,    # E5
}

RECIPES: Dict[str, Dict[str, int]] = {
    "Plank": {"Wood": 1, "Stone": 1},   # E2: craft margin
    "Blade": {"Iron": 1},               # E3
    "Gear": {"Copper": 2},              # E4
    "Bundle": {"Herb": 5},              # E5: needs 5 accumulated Herb
}

DISMANTLE: Dict[str, Dict[str, int]] = {
    "Blade": {"Iron": 3},    # E3 bug: crafted from 1 Iron, returns 3
    "Gear": {"Coal": 1},     # E4 bug: Copper turns into sellable Coal
    "Potion": {"Herb": 1},   # E5
}


@dataclass(frozen=True)
class GameState:
    gold: int
    inventory: Tuple[Tuple[str, int], ...]  # sorted, qty > 0 only -> hashable

    def qty(self, item: str) -> int:
        for name, n in self.inventory:
            if name == item:
                return n
        return 0


def initial_state() -> GameState:
    return GameState(gold=STARTING_GOLD, inventory=())


@dataclass(frozen=True)
class Action:
    kind: str    # "buy" | "sell" | "craft" | "dismantle"
    target: str  # item name, or recipe/output name for craft

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})"


def _with_inventory(state: GameState, deltas: Dict[str, int]) -> Tuple[Tuple[str, int], ...]:
    inv = dict(state.inventory)
    for item, delta in deltas.items():
        inv[item] = inv.get(item, 0) + delta
    return tuple(sorted((k, v) for k, v in inv.items() if v > 0))


def legal_actions(state: GameState) -> List[Action]:
    actions: List[Action] = []
    for item, price in SHOP_BUY.items():
        if state.gold >= price:
            actions.append(Action("buy", item))
    for item in SHOP_SELL:
        if state.qty(item) > 0:
            actions.append(Action("sell", item))
    for output, inputs in RECIPES.items():
        if all(state.qty(i) >= n for i, n in inputs.items()):
            actions.append(Action("craft", output))
    for item in DISMANTLE:
        if state.qty(item) > 0:
            actions.append(Action("dismantle", item))
    return actions


def apply(state: GameState, action: Action) -> GameState:
    if action.kind == "buy":
        price = SHOP_BUY[action.target]
        return GameState(state.gold - price, _with_inventory(state, {action.target: 1}))
    if action.kind == "sell":
        qty = state.qty(action.target)
        price = SHOP_SELL[action.target]
        return GameState(state.gold + price * qty, _with_inventory(state, {action.target: -qty}))
    if action.kind == "craft":
        deltas = {i: -n for i, n in RECIPES[action.target].items()}
        deltas[action.target] = deltas.get(action.target, 0) + 1
        return GameState(state.gold, _with_inventory(state, deltas))
    if action.kind == "dismantle":
        deltas = {action.target: -1}
        for out_item, n in DISMANTLE[action.target].items():
            deltas[out_item] = deltas.get(out_item, 0) + n
        return GameState(state.gold, _with_inventory(state, deltas))
    raise ValueError(f"unknown action kind: {action.kind}")
