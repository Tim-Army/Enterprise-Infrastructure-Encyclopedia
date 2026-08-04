# Volume CXXXIV — Glossary

| Term | Definition |
|:---|:---|
| **Additional polling engine (APE)** | An extra collector deployed for capacity *or* for reachability into a network the primary cannot poll — two distinct reasons. |
| **Alert fatigue** | The state where alert volume so exceeds actionable signal that responders stop reading alerts, making the platform worse than useless. |
| **Availability** | Uptime over total time, expressed as a percentage; meaningful only alongside the polling interval and the maintenance-exclusion rule. |
| **Baseline threshold** | An alert threshold derived from a metric's own historical mean and deviation rather than a global round number. |
| **Configuration drift** | Divergence between the approved configuration baseline and what is actually running — often with no operational symptom. |
| **Component monitor** | A single check within an application template (HTTP response, query result, service state, disk space). |
| **Discards** | Frames dropped despite arriving intact — a congestion or policy signal, distinct from errors. |
| **Error budget** | The downtime an SLA target permits over a period, expressed in minutes; the operational form of an availability percentage. |
| **Errors (CRC/FCS)** | Corrupted frames, indicating a physical-layer fault (cable, optic, connector, duplex) independent of utilization. |
| **Hysteresis** | Clearing an alert at a lower value than it triggers at, preventing flapping when a metric hovers at the threshold. |
| **Observability SaaS / Self-Hosted** | The two editions of the rebranded SolarWinds portfolio; Self-Hosted is the on-premises Orion lineage and dominates the exam list. |
| **Percentile (p95/p99)** | The value below which that share of measurements fall; reveals the tail latency an average conceals. |
| **PSI Services** | The testing partner delivering SCP exams via proprietary remote proctoring, with ID, environment, and compatibility checks. |
| **Rollup** | Combining component-monitor states into one application status, weighted by criticality so degraded is distinguished from down. |
| **Runway** | Time until a resource is exhausted at its current growth rate; actionable only when compared against procurement lead time. |
| **SCP** | SolarWinds Certified Professional — the credential, earned per product-specific exam rather than through a tiered ladder. |
| **Signal ratio** | Alerts acted on divided by total alerts; the metric for whether alerting is worth reading. Check alongside coverage. |
| **SNMPv3** | The authenticated, encrypted version of SNMP; v1/v2c send community strings in clear text. |
| **Template** | A reusable set of component monitors for an application type, giving consistent checks across every instance. |
| **THWACK** | SolarWinds' user community; 60,000 THWACK points exchange for an SCP voucher covering the US$200 exam fee. |
| **Wait-time analysis** | Attributing a query's elapsed time to what it waited on (CPU, I/O, locks, log), which points directly at the remedy where utilization metrics do not. |
