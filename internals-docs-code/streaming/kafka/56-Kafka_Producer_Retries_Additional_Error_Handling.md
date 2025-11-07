# Kafka : Producer Retries and Additional Error Handling

---

## 1. **Two categories of error handling**

Kafka producer reliability is built on the idea that **some errors can be retried safely**, and others cannot.
When a producer sends a message to a broker, the broker responds with either:

* A **success acknowledgment**, or
* An **error code**.

The producer API classifies these into two main categories:

| Error Type               | Description                                         | What Happens                                     |
| ------------------------ | --------------------------------------------------- | ------------------------------------------------ |
| **Retriable errors**     | Temporary problems that may succeed after retrying. | Producer automatically retries.                  |
| **Non-retriable errors** | Permanent configuration or authorization problems.  | Producer raises an exception to the client code. |

---

## 2. **Examples of retriable errors**

These typically occur due to transient cluster events — temporary network failures, leader elections, or broker restarts.
They can be retried safely without losing correctness.

| Error Code             | Cause                                                                  | Typical Resolution                         |
| ---------------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| `LEADER_NOT_AVAILABLE` | The partition’s leader broker just failed; a new one is being elected. | Retry after the new leader is established. |
| `NOT_ENOUGH_REPLICAS`  | Some replicas are temporarily out of sync.                             | Retry once ISR stabilizes.                 |
| `NETWORK_EXCEPTION`    | Transient network glitch between producer and broker.                  | Retry automatically.                       |
| `REQUEST_TIMED_OUT`    | Broker did not respond in time.                                        | Retry after backoff.                       |

When these occur, the producer client can (and should) **retry** sending the same message — either automatically (handled internally by KafkaProducer) or manually if custom logic is needed.

---

## 3. **Examples of non-retriable errors**

These represent **permanent problems** that will not resolve by simply retrying.

| Error Code                   | Description                                            | Why retrying won’t help                   |
| ---------------------------- | ------------------------------------------------------ | ----------------------------------------- |
| `INVALID_CONFIG`             | Producer or topic configuration mismatch.              | Misconfiguration needs manual correction. |
| `TOPIC_AUTHORIZATION_FAILED` | The producer is not authorized to write to the topic.  | Requires security policy change.          |
| `UNKNOWN_TOPIC_OR_PARTITION` | The topic doesn’t exist and auto-creation is disabled. | Topic must be created.                    |
| `MESSAGE_TOO_LARGE`          | The message size exceeds broker limits.                | Message must be adjusted.                 |

For these, Kafka immediately throws an exception to the application; the client must handle or log it — retries are futile.

---

## 4. **How automatic retries work**

Kafka’s producer client library automatically retries **retriable errors** without application intervention.

You control retry behavior via two key settings:

| Config                | Default                            | Description                                                                                    |
| --------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| `retries`             | `2147483647` (`Integer.MAX_VALUE`) | Maximum number of retry attempts. Effectively infinite by default.                             |
| `delivery.timeout.ms` | `120000` (2 minutes)               | Maximum total time (across all retries) for the producer to attempt delivery before giving up. |

This means:

* The producer retries **indefinitely**, but only **within the `delivery.timeout.ms` window**.
* If a message cannot be acknowledged by the broker within that window, the producer drops it and raises an exception.

### Important note:

Retries happen **asynchronously**, in the background I/O thread — the producer batches and resends records efficiently, without blocking your application threads.

---

## 5. **How retries can cause duplicates**

While retries solve temporary errors, they also introduce a new risk: **duplicate writes**.

Consider this sequence:

1. Producer sends a message to broker.
2. Broker writes the message successfully.
3. Broker sends an acknowledgment.
4. The acknowledgment is lost due to a network error.
5. Producer assumes the send failed and retries.
6. Broker receives the retry and writes the same message again.

Now the topic log contains **two copies** of the same message — same payload, different offsets.

### Without safeguards:

This is “**at-least-once delivery**” — every message is stored at least once, possibly more than once.

---

## 6. **How `enable.idempotence=true` fixes this**

Enabling idempotence transforms producer behavior from **at-least-once** to **exactly-once (per session)** by adding **deduplication metadata** to every record batch.

When `enable.idempotence=true`:

* Each producer gets a unique **Producer ID (PID)** from the Kafka cluster controller.
* Each message batch sent includes:

  * The **PID**
  * A **monotonic sequence number**
* The broker tracks the last sequence number it has processed for each PID.

When the producer retries a batch:

* If the broker already has a batch with the same PID and sequence number, it silently discards the duplicate.
* The message is written **exactly once**, even if sent multiple times.

This mechanism ensures:

* Retries never create duplicates.
* Ordering is preserved per partition.
* Exactly-once delivery within the producer session.

---

## 7. **Retry logic and timing behavior**

The Kafka producer’s retry process is governed by several key configurations:

| Config                                  | Function                                                                            |
| --------------------------------------- | ----------------------------------------------------------------------------------- |
| `retries`                               | Number of retry attempts (default effectively infinite).                            |
| `retry.backoff.ms`                      | Wait time before retrying a failed send (default 100ms).                            |
| `delivery.timeout.ms`                   | Total time allowed from initial send to final acknowledgment before giving up.      |
| `max.in.flight.requests.per.connection` | Maximum concurrent sends; setting this to 1 ensures strict ordering during retries. |
| `enable.idempotence`                    | Enables deduplication and exactly-once guarantees for retries.                      |

The combination of these settings controls how long the producer will persist in resending a record and whether retries are safe from duplication.

---

## 8. **Developer-handled errors**

There are still errors that **the developer must handle explicitly**. These typically occur:

* When the producer **gives up** after exceeding `delivery.timeout.ms`.
* When **non-retriable errors** are raised.
* When the application needs custom logic, such as logging, DLQ (dead-letter queue), or alerting.

The producer API surfaces these through:

* **Futures** returned by `producer.send(record)`, or
* **Callback functions**, such as:

```java
producer.send(record, (metadata, exception) -> {
    if (exception != null) {
        // handle error: log, retry, send to DLQ
    } else {
        // message successfully acknowledged
    }
});
```

This is where your application decides whether to retry, log, or route the failed record elsewhere.

---

## 9. **Summary**

| Concept                                     | Description                                                                              |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Retriable errors**                        | Temporary (e.g., `LEADER_NOT_AVAILABLE`, `NETWORK_EXCEPTION`); can be retried safely.    |
| **Non-retriable errors**                    | Permanent (e.g., `INVALID_CONFIG`, `AUTHORIZATION_FAILED`); require manual intervention. |
| **Automatic retries**                       | Producer retries retriable errors transparently within `delivery.timeout.ms`.            |
| **Duplicates risk**                         | Without idempotence, retries may insert duplicate messages.                              |
| **Idempotence (`enable.idempotence=true`)** | Adds PID and sequence metadata for exactly-once delivery within a producer session.      |
| **Developer responsibility**                | Handle non-retriable errors, log/report failures, or implement DLQ.                      |

---

### In essence:

Kafka’s producer automatically retries transient errors to ensure **at-least-once delivery**, but to achieve **exactly-once delivery** (within a session) and avoid duplicates, you must enable `enable.idempotence=true`.

Beyond that, you must still handle **irrecoverable errors** and **timeout conditions** in your application logic — the producer can’t fix those automatically.
