"""Runtime oracle. Unchanged from C2c -- transition-based, OR-based,
three-way. enchant_broken is never read here directly; it only reaches
claim()'s judgment by way of having already been captured into
buff_source_broken at some earlier channel(). See DESIGN_C3.md's
"Oracle -- unchanged from C2c" section.
"""
from __future__ import annotations

from typing import Optional

from engine import Action
from monitor import MonitorState


def classify_claim(action: Action, prev_monitor: MonitorState) -> Optional[str]:
    if action.kind != "claim":
        return None
    eq = prev_monitor.continuity_broken
    buf = prev_monitor.buff_source_broken
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None  # legitimate completion, not an exploit


def is_exploit(action: Action, prev_monitor: MonitorState) -> bool:
    return classify_claim(action, prev_monitor) is not None
