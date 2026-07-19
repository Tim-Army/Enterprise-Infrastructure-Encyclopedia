import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-15-forescout-platform-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Hands-On Lab: Passive Visibility That Goes Silent Exactly When the Mirror Feed Does",
        subtitle="Three endpoints classify from a SPAN feed alone; shutting the SPAN destination interface stops all new host activity",
        svg_title="Chapter 1 lab topology: passive host discovery over a SPAN session, tested against an interrupted mirror feed",
        svg_desc="A lab switch mirrors three test endpoints (Windows, Linux, and an IoT simulator) to the "
                  "Forescout appliance's monitor interface. Within minutes all three appear in the inventory with "
                  "MAC, IP, and a provisional classification; enabling scoped active scanning adds more specific "
                  "detail such as OS version. As a negative test, the SPAN destination interface is shut down on "
                  "the switch; the Console reports the monitor interface down and no new host activity registers "
                  "at all, demonstrating the platform's total dependency on a correctly delivered mirror feed. "
                  "Re-enabling the interface resumes host updates immediately.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Lab switch — SPAN session", 12.5, 700, "#111827"),
        Line("mirrors 3 test endpoints", 10.5, 400, "#374151"),
        Line("(Windows, Linux, IoT)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 260, 120, "alt", [
        Line("Forescout appliance", 12.5, 700, "#111827"),
        Line("monitor interface (passive)", 10.5, 400, "#374151"),
        Line("MAC + IP + classification within minutes", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt", label="mirrored traffic")
    c.node_box(700, 140, 220, 120, "neutral", [
        Line("Active scan (scoped)", 12.5, 700, "#111827"),
        Line("adds OS version detail", 10.5, 400, "#374151"),
        Line("to the same 3 hosts", 10.5, 400, "#374151"),
    ])
    c.connector(660, 200, 700, 200, "alt")
    c.node_box(60, 340, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("SPAN destination interface shut down on the switch", 11, 400, "#7f1d1d"),
        Line("Console reports the monitor interface down; no new host activity registers at all", 11, 400, "#7f1d1d"),
        Line("re-enabling the interface resumes host updates immediately", 11, 400, "#14532d"),
    ])
    c.legend(60, 500, [("mgmt", "Mirror feed"), ("alt", "Passive classification"), ("neutral", "Active-scan refinement")])
    c.save(f"{OUT}/chapter-01-passive-visibility-span-topology.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A Classification Rule Correctly Scoped, Then Deliberately Broadened",
        subtitle="A specific condition classifies exactly the intended endpoint; loosening it to a single common port misclassifies a neighbor",
        svg_title="Chapter 2 lab flow: a custom property and classification policy validated for precision, then deliberately over-broadened",
        svg_desc="A custom Lab Asset Owner property is created and set on a test endpoint, appearing alongside "
                  "built-in properties on its host record. A classification rule sets Function based on a "
                  "condition specific to that device type; applying it updates the endpoint's Function correctly, "
                  "and an inventory view filtered on that Function value shows the test endpoint while excluding "
                  "unrelated hosts. As a negative test, the rule's condition is deliberately broadened to match "
                  "only a single common open port with no other qualifier; reapplying it now incorrectly matches "
                  "at least one other host on the segment, demonstrating why rule specificity and ordering matter "
                  "before the rule is reverted to its specific form.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Custom property + specific rule", 12, 700, "#111827"),
        Line("Lab Asset Owner + device-specific", 10.5, 400, "#374151"),
        Line("Function condition", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 260, 120, "alt", [
        Line("Correct classification", 12.5, 700, "#111827"),
        Line("only the intended endpoint matches", 10.5, 700, "#14532d"),
        Line("inventory view filters correctly", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("rule broadened to 1 common port", 10.5, 700, "#7f1d1d"),
        Line("misclassifies a neighbor host", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(660, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("rule specificity and ordering directly determine classification accuracy — an over-broad condition", 11.5, 400, "#374151"),
        Line("silently over-matches, which is why the rule is reverted to its specific form immediately after the test.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Property + specific rule"), ("alt", "Correctly scoped match"), ("warn", "Over-broad rule (negative test)")])
    c.save(f"{OUT}/chapter-02-classification-rule-specificity-flow.svg")


def ch03():
    c = Canvas(960, 660,
        title="Chapter 3 Hands-On Lab: Monitor-Mode Preview, Live Enforcement, and an Exclusion Group That Actually Holds",
        subtitle="A compliance grace period drives a control policy from a logged preview to a real VLAN reassignment — until the host is excluded",
        svg_title="Chapter 3 lab flow: a compliance and control policy pair staged through monitor mode to live enforcement, tested against an exclusion group",
        svg_desc="Toggling Lab Agent Running to false triggers the compliance policy to set Compliance Status to "
                  "Non-Compliant after a 10-minute grace period. The paired control policy, first in monitor "
                  "mode, logs the VLAN reassignment it would have taken without touching the endpoint. Switching "
                  "to live enforcement and re-triggering the condition actually reassigns the endpoint's VLAN; "
                  "restoring Lab Agent Running to true returns it to its original VLAN within one re-evaluation "
                  "cycle. As a negative test, the endpoint is added to an exclusion group and the non-compliant "
                  "condition is forced again; the control policy does not act despite matching, confirming the "
                  "exclusion-group safeguard takes precedence — the same mechanism production deployments rely on "
                  "to protect sensitive hosts.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Lab Agent Running = false", 12.5, 700, "#111827"),
        Line("compliance policy: grace period", 10.5, 400, "#374151"),
        Line("→ Non-Compliant: Lab", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "neutral", [
        Line("Control policy: monitor mode", 12, 700, "#111827"),
        Line("logs the VLAN reassignment", 10.5, 400, "#374151"),
        Line("it WOULD have taken", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Live enforcement", 12.5, 700, "#111827"),
        Line("actual VLAN reassignment", 10.5, 700, "#14532d"),
        Line("re-admits on compliance", 10.5, 400, "#374151"),
    ])
    c.connector(620, 195, 700, 195, "alt")
    c.node_box(60, 320, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("endpoint added to an exclusion group, then Lab Agent Running forced to false again", 11, 400, "#7f1d1d"),
        Line("control policy does NOT act despite the compliance condition matching — exclusion takes precedence", 11, 400, "#7f1d1d"),
        Line("the same safeguard production deployments rely on to protect sensitive hosts from enforcement", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Compliance transition"), ("neutral", "Monitor-mode preview"), ("alt", "Live enforcement + re-admission")])
    c.save(f"{OUT}/chapter-03-compliance-control-exclusion-flow.svg")


def ch04():
    c = Canvas(960, 620,
        title="Chapter 4 Hands-On Lab: RBAC Scope Enforced Against Writes, Not Just the Inventory View",
        subtitle="A scoped read-only account sees only its permitted population and is actually blocked from modifying anything outside it",
        svg_title="Chapter 4 lab flow: a role-scoped read-only user, a dynamic group, and a scheduled report, tested against an out-of-scope write attempt",
        svg_desc="A custom role scoped to a single lab group is assigned to a second test user; logging in as "
                  "that user shows only the scoped population, with hosts outside the scope invisible. A dynamic "
                  "group defined by Compliance Status = Non-Compliant: Lab updates membership automatically as "
                  "the underlying property is toggled, and a report scoped to that group exports correctly and "
                  "can be scheduled. A configuration backup completes and is retrievable. As a negative test, the "
                  "scoped read-only account attempts to modify a policy or host property outside its granted "
                  "permissions; the platform denies the action, confirming RBAC scope restriction is enforced at "
                  "the write layer, not merely cosmetic in the inventory view.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Scoped read-only role", 12.5, 700, "#111827"),
        Line("assigned to test user", 10.5, 400, "#374151"),
        Line("sees only its scoped population", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Dynamic group + report", 12.5, 700, "#111827"),
        Line("membership auto-updates on", 10.5, 400, "#374151"),
        Line("Compliance Status changes", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("scoped account attempts a", 10.5, 700, "#7f1d1d"),
        Line("write outside its permissions", 10.5, 700, "#7f1d1d"),
        Line("→ denied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("the denial confirms RBAC scope restriction is enforced by the platform itself at the write layer,", 11.5, 400, "#374151"),
        Line("not merely a filter applied to what the inventory view happens to display.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Scoped role"), ("alt", "Reactive group + report"), ("warn", "Enforced write restriction")])
    c.save(f"{OUT}/chapter-04-rbac-scope-enforcement-flow.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: A Simulated Closed-Loop Integration That Still Respects the Exclusion Group",
        subtitle="A critical-severity property drives an escalation and a matching resolution — but never against a protected host",
        svg_title="Chapter 5 lab flow: a simulated inbound enrichment property driving a policy-triggered notification, closed by a resolution rule, tested against an exclusion group",
        svg_desc="A Lab Vulnerability Severity property stands in for an imported vulnerability-scanner field. "
                  "Setting it to Critical fires a policy that sets Compliance Status to Non-Compliant: Critical "
                  "CVE and delivers a simulated ITSM notification. Returning the severity to None fires a paired "
                  "resolution rule that clears the compliance state and sends a resolved notification, completing "
                  "the simulated closed loop. As a negative test, the endpoint is placed in the "
                  "Exclusion - Managed Exceptions group and the severity forced to Critical again; the policy "
                  "does not escalate the excluded host, confirming integration-triggered policies respect the "
                  "same exclusion-group safeguard as directly authored control policies.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Lab Vulnerability Severity", 12.5, 700, "#111827"),
        Line("None → Critical", 10.5, 400, "#374151"),
        Line("policy fires: notify + Non-Compliant", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Closed-loop resolution", 12.5, 700, "#111827"),
        Line("severity → None", 10.5, 400, "#374151"),
        Line("clears status + resolved notice", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("host in exclusion group,", 10.5, 700, "#7f1d1d"),
        Line("severity forced Critical again", 10.5, 700, "#7f1d1d"),
        Line("→ NOT escalated", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("integration-triggered escalations respect the same exclusion-group safeguard as directly authored", 11.5, 400, "#374151"),
        Line("control policies — the protection isn't bypassed just because the trigger came from an external property.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Simulated inbound trigger"), ("alt", "Closed-loop resolution"), ("warn", "Exclusion-protected host")])
    c.save(f"{OUT}/chapter-05-integration-closed-loop-exclusion-flow.svg")


def ch06():
    c = Canvas(960, 640,
        title="Chapter 6 Hands-On Lab: A Layered Diagnosis, a Validated Restore, and a Plugin Failure Isolated From the Network",
        subtitle="A revoked SNMP credential surfaces as a plugin-layer failure, distinct from a network-delivery problem, and recovers cleanly once reverted",
        svg_title="Chapter 6 lab flow: baseline resource metrics, a layered diagnostic model, and a validated backup/restore, tested against a plugin credential failure",
        svg_desc="Baseline CPU, memory, and disk metrics are recorded during idle operation; increasing active-"
                  "scan intensity produces an observable (or documented) resource-metric effect that reverts "
                  "toward baseline once the change is undone. A layered diagnostic write-up for 'Console feels "
                  "slow' works down from network delivery through appliance health, plugin, and policy layers. A "
                  "configuration backup is taken, restored (onto a second instance or as a documented dry run), "
                  "and validated by confirming at least one policy and one custom property survived correctly. As "
                  "a negative test, the Switch plugin's SNMP community string is changed only in the plugin "
                  "configuration (not on the switch itself); the plugin layer surfaces a clear authentication/"
                  "connectivity failure distinct from a network-delivery failure, and reverting the credential "
                  "restores clean operation.")
    c.node_box(60, 130, 240, 100, "mgmt", [
        Line("Baseline metrics", 12.5, 700, "#111827"),
        Line("CPU/mem/disk, idle operation", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 130, 240, 100, "neutral", [
        Line("Layered diagnostic model", 12, 700, "#111827"),
        Line("network → appliance → plugin →", 10.5, 400, "#374151"),
        Line("property/policy → downstream", 10.5, 400, "#374151"),
    ])
    c.connector(300, 180, 380, 180, "mgmt")
    c.node_box(700, 130, 220, 100, "alt", [
        Line("Backup / restore", 12.5, 700, "#111827"),
        Line("validated: policy + property", 10.5, 700, "#14532d"),
        Line("present post-restore", 10.5, 400, "#374151"),
    ])
    c.connector(620, 180, 700, 180, "neutral")
    c.node_box(60, 310, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Switch plugin's SNMP community string changed only in plugin config, not on the switch itself", 11, 400, "#7f1d1d"),
        Line("plugin layer surfaces a clear authentication/connectivity failure — distinct from a network-delivery failure", 11, 400, "#7f1d1d"),
        Line("reverting the credential restores clean operation, confirming the failure was correctly isolated", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 480, [("mgmt", "Baseline"), ("neutral", "Diagnostic layers"), ("alt", "Validated recovery")])
    c.save(f"{OUT}/chapter-06-layered-diagnosis-plugin-failure-flow.svg")


def ch07():
    c = Canvas(960, 620,
        title="Chapter 7 Hands-On Lab: An Idempotent API Reconciliation Script Bounded by Its Own Credential Scope",
        subtitle="The second run of the corrective script makes no additional changes, and the same credential is refused for anything outside its one granted property",
        svg_title="Chapter 7 lab flow: a scoped API reconciliation script proven idempotent and bounded by credential scope, feeding the volume's capstone design document",
        svg_desc="A read-only-scoped API credential queries the inventory for hosts matching a filter; a "
                  "reconciliation script compares a reference CSV against live property values and prints a "
                  "discrepancy report with no writes. Re-issuing the credential with write scope for exactly one "
                  "custom property lets the script correct that discrepancy; running the extended script twice in "
                  "succession shows the second run makes no additional changes, and the audit log attributes both "
                  "runs to the scoped credential. As a negative test, the same write-scoped credential attempts an "
                  "API call outside its granted scope — modifying a control policy; the platform denies the call, "
                  "confirming API scope enforcement constrains the automation, not just its documentation. The "
                  "lab closes with a capstone design document cross-referencing all seven synthesis steps.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Read-only API credential", 12.5, 700, "#111827"),
        Line("queries inventory + reference CSV", 10.5, 400, "#374151"),
        Line("discrepancy report, no writes", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Write-scoped credential", 12.5, 700, "#111827"),
        Line("(1 custom property only)", 10.5, 400, "#374151"),
        Line("2nd run: no additional changes", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("same credential attempts", 10.5, 700, "#7f1d1d"),
        Line("to modify a control policy", 10.5, 700, "#7f1d1d"),
        Line("→ denied (out of scope)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("API scope enforcement blocks the out-of-scope call at the platform level — the credential's grant is", 11.5, 400, "#374151"),
        Line("what actually constrains the automation, not merely how the script itself was written to behave.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Read-only phase"), ("alt", "Idempotent write phase"), ("warn", "Scope-enforced denial")])
    c.save(f"{OUT}/chapter-07-api-reconciliation-scope-flow.svg")


def ch08():
    c = Canvas(960, 620,
        title="Chapter 8 Hands-On Lab: A Passive OT Sensor at the Purdue Boundary That Degrades to Silence, Never to Active Probing",
        subtitle="The sensor identifies Modbus function codes between simulated Level 1 and Level 2 assets, and loses visibility cleanly when the SPAN feed drops",
        svg_title="Chapter 8 lab topology: a passive OT sensor placed at a Purdue-model boundary, observing Modbus traffic and tested against an interrupted SPAN feed",
        svg_desc="A simulated PLC (Purdue Level 1) and an HMI/engineering workstation simulator (Level 2) exchange "
                  "Modbus TCP traffic — read holding registers and write single coil operations — mirrored by a "
                  "SPAN session to the sensor's receive-only monitor interface at the Level 1/2 boundary. The "
                  "sensor correctly identifies the protocol and function codes, and its configuration confirms no "
                  "active probing capability is enabled. As a negative test, the SPAN destination interface is "
                  "disconnected; the sensor immediately loses visibility of the simulated PLC traffic entirely, "
                  "with no compensating active technique attempting to reach the PLC directly — passive OT "
                  "visibility degrades to silence, not to an active fallback. Re-enabling SPAN restores visibility.")
    c.node_box(60, 140, 220, 110, "mgmt", [
        Line("PLC simulator", 13, 700, "#111827"),
        Line("Purdue Level 1", 10.5, 400, "#374151"),
        Line("Modbus TCP responses", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 140, 220, 110, "mgmt", [
        Line("HMI/eng. workstation sim", 12, 700, "#111827"),
        Line("Purdue Level 2", 10.5, 400, "#374151"),
        Line("read/write coil requests", 10.5, 400, "#374151"),
    ])
    c.connector(280, 195, 360, 195, "mgmt", label="Modbus TCP (mirrored)")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Sensor (receive-only)", 12.5, 700, "#111827"),
        Line("identifies protocol + function", 10.5, 700, "#14532d"),
        Line("codes, no active probing", 10.5, 400, "#374151"),
    ])
    c.connector(320, 250, 700, 195, "alt", label="SPAN feed")
    c.node_box(60, 340, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("SPAN destination interface disconnected on the switch", 11, 400, "#7f1d1d"),
        Line("sensor loses visibility of PLC traffic entirely — no active technique compensates by probing the PLC", 11, 400, "#7f1d1d"),
        Line("passive OT visibility correctly degrades to silence, not to an active fallback; SPAN restored → visibility resumes", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Simulated Purdue-level assets"), ("alt", "Passive sensor")])
    c.save(f"{OUT}/chapter-08-ot-purdue-passive-sensor-topology.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: Two-Zone Curation, a Behavioral Baseline, and Escalation That Depends on Timely Change Data",
        subtitle="An anomalous write operation escalates as unapproved until a matching change ticket exists, then correlates cleanly",
        svg_title="Chapter 9 lab topology: a two-zone OT visibility extension with an asset-register curation pass and a behavioral baseline, tested against change-ticket correlation",
        svg_desc="Chapter 8's single zone extends to a second simulated cell/area zone (Line 2), each "
                  "independently visible through its own SPAN session and sensor. A curation pass compares "
                  "sensor-observed assets against a manually maintained asset register, producing at least one "
                  "documented discrepancy finding. A behavioral baseline defines one zone as reads-only under "
                  "normal operation; a deliberate write/program-download operation is then generated and "
                  "confirmed distinguishable from that baseline. As a negative test, the anomalous operation is "
                  "correlated against a change ticket that deliberately does not exist yet; the documented process "
                  "correctly escalates it as unapproved. Creating a matching change record after the fact causes "
                  "the same operation to now correlate as approved, demonstrating that the escalation logic's "
                  "accuracy depends entirely on timely change-management data.")
    c.node_box(60, 130, 240, 100, "mgmt", [
        Line("Zone 1 (Line 1)", 12.5, 700, "#111827"),
        Line("PLC + SPAN + sensor", 10.5, 400, "#374151"),
    ])
    c.node_box(320, 130, 240, 100, "mgmt", [
        Line("Zone 2 (Line 2)", 12.5, 700, "#111827"),
        Line("second PLC + SPAN + sensor", 10.5, 400, "#374151"),
    ])
    c.node_box(600, 130, 300, 100, "neutral", [
        Line("Curation pass", 12.5, 700, "#111827"),
        Line("sensor-observed vs. asset register", 10.5, 400, "#374151"),
        Line("≥1 documented discrepancy", 10.5, 700, "#1d4ed8"),
    ])
    c.connector(280, 185, 320, 185, "mgmt")
    c.connector(560, 180, 600, 180, "neutral")
    c.node_box(60, 280, 400, 100, "alt", [
        Line("Behavioral baseline", 12.5, 700, "#111827"),
        Line("reads-only expected in Zone 1", 10.5, 400, "#374151"),
        Line("anomalous write operation → distinguishable", 10.5, 400, "#374151"),
    ])
    c.node_box(500, 280, 400, 100, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("no matching change ticket → escalates as unapproved", 10.5, 700, "#7f1d1d"),
        Line("matching ticket created after the fact → now correlates as approved", 10.5, 700, "#7c2d12"),
    ])
    c.connector(460, 330, 500, 330, "warn")
    c.legend(60, 440, [("mgmt", "Independent zone visibility"), ("neutral", "Curation finding"), ("alt", "Baseline + anomaly"), ("warn", "Change-correlation dependency")])
    c.save(f"{OUT}/chapter-09-ot-two-zone-curation-baseline-topology.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
