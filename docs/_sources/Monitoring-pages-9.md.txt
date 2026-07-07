# Alerts

Suggested Alertmanager thresholds to configure for this deployment,
grouped by layer:

- Host disk usage above 85% on any node triggers a warning; above 95%
  triggers a critical alert.

- Host CPU sustained above 90% for 10 minutes triggers a warning.

- Ceph cluster health state of WARN triggers a warning; HEALTH_ERR
  triggers a critical alert immediately.

- Any Ceph OSD reporting 'down' for more than 5 minutes triggers a
  critical alert.

- Galera cluster size dropping below quorum (majority of configured
  nodes) triggers a critical alert immediately.

- RabbitMQ queue depth growing continuously for 15 minutes without a
  matching rise in consumers triggers a warning.

- HAProxy backend marked down for any OpenStack API endpoint triggers a
  critical alert.

- TLS certificate expiry within 30 days triggers a warning; within 7
  days triggers a critical alert.

- Container restart count exceeding 3 within 10 minutes for the same
  service triggers a warning.

- Keystone or Horizon HTTP probe returning a non-200 response for more
  than 2 consecutive checks triggers a critical alert.

| Layer | Warning Threshold | Critical Threshold |
|---|---|---|
| Host disk | 85% used | 95% used |
| Host CPU | 90% for 10 min | N/A |
| Ceph cluster health | HEALTH_WARN | HEALTH_ERR |
| Ceph OSD | N/A | Down > 5 min |
| Galera quorum | N/A | Below majority |
| RabbitMQ queue depth | Rising 15 min, no consumers | N/A |
| HAProxy backend | N/A | Backend down |
| TLS certificate | Expiry < 30 days | Expiry < 7 days |
| Container restarts | > 3 in 10 min | N/A |
| Keystone/Horizon probe | N/A | Non-200 x2 consecutive |
