# Chapter 02: SSH Automation with Netmiko

## Learning Objectives

- Connect to network devices with Netmiko.
- Run show commands and capture output.
- Push configuration safely.
- Automate across many devices.
- Complete a walkthrough for each Netmiko skill.

## Theory and Architecture

**Netmiko** is the workhorse for **SSH automation** of network devices — it wraps Paramiko
with platform-aware handling of prompts, paging, and enable mode across many vendors
(`cisco_ios`, `arista_eos`, `juniper_junos`, etc.). You open a connection with a
**device dict** (`device_type`, `host`, credentials), run **`send_command`** for show
output (it disables paging and waits for the prompt) and **`send_config_set`** for
configuration, and iterate over an inventory to scale. Netmiko is CLI-based, so pair it
with parsing (Chapter 03) to get structured data.

## Design Considerations

Use **`send_command`** for reads and **`send_config_set`** for changes (it enters config
mode and exits cleanly). Set the correct **`device_type`** so prompt/enable handling
works. For many devices, iterate (or use Nornir, Chapter 07) and handle per-device
errors so one failure doesn't stop the run.

## Implementation and Automation

The labs use Netmiko to connect, read, configure, and loop over devices.

## Validation and Troubleshooting

Confirm the model:

```text
ConnectHandler(**device) -> send_command("show ...") ; send_config_set([...]).
device: {device_type, host, username, password, secret}. Save config explicitly.
```

Common pitfalls: wrong **`device_type`** (prompt mismatch); and forgetting to **save**
config (changes lost on reload).

## Security and Best Practices

Store credentials in a **vault/env**, use the right **`device_type`**, read before you
write, **save** config after changes, and handle per-device exceptions. Prefer key-based
SSH where supported.

## Hands-On Lab

Netmiko walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install netmiko`); a
lab device (or the patterns shown). **Cost:** none.

### Lab 2.1 — Connect and read

**Objective:** Open a connection and run a show command.

```python
from netmiko import ConnectHandler
dev = {"device_type":"cisco_ios","host":"10.0.0.11","username":"admin","password":"admin"}
with ConnectHandler(**dev) as conn:
    print(conn.send_command("show ip interface brief"))
```

**Expected result:** the interface-brief output — a working SSH read.

**Negative test:** set `device_type` to the wrong platform; **prompt/paging handling**
breaks — match the platform.

**Rollback:** the `with` block closes the connection.

### Lab 2.2 — Push configuration

**Objective:** Apply config with send_config_set.

```python
with ConnectHandler(**dev) as conn:
    out = conn.send_config_set(["interface Lo100", "description automated", "ip address 10.100.0.1 255.255.255.255"])
    conn.save_config()          # write mem / commit
    print(out)
```

**Expected result:** the config applied and **saved** — a persistent change.

**Negative test:** apply config but skip **`save_config`**; changes are **lost on reload**
— save them.

**Rollback:** remove the loopback (`no interface Lo100`).

### Lab 2.3 — Handle enable/secret

**Objective:** Enter privileged mode when needed.

```python
dev2 = {**dev, "secret":"enablepass"}
with ConnectHandler(**dev2) as conn:
    conn.enable()               # enter privileged EXEC
    print(conn.find_prompt())   # ends with '#'
```

**Expected result:** a **`#`** privileged prompt — enable handled.

**Negative test:** run config while in user EXEC without `enable()`; commands are
**rejected** — enter privileged mode.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Loop over many devices

**Objective:** Automate across an inventory with error handling.

```python
inventory = [{"device_type":"cisco_ios","host":h,"username":"admin","password":"admin"} for h in ("10.0.0.11","10.0.0.12")]
for d in inventory:
    try:
        with ConnectHandler(**d) as c:
            print(d["host"], c.send_command("show version | include uptime"))
    except Exception as e:
        print(d["host"], "ERROR", e)
```

**Expected result:** per-device output, with failures **caught** — resilient fan-out.

**Negative test:** let one unreachable device raise and abort the loop; **catch
per-device** so the rest continue.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Netmiko automates SSH: connect with a device dict, `send_command` to read, `send_config_set`
to change (then save), enter enable mode when needed, and loop over an inventory with
per-device error handling. This chapter did each.

- [ ] I can connect and run show commands.
- [ ] I can push and save configuration.
- [ ] I can handle enable/secret.
- [ ] I can loop over devices with error handling.
- [ ] I completed Labs 2.1–2.4 including each negative test.
