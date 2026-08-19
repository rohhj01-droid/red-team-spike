"""C2 search integration test. Per SEARCH_CONTRACT_C2.md's interpretation
rule: reports PASS/FAIL per algorithm (found a witness + witness replays
legally + independently-recomputed classification at the actual claim
transition matches what search recorded), never a comparison table.

Run:
    python run_c2_integration.py
"""
from __future__ import annotations

import inspect

from engine import apply, initial_world, legal_actions
from monitor import initial_monitor, monitor_step
from oracle import classify_claim
from search import (
    Discovery, beam_diverse_search, beam_naive_search, behavior_descriptor,
    mcts_search, random_search, score,
)

MAX_DEPTH = 15
BUDGET = 1_000
BEAM_WIDTH = 5
NOVELTY_WEIGHT = 1
NOVELTY_K = 4
SEEDS = list(range(10))


def check_no_monitor_parameter() -> bool:
    """Visibility-by-construction check: score()/behavior_descriptor()
    literally cannot accept a MonitorState -- their signatures have no
    parameter for one, not just "happen not to use it"."""
    score_params = set(inspect.signature(score).parameters)
    descriptor_params = set(inspect.signature(behavior_descriptor).parameters)
    ok = "monitor" not in score_params and "monitor" not in descriptor_params
    print(f"  score() params: {score_params}")
    print(f"  behavior_descriptor() params: {descriptor_params}")
    print(f"  no monitor parameter anywhere: {'PASS' if ok else 'FAIL'}")
    return ok


def replay_and_validate(discovery: Discovery) -> bool:
    """Legal replay, plus independent reclassification at the witness's
    own claim transition -- must match what search recorded."""
    world, monitor = initial_world(), initial_monitor()
    reclassified = None
    for action in discovery.path:
        if action not in legal_actions(world):
            print(f"    FAIL: witness action {action} illegal at {world}")
            return False
        if action.kind == "claim":
            reclassified = classify_claim(action, monitor)
        new_world = apply(world, action)
        monitor = monitor_step(world, action, new_world, monitor)
        world = new_world
    if reclassified is None:
        print(f"    FAIL: replayed witness never fires a violating claim -- world={world} monitor={monitor}")
        return False
    if reclassified != discovery.classification:
        print(f"    FAIL: search recorded {discovery.classification}, independent replay found {reclassified}")
        return False
    return True


def check_random() -> bool:
    print("--- random_search (10 seeds) ---")
    all_ok = True
    found = 0
    for seed in SEEDS:
        d = random_search(seed, BUDGET, MAX_DEPTH)
        if d:
            found += 1
            if not replay_and_validate(d):
                all_ok = False
    print(f"  found valid witness: {found}/{len(SEEDS)} seeds")
    if found == 0:
        print("  FAIL: no seed found a witness at all")
        return False
    return all_ok


def check_beam_naive() -> bool:
    print("--- beam_naive_search ---")
    d = beam_naive_search(BUDGET, MAX_DEPTH, BEAM_WIDTH)
    if not d:
        print("  FAIL: no witness found")
        return False
    ok = replay_and_validate(d)
    print(f"  found witness, cost={d.cost}, classification={d.classification}: {'PASS' if ok else 'FAIL'}")
    return ok


def check_beam_diverse() -> bool:
    print("--- beam_diverse_search ---")
    d = beam_diverse_search(BUDGET, MAX_DEPTH, BEAM_WIDTH, novelty_k=NOVELTY_K, novelty_weight=NOVELTY_WEIGHT)
    if not d:
        print("  FAIL: no witness found")
        return False
    ok = replay_and_validate(d)
    print(f"  found witness, cost={d.cost}, classification={d.classification}: {'PASS' if ok else 'FAIL'}")
    return ok


def check_mcts() -> bool:
    print("--- mcts_search (10 seeds) ---")
    all_ok = True
    found = 0
    for seed in SEEDS:
        d = mcts_search(seed, BUDGET, MAX_DEPTH)
        if d:
            found += 1
            if not replay_and_validate(d):
                all_ok = False
    print(f"  found valid witness: {found}/{len(SEEDS)} seeds")
    if found == 0:
        print("  FAIL: no seed found a witness at all")
        return False
    return all_ok


if __name__ == "__main__":
    print("=== Visibility-by-construction check ===")
    ok_visibility = check_no_monitor_parameter()
    print()
    print("=== Algorithm integration checks (pass/fail only, no comparison) ===")
    results = {
        "random": check_random(),
        "beam_naive": check_beam_naive(),
        "beam_diverse": check_beam_diverse(),
        "mcts": check_mcts(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    overall = ok_visibility and all(results.values())
    print()
    print("C2 SEARCH INTEGRATION: " + ("PASS" if overall else "FAIL"))
