# Chapter 02: Ports, Protocols, Services, and Traffic Flows

## Learning Objectives

- Identify the transport protocol, port number, and direction of initiation
  for the services most commonly deployed across Volumes II through XXIII of
  this encyclopedia.
- Distinguish well-known (0–1023), registered (1024–49151), and dynamic/
  ephemeral (49152–65535) port ranges and explain why each range implies a
  different firewall posture.
- Read and construct a traffic-flow description (source, destination,
  port, protocol, direction) sufficient to write a firewall rule or a
  security-group entry without ambiguity.
- Identify which common services still default to a cleartext or otherwise
  deprecated protocol and name the encrypted replacement.
- Use a single consolidated port/service table as the first diagnostic
  reference when a connection fails or a firewall rule must be written.

## Theory and Architecture

Every service in this encyclopedia rides on one of a small number of
transport-layer behaviors, and the behavior — not the vendor — determines
how the service must be firewalled, load-balanced, and troubleshot.

- **TCP (protocol 6)** is connection-oriented: a three-way handshake
  (SYN, SYN-ACK, ACK) establishes state before data flows, and that state
  is what stateful firewalls and connection-tracking tables key on. Most
  management, database, and file-sharing protocols use TCP because they
  need reliable, ordered delivery.
- **UDP (protocol 17)** is connectionless: there is no handshake, no
  guaranteed delivery, and no inherent ordering. DNS queries, NTP, SNMP
  traps, and most VoIP/streaming media use UDP because the application
  layer either tolerates loss or supplies its own reliability (as DNS does
  with retries and TCP fallback for large responses).
- **ICMP (protocol 1 / 58 for ICMPv6)** carries control and diagnostic
  messages — echo request/reply (`ping`), destination unreachable,
  time-exceeded (`traceroute`), and, for IPv6, functions IPv4 handled
  separately (such as Neighbor Discovery). ICMP has no port number; filtering
  policy for it is written by message type and code, not by port.
- **Protocol numbers without ports** — GRE (47), ESP (50), AH (51), and
  OSPF (89) operate directly over IP and are frequently the reason a
  port-only firewall rule set fails to pass a VPN or routing adjacency: there
  is no TCP/UDP port to permit, only an IP protocol number.

Port ranges carry policy meaning. The Internet Assigned Numbers Authority
(IANA) divides the 16-bit port space into three ranges:

| Range | Name | Typical assignment authority | Firewall implication |
| --- | --- | --- | --- |
| 0–1023 | Well-known / system ports | IANA-assigned, historically required root/administrator privilege to bind | Stable, safe to hard-code in a rule; represents most classic services (SSH, DNS, HTTP/S, SMTP) |
| 1024–49151 | Registered ports | IANA-registered by vendors/projects, but not privileged to bind | Common for application and management services (RDP, many databases, orchestration APIs); verify against the vendor's current documentation rather than assuming |
| 49152–65535 | Dynamic / private / ephemeral ports | Not registered; assigned per-connection by the OS as the *source* port of an outbound connection | Never hard-code as a destination in a rule; this is the range a stateful firewall must return traffic to, and the range NAT/PAT rewrites |

A traffic flow is fully described only when five elements are known:
source, destination, port/protocol, direction of session initiation, and
the security zone boundary crossed. Omitting the direction of initiation is
the single most common cause of an unnecessarily broad firewall rule —
"allow TCP/443 between A and B" is not the same statement as "A initiates
TCP/443 to B," and stateful firewalls (Chapter 07) only need the latter.

## Design Considerations

- **Firewall rules should name the service, not just the port.** A rule
  permitting TCP/443 says nothing about which application is expected on
  that port; pair every port-based rule with an application-layer
  expectation (an application identity in a next-generation firewall,
  or at minimum a comment) so that port reuse by an unexpected service is
  detectable.
- **Segment by traffic direction, not just by port.** North-south traffic
  (client-to-server, typically crossing a perimeter or DMZ boundary) and
  east-west traffic (server-to-server, typically inside a data center or
  VPC) warrant different default postures — east-west traffic benefits far
  more from micro-segmentation (Volume V NSX, Volume X) because a single
  compromised host has lateral options only east-west rules can constrain.
- **Prefer the encrypted variant of a legacy protocol whenever one
  exists**, and budget the migration explicitly: Telnet (23) to SSH (22),
  FTP (20/21) to SFTP (22) or FTPS (990), HTTP (80) to HTTPS (443), SNMPv1/
  v2c (161/162, community-string authentication) to SNMPv3 (same ports,
  authenticated/encrypted), and syslog over UDP (514) to syslog over TLS
  (6514, RFC 5425).
- **Plan for NAT/PAT port rewriting when documenting flows that cross a
  NAT boundary.** The source port a downstream device observes is not the
  source port the originating host used; only the destination port
  (for inbound flows) is reliably stable across NAT.
- **Reserve a documented port range for internal service discovery** so
  that ephemeral application ports (custom APIs, sidecar proxies) do not
  collide with registered ports a future off-the-shelf product expects.
- **Treat multicast and broadcast-dependent protocols as a separate design
  category.** VRRP (protocol 112), HSRP (UDP/1985), and mDNS (UDP/5353) do
  not behave like unicast client-server flows and are commonly broken by
  routed boundaries or blocked by default in cloud VPCs/VNets.

## Implementation and Automation

### Consolidated port, protocol, and service reference

Read-only diagnostic ports are marked **RO-adjacent** (the service itself
may be read/write, but the connection is used for monitoring or query in
normal operation); state-changing/administrative ports are marked
**Admin**. Direction shows the typical initiator.

| Service | Port(s) | Protocol | Direction (typical initiator) | Notes |
| --- | --- | --- | --- | --- |
| SSH | 22 | TCP | Client → server | Admin. Encrypted remote shell/SFTP/tunnel; the universal Linux/network-device management protocol in this encyclopedia. |
| Telnet | 23 | TCP | Client → server | Admin, cleartext. Deprecated; retained only for legacy console access on isolated management networks. |
| DNS | 53 | UDP (queries), TCP (zone transfer, large/EDNS0 responses, DNSSEC) | Client/resolver → server | RO-adjacent. TCP fallback is a normal condition, not an error. |
| DHCP | 67 (server), 68 (client) | UDP | Broadcast (client → server initially) | Admin (leases). DHCPv6 uses UDP 546/547. |
| TFTP | 69 | UDP | Client → server | Admin, cleartext, no authentication. Common for network-device firmware/config transfer on isolated management VLANs only. |
| HTTP | 80 | TCP | Client → server | Cleartext; redirect to HTTPS in production. |
| Kerberos | 88 | TCP/UDP | Client → KDC | Admin/authentication. Core to Active Directory (Volume IV) authentication. |
| NTP | 123 | UDP | Client → server (peer associations are bidirectional) | RO-adjacent. See Chapter 03 for stratum design. |
| NetBIOS/SMB (legacy) | 137–139 | TCP/UDP | Client → server | Deprecated in favor of direct SMB over 445 where possible. |
| SNMP | 161 (query), 162 (trap) | UDP | Manager → agent (161); agent → manager (162) | RO-adjacent for polling; use SNMPv3 for authentication/encryption. |
| LDAP | 389 | TCP | Client → directory server | Cleartext unless using StartTLS; prefer 636. |
| LDAPS | 636 | TCP | Client → directory server | Admin/authentication, encrypted. |
| HTTPS | 443 | TCP | Client → server | Encrypted; default for web UIs, REST APIs, most vendor management consoles (vCenter, Panorama, FortiGate, iDRAC, OpenManage Enterprise). |
| SMB | 445 | TCP | Client → server | File sharing; a frequent lateral-movement target and common candidate for east-west segmentation. |
| Syslog | 514 | UDP (traditional), TCP (reliable delivery, RFC 6587) | Sender → collector | RO-adjacent (log shipping). Prefer 6514 (TLS) where the collector supports it. |
| LDAP GC (Global Catalog) | 3268 / 3269 (SSL) | TCP | Client → domain controller | Forest-wide directory queries. |
| RADIUS | 1812 (auth), 1813 (accounting); legacy 1645/1646 | UDP | NAS/device → RADIUS server | Admin/authentication. AAA for network device and VPN logins. |
| TACACS+ | 49 | TCP | Device → TACACS+ server | Admin/authentication, encrypted payload. Preferred over RADIUS for command-level device authorization/accounting (Chapter 01, Chapter 07). |
| SMTP | 25 (relay), 587 (submission), 465 (implicit TLS) | TCP | Client/relay → server | Use 587 with STARTTLS for authenticated submission; 25 for server-to-server relay only. |
| IMAP / IMAPS | 143 / 993 | TCP | Client → server | Mail retrieval; prefer 993. |
| POP3 / POP3S | 110 / 995 | TCP | Client → server | Mail retrieval; prefer 995. |
| RDP | 3389 | TCP | Client → server | Admin. Windows remote desktop; restrict to jump hosts/bastion, never expose directly to the internet. |
| WinRM | 5985 (HTTP), 5986 (HTTPS) | TCP | Client → server | Admin. PowerShell remoting; prefer 5986. |
| NFS | 2049 (NFSv4, single port); NFSv3 uses portmapper 111 + dynamic ports | TCP/UDP | Client → server | File sharing; NFSv4 consolidated the multi-port NFSv3/portmapper model. |
| iSCSI | 3260 | TCP | Initiator → target | Storage. Isolate on a dedicated storage VLAN/subnet (Volume VI). |
| Fibre Channel over Ethernet | N/A (Ethertype 0x8906, not IP) | FCoE | N/A | Storage; not IP-routable, relevant to Volume VI data-center fabric design. |
| vCenter Server / ESXi management | 443 (HTTPS UI/API), 902 (legacy host management/vMotion heartbeat) | TCP | Client/host → vCenter | Admin. See Volume V for the full vSphere port matrix. |
| vMotion | 8000 (control), plus a dedicated migration network | TCP | Host → host | Should always ride an isolated, non-routed vMotion VLAN. |
| Kubernetes API server | 6443 | TCP | kubectl/controller → API server | Admin. |
| etcd | 2379 (client), 2380 (peer) | TCP | Kubernetes control plane ↔ etcd | Admin, cluster-critical; never expose beyond the control plane network. |
| kubelet API | 10250 | TCP | API server → node | Admin; anonymous access must be disabled (Volume VIII, Volume X). |
| Container registry (generic) | 5000 (plain), 443 (typical TLS front end) | TCP | Client/CI runner → registry | Prefer TLS-fronted registries in production. |
| Prometheus | 9090 (server UI/API), 9100 (node_exporter) | TCP | Prometheus → exporter (scrape, pull model) | RO-adjacent; Prometheus initiates scrapes, which is the opposite direction from most monitoring agents. |
| Grafana | 3000 | TCP | Client → server | Dashboard UI. |
| Elasticsearch | 9200 (HTTP API), 9300 (transport/cluster) | TCP | Client/Kibana → node (9200); node ↔ node (9300) | Never expose 9200 without authentication. |
| Redis | 6379 | TCP | Client → server | No authentication by default in many deployments; bind to a private network and enable `requirepass`/ACLs. |
| PostgreSQL | 5432 | TCP | Client → server | |
| MySQL/MariaDB | 3306 | TCP | Client → server | |
| Microsoft SQL Server | 1433 (default instance), 1434/UDP (SQL Browser) | TCP/UDP | Client → server | |
| IPsec IKE | 500 (IKE), 4500 (NAT-T) | UDP | Peer ↔ peer | VPN control plane; ESP (protocol 50) carries the encrypted payload with no port. |
| BGP | 179 | TCP | Peer ↔ peer (either side may initiate) | Routing protocol; see Volume II/III for adjacency design. |
| OSPF | N/A (IP protocol 89) | IP | Multicast (224.0.0.5/6) between neighbors | No TCP/UDP port; filtered by protocol number, not port. |
| VRRP | N/A (IP protocol 112) | IP | Multicast (224.0.0.18) | First-hop redundancy; no port. |
| HSRP | 1985 | UDP (multicast 224.0.0.2 or 102, version-dependent) | Router ↔ router | Cisco first-hop redundancy equivalent to VRRP. |
| GRE | N/A (IP protocol 47) | IP | Tunnel endpoint ↔ tunnel endpoint | Common cause of "the tunnel won't come up" when only TCP/UDP ports were opened. |
| Redfish / IPMI | 443 (Redfish, HTTPS REST), 623 (IPMI, UDP) | TCP/UDP | Client → BMC | Admin. Out-of-band server management (Volume XXII/XXIII); IPMI is legacy and less secure than Redfish. |
| PAN-OS management | 443 (Web UI/API), 3978 (HA), 28260/28769 (log collection, version-dependent) | TCP | Admin → firewall; peer ↔ peer (HA) | Confirm HA and log-collection ports against the current PAN-OS release. |
| FortiOS management | 443 (Web UI), 541 (FortiGate-FortiManager, FGFM protocol) | TCP | Admin → device; device ↔ FortiManager | |
| DNS over TLS (DoT) | 853 | TCP | Client → resolver | Encrypted DNS. |
| DNS over HTTPS (DoH) | 443 | TCP | Client → resolver | Encrypted DNS sharing the HTTPS port, which complicates port-based DNS policy enforcement. |
| PTP (Precision Time Protocol) | 319 (event), 320 (general) | UDP | Peer ↔ peer | Sub-microsecond time sync for environments NTP cannot satisfy. |

### Reading and writing a traffic flow statement

Use a fixed five-field template for every flow recorded in a design
document, firewall change request, or security-group definition:

```text
Source: <zone/subnet/host>
Destination: <zone/subnet/host>
Port/Protocol: <port>/<TCP|UDP|ICMP|IP-protocol-number>
Direction: <initiator> -> <responder>
Purpose: <one-line service/application identity>
```

Example — a three-tier web application's east-west flows:

```text
Source: web-tier (10.10.10.0/24)
Destination: app-tier (10.10.20.0/24)
Port/Protocol: 8443/TCP
Direction: web-tier -> app-tier
Purpose: Internal REST API calls, TLS-terminated at app-tier load balancer

Source: app-tier (10.10.20.0/24)
Destination: db-tier (10.10.30.0/24)
Port/Protocol: 5432/TCP
Direction: app-tier -> db-tier
Purpose: PostgreSQL primary connection pool
```

This template is deliberately the same shape a stateful firewall rule,
an AWS/Azure security-group rule, and a Kubernetes `NetworkPolicy` all
need — only the syntax differs, not the five facts.

## Validation and Troubleshooting

- **Confirm listening state on the destination first.** `ss -tulpn`
  (Linux) or `Get-NetTCPConnection -State Listen` (Windows PowerShell)
  shows whether the service is actually bound to the expected port before
  blaming the network.
- **Test reachability independent of the application.** `nc -zv <host>
  <port>` or `Test-NetConnection -ComputerName <host> -Port <port>`
  (PowerShell) distinguishes "port unreachable" from "port open but
  application not responding," which point to entirely different fix
  paths (firewall/routing vs. application/service state).
- **Capture and read the handshake, not just the result.** `tcpdump -ni
  <iface> tcp port <port>` (see Volume XX for full packet-analysis
  methodology) shows whether a SYN is answered with SYN-ACK (application
  reachable), RST (port closed/rejected), or nothing (silently dropped by
  a firewall — the most common false "the network is slow" symptom).
- **Trace the path for routed flows.** `traceroute`/`tracert` (ICMP or
  UDP-based, per OS) or `mtr` identifies the hop at which a flow stops,
  which combined with the five-field flow statement quickly identifies
  which device's rule set to inspect next.
- **For UDP services, remember that "no response" is ambiguous by
  design.** UDP has no handshake to fail cleanly; a missing DNS or SNMP
  response can mean a dropped request, a dropped reply, or an
  application-layer timeout, and the fix is to capture packets in both
  directions rather than infer from one-sided silence.
- **Check both source and destination firewall state for stateful
  services.** A rule permitting outbound TCP/443 with no matching
  established/related return rule fails intermittently in ways that look
  like flaky connectivity rather than a policy defect.

## Security and Best Practices

- Default-deny inbound and outbound, and enumerate only the flows the
  five-field template documents; an "allow any" rule anywhere in the path
  defeats every other control in this table.
- Retire cleartext protocols (Telnet, FTP, HTTP, SNMPv1/v2c, unencrypted
  syslog and LDAP) on any network segment that is not both physically
  isolated and explicitly scoped for legacy equipment; track remaining
  exceptions as a risk-register entry (Chapter 07).
- Never expose RDP, WinRM, SSH, database ports, or Kubernetes/etcd
  control-plane ports directly to the internet; require a bastion host,
  VPN, or Zero Trust broker (Volume X, Volume XVI) for administrative
  access.
- Bind development-convenience services (Redis, Elasticsearch, unsecured
  container registries) to private networks by default; these services
  are common ransomware and data-exposure entry points precisely because
  their defaults favor ease of use over authentication.
- Log and alert on connections to registered/ephemeral ports that do not
  match an expected service fingerprint — unexpected traffic on an
  otherwise idle high port is a common early indicator of a reverse shell
  or command-and-control channel.
- Review this table's ports against the current release notes for each
  platform after every `SOFTWARE_VERSIONS.md` baseline update; vendors do
  change default ports and add new management planes between major
  releases (PAN-OS HA/log-collection ports are a known example).

## References and Knowledge Checks

**References**

- IANA Service Name and Transport Protocol Port Number Registry
  (`iana.org/assignments/service-names-port-numbers`).
- RFC 793 (TCP), RFC 768 (UDP), RFC 792 (ICMP), RFC 4443 (ICMPv6).
- RFC 5425 (syslog over TLS), RFC 6587 (syslog over TCP framing).
- Volume II — Network Engineering Foundations (transport-layer theory).
- Volume V — VMware Virtualization (full vSphere/ESXi port matrix).
- Volume X — Enterprise Cybersecurity (segmentation and Zero Trust
  architecture).
- Volume XX — Wireshark and Packet Analysis (packet-level validation of
  every flow in this chapter).
- `SOFTWARE_VERSIONS.md` (repository root) — dated baseline for
  vendor-specific port references.

**Knowledge checks**

1. Why is a firewall rule that permits "TCP/443 between A and B" less
   precise than a five-field flow statement, even though both technically
   describe the same port?
2. A GRE-over-IPsec tunnel fails to establish even though UDP/500 and
   UDP/4500 are permitted in both directions. What protocol number is most
   likely still blocked, and why would a port-only rule set miss it?
3. Explain why "no response" from a UDP-based service is diagnostically
   ambiguous in a way that a TCP RST is not, and what tool resolves the
   ambiguity.
4. Name three services in the reference table above that default to a
   cleartext or unauthenticated posture, and their encrypted or
   authenticated replacement.

## Hands-On Lab

**Objective:** Build and validate a service-to-port quick-reference card
scoped to your own environment, using the five-field flow template.

**Prerequisites:** Access to at least two hosts/services on a lab or
non-production network; `nc`/`Test-NetConnection` and `tcpdump`/Wireshark
available; a Markdown editor.

1. Create `port-reference-card.md` with a table containing columns
   `Service`, `Port`, `Protocol`, `Direction`, `Purpose`. **Expected
   result:** a table skeleton renders correctly in a Markdown preview.
2. Select five services actually running in your lab or work environment
   (for example SSH, DNS, HTTPS, a database, and one monitoring service)
   and populate one row per service using this chapter's table as a
   starting point, correcting any value that differs in your environment.
   **Expected result:** five populated, environment-verified rows.
3. For each service, run a listening-state check on the host
   (`ss -tulpn` or `Get-NetTCPConnection -State Listen`) and record the
   observed bound address (`0.0.0.0`, a specific interface, or
   `127.0.0.1`) as a new column, `Bound Address`. **Expected result:** the
   card now distinguishes services reachable only locally from services
   reachable across the network.
4. From a second host, test reachability to each service's port with
   `nc -zv` or `Test-NetConnection` and record pass/fail. **Expected
   result:** at least one row shows a successful connection and the
   result is recorded with a timestamp.
5. Choose one TCP service and capture the three-way handshake with
   `tcpdump -ni <iface> tcp port <port> -c 6` (or the equivalent Wireshark
   capture filter) while initiating a connection from the second host.
   **Expected result:** the capture shows SYN, SYN-ACK, ACK in order,
   confirming the flow matches the five-field statement recorded in step
   2.
6. Negative test: attempt a connection to a port you have not opened
   (for example, an unused high port) and record whether the result is a
   TCP RST, an ICMP unreachable, or silence (timeout). **Expected
   result:** the card documents the observable difference between a
   closed port and a firewalled port, which is a recurring troubleshooting
   distinction (Chapter 06).
7. Write one five-field flow statement (using the template in this
   chapter) for each service tested and save it alongside the table.
   **Expected result:** the file contains both a scan table and formal
   flow statements suitable for a firewall change request.

**Cleanup:** Close any temporary listener opened solely for the negative
test in step 6, and remove any packet-capture files containing
environment-specific addressing before sharing the card outside your team.

## Summary and Completion Checklist

This chapter consolidated the transport-layer theory (TCP, UDP, ICMP, and
port-less IP protocols), the IANA port-range taxonomy, and a single
reference table spanning the operating systems, network devices, security
appliances, virtualization platforms, container orchestrators, databases,
and monitoring tools covered across Volumes II through XXIII. The
five-field flow template converts any of those rows into a precise
firewall rule, security-group entry, or `NetworkPolicy`.

- [ ] I can name the port, protocol, and typical initiator for at least 15
      services from the reference table without looking it up.
- [ ] I can explain the difference between well-known, registered, and
      dynamic/ephemeral ports and why the distinction matters for firewall
      rule design.
- [ ] I can identify a port-less IP protocol (GRE, ESP, OSPF, VRRP) and
      explain why a port-only firewall rule set misses it.
- [ ] I wrote and validated at least five five-field flow statements
      against real listening services in a lab environment.
- [ ] I can distinguish a closed port (RST), a firewalled port (silence/
      timeout), and an application-layer failure (port open, no valid
      response) using a packet capture.
