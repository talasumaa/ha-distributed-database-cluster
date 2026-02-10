#!/bin/bash
# High Availability Cluster Setup Script - Reconstruction

# 1. Cluster Authorization & Setup
pcs host auth db1 db2 db3 -u hacluster -p "${HACLUSTER_PASSWORD}"
pcs cluster setup ha_cluster db1 db2 db3 --force
pcs cluster start --all
pcs property set stonith-enabled=false # Note: In prod, use fence_xvm

# 2. Create Floating IP Resource (VIP)
# The IP 192.168.205.70 will float between active nodes
pcs resource create ClusterIP ocf:heartbeat:IPaddr2 \
    ip=192.168.205.70 \
    cidr_netmask=24 \
    op monitor interval=30s

# 3. Constraint Configuration (Optional for Galera active-active)
# Ensures IP prefers a specific node if needed, or stickiness
pcs constraint location ClusterIP prefers db1=50