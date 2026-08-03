# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Troubleshoot the model's characteristic failure: the uncategorized VM.
- Back up and restore the policy — the discipline the DR constraint demands.
- Tear the lab down completely.

## Hands-On Lab

### Exercise 9.1 — Troubleshoot the uncategorized VM

**Objective.** Diagnose the most common Flow ticket: "the new VM can't reach anything."

**Track 1 — Walkthrough.** A VM with no categories matches no application policy's secured group and no permit names it — under applied policy it is default-denied. The Prism Central flow view shows its traffic landing in blocked flows with no policy hit. The fix is categorization, not a rule.

**Track 2 — Walkthrough.** Reproduce, diagnose by counters, fix by category:

```bash
sudo ip netns exec web2 bash -c 'true'   # web2 exists from Chapter 07
sudo nft delete element bridge flow apptier_web '{ 10.150.0.11 }'
sudo ip netns exec web2 bash -c 'nc -z -w2 10.150.0.20 5432 || echo "SYMPTOM: web2->db DENIED"'
sudo nft list chain bridge flow vswitch | tail -1
sudo nft add element bridge flow apptier_web '{ 10.150.0.11 }'
sudo ip netns exec web2 bash -c 'nc -z -w2 10.150.0.20 5432 && echo "FIXED by categorization"'
```

**Expected result.** The symptom reproduces, the final default-deny counter is the rule that ate the traffic (`counter packets N` on the last line), and assigning the category — not editing any rule — fixes it:

```text
SYMPTOM: web2->db DENIED
counter packets 2 bytes 120
FIXED by categorization
```

**Negative test.** The reverse mistake — categorizing a VM into the wrong tier — grants it that tier's permits. Category assignment *is* policy assignment; review it with the same rigor as a firewall change.

**Cleanup.** None.

### Exercise 9.2 — Back up and restore the policy

**Objective.** Drill the export/restore the DR constraint makes mandatory.

**Track 1 — Walkthrough.** Because categories and policies do not replicate between Prism Central instances, mature shops export policy as code (API/automation) and apply it to the DR Prism Central on a schedule — and drill the restore, not just the backup.

**Track 2 — Walkthrough.** Destroy the policy, prove the estate went flat, restore from the Chapter 08 export:

```bash
sudo nft delete table bridge flow
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 && echo "FLAT AGAIN (policy gone)"'
sudo nft -f /tmp/flow-policy-export.nft
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 || echo "RESTORED: lateral denied"'
```

**Expected result.**

```text
FLAT AGAIN (policy gone)
RESTORED: lateral denied
```

One file restored the entire posture — categories, all three policy layers, and the counters (reset to zero). That file is what the DR site needs and never receives automatically.

**Negative test.** Run the restore twice — `nft -f` of a full table fails on the second pass (`Table already exists`); idempotent restore tooling must delete-then-load, which is exactly what this drill did.

**Cleanup.** Policy is live again.

### Exercise 9.3 — Teardown

**Objective.** Remove everything the lab created.

**Track 2 — Walkthrough.**

```bash
sudo nft delete table bridge flow
for vm in web web2 db hmi plc; do sudo ip netns del $vm 2>/dev/null; done
sudo ip link del ahv0
rm -f /tmp/flow-policy-export.nft
```

**Expected result.** `ip netns list` shows none of the lab namespaces; `sudo nft list tables` no longer lists `bridge flow`; the `ahv0` bridge is gone.

**Negative test.** `sudo nft list table bridge flow` reports the table does not exist.

**Cleanup.** Complete — on Track 1, delete the security policies and categories in Prism Central and power off the lab VMs.

## Summary and Completion Checklist

- [ ] Uncategorized-VM failure diagnosed by counter and fixed by categorization.
- [ ] Policy backup/restore drilled — the answer to the no-replication constraint.
- [ ] Lab fully torn down.
