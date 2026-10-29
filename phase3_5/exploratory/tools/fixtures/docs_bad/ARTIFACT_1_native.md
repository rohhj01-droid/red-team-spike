# Artifact 1 -- native description -- EXPLORATORY fixture

No Phase 3 role name appears in this file.

## NC-01 -- the fixture registry
source observation ids: E001-001
native state/data involved: a static table of names (MonitorState)
writers / creation points: compiled in, src/a.c:1
updates / invalidation paths: none at run time
readers / consumption points: lookup in src/a.c:20
lifetime / persistence / reset behavior: process lifetime
relevant transitions: startup
supporting source-code/docs evidence: src/a.c:1-25
remaining native-level uncertainty: none
lineage: inherited -- no [crispy] marker near src/a.c:1
### Sufficiency
Q1 created: the identified name -- src/a.c:20
Q2 written: nowhere; the table is compiled in -- src/a.c:1
Q3 lifetime: N/A: no persistent value is created -- src/a.c:20
Q4 readers: the startup path -- src/a.c:22
Q5 after consumption: disappears with the call -- src/a.c:25
Status: RESOLVED

## NC-02 -- a case left open
source observation ids: E002-001
native state/data involved: a flag
writers / creation points: src/b.c:3
updates / invalidation paths: src/b.c:9
readers / consumption points: src/b.c:12
lifetime / persistence / reset behavior: unknown
relevant transitions: load
supporting source-code/docs evidence: src/b.c:1-15
remaining native-level uncertainty: where the flag is reset
lineage: C084-own -- [crispy] marker at src/b.c:2
### Sufficiency
Q1 created: a flag -- src/b.c:3
Q2 written: src/b.c:3
Q3 lifetime: N/A: not located -- src/b.c:9
Q4 readers: src/b.c:12
Q5 after consumption: not located -- src/b.c:12
Status: E? (Q3, Q5)
