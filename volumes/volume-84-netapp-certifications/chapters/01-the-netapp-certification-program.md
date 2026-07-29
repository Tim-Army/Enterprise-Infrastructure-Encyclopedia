# Chapter 01: The NetApp Certification Program

## Learning Objectives

- Describe the NetApp certification paths and the Professional/Specialist/Expert tiers.
- Place the Associate accreditations and the flagship Data Administrator ONTAP (NCDA) in the ladder.
- Explain exam delivery (Pearson VUE), digital badges (Credly), and the NetApp login migration.
- Explain recertification and validity.
- Complete a walkthrough for each program-orientation topic on a Simulate ONTAP cluster.

## Theory and Architecture

**NetApp** certifications validate skills on **ONTAP** — NetApp's storage operating system — and the
hybrid-cloud data fabric built around it. The program is organized as **certification paths**, each a
ladder through three tiers:

- **Certified Professional** — the entry technical tier: **Technology Solutions** (foundational NetApp
  portfolio knowledge) and the flagship **Data Administrator ONTAP (NCDA, exam NS0-163)**, plus
  role Professionals such as **Hybrid Cloud Administrator (NS0-304)**, **StorageGRID Administration**,
  **Cloud and Storage Services Engineer**, **Storage Installation Engineer — ONTAP**, and **Support
  Engineer**.
- **Certified Specialist** — the implementation/engineering tier: **Implementation Engineer — SAN,
  ONTAP (NCIE-SAN, NS0-521)**, **Implementation Engineer — Data Protection (NCIE-DP, NS0-528)**,
  **Implementation Engineer — MetroCluster**, **Support Engineer ONTAP**, the **Implementation Engineer
  — SAN E-Series**, and the two **Cisco and NetApp FlexPod** specialists (Design; Implementation and
  Administration).
- **Certified Expert** — the architect/specialization tier: **Hybrid Cloud Architect (NS0-604)**, **AI
  Expert**, **AI Data Infrastructure**, and **Cyber Resiliency**.

Beneath these sit the online **Associate accreditations** — **NetApp Cloud Native Associate** and
**NetApp Hybrid Cloud Associate** — which NetApp recommends as foundational preparation before the
NCDA. Most paths begin with **Technology Solutions** and the **Data Administrator ONTAP** credential,
then branch: ONTAP engineering, Hybrid Cloud, Cloud Services, Installation, Support, FlexPod, AI, and
Cyber Resilience.

Exams are delivered through **Pearson VUE** (test center or online-proctored). Passing earns a digital
badge managed on **Credly**. As of **10 December 2024**, the certification system (formerly a separate
CertMetrics login) uses your **NetApp login credentials**, and records live in the **CertCenter**. NetApp
publishes **free exam-prep videos** for every certification and supports each with training courses in
the **Learning Center** (which requires a NetApp Support Site ID). Certifications are generally valid for
about **two years**; you **recertify** by passing the current version of the exam or a higher-level exam
in the path. This chapter orients you on a free **Simulate ONTAP** cluster (a downloadable simulator)
so the certification ladder maps to real commands.

## Design Considerations

Pick a **path** that matches your role — administrator, implementation engineer, hybrid-cloud, support,
or architect — and climb its tiers in order. **Technology Solutions** and **Data Administrator ONTAP**
ground almost everything, so earn the NCDA early. Track **exam versions**: NetApp refreshed the core
exams in **April 2026** (NS0-163, NS0-521, NS0-528, NS0-304, NS0-604), so study against the current
blueprint. Plan **recertification** before the two-year mark.

## Implementation and Automation

The labs use the ONTAP command line (**clustershell**) on a Simulate ONTAP cluster to confirm cluster
health, map the certification path to real subsystems, and read version information — the orientation an
NCDA candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Tiers:  Associate (accreditation) -> Professional -> Specialist -> Expert
Anchor: Technology Solutions + Data Administrator ONTAP (NCDA, NS0-163)
Paths:  ONTAP | Hybrid Cloud | Cloud Services | Installation | Support | FlexPod | AI | Cyber Resilience
Deliver: Pearson VUE (test center / online proctored); badges on Credly; records in CertCenter
Login:  NetApp login credentials (CertMetrics migrated 10 Dec 2024); ~2-year validity; recert by exam
```

Common pitfalls: chasing a Specialist exam before earning the **NCDA** that most Specialist credentials
build on; and studying an **outdated** exam blueprint after the April 2026 refresh.

## Security and Best Practices

Storage certifications validate the ability to run and protect **your own** data platform. Treat every
lab environment as production-adjacent: use least-privilege ONTAP roles, keep the cluster patched, and
never expose management LIFs. All work in this volume is authorized administration.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a free **Simulate ONTAP** cluster (NetApp's
downloadable ONTAP simulator) reachable over SSH as `admin@cluster1`, or any lab ONTAP 9 cluster; and
`python3` for path planning. **Cost:** none (Simulate ONTAP is a free download for registered users).

### Lab 1.1 — Confirm the cluster and ONTAP version

**Objective:** Read cluster identity and version — the orientation every path assumes.

```text
cluster1::> version
NetApp Release 9.15.1: Tue Apr 01 00:00:00 UTC 2026

cluster1::> cluster show
Node                  Health  Eligibility
--------------------- ------- ------------
cluster1-01           true    true
cluster1-02           true    true
2 entries were displayed.
```

**Expected result:** the ONTAP release and a healthy two-node cluster — the platform the NCDA validates.

**Negative test:** run `cluster show` and find a node with `Health false`; a degraded node must be
recovered before administration — investigate with `system node show`.

**Cleanup:** none (read-only).

### Lab 1.2 — Map the certification path

**Objective:** Reason about which credentials a role needs.

```python
python3 - <<'PY'
path = {
  "Associate":   ["Cloud Native Associate", "Hybrid Cloud Associate"],
  "Professional":["Technology Solutions", "Data Administrator ONTAP (NCDA, NS0-163)"],
  "Specialist":  ["Impl Engineer SAN (NS0-521)", "Impl Engineer Data Protection (NS0-528)"],
  "Expert":      ["Hybrid Cloud Architect (NS0-604)", "AI Expert", "Cyber Resiliency"],
}
for tier, certs in path.items():
    print(f"{tier:12}: {', '.join(certs)}")
print("Rule: earn Technology Solutions + NCDA first; Specialist/Expert build on them")
PY
```

**Expected result:** the tiers in order with the NCDA as the anchor before Specialist and Expert.

**Negative test:** plan to sit **Implementation Engineer — Data Protection (NS0-528)** with no NCDA;
the Specialist credential assumes ONTAP administration — earn the NCDA first.

**Cleanup:** none.

### Lab 1.3 — Read your entitlements and roles

**Objective:** See the administrative roles the platform grants — the least-privilege model behind the exams.

```text
cluster1::> security login show -vserver cluster1
Vserver: cluster1
                                                             Second
User/Group                 Authentication                    Acct
Name           Application Method        Role Name           Locked
-------------- ----------- ------------- ------------------- ------
admin          console     password      admin               no
admin          ssh         password      admin               no
3 entries were displayed.
```

**Expected result:** the `admin` account bound to the built-in `admin` role — the RBAC model NetApp
administration and the exams assume.

**Negative test:** grant a day-to-day operator the `admin` role; create a scoped role
(`security login role create`) with only the needed command directories instead.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NetApp program runs Associate accreditations through Professional, Specialist, and Expert tiers
across the ONTAP, Hybrid Cloud, Cloud Services, Installation, Support, FlexPod, AI, and Cyber Resilience
paths. Technology Solutions and the Data Administrator ONTAP (NCDA, NS0-163) anchor the ladder; exams
run through Pearson VUE with Credly badges, use NetApp login credentials, and are valid about two years.

- [ ] I can describe the paths and the Professional/Specialist/Expert tiers.
- [ ] I can place the Associate accreditations and the NCDA in the ladder.
- [ ] I can explain Pearson VUE delivery, Credly badges, and recertification.
- [ ] I completed Labs 1.1–1.3 including each negative test.
