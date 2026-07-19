import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-19-fortinet-network-security"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Hands-On Lab: MFA That Actually Blocks a Password-Only Sign-In",
        subtitle="Rotating a reused password and enabling authenticator MFA is confirmed, not assumed, by trying to sign in with only the old factor",
        svg_title="Chapter 1 lab flow: a personal security hygiene audit culminating in an MFA enforcement check, with a structural phishing-message analysis",
        svg_desc="A password manager's breach report identifies reused or weak credentials; the highest-value "
                  "reused account (typically primary email) gets a unique generated password and authenticator-"
                  "app MFA, with recovery codes stored securely. As a negative test, signing in from a fresh "
                  "private browser session using only the password is rejected or paused pending the second "
                  "factor, confirming MFA is actually enforced rather than merely available but optional. "
                  "Separately, a sample phishing message is analyzed without clicking any link — sender domain "
                  "versus display name, link-destination mismatch, and the social engineering lever used — "
                  "producing a written analysis with at least three structural indicators.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Password rotation + MFA setup", 12.5, 700, "#111827"),
        Line("highest-value reused account", 10.5, 400, "#374151"),
        Line("authenticator-app MFA enabled", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("password-only sign-in attempt", 10.5, 700, "#7f1d1d"),
        Line("(fresh private session)", 10.5, 400, "#7f1d1d"),
        Line("→ rejected / paused for 2nd factor", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 100, "neutral", [
        Line("MFA is confirmed enforced, not merely configured — separately, a sample phishing message is analyzed", 11.5, 400, "#374151"),
        Line("for sender-domain mismatch, link mismatch, and social-engineering lever without clicking anything.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Hygiene improvement"), ("warn", "Enforcement confirmed")])
    c.save(f"{OUT}/chapter-01-security-hygiene-mfa-enforcement-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A Coverage Claim an Independent Reviewer Can Catch From the Notes Alone",
        subtitle="A technology-to-risk inventory maps real gaps to a current attack technique; a false coverage claim is deliberately planted and then caught",
        svg_title="Chapter 2 lab flow: a technology-to-risk inventory validated against public threat intelligence, tested against a deliberately unsupported coverage claim",
        svg_desc="A technology-to-risk inventory for a scenario organization marks each security technology "
                  "category deployed, partial, or not deployed, with each gap's uncovered kill-chain stage "
                  "identified and mapped against one current, real attack technique from public threat "
                  "intelligence. As a negative test, the web application firewall category is deliberately marked "
                  "'deployed: true' with no corresponding enforcement point in front of the scenario's actual "
                  "public-cloud application; re-reading the inventory as an independent reviewer, the unsupported "
                  "claim is identifiable from the coverage notes alone — proving coverage notes must describe "
                  "actual enforcement, not just product ownership. The entry is then corrected to reflect the "
                  "real gap.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("security-technology-inventory.yaml", 12, 700, "#111827"),
        Line("8+ categories, deployment status", 10.5, 400, "#374151"),
        Line("gaps mapped to a real threat technique", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("WAF marked \"deployed: true\"", 10.5, 700, "#7f1d1d"),
        Line("with no real enforcement point", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 100, "neutral", [
        Line("re-reading as an independent reviewer catches the unsupported claim from the coverage notes alone —", 11.5, 400, "#374151"),
        Line("notes must describe actual enforcement, not merely which product is nominally owned; the entry is then corrected.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Validated inventory"), ("warn", "Unsupported claim (caught)")])
    c.save(f"{OUT}/chapter-02-technology-risk-inventory-flow.svg")


def ch03():
    c = Canvas(960, 600,
        title="Chapter 3 Hands-On Lab: A Least-Privilege Operator Account That Reads Everything and Writes Nothing",
        subtitle="operator1's status commands succeed while a configuration write is denied outright in the same session",
        svg_title="Chapter 3 lab flow: a factory-default FortiGate explored read-only as an operator, then a least-privilege account tested against a configuration write attempt",
        svg_desc="A factory-default FortiGate is explored read-only: status commands, Security Fabric topology "
                  "(showing the single local device), and Security Rating (a low initial score with findings tied "
                  "to the unlicensed, unhardened state). A least-privilege operator1 account and accprofile are "
                  "created and logged into. As a negative test, operator1 attempts a configuration write (editing "
                  "an interface); FortiOS denies it with a permission error, while get system status and other "
                  "read commands continue to succeed in the same session — confirming the profile's read/write "
                  "boundary is enforced precisely. The lab account and profile are removed afterward, returning "
                  "the device to a clean baseline.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("Factory-default FortiGate", 12.5, 700, "#111827"),
        Line("read-only status + Security Rating", 10.5, 400, "#374151"),
        Line("(low score, unhardened findings)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 110, "alt", [
        Line("operator1 (least-privilege)", 12.5, 700, "#111827"),
        Line("read commands succeed normally", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 195, 400, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("operator1: config write attempt", 10.5, 700, "#7f1d1d"),
        Line("→ permission error", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 195, 700, 195, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("the write is denied while read commands keep succeeding in the exact same session — the profile's", 11.5, 400, "#374151"),
        Line("read/write boundary is precise, not an all-or-nothing lockout.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Unhardened baseline"), ("alt", "Permitted read access"), ("warn", "Denied write attempt")])
    c.save(f"{OUT}/chapter-03-fortigate-operator-least-privilege-flow.svg")


def ch04():
    c = Canvas(960, 580,
        title="Chapter 4 Hands-On Lab: trusthost Enforcement Confirmed From Outside the Permitted Subnet",
        subtitle="Management access works normally from the lab subnet and is refused entirely from anywhere else",
        svg_title="Chapter 4 lab flow: FortiGate first deployment and hardening, tested against a management-access attempt from outside the trusted subnet",
        svg_desc="FGT-LAB-01 receives hostname, DNS, NTP, FortiCare licensing, a hardened management interface, "
                  "a strong password policy, and trusthost1 restricted to the lab management subnet. As a "
                  "negative test, a workstation on a different subnet than trusthost1 attempts to reach the GUI "
                  "or SSH; the connection is refused or times out, confirming trusthost enforcement is actively "
                  "restricting management access rather than merely being configured. FortiToken (or an email-"
                  "based lab substitute) is then enabled on the admin account, and final validation confirms "
                  "hostname, licensing, hardened admin configuration, and an enabled password policy all together.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("FGT-LAB-01 hardening", 12.5, 700, "#111827"),
        Line("hostname, DNS/NTP, licensing", 10.5, 400, "#374151"),
        Line("trusthost1: lab mgmt subnet only", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Workstation on trusthost1 subnet", 12, 700, "#111827"),
        Line("GUI/SSH reachable normally", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("workstation on a different subnet", 10.5, 700, "#7f1d1d"),
        Line("→ refused / timeout", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("trusthost enforcement blocks management access from any subnet not explicitly permitted, confirmed", 11.5, 400, "#374151"),
        Line("by an actual connection attempt rather than trusting the configuration alone.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Hardening baseline"), ("alt", "Permitted management access"), ("warn", "Denied out-of-subnet access")])
    c.save(f"{OUT}/chapter-04-fortigate-trusthost-hardening-flow.svg")


def ch05():
    c = Canvas(960, 660,
        title="Chapter 5 Hands-On Lab: FGCP HA Split-Brain Reproduced, Then Automatically Resolved",
        subtitle="Cutting both heartbeat links at once lets each member claim primary; reconnecting them resynchronizes to a single primary again",
        svg_title="Chapter 5 lab topology: interfaces, multi-VDOM routing, and a two-member FGCP HA cluster, tested against a dual-heartbeat-link failure",
        svg_desc="FGT-LAB-01 and FGT-LAB-02 form an FGCP HA cluster (priority 200 and 100) with heartbeat "
                  "interfaces port4 and port5 connected between them; within minutes the cluster shows FGT-LAB-01 "
                  "as primary and FGT-LAB-02 as secondary, with configuration changes synchronizing automatically "
                  "between them. Separately, multi-VDOM mode connects VDOM-CORP and VDOM-DMZ over an inter-VDOM "
                  "link with confirmed connectivity. As a negative test, both heartbeat interfaces on the "
                  "secondary are disconnected simultaneously; each member may independently report itself as "
                  "primary — a split-brain condition — until the heartbeat links are reconnected, at which point "
                  "the cluster automatically resynchronizes to a single primary within a short interval.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("FGT-LAB-01 (priority 200)", 12.5, 700, "#111827"),
        Line("primary, HA cluster healthy", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(360, 130, 240, 110, "alt", [
        Line("FGT-LAB-02 (priority 100)", 12.5, 700, "#111827"),
        Line("secondary, config synced", 10.5, 700, "#14532d"),
        Line("(negative test: heartbeat cut)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 185, 360, 185, "mgmt", label="heartbeat port4/port5")
    c.node_box(680, 130, 240, 110, "neutral", [
        Line("VDOM-CORP ⇄ VDOM-DMZ", 12.5, 700, "#111827"),
        Line("inter-VDOM link, confirmed", 10.5, 400, "#374151"),
        Line("connectivity", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 300, 860, 150, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("both heartbeat interfaces on FGT-LAB-02 disconnected simultaneously", 11, 400, "#7f1d1d"),
        Line("each member may independently report itself as primary — split-brain, since neither can see the other", 11, 400, "#7f1d1d"),
        Line("heartbeat links reconnected → cluster automatically resynchronizes to a single primary within a short", 11, 400, "#14532d"),
        Line("interval, demonstrating both the failure mode and FGCP's automatic recovery", 11, 400, "#14532d"),
    ])
    c.legend(60, 480, [("mgmt", "Primary member"), ("alt", "Secondary member"), ("neutral", "Independent VDOM routing")])
    c.save(f"{OUT}/chapter-05-fgcp-ha-split-brain-topology.svg")


def ch06():
    c = Canvas(960, 640,
        title="Chapter 6 Hands-On Lab: A Pre-Shared Key Mismatch That Fails Loudly, Not Silently",
        subtitle="The site-to-site tunnel establishes normally; a deliberately wrong PSK produces an explicit IKE authentication failure in debug output",
        svg_title="Chapter 6 lab flow: firewall policy, authentication, and site-to-site/SSL VPN configuration, tested against a deliberate pre-shared key mismatch",
        svg_desc="Outbound and inbound firewall policies complete the NAT design from the prior chapter, "
                  "confirmed by a translated source address in the session list. LDAP and local authentication "
                  "feed a VPN-Users group, and a site-to-site IPsec tunnel to a second FortiGate peer "
                  "establishes with confirmed phase1 and phase2 security associations. As a negative test, the "
                  "phase1-interface's pre-shared key is changed to an incorrect value on one side only, and the "
                  "tunnel is brought up again; IKE negotiation fails and debug output explicitly reports an "
                  "authentication/proposal failure, confirming the mismatch is detectable rather than failing "
                  "silently. Restoring the correct key re-establishes the tunnel. SSL VPN separately confirms a "
                  "connected session with the authenticated username and assigned tunnel IP.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("LAN-to-WAN-Outbound policy", 12.5, 700, "#111827"),
        Line("outbound NAT confirmed", 10.5, 700, "#1d4ed8"),
        Line("in session list", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "alt", [
        Line("to-Branch02 IPsec tunnel", 12.5, 700, "#111827"),
        Line("phase1 + phase2 SA established", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(680, 130, 240, 110, "mgmt", [
        Line("SSL VPN (VPN-Users)", 12, 700, "#111827"),
        Line("connected session, tunnel IP", 10.5, 400, "#374151"),
        Line("assigned from SSLVPN_TUNNEL_ADDR1", 10, 400, "#374151"),
    ])
    c.node_box(60, 300, 860, 140, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("psksecret on FGT-LAB-01's phase1-interface changed to an incorrect value (one side only)", 11, 400, "#7f1d1d"),
        Line("IKE negotiation fails; debug output explicitly reports an authentication/proposal failure —", 11, 400, "#7f1d1d"),
        Line("the mismatch is detectable, not silent", 11, 400, "#7f1d1d"),
        Line("correct key restored → tunnel re-establishes cleanly", 11, 400, "#14532d"),
    ])
    c.legend(60, 470, [("mgmt", "Policy / NAT layer"), ("alt", "Established VPN"), ("warn", "PSK mismatch (detected loudly)")])
    c.save(f"{OUT}/chapter-06-ipsec-psk-mismatch-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: SSL Deep Inspection Requires Real CA Trust Distribution, Not Just Policy Configuration",
        subtitle="EICAR and a blocked category are stopped before HTTPS inspection even starts; switching to deep inspection breaks trust until the CA is installed",
        svg_title="Chapter 7 lab flow: AV/IPS/web-filter/app-control profiles and SSL inspection validated against real test traffic, tested against a category-allow override",
        svg_desc="AV-Standard, IPS-Standard, WebFilter-Standard, and AppCtrl-Standard profiles attach to the "
                  "outbound policy with Certificate-Inspection SSL scanning. Downloading the EICAR test file is "
                  "blocked and logged against AV-Standard; browsing a filtered category is blocked and logged "
                  "against WebFilter-Standard. Switching to Full-Deep-Inspection without installing the "
                  "FortiGate's CA certificate produces a browser trust warning; installing the CA certificate in "
                  "the test client's trust store removes the warning and gives AV/IPS visibility into "
                  "HTTPS-delivered content they couldn't inspect before. As a negative test, an explicit allow "
                  "override is added to WebFilter-Standard for the previously blocked category; the site becomes "
                  "reachable, confirming the override mechanism works before it is reverted.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("EICAR download attempt", 12.5, 700, "#111827"),
        Line("blocked, AV-Standard logged", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(360, 130, 240, 110, "mgmt", [
        Line("Filtered category browse", 12.5, 700, "#111827"),
        Line("blocked, WebFilter-Standard logged", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(680, 130, 240, 110, "alt", [
        Line("Full-Deep-Inspection + CA trust", 12, 700, "#111827"),
        Line("cert warning until CA installed", 10.5, 400, "#374151"),
        Line("then AV/IPS see HTTPS content", 10.5, 700, "#14532d"),
    ])
    c.node_box(60, 300, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("WebFilter-Standard given an explicit allow override for the previously blocked category", 11, 400, "#7f1d1d"),
        Line("re-attempt of the browse test now succeeds — the site is reachable, confirming the exception", 11, 400, "#7f1d1d"),
        Line("mechanism took effect; the override is reverted immediately afterward", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 470, [("mgmt", "Blocked by default profile"), ("alt", "Deep inspection trust path"), ("warn", "Deliberate exception (reverted)")])
    c.save(f"{OUT}/chapter-07-security-profiles-ssl-inspection-flow.svg")


def ch08():
    c = Canvas(960, 620,
        title="Chapter 8 Hands-On Lab: SD-WAN Failover That Actually Reroutes Critical Traffic Automatically",
        subtitle="Bringing WAN1 down flips the SLA-based rule to WAN2 without any manual intervention, then reverts once WAN1 recovers",
        svg_title="Chapter 8 lab topology: an SD-WAN zone with SLA-based path selection, tested against a simulated WAN1 outage, plus FortiManager and REST API validation",
        svg_desc="An SD-WAN zone with two members (WAN1/port1 and WAN2/port6) and an Internet health-check "
                  "reports both members within SLA thresholds; the Critical-Apps rule currently selects WAN1. As "
                  "a negative test, port1 is administratively brought down to simulate a WAN1 outage; the "
                  "health-check reports member 1 as failed/out of SLA, and Critical-Apps automatically selects "
                  "WAN2 with no manual intervention. Restoring port1 returns path selection to WAN1 once its SLA "
                  "is met again. Separately, the device registers to FortiManager and appears managed and "
                  "in-sync, and a read-only-scoped API token successfully retrieves system status via the REST "
                  "API.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("SD-WAN zone: WAN1 + WAN2", 12.5, 700, "#111827"),
        Line("Internet health-check: both healthy", 10.5, 400, "#374151"),
        Line("Critical-Apps → currently WAN1", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(680, 130, 240, 110, "neutral", [
        Line("FortiManager + REST API", 12.5, 700, "#111827"),
        Line("device managed + in-sync", 10.5, 400, "#374151"),
        Line("read-only API returns status JSON", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 280, 400, 130, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("port1 (WAN1) brought down", 10.5, 700, "#7f1d1d"),
        Line("health-check: member 1 failed/out of SLA", 10.5, 700, "#7f1d1d"),
        Line("Critical-Apps auto-selects WAN2", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(500, 280, 400, 130, "alt", [
        Line("Recovery", 12, 700, "#111827"),
        Line("port1 restored, SLA met again", 10.5, 400, "#374151"),
        Line("Critical-Apps reverts to preferring", 10.5, 700, "#14532d"),
        Line("WAN1 automatically", 10.5, 700, "#14532d"),
    ])
    c.connector(460, 345, 500, 345, "alt")
    c.legend(60, 440, [("mgmt", "Healthy SD-WAN baseline"), ("neutral", "Central management/API"), ("warn", "Simulated outage + failover")])
    c.save(f"{OUT}/chapter-08-sdwan-failover-topology.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: The Capstone — a Deliberately Undocumented Fault, Traced Layer by Layer to Root Cause",
        subtitle="A restored baseline confirms recovery; a hidden misconfiguration is found methodically, not guessed, using the layered decision tree",
        svg_title="Chapter 9 lab flow: full end-to-end capstone validation with a configuration backup, tested against a deliberately undocumented misconfiguration and restored via backup",
        svg_desc="A full validation checklist across licensing, HA, routing, SD-WAN health, and VPN sessions is "
                  "recorded as a dated baseline, and a configuration backup exports to TFTP storage; a "
                  "Config-Change automation stitch confirms an automatic backup fires after a trivial, reversible "
                  "change. As a negative test, a specific, realistic misconfiguration is introduced without being "
                  "documented in advance — for example, an overlapping NAT pool range or a shadowing firewall "
                  "policy reorder — and the resulting symptom is worked through the layered troubleshooting "
                  "decision tree step by step until the actual root cause is correctly identified, without "
                  "guessing. The fault is corrected, the affected traffic flow confirmed restored, and the "
                  "original backup is restored as a final validation that recovery returns the device to the "
                  "exact baseline state.")
    c.node_box(60, 130, 260, 110, "mgmt", [
        Line("Full validation checklist", 12.5, 700, "#111827"),
        Line("licensing, HA, routes, SD-WAN,", 10.5, 400, "#374151"),
        Line("VPN — recorded as dated baseline", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 130, 240, 110, "alt", [
        Line("Config backup + auto-backup", 12.5, 700, "#111827"),
        Line("TFTP export confirmed", 10.5, 400, "#374151"),
        Line("Config-Change stitch fires", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 185, 400, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("undocumented misconfiguration", 10.5, 700, "#7f1d1d"),
        Line("introduced deliberately", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 185, 700, 185, "warn")
    c.node_box(60, 320, 860, 130, "warn", [
        Line("Layered Troubleshooting", 12.5, 700, "#7f1d1d"),
        Line("decision tree walked step by step, layer by layer, documenting what was checked and found at each step", 11, 400, "#7f1d1d"),
        Line("root cause correctly identified without guessing — misconfiguration corrected, traffic flow restored", 11, 400, "#7f1d1d"),
    ])
    c.node_box(60, 470, 860, 90, "alt", [
        Line("Final validation: the step-2 backup is restored, and the device returns to the exact baseline state —", 11.5, 700, "#14532d"),
        Line("recovery is confirmed by re-running the same validation checklist, not merely assumed.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 600, [("mgmt", "Baseline + backup"), ("warn", "Hidden fault + diagnosis"), ("alt", "Confirmed restore")])
    c.save(f"{OUT}/chapter-09-capstone-troubleshooting-restore-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
