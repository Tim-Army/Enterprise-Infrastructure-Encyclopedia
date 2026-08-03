# Chapter 04: Data Platform Certifications

## Learning Objectives

- Map the Db2 and Informix certification family across z/OS and LUW.
- Understand the split between Db2 for z/OS and Db2 (LUW), and where the fundamentals certifications sit.
- Complete runnable SQL/administration labs on free Db2 Community Edition.

## The data-platform portfolio

| Certification | Catalog code | Platform |
|:---|:---|:---|
| Associate Certified DBA - Db2 12 for z/OS Fundamentals | Cert-C8003803 | Db2 for z/OS (fundamentals) |
| Certified Administrator - Db2 12 for z/OS | Cert-C0005400 | Db2 for z/OS |
| Certified Db2 13 for z/OS Database Administrator - Associate | Cert-C9006800 | Db2 13 for z/OS |
| Certified Db2 13 for z/OS Database Administrator - Professional | Cert-C9006700 | Db2 13 for z/OS |
| Certified Db2 v12.1 Database Administrator - Professional | Cert-C9009700 | Db2 (LUW) |
| Certified Informix v15.0 Database Administrator - Professional | Cert-C9009600 | Informix |

Two Db2 lines to keep straight: **Db2 for z/OS** (the mainframe database — the C9006700/C9006800/C0005400/C8003803 credentials) and **Db2** (Linux/UNIX/Windows, "LUW" — the v12.1 credential C9009700). The SQL overlaps; the administration, catalog, and utilities differ. **Informix** is a separate engine with its own DBA credential.

## Hands-On Lab

**Shared prerequisites** — free **Db2 Community Edition** container (`icr.io/db2_community/db2`) or `ibmcom/db2`; Docker/Podman. The LUW labs run against it directly; z/OS-specific items are noted design-level. **Cost:** none.

### Lab 4.1 — Stand up Db2 and connect (Db2 LUW DBA)

**Objective:** Get a running database — the LUW administrator's ground zero.

```bash
docker run -itd --name db2lab --privileged=true -p 50000:50000 \
  -e LICENSE=accept -e DB2INST1_PASSWORD=labpass -e DBNAME=LABDB \
  icr.io/db2_community/db2
sleep 90
docker exec -it db2lab su - db2inst1 -c "db2 connect to LABDB"
```

**Expected result:** `Database Connection Information` with `LABDB` — a live Db2 you administer for the rest of the chapter. The container is the LUW exam's honest lab: real `db2` CLP, real catalog.

**Negative test:** Connect before initialization finishes (skip the sleep) — connection refused; Db2 needs its startup time, a real operational detail.

**Cleanup:** `docker rm -f db2lab` at the chapter's end.

### Lab 4.2 — Tables, tablespaces, and the catalog (DBA core)

**Objective:** Create objects and read the catalog the way the DBA exams expect.

```bash
docker exec -it db2lab su - db2inst1 -c "db2 connect to LABDB && \
  db2 'CREATE TABLE staff(id INT NOT NULL PRIMARY KEY, name VARCHAR(40), dept INT)' && \
  db2 'INSERT INTO staff VALUES (1,''Ada'',10),(2,''Grace'',20)' && \
  db2 'SELECT tabname, card FROM syscat.tables WHERE tabschema=''DB2INST1'' AND tabname=''STAFF'''"
```

**Expected result:** The `STAFF` table created, rows inserted, and `SYSCAT.TABLES` reporting it — the system catalog is where DBAs (and the exam) confirm structure; `card` shows the row estimate once statistics run.

**Negative test:** Query `card` before `RUNSTATS` — it reads `-1` (no statistics); optimizer questions on the exam hinge on knowing statistics must be collected.

**Cleanup:** Table dropped with the container.

### Lab 4.3 — Backup and recovery (DBA core)

**Objective:** Exercise the recovery vocabulary every Db2 DBA exam tests.

```bash
docker exec -it db2lab su - db2inst1 -c "db2 connect to LABDB && \
  db2 'BACKUP DATABASE LABDB TO /database/backup' && \
  db2 'LIST HISTORY BACKUP ALL FOR LABDB' | head -20"
```

**Expected result:** A backup image written and recorded in the recovery history — `BACKUP`/`RESTORE`/`ROLLFORWARD` plus circular vs archive logging are the recovery core; the history file is the audit trail.

**Negative test:** Attempt an online backup in **circular logging** mode — Db2 refuses; online backup and rollforward require **archive logging**, a distinction the exams reliably probe.

**Cleanup:** Backups removed with the container.

### Lab 4.4 — Db2 for z/OS differences (z/OS DBA)

**Objective:** Name what the z/OS credentials add over LUW.

```text
db2 z/OS> objects: databases contain tablespaces; SYSIBM catalog; DBRM/plan/package bind flow
db2 z/OS> utilities: LOAD, REORG, RUNSTATS, COPY, RECOVER run as z/OS jobs (JCL), not CLP commands
db2 z/OS> access: through subsystems; workload managed by z/OS WLM
```

**Expected result:** The z/OS-specific surface — bind/package/plan, JCL-driven utilities, subsystem and WLM concepts — that the four z/OS credentials test and the LUW credential does not. Same SQL, different operations.

**Negative test:** Assuming `db2 BACKUP DATABASE` (a LUW CLP command) on z/OS — there it is a utility job; conflating the two platforms is the trap.

**Cleanup:** None (design).

### Lab 4.5 — Informix positioning (Informix DBA)

**Objective:** Place Informix relative to Db2.

```text
informix> separate engine (OLTP + time-series/IoT strength); dbaccess CLI, onstat monitoring,
          onmode admin, chunks/dbspaces for storage — its own administration vocabulary
```

**Expected result:** Informix as a distinct product with its own tooling (`dbaccess`, `onstat`, `onmode`, dbspaces/chunks) — the v15.0 DBA credential is not a Db2 variant, and the exam vocabulary differs accordingly.

**Negative test:** Bringing Db2 `db2` CLP commands to an Informix exam — wrong engine; the storage and admin models don't transfer.

**Cleanup:** `docker rm -f db2lab` to finish the chapter.

## Summary and Completion Checklist

- [ ] Db2 for z/OS vs Db2 LUW split, and the fundamentals credentials, mapped.
- [ ] Live Db2 Community Edition: tables, catalog, backup/recovery drilled.
- [ ] Archive-vs-circular logging and RUNSTATS distinctions internalized.
- [ ] z/OS utility/bind model and Informix's separate tooling understood.
