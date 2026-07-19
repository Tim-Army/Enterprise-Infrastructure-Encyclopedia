import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-06-enterprise-storage-data-protection"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Hands-On Lab: Storage Service Catalog Validated Against a Measured fio Baseline",
        subtitle="A queue-depth-32 baseline is recorded against the gold tier's targets, then compared to a starved queue-depth-1 run",
        svg_title="Chapter 1 lab flow: a storage service catalog's gold tier validated against a measured fio baseline, with a queue-depth negative test",
        svg_desc="A 4 GB loopback device stands in for a spare block device. storage-service-catalog.yaml defines "
                  "a gold tier (SSD, RAID10, 5ms target latency, 7500 IOPS/TB). fio runs a 70/30 read/write random "
                  "4k profile at queue depth 32, and the measured IOPS and p99 latency are recorded next to the "
                  "catalog's targets. As a negative test, the same job re-run at queue depth 1 shows IOPS dropping "
                  "sharply even though per-operation latency looks similar, demonstrating that queue depth — not "
                  "just raw device speed — determines achievable IOPS, and why a host misconfigured with a "
                  "shallow queue depth under-performs its provisioned storage tier.")
    c.node_box(60, 140, 240, 100, "neutral", [
        Line("storage-service-catalog.yaml", 12.5, 700, "#111827"),
        Line("gold tier: SSD, RAID10", 10.5, 400, "#374151"),
        Line("target: 5ms, 7500 IOPS/TB", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 100, "mgmt", [
        Line("fio (iodepth=32)", 12.5, 700, "#111827"),
        Line("randrw, rwmixread=70, bs=4k", 10.5, 400, "#374151"),
        Line("measured IOPS + p99 latency", 10.5, 700, "#1d4ed8"),
    ])
    c.connector(300, 190, 380, 190, "neutral", label="compare against")
    c.node_box(700, 140, 220, 100, "alt", [
        Line("Recorded Baseline", 12.5, 700, "#111827"),
        Line("results appended to catalog", 10.5, 400, "#374151"),
        Line("(as a companion results: block)", 10, 400, "#374151"),
    ])
    c.connector(620, 190, 700, 190, "mgmt")
    c.node_box(60, 320, 840, 120, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("same job re-run at iodepth=1, numjobs=1 against the same loop device", 11, 400, "#7f1d1d"),
        Line("IOPS drops sharply vs. the iodepth=32 run, even though per-operation latency looks similar", 11, 400, "#7f1d1d"),
        Line("proves queue depth — not raw device speed — bounds achievable IOPS", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Measured baseline"), ("alt", "Catalog comparison"), ("warn", "Queue-depth negative test")])
    c.save(f"{OUT}/chapter-01-storage-catalog-fio-baseline-flow.svg")


def ch02():
    c = Canvas(960, 600,
        title="Chapter 2 Hands-On Lab: iSCSI Target/Initiator Pair with CHAP Authentication",
        subtitle="client01 logs into storage01's LUN over CHAP; a wrong password proves the ACL actually enforces authentication",
        svg_title="Chapter 2 lab topology: an iSCSI target and initiator pair authenticated with CHAP, tested against a wrong password",
        svg_desc="storage01 exposes a 2 GB fileio-backed LUN through target IQN "
                  "iqn.2026-07.lab.example:storage01, with an ACL for client01's IQN and CHAP credentials "
                  "(labuser/LabSecret123) on portal 3260. client01 discovers and logs in, reaching state LOGGED_IN "
                  "with a new block device matching the 2 GB LUN. As a negative test, client01 logs out, sets an "
                  "intentionally wrong CHAP password, and attempts to log back in; the login fails with an "
                  "authentication error and journalctl shows the rejected CHAP negotiation, confirming the ACL and "
                  "CHAP configuration actively enforce authentication rather than silently permitting access.")
    c.node_box(370, 130, 220, 130, "mgmt", [
        Line("storage01 (target)", 13.5, 700, "#111827"),
        Line("IQN ...:storage01", 10.5, 400, "#374151"),
        Line("LUN: 2G fileio, portal 3260", 10.5, 400, "#374151"),
        Line("ACL + CHAP: labuser", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(80, 320, 260, 110, "alt", [
        Line("client01 (correct CHAP)", 12.5, 700, "#111827"),
        Line("session: LOGGED_IN", 11, 700, "#14532d"),
        Line("lsblk: new 2G block device", 10.5, 400, "#374151"),
    ])
    c.node_box(620, 320, 260, 110, "warn", [
        Line("client01 (negative test)", 12.5, 700, "#111827"),
        Line("password set to WrongPassword", 10.5, 700, "#7f1d1d"),
        Line("login fails: auth error", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(430, 260, 250, 320, "alt", label="CHAP: labuser/LabSecret123")
    c.connector(530, 260, 720, 320, "warn", label="CHAP: labuser/WrongPassword")
    c.node_box(80, 470, 800, 80, "neutral", [
        Line("journalctl -u iscsid shows the rejected CHAP negotiation; restoring the correct password logs back in successfully", 11.5, 400, "#374151"),
    ])
    c.legend(80, 570, [("mgmt", "iSCSI target"), ("alt", "Authenticated session"), ("warn", "Rejected negotiation")])
    c.save(f"{OUT}/chapter-02-iscsi-chap-auth-topology.svg")


def ch03():
    c = Canvas(960, 600,
        title="Chapter 3 Hands-On Lab: NFS Root-Squash Enforcement, Proven and Then Disabled",
        subtitle="A client's root-created file lands as nobody with root_squash, and as UID 0 once no_root_squash is set",
        svg_title="Chapter 3 lab topology: an NFS export's root-squash behavior verified positively and then reversed as a negative test",
        svg_desc="nfs-server01 exports /export/lab to nfs-client01 with the default, secure root_squash option. "
                  "The client mounts the export and creates a file as root; on the server, that file is owned by "
                  "the anonymous UID/GID (typically 65534, nobody/nogroup), confirming root-squash maps the "
                  "client's root user to an unprivileged account. As a negative test, the export is changed to "
                  "no_root_squash and reapplied; after remounting, the same root-created-file operation now "
                  "produces a file genuinely owned by UID 0 on the server — demonstrating exactly why "
                  "no_root_squash should be reserved for narrowly justified cases and never used as a default.")
    c.node_box(370, 130, 220, 120, "mgmt", [
        Line("nfs-server01", 13.5, 700, "#111827"),
        Line("/export/lab", 10.5, 400, "#374151"),
        Line("(rw,sync,root_squash)", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(80, 320, 260, 120, "alt", [
        Line("nfs-client01 (root_squash)", 12.5, 700, "#111827"),
        Line("touch as root →", 10.5, 400, "#374151"),
        Line("file owned by nobody/nogroup", 10.5, 700, "#14532d"),
        Line("(65534, not UID 0)", 10, 400, "#374151"),
    ])
    c.node_box(620, 320, 260, 120, "warn", [
        Line("nfs-client01 (negative test)", 12.5, 700, "#111827"),
        Line("export → no_root_squash", 10.5, 700, "#7f1d1d"),
        Line("touch as root →", 10.5, 400, "#7f1d1d"),
        Line("file owned by UID 0 (real root)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(430, 250, 250, 320, "alt", label="NFSv4 mount")
    c.connector(530, 250, 720, 320, "warn", label="NFSv4 remount")
    c.legend(80, 500, [("mgmt", "NFS export"), ("alt", "root_squash (default, secure)"), ("warn", "no_root_squash (negative test)")])
    c.save(f"{OUT}/chapter-03-nfs-root-squash-topology.svg")


def ch04():
    c = Canvas(960, 640,
        title="Chapter 4 Hands-On Lab: DM-Multipath Over Dual iSCSI Paths, Surviving a Path Failure",
        subtitle="mpatha stays mounted and readable when one of its two iSCSI paths is logged out",
        svg_title="Chapter 4 lab topology: DM-Multipath aggregating two iSCSI paths to one LUN, tested against a simulated path failure",
        svg_desc="storage01 presents one 2 GB LUN through two independent portals (ip_A and ip_B). client01 logs "
                  "into both, producing two raw block devices for the same LUN; multipathd aggregates them into "
                  "mpatha with round-robin path selection, both paths active ready running. mpatha is formatted "
                  "and mounted, proving it behaves as one consistent block device. As a negative test, client01 "
                  "logs out of the session on ip_A only; multipath -ll shows that path as failed faulty running "
                  "while the remaining path stays active ready running, and the mounted filesystem's file reads "
                  "continue without interruption — multipath failover, not the application, absorbed the path "
                  "loss. Restoring the path returns it to active ready running via failback immediate.")
    c.node_box(370, 110, 220, 100, "mgmt", [
        Line("storage01", 13.5, 700, "#111827"),
        Line("LUN01 (2G) — 2 portals", 10.5, 400, "#374151"),
        Line("ip_A:3260, ip_B:3260", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 260, 220, 140, "alt", [
        Line("client01 — mpatha", 13, 700, "#111827"),
        Line("path A: active ready running", 10.5, 400, "#374151"),
        Line("path B: active ready running", 10.5, 400, "#374151"),
        Line("round-robin, /mnt/multipath-lab", 10, 400, "#374151"),
    ])
    c.connector(430, 210, 430, 260, "mgmt", label="path A")
    c.connector(530, 210, 530, 260, "mgmt", label="path B")
    c.node_box(700, 260, 220, 140, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("path A: iSCSI logout", 10.5, 700, "#7f1d1d"),
        Line("multipath -ll: path A", 10.5, 400, "#7f1d1d"),
        Line("failed faulty running", 10.5, 700, "#7f1d1d"),
        Line("path B alone keeps mpatha up", 10, 400, "#374151"),
    ])
    c.connector(590, 330, 700, 330, "warn")
    c.node_box(370, 460, 550, 90, "neutral", [
        Line("cat testfile.txt succeeds without interruption — application never saw the path loss", 11.5, 400, "#374151"),
        Line("path A restored → failback immediate returns it to active ready running", 11, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Dual iSCSI portals"), ("alt", "Multipath device (healthy)"), ("warn", "One path failed")])
    c.save(f"{OUT}/chapter-04-dm-multipath-failover-topology.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: Deduplicated restic Backups with Verified Restore and Encryption Enforcement",
        subtitle="A second backup grows the repository by only the changed file's size; a wrong password cannot read any snapshot",
        svg_title="Chapter 5 lab flow: a restic backup repository proven to deduplicate, restore correctly, and enforce its encryption",
        svg_desc="A restic repository is initialized with a password and two source files. The first backup "
                  "creates one snapshot tagged daily; after one file is modified, a second backup adds a second "
                  "snapshot whose repository growth (via restic stats --mode raw-data) matches only the changed "
                  "file's size, not a full second copy — direct evidence of block-level deduplication. Restoring "
                  "the latest snapshot to a separate directory produces a file identical to the current source "
                  "(diff shows no output). As a negative test, listing snapshots with an intentionally wrong "
                  "repository password fails with a decryption/authentication error rather than returning any "
                  "data, confirming the repository's encryption actually protects its contents.")
    c.node_box(60, 140, 240, 120, "mgmt", [
        Line("Source data", 12.5, 700, "#111827"),
        Line("file1.txt, file2.txt", 10.5, 400, "#374151"),
        Line("backup #1 → snapshot (daily)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 120, "alt", [
        Line("restic repository", 12.5, 700, "#111827"),
        Line("file1.txt modified → backup #2", 10.5, 400, "#374151"),
        Line("growth ≈ changed file only", 10.5, 700, "#14532d"),
        Line("(block-level dedup)", 10, 400, "#374151"),
    ])
    c.connector(300, 200, 380, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "neutral", [
        Line("Restore", 12.5, 700, "#111827"),
        Line("restic restore latest", 10.5, 400, "#374151"),
        Line("diff: no output (exact match)", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 200, 700, 200, "alt")
    c.node_box(60, 380, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("restic snapshots run with RESTIC_PASSWORD set to an intentionally wrong value", 11, 400, "#7f1d1d"),
        Line("fails with a decryption/authentication error — no snapshot data returned", 11, 400, "#7f1d1d"),
        Line("confirms the repository's encryption actually protects its contents, not cosmetically", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 550, [("mgmt", "Source + first backup"), ("alt", "Deduplicated increment"), ("warn", "Encryption enforcement")])
    c.save(f"{OUT}/chapter-05-restic-dedup-encryption-flow.svg")


def ch06():
    c = Canvas(960, 640,
        title="Chapter 6 Hands-On Lab: LVM Snapshot Point-in-Time Preservation and Reserve Exhaustion",
        subtitle="A 100 MB snapshot preserves the pre-change state until deliberately overrun, then reports invalid",
        svg_title="Chapter 6 lab flow: an LVM snapshot's copy-on-write behavior proven correct, then deliberately exhausted",
        svg_desc="lv_lab (1 GB origin) is formatted, mounted, and written with point-in-time A data. A 100 MB "
                  "snapshot lv_lab_snap is taken, then the origin is modified to point-in-time B; data_percent on "
                  "the snapshot rises above 0% as copy-on-write data accumulates. Mounted read-only, the snapshot "
                  "still shows point-in-time A while the origin shows point-in-time B, proving independent "
                  "preservation. As a negative test, enough new data (150 MB) is written to the origin to exceed "
                  "the snapshot's 100 MB reserve; data_percent reaches 100%, the snapshot's lv_attr shows an "
                  "invalidated state, and mounting it afterward fails or exposes a partial image — demonstrating "
                  "why proactive snapshot-reserve monitoring is required, not optional.")
    c.node_box(80, 130, 240, 110, "mgmt", [
        Line("lv_lab (origin, 1G)", 12.5, 700, "#111827"),
        Line("point-in-time A", 10.5, 400, "#374151"),
        Line("→ modified to point-in-time B", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 130, 240, 110, "alt", [
        Line("lv_lab_snap (100M reserve)", 12.5, 700, "#111827"),
        Line("data_percent rises with COW", 10.5, 400, "#374151"),
        Line("mounted RO: shows point-in-time A", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 185, 400, 185, "mgmt", label="snapshot + COW tracking")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("150 MB written to origin", 10.5, 700, "#7f1d1d"),
        Line("exceeds 100M reserve", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 185, 700, 185, "warn")
    c.node_box(80, 330, 840, 130, "warn", [
        Line("Result", 12.5, 700, "#7f1d1d"),
        Line("data_percent on lv_lab_snap reaches 100%; lv_attr shows an invalidated state (I/d flag)", 11, 400, "#7f1d1d"),
        Line("mounting the snapshot now fails or exposes a partial, unusable image", 11, 400, "#7f1d1d"),
        Line("demonstrates why proactive snapshot-reserve monitoring is required, not optional", 11, 400, "#7f1d1d"),
    ])
    c.legend(80, 510, [("mgmt", "Origin volume"), ("alt", "Healthy snapshot"), ("warn", "Exhausted / invalidated snapshot")])
    c.save(f"{OUT}/chapter-06-lvm-snapshot-exhaustion-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: Timed Application Failover and a Careless Failback",
        subtitle="app02 is promoted and measured against a timeline log; reversing rsync without reconciliation silently discards data",
        svg_title="Chapter 7 lab topology: a two-site application failover measured end to end, then a careless failback shown discarding data",
        svg_desc="app01 (primary, port 8080) serves content replicated asynchronously to app02 (DR site, port "
                  "8081) via rsync, representing the RPO-defining schedule. A timeline log records the failover "
                  "trigger and execution-complete timestamps. app01's service is killed to simulate failure; app02 "
                  "is promoted by updating its content and is confirmed serving traffic, with the timeline log "
                  "giving the measured execution-phase duration (the demonstrable RTO component). As a negative "
                  "test, new data written at app02 during the outage is discarded when a careless failback runs a "
                  "naive reverse rsync without any diff/reconciliation step — any independent change app01 had "
                  "accumulated would be silently overwritten with no warning and no conflict report.")
    c.node_box(60, 150, 240, 110, "mgmt", [
        Line("app01 (primary, :8080)", 12.5, 700, "#111827"),
        Line("PRIMARY - content version 1", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 150, 240, 110, "alt", [
        Line("app02 (DR, :8081)", 12.5, 700, "#111827"),
        Line("rsync replica, then PROMOTED", 10.5, 700, "#14532d"),
        Line("now serving as primary", 10.5, 400, "#374151"),
    ])
    c.connector(300, 205, 380, 205, "mgmt", label="rsync -avz --delete (async replication)")
    c.node_box(700, 150, 220, 110, "neutral", [
        Line("Timeline Log", 12.5, 700, "#111827"),
        Line("trigger → execution-complete", 10.5, 400, "#374151"),
        Line("measured execution-phase RTO", 10.5, 400, "#374151"),
    ])
    c.connector(620, 205, 700, 205, "neutral")
    c.node_box(60, 340, 860, 130, "warn", [
        Line("Negative Test — Careless Failback", 12.5, 700, "#7f1d1d"),
        Line("new data written at app02 during the outage window (\"NEW ORDER RECORD\")", 11, 400, "#7f1d1d"),
        Line("naive rsync app02 → app01, --delete, with no diff/reconciliation step", 11, 400, "#7f1d1d"),
        Line("app01's file now reflects only app02's final state — any local app01 change is silently discarded", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 610, [("mgmt", "Primary site"), ("alt", "Promoted DR site"), ("warn", "Careless failback (negative test)")])
    c.save(f"{OUT}/chapter-07-dr-failover-failback-topology.svg")


def ch08():
    c = Canvas(960, 640,
        title="Chapter 8 Hands-On Lab: Immutable Backup Copy Resists Deletion, Even by Root",
        subtitle="A chattr +i locked file survives a wildcard mass deletion that destroys its mutable twin",
        svg_title="Chapter 8 lab flow: a filesystem-immutable backup copy standing in for object-lock retention, tested against deletion and mass deletion",
        svg_desc="Two identical files are created: mutable-backup.tar and locked-backup.tar, the latter given the "
                  "immutable attribute (chattr +i) as a locally reproducible stand-in for object-lock/retention-"
                  "lock behavior. Deleting the mutable file as root succeeds normally; deleting the locked file as "
                  "the same root account fails with 'Operation not permitted', and modifying its contents also "
                  "fails — proving the lock resists both deletion and modification even under root privilege. As "
                  "a negative test simulating a ransomware-style mass-deletion attempt, a wildcard rm of all .tar "
                  "files removes any remaining mutable files but reports an error for the locked file, which "
                  "remains present and intact.")
    c.node_box(80, 140, 260, 110, "alt", [
        Line("mutable-backup.tar", 12.5, 700, "#111827"),
        Line("no chattr flag", 10.5, 400, "#374151"),
        Line("rm as root → deletes normally", 10.5, 700, "#7c2d12"),
    ])
    c.node_box(620, 140, 260, 110, "mgmt", [
        Line("locked-backup.tar", 12.5, 700, "#111827"),
        Line("chattr +i (immutable)", 10.5, 700, "#1d4ed8"),
        Line("rm as root → Operation not permitted", 10.5, 700, "#14532d"),
    ])
    c.node_box(80, 320, 800, 110, "warn", [
        Line("Negative Test — Mass Deletion", 12.5, 700, "#7f1d1d"),
        Line("sudo rm -f *.tar (simulated ransomware-style wildcard mass deletion)", 11, 400, "#7f1d1d"),
        Line("mutable-backup.tar (if present) is destroyed; locked-backup.tar remains present and intact", 11, 400, "#7f1d1d"),
        Line("even a compromised root account cannot remove the locked copy before its retention window", 11, 400, "#7f1d1d"),
    ])
    c.connector(210, 250, 210, 320, "alt")
    c.connector(750, 250, 750, 320, "mgmt")
    c.legend(80, 500, [("mgmt", "Immutable (protected)"), ("alt", "Mutable (unprotected)"), ("warn", "Mass-deletion attempt")])
    c.save(f"{OUT}/chapter-08-immutable-backup-deletion-resistance-flow.svg")


def ch09():
    c = Canvas(960, 620,
        title="Chapter 9 Hands-On Lab: Trend-Based Capacity Forecast Outpaces a Static Threshold Alert",
        subtitle="A static 85% check stays silent through day 4 while the trend-based forecast already projects exhaustion",
        svg_title="Chapter 9 lab flow: a static capacity threshold compared against a trend-based forecast on the same growth data",
        svg_desc="A 300 MB loopback filesystem is grown across four simulated days via ~50 MB increments, with "
                  "used-percentage sampled into samples.csv after each. At day 4, a naive static-threshold check "
                  "(alerts only at 85% or higher) reports no alert, since current utilization is still below the "
                  "line. A trend-based forecast run against the same data instead reports a projected number of "
                  "days until 90% utilization, surfacing the exhaustion risk well before the static threshold "
                  "would ever fire. As a negative test, one more simulated day of growth (100 MB) finally trips "
                  "the static alert at day 5 — several days later than the trend-based forecast had already "
                  "projected the same risk.")
    c.node_box(60, 140, 260, 110, "neutral", [
        Line("samples.csv", 12.5, 700, "#111827"),
        Line("day 1-4: used_percent rising", 10.5, 400, "#374151"),
        Line("~50 MB growth per sample", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "warn", [
        Line("Static threshold check", 12.5, 700, "#111827"),
        Line("fires only at ≥ 85%", 10.5, 400, "#374151"),
        Line("day 4: no alert (below 85%)", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(680, 140, 240, 110, "alt", [
        Line("Trend-based forecast", 12.5, 700, "#111827"),
        Line("forecast.py on same data", 10.5, 400, "#374151"),
        Line("projects days to 90% now", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 195, 380, 195, "neutral")
    c.connector(320, 195, 680, 195, "neutral")
    c.node_box(60, 380, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("one more day of growth (100 MB) added, sample 5 recorded", 11, 400, "#7f1d1d"),
        Line("static alert finally fires at day 5 — several days after the trend forecast already projected the risk", 11, 400, "#7f1d1d"),
        Line("concrete evidence that trend-based monitoring detects capacity risk earlier than a static threshold", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 550, [("neutral", "Sampled growth data"), ("alt", "Trend forecast (early warning)"), ("warn", "Static threshold (late warning)")])
    c.save(f"{OUT}/chapter-09-capacity-trend-forecast-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
