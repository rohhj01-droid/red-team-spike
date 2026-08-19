"""C2 QA -- per DESIGN_C2.md. No search algorithm is imported or run
anywhere in this file.

Step 1: monitor_step() vs. the two independent qa_reference facts,
checked via closure over the finite (WorldState, reference-values)
semantic space -- not an arbitrary path-depth bound (raw action-history
space is infinite: equip(Flame) <-> equip(Wood) toggles forever).

Step 1b: the sealed permanent negative control. known_bad_monitor_step
("re-equipping alone revalidates the buff") run through the identical
closure procedure must produce >= 1 mismatch against the same reference
-- proof the check is actually sensitive, not vacuously passing.

Step 2 (only trustworthy once Step 1 passes): per-category minimality
for EQUIPMENT_CONTINUITY_VIOLATION / BUFF_SOURCE_LIFECYCLE_VIOLATION /
BOTH, plus a legitimate-completion sanity check.

Run:
    python verify_c2.py
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional, Set, Tuple

from engine import Action, WorldState, apply, initial_world, legal_actions
from monitor import MonitorState, initial_monitor, monitor_step
from oracle import classify_claim
from qa_reference import reference_buff_source_broken, reference_continuity_broken

MonitorFn = Callable[[WorldState, Action, WorldState, MonitorState], MonitorState]


def known_bad_monitor_step(prev_world: WorldState, action: Action, new_world: WorldState, prev_monitor: MonitorState) -> MonitorState:
    """Negative control only -- never used outside this QA file. Encodes
    C2's actual new lesson backwards: re-equipping the required item is
    treated as revalidating the buff, when only channel() should."""
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != "FlameSword":
        continuity_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if new_world.equipped == "FlameSword":
        buff_source_broken = False  # BUG: re-equipping alone "revalidates" -- no channel() needed
    elif prev_world.has_flame_buff and new_world.equipped != "FlameSword":
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, buff_source_broken=buff_source_broken)


WITNESSES: Dict[str, List[Action]] = {
    "legitimate": [
        Action("equip", "FlameSword"),
        Action("channel"),
        Action("accept"),
        Action("claim"),
    ],
    "EQUIPMENT_CONTINUITY_VIOLATION": [
        Action("equip", "FlameSword"),
        Action("accept"),
        Action("equip", "WoodenSword"),
        Action("equip", "FlameSword"),
        Action("channel"),
        Action("claim"),
    ],
    "BUFF_SOURCE_LIFECYCLE_VIOLATION": [
        Action("equip", "FlameSword"),
        Action("channel"),
        Action("equip", "WoodenSword"),
        Action("equip", "FlameSword"),
        Action("accept"),
        Action("claim"),
    ],
    "BOTH": [
        Action("equip", "FlameSword"),
        Action("channel"),
        Action("accept"),
        Action("equip", "WoodenSword"),
        Action("equip", "FlameSword"),
        Action("claim"),
    ],
}


def run_closure(monitor_fn: MonitorFn, label: str) -> Tuple[int, int, int, List[Tuple[List[Action], MonitorState, Tuple[bool, bool]]], Set[Tuple[bool, bool]]]:
    print(f"--- closure run: {label} ---")
    seen: Dict[Tuple[WorldState, bool, bool], Tuple[WorldState, MonitorState, List[Action]]] = {}
    frontier: Dict[Tuple[WorldState, MonitorState], List[Action]] = {
        (initial_world(), initial_monitor()): []
    }
    checked = 0
    layers = 0
    mismatches: List[Tuple[List[Action], MonitorState, Tuple[bool, bool]]] = []
    reachable_pairs: Set[Tuple[bool, bool]] = set()

    while frontier:
        layers += 1
        discovered_this_layer: Dict[Tuple[WorldState, bool, bool], Tuple[WorldState, MonitorState, List[Action]]] = {}
        for (world, monitor), path in frontier.items():
            for action in legal_actions(world):
                new_world = apply(world, action)
                new_path = path + [action]
                new_monitor = monitor_fn(world, action, new_world, monitor)
                ref_eq = reference_continuity_broken(new_path)
                ref_buf = reference_buff_source_broken(new_path)
                checked += 1
                reachable_pairs.add((ref_eq, ref_buf))
                if (new_monitor.continuity_broken, new_monitor.buff_source_broken) != (ref_eq, ref_buf):
                    mismatches.append((new_path, new_monitor, (ref_eq, ref_buf)))
                key = (new_world, ref_eq, ref_buf)
                if key not in seen and key not in discovered_this_layer:
                    discovered_this_layer[key] = (new_world, new_monitor, new_path)
        if not discovered_this_layer:
            break
        seen.update(discovered_this_layer)
        frontier = {(w, m): p for w, m, p in discovered_this_layer.values()}

    print(f"  transitions checked: {checked}")
    print(f"  layers to closure:   {layers}")
    print(f"  distinct semantic states found: {len(seen)}  (C1 comparison: 12, 13, 7)")
    print(f"  reachable (continuity_broken, buff_source_broken) pairs: {sorted(reachable_pairs)}")
    if mismatches:
        print(f"  {len(mismatches)} mismatch(es) vs. reference:")
        for path, got, expected in mismatches[:5]:
            print(f"    path={path}  {label}={got}  reference={expected}")
    else:
        print("  0 mismatches vs. reference")
    return checked, layers, len(seen), mismatches, reachable_pairs


def step1_production() -> Optional[Set[Tuple[bool, bool]]]:
    print("=== Step 1: production monitor_step vs. reference, semantic closure ===")
    _, _, _, mismatches, pairs = run_closure(monitor_step, "monitor_step")
    if mismatches:
        print("  FAIL: production monitor must have 0 mismatches")
        return None
    print("  PASS")
    return pairs


def step1b_negative_control() -> bool:
    print()
    print("=== Step 1b: negative control (known_bad_monitor_step must fail) ===")
    _, _, _, mismatches, _ = run_closure(known_bad_monitor_step, "known_bad_monitor_step")
    ok = len(mismatches) >= 1
    print(f"  {'PASS' if ok else 'FAIL'}: negative control produced {len(mismatches)} mismatch(es) (requirement: >= 1)")
    return ok


def check_independence(pairs: Set[Tuple[bool, bool]]) -> bool:
    print()
    print("=== Independence check ===")
    print(f"  reachable pairs: {sorted(pairs)}")
    has_eq_only = (True, False) in pairs
    has_buf_only = (False, True) in pairs
    ok = has_eq_only and has_buf_only
    print(f"  (continuity=True, buff=False) reachable: {has_eq_only}")
    print(f"  (continuity=False, buff=True) reachable: {has_buf_only}")
    print(f"  {'PASS' if ok else 'FAIL'}: both divergent combinations must be reachable")
    return ok


def replay(witness: List[Action]) -> Tuple[Optional[str], bool]:
    """Returns the classification recorded at the witness's `claim`
    transition (None if no claim occurs), not a re-derivation from the
    final state -- per the C2c transition-based oracle. Actions after the
    claim still advance world/monitor (so callers can inspect the
    post-claim state too) but must not change the returned verdict."""
    world, monitor = initial_world(), initial_monitor()
    verdict: Optional[str] = None
    for action in witness:
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

    for name, witness in WITNESSES.items():
        result, legal = replay(witness)
        expected = None if name == "legitimate" else name
        if not legal:
            print(f"  FAIL: {name} witness contains an illegal action")
            ok = False
            continue
        if result != expected:
            print(f"  FAIL: {name} witness classified as {result}, expected {expected}")
            ok = False
        else:
            print(f"  {name} witness OK: {len(witness)} actions, classify={result}")

    if not ok:
        return False

    # Exhaustive SearchState-deduped search up to depth 5 (shortest violation
    # witness minus 1): none of the three violation categories may appear
    # earlier than their candidate witness's length.
    SearchState = Tuple[WorldState, MonitorState]
    max_depth = max(len(w) for k, w in WITNESSES.items() if k != "legitimate") - 1  # 5
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
                # Checked at the claim transition itself (prev_monitor),
                # not at the resulting state -- per the C2c oracle.
                if action.kind == "claim":
                    cat = classify_claim(action, monitor)
                    if cat is not None and cat not in early_hits:
                        early_hits[cat] = new_path
                if new_state in visited:
                    continue
                visited.add(new_state)
                next_frontier[new_state] = new_path
        frontier = next_frontier
        if not frontier:
            break

    print(f"  exhaustive search to depth {max_depth}: {len(visited)} SearchStates visited")
    for name in ("EQUIPMENT_CONTINUITY_VIOLATION", "BUFF_SOURCE_LIFECYCLE_VIOLATION", "BOTH"):
        if name in early_hits:
            print(f"  FAIL: {name} reached early at depth {len(early_hits[name])} (< {len(WITNESSES[name])}): {early_hits[name]}")
            ok = False
        else:
            print(f"  no shortcut for {name}: not reached within depth {max_depth}")

    return ok


def step3_post_claim_regression() -> bool:
    print()
    print("=== Step 3: post-claim mutation regression (transition-locality) ===")
    ok = True

    # (a) A legitimate claim followed by an unrelated post-claim mutation
    # must NOT retroactively read as an exploit. This is the exact FAIL
    # the state-based oracle produced before the C2c correction.
    path_a = [
        Action("equip", "FlameSword"),
        Action("accept"),
        Action("channel"),
        Action("claim"),
        Action("equip", "WoodenSword"),
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

    # (b) An exploit claim followed by a post-claim channel() (which
    # resets *current* buff_source_broken) must NOT erase the
    # already-recorded verdict.
    path_b = [
        Action("equip", "FlameSword"),
        Action("channel"),
        Action("equip", "WoodenSword"),
        Action("equip", "FlameSword"),
        Action("accept"),
        Action("claim"),
        Action("channel"),
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
    pairs = step1_production()
    ok1 = pairs is not None
    ok1b = step1b_negative_control()
    ok_indep = check_independence(pairs) if ok1 else False
    ok2 = step2_minimality() if ok1 else False
    ok3 = step3_post_claim_regression() if ok1 else False

    print()
    if not ok1:
        print("C2 QA: FAIL at Step 1 -- Step 2/3 not run (untrustworthy until Step 1 passes)")
    else:
        overall = ok1 and ok1b and ok_indep and ok2 and ok3
        print("C2 QA: " + ("PASS" if overall else "FAIL"))
