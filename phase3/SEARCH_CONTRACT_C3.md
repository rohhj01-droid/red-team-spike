# C3 Search Contract

Sealed before any search algorithm is ported or run against C3. Mirrors
`SEARCH_CONTRACT_C2.md`'s role. Unlike the C1 -> C2 transition, C3's
oracle and monitor-invocation shape did not change from C2c -- this
contract's job is mostly *reuse*, with one explicit scope decision to
seal: search does not track `classify_pathway`.

## Interpretation rule (unchanged framing, restated for C3)

**C3's search results are architecture/integration evidence only, never
a performance verdict.** `verify_c3.py`'s Step 1 found 62 reachable
semantic states from 174 transitions across 11 layers -- larger again
than C2's (19, 40, 8) and C1's (9, 13, 7), but still small enough that a
cost or success-rate difference between algorithms carries no
information. What this run actually tests: does the transition-based
oracle -- unchanged from C2c -- keep integrating correctly into four real
search loops once the action set and `MonitorState` grow by one
dependent lifecycle; no leakage into score/descriptor/policy; correct
dedup; correct reward. A real comparative run stays deferred, per C1's
and C2's contracts, to whenever a case is large enough for the
comparison to mean something.

## Oracle invocation semantics (unchanged from C2)

C3's `classify_claim(action, prev_monitor)` is byte-for-byte the same
function as C2c's -- still a judgment about one `claim` transition, using
the monitor value from immediately before it fires. The invocation order
every algorithm must follow is identical to `SEARCH_CONTRACT_C2.md`'s:

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

Same requirements as C2, restated because they still govern every
transition here too: a discovery's cost includes the triggering `claim`
transition; the check happens after `Budget.step` but uses the
`prev_monitor` value captured before it; the check happens before any
dedup/ranking/pruning (Beam) and at both expansion and every rollout
step (MCTS). `enchant`/`unenchant` are ordinary actions like `equip` --
they only ever affect `MonitorState` through the same `monitor_step`
call every other action already goes through; they introduce no new
oracle-check site.

## `Discovery` -- unchanged shape, deliberately not extended

```python
@dataclass
class Discovery:
    cost: int
    path: List[Action]
    classification: str  # "EQUIPMENT_CONTINUITY_VIOLATION" | "BUFF_SOURCE_LIFECYCLE_VIOLATION" | "BOTH"
```

**Explicit scope decision:** search does not compute or record
`classify_pathway` (`NEW_CHAIN_PATHWAY` / `OLD_EQUIPMENT_SOURCE_PATHWAY`).
That predicate exists in `verify_c3.py` to prove, during QA, that both
causally distinct routes to `BUFF_SOURCE_LIFECYCLE_VIOLATION` are
reachable -- a design-verification question. What a search algorithm
needs to report is the oracle's own three-way attribution, unchanged
from C2; asking search to *also* attribute pathway would extend the
production surface for a distinction the oracle itself was deliberately
built to not need (`DESIGN_C3.md`'s "Oracle -- unchanged from C2c"
section is explicit that `enchant_broken` only ever reaches `claim()`'s
judgment by way of `buff_source_broken`). If a future case needs
pathway-level attribution as a first-class search output, that's a
decision for that case, not one to retrofit here from unused capability.

## Frozen parameters -- reused from C1/C2, not re-tuned

| Parameter | Value | Why |
|---|---|---|
| `MAX_DEPTH` | 15 | Reused unchanged again. C3's longest minimal witness is 7 actions (up from C2's 6) -- still ample headroom (15 >> 7), and the number not moving is itself the evidence nothing was retuned. |
| `BUDGET` | 1,000 | C3's semantic space (62 states, 174 transitions) is bigger than C2's but still tiny; same generous-headroom reasoning. |
| `BEAM_WIDTH` | 5 | Deliberately smaller than the 62 reachable states -- an even wider margin than C2's 5-of-19, same "genuine beam" reasoning. |
| `NOVELTY_WEIGHT` | 1 | Reused as-is from Phase 2 / C1 / C2. |
| `NOVELTY_K` | 4 | Reused as-is. |
| Random / MCTS seeds | `range(10)` | Unchanged convention. |
| MCTS `c` | `sqrt(2)` | Same proof as before: first-hit binary reward makes every candidate's reward 0 at every point selection actually runs, so a uniform positive multiplier can't change the argmax. Not swept. |
| Transition cost | 1 `apply()` call = 1 evaluation | Same `Budget`-wrapper pattern, ported as-is. |

Graph/Static-Conversion-Cycle baseline does not apply to C3, same as
C1/C2 -- no item-conversion economy for it to model.

## `score()` -- unchanged, already sealed

`score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]`,
identical to C1/C2. Neither `has_flame_buff` nor `enchanted` is scored --
both are conditions the planted mechanism itself references, and
rewarding progress toward them would tune guidance to the answer shape,
same reasoning as excluding equipment-match (C1) and buff presence (C2).

## `behavior_descriptor()` -- sealed now, before any run

```python
def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(
        kind_counts.get(k, 0) / path_len
        for k in ("equip", "accept", "enchant", "unenchant", "channel", "claim")
    )
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)
```

8 dimensions: C2's 4 action-kind ratios plus `enchant`/`unenchant`,
inserted between `accept` and `channel` to match their causal position
(prerequisite for `channel`, same as `accept` is a prerequisite for
`claim`) -- not appended at the end, so the ordering still reads as
"setup actions, then the provenance layer, then grant, then the fault
action" rather than "old dims, then new dims tacked on." Explicitly
excluded: `MonitorState` (leakage, unchanged rule) and `enchanted`
specifically -- `WorldState`-visible so not leakage, but it's `channel`'s
own precondition, the same reasoning that excluded `has_flame_buff` from
C2's descriptor.

## What "pass" means for this integration test

- Every algorithm's found witness replays legally against `engine.apply`.
- The `Discovery.classification` each algorithm recorded matches an
  independently-computed `classify_claim(action, prev_monitor)` at the
  actual `claim` transition during replay -- unchanged check from C2,
  now exercised against a larger action set.
- No algorithm's `score()`/`behavior_descriptor()`/policy call ever
  touches `MonitorState` (checked by construction -- no `monitor`
  parameter at all).
- Dedup (Beam) and reward (MCTS) correctly use full `SearchState`
  (`Tuple[WorldState, MonitorState]`).
- Discovery cost includes the triggering `claim` transition.

No result table ranks the four algorithms against each other, and no
witness is expected or required to reach `BUFF_SOURCE_LIFECYCLE_VIOLATION`
via any particular pathway -- whichever an algorithm happens to find
first is a legitimate discovery.

## Non-goals

No calibration exercise for `NOVELTY_WEIGHT`/`NOVELTY_K`/`BEAM_WIDTH`/
`MAX_DEPTH` against C3's larger space -- reused by convention. No held-out
suite for C3. No pathway-attribution in `Discovery` (Section "`Discovery`
-- unchanged shape" above). No further negative-control or reference work
here -- `verify_c3.py`'s Step 1b and the `Hclean`/`Htainted` check already
cover this case's QA sensitivity requirements.
