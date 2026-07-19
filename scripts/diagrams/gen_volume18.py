import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-18-gigamon-network-visibility"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Hands-On Lab: A Tabletop Trace That Reproduces Asymmetric Visibility on Paper",
        subtitle="Every subscribed tool has a documented path to a traced session; removing one TAP direction breaks half of it",
        svg_title="Chapter 1 lab flow: a visibility fabric acquisition plan validated by tracing a session through a tap inventory, tested against a missing TAP direction",
        svg_desc="tap-inventory.yaml documents two acquisition points — a SPAN source at the access-to-core "
                  "uplink and a physical TAP at the internet edge, each with subscribed tools (an IDS and a "
                  "packet capture platform) and, for the TAP, both monitor-port directions. A tabletop trace of a "
                  "hypothetical outbound HTTPS session confirms every subscribed tool has an unbroken, documented "
                  "acquisition path. As a negative test, one direction's network_ports entry is removed from the "
                  "internet-edge TAP and the trace re-run for a bidirectional TCP handshake; the trace now shows "
                  "only one direction of traffic reaching the tools, reproducing the asymmetric-visibility failure "
                  "mode entirely on paper before any hardware is touched.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("tap-inventory.yaml", 12.5, 700, "#111827"),
        Line("access-core uplink: SPAN source", 10.5, 400, "#374151"),
        Line("internet edge: TAP, both directions", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Tabletop trace (HTTPS session)", 12, 700, "#111827"),
        Line("every subscribed tool has an", 10.5, 400, "#374151"),
        Line("unbroken, documented path", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("one TAP direction removed", 10.5, 700, "#7f1d1d"),
        Line("→ only 1 direction reaches tools", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the asymmetric-visibility failure mode is reproduced entirely on paper, before any physical hardware", 11.5, 400, "#374151"),
        Line("is touched — the same class of gap a real missing monitor-port entry would cause in production.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Documented acquisition plan"), ("alt", "Verified trace"), ("warn", "Missing direction (negative test)")])
    c.save(f"{OUT}/chapter-01-visibility-fabric-tabletop-trace-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: The Flow Map, Not the Cabling, Is the Traffic-Selection Control Point",
        subtitle="An all-pass map delivers traffic end to end; narrowing the rule to an absent host proves the map itself gates delivery",
        svg_title="Chapter 2 lab flow: a first-touch GigaVUE node with a minimal Flow Map validated end to end, then narrowed to demonstrate the map as the actual traffic-selection control",
        svg_desc="gv-lab-node01 is configured with a network port and a tool port, and a minimal all-pass Flow "
                  "Map forwards tapped traffic between them; a capture tool on the tool port confirms packets "
                  "matching the tapped source, validating acquisition, mapping, and delivery together. As a "
                  "negative test, the map's rule is narrowed from pass any to a specific host IP not present in "
                  "the lab traffic; the capture tool now shows zero new packets, confirming the map — not the "
                  "physical cabling or port configuration, both of which are unchanged — is the actual traffic-"
                  "selection control point.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("gv-lab-node01", 12.5, 700, "#111827"),
        Line("network port + tool port", 10.5, 400, "#374151"),
        Line("Flow Map: pass any", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Capture tool", 12.5, 700, "#111827"),
        Line("shows tapped traffic", 10.5, 700, "#14532d"),
        Line("(acquisition+mapping+delivery OK)", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("rule narrowed to a host IP", 10.5, 700, "#7f1d1d"),
        Line("not present in lab traffic", 10.5, 700, "#7f1d1d"),
        Line("→ zero new packets", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("cabling and port configuration are unchanged between the two tests — only the map rule changed,", 11.5, 400, "#374151"),
        Line("proving the map is the specific control point that governs what traffic actually reaches the tool.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Node + all-pass map"), ("alt", "Confirmed delivery"), ("warn", "Over-narrow rule (no delivery)")])
    c.save(f"{OUT}/chapter-02-gigavue-first-touch-flow-map-flow.svg")


def ch03():
    c = Canvas(960, 620,
        title="Chapter 3 Hands-On Lab: East-West Traffic a Physical TAP Could Never See",
        subtitle="A virtual tap agent tunnels inter-VM traffic to a V Series node; disabling the agent proves acquisition coverage — not the map — was the point of failure",
        svg_title="Chapter 3 lab topology: a virtual tap agent tunneling east-west VM traffic to a V Series node, tested against a disabled agent representing a coverage gap",
        svg_desc="Two workload VMs on the same virtual switch communicate directly — traffic no physical TAP "
                  "could ever observe. A virtual tap agent on the first workload VM tunnels its traffic to a "
                  "V Series node's tunnel-endpoint IP, where a minimal all-pass Flow Map delivers it to a capture "
                  "tool; the capture confirms the inter-VM session end to end. As a negative test, the virtual "
                  "tap agent is stopped on the first workload VM while the map and V Series node stay unchanged; "
                  "no new traffic reaches the capture tool, confirming acquisition coverage — not the mapping or "
                  "the node — was the point of failure, the same partial-coverage failure mode as a Kubernetes "
                  "DaemonSet not covering every node. Re-enabling the agent restores visibility immediately.")
    c.node_box(60, 140, 220, 110, "mgmt", [
        Line("Workload VM 1", 13, 700, "#111827"),
        Line("virtual tap agent installed", 10.5, 700, "#1d4ed8"),
        Line("(negative test: agent disabled)", 10, 700, "#7f1d1d"),
    ])
    c.node_box(360, 140, 220, 110, "mgmt", [
        Line("Workload VM 2", 13, 700, "#111827"),
        Line("generates traffic toward VM 1", 10.5, 400, "#374151"),
    ])
    c.connector(280, 195, 360, 195, "mgmt", label="east-west (same vSwitch)")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("V Series node", 12.5, 700, "#111827"),
        Line("tunnel-endpoint + all-pass map", 10.5, 400, "#374151"),
        Line("→ capture tool shows traffic", 10.5, 700, "#14532d"),
    ])
    c.connector(160, 250, 700, 200, "mgmt", label="tunneled capture")
    c.node_box(60, 340, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("virtual tap agent on VM 1 stopped — map and V Series node otherwise unchanged", 11, 400, "#7f1d1d"),
        Line("no new traffic reaches the capture tool despite VM 2 still generating traffic toward VM 1", 11, 400, "#7f1d1d"),
        Line("acquisition coverage, not the map or the node, was the point of failure — a partial-coverage gap", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "East-west traffic source"), ("alt", "Tunnel delivery to visibility node")])
    c.save(f"{OUT}/chapter-03-virtual-tap-east-west-topology.svg")


def ch04():
    c = Canvas(960, 620,
        title="Chapter 4 Hands-On Lab: GigaVUE-FM RBAC Scoped Per Fabric Group, Not Just Per Capability",
        subtitle="A flow-author role writes successfully on its own fabric group and is still denied on a second, unrelated one",
        svg_title="Chapter 4 lab flow: GigaVUE-FM onboarding and scoped RBAC roles, tested against a role's access to a fabric group outside its scope",
        svg_desc="A lab GigaVUE node onboards into fabric group lab-fabric-01, appearing healthy in GigaVUE-FM's "
                  "inventory. A lab-read-only role is denied when attempting to create a Flow Map, while a "
                  "lab-flow-author role successfully creates one on the same fabric group, confirming both roles' "
                  "granted permissions function as intended. As a negative test, the lab-flow-author user "
                  "attempts to access a second, unrelated fabric group (lab-fabric-02) not included in that "
                  "role's scope; access is denied, confirming role scoping is enforced per fabric group and not "
                  "merely per capability — write permission on one fabric group does not imply write permission "
                  "on another. The audit log correctly attributes every login, denial, and successful write to "
                  "the right identity.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("lab-fabric-01 (onboarded node)", 12, 700, "#111827"),
        Line("lab-read-only: write denied", 10.5, 700, "#7f1d1d"),
        Line("lab-flow-author: write succeeds", 10.5, 700, "#14532d"),
    ])
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("lab-flow-author attempts", 10.5, 700, "#7f1d1d"),
        Line("lab-fabric-02 (out of scope)", 10.5, 700, "#7f1d1d"),
        Line("→ access denied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 195, 700, 195, "warn", label="cross-fabric-group attempt")
    c.node_box(60, 300, 860, 90, "neutral", [
        Line("write permission scoped to lab-fabric-01 does not extend to lab-fabric-02 — role scoping is enforced", 11.5, 400, "#374151"),
        Line("per fabric group, not merely per capability, and every action is attributed correctly in the audit log.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 430, [("mgmt", "In-scope fabric group"), ("warn", "Out-of-scope access attempt")])
    c.save(f"{OUT}/chapter-04-gigavue-fm-rbac-scope-flow.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: A Rule-Order Defect That Silently Reopens an Excluded Path",
        subtitle="Matching traffic reaches the GigaStream tool farm tagged correctly; a lower-priority pass-any rule leaks traffic the filter should have excluded",
        svg_title="Chapter 5 lab flow: a two-level filtered Flow Map feeding a tagged GigaStream tool group, tested against a rule-order defect",
        svg_desc="A first-level map filters one network source down to a specific subnet; a second-level map "
                  "forwards that output to a GigaStream group of two tool ports with an egress VLAN tag applied. "
                  "Matching traffic appears at both capture tools with the correct tag, and traffic outside the "
                  "filter correctly produces no output. As a negative test, a broad pass any rule is added at a "
                  "lower priority number (evaluated first) than the first-level map's existing filter; the "
                  "previously excluded traffic now appears at the tool farm, reproducing the rule-order failure "
                  "mode where a badly prioritized rule silently reopens a path the filter was designed to close. "
                  "Removing the defect rule restores correct exclusion.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("First-level map", 12.5, 700, "#111827"),
        Line("filters to specific subnet", 10.5, 400, "#374151"),
        Line("excluded traffic → no output", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 140, 260, 110, "alt", [
        Line("GigaStream group (2 tools)", 12, 700, "#111827"),
        Line("VLAN-tagged, matching traffic", 10.5, 700, "#14532d"),
        Line("visible at both tools", 10.5, 400, "#374151"),
    ])
    c.connector(320, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("pass-any rule added at", 10.5, 700, "#7f1d1d"),
        Line("lower priority (evaluated first)", 10.5, 700, "#7f1d1d"),
        Line("→ excluded traffic now leaks", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 195, 700, 195, "warn")
    c.node_box(60, 300, 860, 90, "neutral", [
        Line("removing the defect rule restores correct exclusion — the map's filtering behavior depends entirely", 11.5, 400, "#374151"),
        Line("on rule priority order, not just on which rules exist.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 430, [("mgmt", "First-level filter"), ("alt", "Correctly delivered, tagged traffic"), ("warn", "Rule-order defect (leaked traffic)")])
    c.save(f"{OUT}/chapter-05-two-level-map-rule-order-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: A Masking Offset That Must Be Validated Against Real Traffic, Not Assumed",
        subtitle="The configured slice and mask hide the test pattern correctly; a misaligned offset by even a few bytes exposes it in plain sight",
        svg_title="Chapter 6 lab flow: a GigaSMART slicing and masking chain validated against a known test pattern, then deliberately misaligned",
        svg_desc="A gsgroup slices packets shortly after the TCP/IP header and masks a known test payload pattern "
                  "at its correct offset, fed by the two-level map pattern from Chapter 5. Captured packets at the "
                  "tool port show the correct truncation and the test pattern masked with the configured fixed "
                  "value rather than its original bytes. As a negative test, the masking operation's offset is "
                  "shifted by a fixed number of bytes so it no longer aligns with the test pattern's actual "
                  "position; the captured packets now show the original, unmasked test pattern in plain sight at "
                  "its true offset, reproducing the misaligned-masking failure mode — proof that offset and length "
                  "must be validated against actual observed traffic, not assumed from documentation alone.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("gsgroup: slice + mask", 12.5, 700, "#111827"),
        Line("slice after TCP/IP header", 10.5, 400, "#374151"),
        Line("mask test pattern at correct offset", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Capture at tool port", 12.5, 700, "#111827"),
        Line("truncated correctly", 10.5, 400, "#374151"),
        Line("test pattern masked, not readable", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("mask offset shifted (misaligned)", 10.5, 700, "#7f1d1d"),
        Line("→ original pattern exposed", 10.5, 700, "#7f1d1d"),
        Line("in plain sight", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("correcting the offset back to the validated value restores masked output — offset and length must be", 11.5, 400, "#374151"),
        Line("verified against real traffic captures, not assumed correct from documentation alone.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "GigaSMART transform"), ("alt", "Correctly masked output"), ("warn", "Misaligned mask (exposed data)")])
    c.save(f"{OUT}/chapter-06-gigasmart-masking-offset-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: Fail-Open Keeps Traffic Moving; Fail-Closed Is a Deliberate, Different Choice",
        subtitle="The same tool failure produces continued traffic under fail-open and a hard stop under fail-closed — the trade-off is configured, not assumed",
        svg_title="Chapter 7 lab topology: an inline bypass deployment with heartbeat-based failover, tested under both fail-open and fail-closed modes, plus manual maintenance mode",
        svg_desc="An inline network group and inline tool group with heartbeat monitoring pass continuous traffic "
                  "between two lab hosts through a healthy inline tool. Failing the tool with fail-mode set to "
                  "open causes a brief interruption during heartbeat detection, after which traffic resumes "
                  "flowing in bypass — fail-open protects connectivity. As a negative test, fail-mode is changed "
                  "to closed and the same tool failure repeated; this time traffic stops entirely and does not "
                  "resume until the tool is restored, demonstrating the fail-closed security-availability "
                  "trade-off is a deliberate configuration choice, not a default behavior. Manually invoking "
                  "maintenance mode bypasses the tool immediately, independent of heartbeat detection entirely.")
    c.node_box(60, 130, 220, 110, "mgmt", [
        Line("Lab host A", 12.5, 700, "#111827"),
        Line("continuous traffic", 10.5, 400, "#374151"),
        Line("to lab host B", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 220, 110, "alt", [
        Line("Inline tool (healthy)", 12.5, 700, "#111827"),
        Line("heartbeat: healthy", 10.5, 700, "#14532d"),
        Line("traffic passes through", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 130, 220, 110, "mgmt", [
        Line("Lab host B", 12.5, 700, "#111827"),
        Line("receives traffic", 10.5, 400, "#374151"),
    ])
    c.connector(280, 185, 360, 185, "mgmt")
    c.connector(580, 185, 700, 185, "alt")
    c.node_box(60, 300, 400, 130, "alt", [
        Line("fail-mode: open", 12.5, 700, "#111827"),
        Line("tool fails → brief interruption", 10.5, 400, "#374151"),
        Line("→ traffic resumes (bypass)", 10.5, 700, "#14532d"),
        Line("connectivity protected", 10.5, 400, "#374151"),
    ])
    c.node_box(500, 300, 400, 130, "warn", [
        Line("Negative Test — fail-mode: closed", 12, 700, "#7f1d1d"),
        Line("same tool failure repeated", 10.5, 700, "#7f1d1d"),
        Line("→ traffic STOPS entirely", 10.5, 700, "#7f1d1d"),
        Line("does not resume until tool restored", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("maintenance mode, invoked manually, bypasses the tool immediately regardless of fail-mode setting —", 11.5, 400, "#374151"),
        Line("a controlled bypass path that never waits for heartbeat detection at all.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Traffic endpoints"), ("alt", "Fail-open (connectivity protected)"), ("warn", "Fail-closed (deliberate trade-off)")])
    c.save(f"{OUT}/chapter-07-inline-bypass-failover-topology.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: API Scope Enforcement Matches the UI, Not Just at the Web Layer",
        subtitle="A read-only token queries fabric health successfully and is rejected outright when it attempts to create a Flow Map",
        svg_title="Chapter 8 lab flow: GigaVUE-FM REST API access scoped by service-account role, tested against a write attempt using a read-only token",
        svg_desc="A service account scoped to read-only access on the lab fabric group authenticates to the "
                  "GigaVUE-FM API and successfully queries node inventory and health status. As a negative test, "
                  "the same read-only token attempts a write operation — creating a new Flow Map; the API rejects "
                  "the call with an authorization error, confirming the scoped role enforces least privilege at "
                  "the API layer itself, not merely in the web UI. A second, write-scoped service account "
                  "performs the identical map-creation call successfully, and the new map is visible both via the "
                  "API and in the web UI, with the action correctly attributed to that account in the audit log.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("Read-only service account", 12.5, 700, "#111827"),
        Line("GET /v1/nodes", 10.5, 400, "#374151"),
        Line("→ inventory + health returned", 10.5, 700, "#14532d"),
    ])
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("same token: POST /v1/maps", 10.5, 700, "#7f1d1d"),
        Line("→ authorization error", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 195, 700, 195, "warn", label="write attempt with read-only token")
    c.node_box(60, 300, 860, 120, "alt", [
        Line("Write-scoped service account", 12.5, 700, "#111827"),
        Line("identical POST /v1/maps call → succeeds", 11, 400, "#374151"),
        Line("map visible via API (GET /v1/maps) and in the web UI", 11, 400, "#374151"),
        Line("audit log correctly attributes the write to this account's identity", 11, 700, "#14532d"),
    ])
    c.legend(60, 460, [("mgmt", "Read-only API access"), ("alt", "Write-scoped API access"), ("warn", "Enforced API-layer denial")])
    c.save(f"{OUT}/chapter-08-gigavue-fm-api-scope-flow.svg")


def ch09():
    c = Canvas(960, 680,
        title="Chapter 9 Hands-On Lab: The Capstone — a Full Acquisition-to-Delivery Chain That Fails in Isolation, Not Together",
        subtitle="Every stage traces correctly end to end; the out-of-band rule change and the inline tool failure each reproduce their own chapter's exact failure with no cross-stage interaction",
        svg_title="Chapter 9 lab flow: the volume's integrated capstone — acquisition, mapping, GigaSMART, and inline resiliency composed together, validated with a multi-stage negative test and a documented rollback",
        svg_desc="An acquisition source feeds a first-level map into a GigaSMART group performing slicing and "
                  "Application Metadata Intelligence export, delivered by a second-level map to an out-of-band "
                  "capture tool; a separate inline network and tool group with fail-open heartbeat failover runs "
                  "on a distinct lab link. A full-chain trace confirms traffic at every stage — acquisition, "
                  "mapping, GigaSMART processing, delivery, and metadata export — end to end, with the inline "
                  "path separately confirmed passing traffic. A multi-stage negative test narrows the first-level "
                  "map to exclude the test traffic (out-of-band chain correctly shows no output, then restored) "
                  "and separately fails the inline tool (inline path fails open, then restored); both reproduce "
                  "their own chapter's isolated failure mode with no cross-stage interaction — the out-of-band "
                  "change never touched the inline path, and the inline failure never touched the out-of-band "
                  "chain. An API diff against the pre-capstone baseline confirms no configuration drift, and the "
                  "documented rollback plan is executed and validated.")
    c.node_box(60, 120, 260, 110, "mgmt", [
        Line("Acquisition → 1st-level map", 12.5, 700, "#111827"),
        Line("→ GigaSMART (slice + AMI export)", 10.5, 400, "#374151"),
        Line("→ 2nd-level map → OOB capture", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 120, 260, 110, "alt", [
        Line("Full-chain trace", 12.5, 700, "#111827"),
        Line("every stage shows expected", 10.5, 400, "#374151"),
        Line("traffic/output end to end", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 175, 360, 175, "mgmt")
    c.node_box(680, 120, 240, 110, "mgmt", [
        Line("Inline path (distinct link)", 12.5, 700, "#111827"),
        Line("fail-open heartbeat", 10.5, 400, "#374151"),
        Line("passes traffic through tool", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 280, 400, 130, "warn", [
        Line("Negative Test (a): OOB path", 12, 700, "#7f1d1d"),
        Line("1st-level map narrowed to exclude", 10.5, 400, "#7f1d1d"),
        Line("test traffic → no output, restored", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(500, 280, 400, 130, "warn", [
        Line("Negative Test (b): inline path", 12, 700, "#7f1d1d"),
        Line("inline tool failed → fails open,", 10.5, 400, "#7f1d1d"),
        Line("restored per Chapter 7's behavior", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(60, 440, 840, 90, "neutral", [
        Line("neither negative test affects the other path — confirming no unexpected cross-stage interaction", 11.5, 400, "#374151"),
        Line("was introduced by integrating the mechanisms together into one deployment.", 11.5, 400, "#374151"),
    ])
    c.node_box(60, 550, 840, 90, "alt", [
        Line("API diff against the pre-capstone baseline confirms zero configuration drift", 11.5, 700, "#14532d"),
        Line("the documented rollback plan is executed and validated to restore the exact pre-capstone state", 11.5, 400, "#374151"),
    ])
    c.legend(60, 660, [("mgmt", "Integrated pipeline"), ("alt", "Verified trace / rollback"), ("warn", "Isolated negative tests")])
    c.save(f"{OUT}/chapter-09-capstone-integrated-chain-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
