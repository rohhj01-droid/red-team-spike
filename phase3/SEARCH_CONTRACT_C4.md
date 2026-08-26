# C4 Search Contract

Sealed before any search algorithm is ported or run against C4. Mirrors
`SEARCH_CONTRACT_C2.md`/`SEARCH_CONTRACT_C3.md`'s role. C4's `_step()`
is structurally more involved than C2's/C3's -- two oracle checks and a
third state bucket to thread -- so this contract does more real work
than C3's (which was mostly "reuse C2's rules unchanged").

## Interpretation rule (unchanged framing, restated for C4)

**C4's search results are architecture/integration evidence only, never
a performance verdict.** `verify_c4.py`'s Step 1 found 31 reachable
semantic states from 69 transitions across 9 layers -- smaller than
C3's (62, 174, 11), since C4 reuses C2's base engine rather than C3's
Enchantment-extended one; still far too small for a cost or
success-rate difference between algorithms to carry information. What
this run actually tests: does the two-oracle, three-bucket transition
pipeline integrate correctly into four real search loops -- discovery
keyed to `classify_consume` only, `classify_claim`'s verdict threaded
through as provenance without ever triggering termination itself; no
leakage into score/descriptor/policy; correct dedup; correct reward.

## The `_step()` pipeline -- exact order, sealed

```text
prev_world, prev_monitor, prev_provenance
        |
Budget.step(prev_world, action) -> new_world
        |
monitor_step(prev_world, action, new_world, prev_monitor) -> new_monitor
        |
classify_claim(action, prev_monitor) -> claim_verdict
        |
classify_consume(action, prev_provenance) -> consume_verdict
        |
event_provenance_step(action, claim_verdict, prev_provenance) -> new_provenance
```

This order is a semantic contract, not an implementation convenience --
`monitor_step -> classify_claim -> event_provenance_step` may not be
reordered. `EventProvenanceState` freezes an *already-computed* claim
verdict; it is not itself a property fold, so it must run last, after
the verdict it depends on exists. `classify_consume` reads
`prev_provenance` -- the *frozen* value from before this transition --
never `new_provenance`; reading the post-transition value would ask "is
the reward *currently* tainted" instead of "was *this* consumption of a
tainted reward," collapsing exactly the distinction Witnesses P/Q in
`DESIGN_C4.md` were built to prove matters.

**`_step()`'s signature deliberately does not expose `claim_verdict` to
its caller:**

```python
def _step(budget, world, monitor, provenance, action):
    new_world = budget.step(world, action)
    new_monitor = monitor_step(world, action, new_world, monitor)
    claim_verdict = classify_claim(action, monitor)
    consume_verdict = classify_consume(action, provenance)
    new_provenance = event_provenance_step(action, claim_verdict, provenance)
    return new_world, new_monitor, new_provenance, consume_verdict
```

Not an oversight -- the same "make the correct order the only order
that compiles into a call" reasoning `SEARCH_CONTRACT_C3.md` used for
`prev_monitor` vs. `new_monitor`. A caller literally cannot write

```python
if claim_verdict is not None or consume_verdict is not None:  # WRONG, and not just style
```

because `claim_verdict` was never returned. There is exactly one
verdict a caller can check, and it is the right one.

## Discovery is `consume_verdict`-only -- restated as a first-class rule

**A `claim` verdict is an intermediate judged event and provenance
source; only a tainted `consume` verdict is a C4 discovery.** Every
search loop's check is exactly:

```python
world, monitor, provenance, consume_verdict = _step(budget, world, monitor, provenance, action)
path.append(action)
if consume_verdict is not None:
    return Discovery(budget.used, path, consume_verdict)
```

`DESIGN_C4.md`'s "Search target discovery is consume-only" section
already sealed this at the mechanism level; this restates it at the
search-integration level because it is the single easiest thing to get
wrong when porting four algorithms that all independently call `_step`.

## No `CLAIMED`-terminal pruning

**C3's post-hoc diagnostic (`e3bdfeb`) -- excluding legitimately-reached
`CLAIMED` states from further expansion -- must not be carried into
C4's search, in any algorithm, under any framing ("optimization",
"matches C3's finding", or otherwise.** C4's actual target,
`TAINTED_REWARD_CONSUMPTION`, is only reachable by continuing past
`CLAIMED` (`reward_owned` is set by `claim`; `consume` is the only
action that ever reads it). Pruning `CLAIMED` states would make the
target as unreachable as an any-oracle-terminates rule would (Section
"Discovery is consume_verdict-only" above) -- a different mechanism,
same failure shape. **C4 target requires post-`CLAIMED` expansion by
construction; this is not a performance claim.**

This is the concrete case `RESULTS_C3.md`'s Section 5 flagged as a
caveat rather than a settled policy: *"a future case with
downstream/interacting events... could make post-claim states matter
again."* C4 is that case. C3's diagnostic finding was correct **for
C3**; applying it here would be exactly the kind of imagined
generalization this project has avoided at every prior step. When
porting C3's `phase3/c3/search.py` (the *official* file, `ecbd536` --
not `phase3/c3/diagnostic_claimed_terminal.py`, which must not be used
as a source for this port at all), verify by inspection that no
`quest_status == "CLAIMED"` skip-expansion logic exists anywhere in the
result.

## `SearchState` and visibility

```python
SearchState = Tuple[WorldState, MonitorState, EventProvenanceState]
```

Full 3-tuple used for Beam's dedup and MCTS's node identity/reward,
same as C4's own `verify_c4.py` closure. **New principle, stated as a
documentation rule, not built into an abstraction yet:** all
specification-derived persistent state is part of semantic identity,
but unavailable to search guidance. Concretely: `score()` and
`behavior_descriptor()` take `WorldState` only -- no `MonitorState`, no
`EventProvenanceState` parameter, checked by `inspect.signature` the
same way as C1-C3.

## Frozen parameters -- reused from C1-C3, not re-tuned

| Parameter | Value | Why |
|---|---|---|
| `MAX_DEPTH` | 15 | Reused unchanged again. C4's longest witness (`TAINTED_REWARD_CONSUMPTION`) is 7 actions -- same as C3's longest, still ample headroom. |
| `BUDGET` | 1,000 | C4's semantic space (31 states, 69 transitions) is the smallest since C1; still the same generous-headroom reasoning. |
| `BEAM_WIDTH` | 5 | Same "genuine beam" reasoning; now an even wider margin (5 of 31) than C3's (5 of 62). |
| `NOVELTY_WEIGHT` | 1 | Reused as-is. |
| `NOVELTY_K` | 4 | Reused as-is. |
| Random / MCTS seeds | `range(10)` | Unchanged convention. |
| MCTS `c` | `sqrt(2)` | Same first-hit-reward inertness proof as C1-C3. Not swept. |
| Transition cost | 1 `apply()` call = 1 evaluation | Same `Budget`-wrapper pattern. |

Graph/Static-Conversion-Cycle baseline does not apply to C4, same as
C1-C3 -- no item-conversion economy.

## `score()` -- unchanged, already sealed

`score(world) = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[quest_status]`,
identical to C1-C3. `reward_owned` is not scored -- it is `consume`'s
own precondition and `channel`-analogue leakage risk, same reasoning as
excluding `has_flame_buff`/`enchanted` before it.

## `behavior_descriptor()` -- sealed now, before any run

```python
def behavior_descriptor(world: WorldState, path: List[Action], max_depth: int) -> Tuple[float, ...]:
    path_len = len(path) or 1
    kind_counts = Counter(a.kind for a in path)
    action_ratio = tuple(
        kind_counts.get(k, 0) / path_len
        for k in ("equip", "accept", "channel", "claim", "consume")
    )
    quest_ordinal = {"NOT_ACCEPTED": 0, "ACTIVE": 1, "CLAIMED": 2}[world.quest_status] / 2.0
    return action_ratio + (quest_ordinal, len(path) / max_depth)
```

7 dimensions: C2's 4 action-kind ratios plus `consume`, appended at the
end (unlike C3's mid-insertion of `enchant`/`unenchant` -- `consume` is
the terminal action in C4's causal chain, same position as `claim` was
before it existed, so it belongs after `claim` in the ratio tuple, not
before it). `MonitorState`, `EventProvenanceState`, and `reward_owned`
are all excluded, same reasoning as every prior descriptor.

## What "pass" means for this integration test

- Every algorithm's found witness replays legally against `engine.apply`.
- The `Discovery.classification` each algorithm recorded
  (`"TAINTED_REWARD_CONSUMPTION"`, the only value `consume_verdict` can
  be non-`None` as) matches an independently-computed
  `classify_consume(action, prev_provenance)` at the witness's actual
  `consume` transition during replay.
- The witness must contain exactly one `claim` action, and it must
  precede the discovering `consume` action -- a structural sanity check
  that the found witness is a genuine claim-then-consume chain, not an
  artifact of a search or replay bug.
- No algorithm's `score()`/`behavior_descriptor()`/policy call ever
  touches `MonitorState` or `EventProvenanceState` (checked by
  construction).
- Dedup (Beam) and reward (MCTS) correctly use the full `SearchState`
  3-tuple.
- No `CLAIMED`-terminal pruning anywhere in the ported code (Section
  above) -- checked by inspection, not just by outcome (an algorithm
  finding nothing for an unrelated reason wouldn't be caught by an
  outcome-only check).

No result table ranks the four algorithms against each other.

## Non-goals

No calibration exercise for `NOVELTY_WEIGHT`/`NOVELTY_K`/`BEAM_WIDTH`/
`MAX_DEPTH` against C4's space -- reused by convention. No held-out
suite for C4. No propagation of `claim`'s three-way category into
`Discovery` -- it stays `(cost, path, classification)`, unextended,
per `DESIGN_C4.md`. No generalization of the `CLAIMED`-terminal
prohibition into a permanent rule about all future cases -- it is
specific to C4 having a real target past `CLAIMED`, stated here because
this is the case where it would otherwise be tempting to reuse C3's
diagnostic finding verbatim.
