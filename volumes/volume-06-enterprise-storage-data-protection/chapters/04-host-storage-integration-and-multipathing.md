# Chapter 4: Host Storage Integration and Multipathing

![Lab topology for this chapter: storage01 presents one 2 GB LUN through two independent portals; client01 logs into both, producing two raw block devices for the same LUN, which multipathd aggregates into mpatha with round-robin path selection, both paths active ready running. As a negative test, client01 logs out of the session on one portal only; multipath -ll shows that path as failed faulty running while the remaining path stays active ready running, and the mounted filesystem's file reads continue without interruption — multipath failover, not the application, absorbed the path loss. Restoring the path returns it to active ready running via failback immediate.](../../../diagrams/volume-06-enterprise-storage-data-protection/chapter-04-dm-multipath-failover-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: DM-Multipath aggregating two iSCSI paths to one LUN, tested against a simulated path failure and recovery.*

## Learning Objectives

- Explain why host-side multipathing is required even when the SAN fabric
  itself is fully redundant, and describe the data-corruption risk it
  prevents.
- Describe ALUA (Asymmetric Logical Unit Access) and ANA (Asymmetric
  Namespace Access) path states and how they influence path selection on
  dual-controller arrays.
- Compare multipath path-selection policies and failback behaviors and
  choose an appropriate policy for a given array and workload.
- Configure Linux native multipathing (device-mapper multipath) with a
  working `multipath.conf`.
- Configure NVMe-oF native multipathing and explain how it differs
  architecturally from DM-Multipath.
- Align host-side queue depth, LVM device filtering, and persistent device
  naming with the array-side limits established in Chapters 1 and 2.
- Diagnose path failure, path flapping, and multipath misconfiguration from
  host-side evidence.

## Theory and Architecture

[Chapter 2](02-block-storage-and-storage-area-networks.md) built a fabric with two independent paths from every host to
every array controller — the fabric-layer half of storage redundancy.
Host-side multipathing is the layer that turns that fabric redundancy into
something the operating system, and the applications running on it, can
actually depend on. Without it, a host with two HBA ports connected across
two fabrics to two array controller ports does not see one resilient LUN;
it sees between two and four separate raw block devices, one per
initiator-target path, each apparently a distinct disk. A filesystem or
database mounted directly on top of one of those raw devices while I/O is
occasionally issued to another representing the same physical blocks is a
direct path to silent data corruption, not resilience.

Host multipathing exists to solve exactly that problem. It:

1. **Discovers** that two or more raw block devices are, in fact, different
   paths to the same logical unit, using a stable identifier — the World
   Wide Identifier (WWID) for SCSI/FC/iSCSI LUNs, or the NVMe namespace
   identifier (NSID) plus subsystem NQN for NVMe.
2. **Coalesces** those raw devices into a single, stable multipath (or
   native NVMe) device that the OS presents to applications, LVM, and
   filesystems.
3. **Distributes or fails over** I/O across the underlying paths according
   to a selected path-selection policy, reacting to path loss without host
   or application intervention.

### DM-Multipath architecture

On Linux, device-mapper multipath (`multipathd`, backed by the `dm-multipath`
kernel target) is the standard native multipathing stack for SCSI, Fibre
Channel, and iSCSI block devices. Its components:

- **`multipathd`** — the userspace daemon that monitors path health, reacts
  to udev events (device add/remove), and reconfigures the device-mapper
  table when path state changes.
- **`/etc/multipath.conf`** — the configuration file defining defaults,
  per-array (`devices`) tuning, per-LUN (`multipaths`) overrides, and a
  `blacklist` of devices that should never be multipathed (local boot
  disks, USB media).
- **`dm-multipath` device nodes** (`/dev/mapper/mpathN` or a WWID-based
  alias) — the coalesced device that everything above the multipath layer
  should reference. Referencing an underlying raw path device
  (`/dev/sdc`) directly anywhere above this layer defeats the purpose of
  multipathing and risks the exact corruption scenario multipathing exists
  to prevent.

### ALUA and asymmetric access

Most dual-controller arrays are **asymmetric active/active**: a given LUN
has one "owning" controller, and while both controllers can technically
service I/O for it, paths through the non-owning controller incur an
internal inter-controller redirect and materially higher latency. **ALUA**
(Asymmetric Logical Unit Access) is the SCSI standard mechanism arrays use
to advertise this asymmetry to hosts, exposing each path in one of several
states:

| ALUA state | Meaning | Multipath behavior |
| --- | --- | --- |
| Active/Optimized (AO) | Path to the owning controller; full performance | Preferred for normal I/O |
| Active/Non-Optimized (ANO) | Path to the peer controller; functional but higher latency | Used only if no AO path is available, or deliberately for a fraction of I/O on policies that support it |
| Standby | Path exists but is not currently usable for I/O | Not used for I/O; available as a failover target after a controller-level state change |
| Unavailable | Path is down or the target does not recognize the LUN on this path | Excluded from all path groups |

A multipath configuration that is not ALUA-aware treats AO and ANO paths as
equally weighted members of the same path group, which silently sends a
share of I/O across the slower inter-controller path even while all
controllers are healthy — a common, hard-to-notice source of inconsistent
latency. The `alua` (or vendor-specific `hardware_handler`) setting in
`multipath.conf` is what makes the host aware of, and correctly grouped by,
these states.

NVMe uses the analogous **ANA (Asymmetric Namespace Access)** model, with
states `optimized`, `non-optimized`, `inaccessible`, `persistent loss`, and
`change`, serving the same purpose for NVMe namespaces that ALUA serves for
SCSI LUNs.

### Path selection policies

Once paths are correctly grouped by ALUA/ANA state, a **path selector**
decides how I/O is distributed across the paths within the active group:

| Policy | Behavior | Best fit |
| --- | --- | --- |
| `round-robin` | Cycles through paths in fixed order, optionally batching a configurable number of I/Os per path (`rr_min_io`) | Simple, predictable; can under-perform if paths have unequal latency |
| `queue-length` | Sends the next I/O to the path with the fewest outstanding requests | Adapts to transient per-path congestion; a common modern default |
| `service-time` | Sends the next I/O to the path with the lowest estimated service time (based on outstanding I/O and historical latency) | Best fit when paths have measurably different latency (for example, mixed link speeds); default on many current distributions |

**Failback behavior** is a separate, equally important setting: `immediate`
failback returns I/O to a recovered path as soon as it is seen active
again, which is usually correct, but `manual` or delayed failback (a
configurable number of seconds) is sometimes deliberately chosen to avoid
flapping back and forth across a marginal, intermittently failing path.

### NVMe native multipathing

NVMe multipathing is handled natively in the Linux NVMe core (not
device-mapper) once `nvme_core.multipath=Y` is enabled (the default on
current kernels). Instead of `/dev/mapper/mpathN`, multiple paths to the
same NVMe namespace coalesce transparently under a single `/dev/nvmeXnY`
device, and `nvme-cli` provides the multipath-aware view. Architecturally
this is a cleaner model than DM-Multipath layered on top of SCSI — the path
awareness is built into the block layer for the namespace itself rather
than bolted on as a separate device-mapper target — but the operational
concepts (ANA-aware grouping, active-optimized preference, failover on path
loss) are directly analogous to ALUA-aware DM-Multipath.

### The host-side I/O stack and queue depth chain

An I/O issued by an application traverses a stack in which every layer has
its own concurrency limit:

```text
Application
  -> Filesystem (XFS, ext4, ...)
    -> LVM (dm-linear/dm-thin, if used)
      -> Multipath (dm-multipath queue_depth, path_grouping_policy)
        -> HBA/CNA driver (per-LUN queue depth, HBA firmware/driver max)
          -> Fabric (Chapter 2)
            -> Array front-end port queue depth (Chapter 2)
```

[Chapter 1](01-enterprise-storage-architecture-and-service-design.md)'s `fio` lab demonstrated that achievable IOPS is bounded by queue
depth at the device layer; this chapter's queue depth chain is the same
principle applied across every layer between the application and the
array. A host HBA driver defaulting to a shallow per-LUN queue depth (a
common out-of-box setting on some driver stacks) will bottleneck a
workload long before the array's own front-end port queue limit from
[Chapter 2](02-block-storage-and-storage-area-networks.md) is ever reached, and no amount of array-side tuning fixes a
host-side ceiling.

### Persistent device naming

Raw device names (`/dev/sda`, `/dev/sdb`, ...) are not guaranteed stable
across reboots, especially with multiple paths and dynamic LUN
provisioning. Multipath device naming should always be based on the WWID
(or an administrator-defined alias mapped to that WWID in
`/etc/multipath.conf`), and anything referencing storage above the
multipath layer — LVM physical volumes, filesystem mount entries, database
raw device references — should use the resulting `/dev/mapper/<alias>` or
`/dev/disk/by-id/dm-uuid-*` path, never a raw `/dev/sdX` path.

## Design Considerations

- **Path count vs. operational complexity.** Two paths per fabric (four
  total, two per HBA port) covers the common failure domains — a switch, an
  HBA port, a controller — without the diminishing-returns complexity of
  eight or more paths per LUN; size path count to the failure domains the
  design must survive, consistent with the same principle from [Chapter 2](02-block-storage-and-storage-area-networks.md).
- **`no_path_retry` / `queue_if_no_path` vs. fail-fast.** When all paths to
  a LUN are lost, the host can either queue I/O indefinitely (waiting for a
  path to return) or fail I/O immediately. Queuing is usually correct for
  standalone hosts, where a brief fabric event should not surface as an
  application-visible I/O error. Fail-fast (a bounded `no_path_retry`
  value) is often required for clustered filesystems and cluster software
  that use storage-level fencing, where an indefinitely hung I/O can block
  the cluster's own failure-detection logic rather than letting it act.
- **ALUA/ANA awareness is not optional** on any array that implements
  asymmetric access; omitting it does not disable the asymmetry, it only
  hides it from the multipath layer's path-selection logic, producing
  inconsistent, hard-to-diagnose latency.
- **Queue depth alignment.** Set host HBA and multipath queue depth
  deliberately against the array's documented per-port and per-LUN queue
  limits from [Chapter 2](02-block-storage-and-storage-area-networks.md)'s array capacity planning, not the driver default;
  under-sizing wastes available array performance, and over-sizing across
  many hosts sharing a front-end port can collectively exceed the array's
  port queue limit and trigger the same latency-cliff behavior from
  [Chapter 1](01-enterprise-storage-architecture-and-service-design.md)'s queue-depth lab.
- **Boot-from-SAN.** Hosts booting from a SAN LUN need multipath support
  built into the initial RAM disk (initramfs/dracut), not only the running
  system; a host that boots successfully once but cannot rebuild its
  initramfs with multipath support after a kernel update is a common,
  easily overlooked operational gap.
- **NVMe/TCP and native multipathing convergence.** As NVMe-oF adoption
  grows, expect native NVMe multipathing to gradually replace DM-Multipath
  for NVMe-attached storage; plan host build standards and automation
  ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md)) to support both models during the transition rather than
  assuming one stack indefinitely.

## Implementation and Automation

### `multipath.conf`

```text
# /etc/multipath.conf
defaults {
    user_friendly_names yes
    find_multipaths yes
    path_selector "service-time 0"
    path_grouping_policy group_by_prio
    failback immediate
    no_path_retry 12
    rr_min_io_rq 1
}

blacklist {
    devnode "^sda$"          # local boot disk, never multipathed
    devnode "^(hd|xvd)[a-z]"
}

devices {
    device {
        vendor              "GENERIC"
        product             "SAN-ARRAY"
        path_grouping_policy group_by_prio
        prio                "alua"
        hardware_handler    "1 alua"
        path_selector       "service-time 0"
        failback            immediate
        no_path_retry       12
        rr_weight           uniform
    }
}

multipaths {
    multipath {
        wwid "36000c29a1b2c3d4e5f60718293a4b5c6"
        alias mpath-db01-datavol
    }
}
```

The `devices` stanza is the array-specific tuning block — vendor and
product strings must match the array's reported identification exactly
(`multipath -ll -v3` prints what the host actually sees), and `prio alua`
combined with `hardware_handler "1 alua"` is what enables the ALUA-aware
grouping described above. The `multipaths` stanza pins a specific WWID to
a stable, human-readable alias so `/dev/mapper/mpath-db01-datavol` remains
predictable across the LUN's lifecycle regardless of controller-assigned
device ordering.

### Bringing multipathing online and inspecting state

```bash
sudo dnf install -y device-mapper-multipath   # or: apt-get install multipath-tools
sudo systemctl enable --now multipathd

# Rediscover paths after new LUN presentation
sudo rescan-scsi-bus.sh -a
sudo multipath -v2

# Show the current multipath topology
sudo multipath -ll
```

Representative `multipath -ll` output:

```text
mpath-db01-datavol (36000c29a1b2c3d4e5f60718293a4b5c6) dm-3 GENERIC,SAN-ARRAY
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 3:0:0:1 sdc 8:32  active ready running
| `- 4:0:0:1 sde 8:64  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 3:0:1:1 sdd 8:48  active ready running
  `- 4:0:1:1 sdf 8:80  active ready running
```

The two `prio=50` paths are the Active/Optimized group (owning controller);
the `prio=10` group is Active/Non-Optimized and is used only if the AO
group becomes unavailable — exactly the ALUA-aware behavior configured
above.

### LVM device filtering

Once multipath devices exist, LVM must be prevented from also scanning the
underlying raw paths, which would otherwise let a volume group form on the
wrong (non-multipathed) device path:

```text
# /etc/lvm/lvm.conf (devices section)
devices {
    filter = [ "a|/dev/mapper/mpath.*|", "r|/dev/sd.*|", "r|.*|" ]
    multipath_component_detection = 1
}
```

### NVMe-oF native multipathing

```bash
# Confirm native NVMe multipathing is enabled
cat /sys/module/nvme_core/parameters/multipath   # expect: Y

# Connect to redundant NVMe/TCP portals for the same subsystem
sudo nvme connect -t tcp -a 10.20.40.10 -s 4420 -n nqn.2026-07.com.example:nvme-target01
sudo nvme connect -t tcp -a 10.20.41.10 -s 4420 -n nqn.2026-07.com.example:nvme-target01

# Inspect the coalesced subsystem and per-path (controller) ANA state
sudo nvme list-subsys
sudo nvme list
```

Representative `nvme list-subsys` output shows a single subsystem with two
live controllers, each reporting its ANA state (`optimized` or
`non-optimized`), analogous to the ALUA path groups shown above for
DM-Multipath.

## Validation and Troubleshooting

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| `multipath -ll` shows fewer paths than expected | Missing zone/ACL (Chapter 2), HBA not logged into fabric, `find_multipaths` blacklist matched unintentionally | Check `multipath -v3` verbose discovery output; re-verify zoning/masking from Chapter 2 |
| One path group permanently shown `enabled`, never `active` | ALUA/hardware_handler misconfigured for this array's vendor/product string | Confirm `vendor`/`product` strings match `multipath -ll -v3` exactly; verify `hardware_handler` matches array documentation |
| I/O hangs indefinitely after a fabric event | `no_path_retry` set to `queue` (unbounded) with no fabric recovery in progress | Check `multipathd` logs for path state changes; consider a bounded `no_path_retry` value for fenced cluster nodes |
| Path repeatedly flaps (active/failed/active) | Marginal optic/cable, intermittent switch port errors, mismatched host/array timeout settings | Correlate `journalctl -u multipathd` timestamps against switch port error counters (Chapter 2) |
| New LUN not visible after array-side provisioning | Host has not rescanned the SCSI bus; udev rule not triggered | Run `rescan-scsi-bus.sh -a` (or the vendor-provided rescan script) and `multipath -v2` |
| Uneven latency across paths despite `multipath -ll` showing all paths active | Non-ALUA-aware configuration treating AO and ANO paths as one group | Add or correct `prio "alua"` and `hardware_handler` for the array; re-verify path grouping in `multipath -ll` |
| Application sees I/O errors during a single-path failure that should have been transparent | Application or database bypassing the multipath device and referencing a raw `/dev/sdX` path directly | Audit mount tables, LVM PV list, and database device configuration for any raw path reference; correct to the `/dev/mapper/` device |

`multipathd show paths format "%d %t %o %T"` and `multipathd show maps
topology` provide live, without-reload views of path and map state and are
generally faster for a running investigation than repeatedly parsing
`multipath -ll`.

## Security and Best Practices

- Treat `/etc/multipath.conf` and `/etc/lvm/lvm.conf` as production
  configuration under change control, identical to any other infrastructure
  configuration file — an unreviewed edit here can silently remove path
  redundancy or misdirect I/O.
- Never permit an application, database, or filesystem to reference a raw
  underlying path device; enforce the `/dev/mapper/` (or `/dev/disk/by-id/`)
  convention in build standards and automation (Chapter 9).
- Choose `no_path_retry`/fencing behavior deliberately based on whether the
  host participates in a cluster with its own fencing mechanism; an
  indefinite queue on a fenced cluster node can delay failure detection
  rather than protect availability.
- Blacklist local boot and non-shared devices explicitly in
  `multipath.conf` rather than relying on default heuristics, to avoid
  accidentally multipathing a device that should not be.
- Keep HBA/CNA firmware and driver versions on a tracked, tested baseline
  aligned to the array vendor's interoperability matrix; multipath and ALUA
  behavior is sensitive to firmware/driver mismatches that are otherwise
  hard to reproduce.
- Disable and remove stale multipath alias/WWID entries during
  decommissioning, mirroring the zoning/masking cleanup practice from
  Chapter 2.

## References and Knowledge Checks

**References**

- [SNIA Multipath I/O and ALUA specification references.](https://www.snia.org/)
- [INCITS/NVM Express Asymmetric Namespace Access (ANA) specification.](https://nvmexpress.org/specifications/)
- [`multipath.conf(5)`, `multipathd(8)`, `nvme(1)`, `lvm.conf(5)` manual
  pages, RHEL 10 / Ubuntu Server 26.04 LTS baseline per
  SOFTWARE_VERSIONS.md.](https://manpages.debian.org/unstable/multipath-tools/multipath.conf.5.en.html)

**Knowledge Checks**

1. Explain the specific data-corruption risk that host-side multipathing
   prevents, and why fabric-level redundancy from Chapter 2 alone does not
   prevent it.
2. What is the practical performance difference between an Active/Optimized
   and an Active/Non-Optimized ALUA path, and why does an ALUA-unaware
   multipath configuration create inconsistent latency even when all paths
   are technically healthy?
3. A clustered filesystem node uses storage-level fencing. Explain why an
   unbounded `no_path_retry` (`queue_if_no_path` indefinitely) setting is a
   poor choice on that node specifically.
4. Trace the host-side queue depth chain from application to array front-end
   port, and explain why tuning only the array side cannot fix a
   host-side bottleneck.
5. Why must LVM's device filter exclude raw underlying paths once
   multipathing is configured?

## Hands-On Lab

### Lab: Configure DM-Multipath Over Dual iSCSI Paths and Validate Failover

This lab builds on Chapter 2's iSCSI target/initiator lab by presenting the
same LUN over two independent portals, configuring DM-Multipath on the
initiator, and validating both normal multipath operation and failover
when one path is deliberately removed.

**Prerequisites**

- Two Linux hosts (RHEL 10 or Ubuntu Server 26.04 LTS baseline):
  `storage01` (target) and `client01` (initiator), each with at least two
  IP addresses or interfaces reachable from the other host (two NICs, or
  two IP aliases on one NIC, is sufficient for this lab).
- Root or sudo access on both hosts.
- `targetcli`, `open-iscsi`/`iscsi-initiator-utils`, and
  `device-mapper-multipath`/`multipath-tools` installed.

**Procedure**

1. On `storage01`, create a backing LUN and an iSCSI target with two
   portals, one per address:

   ```bash
   sudo dnf install -y targetcli device-mapper-multipath
   sudo fallocate -l 2G /var/lib/multipath-lab-lun.img
   sudo targetcli
   /> backstores/fileio create lun01 /var/lib/multipath-lab-lun.img 2G
   /> iscsi/ create iqn.2026-07.lab.example:storage01
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/luns create /backstores/fileio/lun01
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/acls create iqn.2026-07.lab.example:client01
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/portals create <storage01_ip_A> 3260
   /> iscsi/iqn.2026-07.lab.example:storage01/tpg1/portals create <storage01_ip_B> 3260
   /> saveconfig
   /> exit
   ```

2. On `client01`, install the initiator and multipath packages, set the
   initiator name, and log into both portals:

   ```bash
   sudo dnf install -y iscsi-initiator-utils device-mapper-multipath
   echo "InitiatorName=iqn.2026-07.lab.example:client01" | sudo tee /etc/iscsi/initiatorname.iscsi
   sudo systemctl restart iscsid

   sudo iscsiadm -m discovery -t sendtargets -p <storage01_ip_A>:3260
   sudo iscsiadm -m discovery -t sendtargets -p <storage01_ip_B>:3260
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip_A>:3260 --login
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip_B>:3260 --login
   lsblk
   ```

   **Expected result:** two new raw block devices appear (for example
   `/dev/sdb` and `/dev/sdc`), both the same size, representing two paths
   to the same LUN.

3. Configure and start multipathing:

   ```bash
   sudo tee /etc/multipath.conf <<'EOF'
   defaults {
       user_friendly_names yes
       find_multipaths yes
       path_selector "round-robin 0"
       failback immediate
       no_path_retry 8
   }
   EOF
   sudo systemctl enable --now multipathd
   sudo multipath -v2
   sudo multipath -ll
   ```

   **Expected result:** `multipath -ll` shows one multipath device (for
   example `mpatha`) with two paths, both `active ready running`.

4. Format and mount the multipath device to prove it behaves as a single
   consistent block device:

   ```bash
   sudo mkfs.xfs /dev/mapper/mpatha
   sudo mkdir -p /mnt/multipath-lab
   sudo mount /dev/mapper/mpatha /mnt/multipath-lab
   echo "multipath lab data" | sudo tee /mnt/multipath-lab/testfile.txt
   ```

**Negative test**

5. Identify which underlying raw device corresponds to one path (from
   `multipath -ll` output) and simulate a path failure by logging out of
   that specific iSCSI session, then confirm the mounted filesystem
   remains accessible:

   ```bash
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip_A>:3260 --logout
   sudo multipath -ll
   cat /mnt/multipath-lab/testfile.txt
   ```

   **Expected result:** `multipath -ll` shows the corresponding path as
   `failed faulty running` while the remaining path stays `active ready
   running`; the file read succeeds without interruption, demonstrating
   that multipath failover — not the application — absorbed the path loss.

6. Restore the failed path and confirm it rejoins the multipath device:

   ```bash
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 -p <storage01_ip_A>:3260 --login
   sudo multipath -ll
   ```

   **Expected result:** the previously failed path returns to `active
   ready running` due to `failback immediate`.

**Cleanup**

7. Unmount and remove the multipath device configuration:

   ```bash
   sudo umount /mnt/multipath-lab
   sudo rmdir /mnt/multipath-lab
   sudo multipath -f mpatha
   sudo iscsiadm -m node -T iqn.2026-07.lab.example:storage01 --logoutall=all
   sudo iscsiadm -m node -o delete -T iqn.2026-07.lab.example:storage01
   ```

8. On `storage01`, remove the target and backing file:

   ```bash
   sudo targetcli /iscsi delete iqn.2026-07.lab.example:storage01
   sudo targetcli saveconfig
   sudo rm -f /var/lib/multipath-lab-lun.img
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter covered why host-side multipathing is required to safely
consume the fabric redundancy built in Chapter 2, the ALUA/ANA path-state
model, path-selection and failback policy choices, and the full host I/O
stack from application to array front-end port. It then applied that
theory to a working DM-Multipath configuration over dual iSCSI paths,
including a live path-failure negative test.

**Completion checklist**

- [ ] Can explain why multipathing exists and what corruption risk it
      prevents.
- [ ] Can describe ALUA/ANA path states and their effect on path grouping
      and selection.
- [ ] Has configured `multipath.conf` with array-specific tuning and an
      alias mapping.
- [ ] Has configured NVMe native multipathing conceptually and can compare
      it to DM-Multipath.
- [ ] Has built and validated a working dual-path iSCSI multipath device.
- [ ] Has reproduced and observed transparent failover during a live path
      failure.
- [ ] Can trace the host-side queue depth chain and identify where a
      bottleneck at each layer would surface.
