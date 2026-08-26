# C4 Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `phase3/c4/{engine,monitor,event_provenance,oracle,qa_reference,verify_c4}.py` per `DESIGN_C4.md` (through C4b, `d7ca12e`) and get `verify_c4.py` to PASS -- core + QA only, no search.

**Architecture:** `engine.py`/`monitor.py` are C2c reused unchanged (extended only with `reward_owned`/`consume` in engine.py, matching DESIGN_C4.md's explicit reused/added split). `event_provenance.py` is a new, independent module -- `EventProvenanceState` is a third persistent data bucket, computed strictly after `classify_claim` has already run, never inside `monitor_step`, to avoid the circular-dependency/logic-duplication problem `DESIGN_C4.md` rejected two other ways of avoiding. `oracle.py` keeps `classify_claim` byte-for-byte and adds `classify_consume` as C4's actual search-target oracle. `verify_c4.py` runs one closure sweep with four independent production-vs-reference comparisons per transition (not four separate sweeps), plus a dedicated, explicit replay of the two hand-derived necessity-proof witnesses (P and Q) rather than relying on them to surface incidentally from the general sweep.

**Tech Stack:** Python 3, stdlib only (`dataclasses`, `typing`) -- same as C1-C3, no new dependencies.

**Spec:** [phase3/DESIGN_C4.md](../../../phase3/DESIGN_C4.md) (sealed through C4b, commit `d7ca12e`)

## Global Constraints

- `engine.py`/`monitor.py`'s equipment/quest/buff logic and `classify_claim` are C2c reused unchanged -- no Enchantment lifecycle, no C3 files imported.
- `claim`'s effect gains `reward_owned = True`, fired unconditionally, after its existing (unchanged) precondition-check -- cannot influence `classify_claim`'s inputs.
- `consume`'s legality is `reward_owned == True` only -- WorldState-only, never reads `MonitorState` or `EventProvenanceState`. Never illegal because of taint.
- `EventProvenanceState` (`reward_provenance_tainted: bool`) is a separate module/bucket from `MonitorState`. `event_provenance_step(action, claim_verdict, prev_provenance)` takes `claim_verdict` as an already-computed plain value -- it must never call `classify_claim` itself, and `monitor_step`/`monitor.py` must never import `oracle.py`.
- `tainted = claim_verdict is not None` inside `if action.kind == "claim":` -- states the freeze rule directly, not `if ... and verdict is not None: tainted = True`.
- Search target discovery is `classify_consume`-only. `classify_claim`'s verdict is real, recorded into `EventProvenanceState`, but never itself triggers a Discovery. (Not exercised by this plan -- no search code here -- but `oracle.py`'s `is_exploit` must be built on `classify_consume` only, not `classify_claim`, so the distinction is correct by construction from the start.)
- QA must perform four *separate* production-vs-reference comparisons per transition (monitor facts, frozen provenance, claim verdict, consume verdict), each with its own mismatch count -- never one combined pass/fail.
- `reference_classify_claim`/`reference_classify_consume`/`reference_reward_provenance_tainted` never call `event_provenance_step`, `classify_claim`, or `classify_consume` -- all re-derive from `reference_continuity_broken`/`reference_buff_source_broken` on a raw action history.
- Negative control (`known_bad_classify_consume`, reads ambient `MonitorState` instead of frozen `EventProvenanceState`) must produce both `false_positive_count >= 1` and `false_negative_count >= 1`, and Witnesses P and Q must be checked by name (dedicated replay), not inferred from the general sweep's totals.
- C1's, C2's, and C3's files are not imported from and not modified.

---

## File Structure

- Create: `phase3/c4/engine.py` -- `WorldState`, `Action`, `EQUIPMENT_CATALOG`, `REQUIRED_EQUIPMENT`, `initial_world`, `legal_actions`, `apply`.
- Create: `phase3/c4/monitor.py` -- `MonitorState`, `initial_monitor`, `monitor_step` (C2c unchanged).
- Create: `phase3/c4/event_provenance.py` -- `EventProvenanceState`, `initial_event_provenance`, `event_provenance_step`.
- Create: `phase3/c4/oracle.py` -- `classify_claim`, `classify_consume`, `is_exploit`.
- Create: `phase3/c4/qa_reference.py` -- `reference_continuity_broken`, `reference_buff_source_broken`, `reference_reward_provenance_tainted`, `reference_classify_claim`, `reference_classify_consume`.
- Create: `phase3/c4/verify_c4.py` -- Step 1 (four-comparison closure), Witnesses P/Q dedicated check, Step 1b (negative control, FP/FN), Step 2 (minimality + C2 claim-level regression check).

---

### Task 1: `phase3/c4/engine.py`

**Files:**
- Create: `phase3/c4/engine.py`

**Interfaces:**
- Produces: `EQUIPMENT_CATALOG: frozenset[str]`, `REQUIRED_EQUIPMENT: str`, `WorldState(equipped: str, quest_status: str, has_flame_buff: bool, reward_owned: bool)` (frozen dataclass), `initial_world() -> WorldState`, `Action(kind: str, target: str = "")` (frozen dataclass), `legal_actions(world) -> List[Action]`, `apply(world, action) -> WorldState`. Consumed by Tasks 2-6.

- [ ] **Step 1: Write the file**

```python
"""C4's buggy world engine. Sealed per DESIGN_C4.md -- claim()'s
precondition-check is byte-for-byte unchanged from C2c; the only new
effect is reward_owned=True, which fires unconditionally after that
check, so it cannot influence classify_claim's inputs. No "correct
claim" implementation exists here or anywhere else, same rule as C1-C3.

Independent of phase3/c2/*.py and phase3/c3/*.py -- both are sealed
evidence, C4 duplicates the small shared shapes rather than import them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

EQUIPMENT_CATALOG = frozenset({"FlameSword", "WoodenSword"})
REQUIRED_EQUIPMENT = "FlameSword"


@dataclass(frozen=True)
class WorldState:
    equipped: str
    quest_status: str  # "NOT_ACCEPTED" | "ACTIVE" | "CLAIMED"
    has_flame_buff: bool
    reward_owned: bool


def initial_world() -> WorldState:
    return WorldState(equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False, reward_owned=False)


@dataclass(frozen=True)
class Action:
    kind: str          # "equip" | "accept" | "channel" | "claim" | "consume"
    target: str = ""    # equipment name, only for "equip"

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})" if self.target else self.kind


def legal_actions(world: WorldState) -> List[Action]:
    actions: List[Action] = []
    for item in EQUIPMENT_CATALOG:
        if item != world.equipped:  # no-op equip is illegal, unchanged from C1-C3
            actions.append(Action("equip", item))
    if world.quest_status == "NOT_ACCEPTED" and world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("accept"))
    if world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("channel"))  # no no-op ban, unchanged from C2
    if world.quest_status == "ACTIVE" and world.equipped == REQUIRED_EQUIPMENT and world.has_flame_buff:
        actions.append(Action("claim"))
    if world.reward_owned:
        actions.append(Action("consume"))
    return actions


def apply(world: WorldState, action: Action) -> WorldState:
    if action.kind == "equip":
        return WorldState(equipped=action.target, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, reward_owned=world.reward_owned)
    if action.kind == "accept":
        return WorldState(equipped=world.equipped, quest_status="ACTIVE",
                           has_flame_buff=world.has_flame_buff, reward_owned=world.reward_owned)
    if action.kind == "channel":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=True, reward_owned=world.reward_owned)
    if action.kind == "claim":
        return WorldState(equipped=world.equipped, quest_status="CLAIMED",
                           has_flame_buff=world.has_flame_buff, reward_owned=True)
    if action.kind == "consume":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, reward_owned=False)
    raise ValueError(f"unknown action kind: {action.kind}")
```

- [ ] **Step 2: Sanity-run it**

Run (from `phase3/c4/`):
```bash
python -c "
from engine import initial_world, legal_actions, apply, Action
w = initial_world()
print(sorted(str(a) for a in legal_actions(w)))
w2 = apply(w, Action('equip', 'FlameSword'))
print(sorted(str(a) for a in legal_actions(w2)))
"
```
Expected: first line `['equip(FlameSword)']` (`channel` requires `equipped == REQUIRED_EQUIPMENT`, not yet true at the initial `WoodenSword` state, so it isn't legal here despite having no other precondition; no `accept` yet either -- still `WoodenSword`); second line (after equipping Flame) `['accept', 'channel', 'equip(WoodenSword)']` -- no `consume` yet (`reward_owned` still `False`).

No commit yet -- committed together with Tasks 2-6 at the end (matches C1's `9ec6249` / C2's `6aab686` / C3's `2441a86` convention).

---

### Task 2: `phase3/c4/monitor.py`

**Files:**
- Create: `phase3/c4/monitor.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.REQUIRED_EQUIPMENT`, `engine.WorldState` (Task 1).
- Produces: `MonitorState(continuity_broken: bool, buff_source_broken: bool)` (frozen dataclass), `initial_monitor() -> MonitorState`, `monitor_step(prev_world, action, new_world, prev_monitor) -> MonitorState`. Consumed by Tasks 3-6.

- [ ] **Step 1: Write the file**

```python
"""Independent property monitor. NOT part of the engine -- claim() never
reads this. Byte-for-byte C2c, unchanged for C4 -- no Enchantment chain.
Same visibility rules as C1-C3: ranking/guidance (score, descriptor,
UCT) may never read this; only dedup identity and reward/oracle checks
may.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, REQUIRED_EQUIPMENT, WorldState


@dataclass(frozen=True)
class MonitorState:
    continuity_broken: bool
    buff_source_broken: bool


def initial_monitor() -> MonitorState:
    return MonitorState(continuity_broken=False, buff_source_broken=False)


def monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = False
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, buff_source_broken=buff_source_broken)
```

- [ ] **Step 2: Sanity-run the two Witness-P/Q-relevant transitions directly**

Run (from `phase3/c4/`):
```bash
python -c "
from engine import initial_world, apply, Action
from monitor import initial_monitor, monitor_step

def replay(actions):
    world, monitor = initial_world(), initial_monitor()
    for a in actions:
        new_world = apply(world, a)
        monitor = monitor_step(world, a, new_world, monitor)
        world = new_world
    return world, monitor

# Witness P prefix: clean claim, then post-claim equip(Wood) drifts buff_source_broken ambiently.
w, m = replay([Action('equip','FlameSword'), Action('accept'), Action('channel'), Action('claim'), Action('equip','WoodenSword')])
print('P prefix buff_source_broken (should be True, ambient drift):', m.buff_source_broken)

# Witness Q prefix: tainted claim, then post-claim channel cleans buff_source_broken ambiently.
w, m = replay([Action('equip','FlameSword'), Action('channel'), Action('equip','WoodenSword'), Action('equip','FlameSword'), Action('accept'), Action('claim'), Action('channel')])
print('Q prefix buff_source_broken (should be False, ambient cleanup):', m.buff_source_broken)
"
```
Expected:
```
P prefix buff_source_broken (should be True, ambient drift): True
Q prefix buff_source_broken (should be False, ambient cleanup): False
```
This confirms the *raw material* DESIGN_C4.md's Witnesses P/Q depend on before Task 3 adds the frozen-provenance layer on top.

---

### Task 3: `phase3/c4/event_provenance.py`

**Files:**
- Create: `phase3/c4/event_provenance.py`

**Interfaces:**
- Consumes: `engine.Action` (Task 1).
- Produces: `EventProvenanceState(reward_provenance_tainted: bool)` (frozen dataclass), `initial_event_provenance() -> EventProvenanceState`, `event_provenance_step(action, claim_verdict, prev_provenance) -> EventProvenanceState`. Consumed by Tasks 4-6.

- [ ] **Step 1: Write the file**

```python
"""Independent event-provenance tracker -- C4's third persistent state
bucket, distinct from MonitorState by design. See DESIGN_C4.md's
"EventProvenanceState -- a distinct boundary" section: folding this
into MonitorState would force monitor.py to import oracle.py
(circular) or duplicate classify_claim's OR-logic. event_provenance_step
takes claim_verdict as an already-computed plain value -- it never
calls classify_claim itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from engine import Action


@dataclass(frozen=True)
class EventProvenanceState:
    reward_provenance_tainted: bool


def initial_event_provenance() -> EventProvenanceState:
    return EventProvenanceState(reward_provenance_tainted=False)


def event_provenance_step(action: Action, claim_verdict: Optional[str], prev_provenance: EventProvenanceState) -> EventProvenanceState:
    tainted = prev_provenance.reward_provenance_tainted
    if action.kind == "claim":
        tainted = claim_verdict is not None
    return EventProvenanceState(reward_provenance_tainted=tainted)
```

- [ ] **Step 2: Sanity-run the freeze rule**

Run (from `phase3/c4/`):
```bash
python -c "
from engine import Action
from event_provenance import initial_event_provenance, event_provenance_step
p = initial_event_provenance()
p2 = event_provenance_step(Action('claim'), None, p)
print('legitimate claim ->', p2.reward_provenance_tainted)
p3 = event_provenance_step(Action('claim'), 'EQUIPMENT_CONTINUITY_VIOLATION', p)
print('violating claim ->', p3.reward_provenance_tainted)
p4 = event_provenance_step(Action('equip', 'WoodenSword'), None, p3)
print('unrelated action after tainted claim, provenance stays ->', p4.reward_provenance_tainted)
"
```
Expected:
```
legitimate claim -> False
violating claim -> True
unrelated action after tainted claim, provenance stays -> True
```

---

### Task 4: `phase3/c4/oracle.py`

**Files:**
- Create: `phase3/c4/oracle.py`

**Interfaces:**
- Consumes: `engine.Action` (Task 1), `monitor.MonitorState` (Task 2), `event_provenance.EventProvenanceState` (Task 3).
- Produces: `classify_claim(action, prev_monitor) -> Optional[str]`, `classify_consume(action, prev_provenance) -> Optional[str]`, `is_exploit(action, prev_provenance) -> bool`. Consumed by Tasks 5-6.

- [ ] **Step 1: Write the file**

```python
"""Runtime oracle. classify_claim is byte-for-byte C2c, unchanged.
classify_consume is new -- C4's actual search-target oracle. See
DESIGN_C4.md's "Search target discovery is consume-only": classify_claim's
verdict is real and recorded (via EventProvenanceState) but must never
trigger a Discovery on its own, so is_exploit is built on
classify_consume only.
"""
from __future__ import annotations

from typing import Optional

from engine import Action
from event_provenance import EventProvenanceState
from monitor import MonitorState


def classify_claim(action: Action, prev_monitor: MonitorState) -> Optional[str]:
    if action.kind != "claim":
        return None
    eq = prev_monitor.continuity_broken
    buf = prev_monitor.buff_source_broken
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None  # legitimate completion, not an exploit


def classify_consume(action: Action, prev_provenance: EventProvenanceState) -> Optional[str]:
    if action.kind != "consume":
        return None
    if prev_provenance.reward_provenance_tainted:
        return "TAINTED_REWARD_CONSUMPTION"
    return None


def is_exploit(action: Action, prev_provenance: EventProvenanceState) -> bool:
    """C4's search-target wrapper -- built on classify_consume only.
    classify_claim's verdict does not go through this function; it is
    not a search-terminal discovery (DESIGN_C4.md)."""
    return classify_consume(action, prev_provenance) is not None
```

- [ ] **Step 2: Sanity-run it**

Run (from `phase3/c4/`):
```bash
python -c "
from monitor import MonitorState
from event_provenance import EventProvenanceState
from engine import Action
from oracle import classify_claim, classify_consume, is_exploit

print(classify_claim(Action('claim'), MonitorState(False, False)))
print(classify_claim(Action('claim'), MonitorState(True, True)))
print(classify_consume(Action('consume'), EventProvenanceState(False)))
print(classify_consume(Action('consume'), EventProvenanceState(True)))
print(is_exploit(Action('consume'), EventProvenanceState(True)))
print(is_exploit(Action('claim'), EventProvenanceState(True)))
"
```
Expected:
```
None
BOTH
None
TAINTED_REWARD_CONSUMPTION
True
False
```
(Last line: `is_exploit` on a `claim` action is always `False` -- wrong action kind for `classify_consume`, confirming `claim` verdicts never register as a discovery through this function.)

---

### Task 5: `phase3/c4/qa_reference.py`

**Files:**
- Create: `phase3/c4/qa_reference.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.REQUIRED_EQUIPMENT`, `engine.apply`, `engine.initial_world` (Task 1).
- Produces: `reference_continuity_broken(history) -> bool`, `reference_buff_source_broken(history) -> bool`, `reference_reward_provenance_tainted(history) -> bool`, `reference_classify_claim(history_before, action) -> Optional[str]`, `reference_classify_consume(history_before, action) -> Optional[str]`. Consumed by Task 6.

- [ ] **Step 1: Write the file**

```python
"""QA-only independent reference specification. Never imported by
engine.py, monitor.py, event_provenance.py, or oracle.py.

reference_continuity_broken/reference_buff_source_broken are C2c's
exact functions (C4's base, unchanged). reference_reward_provenance_
tainted, reference_classify_claim, and reference_classify_consume are
new -- DESIGN_C4.md's QA section: C4 is the first case where the oracle
itself, not just the monitor fold beneath it, needs an independent
reference. None of the three call event_provenance_step, classify_claim,
or classify_consume -- all re-derive directly from the reference
property functions on a raw action history.
"""
from __future__ import annotations

from typing import List, Optional

from engine import Action, REQUIRED_EQUIPMENT, apply, initial_world


def reference_continuity_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        world = apply(world, action)
        if world.quest_status == "ACTIVE" and world.equipped != REQUIRED_EQUIPMENT:
            broken = True
    return broken


def reference_buff_source_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        world = apply(world, action)
        if action.kind == "channel":
            broken = False
        elif world.has_flame_buff and world.equipped != REQUIRED_EQUIPMENT:
            broken = True
    return broken


def reference_reward_provenance_tainted(history: List[Action]) -> bool:
    claim_index = None
    for i, action in enumerate(history):
        if action.kind == "claim":
            claim_index = i
            break   # claim fires at most once
    if claim_index is None:
        return False
    prefix = history[:claim_index]
    return reference_continuity_broken(prefix) or reference_buff_source_broken(prefix)


def reference_classify_claim(history_before: List[Action], action: Action) -> Optional[str]:
    if action.kind != "claim":
        return None
    eq = reference_continuity_broken(history_before)
    buf = reference_buff_source_broken(history_before)
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None


def reference_classify_consume(history_before: List[Action], action: Action) -> Optional[str]:
    if action.kind != "consume":
        return None
    if reference_reward_provenance_tainted(history_before):
        return "TAINTED_REWARD_CONSUMPTION"
    return None
```

- [ ] **Step 2: Sanity-run against Witnesses P and Q**

Run (from `phase3/c4/`):
```bash
python -c "
from engine import Action
from qa_reference import reference_reward_provenance_tainted, reference_classify_consume

P = [Action('equip','FlameSword'), Action('accept'), Action('channel'), Action('claim'), Action('equip','WoodenSword')]
Q = [Action('equip','FlameSword'), Action('channel'), Action('equip','WoodenSword'), Action('equip','FlameSword'), Action('accept'), Action('claim'), Action('channel')]

print('P full history tainted (should be False):', reference_reward_provenance_tainted(P))
print('Q full history tainted (should be True):', reference_reward_provenance_tainted(Q))
print('P + consume classify (should be None):', reference_classify_consume(P, Action('consume')))
print('Q + consume classify (should be TAINTED_REWARD_CONSUMPTION):', reference_classify_consume(Q, Action('consume')))
"
```
Expected:
```
P full history tainted (should be False): False
Q full history tainted (should be True): True
P + consume classify (should be None): None
Q + consume classify (should be TAINTED_REWARD_CONSUMPTION): TAINTED_REWARD_CONSUMPTION
```
This is the reference-side confirmation that Witnesses P/Q have the intended ground truth, matching Task 2's monitor-side trace, before Task 6 checks production against it.

---

### Task 6: `phase3/c4/verify_c4.py`

**Files:**
- Create: `phase3/c4/verify_c4.py`

**Interfaces:**
- Consumes: everything Tasks 1-5 produce.
- Produces: a runnable script, terminal node of this plan.

- [ ] **Step 1: Write the file**

```python
"""C4 QA -- per DESIGN_C4.md (through C4b). No search algorithm is
imported or run anywhere in this file.

Step 1: one closure sweep, four independent production-vs-reference
comparisons per transition (monitor facts, frozen provenance, claim
verdict, consume verdict), each with its own mismatch count -- a
mismatch in one can never be masked by another passing. Dedup/pruning
key is reference-derived, never production-derived.

Witnesses P & Q: dedicated, explicit replay (not left to the general
sweep) proving EventProvenanceState is load-bearing in both directions
-- a naive ambient-MonitorState read gets P wrong one way and Q wrong
the other way.

Step 1b: known_bad_classify_consume, run through the identical closure
sweep, must produce both a false positive and a false negative; P and Q
must reproduce each specifically, by name.

Step 2: minimality for TAINTED_REWARD_CONSUMPTION + legitimate-consume
reachability + a regression check that C2's three claim-level
categories still classify correctly (their minimality was already
proven in C2 and nothing upstream of claim changed).

Run:
    python verify_c4.py
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional, Set, Tuple

from engine import Action, REQUIRED_EQUIPMENT, WorldState, apply, initial_world, legal_actions
from monitor import MonitorState, initial_monitor, monitor_step
from event_provenance import EventProvenanceState, initial_event_provenance, event_provenance_step
from oracle import classify_claim, classify_consume
from qa_reference import (
    reference_buff_source_broken, reference_classify_claim, reference_classify_consume,
    reference_continuity_broken, reference_reward_provenance_tainted,
)

SearchState4 = Tuple[WorldState, MonitorState, EventProvenanceState]
ConsumeFn = Callable[[Action, MonitorState, EventProvenanceState], Optional[str]]


def known_bad_classify_consume(action: Action, prev_monitor: MonitorState) -> Optional[str]:
    """Negative control only -- never used outside this QA file. Reads
    AMBIENT MonitorState at consume-time instead of the frozen
    EventProvenanceState -- the exact mistake Witnesses P/Q prove wrong
    in both directions."""
    if action.kind != "consume":
        return None
    if prev_monitor.continuity_broken or prev_monitor.buff_source_broken:
        return "TAINTED_REWARD_CONSUMPTION"
    return None


def _production_consume(action: Action, prev_monitor: MonitorState, prev_provenance: EventProvenanceState) -> Optional[str]:
    return classify_consume(action, prev_provenance)


def _known_bad_consume(action: Action, prev_monitor: MonitorState, prev_provenance: EventProvenanceState) -> Optional[str]:
    return known_bad_classify_consume(action, prev_monitor)


WITNESS_P = [Action("equip", "FlameSword"), Action("accept"), Action("channel"),
             Action("claim"), Action("equip", "WoodenSword"), Action("consume")]
WITNESS_Q = [Action("equip", "FlameSword"), Action("channel"), Action("equip", "WoodenSword"),
             Action("equip", "FlameSword"), Action("accept"), Action("claim"),
             Action("channel"), Action("consume")]

WITNESS_LEGITIMATE = [Action("equip", "FlameSword"), Action("accept"), Action("channel"),
                       Action("claim"), Action("consume")]
WITNESS_TAINTED = [Action("equip", "FlameSword"), Action("accept"), Action("equip", "WoodenSword"),
                    Action("equip", "FlameSword"), Action("channel"), Action("claim"), Action("consume")]

# C2's own four witnesses, replayed here as a regression check only.
C2_LEGITIMATE = [Action("equip", "FlameSword"), Action("channel"), Action("accept"), Action("claim")]
C2_EQUIPMENT = [Action("equip", "FlameSword"), Action("accept"), Action("equip", "WoodenSword"),
                Action("equip", "FlameSword"), Action("channel"), Action("claim")]
C2_BUFF = [Action("equip", "FlameSword"), Action("channel"), Action("equip", "WoodenSword"),
           Action("equip", "FlameSword"), Action("accept"), Action("claim")]
C2_BOTH = [Action("equip", "FlameSword"), Action("channel"), Action("accept"),
           Action("equip", "WoodenSword"), Action("equip", "FlameSword"), Action("claim")]


def run_closure(consume_fn: ConsumeFn, label: str) -> Dict[str, int]:
    print(f"--- closure run: {label} ---")
    seen: Set[Tuple[WorldState, bool, bool, bool]] = set()
    frontier: Dict[SearchState4, List[Action]] = {
        (initial_world(), initial_monitor(), initial_event_provenance()): []
    }
    layers = 0
    checked = 0
    counts = {"monitor": 0, "provenance": 0, "claim": 0, "consume": 0, "fp": 0, "fn": 0}
    examples: List[str] = []

    while frontier:
        layers += 1
        discovered_this_layer: Dict[Tuple[WorldState, bool, bool, bool], Tuple[SearchState4, List[Action]]] = {}
        for (world, monitor, provenance), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_monitor = monitor_step(world, action, new_world, monitor)
                claim_verdict = classify_claim(action, monitor)
                consume_verdict = consume_fn(action, monitor, provenance)
                new_provenance = event_provenance_step(action, claim_verdict, provenance)
                new_path = path + [action]
                checked += 1

                ref_continuity = reference_continuity_broken(new_path)
                ref_buff = reference_buff_source_broken(new_path)
                ref_provenance = reference_reward_provenance_tainted(new_path)
                ref_claim_verdict = reference_classify_claim(path, action)
                ref_consume_verdict = reference_classify_consume(path, action)

                if (new_monitor.continuity_broken, new_monitor.buff_source_broken) != (ref_continuity, ref_buff):
                    counts["monitor"] += 1
                    examples.append(f"monitor @ {new_path}")
                if new_provenance.reward_provenance_tainted != ref_provenance:
                    counts["provenance"] += 1
                    examples.append(f"provenance @ {new_path}")
                if claim_verdict != ref_claim_verdict:
                    counts["claim"] += 1
                    examples.append(f"claim_verdict @ {new_path}: got={claim_verdict} ref={ref_claim_verdict}")
                if consume_verdict != ref_consume_verdict:
                    counts["consume"] += 1
                    examples.append(f"consume_verdict @ {new_path}: got={consume_verdict} ref={ref_consume_verdict}")
                    if consume_verdict is not None and ref_consume_verdict is None:
                        counts["fp"] += 1
                    elif consume_verdict is None and ref_consume_verdict is not None:
                        counts["fn"] += 1

                key = (new_world, ref_continuity, ref_buff, ref_provenance)
                if key not in seen and key not in discovered_this_layer:
                    discovered_this_layer[key] = ((new_world, new_monitor, new_provenance), new_path)
        if not discovered_this_layer:
            break
        seen.update(discovered_this_layer.keys())
        frontier = {state: p for state, p in discovered_this_layer.values()}

    print(f"  transitions checked: {checked}")
    print(f"  layers to closure:   {layers}")
    print(f"  distinct semantic states found: {len(seen)}")
    print(f"  mismatches -- monitor:{counts['monitor']} provenance:{counts['provenance']} "
          f"claim:{counts['claim']} consume:{counts['consume']} (fp={counts['fp']} fn={counts['fn']})")
    for line in examples[:5]:
        print(f"    {line}")
    return counts


def step1_production() -> bool:
    print("=== Step 1: production, four independent comparisons ===")
    counts = run_closure(_production_consume, "production")
    ok = all(counts[k] == 0 for k in ("monitor", "provenance", "claim", "consume"))
    print("  PASS" if ok else "  FAIL: production must have 0 mismatches on all four comparisons")
    return ok


def replay(path: List[Action], consume_fn=None) -> Tuple[Optional[str], bool]:
    """Replays a path, returning the classify_consume-equivalent verdict
    at its own consume transition (None if no consume). consume_fn lets
    Step 1b re-check known_bad against a fixed witness."""
    world, monitor, provenance = initial_world(), initial_monitor(), initial_event_provenance()
    verdict: Optional[str] = None
    for action in path:
        if action not in legal_actions(world):
            return None, False
        claim_verdict = classify_claim(action, monitor)
        if consume_fn is None:
            step_consume_verdict = classify_consume(action, provenance)
        else:
            step_consume_verdict = consume_fn(action, monitor, provenance)
        if action.kind == "consume":
            verdict = step_consume_verdict
        new_world = apply(world, action)
        new_monitor = monitor_step(world, action, new_world, monitor)
        new_provenance = event_provenance_step(action, claim_verdict, provenance)
        world, monitor, provenance = new_world, new_monitor, new_provenance
    return verdict, True


def check_witnesses_p_and_q() -> bool:
    print()
    print("=== Witnesses P & Q: dedicated necessity + negative-control check ===")
    ok = True

    verdict_p, legal_p = replay(WITNESS_P)
    if not legal_p or verdict_p is not None:
        print(f"  FAIL: Witness P production verdict={verdict_p} (legal={legal_p}), expected None (legitimate)")
        ok = False
    else:
        print("  Witness P production: PASS (legitimate, as expected)")

    verdict_q, legal_q = replay(WITNESS_Q)
    if not legal_q or verdict_q != "TAINTED_REWARD_CONSUMPTION":
        print(f"  FAIL: Witness Q production verdict={verdict_q} (legal={legal_q}), expected TAINTED_REWARD_CONSUMPTION")
        ok = False
    else:
        print("  Witness Q production: PASS (tainted, as expected)")

    bad_verdict_p, _ = replay(WITNESS_P, consume_fn=_known_bad_consume)
    if bad_verdict_p != "TAINTED_REWARD_CONSUMPTION":
        print(f"  FAIL: known_bad on Witness P = {bad_verdict_p}, expected a false positive (TAINTED_REWARD_CONSUMPTION)")
        ok = False
    else:
        print("  Witness P known_bad: PASS (reproduces the false positive)")

    bad_verdict_q, _ = replay(WITNESS_Q, consume_fn=_known_bad_consume)
    if bad_verdict_q is not None:
        print(f"  FAIL: known_bad on Witness Q = {bad_verdict_q}, expected a false negative (None)")
        ok = False
    else:
        print("  Witness Q known_bad: PASS (reproduces the false negative)")

    return ok


def step1b_negative_control() -> bool:
    print()
    print("=== Step 1b: negative control (known_bad_classify_consume) ===")
    counts = run_closure(_known_bad_consume, "known_bad")
    ok = counts["fp"] >= 1 and counts["fn"] >= 1
    print(f"  {'PASS' if ok else 'FAIL'}: fp={counts['fp']} (need >=1), fn={counts['fn']} (need >=1)")
    return ok


def step2_minimality() -> bool:
    print()
    print("=== Step 2: minimality + C2 claim-level regression ===")
    ok = True

    v, legal = replay(WITNESS_LEGITIMATE)
    if not legal or v is not None:
        print(f"  FAIL: legitimate-consume witness verdict={v} (legal={legal})")
        ok = False
    else:
        print(f"  legitimate consume witness OK: {len(WITNESS_LEGITIMATE)} actions")

    v, legal = replay(WITNESS_TAINTED)
    if not legal or v != "TAINTED_REWARD_CONSUMPTION":
        print(f"  FAIL: TAINTED_REWARD_CONSUMPTION witness verdict={v} (legal={legal})")
        ok = False
    else:
        print(f"  TAINTED_REWARD_CONSUMPTION witness OK: {len(WITNESS_TAINTED)} actions")

    # C2 claim-level regression: same four witnesses, same expected classify_claim results.
    for name, path, expected in [
        ("C2_LEGITIMATE", C2_LEGITIMATE, None),
        ("C2_EQUIPMENT", C2_EQUIPMENT, "EQUIPMENT_CONTINUITY_VIOLATION"),
        ("C2_BUFF", C2_BUFF, "BUFF_SOURCE_LIFECYCLE_VIOLATION"),
        ("C2_BOTH", C2_BOTH, "BOTH"),
    ]:
        world, monitor = initial_world(), initial_monitor()
        result = None
        legal = True
        for action in path:
            if action not in legal_actions(world):
                legal = False
                break
            if action.kind == "claim":
                result = classify_claim(action, monitor)
            new_world = apply(world, action)
            monitor = monitor_step(world, action, new_world, monitor)
            world = new_world
        if not legal or result != expected:
            print(f"  FAIL: {name} regression -- got {result} (legal={legal}), expected {expected}")
            ok = False
        else:
            print(f"  {name} regression OK: classify_claim={result}")

    if not ok:
        return False

    # Exhaustive SearchState4-deduped search: TAINTED_REWARD_CONSUMPTION
    # must not appear at a consume earlier than WITNESS_TAINTED's length.
    max_depth = len(WITNESS_TAINTED) - 1
    start: SearchState4 = (initial_world(), initial_monitor(), initial_event_provenance())
    frontier: Dict[SearchState4, List[Action]] = {start: []}
    visited = {start}
    earliest: Optional[List[Action]] = None

    for depth in range(1, max_depth + 1):
        next_frontier: Dict[SearchState4, List[Action]] = {}
        for (world, monitor, provenance), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_monitor = monitor_step(world, action, new_world, monitor)
                claim_verdict = classify_claim(action, monitor)
                new_provenance = event_provenance_step(action, claim_verdict, provenance)
                new_state: SearchState4 = (new_world, new_monitor, new_provenance)
                new_path = path + [action]
                if action.kind == "consume" and classify_consume(action, provenance) is not None and earliest is None:
                    earliest = new_path
                if new_state in visited:
                    continue
                visited.add(new_state)
                next_frontier[new_state] = new_path
        frontier = next_frontier
        if not frontier:
            break

    print(f"  exhaustive search to depth {max_depth}: {len(visited)} SearchStates visited")
    if earliest is not None:
        print(f"  FAIL: TAINTED_REWARD_CONSUMPTION reached early at depth {len(earliest)} (< {len(WITNESS_TAINTED)}): {earliest}")
        ok = False
    else:
        print(f"  no shortcut for TAINTED_REWARD_CONSUMPTION: not reached within depth {max_depth}")

    return ok


if __name__ == "__main__":
    ok1 = step1_production()
    ok_pq = check_witnesses_p_and_q()
    ok1b = step1b_negative_control()
    ok2 = step2_minimality() if ok1 else False

    print()
    if not ok1:
        print("C4 QA: FAIL at Step 1 -- Step 2 not run (untrustworthy until Step 1 passes)")
    else:
        overall = ok1 and ok_pq and ok1b and ok2
        print("C4 QA: " + ("PASS" if overall else "FAIL"))
```

- [ ] **Step 2: Run it**

Run (from `phase3/c4/`):
```bash
python verify_c4.py
```
Expected: every check prints `PASS`, ending with `C4 QA: PASS`. If anything prints `FAIL`, stop and diagnose -- per this project's established discipline, a `FAIL` here means either the implementation has a bug or `DESIGN_C4.md` itself needs another reviewed correction (same pattern as every prior `b`/`c` round). Do not edit `verify_c4.py` to make a failure disappear.

- [ ] **Step 3: Confirm C1/C2/C3 untouched**

Run (from repo root):
```bash
git status --short phase3/*.py phase3/c2/ phase3/c3/ phase3/c4/
```
Expected: only new files under `phase3/c4/`; no modifications to `phase3/*.py` (C1), `phase3/c2/*.py` (C2), or `phase3/c3/*.py` (C3).

- [ ] **Step 4: Commit**

```bash
git add phase3/c4/engine.py phase3/c4/monitor.py phase3/c4/event_provenance.py phase3/c4/oracle.py phase3/c4/qa_reference.py phase3/c4/verify_c4.py
git commit -m "Phase 3 C4 core: engine/monitor/event_provenance/oracle/qa_reference/verify, PASS"
```

(Full commit message with actual observed numbers -- transitions/layers/semantic-states, all four mismatch counts, fp/fn counts -- to be filled in from the real Step 2 output before committing, same convention as C1's `9ec6249`/C2's `6aab686`/C3's `2441a86`.)

---

## Self-Review Notes

- **Spec coverage:** `reward_owned`/`consume` addition without disturbing claim's precondition (Task 1) / `MonitorState` byte-for-byte C2c (Task 2) / `EventProvenanceState` as its own module, `event_provenance_step` taking `claim_verdict` as a plain argument (Task 3) / `classify_consume` + `is_exploit` built on it only (Task 4) / three new reference functions, none calling production (Task 5) / four-comparison closure with separate counters, reference-derived dedup key, dedicated P/Q replay, FP/FN-tracked negative control, C2 regression check, `TAINTED_REWARD_CONSUMPTION` minimality (Task 6) -- all covered.
- **Placeholder scan:** none -- every step has runnable code and a concrete expected-output description.
- **Type consistency:** `WorldState(equipped, quest_status, has_flame_buff, reward_owned)`, `MonitorState(continuity_broken, buff_source_broken)`, `EventProvenanceState(reward_provenance_tainted)` used identically across all six files. `classify_claim(action, prev_monitor)` / `classify_consume(action, prev_provenance)` / `event_provenance_step(action, claim_verdict, prev_provenance)` signatures match between their definitions (Tasks 3-4) and every call site (Task 6).
