# RunBook

First-response steps for the most common alert categories in this
deployment:

# Ceph OSD Down / Degraded PGs

- Check overall cluster state with \'ceph -s\' and identify the affected
  OSD(s).

- Check the OSD host is reachable and the underlying disk has not
  failed.

- Restart the OSD container/service if the host and disk are healthy.

- If the disk has failed, mark the OSD out, let the cluster rebalance,
  then replace the disk.

- Confirm PG state returns to active+clean before considering the
  incident closed.

## Galera Node Out of Sync

- Check wsrep_local_state_comment on each node to identify which node is
  not in the \'Synced\' state.

- Confirm the remaining nodes still hold quorum before taking any node
  offline for repair.

- Restart the affected node so it performs an IST/SST resync from a
  donor node.

- Monitor replication lag until it returns to zero before sending
  traffic back to that node.

## API Endpoint Unreachable (HAProxy/VIP)

- Confirm which node currently holds the VIP with \'ip addr\' /
  Keepalived status.

- Check HAProxy backend status for the affected service on the active
  node.

- Check the underlying service container is running and healthy on all
  backend nodes.

- Fail the VIP over manually if Keepalived has not already done so and
  the active node is unhealthy.

## Certificate Expiry Warning

- Identify which endpoint\'s certificate is expiring from the
  Alertmanager notification.

- Renew via cert-manager if automated renewal is configured, otherwise
  renew manually.

- Run \'kolla-ansible reconfigure\' to push the renewed certificate to
  the relevant containers.

- Verify the new expiry date with a blackbox_exporter probe or a manual
  TLS check.

## RabbitMQ Queue Backlog

- Identify the affected queue and its consumer count from the RabbitMQ
  management UI or Grafana panel.

- Check whether the consuming service (e.g. nova-conductor,
  nova-scheduler) is running and healthy on all controller nodes.

- Restart the stalled consumer service if it is running but not
  processing messages.

- Monitor queue depth until it trends back toward zero; escalate if
  backlog continues to grow after the restart, since this can indicate a
  downstream dependency (database, API) is also degraded.

## Host Disk Usage Critical

- Identify the affected node and mount point from the Alertmanager
  notification.

- Determine the largest consumer of space --- typically container logs,
  old image layers, or a full Glance/Cinder local cache.

- Clear or rotate logs manually if logrotate has fallen behind; prune
  unused Docker images/volumes if safe to do so.

- If usage is a genuine capacity issue rather than reclaimable waste,
  escalate for storage expansion and review the monthly capacity trend
  (section 3) to prevent recurrence
