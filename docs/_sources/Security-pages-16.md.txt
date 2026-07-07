# Closing Summary

> This document has walked through the complete security posture of the
> multi-node OpenStack data center deployment, ten security areas, the
> governance layer (frameworks, standards, thumb rules, methodologies,
> NIST, and ISO) each area is measured against, the specific technical
> controls implemented for each area, a risk and impact assessment
> across all ten, an explicit compliance mapping back to NIST CSF and
> ISO 27002, how those controls are verified through internal
> penetration testing, and the first-response runbook for when a control
> fails despite everything above.
>
> The recurring theme across every section is the same: because this
> deployment is built entirely from open-source components, there is no
> vendor absorbing responsibility for security on the operator\'s
> behalf. Every control in this document, Keystone RBAC, network
> segmentation, TLS, Ansible Vault, Trivy scanning, CephX
> authentication, auditd, encrypted backups, exists because the
> deployment\'s operator is the only party who can apply it.

## What to Revisit First

- Confirm passwords.yml is encrypted with Ansible Vault, the fastest,
  cheapest fix with the largest impact if missed.

- Test, rather than assume, that management-plane ports are unreachable
  from tenant networks.

- Start a recurring Trivy scanning cadence against every container image
  already in use.

- Confirm CephX authentication is active and the admin keyring\'s access
  list is as small as possible.

- Schedule the first internal penetration test against this deployment
  specifically, using the same methodology already applied in prior lab
  work.

## How This Document Should Be Maintained

> Consistent with ISO/IEC 27001\'s requirement that a security program
> be actively managed rather than written once, this document should be
> reviewed on a fixed schedule, not only when an incident forces a
> revision. Each of the ten security areas in Section 1.3 should have an
> assigned owner, and the control tables in Sections 3 through 12 should
> be re-verified against the live deployment at each review, not simply
> re-read.

# Appendix A: Consolidated Command Reference

> Every command referenced across Sections 3 to 12, gathered in one
> place for quick lookup during setup or an incident.

## Identity

| **Purpose** | **Command** |
| --- | --- |
| Assign a scoped role | openstack role add --project \<project\> --user \<user\> \<role\> |
| Create an application credential | openstack application credential create \<name\> --role \<role\> |

## Network

| **Purpose** | **Command** |
| --- | --- |
| Add a security group rule | openstack security group rule create --protocol tcp --dst-port \<port\> --remote-ip \<trusted-cidr\> \<group\> |

## Encryption & Secrets

| **Purpose** | **Command / Setting** |
| --- | --- |
| Enable internal + external TLS | kolla_enable_tls_internal: \"yes\" / kolla_enable_tls_external: \"yes\" (globals.yml) |
| Encrypt the password file | ansible-vault encrypt /etc/kolla/passwords.yml |
| Deploy referencing the vault key | kolla-ansible --key /path/to/vault-key deploy |
| Enable Ceph OSD encryption | osd_encrypt: true (set before OSD creation) |

## Host & Container Hardening

| **Purpose** | **Command** |
| --- | --- |
| Run a CIS-style hardening audit | lynis audit system |
| Scan a container image for CVEs | trivy image \<kolla-image\>:\<tag\> |
| Disable an unused host service | systemctl disable \<service\> |

## Patch Management

| **Purpose** | **Command** |
| --- | --- |
| Fetch updated container images | kolla-ansible pull |
| Roll out the update per role | kolla-ansible deploy (or reconfigure) |

## Ceph

| **Purpose** | **Command** |
| --- | --- |
| Confirm CephX is active on all daemons | ceph auth list |
| Review admin keyring capabilities | ceph auth get client.admin |
| Check overall cluster health | ceph -s |

## Detection & Audit

| **Purpose** | **Command** |
| --- | --- |
| Watch a config path for changes | auditctl -w /etc/kolla -p wa -k kolla_config_changes |
