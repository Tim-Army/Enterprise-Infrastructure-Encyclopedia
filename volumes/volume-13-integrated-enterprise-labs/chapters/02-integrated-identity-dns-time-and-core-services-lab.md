# Chapter 02: Integrated Identity, DNS, Time, and Core Services Lab

![Lab topology for this chapter: dc01 (forest root) and dc02 (additional domain controller and global catalog) replicate with zero failures, share a converged time hierarchy, and load-balance a DHCP scope in Normal state; linux01 joins the domain via realm, and its Kerberos ticket confirms DNS SRV lookup, Kerberos, and LDAP all work from a non-Windows client. As a negative test, dc01 is powered off to simulate an unplanned failure; linux01's Kerberos authentication still succeeds because dc02 answers the KDC request, and DHCP failover reports a degraded partner but keeps leasing from dc02 alone. Powering dc01 back on brings both replication and DHCP failover back to a fully healthy state.](../../../diagrams/volume-13-integrated-enterprise-labs/chapter-02-ad-forest-dc-failure-topology.svg)

*Figure 2-1. Topology used throughout this chapter's Hands-On Lab: a two-node Active Directory forest with DHCP failover and a domain-joined Linux client, tested against a domain controller outage.*

## Learning Objectives

- Deploy a two-node Active Directory Domain Services forest for
  `corp.meridian.example` with AD-integrated DNS, matching the domain and
  addressing plan established in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md).
- Build a layered time-synchronization hierarchy that keeps every
  Kerberos-dependent system inside its authentication tolerance window.
- Configure DHCP failover for the HQ user and wireless/guest VLANs and prove
  the failover partner assumes full scope ownership during an outage.
- Join a Linux host to the domain with `realmd`/SSSD and validate the full
  DNS-to-Kerberos-to-LDAP chain from a non-Windows client.
- Diagnose and recover from a single domain controller failure without a
  directory-wide outage, and capture the recovery as reviewable evidence.

## Theory and Architecture

Identity, DNS, and time are the three services every later chapter in this
volume quietly depends on. Campus and wireless authentication in [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md),
vSphere and backup service accounts in [Chapter 04](04-virtualization-storage-and-data-protection-lab.md), cluster and pipeline
identities in Chapters 05 and 06, and every detection rule and audit trail
in [Chapter 07](07-zero-trust-detection-and-incident-response-lab.md) all assume a directory that resolves names correctly and
agrees on the time. This chapter builds that foundation once, on the `HQ`
site and the VLAN 110 core-services subnet (`10.13.10.0/24`) defined in
[Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)'s topology manifest, so every later chapter can simply point at
`corp.meridian.example` and trust it.

The design follows [Volume IV, Chapter 04](../../volume-04-enterprise-systems-administration/chapters/04-enterprise-identity-and-directory-services.md) (Enterprise Identity and Directory
Services): a single-domain Active Directory forest, DNS integrated directly
into that directory rather than run as a separate service, and a
Windows-Time hierarchy rooted at the domain's PDC emulator — the same
architecture [Volume II, Chapter 05](../../volume-02-network-engineering-foundations/chapters/05-core-network-services.md) (Core Network Services) treats generically
for DNS, DHCP, and NTP. [Volume IV](../../volume-04-enterprise-systems-administration/README.md), Chapters 02 and 03 (Enterprise Linux
Administration and Windows Server Administration) supply the host-level
mechanics this chapter assumes: package management, service management, and
basic firewall configuration on both operating systems.

At this point in the volume, inter-VLAN traffic still crosses the ad hoc
lab router/firewall provisioned informally in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) to give `ctrl01` a
default gateway and NAT path — not yet the resilient Cisco campus and WAN
fabric [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) builds. That is a deliberate sequencing choice: this
chapter's services must work correctly over "good enough" routing before
[Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) replaces the routing layer underneath them, so any regression
introduced by the network rebuild is easy to attribute.

### Systems introduced in this chapter

| Hostname | Role | Address | VLAN |
| --- | --- | --- | --- |
| `dc01` | Forest root DC, DNS, PDC emulator | `10.13.10.11/24` | 110 |
| `dc02` | Additional DC, DNS, global catalog | `10.13.10.12/24` | 110 |
| `linux01` | Domain-joined Linux validation client | `10.13.20.21/24` | 120 |

`ctrl01` (`10.13.10.30`, provisioned in [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md)) remains the automation
controller and evidence-capture host for this chapter's lab.

## Design Considerations

- **Single domain, not a multi-domain forest.** A single-domain forest
  (`corp.meridian.example`) is sufficient to exercise every mechanism this
  volume needs — replication, DNS integration, Kerberos, DHCP failover —
  without the added administrative-boundary complexity a multi-domain
  design would add for no lab benefit.
- **Both domain controllers at HQ, for now.** [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md) introduces a
  read-only domain controller at `BR1` once a real WAN link exists between
  sites; placing it there before the WAN is real would validate against
  routing that will be discarded. Note this dependency now so [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)'s
  design does not appear to arrive out of nowhere.
- **DNS forwarders, not root hints.** Point `dc01`/`dc02` at the lab
  router's NAT'd resolver as a conditional forwarder for anything outside
  `corp.meridian.example`, rather than letting each DC walk the internet
  root hierarchy from inside a NAT'd lab — faster, and it keeps outbound
  lab DNS traffic attributable to one exit point for the isolation checks
  [Chapter 01](01-lab-engineering-safety-reproducibility-and-evidence.md) established.
- **Time hierarchy has exactly one root.** The PDC emulator (`dc01`) is the
  only system in the lab that synchronizes from an external source; every
  other domain member — including `dc02` — synchronizes from a domain
  controller. Pointing multiple systems independently at external time
  sources is a common cause of Kerberos clock-skew failures that this
  design avoids by construction.
- **DHCP failover mode differs by VLAN.** VLAN 120 (user/endpoint) uses
  load-balance failover so both DCs actively lease during normal operation,
  exercising both partners continuously. VLAN 140 (wireless/guest, built out
  in [Chapter 03](03-campus-wan-wireless-and-network-services-lab.md)) is configured for hot-standby instead, because guest
  traffic tolerates a brief failover pause better than it tolerates
  splitting scope state across two active servers for a segment with much
  higher churn.
- **Service accounts, not shared administrator logons.** Every automated
  task this chapter configures (DHCP failover partner communication, the
  Linux domain-join binding account) uses a dedicated, least-privilege
  service account, consistent with the tiered administration model Volume
  X, Chapter 02 (Enterprise Identity, Zero Trust, and Privileged Access)
  describes in depth.

## Implementation and Automation

Promote `dc01` as the forest root. Run this on the freshly provisioned
Windows Server VM after setting its static address and hostname per the
table above:

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSForest `
  -DomainName "corp.meridian.example" `
  -DomainNetbiosName "CORP" `
  -InstallDns:$true `
  -SafeModeAdministratorPassword (ConvertTo-SecureString "<DSRM_PASSWORD>" -AsPlainText -Force) `
  -Force:$true
```

After `dc01` reboots into the new forest, join `dc02` and promote it as an
additional domain controller and global catalog server:

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSDomainController `
  -DomainName "corp.meridian.example" `
  -InstallDns:$true `
  -Credential (Get-Credential CORP\Administrator) `
  -SafeModeAdministratorPassword (ConvertTo-SecureString "<DSRM_PASSWORD>" -AsPlainText -Force) `
  -Force:$true
```

Configure DNS forwarding on both DCs toward the lab router's resolver
(`10.13.10.1` in this topology) for anything outside the AD-integrated
zone:

```powershell
Add-DnsServerForwarder -IPAddress 10.13.10.1 -PassThru
```

Fix the time hierarchy so `dc01` is the only externally synchronized
system:

```powershell
# On dc01 (PDC emulator)
w32tm /config /manualpeerlist:"time.cloudflare.com,0x8 pool.ntp.org,0x8" /syncfromflags:manual /reliable:yes /update
Restart-Service w32time

# On dc02 and every other domain member
w32tm /config /syncfromflags:domhier /update
Restart-Service w32time
```

Configure DHCP on `dc01` and `dc02` for VLAN 120, then establish
load-balance failover between them:

```powershell
Add-DhcpServerv4Scope -Name "VLAN120-User" -StartRange 10.13.20.50 `
  -EndRange 10.13.20.200 -SubnetMask 255.255.255.0 -State Active
Add-DhcpServerv4Failover -Name "dc01-dc02-vlan120" -ScopeId 10.13.20.0 `
  -PartnerServer dc02.corp.meridian.example -LoadBalancePercent 50 `
  -SharedSecret "<FAILOVER_SECRET>"
```

Join `linux01` to the domain (RHEL/Ubuntu; package name varies by
distribution but the workflow is identical per Volume IV, Chapter 02):

```bash
sudo dnf install -y realmd sssd oddjob oddjob-mkhomedir adcli krb5-workstation
sudo realm join --user=svc-domainjoin corp.meridian.example
sudo systemctl enable --now sssd
```

## Validation and Troubleshooting

- **Replication health.** `repadmin /replsummary` on either DC must show
  0 failures. `dcdiag /v` should pass every test, in particular
  `Advertising`, `KnowsOfRoleHolders`, and `NetLogons`.
- **DNS resolution both directions.** From `ctrl01`,
  `nslookup dc02.corp.meridian.example dc01` and
  `nslookup dc01.corp.meridian.example dc02` must both resolve — confirming
  each DC serves the zone correctly, not just its own record.
- **Time convergence.** `w32tm /monitor` from `dc01` should show `dc02`'s
  offset within a few hundred milliseconds. On `linux01`, `chronyc tracking`
  (configured to point at `dc01`/`dc02`) should show a similarly small
  offset. Kerberos authentication starts failing once skew exceeds five
  minutes (the default `MaxClockSkew`), so treat any growing offset as an
  early warning, not a cosmetic issue.
- **DHCP failover state.** `Get-DhcpServerv4Failover` on either DC must
  report `LOAD BALANCE` and a `Normal` communication state before the
  negative test in this chapter's lab; anything else means the failover
  relationship itself is unhealthy and must be fixed before it can be
  trusted to fail over.
- **Common failure: SYSVOL/DFSR not initialized on `dc02`.** If Group
  Policy objects fail to apply from `dc02`, check
  `dfsrmig /getmigrationstate` — a stalled FRS-to-DFSR migration state is
  the most frequent cause in a freshly promoted lab domain.
- **Common failure: DNS dynamic update misconfiguration.** If `linux01`
  registers successfully once but stops updating its record after a lease
  renewal, confirm the zone allows secure dynamic updates
  (`Get-DnsServerZone | Select DynamicUpdate`) rather than none — a zone set
  to no dynamic updates silently drops every subsequent registration.

## Security and Best Practices

- Apply the tiered administration model from Volume X, Chapter 02: no
  domain administrator credential is ever used to log on to `linux01` or
  `ctrl01` directly; use the dedicated `svc-domainjoin` service account,
  scoped only to computer-object creation, for the realm join.
- Restrict dynamic DNS updates to `Secure only` on the AD-integrated zone —
  an open dynamic-update zone lets any host on the segment overwrite
  another host's record.
- Disable SMBv1 on both domain controllers (`Disable-WindowsOptionalFeature
  -Online -FeatureName SMB1Protocol`); nothing in this volume's lab requires
  it, and leaving it enabled would model a real hardening gap.
- Rotate the DHCP failover shared secret and the `svc-domainjoin` account
  password out of this chapter's command history before treating the lab as
  a stable baseline; do not leave lab secrets in shell scrollback that later
  evidence bundles might capture.
- Feed authentication and directory service event logs from both DCs toward
  `siem01` once it exists in Chapter 07 — this chapter's job is to make sure
  there is something worth logging; Chapter 07 is where that logging becomes
  actionable detection.

## References and Knowledge Checks

**References**

- RFC 1035 — *Domain Names: Implementation and Specification*.
- RFC 2131 — *Dynamic Host Configuration Protocol*.
- RFC 4120 — *The Kerberos Network Authentication Service (V5)*.
- [Volume II, Chapter 05](../../volume-02-network-engineering-foundations/chapters/05-core-network-services.md) — Core Network Services.
- [Volume IV](../../volume-04-enterprise-systems-administration/README.md), Chapters 02–04 — Enterprise Linux Administration, Windows
  Server Administration, and Enterprise Identity and Directory Services.
- [Volume X, Chapter 02](../../volume-10-enterprise-cybersecurity/chapters/02-enterprise-identity-zero-trust-and-privileged-access.md) — Enterprise Identity, Zero Trust, and Privileged
  Access.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this chapter's Windows Server and Linux hosts.

**Knowledge checks**

1. Why does only the PDC emulator synchronize from an external time
   source, rather than every domain controller independently?
2. What operational risk does a load-balance DHCP failover configuration
   reduce compared to hot-standby, and why is VLAN 140 configured
   differently from VLAN 120?
3. Which `dcdiag` and `repadmin` outputs would you check first if `dc02`
   appeared healthy but Group Policy was not applying to clients that
   authenticated against it?
4. Why is the BR1 domain controller deferred to Chapter 03 instead of being
   built alongside `dc01`/`dc02` in this chapter?

## Hands-On Lab

**Objective:** Build the two-node `corp.meridian.example` Active Directory
forest, layered time hierarchy, DHCP failover pair, and a domain-joined
Linux validation client, then prove the directory survives a single domain
controller failure.

**Prerequisites**

- The Chapter 01 lab scaffold (`~/vol13-lab/topology.yml`, `evidence.sh`)
  and the `ch01-baseline` snapshot, restored as this chapter's starting
  point.
- Capacity for two Windows Server VMs and one Linux VM in addition to
  `ctrl01` (4 vCPU/8 GB RAM recommended for each domain controller).
- Familiarity with Windows Server administration and Linux administration
  at the level of Volume IV, Chapters 02–03.

**Steps**

1. Restore the `ch01-baseline` snapshot (or confirm `ctrl01` still matches
   it) so this chapter starts from the known-clean scaffold.

2. Provision `dc01` (10.13.10.11/24, VLAN 110) and `dc02`
   (10.13.10.12/24, VLAN 110) as Windows Server VMs, and `linux01`
   (10.13.20.21/24, VLAN 120) as a Linux VM, per the addressing table
   above.

3. Promote `dc01` as the forest root using the `Install-ADDSForest` command
   in Implementation and Automation. Reboot and confirm logon as
   `CORP\Administrator` succeeds before continuing.

4. Take a snapshot named `ch02-dc01-promoted` before joining `dc02` — this
   is the cheapest point to roll back to if the second promotion goes
   wrong.

5. Join and promote `dc02` as an additional domain controller and global
   catalog using the second `Install-ADDSDomainController` command.

6. **Expected result — replication.** From `ctrl01`, over the lab
   router's existing routing:

   ```bash
   ./evidence.sh "ssh administrator@dc01.corp.meridian.example \
     'repadmin /replsummary && dcdiag /q'"
   ```

   `repadmin /replsummary` must show 0 failures; `dcdiag /q` should return
   no failed test lines.

7. Configure DNS forwarding and the time hierarchy on both DCs using the
   commands in Implementation and Automation.

8. **Expected result — time convergence.** Capture and confirm offsets are
   within a few hundred milliseconds:

   ```bash
   ./evidence.sh "ssh administrator@dc01.corp.meridian.example 'w32tm /monitor'"
   ```

9. Configure the VLAN 120 DHCP scope and load-balance failover between
   `dc01` and `dc02` using the commands in Implementation and Automation.

10. **Expected result — failover health.**

    ```bash
    ./evidence.sh "ssh administrator@dc01.corp.meridian.example \
      'Get-DhcpServerv4Failover'"
    ```

    Must report `LOAD BALANCE` mode and `Normal` state before proceeding.

11. Join `linux01` to the domain using the `realm join` command in
    Implementation and Automation, then validate the full chain:

    ```bash
    ./evidence.sh "ssh linux01 'realm list && id CORP\\\\svc-domainjoin@corp.meridian.example && kinit svc-domainjoin && klist'"
    ```

    **Expected result:** `realm list` shows `corp.meridian.example` as
    `configured`, `id` resolves the domain account, and `kinit`/`klist`
    show a valid ticket-granting ticket — proof that DNS SRV lookup,
    Kerberos, and LDAP are all functioning from a non-Windows client.

12. Take a snapshot named `ch02-baseline` capturing this fully validated
    state.

13. **Negative test:** Power off `dc01` to simulate an unplanned domain
    controller failure:

    ```bash
    ./evidence.sh "ssh linux01 'kdestroy && kinit svc-domainjoin && klist'"
    ```

    **Expected result:** Kerberos authentication still succeeds — `dc02`
    answered the KDC request. Confirm DHCP failover also held:

    ```bash
    ./evidence.sh "ssh administrator@dc02.corp.meridian.example \
      'Get-DhcpServerv4Failover; Get-DhcpServerv4Scope'"
    ```

    DHCP failover state should now report a degraded partner but continue
    leasing from `dc02` alone.

14. **Recovery:** Power `dc01` back on. Wait for it to rejoin, then confirm
    replication and failover both re-converge:

    ```bash
    ./evidence.sh "ssh administrator@dc01.corp.meridian.example \
      'repadmin /replsummary'"
    ./evidence.sh "ssh administrator@dc01.corp.meridian.example \
      'Get-DhcpServerv4Failover'"
    ```

    Both commands must report a healthy state again — `Normal`
    communication and 0 replication failures — before this chapter is
    considered complete.

15. **Cleanup:** Retake the `ch02-baseline` snapshot on all three new VMs
    if any state changed during the negative test, so Chapter 03 starts
    from a known-good identity layer. Append the new hostnames to
    `~/vol13-lab/topology.yml` and commit:

    ```bash
    cd ~/vol13-lab
    git add topology.yml
    git commit -m "Chapter 02: identity, DNS, time, and core services"
    ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the identity, DNS, and time foundation every later
chapter in this volume depends on: a replicated two-node Active Directory
forest for `corp.meridian.example`, a single-rooted time hierarchy, DHCP
failover for the user VLAN, and a validated Linux domain join. The negative
test proved the directory tolerates a single domain controller failure
without an authentication outage, and the recovery step confirmed
replication and failover both re-converge cleanly.

- [ ] Promoted `dc01` and `dc02` as a replicated Active Directory forest
      with AD-integrated DNS.
- [ ] Configured a single-rooted time hierarchy and confirmed convergence.
- [ ] Configured and validated DHCP load-balance failover for VLAN 120.
- [ ] Joined `linux01` to the domain and validated DNS, Kerberos, and LDAP
      end to end.
- [ ] Completed the negative test (single DC failure) and recovery, with
      evidence captured for both.
