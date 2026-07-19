import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-20-wireshark-packet-analysis"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Hands-On Lab: Capture Rights Scoped to a Group, Confirmed by an Account That Isn't In It",
        subtitle="A hashed, timestamped baseline capture is produced without elevation; a second, unmodified account is correctly refused",
        svg_title="Chapter 1 lab flow: non-administrative Wireshark capture rights validated end to end, then tested against an account outside the configured group",
        svg_desc="Non-administrative capture access (Npcap unrestricted, ChmodBPF access_bpf group, or Linux "
                  "capabilities) lets tshark -D list interfaces with no permission error and no elevation. A "
                  "30-second baseline capture is taken, confirmed with capinfos, then hashed with sha256sum "
                  "alongside a UTC collection timestamp as an evidence-handling record. As a negative test, a "
                  "capture attempt from a second, unmodified user account without the configured group "
                  "membership is denied with a permission error, confirming capture rights are correctly scoped "
                  "to the intended group rather than open to every local account.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Non-admin capture rights", 12.5, 700, "#111827"),
        Line("tshark -D: interfaces listed", 10.5, 400, "#374151"),
        Line("no sudo/Administrator needed", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Baseline capture", 12.5, 700, "#111827"),
        Line("capinfos: valid pcapng, ~30s", 10.5, 400, "#374151"),
        Line("sha256 + UTC timestamp recorded", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("second, unmodified account", 10.5, 700, "#7f1d1d"),
        Line("attempts capture", 10.5, 700, "#7f1d1d"),
        Line("→ permission denied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("capture rights are scoped to the specific group configured in step 1, not open to every local", 11.5, 400, "#374151"),
        Line("account by default — the denial confirms the scoping is real, not merely documented.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Configured capture group"), ("alt", "Hashed evidence artifact"), ("warn", "Out-of-group denial")])
    c.save(f"{OUT}/chapter-01-nonadmin-capture-evidence-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A Capture Filter Proven Specific, Not Accidentally Broad",
        subtitle="Port 22 traffic never reaches disk even during an active SSH session; DNS traffic from the same window proves the exclusion wasn't overreaching",
        svg_title="Chapter 2 lab flow: a ring-buffer capture with a BPF exclusion filter, validated for both correct exclusion and correctly narrow scope",
        svg_desc="A dumpcap ring-buffer capture bounded to five 2 MB files, filtered to exclude port 22, rotates "
                  "correctly (never more than five files present) while traffic is generated to force rotation. "
                  "Filtering the resulting files for tcp.port==22 returns nothing, confirming SSH management "
                  "traffic was discarded by the BPF capture filter before it ever reached disk — even though the "
                  "SSH session running these commands was active throughout. As a negative test, the same file is "
                  "filtered for DNS traffic instead; DNS packets do appear, confirming the exclusion was specific "
                  "to port 22 rather than an accidentally broad filter that discarded everything.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("dumpcap ring buffer", 12.5, 700, "#111827"),
        Line("5 files x 2MB, filter: not port 22", 10.5, 400, "#374151"),
        Line("rotation confirmed (≤5 files)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("tcp.port==22 check", 12.5, 700, "#111827"),
        Line("→ no output", 10.5, 700, "#14532d"),
        Line("(SSH excluded at capture time)", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("dns filter check on the", 10.5, 700, "#7f1d1d"),
        Line("same file → DNS DOES appear", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("DNS traffic appearing in the same capture confirms the exclusion filter targeted port 22 specifically —", 11.5, 400, "#374151"),
        Line("not an overly broad rule that happened to also discard everything else.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Bounded ring-buffer capture"), ("alt", "Confirmed exclusion"), ("warn", "Confirmed narrow scope")])
    c.save(f"{OUT}/chapter-02-ring-buffer-capture-filter-flow.svg")


def ch03():
    c = Canvas(960, 580,
        title="Chapter 3 Hands-On Lab: Wireshark Rejects an Invalid Filter Field Rather Than Silently Matching Nothing",
        subtitle="A dedicated analysis profile, saved filter, coloring rule, and Follow Stream all work as configured; a misspelled field name is caught immediately",
        svg_title="Chapter 3 lab flow: a dedicated Wireshark analysis profile with a saved filter, coloring rule, and custom column, tested against a misspelled filter field",
        svg_desc="A Lab03-Analysis profile isolates a lab-specific workflow: a SYN-only display filter is saved "
                  "as a filter button, a Retransmissions coloring rule highlights tcp.analysis.retransmission, a "
                  "custom TCP Delta column exposes tcp.time_delta, and Follow TCP Stream reassembles a full "
                  "conversation in a separate window. As a negative test, a deliberately misspelled field name "
                  "(tcp.flagz.syn instead of tcp.flags.syn) is entered in the filter bar; the bar turns red/pink "
                  "and the filter does not apply at all, demonstrating Wireshark's syntax validation rejects an "
                  "invalid field name outright rather than silently applying a filter that matches nothing.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Lab03-Analysis profile", 12.5, 700, "#111827"),
        Line("saved SYN filter, coloring rule,", 10.5, 400, "#374151"),
        Line("custom column, all applied", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Follow TCP Stream", 12.5, 700, "#111827"),
        Line("reassembled conversation", 10.5, 700, "#14532d"),
        Line("client/server data, distinct colors", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("tcp.flagz.syn==1", 10.5, 700, "#7f1d1d"),
        Line("(misspelled field)", 10.5, 700, "#7f1d1d"),
        Line("→ filter bar red, not applied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the invalid filter is rejected outright rather than silently evaluating to zero matches — Wireshark's", 11.5, 400, "#374151"),
        Line("syntax validation catches the typo before it could ever be mistaken for a valid, empty result.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Configured analysis profile"), ("alt", "Reassembled stream"), ("warn", "Rejected invalid syntax")])
    c.save(f"{OUT}/chapter-03-analysis-profile-filter-validation-flow.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: A TTL Filter That Correctly Returns Empty Rather Than Matching the Wrong Traffic",
        subtitle="ARP resolution, ping, and traceroute all isolate cleanly with targeted filters; an impossible TTL condition confirms the filter isn't matching unrelated packets",
        svg_title="Chapter 4 lab flow: ARP, ICMP echo, and traceroute captured and isolated with targeted display filters, tested against a TTL value that cannot appear",
        svg_desc="A capture scoped to ARP and ICMP shows one broadcast ARP request followed by one unicast reply "
                  "resolving the gateway's MAC address; a ping sequence isolates to matched Echo Request/Echo "
                  "Reply pairs; a traceroute isolates to a Time Exceeded hop ladder ending in the destination's "
                  "reply. As a negative test, a filter for an original Echo Request TTL of 1 — a value never "
                  "actually used as the starting TTL in this lab's traffic — returns zero matches, confirming the "
                  "filter correctly produces an empty result rather than matching unrelated packets when the "
                  "condition genuinely does not occur in the capture.")
    c.node_box(60, 140, 220, 110, "mgmt", [
        Line("ARP exchange", 12.5, 700, "#111827"),
        Line("request (broadcast) →", 10.5, 400, "#374151"),
        Line("reply (unicast), gateway MAC", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 140, 220, 110, "alt", [
        Line("Ping sequence", 12.5, 700, "#111827"),
        Line("Echo Request/Reply pairs", 10.5, 700, "#14532d"),
        Line("(4 of each, matched)", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Traceroute hop ladder", 12.5, 700, "#111827"),
        Line("Time Exceeded, increasing hops", 10.5, 400, "#374151"),
        Line("→ final Echo Reply", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 320, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("filter: ip.ttl == 1 && icmp.type == 8 (original Echo Request TTL of 1, never actually used)", 11, 400, "#7f1d1d"),
        Line("zero packets match — the filter correctly returns empty rather than matching unrelated traffic,", 11, 400, "#7f1d1d"),
        Line("confirming the filter logic behaves correctly even when the condition genuinely doesn't occur", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 470, [("mgmt", "Layer 2 resolution"), ("alt", "Isolated ICMP sequences")])
    c.save(f"{OUT}/chapter-04-arp-icmp-traceroute-filter-flow.svg")


def ch05():
    c = Canvas(960, 580,
        title="Chapter 5 Hands-On Lab: A Filter That Distinguishes a Failed Resolution From a Successful One",
        subtitle="A clean DORA exchange and a successful DNS answer both isolate correctly; an NXDOMAIN response is caught by rcode, not confused with success",
        svg_title="Chapter 5 lab flow: DHCP DORA and DNS resolution captured and isolated with targeted filters, tested against a deliberately unresolvable domain",
        svg_desc="A capture scoped to DHCP and DNS shows the full four-message DORA exchange in order — "
                  "Discover, Offer, Request, Ack — each from the expected source, and a DNS query/response pair "
                  "for a real domain shows rcode==0 with at least one answer record. As a negative test, a query "
                  "for a domain guaranteed not to exist is captured the same way; the filter for that domain "
                  "matches a response with rcode==3 (NXDOMAIN), confirming the filter correctly distinguishes a "
                  "failed resolution from the successful one captured moments earlier, rather than treating both "
                  "as equivalent 'a response arrived' events.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("DHCP DORA exchange", 12.5, 700, "#111827"),
        Line("Discover → Offer → Request → Ack", 10.5, 700, "#1d4ed8"),
        Line("(correct order, correct sources)", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 110, "alt", [
        Line("DNS query (real domain)", 12.5, 700, "#111827"),
        Line("rcode==0, answer present", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 195, 400, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("query: nonexistent domain", 10.5, 700, "#7f1d1d"),
        Line("→ rcode==3 (NXDOMAIN)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 195, 700, 195, "warn")
    c.node_box(60, 300, 860, 90, "neutral", [
        Line("the rcode field distinguishes success from failure precisely — a filter matching 'a response arrived'", 11.5, 400, "#374151"),
        Line("alone would have conflated the successful and failed queries; rcode==3 catches the difference.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 430, [("mgmt", "DHCP lease sequence"), ("alt", "Successful resolution"), ("warn", "Failed resolution (correctly detected)")])
    c.save(f"{OUT}/chapter-05-dhcp-dns-nxdomain-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: Expert-Flag Retransmission Analysis Confirmed Against Induced Loss",
        subtitle="A clean baseline transfer shows the handshake options and RTT/throughput graphs; injecting 2% loss makes retransmissions appear where they didn't before",
        svg_title="Chapter 6 lab flow: TCP handshake options, RTT, and throughput analyzed on a real transfer, then contrasted against a transfer with deliberately induced packet loss",
        svg_desc="A 10+ MB file transfer's SYN and SYN-ACK show Window Scale and SACK Permitted options in the "
                  "handshake; TCP Stream Graphs plot RTT and throughput for the transfer, and a "
                  "tcp.analysis.retransmission filter records a baseline count (zero is a valid, clean-network "
                  "result). As a negative test, tc netem introduces 2% artificial loss on the capture interface "
                  "and the transfer repeats; the same retransmission filter now shows a nonzero count in the new "
                  "capture, contrasted directly against the loss-free baseline — confirming Wireshark's expert-"
                  "flag analysis correctly detects retransmissions caused by genuinely induced loss, not just "
                  "reporting a fixed value regardless of network conditions.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Baseline transfer (10+ MB)", 12.5, 700, "#111827"),
        Line("SYN/SYN-ACK: Window Scale + SACK", 10.5, 400, "#374151"),
        Line("retransmissions: baseline count", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("RTT + Throughput graphs", 12.5, 700, "#111827"),
        Line("plotted for the transfer stream", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("tc netem: 2% loss injected", 10.5, 700, "#7f1d1d"),
        Line("transfer repeated", 10.5, 700, "#7f1d1d"),
        Line("→ nonzero retransmissions", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the retransmission count rises specifically because loss was induced — contrasted against the", 11.5, 400, "#374151"),
        Line("loss-free baseline, confirming the expert-flag analysis responds to actual network conditions.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Clean baseline transfer"), ("alt", "Performance graphs"), ("warn", "Induced loss (detected)")])
    c.save(f"{OUT}/chapter-06-tcp-retransmission-induced-loss-flow.svg")


def ch07():
    c = Canvas(960, 580,
        title="Chapter 7 Hands-On Lab: HTTPS Decryption Genuinely Depends on the Configured Key Log",
        subtitle="HTTP frames and response timing appear once the TLS key log is configured; clearing that one setting turns them back into opaque Application Data",
        svg_title="Chapter 7 lab flow: an HTTPS session decrypted in Wireshark via SSLKEYLOGFILE, tested against a cleared key log preference",
        svg_desc="With SSLKEYLOGFILE set, an HTTPS request from an instrumented client populates a key log file "
                  "with at least one CLIENT_HANDSHAKE_TRAFFIC_SECRET or CLIENT_RANDOM line. Pointing Wireshark's "
                  "TLS pre-master-secret log preference at that file and filtering for http reveals decrypted "
                  "HTTP request/response frames, with a populated http.time value for the response. As a "
                  "negative test, the TLS key log preference is cleared and the capture reloaded; the same http "
                  "filter now matches nothing — the identical Application Data records dissect only as encrypted "
                  "TLS — confirming decryption genuinely depended on the configured key log rather than some "
                  "other mechanism or cached state.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("SSLKEYLOGFILE set", 12.5, 700, "#111827"),
        Line("HTTPS request generates", 10.5, 400, "#374151"),
        Line("key log entries", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Key log configured in Wireshark", 12, 700, "#111827"),
        Line("http filter → decrypted frames", 10.5, 700, "#14532d"),
        Line("http.time populated", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("key log preference cleared", 10.5, 700, "#7f1d1d"),
        Line("→ http filter: no matches", 10.5, 700, "#7f1d1d"),
        Line("(encrypted Application Data only)", 10, 400, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("removing only the key log preference — nothing else — collapses decryption entirely, confirming", 11.5, 400, "#374151"),
        Line("it was the specific mechanism responsible, not an artifact of some other Wireshark setting.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Key log generation"), ("alt", "Decrypted HTTP visibility"), ("warn", "Key log removed (re-encrypted view)")])
    c.save(f"{OUT}/chapter-07-tls-decryption-keylog-flow.svg")


def ch08():
    c = Canvas(960, 620,
        title="Chapter 8 Hands-On Lab: A Detection Script That Correctly Reports Nothing Once the Scan Pattern Is Removed",
        subtitle="An authorized SYN scan is detected by its high distinct-port count; the same script run against a sanitized capture finds no pattern left to detect",
        svg_title="Chapter 8 lab flow: a tshark-based port-scan detection one-liner validated against a real scan, then re-run against a sanitized capture with the scan noise removed",
        svg_desc="An authorized TCP SYN scan against a lab target is captured, and a tshark one-liner counting "
                  "SYN-only packets by source address identifies the scanning host with a count near the scanned "
                  "port range — clearly distinguishable from legitimate low-count traffic. The matched attempts "
                  "export to CSV, and a sanitized capture keeping only completed handshakes shows a markedly "
                  "lower packet count than the original. As a negative test, the same detection one-liner is run "
                  "against the sanitized file; it reports no scan-pattern match at all, confirming the half-open "
                  "SYNs were genuinely excluded by the sanitization step and the detection script correctly "
                  "reports nothing when the pattern it looks for is actually absent.")
    c.node_box(60, 130, 260, 110, "mgmt", [
        Line("Authorized SYN scan captured", 12.5, 700, "#111827"),
        Line("detection one-liner: scanning host", 10.5, 700, "#1d4ed8"),
        Line("identified by high SYN count", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 130, 240, 110, "alt", [
        Line("Sanitized capture", 12.5, 700, "#111827"),
        Line("only completed handshakes kept", 10.5, 400, "#374151"),
        Line("markedly lower packet count", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 185, 400, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("same detection script run", 10.5, 700, "#7f1d1d"),
        Line("against sanitized file", 10.5, 700, "#7f1d1d"),
        Line("→ no scan-pattern match", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 185, 700, 185, "warn")
    c.node_box(60, 300, 860, 90, "neutral", [
        Line("the detection script reports nothing once the half-open SYNs it looks for are genuinely gone —", 11.5, 400, "#374151"),
        Line("proof the sanitization step actually removed the scan noise rather than merely relabeling it.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 430, [("mgmt", "Raw capture with scan"), ("alt", "Hand-off-ready sanitized capture"), ("warn", "Confirmed clean re-scan")])
    c.save(f"{OUT}/chapter-08-portscan-detection-sanitization-flow.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: The Capstone — 'Occasionally Unreachable' Traced to a Scan, Confirmed by Isolating It",
        subtitle="DHCP, DNS, and TLS all check out cleanly; the detected scan explains the symptom, and removing the scan host's traffic makes the scan signature disappear",
        svg_title="Chapter 9 lab flow: an integrated investigation combining capture engineering, protocol analysis, and scan detection against one realistic 'slow and occasionally unreachable' scenario",
        svg_desc="A bounded ring-buffer capture on the lab host records a reproduced DHCP renewal, DNS "
                  "resolution, and HTTPS request alongside an authorized port scan simulating the reported "
                  "symptom. Protocol Hierarchy and Conversations give an initial picture before any filter is "
                  "written; DHCP DORA, DNS rcode==0, and the TLS handshake all confirm working as expected, "
                  "leaving the scan as the explanation once the Chapter 8 detection one-liner identifies the "
                  "scanning host by its high distinct-port count. As a negative test, the scanning host's traffic "
                  "is filtered out entirely and the detection command re-run against what remains; no high-count "
                  "scan signature remains, confirming the original detection was correctly attributable to the "
                  "scanning host specifically and not an artifact of the DHCP/DNS/HTTPS traffic itself. A short "
                  "written analysis report ties every finding together with a recommendation.")
    c.node_box(60, 130, 260, 120, "mgmt", [
        Line("Reproduced symptom capture", 12.5, 700, "#111827"),
        Line("DHCP renewal + DNS + HTTPS", 10.5, 400, "#374151"),
        Line("+ authorized port scan", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 130, 240, 120, "alt", [
        Line("Protocol checks all pass", 12.5, 700, "#111827"),
        Line("DORA complete, DNS rcode==0,", 10.5, 700, "#14532d"),
        Line("TLS handshake completes", 10.5, 400, "#374151"),
    ])
    c.connector(320, 190, 400, 190, "mgmt")
    c.node_box(700, 130, 220, 120, "warn", [
        Line("Scan identified", 12, 700, "#111827"),
        Line("high distinct-port SYN count", 10.5, 700, "#7f1d1d"),
        Line("explains \"occasionally", 10.5, 700, "#7f1d1d"),
        Line("unreachable\"", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 190, 700, 190, "warn")
    c.node_box(60, 320, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("scanning host's traffic filtered out entirely, detection command re-run against what remains", 11, 400, "#7f1d1d"),
        Line("no high-count scan signature remains — confirms the original detection was correctly attributable", 11, 400, "#7f1d1d"),
        Line("to the scanning host specifically, not an artifact of the DHCP/DNS/HTTPS traffic itself", 11, 400, "#7f1d1d"),
    ])
    c.node_box(60, 470, 860, 90, "neutral", [
        Line("a short written report ties capture scope, DHCP/DNS/TLS findings, the identified scan source, and a", 11.5, 400, "#374151"),
        Line("recommendation together — the deliverable this investigation was performed to produce.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 600, [("mgmt", "Reproduced investigation scope"), ("alt", "Confirmed-healthy protocols"), ("warn", "Root cause + isolation proof")])
    c.save(f"{OUT}/chapter-09-capstone-investigation-report-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
