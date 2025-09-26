# Kafka Configuring Producers Pt2

**linger.ms**

Let’s go step by step — this is about **how Kafka decides when to send a batch of messages** from the producer to the broker.

---

### 1. What batching means

* The Kafka producer doesn’t send each record immediately over the network.
* Instead, it **groups multiple records into a batch** (per partition).
* Batching reduces network overhead because fewer requests are sent.

---

### 2. How does the producer decide when to send a batch?

Two main triggers:

1. **Batch is full** → defined by `batch.size` (in bytes).

   * As soon as the buffer for a partition is full, it is sent immediately.
2. **Time is up** → controlled by `linger.ms`.

   * If the batch isn’t full, the producer can wait a little time to collect more messages.
   * Once `linger.ms` expires, the batch is sent, even if it isn’t full.

---

### 3. Default behavior (`linger.ms = 0`)

* By default, the producer **does not wait**.
* As soon as a sender thread is available, the record (even if it’s the only one in the batch) is sent.
* This gives **low latency**, but **poor throughput** (lots of small network requests).

---

### 4. Effect of setting `linger.ms > 0`

* The producer waits for up to that many milliseconds before sending a batch.
* This gives more time for additional records to accumulate in the batch.
* Benefits:

  * **Better throughput**: more messages per request, fewer network calls.
  * **Better compression**: larger batches compress more effectively.
* Trade-off:

  * **Increased latency**: each record may sit in memory slightly longer before being sent.

---

### 5. Example

Suppose:

* `batch.size = 16 KB`
* `linger.ms = 5`

Scenario:

* A record arrives, but the batch is not full.
* Instead of sending right away, the producer waits up to 5 ms for more records.
* If more records arrive, they are added to the batch.
* After 5 ms (or earlier, if the batch fills up), the batch is sent.

---

* `linger.ms = 0` → send as soon as possible (low latency, low throughput).
* `linger.ms > 0` → wait a little before sending (higher latency, but much better throughput and compression).

---

**buffer.memory**

Amount of memory producer will use to buffer messages waiting to be sent to broker.

If messages are sent by application faster than broker responds, additional send calls will be blocked for max.block.ms and wait for space to be freed up.

This timeout is thrown by ```send``` and not by Future callback function.

**compression.type**

Let’s break this down clearly — this is about the **`compression.type`** setting in the Kafka producer.

---

### 1. Default behavior

* By default, Kafka producer sends messages **uncompressed**.
* That means every record is sent as raw bytes, which consumes more **network bandwidth** and **broker storage**.

---

### 2. What `compression.type` does

* You can set `compression.type` in producer configs to one of:

  * `none` (default)
  * `snappy`
  * `gzip`
  * `lz4`
  * `zstd`

* The producer will then compress message batches before sending them to brokers.

* The broker stores the compressed form, and consumers can automatically decompress when reading (as long as they use a compatible client).

---

### 3. Why use compression?

* **Network utilization**: fewer bytes to send across the wire.
* **Broker storage**: compressed messages take up less disk space.
* **Throughput**: often improves, because network is a common bottleneck.

---

### 4. Trade-offs of different algorithms

* **Snappy** (by Google):

  * Good balance between compression ratio and speed.
  * Low CPU cost, fast to compress/decompress.
  * Recommended when you care about **performance + reducing bandwidth**.

* **Gzip**:

  * Slower, higher CPU overhead.
  * But achieves **better compression ratios** than Snappy.
  * Recommended if **network bandwidth is the bottleneck** and you can afford extra CPU cost.

* **LZ4**:

  * Very fast, better compression ratio than Snappy in some cases.
  * Good when you need **high throughput and low latency**.

* **Zstd** (newer, from Facebook/Meta):

  * Offers a tunable trade-off between compression ratio and speed.
  * Usually provides **better compression ratios** than gzip at similar or better speed.
  * Useful in modern Kafka clusters where efficiency matters.

---

### 5. How it works with batching

* Compression is applied **per batch**, not per individual message.
* This means if you use `linger.ms` and `batch.size` to allow larger batches, compression gets more effective.
* Example: a batch of 100 messages compressed together → far better ratio than compressing each one individually.

---

**In short:**

* `compression.type` controls whether and how messages are compressed.
* **Snappy** = fast, decent compression (good default for performance + bandwidth).
* **Gzip** = slower, best compression ratio (good for bandwidth-limited environments).
* **LZ4** = very fast, efficient for high throughput.
* **Zstd** = modern, tunable, often best of both worlds.
* Compression reduces network and storage usage, which are often bottlenecks in Kafka.

---

**batch.size**

When multiple records are sent to same partition, the producer will bundle them together.

When the batch is full, all messages in batch will be sent. However producer will not wait for entire batch to fill up. It can even send half filled queue or even one message.

Setting batch size to be too large will not cause memory delays it would just mean each batch will use more memory.

If we set it too small, then producer will need to send messages more frequently and causes overhead.

**max.in.flight.requests.per.connection**

This controls how many message batches the producer will send to the server without receiving a response. Higher settings can increase memory overhead in buffer bt improves throughput.

Default is 5.

<img width="721" height="456" alt="image" src="https://github.com/user-attachments/assets/b05aceb0-25a4-45d2-addf-48ac9e356d4d" />

**max.request.size**

Caps the size of the largest message that can be sent in one request. If its 1MB largest message we can send is 1MB or 1024 messages of 1Kb each.

Broker also has a limit on largest message it can receive. its set using max.message.bytes.

**receive.buffer.bytes** and **send.buffer.bytes**

These are sizes of send and receive buffers used by sockets when reading and writing data. If its -1 then OS defaults are used.

Its a good idea to increase this when Producers and Consumers communicate with brokers in different data centers.

There's a separate chapter on idempotence but these are the conditions to be satisfied.

- ```max.in.flight.requests.per.connection``` to be less than or equal to 5, retries > 0 and acks = all. Exception will be thrown if not satisfied.

