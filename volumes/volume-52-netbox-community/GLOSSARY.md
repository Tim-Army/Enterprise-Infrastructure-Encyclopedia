# Volume LII Glossary

Definitions for terms used in **Volume LII — NetBox Community Edition**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Aggregate** — A top-level IP block (from an RIR) that tracked prefixes roll up to.
Used in Chapter 04.

**Config context** — Scoped JSON data merged onto a device by criteria (site, role,
platform, tag); the data automation templates consume. Used in Chapter 06.

**Custom field** — A typed attribute (text, integer, boolean, selection, object) added
to a NetBox model without code. Used in Chapter 06.

**DCIM** — Data Center Infrastructure Management: the physical model (sites, racks,
devices, cabling, power). Used in Chapters 02–03.

**Device Type** — A reusable device template (from a manufacturer) carrying component
templates (interfaces, ports). Used in Chapter 02.

**Event rule** — A rule that fires an action (often a webhook) on object create/update/
delete. Used in Chapter 07.

**Export template** — A Jinja2 template that renders a queryset to text (CSV, YAML, a
config). Used in Chapter 06.

**IPAM** — IP Address Management: aggregates, prefixes, IP addresses, VLANs, and VRFs.
Used in Chapter 04.

**netbox-docker** — The community Docker Compose project for deploying NetBox. Used in
Chapter 01.

**NSoT (Network Source of Truth)** — An authoritative, intended-state data model that
automation reconciles against. Used in Chapter 01.

**Object permission** — A grant of actions on a model to users/groups, optionally
constrained by a query filter. Used in Chapter 08.

**pynetbox** — The official Python SDK for the NetBox REST API. Used throughout.

**Tenancy** — Attributing objects to a Tenant (optionally in a Tenant Group) for
ownership and filtering. Used in Chapter 05.

**VLAN Group** — A scope within which VLAN IDs are unique. Used in Chapter 04.

**VRF** — A Virtual Routing and Forwarding instance; a separate routing table that lets
overlapping IP space coexist. Used in Chapter 04.

**Webhook** — An outbound HTTP POST NetBox sends to an external system when an event
rule fires. Used in Chapter 07.
