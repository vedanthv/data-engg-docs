## Quotas and Throttling in Kafka

Kafka’s **quota mechanism** is designed to control and balance how much data producers and consumers can send and receive, as well as how much time brokers spend serving client requests.
It ensures that no single client or user overwhelms the cluster, protecting performance and fairness across all users.

---

### 1. What quotas do

Kafka quotas help manage **throughput and resource usage** by defining **limits** on:

1. **Produce rate** — How fast producers can send data to Kafka (in bytes per second).
2. **Consume rate** — How fast consumers can fetch data from Kafka (in bytes per second).
3. **Request rate** — How much broker processing time clients can consume (as a percentage of total broker time).

In other words:

* **Produce quota** limits outgoing traffic from producers.
* **Consume quota** limits incoming traffic to consumers.
* **Request quota** limits the CPU or processing effort a broker dedicates to a client.

If clients exceed these quotas, Kafka **throttles** them — it delays requests to slow them down to the configured rate.

---

### 2. Types of quotas

#### a. **Produce quota**

* Controls the **rate at which producers can send data** to Kafka.
* Measured in **bytes per second**.
* Prevents aggressive producers from saturating network bandwidth or broker disk I/O.

Example:

```properties
quota.producer.default=2M
```

This means every producer can send up to **2 megabytes per second** by default.

If a producer exceeds this rate, the broker will **throttle** it — delaying further sends so the average rate stays within 2 MB/s.

---

#### b. **Consume quota**

* Controls the **rate at which consumers fetch data** from brokers.
* Also measured in **bytes per second**.
* Prevents a single consumer from monopolizing broker resources or network capacity.

Example:

```properties
quota.consumer.default=5M
```

This limits all consumers to fetching up to **5 MB/s** from the broker.

---

#### c. **Request quota**

* Controls how much **broker processing time** each client can consume.
* Expressed as a **percentage of broker time**.
* Ensures that one client cannot consume too much of the broker’s CPU cycles by sending too many small or complex requests.

Example:

```properties
quota.request.default=25
```

This would mean each client can consume up to **25% of the broker’s request-handling time** before being throttled.

---

### 3. Scope of quotas

Kafka allows you to define quotas at **different levels**:

| Level                            | Description                                                                                   |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| **Default**                      | Applies to all clients that don’t have custom settings.                                       |
| **User-specific**                | Applies to an authenticated Kafka user. Works only when security (authentication) is enabled. |
| **Client ID-specific**           | Applies to specific client applications identified by their `client.id` property.             |
| **User + Client ID combination** | Most specific level — applies to a particular client under a particular user identity.        |

Kafka uses the **most specific matching rule** when deciding which quota to apply.

---

### 4. Static vs Dynamic quotas

#### a. **Static quotas**

* Configured in the **Kafka broker configuration file** (e.g., `server.properties`).
* Example:

  ```properties
  quota.producer.default=2M
  quota.producer.override="clientA:4M,clientB:10M"
  ```
* These settings are **static**, meaning:

  * You must **edit the config file**.
  * You must **restart all brokers** for changes to take effect.
* Static quotas are suitable only for small, predictable environments.

---

#### b. **Dynamic quotas**

* Preferred in production environments.
* Configured **without restarting brokers**, using:

  * The **`kafka-configs.sh`** command-line tool, or
  * The **AdminClient API**.
* Dynamic configuration is stored in **ZooKeeper (pre-KIP-500)** or **Kafka’s internal configuration topics** (in KIP-500 and later versions).

Example command:

```bash
kafka-configs.sh --alter --add-config 'producer_byte_rate=4194304' \
--entity-type clients --entity-name clientA --bootstrap-server broker1:9092
```

This sets a **dynamic produce quota** of 4 MB/s for `clientA` (4194304 bytes).

Dynamic quotas take effect immediately and don’t require restarts.

---

### 5. Enforcement mechanism

Kafka brokers continuously **measure the data throughput** for each client and **apply throttling** when limits are exceeded.

* Throttling happens by **delaying responses** to producers or consumers.
* The broker maintains a **moving average** of data rate per client.
* If the rate exceeds the allowed quota, the broker inserts **artificial delay** before sending the acknowledgment (for producers) or response (for consumers).

This ensures the effective throughput remains below the configured limit while maintaining fairness.

---

### 6. Why quotas matter

Quotas are critical in large, shared Kafka clusters for:

* **Preventing resource starvation** — one misbehaving client can’t take down brokers.
* **Maintaining fair usage** across multiple teams or tenants.
* **Protecting system stability** under high load.
* **Avoiding network congestion** and I/O bottlenecks.

---

### Summary

| Quota Type  | Controls                  | Measured In      | Throttling Trigger           | Typical Use               |
| ----------- | ------------------------- | ---------------- | ---------------------------- | ------------------------- |
| **Produce** | Data sent by producers    | Bytes/sec        | Producer sends data too fast | Limit producer throughput |
| **Consume** | Data fetched by consumers | Bytes/sec        | Consumer reads too fast      | Balance consumer usage    |
| **Request** | Broker processing time    | % of broker time | Broker overloaded            | Prevent CPU overuse       |

---

In essence, Kafka quotas are a **governance and stability mechanism**. They provide administrators with precise control over how clients interact with the cluster — ensuring **performance isolation**, **fair resource distribution**, and **predictable system behavior** in multi-tenant or high-load environments.

### Some Code Examples

Limiting clientC (identified by client-id) to produce only 1024 bytes per second.

```bash
bin/kafka-configs --bootstrap-server localhost:9092 --alter --add-config
'producer_byte_rate=1024' --entity-name clientC --entity-type clients
```

Limiting user1 (identified by authenticated principal) to produce only 1024 bytes per second and consume only
2048 bytes per second.

```bash
bin/kafka-configs --bootstrap-server localhost:9092 --alter --add-config
'producer_byte_rate=1024,consumer_byte_rate=2048' --entity-name user1 --
entity-type users
```

```bash
bin/kafka-configs --bootstrap-server localhost:9092 --alter --add-config
'consumer_byte_rate=2048' --entity-type users
```

This section explains **how Kafka enforces quotas** once a client (producer or consumer) exceeds its configured rate limit.

Kafka doesn’t simply reject requests when a quota is exceeded — instead, it **throttles** the client to bring its data rate back within the allowed limits.

Let’s go step by step.

---

### 1. What happens when a client exceeds its quota

Each Kafka broker continuously tracks how much data each client is:

* **Producing** (sending to Kafka), or
* **Consuming** (fetching from Kafka).

If a client’s data rate (in bytes per second) goes above its allowed quota, the broker intervenes.

---

### 2. Throttling mechanism

When the broker detects that a client is over its quota, it **does not immediately block or disconnect** the client.
Instead, it **slows it down** by introducing *delays* in responses.

#### Example:

* Suppose a producer is allowed to send **2 MB/s**, but it starts sending **4 MB/s**.
* The broker calculates that it must **delay the next response** enough to bring the producer’s *average rate* back to 2 MB/s.
* So, if a producer sends a batch too quickly, the broker will **wait (throttle)** before sending back the acknowledgment.

This delay forces the producer to slow down, because most producer clients have:

* A **limited number of in-flight requests** (i.e., unacknowledged messages).
* When acknowledgments are delayed, new sends are paused or queued.
* As a result, the client’s **effective throughput automatically drops** to within the quota.

---

### 3. Mute mechanism (protecting the broker)

Kafka must also defend itself against **misbehaving clients** — ones that ignore backpressure or continue flooding the broker even while throttled.

To handle this, the broker can **mute the client’s network channel** temporarily.

#### What this means:

* The broker stops **reading requests** from the client’s socket for a short time.
* The client can still try to send data, but the broker won’t process or acknowledge it until the mute period ends.
* This enforces compliance by physically blocking the client from overwhelming the broker.

When the delay (throttle duration) expires, the broker **unmutes** the client and resumes communication normally.

---

### 4. Automatic self-regulation

This throttling process works smoothly because:

* Kafka producers and consumers are designed to handle backpressure naturally.
* The delay in acknowledgments (throttling) limits how fast they can send or fetch messages.
* No manual intervention is needed; the client’s behavior automatically adjusts to stay within quota limits.

---

### 5. Key points summarized

| Step                                       | What Happens                                                 | Purpose                                  |
| ------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------- |
| **1. Client exceeds quota**                | Broker detects higher-than-allowed data rate.                | Identify overload.                       |
| **2. Broker delays responses**             | Acknowledgments or fetch responses are held back.            | Slow down the client.                    |
| **3. Client self-adjusts**                 | Limited in-flight requests cause rate to drop automatically. | Maintain compliance.                     |
| **4. Broker mutes connection (if needed)** | Temporarily stops reading from the client’s socket.          | Protect broker from misbehaving clients. |
| **5. Resume normal flow**                  | Once average rate drops below quota.                         | Continue at allowed rate.                |

---

### 6. Why this design matters

This throttling system gives Kafka several advantages:

* **Graceful control** — Clients are slowed down, not disconnected.
* **Fairness** — No single producer or consumer can dominate broker resources.
* **Protection** — Brokers are shielded from overloading or denial-of-service–like behavior.
* **Transparency** — Clients need not be explicitly aware of throttling; it happens naturally through delayed responses.

---

### In essence:

When a client exceeds its quota:

* Kafka brokers **throttle** it by delaying responses.
* The client’s own request flow **slows down automatically** because of limited in-flight requests.
* If the client keeps misbehaving, the broker **mutes its network channel** temporarily.
* Once the quota balance is restored, **normal communication resumes**.

This ensures **stability, fairness, and protection** in multi-client Kafka environments without breaking client connections.

This section explains **how Kafka exposes throttling information to clients** through built-in **metrics**. These metrics let you monitor when and how much Kafka is throttling producer or consumer requests — an important indicator of whether clients are hitting their quota limits.

Let’s break this down in depth.

---

### 1. Purpose of throttling metrics

Kafka doesn’t just throttle clients silently — it also provides **metrics** so you can see:

* Whether throttling is happening.
* How severe it is (how long clients are being delayed).
* Which part of the system (produce or fetch) is affected.

These metrics are part of the client’s **JMX (Java Management Extensions)** or **producer/consumer metrics API**.

They help developers and administrators **detect performance bottlenecks** or **verify that quotas are correctly enforced**.

---

### 2. The key throttling metrics

Kafka exposes four main metrics related to quota throttling:

| Metric Name                     | Applies To | Description                                                                                            |
| ------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------ |
| **`produce-throttle-time-avg`** | Producer   | The **average amount of time (in milliseconds)** that produce requests were delayed due to throttling. |
| **`produce-throttle-time-max`** | Producer   | The **maximum time** that any single produce request was delayed due to throttling.                    |
| **`fetch-throttle-time-avg`**   | Consumer   | The **average time** that fetch requests (data pulls) were delayed due to throttling.                  |
| **`fetch-throttle-time-max`**   | Consumer   | The **maximum delay** applied to any single fetch request.                                             |

These metrics represent how much the broker delayed responses — the higher the numbers, the more the client was throttled.

---

### 3. What causes these throttles

There are two main reasons a Kafka broker will throttle a client, and both are reflected in these metrics:

1. **Throughput quotas**

   * When a producer or consumer exceeds its configured data rate limit (bytes per second).
   * The broker delays responses to slow the client down.
   * These throttles show up in the `produce-throttle-time-*` and `fetch-throttle-time-*` metrics.

2. **Request-time quotas**

   * When a client uses too much broker CPU or I/O time.
   * The broker throttles the client to ensure fair resource sharing.
   * These throttles also appear in the same metrics, since they affect request processing time.

So, the reported throttling time could reflect **either throughput-based throttling, request-time throttling, or both**.

---

### 4. Example interpretation

Suppose you’re monitoring a producer client and see:

```
produce-throttle-time-avg = 300 ms
produce-throttle-time-max = 1200 ms
```

This means:

* On average, the producer’s requests were delayed by **300 milliseconds** before being acknowledged.
* At some point, one request was delayed by as much as **1.2 seconds**.

This strongly suggests the producer is exceeding its **produce quota** (e.g., sending too many bytes per second).

Similarly, for consumers:

```
fetch-throttle-time-avg = 500 ms
fetch-throttle-time-max = 2000 ms
```

indicates the consumer is reading data faster than allowed.

---

### 5. Other client requests

The metrics above specifically measure throttling of **produce** and **fetch** requests.
However, Kafka also throttles **other types of requests** — such as metadata requests, offset fetches, or administrative operations — but only under **request-time quotas**.

For those, similar metrics exist, usually exposed under:

```
request-throttle-time-avg
request-throttle-time-max
```

These help monitor general throttling behavior across all client interactions with the broker.

---

### 6. How to use these metrics

Monitoring these metrics is essential for:

* **Performance tuning:** Detecting if producers or consumers are frequently throttled (indicating quota limits are too low).
* **Quota enforcement validation:** Confirming that quotas are actively controlling data rates as intended.
* **Cluster health checks:** Identifying overloaded brokers or imbalanced client workloads.
* **Application optimization:** Adjusting client configurations (e.g., batch size, linger time, fetch size) to avoid hitting throttling limits.

In most cases, Kafka clients expose these metrics through:

* **JMX exporters** (for Prometheus or Grafana dashboards).
* The **Kafka AdminClient metrics API**.
* Tools like **Confluent Control Center** or **Kafka Manager**.

---

### 7. Summary

| Metric                      | Applies To  | Meaning                                    | Indicates                      |
| --------------------------- | ----------- | ------------------------------------------ | ------------------------------ |
| `produce-throttle-time-avg` | Producer    | Average time produce requests were delayed | Ongoing throttling             |
| `produce-throttle-time-max` | Producer    | Longest delay of any produce request       | Severity of throttling         |
| `fetch-throttle-time-avg`   | Consumer    | Average delay in fetch responses           | Consumer throttled             |
| `fetch-throttle-time-max`   | Consumer    | Maximum delay for any fetch request        | Peak throttling event          |
| `request-throttle-time-*`   | All clients | Delay for non-produce/fetch requests       | Request-time quota enforcement |

---

### In summary

Kafka provides **throttling metrics** to make quota enforcement transparent.
They measure **how long client requests are being delayed** by brokers, helping identify when clients exceed configured **throughput or request-time quotas**.

By observing these metrics, administrators can:

* Confirm that throttling is happening as expected,
* Diagnose overactive clients,
* And fine-tune quotas for fair, balanced, and efficient Kafka cluster performance.
