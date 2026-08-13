# Chapter 01: The Cloudflare Certification Program

![The Cloudflare certification program and platform. The certification track is young: two Associate exams, the Application Security Associate and the Zero Trust Associate, delivered on Cloudflare's own exam platform at certifications.cloudflare.com, with the portal still showing Register Interest. At Cloudflare Connect 2026, October 19 to 21 in San Francisco, a 495-dollar University Pass adds a full training day plus one attempt at both exams, in-person proctored. Duration, question count, passing score, validity, and standalone pricing are not published. A separate partner accreditation track through Cloudflare University covers the Accredited Sales Professional, Accredited Sales Engineer, Accredited Configuration Engineer, Accredited Services Architect, and an Accredited Workers Developer in development. Beneath both sits the platform: a global anycast edge network carrying DNS, CDN caching, and TLS; the Application Security family of WAF, DDoS protection, Bot Management, and API Shield; the Cloudflare One Zero Trust family of Access, Gateway, WARP, and Tunnel; and the Workers developer platform, all managed by API and Terraform.](../../../diagrams/volume-142-cloudflare-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Two Associate exams, a separate partner accreditation track, and the platform beneath both.*

## Learning Objectives

- Describe Cloudflare's two certification exams and what is verifiably known about them.
- Separate the certification track from the partner accreditation track — search results do not.
- Know which exam facts are published and which are not.
- Set up a free study environment for the labs in this volume.

## What Cloudflare is

Cloudflare operates a global **anycast edge network** and sells what runs on it. Every service shares one architectural idea: **your traffic arrives at the nearest Cloudflare data center first**, and whatever inspection, caching, filtering, or compute you have configured happens there, before anything reaches your origin or your users' devices reach the internet.

That single idea produces three product families, and — usefully for this volume — the two certification exams map onto the first two:

| Family | What it does | Exam |
|:---|:---|:---|
| **Application Security** | WAF, DDoS protection, Bot Management, API Shield in front of your applications | **Application Security Associate** |
| **Cloudflare One (Zero Trust)** | Access (ZTNA), Gateway (SWG), WARP, Tunnel — between your users and everything | **Zero Trust Associate** |
| **Developer platform** | Workers, Pages, R2, KV, D1 — compute and storage on the edge itself | (Accredited Workers Developer, partner track, in development) |

## The certification program: young, and honestly described

Cloudflare's certification program is the newest on this shelf, and the volume treats that as a fact to work with rather than around.

**What is verifiable, as of 4 August 2026:**

- **Two exams exist**: the **Application Security Associate** and the **Zero Trust Associate**.
- The Application Security Associate's public page says it "assesses a candidate's foundational knowledge and capabilities," and that "basic, hands-on experience with Cloudflare Application Security products is highly recommended prior to taking the Associate level exam."
- Delivery is **Cloudflare's own exam platform** at `certifications.cloudflare.com` — not Pearson VUE, not Webassessor. The platform's public page still offers **"Register Interest"** alongside "Launch Certification Exam," which is what a program in rollout looks like.
- At **Cloudflare Connect 2026** (October 19–21, Moscone West, San Francisco), a **$495 University Pass** (early-bird pricing until June 30, 2026) adds a full day of live technical training plus **one attempt at both exams**, delivered **in-person proctored** in "a private, quiet environment… with live support." Laptops required.

**What is not published:**

> **Exam duration, question count, passing score, validity period, retake policy, and the standalone (non-Connect) exam price are not publicly stated.** The detailed domain outlines exist — the portal says so — but they sit behind the exam-platform login. This volume asserts none of these, and any third-party source stating them is guessing.

That is the fourth vendor on this shelf requiring this discipline, after [SolarWinds (CXXXIV)](../../volume-134-solarwinds-certifications/README.md), [Rapid7 (CXXXVII)](../../volume-137-rapid7-certifications/README.md), and [Dynatrace (CXL)](../../volume-140-dynatrace-certifications/README.md). The pattern is worth naming: **young or restructured programs publish least**, and that is exactly when third-party "exam dumps" fill the vacuum with invented numbers.

## The partner accreditation track — a different thing

Cloudflare University also issues **accreditations**, aimed at partners, earned through course completion rather than proctored certification exams:

| Accreditation | Covers (Cloudflare's phrasing) |
|:---|:---|
| **Accredited Sales Professional** | "key product features and how to identify opportunities" |
| **Accredited Sales Engineer (ASE)** | "Cloudflare's technical differentiation" |
| **Accredited Configuration Engineer (ACE)** | "implementation, best practices, and supporting Cloudflare" |
| **Accredited Services Architect (ASA)** | "cybersecurity management, performance optimization, and migration services" |
| **Accredited Workers Developer** | serverless applications with Workers — announced as in development |

Two things to keep straight, because search results reliably do not:

1. **An accreditation is not a certification.** The accreditations are partner-enablement course tracks; the certifications are proctored exams. A résumé line saying "Cloudflare certified" should mean the latter.
2. **"ACE" collides.** Cloudflare's ACE is the Accredited Configuration Engineer; Aviatrix's ACE ([Volume CXXVI](../../volume-126-aviatrix-certifications/README.md)) is the Aviatrix Certified Engineer. Same acronym, different vendors, different meanings.

## Hands-On Lab

The labs in this volume model Cloudflare concepts in Python at no cost. Cloudflare's **free tier is genuinely substantial** — a free account with a real domain can exercise DNS, caching, WAF managed rules, Access policies for up to 50 users, Tunnel, and Workers — which makes hands-on practice for both exams unusually cheap.

### Lab 1.1 — What is knowable, sorted

**Objective:** Build the verified-facts table for a young program.

```bash
python3 - <<'EOF'
FACTS = [
  # claim,                                              status,      source
  ("Two exams: App Security Assoc, Zero Trust Assoc",  "VERIFIED",  "certifications.cloudflare.com + Connect 2026 page"),
  ("Hands-on experience 'highly recommended'",          "VERIFIED",  "exam portal, App Security page"),
  ("Delivery on Cloudflare's own exam platform",        "VERIFIED",  "the portal IS the exam engine"),
  ("Connect 2026 University Pass $495, both exams",     "VERIFIED",  "cloudflare.com/connect/cloudflare-university"),
  ("In-person proctoring at Connect",                   "VERIFIED",  "same page"),
  ("Exam duration / question count",                    "UNPUBLISHED","not on any public page"),
  ("Passing score",                                     "UNPUBLISHED","not on any public page"),
  ("Validity / expiration",                             "UNPUBLISHED","not on any public page"),
  ("Standalone exam price",                             "UNPUBLISHED","only the Connect bundle is priced"),
  ("Detailed domain outlines",                          "GATED",     "exist per the portal; behind exam login"),
  ("'Cloudflare Professional/Expert certification'",    "NOT FOUND", "no such tier exists on any official page"),
]
print(f"{'claim':52}{'status':>13}   source")
for c, s, src in FACTS:
    print(f"{c:52}{s:>13}   {src}")
v = sum(1 for _, s, _ in FACTS if s == "VERIFIED")
print(f"\n{v} verified facts. That is genuinely enough to prepare with — the free tier")
print("plus the product documentation covers the recommended hands-on experience —")
print("but every number a practice-exam site offers you beyond these is invented.")
print("\nA young program's shape: 'Register Interest' on the portal, conference-bundled")
print("delivery, unpublished mechanics. Expect ALL of this to change; Chapter 09's")
print("currency section exists for exactly this volume.")
EOF
```

**Expected result:** Five verified facts, four unpublished, one gated, and one tier that does not exist. The table's value is its shape — for a program this young, knowing which column each claim belongs in *is* the preparation advantage, because the vacuum is being filled by third parties faster than by Cloudflare.

**Negative test:** Accepting a question count from any non-Cloudflare source. The domain outlines are behind the exam login; nobody outside has them legitimately.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Certification or accreditation?

**Objective:** Classify credentials the way a résumé reviewer should.

```bash
python3 - <<'EOF'
CREDENTIALS = [
  ("Application Security Associate",      "certification", "proctored exam, practitioner"),
  ("Zero Trust Associate",                "certification", "proctored exam, practitioner"),
  ("Accredited Configuration Engineer",   "accreditation", "partner course track"),
  ("Accredited Sales Engineer",           "accreditation", "partner course track, pre-sales"),
  ("Accredited Services Architect",       "accreditation", "partner course track, services"),
  ("Accredited Sales Professional",       "accreditation", "partner course track, sales"),
  ("Accredited Workers Developer",        "accreditation", "in development at verification"),
]
print(f"{'credential':38}{'type':>15}   nature")
for name, kind, nature in CREDENTIALS:
    print(f"{name:38}{kind:>15}   {nature}")
certs = sum(1 for _, k, _ in CREDENTIALS if k == "certification")
print(f"\n{certs} certifications, {len(CREDENTIALS)-certs} accreditations. The distinction:")
print("   certification  = proctored exam, open to practitioners")
print("   accreditation  = course-completion track, aimed at partners")
print("\nBoth are real credentials; they answer different questions. 'Completed the")
print("partner enablement track' and 'passed a proctored exam' are different claims,")
print("and a hiring conversation goes better when the résumé knows which it makes.")
print("\nAlso: Cloudflare's ACE = Accredited Configuration Engineer. Aviatrix's ACE =")
print("Aviatrix Certified Engineer (Vol CXXVI). Acronyms are not globally unique.")
EOF
```

**Expected result:** Two certifications against five accreditations, cleanly separated. The closing acronym note earns its place — "ACE" now means different things two volumes apart in this encyclopedia, which is precisely the kind of collision that produces confident wrong claims in interviews.

**Negative test:** Listing an accreditation as "Cloudflare certified" on a résumé. It is a real credential described wrongly, and a wrongly described credential reads worse than an absent one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Both certification exams identified, with the verified facts separated from the unpublished ones.
- [ ] The Connect 2026 delivery bundle and its $495 dual-attempt pass understood.
- [ ] Certifications distinguished from partner accreditations.
- [ ] The anycast-edge architecture placed under all three product families.
- [ ] A free-tier account identified as the practice environment both exams recommend.
