# Chapter 09: Choosing a Tier, Currency, and Career

## Learning Objectives

- Choose and sequence Readiverse tiers for your role.
- Use Readiverse coursework to earn ISC2 CPE credits.
- Place Commvault among the encyclopedia's other data-protection programs.
- Keep current with a program that was rebuilt in June 2026.

## Choosing a tier

The tiers are a genuine ladder — each builds on the one below — so the choice is mostly about where you start and how far you need to go:

| If you… | Target | Covers |
|:---|:---|:---|
| Are new to Commvault, or administer it occasionally | **Practitioner** | Platform administration + cyber resilience + one workload (Chapters 02–06, 08) |
| Run the platform daily across several workloads | **Specialist** | Expanded operational, workload, and security depth |
| Lead recovery design, or own resilience | **Professional** | Adds **Cloud Rewind** or **Cleanroom Recovery** (Chapter 07) |
| Architect the platform or lead resilience strategy | **Expert** | Cloud Engineer coursework, advanced features, both recovery capabilities |

Start at **Practitioner** regardless of experience — it is the tier whose requirements are fully published, it establishes the badge, and its Cyber Resilience component is material that experienced backup administrators often have not formally covered. The workload course requirement is a chance to pick the platform you actually protect (Chapter 08).

## ISC2 CPE credits

Commvault is an **ISC2 CPE Authorized Submitter**, so Readiverse coursework earns continuing professional education credits toward ISC2 certifications ([Volume XL](../../volume-040-isc2-certifications/README.md)). If you hold a CISSP, SSCP, or CCSP, you need CPEs every year regardless — taking them as data-protection training you would benefit from anyway is strictly better than hunting for filler webinars. Track submissions as you complete courses.

## Where Commvault sits in the encyclopedia

Data protection is a crowded, well-covered category here, and the volumes complement rather than repeat each other:

- [**Veeam LXXXV**](../../volume-085-veeam-certifications/README.md) — the VMware-rooted backup specialist, strong in virtualization estates.
- [**Rubrik CXXX**](../../volume-130-rubrik-certifications/README.md) — cyber-resilience-first, deliberately focused on one active certification (RCSA).
- [**NetApp LXXXIV**](../../volume-084-netapp-certifications/README.md) — storage-led data management, with protection as a storage capability.
- **Commvault (this volume)** — the broadest **workload coverage** and the most explicit **four-tier learning ladder**, spanning SaaS, software, and hybrid.

Underlying vendor-neutral material is in [Volume VI — Enterprise Storage and Data Protection](../../volume-006-enterprise-storage-data-protection/README.md), and the security framing connects to [Volume X — Enterprise Cybersecurity](../../volume-010-enterprise-cybersecurity/README.md).

A pattern worth noticing across all four: **every major data-protection vendor has repositioned backup as a security control.** Rubrik leads with cyber resilience, Veeam with ransomware recovery, Commvault with Threat Scan and Cleanroom Recovery. If you learn one deeply, the concepts — immutability, anomaly detection, clean recovery points, isolated recovery — transfer.

## Currency

- **This program is new.** The four-tier structure was introduced in **June 2026**, with Practitioner live first and the upper tiers following within weeks. Requirements, course composition, and exam details for Specialist, Professional, and Expert were still being finalized at announcement — **verify current requirements on Readiverse Academy before committing**, and treat any tier detail in this volume beyond Practitioner as directional.
- **The product moves fast.** Cleanroom Recovery, Cloud Rewind, and Threat Scan are recent capabilities and are actively developed; the courses follow the product.
- **Verified 4 August 2026** from Readiverse Academy and Commvault's own announcements. Third-party training resellers and exam-dump sites were deliberately excluded — for a program this new, they are usually describing the *previous* certification scheme.

That last point is worth internalizing as a research habit: when a vendor restructures a program, third-party course sellers lag by months and will confidently sell you preparation for retired exams.

## Hands-On Lab

### Lab 9.1 — Build your Commvault certification plan

**Objective:** Commit to a tier-aligned path.

```bash
cat > my-commvault-plan.md <<'EOF'
Deployment I work with:   Commvault Cloud SaaS / self-managed software / hybrid
Primary workload:         M365 / AD+Entra / VMware / Oracle / file servers
Start:                    Commvault Cloud Practitioner
   - Cloud Administrator course (~4h) + exam
   - Cyber Resilience course (~4h) + exam
   - one workload course (~30m)  -> pick the workload above
   - claim the digital badge
Then:                     Specialist -> Professional (Cloud Rewind or Cleanroom Recovery) -> Expert
ISC2 CPEs:                submit Readiverse coursework (Commvault is an Authorized Submitter)
Verify first:             tier requirements on Readiverse Academy — the program was rebuilt June 2026
Practice:                 model retention, dedup, RPO/RTO, immutability, cleanroom free in Python
EOF
cat my-commvault-plan.md
```

**Expected result:** A plan that starts at Practitioner with a workload chosen to match the estate, records the ISC2 CPE benefit, and — importantly — puts *verify the current requirements* before the study effort. For a program restructured this recently, that verification step is not boilerplate.

**Negative test:** Buying a third-party "Commvault certification" course without checking it against Readiverse — much of the third-party market still teaches the pre-June-2026 scheme.

**Cleanup:** Keep the plan.

### Lab 9.2 — Self-assess against the three pillars

**Objective:** Find the weak pillar before booking an exam.

```bash
python3 - <<'EOF'
pillars = {
  "Platform: architecture (ch02)":            4,
  "Platform: storage & retention (ch03)":     3,
  "Platform: deduplication (ch04)":           2,
  "Platform: backup/recovery ops (ch05)":     4,
  "Cyber resilience: immutability (ch06)":    2,
  "Cyber resilience: cleanroom/rewind (ch07)":1,
  "Workloads: M365/AD/VMware/Oracle (ch08)":  3,
}
print("Self-rated confidence (0-5):\n")
for topic, score in sorted(pillars.items(), key=lambda kv: kv[1]):
    print(f"{topic:44} [{'#'*score}{'.'*(5-score)}] {'STUDY FIRST' if score <= 2 else ('review' if score < 4 else 'ready')}")

by_pillar = {"Platform": [4,3,2,4], "Cyber resilience": [2,1], "Workloads": [3]}
print()
for name, scores in by_pillar.items():
    avg = sum(scores)/len(scores)
    print(f"{name:18} average {avg:.1f}/5 {'<-- WEAKEST PILLAR' if avg < 2.5 else ''}")
print("\nPractitioner requires BOTH the Administrator and Cyber Resilience exams — the weak pillar blocks the tier.")
EOF
```

**Expected result:** Cyber resilience averages 1.5 and is flagged as the weakest pillar. The closing line explains why that specifically matters: the Practitioner tier requires *both* exams, so strength in platform administration cannot compensate for weakness in resilience. Experienced backup administrators are exactly the people likely to show this profile — deep on architecture and operations, thin on immutability and cleanroom recovery, because those capabilities are newer than their experience.

**Negative test:** Studying the pillar you already know — platform administration is comfortable and already at 4s; the exam you would fail is the other one.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A tier chosen, starting at Practitioner with a workload matching your estate.
- [ ] The ISC2 CPE benefit recorded and submissions planned.
- [ ] Commvault placed against Veeam, Rubrik, and NetApp.
- [ ] Currency habits installed for a program restructured in June 2026, with third-party sources treated skeptically.
