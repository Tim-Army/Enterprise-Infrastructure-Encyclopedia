import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-23-dell-idrac-9-10-administration"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Hands-On Lab: The Old Factory Password Stops Authenticating the Moment It's Changed",
        subtitle="First access to a lab iDRAC is validated identically from RACADM and Redfish, then the retired credential is confirmed dead",
        svg_title="Chapter 1 lab flow: first access to a PowerEdge iDRAC validated from both RACADM and Redfish after a mandatory password change, tested against the retired factory-default credential",
        svg_desc="Logging in with factory-default credentials forces an immediate password change before "
                  "reaching the dashboard. RACADM over SSH reports the service tag, firmware version, and "
                  "license tier, and a Redfish bootstrap-check script authenticates with the new password and "
                  "prints the same identity data, confirming both management paths agree. As a negative test, "
                  "the same script is re-run with the old factory-default password; the session raises an HTTP "
                  "401 error, confirming the retired credential no longer authenticates once the change has "
                  "taken effect.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Factory login → forced change", 12.5, 700, "#111827"),
        Line("racadm getsysinfo/getversion", 10.5, 400, "#374151"),
        Line("license tier confirmed", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("idrac_first_boot_check.py", 12.5, 700, "#111827"),
        Line("new password", 10.5, 400, "#374151"),
        Line("→ model, firmware, tag, power state", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("old factory password", 10.5, 700, "#7f1d1d"),
        Line("→ HTTP 401", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("RACADM and Redfish report the same identity data through two different management paths — the", 11.5, 400, "#374151"),
        Line("negative test confirms the credential change is enforced consistently across both.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "First-access bring-up"), ("alt", "Redfish validation"), ("warn", "Retired credential")])
    c.save(f"{OUT}/chapter-01-idrac-first-access-validation-flow.svg")


def ch02():
    c = Canvas(960, 600,
        title="Chapter 2 Hands-On Lab: SCP Import Validates Against Actual Present Hardware Rather Than Succeeding Silently",
        subtitle="A known-good configuration baseline survives a non-disruptive controller restart intact; an import for hardware that isn't there fails at the component level",
        svg_title="Chapter 2 lab flow: an iDRAC configuration baseline exported and preserved across a soft controller restart, tested against an SCP import targeting a component group the hardware does not have",
        svg_desc="The full iDRAC configuration exports to a network share as an XML baseline, alongside a "
                  "smaller iDRAC-only component export for comparison. A soft controller restart drops the "
                  "current session and makes the GUI and API briefly unreachable, with no effect on host OS "
                  "uptime; once the controller returns, the configuration matches the baseline exported before "
                  "the restart. As a negative test, an SCP import targets a RAID component group on hardware "
                  "that does not have a PERC controller; the job reports a component-level failure rather than "
                  "succeeding, confirming SCP import validates against actual present hardware before applying "
                  "anything.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("systemconfig export → XML baseline", 12.5, 700, "#111827"),
        Line("racreset soft", 10.5, 700, "#1d4ed8"),
        Line("brief unreachability, no host reboot", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Controller returns", 12.5, 700, "#111827"),
        Line("configuration matches", 10.5, 700, "#14532d"),
        Line("pre-restart baseline exactly", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("import RAID component group", 10.5, 700, "#7f1d1d"),
        Line("onto hardware without a PERC", 10.5, 700, "#7f1d1d"),
        Line("→ component-level failure", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("lab-baseline.xml is retained for reuse in later chapters, where specific component groups are", 11.5, 400, "#374151"),
        Line("imported after deliberate configuration changes are made.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Baseline export + restart"), ("alt", "Preserved configuration"), ("warn", "Rejected unsupported import")])
    c.save(f"{OUT}/chapter-02-scp-baseline-restart-flow.svg")


def ch03():
    c = Canvas(960, 620,
        title="Chapter 3 Hands-On Lab: A Wrong Gateway Isolates the Fault to Routed Traffic, Not the Whole Network Path",
        subtitle="Static IPv4, DNS registration, and NTP are all confirmed consistent between RACADM and Redfish; a bad gateway breaks only what a gateway is responsible for",
        svg_title="Chapter 3 lab topology: static IPv4 addressing, DNS registration, and NTP configured on a lab iDRAC and cross-validated over Redfish, tested against a deliberately wrong gateway",
        svg_desc="A static IPv4 address replaces DHCP addressing, DNS registration makes the iDRAC resolvable "
                  "by hostname within minutes, and NTP configuration brings its reported time in line with real "
                  "time. Querying the Redfish EthernetInterfaces resource confirms the same address, mask, and "
                  "gateway configured through RACADM. As a negative test, the gateway is deliberately set "
                  "wrong; the iDRAC remains reachable from the same local subnet, since local-subnet traffic "
                  "never needs a gateway, while any off-subnet or routed test fails — isolating the fault "
                  "precisely to the deliberately broken gateway rather than the network configuration as a "
                  "whole. The correct gateway is restored afterward.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Static IPv4 + DNS registration", 12.5, 700, "#111827"),
        Line("idrac-lab-01 resolves to new IP", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "mgmt", [
        Line("NTP configured", 12.5, 700, "#111827"),
        Line("reported time matches", 10.5, 700, "#1d4ed8"),
        Line("real time within seconds", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Redfish EthernetInterfaces", 12.5, 700, "#111827"),
        Line("confirms same address,", 10.5, 700, "#14532d"),
        Line("mask, and gateway", 10.5, 400, "#374151"),
    ])
    c.connector(600, 185, 700, 185, "alt")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("wrong gateway set", 10.5, 700, "#7f1d1d"),
        Line("local subnet: reachable / off-subnet: fails", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("the fault is scoped precisely to routed reachability, not local connectivity — exactly what a", 11.5, 400, "#374151"),
        Line("gateway is and isn't responsible for.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Network + time baseline"), ("alt", "Redfish cross-check"), ("warn", "Gateway-scoped fault")])
    c.save(f"{OUT}/chapter-03-idrac-network-gateway-topology.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: A Scoped Operator Account Is Blocked From the One Setting It Was Never Granted",
        subtitle="A CA-signed certificate replaces the factory self-signed one while a Virtual-Console-only account is confirmed unable to touch network configuration",
        svg_title="Chapter 4 lab flow: a scoped Operator-tier local user and a CA-signed certificate installed on a lab iDRAC, tested against an attempt to change network settings from the restricted account",
        svg_desc="A scoped local user is created with login and Virtual Console privilege only, no configuration "
                  "privilege, and logging in as that user confirms configuration pages are visible but not "
                  "modifiable. A CSR is generated, signed by a lab CA, and uploaded; after the controller "
                  "restarts, the original self-signed certificate warning is gone. Secure Boot status reported "
                  "by RACADM and Redfish agree. As a negative test, the scoped operator account attempts to "
                  "change the Chapter 3 network gateway setting; the command fails with a permission-denied "
                  "response, confirming the scoped privilege genuinely excludes configuration access rather than "
                  "merely hiding it in the GUI.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("lab-operator: login + VConsole only", 12.5, 700, "#111827"),
        Line("CSR generated, signed by lab CA", 10.5, 400, "#374151"),
        Line("cert uploaded, controller restarts", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Secure Boot status", 12.5, 700, "#111827"),
        Line("RACADM and Redfish agree", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("lab-operator attempts", 10.5, 700, "#7f1d1d"),
        Line("set iDRAC.IPv4.Gateway", 10.5, 700, "#7f1d1d"),
        Line("→ permission denied", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("System Lockdown Mode and System Erase are described in this chapter for understanding, not", 11.5, 400, "#374151"),
        Line("exercised here — both are disruptive or irreversible against shared lab hardware.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Scoped account + certificate"), ("alt", "Cross-validated Secure Boot"), ("warn", "Denied configuration attempt")])
    c.save(f"{OUT}/chapter-04-idrac-identity-certificate-flow.svg")


def ch05():
    c = Canvas(960, 580,
        title="Chapter 5 Hands-On Lab: A Missing Image Fails the Mount Cleanly Instead of Booting to an Unpredictable State",
        subtitle="iDRAC Direct reaches the same controller as the network path, and Virtual Media boots a real image while an invalid one is safely rejected",
        svg_title="Chapter 5 lab flow: iDRAC Direct local access and a Virtual Media mount-and-boot sequence over the network path, tested against a Virtual Media image path that does not exist",
        svg_desc="Connecting over the front iDRAC Direct USB port reaches the identical login and dashboard as "
                  "the normal management network, confirming it is the same controller over a different "
                  "physical path. Over the network path, Virtual Console shows live server output, and a script "
                  "mounts a test ISO as Virtual Media; the server restarts and boots from the mounted image "
                  "rather than its normal boot device, confirmed by the virtual media slot reporting attached. "
                  "As a negative test, the same script targets an image path that does not exist on the share; "
                  "the insert-media call fails with an error and the server does not boot from an empty or "
                  "invalid mount, confirming the mount step fails safely rather than producing an unpredictable "
                  "boot state.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("iDRAC Direct (USB)", 12.5, 700, "#111827"),
        Line("same login/dashboard as", 10.5, 400, "#374151"),
        Line("the network management path", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("idrac_mount_and_boot.py", 12.5, 700, "#111827"),
        Line("valid ISO on reachable share", 10.5, 400, "#374151"),
        Line("→ server boots from mounted image", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("nonexistent image path", 10.5, 700, "#7f1d1d"),
        Line("→ insert-media fails,", 10.5, 700, "#7f1d1d"),
        Line("no unpredictable boot", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("virtual media is ejected and boot-once is disabled afterward so a later normal reboot does not", 11.5, 400, "#374151"),
        Line("unexpectedly boot to test media again.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "iDRAC Direct local access"), ("alt", "Successful media boot"), ("warn", "Safe mount failure")])
    c.save(f"{OUT}/chapter-05-idrac-direct-virtual-media-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: The Alerting Pipeline Surfaces a Delivery Failure Rather Than Masking It",
        subtitle="A test alert is confirmed delivered end to end and logged; an unreachable SMTP relay fails the same test loudly instead of reporting false success",
        svg_title="Chapter 6 lab flow: an email alert destination configured and validated end to end with a test alert, cross-checked against the Lifecycle Log, tested against an unreachable SMTP relay",
        svg_desc="An email alert destination and SMTP relay are configured, and a test alert reaches that "
                  "destination within a few minutes, confirming the pipeline works end to end rather than only "
                  "appearing correctly configured. The Lifecycle Log shows a corresponding entry for the "
                  "test-alert event, and a recent-events script confirms no unexpected Critical-severity entries "
                  "in the healthy lab unit. A Tech Support Report bundle scoped to iDRAC and system information "
                  "completes and appears on the target share. As a negative test, the SMTP relay address is "
                  "deliberately pointed at an unreachable host and the test alert is resent; it fails with a "
                  "delivery error rather than silently reporting success, confirming the pipeline surfaces "
                  "delivery failures rather than masking them.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Email alert destination + SMTP", 12.5, 700, "#111827"),
        Line("racadm testemail -i 1", 10.5, 400, "#374151"),
        Line("→ received within minutes", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Lifecycle Log + TSR bundle", 12.5, 700, "#111827"),
        Line("test-alert entry confirmed,", 10.5, 700, "#14532d"),
        Line("no unexpected Critical entries", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("SMTP relay → unreachable host", 10.5, 700, "#7f1d1d"),
        Line("testemail → delivery error", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the correct SMTP relay address is restored afterward, since leaving the unreachable address in", 11.5, 400, "#374151"),
        Line("place would silently break real alerting going forward.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Alert pipeline configured"), ("alt", "Cross-checked delivery"), ("warn", "Surfaced delivery failure")])
    c.save(f"{OUT}/chapter-06-idrac-alerting-lifecycle-log-flow.svg")


def ch07():
    c = Canvas(960, 600,
        title="Chapter 7 Hands-On Lab: Deleting a Virtual Disk by a Nonexistent ID Is Rejected, Not Ignored",
        subtitle="A RAID 1 test virtual disk and dedicated hot spare are built cleanly and torn down deliberately, with an invalid delete target caught first",
        svg_title="Chapter 7 lab flow: a RAID 1 test virtual disk created with a dedicated hot spare on a lab PERC controller, tested against a delete request referencing a nonexistent virtual disk ID",
        svg_desc="Physical disks confirmed as spare and Ready are combined into a RAID 1 test virtual disk, "
                  "which reports Ready/Online, and a third spare disk is assigned as its dedicated hot spare. A "
                  "storage health check script confirms no drives are flagged before the negative test runs. As "
                  "a negative test, a delete request deliberately references a virtual disk ID that does not "
                  "exist; the command returns an error rather than succeeding or silently no-op'ing, confirming "
                  "the platform validates the target before acting. The actual test virtual disk is then deleted "
                  "for real, confirmed absent from subsequent disk listings.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("RAID 1 test VD created", 12.5, 700, "#111827"),
        Line("dedicated hot spare assigned", 10.5, 400, "#374151"),
        Line("storage health check: clean", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("deletevd: Disk.Virtual.99", 10.5, 700, "#7f1d1d"),
        Line("(nonexistent) → error", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "alt", [
        Line("Real deletion", 12.5, 700, "#111827"),
        Line("deletevd: Disk.Virtual.0", 10.5, 400, "#374151"),
        Line("→ VD no longer listed", 10.5, 700, "#14532d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the invalid-ID delete attempt runs before the real deletion, confirming target validation happens", 11.5, 400, "#374151"),
        Line("independently of whether a matching disk would otherwise be deletable.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Storage baseline build"), ("warn", "Rejected invalid target"), ("alt", "Confirmed real deletion")])
    c.save(f"{OUT}/chapter-07-idrac-raid-hotspare-flow.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: The Update Pipeline Validates Image Retrieval Before It Ever Applies Anything",
        subtitle="An iDRAC firmware update stages, applies, and logs cleanly through a controller restart, while an unreachable image URI is rejected before it can be staged",
        svg_title="Chapter 8 lab flow: an iDRAC firmware update staged, applied, and confirmed through a controller restart and the Lifecycle Log, tested against a nonexistent firmware image URI",
        svg_desc="Current firmware inventory records the pre-update iDRAC version, and a staged update task "
                  "progresses to Completed, with the controller restarting automatically as part of applying "
                  "iDRAC firmware; once it returns, the reported version matches the update just applied, and "
                  "the Lifecycle Log shows a corresponding entry with a matching timestamp. As a negative test, "
                  "an update is staged referencing an image URI that does not exist; the task reports an "
                  "Exception state, or the initial request itself fails, confirming the update pipeline "
                  "validates image retrieval rather than silently accepting an unreachable source. A rollback "
                  "attempt afterward either restores the prior version or correctly reports no rollback image is "
                  "available — both valid, informative outcomes.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Firmware inventory recorded", 12.5, 700, "#111827"),
        Line("idrac_stage_update.py: valid image", 10.5, 400, "#374151"),
        Line("→ TaskState: Completed, version confirmed", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Lifecycle Log entry", 12.5, 700, "#111827"),
        Line("matches update timestamp", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("nonexistent image URI", 10.5, 700, "#7f1d1d"),
        Line("→ Exception state / POST fails", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("both rollback outcomes — restored to a prior version, or no rollback image available — are", 11.5, 400, "#374151"),
        Line("recorded as valid, informative results rather than treated as failures of the lab itself.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Staged + applied update"), ("alt", "Logged confirmation"), ("warn", "Rejected unreachable source")])
    c.save(f"{OUT}/chapter-08-idrac-firmware-update-rollback-flow.svg")


def ch09():
    c = Canvas(960, 640,
        title="Chapter 9 Hands-On Lab: The Capstone — Every Chapter's Fail-Safe Behavior Still Holds Inside One Combined Sequence",
        subtitle="Network, identity, storage, and firmware baselines from the whole volume come together into one provisioning runbook, with the Virtual Media fail-safe re-verified at the end",
        svg_title="Chapter 9 capstone lab flow: a full provisioning runbook combining network, identity, storage, firmware, and Virtual Media deployment from every prior chapter, tested against an unreachable OS image URL",
        svg_desc="A pre-capstone SCP baseline is exported as a rollback point, then network configuration, "
                  "certificate-based identity hardening, a clean storage health check, and a recorded firmware "
                  "inventory baseline are each confirmed in sequence before a test OS is deployed via the "
                  "Virtual Media pattern; the server boots from the mounted image, confirming network, identity, "
                  "storage, firmware, and remote media boot all function together as one coherent provisioning "
                  "sequence. The Lifecycle Log shows every major step in chronological order as a single "
                  "reviewable timeline. As a negative test, the Virtual Media step is deliberately re-run with an "
                  "unreachable image URL; the same fail-safe behavior validated in Chapter 5 still holds when "
                  "invoked as part of this larger combined sequence, failing cleanly rather than booting to an "
                  "unpredictable state.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Pre-capstone SCP baseline", 12.5, 700, "#111827"),
        Line("network, identity, storage,", 10.5, 400, "#374151"),
        Line("firmware baselines confirmed", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "alt", [
        Line("Virtual Media OS deploy", 12.5, 700, "#111827"),
        Line("server boots from image", 10.5, 700, "#14532d"),
        Line("Lifecycle Log: full timeline", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "neutral", [
        Line("Every chapter's baseline", 12, 700, "#111827"),
        Line("functions together as one", 10.5, 400, "#374151"),
        Line("coherent sequence", 10.5, 400, "#374151"),
    ])
    c.connector(600, 185, 700, 185, "alt")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("re-run Virtual Media, unreachable URL", 10.5, 700, "#7f1d1d"),
        Line("→ same fail-safe as Chapter 5 holds", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("running each chapter's technique inside a single combined runbook — not just individually — is", 11.5, 400, "#374151"),
        Line("what confirms the volume's fail-safe behaviors compose correctly under real operational sequencing.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Cross-chapter baseline"), ("alt", "Combined provisioning sequence"), ("warn", "Re-verified fail-safe")])
    c.save(f"{OUT}/chapter-09-capstone-provisioning-runbook-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
