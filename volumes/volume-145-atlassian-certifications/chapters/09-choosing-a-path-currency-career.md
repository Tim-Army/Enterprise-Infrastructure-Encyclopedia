# Chapter 09: Choosing a Path, Currency, and Career

## Learning Objectives

- Choose an Atlassian credential path by role and deployment.
- Prepare using the free training Atlassian provides.
- Place Atlassian among the encyclopedia's DevOps and platform volumes.
- Stay current with a cloud-first program that restructured its credentials.

## Choosing a path

An Atlassian credential path is three questions:

1. **Which tier?** ACH (free, foundational) to start; ACA if you *use* the tools in your work; ACP if you *administer* them.
2. **Which product?** Jira, Confluence, JSM, or org-level — the specialty.
3. **Which deployment?** Cloud (where Atlassian invests) or Data Center (if that is what you run).

| If you… | Pursue | Tier |
|:---|:---|:---|
| Are new to Atlassian, want a free start | **Atlassian Cloud Fundamentals** | ACH (free) |
| Run projects / sprints as a lead | **Managing Jira Projects for Cloud** | ACA |
| Administer a Jira instance | **Jira Administration for Cloud** | ACP |
| Administer Confluence | **Confluence Administration** | ACP |
| Own the whole org's Atlassian tenant | **Atlassian Cloud Organization Admin** | ACP |
| Run self-hosted | The **Data Center** variants | ACP |

**Start with the free ACH tier** regardless — it costs nothing, confirms the platform and study style suit you, and is a genuine first credential. Then certify at the tier matching the job you want: the **ACA/ACP line is the important one** — prove you can *use* Jira (ACA) or that you can *administer* it (ACP), and choose the one your role actually is.

**Designations** are worth knowing about for a longer horizon: earning multiple related credentials stacks into a designation, a meta-credential signaling breadth. That is a multi-cert goal, not a starting point.

## Preparing

Atlassian's preparation is unusually generous:

1. **Free on-demand training** backs every certification — Atlassian's own courses, at no cost.
2. **Exam prep courses** (e.g. the Jira Administrator Exam Prep Course) provide study guides built on business cases, hands-on labs, and sample questions.
3. **The free Cloud tier** (up to 10 users) is a real practice instance — and the ACP administration exams assume hands-on configuration experience, so use it.
4. **The credential portal** holds the per-exam specifics (question count, duration, passing score, cost, validity) behind the "Open full exam details" panel — read them there for your exam.

> **The published-versus-portal split:** this volume states the structure, tiers, cloud-first shift, and free prep — all public — and points you at the credential portal for the per-exam numbers. Get cost and validity from the FAQ and the exam's own page; do not take them from a third party.

## Where Atlassian sits in the encyclopedia

Atlassian completes the **plan-build-run** toolchain the encyclopedia has been assembling:

| Volume | Role in the toolchain |
|:---|:---|
| **CXLV Atlassian** (this one) | **Plan and coordinate** — Jira/Confluence/JSM |
| [**CXXXVI GitLab**](../../volume-136-gitlab-certifications/README.md), [**LXXXIX GitHub**](../../volume-089-github-certifications/README.md) | **Build** — source, CI/CD |
| [**LXXX ServiceNow**](../../volume-080-servicenow-certifications/README.md) | The ITSM platform JSM competes with |
| [**CXLIV SAP**](../../volume-144-sap-certifications/README.md), [**LXXXIII Salesforce**](../../volume-083-salesforce-certifications/README.md) | The other module/role business-platform programs |

The comparison to carry: **Atlassian owns the planning-and-coordination layer that sits above the code**, where GitLab and GitHub own the code itself. A modern software org runs both — Jira issues linking to GitHub pull requests linking to Confluence design docs — which is why Atlassian's certification value is real even though its tools are not where code lives. The distinctive current fact is the **cloud-first pivot**: Server's end of life reshaped the whole catalog around Cloud, and the Data-Center-to-Cloud migration is now a skill area of its own.

## Currency

- **The program restructured into three tiers** (ACH/ACA/ACP) plus designations — recent enough that older references may use different names. Confirm the current structure on `community.atlassian.com/learning/certifications`.
- **Atlassian University moved** to the Community learning platform; `university.atlassian.com` redirects there.
- **Cloud-first is accelerating.** Server is gone (Feb 2024); the catalog leads with Cloud variants and treats Data Center as the legacy self-hosted path. Certify for the deployment you run, and expect Cloud emphasis to grow.
- **Per-exam mechanics are portal-gated** — read the "Open full exam details" panel for your target exam rather than assuming figures.
- **Verified 4 August 2026** from community.atlassian.com/learning/certifications (the three-tier structure, the certifications, the free prep, the FAQ topics) and per-certification pages. Per-exam question count, duration, passing score, price, and validity sit behind the credential portal and are not asserted here.

## Hands-On Lab

### Lab 9.1 — Build your Atlassian path

**Objective:** Choose tier, product, and deployment.

```bash
python3 - <<'EOF'
PROFILE = {
  "relationship to the tools": "administer",   # use / administer / lead-projects
  "product focus":            "jira",
  "deployment":               "cloud",
  "new to atlassian":          True,
}
tier = {"use":"ACA", "administer":"ACP", "lead-projects":"ACA"}[PROFILE["relationship to the tools"]]
prod = PROFILE["product focus"]
dep = PROFILE["deployment"]
cert = {
  ("ACP","jira","cloud"):  "Jira Administration for Cloud",
  ("ACP","jira","data center"): "Jira Administration for Data Center",
  ("ACA","jira","cloud"):  "Managing Jira Projects for Cloud",
}.get((tier, prod, dep), f"{tier} {prod} ({dep})")
print("Your Atlassian path:\n")
if PROFILE["new to atlassian"]:
    print("  0. START FREE: Atlassian Cloud Fundamentals (ACH) — confirm fit, zero cost")
print(f"  1. TIER: {tier} (you {PROFILE['relationship to the tools']} the tools)")
print(f"  2. PRODUCT: {prod}")
print(f"  3. DEPLOYMENT: {dep} (certify for what you RUN)")
print(f"\n  -> TARGET: {cert}")
print("\nThe three questions, in order: TIER (use vs administer — the ACA/ACP line),")
print("PRODUCT (your specialty), DEPLOYMENT (Cloud vs Data Center — match reality).")
print("Start on the free ACH tier, then certify at the tier that IS your job.")
print("\nDon't chase ACP if your role is using Jira well (that's ACA), and don't")
print("study the Data Center exam if you run Cloud. Match the credential to the")
print("actual work — the same discipline as every vendor in this batch.")
EOF
```

**Expected result:** A path resolving to a specific certification via tier → product → deployment, with the free ACH start recommended. The match-the-credential-to-the-work discipline is the closing lesson — the ACA/ACP line and the Cloud/Data-Center choice both reward honesty about what your role actually is.

**Negative test:** Pursuing the ACP admin certification when your role is running projects (ACA) on a deployment you do not administer. You certify in a job you do not hold, on a surface you do not touch.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — The free-first preparation plan

**Objective:** Assemble a plan starting from Atlassian's free resources.

```bash
python3 - <<'EOF'
plan = """
TARGET: Jira Administration for Cloud (ACP)

FREE FIRST (Atlassian provides all of this at no cost):
  [ ] Atlassian Cloud Fundamentals certificate (ACH) — free, confirms fit
  [ ] free on-demand training for the Jira admin path
  [ ] Jira Administrator Exam Prep Course — study guide (business cases),
      hands-on labs, sample questions
  [ ] a FREE Cloud tier instance (up to 10 users) to practice on

PRACTICE (the ACP exam assumes hands-on admin experience):
  [ ] build company-managed AND team-managed projects; feel the difference (ch02)
  [ ] create a workflow with a condition, validator, post-function (ch03)
  [ ] write JQL filters; deliberately order one badly, compare (ch03)
  [ ] build a permission scheme, share it across projects, trace the blast radius
  [ ] set up an automation rule; verify it doesn't loop

FROM THE CREDENTIAL PORTAL (the ONLY source for these):
  [ ] question count [ ] duration [ ] passing score [ ] price [ ] validity
  ("Open full exam details" panel — do not take these from third parties)

MINDSET: the ACP exams test ADMINISTRATION judgment — scheme design, blast-radius
awareness, when NOT to customize. Practice configuring a real instance, not
memorizing menu paths.
"""
print(plan)
print("Nearly everything here is FREE — the training, the prep course, the practice")
print("instance. Atlassian's low barrier to preparation is a genuine advantage;")
print("the only gated facts are the per-exam mechanics, one portal click away.")
EOF
```

**Expected result:** A preparation plan built almost entirely on Atlassian's free training, prep course, and Cloud tier, with only the per-exam mechanics portal-gated. The free-first framing is the practical takeaway — Atlassian's low preparation barrier is a real advantage, and the ACP exams reward hands-on admin practice over memorization.

**Negative test:** Buying third-party study material before exhausting Atlassian's free training and prep course. The official resources are free, comprehensive, and aligned to the exam; the paid alternatives rarely improve on them.

**Rollback:** Keep the plan.

## Summary and Completion Checklist

- [ ] A path chosen by tier (ACA/ACP line), product, and deployment.
- [ ] The free ACH tier used as a zero-cost start.
- [ ] Preparation built on Atlassian's free training, prep course, and Cloud tier.
- [ ] Per-exam mechanics sourced from the credential portal, not asserted from third parties.
- [ ] Atlassian placed in the plan-build-run toolchain, with the cloud-first shift noted.
