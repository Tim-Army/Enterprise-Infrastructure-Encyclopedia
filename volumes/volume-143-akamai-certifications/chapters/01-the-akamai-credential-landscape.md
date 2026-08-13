# Chapter 01: The Akamai Credential Landscape

![The Akamai credential landscape. Akamai University Customer Enablement delivers instructor-led, virtual instructor-led, and custom on-site courses across security, content delivery, and edge compute, each earning a Credly badge at Foundational or Advanced level — Web Performance Foundations and Offload, Media Delivery, Bot Manager Foundations and Advanced, Web Application and API Protection, Bot and Abuse Protection, Client-Side Protection and Compliance, Zero Trust Solutions, Automation and DevOps, and Fraud Management. The certification tier holds the Akamai Cloud Computing Foundations Certification and the Guardicore family: Certified Segmentation Administrator and its Advanced variant, Certified Segmentation Engineer and its On-Premise variant, and the partner-level Certified Services Provider programs for Implementation and Support, plus the API Security Architect credential. A separate partner track carries Certified Partner Solutions Architect badges for twelve products and Partner Foundations and Advanced badges across four solution areas. The Akamai Technical Academy offers two Coursera professional certificates for career entry. Beneath everything sits the platform: the intelligent edge for delivery and performance, the application security family, the zero trust and Guardicore segmentation family, and Akamai Cloud compute. Exam mechanics are not published; badge metadata provides level, paid or free, and time-to-earn bands.](../../../diagrams/volume-143-akamai-certifications/chapter-01-credential-landscape.svg)

*Figure 1-1. Courses that badge, certifications that examine, and a partner track beside both.*

## Learning Objectives

- Map Akamai's credential landscape: University course badges, the certification tier, the partner track, and the career-entry academy.
- Read badge metadata correctly — level, cost flag, and time-to-earn are published; exam mechanics are not.
- Place the Guardicore certifications in their own family, with its own ladder.
- Set up the study environment for this volume.

## What Akamai is

Akamai runs one of the internet's oldest and largest edge platforms — the delivery network that predates the term "CDN" being interesting — and has built three businesses on it:

| Family | What it does | Chapters |
|:---|:---|:---|
| **Delivery & performance** | CDN, DNS/GTM, web performance (Ion, mPulse), media delivery | 02–03 |
| **Security** | App & API Protector, Bot Manager, Account/Content Protector, API Security, Client-Side Protection, Zero Trust, **Guardicore segmentation** | 04–07 |
| **Cloud computing** | Akamai Cloud — the Linode acquisition grown into an edge-adjacent cloud | 08 |

The immediate contrast with [Volume CXLII (Cloudflare)](../../volume-142-cloudflare-certifications/README.md) is worth setting up front, because the two edges sell into the same meetings: Cloudflare's platform runs one configuration model on one network with a self-serve free tier; Akamai's is an enterprise estate — richer in per-product depth, configured per product, learned per course, and priced per conversation. The credential programs mirror that exactly.

## The credential landscape

Akamai's credentials divide into four groups, and reading a résumé — or planning a year — requires keeping them apart:

### 1. Akamai University: Customer Enablement (course badges)

Akamai University delivers courses in three modalities — **Instructor-Led Training (ILT), Virtual Instructor-Led Training (VILT)** ("exact same training scope and materials as ILT," in four-hour increments), and **Custom On-Site**. Completing a course earns a **Credly badge**; the program's own description is that it "recognizes Foundational and Advanced learners" across security, content delivery, and edge compute.

The live schedule at verification showed 3-day online regional deliveries (AMER/EMEA/APAC) of: Web Application & API Protection, Bot & Abuse Protection, Automation & DevOps, and Web Performance Foundations, with some 1-day Japanese-language variants.

This is the **course-is-the-credential** model this encyclopedia has met at [Forescout (XV)](../../volume-015-forescout-platform-certifications/README.md) and [Trellix (LXX)](../../volume-070-trellix-certifications/README.md): the badge attests completed training, not a proctored exam.

### 2. The certification tier

A smaller set carries "Certification" or "Certified" in the title with badge metadata to match:

| Credential | Level | Cost flag | Time band |
|:---|:---|:---|:---|
| **Akamai Cloud Computing Foundations Certification** | Foundational | Paid | Hours |
| **Guardicore Certified Segmentation Administrator (GCSA)** | Intermediate | Paid | Hours |
| **GCSA Advanced** | Advanced | — | Days |
| **Guardicore Certified Segmentation Engineer (GCSE)** | Intermediate | Paid | Hours |
| **GCSE – On Premise** | Intermediate | — | Hours |
| **Guardicore Certified Services Provider (GCSP)** – Implementation / Support | Advanced | — | **Weeks** |
| **Akamai API Security – Architect** | Advanced | — | Days |

The Guardicore family is the deepest ladder Akamai runs — administrator and engineer roles, advanced and on-premise variants, and partner services certifications above them — and it maps directly onto this encyclopedia's existing [Guardicore build-it-yourself lab (XCV)](../../volume-095-akamai-guardicore-lab/README.md).

### 3. The partner track

**Akamai Certified Partner: Solutions Architect** badges exist per product — twelve at verification (Ion, App & API Protector, Bot Manager & Account Protector, Edge DNS and GTM, Enterprise Application Access, MFA, Secure Internet Access, Client-side Protection & Compliance, Content Protector, Image and Video Manager, mPulse, AMD & DD) — plus **Partner Foundations/Advanced** badges across four solution areas. Partner-org credentials, same caveat as every other volume: real, and not practitioner certifications.

### 4. Career entry

The **Akamai Technical Academy** partners with Coursera on two professional certificate programs — Network Engineering and Customer Consulting & Support — aimed at people entering the field rather than people running Akamai estates.

## What is and is not published

> **Badge metadata publishes level, a Paid/Free flag, and a time-to-earn band — and that is all.** No exam durations, question counts, or passing scores are public for any Akamai credential; course enrollment runs through Learn Akamai with pricing by arrangement. This volume asserts nothing beyond the published metadata — the discipline from Volumes CXXXIV/CXXXVII/CXL/CXLII, sixth vendor running.

One dead-URL note for anyone following older references: `learn.akamai.com/certification` now redirects to TechDocs. The current program page lives under Akamai University: Customer Enablement on akamai.com.

## Hands-On Lab

The labs in this volume model Akamai concepts in Python at no cost. Akamai Cloud offers a free trial tier, and the platform's TechDocs are public and thorough.

### Lab 1.1 — Sort the 192 badges

**Objective:** Reduce the Credly catalog to what a practitioner can pursue.

```bash
python3 - <<'EOF'
CATALOG = {
  "University course badges (customer)":  ["Web Perf Foundations", "Web Perf & Offload",
      "Media Delivery Foundations", "Bot Manager Foundations", "Bot Manager Advanced",
      "KSD Config & Maintain", "KSD Advanced", "WAAP", "Bot & Abuse Protection",
      "Client-Side Protection & Compliance", "Zero Trust Solutions",
      "Automation and DevOps", "Fraud Management"],
  "Certification tier":                   ["Cloud Computing Foundations Certification",
      "GCSA", "GCSA Advanced", "GCSE", "GCSE On-Premise",
      "GCSP Implementation", "GCSP Support", "API Security - Architect"],
  "Partner track":                        ["Certified Partner: Solutions Architect x12",
      "Partner Foundations x4 areas", "Partner Advanced x4 areas",
      "Guardicore Partner SE/SS"],
  "Career entry (Coursera)":              ["Network Engineering Prof. Certificate",
      "Customer Consulting & Support Prof. Certificate"],
  "Internal/awards (not earnable)":       ["Titans Club", "100 Club", "Instructor MVP",
      "GROW Ambassador", "~130 more employee/community badges"],
}
total_listed = 192
for group, items in CATALOG.items():
    print(f"== {group} ({len(items)} entries shown) ==")
    for i in items: print(f"   {i}")
    print()
practitioner = len(CATALOG["University course badges (customer)"]) + len(CATALOG["Certification tier"])
print(f"Credly issuer total: {total_listed} badges.")
print(f"Practitioner-pursuable (customer courses + certifications): ~{practitioner}.")
print("The rest are partner-org, career-entry, or internal awards — roughly TWO")
print("THIRDS of the catalog is not something a customer engineer can earn.")
print("\nSame lesson as Dynatrace's 34 badges (Vol CXL), at 6x the scale: an issuer")
print("catalog is not a certification path. Sort first, plan second.")
EOF
```

**Expected result:** Roughly 21 practitioner-pursuable credentials inside a 192-badge catalog dominated by internal awards and partner badges. The Dynatrace parallel is exact and the scale is worse — anyone searching "Akamai certification" meets all 192, and the sorting is the first real study skill.

**Negative test:** Planning against a badge you cannot earn — "Technical Mastery: KSD Certification" is a Professional Services credential, not a customer path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Read the metadata bands honestly

**Objective:** Extract every published fact, and only those.

```bash
python3 - <<'EOF'
CERTS = [
  # name,                                  level,         paid,  time_band
  ("Cloud Computing Foundations Cert.",   "Foundational", True,  "Hours"),
  ("GCSA",                                "Intermediate", True,  "Hours"),
  ("GCSA Advanced",                       "Advanced",     None,  "Days"),
  ("GCSE",                                "Intermediate", True,  "Hours"),
  ("GCSE - On Premise",                   "Intermediate", None,  "Hours"),
  ("GCSP Implementation",                 "Advanced",     None,  "Weeks"),
  ("GCSP Support",                        "Advanced",     None,  "Weeks"),
  ("API Security - Architect",            "Advanced",     None,  "Days"),
]
print(f"{'credential':36}{'level':>14}{'paid':>7}{'time':>7}")
for n, lvl, paid, t in CERTS:
    p = {True: "yes", False: "no", None: "n/s"}[paid]
    print(f"{n:36}{lvl:>14}{p:>7}{t:>7}")
print("\nWhat these bands DO tell you:")
print("  - the ladder shape: Foundational -> Intermediate (GCSA/GCSE) -> Advanced")
print("  - GCSP's 'Weeks' band marks it as a partner PROGRAM, not an afternoon exam")
print("  - 'Hours' credentials are course+assessment scale — plan a day, not a month")
print("\nWhat they DO NOT tell you (and nothing public does):")
print("  - exam duration, question count, passing score, retake policy, price")
print("  - 'n/s' means the metadata field is empty, NOT that the thing is free")
print("\nEnrollment runs through Learn Akamai; pricing is by arrangement. Sixth")
print("vendor on this shelf where the only honest posture is: state the bands,")
print("assert nothing else, and treat third-party numbers as invented.")
EOF
```

**Expected result:** Eight credentials with every published fact on one screen, and the two reading rules stated: time bands calibrate planning (Hours vs Days vs Weeks), and an empty cost field is an empty field, not a price. The n/s-is-not-free rule prevents the most tempting wrong inference in the whole table.

**Negative test:** Quoting a "GCSA exam: 60 questions, 70% pass" figure from a search result. No such figures are published anywhere official.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The four credential groups separated, with the internal two-thirds of the catalog set aside.
- [ ] The certification tier's ladder read from level and time bands.
- [ ] The Guardicore family recognized as Akamai's deepest ladder, with an existing lab volume beside it.
- [ ] Unpublished mechanics left unpublished.
- [ ] The Akamai-versus-Cloudflare enterprise/self-serve contrast set up for the chapters ahead.
