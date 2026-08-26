"""QA-only independent reference specification. Never imported by
engine.py, monitor.py, event_provenance.py, or oracle.py.

reference_continuity_broken/reference_buff_source_broken are C2c's
exact functions (C4's base, unchanged). reference_reward_provenance_
tainted, reference_classify_claim, and reference_classify_consume are
new -- DESIGN_C4.md's QA section: C4 is the first case where the oracle
itself, not just the monitor fold beneath it, needs an independent
reference. None of the three call event_provenance_step, classify_claim,
or classify_consume -- all re-derive directly from the reference
property functions on a raw action history.
"""
from __future__ import annotations

from typing import List, Optional

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


def reference_reward_provenance_tainted(history: List[Action]) -> bool:
    claim_index = None
    for i, action in enumerate(history):
        if action.kind == "claim":
            claim_index = i
            break   # claim fires at most once
    if claim_index is None:
        return False
    prefix = history[:claim_index]
    return reference_continuity_broken(prefix) or reference_buff_source_broken(prefix)


def reference_classify_claim(history_before: List[Action], action: Action) -> Optional[str]:
    if action.kind != "claim":
        return None
    eq = reference_continuity_broken(history_before)
    buf = reference_buff_source_broken(history_before)
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None


def reference_classify_consume(history_before: List[Action], action: Action) -> Optional[str]:
    if action.kind != "consume":
        return None
    if reference_reward_provenance_tainted(history_before):
        return "TAINTED_REWARD_CONSUMPTION"
    return None
