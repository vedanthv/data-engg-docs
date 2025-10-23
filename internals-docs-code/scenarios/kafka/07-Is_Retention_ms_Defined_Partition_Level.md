# Is retention defined at topic level or partition level?

---

## **Short Answer**

No, **`retention.ms` is *not* defined at the partition level.**
It is defined at the **topic level**, and applies **uniformly to all partitions** of that topic.

---

## **Detailed Explanation**

### **1. Configuration levels in Kafka**

Kafka configuration settings can exist at different scopes:

| Scope               | Examples                                          | Description                                                                 |
| ------------------- | ------------------------------------------------- | --------------------------------------------------------------------------- |
| **Broker-level**    | `log.retention.hours`, `log.segment.bytes`        | Default values that apply to all topics on that broker (unless overridden). |
| **Topic-level**     | `retention.ms`, `cleanup.policy`, `segment.bytes` | Specific to one topic; overrides the broker defaults.                       |
| **Partition-level** | —                                                 | Kafka does *not* allow per-partition settings for retention or compaction.  |

So `retention.ms` sits at the **topic level**, not per partition.

---

### **2. How it applies to partitions**

Every topic in Kafka is divided into partitions.
Each partition has its own **log directory** on disk.
The broker applies the topic’s retention rules to each partition’s log independently.

So while there is *no separate configuration per partition*, the **effect of `retention.ms`** is enforced **per partition**.

That means:

* Each partition’s log cleaner or retention manager will check the **modification timestamps of its segments**,
* And delete (or compact) them according to the topic’s `retention.ms` rule.

But the rule itself comes **from the topic configuration**, not the partition.

---

### **3. Example**

Suppose:

```bash
# Topic-level config
retention.ms = 604800000   # 7 days
```

and your topic has 3 partitions: `p0`, `p1`, `p2`.

Then:

* Each partition (`p0`, `p1`, `p2`) will keep messages for up to **7 days**,
* After that, old segments will be deleted (for delete-based cleanup) or eligible for compaction (if `cleanup.policy=compact`).

If you wanted one partition to keep messages for 30 days and another for 7, **Kafka doesn’t support that** —
you’d have to create **two separate topics**.

---

### **4. Where it’s stored**

You can verify topic-level retention settings using:

```bash
kafka-configs.sh --bootstrap-server <broker> --describe --topic <topic-name>
```

You’ll see something like:

```
Topic: my-topic  Configs: retention.ms=604800000, cleanup.policy=delete
```

There’s no command or metadata that shows a per-partition `retention.ms` value, because it simply doesn’t exist.

---

### **5. Related parameters**

| Parameter             | Level  | Description                                                       |
| --------------------- | ------ | ----------------------------------------------------------------- |
| `retention.ms`        | Topic  | How long messages are retained before deletion.                   |
| `retention.bytes`     | Topic  | Max log size before old segments are removed.                     |
| `log.retention.ms`    | Broker | Default `retention.ms` for topics without explicit configuration. |
| `log.retention.bytes` | Broker | Default max size for topics without explicit configuration.       |

So — **broker-level values are defaults**, **topic-level values override them**,
and **partitions follow the topic’s settings**.

---

### **6. Analogy**

Imagine a school (Kafka broker) with classes (topics) and students (partitions):

* The **school** sets a default rule:
  “Homework will be kept for 7 days.”

* A **teacher** (topic) can override this rule:
  “In *my class*, homework is kept for 10 days.”

* Each **student’s notebook** (partition) follows that rule independently,
  but they can’t have different rules within the same class.
  Every student in that class follows the same “keep homework for 10 days” policy.

---

**In short:**

* ❌ You cannot define `retention.ms` at partition level.
* ✅ It’s a topic-level property, applied independently to each partition’s data.

---