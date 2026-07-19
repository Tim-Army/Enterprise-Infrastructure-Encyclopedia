# Chapter 2: Block Storage and Storage Area Networks

![Lab topology for this chapter: storage01 exposes a 2 GB fileio-backed LUN through target IQN iqn.2026-07.lab.example:storage01, with an ACL for client01's IQN and CHAP credentials on portal 3260; client01 discovers and logs in, reaching state LOGGED_IN with a new block device matching the 2 GB LUN. As a negative test, client01 logs out, sets an intentionally wrong CHAP password, and attempts to log back in; the login fails with an authentication error and journalctl shows the rejected CHAP negotiation, confirming the ACL and CHAP configuration actively enforce authentication.](../../../diagrams/volume-06-enterprise-storage-data-protection/chapter-02-iscsi-chap-auth-topology.svg)

*Figure 2-1. Topology used throughout this chapter's Hands-On Lab: an iSCSI target/initiator pair authenticated with CHAP, verified positive and then tested against a wrong password.*

## Learning Objectives

- Compare Fibre Channel, iSCSI, FCoE, and NVMe-oF as SAN transports and
  identify which is appropriate for a given data center design.
- Explain SAN fabric topology, zoning, and LUN masking as layered access
  controls, and describe how each restricts host-to-storage visibility.
- Describe storage array front-end/back-end architecture and how port count,
  cache, and back-end fabric bandwidth bound array performance.
- Configure a basic iSCSI target and initiator relationship on Linux and
  verify session establishment.
- Diagnose common SAN failure modes: fabric login failures, zoning
  misconfiguration, LUN masking errors, and path loss.
- Apply zoning, masking, and authentication as layered security controls
  around block storage.

## Theory and Architecture

Block storage delivers a raw, addressable volume — a **LUN** (Logical Unit
Number) — to a host over a dedicated storage network. The host's own
filesystem, volume manager, or hypervisor owns everything above the block
layer; the SAN's job is reliable, low-latency, lossless transport between
initiator (host) and target (array).

### SAN transports

| Transport | Physical layer | Typical use | Key characteristic |
| --- | --- | --- | --- |
| Fibre Channel (FC) | Dedicated FC switches and HBAs, 16/32/64 Gb | Traditional enterprise SAN | Purpose-built, lossless fabric; separate physical network from Ethernet |
| iSCSI | Standard Ethernet, TCP/IP | General-purpose SAN, cost-sensitive deployments | Runs on commodity Ethernet; relies on TCP for reliability |
| FCoE | Converged Ethernet (DCB/lossless Ethernet) | Converged data center fabrics | Encapsulates FC frames on Ethernet; requires Data Center Bridging |
| NVMe-oF (FC-NVMe, NVMe/TCP, NVMe/RoCE) | FC fabric or Ethernet (RDMA or TCP) | Latency-sensitive, flash-native platforms | Extends the NVMe command set (deeper queues, lower protocol overhead) across a fabric |

Fibre Channel remains the reference point for lossless, deterministic-latency
block transport: a purpose-built fabric with buffer-to-buffer credit flow
control means frames are never dropped due to congestion, only paused. iSCSI
trades that determinism for using existing Ethernet infrastructure and IP
routing, at the cost of depending on TCP's congestion control and retransmit
behavior under load — acceptable for most workloads, but historically a
harder sell for the most latency-sensitive tier-1 databases. FCoE attempted to
converge FC and Ethernet onto one physical fabric using Data Center Bridging
extensions (Priority Flow Control, Enhanced Transmission Selection) to make
Ethernet lossless enough for FC traffic; it remains in use in converged
designs but has been substantially overtaken by native high-speed Ethernet
and NVMe/TCP. NVMe-oF is the current performance frontier: it extends NVMe's
massively parallel queuing model (up to 64K queues, 64K commands per queue,
versus SCSI's much shallower queuing) across a fabric, whether that fabric is
FC, RDMA-capable Ethernet (RoCE), or plain TCP — NVMe/TCP in particular has
become popular because it delivers most of NVMe-oF's latency benefit on
ordinary Ethernet without requiring RDMA-capable NICs end to end.

### Fabric topology

A resilient SAN design uses **dual fabrics**: two physically and logically
independent switch fabrics (commonly labeled Fabric A and Fabric B), with
every host and array connected to both. This is not redundancy within a
fabric — it is redundancy achieved by never having a single fabric be a
single point of failure. Within each fabric, larger designs use a **core-edge**
topology: edge switches aggregate host and storage connections, and a
higher-bandwidth core switch (or pair) interconnects the edges via
Inter-Switch Links (ISLs). ISL oversubscription — the ratio of edge-facing
bandwidth to core-facing bandwidth — is a first-order capacity planning input;
an under-provisioned ISL becomes a fabric-wide bottleneck invisible to any
single host's own port statistics.

### Zoning and LUN masking

Two independent layers restrict which initiators can see which targets:

- **Zoning** operates at the fabric switch level and controls which World
  Wide Names (WWNs) or ports can communicate at all. **Single-initiator,
  single-target (1:1) zoning** — one host HBA port zoned with exactly one
  array target port per zone — is the standard practice: it minimizes the
  registered state change notification (RSCN) blast radius when any device
  in a zone changes state, so an unrelated host is never woken up to
  re-evaluate paths because of an unrelated LUN or host event elsewhere in
  the fabric.
- **LUN masking** operates at the storage array and controls which specific
  LUNs a zoned-and-visible initiator is actually permitted to address. Zoning
  without masking still exposes every LUN on the target port to every zoned
  initiator; masking is the layer that actually enforces "this host may see
  only its own volumes."

Both layers are required. Zoning alone is a network-visibility control;
masking alone (without zoning) still leaves the fabric able to route traffic
between hosts and arrays that have no business communicating, which is both a
security exposure and an unnecessary source of fabric-wide RSCN traffic.

### Array front-end/back-end architecture

A dual-controller array exposes **front-end ports** (the FC/iSCSI/NVMe-oF
targets hosts connect to) backed by **controller cache** and **back-end
connectivity** to the physical drives or, in NVMe-native arrays, an internal
NVMe fabric. Performance headroom is bounded by whichever layer saturates
first: front-end port bandwidth, controller CPU (for inline
dedup/compression/encryption), cache size and destage rate, or back-end
drive/fabric bandwidth. A common design mistake is sizing front-end port
count for connectivity alone and ignoring that aggregate front-end
throughput must still fit through the same controller and back-end
resources — adding host paths does not add array performance.

### iSCSI session model

iSCSI establishes a **session** between an initiator's IQN (iSCSI Qualified
Name) and a target's IQN over one or more TCP connections. Discovery happens
via SendTargets against a discovery portal or via an iSNS server in larger
environments; authentication uses CHAP (Challenge-Handshake Authentication
Protocol), optionally mutual (both sides authenticate each other). Because
iSCSI rides ordinary IP networking, standard network segmentation (dedicated
VLANs, jumbo frames for large-block workloads, and where possible a
physically or logically isolated storage network) is part of the design, not
an optional hardening step.

## Design Considerations

- **Transport choice** is driven by existing investment, latency
  requirements, and operational skill set more than by raw throughput
  numbers: an organization with an established FC fabric and SAN team rarely
  benefits from a wholesale move to iSCSI, while a green-field, Ethernet-only
  data center increasingly defaults to NVMe/TCP for new flash platforms.
- **Path count vs. oversubscription.** More host paths improve availability
  but do not, by themselves, improve performance beyond what the array's
  front-end and back-end resources can deliver; size paths for the failure
  domains you must survive (a switch, an HBA, a port), not simply "as many as
  possible."
- **Zoning strategy** should default to 1:1 zones even though it produces
  more zones to manage; zone-set automation ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md)) removes the
  operational burden this otherwise creates at scale.
- **Queue depth planning** spans host HBA queue depth, multipath queue depth
  ([Chapter 4](04-host-storage-integration-and-multipathing.md)), and array target port queue limits; an array that silently
  queues or rejects I/O beyond its port queue depth produces the exact
  latency-cliff behavior shown in [Chapter 1](01-enterprise-storage-architecture-and-service-design.md)'s queue-depth lab, but at the
  fabric layer instead of the device layer.
- **iSCSI network isolation.** Dedicate VLANs (and ideally separate physical
  NICs) to iSCSI traffic, enable jumbo frames consistently end to end
  (mismatched MTU is a leading cause of iSCSI performance problems), and do
  not route general application traffic across the same links without
  explicit QoS.
- **NVMe-oF adoption path.** Where the array and host stack both support it,
  NVMe/TCP is often the lowest-friction path to NVMe-oF's latency benefit
  because it requires no RDMA-capable NIC or lossless-Ethernet fabric
  redesign; FC-NVMe is the natural path for organizations that already run an
  FC fabric end to end.

## Implementation and Automation

### Fibre Channel zoning (illustrative)

Fabric zoning syntax is switch-CLI-specific, but the pattern is consistent
across fabrics: create an alias for each WWN, then a zone containing exactly
one initiator alias and one target alias, then add the zone to the active
zoneset.

```text
# Illustrative FC zoning workflow (generic switch CLI pattern)
alias create hba_esx01_p0  "10:00:00:00:c9:aa:bb:01"
alias create array01_ctrlA_p0 "50:0a:09:81:00:aa:bb:01"

zone create Z_ESX01_P0_ARRAY01_CTRLA_P0
zone member Z_ESX01_P0_ARRAY01_CTRLA_P0 hba_esx01_p0
zone member Z_ESX01_P0_ARRAY01_CTRLA_P0 array01_ctrlA_p0

zoneset add zoneset_prod Z_ESX01_P0_ARRAY01_CTRLA_P0
zoneset activate zoneset_prod
```

Repeat the pattern per initiator/target pair across both fabrics, pairing
each host HBA port with array target ports on redundant controllers so a
single controller failure does not remove all paths for that HBA.

### iSCSI target configuration (Linux, `targetcli`)

```bash
# On the target (storage) host
sudo dnf install -y targetcli   # or apt-get install targetcli-fb

sudo targetcli
/> backstores/block create lun01 /dev/sdb
/> iscsi/ create iqn.2026-07.com.example:target01
/> iscsi/iqn.2026-07.com.example:target01/tpg1/luns create /backstores/block/lun01
/> iscsi/iqn.2026-07.com.example:target01/tpg1/acls create iqn.2026-07.com.example:initiator01
/> iscsi/iqn.2026-07.com.example:target01/tpg1/acls/iqn.2026-07.com.example:initiator01 set auth userid=chapuser password=ChapSecret123
/> iscsi/iqn.2026-07.com.example:target01/tpg1/portals create 0.0.0.0 3260
/> saveconfig
/> exit
```

### iSCSI initiator configuration (Linux, `iscsiadm`)

```bash
# On the initiator (host) machine
sudo dnf install -y iscsi-initiator-utils   # or apt-get install open-iscsi

# Set the initiator name to match the ACL configured on the target
echo "InitiatorName=iqn.2026-07.com.example:initiator01" | sudo tee /etc/iscsi/initiatorname.iscsi

# Configure CHAP before discovery
sudo tee -a /etc/iscsi/iscsid.conf <<'EOF'
node.session.auth.authmethod = CHAP
node.session.auth.username = chapuser
node.session.auth.password = ChapSecret123
EOF

sudo systemctl restart iscsid

# Discover targets on the storage portal
sudo iscsiadm -m discovery -t sendtargets -p 10.20.30.40:3260

# Log in to the discovered target
sudo iscsiadm -m node -T iqn.2026-07.com.example:target01 -p 10.20.30.40:3260 --login

# Verify the session and the resulting block device
sudo iscsiadm -m session -P 3
lsblk
```

## Validation and Troubleshooting

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| HBA shows no fabric login | Bad SFP/cable, port disabled, fabric login rejected | Check switch port status (`show interface`), verify FC speed/topology negotiation |
| Host does not see expected LUN | Missing or incorrect zone, LUN not masked to host's WWN/IQN | Verify zone membership and active zoneset; verify masking/ACL on array |
| iSCSI login fails with auth error | CHAP username/password mismatch, wrong direction (uni- vs. mutual) | Compare `iscsid.conf` values against the target ACL; check target and initiator logs (`journalctl -u iscsid`) |
| Intermittent path loss / flapping | Marginal optic, oversubscribed ISL, MTU mismatch on iSCSI | Check switch port error counters (CRC errors, discards); verify consistent jumbo-frame MTU end to end |
| High latency, normal IOPS | Array back-end saturation, cache destage bottleneck, ISL oversubscription | Correlate host-side latency against array-side controller/back-end utilization; rule out fabric layer before escalating to array vendor |
| Rejected or queued I/O under load | Target port queue depth exceeded | Compare aggregate host queue depth per target port against the array's documented port queue limit; tune multipath queue depth ([Chapter 4](04-host-storage-integration-and-multipathing.md)) |

For iSCSI specifically, `iscsiadm -m session -P 3` reports session state,
negotiated parameters, and per-session statistics — always the first place to
look before escalating a suspected network issue. For FC, switch-side port
error counters (CRC errors, link resets, invalid transmission words) catch
marginal physical-layer problems that never surface as an outright link-down
event but still cause retransmits and latency spikes.

## Security and Best Practices

- Default to 1:1 zoning; avoid broad zones that expose more targets to a host
  (or more hosts to a target) than operationally necessary.
- Always pair zoning with LUN masking — never rely on either control alone.
- Enable CHAP (ideally mutual CHAP) for every iSCSI session; do not run
  iSCSI without authentication even on a network believed to be isolated.
- Isolate iSCSI and NVMe/TCP traffic on dedicated VLANs or physical
  interfaces separate from general application and management traffic.
- Encrypt data in flight where the platform supports it (IPsec for iSCSI,
  FC-SP for Fibre Channel) for links that cross less-trusted network
  segments, such as inter-site replication paths.
- Disable unused front-end ports and remove stale zone/ACL entries during
  decommissioning; orphaned zoning and masking entries are a recurring audit
  finding and a real attack-surface issue.
- Log and alert on fabric-level administrative changes (zoneset activation,
  ACL changes) — these are high-impact, infrequent operations where an
  unauthorized change can silently expose or sever production storage paths.

## References and Knowledge Checks

**References**

- [SNIA Fibre Channel and iSCSI architecture references.](https://www.snia.org/)
- [INCITS/NVM Express NVMe-oF specification (transport-agnostic NVMe over
  fabrics command set).](https://nvmexpress.org/specifications/)
- [`targetcli(8)`, `iscsiadm(8)` manual pages, RHEL 10 / Ubuntu Server 26.04
  LTS baseline per SOFTWARE_VERSIONS.md.](https://manpages.debian.org/bullseye/open-iscsi/iscsiadm.8)

**Knowledge Checks**

1. Explain why 1:1 zoning reduces the operational impact of RSCN events
   compared to broad multi-initiator, multi-target zones.
2. A host can see an array's target port in `iscsiadm -m session` output but
   `lsblk` shows no new device. What layer of access control is most likely
   still blocking the LUN, and how would you verify it?
3. Compare FC, iSCSI, and NVMe/TCP on the dimension of required physical
   infrastructure investment versus achievable latency.
4. Why is adding more host-to-array paths not, by itself, a performance
   improvement?
5. Describe two independent symptoms that would lead you to suspect ISL
   oversubscription rather than a single host's HBA configuration.

## Hands-On Lab

### Lab: Configure and Validate an iSCSI Target/Initiator Pair

This lab builds a working iSCSI block storage path between two Linux hosts
(or two VMs) and validates it end to end, including an authentication
failure negative test.

**Prerequisites**

- Two Linux hosts (RHEL 10 or Ubuntu Server 26.04 LTS baseline) on the same
  IP network: `storage01` (target) and `client01` (initiator).
- Root or sudo access on both hosts.
- A spare block device or a loopback-backed file on `storage01` to present
  as the LUN (a 2 GB file is sufficient for this lab).

**Procedure**

1. On `storage01`, install `targetcli` and create a backing LUN:

   ```bash
   sudo dnf install -y targetcli   # or: apt-get install -y targetcli-fb
   sudo fallocate -l 2G /var/lib/iscsi-lab-lun.img
   ```

2. Configure the target, ACL, CHAP, and portal as shown in the
   Implementation section above, substituting the `client01` initiator IQN
   for the ACL entry and using the backing file instead of `/dev/sdb`:

   ```bash
   sudo targetcli
   /> backstores/fileio create lun01 /var/lib/iscsi-lab-lun.img 2G
   /> iscsi/ create iqn.2026-07.lab.example:storage01
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/luns create /backstores/fileio/lun01
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/acls create iqn.2026-07.lab.example:client01
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/acls/iqn.2026-07.lab.example:client01 set auth userid=labuser password=LabSecret123
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/portals create 0.0.0.0 3260
   /> saveconfig
   /> exit
   ```

3. On `client01`, install `open-iscsi`, set the initiator name to match the
   ACL, configure CHAP, and restart the service:

   ```bash
   sudo dnf install -y iscsi-initiator-utils   # or: apt-get install -y open-iscsi
   echo "InitiatorName=iqn.2026-07.lab.example:client01" | sudo tee /etc/iscsi/initiatorname.iscsi
   sudo tee -a /etc/iscsi/iscsid.conf <<'EOF'
   node.session.auth.authmethod = CHAP
   node.session.auth.username = labuser
   node.session.auth.password = LabSecret123
   EOF
   sudo systemctl restart iscsid
   ```

4. Discover and log in from `client01` (replace `<storage01_ip>` with the
   actual address):

   ```bash
   sudo iscsiadm -m discovery -t sendtargets -p <storage01_ip>:3260
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip>:3260 --login
   ```

5. **Expected result:** `iscsiadm -m session -P 3` shows an established
   session with state `LOGGED_IN`, and `lsblk` on `client01` shows a new
   block device corresponding to the 2 GB LUN.

**Negative test**

6. Log out, deliberately set an incorrect CHAP password, and attempt to log
   in again:

   ```bash
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip>:3260 --logout
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip>:3260 \
       --op=update -n node.session.auth.password -v WrongPassword
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip>:3260 --login
   ```

   **Expected result:** the login fails with an authentication error, and
   `journalctl -u iscsid --since "2 minutes ago"` shows the rejected CHAP
   negotiation. This confirms the ACL and CHAP configuration are actually
   enforcing authentication rather than silently permitting access.

7. Restore the correct password (`--op=update -n node.session.auth.password
   -v LabSecret123`) and log back in to confirm recovery.

**Cleanup**

8. On `client01`, log out and delete the node record:

   ```bash
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip>:3260 --logout
   sudo iscsiadm -m node -o delete -T iqn.2026-07.lab.example:storage01
   ```

9. On `storage01`, remove the target configuration and backing file:

   ```bash
   sudo targetcli /iscsi delete iqn.2026-07.lab.example:storage01
   sudo targetcli saveconfig
   sudo rm -f /var/lib/iscsi-lab-lun.img
   ```

## Summary and Completion Checklist

This chapter covered SAN transports (FC, iSCSI, FCoE, NVMe-oF), fabric
topology and the layered zoning/masking access-control model, array
front-end/back-end architecture, and the iSCSI session model, then applied
that theory to a working target/initiator configuration with a CHAP
authentication negative test.

**Completion checklist**

- [ ] Can explain the trade-offs between FC, iSCSI, and NVMe-oF.
- [ ] Can describe why zoning and LUN masking are both required and neither
      is sufficient alone.
- [ ] Can identify the front-end, cache, and back-end resources that bound
      array performance.
- [ ] Has configured a working iSCSI target with CHAP authentication and a
      corresponding initiator login.
- [ ] Has reproduced and diagnosed a CHAP authentication failure.
- [ ] Can list at least four SAN-layer troubleshooting symptoms and their
      likely root causes.
