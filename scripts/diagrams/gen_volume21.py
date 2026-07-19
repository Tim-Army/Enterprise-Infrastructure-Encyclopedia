import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-21-ubuntu-server-cloud-26-04-lts"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Hands-On Lab: An Invalid Pro Token Fails Cleanly, With No Partial Repository State",
        subtitle="An unattended autoinstall completes from a NoCloud seed and attaches real ESM; a bad token is rejected without touching any configuration",
        svg_title="Chapter 1 lab flow: an unattended Ubuntu autoinstall validated end to end, then Ubuntu Pro attach tested against a deliberately invalid token",
        svg_desc="A NoCloud seed ISO built from autoinstall user-data drives a fully unattended installation that "
                  "reboots into a working system with cloud-init reporting status: done. Default repository "
                  "pockets (release, updates, security, backports) are confirmed present, and attaching a real "
                  "Ubuntu Pro token enables esm-infra and esm-apps. As a negative test, attaching with a "
                  "deliberately invalid token reports an invalid-token error and makes no changes to the system's "
                  "repository configuration at all, confirming a failed attach never leaves the host in a "
                  "partially configured state.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("NoCloud autoinstall seed", 12.5, 700, "#111827"),
        Line("unattended install → reboot", 10.5, 400, "#374151"),
        Line("cloud-init status: done", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Real Pro token attach", 12.5, 700, "#111827"),
        Line("esm-infra + esm-apps: enabled", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("invalid token attach", 10.5, 700, "#7f1d1d"),
        Line("→ error, zero repo changes", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("a failed attach never leaves the host in a partially configured repository state — the operation is", 11.5, 400, "#374151"),
        Line("atomic: it either fully succeeds or makes no change at all.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Unattended provisioning"), ("alt", "Successful ESM attach"), ("warn", "Rejected invalid token")])
    c.save(f"{OUT}/chapter-01-autoinstall-pro-attach-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A Quoting Bug Demonstrated Live, Then a Clean Snap Rollback",
        subtitle="An unquoted variable word-splits into two arguments; snap revert cleanly restores a prior working revision",
        svg_title="Chapter 2 lab flow: an administrative audit script exercised against real package activity, then deliberately broken to demonstrate a quoting bug, alongside a snap rollback",
        svg_desc="disk-and-pkg-report.sh prints disk usage, recent dpkg installs, and largest /var directories "
                  "cleanly; installing a small test package makes it appear in the next run automatically. As a "
                  "negative test, a copy of the script replaces a quoted path with an unquoted multi-word "
                  "variable; running it word-splits the value into two separate arguments, and du reports it "
                  "cannot access a directory literally named audit in the current working directory. Separately, "
                  "a test snap is installed and reverted; snap list --all shows the prior revision retained "
                  "alongside the current one, confirming rollback preserves history rather than discarding it.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("disk-and-pkg-report.sh", 12.5, 700, "#111827"),
        Line("apt install tree → new dpkg.log entry", 10.5, 400, "#374151"),
        Line("re-run picks it up automatically", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("snap revert hello-world", 12.5, 700, "#111827"),
        Line("prior revision retained", 10.5, 700, "#14532d"),
        Line("alongside the current one", 10.5, 400, "#374151"),
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
        Line("\"$TESTDIR\" (quoted) would pass one intact argument to du — the unquoted version demonstrates", 11.5, 400, "#374151"),
        Line("exactly why shell quoting around multi-word variables matters.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Audit script + real package activity"), ("alt", "Snap rollback"), ("warn", "Quoting bug (negative test)")])
    c.save(f"{OUT}/chapter-02-apt-snap-quoting-rollback-flow.svg")


def ch03():
    c = Canvas(960, 560,
        title="Chapter 3 Hands-On Lab: systemd Surfaces an Exec Failure Directly Rather Than Failing Silently",
        subtitle="A scoped service account's timer runs and logs cleanly; pointing ExecStart at a missing script produces an explicit, journal-visible failure",
        svg_title="Chapter 3 lab flow: a custom systemd service and timer running under a dedicated account, tested against a missing ExecStart target",
        svg_desc="lab-report.timer fires lab-report.service under the dedicated svc-labreport account; "
                  "triggering it manually logs the report text to the journal under that user, with the unit "
                  "settling to inactive (dead) and its last run marked SUCCESS. As a negative test, ExecStart is "
                  "pointed at a nonexistent script; starting the service now reports Active: failed, and the "
                  "journal shows a 203/EXEC (No such file or directory) error — confirming systemd surfaces exec "
                  "failures directly rather than failing silently. Restoring the correct path runs the service "
                  "cleanly again.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("lab-report.timer", 12.5, 700, "#111827"),
        Line("triggers lab-report.service", 10.5, 400, "#374151"),
        Line("as svc-labreport", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("journalctl -u lab-report.service", 12, 700, "#111827"),
        Line("report text logged", 10.5, 700, "#14532d"),
        Line("last run: SUCCESS", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("ExecStart → missing script", 10.5, 700, "#7f1d1d"),
        Line("Active: failed, 203/EXEC", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("203/EXEC means systemd could not even execute the configured binary — a distinct, journal-visible", 11.5, 400, "#374151"),
        Line("signature, not a silent no-op. Restoring the correct path runs the service cleanly again.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Scoped service + timer"), ("alt", "Verified via journal"), ("warn", "Missing-binary failure")])
    c.save(f"{OUT}/chapter-03-systemd-timer-exec-failure-flow.svg")


def ch04():
    c = Canvas(960, 620,
        title="Chapter 4 Hands-On Lab: ufw's Default-Deny Policy Confirmed Against an Unlisted Port",
        subtitle="SSH keeps working through a hardened, Netplan-safe configuration while an unlisted listener port is actually unreachable",
        svg_title="Chapter 4 lab topology: a scoped admin account, hardened SSH, a safe Netplan rollback, and a default-deny ufw policy, tested against an unlisted port",
        svg_desc="labadmin authenticates by key; sshd is hardened (PermitRootLogin no, PasswordAuthentication "
                  "no) and reloaded only after sshd -t confirms valid syntax. A static Netplan configuration "
                  "applies via netplan try, which auto-rolls-back if connectivity isn't confirmed within its "
                  "countdown. ufw enables with a default-deny inbound policy and an explicit OpenSSH allow. As a "
                  "negative test, a listener is started on an unlisted port (8080) and a connection attempt from "
                  "a second host times out or is refused, confirming ufw's default-deny policy actually blocks "
                  "traffic to ports with no explicit allow rule, while SSH on port 22 continues to succeed "
                  "throughout.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("labadmin + hardened sshd", 12.5, 700, "#111827"),
        Line("key-based auth, password auth off", 10.5, 400, "#374151"),
        Line("Netplan applied via netplan try", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 110, "alt", [
        Line("ufw: default deny incoming", 12.5, 700, "#111827"),
        Line("OpenSSH explicitly allowed", 10.5, 700, "#14532d"),
        Line("SSH continues to succeed", 10.5, 400, "#374151"),
    ])
    c.connector(320, 195, 400, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("nc listener on port 8080", 10.5, 700, "#7f1d1d"),
        Line("→ connection times out/refused", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 195, 700, 195, "warn")
    c.node_box(60, 300, 860, 90, "neutral", [
        Line("the unlisted port is genuinely unreachable while SSH on the explicitly allowed port keeps working —", 11.5, 400, "#374151"),
        Line("confirming ufw's default-deny policy is enforced, not merely configured.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 430, [("mgmt", "Hardened access baseline"), ("alt", "Explicitly allowed service"), ("warn", "Default-denied port")])
    c.save(f"{OUT}/chapter-04-ufw-netplan-hardening-topology.svg")


def ch05():
    c = Canvas(960, 600,
        title="Chapter 5 Hands-On Lab: An NFS Export Whose Subnet Restriction Actually Refuses a Third Host",
        subtitle="An LVM volume grows online with no unmount; the export's client scope is confirmed by a mount attempt from outside it",
        svg_title="Chapter 5 lab topology: an LVM-backed filesystem exported over NFS to one subnet, extended live and tested against a client outside that subnet",
        svg_desc="A spare disk becomes an LVM-backed ext4 filesystem mounted at /srv/labdata; lvextend plus "
                  "resize2fs grows it online with no unmount required. The volume exports over NFS scoped to "
                  "10.20.30.0/24, and a client on that subnet mounts it and writes a test file the server "
                  "confirms. As a negative test, a third host outside the permitted subnet attempts the identical "
                  "mount; it is refused with 'access denied by server', confirming the subnet restriction in "
                  "/etc/exports is enforced by the NFS server itself, not merely present as a configuration line.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("lab_vg/lab_lv (ext4)", 12.5, 700, "#111827"),
        Line("4G → live-extended to 6G", 10.5, 700, "#1d4ed8"),
        Line("no unmount required", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("NFS export: 10.20.30.0/24", 12, 700, "#111827"),
        Line("in-subnet client mounts,", 10.5, 700, "#14532d"),
        Line("writes confirmed by server", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("third host, outside subnet", 10.5, 700, "#7f1d1d"),
        Line("→ access denied by server", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the export line in /etc/exports shows the specific 10.20.30.0/24 scope rather than a wildcard —", 11.5, 400, "#374151"),
        Line("the refusal from outside that subnet is the concrete evidence the restriction is enforced.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "LVM growth"), ("alt", "Permitted NFS client"), ("warn", "Denied NFS client")])
    c.save(f"{OUT}/chapter-05-lvm-nfs-export-topology.svg")


def ch06():
    c = Canvas(960, 620,
        title="Chapter 6 Hands-On Lab: An AppArmor Profile That Allows One File and Logs the Denial of Another",
        subtitle="A generated profile permits the intended read and blocks the forbidden one with an explicit, named journal entry",
        svg_title="Chapter 6 lab flow: an AppArmor profile generated interactively for a custom script, enforcing a narrow allow list, plus a LUKS-encrypted scratch volume",
        svg_desc="aa-genprof watches a script that reads one allowed file and attempts to read /etc/shadow; the "
                  "generated profile approves the allowed read and denies the shadow-file attempt, loading in "
                  "enforce mode. Running the script again shows the allowed content printing normally. As a "
                  "negative test, the same run's forbidden read now errors or returns nothing, and the kernel "
                  "journal shows an apparmor=\"DENIED\" entry naming both /etc/shadow and the read-config.sh "
                  "profile — direct, attributable evidence enforcement is active. Separately, a loop-backed LUKS "
                  "volume encrypts, mounts, and accepts a written file normally, confirmed by a single active "
                  "keyslot.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("aa-genprof: read-config.sh", 12.5, 700, "#111827"),
        Line("allowed.conf: approved", 10.5, 700, "#1d4ed8"),
        Line("/etc/shadow: denied at profile time", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Allowed read (enforce mode)", 12.5, 700, "#111827"),
        Line("allowed.conf content prints", 10.5, 700, "#14532d"),
        Line("normally", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("/etc/shadow read blocked", 10.5, 700, "#7f1d1d"),
        Line("apparmor=\"DENIED\" logged,", 10.5, 700, "#7f1d1d"),
        Line("names file + profile", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("separately, a loop-backed LUKS volume encrypts, mounts, and accepts a written file normally,", 11.5, 400, "#374151"),
        Line("confirmed by a single active keyslot in the LUKS header.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Profile generation"), ("alt", "Permitted read"), ("warn", "Denied + logged read")])
    c.save(f"{OUT}/chapter-06-apparmor-luks-confinement-flow.svg")


def ch07():
    c = Canvas(960, 580,
        title="Chapter 7 Hands-On Lab: BIND9 Reports an Authoritative NXDOMAIN, Not a Guess",
        subtitle="A defined name resolves and serves real content end to end; an undefined name gets a proper negative answer, not silence or a forwarded guess",
        svg_title="Chapter 7 lab flow: an authoritative BIND9 zone feeding an Nginx virtual host, validated end to end and tested against an undefined DNS name",
        svg_desc="A lab.internal zone resolves web01.lab.internal to 127.0.0.1 directly against BIND9; chrony "
                  "reports synchronized time, and an Nginx virtual host on that hostname serves real content, "
                  "confirmed by a Host-header curl request returning the expected HTML — the full DNS-to-HTTP "
                  "chain working together. As a negative test, a name never defined in the zone is queried; no "
                  "address is returned and the response status shows NXDOMAIN, confirming BIND9 correctly reports "
                  "an authoritative negative answer for its own zone rather than guessing or silently forwarding "
                  "the query elsewhere.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("BIND9: lab.internal zone", 12.5, 700, "#111827"),
        Line("web01.lab.internal → 127.0.0.1", 10.5, 700, "#1d4ed8"),
        Line("chrony: synchronized", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Nginx vhost + curl", 12.5, 700, "#111827"),
        Line("Host: web01.lab.internal", 10.5, 400, "#374151"),
        Line("→ expected HTML returned", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("query for undefined name", 10.5, 700, "#7f1d1d"),
        Line("→ NXDOMAIN, no address", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("NXDOMAIN is an authoritative negative answer specific to this zone — BIND9 neither guesses nor", 11.5, 400, "#374151"),
        Line("silently forwards a query for a name it is authoritative for but has never defined.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Authoritative DNS zone"), ("alt", "End-to-end resolution + serving"), ("warn", "Authoritative negative answer")])
    c.save(f"{OUT}/chapter-07-bind9-nginx-nxdomain-flow.svg")


def ch08():
    c = Canvas(960, 640,
        title="Chapter 8 Hands-On Lab: The chgrp-0/chmod-g=u Pattern Is What Makes an Image Survive an Arbitrary UID",
        subtitle="Docker and LXD both serve the same app independently; a naively built image fails under an OpenShift-style random UID while the portable one succeeds",
        svg_title="Chapter 8 lab flow: the same web app run as a Docker container and an LXD system container, then two image-build patterns tested against an arbitrary UID",
        svg_desc="A Docker container and an independent LXD system container both serve the same simple web "
                  "application from their own addresses, proving the two container technologies coexist without "
                  "interfering with each other. Two variants of a minimal app image are built: a naive one owned "
                  "by root with mode 700, and a portable one using chgrp 0 plus chmod g=u. As a negative test, "
                  "both images run under an arbitrary UID (543210) that was never part of the build; the naive "
                  "image exits non-zero with a permission error writing its output file, because that UID belongs "
                  "to neither root nor any group with write access, while the portable image exits 0, because the "
                  "root-group ownership pattern grants write access to any UID as long as it belongs to group 0 — "
                  "exactly how OpenShift assigns UIDs to containers by default.")
    c.node_box(60, 130, 220, 110, "mgmt", [
        Line("Docker container", 12.5, 700, "#111827"),
        Line("nginx on :8080", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 220, 110, "mgmt", [
        Line("LXD system container", 12.5, 700, "#111827"),
        Line("own IP, own nginx", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 130, 220, 110, "neutral", [
        Line("Both serve independently", 12, 700, "#111827"),
        Line("no interference between", 10.5, 400, "#374151"),
        Line("the two container technologies", 10.5, 400, "#374151"),
    ])
    c.connector(280, 185, 360, 185, "mgmt")
    c.connector(580, 185, 700, 185, "neutral")
    c.node_box(60, 300, 400, 130, "warn", [
        Line("Naive image (chown root, mode 700)", 12, 700, "#111827"),
        Line("run --user 543210", 10.5, 700, "#7f1d1d"),
        Line("→ PermissionError writing output.txt", 10.5, 700, "#7f1d1d"),
        Line("(UID in neither root nor a writable group)", 10, 400, "#7f1d1d"),
    ])
    c.node_box(500, 300, 400, 130, "alt", [
        Line("Portable image (chgrp 0, chmod g=u)", 12, 700, "#111827"),
        Line("run --user 543210", 10.5, 700, "#14532d"),
        Line("→ exit 0, write succeeds", 10.5, 700, "#14532d"),
        Line("(any UID in group 0 can write)", 10, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Independent container runtimes"), ("warn", "Fails under arbitrary UID"), ("alt", "Survives arbitrary UID")])
    c.save(f"{OUT}/chapter-08-docker-lxd-arbitrary-uid-flow.svg")


def ch09():
    c = Canvas(960, 620,
        title="Chapter 9 Hands-On Lab: The Capstone — Ansible's --check Mode Proven to Change Nothing",
        subtitle="cloud-init hands off a deliberately minimal host; Ansible completes the baseline, and its dry run is confirmed to leave the live system untouched",
        svg_title="Chapter 9 lab flow: a cloud-init minimal hand-off completed by an Ansible baseline playbook, tested against Ansible's check-mode dry run",
        svg_desc="A cloud-init seed creates only an Ansible-manageable user and installs no hardening at all; "
                  "cloud-init status shows done while ufw reports inactive or not installed, confirming hardening "
                  "was deliberately left to Ansible rather than cloud-init. An Ansible baseline playbook installs "
                  "chrony and ufw, sets a default-deny inbound firewall policy with an OpenSSH allow rule, and "
                  "enables both services. As a negative test, the playbook first runs in --check mode; it reports "
                  "tasks as changed (what would happen), but an immediate live SSH check shows ufw is still "
                  "inactive, proving check mode made no real change to the host. Applying the playbook for real "
                  "brings ufw active and chrony running, and re-running it shows changed=0 for every task, "
                  "confirming end-to-end idempotency across the whole provisioning chain.")
    c.node_box(60, 130, 260, 110, "mgmt", [
        Line("cloud-init minimal seed", 12.5, 700, "#111827"),
        Line("creates ansible user only", 10.5, 400, "#374151"),
        Line("status: done, ufw not yet configured", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 130, 240, 110, "warn", [
        Line("Negative Test: --check --diff", 12, 700, "#7f1d1d"),
        Line("reports tasks as \"changed\"", 10.5, 700, "#7f1d1d"),
        Line("live ufw status: still inactive", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 185, 400, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Real apply", 12.5, 700, "#111827"),
        Line("ufw active, default-deny + SSH", 10.5, 700, "#14532d"),
        Line("chrony active", 10.5, 400, "#374151"),
    ])
    c.connector(640, 185, 700, 185, "alt")
    c.node_box(60, 320, 860, 100, "neutral", [
        Line("--check mode reported the pending changes accurately but genuinely applied none of them —", 11.5, 400, "#374151"),
        Line("re-running the playbook for real afterward shows changed=0 for every task, confirming full idempotency", 11.5, 400, "#374151"),
        Line("end to end across cloud-init hand-off and Ansible convergence together.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Minimal cloud-init hand-off"), ("warn", "Dry run (no real change)"), ("alt", "Applied, idempotent baseline")])
    c.save(f"{OUT}/chapter-09-cloudinit-ansible-checkmode-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
