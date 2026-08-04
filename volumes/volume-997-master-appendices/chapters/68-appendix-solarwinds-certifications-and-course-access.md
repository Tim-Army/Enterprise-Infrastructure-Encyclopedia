# Chapter 68: Appendix — SolarWinds Certifications and Course Access

The **SolarWinds Certified Professional (SCP)** program — exams, delivery, and access model. Verified on
**4 August 2026** from the official **SolarWinds Certified Professional Program** page
(support.solarwinds.com), the source that anchors [Volume CXXXIV — SolarWinds Certification
Tracks](../../volume-134-solarwinds-certifications/README.md).

> **Sourcing note.** Search results for SolarWinds certification are dominated by braindump and
> "practice exam" sites, many still selling preparation for **retired** exam codes from before the
> portfolio was rebranded. All of those were excluded. SolarWinds itself states that training and
> materials from third parties are **"not reviewed, monitored, or endorsed"** by them — and using
> harvested live exam questions violates the exam agreement accepted at PSI check-in.

**How access works.** SCP is a **single credential earned per product-specific exam** — there is no
tiered ladder. SolarWinds describes the process as **three easy steps**:

1. **Sign up** — register with SolarWinds and watch for the confirmation email with account and
   testing-service instructions.
2. **Study** — each exam has its own **preparation guide**. Customers with a product under **active
   maintenance** can access **virtual and on-demand training** by logging into the **Customer Portal**.
3. **Schedule** — create an account with **PSI Services** and book the exam.

**Delivery.** Exams are delivered through **PSI Services** proprietary **remote proctoring** ("anywhere,
anytime testing with integrity"). Expect identification checks, environment and system requirements, a
**compatibility check** to run *before* exam day, published admission rules and violation policies, and
availability of special accommodations.

**Fees.** **US$200** — or, distinctively, **60,000 THWACK points**. Members of SolarWinds' **THWACK**
community can select an **SCP Voucher** in the THWACK store; the voucher code arrives by email within
**three business days** and is applied at PSI checkout. For active community contributors this makes the
exam effectively free.

> **Currency.** The portfolio has been **rebranded around SolarWinds Observability**, split into **SaaS**
> and **Self-Hosted** (the on-premises Orion lineage), and the exam names follow the products. Verify the
> current exam list on the program page before booking. The page's FAQ also covers **certification
> validity, retake policy, prerequisites, rescheduling, and what the fee includes** — read those directly
> rather than trusting any secondary summary, including this appendix.

## Free and low-cost resources and entry points

- **[SolarWinds Certified Professional Program](https://support.solarwinds.com/solarwinds-certified-professional-program)** — the authoritative program page: exam list, study guides, registration, FAQs
- **Exam preparation guides** — one per exam, the correct starting point for study
- **Customer Portal** — virtual and on-demand training (requires a product under active maintenance)
- **Product documentation**, **virtual classrooms**, and **eLearning videos**
- **[THWACK community](https://thwack.solarwinds.com/)** — forums, and the points route to a free exam voucher
- **Free study lab:** any host with `python3` models the disciplines the exams test — polling and collection, availability and error budgets, utilization versus errors, configuration drift and compliance, application health rollup, database wait-time analysis, dependency-aware alerting, percentiles, and capacity runway (see the volume's labs); no SolarWinds software needed

## The eleven current exams

Verified against the official "Find Your Exam" list on 4 August 2026.

| Exam | Domain |
| --- | --- |
| SolarWinds Observability SaaS Fundamentals | The SaaS observability platform |
| SolarWinds Observability Self-Hosted Fundamentals | The self-hosted platform (Orion lineage) |
| SolarWinds Observability Self-Hosted Network Monitoring | Availability, performance, interfaces, topology |
| SolarWinds Observability Self-Hosted Network Management | Configuration backup, drift, compliance, change |
| SolarWinds Observability Self-Hosted Architecture & Design | Deployment design, scaling, high availability |
| SolarWinds Observability Self-Hosted Diagnostics & Troubleshooting | Diagnosing the platform itself |
| SolarWinds Observability Self-Hosted Federal Fundamentals | The federal/public-sector variant |
| SolarWinds Server and Application Monitor | Server, application, and hardware monitoring (SAM) |
| SolarWinds Database Performance Analyzer | Wait-time analysis and query tuning |
| SolarWinds Database Management | Database administration and health |
| SolarWinds Service Desk | IT service management |

## Notes

- **Product-specific, not tiered:** choose by what you operate. A reasonable sequence for a self-hosted
  shop is **Fundamentals** first (it establishes vocabulary the other exams assume), then the exam
  matching your daily work, then **Architecture & Design** or **Diagnostics & Troubleshooting**.
- **The Federal Fundamentals exam** reflects the distinct compliance and accreditation constraints of
  public-sector deployments — see [Volume LXIII](../../volume-063-public-sector-data-governance/README.md).
- **The THWACK points route is unusual** among vendor programs and worth checking before paying: sustained
  community participation converts directly into a free certification attempt.
- **Position among the encyclopedia's monitoring volumes:** SolarWinds offers the greatest **breadth across
  traditional enterprise IT** with an on-premises heritage, alongside
  [Datadog XC](../../volume-090-datadog-certifications/README.md) (cloud-native SaaS),
  [Splunk XLV](../../volume-045-splunk-certifications/README.md) (logs/security),
  [Prometheus LV](../../volume-055-prometheus/README.md) and
  [OpenTelemetry LIV](../../volume-054-opentelemetry/README.md) (open standards), and
  [LibreNMS LIII](../../volume-053-librenms/README.md) (open-source network monitoring).
