# Phase 3.5 Run 2 -- Candidate Frame Enumeration (re-executed)

Second execution of the candidate discovery frame sealed in
`docs/superpowers/specs/2026-08-27-phase3-5-external-validation-methodology-design.md`
(`401924d`), under the Run 2 preregistration (`4c7e315`, Section 3) and
the contract (`SCREENING_CONTRACT.md`). Run 1's enumeration is
`phase3_5/FRAME_ENUMERATION.md` (2026-08-26); this document records the
re-execution and the item-by-item comparison. Nothing here screens,
ranks or selects.

## Provenance

```text
Enumeration source
  official OpenBSD 7.9 ports.tar.gz release artifact
  https://cdn.openbsd.org/pub/OpenBSD/7.9/ports.tar.gz

Frame source revision (membership-determining)
  SHA256 937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db   = the sealed value
  size   56386078 bytes                                  = the sealed value
  published checksum line (https://cdn.openbsd.org/pub/OpenBSD/7.9/SHA256): SHA256 (ports.tar.gz) = 937aef3d19bc288a838bfa168733872c1a33064db7fe00caf60ea29d9476c6db

Retrieved at (UTC)          2026-10-29T12:57:54Z   (HTTP 200)
Enumeration executed at     2026-10-29T13:03:22Z
Tool                        phase3_5/run2/tools/frame.py (committed before this fetch)
```

The artifact was hashed before extraction; only `*/Makefile`,
`*/distinfo`, `*/pkg/DESCR` and `infrastructure/**` were extracted
(31077 files), into the git-ignored `target/` directory. The Run 2
enumeration timestamp is provenance only; snapshots are pinned at
observation time (contract Section 10).

## Query as executed

Membership by each port Makefile's `CATEGORIES` assignment containing
the token `games` (`^CATEGORIES[ \t]*=`, split on whitespace), port
directory relative to the ports root, byte-wise ascending unique
(`frame.enumerate_games`).

## Results

```text
frame items (CATEGORIES include `games`)        477
  outside the games/ directory                  79
  path depth 3                                  64
screening budget (sealed)                       128
items entering screening                        128
category prefixes inside the screening set      devel 3, editors 1, emulators 11, games 113

comparison with Run 1's screening_set_128.txt   IDENTICAL, 128 of 128
```

## Files

- `raw_frame_all.txt` -- all frame items, byte-wise ascending
- `screening_set_128.txt` -- the first 128, the screening set (identical to Run 1's)

## What has and has not happened

Enumerated: the frame, again, from the same bytes. Not done: any
screening, upstream resolution, inspection of a port's contents or
upstream, ranking or selection. Screening begins from
`screening_set_128.txt` in its recorded order, in batches of eight.
