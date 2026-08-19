# C1 Search Contract

Sealed before any search algorithm is ported or run against C1. Mirrors
`phase2/CONTRACT.md`+`CALIBRATION.md`'s role, scaled to C1's actual size.

## Interpretation rule (the most important line in this document)

**C1's search results are architecture/integration evidence only, never
a performance verdict.** QA already proved: 9 reachable semantic states,
shortest exploit 5 actions, tiny branching factor. That's too small for
any algorithm comparison to mean anything -- a `beam_width` anywhere near
9 makes Beam functionally exhaustive, so "Beam beat Random" or "MCTS took
N transitions" would be noise dressed as a finding. What C1's search run
actually tests: does the `WorldState`/`MonitorState` split hold up
end-to-end -- no leakage into score/descriptor/policy, correct dedup,
correct reward -- across four real (not toy) algorithm implementations,
and can each one find AND replay a valid witness. RQ-B's real comparative
run happens on C2+, once the state space is large enough for the
comparison to carry information.

## Frozen parameters

| Parameter | Value | Why |
|---|---|---|
| `MAX_DEPTH` | 15 | 3x the proven-minimal 5-action witness, same convention as Phase 2 |
| `BUDGET` | 1,000 | C1's semantic space is tiny (9 states); this is generous headroom for a plumbing check, not a stress test |
| `BEAM_WIDTH` | 5 | Deliberately smaller than 9 (the full reachable-state count) so Beam is a genuine beam, not accidentally-exhaustive search -- irrelevant to the interpretation rule above either way |
| `NOVELTY_WEIGHT` | 1 | Phase 2's frozen value, reused as-is -- not re-calibrated, since C1 isn't a real RQ2-style comparison |
| `NOVELTY_K` | 4 | same |
| Random / MCTS seeds | `range(10)` | unchanged convention |
| MCTS `c` | `sqrt(2)` | Same proof as Phase 2 CALIBRATION.md: this MCTS stops at first discovery, so every candidate's reward is 0 at every point selection runs -- a positive constant multiplied uniformly across candidates can't change the argmax. Not swept for the same reason it wasn't swept in Phase 2. |
| Transition cost | 1 `apply()` call = 1 evaluation, tree-expansion and rollout counted identically | Same `Budget`-wrapper pattern as Phase 2, ported as-is |

Graph/Static-Conversion-Cycle baseline does not apply to C1 -- there is
no item-conversion economy for it to model. Not run, not reported as
`N/A` per case (there's no substrate for it to even attempt); simply out
of scope for this domain.

## `score()` -- unchanged, already sealed

`score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]`,
per `DESIGN_C1.md`. Not touched here.

## `behavior_descriptor()` -- sealed now, before any run

```python
def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(kind_counts.get(k, 0) / path_len for k in ("equip", "accept", "claim"))
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)
```

5 dimensions: equip/accept/claim action-kind ratios, quest progress
ordinal, path-length fraction -- the direct C1 analogue of Phase 2's
descriptor. Explicitly excluded: `MonitorState` (would be leakage, per
`DESIGN_C1.md`'s visibility rules), and any feature keyed to
`equipped == REQUIRED_EQUIPMENT` specifically -- that's the exploit's own
condition, and adding it would be tuning the descriptor to the answer
shape, exactly the mistake flagged for the score() bonus term earlier.

## What "pass" means for this integration test

- Every algorithm's found witness replays legally against `engine.apply`
  and is independently confirmed via `oracle.is_exploit`.
- No algorithm's `score()`/`behavior_descriptor()`/policy call ever
  touches `MonitorState` (checked by construction -- these functions
  don't take a `monitor` argument at all, not just "don't happen to use
  it").
- Dedup (Beam) and reward (MCTS) correctly use full `SearchState`.

No result table ranks the four algorithms against each other. A finding
like "Random needed more transitions than Beam here" is not reported as
a finding -- the state space is too small for that number to mean
anything, per the interpretation rule above.

## Non-goals

No calibration exercise for `NOVELTY_WEIGHT`/`NOVELTY_K`/`BEAM_WIDTH`
(reused/chosen by convention, not tuned against C1 results). No held-out
suite for C1 (that's a Phase 2-style pattern for when RQ-B comparison is
the point; C1's point is RQ-A). No negative-control regression test
added to the QA suite now -- valuable, deferred to C2 per the prior
review, not reopening C1 for it.
