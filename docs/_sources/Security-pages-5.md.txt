# Data Encryption: In Transit and At Rest

Encryption makes data unreadable to anyone without the correct key,
whether that data is actively moving across the network or sitting still
on a disk. Network segmentation and access control both reduce who can
reach the data in the first place, but encryption is the control that
protects the data itself even when every other layer has already been
bypassed, an intercepted packet or a stolen disk should still be
unreadable on its own.

TLS is enabled for both internal and external traffic through two
dedicated Kolla flags, Barbican manages encryption keys for tenant
volumes centrally, and Ceph is configured for OSD-level encryption
before any OSDs are created, since retrofitting encryption onto existing
OSDs is not straightforward.

| Control | Implementation |
|---|---|
| TLS everywhere | `kolla_enable_tls_internal: "yes"` and `kolla_enable_tls_external: "yes"` in globals.yml, applied via kolla-ansible reconfigure, covers every API endpoint, Horizon, RabbitMQ, and the HAProxy VIP, internal traffic included. |
| Encrypted Cinder volumes | Barbican-backed encryption keys for tenants handling sensitive data (`enable_barbican: "yes"`). |
| Ceph encryption at rest | `osd_encrypt: true` set in Ceph OSD deployment config before OSD creation, this cannot be easily retrofitted after OSDs exist. |
| Encrypted backups | Backup archives encrypted (gpg or storage-layer encryption) before being shipped offsite, a stolen backup should never be a readable data leak. |

> **Common pitfalls**

- Enabling external TLS but leaving internal service-to-service traffic
  unencrypted, on the assumption that internal traffic is already safe.

- Creating Ceph OSDs before setting osd_encrypt: true, which then
  requires a full rebuild to correct.

- Encrypting live volumes but forgetting that their backups need the
  same protection independently.
