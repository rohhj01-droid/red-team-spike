"""Runtime oracle. classify_claim is byte-for-byte C2c, unchanged.
classify_consume is new -- C4's actual search-target oracle. See
DESIGN_C4.md's "Search target discovery is consume-only": classify_claim's
verdict is real and recorded (via EventProvenanceState) but must never
trigger a Discovery on its own, so is_exploit is built on
classify_consume only.
"""
from __future__ import annotations

from typing import Optional

from engine import Action
from event_provenance import EventProvenanceState
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


def classify_consume(action: Action, prev_provenance: EventProvenanceState) -> Optional[str]:
    if action.kind != "consume":
        return None
    if prev_provenance.reward_provenance_tainted:
        return "TAINTED_REWARD_CONSUMPTION"
    return None


def is_exploit(action: Action, prev_provenance: EventProvenanceState) -> bool:
    """C4's search-target wrapper -- built on classify_consume only.
    classify_claim's verdict does not go through this function; it is
    not a search-terminal discovery (DESIGN_C4.md)."""
    return classify_consume(action, prev_provenance) is not None
