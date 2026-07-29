# Chapter 06: Customization — Fields, Tags, and Config Contexts

## Learning Objectives

- Extend the data model with custom fields.
- Classify objects with tags.
- Deliver structured data to devices with config contexts.
- Generate output with export templates.
- Complete a walkthrough for each customization feature.

## Theory and Architecture

NetBox is extensible without code. **Custom fields** add typed attributes to any model
(text, integer, boolean, selection, object). **Tags** are free-form labels for
cross-cutting classification and filtering. **Config contexts** attach structured JSON
to objects by criteria (site, role, platform, tag), merged and rendered per device —
the data your automation templates consume. **Export templates** render objects to
text (CSV, YAML, a config) via Jinja2.

## Design Considerations

Add **custom fields** for attributes the core model lacks (e.g., asset tag, support
contract). Use **tags** for lightweight grouping. Put automation input in **config
contexts** (NTP servers, SNMP strings) so it merges by scope. Use **export templates**
to feed downstream tools a rendered artifact.

## Implementation and Automation

The labs use `pynetbox`/`curl` to create a custom field, tag an object, define a config
context, and add an export template.

## Validation and Troubleshooting

Confirm the features:

```text
Custom field: typed attribute on a model. Tag: cross-cutting label.
Config context: scoped JSON merged onto an object (device.config_context).
Export template: Jinja2 rendering of a queryset.
```

Common pitfalls: overusing custom fields where a related model fits; and config
contexts scoped too broadly (unexpected merges).

## Security and Best Practices

Keep custom fields **typed and minimal**, tag consistently, scope **config contexts**
precisely (site/role/platform/tag), and version **export templates**. Treat config
contexts as the contract between NetBox and your automation.

## Hands-On Lab

Customization walkthroughs. **Shared prerequisites** — a running NetBox with a device;
`$NB`/`$TOKEN`; `pynetbox`. **Cost:** none.

### Lab 6.1 — Add a custom field

**Objective:** Add an `asset_tag_ext` text field to devices.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
cf = nb.extras.custom_fields.create(
  object_types=["dcim.device"], name="asset_tag_ext", type="text", label="Asset Tag (Ext)")
print("custom field:", cf.name, "on", cf.object_types)
```

**Expected result:** a **custom field** attached to the device model — an extra typed
attribute.

**Negative test:** stuff extra data in the description; a **typed custom field** is
queryable and validated — use it.

**Cleanup:** `cf.delete()`.

### Lab 6.2 — Tag an object

**Objective:** Create a tag and apply it to a device.

```python
tag = nb.extras.tags.create(name="edge", slug="edge")
dev = nb.dcim.devices.get(name="leaf01"); dev.tags = [tag.id]; dev.save()
print("leaf01 tags:", [t.name for t in nb.dcim.devices.get(dev.id).tags])
```

**Expected result:** leaf01 carrying the **edge** tag — cross-cutting classification.

**Negative test:** encode classification in the name (`leaf01-edge`); a **tag** filters
cleanly across models — prefer it.

**Cleanup:** `dev.tags=[]; dev.save(); tag.delete()`.

### Lab 6.3 — Define a config context

**Objective:** Attach NTP data scoped to a site.

```python
site = nb.dcim.sites.get(name="DC1")
cc = nb.extras.config_contexts.create(
  name="ntp-dc1", weight=1000, data={"ntp_servers":["10.0.0.1","10.0.0.2"]}, sites=[site.id])
dev = nb.dcim.devices.get(name="leaf01")
print("leaf01 rendered context:", nb.dcim.devices.get(dev.id).config_context.get("ntp_servers"))
```

**Expected result:** leaf01's `config_context` includes the **NTP servers** from the
site-scoped context — merged automation data.

**Negative test:** hard-code NTP in each device; a **config context** applies by scope
and stays DRY.

**Cleanup:** `cc.delete()`.

### Lab 6.4 — Add an export template

**Objective:** Render devices to a simple inventory line.

```python
tmpl = nb.extras.export_templates.create(
  object_types=["dcim.device"], name="dev-inv",
  template_code="{% for d in queryset %}{{ d.name }},{{ d.site.name }}\n{% endfor %}")
print("export template:", tmpl.name)
# Then GET /api/dcim/devices/?export=dev-inv  returns rendered CSV-like text.
```

**Expected result:** an **export template** that renders `name,site` per device — a
downstream artifact.

**Negative test:** hand-build inventory files; an **export template** renders live from
the source of truth — no drift.

**Cleanup:** `tmpl.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NetBox extends without code: custom fields add typed attributes, tags classify,
config contexts deliver scoped JSON to devices, and export templates render objects to
text. This chapter used each to shape data for automation.

- [ ] I can add typed custom fields.
- [ ] I can classify objects with tags.
- [ ] I can define scoped config contexts.
- [ ] I can render objects with export templates.
- [ ] I completed Labs 6.1–6.4 including each negative test.
