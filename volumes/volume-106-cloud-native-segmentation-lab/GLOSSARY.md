# Volume CVI Glossary

Definitions for terms introduced in **Volume CVI — Cloud-Native Segmentation Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Application Security Group (ASG)** — an Azure object that groups NICs so an NSG rule can name the group as source or destination instead of an IP; the Azure equivalent of referencing an AWS security group.
- **Budget alert** — a spend threshold (set here to $5 with an 80% notification) created on each cloud before any billable resource, so the lab cannot run up a silent bill.
- **Firewall Rules Logging** — GCP's per-rule logging that records each connection a firewall rule allowed or denied, with the source, destination, port, and the rule reference.
- **Flat network** — the permissive default state in which every workload can reach every other; the starting condition the lab breaks then contains (AWS wide-open SG, Azure `AllowVnetInBound`, GCP broad `allow-internal`).
- **Hierarchical firewall policy** — a GCP organization- or folder-level policy evaluated before VPC rules, letting a central team enforce a floor no project can override.
- **Managed prefix list** — an AWS named, versioned set of CIDRs referenced by many security groups, so an address change is made once rather than per rule.
- **Network ACL (NACL)** — AWS's subnet-level, **stateless** filter that supports numbered allow *and* deny rules; because it is stateless it requires an explicit egress rule for return traffic.
- **Network Security Group (NSG)** — Azure's stateful, priority-ordered filter attached to a subnet or NIC, supporting explicit allow and deny rules where the first match by ascending priority wins.
- **Network tag** — a GCP label attached to an instance that firewall rules can target as source or destination; convenient but forgeable by anyone who can edit the instance.
- **Priority ordering** — the Azure/GCP model in which rules are evaluated by ascending priority number and the first match wins, so a specific deny must sit above a broad allow.
- **Security group (SG)** — AWS's stateful, allow-only filter on an ENI/instance; its defining strength is that a rule can name **another security group** as the source, expressing identity rather than IP.
- **Service account (as firewall target)** — a GCP IAM identity bound to an instance; using it as a firewall rule's source/target is stronger than a network tag because membership is IAM-controlled and hard to forge.
- **Single-track** — this volume has no "Track 2" because the clouds are real; every command runs against a live account (which is why cost discipline is part of the lab).
- **Stateful vs stateless** — a stateful filter (SG, NSG, GCP rule) automatically permits return traffic; a stateless filter (NACL) does not, and forgetting the return rule is the most common cloud-firewall mistake.
- **VPC Flow Logs** — AWS's per-ENI/subnet/VPC logging of accepted and/or rejected IP flows, delivered to CloudWatch or S3, used here to see the `hmi → db` REJECT.
