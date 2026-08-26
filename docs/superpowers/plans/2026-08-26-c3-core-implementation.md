# C3 Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `phase3/c3/{engine,monitor,oracle,qa_reference,verify_c3}.py` per `DESIGN_C3.md` (through the C3c pathway-predicate correction) and get `verify_c3.py` to PASS -- core + QA only, no search.

**Architecture:** Direct structural port of `phase3/c2/`'s five-file layout, extended for a third `MonitorState` field (`enchant_broken`) and a new mandatory `enchant`/`unenchant`/`channel`-precondition chain. The one genuinely new piece is `verify_c3.py`'s pathway-attribution machinery (`classify_pathway`) and the dedicated `Hclean`/`Htainted` indistinguishability check -- neither has a C2 analogue to port from.

**Tech Stack:** Python 3, stdlib only (`dataclasses`, `typing`) -- same as C1/C2, no new dependencies.

**Spec:** [phase3/DESIGN_C3.md](../../../phase3/DESIGN_C3.md) (sealed through C3c, commit `8d10071`)

## Global Constraints

- `claim()` and the oracle (`classify_claim`/`is_exploit`) are byte-for-byte unchanged from C2c -- only `channel()`'s precondition and `buff_source_broken`'s update rule change.
- `channel()`'s legality is `equipped == REQUIRED_EQUIPMENT and enchanted == True` -- WorldState-only, never reads `MonitorState`. Its legality never depends on `enchant_broken`.
- `enchant_broken` is permanent once set (same recovery family as `continuity_broken`), triggered only by `unenchant` (structurally independent of `equip` -- must never be derived from `equipped`'s transitions).
- `buff_source_broken`'s `channel` branch captures `prev_monitor.enchant_broken` (grant-time provenance); its other branch (post-grant equipment break) is unchanged from C2.
- `reference_buff_source_broken` must not call `reference_enchant_broken` and must not mirror `monitor_step`'s incremental fold -- last-channel-then-slice, per `DESIGN_C3.md`'s Step 1c.
- `classify_pathway(path)` is only meaningful when the path's claim already classified as `BUFF_SOURCE_LIFECYCLE_VIOLATION`; it never inspects `continuity_broken` itself.
- C2's files (`phase3/c2/*.py`) are not imported from and not modified -- C3 duplicates the small shared shapes, same precedent as C2 not importing from C1.
- No search algorithm is imported or run anywhere in this plan.

---

## File Structure

- Create: `phase3/c3/engine.py` -- `WorldState`, `Action`, `EQUIPMENT_CATALOG`, `REQUIRED_EQUIPMENT`, `initial_world`, `legal_actions`, `apply`.
- Create: `phase3/c3/monitor.py` -- `MonitorState`, `initial_monitor`, `monitor_step`.
- Create: `phase3/c3/oracle.py` -- `classify_claim`, `is_exploit`.
- Create: `phase3/c3/qa_reference.py` -- `reference_continuity_broken`, `reference_enchant_broken`, `reference_buff_source_broken`.
- Create: `phase3/c3/verify_c3.py` -- Step 1 (closure equivalence), indistinguishability pair check, Step 1b (negative control), Step 2 (five minimality claims + pathway attribution), Step 3 (post-claim mutation regression).

---

### Task 1: `phase3/c3/engine.py`

**Files:**
- Create: `phase3/c3/engine.py`

**Interfaces:**
- Produces: `EQUIPMENT_CATALOG: frozenset[str]`, `REQUIRED_EQUIPMENT: str`, `WorldState(equipped: str, quest_status: str, has_flame_buff: bool, enchanted: bool)` (frozen dataclass), `initial_world() -> WorldState`, `Action(kind: str, target: str = "")` (frozen dataclass), `legal_actions(world: WorldState) -> List[Action]`, `apply(world: WorldState, action: Action) -> WorldState`. All consumed by Tasks 2-5.

- [ ] **Step 1: Write the file**

```python
"""C3's buggy world engine. Sealed per DESIGN_C3.md -- claim() is
byte-for-byte unchanged from C2c; channel()'s legality is WorldState-only
and never depends on enchant_broken (see DESIGN_C3.md's "channel() is
legal-but-potentially-unqualified" section). No "correct claim"
implementation exists here or anywhere else, same rule as C1/C2.

Independent of phase3/c2/*.py -- C2 is sealed evidence, so C3 duplicates
the small catalog/action shapes rather than import them.
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
    enchanted: bool


def initial_world() -> WorldState:
    return WorldState(equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False, enchanted=False)


@dataclass(frozen=True)
class Action:
    kind: str          # "equip" | "accept" | "enchant" | "unenchant" | "channel" | "claim"
    target: str = ""    # equipment name, only for "equip"

    def __repr__(self) -> str:
        return f"{self.kind}({self.target})" if self.target else self.kind


def legal_actions(world: WorldState) -> List[Action]:
    actions: List[Action] = []
    for item in EQUIPMENT_CATALOG:
        if item != world.equipped:  # no-op equip is illegal, unchanged from C1/C2
            actions.append(Action("equip", item))
    if world.quest_status == "NOT_ACCEPTED" and world.equipped == REQUIRED_EQUIPMENT:
        actions.append(Action("accept"))
    if not world.enchanted:  # no-op enchant is illegal
        actions.append(Action("enchant"))
    if world.enchanted:
        actions.append(Action("unenchant"))
    if world.equipped == REQUIRED_EQUIPMENT and world.enchanted:
        # NO no-op ban -- unchanged reasoning from DESIGN_C2.md, see
        # DESIGN_C3.md's "channel() is legal-but-potentially-unqualified".
        actions.append(Action("channel"))
    if world.quest_status == "ACTIVE" and world.equipped == REQUIRED_EQUIPMENT and world.has_flame_buff:
        # BUGGY: only checks current equipment and current buff presence,
        # not continuity/source-lifecycle/provenance history.
        actions.append(Action("claim"))
    return actions


def apply(world: WorldState, action: Action) -> WorldState:
    if action.kind == "equip":
        return WorldState(equipped=action.target, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, enchanted=world.enchanted)
    if action.kind == "accept":
        return WorldState(equipped=world.equipped, quest_status="ACTIVE",
                           has_flame_buff=world.has_flame_buff, enchanted=world.enchanted)
    if action.kind == "enchant":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, enchanted=True)
    if action.kind == "unenchant":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=world.has_flame_buff, enchanted=False)
    if action.kind == "channel":
        return WorldState(equipped=world.equipped, quest_status=world.quest_status,
                           has_flame_buff=True, enchanted=world.enchanted)
    if action.kind == "claim":
        return WorldState(equipped=world.equipped, quest_status="CLAIMED",
                           has_flame_buff=world.has_flame_buff, enchanted=world.enchanted)
    raise ValueError(f"unknown action kind: {action.kind}")
```

- [ ] **Step 2: Sanity-run it**

Run (from `phase3/c3/`):
```bash
python -c "
from engine import initial_world, legal_actions, apply, Action
w = initial_world()
print(w)
print(sorted(str(a) for a in legal_actions(w)))
w2 = apply(w, Action('equip', 'FlameSword'))
print(sorted(str(a) for a in legal_actions(w2)))
"
```
Expected: first line `WorldState(equipped='WoodenSword', quest_status='NOT_ACCEPTED', has_flame_buff=False, enchanted=False)`; second line a list containing `equip(FlameSword)`, `enchant` (no `accept`, no `channel`, no `claim`, no `unenchant` yet); third line (after equipping Flame) containing `accept`, `enchant`, `equip(WoodenSword)` (still no `channel` -- not enchanted yet).

No commit yet -- committed together with Tasks 2-5 at the end (matches C1's `9ec6249` / C2's `6aab686` convention: one commit for the whole core+QA milestone).

---

### Task 2: `phase3/c3/monitor.py`

**Files:**
- Create: `phase3/c3/monitor.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.REQUIRED_EQUIPMENT`, `engine.WorldState` (Task 1).
- Produces: `MonitorState(continuity_broken: bool, enchant_broken: bool, buff_source_broken: bool)` (frozen dataclass), `initial_monitor() -> MonitorState`, `monitor_step(prev_world, action, new_world, prev_monitor) -> MonitorState`. Consumed by Tasks 3-5.

- [ ] **Step 1: Write the file**

```python
"""Independent property monitor. NOT part of the engine -- claim() never
reads this. Same visibility rules as C1/C2: ranking/guidance (score,
descriptor, UCT) may never read this; only dedup identity and
reward/oracle checks may.

The known-bad negative-control variant lives in verify_c3.py, not here,
same reasoning as C2.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, REQUIRED_EQUIPMENT, WorldState


@dataclass(frozen=True)
class MonitorState:
    continuity_broken: bool
    enchant_broken: bool
    buff_source_broken: bool


def initial_monitor() -> MonitorState:
    return MonitorState(continuity_broken=False, enchant_broken=False, buff_source_broken=False)


def monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    enchant_broken = prev_monitor.enchant_broken
    if prev_world.enchanted and not new_world.enchanted:
        enchant_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = prev_monitor.enchant_broken   # grant-time capture
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken,
                         enchant_broken=enchant_broken,
                         buff_source_broken=buff_source_broken)
```

- [ ] **Step 2: Sanity-run the grant-time capture directly**

Run (from `phase3/c3/`):
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

clean = [Action('equip','FlameSword'), Action('enchant')]
tainted = clean + [Action('unenchant'), Action('enchant')]
wc, mc = replay(clean)
wt, mt = replay(tainted)
print('worlds equal:', wc == wt)
print('prior buff_source_broken equal:', mc.buff_source_broken == mt.buff_source_broken)
print('enchant_broken clean/tainted:', mc.enchant_broken, mt.enchant_broken)
wc2, mc2 = replay(clean + [Action('channel')])
wt2, mt2 = replay(tainted + [Action('channel')])
print('buff_source_broken after channel, clean/tainted:', mc2.buff_source_broken, mt2.buff_source_broken)
"
```
Expected:
```
worlds equal: True
prior buff_source_broken equal: True
enchant_broken clean/tainted: False True
buff_source_broken after channel, clean/tainted: False True
```
This is the `Hclean`/`Htainted` pair from `DESIGN_C3.md` -- if this doesn't match exactly, stop and re-check `monitor_step` against the sealed formula before continuing to Task 3.

---

### Task 3: `phase3/c3/oracle.py`

**Files:**
- Create: `phase3/c3/oracle.py`

**Interfaces:**
- Consumes: `engine.Action` (Task 1), `monitor.MonitorState` (Task 2).
- Produces: `classify_claim(action: Action, prev_monitor: MonitorState) -> Optional[str]`, `is_exploit(action: Action, prev_monitor: MonitorState) -> bool`. Consumed by Tasks 4-5.

- [ ] **Step 1: Write the file**

```python
"""Runtime oracle. Unchanged from C2c -- transition-based, OR-based,
three-way. enchant_broken is never read here directly; it only reaches
claim()'s judgment by way of having already been captured into
buff_source_broken at some earlier channel(). See DESIGN_C3.md's
"Oracle -- unchanged from C2c" section.
"""
from __future__ import annotations

from typing import Optional

from engine import Action
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


def is_exploit(action: Action, prev_monitor: MonitorState) -> bool:
    return classify_claim(action, prev_monitor) is not None
```

- [ ] **Step 2: Sanity-run it**

Run (from `phase3/c3/`):
```bash
python -c "
from monitor import MonitorState
from engine import Action
from oracle import classify_claim
print(classify_claim(Action('claim'), MonitorState(False, False, False)))
print(classify_claim(Action('claim'), MonitorState(True, False, False)))
print(classify_claim(Action('claim'), MonitorState(False, True, True)))
print(classify_claim(Action('claim'), MonitorState(True, False, True)))
print(classify_claim(Action('equip','FlameSword'), MonitorState(True, True, True)))
"
```
Expected:
```
None
EQUIPMENT_CONTINUITY_VIOLATION
BUFF_SOURCE_LIFECYCLE_VIOLATION
BOTH
None
```
(Last line: non-`claim` actions always return `None`, regardless of monitor state.)

---

### Task 4: `phase3/c3/qa_reference.py`

**Files:**
- Create: `phase3/c3/qa_reference.py`

**Interfaces:**
- Consumes: `engine.Action`, `engine.REQUIRED_EQUIPMENT`, `engine.apply`, `engine.initial_world` (Task 1).
- Produces: `reference_continuity_broken(history: List[Action]) -> bool`, `reference_enchant_broken(history: List[Action]) -> bool`, `reference_buff_source_broken(history: List[Action]) -> bool`. Consumed by Task 5.

- [ ] **Step 1: Write the file**

```python
"""QA-only independent reference specification. Never imported by
engine.py, monitor.py, or oracle.py -- exists only so verify_c3.py can
check monitor_step() against a completely separately written computation
of each fact.

reference_buff_source_broken does not call reference_enchant_broken as a
subroutine (would reintroduce a shared-implementation risk between the
two independence checks) and does not mirror monitor_step's single-pass
incremental fold (would just be the same computation restated) -- it
locates the last channel by a plain scan, then checks the two sides of
it via separate replays. See DESIGN_C3.md's Step 1c for the derivation.
"""
from __future__ import annotations

from typing import List

from engine import Action, REQUIRED_EQUIPMENT, apply, initial_world


def reference_continuity_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        world = apply(world, action)
        if world.quest_status == "ACTIVE" and world.equipped != REQUIRED_EQUIPMENT:
            broken = True
    return broken


def reference_enchant_broken(history: List[Action]) -> bool:
    world = initial_world()
    broken = False
    for action in history:
        prev_enchanted = world.enchanted
        world = apply(world, action)
        if prev_enchanted and not world.enchanted:
            broken = True
    return broken


def reference_buff_source_broken(history: List[Action]) -> bool:
    last_channel_index = None
    for i, action in enumerate(history):
        if action.kind == "channel":
            last_channel_index = i
    if last_channel_index is None:
        return False

    world = initial_world()
    tainted_at_grant = False
    for action in history[:last_channel_index]:
        prev_enchanted = world.enchanted
        world = apply(world, action)
        if prev_enchanted and not world.enchanted:
            tainted_at_grant = True

    world = initial_world()
    for action in history[:last_channel_index + 1]:
        world = apply(world, action)
    broken_after_grant = False
    for action in history[last_channel_index + 1:]:
        world = apply(world, action)
        if world.equipped != REQUIRED_EQUIPMENT:
            broken_after_grant = True

    return tainted_at_grant or broken_after_grant
```

- [ ] **Step 2: Sanity-run against the same Hclean/Htainted pair**

Run (from `phase3/c3/`):
```bash
python -c "
from engine import Action
from qa_reference import reference_enchant_broken, reference_buff_source_broken

clean = [Action('equip','FlameSword'), Action('enchant'), Action('channel')]
tainted = [Action('equip','FlameSword'), Action('enchant'), Action('unenchant'), Action('enchant'), Action('channel')]
print('reference_enchant_broken clean/tainted (pre-channel prefix):',
      reference_enchant_broken(clean[:-1]), reference_enchant_broken(tainted[:-1]))
print('reference_buff_source_broken clean/tainted:',
      reference_buff_source_broken(clean), reference_buff_source_broken(tainted))
"
```
Expected:
```
reference_enchant_broken clean/tainted (pre-channel prefix): False True
reference_buff_source_broken clean/tainted: False True
```
Must match Task 2's `monitor_step`-based results exactly. If they diverge here, stop -- do not proceed to Task 5 until `monitor_step` and the reference agree on this specific pair (this is the pair `verify_c3.py` will assert on in Task 5, so catching a mismatch now is cheaper than debugging it inside the full closure sweep).

---

### Task 5: `phase3/c3/verify_c3.py`

**Files:**
- Create: `phase3/c3/verify_c3.py`

**Interfaces:**
- Consumes: everything Tasks 1-4 produce.
- Produces: a runnable script, terminal node of this plan.

- [ ] **Step 1: Write the file**

```python
"""C3 QA -- per DESIGN_C3.md (through C3c). No search algorithm is
imported or run anywhere in this file.

Step 1: monitor_step() vs. the three independent qa_reference facts,
checked via closure over the finite (WorldState, reference-values)
semantic space.

Indistinguishability pair: Hclean vs. Htainted, checked explicitly and
separately from the general closure sweep -- proves the sibling read in
buff_source_broken's channel branch is load-bearing, not cosmetic.

Step 1b: the sealed permanent negative control -- known_bad_monitor_step
(channel unconditionally cleanses buff_source_broken, ignoring upstream
provenance) must produce >= 1 mismatch.

Step 2 (only trustworthy once Step 1 passes): five minimality claims --
three oracle categories plus two pathway-constrained sub-claims for
BUFF_SOURCE_LIFECYCLE_VIOLATION, via classify_pathway().

Step 3: post-claim mutation regression, carried forward from C2c.

Run:
    python verify_c3.py
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional, Set, Tuple

from engine import Action, REQUIRED_EQUIPMENT, WorldState, apply, initial_world, legal_actions
from monitor import MonitorState, initial_monitor, monitor_step
from oracle import classify_claim
from qa_reference import (
    reference_buff_source_broken, reference_continuity_broken, reference_enchant_broken,
)

MonitorFn = Callable[[WorldState, Action, WorldState, MonitorState], MonitorState]


def known_bad_monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    """Negative control only -- never used outside this QA file. Reverts
    to C2's exact channel rule: channel unconditionally cleanses
    buff_source_broken, ignoring upstream enchant provenance entirely."""
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    enchant_broken = prev_monitor.enchant_broken
    if prev_world.enchanted and not new_world.enchanted:
        enchant_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = False  # BUG: ignores prev_monitor.enchant_broken
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, enchant_broken=enchant_broken,
                         buff_source_broken=buff_source_broken)


# name -> (path, expected oracle classification, expected pathway or None)
WITNESSES: Dict[str, Tuple[List[Action], Optional[str], Optional[str]]] = {
    "legitimate": (
        [Action("equip", "FlameSword"), Action("enchant"), Action("channel"),
         Action("accept"), Action("claim")],
        None, None,
    ),
    "EQUIPMENT_CONTINUITY_VIOLATION": (
        [Action("equip", "FlameSword"), Action("enchant"), Action("accept"),
         Action("equip", "WoodenSword"), Action("equip", "FlameSword"),
         Action("channel"), Action("claim")],
        "EQUIPMENT_CONTINUITY_VIOLATION", None,
    ),
    "BUFF_OLD_PATHWAY": (
        [Action("equip", "FlameSword"), Action("enchant"), Action("channel"),
         Action("equip", "WoodenSword"), Action("equip", "FlameSword"),
         Action("accept"), Action("claim")],
        "BUFF_SOURCE_LIFECYCLE_VIOLATION", "OLD_EQUIPMENT_SOURCE_PATHWAY",
    ),
    "BUFF_NEW_PATHWAY": (
        [Action("equip", "FlameSword"), Action("enchant"), Action("unenchant"),
         Action("enchant"), Action("accept"), Action("channel"), Action("claim")],
        "BUFF_SOURCE_LIFECYCLE_VIOLATION", "NEW_CHAIN_PATHWAY",
    ),
    "BOTH": (
        [Action("equip", "FlameSword"), Action("enchant"), Action("channel"),
         Action("accept"), Action("equip", "WoodenSword"), Action("equip", "FlameSword"),
         Action("claim")],
        "BOTH", None,
    ),
}


def run_closure(monitor_fn: MonitorFn, label: str) -> Tuple[int, int, int, List[Tuple[List[Action], MonitorState, Tuple[bool, bool, bool]]], Set[Tuple[bool, bool, bool]]]:
    print(f"--- closure run: {label} ---")
    seen: Dict[Tuple[WorldState, bool, bool, bool], Tuple[WorldState, MonitorState, List[Action]]] = {}
    frontier: Dict[Tuple[WorldState, MonitorState], List[Action]] = {
        (initial_world(), initial_monitor()): []
    }
    checked = 0
    layers = 0
    mismatches: List[Tuple[List[Action], MonitorState, Tuple[bool, bool, bool]]] = []
    reachable_triples: Set[Tuple[bool, bool, bool]] = set()

    while frontier:
        layers += 1
        discovered_this_layer: Dict[Tuple[WorldState, bool, bool, bool], Tuple[WorldState, MonitorState, List[Action]]] = {}
        for (world, monitor), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_path = path + [action]
                new_monitor = monitor_fn(world, action, new_world, monitor)
                ref_cont = reference_continuity_broken(new_path)
                ref_ench = reference_enchant_broken(new_path)
                ref_buff = reference_buff_source_broken(new_path)
                checked += 1
                reachable_triples.add((ref_cont, ref_ench, ref_buff))
                got = (new_monitor.continuity_broken, new_monitor.enchant_broken, new_monitor.buff_source_broken)
                if got != (ref_cont, ref_ench, ref_buff):
                    mismatches.append((new_path, new_monitor, (ref_cont, ref_ench, ref_buff)))
                key = (new_world, ref_cont, ref_ench, ref_buff)
                if key not in seen and key not in discovered_this_layer:
                    discovered_this_layer[key] = (new_world, new_monitor, new_path)
        if not discovered_this_layer:
            break
        seen.update(discovered_this_layer)
        frontier = {(w, m): p for w, m, p in discovered_this_layer.values()}

    print(f"  transitions checked: {checked}")
    print(f"  layers to closure:   {layers}")
    print(f"  distinct semantic states found: {len(seen)}  (C2 comparison: reachable 19 of 48 theoretical)")
    print(f"  reachable (continuity, enchant, buff) triples: {sorted(reachable_triples)}")
    if mismatches:
        print(f"  {len(mismatches)} mismatch(es) vs. reference:")
        for path, got, expected in mismatches[:5]:
            print(f"    path={path}  {label}={got}  reference={expected}")
    else:
        print("  0 mismatches vs. reference")
    return checked, layers, len(seen), mismatches, reachable_triples


def step1_production() -> Optional[Set[Tuple[bool, bool, bool]]]:
    print("=== Step 1: production monitor_step vs. reference, semantic closure ===")
    _, _, _, mismatches, triples = run_closure(monitor_step, "monitor_step")
    if mismatches:
        print("  FAIL: production monitor must have 0 mismatches")
        return None
    print("  PASS")
    return triples


def check_indistinguishability_pair() -> bool:
    print()
    print("=== Indistinguishability pair check (Hclean vs Htainted) ===")
    Hclean = [Action("equip", "FlameSword"), Action("enchant")]
    Htainted = [Action("equip", "FlameSword"), Action("enchant"), Action("unenchant"), Action("enchant")]

    def replay_prefix(prefix):
        world, monitor = initial_world(), initial_monitor()
        for action in prefix:
            new_world = apply(world, action)
            monitor = monitor_step(world, action, new_world, monitor)
            world = new_world
        return world, monitor

    w_clean, m_clean = replay_prefix(Hclean)
    w_tainted, m_tainted = replay_prefix(Htainted)

    ok = True
    if w_clean != w_tainted:
        print(f"  FAIL: WorldState differs before channel -- clean={w_clean} tainted={w_tainted}")
        ok = False
    if m_clean.buff_source_broken != m_tainted.buff_source_broken:
        print(f"  FAIL: prior buff_source_broken differs -- clean={m_clean.buff_source_broken} tainted={m_tainted.buff_source_broken}")
        ok = False
    if m_clean.enchant_broken == m_tainted.enchant_broken:
        print(f"  FAIL: enchant_broken should differ but both are {m_clean.enchant_broken}")
        ok = False
    if not ok:
        return False

    channel = Action("channel")
    new_w_clean = apply(w_clean, channel)
    new_m_clean = monitor_step(w_clean, channel, new_w_clean, m_clean)
    new_w_tainted = apply(w_tainted, channel)
    new_m_tainted = monitor_step(w_tainted, channel, new_w_tainted, m_tainted)

    print(f"  Hclean   + channel -> buff_source_broken={new_m_clean.buff_source_broken}")
    print(f"  Htainted + channel -> buff_source_broken={new_m_tainted.buff_source_broken}")
    if new_m_clean.buff_source_broken == new_m_tainted.buff_source_broken:
        print("  FAIL: identical prior inputs produced identical outputs -- pair doesn't isolate the sibling read")
        return False
    if new_m_clean.buff_source_broken or not new_m_tainted.buff_source_broken:
        print("  FAIL: results don't match the intended direction (clean=False, tainted=True)")
        return False
    print("  PASS: component-wise-independent fold is provably insufficient -- confirmed by construction")
    return True


def step1b_negative_control() -> bool:
    print()
    print("=== Step 1b: negative control (known_bad_monitor_step must fail) ===")
    _, _, _, mismatches, _ = run_closure(known_bad_monitor_step, "known_bad_monitor_step")
    ok = len(mismatches) >= 1
    print(f"  {'PASS' if ok else 'FAIL'}: negative control produced {len(mismatches)} mismatch(es) (requirement: >= 1)")
    return ok


def check_independence(triples: Set[Tuple[bool, bool, bool]]) -> bool:
    print()
    print("=== Independence check (continuity, buff) -- unchanged claim from C2c ===")
    pairs = {(c, b) for c, _, b in triples}
    print(f"  reachable (continuity, buff) pairs: {sorted(pairs)}")
    has_eq_only = (True, False) in pairs
    has_buf_only = (False, True) in pairs
    ok = has_eq_only and has_buf_only
    print(f"  (continuity=True, buff=False) reachable: {has_eq_only}")
    print(f"  (continuity=False, buff=True) reachable: {has_buf_only}")
    print(f"  {'PASS' if ok else 'FAIL'}: both divergent combinations must be reachable")
    return ok


def classify_pathway(path: List[Action]) -> Optional[str]:
    """Only meaningful when classify_claim(path's claim, ...) already
    returned "BUFF_SOURCE_LIFECYCLE_VIOLATION" -- callers must gate on
    that; this function never inspects continuity_broken itself."""
    last_channel_index = None
    for i, action in enumerate(path):
        if action.kind == "channel":
            last_channel_index = i
    if last_channel_index is None:
        return None

    world, monitor = initial_world(), initial_monitor()
    for action in path[:last_channel_index + 1]:
        new_world = apply(world, action)
        monitor = monitor_step(world, action, new_world, monitor)
        world = new_world
    tainted_at_grant = monitor.buff_source_broken

    broken_after_grant = False
    for action in path[last_channel_index + 1:]:
        world = apply(world, action)
        if world.equipped != REQUIRED_EQUIPMENT:
            broken_after_grant = True

    if tainted_at_grant and not broken_after_grant:
        return "NEW_CHAIN_PATHWAY"
    if not tainted_at_grant and broken_after_grant:
        return "OLD_EQUIPMENT_SOURCE_PATHWAY"
    return None


def replay(path: List[Action]) -> Tuple[Optional[str], bool]:
    world, monitor = initial_world(), initial_monitor()
    verdict: Optional[str] = None
    for action in path:
        if action not in legal_actions(world):
            return None, False
        if action.kind == "claim":
            verdict = classify_claim(action, monitor)
        new_world = apply(world, action)
        monitor = monitor_step(world, action, new_world, monitor)
        world = new_world
    return verdict, True


def step2_minimality() -> bool:
    print()
    print("=== Step 2: minimality (only trustworthy since Step 1 passed) ===")
    ok = True

    for name, (path, expected_oracle, expected_pathway) in WITNESSES.items():
        verdict, legal = replay(path)
        if not legal:
            print(f"  FAIL: {name} witness contains an illegal action")
            ok = False
            continue
        if verdict != expected_oracle:
            print(f"  FAIL: {name} witness classified as {verdict}, expected {expected_oracle}")
            ok = False
            continue
        if expected_pathway is not None:
            pathway = classify_pathway(path)
            if pathway != expected_pathway:
                print(f"  FAIL: {name} witness pathway={pathway}, expected {expected_pathway}")
                ok = False
                continue
            print(f"  {name} witness OK: {len(path)} actions, classify={verdict}, pathway={pathway}")
        else:
            print(f"  {name} witness OK: {len(path)} actions, classify={verdict}")

    if not ok:
        return False

    SearchState = Tuple[WorldState, MonitorState]
    max_depth = max(len(p) for _, (p, cat, _) in WITNESSES.items() if cat is not None) - 1
    start: SearchState = (initial_world(), initial_monitor())
    frontier: Dict[SearchState, List[Action]] = {start: []}
    visited = {start}
    early_hits: Dict[str, List[Action]] = {}

    for depth in range(1, max_depth + 1):
        next_frontier: Dict[SearchState, List[Action]] = {}
        for (world, monitor), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_monitor = monitor_step(world, action, new_world, monitor)
                new_state = (new_world, new_monitor)
                new_path = path + [action]
                if action.kind == "claim":
                    cat = classify_claim(action, monitor)
                    if cat is not None and cat not in early_hits:
                        early_hits[cat] = new_path
                    if cat == "BUFF_SOURCE_LIFECYCLE_VIOLATION":
                        pathway = classify_pathway(new_path)
                        if pathway is not None and pathway not in early_hits:
                            early_hits[pathway] = new_path
                if new_state in visited:
                    continue
                visited.add(new_state)
                next_frontier[new_state] = new_path
        frontier = next_frontier
        if not frontier:
            break

    print(f"  exhaustive search to depth {max_depth}: {len(visited)} SearchStates visited")
    targets = [
        "EQUIPMENT_CONTINUITY_VIOLATION", "BUFF_SOURCE_LIFECYCLE_VIOLATION",
        "OLD_EQUIPMENT_SOURCE_PATHWAY", "NEW_CHAIN_PATHWAY", "BOTH",
    ]
    for name in targets:
        if name in early_hits:
            print(f"  FAIL: {name} reached early at depth {len(early_hits[name])} (<= {max_depth}): {early_hits[name]}")
            ok = False
        else:
            print(f"  no shortcut for {name}: not reached within depth {max_depth}")

    return ok


def step3_post_claim_regression() -> bool:
    print()
    print("=== Step 3: post-claim mutation regression (carried forward from C2c) ===")
    ok = True

    path_a = [
        Action("equip", "FlameSword"), Action("enchant"), Action("accept"),
        Action("channel"), Action("claim"), Action("equip", "WoodenSword"),
    ]
    verdict_a, legal_a = replay(path_a)
    if not legal_a:
        print("  FAIL: (a) path contains an illegal action")
        ok = False
    elif verdict_a is not None:
        print(f"  FAIL: (a) legitimate claim retroactively reclassified as {verdict_a} by post-claim action")
        ok = False
    else:
        print("  (a) PASS: legitimate claim stays legitimate after post-claim equip swap")

    path_b = [
        Action("equip", "FlameSword"), Action("enchant"), Action("channel"),
        Action("equip", "WoodenSword"), Action("equip", "FlameSword"),
        Action("accept"), Action("claim"), Action("channel"),
    ]
    verdict_b, legal_b = replay(path_b)
    if not legal_b:
        print("  FAIL: (b) path contains an illegal action")
        ok = False
    elif verdict_b != "BUFF_SOURCE_LIFECYCLE_VIOLATION":
        print(f"  FAIL: (b) exploit claim verdict was {verdict_b}, expected BUFF_SOURCE_LIFECYCLE_VIOLATION (must not be erased by post-claim channel)")
        ok = False
    else:
        print("  (b) PASS: exploit claim verdict survives a post-claim channel() revalidation")

    return ok


if __name__ == "__main__":
    triples = step1_production()
    ok1 = triples is not None
    ok_pair = check_indistinguishability_pair()
    ok1b = step1b_negative_control()
    ok_indep = check_independence(triples) if ok1 else False
    ok2 = step2_minimality() if ok1 else False
    ok3 = step3_post_claim_regression() if ok1 else False

    print()
    if not ok1:
        print("C3 QA: FAIL at Step 1 -- later steps not run (untrustworthy until Step 1 passes)")
    else:
        overall = ok1 and ok_pair and ok1b and ok_indep and ok2 and ok3
        print("C3 QA: " + ("PASS" if overall else "FAIL"))
```

- [ ] **Step 2: Run it**

Run (from `phase3/c3/`):
```bash
python verify_c3.py
```
Expected: every check prints `PASS`, ending with `C3 QA: PASS`. If anything prints `FAIL`, stop and diagnose -- per this project's established discipline, a `FAIL` here means either the implementation has a bug or `DESIGN_C3.md` itself needs another reviewed correction (same pattern as every prior C1b/C1c/C2b/C2c/C3b/C3c round). Do not edit `verify_c3.py` to make a failure disappear.

- [ ] **Step 3: Confirm C1/C2 untouched**

Run (from repo root):
```bash
git status --short phase3/*.py phase3/c2/ phase3/c3/
```
Expected: only new files under `phase3/c3/`; no modifications to `phase3/*.py` (C1) or `phase3/c2/*.py` (C2's sealed core -- search algorithms from `0025e55` are untouched by this plan).

- [ ] **Step 4: Commit**

```bash
git add phase3/c3/engine.py phase3/c3/monitor.py phase3/c3/oracle.py phase3/c3/qa_reference.py phase3/c3/verify_c3.py
git commit -m "Phase 3 C3 core: engine/monitor/oracle/qa_reference/verify, PASS"
```

(Full commit message with actual observed numbers -- transitions/layers/semantic-states, mismatch counts, reachable triples -- to be filled in from the real Step 2 output before committing, same convention as C1's `9ec6249` and C2's `6aab686`.)

---

## Self-Review Notes

- **Spec coverage:** `channel()`'s new precondition + no-op-ban exemption (Task 1) / `enchant`/`unenchant` actions (Task 1) / grant-time capture in `monitor_step` (Task 2) / oracle unchanged (Task 3) / three independent reference functions with the specified non-sharing structure (Task 4) / `Hclean`/`Htainted` dedicated check (Task 5) / sealed negative control (Task 5) / five minimality claims with `classify_pathway` gating (Task 5) / post-claim regression carried forward (Task 5) -- all covered.
- **Placeholder scan:** none -- every step has runnable code and a concrete expected-output description.
- **Type consistency:** `WorldState(equipped, quest_status, has_flame_buff, enchanted)` used identically across all five files. `MonitorState(continuity_broken, enchant_broken, buff_source_broken)` likewise. `classify_claim(action, prev_monitor)` / `classify_pathway(path)` signatures match between their definitions (Task 3, Task 5) and every call site (Task 5's `step2_minimality`, `replay`).
