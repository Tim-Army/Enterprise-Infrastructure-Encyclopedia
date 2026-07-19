# Chapter 07: DNS, NTP, DHCP, Web, Database, and Common Server Services

![Flow diagram showing an authoritative BIND9 zone resolving a defined hostname to a working Nginx virtual host end to end, and returning an authoritative NXDOMAIN for a name that was never defined in the zone.](../../diagrams/volume-21-ubuntu-server-cloud-26-04-lts/chapter-07-bind9-nginx-nxdomain-flow.svg)

*Figure 7-1. The DNS-to-HTTP resolution chain exercised in this chapter's lab, including the authoritative NXDOMAIN negative test.*

## Learning Objectives

- Deploy an authoritative BIND9 zone and understand `systemd-resolved`'s
  role as the client-side resolution stub.
- Configure time synchronization with `chrony` and verify NTP health.
- Stand up DHCP service with Kea, the modern successor to ISC DHCP.
- Deploy Apache2 and Nginx virtual hosts with Let's Encrypt TLS.
- Install and perform first-run hardening on MySQL/MariaDB and
  PostgreSQL.

## Theory and Architecture

Ubuntu Server's role as a general-purpose infrastructure platform means
most deployments eventually run at least one of the core network and
application services covered in this chapter. Each has an Ubuntu-
specific packaging or default-tooling detail worth knowing before
deployment.

### DNS: BIND9 and systemd-resolved

Ubuntu Server runs two DNS-adjacent components that are easy to
conflate:

- **BIND9** (`bind9` package) is a full authoritative and/or recursive
  DNS *server*, deployed when the host itself needs to serve zone data
  to other hosts.
- **systemd-resolved** is the client-side resolution stub present on
  every Ubuntu host by default, managing `/etc/resolv.conf` (typically
  a symlink to `/run/systemd/resolve/stub-resolv.conf`, pointing at
  `127.0.0.53`), handling DNS caching, and integrating per-interface
  DNS servers assigned via Netplan ([Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)).

A host can run both: `systemd-resolved` resolves the *host's own*
lookups, while BIND9, if installed, answers queries *from other hosts*
as an authoritative or recursive server — they are not alternatives to
each other for the same job.

### NTP: chrony

**chrony** is the default NTP implementation on Ubuntu Server,
replacing the legacy `ntpd` most administrators may still associate
with Linux time sync. chrony handles intermittent network connectivity
and virtualized clock drift better than `ntpd`, converges faster after
a large offset, and exposes `chronyc` for live monitoring and
diagnostics — relevant everywhere Kerberos (Active Directory
integration), TLS certificate validation, or distributed-log
correlation depends on host clocks agreeing closely.

### DHCP: Kea

ISC deprecated `isc-dhcp-server` (end of life), and Ubuntu's supported
DHCP server is now **Kea** (`kea-dhcp4-server`/`kea-dhcp6-server`),
also from ISC. Kea uses JSON configuration rather than the older
`dhcpd.conf` syntax, exposes a REST control-agent API for
automation-driven lease and reservation management, and supports
high-availability lease synchronization between paired servers —
capabilities the legacy server never had natively.

### Web services: Apache2 and Nginx

Both **Apache2** (`apache2`) and **Nginx** (`nginx`) are first-class
citizens in Ubuntu's repositories; the practical distinction is
architectural rather than one being simply "better":

| | Apache2 | Nginx |
| --- | --- | --- |
| Concurrency model | Process/thread-per-connection (worker MPM) or event-driven (event MPM) | Event-driven, async, single-digit worker processes |
| Configuration style | `.htaccess` per-directory overrides supported | Centralized config only, no per-directory override |
| Typical strength | Dynamic content via modules (`mod_php`, etc.), flexible per-directory config | High-concurrency static/proxy workloads, reverse proxy, TLS termination |

Both integrate with **Certbot** for automated Let's Encrypt certificate
issuance and renewal via the ACME protocol.

### Database services: MySQL/MariaDB and PostgreSQL

Ubuntu's repositories carry **MariaDB** (the default MySQL-compatible
server pulled in by the `mysql-server` transitional metapackage on
current Ubuntu Server releases) and **PostgreSQL**. Both ship with a
first-run hardening step Ubuntu strongly expects an administrator to
run explicitly (`mysql_secure_installation` for MariaDB/MySQL;
PostgreSQL's equivalent is largely `pg_hba.conf` authentication method
review) rather than shipping a security posture safe enough to skip
that step.

## Design Considerations

- **When to run an internal DNS server at all.** A single-site
  environment relying entirely on a cloud provider's or ISP's DNS may
  not need BIND9 at all; internal DNS becomes necessary once private
  hostnames, split-horizon resolution, or service discovery for
  internal-only names are required.
- **chrony source selection.** Point production hosts at a small,
  authoritative set of internal NTP sources (themselves synced to
  multiple external strata) rather than every host reaching out to
  public NTP pools directly — this reduces external dependency, external
  query volume, and gives operations a single place to monitor time
  health.
- **Kea vs. a cloud provider's native DHCP.** On-premises and
  private-cloud environments generally need Kea (or an equivalent);
  most public cloud deployments never touch DHCP server configuration
  directly, since the platform provides it — deploy Kea only where the
  environment genuinely needs to run it.
- **Apache2 vs. Nginx selection.** Choose based on the actual workload:
  Nginx as a reverse proxy/TLS terminator in front of application
  servers is extremely common regardless of what serves the dynamic
  content behind it; Apache2 remains a strong choice where
  `.htaccess`-style per-directory configuration or specific legacy
  module dependencies are required.
- **Database sizing and separation.** Decide early whether the database
  runs on the same host as the application (simpler, acceptable for
  small/non-critical workloads) or a dedicated host/managed service
  (better isolation, independent scaling and patching cadence,
  generally the right default for anything production-critical).
- **Certificate renewal automation.** Certbot's systemd timer
  (installed automatically with the package) handles routine renewal;
  design any custom TLS automation (internal CA integration, wildcard
  DNS-01 challenges) with the same "unattended, monitored, alerting on
  failure" bar rather than a renewal process that depends on someone
  remembering.

## Implementation and Automation

### 1. BIND9 authoritative zone

```bash
sudo apt install -y bind9 bind9utils

# Define the zone in named.conf.local
sudo tee -a /etc/bind/named.conf.local <<'EOF'
zone "lab.example.com" {
    type master;
    file "/etc/bind/db.lab.example.com";
    allow-transfer { 10.20.30.6; };
};
EOF

sudo tee /etc/bind/db.lab.example.com <<'EOF'
$TTL    604800
@       IN      SOA     ns1.lab.example.com. admin.lab.example.com. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns1.lab.example.com.
ns1     IN      A       10.20.30.5
app01   IN      A       10.20.30.15
EOF

sudo named-checkconf
sudo named-checkzone lab.example.com /etc/bind/db.lab.example.com
sudo systemctl enable --now bind9
```

### 2. systemd-resolved client status

```bash
resolvectl status
resolvectl query app01.lab.example.com

# Confirm which DNS servers apply to a specific interface (set via Netplan)
resolvectl status ens160
```

### 3. chrony time synchronization

```bash
sudo apt install -y chrony

sudo tee -a /etc/chrony/chrony.conf <<'EOF'
pool ntp.internal.example.com iburst
EOF
sudo systemctl restart chrony

# Verify synchronization state and source quality
chronyc tracking
chronyc sources -v
timedatectl status
```

### 4. Kea DHCP server

```bash
sudo apt install -y kea-dhcp4-server

sudo tee /etc/kea/kea-dhcp4.conf <<'EOF'
{
  "Dhcp4": {
    "interfaces-config": { "interfaces": [ "ens192" ] },
    "lease-database": { "type": "memfile", "persist": true },
    "subnet4": [
      {
        "subnet": "10.20.50.0/24",
        "pools": [ { "pool": "10.20.50.100 - 10.20.50.200" } ],
        "option-data": [
          { "name": "routers", "data": "10.20.50.1" },
          { "name": "domain-name-servers", "data": "10.20.30.5" }
        ]
      }
    ]
  }
}
EOF

sudo kea-dhcp4 -t /etc/kea/kea-dhcp4.conf   # validate before starting
sudo systemctl enable --now kea-dhcp4-server
```

### 5. Nginx virtual host with Let's Encrypt TLS

```bash
sudo apt install -y nginx

sudo tee /etc/nginx/sites-available/app01.lab.example.com <<'EOF'
server {
    listen 80;
    server_name app01.lab.example.com;
    root /var/www/app01;
    index index.html;
}
EOF
sudo ln -s /etc/nginx/sites-available/app01.lab.example.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d app01.lab.example.com --non-interactive --agree-tos -m ops@example.com

# Confirm the automatic renewal timer
systemctl list-timers | grep certbot
sudo certbot renew --dry-run
```

### 6. Database installation and first-run hardening

```bash
# MariaDB (MySQL-compatible)
sudo apt install -y mariadb-server
sudo mysql_secure_installation
sudo mysql -e "CREATE DATABASE appdb; \
  CREATE USER 'app'@'localhost' IDENTIFIED BY 'ChangeMeStrongPW!'; \
  GRANT ALL PRIVILEGES ON appdb.* TO 'app'@'localhost'; FLUSH PRIVILEGES;"

# PostgreSQL
sudo apt install -y postgresql
sudo -u postgres psql -c "CREATE DATABASE appdb;"
sudo -u postgres psql -c "CREATE USER app WITH PASSWORD 'ChangeMeStrongPW!';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE appdb TO app;"

# Review PostgreSQL's authentication method policy
sudo grep -v '^#' /etc/postgresql/*/main/pg_hba.conf | grep -v '^$'
```

## Validation and Troubleshooting

- **A BIND9 zone loads but queries fail.** `named-checkzone` catches
  syntax errors before reload; `dig @localhost app01.lab.example.com`
  from the server itself isolates whether the problem is the zone data
  or client-side reachability/firewalling ([Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)).
- **`systemd-resolved` and BIND9 seem to conflict on port 53.**
  `systemd-resolved`'s actual listener is `127.0.0.53:53`
  (the stub), not the host's real addresses, so BIND9 binding to the
  host's real interface addresses does not normally conflict; confirm
  with `sudo ss -tulnp | grep :53` if in doubt.
- **`chronyc tracking` shows a large offset that never converges.**
  Check `chronyc sources -v` for a source flagged as unreachable or
  falseticker; a firewall blocking UDP/123 outbound to the configured
  NTP source is a common cause ([Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)).
- **Kea fails to start.** `kea-dhcp4 -t <config>` validates JSON syntax
  and semantics before ever touching `systemctl`; `journalctl -u
  kea-dhcp4-server` surfaces interface-binding failures, commonly an
  interface name typo against `ip -br link`.
- **Certbot issuance fails.** The HTTP-01 challenge requires port 80
  reachable from the internet to the exact `server_name`; confirm DNS
  resolves correctly first (`dig app01.lab.example.com`) and that
  `ufw`/upstream firewalls ([Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)) allow inbound 80/tcp during
  issuance.
- **A database won't accept a new application's connection.** For
  MariaDB, confirm the grant matches the connecting host exactly
  (`'app'@'localhost'` will not match a TCP connection from a different
  host — use `'app'@'10.20.30.%'` or the specific address); for
  PostgreSQL, confirm `pg_hba.conf` has a matching line for the
  connection's source and authentication method, and that `postgresql.
  conf`'s `listen_addresses` includes the address the client uses.

## Security and Best Practices

- Restrict BIND9 zone transfers (`allow-transfer`) and recursive
  queries (`allow-recursion`/`allow-query`) explicitly; an open
  recursive resolver reachable from the internet is a well-known DDoS
  amplification vector.
- Run `chronyc` monitoring as part of routine health checks — clock
  drift silently breaks TLS certificate validation and Kerberos
  authentication well before it becomes an obvious incident.
- Enable Kea's lease and configuration logging, and pair a production
  Kea deployment with the high-availability hook library rather than a
  single point of failure for address assignment on any network segment
  that can't tolerate an outage.
- Terminate TLS with modern protocol and cipher settings
  (`ssl_protocols TLSv1.2 TLSv1.3;` in Nginx, equivalent in Apache2),
  and let Certbot's systemd timer handle renewal rather than a manual,
  easily-forgotten process.
- Always run `mysql_secure_installation` (or the equivalent manual
  steps) immediately after installing MariaDB/MySQL — the unhardened
  defaults include anonymous accounts and a test database.
- Review `pg_hba.conf` on every new PostgreSQL install; `trust`
  authentication (no password required) should never appear on a line
  matching anything but `127.0.0.1`/`::1` from a fully trusted local
  process.
- Scope database network exposure with `ufw` ([Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)) to only the
  application hosts that need it — neither MariaDB's 3306/tcp nor
  PostgreSQL's 5432/tcp should be reachable from a general network
  segment by default.

## References and Knowledge Checks

**References**

- [BIND9 Administrator Reference Manual, ISC.](https://bind9.readthedocs.io/)
- [`chrony.conf(5)`, `chronyc(1)` man pages.](https://chrony-project.org/doc/4.0/chrony.conf.html)
- [Kea Administrator Reference Manual, ISC.](https://kea.readthedocs.io/)
- [Apache2 and Nginx documentation; Certbot documentation
  (`certbot.eff.org`).](https://certbot.eff.org/)
- [MariaDB and PostgreSQL official documentation.](https://mariadb.com/kb/en/documentation/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Ubuntu Server
  26.04 baseline referenced throughout this chapter.

**Knowledge checks**

1. What is the functional difference between BIND9 and
   `systemd-resolved` on the same Ubuntu host, and why do they not
   normally conflict?
2. Why did Ubuntu move from `isc-dhcp-server` to Kea, and what
   capability does Kea provide that the legacy server did not?
3. What specific risk does an open recursive DNS resolver reachable
   from the internet introduce?
4. Why is running `mysql_secure_installation` (or reviewing
   `pg_hba.conf`) treated as a mandatory first-run step rather than
   optional hardening?

## Hands-On Lab

**Objective:** Deploy an authoritative BIND9 zone, verify time
synchronization, and stand up an Nginx virtual host — confirming DNS
resolution end-to-end with a negative test against a nonexistent
record.

**Prerequisites**

- An Ubuntu Server 26.04 LTS VM with `sudo` access, acting as both the
  DNS server and the web server for simplicity.
- A second host or the same VM able to run `dig`/`resolvectl query`
  against it.
- This lab is safe on a disposable VM; it opens no ports to the
  internet and requests no real TLS certificate.

**Steps**

1. Install and configure BIND9 with a lab zone:

   ```bash
   sudo apt install -y bind9 bind9utils dnsutils
   sudo tee -a /etc/bind/named.conf.local <<'EOF'
   zone "lab.internal" {
       type master;
       file "/etc/bind/db.lab.internal";
   };
   EOF
   sudo tee /etc/bind/db.lab.internal <<'EOF'
   $TTL    604800
   @       IN      SOA     ns1.lab.internal. admin.lab.internal. (
                                 1         ; Serial
                            604800         ; Refresh
                             86400         ; Retry
                           2419200         ; Expire
                            604800 )       ; Negative Cache TTL
   @       IN      NS      ns1.lab.internal.
   ns1     IN      A       127.0.0.1
   web01   IN      A       127.0.0.1
   EOF
   sudo named-checkconf
   sudo named-checkzone lab.internal /etc/bind/db.lab.internal
   sudo systemctl enable --now bind9
   ```

2. Query the zone directly against BIND9:

   ```bash
   dig @127.0.0.1 web01.lab.internal +short
   ```

   **Expected result:** returns `127.0.0.1`.

3. Confirm chrony is synchronized:

   ```bash
   sudo apt install -y chrony
   chronyc tracking | grep -E "Reference ID|Leap status"
   timedatectl status | grep "synchronized"
   ```

   **Expected result:** `Leap status` shows `Normal` and
   `System clock synchronized: yes`.

4. Install Nginx and serve a simple virtual host on the lab hostname:

   ```bash
   sudo apt install -y nginx
   sudo mkdir -p /var/www/web01
   echo "<h1>Lab web01</h1>" | sudo tee /var/www/web01/index.html
   sudo tee /etc/nginx/sites-available/web01.lab.internal <<'EOF'
   server {
       listen 80;
       server_name web01.lab.internal;
       root /var/www/web01;
       index index.html;
   }
   EOF
   sudo ln -s /etc/nginx/sites-available/web01.lab.internal /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```

5. Confirm end-to-end resolution and retrieval using the lab DNS zone:

   ```bash
   curl -H "Host: web01.lab.internal" http://127.0.0.1/
   ```

   **Expected result:** returns the `<h1>Lab web01</h1>` content,
   confirming the virtual host responds correctly for the configured
   name.

6. **Negative test:** query a name that was never defined in the zone:

   ```bash
   dig @127.0.0.1 doesnotexist.lab.internal +short
   dig @127.0.0.1 doesnotexist.lab.internal | grep -i status
   ```

   **Expected result:** no address is returned, and the status line
   shows `NXDOMAIN`, confirming BIND9 correctly reports an
   authoritative negative answer rather than guessing or forwarding.

7. **Cleanup:**

   ```bash
   sudo systemctl disable --now bind9
   sudo rm -f /etc/bind/db.lab.internal
   sudo sed -i '/zone "lab.internal"/,/};/d' /etc/bind/named.conf.local
   sudo rm -f /etc/nginx/sites-enabled/web01.lab.internal \
              /etc/nginx/sites-available/web01.lab.internal
   sudo rm -rf /var/www/web01
   sudo systemctl reload nginx
   ```

## Summary and Completion Checklist

Ubuntu Server separates client-side DNS resolution
(`systemd-resolved`) from authoritative/recursive DNS service
(BIND9), and replaced the legacy ISC DHCP server with the actively
maintained Kea implementation. chrony provides fast-converging,
virtualization-aware time synchronization. Apache2 and Nginx cover
different web-serving concurrency and configuration models, both
integrating cleanly with Certbot for automated TLS. MariaDB and
PostgreSQL both require an explicit first-run hardening step before
they should be considered production-ready.

- [ ] Can deploy and validate a BIND9 authoritative zone.
- [ ] Can verify time synchronization health with `chronyc`.
- [ ] Can configure and validate a Kea DHCP4 subnet.
- [ ] Can deploy an Nginx (or Apache2) virtual host with automated
      Let's Encrypt TLS.
- [ ] Can install and apply first-run hardening to MariaDB and
      PostgreSQL.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
