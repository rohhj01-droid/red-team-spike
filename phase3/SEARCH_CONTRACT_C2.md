# C2 Search Contract

Sealed before any search algorithm is ported or run against C2. Mirrors
`SEARCH_CONTRACT_C1.md`'s role, but C2's transition-based oracle (C2c,
`DESIGN_C2.md`) makes this contract's first and most important job
different from C1's: pin down exactly *when* and *on what* a discovery
is judged, not just reuse C1's parameters with a bigger action set.

## Interpretation rule (unchanged framing, restated for C2)

**C2's search results are architecture/integration evidence only, never
a performance verdict.** `verify_c2.py`'s Step 1 found 19 reachable
semantic states from 40 transitions across 8 layers -- bigger than C1's
(9, 13, 7), but still far too small for a cost or success-rate
difference between algorithms to carry information. What this run
actually tests: does the transition-based oracle integrate correctly
into four real search loops -- discovery keyed to the `claim` event
itself, not a re-derived state predicate; no leakage into
score/descriptor/policy; correct dedup; correct reward -- and can each
algorithm find AND correctly replay/attribute a valid witness. A real
comparative run is still deferred, per C1's contract, to whenever a case
is large enough for the comparison to mean something.

## Oracle invocation semantics (new for C2 -- the core of this contract)

C1's oracle was a state predicate: askable of any `(world, monitor)`
pair, any time. C2c changed that -- `classify_claim(action, prev_monitor)`
only answers a question about the specific instant a `claim` action
fires, using the monitor value from *immediately before* that action.
Every algorithm's per-step transition must follow this exact order:

```text
prev_world, prev_monitor
        |
legal_actions(prev_world)  -- choose action
        |
Budget.step(prev_world, action)              -- consumes budget
        |
new_world
        |
monitor_step(prev_world, action, new_world, prev_monitor)
        |
new_monitor
        |
if action.kind == "claim":
    classify_claim(action, prev_monitor)      -- judged on PRE-transition monitor
```

**A discovery occurs on a successfully executed legal `claim` transition;
its cost includes that claim transition, while its classification is
computed from the immediately pre-transition `MonitorState`.** This
ordering matters concretely: checking `classify_claim` *before* calling
`Budget.step` would report a discovery whose cost excludes the very
transition that caused it. The check must happen after the world/monitor
update, but must use the `prev_monitor` value captured before that
update -- both C1's existing `_step()`-then-check shape and the
transition-based oracle are satisfied by threading `prev_monitor`
alongside the call, not by reading it back off `new_monitor`.

**Event check before dedup, ranking, or pruning.** Beam's per-layer loop
must classify each freshly-fired `claim` transition and return a
`Discovery` immediately, before that candidate is inserted into the
dedup dictionary or scored/ranked. Random and MCTS already have no
separate dedup step to jump ahead of, but the same principle applies at
expansion and at every rollout step: check the transition that just
executed, don't defer judgment to a later look at accumulated state.

**MCTS specifically:** both the expansion step and every rollout step
must check `classify_claim` against the `prev_monitor` in effect
immediately before that step's action, not `is_exploit` of the resulting
state. The binary reward (1.0/0.0) backpropagated is the direct result
of that one check at the step where it fired -- never recomputed later
from a node's stored final state, since (per C2c) a later state can look
different (e.g. a post-claim `channel()`) without changing what actually
happened at the claim transition.

## `Discovery` gains a field

```python
@dataclass
class Discovery:
    cost: int
    path: List[Action]
    classification: str  # "EQUIPMENT_CONTINUITY_VIOLATION" | "BUFF_SOURCE_LIFECYCLE_VIOLATION" | "BOTH"
```

Unlike C1 (binary found/not-found), C2's RQ-A2 extends to three-way
attribution -- a `Discovery` is meaningless without recording *which*
violation it is, since that's now the thing worth checking search
actually got right, not just "found something."

## Frozen parameters -- reused from C1, not re-tuned

| Parameter | Value | Why |
|---|---|---|
| `MAX_DEPTH` | 15 | Reused unchanged from C1, not recalculated against C2's longer minimal witnesses (6 actions vs. C1's 5) -- still ample headroom (15 >> 6), and keeping the same number is itself evidence C2 wasn't retuned to fit. |
| `BUDGET` | 1,000 | C2's semantic space (19 states, 40 transitions) is still tiny; same generous-headroom reasoning as C1. |
| `BEAM_WIDTH` | 5 | Deliberately smaller than the 19 reachable states, same "genuine beam, not accidentally exhaustive" reasoning as C1 -- an even wider margin here than C1's 5-of-9. |
| `NOVELTY_WEIGHT` | 1 | Reused as-is from Phase 2 / C1. |
| `NOVELTY_K` | 4 | Reused as-is. |
| Random / MCTS seeds | `range(10)` | Unchanged convention. |
| MCTS `c` | `sqrt(2)` | Same proof as Phase 2/C1: first-hit binary reward makes every candidate's reward 0 at every point selection actually runs, so a uniform positive multiplier can't change the argmax. Not swept, same reason it wasn't swept before. |
| Transition cost | 1 `apply()` call = 1 evaluation | Same `Budget`-wrapper pattern, ported as-is. |

Graph/Static-Conversion-Cycle baseline does not apply to C2, same as C1
-- no item-conversion economy for it to model. Not run, not reported.

## `score()` -- unchanged, already sealed

`score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]`,
same as C1. `has_flame_buff` is deliberately excluded from score, same
reasoning as excluding equipment-match from C1's score: it's the
planted mechanism's own condition, and rewarding progress toward it
would be tuning guidance to the answer shape.

## `behavior_descriptor()` -- sealed now, before any run

```python
def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(kind_counts.get(k, 0) / path_len for k in ("equip", "accept", "channel", "claim"))
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)
```

6 dimensions: the direct C2 extension of C1's descriptor, adding a
`channel` ratio alongside `equip`/`accept`/`claim`. Explicitly excluded:
`MonitorState` (leakage, per `DESIGN_C2.md`'s visibility rules, unchanged
from C1), and `has_flame_buff` specifically -- it's `WorldState`-visible
so including it would not be leakage, but it sits too close to C2's
planted mechanism itself; adding it isn't needed and would blur what a
future descriptor-ablation result could mean.

## What "pass" means for this integration test

- Every algorithm's found witness replays legally against `engine.apply`.
- The `Discovery.classification` each algorithm recorded matches an
  independently-computed `classify_claim(action, prev_monitor)` at the
  actual `claim` transition during replay -- not just "is this path an
  exploit," but "did search correctly attribute which one."
- No algorithm's `score()`/`behavior_descriptor()`/policy call ever
  touches `MonitorState` (checked by construction -- no `monitor`
  parameter at all). The oracle *is* allowed to read `MonitorState` --
  that is not leakage; a ground-truth judge reading ground truth is a
  different role from search guidance reading it.
- Dedup (Beam) and reward (MCTS) correctly use full `SearchState`.
- Discovery cost includes the triggering `claim` transition (per the
  invocation-order rule above).

No result table ranks the four algorithms against each other, same rule
as C1.

## Non-goals

No calibration exercise for `NOVELTY_WEIGHT`/`NOVELTY_K`/`BEAM_WIDTH`/
`MAX_DEPTH` against C2's larger space -- reused by convention, not
tuned. No held-out suite for C2 (RQ-B's comparison substrate, not this
case's point). No further negative-control work here -- the permanent
regression (Step 1b) and the post-claim mutation regression (Step 3)
already live in `verify_c2.py`'s core QA, not the search layer.
