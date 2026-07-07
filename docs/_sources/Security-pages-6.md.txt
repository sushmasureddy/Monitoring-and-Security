# Secrets Management

Secrets management covers the protection of passwords, API keys, and
tokens, the credentials that every other control in this document
ultimately depends on to function. If passwords.yml were ever to leak in
plaintext, every access-control, encryption, and audit-logging control
built on top of it becomes irrelevant in practice, because an attacker
holding valid credentials no longer needs to break anything; they can
simply log in.

The generated password file is encrypted with Ansible Vault, the vault
key itself is stored and access-controlled separately from the
repository it protects, Barbican manages tenant-facing secrets
independently, and every credential is rotated on a defined schedule
rather than left in place indefinitely.

| Control | Implementation |
|---|---|
| Encrypted password store | `ansible-vault encrypt /etc/kolla/passwords.yml`, passwords.yml is never left in plaintext, generated originally via kolla-genpwd. |
| Vault key on every run | `kolla-ansible --key /path/to/vault-key deploy`, the vault key itself is stored and access-controlled separately from the repository. |
| Barbican for tenant secrets | Deployed for tenant-facing secret and certificate management (Cinder volume encryption keys, TLS certs). |
| Scheduled rotation | All service credentials rotated on a defined cadence, tracked the same way certificate renewals are tracked. |

> **Common pitfalls**

- Storing the Ansible Vault key in the same repository or location as
  the file it is meant to protect.

- Rotating human passwords on schedule but leaving long-lived service
  account credentials untouched for years.

- Committing an unencrypted passwords.yml to version control even
  briefly during initial setup, leaving it in commit history
  permanently.
