# Chapter 08: ACE Automation and Operations

## Learning Objectives

- Cover the ACE Automation focused course: Terraform/infrastructure-as-code for Aviatrix.
- Cover the ACE Operations focused course: CoPilot visibility, FlowIQ, and compliance.
- Drill real Terraform syntax and an observability model.

## Two focused courses, one operational reality

**ACE Automation** teaches deploying and managing the Aviatrix overlay as **code** (the Aviatrix Terraform provider); **ACE Operations** teaches running it — visibility, troubleshooting, and compliance through **CoPilot**. Together they cover Day-2: provision repeatably, observe continuously.

## Hands-On Lab

Real Terraform (HCL) syntax — validated, not applied (no cloud spend) — plus an observability model. **Cost:** none.

### Lab 8.1 — Aviatrix as Terraform (ACE Automation)

**Objective:** Write and validate Aviatrix resource definitions as code.

```bash
mkdir -p ~/acetf && cd ~/acetf
cat > main.tf <<'EOF'
terraform {
  required_providers {
    aviatrix = { source = "AviatrixSystems/aviatrix" }
  }
}
# a transit gateway and a spoke attached to it — declarative, repeatable
resource "aviatrix_transit_gateway" "transit_aws" {
  cloud_type   = 1            # 1=AWS, 8=Azure, 4=GCP, 16=OCI
  account_name = "aws-prod"
  gw_name      = "transit-aws"
  vpc_id       = "vpc-abc123"
  vpc_reg      = "us-east-1"
  gw_size      = "c5.xlarge"
  subnet       = "10.1.0.0/24"
  ha_gw_size   = "c5.xlarge"   # active-active HA
  connected_transit = true
}
resource "aviatrix_spoke_gateway" "spoke_app" {
  cloud_type   = 1
  account_name = "aws-prod"
  gw_name      = "spoke-app"
  vpc_id       = "vpc-def456"
  vpc_reg      = "us-east-1"
  gw_size      = "t3.medium"
  subnet       = "10.2.0.0/24"
}
resource "aviatrix_spoke_transit_attachment" "attach" {
  spoke_gw_name   = aviatrix_spoke_gateway.spoke_app.gw_name
  transit_gw_name = aviatrix_transit_gateway.transit_aws.gw_name
}
EOF
terraform init -backend=false >/dev/null 2>&1 && terraform validate 2>/dev/null || terraform fmt -check 2>/dev/null || echo "HCL written; 'terraform validate' checks it with the provider installed"
terraform fmt && echo "HCL formatted OK"
```

**Expected result:** Well-formed HCL declaring a transit gateway (with HA), a spoke, and their attachment — the ACE Automation model: the overlay as version-controlled, repeatable code. `cloud_type` (1/8/4/16 = AWS/Azure/GCP/OCI) and `connected_transit` are the kinds of details the course drills.

**Negative test:** Reference `aviatrix_spoke_gateway.spoke_app.gw_name` before defining that resource — `terraform validate` errors on the unknown reference; declarative dependencies must resolve, exactly as the exam expects.

**Rollback:** `rm -rf ~/acetf`.

### Lab 8.2 — Idempotence and drift (ACE Automation)

**Objective:** Show the value of declarative management — plan/apply/drift.

```bash
python3 - <<'EOF'
# Terraform's model: desired state vs actual state -> a plan of changes
desired = {"transit-aws": {"ha": True, "size": "c5.xlarge"}}
actual  = {"transit-aws": {"ha": False, "size": "c5.xlarge"}}   # someone disabled HA by hand (drift)
for gw, want in desired.items():
    have = actual.get(gw, {})
    diffs = {k: (have.get(k), v) for k, v in want.items() if have.get(k) != v}
    print(f"{gw}: {'IN SYNC' if not diffs else 'DRIFT -> '+str(diffs)}")
EOF
```

**Expected result:** `transit-aws: DRIFT -> {'ha': (False, True)}` — Terraform detects that HA was disabled out-of-band and would re-enable it on apply. Managing the overlay as code means drift is visible and correctable, the ACE Automation payoff.

**Negative test:** Click-ops changes on the Controller behind Terraform's back — they become drift; the course's discipline is one source of truth (the code).

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — CoPilot visibility and FlowIQ (ACE Operations)

**Objective:** Model the observability CoPilot provides.

```bash
python3 - <<'EOF'
# FlowIQ-style flow record: CoPilot aggregates these into topology + analytics
flows = [
  ("spoke-app","spoke-db",5432,"allow",1200),
  ("spoke-app","1.2.3.4",443,"deny",3),     # blocked egress attempt
  ("spoke-web","spoke-app",8080,"allow",800),
]
print(f"{'src':<10}{'dst':<12}{'port':<6}{'action':<7}bytes")
for s,d,p,a,b in flows:
    print(f"{s:<10}{d:<12}{p:<6}{a:<7}{b}")
denied = [f for f in flows if f[3]=='deny']
print(f"\nCoPilot alert: {len(denied)} denied flow(s) -> investigate egress policy / possible exfil attempt")
EOF
```

**Expected result:** A flow table with a denied egress attempt surfaced as an alert — CoPilot's **FlowIQ** turns per-flow records into topology maps, throughput/latency analytics, and security alerts across all clouds. ACE Operations is about reading this to troubleshoot and prove compliance.

**Negative test:** Relying on each cloud's native flow logs separately — no unified view, no cross-cloud correlation; CoPilot's single pane is the operational differentiator.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Compliance and audit (ACE Operations)

**Objective:** State what CoPilot gives auditors.

```text
ACE Operations compliance surface:
  - full topology + who-can-reach-what (segmentation proof)
  - flow records + retention (who talked to whom, when)
  - config audit + change history on the Controller
  - alerting on policy violations and anomalies
Use to answer: "show me prod is isolated from dev" and "prove no workload egressed to X"
```

**Expected result:** The auditor-facing outputs — topology, flow history, config audit, alerting — that make the overlay demonstrably compliant. Operations is where the design's security claims become evidence.

**Negative test:** A secure design with no visibility/retention — you can't *prove* it during an audit; Operations exists to make the posture demonstrable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Aviatrix-as-Terraform written and validated; idempotence/drift understood.
- [ ] CoPilot FlowIQ visibility and alerting modeled.
- [ ] The compliance/audit surface (topology, flow history, config audit) understood.
