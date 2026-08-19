"""QA-only independent reference specification. Never imported by
engine.py, monitor.py, or oracle.py -- exists only so verify_c2.py can
check monitor_step() against a completely separately written computation
of each fact. Same discipline as phase3/qa_reference.py (C1): a full
linear scan of the history each call, no persisted running bit threaded
between calls, unlike monitor_step's incremental fold.
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


def reference_buff_source_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        world = apply(world, action)
        if action.kind == "channel":
            broken = False
        elif world.has_flame_buff and world.equipped != REQUIRED_EQUIPMENT:
            broken = True
    return broken
