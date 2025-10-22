## Default Topic Properties

1. ```num.partitions```

<img width="852" height="316" alt="image" src="https://github.com/user-attachments/assets/b27c69c8-05db-4ecc-8974-2b6d36390d4f" />

<img width="885" height="462" alt="image" src="https://github.com/user-attachments/assets/79158231-557b-4228-a919-6d5ee92801bf" />

### How to choose number of partitions?

- What is throughput to expect from the topic? 100KbS or 1Gbps?
- What is the maximum throughput you expect to achieve when consuming from a single partition?

If consumer writes slowly to database and the DB only handles 50MbPs for each thread writitng to it, then we are limited to 50MbPS throughput.
  
If you are sending messages to partitions based on keys, adding partitions later can be very challenging, so calculate throughput based on your expected future usage, not the   current usage.

<img width="853" height="477" alt="image" src="https://github.com/user-attachments/assets/8c941b18-3cbd-498b-9984-4d25a935054b" />

2. ```default.replication.factor```

<img width="856" height="698" alt="image" src="https://github.com/user-attachments/assets/fe428536-fdca-472f-8349-b58b969124e8" />

We would have three replicas of every partition since if there is a network switch update, disk failure or some other problem, we can be assured that additional replica will be available.

3. ```log.retention.ms```

The most common configuration for how long Kafka will retain messages is by time.

- By default using ```log.retention.hours``` and is set to 168 hours.
- There are two other, ```log.retention.minutes``` and ```log.retention.seconds```. The recommended is to use ms as its the smallest unit, if we specify all three ms takes precedence.
- Retention by time is performed by examining the last modified time on each log segment on the disk. Under normal circumstances its the time the log segment was closed and is last message in the file.

4. ```log.retention.bytes```

- Another way to expire messages and this is set at topic level. If we have a topic with 8 partitions and log.retention.bytes set to 1GB, then the amount of data retained in the topic would be 8GB at most.
- If no of partitions increase, then retention will also increase if ```log.retention.bytes``` is used.

<img width="783" height="334" alt="image" src="https://github.com/user-attachments/assets/39997417-ac69-454f-825c-156ffa30ced1" />

5. ```log.segment.bytes```

- The previous config log.retention.bytes acts on log segments and not individual messages.
- As messages are produced to the Kafka broker they are appended to the current log segment and once its reached ```log.segment.bytes``` which defaults to 1GB, its closed and a new one is opened.
- Once a log segment is closed its considered for expiration, if we have lot of small segments, then files are closed and allocated more often and disk efficiency decreases.

We need to size the log segments carefully, take example, if topic receives 100 MB data and log.segment.bytes is 1GB, it will take 10 days for the segment to close and none of the messages in the segment can be expired until the log segment is closed.

If log.retention.ms is set to 1 week, there will actually be upto 17 days of messages retained until closed log segment expires.

This is because we need to wait for 10 days of all messages, the log segment must be retained for 7 days before it expires as per time based policy. Until the last message in the segment expires the segment cant be deleted.

<img width="970" height="282" alt="image" src="https://github.com/user-attachments/assets/5180e2b7-e9a2-4f8d-b725-1c51c9e954e1" />

6. ```log.roll.ms```

Specifies amount of time after which log segment must be closed. ```log.segment.bytes``` and ```log.roll.ms``` are not mutually exclusive.

Kafka will close log segment when time limit is reached or size is crossed first.

There is no default for ```log.roll.ms```

**Disk Performance When Using Time Based Segments**

<img width="969" height="182" alt="image" src="https://github.com/user-attachments/assets/2baf6197-05be-4b25-94df-13872d986d67" />

7. ```min.insync.replicas```

<img width="1052" height="661" alt="image" src="https://github.com/user-attachments/assets/07dbdd45-8d21-46e2-8e8b-ff08fe4b2507" />

8. ```messages.max.bytes```

- Default size which Kafka broker produces is 1mb.
- A producer that produces more than this will receive error from broker.

<img width="1104" height="672" alt="image" src="https://github.com/user-attachments/assets/29d344b2-067f-4d5c-866e-3ff7abc69121" />

### ```log.segment.bytes``` vs ```log.retention.bytes```
---

## 🗂 log.segment.bytes

* Think of this as the **page size** in a notebook.
* It controls the **maximum size of a single log segment file** on disk.
* Once the segment reaches this size, the broker rolls over and creates a **new segment file**.
* Default (Kafka): `1 GB`.

👉 Example:
If `log.segment.bytes = 100 MB` and your topic partition receives 500 MB of messages, you’ll end up with **5 segment files**.

---

## 🗑 log.retention.bytes

* This is about **retention policy**: how much data the broker should keep per topic-partition.
* It defines the **maximum total size** of log data to retain before old segments get deleted.
* Default: `-1` (unlimited, rely on time-based retention).

👉 Example:
If `log.retention.bytes = 1 GB` and each segment is `100 MB`, the broker will keep \~10 segments (1 GB total). When a new segment is rolled, the oldest ones get deleted.

---

## 🔑 Key Difference

* **`log.segment.bytes` = size of each "chunk" (file)**.
* **`log.retention.bytes` = total allowed size before deleting old chunks**.

---

## ⚖️ Together in action

Say you configure:

* `log.segment.bytes = 100 MB`
* `log.retention.bytes = 1 GB`

Then:

1. Messages are written to a segment until it hits 100 MB.
2. Broker rolls over to a new file.
3. Once total partition size exceeds 1 GB, broker starts deleting the **oldest segment files** to free space.

---

👉 So:

* **segment = slice of cake**
* **retention.bytes = whole cake size allowed**

## Deletion at Message Level?

Exactly 👍 — **retention in Kafka/Redpanda is never at the *message* level, it’s always at the *segment* level**.

---

### 🔍 Why?

* Messages are appended **sequentially** to log segment files (immutable, append-only).
* A segment is only eligible for deletion when **all messages inside it** are older/larger than the configured retention policies.
* This avoids the overhead of deleting messages one by one.

---

### ✅ Example:

* `log.segment.bytes = 100 MB`
* `log.retention.hours = 24`

If your segment has messages from **10:00 → 10:15**:

* At **10:16** some messages are already > 1 min old.
* But the **whole segment** stays, since it still contains "younger" messages.
* Only when the **last message** inside the segment is older than 24h does the broker delete the whole file.

---

### 🚫 What does NOT happen:

* Kafka/Redpanda doesn’t scan inside a segment to throw away just one old message.
* That would break the append-only design and make reads/writes much slower.

---

## 🔁 Retention vs Compaction

### 1. **Retention (time/size based)**

* Works at **segment level**.
* Old **files** (segments) are deleted when they exceed `log.retention.*` policies.
* Entire segments are removed, not individual messages.
* Good for **event streaming** where you don’t care about keeping history forever.

📌 Example:
Keep data for **7 days**, then drop old files.

---

### 2. **Log Compaction (key based)**

* Works at the **message level** (but only for topics that have compaction enabled).
* For each **key**, Kafka/Redpanda keeps only the **latest value**.
* Old values for the same key are removed in the background.
* This ensures that at any point, the log contains the "latest snapshot" per key.

📌 Example:
Say topic is compacted and we write:

```
key=user1, value=Vedanth
key=user1, value=Baliga
key=user2, value=StoneX
```

👉 After compaction finishes, only:

```
user1 → Baliga
user2 → StoneX
```

remains.

---

### ⚖️ When to use what?

* **Retention** → for **event streams** (transactions, logs, telemetry, clickstream).
* **Compaction** → for **stateful data** (user profiles, configs, account balances).

---

💡 Sometimes people **combine** both:

* Keep data for 7 days (`log.retention.hours=168`),
* But also enable compaction (`cleanup.policy=compact,delete`) → so you keep latest snapshots forever, while old junk is cleared.

---
