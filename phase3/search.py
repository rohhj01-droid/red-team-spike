"""C1 search algorithms: Random, Beam-Naive, Beam-Diverse, MCTS.

Ported from phase2/search.py's structure, adapted for
SearchState = (WorldState, MonitorState). Visibility rules from
DESIGN_C1.md are enforced by construction, not just convention:
score()/behavior_descriptor()/random and UCT policy selection all take
WorldState only -- they are never passed a MonitorState, so they cannot
leak it even by accident. Dedup (Beam's candidates dict) and reward
(MCTS backprop, both algorithms' online is_exploit check) use the full
SearchState, per SEARCH_CONTRACT_C1.md.

Same discipline as Phase 2: four independent functions, no shared
SearchStrategy interface -- Random/Beam/MCTS control flow still doesn't
match closely enough to be worth unifying.
"""
from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from budget import Budget, BudgetExhausted
from engine import Action, WorldState, initial_world, legal_actions
from monitor import MonitorState, initial_monitor, monitor_step
from oracle import is_exploit

SearchState = Tuple[WorldState, MonitorState]


@dataclass
class Discovery:
    cost: int
    path: List[Action]


def score(world: WorldState) -> float:
    return {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status]


def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(kind_counts.get(k, 0) / path_len for k in ("equip", "accept", "claim"))
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)


def _step(budget: Budget, world: WorldState, monitor: MonitorState, action: Action) -> Tuple[WorldState, MonitorState]:
    new_world = budget.step(world, action)
    new_monitor = monitor_step(world, action, new_world, monitor)
    return new_world, new_monitor


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


# ---------------------------------------------------------------------------
# Random
# ---------------------------------------------------------------------------

def random_search(seed: int, budget_limit: int, max_depth: int) -> Optional[Discovery]:
    rng = random.Random(seed)
    budget = Budget(budget_limit)
    start_world, start_monitor = initial_world(), initial_monitor()
    try:
        while budget.remaining():
            world, monitor = start_world, start_monitor
            path: List[Action] = []
            for _ in range(max_depth):
                actions = legal_actions(world)
                if not actions:
                    break
                action = rng.choice(actions)
                world, monitor = _step(budget, world, monitor, action)
                path.append(action)
                if is_exploit(world, monitor):
                    return Discovery(budget.used, path)
                if not budget.remaining():
                    break
    except BudgetExhausted:
        pass
    return None


# ---------------------------------------------------------------------------
# Beam-Naive / Beam-Diverse
# ---------------------------------------------------------------------------

def beam_naive_search(budget_limit: int, max_depth: int, beam_width: int) -> Optional[Discovery]:
    budget = Budget(budget_limit)
    start: SearchState = (initial_world(), initial_monitor())
    beam: List[Tuple[SearchState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[SearchState, Tuple[float, List[Action]]] = {}
            for (world, monitor), path in beam:
                if not budget.remaining():
                    break
                for action in legal_actions(world):
                    if not budget.remaining():
                        break
                    new_world, new_monitor = _step(budget, world, monitor, action)
                    new_state = (new_world, new_monitor)
                    new_path = path + [action]
                    if is_exploit(new_world, new_monitor):
                        return Discovery(budget.used, new_path)
                    existing = candidates.get(new_state)
                    if existing is None or len(new_path) < len(existing[1]):
                        candidates[new_state] = (score(new_world), new_path)
            ranked = sorted(candidates.items(), key=lambda kv: kv[1][0], reverse=True)
            beam = [(s, p) for s, (_, p) in ranked[:beam_width]]
    except BudgetExhausted:
        pass
    return None


def beam_diverse_search(
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
                if not budget.remaining():
                    break
                for action in legal_actions(world):
                    if not budget.remaining():
                        break
                    new_world, new_monitor = _step(budget, world, monitor, action)
                    new_state = (new_world, new_monitor)
                    new_path = path + [action]
                    if is_exploit(new_world, new_monitor):
                        return Discovery(budget.used, new_path)
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


# ---------------------------------------------------------------------------
# MCTS -- textbook UCT, binary first-hit reward, uniform-random rollout.
# ---------------------------------------------------------------------------

UCT_C = math.sqrt(2)  # inert under first-hit reward -- see SEARCH_CONTRACT_C1.md


class _Node:
    __slots__ = ("state", "parent", "action_from_parent", "children", "untried", "visits", "reward")

    def __init__(self, state: SearchState, parent: Optional["_Node"], action_from_parent: Optional[Action], untried: List[Action]):
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


def mcts_search(seed: int, budget_limit: int, max_depth: int, c: float = UCT_C) -> Optional[Discovery]:
    rng = random.Random(seed)
    budget = Budget(budget_limit)
    start_state: SearchState = (initial_world(), initial_monitor())
    root = _Node(start_state, None, None, legal_actions(start_state[0]))
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
                world, monitor = node.state
                new_world, new_monitor = _step(budget, world, monitor, action)
                new_state: SearchState = (new_world, new_monitor)
                child = _Node(new_state, node, action, legal_actions(new_world))
                node.children[action] = child
                node = child
                depth += 1
                if is_exploit(new_world, new_monitor):
                    best = Discovery(budget.used, _path_to(node))

            # Rollout: uniform random, no shaping.
            reward = 1.0 if is_exploit(*node.state) else 0.0
            rollout_world, rollout_monitor = node.state
            rollout_extra: List[Action] = []
            d = depth
            while reward == 0.0 and d < max_depth and budget.remaining():
                actions = legal_actions(rollout_world)
                if not actions:
                    break
                a = rng.choice(actions)
                rollout_world, rollout_monitor = _step(budget, rollout_world, rollout_monitor, a)
                rollout_extra.append(a)
                d += 1
                if is_exploit(rollout_world, rollout_monitor):
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
