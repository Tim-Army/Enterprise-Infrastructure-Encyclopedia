import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-09-infrastructure-automation"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Hands-On Lab: A Branch-Protected Lint Gate That Mechanically Blocks a Bad Commit",
        subtitle="An unformatted-HCL pull request fails terraform-fmt in CI and cannot be merged until fixed",
        svg_title="Chapter 1 lab flow: a repository skeleton with branch protection and a CI lint gate blocking a non-conforming pull request",
        svg_desc="A baseline repository skeleton (modules/, environments/, .github/workflows/lint.yml) is pushed "
                  "to GitHub with branch protection on main requiring a pull request and passing terraform-fmt / "
                  "ansible-lint status checks. As a negative test, a feature branch deliberately introduces "
                  "unformatted HCL and opens a pull request; the terraform-fmt check fails and the merge button is "
                  "disabled by branch protection, proving a non-conforming change is mechanically blocked rather "
                  "than relying on manual review diligence. Running terraform fmt -recursive locally, committing "
                  "the fix, and pushing again turns the check green and allows the merge.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Repository skeleton", 12.5, 700, "#111827"),
        Line("branch protection on main", 10.5, 400, "#374151"),
        Line("required: terraform-fmt, ansible-lint", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 130, 240, 110, "warn", [
        Line("PR: lab/negative-test", 12.5, 700, "#111827"),
        Line("unformatted HCL committed", 10.5, 700, "#7f1d1d"),
        Line("terraform-fmt check: FAIL", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(300, 185, 380, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Fixed + re-pushed", 12.5, 700, "#111827"),
        Line("terraform fmt -recursive", 10.5, 400, "#374151"),
        Line("check: PASS, merge allowed", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 185, 700, 185, "warn")
    c.node_box(60, 330, 860, 100, "warn", [
        Line("Negative Test (this is the lab's actual test)", 12.5, 700, "#7f1d1d"),
        Line("merge button stays disabled while terraform-fmt is failing — branch protection enforces the gate mechanically", 11, 400, "#7f1d1d"),
        Line("no reliance on a reviewer noticing the formatting issue by hand", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 470, [("mgmt", "Protected branch"), ("warn", "Blocked PR"), ("alt", "Fixed, merge allowed")])
    c.save(f"{OUT}/chapter-01-branch-protection-lint-gate-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: A moved Block Refactor and a Provider's Drift-Detection Blind Spot",
        subtitle="Renaming a resource in place produces a zero-change plan; local_file never notices its own file being hand-edited",
        svg_title="Chapter 2 lab flow: a Terraform module refactored in place with a moved block, then a local_file provider's drift-detection limits",
        svg_desc="A cloud-credential-free module (random and local providers only) creates one random_pet and one "
                  "local_file. terraform test runs a plan-level assertion that passes. A moved block renames the "
                  "resource address; terraform plan afterward reports 0 to add, 0 to change, 0 to destroy, "
                  "confirming the resource was renamed in place rather than replaced. As a negative test, the "
                  "generated output file's contents are edited by hand outside Terraform; terraform plan reports "
                  "no diff at all, because local_file only tracks that it manages the file's existence and "
                  "declared content in state, not out-of-band edits — a concrete demonstration that not every "
                  "provider detects every kind of drift.")
    c.node_box(60, 130, 240, 110, "mgmt", [
        Line("Module apply", 12.5, 700, "#111827"),
        Line("random_pet + local_file", 10.5, 400, "#374151"),
        Line("terraform test: PASS", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 130, 240, 110, "alt", [
        Line("moved block refactor", 12.5, 700, "#111827"),
        Line("resource renamed in place", 10.5, 400, "#374151"),
        Line("plan: 0 add / 0 change / 0 destroy", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 185, 380, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("output file hand-edited", 10.5, 700, "#7f1d1d"),
        Line("terraform plan: no diff!", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 185, 700, 185, "warn")
    c.node_box(60, 330, 860, 100, "neutral", [
        Line("local_file tracks only the fact that it manages a file's existence and declared content in state,", 11.5, 400, "#374151"),
        Line("not the actual on-disk bytes — a specific provider's drift-detection behavior must be understood before relying on it.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("mgmt", "Baseline apply"), ("alt", "Safe in-place refactor"), ("warn", "Undetected drift (negative test)")])
    c.save(f"{OUT}/chapter-02-moved-block-drift-blindspot-flow.svg")


def ch03():
    c = Canvas(960, 560,
        title="Chapter 3 Hands-On Lab: Ansible Idempotency Proven, Then Deliberately Broken",
        subtitle="A template task converges to changed=0 on the second run; a raw shell append never does",
        svg_title="Chapter 3 lab flow: an idempotent Ansible role converging to no-change, contrasted with a non-idempotent shell task",
        svg_desc="The motd role deploys /tmp/ansible-lab-motd via the template module. The first playbook run "
                  "reports changed=1; the second run reports changed=0 across all tasks, the idempotency contract "
                  "holding. As a negative test, a raw ansible.builtin.shell task appending a timestamp is added to "
                  "the same role; its first run reports changed=1 as expected, but the second run also reports "
                  "changed=1 again — idempotency broken, because a raw shell/command task has no built-in concept "
                  "of desired state and needs an explicit creates, removes, or when guard before it belongs in a "
                  "convergence-oriented playbook.")
    c.node_box(60, 140, 260, 120, "mgmt", [
        Line("motd role (template task)", 12.5, 700, "#111827"),
        Line("run 1: changed=1", 10.5, 400, "#374151"),
        Line("run 2: changed=0", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 200, 380, 200, "mgmt")
    c.node_box(380, 140, 260, 120, "warn", [
        Line("+ shell append (negative test)", 12, 700, "#111827"),
        Line("run 1: changed=1", 10.5, 400, "#7f1d1d"),
        Line("run 2: changed=1 again", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(680, 140, 240, 120, "neutral", [
        Line("Why it breaks", 12.5, 700, "#111827"),
        Line("raw shell has no desired-state", 10.5, 400, "#374151"),
        Line("needs creates/removes/when guard", 10.5, 400, "#374151"),
    ])
    c.connector(640, 200, 680, 200, "warn")
    c.legend(60, 380, [("mgmt", "Idempotent task"), ("warn", "Non-idempotent task (negative test)")])
    c.save(f"{OUT}/chapter-03-ansible-idempotency-broken-flow.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: Webhook Signature Verification, Replay Deduplication, and Tamper Detection",
        subtitle="A duplicate event is acknowledged without reprocessing; a tampered body with the original signature is rejected",
        svg_title="Chapter 4 lab flow: a local webhook receiver enforcing HMAC signature verification and idempotency-key deduplication",
        svg_desc="A local HTTP receiver validates an HMAC-SHA256 signature over the raw request body. A correctly "
                  "signed event (evt-001) is accepted with HTTP 200 and processed once. The identical request "
                  "replayed a second time returns HTTP 200 'duplicate event acknowledged' without a second "
                  "processing log line, proving the idempotency-key check suppressed the duplicate. As a negative "
                  "test, a request with a tampered body but the original (now-mismatched) signature returns HTTP "
                  "401 'invalid signature' — the receiver correctly rejects a payload that does not match the "
                  "signature computed over the original body, even though the signature header itself was once a "
                  "real, valid value.")
    c.node_box(60, 140, 240, 110, "alt", [
        Line("Signed event (evt-001)", 12.5, 700, "#111827"),
        Line("valid HMAC-SHA256", 10.5, 400, "#374151"),
        Line("200 accepted, processed once", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 140, 240, 110, "mgmt", [
        Line("Same event replayed", 12.5, 700, "#111827"),
        Line("identical signature + body", 10.5, 400, "#374151"),
        Line("200 duplicate acknowledged", 10.5, 700, "#1d4ed8"),
    ])
    c.connector(300, 195, 380, 195, "alt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("tampered body, original sig", 10.5, 700, "#7f1d1d"),
        Line("401 invalid signature", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 90, "neutral", [
        Line("dedup check prevents double-processing of legitimate retries; signature check rejects any payload that doesn't", 11.5, 400, "#374151"),
        Line("match its signature, even a once-valid header value replayed against different content.", 11.5, 400, "#374151"),
    ])
    c.legend(60, 460, [("alt", "Valid, processed once"), ("mgmt", "Deduplicated replay"), ("warn", "Tampered (rejected)")])
    c.save(f"{OUT}/chapter-04-webhook-signature-dedup-flow.svg")


def ch05():
    c = Canvas(960, 620,
        title="Chapter 5 Hands-On Lab: A Conftest Policy Gate That Must Be Blocking, Not Advisory",
        subtitle="Bypassing a failed policy check and applying anyway produces exactly the noncompliant output the check predicted",
        svg_title="Chapter 5 lab flow: a Terraform plan evaluated by Conftest before apply, with a deliberate bypass showing why the gate must block",
        svg_desc="A minimal Terraform configuration writes an owner tag into a local file. Planning with no "
                  "owner_tag and evaluating with Conftest fails: 'has an empty owner_tag'. Re-planning with "
                  "owner_tag=platform-team and re-evaluating passes cleanly. As a negative test, the failing "
                  "plan from the first step is applied anyway, bypassing the policy gate entirely; the resulting "
                  "output file shows owner= with no value, exactly what the policy predicted — demonstrating that "
                  "nothing at the terraform apply layer itself prevents applying a plan that failed policy, which "
                  "is why the check must be a required, blocking CI step and not an advisory one a human can "
                  "choose to ignore.")
    c.node_box(60, 130, 240, 110, "warn", [
        Line("plan: no owner_tag", 12.5, 700, "#111827"),
        Line("conftest test: FAIL", 10.5, 700, "#7f1d1d"),
        Line("\"has an empty owner_tag\"", 10.5, 400, "#7f1d1d"),
    ])
    c.node_box(380, 130, 240, 110, "alt", [
        Line("plan: owner_tag=platform-team", 12, 700, "#111827"),
        Line("conftest test: PASS", 10.5, 700, "#14532d"),
    ])
    c.node_box(700, 130, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("terraform apply plan.tfout anyway", 10.5, 700, "#7f1d1d"),
        Line("(bypassing the failed gate)", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(300, 185, 380, 185, "warn")
    c.connector(300, 240, 700, 240, "warn", label="apply the FAILED plan directly")
    c.node_box(60, 330, 860, 110, "warn", [
        Line("Result", 12.5, 700, "#7f1d1d"),
        Line("output-*.txt shows \"owner=\" with no value — exactly what the policy predicted", 11, 400, "#7f1d1d"),
        Line("nothing at the apply layer itself blocks a plan that failed policy — the gate must be a required,", 11, 400, "#7f1d1d"),
        Line("blocking CI step, not an advisory one a human can choose to ignore", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("warn", "Failing / bypassed path"), ("alt", "Corrected, passing path")])
    c.save(f"{OUT}/chapter-05-conftest-policy-gate-bypass-flow.svg")


def ch06():
    c = Canvas(960, 620,
        title="Chapter 6 Hands-On Lab: Vault AppRole Scoped to Read-Only, Enforced Against a Write Attempt",
        subtitle="The ci-pipeline token reads the secret from both the CLI and an Ansible lookup, but cannot write to it",
        svg_title="Chapter 6 lab flow: a Vault AppRole-issued, read-only-scoped token used by both a CLI login flow and an Ansible lookup",
        svg_desc="Vault dev mode seeds secret/pipeline/db_password. An AppRole role ci-pipeline is bound to a "
                  "pipeline-read policy granting only read on secret/data/pipeline/*, with a 10-minute token TTL. "
                  "The issued token reads the secret successfully both via the Vault CLI and via an Ansible "
                  "community.hashi_vault lookup task (with no_log: true keeping the value out of task output). As "
                  "a negative test, the same scoped token attempts a write to the same secret path; Vault returns "
                  "'permission denied', proving the read-only policy is enforced by Vault itself, not merely by "
                  "convention.")
    c.node_box(370, 110, 220, 90, "neutral", [
        Line("Vault dev mode", 13, 700, "#111827"),
        Line("secret/pipeline/db_password", 10.5, 400, "#374151"),
    ])
    c.connector(480, 200, 480, 240, "neutral", label="AppRole login")
    c.node_box(370, 240, 220, 90, "mgmt", [
        Line("ci-pipeline AppRole", 12.5, 700, "#111827"),
        Line("policy: pipeline-read (read only)", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(80, 380, 260, 100, "alt", [
        Line("CLI: vault kv get", 12.5, 700, "#111827"),
        Line("returns value successfully", 10.5, 700, "#14532d"),
    ])
    c.node_box(620, 380, 260, 100, "alt", [
        Line("Ansible hashi_vault lookup", 12.5, 700, "#111827"),
        Line("assertion passes, no_log: true", 10.5, 700, "#14532d"),
    ])
    c.connector(400, 330, 210, 380, "alt")
    c.connector(560, 330, 750, 380, "alt")
    c.node_box(80, 510, 800, 90, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("same ci-pipeline token: vault kv put (write) → \"permission denied\"", 11, 400, "#7f1d1d"),
        Line("Vault itself enforces the read-only policy boundary, not merely convention", 11, 400, "#7f1d1d"),
    ])
    c.legend(80, 460, [("neutral", "Secret store"), ("mgmt", "Scoped token issuance"), ("alt", "Permitted reads")])
    c.save(f"{OUT}/chapter-06-vault-approle-readonly-flow.svg")


def ch07():
    c = Canvas(960, 580,
        title="Chapter 7 Hands-On Lab: Event-Driven Ansible with a Self-Produced-Event Loop Guard",
        subtitle="A monitoring-sourced alert triggers the rulebook; an automation-sourced alert is correctly ignored",
        svg_title="Chapter 7 lab flow: an Ansible EDA rulebook reacting to a webhook alert, with a guard preventing it from reacting to its own output",
        svg_desc="ansible-rulebook listens on a local webhook for HighCPU/firing alerts. A matching event with "
                  "source=monitoring triggers the rule, running scale_out.yml and appending a log line recording "
                  "the trigger. As a negative test, an otherwise identical event tagged source=automation (as if "
                  "produced by the automation's own action) is sent; the rulebook receives it but the rule's "
                  "condition (event.payload.source != \"automation\") does not match, so no playbook runs and no "
                  "log line is appended — proving the guard actually prevents a feedback loop rather than merely "
                  "documenting the intent to prevent one.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("Webhook event", 12.5, 700, "#111827"),
        Line("HighCPU/firing, source=monitoring", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 260, 110, "alt", [
        Line("ansible-rulebook", 12.5, 700, "#111827"),
        Line("condition matches (source ≠ automation)", 10.5, 400, "#374151"),
        Line("→ runs scale_out.yml", 10.5, 700, "#14532d"),
    ])
    c.connector(320, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Action taken", 12.5, 700, "#111827"),
        Line("log: \"Scale-out triggered", 10.5, 400, "#374151"),
        Line("by alert on web01\"", 10.5, 400, "#374151"),
    ])
    c.connector(640, 195, 700, 195, "alt")
    c.node_box(60, 330, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("identical event but source=automation (as if self-produced by the automation's own action)", 11, 400, "#7f1d1d"),
        Line("rulebook receives it, but condition source != \"automation\" does not match — rule does not fire", 11, 400, "#7f1d1d"),
        Line("no playbook run, no new log line — the loop-breaking guard is actually enforced, not just documented", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Incoming event"), ("alt", "Matched, actioned"), ("warn", "Guarded, ignored")])
    c.save(f"{OUT}/chapter-07-eda-rulebook-loop-guard-flow.svg")


def ch08():
    c = Canvas(960, 580,
        title="Chapter 8 Hands-On Lab: Signed Module Archive Verified, Then Invalidated by a One-Line Tamper",
        subtitle="cosign verify-blob passes against the untouched archive and fails the instant a byte is appended",
        svg_title="Chapter 8 lab flow: a Terraform module scanned with Checkov, packaged, and cosign-signed, then verified against a tampered archive",
        svg_desc="Checkov scans the demo module for misconfigurations, reporting a clean or low-severity summary. "
                  "The module is packaged into demo-module.tar.gz and signed with cosign sign-blob using a local "
                  "key pair, producing demo-module.tar.gz.sig. cosign verify-blob against the untouched archive "
                  "prints 'Verified OK'. As a negative test, one line is appended to the archive after signing; "
                  "re-running cosign verify-blob against the same signature now fails with a signature mismatch "
                  "error, proving that even a one-line append invalidates the signature and that consuming this "
                  "artifact without verification would have gone undetected.")
    c.node_box(60, 140, 220, 100, "neutral", [
        Line("Checkov scan", 12.5, 700, "#111827"),
        Line("modules/demo", 10.5, 400, "#374151"),
        Line("clean / low-severity summary", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 140, 240, 100, "mgmt", [
        Line("Package + sign", 12.5, 700, "#111827"),
        Line("demo-module.tar.gz", 10.5, 400, "#374151"),
        Line("cosign sign-blob (key pair)", 10.5, 400, "#374151"),
    ])
    c.connector(280, 190, 360, 190, "neutral")
    c.node_box(680, 140, 220, 100, "alt", [
        Line("verify-blob", 12.5, 700, "#111827"),
        Line("untouched archive", 10.5, 400, "#374151"),
        Line("\"Verified OK\"", 10.5, 700, "#14532d"),
    ])
    c.connector(600, 190, 680, 190, "alt")
    c.node_box(60, 330, 860, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("one line appended to demo-module.tar.gz after signing (echo \"tampered\" >> archive)", 11, 400, "#7f1d1d"),
        Line("verify-blob against the same .sig now fails with a signature-mismatch error", 11, 400, "#7f1d1d"),
        Line("even a one-line append invalidates the signature — undetected tampering without verification", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("neutral", "Pre-package scan"), ("mgmt", "Signed artifact"), ("alt", "Verified untampered")])
    c.save(f"{OUT}/chapter-08-checkov-cosign-tamper-flow.svg")


def ch09():
    c = Canvas(960, 600,
        title="Chapter 9 Hands-On Lab: A Success-Rate Metric That Correctly Captures a Failed Run",
        subtitle="Three clean applies report 3/3; a deliberately broken fourth run drops the rate to 3/4 instead of vanishing",
        svg_title="Chapter 9 lab flow: structured JSON logging around Terraform apply, a computed success-rate metric, and a Vault backup drill",
        svg_desc="apply-with-log.sh wraps terraform apply, recording run_id, duration, exit_status, and timestamp "
                  "as one JSON line per run in apply-runs.jsonl. Three successful runs produce a computed success "
                  "rate of 3/3. Separately, a Vault dev-mode backup-and-restore drill seeds a marker secret to "
                  "prove a backup is actually usable, not merely present. As a negative test, a deliberately "
                  "broken resource (negative length) is added and the wrapper run a fourth time; the run log "
                  "gains a fourth entry with a non-zero exit_status, and the recomputed success rate correctly "
                  "drops to 3/4 — proving the instrumentation captures failures as data instead of only recording "
                  "successful runs.")
    c.node_box(60, 140, 260, 110, "mgmt", [
        Line("apply-with-log.sh x3", 12.5, 700, "#111827"),
        Line("apply-runs.jsonl: 3 lines", 10.5, 400, "#374151"),
        Line("Success rate: 3/3", 10.5, 700, "#14532d"),
    ])
    c.node_box(380, 140, 240, 110, "neutral", [
        Line("Vault backup drill", 12.5, 700, "#111827"),
        Line("kv put marker → kv get", 10.5, 400, "#374151"),
        Line("confirms backup is usable", 10.5, 400, "#374151"),
    ])
    c.connector(320, 195, 380, 195, "mgmt")
    c.node_box(700, 140, 220, 110, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("broken resource added", 10.5, 700, "#7f1d1d"),
        Line("4th run: non-zero exit_status", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(620, 195, 700, 195, "warn")
    c.node_box(60, 330, 860, 110, "warn", [
        Line("Result", 12.5, 700, "#7f1d1d"),
        Line("apply-runs.jsonl now has 4 entries; the 4th shows a non-zero exit_status, not a missing entry", 11, 400, "#7f1d1d"),
        Line("recomputed success rate correctly drops to 3/4 — failures are captured as data, not silently dropped", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Successful, logged runs"), ("neutral", "Backup drill"), ("warn", "Failed run (captured, not lost)")])
    c.save(f"{OUT}/chapter-09-structured-logging-success-rate-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
