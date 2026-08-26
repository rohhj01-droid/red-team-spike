# Phase 3.5 External-Validation Methodology Design

**Status:** pre-target methodology design, with the candidate discovery frame now filled (Section 2) and therefore sealable. This document defines how Phase 3.5 will select, analyze, classify, and report one external system before any target-specific architectural conclusion is allowed. It does **not** select a target, enumerate the frame's contents, inspect a target's known bugs, or authorize implementation/search work.

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

Eligibility requires **E1-E4**. E5 is listed with them for readability but is **not** an eligibility gate: it is a post-selection checkpoint, for the reasons given in its own section.

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

**Single designated, URL-bearing source location.** The candidate must additionally have **exactly one externally designated canonical source location, reachable at a stable URL** — a repository or source distribution that the external project itself identifies as authoritative for the system under examination. A project that designates none, that designates several with no primary among them, or whose designated source has no stable URL to normalize, fails E2-REP. Adjudicating which of several repositories "really" holds the system would be our judgment about the target's identity, and this location also supplies half of the Section 2 tie-break key, whose normalization presupposes a URL.

**Exactly one external target identifier.** The external project must also supply **one identifier by which it itself delimits the candidate system** (the name under which the project designates the system, its subsystem, or its module). E4 requires the *universe* to be externally delimited but does not by itself guarantee a single external *name* for the target, and the Section 2 tie-break key's second component depends on one existing. A candidate the external project does not name as a delimited system is not eligible.

**Primary snapshot.** External systems change: fields, validators, docs, and write/read paths all move between revisions, so an analyst free to choose the revision after the fact could choose the result. Before any candidate inventory is built, freeze a mechanical snapshot rule and record the exact revision it resolves to:

```text
primary snapshot = the state of the designated canonical source
location at the ENUMERATION EXECUTION TIMESTAMP (Section 2's frame
field 3b -- no separate time axis is introduced), taken from the
project's own default development branch (not a release channel):

  repository candidate
    the commit the default branch pointed at that instant,
    recorded as a full commit hash

  distribution candidate
    the externally designated canonical artifact at that instant,
    recorded by content hash
```

Three ambiguities are closed deliberately. **Default branch, not release:** a project offering both would otherwise leave the choice open, and the default branch is the one revision every such project has. **Hash, not tag or version:** tags and release labels can be moved or re-cut, so they are not immutable identifiers; only the hash pins the state that was actually analyzed — the same rule Section 2 applies to the frame's own source revision. **The enumeration execution timestamp, not a new one:** an earlier draft referred to a "sealed snapshot timestamp" that no longer exists as a field, which left the snapshot moment undefined; reusing the frame's execution timestamp fixes it without adding a second time axis to keep consistent.

Every later step — inventory, `U_primary`, `P_raw`, information-flow tracing, all three frozen artifacts — is defined against that one recorded revision. The KF lane's `affected version` may differ from it; where it does, that mismatch is recorded as a cross-lane condition on the challenge result rather than silently resolved by re-analyzing at another revision.

### E3 — Architecture-neutral validity eligibility

At least one validity observation must be externally enumerable without requiring the project to first decide that the system contains a lifecycle, provenance chain, cross-system interaction, or any other Phase 3-shaped mechanism.

The admission condition is intentionally weak: the external source must expose a stateful/temporal validity question that can be examined. Whether multiple lifecycles exist or interact is a result, not an entrance requirement.

### E4 — Neutral primary-universe construction

The target must permit a **property-level primary universe** to be determined by external/mechanical rules rather than by researcher interest. A subsystem list such as `Quest / Inventory / Equipment` is not enough if the actual validity observations inside those subsystems would still be hand-picked.

If no externally determined, mechanically enumerable primary observation universe can be constructed at the required granularity, the candidate is rejected as the Phase 3.5 primary target.

### E5 — Bounded exhaustive analysis (a post-selection checkpoint, not an eligibility gate)

It is not enough that source code exists; the entire frozen primary universe must be traceable to the evidence-sufficiency gate without sampling or optional stopping. A huge open-source system whose relevant state is spread across an unbounded implementation surface satisfies E2-REP and still cannot be analyzed exhaustively.

**But E5 cannot be a pre-selection eligibility gate, because judging it would breach the firewall that gate sits behind.** Deciding whether flows are "traceable enough" requires actually tracing some of them, which candidate screening explicitly forbids; and "small/local enough" has no screening-measurable threshold, so an analyst could drop a candidate by declaring it too large after forming an impression of what it would show. An earlier draft listed E5 among the pass/fail admission criteria; that was a contradiction between two of this document's own rules.

E5 is therefore relocated:

```text
E1-E4          pass/fail eligibility, decidable at screening depth
E5             checked AFTER the target is selected and U_primary frozen
```

If the frozen `U_primary` then proves not exhaustively traceable, the primary lane reports a **boundedness failure** — the same outcome shape the KF lane uses (Section 11) — rather than yielding an architectural verdict.

**A boundedness failure does not license selecting a different target.** Re-running selection after a failed attempt would make the first attempt a free look at a candidate, with the second choice informed by it. The failure is reported as the outcome of this Phase 3.5 run.

### Candidate discovery frame — sealed before any candidate is seen

Everything downstream of here constrains how a candidate is *judged*, and none of it constrains how the candidate list came to exist. Screening three hand-chosen projects and then applying a deterministic tie-break satisfies every rule in this section while leaving target-selection bias fully intact, one step further upstream. The candidate frame must therefore be mechanical and sealed in advance, exactly like the tie-break:

```text
Frozen before any candidate is inspected:

  1. enumeration source(s)
     named external index/catalog/registry/topic listing that this
     project does not control

  2. exact query or filter applied to it
     literal, reproducible, no post-hoc adjustment

  3a. frame source revision
      the revision of the enumeration source that DETERMINES
      membership, identified by CONTENT HASH, not by label. A release
      tag or version name is recorded as provenance only, for the same
      reason the primary-snapshot rule refuses them: tags and release
      labels can be moved or re-cut, so they do not pin the bytes that
      were actually enumerated. For a live index, membership is instead
      determined by 3b and this field records "live".

  3b. enumeration execution timestamp
      when the list was actually generated. This is provenance only
      wherever 3a already fixes membership, and is membership-
      determining only for a live index.

  4. screening order
     ascending UTF-8 byte order of the identifier the enumeration
     source itself returns for each result

  5. screening budget
     a number fixed now, not after seeing how many results returned
```

**The frame's ordering key is not the Section 2 tie-break key.** The tie-break key is `(canonical source-location URL, external target identifier)`, and both components are guaranteed only by E2-REP — that is, only for candidates that have already been screened. Ordering the *unscreened* frame by it would require knowing eligibility before screening, and screening in an order that requires screening. The frame is therefore ordered by whatever identifier the enumeration source itself attaches to every result it returns (a catalog entry ID, a `owner/name` pair, a list position), which exists for every frame item by construction. Two keys, two stages, each total over its own set.

Every result the frozen query returns enters the frame. Candidates are screened **in the frozen screening order** until the frame is exhausted or the screening budget is reached, whichever comes first, and the report states which of the two occurred and how far screening got.

#### The sealed frame values

```text
Enumeration source
  the official OpenBSD 7.9 `ports.tar.gz` release artifact,
  retrieved from https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz

Frame source revision (membership-determining) -- RECORDED
  SHA256 937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db
  size   56386078 bytes
  Last-Modified 2026-05-06T12:39:58Z (as served)

  Computed locally from the retrieved bytes and cross-checked against
  OpenBSD's own published checksum at
  https://cdn.openbsd.org/pub/OpenBSD/7.9/SHA256, which lists the
  identical value. Membership identity rests on this hash, never on a
  label.

  The artifact was retrieved and hashed WITHOUT being extracted; the
  `games` category was not enumerated, listed, or read at this step.

Release label (provenance only)
  OpenBSD 7.9 -- recorded for traceability, not relied on for identity

Enumeration execution timestamp
  recorded when the list is generated; provenance for the frame,
  and additionally the fixed point in time at which each candidate's
  primary snapshot is taken (see E2-REP)

Query
  all ports whose OpenBSD-assigned categories include `games`;
  a port listing several categories qualifies on `games` alone.
  No additional genre, popularity, activity, language, or
  maintenance filter of any kind.

Raw-frame membership granularity
  one frame item per PORT DIRECTORY, flavors and subpackages
  collapsed. FULLPKGPATH distinguishes flavors of one port
  (`games/foo` vs `games/foo,-data`), but a flavor is a packaging
  variant of a single upstream system, and a candidate is an
  external system. Counting flavors separately would let one
  upstream project consume several budget slots and repeat in the
  screening order.

Raw screening order
  ascending UTF-8 byte-wise order of the port directory path

Screening budget
  128 frame items
```

**Frame item to candidate: upstream-resolution screening.** A port is packaging metadata and patches; the external system under examination is its **upstream**. But OpenBSD has no single guaranteed upstream field — `HOMEPAGE` is populated only where applicable, and fetching may go through distfile sites, mirrors, or hosting-specific metadata. An analyst reading several plausible URLs and picking "the real upstream" would reinsert discretion directly into candidate identity, at the one place the whole frame exists to remove it. Therefore:

```text
The frozen port metadata identifies exactly one upstream system
unambiguously
    → the frame item resolves to that candidate;
      E1-E4 are judged against the UPSTREAM, which is also where
      E2-REP's canonical source location must exist

It does not
    → the frame item FAILS upstream-resolution screening
      and is recorded as such

The analyst never selects among several plausible upstreams.
```

Failing upstream resolution — like failing E2-REP because the upstream is a tarball with no stable URL-bearing canonical source location — is an ordinary screening outcome, not a frame defect.

**Two frame items, one upstream.** Distinct port directories can package the same external system:

```text
several frame items resolve to the same externally identified upstream
    → ONE candidate after identity resolution
      (the same project must not enter ranking twice)

    → but every original frame item stays in the screening log,
      and each already consumed its screening-budget slot
```

Collapsing them for ranking prevents one project from occupying several ranking positions; refusing to refund their budget slots prevents the sealed frame accounting from being quietly reduced after the fact.

**Why a package-repository category, and why this one.** A curated "best open-source games" list would have been assembled by someone selecting for quality, fame, or interest, which plausibly correlates with maturity, documentation quality, and structural cleanliness — all things this study measures. Category membership in a source-building package repository is a far less semantic criterion: roughly "someone ported it" plus "the repository classified it as a game." A code-hosting search was rejected for the opposite reason — its result set is so large that the screening budget would become the de facto sampling mechanism rather than a workload ceiling.

**Frame-choice provenance, recorded because this document demands it of itself.** While comparing enumeration sources, some candidate names from Debian, Flathub, and F-Droid game listings were incidentally seen. Selecting any of those indices afterwards would violate this section's own "sealed before any candidate is seen" rule in appearance even if not in intent. For the OpenBSD Ports Collection, only the category mechanism and the source-building structure were examined; the `games` category membership list was not enumerated or read. That is the operative reason this index was chosen over the others, and it is recorded rather than left implicit.

**The budget is a workload ceiling, not a sample size.** 128 carries no statistical claim; frame membership is not sample inference. It is the screening workload fixed in advance. If no eligible candidate appears within the first 128 items under the frozen order, that is the reported candidate-discovery outcome of this run — looking at the 129th is forbidden.

Nothing about the frame may be adjusted after seeing its results — not the query, not the budget, not the order. If the frame returns nothing eligible, that is the reported outcome of this run; re-framing afterwards would let the first frame's contents inform the second, which is the same free-look problem E5's boundedness rule guards against.

### Selecting among multiple eligible candidates

E1-E4 are pass/fail admission gates, not a ranking. If more than one candidate is eligible, the choice must not fall to researcher interest — otherwise target-selection bias simply replaces the slice-selection bias E4 exists to prevent, one step earlier.

#### Candidate inventories are frozen before E5 and before ranking

Both E5 ("the **entire frozen primary universe** is boundedly traceable") and ranking criterion 1 ("**every admitted** enforcement enumerator is `enforced`") are statements about a candidate's enumerators and universe. Neither can be evaluated before those exist. Freezing them only after target selection would make the selection basis circular: a candidate could be ranked class A, and then a further `asserted` enumerator found afterwards would retroactively invalidate the ranking that chose it.

Therefore, for **each candidate surviving E1-E4**, freeze a candidate-level inventory before any ranking (E5 is no longer judged here at all — it moved to a post-selection checkpoint):

```text
authoritative-source inventory     (Section 3.1 admissible sources)
admissible-enumerator inventory    (Section 3.2, EN1-EN6)
enumerator completeness tags       (Section 3.3, enforced / asserted)
mechanically enumerated universe   (Section 3, U_normative ∪ U_enforced)
```

This is safe to do before selection because building it is **mechanical enumeration under already-fixed rules, not semantic analysis**: it applies the external project's own segmentation and enumerators, and it does not require tracing information flow, mapping to Phase 3 roles, or forming any architectural judgment. The candidate-screening firewall still applies to everything beyond it.

If an admissible enumerator or authoritative source is discovered **after** target selection, it is recorded as a **screening/inventory protocol failure** and reported as such. It is not silently folded into the universe, because doing so would alter both `P_raw` and the completeness class that justified the selection.

**What that failure does to the run's conclusions.** Reporting it as a footnote is not enough: a late-discovered source or enumerator could have changed the completeness class that selected this target, or changed `P_raw`, which is the coverage denominator every scoped claim rests on. Therefore:

```text
late discovery could have changed the completeness class or P_raw
  → the run's confirmatory primary conclusions (R0 and any
    absence/retention statement) drop to INVALID / INCONCLUSIVE
  → analysis already performed is retained, relabelled exploratory
  → counterexample findings (F1/F2/F3) survive, since a counterexample
    found inside an under-enumerated universe is still a real
    counterexample (Section 3.3's asymmetry, applied again)

late discovery provably could not have changed either
  → record it; conclusions stand
```

The asymmetry is the same one used throughout: incompleteness damages absence claims and leaves existence claims intact.

Ranking then uses exactly two steps, in this fixed order, both fully decidable from the frozen candidate inventories:

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

2. **Deterministic tie-break, sealed here rather than by example.** Order the tied candidates by their **normalized canonical source-location URL**, ascending, comparing the byte sequences of its UTF-8 encoding; select the first.

```text
normalized canonical source-location URL =
  the HTTPS form of the canonical source location (repository or
  source distribution) that the
  external project itself designates, with:
    scheme and host lowercased
    no credentials, query, or fragment
    no trailing slash
    no trailing ".git"
```

   **The key is a pair, because the URL alone is not total.** Two distinct eligible candidates can share one source location — for example, two separately delimited systems inside the same monorepo — and would then be unordered by URL alone. The full sort key is therefore:

```text
tie key = ( normalized canonical source location URL,
            externally designated target identifier )

compared componentwise, each ascending by UTF-8 byte sequence
```

   **Both components are guaranteed by eligibility, not assumed.** An earlier draft justified the second component by appeal to E4, which requires the *universe* to be externally delimited but does not by itself guarantee a single external *name* for the target — the totality argument rested on a premise the document did not actually state. E2-REP now requires exactly one URL-bearing designated canonical source location (first component) **and** exactly one external target identifier (second component), so both exist and are single-valued for every eligible candidate.

   The ordering is then total over the eligible set: if two candidates tie on **both** components, they carry the same external source location and the same external identifier, which means they are the same externally delimited system — one candidate, not two. The rule is fixed at seal time precisely because choosing between ascending and descending, or between a project's name and its source-location URL, after seeing the candidate list would itself be a selection.

**No traceability ranking step is used.** An earlier draft ranked eligible candidates by how directly their evidence supported tracing every unit. That is dropped for two reasons: it was qualitative and never operationalized, and judging it would require inspecting candidate implementations more deeply than the candidate-screening firewall permits — the ranking step would itself breach the firewall it sits behind. That same firewall conflict is why E5 is no longer an eligibility gate either: traceability is assessed once, against the single selected target's frozen `U_primary`, and never as a comparison across candidates.

**`P_raw` size is excluded as a ranking criterion in both directions.** A small universe is easier to analyze but offers fewer chances to observe a counterexample; a large universe makes `U == 0` nearly unreachable and therefore makes an absence claim easy to avoid committing to. Either direction lets a preference about the result enter target selection.

Every screened candidate is recorded, including rejected ones, with the specific eligibility criterion failed or the ranking step lost. A record showing only the selected target hides how many candidates were screened and whether near-misses were rejected on soft grounds.

### Candidate-screening firewall

Before a target is frozen, screening may inspect only what is necessary to determine E1-E4 (not E5, which is now a post-selection checkpoint), to establish the existence/admissibility of enumeration mechanisms, and to build each surviving candidate's frozen inventory by applying those mechanisms. Screening must not inspect known-bug root causes, fix diffs, trace information flow, form architectural mappings, or use interesting-looking validity behavior to hand-pick the target's primary counting units.

Target candidates are evaluated only after this methodology document is sealed.

---

## 3. Primary observation universe

The primary universe is defined at the source-observation level, not by researcher-inferred semantic properties.

```text
U_primary = U_normative ∪ U_enforced
```

Known bugs do not contribute to `U_primary`.

### 3.1 U_normative — externally stated validity observations

`U_normative` contains atomic observations emitted by rule sources the external project has **explicitly designated as authoritative**, and that explicitly state validity requirements.

Source selection rules:

- **Only sources the external project explicitly designates as authoritative for its rules are admissible.** Project ownership alone is not sufficient: a README, a manual, test files, docstrings, and design notes can all be project-owned while disagreeing with each other, and "which project-owned text states the rules" would then be our judgment — a judgment that determines sources, hence observations, hence `P_raw`. An earlier draft said only to *prefer* the self-designated canonical source, which left open whether other project-owned material could also be admitted.
- If the project designates **no** authoritative rule source, the normative route is simply unavailable for that candidate; it must then satisfy E4 through `U_enforced` alone, or fail E4. We do not promote a project-owned source to authoritative on its behalf.
- If multiple designated authoritative sources exist, take their union rather than choosing the cleaner or smaller one.

An earlier draft allowed a third-party source to qualify by satisfying "the target-specific authority rule frozen before analysis." That escape hatch is removed: no such rule is defined anywhere in this document, and letting us author one after seeing a target would reopen universe selection at its root — authority determines sources, sources determine observations, observations and cross-links determine `P_raw`. Third-party material may be used as **supporting evidence** during analysis, but never as primary-universe membership. Phase 3.5 needs exactly one target, so declining to adjudicate third-party authority costs little and closes a large hole.

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

Within the enumerator's declared scope, membership must be closed by something other than our choice. "Strong enough" is not a criterion, so the closure basis is enumerated explicitly instead:

```text
runtime construction closes the set
  (registry contents, interface dispatch, annotation collection)
    → ADMISSIBLE, tagged `enforced`

an unconditional universal claim about the CURRENT codebase
  ("all quest conditions implement QuestCondition")
    → ADMISSIBLE, tagged `asserted`

a policy/aspiration about what contributors ought to do
  ("all quest conditions SHOULD implement QuestCondition")
    → NOT ADMISSIBLE (states an obligation, not closure)

a hedged description
  ("validators are USUALLY under /validation")
    → NOT ADMISSIBLE (asserts no closure at all)
```

These cases are exhaustive for EN5: a closure basis either closes the set operationally (admissible, `enforced`), claims closure of the current state unconditionally (admissible, `asserted`), or does neither — the last covering both aspirational policy and hedged description, which fail for different reasons but fail alike. Section 3.3's `enforced`/`asserted` tag follows directly from which admissible case applies, rather than being assigned separately.

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

**Sufficiency is evaluated per native case; `E?` and coverage are assigned per counting unit, by conjunction over that unit's native cases** (Sections 5.2 and 6). Inside a linked unit, both source observations are retained and their agreement or divergence is reported as a finding of that unit; recovering the unit's native information flow may draw on the evidence attached to any of its observations.

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

**Cross-link edges may not come from known-failure material.** An edge is admissible only if it appears in an artifact already admissible before the known-failure lane opens (Section 11). A bug report, fix discussion, patch, or postmortem that reveals `rule N1 corresponds to validator E3` must **not** create or alter a primary cross-link edge. Edges change connected components, components change `P_raw`, and `P_raw` is the coverage denominator — so allowing KF material to supply edges would let known-failure knowledge reach back and reshape the primary lane's accounting, which Section 12's firewall exists to prevent. Such a correspondence may still be reported in KF-3 as a post-hoc observation.

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

An externally-linked primary counting unit (Section 4.2) contributes **1** to `P_raw` while carrying its retained source observations inside it. Those observations are reported individually within the unit, and their agreement or divergence is a finding of that unit, not a change to the denominator. `E?` and coverage are assigned to the unit as a whole rather than per contained observation; sufficiency itself is evaluated on the unit's native cases, and the unit is resolved only if every one of them passes (Section 6).

Coverage must always be reported with its denominator. `E?` is never silently dropped.

Post-analysis, also report a separate correspondence-collapsed count:

```text
C = number of distinct native information-flow / architectural cases
```

`C` never replaces `P_raw` as the coverage denominator because correspondence is learned after analysis.

If two counting units later map to the same native case, report both:

```text
counting units linked to that F3 native case = 2
native cases carrying an F3 finding = 1
```

No prevalence inference is permitted from either count.

### 5.2 Three levels must remain separate

```text
1. Primary slice (= primary counting unit)
   normally one source observation;
   an externally-linked unit may contain several source observations
   the unit at which E?, coverage, and P_raw are assigned

2. Native information-flow case
   recovered from evidence after analysis
   the level at which architectural findings are assigned

3. Architectural classification
   R0 / F0 / F1 / F2 / F3
   applied only after evidence sufficiency
```

`E?` means level 1 could not be carried reliably into level 2. It is not an architectural class.

**The unit↔case relation is many-to-many, and the two levels carry different things.** Convergence was already noted (several counting units describing one native case). Divergence is equally possible and was not: because we never subdivide a source observation, one observation may state `A ∧ B ∧ C`, and a connected-component linked unit may bundle several observations — either can resolve into **several distinct native information-flow cases**. Assigning one `{F1,F2,F3}` subset per counting unit would then be incoherent whenever a unit's cases differ (case A retained, case B underdetermined; case A collapsing a role, case B misplacing a boundary).

```text
native case     → the sufficiency gate,
                  then R0 / F0 / the supported subset of {F1,F2,F3}
counting unit   → P_raw, E?, coverage;
                  resolved iff every associated native case
                  passes sufficiency

the mapping between them is many-to-many and is reported as such
```

A counting unit is `P_resolved` only if **every** native case it resolves into passes the sufficiency gate; if any one of them cannot be recovered, the unit is `E?` with that case named. This is the same "coarse bundling is not a free win" property noted in Section 4.1: bundling reduces unit count while raising each unit's chance of being `E?`.

---

## 6. Evidence-sufficiency gate

Architectural classification of a **native case** is allowed only after that case's native information flow is recoverable with enough evidence to answer, in native terminology (and a **counting unit** is `P_resolved` only when every native case it resolves into clears this gate):

1. What value/fact is created?
2. Where is it written or updated?
3. What is its lifetime/persistence behavior?
4. Which transitions/components read or consume it?
5. Does it persist after consumption, reset, migrate to another owner, or disappear?

Module/file boundaries are not architectural evidence by themselves. A 3,000-line God class may still contain a clear information-flow boundary; a beautifully separated directory tree may not.

### 6.0 Sufficiency must be evidenced, not asserted

The sufficiency gate is the only thing separating `E?` from a resolved case, and `E?` is expensive: it blocks absence claims (Section 8.4) while producing no architectural finding of its own. That creates a standing incentive to declare sufficiency too readily — the one judgment in this protocol with a built-in directional pull and, as originally written, no constraint on it.

Therefore each native case must record, for each of questions 1-5 above, the **specific located native evidence** answering it (file/symbol/schema/document reference); a counting unit's sufficiency is the conjunction over its cases.

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

This list reads as a decision procedure for each finding individually, **not** as a set of mutually exclusive outcomes; see Section 7.0.

---

## 7. Architectural outcome taxonomy

### 7.0 F1/F2/F3 are findings, not one exclusive label

Nothing makes the three counterexample types mutually exclusive. One native case can easily support more than one at once — for example, a provenance responsibility that collapses into ordinary item state (F1) while a validity monitor's ownership sits on a different lifetime than ours (F3); or a role that collapses (F1) alongside a concurrency structure the four roles cannot express (F2).

If a single label were required, the analyst would pick a "most essential" one after seeing the evidence, which is exactly the discretion this document removes everywhere else.

```text
For each resolved NATIVE CASE (Section 5.2, not per counting unit):

  counterexample findings = any subset of {F1, F2, F3}
  record EVERY supported finding; no precedence rule
  suppresses another supported finding

  if that subset is empty:
      classify as R0 or F0 (Sections 7.1/7.2), which are
      mutually exclusive with each other
```

Section 8's existence logic is unaffected: **any** supported F1/F2/F3 finding establishes that a counterexample exists. Counting reports the number of native cases carrying each finding, and separately the counting units those cases came from; a case carrying two findings is reported under both — never split into fractions and never reduced to one.

### 7.1 R0 — retained within this case

**Absence of F1/F2/F3 is not sufficient for R0.** R0 requires **positive native evidence privileging the Phase 3 responsibility/boundary over a concrete competing representation** — the same positive-evidence standard Section 6.2 imposes on F3, applied symmetrically so that the retention outcome is not the cheap default.

```text
native flow privileges the Phase-3 boundary over a named alternative
→ R0

native flow is compatible with the Phase-3 mapping AND with at least
one materially different mapping, privileging neither
→ F0
```

Mere compatibility with our architecture is therefore never R0. The competing representation must be named, and the evidence must discriminate between them.

**The named competitor must be a real one.** Requiring a name is not enough on its own: an analyst could name a transparently poor alternative, exclude it, and manufacture R0. The competing representation must therefore:

```text
satisfy the frozen external validity semantics,
satisfy every established native fact that does NOT bear on the
  boundary under examination,
and differ from the Phase-3 mapping materially ONLY at that boundary
```

An alternative that fails the external semantics, or that contradicts already-established native facts unrelated to the boundary in question, does not qualify as the competitor R0 must discriminate against — ruling it out shows nothing about the boundary.

An earlier draft allowed R0 when evidence ruled out alternatives "strongly enough," which left the R0/F0 line to be drawn after the result was visible — cheap in whichever direction the analyst preferred.

R0 is corroboration from one external case, never proof of general necessity.

### 7.2 F0 — underdetermined

The native flow is sufficiently observed, but competing representations fit equally well and the system itself does not privilege one decomposition.

F0 is **not** evidence insufficiency. It means we looked successfully and the system does not identify the boundary question.

The allowed claim is target-local: this native case does not establish that the Phase 3 boundary is necessary. Do not automatically upgrade one F0 result into a universal statement that the architecture is case-dependent.

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

Every architectural claim must be scoped to the evidence actually resolved, e.g. `among the native cases recovered from the X/Y preregistered primary counting units that passed the sufficiency gate...`.

### 8.3 Counterexample found

If any native case passes sufficiency and yields F1/F2/F3, the counterexample remains informative regardless of how many counting units are E?. However:

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

**Constraints on the KF-0 rule itself.** Banning hand-picked challenge items accomplishes nothing if the *rule* can be composed after seeing the tracker so that it yields a convenient set — rule-picking is hand-picking with extra steps. The rule is therefore bound by:

```text
It may condition only on externally supplied metadata
(tracker of record, project-applied labels, affected component/scope,
status, declared time range). It may not condition on mechanism,
content, or root cause.

It must take the BROADEST externally defined failure set available
for the target's scope. Narrowing by analyst-chosen label subsets,
status filters, or time windows ("bugs from 2025 only") is not
permitted: restricting metadata values is rule-picking, which
reproduces hand-picking one level up. Narrowing is admissible only
where the external project's own scope definition already imposes it.

Every item satisfying the frozen rule is included.

No post-enumeration subsampling, for any reason.

If the mechanically generated set is too large to analyze
exhaustively, report the known-failure lane as a boundedness
failure / N/A -- do not select a convenient subset from it.
```

The last clause mirrors the primary lane's no-optional-stopping rule (Section 8.6) and E5's treatment of unbounded universes: when exhaustiveness is unavailable, the honest result is that this lane did not produce evidence, not a smaller lane chosen by us.

### KF-1 — symptom-only reveal + disclosure log

For each mechanically selected challenge item, expose only what is needed to establish the reported symptom before causal diagnosis:

Allowed if available:

```text
expected behavior
observed erroneous behavior
minimal externally documented reproduction steps
affected version
```

Withhold until KF-3 unless exposure is unavoidable (see below):

```text
maintainer root-cause discussion
fix diff / patch
postmortem
causal comments such as "flag X was not persisted"
```

Perfect blinding is not assumed. Each item gets a disclosure log recording exactly what the analyst had already seen before the frozen-artifact evaluation (issue ID, title, labels, symptom, etc.) and whether cause leakage occurred.

**"Where practical" is not analyst latitude.** Causal material is withheld unless exposure is *unavoidable* — the cause appears in the issue title, in the same field as the symptom, or is otherwise impossible to read the symptom without seeing. Choosing to read a linked patch because it seemed convenient is not unavoidable exposure. Every unavoidable exposure is logged as cause leakage for that item; the item is still evaluated, with its causal-agreement evidence marked weakened.

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

No derived simulator is created. If the external project's affected historical implementation is itself executable, a native replay may be attempted — but **not item by item at the analyst's discretion**. Attempting replay only where it looks likely to succeed would make the replay results a selected sample. Freeze a feasibility predicate over externally observable facts (affected version is obtainable, build/run instructions exist, documented reproduction steps are present) before opening the items, then **attempt replay for every challenge item satisfying it, or report native replay as `N/A` for the whole lane**. No middle ground.

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

Requiring source-level E2-REP, a mechanically enumerable universe (E4), and a candidate frame drawn from an external index of inspectable projects selects for systems that are open, inspectable, and comparatively well-structured/documented. (E5's boundedness requirement no longer contributes to this effect, since it no longer filters candidates — but it can still end a run, so an unbounded target is excluded from *results* even though it was not excluded from *selection*.) This is not a random sample of game systems and may differ materially from commercial engines.

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

1. the sealed candidate discovery frame (enumeration source, frame source revision as recorded at enumeration, enumeration execution timestamp, exact query, membership granularity, screening order, screening budget) and whether screening exhausted the frame or hit the budget; target eligibility evidence for E1-E4 plus the post-selection E5 checkpoint result; the recorded primary snapshot revision; the full screened-candidate log (rejections with criterion failed, finalists with ranking step lost); and the pre-sealed deterministic tie-break rule;
2. all admitted normative/enforcement universe sources and enforcement `enforced/asserted` tags;
3. frozen `P_raw` with raw source provenance, marking any externally-linked units and the observations retained inside them;
4. `P_resolved / P_raw` and `E? / P_raw` coverage;
5. reason log for every E?, naming which of the five sufficiency questions lacked located evidence, plus the explicit F2 re-check;
6. post-analysis correspondence matrix and correspondence-collapsed `C` count without changing `P_raw`;
7. per resolved **native case**, the full supported subset of {F1,F2,F3} with no suppressed findings, or R0/F0 where that subset is empty, plus for R0 the named competing representation the evidence discriminated against; and the many-to-many map between counting units and native cases;
8. all counterexamples and the evidence-sufficiency/positive-evidence basis for them;
9. explicit absence/inconclusive wording under Section 8's rules;
10. three separately frozen primary artifacts, including Artifact 3's frozen applicability domain stated separately from its decision procedure;
11. known-failure selection rule, disclosure logs, separate KF-2 axes, optional native-replay modification logs, and KF-3 comparison if the challenge lane is available;
12. the pre-registered limitations in Section 13.

No result table may imply prevalence of architectural outcomes from this single target.

---

## 15. Order of operations after this methodology is approved

```text
1. Seal this methodology before any candidate is seen, including the candidate discovery frame (enumeration source, frame source revision, exact query, membership granularity, screening order, screening budget) and the concrete deterministic tie-break rule -- all of Section 2, fixed before any candidate list exists.
2. Run the frozen query against the frozen frame source revision, recording the enumeration execution timestamp as provenance; every result enters the frame. Screen in the frozen screening order until the frame is exhausted or the screening budget is reached, and record which occurred.
3. Screen candidates against E1-E4 / enumeration admissibility only. E5 is NOT judged here.
4. For EACH candidate surviving E1-E4, freeze its primary snapshot (exact revision) and then its candidate-level inventory: authoritative sources, admissible enumerators, enforced/asserted tags, and the mechanically enumerated universe. This is mechanical enumeration under already-fixed rules, not analysis.
5. Rank the eligible candidates by the Section 2 ranking (enumeration completeness class -> deterministic tie-break) and select one; record every screened candidate, including rejections, with the eligibility criterion failed or the ranking step lost -- never an architectural outcome.
6. Promote the selected candidate's frozen inventory to U_primary and P_raw, at its recorded revision. Any admissible source or enumerator discovered after this point is a screening/inventory protocol failure with the conclusion effects defined in Section 2.
7. Check E5 against the frozen U_primary. If it fails, report a primary-lane boundedness failure and stop -- do not select a different target.
8. Freeze the target-specific KF-0 mechanical known-failure selection rule, under Section 11's constraints on the rule itself, without opening failure causes.
9. Analyze every primary counting unit: native-first → sufficiency gate → native case(s) → per native case, the supported subset of {F1,F2,F3}, or R0/F0 if that subset is empty; a unit is E? unless every case it resolves into passes the gate. No optional stopping.
10. Freeze Artifact 1 (native description), Artifact 2 (architectural mapping), Artifact 3 (applicability domain + decision procedure).
11. Seal the primary-lane result and coverage.
12. Only now enumerate/open known-failure challenge items under KF-1.
13. Seal KF-2 representability / judgment-applicability / optional native-replay results.
14. Reveal KF-3 cause/fix evidence and compare without retroactive edits.
15. Write RESULTS for Phase 3.5.
```

No external target candidate is selected by this document. No implementation plan follows until the methodology spec itself is reviewed and approved; Phase 3.5 may remain an analysis-only phase with no code implementation at all.
