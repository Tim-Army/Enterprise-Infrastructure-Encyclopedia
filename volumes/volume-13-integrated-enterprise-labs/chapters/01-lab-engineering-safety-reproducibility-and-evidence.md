# Chapter 01: Lab Engineering, Safety, Reproducibility, and Evidence

![Lab flow for this chapter: ctrl01 runs evidence.sh, which wraps every lab command, captures its output to a timestamped log, and appends a SHA-256 checksum to a manifest. Isolation is confirmed: a traceroute toward a real internet address never shows a lab address once it leaves ctrl01, and a ping to an illustrative RFC 5737 address fails to route anywhere outside the lab. A hypervisor snapshot is taken, a marker file is created, and reverting to the snapshot removes the marker, proving rollback actually works before any later chapter's negative test depends on it. As a negative test, a static route misdirecting lab traffic at the real gateway still fails to reach anything, confirming the isolation holds even under a misconfiguration attempt.](../../../diagrams/volume-13-integrated-enterprise-labs/chapter-01-lab-scaffold-evidence-rollback-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: the reference lab's evidence-capture pipeline and a hypervisor snapshot/rollback cycle, verified before the volume's later chapters rely on it.*

## Learning Objectives

- Explain why Volume XIII uses a single, versioned reference lab topology
  instead of a fresh environment per chapter, and what that trades away.
- Define a lab addressing plan, naming convention, and domain namespace that
  stays collision-free with production networks and with a home internet
  connection.
- Build a topology-as-code manifest and an evidence-capture workflow that
  every later chapter in this volume reuses without modification.
- Apply change-control and rollback discipline (snapshots, tagged commits) to
  a lab environment so failed experiments are cheap to undo.
- Produce a lab evidence bundle — command transcripts, checksums, and a
  timeline — that would satisfy an external technical reviewer.

## Theory and Architecture

Every chapter in this volume performs a real, multi-system change against a
shared lab environment: identity and DNS in [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md), campus and WAN
networking in [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md), virtualization and storage in [Chapter 04](04-virtualization-storage-and-data-protection-lab.md), hybrid
cloud and Kubernetes in [Chapter 05](05-hybrid-cloud-kubernetes-and-platform-services-lab.md), infrastructure as code in [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md),
zero trust and incident response in [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md), observability in [Chapter 08](08-observability-operations-and-major-incident-lab.md),
and a full resilience and decommissioning exercise in [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md). That only
works if every chapter agrees on the same hostnames, addressing, and domain
before any of them touch a keyboard. This chapter is that agreement — the
reference lab this entire volume builds against — plus the safety and
evidence discipline needed to run it responsibly.

This is lab engineering in the same sense [Volume I, Chapter 02](../../volume-01-enterprise-engineering-foundations/chapters/02-repository-architecture.md) (Repository
Architecture) and [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) (Automation Architecture) treat a production
repository: a lab is an artifact with a declared desired state, not a
collection of ad hoc changes an engineer remembers making. [Volume I](../../volume-01-enterprise-engineering-foundations/README.md),
[Chapter 08](08-observability-operations-and-major-incident-lab.md) (Infrastructure Lifecycle Management) and [Volume XII, Chapter 01](../../volume-12-resilience-lifecycle-management/chapters/01-resilience-engineering-and-critical-service-design.md)
(Resilience Engineering and Critical-Service Design) both assume the reader
can stand up a disposable, representative environment to validate a design
before it reaches production; this chapter is the mechanics of doing that
safely and repeatably.

### The Volume XIII reference lab

The reference lab represents **Meridian Industrial Group**, a fictitious
manufacturing and logistics enterprise used only for lab purposes in this
volume. Two sites and one cloud landing zone give later chapters enough
topology to exercise redundancy, failover, and hybrid connectivity without
requiring an implausibly large lab budget.

| Element | Value | Notes |
| --- | --- | --- |
| Internal AD DNS domain / Kerberos realm | `corp.meridian.example` | NetBIOS `CORP`; uses the IANA-reserved `.example` TLD ([RFC 2606](https://www.rfc-editor.org/rfc/rfc2606)), never a real domain |
| Public-facing DNS zone (illustrative) | `meridian.example` | Also reserved; used for any "internet-facing" record in later chapters |
| Lab supernet | `10.13.0.0/16` | [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) space, chosen to key off the volume number |
| HQ site code | `HQ` | Primary site: identity, core network, virtualization, security, observability |
| Branch/DR site code | `BR1` | Secondary site: WAN/VPN peer, DR target, resilience-test target |
| Cloud landing zone | `CLOUD1` | Hybrid connectivity target for Chapters 05 and 09 |
| Illustrative internet/public ranges | `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` | [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737) documentation ranges for HQ, BR1, and cloud internet edges |

VLAN and subnet assignments used from [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) onward:

| VLAN | Subnet | Purpose |
| --- | --- | --- |
| 110 | 10.13.10.0/24 | HQ core services (DCs, NTP, automation controller) |
| 120 | 10.13.20.0/24 | HQ user/endpoint |
| 130 | 10.13.30.0/24 | HQ management/out-of-band |
| 140 | 10.13.40.0/24 | HQ wireless and guest |
| 150/151 | 10.13.50.0/24, 10.13.51.0/24 | HQ storage and vMotion |
| 199 | 10.13.99.0/24 | Security and observability tooling |
| — | 10.13.60.0/24, 10.13.61.0/24 | BR1 server/user and management |
| — | 10.13.70.0/24 | HQ–BR1 WAN transit |
| — | 10.13.80.0/24 | Cloud VPN/transit-gateway attachment |

Hostnames follow `<role><site-instance>` in lowercase — `dc01`, `dc02`,
`esxi-a01`, `vcsa01`, `ctrl01`, `siem01` — so a hostname alone tells a reader
its role without consulting a separate legend. Every later chapter reuses
this table rather than inventing new names; treat it as this volume's
equivalent of a production IP address management (IPAM) record.

## Design Considerations

- **Physical, virtual, or nested.** A fully physical lab (real switches,
  real ESXi hosts) is the most representative but the least portable. A
  nested lab (ESXi-on-ESXi, or a single beefy workstation running VMware
  Workstation/Fusion or Cisco Modeling Labs) is what most readers will use
  for this volume; every chapter's lab notes where nesting changes expected
  behavior (notably NIC promiscuous mode for nested hypervisors and MTU for
  nested overlay networks).
- **Isolation from production and from the internet uplink.** The lab
  supernet must never be routed toward a real corporate network. Terminate
  it behind NAT on a dedicated lab router/firewall interface, and use the
  [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737) ranges from the table above for anything meant to represent "the
  internet" so no lab traffic can be mistaken for a real destination.
- **Reproducibility model.** Following the pattern established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md),
  Chapter 01, this volume combines a declarative topology manifest (below)
  with idempotent automation, built out fully in [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md). Earlier
  chapters use manual steps deliberately, so the reader understands what the
  automation in [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) is replacing.
- **Change control in a lab.** A lab without change control teaches bad
  habits. Every configuration change in this volume is expected to be
  preceded by a hypervisor snapshot or a Git commit, and every destructive
  step is called out as a **negative test** with an explicit recovery step,
  never left as an unrecoverable dead end.
- **Evidence as a deliverable, not an afterthought.** A validation step that
  is not captured did not happen, from a review standpoint. This chapter
  defines a lightweight evidence-capture convention — timestamped,
  checksummed transcripts — that every later Hands-On Lab references instead
  of redefining.

## Implementation and Automation

Two artifacts anchor the reference lab: a topology manifest and an evidence
wrapper. Both are created once, in this chapter's lab, and reused for the
rest of the volume.

The topology manifest is a plain YAML file the reader keeps alongside their
own lab notes (not committed to this repository, which does not store
reader lab state):

```yaml
# topology.yml — Volume XIII reference lab (Meridian Industrial Group)
lab:
  supernet: 10.13.0.0/16
  domain: corp.meridian.example
  sites:
    HQ:
      vlans:
        110: { subnet: 10.13.10.0/24, purpose: core-services }
        120: { subnet: 10.13.20.0/24, purpose: user-endpoint }
        130: { subnet: 10.13.30.0/24, purpose: management }
        140: { subnet: 10.13.40.0/24, purpose: wireless-guest }
        150: { subnet: 10.13.50.0/24, purpose: storage }
        151: { subnet: 10.13.51.0/24, purpose: vmotion }
        199: { subnet: 10.13.99.0/24, purpose: security-observability }
    BR1:
      vlans:
        160: { subnet: 10.13.60.0/24, purpose: server-user }
        161: { subnet: 10.13.61.0/24, purpose: management }
  wan_transit: 10.13.70.0/24
  cloud_transit: 10.13.80.0/24
  public_ranges:
    hq_edge: 192.0.2.0/24
    br1_edge: 198.51.100.0/24
    cloud_edge: 203.0.113.0/24
```

The evidence wrapper is a small shell script that timestamps and checksums
the output of any lab command, so validation steps in later chapters produce
a durable, tamper-evident artifact instead of a terminal scrollback that
disappears on the next `clear`:

```bash
#!/usr/bin/env bash
# evidence.sh — run a command, capture its output, and checksum the result
set -euo pipefail

EVID_DIR="${EVID_DIR:-$HOME/lab-evidence}"
mkdir -p "${EVID_DIR}"

ts="$(date -u +%Y%m%dT%H%M%SZ)"
slug="$(echo "$1" | tr -c 'a-zA-Z0-9' '-' | sed 's/-\+/-/g' | cut -c1-40)"
out="${EVID_DIR}/${ts}_${slug}.log"

{
  echo "# command: $*"
  echo "# started (UTC): ${ts}"
  echo "---"
  eval "$@" 2>&1
  echo "---"
  echo "# exit code: $?"
} | tee "${out}"

sha256sum "${out}" >> "${EVID_DIR}/manifest.sha256"
echo "Evidence written: ${out}"
```

Every Hands-On Lab from [Chapter 02](02-integrated-identity-dns-time-and-core-services-lab.md) onward assumes `evidence.sh "<command>"`
is available on the automation controller (`ctrl01`) and, where practical,
wraps expected-result checks in it so the checkpoint has a saved artifact.

## Validation and Troubleshooting

- **Confirm isolation before building anything else.** From a lab host, run
  a traceroute toward a real external address and confirm it never traverses
  an interface configured with the `10.13.0.0/16` supernet; then confirm a
  traceroute toward `203.0.113.1` (the illustrative cloud edge) resolves
  only inside the lab. Mixing these up is the single most common lab-safety
  defect in a nested environment.
- **Common failure: NIC promiscuous mode on nested hypervisors.** If a
  nested ESXi host or a nested Kubernetes node cannot pass traffic for VMs
  or pods it did not originate, the parent vSwitch/port group almost always
  needs "Promiscuous Mode" and "Forged Transmits" set to Accept. This
  recurs in Chapters 04 and 05 and is diagnosed here once so later chapters
  can simply reference it.
- **Common failure: MTU mismatches across nested overlays.** VXLAN,
  IPsec, and container CNI overlays each add encapsulation overhead; a
  1500-byte physical/virtual MTU with an 1500-byte overlay MTU causes silent
  fragmentation or black-holed large packets. Verify with `ping -M do -s
  1472 <target>` (Linux) before layering another tunnel on top.
- **Verify the evidence pipeline itself.** Run `evidence.sh "echo test"` and
  confirm both the log file and a corresponding line in `manifest.sha256`
  exist; a broken evidence pipeline should be caught here, not discovered
  missing during [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md)'s capstone report.
- **Verify snapshot/rollback works before relying on it.** Take a snapshot,
  make a trivial change, revert, and confirm the change is gone. An
  environment where rollback has never been tested is not a safety net.

## Security and Best Practices

- Use lab-only credentials everywhere. Never reuse a production password,
  API key, or SSH key inside the reference lab, even temporarily — treat the
  lab as a separate trust boundary from day one.
- Keep the lab supernet unroutable from production and from any network
  segment with real user traffic; a lab VLAN that can reach a production
  default gateway is a lab that can also be reached from production.
- Store lab secrets (service account passwords, API tokens generated in
  later chapters) in a lab-scoped secrets store or, at minimum, a file
  excluded from version control — the automation work in [Chapter 06](06-infrastructure-as-code-and-automated-delivery-lab.md) depends
  on this being right from the start.
- Tag every lab VM, cloud resource, and Git branch with an owner and an
  expiration/teardown date. [Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md)'s decommissioning exercise depends on
  being able to enumerate "everything this volume created" without guessing.
- Snapshot before any destructive step, and confirm the snapshot restores
  cleanly before proceeding — do not discover a broken snapshot during an
  actual failure.
- Classify evidence bundles like any other operational data: they may
  contain hostnames, internal addressing, and configuration detail that
  should not leave the lab's own storage without review, even though the
  underlying environment is disposable.

## References and Knowledge Checks

**References**

- [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) — *Address Allocation for Private Internets*.
- [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737) — *IPv4 Address Blocks Reserved for Documentation*.
- [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606) — *Reserved Top Level DNS Names*.
- [Volume I](../../volume-01-enterprise-engineering-foundations/README.md), Chapters 02–03 and 08 — repository architecture, automation
  architecture, and infrastructure lifecycle management.
- [Volume XII, Chapter 01](../../volume-12-resilience-lifecycle-management/chapters/01-resilience-engineering-and-critical-service-design.md) — resilience engineering and critical-service
  design.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated baseline for
  every platform used across this volume's labs.

**Knowledge checks**

1. Why does this volume use [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737) documentation ranges for anything
   representing "the internet" instead of real public IP addresses?
2. What two artifacts does this chapter establish that every later chapter's
   Hands-On Lab depends on?
3. Why is an untested snapshot not a safety net?
4. Name two ways a nested lab environment's behavior can diverge from a
   physical one, and how each is diagnosed.

## Hands-On Lab

Volume XIII integrates Volumes I–XII into one continuous reference environment. This chapter's labs
establish the **lab-engineering discipline** — safety, reproducibility, and evidence — that every
later integrated lab depends on. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 1.1–1.4** — a hypervisor or cloud account for the reference
environment, `git`, and Terraform/Ansible (Volumes I, IX). **Cost:** none beyond lab resources.

### Lab 1.1 — Reproducible environment definition (Topic: Reproducibility)

**Objective:** Define the reference environment as code, not by hand.

```bash
mkdir -p ~/lab-env && cd ~/lab-env && git init -q
cat > topology.md <<'EOF'
# Reference environment (built across Ch02-09)
identity/dns/ntp (Ch02) | network fabric (Ch03) | virtualization+storage (Ch04)
cloud/k8s (Ch05) | IaC/CI (Ch06) | security (Ch07) | observability (Ch08) | resilience (Ch09)
EOF
git add -A && git commit -qm "lab: define reference topology"
```

**Expected result:** the environment's definition and topology are version-controlled from the start —
integrated labs must be **reproducible**: the whole environment is defined as code (Volume I/IX), so
it can be rebuilt identically after a mistake, which is what makes destructive experimentation safe.

**Negative test:** build the reference environment by hand with no code/topology record; a mistake
means rebuilding from memory — a code-defined environment can be rebuilt on demand.

**Cleanup:** none (this repo is the environment's source of truth).

### Lab 1.2 — Safe experimentation with snapshots (Topic: Safety)

**Objective:** Make every change reversible before you make it.

```bash
# Before any risky change, snapshot the affected VM(s) (hypervisor-specific):
#   virsh snapshot-create-as <vm> pre-change     # libvirt/KVM
#   qm snapshot <vmid> pre-change                # Proxmox (Volume XXVI)
echo "snapshot taken -> change -> verify -> keep or 'snapshot-revert' to roll back"
```

**Expected result:** a pre-change snapshot exists so any change can be instantly reverted — safety in
an integrated lab means every risky step is reversible (snapshots, backups, IaC rebuild), so you can
experiment aggressively and recover in seconds rather than fearing every change.

**Negative test:** make a risky change to the shared environment with no snapshot/backup; a mistake
cascades across the integrated services and recovery is slow — the snapshot is the undo button.

**Cleanup:** delete pre-change snapshots once a change is confirmed good.

### Lab 1.3 — Evidence capture (Topic: Evidence)

**Objective:** Record verifiable evidence of each lab's outcome.

```bash
cd ~/lab-env && mkdir -p evidence
{ date -u; echo "lab: baseline"; uname -a; } > evidence/ch01-baseline.txt
sha256sum evidence/ch01-baseline.txt >> evidence/manifest.sha256
cat evidence/manifest.sha256
```

**Expected result:** timestamped, hashed evidence of the lab's state — capturing evidence (command
output, config, hashes) makes results verifiable and auditable, and turns each integrated lab into a
record you (or an assessor) can confirm was actually completed, not just claimed.

**Negative test:** claim a lab "worked" with no captured output/evidence; there is nothing to verify or
troubleshoot against later — evidence capture is what makes the `Lab verified by` sign-off meaningful.

**Cleanup:** none (retain evidence).

### Lab 1.4 — The teardown and rebuild loop (Topic: Lifecycle discipline)

**Objective:** Prove the environment can be destroyed and rebuilt from code.

```bash
cd ~/lab-env
# The whole environment provisions from IaC (Volume IX): terraform apply / ansible-playbook site.yml
# Prove the loop: destroy a component and rebuild it from code, confirming identical state.
echo "break -> rebuild-from-code -> re-verify == the loop every chapter's lab relies on"
```

**Expected result:** any component can be torn down and rebuilt identically from code — the
break/rebuild loop (Volumes IX, XIV, XXVI) is the core lab-engineering skill: because the environment
is code-defined and evidence-verified, you learn by breaking and fixing, confident you can always
return to a known-good state.

**Negative test:** treat the reference environment as precious and never practice teardown/rebuild;
the first real failure finds the rebuild path untested — practicing the loop is what makes recovery
reliable.

**Cleanup:** none (the loop is the intended practice).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter established the single reference lab — addressing, naming, and
domain — that every remaining chapter in Volume XIII builds on, plus two
reusable artifacts: a topology manifest and an evidence-capture wrapper.
Isolation from production and from the real internet was verified before any
service was deployed, and snapshot/rollback was tested rather than assumed.
Treat this chapter's scaffold as load-bearing: later negative tests and
[Chapter 09](09-enterprise-resilience-and-lifecycle-capstone.md)'s capstone report both depend on it existing and working.

- [ ] Can explain why this volume shares one lab topology across all nine
      chapters instead of building isolated environments per chapter.
- [ ] Built and tested the evidence-capture wrapper and topology manifest.
- [ ] Verified lab-to-internet isolation and diagnosed a deliberately
      introduced incorrect route.
- [ ] Verified snapshot/rollback actually restores prior state.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
