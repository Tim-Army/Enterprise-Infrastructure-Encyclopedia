import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-04-enterprise-systems-administration"


def ch01():
    c = Canvas(960, 660,
        title="Chapter 1 Hands-On Lab: Bastion-Mediated Access and Inventory-Drift Check",
        subtitle="web01 is reachable only via a ProxyJump through bastion01, enforced at the network layer by hosts.allow",
        svg_title="Chapter 1 lab topology: a bastion host mediating SSH access to a workload host, with an inventory-drift check",
        svg_desc="The administrator workstation's SSH config routes all access to web01 through bastion01 via "
                  "ProxyJump, using a dedicated lab key. web01's hosts.allow/hosts.deny restrict sshd to only "
                  "accept connections from bastion01's address (10.0.0.10). A simple inventory-drift check compares "
                  "a static inventory file (web01, web02) against hosts that actually respond: web01 is OK, web02 "
                  "is flagged as DRIFT because it does not exist. As a negative test, a direct connection attempt "
                  "to web01 that bypasses bastion01 (ProxyJump removed) times out or is refused, confirming the "
                  "management-plane control is enforced at the network layer, not by convention.")
    c.node_box(60, 160, 220, 110, "mgmt", [
        Line("Administrator Workstation", 12.5, 700, "#111827"),
        Line("~/.ssh/config: ProxyJump", 10.5, 400, "#374151"),
        Line("id_ed25519_lab", 10, 400, "#6b7280"),
    ])
    c.node_box(380, 160, 220, 110, "mgmt", [
        Line("bastion01", 14, 700, "#111827"),
        Line("10.0.0.10", 11.5, 700, "#1d4ed8"),
        Line("management-plane host", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 160, 220, 110, "alt", [
        Line("web01", 14, 700, "#111827"),
        Line("sshd: allow 10.0.0.10 only", 11, 700, "#14532d"),
        Line("(hosts.allow / hosts.deny)", 10, 400, "#374151"),
    ])
    c.connector(280, 215, 380, 215, "mgmt", label="ssh -> bastion01")
    c.connector(600, 215, 700, 215, "mgmt", label="ProxyJump -> web01")
    c.connector(810, 270, 240, 340, "warn", label="direct connect, bypassing bastion01 (negative test)")
    c.node_box(60, 340, 240, 90, "warn", [
        Line("Negative Test", 11.5, 700, "#7f1d1d"),
        Line("ProxyJump removed, direct", 10.5, 400, "#7f1d1d"),
        Line("connect to web01 → refused/timeout", 10, 400, "#7f1d1d"),
    ])
    c.node_box(380, 340, 540, 110, "neutral", [
        Line("Inventory-Drift Check", 12.5, 700, "#111827"),
        Line("inventory.txt: web01, web02", 10.5, 400, "#374151"),
        Line("OK: web01 reachable", 10.5, 700, "#14532d"),
        Line("DRIFT: web02 in inventory but unreachable", 10.5, 700, "#7c2d12"),
    ])
    c.legend(60, 610, [("mgmt", "Mediated access path"), ("alt", "Restricted destination"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-01-bastion-mediated-access-topology.svg")


def ch02():
    c = Canvas(960, 620,
        title="Chapter 2 Hands-On Lab: Confined Service Account, systemd Timer, LVM Extend, and Scoped sudo",
        subtitle="labsvc runs a heartbeat timer under a scoped identity; only the labops group may restart it",
        svg_title="Chapter 2 lab flow: a confined service account, a systemd timer, LVM growth, and a scoped sudo rule on one Linux VM",
        svg_desc="A system account labsvc owns /var/lib/labsvc/data (mode 750) and runs labsvc-heartbeat.timer, "
                  "which writes a timestamp every minute via a oneshot service. The volume group backing / is "
                  "extended with the attached /dev/sdb disk (pvcreate, vgextend, lvextend +2G, then a filesystem "
                  "grow), increasing available space. A sudoers rule scopes the labops group to only restart or "
                  "check the status of labsvc-heartbeat.timer. As a negative test, a user outside labops is refused "
                  "when attempting sudo systemctl restart on the timer; after being added to labops, the same "
                  "command succeeds.")
    c.node_box(60, 130, 260, 110, "mgmt", [
        Line("labsvc (system account)", 12.5, 700, "#111827"),
        Line("/var/lib/labsvc/data (750)", 10.5, 400, "#374151"),
        Line("labsvc-heartbeat.timer (1 min)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 130, 240, 110, "alt", [
        Line("LVM extend", 12.5, 700, "#111827"),
        Line("pvcreate /dev/sdb", 10.5, 400, "#374151"),
        Line("vgextend + lvextend +2G", 10.5, 400, "#374151"),
        Line("df -hT / shows growth", 10, 400, "#14532d"),
    ])
    c.node_box(660, 130, 260, 130, "neutral", [
        Line("Scoped sudo rule", 12.5, 700, "#111827"),
        Line("%labops ALL=(root) NOPASSWD:", 10, 400, "#374151"),
        Line("systemctl restart/status", 10, 400, "#374151"),
        Line("labsvc-heartbeat.timer only", 10, 400, "#374151"),
    ])
    c.connector(320, 185, 380, 185, "mgmt")
    c.connector(620, 185, 660, 185, "mgmt")
    c.node_box(60, 400, 360, 130, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("non-labops user: sudo systemctl restart", 10.5, 400, "#7f1d1d"),
        Line("labsvc-heartbeat.timer → refused", 10.5, 400, "#7f1d1d"),
        Line("user added to labops → same command", 10.5, 400, "#7f1d1d"),
        Line("now succeeds", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(790, 260, 240, 400, "warn")
    c.legend(60, 570, [("mgmt", "Service identity / timer"), ("alt", "Storage operation"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-02-confined-service-account-flow.svg")


def ch03():
    c = Canvas(960, 620,
        title="Chapter 3 Hands-On Lab: Remote Windows Server Role Install and WinRM Hardening",
        subtitle="PowerShell Remoting installs a role, schedules a task, then Basic authentication is disabled and tested",
        svg_title="Chapter 3 lab topology: PowerShell Remoting used end to end to provision and harden a Windows Server target",
        svg_desc="An administrator workstation running PowerShell 7.4+ uses WinRM to reach winsrv-lab: Test-WSMan "
                  "confirms connectivity, Install-WindowsFeature adds the File Server role, and Invoke-Command "
                  "creates an SMB share and registers a scheduled task that writes a heartbeat file every minute. "
                  "The WinRM listener is then hardened by disabling Basic authentication and unencrypted traffic. "
                  "As a negative test, an explicit Basic-authentication connection attempt from the workstation is "
                  "rejected after the hardening step, while a subsequent Kerberos/Negotiate attempt with valid "
                  "credentials succeeds.")
    c.node_box(60, 170, 260, 130, "mgmt", [
        Line("Administrator Workstation", 12.5, 700, "#111827"),
        Line("PowerShell 7.4+", 10.5, 400, "#374151"),
        Line("Test-WSMan / Invoke-Command", 10.5, 400, "#374151"),
    ])
    c.node_box(420, 150, 260, 170, "alt", [
        Line("winsrv-lab", 14, 700, "#111827"),
        Line("FS-FileServer role + LabShare", 10.5, 400, "#374151"),
        Line("LabHeartbeat scheduled task", 10.5, 400, "#374151"),
        Line("WinRM: Basic auth disabled", 10.5, 700, "#14532d"),
        Line("AllowUnencrypted: false", 10, 400, "#374151"),
    ])
    c.connector(320, 235, 420, 235, "mgmt", label="WinRM (Kerberos/Negotiate)")
    c.node_box(60, 400, 780, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Invoke-Command -Authentication Basic against winsrv-lab, after Basic auth was disabled", 11, 400, "#7f1d1d"),
        Line("connection rejected — hardening control confirmed enforced", 11, 400, "#7f1d1d"),
        Line("subsequent attempt with default Kerberos/Negotiate + valid credential succeeds", 11, 400, "#14532d"),
    ])
    c.connector(550, 320, 450, 400, "warn")
    c.legend(60, 570, [("mgmt", "Kerberos/Negotiate (allowed)"), ("alt", "WinRM target state"), ("warn", "Basic auth (denied)")])
    c.save(f"{OUT}/chapter-03-winrm-remoting-hardening-topology.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: Active Directory Domain Join, Group-Restricted Login, and GPO Application",
        subtitle="A Linux host joins example.com via realmd/sssd; a GPO applies to a Windows Server in the same OU",
        svg_title="Chapter 4 lab topology: a Linux host and a Windows Server both governed by the same Active Directory domain",
        svg_desc="A Linux VM discovers and joins the example.com Active Directory domain using realmd/sssd/adcli "
                  "with the svc-joiner account, then restricts interactive login to the linux-admins@example.com "
                  "group. jdoe@example.com, a group member, resolves identity and obtains a Kerberos ticket "
                  "successfully. Separately, a GPO named 'Lab Baseline' is created and linked to "
                  "OU=Windows,OU=Servers,DC=example,DC=com, setting a screen-lock inactivity timeout; a Windows "
                  "Server VM in that OU applies the policy after gpupdate /force. As a negative test, an AD user "
                  "who is not a member of linux-admins is refused interactive login to the Linux host, while "
                  "jdoe@example.com logs in successfully.")
    c.node_box(370, 110, 220, 90, "neutral", [
        Line("example.com", 14, 700, "#111827"),
        Line("Active Directory domain", 10.5, 400, "#374151"),
        Line("domain controller", 10.5, 400, "#374151"),
    ])
    c.node_box(90, 260, 260, 130, "mgmt", [
        Line("Linux VM", 13.5, 700, "#111827"),
        Line("realm join --user=svc-joiner", 10.5, 400, "#374151"),
        Line("realm permit -g linux-admins", 10.5, 700, "#1d4ed8"),
        Line("jdoe@example.com → valid TGT", 10, 400, "#374151"),
    ])
    c.node_box(610, 260, 260, 130, "alt", [
        Line("Windows Server VM", 13.5, 700, "#111827"),
        Line("OU=Windows,OU=Servers", 10.5, 400, "#374151"),
        Line("GPO 'Lab Baseline' applied", 10.5, 700, "#14532d"),
        Line("gpupdate /force → gpresult /r", 10, 400, "#374151"),
    ])
    c.connector(430, 200, 250, 260, "neutral", label="realm join / Kerberos")
    c.connector(530, 200, 710, 260, "neutral", label="GPO link (OU=Windows,OU=Servers)")
    c.node_box(90, 440, 780, 120, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("AD user NOT in linux-admins attempts interactive login to the Linux VM → refused", 11, 400, "#7f1d1d"),
        Line("jdoe@example.com (linux-admins member) attempts the same login → succeeds", 11, 400, "#14532d"),
    ])
    c.connector(220, 390, 220, 440, "warn")
    c.legend(90, 610, [("mgmt", "Linux domain integration"), ("alt", "Windows GPO application")])
    c.save(f"{OUT}/chapter-04-ad-domain-join-gpo-topology.svg")


def ch05():
    c = Canvas(960, 640,
        title="Chapter 5 Hands-On Lab: systemd CPU Quota Enforcement and flock Overlap Prevention",
        subtitle="cpu-burn.service is capped at 50% of one core by CPUQuota; flock refuses a second overlapping job run",
        svg_title="Chapter 5 lab flow: CPU resource control with systemd CPUQuota, and job-overlap prevention with flock",
        svg_desc="cpu-burn.service runs a tight CPU-burning loop under systemd with CPUQuota=50%; systemd-cgtop "
                  "confirms usage stabilizes near 50% of one core. As a negative test, removing CPUQuota= entirely "
                  "and re-running the same service shows usage rise to approximately 100%, proving the earlier 50% "
                  "figure came from the configured limit rather than an unrelated ceiling. Separately, slow-job.sh "
                  "is launched twice back to back, each invocation guarded by flock on the same lock file; the "
                  "second invocation is correctly refused while the first is still running, and the log shows only "
                  "one start/finish pair.")
    c.node_box(60, 130, 260, 130, "mgmt", [
        Line("cpu-burn.service", 12.5, 700, "#111827"),
        Line("CPUQuota=50%", 11, 700, "#1d4ed8"),
        Line("systemd-cgtop: ~50% of 1 core", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 130, 260, 130, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("CPUQuota= removed, re-run", 10.5, 400, "#7f1d1d"),
        Line("systemd-cgtop: ~100% of 1 core", 10.5, 700, "#7f1d1d"),
        Line("confirms the 50% cap was real", 10, 400, "#7f1d1d"),
    ])
    c.connector(320, 195, 370, 195, "warn")
    c.node_box(680, 130, 240, 130, "alt", [
        Line("slow-job.sh (20s runtime)", 12, 700, "#111827"),
        Line("flock /var/lock/slow-job.lock", 10.5, 400, "#374151"),
        Line("run #1: acquires lock, executes", 10, 400, "#374151"),
        Line("run #2: \"lock held\", refused", 10, 700, "#14532d"),
    ])
    c.node_box(60, 340, 860, 90, "neutral", [
        Line("/var/log/slow-job.log shows only one started/finished pair for the overlapping window", 11.5, 400, "#374151"),
        Line("confirming flock prevented the second invocation from ever running concurrently", 11, 400, "#374151"),
    ])
    c.legend(60, 570, [("mgmt", "CPU-bounded (enforced)"), ("warn", "Unbounded (negative test)"), ("alt", "Overlap-safe job")])
    c.save(f"{OUT}/chapter-05-cpu-quota-flock-flow.svg")


def ch06():
    c = Canvas(960, 640,
        title="Chapter 6 Hands-On Lab: Idempotent Ansible Baseline, Drift Correction, and a Non-Idempotent Anti-Pattern",
        subtitle="baseline.yml converges /etc/lab-baseline.conf and self-heals drift; a shell-append task never converges",
        svg_title="Chapter 6 lab flow: an idempotent Ansible playbook enforcing and reconciling a configuration baseline",
        svg_desc="baseline.yml, run against localhost, uses the copy module to enforce /etc/lab-baseline.conf's "
                  "content. Check mode shows the planned change without applying it; the first real run reports "
                  "changed=1 and the second reports changed=0, proving idempotency. Out-of-band drift (sed-tampering "
                  "the file) is corrected automatically by re-running the same playbook. As a negative test, a "
                  "copy of the playbook with an added ansible.builtin.shell append task reports changed=1 on every "
                  "run and grows the file with a new timestamped line each time, demonstrating the anti-pattern "
                  "the chapter's Design Considerations section warns against.")
    c.node_box(60, 150, 280, 150, "mgmt", [
        Line("baseline.yml (localhost)", 12.5, 700, "#111827"),
        Line("copy: /etc/lab-baseline.conf", 10.5, 400, "#374151"),
        Line("run 1: changed=1", 10.5, 400, "#374151"),
        Line("run 2: changed=0 (idempotent)", 10.5, 700, "#14532d"),
    ])
    c.node_box(400, 150, 260, 150, "alt", [
        Line("Drift + Reconciliation", 12.5, 700, "#111827"),
        Line("sed tampers baseline_version", 10.5, 400, "#374151"),
        Line("re-run baseline.yml", 10.5, 400, "#374151"),
        Line("file restored to baseline", 10.5, 700, "#14532d"),
    ])
    c.connector(340, 225, 400, 225, "mgmt")
    c.node_box(700, 150, 220, 150, "warn", [
        Line("bad-baseline.yml", 12, 700, "#111827"),
        Line("shell: echo >> ... (anti-pattern)", 10, 400, "#7f1d1d"),
        Line("run 1: changed=1", 10, 400, "#7f1d1d"),
        Line("run 2: changed=1 (again!)", 10, 700, "#7f1d1d"),
    ])
    c.connector(660, 225, 700, 225, "warn")
    c.node_box(60, 380, 860, 90, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("/etc/lab-baseline.conf grows a new timestamped line on every run — never converges, unlike baseline.yml", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 570, [("mgmt", "Idempotent module"), ("alt", "Drift self-healing"), ("warn", "Non-idempotent shell task")])
    c.save(f"{OUT}/chapter-06-ansible-idempotent-baseline-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: NFSv4 Export Restricted by Subnet, with an XFS Project Quota",
        subtitle="nfsclient01 mounts nfs01's export within the permitted subnet; a third host outside it is refused",
        svg_title="Chapter 7 lab topology: an NFSv4 export restricted to one subnet, enforcing an XFS project quota",
        svg_desc="nfs01 exports /data/labexport read-write to the 10.20.30.0/24 subnet only. nfsclient01, inside "
                  "that subnet, mounts the export over NFSv4 and reads the seeded file successfully. nfs01 applies "
                  "an XFS project quota (10 MiB hard limit) to the exported directory; writing 15 MiB from "
                  "nfsclient01 fails partway with 'Disk quota exceeded' once the limit is reached. As a negative "
                  "test, a third host outside 10.20.30.0/24 attempting the same mount is refused — permission "
                  "denied or no route — confirming the subnet restriction is enforced by the NFS server itself.")
    c.node_box(370, 130, 220, 130, "mgmt", [
        Line("nfs01", 14, 700, "#111827"),
        Line("/data/labexport (XFS, pquota)", 10.5, 400, "#374151"),
        Line("export: 10.20.30.0/24 only", 10.5, 700, "#1d4ed8"),
        Line("project quota: bhard=10m", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(80, 300, 240, 110, "alt", [
        Line("nfsclient01", 13.5, 700, "#111827"),
        Line("inside 10.20.30.0/24", 11, 700, "#14532d"),
        Line("mount -t nfs4 nfs01:/data/labexport", 10, 400, "#374151"),
        Line("dd 15M → \"Disk quota exceeded\"", 10, 400, "#374151"),
    ])
    c.node_box(660, 300, 240, 110, "warn", [
        Line("Third host", 13.5, 700, "#111827"),
        Line("outside 10.20.30.0/24", 11, 700, "#7f1d1d"),
        Line("showmount -e / mount attempt", 10, 400, "#7f1d1d"),
        Line("→ refused (denied / no route)", 10, 400, "#7f1d1d"),
    ])
    c.connector(370, 230, 250, 300, "alt", label="NFSv4 (permitted)")
    c.connector(590, 230, 720, 300, "warn", label="NFSv4 (negative test)")
    c.node_box(80, 460, 820, 90, "neutral", [
        Line("Quota enforcement confirmed on nfs01: sudo xfs_quota -x -c 'report -p' /data shows usage at the hard limit", 11.5, 400, "#374151"),
    ])
    c.legend(80, 610, [("mgmt", "Server-side policy"), ("alt", "Permitted client"), ("warn", "Denied client (negative test)")])
    c.save(f"{OUT}/chapter-07-nfsv4-export-quota-topology.svg")


def ch08():
    c = Canvas(960, 620,
        title="Chapter 8 Hands-On Lab: OpenSCAP Baseline Scan, Ansible Remediation, and Regression Re-Scan",
        subtitle="A CIS baseline scan drives a targeted fix; reintroducing the finding is caught by a re-scan",
        svg_title="Chapter 8 lab flow: OpenSCAP baseline scanning paired with idempotent Ansible remediation and a regression re-scan",
        svg_desc="A baseline oscap xccdf eval against the CIS profile records a nonzero fail count on a fresh VM. "
                  "harden-ssh.yml sets PermitRootLogin no via lineinfile and reloads sshd; a re-scan shows the "
                  "root-login rule now passing where it previously failed. As a negative test, PermitRootLogin is "
                  "manually reverted to yes and sshd reloaded; a targeted re-scan catches the regression, showing "
                  "the same rule failing again, demonstrating why the automation feedback loop must include "
                  "re-scanning rather than trusting a one-time remediation. Re-running harden-ssh.yml restores the "
                  "hardened state.")
    c.node_box(60, 140, 240, 110, "neutral", [
        Line("Baseline Scan", 12.5, 700, "#111827"),
        Line("oscap xccdf eval (CIS profile)", 10.5, 400, "#374151"),
        Line("nonzero fail count recorded", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 140, 240, 110, "mgmt", [
        Line("harden-ssh.yml", 12.5, 700, "#111827"),
        Line("PermitRootLogin no", 11, 700, "#1d4ed8"),
        Line("(lineinfile + reload sshd)", 10.5, 400, "#374151"),
    ])
    c.node_box(680, 140, 220, 110, "alt", [
        Line("Re-Scan", 12.5, 700, "#111827"),
        Line("permit_root_login rule:", 10.5, 400, "#374151"),
        Line("fail → pass", 11, 700, "#14532d"),
    ])
    c.connector(300, 195, 370, 195, "mgmt")
    c.connector(610, 195, 680, 195, "mgmt")
    c.node_box(60, 380, 840, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("PermitRootLogin manually reverted to yes, sshd reloaded", 11, 400, "#7f1d1d"),
        Line("targeted re-scan: permit_root_login rule shows fail again — regression caught", 11, 400, "#7f1d1d"),
        Line("re-running harden-ssh.yml restores PermitRootLogin no", 11, 400, "#14532d"),
    ])
    c.connector(790, 250, 480, 380, "warn")
    c.legend(60, 550, [("mgmt", "Remediation step"), ("alt", "Confirmed pass"), ("warn", "Regression / negative-test path")])
    c.save(f"{OUT}/chapter-08-openscap-ansible-remediation-flow.svg")


def ch09():
    c = Canvas(960, 640,
        title="Chapter 9 Hands-On Lab: Severity-Filtered Log Forwarding to a Mock Collector",
        subtitle="rsyslog forwards only local0.crit to a UDP listener; local0.info stays local, proving severity-based filtering",
        svg_title="Chapter 9 lab flow: a disk health-check script whose critical alerts are forwarded by rsyslog while informational logs are not",
        svg_desc="A mock collector (nc -ul 2514) listens on UDP 2514. rsyslog is configured to forward only "
                  "local0.crit messages to 127.0.0.1:2514. disk-healthcheck.sh, run with an intentionally low "
                  "threshold (1%), logs at local0.crit and the message is received by the mock collector within "
                  "seconds. As a negative test, the threshold is raised to 99% (unreachable by real usage); the "
                  "script now logs at local0.info instead, and the mock collector receives nothing, while the "
                  "local system log still records the informational entry — confirming the forwarding rule matches "
                  "on severity specifically, not on every script invocation.")
    c.node_box(60, 160, 260, 130, "mgmt", [
        Line("disk-healthcheck.sh", 12.5, 700, "#111827"),
        Line("threshold=1 → local0.crit", 10.5, 700, "#1d4ed8"),
        Line("threshold=99 → local0.info", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(380, 160, 260, 130, "alt", [
        Line("rsyslog", 13.5, 700, "#111827"),
        Line("60-forward-critical.conf", 10.5, 400, "#374151"),
        Line("local0.crit → omfwd UDP 2514", 10.5, 700, "#14532d"),
        Line("local0.info → local only", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 160, 220, 130, "neutral", [
        Line("Mock Collector", 12.5, 700, "#111827"),
        Line("nc -ul 2514", 10.5, 400, "#374151"),
        Line("receives crit only", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 225, 380, 225, "mgmt", label="logger -p local0.crit/.info")
    c.connector(640, 225, 700, 225, "alt", label="UDP 2514 (crit only)")
    c.node_box(60, 400, 860, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("threshold=99 → script logs at local0.info instead of local0.crit", 11, 400, "#7f1d1d"),
        Line("mock collector receives nothing; local journal/syslog still shows the \"(OK)\" entry", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 570, [("mgmt", "Health-check output"), ("alt", "Severity-filtered forwarding"), ("neutral", "Remote collector")])
    c.save(f"{OUT}/chapter-09-rsyslog-severity-forwarding-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
