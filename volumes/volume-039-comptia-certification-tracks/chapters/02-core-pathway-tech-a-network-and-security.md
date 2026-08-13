# Chapter 02: Core Pathway — Tech+, A+, Network+, and Security+

## Learning Objectives

- Enumerate the CompTIA Core certifications and their current exam codes.
- Explain the intended sequence from Tech+ through Security+.
- Describe each Core exam's domain focus and format.
- Map the Core certifications to the encyclopedia's networking and security volumes.
- Build a foundational study path for a new IT professional.

## Theory and Architecture

The **Core** pathway is CompTIA's foundation and the most widely held part of
the program. As verified on comptia.org (26 July 2026), it runs in four steps:

- **CompTIA Tech+** — exam **FC0-U71** (V6; renamed from **ITF+**, IT
  Fundamentals). Foundational technology and digital literacy across six
  weighted domains: **Tech concepts and terminology (13%)**, **Infrastructure
  (24%)**, **Applications and software (18%)**, **Software development concepts
  (13%)**, **Data and database fundamentals (13%)**, and **Security (19%)**. A
  70-question, multiple-choice exam over 60 minutes with a passing score of
  **650 (900-point scale)** and no prior experience required. The entry point
  for people new to IT. (The base **FC0-U71** does not expire; an **FC0-U71-CE**
  variant carries a 5-year CE validity.)
- **CompTIA A+** — the **Core Series** (V15): two exams that must both be passed
  and both taken from the **same version** (no mixing) — **220-1201 (Core 1)**
  and **220-1202 (Core 2)**. Each is up to 90 questions (multiple-choice,
  drag-and-drop, and performance-based) over 90 minutes, with ~12 months of
  IT-support experience recommended. **Core 1** weights **Mobile devices (13%)**,
  **Networking (23%)**, **Hardware (25%)**, **Virtualization and cloud computing
  (11%)**, and **Hardware and network troubleshooting (28%)** (passing 675/900);
  **Core 2** weights **Operating systems (28%)**, **Security (28%)**, **Software
  troubleshooting (23%)**, and **Operational procedures (21%)** (passing
  700/900). A+ is the classic first professional certification for help-desk and
  desktop-support roles.
- **CompTIA Network+** — exam **N10-009** (V9) across five weighted domains:
  **Networking concepts (23%)**, **Network implementation (20%)**, **Network
  operations (19%)**, **Network security (14%)**, and **Network troubleshooting
  (24%)**. A 90-question exam (multiple-choice and performance-based) over 90
  minutes with a **scaled passing score of 720 (100–900)**; A+ and 9–12 months
  of networking experience recommended. Vendor-neutral networking before a
  vendor track such as Cisco CCNA (Volume III) or Juniper JNCIA (Volume XXXI).
- **CompTIA Security+** — exam **SY0-701** (V7). Core cybersecurity across five
  weighted domains: **General security concepts (12%)**, **Threats,
  vulnerabilities, and mitigations (22%)**, **Security architecture (18%)**,
  **Security operations (28%)**, and **Security program management and oversight
  (20%)**. A 90-question exam (multiple-choice and performance-based) over 90
  minutes with a **scaled passing score of 750 (100–900)**; Network+ and ~2
  years of security/sysadmin experience recommended. **The most widely required
  entry-level security certification**, and a DoD 8140/8570 baseline.

## Design Considerations

Sequence the Core pathway by experience. A complete beginner starts at
**Tech+**; someone already comfortable with computers can begin at **A+**.
**Network+** and **Security+** follow, and CompTIA recommends (but does not
require) **A+ before Network+ before Security+** — the order builds the mental
model each later exam assumes. **Security+ is the anchor** of most IT-security
careers and often the first CompTIA cert an employer mandates, so many
learners target it directly with prior networking knowledge.

Because A+ requires **two exams**, budget for both. All four Core exams include
**performance-based questions**, so hands-on practice — building a PC,
configuring a small network, hardening a system — matters as much as reading.
The Core certifications map straight into the encyclopedia's foundations
(Volumes I, II, IV) and precede every vendor networking and security track.

## Implementation and Automation

Verify the Core codes from comptia.org:

```bash
for slug in tech a network security; do
  code=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(FC0-U[0-9]{2}|220-1[0-9]{3}|N10-[0-9]{3}|SY0-[0-9]{3})\b' | sort -u | tr '\n' ' ')
  echo "$slug -> ${code:-'(see page; A+ shows Core 1/Core 2)'}"
done
# tech -> FC0-U71 ; network -> N10-009 ; security -> SY0-701 ; A+ -> 220-1201 / 220-1202
```

## Validation and Troubleshooting

Map the Core certifications:

| Certification | Exam(s) | Focus | Precedes / practice in |
| --- | --- | --- | --- |
| Tech+ | FC0-U71 | Digital and IT literacy | Volume I |
| A+ | 220-1201 + 220-1202 | IT support, hardware, OS, troubleshooting | Volume IV |
| Network+ | N10-009 | Vendor-neutral networking | Volume II; Cisco III, Juniper XXXI |
| Security+ | SY0-701 | Core cybersecurity | Volume X; the security tracks |

Common pitfalls: studying the **retired** Network+ N10-008 or Security+ SY0-601
instead of N10-009 / SY0-701; forgetting that **A+ needs both** Core 1 and Core
2; confusing **Tech+** with the old ITF+ name (same lineage, new name and code
FC0-U71); and underestimating the **performance-based questions**, which reward
hands-on practice over memorization.

## Security and Best Practices

Anchor an IT-security career on **Security+**, and build the groundwork with
**A+** and **Network+** so its concepts land on real understanding. Practice
the **performance-based** skills hands-on. Verify the **current exam version**
before studying, and plan **CE renewal** (Chapter 08). For DoD and regulated
environments, note that **A+, Network+, and Security+** are recognized baseline
certifications under **DoD 8140/8570**.

## References and Knowledge Checks

- comptia.org: certification pages for Tech+, A+, Network+, Security+.
- Cross-reference: [Volume II — Network Engineering Foundations](../../volume-002-network-engineering-foundations/README.md); [Volume X — Enterprise Cybersecurity](../../volume-010-enterprise-cybersecurity/README.md).

**Knowledge checks**

1. How many exams does A+ require, and what are their current codes?
2. What is the recommended order through the Core pathway, and is it enforced?
3. Which Core certification is the most widely required entry-level security credential?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted exam domain** of each Core
certification (Tech+, A+ Core 1 and Core 2, Network+, Security+).

**Shared prerequisites** — a Linux shell with `python3`, `sqlite3`, `openssl`,
and standard tools (`ip`, `ss`, `ping`, `lsblk`, `lscpu`, `tar`); a few labs use
`sudo`. **Cost:** none.

### Lab 2.1 — Tech+: Tech concepts and terminology (13%)

**Objective:** Convert between notational systems and read storage units.

```bash
python3 -c "n=42; print(f'dec={n} bin={bin(n)} hex={hex(n)} oct={oct(n)}')"
echo "1 GiB in bytes = $((1024*1024*1024))"
```

**Expected result:** `dec=42 bin=0b101010 hex=0x2a oct=0o52` and `1073741824` —
the four notational systems and a binary storage unit.

**Negative test:** treat 1 GB (10^9) and 1 GiB (2^30) as identical; they differ.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Tech+: Infrastructure (24%)

**Objective:** Inventory computing components — CPU, RAM, and storage.

```bash
lscpu | grep -E 'Model name|^CPU\(s\)'; free -h | awk '/Mem:/{print "RAM:",$2}'
lsblk -d -o NAME,SIZE,TYPE
```

**Expected result:** the CPU model and core count, total RAM, and local disks —
internal components and storage.

**Negative test:** expect `lsblk` to list network shares; it shows local block
devices only.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Tech+: Applications and software (18%)

**Objective:** Identify the OS, its file system, and available applications.

```bash
. /etc/os-release; echo "OS: $NAME $VERSION_ID"
findmnt -no FSTYPE,TARGET /; command -v python3 || true
```

**Expected result:** OS name/version, the root file-system type (e.g., ext4),
and an application path — operating systems and software.

**Negative test:** assume every distro uses the same file system; `findmnt`
shows it varies (ext4/xfs/btrfs).

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Tech+: Software development concepts (13%)

**Objective:** Apply variables, a loop, branching, and a data type.

```bash
python3 - <<'PY'
for i in range(1, 6):
    print(i, "even" if i % 2 == 0 else "odd", type(i).__name__)
PY
```

**Expected result:** lines 1–5 labeled odd/even with type `int` — looping,
branching, and a data type.

**Negative test:** compare `"5" == 5`; a string and an int are not equal.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.5 — Tech+: Data and database fundamentals (13%)

**Objective:** Create a table with a primary key, insert rows, and query.

```bash
sqlite3 /tmp/tech.db "CREATE TABLE assets(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO assets(name) VALUES('router'),('switch'); SELECT count(*) FROM assets;"
```

**Expected result:** `2` — a relational table, two rows, and an aggregate query.

**Negative test:** insert a second row with `id=1`; the PRIMARY KEY rejects the
duplicate.

**Rollback:** `rm -f /tmp/tech.db`.

### Lab 2.6 — Tech+: Security (19%)

**Objective:** Apply integrity (hashing) and confidentiality (encryption).

```bash
echo "secret data" > /tmp/f.txt; sha256sum /tmp/f.txt
openssl enc -aes-256-cbc -pbkdf2 -pass pass:Demo2026 -in /tmp/f.txt -out /tmp/f.enc && file /tmp/f.enc
```

**Expected result:** a 64-hex SHA-256 digest (integrity) and an encrypted blob
(confidentiality at rest).

**Negative test:** `cat /tmp/f.enc`; the ciphertext is unreadable without the
passphrase.

**Rollback:** `rm -f /tmp/f.txt /tmp/f.enc`.

### Lab 2.7 — A+ Core 1: Mobile devices (13%)

**Objective:** Enumerate the peripheral/mobile interfaces an A+ tech configures.

```bash
lsusb | head; command -v bluetoothctl >/dev/null && bluetoothctl --version || echo "no bluetooth stack"
```

**Expected result:** USB devices/hubs and the Bluetooth stack version (or a clear
absence note) — accessory interfaces.

**Negative test:** assume `lsusb` shows cellular signal; it enumerates USB only.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.8 — A+ Core 1: Networking (23%)

**Objective:** Read the SOHO network config — IP addressing and gateway.

```bash
ip -brief addr; ip route | grep default
```

**Expected result:** interfaces with IPv4/IPv6 addresses and the default gateway
— SOHO IP addressing.

**Negative test:** treat a 169.254.x.x (APIPA) address as healthy DHCP; APIPA
signals DHCP failure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.9 — A+ Core 1: Hardware (25%)

**Objective:** Inspect installed hardware — CPU, RAM, and disk type.

```bash
lscpu | grep -E 'Architecture|Core\(s\)'; free -m | awk '/Mem:/{print "RAM MB:",$2}'
lsblk -d -o NAME,SIZE,ROTA
```

**Expected result:** architecture and cores, RAM in MB, and disks with ROTA
(1=HDD, 0=SSD/NVMe) — installed components.

**Negative test:** assume ROTA=0 means NVMe specifically; it means
non-rotational — check the transport.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.10 — A+ Core 1: Virtualization and cloud computing (11%)

**Objective:** Detect virtualization and name the cloud service models.

```bash
systemd-detect-virt || echo none
echo "Service models: IaaS < PaaS < SaaS (rising provider responsibility)"
```

**Expected result:** the hypervisor (e.g., kvm) or `none` on bare metal, plus
the IaaS/PaaS/SaaS model note.

**Negative test:** assume `none` proves it is not a cloud VM; hardened guests can
hide the hypervisor.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.11 — A+ Core 1: Hardware and network troubleshooting (28%)

**Objective:** Isolate a connectivity fault by layer.

```bash
ip link show | grep -E 'state (UP|DOWN)'; ping -c1 -W2 127.0.0.1 >/dev/null && echo "loopback OK"
```

**Expected result:** each NIC's link state and a working loopback — separating
layer-1/2 from higher layers.

**Negative test:** treat a DOWN interface as a DNS problem; link-down is physical.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.12 — A+ Core 2: Operating systems (28%)

**Objective:** Identify the OS and inspect the root mount.

```bash
uname -sr; . /etc/os-release && echo "$PRETTY_NAME"; mount | awk '$3=="/"{print $1,$5}'
```

**Expected result:** kernel + distro and the root device/type — OS and
file-system basics.

**Negative test:** assume `uname` reveals the distro; it shows the kernel — use
/etc/os-release.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.13 — A+ Core 2: Security (28%)

**Objective:** Apply an access control with least-privilege permissions.

```bash
touch /tmp/acl.txt; chmod 600 /tmp/acl.txt; stat -c '%A %U' /tmp/acl.txt
```

**Expected result:** `-rw------- <user>` — owner-only read/write, a
least-privilege control.

**Negative test:** `chmod 777 /tmp/acl.txt`; world-writable is insecure for
sensitive files.

**Rollback:** `rm -f /tmp/acl.txt`.

### Lab 2.14 — A+ Core 2: Software troubleshooting (23%)

**Objective:** Gather the data a software-troubleshooting workflow starts from.

```bash
systemctl is-active cron 2>/dev/null || systemctl is-active crond 2>/dev/null || echo inactive
ps -e --sort=-%mem | head -3
```

**Expected result:** a service state and the top memory consumers.

**Negative test:** kill a random PID to "fix" memory; identify the offending
process first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.15 — A+ Core 2: Operational procedures (21%)

**Objective:** Perform and verify a backup — a core operational procedure.

```bash
mkdir -p /tmp/src && echo data > /tmp/src/file
tar -czf /tmp/backup.tgz -C /tmp src && tar -tzf /tmp/backup.tgz
```

**Expected result:** `src/` and `src/file` listed from the archive — a verified
backup.

**Negative test:** assume creating the archive proves recoverability; always
verify with `-t`.

**Rollback:** `rm -rf /tmp/src /tmp/backup.tgz`.

### Lab 2.16 — Network+: Networking concepts (23%)

**Objective:** Map transport-layer sockets and subnet an IPv4 network.

```bash
ss -tlnp 2>/dev/null | head -4
python3 -c "import ipaddress; n=ipaddress.ip_network('192.168.10.0/26'); print(n,'usable=',n.num_addresses-2)"
```

**Expected result:** listening TCP sockets and a /26 with 62 usable hosts —
ports/protocols and IPv4 subnetting.

**Negative test:** claim /26 gives 64 usable hosts; network + broadcast are
reserved, so 62.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.17 — Network+: Network implementation (20%)

**Objective:** Inspect routing and add a static route.

```bash
ip route show
sudo ip route add 203.0.113.0/24 dev lo 2>/dev/null && ip route | grep 203.0.113
```

**Expected result:** the routing table plus the new static route via lo — a
routing implementation task.

**Negative test:** add the route to a non-existent interface; the kernel rejects
it.

**Rollback:** `sudo ip route del 203.0.113.0/24 dev lo 2>/dev/null || true`.

### Lab 2.18 — Network+: Network operations (19%)

**Objective:** Collect the interface counters operations baselines from.

```bash
ip -s link show | awk '/^[0-9]+:/{i=$2} /RX:/{getline; print i,"RX bytes",$1}'
```

**Expected result:** per-interface RX byte counters — monitoring data for
baselines.

**Negative test:** treat one reading as a baseline; a baseline needs samples
over time.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.19 — Network+: Network security (14%)

**Objective:** Review the host firewall rule set (a logical security control).

```bash
sudo iptables -L INPUT -n --line-numbers 2>/dev/null | head || echo "try: sudo nft list ruleset"
```

**Expected result:** the INPUT chain policy and rules.

**Negative test:** assume an empty rule set is "secure"; a default-ACCEPT empty
policy permits everything.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.20 — Network+: Network troubleshooting (24%)

**Objective:** Separate connectivity from name resolution per the methodology.

```bash
ping -c1 -W2 1.1.1.1 >/dev/null && echo "L3 OK"
getent hosts example.com >/dev/null && echo "DNS OK" || echo "DNS FAIL"
```

**Expected result:** layer-3 reachability and DNS status — isolating the fault
domain.

**Negative test:** conclude "internet down" when only DNS fails; L3 can be up
while DNS is broken.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.21 — Security+: General security concepts (12%)

**Objective:** Demonstrate integrity (hashing) and a PKI keypair.

```bash
echo hello | sha256sum
openssl genrsa -out /tmp/k.pem 2048 2>/dev/null && openssl rsa -in /tmp/k.pem -pubout -out /tmp/k.pub 2>/dev/null && echo "keypair created"
```

**Expected result:** a SHA-256 digest and an RSA private/public keypair —
hashing and PKI.

**Negative test:** publish `/tmp/k.pem` as the "public" key; the private key must
stay secret — share `k.pub` only.

**Rollback:** `rm -f /tmp/k.pem /tmp/k.pub`.

### Lab 2.22 — Security+: Threats, vulnerabilities, and mitigations (22%)

**Objective:** Read the service attack surface and name the hardening action.

```bash
systemctl list-unit-files --state=enabled --type=service 2>/dev/null | head
echo "Mitigation: mask unused services -> systemctl disable --now <svc>"
```

**Expected result:** enabled services (attack surface) and the hardening step.

**Negative test:** disable sshd on a box you reach remotely; hardening must not
sever required access.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.23 — Security+: Security architecture (18%)

**Objective:** Protect data at rest and plan resilience with a backup copy.

```bash
echo "PII" > /tmp/d.txt
openssl enc -aes-256-cbc -pbkdf2 -pass pass:Arch2026 -in /tmp/d.txt -out /tmp/d.enc && cp /tmp/d.enc /tmp/d.enc.bak && ls -1 /tmp/d.enc*
```

**Expected result:** an encrypted data file plus a backup copy — data protection
and recovery.

**Negative test:** store the passphrase beside the ciphertext; key and data must
be separated.

**Rollback:** `rm -f /tmp/d.txt /tmp/d.enc /tmp/d.enc.bak`.

### Lab 2.24 — Security+: Security operations (28%)

**Objective:** Review authentication events — the data SecOps monitors.

```bash
last -n 5 2>/dev/null || journalctl -n 5 --no-pager 2>/dev/null || echo "no log source"
echo "SOC: alert on repeated failed logons"
```

**Expected result:** recent login/journal events for monitoring and incident
response.

**Negative test:** treat one failed login as a breach; correlate volume/pattern
first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.25 — Security+: Security program management and oversight (20%)

**Objective:** Produce a minimal risk register (a governance artifact).

```bash
printf 'risk,likelihood,impact,owner\nphishing,High,High,SecOps\nstale-patch,Med,High,IT\n' > /tmp/risk.csv
column -s, -t /tmp/risk.csv
```

**Expected result:** a formatted risk register with likelihood, impact, and
owner.

**Negative test:** track risks without an owner; unowned risks are not managed.

**Rollback:** `rm -f /tmp/risk.csv`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Core pathway runs Tech+ (FC0-U71), A+ (220-1201 + 220-1202), Network+
(N10-009), and Security+ (SY0-701), in that recommended order. It is the
vendor-neutral foundation beneath every networking and security track, anchored
by Security+, with performance-based questions that reward hands-on practice.

- [ ] I can list the Core certifications and current exam codes.
- [ ] I know A+ requires two exams.
- [ ] I can map the Core certs to the foundation and vendor volumes.
- [ ] I can build a foundational study path anchored on Security+.
- [ ] I completed Labs 2.1–2.2 including each negative test.
