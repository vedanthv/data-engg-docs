## Kafka Configuring Consumers - Part II

### 1. ```max.poll.interval.ms```

This explanation describes the **`max.poll.interval.ms`** property in a Kafka consumer — an important setting that determines **how long a consumer can go without calling `poll()`** before Kafka considers it dead.


---

#### **1. Purpose**

`max.poll.interval.ms` defines the **maximum delay allowed between two consecutive `poll()` calls** made by a consumer.

* If the consumer does **not** call `poll()` within this time window, it is considered **stuck or dead**.
* Kafka will then **remove it from the consumer group** and **trigger a rebalance** to redistribute its partitions.

**Default:** 5 minutes (300,000 ms)

---

#### **2. Why It’s Needed**

Kafka consumers have two main “liveness” mechanisms:

* **Heartbeats (`session.timeout.ms` + `heartbeat.interval.ms`)** — ensure the consumer process is alive.
* **Poll interval (`max.poll.interval.ms`)** — ensures the consumer is **actively processing** records, not just alive but doing work.

Without `max.poll.interval.ms`, it’s possible for:

* The consumer’s **main thread** to be **stuck or deadlocked**,
* While the **background heartbeat thread** keeps sending heartbeats,
* Making Kafka think the consumer is still healthy even though it’s no longer processing messages.

---

#### **3. How It Works**

* The consumer’s main thread must call `poll()` **periodically** to fetch new records.
* If the consumer does not call `poll()` again within the `max.poll.interval.ms` time limit:

  * The consumer is **considered unresponsive**.
  * The broker **removes it from the group**.
  * A **rebalance** occurs so other consumers can take over its partitions.
  * The background heartbeat thread stops sending heartbeats after signaling a **“leave group”** request.

---

#### **4. Interaction with Other Properties**

* **`max.poll.records`**:
  Limits how many records `poll()` returns in one call.
  Smaller values mean the consumer calls `poll()` more frequently.
  Larger values may increase the processing time before the next `poll()`.
  Together with `max.poll.interval.ms`, it helps balance throughput and stability.

* **`session.timeout.ms` vs. `max.poll.interval.ms`:**

  * `session.timeout.ms` detects dead consumers (no heartbeats).
  * `max.poll.interval.ms` detects **stuck consumers** (not polling).

---

#### **5. Tuning Guidance**

| Scenario                                               | Recommended Setting                                                   |
| ------------------------------------------------------ | --------------------------------------------------------------------- |
| Fast message processing                                | Keep default (5 minutes) or lower if frequent polls are guaranteed    |
| Heavy or slow processing per record                    | Increase to allow enough time for processing before next `poll()`     |
| To avoid false rebalances due to long processing times | Adjust both `max.poll.records` and `max.poll.interval.ms` accordingly |

---

#### **6. Example**

If a consumer takes around **2 minutes** to process one batch of messages, set:

```properties
max.poll.interval.ms = 300000   # (5 minutes) – still safe
max.poll.records = 100          # process fewer messages per poll
```

This ensures the consumer won’t be removed unless it truly stops processing for more than 5 minutes.

---

#### **In short**

* `max.poll.interval.ms` controls **how long a consumer can go without polling**.
* It prevents **“zombie” consumers** that appear alive but aren’t processing data.
* Default is **5 minutes**.
* Tune it alongside `max.poll.records` based on how long your consumer takes to process each batch.

### 2. ```default.api.timeout.ms```

This is the timeout that will apply to almost all API calls for timeout and will include a retry when needed.

Exception is poll method that requires a default explicit timeout.

### 3.```request.timout.ms```

Max amount of time that consumer will wait for broker to respond.

If the broker doesnt respond by this time, consumer may think broker is busy and will try reconnecting after some time. We shouldnt keep it too low because if broker is already overloaded then it makes no sense to add more overhead by sending api calls ever 1/2 seconds.

### 4. ```auto.offset.reset```

This property controls the behavious when a consumer starts reading from a partition without a committed offset, or if it has an invalid id.

The default is ```latest```, basically indicating that lacking a valid offset, consumer will start reading from the latest records, alternate is ```earliest```.

If we set it to ```none``` then consumer will fail when trying to restart from invalid offset.

### 5. ```enable.auto.commit```

By default its ```true``` but if we want to control when offsets are committed to minimize duplicates and avoid duplicating data.

