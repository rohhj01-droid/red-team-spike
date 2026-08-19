"""C2's buggy world engine. Sealed per DESIGN_C2.md -- claim() treats
presence as a proxy for validity for both conditions it checks; no
"correct claim" implementation exists here or anywhere else, same rule
as C1.

Independent of phase3/engine.py (C1) by design -- C1 is sealed evidence;
duplicating the small catalog/action shapes here keeps C2 from coupling
to a file that must never change again.
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
    has_flame_buff: bool


def initial_world() -> WorldState:
    return WorldState(equipped="WoodenSword", quest_status="NOT_ACCEPTED", has_flame_buff=False)


@dataclass(frozen=True)
class Action:
    kind: str          # "equip" | "accept" | "channel" | "claim"
    target: str = ""    # equipment name, only for "equip"

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})" if self.target else self.kind


def legal_actions(world: WorldState) -> List[Action]:
    actions: List[Action] = []
    for item in EQUIPMENT_CATALOG:
        if item != world.equipped:  # no-op equip is illegal, unchanged from C1
            actions.append(Action("equip", item))
    if world.quest_status == "NOT_ACCEPTED" and world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("accept"))
    if world.equipped == REQUIRED_EQUIPMENT:
        # NO no-op ban here, unlike equip -- see DESIGN_C2.md "WorldState
        # no-op can be a MonitorState non-no-op". legal_actions() stays
        # WorldState-only, so it cannot tell a revalidating channel() from
        # a genuinely inert one.
        actions.append(Action("channel"))
    if world.quest_status == "ACTIVE" and world.equipped == REQUIRED_EQUIPMENT and world.has_flame_buff:
        # BUGGY: only checks current equipment and current buff presence,
        # not continuity/source-lifecycle history.
        actions.append(Action("claim"))
    return actions


def apply(world: WorldState, action: Action) -> WorldState:
    if action.kind == "equip":
        return WorldState(equipped=action.target, quest_status=world.quest_status, has_flame_buff=world.has_flame_buff)
    if action.kind == "accept":
        return WorldState(equipped=world.equipped, quest_status="ACTIVE", has_flame_buff=world.has_flame_buff)
    if action.kind == "channel":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status, has_flame_buff=True)
    if action.kind == "claim":
        return WorldState(equipped=world.equipped, quest_status="CLAIMED", has_flame_buff=world.has_flame_buff)
    raise ValueError(f"unknown action kind: {action.kind}")
