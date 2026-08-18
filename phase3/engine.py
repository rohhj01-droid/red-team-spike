"""C1's buggy world engine. Sealed per DESIGN_C1.md -- no "correct claim"
implementation exists here or anywhere else; that rule exists only as
prose in the design doc justifying what oracle.py checks.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

EQUIPMENT_CATALOG = frozenset({"FlameSword", "WoodenSword"})
REQUIRED_EQUIPMENT = "FlameSword"


@dataclass(frozen=True)
class WorldState:
    equipped: str
    quest_status: str  # "NOT_ACCEPTED" | "ACTIVE" | "CLAIMED"


def initial_world() -> WorldState:
    return WorldState(equipped="WoodenSword", quest_status="NOT_ACCEPTED")


@dataclass(frozen=True)
class Action:
    kind: str          # "equip" | "accept" | "claim"
    target: str = ""    # equipment name, only for "equip"

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})" if self.target else self.kind


def legal_actions(world: WorldState) -> List[Action]:
    actions: List[Action] = []
    for item in EQUIPMENT_CATALOG:
        if item != world.equipped:  # no-op equip is illegal, sealed in DESIGN_C1.md
            actions.append(Action("equip", item))
    if world.quest_status == "NOT_ACCEPTED" and world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("accept"))
    if world.quest_status == "ACTIVE" and world.equipped == REQUIRED_EQUIPMENT:
        # BUGGY: only checks current equipment, not continuity history.
        actions.append(Action("claim"))
    return actions


def apply(world: WorldState, action: Action) -> WorldState:
    if action.kind == "equip":
        return WorldState(equipped=action.target, quest_status=world.quest_status)
    if action.kind == "accept":
        return WorldState(equipped=world.equipped, quest_status="ACTIVE")
    if action.kind == "claim":
        return WorldState(equipped=world.equipped, quest_status="CLAIMED")
    raise ValueError(f"unknown action kind: {action.kind}")
