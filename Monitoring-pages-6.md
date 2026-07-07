# Security

Security controls are organized by area — access, network, secrets,
transport, patching, and audit — since each needs to be addressed
independently:

- Access control: Keystone RBAC with least-privilege roles, scoped
  projects/domains, and MFA on admin accounts, preventing lateral
  movement from a compromised token.

- Network segmentation: separate management/API, tenant, and
  external/storage networks, so database, RabbitMQ, and Ceph cluster
  traffic is never reachable from tenant instance networks.

- Secrets management: passwords.yml generated via kolla-genpwd, stored
  encrypted in Ansible Vault rather than plaintext in the repo.

- TLS everywhere: Kolla's internal and external TLS enabled for every
  API endpoint and Horizon, so credentials never travel in clear text.

- Patch management: CVEs tracked for OpenStack components and base
  container images, applied through the update process on a defined
  cadence.

- Audit logging: Keystone/Nova/Neutron CADF audit events shipped to the
  centralized OpenSearch log store for 'who did what' reconstruction.

- Intrusion/anomaly detection: host-based tools such as auditd and Wazuh
  run alongside Prometheus/Grafana metrics to catch break-in attempts
  and unusual login patterns.

| Security Area | Control |
|---|---|
| Access control | Keystone RBAC, least privilege, MFA on admin |
| Network segmentation | Separate management, tenant, and storage/Ceph networks |
| Secrets management | kolla-genpwd passwords.yml, encrypted in Ansible Vault |
| TLS everywhere | Internal + external TLS on all APIs and Horizon |
| Patch management | CVE tracking for OpenStack + base container images |
| Audit logging | Keystone/Nova/Neutron CADF logs to OpenSearch |
| Intrusion / anomaly detection | auditd / Wazuh alongside metrics stack |
