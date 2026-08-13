# Chapter 04: Building the Virtual Machines

**Host setup — creating these VMs on your hypervisor.** The per-hypervisor steps to create each VM (install from an ISO or boot a cloud image), size it, and map its NICs to the segments in this lab are the same for every hypervisor and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

## Learning Objectives

- Build the three-legged Linux router that joins every segment.
- Build the two-tier application (nginx front end, PostgreSQL database).
- Build the Windows workload standing in for a SCADA/HMI station.
- Build an agentless “PLC” that answers Modbus TCP.
- Capture a baseline snapshot set so every later exercise is reversible.

Five VMs. Build them in the order given: `ct-gw` first, because
everything else routes through it.

A general note on Ubuntu Server installs: the installer is the same
every time, so Lab 4.1 documents it in full and later exercises
reference it rather than repeating twenty screens. Read C1 properly even
if you have installed Ubuntu a hundred times, because the network
configuration differs per VM and that is the part that matters here.

## Hands-On Lab

### Lab 4.1 — Build ct-gw: the router and Gatekeeper-equivalent

**Objective.** Create the three-legged Linux router that joins all
segments and will later act as the agentless Gatekeeper for the OT cell.

**Walkthrough**

**Part 1 — Create the virtual machine**

**Step 1.** In Workstation: **File → New Virtual Machine…** (`Ctrl+N`).

**Step 2.** Choose **Custom (advanced)** → **Next**. Custom matters: the
Typical path does not let you choose the SCSI controller or add multiple
NICs cleanly.

**Step 3.** Hardware compatibility: **Workstation 17.x** → **Next**.

**Step 4.** **Installer disc image file (iso)** → **Browse…** → select
`ubuntu-22.04.5-live-server-amd64.iso`.

Workstation will detect Ubuntu and offer **Easy Install**. **Decline
it.** Easy Install auto-answers the installer and creates a user account
with settings you did not choose, and it sometimes installs the desktop
environment. Select **I will install the operating system later**, then
set the ISO manually in Step 13. If your Workstation build does not
offer that choice on this screen, continue and simply ignore the Easy
Install fields — but verify the network settings by hand afterward.

**Step 5.** Guest OS: **Linux** → Version: **Ubuntu 64-bit** → **Next**.

**Step 6.** Virtual machine name: `ct-gw`. Location:
`D:\VMs\ColorTokens-Lab\ct-gw` → **Next**.

**Step 7.** Processors: **1** processor, **1** core per processor →
**Next**.

**Step 8.** Memory: **1024 MB** → **Next**.

**Step 9.** Network type: **Use network address translation (NAT)** →
**Next**. This becomes the first NIC; you will add the other two
shortly.

**Step 10.** I/O controller: **LSI Logic (Recommended)** → **Next**.

**Step 11.** Disk type: **SCSI (Recommended)** → **Next**. → **Create a
new virtual disk** → **Next**.

**Step 12.** Disk capacity: **20 GB**. Select **Store virtual disk as a
single file**. Do **not** check “Allocate all disk space now” — thin
provisioning keeps your 130 GB budget honest. → **Next** → **Next** →
**Finish**.

**Part 2 — Add the second and third NICs**

**Step 13.** Select `ct-gw` in the library, click **Edit virtual machine
settings**.

**Step 14.** If you deferred the ISO: select **CD/DVD (SATA)**, choose
**Use ISO image file**, browse to the Ubuntu ISO, and ensure **Connect
at power on** is checked.

**Step 15.** Click **Add… → Network Adapter → Finish**. Select the new
**Network Adapter 2**, choose **Custom: Specific virtual network**, and
pick **VMnet2** from the dropdown.

**Step 16.** Repeat: **Add… → Network Adapter → Finish**. Select
**Network Adapter 3**, choose **Custom: Specific virtual network →
VMnet3**.

**Step 17.** Confirm the final adapter list, then **OK**:

| Adapter           | Network         | Segment        |
|:------------------|:----------------|:---------------|
| Network Adapter   | NAT (VMnet8)    | IT / Corporate |
| Network Adapter 2 | Custom (VMnet2) | Data Center    |
| Network Adapter 3 | Custom (VMnet3) | OT Cell        |

Order matters. Ubuntu will enumerate them by PCI slot, so adapter 1
becomes `ens33`, adapter 2 `ens34`, adapter 3 `ens35`. You will verify
rather than trust this in Step 26.

**Part 3 — Install Ubuntu Server**

**Step 18.** Power on the VM. At the GRUB menu choose **Try or Install
Ubuntu Server**.

**Step 19.** Language: **English** → **Continue**.

**Step 20.** If offered an installer update: **Continue without
updating**. Keeps the run reproducible.

**Step 21.** Keyboard layout: choose yours → **Done**.

**Step 22.** Type of install: **Ubuntu Server** (not minimized) →
**Done**.

**Step 23.** **Network connections.** Three interfaces appear. Leave
them all on DHCP for now — only `ens33` (NAT) will actually get a lease,
and that is all you need to complete the install with package downloads
working. You will configure all three statically after first boot, where
it is far easier to get right. → **Done**.

**Step 24.** Proxy address: blank → **Done**. Mirror: accept the default
→ **Done**.

**Step 25.** **Guided storage configuration:** - **Use an entire disk**
— checked - **Set up this disk as an LVM group** — **uncheck it**. LVM
adds a layer you do not need on a 20 GB lab VM and makes the partition
table harder to read when you are troubleshooting. - → **Done** → review
the summary → **Done** → **Continue** at the destructive-action warning.

**Step 26.** **Profile setup:**

```text
Your name:            Lab Admin
Your server's name:   ct-gw
Pick a username:      labadmin
Choose a password:    <choose a strong one and record it>
Confirm password:     <same>

```

Use the same `labadmin` username and password on all four Linux VMs.
This is a lab convenience, and it is explicitly bad production practice
— shared local credentials across a fleet are precisely how lateral
movement succeeds, which is a point Part D will make concrete.

**Step 27.** **Upgrade to Ubuntu Pro:** select **Skip for now** →
**Continue**.

**Step 28.** **SSH Setup:** check **Install OpenSSH server**. Leave
“Import SSH identity” as **No**. → **Done**.

**Step 29.** **Featured server snaps:** select nothing → **Done**.

**Step 30.** Wait for the install (10–20 minutes). When it shows
**Reboot Now**, select it. If the VM hangs at *“Please remove the
installation medium, then press ENTER”*, power the VM off, disconnect
the CD/DVD device in VM settings, and power on again.

**Part 4 — Post-install: identify the interfaces**

**Step 31.** Log in as `labadmin` at the console.

**Step 32.** Update the system:

```bash
sudo apt update && sudo apt -y upgrade

```

**Step 33.** Install the tools this lab uses throughout:

```bash
sudo apt -y install nftables tcpdump net-tools nmap netcat-openbsd \
                    curl iputils-ping traceroute open-vm-tools \
                    postgresql-client-14 socat jq

```

`open-vm-tools` gives clean shutdown, time sync, and copy-paste with the
host. Install it on every Linux guest.

**Step 34.** Map interfaces to networks. **Do not assume ens33/34/35** —
verify. Each VMware NIC has a distinct MAC, and Workstation shows them
in VM settings.

```bash
ip -br link show

```

Example output:

```text
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
ens33            UP             00:0c:29:1a:2b:3c <BROADCAST,MULTICAST,UP,LOWER_UP>
ens34            DOWN           00:0c:29:1a:2b:46 <BROADCAST,MULTICAST>
ens35            DOWN           00:0c:29:1a:2b:50 <BROADCAST,MULTICAST>

```

The interface that already carries a `192.168.170.x` address is the NAT
leg:

```bash
ip -br addr show

```

To confirm which physical adapter is which, compare the MAC addresses
against **VM settings → Network Adapter N → Advanced… → MAC Address**
for each of the three adapters. Write the mapping down. If your names
differ from `ens33/34/35`, substitute yours everywhere below.

**Part 5 — Static addressing with netplan**

**Step 35.** Ubuntu 22.04 Server uses netplan with the
`systemd-networkd` renderer. Replace the installer-generated file:

```bash
sudo cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.bak
sudo nano /etc/netplan/00-installer-config.yaml

```

**Step 36.** Replace the contents entirely with the following. YAML is
indentation-sensitive — use spaces, never tabs, and keep the alignment
exactly as shown:

```text
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:                          # VMnet8 - IT / Corporate (NAT)
      dhcp4: no
      addresses:
        - 192.168.170.10/24
      routes:
        - to: default
          via: 192.168.170.2
      nameservers:
        addresses: [192.168.170.2, 1.1.1.1]
    ens34:                          # VMnet2 - Data Center
      dhcp4: no
      addresses:
        - 10.10.20.254/24
    ens35:                          # VMnet3 - OT Cell
      dhcp4: no
      addresses:
        - 10.10.30.254/24

```

Only `ens33` carries a default route. The other two legs are directly
connected networks; adding a second default route would create a routing
ambiguity that produces intermittent failures.

**Step 37.** Tighten permissions (netplan warns about world-readable
configs) and apply:

```bash
sudo chmod 600 /etc/netplan/00-installer-config.yaml
sudo netplan generate
sudo netplan apply

```

**Step 38.** Verify all three legs:

```bash
ip -br addr show

```

Expected:

```bash
lo               UNKNOWN        127.0.0.1/8 ::1/128
ens33            UP             192.168.170.10/24
ens34            UP             10.10.20.254/24
ens35            UP             10.10.30.254/24
ip route show

```

Expected:

```text
default via 192.168.170.2 dev ens33 proto static
10.10.20.0/24 dev ens34 proto kernel scope link src 10.10.20.254
10.10.30.0/24 dev ens35 proto kernel scope link src 10.10.30.254
192.168.170.0/24 dev ens33 proto kernel scope link src 192.168.170.10

```

**Step 39.** Confirm name resolution and internet egress — the two
prerequisites the Xshield agent has:

```bash
resolvectl status | grep -A2 "Link 2"
ping -c 3 192.168.170.2
curl -sSI https://ubuntu.com | head -1

```

Expected: `HTTP/2 200`. If this fails, fix it now. An agent that cannot
resolve DNS or reach port 443 outbound will never enrol, and that is the
number-one cause of a stuck onboarding.

**Part 6 — Enable routing**

**Step 40.** Turn on IPv4 forwarding persistently:

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-ct-gw-routing.conf
sudo sysctl --system

```

**Step 41.** Verify:

```text
sysctl net.ipv4.ip_forward

```

Expected: `net.ipv4.ip_forward = 1`

**Part 7 — NAT for the inner segments**

The Data Center and OT segments need outbound internet so their guests
can install packages and — on Track 1 — reach the Xshield SaaS console.

**Step 42.** Create an nftables ruleset. Start permissive; Part F is
where you lock it down. Being able to see the “before” state is the
point of Progressive Segmentation.

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

table inet filter {
    chain input   { type filter hook input   priority 0; policy accept; }
    chain forward { type filter hook forward priority 0; policy accept; }
    chain output  { type filter hook output  priority 0; policy accept; }
}

table ip nat {
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        oifname "ens33" masquerade
    }
}
EOF

```

**Step 43.** Load it and enable at boot:

```bash
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables
sudo systemctl status nftables --no-pager

```

**Step 44.** Verify the ruleset is live:

```bash
sudo nft list ruleset

```

You should see the `inet filter` table with three accept-policy chains
and the `ip nat` table with the masquerade rule.

**Step 45.** Set a login banner so you never confuse this VM with
another — worth doing on all five:

```bash
echo "*** ct-gw :: ROUTER + GATEKEEPER-EQUIVALENT :: ens33=IT ens34=DC ens35=OT ***" \
  | sudo tee /etc/motd

```

**Step 46.** Shut down cleanly and take a snapshot:

```bash
sudo shutdown -h now

```

In Workstation: **VM → Snapshot → Take Snapshot…** Name it
`C1-base-router`, description “Three legs configured, forwarding + NAT
on, no policy”. Snapshot discipline is what makes the rest of this lab
low-risk; you can wreck enforcement in Part F and be back in thirty
seconds.

**Expected result.** A three-legged router at `192.168.170.10` /
`10.10.20.254` / `10.10.30.254`, forwarding, masquerading outbound, with
a snapshot taken.

**Negative test.** Set `net.ipv4.ip_forward=0` and try to ping
`10.10.30.50` from `ct-app01` later. The router silently drops the
traffic — no ICMP error, no log line, just nothing. This is worth seeing
once, because “the gateway is up and pings fine but nothing routes
through it” is a genuinely common troubleshooting scenario, and
forwarding is the first thing to check.

**Rollback.** None yet — `ct-gw` runs for the rest of the lab.

### Lab 4.2 — Build ct-app01: the application tier

**Objective.** Create the web/application tier that will be the subject
of your ring-fence policy.

**Walkthrough**

**Step 1.** Build a new VM following **Lab 4.1, Steps 1–12**,
changing:

- Name: `ct-app01`
- Memory: **1536 MB**
- Processors: **1**
- Disk: **20 GB**
- Network at creation: NAT (you will change it)

**Step 2.** Before first boot, **Edit virtual machine settings → Network
Adapter → Custom: Specific virtual network → VMnet2**. This VM has
exactly **one** NIC, on the Data Center segment. Confirm there is no
second adapter.

**Step 3.** Install Ubuntu Server following **C1, Steps 18–30**, with
hostname `ct-app01` and the same `labadmin` account.

At the network step the single interface will get **no DHCP lease** —
VMnet2 has DHCP disabled, by design. The installer will show it as
unconfigured. Configure it right there in the installer, which saves a
console-only fix later:

- Select the interface → **Edit IPv4** → **Manual**
- Subnet: `10.10.20.0/24`
- Address: `10.10.20.11`
- Gateway: `10.10.20.254`
- Name servers: `192.168.170.2`
- Search domains: *(blank)*
- → **Save** → **Done**

**Step 4.** After first boot, verify egress through `ct-gw` — this
simultaneously tests your router, your NAT rule, and your DNS:

```bash
ip -br addr show
ip route show
ping -c 3 10.10.20.254
ping -c 3 192.168.170.2
curl -sSI https://ubuntu.com | head -1

```

If the `curl` fails but the pings succeed, the problem is DNS or the
masquerade rule on `ct-gw`, not routing. Check `sudo nft list ruleset`
on `ct-gw`.

**Step 5.** Update and install the toolset:

```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install nginx nftables tcpdump net-tools nmap netcat-openbsd \
                    curl postgresql-client-14 open-vm-tools jq

```

**Step 6.** Give nginx a page that identifies the host, so that later
curl output is unambiguous:

```bash
sudo tee /var/www/html/index.html > /dev/null <<'EOF'
<!doctype html>
<html><head><title>ct-app01</title></head>
<body>
  <h1>ct-app01 :: Application Tier</h1>
  <p>Segment: Data Center (VMnet2) 10.10.20.11</p>
  <p>Xshield role: agent-enforced workload</p>
</body></html>
EOF

sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager | head -5

```

**Step 7.** Verify locally:

```bash
curl -s http://127.0.0.1/ | grep -o "ct-app01 :: Application Tier"

```

Expected: `ct-app01 :: Application Tier`

**Step 8.** Set the banner and snapshot:

```bash
echo "*** ct-app01 :: APP TIER :: 10.10.20.11 :: nginx:80 ***" | sudo tee /etc/motd
sudo shutdown -h now

```

Snapshot as `C2-base-app`.

**Expected result.** `ct-app01` at `10.10.20.11`, serving HTTP on port
80, routing through `ct-gw` with working DNS and internet access.

**Negative test.** Set the gateway to `10.10.20.1` (the Windows host
adapter) instead of `10.10.20.254`. Local pings succeed but
`curl https://ubuntu.com` hangs — the Windows host is not routing or
NATting for you. A wrong-but-pingable gateway is a subtle failure worth
having seen.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Build ct-db01: the database tier

**Objective.** Create the crown-jewel asset. Everything you do in Part E
exists to protect this host.

**Walkthrough**

**Step 1.** Build following **C1 Steps 1–12** with:

- Name: `ct-db01`
- Memory: **1536 MB**
- Disk: **20 GB**
- Single NIC on **VMnet2**

**Step 2.** Install Ubuntu Server per **C1 Steps 18–30**, hostname
`ct-db01`, and configure the network manually in the installer:

- Address: `10.10.20.12`, Subnet `10.10.20.0/24`, Gateway
  `10.10.20.254`, DNS `192.168.170.2`

**Step 3.** Update and install PostgreSQL:

```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install postgresql postgresql-contrib nftables tcpdump \
                    net-tools netcat-openbsd curl open-vm-tools jq

```

**Step 4.** Confirm the service is up and note that by default it
listens on loopback only:

```bash
sudo systemctl status postgresql --no-pager | head -5
sudo ss -lntp | grep 5432

```

Expected at this stage:

```text
LISTEN 0  244  127.0.0.1:5432  0.0.0.0:*  users:(("postgres",pid=xxx,fd=x))

```

**Step 5.** Create the lab database and a user, so the application tier
has something real to connect to:

```bash
sudo -u postgres psql <<'SQL'
CREATE DATABASE ctlab;
CREATE USER appuser WITH ENCRYPTED PASSWORD 'LabAppPassw0rd!';
GRANT ALL PRIVILEGES ON DATABASE ctlab TO appuser;
\c ctlab
CREATE TABLE customers (id serial PRIMARY KEY, name text, card_last4 char(4));
INSERT INTO customers (name, card_last4) VALUES
  ('Acme Corp','4242'), ('Globex','1881'), ('Initech','9003');
GRANT ALL ON ALL TABLES IN SCHEMA public TO appuser;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO appuser;
SQL

```

The `card_last4` column is deliberate. It makes the exfiltration in
Lab 5.3 feel like what it is.

**Step 6.** Expose PostgreSQL on the Data Center segment. **This is
intentionally over-exposed** — you are building the insecure “before”
state that microsegmentation will fix.

```bash
sudo sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = '*'/" \
    /etc/postgresql/14/main/postgresql.conf

grep "^listen_addresses" /etc/postgresql/14/main/postgresql.conf

```

Expected: `listen_addresses = '*'`

**Step 7.** Allow password authentication from the whole Data Center
segment — again, deliberately too broad:

```bash
echo "host    all    all    10.10.20.0/24    scram-sha-256" \
  | sudo tee -a /etc/postgresql/14/main/pg_hba.conf
sudo systemctl restart postgresql

```

**Step 8.** Verify it now listens on all interfaces:

```bash
sudo ss -lntp | grep 5432

```

Expected:

```text
LISTEN 0  244  0.0.0.0:5432  0.0.0.0:*  users:(("postgres",pid=xxx,fd=x))

```

**Step 9.** Banner and snapshot:

```bash
echo "*** ct-db01 :: DATABASE TIER :: 10.10.20.12 :: postgres:5432 :: CROWN JEWELS ***" \
  | sudo tee /etc/motd
sudo shutdown -h now

```

Snapshot as `C3-base-db`.

**Expected result.** PostgreSQL 14 on `10.10.20.12:5432`, database
`ctlab` with a `customers` table, reachable from anywhere on the Data
Center segment.

**Negative test.** From `ct-app01`, before any segmentation exists:

```text
PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d ctlab -c "SELECT * FROM customers;"

```

This succeeds — as it should, it is the legitimate application flow. In
Lab 5.3 the *same* command will succeed from `ct-win01`, which has
no business touching the database at all. That contrast is the entire
argument for microsegmentation, and you want to have felt it rather than
read it.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Build ct-win01: the Windows workload and SCADA/HMI

**Objective.** Create the Windows host that demonstrates Windows
Filtering Platform enforcement and the Windows-specific Xshield agent
prerequisites, and which doubles as the SCADA/HMI station that
legitimately talks to the PLC.

**Walkthrough**

**Part 1 — Create the VM**

**Step 1.** **File → New Virtual Machine → Custom (advanced) → Next**.

**Step 2.** Hardware compatibility: **Workstation 17.x** → **Next**.

**Step 3.** **I will install the operating system later** → **Next**.
Declining Easy Install is important here: Workstation’s Windows Easy
Install auto-generates an answer file, creates an account with a blank
or auto-set password, and installs VMware Tools unattended. You want to
see the installation, and you certainly want to choose your own
Administrator password.

**Step 4.** Guest OS: **Microsoft Windows** → Version: **Windows Server
2022** → **Next**.

**Step 5.** Name: `ct-win01`, in your lab folder → **Next**.

**Step 6.** Firmware: **UEFI**. Check **Secure Boot** if offered —
Windows Server 2022 supports it and it keeps the VM closer to a
realistic build. → **Next**.

**Step 7.** Processors: **2** processors, **1** core each (2 vCPU total)
→ **Next**.

**Step 8.** Memory: **4096 MB** → **Next**.

**Step 9.** Network: **Custom: Specific virtual network → VMnet2** →
**Next**.

**Step 10.** I/O controller: **LSI Logic SAS (Recommended)** → **Next**.

**Step 11.** Disk type: **NVMe** → **Next** → **Create a new virtual
disk** → **Next**.

**Step 12.** Capacity: **60 GB**, **single file**, not pre-allocated →
**Next** → **Next** → **Finish**.

**Step 13.** **Edit virtual machine settings → CD/DVD → Use ISO image
file →** browse to the Windows Server 2022 evaluation ISO. Ensure
**Connect at power on** is checked. → **OK**.

**Part 2 — Install Windows Server 2022**

**Step 14.** Power on. Press any key quickly when prompted to boot from
CD — the window is about five seconds and missing it drops you to a UEFI
shell. If that happens, reset the VM and try again.

**Step 15.** Language, time format, keyboard → **Next** → **Install
now**.

**Step 16.** Select the operating system. Choose **Windows Server 2022
Standard Evaluation (Desktop Experience)**. The Desktop Experience is
essential — the Core edition has no GUI, and several exercises use
`wf.msc` and the Windows Security interface. → **Next**.

**Step 17.** Accept the license terms → **Next**.

**Step 18.** **Custom: Install Microsoft Server Operating System only
(advanced)**.

**Step 19.** Select **Drive 0 Unallocated Space** → **Next**.
Installation takes 10–25 minutes with several reboots.

**Step 20.** At the **Customize settings** screen, set the Administrator
password. Record it. Windows Server enforces complexity, so something
like `L@bAdmin2026!` works.

**Step 21.** Log in: click in the VM window and press `Ctrl+Alt+Insert`
(Workstation’s substitute for `Ctrl+Alt+Delete`, which the host
intercepts). Enter the password.

**Part 3 — VMware Tools and base configuration**

**Step 22.** Install VMware Tools: **VM → Install VMware Tools…** in the
Workstation menu. Inside the guest, open File Explorer, open the DVD
drive, run `setup64.exe`, choose **Typical**, and reboot when prompted.
Without Tools you get poor display resolution, no clean shutdown, and no
clipboard sharing.

**Step 23.** Open **PowerShell as Administrator** inside the guest
(right-click Start → Windows PowerShell (Admin)).

**Step 24.** Set the hostname:

```text
Rename-Computer -NewName "ct-win01" -Restart

```

**Step 25.** After the reboot, configure static networking. First
identify the adapter:

```powershell
Get-NetAdapter | Format-Table -AutoSize Name, InterfaceDescription, Status, MacAddress

```

Expected — a single adapter, typically named `Ethernet0`:

```text
Name      InterfaceDescription                Status MacAddress
----      --------------------                ------ ----------
Ethernet0 Intel(R) 82574L Gigabit Network ... Up     00:0C:29:XX:XX:XX

```

**Step 26.** Apply the static address:

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet0" -IPAddress 10.10.20.21 `
    -PrefixLength 24 -DefaultGateway 10.10.20.254

Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" -ServerAddresses 192.168.170.2

```

**Step 27.** Verify:

```powershell
Get-NetIPConfiguration -InterfaceAlias "Ethernet0"
Test-NetConnection -ComputerName 10.10.20.254 -InformationLevel Detailed
Resolve-DnsName ubuntu.com | Select-Object -First 2
Test-NetConnection -ComputerName ubuntu.com -Port 443

```

The last command must report `TcpTestSucceeded : True`. That is exactly
the outbound HTTPS reachability the Xshield agent requires, and testing
it now — rather than during agent installation — is the habit that keeps
onboarding boring.

**Step 28.** Set the network profile to Private so that the built-in
firewall behaves predictably:

```powershell
Set-NetConnectionProfile -InterfaceAlias "Ethernet0" -NetworkCategory Private
Get-NetConnectionProfile

```

**Part 4 — Baseline the Windows firewall state**

This is not busywork; it is an Xshield prerequisite that you must be
able to evidence.

**Step 29.** Record the current firewall profile state:

```powershell
Get-NetFirewallProfile | Format-Table -AutoSize Name, Enabled,
    DefaultInboundAction, DefaultOutboundAction

```

Expected on a fresh install:

```text
Name    Enabled DefaultInboundAction DefaultOutboundAction
----    ------- -------------------- ---------------------
Domain  True    NotConfigured        NotConfigured
Private True    NotConfigured        NotConfigured
Public  True    NotConfigured        NotConfigured

```

**Step 30.** Confirm no Group Policy is managing the firewall. On a
standalone lab VM this should be clean, but running the check builds the
habit:

```text
gpresult /Scope Computer /r | Select-String -Pattern "Applied Group Policy Objects" -Context 0,6

```

Expected on a workgroup machine: only `Local Group Policy`, or “N/A”.

**Step 31.** Confirm nothing else is registered as a third-party
firewall:

```powershell
Get-CimInstance -Namespace root\SecurityCenter2 -ClassName FirewallProduct |
    Select-Object displayName, productState

```

Expected: **no output**, meaning only the Windows Defender Firewall is
in play — which is exactly what Xshield requires. If a third-party
product appears here, Xshield cannot reliably program the native
firewall and you must remove it before enrolling the agent. Lab 7.3
returns to this.

**Step 32.** Install a couple of tools used later. Enable the built-in
OpenSSH client and install a PostgreSQL client:

```text
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

```

For the PostgreSQL client, download the Windows binaries from
`enterprisedb.com` (the “Command Line Tools” component of the installer
is sufficient), or simply use `Test-NetConnection` for the connectivity
proofs — the exercises are written to work either way.

**Step 33.** Snapshot. Shut down cleanly from the Start menu, then in
Workstation take a snapshot named `C4-base-win`.

**Expected result.** `ct-win01` at `10.10.20.21`, Windows Server 2022
Standard Evaluation with Desktop Experience, VMware Tools installed,
Defender Firewall enabled with no third-party firewall product and no
managing GPO — the exact preconditions the Xshield Windows agent
requires.

**Negative test.** Install any third-party endpoint product that takes
over the native firewall, then re-run Step 31. It appears in
`FirewallProduct`, and on a real Xshield deployment the agent would be
unable to apply policy reliably — assets sit in a partially-enforced
state that is worse than either extreme, because you believe you are
protected and you are not. This is the most commonly-hit Windows
prerequisite in real Xshield rollouts. Uninstall it before continuing.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — Build ct-ot01: the agentless “PLC”

**Objective.** Create a stand-in for an operational-technology device
that **cannot** run a security agent — the asset that forces you to use
a Gatekeeper.

**Why a Linux VM stands in for a PLC**

A real PLC runs a proprietary real-time operating system with no package
manager, no shell you can log into, and no possibility whatsoever of
installing third-party software. We cannot virtualize one. What we can
do is reproduce the *properties that matter to a segmentation
architect*: it exposes an industrial protocol on a well-known port, it
sits on an isolated cell network, it has one legitimate peer, and — by
the rule of this exercise — **you may not install a security agent on
it**.

Treat that rule as inviolable for the rest of the lab. The moment you
are tempted to `apt install` something protective on `ct-ot01`, you have
stopped modeling OT.

**Walkthrough**

**Step 1.** Build a VM per **C1 Steps 1–12** with:

- Name: `ct-ot01`
- Memory: **768 MB**
- Processors: **1**
- Disk: **10 GB**
- Single NIC on **VMnet3**

**Step 2.** Install Ubuntu Server per **C1 Steps 18–30**, hostname
`ct-ot01`.

At the network step, configure manually — and note the consequence:

- Address: `10.10.30.50`, Subnet `10.10.30.0/24`, Gateway
  `10.10.30.254`, DNS `192.168.170.2`

`10.10.30.254` is `ct-gw`. `ct-gw` **is this device’s only path to
anything.** That is the Gatekeeper deployment pattern in one line: the
appliance becomes the default gateway, so all device communication
traverses it.

**Important:** `ct-gw` must be powered on and configured before you
install `ct-ot01`, or the installer cannot download packages. Start it
first.

**Step 3.** After first boot, verify the path out:

```bash
ip -br addr show
ip route show
ping -c 3 10.10.30.254
ping -c 3 10.10.20.11

```

The ping to `ct-app01` at `10.10.20.11` should succeed. **That is a
problem, and it is the point.** A PLC has no legitimate reason to reach
the web tier. Right now the network is flat and permissive. Part F fixes
it.

**Step 4.** Install the bare minimum. Nothing security-related —
remember the rule:

```bash
sudo apt update
sudo apt -y install python3 open-vm-tools netcat-openbsd

```

**Step 5.** Create the Modbus TCP responder. This is a dependency-free
Python standard-library service that listens on TCP 502 and returns a
well-formed Modbus/TCP response to a Read Holding Registers request. It
is not a full protocol implementation, and it does not need to be — what
matters is a real TCP service on the real industrial port, responding in
a way you can verify.

```bash
sudo tee /opt/plc_sim.py > /dev/null <<'PYEOF'
#!/usr/bin/env python3
"""Minimal Modbus/TCP responder standing in for a PLC.

Listens on TCP 502. Answers function code 3 (Read Holding Registers) with a
fixed two-register payload so that a client can prove end-to-end reachability.
Any other function code returns a Modbus exception 01 (illegal function).
"""
import socketserver
import struct
import datetime

REGISTERS = [0x1234, 0x5678]          # pretend process values

class ModbusHandler(socketserver.BaseRequestHandler):
    def handle(self):
        peer = self.client_address[0]
        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        print(f"[{stamp}] connection from {peer}", flush=True)
        while True:
            data = self.request.recv(512)
            if not data or len(data) < 8:
                break
            txn, proto, length, unit, func = struct.unpack(">HHHBB", data[:8])
            if func == 3:                                   # read holding registers
                payload = b"".join(struct.pack(">H", r) for r in REGISTERS)
                body = struct.pack(">BB", func, len(payload)) + payload
            else:                                           # illegal function
                body = struct.pack(">BB", func | 0x80, 0x01)
            resp = struct.pack(">HHHB", txn, proto, len(body) + 1, unit) + body
            self.request.sendall(resp)
            print(f"[{stamp}] fc={func} from {peer} -> {len(resp)} bytes", flush=True)

class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    with ReusableTCPServer(("0.0.0.0", 502), ModbusHandler) as srv:
        print("PLC simulator listening on 0.0.0.0:502", flush=True)
        srv.serve_forever()
PYEOF

sudo chmod 755 /opt/plc_sim.py

```

**Step 6.** Run it as a service so it survives reboots:

```bash
sudo tee /etc/systemd/system/plc-sim.service > /dev/null <<'EOF'
[Unit]
Description=Modbus TCP PLC simulator
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/plc_sim.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now plc-sim.service
sudo systemctl status plc-sim.service --no-pager | head -8

```

**Step 7.** Verify it is listening:

```bash
sudo ss -lntp | grep 502

```

Expected:

```text
LISTEN 0  5  0.0.0.0:502  0.0.0.0:*  users:(("python3",pid=xxx,fd=x))

```

**Step 8.** Test locally with a hand-built Modbus request. The bytes are
a transaction ID, protocol ID, length, unit ID, function code 3, start
address 0, and quantity 2:

```text
printf '\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x02' | nc -w 2 127.0.0.1 502 | xxd

```

Expected — a response containing the two register values `1234` and
`5678`:

```text
00000000: 0001 0000 0007 0103 0412 3456 78         ..........4Vx

```

**Step 9.** Banner and snapshot:

```bash
echo "*** ct-ot01 :: OT CELL :: 10.10.30.50 :: MODBUS 502 :: NO AGENT PERMITTED ***" \
  | sudo tee /etc/motd
sudo shutdown -h now

```

Snapshot as `C5-base-plc`.

**Expected result.** A “PLC” at `10.10.30.50` serving Modbus/TCP on port
502, in an isolated cell whose only route to the world is `ct-gw`, with
no security agent and none permitted.

**Negative test.** From the Windows host — the “IT laptop” — with the
route from Lab 3.4 in place:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502

```

Expected right now: `TcpTestSucceeded : True`. **An IT laptop can open a
control-protocol session to a PLC.** In a real plant that is a
reportable finding. It works because the network is flat and `ct-gw`
forwards everything. Part F is the remedy.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.6 — Baseline snapshot set and boot order

**Objective.** Establish a known-good restore point for the whole estate
and a repeatable start sequence.

**Walkthrough**

**Step 1.** With all five VMs powered off, confirm each has its baseline
snapshot. **VM → Snapshot → Snapshot Manager** for each:

| VM       | Snapshot name    |
|:---------|:-----------------|
| ct-gw    | `C1-base-router` |
| ct-app01 | `C2-base-app`    |
| ct-db01  | `C3-base-db`     |
| ct-win01 | `C4-base-win`    |
| ct-ot01  | `C5-base-plc`    |

**Step 2.** Boot in dependency order. `ct-gw` must be fully up before
the others, or their DNS lookups and package operations fail in ways
that look like guest problems:

1. `ct-gw` — wait for the login prompt, roughly 30 seconds

2. `ct-app01`, `ct-db01`, `ct-ot01` — these may start together
3. `ct-win01` — last, it is the heaviest

**Step 3.** Optional but recommended: create a Workstation folder to
keep the estate together. In the library, right-click **My Computer →
New Folder**, name it `ColorTokens-Lab`, and drag all five VMs into it.
You can then power the whole estate on or off from the folder’s context
menu.

**Step 4.** Run a full reachability matrix from `ct-gw`, which can see
every segment:

```bash
for host in 10.10.20.11 10.10.20.12 10.10.20.21 10.10.30.50; do
  printf "%-14s " "$host"
  ping -c 1 -W 1 "$host" > /dev/null 2>&1 && echo "UP" || echo "DOWN"
done

```

Expected:

```text
10.10.20.11    UP
10.10.20.12    UP
10.10.20.21    UP
10.10.30.50    UP

```

**Step 5.** Confirm the services are answering, from `ct-gw`:

```bash
nc -z -w2 10.10.20.11 80    && echo "app01  :80   OPEN"
nc -z -w2 10.10.20.12 5432  && echo "db01   :5432 OPEN"
nc -z -w2 10.10.30.50 502   && echo "ot01   :502  OPEN"

```

Expected: all three report `OPEN`.

**Expected result.** Five VMs running, fully reachable, all services
answering, every VM holding a baseline snapshot.

**Negative test.** Boot `ct-app01` before `ct-gw`. Its `apt update`
fails with “Temporary failure resolving” because its only route to DNS
is through a router that is not running. Dependency ordering is real,
and this is a five-second lesson.

**Rollback.** None — this is the working baseline for Parts D through G.

## Summary and Completion Checklist

- [ ] Lab 4.1 complete, including its negative test.
- [ ] Lab 4.2 complete, including its negative test.
- [ ] Lab 4.3 complete, including its negative test.
- [ ] Lab 4.4 complete, including its negative test.
- [ ] Lab 4.5 complete, including its negative test.
- [ ] Lab 4.6 complete, including its negative test.
