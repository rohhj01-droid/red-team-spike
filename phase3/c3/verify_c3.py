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
