import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-14-red-hat-enterprise-linux-10"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Hands-On Lab: Cockpit Access Depends on Socket Activation, Not the Firewall Rule Alone",
        subtitle="Opening port 9090 is not enough by itself — stopping cockpit.socket makes the console unreachable even with the port still open",
        svg_title="Chapter 1 lab flow: local repository configuration and Cockpit access, proven to depend on socket activation rather than the firewall rule alone",
        svg_desc="Local repositories point at the mounted RHEL 10 ISO's BaseOS and AppStream content sets; dnf "
                  "repolist confirms both resolve with a nonzero package count. Cockpit and cockpit-storaged "
                  "install from those repos, cockpit.socket is enabled, and the firewall opens the cockpit "
                  "service; a browser reaches the Overview page at port 9090 showing hostname, uptime, and "
                  "resource graphs. As a negative test, cockpit.socket is stopped while the firewall rule stays "
                  "in place; a curl request to the same port now fails to connect, confirming that socket "
                  "activation — not just the open firewall port — is what actually provides access.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Local ISO repositories", 12.5, 700, "#111827"),
        Line("BaseOS + AppStream", 10.5, 400, "#374151"),
        Line("dnf repolist: nonzero packages", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("cockpit.socket + firewall", 12.5, 700, "#111827"),
        Line("both enabled → :9090 reachable", 10.5, 700, "#14532d"),
        Line("Overview page loads in browser", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("cockpit.socket stopped", 10.5, 700, "#7f1d1d"),
        Line("firewall port still open", 10.5, 400, "#7f1d1d"),
        Line("curl :9090 → connection failed", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the firewall rule alone never provided the service — socket activation is the actual control that", 11.5, 400, "#374151"),
        Line("makes Cockpit reachable, and stopping it removes access even with the port still open.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Repository source"), ("alt", "Working access path"), ("warn", "Socket stopped (negative test)")])
    c.save(f"{OUT}/chapter-01-cockpit-socket-activation-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A Quoting Bug Demonstrated Live, Then a Clean dnf history Rollback",
        subtitle="An unquoted variable word-splits into two arguments; dnf history undo cleanly reverses a real package installation",
        svg_title="Chapter 2 lab flow: an administrative audit script exercised against a real package transaction, then deliberately broken to demonstrate a quoting bug",
        svg_desc="disk-and-pkg-report.sh prints disk usage, recent dnf transactions, and largest /var directories "
                  "cleanly. Installing the tree package creates a new transaction that the script's next run "
                  "picks up automatically. As a negative test, a copy of the script replaces a quoted path with an "
                  "unquoted multi-word variable ($TESTDIR instead of \"$TESTDIR\"); running it word-splits the "
                  "value into two separate arguments, and du reports it cannot access a directory literally named "
                  "audit in the current working directory — exactly the class of bug quoting prevents. Separately, "
                  "dnf history undo last cleanly reverses the tree installation, confirmed by rpm -q reporting the "
                  "package no longer installed.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("disk-and-pkg-report.sh", 12.5, 700, "#111827"),
        Line("dnf install tree → new transaction", 10.5, 400, "#374151"),
        Line("re-run picks up the transaction", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("dnf history undo last", 12.5, 700, "#111827"),
        Line("tree cleanly reverted", 10.5, 700, "#14532d"),
        Line("rpm -q tree: not installed", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("$TESTDIR left unquoted", 10.5, 700, "#7f1d1d"),
        Line("word-splits into 2 arguments", 10.5, 700, "#7f1d1d"),
        Line("du: cannot access \"audit\"", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("\"$TESTDIR\" (quoted) would have passed one argument, /var/log audit, to du intact — the unquoted", 11.5, 400, "#374151"),
        Line("version demonstrates exactly why shell quoting around multi-word variables matters.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Audit script + real transaction"), ("alt", "Clean rollback"), ("warn", "Quoting bug (negative test)")])
    c.save(f"{OUT}/chapter-02-dnf-audit-quoting-rollback-flow.svg")


def ch03():
    c = Canvas(960, 560,
        title="Chapter 3 Hands-On Lab: A Missing-Binary systemd Failure Surfaced Distinctly From an App Crash",
        subtitle="heartbeat.timer runs cleanly every minute; a unit pointed at a nonexistent script fails with a distinct 203/EXEC status",
        svg_title="Chapter 3 lab flow: a custom systemd service and timer observed through the journal, contrasted with a unit whose ExecStart path does not exist",
        svg_desc="heartbeat.timer fires heartbeat.service every minute; after waiting past the first interval, "
                  "the journal shows at least one heartbeat line and systemctl status reports the oneshot unit as "
                  "inactive (dead) with exit code 0 between runs. As a negative test, broken-demo.service points "
                  "ExecStart at a script that does not exist; starting it reports failed with a status such as "
                  "203/EXEC, and the journal shows systemd could not execute the configured path at all — a "
                  "distinct failure signature from an application starting and then crashing on its own.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("heartbeat.timer", 12.5, 700, "#111827"),
        Line("fires heartbeat.service every 1min", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("journalctl -u heartbeat.service", 12, 700, "#111827"),
        Line("heartbeat lines present", 10.5, 700, "#14532d"),
        Line("status: inactive (dead), exit 0", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("broken-demo.service", 10.5, 700, "#7f1d1d"),
        Line("ExecStart → nonexistent script", 10.5, 700, "#7f1d1d"),
        Line("status: failed (203/EXEC)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("203/EXEC means systemd could not even execute the configured binary — a distinct signature from an", 11.5, 400, "#374151"),
        Line("application that started and then crashed, and one worth recognizing immediately in the journal.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Working timer + service"), ("alt", "Verified via journal"), ("warn", "Missing-binary failure")])
    c.save(f"{OUT}/chapter-03-systemd-timer-missing-binary-flow.svg")


def ch04():
    c = Canvas(960, 620,
        title="Chapter 4 Hands-On Lab: Scoped Sudo, Restricted SSH, and a Verified Account Lockout",
        subtitle="operator1 authenticates by key with a two-command sudo grant; repeated bad passwords actually trip faillock",
        svg_title="Chapter 4 lab topology: a scoped operator account with delegated sudo and source-restricted SSH, tested against a brute-force lockout",
        svg_desc="operator1, a member of the webteam group, authenticates via SSH key with no password prompt, "
                  "and sudo -l confirms exactly two permitted systemctl commands, not full root. A static IP on a "
                  "second interface has SSH restricted by a firewalld rich rule to the 192.0.2.0/24 client subnet, "
                  "with the plain ssh service removed from that zone's service list. As a negative test, five "
                  "repeated wrong-password login attempts are sent against operator1; faillock records the "
                  "failures and, once the configured threshold is exceeded, temporarily locks the account. "
                  "Resetting the lockout with faillock --reset restores normal access.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("operator1 (webteam group)", 12.5, 700, "#111827"),
        Line("SSH key auth, no password prompt", 10.5, 400, "#374151"),
        Line("sudo -l: 2 commands only", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("firewalld rich rule", 12.5, 700, "#111827"),
        Line("SSH scoped to 192.0.2.0/24", 10.5, 700, "#14532d"),
        Line("plain ssh service removed", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("5x wrong password attempts", 10.5, 700, "#7f1d1d"),
        Line("faillock: account locked", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("faillock --user operator1 shows recorded failures and the temporary lock; --reset restores normal", 11.5, 400, "#374151"),
        Line("access — confirming the lockout policy is enforced by faillock, not merely documented.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Scoped identity"), ("alt", "Network-restricted access"), ("warn", "Verified lockout")])
    c.save(f"{OUT}/chapter-04-scoped-sudo-ssh-lockout-topology.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: An LVM-Backed NFS Export Whose Client Restriction Is Actually Enforced",
        subtitle="The volume grows live from 4G to 6G with no unmount, and narrowing the export to a different subnet refuses the same client's mount",
        svg_title="Chapter 5 lab topology: an LVM-backed XFS filesystem exported over NFS, extended live and tested against a client-restriction negative test",
        svg_desc="/dev/sdb becomes vg_lab/lv_share, formatted XFS and mounted at /srv/nfs/lab-share; "
                  "lvextend plus xfs_growfs takes it from 4G to approximately 6G with no unmount required. A swap "
                  "logical volume joins the same volume group. The filesystem exports to 10.10.10.0/24 over NFS, "
                  "and a client on that subnet mounts it and writes a test file successfully. As a negative test, "
                  "the export is narrowed to a different subnet (192.0.2.0/24) that the same client is not on; "
                  "re-mounting from that client now fails with a permission or access error, confirming the "
                  "export's client restriction is enforced by the NFS server, not merely documented in "
                  "/etc/exports.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("vg_lab/lv_share (XFS)", 12.5, 700, "#111827"),
        Line("4G → live-extended to 6G", 10.5, 700, "#1d4ed8"),
        Line("+ lv_swap in same VG", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("NFS export: 10.10.10.0/24", 12, 700, "#111827"),
        Line("client on that subnet mounts", 10.5, 700, "#14532d"),
        Line("writes test.txt successfully", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("export narrowed to 192.0.2.0/24", 10.5, 700, "#7f1d1d"),
        Line("same client's mount refused", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the mount attempt fails with a permission/access error — confirming the exported subnet restriction", 11.5, 400, "#374151"),
        Line("is enforced by nfs-server itself, not merely a line in a configuration file.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "LVM growth"), ("alt", "Permitted NFS client"), ("warn", "Denied NFS client")])
    c.save(f"{OUT}/chapter-05-lvm-nfs-export-restriction-topology.svg")


def ch06():
    c = Canvas(960, 660,
        title="Chapter 6 Hands-On Lab: An SELinux Denial Fixed Persistently, and LUKS Data Confirmed Unrecoverable Without the Key",
        subtitle="httpd is blocked until the content type is relabeled; the raw LUKS backing file yields no plaintext once the mapping is closed",
        svg_title="Chapter 6 lab flow: a relocated web content directory triggering and then resolving an SELinux denial, plus a LUKS volume tested for plaintext leakage",
        svg_desc="Serving content from /data/web fails, because the directory does not carry the "
                  "httpd_sys_content_t context; ausearch and sealert confirm httpd_t was denied access to the "
                  "mislabeled path. semanage fcontext plus restorecon apply the correct persistent label, and the "
                  "same curl request now succeeds. An ACL separately grants one non-owner user write access "
                  "without touching the SELinux policy. A LUKS-encrypted loopback volume mounts and accepts a "
                  "written file normally. As a negative test, the volume is unmounted and the LUKS mapping closed; "
                  "searching the raw backing file for the plaintext string finds nothing, confirming the data is "
                  "not recoverable from the backing file without the LUKS key.")
    c.node_box(60, 130, 240, 110, "warn", [
        Line("/data/web (wrong context)", 12, 700, "#111827"),
        Line("httpd request fails / 403", 10.5, 700, "#7f1d1d"),
        Line("AVC denial in audit log", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(380, 130, 240, 110, "alt", [
        Line("semanage + restorecon", 12.5, 700, "#111827"),
        Line("httpd_sys_content_t applied", 10.5, 700, "#14532d"),
        Line("curl now succeeds", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 380, 185, "warn")
    c.node_box(700, 130, 220, 110, "mgmt", [
        Line("ACL grant", 12.5, 700, "#111827"),
        Line("contentwriter: rwx via ACL", 10.5, 400, "#374151"),
        Line("independent of SELinux policy", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 320, 400, 130, "mgmt", [
        Line("LUKS volume (loopback)", 12.5, 700, "#111827"),
        Line("cryptsetup luksFormat/luksOpen", 10.5, 400, "#374151"),
        Line("mounted, file written normally", 10.5, 400, "#374151"),
    ])
    c.node_box(500, 320, 400, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("unmounted, luksClose'd", 10.5, 700, "#7f1d1d"),
        Line("strings on raw backing file:", 10.5, 400, "#7f1d1d"),
        Line("plaintext not found (as expected)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(460, 385, 500, 385, "warn")
    c.legend(60, 500, [("warn", "Denial / negative test"), ("alt", "Fixed context"), ("mgmt", "Independent grant / volume")])
    c.save(f"{OUT}/chapter-06-selinux-acl-luks-flow.svg")


def ch07():
    c = Canvas(960, 600,
        title="Chapter 7 Hands-On Lab: A Scoped Database Grant Confirmed to Not Reach the System Database",
        subtitle="labuser sees its own database over a validated DNS/TLS/web stack, but is correctly denied access to MariaDB's mysql schema",
        svg_title="Chapter 7 lab topology: a caching DNS resolver, TLS web virtual host, and scoped MariaDB user, tested against an out-of-scope database access attempt",
        svg_desc="chronyd reports Leap status Normal; a local BIND caching resolver forwards to public resolvers "
                  "and dig returns a real answer. A self-signed TLS virtual host serves lab content over HTTPS. "
                  "MariaDB's labuser, granted all privileges only on labdb, can see and use that one database. As "
                  "a negative test, labuser attempts USE mysql; SHOW TABLES against the system database; MariaDB "
                  "returns an access-denied error, confirming the grant is properly scoped to labdb alone and "
                  "does not implicitly extend to server-wide system tables.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("chronyd + BIND resolver", 12, 700, "#111827"),
        Line("Leap status: Normal", 10.5, 400, "#374151"),
        Line("dig @127.0.0.1: real answer", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Apache TLS vhost", 12.5, 700, "#111827"),
        Line("self-signed cert, :443", 10.5, 400, "#374151"),
        Line("curl -k returns lab vhost", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "mgmt", [
        Line("MariaDB: labuser → labdb", 12, 700, "#111827"),
        Line("SHOW DATABASES: labdb visible", 10.5, 400, "#374151"),
    ])
    c.connector(620, 195, 700, 195, "alt")
    c.node_box(60, 320, 860, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("labuser: USE mysql; SHOW TABLES → access denied", 11, 400, "#7f1d1d"),
        Line("the GRANT ALL on labdb.* does not extend to the mysql system schema — the scope holds exactly as defined", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 460, [("mgmt", "Core service"), ("alt", "TLS-verified access"), ("warn", "Correctly denied scope")])
    c.save(f"{OUT}/chapter-07-dns-tls-mariadb-scope-topology.svg")


def ch08():
    c = Canvas(960, 640,
        title="Chapter 8 Hands-On Lab: A Rootless Quadlet Pod Rebuilt Entirely From Its Own Exported YAML",
        subtitle="The sidecar reaches the app over the shared pod network; rootless Podman still cannot bind port 80 without extra configuration",
        svg_title="Chapter 8 lab flow: a custom container image run rootless as a Quadlet service, grouped into a pod, and recreated from exported Kubernetes YAML",
        svg_desc="A custom UBI-based image runs as a rootless, Quadlet-managed systemd --user service publishing "
                  "port 8091; curl confirms the service responds. A two-container pod (app plus sidecar) shares "
                  "one network namespace, and the sidecar reaches the app over localhost. podman generate kube "
                  "exports the pod as Kubernetes-compatible YAML; the pod is removed entirely and podman play kube "
                  "recreates both containers running again purely from that file. As a negative test, running the "
                  "same image rootless with -p 80:80 fails with a permission error binding the privileged port — "
                  "the documented, deliberate limitation of rootless Podman without additional configuration.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Quadlet: lab-app.container", 12.5, 700, "#111827"),
        Line("rootless, systemd --user", 10.5, 400, "#374151"),
        Line("curl :8091 → responds", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 130, 240, 110, "alt", [
        Line("lab-pod (app + sidecar)", 12.5, 700, "#111827"),
        Line("shared network namespace", 10.5, 400, "#374151"),
        Line("sidecar curls app via localhost", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 185, 380, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("generate kube → play kube", 12, 700, "#111827"),
        Line("pod removed, then rebuilt", 10.5, 700, "#14532d"),
        Line("entirely from exported YAML", 10.5, 400, "#374151"),
    ])
    c.connector(620, 185, 700, 185, "alt")
    c.node_box(60, 330, 860, 100, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("rootless podman run -p 80:80 → permission error binding the privileged port", 11, 400, "#7f1d1d"),
        Line("the documented, deliberate limitation of running without host root, not a misconfiguration", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 470, [("mgmt", "Rootless service"), ("alt", "Pod / kube portability")])
    c.save(f"{OUT}/chapter-08-podman-quadlet-kube-flow.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: The RHCSA Capstone — One Ansible Run Verified Independently Across Every Domain",
        subtitle="An idempotent playbook builds identity, storage, SELinux, firewall, and a timer at once; reverting SELinux by hand breaks it and the playbook heals it again",
        svg_title="Chapter 9 lab flow: an integrated Ansible capstone build across identity, storage, SELinux, firewall, and scheduled work, tested against a manual SELinux regression",
        svg_desc="capstone.yml builds a scoped service account, an LVM-backed XFS filesystem, an SELinux file "
                  "context, an httpd virtual host, an open firewall port, and a nightly timer in one run; a "
                  "second run reports changed=0 for every task except the always-changed restorecon command. "
                  "Independent verification checks every domain directly — id, lsblk, SELinux context, firewall "
                  "list, service status, and timer schedule — exactly as an RHCSA practical would require. As a "
                  "negative test, the SELinux context is manually removed and reset to var_t; the web service now "
                  "fails at the SELinux layer with a corresponding AVC denial in the audit log, and re-running the "
                  "playbook restores the correct context and working service — demonstrating both MAC enforcement "
                  "and idempotent remediation in the same exercise.")
    c.node_box(60, 130, 260, 120, "mgmt", [
        Line("capstone.yml (one run)", 12.5, 700, "#111827"),
        Line("identity, LVM/XFS, SELinux,", 10.5, 400, "#374151"),
        Line("firewall, httpd, nightly timer", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 130, 240, 120, "alt", [
        Line("Independent verification", 12.5, 700, "#111827"),
        Line("id, lsblk, ls -Z, firewall-cmd,", 10.5, 400, "#374151"),
        Line("systemctl, list-timers — all pass", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 190, 400, 190, "mgmt")
    c.node_box(700, 130, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("SELinux context reverted", 10.5, 700, "#7f1d1d"),
        Line("by hand (chcon var_t)", 10.5, 700, "#7f1d1d"),
        Line("httpd fails, AVC denial logged", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 190, 700, 190, "warn")
    c.node_box(60, 340, 860, 110, "alt", [
        Line("Idempotent Remediation", 12.5, 700, "#111827"),
        Line("capstone.yml re-run restores httpd_sys_content_t on /capstone-data", 11, 400, "#374151"),
        Line("curl succeeds again — MAC enforcement and idempotent remediation demonstrated together", 11, 700, "#14532d"),
    ])
    c.legend(60, 500, [("mgmt", "Integrated build"), ("alt", "Verified / remediated state"), ("warn", "Manual regression")])
    c.save(f"{OUT}/chapter-09-rhcsa-capstone-selinux-remediation-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
