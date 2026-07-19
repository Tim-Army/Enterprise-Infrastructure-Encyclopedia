import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-02-network-engineering-foundations"


def ch01():
    c = Canvas(960, 660,
        title="Chapter 1 Hands-On Lab: Packet Capture and OSI Layer Decode",
        subtitle="tcpdump capture of an HTTP request, decoded layer by layer and cross-checked with a scapy-built packet",
        svg_title="Chapter 1 lab flow: capturing an HTTP request and confirming OSI-layer encapsulation",
        svg_desc="A lab host runs tcpdump scoped to tcp port 80 or 443 while curl issues an HTTP GET to example.com "
                  "(93.184.216.34:80). The captured .pcap is decoded with tshark -V, showing Frame, Ethernet II, "
                  "IPv4, TCP, and HTTP sections in order; a second tshark filter isolates the three-frame TCP "
                  "handshake (SYN, SYN-ACK, ACK); a scapy-built IP()/TCP() packet is shown to match the same layer "
                  "order. As a negative test, repeating the capture with an unused filter (tcp port 8443) yields a "
                  "capture with zero matching packets, demonstrating that an incorrect Layer 4 filter value silently "
                  "discards traffic rather than producing an error.")
    c.plane_bar(60, 90, 840, 30, "data", "Captured segment — tcpdump -i eth0 'tcp port 80 or tcp port 443'")
    c.node_box(60, 150, 240, 100, "mgmt", [
        Line("Lab Host", 14, 700, "#111827"),
        Line("curl http://example.com", 11, 400, "#374151"),
        Line("tcpdump -w model-lab.pcap", 11, 400, "#374151"),
    ])
    c.node_box(660, 150, 240, 100, "alt", [
        Line("example.com", 14, 700, "#111827"),
        Line("93.184.216.34:80", 11.5, 700, "#14532d"),
        Line("HTTP server", 11, 400, "#374151"),
    ])
    c.connector(300, 200, 660, 200, "data", label="HTTP GET / (captured)")
    c.node_box(60, 300, 260, 130, "neutral", [
        Line("tshark -r model-lab.pcap -V", 12, 700, "#111827"),
        Line("Frame → Ethernet II →", 10.5, 400, "#374151"),
        Line("IPv4 → TCP → HTTP", 10.5, 400, "#374151"),
        Line("(header order confirmed)", 10, 400, "#6b7280"),
    ])
    c.node_box(350, 300, 260, 130, "neutral", [
        Line("tshark -Y tcp.flags.syn|fin", 12, 700, "#111827"),
        Line("SYN → SYN,ACK → ACK", 10.5, 400, "#374151"),
        Line("3 distinct frames", 10, 400, "#6b7280"),
    ])
    c.node_box(640, 300, 260, 130, "alt", [
        Line("scapy: IP()/TCP()/Raw()", 12, 700, "#111827"),
        Line("###[ IP ]### / ###[ TCP ]###", 10.5, 400, "#14532d"),
        Line("matches captured order", 10, 400, "#374151"),
    ])
    c.connector(180, 250, 180, 300, "mgmt")
    c.connector(180, 250, 480, 300, "mgmt")
    c.connector(180, 250, 770, 300, "mgmt")
    c.node_box(60, 470, 840, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Filter changed to 'tcp port 8443' (unused port); curl re-run against example.com", 11, 400, "#7f1d1d"),
        Line("tshark -r model-lab.pcap → 0 matching packets (silently discarded, not an error)", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 610, [("mgmt", "Local analysis step"), ("data", "Captured network traffic"), ("alt", "Cross-check / expected match")])
    c.save(f"{OUT}/chapter-01-packet-capture-osi-layer-decode-flow.svg")


def ch02():
    c = Canvas(960, 660,
        title="Chapter 2 Hands-On Lab: VLSM Addressing Plan Validation",
        subtitle="Users /26 and Servers /27 segments derived from 10.50.0.0/24 and routed through a namespace router",
        svg_title="Chapter 2 lab topology: a VLSM addressing plan implemented with Linux network namespaces",
        svg_desc="A parent block 10.50.0.0/24 is subdivided by VLSM into a /26 Users segment (10.50.0.0/26), a /27 "
                  "Servers segment (10.50.0.64/27), and a /30 point-to-point block (10.50.0.96/30) reserved but "
                  "unused by this lab. ns-users (10.50.0.2/26) and ns-servers (10.50.0.65/27) each connect to "
                  "ns-router, which holds the first usable address of each block (10.50.0.1/26 and 10.50.0.66/27) "
                  "and forwards between them. As a negative test, a fourth namespace addressed at 10.50.0.30/26 "
                  "collides with the already-allocated Users block, and the conflicting 'ip addr add' on ns-router "
                  "fails with 'RTNETLINK answers: File exists'.")
    c.plane_bar(60, 90, 840, 30, "neutral", "Parent block — 10.50.0.0/24 (VLSM: largest block first)")
    c.node_box(80, 160, 230, 110, "mgmt", [
        Line("ns-users", 14, 700, "#111827"),
        Line("veth-u: 10.50.0.2/26", 11.5, 700, "#1d4ed8"),
        Line("block 10.50.0.0/26", 10.5, 400, "#374151"),
    ])
    c.node_box(365, 160, 230, 130, "alt", [
        Line("ns-router", 14, 700, "#111827"),
        Line("veth-ur: 10.50.0.1/26", 11, 700, "#14532d"),
        Line("veth-sr: 10.50.0.66/27", 11, 700, "#14532d"),
        Line("net.ipv4.ip_forward=1", 10, 400, "#374151"),
    ])
    c.node_box(650, 160, 230, 110, "mgmt", [
        Line("ns-servers", 14, 700, "#111827"),
        Line("veth-s: 10.50.0.65/27", 11.5, 700, "#1d4ed8"),
        Line("block 10.50.0.64/27", 10.5, 400, "#374151"),
    ])
    c.connector(310, 215, 365, 215, "mgmt", label="10.50.0.0/26")
    c.connector(595, 215, 650, 215, "mgmt", label="10.50.0.64/27")
    c.node_box(365, 340, 230, 70, "neutral", [
        Line("Reserved P2P block", 12, 700, "#111827"),
        Line("10.50.0.96/30 (not used by netns)", 10.5, 400, "#374151"),
    ])
    c.connector(480, 290, 480, 340, "neutral")
    c.node_box(80, 450, 800, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("ns-conflict addressed at 10.50.0.30/26 — overlaps the already-allocated Users block", 11, 400, "#7f1d1d"),
        Line("second 'ip addr add 10.50.0.30/26' on ns-router fails:", 11, 400, "#7f1d1d"),
        Line("RTNETLINK answers: File exists", 11, 700, "#7f1d1d"),
    ])
    c.legend(80, 610)
    c.save(f"{OUT}/chapter-02-vlsm-addressing-plan-topology.svg")


def ch03():
    c = Canvas(960, 660,
        title="Chapter 3 Hands-On Lab: VLAN-Filtered Bridge and Broadcast-Domain Isolation",
        subtitle="Two VLAN 20 hosts and one VLAN 30 host on a shared 802.1Q bridge, plus an STP loop test",
        svg_title="Chapter 3 lab topology: a VLAN-aware Linux bridge separating VLAN 20 and VLAN 30 broadcast domains",
        svg_desc="ns-host-a (10.20.0.2/24) and ns-host-b (10.20.0.3/24) are access ports on VLAN 20 of a VLAN-filtered "
                  "bridge br0 in ns-switch, and can reach each other. ns-host-c (10.20.0.4/24) is an access port on "
                  "VLAN 30 of the same physical bridge and cannot reach VLAN 20, demonstrating broadcast-domain "
                  "isolation. As a negative test, a second, looped link from ns-host-a back to the bridge causes a "
                  "broadcast storm with STP disabled; enabling the bridge's STP (stp_state 1) puts the redundant "
                  "link into a blocking state while the primary link stays forwarding, breaking the loop.")
    c.node_box(60, 150, 200, 100, "mgmt", [
        Line("ns-host-a", 13, 700, "#111827"),
        Line("10.20.0.2/24", 11, 700, "#1d4ed8"),
        Line("VLAN 20 access", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 300, 200, 100, "mgmt", [
        Line("ns-host-b", 13, 700, "#111827"),
        Line("10.20.0.3/24", 11, 700, "#1d4ed8"),
        Line("VLAN 20 access", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 190, 220, 170, "alt", [
        Line("ns-switch / br0", 14, 700, "#111827"),
        Line("vlan_filtering=1", 10.5, 400, "#374151"),
        Line("VLAN 20 + VLAN 30 ports", 10.5, 400, "#374151"),
        Line("stp_state 1 (negative test)", 10, 400, "#6b7280"),
    ])
    c.node_box(700, 150, 200, 100, "warn", [
        Line("ns-host-c", 13, 700, "#111827"),
        Line("10.20.0.4/24", 11, 700, "#b91c1c"),
        Line("VLAN 30 access", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(260, 190, 380, 240, "mgmt", label="VLAN 20")
    c.connector(260, 340, 380, 300, "mgmt", label="VLAN 20")
    c.connector(600, 250, 700, 200, "warn", label="VLAN 30 (isolated)")
    c.node_box(60, 420, 200, 90, "warn", [
        Line("veth-a2 (looped link)", 11.5, 700, "#7f1d1d"),
        Line("VLAN 20, STP disabled", 10.5, 400, "#7f1d1d"),
        Line("→ broadcast storm", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(160, 250, 160, 420, "warn", label="redundant cable")
    c.node_box(380, 420, 380, 110, "neutral", [
        Line("After stp_state 1 (5s convergence)", 11.5, 700, "#111827"),
        Line("veth-a-br: state forwarding", 10.5, 400, "#374151"),
        Line("veth-a2-br: state blocking", 10.5, 400, "#374151"),
        Line("loop broken, no storm", 10, 400, "#6b7280"),
    ])
    c.connector(260, 465, 380, 475, "neutral")
    c.legend(60, 610, [("mgmt", "VLAN 20 (allowed)"), ("warn", "VLAN 30 / negative-test path")])
    c.save(f"{OUT}/chapter-03-vlan-bridge-broadcast-isolation-topology.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: Three-Router OSPF Area 0 with Simulated Link Failure",
        subtitle="r1—r2—r3 line topology; OSPF learns 192.168.3.1/32 across r2 with no direct r1–r3 link",
        svg_title="Chapter 4 lab topology: three FRRouting routers in a line, running OSPF in Area 0",
        svg_desc="Router r1 (loopback 192.168.1.1/32) connects to r2 over 10.0.12.0/30; r2 connects to r3 (loopback "
                  "192.168.3.1/32) over 10.0.23.0/30. All three run FRR's ospfd advertising their connected "
                  "interfaces into Area 0. r1 learns a dynamic route to 192.168.3.1/32 via r2, though r1 has no "
                  "direct link to r3. As a negative test, the r1–r2 link is set down; OSPF withdraws the route to "
                  "192.168.3.1/32 within the failure-detection window, and a subsequent ping from r1 fails "
                  "immediately with 'Network is unreachable' rather than timing out.")
    c.node_box(60, 180, 220, 130, "mgmt", [
        Line("r1", 15, 700, "#111827"),
        Line("r1-r2: 10.0.12.1/30", 11, 700, "#1d4ed8"),
        Line("lo: 192.168.1.1/32", 11, 400, "#374151"),
        Line("OSPF Area 0", 10, 400, "#6b7280"),
    ])
    c.node_box(370, 180, 220, 130, "alt", [
        Line("r2", 15, 700, "#111827"),
        Line("r2-r1: 10.0.12.2/30", 11, 700, "#14532d"),
        Line("r2-r3: 10.0.23.1/30", 11, 700, "#14532d"),
        Line("OSPF Area 0", 10, 400, "#6b7280"),
    ])
    c.node_box(680, 180, 220, 130, "mgmt", [
        Line("r3", 15, 700, "#111827"),
        Line("r3-r2: 10.0.23.2/30", 11, 700, "#1d4ed8"),
        Line("lo: 192.168.3.1/32", 11, 400, "#374151"),
        Line("OSPF Area 0", 10, 400, "#6b7280"),
    ])
    c.connector(280, 245, 370, 245, "mgmt", label="10.0.12.0/30")
    c.connector(590, 245, 680, 245, "mgmt", label="10.0.23.0/30")
    c.node_box(60, 360, 220, 60, "warn", [
        Line("Negative test: link down", 11.5, 700, "#7f1d1d"),
        Line("ip link set r1-r2 down", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(170, 310, 170, 360, "warn")
    c.node_box(310, 450, 640, 130, "neutral", [
        Line("Result of the OSPF Area 0 adjacency and failover", 12.5, 700, "#111827"),
        Line("Normal: r2 lists r1 and r3 as Full neighbors; r1 pings 192.168.3.1 via r2 (0% loss)", 11, 400, "#374151"),
        Line("After r1–r2 down: r1's route to 192.168.3.1/32 is withdrawn", 11, 400, "#7f1d1d"),
        Line("ping from r1 fails immediately — \"Network is unreachable\", not a timeout", 11, 400, "#7f1d1d"),
    ])
    c.connector(280, 390, 310, 460, "neutral")
    c.legend(60, 610, [("mgmt", "Router-to-router OSPF link"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-04-ospf-three-router-topology.svg")


def ch05():
    c = Canvas(960, 660,
        title="Chapter 5 Hands-On Lab: DHCP, DNS, and PAT with dnsmasq",
        subtitle="ns-client leases an address and resolves a lab domain through ns-router, which PATs to ns-wan",
        svg_title="Chapter 5 lab topology: a router namespace providing DHCP, DNS, and NAT for a client namespace",
        svg_desc="ns-router runs dnsmasq, offering a single-address DHCP scope (10.90.0.100) with gateway and DNS "
                  "server both set to 10.90.0.1, and a static record app.lab.internal -> 10.90.0.1. ns-client leases "
                  "10.90.0.100/24 by DHCP and resolves app.lab.internal via DNS. ns-router also MASQUERADEs "
                  "10.90.0.0/24 traffic out its 203.0.113.1/30 interface toward ns-wan (203.0.113.2/30), which never "
                  "sees a route back to 10.90.0.0/24. As a negative test, a second client cannot obtain a lease from "
                  "the exhausted single-address DHCP scope.")
    c.node_box(60, 190, 220, 120, "mgmt", [
        Line("ns-client", 14, 700, "#111827"),
        Line("DHCP → 10.90.0.100/24", 11, 700, "#1d4ed8"),
        Line("DNS via 10.90.0.1", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 170, 240, 160, "alt", [
        Line("ns-router (dnsmasq)", 13.5, 700, "#111827"),
        Line("veth-cr: 10.90.0.1/24", 11, 700, "#14532d"),
        Line("veth-wr: 203.0.113.1/30", 11, 700, "#14532d"),
        Line("DHCP scope: 10.90.0.100 only", 10, 400, "#374151"),
        Line("MASQUERADE → veth-wr", 10, 400, "#374151"),
    ])
    c.node_box(700, 190, 220, 120, "mgmt", [
        Line("ns-wan (\"internet\")", 13, 700, "#111827"),
        Line("203.0.113.2/30", 11, 700, "#1d4ed8"),
        Line("sees only NAT'd source", 10.5, 400, "#374151"),
    ])
    c.connector(280, 250, 370, 250, "mgmt", label="DHCP + DNS (10.90.0.0/24)")
    c.connector(610, 250, 700, 250, "data", label="PAT (203.0.113.0/30)")
    c.node_box(60, 400, 840, 120, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("ns-client2 requests a lease from the same single-address scope (10.90.0.100, already leased)", 11, 400, "#7f1d1d"),
        Line("dhclient on ns-client2 repeats DHCPDISCOVER with no DHCPOFFER — veth-c2 receives no address", 11, 400, "#7f1d1d"),
        Line("reproduces DHCP scope exhaustion", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 570, [("mgmt", "DHCP / DNS (internal)"), ("data", "PAT'd outbound traffic")])
    c.save(f"{OUT}/chapter-05-dhcp-dns-pat-topology.svg")


def ch06():
    c = Canvas(960, 660,
        title="Chapter 6 Hands-On Lab: 802.11 Association Sequence and Free Space Path Loss",
        subtitle="Synthetic Beacon/Probe/Association frames between AP and Client, plus a 2.4/5/6 GHz coverage comparison",
        svg_title="Chapter 6 lab sequence: a synthetic 802.11 beacon and association exchange, decoded with tshark",
        svg_desc="A synthetic AP (02:00:00:00:00:01, SSID LAB-WLAN, channel 6) and Client (02:00:00:00:00:02) exchange "
                  "five crafted management frames in order: Beacon, Probe Request, Probe Response, Association "
                  "Request, and Association Response, matching the association sequence from this chapter's theory "
                  "section. Separately, free space path loss is calculated at 10, 30, and 60 meters for 2.4 GHz, "
                  "5 GHz, and 6 GHz, showing 6 GHz attenuates fastest. As a negative test, at 100 meters the "
                  "estimated 6 GHz RSSI falls below a -70 dBm reliability threshold, showing a link budget deficit.")
    c.node_box(60, 110, 220, 80, "mgmt", [
        Line("Client (STA)", 13, 700, "#111827"),
        Line("addr 02:00:00:00:00:02", 10.5, 400, "#374151"),
    ])
    c.node_box(680, 110, 220, 80, "alt", [
        Line("AP — LAB-WLAN, ch 6", 13, 700, "#111827"),
        Line("addr 02:00:00:00:00:01", 10.5, 400, "#374151"),
    ])
    c.divider(170, 190, 170, 470)
    c.divider(790, 190, 790, 470)
    c.connector(790, 215, 170, 215, "alt", label="1. Beacon (subtype 0x08)")
    c.connector(170, 265, 790, 265, "mgmt", label="2. Probe Request (0x04)")
    c.connector(790, 315, 170, 315, "alt", label="3. Probe Response (0x05)")
    c.connector(170, 365, 790, 365, "mgmt", label="4. Association Request (0x00)")
    c.connector(790, 415, 170, 415, "alt", label="5. Association Response (0x01)")
    c.node_box(230, 470, 500, 90, "neutral", [
        Line("Free space path loss @ 10 / 30 / 60 m", 12, 700, "#111827"),
        Line("2.4 GHz lowest loss  ·  5 GHz mid  ·  6 GHz highest loss", 10.5, 400, "#374151"),
        Line("(higher frequency attenuates faster over distance)", 10, 400, "#6b7280"),
    ])
    c.node_box(230, 580, 500, 60, "warn", [
        Line("Negative test: @100 m, 6 GHz RSSI < −70 dBm → link budget deficit", 11, 700, "#7f1d1d"),
    ])
    c.legend(60, 610, [("mgmt", "Client-originated frame"), ("alt", "AP-originated frame")])
    c.save(f"{OUT}/chapter-06-wireless-association-sequence.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: VRRP Failover Across a Shared Bridge",
        subtitle="ns-r1 (Master, priority 150) holds VIP 10.60.0.1 until keepalived is killed; ns-r2 (Backup) then takes over",
        svg_title="Chapter 7 lab topology: two VRRP routers sharing a bridge and a virtual IP, with a measured failover",
        svg_desc="ns-r1 (10.60.0.2/24, priority 150) and ns-r2 (10.60.0.3/24, priority 100) both run keepalived for "
                  "VRRP group 60, sharing the virtual IP 10.60.0.1/24 over the bridge br-vrrp. ns-r1 wins the "
                  "election as Master and holds the VIP; ns-client (10.60.0.100/24) reaches the VIP as its default "
                  "gateway. As a negative test, keepalived is killed on ns-r1; a continuous ping shows one to three "
                  "missed replies (consistent with the 1-second advertisement interval) before the VIP reappears on "
                  "ns-r2, confirming Backup promotes to Master.")
    c.node_box(70, 150, 210, 110, "mgmt", [
        Line("ns-r1 (MASTER)", 13, 700, "#111827"),
        Line("10.60.0.2/24 · prio 150", 11, 700, "#1d4ed8"),
        Line("owns VIP 10.60.0.1", 10.5, 400, "#374151"),
    ])
    c.node_box(70, 320, 210, 110, "warn", [
        Line("ns-r2 (BACKUP)", 13, 700, "#111827"),
        Line("10.60.0.3/24 · prio 100", 11, 700, "#7f1d1d"),
        Line("takes VIP if r1 fails", 10.5, 400, "#7f1d1d"),
    ])
    c.node_box(370, 230, 200, 150, "neutral", [
        Line("br-vrrp", 14, 700, "#111827"),
        Line("shared L2 segment", 10.5, 400, "#374151"),
        Line("10.60.0.0/24", 10.5, 400, "#374151"),
        Line("VIP 10.60.0.1 (VRID 60)", 10.5, 700, "#111827"),
    ])
    c.node_box(690, 260, 210, 110, "alt", [
        Line("ns-client", 13, 700, "#111827"),
        Line("10.60.0.100/24", 11, 700, "#14532d"),
        Line("default via 10.60.0.1", 10.5, 400, "#374151"),
    ])
    c.connector(280, 205, 370, 280, "mgmt")
    c.connector(280, 375, 370, 330, "warn")
    c.connector(570, 305, 690, 315, "alt")
    c.node_box(70, 500, 830, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("kill keepalived on ns-r1 (Master) — continuous ping to VIP shows 1–3 missed replies (~1s advert_int)", 11, 400, "#7f1d1d"),
        Line("VIP 10.60.0.1 reappears on ns-r2's veth-r2 — Backup promoted to Master, correct FHRP failover", 11, 400, "#7f1d1d"),
    ])
    c.legend(70, 630, [("mgmt", "Master (normal)"), ("warn", "Backup / failover path"), ("alt", "Client reachability")])
    c.save(f"{OUT}/chapter-07-vrrp-failover-topology.svg")


def ch08():
    c = Canvas(960, 660,
        title="Chapter 8 Hands-On Lab: Minimal Syslog Receiver and Alert Correlation",
        subtitle="An RFC 5424 UDP receiver parses PRI severity and correlates a burst of errors into one alert",
        svg_title="Chapter 8 lab flow: a UDP syslog receiver parsing RFC 5424 severity and correlating error bursts",
        svg_desc="logger (or a Python UDP fallback) sends RFC 5424-formatted syslog messages to 127.0.0.1:1514. "
                  "syslog_receiver.py parses the PRI field into facility and severity, printing a human-readable "
                  "line per message, for example '[Warning] facility=16 :: interface Gi0/1 flapping'. Three "
                  "error-or-higher messages within 10 seconds trigger a correlated ALERT line rather than three "
                  "separate low-signal notices. As a negative test, a message with no valid PRI field is printed as "
                  "'[UNPARSEABLE] raw message: ...' and the receiver keeps running rather than crashing.")
    c.node_box(60, 180, 240, 130, "mgmt", [
        Line("logger --rfc5424", 13, 700, "#111827"),
        Line("or python3 UDP fallback", 10.5, 400, "#374151"),
        Line("→ 127.0.0.1:1514", 10.5, 400, "#374151"),
        Line("-p local0.warning / .err", 10, 400, "#6b7280"),
    ])
    c.node_box(360, 170, 260, 150, "alt", [
        Line("syslog_receiver.py", 13.5, 700, "#111827"),
        Line("UDP :1514", 10.5, 400, "#374151"),
        Line("parse PRI → facility/severity", 10.5, 400, "#374151"),
        Line("≥3 errors / 10s → ALERT", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(700, 180, 220, 130, "neutral", [
        Line("Console Output", 12.5, 700, "#111827"),
        Line("[Warning] facility=16 ::", 10, 400, "#374151"),
        Line("interface Gi0/1 flapping", 10, 400, "#374151"),
        Line("!! ALERT (3 errors/10s)", 10, 700, "#111827"),
    ])
    c.connector(300, 245, 360, 245, "mgmt", label="UDP")
    c.connector(620, 245, 700, 245, "mgmt", label="stdout")
    c.node_box(60, 400, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("malformed message with no valid PRI field sent to the receiver", 11, 400, "#7f1d1d"),
        Line("→ '[UNPARSEABLE] raw message: ...' printed; receiver keeps listening (no unhandled exception)", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 570)
    c.save(f"{OUT}/chapter-08-syslog-receiver-alert-correlation-flow.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: Structured Troubleshooting of a DHCP-Delivered DNS Fault",
        subtitle="A wrong DHCP dns-server option (10.95.0.53) is diagnosed bottom-up and fixed at the actual cause",
        svg_title="Chapter 9 lab topology: diagnosing a DHCP-delivered DNS server address that points at nothing",
        svg_desc="ns-router runs dnsmasq serving both DHCP and DNS on 10.95.0.1/24, but the DHCP dns-server option "
                  "is deliberately misconfigured to 10.95.0.53, an address nothing listens on. ns-client leases "
                  "10.95.0.100/24 correctly but receives the broken resolver address. Step 1 defines the problem "
                  "(dig times out); Step 2/3 confirm Layer 3 to the gateway is healthy and isolate resolv.conf's "
                  "10.95.0.53 as the theory; Step 4 tests the theory by querying 10.95.0.1 directly, which "
                  "succeeds; Steps 5/6 fix the DHCP option to 10.95.0.1 and verify. As a negative test, skipping "
                  "the theory-test step and instead only bouncing the client interface leaves the fault in place.")
    c.node_box(70, 170, 240, 140, "mgmt", [
        Line("ns-client", 14, 700, "#111827"),
        Line("DHCP → 10.95.0.100/24", 11, 700, "#1d4ed8"),
        Line("resolv.conf: 10.95.0.53", 11, 700, "#b91c1c"),
        Line("(wrong — fault)", 10, 400, "#7f1d1d"),
    ])
    c.node_box(400, 160, 260, 160, "alt", [
        Line("ns-router (dnsmasq)", 13.5, 700, "#111827"),
        Line("veth-cr: 10.95.0.1/24", 11, 700, "#14532d"),
        Line("dhcp-option dns-server:", 10.5, 400, "#374151"),
        Line("10.95.0.53 ← injected fault", 10.5, 700, "#b91c1c"),
        Line("actual DNS service: 10.95.0.1", 10.5, 400, "#374151"),
    ])
    c.connector(310, 240, 400, 240, "mgmt", label="10.95.0.0/24")
    c.node_box(70, 350, 300, 100, "warn", [
        Line("Steps 1–3: define + theorize", 11.5, 700, "#7f1d1d"),
        Line("dig app.lab.internal → timeout", 10.5, 400, "#7f1d1d"),
        Line("ping gateway OK; resolv.conf = .53", 10.5, 400, "#7f1d1d"),
    ])
    c.node_box(400, 350, 260, 100, "neutral", [
        Line("Step 4: test the theory", 11.5, 700, "#111827"),
        Line("dig @10.95.0.1 app.lab.internal", 10.5, 400, "#374151"),
        Line("→ succeeds: DNS itself is fine", 10.5, 400, "#374151"),
    ])
    c.node_box(690, 350, 220, 100, "alt", [
        Line("Steps 5–6: fix + verify", 11.5, 700, "#111827"),
        Line("dns-server → 10.95.0.1", 10.5, 400, "#14532d"),
        Line("renew lease; dig succeeds", 10.5, 400, "#14532d"),
    ])
    c.connector(220, 310, 220, 350, "warn")
    c.connector(370, 400, 400, 400, "neutral")
    c.connector(660, 400, 690, 400, "alt")
    c.node_box(70, 490, 840, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Skip the theory test: with the original fault still in place, only bounce ns-client's interface", 11, 400, "#7f1d1d"),
        Line("dig app.lab.internal still fails — the interface bounce never touched the DHCP scope's DNS option", 11, 400, "#7f1d1d"),
    ])
    c.legend(70, 630, [("mgmt", "DHCP-delivered config"), ("warn", "Fault / negative-test path"), ("alt", "Corrected state")])
    c.save(f"{OUT}/chapter-09-dhcp-dns-fault-troubleshooting-topology.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
