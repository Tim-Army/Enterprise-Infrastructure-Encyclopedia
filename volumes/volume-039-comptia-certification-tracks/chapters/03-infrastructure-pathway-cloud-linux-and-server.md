# Chapter 03: Infrastructure Pathway — Cloud+, Linux+, and Server+

## Learning Objectives

- Enumerate the CompTIA Infrastructure certifications and their current exam codes.
- Describe the domain focus of Cloud+, Linux+, and Server+.
- Map each to the encyclopedia's cloud, Linux, and Windows Server volumes.
- Explain how the Infrastructure certs build on the Core pathway.
- Build a study path for a systems or cloud administrator.

## Theory and Architecture

The **Infrastructure** pathway certifies the roles that build and operate
systems — servers, operating systems, and cloud. As verified on comptia.org
(26 July 2026):

- **CompTIA Cloud+** — exam **CV0-004** (V4) across six weighted domains:
  **Cloud architecture (23%)**, **Deployment (19%)**, **Operations (17%)**,
  **Security (19%)**, **DevOps fundamentals (10%)**, and **Troubleshooting
  (12%)** — V4 adds the **DevOps-fundamentals** domain (CI/CD, IaC, automation).
  A 90-question exam (multiple-choice and performance-based) over 90 minutes with
  a **scaled passing score of 750 (100–900)**; 2–3 years as a systems
  administrator or cloud engineer recommended. Vendor-neutral cloud across
  **multi-cloud** environments, complementing the vendor cloud volumes (AWS
  XVII, Azure XXXIII, Google Cloud XXXIV) by teaching the concepts common to all
  of them.
- **CompTIA Linux+** — exam **XK0-006** (V8; XK0-005 retiring) across five
  weighted domains: **System management (23%)**, **Services and user management
  (20%)**, **Security (18%)**, **Automation, orchestration, and scripting
  (17%)**, and **Troubleshooting (22%)** — V8 adds Python scripting, Git,
  containers, and responsible-AI practices. A 90-question exam (multiple-choice
  and performance-based) over 90 minutes with a **scaled passing score of 720
  (100–900)**; ~12 months of Linux experience recommended. It precedes the
  distribution-specific depth of **Volume XIV (RHEL 10)** and **Volume XXI
  (Ubuntu Server)** and vendor exams such as RHCSA.
- **CompTIA Server+** — exam **SK0-005** (V5) across four weighted domains:
  **Server hardware installation and management (18%)**, **Server administration
  (30%)**, **Security and disaster recovery (24%)**, and **Troubleshooting
  (28%)**. A 90-question exam (multiple-choice and performance-based) over 90
  minutes with a **scaled passing score of 750 (100–900)**; A+ and ~2 years in a
  server environment recommended. Server administration on-premises and in
  hybrid environments; it precedes the Windows-specific depth of **Volume
  XXXVI**. (Server+ has historically carried **non-expiring** status — confirm on
  the page.)

## Design Considerations

Build the Infrastructure pathway on the Core foundation: **A+ and Network+**
give the hardware and networking grounding these exams assume, and **Security+**
supplies the security concepts each infrastructure domain applies. Choose the
credential by role — **Cloud+** for cloud/multi-cloud operations, **Linux+**
for Linux administrators, **Server+** for data-center and hybrid server
administrators.

These certifications are **vendor-neutral on purpose**: Cloud+ teaches the
cloud model that AWS, Azure, and Google Cloud each implement differently, so
it pairs naturally with a vendor cloud volume rather than replacing it.
Similarly, Linux+ precedes the RHEL and Ubuntu volumes, and Server+ precedes
the Windows Server volume. All three include **performance-based questions**,
so hands-on lab time — building servers, administering Linux, deploying cloud
resources — is essential.

## Implementation and Automation

Verify the Infrastructure codes from comptia.org:

```bash
for slug in cloud linux server; do
  code=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(CV0-[0-9]{3}|XK0-[0-9]{3}|SK0-[0-9]{3})\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# cloud -> CV0-004 ; linux -> XK0-005 XK0-006 ; server -> SK0-005
```

## Validation and Troubleshooting

Map the Infrastructure certifications:

| Certification | Exam | Focus | Precedes / practice in |
| --- | --- | --- | --- |
| Cloud+ | CV0-004 | Vendor-neutral multi-cloud | Volumes XVII, XXXIII, XXXIV |
| Linux+ | XK0-006 | Linux administration | Volumes XIV, XXI |
| Server+ | SK0-005 | Server hardware/software administration | Volume XXXVI |

Common pitfalls: studying **Linux+ XK0-005** instead of the current **XK0-006**;
treating **Cloud+** as a substitute for a vendor cloud certification (it is the
vendor-neutral complement, not a replacement); and skipping the **Core**
groundwork — the Infrastructure exams assume the hardware, networking, and
security fundamentals that A+, Network+, and Security+ provide.

## Security and Best Practices

Ground the Infrastructure pathway on **Security+** so its security domains
build on real understanding, and practice the **performance-based** tasks in a
lab (a Linux VM, a server build, a free-tier cloud account). Verify the
**current exam version** — Linux+ in particular recently moved to XK0-006.
Pair each credential with the matching vendor volume for depth: Cloud+ with
AWS/Azure/GCP, Linux+ with RHEL/Ubuntu, Server+ with Windows Server. Plan **CE
renewal** (Chapter 08), noting Server+'s historically non-expiring status.

## References and Knowledge Checks

- comptia.org: certification pages for Cloud+, Linux+, Server+.
- Cross-reference: [Volume XIV (RHEL)](../volume-014-red-hat-enterprise-linux-10/README.md), [Volume XXI (Ubuntu)](../volume-021-ubuntu-server-cloud-26-04-lts/README.md), [Volume XXXVI (Windows Server)](../volume-036-windows-server-2025-active-directory/README.md).

**Knowledge checks**

1. Why is Cloud+ a complement to, not a replacement for, a vendor cloud certification?
2. What is the current Linux+ exam code, and which version did it replace?
3. Which encyclopedia volume does Server+ precede?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted exam domain** of Cloud+,
Linux+, and Server+.

**Shared prerequisites** — a Linux shell with `python3` (and `pyyaml` for one
lab), `openssl`, `git`, and standard tools; some labs use `sudo`. **Cost:** none.

### Lab 3.1 — Cloud+: Cloud architecture (23%)

**Objective:** Inspect the virtualization/containerization layer cloud
architecture builds on.

```bash
systemd-detect-virt || echo bare-metal
command -v docker podman 2>/dev/null | head -1 || echo "no container runtime"
```

**Expected result:** the hypervisor/virt type and a container runtime path (or a
clear absence) — the virtualization and containerization of cloud architecture.

**Negative test:** assume containers and VMs give the same isolation; containers
share the host kernel.

**Cleanup:** none.

### Lab 3.2 — Cloud+: Deployment (19%)

**Objective:** Author and validate an infrastructure-as-code resource
definition.

```bash
cat > /tmp/vm.json <<'JSON'
{"resource":"vm","name":"web01","cpu":2,"mem_gb":4,"disk_gb":40}
JSON
python3 -c "import json;d=json.load(open('/tmp/vm.json'));print('valid IaC:',d['name'],d['cpu'],'vCPU')"
```

**Expected result:** `valid IaC: web01 2 vCPU` — a declarative resource parsed
and validated, the essence of IaC deployment.

**Negative test:** delete a comma to break the JSON; the parser errors — IaC must
be valid to apply.

**Cleanup:** `rm -f /tmp/vm.json`.

### Lab 3.3 — Cloud+: Operations (17%)

**Objective:** Practice lifecycle, backup, and observability on a resource.

```bash
mkdir -p /tmp/vol && echo v1 > /tmp/vol/data; cp -r /tmp/vol /tmp/vol.snap; du -sh /tmp/vol
```

**Expected result:** a point-in-time snapshot copy and a size metric —
backup/recovery and observability in operations.

**Negative test:** treat the snapshot as live; changes after the snapshot are
not captured.

**Cleanup:** `rm -rf /tmp/vol /tmp/vol.snap`.

### Lab 3.4 — Cloud+: Security (19%)

**Objective:** Apply IAM-style least privilege and review exposure.

```bash
touch /tmp/cloud.key && chmod 400 /tmp/cloud.key && stat -c '%A' /tmp/cloud.key
ss -tln 2>/dev/null | head
```

**Expected result:** a read-only key (400) and listening ports — least-privilege
IAM and attack-surface review.

**Negative test:** leave the key at 644; a world-readable private key is an IAM
failure.

**Cleanup:** `rm -f /tmp/cloud.key`.

### Lab 3.5 — Cloud+: DevOps fundamentals (10%)

**Objective:** Use source control — the foundation of CI/CD.

```bash
d=$(mktemp -d); cd "$d"; git init -q; echo v1 > app.txt; git add app.txt
git -c user.email=a@b.c -c user.name=ci commit -qm init; git log --oneline
```

**Expected result:** one commit in the log — version-controlled code, the input
to a CI/CD pipeline.

**Negative test:** commit with nothing staged; there is nothing to commit.

**Cleanup:** `rm -rf "$d"`.

### Lab 3.6 — Cloud+: Troubleshooting (12%)

**Objective:** Rule out a misconfiguration by validating a config file.

```bash
printf 'server:\n  port: 8080\n  tls: true\n' > /tmp/svc.yaml
python3 -c "import yaml;yaml.safe_load(open('/tmp/svc.yaml'));print('config OK')" 2>/dev/null || echo "install pyyaml or fix syntax"
```

**Expected result:** `config OK` — a well-formed config, ruling out a
misconfiguration.

**Negative test:** indent `port` with a tab; YAML rejects tabs — a classic
misconfiguration.

**Cleanup:** `rm -f /tmp/svc.yaml`.

### Lab 3.7 — Linux+: System management (23%)

**Objective:** Review boot target, storage, and network configuration.

```bash
systemctl get-default; lsblk -o NAME,SIZE,MOUNTPOINT | head; ip -brief addr | head
```

**Expected result:** the default boot target, block devices with mountpoints,
and interface addresses — core system management.

**Negative test:** read `get-default` as the running target; it shows the
configured default.

**Cleanup:** none.

### Lab 3.8 — Linux+: Services and user management (20%)

**Objective:** Create a user and group and check a service.

```bash
sudo groupadd -f apps; sudo useradd -m -g apps -s /bin/bash svcuser 2>/dev/null; id svcuser
systemctl is-enabled cron 2>/dev/null || systemctl is-enabled crond 2>/dev/null || echo n/a
```

**Expected result:** `svcuser` with group `apps` and a service state —
user/group and service management.

**Negative test:** run `useradd svcuser` twice; the second reports the account
exists.

**Cleanup:** `sudo userdel -r svcuser 2>/dev/null; sudo groupdel apps 2>/dev/null || true`.

### Lab 3.9 — Linux+: Security (18%)

**Objective:** Harden with sudo scoping and file permissions.

```bash
sudo -l 2>/dev/null | head; touch /tmp/s.conf && chmod 640 /tmp/s.conf && stat -c '%A %G' /tmp/s.conf
```

**Expected result:** the sudo privileges summary and a group-readable 640 config
— authorization and permission hardening.

**Negative test:** set the config 666; a world-writable config violates
hardening.

**Cleanup:** `rm -f /tmp/s.conf`.

### Lab 3.10 — Linux+: Automation, orchestration, and scripting (17%)

**Objective:** Write a shell script and a Python snippet.

```bash
cat > /tmp/a.sh <<'SH'
#!/bin/bash
for s in web db cache; do echo "provisioning $s"; done
SH
bash /tmp/a.sh; python3 -c "print('py:', sum(range(1,11)))"
```

**Expected result:** three "provisioning" lines and `py: 55` — a shell loop and
a Python calculation, the automation building blocks.

**Negative test:** execute `/tmp/a.sh` without the exec bit or an interpreter;
permission denied.

**Cleanup:** `rm -f /tmp/a.sh`.

### Lab 3.11 — Linux+: Troubleshooting (22%)

**Objective:** Triage system health — disk, errors, and top processes.

```bash
df -h / | awk 'NR==2{print "root use%:",$5}'
journalctl -p err -n 3 --no-pager 2>/dev/null || dmesg | tail -3
ps -eo pid,comm,%cpu --sort=-%cpu | head -3
```

**Expected result:** root filesystem usage, recent errors, and top CPU consumers
— the troubleshooting data set.

**Negative test:** let `/` fill and expect services to keep writing; a full root
breaks logging and services.

**Cleanup:** none.

### Lab 3.12 — Server+: Server hardware installation and management (18%)

**Objective:** Enumerate storage and RAID for a server build.

```bash
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
cat /proc/mdstat 2>/dev/null | head -2 || echo "no software RAID configured"
```

**Expected result:** disks/partitions and any md RAID status — storage
deployment and capacity planning.

**Negative test:** assume more disks means redundancy; RAID 0 adds capacity but
no redundancy.

**Cleanup:** none.

### Lab 3.13 — Server+: Server administration (30%)

**Objective:** Review server roles/services and a network service.

```bash
systemctl list-units --type=service --state=running 2>/dev/null | head
getent hosts localhost; ss -uln 2>/dev/null | grep -E ':53|:67' || echo "no DNS/DHCP listener here"
```

**Expected result:** running services, name resolution, and whether DNS/DHCP
listeners exist — server roles and network services.

**Negative test:** assume a role is active because the package is installed; it
must be enabled and running.

**Cleanup:** none.

### Lab 3.14 — Server+: Security and disaster recovery (24%)

**Objective:** Encrypt server data and stage an offsite recovery copy.

```bash
echo "db-dump" > /tmp/db.sql
openssl enc -aes-256-cbc -pbkdf2 -pass pass:DR2026 -in /tmp/db.sql -out /tmp/db.sql.enc && cp /tmp/db.sql.enc /tmp/offsite.enc && ls -1 /tmp/*.enc
```

**Expected result:** an encrypted backup plus an "offsite" copy — data security
and disaster recovery.

**Negative test:** keep the only backup on the source disk; one disk failure
loses both.

**Cleanup:** `rm -f /tmp/db.sql /tmp/db.sql.enc /tmp/offsite.enc`.

### Lab 3.15 — Server+: Troubleshooting (28%)

**Objective:** Run a first-pass server diagnostic across compute and network.

```bash
uptime; free -h | awk '/Mem:/{print "mem free:",$4}'; ping -c1 -W2 127.0.0.1 >/dev/null && echo "net stack OK"
```

**Expected result:** load average, free memory, and a working network stack.

**Negative test:** read high load as CPU-bound without checking I/O wait; load
includes uninterruptible I/O.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Infrastructure pathway runs Cloud+ (CV0-004), Linux+ (XK0-006), and Server+
(SK0-005) — vendor-neutral cloud, Linux, and server administration that builds
on the Core pathway and precedes the encyclopedia's vendor cloud, Linux, and
Windows Server volumes.

- [ ] I can list the Infrastructure certs and current exam codes.
- [ ] I can explain Cloud+ as a complement to vendor cloud certs.
- [ ] I can map each to its vendor volume.
- [ ] I can build a systems/cloud administrator study path.
- [ ] I completed Labs 3.1–3.2 including each negative test.
