# C3 Results (sealed)

Consolidates what `DESIGN_C3.md` (plan, through C3c), `verify_c3.py`
(core QA), `SEARCH_CONTRACT_C3.md` (search contract), `ecbd536`'s
official search integration run, and `e3bdfeb`'s post-hoc diagnostic
each separately established. C3 is closed as of this document -- no
further tuning or re-running.

## 1. Question / planted mechanism

**Single architectural fault, now with a provenance chain behind one of
its inputs.** `claim()` is byte-for-byte unchanged from C2c -- it still
only checks `equipped == REQUIRED_EQUIPMENT` (snapshot) and
`has_flame_buff == True` (presence). What's new: `channel()`, the only
way to acquire `has_flame_buff`, now requires a prerequisite
**Enchantment** lifecycle (`enchanted`), and captures that lifecycle's
broken-and-restored history into `buff_source_broken` at the instant it
fires -- without `channel()` itself ever becoming a second illegitimate
decision point (`legal != qualified-for-downstream-use`, sealed in
`DESIGN_C3.md`).

Shortest witnesses, proven not merely asserted (Section 4.1):

| Category | Len |
|---|---|
| Legitimate | 5 |
| `EQUIPMENT_CONTINUITY_VIOLATION` | 7 |
| `BUFF_SOURCE_LIFECYCLE_VIOLATION` (global) | 7 |
| `OLD_EQUIPMENT_SOURCE_PATHWAY` | 7 |
| `NEW_CHAIN_PATHWAY` | 7 |
| `BOTH` | 7 |

## 2. RQ-A1 -- Representation (the central result)

**Component-wise independent monitor folding -- the implicit structure
C1 and C2 both relied on without ever testing it -- broke for the first
time, and the break is proven by construction, not inferred from how
`monitor_step` happens to be written.**

|  | theoretical states | reachable | transitions checked | layers |
|---|---|---|---|---|
| C1 | 12 | 9 | 13 | 7 |
| C2 | 48 | 19 | 40 | 8 |
| C3 | 192 | 62 | 174 | 11 |

`monitor_step` matched the independent full-history reference
(`reference_continuity_broken`/`reference_enchant_broken`/
`reference_buff_source_broken`, the last of which locates the last
`channel` by a plain scan and checks each side of it via separate
replays -- never calling the other two references or mirroring
`monitor_step`'s own fold) on all 174 generated transitions, 0
mismatches.

**The precise claim, stated the way `DESIGN_C3.md`'s C3b revision fixed
it:** not that `MonitorState` stopped being a flat tuple (it didn't --
`enchant_broken` is a third boolean, same shape). The break is that
`buff_source_broken`'s correct incremental update, for the first time,
requires reading a *sibling* `MonitorState` field
(`prev_monitor.enchant_broken`) rather than being foldable from only its
own prior value and the current world transition, the way every C1/C2
fact was.

This was proven with a constructive indistinguishability pair, not
inferred from the implementation choice:

```text
Hclean:    equip(Flame), enchant
Htainted:  equip(Flame), enchant, unenchant, enchant
```

Confirmed by `verify_c3.py`'s dedicated check (not left to fall out of
the general closure sweep): immediately before a `channel()`, both
histories reach an identical `WorldState` and an identical prior
`buff_source_broken` (`False` in both) -- the only difference is
`enchant_broken` (`False` vs. `True`). Executing the same `channel()`
from both produced `buff_source_broken = False` after `Hclean` and
`True` after `Htainted`. No function of `(prev_buff_source_broken,
prev_world, action, new_world)` -- i.e. no component-wise-independent
fold -- can return both answers from identical arguments. The sibling
read is load-bearing by construction, confirmed by running the actual
code against this exact pair, not asserted from the fact that
`monitor_step` happens to contain one.

**Scope of this claim: one sibling dependency, one hop.** C3 shows a
flat-but-cross-referencing `MonitorState` can still work -- it does not
show *how far* that can be pushed (deeper chains, multiple
simultaneous cross-references) before some other representation becomes
necessary. That is untested.

## 3. RQ-A2 -- Attribution

Three-way, OR-based, honest attribution -- `classify_claim`, unchanged
from C2c -- held up under the added chain. All 8
`(continuity_broken, enchant_broken, buff_source_broken)` triples are
reachable (the three facts are maximally independent in reachability
terms), and both `OLD_EQUIPMENT_SOURCE_PATHWAY` and `NEW_CHAIN_PATHWAY`
-- mutually exclusive by construction (`classify_pathway`, gated on
`classify_claim` already having returned `BUFF_SOURCE_LIFECYCLE_VIOLATION`)
-- are independently reachable at the same minimal length (7), via
witnesses that isolate each cause from the other (`OLD`:
`continuity_broken == False` and the taint comes entirely from a
post-grant equipment break; `NEW`: `continuity_broken == False` and the
taint comes entirely from a pre-grant enchantment break, with zero
reliance on the equipment-break path).

Every witness the search algorithms found (Section 4.2/4.3) was
independently replayed from scratch and re-evaluated via the sealed
`classify_claim()` at its actual `claim` transition -- confirms each
algorithm's own bookkeeping against a fresh recomputation using the
*same* sealed oracle, not a separately-implemented one (that stronger
guarantee is Step 1's job, already established above).

**Negative control:** production monitor, 0 mismatches;
`known_bad_monitor_step` (channel unconditionally cleanses
`buff_source_broken`, ignoring upstream provenance -- C2's exact rule,
now wrong) produced 11 mismatches through the identical closure
procedure.

## 4. RQ-A3 -- Reproduction

### 4.1 Ground-truth reproduction -- PASS

Exhaustive `SearchState`-deduped search to depth 6 confirmed no shorter
history's `claim` reaches any of `EQUIPMENT_CONTINUITY_VIOLATION`,
`BUFF_SOURCE_LIFECYCLE_VIOLATION` (global), `OLD_EQUIPMENT_SOURCE_PATHWAY`,
`NEW_CHAIN_PATHWAY`, or `BOTH` -- five minimality claims, all confirmed
minimal at length 7; the legitimate 5-action completion confirmed
reachable as a sanity check. Both `BUFF_SOURCE_LIFECYCLE_VIOLATION`
pathways are independently executable, not just independently
classifiable.

### 4.2 Frozen search integration -- FAIL

```text
Random        10/10 seeds
Beam-Naive    no discovery
Beam-Diverse  no discovery
MCTS          10/10 seeds

C3 SEARCH INTEGRATION: FAIL
```

No parameter was retuned and no check was relaxed after seeing this --
`ecbd536` seals it exactly as the first and only official run produced
it.

**The failure does not invalidate 4.1's existence/minimality result; it
shows that two of the four frozen search policies failed to recover an
already-proven executable witness.** Three separate facts, not one:

```text
witness exists?                  YES (4.1)
minimal witness proven?          YES (4.1)
all frozen searches recover it?  NO  (4.2)
```

Root cause, established by layer-by-layer tracing of the actual search
run (not inferred from the failure alone -- Random/MCTS succeeding is
supporting evidence the oracle/monitor/dedup/visibility machinery works,
but does not by itself rule out a Beam-specific bug; the trace does):
under `score(world) = quest-status ordinal`, a legitimately-reached
`CLAIMED` state scores higher than any still-in-progress `ACTIVE`
candidate, regardless of exploit relevance. `quest_status` never reverts
from `CLAIMED`, so such a state is terminal with respect to producing
any *future* exploit-triggering `claim` -- but nothing in the frozen
search policy treats it that way, and it keeps generating descendants.
C3's richer post-claim action set (`equip` + `enchant`/`unenchant` +
possibly `channel`, up to 3 legal actions vs. C1's 1 and C2's 2) makes
those dead-end descendants multiply fast enough to displace every
still-alive exploit-capable `ACTIVE` branch under `BEAM_WIDTH=5`, before
depth 7 (where C3's minimal witnesses live). **Scope: this is C1/C2's
frozen search policy failing under C3's specific branching increase --
not a general claim that Beam is weak in richer domains.**

### 4.3 Post-hoc diagnostic -- hypothesis supported, official result unchanged

A single, isolated intervention, run and reported entirely separately
from 4.2's sealed result: beam members whose `WorldState` has
`quest_status == "CLAIMED"` are excluded from expansion. `BEAM_WIDTH`,
`score()`, `behavior_descriptor()`, novelty weighting, `MAX_DEPTH`,
`BUDGET` all held at their frozen contract values.

```text
                official (4.2)    diagnostic (CLAIMED-terminal)
Beam-Naive      no discovery      7-action witness,  cost 62
Beam-Diverse    no discovery      11-action witness, cost 105
```

Both variants found a witness once legitimate `CLAIMED` states stopped
being expanded -- not a comparison of algorithm performance, the result
of one controlled intervention testing one hypothesis. **Under the
frozen search policy, legitimately completed `CLAIMED` states were
terminal with respect to future exploit-producing `claim` events but
non-terminal to the search itself. Because `score(CLAIMED) = 2` was
maximal and C3 introduced richer post-claim branching, their
descendants displaced exploit-capable `ACTIVE` branches. A post-hoc
intervention that changed only this terminality treatment restored
discovery for both Beam variants, supporting this mechanism as the
cause of the official failure.** Restored *discovery*, not restored
*PASS* -- `ecbd536`'s sealed result is unchanged; this section explains
it, not overturns it. Also not claimed: that CLAIMED-terminality is the
*only* possible cause -- it is the one hypothesis tested, and it held.

## 5. Architecture and methodology decisions carried forward

- **Presence is not validity**, and **a `WorldState` no-op can be a
  `MonitorState` non-no-op** -- both unchanged from C1/C2, both still
  load-bearing in C3's `channel()`.
- **A violation can be transition-local, not state-local** (C2c) --
  unchanged, still the shape of `classify_claim`.
- **Component-wise independent monitor folding is not guaranteed** --
  C1 and C2 never tested it, both happened to have it, and it is
  possible to lose it deliberately (one sibling-field read) while still
  producing a flat, closure-verifiable `MonitorState`. This is C3's
  central result (Section 2), restated here as a standing fact for
  future cases to check, not assume.
- **New: environment terminality and search terminality are distinct
  modeling decisions.** `legal_actions()` correctly keeps offering
  `equip`/`enchant`/`unenchant`/`channel` after a legitimate `claim` --
  that is honest world modeling, nothing is wrong with it. But whether a
  *search* should keep expanding from such a state is a different
  question, answerable only relative to what future violation events
  that case can still produce. C3 is the first case where the two
  diverge sharply enough to matter. **Not generalized further than
  that:** search terminality must be defined relative to the future
  violation events a case can still produce, not copied mechanically
  from world action availability -- and not fixed as "always treat
  `CLAIMED` as search-terminal" either, since a future case with
  downstream/interacting events (a `claim` feeding a later `consume`,
  for instance) could make post-claim states matter again. This is a
  distinction to keep making per-case, not a policy to bake in now.
- **Independent monitor reference, permanent negative control, and
  post-claim mutation regression** all required again, unchanged as a
  standing QA requirement.
- **Diagnosing an integration failure is now a demonstrated pattern, not
  just a rule.** `ecbd536`/`e3bdfeb` did what `SEARCH_CONTRACT_C1.md`'s
  interpretation rule always implied but never had to prove: a frozen
  search policy can genuinely fail on a new case, the failure can be
  root-caused with an isolated single-variable intervention instead of
  parameter retuning, and the official sealed result stays exactly what
  it was.

## 6. What C4 must actually test (open question, not a decision)

C3's own open question from `RESULTS_C2.md` -- does the architecture
survive multiple interacting violation-event types, as opposed to a
single event fed by chained provenance -- is unchanged and still open;
C3 deliberately tested the provenance-chain axis, not the
interacting-events axis (`DESIGN_C3.md`'s brainstorming record).

Section 4.2/4.3 adds a second, narrower thread worth carrying into
whatever C4's search contract turns out to need: if C4 introduces an
event downstream of `claim` (something like `consume`, whose legitimacy
depends on `claim` having been legitimate), post-claim states stop being
safely treatable as dead weight for search purposes -- exactly the
"search terminality is relative to future violation events" lesson from
Section 5, now with a concrete future case that would make it bite. This
is not a decision to add such an event; it is a note that if C4 does, the
score-only-greedy Beam policy this project has reused unmodified since
C1 should not be assumed safe by default there either.
