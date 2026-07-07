# Storage Security: Ceph

Ceph is the storage backend underneath both Cinder volumes and Glance
images, and its own authentication and access controls are what actually
protect that persistent data at rest. A compromise at the Ceph layer is
considerably more severe than a compromise of any single OpenStack
service, because Ceph holds the real data for every volume and every
image across the entire cloud at once, not just the data belonging to
one tenant or one service.

CephX authentication is kept permanently enabled across every daemon,
the admin keyring, which can destroy the entire cluster if it leaks, is
restricted to the smallest realistic set of hosts and people, and pools
are isolated per tenant wherever that isolation is actually required.

| Control | Implementation |
|---|---|
| CephX authentication | Confirmed active on all daemons at all times (`ceph auth list`), never disabled, even for troubleshooting. |
| Admin keyring restriction | `ceph auth get client.admin` reviewed regularly; the admin keyring, which can destroy the entire cluster if leaked, is restricted to the fewest possible hosts and people. |
| Per-tenant pool isolation | Separate Ceph pools created per tenant or project where data isolation is required. |
| Network isolation | Ceph public and cluster networks kept on separate VLANs, per Section 4. |

> **Common pitfalls**

- Disabling CephX temporarily to simplify troubleshooting and forgetting
  to re-enable it before returning to production traffic.

- Copying the admin keyring onto more hosts than strictly necessary for
  convenience during a one-off maintenance task.

- Assuming pool-level isolation exists between tenants without ever
  having explicitly created separate pools.
