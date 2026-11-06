# Lab automation scripts for Volume CCI

These scripts create the virtual machines of the shared lab in Chapter 999 of
Volume CCI (FortiSwitch STIG and SRG Mapping). Each platform has a chapter that
explains it, and all of them read the same manifest.

| Folder | Platform | Chapter | Run it with |
| --- | --- | --- | --- |
| `esxi/` | VMware ESXi 7, 8, and 9, standalone host | 09 | PowerShell and PowerCLI |
| `vcenter/` | VMware vCenter Server 7, 8, and 9 | 10 | PowerShell and PowerCLI |
| `workstation/` | VMware Workstation Pro for Windows | 11 | PowerShell |
| `proxmox/` | Proxmox VE 8.1 or later | 12 | Bash, as root on the node |
| `wsl/` | WSL 2 on Windows 11 (service hosts only) | 13 | PowerShell |
| `common/` | The manifest and the cloud-init seed tool | 09 | Used by all of them |

## Before you run anything

1. Read the chapter for your platform, and run the script with `-WhatIf` (or
   `--dry-run` for Proxmox) first. None of these scripts has been run against a
   real host yet. Treat them as a starting point to check, not a tested tool.
2. Install Python 3.8 or later. For the seed ISOs (every platform except
   Proxmox and WSL), also run `pip install pycdlib`.
3. Make an SSH key pair (`ssh-keygen -t ed25519`) and pass the public key file
   with `-SshKeyFile` (or `--ssh-key`).
4. Keep the scripts and the `common` folder together, because each script finds
   `..\common\lab201-vms.json` and `make-seed.py` relative to itself.

## What is in `common/`

- `lab201-vms.json` lists the twelve machines, their sizes, networks, and IPv4
  addresses. The IPv6 addresses are derived from the IPv4 addresses.
- `make-seed.py` writes the cloud-init files (and, with `--iso`, a seed ISO) for
  each machine, or with `--wsl` the provisioning script for a WSL host.

Check the downloaded files against `SHA256SUMS` in this folder.

## What these scripts do not do

They create the machines. They do not configure the switches, the services
(RADIUS, syslog, NTP, and the rest), or the routing peers' protocols. Those are
Chapter 999 and the requirement labs in Chapters 04 to 07. They also do not
create `fgt-201` (a licensed FortiGate-VM image), the console server, or the
physical test endpoints.
