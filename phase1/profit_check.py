"""Synthetic-Economy-specific profit detector for E1-E5.

Deliberately NOT named `oracle.py` or `exploit_detector.py`. What this does
-- isolate a sealed exploit's own actions by item-family membership, replay
them alone from a fresh initial_state, and check if that isolated replay is
profitable -- only works because E1-E5 use disjoint item sets. A genuine
cross-system exploit (e.g. Quest x Equipment x Buff) is NOT isolable this
way: pulling the Quest actions out to test Equipment "alone" removes the
very interaction that causes the bug. Do not import this into anything
that claims to be a general exploit detector. See red-team-spike/README.md.
"""
from __future__ import annotations

from typing import Dict, List, Set

from model import Action, STARTING_GOLD, apply, initial_state, legal_actions

# item -> which sealed exploit it belongs to (families are disjoint by design
# for E1-E5; this is a Phase 0 benchmark answer key, not a general concept)
FAMILY: Dict[str, str] = {
    "Trinket": "E1",
    "Wood": "E2", "Stone": "E2", "Plank": "E2",
    "Iron": "E3", "Blade": "E3",
    "Copper": "E4", "Gear": "E4", "Coal": "E4",
    "Potion": "E5", "Herb": "E5", "Bundle": "E5",
}


def discovered_exploits(path: List[Action]) -> Set[str]:
    result: Set[str] = set()
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


def is_profit(state, start_gold: int = STARTING_GOLD) -> bool:
    return state.gold > start_gold
