# Chapter 06: Configuration Templating with Jinja2

## Learning Objectives

- Explain why templated config beats hand-editing.
- Render device config from data with Jinja2.
- Use variables, loops, and conditionals.
- Separate data (source of truth) from templates.
- Complete a walkthrough for each templating skill.

## Theory and Architecture

**Config templating** generates device configuration from **structured data** and a
**template**, so the config is consistent, versioned, and driven by a source of truth
rather than typed by hand. **Jinja2** is the standard engine: templates contain
**variables** (`{{ }}`), **control flow** (`{% for %}`, `{% if %}`), and **filters**. The
pattern is **data (YAML/JSON/NetBox) + template → rendered config**, which you then push
with Netmiko/NAPALM/NETCONF. This is the heart of intent-based networking: change the
data, re-render, deploy.

## Design Considerations

Keep **data separate from templates** — variables in YAML/a source of truth, logic in the
template. Use **loops** for repeated stanzas (interfaces, VLANs, neighbors) and
**conditionals** for optional features. Render and **review the diff** before deploying.

## Implementation and Automation

The labs render config with Jinja2 variables, loops, and conditionals, sourced from data.

## Validation and Troubleshooting

Confirm the model:

```text
Data (YAML/JSON/NetBox) + Jinja2 template -> rendered config -> push (Netmiko/NAPALM).
Jinja2: {{ var }} ; {% for x in xs %} ; {% if cond %} ; | filters.
```

Common pitfalls: logic and data mixed in one file (unmaintainable); and deploying
rendered config without a **diff review**.

## Security and Best Practices

Store **data in a source of truth**, keep templates **logic-focused and versioned**,
render then **diff before deploy**, and validate the output. Never embed secrets in
templates.

## Hands-On Lab

Templating walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install jinja2
pyyaml`). Labs run locally. **Cost:** none.

### Lab 6.1 — Render with a variable

**Objective:** Substitute a value into a template.

```python
from jinja2 import Template
t = Template("hostname {{ name }}\n")
print(t.render(name="core-sw1"))   # hostname core-sw1
```

**Expected result:** `hostname core-sw1` — variable substitution.

**Negative test:** build config with f-strings and manual escaping; **Jinja2** scales to
real templates — use it.

**Cleanup:** none.

### Lab 6.2 — Loop over a list

**Objective:** Generate repeated stanzas.

```python
from jinja2 import Template
t = Template("{% for v in vlans %}vlan {{ v.id }}\n name {{ v.name }}\n{% endfor %}")
print(t.render(vlans=[{"id":10,"name":"users"},{"id":20,"name":"voice"}]))
```

**Expected result:** two `vlan` stanzas from the list — data-driven repetition.

**Negative test:** copy-paste each VLAN stanza by hand; a **loop** stays correct as the
data grows.

**Cleanup:** none.

### Lab 6.3 — Conditionals

**Objective:** Include config only when needed.

```python
from jinja2 import Template
t = Template("interface {{ intf }}\n{% if shutdown %} shutdown\n{% endif %}")
print(t.render(intf="Gi1", shutdown=True))
```

**Expected result:** the interface with `shutdown` present — conditional config.

**Negative test:** maintain separate templates per variant; a **conditional** keeps one
template — DRY.

**Cleanup:** none.

### Lab 6.4 — Data-driven from YAML

**Objective:** Render config from a source-of-truth file.

```python
import yaml
from jinja2 import Template
data = yaml.safe_load("host: r1\ninterfaces:\n  - {name: Gi1, ip: 10.0.0.1}\n")
t = Template("hostname {{ host }}\n{% for i in interfaces %}interface {{ i.name }}\n ip address {{ i.ip }} 255.255.255.0\n{% endfor %}")
print(t.render(**data))
```

**Expected result:** full config rendered from the **YAML data** — intent → config.

**Negative test:** hard-code values in the template; keep **data external** so one
template serves many devices.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Jinja2 renders consistent device config from structured data (source of truth) using
variables, loops, and conditionals — data separate from template, diffed before deploy.
This chapter rendered config from variables, loops, conditionals, and YAML data.

- [ ] I can render config with variables.
- [ ] I can loop over lists for repeated stanzas.
- [ ] I can include config conditionally.
- [ ] I can render from external YAML data.
- [ ] I completed Labs 6.1–6.4 including each negative test.
