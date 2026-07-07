# Backup

Backups are organized by data type, since each layer is stored
differently and needs its own mechanism:

- Database (MariaDB): Kolla-Ansible's mariadb_backup playbook runs
  mariabackup for scheduled full and incremental backups, which supports
  near point-in-time recovery for large DBs.

- Config files (globals.yml, passwords.yml, inventory):
  version-controlled in a private git repository, with periodic tar
  snapshots sent offsite — version control preserves a 'who changed
  what and when' history.

- Glance images / Cinder volumes: backed up at the Ceph RBD layer via
  scheduled snapshots and export-diff, far more efficient at scale than
  an API-level export per object.

- Cinder's own backup-to-swift mechanism remains available as a
  secondary, crash-consistent option tied to the OpenStack inventory.

- Instance/VM state: Nova snapshots to Glance only for critical VMs;
  other instances are treated as re-creatable from Heat/Terraform
  templates.

- Full DR / offsite copy: all backup sets (DB dumps, config repo, Ceph
  RBD snapshots) are synced to a secondary site on a schedule, since
  on-site-only backups do not survive a data-center-level failure.

| Data Type | Method |
|---|---|
| Database (MariaDB/Galera) | kolla-ansible mariadb_backup (mariabackup, full + incremental) |
| Config (globals.yml, inventory) | Git repo + periodic tar snapshot to offsite storage |
| Glance images / Cinder volumes | Ceph RBD snapshot / export-diff at the storage layer |
| Instance / VM state | Nova snapshot for critical VMs; else re-created from IaC |
| Full DR / offsite copy | Scheduled sync of all backup sets to a secondary site |
