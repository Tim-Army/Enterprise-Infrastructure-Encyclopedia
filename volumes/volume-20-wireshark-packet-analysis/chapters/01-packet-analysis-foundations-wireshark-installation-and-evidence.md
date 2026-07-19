# Chapter 01: Packet Analysis Foundations, Wireshark Installation, and Evidence

## Learning Objectives

- Explain what packet analysis reveals that logs, metrics, and flow records
  cannot, and where it fits in an enterprise troubleshooting and security
  workflow.
- Map Wireshark's components (Npcap/libpcap, dumpcap, the dissector engine,
  and the Qt GUI) to the OSI and TCP/IP layers they operate on.
- Install and correctly permission Wireshark and `tshark` on Windows, macOS,
  and Linux without requiring interactive root/administrator access for
  routine captures.
- Distinguish the legacy pcap and modern pcapng capture-file formats and
  choose correctly between them for a given use case.
- Apply evidentiary handling practices — hashing, access control, and
  documentation — to a packet capture that may become part of an incident
  record.

## Theory and Architecture

Packet analysis is the practice of capturing frames as they cross a network
segment and decoding them, layer by layer, to observe exactly what was
transmitted rather than what a device's logs claim was transmitted. Logs,
NetFlow/IPFIX records, and SNMP counters are all *summaries* produced by a
device's own software; a packet capture is a direct observation of the wire.
That distinction matters most when the question under investigation is
whether a device's own reporting can be trusted — a compromised host, a
misbehaving application, or a misconfigured middlebox will often report
itself correctly in logs while its actual traffic tells a different story.

Wireshark is the open-source (GPLv2) graphical front end most commonly used
for this work; `tshark` is its command-line sibling built from the same core
libraries. Both are consumers of a shared architecture:

| Component | Role |
| --- | --- |
| Npcap (Windows) / libpcap (Linux, macOS, BSD) | Kernel-adjacent capture driver that copies frames off a network interface into user space. |
| `dumpcap` | The privileged, minimal-surface capture process. It is the only Wireshark component that needs elevated capture privileges; it writes raw packets to disk or a pipe and does no protocol decoding. |
| Dissector engine (`epan`) | Parses captured bytes into a protocol tree, one dissector per protocol, chained by well-known ports, EtherTypes, or heuristics. |
| Qt GUI (`wireshark`) / `tshark` | Consume dissected packets for interactive or scripted analysis. Neither needs elevated privileges when reading from a file or from `dumpcap` output. |

Separating `dumpcap` from the GUI is a deliberate security boundary: the
component that touches the network with elevated privileges is small and
auditable, while the much larger and more frequently updated dissection and
UI code never runs as root/Administrator. This chapter's installation
guidance preserves that boundary; do not run the full Wireshark GUI as root
to work around a permissions problem — fix the underlying capture
permission instead (see Implementation and Automation, below).

### OSI and TCP/IP mapping

Wireshark's packet detail pane is organized as a stack of dissectors that
mirrors the layered reference models covered in [Volume II](../../volume-02-network-engineering-foundations/README.md). A typical HTTPS
frame captured on an Ethernet segment decodes as:

```text
Frame (capture metadata: length, timestamps, interface)
 └─ Ethernet II (L2: source/destination MAC, EtherType)
     └─ Internet Protocol Version 4 (L3: source/destination IP, TTL, protocol)
         └─ Transmission Control Protocol (L4: ports, sequence/ack, flags)
             └─ Transport Layer Security (L5/6: handshake or application data)
                 └─ Hypertext Transfer Protocol (L7: request/response)
```

Each layer in this tree is produced by an independent dissector; Wireshark's
protocol tree is therefore a live demonstration of encapsulation, not just a
teaching diagram. Understanding this chain is what lets an analyst read an
unfamiliar protocol stacked on top of familiar ones (for example, a
vendor-proprietary protocol riding over UDP) by reasoning from the known
layers inward.

### Capture-file formats

| Format | Extension | Characteristics |
| --- | --- | --- |
| pcap (legacy) | `.pcap` | Single link-layer type per file, microsecond or nanosecond timestamp resolution fixed at capture start, no comments or metadata blocks. Still the lowest common denominator for older tooling. |
| pcapng | `.pcapng` | Wireshark's default since Wireshark 2.x. Block-structured: supports multiple interfaces per file, per-packet interface description blocks, name resolution blocks, decryption secrets blocks (for example, stored TLS key logs), and free-text comments attached to individual packets. |

Enterprise capture engineering ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)) and TLS decryption workflows
([Chapter 07](07-application-protocol-tls-and-service-response-analysis.md)) both depend on pcapng-specific features — multi-interface
capture and embedded decryption secrets — so pcapng should be the default
target format unless a downstream tool specifically requires legacy pcap.

## Design Considerations

- **GUI vs. `tshark` vs. `dumpcap` for the task at hand.** Use `dumpcap` for
  unattended, long-running, or remote capture because it has the smallest
  attack surface and lowest resource footprint. Use `tshark` for scripted
  extraction, filtering, and statistics ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)). Reserve the full GUI
  for interactive human analysis — it is the heaviest of the three and is
  rarely appropriate to run on a production server.
- **Least-privilege capture access.** Every platform in this chapter is
  configured so that a non-administrative analyst account can capture
  without `sudo`/Administrator elevation for the GUI process itself. Grant
  capture rights through a dedicated group or capability, not by adding
  analysts to the local administrators/root-equivalent group.
- **Where analysis happens vs. where capture happens.** Capturing directly
  on a production system consumes CPU, memory, and disk I/O that can perturb
  the very performance issue being investigated. Prefer capturing on a
  dedicated collection point ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md): taps, mirrors) and analyzing on a
  separate workstation whenever the topology allows it.
- **Storage and retention.** A saturated 1 Gbps link can produce well over
  400 GB per hour of capture data. Decide retention windows and rotation
  policy ([Chapter 02](02-enterprise-capture-engineering-taps-mirrors-and-ring-buffers.md)) before a capture starts, not after a disk fills.
- **Licensing and redistribution.** Wireshark is GPLv2-licensed and free to
  install and redistribute inside an enterprise; no licensing gate exists
  for the tool itself, though captured traffic may still be subject to the
  organization's own data-handling and privacy policies.

## Implementation and Automation

This chapter's baseline is Wireshark 4.4.x, per
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md). Menu paths and package
names below are current for that release line; always confirm against the
installed version with **Help > About Wireshark**.

### Windows: Npcap-backed install

1. Install Wireshark from the official installer, which bundles the Npcap
   driver. During setup, accept the Npcap installation step and enable
   **"Support raw 802.11 traffic (and monitor mode) for wireless adapters"**
   only if wireless capture is required.
2. During the Npcap install screen, enable **"Restrict Npcap driver's access
   to Administrators only"** as `unchecked` if non-administrative analysts
   must capture — leaving it checked forces every capture session to run
   elevated.
3. Verify the driver and list interfaces without launching the GUI:

   ```powershell
   "C:\Program Files\Wireshark\tshark.exe" -D
   ```

### macOS: Homebrew install and ChmodBPF

1. Install via Homebrew:

   ```bash
   brew install --cask wireshark
   ```

2. macOS gates raw packet capture behind `/dev/bpf*` device permissions. The
   Wireshark installer offers to install the **ChmodBPF** launch daemon,
   which creates an `access_bpf` group and adjusts `/dev/bpf*` permissions on
   every boot. Add analyst accounts to that group:

   ```bash
   sudo dseditgroup -o edit -a "$(whoami)" -t user access_bpf
   ```

3. Log out and back in for group membership to take effect, then confirm:

   ```bash
   tshark -D
   ```

### Linux (Debian/Ubuntu family): capability-based install

1. Install the package and let the installer prompt for non-root capture:

   ```bash
   sudo apt update
   sudo apt install -y wireshark
   ```

2. If prompted **"Should non-superusers be able to capture packets?"**,
   answer **Yes**. This reconfigures `dumpcap` to run with file capabilities
   rather than setuid-root:

   ```bash
   sudo dpkg-reconfigure wireshark-common
   ```

3. Add the analyst account to the `wireshark` group created by the package,
   then start a new login session:

   ```bash
   sudo usermod -aG wireshark "$(whoami)"
   ```

4. Confirm the capability is set correctly on `dumpcap` (expect
   `cap_net_admin,cap_net_raw=eip`):

   ```bash
   getcap /usr/bin/dumpcap
   ```

5. If the package installer's prompt was skipped, apply the same
   configuration manually:

   ```bash
   sudo groupadd -f wireshark
   sudo usermod -aG wireshark "$(whoami)"
   sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap
   sudo chgrp wireshark /usr/bin/dumpcap
   sudo chmod 750 /usr/bin/dumpcap
   ```

### First capture and sanity check

Regardless of platform, confirm the install with a short, scoped capture
before relying on it for investigative work:

```bash
tshark -D
# 1. en0
# 2. lo0
# ...

tshark -i 1 -c 20 -w /tmp/first-capture.pcapng
capinfos /tmp/first-capture.pcapng
```

`capinfos` reports packet count, capture duration, and — critically for
evidentiary use — file hashes, covered next.

## Validation and Troubleshooting

- **"You don't have permission to capture on that device" (Linux).** Almost
  always a stale group membership: `groups` in the current shell will not
  show a group added after login. Log out and back in, or run `newgrp
  wireshark` for the current shell, then retry.
- **Npcap loopback capture returns nothing (Windows).** Windows loopback
  traffic requires Npcap's separate loopback adapter (`Npcap Loopback
  Adapter`), listed as its own interface in `tshark -D`; capture on that
  interface rather than the physical NIC to see `localhost` traffic.
- **`dumpcap` capability lost after a package upgrade (Linux).** Package
  upgrades sometimes reset file capabilities set outside the package
  manager. Re-run `dpkg-reconfigure wireshark-common` (Debian/Ubuntu) after
  upgrades, or add a post-upgrade hook that reapplies `setcap`.
- **No interfaces listed at all.** Confirm the capture driver is actually
  running: `sc query npcap` (Windows), `kextstat | grep -i bpf` or check
  ChmodBPF daemon status (older macOS), or `lsmod | grep -i packet`-style
  checks are not meaningful on Linux since `libpcap` uses `AF_PACKET`
  sockets directly — instead confirm the interface is up with `ip link show`.
- **GUI runs but freezes on a large file.** This is a resource, not a
  permissions, problem. Apply a display filter before loading fully, or
  split the file first with `editcap` ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md)) rather than loading an
  oversized capture into the GUI unfiltered.

## Security and Best Practices

- **Treat packet captures as sensitive data by default.** A capture can
  contain credentials sent in cleartext protocols, session tokens, internal
  hostnames, and PII in application payloads. Apply the same access control
  and retention discipline used for log data containing secrets.
- **Hash every capture intended as evidence at the moment of collection.**

  ```bash
  sha256sum incident-2026-0718-capture.pcapng > incident-2026-0718-capture.pcapng.sha256
  ```

  Record the hash, the collecting analyst, the capture point, and the start
  and end timestamps in an incident record before the file is copied
  anywhere else. Recompute and compare the hash after every transfer.
- **Preserve chain of custody.** Store the original capture read-only, work
  from a copy, and log every copy operation (who, when, where) if the
  capture may support a personnel action, legal hold, or law-enforcement
  referral. [Volume X](../../volume-10-enterprise-cybersecurity/README.md) (Enterprise Cybersecurity) covers formal evidence
  handling in depth; this volume assumes those practices apply to packet
  evidence specifically.
- **Scope captures to the minimum necessary.** Use a capture filter (Chapter
  02) to exclude unrelated hosts and protocols rather than capturing an
  entire segment and filtering later — this both reduces exposure of
  unrelated users' traffic and reduces storage/handling burden.
- **Never run the Wireshark GUI as root/Administrator to bypass a
  permissions problem.** Doing so runs the entire dissection and UI code
  base — the largest and most frequently patched part of Wireshark —  with
  full system privileges. Fix the underlying capture-group or capability
  configuration instead.
- **Encrypt captures at rest** when stored outside a controlled evidence
  system, and strip or redact captures before sharing with vendors or
  external parties ([Chapter 08](08-security-investigation-command-line-analysis-and-automation.md) covers `tshark`-based sanitization).

## References and Knowledge Checks

**References**

- Wireshark User's Guide, "Building and Installing Wireshark" and
  "Capture Privileges" chapters (current for the 4.4.x release line).
- Npcap documentation, "Restricting Npcap driver's access."
- `man dumpcap`, `man capinfos` (Wireshark 4.4.x manual pages).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  encyclopedia's dated baseline for Wireshark 4.4.x.

**Knowledge checks**

1. Why does `dumpcap` run as a separate, minimal process instead of folding
   capture privileges into the main Wireshark GUI binary?
2. What capability set does `setcap` grant to `dumpcap` on Linux, and why is
   `cap_net_raw` alone insufficient for most interfaces?
3. Name two features pcapng supports that legacy pcap does not, and explain
   why one of them matters for TLS decryption workflows.
4. What two pieces of information should be recorded at the moment a
   capture is hashed for evidentiary purposes?

## Hands-On Lab

**Objective:** Install Wireshark and `tshark` with non-administrative
capture rights, take a short baseline capture, and produce a hashed,
documented evidence-handling record for it.

**Prerequisites**

- A workstation running Windows, macOS, or Linux with local administrative
  access for the one-time installation step.
- Network connectivity sufficient to generate a small amount of traffic
  (a web request is enough).

**Steps**

1. Install Wireshark using the platform-specific procedure in
   Implementation and Automation, above, and configure non-administrative
   capture access (Npcap unrestricted, ChmodBPF `access_bpf` group, or
   Linux `wireshark` group + capabilities).
2. Confirm capture rights without elevation:

   ```bash
   tshark -D
   ```

   **Expected result:** a numbered interface list is returned without a
   permission error and without requiring `sudo`/Administrator.

3. Take a short, scoped baseline capture while generating a small amount of
   traffic (for example, browsing to one site):

   ```bash
   tshark -i <INTERFACE_NUMBER> -a duration:30 -w lab01-baseline.pcapng
   ```

4. Inspect the capture's summary metadata:

   ```bash
   capinfos lab01-baseline.pcapng
   ```

   **Expected result:** `capinfos` reports a pcapng file, a packet count
   greater than zero, and a capture duration close to 30 seconds.

5. Hash the capture and record the evidence metadata:

   ```bash
   sha256sum lab01-baseline.pcapng > lab01-baseline.pcapng.sha256
   date -u +"%Y-%m-%dT%H:%M:%SZ" > lab01-baseline.collected-at.txt
   ```

6. **Negative test:** Attempt a capture without the configured group
   membership or Npcap permission (for example, from a second, unmodified
   user account) and confirm it is denied:

   ```bash
   tshark -i <INTERFACE_NUMBER> -c 5
   ```

   **Expected result:** a permission-denied error, demonstrating that
   capture rights are correctly scoped to the intended group rather than
   open to every local account.

7. **Cleanup:** Remove the lab capture and its evidence artifacts once the
   exercise is reviewed:

   ```bash
   rm -f lab01-baseline.pcapng lab01-baseline.pcapng.sha256 lab01-baseline.collected-at.txt
   ```

## Summary and Completion Checklist

Packet analysis provides ground truth that logs and summaries cannot, and
Wireshark's split architecture — a minimal-privilege `dumpcap` capture
process feeding an unprivileged dissection and analysis layer — is designed
to make that ground truth safe to collect without granting broad system
access. Installing correctly means configuring least-privilege capture
access once per platform, defaulting to pcapng, and treating every capture
as potentially sensitive evidence from the moment it is written to disk.

- [ ] Can explain what a packet capture reveals that logs and flow records
      cannot.
- [ ] Can map a captured frame's protocol tree to OSI/TCP-IP layers.
- [ ] Installed Wireshark and `tshark` with non-administrative capture
      rights on at least one platform.
- [ ] Can explain the difference between pcap and pcapng and when each
      applies.
- [ ] Can hash and document a capture for evidentiary handling.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
