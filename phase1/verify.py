"""Phase 1 completion check.

Phase 1's ONLY job: reproduce Phase 0's frozen Round 1 / Round 2 numbers
(see ../README.md) inside the new model.py / search.py / profit_check.py
split. No new features, no new algorithms. If every number below matches
exactly, Phase 1 is done -- nothing else is required to call it complete.

Run:
    python verify.py
"""
from __future__ import annotations

import statistics
from typing import Dict, List, Optional

from search import Discovery, beam_diverse_search, beam_naive_search, random_search

BUDGET = 100_000
MAX_DEPTH = 25
BEAM_WIDTH = 50
RANDOM_SEEDS = list(range(10))
EXPLOITS = ["E1", "E2", "E3", "E4", "E5"]

# Frozen Phase 0 results (red-team-spike/README.md). (beam_found, beam_cost)
EXPECTED_ROUND1 = {
    "E1": (True, 13), "E2": (True, 259), "E3": (True, 302),
    "E4": (False, None), "E5": (False, None),
}
EXPECTED_ROUND2 = {
    "E1": (True, 21), "E2": (True, 245), "E3": (True, 237),
    "E4": (True, 718), "E5": (False, None),
}
EXPECTED_RANDOM = {
    "E1": (10, 17), "E2": (10, 48), "E3": (10, 73),
    "E4": (10, 1255), "E5": (6, 40012),
}


def summarize(beam_found: Dict[str, Discovery]) -> Dict[str, tuple]:
    return {
        exploit: (exploit in beam_found, beam_found[exploit].expansions if exploit in beam_found else None)
        for exploit in EXPLOITS
    }


def check(label: str, actual: Dict[str, tuple], expected: Dict[str, tuple]) -> bool:
    ok = True
    for exploit in EXPLOITS:
        if actual[exploit] != expected[exploit]:
            print(f"  MISMATCH [{label}] {exploit}: got {actual[exploit]}, expected {expected[exploit]}")
            ok = False
    return ok


if __name__ == "__main__":
    per_seed: List[Dict[str, Discovery]] = [random_search(seed, BUDGET, MAX_DEPTH) for seed in RANDOM_SEEDS]
    random_actual = {
        exploit: (
            len([r for r in per_seed if exploit in r]),
            int(statistics.median([r[exploit].expansions for r in per_seed if exploit in r]))
            if any(exploit in r for r in per_seed) else None,
        )
        for exploit in EXPLOITS
    }

    naive_found, _ = beam_naive_search(BUDGET, MAX_DEPTH, BEAM_WIDTH, len(EXPLOITS))
    diverse_found, _ = beam_diverse_search(BUDGET, MAX_DEPTH, BEAM_WIDTH, len(EXPLOITS))

    ok = True
    ok &= check("random", random_actual, EXPECTED_RANDOM)
    ok &= check("beam-naive", summarize(naive_found), EXPECTED_ROUND1)
    ok &= check("beam-diverse", summarize(diverse_found), EXPECTED_ROUND2)

    print("PHASE 1 REPRODUCTION: " + ("PASS -- matches Phase 0 exactly" if ok else "FAIL -- see mismatches above"))
