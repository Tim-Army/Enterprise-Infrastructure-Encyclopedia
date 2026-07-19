import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-03-cisco-enterprise-networking"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Hands-On Lab: Catalyst 9000 Bring-Up to a Hardened Install-Mode Device",
        subtitle="Bundle mode → install mode → hardened CLI/SSH → management VLAN → Smart Licensing",
        svg_title="Chapter 1 lab flow: bringing a Catalyst 9000 switch from factory defaults to a hardened, licensed device",
        svg_desc="A Catalyst 9000 switch starting in bundle mode is converted to install mode and reloaded, then "
                  "hardened with a hostname, local credentials, and SSH/console/vty lockdown as CAMPUS-ACCESS-01. "
                  "VLAN 99 and its SVI (10.10.99.10/24) are created and confirmed up with a successful gateway "
                  "ping, then Smart Licensing is registered against CSSM. As a negative test, an SSH login with an "
                  "intentionally wrong password is rejected after three attempts and the failure is confirmed in "
                  "the device's logging output.")
    c.node_box(40, 120, 200, 90, "neutral", [
        Line("Switch (bundle mode)", 12.5, 700, "#111827"),
        Line("factory defaults", 10.5, 400, "#374151"),
    ])
    c.connector(240, 165, 320, 165, "mgmt", label="install_mode + reload")
    c.node_box(320, 120, 220, 90, "mgmt", [
        Line("CAMPUS-ACCESS-01", 12.5, 700, "#111827"),
        Line("install mode, hardened", 10.5, 400, "#374151"),
        Line("SSH + console/vty lockdown", 10, 400, "#6b7280"),
    ])
    c.connector(430, 210, 430, 260, "mgmt", label="VLAN 99 + SVI")
    c.node_box(320, 260, 220, 90, "mgmt", [
        Line("Vlan99 (mgmt SVI)", 12.5, 700, "#111827"),
        Line("10.10.99.10/24", 11.5, 700, "#1d4ed8"),
        Line("up/up, gateway ping OK", 10, 400, "#374151"),
    ])
    c.connector(540, 305, 660, 305, "alt", label="license smart trust idtoken")
    c.node_box(660, 260, 260, 90, "alt", [
        Line("Smart Licensing (CSSM)", 12.5, 700, "#111827"),
        Line("transport: smart", 10.5, 400, "#374151"),
        Line("last report: successful", 10, 400, "#14532d"),
    ])
    c.node_box(40, 400, 400, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("ssh netadmin@10.10.99.10 with an intentionally wrong password", 11, 400, "#7f1d1d"),
        Line("rejected after 3 attempts; session closed", 11, 400, "#7f1d1d"),
        Line("show logging | include Login confirms the failed attempt", 11, 400, "#7f1d1d"),
    ])
    c.legend(40, 550, [("mgmt", "Bring-up / hardening step"), ("alt", "Licensing step")])
    c.save(f"{OUT}/chapter-01-catalyst-9000-bringup-flow.svg")


def ch02():
    c = Canvas(960, 660,
        title="Chapter 2 Hands-On Lab: Distribution HSRP Pair with LACP-Trunked Access Switch",
        subtitle="DIST-01 active for VLAN 10 / standby for VLAN 20, DIST-02 the inverse, with BPDU Guard on the access edge",
        svg_title="Chapter 2 lab topology: an HSRP distribution pair connected to an access switch by two LACP EtherChannel trunks",
        svg_desc="DIST-01 and DIST-02 form an HSRP pair across VLANs 10 and 20, with active/standby roles reversed "
                  "per VLAN to spread gateway load: DIST-01 is Active for VLAN 10 and Standby for VLAN 20; DIST-02 "
                  "is the inverse. Both connect to ACCESS-01 by independent two-member LACP EtherChannel trunks "
                  "carrying VLANs 10, 20, and 99 with native VLAN 999; DIST-01 is Rapid PVST+ root for all three "
                  "VLANs. ACCESS-01's spare access port runs BPDU Guard and PortFast. As a negative test, attaching "
                  "an unauthorized switch that emits BPDUs to that port causes it to transition to err-disabled, "
                  "logging a SPANTREE-2-BLOCK_BPDUGUARD event.")
    c.node_box(80, 140, 220, 120, "mgmt", [
        Line("DIST-01", 14, 700, "#111827"),
        Line("VLAN 10: Active (110)", 11, 700, "#1d4ed8"),
        Line("VLAN 20: Standby (100)", 11, 400, "#374151"),
        Line("STP root: VLANs 10/20/99", 10, 400, "#6b7280"),
    ])
    c.node_box(660, 140, 220, 120, "alt", [
        Line("DIST-02", 14, 700, "#111827"),
        Line("VLAN 10: Standby (100)", 11, 400, "#374151"),
        Line("VLAN 20: Active (110)", 11, 700, "#14532d"),
    ])
    c.node_box(370, 320, 220, 130, "neutral", [
        Line("ACCESS-01", 14, 700, "#111827"),
        Line("2x LACP EtherChannel trunks", 10.5, 400, "#374151"),
        Line("VLANs 10, 20, 99 · native 999", 10.5, 400, "#374151"),
        Line("Gi1/0/10: PortFast + BPDU Guard", 10, 400, "#6b7280"),
    ])
    c.connector(190, 260, 430, 320, "mgmt", label="LACP trunk (VLAN 10/20/99)")
    c.connector(770, 260, 550, 320, "mgmt", label="LACP trunk (VLAN 10/20/99)")
    c.node_box(370, 500, 220, 100, "warn", [
        Line("Negative Test", 11.5, 700, "#7f1d1d"),
        Line("unauthorized switch on Gi1/0/10", 10.5, 400, "#7f1d1d"),
        Line("emits BPDUs → err-disabled", 10.5, 400, "#7f1d1d"),
        Line("%SPANTREE-2-BLOCK_BPDUGUARD", 10, 700, "#7f1d1d"),
    ])
    c.connector(480, 450, 480, 500, "warn")
    c.legend(80, 610, [("mgmt", "VLAN 10 active path"), ("alt", "VLAN 20 active path"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-02-hsrp-distribution-lacp-topology.svg")


def ch03():
    c = Canvas(960, 660,
        title="Chapter 3 Hands-On Lab: Two-Area OSPF, EIGRP Redistribution, and Tracked PBR",
        subtitle="CORE-01 redistributes between OSPF Area 0/10 and EIGRP AS 100, then policy-routes GUEST VRF traffic",
        svg_title="Chapter 3 lab topology: OSPF and EIGRP domains joined by mutual redistribution on an ASBR, plus IP SLA-tracked PBR",
        svg_desc="CORE-01 runs OSPF Area 0 toward DIST-01 (Area 10, totally stubby) and EIGRP AS 100 toward "
                  "BRANCH-01, mutually redistributing routes between the two protocols with route tags. DIST-01 "
                  "learns BRANCH-01's subnet as an OSPF external route; BRANCH-01 learns DIST-01's subnet as an "
                  "EIGRP external route. Separately, CORE-01 policy-routes the GUEST VRF (10.30.0.0/24) to an "
                  "alternate next hop using IP SLA object 10, tracking a simulated exit path. As a negative test, "
                  "shutting down the tracked next hop transitions track 10 to Down, and PBR falls back to normal "
                  "destination-based routing instead of black-holing traffic.")
    c.node_box(370, 140, 220, 110, "alt", [
        Line("CORE-01", 14, 700, "#111827"),
        Line("Area 0 / EIGRP AS 100 ASBR", 10.5, 400, "#374151"),
        Line("mutual redistribution + tags", 10.5, 400, "#374151"),
    ])
    c.node_box(80, 300, 220, 100, "mgmt", [
        Line("DIST-01", 13, 700, "#111827"),
        Line("Area 10 (totally stubby)", 10.5, 400, "#374151"),
        Line("learns BRANCH subnet (OSPF ext)", 10, 400, "#6b7280"),
    ])
    c.node_box(660, 300, 220, 100, "mgmt", [
        Line("BRANCH-01", 13, 700, "#111827"),
        Line("EIGRP AS 100", 10.5, 400, "#374151"),
        Line("learns DIST subnet (EIGRP ext)", 10, 400, "#6b7280"),
    ])
    c.connector(400, 250, 220, 300, "mgmt", label="OSPF Area 0 ⇄ Area 10")
    c.connector(560, 250, 740, 300, "mgmt", label="EIGRP AS 100")
    c.node_box(370, 440, 220, 110, "data", [
        Line("GUEST VRF PBR", 12.5, 700, "#7c2d12"),
        Line("10.30.0.0/24 → tracked next hop", 10.5, 400, "#7c2d12"),
        Line("IP SLA object: track 10", 10.5, 400, "#7c2d12"),
    ])
    c.connector(480, 250, 480, 440, "data")
    c.node_box(60, 440, 260, 130, "warn", [
        Line("Negative Test", 11.5, 700, "#7f1d1d"),
        Line("tracked next hop shut down", 10.5, 400, "#7f1d1d"),
        Line("track 10 → Down", 10.5, 400, "#7f1d1d"),
        Line("PBR falls back to normal", 10.5, 400, "#7f1d1d"),
        Line("destination-based routing", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(320, 500, 370, 495, "warn")
    c.legend(80, 610, [("mgmt", "IGP adjacency"), ("data", "PBR / tracked path"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-03-ospf-eigrp-redistribution-pbr-topology.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: DMVPN Phase 3 Hub-and-Spoke with Dual-Path Internet Edge",
        subtitle="Dynamic spoke-to-spoke tunnel formation over mGRE/NHRP, plus IP SLA-tracked ISP failover on the hub",
        svg_title="Chapter 4 lab topology: a DMVPN Phase 3 overlay with two spokes and a dual-ISP internet edge on the hub",
        svg_desc="HUB-01 runs a multipoint GRE Tunnel0 (NHRP network-id 100) over IPsec, with SPOKE-01 "
                  "(172.16.0.11) and SPOKE-02 (172.16.0.12) registered as NHRP peers and EIGRP neighbors. Traffic "
                  "from SPOKE-01 to SPOKE-02's loopback is initially hub-relayed, then NHRP shortcut resolves a "
                  "dynamic spoke-to-spoke tunnel directly between them, confirmed with 'show ip nhrp'. Separately, "
                  "HUB-01's internet edge uses IP SLA-tracked dual paths (ISP-A primary, ISP-B floating static). As "
                  "a negative test, shutting down the ISP-A transport interface transitions the tracked object to "
                  "Down and the floating static route through ISP-B becomes the active default route.")
    c.node_box(370, 130, 220, 110, "mgmt", [
        Line("HUB-01", 14, 700, "#111827"),
        Line("Tunnel0 mGRE, NHRP nid 100", 10.5, 400, "#374151"),
        Line("ISP-A (primary) / ISP-B (float)", 10.5, 400, "#374151"),
    ])
    c.node_box(80, 300, 220, 100, "mgmt", [
        Line("SPOKE-01", 13, 700, "#111827"),
        Line("tunnel 172.16.0.11", 11, 700, "#1d4ed8"),
        Line("NHS: HUB-01", 10.5, 400, "#374151"),
    ])
    c.node_box(660, 300, 220, 100, "mgmt", [
        Line("SPOKE-02", 13, 700, "#111827"),
        Line("tunnel 172.16.0.12", 11, 700, "#1d4ed8"),
        Line("NHS: HUB-01", 10.5, 400, "#374151"),
    ])
    c.connector(400, 240, 210, 300, "mgmt", label="mGRE/NHRP + EIGRP")
    c.connector(560, 240, 750, 300, "mgmt", label="mGRE/NHRP + EIGRP")
    c.connector(300, 330, 660, 330, "data", label="dynamic spoke-to-spoke (NHRP shortcut)")
    c.node_box(80, 460, 260, 110, "neutral", [
        Line("ISP-A (primary transport)", 11.5, 700, "#111827"),
        Line("tracked by IP SLA (track 1)", 10.5, 400, "#374151"),
        Line("normal default route", 10.5, 400, "#374151"),
    ])
    c.node_box(390, 460, 260, 110, "warn", [
        Line("Negative Test", 11.5, 700, "#7f1d1d"),
        Line("ISP-A shut down → track 1 Down", 10.5, 400, "#7f1d1d"),
        Line("floating static via ISP-B becomes", 10.5, 400, "#7f1d1d"),
        Line("the active default route", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(430, 240, 210, 460, "neutral")
    c.connector(430, 570, 520, 460, "warn")
    c.legend(80, 610, [("mgmt", "DMVPN control-plane path"), ("data", "Dynamic data-plane tunnel"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-04-dmvpn-phase3-hub-spoke-topology.svg")


def ch05():
    c = Canvas(960, 660,
        title="Chapter 5 Hands-On Lab: Catalyst 9800 WLC, AP Join, and 802.1X WLAN",
        subtitle="CORP-WLAN on VLAN 20, authenticated against RADIUS/ISE, with fast roaming enabled",
        svg_title="Chapter 5 lab topology: a Catalyst 9800 WLC joining an AP and authenticating an 802.1X client",
        svg_desc="WLC-01's wireless management interface is on Vlan100. An access point joins the controller and "
                  "shows State Registered, tagged with CORP-POLICY-TAG/CAMPUS-SITE-TAG/CAMPUS-RF-TAG. CORP-WLAN "
                  "(802.1X, CORP-POLICY) is applied to the AP; a test client associates, authenticates against the "
                  "RADIUS/ISE server, and lands on VLAN 20 in State: Run. As a negative test, a second client using "
                  "an intentionally wrong 802.1X password never reaches Run state, and a failed-authentication "
                  "event is logged.")
    c.node_box(370, 120, 220, 100, "mgmt", [
        Line("WLC-01", 14, 700, "#111827"),
        Line("mgmt: Vlan100", 11, 700, "#1d4ed8"),
        Line("CORP-WLAN / CORP-POLICY", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 260, 220, 90, "mgmt", [
        Line("Access Point", 13, 700, "#111827"),
        Line("State: Registered", 10.5, 400, "#374151"),
        Line("CORP-POLICY-TAG applied", 10, 400, "#6b7280"),
    ])
    c.node_box(700, 120, 220, 100, "alt", [
        Line("RADIUS / ISE", 13, 700, "#111827"),
        Line("802.1X policy server", 10.5, 400, "#374151"),
        Line("returns VLAN 20 + dACL", 10, 400, "#374151"),
    ])
    c.node_box(60, 260, 240, 100, "alt", [
        Line("Test Client", 13, 700, "#111827"),
        Line("State: Run", 11, 700, "#14532d"),
        Line("VLAN 20, correct 802.1X creds", 10, 400, "#374151"),
    ])
    c.connector(480, 220, 480, 260, "mgmt", label="AP join (CAPWAP)")
    c.connector(590, 170, 700, 170, "alt", label="RADIUS authc")
    c.connector(370, 310, 300, 300, "alt", label="associate + 802.1X")
    c.node_box(370, 440, 340, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("2nd client, wrong 802.1X password", 10.5, 400, "#7f1d1d"),
        Line("never reaches State: Run", 10.5, 400, "#7f1d1d"),
        Line("failed-authentication event logged", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(370, 360, 460, 440, "warn")
    c.legend(60, 600, [("mgmt", "Join / control-plane"), ("alt", "Successful client path"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-05-catalyst-9800-wlc-8021x-topology.svg")


def ch06():
    c = Canvas(960, 660,
        title="Chapter 6 Hands-On Lab: End-to-End QoS from Access Trust Boundary to WAN-Edge LLQ",
        subtitle="VOICE traffic protected by WAN-EDGE-OUT's priority queue while class-default absorbs congestion",
        svg_title="Chapter 6 lab flow: an access-layer trust boundary feeding a WAN-edge LLQ/CBWFQ policy under congestion",
        svg_desc="An IP phone on ACCESS-01's trust boundary (trust device cisco-phone) marks voice traffic, which "
                  "flows through DIST-01 to a WAN-edge device applying the WAN-EDGE-OUT policy-map (VOICE, VIDEO, "
                  "CALL-SIGNALING, BUSINESS-CRITICAL classes with LLQ/CBWFQ) outbound. Under sustained best-effort "
                  "congestion plus a DSCP EF-marked test stream, the VOICE class shows near-zero drops while "
                  "class-default absorbs tail-drops. As a negative test, removing the service-policy from the WAN "
                  "interface and repeating the test shows the EF stream now drops/jitters proportionally to the "
                  "congestion, proving the queuing policy — not the marking alone — protected voice.")
    c.node_box(60, 160, 200, 100, "mgmt", [
        Line("ACCESS-01", 13, 700, "#111827"),
        Line("trust device cisco-phone", 10.5, 400, "#374151"),
        Line("DHCP snooping binding", 10, 400, "#6b7280"),
    ])
    c.node_box(370, 160, 200, 100, "mgmt", [
        Line("DIST-01", 13, 700, "#111827"),
        Line("trusted DSCP carried", 10.5, 400, "#374151"),
        Line("through to WAN edge", 10, 400, "#6b7280"),
    ])
    c.node_box(680, 130, 240, 160, "alt", [
        Line("WAN Edge — WAN-EDGE-OUT", 12.5, 700, "#111827"),
        Line("VOICE (LLQ, priority)", 10.5, 700, "#14532d"),
        Line("VIDEO / CALL-SIGNALING", 10.5, 400, "#374151"),
        Line("BUSINESS-CRITICAL / class-default", 10.5, 400, "#374151"),
        Line("class-default absorbs congestion", 10, 400, "#6b7280"),
    ])
    c.connector(260, 210, 370, 210, "mgmt", label="voice + best-effort")
    c.connector(570, 210, 680, 210, "mgmt", label="outbound WAN-EDGE-OUT")
    c.node_box(60, 400, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("service-policy output WAN-EDGE-OUT removed from the WAN interface, congestion test repeated", 11, 400, "#7f1d1d"),
        Line("EF-marked stream now experiences drops/jitter proportional to best-effort congestion", 11, 400, "#7f1d1d"),
        Line("confirms queuing — not marking alone — protected VOICE in the baseline test", 11, 400, "#7f1d1d"),
    ])
    c.connector(800, 290, 480, 400, "warn")
    c.legend(60, 570)
    c.save(f"{OUT}/chapter-06-qos-trust-boundary-wan-edge-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: 802.1X with MAB Fallback and TACACS+ Administration",
        subtitle="Three identically configured ports show dot1x success, MAB fallback, and RADIUS-dead behavior",
        svg_title="Chapter 7 lab topology: 802.1X/MAB open-mode authentication with a TACACS+-authenticated management plane",
        svg_desc="CLI administration on DIST-01 authenticates via TACACS+, confirmed by incrementing request/"
                  "response counters after an SSH login. ACCESS-01 has three identically configured open-mode "
                  "802.1X/MAB ports: Gi1/0/1 with an 802.1X-capable client authenticates via dot1x with a "
                  "RADIUS/ISE-returned VLAN and dACL; Gi1/0/2 with a non-802.1X device falls back to MAB after the "
                  "dot1x timeout; Gi1/0/3 is the negative test. As a negative test, RADIUS reachability is removed "
                  "and a new client on Gi1/0/3 either lands in the critical-authentication VLAN or stays "
                  "unauthenticated per the port's server-dead action, rather than being silently granted access.")
    c.node_box(370, 100, 220, 90, "alt", [
        Line("TACACS+ / RADIUS-ISE", 12.5, 700, "#111827"),
        Line("device admin + 802.1X/MAB", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 240, 220, 80, "mgmt", [
        Line("DIST-01", 13, 700, "#111827"),
        Line("CLI admin via TACACS+", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 240, 220, 100, "neutral", [
        Line("ACCESS-01", 14, 700, "#111827"),
        Line("Gi1/0/1, Gi1/0/2, Gi1/0/3", 10.5, 400, "#374151"),
        Line("open-mode 802.1X + MAB", 10.5, 400, "#374151"),
    ])
    c.connector(170, 240, 400, 190, "alt", label="TACACS+ (admin)")
    c.connector(480, 190, 480, 240, "alt", label="RADIUS (dot1x/MAB)")
    c.node_box(60, 400, 240, 100, "mgmt", [
        Line("Gi1/0/1: dot1x client", 11.5, 700, "#111827"),
        Line("Authc Success, method dot1x", 10.5, 400, "#374151"),
        Line("RADIUS-returned VLAN/dACL", 10, 400, "#6b7280"),
    ])
    c.node_box(360, 400, 240, 100, "alt", [
        Line("Gi1/0/2: non-802.1X device", 11.5, 700, "#111827"),
        Line("Authc Success, method mab", 10.5, 700, "#14532d"),
        Line("after dot1x timeout tx-period", 10, 400, "#374151"),
    ])
    c.node_box(660, 400, 240, 130, "warn", [
        Line("Gi1/0/3: Negative Test", 11.5, 700, "#7f1d1d"),
        Line("RADIUS server down", 10.5, 400, "#7f1d1d"),
        Line("critical-auth VLAN, or", 10.5, 400, "#7f1d1d"),
        Line("stays unauthenticated —", 10.5, 400, "#7f1d1d"),
        Line("never silently granted access", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(480, 340, 180, 400, "mgmt")
    c.connector(480, 340, 480, 400, "alt")
    c.connector(480, 340, 780, 400, "warn")
    c.legend(60, 600, [("mgmt", "802.1X path"), ("alt", "MAB fallback path"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-07-8021x-mab-tacacs-topology.svg")


def ch08():
    c = Canvas(960, 660,
        title="Chapter 8 Hands-On Lab: NETCONF/RESTCONF, Model-Driven Telemetry, and Idempotent Ansible",
        subtitle="RESTCONF read/auth-enforcement, a telemetry subscription, and a two-run idempotency check",
        svg_title="Chapter 8 lab flow: programmatic access to a Catalyst 9000 switch over RESTCONF, telemetry, and Ansible",
        svg_desc="A workstation queries DIST-01's Vlan10 interface over RESTCONF with curl, receiving a JSON "
                  "response matching the CLI's running-config. A model-driven telemetry subscription (ID 101) "
                  "streams state to the workstation, showing State Valid and an incrementing Sent Records counter. "
                  "An Ansible playbook run against the cisco.ios collection reports changed on its first run "
                  "(VLANs created) and ok with no changed tasks on a second, identical run, confirming idempotency. "
                  "As a negative test, the same RESTCONF query repeated with an intentionally wrong password "
                  "returns HTTP 401 Unauthorized, confirming RESTCONF enforces the same AAA credentials as CLI/SSH.")
    c.node_box(60, 180, 260, 140, "mgmt", [
        Line("Workstation", 13.5, 700, "#111827"),
        Line("curl, python3, ansible-core", 10.5, 400, "#374151"),
        Line("cisco.ios collection", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 160, 260, 180, "alt", [
        Line("DIST-01", 14, 700, "#111827"),
        Line("NETCONF + RESTCONF enabled", 10.5, 400, "#374151"),
        Line("telemetry subscription 101:", 10.5, 400, "#374151"),
        Line("State Valid, Sent Records ↑", 10.5, 700, "#14532d"),
    ])
    c.node_box(720, 160, 200, 100, "neutral", [
        Line("Ansible runs", 12, 700, "#111827"),
        Line("run 1: changed", 10.5, 400, "#374151"),
        Line("run 2: ok (idempotent)", 10.5, 400, "#374151"),
    ])
    c.connector(320, 220, 400, 220, "mgmt", label="RESTCONF GET Vlan10")
    c.connector(400, 280, 320, 280, "data", label="telemetry push")
    c.connector(660, 210, 720, 210, "mgmt", label="ansible-playbook")
    c.node_box(60, 420, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("curl RESTCONF GET repeated with an intentionally wrong password", 11, 400, "#7f1d1d"),
        Line("HTTP 401 Unauthorized — RESTCONF enforces the same AAA credentials as CLI/SSH", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 590, [("mgmt", "Request/response"), ("data", "Telemetry stream")])
    c.save(f"{OUT}/chapter-08-netconf-restconf-telemetry-ansible-flow.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: Catalyst Center SD-Access Fabric Provisioning and Assurance",
        subtitle="Discovery, LAN Automation, and fabric roles provisioned centrally, verified with Assurance Path Trace",
        svg_title="Chapter 9 lab topology: a Catalyst Center-provisioned SD-Access fabric with two edge nodes and SGACL enforcement",
        svg_desc="Catalyst Center discovers a seed device and runs LAN Automation to provision the underlay to two "
                  "candidate switches, then assigns fabric roles: the seed device as Control Plane + Border "
                  "(CTRL-01), and the two candidates as Edge nodes (EDGE-01, EDGE-02). EDGE-01's LISP session "
                  "establishes to CTRL-01's RLOC, and a test endpoint on EDGE-01 registers on the Control Plane "
                  "Node. Assurance Path Trace between endpoints on EDGE-01 and EDGE-02 confirms VXLAN "
                  "encapsulation at the edge/border and reports the SGT-pair policy applied. As a negative test, an "
                  "explicit deny SGACL is applied between the two endpoints' SGTs in Catalyst Center's Policy "
                  "application, and Path Trace/ping then shows the traffic denied at the enforcing node.")
    c.node_box(370, 100, 220, 90, "neutral", [
        Line("Catalyst Center", 13.5, 700, "#111827"),
        Line("Discovery + LAN Automation", 10.5, 400, "#374151"),
        Line("+ fabric/policy provisioning", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 250, 220, 100, "alt", [
        Line("CTRL-01", 14, 700, "#111827"),
        Line("Control Plane + Border", 11, 700, "#14532d"),
        Line("RLOC for edge sessions", 10.5, 400, "#374151"),
    ])
    c.node_box(90, 400, 220, 100, "mgmt", [
        Line("EDGE-01", 13, 700, "#111827"),
        Line("LISP session → CTRL-01", 10.5, 400, "#374151"),
        Line("test endpoint registered", 10, 400, "#6b7280"),
    ])
    c.node_box(650, 400, 220, 100, "mgmt", [
        Line("EDGE-02", 13, 700, "#111827"),
        Line("second test endpoint", 10.5, 400, "#374151"),
        Line("Path Trace target", 10, 400, "#6b7280"),
    ])
    c.connector(430, 190, 460, 250, "neutral", label="provision")
    c.connector(370, 300, 200, 400, "mgmt", label="LISP + VXLAN")
    c.connector(590, 300, 760, 400, "mgmt", label="LISP + VXLAN")
    c.connector(310, 450, 650, 450, "data", label="Path Trace: EDGE-01 ⇄ EDGE-02 (VXLAN)")
    c.node_box(90, 540, 780, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("deny SGACL applied between the two endpoints' SGTs in Catalyst Center Policy", 11, 400, "#7f1d1d"),
        Line("Path Trace / ping now shows traffic denied at the enforcing node (BORDER-01 role on CTRL-01)", 11, 400, "#7f1d1d"),
    ])
    c.legend(90, 620, [("mgmt", "Fabric control plane (LISP)"), ("data", "Endpoint-to-endpoint data path")])
    c.save(f"{OUT}/chapter-09-catalyst-center-sd-access-fabric-topology.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
