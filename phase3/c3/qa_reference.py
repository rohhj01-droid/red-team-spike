"""QA-only independent reference specification. Never imported by
engine.py, monitor.py, or oracle.py -- exists only so verify_c3.py can
check monitor_step() against a completely separately written computation
of each fact.

reference_buff_source_broken does not call reference_enchant_broken as a
subroutine (would reintroduce a shared-implementation risk between the
two independence checks) and does not mirror monitor_step's single-pass
incremental fold (would just be the same computation restated) -- it
locates the last channel by a plain scan, then checks the two sides of
it via separate replays. See DESIGN_C3.md's Step 1c for the derivation.
"""
from __future__ import annotations

from typing import List

from engine import Action, REQUIRED_EQUIPMENT, apply, initial_world


def reference_continuity_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        world = apply(world, action)
        if world.quest_status == "ACTIVE" and world.equipped != REQUIRED_EQUIPMENT:
            broken = True
    return broken


def reference_enchant_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        prev_enchanted = world.enchanted
        world = apply(world, action)
        if prev_enchanted and not world.enchanted:
            broken = True
    return broken


def reference_buff_source_broken(history: List[Action]) -> bool:
    last_channel_index = None
    for i, action in enumerate(history):
        if action.kind == "channel":
            last_channel_index = i
    if last_channel_index is None:
        return False

    world = initial_world()
    tainted_at_grant = False
    for action in history[:last_channel_index]:
        prev_enchanted = world.enchanted
        world = apply(world, action)
        if prev_enchanted and not world.enchanted:
            tainted_at_grant = True

    world = initial_world()
    for action in history[:last_channel_index + 1]:
        world = apply(world, action)
    broken_after_grant = False
    for action in history[last_channel_index + 1:]:
        world = apply(world, action)
        if world.equipped != REQUIRED_EQUIPMENT:
            broken_after_grant = True

    return tainted_at_grant or broken_after_grant
