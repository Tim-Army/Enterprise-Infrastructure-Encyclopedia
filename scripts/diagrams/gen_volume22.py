import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-22-dell-openmanage-enterprise"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Hands-On Lab: The Session Endpoint Rejects a Wrong Password Rather Than Issuing a Token Anyway",
        subtitle="A fresh OME appliance is bootstrapped through the console wizard, then validated end to end over the REST API",
        svg_title="Chapter 1 lab flow: an OME virtual appliance deployed and bootstrapped through the first-run wizard, then validated over the REST API, tested against an intentionally wrong password",
        svg_desc="An OME virtual appliance is imported, network-bootstrapped from its text console, and taken "
                  "through the browser first-run wizard, ending with a home dashboard showing zero managed "
                  "devices and no active alerts. A bootstrap-check script authenticates against the session "
                  "endpoint with the new admin password and prints the appliance version, confirming the REST "
                  "API and session-token workflow both succeed. As a negative test, the same script is re-run "
                  "with an intentionally wrong password; the session endpoint returns an HTTP error, typically "
                  "401, and the script exits non-zero, confirming the endpoint correctly rejects invalid "
                  "credentials rather than silently issuing a token anyway.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Appliance deploy + wizard", 12.5, 700, "#111827"),
        Line("static IP, EULA, admin password, NTP", 10.5, 400, "#374151"),
        Line("dashboard: 0 devices, 0 alerts", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("ome_bootstrap_check.py", 12.5, 700, "#111827"),
        Line("correct admin password", 10.5, 400, "#374151"),
        Line("→ version + product name printed", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("wrong password", 10.5, 700, "#7f1d1d"),
        Line("→ 401, script exits non-zero", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 320, 860, 90, "neutral", [
        Line("the session endpoint's raise_for_status() failure confirms the API validates credentials on every", 11.5, 400, "#374151"),
        Line("request rather than trusting a prior successful login state.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 450, [("mgmt", "Appliance bootstrap"), ("alt", "Valid API authentication"), ("warn", "Rejected credentials")])
    c.save(f"{OUT}/chapter-01-ome-bootstrap-api-validation-flow.svg")


def ch02():
    c = Canvas(960, 600,
        title="Chapter 2 Hands-On Lab: A Viewer-Tier Token Is Rejected With 403 When It Tries to Create an Account",
        subtitle="A least-privilege scoped account authenticates normally but is denied the one administrative action its role should not permit",
        svg_title="Chapter 2 lab flow: a scoped Viewer-tier local account created via the REST API, authenticated successfully, then tested against an administrative action it should not be permitted to perform",
        svg_desc="A lab-only CA-signed certificate is generated to practice the certificate-replacement workflow, "
                  "and a Viewer-tier local account is created via the account-creation script, scoped to an "
                  "empty test device group. Authenticating that account directly against the session endpoint "
                  "returns an HTTP 201 with a valid X-Auth-Token, confirming the restricted account can log in "
                  "normally. As a negative test, that same Viewer-tier token is used to attempt creating a second "
                  "local account, an administrative action outside its role; the API returns HTTP 403 Forbidden, "
                  "confirming the role boundary is enforced by the server rather than merely hidden in the "
                  "console UI. Three deliberately failed logins afterward also correctly lock the account.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("ome_create_scoped_user.py", 12.5, 700, "#111827"),
        Line("labviewer, Viewer role,", 10.5, 400, "#374151"),
        Line("scoped to lab-scope-test group", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("POST /SessionService/Sessions", 12, 700, "#111827"),
        Line("as labviewer", 10.5, 400, "#374151"),
        Line("→ 201, X-Auth-Token issued", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("labviewer token attempts", 10.5, 700, "#7f1d1d"),
        Line("POST /AccountService/Accounts", 10.5, 700, "#7f1d1d"),
        Line("→ 403 Forbidden", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("three deliberately failed labviewer logins afterward correctly lock the account in the user", 11.5, 400, "#374151"),
        Line("administration screen, confirming the lockout policy is active alongside the role boundary.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Scoped account creation"), ("alt", "Permitted authentication"), ("warn", "Denied administrative action")])
    c.save(f"{OUT}/chapter-02-scoped-account-rbac-flow.svg")


def ch03():
    c = Canvas(960, 640,
        title="Chapter 3 Hands-On Lab: A Wrong Community String Discovers Reachability but Never Onboards a Device",
        subtitle="A correct SNMP credential onboards the lab host into managed inventory; a wrong one and a missing iDRAC interface both fail differently and informatively",
        svg_title="Chapter 3 lab topology: an SNMP-discovered lab host onboarded into static and dynamic groups, tested against a wrong community string and an unsupported power-control action",
        svg_desc="A lab Linux host running an SNMP agent is discovered using the correct read-only community "
                  "string, then onboarded into managed inventory, added to a static group, and picked up "
                  "automatically by a dynamic group filtered on SNMP discovery protocol. A forced inventory "
                  "refresh updates its last-inventoried timestamp. As a first negative test, a second discovery "
                  "job against the same host using an intentionally wrong community string completes but reports "
                  "the target as unauthenticated and unidentified rather than onboarding it, confirming network "
                  "reachability alone does not produce a managed device. As a second negative test, a "
                  "device-control power action against this same SNMP-only host fails, since a generic "
                  "SNMP-discovered Linux host has no iDRAC out-of-band interface for OME to control.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("SNMP discovery: correct string", 12.5, 700, "#111827"),
        Line("onboarded → static + dynamic group", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "alt", [
        Line("RefreshInventory", 12.5, 700, "#111827"),
        Line("last-inventoried timestamp", 10.5, 700, "#14532d"),
        Line("updates", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test 1", 12, 700, "#7f1d1d"),
        Line("wrong community string", 10.5, 700, "#7f1d1d"),
        Line("→ unauthenticated, not onboarded", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(600, 185, 700, 185, "warn")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test 2", 12, 700, "#7f1d1d"),
        Line("power-control action vs. SNMP-only host", 10.5, 700, "#7f1d1d"),
        Line("→ rejected, no iDRAC OOB interface", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("both negative tests illustrate the inventory/control fidelity gap: SNMP discovery proves a host is", 11.5, 400, "#374151"),
        Line("reachable and identifiable, but only native iDRAC discovery exposes out-of-band device control.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Discovery + onboarding"), ("alt", "Inventory refresh"), ("warn", "Reachable but not manageable")])
    c.save(f"{OUT}/chapter-03-snmp-discovery-onboarding-topology.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: Severity Filtering Suppresses a Below-Threshold Event Rather Than Forwarding Everything",
        subtitle="A Warning-and-above alert policy forwards a real event to syslog; an identical Critical-only policy correctly stays silent for the same event",
        svg_title="Chapter 4 lab flow: an alert policy forwarding qualifying events to a syslog listener, cross-checked against the job engine's execution history, tested against a stricter severity-scoped policy",
        svg_desc="An alert policy scoped to the lab device group, matching Warning-and-above severity, forwards "
                  "a test event to a syslog listener; stopping the lab host's SNMP agent and forcing a refresh "
                  "produces a qualifying event that appears both in the syslog listener's output and the OME "
                  "console's alert log. Querying the job engine for the corresponding refresh job's execution "
                  "history shows a status consistent with the device becoming unreachable. As a negative test, a "
                  "second, otherwise identical policy scoped to Critical-only severity is exercised against the "
                  "same event; because a stopped SNMP agent typically registers below Critical severity, no line "
                  "appears in the syslog listener for this second policy, confirming severity filtering correctly "
                  "suppresses a non-matching event.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Alert policy: Warning+", 12.5, 700, "#111827"),
        Line("SNMP agent stopped → event fires", 10.5, 400, "#374151"),
        Line("→ syslog line + console alert", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("JobService/Jobs query", 12.5, 700, "#111827"),
        Line("refresh job execution history", 10.5, 400, "#374151"),
        Line("→ status: unreachable", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("Critical-only policy,", 10.5, 700, "#7f1d1d"),
        Line("same below-Critical event", 10.5, 700, "#7f1d1d"),
        Line("→ no syslog line", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the same underlying event is forwarded by the Warning+ policy and suppressed by the Critical-only", 11.5, 400, "#374151"),
        Line("policy — proving severity scope is enforced per policy, not applied globally to every forward action.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Qualifying event forwarded"), ("alt", "Job engine cross-check"), ("warn", "Suppressed by severity scope")])
    c.save(f"{OUT}/chapter-04-alert-policy-severity-filtering-flow.svg")


def ch05():
    c = Canvas(960, 580,
        title="Chapter 5 Hands-On Lab: Compliance Evaluation Against a Baseline That Does Not Exist Fails Loudly",
        subtitle="A real baseline evaluates per-device firmware drift against a catalog; a fabricated baseline ID is rejected outright",
        svg_title="Chapter 5 lab flow: a firmware baseline created against a catalog and device group, evaluated for compliance, tested against a nonexistent baseline ID",
        svg_desc="A baseline is created against an existing catalog and the Chapter 3 device group, then "
                  "compliance evaluation is triggered and polled to completion through the job engine. The "
                  "resulting per-device compliance report identifies at least one non-compliant device and a "
                  "specific non-compliant component with its severity classification. As a negative test, "
                  "compliance evaluation is triggered against a baseline ID that does not exist on the "
                  "appliance; the API returns an HTTP 4xx error rather than silently succeeding, confirming the "
                  "evaluation endpoint validates the baseline reference before doing any work.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Baseline: catalog + device group", 12.5, 700, "#111827"),
        Line("CheckBaselineCompliance job", 10.5, 400, "#374151"),
        Line("polled to completion", 10.5, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("DeviceComplianceReports", 12.5, 700, "#111827"),
        Line("non-compliant device +", 10.5, 700, "#14532d"),
        Line("component + severity identified", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("CheckBaselineCompliance", 10.5, 700, "#7f1d1d"),
        Line("against baseline 999999", 10.5, 700, "#7f1d1d"),
        Line("→ HTTP 4xx", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the same evaluation action succeeds against a real baseline and is rejected against a fabricated ID —", 11.5, 400, "#374151"),
        Line("the API validates the reference rather than trusting the caller's input.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Baseline + compliance job"), ("alt", "Per-device report"), ("warn", "Rejected nonexistent baseline")])
    c.save(f"{OUT}/chapter-05-firmware-baseline-compliance-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: A Catalog Refresh Genuinely Depends on Working Egress, Not Cached State",
        subtitle="A working proxy path refreshes the connected catalog and advances its timestamp; an unreachable proxy fails the same refresh cleanly",
        svg_title="Chapter 6 lab flow: a connected online catalog refreshed manually and its effect confirmed on a dependent baseline, tested against an intentionally unreachable proxy",
        svg_desc="Direct reachability to Dell's download host is confirmed independently, then a connected "
                  "catalog's manual refresh job is triggered and polled to completion, advancing its "
                  "last-refreshed timestamp past its previously recorded value. Re-running compliance evaluation "
                  "on the Chapter 5 baseline completes without error, referencing the newly refreshed catalog "
                  "content. As a negative test, the appliance's proxy is deliberately pointed at an unreachable "
                  "reserved address and another catalog refresh is attempted; the refresh job fails with a "
                  "connectivity-related error, confirming catalog refresh genuinely depends on working egress "
                  "rather than succeeding from cached state. Restoring the correct proxy configuration lets a "
                  "subsequent refresh succeed again.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Direct reachability confirmed", 12.5, 700, "#111827"),
        Line("RefreshCatalog job", 10.5, 400, "#374151"),
        Line("→ last-refreshed timestamp advances", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Compliance re-evaluation", 12.5, 700, "#111827"),
        Line("against refreshed catalog", 10.5, 400, "#374151"),
        Line("→ completes without error", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("proxy → unreachable 192.0.2.1", 10.5, 700, "#7f1d1d"),
        Line("refresh job → connectivity error", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("restoring the correct proxy configuration lets a subsequent refresh succeed again, confirming the", 11.5, 400, "#374151"),
        Line("failure was specific to the broken egress path, not a lingering appliance-side fault.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Working egress path"), ("alt", "Downstream compliance re-eval"), ("warn", "Broken egress path")])
    c.save(f"{OUT}/chapter-06-connected-catalog-refresh-flow.svg")


def ch07():
    c = Canvas(960, 600,
        title="Chapter 7 Hands-On Lab: A Tampered Package Is Caught by Checksum Verification Before It Ever Reaches OME",
        subtitle="A synthetic offline export is hashed, transferred, hosted, and registered cleanly; a single corrupted byte is caught before continuing",
        svg_title="Chapter 7 lab flow: a synthetic offline catalog export verified by checksum, hosted over HTTP, and registered as a custom catalog, tested against a deliberately corrupted package file",
        svg_desc="A minimal synthetic catalog directory stands in for a real DRM export; a sha256 manifest is "
                  "generated and verified, with every file reporting OK. The verified export is hosted over HTTP "
                  "from the lab host, confirmed reachable from the appliance's network, and registered in OME as "
                  "a custom catalog. As a negative test, one package file is deliberately corrupted after the "
                  "manifest was generated, and re-verification against the same manifest reports a FAILED entry "
                  "for exactly that file, confirming the integrity check detects transfer corruption or "
                  "tampering before the export is ever hosted or registered. The file is restored before "
                  "continuing to the hosting and registration steps.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Synthetic DRM export", 12.5, 700, "#111827"),
        Line("sha256sum manifest generated", 10.5, 400, "#374151"),
        Line("sha256sum -c → all OK", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Hosted via http.server", 12.5, 700, "#111827"),
        Line("registered as custom catalog", 10.5, 400, "#374151"),
        Line("lab-offline-catalog confirmed", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("package file tampered", 10.5, 700, "#7f1d1d"),
        Line("sha256sum -c → FAILED", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("the manifest check runs before hosting or registration in the actual lab sequence — tampering is", 11.5, 400, "#374151"),
        Line("caught at the transfer-integrity step, not discovered later inside OME's catalog processing.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Verified export"), ("alt", "Hosted + registered catalog"), ("warn", "Detected tampering")])
    c.save(f"{OUT}/chapter-07-offline-catalog-integrity-flow.svg")


def ch08():
    c = Canvas(960, 580,
        title="Chapter 8 Hands-On Lab: A Pruned Attribute Is Excluded From Drift Reporting, Not Just Hidden in the UI",
        subtitle="A captured template's device-unique attribute is marked ignored, and compliance evaluation confirms it stops being reported as drift",
        svg_title="Chapter 8 lab flow: a configuration template captured from a reference device, pruned of one device-unique attribute, and evaluated for compliance, tested against a nonexistent template ID",
        svg_desc="A configuration template is captured from a reference device and polled to completion; a "
                  "device-unique attribute, such as a static iDRAC network setting, is identified and marked "
                  "IsIgnored. Configuration compliance evaluation against the Chapter 3 device group confirms "
                  "the pruned attribute no longer appears as a source of reported drift for any device, while "
                  "other, non-pruned attributes continue to be evaluated normally. As a negative test, compliance "
                  "evaluation is triggered against a template ID that does not exist; the API returns an HTTP "
                  "4xx error, confirming the endpoint rejects evaluation against a nonexistent template rather "
                  "than silently succeeding. No device configuration is changed at any point, since the lab uses "
                  "compliance-only evaluation rather than deployment.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("Template captured + pruned", 12.5, 700, "#111827"),
        Line("device-unique attribute", 10.5, 400, "#374151"),
        Line("IsIgnored = true", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("CheckConfigurationCompliance", 12.5, 700, "#111827"),
        Line("pruned attribute excluded", 10.5, 700, "#14532d"),
        Line("from drift reporting", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("compliance eval against", 10.5, 700, "#7f1d1d"),
        Line("template 999999", 10.5, 700, "#7f1d1d"),
        Line("→ HTTP 4xx", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("no device configuration is changed at any point in this lab — compliance-only evaluation reports", 11.5, 400, "#374151"),
        Line("drift without deploying anything, confirmed by the reference device's configuration being unchanged.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Template capture + prune"), ("alt", "Filtered compliance eval"), ("warn", "Rejected nonexistent template")])
    c.save(f"{OUT}/chapter-08-template-compliance-prune-flow.svg")


def ch09():
    c = Canvas(960, 640,
        title="Chapter 9 Hands-On Lab: The Capstone — a Before/After Snapshot Diff Shows Only the Expected Changes",
        subtitle="A validated backup destination, a scripted cross-chapter operational sequence, and a snapshot diff confirming nothing unexpected moved",
        svg_title="Chapter 9 capstone lab flow: an on-demand backup to a validated NFS share, a pre/post-change operational snapshot diff across the volume's earlier chapters, tested against an invalid password",
        svg_desc="An NFS share is configured and validated as the appliance's backup destination, and an "
                  "on-demand backup completes with a backup file appearing on the share. A pre-change snapshot "
                  "script captures the appliance's operational state, after which a representative cross-chapter "
                  "sequence is exercised: an inventory refresh, an alert-log check, and where hardware allows, a "
                  "firmware compliance re-evaluation. A post-change snapshot is captured and diffed against the "
                  "pre-change one, showing only the changes attributable to the operations just performed, with "
                  "no unexplained changes in device health counts. As a negative test, the same snapshot script "
                  "is run with an intentionally invalid password; it fails with an HTTP error from the session "
                  "endpoint, consistent with Chapter 1's original bootstrap validation, confirming this final "
                  "capstone script depends on the same authentication discipline established at the very start "
                  "of the volume.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Validated NFS backup share", 12.5, 700, "#111827"),
        Line("on-demand backup completes", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 110, "mgmt", [
        Line("pre-change-snapshot.json", 12.5, 700, "#111827"),
        Line("captured before operations", 10.5, 400, "#374151"),
    ])
    c.connector(300, 185, 360, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("post-change diff", 12.5, 700, "#111827"),
        Line("only expected changes", 10.5, 700, "#14532d"),
        Line("appear, nothing else", 10.5, 400, "#374151"),
    ])
    c.connector(600, 185, 700, 185, "alt")
    c.node_box(360, 300, 400, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("snapshot script, wrong password", 10.5, 700, "#7f1d1d"),
        Line("→ session HTTP error (as in Ch. 1)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(480, 240, 480, 300, "warn")
    c.node_box(60, 460, 860, 90, "neutral", [
        Line("the capstone's snapshot script fails on invalid credentials exactly like Chapter 1's original", 11.5, 400, "#374151"),
        Line("bootstrap check — the same authentication discipline holds from the first lab to the last.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Backup + baseline snapshot"), ("alt", "Diffed operational sequence"), ("warn", "Rejected invalid credentials")])
    c.save(f"{OUT}/chapter-09-capstone-backup-snapshot-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
