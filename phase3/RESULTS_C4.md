# C4 Results (sealed)

Consolidates what `DESIGN_C4.md` (plan, through C4b), `verify_c4.py`
(core QA), `SEARCH_CONTRACT_C4.md` (search contract), `2a10826`'s
official search integration run, and `ee25b0a`'s post-hoc diagnostic
each separately established. C4 is closed as of this document -- and
with it, Phase 3's synthetic-case sequence.

## 1. Question / planted mechanism

**C2's base, unchanged, plus one new downstream event.** `claim()`'s
precondition-check is byte-for-byte C2c -- still the single planted
fault (presence as a proxy for validity). What C4 adds: `claim` now
also grants `reward_owned = True` unconditionally, *after* that check,
so it cannot influence the check's own inputs; and a new action
`consume` (legal iff `reward_owned == True`, WorldState-only, never
illegal because of taint) whose *legitimacy* depends on whether the
reward it consumes came from a tainted claim.

`EventProvenanceState.reward_provenance_tainted` is a boolean freeze of
the `claim` event's own verdict, captured at the instant `claim` fires
(`tainted = claim_verdict is not None`). `claim` can occur at most once
(`quest_status` never reverts from `CLAIMED`), so `consume` can too --
no reset semantics exist or are needed.

Shortest witnesses, proven not merely asserted (Section 4.1):
legitimate consume 5 actions; `TAINTED_REWARD_CONSUMPTION` 7 actions.

## 2. RQ-A1 -- Representation (the central result)

**`WorldState` / `MonitorState` / transition-local violation judgment
was not sufficient once a later event's judgment depends on an earlier
event's verdict. That verdict had to acquire persistent state of its
own.**

Stated precisely, since the weaker and stronger versions of this claim
are easy to confuse: the three-component architecture C1-C3 built did
not *fail* -- `WorldState` and `MonitorState` are unchanged from C2c
and still correct, and violation judgment is still transition-local
(C2c's own result, reconfirmed). What broke is the implicit assumption
that a violation verdict, once computed and reported, can be *discarded*
-- that nothing downstream will ever need it again. C4 is the first
case where something does.

|  | theoretical | reachable | transitions | layers |
|---|---|---|---|---|
| C1 | 12 | 9 | 13 | 7 |
| C2 | 48 | 19 | 40 | 8 |
| C3 | 192 | 62 | 174 | 11 |
| C4 | 192 | 31 | 69 | 9 |

(C3 and C4 have identically-sized theoretical spaces -- 24 `WorldState`
combinations x 8 spec-state combinations in both, arriving there by
different routes: C3 via a third monitor bit, C4 via a fourth
`WorldState` field plus a provenance bit. C4's reachable count is lower
than C3's, consistent with `reward_owned` being gated behind the
one-shot `claim`/`consume` lifecycle while C3's `enchanted` dimension is
directly manipulable from the start -- but the exact 31-vs-62 ratio is
descriptive, not attributed to a single cause: C3 and C4 differ in
their whole mechanism, not just that one field's gating. Not a
scalability regression, and not a like-for-like difficulty comparison
either.)

`monitor_step` and `event_provenance_step` matched their independent
full-history references on all 69 transitions, and both oracles matched
theirs -- four separate comparisons, four separate mismatch counters,
0 mismatches on each (Section 3).

**Why a persistent verdict is necessary, proven by a bidirectional
constructive pair, not inferred from the implementation:**

```text
Witness P:  equip(Flame), accept, channel, claim, equip(Wood), consume
Witness Q:  equip(Flame), channel, equip(Wood), equip(Flame), accept, claim, channel, consume
```

Both are legal histories, both confirmed by `verify_c4.py` as dedicated,
individually-reported checks. In **P**, the `claim` is legitimate
(frozen `reward_provenance_tainted = False`), but the post-claim
`equip(Wood)` -- entirely ordinary, already-established C2 behavior --
sets ambient `buff_source_broken = True` anyway. A `consume` oracle
reading ambient `MonitorState` calls this tainted: **a false positive**.
In **Q**, the `claim` is a genuine `BUFF_SOURCE_LIFECYCLE_VIOLATION`
(frozen `tainted = True`), but the post-claim `channel` unconditionally
resets ambient `buff_source_broken = False`. The same ambient-reading
oracle calls this clean: **a false negative**.

No re-derivation from present property state can get both right, because
the two histories' ambient states point the *opposite* way from their
actual claim verdicts. This is C2c's lesson ("ambient property state
answers a different question than a specific past event's verdict")
re-applied one hop downstream -- and this time the answer isn't "judge
at the transition" (C2c's fix) but "keep the judgment."

**Scope of this claim: one downstream hop, one boolean.** C4 shows a
verdict sometimes needs to persist -- it does not show how much of a
verdict needs to persist (C4 propagates one bit, deliberately not
`claim`'s three-way category), or whether a second hop
(`claim -> consume -> ???`) would need anything further. Both untested.

## 3. RQ-A2 -- Attribution / judgment

**C4 is the first case where the oracle itself, not just the monitor
fold beneath it, was checked against an independent reference.**
`reference_classify_claim` and `reference_classify_consume` re-derive
each verdict directly from reference property functions on the raw
history prefix -- neither calls `classify_claim`, `classify_consume`, or
`event_provenance_step`. This mattered because C4's actual research
content *is* downstream event judgment: verifying only the property
facts underneath it would have left the layer under test unverified.
Production matched on both, 0 mismatches across all 69 transitions.

**Negative control, two-directional -- stronger than C2's or C3's,
which only had to fail one way.** `known_bad_classify_consume` (reads
ambient `MonitorState` at consume-time instead of the frozen
provenance) produced `false_positive_count = 2` and
`false_negative_count = 1` through the identical closure sweep. The
sweep's own reported mismatch paths are literally Witness P's and
Witness Q's -- not merely similar cases, the exact two the design
predicted, confirming the closure genuinely generates them rather than
the witnesses being a separate hand-checked artifact.

C2's three claim-level categories
(`EQUIPMENT_CONTINUITY_VIOLATION`/`BUFF_SOURCE_LIFECYCLE_VIOLATION`/
`BOTH`) all still classify identically under C4's engine -- a
regression check that adding `reward_owned`/`consume` perturbed nothing
upstream, not new research content.

## 4. RQ-A3 -- Reproduction

### 4.1 Ground-truth reproduction -- PASS

Exhaustive `SearchState`-deduped search to depth 6 confirmed no shorter
history reaches `TAINTED_REWARD_CONSUMPTION`; the sealed 7-action
witness does. The legitimate 5-action consume was confirmed reachable
as a sanity check that the case can be completed honestly.

### 4.2 Frozen search integration -- FAIL

```text
Random        10/10 seeds
Beam-Naive    no discovery
Beam-Diverse  PASS -- cost 90
MCTS          10/10 seeds

C4 SEARCH INTEGRATION: FAIL
```

No parameter was retuned and no check relaxed after seeing this --
`2a10826` seals it exactly as the first and only official run produced
it. As in C3: **the failure does not invalidate 4.1's
existence/minimality result; it shows that one of the four frozen
search policies failed to recover an already-proven executable
witness.** 31 reachable states is far too small for a performance
verdict, so no ranking is reported -- including the fact that
Beam-Diverse succeeded where Beam-Naive did not, which is an
integration observation, not evidence about novelty search.

### 4.3 Post-hoc diagnostic -- tie-cutoff hypothesis supported, official result unchanged

A passive trace (`ee25b0a`, Part 1 -- observation only, using the
official `score()` and stable-sort ordering unmodified) located the
exact drop. The sealed 6-action tainted-claim prefix
`equip(Flame), accept, equip(Wood), equip(Flame), channel, claim`
is generated correctly and selected into the beam at *every* layer
while still `ACTIVE` (prefix lengths 1-5). At layer 6 -- the instant it
reaches `CLAIMED` -- it ties in score (both = 2) with five
independently-arrived clean-claim candidates reaching `CLAIMED` that
same layer, and under deterministic stable-sort tie-breaking lands at
0-indexed rank 5, i.e. the sixth candidate. `BEAM_WIDTH=5` cuts it
precisely at the cutoff, one position short, before its own downstream
`consume` can ever be expanded.

Primary causal test (Part 2): the **official, unmodified**
`beam_naive_search()` called with `beam_width=6` -- one more slot than
the cutoff, and nothing else changed (`score()`, candidate generation,
dedup, tie-ordering, `MAX_DEPTH`, `BUDGET` all identical). It found the
sealed 7-action witness at cost 61.

```text
                official (4.2)    diagnostic (beam_width=6)
Beam-Naive      no discovery      7-action witness, cost 61
```

**Tie-cutoff hypothesis supported: increasing only the beam capacity
from 5 to 6, exactly as the passive trace predicted, preserved the
sixth score-tied tainted `CLAIMED` candidate and restored downstream
discovery.** Restored *discovery*, not restored *PASS* -- `2a10826`'s
sealed result is unchanged. Not claimed: that `beam_width=6` is a
better parameter, that Beam-Naive is "fixed", or that this is the only
possible contributing cause.

An earlier attempt (scoring `CLAIMED` as 1, tied with `ACTIVE`, instead
of 2) also restored discovery at cost 52, but is kept only as a
**secondary sensitivity observation, explicitly demoted**: it merges the
`ACTIVE` and `CLAIMED` tie groups, reordering the combined tied set
under stable sort in a way not cleanly attributable to the cutoff
mechanism. The `beam_width=6` test isolates that mechanism without the
confound; this one does not.

### 4.4 C3 vs. C4 Beam failure -- same family, different mechanism

```text
C3 (ecbd536 / e3bdfeb):
  post-claim dead-end proliferation
  -> legitimately-CLAIMED states have no exploit-producing future,
     but keep generating high-scoring descendants
  -> those descendants displace every exploit-capable ACTIVE branch
  -> diagnostic fix: stop expanding CLAIMED states

C4 (2a10826 / ee25b0a):
  same-layer score-tie cutoff
  -> the target-relevant tainted CLAIMED candidate IS generated,
     correctly, at the expected layer
  -> it ties in score with clean CLAIMED candidates arriving the
     same layer, and lands sixth under deterministic tie ordering
  -> BEAM_WIDTH=5 cuts it exactly at the cutoff, before its own
     downstream consume can be expanded
  -> diagnostic fix: one more beam slot (and C3's fix would make
     things strictly worse here -- see Section 5)
```

Both belong to the same family -- a quest-status-only `score()` that
cannot see target semantics -- but the mechanisms are genuinely
different, and so are the interventions that address them. Neither is
evidence for a general claim about greedy search or about Beam.

## 5. Architecture and methodology decisions carried forward

- **Everything C1-C3 established still holds** -- presence is not
  validity; a `WorldState` no-op can be a `MonitorState` non-no-op;
  violations are transition-local, not state-local (C2c); monitor facts
  are not guaranteed component-wise-independently foldable (C3).
- **New: a violation verdict is not always ephemeral.** C1-C3 could
  compute a verdict, report it, and discard it. Once a later event's
  legitimacy depends on an earlier event's verdict, that verdict needs
  persistent state -- a third data bucket (`EventProvenanceState`),
  distinct from property state because it holds a *judgment about the
  past*, not a *fact about the present*.
- **Ordering constraint, stated at its actual strength.** Two
  requirements are genuinely load-bearing: `event_provenance_step` must
  run *after* the claim verdict it freezes exists, and
  `classify_consume` must read `prev_provenance` (the frozen
  pre-transition value), never `new_provenance`. C4 sealed a complete
  five-step call order in `SEARCH_CONTRACT_C4.md`, which is fine as a
  contract -- but only those two constraints are architecturally
  necessary; the rest of the order is a choice, not a derived result,
  and should not be reported as one.
- **New: a violation event is not necessarily a search-terminal
  discovery.** C1-C3's "any oracle firing ends the search" rule would
  make C4's target structurally undiscoverable -- a tainted `claim`
  would end the run before `consume` could ever happen. C4 seals
  discovery to `classify_consume` only, and `_step()` deliberately does
  not return `claim_verdict`, so the wrong check cannot be written by
  accident. Recorded as a distinction that must be made per-case, not a
  general rule that violations should never terminate search.
- **C3's caveat confirmed by a real case.** `RESULTS_C3.md` Section 5
  declined to generalize its `CLAIMED`-terminal diagnostic into policy,
  specifically because "a future case with downstream/interacting
  events... could make post-claim states matter again." C4 is that
  case: applying C3's fix here would prune the only paths that reach
  C4's target. `SEARCH_CONTRACT_C4.md` bans it explicitly. This is the
  clearest evidence so far that this project's refusal to generalize
  from single cases has been load-bearing, not just cautious.
- **Independent references now extend to the oracle layer** (Section 3),
  not just monitor folds -- required whenever the case's research
  content lives in the judgment layer itself.
- **Diagnosing an integration failure is now an established two-step
  pattern**: passive trace first (observation only, no behavior change,
  to locate the exact failure point), then a single-variable
  intervention chosen *because the trace predicted it* -- not a
  parameter sweep, and not the first intervention that happens to work.
  C4's demotion of the `CLAIMED=1` result in favor of the `width=6`
  test is the first time this project explicitly ranked two working
  interventions by how cleanly each isolates the mechanism.

## 6. What Phase 3.5 must actually test (open question, not a decision)

C1-C4 built an architecture -- `WorldState` / `MonitorState` /
transition-local violation judgment / persistent event provenance --
entirely against synthetic cases this project designed itself. Every
component was forced by a case built to force it. That is exactly the
right way to avoid speculative generalization, and exactly why the
result is now vulnerable to the opposite failure: **an architecture
that fits four cases the same author designed may be fitting the
author's own habits of mind rather than any property of game systems.**

The open question for Phase 3.5, stated as a question and deliberately
not answered here: **do these boundaries appear when the system under
test was defined by someone else?** Take a system this project did not
design -- a published game's documented rules, an existing rules engine,
an open-source game's actual mechanics -- and ask whether the same
separations are needed there, whether some are unnecessary, and whether
something C1-C4 never encountered turns out to be required. Anything
short of that leaves "this architecture is necessary" resting on four
cases with a common author, which is a weaker claim than the volume of
evidence makes it look.

No C5 in the C1-C4 mold. Phase 3's synthetic sequence is closed.
