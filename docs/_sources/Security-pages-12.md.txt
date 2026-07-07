# Backup & Recovery Security

Backup security exists to ensure that the deployment\'s last line of
defense, the backups themselves, never becomes a new source of data loss
or leakage in its own right. If every other control in this document
fails, backups are what make recovery possible instead of total data
loss; but an unencrypted or untested backup provides only a false sense
of security, not an actual safety net.

Every backup in this deployment is encrypted the same way live data is,
restores are actually rehearsed on a regular schedule rather than
assumed to work, and the offsite or disaster-recovery copy is held to
identical access controls as production, rather than treated as a
lower-priority afterthought.

| **Control** | **Implementation** |
| --- | --- |
| Encrypted backups | Database dumps, config repository, and Ceph RBD snapshots encrypted before storage or transfer, matching the standard set for live data in Section 5. |
| Tested restores | Restore procedures actually run on a quarterly basis, an untested backup is treated as unverified, not as a working plan. |
| Equal access control offsite | The offsite/DR copy is held to the same access controls as production, the DR site is a common weak link and is not treated as an exception. |

> ***Common pitfalls***

- Encrypting the primary backup but replicating it to an offsite
  location that decrypts it in transit or storage.

- Assuming a backup works because the job completed successfully,
  without ever performing an actual restore.

- Applying weaker access controls to the DR site on the reasoning that
  it is \"just a backup,\" when it holds the same sensitive data as
  production.
