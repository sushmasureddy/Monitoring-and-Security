# Alternative Approaches Considered

Each of the following was evaluated and rejected in favor of the
recommendation in section 12. Deployment steps are included for
completeness and reference only.

# Zabbix Route

- Install Zabbix server + Zabbix web frontend: separate installation,
  not part of Kolla-Ansible at all.

- Install a Zabbix agent on every node: Nova compute nodes, controller,
  storage nodes, all of them.

- Manually write or find community templates to query OpenStack APIs
  (Nova, Neutron, Keystone, Cinder): Zabbix does not understand
  OpenStack natively.

- Manually write checks for Ceph: no first-party Ceph integration,
  either scripts or third-party templates of varying quality.

- Build custom dashboards inside Zabbix's UI (older, less flexible than
  Grafana).

- Configure Zabbix's built-in alerting/triggers.

## Ceph Dashboard (Alone) Route

- Turn it on: 'ceph mgr module enable dashboard'; it is already built
  into ceph-mgr, nothing extra to install.

- Create a login: set up an admin username and password so you can
  access the web UI.

- Secure it: enable SSL/TLS (self-signed or a real certificate) since
  it is a web frontend.

- Open it: find the URL via 'ceph mgr services' (default port 8443)
  and log in to see cluster health, OSD status, and pool usage live.

- Know its limit: it only sees Ceph; it has zero visibility into Nova,
  Neutron, Keystone, or any other OpenStack service.

# Telegraf + InfluxDB + Grafana Route

- Install InfluxDB: a separate database, not part of Kolla-Ansible, to
  store all the metrics.

- Install Telegraf on every node: this is the agent that actually
  collects the metrics from each node.

- Set up plugins: host metrics are easy to enable, but OpenStack and
  Ceph need manual/custom plugin work since Telegraf does not
  understand them natively.

- Connect the pieces: Telegraf sends data to InfluxDB, then Grafana
  connects to InfluxDB to display it.

- Build it yourself: fewer ready-made dashboards exist for this combo,
  so most panels and alerts have to be built manually.

## ELK / OpenSearch (Alone) Route

- Install the stack: Elasticsearch/OpenSearch (storage + search
  engine), plus Logstash or Fluentd/Fluent Bit (log shipper), plus
  Kibana or OpenSearch Dashboards (UI): three separate components to
  set up.

- Ship logs from every node: an agent (Fluentd/Fluent Bit/Logstash)
  runs on each node, reading container and service logs and forwarding
  them in.

- Index and search logs: Elasticsearch/OpenSearch stores logs so you
  can search by service, error, timestamp, or keyword.

- Know its limit: it is built for logs, not metrics; it cannot show OSD
  latency, API response times, CPU/disk trends, or trigger
  threshold-based alerts the way Prometheus + Grafana can.

- Best used alongside, not instead of: this route answers "why did it
  fail" from logs, but Prometheus + Grafana is still needed to know
  "something is wrong" in the first place.

## Nagios/Icinga Route

- Install Nagios or Icinga server: separate installation, not part of
  Kolla-Ansible.

- Install NRPE/agent on every node: controller, network, compute,
  storage nodes each need a check agent.

- Write or find plugins for each check: OpenStack, Ceph, MariaDB,
  RabbitMQ each need their own custom check script.

- Define hosts and services manually: every node and every check gets
  configured by hand in config files.

- Know its limit: it is check-based (up/down, OK/WARNING/CRITICAL
  only), not metrics/time-series based, so it cannot show capacity
  trends or latency graphs.

## Two Separate Grafana Instances (One per System) Route

- Set up Grafana 1 for OpenStack: connected to the Prometheus instance
  scraping Nova, Neutron, Keystone, HAProxy, MariaDB, RabbitMQ, and
  hosts.

- Set up Grafana 2 for Ceph: connected separately to the Ceph
  Prometheus mgr module (port 9283), with Ceph's own dashboards
  imported.

- Keep both running independently: two logins, two URLs, two sets of
  dashboards to maintain and upgrade.

- Check both during an incident: during a slowdown or failure, an
  operator must manually flip between two screens and mentally line up
  timestamps.

- Know its limit: it technically works and needs no new tooling, but it
  defeats the purpose of unified monitoring since nothing correlates
  OpenStack and Ceph on one screen automatically.
