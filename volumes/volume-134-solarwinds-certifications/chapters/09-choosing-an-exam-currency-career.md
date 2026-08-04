# Chapter 09: Choosing an Exam, Currency, and Career

## Learning Objectives

- Choose the right SCP exam for the product you operate.
- Prepare using official resources, and avoid the braindump market.
- Place SolarWinds among the encyclopedia's other monitoring and observability volumes.
- Verify the program details that change.

## Choosing an exam

SCP is **product-specific, not tiered**, so the question is what you operate rather than what level you have reached:

| You operate… | Take |
|:---|:---|
| The self-hosted platform, general administration | **Observability Self-Hosted Fundamentals** |
| Network availability and performance monitoring | **Observability Self-Hosted Network Monitoring** |
| Device configuration and change management | **Observability Self-Hosted Network Management** |
| Deployment design, scaling, high availability | **Observability Self-Hosted Architecture & Design** |
| Platform troubleshooting | **Observability Self-Hosted Diagnostics & Troubleshooting** |
| A federal/public-sector deployment | **Observability Self-Hosted Federal Fundamentals** |
| The SaaS platform | **Observability SaaS Fundamentals** |
| Server and application monitoring | **Server and Application Monitor** |
| Database performance tuning | **Database Performance Analyzer** |
| Database administration | **Database Management** |
| IT service management | **Service Desk** |

A sensible sequence for someone running the self-hosted platform: **Fundamentals** first (it establishes the platform vocabulary the other exams assume), then the exam matching your daily work, then **Architecture & Design** or **Diagnostics & Troubleshooting** as you take on design and escalation responsibility.

## Preparing

Use, in order:

1. **The exam preparation guide** for your specific exam — the authoritative scope statement.
2. **Customer Portal training** — virtual and on-demand courses, available if your organization has a product under active maintenance.
3. **Product documentation** and **eLearning videos**.
4. **THWACK** — the community forum, where the questions you have have usually been asked.

And a warning that matters more for this vendor than most: **the search results for SolarWinds certification are dominated by braindump and "practice exam" sites**, many still selling preparation for retired exam codes. SolarWinds states that third-party training is "not reviewed, monitored, or endorsed" by them. Beyond the accuracy problem, using harvested live exam questions violates the exam agreement you accept at PSI check-in and can invalidate your certification. Use the official guide.

## The THWACK points route

Worth repeating from Chapter 01 because it is genuinely unusual: **60,000 THWACK points** exchange for an SCP voucher in the THWACK store, covering the **US$200** fee. Points come from community participation. If you are already active — answering questions, contributing content, joining betas — check your balance before paying. Allow three business days for the voucher email.

## Where SolarWinds sits in the encyclopedia

The monitoring and observability shelf is well populated, and the volumes divide along real lines:

- **SolarWinds (this volume)** — the traditional, broad **IT operations** monitoring suite: network, server, application, database, configuration, service desk, on-premises first.
- [**Datadog XC**](../../volume-090-datadog-certifications/README.md) — cloud-native SaaS observability.
- [**Splunk XLV**](../../volume-045-splunk-certifications/README.md) — log analytics and the security angle.
- [**Prometheus LV**](../../volume-055-prometheus/README.md) and [**OpenTelemetry LIV**](../../volume-054-opentelemetry/README.md) — the open-source metrics and instrumentation standards.
- [**LibreNMS LIII**](../../volume-053-librenms/README.md) — the open-source network monitoring counterpart.
- [**Observability and Enterprise Operations XI**](../../volume-011-observability-enterprise-operations/README.md) — the vendor-neutral discipline.

SolarWinds' distinctive position is **breadth across traditional enterprise IT** and a deep on-premises heritage — which is exactly why the Self-Hosted family dominates its exam list, and why the **Federal Fundamentals** exam exists at all ([Volume LXIII](../../volume-063-public-sector-data-governance/README.md) covers public-sector governance).

## Currency

- **The portfolio was rebranded** around SolarWinds Observability (SaaS and Self-Hosted). Exam names follow the products, so **verify the current exam list** on the SolarWinds Certified Professional program page before booking — third-party material referencing "SCP-NPM" or similar codes is describing the previous scheme.
- **Verify the details this volume deliberately does not assert.** The program page's FAQ covers certification validity period, retake policy, prerequisites, cancellation and rescheduling, and what the exam fee includes. Those answers can change, and they are authoritative only from SolarWinds — read the FAQ directly rather than trusting a secondary summary (including this one).
- **Verified 4 August 2026** from the official program page: the eleven-exam list, the three-step process, PSI Services remote proctoring, the US$200 fee, and the 60,000-point THWACK alternative.

## Hands-On Lab

### Lab 9.1 — Build your SCP plan

**Objective:** Choose an exam and a preparation route.

```bash
cat > my-scp-plan.md <<'EOF'
Platform I operate:   Observability Self-Hosted  /  Observability SaaS  /  both
My daily work:        network monitoring / config management / servers+apps / databases / service desk
Target exam:          SCP: ______________________________________
Prepare with:         (1) that exam's official preparation guide
                      (2) Customer Portal virtual + on-demand training (needs active maintenance)
                      (3) product documentation + eLearning videos
                      (4) THWACK community
Pay with:             US$200  OR  60,000 THWACK points -> SCP Voucher (allow 3 business days)
Book through:         PSI Services (remote proctored) — do the system/compatibility check EARLY
Verify on the official program page before booking:
                      - the current exam list (portfolio was rebranded)
                      - validity period, retake policy, prerequisites, reschedule rules
AVOID:                braindump/"practice exam" sites — inaccurate, often the retired scheme,
                      and using harvested questions violates the PSI exam agreement
EOF
cat my-scp-plan.md
```

**Expected result:** A plan that names one specific exam, sequences official preparation, records both payment routes, and — importantly — lists the facts to verify rather than assuming them. The PSI system check belongs early in the plan: a failed compatibility check on exam day costs you the appointment.

**Negative test:** Preparing from a practice-question dump — beyond the ethical and contractual problem, much of that material targets exams that no longer exist under the rebranded portfolio.

**Cleanup:** Keep the plan.

### Lab 9.2 — Self-assess against the exam domains

**Objective:** Find your weakest area before booking.

```bash
python3 - <<'EOF'
domains = {
  "Platform architecture & collection (ch02)": 3,
  "Network monitoring & availability (ch03)":  4,
  "Config & change management (ch04)":         2,
  "Server & application monitoring (ch05)":    3,
  "Database performance (ch06)":               1,
  "Alerting & noise reduction (ch07)":         2,
  "Dashboards, SLA & capacity (ch08)":         3,
}
print("Self-rated confidence (0-5):\n")
for d, s in sorted(domains.items(), key=lambda kv: kv[1]):
    print(f"{d:44} [{'#'*s}{'.'*(5-s)}] {'STUDY FIRST' if s <= 2 else ('review' if s < 4 else 'ready')}")
print("\nExam mapping:")
print("  Network Monitoring exam       -> ch02, ch03, ch07, ch08")
print("  Network Management exam       -> ch02, ch04, ch07")
print("  Server & Application Monitor  -> ch02, ch05, ch07, ch08")
print("  Database Performance Analyzer -> ch06")
print("  Architecture & Design         -> ch02 (scaling/HA) + ch08 (capacity)")
EOF
```

**Expected result:** Database performance, configuration management, and alerting sort to the top as STUDY FIRST, and the exam mapping converts that into a study order. The mapping is the useful half — a Network Management candidate can see immediately that their weak configuration-management score sits squarely on their exam, while their strong network-monitoring score largely does not.

**Negative test:** Studying the whole volume evenly for a single product exam — the exams are product-scoped, so half the material may be out of scope while your weak in-scope domain stays weak.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A product-matched exam chosen from the eleven, with Fundamentals sequenced first where relevant.
- [ ] Official preparation resources identified and the braindump market avoided.
- [ ] The THWACK points route recorded as an alternative to the fee.
- [ ] SolarWinds placed against Datadog, Splunk, Prometheus, OpenTelemetry, and LibreNMS.
- [ ] Program details flagged for verification on the official page rather than assumed.
