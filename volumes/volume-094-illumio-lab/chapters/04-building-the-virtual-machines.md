# Chapter 04: Building the Virtual Machines

## Learning Objectives

- Build the three-legged Linux router (`il-gw`) that joins the segments and later enforces on behalf of the PLC.
- Build the two-tier application: `il-app01` (nginx) and `il-db01` (PostgreSQL).
- Build the Windows SCADA/HMI workstation (`il-win01`).
- Build the agentless "PLC" (`il-ot01`) that answers Modbus TCP and can host no agent.
- Snapshot every VM at a known-good baseline.

Every static address in this chapter comes from the address plan in Chapter 01. Keep it in front of you.

## Hands-On Lab

### Lab 4.1 — Build `il-gw`, the three-legged router

**Objective.** Create the Ubuntu router with one NIC on each network, forwarding and masquerading so the internal segments reach the internet.

**Walkthrough**

**Step 1.** New VM in Workstation: Ubuntu Server 22.04.5, 1 vCPU, 1024 MB, 20 GB. Add **three** network adapters: NIC1 → **VMnet8**, NIC2 → **VMnet2**, NIC3 → **VMnet3**. Install Ubuntu with hostname `il-gw`, user `labadmin`, and OpenSSH enabled.

**Step 2.** After first boot, identify the interface names (`ip -br link`) — typically `ens33/ens34/ens35` in NIC order. Write the netplan:

```bash
sudo tee /etc/netplan/00-il-gw.yaml > /dev/null <<'EOF'
network:
  version: 2
  ethernets:
    ens33:                       # VMnet8 - IT / NAT
      addresses: [192.168.170.10/24]
      routes:
        - to: default
          via: 192.168.170.2
      nameservers:
        addresses: [192.168.170.2]
    ens34:                       # VMnet2 - Data Center
      addresses: [10.10.20.254/24]
    ens35:                       # VMnet3 - OT Cell
      addresses: [10.10.30.254/24]
EOF
sudo chmod 600 /etc/netplan/00-il-gw.yaml
sudo netplan apply
```

**Step 3.** Enable forwarding and masquerade the internal segments out of `ens33`:

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

**Expected result.** `ip -br addr` shows the three addresses. From `il-gw`, `ping -c1 192.168.170.2` and `ping -c1 8.8.8.8` succeed.

**Negative test.** Skip `net.ipv4.ip_forward=1`; the Data Center hosts you build next will reach `il-gw` but not the internet. Forwarding is what makes a router a router.

**Cleanup.** None.

### Lab 4.2 — Build `il-db01`, the PostgreSQL tier

**Objective.** Create the database, the crown jewel this lab exists to protect.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 1 vCPU, 1536 MB, one NIC → **VMnet2**. Hostname `il-db01`. Netplan:

```bash
sudo tee /etc/netplan/00-il-db01.yaml > /dev/null <<'EOF'
network:
  version: 2
  ethernets:
    ens33:
      addresses: [10.10.20.12/24]
      routes:
        - to: default
          via: 10.10.20.254
      nameservers:
        addresses: [192.168.170.2]
EOF
sudo chmod 600 /etc/netplan/00-il-db01.yaml
sudo netplan apply
```

**Step 2.** Install PostgreSQL and create the app database, listening on the segment address:

```bash
sudo apt update && sudo apt -y install postgresql
sudo -u postgres psql <<'SQL'
CREATE DATABASE illab;
CREATE USER appuser WITH PASSWORD 'LabAppPassw0rd!';
GRANT ALL PRIVILEGES ON DATABASE illab TO appuser;
\c illab
CREATE TABLE customers (id serial PRIMARY KEY, name text);
INSERT INTO customers (name) VALUES ('acme'), ('globex'), ('initech');
GRANT ALL ON ALL TABLES IN SCHEMA public TO appuser;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO appuser;
SQL
sudo sed -i "s/^#listen_addresses.*/listen_addresses = '10.10.20.12,127.0.0.1'/" \
    /etc/postgresql/*/main/postgresql.conf
echo "host illab appuser 10.10.20.0/24 md5" | \
    sudo tee -a /etc/postgresql/*/main/pg_hba.conf
sudo systemctl restart postgresql
```

**Expected result.** `sudo ss -ltnp | grep 5432` shows PostgreSQL listening on `10.10.20.12:5432`.

**Negative test.** Leave `listen_addresses` at `localhost`; the app tier cannot connect and you would wrongly blame the network. Confirm the listener before moving on.

**Cleanup.** None.

### Lab 4.3 — Build `il-app01`, the nginx application tier

**Objective.** Create the web/app tier whose only legitimate east-west dependency is the database.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 1 vCPU, 1536 MB, one NIC → **VMnet2**. Hostname `il-app01`, address `10.10.20.11/24`, gateway `10.10.20.254`, DNS `192.168.170.2` (same netplan shape as Lab 4.2).

**Step 2.** Install nginx and the PostgreSQL client, and a tiny page that proves the app→db path:

```bash
sudo apt update && sudo apt -y install nginx postgresql-client
echo "il-app01 nginx up" | sudo tee /var/www/html/index.html
cat > ~/checkdb.sh <<'EOF'
#!/usr/bin/env bash
PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d illab \
    -tAc "SELECT count(*) FROM customers;"
EOF
chmod +x ~/checkdb.sh
~/checkdb.sh
```

**Expected result.** `curl -s http://10.10.20.11` returns the page; `~/checkdb.sh` prints `3` — the legitimate app→db flow works.

**Negative test.** Stop PostgreSQL on `il-db01` and re-run `~/checkdb.sh`; it hangs then fails. This is the flow your policy must *permit*; remember what its success looks like so you notice if a rule breaks it.

**Cleanup.** Restart PostgreSQL on `il-db01` if you stopped it.

### Lab 4.4 — Build `il-win01`, the Windows SCADA/HMI workstation

**Objective.** Create the Windows workload that supervises the PLC — and, in Chapter 05, the machine an attacker pivots from.

**Walkthrough**

**Step 1.** New VM: Windows Server 2022 Evaluation, 2 vCPU, 4096 MB, 60 GB, one NIC → **VMnet2**. Complete the install, set Administrator password `LabAdminPassw0rd!`.

**Step 2.** Set the static address in an elevated PowerShell:

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet0" -IPAddress 10.10.20.21 `
    -PrefixLength 24 -DefaultGateway 10.10.20.254
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" -ServerAddresses 192.168.170.2
Rename-Computer -NewName "il-win01" -Restart
```

**Step 3.** After reboot, confirm it can supervise the PLC (the legitimate HMI→PLC flow), and reach the database (which it should *not* need — that becomes the lateral-movement path in Chapter 05):

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # HMI -> PLC (legitimate)
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # HMI -> DB (should be unnecessary)
```

**Expected result.** Both currently succeed (`TcpTestSucceeded : True`) — the flat network permits everything. That is the problem this lab fixes.

**Negative test.** Note that the HMI can reach the database at all. On a correctly segmented network it never should. Chapter 07 makes that true.

**Cleanup.** None.

### Lab 4.5 — Build `il-ot01`, the agentless PLC

**Objective.** Create the unpatchable device that answers Modbus TCP 502 and can host no security agent — the reason Chapter 08 exists.

**Walkthrough**

**Step 1.** New VM: Ubuntu Server 22.04.5, 1 vCPU, 768 MB, 10 GB, one NIC → **VMnet3** (the isolated OT cell). Hostname `il-ot01`, address `10.10.30.50/24`, gateway `10.10.30.254`, DNS `192.168.170.2`.

**Step 2.** Stand up a minimal Modbus TCP responder so the device behaves like a PLC. Treat this VM, from here on, as a sealed appliance — you will install nothing else on it:

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

**Expected result.** The listener is bound on `10.10.30.50:502`. From `il-gw`, `nc -vz 10.10.30.50 502` connects.

**Negative test.** Try to reach the PLC directly from the Windows host (`Test-NetConnection 10.10.30.50 -Port 502`). It fails — the host has no adapter on VMnet3. Only paths through `il-gw` can reach it, which is exactly the property Chapter 08 relies on.

**Cleanup.** None. Do not install an agent here; that is the whole point.

### Lab 4.6 — Snapshot the baseline

**Objective.** Capture a known-good state so every later chapter can be redone from a clean baseline.

**Walkthrough**

Shut down all five guests cleanly, then in Workstation take a snapshot named `baseline` on each: **VM → Snapshot → Take Snapshot**.

**Expected result.** Each VM shows a `baseline` snapshot in **VM → Snapshot → Snapshot Manager**.

**Negative test.** Skip snapshots and make a policy mistake in Chapter 07 that locks a host out; without a baseline your only recovery is a rebuild. Take the snapshots.

**Cleanup.** Leave the VMs powered off until Chapter 05.

## Summary and Completion Checklist

- [ ] `il-gw` routes and masquerades; internal hosts reach the internet.
- [ ] `il-db01` serves PostgreSQL on `10.10.20.12:5432` with the `illab` database.
- [ ] `il-app01` serves nginx and reaches the database (`~/checkdb.sh` prints 3).
- [ ] `il-win01` is up as the SCADA/HMI workstation.
- [ ] `il-ot01` answers Modbus TCP 502 and reachable only via `il-gw`.
- [ ] `baseline` snapshot taken on all five VMs.
