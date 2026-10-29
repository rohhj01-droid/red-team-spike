# Pin record -- EXPLORATORY C084 study (X4a)

EXPLORATORY. This record belongs to the exploratory C084 study (design
`docs/superpowers/specs/2026-10-29-phase3-5-exploratory-c084-design.md`,
sealed `984f0c5`), Section 4.2. It pins the tree that every later step
of the study reads. Every value below was printed by
`phase3_5/exploratory/tools/snapshot.py` (commit `d6501f7`) or by git,
and is reproduced here as printed.

## 1. Fetch (Section 4.2 step 1)

```text
2026-10-29T05:59:43Z  git init phase3_5/exploratory/target/crispy-doom
                      git -C phase3_5/exploratory/target/crispy-doom config core.autocrlf false
                      git -C phase3_5/exploratory/target/crispy-doom remote add origin https://github.com/fabiangreffrath/crispy-doom
                      git -C phase3_5/exploratory/target/crispy-doom fetch --depth 1 origin 7775ef82d1e9dfd50eb9d2824acefaeff7247458
                      git -C phase3_5/exploratory/target/crispy-doom checkout --detach FETCH_HEAD
2026-10-29T05:59:47Z  done
```

The host accepted the depth-1 fetch of the bare commit id; the archive
fallback of Section 4.2 step 1 was not needed. The checkout holds one
commit object, the pinned commit itself (`git log --oneline | wc -l`
= 1); its message was not displayed.

## 2. Identity (step 2)

```text
git rev-parse HEAD   7775ef82d1e9dfd50eb9d2824acefaeff7247458   = the revision
git ls-files | wc -l 801
```

## 3. The ten pinned digests (step 3)

`python -I phase3_5/exploratory/tools/snapshot.py digest phase3_5/exploratory/target/crispy-doom`

| file | bytes | sha256 | pinned sha256 | match |
|---|---|---|---|---|
| README.md | 13111 | 583bbc60755242bcb97ade06666f90e1544240d41f4d9739514eb7cc6511d6d0 | 583bbc60755242bcb97ade06666f90e1544240d41f4d9739514eb7cc6511d6d0 | True |
| src/d_iwad.c | 26304 | 1cc2f0575aa23314de779ade8841c92fc619780caa5e9a982229407ddbb60b5e | 1cc2f0575aa23314de779ade8841c92fc619780caa5e9a982229407ddbb60b5e | True |
| src/d_iwad.h | 1745 | 6b66d804248617e3955737ace60e07894abc4eae612ac76a298e42da013de615 | 6b66d804248617e3955737ace60e07894abc4eae612ac76a298e42da013de615 | True |
| src/doom/d_main.c | 65708 | 6dd3658604fc1c093562bbb9c2d2e5a92401d81944e3a186745af85396ac17f6 | 6dd3658604fc1c093562bbb9c2d2e5a92401d81944e3a186745af85396ac17f6 | True |
| src/doom/g_game.c | 94495 | 09afab2ea0147fcfa6bb58ff99f87e6a47b7e4e8a8a30a36b8f68f7fd4674cb9 | 09afab2ea0147fcfa6bb58ff99f87e6a47b7e4e8a8a30a36b8f68f7fd4674cb9 | True |
| src/doom/m_menu.c | 88348 | 79e528eea3b40aa92e2461953aea257b6afa087fbc7936bd5ec96cc291e6a9a7 | 79e528eea3b40aa92e2461953aea257b6afa087fbc7936bd5ec96cc291e6a9a7 | True |
| src/doom/p_saveg.c | 39855 | 391525093535a2e893fa1873cb2a3e833f8ce8e82c6ee9b9c97d78f3b1dc1ae4 | 391525093535a2e893fa1873cb2a3e833f8ce8e82c6ee9b9c97d78f3b1dc1ae4 | True |
| src/heretic/d_main.c | 37580 | f189aef7e934a7a9569a8527374d6f51446adf703571a8746f1d70090bc40e84 | f189aef7e934a7a9569a8527374d6f51446adf703571a8746f1d70090bc40e84 | True |
| src/hexen/h2_main.c | 38148 | 29118382638044d7d5ebb7641a38280eee23e1ae7b99221ab86a3387ea20c610 | 29118382638044d7d5ebb7641a38280eee23e1ae7b99221ab86a3387ea20c610 | True |
| src/strife/d_main.c | 63255 | 5080ef9009672089b478850c929ac79320d73f909e8967d9c23e87368508da2e | 5080ef9009672089b478850c929ac79320d73f909e8967d9c23e87368508da2e | True |

```text
10 of 10 match
```

The tree on disk is the object EV-C084-PIN-01 describes.

## 4. Archive (step 4)

Fetched 2026-10-29T06:00:03Z from
`https://github.com/fabiangreffrath/crispy-doom/archive/7775ef82d1e9dfd50eb9d2824acefaeff7247458.tar.gz`
to `phase3_5/exploratory/target/archive.tar.gz` (git-ignored; listed,
not extracted).

```text
bytes=2648481 (MATCH pinned 2648481) sha256=4edfcde1c4f6f9292d673116f81ba40df6cf04033f17346131b4f2fe72fbce55 (MATCH pinned 4edfcde1c4f6f9292d673116f81ba40df6cf04033f17346131b4f2fe72fbce55) entries=832 (MATCH pinned 832)
```

The archive reproduced byte for byte, sixty days after the screening
retrieved it. Recorded as a Run 2 input (design Section 12 item 4).

## 5. Sealed-instant consistency check (step 5)

Queried 2026-10-29T06:00:05Z:
`GET https://api.github.com/repos/fabiangreffrath/crispy-doom/commits?sha=master&until=2026-08-26T19:23:05Z&per_page=1`
(the tool keeps the commit id and dates and discards the message).

```text
sha=3a39d0a53aaa52562f099a7c4fab649d8962d947 author_date=2026-08-24T16:33:06Z committer_date=2026-08-24T16:33:06Z -> DIFFERS revision 7775ef82d1e9dfd50eb9d2824acefaeff7247458
```

**DIFFERS.** Recorded as XQA-01. The revision does not change (Section
4.2 step 5): it is the object the screening record describes, and
Section 3 above shows the tree on disk is that object.

What this observation says and does not say. It says that master's
current history contains a commit dated 2026-08-24 that is not the
revision. It does not say which commit master pointed at on
2026-08-26T19:23:05Z: a commit whose committer date precedes an instant
can enter master's history after that instant (through a merge, for
one), and an observation made later cannot tell that case from the
other -- QA-28's point, met here in the data rather than closed.
Whether `3a39d0a5` is an ancestor or a descendant of the revision was
not queried: Section 5.1 admits the API for three purposes only, and
that is not one of them. The screening's own observation stands beside
this one: EV-C084-PIN-01 resolved `master` to the revision on
2026-08-30T06:09:46Z, four days after the sealed instant.

## 6. Summary

```text
revision      7775ef82d1e9dfd50eb9d2824acefaeff7247458   on disk, verified by 10/10 digests
archive       MATCH / MATCH / MATCH
sealed instant DIFFERS (XQA-01) -- not a snapshot of the sealed instant; see Section 5
fallback      not used
```
