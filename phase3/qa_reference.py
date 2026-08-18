"""QA-only independent reference specification. Never imported by
engine.py, monitor.py, oracle.py, or (later) search.py -- exists only so
verify_c1.py can check monitor_step() against a completely separately
written computation of the same fact. A bug shared between monitor_step
and this file would have to be a mistake in the natural-language spec
itself, not an implementation slip in either one, which is the strongest
independence two implementations of the same property can realistically
have.

This computes the fact by a full linear scan of the history each call --
no persisted running bit threaded between calls, unlike monitor_step's
incremental fold.
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
