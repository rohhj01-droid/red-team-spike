"""Independent property monitor. NOT part of the engine -- claim() never
reads this. Same visibility rules as C1/C2: ranking/guidance (score,
descriptor, UCT) may never read this; only dedup identity and
reward/oracle checks may.

The known-bad negative-control variant lives in verify_c3.py, not here,
same reasoning as C2.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, REQUIRED_EQUIPMENT, WorldState


@dataclass(frozen=True)
class MonitorState:
    continuity_broken: bool
    enchant_broken: bool
    buff_source_broken: bool


def initial_monitor() -> MonitorState:
    return MonitorState(continuity_broken=False, enchant_broken=False, buff_source_broken=False)


def monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    enchant_broken = prev_monitor.enchant_broken
    if prev_world.enchanted and not new_world.enchanted:
        enchant_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = prev_monitor.enchant_broken   # grant-time capture
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken,
                         enchant_broken=enchant_broken,
                         buff_source_broken=buff_source_broken)
