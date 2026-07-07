# OpenStack Cloud Infrastructure Operations Guide

> **Monitoring, Maintenance, Updates, Security, and Migration**

# Deployment Overview

- This document explains, in order, how the OpenStack cloud deployed
  with Kolla-Ansible 2026.1 (Gazpacho) is monitored, maintained, backed
  up, updated, and secured/migrated in a data center setting.

- Kolla-Ansible deploys every OpenStack service as a Docker container,
  driven from a central Ansible inventory (globals.yml, passwords.yml,
  multinode inventory file).

- This container-based, Ansible-driven model is why the monitoring and
  operations tooling in this document is chosen the way it is.

- The same layers host OS, Docker containers, OpenStack APIs, database,
  message queue --- exist on every node.

- Because those layers repeat identically across nodes, the same small
  set of tools can cover the whole deployment consistently.

### Deploying the Monitoring & Logging Stack Before Workload Onboarding

- Prometheus, Grafana, and exporters (node_exporter, openstack-exporter,
  blackbox_exporter, mysqld_exporter, etc.) are installed and confirmed
  scraping data from every node before any tenant traffic is allowed
  onto the cloud.

- Fluentd (or Fluent Bit), OpenSearch, and OpenSearch Dashboards are
  stood up as a separate pipeline so container and service logs are
  centralized and searchable from day one, not bolted on after an
  incident.

- This step happens right after \'kolla-ansible post-deploy\' validation
  and before tenants, networks, or workloads are onboarded, so there is
  a clean historical baseline to compare against later.

- Deploying monitoring first means the very first real incident already
  has metrics history and log history to investigate, instead of
  starting blind.

- Skipping this step or deploying it late is a common mistake --- it
  leaves a \"monitoring gap\" where early issues go undetected simply
  because nothing was watching yet.

### Ceph Integration Architecture

- Ceph is deployed externally to the OpenStack control plane, using
  cephadm as the orchestration tool, and is not managed by
  Kolla-Ansible.

- OpenStack integrates with this external Ceph cluster through dedicated
  RBD pools (e.g. volumes, images, vms) and cephx keyrings scoped per
  service, so each OpenStack service authenticates to Ceph with its own
  least-privilege credential.

- Ceph serves as the actual storage backend for three core services:
  Glance (images), Cinder (block volumes), and Nova
  (ephemeral/boot-from-volume instance disks).

- Because the persistent data lives on Ceph rather than inside the
  OpenStack API layer itself, monitoring, backup, and maintenance for
  storage are treated as Ceph-first throughout this

document the OpenStack API shows whether an operation succeeded, and the
Ceph layer shows why it might be slow or failing.
