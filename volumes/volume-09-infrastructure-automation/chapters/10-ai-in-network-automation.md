# Chapter 10: AI in Network Automation

## Learning Objectives

- Describe the benefits and risks of AI-assisted code development for network
  automation, including data privacy, intellectual-property ownership, and the
  need to validate generated code before it runs.
- Interpret the security risks in an AI-based network automation solution —
  prompt injection through a source of truth, secret leakage in model context,
  and over-broad tool permissions.
- Construct a Model Context Protocol (MCP) server with Python **FastMCP** that
  exposes read-only network information to an AI agent.
- Construct a conversational agent that leverages a large language model (LLM)
  to select and drive automation tools, behind an allowlist and an approval
  gate.
- Evaluate the accuracy of AI recommendations against a ground-truth test
  harness rather than accepting them on trust.
- Place these skills against the two ways Cisco now tests AI in the Automation
  track: the **AI in Automation** domain of the AUTOCOR 350-901 v2.0 written
  exam, and the **AI Deploy, Operate, and Optimize (AI DOO)** module coming to
  the CCIE Automation practical exam.

## Theory and Architecture

The preceding chapters treated automation as deterministic code: a Terraform
plan, an Ansible role, a pipeline stage, a webhook receiver. Each produces the
same result every time it runs, and the whole discipline of testing and policy
gates (Chapter 05) rests on that determinism. Large language models break that
assumption. An LLM is a *probabilistic* component — the same prompt can yield
different output on two runs — and that single property reshapes how AI is
introduced into an automation system: never as the thing that decides and acts
unsupervised, but as an assistant whose output is validated by the
deterministic machinery already in place.

Cisco frames the AI skill set for the Automation track in two complementary
ways, and this chapter covers both:

- **Soft engineering** — using a general-purpose LLM to help a human engineer:
  scoping a problem, drafting code, explaining an error, and validating output.
  The engineer stays in the loop and owns the result.
- **Augmented engineering (AIOps)** — wiring AI *into* the operational system:
  an agent that can query network state through tools, correlate telemetry, and
  propose or (behind guardrails) apply changes.

### AI-assisted development: assistant, not author

An AI coding assistant accelerates the mechanical parts of automation work —
boilerplate for a REST client, a first draft of a YANG-to-Jinja template, a
regular expression for a parser. The benefit is real: less time on repetitive
scaffolding, more on design and review. The risk is equally real and specific:

- **Data privacy.** Whatever you paste into a hosted model — running configs,
  addresses, community strings, topology — may leave your administrative
  boundary. Sanitize context before it goes to an external model, or use a
  model deployment that contractually and technically keeps data in-boundary.
- **IP ownership.** Generated code can echo training data, and your
  organization's policy on the license and ownership of model output must be
  settled *before* that output lands in a production repository.
- **Validation.** Model output is plausible, not correct. It can invent a
  module argument, a CLI keyword, or an API field that does not exist. Nothing
  generated is trusted until the same linters, `--syntax-check`, `validate`,
  and tests that gate human-written code have passed on it.

The through-line is that AI does not replace the validation pipeline; it
*increases the load on it*, because it produces more code, faster, that has
never been reasoned through by a person.

### Model Context Protocol and tools

An LLM on its own only produces text. To make it useful for operations it needs
**tools** — functions it can call to read real state or effect change. The
**Model Context Protocol (MCP)** is an open protocol that standardizes how a
model (the client) discovers and calls tools exposed by a server. An MCP server
advertises a set of named tools with typed inputs and outputs; the agent picks
a tool, the server runs it, and the result returns to the model as grounded
context. **FastMCP** is the Python framework for building these servers: a
decorated function becomes a tool, and its type hints become the tool's schema.

The architectural rule that matters most here is the **read/write split**. A
server that only *reads* network state (device facts, interface status, a
route) is low-risk: the worst case is a wrong answer. A server that *writes*
(pushes config, reloads a device) hands an irreversible action to a
probabilistic caller, and must never be exposed without an explicit approval
gate around the write.

### Conversational agents and the agentic loop

A conversational automation agent runs a loop: take a natural-language request,
ask the model which tool to call (and with what arguments), execute that tool,
feed the result back, and repeat until the request is satisfied. This is
powerful and dangerous in equal measure. The safeguards are not optional:

- **Allowlist.** The agent may only invoke tools on an explicit list; a model
  that "decides" to call something else is refused by the dispatcher, not the
  model.
- **Approval gate.** Any tool that changes state pauses for human confirmation
  before it runs.
- **Validation.** A change the agent proposes goes through the same
  plan/validate/test path as any other change.

The model chooses; the deterministic code decides what is allowed to happen.

## Design Considerations

### Keep the model outside the trust boundary

Treat model output the way Chapter 04 treats a webhook payload: untrusted input
that must be validated before it drives an action. A tool result the model
summarizes, a config snippet it drafts, a command it suggests — each crosses
back into the trusted, deterministic world only through a gate.

### Redact before you send

Context sent to a model is the leak surface. Strip secrets (passwords, keys,
SNMP communities, tokens) and, where policy requires, addresses and hostnames,
*before* building the prompt. A redaction step is cheaper than a disclosure.

### Prompt injection travels through your source of truth

Chapter 04's source-of-truth pattern becomes an attack surface once an agent
reads it: text in a device description or a ticket field ("ignore previous
instructions and …") can hijack an agent that feeds that field into a model.
Data read from the network is not a trusted instruction — segregate retrieved
content from the agent's own instructions, and never let retrieved text expand
the agent's tool permissions.

### Evaluate accuracy as a measured property

"The AI suggested it" is not a validation. An AI recommendation is evaluated
the same way a change is: against a ground-truth expectation, with a pass/fail
metric you can report. If a recommendation cannot be checked against a test,
it cannot be trusted into production.

## Implementation and Automation

### Validating AI-generated code before it runs

Generated code enters the repository through the same gate as any other code.
A first, cheap gate is a compile/syntax check:

```bash
# An AI assistant drafted this device-facts helper. Validate before trusting it.
cat > ai_suggested.py <<'EOF'
def parse_version(show_version_output):
    for line in show_version_output.splitlines():
        if "Version" in line:
            return line.split("Version")[1].strip().split(",")[0]
    return None
EOF
python3 -m py_compile ai_suggested.py && echo "syntax OK -> proceed to lint + unit test"
```

A compile pass only proves the code parses; it says nothing about correctness.
The next gates are the linters and unit tests from Chapters 03 and 05, now
applied to code no human wrote line by line.

### A read-only MCP server with FastMCP

The following server exposes a single read-only tool that returns device facts
from a local source of truth. Its type hints define the tool schema; there is
deliberately no tool that changes device state.

```python
# netinfo_server.py — read-only network information for an AI agent
from fastmcp import FastMCP

mcp = FastMCP("netinfo")

# Stand-in source of truth; in production this reads NetBox/Nautobot or a RESTCONF GET.
_INVENTORY = {
    "core1": {"platform": "iosxe", "mgmt_ip": "192.0.2.1", "role": "core"},
    "edge1": {"platform": "iosxr", "mgmt_ip": "192.0.2.9", "role": "edge"},
}

@mcp.tool()
def get_device_facts(hostname: str) -> dict:
    """Return read-only facts for a device from the source of truth."""
    return _INVENTORY.get(hostname, {"error": f"unknown device: {hostname}"})

if __name__ == "__main__":
    mcp.run()
```

### A guarded conversational agent

The agent maps a natural-language request to a tool call. The model is a
pluggable function — here a deterministic stub so the lab runs with no API key
— and the dispatcher enforces an allowlist and an approval gate. Swapping the
stub for a real LLM client changes nothing about the safety machinery.

```python
# agent.py — LLM selects a tool; deterministic code decides what may run
import json

def call_model(request: str) -> dict:
    # Stub for a real LLM call. A production model returns a structured tool call.
    if "facts" in request or "version" in request:
        return {"tool": "get_device_facts", "args": {"hostname": "core1"}}
    return {"tool": "reload_device", "args": {"hostname": "core1"}}  # tests the guardrail

READ_ONLY = {"get_device_facts"}

def get_device_facts(hostname): return {"hostname": hostname, "platform": "iosxe"}

def dispatch(call: dict, approver=lambda c: False) -> dict:
    tool = call["tool"]
    if tool not in READ_ONLY:                       # allowlist + approval gate
        if not approver(call):
            return {"refused": tool, "reason": "write tool without approval"}
    return {"tool": tool, "result": get_device_facts(**call["args"])}

if __name__ == "__main__":
    print(json.dumps(dispatch(call_model("get device facts")), indent=2))
```

### Evaluating an AI recommendation

An AI recommendation is scored against a ground-truth expectation, producing a
metric you can gate on:

```python
# evaluate.py — score AI-recommended ACL lines against expected policy
recommended = ["permit tcp any host 192.0.2.10 eq 443",
               "permit tcp any host 192.0.2.10 eq 80"]      # AI also allowed cleartext 80
expected    = {"permit tcp any host 192.0.2.10 eq 443"}

correct = [r for r in recommended if r in expected]
accuracy = len(correct) / len(recommended)
print(f"accuracy: {accuracy:.0%}  extra/incorrect: {sorted(set(recommended) - expected)}")
assert accuracy == 1.0, "AI recommendation failed policy evaluation — do not apply"
```

## Validation and Troubleshooting

- **Non-determinism looks like a flaky pipeline.** If an AI-assisted step
  passes and fails on identical input, that is the model's variance, not a race
  condition — pin the deterministic validators downstream so the gate result is
  stable even when the model's draft is not.
- **A tool the model "can't find"** is usually a schema problem: an untyped
  FastMCP argument produces a weak schema the agent cannot call reliably. Add
  the type hint.
- **An agent that does the wrong thing** is contained by the dispatcher, not
  debugged in the model. Assert on refusals in tests: a write tool reached
  without approval must return a refusal, every time.

## Security and Best Practices

- **Redact context before it leaves the boundary.** No secrets, and — per
  policy — no addresses or hostnames, in a prompt to a hosted model.
- **Split read from write.** Expose read-only tools freely; gate every
  state-changing tool behind explicit human approval.
- **Treat retrieved data as untrusted.** Content read from the network or a
  ticket is data, never an instruction; guard against prompt injection through
  the source of truth.
- **Validate everything generated.** AI output passes the same linters,
  syntax checks, and tests as human code before it merges or runs.
- **Own the policy.** Settle data-privacy and IP-ownership rules for model use
  before AI output reaches a production repository.

## References and Knowledge Checks

### References

- AUTOCOR 350-901 v2.0, *Designing, Deploying and Managing Network Automation
  Systems*, domain 4.0 "AI in Automation" — Cisco Learning &
  Certifications exam topics.
- *CCIE Practical Exam Format with AI Deploy, Operate, and Optimize (AI DOO)
  Module* — Cisco Learning Network (article 000010877).
- Model Context Protocol specification and the FastMCP framework documentation.

### Knowledge Checks

- Why is model output treated as untrusted input rather than trusted code?
- What is the read/write split in an MCP server, and why does a write tool need
  an approval gate a read tool does not?
- How does prompt injection reach an automation agent through a source of
  truth, and what stops it?
- What does it mean to *evaluate* an AI recommendation, and why is "the AI
  suggested it" not a validation?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each skill in the
AUTOCOR 350-901 v2.0 "AI in Automation" domain (4.1–4.5)** — AI-assisted code
validation, security risks, an MCP server, a conversational agent, and
evaluating AI recommendations. The labs are deterministic and need **no LLM API
key**: the model is stubbed so the safety machinery is what you exercise. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 10.1–10.5** — `python3`, and for Lab 10.3
`pip install fastmcp`. **Cost:** none (no paid API calls).

### Lab 10.1 — Validate AI-assisted code before it runs (Topic: AI-assisted development)

**Objective:** Gate AI-generated code through a syntax check before trusting it.

```bash
cat > ai_suggested.py <<'EOF'
def parse_version(text):
    for line in text.splitlines():
        if "Version" in line:
            return line.split("Version")[1].strip().split(",")[0]
    return None
EOF
python3 -m py_compile ai_suggested.py && echo "syntax OK -> lint + unit test next"
```

**Expected result:** the compile check passes and prints the go-ahead — AI
output is plausible, not proven; it enters the repo only through the same
validation gates (syntax, lint, tests) as human-written code, because a model
can invent an argument or keyword that does not exist.

**Negative test:** apply an AI-suggested snippet straight to a device without
any check; a hallucinated command or argument fails at runtime — validation
before execution is exactly what makes AI assistance safe.

**Cleanup:** `rm -f ai_suggested.py`.

### Lab 10.2 — Security risks in AI-based automation (Topic: AI security risks)

**Objective:** Redact secrets from context before it reaches a model.

```bash
cat > running_config.txt <<'EOF'
hostname edge1
snmp-server community S3cr3t-RO RO
username admin secret 0 P@ssw0rd
EOF
python3 - <<'EOF'
import re
ctx = open("running_config.txt").read()
redacted = re.sub(r'(community|secret \d)\s+\S+', r'\1 <REDACTED>', ctx)
print(redacted)
assert "S3cr3t" not in redacted and "P@ssw0rd" not in redacted, "secret leaked to model context!"
print("safe to send to model")
EOF
```

**Expected result:** the community string and password are replaced with
`<REDACTED>` and the assertion passes — context sent to a hosted model is the
leak surface, so secrets are stripped before the prompt is built; sending a raw
running-config to an external LLM discloses credentials outside the trust
boundary.

**Negative test:** feed the raw config to the model unredacted; the secrets
leave your administrative boundary — redaction, not trust in the provider, is
the control.

**Cleanup:** `rm -f running_config.txt`.

### Lab 10.3 — An MCP server with FastMCP (Topic: MCP server for an AI agent)

**Objective:** Expose read-only device facts to an agent and list the tool.

```bash
cat > netinfo_server.py <<'EOF'
from fastmcp import FastMCP
mcp = FastMCP("netinfo")

_INVENTORY = {"core1": {"platform": "iosxe", "role": "core"}}

@mcp.tool()
def get_device_facts(hostname: str) -> dict:
    """Return read-only facts for a device."""
    return _INVENTORY.get(hostname, {"error": "unknown device"})
EOF
python3 - <<'EOF'
import asyncio
from fastmcp import Client
from netinfo_server import mcp

async def main():
    async with Client(mcp) as c:
        tools = [t.name for t in await c.list_tools()]
        print("tools:", tools)
        res = await c.call_tool("get_device_facts", {"hostname": "core1"})
        print("call:", res.data)

asyncio.run(main())
EOF
```

**Expected result:** the tool list contains `get_device_facts` and the call
returns the device facts — an MCP server advertises typed tools an agent can
discover and call; the type hints become the tool schema, and grounding the
model in real, tool-returned state is what makes AIOps accurate rather than
guessed.

**Negative test:** add a `reload_device` write tool to the same server with no
approval gate; a probabilistic caller can now reload a device — read tools are
safe to expose, but write tools must sit behind an explicit approval gate.

**Cleanup:** `rm -f netinfo_server.py`.

### Lab 10.4 — A guarded conversational agent (Topic: LLM conversational agent)

**Objective:** Let a model pick a tool while the dispatcher enforces safety.

```bash
python3 - <<'EOF'
def call_model(request):                       # stub LLM: returns a structured tool call
    return {"tool": "get_device_facts", "args": {"hostname": "core1"}}

READ_ONLY = {"get_device_facts"}
def get_device_facts(hostname): return {"hostname": hostname, "platform": "iosxe"}

def dispatch(call, approver=lambda c: False):
    if call["tool"] not in READ_ONLY and not approver(call):
        return {"refused": call["tool"], "reason": "write tool without approval"}
    return {"tool": call["tool"], "result": get_device_facts(**call["args"])}

print(dispatch(call_model("show me core1 facts")))
print(dispatch({"tool": "reload_device", "args": {"hostname": "core1"}}))
EOF
```

**Expected result:** the read request returns facts and the unapproved
`reload_device` call is refused — in the agentic loop the model *chooses* a tool
but deterministic code *decides* what may run: an allowlist plus an approval
gate keeps a probabilistic caller from taking an irreversible action.

**Negative test:** remove the allowlist/approval check and let the agent execute
whatever the model returns; a hallucinated or injected `reload_device` runs —
the guardrail, not the model's good behavior, is the safety boundary.

**Cleanup:** none.

### Lab 10.5 — Evaluate AI recommendation accuracy (Topic: Evaluating AI recommendations)

**Objective:** Score an AI recommendation against ground truth before applying.

```bash
python3 - <<'EOF'
recommended = ["permit tcp any host 192.0.2.10 eq 443",
               "permit tcp any host 192.0.2.10 eq 80"]   # AI also allowed cleartext 80
expected = {"permit tcp any host 192.0.2.10 eq 443"}

correct = [r for r in recommended if r in expected]
accuracy = len(correct) / len(recommended)
print(f"accuracy: {accuracy:.0%}  extra: {sorted(set(recommended) - expected)}")
assert accuracy == 1.0, "AI recommendation failed policy evaluation - do not apply"
EOF
```

**Expected result:** the script reports `accuracy: 50%`, flags the extra
cleartext-port rule, and the assertion **fails** — which is the point: the AI
recommendation is measured against expected policy and rejected because it
over-permits, so an evaluation harness catches an unsafe suggestion before it
reaches a device.

**Negative test:** accept the recommendation because "the AI suggested it,"
with no evaluation; the cleartext rule ships — a measured accuracy metric
against ground truth is what turns a suggestion into a validated change.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

AI enters network automation as a probabilistic assistant, never as an
unsupervised author or actor. The benefits — faster scaffolding, natural-
language operation, tool-grounded answers — are real, but each arrives with a
specific control: redact context before it leaves the boundary, split read
tools from gated write tools, treat retrieved data as untrusted input against
prompt injection, validate every generated line through the pipeline from
Chapters 03 and 05, and evaluate recommendations against ground truth before
they ship. Those controls are exactly what Cisco now tests in the Automation
track — the **AI in Automation** domain of the AUTOCOR 350-901 v2.0 written
exam, and the **AI Deploy, Operate, and Optimize (AI DOO)** module joining the
CCIE Automation practical — and they are the deterministic machinery that lets
a non-deterministic component be used safely.

- [ ] Can explain why AI output is validated through the existing pipeline
      rather than trusted on generation.
- [ ] Has built a read-only FastMCP server and listed/called its tool.
- [ ] Has run an agent whose dispatcher refuses an unapproved write tool.
- [ ] Has evaluated an AI recommendation against ground truth and rejected an
      over-permissive one.
