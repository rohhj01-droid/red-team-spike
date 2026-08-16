"""Commit C sanity/smoke test -- dev suite (E1-E5) ONLY.

Confirms each algorithm is wired correctly: runs, doesn't crash, and finds
the trivially-easy cases. This is NOT calibration (no parameter is chosen
based on these results -- the values below are the same defaults Phase
0/1 used, unexamined) and it never touches cases_heldout -- H1/H2/H3 don't
have concrete data yet and are not a valid target for anything in Commit C.

Run:
    python test_algorithms.py
"""
from __future__ import annotations

from cases_dev import ALL_DEV_CASES, Case
from graph_baseline import find_positive_cycle
from oracle import is_exploit_found
from search import beam_diverse_search, beam_naive_search, mcts_search, random_search

BUDGET = 10_000
DEPTH_HEADROOM = 10
RANDOM_SEEDS = [0, 1, 2]
MCTS_SEEDS = [0, 1, 2]
BEAM_WIDTH = 30


def check_graph(case: Case) -> None:
    r = find_positive_cycle(case.data)
    if case.name == "E2":
        assert not r.supported, "E2 has a multi-input recipe; must be reported unsupported"
    status = "N/A" if not r.supported else ("found+path" if r.path else "found,no-path" if r.found else "not-found")
    print(f"    graph          : {status:14} nodes={r.nodes_inspected} edges={r.edges_inspected} wall={r.wall_seconds*1000:.2f}ms")
    if r.path:
        assert is_exploit_found(case.data, r.path), "graph baseline's own reconstructed path failed oracle validation"


def check_random(case: Case, max_depth: int) -> None:
    found = 0
    for seed in RANDOM_SEEDS:
        d = random_search(case.data, seed, BUDGET, max_depth)
        if d:
            found += 1
            assert is_exploit_found(case.data, d.path), "random found a path the oracle rejects"
    print(f"    random         : {found}/{len(RANDOM_SEEDS)} seeds found it (budget={BUDGET})")


def check_beam_naive(case: Case, max_depth: int) -> None:
    d = beam_naive_search(case.data, BUDGET, max_depth, BEAM_WIDTH)
    if d:
        assert is_exploit_found(case.data, d.path), "beam-naive found a path the oracle rejects"
    print(f"    beam-naive     : {'found cost=' + str(d.cost) if d else 'not found'}")


def check_beam_diverse(case: Case, max_depth: int) -> None:
    d = beam_diverse_search(case.data, BUDGET, max_depth, BEAM_WIDTH)
    if d:
        assert is_exploit_found(case.data, d.path), "beam-diverse found a path the oracle rejects"
    print(f"    beam-diverse   : {'found cost=' + str(d.cost) if d else 'not found'}")


def check_mcts(case: Case, max_depth: int) -> None:
    found = 0
    for seed in MCTS_SEEDS:
        d = mcts_search(case.data, seed, BUDGET, max_depth)
        if d:
            found += 1
            assert is_exploit_found(case.data, d.path), "mcts found a path the oracle rejects"
    print(f"    mcts           : {found}/{len(MCTS_SEEDS)} seeds found it (budget={BUDGET})")


if __name__ == "__main__":
    for case in ALL_DEV_CASES:
        max_depth = len(case.minimal_path) + DEPTH_HEADROOM
        print(f"--- {case.name} (minimal depth {len(case.minimal_path)}, search max_depth {max_depth})")
        check_graph(case)
        check_random(case, max_depth)
        check_beam_naive(case, max_depth)
        check_beam_diverse(case, max_depth)
        check_mcts(case, max_depth)

    print()
    print("SANITY CHECK PASSED: no crashes, no oracle-rejected paths from any algorithm.")
