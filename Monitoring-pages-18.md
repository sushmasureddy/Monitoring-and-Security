# Appendix A: Glossary of Terms

Terms used throughout this document, defined in plain language for
readers without prior OpenStack or Ceph background.

| Term | Meaning |
|---|---|
| OSD (Object Storage Daemon) | The Ceph process that manages one physical disk, storing and serving the actual data. |
| PG (Placement Group) | A logical grouping of stored data inside a Ceph pool, used to distribute data across OSDs. |
| Pool | A named logical partition inside Ceph where a category of data (e.g. Cinder volumes) is stored. |
| RBD (RADOS Block Device) | Ceph's block storage interface, used by Cinder and Nova to store volumes and instance disks. |
| cephx | Ceph's authentication system; each OpenStack service connects to Ceph using its own cephx keyring/credential. |
| VIP (Virtual IP) | A single floating IP address shared by multiple nodes (via HAProxy/Keepalived) so traffic keeps flowing if one node fails. |
| Quorum | The minimum number of database (Galera) nodes that must agree before the cluster is considered consistent and safe to serve traffic. |
| wsrep_* | A family of status variables reported by Galera showing replication state, lag, and cluster size. |
| Exporter | A small agent that reads metrics from a system and exposes them in a format Prometheus can scrape. |
| Scrape | The act of Prometheus fetching (pulling) metrics from an exporter's /metrics endpoint. |
| PromQL | Prometheus's query language, used to filter, calculate, and aggregate stored metrics. |
| IOPS (I/O Operations Per Second) | A count of how many read or write requests a storage system handles per second. |
| Amphora | The virtual machine Octavia uses to run an actual load balancer instance for a tenant. |
| CADF | Cloud Auditing Data Federation — the audit event format used by Keystone/Nova/Neutron for logging 'who did what'. |
| Cephadm | The tool used to deploy and manage a Ceph cluster, independent of Kolla-Ansible. |
