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
`NOT_REACHED`, never evaluated. Only three states exist:

```text
PASS  |  FAIL  |  NOT_REACHED
```

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
```
