"""POST-HOC DIAGNOSTIC -- NOT part of the sealed C3 search contract.
Never used to retroactively change the official result in `ecbd536`
(C3 SEARCH INTEGRATION: FAIL). Its own result is reported as a
diagnostic finding, not a re-run of the official test.

Tests one specific hypothesis about why beam_naive_search and
beam_diverse_search returned None in the official run: a legitimately-
reached CLAIMED state is terminal with respect to producing any FUTURE
exploit-triggering claim transition (quest_status never reverts from
CLAIMED), but score()'s quest-status-only signal treats it as the
single best possible outcome (score=2), so its descendants keep
entering the beam. C3's richer post-claim action set (equip +
enchant/unenchant + possibly channel, all still legal post-claim)
makes those dead-end descendants multiply fast enough to displace every
still-alive exploit-capable ACTIVE branch under BEAM_WIDTH=5.

The ONLY change from search.py's beam_naive_search/beam_diverse_search:
beam members whose WorldState has quest_status == "CLAIMED" are
excluded from expansion this layer (contribute no candidates, so they
can't out-compete live branches for a beam slot). BEAM_WIDTH, score(),
behavior_descriptor(), novelty weighting, MAX_DEPTH, BUDGET are all
untouched -- identical to SEARCH_CONTRACT_C3.md's frozen values.

Run:
    python diagnostic_claimed_terminal.py
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from budget import Budget, BudgetExhausted
from engine import Action, legal_actions, initial_world
from monitor import initial_monitor
from search import (
    Discovery, SearchState, _novelty_scores, _rank_normalize, _step,
    behavior_descriptor, score,
)

MAX_DEPTH = 15
BUDGET = 1_000
BEAM_WIDTH = 5
NOVELTY_WEIGHT = 1
NOVELTY_K = 4


def beam_naive_claimed_terminal(budget_limit: int, max_depth: int, beam_width: int) -> Optional[Discovery]:
    budget = Budget(budget_limit)
    start: SearchState = (initial_world(), initial_monitor())
    beam: List[Tuple[SearchState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[SearchState, Tuple[float, List[Action]]] = {}
            for (world, monitor), path in beam:
                if world.quest_status == "CLAIMED":
                    continue  # ONLY CHANGE: don't expand a legitimately-claimed dead end
                if not budget.remaining():
                    break
                for action in legal_actions(world):
                    if not budget.remaining():
                        break
                    new_world, new_monitor, classification = _step(budget, world, monitor, action)
                    new_state = (new_world, new_monitor)
                    new_path = path + [action]
                    if classification is not None:
                        return Discovery(budget.used, new_path, classification)
                    existing = candidates.get(new_state)
                    if existing is None or len(new_path) < len(existing[1]):
                        candidates[new_state] = (score(new_world), new_path)
            ranked = sorted(candidates.items(), key=lambda kv: kv[1][0], reverse=True)
            beam = [(s, p) for s, (_, p) in ranked[:beam_width]]
    except BudgetExhausted:
        pass
    return None


def beam_diverse_claimed_terminal(
    budget_limit: int, max_depth: int, beam_width: int,
    novelty_k: int = 4, novelty_weight: float = 1.0,
) -> Optional[Discovery]:
    budget = Budget(budget_limit)
    start: SearchState = (initial_world(), initial_monitor())
    beam: List[Tuple[SearchState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[SearchState, Tuple[float, List[Action]]] = {}
            for (world, monitor), path in beam:
                if world.quest_status == "CLAIMED":
                    continue  # ONLY CHANGE: don't expand a legitimately-claimed dead end
                if not budget.remaining():
                    break
                for action in legal_actions(world):
                    if not budget.remaining():
                        break
                    new_world, new_monitor, classification = _step(budget, world, monitor, action)
                    new_state = (new_world, new_monitor)
                    new_path = path + [action]
                    if classification is not None:
                        return Discovery(budget.used, new_path, classification)
                    existing = candidates.get(new_state)
                    if existing is None or len(new_path) < len(existing[1]):
                        candidates[new_state] = (score(new_world), new_path)
            if not candidates:
                break
            states = list(candidates.keys())
            descriptors = [behavior_descriptor(s[0], candidates[s][1], max_depth) for s in states]
            k = min(novelty_k, len(states) - 1)
            novelty = _novelty_scores(descriptors, k) if k > 0 else [0.0] * len(states)
            obj_rank = _rank_normalize([candidates[s][0] for s in states])
            novelty_rank = _rank_normalize(novelty)
            combined = [o + novelty_weight * v for o, v in zip(obj_rank, novelty_rank)]
            ranked = sorted(zip(states, combined), key=lambda sc: sc[1], reverse=True)
            beam = [(s, candidates[s][1]) for s, _ in ranked[:beam_width]]
    except BudgetExhausted:
        pass
    return None


if __name__ == "__main__":
    print("=== DIAGNOSTIC ONLY -- not the official C3 search contract result ===")
    print("Official result stays sealed as FAIL (ecbd536). This only tests")
    print("whether treating legitimate CLAIMED states as non-expandable dead")
    print("ends explains the displacement -- BEAM_WIDTH/score/novelty/depth")
    print("are all still the frozen contract values.")
    print()

    d1 = beam_naive_claimed_terminal(BUDGET, MAX_DEPTH, BEAM_WIDTH)
    print(f"beam_naive (CLAIMED-terminal):   {d1}")
    print()

    d2 = beam_diverse_claimed_terminal(BUDGET, MAX_DEPTH, BEAM_WIDTH, novelty_k=NOVELTY_K, novelty_weight=NOVELTY_WEIGHT)
    print(f"beam_diverse (CLAIMED-terminal): {d2}")

    print()
    if d1 and d2:
        print("DIAGNOSTIC RESULT: hypothesis SUPPORTED -- both variants found a witness")
        print("once legitimate CLAIMED states stopped being expanded. Explains the")
        print("official FAIL; does not change it.")
    elif d1 or d2:
        print("DIAGNOSTIC RESULT: PARTIAL -- only one variant found a witness.")
        print("The CLAIMED-dead-end mechanism is not the whole story.")
    else:
        print("DIAGNOSTIC RESULT: hypothesis NOT SUPPORTED -- still no witness even")
        print("with CLAIMED treated as terminal. The explanation needs more work.")
