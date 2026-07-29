# Chapter 03: Parsing Device Output

## Learning Objectives

- Explain why structured data beats raw CLI text.
- Parse with TextFSM and ntc-templates.
- Use Genie parsers and TTP.
- Fall back to regex when needed.
- Complete a walkthrough for each parsing approach.

## Theory and Architecture

CLI output is **text**, but automation needs **structured data** (dicts/lists) to make
decisions. Parsers bridge the gap: **TextFSM** (template-based state machines) with the
community **ntc-templates** library covers hundreds of `show` commands; **Genie** parsers
(from pyATS) return rich structured data for Cisco platforms; **TTP** (Template Text
Parser) offers a Jinja-like reverse-template syntax; and plain **regex** handles one-offs.
`send_command(..., use_textfsm=True)` in Netmiko returns parsed data directly.

## Design Considerations

Prefer an **existing parser** (ntc-templates/Genie) over hand-written regex — they're
tested and maintained. Use **TextFSM** for multi-vendor CLI, **Genie** for deep Cisco
structure, **TTP** for custom formats, and **regex** only for simple extractions.

## Implementation and Automation

The labs parse CLI text with TextFSM/ntc-templates, TTP, and regex.

## Validation and Troubleshooting

Confirm the tools:

```text
TextFSM + ntc-templates: parse show output to list-of-dicts (Netmiko use_textfsm=True).
Genie: device.parse("show ...") -> structured dict. TTP: reverse-template parsing. regex: one-offs.
```

Common pitfalls: brittle **regex** where a parser exists; and assuming parser output
shape without checking.

## Security and Best Practices

Use **maintained parsers** (ntc-templates/Genie), validate the parsed structure before
acting, and keep custom templates in version control. Reserve regex for trivial cases.

## Hands-On Lab

Parsing walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install textfsm
ntc-templates ttp`). Sample output is embedded, so labs run without a device. **Cost:**
none.

### Lab 3.1 — Parse with TextFSM + ntc-templates

**Objective:** Turn `show ip int brief` text into records.

```python
from ntc_templates.parse import parse_output
text = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       10.0.0.11       YES manual up                    up
GigabitEthernet2       unassigned      YES unset  administratively down down"""
rows = parse_output(platform="cisco_ios", command="show ip interface brief", data=text)
print(rows[0]["intf"], rows[0]["ipaddr"])
```

**Expected result:** structured fields (interface + IP) — CLI text parsed to data.

**Negative test:** hand-write a regex for every show command; **ntc-templates** already
covers them — reuse.

**Cleanup:** none.

### Lab 3.2 — Netmiko with use_textfsm

**Objective:** Get parsed data directly from Netmiko.

```python
# with a live device:
# data = conn.send_command("show ip interface brief", use_textfsm=True)
# print(data[0]["status"])   # 'up' — already a list of dicts
print("use_textfsm=True returns a list of dicts, no manual parsing")
```

**Expected result:** parsed structured output straight from the read — no separate parse
step.

**Negative test:** parse Netmiko's raw string by hand; pass **`use_textfsm=True`** to get
data directly.

**Cleanup:** none.

### Lab 3.3 — TTP custom template

**Objective:** Parse a custom format with TTP.

```python
from ttp import ttp
data = "hostname r1\ninterface Gi1\n ip address 10.0.0.11 255.255.255.0"
template = "interface {{ intf }}\n ip address {{ ip }} {{ mask }}"
parser = ttp(data=data, template=template); parser.parse()
print(parser.result()[0][0])
```

**Expected result:** the extracted interface/ip/mask — a custom reverse-template parse.

**Negative test:** force ntc-templates onto a non-standard format; **TTP** handles custom
layouts — use it there.

**Cleanup:** none.

### Lab 3.4 — Regex for a one-off

**Objective:** Extract a value with a regex.

```python
import re
version = "Cisco IOS XE Software, Version 17.09.04a"
m = re.search(r"Version (\S+)", version)
print(m.group(1))   # 17.09.04a
```

**Expected result:** **`17.09.04a`** — a simple regex extraction.

**Negative test:** build a full parser for a single value; a **regex** suffices for
one-offs — don't over-engineer.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Parsing turns CLI text into structured data: TextFSM/ntc-templates and Genie for
maintained coverage, TTP for custom formats, and regex for one-offs — with Netmiko's
`use_textfsm=True` doing it inline. This chapter parsed with each approach.

- [ ] I can parse with TextFSM/ntc-templates.
- [ ] I can get parsed data from Netmiko directly.
- [ ] I can write a TTP template for custom output.
- [ ] I can use regex for a one-off extraction.
- [ ] I completed Labs 3.1–3.4 including each negative test.
