"""Ground-truth exploit success predicate.

HARD RULE (sealed by Commit B review): this file must never import or
reference any search algorithm's value estimate (Beam's `score()`/`VALUE`
in phase0/phase1, or whatever a future MCTS/Beam module in Phase 2 uses
for its own guidance). Phase 0's `estimate_values()` bug corrupted the
search AND would have corrupted grading too if the two had shared a value
function -- an exploit "found" by a broken heuristic and graded by that
same broken heuristic can never catch its own error. Oracle and search
heuristic must be able to disagree; that's what makes the oracle a check
on the heuristic instead of an echo of it.

Exploit success = REALIZED gold only. Holding valuable-looking inventory
does not count -- the path must actually reach a state with more gold in
hand than the case started with. If a future held-out case needs
inventory to count as profit (e.g. an item that's obviously convertible
but the path doesn't bother selling it), that requires a new,
benchmark-declared ground-truth liquidation rule written here explicitly
-- never a shortcut through a search module's derived value estimate.

PRECONDITION this file assumes but does not check: `is_profitable_state`
compares final gold to `data.starting_gold` alone, with no accounting for
any value the case may have started with in `data.initial_inventory`
(introduced for H1/H3's finite resources). That comparison is only
correct if the starting resource has no legitimate way to become gold
outside the case's intended mechanism -- otherwise "sell what you already
had" would register as a false-positive exploit. Enforcing that is a
benchmark-authoring discipline (cases_heldout.py H1's condition), not
something this file can verify on its own.
"""
from __future__ import annotations

from typing import List

from engine import Action, GameData, GameState, apply, initial_state, legal_actions


def is_profitable_state(data: GameData, state: GameState) -> bool:
    """The one canonical definition of 'profitable' -- used both here
    (replay-based, for grading a completed trace) and by search algorithms
    doing a fast online check as they go. Keeping this in one place is
    exactly the insurance Phase 0 needed twice already: two independent
    definitions of the same condition drifting apart is how a false
    positive/negative gets in."""
    return state.gold > data.starting_gold


def is_exploit_found(data: GameData, path: List[Action]) -> bool:
    """A single illegal action anywhere in `path` invalidates the WHOLE
    trace -- not skip-and-continue. Phase 0's family-isolated replay had a
    reason to skip (the sub-path was deliberately extracted out of its
    original context); Phase 2 replays a complete claimed trace exactly as
    given, so an illegal step means the claim itself is invalid. Silently
    dropping it and crediting whatever legal actions remained would let a
    garbled trace still get counted as a real find."""
    state = initial_state(data)
    for action in path:
        if action not in legal_actions(data, state):
            return False
        state = apply(data, state, action)
    return is_profitable_state(data, state)


def realized_gold_gain(data: GameData, path: List[Action]) -> int:
    """Benchmark-authoring/debugging helper, not part of grading. Raises
    on an illegal action instead of skipping it -- this function exists to
    catch wiring mistakes in a case's declared minimal_path, and a silent
    skip would hide exactly the bug it's meant to surface."""
    state = initial_state(data)
    for action in path:
        if action not in legal_actions(data, state):
            raise ValueError(f"illegal action {action} at state {state}")
        state = apply(data, state, action)
    return state.gold - data.starting_gold
