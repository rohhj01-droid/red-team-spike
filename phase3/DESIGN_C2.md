# Phase 3 C2 Design Spec

Status: draft, sealed before any C2 code exists. Same role as
`DESIGN_C1.md`. Per `RESULTS_C1.md`'s closing question, C2's actual
research content is: **does the WorldState/MonitorState boundary that
worked for C1's one lifecycle (equipment continuity) survive a second,
causally-linked one (a Buff whose validity depends on its granting
Equipment)?** Not "add a Buff system."

## C2 mechanism (sealed)

**Single architectural fault**: `claim()` treats *presence* as a proxy
for *validity*, for both conditions it checks. It requires
`equipped == REQUIRED_EQUIPMENT` (current snapshot, ignoring whether
equipment continuity held) **and** `has_flame_buff == True` (current
presence, ignoring whether the buff's source has stayed qualified since
it was last validated). One wrong abstraction -- "if I can observe it
right now, it's valid" -- misapplied to both fields claim's precondition
happens to reference, not two independent missing checks.

Two independent spec facts, tracked in `MonitorState`, characterize how
that one fault can be violated:

- `continuity_broken` -- unchanged from C1: has `equipped` ever left
  `REQUIRED_EQUIPMENT` while `quest_status == ACTIVE`. Monotonic, no
  reset within one quest attempt (same reasoning as `DESIGN_C1.md`:
  nothing in C2's action set returns quest_status to `NOT_ACCEPTED`
  either).
- `buff_source_broken` -- new: has `equipped` left `REQUIRED_EQUIPMENT`
  at any point since the buff was last (re-)validated by `channel()`.
  Reset to `False` by `channel()`; set `True` the moment `equipped !=
  REQUIRED_EQUIPMENT`, tracked unconditionally (independent of
  `quest_status` -- buff validity has nothing to do with whether a quest
  is active).

Different reset rules (permanent-per-attempt vs. resettable-by-channel)
are what makes the two facts genuinely non-redundant -- see the
reachability table below.

## Sealed catalog and initial conditions

Reuses C1's equipment catalog and initial world unchanged, extended with
the buff field:

```python
EQUIPMENT_CATALOG = {"FlameSword", "WoodenSword"}   # unchanged from C1
REQUIRED_EQUIPMENT = "FlameSword"                     # unchanged from C1

initial WorldState:   equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False
initial MonitorState: continuity_broken=False, buff_source_broken=False
```

`equip(item)` keeps C1's no-op ban (`item != currently_equipped`) --
that check only ever needed `WorldState`, so it's untouched.

## Actions (sealed)

```
equip(item):
  requires: item in EQUIPMENT_CATALOG and item != currently_equipped
  effect:   equipped = item

accept:
  requires: quest_status == NOT_ACCEPTED and equipped == REQUIRED_EQUIPMENT
  effect:   quest_status = ACTIVE
  # unchanged from C1 -- accept does not reference buff at all

channel:
  requires: equipped == REQUIRED_EQUIPMENT
  # NO no-op ban -- see "WorldState no-op, Monitor non-no-op" below.
  # legal_actions() stays WorldState-only; this is the price of that.
  world effect:   has_flame_buff = True
  monitor effect: buff_source_broken = False   # the only action that resets it

claim (buggy, as actually shipped):
  requires: quest_status == ACTIVE and equipped == REQUIRED_EQUIPMENT
            and has_flame_buff == True
  effect:   quest_status = CLAIMED
  # presence-only on both conditions -- the single fault, manifesting twice
```

No "correct claim" implementation exists anywhere, same as C1 -- the
correct rule is prose above, checked only by the oracle.

## `WorldState` no-op can be a `MonitorState` non-no-op (new in C2)

A review catch during design, kept deliberately rather than engineered
away: calling `channel()` while `has_flame_buff` is already `True`
produces **no change to `WorldState`** (the field is already `True`) but
can still produce a **real change to `MonitorState`**
(`buff_source_broken: True -> False`, if the buff had gone stale). The
first-instinct fix -- ban `channel()` when it would be a WorldState
no-op, mirroring C1's `equip` rule -- was rejected: that ban is only
decidable by also reading `buff_source_broken`, which would force
`legal_actions()` to accept a `MonitorState` argument, breaking the
sealed `WorldState`-only rule and making the buggy engine's own action
availability depend on a spec-only fact it should have no way to know.
Accepting the resulting self-loop (legal, sometimes inert, action) is
more honest than fixing search-cost cosmetics by leaking spec state into
the engine. This is the first real evidence that "world dynamics" and
"property-monitoring dynamics" are not just separately-stored but can
have genuinely different notions of what counts as a no-op.

## `MonitorState` / `monitor_step`

```python
def monitor_step(prev_world, action, new_world, prev_monitor):
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = False
    elif new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, buff_source_broken=buff_source_broken)
```

## Oracle -- honest, OR-based, three-way attribution

```python
def classify(world, monitor):
    if world.quest_status != "CLAIMED":
        return None
    eq = monitor.continuity_broken
    buf = monitor.buff_source_broken
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None   # legitimate completion, not an exploit

def is_exploit(world, monitor):
    return classify(world, monitor) is not None
```

Sealed, and sealed for a reason worth restating: an earlier draft
required *both* `continuity_broken` and `buff_source_broken` before
calling something an exploit. That was rejected -- it would make the
oracle silently ignore a genuine equipment-continuity-only violation
(already proven to be a real bug by C1) purely to manufacture a "needs
both" research result, i.e. shaping ground truth around the desired
finding. The oracle reports every real violation; what C2 actually needs
to demonstrate is independence (next section), not joint necessity.

## What C2 must demonstrate: independence, not joint necessity

Not: *this exploit requires both properties*. The claim C2 tests: **do
`continuity_broken` and `buff_source_broken` carry genuinely different
information**, i.e. can a legal history reach each of the divergent
combinations. At minimum, both of `(continuity=True, buff=False)` and
`(continuity=False, buff=True)` must be reachable -- if only one
direction were reachable, the two fields would be (at least partially)
redundant.

Candidate witnesses (hand-derived, **not asserted as proven** -- QA below
proves or corrects these, the same discipline C1 used for its own
5-action witness):

| Category | Candidate witness | Len |
|---|---|---|
| Legitimate (no exploit) | `equip(Flame), channel, accept, claim` | 4 |
| `EQUIPMENT_CONTINUITY_VIOLATION` | `equip(Flame), accept, equip(Wood), equip(Flame), channel, claim` | 6 |
| `BUFF_SOURCE_LIFECYCLE_VIOLATION` | `equip(Flame), channel, equip(Wood), equip(Flame), accept, claim` | 6 |
| `BOTH` | `equip(Flame), channel, accept, equip(Wood), equip(Flame), claim` | 6 |

Note the structural reason each works: `EQUIPMENT`-only re-validates the
buff *after* the continuity-breaking excursion (channel is the last
buff-relevant event); `BUFF`-only breaks buff validity *before* `accept`
so continuity's `ACTIVE`-scoped check never fires; `BOTH` breaks
continuity during `ACTIVE` and never re-channels afterward.

## QA (two ordered steps, same discipline as C1, larger space)

**Step 1 -- closure equivalence**, unchanged in method from `C1c`'s fix:
enumerate by semantic closure over `(WorldState, reference-derived
monitor facts)`, not a raw-path depth bound (the raw history space is
still infinite). The semantic space is bigger now -- `WorldState` has
2 (equipped) x 3 (quest_status) x 2 (has_flame_buff) = 12 combinations,
crossed with 2x2 = 4 monitor combinations, for up to 48 theoretical
`(WorldState, continuity_broken, buff_source_broken)` triples (most
won't be reachable -- that's a result, not an input). An independent
`reference_*` function (full-history scan, no persisted running state)
is required for **both** monitored facts, checked against
`monitor_step`'s incremental computation on every generated transition,
before any dedup, exactly as C1c specified. This run is C2's data point
for the exhaustive-QA-scalability question `RESULTS_C1.md` flagged --
compare semantic-space size, transitions checked, and layers-to-closure
against C1's (12, 13, 7).

**Step 2 -- minimality, per category, only trustworthy once Step 1
passes.** Not one minimality claim -- three, since C2 introduces
three-way attribution: for each of `EQUIPMENT_CONTINUITY_VIOLATION`,
`BUFF_SOURCE_LIFECYCLE_VIOLATION`, and `BOTH`, exhaustively confirm no
shorter witness reaches that specific classification, and that the
candidate witness above does. (The legitimate 4-action path is not a
minimality claim -- there's nothing to minimize about a non-exploit --
but is worth confirming reachable as a sanity check that the case isn't
accidentally impossible to complete honestly.)

**Independence check**: after Step 1's closure completes, confirm both
`(True, False)` and `(False, True)` appear among the reachable
`(continuity_broken, buff_source_broken)` pairs -- discovered by running
the closure, not hardcoded as an expected-4-tuple list to assert against
(same principle as C1's "9 of 12" being a discovered result, not an
input).

## Non-goals for C2

No third lifecycle, no item-instance provenance beyond what C1 already
excluded, no generic cross-system oracle framework (two data points, C1
and C2, is still not "evidence" -- same standing rule), no negative
control added retroactively to C1 (deferred to become a permanent
regression test starting with C2's own QA suite, per the prior review),
no search-algorithm parameters decided yet (mirrors C1: core first,
search contract sealed separately once QA passes).
