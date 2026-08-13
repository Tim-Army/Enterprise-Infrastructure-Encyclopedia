# Chapter 06: Endpoint Lockdown with StellarProtect

## Learning Objectives

- Lock an OT host to an application allowlist so only approved software runs.
- Confirm an approved binary runs and an unapproved (malware) binary is blocked.
- Understand why endpoint lockdown complements the inline network shield.

## The host is the other half

The inline shield protects the wire, but the engineering workstation (EWS) that programs the PLC is itself a target — one malicious executable there can push a malicious logic change the PLC will accept. **StellarProtect** answers this with **application lockdown**: the host runs an **allowlist** of approved software and blocks everything else, which suits OT because the approved software set is small and stable. This chapter models lockdown on the EWS.

## Hands-On Lab

### Exercise 6.1 — Build the application allowlist

**Objective.** Define which programs are approved on the EWS.

**Track 1 — Walkthrough.** StellarProtect learns or is given the approved application set (by hash), then enters **lockdown**: only listed applications may execute; anything else is denied and logged.

**Track 2 — Walkthrough.** Model lockdown with an allowlist of approved program hashes and a launcher that enforces it. Save the launcher as `/usr/local/bin/stellar-run`:

```bash
sudo tee /usr/local/bin/stellar-run >/dev/null <<'SH'
#!/bin/bash
# usage: stellar-run <program> [args...]  -- runs only allowlisted programs
prog="$1"; h=$(sha256sum "$prog" 2>/dev/null | cut -d' ' -f1)
if grep -q "^$h " /etc/txone/allowlist 2>/dev/null; then
  shift; exec "$prog" "$@"
else
  logger -t stellar "BLOCKED $prog ($h)"; echo "StellarProtect: BLOCKED (not allowlisted)"; exit 1
fi
SH
sudo chmod +x /usr/local/bin/stellar-run

# approve the legitimate HMI client (compute and record its hash)
sudo mkdir -p /etc/txone
printf '#!/bin/bash\necho "hmi-tool: reading PLC"\n' | sudo tee /usr/local/bin/hmi-tool >/dev/null
sudo chmod +x /usr/local/bin/hmi-tool
echo "$(sha256sum /usr/local/bin/hmi-tool | cut -d' ' -f1) hmi-tool" | sudo tee /etc/txone/allowlist >/dev/null
cat /etc/txone/allowlist
```

**Expected result.** The allowlist contains the approved `hmi-tool` hash — the only program permitted to run under lockdown.

**Negative test.** An allowlist that matches by *name* rather than *hash* would let malware named `hmi-tool` run; hashing the binary is what makes the lockdown meaningful.

**Rollback.** Keep the allowlist and launcher.

### Exercise 6.2 — Approved runs, malware is blocked

**Objective.** Prove lockdown permits the approved tool and blocks an unapproved one.

**Track 2 — Walkthrough.** Create a malicious program and try to run both through the lockdown launcher:

```bash
printf '#!/bin/bash\necho "malware: pushing bad logic to PLC"\n' | sudo tee /usr/local/bin/evil-tool >/dev/null
sudo chmod +x /usr/local/bin/evil-tool
# approved program runs
sudo ip netns exec ews /usr/local/bin/stellar-run /usr/local/bin/hmi-tool
# unapproved malware is blocked
sudo ip netns exec ews /usr/local/bin/stellar-run /usr/local/bin/evil-tool
```

**Expected result.**

```text
hmi-tool: reading PLC
StellarProtect: BLOCKED (not allowlisted)
```

The approved tool runs; the malware is denied execution — the EWS cannot be used to push a malicious change even if an attacker drops a binary on it.

**Negative test.** Modify `hmi-tool` (changing its hash) and watch even it get blocked — proof the control is the exact approved binary, not its name or location. Re-approve it by re-recording its hash if you change it.

**Rollback.** Keep the lockdown for verification.

## Summary and Completion Checklist

- [ ] An application allowlist (by hash) defined for the EWS.
- [ ] The approved tool runs; unapproved malware is blocked.
- [ ] Hash-based (not name-based) lockdown understood.
- [ ] Endpoint lockdown seen as the complement to the inline network shield.
