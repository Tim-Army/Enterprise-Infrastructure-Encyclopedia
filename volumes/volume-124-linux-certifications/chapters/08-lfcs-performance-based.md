# Chapter 08: LFCS — The Performance-Based Exam

## Learning Objectives

- Cover the LFCS's five weighted domains with a lab each, in exam style: tasks, not questions.
- Train the performance-exam habits: speed, verification, and man-page fluency.
- Know the logistics: 2 hours, terminal-only, 2-year validity, one retake, simulator included.

## The exam in brief

**Exam:** Linux Foundation Certified System Administrator — **performance-based**: a live terminal, real tasks, no multiple choice. 2 hours; distribution-independent; online proctored; includes a killer.sh-style simulator and one retake; certification valid **2 years**. Five weighted domains:

| Domain | Weight |
|:---|:---|
| Operations Deployment | 25% |
| Networking | 25% |
| Storage | 20% |
| Essential Commands | 20% |
| Users and Groups | 10% |

**Exam habit:** every task below ends with a verification command — on a performance exam, unverified work is unscored work.

## Hands-On Lab

A disposable Linux VM. Each lab is phrased as an exam task. **Cost:** none.

### Lab 8.1 — Operations deployment (25%)

**Objective (task):** "Create a systemd service that runs a script at boot; enable and verify it."

```bash
sudo tee /usr/local/bin/labsvc.sh >/dev/null <<'EOF'
#!/bin/bash
echo "labsvc ran at $(date)" >> /var/log/labsvc.log
EOF
sudo chmod +x /usr/local/bin/labsvc.sh
sudo tee /etc/systemd/system/labsvc.service >/dev/null <<'EOF'
[Unit]
Description=Lab service
[Service]
Type=oneshot
ExecStart=/usr/local/bin/labsvc.sh
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable --now labsvc
systemctl is-enabled labsvc && sudo tail -1 /var/log/labsvc.log
```

**Expected result:** `enabled` and the log line — a unit written, enabled, started, and **verified**. Operations Deployment covers units/targets, scheduling (timers/cron), logs (journalctl), and process management: the daily-driver 25%.

**Negative test:** Forget `daemon-reload` after writing the unit — systemd doesn't see it; the reload step is the most-lost point on this domain.

**Rollback:** `sudo systemctl disable --now labsvc; sudo rm /etc/systemd/system/labsvc.service /usr/local/bin/labsvc.sh /var/log/labsvc.log`.

### Lab 8.2 — Networking (25%)

**Objective (task):** "Give the interface a second address, add a static route, and prove a port is listening."

```bash
sudo ip addr add 192.0.2.99/24 dev $(ip -brief route get 1.1.1.1 2>/dev/null | awk '{print $5}' | head -1) 2>/dev/null || sudo ip addr add 192.0.2.99/24 dev lo
ip -brief addr | grep 192.0.2.99
sudo ip route add 203.0.113.0/24 via 192.0.2.1 2>/dev/null || true; ip route | grep 203.0.113 || echo "route needs a reachable gateway"
python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &
sleep 1; ss -tln | grep 8080 && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/
kill %1
```

**Expected result:** The address present, the route logic exercised, `ss` showing the listener and curl returning `200` — addressing, routing, and socket verification: the Networking 25% (plus DNS client config, firewall basics, and time sync).

**Negative test:** Verify a "listening" service with `ps` instead of `ss` — a hung process shows in `ps` while the port is dead; sockets, not processes, are the proof.

**Rollback:** `sudo ip addr del 192.0.2.99/24 dev lo 2>/dev/null; sudo ip route del 203.0.113.0/24 2>/dev/null`.

### Lab 8.3 — Storage (20%)

**Objective (task):** "Create an LVM logical volume with a filesystem, mount it persistently, and verify."

```bash
dd if=/dev/zero of=/tmp/pv.img bs=1M count=128 status=none
LOOP=$(sudo losetup -f --show /tmp/pv.img)
sudo pvcreate $LOOP && sudo vgcreate lfcsvg $LOOP && sudo lvcreate -L 64M -n data lfcsvg
sudo mkfs.ext4 -q /dev/lfcsvg/data && sudo mkdir -p /mnt/data && sudo mount /dev/lfcsvg/data /mnt/data
df -h /mnt/data | tail -1
echo "persist: /dev/lfcsvg/data /mnt/data ext4 defaults 0 2  >> /etc/fstab (then mount -a to verify!)"
```

**Expected result:** The LV mounted and reported by `df` — the full storage chain (PV→VG→LV→fs→mount) plus the fstab persistence step and its **`mount -a` verification** (an fstab typo that breaks boot is the worst unverified change on this exam).

**Negative test:** Write the fstab line and *don't* run `mount -a` — a typo surfaces at reboot as emergency mode; the verification habit is the point.

**Rollback:** `sudo umount /mnt/data; sudo vgremove -f lfcsvg; sudo losetup -d $LOOP; rm /tmp/pv.img`.

### Lab 8.4 — Essential commands (20%)

**Objective (task):** "Find, filter, transform, and archive — against the clock."

```bash
mkdir -p /tmp/ec && cd /tmp/ec
seq 1 100 | sed 's/^/line /' > data.txt
grep -c "line" data.txt
awk '$2 % 10 == 0 {print $2}' data.txt | tail -3
find /tmp/ec -name "*.txt" -size -1M -exec tar czf archive.tgz {} +
tar tzf archive.tgz
```

**Expected result:** `100`, then `80 90 100`, then the archive listing `data.txt` — grep/awk/find/tar under time pressure. Essential Commands is LPIC-1 Topic 103's ground on a stopwatch: the difference is speed and the absence of a multiple-choice safety net.

**Negative test:** `find -exec ... \;` (per-file) vs `+` (batched) on thousands of files — same result, very different runtime; on a timed exam, that difference is points.

**Rollback:** `rm -rf /tmp/ec`.

### Lab 8.5 — Users and groups (10%)

**Objective (task):** "Create a user with a specific group set, password policy, and sudo scope; verify each."

```bash
sudo groupadd -f ops
sudo useradd -m -G ops -s /bin/bash lfcsuser
sudo chage -M 60 -W 7 lfcsuser && sudo chage -l lfcsuser | head -2
echo 'lfcsuser ALL=(ALL) NOPASSWD: /usr/bin/systemctl status *' | sudo tee /etc/sudoers.d/lfcsuser >/dev/null
sudo visudo -cf /etc/sudoers.d/lfcsuser
id lfcsuser
```

**Expected result:** The user in `ops`, password aging set (max 60, warn 7), and a **validated** scoped sudoers entry (`visudo -cf` says parsed OK) — users, groups, aging, and sudo scoping: the 10% that is pure rote points if drilled.

**Negative test:** Write the sudoers file without `visudo -cf` validation — a syntax error can lock sudo entirely; the validator is non-negotiable.

**Rollback:** `sudo userdel -r lfcsuser; sudo groupdel ops; sudo rm /etc/sudoers.d/lfcsuser`.

## Summary and Completion Checklist

- [ ] All five LFCS domains drilled as timed tasks with verification steps.
- [ ] The daemon-reload, mount -a, ss-not-ps, and visudo -cf habits installed.
- [ ] Simulator scheduled (included with registration) before the real sitting.
