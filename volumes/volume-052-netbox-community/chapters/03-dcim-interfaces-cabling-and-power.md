# Chapter 03: DCIM — Interfaces, Cabling, and Power

## Learning Objectives

- Add interfaces and other components to devices.
- Model cables connecting two termination points and trace them.
- Represent power: power ports, feeds, and panels.
- Query connections through the REST API.
- Complete a walkthrough for each connectivity building block.

## Theory and Architecture

Devices carry **components**: interfaces, console ports, power ports, and more. A
**Cable** connects two **termination points** (e.g., interface↔interface,
front-port↔rear-port for patch panels), and NetBox can **trace** an end-to-end path
across patch panels. Power is modeled as **power feeds** from **power panels** to
device **power ports**, letting you track draw and redundancy.

## Design Considerations

Model connectivity to the fidelity you will automate against: interface names must
match the real devices for automation to bind. Use **front/rear ports** for patch
panels so cable **tracing** works. Track **power** for capacity and A/B redundancy.

## Implementation and Automation

The labs use `pynetbox`/`curl` to add interfaces, cable them, trace the path, and model
power.

## Validation and Troubleshooting

Confirm the model:

```text
Component (interface/port) on a Device; Cable connects two terminations;
trace() walks through patch panels; PowerFeed (from PowerPanel) -> device PowerPort.
```

Common pitfalls: cabling two interfaces already terminated (a termination has one
cable); and interface names that don't match the real device.

## Security and Best Practices

Name interfaces to match device config, model **patch panels** with front/rear ports
for accurate tracing, and track **power feeds** with A/B redundancy. Keep connectivity
current so automation and capacity planning stay correct.

## Hands-On Lab

Connectivity walkthroughs. **Shared prerequisites** — a running NetBox with two devices
(`leaf01`, `leaf02`) in a site; `$NB`/`$TOKEN` set; `pynetbox`. **Cost:** none.

### Lab 3.1 — Add interfaces

**Objective:** Add an interface to each device.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
d1 = nb.dcim.devices.get(name="leaf01"); d2 = nb.dcim.devices.get(name="leaf02")
i1 = nb.dcim.interfaces.create(device=d1.id, name="eth1", type="10gbase-t")
i2 = nb.dcim.interfaces.create(device=d2.id, name="eth1", type="10gbase-t")
print("interfaces:", i1.name, "/", i2.name)
```

**Expected result:** an `eth1` interface on each device — termination points for a
cable.

**Negative test:** duplicate `eth1` on the same device; interface names are unique per
device — NetBox rejects it.

**Rollback:** `i1.delete(); i2.delete()`.

### Lab 3.2 — Cable two interfaces

**Objective:** Connect the interfaces with a cable.

```python
cable = nb.dcim.cables.create(
  a_terminations=[{"object_type":"dcim.interface","object_id":i1.id}],
  b_terminations=[{"object_type":"dcim.interface","object_id":i2.id}],
  status="connected")
print("cable id:", cable.id, "status:", cable.status.value)
```

**Expected result:** a **connected cable** between leaf01:eth1 and leaf02:eth1.

**Negative test:** cable `i1` to a third interface while it's already terminated; a
termination holds **one** cable — remove the first.

**Rollback:** `cable.delete()`.

### Lab 3.3 — Trace the connection

**Objective:** Confirm the connected endpoint via the API.

```python
i1 = nb.dcim.interfaces.get(i1.id)
print("leaf01:eth1 connected to:", i1.connected_endpoints)
```

**Expected result:** the connected endpoint resolving to **leaf02:eth1** — the trace
across the cable.

**Negative test:** trust a spreadsheet of connections; **trace in NetBox** — it walks
patch panels the spreadsheet won't.

**Rollback:** none (read-only).

### Lab 3.4 — Model power

**Objective:** Create a power panel, feed, and device power port.

```python
site = d1.site
panel = nb.dcim.power_panels.create(site=site.id, name="PP1")
feed = nb.dcim.power_feeds.create(power_panel=panel.id, name="A-feed", status="active")
pp = nb.dcim.power_ports.create(device=d1.id, name="PSU1")
print("power:", panel.name, feed.name, pp.name)
```

**Expected result:** a power **panel, feed, and device power port** — the power model
for capacity/redundancy.

**Negative test:** ignore power modeling; without **feeds/ports** you cannot track draw
or A/B redundancy — model it.

**Rollback:** `pp.delete(); feed.delete(); panel.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Connectivity in DCIM is interfaces/ports joined by cables (traceable across patch
panels) and power modeled as panels → feeds → device power ports. This chapter cabled
two devices, traced the link, and modeled power via the REST API.

- [ ] I can add interfaces and components to devices.
- [ ] I can cable two terminations and respect the one-cable rule.
- [ ] I can trace a connection through the API.
- [ ] I can model power panels, feeds, and ports.
- [ ] I completed Labs 3.1–3.4 including each negative test.
