# Maintenance

Routine maintenance keeps the deployment stable between updates. Each
task is handled through Kolla-Ansible or its underlying components, not
by hand, so changes stay consistent with the single source of truth:

- Container/service restarts: 'kolla-ansible restart' or 'docker
  restart', orchestrated one role at a time (e.g. all Nova containers
  together) to avoid a full-cloud outage.

- Log rotation: logrotate runs inside containers to stop disks filling
  up; the Fluentd-to-OpenSearch pipeline applies its own ILM policy for
  searchable history after rotation.

- Database maintenance: Galera nodes are patched one at a time during a
  low-traffic window (mysqlcheck/OPTIMIZE TABLE), since taking down all
  nodes together breaks quorum.

- Config drift checks: the Ansible inventory is the only source of truth
  — any globals.yml/passwords.yml change is followed by 're-run
  deploy/reconfigure', so manual per-node edits get overwritten.

- Certificate renewal: cert-manager or manual renewal + 'kolla-ansible
  reconfigure', with blackbox_exporter alerting ahead of expiry.

- Capacity review: Grafana dashboards showing CPU/RAM/disk trends over
  30/90 days, reviewed monthly to plan ahead of hard limits.

| Maintenance Task | Approach |
|---|---|
| Container/service restarts | kolla-ansible restart, rolling per role |
| Log rotation | logrotate in-container + OpenSearch ILM policy |
| Database maintenance | Rolling Galera node maintenance, quorum preserved |
| Config drift checks | Re-run kolla-ansible deploy/reconfigure from git repo |
| Certificate renewal (TLS) | cert-manager or manual + kolla-ansible reconfigure |
| Capacity review | Monthly Grafana trend review (30/90-day) |
