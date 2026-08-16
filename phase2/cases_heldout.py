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
        "limited number of times (capped stock or a one-time source, via "
        "`GameData.initial_inventory`), forcing planning around scarcity "
        "instead of an infinitely repeatable cycle. "
        "ORACLE-VALIDITY CONSTRAINT (sealed before D.5, not optional): "
        "oracle.py defines profit as `final gold > starting_gold` alone -- "
        "it says nothing about inventory value, because dev (E1-E5) never "
        "starts with any. The moment `initial_inventory` is non-empty, "
        "that definition only stays correct if the starting resource has "
        "NO legitimate sell/liquidation path outside the planted "
        "exploit -- no shop_sell entry for it, and no recipe/dismantle "
        "chain that turns it into anything sellable except through the "
        "one intended mechanism. Otherwise D.5 accidentally plants a "
        "trivial 'just sell what you started with' false positive, not "
        "H1's actual mechanism. This must be true by construction, not "
        "just checked after the fact -- design H1 so there is nothing "
        "else the extra resource could ever legitimately become."
    ),
    targets_rq="RQ1 (supporting observation only; does not drive RQ3)",
)

H2 = HeldOutCategory(
    name="H2",
    condition=(
        "Genuinely lossy intermediate step -- OPERATIONAL DEFINITION, "
        "sealed before Commit C: along the ONLY path from the initial "
        "state to H2's payoff, there is at least one state the design "
        "requires passing through where Beam-Diverse's frozen score() "
        "(as it exists after Commit D's calibration -- gold plus "
        "estimated inventory value, not raw gold alone) is STRICTLY LESS "
        "than score(initial_state). Not just gold dipping (buying always "
        "dips gold, that alone would make E1 count) -- the *heuristic's "
        "own estimate* has to dip and stay below baseline until the final "
        "combination. This is what distinguishes H2 from E5: E5's Herb "
        "had positive derived value under the Phase 0/1 value heuristic, "
        "so score() never actually dropped below baseline during "
        "accumulation, only raw gold did. Constructing this is D.5's job "
        "(e.g. a payoff recipe with 2+ required intermediates, since the "
        "single-input-only value propagation rule fixed in Phase 0 "
        "assigns no derived value to any item that's part of a "
        "multi-input recipe) -- exact numbers stay undecided until then, "
        "but the condition itself is locked now."
    ),
    targets_rq="RQ3 (sole verdict-driving case, per CONTRACT.md)",
)

H3 = HeldOutCategory(
    name="H3",
    condition=(
        "Branching recipe choice: a shared input (plausibly via "
        "`GameData.initial_inventory`, finite) is consumable by two or "
        "more recipes, only one of which leads anywhere profitable, and "
        "the wrong choice burns the resource with no easy recovery. "
        "SAME ORACLE-VALIDITY CONSTRAINT AS H1 applies if H3 uses "
        "initial_inventory: the shared resource must have no legitimate "
        "sell/liquidation path outside the intended (correct-branch) "
        "mechanism -- see H1's condition for why."
    ),
    targets_rq="RQ1 (supporting observation only; does not drive RQ3)",
)

ALL_HELDOUT_CATEGORIES = [H1, H2, H3]
