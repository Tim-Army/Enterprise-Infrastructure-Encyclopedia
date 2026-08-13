# Chapter 08: Systems and Asset Management Certifications

## Learning Objectives

- Map the systems portfolio: z/OS, AIX, IBM i, and WebSphere.
- Map the asset-management portfolio: Maximo and TRIRIGA, plus the retiring Engineering pair.
- Complete walkthrough labs on the concepts these certifications test.

## The systems portfolio

| Certification | Catalog code | Platform |
|:---|:---|:---|
| Certified z/OS v3.x Administrator - Professional | Cert-C9007900 | z/OS mainframe OS |
| AIX v7.3 Administrator Specialty | Cert-S2113000 | AIX (Power UNIX) |
| Certified Developer - IBM i 7.x | Cert-C9002700 | IBM i (Power) |
| Certified Administrator - WebSphere Application Server ND v9.0.5 | Cert-C9006100 | WebSphere (Java app server) |
| Certified Solution Architect - WebSphere Hybrid Edition V5.0 PLUS RH OpenShift Admin | Cert-C0006421 | WebSphere + OpenShift |

## The asset-management portfolio

| Certification | Catalog code | Product |
|:---|:---|:---|
| Certified Administrator - Maximo Manage v8.x | Cert-C9002600 | Maximo (EAM) |
| Certified Deployment Professional - Maximo Manage v8.0 | Cert-C4018302 | Maximo deployment |
| Certified Maximo Manage v9 Work Management - Associate | Cert-C9008600 | Maximo v9 (work mgmt) |
| Certified Maximo Manage v9.1 Inventory Management - Associate | Cert-C9009300 | Maximo v9.1 (inventory) |
| Certified Maximo Real Estate and Facilities v9.1 Space Management - Associate | Cert-C9009500 | Maximo RE&F |
| Certified Associate Application Developer - TRIRIGA Application Platform V3.2.1 | Cert-24014601 | TRIRIGA (IWMS) |
| *Retiring soon:* Engineering Requirements Mgmt DOORS Next v7.x Specialty | Cert-S2112000 | DOORS Next (RM) |
| *Retiring soon:* Engineering Test Management v7.x Specialist | Cert-S2112200 | ETM (test mgmt) |

Maximo shows IBM's modern **modular** certification design: v9/v9.1 splits into per-discipline Associate credentials (Work Management, Inventory, Space Management) rather than one monolithic exam.

## Hands-On Lab

Walkthroughs use free primitives; the platforms are commercial (design-level). **Cost:** none.

### Lab 8.1 — z/OS mental model (z/OS Administrator)

**Objective:** Name the z/OS constructs the exam assumes.

```text
z/OS> address spaces (jobs), JCL (job control language) submits batch work, JES2/3 spooling,
      SMF (system activity records), RACF (security), SDSF (operator/spool view), Parmlib/Proclib config
```

**Expected result:** The z/OS vocabulary — JCL, JES, SMF, RACF, SDSF, Parmlib — that the Administrator exam is built on; the mainframe is a different operational world from UNIX/Linux, and the exam tests its terms.

**Negative test:** Bringing Linux `systemd`/`cron` mental models to z/OS batch — the concepts (started tasks, JCL jobs, JES initiators) map differently; conflating them is the trap.

**Rollback:** None (design).

### Lab 8.2 — AIX/LVM (AIX Administrator Specialty)

**Objective:** Exercise AIX's storage model, which its labs mirror in Linux LVM terms.

```bash
# AIX uses PV -> VG -> LV -> filesystem. The concept, in portable terms:
echo "AIX: hdisk (PV) -> volume group (VG) -> logical volume (LV) -> JFS2 filesystem"
echo "commands: lspv, lsvg, lslv, mklv, crfs, mount ; ODM stores device config"
```

**Expected result:** The AIX storage stack (PV→VG→LV→JFS2) and its command set (`lspv`, `lsvg`, `mklv`, `crfs`) plus the **ODM** device database — the AIX Specialty exam's administration core, conceptually like Linux LVM but with AIX-specific tooling.

**Negative test:** Assuming Linux `lvcreate`/`/etc/fstab` on AIX — the commands and the ODM-based config differ; the Specialty exam tests the AIX specifics.

**Rollback:** None (design).

### Lab 8.3 — IBM i (IBM i Developer)

**Objective:** State what makes IBM i distinct.

```text
IBM i (7.x)> integrated OS+DB (Db2 for i built in), objects & libraries (not files/dirs) as the model,
             CL commands, control language programs, and RPG/COBOL or SQL for application development
```

**Expected result:** IBM i as an integrated platform with the database built into the OS, a library/object model, CL for control, and RPG/SQL for apps — the Developer exam tests this object-based world, unlike any of the other systems.

**Negative test:** Treating IBM i like AIX (it is not UNIX) — object/library vs file/directory is the fundamental difference the exam probes.

**Rollback:** None (design).

### Lab 8.4 — WebSphere topology (WebSphere ND Administrator)

**Objective:** Model the Network Deployment cell the exam centers on.

```text
websphere nd (v9.0.5)> cell -> deployment manager (dmgr) -> node agents -> managed servers/clusters;
                       apps deployed to clusters; the dmgr is the admin control point
```

**Expected result:** The ND topology — cell, deployment manager, node agents, clustered application servers — the Administrator exam's core; the Hybrid Edition PLUS credential adds OpenShift (the Red Hat exam) as WebSphere modernizes onto containers.

**Negative test:** Confusing a base (standalone) WAS profile with an ND cell — clustering and central administration are ND's point, and the exam distinguishes them.

**Rollback:** None (design).

### Lab 8.5 — Maximo modular work management (Maximo Associate)

**Objective:** Exercise the EAM work-order model the modular exams test.

```python
python3 - <<'EOF'
# Maximo's core object: the work order through its lifecycle
statuses = ["WAPPR","APPR","INPRG","COMP","CLOSE"]  # waiting-approval -> approved -> in-progress -> complete -> closed
wo = {"id":1001,"asset":"PUMP-07","status":"WAPPR"}
for s in statuses[1:]:
    wo["status"]=s; print(f"WO {wo['id']} on {wo['asset']}: {s}")
EOF
```

**Expected result:** A work order walking `WAPPR → APPR → INPRG → COMP → CLOSE` against an asset — Maximo's work-order lifecycle, tied to assets, locations, and inventory. The v9/v9.1 Associate credentials each own one discipline (Work Management, Inventory, Space Management) of this model.

**Negative test:** Skipping approval (`WAPPR → INPRG`) where the workflow requires it — Maximo's status flow and approvals are configurable controls the exam tests.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.6 — The retiring Engineering pair

**Objective:** Note the DOORS Next / ETM credentials' status.

```text
retiring> DOORS Next v7.x (requirements management) Specialty and Engineering Test Management v7.x
          Specialist are flagged retiring — valid to hold, but not to target for a new plan
```

**Expected result:** Awareness that the Engineering Lifecycle Management credentials are winding down — [Chapter 09](09-red-hat-combos-choosing-currency-career.md) folds the retiring-soon list into the currency plan.

**Negative test:** Building a certification roadmap around a retiring credential — the catalog's "Retiring soon" flag is the signal to redirect.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Systems portfolio (z/OS, AIX, IBM i, WebSphere) mapped with each platform's distinct model.
- [ ] Maximo modular work-management model and TRIRIGA placement understood.
- [ ] The retiring Engineering pair flagged for the currency plan.
