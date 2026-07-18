# Chapter 04: API, Event, and Integration Automation

## Learning Objectives

- Distinguish synchronous request/response API automation from asynchronous,
  event-driven integration, and identify which pattern fits a given
  integration problem.
- Call REST APIs idempotently from Ansible (`uri` module) and Terraform
  (`http` data source), including pagination, retries, and rate-limit
  handling.
- Design and validate a webhook receiver, including HMAC signature
  verification and replay protection.
- Wire Terraform outputs into Ansible inventory as the standard
  provisioning-to-configuration handoff between the two tools.
- Integrate automation with IT service management (ITSM) systems as a
  governance checkpoint for change records.
- Diagnose common integration failures: rate limiting, pagination bugs,
  signature mismatches, and idempotency-key collisions.

## Theory and Architecture

Chapters 02 and 03 treated Terraform and Ansible as tools that talk to a
single provider or a fleet of managed hosts. In practice, automation spends
much of its time integrating with everything *around* those systems: ITSM
platforms that gate changes, monitoring systems that need to be told about
planned maintenance, secrets managers, chat platforms, and internal APIs
that other teams own. This chapter covers the patterns for that
integration layer — synchronous API calls and asynchronous event handling —
independent of any single vendor's API.

### Automation as API consumer and API producer

Automation systems sit on both sides of an API relationship:

- **Consumer.** A Terraform provider, an Ansible module, or a pipeline step
  calls someone else's API — a cloud provider, a SaaS platform, an internal
  service — to read state or make a change.
- **Producer.** The automation system exposes its own API or webhook
  endpoint so other systems can trigger it: a CI platform's
  `repository_dispatch` endpoint, a webhook receiver that kicks off a
  playbook run, or a status API that reports the last successful apply.

Most enterprise automation estates are both simultaneously: a pipeline
consumes a cloud provider's API to provision infrastructure, then produces
a webhook call to notify a change management system that the work
completed.

### Synchronous versus asynchronous integration

| Pattern | Description | Typical use |
| --- | --- | --- |
| Polling | The automation system periodically calls an API and checks for a state change. | Checking whether a long-running cloud operation (image build, snapshot) has completed. |
| Request/response (synchronous) | The caller sends a request and blocks until it receives a result. | Creating a ticket, looking up a CMDB record, validating a certificate. |
| Webhook (push) | The remote system calls back into automation when an event occurs. | A Git provider notifying a CI system of a merged pull request; a monitoring system notifying automation of an alert. |
| Event stream | Events are published to a durable log or bus (Kafka, SNS/SQS, EventBridge) and consumed asynchronously, often by multiple independent subscribers. | Fan-out notification of an infrastructure change to logging, ChatOps, and ITSM simultaneously. |

Polling is simple to reason about but trades latency and API load for
simplicity — a five-minute poll interval means up to five minutes of
detection lag. Webhooks and event streams invert the relationship: the
remote system tells automation immediately, at the cost of requiring
automation to expose a reachable, authenticated endpoint and to handle
delivery guarantees it does not control.

### Delivery guarantees and idempotency keys

Nearly every webhook and event-stream provider documents **at-least-once**
delivery: a network retry, a consumer restart, or a provider-side redelivery
policy can cause the same event to arrive twice. Automation that reacts to
events must therefore be idempotent at the event-handling layer, not just
at the underlying resource layer. The standard mechanism is an
**idempotency key** — a unique identifier (an event ID, a request UUID)
that the receiver records and checks before acting, so a duplicate delivery
is a no-op rather than a duplicate action:

```text
event received -> has event_id been processed? -> yes: ack and discard
                                                 -> no: process, then record event_id
```

Providers that expose a client-generated idempotency key on write
operations (many payment and provisioning APIs do) let the *caller* enforce
this instead: the same key submitted twice returns the original result
rather than creating a second resource.

### CloudEvents and event schema

Event-driven integrations that fan out to multiple consumers benefit from a
common event envelope rather than each producer inventing its own JSON
shape. The CNCF **CloudEvents** specification standardizes the envelope
(`id`, `source`, `type`, `time`, `data`) while leaving the payload
provider-specific, which is why it shows up as the event format underneath
tools such as Knative, several service meshes, and Event-Driven Ansible's
webhook source plugin (Chapter 07):

```json
{
  "specversion": "1.0",
  "id": "8f14e45f-ceea-4d8f-b1d3-9b7e0f6c6a11",
  "source": "urn:acme:terraform:pipeline",
  "type": "com.acme.terraform.apply.completed",
  "time": "2026-07-18T14:03:00Z",
  "data": {
    "workspace": "network-prod",
    "status": "success",
    "resources_changed": 4
  }
}
```

### ITSM integration as a governance checkpoint

Enterprises with a formal change-management process (Volume I, Chapter 08)
frequently require an automated change to reference an approved change
record before it is allowed to run against production, or to close that
record automatically once the pipeline completes. This is a concrete,
common example of API automation: the pipeline calls the ITSM platform's
REST API to create or validate a change record as a gate step, and calls it
again to update the record's state on completion or failure.

## Design Considerations

### Retry strategy: backoff and jitter

A naive retry loop that retries immediately, or at a fixed interval,
synchronizes failures across many callers and can turn a brief provider
hiccup into a self-inflicted denial-of-service ("retry storm"). Use
**exponential backoff with jitter**: each retry waits roughly double the
previous interval, randomized within a range, capped at a maximum:

```text
attempt 1: immediate
attempt 2: wait random(0, 2s)
attempt 3: wait random(0, 4s)
attempt 4: wait random(0, 8s)
give up after N attempts or a total elapsed-time budget
```

Respect a `Retry-After` header when a provider returns one (commonly on
HTTP 429 or 503 responses) instead of computing your own backoff — the
provider is telling you exactly how long to wait.

### Pagination

APIs that return large collections paginate results, using either an
offset/limit scheme or an opaque cursor token. Cursor-based pagination is
more robust under concurrent writes (an offset-based page can skip or repeat
records if the underlying collection changes between requests) and is the
pattern most modern APIs prefer. Automation that only reads the first page
and assumes it has the complete result set is a common, quiet source of
"but it worked when I tested it with 12 items" bugs once a collection grows
past the default page size.

### Rate limits and backpressure

Design integration code assuming the remote API enforces a rate limit, even
if current traffic is well under it — traffic grows, and shared credentials
mean automation may be competing with human users or other pipelines for
the same quota. Detect HTTP 429 explicitly, honor `Retry-After`, and prefer
batched or bulk endpoints over per-item loops where the API offers them.

### Webhook security

A webhook receiver is an internet- or network-reachable endpoint that
triggers automation on unauthenticated request unless it is explicitly
secured. Two controls are non-negotiable:

- **Signature verification.** The provider signs the payload with a shared
  secret (commonly HMAC-SHA256); the receiver recomputes the signature over
  the raw request body and rejects any request where it does not match
  exactly, using a constant-time comparison to avoid timing side channels.
- **Replay protection.** Verify the event's timestamp is within an
  acceptable window (for example, five minutes) and track processed event
  IDs, rejecting or deduplicating events outside that window or already
  seen — this is the idempotency-key pattern from Theory and Architecture,
  applied specifically to prevent a captured, replayed request from
  re-triggering automation.

### Choosing polling versus webhook versus event stream

Prefer a webhook or event stream when the source system supports one, low
latency matters, and you can secure an inbound endpoint. Prefer polling
when the source has no push mechanism, when you do not control network
reachability to expose a receiver, or when the operation being watched
(an image build, a long-running cloud API operation) is asynchronous on the
provider's side and only exposes a status-check API. Event streams add
durability and fan-out beyond a single webhook receiver, at the cost of
operating a broker (or consuming a managed one) — justified when more than
one system needs to react to the same event independently.

## Implementation and Automation

### Calling a REST API idempotently from Ansible

```yaml
# playbooks/roles/itsm_change/tasks/main.yml
---
- name: Create a change record before applying infrastructure changes
  ansible.builtin.uri:
    url: "https://itsm.acme.internal/api/now/table/change_request"
    method: POST
    headers:
      Authorization: "Bearer {{ itsm_api_token }}"
      Idempotency-Key: "{{ pipeline_run_id }}"
    body_format: json
    body:
      short_description: "Automated apply: {{ workspace_name }}"
      category: "infrastructure"
      requested_by: "svc_pipeline"
    status_code: [200, 201]
    timeout: 15
  register: change_record
  retries: 4
  delay: 3
  until: change_record.status in [200, 201, 429] and change_record.status != 429

- name: Fail fast on a non-retryable error
  ansible.builtin.fail:
    msg: "Change record creation failed: {{ change_record.status }}"
  when: change_record.status not in [200, 201]
```

The `Idempotency-Key` header, set to the pipeline's own run identifier,
means a retried task (from a transient network failure, or a pipeline
re-run) returns the original change record rather than creating a
duplicate — the client-side half of the idempotency-key pattern.

### Reading an external API from Terraform

Terraform's built-in `http` data source is appropriate for read-only lookups
during plan (never for creating resources — it has no lifecycle awareness
and Terraform cannot track or clean up whatever the call causes):

```hcl
data "http" "change_window_status" {
  url = "https://itsm.acme.internal/api/now/table/change_window?environment=prod"

  request_headers = {
    Authorization = "Bearer ${var.itsm_api_token}"
    Accept        = "application/json"
  }
}

locals {
  change_window_open = jsondecode(data.http.change_window_status.response_body).open
}

resource "null_resource" "guard" {
  lifecycle {
    precondition {
      condition     = local.change_window_open
      error_message = "No open change window for prod; aborting apply."
    }
  }
}
```

For actual write operations against a REST API that has no dedicated
Terraform provider, prefer a purpose-built community provider
(`terraform-provider-restapi` or similar) over `http`, since a real
provider models create/read/update/delete against state, letting Terraform
track and clean up the resource it created — exactly the gap the `http`
data source cannot fill.

### Terraform output into Ansible inventory

Chapter 03 flagged this integration point: Terraform provisions
infrastructure, and Ansible needs to know what Terraform just created
without re-typing hostnames by hand. Expose the values Ansible needs as
Terraform outputs:

```hcl
# environments/dev/outputs.tf
output "web_private_ips" {
  value = module.compute.web_private_ips
}

output "db_private_ips" {
  value = module.compute.db_private_ips
}
```

The `cloud.terraform` collection's `terraform_provider` inventory plugin
reads a Terraform state file directly and builds inventory groups from
resource tags or output structure, avoiding a hand-written glue script:

```yaml
# playbooks/inventory/terraform.yml
plugin: cloud.terraform.terraform_provider
project_path: ../../environments/dev
```

```bash
ansible-galaxy collection install cloud.terraform
ansible-inventory -i playbooks/inventory/terraform.yml --graph
```

Where the plugin is unavailable or the mapping needs custom logic, a small
`terraform output -json` pipeline achieves the same handoff explicitly:

```bash
terraform -chdir=environments/dev output -json web_private_ips \
  | jq -r '.[] | "\(.) ansible_user=svc_ansible"' > /tmp/web_hosts.ini
```

Either approach keeps the provisioning-to-configuration boundary a data
handoff through Terraform state and outputs, not a manually maintained
inventory file that silently drifts from what Terraform actually built.

### A minimal, verifiable webhook receiver

```python
# webhook/receiver.py
import hashlib
import hmac
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

SHARED_SECRET = b"replace-with-a-real-shared-secret"
SEEN_EVENT_IDS: set[str] = set()
MAX_SKEW_SECONDS = 300


def verify_signature(raw_body: bytes, signature_header: str) -> bool:
    expected = hmac.new(SHARED_SECRET, raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature_header or "")


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length)
        signature = self.headers.get("X-Signature-256", "")

        if not verify_signature(raw_body, signature):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"invalid signature")
            return

        event = json.loads(raw_body)
        if abs(time.time() - event.get("time_epoch", 0)) > MAX_SKEW_SECONDS:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"stale event rejected")
            return

        event_id = event.get("id")
        if event_id in SEEN_EVENT_IDS:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"duplicate event acknowledged")
            return

        SEEN_EVENT_IDS.add(event_id)
        print(f"processing event {event_id}: {event.get('type')}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"accepted")


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8085), Handler).serve_forever()
```

This receiver implements the three controls from Design Considerations in
about thirty lines: signature verification with a constant-time comparison,
a replay window, and an in-memory idempotency-key check. A production
receiver would persist `SEEN_EVENT_IDS` outside process memory (a database
or cache with a TTL matching the replay window) so a restart does not
silently reopen the replay window.

### Triggering a pipeline from an external event

```yaml
# .github/workflows/on-repository-dispatch.yml
name: on-repository-dispatch

on:
  repository_dispatch:
    types: [infra-change-approved]

jobs:
  apply:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Show dispatched payload
        run: echo '${{ toJson(github.event.client_payload) }}'
```

```bash
curl -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/acme/infra/dispatches \
  -d '{"event_type":"infra-change-approved","client_payload":{"change_id":"CHG0012345"}}'
```

`repository_dispatch` is GitHub's mechanism for letting an external system
(the ITSM webhook receiver, in this scenario) trigger a workflow run
carrying an arbitrary JSON payload, closing the loop between an approved
change record and an automated apply.

## Validation and Troubleshooting

- **Intermittent 429 responses under load.** Confirm the client honors
  `Retry-After` and uses jittered backoff rather than fixed-interval
  retries; log the rate-limit headers (`X-RateLimit-Remaining` or
  equivalent) to see how close to the limit normal traffic already runs.
- **Pagination silently truncates results.** Confirm the client loops until
  the response omits a `next` cursor (or `has_more: false`), not just until
  the first page looks "big enough"; write a test fixture with more items
  than one page to catch this in CI rather than in production.
- **Webhook signature verification fails for every request.** The most
  common cause is computing the signature over a re-serialized JSON object
  instead of the exact raw request bytes — whitespace and key ordering
  differences change the HMAC. Always sign and verify the raw body.
- **Duplicate actions despite an idempotency key.** Confirm the key is
  derived from something stable across retries (a pipeline run ID, not a
  freshly generated UUID per attempt) — a new key on every retry defeats
  the mechanism entirely.
- **Clock skew rejecting legitimate events.** If a receiver's replay-window
  check rejects valid events intermittently, verify NTP synchronization on
  both the sending and receiving systems before widening the skew
  tolerance, which weakens replay protection.

## Security and Best Practices

- Store API tokens and webhook shared secrets in a secrets manager
  (Chapter 06), never in playbook variables, Terraform `.tfvars`, or
  pipeline YAML committed to version control.
- Scope API tokens to the minimum set of endpoints and operations the
  integration actually uses; a token with full ITSM admin rights used only
  to create change records is unnecessary blast radius.
- Enforce TLS certificate validation on every outbound call
  (`validate_certs: true` in Ansible's `uri` module is the default — never
  disable it to work around a certificate problem instead of fixing it).
- Verify webhook signatures on every request with no exceptions for
  "trusted" networks; network position is not authentication.
- Redact tokens, signatures, and payload secrets from logs; a webhook
  receiver that logs the full raw request for debugging is a common,
  avoidable credential leak.
- Set a request timeout on every outbound call. An integration with no
  timeout can hang a pipeline stage indefinitely on a stalled remote
  service, holding locks and blocking other work.

## References and Knowledge Checks

### References

- CNCF, *CloudEvents Specification* —
  <https://cloudevents.io/>
- Red Hat, *Ansible `uri` Module Documentation* —
  <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html>
- HashiCorp, *`http` Data Source Documentation* —
  <https://registry.terraform.io/providers/hashicorp/http/latest/docs>
- Ansible, *`cloud.terraform` Collection Documentation* —
  <https://galaxy.ansible.com/ui/repo/published/cloud/terraform/>

### Knowledge Checks

1. Why must a webhook receiver verify a signature over the raw request
   body rather than a re-serialized copy of the parsed payload?
2. What problem does an idempotency key solve that retries alone do not?
3. When is the `http` Terraform data source appropriate, and why is it the
   wrong tool for creating a resource through an API with no dedicated
   provider?
4. Why is cursor-based pagination generally more robust than offset-based
   pagination under concurrent writes?
5. What two checks does replay protection require beyond simple signature
   verification?

## Hands-On Lab

### Objective

Stand up a local webhook receiver that enforces signature verification,
replay protection, and idempotency-key deduplication, then drive it with a
signed and an intentionally tampered request to prove both the positive
and negative paths.

### Prerequisites

- Python 3.10+ available locally (`python3 --version`).
- `curl` and `python3 -c "import hmac"` (standard library — no extra
  packages required).
- No cloud account or external network access required.

### Steps

1. Create the lab directory and save the receiver:

   ```bash
   mkdir -p webhook-lab && cd webhook-lab
   ```

   Save the `receiver.py` script from the Implementation section into this
   directory.

2. Start the receiver in the foreground of one terminal:

   ```bash
   python3 receiver.py
   ```

3. In a second terminal, compute a valid signature and send a legitimate
   event:

   ```bash
   cat > event.json <<'EOF'
   {"id":"evt-001","type":"infra.apply.completed","time_epoch": TIMESTAMP}
   EOF
   python3 - <<'PYEOF'
   import time
   with open("event.json") as f:
       content = f.read().replace("TIMESTAMP", str(int(time.time())))
   with open("event.json", "w") as f:
       f.write(content)
   PYEOF

   SIG=$(python3 -c "
   import hmac, hashlib
   body = open('event.json','rb').read()
   print(hmac.new(b'replace-with-a-real-shared-secret', body, hashlib.sha256).hexdigest())
   ")

   curl -i -X POST http://127.0.0.1:8085/ \
     -H "X-Signature-256: sha256=${SIG}" \
     --data-binary @event.json
   ```

4. Replay the exact same request a second time and observe deduplication:

   ```bash
   curl -i -X POST http://127.0.0.1:8085/ \
     -H "X-Signature-256: sha256=${SIG}" \
     --data-binary @event.json
   ```

### Expected Results

- Step 3 returns `HTTP/1.0 200 OK` with body `accepted`, and the receiver's
  terminal prints `processing event evt-001: infra.apply.completed`.
- Step 4 returns `HTTP/1.0 200 OK` with body `duplicate event acknowledged`
  and does **not** print a second `processing event` line — proving the
  idempotency-key check suppressed the duplicate.

### Negative Test

Send a request with a tampered body but the original signature:

```bash
curl -i -X POST http://127.0.0.1:8085/ \
  -H "X-Signature-256: sha256=${SIG}" \
  -d '{"id":"evt-002","type":"infra.apply.completed","time_epoch": 9999999999}'
```

Confirm the response is `HTTP/1.0 401 Unauthorized` with body
`invalid signature` — the receiver correctly rejects a payload that does
not match the signature computed over the original body, even though the
signature header itself is a real, previously valid value.

### Cleanup

```bash
# Stop the receiver with Ctrl+C in its terminal, then:
cd .. && rm -rf webhook-lab
```

## Summary and Completion Checklist

API and event automation extends infrastructure-as-code and configuration
management into the systems around them: ITSM platforms, chat tools, and
internal services that automation must call and be called by. Idempotency
keys, exponential backoff with jitter, cursor-based pagination, and
signature-verified, replay-protected webhooks are the small set of patterns
that make that integration layer reliable under real-world network and
provider behavior rather than only under a happy-path demo. The
Terraform-output-to-Ansible-inventory handoff closes the loop between
Chapters 02 and 03, and the change-record pattern here is the concrete
mechanism behind the policy and pipeline gates covered next in Chapter 05.

- [ ] Can explain when to use polling, a webhook, or an event stream for a
      given integration.
- [ ] Has implemented exponential backoff with jitter and `Retry-After`
      handling in at least one API client.
- [ ] Has built and tested a webhook receiver with signature verification,
      a replay window, and idempotency-key deduplication.
- [ ] Can wire Terraform outputs into Ansible inventory using either the
      `cloud.terraform` inventory plugin or an explicit `terraform output
      -json` handoff.
- [ ] Understands why the `http` Terraform data source is unsuitable for
      creating resources through an API.
