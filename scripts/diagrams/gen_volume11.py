import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-11-observability-enterprise-operations"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Hands-On Lab: A Service Catalog Completeness Audit That Fails Closed",
        subtitle="Two complete entries pass silently; an unowned legacy service is flagged and the script exits non-zero",
        svg_title="Chapter 1 lab flow: an automated service-catalog completeness audit catching missing ownership and escalation metadata",
        svg_desc="Three catalog-info.yaml entries are created: checkout-api and inventory-service are complete "
                  "with an owner and a PagerDuty escalation annotation, while legacy-reporting deliberately omits "
                  "both. audit-catalog.sh reports MISSING OWNER and MISSING ESCALATION ROUTE for legacy-reporting, "
                  "'2 issue(s) found', and exits 2. As a negative test, confirming echo $? returns 2 (not 0) shows "
                  "a CI gate would correctly fail the build; separately, truncating inventory-service's YAML to "
                  "corrupt it and re-running confirms the script errors clearly rather than silently treating the "
                  "broken entry as compliant.")
    c.node_box(60, 140, 260, 120, "alt", [
        Line("checkout-api / inventory-service", 12, 700, "#111827"),
        Line("owner + escalation present", 10.5, 400, "#374151"),
        Line("audit: no findings", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 140, 240, 120, "warn", [
        Line("legacy-reporting", 12.5, 700, "#111827"),
        Line("no owner, no escalation route", 10.5, 700, "#7f1d1d"),
        Line("audit: 2 issues found, exit 2", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 200, 380, 200, "alt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("corrupted YAML (truncated)", 10.5, 700, "#7f1d1d"),
        Line("errors clearly, not silently OK", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("echo $? returns 2, not 0 — a CI pipeline gate on this script correctly fails the build when", 11.5, 400, "#374151"),
        Line("ownership metadata is incomplete, rather than merging a service with no accountable owner.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("alt", "Complete catalog entry"), ("warn", "Incomplete / corrupted entry")])
    c.save(f"{OUT}/chapter-01-service-catalog-audit-flow.svg")


def ch02():
    c = Canvas(960, 620,
        title="Chapter 2 Hands-On Lab: OpenTelemetry Collector Buffering Under Backend Backpressure",
        subtitle="A synthetic trace reaches Jaeger end to end; stopping Jaeger doesn't error the sender, it grows the exporter queue instead",
        svg_title="Chapter 2 lab topology: an OpenTelemetry Collector pipeline exporting to Prometheus and Jaeger, tested against a Jaeger outage",
        svg_desc="A synthetic trace sent to the Collector's OTLP HTTP receiver is exported to Jaeger and confirmed "
                  "via the Jaeger UI search; otelcol_receiver_accepted_spans_total in Prometheus confirms at least "
                  "one span was accepted end to end. As a negative test, the Jaeger container is stopped and "
                  "another trace is sent; the Collector still returns HTTP 200 to the sender rather than erroring, "
                  "and the Collector's own self-telemetry shows the otlp/jaeger exporter's queue size growing "
                  "nonzero with each additional send — the buffering-under-backpressure behavior. Restarting "
                  "Jaeger drains the queue back toward zero within the configured retry interval.")
    c.node_box(60, 150, 220, 100, "mgmt", [
        Line("Synthetic trace (curl)", 12.5, 700, "#111827"),
        Line("OTLP HTTP :4318", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 130, 220, 140, "alt", [
        Line("OTel Collector", 13, 700, "#111827"),
        Line("receivers → batch processor", 10.5, 400, "#374151"),
        Line("exporters: prometheus, otlp/jaeger", 10.5, 400, "#374151"),
        Line("self-telemetry :8888", 10, 400, "#374151"),
    ])
    c.node_box(700, 130, 220, 70, "alt", [
        Line("Prometheus", 12.5, 700, "#111827"),
        Line("accepted_spans_total ≥ 1", 10, 700, "#14532d"),
    ])
    c.node_box(700, 230, 220, 90, "warn", [
        Line("Jaeger (negative test)", 12, 700, "#111827"),
        Line("stopped → queue grows", 10.5, 700, "#7f1d1d"),
        Line("restarted → queue drains", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(280, 200, 370, 200, "mgmt")
    c.connector(590, 175, 700, 165, "alt")
    c.connector(590, 230, 700, 265, "warn")
    c.node_box(60, 400, 860, 90, "neutral", [
        Line("curl to the OTLP receiver still returns 200 while Jaeger is down — the sender never sees the backend outage;", 11.5, 400, "#374151"),
        Line("otelcol_exporter_queue_size for otlp/jaeger is the signal that reveals the backpressure instead.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 530, [("mgmt", "Trace ingestion"), ("alt", "Healthy export path"), ("warn", "Backend outage (buffered)")])
    c.save(f"{OUT}/chapter-02-otel-collector-backpressure-topology.svg")


def ch03():
    c = Canvas(960, 580,
        title="Chapter 3 Hands-On Lab: A Burn-Rate Alert That Distinguishes Fast-Burn From Budget-Compliant",
        subtitle="A 2% error rate fires the SLO alert; the same alert returns to inactive once errors drop under the threshold",
        svg_title="Chapter 3 lab flow: a Prometheus multi-window burn-rate SLO alert validated against both a burning and a healthy error rate",
        svg_desc="lab-app injects a 2% error rate and a 5% slow-tail. slo:sli_error:ratio_rate5m reports "
                  "approximately 0.02, and because this exceeds the 14.4 x 0.1% = 1.44% page threshold, "
                  "LabAppAvailabilitySLOBurn is firing. As a negative test, the error probability is lowered to "
                  "0.05% (well under the 0.1% SLO) and the app rebuilt and restarted; after five minutes, "
                  "slo:sli_error:ratio_rate5m reports approximately 0.0005, well under the 0.0144 burn-rate "
                  "threshold, and LabAppAvailabilitySLOBurn returns to inactive — confirming the alert "
                  "distinguishes a genuine fast-burn condition from normal, budget-compliant operation rather than "
                  "firing on any nonzero error rate.")
    c.node_box(60, 140, 260, 120, "warn", [
        Line("lab-app: 2% error injection", 12.5, 700, "#111827"),
        Line("slo:sli_error:ratio_rate5m ≈ 0.02", 10.5, 400, "#374151"),
        Line("2% > 1.44% page threshold", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(380, 140, 240, 120, "warn", [
        Line("LabAppAvailabilitySLOBurn", 12, 700, "#111827"),
        Line("state: firing", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 200, 380, 200, "warn")
    c.node_box(700, 140, 220, 120, "alt", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("error rate lowered to 0.05%", 10.5, 700, "#14532d"),
        Line("ratio ≈ 0.0005 < 0.0144", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 200, 700, 200, "alt")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("LabAppAvailabilitySLOBurn returns to inactive — the alert fires on the burn-rate threshold specifically,", 11.5, 400, "#374151"),
        Line("not on any nonzero error rate, correctly distinguishing genuine fast-burn from healthy operation.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("warn", "Burning error budget"), ("alt", "Healthy, below threshold")])
    c.save(f"{OUT}/chapter-03-slo-burn-rate-alert-flow.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: PII Redaction Enforced by the Pipeline Transform, Not by Convention",
        subtitle="The authorization field never reaches Loki while the redact transform is active — and reappears the instant it is removed",
        svg_title="Chapter 4 lab flow: a Vector-to-Loki log pipeline redacting a sensitive field before ingestion, tested with the transform removed",
        svg_desc="emit-logs.sh writes 21 structured JSON log lines, one carrying an authorization bearer token. "
                  "Vector parses each line as JSON and removes the authorization field before shipping to Loki. "
                  "Querying Loki confirms all 21 entries arrived and the authorization field is absent even from "
                  "the one entry that originally carried it. As a negative test, querying specifically for a "
                  "non-empty authorization field returns zero results, confirming enforcement rather than mere "
                  "display omission. Commenting out the del(.authorization) line in vector.toml, restarting "
                  "Vector, and re-emitting logs causes the same query to return the previously redacted value in "
                  "plain text — the pipeline does not protect sensitive fields on its own, the transform does.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("emit-logs.sh", 12.5, 700, "#111827"),
        Line("21 JSON lines, 1 with", 10.5, 400, "#374151"),
        Line("authorization: Bearer ...", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Vector: parse + redact", 12.5, 700, "#111827"),
        Line("del(.authorization) transform", 10.5, 700, "#1d4ed8"),
        Line("field removed before Loki sink", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Loki", 12.5, 700, "#111827"),
        Line("21 entries, authorization", 10.5, 700, "#14532d"),
        Line("absent from all of them", 10.5, 400, "#374151"),
    ])
    c.connector(620, 195, 700, 195, "alt")
    c.node_box(60, 330, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("query specifically for authorization != \"\" against Loki → zero results (redaction is enforced)", 11, 400, "#7f1d1d"),
        Line("del(.authorization) commented out, Vector restarted, logs re-emitted →", 11, 400, "#7f1d1d"),
        Line("same query now returns the token in plain text — the transform, not the pipeline, was protecting it", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Raw log source"), ("alt", "Redacted, enforced")])
    c.save(f"{OUT}/chapter-04-vector-loki-pii-redaction-flow.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: Tail Sampling That Actually Discards Routine Traffic",
        subtitle="All errors and slow traces are retained; only about 10% of the 90 fast/successful traces survive sampling",
        svg_title="Chapter 5 lab flow: a tail-sampling policy retaining every error and slow trace while probabilistically discarding routine traffic",
        svg_desc="100 synthetic traces are sent: 90 fast/successful, 5 slow (over 800ms), and 5 errors. The "
                  "Collector's tail_sampling processor retains all traces matching keep-errors or keep-slow "
                  "policies, and samples only 10% of everything else via baseline-sample. Jaeger shows "
                  "approximately 19-20 retained traces: all 5 slow, all 5 error, and roughly 9 of the 90 fast/"
                  "successful traces. As a negative test, counting the retained fast/successful traces "
                  "specifically confirms the count is well under 90 (roughly 5-15) rather than close to 90 — a "
                  "count near 90 would mean the baseline-sample policy was unreachable due to an inverted earlier "
                  "policy, defeating the cost control tail sampling exists to provide.")
    c.node_box(60, 140, 260, 130, "mgmt", [
        Line("100 synthetic traces", 12.5, 700, "#111827"),
        Line("90 fast/OK, 5 slow, 5 error", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 130, 260, 150, "alt", [
        Line("tail_sampling processor", 12.5, 700, "#111827"),
        Line("keep-errors: status_code", 10.5, 400, "#374151"),
        Line("keep-slow: latency > 800ms", 10.5, 400, "#374151"),
        Line("baseline-sample: 10% of rest", 10.5, 700, "#1d4ed8"),
    ])
    c.connector(320, 205, 400, 205, "mgmt")
    c.node_box(720, 130, 200, 150, "alt", [
        Line("Jaeger", 12.5, 700, "#111827"),
        Line("~19-20 retained:", 10.5, 400, "#374151"),
        Line("5 slow + 5 error + ~9 sampled", 10, 700, "#14532d"),
    ])
    c.connector(660, 205, 720, 205, "alt")
    c.node_box(60, 340, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("count fast/successful traces retained specifically → well under 90 (roughly 5-15)", 11, 400, "#7f1d1d"),
        Line("a count near 90 would mean baseline-sample is unreachable — every trace retained regardless of", 11, 400, "#7f1d1d"),
        Line("sampling percentage, defeating tail sampling's cost-control purpose", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 510, [("mgmt", "Traffic mix sent"), ("alt", "Correctly sampled result"), ("warn", "Misconfiguration this test catches")])
    c.save(f"{OUT}/chapter-05-tail-sampling-retention-flow.svg")


def ch06():
    c = Canvas(960, 620,
        title="Chapter 6 Hands-On Lab: Alertmanager Grouping and Node-Scoped Inhibition",
        subtitle="Three pod alerts on one node collapse into a single notification; a NodeDown alert suppresses new pod alerts for that node only",
        svg_title="Chapter 6 lab flow: Alertmanager grouping three related alerts into one notification, then a node-scoped inhibition rule tested against two nodes",
        svg_desc="Three PodUnavailable alerts for different pods on node-7 are fired together; the webhook sink "
                  "receives a single notification payload containing all three, grouped by [alertname, service] "
                  "as configured. As a negative test, a NodeDown alert for node-7 is fired, then a new "
                  "PodUnavailable alert for node-7; the count of PodUnavailable notifications after NodeDown fired "
                  "is 0 — inhibited because the matching NodeDown alert shares the node label. Repeating with "
                  "PodUnavailable on node-8 (no active NodeDown there) confirms that notification IS delivered, "
                  "showing the inhibition correctly scopes to the matching node label rather than suppressing all "
                  "PodUnavailable alerts globally.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("3x PodUnavailable, node-7", 12.5, 700, "#111827"),
        Line("different pods, same node", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Alertmanager grouping", 12.5, 700, "#111827"),
        Line("group_by [alertname, service]", 10.5, 400, "#374151"),
        Line("→ 1 notification, 3 alerts", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "neutral", [
        Line("webhook sink", 12.5, 700, "#111827"),
        Line("received.jsonl: 1 payload", 10.5, 400, "#374151"),
    ])
    c.connector(620, 195, 700, 195, "alt")
    c.node_box(60, 330, 420, 130, "warn", [
        Line("Negative Test: node-7", 12, 700, "#7f1d1d"),
        Line("NodeDown(node-7) fires, then", 10.5, 400, "#7f1d1d"),
        Line("PodUnavailable(node-7) fires", 10.5, 400, "#7f1d1d"),
        Line("0 PodUnavailable notifications", 10.5, 700, "#7f1d1d"),
        Line("(inhibited by matching node label)", 10, 400, "#7f1d1d"),
    ])
    c.node_box(500, 330, 420, 130, "alt", [
        Line("Control: node-8", 12, 700, "#111827"),
        Line("PodUnavailable(node-8) fires", 10.5, 400, "#374151"),
        Line("no active NodeDown on node-8", 10.5, 400, "#374151"),
        Line("notification IS delivered", 10.5, 700, "#14532d"),
    ])
    c.legend(60, 500, [("mgmt", "Grouped source alerts"), ("alt", "Delivered notification"), ("warn", "Inhibited (scoped correctly)")])
    c.save(f"{OUT}/chapter-06-alertmanager-grouping-inhibition-flow.svg")


def ch07():
    c = Canvas(960, 620,
        title="Chapter 7 Hands-On Lab: Postmortem Coverage and Change-Approval Gates That Fail Closed",
        subtitle="A SEV1 incident missing its postmortem is caught by the audit; an under-approved change is blocked from proceeding",
        svg_title="Chapter 7 lab flow: a postmortem-completeness audit and a change-approval gate, each validated against a compliant and a violating record",
        svg_desc="INC-1001 (SEV1, with a linked postmortem) and INC-1002 (SEV3, postmortem not required) both "
                  "pass the coverage audit with 0 issues. CHG-2001 (2 of 2 approvals) passes the change gate; "
                  "CHG-2002 (1 of 2 approvals) is BLOCKED with a nonzero exit. As a negative test, INC-1001's "
                  "postmortem file is moved aside to simulate a SEV1 incident closed without one; re-running the "
                  "audit now reports 'MISSING POSTMORTEM: INC-1001 (SEV1)' and exits non-zero, demonstrating the "
                  "gate would fail a CI check rather than silently allowing the incident to close unreviewed. "
                  "Restoring the file returns the audit to passing.")
    c.node_box(60, 140, 240, 110, "alt", [
        Line("INC-1001 (SEV1)", 12.5, 700, "#111827"),
        Line("postmortem linked", 10.5, 400, "#374151"),
        Line("audit: 0 issues", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("CHG-2001", 12.5, 700, "#111827"),
        Line("2/2 approvals", 10.5, 400, "#374151"),
        Line("gate: approved, proceeding", 10.5, 700, "#14532d"),
    ])
    c.node_box(700, 140, 220, 110, "warn", [
        Line("CHG-2002", 12.5, 700, "#111827"),
        Line("1/2 approvals", 10.5, 700, "#7f1d1d"),
        Line("gate: BLOCKED, exit ≠ 0", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(60, 330, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("INC-1001's postmortem file moved aside, audit re-run", 11, 400, "#7f1d1d"),
        Line("\"MISSING POSTMORTEM: INC-1001 (SEV1)\", exit non-zero — CI would fail the build on this condition", 11, 400, "#7f1d1d"),
        Line("restoring the file returns the audit to passing", 11, 400, "#14532d"),
    ])
    c.legend(60, 500, [("alt", "Compliant record"), ("warn", "Blocked / caught by audit")])
    c.save(f"{OUT}/chapter-07-postmortem-change-gate-flow.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: Finding a Real Saturation Point, Then Missing It With a Shallow Test",
        subtitle="Latency stays flat through concurrency 8, then jumps sharply — a shallow traffic model never reaches that inflection at all",
        svg_title="Chapter 8 lab flow: a load test that locates a service's real saturation point, contrasted with a shallow test that misses it entirely",
        svg_desc="A sample service bounded to 8 concurrent workers is load-tested at increasing concurrency (2, "
                  "4, 8, 12, 16, 24). Average latency stays near 50-70ms through concurrency 8, then jumps sharply "
                  "to roughly 150-300ms at concurrency 12 and beyond — a clear non-linear inflection identifying "
                  "the real saturation point between 8 and 12. As a negative test, a shallow traffic model using "
                  "only concurrency 1, 2, and 3 is run instead; latency stays flat at 50-70ms across all three "
                  "levels with no degradation, never approaching the worker pool limit — producing a false-"
                  "confidence 'handles load fine' conclusion, the exact traffic-model risk this chapter's "
                  "Validation section describes.")
    c.node_box(60, 140, 400, 130, "mgmt", [
        Line("Real load test: concurrency 2→24", 12.5, 700, "#111827"),
        Line("flat ~50-70ms through concurrency 8", 10.5, 400, "#374151"),
        Line("sharp jump to ~150-300ms at 12+", 10.5, 700, "#1d4ed8"),
        Line("saturation point located: 8-12", 10.5, 700, "#14532d"),
    ])
    c.node_box(540, 140, 380, 130, "warn", [
        Line("Negative Test: shallow model", 12.5, 700, "#111827"),
        Line("concurrency 1, 2, 3 only", 10.5, 400, "#7f1d1d"),
        Line("flat ~50-70ms across all levels", 10.5, 700, "#7f1d1d"),
        Line("saturation point NEVER reached", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(60, 320, 860, 100, "warn", [
        Line("the shallow test produces a false-confidence \"the service handles load fine\" conclusion, because its", 11.5, 400, "#7f1d1d"),
        Line("traffic model never exercises concurrency anywhere near the real worker-pool boundary at 8.", 11.5, 400, "#7f1d1d"),
    ])
    c.legend(60, 460, [("mgmt", "Traffic model that finds the boundary"), ("warn", "Traffic model that misses it")])
    c.save(f"{OUT}/chapter-08-load-test-saturation-point-flow.svg")


def ch09():
    c = Canvas(960, 640,
        title="Chapter 9 Hands-On Lab: A Rate-Limited Auto-Remediation Loop That Escalates Instead of Looping Forever",
        subtitle="Restarts are capped at 3 per 10-second window under sustained fault injection; the remainder escalate to on-call",
        svg_title="Chapter 9 lab flow: a rate-limited closed-loop remediation script tested against sustained fault injection, plus an MTTA/MTTR trend",
        svg_desc="inject_fault.py marks a simulated pod unhealthy every 0.2 seconds for about 24 seconds (roughly "
                  "120 fault events) while auto_remediate.py restarts it, but only up to 3 restarts per rolling "
                  "10-second window. audit.jsonl contains both restart and escalate entries. As a negative test, "
                  "counting actual restart entries against the fault-injection rate confirms restart_count is well "
                  "under 120 (bounded to roughly 6-9, matching the two-to-three 10-second windows the run spans), "
                  "with escalate_count accounting for the remainder — confirming the guardrail genuinely bounds "
                  "the action count rather than merely logging a warning while still restarting every cycle. "
                  "Separately, a monthly MTTA/MTTR trend computed from sample incident data shows MTTR rising from "
                  "roughly 34 minutes in May to roughly 87 minutes in July.")
    c.node_box(60, 140, 260, 110, "warn", [
        Line("inject_fault.py", 12.5, 700, "#111827"),
        Line("marks pod unhealthy every 0.2s", 10.5, 400, "#374151"),
        Line("~120 fault events over ~24s", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 260, 110, "mgmt", [
        Line("auto_remediate.py", 12.5, 700, "#111827"),
        Line("rate limit: 3 restarts / 10s window", 10.5, 700, "#1d4ed8"),
        Line("beyond limit → escalate to on-call", 10.5, 400, "#374151"),
    ])
    c.connector(320, 195, 380, 195, "warn")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("audit.jsonl", 12.5, 700, "#111827"),
        Line("restarts: ~6-9 (bounded)", 10.5, 700, "#14532d"),
        Line("escalations: remainder", 10.5, 700, "#14532d"),
    ])
    c.connector(640, 195, 700, 195, "alt")
    c.node_box(60, 320, 860, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("restart_count counted directly against ~120 fault events → well under 120, not close to it", 11, 400, "#7f1d1d"),
        Line("confirms the rate limiter genuinely bounds actions under sustained pressure, not just warns while acting", 11, 400, "#7f1d1d"),
    ])
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("Separately: MTTA/MTTR trend from sample incidents shows MTTR rising ~34min (May) → ~87min (July),", 11.5, 400, "#374151"),
        Line("an upward trend that would warrant the operational-analytics investigation this chapter describes.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("warn", "Sustained fault pressure"), ("mgmt", "Rate-limited response"), ("alt", "Bounded, audited outcome")])
    c.save(f"{OUT}/chapter-09-rate-limited-remediation-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
