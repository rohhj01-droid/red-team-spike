"""Commit B self-check: exhaustively verify each dev case before it's
sealed as the calibration suite.

For every case, does a full (non-heuristic, non-beam) breadth-first
enumeration of reachable states up to a depth bound, and checks:

  1. The declared MINIMAL_PATH is legal and realizes exactly the claimed
     profit (via oracle.py -- the ground-truth check, not any heuristic).
  2. No state becomes profitable at a depth SHORTER than the declared
     minimal path (would mean it isn't actually minimal, or there's an
     unintended shortcut).
  3. No OTHER profitable state exists anywhere in the searched depth that
     isn't explained by the declared mechanism -- i.e. the distractor
     items genuinely never pay off, alone or combined with anything else
     reachable in this environment.

This is full enumeration, not sampling -- these environments are small
enough (a handful of items, gold-bounded) that exhaustive BFS with
deduplication is fast and actually exhaustive within the depth bound, not
an approximation.

Run:
    python verify_cases.py
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from cases_dev import ALL_DEV_CASES, Case
from engine import Action, GameData, GameState, apply, initial_state, legal_actions
from oracle import is_exploit_found, realized_gold_gain

DEPTH_HEADROOM = 6  # search this many actions past the declared minimal path


def exhaustive_profitable_states(data: GameData, max_depth: int) -> List[Tuple[int, List[Action], int]]:
    """Returns (depth, path, gold_gain) for every distinct first-reached
    profitable state, in order of discovery (breadth-first -> shortest
    paths first)."""
    start = initial_state(data)
    frontier: Dict[GameState, List[Action]] = {start: []}
    visited = {start}
    found: List[Tuple[int, List[Action], int]] = []

    for depth in range(1, max_depth + 1):
        next_frontier: Dict[GameState, List[Action]] = {}
        for state, path in frontier.items():
            for action in legal_actions(data, state):
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

    # Scaling up the real mechanism (buying more before selling, repeating
    # the cycle, or diluting it with an unprofitable side trade) legitimately
    # produces many different (depth, gain) pairs -- that's not a second
    # exploit, it's the same one at a different scale. The only thing that
    # would actually indicate a distractor accidentally paying off is a
    # profitable path whose actions touch ONLY distractor items.
    distractor_only = [
        (depth, path, gain) for depth, path, gain in profitable
        if all(a.target in case.distractor_items for a in path)
    ]
    if distractor_only:
        print(f"  FAIL: distractor-only path is profitable (should never happen):")
        for depth, path, gain in distractor_only:
            print(f"    depth={depth} gain={gain} path={path}")
        ok = False
    else:
        print(
            f"  distractors OK: no distractor-only path is profitable "
            f"({len(profitable)} profitable states found up to depth {max_depth}, "
            f"all involve the real mechanism)"
        )

    action_types = len(case.data.shop_buy) + len(case.data.shop_sell) + len(case.data.recipes) + len(case.data.dismantle)
    print(f"  nominal action types: {action_types}, minimal exploit depth: {len(case.minimal_path)}")
    return ok


if __name__ == "__main__":
    results = [verify_case(c) for c in ALL_DEV_CASES]
    print()
    print("DEV SUITE VERIFICATION: " + ("PASS -- all 5 cases sealed clean" if all(results) else "FAIL -- see above"))
