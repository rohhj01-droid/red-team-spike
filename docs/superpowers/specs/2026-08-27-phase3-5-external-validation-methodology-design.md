# Phase 3.5 External-Validation Methodology Design

**Status:** pre-target methodology design. This document defines how Phase 3.5 will select, analyze, classify, and report one external system before any target-specific architectural conclusion is allowed. It does **not** select a target, enumerate target properties, inspect a target's known bugs, or authorize implementation/search work.

**Purpose:** break the self-validation loop left by Phase 3's four synthetic cases. C1-C4 were intentionally designed by this project to force specific representation pressures; Phase 3.5 asks what happens when the rules, native state representation, and implementation boundaries were designed by someone else.

**Phase 3 carry-in:** the synthetic architecture under examination is:

```text
WorldState
MonitorState
transition-local violation judgment
persistent event provenance
```

Phase 3.5 does not assume those four roles are necessary, sufficient, or naturally separated in an external system.

---

## 1. Methodological success, not directional success

Phase 3.5 is successful if the protocol is followed, regardless of whether the external evidence retains, collapses, extends, contradicts, or underdetermines the Phase 3 architecture.

Success requires all three:

1. **Pre-registration:** before architectural analysis of the selected target, define what external evidence would support retention, F0, F1, F2, and F3; freeze the primary observation universe and the evidence-sufficiency rules.
2. **Native-first analysis:** describe the external system in its own terms before translating it into `WorldState` / `MonitorState` / judgment / provenance language.
3. **Outcome preservation:** report the observed result exactly as produced. A FAIL, counterexample, underdetermined result, or evidence-insufficient result is not retroactively repaired into a favorable conclusion.

This follows the same discipline used earlier when a frozen search policy failed in C3/C4: methodological validity is not defined by whether the result points in a preferred direction.

---

## 2. Eligibility: one strong external target, not a survey

Phase 3.5 is a single-target external-validation case, not a population survey. Candidate scarcity is acceptable if it buys cleaner falsification.

A candidate must satisfy all of the following.

### E1 — External authorship

The system's rules and native implementation boundaries must not have been designed by this project. Re-implementing an external ruleset in a new simulator authored by this project does not satisfy the representation part of externality.

### E2 — Evidence is split into RULE and REP

#### E2-RULE — rule/validity evidence

The target must expose externally authored evidence sufficient to determine at least one validity requirement without inventing the requirement ourselves. Examples include project-owned canonical rules, documentation, tests that explicitly state expected validity, or equivalent authoritative artifacts.

#### E2-REP — native representation evidence

The primary F3 test requires access to the **actual native state representation and information flow**, not merely the rules. Source code is required for the primary target because F3 is about ownership/lifetime/write-read boundaries. Save formats, schemas, official internal-architecture documents, and black-box persistence probes may strengthen the evidence but do not independently establish F3.

Evidence roles are deliberately non-flat:

| Evidence | What it can establish well | F1 value | F3 value |
|---|---|---:|---:|
| source code | fields + writers/readers + lifetime + consumption path | strong | strong |
| save format / DB schema | persistent field inventory | strong | weak alone |
| official internal-structure docs | intended organization | medium | medium; intent != implementation |
| black-box behavior/persistence probes | indirect persistence facts | weak/supporting | very weak alone |

### E3 — Architecture-neutral validity eligibility

At least one validity observation must be externally enumerable without requiring the project to first decide that the system contains a lifecycle, provenance chain, cross-system interaction, or any other Phase 3-shaped mechanism.

The admission condition is intentionally weak: the external source must expose a stateful/temporal validity question that can be examined. Whether multiple lifecycles exist or interact is a result, not an entrance requirement.

### E4 — Neutral primary-universe construction

The target must permit a **property-level primary universe** to be determined by external/mechanical rules rather than by researcher interest. A subsystem list such as `Quest / Inventory / Equipment` is not enough if the actual validity observations inside those subsystems would still be hand-picked.

If no externally determined, mechanically enumerable primary observation universe can be constructed at the required granularity, the candidate is rejected as the Phase 3.5 primary target.

### E5 — Bounded exhaustive analysis

E2-REP and E5 form a joint practical constraint. It is not enough that source code exists; the entire frozen primary universe must be small/local enough that its native information flows can be traced to the evidence-sufficiency gate without sampling or optional stopping.

A huge open-source system whose relevant state is spread across an unbounded implementation surface can pass E2-REP but fail E5.

### Selecting among multiple eligible candidates

E1-E5 are pass/fail admission gates, not a ranking. If more than one candidate is eligible, the choice must not fall to researcher interest — otherwise target-selection bias simply replaces the slice-selection bias E4 exists to prevent, one step earlier.

Ranking uses exactly two steps, in this fixed order, both fully decidable from screening-level evidence:

1. **Enumeration completeness class**, a binary class, not a score:

```text
class A: at least one enforcement enumerator is admitted
         AND every admitted enforcement enumerator is `enforced`

class B: otherwise
         (any admitted enumerator is `asserted`,
          OR no enforcement enumerator is admitted at all)

class A outranks class B; within a class this criterion is a tie.
```

   The threshold is binary because Section 3.3's absence rule is binary: a single `asserted` enumerator already weakens every absence claim, regardless of how many `enforced` ones accompany it. No ratio or count-based refinement is introduced, precisely so that a case like `2 enforced / 0 asserted` versus `20 enforced / 1 asserted` is decided by a rule fixed now rather than by a comparison invented after seeing the candidates.

   Class A's first conjunct is not redundant. A candidate may satisfy E4 from `U_normative` alone and admit **no** enforcement enumerator; "every admitted enumerator is `enforced`" would then be vacuously true over the empty set and would promote a normative-only candidate to class A, which is the opposite of the intent. A normative-only candidate has no complete-by-construction enforcement evidence at all, so it belongs in class B alongside `asserted` candidates, and the choice between them falls to the tie-break rather than to a new discretionary comparison.

2. **Deterministic tie-break, sealed here rather than by example.** Order the tied candidates by their **normalized canonical repository URL**, ascending, comparing the byte sequences of its UTF-8 encoding; select the first.

```text
normalized canonical repository URL =
  the HTTPS form of the primary source repository that the
  external project itself designates, with:
    scheme and host lowercased
    no credentials, query, or fragment
    no trailing slash
    no trailing ".git"
```

   A candidate with no project-designated source repository cannot have satisfied E2-REP and is therefore not eligible in the first place, so this ordering is total over the eligible set. The rule is fixed at seal time precisely because choosing between ascending and descending, or between repository name and URL, after seeing the candidate list would itself be a selection.

**No traceability ranking step is used.** An earlier draft ranked eligible candidates by how directly their evidence supported tracing every unit. That is dropped for two reasons: it was qualitative and never operationalized, and judging it would require inspecting candidate implementations more deeply than the candidate-screening firewall permits — the ranking step would itself breach the firewall it sits behind. E5 already gates exhaustive traceability as pass/fail; among candidates that pass it, no further traceability comparison is made.

**`P_raw` size is excluded as a ranking criterion in both directions.** A small universe is easier to analyze but offers fewer chances to observe a counterexample; a large universe makes `U == 0` nearly unreachable and therefore makes an absence claim easy to avoid committing to. Either direction lets a preference about the result enter target selection.

Every screened candidate is recorded, including rejected ones, with the specific eligibility criterion failed or the ranking step lost. A record showing only the selected target hides how many candidates were screened and whether near-misses were rejected on soft grounds.

### Candidate-screening firewall

Before a target is frozen, screening may inspect only what is necessary to determine E1-E5 and the existence/admissibility of enumeration mechanisms. Screening must not inspect known-bug root causes, fix diffs, or use interesting-looking validity behavior to hand-pick the target's primary slices.

Target candidates are evaluated only after this methodology document is sealed.

---

## 3. Primary observation universe

The primary universe is defined at the source-observation level, not by researcher-inferred semantic properties.

```text
U_primary = U_normative ∪ U_enforced
```

Known bugs do not contribute to `U_primary`.

### 3.1 U_normative — externally stated validity observations

`U_normative` contains atomic observations emitted by project-owned or project-designated authoritative rule sources that explicitly state validity requirements.

Source selection rules:

- Prefer the external project's own self-designated canonical/authoritative source.
- If multiple admissible canonical sources exist, take their union rather than choosing the cleaner or smaller one.
- A third-party wiki does not become authoritative merely because it is convenient; it must be designated by the external project or otherwise satisfy the target-specific authority rule frozen before analysis.

### 3.2 U_enforced — mechanically enumerable enforcement observations

`U_enforced` may be generated only by external enforcement enumerators that satisfy **all** EN1-EN6.

#### EN1 — external authorship

The mechanism/convention existed independently of this analysis.

#### EN2 — explicit scope

The external project identifies what enforcement domain the mechanism enumerates, e.g. quest eligibility conditions, effect requirements, transfer guards.

#### EN3 — mechanical membership

Membership can be decided without semantic reading of individual items. Examples: all entries in a registry, all implementations of a declared interface, all collected annotations/decorators, or all items in an externally declared closed directory convention.

#### EN4 — enforcement meaning

The external project itself connects the mechanism to validation, eligibility, rule enforcement, or an equivalent validity role. A directory merely named `validators/` or functions that happen to look like `validate_*` are not sufficient if that meaning is inferred by us.

#### EN5 — closed within scope

Within the enumerator's declared scope, the project gives a closure basis strong enough that researchers do not choose which members count. `All quest conditions implement QuestCondition` can qualify; `validators are usually under /validation` cannot.

A policy statement such as `all quest conditions should implement QuestCondition` is also insufficient: it states what contributors ought to do, not that the current codebase is closed by that rule.

#### EN6 — outcome independence

Membership must not be defined by known failure. A bug/exploit label, fix list, or `things that broke` registry cannot define the primary enforcement universe.

### 3.3 Enumerator completeness tag

Every admitted enforcement enumerator receives one of two evidence-quality tags:

- **`enforced` — complete by construction:** runtime dispatch/collection itself uses the list (registry, interface dispatch, annotation collection, etc.). The enumerated set is the mechanism's operational membership.
- **`asserted` — complete by assertion:** an external current-state statement claims closure, but runtime structure does not make omission impossible. The assertion may be stale or violated by later contributors.

`asserted` enumerators are allowed because a real counterexample found inside an incomplete list remains a real counterexample. But they weaken any absence/retention claim: if any primary enumerator is `asserted`, absence statements must be scoped to **the range the external project asserted to be complete**, never upgraded to a claim about the entire implementation.

This asymmetry is intentional: enumeration incompleteness threatens absence claims much more than existence claims.

### 3.4 Union, provenance, and no convenient enumerator choice

If multiple enumerators satisfy EN1-EN6, include the union of all of them. Do not select the one with the cleanest structure or smallest list.

Every **source observation** retains its own source provenance — normative source ID or enforcement enumerator ID, plus that enumerator's `enforced/asserted` tag — including when it sits inside an externally-linked counting unit alongside others.

---

## 4. Atomicity and crosswalk rules

### 4.1 Atomicity: use the source's own segmentation

Two levels must be distinguished, because Section 4.2's externally-linked exception makes them come apart:

```text
Source observation
= one atomic item, as the external source itself segmented it

Primary slice (= primary counting unit)
= normally exactly one source observation
= but one linked unit holding several source observations where the
  external project explicitly cross-links them (Section 4.2)

P_raw = number of preregistered primary counting units
```

**The sufficiency gate, `E?`, and coverage all apply at the counting-unit level.** Inside a linked unit, both source observations are retained and their agreement or divergence is reported as a finding of that unit; recovering the unit's native information flow may draw on the evidence attached to any of its observations.

Atomicity of the source observations themselves is never inferred semantically by this project. Each source is segmented at the finest level that the source itself explicitly exposes.

- A numbered rule item is one normative source observation if the source exposes it as one item.
- If that item says `A AND B AND C`, it remains one source observation unless the source itself subdivides A/B/C.
- One mechanically enumerated enforcement item is one enforcement source observation, even if later analysis shows that it checks several semantic conditions.
- If a normative source is an undifferentiated prose blob with no mechanically usable segmentation, that source is not admissible as a primary-universe source; researchers do not rescue it by manually splitting it.

Why: deciding whether `A` and `B` are semantically separable requires understanding their meaning and information flows, which is part of the analysis. Universe construction must precede that analysis.

The resulting `P_raw` inherits the external source's editorial granularity. This is accepted. Coverage is an internal transparency measure for this one target, not a cross-target quality score.

### 4.2 No analyst-inferred crosswalk before analysis

Normative and enforcement observations are **not deduplicated** because determining whether a rule sentence and a code validator express the same property usually requires the analysis we are trying to perform.

An exception is allowed only when the external project itself explicitly asserts the correspondence, e.g. a validator cites a rule ID, a test names the exact rule clause, or another project-owned artifact links them.

**When such an external link exists, merge the counting unit but not the observations.** The linked source observations form **one** externally-linked primary counting unit (Section 4.1), while **both source observations are retained inside it**. The external project's link asserts that the two concern the same rule; it does not assert that their contents agree. Collapsing the observations as well as the count would erase exactly the `divergent` relationship of Section 4.3 — a documented rule stating `X` while the linked validator checks `X'`. The objection that justified refusing analyst-inferred crosswalk (our judgment entering universe construction) is resolved by the external link; the separate objection (losing the divergence observation) is not, and must be handled separately.

**Grouping when links are not pairwise.** External cross-links need not come in isolated pairs: a project may link `N1↔E1` and `N1↔E2`, or `N1↔E1` and `E1↔N2`. Leaving the grouping to analyst judgment would put `P_raw` back under our control, so it is fixed mechanically:

```text
Treat every externally declared cross-link as an undirected edge
between source observations. Each connected component of the
resulting graph is exactly one externally-linked primary counting
unit.
```

This decides pairwise, one-to-many, and chained/many-to-many cases identically and without discretion. All source observations in a component are retained inside its unit, and divergence among any of them remains reportable as a finding of that unit.

Otherwise, with no external link:

```text
N7 and E12 remain two source observations and two separate counting units
```

even if they later turn out to describe one native information-flow case.

### 4.3 Correspondence is a post-analysis result

After analysis, report correspondence without rewriting the original denominator. Possible relationships include:

```text
matched
normative-only
enforcement-only
divergent
externally-linked
analyst-inferred correspondence
one-to-many / many-to-one
```

`normative-only` is not automatically an implementation bug, and `enforcement-only` is not automatically a documentation defect. Alternative explanations must remain open (stale docs, structural enforcement outside an explicit validator, incomplete enumeration, etc.).

---

## 5. Counting, coverage, and the three analysis levels

### 5.1 Raw coverage accounting

Let:

```text
P_raw      = number of preregistered primary counting units (Section 4.1)
P_resolved = counting units that pass the evidence-sufficiency gate
U          = counting units classified E? (evidence insufficient)

P_raw = P_resolved + U
coverage = P_resolved / P_raw

O_raw      = number of underlying source observations (descriptive only,
             never a coverage denominator; differs from P_raw only where
             externally-linked units exist)
```

An externally-linked primary counting unit (Section 4.2) contributes **1** to `P_raw` while carrying its retained source observations inside it. Those observations are reported individually within the unit, and their agreement or divergence is a finding of that unit, not a change to the denominator. Sufficiency and `E?` are judged for the unit as a whole, not separately per contained observation.

Coverage must always be reported with its denominator. `E?` is never silently dropped.

Post-analysis, also report a separate correspondence-collapsed count:

```text
C = number of distinct native information-flow / architectural cases
```

`C` never replaces `P_raw` as the coverage denominator because correspondence is learned after analysis.

If two counting units later map to the same native case, report both:

```text
counting units classified F3 = 2
distinct F3 architectural cases = 1
```

No prevalence inference is permitted from either count.

### 5.2 Three levels must remain separate

```text
1. Primary slice (= primary counting unit)
   normally one source observation;
   an externally-linked unit may contain several source observations
   the unit at which sufficiency, E?, and coverage are judged

2. Native information-flow case
   recovered from evidence after analysis
   multiple counting units may converge here

3. Architectural classification
   R0 / F0 / F1 / F2 / F3
   applied only after evidence sufficiency
```

`E?` means level 1 could not be carried reliably into level 2. It is not an architectural class.

---

## 6. Evidence-sufficiency gate

Architectural classification is allowed only after the native information flow for the slice is recoverable with enough evidence to answer, in native terminology:

1. What value/fact is created?
2. Where is it written or updated?
3. What is its lifetime/persistence behavior?
4. Which transitions/components read or consume it?
5. Does it persist after consumption, reset, migrate to another owner, or disappear?

Module/file boundaries are not architectural evidence by themselves. A 3,000-line God class may still contain a clear information-flow boundary; a beautifully separated directory tree may not.

### 6.0 Sufficiency must be evidenced, not asserted

The sufficiency gate is the only thing separating `E?` from a resolved case, and `E?` is expensive: it blocks absence claims (Section 8.4) while producing no architectural finding of its own. That creates a standing incentive to declare sufficiency too readily — the one judgment in this protocol with a built-in directional pull and, as originally written, no constraint on it.

Therefore each resolved counting unit must record, for each of questions 1-5 above, the **specific located native evidence** answering it (file/symbol/schema/document reference).

Inference is not the thing being banned. Reading that one function sets a flag and another reads it, and concluding that the flag's lifetime spans those two transitions, is inference — and essentially all source-level analysis is of that kind. What is banned is inference that cannot be traced back to located evidence:

```text
located evidence + stated reasoning connecting it to the answer
    → question satisfied

answer asserted without identifiable evidence behind it
    → gap
```

A question may also be satisfied by an **evidenced `N/A`**. If a validity check is recomputed on the spot and creates no persistent fact, then question 3 (lifetime/persistence) is legitimately answered `N/A: no persistent value is created`, with the specific code path cited. An unsupported `N/A` is a gap exactly as an unsupported answer is.

```text
located answer, or evidenced N/A   → sufficiency question satisfied
unsupported answer, or bare N/A    → gap → unit recorded E?
```

An `E?` names the specific question(s) left as gaps. This makes sufficiency a checklist with citations rather than an overall impression, and makes the cost of an `E?` fall on evidence that is genuinely missing rather than on the analyst's willingness to call it missing.

### 6.1 E? — evidence insufficient, outside the taxonomy

If the required information flow cannot be recovered reliably, record `E?`.

Every `E?` must include:

- the specific missing/unrecoverable evidence,
- why recovery failed,
- whether the failure is due to opacity/engineering structure/tooling versus a possible unmodeled structure,
- an explicit re-check against F2.

The key distinction:

```text
E? = we could not observe/recover enough to describe the native structure
F2 = we did observe the needed native structure, and the frozen architecture has no place for it
```

`E?` is a claim about our observation; F0/F1/F2/F3/R0 are claims about the system.

### 6.2 Absence of an identifiable boundary is not F3

F3 requires **positive evidence for an alternative native boundary**, not merely failure to observe ours.

Use this decision logic after sufficiency:

```text
flow not recoverable reliably
→ E?

flow recoverable, but evidence privileges no decomposition
→ F0

flow recoverable, and a separate Phase-3 component responsibility is unnecessary
→ F1

flow recoverable, but a required structure/information role has no place in the four-role architecture
→ F2

flow recoverable, the responsibility exists, but ownership/lifetime/write-read boundaries
are positively supported in a way inconsistent with ours
→ F3
```

---

## 7. Architectural outcome taxonomy

### R0 — retained within this case

Native evidence supports the Phase 3 role/boundary under examination, or rules out the relevant simpler/alternative representation strongly enough that the role remains needed for this case.

R0 is corroboration from one external case, never proof of general necessity.

### F0 — underdetermined

The native flow is sufficiently observed, but competing representations fit equally well and the system itself does not privilege one decomposition.

F0 is **not** evidence insufficiency. It means we looked successfully and the system does not identify the boundary question.

The allowed claim is target-local: this slice does not establish that the Phase 3 boundary is necessary. Do not automatically upgrade one F0 result into a universal statement that the architecture is case-dependent.

### F1 — component collapse

The native system represents the relevant information/behavior without needing one of the Phase 3 roles as a distinct conceptual responsibility. Example shape: provenance that is naturally part of an item/reward instance's ordinary domain state rather than a separate persistent event-provenance component.

### F2 — missing component / missing structure

The native system requires information or structure that the four-role architecture cannot faithfully place or express. Potential examples might include multi-actor concurrency, non-boolean validity state, partial observability, or other structures, but no such example is assumed in advance.

### F3 — wrong boundary placement

The relevant responsibility exists, but recoverable native information flow positively supports a different ownership/lifetime/update/consumption boundary than the Phase 3 partition.

F3 is about information flow, not folder/module cleanliness.

---

## 8. Interpretation rules

### 8.1 Directional asymmetry is logical, not statistical

Existence and absence claims have different burdens:

```text
one valid F1/F2/F3 witness
→ sufficient to establish that counterexample exists

no F1/F2/F3 in the preregistered set
→ requires every primary slice to be resolved before an absence statement
```

No global `E?` percentage threshold is used.

### 8.2 Mandatory coverage reporting

Every results summary must state:

```text
resolved / P_raw
E? / P_raw
```

and list E? slices with reasons in the main results, not only an appendix.

Every architectural claim must be scoped to the evidence actually resolved, e.g. `among the X/Y preregistered primary counting units whose native information flow was recoverable...`.

### 8.3 Counterexample found

If any primary slice passes sufficiency and yields F1/F2/F3, the counterexample remains informative regardless of how many other slices are E?. However:

- continue analyzing **all** preregistered primary slices,
- do not infer prevalence,
- report the full distribution and coverage,
- never stop early because the existence claim has already been established.

### 8.4 No counterexample found

If no F1/F2/F3 appears:

- `U == 0`: report only that **no counterexample was observed in all preregistered primary slices of this target**. This is not universal confirmation.
- `U > 0`: the primary external-validation question is **INCONCLUSIVE** with respect to absence/retention because unresolved slices prevent an absence claim.

If any admitted universe enumerator is tagged `asserted`, even the `U == 0` absence wording must be weakened to the externally asserted enumeration scope. Do not claim the list was implementation-complete by construction.

### 8.5 The protocol is intentionally hard on clean absence

With source-segmented primary counting units, `U == 0` may be difficult or rare. This cost is accepted **before** seeing target results. It must not later be used as justification to loosen the sufficiency gate, group slices post hoc, change the denominator, or reduce the primary set.

### 8.6 No optional stopping and no denominator drift

Every preregistered primary slice is analyzed even after a counterexample is found.

Exploratory validity observations discovered during analysis may be reported separately, but they:

- are not retroactively added to `P_raw`,
- do not change the conclusiveness rule for the frozen primary set,
- are clearly labeled exploratory.

The primary universe determines **what must be analyzed**, not what evidence may be inspected. Tracing a primary slice may follow any relevant native code/data path, including code outside the enumerator's original location.

---

## 9. Primary-lane frozen artifacts

Before the known-failure challenge lane is opened, the primary lane must freeze three separate artifacts. They must be reported separately because their failure implications differ.

### Artifact 1 — Native description

For every resolved native case, record in external/native terminology:

```text
source observation IDs
native state/data involved
writers / creation points
updates / invalidation paths
readers / consumption points
lifetime / persistence / reset behavior
relevant transitions
supporting source-code/docs evidence
remaining native-level uncertainty
```

This artifact must not start by assigning Phase 3 names to fields.

### Artifact 2 — Architectural mapping

Only after Artifact 1 is written, map native roles to the Phase 3 architecture, including explicit `no clean mapping` where appropriate.

Record the reasoning for each role assignment and the architectural outcome it supports. This mapping is the main contamination surface for the known-failure lane and therefore must be frozen before any known-bug symptom is revealed.

### Artifact 3 — Derived judgment specification

From the frozen native description + mapping + external validity evidence, write the judgment definition that would classify a relevant transition/history as valid or invalid.

This is a specification, not an executable simulator. It must state enough to determine a verdict on a described history/event without consulting future known-bug root-cause information.

**Artifact 3 freezes two things, and must be total within the first:**

```text
1. Applicability domain
   which transitions/histories this judgment claims to decide,
   bounded by what the external validity evidence actually covers

2. Decision procedure
   total within that domain: every case inside it receives a
   determinate verdict, including verdicts that may prove wrong
```

Both are frozen together, before any known-bug symptom is revealed.

**Domain inclusion is not discretionary.** Freezing the domain before seeing any bug removes post-hoc bias, but an *ex ante* discretion would remain if we could simply declare a narrow domain and later route every inconvenient challenge item to `out-of-domain`. The inclusion rule is therefore mechanical:

```text
frozen external validity evidence supplies a verdict for the case
    → the case MUST be inside the applicability domain

frozen external validity evidence does not define the case's validity
    → the case may be outside it
```

Analyst convenience, expected difficulty, or a guess about what the challenge lane will contain is never a valid ground for exclusion. The only admissible ground is that the frozen external evidence itself does not determine that case.

Freezing the domain first is what keeps the totality requirement honest in **both** directions. A specification vague enough to return `indeterminate` on everything is an escape hatch, not a neutral outcome — it can never be `DISCORDANT` (Section 11.2.2), so the challenge lane can never falsify it. But a requirement to return a verdict on *every* case would be equally wrong in the other direction: where the external validity evidence defines no judgment, forcing one means **inventing an external rule** and then testing our own invention, which is the self-validation failure this whole phase exists to break.

Consequently `not applicable` and `indeterminate` are **different results and must not be reported as one bucket**:

```text
case outside the frozen applicability domain
→ scope mismatch / N/A; not a defect of Artifact 3

case inside the domain but no determinate verdict
→ Artifact 3 limitation (the procedure was not total where it claimed to be)
```

A high rate of in-domain `indeterminate` is reported as a limitation of Artifact 3. A high rate of out-of-domain cases is reported as a scope observation about the challenge set, and may indicate that the frozen domain was narrow — but narrowness declared in advance is legitimate, whereas narrowness discovered by declining to decide is not.

Artifact 3 depends on Artifact 2. If KF-3 later shows that the mapping was wrong and the derived judgment therefore changes automatically, record that as **one coupled post-hoc mapping→judgment finding**, not two independent failures.

---

## 10. Phase 3.5 scope: no derived simulator, no search

Phase 3.5 validates external representation and judgment boundaries. It does **not** build a project-authored executable surrogate of the external system.

Non-goals:

- no newly written simulator of the external target,
- no port of Random/Beam/MCTS to the external system,
- no claim that external exploit search generalized,
- no automated executable-witness recovery claim.

Reason: a derived simulator would reintroduce the project's own representation choices into the very experiment meant to test whether those representation choices were artifacts of the synthetic engines.

Search/executable validation may become a later phase if Phase 3.5 produces a reason to do it, but no later phase number or design is committed here.

---

## 11. Known-failure challenge lane

Known failures are excluded from the primary universe because selecting observations conditioned on observed failure would create a failure-enriched sample. They are retained as a separate challenge lane testing whether artifacts already frozen from the primary lane can explain an independently documented real failure.

The challenge lane does **not** retroactively change primary R0/F0/F1/F2/F3 results.

### KF-0 — selection rule freeze

After the target is selected but before primary architectural analysis, define the target-specific mechanical rule that would later enumerate known-failure items (e.g. project-owned tracker, external labels, affected scope, status/time rule). Do not open or enumerate issue contents/titles if doing so would disclose failure details.

The actual qualifying items are enumerated only after the primary lane and all three primary artifacts are frozen.

Known-failure items never enter `P_raw`.

### KF-1 — symptom-only reveal + disclosure log

For each mechanically selected challenge item, expose only what is needed to establish the reported symptom before causal diagnosis:

Allowed if available:

```text
expected behavior
observed erroneous behavior
minimal externally documented reproduction steps
affected version
```

Withhold until KF-3 where practical:

```text
maintainer root-cause discussion
fix diff / patch
postmortem
causal comments such as "flag X was not persisted"
```

Perfect blinding is not assumed. Each item gets a disclosure log recording exactly what the analyst had already seen before the frozen-artifact evaluation (issue ID, title, labels, symptom, etc.) and whether cause leakage occurred.

### KF-2 — evaluate frozen artifacts

The challenge evaluates the already-frozen artifacts; known-failure evidence may not be used to revise them before the KF-2 outcome is sealed.

Report separate axes.

#### 11.2.1 Representability

Can the reported symptom/history be expressed using the frozen native description + architectural mapping without adding/reassigning roles after seeing the bug?

#### 11.2.2 Judgment applicability

Using only the frozen judgment specification, classify the externally reported case:

First place the case against Artifact 3's **frozen applicability domain** (Section 9), then classify:

- **in-domain, concordant:** a determinate verdict is produced and agrees with the external expected/violation judgment.
- **in-domain, DISCORDANT:** a determinate verdict is produced but conflicts with the external system's own expected/violation judgment.
- **in-domain, indeterminate:** the frozen specification claimed to decide this case and did not. This is an **Artifact 3 limitation**, not a neutral outcome.
- **out-of-domain:** the case falls outside the frozen applicability domain — scope mismatch, reported as `N/A`. Not a defect of Artifact 3, and never repaired by extending the domain after seeing the case.

Discordance is not collapsed into a generic `applicable PASS`; it is direct evidence that the frozen judgment layer does not capture the external system's stated validity judgment for that case. In-domain indeterminacy and out-of-domain scope mismatch are likewise never merged into a single `not applicable` bucket: the first is our failure, the second is a boundary declared in advance.

#### 11.2.3 Native reproduction — optional ground-truth support only

No derived simulator is created. If the external project's affected historical implementation is itself executable, a native replay may be attempted.

Native replay's evidence role is narrow: it strengthens ground truth that the reported symptom is real/reproducible and that we understood the symptom correctly. **It provides no positive evidence that the Phase 3 architecture is correct.**

Replay qualification and modification log:

- build/dependency/toolchain/environment changes: allowed, but every change is recorded;
- changes to the analyzed target-system logic: replay loses native-replay qualification;
- stubbing an interacting layer: record exactly what was stubbed and label the replay evidence as weakened/conditional;
- if native replay is not feasible without target-logic modification: report `N/A`, do not build a surrogate afterward.

A successful native replay must not be reported as `our architecture reproduced the external bug`; the native implementation reproduced its own documented behavior.

### KF-2 failure attribution

Do not reduce the challenge to one PASS/FAIL. At minimum distinguish:

```text
native description incomplete/unrecoverable
→ measurement insufficiency / E?-like challenge limitation

native structure sufficiently known but frozen architecture has no place for it
→ F2-like architectural limitation (challenge evidence; primary result unchanged)

frozen mapping represents the case but frozen judgment is discordant/indeterminate
→ judgment-layer limitation

native replay unavailable/fails for execution reasons
→ reproduction/environment issue, not automatically architectural

reported bug is not a validity phenomenon within the frozen Phase 3.5 scope
→ scope mismatch
```

### KF-3 — cause/fix reveal and comparison

Only after KF-2 is sealed may maintainer diagnosis, fix commit, patch, or postmortem be examined.

Compare the frozen independent account with external causal evidence. Cause agreement is evaluated only when the external fix/diagnosis exposes enough information to identify the relevant cause; otherwise report `N/A`.

Possible outcomes include agreement, partial agreement, different causal explanation, previously hidden native information, scope mismatch, or insufficient external causal evidence. None retroactively changes KF-2 or the primary lane.

If KF-3 reveals that Artifact 2's mapping was wrong and Artifact 3 therefore inherited the error, record one coupled post-hoc mapping→judgment finding rather than double-counting two independent problems.

---

## 12. Known-failure and primary lanes answer different questions

```text
Primary external-validation lane
→ What does an externally designed system imply about the Phase 3 representation boundaries?

Known-failure challenge lane
→ Can the already-frozen external description/mapping/judgment account for a documented real failure without being redesigned after seeing its cause?
```

Known-failure evidence may evaluate a representation already frozen from the primary lane, but it may not participate in constructing or revising that representation before the challenge outcome is sealed.

---

## 13. Biases and limitations pre-registered now

### 13.1 Open-source / inspectability selection effect

Requiring source-level E2-REP and a bounded mechanically enumerable universe selects for systems that are open, inspectable, and comparatively well-structured/documented. This is not a random sample of game systems and may differ materially from commercial engines.

### 13.2 F2 may be especially under-observed

Systems with explicit enumeration mechanisms and documentation conventions may be more likely to use conventional boundaries, reducing the chance of observing genuinely novel F2 structures. Therefore `no F2 observed` must not be interpreted as evidence that F2 is rare in games generally.

### 13.3 Asserted-enumerator missingness is directional

An `asserted` convention may miss ad-hoc exceptions, and those exceptions may be exactly where F2/F3-like behavior lives. Counterexamples found inside the asserted set remain valid; absence claims are weaker and explicitly scoped.

### 13.4 External segmentation and external cross-links determine P_raw

`P_raw` is fixed by two things we do not control: how the external sources segment themselves, and which cross-links the external project happens to declare (Section 4.2's connected components). Similar targets can therefore produce very different counting-unit totals for reasons unrelated to their architectural content. `coverage` is a within-target transparency measure, not a cross-target comparison metric.

### 13.5 No executable-search generalization claim

Because Phase 3.5 creates no project-authored simulator and runs no external search benchmark, it cannot establish external search-algorithm performance or automatic exploit discovery.

---

## 14. Reporting requirements

The final Phase 3.5 result must include, in the main body:

1. target eligibility evidence for E1-E5, plus the full screened-candidate log (rejections with criterion failed, finalists with ranking step lost) and the pre-sealed deterministic tie-break rule;
2. all admitted normative/enforcement universe sources and enforcement `enforced/asserted` tags;
3. frozen `P_raw` with raw source provenance, marking any externally-linked units and the observations retained inside them;
4. `P_resolved / P_raw` and `E? / P_raw` coverage;
5. reason log for every E?, naming which of the five sufficiency questions lacked located evidence, plus the explicit F2 re-check;
6. post-analysis correspondence matrix and correspondence-collapsed `C` count without changing `P_raw`;
7. R0/F0/F1/F2/F3 outcomes for resolved cases;
8. all counterexamples and the evidence-sufficiency/positive-evidence basis for them;
9. explicit absence/inconclusive wording under Section 8's rules;
10. three separately frozen primary artifacts, including Artifact 3's frozen applicability domain stated separately from its decision procedure;
11. known-failure selection rule, disclosure logs, separate KF-2 axes, optional native-replay modification logs, and KF-3 comparison if the challenge lane is available;
12. the pre-registered limitations in Section 13.

No result table may imply prevalence of architectural outcomes from this single target.

---

## 15. Order of operations after this methodology is approved

```text
1. Seal this methodology before target evaluation, including the concrete deterministic tie-break rule (Section 2), which must be fixed before any candidate list exists.
2. Screen candidates only against E1-E5 / enumeration admissibility.
3. Select one external target by the Section 2 ranking (enumeration completeness class -> deterministic tie-break); record every screened candidate, including rejections, with the eligibility criterion failed or the ranking step lost -- never an architectural outcome.
4. Freeze target-specific authoritative sources and all admissible normative/enforcement enumerators.
5. Freeze U_primary and P_raw before architectural analysis.
6. Freeze the target-specific KF-0 mechanical known-failure selection rule without opening failure causes.
7. Analyze every primary slice: native-first → sufficiency gate → native case → R0/F0/F1/F2/F3 or E?. No optional stopping.
8. Freeze Artifact 1 (native description), Artifact 2 (architectural mapping), Artifact 3 (derived judgment specification).
9. Seal the primary-lane result and coverage.
10. Only now enumerate/open known-failure challenge items under KF-1.
11. Seal KF-2 representability / judgment-applicability / optional native-replay results.
12. Reveal KF-3 cause/fix evidence and compare without retroactive edits.
13. Write RESULTS for Phase 3.5.
```

No external target candidate is selected by this document. No implementation plan follows until the methodology spec itself is reviewed and approved; Phase 3.5 may remain an analysis-only phase with no code implementation at all.
