# Chapter 06: LPIC-2 — Exam 202 (202-450)

## Learning Objectives

- Cover exam 202-450's six topics with a walkthrough lab each.
- Drill DNS, web services, file sharing, network client management, e-mail, and system security.
- Work from the published v4.5 objectives.

## The exam in brief

**Exam:** 202-450 (objectives v4.5), LPIC-2's second exam. Six topics: **207 Domain Name Server**, **208 Web Services**, **209 File Sharing**, **210 Network Client Management**, **211 E-Mail Services**, **212 System Security**. Passing 201-450 and 202-450 (with active LPIC-1) earns LPIC-2.

## Hands-On Lab

A Linux VM; services installed per-lab and removed after. **Cost:** none.

### Lab 6.1 — DNS with BIND (Topic 207)

**Objective:** Serve an authoritative zone and query it.

```bash
sudo apt-get install -y -qq bind9 dnsutils
sudo tee /etc/bind/db.lab.test >/dev/null <<'EOF'
$TTL 300
@ IN SOA ns.lab.test. root.lab.test. (1 3600 900 604800 300)
@ IN NS ns.lab.test.
ns IN A 127.0.0.1
www IN A 192.0.2.80
EOF
echo 'zone "lab.test" { type master; file "/etc/bind/db.lab.test"; };' | sudo tee -a /etc/bind/named.conf.local >/dev/null
sudo named-checkzone lab.test /etc/bind/db.lab.test && sudo systemctl restart bind9
dig +short www.lab.test @127.0.0.1
```

**Expected result:** `named-checkzone` reporting `OK` and `dig` answering `192.0.2.80` — an authoritative master zone served: SOA/NS/A records, zone checking, and querying are Topic 207's core (plus recursion control, forwarders, and basic DNSSEC awareness).

**Negative test:** Bump the zone serial *down* and reload — secondaries would never transfer; serial discipline is the classic DNS operations question.

**Cleanup:** Remove the zone lines and `sudo apt-get remove -y bind9`.

### Lab 6.2 — Web services with Apache (Topic 208)

**Objective:** Serve a virtual host and read the controls.

```bash
sudo apt-get install -y -qq apache2
echo "lab vhost" | sudo tee /var/www/html/index.html >/dev/null
curl -s http://127.0.0.1/ | head -1
apachectl -M 2>/dev/null | grep -c ssl || echo "ssl module not loaded"
echo "vhost grammar: <VirtualHost *:80> ServerName / DocumentRoot; a2ensite/a2enmod; proxy: nginx/squid awareness"
```

**Expected result:** The page served (`lab vhost`), module inventory checked — Topic 208: Apache configuration (vhosts, modules, authentication), HTTPS/SSL configuration, plus nginx as reverse proxy and squid as caching proxy at awareness level.

**Negative test:** Enable a vhost without `ServerName` on a name-based setup — the wrong site answers; name-based vhosting resolves by Host header, the mechanism the exam tests.

**Cleanup:** `sudo apt-get remove -y apache2`.

### Lab 6.3 — File sharing (Topic 209)

**Objective:** Export the same directory both ways: Samba and NFS.

```bash
sudo apt-get install -y -qq samba nfs-kernel-server
sudo mkdir -p /srv/share && echo data | sudo tee /srv/share/f.txt >/dev/null
printf '[labshare]\n path=/srv/share\n read only = yes\n' | sudo tee -a /etc/samba/smb.conf >/dev/null
testparm -s 2>/dev/null | grep -A2 labshare | head -3
echo "/srv/share 127.0.0.1(ro)" | sudo tee -a /etc/exports >/dev/null && sudo exportfs -ra && sudo exportfs -v | head -2
```

**Expected result:** `testparm` validating the Samba share and `exportfs -v` listing the NFS export — the same data offered over SMB (Windows-world) and NFS (UNIX-world), with each stack's config file, validator, and daemon: Topic 209 entire.

**Negative test:** An NFS export without the host restriction (`/srv/share *(rw)`) — world-writable network storage; the exam expects you to flinch.

**Cleanup:** Remove the share/export lines; `sudo apt-get remove -y samba nfs-kernel-server`.

### Lab 6.4 — Network client management (Topic 210)

**Objective:** Model DHCP and PAM/LDAP-backed login plumbing.

```bash
sudo apt-get install -y -qq isc-dhcp-server 2>/dev/null || true
cat <<'EOF' | sudo tee /tmp/dhcpd-lab.conf >/dev/null
subnet 192.0.2.0 netmask 255.255.255.0 { range 192.0.2.100 192.0.2.150; option routers 192.0.2.1; }
EOF
dhcpd -t -cf /tmp/dhcpd-lab.conf 2>&1 | tail -1
grep -m2 "^auth" /etc/pam.d/sshd 2>/dev/null || grep -m2 auth /etc/pam.d/* 2>/dev/null | head -2
```

**Expected result:** `dhcpd -t` validating the scope config, and real PAM `auth` lines read from a service file — Topic 210: DHCP scopes/leases, PAM's module stacks (`auth/account/password/session`), and LDAP client integration (nsswitch + pam_ldap/sssd) at configuration level.

**Negative test:** Overlapping DHCP ranges in two subnets of one scope file — `dhcpd -t` catches it; validating before restarting is the operational habit.

**Cleanup:** `rm /tmp/dhcpd-lab.conf; sudo apt-get remove -y isc-dhcp-server`.

### Lab 6.5 — E-mail services (Topic 211)

**Objective:** Trace mail flow through a local MTA.

```bash
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq postfix bsd-mailx 2>/dev/null
echo "lab mail" | mail -s "lpic2" $(whoami) 2>/dev/null
sleep 2; postqueue -p | tail -2
tail -3 /var/mail/$(whoami) 2>/dev/null || sudo tail -3 /var/log/mail.log
echo "aliases: /etc/aliases + newaliases ; ~/.forward ; delivery: procmail/sieve awareness"
```

**Expected result:** A message submitted to Postfix, the queue empty (delivered) or showing the item, and the message (or its log line) on disk — Topic 211: MTA operation (Postfix), aliases and forwarding, queues, and delivery agents at awareness level.

**Negative test:** Alias loop (`a: b` and `b: a` in `/etc/aliases`) — mail bounces with a loop error; aliases are a graph, and loops are the classic misconfiguration.

**Cleanup:** `sudo apt-get remove -y postfix bsd-mailx`.

### Lab 6.6 — System security (Topic 212)

**Objective:** Build the router/firewall + secure shell layer of LPIC-2.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 192.0.2.0/24 -o lo -j MASQUERADE 2>/dev/null && sudo iptables -t nat -L POSTROUTING -n | tail -1
sudo iptables -t nat -D POSTROUTING -s 192.0.2.0/24 -o lo -j MASQUERADE 2>/dev/null
ssh-keygen -t ed25519 -N "" -f labkey -q && ssh-keygen -lf labkey.pub
echo "fail2ban / openvpn / security advisories (CVE feeds) round out the topic"
```

**Expected result:** Forwarding enabled, a NAT masquerade rule added and removed, and an ed25519 keypair generated with its fingerprint shown — Topic 212: packet filtering and NAT (iptables/nftables), OpenSSH server hardening and keys, VPN awareness (OpenVPN), and staying on top of advisories.

**Negative test:** Enable forwarding without any filter policy — the host routes everything; forwarding plus default-accept is the accidental-router misconfiguration the exam wants you to catch.

**Cleanup:** `rm labkey labkey.pub; sudo sysctl -w net.ipv4.ip_forward=0`.

## Summary and Completion Checklist

- [ ] All six 202-450 topics exercised with real services.
- [ ] Zone served and validated; vhost served; share exported both ways.
- [ ] DHCP validated, PAM read, mail traced, NAT + SSH keys drilled.
- [ ] LPIC-2 complete: both exams' topics covered between Chapters 05–06.
