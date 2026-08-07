# Chapter 01: The Hitachi Vantara Certification Program

## Learning Objectives

- Describe Hitachi Vantara as the data-infrastructure arm of Hitachi and where certification fits.
- Distinguish Qualification credentials (HQT exams) from Certification credentials (HCE exams).
- Map the four levels — Associate, Professional, Specialist, Expert.
- Understand the tracks and the exam mechanics (e.g. HQT-6742) and validity.

*Cert relevance: this chapter frames the whole program — the two credential categories, four levels, and tracks the rest of the volume develops.*

## Hitachi Vantara and its certifications

**Hitachi Vantara** is the **data-infrastructure** business of Hitachi — the company behind **enterprise storage**, data protection, infrastructure management, and data-and-analytics software. If a large enterprise needs highly reliable **block, file, and object storage**, replication and protection for it, tooling to manage it, and a platform to integrate and analyze data, Hitachi Vantara is one of the names that provides it. Its flagship is the **VSP — Virtual Storage Platform** ([Ch 2](02-hitachi-storage-and-vsp.md)) storage line, complemented by **Hitachi Ops Center** management ([Ch 6](06-hitachi-ops-center.md)) and **Pentaho** data software ([Ch 7](07-pentaho-data-and-analytics.md)).

The **Hitachi Vantara Certified Professional (HVCP)** program validates skill with these platforms — configuring and administering storage, protecting data, managing infrastructure, and working with Pentaho. Hitachi Vantara sits alongside the storage and data vendors this shelf covers ([NetApp LXXXIV](../../volume-084-netapp-certifications/README.md), [Dell XXXII](../../volume-032-dell-technologies-certifications/README.md), [Everpure CXXXVIII](../../volume-138-everpure-purestorage-certifications/README.md)). The lab builds the program map.

## Two credential categories

The HVCP program's distinctive structure is **two categories** of credential, distinguished by **exam type and rigor**:

- **Qualification Credentials** — earned through **HQT-xxxx** exams. These are **medium-stakes** tests of **foundational and role-based knowledge**; some are **open-book and unproctored**, others closed-book and proctored online. They validate that you **know** the platform and role.
- **Certification Credentials** — earned through **HCE-xxxx** exams. These are **high-stakes, closed-book, proctored** exams (onsite or remote) designed to validate **hands-on, real-world skills** beyond classroom knowledge. They validate that you can **do** the work at depth.

Read the split as **know it (HQT / Qualification)** versus **prove you can do it under exam conditions (HCE / Certification)**. The HQT exams are the accessible entry; the HCE exams are the rigorous, expert-level proof. Knowing which category a credential is — and thus its rigor — is the first thing to understand. The lab models the two categories.

## The four levels

Across the two categories sit **four levels** of increasing depth:

| Category | Level | Meaning |
| --- | --- | --- |
| **Qualification (HQT)** | **Associate** | Foundational knowledge of a product/area |
| **Qualification (HQT)** | **Professional** | Role-based competency (e.g. VSP 360 Storage Administration) |
| **Certification (HCE)** | **Specialist** | Deep, hands-on, proctored competency in a domain |
| **Certification (HCE)** | **Expert** | The highest tier — expert, hands-on mastery |

The progression is **Associate → Professional → Specialist → Expert**, moving from knowing to doing to mastery, and from medium-stakes HQT exams to high-stakes HCE exams. You climb the levels in the **track** your role centers on. The lab maps the levels.

## Tracks, mechanics, and validity

Certifications span Hitachi Vantara's **product domains** (tracks):

- **Block Storage** — VSP 5000, VSP One Block, VSP Midrange, VSP 360 ([Ch 3](03-block-storage-administration.md)).
- **File Storage** (VSP One File) and **Object Storage** (Content Platform) ([Ch 4](04-file-and-object-storage.md)).
- **Data Protection & Replication** ([Ch 5](05-data-protection-and-replication.md)).
- **Hitachi Ops Center** — Administration, Automation, Protection, Analyzer ([Ch 6](06-hitachi-ops-center.md)).
- **Pentaho** — Business Analytics and Data Integration ([Ch 7](07-pentaho-data-and-analytics.md)).
- **Infrastructure / converged (UCP)** ([Ch 8](08-converged-and-cloud.md)).

**Exam mechanics** are illustrated by the **HQT-6742** exam (Qualified Professional VSP 360 Storage Administration): **35 questions, 60 minutes, 65% to pass, $100**. **Credentials are valid 2–3 years** depending on the track, so recertification keeps them current with the platform. The lab records the tracks and mechanics.

## Hands-On Lab

Python models the program: categories, levels, tracks, and mechanics. **Cost:** none.

### Lab 1.1 — Map the categories and levels

**Objective:** Record the HQT/HCE split and the four levels.

```bash
python3 - <<'EOF'
PROGRAM = {
  "Qualification (HQT-xxxx exams)": {
    "rigor": "medium-stakes; foundational/role-based; some open-book/unproctored",
    "levels": ["Associate", "Professional"],
    "validates": "you KNOW the platform and role",
  },
  "Certification (HCE-xxxx exams)": {
    "rigor": "high-stakes; closed-book; PROCTORED; hands-on real-world skills",
    "levels": ["Specialist", "Expert"],
    "validates": "you can DO the work at depth",
  },
}
print("HITACHI VANTARA CERTIFIED PROFESSIONAL (HVCP) — two categories, four levels:\n")
for cat, d in PROGRAM.items():
    print(f"   {cat}")
    print(f"      rigor:     {d['rigor']}")
    print(f"      levels:    {' -> '.join(d['levels'])}")
    print(f"      validates: {d['validates']}\n")
print("Progression across both: Associate -> Professional (HQT) -> Specialist -> Expert (HCE).")
print("Read it as KNOW IT (HQT/Qualification) vs PROVE YOU CAN DO IT proctored (HCE/Certification).")
print("Credentials are valid 2-3 years depending on the track.")
EOF
```

**Expected result:** A map of the two credential categories — Qualification (HQT exams, Associate/Professional, medium-stakes, some open-book) and Certification (HCE exams, Specialist/Expert, high-stakes, proctored, hands-on) — and the Associate→Professional→Specialist→Expert progression. The lesson is that HVCP splits into "know it" HQT qualifications and "prove you can do it" proctored HCE certifications, across four levels, valid 2–3 years.

**Cleanup:** None.

### Lab 1.2 — Map the tracks and exam mechanics

**Objective:** Record the product tracks and the representative HQT-6742 mechanics.

```bash
python3 - <<'EOF'
TRACKS = {
  "Block Storage":       "VSP 5000 / VSP One Block / VSP Midrange / VSP 360",
  "File Storage":        "VSP One File",
  "Object Storage":      "Content Platform (HCP)",
  "Data Protection":     "replication (ShadowImage / TrueCopy / Universal Replicator)",
  "Hitachi Ops Center":  "Administration / Automation / Protection / Analyzer",
  "Pentaho":             "Business Analytics / Data Integration",
  "Infrastructure/UCP":  "converged / hyperconverged",
}
HQT_6742 = {"exam": "HQT-6742 (Qualified Professional VSP 360 Storage Administration)",
            "questions": 35, "minutes": 60, "passing": "65%", "cost": "$100"}
print("HITACHI VANTARA CERTIFICATION TRACKS:\n")
for track, prod in TRACKS.items():
    print(f"   {track:20} {prod}")
print("\nRepresentative exam mechanics:")
for k, v in HQT_6742.items():
    print(f"   {k:10}: {v}")
print()
print("Certify in the TRACK your role centers on (block/file/object storage, protection, Ops")
print("Center, Pentaho, or converged infrastructure). HQT exams like HQT-6742 are 35 Q / 60 min /")
print("65% / $100 -> a Qualified Professional credential; HCE certifications go deeper, proctored.")
EOF
```

**Expected result:** A track map (block/file/object storage, data protection, Ops Center, Pentaho, converged infrastructure) with the HQT-6742 mechanics (35 questions, 60 minutes, 65%, $100). The lesson is that HVCP certifications span Hitachi Vantara's product domains, you certify in the track matching your role, and HQT qualification exams like HQT-6742 are short and accessible while HCE certifications are deeper and proctored.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Hitachi Vantara placed — the data-infrastructure arm of Hitachi (VSP storage, Ops Center, Pentaho).
- [ ] The two categories understood — Qualification (HQT, know it) and Certification (HCE, proctored, do it).
- [ ] The four levels understood — Associate, Professional (HQT); Specialist, Expert (HCE).
- [ ] The tracks and mechanics recorded — storage/protection/Ops Center/Pentaho; HQT-6742 (35Q/60min/65%/$100); 2–3-year validity.

## See also

- [Volume LXXXIV — NetApp](../../volume-084-netapp-certifications/README.md), [Volume XXXII — Dell](../../volume-032-dell-technologies-certifications/README.md), and [Volume CXXXVIII — Everpure](../../volume-138-everpure-purestorage-certifications/README.md) — enterprise-storage peers.
- [Chapter 02 — Hitachi Storage and the VSP Platform](02-hitachi-storage-and-vsp.md).
