# Chapter 01: The Atlassian Credential Program

![The Atlassian credential program, restructured into three tiers plus designations. At the base, Atlassian Certificate Holder credentials, ACH, are free, quick-to-earn certificates for app users demonstrating foundational knowledge — the Atlassian Cloud Fundamentals certificate is an example. In the middle, Atlassian Certified Associate certifications, ACA, are industry-recognized credentials for professionals who use Atlassian apps in their jobs, such as Managing Jira Projects for Cloud. At the top, Atlassian Certified Professional certifications, ACP, are role-based credentials crafted for solution administrators — Jira Administration for Cloud, Confluence Administration, Atlassian Cloud Organization Admin, and the cross-product System Administrator. Designations stack multiple credentials in related paths into a meta-credential. The program is aggressively cloud-first: Server reached end of support in February 2024, and the catalog now leads with the for-Cloud variants while Data Center certifications persist for on-premise holdouts. Preparation is free — on-demand training, exam-prep courses with business-case study guides and hands-on labs, and documentation — with exams scheduled through the credential portal. The platform beneath is Jira, Confluence, Jira Service Management, and the Atlassian cloud administration hub.](../../../diagrams/volume-145-atlassian-certifications/chapter-01-credential-program.svg)

*Figure 1-1. Three credential tiers over a cloud-first, product-structured platform.*

## Learning Objectives

- Describe Atlassian's three-tier credential structure and designations.
- Distinguish the ACH, ACA, and ACP credentials by audience and depth.
- Understand the cloud-first shift shaping the current catalog.
- Recognize what Atlassian publishes and what sits behind the credential portal.

## What Atlassian is

Atlassian makes the tools a large share of the software world plans and documents its work in: **Jira** (issue and project tracking), **Confluence** (team documentation and knowledge), **Jira Service Management** (IT service management), and a cloud administration layer tying them together. Where [GitLab (CXXXVI)](../../volume-136-gitlab-certifications/README.md) and [GitHub (LXXXIX)](../../volume-089-github-certifications/README.md) own the code, Atlassian owns the *planning and coordination* around it — and its certification program is about administering that toolset well.

Atlassian's heritage is agile: Jira grew up as the tool agile teams run their sprints in, and that shows in the certifications' emphasis on configuring the tool to fit how teams actually work.

## The three-tier structure

Atlassian restructured its credentials into three tiers, and reading a résumé requires keeping them straight:

| Tier | Full name | For | Cost |
|:---|:---|:---|:---|
| **ACH** | Atlassian **Certificate Holder** | App *users* — foundational knowledge of an app or solution | **Free** |
| **ACA** | Atlassian **Certified Associate** | Professionals who *use* the apps in their jobs | Paid |
| **ACP** | Atlassian **Certified Professional** | Solution *administrators* — advanced, role-based | Paid |

The progression tracks responsibility: **ACH is for anyone using the tool, ACA for someone doing real work in it, ACP for the person who administers it.** The distinction that matters most on a hiring conversation is the ACA/ACP line — ACA proves you can *work in* Jira effectively; ACP proves you can *configure and administer* it for others. They are different jobs.

Above the three tiers sit **Designations** — meta-credentials that recognize earning *multiple* credentials in a related path. A designation is not a single exam but a stacking of several, signaling breadth across a solution area.

### The free base tier is real

The **ACH certificates are genuinely free and quick to earn** — Atlassian's own framing is "a valuable first step in your Atlassian credential journey." This is unusual and worth using: the [Atlassian Cloud Fundamentals] certificate and its peers cost nothing, and for someone deciding whether to invest in the paid tiers, they are a zero-cost way to confirm the platform and the study style suit you.

## The cloud-first shift

The single biggest force shaping the current catalog is Atlassian's **cloud-first pivot**:

- **Atlassian Server reached end of support in February 2024.** The self-hosted single-server deployment is gone; customers run **Cloud** (Atlassian-hosted SaaS) or **Data Center** (self-managed, clustered).
- **The certification catalog now leads with "for Cloud" variants** — Jira Administration for Cloud, Managing Jira Projects for Cloud, Atlassian Cloud Organization Admin, Atlassian Cloud Fundamentals.
- **Data Center certifications persist** for the on-premise holdouts, but they are the legacy path, not the emphasis.

For a certification candidate this is a real decision, not a formality: **certify for the deployment your organization actually runs**, and if you have a choice, Cloud is where Atlassian is investing. The migration itself — Data Center to Cloud — is prominent enough in Atlassian's learning paths that it is effectively a skill area of its own.

## What is published

Atlassian publishes the credential structure, the certifications, the free prep, and the FAQ topics (cost, validity, payment). The **per-exam mechanics** — exact question count, duration, passing score, price, and validity — sit behind an "Open full exam details" panel and the credential portal, which is where you should read them for your target exam.

> **The discipline, familiar by now:** this volume states the structure, the tiers, the cloud-first shift, and the free base tier — all published — and points you at the credential portal for the per-exam numbers rather than asserting figures that render only in the live panel. One published fact worth carrying: Atlassian cites that **"86% of Atlassian Certified Professionals reported their credentials increased their credibility"** — a vendor survey stat, quoted as such.

## Hands-On Lab

The labs in this volume model Atlassian administration concepts in Python at no cost. Atlassian Cloud also offers a **free tier** (up to 10 users) — genuinely useful for practicing the ACP administration skills, since the exams assume hands-on configuration experience.

### Lab 1.1 — Place a credential by tier and audience

**Objective:** Read the three tiers as a responsibility ladder.

```bash
python3 - <<'EOF'
CREDENTIALS = [
  # name,                                   tier,  audience,              cost
  ("Atlassian Cloud Fundamentals",          "ACH", "any app user",        "FREE"),
  ("Managing Jira Projects for Cloud",      "ACA", "project lead / user", "paid"),
  ("Jira Administration for Cloud",         "ACP", "Jira admin",          "paid"),
  ("Confluence Administration",             "ACP", "Confluence admin",    "paid"),
  ("Atlassian Cloud Organization Admin",    "ACP", "org-level admin",     "paid"),
  ("Atlassian Certified System Administrator","ACP","cross-product admin", "paid"),
]
TIER_RANK = {"ACH": 1, "ACA": 2, "ACP": 3}
print(f"{'credential':42}{'tier':>6}{'cost':>7}   audience")
for name, tier, aud, cost in sorted(CREDENTIALS, key=lambda c: (TIER_RANK[c[1]], c[0])):
    print(f"{name:42}{tier:>6}{cost:>7}   {aud}")
print("\nThe tiers are a RESPONSIBILITY ladder, not a difficulty ladder:")
print("  ACH — can you USE the app? (foundational, free)")
print("  ACA — can you WORK effectively in it? (a project lead running sprints)")
print("  ACP — can you ADMINISTER it for others? (the config, the schemes, the org)")
print("\nThe ACA/ACP line is the one that matters when hiring: 'Managing Jira")
print("Projects' (ACA) is a PROJECT admin — runs one project's board and workflow.")
print("'Jira Administration' (ACP) is an INSTANCE admin — owns the workflows,")
print("permission schemes, and fields EVERY project inherits. Different jobs,")
print("different blast radius, different certification.")
print("\nStart free (ACH) to confirm fit, then certify at the tier that matches the")
print("job you want — not the highest tier available.")
EOF
```

**Expected result:** The six credentials sorted into the ACH→ACA→ACP responsibility ladder, with the ACA/ACP project-admin-versus-instance-admin distinction made concrete. The blast-radius framing is the hiring-relevant lesson — a project admin configures one project, an instance admin configures what all projects inherit, and the certifications name which.

**Negative test:** Reading the tiers as beginner/intermediate/advanced difficulty. They are audience tiers — an ACP is not "harder ACA," it is a different role (administering versus using).

**Cleanup:** None.

### Lab 1.2 — Certify for the deployment you actually run

**Objective:** Choose Cloud versus Data Center by reality, not preference.

```bash
python3 - <<'EOF'
ORGS = [
  ("SaaS-native startup",           "Cloud",       "born in Atlassian Cloud"),
  ("enterprise, data-residency reqs","Data Center", "must self-host (regulatory)"),
  ("mid-size, migrating off Server", "Cloud",       "Server EOL Feb 2024 forced the move"),
  ("large enterprise, heavy custom", "Data Center", "clustered self-managed, deep customization"),
]
print("Atlassian Server reached END OF SUPPORT in February 2024.")
print("Remaining deployments: Cloud (Atlassian-hosted) or Data Center (self-managed).\n")
print(f"{'organization':34}{'deployment':>13}   why")
cloud = dc = 0
for org, dep, why in ORGS:
    if dep == "Cloud": cloud += 1
    else: dc += 1
    print(f"{org:34}{dep:>13}   {why}")
print(f"\n{cloud} Cloud, {dc} Data Center. The certification decision follows the")
print("deployment: 'Jira Administration for CLOUD' and 'for DATA CENTER' are")
print("SEPARATE exams testing different admin surfaces (Cloud's org model and")
print("automation vs Data Center's clustering and infrastructure).")
print("\nThe rule: certify for what your organization RUNS. And note the direction of")
print("travel — Atlassian leads its catalog with the Cloud variants and treats")
print("Data-Center-to-Cloud MIGRATION as its own learning path. If you have a free")
print("choice (new career, no employer constraint), Cloud is where the investment is.")
print("\nStudying the Cloud exam for a Data Center admin job (or vice versa) wastes")
print("effort on an admin surface you will not touch — the clustering questions")
print("simply do not exist in Cloud, and the org-model questions do not exist in DC.")
EOF
```

**Expected result:** Organizations split between Cloud and Data Center by regulatory and migration reality, with the certification following the deployment. The direction-of-travel note is the career guidance — Cloud is Atlassian's investment focus, and the exams are deployment-specific because the admin surfaces genuinely differ.

**Negative test:** Pursuing the Data Center certification because it "sounds more serious." If your organization runs Cloud, you have certified in an admin surface you will never operate.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The three tiers (ACH free / ACA / ACP) understood as a responsibility ladder, plus designations.
- [ ] The ACA/ACP line read as use-versus-administer, project-admin versus instance-admin.
- [ ] The cloud-first shift understood, with Server's Feb 2024 EOL and Cloud/Data Center as the remaining choices.
- [ ] Per-exam mechanics identified as portal-gated, not asserted here.
- [ ] The free base tier and free Cloud tier identified as zero-cost ways to start.
