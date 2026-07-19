# Chapter 07: DNS, NTP, Web, Database, and Common Server Services

![Lab topology for this chapter: chronyd reports normal time sync, a local caching DNS resolver forwards to public resolvers successfully, and a self-signed TLS virtual host serves lab content over HTTPS. A MariaDB user granted privileges only on one database can see and use that database. As a negative test, the same user attempts to access the MariaDB system database directly; the server returns an access-denied error, confirming the grant is properly scoped to the one application database and does not implicitly extend to server-wide system tables.](../../../diagrams/volume-14-red-hat-enterprise-linux-10/chapter-07-dns-tls-mariadb-scope-topology.svg)

*Figure 7-1. Topology used throughout this chapter's Hands-On Lab: a caching DNS resolver, TLS web virtual host, and scoped MariaDB user, tested against an out-of-scope database access attempt.*

## Learning Objectives

- Configure time synchronization with `chrony` and explain why
  accurate time underpins nearly every other service in this chapter.
- Deploy a caching or authoritative DNS service with BIND and diagnose
  resolution problems from both server and client sides.
- Deploy and secure the Apache HTTP Server, including virtual hosts and
  TLS with `mod_ssl`.
- Install and initialize MariaDB and PostgreSQL, and apply baseline
  database hardening.
- Apply SELinux and firewalld configuration consistently across every
  service in this chapter, reinforcing Chapters 04 and 06.
- Diagnose common server-service failures using service-specific and
  general-purpose tools together.

## Theory and Architecture

The services in this chapter — time, name resolution, web, and
database — are the most commonly deployed workloads on a general-
purpose RHEL 10 server, and they share a recurring pattern this
chapter makes explicit: each service has its own configuration files
and daemon, but every one of them also depends on the identity,
network, firewall, and SELinux foundations built in Chapters 04 and
06. A service that "won't start" or "isn't reachable" is very often
correctly configured at the application layer and blocked at one of
those shared layers instead.

### Time synchronization with chrony

Accurate system time is a quiet prerequisite for correctness
elsewhere: TLS certificate validation fails outside a certificate's
validity window if the clock is wrong, Kerberos authentication (used
by Active Directory integration and IdM) has a strict clock-skew
tolerance, and log correlation across hosts is meaningless without
synchronized clocks. RHEL 10 uses **chrony** (`chronyd`) as its NTP
implementation, preferred over the legacy `ntpd` for faster
convergence after a network interruption and better handling of
systems that are not always powered on (workstations, cloud instances
that pause/resume). `chronyd` polls one or more upstream time sources
defined in `/etc/chrony.conf`, gradually or immediately correcting
the local clock and continuously tracking drift.

### DNS architecture with BIND

DNS resolves names to addresses (and the reverse) and underlies
virtually every other network service's usability. RHEL 10 systems are
DNS **clients** by default — resolution is configured through
NetworkManager-managed `/etc/resolv.conf` — but a RHEL 10 host can also
run **BIND** (`named`) as a DNS server in one of two common roles:

- **Caching/recursive resolver** — answers queries on behalf of local
  clients by querying the wider DNS hierarchy and caching results,
  reducing latency and external query volume for a site.
- **Authoritative server** — serves DNS zone data it owns directly
  (forward zones mapping names to addresses, reverse zones mapping
  addresses to names), the source of truth for a domain rather than a
  cache of someone else's.

A single `named` instance is not usually both recursive-for-everyone
and authoritative-for-the-internet at the same time; production BIND
deployments deliberately scope each role (an internal caching resolver
for client lookups, a separate authoritative pair for a domain a site
owns) to avoid the operational and security complexity of mixing them
on one instance.

### Web services: Apache HTTP Server

**Apache httpd** remains a default, fully supported web server on
RHEL 10, configured primarily through `/etc/httpd/conf/httpd.conf` and
modular drop-ins under `/etc/httpd/conf.d/`. Two concepts matter for
any nontrivial deployment:

- **Virtual hosts** (`<VirtualHost>` blocks) let one `httpd` instance
  serve multiple independent sites, distinguished by hostname
  (name-based) or by IP/port (IP-based), each with its own document
  root and logging.
- **TLS termination** via `mod_ssl` protects data in transit; a
  certificate and private key are bound to a virtual host, and modern
  deployments increasingly automate certificate issuance and renewal
  rather than managing certificates by hand.

`nginx` is available as an alternative or complementary web/reverse-
proxy server on RHEL 10 and is common in front of application servers,
but Apache remains the chapter's primary example because of its
tighter default integration with RHEL's SELinux policy and
documentation.

### Database services: MariaDB and PostgreSQL

RHEL 10's AppStream repository offers both **MariaDB** (a
MySQL-compatible relational database, RHEL's traditional default) and
**PostgreSQL** (an advanced open-source relational database with
strong standards compliance and extensibility) as module streams,
letting an environment pin a specific major version independent of the
base OS release. Both follow the same operational shape: install the
server package, initialize the data directory, enable and start the
service, then run each engine's respective hardening routine
(`mysql_secure_installation` for MariaDB; PostgreSQL's `pg_hba.conf`
authentication configuration serves the equivalent purpose) before
allowing any non-local connection.

### The shared foundation: SELinux and firewalld per service

Every service in this chapter ships SELinux policy scoped to its own
type (`httpd_t`, `named_t`, `mysqld_t`, `postgresql_t`) and its own set
of relevant booleans and port labels, and every one of them needs an
explicit `firewalld` allow rule — neither is optional, and neither
substitutes for the other. A new listening port that is not already
covered by a service's default SELinux port type must be added with
`semanage port`, and a service moved to a nonstandard TCP/UDP port must
have both its SELinux port label and its firewall rule updated
together, or the service will fail in ways that look identical to a
misconfigured application.

## Design Considerations

- **Internal NTP hierarchy.** Rather than pointing every host directly
  at external NTP servers, designate a small number of internal
  `chronyd` servers that synchronize from external sources and serve
  the rest of the fleet — this reduces external dependency, improves
  consistency, and is the standard pattern for regulated or
  air-gapped environments.
- **Recursive vs. authoritative DNS separation.** Keep an internal
  caching resolver serving client lookups architecturally separate
  from any authoritative zone a site publishes; conflating the two
  increases both the operational blast radius of a misconfiguration
  and the attack surface exposed to arbitrary client queries.
  Internal-only recursive resolvers should never be reachable from
  the public internet.
- **Virtual host and TLS certificate lifecycle.** Decide whether
  certificates are issued and renewed manually, via an internal CA, or
  via an automated protocol (ACME/Let's Encrypt-style); manual
  certificate management does not scale past a handful of sites and is
  a common source of expiry-driven outages.
- **Database version pinning via module streams.** Treat the chosen
  MariaDB or PostgreSQL module stream the same way [Chapter 01](01-installation-subscriptions-repositories-and-cockpit.md) treats
  any module stream — a deliberate, fleet-wide decision, because
  switching streams later is disruptive (typically requiring backup,
  removal, and reinstall against the new stream).
- **Local vs. remote database access.** Default to local-only
  (`127.0.0.1`) or application-tier-scoped database access; a database
  listening on all interfaces with a broad firewall allow rule is a
  disproportionate risk relative to the convenience gained, especially
  for engines where authentication defaults are permissive out of the
  box until explicitly hardened.
- **Consistent per-service hardening discipline.** Apply the same
  three-part checklist to every server service added to a host:
  correct SELinux context/booleans/ports, a scoped firewalld rule, and
  the service's own authentication/TLS hardening — treating this as a
  repeatable pattern rather than re-deriving it per service reduces
  the chance of skipping a layer.

## Implementation and Automation

### 1. Time synchronization with chrony

```bash
dnf install -y chrony

# Configure upstream time sources
sed -i '/^pool /d' /etc/chrony.conf
cat >> /etc/chrony.conf <<'EOF'
pool time.example.com iburst
EOF

systemctl enable --now chronyd

# Verify synchronization state and source quality
chronyc tracking
chronyc sources -v
```

### 2. DNS with BIND: a caching resolver

```bash
dnf install -y bind bind-utils

cat > /etc/named.conf <<'EOF'
options {
    listen-on port 53 { 127.0.0.1; 10.10.10.5; };
    allow-query     { localhost; 10.10.10.0/24; };
    recursion yes;
    forwarders { 8.8.8.8; 9.9.9.9; };
    dnssec-validation yes;
};
EOF

named-checkconf
systemctl enable --now named

firewall-cmd --add-service=dns --permanent
firewall-cmd --reload

# Client-side query test
dig @10.10.10.5 example.com
```

### 3. DNS with BIND: a minimal authoritative zone

```bash
cat >> /etc/named.conf <<'EOF'
zone "lab.example.com" IN {
    type master;
    file "/var/named/lab.example.com.zone";
};
EOF

cat > /var/named/lab.example.com.zone <<'EOF'
$TTL 3600
@   IN SOA  ns1.lab.example.com. admin.lab.example.com. (
        2026071801 ; serial
        3600       ; refresh
        900        ; retry
        604800     ; expire
        3600 )     ; minimum
    IN NS   ns1.lab.example.com.
ns1 IN A    10.10.10.5
www IN A    10.10.10.20
EOF

chgrp named /var/named/lab.example.com.zone
named-checkzone lab.example.com /var/named/lab.example.com.zone
systemctl restart named
dig @10.10.10.5 www.lab.example.com
```

### 4. Apache HTTP Server with a virtual host and TLS

```bash
dnf install -y httpd mod_ssl

mkdir -p /var/www/vhosts/app1/html
echo "<h1>app1</h1>" > /var/www/vhosts/app1/html/index.html
restorecon -Rv /var/www/vhosts

cat > /etc/httpd/conf.d/app1.conf <<'EOF'
<VirtualHost *:80>
    ServerName app1.example.com
    DocumentRoot /var/www/vhosts/app1/html
    ErrorLog /var/log/httpd/app1-error.log
    CustomLog /var/log/httpd/app1-access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName app1.example.com
    DocumentRoot /var/www/vhosts/app1/html
    SSLEngine on
    SSLCertificateFile /etc/pki/tls/certs/app1.crt
    SSLCertificateKeyFile /etc/pki/tls/private/app1.key
</VirtualHost>
EOF

httpd -t
systemctl enable --now httpd

firewall-cmd --add-service=http --add-service=https --permanent
firewall-cmd --reload

# Allow outbound connections from httpd if the app is a reverse proxy/backend client
setsebool -P httpd_can_network_connect on
```

### 5. MariaDB installation and hardening

```bash
dnf module list mariadb
dnf module enable -y mariadb:10.11
dnf install -y mariadb-server

systemctl enable --now mariadb
mysql_secure_installation

firewall-cmd --add-service=mysql --permanent
firewall-cmd --reload

# Create an application database and a scoped user
mysql -u root -p <<'EOF'
CREATE DATABASE appdb CHARACTER SET utf8mb4;
CREATE USER 'appuser'@'10.10.10.%' IDENTIFIED BY 'ChangeMe!23';
GRANT ALL PRIVILEGES ON appdb.* TO 'appuser'@'10.10.10.%';
FLUSH PRIVILEGES;
EOF
```

### 6. PostgreSQL installation and baseline hardening

```bash
dnf module list postgresql
dnf module enable -y postgresql:16
dnf install -y postgresql-server

postgresql-setup --initdb
systemctl enable --now postgresql

# Restrict authentication to the application subnet, using scram-sha-256
sed -i '/^host/d' /var/lib/pgsql/data/pg_hba.conf
echo "host  appdb  appuser  10.10.10.0/24  scram-sha-256" >> /var/lib/pgsql/data/pg_hba.conf
sed -i "s/^#listen_addresses.*/listen_addresses = '10.10.10.5'/" /var/lib/pgsql/data/postgresql.conf
systemctl restart postgresql

firewall-cmd --add-service=postgresql --permanent
firewall-cmd --reload
```

### 7. Nonstandard ports: SELinux and firewalld together

```bash
# Move a service to a nonstandard port (example: httpd on 8443)
semanage port -a -t http_port_t -p tcp 8443
firewall-cmd --add-port=8443/tcp --permanent
firewall-cmd --reload
```

## Validation and Troubleshooting

- **Confirm time is actually synchronized.** `chronyc tracking` shows
  the current offset and whether the system considers itself
  synchronized (`Leap status: Normal`); a service that depends on
  strict clock accuracy (Kerberos, certificate validation) failing
  intermittently is worth checking here first, before assuming an
  application bug.
- **Diagnose DNS resolution failures at the correct layer.** `dig
  @<server> <name>` tests the server directly, bypassing client
  resolver configuration; `dig <name>` (no `@server`) tests what the
  client actually resolves through `/etc/resolv.conf`; a mismatch
  between the two isolates whether the problem is the DNS server or
  the client's configured resolver.
- **Diagnose an httpd virtual host serving the wrong content or
  failing to start.** `httpd -t` validates configuration syntax before
  a restart risks downtime; `apachectl -S` shows how virtual hosts are
  actually matched, which is the fastest way to catch a `ServerName`
  typo or a missing `NameVirtualHost`-equivalent binding; check
  `journalctl -u httpd` and the per-vhost error log together.
- **Diagnose a database that starts but rejects application
  connections.** Confirm the service is listening on the intended
  interface (`ss -tlnp | grep -E '3306|5432'`), confirm the firewall
  rule is active, then confirm the database's own authentication
  configuration (MariaDB grants; PostgreSQL's `pg_hba.conf`) — a
  connection refused error and an authentication-denied error point to
  different layers and should not be treated interchangeably.
- **Diagnose an SELinux-caused service failure that looks like a
  configuration error.** Any of these services failing only when
  moved to a nonstandard port, nonstandard content path, or
  nonstandard data directory is a strong signal to check `ausearch -m
  avc -ts recent` before re-reading the application's own
  configuration file again.
- **Common failure: firewall rule added but not reloaded, or added
  without `--permanent`.** A service that is reachable immediately
  after `firewall-cmd --add-service=...` but unreachable after the
  next reboot is almost always this — confirm with `firewall-cmd
  --list-all` after a `--reload`, not only immediately after the
  `--add-service` command.
- **Common failure: forgetting to enable the SQL module stream before
  installing.** Installing a database package without first running
  `dnf module enable` silently installs the module's default stream,
  which may not match the version a fleet standardized on.

## Security and Best Practices

- Point every host at an internal, authenticated NTP hierarchy rather
  than arbitrary public servers, and monitor for clock drift as an
  operational signal, not only a compliance checkbox.
- Restrict a recursive DNS resolver's `allow-query` to trusted internal
  networks; an open recursive resolver reachable from the internet is
  a known vector for DNS amplification abuse.
- Enable DNSSEC validation (`dnssec-validation yes`) on recursive
  resolvers, and sign any authoritative zone a site is directly
  responsible for once the domain's parent zone supports it.
- Terminate TLS on every public-facing web virtual host, redirect
  plaintext HTTP to HTTPS, and track certificate expiry with
  automated alerting rather than a calendar reminder.
- Run `mysql_secure_installation` (MariaDB) and lock down
  `pg_hba.conf` (PostgreSQL) immediately after initialization — both
  engines ship defaults intended for initial setup, not production
  exposure.
- Scope database network access to the specific application subnet or
  host, never `0.0.0.0`/`%` without a network-layer control also
  restricting reachability, and require encrypted client connections
  for any database reachable outside `localhost`.
- Apply the SELinux-plus-firewalld pattern to every service in this
  chapter without exception, including internal-only services — MAC
  and network-layer controls are not redundant with each other and
  both meaningfully reduce blast radius.

## References and Knowledge Checks

**References**

- [`chrony.conf(5)`, `chronyc(1)` man pages.](https://chrony-project.org/doc/4.0/chrony.conf.html)
- [BIND 9 Administrator Reference Manual; `named.conf(5)`, `dig(1)` man
  pages.](https://bind9.readthedocs.io/)
- [Apache HTTP Server documentation](https://httpd.apache.org/docs/) — virtual hosts and `mod_ssl`
  configuration.
- [MariaDB Server documentation; `mysql_secure_installation(1)`.](https://mariadb.com/kb/en/documentation/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/) — `pg_hba.conf` authentication
  configuration.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — RHEL 10
  baseline referenced throughout this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. Why should an internal recursive DNS resolver and a
   publicly reachable authoritative zone generally not be served by
   the same `named` instance?
2. What two independent things must both be true for a service moved
   to a nonstandard port to work correctly on a RHEL 10 host with
   SELinux enforcing and `firewalld` active?
3. Why does `chronyc tracking` matter for troubleshooting a Kerberos
   or TLS-related authentication failure that seems unrelated to time?
4. What is the practical difference in what `dig @<server> <name>` and
   plain `dig <name>` each test?

## Hands-On Lab

**Objective:** Stand up an internal caching DNS resolver, a
TLS-enabled Apache virtual host, and a MariaDB instance serving a
scoped application user, wiring SELinux and firewalld correctly at
every step.

**Prerequisites**

- A RHEL 10 host or VM with root/sudo access and outbound internet
  access (for `chronyd` and BIND forwarding).
- `openssl` available for generating a self-signed lab certificate.

**Steps**

1. Configure and verify time synchronization:

   ```bash
   sudo dnf install -y chrony
   sudo systemctl enable --now chronyd
   chronyc tracking | grep "Leap status"
   ```

   **Expected result:** `Leap status: Normal`.

2. Install and configure BIND as a caching resolver:

   ```bash
   sudo dnf install -y bind bind-utils
   sudo tee /etc/named.conf <<'EOF'
   options {
       listen-on port 53 { 127.0.0.1; };
       allow-query     { localhost; };
       recursion yes;
       forwarders { 8.8.8.8; 9.9.9.9; };
       dnssec-validation yes;
   };
   EOF
   sudo named-checkconf
   sudo systemctl enable --now named
   sudo firewall-cmd --add-service=dns --permanent
   sudo firewall-cmd --reload
   dig @127.0.0.1 redhat.com +short
   ```

   **Expected result:** `dig` returns at least one IP address.

3. Install Apache, create a self-signed certificate, and configure a
   TLS virtual host:

   ```bash
   sudo dnf install -y httpd mod_ssl
   sudo mkdir -p /var/www/vhosts/lab/html
   echo "<h1>lab vhost</h1>" | sudo tee /var/www/vhosts/lab/html/index.html
   sudo restorecon -Rv /var/www/vhosts

   sudo openssl req -x509 -nodes -days 30 -newkey rsa:2048 \
     -keyout /etc/pki/tls/private/lab.key \
     -out /etc/pki/tls/certs/lab.crt \
     -subj "/CN=lab.example.com"

   sudo tee /etc/httpd/conf.d/lab.conf <<'EOF'
   <VirtualHost *:443>
       ServerName lab.example.com
       DocumentRoot /var/www/vhosts/lab/html
       SSLEngine on
       SSLCertificateFile /etc/pki/tls/certs/lab.crt
       SSLCertificateKeyFile /etc/pki/tls/private/lab.key
   </VirtualHost>
   EOF

   sudo httpd -t
   sudo systemctl enable --now httpd
   sudo firewall-cmd --add-service=https --permanent
   sudo firewall-cmd --reload
   curl -sk https://localhost/ -H "Host: lab.example.com"
   ```

   **Expected result:** the curl request returns `<h1>lab vhost</h1>`.

4. Install MariaDB and create a scoped application user:

   ```bash
   sudo dnf module enable -y mariadb:10.11
   sudo dnf install -y mariadb-server
   sudo systemctl enable --now mariadb

   sudo mysql <<'EOF'
   CREATE DATABASE labdb CHARACTER SET utf8mb4;
   CREATE USER 'labuser'@'localhost' IDENTIFIED BY 'LabPass!234';
   GRANT ALL PRIVILEGES ON labdb.* TO 'labuser'@'localhost';
   FLUSH PRIVILEGES;
   EOF

   mysql -u labuser -pLabPass!234 -e "SHOW DATABASES;" | grep labdb
   ```

   **Expected result:** `labdb` appears in the output, confirming the
   scoped user can authenticate and see its own database.

5. **Negative test:** confirm the scoped database user cannot see or
   access an unrelated database:

   ```bash
   mysql -u labuser -pLabPass!234 -e "USE mysql; SHOW TABLES;" \
     2>&1 | grep -i "denied" && echo "Access correctly denied"
   ```

   **Expected result:** MariaDB returns an access-denied error for the
   `mysql` system database, confirming the grant is properly scoped.

6. **Cleanup:**

   ```bash
   sudo mysql -e "DROP DATABASE labdb; DROP USER 'labuser'@'localhost';"
   sudo rm -f /etc/httpd/conf.d/lab.conf
   sudo rm -f /etc/pki/tls/private/lab.key /etc/pki/tls/certs/lab.crt
   sudo rm -rf /var/www/vhosts/lab
   sudo systemctl restart httpd
   sudo firewall-cmd --remove-service=https --permanent
   sudo firewall-cmd --remove-service=dns --permanent
   sudo firewall-cmd --reload
   ```

## Summary and Completion Checklist

Time synchronization, DNS, web, and database services form the core of
most general-purpose RHEL 10 server deployments, and each depends on
the identity, network, firewall, and SELinux foundations from earlier
chapters as much as it depends on its own configuration files.
Diagnosing a failure in any of these services means checking both the
service-specific layer and the shared layers — SELinux context and
booleans, firewalld rules, and correct network/time configuration —
rather than assuming the fault is isolated to the application.

- [ ] Can configure and verify `chrony` time synchronization.
- [ ] Can deploy a caching and a minimal authoritative BIND DNS
      service, and diagnose resolution from both server and client
      sides.
- [ ] Can configure an Apache virtual host with TLS termination.
- [ ] Can install and apply baseline hardening to MariaDB and
      PostgreSQL.
- [ ] Can correctly pair SELinux port/context changes with matching
      firewalld rules for a relocated or nonstandard service.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
