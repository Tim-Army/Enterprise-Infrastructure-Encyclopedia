# Chapter 09: Automating the Lab Virtual Machines on VMware ESXi 7, 8, and 9

## Learning Objectives

- Name the twelve virtual machines of the Chapter 999 lab, the network each one attaches to, and the cloud-init seed that gives each its hostname, addresses, and packages.
- Build the virtual switches and port groups the lab needs on a standalone ESXi 7, 8, or 9 host, including the trunk port groups that `gw-201` bridges.
- Run `Deploy-Lab201-Esxi.ps1` against an ESXi host, check each machine, remove the build network adapters, and take the `baseline-201` snapshots.
- Say which differences between ESXi 7, 8, and 9 change the script's behavior: the virtual hardware version, the license that allows API writes, and the support status.
- Recognize the cases where the script cannot work (free license, missing uplinks) and what to do instead.

## Theory and Architecture

### What the automation builds

[Chapter 999](999-shared-lab-infrastructure.md) lists the hosts of the shared lab and says they can all be virtual except the two switches. The Chapters 09 to 13 turn that list into scripts, one chapter for each place the machines can run. All five chapters read the same manifest and use the same seed tool, so a machine has the same name, the same addresses, and the same packages whichever platform builds it.

| Machine | Role | vCPU | Memory (MB) | Disk (GB) | Networks |
| --- | --- | --- | --- | --- | --- |
| `gw-201` | Gateway and firewall | 2 | 2048 | 20 | wan, oob, T1 trunk, T2 trunk |
| `svc-201a` | RADIUS, syslog, NTP, SNMP manager | 2 | 4096 | 40 | T1 VLAN 10 |
| `svc-201b` | RADIUS, syslog, NTP, collectors, file server | 2 | 4096 | 40 | T1 VLAN 10 |
| `ca-201` | Lab certificate authority | 1 | 1024 | 16 | T1 VLAN 10 |
| `dhcp-201` | DHCP server | 1 | 1024 | 16 | T1 VLANs 10, 40, 41, 50 |
| `admin-201` | Administrator workstation | 2 | 4096 | 40 | T1 VLAN 20 |
| `rtr-peer-1` | Routing peer, AS 65202 | 1 | 1024 | 16 | T1 VLAN 2001, T2 VLAN 2003, segment 220 |
| `rtr-peer-2` | Routing peer, AS 65203 | 1 | 1024 | 16 | T1 VLAN 2002, T2 VLAN 2004 |
| `mcast-src-201` | Multicast source | 1 | 512 | 8 | segment 220 |
| `static-1`, `static-2` | Statically addressed hosts | 1 each | 512 each | 8 each | T1 VLAN 42 |
| `attacker-201` | Spoofing and flooding test host | 2 | 2048 | 20 | T1 VLAN 42 |

Every machine also has a **build** network adapter on the `lab201-wan` network, first in its adapter list. It gets an address by DHCP so that cloud-init can install packages, and it is removed when the build is done. The twelve machines need 17 vCPUs, 21.5 GiB of memory, and up to 248 GB of thin-provisioned disk.

Four items in Chapter 999 are not built by the scripts. `fgt-201` needs a FortiGate-VM image that Fortinet supplies under license, `og-201` is the console server of [Chapter 08](08-opengear-im7216-console-server-and-optional-console-lab.md), `oob-admin-201` is a laptop, and `vx-host-a` and `vx-host-b` plug into switch ports. Chapter 999 lets `gw-201` be a Linux router, and so do the scripts.

### The shared files

The scripts are in one folder and are downloadable as a unit.

| File | Purpose |
| --- | --- |
| `common/lab201-vms.json` | The manifest: networks, machines, sizes, adapters, and IPv4 addresses. The IPv6 address of each IPv4 address is derived (`fd00:db8:201::` plus the third and fourth octets in hexadecimal), so the two families cannot drift apart. |
| `common/make-seed.py` | Renders the cloud-init files for each machine and, with `--iso`, writes a seed ISO labeled `cidata`. |
| `builder/lab-builder.html` | The [Lab Builder](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/lab-scripts/builder/lab-builder.html), a page that runs in your browser. It writes a manifest for your choices, the commands for each platform, and a checklist, and downloads them as a zip. |
| `diagrams/lab-topology.svg` and `.png` | The Chapter 999 network diagram, copied into the zip when the site is built, so the scripts and the picture of what they build travel together. |
| `esxi/Deploy-Lab201-Esxi.ps1` | This chapter's script. |

[Download the whole set as one zip](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/volume-201-fortiswitch-stig-and-srg-mapping-lab-scripts.zip), or fetch single files from the [lab-scripts folder](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/lab-scripts/common/lab201-vms.json). A `SHA256SUMS` file in the folder lists the checksum of every script.

### The Lab Builder

The [Lab Builder](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/lab-scripts/builder/lab-builder.html) is one HTML page that runs in your browser, with the manifest built into it. You choose a platform and version, fill in the names of your hosts, storage, and network connections, and change what to build. It then writes three things: a copy of the manifest that holds your changes, the commands to run for your platform (a preview, the build, the removal of the build adapters, and the baseline snapshots), and a checklist of what the scripts cannot do. A zip button bundles them with the platform's script, `make-seed.py`, the README, and the network diagram. The page has to be opened from the published site for the zip to include the scripts, because a page opened from a local file cannot fetch them.

What you can change:

- **Machines.** Leave any machine out (the gateway always stays), rename it, and change its vCPUs, memory, and disk. Each machine has a proposed minimum size, and a value below it is refused, with the default kept, unless you tick that machine's **Override** box. The minimums are the `min` values in the manifest. They are proposals, and each needs a test build before you rely on it.
- **Names.** A name uses lowercase letters, digits, and hyphens, and must be unique. The scripts find the gateway by its `role`, not its name, so it can be renamed. Chapter 999 and the requirement labs use the default names, so keep a note of your renames.
- **Address block.** Move the lab to another private block (the first two octets of IPv4, and a unique local IPv6 prefix). The manifest holds the two prefixes (`ipv4_prefix` and `ipv6_prefix`), and `make-seed.py` rewrites every address, the gateway's VLAN interfaces, and its firewall sets. The page writes a `CHANGES.md` that lists the changes you must repeat on the switches.
- **Licensing.** The page lists the products your choices need a license for, and records where you keep each key, as a note in the checklist. It does not accept keys, because the scripts do not apply them, and a key typed into a page has no safe place to go. Applying license keys from a secret file is a planned addition.

What is not there yet: flavors other than Ubuntu 24.04 LTS (Red Hat, Debian, the hardened STIG flavors, Windows, and the others are marked planned, and the page shows a proposed support table), Dell VxRail and KVM, renumbering a segment's VLAN, and editing one machine's address. The page refuses nothing silently: a rejected value is marked, the default stays in use, and the reason is listed.

The page keeps its own copy of the manifest so that it works with no server. After you change `lab201-vms.json`, run `python scripts/python/sync_lab_builder.py` to copy it into the page. `validate.sh` fails if the two differ. The page also has a self-test: add `?selftest=1` to its address, and it runs 32 checks of its logic and its controls, and shows the results at the bottom.

### How a machine gets its identity

The script imports the Ubuntu Server LTS cloud image (the OVA from Canonical, checked against Canonical's `SHA256SUMS`). A cloud image has no users and no network settings of its own. It looks for a **NoCloud** data source, which is a CD-ROM with the volume label `cidata` holding three files: `user-data` (the user, the packages, a few files), `meta-data` (the instance ID and hostname), and `network-config` (netplan version 2). The script attaches one such ISO to each machine, so the first boot finishes the setup with no one at the console.

Each network adapter gets a fixed MAC address, `00:50:56:2d:<machine number>:<adapter number>`, which sits in the range ESXi allows for manually assigned addresses. The `network-config` file matches adapters by that MAC address, so the guest's interface names never matter, and the same seed works on every platform in this volume.

### The network model

ESXi has two ways to carry VLANs. With **virtual switch tagging (VST)**, a port group has one VLAN ID and the switch adds and removes the tag, so the guest sees untagged frames. With **virtual guest tagging (VGT)**, the port group has VLAN ID 4095 and the guest sees every tag. The script uses VST for every machine except `gw-201`, and VGT for the gateway's two trunk adapters.

Chapter 999 shows two trunks, T1 to `sw-648f-1` and T2 to `sw-2048f-1`, and a gateway that holds `.1` on every segment. An ESXi virtual switch cannot join two uplinks into one Layer 2 network, because it never forwards frames from one uplink to another. So the script creates one virtual switch for each trunk, `vSwitch-lab201-t1` and `vSwitch-lab201-t2`, and `gw-201` joins them: its `network-config` creates a Linux bridge, `br-trunk`, from its two trunk adapters and puts the VLAN interfaces (`vlan10`, `vlan20`, and so on) on the bridge. Every `.1` address then exists once and answers on both trunks.

A bridge inside a guest sees frames whose source MAC address is not its own. ESXi rejects those unless the port group allows them, so the script sets **promiscuous mode, forged transmits, and MAC address changes** to *accept* on the two trunk virtual switches, and nowhere else.

### ESXi 7, 8, and 9

The same script runs against all three. The differences it handles, and the ones it cannot, are these.

| Item | ESXi 7.0 | ESXi 8.0 | ESXi 9.0 |
| --- | --- | --- | --- |
| Virtual hardware version the script sets | `vmx-19` (7.0 U2 and later; `vmx-17` on older builds) | `vmx-20` (8.0 and U1), `vmx-21` (8.0 U2 and U3) | `vmx-22` |
| Support status | End of general support was 2 October 2025, so it receives no new fixes | Supported | Current release (general availability June 2025) |
| Free license | Broadcom's free-hypervisor article does not cover ESXi 7 | ESXi 8.0 U3e returned as a free hypervisor (2025); its license makes the API read-only | None. Sources report no free ESXi 9, and vSphere 9 is sold only inside vSphere Foundation and Cloud Foundation |
| `-VsphereVersion` check | The host must report `7.*` | The host must report `8.*` | The host must report `9.*` |
| PowerCLI | 13.3 | 13.3 | The release that supports vSphere 9 (Broadcom now calls the product VCF PowerCLI) |

Hardware version 22 runs only on ESXi 9.0. Pass `-HardwareVersion` to override the choice, for example to keep machines at `vmx-19` so an ESXi 7 host can still run them. A machine at a higher hardware version does not start on a host that does not support it.

**The license decides whether this script can work at all.** The free ESXi license allows only read-only API access. Broadcom's article on the free 8.0 U3e hypervisor says API use for host management "is not supported" and may return read-only information. PowerCLI makes its changes through that API, so on a free license the script stops at the first change with the message "Current license or ESXi version prohibits execution of the requested operation," which the script turns into a plain explanation. Use an evaluation license, a paid license, or a program license you hold. Otherwise follow the manifest by hand in the host client, or use [Chapter 12](12-proxmox-ve-lab-virtual-machine-automation.md) or [Chapter 11](11-vmware-workstation-pro-lab-virtual-machine-automation.md).

## Design Considerations

- **One import for each machine.** A standalone ESXi host cannot clone a virtual machine through PowerCLI (cloning is a vCenter feature), so the script imports the OVA once for each machine. It downloads the OVA once and reuses the local copy, but ESXi still receives about 600 MB twelve times. [Chapter 10](10-vcenter-7-8-and-9-lab-virtual-machine-automation.md) imports it once and clones.
- **Uplinks are yours to name.** A network without `-Trunk1Nic`, `-Trunk2Nic`, `-OobNic`, or `-WanNic` becomes an internal-only virtual switch and the script warns. That is useful for a dry run with no hardware switches, because the machines still start and cloud-init still runs on any network that has an uplink.
- **Do not move the management uplink.** Give each network a spare physical NIC. Taking `vmnic0` away from the management virtual switch cuts off the host.
- **Thin disks.** The script imports with thin provisioning, so the 248 GB maximum is not allocated up front. A datastore that cannot hold the maximum can still run the lab until the guests fill their disks.
- **Idempotence.** A machine that already exists is skipped, and switches and port groups are created only if missing. Re-run the script after a failure and it carries on.
- **Packages need the build adapter.** Machines such as `rtr-peer-1` have no route to the internet through `gw-201`, so every machine gets the build adapter instead of relying on masquerading. Chapter 999 offers masquerading as an option and this avoids it. The cost is that, until you remove the adapters, every lab machine can reach the internet.
- **Secrets.** The manifest holds no passwords. The admin user (`labadmin`) has key-based SSH and passwordless `sudo`, and the guest password is locked. To also allow a console password, set the environment variable `LAB201_ADMIN_PASSWORD_HASH` to a crypt hash (`openssl passwd -6`) before you run the script.

## Implementation and Automation

### What the script does, in order

1. Loads PowerCLI, connects to the host, and checks that its version matches `-VsphereVersion`.
2. Chooses the virtual hardware version for the host.
3. Creates a virtual switch for each network, sets the trunk security policy, and creates a port group for each network and VLAN combination in the manifest. Names follow `lab201-t1-v10` for VLAN 10 on trunk T1 and `lab201-t1-trunk` for a gateway trunk.
4. Downloads the OVA if it is not in `work/` and checks its SHA-256 sum.
5. Renders a seed ISO for each machine with `make-seed.py`, using `--guest-agent vmware` (the machines get `open-vm-tools`) and `--tagging hypervisor`.
6. For each machine: imports the OVA under the machine's name, sets the vCPU count, memory, guest OS (`ubuntu64Guest`), and hardware version, grows the disk, replaces the network adapters with VMXNET 3 adapters that have the manifest's MAC addresses, uploads the seed ISO to `lab201-seeds/` on the datastore, and attaches it.
7. Powers on `gw-201` first, then the rest.

Every action in step 3 and later honors `-WhatIf`.

### Parameters

| Parameter | Meaning |
| --- | --- |
| `-EsxiHost` | Name or address of the host. |
| `-Datastore` | Datastore for the machines and the seed ISOs. |
| `-VsphereVersion` | `7` or `8`. The script refuses a host that reports the other version. |
| `-SshKeyFile` | One or more public key files for `labadmin`. |
| `-Trunk1Nic`, `-Trunk2Nic`, `-OobNic`, `-WanNic` | Physical NICs (for example `vmnic1`) for the four uplinks. |
| `-Action` | `Deploy` (default), `Status`, `RemoveBuildNics`, or `Remove`. |
| `-HardwareVersion` | Override of the virtual hardware version. |
| `-SkipCertificateCheck` | Accept the host's self-signed certificate for this session. Use it only on a lab network. |

## Validation and Troubleshooting

After a deploy, give the machines about three minutes for cloud-init, then check each layer in turn.

| Check | Command | Expected |
| --- | --- | --- |
| All machines exist and run | `.\Deploy-Lab201-Esxi.ps1 -Action Status -EsxiHost <host>` | Twelve machines, `PoweredOn`, with guest addresses once VMware Tools starts |
| Cloud-init finished | On a machine: `cloud-init status --long` | `status: done` |
| Hostname and addresses | `hostnamectl; ip -br addr` | The name and the Chapter 999 addresses (both families) |
| Gateway bridge | On `gw-201`: `bridge link; ip -br addr show type vlan` | `nic2` and `nic3` in `br-trunk`, seven VLAN interfaces with `.1` addresses |
| Forwarding policy | On `gw-201`: `sudo nft list ruleset` | The `inet lab201` table from Lab 999.1 |
| Segment 10 reachable | From `admin-201`: `ping -c2 10.201.10.1` and `ping -c2 fd00:db8:201::a01` | Both answer, once the switch trunk allows VLANs 10 and 20 |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| The script stops with a license message | Free ESXi license | Apply an evaluation or paid license |
| `The host runs ESXi 8.0.3, but -VsphereVersion is 7` | Wrong `-VsphereVersion` | Pass the version the host reports |
| A machine starts but has no hostname or addresses | The seed ISO did not attach, or cloud-init did not find it | Check the CD drive is connected at power-on and labeled `cidata` (`blkid` in the guest) |
| Interface names do not matter, but an address is missing | The MAC address in the manifest and the adapter differ | Compare `ip link` with `Get-NetworkAdapter` output; the manifest MAC formula must match |
| `gw-201` bridge passes no frames | Trunk port group security policy was not applied | Check promiscuous mode, forged transmits, and MAC changes are `Accept` on both trunk switches |
| Packages missing | The build adapter had no DHCP lease | Check the `lab201-wan` uplink and DHCP; `cloud-init` logs are in `/var/log/cloud-init-output.log` |
| The OVA import is very slow | One OVA upload for each machine | Import once, then clone: use [Chapter 10](10-vcenter-7-8-and-9-lab-virtual-machine-automation.md) if you have vCenter |

## Security and Best Practices

- **Use a lab network and a lab account.** The script needs an account that can create switches and machines. Do not run it with the host's `root` account over an untrusted network, and give it a dedicated account where you can.
- **Do not leave the certificate check off.** `-SkipCertificateCheck` makes PowerCLI trust any certificate for the session. It is for a first run against a host that still has its self-signed certificate. Replace the certificate afterwards.
- **Remove the build adapters.** The lab holds test attackers and weak settings by design. Run `-Action RemoveBuildNics` as soon as the packages are installed, so no lab machine can reach the internet. The gateway's uplink is its build adapter, so this also cuts `gw-201` off from the internet. Attach an adapter to `lab201-wan` again, with the MAC address `00:50:56:2d:01:00` so the seed's network settings still match it, when you need to install packages later.
- **Trunk security policy is a deliberate exception.** Promiscuous mode on the two trunk switches lets the gateway see all frames on those switches. Keep other machines off them, which the script does by attaching only the gateway and the VLAN-tagged lab machines.
- **Restrict VLANs on the switch trunks.** `gw-201` bridges T1 and T2, so a frame for a link VLAN (2001 or 2002) on T1 is flooded to T2. Allow only the VLANs each switch needs on each trunk port.
- **Key only.** Keep the private key of `-SshKeyFile` in a password manager or agent. Put no secret in the manifest, in `work/`, or in a seed ISO.
- **Treat `work/` as sensitive.** The seed files hold your public keys and, if you set the password hash, a hash. Delete the folder when you finish.

## References and Knowledge Checks

**References:**

- Broadcom, [VMware ESXi 8.0 Update 3e now available as a Free Hypervisor](https://knowledge.broadcom.com/external/article/399823), for the license and the read-only API.
- Broadcom, VMware Cloud Foundation 9.0 release information and the [StarWind overview of virtual hardware version 22](https://www.starwindsoftware.com/blog/vmware-virtual-hardware-version-22-vsphere-9/), for the vSphere 9 hardware version and its availability only through vSphere Foundation and Cloud Foundation. Confirm both against Broadcom's current pages.
- Broadcom, [End of General Support for vSphere 7.0](https://knowledge.broadcom.com/external/article/415405/end-of-general-support-for-vsphere.html), for the 2 October 2025 date.
- Broadcom, VMware PowerCLI downloads and release notes ([PowerCLI 13.3 release notes](https://docs.vmware.com/en/VMware-PowerCLI/latest/rn/powercli-133-release-notes.html)); the product is now also called VCF PowerCLI.
- Broadcom, VMware Product Interoperability Matrix, to confirm which PowerCLI release supports your ESXi build, and the virtual hardware versions article, to confirm the version numbers above for your build.
- Canonical, [Ubuntu cloud images](https://cloud-images.ubuntu.com/noble/current/), for the OVA and the `SHA256SUMS` file.
- Cloud-init documentation, NoCloud data source and network configuration version 2.
- [Chapter 999](999-shared-lab-infrastructure.md), for the host table, addresses, and baseline.

**Knowledge checks:**

1. Why does `gw-201` need its trunk port groups set to VLAN 4095, while every other machine uses a single VLAN ID?
2. The manifest lists only IPv4 addresses. Where does each machine's IPv6 address come from, and why is that safer than listing both?
3. A host reports `8.0.3` and you run the script with `-VsphereVersion 7`. What happens, and why is the check there?
4. Why is the build adapter removed after the packages are installed, and which command removes it?
5. What would break if you gave all four uplinks to one virtual switch?

## Hands-On Lab

**Prerequisites.** An ESXi 7, 8, or 9 host with a license that allows API writes, a datastore with 250 GB free (less if you accept thin disks filling slowly), up to four spare physical NICs for the uplinks (T1, T2, out-of-band, WAN), a Windows, macOS, or Linux computer with PowerShell 7, PowerCLI, Python 3.8 or later with `pip install pycdlib`, and an SSH key pair (`ssh-keygen -t ed25519`). Switch-side configuration (the trunk ports and VLANs) is Chapter 999, Lab 999.3 and later.

### Lab 9.1: Preview the build

1. Download and unpack the lab-scripts zip. Open PowerShell in the `esxi` folder.
2. Run the script with `-WhatIf` and read every line it prints:

   ```powershell
   .\Deploy-Lab201-Esxi.ps1 -EsxiHost <ESXI_HOST> -Datastore <DATASTORE> -VsphereVersion 8 `
     -SshKeyFile ~\.ssh\id_ed25519.pub -Trunk1Nic vmnic1 -Trunk2Nic vmnic2 -OobNic vmnic3 -WanNic vmnic0 -WhatIf
   ```

**Expected result.** It lists the switches, port groups, and twelve machines it would create, and creates nothing.

### Lab 9.2: Build the lab

1. Run the same command without `-WhatIf`. Enter the host account when asked.
2. Run `-Action Status` and wait until every machine reports a guest address.
3. On `admin-201`, run `cloud-init status --long` and `ip -br addr`.

**Expected result.** Twelve running machines, cloud-init `done`, and every address from the table in Chapter 999.

### Lab 9.3: Remove the build adapters and take the baseline

1. Run `.\Deploy-Lab201-Esxi.ps1 -Action RemoveBuildNics -EsxiHost <ESXI_HOST>`.
2. Confirm that no machine has an adapter on `lab201-wan`. That includes `gw-201`, whose uplink is its build adapter.
3. Take the snapshots Lab 999.6 needs:

   ```powershell
   Get-VM -Name gw-201, svc-*, ca-201, dhcp-201, admin-201, rtr-peer-*, mcast-src-201, static-*, attacker-201 |
     New-Snapshot -Name baseline-201 -Description 'Lab 999.6 baseline'
   ```

**Negative test.** From `static-1`, run `curl -m 5 https://cloud-images.ubuntu.com`. It must fail, because no path to the internet remains.

**Evidence.** The `-Action Status` output, `ip -br addr` from three machines, and the failed `curl`.

### Cleanup

Run `-Action Remove` to delete the machines. Remove the virtual switches and port groups in the host client if you do not need them, and delete `work/`.

## Lab Verification

Complete this sign-off once Labs 9.1 to 9.3 have been run end to end against a real ESXi 7 host and a real ESXi 8 host. Until then the script is unverified. It was written against the PowerCLI documentation and checked for syntax and for the shared seed output, and it has not been run against a host. The virtual hardware version numbers and the interaction of the manual MAC addresses with each ESXi build are the first things to confirm.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the twelve lab machines on a standalone ESXi host from one manifest and one seed tool. The script creates a virtual switch for each trunk, bridges the trunks inside `gw-201`, gives every machine a fixed MAC address and a cloud-init seed, and handles the differences between ESXi 7, 8, and 9 in the virtual hardware version. The free license makes the API read-only, so the script needs a license that allows writes.

- [ ] Can name the twelve machines and the networks each one uses.
- [ ] Can explain why `gw-201` bridges the two trunks and why that needs promiscuous mode.
- [ ] Has run the script with `-WhatIf` and then for real on an ESXi 7 or 8 host.
- [ ] Has removed the build adapters and taken the `baseline-201` snapshots.
- [ ] Can say which hardware version and license apply to ESXi 7 and ESXi 8.
