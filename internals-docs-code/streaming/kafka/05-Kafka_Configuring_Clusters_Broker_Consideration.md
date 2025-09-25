## Broker Considerations while Configuring Clusters

Having multiple brokers allows us to scale the load across multiple servers. Secondly we can guard against data loss due to single system failures.

Replication will allow us to perform maintainance work without downtime to consumers.

<img width="812" height="685" alt="image" src="https://github.com/user-attachments/assets/053211d1-e87f-447b-a23c-c920092cb94f" />

### How many brokers?

<img width="762" height="306" alt="image" src="https://github.com/user-attachments/assets/e2aad2fb-8746-4a6f-a84e-76046ef89ec6" />

**Disk Capacity**

If cluster is require to maintain 10 TB data, and each broker can hold 5 Tb we need 5 brokers.

Replicas can again change this math, if we need to have two replicas per broker then we would need 20Tb.

<img width="1389" height="382" alt="image" src="https://github.com/user-attachments/assets/fabd6c72-9c5a-4696-b1d9-9d625251f33d" />

**CPU**

Not a major cause of problem but if we have excessive client connections then we need to rev up CPU.

**Networking**

<img width="1262" height="506" alt="image" src="https://github.com/user-attachments/assets/480d1bfa-2b55-498f-b867-9f5ade486519" />

### Broker Configurations

There are only two requirements for a broker to be part of the cluster:

1. They must have same configuration for zookeeper.connect
2. They must have unique ```broker.id```
