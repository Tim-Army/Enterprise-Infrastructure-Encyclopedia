# Chapter 13: Automating the Lab Service Hosts in WSL

## Learning Objectives

- Explain why Windows Subsystem for Linux (WSL) is not a hypervisor for this lab, and name what it can and cannot build.
- Describe the shared kernel and network namespace of WSL 2 distributions, and how the lab's addresses fit on top of them.
- Run `Deploy-Lab201-Wsl.ps1` to create the eight service-side hosts as distributions, and check each one.
- Reach the lab addresses from Windows, and know what stays out of reach (hardware switches).
- Choose between WSL and the other chapters' platforms for a given lab.

## Theory and Architecture

### WSL does not make virtual machines

The other chapters create a virtual machine for each lab host. WSL 2 does not. It runs **one** lightweight virtual machine, and every Linux distribution you install is a separate root file system and set of processes inside that machine. All distributions therefore share one Linux kernel and one network namespace: an address added in one distribution exists in all of them, and the network interfaces, routing table, and firewall are common.

This rules out most of the lab and keeps a useful part.

| Lab host | Built by this chapter? | Why |
| --- | --- | --- |
| `svc-201a`, `svc-201b` | Yes | Services that bind to their own addresses |
| `ca-201`, `dhcp-201` | Yes | Same |
| `admin-201`, `static-1`, `static-2`, `attacker-201` | Yes | Command-line tools and test hosts |
| `gw-201` | No | A gateway needs separate interfaces and a firewall of its own, and the shared namespace has neither |
| `rtr-peer-1`, `rtr-peer-2`, `mcast-src-201` | No | They need routed links to the hardware switches, and WSL cannot carry an 802.1Q trunk to a switch |

The manifest marks the eight built hosts with `"wsl": true`. Everything else in [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md)'s machine table needs another platform.

### What it is good for

- **Rehearsal.** Build the service hosts (Lab 999.2) on a Windows laptop with no hypervisor, configure RADIUS, syslog, NTP, and DHCP, and test the configurations before you build the real machines. The same package list and the same addresses apply.
- **Tooling.** `admin-201` and `attacker-201` give you Linux tools beside Windows.
- **Low cost.** There is no hypervisor to install, and the distributions use memory only as their processes need it.

It is not a way to test the switches. A hardware switch cannot reach these addresses, and no VLAN tag leaves the computer.

### How the lab addresses are placed

Each host's `lab201-net.sh` script (written by `make-seed.py --wsl`) creates one **dummy** interface, `lab201`, and a VLAN interface on it for each VLAN the host uses (`lab201.10`, `lab201.40`, and so on). It then adds the host's IPv4 and IPv6 addresses from the manifest to the right VLAN interface. The script runs again each time a distribution starts, through the `[boot] command` setting in `/etc/wsl.conf`, and is safe to repeat, because WSL forgets interface changes when its virtual machine stops.

Because the namespace is shared, every distribution sees every host's addresses, and a service that listens on all addresses (`0.0.0.0`) answers on all of them. To keep the hosts distinct, configure each service to listen only on its own address (`radius-201a` on `10.201.10.10`, and so on). If the WSL kernel lacks 802.1Q support, the script puts the addresses on the dummy interface itself and the VLAN structure is lost, which does not matter for service testing.

### Requirements

WSL 2 on Windows 11 (or a current Windows 10), updated with `wsl --update`. systemd support (`systemd=true`) and the `[boot] command` setting need a recent WSL release, which an update provides. The manifest's `wsl_release_url` and `wsl_pattern` find Canonical's newest Ubuntu 24.04 WSL image, a `.wsl` file that the script saves with a `.tar.gz` name and imports.

### Reaching the addresses from Windows

In the default NAT mode, Windows can reach the WSL virtual machine's own address, and the lab addresses are local addresses of that machine, so a route on Windows is enough:

```powershell
$wsl = (wsl -d lab201-svc-201a -- hostname -I).Split(' ')[0]
route add 10.201.0.0 mask 255.255.0.0 $wsl
```

Run it from an elevated PowerShell, and delete the route with `route delete 10.201.0.0` when you finish. This was not tested for the book. WSL's *mirrored* and *bridged* networking modes change how Windows and WSL share addresses, and they are reported to have problems with some builds, so the script assumes the default.

## Design Considerations

- **Memory is shared.** The WSL virtual machine takes up to half of the host's memory by default. Set a limit in `%USERPROFILE%\.wslconfig` (for example `[wsl2]` and `memory=16GB`) so the lab does not starve Windows.
- **Disk.** Each distribution has its own virtual disk that grows as it fills. Eight distributions with a full Ubuntu installation take several gigabytes each, and more once the services have data.
- **Names.** Distributions are named `lab201-<host>` (for example `lab201-svc-201a`), so they never collide with distributions you already have.
- **One image, eight hosts.** The script imports the same file eight times. A host that already exists is skipped.
- **No cloud-init.** The WSL image is not a cloud image, so the script writes the user, `wsl.conf`, the network script, and the packages directly with a generated shell script, `wsl-provision.sh`, run as `root` inside each new distribution.
- **Services start with systemd.** The script turns systemd on and restarts each distribution, so packages such as FreeRADIUS and Kea start as services.
- **No build adapter.** The distributions use Windows' NAT network for package installs, so there is no separate build adapter to remove.

## Implementation and Automation

### What the script does, in order

1. Checks that `wsl.exe` exists and reads the manifest.
2. Finds the newest Ubuntu 24.04 WSL image, downloads it, and checks its SHA-256 sum against Canonical's `SHA256SUMS`.
3. Runs `make-seed.py --wsl` to write `wsl-provision.sh` for each host.
4. For each host: `wsl --import lab201-<host> <folder> <image> --version 2`, runs the provisioning script as `root`, terminates the distribution, and starts it again so `wsl.conf` takes effect.

The provisioning script writes `/etc/wsl.conf` (systemd, hostname, default user, boot command), creates `labadmin` with passwordless `sudo` and your public keys, installs `/usr/local/sbin/lab201-net.sh`, and runs `apt-get install` for the host's packages from the manifest.

### Parameters

| Parameter | Meaning |
| --- | --- |
| `-SshKeyFile` | Public key files for `labadmin` (required for `Deploy`). |
| `-InstallRoot` | Folder for the distributions' disks (default `%USERPROFILE%\wsl-lab201`). |
| `-Action` | `Deploy` (default), `Status`, or `Remove` (which unregisters each distribution and deletes its disk). |

## Validation and Troubleshooting

| Check | Command | Expected |
| --- | --- | --- |
| Distributions exist | `.\Deploy-Lab201-Wsl.ps1 -Action Status` | Eight `lab201-…` distributions |
| Hostname | `wsl -d lab201-svc-201a -- hostname` | `svc-201a` |
| Addresses | `wsl -d lab201-svc-201a -- ip -br addr` | `lab201.10` with the `10.201.10.x` addresses of the host |
| Hosts reach each other | `wsl -d lab201-admin-201 -- ping -c2 10.201.10.10` | Replies (every address is local to the shared namespace) |
| systemd | `wsl -d lab201-svc-201a -- systemctl is-system-running` | `running` or `degraded` |
| A service listens | `wsl -d lab201-svc-201a -- ss -lntu` | The service's ports |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `wsl --import` rejects the file | The `.wsl` image format is not accepted as a `.tar.gz` | Update WSL (`wsl --update`); or extract and re-compress the archive |
| No `lab201` interface after a restart | The boot command did not run | Check `/etc/wsl.conf` has `[boot] command=`, and that WSL is up to date |
| `lab201.10` is missing, addresses are on `lab201` | The WSL kernel lacks 802.1Q | Expected fallback; services still work |
| `apt-get` fails | No internet in the distribution | Check Windows' network and VPN; restart WSL (`wsl --shutdown`) |
| A service answers for the wrong host | It listens on all addresses | Bind it to its own address in its configuration |
| A service will not start: "address already in use" | Another host's copy of the same service already holds the port on all addresses | Bind both copies to their own addresses, then restart the service |
| The addresses vanish after `wsl --shutdown` | The namespace is rebuilt | Start any `lab201-…` distribution; the boot command re-adds its addresses |

## Security and Best Practices

- **Shared namespace, shared exposure.** A firewall rule or a listening service in one distribution applies to every distribution, and to the Windows network if mirrored networking is on. Do not run the attacker tools (`hping3`, `yersinia`) on a network you do not own, and keep the default NAT mode so the lab stays behind it.
- **Windows can reach into the files.** Distributions mount Windows drives under `/mnt/c`, and Windows can read the distributions' files. Keep secrets out of both, and keep `work\` clear of keys.
- **Passwordless `sudo`.** `labadmin` has it, as on the other platforms. That is acceptable for a rehearsal host and not for anything shared.
- **Remove it when you finish.** `-Action Remove` deletes the distributions and their data. Delete the route you added to Windows, and `work\`.
- **Updates.** Keep WSL and Windows updated: the lab runs on the same Linux kernel Microsoft ships.

## References and Knowledge Checks

**References:**

- Microsoft Learn, Windows Subsystem for Linux: basic commands (`wsl --import`, `--terminate`, `--unregister`), the `wsl.conf` and `.wslconfig` settings, and accessing network applications and networking modes.
- Canonical, [Ubuntu 24.04 releases](https://releases.ubuntu.com/noble/), for the `.wsl` image and `SHA256SUMS`.
- GitHub, microsoft/WSL issue tracker, for the reports of problems with bridged and mirrored networking.
- [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) for the manifest, and [Chapter 999](999-shared-lab-infrastructure.md), Lab 999.2, for the service configuration the hosts are for.

**Knowledge checks:**

1. Why can WSL not build `gw-201` or the routing peers?
2. If you add an address in one distribution, which distributions see it, and why?
3. How do the lab addresses return after WSL's virtual machine restarts?
4. What setting would you change in a service's configuration to keep `svc-201b`'s RADIUS server from answering on `svc-201a`'s address?
5. When would you pick WSL over Proxmox, and when would you not?

## Hands-On Lab

**Prerequisites.** Windows 11 with WSL 2 (`wsl --update`), about 16 GB of memory for the WSL machine (set in `.wslconfig`) and 190 GB of disk for eight distributions at most, PowerShell 7 or Windows PowerShell 5.1, Python 3.8 or later, and an SSH key pair.

### Lab 13.1: Build the hosts

1. Unpack the lab-scripts zip and open PowerShell in the `wsl` folder. Preview with `-WhatIf`:

   ```powershell
   .\Deploy-Lab201-Wsl.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub -WhatIf
   ```

2. Run it without `-WhatIf`. It downloads the image once, then builds eight distributions.
3. Run `-Action Status`.

**Expected result.** Eight `lab201-…` distributions, each with its hostname and addresses.

### Lab 13.2: Rehearse Lab 999.2 on the hosts

1. The packages are installed, and FreeRADIUS started on both `lab201-svc-201a` and `lab201-svc-201b`. Because the distributions share one network namespace, both want port 1812 on every address, so one of them reports "address already in use". Fix that first: in each distribution, edit the `listen` sections in `/etc/freeradius/3.0/sites-enabled/default` and set `ipaddr = 10.201.10.10` in `svc-201a` and `ipaddr = 10.201.10.11` in `svc-201b`, then run `sudo systemctl restart freeradius`.
2. Configure the client and a test user as in Lab 999.2, step 4, and test locally with `radtest`.
3. From `lab201-admin-201`, send a test RADIUS request to `10.201.10.10` and to `10.201.10.11`.

**Expected result.** Each server answers only on its own address, and `ss -lnu` in either distribution shows both listeners.

**Negative test.** From `lab201-static-1`, request RADIUS with a wrong secret. The server must reject it.

### Lab 13.3: Reach the lab from Windows (optional)

1. Add the route shown in the chapter and ping `10.201.10.10` from Windows.
2. Delete the route.

**Evidence.** The `Status` output, `ip -br addr` from two hosts, the accepted and rejected RADIUS requests, and (optionally) the Windows ping.

### Cleanup

Run `-Action Remove`. Delete `%USERPROFILE%\wsl-lab201`, the `work\` folder, and any Windows route you added.

## Lab Verification

Complete this sign-off once Labs 13.1 and 13.2 have been run end to end on a real Windows 11 host. Until then the script is unverified. The generated provisioning scripts pass `bash -n` and `shellcheck`, and the selection of the image and its checksum was tested against Canonical's site, but nothing has been run in WSL. Whether `wsl --import` accepts the renamed `.wsl` image, whether the WSL kernel has 802.1Q support, and whether the boot command runs on your WSL release are the first things to confirm.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the eight service-side lab hosts as WSL distributions. WSL runs one virtual machine for all distributions, so they share a kernel and a network namespace. The lab's addresses go on VLAN interfaces of one dummy device, restored on every start, and hosts keep apart only by the addresses their services listen on. WSL suits a rehearsal of the service build. It cannot carry a trunk to a hardware switch, so it cannot replace the other platforms for the labs that test the switches.

- [ ] Can explain what WSL shares between distributions and what that rules out.
- [ ] Can name the four lab hosts WSL cannot build, and why.
- [ ] Has built the eight hosts and checked their addresses.
- [ ] Has rehearsed a service configuration on them.
- [ ] Can choose between WSL and the platforms in Chapters 09 to 12 for a given lab.
