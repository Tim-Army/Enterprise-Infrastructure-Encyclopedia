import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-01-enterprise-engineering-foundations"

def ch01():
    c = Canvas(920, 480,
        title="Chapter 1 Hands-On Lab: Signed-Commit Workstation Flow",
        subtitle="SSH commit signing, key registration, and verification",
        svg_title="Chapter 1 lab flow: generating and registering an SSH signing key, then verifying signed commits",
        svg_desc="A lab-only ed25519 key is generated on the developer workstation and registered with GitHub as a "
                  "signing key via the gh CLI. A commit made with that key shows as a Good signature when verified "
                  "locally and as Verified on GitHub. As a negative test, a commit signed with a key that was never "
                  "registered with GitHub still produces a local signature but shows as Unverified on GitHub, "
                  "demonstrating that registration -- not just local signing -- is the control that matters.")
    c.node_box(40, 90, 220, 90, "mgmt", [
        Line("Developer Workstation", 13, 700, "#111827"),
        Line("bash, git, ssh-keygen, gh CLI", 10.5, 400, "#374151"),
    ])
    c.connector(260, 120, 380, 120, "mgmt", label="ssh-keygen -t ed25519")
    c.node_box(380, 75, 200, 60, "mgmt", [
        Line("Lab SSH Key", 12, 700, "#111827"),
        Line("id_ed25519_lab", 10.5, 400, "#374151"),
    ])
    c.connector(480, 135, 480, 190, "mgmt", label="gh ssh-key add --type signing")
    c.node_box(380, 190, 200, 60, "alt", [
        Line("GitHub Account", 12, 700, "#111827"),
        Line("registered signing key", 10.5, 400, "#14532d"),
    ])
    c.connector(150, 180, 150, 260, "mgmt", label="git commit (gpgsign)")
    c.node_box(40, 260, 260, 70, "data", [
        Line("Local Repo Commit", 12, 700, "#7c2d12"),
        Line("git config commit.gpgsign true", 10.5, 400, "#7c2d12"),
    ])
    c.connector(170, 330, 170, 380, "data", label="git log --show-signature")
    c.node_box(40, 380, 260, 60, "alt", [
        Line('Registered key -> "Good signature"', 11, 700, "#14532d"),
    ])
    c.connector(480, 260, 620, 380, "warn", label="unregistered key (negative test)")
    c.node_box(620, 380, 260, 60, "warn", [
        Line('Unregistered key -> "Unverified" on GitHub', 11, 700, "#7f1d1d"),
    ])
    c.legend(40, 450, [("mgmt", "Setup / registration step"), ("alt", "Expected (passing) outcome"), ("warn", "Negative-test outcome")])
    c.save(f"{OUT}/chapter-01-signed-commit-workstation-flow.svg")

def ch02():
    c = Canvas(920, 480,
        title="Chapter 2 Hands-On Lab: Repository Contract Enforcement Flow",
        subtitle="Directory contract, CODEOWNERS, branch protection, and a pre-commit structural gate",
        svg_title="Chapter 2 lab flow: a scratch repository's structural contract enforced locally by pre-commit and remotely by branch protection",
        svg_desc="A scratch GitHub repository is created with a directory contract (every unit/ directory must contain "
                  "a README.md), a CODEOWNERS file, GitHub branch protection on main, and a local pre-commit hook that "
                  "runs the same structure check before any commit is made. A unit that satisfies the contract commits "
                  "successfully. As a negative test, a unit missing its required README.md is rejected by the "
                  "pre-commit hook locally, before it ever reaches GitHub.")
    c.node_box(40, 60, 260, 70, "mgmt", [
        Line("Scratch GitHub Repo", 13, 700, "#111827"),
        Line("CODEOWNERS + branch protection", 10.5, 400, "#374151"),
    ])
    c.connector(170, 130, 170, 180, "mgmt", label="pre-commit install")
    c.node_box(40, 180, 260, 60, "mgmt", [
        Line("Local Pre-Commit Hook", 12, 700, "#111827"),
        Line("scripts/validate-structure.sh", 10.5, 400, "#374151"),
    ])
    c.connector(170, 240, 170, 290, "data")
    c.node_box(40, 290, 260, 60, "data", [
        Line("git commit", 12, 700, "#7c2d12"),
        Line("runs the structure-check hook", 10.5, 400, "#7c2d12"),
    ])
    c.connector(300, 320, 420, 260, "alt", label="unit-02/README.md present")
    c.node_box(420, 230, 260, 60, "alt", [
        Line("Commit accepted", 12, 700, "#14532d"),
        Line("contract satisfied", 10.5, 400, "#14532d"),
    ])
    c.connector(300, 340, 420, 400, "warn", label="unit-03/README.md missing (negative test)")
    c.node_box(420, 370, 260, 70, "warn", [
        Line("Commit rejected locally", 12, 700, "#7f1d1d"),
        Line("MISSING: units/unit-03-broken/README.md", 10, 400, "#7f1d1d"),
    ])
    c.legend(40, 450, [("mgmt", "Setup step"), ("alt", "Passing commit"), ("warn", "Blocked commit (negative test)")])
    c.save(f"{OUT}/chapter-02-repository-contract-enforcement-flow.svg")

def ch03():
    c = Canvas(940, 520,
        title="Chapter 3 Hands-On Lab: Two-Stage Pipeline with an Approval Gate",
        subtitle="A read-only validation job on every pull request, and a manually approved deploy job after merge",
        svg_title="Chapter 3 lab flow: pull-request validation, merge, and an approval-gated deploy workflow",
        svg_desc="Every pull request triggers a read-only Validate workflow automatically. Merging to main triggers a "
                  "separate Deploy workflow scoped to the production GitHub environment, which pauses in a Waiting "
                  "state until a configured reviewer approves it, then completes. As a negative test, removing the "
                  "only eligible reviewer from the production environment and triggering a new deploy run shows the "
                  "gate fails closed: the run cannot proceed without any eligible approver.")
    c.node_box(40, 60, 220, 60, "mgmt", [
        Line("Pull Request", 13, 700, "#111827"),
        Line("opened against main", 10.5, 400, "#374151"),
    ])
    c.connector(260, 90, 380, 90, "mgmt", label="on: pull_request")
    c.node_box(380, 60, 220, 60, "alt", [
        Line("Validate workflow", 12, 700, "#14532d"),
        Line("runs automatically, passes", 10.5, 400, "#14532d"),
    ])
    c.connector(150, 120, 150, 180, "mgmt", label="gh pr merge --squash")
    c.node_box(40, 180, 220, 50, "mgmt", [
        Line("Merge to main", 12, 700, "#111827"),
    ])
    c.connector(150, 230, 150, 280, "mgmt", label="on: push (main)")
    c.node_box(40, 280, 260, 70, "data", [
        Line("Deploy workflow", 12, 700, "#7c2d12"),
        Line("environment: production", 10.5, 400, "#7c2d12"),
        Line('paused: "Waiting"', 10.5, 700, "#7c2d12"),
    ])
    c.connector(300, 300, 420, 250, "alt", label="reviewer approves")
    c.node_box(420, 220, 260, 60, "alt", [
        Line("Deployment step executed", 12, 700, "#14532d"),
        Line("job proceeds and completes", 10.5, 400, "#14532d"),
    ])
    c.connector(300, 340, 420, 400, "warn", label="no eligible reviewer (negative test)")
    c.node_box(420, 400, 260, 70, "warn", [
        Line("Run cannot proceed", 12, 700, "#7f1d1d"),
        Line("gate fails closed, not open", 10.5, 400, "#7f1d1d"),
    ])
    c.legend(40, 480, [("mgmt", "Trigger / merge event"), ("alt", "Approved and passing"), ("warn", "Blocked (no approver)")])
    c.save(f"{OUT}/chapter-03-two-stage-pipeline-approval-gate-flow.svg")

def ch04():
    c = Canvas(940, 480,
        title="Chapter 4 Hands-On Lab: Linked Issue and Pull Request Flow",
        subtitle="A GitHub Project board with an issue that auto-closes only via the documented closing-keyword syntax",
        svg_title="Chapter 4 lab flow: an issue linked to a Project board, closed automatically by a pull request's closing keyword",
        svg_desc="An issue is created, added to a GitHub Project (v2) board, and a pull request whose body contains "
                  "the closing keyword syntax (Closes #N) is opened against it. Merging that pull request auto-closes "
                  "the issue. As a negative test, a second pull request that only references its issue inside a code "
                  "comment -- not in the PR body's closing-keyword syntax -- is merged, and the issue remains open, "
                  "confirming only the documented syntax triggers auto-close.")
    c.node_box(40, 70, 240, 60, "mgmt", [
        Line("Issue + Project (v2) Board", 13, 700, "#111827"),
        Line("gh issue create / project item-add", 10.5, 400, "#374151"),
    ])
    c.connector(160, 130, 160, 190, "mgmt")
    c.node_box(40, 190, 240, 60, "data", [
        Line("Pull Request body:", 11.5, 700, "#7c2d12"),
        Line('"Closes #<issue-number>"', 11, 400, "#7c2d12"),
    ])
    c.connector(280, 220, 420, 160, "alt", label="gh pr merge")
    c.node_box(420, 130, 260, 60, "alt", [
        Line("Issue auto-closes", 12, 700, "#14532d"),
        Line("state == CLOSED", 10.5, 400, "#14532d"),
    ])
    c.node_box(40, 300, 240, 60, "warn", [
        Line("Second PR:", 11.5, 700, "#7f1d1d"),
        Line("issue referenced in a code comment only", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(280, 330, 420, 380, "warn", label="gh pr merge (negative test)")
    c.node_box(420, 350, 260, 60, "warn", [
        Line("Issue stays OPEN", 12, 700, "#7f1d1d"),
        Line("informal reference does not close it", 10.5, 400, "#7f1d1d"),
    ])
    c.legend(40, 440, [("mgmt", "Setup"), ("alt", "Documented syntax closes issue"), ("warn", "Informal reference does not")])
    c.save(f"{OUT}/chapter-04-linked-issue-pull-request-flow.svg")

def ch05():
    c = Canvas(940, 460,
        title="Chapter 5 Hands-On Lab: Documentation Pipeline Link-Validation Gate",
        subtitle="An internal-link checker that must pass before a Pandoc build ever runs",
        svg_title="Chapter 5 lab flow: a markdown source tree, an internal-link checker gate, and a Pandoc HTML build",
        svg_desc="A small markdown source tree (intro.md linking to setup.md) is validated by an internal-link "
                  "checker script before Pandoc builds standalone HTML. With valid links the checker exits 0 and the "
                  "Pandoc build produces working HTML. As a negative test, the link in intro.md is deliberately broken "
                  "(setup.md misspelled as setpu.md); the checker catches it and exits non-zero before any HTML is "
                  "built, then the file is restored and the checker passes again.")
    c.node_box(40, 70, 220, 60, "mgmt", [
        Line("Markdown Source Tree", 12, 700, "#111827"),
        Line("content/intro.md, setup.md", 10.5, 400, "#374151"),
    ])
    c.connector(260, 100, 380, 100, "mgmt", label="check-internal-links.sh")
    c.node_box(380, 70, 220, 60, "data", [
        Line("Internal-Link Checker", 12, 700, "#7c2d12"),
    ])
    c.connector(490, 130, 490, 190, "alt", label="all links valid")
    c.node_box(380, 190, 220, 50, "alt", [
        Line("Exit 0", 12, 700, "#14532d"),
    ])
    c.connector(490, 240, 490, 290, "alt", label="pandoc --embed-resources")
    c.node_box(380, 290, 220, 50, "alt", [
        Line("output/html/intro.html", 12, 700, "#14532d"),
    ])
    c.node_box(40, 190, 220, 60, "warn", [
        Line("setup.md -> setpu.md", 11.5, 700, "#7f1d1d"),
        Line("(negative test)", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(150, 250, 150, 300, "warn", label="check-internal-links.sh")
    c.node_box(40, 300, 220, 70, "warn", [
        Line("BROKEN LINK in content/intro.md", 10.5, 700, "#7f1d1d"),
        Line("exits non-zero, build never runs", 10.5, 400, "#7f1d1d"),
    ])
    c.legend(40, 420, [("mgmt", "Source"), ("alt", "Valid links, build proceeds"), ("warn", "Broken link, build blocked")])
    c.save(f"{OUT}/chapter-05-documentation-pipeline-link-validation-flow.svg")

def ch06():
    c = Canvas(940, 460,
        title="Chapter 6 Hands-On Lab: Domain Inventory Schema Validation",
        subtitle="A git-tracked infrastructure domain inventory validated against required fields and controlled vocabularies",
        svg_title="Chapter 6 lab flow: a version-controlled domain inventory validated against a required-field and controlled-vocabulary schema",
        svg_desc="A JSON inventory of infrastructure domains (networking, identity, and so on) is validated by a "
                  "script that checks every record has all required fields and that criticality_tier and "
                  "consumption_model use only the controlled vocabulary values. A valid inventory passes with exit 0. "
                  "As a negative test, a new record with a missing field and two invalid vocabulary values "
                  "(on-prem instead of on-premises, critical instead of a defined tier) is added, and the validator "
                  "reports all four problems in the same run before the file is restored.")
    c.node_box(40, 70, 260, 70, "mgmt", [
        Line("domain-inventory.json", 13, 700, "#111827"),
        Line("networking, identity records", 10.5, 400, "#374151"),
    ])
    c.connector(170, 140, 170, 190, "mgmt", label="validate-domain-inventory.sh")
    c.node_box(40, 190, 260, 60, "data", [
        Line("Schema Validator", 12, 700, "#7c2d12"),
        Line("required fields + controlled vocab", 10.5, 400, "#7c2d12"),
    ])
    c.connector(300, 210, 420, 150, "alt", label="valid record")
    c.node_box(420, 120, 280, 60, "alt", [
        Line("Exit 0, no errors", 12, 700, "#14532d"),
    ])
    c.connector(300, 250, 420, 310, "warn", label="record missing fields + bad values (negative test)")
    c.node_box(420, 280, 280, 100, "warn", [
        Line("RECORD 2: missing 'primary_locations'", 10, 700, "#7f1d1d"),
        Line("RECORD 2: missing 'encyclopedia_reference'", 10, 400, "#7f1d1d"),
        Line("RECORD 2: invalid criticality_tier 'critical'", 10, 400, "#7f1d1d"),
        Line("RECORD 2: invalid consumption_model 'on-prem'", 10, 400, "#7f1d1d"),
    ])
    c.legend(40, 420, [("mgmt", "Source"), ("alt", "Valid record"), ("warn", "Rejected record (negative test)")])
    c.save(f"{OUT}/chapter-06-domain-inventory-schema-validation-flow.svg")

def ch07():
    c = Canvas(940, 480,
        title="Chapter 7 Hands-On Lab: ADR Log with Supersession",
        subtitle="Two linked architecture decisions, validated for required sections and a controlled status vocabulary",
        svg_title="Chapter 7 lab flow: an ADR log validated for structure, with one decision superseding another",
        svg_desc="ADR-0001 records a decision (Accepted) to standardize on a monorepo. ADR-0002 later reverses that "
                  "decision, and ADR-0001's status is updated to Superseded by ADR-0002. A validator checks every "
                  "ADR file for four required sections (Status, Context, Decision, Consequences) and a status value "
                  "matching the controlled pattern. As a negative test, a third ADR missing two required sections and "
                  "using an invalid status value (In Review) is rejected with all three problems reported together.")
    c.node_box(40, 60, 240, 70, "mgmt", [
        Line("ADR-0001: Accepted", 12, 700, "#111827"),
        Line("Standardize on a monorepo", 10.5, 400, "#374151"),
    ])
    c.connector(280, 95, 380, 95, "data", label="ADR-0002 supersedes it")
    c.node_box(380, 60, 260, 70, "data", [
        Line("ADR-0002: Accepted", 12, 700, "#7c2d12"),
        Line("Revert to polyrepo", 10.5, 400, "#7c2d12"),
    ])
    c.connector(160, 130, 160, 180, "mgmt", label="status updated")
    c.node_box(40, 180, 240, 50, "mgmt", [
        Line("ADR-0001: Superseded by ADR-0002", 11, 700, "#111827"),
    ])
    c.connector(160, 230, 160, 280, "alt", label="validate-adr-log.sh")
    c.node_box(40, 280, 240, 50, "alt", [
        Line("Exit 0 -- structure & status valid", 11.5, 700, "#14532d"),
    ])
    c.node_box(420, 180, 300, 60, "warn", [
        Line("ADR-0003: status 'In Review'", 11.5, 700, "#7f1d1d"),
        Line("(negative test)", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(570, 240, 570, 290, "warn", label="validate-adr-log.sh")
    c.node_box(420, 290, 300, 90, "warn", [
        Line("MISSING SECTION '## Context'", 10.5, 700, "#7f1d1d"),
        Line("MISSING SECTION '## Consequences'", 10.5, 400, "#7f1d1d"),
        Line("INVALID STATUS 'In Review'", 10.5, 400, "#7f1d1d"),
    ])
    c.legend(40, 440, [("mgmt", "Decision record"), ("alt", "Passing validation"), ("warn", "Rejected (negative test)")])
    c.save(f"{OUT}/chapter-07-adr-log-supersession-flow.svg")

def ch08():
    c = Canvas(940, 460,
        title="Chapter 8 Hands-On Lab: CMDB Lifecycle State Machine",
        subtitle="A git-tracked asset record driven through its legal lifecycle, with illegal transitions rejected",
        svg_title="Chapter 8 lab flow: a CMDB asset record transitioned through a lifecycle state machine, with an illegal transition rejected",
        svg_desc="A CMDB record for srv-app-lab-001 moves through its legal lifecycle states in order: planned, "
                  "procured, deployed, operating, maintenance, operating again, and finally decommissioned. Every "
                  "transition is checked by a validator against a table of legal from-to state pairs before the "
                  "record is modified. As a negative test, an attempt to transition the asset from decommissioned "
                  "back to operating is rejected as illegal, and because the validator runs before the file is "
                  "written, the record's state is never corrupted by the rejected attempt.")
    states = ["planned", "procured", "deployed", "operating", "maintenance"]
    x = 30
    for i, s in enumerate(states):
        c.node_box(x, 90, 150, 50, "mgmt", [Line(s, 11.5, 700, "#111827")])
        if i < len(states) - 1:
            c.connector(x + 150, 115, x + 180, 115, "mgmt")
        x += 180
    c.connector(x - 30, 140, x - 30, 190, "mgmt", label="apply-transition.sh")
    c.node_box(x - 180, 190, 150, 50, "alt", [Line("operating", 11.5, 700, "#14532d")])
    c.connector(x - 105, 240, x - 105, 290, "alt")
    c.node_box(x - 180, 290, 150, 50, "alt", [Line("decommissioned", 11, 700, "#14532d")])
    c.text(480, 20 + 350, "", 1)  # no-op spacer to keep formatter happy
    c.node_box(60, 350, 300, 60, "warn", [
        Line("attempt: decommissioned -> operating", 11, 700, "#7f1d1d"),
        Line("(negative test)", 10.5, 400, "#7f1d1d"),
    ])
    c.connector(360, 380, 460, 380, "warn", label="validate-lifecycle-transition.sh")
    c.node_box(460, 350, 300, 60, "warn", [
        Line("ILLEGAL TRANSITION -- rejected", 11.5, 700, "#7f1d1d"),
        Line("record state unchanged", 10.5, 400, "#7f1d1d"),
    ])
    c.legend(40, 440, [("mgmt", "Legal transition"), ("alt", "Terminal state reached"), ("warn", "Illegal transition (negative test)")])
    c.save(f"{OUT}/chapter-08-cmdb-lifecycle-state-machine-flow.svg")

ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08()
