# Chapter 01: The Nutanix Certification Program

## Learning Objectives

- Describe the Nutanix Cloud Platform and what its certifications validate.
- Identify the four certification levels and their tracks.
- Explain the exam format, delivery, fees, and three-year validity.
- Locate the exam blueprint guides and Community Edition for practice.
- Verify program facts from the authoritative source.

## Theory and Architecture

**Nutanix** builds a hyperconverged, multicloud platform — the **Nutanix Cloud
Infrastructure (NCI)** with the **AHV** hypervisor, the **AOS** distributed storage
fabric, and **Prism** management, extended by unified storage, database services,
automation, and cloud-cluster (NC2) offerings. **Nutanix University** validates the
skills to deploy, operate, and design these with a four-level program:
**Associate (NCA)**, **Professional (NCP)**, **Master (NCM)**, and **Expert
(NCX/NPX)**.

This is a **certification-tracks** volume: it maps the program — which credentials
exist, their **blueprint sections**, and levels — and teaches each with a hands-on
walkthrough. Every credential was **verified against nutanix.com on 27 July 2026**.
Recent facts: since **1 August 2025 all certifications are valid three years** (up
from two), and version **7.5** exams launched for **NCA** and **NCP-MCI** (NCA 7.5
appointments from 28 July 2026).

## Design Considerations

Choose by level and track. **NCA** is the foundation. The **NCP** professional tier
has role tracks: **Multicloud Infrastructure (NCP-MCI)**, **Multicloud Automation
(NCP-MCA)**, **Database Automation (NCP-DB)**, **Unified Storage (NCP-US)**, and
**Cloud Integration** for **NC2 on AWS (NCP-CI-AWS)** and **Azure (NCP-CI-Azure)**.
**NCM-MCI** is the master tier; **NCX-MCI** is the expert design credential. Practice
free on **Community Edition (CE)**.

## Implementation and Automation

Labs use real Nutanix tooling — the **Nutanix CLI (`ncli`)**, the **Acropolis CLI
(`acli`)**, the **Prism REST API (v3/v4)**, and the **v4 SDKs / `nutanix.ncp` Ansible
collection** — against a cluster or **Community Edition**. Confirm the lineup:

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.nutanix.com/support-services/training-certification/certifications" \
  | grep -oiE 'NCA|NCP-[A-Z-]+|NCM-MCI|NCX-MCI|NPX' | sort -u
```

## Validation and Troubleshooting

Confirm the program facts before you study:

```text
nutanix.com > Training & Certification:
  - levels: NCA (Associate), NCP (Professional), NCM (Master), NCX/NPX (Expert)
  - NCP tracks: MCI, MCA, DB, US, CI-AWS, CI-Azure
  - Pearson VUE; valid 3 years (since 1 Aug 2025); recertify by exam
  - blueprint guide per exam (Section 3 = objectives)
```

Common pitfalls: studying an old version blueprint (7.5 is current for NCA/NCP-MCI);
and assuming a two-year validity (it is now three).

## Security and Best Practices

Read the current **exam blueprint guide** for your target credential, follow the
matching Nutanix University course, and practice on **Community Edition**. Treat Prism
and API access as privileged (RBAC, API keys). Recertify within the three-year window.

## References and Knowledge Checks

- nutanix.com/support-services/training-certification: the program, blueprint guides, and courses.

**Knowledge checks**

1. Name the four certification levels and the NCP tracks.
2. What is the validity period, and when did it change?
3. Where do you practice Nutanix for free?

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell
with `curl`; a Nutanix cluster or **Community Edition** with `ncli`/`acli` for the
API/CLI checks. **Cost:** none (CE is free).

### Lab 1.1 — Enumerate the certification lineup

**Objective:** Read the certifications and tracks from the source.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.nutanix.com/support-services/training-certification/certifications" \
  | grep -oiE 'NCA|NCP-[A-Z-]+|NCM-MCI|NCX-MCI' | sort -u
```

**Expected result:** the credential acronyms (**NCA, NCP-MCI, NCP-MCA, NCP-DB,
NCP-US, NCP-CI-AWS, NCP-CI-Azure, NCM-MCI, NCX-MCI**) — the program map.

**Negative test:** trust a third-party list; vendors add/rename tracks — confirm on
nutanix.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Confirm cluster access (ncli)

**Objective:** Verify CLI access to a cluster/CE (the basis for later labs).

```bash
ncli cluster info | head -20
# name, id, version (AOS), and cluster state
```

**Expected result:** the cluster **name, AOS version, and state** — proof of `ncli`
access.

**Negative test:** run `acli`/`ncli` off-cluster; these run on a CVM/Prism context —
connect to the cluster first.

**Rollback:** none (read-only).

### Lab 1.3 — Confirm the level/track model

**Objective:** State the level-and-track structure.

```bash
python3 - <<'PY'
levels={"Associate":"NCA",
        "Professional":"NCP-MCI, NCP-MCA, NCP-DB, NCP-US, NCP-CI-AWS, NCP-CI-Azure",
        "Master":"NCM-MCI","Expert":"NCX-MCI / NPX"}
for lvl,tracks in levels.items(): print(f"{lvl:13}: {tracks}")
PY
```

**Expected result:** the four levels mapped to their tracks — the program's structure.

**Negative test:** treat all NCPs as one exam; each **track** is a separate blueprint
and exam — pick the right one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Nutanix certification program validates operating and designing the Nutanix Cloud
Platform across four levels — NCA, NCP (six tracks), NCM, and NCX/NPX — delivered by
Pearson VUE and valid three years. Blueprint guides define the sections; this volume
teaches each with real Nutanix tooling on Community Edition.

- [ ] I can name the levels and NCP tracks.
- [ ] I can state the exam format, fees, and validity.
- [ ] I can confirm cluster access with ncli.
- [ ] I can locate the blueprint guides and Community Edition.
- [ ] I completed Labs 1.1–1.3 including each negative test.
