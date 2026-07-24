# Chapter 02: PowerEdge Servers — from Foundations to XE

## Learning Objectives

- Operate PowerEdge at certification depth: platform anatomy, BIOS/UEFI
  and boot, storage controllers, and firmware lifecycle
- Manage at scale with iDRAC and OpenManage Enterprise, connecting
  this chapter to Volumes XXII and XXIII
- Deploy the MX modular platform and understand the XE accelerated
  line that carries Dell's AI infrastructure
- Map the server ladder: PowerEdge Foundations (D-PE-FN-01), Operate
  (D-PE-OE-01), MX Modular Deploy (D-PEMX-DY-23), XE Install
  (D-PEXE-IN-A-01), and XE Operate (D-PEXE-OE-00)

## Theory and Architecture

### The ladder in one sentence

The server track certifies the machine under everything else in this
encyclopedia: **Foundations** names the parts and the portfolio,
**Operate** certifies day-to-day administration — BIOS/UEFI
configuration, PERC RAID, iDRAC-driven management, firmware update
discipline — **MX Deploy** adds the chassis-based modular platform
(MX7000: shared power, networking fabrics, OpenManage Enterprise
Modular), and the **XE pair** covers the accelerated servers (XE9680
class: GPU-dense, liquid-cooling options) that host AI workloads.

### The management plane is the product

PowerEdge administration is iDRAC administration: out-of-band
console, virtual media, RACADM and Redfish APIs, and lifecycle
operations (the Volume XXVI lab's first chapter is exactly this).
Fleet scale moves to **OpenManage Enterprise**: discovery, baselines,
firmware compliance, and configuration templates — Volume XXII covers
the platform end to end; this chapter frames what its exams assume.

### XE and the AI substrate

The XE line's exam pair exists because accelerated servers break
general-server assumptions: GPU topology and NVLink domains, power
budgets per rack position, airflow/liquid cooling, and
firmware/driver stacks validated as one unit. XE Install certifies
racking-to-first-boot; XE Operate certifies the running estate —
both feed Chapter 08's AI certifications.

## Design Considerations

- One iDRAC credential model and certificate policy fleet-wide before
  the tenth server, not after the hundredth
- Firmware as a baseline, never per-box: OME catalogs against a
  repository you control (Volume XXII's pattern)
- MX versus rack servers: shared infrastructure economics against
  blast radius — the MX chassis is a failure domain and must be
  drawn as one (Volume II doctrine)

## Implementation and Automation

```text
# RACADM one-liners the Operate exam expects you to know exist
racadm get iDRAC.NIC                   # management NIC state
racadm get BIOS.SysProfileSettings     # performance profile
racadm jobqueue view                   # lifecycle jobs in flight
racadm update -f catalog.xml -t HTTP   # firmware from a catalog

# Redfish, the modern surface (Volume XXII automates this at fleet scale)
curl -sk -u root:*** https://idrac-lab/redfish/v1/Systems/System.Embedded.1 \
  | jq '.PowerState, .BiosVersion, .Model'
```

## Validation and Troubleshooting

- iDRAC Lifecycle Log first, OS logs second — hardware truth lives
  out-of-band
- `racadm getsel` (system event log) for the hardware timeline;
  drive/PERC state from storage views before any OS-level guess
- Firmware compliance report in OME — drift is the root cause of a
  remarkable share of "random" PowerEdge behavior
- For XE: GPU inventory and thermal headroom via iDRAC before
  blaming frameworks

## Security and Best Practices

- Dedicated management VLAN, unique per-box iDRAC credentials from a
  vault, TLS certificates replaced, default root/calvin retired on
  first boot (the scope-boundaries policy documents defaults; change
  them)
- Signed-firmware-only, staged rollouts by baseline ring
- System Lockdown Mode where the platform supports it

## References and Knowledge Checks

- Exam descriptions: D-PE-FN-01, D-PE-OE-01, D-PEMX-DY-23,
  D-PEXE-IN-A-01, D-PEXE-OE-00 (Dell Learning catalog)
- Volumes XXII, XXIII, XXVI of this encyclopedia; PowerEdge and MX
  owner's manuals

Knowledge checks:

1. Which subsystem answers "why did this server reboot at 03:14" and
   why is it authoritative over the OS log?
2. Contrast MX7000 shared fabrics with per-server NICs as failure
   domains.
3. Name three properties of XE-class servers that justify a separate
   Install exam.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab spanning the **PowerEdge exam
family — Foundations (D-PE-FN-01), Operate (D-PE-OE-01), MX Modular Deploy
(D-PEMX-DY-23), and XE Install/Operate (D-PEXE-IN-A-01 / D-PEXE-OE-00)** — mapped in
the volume README's coverage tables. Labs use the iDRAC `racadm` CLI and OpenManage
Enterprise. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 2.1–2.9** — a PowerEdge server with iDRAC9/10
reachable at `$IDRAC`, `racadm` (local or remote), an OpenManage Enterprise (OME)
console, and (for MX) an OME-Modular chassis. **Cost:** none beyond lab resources.

### Lab 2.1 — Server inventory and iDRAC (PowerEdge Foundations)

**Objective:** Read the server inventory and iDRAC status via racadm.

```text
racadm -r $IDRAC -u root -p $PW getsysinfo
racadm -r $IDRAC -u root -p $PW hwinventory | grep -E "FQDD|Model|Manufacturer" | head
```

**Expected result:** the service tag, model, BIOS/iDRAC versions, and hardware
inventory — **iDRAC** (the out-of-band controller) plus the **Lifecycle Controller**
give agent-free inventory, configuration, and monitoring of every FRU, the foundation
of PowerEdge management.

**Negative test:** manage the OS in-band only and lose visibility when the OS is
down; iDRAC works with the host powered off (on standby power) — out-of-band is
independent of the OS.

**Cleanup:** none (read-only).

### Lab 2.2 — BIOS and UEFI configuration (PowerEdge Operate)

**Objective:** Read and stage a BIOS attribute via racadm.

```text
racadm -r $IDRAC -u root -p $PW get BIOS.SysProfileSettings.SysProfile
racadm -r $IDRAC -u root -p $PW set BIOS.SysProfileSettings.SysProfile PerfOptimized
racadm -r $IDRAC -u root -p $PW jobqueue create BIOS.Setup.1-1 -s TIME_NOW
```

**Expected result:** the system profile read and a staged BIOS job — BIOS/UEFI
settings (system profile, boot mode, virtualization, memory) are configured via
racadm/Redfish and applied through a **staged job** at the next reboot, so changes
are scheduled, not immediate.

**Negative test:** `set` a BIOS attribute and expect it live without a job/reboot; it
stays pending — BIOS changes require the Lifecycle Controller job to apply on
restart.

**Cleanup:** `racadm ... jobqueue delete -i <jobid>` if not yet applied.

### Lab 2.3 — Storage and PERC RAID (PowerEdge Operate)

**Objective:** Read the PERC controller and create a virtual disk.

```text
racadm -r $IDRAC -u root -p $PW storage get controllers
racadm -r $IDRAC -u root -p $PW storage get pdisks -o
racadm -r $IDRAC -u root -p $PW storage createvd:RAID.Integrated.1-1 -rl r1 -pdkey:<pd1>,<pd2>
racadm -r $IDRAC -u root -p $PW jobqueue create RAID.Integrated.1-1 -s TIME_NOW
```

**Expected result:** the PERC controller, physical disks, and a staged RAID-1 VD job
— the **PERC** RAID controller presents virtual disks to the OS; racadm creates VDs
by RAID level and disk keys, applied through a storage job.

**Negative test:** create a RAID-5 VD with two disks; the controller rejects it —
RAID levels have minimum-disk requirements the controller enforces.

**Cleanup:** `racadm ... storage deletevd:<vd-fqdd>` then apply the job.

### Lab 2.4 — Firmware update via Lifecycle Controller (PowerEdge Operate)

**Objective:** Stage a firmware update and read the version inventory.

```text
racadm -r $IDRAC -u root -p $PW update viewinventory
racadm -r $IDRAC -u root -p $PW update -f BIOS_XXXX.EXE -l //10.0.0.50/share -u user -p pw
racadm -r $IDRAC -u root -p $PW jobqueue view
```

**Expected result:** the current firmware inventory and a staged update job — the
**Lifecycle Controller** manages firmware for every component from a catalog (local,
network share, or Dell online), staging and applying updates with rollback, so the
fleet stays on a validated baseline.

**Negative test:** apply a firmware image for the wrong model/component; the LC
rejects it as incompatible — the catalog/component match is validated before flash.

**Cleanup:** cancel the job if staged and not yet applied.

### Lab 2.5 — OpenManage Enterprise monitoring (PowerEdge Operate)

**Objective:** Read device health and firmware compliance in OME.

```bash
curl -sk -u admin:$PW "https://$OME/api/DeviceService/Devices" | jq -r '.value[] | "\(.DeviceName) \(.DeviceManagement[0].NetworkAddress)"' | head
curl -sk -u admin:$PW "https://$OME/api/DeviceService/Devices?\$filter=Health eq 3000" 2>/dev/null | jq '.["@odata.count"]'
```

**Expected result:** the managed devices and any in critical health — **OpenManage
Enterprise** discovers and monitors PowerEdge at fleet scale: health, firmware
compliance against a catalog baseline, configuration templates, and alerting, all via
a REST API for automation.

**Negative test:** a device discovered without iDRAC credentials shows limited data;
OME needs the iDRAC credential to inventory and manage it fully.

**Cleanup:** none (read-only).

### Lab 2.6 — Power and thermal management (PowerEdge Operate)

**Objective:** Read power/thermal state and set a power cap.

```text
racadm -r $IDRAC -u root -p $PW getpower
racadm -r $IDRAC -u root -p $PW get System.Power.Cap
racadm -r $IDRAC -u root -p $PW set System.Power.Cap.Enable Enabled
```

**Expected result:** current draw, temperatures, and a power cap — PowerEdge power
management reads real-time consumption and can **cap** power (for rack/PDU budgets)
and tune thermal/fan profiles; iDRAC exposes it for capacity planning.

**Negative test:** cap power below the server's minimum for its load; the server
throttles CPU to stay under the cap, hurting performance — the cap must exceed the
workload's floor.

**Cleanup:** `racadm ... set System.Power.Cap.Enable Disabled`.

### Lab 2.7 — PowerEdge MX modular (MX Modular Deploy)

**Objective:** Read the MX chassis fabric and sled assignment via OME-Modular.

```bash
curl -sk -u admin:$PW "https://$OMEM/api/DeviceService/Devices?\$filter=Type eq 2000" | jq -r '.value[]?.DeviceName'
curl -sk -u admin:$PW "https://$OMEM/api/NetworkService/Fabrics" 2>/dev/null | jq -r '.value[]?.Name'
```

**Expected result:** the MX7000 chassis, compute sleds, and fabric — **PowerEdge MX**
is a modular, fabric-based system: OME-Modular manages compute/storage sleds and the
**Scalable Fabric** (MX9116n switches) as one system, with templated deployment and
multi-chassis fabric.

**Negative test:** assign a sled to a fabric uplink set that is not configured; the
sled has no external connectivity — the Scalable Fabric must be built before sled
networking works.

**Cleanup:** none (read-only).

### Lab 2.8 — PowerEdge XE install for AI (XE Install)

**Objective:** Verify a PowerEdge XE (GPU) server's accelerator inventory.

```text
racadm -r $IDRAC -u root -p $PW hwinventory | grep -iE "GPU|Accelerator|NVLink" | head
```

```bash
nvidia-smi --query-gpu=name,memory.total,pstate --format=csv 2>/dev/null
```

**Expected result:** the GPUs/accelerators in the XE server — **PowerEdge XE**
platforms (e.g., XE9680) are dense GPU servers for AI training/inference; install
covers GPU/NVLink verification, power/cooling (often high-wattage, liquid-ready), and
the AI software stack.

**Negative test:** populate an XE server beyond its power/cooling envelope; GPUs
throttle or the PSUs alarm — XE deployment must match rack power and cooling to the
GPU load.

**Cleanup:** none (read-only).

### Lab 2.9 — Server troubleshooting (PowerEdge Operate)

**Objective:** Read the System Event Log and run diagnostics.

```text
racadm -r $IDRAC -u root -p $PW getsel
racadm -r $IDRAC -u root -p $PW get System.ServerOS
racadm -r $IDRAC -u root -p $PW techsupreport collect
```

**Expected result:** the SEL entries and a support bundle — PowerEdge
troubleshooting starts at the **System Event Log** (hardware faults, thermal, POST),
LC logs, and a **TSR** (tech-support report) for Dell; the SEL localizes a hardware
fault the OS cannot see.

**Negative test:** chase the OS for a server that fails POST; the OS never loads —
the SEL/LC logs (out-of-band) are where a pre-boot hardware fault appears.

**Cleanup:** none (read-only).

## Lab Verification

Verification means both API surfaces returned matching inventory,
the firmware job completed with its log archived, credentials and
certificates were rotated with evidence, and the MX/rack memo
defends its failure-domain math.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] iDRAC/RACADM/Redfish fluency demonstrated
- [ ] Firmware-baseline discipline exercised once end to end
- [ ] MX and XE platforms positioned with their exams
- [ ] Server ladder codes recorded from the verified table
