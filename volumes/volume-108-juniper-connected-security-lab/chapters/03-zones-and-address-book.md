# Chapter 03: Zones and the Address Book

## Learning Objectives

- Assign each interface to a security zone.
- Build an address book of named endpoints and address sets.
- Confirm the zones exist and host-inbound traffic is controlled.
- Model the same zones and address sets in Track 2.

## Hands-On Lab

### Exercise 3.1 — Create the four security zones

**Objective.** Put each interface in its zone so the firewall will forward and enforce.

**Track 1 — Walkthrough.**

```text
[edit security zones]
set security-zone APP  interfaces ge-0/0/0.0
set security-zone DB   interfaces ge-0/0/1.0
set security-zone MGMT interfaces ge-0/0/2.0
set security-zone OT   interfaces ge-0/0/3.0
# allow ping to the SRX from each zone for testing
set security-zone APP  host-inbound-traffic system-services ping
set security-zone DB   host-inbound-traffic system-services ping
commit
```

**Expected result.**

```text
srx> show security zones
Security zone: APP   Interfaces: ge-0/0/0.0
Security zone: DB    Interfaces: ge-0/0/1.0
Security zone: MGMT  Interfaces: ge-0/0/2.0
Security zone: OT    Interfaces: ge-0/0/3.0
```

**Negative test.** With no `host-inbound-traffic` service, even a ping to the SRX interface is dropped — SRX zones are closed by default, including to the box itself. This is the default-deny posture in action.

**Track 2 — Walkthrough.** Model zones as nftables named sets mapping each subnet to a zone name via a verdict/lookup; first record the mapping:

```bash
sudo mkdir -p /etc/jsec
sudo tee /etc/jsec/zones > /dev/null <<'EOF'
10.20.1.0/24 APP
10.20.2.0/24 DB
10.20.3.0/24 MGMT
10.20.4.0/24 OT
EOF
cat /etc/jsec/zones
```

**Expected result.** Four subnet→zone rows — the Track 2 zone table.

**Cleanup.** Keep the zones.

### Exercise 3.2 — Build the address book

**Objective.** Name the endpoints so policies read by name, not by raw IP.

**Track 1 — Walkthrough.**

```text
[edit security address-book global]
set address web 10.20.1.10/32
set address db  10.20.2.10/32
set address hmi 10.20.3.10/32
set address plc 10.20.4.10/32
set address-set app-servers address web
commit
```

**Expected result.**

```text
srx> show configuration security address-book global
address web 10.20.1.10/32;
address db  10.20.2.10/32;
address hmi 10.20.3.10/32;
address plc 10.20.4.10/32;
address-set app-servers { address web; }
```

**Negative test.** A policy that references an address name not in the book fails to commit — the address book is the single source of named objects; typos are caught at commit, not at runtime.

**Track 2 — Walkthrough.** Record named addresses (an nftables set the policy chain will reference):

```bash
sudo tee /etc/jsec/addresses > /dev/null <<'EOF'
web 10.20.1.10
db  10.20.2.10
hmi 10.20.3.10
plc 10.20.4.10
EOF
sudo nft add table inet jsec
sudo nft add set inet jsec app_servers '{ type ipv4_addr ; elements = { 10.20.1.10 } }'
sudo nft list set inet jsec app_servers
```

**Expected result.** The `app_servers` set contains the web address — the Track 2 address-set.

**Cleanup.** Keep the address book.

## Summary and Completion Checklist

- [ ] Four zones created and interfaces assigned.
- [ ] Host-inbound default-deny confirmed (ping needs explicit permit).
- [ ] Address book of named endpoints built, with an app-servers set.
- [ ] Track 2 zone table and address set mirror the SRX config.
