# Tools Reference

Every monitored component in this deployment, in one place, for quick
lookup during an incident.

| Component | Tool(s) | Layer | Key Signal |
|---|---|---|---|
| Nova (Compute) | openstack-exporter, node_exporter | API + Host | Instance/hypervisor state |
| Neutron (Networking) | openstack-exporter, blackbox_exporter | API + Network | Agent status, VIP reachability |
| Keystone (Identity) | blackbox_exporter | API | Reachability, token latency |
| Glance (Image) | openstack-exporter, node_exporter | API + Storage | Image status, disk usage |
| Cinder (Block Storage API) | openstack-exporter | API | Volume state counts |
| Ceph (Storage Backend) | ceph-mgr Prometheus module | Storage | OSD/PG health, pool capacity |
| Horizon (Dashboard) | blackbox_exporter | Web | Page load, TLS expiry |
| Heat (Orchestration) | openstack-exporter, Fluentd | API + Logs | Stack status, failures |
| Octavia (Load Balancer) | openstack-exporter, blackbox_exporter | API + Network | Amphora, VIP status |
| Zun (Containers) | cAdvisor | Container | Per-container resources |
| MariaDB / Galera | mysqld_exporter | Database | Replication lag, quorum |
| RabbitMQ | RabbitMQ Prometheus plugin | Messaging | Queue depth, consumers |
| HAProxy / Keepalived | haproxy_exporter, blackbox_exporter | Network | Backend health, VIP failover |
| Docker containers | cAdvisor, Docker healthchecks | Container | Restarts, unhealthy state |
| Host / OS | node_exporter | Host | CPU, memory, disk, network |

# Tools Comparison

| Function | Tool(s) | User-Friendliness | Notes |
|---|---|---|---|
| Metrics (OpenStack + infra) | Prometheus + Grafana (Kolla default) | High (visual, drag-drop panels) | Kolla ships exporters for most services out of the box |
| Metrics (OpenStack + infra) | Zabbix | Medium (steeper learning curve, older UI) | Better for classic infra/agent-based monitoring, not OpenStack-native |
| Metrics (OpenStack + infra) | Telegraf + InfluxDB + Grafana | Medium-High | More setup work than Prometheus, good for time-series flexibility |
| Ceph-specific metrics | Ceph Dashboard (built-in) | Very High (zero extra install) | Best first stop for Ceph health/capacity |
| Ceph-specific metrics | Ceph Prometheus mgr module + Grafana | High | Can be merged into the same Grafana as OpenStack for single-pane view |
| Log Management | OpenSearch + OpenSearch Dashboards (Kolla default) | Medium-High | Built-in with Kolla; needs some query learning |
| Log Management | Graylog | High (simpler UI) | Good alternative if OpenSearch feels heavy |
| Log Management | ELK (Elasticsearch+Logstash+Kibana) | Medium | Heavier resource footprint, very customizable |
| Alerting | Prometheus Alertmanager | Medium (YAML config-based) | Integrates directly with Prometheus, industry standard |
| Alerting | Grafana Alerting (built-in) | High (GUI-based rule creation) | Easiest for teams already using Grafana dashboards |
| Alerting | Zabbix Alerting | Medium | Good if already using Zabbix as primary monitor |
