## Cluster Membership in Kafka

Every broker has a unique identifier which is in broker configuration or automatically granted.

It registers itself with its ID in Zookeeper by creating ephermal node and some of the ecosystem tools subscribe to /broker/ids path in Zookeeper to get notified when brokers are added or removed. 

If we try to create another broker with same Id we get error.

When a broker loses connectivity, the ephehermal node automatically gets removed from Zookeeper.

If the broker is part of the replicas, the new one immediately takes its place and partitions depending on the rebalancing technique used.

### The Controller

The controller node is resposible for electing partition leaders.

The first broker that joins the cluster becomes the controller by creating */controller* ephemeral node.

When other brokers try to become controller, they get "node already exists exception".

When the controller stops sending heartbeats, the other brokers get this notification through Zookeeper and will attempt to create the controller themselves.

The first node that's successful becomes new controller, each time a new one is elected it receives a higher **controller epoch number** through Zookeeper conditional increment operation.

The brokers know the current highest epoch number and if they recieve pings from a controller with lower number they ignore it.

This is important because the controller broker can disconnect from ZooKeeper due to a long garbage collection pause—during this pause a new controller will be elected. When the previous leader resumes operations after the pause, it can continue sending messages to brokers without knowing that there is a new controller—in this case, the old controller is considered a zombie. The controller epoch in the message, which allows brokers to ignore messages from old controllers, is a form of zombie fencing.

# Kafka controller startup, leader election, and replica state transitions — detailed explanation

When a Kafka cluster boots or a controller process starts, it must first learn the *current cluster state* before it can safely manage metadata and perform leader elections. That initial bootstrapping and the subsequent response to broker failures are what keep the cluster available and consistent. Below is a step-by-step, in-depth description of what happens, why it matters, and the key implementation and operational details.

## Controller bootstrap: loading the replica state map

1. **What the controller needs**
   The controller is the broker responsible for cluster-wide metadata decisions (which partition has which leader, triggering reassignments, orchestrating topic creations/deletions, etc.). To make correct decisions it needs the most recent view of:

   * the list of brokers,
   * the replica assignment for every partition (which replicas exist and their order),
   * the last known leader and in-sync replica (ISR) sets,
   * ongoing partition state (e.g., under-replicated partitions, preferred leader info).

2. **Reading from ZooKeeper**
   Historically Kafka stored this metadata in ZooKeeper. On startup the controller reads the replica state map and related znodes. Because many partitions exist in production clusters, this read is not a single small call but many metadata reads. To avoid being dominated by per-request latency, the controller issues *pipelined asynchronous* read requests to ZooKeeper. Pipelining means it fires many async reads in parallel and handles responses as they arrive, rather than waiting for each one sequentially. This hides round-trip latency and reduces total load time.

3. **Why it can take seconds**
   Even with pipelining, large clusters (hundreds of brokers / tens or hundreds of thousands of partitions) can require reading many znodes and reconstructing in-memory maps. The controller must validate and merge states, detect inconsistencies, and often rehydrate caches. Kafka performance tests have shown this can take several seconds in large clusters — a meaningful window during which the cluster is not making leader changes.

## Detecting broker departure

1. **How the controller notices a broker is gone**
   The controller watches ZooKeeper paths that reflect broker liveness (ephemeral znodes written by brokers) or receives an explicit `ControlledShutdownRequest` from a broker that is shutting down gracefully. An ephemeral znode disappears if the broker process or network session dies; ZooKeeper notifies the controller.

2. **Scope of work when a broker dies**
   Any partition for which the departed broker was the leader now needs a new leader. The controller enumerates those partitions and determines the new leader for each.

## Choosing the new leader

1. **Replica list order**
   Each partition has a configured *replica list* — an ordered list of broker IDs that hold replicas. The controller typically picks the next eligible replica in that list as the new leader. Eligibility depends on whether the replica is in the partition’s ISR (in-sync replicas). If the first replica in the list is unavailable, the controller picks the next ISR replica, and so on. If no ISR replica is available, the controller may elect a non-ISR (depending on configuration), but that risks data loss.

2. **Leadership selection rules**
   Kafka respects the invariant that a new leader should be as up-to-date as possible (prefer ISR). Configuration flags control whether the controller may choose out-of-sync replicas in exceptional cases (for availability).

## Persisting state and broadcasting changes

1. **Persisting to ZooKeeper**
   After deciding new leaders and updated ISR sets, the controller persists the updated partition state back to ZooKeeper. Like reads, these writes are issued via pipelined asynchronous requests to reduce latency and increase throughput. Persisting ensures the authoritative state is durably stored and visible to any other controller or admin tooling that reads ZooKeeper.

2. **LeaderAndISR requests**
   Once the new state is persisted, the controller sends `LeaderAndIsr` requests to every broker that holds replicas for the affected partitions. These are broker-to-broker RPCs that tell each replica who the new leader is, what the updated ISR set is, and other metadata required for replication coordination. The controller batches these updates: rather than sending a separate request for each partition, it groups multiple partition updates that affect the same broker into a single `LeaderAndIsr` RPC to reduce overhead.

3. **UpdateMetadata broadcast**
   Kafka brokers cache cluster metadata (topics, partitions, leaders, replicas). To keep those caches fresh, the controller sends `UpdateMetadata` requests to all brokers, which contain the new leadership information for changed partitions. After receiving this, brokers update their `MetadataCache` so that producers and consumers hitting them later will discover the new leaders.

## Broker roles after a leadership change

1. **New leader behavior**
   A broker that becomes the leader for a partition begins serving client requests immediately for that partition (subject to any internal checks). It accepts producer writes and responds to consumer fetches for the partition’s offsets.

2. **Follower behavior**
   Followers learn their new status from `LeaderAndIsr` and start replicating messages from the leader. They must pull messages and apply them to their local log to catch up.

3. **Catch-up and ISR maintenance**
   A replica rejoins the ISR only after it has caught up to the leader’s high watermark (or otherwise met the configured replication criteria). The controller tracks ISR membership; when followers fall behind they may be removed from ISR, which affects future leader election safety.

## Broker rejoin and recovery

1. **Broker starts back up**
   When a previously dead broker returns, it registers with ZooKeeper and reports the replicas it hosts. Initially, those replicas are treated as followers and must replicate from the partition leaders to catch up.

2. **Eligibility for leadership**
   Only after catching up and rejoining the ISR will those replicas be eligible to become leaders in later elections. This prevents electing a lagging replica that could cause data loss.

## Efficiency and operational considerations

1. **Batching and pipelining**
   The controller batches `LeaderAndIsr` and `UpdateMetadata` requests by destination broker, reducing RPC overhead. Pipelining ZooKeeper reads/writes hides latency but requires careful handling of ordering and error cases.

2. **Latency vs safety trade-offs**
   Sometimes administrators prefer faster availability (elect any replica) and accept potential data loss; other times the cluster prioritizes durability and waits for ISR replicas. Kafka exposes configuration knobs to tune this behavior (e.g., unclean leader election settings).

3. **Scale limits**
   Large partition counts slow initial controller load and can lengthen the time to converge after failures. Operators reduce impact by judicious partition counts, careful controller placement, and monitoring controller load and ZooKeeper throughput.

4. **Future changes**
   Later Kafka architectures replace ZooKeeper with an internal quorum (KRaft); the high-level flow (bootstrapping metadata, leader election, persisting state, notifying brokers) remains conceptually similar though implemented without external ZooKeeper.

## Summary

The controller’s work — reading the current replica state, deciding leaders on broker failure, persisting changes, and notifying brokers — is the choreography that keeps Kafka available and consistent. Pipelined async I/O and request batching optimize latency at scale, but large partition counts still impose measurable startup and failover delays. The design balances availability, durability, and scalability through ISR semantics, batching, and configurable election policies.