# Phase 3 C3 Design Spec

Status: draft, sealed before any C3 code exists. Same role as
`DESIGN_C1.md`/`DESIGN_C2.md`. Per `RESULTS_C2.md`'s closing question,
reframed precisely through brainstorming before this document: C1 and C2
together established `world dynamics / property dynamics / violation
events` as the architecture, with `MonitorState` always a flat tuple of
booleans, each foldable **independently** of its sibling fields. C3 tests
whether that independence survives once one property's validity is
genuinely provenance-dependent on another property's history -- not
whether the flat *shape* survives (it trivially can: one more boolean is
still a tuple).

## C3 mechanism (sealed)

**Single architectural fault, unchanged in kind from C1/C2, now with a
provenance chain behind one of its inputs.** `claim()` still only checks
`equipped == REQUIRED_EQUIPMENT` (current snapshot) and `has_flame_buff
== True` (current presence) -- exactly C2's fault, byte-for-byte. What's
new is *how* `has_flame_buff` can come to exist: C2 had one way to
acquire it (`channel()`, gated only by current equipment). C3 adds a
prerequisite lifecycle -- **Enchantment** -- that `channel()` now
requires, and whose own broken-and-restored history determines whether a
given `channel()` was a trustworthy grant, without `channel()` itself
ever becoming illegitimate (see the dedicated section below -- this is
the critical distinction this design round exists to nail down).

Three monitor facts, three different recovery semantics -- deliberately,
so no two facts are reducible to each other by pattern-matching their
shape alone:

- `continuity_broken` -- unchanged from C1/C2. Permanent per quest
  attempt, no reset.
- `enchant_broken` -- new. Permanent once set (same family as
  `continuity_broken`), but triggered by a dedicated `unenchant` action
  that is **structurally independent of `equip`** -- deliberately, so
  `enchant_broken` cannot be re-derived from `equipped`'s own transition
  history. If it were equip-triggered, chaining `buff_source_broken`
  through it would carry no information beyond what C2's flat design
  already read directly off `WorldState`, and C3 would be testing
  nothing new.
- `buff_source_broken` -- C2's rule, plus one new branch: at the instant
  `channel()` fires, it **captures** `enchant_broken`'s current value
  (grant-time provenance), on top of the unchanged post-grant
  equipment-based break rule it already had.

## Sealed catalog and initial conditions

Reuses C1/C2's equipment catalog and `REQUIRED_EQUIPMENT` unchanged,
extended with the enchantment field:

```python
EQUIPMENT_CATALOG = {"FlameSword", "WoodenSword"}   # unchanged
REQUIRED_EQUIPMENT = "FlameSword"                     # unchanged

initial WorldState:   equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False, enchanted=False
initial MonitorState: continuity_broken=False, buff_source_broken=False,
                       enchant_broken=False
```

## Actions (sealed)

```
equip(item):
  requires: item in EQUIPMENT_CATALOG and item != currently_equipped
  effect:   equipped = item
  # unchanged from C1/C2

accept:
  requires: quest_status == NOT_ACCEPTED and equipped == REQUIRED_EQUIPMENT
  effect:   quest_status = ACTIVE
  # unchanged -- still doesn't reference buff or enchantment at all

enchant:
  requires: enchanted == False   # no-op banned, like equip
  effect:   enchanted = True

unenchant:
  requires: enchanted == True
  world effect:   enchanted = False
  monitor effect: enchant_broken = True   # permanent -- see below

channel:
  requires: equipped == REQUIRED_EQUIPMENT and enchanted == True   # NEW: was equipped-only in C2
  # NO no-op ban -- unchanged reasoning from DESIGN_C2.md's "WorldState
  # no-op can be a MonitorState non-no-op": legal_actions() stays
  # WorldState-only, so a redundant channel() is still legal and can
  # still change buff_source_broken (re-capture) even when it doesn't
  # change has_flame_buff.
  world effect:   has_flame_buff = True
  monitor effect: buff_source_broken = prev_monitor.enchant_broken
                  # grant-time capture -- see below. ALWAYS applies,
                  # regardless of enchant_broken's value: channel is
                  # never illegal because of it.

claim (buggy, as actually shipped -- unchanged from C2, byte-for-byte):
  requires: quest_status == ACTIVE and equipped == REQUIRED_EQUIPMENT
            and has_flame_buff == True
  effect:   quest_status = CLAIMED
  # presence-only on both conditions -- still the single fault. claim()
  # has no idea has_flame_buff's own provenance is now layered; it was
  # never supposed to.
```

The `channel` precondition addition (`enchanted == True`) closes a real
gap, not a stylistic one: without it, `channel()` could fire having never
enchanted at all, and since `enchant_broken` defaults `False`,
`buff_source_broken` would capture `False` -- a buff that looks validly
sourced despite no enchantment ever backing it. Requiring `enchanted ==
True` to channel at all means `enchant_broken`'s default value is never
load-bearing for a buff that was never actually enchanted; provenance
capture only ever fires at a moment when *some* enchantment genuinely
exists.

## `channel()` is legal-but-potentially-unqualified -- not a second fault

The one wording mistake this design round caught and fixed, worth
sealing explicitly so it can't drift back in during implementation:
**`channel()`'s legality never depends on `enchant_broken`.** It is
decided purely by `WorldState` (`equipped == REQUIRED_EQUIPMENT and
enchanted == True`), exactly like every other action's legality. A
`channel()` executed while `enchant_broken == True` is a completely
ordinary, legal action -- the world grants `has_flame_buff = True` just
as it would under a clean enchantment. What differs is invisible to the
world entirely: the *monitor* records that this particular grant
inherited a broken provenance. `legal != qualified-for-downstream-use`
is the exact distinction -- and it's what keeps the single-fault
property intact. If `channel()`'s legality had instead depended on
enchant continuity, a bad `channel()` call would itself become a second
violating decision point, and any future finding would need to first
untangle whether it came from `claim()`'s fault or `channel()`'s before
it could be attributed at all -- exactly the ambiguity C3 was scoped to
avoid by keeping the planted fault singular.

`unenchant`'s `enchant_broken = True` effect is permanent, matching
`continuity_broken`'s family, not `buff_source_broken`'s. A later
`enchant()` **restores current presence** (`enchanted = True`) but does
**not** restore provenance qualification -- deliberately avoided wording:
not "a new enchantment instance," since C3 does not model instance
identity at all; there is exactly one `enchanted` bit, and what's
permanent is a fact *about* its history, not a fact about which
"instance" currently occupies it.

## `MonitorState` / `monitor_step`

```python
def monitor_step(prev_world, action, new_world, prev_monitor):
    continuity_broken = prev_monitor.continuity_broken
    if new_world.quest_status == "ACTIVE" and new_world.equipped != REQUIRED_EQUIPMENT:
        continuity_broken = True

    enchant_broken = prev_monitor.enchant_broken
    if prev_world.enchanted and not new_world.enchanted:
        enchant_broken = True

    buff_source_broken = prev_monitor.buff_source_broken
    if action.kind == "channel":
        buff_source_broken = prev_monitor.enchant_broken   # grant-time capture
    elif prev_world.has_flame_buff and new_world.equipped != REQUIRED_EQUIPMENT:
        buff_source_broken = True

    return MonitorState(continuity_broken=continuity_broken,
                         enchant_broken=enchant_broken,
                         buff_source_broken=buff_source_broken)
```

Written with the same confidence C2's original (pre-C2b) formula was --
expect this may need its own correction once `verify_c3.py`'s closure
QA runs against an independent reference, exactly like C1b/C1c and
C2b/C2c. Not sealed as final until that happens; sealed as *this round's*
starting point.

**The precise research question, restated to avoid the imprecise version
used earlier in brainstorming:** not "does `MonitorState` stop being a
flat tuple" (it doesn't -- `enchant_broken` is a third boolean, same
shape). The actual break: C1 and C2's monitor facts were each
**component-wise independent** -- foldable from only their own prior
value plus the current world transition, with zero knowledge of sibling
fields. `buff_source_broken`'s new `channel` branch reads
`prev_monitor.enchant_broken`, a sibling field, for the first time.
Whether a flat-but-cross-referencing representation remains sufficient,
or whether some future case would force `MonitorState` into an actual
dependency graph, is the open question C3 is the first data point for --
not decided by this document, only tested by it.

## Oracle -- unchanged from C2c

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
    return None

def is_exploit(action, prev_monitor):
    return classify_claim(action, prev_monitor) is not None
```

Not touched at all -- still transition-based, still only reads
`continuity_broken`/`buff_source_broken`, still three-way. `enchant_broken`
is never read by the oracle directly; it only ever reaches `claim()`'s
judgment by way of having already been captured into
`buff_source_broken` at some earlier `channel()`. This is deliberate: C3
is not adding a fourth classification category. It's testing whether an
*existing* category (`BUFF_SOURCE_LIFECYCLE_VIOLATION`) can now be
reached through a second, causally distinct pathway.

## What C3 must demonstrate

**1. The cross-reference is load-bearing, not cosmetic.** Any monitor
fact is, by definition, some function of the raw action history --
`qa_reference.py`-style full-history rescans can always reproduce any of
them without ever materializing intermediate fields. So "can
`buff_source_broken`'s value be reproduced some other way" is not the
question (trivially yes, always). The question is representational: does
correct *incremental* computation of `buff_source_broken` require
reading `enchant_broken` as a stored sibling field, rather than being
foldable in isolation the way both C1's and C2's original facts were.
The `monitor_step` above already answers this by construction -- QA's
job is to confirm the independent reference agrees, not to re-litigate
the representation choice.

**2. The new pathway is real, not redundant with the old one.** C2's
existing route to `BUFF_SOURCE_LIFECYCLE_VIOLATION` (grant a buff, then
later leave `REQUIRED_EQUIPMENT`) still exists unchanged in C3. QA must
confirm two witnesses, not one:

- A witness reaching `BUFF_SOURCE_LIFECYCLE_VIOLATION` **purely through
  the new enchant-chain pathway** -- `continuity_broken == False`
  throughout, `equipped` never leaves `REQUIRED_EQUIPMENT` after the
  buff is granted, and the violation comes entirely from a tainted
  `channel()` capture.
- A witness reaching the same classification through **the original C2
  pathway**, confirming the new fact didn't silently subsume or replace
  the old one.

If only one of the two is reachable, the "chain" claim is weaker than
intended -- either the new pathway doesn't actually work, or it turned
out to be the only way left to reach that category, which would itself
be worth reporting honestly rather than smoothing over.

## Candidate witnesses (hand-derived, not asserted as proven)

| Category | Candidate witness | Len |
|---|---|---|
| Legitimate | `equip(Flame), enchant, channel, accept, claim` | 5 |
| `EQUIPMENT_CONTINUITY_VIOLATION` | `equip(Flame), enchant, accept, equip(Wood), equip(Flame), channel, claim` | 7 |
| `BUFF_SOURCE_LIFECYCLE_VIOLATION` (old pathway, post-grant equip break) | `equip(Flame), enchant, channel, equip(Wood), equip(Flame), accept, claim` | 7 |
| `BUFF_SOURCE_LIFECYCLE_VIOLATION` (new pathway, tainted grant, isolated) | `equip(Flame), enchant, unenchant, enchant, accept, channel, claim` | 7 |
| `BOTH` | `equip(Flame), enchant, channel, accept, equip(Wood), equip(Flame), claim` | 7 |

Every category grows by exactly one action relative to its C2 analogue
-- the mandatory `enchant` before any `channel()` can be legal at all.
QA (next round) proves or corrects both the classifications and the
minimality of each; the fourth row (new-pathway BUFF witness, with
`continuity_broken == False` for its entire length) is the one Section
"What C3 must demonstrate" actually depends on.

## QA (method carried forward from C1/C2, exact mechanics next round)

Same two-ordered-steps discipline: **Step 1**, closure equivalence over
the semantic space, checked against an independent full-history
reference for all three facts before any dedup, exactly as C1c and C2c
require. **Step 1b**, a permanent negative control (a `known_bad`
variant that gets the grant-time capture wrong -- e.g. capturing
`enchant_broken`'s value *after* processing the channel rather than
before, or omitting the capture and leaving `buff_source_broken`
untouched by `channel()` entirely). **Step 2**, per-category minimality,
now including the pathway-isolation witness above as its own explicit
check, not folded into the general `BUFF_SOURCE_LIFECYCLE_VIOLATION`
minimality claim. **Step 3**, the post-claim mutation regression C2c
added, carried forward unchanged (still applicable -- `claim` is still
the only judged event).

Left open for the next design round, deliberately not decided here: the
exact independent-reference formula for `buff_source_broken` (does
`qa_reference.py` need its own `reference_enchant_broken` that
`reference_buff_source_broken` calls, or must the two stay fully
textually independent the way `monitor_step`'s fields do internally --
this is a real methodological question, not a detail). Resolving it by
staring at the mechanism in the abstract risks getting it wrong the same
way the original C2 oracle did; better to draft `qa_reference.py` and let
an actual closure run surface the real issue, per this project's
established pattern.

## Non-goals for C3

No fourth classification category (Section "Oracle" above). No item-
instance/provenance identity modeling (Section "channel() is
legal-but-potentially-unqualified" above -- re-enchant restores presence,
not identity). No generic provenance-graph abstraction regardless of
what this case's results show (three data points, C1/C2/C3, still isn't
a trend to build a framework from). No search-algorithm parameters or
contract decided yet -- core and QA first, exactly as every prior case.
