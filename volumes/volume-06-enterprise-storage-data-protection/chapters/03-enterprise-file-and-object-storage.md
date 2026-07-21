# Chapter 3: Enterprise File and Object Storage

![Lab topology for this chapter: nfs-server01 exports /export/lab to nfs-client01 with the default, secure root_squash option; the client mounts the export and creates a file as root, and on the server that file is owned by the anonymous UID/GID (typically 65534, nobody/nogroup), confirming root-squash maps the client's root user to an unprivileged account. As a negative test, the export is changed to no_root_squash and reapplied; after remounting, the same root-created-file operation now produces a file genuinely owned by UID 0 on the server.](../../../diagrams/volume-06-enterprise-storage-data-protection/chapter-03-nfs-root-squash-topology.svg)

*Figure 3-1. Topology used throughout this chapter's Hands-On Lab: an NFS export's root-squash behavior proven positive, then reversed as a negative test.*

## Learning Objectives

- Compare NFS and SMB as enterprise file-sharing protocols, including their
  locking, permission, and versioning models.
- Explain distributed/scale-out file system architecture and how it differs
  from a single-head NAS filer.
- Describe object storage's flat namespace, metadata model, and consistency
  guarantees, and when object storage is preferable to file storage.
- Configure NFS exports and Samba shares with appropriate access controls.
- Write S3-compatible bucket policies and lifecycle rules for tiering and
  retention.
- Diagnose common file- and object-storage access, permission, and
  performance problems.

## Theory and Architecture

File and object storage both provide shared, multi-client access to data, but
they solve different problems. File storage preserves a hierarchical
namespace and POSIX-like (or CIFS-like) semantics that applications and users
expect from a traditional filesystem. Object storage abandons that hierarchy
in exchange for scale, durability, and an HTTP-native API that suits
distributed, cloud-native, and archival workloads.

### NFS

Network File System (NFS), now predominantly deployed as **NFSv4** (and
NFSv4.1/4.2 with parallel NFS extensions in scale-out platforms), is the
standard file-sharing protocol for Linux/Unix environments. Key
architectural points:

- NFSv4 is a single, stateful protocol (unlike NFSv3's separate mount,
  NLM lock, and NFS daemons) that integrates locking and uses a single TCP
  port (2049), simplifying firewall design.
- Access control combines traditional POSIX mode bits with optional NFSv4
  ACLs for finer-grained permission models.
- **root_squash** (the default) maps the remote root user to an unprivileged
  local account on the server, preventing a client's root user from having
  root privilege over the exported filesystem; **no_root_squash** disables
  this and should be reserved for tightly controlled cases (for example,
  specific virtualization or backup infrastructure that requires it).
- File locking uses NFSv4's lease-based state model, replacing the
  notoriously fragile NLM side-channel protocol used in NFSv3.

### SMB/CIFS

Server Message Block (SMB), now at version 3.x in current Windows and Samba
implementations, is the standard for Windows-centric file sharing and is
also widely used cross-platform via Samba on Linux.

- SMB 3.x adds **SMB signing** (integrity protection against tampering) and
  **SMB encryption** (confidentiality on the wire), both of which should be
  enabled for any share carrying sensitive data.
- SMB supports **opportunistic locks (oplocks)** and **leases** for
  client-side caching, improving perceived performance for typical
  office-document workloads.
- **Access-Based Enumeration (ABE)** hides files and folders a user has no
  permission to see, rather than showing them as access-denied — a usability
  and information-disclosure control.
- Windows **Previous Versions**/shadow-copy integration exposes
  filesystem-level snapshots ([Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)) directly to end users for
  self-service file recovery.

### Scale-out and distributed file systems

A single-head NAS filer — one (or one active/passive pair of) controller
serving a namespace from local or directly attached storage — is simple to
operate but scales only as far as that head's CPU, memory, and port
bandwidth allow, and represents a larger blast radius on failure. **Scale-out
file systems** distribute both the namespace metadata and the data itself
across a cluster of nodes, allowing capacity and performance to scale
roughly linearly by adding nodes, and confining a single node failure's
impact to a fraction of the overall namespace. This comes at the cost of
materially higher operational complexity: cluster membership, distributed
metadata consistency, and rebalancing after node addition/removal all
require operational attention that a single-head filer does not.

### Object storage

Object storage organizes data as **objects** — a blob of data plus
user-defined and system metadata plus a unique key — stored in a flat
namespace (commonly presented as **buckets** or **containers**) and accessed
through an HTTP-based REST API, most commonly using S3-compatible semantics
as the de facto industry API standard. Key architectural properties:

- **No in-place modification.** Objects are replaced wholesale, not edited;
  this immutability-by-default model is foundational to object storage's use
  as a backup and archive target and to features like object lock (Chapter
  8).
- **Erasure coding across nodes** (introduced in [Chapter 1](01-enterprise-storage-architecture-and-service-design.md)) is the default
  durability mechanism at scale, commonly delivering configurable "nines" of
  durability by spreading data and parity fragments across independent
  failure domains.
- **Eventual vs. strong consistency.** Early object stores offered only
  eventual consistency (a write might not be immediately visible to a
  subsequent read); most current platforms provide strong read-after-write
  consistency for new object PUTs, but architects should still verify the
  consistency model of the specific platform in use rather than assuming it.
- **Storage classes and lifecycle policies** let a bucket automatically
  transition objects from a hot/standard tier to progressively colder
  (and cheaper) tiers, and eventually expire them, based on object age —
  directly implementing the tiering concept from [Chapter 1](01-enterprise-storage-architecture-and-service-design.md) at the object
  layer.
- **Versioning** retains prior versions of an object on overwrite or delete,
  providing protection against accidental deletion and a building block for
  ransomware resilience ([Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md)).

### Choosing between file and object

| Consideration | File storage | Object storage |
| --- | --- | --- |
| Access pattern | POSIX/CIFS semantics, in-place edits, directory hierarchy | Whole-object PUT/GET, flat namespace, rich metadata |
| Client integration | Native OS mount (NFS/SMB) | HTTP/REST API, SDKs |
| Typical scale | Terabytes to low petabytes per namespace | Petabytes to exabytes |
| Consistency needs | Strong, POSIX-like locking | Application-tolerant of API-level consistency model |
| Best-fit workloads | Home directories, application config shares, general NAS | Backup targets, archives, unstructured/media data, cloud-native apps |

## Design Considerations

- **Namespace design.** Flat, wide export/share structures (many top-level
  shares with clear ownership) are easier to secure and delegate than deep,
  narrow hierarchies with permission inheritance sprawling across dozens of
  levels; design the namespace around organizational ownership boundaries,
  not just directory convenience.
- **Quota strategy.** Set both user/group and directory/project quotas where
  the platform supports it, and alert well before hard limits are reached —
  file-serving outages caused by quota exhaustion are common and entirely
  preventable with proactive monitoring ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md)).
- **Protocol selection and multiprotocol shares.** Where the same dataset
  must be served over both NFS and SMB, plan the permission-mapping strategy
  (POSIX-to-Windows ACL translation, user identity mapping) explicitly;
  multiprotocol access is one of the most common sources of confusing,
  hard-to-reproduce permission bugs.
- **Erasure coding width vs. fault domain** for object platforms: wider
  stripes (for example, 17+3 versus 10+2) improve capacity efficiency but
  require more nodes to participate in every read/rebuild and increase
  exposure to correlated failures; align stripe width to actual cluster size
  and rack/power fault domains, not just a vendor default.
- **Lifecycle policy design.** Model the expected access pattern (how
  quickly does data go cold) before setting lifecycle transition ages;
  transitioning too aggressively increases retrieval latency and, on
  platforms with tiered retrieval pricing or rehydration delay, retrieval
  cost/time for data that turns out to still be accessed occasionally.
- **Versioning and cost.** Object versioning is a strong protection against
  accidental overwrite/delete, but without a lifecycle policy to expire old
  versions it silently grows storage consumption; always pair versioning
  with a noncurrent-version expiration rule.
- **WORM and object lock** (introduced here, developed fully in [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md))
  should be a deliberate decision made at bucket-creation time on platforms
  where retention mode cannot be loosened after the fact — retrofitting
  compliance-mode object lock onto an existing bucket is often not possible.

## Implementation and Automation

### NFS export configuration

```bash
# /etc/exports on the NFS server
/export/engineering  10.20.30.0/24(rw,sync,root_squash,sec=sys)
/export/finance       10.20.31.0/24(rw,sync,root_squash,sec=krb5p)
/export/backup-stage  10.20.32.10(rw,sync,no_root_squash)   # backup infra only, explicitly scoped

# Apply the export table
sudo exportfs -ra
sudo exportfs -v          # verify active exports and their options
```

Note the deliberately narrow scope of the `no_root_squash` export: it is
limited to a single backup-infrastructure host address, not an entire
subnet, and is documented as an explicit, justified exception rather than a
default.

### Samba share configuration

```ini
# /etc/samba/smb.conf
[engineering]
  path = /export/engineering
  valid users = @engineering
  read only = no
  browseable = yes
  smb encrypt = required
  vfs objects = full_audit
  full_audit:success = mkdir rename unlink
  full_audit:failure = none
  full_audit:facility = local5
```

```bash
sudo testparm                 # validate syntax before reloading
sudo systemctl reload smb
```

`smb encrypt = required` enforces SMB 3.x encryption on the wire for this
share; `full_audit` provides an auditable trail of destructive operations,
directly supporting the governance requirements covered in [Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md).

### S3-compatible bucket policy and lifecycle rule

```json
{
  "Version": "2026-07-01",
  "Statement": [
    {
      "Sid": "AllowBackupServiceWriteOnly",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::EXAMPLE:role/backup-service-role" },
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": "arn:aws:s3:::backup-repository-01/*"
    },
    {
      "Sid": "DenyUnencryptedTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::backup-repository-01",
        "arn:aws:s3:::backup-repository-01/*"
      ],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    }
  ]
}
```

```yaml
# lifecycle-policy.yaml — generic S3-compatible lifecycle configuration
Rules:
  - ID: TierAndExpireBackupObjects
    Status: Enabled
    Filter:
      Prefix: "daily/"
    Transitions:
      - Days: 30
        StorageClass: "STANDARD_IA"     # infrequent-access tier
      - Days: 90
        StorageClass: "ARCHIVE"         # cold/archive tier
    NoncurrentVersionExpiration:
      NoncurrentDays: 400
    Expiration:
      Days: 730
```

This pair of policies denies any unencrypted-transport access to the bucket,
grants a backup service a narrowly scoped principal write/read access, and
automatically tiers and eventually expires daily backup objects — enforcing
the retention design from [Chapter 5](05-backup-architecture-and-data-protection-policy.md) directly in the object platform rather
than relying on operator discipline.

## Validation and Troubleshooting

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| NFS mount hangs | Server unreachable, export not published, firewall blocking 2049 | `rpcinfo -p <server>`, `showmount -e <server>`, check firewall rules |
| "Permission denied" despite correct mode bits | NFSv4 ID mapping mismatch (client/server `idmapd` domain mismatch) | Compare `/etc/idmapd.conf` `Domain` setting on client and server; check `ls -ln` for numeric UID/GID mismatches |
| SMB share visible but access denied | Share-level ACL vs. NTFS/POSIX ACL conflict, group membership not refreshed | `smbstatus`, verify `net groupmap`/Samba group resolution, confirm Kerberos ticket validity if using AD |
| Object PUT succeeds but subsequent GET returns 404 | Eventual-consistency window on a non-strongly-consistent platform, or wrong bucket/region endpoint | Retry with backoff; confirm platform's documented consistency model; verify endpoint/region configuration |
| Lifecycle transition not occurring | Filter prefix mismatch, versioning interaction, policy not enabled | Re-check rule `Filter`/`Prefix` against actual object keys; confirm `Status: Enabled`; check for a more specific rule shadowing the intended one |
| Slow file listing on very large directories | Extremely large flat directories on a file namespace not designed for that scale | Consider object storage or a namespace redesign with subdirectory sharding for that workload |

`rpcinfo -p` and `showmount -e` remain the fastest way to confirm an NFS
server is actually publishing the expected exports before investigating
client-side mount options. For Samba, `smbstatus` shows active sessions,
locked files, and share connections in real time and is the first stop for
any "why can't this user access this file" investigation.

## Security and Best Practices

- Use `root_squash` by default; treat every `no_root_squash` export as a
  documented, narrowly scoped exception, never a default.
- Prefer Kerberos (`sec=krb5`, `sec=krb5i`, `sec=krb5p`) over `sec=sys` for
  NFS exports carrying sensitive data — `sec=sys` trusts the client's
  self-reported UID/GID with no cryptographic verification.
- Require SMB signing and encryption (`smb encrypt = required`) for any
  share carrying sensitive data; do not rely on SMB 1 or unsigned SMB 2 in
  any production environment.
- Enable object versioning and pair it with a noncurrent-version expiration
  lifecycle rule to bound the cost of protecting against accidental
  overwrite/delete.
- Explicitly deny unencrypted transport (`aws:SecureTransport: false` or the
  equivalent condition) on any bucket policy protecting sensitive data.
- Apply least-privilege, action-scoped bucket policies (separate read and
  write principals where roles genuinely differ) rather than broad
  `s3:*`-style grants.
- Enable audit logging (Samba `full_audit`, NFS server-side auditd rules,
  object storage server access logging) on any namespace subject to
  compliance or forensic requirements, and ship those logs off-platform.
- Review multiprotocol NFS/SMB permission mappings periodically — permission
  drift across protocol boundaries is a recurring, hard-to-detect
  misconfiguration.

## References and Knowledge Checks

**References**

- [RFC 8881](https://www.rfc-editor.org/rfc/rfc8881) (NFSv4.1) and the NFSv4.2 extensions.
- [SNIA Cloud Data Management Interface (CDMI) and object storage
  architecture references.](https://www.snia.org/)
- [`exports(5)`, `smb.conf(5)`, `showmount(8)`, `rpcinfo(8)` manual pages,
  RHEL 10 / Ubuntu Server 26.04 LTS baseline per SOFTWARE_VERSIONS.md.](https://man7.org/linux/man-pages/man5/exports.5.html)

**Knowledge Checks**

1. Why does NFSv4's single-protocol, single-port design simplify firewall
   configuration compared to NFSv3?
2. A user reports they can mount an NFS export but every operation returns
   "Permission denied" even though `ls -l` shows they own the files. What
   NFSv4-specific configuration should you check first?
3. Explain why object storage is generally a better fit than file storage
   for a backup repository, referencing at least two architectural
   properties from this chapter.
4. What is the operational risk of enabling object versioning without a
   corresponding lifecycle expiration rule?
5. Describe the difference in blast radius between a single-head NAS filer
   failure and a single-node failure in a properly configured scale-out file
   or object cluster.

## Hands-On Lab

### Lab: Configure NFS Export Security and Validate Root-Squash Behavior

This lab configures an NFS export with default (secure) root-squash
behavior, validates it from a client, and then demonstrates — as a negative
test — the access change that occurs when root-squash is disabled, so the
security implication is directly observable rather than theoretical.

**Prerequisites**

- Two Linux hosts (RHEL 10 or Ubuntu Server 26.04 LTS baseline):
  `nfs-server01` and `nfs-client01`, on the same network.
- Root or sudo access on both hosts.
- `nfs-utils` (RHEL) or `nfs-kernel-server`/`nfs-common` (Ubuntu) installed.

**Procedure**

1. On `nfs-server01`, create and populate the export directory:

   ```bash
   sudo mkdir -p /export/lab
   sudo chown nobody:nogroup /export/lab   # Ubuntu; use nobody:nobody on RHEL
   echo "owned by nobody" | sudo tee /export/lab/marker.txt
   sudo chmod 755 /export/lab
   ```

2. Configure the export with default root-squash and restart the NFS
   service:

   ```bash
   echo "/export/lab  <nfs-client01_ip>(rw,sync,root_squash)" | sudo tee -a /etc/exports
   sudo exportfs -ra
   sudo systemctl restart nfs-server   # or: nfs-kernel-server on Ubuntu
   sudo exportfs -v
   ```

3. On `nfs-client01`, mount the export and attempt to create a file as
   root:

   ```bash
   sudo mkdir -p /mnt/lab
   sudo mount -t nfs4 <nfs-server01_ip>:/export/lab /mnt/lab
   sudo touch /mnt/lab/root-created-file.txt
   ls -ln /mnt/lab/
   ```

4. **Expected result:** the new file is owned by the anonymous UID/GID
   (typically 65534, `nobody`/`nogroup`) as seen from `nfs-server01`, not by
   UID 0 — confirming root-squash is mapping the client's root user to an
   unprivileged account.

**Negative test**

5. On `nfs-server01`, change the export to `no_root_squash` and reapply:

   ```bash
   sudo sed -i 's/root_squash/no_root_squash/' /etc/exports
   sudo exportfs -ra
   sudo exportfs -v
   ```

6. On `nfs-client01`, unmount and remount, then repeat the root file
   creation:

   ```bash
   sudo umount /mnt/lab
   sudo mount -t nfs4 <nfs-server01_ip>:/export/lab /mnt/lab
   sudo touch /mnt/lab/root-created-file-2.txt
   ls -ln /mnt/lab/
   ```

   **Expected result:** the new file is now owned by UID 0 as seen from
   `nfs-server01` — the client's root user now has genuine root ownership on
   the server's filesystem, demonstrating exactly why `no_root_squash`
   should be reserved for narrowly justified cases and never used as a
   default.

**Cleanup**

7. On `nfs-client01`, unmount the export:

   ```bash
   sudo umount /mnt/lab
   sudo rmdir /mnt/lab
   ```

8. On `nfs-server01`, remove the export entry, reapply, and remove the test
   directory:

   ```bash
   sudo sed -i '\#/export/lab#d' /etc/exports
   sudo exportfs -ra
   sudo rm -rf /export/lab
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter compared NFS and SMB as enterprise file protocols, introduced
scale-out file system architecture, and covered object storage's flat
namespace, metadata, consistency, versioning, and lifecycle model. It then
applied that theory to NFS export, Samba share, and S3-compatible bucket
policy/lifecycle configuration, and demonstrated the security impact of
root-squash directly through a hands-on negative test.

**Completion checklist**

- [ ] Can compare NFS and SMB on locking, ACL, and encryption models.
- [ ] Can explain why scale-out file/object platforms confine failure impact
      better than single-head filers.
- [ ] Can write a lifecycle policy that tiers and expires objects based on
      age.
- [ ] Has configured an NFS export with root-squash and validated the
      resulting file ownership behavior.
- [ ] Has reproduced the access-control difference between root_squash and
      no_root_squash directly.
- [ ] Can diagnose at least four common file/object access or performance
      symptoms from this chapter's troubleshooting table.
