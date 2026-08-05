# Chapter 07: Identity Orchestration — PingOne DaVinci

## Learning Objectives

- Explain identity orchestration and the problem it solves.
- Understand no-code flows and connectors.
- Place orchestration as the glue across a multi-vendor identity estate.
- Recognize how orchestration balances security and user experience.

*Cert relevance: PingOne DaVinci is the **orchestration** certification (68% pass mark) — flows, connectors, and identity journeys.*

## The orchestration problem

A real identity experience is rarely one step. A single login journey might: check the user's risk ([Chapter 6](06-mfa-passwordless-and-threat-protection.md)), branch to MFA if risky, look up the user in a directory, call a fraud API, provision an account if new, send a verification email, and finally issue a token. Wiring this together in custom code is slow, brittle, and hard to change — and it hard-codes the journey so that a small policy change means a development cycle.

**PingOne DaVinci** is Ping's **identity orchestration** product: a **no-code** environment for designing these journeys as visual **flows**. You drag and connect steps — decisions, MFA challenges, directory lookups, API calls, account creation — into a flow that runs the journey, without writing code. It is to identity journeys what a flowchart is to a process: the logic is visible, editable, and changeable without a redeploy.

## Flows and connectors

Two concepts:

- A **flow** is the visual journey — a graph of steps and decision branches describing how a user moves from arrival to authenticated (or rejected). Flows can branch on risk, user type, or any signal, so one flow handles many cases.
- **Connectors** are the integrations a flow calls — to PingFederate, PingOne MFA, a directory, a fraud service, an email provider, a CRM, or *third-party* systems. Connectors are what let a flow orchestrate across the **whole identity estate**, not just Ping products.

This is orchestration's real power: identity environments are **multi-vendor** (a Ping federation server, a Microsoft directory, a third-party fraud tool, a homegrown app), and DaVinci **glues them into one coherent journey** via connectors. The lab models a branching flow.

## Balancing security and experience

Orchestration is where the [security-versus-experience balance (Chapter 6)](06-mfa-passwordless-and-threat-protection.md) is actually *implemented*. The flow decides, per user and per risk, how much friction to apply: a returning low-risk customer glides through; a high-risk login is routed through MFA and fraud checks; a new user gets a registration sub-flow. Because it is no-code, the security and experience teams can *tune the journey directly* — adjusting where friction lands without a development cycle. Orchestration turns identity policy from hard-coded logic into an editable flow. The lab models the branching.

## Hands-On Lab

Python models an identity orchestration flow. **Cost:** none.

### Lab 7.1 — A branching identity flow

**Objective:** Route users through a journey that adapts to risk and type.

```bash
python3 - <<'EOF'
# a DaVinci-style flow: steps + decision branches, per user
def run_flow(user):
    trace = ["START: user arrives"]
    # step: known user?
    if user["new"]:
        trace.append("BRANCH new user -> registration sub-flow (create account, verify email)")
    else:
        trace.append("directory lookup -> existing user found")
    # step: risk check (connector: PingOne Protect)
    risk = user["risk"]
    trace.append(f"connector PingOne Protect -> risk = {risk}")
    if risk >= 50:
        trace.append("BRANCH high risk -> STEP UP: MFA challenge (connector PingID)")
        if not user["passes_mfa"]:
            trace.append("MFA failed -> DENY")
            return trace
    elif risk >= 25:
        trace.append("BRANCH medium risk -> lightweight MFA (push)")
    else:
        trace.append("low risk -> no step-up (smooth)")
    # step: issue token
    trace.append("issue token (connector PingFederate) -> ACCESS GRANTED")
    return trace

USERS = [
  ("returning, low risk",  {"new": False, "risk": 10, "passes_mfa": True}),
  ("returning, high risk",  {"new": False, "risk": 70, "passes_mfa": True}),
  ("new customer",          {"new": True,  "risk": 20, "passes_mfa": True}),
  ("takeover attempt",      {"new": False, "risk": 80, "passes_mfa": False}),
]
for label, user in USERS:
    print(f"=== {label} ===")
    for step in run_flow(user):
        print(f"   {step}")
    print()
print("ONE flow, MANY journeys — it BRANCHES on user type and risk:")
print("  returning low-risk -> glides straight through (no friction)")
print("  returning high-risk -> stepped up to MFA before a token is issued")
print("  new customer -> routed through a registration sub-flow first")
print("  takeover attempt (high risk, fails MFA) -> DENIED at the MFA gate")
print("\nEach external step is a CONNECTOR (PingOne Protect for risk, PingID for MFA,")
print("PingFederate for the token) — and connectors can call THIRD-PARTY systems too,")
print("so one flow orchestrates a multi-vendor identity estate. And it's NO-CODE: the")
print("security/UX teams edit this flow directly — move the MFA branch, add a fraud")
print("check, change the risk threshold — WITHOUT a development cycle. That's what")
print("DaVinci is: identity policy as an editable flow, not hard-coded logic.")
EOF
```

**Expected result:** One flow branching by user type and risk — low-risk returning users gliding through, high-risk stepped up to MFA, new users routed to registration, and a failed-MFA takeover denied — with each external step a connector. The orchestration lesson is that DaVinci expresses identity journeys as no-code, branching flows glued across a multi-vendor estate by connectors, editable directly by security and UX teams without a development cycle.

**Negative test:** Hard-coding the identity journey in custom application code. Every policy change (move the MFA step, add a fraud check) becomes a development cycle, and the logic is invisible and brittle — a no-code flow makes the journey editable and visible.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Identity orchestration understood as designing multi-step identity journeys without custom code.
- [ ] Flows (visual branching journeys) and connectors (integrations, including third-party) understood.
- [ ] Orchestration recognized as the glue across a multi-vendor identity estate.
- [ ] The security-versus-experience balance seen as implemented in editable, branching flows.
