"""Held-out suite: CATEGORY DEFINITIONS ONLY. No concrete GameData exists
here, on purpose -- see CONTRACT.md Commit sequence, step D.5. Exact item
names, prices, recipes and stock caps are authored only after algorithm
implementation (Commit C) and calibration (Commit D) are frozen.

Do not add a `data` field to these, do not import `engine.GameData` here,
and do not write concrete numbers "just as a placeholder" -- a placeholder
that happens to compile is still information an implementer can see.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HeldOutCategory:
    name: str
    condition: str
    targets_rq: str


H1 = HeldOutCategory(
    name="H1",
    condition=(
        "Resource bottleneck: a profitable action is available only a "
        "limited number of times (capped stock or a one-time source), "
        "forcing planning around scarcity instead of an infinitely "
        "repeatable cycle."
    ),
    targets_rq="RQ1 (supporting observation only; does not drive RQ3)",
)

H2 = HeldOutCategory(
    name="H2",
    condition=(
        "Genuinely lossy intermediate step: a step that reduces REALIZED "
        "value at the moment it's taken (not just looks flat under some "
        "heuristic) and only pays off through a later, separate "
        "combination. No cushion of the kind E5's Herb (which had "
        "derived heuristic value) provided."
    ),
    targets_rq="RQ3 (sole verdict-driving case, per CONTRACT.md)",
)

H3 = HeldOutCategory(
    name="H3",
    condition=(
        "Branching recipe choice: a shared input is consumable by two or "
        "more recipes, only one of which leads anywhere profitable, and "
        "the wrong choice burns the resource with no easy recovery."
    ),
    targets_rq="RQ1 (supporting observation only; does not drive RQ3)",
)

ALL_HELDOUT_CATEGORIES = [H1, H2, H3]
