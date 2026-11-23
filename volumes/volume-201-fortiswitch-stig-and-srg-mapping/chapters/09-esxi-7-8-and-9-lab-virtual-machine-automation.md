# Chapter 09: Automating the Lab Virtual Machines on VMware ESXi 7, 8, and 9

## Learning Objectives

- Name the twelve virtual machines of the Chapter 999 lab, the network each one attaches to, and the cloud-init seed that gives each its hostname, addresses, and packages.
- Build the virtual switches and port groups the lab needs on a standalone ESXi 7, 8, or 9 host, including the trunk port groups that `gw-201` bridges.
- Run `Deploy-Lab201-Esxi.ps1` against an ESXi host, check each machine, remove the build network adapters, and take the `baseline-201` snapshots.
- Say which differences between ESXi 7, 8, and 9 change the script's behavior: the virtual hardware version, the license that allows API writes, and the support status.
- Recognize the cases where the script cannot work (free license, missing uplinks) and what to do instead.

## Theory and Architecture

### What the automation builds

[Chapter 999](999-shared-lab-infrastructure.md) lists the hosts of the shared lab and says they can all be virtual except the two switches. Chapters 09 to 14 turn that list into scripts, one chapter for each place the machines can run. All six chapters read the same manifest and use the same seed tool, so a machine has the same name, the same addresses, and the same packages whichever platform builds it.

| Machine | Role | vCPU | Memory (MB) | Disk (GB) | Networks |
| --- | --- | --- | --- | --- | --- |
| `gw-201` | Gateway and firewall | 2 | 2048 | 20 | wan, oob, T1 trunk, T2 trunk |
| `svc-201a` | RADIUS, syslog, NTP, SNMP manager | 2 | 4096 | 40 | T1 VLAN 2 |
| `svc-201b` | RADIUS, syslog, NTP, collectors, file server | 2 | 4096 | 40 | T1 VLAN 2 |
| `ca-201` | Lab certificate authority | 1 | 1024 | 16 | T1 VLAN 2 |
| `dhcp-201` | DHCP server | 1 | 1024 | 16 | T1 VLANs 2, 5, 6, 8 |
| `admin-201` | Administrator workstation | 2 | 4096 | 40 | T1 VLAN 3 |
| `rtr-peer-1` | Routing peer, AS 65202 | 1 | 1024 | 16 | T1 VLAN 2001, T2 VLAN 2003, segment 12 |
| `rtr-peer-2` | Routing peer, AS 65203 | 1 | 1024 | 16 | T1 VLAN 2002, T2 VLAN 2004 |
| `mcast-src-201` | Multicast source | 1 | 512 | 8 | segment 12 |
| `static-1`, `static-2` | Statically addressed hosts | 1 each | 512 each | 8 each | T1 VLAN 7 |
| `attacker-201` | Spoofing and flooding test host | 2 | 2048 | 20 | T1 VLAN 7 |

Every machine also has a **build** network adapter on the `lab201-wan` network, first in its adapter list. It gets an address by DHCP so that cloud-init can install packages, and it is removed when the build is done. The twelve machines need 17 vCPUs, 21.5 GiB of memory, and up to 248 GB of thin-provisioned disk.

Four items in Chapter 999 are not built by the scripts. `fgt-201` needs a FortiGate-VM image that Fortinet supplies under license, `og-201` is the console server of [Chapter 08](08-opengear-im7216-console-server-and-optional-console-lab.md), `oob-admin-201` is a laptop, and `vx-host-a` and `vx-host-b` plug into switch ports. Chapter 999 lets `gw-201` be a Linux router, and so do the scripts.

### The shared files

The scripts are in one folder and are downloadable as a unit. The folder is `lab-scripts` in [Volume CMI](../../volume-901-lab-selector/README.md), which also holds the Lab Selector. It was in this volume until 2026-11-20.

| File | Purpose |
| --- | --- |
| `common/lab201-vms.json` | The manifest: networks, machines, sizes, adapters, and IPv4 addresses. The IPv6 address of each IPv4 address is derived (`fd00:db8:201::` plus the third and fourth octets in hexadecimal), so the two families cannot drift apart. |
| `common/make-seed.py` | Renders the cloud-init files for each machine and, with `--iso`, writes a seed ISO labeled `cidata`. |
| `selector/lab-selector.html` | The [Lab Selector](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html), a page that runs in your browser. It writes a manifest for your choices, the commands for each platform, and a checklist, and downloads them as a zip with the lab walkthroughs. |
| `common/lab-catalog.json` | The lab kinds and the lab sets that the Lab Selector offers, with the lab chapters of each set. |
| `diagrams/lab-topology.svg` and `.png` | The Chapter 999 network diagram, copied into the zip when the site is built, so the scripts and the picture of what they build travel together. |
| `common/flavors.json` | The Linux flavors, the package names for each family, and which machine types each flavor can run. |
| `common/resolve-image.py` | Finds, downloads, and checks the cloud image for a flavor. |
| `esxi/Deploy-Lab201-Esxi.ps1` | This chapter's script. |
| `kvm/deploy-lab201-kvm.sh` | The KVM and libvirt script ([Chapter 14](14-kvm-libvirt-lab-virtual-machine-automation.md)). |

[Download the whole set as one zip](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/volume-901-lab-selector-lab-scripts.zip), or fetch single files from the [lab-scripts folder](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/common/lab201-vms.json). A `SHA256SUMS` file in the folder lists the checksum of every script.

### The Lab Selector

The [Lab Selector](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html) of [Volume CMI](../../volume-901-lab-selector/README.md) plans a build of this lab. It is one HTML page that runs in your browser. You choose the labs to run, a platform and its version, and what to build. It then writes a copy of the manifest that holds your changes, the commands to run for your platform (a readiness check, a preview, the build, the wait for the first boot, the removal of the build adapters, the baseline snapshots, and the return to the baseline between labs), a checklist of what the scripts cannot do, and a zip with the script, the seed tool, and the lab walkthroughs. A link can name the labs that the page starts with: [Lab Selector with the FortiSwitch labs ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortiswitch).

Until 2026-11-20 the page was the Lab Builder of this volume. It now offers the labs of more than one volume, so the page, its data, and the scripts of Chapters 09 to 14 are in the `lab-scripts` folder of Volume CMI. [Volume CMI, Chapter 01](../../volume-901-lab-selector/chapters/01-the-lab-selector.md) describes every option of the page, and its [Chapter 02](../../volume-901-lab-selector/chapters/02-lab-data-and-how-to-add-a-lab-set.md) describes the data. An old link to the Lab Builder opens the Lab Selector.

Every flavor is now built or buildable. Windows, Linux Mint, and Tiny Core install from an ISO you supply (see *ISO-based flavors* below), and a flavor's own minimum size can raise a machine's default size, as Windows 11 raises a small host to 4 GB and 64 GB. A cloud image also sets the smallest disk, because a disk cannot be smaller than its image. The Rocky Linux and AlmaLinux images are 10 GB and the Fedora image is 5 GB (measured), so those flavors raise a smaller disk to that size, and the Red Hat flavors use 10 GB too (not measured). The three smallest machines have 8 GB disks, so Rocky Linux or AlmaLinux raises them to 10 GB. The scripts do not shrink a disk either: if a manifest edited by hand asks for less than the image holds, the machine keeps the size of the image and the script says so.

### Linux flavors

Each machine can use its own Linux flavor. `flavors.json` lists them, and the manifest names a machine's flavor in `flavor` (or sets `default_flavor` for all). The seed tool translates the package names for the flavor's family: `apt` families use the manifest's Ubuntu names, and `dnf` families use their own (`net-snmp-utils` for `snmp`, `tftp-server` for `tftpd-hpa`, `kea` for `kea-dhcp4-server`, and so on). A package a flavor does not have is left out, and the seed tool says so. On Rocky Linux and AlmaLinux the seed enables EPEL first for the tools that live there.

| Flavor | Status | Built so far | Image | Notes |
| --- | --- | --- | --- | --- |
| Ubuntu 24.04 LTS | Ready (the default) | All twelve machines, on Proxmox VE. All the lab machines of one Lab Selector zip, on Workstation Pro | Published, with an OVA for VMware | The flavor every chapter was written against |
| Ubuntu 26.04 LTS | Experimental | `ca-201` and `svc-201b`, on Proxmox VE | Published, with an OVA | |
| Debian 13 | Experimental | `ca-201` and `svc-201b`, on Proxmox VE | Published qcow2 | |
| Rocky Linux 10, AlmaLinux 10 | Experimental | `ca-201` and `svc-201b` from each, on Proxmox VE | Published qcow2 | EPEL for `nfdump`, `hping3`, `frr`, and a few others |
| Fedora Cloud 43 | Experimental | `ca-201` and `svc-201b`, on Proxmox VE | Published qcow2 (the file name is found by pattern) | |
| Red Hat Enterprise Linux 10 | Experimental | Nothing | You download it (subscription needed) | Registered with an activation key and organization, if you give them |
| Ubuntu 24.04 LTS, DoW STIG hardened | Experimental | One machine, on Proxmox VE, without an Ubuntu Pro token, so it was not hardened | The Ubuntu 24.04 image | Ubuntu Pro token; the seed runs the Ubuntu Security Guide's `disa_stig` fix and reboots once |
| RHEL 10, DoW STIG hardened | Experimental | Nothing | The RHEL 10 image | The seed runs `oscap` with the `stig` profile and reboots once |
| Windows 11, Windows Server 2022 and 2025 | Experimental | Nothing | An ISO you supply | Unattended install on Proxmox VE, ESXi, vCenter, and VxRail |
| Linux Mint 22, Tiny Core Linux | Experimental | Nothing | An ISO you supply | A person runs part of the install |

**Experimental** means the files are generated and pass their checks (valid YAML or XML, the right packages, the right groups, scripts that parse), but the flavor has not been built as a whole lab. The **Built so far** column names the machines that have been built from it, and *Tested on Proxmox VE* below says what was checked on them. Expect fixes on the first real build of any other machine, and on any other platform. The ratings of which machine types a flavor can run (`roles` in `flavors.json`) are proposals. The seed tool refuses a machine type a flavor is rated `n` for, such as a hardened flavor for `attacker-201`.

### ISO-based flavors

Windows 11, Windows Server 2022 and 2025, Linux Mint 22, and Tiny Core Linux have no cloud image, so they install from an ISO you supply. The platform script makes an empty machine, attaches the install ISO, and attaches a second CD (labeled `LAB201`) that `make-seed.py` fills for the flavor. They are available on Proxmox VE, ESXi, vCenter, and VxRail, where the hypervisor tags VLANs: a Windows guest cannot tag the trunks itself, so Workstation, KVM, and WSL do not offer them.

| Flavor | What the second CD holds | What you still do |
| --- | --- | --- |
| Windows 11 | `autounattend.xml` and `lab201-setup.ps1` | Nothing during the install. Remove both CDs afterwards |
| Windows Server 2022 and 2025 | The same | The same |
| Linux Mint 22 | `lab201-firstlogin.sh` | Run the Mint installer, then run the script as `root` |
| Tiny Core Linux | `lab201-tc.sh` | Boot the ISO, mount the second CD, and run the script |

**Windows.** The answer file partitions the disk, picks the image by index (1 for Windows 11 and 2 for Windows Server, which is usually Standard with Desktop Experience on Microsoft's ISOs; check yours), sets the computer name, creates `labadmin` and the built-in administrator with the password from `LAB201_WINDOWS_ADMIN_PASSWORD`, and logs on once to run `lab201-setup.ps1`. That script sets each adapter's addresses by MAC address, allows ping, installs OpenSSH Server with your key, and, on Windows Server, installs the role that stands in for the lab service: Certificate Services as a standalone root CA for `ca-201`, and the DHCP role with a scope for each user segment for `dhcp-201`. The product key comes from the `windows` section of the license file. Microsoft's evaluation ISOs need none (90 days for Windows 11 Enterprise, 180 days for Windows Server). Windows 11 is installed with the TPM, Secure Boot, RAM, and CPU checks bypassed through registry values in the answer file, so no virtual TPM is needed. Microsoft does not support that. The disk uses a SATA controller and the adapters use the Intel e1000e model, because Windows has drivers for both, so no driver disk is needed. The admin password sits in the answer file, so remove the CD after the install.

**Linux Mint and Tiny Core.** Mint's installer and Tiny Core's boot cannot be driven without a person, so the second CD holds a script that does the rest: set the name, the addresses (Mint with NetworkManager, Tiny Core with `ip`), your key and the tools. Tiny Core runs from memory, so save its changes with `filetool.sh -b` if you want them to last.

The platform scripts take the ISO paths with `-IsoImages @{ 'win-2025' = '[datastore1] iso/Server2025.iso' }` (ESXi and vCenter, a path on a datastore) or `--iso win-2025=local:iso/Server2025.iso` (Proxmox VE, a storage volume). These flavors have the largest unknowns. Nothing here has installed on a real hypervisor, so expect first-run fixes, especially in the answer file's image selection and the first-logon timing.

**Tested on Proxmox VE.** One machine (`ca-201`) was built from each of Ubuntu 24.04 and 26.04, Debian 13, Rocky 10, AlmaLinux 10, and Fedora 43 on Proxmox VE 9.2.9. Each reached `cloud-init status: done` with its hostname, `labadmin`, both lab addresses, the default routes, `openssl`, SSH, and the guest agent. The services host `svc-201b`, which installs the most packages, was then built from the same six flavors. On all six, cloud-init finished, the lab addresses and routes were in place, and FreeRADIUS, rsyslog, chrony, and TFTP ran. The Red Hat family and Fedora needed their services started and FreeRADIUS's certificates generated, and `sflowtool` is not in the Ubuntu 24.04 or Debian 13 repositories, so the scripts now compile it from source (tested on all six flavors). A Rocky 10 machine also kept its addresses and default routes across a reboot. All 12 default machines were also built together on Ubuntu 24.04. Every one reached `cloud-init status: done` with its lab addresses, VLAN interfaces, and routes, and the gateway, routing peers, and DHCP, multicast, static, and test hosts had their packages and services. The gateway and a routing peer kept their addresses, VLAN interfaces, and loopbacks across a reboot. The scripts install and address the machines but leave each service unconfigured: Kea has no subnets, BGP is off on the routing peers, and `snmptrapd` is not running until a lab configures it. Traffic between VLANs was not tested, because the test bridge carried only VLAN 99. The Ubuntu STIG flavor was built without an Ubuntu Pro token, so it booted, rebooted once, and took a password login but was not hardened; the Red Hat flavors with a subscription, the Windows, Linux Mint, and Tiny Core flavors, and the ESXi, vCenter, VxRail, KVM, and WSL scripts have not been run. The Workstation script has built and started all the lab machines, with Ubuntu 24.04 as their flavor, on one Windows computer with Workstation Pro 26 ([Chapter 11](11-vmware-workstation-pro-lab-virtual-machine-automation.md)). The actions added later (`check`, `status --wait`, `snapshot`, and `restore`) were run on Proxmox VE 9.2 against all twelve machines, eleven on Ubuntu 24.04 and one on Rocky Linux 10. The status read `ok` from each Ubuntu machine through the guest agent, and `unknown` from the Rocky machine, whose agent runs no commands. A service stopped by hand showed as `failed`, and `restore` returned the machine to its snapshot. In a further run with two machines, `snapshot` refused while the build NICs were still there, and after `remove-build-nics`, `snapshot`, and `restore` they were still gone. On VMware Workstation, ESXi, vCenter, and KVM those actions have not been run against machines. Their readiness checks ran on one Windows computer without PowerCLI under PowerShell 7 and without WSL, and the ESXi and vCenter checks also ran under Windows PowerShell 5.1 with PowerCLI as far as a failed login to a host that does not exist. Findings shape the catalog. The Red Hat 10 family (Rocky 10, AlmaLinux 10, RHEL 10) needs a CPU that supports the x86-64-v3 level, so the Proxmox script gives those machines `x86-64-v3` instead of the default `x86-64-v2-AES`; on an older CPU they stop silently after GRUB. The Red Hat family and Fedora also render the network with NetworkManager, which cannot take the seed's IPv4 and IPv6 default routes, so their routes are set with `nmcli` on first boot.

**Hardened flavors.** The STIG forbids passwordless `sudo`, so a hardened machine asks for a password, and the seed tool refuses to build one unless `LAB201_ADMIN_PASSWORD_HASH` is set (make a hash with `openssl passwd -6`). The machine reboots once after hardening, and `/root/LAB201-STIG-NOTES.txt` lists the findings the lab accepts because it needs the behavior: IP forwarding on the gateway and peers, and the services on the service hosts. Whether Ubuntu's `disa_stig` profile has shipped for 24.04 was not confirmed.

**Images on each platform.** Proxmox VE and KVM use the qcow2 images directly, and `resolve-image.py` downloads and checks them. The VMware platforms import OVA files. Ubuntu publishes them, and the scripts download them. For any other flavor, convert its qcow2 image to a stream-optimized VMDK with `qemu-img` and wrap it in an OVA, then pass the path with `-FlavorImages @{ 'debian-13' = 'C:\images\debian.ova' }`. The script stops with that message if a flavor has no OVA. WSL builds Ubuntu 24.04 only.

### License keys

The scripts that can apply a license read it from a JSON file you keep on your own computer, passed with `-LicenseFile` (PowerShell) or `--license-file` (Bash). The Lab Selector writes a template, `licenses.example.json`, with empty values for the products your choices need. Copy it to `licenses.local.json`, fill it in, and keep it out of the repository (the name is in `.gitignore`).

| Section of the file | Applied by | What it does |
| --- | --- | --- |
| `redhat` (`activation_key`, `org`) | The seed tool, on every platform except WSL | Registers a Red Hat machine on its first boot (cloud-init's subscription module) |
| `ubuntu_pro` (`token`) | The seed tool | Attaches Ubuntu Pro on the hardened Ubuntu machines |
| `windows` (`product_key`) | The seed tool, for the Windows flavors | Written into the answer file. Leave it out for an evaluation ISO |
| `vsphere` (`esxi`, `vcenter`) | The ESXi and vCenter scripts | Adds the license and assigns it to the host and to vCenter |
| `proxmox` (`subscription_key`) | The Proxmox script | Runs `pvesubscription set` |

A key is written only into the seed of a machine that needs it, never printed, and never copied into the manifest or the zip. Licensing for Dell VxRail 9 is done in VCF Operations, and the FortiSwitch licenses are for hardware, so neither is applied by a script. Workstation Pro needs no key. The vSphere license calls were written from the vSphere API and have not been run against a host. A preview (`-WhatIf` or `--dry-run`) applies no license key to a host.

### How a machine gets its identity

The script imports the Ubuntu Server LTS cloud image (the OVA from Canonical, checked against Canonical's `SHA256SUMS`). A cloud image has no users and no network settings of its own. It looks for a **NoCloud** data source, which is a CD-ROM with the volume label `cidata` holding three files: `user-data` (the user, the packages, a few files), `meta-data` (the instance ID and hostname), and `network-config` (netplan version 2). The script attaches one such ISO to each machine, so the first boot finishes the setup with no one at the console.

Each network adapter gets a fixed MAC address, `00:50:56:2d:<machine number>:<adapter number>`, which sits in the range ESXi allows for manually assigned addresses. The `network-config` file matches adapters by that MAC address, so the guest's interface names never matter, and the same seed works on every platform in this volume.

### The network model

ESXi has two ways to carry VLANs. With **virtual switch tagging (VST)**, a port group has one VLAN ID and the switch adds and removes the tag, so the guest sees untagged frames. With **virtual guest tagging (VGT)**, the port group has VLAN ID 4095 and the guest sees every tag. The script uses VST for every machine except `gw-201`, and VGT for the gateway's two trunk adapters.

Chapter 999 shows two trunks, T1 to `sw-648f-1` and T2 to `sw-2048f-1`, and a gateway that holds `.1` on every segment. An ESXi virtual switch cannot join two uplinks into one Layer 2 network, because it never forwards frames from one uplink to another. So the script creates one virtual switch for each trunk, `vSwitch-lab201-t1` and `vSwitch-lab201-t2`, and `gw-201` joins them: its `network-config` creates a Linux bridge, `br-trunk`, from its two trunk adapters and puts the VLAN interfaces (`vlan2`, `vlan3`, and so on) on the bridge. Every `.1` address then exists once and answers on both trunks.

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
3. Creates a virtual switch for each network, sets the trunk security policy, and creates a port group for each network and VLAN combination in the manifest. Names follow `lab201-t1-v2` for VLAN 2 on trunk T1 and `lab201-t1-trunk` for a gateway trunk.
4. Downloads the OVA if it is not in `work/` and checks its SHA-256 sum.
5. Renders a seed ISO for each machine with `make-seed.py`, using `--guest-agent vmware` (the machines get `open-vm-tools`) and `--tagging hypervisor`.
6. For each machine: imports the OVA under the machine's name, sets the vCPU count, memory, guest OS (`ubuntu64Guest`), and hardware version, grows the disk, replaces the network adapters with VMXNET 3 adapters that have the manifest's MAC addresses, uploads the seed ISO to `lab201-seeds/` on the datastore, and attaches it.
7. Powers on `gw-201` first, then the rest.

Every action in step 3 and later honors `-WhatIf`. A preview downloads no image and applies no license key. In place of step 4 it names the image file that the build fetches, and it names the products whose license key the build applies. Step 5 still runs, so a preview leaves the seed ISOs in `work/seeds`.

### Parameters

| Parameter | Meaning |
| --- | --- |
| `-EsxiHost` | Name or address of the host. |
| `-Datastore` | Datastore for the machines and the seed ISOs. |
| `-VsphereVersion` | `7` or `8`. The script refuses a host that reports the other version. |
| `-SshKeyFile` | One or more public key files for `labadmin`. |
| `-Trunk1Nic`, `-Trunk2Nic`, `-OobNic`, `-WanNic` | Physical NICs (for example `vmnic1`) for the four uplinks. |
| `-Action` | `Deploy` (default), `Check`, `Status`, `RemoveBuildNics`, `Snapshot`, `Restore`, or `Remove`. `Check` tests what a deploy needs and changes nothing. `Snapshot` takes the baseline snapshot of every machine, and refuses while a machine still has its build adapter. `Restore` returns every machine to that snapshot and powers it on. |
| `-Wait`, `-WaitMinutes` | With `-Action Status`: keep checking until every machine reports that its first boot has finished, for at most `-WaitMinutes` (30 by default). |
| `-SnapshotName` | The snapshot that `Snapshot` and `Restore` use. The default is `baseline-201`. |
| `-HardwareVersion` | Override of the virtual hardware version. |
| `-SkipCertificateCheck` | Accept the host's self-signed certificate for this session. Use it only on a lab network. |
| `-FlavorImages` | A hashtable of OVA paths for flavors that publish no OVA (`@{ 'debian-13' = 'C:\images\debian.ova' }`). |
| `-LicenseFile` | The JSON license file (see *License keys*). |
| `-IsoImages` | A hashtable of install ISO paths on a datastore, for the ISO-based flavors (`@{ 'win-2025' = '[datastore1] iso/Server2025.iso' }`). |

## Validation and Troubleshooting

After a deploy, give the machines about three minutes for cloud-init, then check each layer in turn.

| Check | Command | Expected |
| --- | --- | --- |
| All machines exist and run | `.\Deploy-Lab201-Esxi.ps1 -Action Status -EsxiHost <host>` | Twelve machines, `PoweredOn`, with guest addresses once VMware Tools starts |
| The first boot finished | The same command with `-Wait` | `ok` in the Build column of every machine. `failed` names a missing package or a lab service that does not run |
| Cloud-init finished | On a machine: `lab201-status`, then `cloud-init status --long` | A line that starts `lab201 ok`, and `status: done` |
| Hostname and addresses | `hostnamectl; ip -br addr` | The name and the Chapter 999 addresses (both families) |
| Gateway bridge | On `gw-201`: `bridge link; ip -br addr show type vlan` | `nic2` and `nic3` in `br-trunk`, seven VLAN interfaces with `.1` addresses |
| Forwarding policy | On `gw-201`: `sudo nft list ruleset` | The `inet lab201` table from Lab 999.1 |
| Segment 2 reachable | From `admin-201`: `ping -c2 10.200.2.1` and `ping -c2 fd00:db8:201::201` | Both answer, once the switch trunk allows VLANs 2 and 3 |

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
- **Remove the build adapters.** The lab holds test attackers and weak settings by design. Run `-Action RemoveBuildNics` as soon as the packages are installed, so no lab machine can reach the internet. The gateway's uplink is its build adapter, so this also cuts `gw-201` off from the internet. Attach an adapter to `lab201-wan` again, with the MAC address `00:50:56:2d:01:00` so the seed's network settings still match it, when you need to install packages later. A manifest with `uplink` (the **Uplink** box of the Lab Selector) keeps that adapter of `gw-201` as the way to an external firewall: `RemoveBuildNics` leaves it, and `Snapshot` does not count it. `gw-201` then forwards to it only the traffic of the machines that the manifest lists.
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

1. Download and unpack the lab-scripts zip. Open PowerShell in the `esxi` folder. Windows blocks downloaded PowerShell scripts by default. If PowerShell says that running scripts is disabled, or that the file is not digitally signed, run the script with `powershell -ExecutionPolicy Bypass -File` and the script name (`pwsh` for PowerShell 7), or run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force` to allow scripts for the rest of the window. Both apply to one PowerShell process only, and neither works where Group Policy sets the execution policy. The `README.md` in the lab-scripts zip has the details. If you want to change machine names or sizes, leave machines out, or move the lab to another address block, open the Lab Selector first (`selector/lab-selector.html` on the published site), choose ESXi and your version, and download its zip. It gives you a manifest to put in `common/` and the command to use in the next step.
2. Run the readiness check. It changes nothing. It tests Python, the SSH key, PowerCLI, and the manifest on your computer, then logs in to the host and tests its version, the datastore, the uplinks, and memory:

   ```powershell
   .\Deploy-Lab201-Esxi.ps1 -Action Check -EsxiHost <ESXI_HOST> -Datastore <DATASTORE> -VsphereVersion 8 `
     -SshKeyFile ~\.ssh\id_ed25519.pub -Trunk1Nic vmnic1 -Trunk2Nic vmnic2 -OobNic vmnic3 -WanNic vmnic0
   ```

3. Run the script with `-WhatIf` and read every line it prints:

   ```powershell
   .\Deploy-Lab201-Esxi.ps1 -EsxiHost <ESXI_HOST> -Datastore <DATASTORE> -VsphereVersion 8 `
     -SshKeyFile ~\.ssh\id_ed25519.pub -Trunk1Nic vmnic1 -Trunk2Nic vmnic2 -OobNic vmnic3 -WanNic vmnic0 -WhatIf
   ```

**Expected result.** The check ends with `Ready`, or names what to fix. The preview lists the switches, port groups, and twelve machines it would create, and creates nothing. It downloads nothing, and it names the image file that the build fetches.

### Lab 9.2: Build the lab

1. Run the same command without `-WhatIf`. Enter the host account when asked.
2. Run `.\Deploy-Lab201-Esxi.ps1 -Action Status -Wait -EsxiHost <ESXI_HOST>`. It ends when every machine reports that its first boot has finished. Each machine hands that state to the host through VMware Tools about once a minute. If none reports within six minutes, the wait stops and says so: then check a machine by hand in the next step.
3. On `admin-201`, run `lab201-status`, `cloud-init status --long`, and `ip -br addr`.

**Expected result.** Twelve running machines, `ok` for each in the Build column, cloud-init `done`, and every address from the table in Chapter 999.

### Lab 9.3: Remove the build adapters and take the baseline

1. Run `.\Deploy-Lab201-Esxi.ps1 -Action RemoveBuildNics -EsxiHost <ESXI_HOST>`.
2. Confirm that no machine has an adapter on `lab201-wan`. That includes `gw-201`, whose uplink is its build adapter. With `uplink` in the manifest, `gw-201` alone keeps its adapter there.
3. Take the snapshots Lab 999.6 needs. The script refuses, and names the machines, if one of them still has its build adapter:

   ```powershell
   .\Deploy-Lab201-Esxi.ps1 -Action Snapshot -EsxiHost <ESXI_HOST>
   ```

4. Between labs, return every machine to that snapshot. It discards what changed on the machines since the snapshot and powers them on, the gateway first:

   ```powershell
   .\Deploy-Lab201-Esxi.ps1 -Action Restore -EsxiHost <ESXI_HOST>
   ```

**Negative test.** From `static-1`, run `curl -m 5 https://cloud-images.ubuntu.com`. It must fail, because no path to the internet remains.

**Evidence.** The `-Action Status` output, `ip -br addr` from three machines, and the failed `curl`.

### Cleanup

Run `-Action Remove` to delete the machines. Remove the virtual switches and port groups in the host client if you do not need them, and delete `work/`.

## Lab Verification

Complete this sign-off once Labs 9.1 to 9.3 have been run end to end against a real ESXi 7 host and a real ESXi 8 host. Until then the script is unverified. It was written against the PowerCLI documentation and checked for syntax and for the shared seed output, and it has not been run against a host. The virtual hardware version numbers and the interaction of the manual MAC addresses with each ESXi build are the first things to confirm. Of the `Check`, `Status -Wait`, `Snapshot`, and `Restore` actions, only `Check` has been run: its local tests, and then, under Windows PowerShell 5.1 with PowerCLI, as far as a failed login to a host that does not exist. Whether the host shows the build state that a machine hands to it (`guestinfo.lab201`) is the first thing to confirm for `Status -Wait`.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the twelve lab machines on a standalone ESXi host from one manifest and one seed tool. The script creates a virtual switch for each trunk, bridges the trunks inside `gw-201`, gives every machine a fixed MAC address and a cloud-init seed, and handles the differences between ESXi 7, 8, and 9 in the virtual hardware version. The free license makes the API read-only, so the script needs a license that allows writes.

- [ ] Can name the twelve machines and the networks each one uses.
- [ ] Can explain why `gw-201` bridges the two trunks and why that needs promiscuous mode.
- [ ] Has run the script with `-WhatIf` and then for real on an ESXi 7, 8, or 9 host.
- [ ] Has removed the build adapters and taken the `baseline-201` snapshots.
- [ ] Can say which hardware version and license apply to ESXi 7, 8, and 9.
