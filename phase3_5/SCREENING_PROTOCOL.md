# Phase 3.5 Screening Record Contract

Fixes the record schema, gate order, and controlled vocabularies for
screening the 128 frame items in `screening_set_128.txt`, **before any
item is screened**. Same reason every other contract in this project
was sealed first: the format must not be shaped by what the results
turn out to look like.

Governed by the methodology sealed at `401924d`. This document adds no
eligibility criterion — it only names, orders, and records the ones
already sealed there.

## Two ledger levels

An OpenBSD port and an external system are not 1:1, so the record has
two levels that must not be merged:

```text
screening_frame_items.tsv   exactly 128 rows, always
                            one per frame item, in frozen rank order

screening_candidates.tsv    one row per UNIQUE upstream candidate
                            created only after upstream resolution
```

A duplicate never disappears from the frame ledger and never refunds
its budget slot; it simply creates no new candidate row. This is the
sealed rule from the methodology's "Two frame items, one upstream"
paragraph, expressed as a file layout.

## Gate order, and first-fail stop

```text
0. UR        upstream resolution
1. E1        external authorship
2. E2-REP    native representation access
3. E2-RULE   externally authored validity evidence
4. E3        architecture-neutral validity eligibility
5. E4        mechanically constructible primary universe
```

The order is dependency-respecting: E3 needs sources to exist (E2), and
E4 needs both `U_normative` (E2-RULE) and `U_enforced` (E2-REP) to be
constructible, so it runs last.

**Screening stops at the first FAIL.** Gates after it are recorded
`NOT_REACHED`, never evaluated. Gate states:

```text
PASS  |  FAIL  |  UNRESOLVED  |  NOT_REACHED
```

`UNRESOLVED` exists because the network contract below produces a state
that `PASS/FAIL/NOT_REACHED` cannot express without lying: a protocol
issue is neither a criterion failure nor an unexamined gate. Recording
one as `FAIL` would disguise a protocol issue as a criterion failure,
which is precisely what that contract exists to prevent.

```text
protocol issue at gate G:
  G                 = UNRESOLVED
  gates after G     = NOT_REACHED
  overall           = UNRESOLVED
  stop_gate         = G
  failure_code      = NONE
  protocol_issue_code = the applicable PI- code
```

`failure_code` and `protocol_issue_code` are separate columns and never
both populated. Candidate `overall` is correspondingly
`ELIGIBLE | REJECTED | UNRESOLVED`, matching the frame ledger's existing
`terminal_status=UNRESOLVED`.

This is not merely economy. Continuing past a failure would expose
target information the protocol has no use for, and would let curiosity
decide which failed candidates get inspected more deeply than others —
selective inspection reintroduced one level below target selection.

## UR and E2-REP ask different questions

This distinction is what keeps upstream resolution mechanical, and it
must be applied exactly:

```text
UR   — from the FROZEN OpenBSD port metadata
       "which external system is this port packaging?"

E2-REP — from the UPSTREAM SYSTEM ITSELF
       "does that system designate exactly one canonical
        source location, at a stable URL, and does it supply
        exactly one external target identifier?"
```

A port whose `HOMEPAGE` points at a project website while `GH_ACCOUNT`/
`GH_PROJECT` point at a repository and `MASTER_SITES` points at a
distfile mirror is **not** ambiguous: those are several facts about one
system. `UR-AMBIGUOUS` applies only where the metadata points at
genuinely *different* systems with no external basis for choosing.

Which location is canonical is therefore **not** decided from OpenBSD's
metadata at all — the sealed spec requires the external project itself
to identify it, so that judgment belongs to E2-REP and rests on
upstream's own designation. Reading it off the port's fields would make
OpenBSD's packaging convenience our identity criterion.

## E2-REP network-access contract

E2-REP asks a question about the upstream system, so it is answered
from the upstream system — frozen OpenBSD metadata cannot substitute,
and this document already rejects letting it. That means live network
access, which brings its own discretion to remove: without limits,
"screen a candidate" quietly becomes "read about the project until
satisfied."

**Purpose.** Establish only whether a canonical source location exists,
is designated by upstream itself, sits at a stable URL, carries one
external target identifier, and actually holds a source tree.

**Allowed starting points.** Only the URLs and identifiers found in the
frozen OpenBSD metadata that UR already resolved to one system.

**Allowed navigation, in order:**

```text
1. the upstream official landing/project page
2. a Source / Code / Repository / Development link that page
   explicitly exposes
3. the metadata/root surface of the official source repository reached
```

**Allowed observations at the repository:** existence; project or
repository name; owning project or account; default branch; that a
source tree is actually present; whether upstream designates this
location as its source; any primary/mirror marking.

**Forbidden at E2-REP:**

```text
reading README prose            opening any source file
browsing docs                   issues / PRs / changelog / releases
searching for bugs or exploits  checking validity semantics
any extra look justified by "this might help E3/E4 later"
```

**Stop rule.** Navigation ends the moment a `PASS` or a specific
failure code is determined. Not one page further.

### Unavoidable exposure

"Never see a README" is not achievable — code-hosting landing pages
render one automatically. So the rule is not blindness but quarantine:

```text
Content encountered incidentally at E2-REP is recorded in the exposure
log and is NOT used to pre-judge E2-RULE, E3, or E4, nor to reorder or
shortcut any later gate.
```

The same discipline the known-failure lane applies to cause leakage:
log what was unavoidably seen, and refuse to let it do work.

### Transport failure is not criterion failure

A candidate must not be rejected because of our network conditions.
Distinguish what the endpoint said from what we failed to learn:

```text
definitive HTTP answer (404, 410, or an equivalent permanent absence)
  → genuine evidence ABOUT THAT ENDPOINT. It is not by itself a
    candidate-level E2-REP FAIL: if other allowed upstream paths
    remain (Section "Allowed navigation"), they are followed first,
    and a failure code is assigned only once E2-REP as a whole is
    actually determined.

transport-level indeterminacy (timeout, DNS failure, connection
refused, 5xx)
  → NOT evidence of absence. Retry twice at recorded times; if still
    indeterminate, record a PROTOCOL ISSUE for that item rather than
    forcing it into a failure code.
```

Coding a timeout as `E2REP-NO-STABLE-URL` would reject a candidate for
a fact about us, and would be indistinguishable in the record from a
genuinely dead location. This mirrors the methodology's own `E?`
separation: a claim about our observation never becomes a claim about
the system.

### Evidence fields for network observations

```text
observed_at_utc      when the request was made
requested_url
final_url
http_status
redirect_chain       NONE when there was none
evidence_role        official-project-page | official-source-location
observed             only what was directly seen
inference            why that entails the verdict
decision             PASS | FAIL
```

### Two times that must never merge

```text
E2-REP observation time
  now, during screening — provenance for "what does upstream
  designate as its source TODAY"

primary snapshot time
  2026-08-26T19:23:05Z — the sealed instant fixing which revision
  gets analyzed
```

Confirming today that upstream's canonical repository is `X` does
**not** license analyzing `X`'s current `HEAD`. Identifying the
location and fixing the revision are separate acts, and only the second
is already sealed.

## AMENDMENT (post-seal, corrective) — the existential gates are asymmetric for this run

**Status.** This is not part of the methodology sealed at `401924d`, and
must never be cited as though it were. It is a *post-seal corrective
amendment*, triggered mid-run by the discovery of an unoperationalized
negative branch. It is dated to its cause, not backdated to the seal.

**The gap.** Three of the screening gates are *existential*: each asks
whether at least one thing exists.

```text
E2-RULE  at least one externally authored validity requirement
E3       at least one stateful/temporal validity question
E4       at least one constructible property-level universe
```

For every one of them, PASS is decidable by exhibiting a single located
witness, and FAIL is a universal absence claim over everything the
project might contain. The sealed methodology specifies admissibility
in detail — Section 3.1's designation requirement, Section 3.2's
EN1-EN6 — and specifies no discovery procedure by which such an absence
could be established.

**Why E2-REP is not included.** E2-REP is the one gate whose search is
bounded by something sealed: its network-access contract fixes the
starting points and the navigation whitelist, so "what was there to
look at" is defined by upstream's own link structure rather than by us.
Its failure code in use, `E2REP-NO-SINGLE-CANONICAL-LOCATION`, is also
positive in shape — it records that several designations were found
with no primary among them, not that nothing was found. The remaining
E2-REP codes are absence-shaped but stay inside that bounded whitelist.
The other three gates have no equivalent contract, which is exactly the
difference.

This matters because the sealed rules explicitly admit runtime
construction — registry contents, interface dispatch, annotation
collection — as closure evidence. Any "closure argument" that confines
the search to prose documentation silently removes an evidence type the
seal allows, narrowing admissibility to make the negative tractable.
Two such arguments were attempted and withdrawn before this amendment.

**The amendment.** For this run only, E4 is asymmetric:

```text
E2-RULE   a concrete externally-authored validity witness is located
            -> PASS
          otherwise
            -> UNRESOLVED / PI-UNCLASSIFIED-SHAPE

E3        a concrete stateful/temporal validity witness is located
            -> PASS
          otherwise
            -> UNRESOLVED / PI-UNCLASSIFIED-SHAPE

E4        a positive construction is exhibited: a mechanism satisfying
          Section 3.2's EN1-EN6, or a source meeting Section 3.1's
          designation requirement, from which the property-level
          universe is ACTUALLY mechanically constructible
            -> PASS
          otherwise
            -> UNRESOLVED / PI-UNCLASSIFIED-SHAPE

in every UNRESOLVED case
    overall             = UNRESOLVED
    stop_gate           = the gate in question
    failure_code        = NONE
    protocol_issue_code = PI-UNCLASSIFIED-SHAPE
```

The three gates now share one principle: **existence is proved by
witness; absence without a preregistered complete discovery procedure
is not recorded as a property of the system.** That is the same
separation the methodology already makes with `E?` and with transport
indeterminacy, applied to the screening gates themselves.

`PI-UNCLASSIFIED-SHAPE` is reused deliberately rather than a new code
being minted. That code was sealed for exactly this situation — a real
screening outcome the sealed criteria do not describe — and inventing
fresh vocabulary after seeing results is the habit this amendment
exists to avoid.

No gate's PASS is relaxed. E2-RULE and E3 still require a quoted,
located witness, not the existence of documentation or of a test
directory. E4 still requires a positive construction: locating a
validator, a registry, or a plausible-looking mechanism is not one on
its own -- the mechanism must satisfy every one of EN1-EN6 and the
universe must actually be constructible from it.

**Effects, stated plainly:**

```text
creates no new eligible candidate
does not relax E4 PASS in any way
removes an E2-RULE / E3 / E4 FAIL capability this run could not support
increases the number of UNRESOLVED outcomes
```

The amendment reduces what this run claims and increases its recorded
uncertainty. That is the opposite direction from an adjustment made to
obtain a preferred result, and it is why it is admissible mid-run at
all.

**Future runs.** A run may restore FAIL at these gates by
preregistering a discovery procedure **before any candidate is seen**: a discovery
grammar, a source-traversal rule, language-specific probes, hit
adjudication against EN1-EN6, and an explicit termination/closure rule.
The hard part is defining discovery *completeness* in advance, so that
"our probes found nothing" cannot quietly become "nothing is there".
Designing that now, having already examined candidates, would fit the
probes to what has been seen and forfeit the preregistration that makes
the procedure worth anything.

## Controlled vocabularies

`upstream_resolution`:

```text
PASS            resolved to exactly one external system
FAIL_NONE       port metadata identifies no upstream system
FAIL_AMBIGUOUS  points at genuinely different systems, no basis to choose
DUPLICATE       resolved successfully, to a system already given a
                candidate_id by an earlier frame item
```

`failure_code` — one per sealed criterion, no catch-all:

```text
UR-NONE                              no upstream identified
UR-AMBIGUOUS                         multiple distinct plausible upstreams

E1-NONEXTERNAL                       external-authorship requirement failed

E2REP-NO-SOURCE                      no access to actual source representation
E2REP-NO-SINGLE-CANONICAL-LOCATION   not exactly one designated canonical location
E2REP-NO-STABLE-URL                  canonical location has no stable URL
E2REP-NO-SINGLE-TARGET-ID            not exactly one external target identifier

E2RULE-NO-VALIDITY-EVIDENCE          no externally authored validity evidence

E3-NO-STATEFUL-TEMPORAL-VALIDITY     no qualifying stateful/temporal
                                     validity observation

E4-NO-MECHANICAL-PRIMARY-UNIVERSE    no external/mechanical property-level
                                     universe constructible
```

**There is deliberately no `OTHER`.** A failure shape that fits none of
these is not squeezed into the nearest code; it is recorded as a
**protocol issue** and reported separately. A catch-all would quietly
absorb exactly the cases that indicate the sealed criteria are
incomplete — the thing most worth knowing.

`protocol_issue_code`, a separate column from `failure_code`:

```text
NONE
PI-TRANSPORT-INDETERMINATE   retries exhausted, endpoint state unknown
PI-UNCLASSIFIED-SHAPE        a real screening outcome that no sealed
                             criterion describes
```

## File schemas

`screening_frame_items.tsv`:

```text
frame_rank            1..128, the frozen order
port_path             from screening_set_128.txt
upstream_resolution   PASS | FAIL_NONE | FAIL_AMBIGUOUS | DUPLICATE
candidate_id          C001.. , or NONE if unresolved
duplicate_of          candidate_id if DUPLICATE, else NONE
terminal_status       ELIGIBLE | REJECTED | DUPLICATE | UNRESOLVED
stop_gate             gate at which screening stopped, or NONE
failure_code          from the vocabulary, or NONE
evidence_refs         semicolon-separated EV- ids
```

`screening_candidates.tsv`:

```text
candidate_id
first_frame_rank
frame_items                       all contributing ranks
external_upstream_name

E1  E2_REP  E2_RULE  E3  E4       PASS | FAIL | NOT_REACHED
overall                           ELIGIBLE | REJECTED
stop_gate
failure_code
evidence_refs

canonical_source_location         filled only if ELIGIBLE
external_target_identifier        else NOT_REACHED
primary_snapshot
authoritative_source_inventory_ref
enumerator_inventory_ref
completeness_class
tie_key
```

Fields from `canonical_source_location` down are inventory work that
the sealed methodology performs only for candidates surviving E1-E4;
rejected candidates carry `NOT_REACHED` there.

## Evidence log format

TSVs carry verdicts; `screening_evidence.md` carries grounds. Every
`PASS` and every `FAIL` cites at least one entry:

```text
## EV-C017-E2REP-01

Candidate: C017
Gate: E2-REP
Source:   exact URL, OpenBSD metadata path, or upstream location

Observed: only what was directly seen at that source

Inference: why that observation entails the verdict

Decision: PASS | FAIL
```

When a gate determination has a **negative component** -- E2-REP's
"exactly one", an E3 or E4 failure, or any verdict resting on something
not being there -- the entry additionally records, before the
investigation:

```text
Surfaces:  the surfaces that would carry the fact if it existed
Necessary because:
  [which question in the sealed criterion requires this surface]
  + [which already-observed upstream structure raises it]
  so the verdict cannot be settled without reading it.
```

Necessity is justified from the criterion and from structure already
lawfully observed -- never from the act of naming. A surface justified
this way and then found unobservable makes the gate UNRESOLVED; it is
not demoted to optional, and indirect inference from another surface
does not stand in for it.

**`Observed` and `Inference` stay separate**, for the same reason the
sufficiency gate distinguishes located evidence from traced reasoning:
a later reader must be able to see which parts were external fact and
which were our reading of it, without re-deriving the whole judgment.

## Invariants

```text
frame ledger rows                          == 128, always
candidate rows                             == count of distinct
                                              UR-PASS upstreams
budget slots consumed by duplicates        never refunded
gates after the first FAIL                 NOT_REACHED, never evaluated
failure codes outside the vocabulary       protocol issue, not OTHER
transport-level network indeterminacy      protocol issue, not a
                                           failure code
incidental content seen at E2-REP          logged, never used by
                                           E2-RULE / E3 / E4
E2-REP observation time                    never substituted for the
                                           sealed primary snapshot time
```
