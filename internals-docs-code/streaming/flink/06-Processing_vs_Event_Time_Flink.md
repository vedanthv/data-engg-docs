# Processing vs Event Time in Flink

---

# **1. Processing Time (System Time)**

Processing time means:

**“Use the time of the machine where the event is being processed.”**

So the timestamp comes from **the system clock** of the Task Manager.

### Characteristics

* Fastest
* No need for watermarks
* No waiting for late events
* Sensitive to system load, network delays, backpressure

### Example

If an event arrives at 12:00:10 PM system time, that’s its processing time — even if that event was actually produced at 11:59:55 AM.

### Use cases

* Basic dashboards
* Monitoring where slight inaccuracies are okay
* High-throughput counters
* No out-of-order handling needed

---

# **2. Event Time**

Event time means:

**“Use the timestamp inside the event — when it actually occurred in the real world.”**

Flink extracts the timestamp from the event using:

```java
assignTimestampsAndWatermarks(...)
```

### Key characteristics

* Handles late and out-of-order events
* Uses watermarks to decide when to close windows
* Most accurate
* Slightly slower (waiting for late events)

### Example

Suppose a sensor generated data at 11:59:55 AM but reached Flink at 12:00:10 PM.

* **Event time = 11:59:55**
* **Processing time = 12:00:10**

Event time gives “real-world correctness” instead of “arrival-time correctness.”

---

# **3. Why event time is critical**

Real streaming data is **almost always out-of-order**.

Events can arrive late due to:

* Network delays
* Clock skew
* Mobile devices going offline
* Batch uploads
* Retries in Kafka

If you use **processing time**, windows close too early.

If you use **event time**, windows only close when watermarks say “we have seen almost all events.”

---

# **4. Watermarks (core to event time)**

Event time requires **watermarks** — these tell Flink:

**“No more events older than this timestamp should arrive.”**

Watermarks = progress indicators of event time.

Example:

If watermark = 12:00:00, Flink believes:

* All events with timestamps ≤ 12:00:00 have arrived
* Safe to close windows up to 12:00:00

Late events after this watermark go to **late arrival handling** (drop or side outputs).

---

# **5. Event Time vs Processing Time: Side-by-Side Comparison**

| Feature               | Processing Time             | Event Time                      |
| --------------------- | --------------------------- | ------------------------------- |
| Timestamp source      | System clock                | Inside event                    |
| Handles out-of-order? | No                          | Yes                             |
| Accuracy              | Low                         | High                            |
| Throughput            | High                        | Medium                          |
| Requires watermarks?  | No                          | Yes                             |
| Windows               | Close based on arrival time | Close based on event time       |
| Late event support    | Not possible                | Supported                       |
| Use cases             | Monitoring, quick stats     | Analytics, correctness-critical |

---

# **6. Example with a window**

Let’s say you have a **1-minute window**.

### If using processing time:

Window 12:00:00–12:01:00 closes at **12:01:00 system time**.
If an event with timestamp 11:59:50 arrives at 12:00:50, it goes into the running window.
If it arrives at 12:01:05, it is **too late**.

### If using event time:

Window 12:00:00–12:01:00 closes when watermark passes 12:01:00.

If watermark = event_time − 5 seconds:

* Out-of-order events up to 5 seconds late are accepted
* Windows close correctly based on event timestamps

---

# **7. When to use what?**

### Use **event time** when:

* Data comes late, out of order (common in Kafka, IoT, logs)
* Need accurate results (analytics, billing, fraud detection)
* You use windows, joins, aggregations

### Use **processing time** when:

* You need ultra-low latency
* Out-of-order is not a concern
* Simple transformations, monitoring, counters

---

# **8. One-line summary**

* **Processing time** = use machine clock → fast but inaccurate
* **Event time** = use timestamp inside event → accurate, requires watermarks

---