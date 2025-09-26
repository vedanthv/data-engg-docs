# Configuring Producers in Kafka

1. ```acks```

Controls how many partition replicas must receive the record before Kafka producer can consider write successful.

By default Kafka considers it successful when the leader receives the message but this may be slow and impact durability of written messages.

**ack = 0**

The producer will not wait for the message acknowledgement to be received.

**acks = 1**

The producer will receive a success response from broker the moment leader receives the message, if the leader doesnt receive it producer retries.

The message can get lost if leader crashes and latest messages are still not replicated to new leader.

**acks = all**

Only once all in sync replicas receive message, the write is successful. This has very high latency.

## Messgae Delivery Time Parameters

'How long will it take for a call to send() to be successful or failed?'

Two main time intervals:

---

### 1. Time until an async call to `send()` returns

* `producer.send(record, callback)` is **asynchronous**.
* Normally, `send()` should return **very quickly** because it just places the record into a buffer (producer’s local memory).
* However, there are situations where `send()` can actually **block** the calling thread before returning:

  * If the producer’s **buffer is full** (e.g., you’re producing faster than Kafka can send), `send()` will block until there’s room, or until `max.block.ms` is exceeded.
  * This is the **“time until send() returns”**.
  * During this time, your application thread is stuck waiting — it can’t continue until the record is accepted into the buffer.

**So:** this measures how long the application thread waits just to hand off the record to the producer.

---

### 2. Time from send() return until callback triggered

* Once `send()` has returned, the record is now queued inside the producer’s buffer.
* From here, the producer batches it with other records (to the same partition) and eventually sends the batch to the Kafka broker.
* The callback you passed to `send()` will be triggered **later**, once Kafka responds.

This second interval covers:

1. Time the record spends in the local buffer waiting for batching.
2. Network transmission time to Kafka.
3. Broker processing time (writing to log, replicating if needed).
4. Broker response coming back.

At the end:

* If everything succeeds → callback gets a **success** with `RecordMetadata`.
* If retries fail or an unrecoverable error happens → callback gets a **failure exception**.

**So:** this interval = "from the moment `send()` returns successfully → until Kafka responds (success or failure)."

---

### Putting it together

* **Interval 1:** “Time until send() returns” = how long your application thread is blocked just waiting to enqueue the record.
* **Interval 2:** “Time from send() return to callback” = how long Kafka + the producer pipeline takes to actually deliver the record and get an acknowledgment.

---

1. First wait: “Can I even hand this message to the producer, or is the buffer full?”
2. Second wait: “Now that it’s handed off, how long until Kafka says the message is written (or failed)?”

---

<img width="725" height="338" alt="image" src="https://github.com/user-attachments/assets/91e80a53-00fa-4140-b488-590d8b15f20b" />

**max.block.ms**

How long a producer may block send() thread while waiting for metadata via ```partitionsFor()```

**delivery.timeout.ms**

Amount of time from a point where the record is set for sending until either the broker or client gives up / times out.

It should be greater than sum of ```linger.ms``` and ```request.timeout.ms```

This is about how **Kafka producer timeouts** interact with **retries** and the **callback** you provide to `send()`. Let’s break it into parts.

---

### 1. What is `delivery.timeout.ms`?

* It is the **maximum time the producer will try to deliver a record**, from the moment you call `send()` until a final outcome (success or failure).
* Default = **120,000 ms (2 minutes)**.
* It covers **both retries and waiting in the buffer**.
* If this time limit is reached, the record is considered failed, and the callback is triggered with an exception.

---

### 2. Case 1: Timeout happens **during retries**

* Imagine the producer sends a batch → broker responds with an error (like `NOT_ENOUGH_REPLICAS`).
* The producer will retry sending (depending on `retries` and `retry.backoff.ms`).
* But if all those retries push the elapsed time **past `delivery.timeout.ms`**, the producer gives up.
* **What happens then?**

  * The callback will get the **last error exception that the broker returned before retrying**.
  * Example: If the broker said “Not enough replicas” before retrying, that same exception will be delivered to you.

---

### 3. Case 2: Timeout happens **while waiting to send**

* Records don’t always get sent immediately:

  * They may wait in the buffer (producer batches messages).
  * Or they may wait because the broker is slow or the partition leader is unavailable.
* If the record is still sitting in the batch (never sent) when `delivery.timeout.ms` is exceeded:

  * The callback will get a **TimeoutException**.
  * This means: “We didn’t even manage to send this record in time.”

---

### 4. Why the difference?

* Kafka wants to give you **useful error context**:

  * If retries happened → the callback returns the **broker error that caused retries**.
  * If no send happened → the callback just returns a **generic timeout**.

That way, you know whether the problem was:

* “Broker responded with errors but we couldn’t fix it in time” (Case 1).
* “We never even got a chance to send” (Case 2).

---

✅ **In short:**

* `delivery.timeout.ms` = max time a record is allowed to live (send + retry + wait).
* If timeout hits after retries → callback gets the **last broker error**.
* If timeout hits while waiting to be sent → callback gets a **TimeoutException**.

---
## ```delivery.timeout.ms``` vs ```max.block.ms```
---

### 1. `max.block.ms`

* Applies **before** the record is handed over to the producer’s buffer.
* Specifically:

  * If the buffer is **full** (`buffer.memory` exhausted) or metadata (like partition leader info) is **not available**, the `send()` call can block.
  * It will block at most for `max.block.ms` (default = 60,000 ms).
  * If that time passes → `send()` throws a `TimeoutException` immediately, **before the record is accepted**.
* So this timeout is about: *“Can I enqueue this record into the producer at all?”*

---

### 2. `delivery.timeout.ms`

* Applies **after** the record has been accepted into the producer buffer.
* It measures the total time a record is allowed to live (waiting in buffer + batching + retries + network sends) before either success or failure.
* If exceeded → the callback is triggered with either:

  * The **last broker error** (if retries happened), or
  * A **TimeoutException** (if the record never got sent).

---

### 3. Do they overlap?

No — they are **separate**:

* If the record cannot even enter the buffer (blocked by memory/metadata) → `max.block.ms` applies. In this case, `delivery.timeout.ms` never starts, because the record was never enqueued.
* Once the record is successfully handed to the producer → `delivery.timeout.ms` applies until final success/failure.

---

### 4. Analogy

* **`max.block.ms`** = waiting in line to enter the store. If you wait too long, you give up before shopping.
* **`delivery.timeout.ms`** = once you’re inside, you have a maximum time to shop and check out. If you exceed it, your shopping trip fails.

---

✅ **Answer to your question:**
No, `delivery.timeout.ms` **does not include** `max.block.ms`.
They apply at **different stages**:

* `max.block.ms` = before record enters producer buffer.
* `delivery.timeout.ms` = after record is accepted into the buffer, until acknowledgment.

---

### ```request.timeout.ms```

How long does each producer wait for reply from server before giving up.

Does not include retries, time before sending and so on.

If timeout reached without reply, then producer will complete with callback exception.

### ```retries``` and ```retries.backoff.ms```

By default, producer waits 100 ms betweenr retries.

Instead of setting this parameter, we need to check how long it takes for Kafka cluster to recover from crash (how long until all producers get leaders) and set this time to
something greater than it.

