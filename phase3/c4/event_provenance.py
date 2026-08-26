"""Independent event-provenance tracker -- C4's third persistent state
bucket, distinct from MonitorState by design. See DESIGN_C4.md's
"EventProvenanceState -- a distinct boundary" section: folding this
into MonitorState would force monitor.py to import oracle.py
(circular) or duplicate classify_claim's OR-logic. event_provenance_step
takes claim_verdict as an already-computed plain value -- it never
calls classify_claim itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from engine import Action


@dataclass(frozen=True)
class EventProvenanceState:
    reward_provenance_tainted: bool


def initial_event_provenance() -> EventProvenanceState:
    return EventProvenanceState(reward_provenance_tainted=False)


def event_provenance_step(action: Action, claim_verdict: Optional[str], prev_provenance: EventProvenanceState) -> EventProvenanceState:
    tainted = prev_provenance.reward_provenance_tainted
    if action.kind == "claim":
        tainted = claim_verdict is not None
    return EventProvenanceState(reward_provenance_tainted=tainted)
