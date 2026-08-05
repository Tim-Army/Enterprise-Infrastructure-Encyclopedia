# Chapter 06: MFA, Passwordless, and Threat Protection

## Learning Objectives

- Explain multi-factor authentication and its factor types.
- Understand passwordless authentication and why it is more secure.
- Describe adaptive (risk-based) authentication.
- Place PingOne Protect for threat and fraud detection.

*Cert relevance: MFA, passwordless, and adaptive auth (PingID, PingOne MFA, PingOne Protect) run through the PingOne certifications.*

## Multi-factor authentication

A password alone is weak — phished, guessed, reused, breached. **Multi-factor authentication (MFA)** requires **two or more** factors from different categories:

| Factor category | Is | Examples |
|:---|:---|:---|
| **Something you know** | Knowledge | Password, PIN |
| **Something you have** | Possession | Phone (push, OTP), security key |
| **Something you are** | Inherence | Fingerprint, face |

The strength comes from **combining categories**: an attacker who phishes your password (know) still lacks your phone (have). **PingID** is Ping's MFA product, supporting push notifications, one-time passcodes, biometrics, and FIDO2 security keys. Requiring a second factor blocks the overwhelming majority of account-takeover attacks that rely on a stolen password alone. The lab quantifies this.

## Passwordless

**Passwordless** authentication removes the password entirely, replacing it with stronger factors — a **FIDO2/WebAuthn** security key or platform authenticator (Touch ID, Windows Hello), or a phone-based cryptographic credential. It is **more secure *and* more usable**, which is rare: there is no password to phish, reuse, or breach, and the user just taps a key or their fingerprint.

Passwordless (especially FIDO2) is **phishing-resistant** by design — the credential is cryptographically bound to the specific website, so a fake login page cannot capture anything reusable. This is where identity is heading, and Ping supports it. The lab contrasts phishing resistance.

## Adaptive (risk-based) authentication

The smartest layer is **adaptive authentication** — adjusting the authentication requirement based on **risk signals**. Not every login is equally risky: a user on their usual device, from their usual location, at a normal hour is low-risk; the same account from a new country, a new device, at 3 a.m. is high-risk. Adaptive auth **steps up** the challenge for risky logins (require MFA, or block) while letting low-risk logins through with less friction.

**PingOne Protect** is Ping's threat-protection product — it scores each authentication for **risk and fraud** using signals (device, location, velocity, behavioral anomalies, known-bad indicators) and feeds that risk into the auth decision. This balances **security and experience**: friction where it is warranted, smoothness where it is safe — the same [risk-based prioritization](../../volume-147-wiz-certifications/chapters/03-attack-paths-and-toxic-combinations.md) philosophy the security shelf teaches, applied to login. The lab models risk scoring.

## Hands-On Lab

Python models authentication security. **Cost:** none.

### Lab 6.1 — Adaptive step-up by risk score

**Objective:** Require more assurance for riskier logins, less for safe ones.

```bash
python3 - <<'EOF'
LOGINS = [
  # user,   known_device, usual_location, odd_hour, impossible_travel
  ("alice", True,  True,  False, False),   # normal -> low risk
  ("bob",   False, True,  False, False),   # new device -> medium
  ("carol", False, False, True,  False),   # new device + new place + 3am -> high
  ("dave",  True,  False, False, True),    # impossible travel -> high (account takeover?)
  ("erin",  True,  True,  True,  False),   # usual device/place, just late -> low-ish
]
def risk(known_dev, usual_loc, odd_hour, imposs_travel):
    score = 0
    if not known_dev:  score += 30
    if not usual_loc:  score += 25
    if odd_hour:       score += 10
    if imposs_travel:  score += 50   # strong takeover signal
    return score
def decision(score):
    if score >= 50: return "STEP UP: require MFA (or BLOCK) — high risk"
    if score >= 25: return "STEP UP: require MFA — medium risk"
    return "ALLOW with password/session — low risk, low friction"

print(f"{'user':7}{'risk':>6}   decision")
for user, kd, ul, oh, it in LOGINS:
    s = risk(kd, ul, oh, it)
    print(f"{user:7}{s:>6}   {decision(s)}")
print("\nAdaptive auth adjusts the CHALLENGE to the RISK:")
print("  alice (known device, usual place, normal hour) -> low risk -> smooth login.")
print("  carol (new device + new location + 3am) -> high risk -> STEP UP to MFA.")
print("  dave (impossible travel — logged in from two continents an hour apart) ->")
print("       high risk even on a KNOWN device: a strong account-takeover signal.")
print("\nThe balance: friction WHERE WARRANTED, smoothness WHERE SAFE. Forcing MFA on")
print("every login annoys users; never forcing it is insecure. PingOne Protect scores")
print("each login on signals (device, location, velocity, anomalies) and feeds the risk")
print("into the decision — step up the risky ones, let the safe ones flow. Same risk-")
print("based philosophy as the security shelf (prioritize by real risk), applied to the")
print("front door. Security AND experience, instead of trading one for the other.")
EOF
```

**Expected result:** Low-risk logins allowed with low friction and high-risk ones (new device plus new location plus odd hour, or impossible travel) stepped up to MFA or blocked, scored from signals. The adaptive lesson is to match the authentication challenge to the risk — friction where warranted, smoothness where safe — which PingOne Protect enables by scoring each login, balancing security and experience instead of trading one for the other.

**Negative test:** Requiring the same authentication for every login. Forcing MFA always annoys users into workarounds; never stepping up lets an impossible-travel takeover through — adaptive, risk-scored auth applies friction only where the signals warrant it.

**Cleanup:** None.

### Lab 6.2 — Why MFA and passwordless beat passwords

**Objective:** Quantify how a second factor and phishing resistance cut account takeover.

```bash
python3 - <<'EOF'
ATTEMPTS = 10000   # credential-stuffing / phishing attempts against accounts
print(f"{ATTEMPTS} account-takeover attempts (stolen/phished passwords):\n")

# password only: a valid stolen password = access
pw_success = int(ATTEMPTS * 0.03)   # 3% of stolen creds still valid & land
print("PASSWORD ONLY:")
print(f"   ~{pw_success} attempts succeed — a valid stolen password IS access.\n")

# password + MFA: attacker also needs the second factor
mfa_success = int(pw_success * 0.02)   # ~98% blocked lacking the 2nd factor
print("PASSWORD + MFA (PingID):")
print(f"   attacker has the password but NOT the phone/key -> ~{mfa_success} succeed")
print(f"   ({pw_success - mfa_success} blocked by the second factor)\n")

# passwordless FIDO2: phishing-resistant, nothing reusable to steal
print("PASSWORDLESS (FIDO2/WebAuthn):")
print("   there's no password to steal or phish; the credential is cryptographically")
print("   bound to the real site -> a fake login page captures NOTHING reusable")
print(f"   phishing-based takeovers: ~0\n")
print("The progression:")
print("  password only -> a stolen password is a breach.")
print("  + MFA -> the attacker needs the SECOND factor too; ~98% of stolen-password")
print("     attacks are blocked. Huge, cheap win.")
print("  passwordless FIDO2 -> removes the phishable secret ENTIRELY and binds the")
print("     credential to the real domain, so phishing captures nothing. More secure")
print("     AND more usable (tap a key / fingerprint — no password to remember).")
print("\nThis is why Ping (PingID, PingOne MFA, passwordless) pushes beyond passwords:")
print("the password is the weakest link, MFA patches most of it, and passwordless")
print("removes the link. Identity's direction of travel.")
EOF
```

**Expected result:** Stolen passwords succeeding on a password-only system, ~98% blocked when MFA adds a second factor, and phishing-based takeovers reduced to near zero with phishing-resistant passwordless FIDO2. The lesson is the security progression — a password alone is a breach when stolen, MFA blocks most stolen-password attacks cheaply, and passwordless removes the phishable secret entirely while improving usability.

**Negative test:** Relying on password complexity rules alone. A complex password, once phished or breached, is still a valid credential; only a second factor (MFA) or removing the password (passwordless) stops the stolen-credential attack.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] MFA understood as combining factors from different categories, blocking most stolen-password attacks.
- [ ] Passwordless understood as more secure and more usable — phishing-resistant FIDO2 with no password to steal.
- [ ] Adaptive (risk-based) authentication understood as stepping up challenge by risk signals.
- [ ] PingOne Protect placed as the threat/fraud scoring that feeds risk into the authentication decision.
