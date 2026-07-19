import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-12-resilience-lifecycle-management"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Hands-On Lab: SPOF Detection Distinguishes Chokepoints From Shared Dependencies",
        subtitle="web-frontend and api-service are topological SPOFs; auth-service is a shared-dependency risk the algorithm correctly does not flag",
        svg_title="Chapter 1 lab flow: a dependency graph's single-point-of-failure detection, contrasted with a severed-path negative test",
        svg_desc="find_spof.py analyzes a graph (ingress to web-frontend to api-service, which fans out to "
                  "auth-service and database, with web-frontend also calling auth-service directly) and reports "
                  "['web-frontend', 'api-service'] as SPOFs, since both sit on the only path from ingress to the "
                  "critical services. auth-service is correctly NOT reported, even though both upstream services "
                  "call it — it is a leaf with no outgoing path back toward the critical services, a "
                  "shared-dependency risk rather than a topological chokepoint. As a negative test, removing the "
                  "web-frontend-to-api-service edge leaves api-service with no inbound edge at all; every "
                  "remaining node is then trivially reported as a 'SPOF', correctly signaling that the redesign "
                  "severed the only route in — a worse problem than any single SPOF.")
    c.node_box(60, 140, 180, 90, "mgmt", [
        Line("ingress", 13, 700, "#111827"),
    ])
    c.node_box(300, 140, 200, 90, "warn", [
        Line("web-frontend", 13, 700, "#111827"),
        Line("SPOF #1", 11, 700, "#7f1d1d"),
    ])
    c.node_box(540, 140, 200, 90, "warn", [
        Line("api-service", 13, 700, "#111827"),
        Line("SPOF #2", 11, 700, "#7f1d1d"),
    ])
    c.node_box(780, 60, 160, 80, "alt", [
        Line("auth-service", 12, 700, "#111827"),
        Line("shared dep, not a SPOF", 10, 400, "#374151"),
    ])
    c.node_box(780, 220, 160, 80, "mgmt", [
        Line("database", 12.5, 700, "#111827"),
    ])
    c.connector(240, 185, 300, 185, "mgmt")
    c.connector(500, 185, 540, 185, "mgmt")
    c.connector(700, 165, 780, 110, "alt", label="calls")
    c.connector(400, 175, 780, 100, "alt", label="calls")
    c.connector(700, 205, 780, 250, "mgmt")
    c.node_box(60, 340, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("web-frontend → api-service edge removed (redesign: front end talks only to auth)", 11, 400, "#7f1d1d"),
        Line("api-service now has NO inbound edge at all — every remaining node trivially becomes a \"SPOF\"", 11, 400, "#7f1d1d"),
        Line("the real finding: the redesign severed the only route to api-service, worse than any single SPOF", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Path to critical services"), ("warn", "Topological SPOF"), ("alt", "Shared dependency (not a SPOF)")])
    c.save(f"{OUT}/chapter-01-spof-dependency-graph-flow.svg")


def ch02():
    c = Canvas(960, 560,
        title="Chapter 2 Hands-On Lab: A Data-Derived MTD That Disagrees With the Owner-Stated Figure",
        subtitle="The impact-escalation curve crosses threshold at 24 hours; the questionnaire's own answer says 48 — evidence wins",
        svg_title="Chapter 2 lab flow: deriving a maximum tolerable downtime from a BIA impact-escalation curve, checked against a flat-impact negative test",
        svg_desc="derive_mtd.py walks the impact_by_checkpoint data from a sample BIA and finds the operational "
                  "impact category first crosses the severity threshold at the 24-hour checkpoint, producing a "
                  "derived MTD of 24 hours — deliberately in conflict with the questionnaire's owner-stated 48 "
                  "hours. The evidence-based, data-derived figure should generally take precedence, with the "
                  "disagreement escalated to the process owner for reconciliation. As a negative test, every "
                  "checkpoint's impact scores are set identical (no escalation over time); the script still "
                  "returns a 1-hour-checkpoint-based MTD, but this flat-impact scenario should itself be flagged "
                  "as suspect during BIA quality review, per the checkpoint-monotonicity guidance.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("bia-customer-refunds.yaml", 12.5, 700, "#111827"),
        Line("impact_by_checkpoint: 1h/4h/24h/72h", 10.5, 400, "#374151"),
        Line("owner-stated MTD: 48h", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("derive_mtd.py", 12.5, 700, "#111827"),
        Line("operational impact crosses", 10.5, 400, "#374151"),
        Line("threshold at 24h checkpoint", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "neutral", [
        Line("RESOLUTION.md", 12.5, 700, "#111827"),
        Line("evidence-based 24h figure", 10.5, 400, "#374151"),
        Line("used, escalated to owner", 10.5, 400, "#374151"),
    ])
    c.connector(640, 200, 700, 200, "alt")
    c.node_box(60, 320, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("every checkpoint's impact score set identical (no escalation over time)", 11, 400, "#7f1d1d"),
        Line("script still returns a 1-hour-checkpoint MTD — but a flat-impact curve is itself a BIA quality defect", 11, 400, "#7f1d1d"),
        Line("that should be flagged during review per checkpoint-monotonicity guidance, not accepted at face value", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 460, [("mgmt", "Questionnaire input"), ("alt", "Evidence-derived MTD")])
    c.save(f"{OUT}/chapter-02-bia-mtd-derivation-flow.svg")


def ch03():
    c = Canvas(960, 600,
        title="Chapter 3 Hands-On Lab: Circuit Breaker Fail-Fast and RTO-Enforced Failover Verification",
        subtitle="After 3 failures the breaker fails fast instead of retrying; a zero-second RTO budget correctly fails the check",
        svg_title="Chapter 3 lab flow: a circuit breaker transitioning to open after repeated failures, and a failover-verification script enforcing an RTO budget",
        svg_desc="breaker_demo.py wraps a deliberately failing dependency in a circuit breaker (fail_max=3). The "
                  "first three calls fail with RuntimeError as the breaker's state progresses toward open; from "
                  "the fourth call onward, calls are rejected immediately with CircuitBreakerError rather than "
                  "waiting for the dependency to fail again — fail-fast behavior. Separately, verify-failover.sh "
                  "run against a load-balancer stub with a 60-second RTO budget reports PASS once the target is no "
                  "longer InService. As a negative test, rerunning with an artificially tight 0-second RTO budget "
                  "reports FAIL, proving the RTO-enforcement branch is reachable and correctly triggers, not just "
                  "the success path.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Calls 1-3", 12.5, 700, "#111827"),
        Line("dependency fails (RuntimeError)", 10.5, 400, "#374151"),
        Line("breaker state → open", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Calls 4-6", 12.5, 700, "#111827"),
        Line("rejected immediately", 10.5, 700, "#14532d"),
        Line("CircuitBreakerError (fail-fast)", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "alt", [
        Line("verify-failover.sh 60s", 12, 700, "#111827"),
        Line("target no longer InService", 10.5, 400, "#374151"),
        Line("PASS", 10.5, 700, "#14532d"),
    ])
    c.node_box(60, 330, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("verify-failover.sh re-run with RTO budget = 0 seconds", 11, 400, "#7f1d1d"),
        Line("script reports FAIL — proving the RTO-enforcement branch is reachable and actually triggers,", 11, 400, "#7f1d1d"),
        Line("not merely present alongside a success path that always passes", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Failures accumulating"), ("alt", "Fail-fast / passing checks")])
    c.save(f"{OUT}/chapter-03-circuit-breaker-failover-flow.svg")


def ch04():
    c = Canvas(960, 560,
        title="Chapter 4 Hands-On Lab: A Backup Verification Step That Actually Catches Corruption",
        subtitle="A truncated archive fails tar's integrity check immediately, exactly the failure mode verification exists to catch before a real restore",
        svg_title="Chapter 4 lab flow: a self-verifying backup and restore workflow tested against a deliberately truncated archive",
        svg_desc="run-backup.sh archives 20 sample records and reports 'PASS: backup created and verified', "
                  "producing a .tar.gz and a .sha256 manifest. restore-verify.sh restores from that archive and "
                  "reports 'PASS: restore produced 20 files', matching the source exactly (diff -r confirms). As a "
                  "negative test, the latest archive is truncated by 200 bytes to break its compressed stream "
                  "(appending bytes is insufficient, since readers stop cleanly at the valid stream's end); "
                  "tar -tzf against the truncated archive fails with a message such as 'truncated gzip input' "
                  "rather than silently appearing to succeed, confirming the specific failure mode the "
                  "verification step exists to catch before a real restore is ever attempted against it.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("run-backup.sh", 12.5, 700, "#111827"),
        Line("20 records → .tar.gz + .sha256", 10.5, 400, "#374151"),
        Line("PASS: created and verified", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("restore-verify.sh", 12.5, 700, "#111827"),
        Line("restore/: 20 files", 10.5, 400, "#374151"),
        Line("diff -r source restore: match", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("archive truncated by 200 bytes", 10.5, 700, "#7f1d1d"),
        Line("tar -tzf: truncated gzip input", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("corruption is caught by the integrity check before a real restore is ever attempted against the archive —", 11.5, 400, "#374151"),
        Line("the exact failure mode this verification step exists to catch, not merely a check for its own sake.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Verified backup"), ("alt", "Verified restore"), ("warn", "Detected corruption")])
    c.save(f"{OUT}/chapter-04-backup-restore-verification-flow.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: A Chaos Experiment Whose Rollback Must Be Structurally Guaranteed",
        subtitle="finally guarantees rollback even on early abort; removing that guarantee leaves the fault permanently active",
        svg_title="Chapter 5 lab flow: a hypothesis-driven fault-injection experiment aborting on steady-state violation, contrasted with an unprotected rollback",
        svg_desc="experiment.py injects a simulated dependency failure; the steady-state checkout success metric "
                  "drops below the 95.0 threshold at approximately the 3-4 second mark, triggering an ABORT — and "
                  "because rollback_fn() is wrapped in a finally block, it executes even though the experiment "
                  "exited early, confirmed by degraded=False afterward. As a negative test, rollback_fn() is "
                  "deliberately moved outside the try/finally to run only after normal loop completion; rerunning "
                  "the identical scenario produces the same ABORT at the same elapsed time, but state['degraded'] "
                  "now remains True after the script exits, because the early return on the abort path no longer "
                  "passes through any rollback call — the exact unprotected-rollback failure mode this chapter "
                  "warns against.")
    c.node_box(60, 140, 260, 130, "mgmt", [
        Line("experiment.py (finally-guarded)", 12, 700, "#111827"),
        Line("fault injected → metric drops", 10.5, 400, "#374151"),
        Line("ABORT at ~3-4s", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(400, 140, 260, 130, "alt", [
        Line("finally: rollback_fn()", 12.5, 700, "#111827"),
        Line("executes on EVERY exit path", 10.5, 400, "#374151"),
        Line("degraded=False (cleared)", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 205, 400, 205, "mgmt")
    c.node_box(700, 140, 220, 130, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("rollback moved outside finally", 10.5, 700, "#7f1d1d"),
        Line("same ABORT fires, but", 10.5, 400, "#7f1d1d"),
        Line("degraded=True remains after exit", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(660, 205, 700, 205, "warn")
    c.node_box(60, 350, 860, 100, "warn", [
        Line("the early-return abort path no longer passes through any rollback call once finally is removed —", 11.5, 400, "#7f1d1d"),
        Line("rollback must be structurally guaranteed to run on every exit path, not merely present in the normal-completion path.", 11.5, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Injected fault + abort"), ("alt", "Guaranteed rollback"), ("warn", "Unprotected rollback (bug)")])
    c.save(f"{OUT}/chapter-05-chaos-experiment-rollback-flow.svg")


def ch06():
    c = Canvas(960, 620,
        title="Chapter 6 Hands-On Lab: A Quorum-Preserving Rolling Patch and a Deliberately Broken Quorum Guard",
        subtitle="Five nodes patch one at a time with quorum intact throughout; hardcoding MIN_QUORUM=1 lets the script proceed when it should not",
        svg_title="Chapter 6 lab flow: a rolling patch that drains, patches, and rejoins nodes one at a time while preserving cluster quorum",
        svg_desc="patch-cluster-rolling.sh patches all five simulated cluster nodes one at a time (drain, patch, "
                  "rejoin), reporting 'All nodes patched with quorum preserved throughout' and returning "
                  "active-nodes.txt to 5. Separately, compliance.py flags web-frontend-03 as critical-patch "
                  "overdue against a 48-hour SLA. As a negative test, the script's MIN_QUORUM calculation is "
                  "hardcoded to 1 (well below true majority) and the rolling patch re-run; the script now proceeds "
                  "even when it should not, demonstrating that a quorum guard with an incorrect threshold provides "
                  "false confidence rather than real protection — the formula itself must be verified, not merely "
                  "present.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("5-node cluster", 12.5, 700, "#111827"),
        Line("drain → patch → rejoin, x5", 10.5, 400, "#374151"),
        Line("quorum check before each drain", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Correct MIN_QUORUM", 12.5, 700, "#111827"),
        Line("All nodes patched,", 10.5, 700, "#14532d"),
        Line("quorum preserved throughout", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("MIN_QUORUM hardcoded to 1", 10.5, 700, "#7f1d1d"),
        Line("proceeds even when it", 10.5, 700, "#7f1d1d"),
        Line("should not — false confidence", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("separately, compliance.py flags web-frontend-03 as critical-patch overdue against a 48-hour SLA —", 11.5, 400, "#374151"),
        Line("the quorum guard and the SLA scan are independent checks that must each be verified correct on their own terms.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Rolling patch cycle"), ("alt", "Verified quorum guard"), ("warn", "Broken quorum guard")])
    c.save(f"{OUT}/chapter-06-quorum-rolling-patch-flow.svg")


def ch07():
    c = Canvas(960, 580,
        title="Chapter 7 Hands-On Lab: Urgency-Adjusted Debt Scoring Elevates an Approaching EOL Over Raw Impact",
        subtitle="A moderate-effort item with an EOL under 180 days outranks a more architecturally severe item with no deadline",
        svg_title="Chapter 7 lab flow: a technical-debt register scored by urgency-adjusted impact, re-tested after scoping down effort and after an EOL lapses",
        svg_desc="score_debt_item ranks legacy-billing-service-eol (EOL under 180 days, moderate 8-week effort) "
                  "first, ahead of the architecturally more severe but non-urgent monolith-order-processing entry "
                  "— urgency-adjusted prioritization rather than raw impact alone. Reducing "
                  "monolith-order-processing's effort estimate to 2 weeks (a smaller, well-scoped first "
                  "increment) raises its score substantially, illustrating the strangler-fig principle. As a "
                  "negative test, setting legacy-billing-service-eol's EOL date into the past increases its score "
                  "further still, correctly modeling that a system already past its EOL carries materially higher "
                  "unmanaged risk than one still inside its remediation window.")
    c.node_box(60, 140, 260, 120, "warn", [
        Line("legacy-billing-service-eol", 12.5, 700, "#111827"),
        Line("EOL < 180 days, 8wk effort", 10.5, 400, "#374151"),
        Line("ranks #1 (urgency-adjusted)", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(400, 140, 260, 120, "mgmt", [
        Line("monolith-order-processing", 12.5, 700, "#111827"),
        Line("higher raw impact, no deadline", 10.5, 400, "#374151"),
        Line("ranks lower until re-scoped", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "alt", [
        Line("Effort → 2 weeks", 12.5, 700, "#111827"),
        Line("score rises substantially", 10.5, 700, "#14532d"),
        Line("(strangler-fig increment)", 10.5, 400, "#374151"),
    ])
    c.connector(660, 200, 700, 200, "alt")
    c.node_box(60, 320, 860, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("legacy-billing-service-eol's eol_date set into the past → score increases further (urgency maxes out)", 11, 400, "#7f1d1d"),
        Line("correctly models that a system already past EOL carries higher unmanaged risk than one still in-window", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 460, [("warn", "Deadline-driven urgency"), ("mgmt", "High raw impact, no deadline"), ("alt", "Re-scoped increment")])
    c.save(f"{OUT}/chapter-07-tech-debt-scoring-flow.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: A Right-Sizing Scan That Must Not Mistake Redundancy for Waste",
        subtitle="Two idle production instances are flagged; tagged HA/DR standby capacity is correctly excluded — until the tag is removed",
        svg_title="Chapter 8 lab topology: a fleet right-sizing scan excluding tagged HA/DR standby capacity from its recommendations, tested against an untagged standby",
        svg_desc="calculate_pue reports 1.45 for Q1 versus 1.62 for Q3 against identical IT load, illustrating a "
                  "seasonal cooling-load increase a single-period snapshot would miss. find_rightsizing_candidates "
                  "scans a six-instance fleet and flags exactly web-02 and batch-01 as candidates, correctly "
                  "excluding db-standby-01 and dr-replica-01 (low utilization is deliberate redundancy headroom, "
                  "not waste) and web-03 (fewer than 14 days observed). As a negative test, removing the role "
                  "field from db-standby-01 (simulating an untagged standby) causes it to incorrectly appear as a "
                  "right-sizing candidate — automation that cannot distinguish deliberate redundancy from waste "
                  "will recommend reducing HA capacity when the underlying data isn't properly tagged. Restoring "
                  "the tag returns the candidate list to its expected state.")
    c.node_box(60, 140, 240, 110, "warn", [
        Line("web-02, batch-01", 12.5, 700, "#111827"),
        Line("production, low CPU, ≥14 days", 10.5, 400, "#374151"),
        Line("flagged: downsize/consolidate", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("db-standby-01, dr-replica-01", 12, 700, "#111827"),
        Line("role: ha-standby / dr-standby", 10.5, 700, "#14532d"),
        Line("correctly excluded (redundancy)", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 140, 220, 110, "mgmt", [
        Line("web-03", 12.5, 700, "#111827"),
        Line("only 5 days observed", 10.5, 400, "#374151"),
        Line("excluded (insufficient data)", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 330, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("role field removed from db-standby-01 (simulating an untagged standby instance)", 11, 400, "#7f1d1d"),
        Line("db-standby-01 now incorrectly appears as a right-sizing candidate", 11, 400, "#7f1d1d"),
        Line("automation cannot distinguish deliberate redundancy from waste without correct tagging — restoring", 11, 400, "#7f1d1d"),
        Line("the role field returns the candidate list to its expected, correct state", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("warn", "Right-sizing candidate"), ("alt", "Excluded redundancy"), ("mgmt", "Excluded, insufficient data")])
    c.save(f"{OUT}/chapter-08-pue-rightsizing-scan-topology.svg")


def ch09():
    c = Canvas(960, 620,
        title="Chapter 9 Hands-On Lab: A Dependency-Gated Decommission Check That Blocks an Active Dependent",
        subtitle="auth-service-v1 stays BLOCKED while its batch-job dependent is active, and READY the moment that dependent retires",
        svg_title="Chapter 9 lab flow: a decommission-readiness gate blocking a system with an active dependent, contrasted with an ungated naive decommission",
        svg_desc="decommission_check.py evaluates a dependency graph where legacy-batch-job still actively calls "
                  "auth-service-v1, while unrelated production traffic uses auth-service-v2. The gate reports "
                  "auth-service-v1 as BLOCKED (still depended on by legacy-batch-job) and legacy-batch-job itself "
                  "as READY (nothing calls it). Retiring legacy-batch-job's status and re-running flips "
                  "auth-service-v1 to READY, demonstrating the gate re-evaluates once the blocking dependent is "
                  "itself retired. As a negative test, a naive one-line script that 'decommissions' "
                  "auth-service-v1 unconditionally, with no dependency check, proceeds with no warning against the "
                  "exact same active-dependent input the gated script correctly blocked — the concrete mechanism "
                  "that prevents a premature-decommissioning outage.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("legacy-batch-job", 12.5, 700, "#111827"),
        Line("status: active → retired", 10.5, 400, "#374151"),
        Line("READY (nothing depends on it)", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 140, 260, 110, "warn", [
        Line("auth-service-v1", 12.5, 700, "#111827"),
        Line("BLOCKED while batch-job active", 10.5, 700, "#7f1d1d"),
        Line("→ READY once batch-job retires", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt", label="active dependent")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("naive 1-line \"decommission\"", 10.5, 700, "#7f1d1d"),
        Line("no check → proceeds, no warning", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 100, "warn", [
        Line("the ungated script decommissions auth-service-v1 unconditionally against the SAME input the gated", 11.5, 400, "#7f1d1d"),
        Line("script correctly BLOCKED — the gate is a required control, not an optional nicety, against premature-decommissioning outages.", 11.5, 400, "#7f1d1d"),
    ])
    c.legend(60, 470, [("mgmt", "Safe to retire"), ("warn", "Gated / blocked path")])
    c.save(f"{OUT}/chapter-09-decommission-dependency-gate-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
