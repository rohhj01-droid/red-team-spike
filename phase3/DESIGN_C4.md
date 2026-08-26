# Phase 3 C4 Design Spec

Status: draft, sealed before any C4 code exists. Same role as
`DESIGN_C1.md`/`DESIGN_C2.md`/`DESIGN_C3.md`. Per `RESULTS_C3.md`'s open
question, reframed precisely through brainstorming before this document:
C1-C3 established `world dynamics / property dynamics / violation
events`, with violation-event verdicts always ephemeral -- computed once
at a transition, reported, and discarded, never re-derived and never
referenced by anything downstream. C4 tests whether that ephemerality
assumption survives once a **second** violation event's legitimacy
depends on an **earlier** violation event's own verdict.

## C4 mechanism (sealed)

**Base: C2, unchanged, not C3.** `WorldState` (`equipped`, `quest_status`,
`has_flame_buff`), `MonitorState` (`continuity_broken`,
`buff_source_broken`), `claim()`'s single fault, and `classify_claim`
are reused byte-for-byte from C2c -- C3's Enchantment chain is
deliberately not carried forward. C3 already tested "does property
provenance need to be chained" (RESULTS_C3.md, RQ-A1); stacking that
same axis under C4 would make any C4 failure ambiguous between two
causes (chained property provenance vs. event-verdict persistence) --
exactly the attribution risk this project has avoided at every prior
choice point (C3's own A/B framing, C3's B/B' framing). C4 moves exactly
one new axis, built on the simplest base that's already fully verified.

**New: a second violation event, `consume`, whose legitimacy depends on
the frozen verdict of the one `claim` event that can ever occur.**
`claim()`'s effect gains one addition -- it unconditionally grants
`reward_owned = True` in `WorldState`, regardless of its own verdict,
mirroring C3's "legal-but-potentially-unqualified" pattern (`channel()`)
one level up: the world doesn't care whether the claim was legitimate,
only the spec-side judgment does. `consume()` is legal whenever
`reward_owned == True` (WorldState-only, never reads spec-derived
state) and sets `reward_owned = False` (one-shot, mirroring `claim`'s
own one-shot `quest_status` transition). Its *legitimacy* -- judged by a
new oracle, `classify_consume` -- depends on whether the reward it
consumes originated from a tainted `claim`.

**Boolean-only provenance, deliberately not the full three-way
category.** What survives from `claim` to `consume` is exactly one bit:
was the claim *any* kind of violation, yes or no. `classify_claim`'s
`EQUIPMENT_CONTINUITY_VIOLATION` / `BUFF_SOURCE_LIFECYCLE_VIOLATION` /
`BOTH` distinction is not propagated. Preserving it would open a second
new question (does categorical richness survive event-to-event
handoff) on top of the one C4 is actually testing (does a verdict need
to persist at all) -- the same reasoning C3 used to reject flat
multi-fact provenance in favor of testing one chain first.

## Sealed catalog and initial conditions

```python
EQUIPMENT_CATALOG = {"FlameSword", "WoodenSword"}   # unchanged from C1/C2
REQUIRED_EQUIPMENT = "FlameSword"                     # unchanged

initial WorldState:   equipped="WoodenSword", quest_status="NOT_ACCEPTED",
                       has_flame_buff=False, reward_owned=False
initial MonitorState: continuity_broken=False, buff_source_broken=False
                       # byte-for-byte C2c -- unchanged
initial EventProvenanceState: reward_provenance_tainted=False
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
  # unchanged

channel:
  requires: equipped == REQUIRED_EQUIPMENT
  effect:   has_flame_buff = True
  # unchanged from C2 -- NOT C3's enchant-gated version. No Enchantment
  # lifecycle exists in C4 at all.

claim (buggy, as actually shipped -- unchanged fault from C2c):
  requires: quest_status == ACTIVE and equipped == REQUIRED_EQUIPMENT
            and has_flame_buff == True
  effect:   quest_status = CLAIMED, reward_owned = True
  # reward_owned=True fires UNCONDITIONALLY -- claim() still has no idea
  # whether its own precondition-check was spec-honest; that's still the
  # single fault, now also the source of a persistent artifact.

consume:
  requires: reward_owned == True
  effect:   reward_owned = False
  # WorldState-only legality, like every other action. Never illegal
  # because of taint -- see the dedicated section below.
```

`claim` can fire at most once (`quest_status` never reverts from
`CLAIMED`); `consume` can therefore also fire at most once
(`reward_owned` only ever becomes `True` via that one `claim`, and
`consume` immediately zeroes it). No reward-regranting, no repeated
consumption -- deliberately, per Non-goals.

## `consume()` is legal-but-potentially-invalid -- not a second planted fault

Same discipline as `DESIGN_C3.md`'s `channel()` section, restated for
the new action: **`consume()`'s legality never depends on
`reward_provenance_tainted`.** It is decided purely by `WorldState`
(`reward_owned == True`). A `consume()` executed while the reward is
tainted is a completely ordinary, legal action -- the world lets it
happen exactly as it would for a clean reward. What differs is invisible
to the world: the *oracle* judges that this particular consumption used
a tainted artifact. `claim()` remains the only place a wrong
precondition-check was ever shipped; `consume()`'s own precondition
(`reward_owned == True`) is honest and correct. This keeps the
single-fault property intact across two events instead of one.

## `EventProvenanceState` -- a distinct boundary, not a fourth `MonitorState` field

**Rejected: folding `reward_provenance_tainted` into `MonitorState`.**
Computing it correctly requires `classify_claim(action, prev_monitor)`'s
*result* at the claim transition. `MonitorState` is produced by
`monitor_step`, and `oracle.py` already imports `monitor.py` for
`MonitorState`'s type -- having `monitor_step` call `classify_claim`
would require `monitor.py` to import `oracle.py`, a circular
dependency. Avoiding the cycle by inlining `classify_claim`'s OR-logic
directly into `monitor_step` avoids the crash but duplicates
ground-truth judgment logic across two files, breaking the "oracle is
the only place classification logic lives" rule kept since C1. Avoiding
*that* by passing the verdict into `monitor_step` as a parameter avoids
duplication but means the property monitor now accepts an event verdict
as input -- re-merging the two boundaries (`property dynamics` /
`violation events`) that `RESULTS_C2.md` established as separate. None
of these are *impossible*; all three cost something C2 already paid to
avoid. **This is not the only logically possible implementation -- it is
the one that preserves the sealed C2 boundaries while moving exactly one
new axis.**

**Adopted: a fourth, distinct state bucket**, computed strictly after
both `monitor_step` and `classify_claim`, never before:

```text
prev_world, prev_monitor, prev_provenance
        |
apply(action) -> new_world
        |
monitor_step(prev_world, action, new_world, prev_monitor) -> new_monitor
        |
claim_verdict   = classify_claim(action, prev_monitor)
consume_verdict = classify_consume(action, prev_provenance)
        |
event_provenance_step(action, claim_verdict, prev_provenance) -> new_provenance
```

`classify_claim`/`classify_consume` are computed unconditionally every
transition (each already gates internally on `action.kind`, so this is
uniform rather than requiring a per-call-site `if action.kind == ...`
guard) -- both read only the state that already existed *before* this
transition, matching every prior oracle's `prev_*`-only contract.

```python
@dataclass(frozen=True)
class EventProvenanceState:
    reward_provenance_tainted: bool

def initial_event_provenance() -> EventProvenanceState:
    return EventProvenanceState(reward_provenance_tainted=False)

def event_provenance_step(action, claim_verdict, prev_provenance):
    tainted = prev_provenance.reward_provenance_tainted
    if action.kind == "claim":
        tainted = claim_verdict is not None
    return EventProvenanceState(reward_provenance_tainted=tainted)
```

`tainted = claim_verdict is not None` (not `if ... and verdict is not
None: tainted = True`) is deliberate: it states the transition rule
directly -- *at the claim event, freeze `reward_provenance_tainted` to
reflect that verdict, whatever it is* -- rather than relying on
"`claim` only happens once, so leaving it alone in the legitimate case
happens to produce the same result" to be correct. No reset semantics
are needed or defined: `claim` fires at most once, so this field is set
at most once, ever.

## Oracle -- `classify_claim` unchanged, `classify_consume` new

```python
# classify_claim: byte-for-byte C2c, unchanged.

def classify_consume(action, prev_provenance):
    if action.kind != "consume":
        return None
    if prev_provenance.reward_provenance_tainted:
        return "TAINTED_REWARD_CONSUMPTION"
    return None
```

## Search target discovery is `consume`-only -- the critical scope decision this round

**A genuine violation event is not necessarily a search-terminal
discovery -- C4 is the first case where these two ideas come apart, and
getting this wrong would make the case unimplementable, not just
imprecise.** If a search algorithm terminated the instant *any* oracle
returned non-`None` (C1-C3's rule, restated in every prior
`SEARCH_CONTRACT_*.md`), a tainted `claim` would end the search
immediately -- `classify_claim` fires before `consume` can ever be
reached, so no path could ever demonstrate `TAINTED_REWARD_CONSUMPTION`
at all. `EventProvenanceState` would be written and never meaningfully
read by a discovering run.

**Sealed rule:** `classify_claim`'s verdict is recorded (captured into
`EventProvenanceState`) but never triggers a `Discovery` on its own.
Only `classify_consume` returning non-`None` is a discovery. Search must
survive past a tainted claim, not stop there.

This is a different distinction from `RESULTS_C3.md`'s "environment
terminality is not search terminality" (whether a *reached state* is
worth expanding further). This is about whether a *judged violation* is
worth *ending the search over*. Recorded here as a C4-specific
requirement, not generalized into "violations should never terminate
search" -- C1-C3's single-event cases were correctly terminal; a
multi-event case with nothing downstream of a given violation would
still be correctly terminal there too. The distinction is real but the
general shape of it is still one data point.

## What C4 must demonstrate

**1. `EventProvenanceState` is load-bearing, not cosmetic -- proven by a
bidirectional constructive pair**, mirroring C3's `Hclean`/`Htainted`
discipline but demonstrating both failure directions a naive
ambient-state read would produce:

```text
Witness P (false positive if ambient-read):
  equip(Flame), accept, channel, claim, equip(Wood), consume

Witness Q (false negative if ambient-read):
  equip(Flame), channel, equip(Wood), equip(Flame), accept, claim, channel, consume
```

In P, `claim` is legitimate (`reward_provenance_tainted = False`,
frozen), but the post-claim `equip(Wood)` -- an entirely ordinary,
already-established C2 behavior -- sets ambient `buff_source_broken =
True` anyway (`prev_world.has_flame_buff` doesn't check `quest_status`).
A `consume` oracle reading ambient `MonitorState` at this point would
wrongly call this tainted. In Q, `claim` is a genuine
`BUFF_SOURCE_LIFECYCLE_VIOLATION` (`reward_provenance_tainted = True`,
frozen), but the post-claim `channel` -- also already-established C2
behavior -- unconditionally resets ambient `buff_source_broken = False`.
An ambient-reading oracle would wrongly call this clean. Both are the
same C2c lesson ("ambient property state answers a different question
than a specific past event's verdict") re-applied one hop downstream,
not a new invariant invented for C4.

**2. The `consume`-only discovery rule actually works end to end** --
some algorithm, run under it, finds a `TAINTED_REWARD_CONSUMPTION`
witness. Not obvious in advance; this is what Section "Search target
discovery" above predicts should be possible and what would falsify it
if it weren't.

## Candidate witnesses (hand-derived, not asserted as proven)

| Category | Candidate witness | Len |
|---|---|---|
| Legitimate consume | `equip(Flame), accept, channel, claim, consume` | 5 |
| `TAINTED_REWARD_CONSUMPTION` | `equip(Flame), accept, equip(Wood), equip(Flame), channel, claim, consume` | 7 |

`claim`'s own three C2 categories (`EQUIPMENT_CONTINUITY_VIOLATION` /
`BUFF_SOURCE_LIFECYCLE_VIOLATION` / `BOTH`, all still real, judged,
recorded events) are not re-tabulated here -- their reachability and
minimality are C2's already-sealed result, inherited unchanged since
`claim()` itself didn't change. QA re-confirms they still hold under
C4's engine (sanity check that adding `reward_owned`/`consume` didn't
accidentally perturb them), not as new research content.

## QA (method carried forward, mechanics sealed as far as this round supports)

**Step 1 -- closure equivalence**, extended to the 3-tuple
`(WorldState, MonitorState, EventProvenanceState)` -- dedup/pruning key
`(WorldState, ref_continuity, ref_buff, ref_provenance)`. `monitor_step`
checked against `reference_continuity_broken`/`reference_buff_source_broken`
(both unchanged from C2c) exactly as before; `event_provenance_step`
checked against a new reference:

```python
def reference_reward_provenance_tainted(history):
    claim_index = None
    for i, action in enumerate(history):
        if action.kind == "claim":
            claim_index = i
            break   # claim fires at most once
    if claim_index is None:
        return False
    prefix = history[:claim_index]
    return reference_continuity_broken(prefix) or reference_buff_source_broken(prefix)
```

Independent of `event_provenance_step`'s incremental fold and of
`classify_claim` -- re-derives claim legitimacy directly from reference
property facts on the history prefix, the same "don't call the
production pipeline" discipline as C3's `reference_buff_source_broken`.
Includes Witnesses P and Q from the previous section as named, explicitly
reported checks, not left to fall out of the general sweep.

**Step 1b -- negative control**, sealed at the oracle layer rather than
the monitor layer for the first time (C4's boundary under test is
`classify_consume`'s input source, not a `monitor_step` fold):

```python
def known_bad_classify_consume(action, prev_monitor):
    """Negative control only. Reads AMBIENT MonitorState at consume-time
    instead of the frozen EventProvenanceState -- the exact mistake
    Section 'What C4 must demonstrate' #1 proves is wrong in both
    directions."""
    if action.kind != "consume":
        return None
    if prev_monitor.continuity_broken or prev_monitor.buff_source_broken:
        return "TAINTED_REWARD_CONSUMPTION"
    return None
```

Run against Witness P: returns `TAINTED_REWARD_CONSUMPTION` where the
reference says legitimate (false positive). Run against Witness Q:
returns `None` where the reference says tainted (false negative). A
single negative control producing mismatches in both directions from
the two witnesses already required by Section "What C4 must
demonstrate" -- stronger sensitivity evidence than C2's or C3's
negative controls, which only had to fail in one direction.

**Step 2 -- minimality**, for `TAINTED_REWARD_CONSUMPTION` (the actual
search target) plus a reachability sanity check for legitimate consume;
C2's three `claim`-level categories reconfirmed as a regression check,
not a new claim.

**Step 3 -- post-claim mutation regression**, carried forward in spirit
from C2c, but the interesting instance now *is* Witnesses P and Q --
they already are the "does a later thing get confused by ambient drift"
check, at the event level rather than the state level.

**Left for closer scrutiny when `verify_c4.py` is actually drafted,**
per this project's established pattern (C2's oracle bug and C3's
negative-control/reference fixes were both caught at exactly this
stage, not before): the precise closure-traversal restructuring needed
to check two oracle functions (`classify_claim`, `classify_consume`)
against one reference-key tuple without accidentally letting one
mask the other's mismatches.

## Non-goals for C4

No propagation of `claim`'s three-way category through to `consume` --
boolean provenance only (Section "C4 mechanism"). No repeated
consumption or reward-regranting -- both events are one-shot. No third
downstream event (`claim -> consume -> ???`) -- one new hop, matching
C3's one-hop-first discipline. No C3 Enchantment/chained-provenance
mechanism -- C2 base only. No generalization of "violation events don't
have to be search-terminal" beyond this case (Section "Search target
discovery"). No search-algorithm parameters or contract decided yet --
core and QA first, exactly as every prior case.
