## Kafka Setup Hardware Considerations

### Disk Throughput

<img width="613" height="546" alt="image" src="https://github.com/user-attachments/assets/486efa9b-fb7d-4217-bb00-8ee21084acd4" />

SSD's are used if there are lot of client connections.

### Disk Capacity

<img width="752" height="456" alt="image" src="https://github.com/user-attachments/assets/c435931d-76d5-4738-bc3e-d3bf5b491ca3" />

### Memory

<img width="805" height="244" alt="image" src="https://github.com/user-attachments/assets/a754c6bd-a1d9-47fd-9d93-69794a833369" />

<img width="781" height="398" alt="image" src="https://github.com/user-attachments/assets/65f3311e-a6d9-4ccb-ba6d-0d348dc897c1" />

---

## 🔹 1. JVM Heap Basics

* Kafka brokers run on the **Java Virtual Machine (JVM)**.
* The JVM provides a **heap** = the memory area where **Java objects** live (data structures, buffers, metadata, etc.).
* The heap is managed by the **Garbage Collector (GC)**, which automatically frees unused objects.

---

## 🔹 2. What goes into Kafka’s Heap

Even though Kafka is an I/O-heavy system (most data lives on disk or page cache), it still needs the heap for several critical tasks:

1. **Message Buffers**

   * Temporary storage for messages being read from producers before written to disk.
   * Buffers used when serving fetch requests to consumers.

2. **Metadata**

   * Cluster metadata: topics, partitions, offsets, leader/follower info.
   * Zookeeper/KRaft state in memory.

3. **Indexes and Caches**

   * Offset index and time index objects.
   * In-memory caches like the `ReplicaFetcher` buffer, producer state maps, etc.

4. **Control Structures**

   * Java objects representing network connections, requests, and responses.
   * Threads, queues, locks, and other concurrency structures.

5. **ZooKeeper/KRaft client state**

   * If Kafka is using ZooKeeper (older versions), ZooKeeper client connections use heap.
   * In KRaft (newer versions), metadata quorum state also lives in heap.

---

## 🔹 3. What does *not* live in Heap

* **Actual log data** (the big message payloads) is written to **disk** (segment files).
* Kafka relies heavily on the **OS page cache** to serve log reads/writes efficiently.
* So the heap is not where Kafka keeps gigabytes of topic data — it’s more for metadata and transient objects.

---

## 🔹 4. JVM Heap + GC Issues in Kafka

* If heap is too small → OutOfMemoryError (OOM).
* If heap is too big → GC pauses get long (stop-the-world events).
* That’s why Kafka best practice is:

  * Keep heap **moderate** (e.g., 4–8 GB for brokers, even if broker has 64–128 GB RAM).
  * Let the **OS page cache** handle log segment data.
  * Use **G1 GC** (Garbage First) for predictable pause times.

---

## 🔹 5. Analogy

* Think of Kafka like a **library**:

  * The **heap** is the librarian’s desk (indexes, notes, active tasks).
  * The **page cache + disk** is the massive archive of books (actual topic data).
* The librarian’s desk must be tidy and efficient (GC keeps it clean), but the heavy lifting (book storage) happens outside the desk.

---

✅ **In short:**
In Kafka, the JVM heap holds **metadata, temporary buffers, and control structures**, but **not the bulk of the log data**. That bulk lives in disk files + OS page cache. The JVM heap’s job is to make sure Kafka can efficiently manage metadata, requests, and temporary data, while avoiding GC stalls.

---

### Networking

<img width="769" height="513" alt="image" src="https://github.com/user-attachments/assets/be4bccfc-a87a-4e3a-b191-89a5ed38a5fb" />

We should have atleast 10Gb NICs and older 1Gb NICs is not sufficient.

### CPU

<img width="785" height="424" alt="image" src="https://github.com/user-attachments/assets/a7f06d13-a1a1-4fe9-aea1-8ca2e6cc4f2b" />
