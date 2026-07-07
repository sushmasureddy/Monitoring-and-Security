# Recommended Deployment: Prometheus + Grafana Route

- Enable in Kolla-Ansible: set `enable_prometheus: "yes"`,
  `enable_grafana: "yes"` in globals.yml.

- Run 'kolla-ansible reconfigure' (or deploy): Kolla automatically
  installs Prometheus, Grafana, and the exporters (node_exporter,
  openstack-exporter, blackbox_exporter, mysqld_exporter) as containers
  on your nodes, and wires them to auto-scrape.

- Enable Ceph's own exporter: turn on ceph-mgr's Prometheus module, get
  its port via 'ceph mgr services'.

- Add Ceph as a scrape target in Prometheus config: one line, tells
  Prometheus "also collect from here".

- Import ready-made dashboards into Grafana: dashboard ID 9701/21085 for
  OpenStack, 2842 for Ceph — a few clicks, no building from scratch.

- Set alert rules in Prometheus and hook up Alertmanager for
  notifications.
