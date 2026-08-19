"""Runtime oracle. Transition-based, not state-based (C2c correction):
exploit status is a judgment about whether a specific `claim` event was
legitimate, evaluated using the qualification facts as of immediately
before that claim -- not a predicate re-derived from whatever the
current world/monitor happen to be. quest_status latches at CLAIMED
forever, but buff_source_broken keeps tracking honestly after claim (it
describes present buff validity, not claim legitimacy), so a state-based
predicate queried after further actions could misjudge an
already-settled claim. See DESIGN_C2.md's C2c correction.
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
