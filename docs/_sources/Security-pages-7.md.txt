# Host & Container Hardening

Hardening is about reducing what an attacker can actually accomplish if
they gain any foothold at all on a host or inside a container, closing
unnecessary services, restricting what Docker itself is allowed to do,
and scoring the resulting configuration against a known, external
baseline rather than a subjective sense of "good enough." Every
OpenStack-level control described elsewhere in this document quietly
assumes the underlying host and container runtime are themselves
trustworthy; if the host OS or the Docker daemon is misconfigured, a
compromise at that layer can undermine everything built on top of it.

Hosts in this deployment are scored against CIS Benchmarks using Lynis,
every container image is scanned with Trivy before it is deployed,
brute-force protection is enabled on exposed endpoints, and any service
that is not actively in use is disabled entirely rather than left idle.

| Control | Implementation |
|---|---|
| CIS Benchmark scoring | `lynis audit system` run on every node, produces a hardening score plus specific remediation steps. |
| Container image scanning | `trivy image <kolla-image>:<tag>` run against every image before it is pulled into production. |
| Docker daemon hardening | Docker socket not exposed unnecessarily; containers run with least privilege where Kolla configuration allows overrides. |
| Brute-force protection | fail2ban installed on every SSH- and API-facing node. |
| Reduced attack surface | Unused services disabled at the host level (`systemctl disable <service>`) and unused Kolla roles turned off (`enable_<service>: "no"` in globals.yml). |

> **Common pitfalls**

- Running Lynis once at initial setup and never re-running it after
  subsequent configuration changes.

- Scanning a container image with Trivy but deploying it anyway when the
  scan surfaces a medium-severity finding, without a documented decision
  to accept that risk.

- Leaving the Docker socket bind-mounted into a container for
  convenience during debugging and forgetting to remove it.
