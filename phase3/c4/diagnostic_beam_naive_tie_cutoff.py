"""POST-HOC DIAGNOSTIC -- NOT part of the sealed C4 search contract.
Never used to retroactively change the official result in `2a10826`
(C4 SEARCH INTEGRATION: FAIL). Its own result is reported as a
diagnostic finding, not a re-run of the official test.

Part 1: a passive trace -- no behavior change; ranking, candidate
generation, and tie-breaking are exactly search.py's own official
score() and stable-sort logic, only observed and printed. Pins down
the exact moment beam_naive's official run (BEAM_WIDTH=5) drops the
sealed 6-action tainted-claim witness: it survives every layer while
still ACTIVE, and at layer 6 -- the instant it reaches CLAIMED -- it
ties in score (both = 2, official score(), unmodified) with five
independently-arrived clean-claim candidates also reaching CLAIMED
that same layer. Under deterministic stable-sort tie-breaking it is
exactly the sixth candidate in that tied group; BEAM_WIDTH=5 excludes
it precisely at the cutoff, before its own downstream consume can ever
be expanded.

Part 2 (primary causal test): the single, most surgical intervention
the trace predicts. Calls the OFFICIAL, already-committed
beam_naive_search() completely unmodified, with BEAM_WIDTH=6 instead
of 5 -- one more slot than the cutoff that excluded the sixth-ranked
candidate. score(), candidate generation, dedup, and stable
tie-ordering are all untouched; only the width argument differs from
the frozen contract value. No width sweep -- this tests the one value
the trace specifically predicts, not a search for a value that happens
to work.

Part 3 (auxiliary, demoted): an earlier diagnostic attempt (CLAIMED
scored 1 instead of 2, tied with ACTIVE) also restored discovery, but
is not the primary causal test -- it merges the ACTIVE and CLAIMED tie
groups, which reorders the combined tied set under stable-sort in a
way not cleanly attributable to "CLAIMED's advantage over ACTIVE." Kept
for the record as a secondary sensitivity observation, not evidence
for the tie-cutoff mechanism specifically.

Run:
    python diagnostic_beam_naive_tie_cutoff.py
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from budget import Budget, BudgetExhausted
from engine import Action, WorldState, initial_world, legal_actions
from event_provenance import initial_event_provenance, event_provenance_step
from monitor import initial_monitor, monitor_step
from oracle import classify_claim, classify_consume
from search import Discovery, SearchState, beam_naive_search, score

MAX_DEPTH = 15
BUDGET = 1_000
OFFICIAL_BEAM_WIDTH = 5
DIAGNOSTIC_BEAM_WIDTH = 6


# ---------------------------------------------------------------------------
# Part 1: passive trace (observation only -- uses the official score())
# ---------------------------------------------------------------------------

def passive_trace(beam_width: int, max_depth: int, budget_limit: int) -> None:
    print(f"--- passive trace, beam_width={beam_width} (official score(), observation only) ---")
    budget = Budget(budget_limit)
    start: SearchState = (initial_world(), initial_monitor(), initial_event_provenance())
    beam: List[Tuple[SearchState, List[Action]]] = [(start, [])]

    for layer in range(1, max_depth + 1):
        if not beam or not budget.remaining():
            break
        candidates: Dict[SearchState, Tuple[float, List[Action]]] = {}
        for (world, monitor, provenance), path in beam:
            if not budget.remaining():
                break
            for action in legal_actions(world):
                if not budget.remaining():
                    break
                new_world = budget.step(world, action)
                new_monitor = monitor_step(world, action, new_world, monitor)
                claim_verdict = classify_claim(action, monitor)
                new_provenance = event_provenance_step(action, claim_verdict, provenance)
                new_state = (new_world, new_monitor, new_provenance)
                new_path = path + [action]
                existing = candidates.get(new_state)
                if existing is None or len(new_path) < len(existing[1]):
                    candidates[new_state] = (score(new_world), new_path)

        ranked = sorted(candidates.items(), key=lambda kv: kv[1][0], reverse=True)
        selected_keys = {s for s, _ in ranked[:beam_width]}
        tainted_entries = [(s, sc, p) for s, (sc, p) in candidates.items() if s[2].reward_provenance_tainted]

        print(f"layer {layer}: total={len(candidates)} tainted={len(tainted_entries)} budget_used={budget.used}")
        for s, sc, p in tainted_entries:
            rank = next(i for i, (rs, _) in enumerate(ranked) if rs == s)
            print(f"  TAINTED score={sc} rank={rank} (0-indexed) selected={s in selected_keys} path={[str(a) for a in p]}")

        beam = [(s, p) for s, (_, p) in ranked[:beam_width]]
    print(f"  final budget_used={budget.used}")


# ---------------------------------------------------------------------------
# Part 3: auxiliary, demoted -- CLAIMED scored 1 (tied with ACTIVE), kept
# only as a secondary sensitivity observation, not the primary test.
# ---------------------------------------------------------------------------

def _score_no_claimed_advantage(world: WorldState) -> float:
    return {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 1}[world.quest_status]


def beam_naive_score_gap_neutralized(budget_limit: int, max_depth: int, beam_width: int) -> Optional[Discovery]:
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
                    new_world = budget.step(world, action)
                    new_monitor = monitor_step(world, action, new_world, monitor)
                    claim_verdict = classify_claim(action, monitor)
                    consume_verdict = classify_consume(action, provenance)
                    new_provenance = event_provenance_step(action, claim_verdict, provenance)
                    new_state = (new_world, new_monitor, new_provenance)
                    new_path = path + [action]
                    if consume_verdict is not None:
                        return Discovery(budget.used, new_path, consume_verdict)
                    existing = candidates.get(new_state)
                    if existing is None or len(new_path) < len(existing[1]):
                        candidates[new_state] = (_score_no_claimed_advantage(new_world), new_path)
            ranked = sorted(candidates.items(), key=lambda kv: kv[1][0], reverse=True)
            beam = [(s, p) for s, (_, p) in ranked[:beam_width]]
    except BudgetExhausted:
        pass
    return None


if __name__ == "__main__":
    print("=== DIAGNOSTIC ONLY -- not the official C4 search contract result ===")
    print("Official result stays sealed as FAIL (2a10826).")
    print()

    passive_trace(OFFICIAL_BEAM_WIDTH, MAX_DEPTH, BUDGET)

    print()
    print(f"--- Part 2 (primary causal test): official beam_naive_search(), BEAM_WIDTH={DIAGNOSTIC_BEAM_WIDTH} ---")
    d_width6 = beam_naive_search(BUDGET, MAX_DEPTH, DIAGNOSTIC_BEAM_WIDTH)
    print(f"beam_naive (BEAM_WIDTH={DIAGNOSTIC_BEAM_WIDTH}): {d_width6}")
    print()
    if d_width6 is not None:
        print("PART 2 RESULT: tie-cutoff hypothesis SUPPORTED -- increasing only the")
        print("beam capacity from 5 to 6, exactly as predicted by the passive trace,")
        print("preserved the sixth score-tied tainted CLAIMED candidate and restored")
        print("downstream discovery.")
    else:
        print("PART 2 RESULT: tie-cutoff hypothesis NOT SUPPORTED -- BEAM_WIDTH=6 was")
        print("not sufficient. The single-cutoff explanation is incomplete.")

    print()
    print("--- Part 3 (auxiliary, demoted): CLAIMED scored 1 instead of 2 ---")
    d_scoregap = beam_naive_score_gap_neutralized(BUDGET, MAX_DEPTH, OFFICIAL_BEAM_WIDTH)
    print(f"beam_naive (CLAIMED score-gap neutralized): {d_scoregap}")
    print("  Secondary sensitivity observation only -- merges the ACTIVE and")
    print("  CLAIMED tie groups, reordering the combined tied set under stable")
    print("  sort in a way not cleanly attributable to the tie-cutoff mechanism")
    print("  Part 2 isolates. Not used as evidence for that mechanism specifically.")
