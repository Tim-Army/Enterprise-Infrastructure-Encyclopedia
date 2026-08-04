# Chapter 04: LPIC-1 — Exam 102 (102-500)

## Learning Objectives

- Cover exam 102-500's six topics with a walkthrough lab each.
- Drill shells/scripting, desktops, administrative tasks, system services, networking, and security.
- Work from the published v5.0 objectives.

## The exam in brief

**Exam:** 102-500 (objectives v5.0), LPIC-1's second exam. Six topics: **105 Shells and Shell Scripting**, **106 User Interfaces and Desktops**, **107 Administrative Tasks**, **108 Essential System Services**, **109 Networking Fundamentals**, **110 Security**. Passing both 101-500 and 102-500 earns LPIC-1 (5-year validity).

## Hands-On Lab

Any Linux VM. **Cost:** none.

### Lab 4.1 — Shells and scripting (Topic 105)

**Objective:** Write the exam's scripting repertoire: variables, tests, loops, exit codes.

```bash
cat > check.sh <<'EOF'
#!/bin/bash
LIMIT=${1:-3}
for f in /etc/hostname /etc/nosuch; do
  if [ -r "$f" ]; then echo "OK: $f"; else echo "MISSING: $f"; fi
done
seq 1 "$LIMIT" | while read -r n; do echo "tick $n"; done
exit 0
EOF
chmod +x check.sh && ./check.sh 2 && echo "exit=$?"
```

**Expected result:** `OK`/`MISSING` per file, two ticks, `exit=0` — parameters with defaults, `[ ]` tests, loops, and exit status: Topic 105's grammar, plus environment (`export`, `.profile`/`.bashrc`) and aliases/functions.

**Negative test:** Change `exit 0` to `exit 3`; `echo $?` prints `3` and `&&` chains stop running — exit codes drive scripting logic, and the exam tests reading them.

**Cleanup:** `rm check.sh`.

### Lab 4.2 — User interfaces and desktops (Topic 106)

**Objective:** Know the display stack without needing a desktop installed.

```bash
echo $XDG_SESSION_TYPE 2>/dev/null || true
ls /usr/share/xsessions 2>/dev/null || echo "no desktop sessions installed (server)"
cat <<'EOF'
stack: display server (X11 or Wayland) -> display manager (gdm/sddm/lightdm) -> desktop (GNOME/KDE)
remote: X forwarding (ssh -X), VNC, RDP, SPICE ; accessibility: screen readers, high contrast, sticky keys
EOF
```

**Expected result:** The session type (or a clean "server" answer) and the stack recited — Topic 106 is the lightest topic: X11 vs Wayland, display managers, remote desktop options, and accessibility features.

**Negative test:** Claiming a server needs X installed for `ssh -X` *from* it — forwarding needs the client-side pieces (`xauth`) not a full desktop; a favorite trick question.

**Cleanup:** None.

### Lab 4.3 — Administrative tasks (Topic 107)

**Objective:** Manage users, groups, and scheduled jobs.

```bash
sudo useradd -m -s /bin/bash labuser && sudo usermod -aG users labuser
id labuser
echo '17 3 * * 1 /usr/bin/uptime' | sudo tee /tmp/labcron >/dev/null && sudo crontab -u labuser /tmp/labcron
sudo crontab -l -u labuser
date -d "next Monday 03:17" 2>/dev/null || true
```

**Expected result:** `labuser` created with group membership shown by `id`, and a crontab installed reading `17 3 * * 1` — Mondays at 03:17. Users/groups (`useradd/usermod/passwd`, `/etc/passwd`, `/etc/shadow`), cron/anacron/systemd timers, and localization (`locale`, `TZ`) make up Topic 107.

**Negative test:** Read the cron line as "3:17 every day" — field order (minute hour dom month dow) says otherwise; cron-field ordering is a guaranteed exam item.

**Cleanup:** `sudo crontab -r -u labuser; sudo userdel -r labuser; rm /tmp/labcron`.

### Lab 4.4 — Essential system services (Topic 108)

**Objective:** Touch time, logging, mail, and printing — the four services of Topic 108.

```bash
timedatectl | head -4
journalctl --since "-5 min" -n 3 --no-pager
logger "lpic1 lab marker" && journalctl -t $(whoami) -n 1 --no-pager 2>/dev/null || journalctl -n 1 --no-pager | tail -1
echo "mail: MTA concepts (postfix/sendmail aliases, ~/.forward) ; print: CUPS (lpadmin, lpstat)"
```

**Expected result:** NTP-synchronized time status, recent journal entries, and your own `logger` marker retrieved from the journal — timekeeping (`timedatectl`/chrony), logging (journald + rsyslog), and awareness of MTA and CUPS basics complete the topic.

**Negative test:** `timedatectl set-time` while NTP sync is active — refused; the daemon owns the clock, an operational truth the exam encodes.

**Cleanup:** None.

### Lab 4.5 — Networking fundamentals (Topic 109)

**Objective:** Address, route, resolve, and test — the client-side networking loop.

```bash
ip -brief addr
ip route | head -2
getent hosts localhost
ping -c1 -W2 127.0.0.1 | tail -2
ss -tln | head -5
```

**Expected result:** Interfaces with addresses, the default route, name resolution via the configured order (`nsswitch.conf`), a successful loopback ping, and listening sockets — Topic 109: IPv4/IPv6 basics, CIDR, `ip`, DNS client configuration (`/etc/resolv.conf`), and `ss`/`netstat` diagnostics.

**Negative test:** `ping` a firewalled host and conclude "network down" — TCP services may still answer; `ss`/`nc` distinguish ICMP policy from real outage, and the exam probes exactly that reasoning.

**Cleanup:** None.

### Lab 4.6 — Security (Topic 110)

**Objective:** Audit the host the way Topic 110 expects.

```bash
find / -perm -4000 -type f 2>/dev/null | head -5
sudo ss -tlnp | awk 'NR<=5'
last | head -3
sudo grep -c "^[^:]*:[^!*]" /etc/shadow
echo "harden: su/sudo policy, ulimits, ssh keys + agent, gpg basics, disable unused services"
```

**Expected result:** The SUID inventory (the exam's favorite audit), listening services with owning processes, recent logins, and a count of accounts with real password hashes — host security auditing plus the hardening checklist (sudo, limits, SSH key auth, GnuPG) that closes LPIC-1.

**Negative test:** A world-writable SUID-root binary (never create one outside a throwaway VM) is the canonical catastrophe the audit exists to catch — recognize the pattern on sight.

**Cleanup:** None (read-only).

## Summary and Completion Checklist

- [ ] All six 102-500 topics exercised.
- [ ] Scripting, cron ordering, journal/time services drilled.
- [ ] Networking client loop and the SUID/security audit done.
- [ ] LPIC-1 complete: both exams' topics covered between Chapters 03–04.
