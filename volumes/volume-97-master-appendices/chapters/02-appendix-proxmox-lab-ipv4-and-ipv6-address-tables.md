# Chapter 02: Appendix — Proxmox Lab IPv4 and IPv6 Address Tables

The as-built addressing for the Dell PowerEdge R640 Proxmox lab
documented in
[Volume XXVI — Proxmox Virtualization Lab on Dell PowerEdge R640](../../volume-26-proxmox-lab-poweredge-r640/README.md).
**Appendix A** records the IPv4 plan as deployed; **Appendix B** is the
IPv6 template, awaiting an assigned prefix, because the build is
IPv4-only. The environment specification and build chapters live in the
source volume; these tables are the quick-reference record.

## Appendix A: IPv4 Table

The complete IPv4 addressing for the build — the iDRAC and Proxmox host
management interfaces followed by the ten virtual machines. Every address
uses a /24 network mask (255.255.255.0).

| Hostname | IPv4 Address | Network Mask | Gateway | VLAN ID |
| --- | --- | --- | --- | --- |
| `idrac` † | 10.30.161.25 | 255.255.255.0 | 10.30.161.1 | untagged † |
| `pve` † | 10.30.161.10 | 255.255.255.0 | 10.30.161.1 | untagged † |
| `ubuntu1` | 10.30.12.100 | 255.255.255.0 | 10.30.12.1 | 6 |
| `ubuntu-server1` | 10.30.10.100 | 255.255.255.0 | 10.30.10.1 | 3 |
| `eve-ng` | 10.30.10.85 | 255.255.255.0 | 10.30.10.1 | 3 |
| `gns3` | 10.30.10.86 | 255.255.255.0 | 10.30.10.1 | 3 |
| `cml` | 10.30.10.87 | 255.255.255.0 | 10.30.10.1 | 3 |
| `rhel-desktop1` | 10.30.12.101 | 255.255.255.0 | 10.30.12.1 | 6 |
| `rhel-server1` | 10.30.10.88 | 255.255.255.0 | 10.30.10.1 | 3 |
| `win11-1` | 10.30.12.102 | 255.255.255.0 | 10.30.12.1 | 6 |
| `win-server1` | 10.30.10.89 | 255.255.255.0 | 10.30.10.1 | 3 |
| `netbox` | 10.30.10.62 | 255.255.255.0 | 10.30.10.1 | 3 |

† The iDRAC and the Proxmox host management interface were specified by
role rather than hostname in the source build; `idrac` and `pve` are
conventional labels used here. Both sit on the management network
(10.30.161.0/24) on the dedicated management port, which is untagged rather
than carried on the VM trunk, so they have no VLAN tag.

## Appendix B: IPv6 Table

**This build defines no IPv6 addressing.** The specification is IPv4-only
throughout (the 10.30.0.0/16 space), so there are no IPv6 addresses,
prefixes, or gateways to record. The table below is therefore a **template**
rather than an as-built record: the hostnames and VLAN IDs are carried over
from the IPv4 plan, and the IPv6 columns are left to be completed if and
when IPv6 is added — which requires an assigned IPv6 prefix the build does
not currently have.

IPv6 uses a **prefix length** (for example `/64`) rather than the dotted
network mask of IPv4, so the third column below is *Prefix Length* rather
than *Network Mask*; it will hold a value such as `/64` once addressing is
assigned.

| Hostname | IPv6 Address | Prefix Length | Gateway | VLAN ID |
| --- | --- | --- | --- | --- |
| `idrac` | *not assigned* | *not assigned* | *not assigned* | untagged |
| `pve` | *not assigned* | *not assigned* | *not assigned* | untagged |
| `ubuntu1` | *not assigned* | *not assigned* | *not assigned* | 6 |
| `ubuntu-server1` | *not assigned* | *not assigned* | *not assigned* | 3 |
| `eve-ng` | *not assigned* | *not assigned* | *not assigned* | 3 |
| `gns3` | *not assigned* | *not assigned* | *not assigned* | 3 |
| `cml` | *not assigned* | *not assigned* | *not assigned* | 3 |
| `rhel-desktop1` | *not assigned* | *not assigned* | *not assigned* | 6 |
| `rhel-server1` | *not assigned* | *not assigned* | *not assigned* | 3 |
| `win11-1` | *not assigned* | *not assigned* | *not assigned* | 6 |
| `win-server1` | *not assigned* | *not assigned* | *not assigned* | 3 |
| `netbox` | *not assigned* | *not assigned* | *not assigned* | 3 |
