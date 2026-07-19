# Chapter 07: Workflow Orchestration and Event-Driven Operations

## Learning Objectives

- Distinguish configuration management, pipeline automation, and workflow
  orchestration, and place each correctly in an automation architecture.
- Explain the event-driven automation loop (event source, rule engine,
  action) and where Event-Driven Ansible fits in an Ansible-based estate.
- Write and run an Event-Driven Ansible rulebook that reacts to a webhook
  event by triggering a playbook.
- Design multi-step orchestration with human approval gates and
  compensating actions for partial failure.
- Apply safeguards against automation feedback loops and event storms.
- Diagnose common orchestration failures: rulebooks that never match,
  stuck workflow executions, and runaway automated responses.

## Theory and Architecture

[Chapter 01](01-automation-operating-models-and-engineering-foundations.md)'s automation maturity curve named event-driven, self-service
platform engineering as advanced stages built on everything before them.
[Chapter 04](04-api-event-and-integration-automation.md) covered the mechanics of consuming and producing events and
webhooks; [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md) covered pipelines as the mechanism for staged,
reviewed change delivery. This chapter covers what sits above both: an
orchestration layer that sequences multi-step, often multi-system work,
and reacts to events in real time rather than only on a schedule or a
pull request.

### Configuration management, pipelines, and orchestration are not the same layer

- **Configuration management** ([Chapter 03](03-configuration-management-and-desired-state-convergence.md)) converges one host or a
  bounded group of hosts to a desired state, invoked directly.
- **Pipeline automation** ([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)) sequences plan/test/policy/approve/
  apply stages for a single change, triggered by a commit or a schedule.
- **Workflow orchestration** sequences multiple, often heterogeneous steps
  — some of them playbooks, some API calls, some pipeline triggers, some
  human approvals — into a single coherent operation, and can be triggered
  by an event rather than only a commit.

A single incident-response runbook illustrates all three: workflow
orchestration invokes an API call to acknowledge the alert, an Ansible
playbook to collect diagnostics, a human approval gate before a
remediation step, and finally a pipeline trigger to apply a permanent
fix — no single layer alone models that whole sequence well.

### The event-driven automation loop

Event-driven automation follows a consistent three-part loop, matching the
architecture behind Ansible's Event-Driven Ansible (EDA) framework,
AWS EventBridge with Lambda targets, and StackStorm alike:

```text
Event source  --->  Rule engine (match conditions)  --->  Action
(webhook, message   (does this event match a           (run a playbook,
queue, log stream,   condition worth acting on?)         call an API,
metric threshold)                                        open a ticket)
```

- **Event source.** Where events originate — a webhook receiver (Chapter
  04), a message queue subscription, a monitoring system's alert stream,
  or a filesystem/log watcher.
- **Rule engine.** Evaluates incoming events against declared conditions,
  discarding events that do not match and routing matches to an action.
  This is the layer that keeps event-driven automation from being "run
  this playbook on every single event," which does not scale past a
  handful of trivial cases.
- **Action.** What actually runs when a rule matches — most often, in an
  Ansible-centric estate, a playbook run against a specific host pattern
  with variables drawn from the event payload.

### Event-Driven Ansible

Event-Driven Ansible (the `ansible-rulebook` engine, part of the Ansible
Automation Platform ecosystem) implements this loop with **rulebooks**: a
declarative YAML file naming an event source plugin, one or more
condition/action rules, and the playbook or module to run on a match.
It reuses the same execution model as ordinary Ansible content — the same
modules, the same idempotency expectations from [Chapter 03](03-configuration-management-and-desired-state-convergence.md) — but is
triggered by an event instead of a human or a cron schedule.

### Orchestration engines beyond Ansible

Where an organization needs long-running, stateful, multi-day workflows
with complex branching and retry semantics — not just "react to an event
and run a playbook" — dedicated workflow orchestration engines (AWS Step
Functions, Temporal, Argo Workflows) model the workflow itself as a state
machine, with each state's entry, exit, and failure transitions explicit
and durable across process restarts. Ansible Automation Platform's own
**workflow templates** sit between the two: they chain multiple job
templates (including approval nodes) into a single visual, auditable
workflow without requiring a separate orchestration engine, which is
sufficient for the large majority of infrastructure-operations workflows
that do not need a general-purpose durable-execution engine.

## Design Considerations

### Choosing orchestration versus point automation

Introduce a workflow/orchestration layer only when a real operation spans
multiple systems or requires conditional branching and human gates — a
single playbook run, or a single pipeline, is simpler to build, test, and
debug than a workflow wrapping just one step. The signal that orchestration
is warranted is a runbook that already has multiple named phases with
different owners or different systems, not a preference for using a newer
tool.

### Idempotency and retries at the workflow level

Idempotency ([Chapter 03](03-configuration-management-and-desired-state-convergence.md)) applies at the workflow level too, and is harder
to get right there: a workflow step that calls an external API to create a
ticket is not automatically safe to retry unless that API call itself uses
an idempotency key ([Chapter 04](04-api-event-and-integration-automation.md)). Design every workflow step assuming the
orchestration engine may retry it after a partial failure — a crashed
worker, a timed-out step — and make each step either naturally idempotent
or explicitly guarded, exactly as with a playbook task.

### Compensating actions for partial failure

A workflow that fails partway through — three of five steps completed —
needs a defined recovery path, not just a failed status. The **saga
pattern** addresses this by pairing every workflow step that has a
side effect with an explicit compensating action that undoes it, run in
reverse order from the point of failure: if step 3 of 5 (provision a
database) succeeds but step 4 (register DNS) fails, the workflow's failure
path runs step 3's compensating action (deprovision the database) rather
than leaving an orphaned, half-provisioned resource with no record of why
it exists.

### Human-in-the-loop approval gates

Not every workflow should run to completion unattended. Model an explicit
approval node for any step whose blast radius or reversibility does not
meet the bar for full automation — the same principle behind [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)'s
required-reviewer environment, generalized to a workflow that may span
multiple systems rather than a single Terraform apply. Ansible Automation
Platform's workflow templates support this natively as an approval node
that pauses the workflow and notifies a named approver group.

### Guarding against event storms and feedback loops

Event-driven automation introduces a failure mode configuration management
and pipelines do not have: an automated action that itself produces an
event the rule engine reacts to, creating a loop, or a single upstream
incident producing thousands of near-identical events that each
independently trigger an action. Guard against both explicitly:

- **Deduplicate and rate-limit** at the rule engine, not just at the event
  source — a rule that fires a remediation playbook should coalesce
  repeated matching events within a short window into a single action.
- **Break the loop structurally.** Tag or annotate events produced by
  automation itself (a `source: automation` field) and exclude that tag
  from rules that could otherwise react to their own output.
- **Circuit-break repeated failures.** If an action fails repeatedly for
  the same matched condition, stop retrying automatically and escalate to
  a human instead of looping indefinitely on a condition automation cannot
  actually resolve.

## Implementation and Automation

### A minimal Event-Driven Ansible rulebook

```yaml
# eda/rulebooks/scale-out-on-alert.yml
---
- name: React to a high-CPU alert by running a scale-out playbook
  hosts: all
  sources:
    - ansible.eda.webhook:
        host: 0.0.0.0
        port: 5000

  rules:
    - name: High CPU alert triggers scale-out
      condition: >
        event.payload.alert_name == "HighCPU" and
        event.payload.status == "firing" and
        event.payload.source != "automation"
      action:
        run_playbook:
          name: playbooks/scale_out.yml
          extra_vars:
            triggering_host: "{{ event.payload.host }}"
```

```yaml
# playbooks/scale_out.yml
---
- name: Scale out the web tier in response to a triggered alert
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Log the scale-out trigger
      ansible.builtin.debug:
        msg: "Scale-out triggered by alert on {{ triggering_host }}"

    - name: Tag this action so downstream events do not re-trigger this rule
      ansible.builtin.uri:
        url: "http://127.0.0.1:5000/annotate"
        method: POST
        body_format: json
        body:
          source: automation
          action: scale_out
          triggering_host: "{{ triggering_host }}"
        status_code: 200
```

```bash
pip install ansible-rulebook ansible-eda
ansible-galaxy collection install ansible.eda
ansible-rulebook --rulebook eda/rulebooks/scale-out-on-alert.yml -i inventory.yml --verbose
```

The `event.payload.source != "automation"` condition is the loop-breaking
guard from Design Considerations, applied directly in the rule's `condition`
expression rather than left as an assumption — any event the scale-out
playbook itself produces is explicitly excluded from re-matching the same
rule.

### An orchestration workflow with an approval gate

Ansible Automation Platform models a workflow as a directed graph of nodes
in its API; the equivalent structure, expressed as the workflow
specification the controller API consumes, looks like this:

```json
{
  "name": "incident-remediation-workflow",
  "nodes": [
    { "id": "diagnose", "unified_job_template": "collect-diagnostics-jt" },
    {
      "id": "approve",
      "unified_job_template": "approval-remediate-prod",
      "success_nodes": ["remediate"]
    },
    { "id": "remediate", "unified_job_template": "apply-remediation-jt" }
  ],
  "edges": [
    { "from": "diagnose", "to": "approve", "on": "success" }
  ]
}
```

```bash
curl -X POST https://aap.acme.internal/api/v2/workflow_job_templates/42/launch/ \
  -H "Authorization: Bearer ${AAP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"extra_vars": {"incident_id": "INC0045678"}}'
```

The `approve` node pauses the workflow and waits for a named approver to
act through the controller UI or API before `remediate` runs — the
workflow-level equivalent of [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)'s required-reviewer environment,
but spanning a multi-step operation instead of a single apply.

### ChatOps as a trigger and approval surface

```yaml
# .github/workflows/chatops-trigger.yml (excerpt)
name: chatops-trigger

on:
  repository_dispatch:
    types: [slack-remediate-command]

jobs:
  remediate:
    runs-on: ubuntu-latest
    environment: prod-remediation
    steps:
      - name: Run remediation playbook
        run: ansible-playbook playbooks/remediate.yml -e "incident_id=${{ github.event.client_payload.incident_id }}"
```

A Slack slash command (`/remediate INC0045678`) posted to a small internal
service that validates the requester's group membership and then calls
GitHub's `repository_dispatch` endpoint ([Chapter 04](04-api-event-and-integration-automation.md)) is a common,
low-effort ChatOps pattern: it puts a human-triggered action behind the
same environment-scoped credential and approval controls as any other
pipeline stage, rather than granting chat-platform users direct pipeline
access.

## Validation and Troubleshooting

- **A rulebook never fires despite matching events arriving.** Confirm the
  event source plugin is actually receiving events — run
  `ansible-rulebook` with `--verbose` and inspect the raw event payload
  logged before the rule's `condition` is evaluated; a condition
  referencing `event.payload.alert_name` fails silently (never matches) if
  the actual field is nested differently, such as
  `event.payload.labels.alertname`.
- **The same event triggers the action multiple times.** Check for
  multiple event source instances subscribed to the same feed (a common
  result of running more than one `ansible-rulebook` process against the
  same webhook or queue), and confirm the idempotency-key pattern from
  [Chapter 04](04-api-event-and-integration-automation.md) is applied at the action layer, not assumed at the event
  layer.
- **A workflow stalls indefinitely at an approval node.** Confirm the
  configured approver group actually has members with notification
  channels configured — an approval node with no reachable approver fails
  silently from the requester's point of view, appearing "stuck" rather
  than erroring.
- **An automated action appears to re-trigger itself in a loop.** Audit
  whether the action's own side effects (a log line, a status update, a
  metric) are visible to the same event source the rule watches, and add
  or fix the `source: automation` exclusion tag from Implementation and
  Automation.
- **A saga's compensating action fails after the original step already
  succeeded.** Treat this as a distinct incident from the original
  workflow failure — a failed compensating action can leave a resource in
  a worse, inconsistent state than either fully applied or fully rolled
  back, and needs its own alerting rather than being silently swallowed.

## Security and Best Practices

- Restrict who can trigger privileged workflows (a `remediate` or
  `scale_out` action against production) to a named, audited group,
  whether the trigger is a rulebook, a ChatOps command, or a manual
  workflow launch.
- Treat every event source as untrusted input until authenticated — apply
  the same webhook signature verification and replay protection from
  [Chapter 04](04-api-event-and-integration-automation.md) to any event source feeding a rule engine, since a forged
  event is a forged trigger for a privileged action.
- Log every rule match and every action it triggered, including the
  matched event's ID, for the same audit reasons pipeline runs are logged
  in [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md).
- Rate-limit and circuit-break automated responses to repeated triggers;
  an automated remediation that fires without limit during a real incident
  can amplify the incident rather than resolve it.
- Scope the credentials an orchestration engine or rulebook action uses
  with the same least-privilege discipline as a pipeline's apply stage
  ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)) — an orchestration engine with standing broad credentials
  is a single point of privileged compromise across every workflow it
  runs.
- Require human approval for any workflow node whose action is not fully
  reversible, regardless of how confident the automation's diagnosis step
  is.

## References and Knowledge Checks

### References

- Red Hat, *Event-Driven Ansible Documentation* —
  <https://docs.ansible.com/projects/ansible-eda/>
- Red Hat, *Ansible Rulebook Documentation* —
  <https://ansible.readthedocs.io/projects/rulebook/>
- Red Hat, *Ansible Automation Platform: Workflow Job Templates* —
  <https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/>
- AWS, *AWS Step Functions Developer Guide* —
  <https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html>

### Knowledge Checks

1. What distinguishes workflow orchestration from both configuration
   management and pipeline automation?
2. Describe the three components of the event-driven automation loop and
   give an example of each.
3. What is a compensating action, and why does the saga pattern run them
   in reverse order from the point of failure?
4. What two structural techniques prevent an automated action from
   re-triggering the rule that caused it?
5. Why should a webhook feeding an event-driven rule engine be treated as
   untrusted input?

## Hands-On Lab

### Objective

Install Event-Driven Ansible locally, write a rulebook that reacts to a
webhook event by running a playbook, and demonstrate the loop-breaking
guard by sending both a triggering event and a self-produced event that
must be ignored.

### Prerequisites

- Python 3.10+, `pip install ansible-rulebook ansible-core==2.17.*`.
- `ansible-galaxy collection install ansible.eda`.
- `curl` for sending test events.
- No cloud account required — this lab runs entirely on localhost.

### Steps

1. Create the lab layout:

   ```bash
   mkdir -p eda-lab/eda/rulebooks eda-lab/playbooks
   cd eda-lab
   ```

2. Create the inventory and playbook:

   ```bash
   cat > inventory.yml <<'EOF'
   all:
     hosts:
       localhost:
         ansible_connection: local
   EOF

   cat > playbooks/scale_out.yml <<'EOF'
   ---
   - name: Scale-out response
     hosts: localhost
     gather_facts: false
     tasks:
       - name: Record the trigger
         ansible.builtin.lineinfile:
           path: /tmp/eda-lab-actions.log
           line: "Scale-out triggered by alert on {{ triggering_host | default('unknown') }}"
           create: true
   EOF
   ```

3. Create the rulebook from the Implementation section, simplified for a
   local file-based action instead of the annotate callback:

   ```bash
   cat > eda/rulebooks/scale-out-on-alert.yml <<'EOF'
   ---
   - name: React to a high-CPU alert
     hosts: all
     sources:
       - ansible.eda.webhook:
           host: 0.0.0.0
           port: 5000
     rules:
       - name: High CPU alert triggers scale-out
         condition: >
           event.payload.alert_name == "HighCPU" and
           event.payload.status == "firing" and
           event.payload.source != "automation"
         action:
           run_playbook:
             name: playbooks/scale_out.yml
             extra_vars:
               triggering_host: "{{ event.payload.host }}"
   EOF
   ```

4. Start the rulebook in one terminal:

   ```bash
   ansible-rulebook --rulebook eda/rulebooks/scale-out-on-alert.yml \
     -i inventory.yml --verbose
   ```

5. In a second terminal, send a matching event:

   ```bash
   curl -X POST http://127.0.0.1:5000/endpoint \
     -H "Content-Type: application/json" \
     -d '{"alert_name": "HighCPU", "status": "firing", "host": "web01", "source": "monitoring"}'
   ```

### Expected Results

- The `ansible-rulebook` terminal logs the matched rule and the
  `scale_out.yml` playbook run.
- `/tmp/eda-lab-actions.log` contains the line
  `Scale-out triggered by alert on web01`.

### Negative Test

Send an event tagged as automation-produced and confirm it is correctly
ignored:

```bash
curl -X POST http://127.0.0.1:5000/endpoint \
  -H "Content-Type: application/json" \
  -d '{"alert_name": "HighCPU", "status": "firing", "host": "web01", "source": "automation"}'
```

Confirm no new line is appended to `/tmp/eda-lab-actions.log` and the
`ansible-rulebook` terminal shows the event was received but the rule's
condition did not match — proving the `event.payload.source != "automation"`
guard actually prevents a feedback loop rather than merely documenting the
intent to prevent one.

### Cleanup

```bash
# Stop ansible-rulebook with Ctrl+C in its terminal, then:
rm -f /tmp/eda-lab-actions.log
cd .. && rm -rf eda-lab
```

## Summary and Completion Checklist

Workflow orchestration and event-driven automation extend the pipeline and
configuration-management layers from earlier chapters into real-time,
multi-step, multi-system operations. Event-Driven Ansible's rulebooks
apply the same event-source/rule/action loop used by EventBridge and
StackStorm to Ansible's existing module and playbook ecosystem, while
Ansible Automation Platform's workflow templates (or a dedicated engine
such as Step Functions or Temporal for genuinely long-running, stateful
work) sequence heterogeneous steps with explicit approval gates and
compensating actions for partial failure. The loop-breaking, deduplication,
and circuit-breaking guards in this chapter exist because event-driven
automation is the one layer in this volume capable of triggering itself —
a failure mode configuration management and scheduled pipelines simply do
not have.

- [ ] Can distinguish configuration management, pipeline automation, and
      workflow orchestration by scope and trigger.
- [ ] Has written and run an Event-Driven Ansible rulebook that reacts to a
      webhook event.
- [ ] Can explain the saga pattern and when a compensating action is
      required.
- [ ] Has implemented (or can describe implementing) a guard against an
      automated action re-triggering its own rule.
- [ ] Understands why event sources feeding a rule engine must be
      authenticated, not merely reachable.
