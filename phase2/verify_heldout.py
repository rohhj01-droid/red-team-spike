"""D.5 benchmark QA -- held-out suite (H1-H3). Confirms the exact
instances satisfy their sealed category conditions and contain no
accidental shortcuts or false positives.

DOES NOT IMPORT search.py's random_search/beam_naive_search/
beam_diverse_search/mcts_search, OR graph_baseline.py, ANYWHERE in this
file. No search algorithm is executed against H1-H3 in this commit --
that is Commit E's job, once, after this QA is the only thing that has
touched them. `search.score`/`search.estimate_values` ARE imported for
the H2 valley check below, but that is reading the FROZEN scoring
*formula* as a benchmark-construction yardstick ("does this case satisfy
its own sealed definition"), not running Beam-Diverse's search over the
case -- no exploration, no discovery, nothing that answers "would Beam
find this."

Run:
    python verify_heldout.py
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from cases_dev import Case
from cases_heldout_exact import ALL_HELDOUT_CASES
from engine import Action, GameState, apply, initial_state, legal_actions
from frozen_params import MAX_DEPTH as FROZEN_MAX_DEPTH
from oracle import is_exploit_found, realized_gold_gain
from verify_cases import DEPTH_HEADROOM, DISTRACTOR_ONLY_DEPTH, exhaustive_profitable_states, verify_case


def check_fits_frozen_depth(case: Case) -> bool:
    ok = len(case.minimal_path) <= FROZEN_MAX_DEPTH
    verdict = "OK" if ok else "FAIL"
    print(f"  fits frozen MAX_DEPTH={FROZEN_MAX_DEPTH}: {verdict} (minimal_path={len(case.minimal_path)})")
    return ok


def check_initial_inventory_no_direct_sale(case: Case) -> bool:
    """Oracle-validity constraint from cases_heldout.py H1/H3: nothing in
    initial_inventory may have a direct shop_sell entry (the cheapest
    possible accidental liquidation)."""
    if not case.data.initial_inventory:
        print("  initial_inventory: empty, oracle-validity constraint not applicable")
        return True
    offenders = [item for item, _ in case.data.initial_inventory if item in case.data.shop_sell]
    ok = not offenders
    if ok:
        print(f"  initial_inventory items have no direct shop_sell entry: OK {dict(case.data.initial_inventory)}")
    else:
        print(f"  FAIL: initial_inventory items directly sellable: {offenders}")
    return ok


def verify_case_shared_resource(case: Case) -> bool:
    """For H3 only. verify_cases.verify_case's structural-disjointness
    check assumes distractor items never appear in the same recipe as a
    real item -- true for dev (distractors are a fully separate item
    family) but FALSE FOR H3 BY DESIGN: Trinket3 (distractor-labeled,
    the wrong branch) necessarily consumes the same Gem the profitable
    Amulet recipe does -- that shared consumption IS the branching-choice
    mechanism, not an accidental leak. Applying dev's disjointness
    invariant here would flag correct-by-design behavior as a defect, so
    this mirrors verify_case's other checks (minimal_path correctness, no
    shortcut, distractor-only-never-profitable) and skips only that one.
    distractor_items = {Scrap, Trinket3, Widget2} excludes Amulet, so the
    distractor-only search below already answers the real question for
    H3: without ever crafting/selling Amulet, is there any profit? No.
    """
    print(f"--- {case.name}: {case.mechanism}")
    ok = True

    expected_gain = realized_gold_gain(case.data, case.minimal_path)
    if not is_exploit_found(case.data, case.minimal_path):
        print(f"  FAIL: declared minimal_path does not realize profit (gain={expected_gain})")
        ok = False
    else:
        print(f"  minimal_path OK: {len(case.minimal_path)} actions, +{expected_gain} gold")

    max_depth = len(case.minimal_path) + DEPTH_HEADROOM
    profitable = exhaustive_profitable_states(case.data, max_depth)
    if not profitable:
        print(f"  FAIL: exhaustive search up to depth {max_depth} found no profitable state at all")
        return False

    first_depth = profitable[0][0]
    if first_depth < len(case.minimal_path):
        print(f"  FAIL: a shorter profitable path exists at depth {first_depth}: {profitable[0][1]}")
        ok = False
    else:
        print(f"  no shortcut: nothing profitable before depth {len(case.minimal_path)}")

    print("  structural disjointness: SKIPPED (Gem is intentionally shared between Amulet and Trinket3 -- see docstring)")

    distractor_only = exhaustive_profitable_states(case.data, DISTRACTOR_ONLY_DEPTH, allowed_targets=set(case.distractor_items))
    if distractor_only:
        print("  FAIL: distractor-only search found profit (i.e. profit without ever touching Amulet):")
        for depth, path, gain in distractor_only:
            print(f"    depth={depth} gain={gain} path={path}")
        ok = False
    else:
        print(
            f"  distractor-only search OK: without ever crafting/selling Amulet, no profitable "
            f"state up to depth {DISTRACTOR_ONLY_DEPTH} (confirms Amulet is necessary, not just sufficient)"
        )

    action_types = len(case.data.shop_buy) + len(case.data.shop_sell) + len(case.data.recipes) + len(case.data.dismantle)
    print(f"  nominal action types: {action_types}, minimal exploit depth: {len(case.minimal_path)}")
    return ok


def h2_valley_check(case: Case, max_depth: int) -> bool:
    """Exhaustive (state, has_crossed_valley) BFS. Reading the frozen
    score() formula as a yardstick only -- see module docstring."""
    from search import estimate_values, score  # frozen formula, not a search run

    value = estimate_values(case.data)
    start = initial_state(case.data)
    baseline = score(case.data, value, start)

    start_key = (start, False)
    frontier: Dict[Tuple[GameState, bool], List[Action]] = {start_key: []}
    visited = {start_key}
    violations: List[Tuple[int, List[Action]]] = []

    for depth in range(1, max_depth + 1):
        next_frontier: Dict[Tuple[GameState, bool], List[Action]] = {}
        for (state, dipped), path in frontier.items():
            for action in legal_actions(case.data, state):
                new_state = apply(case.data, state, action)
                new_dipped = dipped or (score(case.data, value, new_state) < baseline - 1e-9)
                key = (new_state, new_dipped)
                if key in visited:
                    continue
                visited.add(key)
                new_path = path + [action]
                if new_state.gold > case.data.starting_gold and not new_dipped:
                    violations.append((depth, new_path))
                next_frontier[key] = new_path
        frontier = next_frontier
        if not frontier:
            break

    if violations:
        print(f"  FAIL: {len(violations)} profitable path(s) reach profit WITHOUT ever dipping below baseline score={baseline}:")
        for depth, path in violations[:5]:
            print(f"    depth={depth} path={path}")
        return False
    print(f"  H2 valley check OK: every profitable path dips below baseline score={baseline} at least once before paying off")
    return True


if __name__ == "__main__":
    results = []
    for case in ALL_HELDOUT_CASES:
        print(f"=== {case.name} ===")
        if case.name == "H3":
            ok = verify_case_shared_resource(case)  # disjointness doesn't apply -- see its docstring
        else:
            ok = verify_case(case)  # reuses dev's exact QA: minimal_path correctness, no shortcut, structural disjointness, distractor-only
        ok &= check_fits_frozen_depth(case)
        ok &= check_initial_inventory_no_direct_sale(case)
        if case.name == "H2":
            # Full frozen MAX_DEPTH, not minimal_path+headroom -- Commit E's
            # algorithms search up to 36, so "no valley-free path" must be
            # proven over that whole horizon, not just near the minimal path.
            ok &= h2_valley_check(case, max_depth=FROZEN_MAX_DEPTH)
        results.append(ok)
        print()

    print("HELD-OUT SUITE VERIFICATION: " + ("PASS -- H1-H3 sealed clean" if all(results) else "FAIL -- see above"))
