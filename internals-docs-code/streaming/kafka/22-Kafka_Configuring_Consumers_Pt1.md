## Configuring Consumers in Kafka - Part 1

### 1. ```fetch.min.bytes```

This property allows a consumer to specify the minimum amount of data that it wants to receive from the broker. If the batch size is less than 1KB(default) then the consumer waits.

This reduces the load on both broker and consumer as they dont have to handle back and forth requests.

If the consumer is using too much CPU then we need to set this param higher but if there are lot of consumers then we need to set the value lower so that the other consumers 
dont wait for a very long time for their request to be considered by broker.

Tuning this property could introduce higher latency than usual.

### 2. ```fetch.max.wait.ms```

We are telling Kafka to wait before it has enough data to sendto consumer. By default Kafka waits for 500 ms. This introduce a latency of 500ms if kafka doesnt have enough data to send to consumer. 

If we want to control latency it can be set to 10ms and fetch.min.bytes to 1MB.

Kafka broker will respond when the data is either 1MB or 100ms has passed.

### 3. ```fetch.max.bytes```

The `fetch.max.bytes` property in a Kafka consumer controls the **maximum amount of data (in bytes)** the consumer can receive from the broker in a single fetch request.

Here’s what it means in detail:

* **Purpose:** It limits how much data the consumer will store in memory per poll request, regardless of how many partitions or messages are included in that data.
* **Default Value:** 50 MB.
* **Behavior:**

  * When a consumer calls `poll()`, the broker sends data up to this size limit.
  * However, if the **first batch of messages** available for a partition is larger than this limit, the broker will still send that entire batch — ignoring the limit temporarily — to ensure the consumer keeps making progress and does not get stuck.
* **Broker Side Control:**

  * The broker also has its own limit through the `message.max.bytes` (for producer messages) and `max.message.bytes` or `max.partition.fetch.bytes` (for consumers) configurations.
  * These ensure that a single fetch request or message doesn’t overload the broker or network.
* **Performance Consideration:**

  * Setting this value too high can cause large memory usage and long network transfers.
  * Setting it too low can cause the consumer to make frequent fetch requests, reducing efficiency.

In short, `fetch.max.bytes` helps balance **memory usage**, **network load**, and **fetch frequency** on the consumer side.

### 4. ```max.poll.records```

Controls max number of records that a single poll of broker can fetch.

### 5. ```max.partition.fetch.bytes```

---

#### **Definition**

`max.partition.fetch.bytes` specifies the **maximum number of bytes the broker will return for each partition** in a single fetch request.
The default value is **1 MB**.

---

#### **How It Works**

* When the consumer sends a fetch request, the broker looks at **each partition** the consumer is subscribed to.
* The broker sends up to `max.partition.fetch.bytes` of data **per partition** in that request.
* So if a consumer is reading from multiple partitions, the total data returned can be up to:

  ```
  total bytes ≈ number of partitions × max.partition.fetch.bytes
  ```

---

#### **Example**

If a consumer reads from 5 partitions and `max.partition.fetch.bytes = 1MB`,
the broker could return **up to 5 MB** of data in one poll.

---

#### **Important Note**

* If the **first record batch** in a partition is larger than this value, Kafka will **still send it** (ignoring the limit temporarily) to ensure progress.
* Managing consumer memory through this property can be tricky because you can’t easily control how many partitions the broker will include in a single response.

---

#### **Recommendation**

Because it’s difficult to predict and control total memory use across multiple partitions, it’s **usually better to tune `fetch.max.bytes`** instead.
That property sets a **global upper limit** on how much data the consumer fetches in total per request, making it easier to manage memory and network load.

---

**In short:**

* `max.partition.fetch.bytes` → limits data per partition (default 1 MB)
* `fetch.max.bytes` → limits total data per fetch request (default 50 MB)
* Use `fetch.max.bytes` for general memory control; use `max.partition.fetch.bytes` only when you need fine-grained control per partition.

### 6. ```session.timeout.ms``` and ```heartbeat.interval.ms```

#### **1. What It Does**

`session.timeout.ms` specifies the **maximum time** the Kafka group coordinator will wait for a consumer to send a heartbeat before deciding that the consumer has failed.

* **Default:** 10 seconds
* If the consumer does not send a heartbeat within this period, the coordinator assumes the consumer is dead and **triggers a rebalance**.
* During a rebalance, the coordinator reassigns the partitions owned by that consumer to the remaining active consumers in the group.

---

#### **2. Related Property — `heartbeat.interval.ms`**

This property defines **how often** the consumer sends heartbeats to the group coordinator.

* `heartbeat.interval.ms` must always be **less than** `session.timeout.ms`.
* Common practice is to set:

  ```
  heartbeat.interval.ms = session.timeout.ms / 3
  ```

**Example:**
If `session.timeout.ms = 9000` (9 seconds),
then `heartbeat.interval.ms` should be around `3000` (3 seconds).

---

#### **3. Balancing Failure Detection vs. Stability**

Tuning `session.timeout.ms` involves a tradeoff:

* **Lower value** (e.g., 3–5 seconds):

  * Detects consumer failures faster
  * But may cause **frequent rebalances** if network delays or short pauses occur

* **Higher value** (e.g., 20–30 seconds):

  * Fewer accidental rebalances
  * But slower to detect actual consumer failures

---

#### **4. Summary**

| Property                | Purpose                                                                  | Default   | Notes                                                       |
| ----------------------- | ------------------------------------------------------------------------ | --------- | ----------------------------------------------------------- |
| `session.timeout.ms`    | Max time consumer can go without heartbeats before being considered dead | 10,000 ms | Shorter = faster failure detection, but risk of instability |
| `heartbeat.interval.ms` | How often heartbeats are sent                                            | 3,000 ms  | Must be less than session timeout, usually ⅓ of it          |

---

#### **In short**

* `session.timeout.ms` = how long a consumer can be silent before being declared dead.
* `heartbeat.interval.ms` = how frequently the consumer checks in.
* Keep heartbeat interval lower than session timeout (about one-third).
* Adjust both together based on your system’s network stability and desired failure recovery speed.

