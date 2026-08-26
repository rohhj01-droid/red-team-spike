# C3 Search Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port Random/Beam-Naive/Beam-Diverse/MCTS search into `phase3/c3/`, wired to C3's (unchanged-from-C2c) transition-based oracle, and prove the wiring is correct via an integration runner -- architecture/integration evidence only, no algorithm-comparison verdict, no pathway attribution.

**Architecture:** Structural port of `phase3/c2/{budget,search}.py`. Since `classify_claim`'s signature and the `_step()` invocation-order pattern are byte-for-byte unchanged from C2c, `SearchState = Tuple[WorldState, MonitorState]` stays fully opaque to search -- `MonitorState` gaining a third field (`enchant_broken`) requires zero logic changes anywhere in `search.py` except `behavior_descriptor()`, which grows from 6 to 8 dimensions per `SEARCH_CONTRACT_C3.md`.

**Tech Stack:** Python 3, stdlib only (`math`, `random`, `dataclasses`, `collections.Counter`, `typing`) -- same as C1/C2, no new dependencies.

**Spec:** [phase3/SEARCH_CONTRACT_C3.md](../../../phase3/SEARCH_CONTRACT_C3.md) (sealed `093a2cf`), [phase3/DESIGN_C3.md](../../../phase3/DESIGN_C3.md) (sealed through C3c, `8d10071`)

## Global Constraints

- Frozen parameters, reused unchanged from C1/C2, not re-tuned: `MAX_DEPTH=15`, `BUDGET=1000`, `BEAM_WIDTH=5`, `NOVELTY_WEIGHT=1`, `NOVELTY_K=4`, `SEEDS=range(10)`, `MCTS_C=sqrt(2)`.
- `score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]` -- unchanged, `has_flame_buff`/`enchanted` excluded.
- `behavior_descriptor()` -- 8 dims: `equip`/`accept`/`enchant`/`unenchant`/`channel`/`claim` action ratios (in that order) + quest ordinal + path fraction. `MonitorState` and `enchanted` excluded.
- `score()`/`behavior_descriptor()` must have no `monitor` parameter in their signatures at all (checked by `inspect.signature`).
- Oracle invocation order (byte-for-byte from `SEARCH_CONTRACT_C2.md`, restated in `SEARCH_CONTRACT_C3.md`): `Budget.step()` executes the action first; `classify_claim(action, prev_monitor)` is evaluated using the monitor value from **before** that step, never `new_monitor`. Checked before any dedup/ranking/pruning (Beam) and before backprop (MCTS).
- `Discovery.cost` includes the triggering `claim` transition -- guaranteed by construction via a shared `_step()` helper, same pattern as C2.
- `Discovery` stays `(cost, path, classification)` -- **not** extended with `classify_pathway`. That predicate is QA-only (lives in `verify_c3.py`), a deliberate scope decision sealed in `SEARCH_CONTRACT_C3.md`, not something for this plan to add.
- No result table ranks the four algorithms against each other.
- C1's and C2's files (`phase3/*.py`, `phase3/c2/*.py`) are not imported from and not modified.

---

## File Structure

- Create: `phase3/c3/budget.py` -- `Budget`/`BudgetExhausted`, direct port of `phase3/c2/budget.py` repointed to `phase3/c3/engine.py`.
- Create: `phase3/c3/search.py` -- `Discovery`, `score`, `behavior_descriptor` (8-dim), `_step`, `random_search`, `beam_naive_search`, `beam_diverse_search`, `mcts_search`.
- Create: `phase3/c3/run_c3_integration.py` -- visibility-by-construction check + per-algorithm pass/fail + independent classification re-check at replay.

---

### Task 1: `phase3/c3/budget.py`

**Files:**
- Create: `phase3/c3/budget.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.WorldState`, `engine.apply` (from `phase3/c3/engine.py`, already committed in `2441a86`).
- Produces: `Budget(limit: int, used: int = 0)` with `.remaining() -> bool` and `.step(world, action) -> WorldState`; `BudgetExhausted` exception. Consumed by Task 2.

- [ ] **Step 1: Write the file**

```python
"""The only sanctioned way to advance WorldState during search. Ported
from phase3/c2/budget.py, import repointed to phase3/c3/engine.py -- C1
and C2 are sealed evidence, C3 doesn't import from either.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, WorldState, apply


class BudgetExhausted(Exception):
    pass


@dataclass
class Budget:
    limit: int
    used: int = 0

    def remaining(self) -> bool:
        return self.used < self.limit

    def step(self, world: WorldState, action: Action) -> WorldState:
        if self.used >= self.limit:
            raise BudgetExhausted()
        self.used += 1
        return apply(world, action)
```

- [ ] **Step 2: Sanity-run it**

Run (from `phase3/c3/`):
```bash
python -c "from budget import Budget; b = Budget(2); print(b.remaining()); b.used = 2; print(b.remaining())"
```
Expected:
```
True
False
```

No commit yet -- committed together with Tasks 2-3 at the end (matches C1's `9ec6249` / C2's `0025e55` convention).

---

### Task 2: `phase3/c3/search.py`

**Files:**
- Create: `phase3/c3/search.py`

**Interfaces:**
- Consumes: `budget.Budget`, `budget.BudgetExhausted` (Task 1); `engine.Action`, `engine.WorldState`, `engine.initial_world`, `engine.legal_actions` (committed); `monitor.MonitorState`, `monitor.initial_monitor`, `monitor.monitor_step` (committed); `oracle.classify_claim` (committed).
- Produces: `Discovery(cost: int, path: List[Action], classification: str)`; `score(world) -> float`; `behavior_descriptor(world, path, max_depth) -> Tuple[float, ...]`; `random_search`, `beam_naive_search`, `beam_diverse_search`, `mcts_search` -- identical signatures to `phase3/c2/search.py`'s. Consumed by Task 3.

- [ ] **Step 1: Write the file**

```python
"""C3 search algorithms: Random, Beam-Naive, Beam-Diverse, MCTS.

Ported from phase3/c2/search.py -- classify_claim's signature and the
_step() invocation-order pattern are unchanged from C2c, so SearchState
stays fully opaque to search: MonitorState gaining a third field
(enchant_broken) requires no logic change here except
behavior_descriptor(), which grows to 8 dimensions per
SEARCH_CONTRACT_C3.md. classify_pathway is deliberately not used
anywhere in this file -- Discovery stays (cost, path, classification),
per that contract's explicit scope decision.

Same discipline as C1/C2: four independent search functions, no shared
SearchStrategy interface.
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
from oracle import classify_claim

SearchState = Tuple[WorldState, MonitorState]


@dataclass
class Discovery:
    cost: int
    path: List[Action]
    classification: str  # "EQUIPMENT_CONTINUITY_VIOLATION" | "BUFF_SOURCE_LIFECYCLE_VIOLATION" | "BOTH"


def score(world: WorldState) -> float:
    return {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status]


def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(
        kind_counts.get(k, 0) / path_len
        for k in ("equip", "accept", "enchant", "unenchant", "channel", "claim")
    )
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)


def _step(budget: Budget, world: WorldState, monitor: MonitorState, action: Action) -> Tuple[WorldState, MonitorState, Optional[str]]:
    """Returns (new_world, new_monitor, classification). `classification`
    is computed from `monitor` -- the pre-transition value -- per
    SEARCH_CONTRACT_C3.md's invocation-order rule. Must never read
    `new_monitor` here."""
    new_world = budget.step(world, action)
    new_monitor = monitor_step(world, action, new_world, monitor)
    classification = classify_claim(action, monitor) if action.kind == "claim" else None
    return new_world, new_monitor, classification


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
                world, monitor, classification = _step(budget, world, monitor, action)
                path.append(action)
                if classification is not None:
                    return Discovery(budget.used, path, classification)
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


# ---------------------------------------------------------------------------
# MCTS -- textbook UCT, binary first-hit reward, uniform-random rollout.
# ---------------------------------------------------------------------------

UCT_C = math.sqrt(2)  # inert under first-hit reward -- see SEARCH_CONTRACT_C3.md


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

            # Expansion. `classification` stays None if no expansion
            # happens this iteration -- any node already in the tree was
            # reached by a transition that provably didn't fire a
            # violation (otherwise `best` would already be set and the
            # loop would have stopped), so there is nothing to re-check.
            classification: Optional[str] = None
            if node.untried and depth < max_depth:
                action = rng.choice(node.untried)
                node.untried.remove(action)
                world, monitor = node.state
                new_world, new_monitor, classification = _step(budget, world, monitor, action)
                new_state: SearchState = (new_world, new_monitor)
                child = _Node(new_state, node, action, legal_actions(new_world))
                node.children[action] = child
                node = child
                depth += 1
                if classification is not None:
                    best = Discovery(budget.used, _path_to(node), classification)

            # Rollout: uniform random, no shaping.
            reward = 1.0 if classification is not None else 0.0
            rollout_world, rollout_monitor = node.state
            rollout_extra: List[Action] = []
            rollout_classification = classification
            d = depth
            while reward == 0.0 and d < max_depth and budget.remaining():
                actions = legal_actions(rollout_world)
                if not actions:
                    break
                a = rng.choice(actions)
                rollout_world, rollout_monitor, rollout_classification = _step(budget, rollout_world, rollout_monitor, a)
                rollout_extra.append(a)
                d += 1
                if rollout_classification is not None:
                    reward = 1.0

            if reward == 1.0 and best is None:
                best = Discovery(budget.used, _path_to(node) + rollout_extra, rollout_classification)

            # Backpropagation
            n: Optional[_Node] = node
            while n is not None:
                n.visits += 1
                n.reward += reward
                n = n.parent
    except BudgetExhausted:
        pass
    return best
```

- [ ] **Step 2: Sanity-run each algorithm once**

Run (from `phase3/c3/`):
```bash
python -c "
from search import random_search, beam_naive_search, beam_diverse_search, mcts_search
print('random:', random_search(0, 1000, 15))
print('beam_naive:', beam_naive_search(1000, 15, 5))
print('beam_diverse:', beam_diverse_search(1000, 15, 5))
print('mcts:', mcts_search(0, 1000, 15))
"
```
Expected: all four print a `Discovery(cost=..., path=[...], classification='EQUIPMENT_CONTINUITY_VIOLATION' | 'BUFF_SOURCE_LIFECYCLE_VIOLATION' | 'BOTH')` -- not `None`, not a crash. The specific classification found is not asserted here; Task 3 does the real replay-and-match check.

No commit yet -- see Task 3.

---

### Task 3: `phase3/c3/run_c3_integration.py`

**Files:**
- Create: `phase3/c3/run_c3_integration.py`

**Interfaces:**
- Consumes: everything Task 2 produces, plus `engine.apply`, `engine.initial_world`, `engine.legal_actions`, `monitor.initial_monitor`, `monitor.monitor_step`, `oracle.classify_claim`.
- Produces: a runnable script, terminal node of this plan.

- [ ] **Step 1: Write the file**

```python
"""C3 search integration test. Per SEARCH_CONTRACT_C3.md's interpretation
rule: reports PASS/FAIL per algorithm (found a witness + witness replays
legally + independently-recomputed classification at the actual claim
transition matches what search recorded), never a comparison table.
classify_pathway is intentionally not checked here -- Discovery doesn't
carry it, per SEARCH_CONTRACT_C3.md's explicit scope decision.

Run:
    python run_c3_integration.py
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
    print("C3 SEARCH INTEGRATION: " + ("PASS" if overall else "FAIL"))
```

- [ ] **Step 2: Run it**

Run (from `phase3/c3/`):
```bash
python run_c3_integration.py
```
Expected: every check line prints `PASS`, ending with `C3 SEARCH INTEGRATION: PASS`. If anything prints `FAIL`, stop and diagnose -- do not edit the checker to make a failure disappear.

- [ ] **Step 3: Re-run core QA to confirm no drift**

Run (from `phase3/c3/`):
```bash
python verify_c3.py
```
Expected: `C3 QA: PASS`, identical to the result already recorded in commit `2441a86` -- this task must not have touched `engine.py`/`monitor.py`/`oracle.py`/`qa_reference.py`/`verify_c3.py`.

- [ ] **Step 4: Confirm C1/C2/C3-core untouched**

Run (from repo root):
```bash
git status --short phase3/*.py phase3/c2/ phase3/c3/
```
Expected: only new files under `phase3/c3/` (`budget.py`, `search.py`, `run_c3_integration.py`); no modifications to `phase3/*.py` (C1), `phase3/c2/*.py` (C2), or C3's already-committed core files.

- [ ] **Step 5: Commit**

```bash
git add phase3/c3/budget.py phase3/c3/search.py phase3/c3/run_c3_integration.py
git commit -m "Phase 3 C3: search algorithms ported + integration test, PASS"
```

(Full commit message with actual observed numbers -- found-witness counts per algorithm, visibility check result -- to be filled in from the real Step 2 output before committing, same convention as C1's `9ec6249` and C2's `0025e55`.)

---

## Self-Review Notes

- **Spec coverage:** oracle invocation order via shared `_step()` (Task 2) / `Discovery` unextended, no pathway (Task 2, Task 3 docstring) / descriptor 8-dim + no-monitor-param (Task 2, Task 3 Step 1) / frozen params reused (Task 3 constants) / no comparison table (Task 3 print structure) / event-check-before-dedup for Beam, event-checked expansion+rollout for MCTS (Task 2, ported unchanged from C2) -- all covered.
- **Placeholder scan:** none -- every step has runnable code and a concrete expected-output description.
- **Type consistency:** `Discovery(cost: int, path: List[Action], classification: str)` used identically in Task 2's construction sites and Task 3's `discovery.classification` reads. `_step()`'s `Tuple[WorldState, MonitorState, Optional[str]]` return unpacked identically in all four search functions.
