# Chapter 04: File and Object Storage

## Learning Objectives

- Describe file storage (VSP One File / NAS) and its protocols.
- Describe object storage (Content Platform / HCP) and its model.
- Distinguish when to use file versus object versus block.
- Understand metadata, scale, and cloud integration for object storage.

*Cert relevance: this is the File Storage and Object Storage tracks.*

## File storage

**File storage** presents **shared file systems** that many clients mount and access with familiar folder/file semantics. Hitachi Vantara's file offering (**VSP One File** / NAS systems) serves:

- **Protocols** — **NFS** (Unix/Linux) and **SMB/CIFS** (Windows) so any client can mount shares.
- **Shared access** — many users and applications read/write the **same** file system, with permissions controlling who can do what.
- **Use cases** — **user home directories, departmental shares, application file data** — anywhere a **shared file system** is the natural model.

File storage is the right choice when the workload thinks in **files and folders** shared across clients (unlike block, which presents raw volumes to one host, or object, which is accessed by API). Administering it means managing **file systems, shares, quotas, and permissions**. The lab models a file share with quotas.

## Object storage

**Object storage** (Hitachi **Content Platform**, HCP) is a different model built for **massive scale and durability**:

- **Objects, not files** — data is stored as **objects** (the data + rich **metadata** + a unique ID) in a **flat namespace** (no folder hierarchy), accessed by **HTTP/REST** APIs (commonly **S3-compatible**).
- **Massive scale** — designed for **billions** of objects and petabytes, scaling out across nodes.
- **Durability and immutability** — built-in replication/erasure coding for durability, and **WORM/retention** (write-once-read-many) for compliance and ransomware resilience.
- **Metadata** — rich, searchable metadata on each object enables management and analytics at scale.

Object storage is the choice for **archives, backups, unstructured data, and cloud-native applications** — data that is written, kept, and read by applications at scale rather than edited in place by users. The lab stores and retrieves objects with metadata and retention. *(Object storage with S3 APIs and retention is the backbone of modern backup and archive, as in [Cohesity CLVII](../../volume-157-cohesity-certifications/README.md) and [Rubrik CXXX](../../volume-130-rubrik-certifications/README.md).)*

## Choosing block, file, or object

The three storage types are **complementary**, and choosing correctly is core storage knowledge:

| Type | Access | Best for |
| --- | --- | --- |
| **Block** (VSP) | raw volumes (LUNs) over SAN, one host | databases, VMs — low-latency transactional ([Ch 3](03-block-storage-administration.md)) |
| **File** (VSP One File) | shared file systems over NFS/SMB | user shares, file workloads |
| **Object** (Content Platform) | objects over HTTP/S3 API | archives, backups, unstructured data at scale |

The decision follows the **access pattern**: transactional and low-latency → block; shared files → file; scale, archive, and API access → object. A well-designed enterprise uses all three for the right workloads, often on Hitachi's unified portfolio. The lab routes data to the right type.

## Metadata, scale, and cloud

Object storage's defining strengths are **metadata, scale, and cloud integration**:

- **Metadata** makes billions of objects **manageable and searchable** — policies, retention, and analytics key off it.
- **Scale-out** growth adds nodes without disruption, handling relentless data growth.
- **Cloud tiering / hybrid** — object platforms often **tier to or integrate with public cloud** (S3), so cold data moves to cheaper cloud storage while staying in one namespace.

This is why object storage underpins **modern data management** — cheap, durable, API-driven storage for the ever-growing volume of unstructured and archival data, bridging on-premises and cloud. Understanding these properties distinguishes object from file/block and is what the object-storage track tests. The lab applies a retention policy and cloud tiering.

## Hands-On Lab

Python models a file share, object storage with metadata/retention, type routing, and cloud tiering. **Cost:** none.

### Lab 4.1 — File shares and object storage

**Objective:** Manage a file share with quotas, store objects with metadata and retention, and route data.

```bash
python3 - <<'EOF'
# FILE storage: a shared file system with quotas + permissions (NFS/SMB)
file_share = {"path":"/exports/finance","protocol":"SMB","quota_gb":100,"used_gb":0,"acl":{"finance":"rw","others":"none"}}
def write_file(share, gb, group):
    if share["acl"].get(group,"none")=="none": return f"DENY: '{group}' has no access"
    if share["used_gb"]+gb > share["quota_gb"]: return f"DENY: quota {share['quota_gb']}GB exceeded"
    share["used_gb"]+=gb; return f"wrote {gb}GB as '{group}' (used {share['used_gb']}/{share['quota_gb']}GB)"
print("FILE STORAGE (VSP One File, SMB share):")
print(f"   {write_file(file_share, 40, 'finance')}")
print(f"   {write_file(file_share, 5, 'others')}")

# OBJECT storage: objects with metadata + retention (WORM), S3-style
class ObjectStore:
    def __init__(self): self.objects={}
    def put(self, key, data, metadata, retain_days=0):
        self.objects[key]={"data":data,"metadata":metadata,"retain_days":retain_days}
        return f"PUT {key}  metadata={metadata}  retention={retain_days}d (WORM)"
    def delete(self, key):
        if self.objects[key]["retain_days"]>0: return f"DENY delete {key}: under retention (immutable)"
        del self.objects[key]; return f"deleted {key}"
hcp = ObjectStore()
print("\nOBJECT STORAGE (Content Platform, S3-style):")
print(f"   {hcp.put('backups/2026-08-06.tar', b'...', {'app':'erp','type':'backup'}, retain_days=2555)}")
print(f"   {hcp.delete('backups/2026-08-06.tar')}")   # blocked by retention

# route data to the right type + cloud tiering
def route(workload): return {"database":"BLOCK","home directories":"FILE","7-year archive":"OBJECT"}.get(workload,"?")
print("\nTYPE ROUTING + CLOUD TIERING:")
for w in ["database","home directories","7-year archive"]:
    r = route(w); tier = " -> tier cold objects to public cloud (S3)" if r=="OBJECT" else ""
    print(f"   {w:16} -> {r}{tier}")
print()
print("FILE storage (VSP One File) serves shared file systems over NFS/SMB with QUOTAS + ACLs.")
print("OBJECT storage (Content Platform) stores objects with rich METADATA and RETENTION (WORM)")
print("— the retained backup can't be deleted (ransomware/compliance resilience). Block for")
print("databases, file for shares, object for archive at scale (tiered to cloud). Right type per workload.")
EOF
```

**Expected result:** A file share enforcing quota and ACLs, an object store putting a backup with metadata and a retention policy that blocks deletion (WORM), and data routed to block/file/object with cold objects tiered to cloud. The lesson is Hitachi's file and object storage: file (VSP One File) serves shared NFS/SMB file systems with quotas/permissions, object (Content Platform) stores immutable, metadata-rich objects at scale for archives and backups (tiered to cloud), and each storage type fits a different access pattern.

**Negative test:** Storing 7-year compliance archives on a file share, or transactional databases in object storage. The archive lacks immutability/retention and scales poorly; the database suffers object latency; object for archive (with WORM) and block for databases matches each workload to the right storage type.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] File storage understood — VSP One File / NAS, NFS/SMB shares, quotas, and permissions.
- [ ] Object storage understood — Content Platform, objects with metadata, S3 API, scale, and WORM retention.
- [ ] Choosing block/file/object understood — matching the storage type to the access pattern.
- [ ] Metadata, scale, and cloud understood — why object underpins modern archive and hybrid-cloud data.

## See also

- [Chapter 03 — Block Storage Administration](03-block-storage-administration.md) — the third storage type.
- [Chapter 05 — Data Protection and Replication](05-data-protection-and-replication.md) — protecting all three.
- [Volume CLVII — Cohesity](../../volume-157-cohesity-certifications/README.md) — object storage in backup/data protection.
