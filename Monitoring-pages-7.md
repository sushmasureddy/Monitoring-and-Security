# Migration

Covers migrating the deployment to a new data center or DR site securely
and in order, so nothing is exposed or lost mid-migration:

- Pre-migration: document the current inventory.ini, globals.yml,
  passwords.yml, and running service list, since the new site must
  reproduce the exact topology.

- Data migration order: backup DB and configs, stand up new site nodes
  with the same globals.yml, restore DB via mariabackup, sync Ceph RBD
  data (images/volumes), then cut over networking last.

- Networking is cut over last (DNS/VIP) to avoid serving live traffic to
  a half-migrated backend.

- Network re-IP: update ext-net/tenant-net CIDRs and the HAProxy VIP for
  the new site, with low-TTL DNS if externally addressed, since data
  centers rarely share IP ranges.

- Validation before cutover: run 'openstack service list', 'nova
  hypervisor-list', and a smoke-test instance boot against the new site
  while the old site is still live.

- Decommission the old site only after a defined burn-in period (1-2
  weeks) with backups confirmed restorable from the new site.

| Migration Step | Approach |
|---|---|
| Pre-migration inventory | Document inventory.ini, globals.yml, passwords.yml, services |
| Data migration order | Backup -> stand up new site -> restore DB -> sync Ceph data -> cut over networking |
| Network re-IP / VIP cutover | Update CIDRs and HAProxy VIP, low-TTL DNS |
| Validation before cutover | Service list, hypervisor list, smoke-test boot on new site |
| Decommission old site | Only after burn-in period with backups confirmed restorable |
