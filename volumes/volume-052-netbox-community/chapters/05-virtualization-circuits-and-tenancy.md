# Chapter 05: Virtualization, Circuits, and Tenancy

## Learning Objectives

- Model virtual machines in clusters with the virtualization model.
- Represent WAN/transport with providers and circuits.
- Attribute objects to tenants for multi-tenant tracking.
- Query these objects through the REST API.
- Complete a walkthrough for each model.

## Theory and Architecture

Beyond physical DCIM, NetBox models **virtualization** (a **Cluster** of a Cluster
Type/Group hosting **Virtual Machines** with virtual interfaces and resources),
**circuits** (a **Provider** delivering a **Circuit** of a **Circuit Type**, terminated
at sites), and **tenancy** (a **Tenant**, optionally in a Tenant Group, that owns
objects across DCIM/IPAM). Tenancy is the cross-cutting "who owns this" axis.

## Design Considerations

Model **VMs** alongside physical devices so IPAM and automation see both. Track
**circuits** for WAN/transport with committed rates and terminations. Use **tenants**
to attribute sites, prefixes, devices, and VMs to a customer/business unit — essential
for multi-tenant environments.

## Implementation and Automation

The labs use `pynetbox`/`curl` to create a cluster + VM, a provider + circuit, and a
tenant.

## Validation and Troubleshooting

Confirm the models:

```text
Virtualization: Cluster (Type/Group) -> Virtual Machine -> VM interfaces.
Circuits: Provider -> Circuit (Type) -> terminations at sites.
Tenancy: Tenant (Group) owns objects across DCIM/IPAM.
```

Common pitfalls: creating VMs with no **cluster**; and objects with no **tenant** in a
multi-tenant deployment.

## Security and Best Practices

Assign every VM to a **cluster**, record **circuits** with providers and committed
rates, and attribute objects to **tenants** for ownership and filtering. Consistent
tenancy makes reporting and RBAC scoping possible.

## Hands-On Lab

Walkthroughs. **Shared prerequisites** — a running NetBox with a site; `$NB`/`$TOKEN`;
`pynetbox`. **Cost:** none.

### Lab 5.1 — Create a cluster and VM

**Objective:** Model a virtualization cluster and a VM.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
ct = nb.virtualization.cluster_types.create(name="KVM", slug="kvm")
cl = nb.virtualization.clusters.create(name="cluster1", type=ct.id)
vm = nb.virtualization.virtual_machines.create(name="web01", cluster=cl.id, vcpus=2, memory=4096)
print("VM:", vm.name, "vcpus:", vm.vcpus, "in", cl.name)
```

**Expected result:** a **VM "web01"** (2 vCPU, 4 GB) in cluster1 — the virtualization
model.

**Negative test:** create a VM with no cluster; VMs require a **cluster** — model it
first.

**Rollback:** `vm.delete(); cl.delete(); ct.delete()`.

### Lab 5.2 — Add a VM interface with an IP

**Objective:** Attach a virtual interface and assign an IP.

```python
vmi = nb.virtualization.interfaces.create(virtual_machine=vm.id, name="eth0")
ip = nb.ipam.ip_addresses.create(address="10.1.0.10/24",
     assigned_object_type="virtualization.vminterface", assigned_object_id=vmi.id)
print("assigned", ip.address, "to", vm.name, vmi.name)
```

**Expected result:** **10.1.0.10/24** assigned to web01:eth0 — IPAM and virtualization
joined.

**Negative test:** track the VM's IP in a note; **assign it in IPAM** so it counts
against the prefix and is discoverable.

**Rollback:** `ip.delete(); vmi.delete()`.

### Lab 5.3 — Model a circuit

**Objective:** Create a provider and a circuit.

```python
prov = nb.circuits.providers.create(name="Telco", slug="telco")
ctype = nb.circuits.circuit_types.create(name="Internet", slug="internet")
ckt = nb.circuits.circuits.create(cid="CKT-001", provider=prov.id, type=ctype.id, status="active")
print("circuit:", ckt.cid, "from", prov.name)
```

**Expected result:** an active **circuit "CKT-001"** from Telco — the WAN/transport
model.

**Negative test:** track circuits in email; model them in NetBox so **terminations** and
capacity are authoritative.

**Rollback:** `ckt.delete(); ctype.delete(); prov.delete()`.

### Lab 5.4 — Attribute objects to a tenant

**Objective:** Create a tenant and assign an object to it.

```python
tg = nb.tenancy.tenant_groups.create(name="Customers", slug="customers")
tenant = nb.tenancy.tenants.create(name="Acme Corp", slug="acme-corp", group=tg.id)
site = nb.dcim.sites.get(name="DC1"); site.tenant = tenant.id; site.save()
print("site", site.name, "tenant:", nb.dcim.sites.get(site.id).tenant.name)
```

**Expected result:** DC1 attributed to **Acme Corp** — the tenancy ownership axis.

**Negative test:** leave objects tenant-less in a multi-tenant NetBox; **assign
tenants** so ownership/filtering works.

**Rollback:** `site.tenant=None; site.save(); tenant.delete(); tg.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NetBox models virtualization (clusters and VMs with interfaces/IPs), circuits
(providers and terminated circuits), and tenancy (tenants owning objects across the
model). This chapter created a VM, a circuit, and a tenant through the API.

- [ ] I can model clusters and virtual machines.
- [ ] I can assign IPs to VM interfaces.
- [ ] I can model providers and circuits.
- [ ] I can attribute objects to tenants.
- [ ] I completed Labs 5.1–5.4 including each negative test.
