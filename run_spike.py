"""Phase 0 Feasibility Spike -- entry point.

ROUND 1 question (sealed before this code was written):
  Can automated search find hand-planted exploits in a small economy+crafting
  system, and does Beam Search show a real advantage over Random on the
  delayed-reward cases (E4/E5)?

Round 1 result: AMBIGUOUS. Recall 5/5, but naive Beam (Beam-Naive, pure
economic score() selection) found NEITHER E4 nor E5 -- worse than Random.
Diagnosis (verified, not guessed): Beam-Naive's top-K beam collapses onto
whichever single strategy has the best per-action score (buying Trinket,
+15/action), starving other branches of beam width before they can complete.
That result and its code path (beam_naive_search) are FROZEN -- not modified.

ROUND 2 (H2): Beam-Naive's failure is diversity collapse, not a fundamental
search limit. A diversity-preserving variant (Beam-Diverse) that adds a
novelty term computed ONLY from generic state/action descriptors (action
kind ratios, inventory shape, gold, craftable-recipe count -- see
search.behavior_descriptor) -- never from which items belong to which
sealed exploit -- should recover E4/E5 without being told where to look.

Round 2 grading (sealed before this run):
  STRONG SUCCESS  Beam-Diverse finds E4 or E5, with cost <= 50% of Random's
                  median (or Random fails within budget while Diverse
                  succeeds), AND E1/E2/E3 recall is not sacrificed.
  WEAK SUCCESS    Beam-Diverse finds E4 or E5 but with no cost advantage
                  over Random.
  FAILURE         Beam-Diverse still finds neither E4 nor E5. Beam is not
                  tuned further after this -- MCTS/QD are the next things to
                  try, in a later phase, not more knob-turning here.

Run:
    python run_spike.py
"""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from search import Discovery, beam_diverse_search, beam_naive_search, random_search

BUDGET = 100_000       # state expansions, same cap for every algorithm and every random seed
MAX_DEPTH = 25          # generous headroom over E5's 12-action minimum
BEAM_WIDTH = 50
RANDOM_SEEDS = list(range(10))
EXPLOITS = ["E1", "E2", "E3", "E4", "E5"]


@dataclass
class ExploitResult:
    beam_found: bool
    beam_cost: Optional[int]
    random_found_seeds: int  # out of len(RANDOM_SEEDS)
    random_median_cost: Optional[int]


def run_random() -> List[Dict[str, Discovery]]:
    t0 = time.perf_counter()
    per_seed = [random_search(seed, BUDGET, MAX_DEPTH) for seed in RANDOM_SEEDS]
    t1 = time.perf_counter()
    print(f"[random] {len(RANDOM_SEEDS)} seeds x {BUDGET} budget  wall={t1 - t0:6.2f}s")
    return per_seed


def summarize(beam_found: Dict[str, Discovery], per_seed: List[Dict[str, Discovery]]) -> Dict[str, ExploitResult]:
    results: Dict[str, ExploitResult] = {}
    for exploit in EXPLOITS:
        costs = [r[exploit].expansions for r in per_seed if exploit in r]
        results[exploit] = ExploitResult(
            beam_found=exploit in beam_found,
            beam_cost=beam_found[exploit].expansions if exploit in beam_found else None,
            random_found_seeds=len(costs),
            random_median_cost=int(statistics.median(costs)) if costs else None,
        )
    return results


def grade_round1(results: Dict[str, ExploitResult]) -> str:
    """Frozen. Do not modify -- this is the sealed Round 1 verdict."""
    recall = sum(1 for r in results.values() if r.beam_found or r.random_found_seeds > 0)

    beam_advantage = False
    for exploit in ("E4", "E5"):
        r = results[exploit]
        if not r.beam_found:
            continue
        if r.random_found_seeds == 0:
            beam_advantage = True
        elif r.beam_cost is not None and r.random_median_cost is not None:
            if r.beam_cost <= 0.5 * r.random_median_cost:
                beam_advantage = True

    if recall >= 4 and beam_advantage:
        return "PASS"
    if recall <= 2:
        return "FAIL"
    return "AMBIGUOUS"


def grade_round2(results: Dict[str, ExploitResult]) -> str:
    easy_intact = all(results[e].beam_found for e in ("E1", "E2", "E3"))
    hard_found = [e for e in ("E4", "E5") if results[e].beam_found]
    if not hard_found:
        return "FAILURE"

    strong = False
    for exploit in hard_found:
        r = results[exploit]
        if r.random_found_seeds == 0:
            strong = True
        elif r.beam_cost is not None and r.random_median_cost is not None:
            if r.beam_cost <= 0.5 * r.random_median_cost:
                strong = True

    return "STRONG SUCCESS" if (strong and easy_intact) else "WEAK SUCCESS"


def print_table(results: Dict[str, ExploitResult]) -> None:
    header = f"{'exploit':7} {'beam_found':11} {'beam_cost':10} {'rand_found':11} {'rand_median_cost':17}"
    print(header)
    print("-" * len(header))
    for exploit in EXPLOITS:
        r = results[exploit]
        print(
            f"{exploit:7} {str(r.beam_found):11} {str(r.beam_cost):10} "
            f"{f'{r.random_found_seeds}/{len(RANDOM_SEEDS)}':11} {str(r.random_median_cost):17}"
        )


if __name__ == "__main__":
    per_seed = run_random()

    print()
    print("=== ROUND 1: Beam-Naive (frozen, sealed contract) ===")
    t0 = time.perf_counter()
    naive_found, naive_expansions = beam_naive_search(BUDGET, MAX_DEPTH, BEAM_WIDTH, len(EXPLOITS))
    t1 = time.perf_counter()
    print(f"[beam-naive]   expansions_used={naive_expansions:>7}  wall={t1 - t0:6.2f}s  found={sorted(naive_found)}")
    round1_results = summarize(naive_found, per_seed)
    print_table(round1_results)
    print(f"\nROUND 1 VERDICT: {grade_round1(round1_results)}  (frozen, unchanged from the sealed run)")

    print()
    print("=== ROUND 2: Beam-Diverse (H2: diversity collapse fix, no exploit-ID leakage) ===")
    t0 = time.perf_counter()
    diverse_found, diverse_expansions = beam_diverse_search(BUDGET, MAX_DEPTH, BEAM_WIDTH, len(EXPLOITS))
    t1 = time.perf_counter()
    print(f"[beam-diverse] expansions_used={diverse_expansions:>7}  wall={t1 - t0:6.2f}s  found={sorted(diverse_found)}")
    round2_results = summarize(diverse_found, per_seed)
    print_table(round2_results)
    print(f"\nROUND 2 VERDICT: {grade_round2(round2_results)}")
