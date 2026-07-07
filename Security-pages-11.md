# Policy & API Hardening

Policy hardening governs what an already-authenticated,
already-authorized user is still permitted to do at the level of
individual API calls, and rate-limiting governs how often they are
allowed to call it. Role-based access control decides whether someone
can log in holding a given role; policy decides what that role is
actually allowed to execute once inside, related layers, but genuinely
distinct ones, and a default policy file should be treated as a starting
point rather than a guarantee of least privilege for this specific
environment.

Each service\'s policy.yaml is reviewed individually against Kolla\'s
shipped defaults rather than accepted as-is, API rate-limiting is
enabled wherever the underlying service supports it, and any OpenStack
service that is not actively used is fully disabled rather than left
running idle in the background.

| **Control** | **Implementation** |
| --- | --- |
| Policy review | policy.yaml reviewed per service under /etc/kolla/config/\<service\>/, Kolla\'s shipped defaults are a starting point, not assumed to be least-privilege for this environment. |
| API rate-limiting | Enabled wherever the individual OpenStack service supports it, to reduce denial-of-service exposure. |
| Disabled unused services | Any OpenStack service not actively in use is fully disabled rather than left running idle, every running service is attack surface with no offsetting benefit. |

> ***Common pitfalls***

- Reviewing policy.yaml once at initial deployment and never revisiting
  it as new roles and use cases are added.

- Leaving a service like Zun or Octavia enabled from an early evaluation
  phase long after it stopped being actively used.
