import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-99-reference-library"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Hands-On Lab: A Read-Only Command's Typo Becomes a Documented \"Common Failure\" Note",
        subtitle="A versioned command card is built from real observed output, and one Tier 1 change passes through all four safe-administration gates before it runs",
        svg_title="Chapter 1 lab flow: a command quick-reference card populated with real Tier 0 output and a Tier 1 change gated through authorization, backup, dry run, and rollback, tested against a mistyped read-only flag",
        svg_desc="command-card.md is populated with real output captured from Tier 0, read-only commands run "
                  "against a lab system, so each row is backed by observed evidence rather than assumed syntax. "
                  "One Tier 1, state-changing command is gated by writing the authorization line, taking a "
                  "backup, running a dry run, and recording the rollback command, all before it executes; "
                  "running it and immediately re-validating with the matching Tier 0 command confirms only the "
                  "intended change occurred. As a negative test, a read-only command is deliberately run with a "
                  "mistyped flag, and the resulting error text is captured and added to the card as a documented "
                  "\"common failure\" note, improving its diagnostic value for future readers.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Tier 0 rows: real output captured", 12.5, 700, "#111827"),
        Line("Tier 1 change: 4 safe-admin gates", 10.5, 400, "#374151"),
        Line("(authorize, backup, dry run, rollback)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Tier 1 executed", 12.5, 700, "#111827"),
        Line("Tier 0 validation re-run", 10.5, 400, "#374151"),
        Line("→ only intended change confirmed", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("mistyped flag on a", 10.5, 700, "#7f1d1d"),
        Line("read-only command", 10.5, 700, "#7f1d1d"),
        Line("→ error text documented", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the completed card is committed to version control with a message describing the platforms covered,", 11.5, 400, "#374151"),
        Line("giving the reference card version history so it cannot drift silently.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Evidence-backed card build"), ("alt", "Gated state change"), ("warn", "Documented failure mode")])
    c.save(f"{OUT}/chapter-01-command-card-safe-admin-gates-flow.svg")


def ch02():
    c = Canvas(960, 600,
        title="Chapter 2 Hands-On Lab: A Closed Port and a Firewalled Port Look Different on the Wire, Not the Same",
        subtitle="A port reference card is validated by a live handshake capture, and the negative test distinguishes a reset from a silent timeout",
        svg_title="Chapter 2 lab flow: a service-to-port reference card validated by a live TCP handshake capture and a cross-host reachability test, tested against a connection to an unopened port",
        svg_desc="A port-reference-card.md table is populated with real services from the lab environment, each "
                  "row extended with its observed bound address from a listening-state check. A reachability "
                  "test from a second host confirms which services are actually reachable across the network, "
                  "and capturing one TCP service's handshake shows SYN, SYN-ACK, ACK in order, confirming the "
                  "flow matches the row recorded for it. As a negative test, a connection is attempted to a port "
                  "that was never opened, and the observable result, a TCP RST, an ICMP unreachable, or silent "
                  "timeout, is recorded, documenting the practical difference between a closed port and a "
                  "firewalled port that this reference card exists to capture.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("port-reference-card.md", 12.5, 700, "#111827"),
        Line("+ Bound Address column", 10.5, 400, "#374151"),
        Line("(listening-state check)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("tcpdump capture", 12.5, 700, "#111827"),
        Line("SYN, SYN-ACK, ACK", 10.5, 700, "#14532d"),
        Line("confirms the flow statement", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("connect to unopened port", 10.5, 700, "#7f1d1d"),
        Line("→ RST, ICMP unreachable,", 10.5, 700, "#7f1d1d"),
        Line("or silent timeout", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("which of the three outcomes actually occurs is itself the recurring troubleshooting distinction —", 11.5, 400, "#374151"),
        Line("closed and firewalled ports are observably different, not interchangeable failure modes.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Card + bound-address evidence"), ("alt", "Captured handshake"), ("warn", "Observed closed/firewalled distinction")])
    c.save(f"{OUT}/chapter-02-port-reference-handshake-flow.svg")


def ch03():
    c = Canvas(960, 600,
        title="Chapter 3 Hands-On Lab: A Documentation-Range Address Correctly Refuses to Resolve",
        subtitle="Manual subnet math is checked against a tool, DNS and time are validated against real infrastructure, and a reserved address is confirmed non-routable",
        svg_title="Chapter 3 lab flow: addressing, DNS, time, and identity values validated against real lab infrastructure, tested against a reverse DNS lookup of a documentation-only address",
        svg_desc="A lab CIDR block's network address, broadcast address, usable host range, and wildcard mask "
                  "are calculated by hand and then verified against a calculation tool, with any discrepancy "
                  "identified and corrected. DNS queries against both the internal resolver and the "
                  "authoritative server return consistent records for three real hostnames, and a time-sync "
                  "check records the lab host's current stratum and offset. Four identity formats, DN, UPN, "
                  "SPN, and ARN, are constructed from real or clearly marked placeholder values. As a negative "
                  "test, a reverse DNS lookup is attempted against 192.0.2.1, an address from the documentation "
                  "range reserved specifically for use in examples; the query fails or returns no authoritative "
                  "answer, confirming the range is genuinely non-routable rather than merely documented as such.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Manual subnet math", 12.5, 700, "#111827"),
        Line("verified against ipcalc", 10.5, 400, "#374151"),
        Line("DNS + chronyc offset checked", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Identity formats assembled", 12.5, 700, "#111827"),
        Line("DN, UPN, SPN, ARN", 10.5, 700, "#14532d"),
        Line("from real environment values", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("dig -x 192.0.2.1", 10.5, 700, "#7f1d1d"),
        Line("(documentation range)", 10.5, 700, "#7f1d1d"),
        Line("→ no authoritative answer", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("all four systems — addressing, naming, time, and identity — are assembled into one reference file,", 11.5, 400, "#374151"),
        Line("each backed by a real query result rather than a value copied from the chapter's table alone.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Verified addressing + time"), ("alt", "Identity format examples"), ("warn", "Confirmed reserved range")])
    c.save(f"{OUT}/chapter-03-addressing-identity-verification-flow.svg")


def ch04():
    c = Canvas(960, 620,
        title="Chapter 4 Hands-On Lab: Drift Introduced on Purpose Is Detected, Not Assumed Absent",
        subtitle="A template renders to a baseline that matches the running system exactly, until a deliberate undocumented change proves the drift check actually works",
        svg_title="Chapter 4 lab flow: a parameterized template rendered into an approved baseline and applied through a documented change record, tested against a manually introduced configuration drift",
        svg_desc="A configuration template with placeholder variables renders into a fully resolved "
                  "baseline-v1.conf, and a complete change record documents the backup step and rollback command "
                  "before anything is applied. A dry run's output is attached showing only the intended "
                  "difference, and applying the change followed by re-capturing the running configuration shows "
                  "no unexpected difference from the declared baseline. As a negative test, one small, "
                  "undocumented change is introduced directly on the lab system outside the change-record "
                  "process; re-running the platform's drift detection method correctly detects and reports it. "
                  "The drift is then reconciled, either by updating the baseline with a new documented change or "
                  "by reverting the system, with the chosen path and its reasoning recorded.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Template → baseline-v1.conf", 12.5, 700, "#111827"),
        Line("change record: backup + rollback", 10.5, 400, "#374151"),
        Line("dry run: only intended diff", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Applied + re-captured", 12.5, 700, "#111827"),
        Line("matches declared baseline", 10.5, 700, "#14532d"),
        Line("exactly, no unexpected diff", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("undocumented change", 10.5, 700, "#7f1d1d"),
        Line("introduced manually", 10.5, 700, "#7f1d1d"),
        Line("→ drift detected + reconciled", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 110, "neutral", [
        Line("reconciliation takes one of two documented paths: update the baseline with a new change record if the", 11.5, 400, "#374151"),
        Line("drift was an intentional, undocumented change worth keeping, or revert the system to match the existing", 11.5, 400, "#374151"),
        Line("baseline if it was not — either way, the system and its declared baseline agree again.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 480, [("mgmt", "Template + change record"), ("alt", "Baseline-matching apply"), ("warn", "Detected + reconciled drift")])
    c.save(f"{OUT}/chapter-04-template-baseline-drift-flow.svg")


def ch05():
    c = Canvas(960, 600,
        title="Chapter 5 Hands-On Lab: Every Disposition Traces to Linked Evidence, Never to Memory",
        subtitle="Four falsifiable checklist items are validated with captured artifacts, and one deliberate Fail proves the checklist has a real failure path",
        svg_title="Chapter 5 lab flow: an acceptance checklist populated with falsifiable items and evidence-backed dispositions, tested against one item deliberately recorded as Fail",
        svg_desc="A reusable acceptance-checklist-template.md is copied to a change-specific file and populated "
                  "with four checklist items, each with a specific, falsifiable expected result rather than a "
                  "vague one. Executing each check and capturing evidence, command output, a screenshot, a test "
                  "report, or a log excerpt, produces four timestamped artifacts, each linked from its row; a "
                  "disposition of Pass, Fail, or Waived is then assigned to each item strictly from that linked "
                  "evidence. As a negative test, one item is deliberately recorded as Fail, using a real observed "
                  "failure or a condition known not yet to be met, and the resulting action, rollback, follow-up "
                  "change, or escalation, is documented, proving the checklist has a real, working Fail path and "
                  "not only a happy path.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("4 falsifiable checklist items", 12.5, 700, "#111827"),
        Line("evidence captured per item", 10.5, 400, "#374151"),
        Line("(output, screenshot, log, report)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Dispositions assigned", 12.5, 700, "#111827"),
        Line("Pass/Fail/Waived, each", 10.5, 700, "#14532d"),
        Line("traceable to linked evidence", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("one item deliberately Fail", 10.5, 700, "#7f1d1d"),
        Line("→ documented rollback/", 10.5, 700, "#7f1d1d"),
        Line("follow-up/escalation action", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("an overall disposition and accepting reviewer are recorded at the bottom, and the completed checklist", 11.5, 400, "#374151"),
        Line("plus its evidence directory are committed together as one versioned acceptance record.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Falsifiable checklist + evidence"), ("alt", "Evidence-traceable disposition"), ("warn", "Documented Fail path")])
    c.save(f"{OUT}/chapter-05-acceptance-checklist-evidence-flow.svg")


def ch06():
    c = Canvas(960, 620,
        title="Chapter 6 Hands-On Lab: The Same Decision Tree Reaches the Same Diagnosis Twice, Not by Coincidence",
        subtitle="A single induced failure is diagnosed node by node from a documented baseline, then reproduced to confirm the tree is repeatable",
        svg_title="Chapter 6 lab flow: a single simulated failure diagnosed through a decision tree to a specific conclusion and resolved back to baseline, tested by reproducing the identical failure a second time",
        svg_desc="A lab service's working baseline and response time are documented before exactly one failure "
                  "condition is induced without pre-announcing which one. Working through the appropriate "
                  "decision tree node by node, recording each check and its result, ends at a specific, correct "
                  "diagnosis; the incident is then classified by severity and escalation trigger using the "
                  "chapter's matrix, and a timestamped incident timeline is produced from detection through "
                  "resolution. Resolving the failure and re-running the original detection check confirms the "
                  "service matches its original baseline, not merely that it appears to work. As a negative "
                  "test, the identical failure condition is reintroduced, and the same decision tree is walked "
                  "again; it reaches the same diagnosis a second time, confirming the tree is repeatable rather "
                  "than a one-time coincidence.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Baseline documented", 12.5, 700, "#111827"),
        Line("one failure condition induced", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "alt", [
        Line("Decision tree walked", 12.5, 700, "#111827"),
        Line("node by node →", 10.5, 700, "#14532d"),
        Line("specific correct diagnosis", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Resolved + re-checked", 12.5, 700, "#111827"),
        Line("matches original baseline", 10.5, 700, "#14532d"),
    ])
    c.connector(600, 185, 700, 185, "alt")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("same failure reintroduced", 10.5, 700, "#7f1d1d"),
        Line("→ same diagnosis reached again", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("severity and escalation trigger are classified from the matrix's criteria, not intuition, and the", 11.5, 400, "#374151"),
        Line("resulting timeline links evidence at every stage from detection through confirmed resolution.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Baseline + induced failure"), ("alt", "Diagnosis + confirmed resolution"), ("warn", "Repeatability confirmed")])
    c.save(f"{OUT}/chapter-06-decision-tree-repeatability-flow.svg")


def ch07():
    c = Canvas(960, 640,
        title="Chapter 7 Hands-On Lab: Skipping Containment for Eradication Loses Evidence You Cannot Get Back",
        subtitle="A hardening Fail is scored, risk-rated, and remediated while a simulated incident walks all five NIST phases in order",
        svg_title="Chapter 7 lab flow: a CIS Benchmark hardening check scored, risk-rated, and remediated, alongside a simulated incident walked through all five NIST 800-61 phases, tested against skipping the Containment phase",
        svg_desc="Five hardening controls from a correctly identified, version-dated CIS Benchmark are checked "
                  "against a lab system with linked Pass/Fail evidence; each Fail is assigned a CVSS-style "
                  "severity band and plotted on the chapter's risk matrix using assessed likelihood. A simulated "
                  "minor incident, such as an unauthorized local account creation, is walked through all five "
                  "NIST 800-61 phases, Preparation through Post-Incident Activity, with at least one action and "
                  "one piece of evidence recorded per phase. As a negative test, the exercise attempts to skip "
                  "directly to Eradication without completing Containment, and the evidence-preservation step "
                  "that would be lost by doing so is documented, demonstrating concretely why phase order "
                  "matters rather than asserting it abstractly. The highest-risk Fail is then remediated and "
                  "re-validated against the same control, now passing.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("CIS Benchmark: 5 controls checked", 12.5, 700, "#111827"),
        Line("Fails: CVSS severity + risk-matrix", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "mgmt", [
        Line("Simulated incident", 12.5, 700, "#111827"),
        Line("all 5 NIST 800-61 phases", 10.5, 700, "#1d4ed8"),
        Line("walked in order", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Highest-risk Fail", 12.5, 700, "#111827"),
        Line("remediated + re-validated", 10.5, 700, "#14532d"),
        Line("→ now passes", 10.5, 400, "#374151"),
    ])
    c.connector(600, 185, 700, 185, "alt")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("skip Containment → Eradication", 10.5, 700, "#7f1d1d"),
        Line("→ documented evidence lost", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("the lab system is confirmed returned to its Chapter 4 baseline afterward, and the unauthorized account", 11.5, 400, "#374151"),
        Line("created for the simulated incident is removed as part of cleanup.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Hardening + incident walkthrough"), ("alt", "Remediated finding"), ("warn", "Skipped-phase evidence loss")])
    c.save(f"{OUT}/chapter-07-hardening-incident-phase-order-flow.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: A 401 and a 403 Are Confirmed as Two Different Things, Not One \"Access Denied\"",
        subtitle="A working authenticated call and a documented delivery model anchor the card, and two distinct negative tests separate bad credentials from insufficient permission",
        svg_title="Chapter 8 lab flow: an API reference card built from a documented authentication procedure and one successful authenticated call, tested against an invalid credential and against an unauthorized resource",
        svg_desc="An API's authentication pattern is documented as a secret-free procedure, and one successful "
                  "GET request against a read-only endpoint confirms a 2xx response with a redacted evidence "
                  "excerpt. A JSON response is converted to YAML (or the reverse) with the structural difference "
                  "noted, and the platform's webhook or polling delivery model is recorded. As a first negative "
                  "test, a request made with an invalid or expired credential returns a 401. As a second, "
                  "distinct negative test, a request for a resource the credential is not authorized to access "
                  "returns a 403, confirmed and explicitly distinguished from the 401 case, so the finished card "
                  "documents two different failure modes rather than collapsing them into one generic \"access "
                  "denied\" entry.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Auth documented (secret-free)", 12.5, 700, "#111827"),
        Line("GET → 2xx, evidence redacted", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "mgmt", [
        Line("Format + delivery model", 12.5, 700, "#111827"),
        Line("JSON↔YAML diff noted", 10.5, 400, "#374151"),
        Line("retry/delivery guarantee recorded", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test 1", 12, 700, "#7f1d1d"),
        Line("invalid credential", 10.5, 700, "#7f1d1d"),
        Line("→ 401", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(600, 185, 700, 185, "warn")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test 2", 12, 700, "#7f1d1d"),
        Line("unauthorized resource, valid credential", 10.5, 700, "#7f1d1d"),
        Line("→ 403, distinguished from 401 above", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("any temporary credential created for this lab is revoked or rotated afterward, and every token, key,", 11.5, 400, "#374151"),
        Line("or secret value is redacted from saved evidence before the card is committed.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Documented auth + successful call"), ("warn", "Distinguished 401/403 failure modes")])
    c.save(f"{OUT}/chapter-08-api-reference-auth-failure-flow.svg")


def ch09():
    c = Canvas(960, 620,
        title="Chapter 9 Hands-On Lab: The Capstone — This Encyclopedia's Own Reference Tables Get Audited Against Reality",
        subtitle="Three cited references are independently re-verified against their live authoritative sources, with a compliance check confirming no licensed exam content was ever reproduced",
        svg_title="Chapter 9 capstone lab flow: three reference-library table entries independently re-verified against their live authoritative sources, tested against an attempt to find reproduced certification exam content",
        svg_desc="Three references from this chapter's own tables, one standard, one certification, one vendor "
                  "documentation portal, are recorded as baseline claims, then independently re-verified against "
                  "their live authoritative sources using the Fact/Value/Source/As-of row shape. Comparing the "
                  "two sets surfaces either a confirmed match or a specific, documented discrepancy for each "
                  "item, with a ready-to-apply corrected row drafted for any discrepancy found and cross-checked "
                  "against the repository's root SOFTWARE_VERSIONS.md and CERTIFICATION_BLUEPRINTS.md files. As "
                  "a negative test, the exercise attempts to locate a certification exam question or licensed "
                  "courseware excerpt for one of the cross-referenced certifications; neither this encyclopedia "
                  "nor the findings record reproduces any such content, confirming compliance with "
                  "EDITORIAL_STANDARDS.md's reproduction rule. A concrete, justified review-cadence "
                  "recommendation closes the exercise.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("3 baseline claims recorded", 12.5, 700, "#111827"),
        Line("(standard, cert, vendor doc)", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "alt", [
        Line("Re-verified against", 12.5, 700, "#111827"),
        Line("live authoritative sources", 10.5, 700, "#14532d"),
        Line("→ match or documented discrepancy", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Corrected row drafted", 12.5, 700, "#111827"),
        Line("cross-checked against root", 10.5, 400, "#374151"),
        Line("reference files", 10.5, 400, "#374151"),
    ])
    c.connector(600, 185, 700, 185, "alt")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("search for reproduced exam/", 10.5, 700, "#7f1d1d"),
        Line("courseware content", 10.5, 700, "#7f1d1d"),
        Line("→ confirmed absent, compliant", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("this lab is read-only against external sources — its output is a governance-ready findings record", 11.5, 400, "#374151"),
        Line("plus a review-cadence recommendation, not a change applied directly to the encyclopedia.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Baseline claims"), ("alt", "Independently re-verified"), ("warn", "Confirmed reproduction compliance")])
    c.save(f"{OUT}/chapter-09-capstone-reference-governance-audit-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
