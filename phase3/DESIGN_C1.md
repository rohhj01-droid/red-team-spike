# Phase 3 C1 Design Spec

Status: draft, sealed before any `phase3/` code exists. Mirrors
`phase2/CONTRACT.md`'s role -- reviewed and locked *before* implementation,
not written to match code that already exists.

## Phase 3 research questions (context)

- **RQ-A1 (representation)**: can Quest x Equipment history-sensitive
  state be represented correctly?
- **RQ-A2 (attribution)**: can an oracle correctly attribute a cross-
  system anomaly to the systems that caused it?
- **RQ-A3 (reproduction)**: can a validated anomaly be turned into an
  executable minimal witness?
- **RQ-B (secondary)**: given a larger state space, which search method
  finds things best? Subordinate to A -- not the point of C1.

## C1 definition (sealed)

> **Continuous Equipment Qualification.** A quest accepted while the
> required equipment is worn remains claim-eligible only if that
> equipment requirement is continuously satisfied until claim; once
> violated, eligibility is irreversibly lost, even if the required
> equipment is re-equipped later. The planted bug re-checks only the
> current equipment at claim time and forgets the historical violation.

Minimal witness (5 actions): `equip(Flame) -> accept -> equip(Wood) ->
equip(Flame) -> claim`. The buggy engine permits step 5; the stated rule
says it shouldn't.

Deliberately excluded from C1 (would be imagining ahead, not evidence-
forced): no gold/economy, no item-instance provenance (type-level
equipment only, e.g. `"FlameSword"` not `instance_id=3817`), no
unequipped/bare-hands state, no Buff system (that's C2), no kill-count
progress mechanic (dropped once the sealed rule turned out not to need
one).

## Architecture

```
Buggy World Engine                 Independent Property Monitor
  WorldState                         MonitorState
    equipped: str                      continuity_broken: bool
    quest_status: enum                 monitor_step(prev_world, action,
  Action                                            new_world, prev_monitor)
    equip(item)                                     -> new_monitor
    accept
    claim   <- reads WorldState only, never MonitorState (that's the bug)

Search
  carries SearchState = (world: WorldState, monitor: MonitorState)
  dedup identity = full SearchState
  heuristics/policies/reward can read monitor VALUES but must not be
  *tunable against* them the way FAMILY was in Phase 2 -- see visibility
  rules below for the precise line

Oracle (runtime, one-shot check per candidate)
  quest_status == CLAIMED and monitor.continuity_broken == True
    -> exploit

QA-only Independent Reference Specification
  derives the same violation from the FULL action history, computed a
  completely different way than monitor_step() -- never imported by
  search or by the runtime oracle
```

## WorldState / Action (the actual buggy engine)

```python
@dataclass(frozen=True)
class WorldState:
    equipped: str
    quest_status: Literal["NOT_ACCEPTED", "ACTIVE", "CLAIMED"]

# equip(item):
#   requires: item in EQUIPMENT_CATALOG (a small fixed set, e.g. 2-3 types)
#   effect:   equipped = item
#
# accept:
#   requires: quest_status == NOT_ACCEPTED and equipped == REQUIRED_EQUIPMENT
#   effect:   quest_status = ACTIVE
#
# claim (buggy, as actually shipped -- this is the only implementation
# that exists anywhere in the engine):
#   requires: quest_status == ACTIVE and equipped == REQUIRED_EQUIPMENT
#   effect:   quest_status = CLAIMED
```

There is no "correct claim" function anywhere in the engine. The correct
rule exists only as prose (above) justifying what the oracle checks --
exactly like Phase 0-2 never implemented a "correct dismantle."

## MonitorState / monitor_step (independent of the engine)

```python
@dataclass(frozen=True)
class MonitorState:
    continuity_broken: bool

def monitor_step(prev_world, action, new_world, prev_monitor) -> MonitorState:
    broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        broken = True
    return MonitorState(continuity_broken=broken)
```

Monotonic: once `True`, an accept resets it to `False` (fresh quest
attempt), nothing else ever clears it mid-quest.

## SearchState and visibility rules (sealed, applies to every algorithm)

```python
@dataclass(frozen=True)
class SearchState:
    world: WorldState
    monitor: MonitorState
```

| Component | Sees |
|---|---|
| `legal_actions` | `WorldState` only |
| `apply` (world transition) | `WorldState` only |
| `monitor_step` | `WorldState` (prev+new) + prior `MonitorState` -- never writes to WorldState |
| Beam `score()` | `WorldState` only |
| Beam-Diverse `behavior_descriptor()` | `WorldState` + generic path/action-kind features only |
| Random policy | `WorldState` only (uniform over legal actions, unchanged from Phase 2) |
| MCTS UCT selection | visit counts / accumulated reward only (never state fields directly, same as Phase 2) |
| **Dedup identity** (Beam's `candidates` dict key, MCTS node identity) | **full `SearchState`** -- required for correctness, not a hint |
| **Reward / online exploit check** (what MCTS backprops, what triggers early-exit) | **full `SearchState`** (`world.quest_status == CLAIMED and monitor.continuity_broken`) -- this is just the same oracle predicate computed incrementally, not new information |
| Oracle (final grading) | full `SearchState`, replayed independently start-to-finish |

The line: **ranking/guidance signals (score, descriptor, UCT) stay
WorldState-only; correctness-critical bookkeeping (dedup, reward) uses
the full SearchState because the oracle predicate IS part of what "found
it" means, not because it's being used to point search at the answer.**

Beam-Naive/Beam-Diverse's `candidates: Dict[GameState, ...]` becomes
`Dict[SearchState, ...]`; `score()` is called as `score(candidate.world)`.
MCTS's `_Node.state` becomes `SearchState`; no transposition table is
added (still a pure tree, per Phase 2's "don't build what isn't forced"
discipline) -- only the per-node state type changes.

## Beam scoring for a non-economic domain (new decision, needs confirmation)

Phase 2's `score() = gold + inventory_value` has no analogue here -- C1
has no economic quantity. Proposed default: **ordinal progress score**,
`score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]`,
i.e. reward reaching further along the quest state machine, the direct
analogue of "reward accumulating value" in Phase 2. No bonus term for
`equipped == REQUIRED_EQUIPMENT` -- adding one would be tuning the score
toward the specific exploit's shape (imagining ahead), and the ordinal
score alone still lets Beam distinguish "made progress" from "didn't."

## Oracle (runtime)

```python
def is_exploit(state: SearchState) -> bool:
    return state.world.quest_status == "CLAIMED" and state.monitor.continuity_broken
```

## QA: independent reference + exhaustive equivalence (this is the actual RQ-A1 test)

A second, completely separate function computes the same fact a
different way -- reading the full action history from scratch rather
than incrementally:

```python
def reference_continuity_broken(history: List[Action]) -> bool:
    """Replays `history` and independently determines whether the
    required-equipment condition was ever violated between accept and
    claim -- by scanning the whole trace, not by carrying a running bit.
    Never imported by search.py or by the runtime oracle above --
    QA-only, so a bug in monitor_step() can't confirm itself."""
```

Verification step (before C1 is sealed, mirrors `verify_cases.py`'s
role): exhaustively enumerate every reachable `SearchState` up to a
depth bound and confirm, for every one, `monitor.continuity_broken ==
reference_continuity_broken(path_to_it)`. Any mismatch fails C1's QA
outright -- it would mean the incremental summary and the full-history
definition disagree, exactly the kind of self-confirming bug Phase 0
already taught us to distrust.

This run is also Phase 3's first real measurement of the open risk
flagged earlier ("does exhaustive QA scale past Phase 0-2's small state
spaces") -- record reachable-state count, wall-clock, and peak depth
here as a reference point for C2 (which adds Buff and will grow the
state space further).

## RQ-A2, precisely (not "solved for free")

Not: *cross-system attribution is solved.* The precise claim C1 tests:
**can an explicit, domain-specific property monitor provide direct
attribution without Phase 0's family-isolation-replay technique, for
this one planted cross-system mechanism?** A pass here is evidence for
that narrow claim, to be re-tested (not assumed) on C2 and later cases
with different attribution shapes.

## Non-goals for C1

No Buff system, no item-instance provenance, no gold/economy, no
transposition tables, no new MCTS rollout policy, no kill-count
mechanic, no generalized cross-system oracle framework. C1 is one
mechanism, sized to force exactly the state/architecture questions above
and nothing more.
