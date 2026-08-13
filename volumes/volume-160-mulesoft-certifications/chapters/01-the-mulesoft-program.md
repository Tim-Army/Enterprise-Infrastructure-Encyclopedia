# Chapter 01: The MuleSoft Certification Program

![The MuleSoft certification program and the Anypoint Platform beneath it. MuleSoft is the API and integration platform owned by Salesforce, and its certifications are branded Salesforce Certified MuleSoft credentials across three families. The Associate family has the MuleSoft Integration Foundations certification for core integration and API-led connectivity terminology. The Developer family has the MuleSoft Developer certification for designing, building, testing, deploying, and managing basic APIs and integrations, the MuleSoft Developer II certification for production-ready Mule applications in a DevOps environment, and the MuleSoft Hyperautomation Developer certification. The Architect family has the MuleSoft Catalyst Consultant certification for the Catalyst delivery methodology, the MuleSoft Platform Architect certification for defining an organization's Anypoint Platform strategy, delivered as sixty questions in ninety minutes with a seventy percent passing score for four hundred dollars, and the MuleSoft Platform Integration Architect certification. The platform beneath is the Anypoint Platform, built around API-led connectivity, a three-layer architecture of System, Process, and Experience APIs forming a reusable application network, with DataWeave, CloudHub, and API Manager.](../../../diagrams/volume-160-mulesoft-certifications/chapter-01-program.svg)

*Figure 1-1. The Salesforce-branded MuleSoft certifications and the Anypoint Platform they validate.*

## Learning Objectives

- Describe the MuleSoft certification program — Associate, Developer, Architect families.
- Place the seven certifications and their focus.
- State the exam mechanics (e.g., Platform Architect — 60 questions, 70%, $400).
- Recognize MuleSoft's position as the integration platform owned by Salesforce.

## What MuleSoft is

MuleSoft is a leader in **API-led integration** — its **Anypoint Platform** connects applications, data, and devices by building and managing **APIs** and integrations. MuleSoft is **owned by Salesforce** (acquired 2018), so its certifications are branded **Salesforce Certified MuleSoft** credentials, delivered through Salesforce's certification program. The core idea MuleSoft champions is **API-led connectivity** ([Chapter 2](02-api-led-connectivity.md)) — composing reusable APIs into an **application network** instead of brittle point-to-point integrations. MuleSoft sits alongside the rest of the [Salesforce ecosystem (LXXXIII)](../../volume-083-salesforce-certifications/README.md) as its **integration layer**. The lab models the program.

## The program

The certifications are organized into **three families**:

| Family | Certification | Focus |
|:---|:---|:---|
| **Associate** | MuleSoft Integration Foundations | Core integration + API-led connectivity terminology (entry) |
| **Developer** | MuleSoft Developer | Design, build, test, deploy, manage basic APIs and integrations |
| | MuleSoft Developer II | Production-ready Mule apps in a DevOps environment |
| | MuleSoft Hyperautomation Developer | Hyperautomation across Salesforce + MuleSoft |
| **Architect** | MuleSoft Catalyst Consultant | The Catalyst delivery methodology |
| | MuleSoft Platform Architect | Defining an org's Anypoint Platform strategy |
| | MuleSoft Platform Integration Architect | Translating requirements into integration implementations |

The families rise from **knowledge** (Associate) through **building** (Developer) to **strategy and delivery** (Architect). The lab maps the program.

## Exam mechanics

Exams are multiple-choice, proctored. As a representative example, the **Platform Architect** exam publishes precise mechanics:

| Element | Value (Platform Architect) |
|:---|:---|
| **Questions** | **60** multiple-choice |
| **Duration** | **90 minutes** |
| **Passing score** | **70%** |
| **Fee** | **$400 USD** (one complimentary retake) |
| **Domains** | 9 — from Application Network Basics through Monitoring and Analyzing Application Networks |

The domains trace the whole platform lifecycle — foundations, designing and sharing APIs, integration patterns, managing APIs, deploying to CloudHub, quality, and monitoring — reflecting that MuleSoft validates end-to-end **platform** competence, not just coding. The lab models the rule set.

## The certification families

The middle chapters follow the platform: [API-led connectivity (Ch 2)](02-api-led-connectivity.md), [the Anypoint Platform (Ch 3)](03-the-anypoint-platform.md), [designing APIs (Ch 4)](04-designing-apis.md), [building integrations (Ch 5)](05-building-integrations.md), [DataWeave (Ch 6)](06-dataweave.md), [deploying and managing (Ch 7)](07-deploying-and-managing.md), and [hyperautomation and Catalyst (Ch 8)](08-hyperautomation-and-catalyst.md). [Chapter 9](09-choosing-your-mulesoft-path.md) sequences a path from Associate to Architect. The lab situates the certifications.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the certification families

**Objective:** Represent the three families and their certifications.

```bash
python3 - <<'EOF'
PROGRAM = {
  "Associate": [("MuleSoft Integration Foundations", "core integration + API-led terminology (entry)")],
  "Developer": [
    ("MuleSoft Developer", "design/build/test/deploy/manage basic APIs + integrations"),
    ("MuleSoft Developer II", "production-ready Mule apps in a DevOps environment"),
    ("MuleSoft Hyperautomation Developer", "hyperautomation across Salesforce + MuleSoft"),
  ],
  "Architect": [
    ("MuleSoft Catalyst Consultant", "the Catalyst delivery methodology"),
    ("MuleSoft Platform Architect", "define an org's Anypoint Platform strategy"),
    ("MuleSoft Platform Integration Architect", "translate requirements into integration implementations"),
  ],
}
print("MuleSoft certifications (Salesforce-branded) — three families:\n")
total = 0
for family, certs in PROGRAM.items():
    print(f"   {family}:")
    for name, focus in certs:
        print(f"      - Salesforce Certified {name}")
        print(f"          {focus}")
        total += 1
    print()
print(f"   {total} certifications\n")
print("Platform Architect exam (verified): 60 questions / 90 min / 70% to pass / $400 (1 free retake).")
print("\nThe arc: ASSOCIATE (know) -> DEVELOPER (build) -> ARCHITECT (strategy + delivery). MuleSoft")
print("is OWNED BY SALESFORCE (acq. 2018) -> certs are 'Salesforce Certified MuleSoft ...'. The")
print("platform validates END-TO-END integration competence: API-led connectivity on the Anypoint")
print("Platform, not just coding. Hyperautomation Developer + Catalyst Consultant are newer additions.")
EOF
```

**Expected result:** The seven certifications across Associate (Integration Foundations), Developer (Developer, Developer II, Hyperautomation Developer), and Architect (Catalyst Consultant, Platform Architect, Integration Architect) families, with the Platform Architect mechanics. The program lesson is that MuleSoft's Salesforce-branded certifications rise from knowledge to building to strategy/delivery, validating end-to-end integration competence on the Anypoint Platform.

**Negative test:** Expecting a single "MuleSoft Certified" exam. The program spans three families and seven role-based certifications from Integration Foundations to Platform Architect; you certify for your role along the develop-to-architect path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — The Platform Architect domains trace the lifecycle

**Objective:** See that the exam domains span the whole platform.

```bash
python3 - <<'EOF'
DOMAINS = [
  ("Application Network Basics", 11), ("Org & Platform Foundations", 17),
  ("Designing & Sharing APIs", 11), ("Applying Integration Patterns", 11),
  ("Managing APIs", 12), ("Architecting & Deploying API Implementations", 11),
  ("Deploying to CloudHub", 11), ("Meeting API Quality Goals", 8),
  ("Monitoring & Analyzing Application Networks", 8),
]
total = sum(w for _, w in DOMAINS)
print("Platform Architect — 9 weighted domains (the full platform lifecycle):\n")
for name, w in DOMAINS:
    print(f"   {w:>2}%  {'#'*(w//2)} {name}")
print(f"\n   total: {total}%")
print("\nThe domains trace END TO END: FOUNDATIONS (org/platform setup) -> DESIGN + SHARE APIs")
print("-> integration PATTERNS -> MANAGE APIs -> DEPLOY (to CloudHub) -> QUALITY -> MONITOR the")
print("application network. That's PLATFORM competence, not just writing a flow. The heaviest")
print("weight is FOUNDATIONS (17%) — getting the org + platform strategy right is the architect's")
print("core job, exactly what API-led connectivity (Ch 2) and the application network are about.")
EOF
```

**Expected result:** The nine Platform Architect domains summing to 100%, tracing the platform lifecycle from foundations (heaviest at 17%) through designing, managing, deploying to CloudHub, quality, and monitoring. The lesson is that the exam validates end-to-end platform competence — organizational and platform strategy, API design and management, deployment, and monitoring the application network — not just building a single integration.

**Negative test:** Preparing only to build a Mule flow for the architect exam. The domains span foundations, design, management, deployment, quality, and monitoring of the whole application network; architect competence is platform-wide strategy, not a single implementation.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The program understood — Associate, Developer, and Architect families of Salesforce-branded MuleSoft certifications.
- [ ] The seven certifications placed against their focus.
- [ ] The exam mechanics known (Platform Architect — 60 questions, 90 minutes, 70%, $400, 9 domains).
- [ ] MuleSoft recognized as Salesforce's integration platform, built on API-led connectivity.
