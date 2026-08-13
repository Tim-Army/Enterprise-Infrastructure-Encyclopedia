# Chapter 04: Building the Virtual Machines

**Host setup — creating these VMs on your hypervisor.** The per-hypervisor steps to create each VM (install from an ISO or boot a cloud image), size it, and map its NICs to the segments in this lab are the same for every hypervisor and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

## Learning Objectives

- Build the three-legged Linux router (`aw-gw`) that joins the underlay segments and will host the overlay hub and the Airwall Gateway.
- Build the two-tier application: `aw-app01` (nginx) and `aw-db01` (PostgreSQL).
- Build the Windows SCADA/HMI workstation (`aw-win01`).
- Build the agentless "PLC" (`aw-ot01`).
- Snapshot every VM at a known-good baseline.

Every static address comes from the Chapter 01 address plan (underlay addresses here; overlay addresses are assigned in Chapter 06).

## Hands-On Lab

### Lab 4.1 — Build `aw-gw`, the three-legged router

**Objective.** Create the Ubuntu router with one NIC on each underlay segment, forwarding and masquerading.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 1 vCPU, 1024 MB, 20 GB. Add **three** NICs: NIC1 → **VMnet8**, NIC2 → **VMnet2**, NIC3 → **VMnet3**. Hostname `aw-gw`, user `labadmin`, OpenSSH enabled.

**Step 2.** Identify interfaces (`ip -br link`, typically `ens33/ens34/ens35`) and write the netplan:

```bash
sudo tee /etc/netplan/00-aw-gw.yaml > /dev/null <<'EOF'
network:
  version: 2
  ethernets:
    ens33:
      addresses: [192.168.170.10/24]
      routes: [{ to: default, via: 192.168.170.2 }]
      nameservers: { addresses: [192.168.170.2] }
    ens34:
      addresses: [10.10.20.254/24]
    ens35:
      addresses: [10.10.30.254/24]
EOF
sudo chmod 600 /etc/netplan/00-aw-gw.yaml
sudo netplan apply
```

**Step 3.** Enable forwarding and masquerade:

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-router.conf
sudo sysctl --system
sudo apt -y install nftables
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
table ip nat {
    chain postrouting {
        type nat hook postrouting priority 100;
        oifname "ens33" masquerade
    }
}
EOF
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables
```

**Expected result.** `ip -br addr` shows the three addresses; `ping -c1 8.8.8.8` succeeds.

**Negative test.** Skip `net.ipv4.ip_forward=1` and internal hosts reach `aw-gw` but not the internet.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Build `aw-db01`, the PostgreSQL tier

**Objective.** Create the database, the crown jewel this lab protects.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 1536 MB, one NIC → **VMnet2**. Hostname `aw-db01`, `10.10.20.12/24`, gateway `10.10.20.254`, DNS `192.168.170.2`.

**Step 2.** Install PostgreSQL and create the app database. Note it will listen on the *overlay* address later; for now it listens on its underlay address so Chapter 05 can demonstrate the flat-network attack:

```bash
sudo apt update && sudo apt -y install postgresql
sudo -u postgres psql <<'SQL'
CREATE DATABASE awlab;
CREATE USER appuser WITH PASSWORD 'LabAppPassw0rd!';
GRANT ALL PRIVILEGES ON DATABASE awlab TO appuser;
\c awlab
CREATE TABLE customers (id serial PRIMARY KEY, name text);
INSERT INTO customers (name) VALUES ('acme'), ('globex'), ('initech');
GRANT ALL ON ALL TABLES IN SCHEMA public TO appuser;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO appuser;
SQL
sudo sed -i "s/^#listen_addresses.*/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
echo "host awlab appuser 10.99.0.0/24 md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf
echo "host awlab appuser 10.10.20.0/24 md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf
sudo systemctl restart postgresql
```

**Expected result.** `sudo ss -ltnp | grep 5432` shows PostgreSQL listening.

**Negative test.** Restricting `listen_addresses` to the underlay only would block overlay clients in Chapter 07; listening on `*` lets the database serve whichever interface policy permits.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Build `aw-app01`, the nginx application tier

**Objective.** Create the web/app tier whose only legitimate east-west dependency is the database.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 1536 MB, one NIC → **VMnet2**. Hostname `aw-app01`, `10.10.20.11/24`, gateway `10.10.20.254`, DNS `192.168.170.2`.

**Step 2.** Install nginx and the PostgreSQL client, and a probe of the app→db path. During Chapter 05 it targets the underlay address; from Chapter 07 it targets the overlay address:

```bash
sudo apt update && sudo apt -y install nginx postgresql-client
echo "aw-app01 nginx up" | sudo tee /var/www/html/index.html
cat > ~/checkdb.sh <<'EOF'
#!/usr/bin/env bash
DB="${1:-10.10.20.12}"    # underlay by default; pass 10.99.0.12 for the overlay
PGPASSWORD='LabAppPassw0rd!' psql -h "$DB" -U appuser -d awlab -tAc "SELECT count(*) FROM customers;"
EOF
chmod +x ~/checkdb.sh
~/checkdb.sh
```

**Expected result.** `curl -s http://10.10.20.11` returns the page; `~/checkdb.sh` prints `3`.

**Negative test.** Stop PostgreSQL and re-run `~/checkdb.sh`; it fails. This is the flow the overlay must permit.

**Rollback.** Restart PostgreSQL if you stopped it.

### Lab 4.4 — Build `aw-win01`, the Windows SCADA/HMI workstation

**Objective.** Create the Windows workload that supervises the PLC — and the attacker's pivot point in Chapter 05.

**Walkthrough**

**Step 1.** New VM: Windows Server 2022 Evaluation, 2 vCPU, 4096 MB, 60 GB, one NIC → **VMnet2**. Administrator password `LabAdminPassw0rd!`.

**Step 2.** Set the static address (elevated PowerShell):

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet0" -IPAddress 10.10.20.21 `
    -PrefixLength 24 -DefaultGateway 10.10.20.254
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" -ServerAddresses 192.168.170.2
Rename-Computer -NewName "aw-win01" -Restart
```

**Step 3.** After reboot, confirm the legitimate HMI→PLC flow and the (unwanted) HMI→DB reachability on the underlay:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # HMI -> PLC (legitimate)
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # HMI -> DB (should be unnecessary)
```

**Expected result.** Both succeed now — the flat underlay permits everything.

**Negative test.** Note the HMI can reach the database at all; after cloaking and overlay policy (Chapters 06–07) it will not.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — Build `aw-ot01`, the agentless PLC

**Objective.** Create the unpatchable device that answers Modbus TCP 502 and can host no agent.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 768 MB, 10 GB, one NIC → **VMnet3**. Hostname `aw-ot01`, `10.10.30.50/24`, gateway `10.10.30.254`, DNS `192.168.170.2`.

**Step 2.** Stand up a minimal Modbus responder, then treat the VM as a sealed appliance:

```bash
sudo apt update && sudo apt -y install python3-pip
pip3 install --user pymodbus==3.6.9
cat > ~/plc.py <<'EOF'
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [17]*100))
StartTcpServer(context=ModbusServerContext(slaves=store, single=True),
               address=("10.10.30.50", 502))
EOF
sudo tee /etc/systemd/system/plc.service > /dev/null <<'EOF'
[Unit]
Description=Toy Modbus PLC
After=network-online.target
[Service]
ExecStart=/usr/bin/python3 /home/labadmin/plc.py
User=labadmin
Restart=always
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now plc.service
sudo ss -ltnp | grep 502
```

**Expected result.** The listener is bound on `10.10.30.50:502`; from `aw-gw`, `nc -vz 10.10.30.50 502` connects.

**Negative test.** From the Windows host, `Test-NetConnection 10.10.30.50 -Port 502` fails — the host has no adapter on VMnet3. The PLC will reach the overlay only through the `aw-gw` gateway.

**Rollback.** None. Do not install anything else here — it cannot run an overlay agent, which is why Chapter 08 uses a gateway.

### Lab 4.6 — Snapshot the baseline

**Objective.** Capture a known-good state.

**Walkthrough**

Shut down all five guests cleanly, then take a snapshot named `baseline` on each.

**Expected result.** Each VM shows a `baseline` snapshot.

**Negative test.** Skip snapshots and an overlay mistake in Chapter 07 leaves you rebuilding. Take them.

**Rollback.** Leave the VMs powered off until Chapter 05.

## Summary and Completion Checklist

- [ ] `aw-gw` routes and masquerades; internal hosts reach the internet.
- [ ] `aw-db01` serves PostgreSQL with the `awlab` database (listening on all interfaces).
- [ ] `aw-app01` serves nginx and reaches the database (`~/checkdb.sh` prints 3).
- [ ] `aw-win01` is up as the SCADA/HMI workstation.
- [ ] `aw-ot01` answers Modbus TCP 502 and is reachable only via `aw-gw`.
- [ ] `baseline` snapshot taken on all five VMs.
