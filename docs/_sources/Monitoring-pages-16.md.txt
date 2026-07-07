# Ownership and Escalation

This section defines who is responsible for responding to an alert, and
what happens step by step if the first responder cannot resolve it.

# Severity and Response Table

| Alert Severity | First Responder | Escalation Path | Target Response Time |
|---|---|---|---|
| Critical (e.g. Ceph OSD down, HAProxy backend down, Galera below quorum) | On-call engineer (pager/Slack) | Team lead if unresolved after 30 minutes | Immediate acknowledgement, work begins within 15 minutes |
| Warning (e.g. disk usage 85%, TLS expiry < 30 days, queue backlog) | Assigned engineer, next business day | Team lead if unresolved after 1 business day | Within 24 hours |
| Informational (capacity trend review, routine maintenance) | Rotating monthly reviewer | Not applicable | Reviewed at next scheduled check |

## Step-by-Step Escalation Flow

- An alert fires in Alertmanager and is routed to the on-call channel
  (Slack/email) as defined in section 15.

- The on-call engineer acknowledges the alert and begins first-response
  steps from the matching RunBook entry (section 10).

- If the issue is resolved, the engineer confirms resolution in the
  alert channel and closes the alert.

- If the issue is not resolved within the target response time in Table
  16.1, the engineer escalates to the team lead, including what has
  already been checked and ruled out.

- The team lead either continues the investigation, brings in a
  subject-matter owner (see Table 16.2), or declares a wider incident if
  the issue affects multiple services.

- Once resolved, a short written summary (cause, fix, time to resolve)
  is added to the incident log for future reference.

## Component Ownership

| Component / Layer | Primary Owner |
|---|---|
| OpenStack control plane (Nova, Neutron, Keystone, Glance, Cinder) | Cloud Platform Team |
| Ceph storage cluster | Storage Team |
| Monitoring stack (Prometheus, Grafana, Alertmanager) | Cloud Platform Team |
| Network (HAProxy, Keepalived, VIPs) | Network Team |
| Database (MariaDB/Galera) | Database Team |
| Security and access control | Security Team |
