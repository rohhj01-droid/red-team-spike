"""Independent property monitor. NOT part of the engine -- the buggy
game's claim() never reads this, anywhere. See DESIGN_C1.md's visibility
rules: ranking/guidance (score, descriptor, UCT) may never read this
either; only dedup identity and reward/oracle checks may.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, REQUIRED_EQUIPMENT, WorldState


@dataclass(frozen=True)
class MonitorState:
    continuity_broken: bool


def initial_monitor() -> MonitorState:
    return MonitorState(continuity_broken=False)


def monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        broken = True
    return MonitorState(continuity_broken=broken)
