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
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, buff_source_broken=buff_source_broken)
```

**C2b correction**: the `buff_source_broken` branch now gates on
`prev_world.has_flame_buff`. Without that gate, the field could become
`True` before any buff has ever existed -- e.g. `equip(Flame) ->
equip(Wood)` with no `channel()` in between sets it `True` even though
`has_flame_buff` is still `False`, which has no coherent reading under
the sealed meaning ("has the source broken *since the buff was last
validated*" presupposes a buff to validate). This never changes the
oracle's judgment at any *reachable claimed* state -- `claim()` requires
`has_flame_buff == True`, so any completed claim's history already
contains at least one `channel()` call, and `channel()` unconditionally
overwrites whatever came before -- but it does pollute Step 1's closure
with semantically meaningless extra states and, worse, was exactly
ambiguous enough that an independently-written `monitor_step` and
`reference_*` could plausibly disagree on it by accident, producing a
false "mismatch" that's really just an unresolved spec question, not a
real bug. Sealed now so neither implementation has to guess.
`buff_source_broken` stays `False` for as long as no buff exists.

## Oracle -- transition-based, not state-based (C2c correction)

**C2c correction**: the oracle first sealed here evaluated
`classify(world, monitor)` as a predicate on *whatever the current
world/monitor happen to be* -- correct for C1, where it was never
actually exercised, but wrong here. Running `verify_c2.py`'s Step 2
minimality check surfaced a real 5-action sequence, `equip(Flame),
accept, channel, claim, equip(Wood)`, that a state-based oracle
misclassifies as `BUFF_SOURCE_LIFECYCLE_VIOLATION` even though the
`claim` at step 4 was completely legitimate (`continuity_broken` and
`buff_source_broken` were both `False` at that moment) -- the final
`equip(Wood)` at step 5, entirely after the quest was already claimed,
is what flips `buff_source_broken` back to `True` and fools a query on
the final state.

Root cause: `quest_status` latches at `CLAIMED` forever, but
`buff_source_broken` keeps tracking honestly *after* claim too (it
describes present buff validity, not claim legitimacy -- correctly so,
see below). `continuity_broken` never exposed this because its own
trigger condition requires `quest_status == "ACTIVE"`, which structurally
can never hold again once claimed -- so continuity_broken was
accidentally frozen post-claim, and C1 never had a second fact around to
reveal that this was an accident rather than a designed guarantee.

**Rejected fix: freeze `MonitorState` once `quest_status == "CLAIMED"`.**
This would make `monitor_step` lie -- `buff_source_broken` is defined as
*current* buff-source validity, and un-equipping the required item after
a legitimate claim really does invalidate the buff going forward. A
property monitor that stops reflecting reality once a judgment has been
made about it conflates "tracking a fact" with "having ruled on a fact."

**Adopted fix: the oracle judges a `claim` *event*, not a state.**
`MonitorState` and `monitor_step` are unchanged -- `buff_source_broken`
keeps updating honestly forever, exactly as before. What changes is that
"is this an exploit" is no longer a question askable of an arbitrary
state; it is asked exactly once, at the instant a `claim` action
executes, using the monitor value as of immediately before that action:

```python
def classify_claim(action, prev_monitor):
    if action.kind != "claim":
        return None
    eq = prev_monitor.continuity_broken
    buf = prev_monitor.buff_source_broken
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None   # legitimate completion, not an exploit

def is_exploit(action, prev_monitor):
    return classify_claim(action, prev_monitor) is not None
```

The OR-based, honest, three-way attribution is unchanged in substance --
only *when* it is evaluated changed, from "any time you ask" to "the
moment claim fires." The earlier rejection of a "both required" draft
(same reasoning as before: reports every real violation, doesn't shape
ground truth to manufacture a "needs both" result) is unaffected by this
correction.

**Architecture finding, carried forward:** C1's WorldState/MonitorState
boundary implicitly assumed the exploit predicate is state-local --
Markov in `(WorldState, MonitorState)`, askable at any point and always
answering the same live question. C2 is the first case where that
assumption breaks: a violation is a judgment about a specific past
*event* (the `claim` transition), not a fact about the present. Going
forward there are three distinct things, not two: **world dynamics**
(`apply`), **property dynamics** (`monitor_step`, always current, always
honest), and **violation events** (evaluated only at the transition that
matters, never re-derived later). `RESULTS_C1.md` framed C2's open
question as whether the C1 boundary "survives" a second lifecycle; the
more precise answer is that the boundary survives but needed a third
piece next to it.

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
shorter history's `claim` *transition* reaches that specific
classification (per the C2c oracle correction above -- checked at
`claim` actions specifically, not at arbitrary visited states), and that
the candidate witness above does. (The legitimate 4-action path is not a
minimality claim -- there's nothing to minimize about a non-exploit --
but is worth confirming reachable as a sanity check that the case isn't
accidentally impossible to complete honestly.)

**Step 3 -- post-claim mutation regression (new in C2c), permanent
alongside the negative control.** Proof the transition-based oracle
actually behaves differently from the rejected state-based one, in both
directions: (a) a legitimate `claim` followed by an unrelated post-claim
equipment swap must **not** retroactively read as an exploit; (b) a
violating `claim` followed by a post-claim `channel()` (which resets
*current* `buff_source_broken`) must **not** erase the already-recorded
verdict. Both are regression tests against the exact failure mode Step 2
found, not hypothetical edge cases.

**Independence check**: after Step 1's closure completes, confirm both
`(True, False)` and `(False, True)` appear among the reachable
`(continuity_broken, buff_source_broken)` pairs -- discovered by running
the closure, not hardcoded as an expected-4-tuple list to assert against
(same principle as C1's "9 of 12" being a discovered result, not an
input).

**Negative control -- sealed now, as a permanent regression test (C1's
was a throwaway process; C2's becomes part of the QA suite going
forward, per `RESULTS_C1.md`'s architecture decision).** Exactly one
`known_bad_monitor_step`, chosen for hitting C2's actual new lesson
(re-equipping is not revalidating -- `channel()` is the only
revalidation) rather than an arbitrary unrelated defect:

```python
def known_bad_monitor_step(prev_world, action, new_world, prev_monitor):
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if new_world.equipped == REQUIRED_EQUIPMENT:
        buff_source_broken = False   # BUG: re-equipping alone "revalidates" -- no channel() needed
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken, buff_source_broken=buff_source_broken)
```

Requirement, sealed before either monitor is run: the production
`monitor_step` passes Step 1's closure equivalence with zero mismatches
(as required above); `known_bad_monitor_step`, run through the identical
Step 1 procedure, **must** produce at least one mismatch against the
independent reference. The exact mismatch count is not sealed and isn't
asserted to any specific number -- only that it's `>= 1` -- the count
itself is a result to report, not a target to hit.

## Non-goals for C2

No third lifecycle, no item-instance provenance beyond what C1 already
excluded, no generic cross-system oracle framework (two data points, C1
and C2, is still not "evidence" -- same standing rule), no search-
algorithm parameters decided yet (mirrors C1: core first, search
contract sealed separately once QA passes).
