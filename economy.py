"""Phase 0 spike simulator: economy + crafting only.

Throwaway by design (see Spike Contract) — no adapters, no config, no plugin
system. Five exploits (E1-E5) are hardcoded into the game data below and are
sealed: do not add/change/remove one after seeing search results.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

STARTING_GOLD = 300

# item -> buy price at the shop
SHOP_BUY: Dict[str, int] = {
    "Trinket": 50,   # E1: priced wrong, sells for more than it costs
    "Wood": 5,
    "Stone": 5,
    "Iron": 10,
    "Copper": 8,
    "Potion": 10,
}

# item -> sell price at the shop
SHOP_SELL: Dict[str, int] = {
    "Trinket": 65,   # E1
    "Plank": 40,     # E2
    "Iron": 10,      # E3 (sell the duplicated iron)
    "Coal": 20,      # E4
    "Bundle": 90,    # E5
}

# craft: output item -> {input item: qty consumed}
RECIPES: Dict[str, Dict[str, int]] = {
    "Plank": {"Wood": 1, "Stone": 1},   # E2: craft margin
    "Blade": {"Iron": 1},               # E3
    "Gear": {"Copper": 2},              # E4
    "Bundle": {"Herb": 5},              # E5: needs 5 accumulated Herb
}

# dismantle: item -> {output item: qty}. Deliberately NOT the inverse of
# RECIPES above -- that mismatch is the bug in E3/E4. Potion has no recipe;
# dismantling it is the only source of Herb (no shop entry for Herb).
DISMANTLE: Dict[str, Dict[str, int]] = {
    "Blade": {"Iron": 3},    # E3 bug: crafted from 1 Iron, returns 3
    "Gear": {"Coal": 1},     # E4 bug: Copper turns into sellable Coal
    "Potion": {"Herb": 1},   # E5
}

# item -> which sealed exploit it belongs to (families are disjoint by design)
FAMILY: Dict[str, str] = {
    "Trinket": "E1",
    "Wood": "E2", "Stone": "E2", "Plank": "E2",
    "Iron": "E3", "Blade": "E3",
    "Copper": "E4", "Gear": "E4", "Coal": "E4",
    "Potion": "E5", "Herb": "E5", "Bundle": "E5",
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


def discovered_exploits(path: List[Action]) -> set:
    """Which sealed exploit families does this path *causally* realize?

    Not "which families were merely touched" -- a path can buy a Potion out
    of idle curiosity while its actual profit came entirely from Trinket
    flipping, and that must NOT count as finding the Potion/Herb/Bundle
    exploit. This isolates each family's own actions (in their original
    relative order), replays them ALONE from a fresh initial_state, and
    credits the family only if that isolated replay is itself profitable.
    """
    result = set()
    families_present = {FAMILY[a.target] for a in path if a.target in FAMILY}
    for fam in families_present:
        sub_path = [a for a in path if FAMILY.get(a.target) == fam]
        state = initial_state()
        for action in sub_path:
            if action not in legal_actions(state):
                continue
            state = apply(state, action)
        if state.gold > STARTING_GOLD:
            result.add(fam)
    return result
