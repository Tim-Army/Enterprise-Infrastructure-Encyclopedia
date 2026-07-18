# Chapter 08: Data Security, Cryptography, Privacy, and Ransomware Resilience

## Learning Objectives

- Apply data classification to drive encryption, access, and retention
  decisions rather than treating all data identically.
- Explain symmetric and asymmetric cryptography, envelope encryption, and
  key management architecture, including the role of an HSM/KMS.
- Design a secrets management approach that eliminates static,
  long-lived credentials from application and infrastructure
  configuration.
- Apply privacy-engineering principles — data minimization, purpose
  limitation, and data subject rights — as design constraints, not
  after-the-fact compliance checks.
- Explain the ransomware kill chain from a defender's perspective and
  design backup and recovery architecture resilient to it.
- Build and test a working envelope-encryption workflow, including a
  negative test that detects tampered ciphertext.

## Theory and Architecture

### Data classification as the foundation

Every control in this chapter — encryption strength, key management
rigor, DLP scope, backup immutability — should be calibrated by **data
classification**, not applied uniformly. A typical classification scheme:

| Classification | Example data | Baseline control expectation |
| --- | --- | --- |
| Public | Marketing materials, published documentation | Integrity protection only |
| Internal | Internal wikis, non-sensitive operational data | Access control, standard backup |
| Confidential | Financial forecasts, internal strategy, source code | Encryption at rest/in transit, DLP monitoring, restricted access |
| Restricted / Regulated | Cardholder data, PHI, PII, authentication secrets | Strong encryption, HSM/KMS-backed keys, strict least-privilege access, audit logging, regulatory retention rules |

Classification should be assigned at data creation (or ingestion) time and
carried as metadata through storage, processing, and transmission, so
downstream systems (DLP, backup, access control) can apply
classification-appropriate controls automatically rather than requiring
manual per-system judgment. This directly extends the regulatory
obligations register from Chapter 1 — a classification of "Restricted"
should programmatically imply which regulations apply and which controls
are mandatory.

### Cryptography fundamentals

- **Symmetric encryption** (AES-256-GCM being the current enterprise
  standard) uses one key for both encryption and decryption — fast, and
  well suited to bulk data encryption, but requires the key to be shared
  or derived by every legitimate party, creating a key-distribution
  problem.
- **Asymmetric encryption** (RSA, and increasingly elliptic-curve schemes
  such as ECDSA/Ed25519) uses a mathematically related public/private key
  pair — the public key can be shared openly, while only the private key
  can decrypt or sign. Asymmetric cryptography is computationally
  expensive relative to symmetric, so it is typically used to establish
  or exchange a symmetric session key rather than to encrypt bulk data
  directly — the pattern TLS 1.3 itself follows.
- **TLS 1.3** is the current baseline for encryption in transit,
  simplifying the handshake and removing legacy, weaker cipher suites
  supported in TLS 1.2. Systems still negotiating TLS 1.0/1.1 or weak
  cipher suites should be treated as a hardening finding under the
  baseline established in Chapter 3.
- **Hashing** (SHA-256 and stronger) provides integrity verification, not
  encryption — a hash cannot be reversed to recover the original data,
  which is why chain-of-custody integrity checks in Chapter 7 use hashing
  rather than encryption.

### Envelope encryption and key management

**Envelope encryption** is the standard enterprise pattern for encrypting
data at rest at scale: a unique **data encryption key (DEK)** encrypts the
actual data (fast, symmetric operation), and the DEK itself is then
encrypted ("wrapped") by a **key encryption key (KEK)** held in a
centralized **Key Management Service (KMS)** or **Hardware Security
Module (HSM)**. Only the wrapped DEK is stored alongside the encrypted
data; the KEK never leaves the KMS/HSM boundary. This design means
revoking access, rotating the KEK, or auditing every decryption operation
happens centrally at the KMS, without re-encrypting the underlying bulk
data — critical at any scale where re-encrypting petabytes of data on
every key rotation would be operationally infeasible.

- **HSM** — a dedicated, tamper-resistant hardware device that generates
  and holds cryptographic keys, performing operations inside the device
  boundary so private key material is never exposed in plaintext to the
  host system. Used where regulatory or extreme-assurance requirements
  apply (payment processing, certificate authorities).
- **Cloud KMS** — a managed service providing similar centralized key
  control without dedicated hardware, commonly backed by an HSM at the
  provider layer. The customer-managed-key vs. provider-managed-key
  decision determines who controls key lifecycle and audit logging —
  customer-managed keys give the enterprise direct control (and direct
  responsibility) over rotation and revocation.
- **Key rotation** should be automated and scheduled, with the KMS
  handling re-wrapping of DEKs under a new KEK version without requiring
  bulk data re-encryption — the operational benefit envelope encryption
  is specifically designed to provide.

### PKI and certificate lifecycle

**Public Key Infrastructure (PKI)** is the trust hierarchy — root
certificate authority (CA), intermediate CAs, and issued end-entity
certificates — that binds a public key to a verified identity, underlying
both TLS and the certificate-based authentication mechanisms referenced
in Chapter 2 (FIDO2/WebAuthn credentials, mutual TLS for machine
identity). Certificate lifecycle management (issuance, renewal, and
timely revocation) is a common operational failure point: an expired
internal CA or leaf certificate causes outages, while a compromised
private key that is not promptly revoked remains a standing trust
liability. Automated certificate lifecycle tooling (ACME-based issuance
and renewal) has become standard practice specifically to eliminate
manual renewal as a recurring operational risk.

### Data loss prevention and secrets management

**Data Loss Prevention (DLP)** inspects data in motion (network egress),
at rest (file shares, cloud storage), and in use (endpoint clipboard,
removable media) for classification-matching content, enforcing policy
(block, quarantine, alert, encrypt) based on where restricted data is
attempting to move. DLP is most effective when driven by the
classification metadata described above rather than by pattern-matching
alone, since pattern-matching against unstructured content produces
significant false-positive volume without classification context to
narrow scope.

**Secrets management** extends the machine-identity principles from
Chapter 2 to the credentials, API keys, and certificates an application
needs at runtime: a centralized secrets vault issues short-lived,
scoped credentials to authenticated workloads rather than embedding
static secrets in configuration files or source code, and rotates
standing secrets (database passwords, third-party API keys) automatically
on a schedule. A static secret embedded in a configuration repository —
even a private one — should be treated as compromised the moment it is
committed, since repository history, backups, and access logs all
represent exposure surface that is difficult to fully remediate after
the fact.

### Privacy engineering

Privacy is a design constraint, not solely a legal compliance exercise:

- **Data minimization** — collect and retain only the data actually
  required for a defined purpose, reducing both breach impact and
  regulatory exposure by construction.
- **Purpose limitation** — data collected for one purpose should not be
  silently repurposed for another without a fresh legal basis and, where
  required, renewed consent.
- **Data Subject Requests (DSRs)** — GDPR, CCPA/CPRA, and similar
  regulations grant individuals rights to access, correct, or delete
  their data; fulfilling a deletion request requires the organization to
  actually know where every copy of that individual's data resides —
  which is only tractable if data classification and inventory (this
  chapter) and asset/data-flow inventory (Chapter 1) are maintained
  continuously, not reconstructed manually per request.
- **Privacy by design** — considering data minimization and purpose
  limitation during system design (the same SDLC stage as the STRIDE
  threat-modeling gate in Chapter 1), rather than retrofitting privacy
  controls after a system is already in production.

### The ransomware kill chain and resilience — a defender's view

Ransomware incidents typically follow a recognizable progression, useful
here strictly as a defensive planning framework for identifying where
controls from this volume interrupt the chain:

1. **Initial access** — commonly phishing, exposed remote access, or an
   unpatched internet-facing vulnerability (Chapters 2, 4, and 5
   collectively address this stage).
2. **Lateral movement and privilege escalation** — the compromised
   foothold is used to reach additional systems and elevate privilege,
   which network segmentation (Chapter 4) and JIT/PAM controls
   (Chapter 2) are specifically designed to contain.
3. **Data exfiltration** — increasingly performed *before* encryption, to
   support "double extortion" (threatening publication in addition to
   withholding decryption), making DLP and network egress monitoring
   (this chapter and Chapter 6) relevant defensive controls even against
   an attack whose final stage is encryption, not just theft.
4. **Encryption/detonation** — mass, rapid encryption of accessible data,
   including any backup targets reachable from the compromised
   environment.
5. **Extortion** — a ransom demand, frequently with a deadline and threat
   of data publication ("double extortion") or, increasingly, direct
   pressure on customers or regulators ("triple extortion").

**Ransomware resilience** is built primarily around ensuring stage four
cannot achieve its objective: recoverable, uncompromised backups make
the encryption stage survivable regardless of whether extortion is
attempted. The **3-2-1-1-0 backup rule** extends the traditional 3-2-1
rule (three copies, two different media types, one offsite) with one
immutable/air-gapped copy and zero verified recovery errors — the last
two additions exist specifically because ransomware operators
increasingly target reachable backup infrastructure directly, and an
unverified backup is not a proven recovery capability.

## Design Considerations

- **Customer-managed vs. provider-managed encryption keys.**
  Customer-managed keys give direct control over rotation, revocation, and
  audit logging, and can support a "crypto-shredding" data-destruction
  pattern (destroying the key renders the data permanently unrecoverable
  without deleting the bulk data itself) — valuable for DSR deletion
  fulfillment at scale. This control comes with direct operational
  responsibility: losing the customer-managed key means losing the data
  irrecoverably, so key backup and access-recovery procedures require the
  same rigor as the break-glass patterns in Chapter 2.
- **DLP false-positive tuning cost.** An overly broad DLP policy
  generates high false-positive volume that erodes both user trust and
  security team attention, mirroring the alert-fatigue problem in
  Chapter 6. Scope DLP policy by classification and by the highest-risk
  egress channels first (email attachments, cloud storage uploads to
  unsanctioned destinations), expanding coverage incrementally.
- **Backup immutability vs. storage cost and recovery time.** Immutable,
  air-gapped backup copies cost more and can complicate rapid recovery
  compared to always-online replicas. Calibrate the immutable-copy
  retention window and recovery time objective (RTO) to the
  organization's actual ransomware risk tolerance, documented alongside
  the risk register from Chapter 1, rather than defaulting to either
  extreme.
- **Backup infrastructure credential segregation.** Backup infrastructure
  that is reachable and administrable using the same domain credentials
  as production is a common ransomware failure mode — if a domain
  administrator account is compromised, the backups are compromised too.
  Segregate backup administration credentials and, where feasible,
  authentication domain from production identity, consistent with the
  Tier 0 infrastructure treatment described in Chapter 2.
- **Ransom payment is a business and legal decision, not a technical
  one**, and carries its own regulatory and sanctions-related
  considerations depending on jurisdiction and the payee. This volume
  does not provide payment guidance; the relevant design decision for
  security architecture is ensuring the organization is never
  operationally forced into that decision by an absence of viable backup
  recovery.
- **DSR fulfillment architecture.** Building the ability to locate and
  act on a single individual's data across every system, after the fact
  and under regulatory deadline, is far more expensive than designing
  data flows with DSR fulfillment in mind from the start — an
  architecture decision that belongs in the SDLC privacy-by-design review
  alongside STRIDE threat modeling (Chapter 1).

## Implementation and Automation

### Envelope encryption workflow (illustrative KMS pattern)

```text
# Conceptual envelope encryption flow (vendor-neutral)
1. Application requests a data encryption key (DEK) from the KMS.
2. KMS generates a random DEK, returns it in plaintext AND wrapped
   (encrypted by the KEK, which never leaves the KMS).
3. Application encrypts the data locally using the plaintext DEK,
   then discards the plaintext DEK from memory.
4. Application stores the encrypted data alongside the WRAPPED DEK only.
5. To decrypt later, the application sends the wrapped DEK back to the
   KMS, which unwraps it (using the KEK) and returns the plaintext DEK.
```

### Data classification tagging (structured metadata)

```yaml
# data-classification/customer-pii-store.yaml
data_store: customer-profile-service.pii-table
classification: restricted
regulatory_scope: [gdpr, ccpa]
encryption:
  at_rest: aes-256-gcm
  key_management: customer-managed-kms
  key_rotation_days: 90
dlp_policy: block-unencrypted-egress
retention_days: 730
dsr_fulfillment_owner: data-platform-team
```

### Working envelope encryption example (Python, `cryptography` library)

```python
#!/usr/bin/env python3
"""envelope_encrypt.py — illustrates envelope encryption locally using
AES-256-GCM for both the data key and a simulated key-encryption key.
AES-GCM's authentication tag is what allows the negative test below to
detect tampered ciphertext, not just decrypt-or-fail silently.

Usage:
  python3 envelope_encrypt.py encrypt <infile> <outfile.enc>
  python3 envelope_encrypt.py decrypt <infile.enc> <outfile>
"""
import os
import sys
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# In production, the KEK lives in a KMS/HSM and never leaves that
# boundary in unwrapped form. This lab simulates the KMS boundary with
# a local key file so separate encrypt/decrypt invocations share the
# same KEK, the same way separate calls to a real KMS API would.
KEK_PATH = "kek.local"


def load_or_create_kek() -> bytes:
    if os.path.exists(KEK_PATH):
        with open(KEK_PATH, "rb") as fh:
            return fh.read()
    kek = AESGCM.generate_key(bit_length=256)
    with open(KEK_PATH, "wb") as fh:
        fh.write(kek)
    os.chmod(KEK_PATH, 0o600)
    return kek


def encrypt(infile: str, outfile: str) -> None:
    kek = load_or_create_kek()
    dek = AESGCM.generate_key(bit_length=256)          # per-object data key
    data_aesgcm = AESGCM(dek)
    data_nonce = os.urandom(12)
    with open(infile, "rb") as fh:
        plaintext = fh.read()
    ciphertext = data_aesgcm.encrypt(data_nonce, plaintext, None)

    kek_aesgcm = AESGCM(kek)
    kek_nonce = os.urandom(12)
    wrapped_dek = kek_aesgcm.encrypt(kek_nonce, dek, None)

    envelope = {
        "data_nonce": base64.b64encode(data_nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "wrapped_dek": base64.b64encode(wrapped_dek).decode(),
        "kek_nonce": base64.b64encode(kek_nonce).decode(),
    }
    with open(outfile, "w", encoding="utf-8") as fh:
        json.dump(envelope, fh)
    print(f"Encrypted {infile} -> {outfile}")


def decrypt(infile: str, outfile: str) -> None:
    kek = load_or_create_kek()
    with open(infile, encoding="utf-8") as fh:
        envelope = json.load(fh)

    kek_aesgcm = AESGCM(kek)
    dek = kek_aesgcm.decrypt(
        base64.b64decode(envelope["kek_nonce"]),
        base64.b64decode(envelope["wrapped_dek"]),
        None,
    )
    data_aesgcm = AESGCM(dek)
    plaintext = data_aesgcm.decrypt(
        base64.b64decode(envelope["data_nonce"]),
        base64.b64decode(envelope["ciphertext"]),
        None,
    )
    with open(outfile, "wb") as fh:
        fh.write(plaintext)
    print(f"Decrypted {infile} -> {outfile}")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("encrypt", "decrypt"):
        raise SystemExit(__doc__)
    {"encrypt": encrypt, "decrypt": decrypt}[sys.argv[1]](sys.argv[2], sys.argv[3])
```

### Immutable backup configuration (object-lock pattern)

```bash
# Illustrative object-storage immutability configuration (vendor-neutral)
storage-cli bucket set-object-lock \
  --bucket backup-prod-immutable \
  --mode compliance \
  --retention-days 35

# Verify a specific backup object cannot be deleted or overwritten
# before its retention period expires, even by an account with
# otherwise-privileged delete permission
storage-cli object lock-status --bucket backup-prod-immutable --key nightly-2026-07-18.bak
```

## Validation and Troubleshooting

- **Validate encryption coverage, not just policy existence.** Confirm
  that data stores tagged "restricted" in the classification inventory
  are actually encrypted with the expected algorithm and key management
  backend — a classification tag with no enforced control behind it is
  the same shelfware-policy failure described in Chapter 1.
- **Common failure: DEK/KEK confusion in incident scoping.** During a
  key-compromise investigation, confirm precisely which key tier was
  exposed — a compromised DEK affects only the data it wrapped, while a
  compromised KEK potentially affects every DEK it has ever wrapped,
  requiring a much larger-scope response.
- **Common failure: backup restore never actually tested.** A backup
  that has never been restored is an unverified assumption, not a
  recovery capability — the "0" in the 3-2-1-1-0 rule specifically
  addresses this. Schedule regular, documented restore tests and treat a
  failed restore test as an incident-worthy finding, not routine
  maintenance noise.
- **Common failure: DLP policy silently disabled after a false-positive
  complaint.** Track DLP policy state changes as audited events; a
  policy quietly set to monitor-only after a business complaint, and
  never restored to enforcing, reintroduces the exposure the policy was
  meant to prevent.
- **Diagnosing certificate-related outages**: check certificate
  expiration first for any TLS handshake failure that appeared suddenly
  fleet-wide; automated ACME renewal failures are a common root cause and
  should themselves generate an alert well before expiration, not be
  discovered at the moment of failure.
- **Diagnosing failed DSR fulfillment**: if a deletion or access request
  cannot be completed within the regulatory window, the root cause is
  almost always an incomplete data inventory rather than a technical
  deletion failure — treat repeated DSR fulfillment difficulty as a
  signal to invest in the underlying data-flow inventory, not just the
  deletion tooling.

## Security and Best Practices

- Classify data at creation time and drive encryption, DLP, and
  retention controls from that classification programmatically, rather
  than relying on manual per-system judgment.
- Use envelope encryption with a centralized KMS/HSM for data at rest,
  and rotate keys on a defined schedule without requiring bulk
  re-encryption of underlying data.
- Eliminate static secrets from configuration and source code; issue
  short-lived, scoped credentials from a centralized secrets vault, and
  treat any committed static secret as compromised immediately upon
  discovery, requiring rotation rather than deletion from history alone.
- Maintain at least one immutable, air-gapped or logically isolated
  backup copy, with backup administration credentials segregated from
  production identity, and test restoration on a recurring, documented
  schedule.
- Apply data minimization and purpose limitation as SDLC design
  constraints, reviewed at the same design-proposal gate as STRIDE threat
  modeling in Chapter 1.
- Automate certificate issuance and renewal (ACME or equivalent) to
  eliminate manual renewal as a recurring outage and trust-liability
  risk.
- Maintain a current, continuously reconciled data-flow inventory
  specifically to support timely, accurate Data Subject Request
  fulfillment — do not treat DSR response as a one-off manual
  investigation each time a request arrives.

## References and Knowledge Checks

**References**

- NIST SP 800-57, *Recommendation for Key Management*
- NIST SP 800-111, *Guide to Storage Encryption Technologies for
  End User Devices*
- NIST SP 800-175B, *Guideline for Using Cryptographic Standards*
- CISA and partner agencies, *#StopRansomware Guide*
- Regulation (EU) 2016/679 (GDPR), Articles 5, 15–22, and 33
- CIS Controls v8.1, Control 3 (Data Protection) and Control 11
  (Data Recovery)

**Knowledge Checks**

1. Why does envelope encryption separate the data encryption key from
   the key encryption key, and what operational problem does that
   separation solve?
2. What is the practical difference between a customer-managed and a
   provider-managed encryption key, and what does crypto-shredding
   depend on?
3. Why is DLP more effective when driven by data classification metadata
   than by unstructured content pattern-matching alone?
4. At which stage of the ransomware kill chain does an immutable,
   air-gapped backup copy provide resilience, and why does that not
   depend on preventing earlier stages?
5. What does the "0" in the 3-2-1-1-0 backup rule require, and why is an
   untested backup not a proven recovery capability?
6. Why must backup administration credentials be segregated from
   production identity?

## Hands-On Lab

**Objective:** Implement and test a working envelope-encryption workflow,
confirming successful encrypt/decrypt round-trip and validating that
tampered ciphertext is detected and rejected rather than silently
decrypted incorrectly.

**Prerequisites**

- A workstation with Python 3.11 or later and the `cryptography` package
  installed (`pip install --user cryptography`).
- No production KMS or key material is required — this lab simulates the
  KEK locally for reproducibility.

**Steps**

1. Create a lab directory and a sample plaintext file:

   ```bash
   mkdir -p ~/labs/vol10-ch08 && cd ~/labs/vol10-ch08
   echo "customer record: restricted classification sample data" > record.txt
   ```

2. Save the `envelope_encrypt.py` script from the Implementation and
   Automation section into the same directory.

3. Encrypt the sample file:

   ```bash
   python3 envelope_encrypt.py encrypt record.txt record.enc
   ```

4. **Expected result:**
   `Encrypted record.txt -> record.enc` prints, and `record.enc` contains
   a JSON envelope with `data_nonce`, `ciphertext`, `wrapped_dek`, and
   `kek_nonce` fields:

   ```bash
   cat record.enc
   ```

5. Decrypt the file and confirm it matches the original:

   ```bash
   python3 envelope_encrypt.py decrypt record.enc record.decrypted.txt
   diff record.txt record.decrypted.txt && echo "MATCH: round-trip successful"
   ```

   **Expected result:** `MATCH: round-trip successful` prints, confirming
   the envelope-encryption round trip preserved the data exactly.

6. **Negative test:** Tamper with the ciphertext field in the encrypted
   envelope (simulating corruption or an attempted modification) and
   attempt to decrypt it:

   ```bash
   python3 - << 'EOF'
   import json
   with open("record.enc") as fh:
       envelope = json.load(fh)
   # Flip the last character of the ciphertext to simulate tampering
   envelope["ciphertext"] = envelope["ciphertext"][:-1] + (
       "A" if envelope["ciphertext"][-1] != "A" else "B"
   )
   with open("record.tampered.enc", "w") as fh:
       json.dump(envelope, fh)
   EOF
   python3 envelope_encrypt.py decrypt record.tampered.enc record.tampered.out.txt
   echo "exit=$?"
   ```

   **Expected result:** The script raises a
   `cryptography.exceptions.InvalidTag` exception and exits with a
   nonzero status — AES-GCM's authentication tag detects that the
   ciphertext was modified after encryption and refuses to produce
   output, rather than silently returning corrupted plaintext. This is
   the same tamper-evidence property, applied to encrypted data instead
   of a hash log, that the chain-of-custody tooling in Chapter 7 relies
   on for evidence integrity.

7. Confirm no `record.tampered.out.txt` file was written, since the
   decryption failed before any output was produced:

   ```bash
   ls record.tampered.out.txt 2>&1
   ```

   **Expected result:** `No such file or directory`, confirming the
   failure occurred before any (potentially corrupted) plaintext was
   written to disk.

**Cleanup**

```bash
cd ~ && rm -rf ~/labs/vol10-ch08
```

## Summary and Completion Checklist

This chapter covered data-centric protection: classification as the
driver for every downstream control, envelope encryption and centralized
key management, PKI and certificate lifecycle, DLP and secrets
management, privacy engineering as a design constraint, and the
ransomware kill chain viewed specifically to identify where each of this
volume's controls interrupts it — with backup immutability and tested
recovery as the resilience control that remains effective even if every
earlier stage succeeds for the adversary. The hands-on lab implemented a
real envelope-encryption workflow and proved, with a negative test using
AES-GCM's authentication tag, that tampered ciphertext is detected and
rejected rather than silently mis-decrypted.

- [ ] I can explain why data classification should drive encryption and
      DLP control selection rather than being applied uniformly.
- [ ] I can describe envelope encryption and why it separates the DEK
      from the KEK.
- [ ] I can explain the customer-managed vs. provider-managed key
      trade-off, including crypto-shredding.
- [ ] I can walk through the ransomware kill chain and name which
      control from this volume addresses each stage.
- [ ] I can explain the 3-2-1-1-0 backup rule and why untested backups
      are not a proven recovery capability.
- [ ] I implemented and tested an envelope-encryption workflow in the
      hands-on lab, including a negative test proving tampered
      ciphertext is rejected.
