# Constructing Kafka Producer

There are three primary properties to be specified.

**bootstrap.servers**

**key.serializer**

Let’s break this down step by step:

1. **Kafka message format**

   * Kafka brokers **store and transmit messages as byte arrays** for both **keys** and **values**.
   * This is because Kafka itself doesn’t know or care what the data means; it just moves raw bytes.

2. **Producer flexibility**

   * When using the Kafka Producer API in Java, you don’t have to manually create byte arrays.
   * Instead, the producer API lets you work with normal Java objects as **keys** and **values** (like `String`, `Integer`, or custom objects).
   * This makes your producer code more readable and type-safe.

3. **Serialization requirement**

   * Since Kafka only understands byte arrays, there must be a **conversion step** from your Java object (e.g., `String` or `Integer`) into a byte array before sending.
   * That’s what the **Serializer** interface is for: it defines how to transform an object into a byte array.

4. **`key.serializer` configuration**

   * In the producer configuration, you set the `key.serializer` property to the **class name** of a serializer.
   * This tells the Kafka producer which serializer to use when converting your key objects into bytes.
   * Example serializers provided by Kafka:

     * `org.apache.kafka.common.serialization.StringSerializer`
     * `org.apache.kafka.common.serialization.IntegerSerializer`
     * `org.apache.kafka.common.serialization.ByteArraySerializer`

   If you use a common type like `String` or `Integer`, you don’t need to write your own serializer — you just use the one provided.

5. **Required setting**

   * Even if you don’t plan to use keys in your messages (only values), you **must** still set `key.serializer`.
   * In that case, you can configure the producer to use the **`Void` type** for keys, along with the provided `org.apache.kafka.common.serialization.VoidSerializer`. This is a special serializer that essentially says, “I’m not sending a key.”

---

**In short:**

* Kafka always works with byte arrays internally.
* `key.serializer` defines which class will convert your key objects into byte arrays.
* Kafka provides built-in serializers for common Java types (`String`, `Integer`, etc.), so you usually don’t need to implement your own.
* You must configure `key.serializer` even if your producer doesn’t use keys — in that case, you use `VoidSerializer`.


Great, let’s go through **`value.serializer`** in parallel with **`key.serializer`** so you see the complete picture.

---

### 1. Kafka expects **byte arrays** for both **keys** and **values**

* Every Kafka message has two parts:

  * **Key** → used mainly for partitioning (decides which partition the record goes to).
  * **Value** → the actual payload of the message.
* Kafka itself only works with raw byte arrays, so both key and value must be converted before sending.

---

### 2. Why do we need a serializer?

* You might be producing records with Java objects like `String`, `Integer`, or even a custom POJO (Plain Old Java Object).
* The **Producer API** is generic — you can use any object type for keys and values.
* Before sending, these objects need to be **serialized** into byte arrays, which Kafka understands.
* That’s where the `Serializer` interface comes in.

---

### 3. `value.serializer` configuration

* Just like `key.serializer`, you must tell the producer how to serialize the **value** of your records.

* Example serializers included with Kafka:

  * `org.apache.kafka.common.serialization.StringSerializer`
  * `org.apache.kafka.common.serialization.IntegerSerializer`
  * `org.apache.kafka.common.serialization.ByteArraySerializer`

* If you’re using common Java types, you can use these directly.

* If you have a **custom object** (e.g., a `User` class), you’d typically:

  * Implement a custom serializer (convert object → JSON, Avro, or Protobuf → bytes).
  * Or use frameworks like **Kafka Avro Serializer**, **Protobuf Serializer**, or **JSON Serializer** from Confluent or other libraries.

---

### 4. Required settings

* **`key.serializer`** → must always be set (even if you don’t use keys → use `VoidSerializer`).
* **`value.serializer`** → must always be set, because you’ll always send some value.

Example producer properties:

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");

// Key serializer (say we use strings for keys)
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");

// Value serializer (say we use integers for values)
props.put("value.serializer", "org.apache.kafka.common.serialization.IntegerSerializer");
```

---

### 5. Example in action

If you create a record like this:

```java
ProducerRecord<String, Integer> record =
    new ProducerRecord<>("my-topic", "user123", 42);
```

* `"user123"` → key (String) → converted to bytes by `StringSerializer`.
* `42` → value (Integer) → converted to bytes by `IntegerSerializer`.
* Kafka stores/transmits them as byte arrays.
* When consumed, the consumer will use the matching **deserializer** (`StringDeserializer` and `IntegerDeserializer`) to convert them back.

---

**Summary:**

* `key.serializer` = defines how to convert keys → byte arrays.
* `value.serializer` = defines how to convert values → byte arrays.
* Both are required properties.
* Use Kafka’s built-in serializers for standard types, or write your own/custom ones for complex objects.

## Three Primary Methods of Sending Messages

1. Fire and Forget

We send message and dont care if it reached or not. Generally it does since Kafka is highly available and producer retries automatically.

In case of Timeout or non retriable errors, the message gets lost.

2. Synchronous Send

the send() message returns a Future object. We use get() to wait on the Furture and see if send() was successful before sending next record.

3. Asynchronous Send

We call the send() method with a callback function that triggers when kafka sends a response

**Sychronous Send Code**

Let’s unpack this step by step:

---

### 1. What does **sending a message synchronously** mean?

* When you use the Kafka producer, you call `send()` to send a message.
* `send()` is **asynchronous by default** — it immediately returns a `Future<RecordMetadata>`, and the actual send happens in the background.
* But you can force it to be **synchronous** by calling `.get()` on that future:

  ```java
  producer.send(record).get();
  ```
* This means your program waits until Kafka acknowledges the message before continuing.

---

### 2. Why would you send synchronously?

* You get immediate feedback on whether the message was successfully written or failed.
* You can catch exceptions like:

  * Broker errors (e.g., "not enough replicas").
  * Exhausted retries (Kafka gave up after multiple attempts).
* This can be useful in simple examples, tests, or when correctness is more important than speed.

---

### 3. The performance trade-off

* **Kafka brokers take some time to respond** to a produce request — it could be as quick as a couple of milliseconds, or as slow as several seconds (if the cluster is busy, network latency is high, or replicas need syncing).

* With synchronous sends:

  * The sending thread **blocks** (waits) until it gets the broker’s response.
  * During this time, it cannot send any other messages.
  * This makes throughput very low, because you’re effectively sending **one message at a time**.

* With asynchronous sends:

  * The producer can **batch multiple records** together in the background while waiting for acknowledgments.
  * This greatly improves throughput and efficiency.

---

### 4. Why synchronous is avoided in production

* Production applications usually need to send thousands or millions of messages per second.
* If each message is sent synchronously, the throughput drops drastically because the client spends most of its time waiting.
* That’s why synchronous sends are almost never used in real systems.
* They are often used only in **demos, tutorials, or test programs** where clarity is more important than performance.

---

* **Synchronous send** = wait for acknowledgment before sending the next message. Simple, but slow.
* **Asynchronous send** = fire off the message, keep working, and handle success/failure via callback. Much faster and used in production.

---

There are retriable and non retriable errors in Kafka, connection and leader unresponsive errors are retriable but message size too large is not.

### Async Send Callback Function

<img width="776" height="518" alt="image" src="https://github.com/user-attachments/assets/a3fa0106-e122-4ae6-afbf-ffe9b7c3db03" />

