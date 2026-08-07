# Chapter 09: Choosing Your Hitachi Vantara Path

## Learning Objectives

- Map roles (storage admin, storage architect, data-protection specialist, Ops Center engineer, Pentaho developer) to credentials.
- Sequence credentials — Qualification (HQT) first, then Certification (HCE).
- Decide between the storage and data (Pentaho) tracks.
- Place Hitachi Vantara in the storage and data ecosystem.

*Cert relevance: this chapter turns the program map ([Ch 1](01-the-hitachi-vantara-program.md)) into a personal plan and ends with a capstone.*

## Match the credential to your role

Hitachi Vantara certifications map to what you do:

| Your role | Start here | Then consider |
| --- | --- | --- |
| **Storage administrator** | Qualified Professional VSP 360 Storage Admin (HQT-6742) ([Ch 3](03-block-storage-administration.md)) | HCE Specialist storage |
| **Storage architect** | Professional (HQT) storage credentials | HCE Specialist / Expert ([Ch 2](02-hitachi-storage-and-vsp.md)) |
| **Data-protection specialist** | Data Protection & Replication ([Ch 5](05-data-protection-and-replication.md)) | Ops Center Protector |
| **Ops Center engineer** | Ops Center (Admin/Automator/Analyzer) ([Ch 6](06-hitachi-ops-center.md)) | HCE certification |
| **Pentaho developer** | Pentaho Data Integration ([Ch 7](07-pentaho-data-and-analytics.md)) | Pentaho Business Analytics |
| **Infrastructure specialist** | Converged / UCP ([Ch 8](08-converged-and-cloud.md)) | hybrid-cloud content |

The pattern: certify in the **track your role centers on**, starting at the **Qualification (HQT)** level and climbing to **Certification (HCE)** for depth. The lab builds a role-to-path planner.

## Sequence sensibly

A workable sequence for most people:

1. **Start with a Qualification (HQT) credential** in your area — Associate for foundational knowledge, Professional for role-based competency (e.g. VSP 360 Storage Administration, HQT-6742). These are **accessible** (some open-book), medium-stakes, and prove you know the platform.
2. **Deepen with a Certification (HCE) credential** — Specialist or Expert — the **high-stakes, proctored, hands-on** proof of real-world skill, when you are ready to demonstrate depth.
3. **Broaden across tracks** if useful — a storage admin who adds Data Protection and Ops Center is far more capable across the estate.
4. **Recertify** — credentials are valid **2–3 years**, so plan to renew as the platform evolves.

Because HQT exams are the accessible entry and HCE the rigorous depth, the natural climb is **HQT → HCE** within your track. The lab sequences a plan.

## Storage or data

A distinctive choice in Hitachi Vantara certification is **storage versus data (Pentaho)**:

- **Storage track** — VSP administration, data protection, Ops Center, converged infrastructure. This is **infrastructure/storage engineering** — the majority of the program and the classic Hitachi strength.
- **Data track** — **Pentaho** Data Integration and Business Analytics. This is **data engineering/analytics** — a different discipline (ETL and BI, not storage administration).

They are genuinely different careers, and Hitachi Vantara certifies both because it is a **storage-plus-data** company. Choose the track that matches your discipline; a few people bridge both (the storage that holds data and the pipelines that process it). The lab reflects the choice.

## Hitachi Vantara in the ecosystem

Hitachi Vantara competes in enterprise storage and data infrastructure:

- **Storage peers** — [NetApp (LXXXIV)](../../volume-084-netapp-certifications/README.md), [Dell (XXXII)](../../volume-032-dell-technologies-certifications/README.md), and [Everpure/Pure (CXXXVIII)](../../volume-138-everpure-purestorage-certifications/README.md): enterprise storage arrays; Hitachi's edge is **VSP reliability and storage virtualization**.
- **Data-protection peers** — [Rubrik (CXXX)](../../volume-130-rubrik-certifications/README.md), [Cohesity (CLVII)](../../volume-157-cohesity-certifications/README.md), [Commvault (CXXXIII)](../../volume-133-commvault-certifications/README.md): Hitachi protects with array-based replication.
- **Data peers** (Pentaho) — [Informatica (CLXV)](../../volume-165-informatica-certifications/README.md) and [Tableau (CLIV)](../../volume-154-tableau-certifications/README.md): data integration and BI.

Learning Hitachi Vantara is learning **enterprise data infrastructure** — the reliable storage that holds critical data, the protection that keeps it safe, the management that operates it, and (via Pentaho) the pipelines that turn it into insight. The capstone builds across it. The lab closes with it.

## Hands-On Lab

Python builds a role-to-path planner, then a capstone across storage, protection, and data. **Cost:** none.

### Lab 9.1 — Plan your Hitachi Vantara path

**Objective:** Turn a role into a sequenced credential plan.

```bash
python3 - <<'EOF'
ROLE_PATHS = {
  "Storage administrator": ["HQT: VSP 360 Storage Admin (Professional)", "HCE: storage Specialist"],
  "Data-protection specialist": ["HQT: Data Protection & Replication", "HCE: Ops Center Protector"],
  "Pentaho developer": ["Pentaho Data Integration", "Pentaho Business Analytics"],
  "Infrastructure specialist": ["HQT: Converged/UCP", "hybrid-cloud"],
}
def plan(role):
    steps = ROLE_PATHS[role]
    print(f"   ROLE: {role}")
    print(f"      1. START (Qualification/HQT or Pentaho): {steps[0]}")
    for i, s in enumerate(steps[1:], 2):
        print(f"      {i}. THEN (Certification/HCE or deeper): {s}")
    print("      note: HQT = medium-stakes (some open-book); HCE = high-stakes proctored; valid 2-3 yrs")
print("HITACHI VANTARA ROLE -> CREDENTIAL PATH:\n")
for role in ["Storage administrator", "Data-protection specialist", "Pentaho developer"]:
    plan(role); print()
print("Start with a QUALIFICATION (HQT) credential in your track, deepen with a CERTIFICATION")
print("(HCE) proctored credential, and choose the STORAGE track or the DATA (Pentaho) track by discipline.")
EOF
```

**Expected result:** A planner turning roles into sequenced paths — a storage admin starts with the HQT VSP 360 credential then an HCE storage Specialist; a Pentaho developer takes Data Integration then Business Analytics. The lesson is to start with a Qualification (HQT) credential in your track, deepen with a Certification (HCE), and choose storage versus data (Pentaho) by discipline.

**Cleanup:** None.

### Lab 9.2 — Capstone: data infrastructure end to end

**Objective:** Provision storage, protect it, manage via Ops Center, and process data with Pentaho.

```bash
python3 - <<'EOF'
# CAPSTONE: the Hitachi Vantara data-infrastructure stack, end to end
log = []
# 1) STORAGE: provision a VSP volume (pool -> LDEV -> host), thin + tiered
log.append("STORAGE (VSP 360): provisioned 500GB thin LDEV -> db-server (flash tier, RAID-6)")
# 2) PROTECT: local snapshot + remote async replication for DR
log.append("PROTECT: Thin Image snapshot (local) + Universal Replicator to site B (async DR, small RPO)")
# 3) OPS CENTER: automate + analyze the estate
log.append("OPS CENTER: Automator provisioned to a gold template; Analyzer forecasts pool full in 30 days")
# 4) OBJECT + CLOUD: archive cold data, tier to cloud
log.append("OBJECT (Content Platform): archived backups with WORM retention; cold objects tiered to cloud (S3)")
# 5) PENTAHO: integrate + analyze the data
log.append("PENTAHO: PDI pipeline integrates the data; Business Analytics dashboards it for the business")

print("CAPSTONE — Hitachi Vantara data infrastructure end to end:\n")
for step in log: print(f"   {step}")
print()
print("STORAGE (VSP) holds the data on redundant enterprise arrays; PROTECT (snapshots + replication)")
print("keeps it safe for DR; OPS CENTER automates + analyzes the estate; OBJECT storage archives it")
print("(WORM, cloud-tiered); and PENTAHO integrates + analyzes it. Hold -> protect -> manage -> archive")
print("-> analyze — enterprise DATA INFRASTRUCTURE, and what this volume's certifications prepare you to run.")
EOF
```

**Expected result:** A capstone provisioning VSP storage, protecting it with snapshots and replication, managing it via Ops Center automation/analytics, archiving to object storage with cloud tiering, and processing the data with Pentaho. The lesson synthesizes the volume: Hitachi Vantara spans the whole data-infrastructure lifecycle — hold (storage), protect (replication), manage (Ops Center), archive (object/cloud), and analyze (Pentaho) — which the storage and data certification tracks prepare you to run.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Roles mapped to credentials — storage admin/architect, data-protection, Ops Center, Pentaho, infrastructure.
- [ ] A sensible sequence chosen — Qualification (HQT) first, then Certification (HCE), broaden and recertify.
- [ ] The storage-vs-data choice made — infrastructure/storage engineering versus Pentaho data engineering/analytics.
- [ ] Hitachi Vantara placed in the ecosystem — enterprise data infrastructure: storage, protection, management, and data.

## See also

- [Chapter 01 — The Hitachi Vantara Certification Program](01-the-hitachi-vantara-program.md) — the categories and levels this plan draws on.
- [Volume LXXXIV — NetApp](../../volume-084-netapp-certifications/README.md) and [Volume XXXII — Dell](../../volume-032-dell-technologies-certifications/README.md) — storage peers.
- [Volume CLXV — Informatica](../../volume-165-informatica-certifications/README.md) — a data-integration peer (Pentaho's space).
