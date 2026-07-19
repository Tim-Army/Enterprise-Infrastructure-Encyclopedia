# Chapter 08: Security Investigation, Command-Line Analysis, and Automation

## Learning Objectives

- Build `tshark`-based scripted workflows that extract, filter, and
  summarize fields across large captures without opening the GUI.
- Recognize the packet-level signatures of port scans, SYN floods, ARP/NDP
  spoofing, and DNS tunneling introduced conceptually in earlier chapters,
  and detect each with a specific filter or script.
- Use `editcap`, `mergecap`, and `capinfos` to split, combine, sanitize,
  and validate capture files as part of a repeatable pipeline.
- Export machine-readable output (CSV, JSON, PDML) for ingestion by
  external tools, SIEM pipelines, or further scripting.
- Sanitize a capture file before sharing it outside the investigating
  team.

## Theory and Architecture

Every chapter to this point has built filters and read fields
interactively in the Wireshark GUI. This chapter moves the same analysis
into scripted, repeatable, and automatable form using `tshark` and
Wireshark's companion command-line utilities — the toolset an analyst
actually reaches for once an investigation moves from "explore one
capture" to "check this pattern across every capture from this incident,"
or into a recurring detection pipeline.

### The command-line toolset

| Tool | Role |
| --- | --- |
| `tshark` | Full dissection engine at the command line; applies capture filters (`-f`), display filters (`-Y`), and field extraction (`-T fields -e <field>`) without a GUI. |
| `dumpcap` | Capture-only, covered in [Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md); no dissection. |
| `capinfos` | Reports file-level metadata: packet count, duration, file hashes ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)), encapsulation type. |
| `editcap` | Splits, filters, deduplicates, time-shifts, and sanitizes capture files without a live capture. |
| `mergecap` | Combines multiple capture files into one, chronologically interleaved by timestamp — the tool that makes correlating a dual-ended capture ([Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md)) practical. |
| `text2pcap` / `pcapng` builders | Converts hex dumps or other text representations into a valid capture file, occasionally useful for reconstructing packets described in a log or report. |

All of these tools share `epan`, the same dissection engine the GUI uses
([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)), so a `tshark` filter expression behaves identically to the
same expression typed into the Wireshark GUI's filter bar — a workflow can
be prototyped interactively ([Chapter 03](03-wireshark-interface-profiles-filters-and-analysis-workflows.md)) and then transcribed directly into
a script.

### Security investigation signatures

This chapter consolidates and operationalizes signatures introduced
conceptually in earlier chapters:

| Pattern | Earlier reference | Detection approach |
| --- | --- | --- |
| Port scan (many ports, one source) | [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md) (SYN/RST behavior) | High count of distinct destination ports from one source in a short window, each receiving SYN with no completing handshake. |
| SYN flood (many sources, one destination) | [Chapter 06](06-tcp-reliability-flow-control-and-performance-analysis.md) | High count of half-open connections to one destination from many distinct, often spoofed-looking source addresses. |
| ARP spoofing | [Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md) | One IP address associated with more than one MAC address outside a known failover pattern. |
| NDP spoofing | [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) | Same pattern as ARP spoofing, applied to Neighbor Advertisements. |
| Rogue DHCP server | [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) | More than one distinct source address issuing DHCP Offers on the same segment. |
| DNS tunneling | [Chapter 05](05-ipv6-icmpv6-udp-dhcp-and-dns-analysis.md) | High-entropy, unusually long subdomain labels queried at high frequency against a small set of domains. |
| ICMP tunneling/exfiltration | [Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md) | Unusually large or consistently-sized ICMP Echo payloads inconsistent with normal diagnostic use. |

Each of these is a hypothesis to confirm with evidence, not an automatic
verdict — a scripted match should feed a documented investigation
([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)) rather than an automatic conclusion.

## Design Considerations

- **Field extraction output should be script-consumable from the
  start.** Use `-T fields -e <field>` with explicit field names rather
  than parsing `tshark`'s default human-readable summary line — the
  default format is stable for reading, not for parsing, and can change
  wording between minor releases.
- **Large captures need staged filtering, not one giant expression.**
  Apply a capture filter at collection time ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)) where possible,
  then a coarse display filter, then a narrower one — running one complex
  expression against a multi-gigabyte file is slower and harder to debug
  than a staged pipeline of `editcap`/`tshark` steps.
- **Detection scripts need a baseline, not just a threshold.** A fixed
  numeric threshold (for example, "more than 50 SYNs per second") that
  works for one environment's normal traffic can be silent in a
  high-traffic environment or noisy in a quiet one; establish and revisit
  environment-specific baselines rather than reusing a generic number
  unchanged.
- **Sanitization changes evidentiary value.** A sanitized capture
  (IP/MAC addresses rewritten, payloads stripped) is appropriate for
  sharing with a vendor or in training material, but is no longer the
  original evidence — always sanitize a copy and retain the original,
  hashed and access-controlled per [Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md).
- **Output format should match the consumer.** CSV suits spreadsheet
  review and simple scripting; JSON/PDML suits ingestion by another
  program (a SIEM, a custom parser) that expects structured, nested data.

## Implementation and Automation

### Field extraction to CSV

```bash
tshark -r capture.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -E header=y -E separator=, -E quote=d \
  -e frame.time -e ip.src -e ip.dst -e tcp.dstport \
  > syn-attempts.csv
```

### Port scan detection

```bash
# Count distinct destination ports per source IP among unanswered SYNs.
tshark -r capture.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -e ip.src -e tcp.dstport \
  | sort | uniq | awk '{print $1}' | sort | uniq -c | sort -rn \
  | awk '$1 > 20 {print "Possible scan source:", $2, "(" $1 " distinct ports)"}'
```

### SYN flood detection

```bash
# Count half-open attempts (SYN with no matching SYN-ACK reply) per destination.
tshark -r capture.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -e ip.dst | sort | uniq -c | sort -rn | head -10
```

### ARP/NDP spoofing detection (extending [Chapter 04](04-ethernet-arp-ipv4-and-icmpv4-analysis.md)/05)

```bash
tshark -r capture.pcapng -Y "arp.opcode==2" -T fields \
  -e arp.src.proto_ipv4 -e arp.src.hw_mac | sort -u \
  | awk '{print $1}' | sort | uniq -d
```

Any IP address printed by the final `uniq -d` appeared with more than one
distinct MAC address in the ARP reply set and warrants manual review.

### DNS tunneling indicators

```bash
# Flag unusually long query names and their frequency, per domain.
tshark -r capture.pcapng -Y "dns.flags.response==0" -T fields -e dns.qry.name \
  | awk '{ print length($0), $0 }' | sort -rn | head -20
```

### JSON and PDML output for downstream tooling

```bash
tshark -r capture.pcapng -Y "http.response.code>=400" -T json > http-errors.json
tshark -r capture.pcapng -T pdml > full-dissection.pdml
```

`-T json` is generally preferred for SIEM/log-pipeline ingestion; `-T
pdml` preserves the complete field tree and is better suited to archival
or deep programmatic reprocessing.

### Splitting, merging, and validating capture files

```bash
# Split a large capture into 100 MB segments for easier handling.
editcap -c 100000 large-capture.pcapng segment.pcapng

# Merge two ends of a dual-ended capture, interleaved by timestamp.
mergecap -w merged.pcapng client-side.pcapng server-side.pcapng

# Validate file integrity and summarize before analysis.
capinfos -a -e -c -d large-capture.pcapng
```

### Sanitizing a capture for external sharing

```bash
# Strip application-layer payload beyond the first 68 bytes (headers only),
# reducing exposure of sensitive payload content while preserving headers
# needed for protocol-level review.
editcap -s 68 original.pcapng headers-only.pcapng

# Remove a specific sensitive host's traffic entirely before sharing.
tshark -r original.pcapng -Y "not ip.addr==10.0.20.99" -w filtered.pcapng
```

For address anonymization (rewriting real IP/MAC addresses to consistent
but non-identifying values) beyond simple truncation or exclusion, use a
dedicated sanitization tool designed for that purpose rather than manual
field editing, and always sanitize a working copy — never the original
evidence file ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)).

### Scheduling recurring detection

```bash
# /etc/cron.d/wireshark-scan-detect — run hourly against the current
# ring-buffer segment produced by the Chapter 02 continuous-capture service.
0 * * * * capture-svc /usr/local/bin/detect-port-scans.sh /var/capture/segment-a_*.pcapng
```

Wrap the detection one-liners above into a small script invoked this way
so scan and flood detection runs continuously against rotating capture
segments rather than requiring a manual review pass.

## Validation and Troubleshooting

- **`tshark -T fields` output has misaligned columns.** A field that is
  absent in some packets (for example, `tcp.dstport` on a non-TCP packet
  matched by a broad filter) shifts later columns; scope the display
  filter tightly enough that every matched packet actually has every
  extracted field, or use `-E occurrence=f` to control repeated-field
  behavior.
- **Detection script reports far more "scan sources" than expected.**
  Confirm the threshold accounts for legitimate multi-port clients (load
  balancer health checks, monitoring systems) before treating every match
  as malicious; add a documented allowlist rather than raising the
  threshold blindly.
- **`mergecap` output has packets in the wrong order.** `mergecap`
  interleaves strictly by the capture timestamp recorded in each source
  file; if the two capture hosts' clocks were not synchronized (Chapter
  02), the merged order will not reflect true wire order — resynchronize
  clocks (NTP/PTP) before a dual-ended capture where merge order matters.
- **Sanitized capture still contains sensitive data.** Confirm the
  sanitization step's scope matches the actual threat — truncating payload
  with `editcap -s` does not remove sensitive data that appears in header
  fields themselves (a hostname in SNI, a URI containing a token); review
  sanitized output with the same filters used in Chapters 04–07 before
  sharing it.
- **Scheduled detection job silently stops running.** Confirm the cron/
  systemd timer's log output separately from the ring-buffer capture
  service's own logs ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)) — a missing or rotated-away capture file
  the job expected to read is a common silent-failure cause.

## Security and Best Practices

- **Every automated detection output feeds a human-reviewed
  investigation, not an automatic block action**, unless that automation
  has been deliberately designed, tested, and approved as an active
  control — this chapter's scripts are detection and evidence-gathering
  tools, not enforcement mechanisms.
- **Store and version-control detection scripts, not just their
  output.** A script's logic is part of the evidentiary record when its
  output drives an investigative conclusion; keep it alongside the
  capture and its hash ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)).
- **Apply least privilege to scheduled/automated capture-analysis
  jobs.** The `capture-svc` account introduced in [Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md) should also
  run scripted detection — it needs read access to capture files, not
  broader system privileges.
- **Sanitize before sharing, every time, with no exceptions for "trusted"
  external parties.** A vendor support case or a training example is still
  external to the organization's access-control boundary.
- **Rate-limit and review automated alerts before they reach a wide
  distribution list.** A detection script with an untuned threshold
  generates alert fatigue quickly, which degrades response to the alerts
  that matter.

## References and Knowledge Checks

**References**

- Wireshark User's Guide, "tshark," "editcap," "mergecap," and
  "capinfos" reference chapters (current for the 4.4.x release line).
- `man tshark`, `man editcap`, `man mergecap`, `man capinfos`.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. Why does `tshark -T fields -e <field>` output suit scripting better
   than `tshark`'s default one-line-per-packet summary format?
2. What packet-level pattern distinguishes a port scan from a SYN flood,
   given that both involve unanswered SYN packets?
3. Why must clocks be synchronized between two capture hosts before
   `mergecap`'s chronological interleaving can be trusted?
4. Why does truncating payload with `editcap -s` fail to fully sanitize a
   capture that contains a sensitive value in a header field such as TLS
   SNI?

## Hands-On Lab

**Objective:** Build a `tshark`-based port-scan detection script, run it
against a captured scan, export findings to CSV, and sanitize the capture
before a simulated hand-off.

**Prerequisites**

- Wireshark and `tshark` installed with capture rights ([Chapter 01](01-packet-analysis-foundations-wireshark-installation-and-evidence.md)).
- `nmap` or an equivalent scanning tool, run only against a host the
  analyst owns or is explicitly authorized to scan (for example, a lab VM
  on an isolated segment).

**Steps**

1. Start a capture scoped to the lab target:

   ```bash
   tshark -i <INTERFACE_NUMBER> -f "host <LAB_TARGET_IP>" -w lab08.pcapng &
   ```

2. Run an authorized TCP SYN scan against the lab target:

   ```bash
   nmap -sS -p 1-200 <LAB_TARGET_IP>
   ```

3. Stop the capture:

   ```bash
   kill %1
   ```

4. Run the port-scan detection one-liner against the capture:

   ```bash
   tshark -r lab08.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
     -T fields -e ip.src -e tcp.dstport \
     | awk '{print $1}' | sort | uniq -c | sort -rn
   ```

   **Expected result:** the scanning host's IP address appears with a
   count near or above 200, matching the scanned port range — clearly
   distinguishable from any legitimate low-count traffic in the same
   capture.

5. Export the matched SYN attempts to CSV:

   ```bash
   tshark -r lab08.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
     -T fields -E header=y -E separator=, \
     -e frame.time -e ip.src -e ip.dst -e tcp.dstport \
     > lab08-syn-attempts.csv
   wc -l lab08-syn-attempts.csv
   ```

   **Expected result:** a CSV file with a header row and one row per SYN
   attempt.

6. Sanitize the capture by removing all traffic except the connections
   that actually completed a handshake, simulating a hand-off that
   excludes raw scan noise:

   ```bash
   tshark -r lab08.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==1" \
     -w lab08-sanitized.pcapng
   capinfos lab08.pcapng lab08-sanitized.pcapng
   ```

   **Expected result:** `capinfos` shows a markedly lower packet count in
   `lab08-sanitized.pcapng` than in the original, confirming the scan
   noise was excluded while any real completed connections remain.

7. **Negative test:** Run the same detection one-liner against the
   sanitized file:

   ```bash
   tshark -r lab08-sanitized.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
     -T fields -e ip.src | sort | uniq -c | sort -rn
   ```

   **Expected result:** no scan-pattern match (the half-open SYNs were
   excluded by the sanitization filter in step 6), confirming the
   detection script correctly reports nothing on traffic that no longer
   contains the pattern.

8. **Cleanup:** Remove all lab artifacts:

   ```bash
   rm -f lab08.pcapng lab08-sanitized.pcapng lab08-syn-attempts.csv
   ```

## Summary and Completion Checklist

`tshark` and its companion utilities extend every filter and field
introduced in Chapters 03 through 07 into scripted, repeatable, and
schedulable form — the difference between analyzing one capture by hand
and running a detection pipeline continuously against rotating capture
segments. Security investigation signatures (port scans, floods, spoofing,
tunneling) are hypotheses a script can flag efficiently, but confirming and
acting on them remains a human, documented investigative step. [Chapter 09](09-wca-101-certification-readiness-and-enterprise-capstone.md)
closes the volume by mapping this chapter's skills, and every prior
chapter's, to the WCA-101 certification blueprint and an integrated
enterprise capstone.

- [ ] Can extract fields from a capture to CSV/JSON using `tshark -T
      fields`/`-T json`.
- [ ] Can detect a port scan and a SYN flood pattern using scripted
      `tshark` filters.
- [ ] Can split, merge, and validate capture files with `editcap`,
      `mergecap`, and `capinfos`.
- [ ] Can sanitize a capture for external sharing and explain the limits
      of payload truncation alone.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
