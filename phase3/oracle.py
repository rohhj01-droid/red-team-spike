"""Runtime oracle. Ground truth = the invariant itself, not a currency
signal -- unlike Phase 0-2, C1 has no gold/economy to check.
"""
from __future__ import annotations

from monitor import MonitorState
from engine import WorldState


def is_exploit(world: WorldState, monitor: MonitorState) -> bool:
    return world.quest_status == "CLAIMED" and monitor.continuity_broken
