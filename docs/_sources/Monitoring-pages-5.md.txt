# Updates

Updates are split into two layers, sequenced separately —
container/service-level (Kolla-Ansible) and host-level OS/Docker updates
(Ubuntu level):

- Minor version / patch update: 'kolla-ansible pull' fetches new
  container images, then 'deploy' (or reconfigure) redeploys role by
  role, so the cloud is never fully down.

- Major OpenStack release: update kolla-ansible + globals.yml release
  tag, then run 'kolla-ansible -i inventory upgrade', which sequences
  upgrades in dependency order (DB schema before API services).

- Host OS patching (Ubuntu 24.04): drain the node (disable nova-compute,
  migrate instances), apt update/upgrade, reboot only if the kernel
  changed, one node at a time.

- Docker Engine updates: one node at a time, verifying container health
  after each restart before moving to the next node.

- Rollback plan: keep previous container image tags available locally/in
  registry, with globals.yml pinned to a known-good release tag before
  starting.

| Update Type | Approach |
|---|---|
| Minor version / patch | kolla-ansible pull, then deploy/reconfigure by role |
| Major OpenStack release | kolla-ansible -i inventory upgrade (dependency-ordered) |
| Host OS patching (Ubuntu 24.04) | Drain node, apt upgrade, reboot if needed, one at a time |
| Docker Engine updates | One node at a time, verify container health before next |
| Rollback plan | Pinned known-good image tags kept available |
