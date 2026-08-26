"""Independent property monitor. NOT part of the engine -- claim() never
reads this. Byte-for-byte C2c, unchanged for C4 -- no Enchantment chain.
Same visibility rules as C1-C3: ranking/guidance (score, descriptor,
UCT) may never read this; only dedup identity and reward/oracle checks
may.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, REQUIRED_EQUIPMENT, WorldState


@dataclass(frozen=True)
class MonitorState:
    continuity_broken: bool
    buff_source_broken: bool


def initial_monitor() -> MonitorState:
    return MonitorState(continuity_broken=False, buff_source_broken=False)


def monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = False
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, buff_source_broken=buff_source_broken)
