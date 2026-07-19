import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-16-palo-alto-networks-security"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Hands-On Lab: PAN-OS Candidate Configuration Validation Rejects an Invalid Management IP",
        subtitle="A hostname, management address, and scoped admin commit cleanly; a broadcast-adjacent address does not",
        svg_title="Chapter 1 lab flow: first-touch PAN-OS configuration committed successfully, then a deliberately invalid management address tested against commit validation",
        svg_desc="pa-lab-fw01's hostname and management IP (10.10.10.5/24) commit successfully, confirmed by SSH "
                  "reachability from the workstation; a second, role-based administrator account (labeng) is "
                  "created for daily use instead of admin. As a negative test, the management IP is set to "
                  "10.10.10.255 — a broadcast-adjacent address outside any valid host range for the configured "
                  "netmask — and committed; PAN-OS either rejects the commit outright or the interface becomes "
                  "unreachable at that address, confirming candidate-configuration validation catches the invalid "
                  "value rather than silently accepting it. Reverting to the working address restores management "
                  "access.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("pa-lab-fw01", 13, 700, "#111827"),
        Line("hostname + mgmt IP 10.10.10.5/24", 10.5, 400, "#374151"),
        Line("commit: successful", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Role-based admin: labeng", 12.5, 700, "#111827"),
        Line("SSH reachable at 10.10.10.5", 10.5, 700, "#14532d"),
        Line("replaces daily use of admin", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("mgmt IP → 10.10.10.255", 10.5, 700, "#7f1d1d"),
        Line("(broadcast-adjacent, invalid)", 10.5, 700, "#7f1d1d"),
        Line("commit rejected / unreachable", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("candidate-configuration validation catches the invalid address before or immediately after commit —", 11.5, 400, "#374151"),
        Line("reverting to 10.10.10.5 and committing again restores working management access.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Committed baseline config"), ("alt", "Working admin access"), ("warn", "Rejected invalid commit")])
    c.save(f"{OUT}/chapter-01-panos-first-touch-commit-validation-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: Content Updates Require an Explicit Download Before Install",
        subtitle="Installing a version not yet on the firewall fails outright — download and install are two distinct actions, never one",
        svg_title="Chapter 2 lab flow: license activation and dynamic content updates, tested against installing a content version that was never downloaded",
        svg_desc="An auth code activates a subscription license, confirmed by its expiration date appearing in "
                  "request license info. A content upgrade check lists available Applications and Threats "
                  "versions. As a negative test, installing a specific content version that has not been "
                  "downloaded to this system fails, with PAN-OS reporting the package is not present locally — "
                  "confirming download and install are two distinct, sequential actions rather than one combined "
                  "operation. Downloading and then installing the latest content correctly updates app-version, "
                  "and a weekly automatic download-and-install schedule is committed for ongoing currency.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Auth code activation", 12.5, 700, "#111827"),
        Line("subscription license confirmed", 10.5, 400, "#374151"),
        Line("expiration date appears", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("install version <not downloaded>", 10.5, 700, "#7f1d1d"),
        Line("→ package not present locally", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("download latest → install latest", 12, 700, "#111827"),
        Line("app-version updates correctly", 10.5, 700, "#14532d"),
        Line("weekly auto schedule committed", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("download then install — never a single combined action — is the dependency the negative test proves;", 11.5, 400, "#374151"),
        Line("the weekly schedule automates both steps together going forward.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "License activation"), ("alt", "Correct download-then-install"), ("warn", "Install-without-download (rejected)")])
    c.save(f"{OUT}/chapter-02-content-update-download-install-flow.svg")


def ch03():
    c = Canvas(960, 580,
        title="Chapter 3 Hands-On Lab: A Bootstrap ISO That Configures VM-Series With Zero Manual Console Entry",
        subtitle="A correct init-cfg.txt reaches a licensed, networked state automatically; a malformed netmask value is rejected, not silently accepted",
        svg_title="Chapter 3 lab flow: a VM-Series bootstrap package validated end to end, then a deliberately malformed init-cfg.txt tested against bootstrap validation",
        svg_desc="A bootstrap ISO built from init-cfg.txt (static IP 10.10.10.15, hostname pa-vmseries-lab01) is "
                  "attached to a freshly deployed VM-Series instance; show system bootstrap reports SUCCESS and "
                  "the hostname/management IP match init-cfg.txt exactly, with no manual configuration entered at "
                  "the console. SSH from the workstation confirms reachability. As a negative test, "
                  "init-cfg.txt is edited to introduce a malformed netmask value and rebuilt into a second ISO "
                  "attached to a new instance; the instance either fails bootstrap validation outright or falls "
                  "back to its factory default management IP, confirming PAN-OS does not silently accept invalid "
                  "bootstrap values.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("bootstrap ISO (valid)", 12.5, 700, "#111827"),
        Line("init-cfg.txt: static IP,", 10.5, 400, "#374151"),
        Line("hostname, correct netmask", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 260, 120, "alt", [
        Line("VM-Series instance", 12.5, 700, "#111827"),
        Line("Bootstrap: SUCCESS", 10.5, 700, "#14532d"),
        Line("SSH reachable, zero manual config", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("malformed netmask in", 10.5, 700, "#7f1d1d"),
        Line("init-cfg.txt", 10.5, 700, "#7f1d1d"),
        Line("→ FAILURE or factory-default IP", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(660, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("bootstrap validation catches the malformed field rather than silently applying a broken network config —", 11.5, 400, "#374151"),
        Line("the bootstrap log identifies the specific rejected field before the file is corrected and redeployed.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Bootstrap package"), ("alt", "Successful zero-touch bootstrap"), ("warn", "Malformed field (rejected)")])
    c.save(f"{OUT}/chapter-03-vmseries-bootstrap-validation-flow.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: Outbound NAT Confirmed, an Unpublished Service Confirmed Unreachable, and a Clean HA Failover",
        subtitle="A destination NAT lookup with no matching rule proves inbound exposure is intentional, not implicit",
        svg_title="Chapter 4 lab topology: Layer 3 interfaces, source NAT, and an active/passive HA pair, tested against an unpublished destination NAT lookup and a failover",
        svg_desc="ethernet1/1 (untrust, 203.0.113.2/30) and ethernet1/2 (trust, 10.10.20.1/24) route a default "
                  "route via 203.0.113.1; a dynamic-IP-and-port source NAT rule translates outbound sessions to "
                  "ethernet1/1's address, confirmed in the session table. As a negative test, a NAT policy lookup "
                  "for an inbound destination NAT rule that does not yet exist reports no matching rule, "
                  "confirming an unpublished internal service is not reachable inbound. Two firewalls in "
                  "active/passive HA show one active and one passive with both HA links Running; disabling the "
                  "active member's monitored uplink causes the peer to transition to active within the "
                  "failure-detection interval while the trust-zone test host stays reachable throughout, and "
                  "restoring the interface returns the original member to a synchronized state.")
    c.node_box(60, 130, 220, 110, "mgmt", [
        Line("eth1/2 (trust)", 12.5, 700, "#111827"),
        Line("10.10.20.1/24", 10.5, 400, "#374151"),
        Line("DIPP source NAT → eth1/1", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 220, 110, "alt", [
        Line("eth1/1 (untrust)", 12.5, 700, "#111827"),
        Line("203.0.113.2/30", 10.5, 400, "#374151"),
        Line("default route via .1", 10.5, 700, "#14532d"),
    ])
    c.connector(280, 185, 360, 185, "mgmt", label="outbound, NAT'd")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("test nat-policy-match for", 10.5, 700, "#7f1d1d"),
        Line("nonexistent dest-NAT rule", 10.5, 700, "#7f1d1d"),
        Line("→ no matching rule", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(580, 185, 700, 185, "warn")
    c.node_box(60, 300, 260, 130, "mgmt", [
        Line("pa-fw01 (active)", 12.5, 700, "#111827"),
        Line("uplink disabled (negative test)", 10.5, 700, "#7f1d1d"),
        Line("→ peer takes over", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(400, 300, 260, 130, "alt", [
        Line("pa-fw01-b (was passive)", 12.5, 700, "#111827"),
        Line("→ becomes active within", 10.5, 700, "#14532d"),
        Line("the detection interval", 10.5, 400, "#374151"),
    ])
    c.connector(320, 365, 400, 365, "warn", label="HA1/HA2 failover")
    c.node_box(700, 300, 220, 130, "neutral", [
        Line("Trust-zone test host", 12, 700, "#111827"),
        Line("stays reachable throughout", 10.5, 700, "#1d4ed8"),
        Line("the failover", 10.5, 400, "#374151"),
    ])
    c.legend(60, 470, [("mgmt", "Trust-side / active member"), ("alt", "Untrust-side / failover target"), ("warn", "Negative test / failed uplink")])
    c.save(f"{OUT}/chapter-04-nat-ha-failover-topology.svg")


def ch05():
    c = Canvas(960, 640,
        title="Chapter 5 Hands-On Lab: An App-ID Rule That Doesn't Implicitly Permit Unrelated Applications",
        subtitle="A scoped web/SSL/DNS rule matches exactly the intended traffic and blocks bittorrent by default; a financial-services site skips decryption",
        svg_title="Chapter 5 lab flow: an App-ID security policy with an attached inspection profile, validated for scope and paired with a category-excluded decryption rule",
        svg_desc="Allow-Outbound-Web-Scoped (web-browsing, ssl, dns only, with the Lab-Inspection profile group "
                  "attached) matches a simulated SSL session from the trust zone, confirmed by "
                  "test security-policy-match. As a negative test, the same lookup for a bittorrent application "
                  "matches no rule but the default deny, confirming the scoped rule does not implicitly permit "
                  "unrelated applications. A decryption rule pair — decrypt everything except financial-services, "
                  "with the exclusion ordered first — is validated by browsing to a non-excluded site (decrypted, "
                  "logged) and a financial-services site (not decrypted, no certificate warning, logged as "
                  "no-decrypt).")
    c.node_box(60, 130, 260, 110, "alt", [
        Line("Allow-Outbound-Web-Scoped", 12.5, 700, "#111827"),
        Line("web-browsing, ssl, dns +", 10.5, 400, "#374151"),
        Line("Lab-Inspection profile group", 10.5, 700, "#14532d"),
    ])
    c.node_box(360, 130, 240, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("test: application bittorrent", 10.5, 700, "#7f1d1d"),
        Line("→ no rule match (default deny)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 185, 360, 185, "warn")
    c.node_box(660, 130, 260, 110, "mgmt", [
        Line("Decrypt-Exclude-Financial", 12, 700, "#111827"),
        Line("(ordered first) → no-decrypt", 10.5, 700, "#1d4ed8"),
        Line("Decrypt-Outbound-Lab → decrypt", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 300, 400, 100, "alt", [
        Line("Non-excluded HTTPS site", 12, 700, "#111827"),
        Line("decrypted, inspected", 10.5, 700, "#14532d"),
        Line("logged in Monitor > Logs > Decryption", 10.5, 400, "#374151"),
    ])
    c.node_box(500, 300, 400, 100, "mgmt", [
        Line("financial-services category site", 12, 700, "#111827"),
        Line("NOT decrypted", 10.5, 700, "#1d4ed8"),
        Line("no cert warning, logged no-decrypt", 10.5, 400, "#374151"),
    ])
    c.legend(60, 440, [("alt", "Scoped, correctly matching"), ("warn", "Correctly non-matching"), ("mgmt", "Decryption rule outcome")])
    c.save(f"{OUT}/chapter-05-app-id-decryption-scope-flow.svg")


def ch06():
    c = Canvas(960, 640,
        title="Chapter 6 Hands-On Lab: A Local Firewall Rule That Persists Independently of Panorama's Push",
        subtitle="Panorama pushes a Shared deny and a device-group allow rule cleanly; a rule added directly on the firewall survives alongside them, demonstrating drift risk",
        svg_title="Chapter 6 lab topology: a two-level Panorama device-group hierarchy with a template stack pushed to a managed firewall, tested against local configuration drift",
        svg_desc="Panorama's Global-Baseline device group holds a Shared pre-rule (Block-Known-Malicious); its "
                  "Branch-Offices child holds a device-group-scoped allow rule (Allow-Branch-Web). A template "
                  "stack supplies DNS and, once configured, points the firewall's panorama-server setting back at "
                  "Panorama for log forwarding. Pushing both the device group and template stack to an onboarded "
                  "firewall causes show rulebase security rules to list both pushed rules, and test traffic "
                  "appears in Panorama's log viewer. As a negative test, a rule is added directly on the managed "
                  "firewall's own CLI, not through Panorama; show config running on the firewall shows this local "
                  "rule persisting alongside the Panorama-pushed rules, confirming that uncontrolled local changes "
                  "are exactly how policy drift enters a Panorama-managed fleet.")
    c.node_box(60, 120, 260, 110, "mgmt", [
        Line("Panorama: Global-Baseline", 12.5, 700, "#111827"),
        Line("Shared pre-rule:", 10.5, 400, "#374151"),
        Line("Block-Known-Malicious", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(360, 120, 260, 110, "alt", [
        Line("Branch-Offices (child DG)", 12.5, 700, "#111827"),
        Line("Allow-Branch-Web", 10.5, 700, "#14532d"),
        Line("+ Branch-Stack template", 10.5, 400, "#374151"),
    ])
    c.connector(320, 175, 360, 175, "mgmt")
    c.node_box(680, 120, 240, 110, "alt", [
        Line("Onboarded firewall", 12.5, 700, "#111827"),
        Line("both rules pushed and present", 10.5, 700, "#14532d"),
        Line("traffic logs reach Panorama", 10.5, 400, "#374151"),
    ])
    c.connector(620, 175, 680, 175, "alt", label="batch-push")
    c.node_box(60, 300, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Local-Test-Rule added directly on the managed firewall's CLI, bypassing Panorama entirely", 11, 400, "#7f1d1d"),
        Line("show config running shows it persisting alongside the Panorama-pushed rules — not overwritten, not rejected", 11, 400, "#7f1d1d"),
        Line("confirms uncontrolled local changes are how policy drift enters a Panorama-managed fleet", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 470, [("mgmt", "Shared / global policy"), ("alt", "Device-group / pushed policy"), ("warn", "Local drift (negative test)")])
    c.save(f"{OUT}/chapter-06-panorama-device-group-drift-topology.svg")


def ch07():
    c = Canvas(960, 620,
        title="Chapter 7 Hands-On Lab: The API Enforces Key Validation Rather Than Falling Back to a Default",
        subtitle="A suspended HA member keeps traffic flowing on its peer; a deliberately invalid API key is rejected, not silently accepted",
        svg_title="Chapter 7 lab flow: an HA-aware upgrade sequence, packet-diag capture, and XML/REST API operations, tested against an invalid API key",
        svg_desc="Suspending the passive HA member for upgrade preparation leaves the active peer serving traffic "
                  "uninterrupted, confirmed by show high-availability state; returning the member to functional "
                  "state completes the sequence. A filtered packet-diag capture confirms matching packets for a "
                  "specific test flow. An XML API keygen request retrieves system info matching the CLI's output, "
                  "and a REST API POST creates an address object confirmed at the CLI. As a negative test, the "
                  "same system info request is repeated with a deliberately invalid API key; the API returns an "
                  "authentication failure rather than falling back to an unauthenticated default, confirming key "
                  "validation is actually enforced.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("Passive HA member", 12.5, 700, "#111827"),
        Line("suspended for upgrade prep", 10.5, 400, "#374151"),
        Line("peer stays active, uninterrupted", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("XML/REST API (valid key)", 12.5, 700, "#111827"),
        Line("system info retrieved", 10.5, 400, "#374151"),
        Line("address object created", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("same request, invalid key", 10.5, 700, "#7f1d1d"),
        Line("→ authentication failure", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("no unauthenticated fallback exists — an invalid key is rejected outright, the same enforcement", 11.5, 400, "#374151"),
        Line("boundary that protects the CLI, applied consistently to the XML and REST APIs.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "HA-aware upgrade prep"), ("alt", "Authenticated API operations"), ("warn", "Rejected invalid credential")])
    c.save(f"{OUT}/chapter-07-ha-upgrade-api-key-validation-flow.svg")


def ch08():
    c = Canvas(960, 660,
        title="Chapter 8 Hands-On Lab: The Capstone — a Shared Pre-Rule That a Local Override Attempt Cannot Beat",
        subtitle="Every layer — provisioning, governance, HA, policy, decryption, logging, automation — is validated together, then a local rule tries and fails to bypass the global block",
        svg_title="Chapter 8 lab topology: the full Panorama-governed capstone — data-center HA pair and branch firewall — validated end to end, tested against a local policy-override attempt",
        svg_desc="A data-center HA pair and a branch firewall bootstrap into Panorama-defined device groups and "
                  "template stacks under a Global-Baseline hierarchy; HA reports one active and one passive "
                  "member. A Shared pre-rule blocks known-malicious categories globally, while device-group-"
                  "scoped allow rules with attached inspection profiles permit legitimate web traffic at each "
                  "site; a phased decryption rule pair excludes financial-services; centralized logging confirms "
                  "traffic from all three firewalls in Panorama's log viewer; and a bulk API script creates "
                  "address objects on the branch firewall. As a negative test, a local rule added directly on the "
                  "branch firewall attempts to permit the malware category the Shared pre-rule blocks; "
                  "test security-policy-match still reports Block-Known-Malicious as the matching rule, not the "
                  "local override, confirming Shared pre-rules evaluate ahead of local firewall rules and cannot "
                  "be bypassed by local configuration.")
    c.node_box(60, 120, 260, 110, "mgmt", [
        Line("Panorama: Global-Baseline", 12.5, 700, "#111827"),
        Line("Shared pre-rule:", 10.5, 400, "#374151"),
        Line("Block-Known-Malicious", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(360, 120, 260, 110, "alt", [
        Line("DataCenter (HA pair) +", 12.5, 700, "#111827"),
        Line("Branch-Offices", 10.5, 400, "#374151"),
        Line("scoped allow rules, decryption", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 175, 360, 175, "mgmt")
    c.node_box(680, 120, 240, 110, "neutral", [
        Line("Logging + automation", 12.5, 700, "#111827"),
        Line("all 3 firewalls' traffic logged", 10.5, 400, "#374151"),
        Line("bulk API address objects on branch", 10.5, 400, "#374151"),
    ])
    c.connector(620, 175, 680, 175, "alt")
    c.node_box(60, 300, 860, 150, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Local-Override-Attempt added directly on the branch firewall's CLI, permitting the malware category", 11, 400, "#7f1d1d"),
        Line("test security-policy-match for matching malware-category traffic still reports Block-Known-Malicious", 11, 400, "#7f1d1d"),
        Line("as the matching rule, not Local-Override-Attempt", 11, 400, "#7f1d1d"),
        Line("Shared pre-rules evaluate ahead of local firewall rules and cannot be bypassed by local configuration", 11, 400, "#14532d"),
    ])
    c.legend(60, 480, [("mgmt", "Global, non-negotiable policy"), ("alt", "Site-scoped policy"), ("warn", "Local override attempt (fails)")])
    c.save(f"{OUT}/chapter-08-capstone-panorama-prerule-override-topology.svg")


def ch09():
    c = Canvas(960, 620,
        title="Chapter 9 Hands-On Lab: A Checkov Scan That Must Fail Before It Can Prove Remediation Works",
        subtitle="An open-SSH security group fails CKV_AWS_24 on the first scan by design; a clean scan against this file would mean Checkov itself was broken",
        svg_title="Chapter 9 lab flow: a Terraform configuration scanned with Checkov, deliberately failing first, then remediated and gated in CI/CD",
        svg_desc="A sample Terraform file with an unrestricted SSH ingress rule and an unencrypted S3 bucket is "
                  "scanned with Checkov; it reports at least one FAILED check (CKV_AWS_24) for the open ingress "
                  "rule. This failure is the expected, correct behavior for a known-bad configuration — a scan "
                  "reporting no findings against this specific file would indicate a broken Checkov installation, "
                  "not a secure configuration. Narrowing the security group's CIDR block to a lab subnet and "
                  "re-scanning shows CKV_AWS_24 now PASSED; a documented suppression is added for the remaining "
                  "S3 finding. Pushed to a CI/CD pipeline, the unremediated branch fails the check and the "
                  "remediated branch passes.")
    c.node_box(60, 130, 260, 110, "warn", [
        Line("Sample Terraform (as-is)", 12.5, 700, "#111827"),
        Line("SSH ingress: 0.0.0.0/0", 10.5, 700, "#7f1d1d"),
        Line("checkov: CKV_AWS_24 FAILED", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(400, 130, 240, 110, "alt", [
        Line("Remediated", 12.5, 700, "#111827"),
        Line("CIDR narrowed to 10.10.0.0/16", 10.5, 400, "#374151"),
        Line("checkov: CKV_AWS_24 PASSED", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 185, 400, 185, "warn")
    c.node_box(700, 130, 220, 110, "neutral", [
        Line("CI/CD gate", 12, 700, "#111827"),
        Line("unremediated branch: fails", 10.5, 400, "#374151"),
        Line("remediated branch: passes", 10.5, 400, "#374151"),
    ])
    c.connector(640, 185, 700, 185, "alt")
    c.node_box(60, 300, 860, 100, "neutral", [
        Line("the initial FAILED result is the expected, correct behavior for a deliberately insecure sample —", 11.5, 400, "#374151"),
        Line("a scan reporting zero findings against this exact file would mean Checkov itself was broken, not that the code was secure.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 440, [("warn", "Deliberately failing (as designed)"), ("alt", "Remediated, passing"), ("neutral", "Pipeline gate outcome")])
    c.save(f"{OUT}/chapter-09-checkov-iac-scan-remediation-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
