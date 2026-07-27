# Chapter 02: DCIM — Sites, Racks, and Devices

## Learning Objectives

- Model the physical hierarchy: regions, sites, locations, racks.
- Define device types from manufacturers and roles.
- Install devices into racks with positions and faces.
- Use the REST API to create and query DCIM objects.
- Complete a walkthrough for each DCIM building block.

## Theory and Architecture

**DCIM** (Data Center Infrastructure Management) models the **physical** world. The
hierarchy is **Region → Site → Location → Rack**, and equipment is a **Device** of a
given **Device Type** (from a **Manufacturer**) and **Device Role**, mounted at a
**position** and **face** in a rack. Device Types are reusable templates carrying
interfaces, power ports, and console ports.

## Design Considerations

Model **once, reuse many**: define a Device Type with its components, then instantiate
devices from it. Use **Device Roles** (e.g., leaf, spine, firewall) for classification
and coloring, and **Sites/Locations** for physical grouping. Racks track **U-space**,
so positions must not overlap.

## Implementation and Automation

The labs use `pynetbox`/`curl` to build the hierarchy — site, rack, manufacturer,
device type, role, and device.

## Validation and Troubleshooting

Confirm the model:

```text
DCIM hierarchy: Region > Site > Location > Rack
Device = Device Type (Manufacturer) + Device Role, mounted at position/face in a Rack.
```

Common pitfalls: placing a device at an occupied U-position; and creating devices with
no **Device Type** (no component templates).

## Security and Best Practices

Standardize **Device Types** (import from the community device-type library), name
consistently, track **rack elevations** to avoid overlaps, and use **roles** for
classification. Keep the physical model accurate — automation depends on it.

## Hands-On Lab

DCIM walkthroughs. **Shared prerequisites** — a running NetBox (`$NB`, `$TOKEN` set);
`pip install pynetbox`. **Cost:** none.

### Lab 2.1 — Create a site

**Objective:** Create a site via the API.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
site = nb.dcim.sites.create(name="DC1", slug="dc1", status="active")
print("site id:", site.id, "status:", site.status.value)
```

**Expected result:** a new **site "DC1"** with status `active` — the top of the
physical hierarchy.

**Negative test:** create two sites with the same **slug**; slugs are unique — NetBox
rejects the duplicate.

**Cleanup:** `nb.dcim.sites.get(site.id).delete()`.

### Lab 2.2 — Add a rack

**Objective:** Create a 42U rack in the site.

```python
rack = nb.dcim.racks.create(name="R01", site=site.id, u_height=42, status="active")
print("rack:", rack.name, "height:", rack.u_height)
```

**Expected result:** a **42U rack "R01"** in DC1 — U-space to mount devices.

**Negative test:** mount a device beyond U42; NetBox rejects positions outside the
rack height.

**Cleanup:** `rack.delete()`.

### Lab 2.3 — Define a device type

**Objective:** Create a manufacturer and device type.

```python
mfr = nb.dcim.manufacturers.create(name="Acme", slug="acme")
dt = nb.dcim.device_types.create(manufacturer=mfr.id, model="AX-1", slug="ax-1", u_height=1)
print("device type:", dt.model, "1U from", mfr.name)
```

**Expected result:** a **1U device type "AX-1"** from Acme — a reusable template.

**Negative test:** create devices without a device type; you lose the **component
templates** (interfaces/ports) — model the type first.

**Cleanup:** `dt.delete(); mfr.delete()`.

### Lab 2.4 — Install a device in the rack

**Objective:** Create a device mounted at a rack position.

```python
role = nb.dcim.device_roles.create(name="leaf", slug="leaf", color="00ff00")
dev = nb.dcim.devices.create(name="leaf01", device_type=dt.id, role=role.id,
                             site=site.id, rack=rack.id, position=1, face="front")
print("device:", dev.name, "@ U", dev.position, dev.face.value)
```

**Expected result:** **leaf01** mounted at **U1, front** — a device placed in the
model.

**Negative test:** place a second device at U1; the position is occupied — NetBox
prevents the overlap.

**Cleanup:** `dev.delete(); role.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

DCIM models the physical estate: Region → Site → Location → Rack, with Devices
instantiated from reusable Device Types and classified by Role, mounted at rack
positions. This chapter built the hierarchy through the REST API.

- [ ] I can create sites, locations, and racks.
- [ ] I can define manufacturers and device types.
- [ ] I can classify devices with roles.
- [ ] I can install devices at rack positions without overlap.
- [ ] I completed Labs 2.1–2.4 including each negative test.
