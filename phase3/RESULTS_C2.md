# C2 Results (sealed)

Consolidates what `DESIGN_C2.md` (plan, through the C2c oracle
correction), `verify_c2.py` (core QA), `SEARCH_CONTRACT_C2.md` (search
contract), and `0025e55`'s integration run (search) each separately
established. C2 is closed as of this document -- no further tuning or
re-running.

## 1. Question / planted mechanism

**Single architectural fault, two lifecycles.** `claim()` treats
*presence* as a proxy for *validity*, for both conditions it checks:
`equipped == REQUIRED_EQUIPMENT` (current snapshot, ignoring whether
continuity held) and `has_flame_buff == True` (current presence,
ignoring whether the buff's source has stayed qualified since it was
last validated). The two properties this produces have different
recovery semantics -- `continuity_broken` is permanent-per-attempt, no
reset; `buff_source_broken` resets on `channel()` -- which is what makes
them genuinely non-redundant rather than two names for the same fact.

Shortest witnesses, proven not merely asserted (Section 4): legitimate
completion 4 actions; each of `EQUIPMENT_CONTINUITY_VIOLATION`,
`BUFF_SOURCE_LIFECYCLE_VIOLATION`, and `BOTH`, 6 actions.

## 2. RQ-A1 -- Representation

**The `WorldState`/`MonitorState` split survived a second, dependent
lifecycle -- but was not sufficient by itself, and that gap is C2's
central result.**

|  | theoretical states | reachable | transitions checked | layers |
|---|---|---|---|---|
| C1 | 12 | 9 | 13 | 7 |
| C2 | 48 | 19 | 40 | 8 |

(`verify_c2.py`'s own console output labels this comparison as
`(C1 comparison: 12, 13, 7)`, which reads ambiguously -- 12 is C1's
*theoretical* count, not reachable. The table above is the corrected
framing; it doesn't change any QA result, so the print string wasn't
worth reopening `6aab686` to fix.)

Both monitor facts were reachable in every divergent combination:
`(continuity=True, buff=False)`, `(continuity=False, buff=True)`, and
`(True, True)` are all reachable via legal history, which is
constructive evidence the two bits are non-redundant, not an assumption.
`monitor_step` matched the independent full-history reference on all 40
generated transitions with 0 mismatches.

**Where the split alone fell short:** Step 2's minimality check (not
Step 1's equivalence check) surfaced a real 5-action sequence,
`equip(Flame), accept, channel, claim, equip(Wood)`, where a
straightforward state-based oracle (`classify(world, monitor)`, askable
of any state at any time) misclassified an already-legitimate claim as
`BUFF_SOURCE_LIFECYCLE_VIOLATION` -- caused by an unrelated post-claim
equipment swap flipping `buff_source_broken` back to `True` after the
claim had already, correctly, succeeded. `continuity_broken` never
exposed this because its own trigger condition (`quest_status ==
"ACTIVE"`) structurally can't fire again once `quest_status` latches at
`CLAIMED`; C1 never had a second fact around to reveal that this was an
accidental protection, not a designed one.

A freeze-`MonitorState`-after-claim fix was considered and rejected --
it would make `monitor_step` lie about present buff validity, which
really does keep changing after a legitimate claim. The adopted fix
(`DESIGN_C2.md`'s C2c revision) makes the oracle judge the `claim`
*event* itself, using the monitor value from immediately before it
fires, rather than re-deriving an answer from whatever state happens to
be current. `MonitorState`/`monitor_step` were not changed.

**The architecture needed a third component, not a bigger version of the
first two:**

```text
C1:  world dynamics, property dynamics
C2:  world dynamics, property dynamics, violation events
```

Property dynamics stay current and Markov -- `monitor_step` never
stopped updating honestly. What changed is that a violation verdict is
now a judgment about a specific past transition, evaluated once, not a
predicate re-askable of an arbitrary present state.

**Scope of this claim: two dependent lifecycles, one event type
(`claim`).** Whether this event-local pattern still holds with multiple
distinct violation-event types, or a violation fed by more than one
provenance/source fact, is untested -- the open question Section 6
leaves for C3.

## 3. RQ-A2 -- Attribution

**Three-way, OR-based, honest attribution held up under construction.**
`classify_claim` reports `EQUIPMENT_CONTINUITY_VIOLATION`,
`BUFF_SOURCE_LIFECYCLE_VIOLATION`, or `BOTH` without ever requiring both
properties to manufacture a "needs both" result -- the earlier draft
that did was rejected during design, before any code existed.

Every witness each search algorithm found was independently replayed
from scratch and re-evaluated via the sealed `classify_claim()` at its
actual `claim` transition; every algorithm's recorded classification
matched. Precisely worded: this confirms each algorithm's own
bookkeeping against a fresh recomputation using the *same* sealed
oracle, not against a separately-implemented one -- that stronger
independence guarantee is Step 1's job (`monitor_step` vs.
`qa_reference.py`, 0 mismatches), already established in Section 2.

**Negative control, now a permanent regression test:** the production
monitor produced 0 mismatches against the independent reference;
`known_bad_monitor_step` (encoding "re-equipping alone revalidates the
buff") produced 7, run through the identical closure procedure --
concrete evidence the check is sensitive, not vacuously passing.

## 4. RQ-A3 -- Reproduction

Exhaustive `SearchState`-deduped search to depth 5 confirmed no
shorter-than-6-action `claim` transition reaches any of the three
violation categories; the legitimate 4-action completion was confirmed
reachable as a sanity check that the case isn't accidentally impossible
to complete honestly.

```text
Random:        10/10 seeds
Beam-Naive:    cost 38, EQUIPMENT_CONTINUITY_VIOLATION
Beam-Diverse:  cost 41, BOTH
MCTS:          10/10 seeds
```

**Integration observations only, no algorithm-performance conclusion.**
19 reachable states is bigger than C1's 9 but still far too small for a
cost or success-rate difference to carry information -- the same
interpretation rule as C1, sealed in advance in
`SEARCH_CONTRACT_C2.md` rather than decided after seeing these numbers.

## 5. Architecture and methodology decisions carried forward

- **Presence is not validity.** The planted fault itself, and --
  briefly, during design, before any code existed -- almost the oracle's
  own shape too (the rejected "both required" draft would have made the
  oracle presence-check its own two facts instead of reporting each
  honestly).
- **A `WorldState` no-op can be a `MonitorState` non-no-op.** `channel()`
  while `has_flame_buff` is already `True` changes nothing observable in
  `WorldState` but can still reset `buff_source_broken`. Engineering this
  away would have required `legal_actions()` to read `MonitorState`,
  which was rejected as a bigger violation than the cosmetic search-cost
  it would have fixed.
- **Property state is not the same thing as a violation verdict.** The
  central new result (Section 2): `buff_source_broken` staying current
  and honest is correct monitor behavior, but querying it at an
  arbitrary later point answers a different question than "was the
  claim legitimate when it happened."
- **A violation can be transition-local, not state-local.** C1's
  boundary implicitly assumed otherwise, by accident (its one fact
  happened to freeze itself post-claim) rather than by design. C2 is the
  first case to actually test that assumption, and the first to break
  it.
- **Independent monitor reference, permanent negative control, and
  post-claim mutation regression are now required QA components for any
  new case with a lifecycle-tracking property** -- not one-off diligence
  specific to C1 or C2.

The false positive itself is worth recording as a finding, not a
footnote: `verify_c2.py`'s Step 2 caught it before any commit, the fix
was designed and reviewed (rejecting the tempting freeze-based patch)
and sealed in `DESIGN_C2.md` (`071f397`) *before* `oracle.py` was
edited to match, and only then did the corrected core get committed
(`6aab686`) and re-verified. The QA methodology worked exactly as
intended -- it caught a real architectural gap that a purely
hand-reasoned design review had missed.

## 6. What C3 must actually test (open question, not a decision)

**C2 did not invalidate the `WorldState`/`MonitorState` separation; it
exposed that this separation alone was incomplete. Property dynamics can
remain current and Markov while violation judgments are event-local,
requiring a third boundary for violation events.**

The natural next pressure point, stated as a question and deliberately
*not* answered or designed here: does the `WorldState` / `MonitorState`
/ violation-event three-way boundary still hold once there is more than
one kind of violation event, or a single event whose legitimacy depends
on more than one upstream provenance/source fact? C2's own mechanism is
closed -- deciding C3's mechanism now, from what C2 happened to reveal,
would be exactly the "generalize from imagination instead of evidence"
mistake this project has avoided at every prior step.
