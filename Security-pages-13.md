# Verification: Internal Penetration Testing

Every control described in Sections 3 to 12 is, ultimately, a claim
about the deployment\'s security, \"the network is segmented\" is a
sentence, not proof. This section exists specifically to verify those
claims are actually true, in the same way an exploit\'s mitigation would
be verified to have actually worked rather than simply assumed to have
taken effect once the configuration was applied.

This section sits deliberately after every technical control (Sections
3--12) and immediately before the incident runbook (Section 14): it is
the hinge between what was built and what happens once it breaks.
Penetration testing is what actually discovers incidents in the first
place; the runbook in Section 14 is what happens once one is found. The
two are sequenced to reflect that relationship directly, not placed
arbitrarily.

- Default credentials checked on Horizon and every exposed API endpoint.

- Management-plane reachability tested directly from a tenant instance,
  Keystone, RabbitMQ, and MariaDB should all be unreachable from tenant
  networks.

- Lateral movement attempted from a deliberately compromised instance,
  to confirm segmentation actually contains it.

- Privilege escalation paths tested on hosts and containers, using the
  same full exploit, post-exploitation, mitigation, and verification
  cycle methodology applied against Metasploitable 2 in prior lab work.

- Testing repeated on a recurring schedule, not performed once at launch
  and left unrevisited.
