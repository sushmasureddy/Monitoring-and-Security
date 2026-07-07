# Identity & Access Security: Keystone

Keystone is the authentication and authorization service every other
OpenStack component ultimately relies on, it decides who is logged in
and what role they hold once inside. It is, in the plainest sense, the
front door to the entire cloud, and every other control described later
in this document quietly assumes identity has already been handled
correctly. A Keystone compromise makes nearly every downstream control
irrelevant, because an attacker holding a valid, sufficiently privileged
token no longer needs to break anything else.

In this deployment, roles are scoped per project and domain rather than
granted globally, multi-factor authentication is enforced through
federation for any account with elevated access, and automation and
scripts authenticate using separately scoped application credentials
instead of a full user login, so a leaked script credential never
exposes a human account's complete access.

| Control | Implementation |
|---|---|
| Least-privilege RBAC | Scoped roles per project/domain: `openstack role add --project <project> --user <user> <role>`. No blanket admin role. |
| MFA on admin accounts | Federated identity (SAML/LDAP) configured in keystone.conf; MFA enforced at the external IdP for every account with elevated access. |
| Application credentials | `openstack application credential create <name> --role <role>`, scoped, independently revocable credentials for automation and scripts, instead of full user passwords. |
| Credential rotation | Service and admin passwords in passwords.yml rotated on a defined, calendared schedule, not only at initial deployment. |
| Federated identity | External LDAP/SAML IdP preferred over local Keystone users, so access is centrally managed and instantly revocable. |

> **Common pitfalls**

- Granting the admin role "temporarily" during troubleshooting and
  forgetting to revoke it afterward.

- Reusing one application credential across multiple unrelated
  automation scripts, which erases the audit trail of which script
  actually took an action.

- Treating MFA as optional for service accounts used by humans in an
  emergency access path, emergency access is exactly when strong
  authentication matters most.
