# Phase 3.5 Candidate Frame Enumeration (sealed record)

First execution of the candidate discovery frame sealed in
`docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`
at commit `401924d`. This document records what the frozen query
returned. It does **not** screen, rank, or select anything.

## Provenance

```text
Sealed methodology commit
  401924dec7bf63fd1cec4ed7c7db7edf8f8695d2

Enumeration source
  official OpenBSD 7.9 ports.tar.gz release artifact
  https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz

Frame source revision (membership-determining)
  SHA256 937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db
  size   56386078 bytes
  Last-Modified 2026-05-06T12:39:58Z (as served)
  cross-checked against OpenBSD's published SHA256 for the release;
  re-verified byte-identical immediately before extraction

Enumeration execution timestamp
  2026-08-26T19:23:05Z
```

Per the sealed spec this timestamp is also the fixed instant at which
each candidate's **primary snapshot** is taken, if and when screening
reaches that step.

## Query as executed

The sealed query is *all ports whose OpenBSD-assigned categories
include `games`* — not the contents of the `games/` directory. Those
are materially different sets, and the distinction was executed
faithfully: membership was determined by each port Makefile's
`CATEGORIES` variable.

```text
grep -rH -E "^CATEGORIES[[:space:]]*=" --include=Makefile .
  → split the assigned value on whitespace
  → include the port directory iff `games` appears as a token
  → strip /Makefile, make path relative to the ports root
  → LC_ALL=C sort -u   (byte-wise ascending, per the sealed order)
```

`CATEGORIES` is defined in 8819 Makefiles across the tree, and none of
them continue the assignment across a line break, so single-line
parsing is complete rather than approximate.

## Results

```text
frame items (port directories whose CATEGORIES include `games`)   477
  of which outside the games/ directory                            79
  path depth 2 (category/port)                                    413
  path depth 3 (category/parent/port)                              64

parent/child overlap among frame items                              0
screening budget                                                  128
items entering screening                                          128
items beyond the budget, never to be examined                     349
```

**79 of 477 lie outside `games/`** — reading the category variable
rather than listing the directory changed the frame by roughly a
sixth. Their category prefixes inside the screening set are `games`
(113), `emulators` (11), `devel` (3), `editors` (1).

**No collapsing was required.** The port-directory granularity rule
exists to prevent one upstream system from occupying several frame
slots via flavors or subpackages. Neither arose here: flavors are
`FULLPKGPATH` suffixes rather than directories, so they never appear
as separate paths; and no depth-2 frame item is a parent of any
depth-3 frame item (overlap count 0), because the intermediate
directories (`games/alephone`, `games/nethack`, `x11/gnome`, …) are
`SUBDIR` containers that define no `CATEGORIES` of their own and so
were never matched. All 477 items are distinct leaf ports.

## Budget boundary

The budget is a workload ceiling fixed before enumeration, not a
sample size. The cutoff fell here:

```text
126  games/fire
127  games/flare
128  games/fnaify-extralibs
---- budget cutoff ----
129  games/foobillard        ← outside the frame's screening set
130  games/fotaq
131  games/freebee
```

Items 129-477 are recorded in `raw_frame_all.txt` for auditability but
are **not** screening candidates. If no eligible candidate is found
within the 128, that is this run's candidate-discovery outcome; the
129th is not examined.

## Files

- `raw_frame_all.txt` — all 477 frame items, byte-wise ascending
- `screening_set_128.txt` — the first 128, the screening set

## What has and has not happened

Enumerated: the frame. Recorded: its provenance, ordering, and
boundary. **Not** done: any E1-E4 screening, any upstream resolution,
any inspection of a port's contents or upstream project, any ranking,
any target selection. Screening begins from
`screening_set_128.txt` in its recorded order.
