"""C3's buggy world engine. Sealed per DESIGN_C3.md -- claim() is
byte-for-byte unchanged from C2c; channel()'s legality is WorldState-only
and never depends on enchant_broken (see DESIGN_C3.md's "channel() is
legal-but-potentially-unqualified" section). No "correct claim"
implementation exists here or anywhere else, same rule as C1/C2.

Independent of phase3/c2/*.py -- C2 is sealed evidence, so C3 duplicates
the small catalog/action shapes rather than import them.
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
    enchanted: bool


def initial_world() -> WorldState:
    return WorldState(equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False, enchanted=False)


@dataclass(frozen=True)
class Action:
    kind: str          # "equip" | "accept" | "enchant" | "unenchant" | "channel" | "claim"
    target: str = ""    # equipment name, only for "equip"

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})" if self.target else self.kind


def legal_actions(world: WorldState) -> List[Action]:
    actions: List[Action] = []
    for item in EQUIPMENT_CATALOG:
        if item != world.equipped:  # no-op equip is illegal, unchanged from C1/C2
            actions.append(Action("equip", item))
    if world.quest_status == "NOT_ACCEPTED" and world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("accept"))
    if not world.enchanted:  # no-op enchant is illegal
        actions.append(Action("enchant"))
    if world.enchanted:
        actions.append(Action("unenchant"))
    if world.equipped == REQUIRED_EQUIPMENT and world.enchanted:
        # NO no-op ban -- unchanged reasoning from DESIGN_C2.md, see
        # DESIGN_C3.md's "channel() is legal-but-potentially-unqualified".
        actions.append(Action("channel"))
    if world.quest_status == "ACTIVE" and world.equipped == REQUIRED_EQUIPMENT and world.has_flame_buff:
        # BUGGY: only checks current equipment and current buff presence,
        # not continuity/source-lifecycle/provenance history.
        actions.append(Action("claim"))
    return actions


def apply(world: WorldState, action: Action) -> WorldState:
    if action.kind == "equip":
        return WorldState(equipped=action.target, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, enchanted=world.enchanted)
    if action.kind == "accept":
        return WorldState(equipped=world.equipped, quest_status="ACTIVE",
                           has_flame_buff=world.has_flame_buff, enchanted=world.enchanted)
    if action.kind == "enchant":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, enchanted=True)
    if action.kind == "unenchant":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, enchanted=False)
    if action.kind == "channel":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=True, enchanted=world.enchanted)
    if action.kind == "claim":
        return WorldState(equipped=world.equipped, quest_status="CLAIMED",
                           has_flame_buff=world.has_flame_buff, enchanted=world.enchanted)
    raise ValueError(f"unknown action kind: {action.kind}")
