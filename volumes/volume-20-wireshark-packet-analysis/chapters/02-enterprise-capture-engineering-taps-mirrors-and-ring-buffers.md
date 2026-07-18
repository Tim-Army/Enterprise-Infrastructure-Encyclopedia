# Chapter 02: Enterprise Capture Engineering, Taps, Mirrors, and Ring Buffers

## Learning Objectives

- Compare SPAN/mirror ports and TAPs as capture points and select the
  correct one for a given topology, duplex requirement, and budget.
- Explain why an aggregating TAP or oversubscribed SPAN port silently drops
  packets under load, and design a capture point that avoids that failure
  mode.
- Distinguish capture filters (BPF, applied by `dumpcap` before packets are
  written) from display filters (Chapter 03, applied after capture) and
  choose correctly between them.
- Configure `dumpcap` ring-buffer rotation for unattended, storage-bounded,
  continuous capture.
- Capture from a remote or headless host without installing the full
  Wireshark GUI on that host.

## Theory and Architecture

Enterprise capture engineering is the discipline of getting the right
traffic to the right capture point without perturbing the network being
observed or dropping the packets that matter. Chapter 01 covered installing
and permissioning Wireshark and `tshark`; this chapter covers where those
tools should point and how they should be run when a human is not sitting
in front of the GUI watching packets arrive live.

### SPAN/mirror ports vs. TAPs

| Method | Mechanism | Strengths | Weaknesses |
| --- | --- | --- | --- |
| SPAN / mirror port (Cisco `monitor session`, generic "port mirroring") | The switch's ASIC copies frames from one or more source ports or VLANs to a destination port, in software/ASIC alongside its normal forwarding work. | No additional hardware; reconfigurable in minutes; can mirror multiple sources to one destination. | Mirrored traffic is lowest switching priority — under sustained load the switch silently drops mirrored copies before it drops production traffic. Can alter timing (inter-packet gaps) and, on some platforms, strips or rewrites VLAN tags and corrupted-frame indicators. |
| TAP (Test Access Point), regeneration/passive | A physical inline device that splits the optical or electrical signal, delivering an exact copy — including Layer 1 errors — to one or more monitor ports. | Full fidelity, including frames a switch would never forward (runts, CRC errors, jabber). No impact on switch CPU/ASIC. Fails safe (many passive TAPs pass link traffic even on power loss). | Requires a physical break in the link to insert; one TAP per link; adds a hardware asset to inventory and a fiber/copper budget line. |
| TAP, aggregating | A TAP that merges the Tx and Rx directions of a full-duplex link onto a single monitor output. | One monitor port instead of two; convenient for tools with a single capture NIC. | The merged output must carry both directions at once. On a full-duplex link running above roughly 50% utilization in each direction, the aggregated output can exceed the physical capacity of the single monitor port, and the TAP drops packets exactly like an oversubscribed SPAN port. |

The failure mode to internalize: **both an oversubscribed SPAN port and an
oversubscribed aggregating TAP drop packets without any protocol-level
signal that they did so.** No retransmission is triggered on the monitor
path because the production link is not affected — the drop is invisible
except as a gap when the analyst later notices sequence numbers or frame
counts that do not add up. Chapter 06 explains how to distinguish a
capture-point drop from a real network-induced retransmission using TCP
sequence analysis; the design decision that prevents the ambiguity is made
here, before capture starts.

### Network packet brokers

At scale, taps and SPAN ports feed a network packet broker (NPB) — for
example, a Gigamon GigaVUE fabric (Volume XVIII, Gigamon Network
Visibility) — rather than feeding an analysis tool directly. An NPB
aggregates multiple capture points, deduplicates copies of the same packet
arriving from redundant paths, filters and load-balances traffic across
multiple monitor-port destinations, and can strip encapsulation (VXLAN,
GTP) before delivery. Wireshark and `tshark` are consumers at the end of
that fabric, not participants in it; this chapter's ring-buffer and
capture-filter guidance applies identically whether the capture NIC is
plugged into a TAP, a SPAN port, or an NPB tool port.

### Capture filters vs. display filters

Wireshark exposes two independent filtering layers that are frequently
confused:

| | Capture filter | Display filter |
| --- | --- | --- |
| Engine | Berkeley Packet Filter (BPF), the same syntax `tcpdump` uses | Wireshark's own dissector-aware expression language (Chapter 03) |
| Applied by | `dumpcap`, before a packet is written to disk or memory | `wireshark`/`tshark`, after the packet is dissected |
| Effect | Packets that do not match are **never captured** — they cannot be recovered later | Packets that do not match are hidden from view but remain in the file |
| Syntax example | `host 10.0.20.15 and tcp port 443` | `ip.addr==10.0.20.15 && tcp.port==443` |

Because a capture filter permanently discards non-matching traffic, use it
only when the exclusion is certain and durable (for example, excluding a
known-noisy backup VLAN from a segment-wide capture). When in doubt,
capture broadly with at most a coarse capture filter and narrow the view
with a display filter instead — a display filter mistake costs a
re-analysis; a capture filter mistake costs the capture itself.

## Design Considerations

- **Match capture point to the question.** A performance problem between a
  client and a server is best captured at both ends simultaneously (or at
  the point closest to the reported symptom) so the analyst can compare
  timestamps across the path; a broad security sweep is better served by a
  TAP or SPAN at a chokepoint such as a core switch or firewall interface.
- **Duplex and bandwidth budget.** Size the monitor port and capture NIC for
  the sum of both directions of the source link(s), not just one direction.
  A mirrored or aggregated 10 Gbps full-duplex link can require up to 20
  Gbps of monitor-side capacity at peak.
- **Storage budget drives ring-buffer sizing.** A saturated 1 Gbps link can
  produce roughly 450 GB/hour of pcapng data before compression. Calculate
  `file size × file count` against available disk before starting an
  unattended capture, and prefer time-bounded rotation (`-b duration:`) when
  the retention requirement is expressed in hours rather than gigabytes.
- **VLAN and encapsulation visibility.** Confirm whether the chosen SPAN or
  TAP configuration preserves 802.1Q tags and any tunnel encapsulation
  (VXLAN, GRE, MPLS) the analysis will depend on; some switch platforms
  strip the tag that identifies which VLAN a mirrored frame came from.
- **Placement changes the timestamp reference.** Every capture point applies
  its own arrival timestamp; comparing captures from two points (Chapter 06,
  Chapter 07) requires either synchronized clocks (NTP/PTP) on both capture
  hosts or an explicit acknowledgment that cross-capture timing deltas
  include clock skew.
- **Unattended capture needs a supervision plan.** A `dumpcap` process left
  running without rotation limits will eventually fill its disk; a process
  left running without a stop condition will outlive the investigation it
  was started for. Every continuous capture needs an explicit rotation,
  retention, and termination policy before it starts.

## Implementation and Automation

This chapter's examples target Wireshark/`dumpcap` 4.4.x, per
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md), run from the
non-administrative capture configuration established in Chapter 01.

### Writing a capture filter

Capture filters use BPF primitives (`host`, `net`, `port`, `portrange`,
`and`/`or`/`not`), combinable into compound expressions:

```bash
# Capture only traffic to/from one host, excluding SSH management traffic.
dumpcap -i eth0 -f "host 10.0.20.15 and not port 22" -w host-capture.pcapng

# Capture only a subnet's traffic on standard web ports.
dumpcap -i eth0 -f "net 10.0.20.0/24 and (port 80 or port 443)" -w web-capture.pcapng
```

Validate a capture filter's syntax before a long-running capture depends on
it:

```bash
dumpcap -i eth0 -f "host 10.0.20.15" -c 1
```

### Ring-buffer capture for continuous collection

`dumpcap`'s ring buffer rotates through a fixed set of files, deleting the
oldest when the set is full, bounding total disk usage regardless of how
long the capture runs:

```bash
dumpcap -i eth0 \
  -b filesize:512000 \
  -b files:20 \
  -w /var/capture/segment-a.pcapng
```

This example bounds total usage to roughly 10 GB (20 files × 512 MB) and
produces sequentially numbered files
(`segment-a_00001_20260718120000.pcapng`, and so on). Rotate on elapsed
time instead of size when the retention requirement is expressed in hours:

```bash
dumpcap -i eth0 \
  -b duration:3600 \
  -b files:24 \
  -w /var/capture/hourly.pcapng
```

This retains the most recent 24 hours as 24 hourly files.

### Running continuous capture as a supervised service

Run long-lived capture under a process supervisor rather than a manually
started foreground process so it restarts after a host reboot and logs its
own health. On a Linux capture host:

```ini
# /etc/systemd/system/dumpcap-segment-a.service
[Unit]
Description=Continuous ring-buffer capture on eth0
After=network-online.target

[Service]
ExecStart=/usr/bin/dumpcap -i eth0 -b filesize:512000 -b files:20 \
  -w /var/capture/segment-a.pcapng
User=capture-svc
Group=wireshark
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now dumpcap-segment-a.service
sudo systemctl status dumpcap-segment-a.service
```

Running the service as a dedicated `capture-svc` account in the `wireshark`
capability group (Chapter 01) keeps the continuous capture process off both
`root` and any interactive analyst account.

### Capturing from a remote or headless host

Two supported patterns avoid installing the full GUI on a production or
remote host:

```bash
# Pattern 1: SSH pipe — dumpcap runs remotely, packets stream to a local
# Wireshark GUI over the SSH tunnel and are never written to disk remotely.
ssh analyst@remote-host \
  "dumpcap -i eth0 -P -w -" | wireshark -k -i -

# Pattern 2: rpcapd — the remote packet capture daemon exposes an
# interface for direct remote capture from Wireshark's Capture > Options
# dialog, authenticated separately from SSH.
ssh analyst@remote-host "rpcapd -n -p 2002"
```

Prefer the SSH pipe pattern where SSH access already exists — it reuses an
already-audited access path and avoids running an additional listening
daemon (`rpcapd`) on the target host.

## Validation and Troubleshooting

- **Packet counts don't match between the switch's interface counters and
  the capture file.** Check the SPAN/mirror session's own drop counters
  first (for example, Cisco `show monitor session <ID>`); an oversubscribed
  destination port drops silently and the switch itself usually still
  reports the drop count even though Wireshark cannot see the missing
  frames.
- **`dumpcap` reports "packets dropped."** Run with `-S` for a live capture
  summary, or inspect the pcapng interface statistics block after the fact
  with `capinfos -A file.pcapng`. Drops here indicate the capture host — not
  the network — could not keep up; reduce scope with a tighter capture
  filter, capture to a faster disk, or split the capture across two NICs.
- **Aggregating TAP shows drops only during business-hours peaks.** This is
  the expected signature of an aggregating TAP exceeding its monitor-port
  capacity under combined bidirectional load; replace it with a
  regeneration TAP feeding two monitor ports (one per direction) or an NPB
  tool port sized for full-duplex aggregate throughput.
- **VLAN tag missing from mirrored frames.** Some switch platforms strip
  the 802.1Q tag on frames mirrored from an access port; mirror from the
  trunk side of the path, or confirm the platform's documented mirroring
  behavior for tagged frames before relying on `vlan.id` filters (Chapter
  04) against that capture point.
- **Ring buffer fills faster than expected.** Recalculate `file size × file
  count` against observed throughput rather than assumed throughput; a
  burst of replication or backup traffic can inflate the true capture rate
  well above steady-state utilization figures pulled from interface
  counters.

## Security and Best Practices

- **Treat TAP and SPAN destination ports as sensitive infrastructure.**
  A monitor port carries a full copy of production traffic, often including
  cleartext protocols; restrict physical and logical access to capture
  hosts and NPB tool ports as tightly as the production segments they
  mirror.
- **Scope capture filters and NPB rules to the minimum needed for the
  investigation**, both to reduce exposure of unrelated users' traffic and
  to reduce the volume of sensitive data that must later be retained,
  hashed, and eventually destroyed (Chapter 01).
- **Disable or physically secure unused SPAN sessions and TAP monitor
  ports.** An idle mirror session pointed at a forgotten port is an
  unmonitored eavesdropping path if an unauthorized device is connected to
  it later.
- **Encrypt ring-buffer storage at rest** on capture hosts that are not
  inside a physically controlled evidence room, and apply the same
  retention-and-destruction schedule to rotated-out files as to any other
  capture (Chapter 01).
- **Log every remote-capture session.** SSH-piped and `rpcapd` capture
  sessions should be attributable to a named analyst and a stated
  investigation, consistent with the chain-of-custody practice established
  in Chapter 01.

## References and Knowledge Checks

**References**

- Wireshark User's Guide, "Capturing Live Network Data" and "Remote
  Packet Capture" chapters (current for the 4.4.x release line).
- `man dumpcap`, `man pcap-filter` (BPF syntax reference).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.
- Volume XVIII (Gigamon Network Visibility) — network packet broker
  architecture and deployment.

**Knowledge checks**

1. Why can an aggregating TAP drop packets even though the production link
   it monitors never drops a frame?
2. What is the practical difference between a capture filter and a display
   filter, and why does that difference argue for capturing broadly and
   filtering narrowly at display time?
3. Name two `dumpcap` ring-buffer rotation triggers and describe a
   retention requirement each is best suited for.
4. Why is a systemd-supervised `dumpcap` service preferable to a manually
   started foreground capture for continuous, unattended collection?

## Hands-On Lab

**Objective:** Configure a storage-bounded ring-buffer capture with a
capture filter, verify rotation behavior, and confirm that unwanted
traffic is excluded at capture time.

**Prerequisites**

- Completion of Chapter 01's installation and non-administrative capture
  configuration.
- At least 200 MB of free disk space in a working directory.

**Steps**

1. Create a working directory for the lab capture:

   ```bash
   mkdir -p ~/lab02-capture && cd ~/lab02-capture
   ```

2. Identify the active capture interface:

   ```bash
   tshark -D
   ```

3. Start a ring-buffer capture bounded to five 2 MB files, with a capture
   filter that excludes SSH management traffic:

   ```bash
   dumpcap -i <INTERFACE_NUMBER> -f "not port 22" \
     -b filesize:2000 -b files:5 -w lab02.pcapng
   ```

4. While the capture runs, generate enough traffic to force at least one
   rotation (for example, download a multi-megabyte file or browse several
   pages), then stop `dumpcap` with `Ctrl+C` after at least two rotation
   files appear:

   ```bash
   ls -la lab02_*.pcapng
   ```

   **Expected result:** multiple sequentially timestamped files, and no
   more than five present at once (older files are deleted as new ones are
   written once the ring fills).

5. Confirm the capture filter excluded SSH traffic even though the SSH
   session used to run these commands (if remote) was active throughout:

   ```bash
   tshark -r lab02_00001_*.pcapng -Y "tcp.port==22"
   ```

   **Expected result:** no output — port 22 traffic was never captured,
   because the BPF capture filter discarded it before it reached disk.

6. **Negative test:** Attempt the same filter check for a protocol that was
   *not* excluded (for example, DNS):

   ```bash
   tshark -r lab02_00001_*.pcapng -Y "dns"
   ```

   **Expected result:** DNS packets appear if any were generated during the
   capture window, confirming the capture filter's exclusion was specific
   to port 22 rather than accidentally broad.

7. **Cleanup:** Remove the lab capture files:

   ```bash
   cd ~ && rm -rf ~/lab02-capture
   ```

## Summary and Completion Checklist

Enterprise capture engineering is a set of decisions made before a single
packet is captured: where the tap point sits relative to the question being
asked, whether that point can carry full-duplex traffic without silent
loss, what capture filter (if any) permanently excludes noise, and how
long unattended capture is allowed to run before rotation reclaims disk.
Getting these decisions right prevents the two failure modes that undermine
an investigation after the fact — a capture point that silently dropped the
packets that mattered, and a capture host that filled its disk or ran
unsupervised past its useful window.

- [ ] Can compare SPAN/mirror ports and TAPs and identify when each
      silently drops packets under load.
- [ ] Can explain the architectural difference between capture filters and
      display filters.
- [ ] Configured a `dumpcap` ring buffer with a bounded file count and
      size.
- [ ] Configured and validated a capture filter that excludes unwanted
      traffic.
- [ ] Can describe at least one supervised (systemd) and one remote
      (SSH-piped or `rpcapd`) capture pattern.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
