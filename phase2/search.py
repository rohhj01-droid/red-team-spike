"""Phase 2 search algorithms: Random, Beam-Naive, Beam-Diverse, MCTS.

Four independent functions, not a shared SearchStrategy interface --
Random's rollout control flow, Beam's layer-expand-then-select-top-K, and
MCTS's select/expand/rollout/backpropagate are genuinely different shapes
(same reasoning as Phase 1's search.py). Only what's truly identical
across all of them is shared: `Budget` (cost accounting) and `Discovery`.

Every algorithm operates on a single isolated Case's `GameData` and
returns `Optional[Discovery]` -- there is exactly one exploit possible per
case now (CONTRACT.md "every case is an isolated environment"), so unlike
Phase 0/1 there's no dict-of-exploit-id to track.

MCTS is the textbook baseline on purpose (CONTRACT.md, C's scope): UCT
with a uniform-random rollout policy and a binary [0, 1] reward. No
delayed-reward-specific shaping -- that would be designing the algorithm
around H2 before H2 exists, which the whole commit ordering was built to
prevent.
"""
from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from budget import Budget, BudgetExhausted
from engine import Action, GameData, GameState, initial_state, legal_actions
from oracle import is_profitable_state


@dataclass
class Discovery:
    cost: int  # transition evaluations
    path: List[Action]


# ---------------------------------------------------------------------------
# Random
# ---------------------------------------------------------------------------

def random_search(data: GameData, seed: int, budget_limit: int, max_depth: int) -> Optional[Discovery]:
    rng = random.Random(seed)
    budget = Budget(budget_limit)
    start = initial_state(data)
    try:
        while budget.remaining():
            state = start
            path: List[Action] = []
            for _ in range(max_depth):
                actions = legal_actions(data, state)
                if not actions:
                    break
                action = rng.choice(actions)
                state = budget.step(data, state, action)
                path.append(action)
                if is_profitable_state(data, state):
                    return Discovery(budget.used, path)
                if not budget.remaining():
                    break
    except BudgetExhausted:
        pass
    return None


# ---------------------------------------------------------------------------
# Beam-Naive / Beam-Diverse (ported from phase1/search.py, parameterized by
# `data` instead of a fixed module-level game)
# ---------------------------------------------------------------------------

def estimate_values(data: GameData) -> Dict[str, float]:
    """See phase1/search.py -- single-input-recipe-only propagation, fixing
    Phase 0's double-counting bug. Same rule, now parameterized."""
    value = {item: float(price) for item, price in data.shop_sell.items()}
    for _ in range(len(data.recipes) + 1):
        for output, inputs in data.recipes.items():
            if output not in value or len(inputs) != 1:
                continue
            (item, qty), = inputs.items()
            derived = value[output] / qty
            if derived > value.get(item, 0.0):
                value[item] = derived
    return value


def score(data: GameData, value: Dict[str, float], state: GameState) -> float:
    return state.gold + sum(qty * value.get(item, 0.0) for item, qty in state.inventory)


def beam_naive_search(data: GameData, budget_limit: int, max_depth: int, beam_width: int) -> Optional[Discovery]:
    value = estimate_values(data)
    budget = Budget(budget_limit)
    start = initial_state(data)
    beam: List[Tuple[GameState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[GameState, Tuple[float, List[Action]]] = {}
            for state, path in beam:
                if not budget.remaining():
                    break
                for action in legal_actions(data, state):
                    if not budget.remaining():
                        break
                    new_state = budget.step(data, state, action)
                    new_path = path + [action]
                    if is_profitable_state(data, new_state):
                        return Discovery(budget.used, new_path)
                    existing = candidates.get(new_state)
                    if existing is None or len(new_path) < len(existing[1]):
                        candidates[new_state] = (score(data, value, new_state), new_path)
            ranked = sorted(candidates.items(), key=lambda kv: kv[1][0], reverse=True)
            beam = [(s, p) for s, (_, p) in ranked[:beam_width]]
    except BudgetExhausted:
        pass
    return None


def behavior_descriptor(data: GameData, state: GameState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(kind_counts.get(k, 0) / path_len for k in ("buy", "sell", "craft", "dismantle"))
    craftable = sum(
        1 for inputs in data.recipes.values()
        if all(state.qty(item) >= req for item, req in inputs.items())
    )
    n_recipes = max(len(data.recipes), 1)
    return action_ratio + (
        len(state.inventory) / 5.0,
        sum(qty for _, qty in state.inventory) / 10.0,
        state.gold / data.starting_gold,
        craftable / n_recipes,
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
    data: GameData, budget_limit: int, max_depth: int, beam_width: int,
    novelty_k: int = 8, novelty_weight: float = 3.0,
) -> Optional[Discovery]:
    value = estimate_values(data)
    budget = Budget(budget_limit)
    start = initial_state(data)
    beam: List[Tuple[GameState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[GameState, Tuple[float, List[Action]]] = {}
            for state, path in beam:
                if not budget.remaining():
                    break
                for action in legal_actions(data, state):
                    if not budget.remaining():
                        break
                    new_state = budget.step(data, state, action)
                    new_path = path + [action]
                    if is_profitable_state(data, new_state):
                        return Discovery(budget.used, new_path)
                    existing = candidates.get(new_state)
                    if existing is None or len(new_path) < len(existing[1]):
                        candidates[new_state] = (score(data, value, new_state), new_path)
            if not candidates:
                break
            states = list(candidates.keys())
            descriptors = [behavior_descriptor(data, s, candidates[s][1], max_depth) for s in states]
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


# ---------------------------------------------------------------------------
# MCTS (new) -- textbook UCT, binary reward, uniform-random rollout policy.
# ---------------------------------------------------------------------------

UCT_C = math.sqrt(2)  # CONTRACT.md default; valid because reward is binary [0,1]


class _Node:
    __slots__ = ("state", "parent", "action_from_parent", "children", "untried", "visits", "reward")

    def __init__(self, state: GameState, parent: Optional["_Node"], action_from_parent: Optional[Action], untried: List[Action]):
        self.state = state
        self.parent = parent
        self.action_from_parent = action_from_parent
        self.children: Dict[Action, "_Node"] = {}
        self.untried = untried
        self.visits = 0
        self.reward = 0.0


def _path_to(node: _Node) -> List[Action]:
    path = []
    while node.parent is not None:
        path.append(node.action_from_parent)
        node = node.parent
    path.reverse()
    return path


def _uct_select(node: _Node, c: float) -> _Node:
    log_n = math.log(node.visits)
    return max(
        node.children.values(),
        key=lambda ch: ch.reward / ch.visits + c * math.sqrt(log_n / ch.visits),
    )


def mcts_search(
    data: GameData, seed: int, budget_limit: int, max_depth: int, c: float = UCT_C,
) -> Optional[Discovery]:
    rng = random.Random(seed)
    budget = Budget(budget_limit)
    root = _Node(initial_state(data), None, None, legal_actions(data, initial_state(data)))
    best: Optional[Discovery] = None

    try:
        while budget.remaining() and best is None:
            # Selection
            node = root
            depth = 0
            while not node.untried and node.children and depth < max_depth:
                node = _uct_select(node, c)
                depth += 1

            # Expansion
            if node.untried and depth < max_depth:
                action = rng.choice(node.untried)
                node.untried.remove(action)
                new_state = budget.step(data, node.state, action)
                child = _Node(new_state, node, action, legal_actions(data, new_state))
                node.children[action] = child
                node = child
                depth += 1
                if is_profitable_state(data, new_state):
                    best = Discovery(budget.used, _path_to(node))

            # Rollout: uniform random from `node.state`, no shaping.
            reward = 1.0 if is_profitable_state(data, node.state) else 0.0
            rollout_state = node.state
            rollout_extra: List[Action] = []
            d = depth
            while reward == 0.0 and d < max_depth and budget.remaining():
                actions = legal_actions(data, rollout_state)
                if not actions:
                    break
                a = rng.choice(actions)
                rollout_state = budget.step(data, rollout_state, a)
                rollout_extra.append(a)
                d += 1
                if is_profitable_state(data, rollout_state):
                    reward = 1.0

            if reward == 1.0 and best is None:
                best = Discovery(budget.used, _path_to(node) + rollout_extra)

            # Backpropagation
            n: Optional[_Node] = node
            while n is not None:
                n.visits += 1
                n.reward += reward
                n = n.parent
    except BudgetExhausted:
        pass
    return best
