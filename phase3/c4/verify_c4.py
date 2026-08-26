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
