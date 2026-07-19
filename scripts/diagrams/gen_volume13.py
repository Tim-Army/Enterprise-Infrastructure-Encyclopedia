import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-13-integrated-enterprise-labs"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Hands-On Lab: The Reference Lab Scaffold — Evidence Pipeline and a Verified Rollback",
        subtitle="Every command is checksummed into a tamper-evident manifest; snapshot rollback is proven before any later chapter depends on it",
        svg_title="Chapter 1 lab flow: ctrl01's evidence-capture pipeline and a hypervisor snapshot/rollback cycle, verified before the volume's later chapters rely on it",
        svg_desc="ctrl01 (10.13.10.30/24, VLAN 110) runs evidence.sh, which wraps every lab command, captures its "
                  "output to a timestamped log, and appends a SHA-256 checksum to a manifest. Isolation is "
                  "confirmed: a traceroute toward 1.1.1.1 never shows a 10.13.x.x address once it leaves ctrl01, "
                  "and a ping to the illustrative 203.0.113.1 fails to route anywhere outside the lab. A "
                  "hypervisor snapshot named ch01-baseline is taken, a marker file is created, and reverting to "
                  "the snapshot removes the marker — proving rollback actually works before any later chapter's "
                  "negative test depends on it. As a negative test, a static route misdirecting the "
                  "203.0.113.0/24 range at the real gateway still fails to reach anything, since that range is "
                  "not announced on the real internet either — confirming the isolation holds even under a "
                  "misconfiguration attempt.")
    c.node_box(60, 140, 260, 130, "mgmt", [
        Line("ctrl01 — 10.13.10.30/24 (VLAN 110)", 12, 700, "#111827"),
        Line("evidence.sh wraps every command", 10.5, 400, "#374151"),
        Line("→ timestamped log + sha256 manifest", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 260, 130, "alt", [
        Line("Snapshot / rollback proof", 12.5, 700, "#111827"),
        Line("ch01-baseline snapshot taken", 10.5, 400, "#374151"),
        Line("marker created → reverted → ABSENT", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 205, 400, 205, "mgmt")
    c.node_box(700, 140, 220, 130, "neutral", [
        Line("Isolation check", 12.5, 700, "#111827"),
        Line("traceroute → 1.1.1.1: no 10.13.x.x", 10.5, 400, "#374151"),
        Line("ping 203.0.113.1: unreachable", 10.5, 400, "#374151"),
    ])
    c.connector(660, 205, 700, 205, "neutral")
    c.node_box(60, 340, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("static route added on ctrl01 pointing 203.0.113.0/24 at the real gateway instead of the lab router", 11, 400, "#7f1d1d"),
        Line("ping to 203.0.113.1 still fails — that range isn't announced on the real internet either", 11, 400, "#7f1d1d"),
        Line("confirms the exercise of detecting and removing an incorrect route, not a real isolation breach", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Evidence pipeline"), ("alt", "Verified rollback"), ("neutral", "Isolation boundary")])
    c.save(f"{OUT}/chapter-01-lab-scaffold-evidence-rollback-flow.svg")


def ch02():
    c = Canvas(960, 620,
        title="Chapter 2 Hands-On Lab: An Active Directory Forest That Survives a Domain Controller Failure",
        subtitle="Kerberos and DHCP both keep working on dc02 alone when dc01 is powered off, then re-converge on recovery",
        svg_title="Chapter 2 lab topology: a two-node corp.meridian.example forest with DHCP failover and a domain-joined Linux client, tested against a DC outage",
        svg_desc="dc01 (10.13.10.11, forest root) and dc02 (10.13.10.12, additional DC and global catalog) "
                  "replicate with zero failures, share a converged time hierarchy, and load-balance a VLAN 120 "
                  "DHCP scope in Normal state. linux01 (10.13.20.21) joins the domain via realm, and kinit/klist "
                  "confirm DNS SRV lookup, Kerberos, and LDAP all work from a non-Windows client. As a negative "
                  "test, dc01 is powered off to simulate an unplanned failure; linux01 destroys and re-requests "
                  "its Kerberos ticket and still succeeds, because dc02 answers the KDC request, and DHCP failover "
                  "reports a degraded partner but continues leasing from dc02 alone. Powering dc01 back on brings "
                  "both replication and DHCP failover back to a fully healthy state.")
    c.node_box(60, 140, 240, 120, "mgmt", [
        Line("dc01 — 10.13.10.11", 13, 700, "#111827"),
        Line("forest root, VLAN 110", 10.5, 400, "#374151"),
        Line("negative test: powered off", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(360, 140, 240, 120, "alt", [
        Line("dc02 — 10.13.10.12", 13, 700, "#111827"),
        Line("additional DC + GC, VLAN 110", 10.5, 400, "#374151"),
        Line("answers KDC + DHCP alone", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 200, 360, 200, "mgmt", label="AD replication, 0 failures")
    c.node_box(680, 140, 240, 120, "mgmt", [
        Line("linux01 — 10.13.20.21", 13, 700, "#111827"),
        Line("VLAN 120, realm-joined", 10.5, 400, "#374151"),
        Line("kinit succeeds via dc02", 10.5, 700, "#14532d"),
    ])
    c.connector(480, 200, 680, 200, "alt", label="Kerberos/LDAP/DNS SRV")
    c.node_box(60, 320, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("dc01 powered off — linux01 kdestroy + kinit still succeeds (dc02 answers the KDC request)", 11, 400, "#7f1d1d"),
        Line("DHCP failover reports a degraded partner but continues leasing from dc02 alone", 11, 400, "#7f1d1d"),
        Line("recovery: dc01 rejoins, repadmin and DHCP failover both report Normal and 0 failures again", 11, 400, "#14532d"),
    ])
    c.legend(60, 490, [("mgmt", "Forest root / client"), ("alt", "Surviving DC (carries load alone)")])
    c.save(f"{OUT}/chapter-02-ad-forest-dc-failure-topology.svg")


def ch03():
    c = Canvas(960, 660,
        title="Chapter 3 Hands-On Lab: HSRP Core Failover Transparent to Every Endpoint on the Gateway",
        subtitle="Failing the active core switch moves gateway duty to the standby within the timer window — linux01 never reconfigures anything",
        svg_title="Chapter 3 lab topology: a Catalyst core/WAN/wireless build with HSRP, OSPF/IPsec to BR1, and an RODC, tested against a core switch failure",
        svg_desc="sw-core01 (HSRP priority 110, active) and sw-core02 (priority 90, standby) share every HQ VLAN's "
                  "gateway; rtr-hq01 and rtr-br101 form an OSPF-FULL, IPsec-protected WAN link to a read-only "
                  "domain controller (dc-br101) at BR1, which replicates cleanly from dc01. wlc01 serves two "
                  "SSIDs mapped to their own VLANs and DHCP scopes. As a negative test, VLAN 110's SVI on "
                  "sw-core01 is shut down; sw-core02 transitions to Active for every group within the standby "
                  "timer window, and linux01 keeps routing through the same 10.13.10.1 gateway address with no "
                  "local reconfiguration — the outage is visible only as a brief pause, not a routing change on "
                  "the endpoint. Re-enabling sw-core01's SVI and its preempt setting returns it to Active.")
    c.node_box(60, 130, 220, 110, "mgmt", [
        Line("sw-core01", 13, 700, "#111827"),
        Line("HSRP priority 110", 10.5, 700, "#1d4ed8"),
        Line("negative test: VLAN 110 shut", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(320, 130, 220, 110, "alt", [
        Line("sw-core02", 13, 700, "#111827"),
        Line("HSRP priority 90", 10.5, 400, "#374151"),
        Line("→ becomes Active on failure", 10.5, 700, "#14532d"),
    ])
    c.connector(280, 185, 320, 185, "mgmt", label="HSRP peer")
    c.node_box(600, 130, 200, 110, "mgmt", [
        Line("rtr-hq01 ⇄ rtr-br101", 12.5, 700, "#111827"),
        Line("OSPF FULL, IPsec SA up", 10.5, 400, "#374151"),
    ])
    c.node_box(820, 130, 120, 110, "mgmt", [
        Line("dc-br101", 11.5, 700, "#111827"),
        Line("RODC, replicates", 9.5, 400, "#374151"),
    ])
    c.connector(800, 185, 820, 185, "mgmt")
    c.node_box(60, 300, 220, 100, "alt", [
        Line("linux01", 12.5, 700, "#111827"),
        Line("gateway 10.13.10.1 unchanged", 10.5, 700, "#14532d"),
        Line("through the failover", 10.5, 400, "#374151"),
    ])
    c.connector(170, 240, 170, 300, "warn", label="brief pause only")
    c.node_box(320, 300, 220, 100, "neutral", [
        Line("wlc01", 12.5, 700, "#111827"),
        Line("MERIDIAN-CORP → VLAN 120", 10, 400, "#374151"),
        Line("MERIDIAN-GUEST → VLAN 140", 10, 400, "#374151"),
    ])
    c.node_box(60, 450, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("sw-core01: VLAN 110 SVI shut down — sw-core02 transitions to Active within the standby timer window", 11, 400, "#7f1d1d"),
        Line("linux01 continues routing through the same 10.13.10.1 gateway with no local reconfiguration", 11, 400, "#7f1d1d"),
        Line("recovery: SVI re-enabled, standby preempt returns sw-core01 to Active (higher priority)", 11, 400, "#14532d"),
    ])
    c.legend(60, 610, [("mgmt", "Active gateway"), ("alt", "Standby, then failover")])
    c.save(f"{OUT}/chapter-03-hsrp-core-failover-topology.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: vSAN HA Restarts a Failed Host's VMs, and a Backup Actually Restores",
        subtitle="dc01 relocates to esxi-a02 automatically after a simulated host failure; a corrupted file is recovered from a verified export",
        svg_title="Chapter 4 lab topology: an HQ vSphere/vSAN cluster with HA and a backup/replication pipeline, tested against a host failure and a restore",
        svg_desc="esxi-a01 and esxi-a02, backed by vsan-witness01, form HQ-Cluster with vSAN, HA "
                  "(HAFailoverLevel 1), and DRS fully automated; dc01, dc02, ctrl01, and linux01 migrate in "
                  "without losing domain authentication. bkp01 exports a verified backup of dc02, and "
                  "esxi-br101 receives a vSphere Replication copy within its configured RPO window. As a "
                  "negative test, esxi-a01 is forced offline while running dc01; vSphere HA detects the "
                  "unreachable host and restarts dc01 on esxi-a02 within a few minutes, and once esxi-a01 "
                  "rejoins, vSAN resynchronizes to a green health state. A restore test deliberately corrupts a "
                  "file on dc02, then imports the bkp01 export to a temporary VM and confirms the file matches "
                  "its pre-corruption state before that temporary VM is deleted.")
    c.node_box(60, 130, 220, 110, "warn", [
        Line("esxi-a01 (negative test)", 12, 700, "#111827"),
        Line("forced offline while", 10.5, 700, "#7f1d1d"),
        Line("running dc01", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(320, 130, 220, 110, "alt", [
        Line("esxi-a02", 13, 700, "#111827"),
        Line("HA restarts dc01 here", 10.5, 700, "#14532d"),
        Line("within a few minutes", 10.5, 400, "#374151"),
    ])
    c.connector(280, 185, 320, 185, "warn", label="HA restart")
    c.node_box(600, 130, 220, 110, "mgmt", [
        Line("HQ-Cluster (vSAN + HA + DRS)", 11.5, 700, "#111827"),
        Line("vsan-witness01 quorum", 10.5, 400, "#374151"),
        Line("resyncs green on rejoin", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 300, 260, 120, "neutral", [
        Line("bkp01", 12.5, 700, "#111827"),
        Line("vm-backup.sh dc02 → verified", 10.5, 400, "#374151"),
        Line(".ovf export + manifest", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 300, 260, 120, "alt", [
        Line("Restore test", 12.5, 700, "#111827"),
        Line("dc02 file corrupted →", 10.5, 400, "#374151"),
        Line("imported to temp VM, file intact", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 360, 360, 360, "neutral")
    c.node_box(660, 300, 220, 120, "mgmt", [
        Line("esxi-br101", 12.5, 700, "#111827"),
        Line("vSphere Replication target", 10.5, 400, "#374151"),
        Line("sync within RPO window", 10.5, 400, "#374151"),
    ])
    c.legend(60, 470, [("mgmt", "Cluster / replication"), ("alt", "Recovery outcome"), ("warn", "Simulated host failure")])
    c.save(f"{OUT}/chapter-04-vsan-ha-backup-restore-topology.svg")


def ch05():
    c = Canvas(960, 660,
        title="Chapter 5 Hands-On Lab: A Hybrid Kubernetes Cluster That Degrades Safely When the VPN Fails",
        subtitle="Losing the CLOUD1 tunnel drops one worker to NotReady; the control plane and workload availability both survive because neither depended on the VPN",
        svg_title="Chapter 5 lab topology: a hybrid Kubernetes cluster spanning HQ and a CLOUD1 landing zone over VPN, tested against a hybrid-link failure",
        svg_desc="rtr-hq01 extends its crypto map to cloud-vpgw01, establishing an IPsec SA into the CLOUD1 "
                  "VPC (10.13.90.0/24). k8s-cp01 and k8s-wk01 run as HQ-Cluster VMs; k8s-wk02 runs as a CLOUD1 "
                  "compute instance; all three join one cluster, zone-labeled, and meridian-web deploys with a "
                  "topology spread constraint placing replicas on both zones. As a negative test, the cloud VPN "
                  "crypto map entry is removed to simulate a hybrid link outage; k8s-wk02 transitions to "
                  "NotReady within the node-heartbeat timeout, but k8s-cp01 and k8s-wk01 remain Ready and the "
                  "control plane keeps responding throughout, since it never depended on the VPN. Pods that were "
                  "on k8s-wk02 reschedule onto k8s-wk01 once their grace period expires, and meridian-web "
                  "continues answering requests — degraded scheduling flexibility, not an outage. Restoring the "
                  "crypto map returns k8s-wk02 to Ready.")
    c.node_box(60, 140, 240, 120, "mgmt", [
        Line("HQ-Cluster", 13, 700, "#111827"),
        Line("k8s-cp01 (control plane)", 10.5, 700, "#1d4ed8"),
        Line("k8s-wk01 — stays Ready", 10.5, 700, "#14532d"),
    ])
    c.node_box(400, 130, 220, 100, "neutral", [
        Line("rtr-hq01 ⇄ cloud-vpgw01", 11.5, 700, "#111827"),
        Line("IPsec SA (negative test: torn down)", 10, 700, "#7f1d1d"),
    ])
    c.node_box(700, 140, 220, 120, "warn", [
        Line("k8s-wk02 (CLOUD1)", 13, 700, "#111827"),
        Line("VPC 10.13.90.0/24", 10.5, 400, "#374151"),
        Line("→ NotReady on VPN loss", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 195, 400, 180, "mgmt")
    c.connector(620, 180, 700, 195, "warn")
    c.node_box(60, 320, 860, 150, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("crypto map entry removed on rtr-hq01 — VPN tunnel down, simulating a hybrid link outage", 11, 400, "#7f1d1d"),
        Line("k8s-wk02 → NotReady within the heartbeat timeout; k8s-cp01/k8s-wk01 stay Ready, control plane keeps responding", 11, 400, "#7f1d1d"),
        Line("meridian-web pods on k8s-wk02 reschedule onto k8s-wk01 and keep answering — degraded flexibility, not an outage", 11, 400, "#7f1d1d"),
        Line("recovery: crypto map restored, tunnel re-establishes, k8s-wk02 returns to Ready", 11, 400, "#14532d"),
    ])
    c.legend(60, 500, [("mgmt", "Unaffected by VPN loss"), ("warn", "Cloud-side, affected by VPN loss")])
    c.save(f"{OUT}/chapter-05-hybrid-k8s-vpn-failure-topology.svg")


def ch06():
    c = Canvas(960, 620,
        title="Chapter 6 Hands-On Lab: A Policy Gate That Blocks an Open-SSH Security Group Before It Ever Applies",
        subtitle="A compliant pull request flows through plan, gate, and apply; a 0.0.0.0/0 SSH rule is denied and the apply stage never runs",
        svg_title="Chapter 6 lab flow: Terraform/Ansible/Vault brought under CI with a Conftest policy gate, tested against a policy-violating pull request",
        svg_desc="git01 and vault01 centralize the DHCP failover secret and both IPsec pre-shared keys; "
                  "Terraform imports the existing CLOUD1 VPC and HQ vSphere cluster with a clean plan "
                  "(0 changes), and the Chapter 2 DHCP configuration converts to an idempotent Ansible playbook "
                  "(second run: 0 changed tasks). A compliant pull request adding a resource tag runs plan, "
                  "passes the Conftest policy gate, and applies only after merge and approval. As a negative "
                  "test, a second pull request introduces a security group rule permitting SSH from 0.0.0.0/0; "
                  "the Conftest policy gate reports the specific deny message and the pipeline blocks the apply "
                  "stage from running, confirmed in the pipeline UI itself, not just local output. Reverting the "
                  "change and re-running the gate confirms a clean pass before the pull request closes.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("vault01", 12.5, 700, "#111827"),
        Line("DHCP failover secret", 10.5, 400, "#374151"),
        Line("IPsec PSKs (BR1, CLOUD1)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("Compliant PR", 12.5, 700, "#111827"),
        Line("plan → Conftest PASS", 10.5, 700, "#14532d"),
        Line("apply after merge + approval", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test PR", 12, 700, "#7f1d1d"),
        Line("SSH from 0.0.0.0/0 rule", 10.5, 700, "#7f1d1d"),
        Line("Conftest: deny, apply blocked", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the block is confirmed in the pipeline UI/logs, not just local Conftest output; reverting the change and", 11.5, 400, "#374151"),
        Line("re-running plan + the policy gate confirms a clean pass before the pull request is closed.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Centralized secrets"), ("alt", "Passing pipeline"), ("warn", "Gate-blocked change")])
    c.save(f"{OUT}/chapter-06-iac-policy-gate-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: A Full Detect-Contain-Eradicate-Recover Cycle Against a Kerberos Brute Force",
        subtitle="atk01's pre-auth brute force is detected by siem01, contained by shutting its switch port, then the attacker is removed entirely",
        svg_title="Chapter 7 lab topology: 802.1X and default-deny microsegmentation paired with SIEM detection, exercised through a full incident response cycle",
        svg_desc="dc01's NPS/RADIUS role and 802.1X on sw-acc01 authenticate linux01's port; a default-deny ACL "
                  "between VLAN 120 and VLAN 110 blocks an RDP probe while Kerberos authentication still "
                  "succeeds. siem01 ingests logs from every system built so far and runs a "
                  "kerberos-preauth-bruteforce detection rule tuned above the measured baseline failure rate. "
                  "As a negative test, atk01 is attached to VLAN 120 and runs 15 rapid Kerberos "
                  "pre-authentication attempts against dc01; siem01 raises an alert naming atk01's address "
                  "within the rule's evaluation window. Containment shuts atk01's switch port, immediately "
                  "cutting all connectivity; eradication confirms no lateral movement occurred (clean "
                  "replication summary, no new domain accounts) before atk01 is removed from the network "
                  "entirely rather than left merely port-shut.")
    c.node_box(60, 130, 220, 100, "mgmt", [
        Line("dc01 (NPS/RADIUS)", 12.5, 700, "#111827"),
        Line("+ sw-acc01: 802.1X", 10.5, 400, "#374151"),
    ])
    c.node_box(320, 130, 220, 100, "neutral", [
        Line("VLAN 120 ⇄ VLAN 110", 12, 700, "#111827"),
        Line("default-deny ACL: RDP blocked,", 10, 400, "#374151"),
        Line("Kerberos still succeeds", 10, 400, "#374151"),
    ])
    c.node_box(600, 130, 220, 100, "alt", [
        Line("siem01", 13, 700, "#111827"),
        Line("kerberos-preauth-bruteforce", 10.5, 700, "#1d4ed8"),
        Line("rule, tuned above baseline", 10.5, 400, "#374151"),
    ])
    c.connector(280, 180, 320, 180, "mgmt")
    c.connector(540, 180, 600, 180, "neutral")
    c.node_box(60, 280, 220, 110, "warn", [
        Line("atk01 (VLAN 120)", 12.5, 700, "#111827"),
        Line("15x Kerberos pre-auth", 10.5, 700, "#7f1d1d"),
        Line("brute-force attempts", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(600, 230, 170, 280, "warn", label="detected")
    c.node_box(360, 280, 260, 110, "warn", [
        Line("Contain", 12, 700, "#111827"),
        Line("sw-acc01 port shutdown", 10.5, 700, "#7f1d1d"),
        Line("atk01 loses all connectivity", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(280, 335, 360, 335, "warn")
    c.node_box(680, 280, 220, 110, "alt", [
        Line("Eradicate + recover", 12, 700, "#111827"),
        Line("no lateral movement confirmed", 10.5, 700, "#14532d"),
        Line("atk01 removed from network", 10.5, 400, "#374151"),
    ])
    c.connector(620, 335, 680, 335, "alt")
    c.legend(60, 460, [("mgmt", "Authentication path"), ("neutral", "Segmentation boundary"), ("alt", "Detection / recovery"), ("warn", "Attack + containment")])
    c.save(f"{OUT}/chapter-07-zero-trust-incident-response-topology.svg")


def ch08():
    c = Canvas(960, 660,
        title="Chapter 8 Hands-On Lab: A Full Major-Incident Cycle From Injected Failure to Verified Recovery",
        subtitle="Resource exhaustion trips the SLO burn-rate alert and pages on-call; draining the affected node restores the SLI within minutes",
        svg_title="Chapter 8 lab flow: complete environment instrumentation, an SLO burn-rate alert, and a full major-incident cycle against an injected resource-exhaustion failure",
        svg_desc="obs01 scrapes every host, network device, and Kubernetes component with 100% target health; "
                  "meridian-web exposes a /metrics endpoint feeding the meridian-web-availability SLO and its "
                  "multi-window burn-rate alert rules, and a synthetic test alert confirms the paging webhook "
                  "reaches the simulated pager before the real test runs. As a negative test, a resource-"
                  "exhaustion workload is injected on k8s-wk01; meridian-web's SLI drops below its SLO and "
                  "MeridianWebFastBurn fires within the fast-burn window, logging a page. A major incident is "
                  "declared and an incident commander assigned; cordoning and draining k8s-wk01 lets the "
                  "scheduler move meridian-web elsewhere, and the SLI recovers to at least 99.5% within a few "
                  "minutes, clearing the burn-rate alert. The postmortem is reconstructed entirely from "
                  "dashboards, the paging log, and evidence.sh output — not from memory.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("obs01", 12.5, 700, "#111827"),
        Line("100% target health", 10.5, 400, "#374151"),
        Line("meridian-web SLO + burn-rate", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "warn", [
        Line("Negative Test: k8s-wk01", 12, 700, "#111827"),
        Line("stress-ng resource exhaustion", 10.5, 700, "#7f1d1d"),
        Line("SLI drops, MeridianWebFastBurn fires", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 195, 380, 195, "warn")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Page logged", 12.5, 700, "#111827"),
        Line("major incident declared", 10.5, 700, "#7f1d1d"),
        Line("incident commander assigned", 10.5, 400, "#374151"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 130, "alt", [
        Line("Resolve + Recover", 12.5, 700, "#111827"),
        Line("k8s-wk01 cordoned and drained — scheduler moves meridian-web pods to healthy nodes", 11, 400, "#374151"),
        Line("SLI recovers to ≥ 99.5% within a few minutes, burn-rate alert clears", 11, 700, "#14532d"),
        Line("postmortem reconstructed entirely from dashboards, paging log, and evidence.sh — not memory", 11, 400, "#374151"),
    ])
    c.legend(60, 500, [("mgmt", "Healthy baseline"), ("warn", "Injected failure + paging"), ("alt", "Verified recovery")])
    c.save(f"{OUT}/chapter-08-slo-major-incident-flow.svg")


def ch09():
    c = Canvas(960, 680,
        title="Chapter 9 Hands-On Lab: HQ Site Failure, BR1 Disaster Recovery, Failback, and Full Decommission",
        subtitle="FSMO roles seize onto the BR1-replicated dc02 copy while HQ is down, then dc01's stale claims are cleaned up on failback",
        svg_title="Chapter 9 lab flow: the volume's capstone chaos exercise — HQ outage, DR failover to BR1, measured RTO/RPO, failback, and reverse-dependency decommission",
        svg_desc="simulate-hq-outage.sh takes HQ down; from BR1, the WAN peer is unreachable and OSPF drops, and "
                  "a directory write against the RODC alone fails as the confirmed limitation. The replicated "
                  "dc02 image at esxi-br101 is recovered and seizes all five FSMO roles; BR1's DHCP relay and "
                  "replication partner repoint to it, and identity writes succeed again. A minimal Kubernetes "
                  "control plane is rebuilt at BR1, with elapsed time from outage to working control plane "
                  "recorded as the measured RTO against the BIA targets. On failback, dc01 is checked for a USN "
                  "rollback condition before rejoining replication, and a metadata cleanup removes its stale "
                  "FSMO claims so exactly one authoritative answer remains. The volume then tears down every "
                  "system built, in strict reverse-dependency order — Kubernetes and CLOUD1 first, vSphere and "
                  "network next, security/observability and automation after that, and identity demoted last — "
                  "with disk sanitization and a final verified evidence manifest.")
    c.node_box(60, 130, 220, 110, "warn", [
        Line("HQ outage simulated", 12, 700, "#111827"),
        Line("WAN peer unreachable,", 10.5, 700, "#7f1d1d"),
        Line("OSPF neighbor down", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(320, 130, 240, 110, "alt", [
        Line("DR failover to BR1", 12.5, 700, "#111827"),
        Line("dc02 replica recovered,", 10.5, 400, "#374151"),
        Line("seizes all 5 FSMO roles", 10.5, 700, "#14532d"),
    ])
    c.connector(280, 185, 320, 185, "warn")
    c.node_box(600, 130, 240, 110, "alt", [
        Line("Emergency K8s at BR1", 12.5, 700, "#111827"),
        Line("control plane rebuilt", 10.5, 400, "#374151"),
        Line("elapsed time = measured RTO", 10.5, 700, "#14532d"),
    ])
    c.connector(560, 185, 600, 185, "alt")
    c.node_box(60, 290, 400, 110, "mgmt", [
        Line("Failback", 12.5, 700, "#111827"),
        Line("dc01 checked for USN rollback before rejoining", 10.5, 400, "#374151"),
        Line("metadata cleanup removes dc01's stale FSMO claims", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(500, 290, 400, 110, "warn", [
        Line("Full decommission (reverse order)", 12, 700, "#111827"),
        Line("K8s/CLOUD1 → vSphere → network →", 10, 400, "#7f1d1d"),
        Line("security/observability → automation → identity last", 10, 700, "#7f1d1d"),
    ])
    c.connector(460, 345, 500, 345, "neutral")
    c.node_box(60, 460, 840, 100, "neutral", [
        Line("disk sanitization matched to medium (NIST SP 800-88) before datastores/volumes are released;", 11.5, 400, "#374151"),
        Line("final step verifies every checksum in the evidence manifest from Chapter 1 through this capstone.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 600, [("warn", "Failure / decommission"), ("alt", "Recovery outcome"), ("mgmt", "Cleanup / consistency")])
    c.save(f"{OUT}/chapter-09-capstone-dr-failback-decommission-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
