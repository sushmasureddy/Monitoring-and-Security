# Cloud Infrastructure Security Guide

## Executive Summary

This document consolidates every security area, control, framework,
standard, and methodology relevant to this multi-node OpenStack data
center deployment, built with Kolla-Ansible. It is organized the same
way the deployment's monitoring documentation is organized, by area,
with the actual implementation detail alongside each control, not just
the concept.

The quick-reference table below is the condensed, ten-area summary. Full
reasoning and step-by-step implementation for every row follows in the
numbered sections after it.

| Security Area | Control |
|---|---|
| Access control | Keystone RBAC, least privilege, MFA on admin accounts, application credentials |
| Network segmentation | Separate management, tenant, and storage/Ceph networks; deny-by-default security groups |
| Data encryption | TLS internal + external on all APIs and Horizon; Ceph OSD encryption at rest; Barbican-backed volume encryption |
| Secrets management | kolla-genpwd passwords.yml, encrypted in Ansible Vault; scheduled credential rotation |
| Host / container hardening | CIS Benchmark scoring via Lynis; Trivy image scanning; fail2ban; unused services disabled |
| Patch management | CVE tracking for OpenStack components and base container images; scheduled kolla-ansible pull/deploy |
| Storage security (Ceph) | CephX authentication always on; admin keyring access tightly restricted; per-tenant pool isolation |
| Audit logging | Keystone/Nova/Neutron CADF logs shipped to OpenSearch for a full who-did-what-when trail |
| Intrusion / anomaly detection | auditd on every host for system-call tracking and file-integrity/privilege-escalation monitoring, with its own dedicated alert path |
| Backup security | Encrypted backups, regularly tested restores, offsite copy held to the same access controls as production |

## Security Overview

This deployment runs every OpenStack service, Nova, Neutron, Keystone,
Glance, Cinder, Heat, Octavia, Horizon, as an open-source Docker
container, orchestrated by Kolla-Ansible across multiple nodes in a
physical data center.

Because every component is open source, every known vulnerability in it
is public the moment it is disclosed. There is no vendor silently
patching in the background and no single company responsible for the
code's safety. That responsibility sits entirely with whoever operates
the deployment, which is the reason this document treats security as a
continuous, layered discipline rather than a one-time setup checklist.

The structure of this document borrows the five-stage cycle from the
NIST Cybersecurity Framework: know what is running (Identify), lock it
down (Protect), watch for intrusion (Detect), act when something happens
(Respond), and get back to normal cleanly (Recover). Every section from
here onward maps to one of these five stages, and that mapping is made
explicit in Section 17.

### Why Open Source Changes the Security Approach

An open-source deployment is not inherently less secure than a
commercial one, but it does shift where responsibility sits.
Vulnerabilities in Nova, Neutron, Ceph, RabbitMQ, or Docker itself are
public knowledge the instant they are disclosed, there is no vendor
absorbing a delay window before a patch quietly ships. Anyone, including
an attacker, can read the exact source code running in this deployment,
so security here cannot lean on obscurity; it has to come from correctly
applied, verifiable controls.

This also means patch responsibility is entirely operator-side.
Subscribing to OpenStack Security Notes (OSSN) and the individual
advisories for Ceph, RabbitMQ, MariaDB, and Docker is not an optional
nicety, it is the only early-warning system that exists for this
deployment. The advantage that comes with this openness is that
defensive tooling and documentation are just as freely available as the
source code itself: the exporters, security guides, and hardening
benchmarks referenced throughout this document are the direct benefit of
the same openness that creates the risk in the first place.

### Deployment Components in Scope

Every component below is a real attack surface and is addressed
explicitly somewhere in this document.

| Layer | Components / Containers |
|---|---|
| Identity | Keystone |
| Compute | Nova, nova-compute, nova-conductor, nova-scheduler |
| Networking | Neutron, OVS/OVN agents, L3/DHCP agents |
| Image | Glance |
| Block Storage | Cinder API/scheduler/volume |
| Storage Backend | Ceph (mon, osd, mgr, rgw) |
| Orchestration | Heat |
| Load Balancing | Octavia, amphora instances |
| Dashboard | Horizon |
| Containers (tenant) | Zun, cAdvisor |
| Database | MariaDB / Galera cluster |
| Messaging | RabbitMQ |
| Edge / VIP | HAProxy, Keepalived |
| Secrets | Barbican |
| Monitoring / Logging | Prometheus, Grafana, Alertmanager, Fluentd, OpenSearch |
| Host layer | Docker Engine, Ubuntu 24.04 host OS, all nodes |

Note on scope: the monitoring/logging layer listed above (Prometheus,
Grafana, Alertmanager, Fluentd, OpenSearch) is the infrastructure
observability stack covered in the deployment's separate monitoring
documentation. Security detection, covered in Section 10 of this
document, is a deliberately separate concern with its own dedicated
tooling, the two are related but are not the same pipeline.

### The Ten Security Areas

Every control in this document falls under one of these ten areas, this
is the master list the rest of the document is organized around.

| # | Area | One-line purpose |
|---|---|---|
| 1 | Identity / Access control | Controls who can log in and what they are allowed to do |
| 2 | Network segmentation | Controls which traffic can reach which service |
| 3 | Data encryption | Protects data in transit and at rest |
| 4 | Secrets management | Protects passwords, keys, and tokens |
| 5 | Host / container hardening | Reduces what an attacker can do on a compromised node |
| 6 | Patch / vulnerability management | Closes known security holes before exploitation |
| 7 | Storage security (Ceph) | Protects the data layer underneath Cinder and Glance |
| 8 | Detection / audit logging | Notices intrusions and records who did what |
| 9 | Policy / API hardening | Fine-grained control over individual API actions |
| 10 | Backup / recovery security | The last line of defense if every other control fails |
