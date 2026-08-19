# C2 Search Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port Random/Beam-Naive/Beam-Diverse/MCTS search into `phase3/c2/`, wired to the transition-based oracle (C2c), and prove the wiring is correct via an integration runner -- architecture/integration evidence only, no algorithm-comparison verdict.

**Architecture:** Direct structural port of `phase3/search.py` (C1), with every discovery check replaced by a single shared `_step()` helper that computes `classify_claim(action, monitor)` from the **pre-transition** `monitor` argument (never `new_monitor`) inside the same function that calls `Budget.step()` -- this makes the invocation-order rule from `SEARCH_CONTRACT_C2.md` correct by construction instead of relying on four independent call sites to each remember it. `Discovery` gains a `classification` field. `behavior_descriptor()` gets a `channel` ratio; `score()` is untouched.

**Tech Stack:** Python 3, stdlib only (`math`, `random`, `dataclasses`, `collections.Counter`, `typing`) -- same as C1, no new dependencies.

**Spec:** [phase3/SEARCH_CONTRACT_C2.md](../../../phase3/SEARCH_CONTRACT_C2.md) (sealed `9cd676c`), [phase3/DESIGN_C2.md](../../../phase3/DESIGN_C2.md) (C2c oracle correction, sealed `071f397`)

## Global Constraints

- Frozen parameters, reused unchanged from C1, not re-tuned: `MAX_DEPTH=15`, `BUDGET=1000`, `BEAM_WIDTH=5`, `NOVELTY_WEIGHT=1`, `NOVELTY_K=4`, `SEEDS=range(10)`, `MCTS_C=sqrt(2)`.
- `score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]` -- unchanged from C1, `has_flame_buff` excluded.
- `behavior_descriptor()` -- 6 dims: `equip`/`accept`/`channel`/`claim` action ratios + quest ordinal + path fraction. `MonitorState` and `has_flame_buff` excluded.
- `score()`/`behavior_descriptor()` must have no `monitor` parameter in their signatures at all (checked by `inspect.signature`, not convention).
- Oracle invocation order (the core of `SEARCH_CONTRACT_C2.md`): `Budget.step()` executes the action first; `classify_claim(action, prev_monitor)` is then evaluated using the monitor value from **before** that step, never `new_monitor`. The check happens before any dedup/ranking/pruning (Beam) and before backprop (MCTS).
- `Discovery.cost` includes the triggering `claim` transition -- guaranteed by construction since `Budget.step()` runs inside the same `_step()` call that computes the classification.
- No result table ranks the four algorithms against each other. Only pass/fail + found-witness-count are reported.
- C1's files (`phase3/*.py`) are not imported from and not modified -- C2 duplicates the small shared shapes, same as `phase3/c2`'s existing engine/monitor/oracle/qa_reference.

---

## File Structure

- Create: `phase3/c2/budget.py` -- `Budget`/`BudgetExhausted`, direct port of `phase3/budget.py` repointed to `phase3/c2/engine.py`.
- Create: `phase3/c2/search.py` -- `Discovery`, `score`, `behavior_descriptor`, `_step` (the shared pre-transition-monitor helper), `random_search`, `beam_naive_search`, `beam_diverse_search`, `mcts_search`.
- Create: `phase3/c2/run_c2_integration.py` -- visibility-by-construction check + per-algorithm pass/fail + independent classification re-check at replay.

---

### Task 1: `phase3/c2/budget.py`

**Files:**
- Create: `phase3/c2/budget.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.WorldState`, `engine.apply` (from `phase3/c2/engine.py`, already committed in `6aab686`)
- Produces: `Budget(limit: int, used: int = 0)` with `.remaining() -> bool` and `.step(world, action) -> WorldState`; `BudgetExhausted` exception. Both consumed by Task 2.

- [ ] **Step 1: Write the file**

```python
"""The only sanctioned way to advance WorldState during search. Ported
from phase3/budget.py (C1), import repointed to phase3/c2/engine.py --
C1 is sealed evidence, C2 doesn't import from it.
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

Run (from `phase3/c2/`):
```bash
python -c "from budget import Budget; b = Budget(2); print(b.remaining()); b.used = 2; print(b.remaining())"
```
Expected output:
```
True
False
```

No commit yet -- committed together with Tasks 2-3 at the end (matches C1's `9ec6249`, a single commit for the whole search port + integration test).

---

### Task 2: `phase3/c2/search.py`

**Files:**
- Create: `phase3/c2/search.py`

**Interfaces:**
- Consumes: `budget.Budget`, `budget.BudgetExhausted` (Task 1); `engine.Action`, `engine.WorldState`, `engine.initial_world`, `engine.legal_actions` (committed); `monitor.MonitorState`, `monitor.initial_monitor`, `monitor.monitor_step` (committed); `oracle.classify_claim` (committed, C2c signature: `classify_claim(action: Action, prev_monitor: MonitorState) -> Optional[str]`).
- Produces: `Discovery(cost: int, path: List[Action], classification: str)`; `score(world) -> float`; `behavior_descriptor(world, path, max_depth) -> Tuple[float, ...]`; `random_search(seed, budget_limit, max_depth) -> Optional[Discovery]`; `beam_naive_search(budget_limit, max_depth, beam_width) -> Optional[Discovery]`; `beam_diverse_search(budget_limit, max_depth, beam_width, novelty_k=4, novelty_weight=1.0) -> Optional[Discovery]`; `mcts_search(seed, budget_limit, max_depth, c=UCT_C) -> Optional[Discovery]`. All consumed by Task 3.

- [ ] **Step 1: Write the file**

```python
"""C2 search algorithms: Random, Beam-Naive, Beam-Diverse, MCTS.

Ported from phase3/search.py's structure (C1), adapted for C2c's
transition-based oracle. The one structural change from C1: every
discovery check now goes through `_step()`, which computes
`classify_claim(action, monitor)` from the PRE-transition `monitor`
argument, inside the same call that runs `Budget.step()`. Per
SEARCH_CONTRACT_C2.md, checking `classify_claim(action, new_monitor)`
instead would be a real contract violation that today's specific
monitor_step (claim doesn't touch either bit) would NOT surface as a
test failure -- folding the check into one shared helper, rather than
trusting four independent call sites to each thread `monitor` and not
`new_monitor`, makes the correct order the only order that compiles
into a call.

Same discipline as C1: four independent search functions, no shared
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
    action_ratio = tuple(kind_counts.get(k, 0) / path_len for k in ("equip", "accept", "channel", "claim"))
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)


def _step(budget: Budget, world: WorldState, monitor: MonitorState, action: Action) -> Tuple[WorldState, MonitorState, Optional[str]]:
    """Returns (new_world, new_monitor, classification). `classification`
    is computed from `monitor` -- the pre-transition value -- per C2c and
    SEARCH_CONTRACT_C2.md's invocation-order rule. Must never read
    `new_monitor` here, even though claim happens not to change either
    bit today."""
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

UCT_C = math.sqrt(2)  # inert under first-hit reward -- see SEARCH_CONTRACT_C2.md


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

Run (from `phase3/c2/`):
```bash
python -c "
from search import random_search, beam_naive_search, beam_diverse_search, mcts_search
print('random:', random_search(0, 1000, 15))
print('beam_naive:', beam_naive_search(1000, 15, 5))
print('beam_diverse:', beam_diverse_search(1000, 15, 5))
print('mcts:', mcts_search(0, 1000, 15))
"
```
Expected: all four print a `Discovery(cost=..., path=[...], classification='EQUIPMENT_CONTINUITY_VIOLATION' | 'BUFF_SOURCE_LIFECYCLE_VIOLATION' | 'BOTH')` -- not `None`, and not a crash. The specific classification found is not asserted here (that's Task 3's job, with independent replay); this step only confirms the port runs end-to-end.

No commit yet -- see Task 3.

---

### Task 3: `phase3/c2/run_c2_integration.py`

**Files:**
- Create: `phase3/c2/run_c2_integration.py`

**Interfaces:**
- Consumes: everything Task 2 produces, plus `engine.apply`, `engine.initial_world`, `engine.legal_actions`, `monitor.initial_monitor`, `monitor.monitor_step`, `oracle.classify_claim` (all already committed or from Task 2).
- Produces: a runnable script with no importable symbols other consumers need (terminal node of this plan).

- [ ] **Step 1: Write the file**

```python
"""C2 search integration test. Per SEARCH_CONTRACT_C2.md's interpretation
rule: reports PASS/FAIL per algorithm (found a witness + witness replays
legally + independently-recomputed classification at the actual claim
transition matches what search recorded), never a comparison table.

Run:
    python run_c2_integration.py
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
    print("C2 SEARCH INTEGRATION: " + ("PASS" if overall else "FAIL"))
```

- [ ] **Step 2: Run it**

Run (from `phase3/c2/`):
```bash
python run_c2_integration.py
```
Expected: every check line prints `PASS`, ending with `C2 SEARCH INTEGRATION: PASS`. If anything prints `FAIL`, stop and diagnose before proceeding -- do not edit the checker to make a failure disappear; a `FAIL` here means either the port has a bug or `SEARCH_CONTRACT_C2.md` itself needs another reviewed correction (same discipline as the C2c finding).

- [ ] **Step 3: Re-run core QA to confirm no drift**

Run (from `phase3/c2/`):
```bash
python verify_c2.py
```
Expected: `C2 QA: PASS`, identical to the result already recorded in commit `6aab686` -- this task must not have touched `engine.py`/`monitor.py`/`oracle.py`/`qa_reference.py`/`verify_c2.py`.

- [ ] **Step 4: Confirm C1 untouched**

Run (from repo root):
```bash
git status --short phase3/*.py phase3/c2/
```
Expected: only new files under `phase3/c2/` (`budget.py`, `search.py`, `run_c2_integration.py`); no modifications to `phase3/*.py` (C1's sealed files).

- [ ] **Step 5: Commit**

```bash
git add phase3/c2/budget.py phase3/c2/search.py phase3/c2/run_c2_integration.py
git commit -m "Phase 3 C2: search algorithms ported + integration test, PASS"
```

(Full commit message with actual observed numbers -- found-witness counts per algorithm, visibility check result -- to be filled in from the real Step 2 output before committing, same convention as C1's `9ec6249`.)

---

## Self-Review Notes

- **Spec coverage:** Oracle invocation order (Global Constraints + `_step()`) / Discovery classification field (Task 2) / descriptor 6-dim + no-monitor-param (Task 2 + Task 3 Step 1) / frozen params reused (Task 3 constants) / no comparison table (Task 3 print structure) / event-check-before-dedup for Beam (Task 2, classification checked before `candidates` dict write) / MCTS expansion+rollout event-checked (Task 2) -- all covered.
- **Placeholder scan:** none -- every step has runnable code and a concrete expected-output description.
- **Type consistency:** `Discovery(cost: int, path: List[Action], classification: str)` used identically in Task 2's construction sites and Task 3's `discovery.classification` reads. `_step()`'s `Tuple[WorldState, MonitorState, Optional[str]]` return is unpacked identically in all four search functions.
