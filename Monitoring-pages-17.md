# Access and Credentials

This section explains, step by step, how a team member gets access to
the tools described in this document, and how that access is removed
when no longer needed.

# Requesting Access Step by Step

- Identify which tool access is needed: Grafana (dashboards), Prometheus
  (raw queries), Alertmanager (alert silencing), Ceph Dashboard, or
  Horizon (OpenStack UI).

- Submit an access request to the relevant component owner listed in
  Table 16.2, stating the tool and the reason access is needed.

- The owner creates an account scoped to the least privilege required —
  read-only (dashboard viewing) or admin (configuration changes) —
  rather than granting full admin access by default.

- For Grafana and the Ceph Dashboard, the owner creates the account
  directly in that tool's user management screen and shares the login
  through a secure channel, never in plain chat or email.

- For Horizon and OpenStack CLI access, the owner creates a scoped
  Keystone project/role assignment following the RBAC model described in
  section 6.

- The new user changes their temporary password on first login and,
  where supported (Horizon, Grafana), enables multi-factor
  authentication before being considered fully onboarded.

## Where Each Tool Is Accessed

| Tool | Typical Access Point | Access Level Needed |
|---|---|---|
| Grafana | Web UI, internal DNS name over HTTPS | Viewer (default) or Editor (dashboard changes) |
| Prometheus | Web UI, internal-only, not exposed externally | Read-only by default; restrict write/config access |
| Alertmanager | Web UI, internal-only | Viewer, or Admin for silencing rules |
| Ceph Dashboard | https://\<ceph-mgr-host\>:8443 | Admin account created per section 13.2 |
| Horizon | https://\<horizon-vip\>/horizon | Keystone-scoped project role |

## Revoking Access Step by Step

- When a team member changes role or leaves the team, their component
  owner is notified within one business day.

- The owner disables (rather than immediately deletes) the account in
  each tool the person had access to, preserving an audit trail of past
  actions.

- Keystone role assignments are removed so the person's OpenStack
  access is revoked immediately, consistent with the least-privilege
  principle in section 6.

- Shared credentials (if any legacy ones exist) are rotated, since a
  shared credential cannot be revoked for one person without affecting
  everyone else — this is also why individual accounts are required
  going forward.

- The access change is logged in the same audit trail referenced in
  section 6, so 'who had access when' remains reconstructable.
