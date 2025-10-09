## Kafka Interceptors

Kafka **interceptors** allow you to modify or extend the behavior of Kafka producers (or consumers) **without changing the main application code**.
They act as **middleware hooks** that intercept records before they’re sent to Kafka and after acknowledgments are received.

### Why use interceptors

There are cases where you want to:

* Add the same custom logic across multiple producer applications.
* Track or monitor messages.
* Modify or sanitize data before it’s sent.
* Collect metrics or logs for auditing and debugging.
* You might not have access to the original application source code.

---

### ProducerInterceptor interface

Kafka provides the `ProducerInterceptor` interface with two main methods:

#### 1. `ProducerRecord<K, V> onSend(ProducerRecord<K, V> record)`

* This method is called **before** a record is serialized and sent to Kafka.
* You can:

  * Inspect or log the message.
  * Add headers or metadata (for example, tracking IDs or timestamps).
  * Mask or redact sensitive data.
  * Even modify the record itself.
* The method must return a **valid `ProducerRecord`**, because that record is what will actually be serialized and sent.

**Example use:**

```java
@Override
public ProducerRecord<String, String> onSend(ProducerRecord<String, String> record) {
    // Add a custom header before sending
    record.headers().add("source-app", "payment-service".getBytes());
    return record;
}
```

---

#### 2. `void onAcknowledgement(RecordMetadata metadata, Exception exception)`

* This method runs **after Kafka acknowledges** a message (i.e., once the broker confirms receipt).
* You cannot change the acknowledgment itself.
* Typical uses:

  * Record success/failure metrics.
  * Log message delivery status.
  * Send tracing or monitoring data.

**Example use:**

```java
@Override
public void onAcknowledgement(RecordMetadata metadata, Exception exception) {
    if (exception == null) {
        System.out.println("Message sent successfully to " + metadata.topic());
    } else {
        System.err.println("Send failed: " + exception.getMessage());
    }
}
```

---

### Common use cases

* **Monitoring and tracing** — Collect metrics about message latency or failures.
* **Data enrichment** — Add standard headers (for lineage or auditing).
* **Redaction** — Remove or mask sensitive data before sending.
* **Consistent policies** — Apply organization-wide behaviors without altering each app’s code.

---

In short, producer interceptors give you a flexible way to **observe, modify, and log message flow** in Kafka producers before and after communication with the Kafka cluster — all without touching the core application logic.

Check pg 129 and 130 of Kafka Def Guide for the code examples