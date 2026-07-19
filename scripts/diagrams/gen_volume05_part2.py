import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-05-vmware-virtualization"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Hands-On Lab: Folder-Scoped RBAC Verified Through a Second API Client",
        subtitle="LabRestrictedOperator is confined to the Restricted-Apps folder; govc confirms vCenter and PowerCLI agree",
        svg_title="Chapter 1 lab topology: an inventory hierarchy with a folder-scoped custom role, cross-verified with govc",
        svg_desc="LAB-DC/LAB-CLUSTER is built with PowerCLI, including a Restricted-Apps folder and a "
                  "DataClassification tag category, both confirmed visible through a second, independent API "
                  "client (govc). A custom role LabRestrictedOperator (power on/off only) is assigned to "
                  "lab-restricted-user at the Restricted-Apps folder with Propagate true; a test VM moved into that "
                  "folder inherits the permission. As a negative test, logging in as lab-restricted-user allows "
                  "power operations inside Restricted-Apps but is denied or cannot see objects outside it (for "
                  "example LAB-CLUSTER's settings), proving the folder-scoped permission — not a naming convention "
                  "— enforces the boundary.")
    c.node_box(370, 110, 220, 90, "mgmt", [
        Line("vCenter01 (LAB-DC)", 13, 700, "#111827"),
        Line("LAB-CLUSTER (HA+DRS)", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 250, 220, 110, "alt", [
        Line("Restricted-Apps folder", 12.5, 700, "#111827"),
        Line("LabRestrictedOperator role", 10.5, 700, "#14532d"),
        Line("lab-restricted-user, Propagate:True", 10, 400, "#374151"),
        Line("test VM (inherits permission)", 10, 400, "#374151"),
    ])
    c.node_box(700, 110, 220, 90, "neutral", [
        Line("govc (2nd API client)", 12.5, 700, "#111827"),
        Line("tags.category.ls / tags.ls", 10.5, 400, "#374151"),
    ])
    c.connector(480, 200, 480, 250, "mgmt")
    c.connector(590, 155, 700, 155, "neutral", label="cross-verify")
    c.node_box(60, 430, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("logged in as lab-restricted-user: power on/off inside Restricted-Apps succeeds", 11, 400, "#14532d"),
        Line("viewing/modifying LAB-CLUSTER or a VM in another folder is hidden or permission-denied", 11, 400, "#7f1d1d"),
    ])
    c.connector(480, 360, 480, 430, "warn")
    c.legend(60, 570, [("mgmt", "vCenter inventory"), ("alt", "Folder-scoped role"), ("neutral", "Independent verification")])
    c.save(f"{OUT}/chapter-01-folder-scoped-rbac-topology.svg")


def ch02():
    c = Canvas(960, 620,
        title="Chapter 2 Hands-On Lab: Scripted ESXi Install and Host Profile Drift Remediation",
        subtitle="A kickstart-built reference host's profile detects and remediates a second, non-standardized host",
        svg_title="Chapter 2 lab flow: a Host Profile extracted from a kickstart-installed reference host, applied to a drifted second host",
        svg_desc="esxi-lab-01 is installed unattended via a kickstart file setting IP, hostname, NTP, and syslog "
                  "forwarding, confirmed by esxcli system syslog config get. esxi-lab-02 is installed without NTP "
                  "or syslog configured, deliberately non-standardized. A Host Profile (lab-standard-profile) "
                  "extracted from esxi-lab-01 flags esxi-lab-02 as non-compliant on exactly the NTP/syslog "
                  "settings. As a negative test, remediation without a required host-specific answer-file value "
                  "fails or prompts rather than silently overwriting host identity; supplying the value and "
                  "remediating again brings esxi-lab-02 to full compliance.")
    c.node_box(60, 150, 240, 120, "mgmt", [
        Line("esxi-lab-01 (reference)", 12.5, 700, "#111827"),
        Line("kickstart: NTP + syslog set", 10.5, 400, "#374151"),
        Line("source of lab-standard-profile", 10, 400, "#374151"),
    ])
    c.node_box(380, 150, 240, 120, "alt", [
        Line("lab-standard-profile", 12.5, 700, "#111827"),
        Line("extracted Host Profile", 10.5, 400, "#374151"),
        Line("checked against esxi-lab-02", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 150, 220, 120, "warn", [
        Line("esxi-lab-02 (drifted)", 12.5, 700, "#111827"),
        Line("no NTP / no syslog set", 10.5, 700, "#7f1d1d"),
        Line("non-compliant vs. profile", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 210, 380, 210, "mgmt", label="extract profile")
    c.connector(620, 210, 700, 210, "mgmt", label="compliance check")
    c.node_box(60, 400, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("remediation attempted before supplying a required host-specific answer-file value → fails/prompts", 11, 400, "#7f1d1d"),
        Line("value supplied, remediation re-run → esxi-lab-02 compliant, syslog matches the reference host", 11, 400, "#14532d"),
    ])
    c.connector(810, 270, 480, 400, "warn")
    c.legend(60, 570, [("mgmt", "Reference / profile source"), ("alt", "Profile artifact"), ("warn", "Drifted target")])
    c.save(f"{OUT}/chapter-02-esxi-kickstart-host-profile-flow.svg")


def ch03():
    c = Canvas(960, 620,
        title="Chapter 3 Hands-On Lab: VCSA Deployment, AD Identity, and Backup/Restore of Simulated Loss",
        subtitle="A file-based backup rehydrates SSO, AD identity source, and RBAC after the appliance is deleted entirely",
        svg_title="Chapter 3 lab flow: deploying a VCSA, integrating Active Directory, then simulating and recovering from total appliance loss",
        svg_desc="vcsa-deploy installs a new VCSA from a JSON template; an LDAPS identity source (lab.example) is "
                  "added and a scoped RBAC role assigned to an AD test account. A file-based backup is taken to a "
                  "remote SFTP target. As a negative test, the VCSA VM is powered off and deleted entirely, "
                  "simulating total appliance loss — ESXi hosts keep running existing workloads, but centralized "
                  "management, DRS, and vCenter-mediated HA orchestration are unavailable. vcsa-deploy in restore "
                  "mode rehydrates a new appliance from the SFTP backup, restoring the SSO domain, AD identity "
                  "source, and RBAC assignment; hosts reconnect and the AD test account authenticates successfully.")
    c.node_box(60, 150, 240, 120, "mgmt", [
        Line("vcsa-deploy install", 12.5, 700, "#111827"),
        Line("VCSA + AD identity source", 10.5, 400, "#374151"),
        Line("(lab.example, LDAPS)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 150, 220, 120, "alt", [
        Line("Backup Now (VAMI)", 12.5, 700, "#111827"),
        Line("file-based backup", 10.5, 400, "#374151"),
        Line("→ SFTP target", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 210, 380, 210, "mgmt")
    c.node_box(680, 150, 240, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("VCSA VM powered off + deleted", 10.5, 700, "#7f1d1d"),
        Line("(simulated total appliance loss)", 10.5, 400, "#7f1d1d"),
        Line("hosts keep running VMs; no mgmt", 10, 400, "#7f1d1d"),
    ])
    c.connector(600, 210, 680, 210, "warn")
    c.node_box(60, 400, 840, 110, "alt", [
        Line("Restore", 12.5, 700, "#14532d"),
        Line("vcsa-deploy restore, pointed at the SFTP backup and timestamp from step 4", 11, 400, "#374151"),
        Line("new appliance rehydrates: SSO, AD identity source, RBAC role, and host reconnection all restored", 11, 400, "#14532d"),
    ])
    c.connector(800, 270, 480, 400, "warn")
    c.legend(60, 570, [("mgmt", "Deploy / configure"), ("alt", "Backup / restore"), ("warn", "Simulated loss")])
    c.save(f"{OUT}/chapter-03-vcsa-backup-restore-flow.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: Distributed Switch with LACP LAG and NIOC, Surviving an Uplink Failure",
        subtitle="Two-host VDS with a bundled LACP LAG; the test VM's traffic continues after one physical uplink fails",
        svg_title="Chapter 4 lab topology: a distributed switch with an LACP link aggregation group, tested against an uplink failure",
        svg_desc="dvs-lab spans esxi-lab-01 and esxi-lab-02, each contributing two uplinks bundled into an Active "
                  "LACP LAG (lag-lab). A VST-tagged port group (pg-lab-test, VLAN 150) hosts a test VM; NIOC shares "
                  "favor vMotion traffic during contention, and vmkping at 8972 bytes confirms end-to-end MTU 9000. "
                  "As a negative test, one physical uplink is disabled while the test VM has active traffic: the "
                  "LAG shows that uplink as no longer bundled while the surviving uplink keeps carrying traffic "
                  "with no sustained loss, and the failed uplink automatically rejoins the LAG once restored.")
    c.node_box(370, 110, 220, 90, "mgmt", [
        Line("dvs-lab (VDS, MTU 9000)", 13, 700, "#111827"),
        Line("lag-lab (LACP, Active)", 10.5, 400, "#374151"),
    ])
    c.node_box(80, 260, 260, 130, "alt", [
        Line("esxi-lab-01", 13, 700, "#111827"),
        Line("vmnic1 + vmnic2 → lag-lab", 10.5, 400, "#374151"),
        Line("pg-lab-test (VLAN 150)", 10.5, 400, "#374151"),
    ])
    c.node_box(620, 260, 260, 130, "warn", [
        Line("esxi-lab-02", 13, 700, "#111827"),
        Line("vmnic1 disabled (negative test)", 10.5, 700, "#7f1d1d"),
        Line("vmnic2: still bundled, carries load", 10.5, 700, "#14532d"),
    ])
    c.connector(430, 200, 210, 260, "mgmt", label="2x uplinks (LACP)")
    c.connector(530, 200, 750, 260, "mgmt", label="2x uplinks (1 failed)")
    c.node_box(60, 440, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("one physical uplink on esxi-lab-02 disabled while test VM traffic is active", 11, 400, "#7f1d1d"),
        Line("LAG shows the failed uplink no longer bundled; surviving uplink absorbs traffic, no sustained loss", 11, 400, "#7f1d1d"),
        Line("uplink restored → automatically rejoins the LAG (bundled) without manual intervention", 11, 400, "#14532d"),
    ])
    c.legend(80, 610, [("mgmt", "VDS uplink membership"), ("alt", "Healthy host"), ("warn", "Uplink-failure host")])
    c.save(f"{OUT}/chapter-04-vds-lacp-uplink-failure-topology.svg")


def ch05():
    c = Canvas(960, 660,
        title="Chapter 5 Hands-On Lab: Template Cloning, the Resource Pool Sibling Pitfall, and Snapshot Delta Growth",
        subtitle="Two pooled clones share one High-share allocation against a standalone sibling VM, and a snapshot's delta disk grows measurably",
        svg_title="Chapter 5 lab flow: cloning from a template, a deliberate resource pool sibling misconfiguration, and snapshot delta-disk growth",
        svg_desc="lab-src-01 is converted to a template and two customized clones (lab-clone-01, lab-clone-02) are "
                  "deployed with DHCP networking, confirmed by distinct guest hostnames. Both clones are moved into "
                  "lab-pool-high (CPU shares: High), while a third standalone VM remains at the cluster root as a "
                  "sibling of that pool. As a negative test, simultaneous CPU load on all three shows the "
                  "standalone VM receiving scheduling roughly proportional to one High-share entity competing "
                  "against the entire pool as a single entity — not two independently High-share VMs — visible as "
                  "disproportionate %RDY on the pooled VMs in esxtop. Separately, a snapshot of lab-clone-01 grows "
                  "its delta disk by roughly the size of new guest writes, confirmed via Get-Snapshot.")
    c.node_box(60, 130, 220, 90, "mgmt", [
        Line("lab-src-01 → template", 12.5, 700, "#111827"),
        Line("Set-VM -ToTemplate", 10.5, 400, "#374151"),
    ])
    c.connector(280, 175, 370, 175, "mgmt", label="2x clone + customize")
    c.node_box(370, 260, 250, 130, "warn", [
        Line("lab-pool-high (CPU: High)", 12.5, 700, "#111827"),
        Line("lab-clone-01", 10.5, 400, "#374151"),
        Line("lab-clone-02", 10.5, 400, "#374151"),
        Line("(share ONE pool-level allocation)", 10, 700, "#7f1d1d"),
    ])
    c.node_box(700, 260, 220, 130, "alt", [
        Line("Standalone VM", 12.5, 700, "#111827"),
        Line("cluster root (sibling of pool)", 10.5, 400, "#374151"),
        Line("competes against the pool", 10.5, 700, "#7f1d1d"),
        Line("as if it were ONE entity", 10, 400, "#374151"),
    ])
    c.connector(620, 325, 700, 325, "warn", label="CPU contention (negative test)")
    c.node_box(60, 450, 400, 110, "neutral", [
        Line("Negative test result", 11.5, 700, "#111827"),
        Line("esxtop %RDY climbs disproportionately on", 10.5, 400, "#374151"),
        Line("the two pooled VMs relative to their", 10.5, 400, "#374151"),
        Line("individual pool-inherited High share", 10.5, 400, "#374151"),
    ])
    c.node_box(500, 450, 420, 110, "neutral", [
        Line("Snapshot delta-disk growth", 11.5, 700, "#111827"),
        Line("pre-change-snapshot on lab-clone-01", 10.5, 400, "#374151"),
        Line("500 MB guest write → SizeGB grows ~500 MB", 10.5, 400, "#374151"),
        Line("(delta disk absorbs the change, not base)", 10, 400, "#374151"),
    ])
    c.legend(60, 610, [("mgmt", "Template/clone lifecycle"), ("warn", "Shared pool allocation"), ("alt", "Sibling competing VM")])
    c.save(f"{OUT}/chapter-05-template-clone-resource-pool-flow.svg")


def ch06():
    c = Canvas(960, 660,
        title="Chapter 6 Hands-On Lab: vSAN RAID-1 FTT=1 Policy Surviving a Simulated Host Loss",
        subtitle="A test VM stays online with reduced redundancy when one of three hosts enters maintenance mode with no data migration",
        svg_title="Chapter 6 lab topology: a 3-host vSAN cluster enforcing a RAID-1 FTT=1 storage policy through a simulated host loss",
        svg_desc="Three nested ESXi hosts each contribute a cache and capacity disk to a vSAN disk group, forming "
                  "the vsanDatastore. A RAID-1 FTT=1 storage policy is applied to vsan-lab-test-vm, reporting "
                  "ComplianceStatus compliant across all three fault domains. As a negative test, one host enters "
                  "maintenance mode with the 'No data migration' option while the test VM's replica components "
                  "reside partly on it, simulating unplanned host loss; the object becomes nonCompliant / "
                  "reduced-redundancy since only 2 of 3 fault domains remain reachable, but the VM stays running — "
                  "exactly what FTT=1 is designed to tolerate. Exiting maintenance mode triggers a resync back to "
                  "full compliance.")
    c.node_box(60, 150, 200, 110, "mgmt", [
        Line("Host 1", 13, 700, "#111827"),
        Line("disk group (cache+capacity)", 10, 400, "#374151"),
        Line("fault domain 1", 10, 400, "#374151"),
    ])
    c.node_box(380, 150, 200, 110, "mgmt", [
        Line("Host 2", 13, 700, "#111827"),
        Line("disk group (cache+capacity)", 10, 400, "#374151"),
        Line("fault domain 2", 10, 400, "#374151"),
    ])
    c.node_box(700, 150, 220, 110, "warn", [
        Line("Host 3 (negative test)", 12.5, 700, "#111827"),
        Line("maintenance mode, No data migration", 10, 700, "#7f1d1d"),
        Line("fault domain 3 — unreachable", 10, 700, "#7f1d1d"),
    ])
    c.node_box(340, 320, 280, 100, "alt", [
        Line("vsanDatastore", 13, 700, "#111827"),
        Line("vsan-lab-test-vm — RAID-1 FTT=1", 10.5, 400, "#374151"),
        Line("2 of 3 fault domains reachable →", 10.5, 700, "#7f1d1d"),
        Line("nonCompliant, VM stays running", 10.5, 700, "#7c2d12"),
    ])
    c.connector(160, 260, 420, 320, "mgmt")
    c.connector(480, 260, 480, 320, "mgmt")
    c.connector(800, 260, 550, 320, "warn")
    c.node_box(60, 470, 840, 100, "neutral", [
        Line("Exit maintenance mode → Resyncing Objects shows active resync traffic", 11.5, 400, "#374151"),
        Line("ComplianceStatus returns to compliant once resync completes", 11.5, 400, "#14532d"),
    ])
    c.legend(60, 610, [("mgmt", "Healthy fault domain"), ("alt", "vSAN object state"), ("warn", "Simulated host loss")])
    c.save(f"{OUT}/chapter-06-vsan-raid1-host-loss-topology.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: vMotion Baseline and an HA Isolation Event",
        subtitle="A live vMotion confirms mobility, then a management-network isolation triggers HA's power-off-and-restart response",
        svg_title="Chapter 7 lab topology: HA/DRS cluster behavior under a live vMotion and a simulated host isolation event",
        svg_desc="HA admission control is enabled on a 3-host cluster with an explicit isolation address "
                  "(10.10.10.1) and isolation response set to 'Power off and restart VMs'. lab-ha-test-vm is live "
                  "vMotioned to a second host with no sustained ping loss, confirming baseline mobility. As a "
                  "negative test, that host's management vmknic (vmk0) is disabled directly at the console while "
                  "the VM network path stays theoretically reachable, simulating isolation rather than failure: "
                  "the HA master detects loss of network heartbeats, confirms isolation via datastore "
                  "heartbeating, hard-powers-off lab-ha-test-vm on the isolated host, and restarts it on a "
                  "surviving host without any administrator-initiated migration. Restoring vmk0 reconnects the "
                  "host to the cluster within minutes.")
    c.node_box(80, 150, 220, 110, "mgmt", [
        Line("Host A", 13, 700, "#111827"),
        Line("lab-ha-test-vm (before)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 150, 220, 110, "alt", [
        Line("Host B", 13, 700, "#111827"),
        Line("lab-ha-test-vm (after vMotion)", 10.5, 700, "#14532d"),
        Line("then: vmk0 disabled (negative test)", 10, 700, "#7f1d1d"),
    ])
    c.node_box(680, 150, 220, 110, "mgmt", [
        Line("Host C", 13, 700, "#111827"),
        Line("HA restarts lab-ha-test-vm here", 10.5, 700, "#14532d"),
        Line("after isolation is confirmed", 10, 400, "#374151"),
    ])
    c.connector(300, 205, 380, 205, "mgmt", label="live vMotion (no sustained loss)")
    c.connector(600, 205, 680, 205, "warn", label="HA restart after isolation")
    c.node_box(80, 340, 820, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Host B's management vmknic (vmk0) disabled — VM network path remains theoretically reachable", 11, 400, "#7f1d1d"),
        Line("HA master detects lost heartbeats, confirms isolation via datastore heartbeating (not failure)", 11, 400, "#7f1d1d"),
        Line("lab-ha-test-vm hard-powered-off on Host B, restarted on Host C with no admin action", 11, 400, "#7f1d1d"),
    ])
    c.node_box(80, 500, 820, 60, "neutral", [
        Line("Restoring vmk0 reconnects Host B to the cluster as an agent host within a few minutes", 11.5, 400, "#374151"),
    ])
    c.legend(80, 610, [("mgmt", "Healthy host"), ("alt", "vMotion target / isolated host"), ("warn", "HA-driven restart")])
    c.save(f"{OUT}/chapter-07-vmotion-ha-isolation-topology.svg")


def ch08():
    c = Canvas(960, 660,
        title="Chapter 8 Hands-On Lab: Lockdown Mode, Least-Privilege RBAC, and NSX Micro-Segmentation",
        subtitle="A default-deny DFW policy allows only web-to-db on TCP 5432; every other flow between them is blocked",
        svg_title="Chapter 8 lab topology: ESXi Lockdown Mode, a folder-scoped custom role, and NSX dynamic-group micro-segmentation",
        svg_desc="esxi01 is placed in Normal Lockdown Mode, blocking direct SSH from non-exception accounts. A "
                  "custom role lab-role-power-only is assigned to CORP\\lab-test-user at a single folder "
                  "(lab-scoped-vms), confirmed to permit power operations but deny settings/snapshot/delete. "
                  "lab-web-01 and lab-db-01 are tagged web/db, forming dynamic NSX security groups lab-sg-web and "
                  "lab-sg-db; a default-deny DFW policy allows only web-to-db traffic on TCP 5432. The allowed flow "
                  "succeeds and increments the rule's hit counter. As a negative test, a connection from "
                  "lab-web-01 to lab-db-01 on TCP 22 (not covered by the allow rule) is blocked, and NSX's "
                  "Traffic Analysis view shows it matching the default-deny rule.")
    c.node_box(60, 130, 220, 90, "mgmt", [
        Line("esxi01 — Lockdown: Normal", 12.5, 700, "#111827"),
        Line("non-exception SSH refused", 10.5, 400, "#374151"),
    ])
    c.node_box(60, 260, 260, 100, "alt", [
        Line("lab-scoped-vms folder", 12.5, 700, "#111827"),
        Line("lab-role-power-only", 10.5, 700, "#14532d"),
        Line("(power on/off only, no edit)", 10, 400, "#374151"),
    ])
    c.node_box(400, 130, 220, 100, "mgmt", [
        Line("lab-web-01 (tag: web)", 12.5, 700, "#111827"),
        Line("lab-sg-web (dynamic group)", 10.5, 400, "#374151"),
    ])
    c.node_box(700, 130, 220, 100, "alt", [
        Line("lab-db-01 (tag: db)", 12.5, 700, "#111827"),
        Line("lab-sg-db (dynamic group)", 10.5, 400, "#374151"),
    ])
    c.connector(620, 180, 700, 180, "alt", label="TCP 5432 only — ALLOW")
    c.node_box(400, 300, 520, 100, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("lab-web-01 → lab-db-01 on TCP 22 (not covered by the allow rule)", 11, 400, "#7f1d1d"),
        Line("blocked; Traffic Analysis shows the flow matching the default-deny rule", 11, 400, "#7f1d1d"),
    ])
    c.connector(660, 230, 660, 300, "warn")
    c.legend(60, 570, [("mgmt", "Lockdown / dynamic group"), ("alt", "Scoped role / allowed flow"), ("warn", "Default-deny (negative test)")])
    c.save(f"{OUT}/chapter-08-lockdown-nsx-microsegmentation-topology.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: vLCM Drift Detection, Remediation, and esxtop Contention Observation",
        subtitle="An out-of-image VIB flips a host non-compliant; vLCM remediation removes it and restores the desired-state image",
        svg_title="Chapter 9 lab flow: vLCM image compliance drift detection and remediation, plus an esxtop CPU-contention observation",
        svg_desc="A vLCM-managed cluster's desired-state image reports all hosts Compliant at baseline. As a "
                  "negative test, an unmanaged VIB is manually installed on one host outside the desired-state "
                  "image; the next compliance check flags that host non-compliant, demonstrating vLCM's "
                  "whole-image drift detection. Update-VMHostImage remediates the cluster, removing the test VIB "
                  "and restoring Compliant status. Separately, a custom datastore-usage alarm is created, a "
                  "support bundle is generated with vm-support, and esxtop's CPU view shows %RDY rising measurably "
                  "under synthetic CPU contention and returning to baseline once the extra load stops.")
    c.node_box(60, 150, 240, 110, "mgmt", [
        Line("Baseline Image Check", 12.5, 700, "#111827"),
        Line("Get-VMHostImageCompliance", 10.5, 400, "#374151"),
        Line("all hosts: Compliant", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 150, 240, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("esxcli vib install (unmanaged)", 10.5, 700, "#7f1d1d"),
        Line("host now: non-compliant", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 205, 380, 205, "warn")
    c.node_box(700, 150, 220, 110, "alt", [
        Line("Remediation", 12.5, 700, "#111827"),
        Line("Update-VMHostImage", 10.5, 400, "#374151"),
        Line("VIB removed → Compliant", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 205, 700, 205, "alt")
    c.node_box(60, 340, 400, 110, "neutral", [
        Line("Support Bundle + Alarm", 12, 700, "#111827"),
        Line("vm-support → .tgz on datastore", 10.5, 400, "#374151"),
        Line("custom datastore-usage alarm enabled", 10.5, 400, "#374151"),
    ])
    c.node_box(500, 340, 400, 110, "neutral", [
        Line("esxtop CPU Contention", 12, 700, "#111827"),
        Line("synthetic load exceeds logical CPUs", 10.5, 400, "#374151"),
        Line("%RDY rises, then returns to baseline", 10.5, 400, "#374151"),
    ])
    c.legend(60, 570, [("mgmt", "Compliant baseline"), ("alt", "Remediated state"), ("warn", "Drift (negative test)")])
    c.save(f"{OUT}/chapter-09-vlcm-drift-remediation-flow.svg")


def ch11():
    c = Canvas(960, 660,
        title="Chapter 11 Hands-On Lab: NSX Tier-0/Tier-1 Gateways with a Traceflow-Verified DFW Allow Rule",
        subtitle="A default-deny DFW rule blocks test-app-01 to test-db-01 until a scoped allow rule is added above it",
        svg_title="Chapter 11 lab topology: a Tier-0/Tier-1 gateway hierarchy with an overlay segment and a DFW policy verified by Traceflow",
        svg_desc="A Tier-0 gateway peers over BGP with a simulated upstream router (neighbor Established); a "
                  "Tier-1 gateway attaches beneath it, with an overlay segment using DHCP relay. test-app-01 and "
                  "test-db-01 deploy onto the segment, receive DHCP-relayed addresses, and can ping each other and "
                  "the gateway. A DFW policy section's default-deny rule initially blocks test-app-01 to "
                  "test-db-01 on TCP 5432; Traceflow confirms the packet reaches the destination segment but is "
                  "dropped by the default-deny rule, not a routing failure. A scoped allow rule for exactly that "
                  "flow is added above the default-deny rule; Traceflow now shows the allow rule as the match, and "
                  "a third, out-of-group test VM remains blocked, confirming the Applied To scope is not "
                  "inadvertently permissive.")
    c.node_box(370, 110, 220, 90, "mgmt", [
        Line("Tier-0 Gateway", 13.5, 700, "#111827"),
        Line("BGP to upstream: Established", 10.5, 400, "#374151"),
    ])
    c.connector(480, 200, 480, 240, "mgmt")
    c.node_box(370, 240, 220, 80, "mgmt", [
        Line("Tier-1 Gateway", 13, 700, "#111827"),
        Line("overlay segment, DHCP relay", 10.5, 400, "#374151"),
    ])
    c.node_box(120, 380, 220, 100, "alt", [
        Line("test-app-01", 13, 700, "#111827"),
        Line("DHCP-relayed address", 10.5, 400, "#374151"),
    ])
    c.node_box(620, 380, 220, 100, "warn", [
        Line("test-db-01", 13, 700, "#111827"),
        Line("TCP 5432: allow rule added", 10.5, 700, "#14532d"),
        Line("(was default-deny — negative test)", 10, 400, "#7f1d1d"),
    ])
    c.connector(390, 340, 230, 380, "mgmt")
    c.connector(570, 340, 730, 380, "mgmt")
    c.connector(340, 430, 620, 430, "warn", label="default-deny → Traceflow confirms drop → allow rule added → succeeds")
    c.node_box(60, 540, 840, 60, "neutral", [
        Line("Out-of-group 3rd VM attempts the same flow → still blocked by default-deny (Applied To scope confirmed correct)", 11.5, 400, "#374151"),
    ])
    c.legend(60, 610, [("mgmt", "Gateway hierarchy"), ("alt", "Source group"), ("warn", "DFW-controlled flow")])
    c.save(f"{OUT}/chapter-11-nsx-tier0-tier1-dfw-topology.svg")


def ch12():
    c = Canvas(960, 560,
        title="Chapter 12 Hands-On Lab: Timed NSX Build-and-Troubleshoot Self-Assessment (VCP-NV)",
        subtitle="Five timed steps from transport-zone prep through a blind negative test, target under 90 minutes total",
        svg_title="Chapter 12 lab flow: a timed, unaided NSX build-and-troubleshoot exercise for exam self-assessment",
        svg_desc="From a clean NSX state, five timed steps are completed from memory without reference material: "
                  "transport zone/uplink profile/TEP pool and transport node prep (target 20 minutes), Edge node "
                  "and Edge cluster (15 minutes), Tier-0 BGP plus Tier-1 and overlay segment (20 minutes), a DFW "
                  "default-deny plus scoped allow policy (15 minutes), and a blind negative test diagnosing one "
                  "deliberately introduced fault — a wrong BGP AS number, a mis-scoped DFW rule, or an exhausted "
                  "TEP pool — using only Traceflow, BGP neighbor status, and transport node status (15 minutes). "
                  "Total elapsed time under 90 minutes with all steps unaided is a strong exam-readiness signal.")
    c.node_box(40, 140, 160, 100, "mgmt", [
        Line("1. Transport prep", 11.5, 700, "#111827"),
        Line("zone/uplink/TEP", 10, 400, "#374151"),
        Line("target 20 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(220, 140, 160, 100, "mgmt", [
        Line("2. Edge cluster", 11.5, 700, "#111827"),
        Line("Edge node join", 10, 400, "#374151"),
        Line("target 15 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 160, 100, "mgmt", [
        Line("3. T0/T1 + BGP", 11.5, 700, "#111827"),
        Line("overlay segment", 10, 400, "#374151"),
        Line("target 20 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(580, 140, 160, 100, "mgmt", [
        Line("4. DFW policy", 11.5, 700, "#111827"),
        Line("deny + scoped allow", 10, 400, "#374151"),
        Line("target 15 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(760, 140, 160, 100, "warn", [
        Line("5. Blind fault", 11.5, 700, "#7f1d1d"),
        Line("diagnose unaided", 10, 700, "#7f1d1d"),
        Line("target 15 min", 10, 700, "#7f1d1d"),
    ])
    c.connector(200, 190, 220, 190, "mgmt")
    c.connector(380, 190, 400, 190, "mgmt")
    c.connector(560, 190, 580, 190, "mgmt")
    c.connector(740, 190, 760, 190, "warn")
    c.node_box(160, 320, 640, 110, "warn", [
        Line("Negative Test (step 5)", 12.5, 700, "#7f1d1d"),
        Line("one fault injected blind: wrong BGP AS, mis-scoped DFW Applied To, or exhausted TEP pool", 11, 400, "#7f1d1d"),
        Line("diagnosed using Traceflow / BGP neighbor status / transport node status only — no reference material", 11, 400, "#7f1d1d"),
    ])
    c.connector(840, 240, 480, 320, "warn")
    c.text(480, 480, "Total elapsed time under 90 minutes, all results achieved unaided: strong exam-readiness signal", 12, 700, "#111827")
    c.legend(160, 520, [("mgmt", "Timed build step"), ("warn", "Timed diagnosis step")])
    c.save(f"{OUT}/chapter-12-nsx-timed-self-assessment-flow.svg")


def ch13():
    c = Canvas(960, 560,
        title="Chapter 13 Hands-On Lab: Layered VCF-Support Diagnostic Workflow Across Three Failure Domains",
        subtitle="Identity, networking, and storage faults are each diagnosed unaided in under 15 minutes from a known-good baseline",
        svg_title="Chapter 13 lab flow: three blind faults across identity, networking, and storage domains, each diagnosed against a target time",
        svg_desc="A baseline health check confirms host connection state, vCenter Server services, NSX Manager "
                  "cluster status, and DFW/gateway configuration are all healthy. Three faults are then introduced "
                  "blind: a vCenter machine SSL certificate or LDAPS credential problem (identity domain, "
                  "diagnosed with vecs-cli and identity-source test-connection), a mis-scoped DFW rule (networking "
                  "domain, diagnosed with Traceflow and rule hit counters), and a vSAN network partition or "
                  "datastore loss (storage domain, diagnosed with esxcli vsan cluster get and Skyline Health). "
                  "Each diagnosis is timed against a 15-minute target, then all three faults are restored to the "
                  "known-good baseline.")
    c.node_box(60, 130, 220, 80, "neutral", [
        Line("Baseline Health Check", 12.5, 700, "#111827"),
        Line("all layers healthy", 10.5, 700, "#14532d"),
    ])
    c.node_box(60, 260, 250, 120, "warn", [
        Line("Fault 1: Identity", 12, 700, "#7f1d1d"),
        Line("cert expiry / LDAPS bind cred", 10.5, 400, "#7f1d1d"),
        Line("vecs-cli, test-connection", 10, 400, "#374151"),
        Line("target: 15 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(355, 260, 250, 120, "warn", [
        Line("Fault 2: Networking", 12, 700, "#7f1d1d"),
        Line("DFW Applied To mis-scoped", 10.5, 400, "#7f1d1d"),
        Line("Traceflow, rule hit counters", 10, 400, "#374151"),
        Line("target: 15 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(650, 260, 250, 120, "warn", [
        Line("Fault 3: Storage", 12, 700, "#7f1d1d"),
        Line("vSAN partition / datastore loss", 10.5, 400, "#7f1d1d"),
        Line("vsan cluster get, Skyline Health", 10, 400, "#374151"),
        Line("target: 15 min", 10, 700, "#1d4ed8"),
    ])
    c.connector(170, 210, 170, 260, "warn")
    c.connector(470, 210, 470, 260, "warn")
    c.connector(770, 210, 770, 260, "warn")
    c.node_box(60, 430, 840, 80, "alt", [
        Line("All three faults restored to known-good baseline; step-1 health check passes again", 12, 700, "#14532d"),
    ])
    c.legend(60, 530, [("neutral", "Baseline state"), ("warn", "Timed blind fault"), ("alt", "Restored state")])
    c.save(f"{OUT}/chapter-13-vcf-support-diagnostic-flow.svg")


def ch14():
    c = Canvas(960, 620,
        title="Chapter 14 Hands-On Lab: VCF Administrator Workflow — Commissioning, RBAC Layering, and Import Prerequisites",
        subtitle="A deliberately broken NTP prerequisite fails commissioning by name before being corrected and re-verified",
        svg_title="Chapter 14 lab flow: host commissioning prerequisites, workload-domain-style cluster creation, and RBAC layering",
        svg_desc="Host commissioning prerequisites (NTP sync, DNS resolution, acceptance level) are verified on an "
                  "additional host. As a negative test, NTP is deliberately misconfigured and commissioning is "
                  "attempted; the validation fails or warns specifically on the time-synchronization prerequisite, "
                  "naming the actual root cause rather than a generic error. NTP is corrected and re-verified, "
                  "then a new cluster (representing a VI workload domain's compute layer) is created with HA/DRS "
                  "and the host joins successfully. A scoped RBAC role at the new cluster's folder confirms a test "
                  "account can manage the new cluster but is denied against the pre-existing standalone "
                  "infrastructure. The standalone vCenter's certificate store is inspected as import-path "
                  "preparation.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Prerequisite Checks", 12.5, 700, "#111827"),
        Line("NTP, DNS, acceptance level", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 130, 240, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("NTP pointed at unreachable server", 10.5, 700, "#7f1d1d"),
        Line("commissioning fails, names NTP", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 185, 380, 185, "warn")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Corrected + Verified", 12, 700, "#111827"),
        Line("NTP fixed, re-check passes", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 185, 700, 185, "alt")
    c.node_box(60, 300, 260, 110, "mgmt", [
        Line("lab-wld-cluster", 12.5, 700, "#111827"),
        Line("HA + DRS, host joins", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 300, 260, 110, "alt", [
        Line("Scoped RBAC role", 12.5, 700, "#111827"),
        Line("manages new cluster only", 10.5, 700, "#14532d"),
        Line("denied on standalone infra", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(700, 300, 220, 110, "neutral", [
        Line("Certificate Store", 12.5, 700, "#111827"),
        Line("vecs-cli entry list", 10.5, 400, "#374151"),
        Line("(import-path prerequisite)", 10, 400, "#374151"),
    ])
    c.connector(810, 240, 810, 300, "neutral")
    c.legend(60, 500, [("mgmt", "Prerequisite / infrastructure"), ("alt", "Corrected / scoped state"), ("warn", "Negative-test path")])
    c.save(f"{OUT}/chapter-14-vcf-admin-commissioning-rbac-flow.svg")


def ch15():
    c = Canvas(960, 560,
        title="Chapter 15 Hands-On Lab: Timed VVF Build-and-Troubleshoot Self-Assessment (VCP-VVF Administrator)",
        subtitle="Four timed builds followed by two timed negative tests, target under 2 hours total",
        svg_title="Chapter 15 lab flow: a timed, combined vSphere/vSAN/HA-DRS build exercise culminating in two diagnostic negative tests",
        svg_desc="Four timed build steps reuse earlier chapters' procedures as one continuous exercise: 3 ESXi "
                  "hosts plus vCenter Server with a Host Profile (target 30 minutes), a VDS with a tagged port "
                  "group (20 minutes), vSAN with a RAID-1 FTT=1 policy and compliant test VM (25 minutes), and HA "
                  "admission control plus DRS Fully Automated (20 minutes). Two timed negative tests follow: a "
                  "host placed in maintenance mode with no data migration while the test VM has replica components "
                  "on it, diagnosing the resulting reduced-redundancy state (15 minutes), and induced CPU "
                  "contention diagnosed via esxtop %RDY (15 minutes). Total elapsed time under 2 hours, achieved "
                  "largely unaided, is a strong readiness signal.")
    c.node_box(40, 140, 200, 100, "mgmt", [
        Line("1. Hosts + vCenter", 11.5, 700, "#111827"),
        Line("+ Host Profile", 10, 400, "#374151"),
        Line("target 30 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(260, 140, 200, 100, "mgmt", [
        Line("2. VDS + port group", 11.5, 700, "#111827"),
        Line("tagged, 3 hosts", 10, 400, "#374151"),
        Line("target 20 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(480, 140, 200, 100, "mgmt", [
        Line("3. vSAN RAID-1 FTT=1", 11.5, 700, "#111827"),
        Line("compliant test VM", 10, 400, "#374151"),
        Line("target 25 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(700, 140, 220, 100, "mgmt", [
        Line("4. HA + DRS", 11.5, 700, "#111827"),
        Line("admission control", 10, 400, "#374151"),
        Line("target 20 min", 10, 700, "#1d4ed8"),
    ])
    c.connector(240, 190, 260, 190, "mgmt")
    c.connector(460, 190, 480, 190, "mgmt")
    c.connector(680, 190, 700, 190, "mgmt")
    c.node_box(160, 300, 320, 110, "warn", [
        Line("Negative test 1", 12, 700, "#7f1d1d"),
        Line("host in maintenance, no data migration", 10.5, 400, "#7f1d1d"),
        Line("diagnose reduced-redundancy state", 10.5, 400, "#7f1d1d"),
        Line("target 15 min", 10, 700, "#7f1d1d"),
    ])
    c.node_box(500, 300, 320, 110, "warn", [
        Line("Negative test 2", 12, 700, "#7f1d1d"),
        Line("induced CPU contention", 10.5, 400, "#7f1d1d"),
        Line("diagnose via esxtop %RDY", 10.5, 400, "#7f1d1d"),
        Line("target 15 min", 10, 700, "#7f1d1d"),
    ])
    c.connector(810, 240, 320, 300, "warn")
    c.connector(810, 240, 660, 300, "warn")
    c.text(480, 470, "Total elapsed time under 2 hours, largely unaided: strong readiness signal", 12, 700, "#111827")
    c.legend(160, 510, [("mgmt", "Timed build step"), ("warn", "Timed diagnosis step")])
    c.save(f"{OUT}/chapter-15-vvf-admin-timed-self-assessment-flow.svg")


def ch16():
    c = Canvas(960, 560,
        title="Chapter 16 Hands-On Lab: Timed VVF Support Diagnostic Across Compute, Storage, and Network",
        subtitle="Three timed faults plus an untimed licensing-recognition exercise, each traced to its layer without reference material",
        svg_title="Chapter 16 lab flow: three timed layered faults in a VVF-scoped lab, plus a licensing-tier recognition exercise",
        svg_desc="A baseline health check confirms compute, storage, and network layers are healthy in a "
                  "VVF-scoped lab (vSphere + vSAN, no NSX). Three timed faults follow: hostd stopped on one host "
                  "(compute domain, target 10 minutes, diagnosed via DCUI/esxcli as a management-agent issue "
                  "distinct from full host failure), an MTU mismatch on a vSAN VMkernel adapter (storage domain, "
                  "target 15 minutes, diagnosed via esxcli vsan cluster get and vmkping), and a misconfigured port "
                  "group VLAN ID (network domain, target 10 minutes, diagnosed per Chapter 4's approach). An "
                  "untimed licensing-recognition exercise identifies a feature unavailable under a more "
                  "restrictive license tier without changing the actual assignment. All three faults are then "
                  "restored to baseline.")
    c.node_box(60, 130, 220, 80, "neutral", [
        Line("Baseline Health Check", 12.5, 700, "#111827"),
        Line("compute/storage/network: healthy", 10, 700, "#14532d"),
    ])
    c.node_box(60, 250, 250, 110, "warn", [
        Line("Fault 1: Compute", 12, 700, "#7f1d1d"),
        Line("hostd stopped on one host", 10.5, 400, "#7f1d1d"),
        Line("DCUI/esxcli restart, no reboot", 10, 400, "#374151"),
        Line("target: 10 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(355, 250, 250, 110, "warn", [
        Line("Fault 2: Storage", 12, 700, "#7f1d1d"),
        Line("vSAN VMkernel MTU mismatch", 10.5, 400, "#7f1d1d"),
        Line("vsan cluster get, vmkping", 10, 400, "#374151"),
        Line("target: 15 min", 10, 700, "#1d4ed8"),
    ])
    c.node_box(650, 250, 250, 110, "warn", [
        Line("Fault 3: Network", 12, 700, "#7f1d1d"),
        Line("port group VLAN ID wrong", 10.5, 400, "#7f1d1d"),
        Line("diagnosed per Chapter 4", 10, 400, "#374151"),
        Line("target: 10 min", 10, 700, "#1d4ed8"),
    ])
    c.connector(170, 210, 170, 250, "warn")
    c.connector(470, 210, 470, 250, "warn")
    c.connector(770, 210, 770, 250, "warn")
    c.node_box(60, 410, 840, 70, "neutral", [
        Line("Untimed: licensing-recognition exercise — identify one feature gated by a more restrictive license tier", 11.5, 400, "#374151"),
    ])
    c.legend(60, 510, [("neutral", "Baseline / untimed exercise"), ("warn", "Timed layered fault")])
    c.save(f"{OUT}/chapter-16-vvf-support-timed-diagnostic-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09(); ch11(); ch12(); ch13(); ch14(); ch15(); ch16()
