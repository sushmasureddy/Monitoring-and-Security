# Security Runbook

First-response steps for the most likely security incident categories in
this deployment.

# Suspected Credential Compromise

- Immediately revoke the affected token or application credential via
  Keystone.

- Rotate the associated password and re-issue application credentials
  with new scopes.

- Review CADF audit logs in OpenSearch for actions taken under that
  identity since the suspected compromise window.

- Confirm MFA is enforced on the account going forward if it was not
  already.

## Unauthorized Network Access Detected

- Identify the source subnet and confirm whether it originated from a
  tenant network reaching the management plane.

- Apply an immediate firewall rule to block the source, then investigate
  why segmentation did not already prevent it.

- Check auditd logs on affected hosts for follow-on activity.

- Document the segmentation gap and correct the underlying VLAN/firewall
  rule, not just the symptom.

## Ceph Admin Keyring Exposure

- Rotate the exposed keyring immediately (ceph auth caps / re-issue
  key).

- Audit ceph auth list for any unauthorized capability changes made
  using the exposed key.

- Restrict the new keyring\'s host/user access more tightly than before
  the incident.

- Review cluster health (ceph -s) to confirm no unauthorized destructive
  action occurred.

## Container Image Vulnerability Found

- Confirm the CVE\'s severity and whether it is remotely exploitable in
  this deployment\'s configuration.

- Check whether an updated image is available upstream; if so,
  kolla-ansible pull and reconfigure that service.

- If no patch exists yet, apply compensating controls (network
  restriction, service pause) until one is released.

- Re-scan with Trivy after remediation to confirm the finding is
  resolved.
