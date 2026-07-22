# Volume XXX — Cisco CCDE Network Design

The CCDE is Cisco's expert certification for network *design* — not
configuration. Where the CCNP tracks in Volumes III and XXV–XXIX teach
you to build and operate technologies, the CCDE certifies the judgment
that decides which technologies, arranged how, to meet a business's
requirements and constraints. This volume teaches that judgment: the
design methodology, the five design domains, the elective technology
areas, and the decision discipline the eight-hour practical exam
demands.

## Overview

This volume is deliberately shaped differently from the rest of the
encyclopedia. The CCDE is closed-book, design-only, and assessed on
**high-level design (HLD)** and business alignment, so there are no
device-configuration labs here. Each chapter instead closes with a
**Design Exercise** — a requirements-and-constraints scenario for
which you produce a design with justified trade-offs — and the
verification sign-off confirms the design meets its requirements and
the trade-offs are defensible, rather than that a lab converged. That
adaptation is the honest one for a design certification; the
`Lab Verification` heading is retained for consistency with the rest
of the encyclopedia, but it verifies a design artifact.

The chapters follow the CCDE's five unified domains, weighted toward
the core enterprise architecture (Network and plane design are 55% of
the exam together), then cover the four practical-exam electives and
the scenario method itself.

## Chapters

1. [The CCDE and the Discipline of Network Design](chapters/01-the-ccde-and-the-discipline-of-network-design.md)
2. [Business Strategy Design](chapters/02-business-strategy-design.md)
3. [Enterprise Campus, WAN, and Edge Design](chapters/03-enterprise-campus-wan-and-edge-design.md)
4. [Routing and Control Plane Design](chapters/04-routing-and-control-plane-design.md)
5. [Data Plane, Management Plane, Automation, and Operational Design](chapters/05-data-plane-management-plane-automation-and-operational-design.md)
6. [Service Design](chapters/06-service-design.md)
7. [Security Design](chapters/07-security-design.md)
8. [Designing for the Electives: AI, Large-Scale, Cloud, and Mobility](chapters/08-designing-for-the-electives-ai-large-scale-cloud-and-mobility.md)
9. [The CCDE Practical: Scenario Method, Trade-offs, and Readiness](chapters/09-the-ccde-practical-scenario-method-trade-offs-and-readiness.md)

## Volume resources

- [Index](INDEX.md) — alphabetized topics with chapter pointers
- [Glossary](GLOSSARY.md) — design terminology introduced in this
  volume

## Related volumes

The CCDE designs at the architecture level what the technology volumes
build. This volume references them as the implementation detail behind
each design decision:

- [Volume III — Cisco Enterprise Networking](../volume-03-cisco-enterprise-networking/README.md)
  and [Volume II — Network Engineering Foundations](../volume-02-network-engineering-foundations/README.md)
  for the campus, routing, and switching being designed.
- [Volume XXVII — Cisco Data Center](../volume-27-cisco-data-center/README.md)
  for the AI-infrastructure elective's fabrics.
- [Volume XXIX — Cisco Service Provider](../volume-29-cisco-service-provider/README.md)
  for the large-scale-networks elective's routing and segment
  routing.
- [Volume XVI — Palo Alto Networks Security](../volume-16-palo-alto-networks-security/README.md)
  and [Volume X — Enterprise Cybersecurity](../volume-10-enterprise-cybersecurity/README.md)
  for the security-design domain and the mobility elective's SASE.

## Certification alignment

This volume maps to the **CCDE** — Cisco Certified Design Expert — as
recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The
CCDE is an expert-level design certification with two exams: a
qualifying **Written** exam and a scenario-based **Practical** exam,
sharing one unified set of exam topics. Chapter content describes
blueprint domains and points to Cisco's official sources; it does not
reproduce proprietary exam content.

### The exams

| Exam | Format | Duration | Role |
| --- | --- | --- | --- |
| **CCDE Written (400-007)** v3.1 | Multiple-choice, 90–110 questions | 2 hours | Qualifying exam — must pass before scheduling the Practical |
| **CCDE Practical** v3.1 | Scenario-based design exam | 8 hours | Three Core (Enterprise) modules plus one elective module |

Both exams are **closed book** — no outside reference materials — and
both are assessed against the same unified exam topics. The Practical
is delivered on set dates through Pearson VUE; confirm current
scheduling, prerequisites, and pricing with Cisco at registration.

**The elective (Practical, fourth module).** At the start of the
Practical you select one elective, which determines the fourth
scenario module; the first three are always Core Enterprise. The four
electives are **AI Infrastructure**, **Large Scale Networks**,
**On-Prem and Cloud Services**, and **Workforce Mobility** — covered
in Chapter 08.

### Domain weights (unified — Written and Practical)

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Business Strategy Design | 15% | 02 |
| 2.0 Control, Data, Management Plane, and Operational Design | 25% | 04, 05 |
| 3.0 Network Design | 30% | 03, 04 |
| 4.0 Service Design | 15% | 06 |
| 5.0 Security Design | 15% | 07 |

Version 3.1 added **artificial-intelligence and machine-learning
topics, including generative AI**, across the domains and as a
dedicated Practical elective — the design implications of AI
infrastructure and AI-assisted operations are now examinable.

### Study plan

The CCDE rewards breadth of design experience over memorization, so
this plan assumes a reader who already holds or has the knowledge of a
CCNP and is now learning to *design* rather than configure. Roughly
**twelve to sixteen weeks** at 8–10 hours per week for the Written,
then dedicated scenario practice for the Practical.

| Weeks | Focus | Chapters |
| --- | --- | --- |
| 1 | The design discipline: HLD versus LLD, requirements, constraints, trade-offs | 01 |
| 2 | Business strategy: alignment, methodologies, continuity, cost and risk | 02 |
| 3–5 | **The heavy block (Network Design, 30%).** Campus/WAN/edge architecture, then routing and control-plane design | 03, 04 |
| 6–7 | Data and management plane, automation, and operational design (the rest of the 25% domain) | 05 |
| 8 | Service design: overlays, VPNs, QoS, multicast, SD-WAN/SD-Access | 06 |
| 9 | Security design: zero trust, segmentation, security-by-design | 07 |
| 10 | The four electives at design level; choose and go deep on one | 08 |
| 11–12 | Scenario method: practice full design scenarios under time, with trade-off justification | 09 |
| 13+ | Practical preparation: repeated timed scenarios in the chosen elective | 09 |

The single most important habit — and the one Chapter 09 drills — is
**justifying every design decision from a requirement or constraint**.
The Practical does not reward the "best" technology; it rewards the
design that best fits the stated business and technical context, with
the reasoning made explicit.

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | [Cisco Learning Network CCDE v3.1 unified exam topics](https://learningnetwork.cisco.com/s/ccde-v3-1-unified-exam-topics) | Authority on domains, weights, electives, and format |
| Reference text | Cisco Press *CCDE v3 Study Guide* and the design-focused Cisco Press library | Design-reasoning oriented rather than configuration oriented |
| Design references | Cisco Validated Designs (CVDs), SRND/Preferred Architecture guides | How Cisco itself documents design decisions and trade-offs |
| Practice | Full scenario walkthroughs (Cisco U. and reputable CCDE-specific providers) | The Practical is a scenario skill; it is built by doing scenarios, not reading |
| Breadth | The technology volumes of this encyclopedia (see Related volumes) | The implementation detail behind each design decision |

## Practicing

There is nothing to configure and therefore nothing to lab in the
device sense — the CCDE is exercised on paper (or whiteboard). Practice
by taking real or realistic requirements, drawing the high-level
design, and — critically — writing the **trade-off rationale**: what
you chose, what you rejected, and which requirement or constraint
drove each decision. The Design Exercises in each chapter are built
this way, and Chapter 09 assembles them into full-scenario practice
under time pressure, which is the closest analog to the Practical
exam.

## Software and platform baseline

This volume is technology- and version-agnostic by nature — it designs
architectures, not releases — but where it references implementing
technologies it assumes the dated baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) and the technology
volumes cross-referenced above.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format html --volume volume-30-cisco-ccde-network-design
```
