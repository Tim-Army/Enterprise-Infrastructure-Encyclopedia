# Chapter 05: Virtual Zones and the Segmentation Policy

## Learning Objectives

- Group assets into virtual zones.
- Derive a least-privilege, zone-to-zone segmentation policy from the curated baseline.
- Understand why zoning generalizes the policy so it survives new, similar assets.

## From flows to zones to policy

A per-asset baseline is precise but brittle: add a second web server and its flows are not in the baseline. Claroty groups assets into **virtual zones** and expresses the policy **zone-to-zone**, so the rule "IT-App may reach IT-Data on 5432" covers any web server in the zone. This chapter assigns the four assets to zones and turns the curated baseline into a zone policy.

## Hands-On Lab

### Exercise 5.1 — Assign assets to virtual zones

**Objective.** Map each asset to a zone.

**Track 1 — Walkthrough.** In xDome you define zones (by site, function, or Purdue level) and place assets in them, often with rules that auto-assign by attributes (vendor, protocol, subnet).

**Track 2 — Walkthrough.** Record the zone map:

```bash
sudo mkdir -p /etc/xdome
sudo tee /etc/xdome/zones > /dev/null <<'EOF'
10.70.1.10 IT-App
10.70.2.20 IT-Data
10.70.3.30 OT-Ops
10.70.4.40 OT-Control
EOF
cat /etc/xdome/zones
```

**Expected result.** Four assets mapped to four zones.

**Negative test.** An asset in no zone matches no zone-to-zone rule and, under default-deny, is isolated — every asset must be zoned for the policy to cover it.

**Rollback.** Keep the zone map.

### Exercise 5.2 — Derive the zone-to-zone policy

**Objective.** Turn the curated baseline into least-privilege zone rules.

**Track 1 — Walkthrough.** xDome recommends a policy: for each observed, sanctioned flow, an allow rule between the source and destination zones on that service; everything else is denied.

**Track 2 — Walkthrough.** Translate each curated flow into a zone-to-zone rule by looking up the zone of each endpoint:

```bash
zone_of() { awk -v ip="$1" '$1==ip{print $2}' /etc/xdome/zones; }
: > /etc/xdome/policy
while read src arrow dstport; do
  dst="${dstport%%:*}"; port="${dstport##*:}"
  echo "$(zone_of "$src") -> $(zone_of "$dst") : $port  ($src -> $dst)" | sudo tee -a /etc/xdome/policy >/dev/null
done < <(sed 's/ -> / /; s/:/ :/' /tmp/baseline.txt | awk '{print $1" -> "$2":"$4}')
cat /etc/xdome/policy
```

**Expected result.**

```text
IT-App -> IT-Data : 5432  (10.70.1.10 -> 10.70.2.20)
OT-Ops -> OT-Control : 502  (10.70.3.30 -> 10.70.4.40)
```

Two zone-to-zone allow rules, derived from the sanctioned baseline; everything else (including OT-Ops → IT-Data) is denied by default.

**Negative test.** Note the policy has no `OT-Ops -> IT-Data` rule — the curated baseline never sanctioned `hmi → db`, so the derived policy denies it automatically. The segmentation came from the observation, not from writing a deny by hand.

**Rollback.** Keep the policy; Chapter 06 pushes it to the enforcer.

## Summary and Completion Checklist

- [ ] Assets assigned to four virtual zones.
- [ ] A zone-to-zone least-privilege policy derived from the curated baseline.
- [ ] The lateral flow absent from the policy (denied by default).
- [ ] Policy ready to enforce via integration.
