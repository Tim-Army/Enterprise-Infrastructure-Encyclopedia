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
| `kvm/` | KVM and libvirt on Linux | 14 | Bash, as root or a libvirt user |
| `common/` | The manifest, the Linux flavor catalog, the seed tool, and the image resolver | 09 | Used by all of them |
| `builder/` | The Lab Builder page | 09 | A web browser |

## The Lab Builder

`builder/lab-builder.html` is a single page that runs in your browser. Pick a platform and version, set the host and network names, rename machines, change their sizes (a size below the proposed minimum is refused unless you tick Override), leave machines out, and move the lab to another address block. It then shows the manifest, the commands, and a checklist, and can download them in a zip. The zip also holds `lab-builder-choices.json`, the same file that **Save choices** makes. Use **Load choices** with it to get the same build back on the page. Load that file and not the manifest (`lab201-vms.json`), which the page refuses. Open it from the published site so it can add the scripts to the zip. Nothing you type leaves the page, and it never asks for a license key: it writes a `licenses.example.json` template for the keys the scripts can apply (Red Hat, Ubuntu Pro, vSphere, and Proxmox), and you fill in `licenses.local.json` on your own computer.

## Walk the labs with Claude

The zip that the Lab Builder makes is ready for a Claude session. Besides the
scripts and the manifest, it holds:

- `LAB-VALUES.md`: the values of your build in one place (switch models and
  host names, VLAN IDs, subnets, and machine names and addresses).
- `walkthroughs/`: the lab chapters this build is for (Chapter 999 and the
  requirement labs in Chapters 04 to 08), rewritten with those values.
- `CLAUDE.md`: instructions that tell Claude what the folder holds and how to
  walk the labs, starting with Lab 999.1.
- `START-CLAUDE.txt`: the line to start with.

The walkthrough files have short names in the zip, such as
`walkthroughs/999-shared-lab.md`, so that the paths stay short on Windows.
On the Lab Builder you can pick the FortiSwitchOS release (7.6.7, 8.0.0, or 8.0.1) and your
two switch models. `LAB-VALUES.md` then lists the lab features that Fortinet's
Feature Matrix marks as not supported on those models, with the labs that
name them, and `CLAUDE.md` tells Claude to record such a step as blocked by
the model. The data is `common/fortiswitch-features.json`. It covers model
series, so check the matrix for your exact model.

On the Lab Builder you can also type the switch ports you use, which replace
placeholders such as `<PORT_EP1>` in the walkthroughs, and pick the lab that
Claude starts with.

Claude logs each step in `PROGRESS.md`, as a table with the columns Lab, Step,
Result, Date, and Note. Click **Load progress** on the Lab Builder and pick
that file to see, on the **Progress** tab, which labs passed.

With Claude Code, unzip the file, open a terminal in the `lab201-build`
folder, and run:

```powershell
claude "Start the lab walkthrough."
```

Claude Code reads `CLAUDE.md` by itself. In the Claude desktop or web app, add
the folder to a project or chat and send: `Read CLAUDE.md and LAB-VALUES.md,
then start the lab walkthrough.`

Claude then takes one step at a time, waits for your output, and checks it
against the expected result. It is told not to change a switch or a machine
without your go-ahead, and never to ask for a password or a license key.

The walkthroughs are rewritten by pattern (`VLAN 40`, `set vlanid 40`,
`vlan40`, and the lab addresses). If a step and `LAB-VALUES.md` differ,
`LAB-VALUES.md` is right. The chapters in `walkthroughs/` of the lab-scripts
zip are the unchanged originals. `walkthroughs.list` names them.

## Before you run anything

On VMware Workstation, start with the readiness check. It changes nothing. It
tests Python and `pycdlib`, the SSH key, the Workstation tools, the manifest,
memory, disk space, and the networks, and says how to fix what is missing:

```powershell
.\Deploy-Lab201-Workstation.ps1 -Action Check -SshKeyFile ~\.ssh\id_ed25519.pub
```

The other scripts have no check yet, so follow this list for them.

1. Read the chapter for your platform, and run the script with `-WhatIf` (or
   `--dry-run` for Proxmox) first. The Proxmox VE and VMware Workstation scripts
   have built the lab machines on real hosts (Chapter 09 says what was run).
   The ESXi, vCenter, VxRail, KVM, and WSL scripts have not been run. Treat
   all of them as a starting point to check, not a finished tool.
2. Install Python 3.8 or later. For the seed ISOs (every platform except
   Proxmox and WSL), also run `python -m pip install pycdlib`. The PowerShell
   scripts look for `python3`, then the `py` launcher, then `python`, and skip
   the Microsoft Store stubs that only print "Python was not found". To pick
   the command or version yourself, pass `-PythonCommand` (for example
   `-PythonCommand 'py -3.15'`), or `--python python3.15` to the Bash scripts,
   which use `python3` by default. See *Install Python on Windows* below.
3. Make an SSH key pair (`ssh-keygen -t ed25519`) and pass the public key file
   with `-SshKeyFile` (or `--ssh-key`). See *Make an SSH key on Windows* below.
4. Keep the scripts and the `common` folder together, because each script finds
   `..\common\lab201-vms.json` and `make-seed.py` relative to itself.

## Install Python on Windows

If a script says that Python was not found, install Python with `winget`.
First list the versions that `winget` offers, to see the latest one:

```powershell
winget search Python.Python
```

Install the version you want. This installs Python 3.15:

```powershell
winget install Python.Python.3.15
```

Close the PowerShell window and open a new one, so the new `python` command
is found. Then check the version and install the package that the scripts need
for the seed ISOs:

```powershell
python --version
python -m pip install pycdlib
```

If `python` still says that Python was not found, the Microsoft Store stub is
taking priority. Use the `py` launcher instead (`py -3 --version`), or pass
`-PythonCommand 'py -3.15'` to the script. The scripts were written for Python
3.8 or later and have been run on Python 3.10 and 3.15.

### If the script says the ISO needs pycdlib

The script makes the seed ISOs with the `pycdlib` Python package, and stops
when that package is missing. Install it with the same Python that the script
uses:

```powershell
python -m pip install pycdlib
```

If `python` is the Microsoft Store stub on your computer, use the launcher:

```powershell
py -3 -m pip install pycdlib
```

Then run the script again. With more than one Python installed, `pycdlib` has
to be in the one the script picks. The script tries `python3`, then `py -3`,
then `python`. To use one version for both, install the package into it and
name it with `-PythonCommand`:

```powershell
py -3.15 -m pip install pycdlib
.\Deploy-Lab201-Workstation.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub -PythonCommand 'py -3.15' -WhatIf
```

## Make an SSH key on Windows

A deploy needs an SSH public key, so that you can log in to the machines it
builds. Without one, the script stops with `-SshKeyFile is required`. First
check whether you already have a key:

```powershell
Get-ChildItem ~\.ssh\*.pub
```

If that lists a file such as `id_ed25519.pub`, use it. If it prints nothing,
make a key pair:

```powershell
ssh-keygen -t ed25519
```

Press Enter at each prompt to accept the default file name. A passphrase is
optional. The command writes two files in `~\.ssh`: `id_ed25519` is the private
key, which stays on your computer, and `id_ed25519.pub` is the public key.
Pass the public key to the script by adding `-SshKeyFile` and the path to the
`.pub` file on the command that runs the script. Run it from the script's own
folder, for example `workstation`. This is the preview run:

```powershell
.\Deploy-Lab201-Workstation.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub -WhatIf
```

To build the machines, run the same line without `-WhatIf`:

```powershell
.\Deploy-Lab201-Workstation.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub
```

Pass `id_ed25519.pub` and not `id_ed25519`, which is the private key. Other
options, such as `-BridgeVmnet vmnet0`, go on the same line. The Lab Builder's
Command tab and `RUN.txt` in its zip give the whole command with `-SshKeyFile`
already filled in. The Bash scripts take the same file with `--ssh-key`.

If `ssh-keygen` is not recognized, the OpenSSH client is not installed. Open
PowerShell as administrator and check for it:

```powershell
Get-WindowsCapability -Online -Name OpenSSH.Client*
```

If the state is `NotPresent`, install it, then open a new PowerShell window and
run `ssh-keygen` again:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

## Log in to the machines

The admin user on every Linux machine is `labadmin`. Over SSH it accepts only
the key you passed with `-SshKeyFile` (or `--ssh-key`). Log in from the
computer that holds the private key:

```powershell
ssh labadmin@<address>
```

`<address>` is the machine's address on the build network. On VMware
Workstation, the script lists every machine with the line that logs in to it.
A new machine needs a few minutes to install its guest tools before its
address shows:

```powershell
.\Deploy-Lab201-Workstation.ps1 -Action Status
```

`sudo` asks for no password on the standard flavors.

To sign in at the machine's console window, give `labadmin` a console
password before you run the deploy. Put it in `LAB201_CONSOLE_PASSWORD`:

```powershell
$env:LAB201_CONSOLE_PASSWORD = '<LAB_ONLY_PASSWORD>'
```

In Bash, use `export LAB201_CONSOLE_PASSWORD='<LAB_ONLY_PASSWORD>'`. The
password works at the console and for `sudo`. SSH still takes only the key,
because password login over SSH stays off. The Lab Builder proposes a console
password and puts this line in the commands. That default is published with
the page, so change it or clear it for anything but a closed lab. The seed
file holds the password as plain text, so use a lab-only value. This was
tested on one Ubuntu 24.04 machine on Proxmox VE.

To allow password login over SSH as well, use a password hash instead. Make
the hash with `openssl passwd -6`, which prompts for the password, and put it
in `LAB201_ADMIN_PASSWORD_HASH`. When the hash is set, the console password is
not used:

```powershell
$env:LAB201_ADMIN_PASSWORD_HASH = '<CRYPT_HASH>'
```

In Bash, use `export LAB201_ADMIN_PASSWORD_HASH='<CRYPT_HASH>'`. The password
then works at the console and over SSH. Machines that are already built keep
their setup, so this applies to machines you build afterwards. The hardened
(STIG) flavors always need this hash, because their `sudo` asks for the
password.

## VMware Workstation: see the machines in the library

The Workstation script builds and starts the machines with `vmrun`, which does
not add them to the Workstation library. They run, but the Library pane stays
empty. To list them:

1. In Workstation, right-click **My Computer** in the Library.
2. Choose **Scan for Virtual Machines**.
3. Pick the machines folder. The script prints it as `Machines folder`. By
   default it is `lab201` inside Workstation's folder for virtual machines.
4. Finish the scan. The lab machines then appear in the Library.

The script can also open each machine in Workstation after the build, which
lists it in the Library. Add `-AddToLibrary` to the deploy command, or tick
the box in the Lab Builder. This option has not been tested yet, so use the
scan if a machine is missing.

When a machine starts, Workstation may warn that the value `preset` for
`powerType.powerOff` is not valid and that it uses `soft` instead. The setting
comes from the imported cloud image, and the warning is harmless. The script
now removes those settings from each machine it builds.

## If PowerShell blocks a script

Windows blocks downloaded PowerShell scripts by default. PowerShell then says
that running scripts is disabled on this system, or that the file is not
digitally signed. Use one of the two commands below. Both apply to one
PowerShell process only, so nothing changes for the rest of the computer.

To run one script past the execution policy without changing any setting:

```powershell
powershell -ExecutionPolicy Bypass -File .\Deploy-Lab201-Vcenter.ps1 -WhatIf
```

Use the script for your platform, and add its parameters after the file name.
Use `pwsh` instead of `powershell` if you run PowerShell 7. A table parameter
such as `-FlavorImages @{ ... }` cannot be passed this way, so use the next
command for those.

To allow scripts for the rest of the current window instead, and then run the
scripts as the chapters show:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

The setting ends when you close the window. Neither command works if Group
Policy sets the execution policy. In that case, ask your administrator.

`Bypass` also skips the "downloaded from the internet" prompt. Under a policy
such as `RemoteSigned`, unblock the downloaded scripts instead. Run this from
a platform folder such as `esxi`:

```powershell
Get-ChildItem -Path .. -Recurse -Filter *.ps1 | Unblock-File
```

## What is in `common/`

- `lab201-vms.json` lists the twelve machines, their sizes, networks, and IPv4
  addresses. The IPv6 addresses are derived from the IPv4 addresses.
- `flavors.json` lists the Linux flavors (Ubuntu, Debian, Rocky, Alma, Fedora, Red Hat, and the hardened Ubuntu and Red Hat), their package names, and which machine types each can run. Windows 11, Windows Server, Linux Mint, and Tiny Core install from an ISO you supply, and are available on Proxmox VE, ESXi, vCenter, and VxRail.
- `resolve-image.py` finds, downloads, and checks the cloud image for a flavor.
- `make-seed.py` writes the cloud-init files (and, with `--iso`, a seed ISO) for
  each machine, or with `--wsl` the provisioning script for a WSL host.

The published copy of this folder also has `diagrams/lab-topology.svg` and `lab-topology.png`, the Chapter 999 network diagram. The site build adds them, so they are not in the repository copy of this folder.

Check the downloaded files against `SHA256SUMS` in this folder.

## What these scripts do not do

They create the machines. They do not configure the switches, the services
(RADIUS, syslog, NTP, and the rest), or the routing peers' protocols. Those are
Chapter 999 and the requirement labs in Chapters 04 to 07. They also do not
create `fgt-201` (a licensed FortiGate-VM image), the console server, or the
physical test endpoints.
