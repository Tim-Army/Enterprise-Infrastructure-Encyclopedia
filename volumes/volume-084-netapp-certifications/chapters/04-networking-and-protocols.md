# Chapter 04: Networking and Protocols

## Learning Objectives

- Create logical interfaces (LIFs) and reason about IPspaces and broadcast domains.
- Serve NFS with an export policy.
- Share over SMB/CIFS.
- Provision a SAN LUN over iSCSI.
- Serve objects over ONTAP S3.
- Complete a walkthrough for each networking-and-protocol topic.

## Theory and Architecture

The NCDA's **Networking** and **Storage Protocols and Connectivity** domains cover how clients reach
ONTAP data. Client and management traffic ride **logical interfaces (LIFs)** — virtual network
interfaces bound to a port and owned by an SVM, freely movable across ports and nodes for
non-disruptive operations. **IPspaces** and **broadcast domains** isolate and group ports for
multi-tenant networks. On top of the network, ONTAP is **unified multiprotocol**: the same volume can be
served as **NAS** — **NFS** (export policies control access) and **SMB/CIFS** (shares) — and ONTAP also
serves **SAN** block storage — **iSCSI** and **FC/FCP** (and **NVMe/FC**) LUNs mapped to host
**initiator groups (igroups)** — and **ONTAP S3** object buckets. This chapter provisions each protocol
with hands-on ONTAP walkthroughs.

## Design Considerations

Give each SVM its own **data LIFs** and place them in the right **IPspace/broadcast domain**. Prefer
**NFS** for Linux/UNIX and **SMB** for Windows; the same volume can serve both (multiprotocol). Use
**iSCSI/FC** LUNs for block workloads (databases, VMware datastores) and map them to the correct
**igroup**. Serve **S3** for object/cloud-native workloads. Keep export policies and share ACLs least
privilege.

## Implementation and Automation

The labs create a data LIF, export a volume over NFS, share it over SMB, provision an iSCSI LUN with an
igroup, and enable an ONTAP S3 bucket — the multiprotocol access the NCDA validates.

## Validation and Troubleshooting

Confirm access:

```text
LIF = virtual NIC (SVM-owned, movable); IPspace/broadcast domain isolate + group ports
NAS: NFS (export policy) + SMB/CIFS (share) -- multiprotocol on one volume
SAN: iSCSI / FC / NVMe LUN mapped to an igroup (host initiators)
Object: ONTAP S3 bucket
```

Common pitfalls: an NFS mount failing because the **export policy** rule is missing or the LIF is on the
wrong subnet; and a LUN invisible to a host because it is mapped to the wrong **igroup**.

## Security and Best Practices

Scope **export policies** and **share ACLs** to the clients that need them, isolate tenants with
**IPspaces**, and map LUNs only to the intended **igroup**. Prefer Kerberos for NFS and signing for SMB
where required. All work is authorized administration.

## Hands-On Lab

Networking-and-protocol walkthroughs. **Shared prerequisites** — a Simulate ONTAP cluster with SVM
`svm_app` and volume `vol_finance` (Chapter 03), plus a free data port. **Cost:** none.

### Lab 4.1 — Create a data LIF

**Objective:** Give the SVM a network presence.

```text
cluster1::> network interface create -vserver svm_app -lif data1 -service-policy default-data-files \
  -home-node cluster1-01 -home-port e0d -address 192.168.10.20 -netmask 255.255.255.0
cluster1::> network interface show -vserver svm_app -fields address,status-admin,status-oper,home-port
vserver  lif    address        status-admin status-oper home-port
-------- ------ -------------- ------------ ----------- ---------
svm_app  data1  192.168.10.20  up           up          e0d
```

**Expected result:** an `up/up` data LIF on the SVM — clients can now reach it.

**Negative test:** place the LIF on a port in the wrong broadcast domain; clients on the intended subnet
cannot reach it — assign the correct home port/IPspace.

**Rollback:**

```text
cluster1::> network interface delete -vserver svm_app -lif data1
```

### Lab 4.2 — Export a volume over NFS

**Objective:** Serve NAS to UNIX clients.

```text
cluster1::> vserver nfs create -vserver svm_app -access true -v3 enabled
cluster1::> export-policy rule create -vserver svm_app -policyname default -clientmatch 192.168.10.0/24 \
  -rorule sys -rwrule sys -superuser sys -ruleindex 1
cluster1::> volume modify -vserver svm_app -volume vol_finance -policy default

cluster1::> export-policy rule show -vserver svm_app -policyname default
Vserver  Policy   Rule  Client Match      RO Rule RW Rule
-------- -------- ----- ----------------- ------- -------
svm_app  default  1     192.168.10.0/24   sys     sys
```

**Expected result:** the volume exported to the `192.168.10.0/24` clients — mountable over NFSv3.

**Negative test:** export with `-clientmatch 0.0.0.0/0` and `-rwrule any`; that opens the volume to
everyone — scope the rule to the client subnet.

**Rollback:**

```text
cluster1::> export-policy rule delete -vserver svm_app -policyname default -ruleindex 1
```

### Lab 4.3 — Provision an iSCSI LUN

**Objective:** Serve SAN block storage to a host.

```text
cluster1::> iscsi create -vserver svm_app
cluster1::> lun create -vserver svm_app -path /vol/vol_finance/lun0 -size 10GB -ostype linux
cluster1::> igroup create -vserver svm_app -igroup host1 -protocol iscsi -ostype linux \
  -initiator iqn.1994-05.com.redhat:host1
cluster1::> lun map -vserver svm_app -path /vol/vol_finance/lun0 -igroup host1

cluster1::> lun mapping show -vserver svm_app
Vserver  Path                        Igroup  LUN ID
-------- --------------------------- ------- ------
svm_app  /vol/vol_finance/lun0       host1   0
```

**Expected result:** a 10GB LUN mapped to the `host1` igroup — visible to that initiator only.

**Negative test:** map the LUN to an igroup holding the wrong initiator IQN; the host sees nothing —
map to the igroup containing the host's real IQN.

**Rollback:**

```text
cluster1::> lun unmap -vserver svm_app -path /vol/vol_finance/lun0 -igroup host1
cluster1::> lun delete -vserver svm_app -path /vol/vol_finance/lun0
cluster1::> igroup delete -vserver svm_app -igroup host1
```

### Lab 4.4 — Enable an ONTAP S3 bucket

**Objective:** Serve object storage.

```text
cluster1::> vserver object-store-server create -vserver svm_app -object-store-server s3.svm_app.local \
  -is-enabled true
cluster1::> vserver object-store-server bucket create -vserver svm_app -bucket data-lake \
  -size 50GB -aggr-list aggr1_data

cluster1::> vserver object-store-server bucket show -vserver svm_app -fields bucket,size
vserver  bucket     size
-------- ---------- -----
svm_app  data-lake  50GB
```

**Expected result:** an S3 bucket `data-lake` served by the SVM — object access alongside NAS and SAN.

**Negative test:** hand out the S3 root/admin key to applications; issue scoped **S3 users/access keys**
per application instead.

**Rollback:**

```text
cluster1::> vserver object-store-server bucket delete -vserver svm_app -bucket data-lake
cluster1::> vserver object-store-server delete -vserver svm_app
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ONTAP networking rides movable LIFs isolated by IPspaces and broadcast domains, and its unified
multiprotocol stack serves the same storage as NFS and SMB (NAS), iSCSI/FC/NVMe LUNs mapped to igroups
(SAN), and ONTAP S3 buckets (object) — the access model the NCDA validates.

- [ ] I can create a data LIF and reason about IPspaces.
- [ ] I can export a volume over NFS and share over SMB.
- [ ] I can provision an iSCSI LUN with an igroup.
- [ ] I can enable an ONTAP S3 bucket.
- [ ] I completed Labs 4.1–4.4 including each negative test.
