# Live Demo - Distributed Database Cluster Testing Commands

## Cluster Status and Monitoring

### Check Galera Cluster Status

sudo mysql -u root -pgaleraadmin -e "SHOW STATUS LIKE 'wsrep_cluster_size'; SHOW STATUS LIKE 'wsrep_cluster_status'; SHOW STATUS LIKE 'wsrep_ready'; SHOW STATUS LIKE 'wsrep_connected';"

### Check Pacemaker/Corosync Status

sudo pcs status

### Monitor Cluster Status in Real-time

watch -n 1 sudo pcs status

## Database Connectivity and Verification

### Verify Database Hostname

mysql -u root -h 192.168.205.70 -p -e "SELECT @@hostname;"

### Connect to Database

mysql -u root -h 192.168.205.70 -p

## Data Replication Testing

### Write Test Data

USE cluster_test;
INSERT INTO replicated_data VALUES (4, 'Live-Demo');
EXIT;

### Verify Data Replication

mysql -u root -h 192.168.205.70 -p -e "SELECT * FROM cluster_test.replicated_data;"

## Failover and Recovery Testing

### Simulate Node Failure

sudo killall -9 corosync

### Recover Failed Node

sudo systemctl start corosync
sudo systemctl start pacemaker
