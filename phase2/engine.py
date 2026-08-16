"""Phase 2 shared transition engine.

Generalized from phase1/model.py -- justified now, not before: Phase 2
needs the identical buy/sell/craft/dismantle semantics repeated across 5
dev cases (and later 3 held-out cases), which is real "rule of three"
evidence. This is still just this one economy-shaped game, parameterized
by data instead of hardcoded -- not a general GameModel/Adapter interface
for arbitrary future games (still no evidence for that).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class GameData:
    starting_gold: int
    shop_buy: Dict[str, int]
    shop_sell: Dict[str, int]
    recipes: Dict[str, Dict[str, int]]     # output -> {input: qty}
    dismantle: Dict[str, Dict[str, int]]   # item -> {output: qty}
    initial_inventory: Tuple[Tuple[str, int], ...] = ()
    # A finite, non-purchasable resource: give qty here and DON'T add the
    # item to shop_buy. Needed for H1 (scarcity/planning) and H3
    # (irrecoverable branching) -- neither is expressible without this.
    # Dev cases (E1-E5) all use the default () and are unaffected.


@dataclass(frozen=True)
class GameState:
    gold: int
    inventory: Tuple[Tuple[str, int], ...]  # sorted, qty > 0 only -> hashable

    def qty(self, item: str) -> int:
        for name, n in self.inventory:
            if name == item:
                return n
        return 0


def initial_state(data: GameData) -> GameState:
    inventory = tuple(sorted((k, v) for k, v in data.initial_inventory if v > 0))
    return GameState(gold=data.starting_gold, inventory=inventory)


@dataclass(frozen=True)
class Action:
    kind: str    # "buy" | "sell" | "craft" | "dismantle"
    target: str

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})"


def _with_inventory(state: GameState, deltas: Dict[str, int]) -> Tuple[Tuple[str, int], ...]:
    inv = dict(state.inventory)
    for item, delta in deltas.items():
        inv[item] = inv.get(item, 0) + delta
    return tuple(sorted((k, v) for k, v in inv.items() if v > 0))


def legal_actions(data: GameData, state: GameState) -> List[Action]:
    actions: List[Action] = []
    for item, price in data.shop_buy.items():
        if state.gold >= price:
            actions.append(Action("buy", item))
    for item in data.shop_sell:
        if state.qty(item) > 0:
            actions.append(Action("sell", item))
    for output, inputs in data.recipes.items():
        if all(state.qty(i) >= n for i, n in inputs.items()):
            actions.append(Action("craft", output))
    for item in data.dismantle:
        if state.qty(item) > 0:
            actions.append(Action("dismantle", item))
    return actions


def apply(data: GameData, state: GameState, action: Action) -> GameState:
    if action.kind == "buy":
        price = data.shop_buy[action.target]
        return GameState(state.gold - price, _with_inventory(state, {action.target: 1}))
    if action.kind == "sell":
        qty = state.qty(action.target)
        price = data.shop_sell[action.target]
        return GameState(state.gold + price * qty, _with_inventory(state, {action.target: -qty}))
    if action.kind == "craft":
        deltas = {i: -n for i, n in data.recipes[action.target].items()}
        deltas[action.target] = deltas.get(action.target, 0) + 1
        return GameState(state.gold, _with_inventory(state, deltas))
    if action.kind == "dismantle":
        deltas = {action.target: -1}
        for out_item, n in data.dismantle[action.target].items():
            deltas[out_item] = deltas.get(out_item, 0) + n
        return GameState(state.gold, _with_inventory(state, deltas))
    raise ValueError(f"unknown action kind: {action.kind}")
