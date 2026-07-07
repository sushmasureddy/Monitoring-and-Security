# Vulnerability & Patch Management

Patch management is the process of tracking known vulnerabilities in
every component of the deployment and applying fixes on a predictable
schedule rather than reactively. This is arguably the single most
important control in this entire document specifically because the
deployment is open source: every vulnerability becomes public knowledge
the moment it is disclosed, and there is no vendor quietly patching
things in the background on the operator's behalf. Patch management
here is a genuine race against public disclosure, not a routine
maintenance chore.

Security advisories are actively subscribed to, container images are
pulled and redeployed on a fixed cadence, host operating system patching
proceeds one node at a time so the cluster is never fully exposed to an
old vulnerability at once, and a running version inventory is kept so it
is always known exactly what is deployed at any given moment.

| Control | Implementation |
|---|---|
| CVE awareness | Subscribed to OpenStack Security Notes (OSSN) and the OpenStack security-announce mailing list, plus advisories for Ceph, RabbitMQ, MariaDB, and Docker itself. |
| Container image updates | `kolla-ansible pull` followed by deploy or reconfigure, run on a fixed weekly or biweekly cadence, not "when remembered." |
| Host OS patching | Ubuntu 24.04 patched on a rolling schedule, one node drained (nova-compute disabled, instances migrated) and rebooted at a time. |
| Glance image scanning | Every tenant-facing image scanned for known vulnerabilities before being made available. |
| Version inventory | A maintained record of every OpenStack component version, base container image tag, and Kolla-Ansible release currently in use. |

> **Common pitfalls**

- Subscribing to OSSN but not actually assigning anyone to read and act
  on the notices that arrive.

- Patching container images promptly but letting the underlying host OS
  packages drift for months.

- Losing track of exactly which image tags are running in production,
  making it impossible to quickly confirm whether a newly disclosed CVE
  actually affects this deployment.
