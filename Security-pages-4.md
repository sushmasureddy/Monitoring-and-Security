# Network Security & Segmentation

Network segmentation separates management, tenant, external, and storage
traffic so that none of them share a reachable network by accident. In a
multi-node data center deployment this is arguably the single most
impactful control available, because it is what limits how far an
attacker can move after any one compromise, a single compromised tenant
instance should never be able to reach the database or the message
queue, no matter what happens inside that instance.

Separate VLANs are assigned per traffic type, security groups deny all
traffic by default, and management-plane ports are explicitly firewalled
off from tenant subnets. Segmentation is then verified directly, by
attempting the forbidden connection and confirming it fails, rather than
trusted to have worked simply because the configuration looks correct on
paper.

| Control | Implementation |
|---|---|
| VLAN / physical segmentation | Management/API, tenant, external, and Ceph storage traffic placed on separate VLANs or physical networks, never sharing a broadcast domain. |
| Deny-by-default security groups | `openstack security group rule create --protocol tcp --dst-port <port> --remote-ip <trusted-cidr> <group>`, every instance starts closed, only required ports opened. |
| Management-plane firewalling | iptables/nftables rules on controller nodes blocking tenant subnets from reaching RabbitMQ (5672), MariaDB (3306), and Ceph mon (6789) ports. |
| Ceph network split | Public (client-facing) and cluster (replication) Ceph networks kept separate, so replication traffic has neither the bandwidth exposure nor the reachability of client traffic. |
| Verification | Segmentation is tested directly, attempt to reach management-plane ports from a tenant instance and confirm the connection fails, rather than assuming the rule works. |

> **Common pitfalls**

- Assuming a VLAN configuration works because it was applied, without
  ever testing reachability from a tenant instance.

- Leaving a broad debugging security-group rule (e.g. allow-all from
  0.0.0.0/0) in place after troubleshooting is finished.

- Forgetting that a newly added node needs the same segmentation applied
  before it joins the cluster, not after.
