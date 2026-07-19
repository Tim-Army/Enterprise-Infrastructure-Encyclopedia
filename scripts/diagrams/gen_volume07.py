import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-07-cloud-infrastructure"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Hands-On Lab: Provider-Neutral Tagging Contract Enforced at the Module Boundary",
        subtitle="A local Terraform module validates environment/owner_tag before simulating any resource creation",
        svg_title="Chapter 1 lab flow: a Terraform variable validation contract enforced before a simulated resource is created",
        svg_desc="A fully local Terraform root module (local and random providers only, no cloud account) defines "
                  "a validated environment variable (must be dev/test/stage/prod) and owner_tag. Applying with "
                  "environment=dev and owner_tag=platform-team succeeds, creating a local_file standing in for a "
                  "real cloud resource, stamped with the validated tags. As a negative test, applying with "
                  "environment=production (not in the allowed set) is refused before any resource — simulated or "
                  "real — is touched, with Terraform reporting the exact custom validation error message.")
    c.node_box(60, 130, 260, 110, "mgmt", [
        Line("Input variables", 12.5, 700, "#111827"),
        Line("environment=dev", 10.5, 400, "#374151"),
        Line("owner_tag=platform-team", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 130, 260, 110, "neutral", [
        Line("Validation contract", 12.5, 700, "#111827"),
        Line("variables.tf: validation blocks", 10.5, 400, "#374151"),
        Line("environment ∈ {dev,test,stage,prod}", 10.5, 400, "#374151"),
    ])
    c.connector(320, 185, 380, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("local_file resource", 12.5, 700, "#111827"),
        Line("Apply complete: 2 added", 10.5, 700, "#14532d"),
        Line("tags stamped into JSON", 10.5, 400, "#374151"),
    ])
    c.connector(640, 185, 700, 185, "alt")
    c.node_box(60, 330, 840, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("apply with environment=production (not in the allowed set)", 11, 400, "#7f1d1d"),
        Line("refused before any resource is touched: \"environment must be one of: dev, test, stage, prod.\"", 11, 400, "#7f1d1d"),
        Line("policy enforcement at the module boundary, not after resource creation", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Input"), ("alt", "Validated + applied"), ("warn", "Rejected at the boundary")])
    c.save(f"{OUT}/chapter-01-tagging-contract-validation-flow.svg")


def ch02():
    c = Canvas(960, 580,
        title="Chapter 2 Hands-On Lab: conftest Guardrail on a Terraform Plan's Required Tags",
        subtitle="A missing cost_center tag fails the guardrail; a tagless delete-only change correctly passes",
        svg_title="Chapter 2 lab flow: a policy-as-code guardrail evaluating a Terraform plan JSON for required tags",
        svg_desc="policy/required_tags.rego is evaluated with conftest against two sample Terraform plan "
                  "representations. plan-compliant.json (a create action with environment, owner, and cost_center "
                  "tags) passes with zero failures. plan-noncompliant.json (missing cost_center) fails, reporting "
                  "the resource address and the specific missing tag, with a nonzero exit code. As a negative "
                  "test, plan-delete.json — a delete-only action with no tags at all — still passes, because the "
                  "policy is intentionally scoped to evaluate only create actions, avoiding unnecessary friction "
                  "against untagged legacy resources being removed.")
    c.node_box(370, 110, 220, 90, "neutral", [
        Line("policy/required_tags.rego", 12, 700, "#111827"),
        Line("conftest test --policy policy", 10.5, 400, "#374151"),
    ])
    c.node_box(80, 250, 240, 110, "alt", [
        Line("plan-compliant.json", 12.5, 700, "#111827"),
        Line("create, all tags present", 10.5, 400, "#374151"),
        Line("PASS — 0 failures", 11, 700, "#14532d"),
    ])
    c.node_box(370, 250, 240, 110, "warn", [
        Line("plan-noncompliant.json", 12.5, 700, "#111827"),
        Line("create, missing cost_center", 10.5, 400, "#7f1d1d"),
        Line("FAIL — exit code 1", 11, 700, "#7f1d1d"),
    ])
    c.node_box(660, 250, 240, 110, "mgmt", [
        Line("plan-delete.json", 12.5, 700, "#111827"),
        Line("delete action, no tags", 10.5, 400, "#374151"),
        Line("PASS — out of policy scope", 11, 700, "#1d4ed8"),
    ])
    c.connector(430, 200, 200, 250, "alt")
    c.connector(480, 200, 490, 250, "warn")
    c.connector(560, 200, 780, 250, "mgmt")
    c.node_box(80, 420, 820, 90, "neutral", [
        Line("Negative test: the delete-only change has no tags but still passes — the policy evaluates create actions only,", 11.5, 400, "#374151"),
        Line("proving a guardrail scoped too broadly would create friction the actual policy correctly avoids.", 11.5, 400, "#374151"),
    ])
    c.legend(80, 540, [("alt", "Compliant create"), ("warn", "Noncompliant create (caught)"), ("mgmt", "Out-of-scope action")])
    c.save(f"{OUT}/chapter-02-conftest-required-tags-flow.svg")


def ch03():
    c = Canvas(960, 580,
        title="Chapter 3 Hands-On Lab: Least-Privilege IAM Policy Evaluation Catching a Wildcard Over-Grant",
        subtitle="A wildcard-action-on-wildcard-resource statement fails; a legitimate prefix wildcard correctly passes",
        svg_title="Chapter 3 lab flow: a local policy engine catching an overly broad IAM permission grant before it is ever attached",
        svg_desc="policy/no_wildcard_actions.rego denies any Allow statement combining a literal wildcard action "
                  "with a literal wildcard resource. policy-scoped.json (database:Reboot and database:Describe* "
                  "scoped to specific prod database ARNs) passes with zero failures. policy-overbroad.json (a "
                  "single EmergencyAccess statement granting action:* on resource:*) fails, naming the offending "
                  "statement. As a negative test, policy-prefix-wildcard.json — a legitimate action-prefix wildcard "
                  "(database:Describe*) scoped to a specific resource — passes, confirming the guardrail targets "
                  "only the literal double-wildcard pattern and does not false-positive on scoped prefix wildcards.")
    c.node_box(370, 110, 220, 90, "neutral", [
        Line("no_wildcard_actions.rego", 12, 700, "#111827"),
        Line("conftest test --policy policy", 10.5, 400, "#374151"),
    ])
    c.node_box(80, 250, 240, 110, "alt", [
        Line("policy-scoped.json", 12.5, 700, "#111827"),
        Line("Reboot/Describe* on prod-* ARN", 10.5, 400, "#374151"),
        Line("PASS — 0 failures", 11, 700, "#14532d"),
    ])
    c.node_box(370, 250, 240, 110, "warn", [
        Line("policy-overbroad.json", 12.5, 700, "#111827"),
        Line("EmergencyAccess: action:* resource:*", 10.5, 400, "#7f1d1d"),
        Line("FAIL — exit code 1", 11, 700, "#7f1d1d"),
    ])
    c.node_box(660, 250, 240, 110, "mgmt", [
        Line("policy-prefix-wildcard.json", 12.5, 700, "#111827"),
        Line("Describe* on specific ARN", 10.5, 400, "#374151"),
        Line("PASS — legitimate prefix", 11, 700, "#1d4ed8"),
    ])
    c.connector(430, 200, 200, 250, "alt")
    c.connector(480, 200, 490, 250, "warn")
    c.connector(560, 200, 780, 250, "mgmt")
    c.node_box(80, 420, 820, 90, "neutral", [
        Line("Negative test: a scoped action-prefix wildcard is a common, legitimate least-privilege pattern —", 11.5, 400, "#374151"),
        Line("the policy targets only the literal \"*\" action combined with the literal \"*\" resource, not any wildcard use.", 11.5, 400, "#374151"),
    ])
    c.legend(80, 540, [("alt", "Scoped, compliant policy"), ("warn", "Over-broad grant (caught)"), ("mgmt", "Legitimate wildcard (no false positive)")])
    c.save(f"{OUT}/chapter-03-iam-least-privilege-policy-flow.svg")


def ch04():
    c = Canvas(960, 560,
        title="Chapter 4 Hands-On Lab: CIDR Allocation Overlap Detection with a Terraform check Block",
        subtitle="Three distinct /20 allocations pass; duplicating one to match another trips the overlap check",
        svg_title="Chapter 4 lab flow: a Terraform check block validating that proposed CIDR allocations do not overlap",
        svg_desc="Three candidate /20 allocations (hub, payments, platform) are compared pairwise by network "
                  "address inside a Terraform check block, entirely with local values and no cloud account. "
                  "terraform plan succeeds with No changes and no check failure, confirming the three allocations "
                  "are distinct. As a negative test, the platform allocation is edited to exactly duplicate the "
                  "payments allocation (10.20.16.0/20); re-running plan reports the check failure naming the "
                  "overlap, catching the accidental duplicate before it is ever applied to a real network — though "
                  "the lab notes this simplified check only detects identical network addresses, not partial "
                  "overlap between differently sized blocks.")
    c.node_box(60, 140, 260, 130, "mgmt", [
        Line("Candidate allocations", 12.5, 700, "#111827"),
        Line("hub: 10.20.0.0/20", 10.5, 400, "#374151"),
        Line("payments: 10.20.16.0/20", 10.5, 400, "#374151"),
        Line("platform: 10.20.32.0/20", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 130, "neutral", [
        Line("check \"no_cidr_overlap\"", 12.5, 700, "#111827"),
        Line("pairwise cidrhost comparison", 10.5, 400, "#374151"),
        Line("terraform plan", 10.5, 400, "#374151"),
    ])
    c.connector(320, 205, 380, 205, "mgmt")
    c.node_box(680, 140, 240, 130, "alt", [
        Line("Result", 12.5, 700, "#111827"),
        Line("No changes.", 10.5, 700, "#14532d"),
        Line("no check failure", 10.5, 400, "#374151"),
    ])
    c.connector(620, 205, 680, 205, "alt")
    c.node_box(60, 340, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("platform allocation edited to 10.20.16.0/20 — an exact duplicate of the payments allocation", 11, 400, "#7f1d1d"),
        Line("terraform plan reports: \"Two or more allocations share an identical network address; investigate for overlap.\"", 11, 400, "#7f1d1d"),
        Line("catches the accidental duplicate before it is ever applied to a real network", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Candidate input"), ("alt", "Validated, no overlap"), ("warn", "Detected overlap")])
    c.save(f"{OUT}/chapter-04-cidr-overlap-check-flow.svg")


def ch05():
    c = Canvas(960, 560,
        title="Chapter 5 Hands-On Lab: Purchasing-Mix Calculator with a Reserved-Floor Guardrail",
        subtitle="A reserved floor of 6 (at the observed minimum) passes; a floor of 12 commits to unused capacity",
        svg_title="Chapter 5 lab flow: an on-demand/reserved/spot purchasing-mix calculation validated against observed demand",
        svg_desc="From observed_minimum_instances=6, observed_peak_instances=30, and proposed_reserved_floor=6, a "
                  "Terraform check block asserts the reserved floor never exceeds observed minimum demand. The "
                  "default plan passes with no check failure, and the purchasing_mix output shows reserved=6, "
                  "on_demand=8, spot=16, total_peak=30. As a negative test, re-planning with "
                  "proposed_reserved_floor=12 (double the observed minimum) fails the check, reporting that the "
                  "proposal commits to paying for committed capacity that is never used — an automated guardrail "
                  "against over-committing reserved capacity before any real financial commitment is made.")
    c.node_box(60, 140, 260, 130, "mgmt", [
        Line("Observed demand", 12.5, 700, "#111827"),
        Line("minimum: 6 instances", 10.5, 400, "#374151"),
        Line("peak: 30 instances", 10.5, 400, "#374151"),
        Line("proposed reserved floor: 6", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 140, 240, 130, "neutral", [
        Line("check \"reserved_floor_not_oversized\"", 11.5, 700, "#111827"),
        Line("floor ≤ observed minimum?", 10.5, 400, "#374151"),
        Line("terraform plan", 10.5, 400, "#374151"),
    ])
    c.connector(320, 205, 380, 205, "mgmt")
    c.node_box(680, 140, 240, 130, "alt", [
        Line("purchasing_mix output", 12, 700, "#111827"),
        Line("reserved=6, on_demand=8", 10.5, 400, "#374151"),
        Line("spot=16 (no check failure)", 10.5, 700, "#14532d"),
    ])
    c.connector(620, 205, 680, 205, "alt")
    c.node_box(60, 340, 860, 120, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("re-plan with proposed_reserved_floor=12 — double the observed minimum of 6", 11, 400, "#7f1d1d"),
        Line("check fails: \"this commits to paying for capacity that is never used.\"", 11, 400, "#7f1d1d"),
        Line("catches an over-committed reserved purchase before any real financial commitment", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Observed input"), ("alt", "Validated purchasing mix"), ("warn", "Over-committed floor (caught)")])
    c.save(f"{OUT}/chapter-05-purchasing-mix-guardrail-flow.svg")


def ch06():
    c = Canvas(960, 600,
        title="Chapter 6 Hands-On Lab: Storage Lifecycle Ordering and RPO-Satisfying Backup Interval Checks",
        subtitle="A default hourly backup interval fails a 15-minute RPO requirement until corrected to 10 minutes",
        svg_title="Chapter 6 lab flow: two independent Terraform check blocks validating lifecycle tier ordering and backup-interval RPO compliance",
        svg_desc="Two check blocks run against a proposed storage lifecycle policy: lifecycle_transitions_ordered "
                  "(archive_after_days must exceed infrequent_access_after_days) and "
                  "backup_interval_meets_rpo (backup_interval_minutes must not exceed required_rpo_minutes). With "
                  "defaults (30/90 days, 60-minute backups, 15-minute RPO), the ordering check passes but the RPO "
                  "check correctly fails — a 60-minute backup cannot satisfy a 15-minute RPO. Supplying "
                  "backup_interval_minutes=10 makes both checks pass. As a negative test, independently supplying "
                  "archive_after_days=20 (below the 30-day infrequent-access threshold) fails the ordering check "
                  "regardless of the backup interval, confirming the two checks validate independently.")
    c.node_box(60, 130, 260, 110, "mgmt", [
        Line("Default proposal", 12.5, 700, "#111827"),
        Line("IA: 30d, archive: 90d", 10.5, 400, "#374151"),
        Line("backup: 60min, RPO: 15min", 10.5, 400, "#374151"),
    ])
    c.node_box(380, 130, 260, 110, "warn", [
        Line("Two check blocks", 12.5, 700, "#111827"),
        Line("ordering: PASS (90 > 30)", 10.5, 700, "#14532d"),
        Line("RPO: FAIL (60 > 15)", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(320, 185, 380, 185, "mgmt")
    c.node_box(700, 130, 220, 110, "alt", [
        Line("Corrected", 12.5, 700, "#111827"),
        Line("backup_interval_minutes=10", 10.5, 400, "#374151"),
        Line("both checks PASS", 10.5, 700, "#14532d"),
    ])
    c.connector(640, 185, 700, 185, "alt")
    c.node_box(60, 340, 860, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("independently: archive_after_days=20, below infrequent_access_after_days=30", 11, 400, "#7f1d1d"),
        Line("lifecycle_transitions_ordered fails: \"tiers must transition in increasing order.\"", 11, 400, "#7f1d1d"),
        Line("confirms the ordering check fires regardless of the backup interval value", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 500, [("mgmt", "Default proposal"), ("warn", "Mixed result (one check fails)"), ("alt", "Corrected, both pass")])
    c.save(f"{OUT}/chapter-06-storage-lifecycle-rpo-checks-flow.svg")


def ch07():
    c = Canvas(960, 600,
        title="Chapter 7 Hands-On Lab: Provider-Abstracted Module Dispatch with Simulated Backends",
        subtitle="The same bucket_name/lifecycle_days_to_archive interface dispatches to provider-a or provider-b unchanged",
        svg_title="Chapter 7 lab flow: a provider-abstracted Terraform module whose calling interface stays identical across two simulated backends",
        svg_desc="A root module calls modules/object-storage with a provider_target variable and a fixed calling "
                  "interface (bucket_name, lifecycle_days_to_archive). With provider_target=provider-a (the "
                  "default), the module dispatches to a local_file resource simulating provider A's bucket, "
                  "producing endpoint \"provider-a://app-data\". Switching only provider_target to provider-b "
                  "dispatches to a differently shaped simulated resource, producing "
                  "\"provider-b://app-data\" — the calling interface never changed. As a negative test, "
                  "provider_target=provider-c is refused with a custom validation error naming the two "
                  "implemented targets, rather than silently doing nothing.")
    c.node_box(370, 110, 220, 90, "neutral", [
        Line("Root module call", 12.5, 700, "#111827"),
        Line("bucket_name, lifecycle_days", 10.5, 400, "#374151"),
    ])
    c.connector(480, 200, 480, 240, "neutral", label="provider_target")
    c.node_box(80, 260, 260, 110, "alt", [
        Line("provider_target=provider-a", 12, 700, "#111827"),
        Line("local_file: provider-a-app-data.json", 10.5, 400, "#374151"),
        Line("endpoint: provider-a://app-data", 10.5, 700, "#14532d"),
    ])
    c.node_box(620, 260, 260, 110, "alt", [
        Line("provider_target=provider-b", 12, 700, "#111827"),
        Line("local_file: provider-b-app-data.json", 10.5, 400, "#374151"),
        Line("endpoint: provider-b://app-data", 10.5, 700, "#14532d"),
    ])
    c.connector(430, 240, 210, 260, "alt")
    c.connector(530, 240, 750, 260, "alt")
    c.node_box(80, 420, 800, 110, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("provider_target=provider-c (unimplemented)", 11, 400, "#7f1d1d"),
        Line("refused: \"provider_target must be one of: provider-a, provider-b.\"", 11, 400, "#7f1d1d"),
        Line("rejects an unimplemented target explicitly rather than silently doing nothing", 11, 400, "#7f1d1d"),
    ])
    c.legend(80, 570, [("neutral", "Fixed calling interface"), ("alt", "Implemented backend"), ("warn", "Unimplemented target (rejected)")])
    c.save(f"{OUT}/chapter-07-provider-abstracted-dispatch-flow.svg")


def ch08():
    c = Canvas(960, 580,
        title="Chapter 8 Hands-On Lab: CSPM Encryption and Cost-Tag Policy Evaluation",
        subtitle="An unencrypted, untagged resource fails two policies at once; an out-of-scope resource type correctly passes both",
        svg_title="Chapter 8 lab flow: CSPM-style encryption and cost-tag governance policies evaluated against simulated resource inventories",
        svg_desc="Two conftest policies — encryption_required.rego and required_cost_tags.rego — evaluate "
                  "simulated resource inventories. inventory-compliant.json (encrypted storage bucket and "
                  "database, both fully tagged) passes both policies with zero failures. "
                  "inventory-noncompliant.json (unencrypted, missing cost_center and environment tags) fails "
                  "with two findings. As a negative test, inventory-out-of-scope.json (a log_group resource type "
                  "neither policy governs) passes cleanly, confirming CSPM and tag-governance policies scoped to "
                  "specific resource types do not produce false positives against resource types outside their "
                  "intended scope.")
    c.node_box(370, 110, 220, 90, "neutral", [
        Line("Two conftest policies", 12, 700, "#111827"),
        Line("encryption + cost-tags", 10.5, 400, "#374151"),
    ])
    c.node_box(80, 250, 240, 110, "alt", [
        Line("inventory-compliant.json", 12, 700, "#111827"),
        Line("encrypted + fully tagged", 10.5, 400, "#374151"),
        Line("PASS — 0 failures", 11, 700, "#14532d"),
    ])
    c.node_box(370, 250, 240, 110, "warn", [
        Line("inventory-noncompliant.json", 11.5, 700, "#111827"),
        Line("unencrypted, missing tags", 10.5, 400, "#7f1d1d"),
        Line("FAIL — 2 findings", 11, 700, "#7f1d1d"),
    ])
    c.node_box(660, 250, 240, 110, "mgmt", [
        Line("inventory-out-of-scope.json", 11.5, 700, "#111827"),
        Line("log_group (ungoverned type)", 10.5, 400, "#374151"),
        Line("PASS — out of scope", 11, 700, "#1d4ed8"),
    ])
    c.connector(430, 200, 200, 250, "alt")
    c.connector(480, 200, 490, 250, "warn")
    c.connector(560, 200, 780, 250, "mgmt")
    c.node_box(80, 420, 820, 90, "neutral", [
        Line("Negative test: a log_group resource matches neither policy's resource-type scope, so it passes cleanly —", 11.5, 400, "#374151"),
        Line("confirming type-scoped CSPM/tag policies do not create false-positive friction outside their governed scope.", 11.5, 400, "#374151"),
    ])
    c.legend(80, 540, [("alt", "Compliant resources"), ("warn", "Noncompliant (caught)"), ("mgmt", "Out-of-scope type")])
    c.save(f"{OUT}/chapter-08-cspm-cost-tag-policy-flow.svg")


def ch09():
    c = Canvas(960, 620,
        title="Chapter 9 Hands-On Lab: Drift Detection, Reconciliation, and a False-Positive Negative Test",
        subtitle="An out-of-band edit is detected as drift (exit code 2) and reconciled; a legitimate code-applied change is not",
        svg_title="Chapter 9 lab flow: a Terraform drift-detection cycle from baseline through out-of-band drift to reconciliation",
        svg_desc="terraform apply establishes a baseline managed_config.json with replicas=3. A drift check "
                  "(plan -detailed-exitcode) returns exit code 0, confirming no drift. An out-of-band edit via jq "
                  "(bypassing plan/apply entirely) sets replicas=5; the drift check now returns exit code 2, the "
                  "signal a scheduled drift-detection job would alert on. Applying the saved drift plan restores "
                  "replicas=3 and a follow-up check returns to exit code 0. As a negative test, a legitimate, "
                  "code-reviewed change (editing main.tf to replicas=4 and applying normally) is confirmed to "
                  "still report exit code 0 afterward — proving the drift check does not false-positive against "
                  "changes made correctly through code and apply, only against out-of-band divergence.")
    c.node_box(60, 130, 220, 100, "mgmt", [
        Line("Baseline", 12.5, 700, "#111827"),
        Line("terraform apply", 10.5, 400, "#374151"),
        Line("replicas=3", 10.5, 400, "#374151"),
    ])
    c.node_box(340, 130, 220, 100, "alt", [
        Line("Drift check #1", 12.5, 700, "#111827"),
        Line("plan -detailed-exitcode", 10.5, 400, "#374151"),
        Line("exit code 0 (no drift)", 10.5, 700, "#14532d"),
    ])
    c.connector(280, 180, 340, 180, "mgmt")
    c.node_box(620, 130, 260, 100, "warn", [
        Line("Out-of-band edit", 12.5, 700, "#111827"),
        Line("jq sets replicas=5 (bypasses IaC)", 10.5, 700, "#7f1d1d"),
        Line("drift check #2: exit code 2", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(560, 180, 620, 180, "warn")
    c.node_box(340, 280, 260, 100, "alt", [
        Line("Reconciled", 12.5, 700, "#111827"),
        Line("terraform apply drift.plan", 10.5, 400, "#374151"),
        Line("replicas=3 restored, exit 0", 10.5, 700, "#14532d"),
    ])
    c.connector(750, 230, 470, 280, "warn")
    c.node_box(60, 420, 860, 130, "neutral", [
        Line("Negative Test", 12.5, 700, "#111827"),
        Line("legitimate change: main.tf edited to replicas=4, applied normally through terraform apply", 11, 400, "#374151"),
        Line("follow-up drift check: exit code 0 — no false positive", 11, 700, "#14532d"),
        Line("confirms the check only fires on out-of-band divergence, not on changes made correctly through code", 11, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Baseline"), ("alt", "Healthy / reconciled state"), ("warn", "Drift detected")])
    c.save(f"{OUT}/chapter-09-drift-detection-reconciliation-flow.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
