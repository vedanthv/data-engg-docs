## Production Concerns in Kafka
---

### 1. Garbage Collection Before G1GC

* Tuning Java GC was difficult and required a lot of trial and error.
* Developers had to carefully adjust GC options based on how the application used memory.
* Different workloads often required different GC tuning strategies.

---

### 2. Introduction of G1GC

* G1GC (Garbage-First Garbage Collector) was introduced in **Java 7**.
* Initially, it was not stable enough for production.
* By **Java 8 and Java 11**, it had matured significantly.
* Kafka now recommends **G1GC as the default GC**.

---

### 3. Why G1GC is Better

* **Adaptive**: Automatically adjusts to different workloads without requiring heavy manual tuning.
* **Consistent Pause Times**: Designed to provide predictable, shorter GC pauses (important for systems like Kafka that need low latency).
* **Scales with Large Heaps**:

  * Older collectors would stop and scan the entire heap during GC.
  * G1GC divides the heap into smaller regions (zones).
  * It collects garbage region by region instead of the whole heap at once, which reduces pause times.

---

### 4. Configuration Simplicity

* Unlike older collectors, G1GC requires **minimal manual tuning** for most use cases.
* Out-of-the-box defaults are good enough for many production environments, including Kafka.

### Parameters

**MaxGCPauseMillis** : Preferred but not strict pause time for each GC cycle. By default its 200ms.

**InitiatingHeapOccupancyPercent** : Specifies total heap that may be in use before garbage collection comes into force. Default is 45. This includes both old and new zone.

## Production Concerns : Datacenter Layout

---

### 1. What is Rack Awareness

* Kafka stores multiple replicas of a partition for fault tolerance.
* If all replicas of a partition are placed on brokers in the same rack, they could all fail together if that rack loses power or network connectivity.
* Rack awareness ensures that replicas for a partition are spread across different racks or fault domains.
* To enable this, each broker must be configured with its rack location using the `broker.rack` property.

---

### 2. How It Works in Practice

* When new partitions are created, Kafka places their replicas across racks so they don’t share the same rack.
* In cloud environments, `broker.rack` can be mapped to a cloud “fault domain” or “availability zone” for the same benefit.
* Important limitation:

  * Rack awareness is only applied at partition creation.
  * Kafka does not automatically re-check or fix replicas if they later end up on the same rack (for example, due to manual partition reassignment).

---

### 3. Maintaining Rack Awareness

* Because Kafka does not self-correct rack misplacements, you need external tools to maintain balance over time.
* One common tool is **Cruise Control**, which helps monitor and rebalance partitions while respecting rack awareness.
* Regular balancing ensures that partitions remain fault-tolerant across racks.

---

### 4. Best Practices for Infrastructure

* Ideally, each Kafka broker should be in a different rack to maximize fault tolerance.
* At minimum, brokers should avoid sharing the same single points of failure for power and networking.
* Recommendations:

  * Use **dual power connections** (to different power circuits).
  * Use **dual network switches** and configure bonded interfaces for failover.
* Even with redundancy, placing brokers in separate racks provides stronger resilience.
* This is also useful for planned maintenance, where a rack may need to be taken offline temporarily.

---

### 5. Key Takeaway

* Rack awareness ensures partition replicas are distributed across failure domains.
* You must set `broker.rack` correctly for each broker.
* Kafka applies this only when partitions are created; you need rebalancing tools like Cruise Control to maintain it.
* For hardware resilience, brokers should be deployed across racks, with redundant power and networking.

## Production Concerns : Colocating Applications on Zookeeper

Writes to Zookeeper is are only performed when consumer groups are updated or changes on cluster is made. So we do not need dedicated Zookeeper for single Kafka cluster, it can be shared across clusters.

Consumers have a choice of using Zookeeper or Kafka for commiting offsets. Each consumer will perform a zookeeper write for every partition it consumes and dafault is 1 minuute. In this timeframe, the consumer may read duplicate messages. If multiple consumers write at same time we may end up with concurrent write issues.
