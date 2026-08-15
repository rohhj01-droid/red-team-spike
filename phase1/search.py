"""Phase 1 Minimal Core: search algorithms.

Ported from Phase 0 (../search.py). Random, Beam-Naive and Beam-Diverse are
kept as independent functions on purpose -- Random's rollout-based control
flow and Beam's layer-expand-then-select-top-K control flow are genuinely
different shapes, and a future MCTS (select/expand/simulate/backpropagate)
will be different again. Forcing all three into one `SearchStrategy`
interface now would be generalizing from imagination, not evidence: we only
have three examples, and the only two that truly share a shape
(Beam-Naive, Beam-Diverse) are left un-merged too, since even that
"evidence of two" isn't enough of a reason on its own yet. Only the pieces
that are ALREADY identical (Discovery, the profit callback) are shared.
"""
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple

from model import Action, GameState, RECIPES, STARTING_GOLD, SHOP_SELL, apply, initial_state, legal_actions
from profit_check import discovered_exploits, is_profit


@dataclass
class Discovery:
    expansions: int
    path: List[Action]


def estimate_values() -> Dict[str, float]:
    """See ../search.py docstring for why multi-input recipes are skipped
    (double-counting bug found and fixed in Phase 0 Round 1)."""
    value = {item: float(price) for item, price in SHOP_SELL.items()}
    for _ in range(len(RECIPES) + 1):
        for output, inputs in RECIPES.items():
            if output not in value or len(inputs) != 1:
                continue
            (item, qty), = inputs.items()
            derived = value[output] / qty
            if derived > value.get(item, 0.0):
                value[item] = derived
    return value


VALUE = estimate_values()


def score(state: GameState) -> float:
    return state.gold + sum(qty * VALUE.get(item, 0.0) for item, qty in state.inventory)


def random_search(seed: int, budget: int, max_depth: int) -> Dict[str, Discovery]:
    rng = random.Random(seed)
    start = initial_state()
    found: Dict[str, Discovery] = {}
    expansions = 0
    while expansions < budget:
        state = start
        path: List[Action] = []
        for _ in range(max_depth):
            actions = legal_actions(state)
            if not actions:
                break
            action = rng.choice(actions)
            state = apply(state, action)
            path.append(action)
            expansions += 1
            if is_profit(state, start.gold):
                for fam in discovered_exploits(path):
                    if fam not in found:
                        found[fam] = Discovery(expansions, list(path))
            if expansions >= budget:
                break
    return found


def beam_naive_search(budget: int, max_depth: int, beam_width: int, num_exploits: int) -> Tuple[Dict[str, Discovery], int]:
    start = initial_state()
    beam: List[Tuple[GameState, List[Action]]] = [(start, [])]
    found: Dict[str, Discovery] = {}
    expansions = 0
    for _ in range(max_depth):
        if not beam or expansions >= budget or len(found) >= num_exploits:
            break
        candidates: Dict[GameState, Tuple[float, List[Action]]] = {}
        for state, path in beam:
            if expansions >= budget:
                break
            for action in legal_actions(state):
                if expansions >= budget:
                    break
                new_state = apply(state, action)
                new_path = path + [action]
                expansions += 1
                if is_profit(new_state, start.gold):
                    for fam in discovered_exploits(new_path):
                        if fam not in found:
                            found[fam] = Discovery(expansions, new_path)
                existing = candidates.get(new_state)
                if existing is None or len(new_path) < len(existing[1]):
                    candidates[new_state] = (score(new_state), new_path)
        ranked = sorted(candidates.items(), key=lambda kv: kv[1][0], reverse=True)
        beam = [(s, p) for s, (_, p) in ranked[:beam_width]]
    return found, expansions


def behavior_descriptor(state: GameState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(kind_counts.get(k, 0) / path_len for k in ("buy", "sell", "craft", "dismantle"))
    craftable = sum(
        1 for inputs in RECIPES.values()
        if all(state.qty(item) >= req for item, req in inputs.items())
    )
    return action_ratio + (
        len(state.inventory) / 5.0,
        sum(qty for _, qty in state.inventory) / 10.0,
        state.gold / STARTING_GOLD,
        craftable / len(RECIPES),
        len(path) / max_depth,
    )


def _euclidean(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def _novelty_scores(descriptors: List[Tuple[float, ...]], k: int) -> List[float]:
    scores = []
    for i, d in enumerate(descriptors):
        dists = sorted(_euclidean(d, other) for j, other in enumerate(descriptors) if j != i)
        neighbors = dists[:k] if dists else [0.0]
        scores.append(sum(neighbors) / len(neighbors) if neighbors else 0.0)
    return scores


def _rank_normalize(values: List[float]) -> List[float]:
    n = len(values)
    if n <= 1:
        return [1.0] * n
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    for rank, i in enumerate(order):
        ranks[i] = rank / (n - 1)
    return ranks


def beam_diverse_search(
    budget: int, max_depth: int, beam_width: int, num_exploits: int,
    novelty_k: int = 8, novelty_weight: float = 3.0,
) -> Tuple[Dict[str, Discovery], int]:
    start = initial_state()
    beam: List[Tuple[GameState, List[Action]]] = [(start, [])]
    found: Dict[str, Discovery] = {}
    expansions = 0
    for _ in range(max_depth):
        if not beam or expansions >= budget or len(found) >= num_exploits:
            break
        candidates: Dict[GameState, Tuple[float, List[Action]]] = {}
        for state, path in beam:
            if expansions >= budget:
                break
            for action in legal_actions(state):
                if expansions >= budget:
                    break
                new_state = apply(state, action)
                new_path = path + [action]
                expansions += 1
                if is_profit(new_state, start.gold):
                    for fam in discovered_exploits(new_path):
                        if fam not in found:
                            found[fam] = Discovery(expansions, new_path)
                existing = candidates.get(new_state)
                if existing is None or len(new_path) < len(existing[1]):
                    candidates[new_state] = (score(new_state), new_path)
        if not candidates:
            break
        states = list(candidates.keys())
        descriptors = [behavior_descriptor(s, candidates[s][1], max_depth) for s in states]
        k = min(novelty_k, len(states) - 1)
        novelty = _novelty_scores(descriptors, k) if k > 0 else [0.0] * len(states)
        obj_rank = _rank_normalize([candidates[s][0] for s in states])
        novelty_rank = _rank_normalize(novelty)
        combined = [o + novelty_weight * v for o, v in zip(obj_rank, novelty_rank)]
        ranked = sorted(zip(states, combined), key=lambda sc: sc[1], reverse=True)
        beam = [(s, candidates[s][1]) for s, _ in ranked[:beam_width]]
    return found, expansions
