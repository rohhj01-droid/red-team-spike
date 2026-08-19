# C1 Results (sealed)

Consolidates what `DESIGN_C1.md` (plan), `verify_c1.py` (QA), and
`9ec6249`'s integration run (search) each separately established, before
that separation lets the plan and the proof drift apart. C1 is closed as
of this document -- no further tuning or re-running.

## 1. Question / planted mechanism

**Continuous Equipment Qualification.** A quest accepted while the
required equipment is worn stays claim-eligible only if that condition
holds continuously until claim; one violation, even briefly, is
permanent. The shipped (buggy) `claim()` only re-checks current
equipment, forgetting the history.

Shortest exploit, proven not asserted (Section 4): 5 actions --
`equip(Flame) -> accept -> equip(Wood) -> equip(Flame) -> claim`.

## 2. RQ-A1 -- Representation

**WorldState (`equipped`, `quest_status`) + a separate MonitorState
(`continuity_broken`) was sufficient.** The raw action-history space is
infinite (`equip(Flame) <-> equip(Wood)` toggles forever), but closure
over the semantic space `(WorldState, monitor value)` terminated at 9
reachable states out of 12 theoretically possible -- the 3 unreachable
ones (`NOT_ACCEPTED` with `continuity_broken=True` x2, `ACTIVE`+
`WoodenSword` with `continuity_broken=False`) are excluded by the action
semantics themselves, not by assumption. The incremental `monitor_step()`
was checked against an independently-written full-history reference on
every one of 13 transitions across 7 closure layers -- 0 mismatches. A
negative control (an injected non-monotonic bug) confirmed the check is
actually sensitive: it flagged exactly 4 mismatches at exactly the paths
where that bug mattered, not run against production code.

**Scope of this claim: evidence for C1, not a general result.** One
monotonic bit was sufficient here because C1 has exactly one lifecycle to
track. Whether a minimal-summary approach still works once a second
lifecycle (Buff, in C2) is added is untested.

## 3. RQ-A2 -- Attribution

**An explicit, domain-specific oracle (`quest_status == CLAIMED and
continuity_broken`) attributed the cross-system exploit directly** --
no Phase 0/1-style family-isolation-and-replay was needed, because the
oracle can name the interacting fields instead of inferring causation
from an aggregate signal like gold.

**Scope of this claim: evidence for this one mechanism.** Not "cross-
system attribution is solved" -- a different C2 mechanism with a
different attribution shape (e.g. one requiring reasoning about which of
several sources granted an effect) is a separate, untested case.

## 4. RQ-A3 -- Reproduction

Exhaustive search confirmed no state below depth 5 satisfies the oracle
(7 states visited to depth 4). The sealed 5-action witness is legal and
oracle-valid. All four algorithms found and correctly replayed a valid
witness:

```
Random:        10/10 seeds
Beam-Naive:    cost 13
Beam-Diverse:  cost 14
MCTS:          10/10 seeds
```

**These are integration observations, not comparative performance
evidence.** C1's 9-state space is too small for a cost or success-rate
difference between algorithms to carry information -- this is exactly
what `SEARCH_CONTRACT_C1.md`'s interpretation rule states and what
`run_c1_integration.py` enforces by never printing a ranked comparison.

## 5. Architecture decisions carried to C2

- **World dynamics and property-checking state can require different
  Markov closures.** The actual (buggy) engine's state was sufficient for
  legality/effects on its own; a separate, smaller monitor summary was
  what property-checking needed. Phase 2 never had to draw this
  distinction (gold+inventory served both purposes at once) -- C1 is the
  first case where they diverged.
- **Monitor-derived state is required for dedup/reward, forbidden for
  guidance.** Beam's dedup key and MCTS's reward need full `SearchState`;
  `score()`/`behavior_descriptor()`/policy selection must never receive a
  `MonitorState` argument at all -- enforced by the function signatures
  themselves in C1, not by convention.
- **Independent reference + exhaustive equivalence QA is now a required
  step for any new monitor-style property**, not a one-off for C1.
  Enumerate by semantic closure, not an arbitrary depth bound, when the
  raw action-history space is infinite.
- **C2 onward: the negative control becomes a permanent regression test**
  in the QA suite (a fixed "known-bad monitor must fail equivalence"
  case), not a throwaway process re-run by hand each time.
- **Exhaustive QA scalability has a first data point, not yet a trend.**
  C1: 9 semantic states, 13 transitions, 7 closure layers, all in well
  under a second. C2 (adding Buff) is the second point -- worth recording
  the same numbers there specifically to see how they grow.
- **No generic cross-system framework yet.** Two data points (C1, then
  C2) is still not "evidence," per the project's standing rule against
  generalizing from imagination.

## What C2 must actually test

Not "add a Buff system" -- **does the WorldState/MonitorState boundary
that worked for C1's single lifecycle (equipment continuity) still hold
once a second, dependent lifecycle (a Buff whose validity depends on its
granting Equipment) is layered on top?** C1 proved the boundary works for
one temporal property. C2 is the first test of whether it survives a
second, causally-linked one -- that comparison, not the Buff mechanic
itself, is the actual research content of C2.
