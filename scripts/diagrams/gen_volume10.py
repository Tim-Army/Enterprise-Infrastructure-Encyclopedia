import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-10-enterprise-cybersecurity"


def ch01():
    c = Canvas(960, 580,
        title="Chapter 1 Hands-On Lab: Risk-Register Scoring with a Data-Quality Guard",
        subtitle="Residual scores rank correctly by control effectiveness; an unowned risk blocks the report from ever printing",
        svg_title="Chapter 1 lab flow: computing ranked residual risk scores from a register, guarded by an ownership validation check",
        svg_desc="compute_risk.py ranks three sample risks by residual score: RISK-0144 (no mapped controls) "
                  "shows a residual score equal to its inherent score, while RISK-0142 (two mapped controls) "
                  "shows a materially reduced residual score. As a negative test, a validate() guard is patched in "
                  "ahead of main() to require every risk have an assigned owner; re-running against the "
                  "unmodified register exits with 'VALIDATION FAILED: RISK-0144 has no owner' and a nonzero exit "
                  "code, blocking the ranked report from printing at all until the governance gap is fixed. "
                  "Assigning an owner and re-running restores the full ranked output.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("risk_register.csv", 12.5, 700, "#111827"),
        Line("3 risks, likelihood × impact", 10.5, 400, "#374151"),
        Line("RISK-0144: no owner, no controls", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("compute_risk.py", 12.5, 700, "#111827"),
        Line("ranked residual scores", 10.5, 400, "#374151"),
        Line("RISK-0144 = inherent (no controls)", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("validate() guard added", 10.5, 700, "#7f1d1d"),
        Line("VALIDATION FAILED, exit 1", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 340, 860, 100, "neutral", [
        Line("RISK-0144 has no owner — the ranked report never prints until an owner is assigned and the script re-run", 11.5, 400, "#374151"),
        Line("confirming the governance rule that every risk must be assigned is mechanically enforced, not advisory.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 480, [("mgmt", "Register input"), ("alt", "Ranked, valid output"), ("warn", "Blocked by ownership guard")])
    c.save(f"{OUT}/chapter-01-risk-register-ownership-guard-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: Just-In-Time Privileged Elevation, Auto-Expiring and Policy-Guarded",
        subtitle="A 60-minute grant auto-expires with no manual revocation; missing justification and over-duration requests are rejected before issuance",
        svg_title="Chapter 2 lab flow: a just-in-time privileged elevation workflow that expires automatically and rejects policy-violating requests",
        svg_desc="request_elevation grants alice@corp.example the db-admin role for 60 minutes with a ticket "
                  "justification; the grant shows active=True immediately, and active=False once 61 minutes have "
                  "elapsed, confirming automatic expiry with no manual revocation step. As a negative test, a "
                  "request with no justification raises 'Elevation requests require a justification (ticket "
                  "reference)', and a separate request for a 600-minute duration raises 'Elevation duration "
                  "exceeds policy maximum of 8 hours' — both failures occur before any credential is ever issued.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("request_elevation()", 12.5, 700, "#111827"),
        Line("alice, db-admin, 60 min", 10.5, 400, "#374151"),
        Line("active=True immediately", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("After 61 minutes", 12.5, 700, "#111827"),
        Line("active=False", 10.5, 700, "#14532d"),
        Line("auto-expired, no manual revoke", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("no justification → ValueError", 10.5, 700, "#7f1d1d"),
        Line("600 min → exceeds 8h max", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 340, 860, 90, "neutral", [
        Line("both policy-violating requests are rejected by the policy engine before any credential is ever issued —", 11.5, 400, "#374151"),
        Line("the elevation never reaches an active state for a request that never should have been granted.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 470, [("mgmt", "Compliant grant"), ("alt", "Auto-expiry"), ("warn", "Rejected before issuance")])
    c.save(f"{OUT}/chapter-02-jit-elevation-policy-guard-flow.svg")


def ch03():
    c = Canvas(960, 600,
        title="Chapter 3 Hands-On Lab: SSH Hardening That Rejects Password Auth at the Protocol Level",
        subtitle="Key-based access succeeds; an explicit password-authentication attempt is refused before any prompt appears",
        svg_title="Chapter 3 lab topology: an SSH hardening baseline validated by a successful key-based login and a rejected password login",
        svg_desc="A hardening drop-in (PermitRootLogin no, PasswordAuthentication no, MaxAuthTries 4, and more) "
                  "is applied to sshd and reloaded; sshd -T confirms the settings are active. From a second host, "
                  "key-based access succeeds normally. As a negative test, an explicit password-authentication "
                  "attempt is refused with 'Permission denied (publickey)' — rejected at the protocol level rather "
                  "than prompting for a password — confirming the hardening control is enforced. SELinux is "
                  "confirmed Enforcing, and an OpenSCAP CIS evaluation independently marks the SSH-related rules "
                  "as passing.")
    c.node_box(60, 150, 220, 110, "mgmt", [
        Line("Second host", 13, 700, "#111827"),
        Line("ssh -o PreferredAuthentications=publickey", 10, 400, "#374151"),
    ])
    c.node_box(380, 130, 240, 150, "alt", [
        Line("Lab host — sshd hardened", 12.5, 700, "#111827"),
        Line("PasswordAuthentication no", 10.5, 700, "#1d4ed8"),
        Line("PermitRootLogin no", 10.5, 400, "#374151"),
        Line("SELinux: Enforcing", 10.5, 700, "#14532d"),
        Line("OpenSCAP CIS: sshd rules pass", 10, 400, "#374151"),
    ])
    c.connector(280, 200, 380, 200, "alt", label="pubkey auth: succeeds")
    c.node_box(700, 150, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("password auth attempt", 10.5, 700, "#7f1d1d"),
        Line("\"Permission denied (publickey)\"", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 200, 700, 200, "warn", label="password auth: refused")
    c.node_box(60, 340, 860, 90, "neutral", [
        Line("rejected at the protocol level, not with a password prompt — confirming PasswordAuthentication no is enforced,", 11.5, 400, "#374151"),
        Line("not merely configured.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 470, [("mgmt", "Client"), ("alt", "Hardened server state"), ("warn", "Rejected auth method")])
    c.save(f"{OUT}/chapter-03-ssh-hardening-pubkey-only-topology.svg")


def ch04():
    c = Canvas(960, 660,
        title="Chapter 4 Hands-On Lab: nftables Host Segmentation and a CI Policy Validator",
        subtitle="Only SSH and HTTPS pass; every other port is dropped and logged, and a missing default-deny rule fails CI",
        svg_title="Chapter 4 lab topology: an nftables default-drop segmentation policy validated by permitted and denied connectivity, plus a CI policy check",
        svg_desc="lab-segmentation.nft implements a default-drop inbound chain allowing only established/related "
                  "traffic, loopback, TCP 22, and TCP 443, logging every other drop with prefix SEG-DENY. From a "
                  "second host, a request to the permitted port 443 succeeds. As a negative test, a request to an "
                  "unlisted port (8080) times out or is refused, and dmesg shows the SEG-DENY log entry, "
                  "confirming both enforcement and the audit trail. Separately, validate_segmentation.py passes "
                  "cleanly against a compliant policy.yaml but fails with 'no explicit default-deny egress rule' "
                  "and a nonzero exit against a broken-policy.yaml missing that rule — the same fail-closed CI "
                  "gate pattern used for the OSCAP remediation review.")
    c.node_box(60, 140, 220, 100, "mgmt", [
        Line("Second host", 13, 700, "#111827"),
        Line("curl :443 and :8080", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 110, 240, 160, "alt", [
        Line("lab VM — nftables", 13, 700, "#111827"),
        Line("policy drop (default)", 10.5, 400, "#374151"),
        Line("accept: 22/tcp, 443/tcp", 10.5, 700, "#14532d"),
        Line("drop + log SEG-DENY: else", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(280, 175, 370, 175, "alt", label="443: 200 OK")
    c.connector(280, 210, 370, 245, "warn", label="8080: blocked + SEG-DENY logged")
    c.node_box(700, 140, 220, 100, "neutral", [
        Line("dmesg | grep SEG-DENY", 12, 700, "#111827"),
        Line("logged drop confirms audit trail", 10.5, 400, "#374151"),
    ])
    c.connector(610, 220, 700, 190, "warn")
    c.node_box(80, 350, 800, 110, "warn", [
        Line("CI Policy Validator (negative test)", 12.5, 700, "#111827"),
        Line("policy.yaml (default-deny egress present) → validate_segmentation.py: PASS, exit 0", 11, 400, "#14532d"),
        Line("broken-policy.yaml (default-deny egress removed) → \"POLICY ERROR: no explicit default-deny", 11, 400, "#7f1d1d"),
        Line("egress rule\", exit 1 — caught before it would reach production", 11, 400, "#7f1d1d"),
    ])
    c.legend(80, 610, [("mgmt", "Test client"), ("alt", "Permitted path"), ("warn", "Denied path / CI catch")])
    c.save(f"{OUT}/chapter-04-nftables-segmentation-ci-validator-topology.svg")


def ch05():
    c = Canvas(960, 600,
        title="Chapter 5 Hands-On Lab: Risk-Based Vulnerability Prioritization That Inverts Raw CVSS Ranking",
        subtitle="A KEV-listed 7.5 outranks an unexploited 9.8; an overdue KEV finding blocks the ranked report from printing",
        svg_title="Chapter 5 lab flow: CVSS/EPSS/KEV-aware vulnerability prioritization, guarded by a KEV SLA-overdue check",
        svg_desc="prioritize_vulns.py ranks three sample findings: CVE-2025-11001 (CVSS 7.5, but KEV-listed, "
                  "EPSS 0.91, critical asset) ranks first with a 3-day SLA despite having the lowest raw CVSS "
                  "score, while CVE-2025-10877 (CVSS 9.8, EPSS 0.02, not KEV-listed) ranks last with a 30-day "
                  "SLA — demonstrating that risk-based prioritization can invert a raw-severity ordering. As a "
                  "negative test, a check_overdue() guard is patched in ahead of main(); because "
                  "CVE-2025-11001 was discovered 8 days before the check date against a 3-day KEV SLA, the script "
                  "exits with 'OVERDUE: ... exceeding the 3-day KEV SLA' before any ranked output prints. Updating "
                  "the discovery date restores the full ranked report.")
    c.node_box(60, 140, 260, 130, "mgmt", [
        Line("findings.csv (3 CVEs)", 12.5, 700, "#111827"),
        Line("CVE-2025-11001: CVSS 7.5, KEV, EPSS .91", 10, 400, "#374151"),
        Line("CVE-2025-10877: CVSS 9.8, no KEV, EPSS .02", 10, 400, "#374151"),
    ])
    c.node_box(400, 140, 240, 130, "alt", [
        Line("prioritize_vulns.py", 12.5, 700, "#111827"),
        Line("#1: CVE-2025-11001, sla=3d", 10.5, 700, "#14532d"),
        Line("#3: CVE-2025-10877, sla=30d", 10.5, 400, "#374151"),
    ])
    c.connector(320, 205, 400, 205, "mgmt")
    c.node_box(700, 140, 220, 130, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("check_overdue() guard added", 10.5, 700, "#7f1d1d"),
        Line("CVE-2025-11001: 8d > 3d SLA", 10.5, 700, "#7f1d1d"),
        Line("OVERDUE, exit 1", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 205, 700, 205, "warn")
    c.node_box(60, 350, 860, 90, "neutral", [
        Line("the guard raises before any ranked output prints, so an overdue critical finding cannot be silently", 11.5, 400, "#374151"),
        Line("buried in a general report; updating the discovery date and re-running restores the full report.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 480, [("mgmt", "Sample findings"), ("alt", "Risk-ranked output"), ("warn", "SLA-overdue guard (blocks)")])
    c.save(f"{OUT}/chapter-05-vuln-prioritization-sla-guard-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: Credential-Stuffing Detection Tuned Against a Benign Retry Pattern",
        subtitle="Eight tightly clustered failures then a success trigger an alert; the same failures spread over hours do not",
        svg_title="Chapter 6 lab flow: a log-correlation rule detecting a credential-stuffing success pattern, tuned against benign and boundary datasets",
        svg_desc="detect_credential_stuffing.py flags a user with 8 or more authentication failures followed by a "
                  "success within a 15-minute window. Against the sample dataset, bob@corp.example (8 failures "
                  "then a success, all within under a minute) triggers an ALERT; alice@corp.example's single clean "
                  "sign-in does not. As a negative test, a benign dataset with the same user's failures spread "
                  "across hours (a plausible forgotten-password pattern) produces no alert, and trimming the "
                  "malicious dataset to exactly 7 failures (one below the threshold) also produces no alert — "
                  "confirming the rule's tuning correctly distinguishes automated credential stuffing from benign "
                  "retry behavior without over-firing at the threshold boundary.")
    c.node_box(60, 140, 240, 120, "mgmt", [
        Line("bob@corp.example", 12.5, 700, "#111827"),
        Line("8 failures + success, <1 min", 10.5, 400, "#374151"),
        Line("ALERT: credential stuffing", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(380, 140, 240, 120, "alt", [
        Line("alice@corp.example", 12.5, 700, "#111827"),
        Line("single clean sign-in", 10.5, 400, "#374151"),
        Line("no alert", 10.5, 700, "#14532d"),
    ])
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Tests", 12, 700, "#7f1d1d"),
        Line("failures spread over hours", 10.5, 700, "#7f1d1d"),
        Line("or only 7 (below threshold)", 10.5, 700, "#7f1d1d"),
        Line("→ no alert in either case", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 200, 380, 200, "mgmt")
    c.connector(620, 200, 700, 200, "warn")
    c.node_box(60, 360, 860, 90, "neutral", [
        Line("the 15-minute window and 8-failure threshold together distinguish tightly clustered automated attempts", 11.5, 400, "#374151"),
        Line("from widely spaced, plausible human retry behavior — confirmed at the exact tuning boundary.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 490, [("mgmt", "Detected pattern"), ("alt", "Benign, no alert"), ("warn", "Tuned to avoid false positives")])
    c.save(f"{OUT}/chapter-06-credential-stuffing-detection-flow.svg")


def ch07():
    c = Canvas(960, 580,
        title="Chapter 7 Hands-On Lab: Chain-of-Custody Hashing That Detects Post-Collection Tampering",
        subtitle="The unmodified artifact verifies cleanly; a single appended line produces a hash mismatch and a nonzero exit",
        svg_title="Chapter 7 lab flow: a chain-of-custody evidence log recording a SHA-256 baseline hash and detecting subsequent tampering",
        svg_desc="evidence_custody.py logs the initial collection of host-snapshot.txt as evidence EV-2026-0031, "
                  "recording a SHA-256 digest into custody_log.csv. Verifying against the unmodified artifact "
                  "prints 'Integrity verified'. As a negative test, one line is appended to the artifact after "
                  "collection; re-running verify now exits with 'INTEGRITY FAILURE: EV-2026-0031 hash mismatch', "
                  "showing the expected and actual hashes differ, and a nonzero exit code — demonstrating the "
                  "custody log detects post-collection tampering rather than silently accepting a modified "
                  "artifact. Restoring the artifact to its original state confirms verification succeeds again, "
                  "deterministically.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("host-snapshot.txt", 12.5, 700, "#111827"),
        Line("log EV-2026-0031", 10.5, 400, "#374151"),
        Line("SHA-256 baseline recorded", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("verify (unmodified)", 12.5, 700, "#111827"),
        Line("Integrity verified", 10.5, 700, "#14532d"),
        Line("hash matches baseline", 10.5, 400, "#374151"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("line appended post-collection", 10.5, 700, "#7f1d1d"),
        Line("INTEGRITY FAILURE, exit ≠ 0", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("restoring the artifact to its original bytes and re-verifying succeeds again — the hash comparison is", 11.5, 400, "#374151"),
        Line("exact and reproducible, not a one-time check.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Collection + baseline"), ("alt", "Verified, untampered"), ("warn", "Detected tampering")])
    c.save(f"{OUT}/chapter-07-chain-of-custody-tamper-detection-flow.svg")


def ch08():
    c = Canvas(960, 600,
        title="Chapter 8 Hands-On Lab: Envelope Encryption Round-Trip and an AES-GCM Tamper Rejection",
        subtitle="Decryption matches the original exactly; a single flipped ciphertext byte raises InvalidTag before any output is written",
        svg_title="Chapter 8 lab flow: an envelope-encryption round trip verified byte-for-byte, then an authenticated-encryption tamper rejection",
        svg_desc="envelope_encrypt.py encrypts record.txt into record.enc, a JSON envelope carrying data_nonce, "
                  "ciphertext, wrapped_dek, and kek_nonce. Decrypting produces output identical to the original "
                  "(diff shows no output). As a negative test, the ciphertext field is tampered by flipping its "
                  "last character; attempting to decrypt the tampered envelope raises "
                  "cryptography.exceptions.InvalidTag and exits nonzero — AES-GCM's authentication tag detects the "
                  "post-encryption modification and refuses to produce output, rather than silently returning "
                  "corrupted plaintext. No output file is written at all, confirming the failure occurs before any "
                  "potentially corrupted plaintext reaches disk.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("record.txt", 12.5, 700, "#111827"),
        Line("envelope_encrypt.py encrypt", 10.5, 400, "#374151"),
        Line("→ record.enc (DEK wrapped by KEK)", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 110, "alt", [
        Line("decrypt (untampered)", 12.5, 700, "#111827"),
        Line("diff: no output", 10.5, 700, "#14532d"),
        Line("MATCH: round-trip successful", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("ciphertext byte flipped", 10.5, 700, "#7f1d1d"),
        Line("decrypt → InvalidTag, exit ≠ 0", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("no output file is written at all — the authentication tag check fails before any potentially corrupted", 11.5, 400, "#374151"),
        Line("plaintext could reach disk, the same tamper-evidence property Chapter 7's custody hash relies on.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Encrypted envelope"), ("alt", "Verified round trip"), ("warn", "Tamper rejected (AES-GCM tag)")])
    c.save(f"{OUT}/chapter-08-envelope-encryption-tamper-flow.svg")


def ch09():
    c = Canvas(960, 600,
        title="Chapter 9 Hands-On Lab: A Continuous Control-Validation Scorecard That Gates CI/CD Promotion",
        subtitle="Three simulated controls pass cleanly; a reintroduced standing-access regression flips one check and the exit code",
        svg_title="Chapter 9 lab flow: a continuous control-validation scorecard covering segmentation, JIT access, and backup restore, gating on exit code",
        svg_desc="control_validation.py checks three simulated controls — default-deny segmentation, no standing "
                  "privileged access (all grants time-boxed), and a verified backup restore — all printing [PASS], "
                  "with a summary of 3 passed, 0 failed and exit 0. As a negative test, a standing (non-expiring) "
                  "backup-admin grant is added, simulating an emergency-access exception that was never converted "
                  "back to time-boxed JIT access; re-running now shows CTL-002-01 as [FAIL], with the summary "
                  "dropping to 2 passed, 1 failed and exit 1 — exactly the nonzero exit a CI pipeline would use to "
                  "block promotion. Removing the standing grant restores the scorecard to 3 passed, 0 failed.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("control_validation.py", 12.5, 700, "#111827"),
        Line("segmentation, JIT access,", 10.5, 400, "#374151"),
        Line("backup restore — all [PASS]", 10.5, 700, "#14532d"),
    ])
    c.node_box(400, 140, 240, 120, "alt", [
        Line("Baseline scorecard", 12.5, 700, "#111827"),
        Line("3 passed, 0 failed", 10.5, 700, "#14532d"),
        Line("exit 0", 10.5, 400, "#374151"),
    ])
    c.connector(320, 200, 400, 200, "mgmt")
    c.node_box(700, 140, 220, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("standing backup-admin grant", 10.5, 700, "#7f1d1d"),
        Line("CTL-002-01 [FAIL]", 10.5, 700, "#7f1d1d"),
        Line("2 passed, 1 failed — exit 1", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(640, 200, 700, 200, "warn")
    c.node_box(60, 350, 860, 90, "neutral", [
        Line("a CI pipeline consuming this scorecard correctly blocks promotion on the nonzero exit code;", 11.5, 400, "#374151"),
        Line("removing the standing grant restores 3 passed, 0 failed and exit 0.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 480, [("mgmt", "Simulated controls"), ("alt", "Healthy scorecard"), ("warn", "Regression (CI-blocking)")])
    c.save(f"{OUT}/chapter-09-control-validation-scorecard-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
