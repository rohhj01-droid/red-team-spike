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

**Base: C2, not C3 -- reused unchanged where "unchanged" actually
applies, extended precisely where C4's new axis requires it.**

```text
Reused unchanged from C2c:
- equipment / quest / buff WorldState fields and their legality
- MonitorState / monitor_step
- classify_claim

Added by C4 (nothing above this line moved):
- WorldState.reward_owned
- claim's additive reward_owned=True effect (fires after the existing,
  unchanged claim precondition-check; the check itself didn't move)
- consume (new action)
- EventProvenanceState (new)
```

C3's Enchantment chain is deliberately not carried forward. C3 already
tested "does property provenance need to be chained" (RESULTS_C3.md,
RQ-A1); stacking that same axis under C4 would make any C4 failure
ambiguous between two causes (chained property provenance vs.
event-verdict persistence) -- exactly the attribution risk this project
has avoided at every prior choice point (C3's own A/B framing, C3's
B/B' framing). C4 moves exactly one new axis, built on the simplest
base that's already fully verified.

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

**Adopted: a third persistent state bucket** (`WorldState`,
`MonitorState`, `EventProvenanceState` -- `violation events` was never a
stored bucket in C1-C3, only a transition-local computation, so this is
C4's fourth *architectural component*, counting `RESULTS_C2.md`'s
`world dynamics / property dynamics / violation events` alongside it,
but its third literal data bucket), computed strictly after both
`monitor_step` and `classify_claim`, never before:

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
recorded events) are not re-tabulated here. `claim`'s legality and every
input `classify_claim` reads are unchanged; the new `reward_owned=True`
effect fires only *after* the claim transition is already decided, so it
cannot influence that decision. C2's witnesses for these three
categories should therefore still be exactly reachable and minimal
under C4's engine -- QA re-checks this as regression evidence (did
adding `reward_owned`/`consume` accidentally perturb something it
shouldn't have), not as new research content.

## QA (method carried forward, mechanics sealed as far as this round supports)

**Step 1 -- closure equivalence, four independent comparisons per
transition, sealed exactly (not deferred).** One closure sweep. For
every transition the sweep generates:

```python
new_world = apply(prev_world, action)
new_monitor = monitor_step(prev_world, action, new_world, prev_monitor)
claim_verdict = classify_claim(action, prev_monitor)
consume_verdict = classify_consume(action, prev_provenance)
new_provenance = event_provenance_step(action, claim_verdict, prev_provenance)
new_history = prev_history + [action]

ref_continuity = reference_continuity_broken(new_history)
ref_buff = reference_buff_source_broken(new_history)
ref_provenance = reference_reward_provenance_tainted(new_history)
ref_claim_verdict = reference_classify_claim(prev_history, action)
ref_consume_verdict = reference_classify_consume(prev_history, action)
```

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

def reference_classify_claim(history_before, action):
    if action.kind != "claim":
        return None
    eq = reference_continuity_broken(history_before)
    buf = reference_buff_source_broken(history_before)
    if eq and buf:
        return "BOTH"
    if eq:
        return "EQUIPMENT_CONTINUITY_VIOLATION"
    if buf:
        return "BUFF_SOURCE_LIFECYCLE_VIOLATION"
    return None

def reference_classify_consume(history_before, action):
    if action.kind != "consume":
        return None
    if reference_reward_provenance_tainted(history_before):
        return "TAINTED_REWARD_CONSUMPTION"
    return None
```

`reference_classify_claim`/`reference_classify_consume` are new: C4 is
the first case where the *oracle itself*, not just the monitor fold
beneath it, gets an independent reference -- because C4's actual
research content is downstream event judgment, checking only the
property facts underneath it would leave the most important layer
unverified. Neither calls `classify_claim`/`classify_consume`/
`event_provenance_step` -- both re-derive from reference property
functions on `history_before` directly, the same "don't call the
production pipeline" discipline as C3's `reference_buff_source_broken`.

**Four separate comparisons, four separate mismatch counters -- never
one combined pass/fail**, so a mismatch in one can never be masked by
another passing:

1. `(new_monitor.continuity_broken, new_monitor.buff_source_broken) == (ref_continuity, ref_buff)`
2. `new_provenance.reward_provenance_tainted == ref_provenance`
3. `claim_verdict == ref_claim_verdict`
4. `consume_verdict == ref_consume_verdict`

**Dedup/pruning key for closure traversal:** `(new_world, ref_continuity,
ref_buff, ref_provenance)` -- reference-derived, never production-derived,
same discipline as C1-C3 (canonical closure identity must not depend on
whatever production happens to compute, including when production is
wrong). Includes Witnesses P and Q as named, explicitly reported checks
inside this sweep, not left to fall out of it by chance.

**Step 1b -- negative control, run through the identical sweep,
two-directional, sealed exactly.** `known_bad_classify_consume`
substituted for `classify_consume` in the same closure procedure --
`comparison 4` above becomes `known_bad_classify_consume(action,
prev_monitor) == ref_consume_verdict`, tracked with two separate
counters rather than one:

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

- `false_positive_count`: known_bad returns `"TAINTED_REWARD_CONSUMPTION"`
  where the reference says legitimate.
- `false_negative_count`: known_bad returns `None` where the reference
  says tainted.

**Requirement, sealed before either classifier runs:** production's four
comparisons all reach 0 mismatches; `known_bad_classify_consume`'s
substitution produces `false_positive_count >= 1` **and**
`false_negative_count >= 1` -- both directions required, not just one,
since Witnesses P and Q were specifically constructed to force each
independently. Witness P's `consume` transition must appear among the
false positives; Witness Q's must appear among the false negatives --
checked as named assertions, not inferred from a nonzero total.

**Step 2 -- minimality**, for `TAINTED_REWARD_CONSUMPTION` (the actual
search target) plus a reachability sanity check for legitimate consume;
C2's three `claim`-level categories reconfirmed as a regression check,
not a new claim.

**Step 3 -- post-claim mutation regression**, carried forward in spirit
from C2c, but the interesting instance now *is* Witnesses P and Q --
they already are the "does a later thing get confused by ambient drift"
check, at the event level rather than the state level.

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
