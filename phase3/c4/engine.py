"""C4's buggy world engine. Sealed per DESIGN_C4.md -- claim()'s
precondition-check is byte-for-byte unchanged from C2c; the only new
effect is reward_owned=True, which fires unconditionally after that
check, so it cannot influence classify_claim's inputs. No "correct
claim" implementation exists here or anywhere else, same rule as C1-C3.

Independent of phase3/c2/*.py and phase3/c3/*.py -- both are sealed
evidence, C4 duplicates the small shared shapes rather than import them.
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
    reward_owned: bool


def initial_world() -> WorldState:
    return WorldState(equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False, reward_owned=False)


@dataclass(frozen=True)
class Action:
    kind: str          # "equip" | "accept" | "channel" | "claim" | "consume"
    target: str = ""    # equipment name, only for "equip"

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})" if self.target else self.kind


def legal_actions(world: WorldState) -> List[Action]:
    actions: List[Action] = []
    for item in EQUIPMENT_CATALOG:
        if item != world.equipped:  # no-op equip is illegal, unchanged from C1-C3
            actions.append(Action("equip", item))
    if world.quest_status == "NOT_ACCEPTED" and world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("accept"))
    if world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("channel"))  # no no-op ban, unchanged from C2
    if world.quest_status == "ACTIVE" and world.equipped == REQUIRED_EQUIPMENT and world.has_flame_buff:
        actions.append(Action("claim"))
    if world.reward_owned:
        actions.append(Action("consume"))
    return actions


def apply(world: WorldState, action: Action) -> WorldState:
    if action.kind == "equip":
        return WorldState(equipped=action.target, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, reward_owned=world.reward_owned)
    if action.kind == "accept":
        return WorldState(equipped=world.equipped, quest_status="ACTIVE",
                           has_flame_buff=world.has_flame_buff, reward_owned=world.reward_owned)
    if action.kind == "channel":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=True, reward_owned=world.reward_owned)
    if action.kind == "claim":
        return WorldState(equipped=world.equipped, quest_status="CLAIMED",
                           has_flame_buff=world.has_flame_buff, reward_owned=True)
    if action.kind == "consume":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, reward_owned=False)
    raise ValueError(f"unknown action kind: {action.kind}")
