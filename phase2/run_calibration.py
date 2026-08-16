"""Executes the plan declared in CALIBRATION.md. Dev suite (E1-E5) only.

Run:
    python run_calibration.py
"""
from __future__ import annotations

import statistics
from itertools import product
from typing import List, Tuple

from cases_dev import ALL_DEV_CASES
from graph_baseline import find_positive_cycle
from search import beam_diverse_search, beam_naive_search, mcts_search, random_search

SEEDS = list(range(10))

BUDGET = 100_000
MAX_DEPTH = 36

BEAM_WIDTH_GRID = [25, 50, 100]
NOVELTY_WEIGHT_GRID = [1, 2, 3, 5]
NOVELTY_K_GRID = [4, 8, 16]


def score_setting(recall: int, summed_cost: int) -> Tuple[int, int]:
    """Sort key: maximize recall, then minimize summed cost. Returns a
    tuple usable directly as a sort key with reverse semantics handled by
    the caller (recall descending, cost ascending)."""
    return recall, summed_cost


def evaluate_beam_naive(beam_width: int) -> Tuple[int, int, List[str]]:
    recall = 0
    summed_cost = 0
    missed = []
    for case in ALL_DEV_CASES:
        d = beam_naive_search(case.data, BUDGET, MAX_DEPTH, beam_width)
        if d:
            recall += 1
            summed_cost += d.cost
        else:
            missed.append(case.name)
    return recall, summed_cost, missed


def evaluate_beam_diverse(beam_width: int, novelty_weight: float, novelty_k: int) -> Tuple[int, int, List[str]]:
    recall = 0
    summed_cost = 0
    missed = []
    for case in ALL_DEV_CASES:
        d = beam_diverse_search(case.data, BUDGET, MAX_DEPTH, beam_width, novelty_k=novelty_k, novelty_weight=novelty_weight)
        if d:
            recall += 1
            summed_cost += d.cost
        else:
            missed.append(case.name)
    return recall, summed_cost, missed


def stage1_beam_width() -> int:
    print("=== Stage 1: beam_width (Beam-Naive, dev E1-E5) ===")
    results = []
    for bw in BEAM_WIDTH_GRID:
        recall, cost, missed = evaluate_beam_naive(bw)
        print(f"  beam_width={bw:4}  recall={recall}/5  summed_cost={cost:8}  missed={missed}")
        results.append((bw, recall, cost))
    # max recall first (descending), then min cost (ascending)
    best = sorted(results, key=lambda r: (-r[1], r[2]))[0]
    print(f"  -> chosen beam_width = {best[0]} (recall={best[1]}, summed_cost={best[2]})")
    return best[0]


def stage2_novelty(beam_width: int) -> Tuple[float, int]:
    print()
    print(f"=== Stage 2: novelty_weight x novelty_k (Beam-Diverse, beam_width={beam_width} fixed) ===")
    results = []
    for weight, k in product(NOVELTY_WEIGHT_GRID, NOVELTY_K_GRID):
        recall, cost, missed = evaluate_beam_diverse(beam_width, weight, k)
        print(f"  weight={weight:3} k={k:3}  recall={recall}/5  summed_cost={cost:8}  missed={missed}")
        results.append((weight, k, recall, cost))
    # max recall first, then min cost, then lowest weight (grid order) as final tiebreak
    best = sorted(results, key=lambda r: (-r[2], r[3], NOVELTY_WEIGHT_GRID.index(r[0])))[0]
    print(f"  -> chosen novelty_weight={best[0]}, novelty_k={best[1]} (recall={best[2]}, summed_cost={best[3]})")
    return best[0], best[1]


def dev_regression(beam_width: int, novelty_weight: float, novelty_k: int) -> None:
    print()
    print("=== Dev regression table, all 5 algorithms, frozen settings (E1-E5) ===")
    header = f"{'case':6}{'graph':16}{'random':16}{'beam-naive':14}{'beam-diverse':14}{'mcts':16}"
    print(header)
    print("-" * len(header))
    for case in ALL_DEV_CASES:
        g = find_positive_cycle(case.data)
        g_str = "N/A" if not g.supported else ("exploit_found" if g.exploit_found else "cycle_only" if g.cycle_detected else "not_found")

        r_costs = []
        for seed in SEEDS:
            d = random_search(case.data, seed, BUDGET, MAX_DEPTH)
            if d:
                r_costs.append(d.cost)
        r_str = f"{len(r_costs)}/10 med={int(statistics.median(r_costs)) if r_costs else '-'}"

        bn = beam_naive_search(case.data, BUDGET, MAX_DEPTH, beam_width)
        bn_str = f"cost={bn.cost}" if bn else "not found"

        bd = beam_diverse_search(case.data, BUDGET, MAX_DEPTH, beam_width, novelty_k=novelty_k, novelty_weight=novelty_weight)
        bd_str = f"cost={bd.cost}" if bd else "not found"

        m_costs = []
        for seed in SEEDS:
            d = mcts_search(case.data, seed, BUDGET, MAX_DEPTH)
            if d:
                m_costs.append(d.cost)
        m_str = f"{len(m_costs)}/10 med={int(statistics.median(m_costs)) if m_costs else '-'}"

        print(f"{case.name:6}{g_str:16}{r_str:16}{bn_str:14}{bd_str:14}{m_str:16}")


if __name__ == "__main__":
    beam_width = stage1_beam_width()
    novelty_weight, novelty_k = stage2_novelty(beam_width)
    print()
    print("=== FROZEN ===")
    print(f"BUDGET={BUDGET}")
    print(f"MAX_DEPTH={MAX_DEPTH}")
    print(f"BEAM_WIDTH={beam_width}")
    print(f"NOVELTY_WEIGHT={novelty_weight}")
    print(f"NOVELTY_K={novelty_k}")

    dev_regression(beam_width, novelty_weight, novelty_k)
