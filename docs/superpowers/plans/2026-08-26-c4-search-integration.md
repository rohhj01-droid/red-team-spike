# C4 Search Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port Random/Beam-Naive/Beam-Diverse/MCTS search into `phase3/c4/`, wired to the exact `_step()` pipeline and consume-only discovery rule sealed in `SEARCH_CONTRACT_C4.md`, and prove the wiring correct via an integration runner -- architecture/integration evidence only, no algorithm-comparison verdict.

**Architecture:** Structural port of `phase3/c3/search.py` -- the *official* file (`ecbd536`), never `phase3/c3/diagnostic_claimed_terminal.py`. `SearchState` grows from C3's 2-tuple to a 3-tuple `(WorldState, MonitorState, EventProvenanceState)`. `_step()` computes `classify_claim` internally (to feed `event_provenance_step`) but deliberately never returns it -- callers can only ever see `consume_verdict`, making the wrong discovery condition (`claim_verdict is not None or ...`) impossible to write, not just documented as wrong. No `quest_status == "CLAIMED"` skip/continue logic anywhere -- C4's target is only reachable *past* `CLAIMED`.

**Tech Stack:** Python 3, stdlib only (`math`, `random`, `dataclasses`, `collections.Counter`, `typing`) -- same as C1-C3, no new dependencies.

**Spec:** [phase3/SEARCH_CONTRACT_C4.md](../../../phase3/SEARCH_CONTRACT_C4.md) (sealed `61f6d77`), [phase3/DESIGN_C4.md](../../../phase3/DESIGN_C4.md) (sealed through C4b, `d7ca12e`)

## Global Constraints

- Frozen parameters, reused unchanged from C1-C3, not re-tuned: `MAX_DEPTH=15`, `BUDGET=1000`, `BEAM_WIDTH=5`, `NOVELTY_WEIGHT=1`, `NOVELTY_K=4`, `SEEDS=range(10)`, `MCTS_C=sqrt(2)`.
- `score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]` -- unchanged, `reward_owned` excluded.
- `behavior_descriptor()` -- 7 dims: `equip`/`accept`/`channel`/`claim`/`consume` action ratios (`consume` appended at the end, C4's new terminal action) + quest ordinal + path fraction. `MonitorState`, `EventProvenanceState` excluded.
- `score()`/`behavior_descriptor()` must have no `monitor` or `provenance` parameter in their signatures at all.
- `_step()`'s exact pipeline (`SEARCH_CONTRACT_C4.md`): `Budget.step` -> `monitor_step` -> `classify_claim` -> `classify_consume` -> `event_provenance_step`, in that order. `classify_consume` reads `prev_provenance`, never `new_provenance`. `_step()` returns `(new_world, new_monitor, new_provenance, consume_verdict)` -- `claim_verdict` is computed internally and never returned.
- `Discovery` stays `(cost, path, classification)`; `classification` is always `"TAINTED_REWARD_CONSUMPTION"` when non-`None` (the only value `classify_consume` can return).
- **No `quest_status == "CLAIMED"` expansion-skipping anywhere in `search.py`** -- checked by inspection before every commit, not just by run outcome.
- No result table ranks the four algorithms against each other.
- C1's, C2's, and C3's files are not imported from and not modified.

**Forbidden-pattern self-review checklist** (run against the diff before committing, per the design-review discussion that produced this plan):
- [ ] `claim_verdict` returned from `_step()`? -- must not be.
- [ ] `if claim_verdict ...` anywhere in `search.py`/`run_c4_integration.py`? -- must not be.
- [ ] `quest_status == "CLAIMED"` combined with `continue`/`break`/`skip`? -- must not be.
- [ ] Any import of or reference to `diagnostic_claimed_terminal`? -- must not be.
- [ ] `MonitorState` or `EventProvenanceState` appearing in `score`/`behavior_descriptor`'s signature? -- must not be.

---

## File Structure

- Create: `phase3/c4/budget.py` -- `Budget`/`BudgetExhausted`, direct port of `phase3/c3/budget.py` repointed to `phase3/c4/engine.py`.
- Create: `phase3/c4/search.py` -- `Discovery`, `score`, `behavior_descriptor`, `_step`, `random_search`, `beam_naive_search`, `beam_diverse_search`, `mcts_search`.
- Create: `phase3/c4/run_c4_integration.py` -- visibility-by-construction check + per-algorithm pass/fail + independent classification re-check at replay + exactly-one-`claim` structural check.

---

### Task 1: `phase3/c4/budget.py`

**Files:**
- Create: `phase3/c4/budget.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.WorldState`, `engine.apply` (from `phase3/c4/engine.py`, already committed in `ab4a28c`).
- Produces: `Budget(limit: int, used: int = 0)` with `.remaining() -> bool` and `.step(world, action) -> WorldState`; `BudgetExhausted`. Consumed by Task 2.

- [ ] **Step 1: Write the file**

```python
"""The only sanctioned way to advance WorldState during search. Ported
from phase3/c3/budget.py, import repointed to phase3/c4/engine.py -- C1,
C2, and C3 are sealed evidence, C4 doesn't import from any of them.
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

Run (from `phase3/c4/`):
```bash
python -c "from budget import Budget; b = Budget(2); print(b.remaining()); b.used = 2; print(b.remaining())"
```
Expected:
```
True
False
```

No commit yet -- committed together with Tasks 2-3 at the end (matches C1's `9ec6249` / C2's `0025e55` / C3's `ecbd536` convention).

---

### Task 2: `phase3/c4/search.py`

**Files:**
- Create: `phase3/c4/search.py`

**Interfaces:**
- Consumes: `budget.Budget`, `budget.BudgetExhausted` (Task 1); `engine.Action`, `engine.WorldState`, `engine.initial_world`, `engine.legal_actions` (committed); `monitor.MonitorState`, `monitor.initial_monitor`, `monitor.monitor_step` (committed); `event_provenance.EventProvenanceState`, `event_provenance.initial_event_provenance`, `event_provenance.event_provenance_step` (committed); `oracle.classify_claim`, `oracle.classify_consume` (committed).
- Produces: `Discovery(cost: int, path: List[Action], classification: str)`; `score(world) -> float`; `behavior_descriptor(world, path, max_depth) -> Tuple[float, ...]`; `random_search`, `beam_naive_search`, `beam_diverse_search`, `mcts_search` -- same signatures as `phase3/c3/search.py`'s. Consumed by Task 3.

- [ ] **Step 1: Write the file**

```python
"""C4 search algorithms: Random, Beam-Naive, Beam-Diverse, MCTS.

Ported from phase3/c3/search.py -- the OFFICIAL file (ecbd536), never
phase3/c3/diagnostic_claimed_terminal.py (SEARCH_CONTRACT_C4.md). Two
structural changes from C3: SearchState grows to a 3-tuple with
EventProvenanceState, and _step() computes classify_claim internally
(to feed event_provenance_step) but never returns it -- discovery is
consume_verdict-only, and this makes the wrong check impossible to
write, not just documented as wrong. No quest_status == "CLAIMED"
skip/continue logic anywhere in this file -- C4's target
(TAINTED_REWARD_CONSUMPTION) is only reachable past CLAIMED.

Same discipline as C1-C3: four independent search functions, no shared
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
from event_provenance import EventProvenanceState, event_provenance_step, initial_event_provenance
from monitor import MonitorState, initial_monitor, monitor_step
from oracle import classify_claim, classify_consume

SearchState = Tuple[WorldState, MonitorState, EventProvenanceState]


@dataclass
class Discovery:
    cost: int
    path: List[Action]
    classification: str  # "TAINTED_REWARD_CONSUMPTION" -- the only value classify_consume can return


def score(world: WorldState) -> float:
    return {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status]


def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(
        kind_counts.get(k, 0) / path_len
        for k in ("equip", "accept", "channel", "claim", "consume")
    )
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)


def _step(budget: Budget, world: WorldState, monitor: MonitorState, provenance: EventProvenanceState, action: Action) -> Tuple[WorldState, MonitorState, EventProvenanceState, Optional[str]]:
    """Returns (new_world, new_monitor, new_provenance, consume_verdict).
    claim_verdict is computed here (to feed event_provenance_step) but
    deliberately never returned -- per SEARCH_CONTRACT_C4.md, a caller
    cannot check it even by accident."""
    new_world = budget.step(world, action)
    new_monitor = monitor_step(world, action, new_world, monitor)
    claim_verdict = classify_claim(action, monitor)
    consume_verdict = classify_consume(action, provenance)
    new_provenance = event_provenance_step(action, claim_verdict, provenance)
    return new_world, new_monitor, new_provenance, consume_verdict


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
    start_world, start_monitor, start_provenance = initial_world(), initial_monitor(), initial_event_provenance()
    try:
        while budget.remaining():
            world, monitor, provenance = start_world, start_monitor, start_provenance
            path: List[Action] = []
            for _ in range(max_depth):
                actions = legal_actions(world)
                if not actions:
                    break
                action = rng.choice(actions)
                world, monitor, provenance, consume_verdict = _step(budget, world, monitor, provenance, action)
                path.append(action)
                if consume_verdict is not None:
                    return Discovery(budget.used, path, consume_verdict)
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
    start: SearchState = (initial_world(), initial_monitor(), initial_event_provenance())
    beam: List[Tuple[SearchState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[SearchState, Tuple[float, List[Action]]] = {}
            for (world, monitor, provenance), path in beam:
                if not budget.remaining():
                    break
                for action in legal_actions(world):
                    if not budget.remaining():
                        break
                    new_world, new_monitor, new_provenance, consume_verdict = _step(budget, world, monitor, provenance, action)
                    new_state = (new_world, new_monitor, new_provenance)
                    new_path = path + [action]
                    if consume_verdict is not None:
                        return Discovery(budget.used, new_path, consume_verdict)
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
    start: SearchState = (initial_world(), initial_monitor(), initial_event_provenance())
    beam: List[Tuple[SearchState, List[Action]]] = [(start, [])]
    try:
        for _ in range(max_depth):
            if not beam or not budget.remaining():
                break
            candidates: Dict[SearchState, Tuple[float, List[Action]]] = {}
            for (world, monitor, provenance), path in beam:
                if not budget.remaining():
                    break
                for action in legal_actions(world):
                    if not budget.remaining():
                        break
                    new_world, new_monitor, new_provenance, consume_verdict = _step(budget, world, monitor, provenance, action)
                    new_state = (new_world, new_monitor, new_provenance)
                    new_path = path + [action]
                    if consume_verdict is not None:
                        return Discovery(budget.used, new_path, consume_verdict)
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

UCT_C = math.sqrt(2)  # inert under first-hit reward -- see SEARCH_CONTRACT_C4.md


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
    start_state: SearchState = (initial_world(), initial_monitor(), initial_event_provenance())
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

            # Expansion. consume_verdict stays None if no expansion
            # happens this iteration -- any node already in the tree was
            # reached by a transition that provably didn't fire a
            # discovery (otherwise `best` would already be set and the
            # loop would have stopped), so there is nothing to re-check.
            consume_verdict: Optional[str] = None
            if node.untried and depth < max_depth:
                action = rng.choice(node.untried)
                node.untried.remove(action)
                world, monitor, provenance = node.state
                new_world, new_monitor, new_provenance, consume_verdict = _step(budget, world, monitor, provenance, action)
                new_state: SearchState = (new_world, new_monitor, new_provenance)
                child = _Node(new_state, node, action, legal_actions(new_world))
                node.children[action] = child
                node = child
                depth += 1
                if consume_verdict is not None:
                    best = Discovery(budget.used, _path_to(node), consume_verdict)

            # Rollout: uniform random, no shaping.
            reward = 1.0 if consume_verdict is not None else 0.0
            rollout_world, rollout_monitor, rollout_provenance = node.state
            rollout_extra: List[Action] = []
            rollout_verdict = consume_verdict
            d = depth
            while reward == 0.0 and d < max_depth and budget.remaining():
                actions = legal_actions(rollout_world)
                if not actions:
                    break
                a = rng.choice(actions)
                rollout_world, rollout_monitor, rollout_provenance, rollout_verdict = _step(budget, rollout_world, rollout_monitor, rollout_provenance, a)
                rollout_extra.append(a)
                d += 1
                if rollout_verdict is not None:
                    reward = 1.0

            if reward == 1.0 and best is None:
                best = Discovery(budget.used, _path_to(node) + rollout_extra, rollout_verdict)

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

Run (from `phase3/c4/`):
```bash
python -c "
from search import random_search, beam_naive_search, beam_diverse_search, mcts_search
print('random:', random_search(0, 1000, 15))
print('beam_naive:', beam_naive_search(1000, 15, 5))
print('beam_diverse:', beam_diverse_search(1000, 15, 5))
print('mcts:', mcts_search(0, 1000, 15))
"
```
Expected: all four print a `Discovery(cost=..., path=[...], classification='TAINTED_REWARD_CONSUMPTION')` -- not `None`, not a crash. Task 3 does the real replay-and-match check.

No commit yet -- see Task 3.

---

### Task 3: `phase3/c4/run_c4_integration.py`

**Files:**
- Create: `phase3/c4/run_c4_integration.py`

**Interfaces:**
- Consumes: everything Task 2 produces, plus `engine.apply`, `engine.initial_world`, `engine.legal_actions`, `monitor.initial_monitor`, `monitor.monitor_step`, `event_provenance.initial_event_provenance`, `event_provenance.event_provenance_step`, `oracle.classify_claim`, `oracle.classify_consume`.
- Produces: a runnable script, terminal node of this plan.

- [ ] **Step 1: Write the file**

```python
"""C4 search integration test. Per SEARCH_CONTRACT_C4.md's interpretation
rule: reports PASS/FAIL per algorithm (found a witness + witness replays
legally + contains exactly one claim + independently-recomputed
classification at the actual consume transition matches what search
recorded), never a comparison table.

Run:
    python run_c4_integration.py
"""
from __future__ import annotations

import inspect

from engine import apply, initial_world, legal_actions
from event_provenance import event_provenance_step, initial_event_provenance
from monitor import initial_monitor, monitor_step
from oracle import classify_claim, classify_consume
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
    literally cannot accept MonitorState or EventProvenanceState -- their
    signatures have no parameter for either, not just "happen not to use
    it"."""
    score_params = set(inspect.signature(score).parameters)
    descriptor_params = set(inspect.signature(behavior_descriptor).parameters)
    forbidden = {"monitor", "provenance"}
    ok = not (forbidden & score_params) and not (forbidden & descriptor_params)
    print(f"  score() params: {score_params}")
    print(f"  behavior_descriptor() params: {descriptor_params}")
    print(f"  no MonitorState/EventProvenanceState parameter anywhere: {'PASS' if ok else 'FAIL'}")
    return ok


def replay_and_validate(discovery: Discovery) -> bool:
    """Legal replay; confirms exactly one claim occurs (structural sanity
    check that this is a genuine claim-then-consume chain); confirms
    classify_consume, recomputed at the actual consume transition,
    matches what search recorded."""
    world, monitor, provenance = initial_world(), initial_monitor(), initial_event_provenance()
    claim_count = 0
    reclassified = None
    for action in discovery.path:
        if action not in legal_actions(world):
            print(f"    FAIL: witness action {action} illegal at {world}")
            return False
        if action.kind == "claim":
            claim_count += 1
        if action.kind == "consume":
            reclassified = classify_consume(action, provenance)
        claim_verdict = classify_claim(action, monitor)
        new_world = apply(world, action)
        new_monitor = monitor_step(world, action, new_world, monitor)
        new_provenance = event_provenance_step(action, claim_verdict, provenance)
        world, monitor, provenance = new_world, new_monitor, new_provenance

    if claim_count != 1:
        print(f"    FAIL: witness contains {claim_count} claim actions, expected exactly 1")
        return False
    if reclassified is None:
        print(f"    FAIL: replayed witness never fires a discovering consume -- world={world}")
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
    print("C4 SEARCH INTEGRATION: " + ("PASS" if overall else "FAIL"))
```

- [ ] **Step 2: Run it**

Run (from `phase3/c4/`):
```bash
python run_c4_integration.py
```
Expected: every check line prints `PASS`, ending with `C4 SEARCH INTEGRATION: PASS`. If anything prints `FAIL`, stop and diagnose first -- per this project's established discipline (most recently exercised on C3's Beam failure), do not retune parameters or relax the checker to make a failure disappear. A genuine failure here is itself a result to seal and explain, not a bug to silently patch away.

- [ ] **Step 3: Re-run core QA to confirm no drift**

Run (from `phase3/c4/`):
```bash
python verify_c4.py
```
Expected: `C4 QA: PASS`, identical to the result already recorded in commit `ab4a28c` -- this task must not have touched `engine.py`/`monitor.py`/`event_provenance.py`/`oracle.py`/`qa_reference.py`/`verify_c4.py`.

- [ ] **Step 4: Run the forbidden-pattern self-review checklist**

Manually check the Global Constraints checklist above against the actual diff (`git diff --cached -- phase3/c4/search.py phase3/c4/run_c4_integration.py` after staging). Confirm each of the five items is absent. This is the "checked by inspection" requirement `SEARCH_CONTRACT_C4.md` specifically calls for -- not satisfied by Step 2 passing alone, since an algorithm finding nothing for an unrelated reason wouldn't surface a `CLAIMED`-pruning regression either.

- [ ] **Step 5: Confirm C1/C2/C3/C4-core untouched**

Run (from repo root):
```bash
git status --short phase3/*.py phase3/c2/ phase3/c3/ phase3/c4/
```
Expected: only new files under `phase3/c4/` (`budget.py`, `search.py`, `run_c4_integration.py`); no modifications to `phase3/*.py` (C1), `phase3/c2/*.py` (C2), `phase3/c3/*.py` (C3), or C4's already-committed core files.

- [ ] **Step 6: Commit**

```bash
git add phase3/c4/budget.py phase3/c4/search.py phase3/c4/run_c4_integration.py
git commit -m "Phase 3 C4: search algorithms ported + integration test, PASS"
```

(Full commit message with actual observed numbers -- found-witness counts per algorithm, visibility check result, confirmation the forbidden-pattern checklist was run -- to be filled in from the real Step 2 output before committing, same convention as C1's `9ec6249`/C2's `0025e55`/C3's `ecbd536`. If the result is a genuine FAIL like C3's was, seal it as observed and follow the same diagnose-separately discipline C3 used, not this plan's happy-path Step 6.)

---

## Self-Review Notes

- **Spec coverage:** exact `_step()` pipeline order + `claim_verdict` never returned (Task 2) / consume-only discovery check at every call site (Task 2, all four algorithms) / no `CLAIMED`-terminal pruning anywhere (Task 2, verified absent; Task 3 Step 4 re-checks) / port source is the official `phase3/c3/search.py` (Task 2 docstring) / full `SearchState` 3-tuple dedup and reward (Task 2) / descriptor 7-dim with `consume` appended (Task 2) / no-monitor/no-provenance-param visibility check (Task 3) / exactly-one-claim structural check (Task 3) / frozen params reused (Task 3 constants) / no comparison table (Task 3 print structure) -- all covered.
- **Placeholder scan:** none -- every step has runnable code and a concrete expected-output description.
- **Type consistency:** `Discovery(cost: int, path: List[Action], classification: str)` used identically in Task 2's four construction sites and Task 3's `discovery.classification` reads. `_step()`'s `Tuple[WorldState, MonitorState, EventProvenanceState, Optional[str]]` return unpacked identically in `random_search`/`beam_naive_search`/`beam_diverse_search`/MCTS's expansion and rollout call sites.
