"""C1 QA -- two ordered steps per DESIGN_C1.md. No search algorithm is
imported or run anywhere in this file.

Step 1: monitor_step() vs. the independent qa_reference implementation,
checked via closure over the finite (WorldState, reference-value)
semantic space -- not an arbitrary path-depth bound (the raw action
history space is infinite: equip(Flame) <-> equip(Wood) toggles forever).

Step 2 (only trustworthy once Step 1 passes): minimality. No exploit
below depth 5; the declared 5-action witness succeeds.

Run:
    python verify_c1.py
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine import Action, WorldState, apply, initial_world, legal_actions
from monitor import MonitorState, initial_monitor, monitor_step
from oracle import is_exploit
from qa_reference import reference_continuity_broken

WITNESS = [
    Action("equip", "FlameSword"),
    Action("accept"),
    Action("equip", "WoodenSword"),
    Action("equip", "FlameSword"),
    Action("claim"),
]


def step1_closure_equivalence() -> bool:
    print("=== Step 1: monitor_step vs. reference, semantic closure ===")
    seen: Dict[Tuple[WorldState, bool], List[Action]] = {}
    frontier: Dict[Tuple[WorldState, MonitorState], List[Action]] = {
        (initial_world(), initial_monitor()): []
    }
    checked = 0
    layers = 0
    mismatches: List[Tuple[List[Action], bool, bool]] = []

    while frontier:
        layers += 1
        discovered_this_layer: Dict[Tuple[WorldState, bool], Tuple[WorldState, MonitorState, List[Action]]] = {}
        for (world, monitor), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_path = path + [action]
                new_monitor = monitor_step(world, action, new_world, monitor)
                ref = reference_continuity_broken(new_path)
                checked += 1
                if new_monitor.continuity_broken != ref:
                    mismatches.append((new_path, new_monitor.continuity_broken, ref))
                key = (new_world, ref)
                if key not in seen and key not in discovered_this_layer:
                    discovered_this_layer[key] = (new_world, new_monitor, new_path)
        if not discovered_this_layer:
            break
        seen.update(discovered_this_layer)
        frontier = {(w, m): p for w, m, p in discovered_this_layer.values()}

    print(f"  transitions checked: {checked}")
    print(f"  layers to closure:   {layers}")
    print(f"  distinct semantic states (WorldState, reference) found: {len(seen)}")
    for (world, ref) in sorted(seen, key=lambda k: (k[0].quest_status, k[0].equipped, k[1])):
        print(f"    {world}  continuity_broken={ref}")

    if mismatches:
        print(f"  FAIL: {len(mismatches)} mismatch(es) between monitor_step and reference:")
        for path, got, expected in mismatches[:5]:
            print(f"    path={path}  monitor_step={got}  reference={expected}")
        return False
    print("  PASS: monitor_step agrees with the independent reference on every checked transition")
    return True


def step2_minimality() -> bool:
    print()
    print("=== Step 2: minimality (only trustworthy since Step 1 passed) ===")
    ok = True

    # (a) witness is legal and reaches is_exploit == True
    world, monitor = initial_world(), initial_monitor()
    for action in WITNESS:
        if action not in legal_actions(world):
            print(f"  FAIL: witness action {action} illegal at {world}")
            return False
        new_world = apply(world, action)
        monitor = monitor_step(world, action, new_world, monitor)
        world = new_world
    if not is_exploit(world, monitor):
        print(f"  FAIL: witness does not reach is_exploit -- final world={world} monitor={monitor}")
        ok = False
    else:
        print(f"  witness OK: {len(WITNESS)} actions, reaches is_exploit=True")

    # (b) exhaustive SearchState-deduped search up to depth 4: no exploit
    SearchState = Tuple[WorldState, MonitorState]
    start: SearchState = (initial_world(), initial_monitor())
    frontier: Dict[SearchState, List[Action]] = {start: []}
    visited = {start}
    max_depth = len(WITNESS) - 1  # 4

    for depth in range(1, max_depth + 1):
        next_frontier: Dict[SearchState, List[Action]] = {}
        for (world, monitor), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_monitor = monitor_step(world, action, new_world, monitor)
                new_state = (new_world, new_monitor)
                new_path = path + [action]
                if is_exploit(new_world, new_monitor):
                    print(f"  FAIL: exploit found at depth {depth} (< 5): {new_path}")
                    return False
                if new_state in visited:
                    continue
                visited.add(new_state)
                next_frontier[new_state] = new_path
        frontier = next_frontier
        if not frontier:
            break

    print(f"  no shortcut: exhaustive search to depth {max_depth} found no exploit ({len(visited)} states visited)")
    return ok


if __name__ == "__main__":
    ok1 = step1_closure_equivalence()
    ok2 = step2_minimality() if ok1 else False
    print()
    if not ok1:
        print("C1 QA: FAIL at Step 1 -- Step 2 not run (untrustworthy until Step 1 passes)")
    else:
        print("C1 QA: " + ("PASS" if ok2 else "FAIL"))
