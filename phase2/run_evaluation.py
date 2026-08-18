"""Commit E: the ONE held-out evaluation. Run once. Whatever this shows,
it gets recorded, not re-tuned and not re-run. Every parameter is read
directly from frozen_params.py -- nothing here re-declares a number that
could quietly drift from what Commit D actually froze.

RQ2/RQ3 verdicts are computed by code from CONTRACT.md's sealed formulas,
not eyeballed after the fact.

Run:
    python run_evaluation.py
"""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from cases_dev import ALL_DEV_CASES, Case
from cases_heldout_exact import ALL_HELDOUT_CASES
from frozen_params import BEAM_WIDTH, BUDGET, MAX_DEPTH, MCTS_C, NOVELTY_K, NOVELTY_WEIGHT, SEEDS
from graph_baseline import find_positive_cycle
from oracle import is_exploit_found
from search import Discovery, beam_diverse_search, beam_naive_search, mcts_search, random_search

ALL_CASES: List[Case] = ALL_DEV_CASES + ALL_HELDOUT_CASES


@dataclass
class StochasticResult:
    success_rate: float
    median_cost: Optional[float]
    iqr: Optional[float]
    witness: Optional[Discovery]
    wall_seconds: float


@dataclass
class DeterministicResult:
    found: bool
    cost: Optional[int]
    witness: Optional[List]
    wall_seconds: float


def run_stochastic(fn, case: Case, **kwargs) -> StochasticResult:
    t0 = time.perf_counter()
    discoveries = [fn(case.data, seed, BUDGET, MAX_DEPTH, **kwargs) for seed in SEEDS]
    wall = time.perf_counter() - t0
    found = [d for d in discoveries if d is not None]
    costs = [d.cost for d in found]
    iqr = None
    if len(costs) >= 2:
        q = statistics.quantiles(costs, n=4, method="inclusive")
        iqr = q[2] - q[0]
    return StochasticResult(
        success_rate=len(found) / len(SEEDS),
        median_cost=statistics.median(costs) if costs else None,
        iqr=iqr,
        witness=found[0] if found else None,
        wall_seconds=wall,
    )


def run_deterministic_beam(fn, case: Case, **kwargs) -> DeterministicResult:
    t0 = time.perf_counter()
    d = fn(case.data, BUDGET, MAX_DEPTH, BEAM_WIDTH, **kwargs)
    wall = time.perf_counter() - t0
    return DeterministicResult(found=d is not None, cost=d.cost if d else None, witness=d.path if d else None, wall_seconds=wall)


def diverse_wins(naive: DeterministicResult, diverse: DeterministicResult) -> bool:
    if diverse.found and not naive.found:
        return True
    if diverse.found and naive.found and diverse.cost <= 0.75 * naive.cost:
        return True
    return False


if __name__ == "__main__":
    print(f"FROZEN: BUDGET={BUDGET} MAX_DEPTH={MAX_DEPTH} BEAM_WIDTH={BEAM_WIDTH} "
          f"NOVELTY_WEIGHT={NOVELTY_WEIGHT} NOVELTY_K={NOVELTY_K} MCTS_C={MCTS_C} SEEDS={len(SEEDS)}")
    print()

    results: Dict[str, dict] = {}
    for case in ALL_CASES:
        print(f"--- {case.name} ---")
        g = find_positive_cycle(case.data)
        g_status = "N/A" if not g.supported else ("exploit_found" if g.exploit_found else "cycle_only" if g.cycle_detected else "not_found")
        if g.path:
            assert is_exploit_found(case.data, g.path), f"{case.name}: graph witness FAILED oracle validation"

        r = run_stochastic(random_search, case)
        if r.witness:
            assert is_exploit_found(case.data, r.witness.path), f"{case.name}: random witness FAILED oracle validation"

        bn = run_deterministic_beam(beam_naive_search, case)
        if bn.witness:
            assert is_exploit_found(case.data, bn.witness), f"{case.name}: beam-naive witness FAILED oracle validation"

        bd = run_deterministic_beam(beam_diverse_search, case, novelty_k=NOVELTY_K, novelty_weight=NOVELTY_WEIGHT)
        if bd.witness:
            assert is_exploit_found(case.data, bd.witness), f"{case.name}: beam-diverse witness FAILED oracle validation"

        m = run_stochastic(mcts_search, case, c=MCTS_C)
        if m.witness:
            assert is_exploit_found(case.data, m.witness.path), f"{case.name}: mcts witness FAILED oracle validation"

        results[case.name] = dict(graph=g, graph_status=g_status, random=r, beam_naive=bn, beam_diverse=bd, mcts=m)

        print(f"  graph        : {g_status:14} wall={g.wall_seconds*1000:.2f}ms nodes={g.nodes_inspected} edges={g.edges_inspected}")
        print(f"  random       : {r.success_rate*10:.0f}/10  median={r.median_cost}  IQR={r.iqr}  wall={r.wall_seconds:.2f}s")
        print(f"  beam-naive   : {'found cost=' + str(bn.cost) if bn.found else 'not found'}  wall={bn.wall_seconds:.3f}s")
        print(f"  beam-diverse : {'found cost=' + str(bd.cost) if bd.found else 'not found'}  wall={bd.wall_seconds:.3f}s")
        print(f"  mcts         : {m.success_rate*10:.0f}/10  median={m.median_cost}  IQR={m.iqr}  wall={m.wall_seconds:.2f}s")
        print()

    print("ALL WITNESS PATHS VALIDATED AGAINST ORACLE: PASS (would have raised AssertionError otherwise)")
    print()

    # --- RQ2: diversity, held-out only (H1, H2, H3) ---
    print("=== RQ2 (diversity, held-out H1-H3) ===")
    wins = 0
    regression = False
    for case in ALL_HELDOUT_CASES:
        bn, bd = results[case.name]["beam_naive"], results[case.name]["beam_diverse"]
        win = diverse_wins(bn, bd)
        if win:
            wins += 1
        if bn.found and not bd.found:
            regression = True
        print(f"  {case.name}: naive_found={bn.found} (cost={bn.cost})  diverse_found={bd.found} (cost={bd.cost})  win={win}")
    if wins >= 2 and not regression:
        rq2_verdict = "STRONG"
    elif wins == 1 and not regression:
        rq2_verdict = "WEAK"
    else:
        rq2_verdict = "NO EVIDENCE"
    print(f"  wins={wins}/3  recall_regression={regression}  -> RQ2 VERDICT: {rq2_verdict}")
    print()

    # --- RQ3: lookahead, H2 only ---
    print("=== RQ3 (lookahead, H2 only) ===")
    m_h2 = results["H2"]["mcts"]
    bd_h2 = results["H2"]["beam_diverse"]
    strong_cond = m_h2.success_rate >= 0.8 and (not bd_h2.found or (m_h2.median_cost is not None and m_h2.median_cost <= 0.5 * bd_h2.cost))
    if m_h2.success_rate >= 0.8 and strong_cond:
        rq3_verdict = "STRONG"
    elif m_h2.success_rate > 0:
        rq3_verdict = "WEAK"
    else:
        rq3_verdict = "NO EVIDENCE"
    print(f"  mcts_success_rate={m_h2.success_rate}  mcts_median_cost={m_h2.median_cost}  beam_diverse_found={bd_h2.found} cost={bd_h2.cost}")
    print(f"  -> RQ3 VERDICT: {rq3_verdict}")
    print()

    # --- RQ1: full results table, no verdict, descriptive only ---
    print("=== RQ1 (structure-dependent method choice) -- results table ===")
    header = f"{'case':6}{'graph':16}{'random':18}{'beam-naive':14}{'beam-diverse':14}{'mcts':18}"
    print(header)
    print("-" * len(header))
    for case in ALL_CASES:
        r = results[case.name]
        g_str = r["graph_status"]
        rand_str = f"{r['random'].success_rate*10:.0f}/10 m={r['random'].median_cost}"
        bn_str = f"cost={r['beam_naive'].cost}" if r["beam_naive"].found else "not found"
        bd_str = f"cost={r['beam_diverse'].cost}" if r["beam_diverse"].found else "not found"
        m_str = f"{r['mcts'].success_rate*10:.0f}/10 m={r['mcts'].median_cost}"
        print(f"{case.name:6}{g_str:16}{rand_str:18}{bn_str:14}{bd_str:14}{m_str:18}")
