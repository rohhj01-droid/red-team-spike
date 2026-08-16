"""Commit B self-check: exhaustively verify each dev case before it's
sealed as the calibration suite.

For every case:

  1. The declared MINIMAL_PATH is legal and realizes exactly the claimed
     profit (via oracle.py -- the ground-truth check, not any heuristic).
  2. No state in the FULL environment becomes profitable at a depth
     SHORTER than the declared minimal path (would mean it isn't actually
     minimal, or there's an unintended shortcut).
  3. Structural disjointness: no recipe or dismantle rule mixes a
     distractor item with a real-mechanism item, checked directly against
     the declared data -- distractor and real subsystems cannot combine
     via any transformation, by construction, not just by observation.
  4. A SEPARATE, dedicated breadth-first search restricted to ONLY
     distractor-item actions never reaches a profitable state. This is a
     distinct search from (2) -- the full-environment BFS in (2)
     deduplicates by state and keeps just the first path found to each
     one, so a distractor-only path that happens to land on a state also
     reachable via a mixed path could be shadowed and never actually
     checked. Restricting the action set up front avoids that entirely.

(3) and (4) together are what justify "distractors never pay off, alone
or in combination" -- (3) rules out combination via crafting, (4)
exhaustively rules out profit from distractor buy/sell/craft/dismantle
alone.

These environments are small enough (a handful of items, gold-bounded)
that exhaustive BFS with deduplication is fast and actually exhaustive
within the depth bound, not an approximation.

Run:
    python verify_cases.py
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from cases_dev import ALL_DEV_CASES, Case
from engine import Action, GameData, GameState, apply, initial_state, legal_actions
from oracle import is_exploit_found, realized_gold_gain

DEPTH_HEADROOM = 6  # search this many actions past the declared minimal path
DISTRACTOR_ONLY_DEPTH = 20  # generous -- distractor subsystems are small


def exhaustive_profitable_states(
    data: GameData, max_depth: int, allowed_targets: set = None
) -> List[Tuple[int, List[Action], int]]:
    """Full breadth-first enumeration of reachable states, deduplicated.
    If `allowed_targets` is given, only actions whose target is in that
    set are expanded -- used to run an isolated distractor-only search."""
    start = initial_state(data)
    frontier: Dict[GameState, List[Action]] = {start: []}
    visited = {start}
    found: List[Tuple[int, List[Action], int]] = []

    for depth in range(1, max_depth + 1):
        next_frontier: Dict[GameState, List[Action]] = {}
        for state, path in frontier.items():
            for action in legal_actions(data, state):
                if allowed_targets is not None and action.target not in allowed_targets:
                    continue
                new_state = apply(data, state, action)
                if new_state in visited:
                    continue
                visited.add(new_state)
                new_path = path + [action]
                if new_state.gold > data.starting_gold:
                    found.append((depth, new_path, new_state.gold - data.starting_gold))
                next_frontier[new_state] = new_path
        frontier = next_frontier
        if not frontier:
            break
    return found


def check_structural_disjointness(case: Case) -> bool:
    distractors = set(case.distractor_items)
    for output, inputs in case.data.recipes.items():
        items = set(inputs) | {output}
        if items & distractors and items - distractors:
            return False
    for target, outputs in case.data.dismantle.items():
        items = set(outputs) | {target}
        if items & distractors and items - distractors:
            return False
    return True


def verify_case(case: Case) -> bool:
    print(f"--- {case.name}: {case.mechanism}")
    ok = True

    expected_gain = realized_gold_gain(case.data, case.minimal_path)
    if not is_exploit_found(case.data, case.minimal_path):
        print(f"  FAIL: declared minimal_path does not realize profit (gain={expected_gain})")
        ok = False
    else:
        print(f"  minimal_path OK: {len(case.minimal_path)} actions, +{expected_gain} gold")

    max_depth = len(case.minimal_path) + DEPTH_HEADROOM
    profitable = exhaustive_profitable_states(case.data, max_depth)

    if not profitable:
        print(f"  FAIL: exhaustive search up to depth {max_depth} found no profitable state at all")
        ok = False
        return ok

    first_depth = profitable[0][0]
    if first_depth < len(case.minimal_path):
        print(
            f"  FAIL: a shorter profitable path exists at depth {first_depth} "
            f"(declared minimal_path is {len(case.minimal_path)} actions) -- "
            f"path: {profitable[0][1]}"
        )
        ok = False
    else:
        print(f"  no shortcut: nothing profitable before depth {len(case.minimal_path)}")

    if not check_structural_disjointness(case):
        print("  FAIL: a recipe or dismantle rule mixes distractor and real items")
        ok = False
    else:
        print("  structural disjointness OK: no rule combines distractor and real items")

    distractor_only_profitable = exhaustive_profitable_states(
        case.data, DISTRACTOR_ONLY_DEPTH, allowed_targets=set(case.distractor_items)
    )
    if distractor_only_profitable:
        print(f"  FAIL: distractor-only search found profit (should be impossible):")
        for depth, path, gain in distractor_only_profitable:
            print(f"    depth={depth} gain={gain} path={path}")
        ok = False
    else:
        print(
            f"  distractor-only search OK: no profitable state up to depth "
            f"{DISTRACTOR_ONLY_DEPTH} using only distractor actions"
        )

    action_types = len(case.data.shop_buy) + len(case.data.shop_sell) + len(case.data.recipes) + len(case.data.dismantle)
    print(f"  nominal action types: {action_types}, minimal exploit depth: {len(case.minimal_path)}")
    return ok


if __name__ == "__main__":
    results = [verify_case(c) for c in ALL_DEV_CASES]
    print()
    print("DEV SUITE VERIFICATION: " + ("PASS -- all 5 cases sealed clean" if all(results) else "FAIL -- see above"))
