## Kafka OS Tuning : Dirty Page Handling

Kafka relies on disk I/O operations to give good response time to producers sending the data.

Hence the log segments are put on a fast disk, it can be an individual disk with fast response time like SSD or a disk subsystem with lot of NVRAM for caching like RAID.

---

# 🔹 1. What are “dirty pages”?

* A **page** = a chunk of memory.
* A page is called **dirty** if it contains data that has been changed in memory but **not yet written to disk**.

  * Example: You write a log entry → it first goes into memory.
  * That memory page is now “dirty.”
  * Later, the kernel flushes it to disk.

This buffering is **good**, because writing to RAM is faster than writing to disk, and the kernel can group small writes together.

---

# 🔹 2. What is `vm.dirty_background_ratio`?

* It’s a **kernel parameter** that sets:
  👉 “How much of total system memory can be dirty pages **before the background flusher starts writing them to disk**.”
* Value is a **percentage of total RAM**.
* Default = 10.

  * Means: if 10% of system memory contains dirty pages, the kernel’s background flush process starts.

---

# 🔹 3. What happens if you lower it?

* Example: set `vm.dirty_background_ratio = 5`.
* Now the kernel starts flushing **earlier** (when only 5% of RAM is dirty).
* Result:

  * Dirty data stays in memory for less time.
  * Disk writes happen more continuously instead of in big bursts.
  * Good for workloads where you don’t want long spikes of writes.

---

# 🔹 4. Why not set it to 0?

* If it’s **0**, the kernel would flush **immediately** whenever any page becomes dirty.
* That means:

  * No buffering.
  * Every write goes straight to disk.
  * Eliminates the kernel’s ability to **smooth out temporary spikes** (e.g., a burst of writes).
  * Performance would tank, because you’d lose batching benefits.

---

# 🔹 5. Analogy

Think of RAM like a **kitchen counter** and disk like the **pantry in another room**:

* You prepare groceries (data) on the counter first.
* When the counter gets 10% full (default), the helper (kernel flusher) starts moving items to the pantry.
* If you lower it to 5%, the helper starts earlier → the counter never gets too messy.
* But if you set it to 0, the helper runs **every single time** you put something down → you can’t work efficiently anymore.

---

✅ **In summary:**

* `vm.dirty_background_ratio` controls when the kernel starts flushing dirty pages to disk.
* Lower values → smoother, more frequent flushes.
* Too low (like 0) → kills performance because every write goes straight to disk.

---

### Synchronous and Background Dirty Page Handling

Perfect 👍 you’re asking about the **second half of Linux dirty page handling** — `vm.dirty_ratio`. Let’s break it down step by step.

---

# 🔹 1. What is `vm.dirty_ratio`?

* It’s another Linux kernel setting (percentage of total RAM).
* It controls the **absolute upper limit** of dirty pages allowed in memory.

👉 Difference vs `vm.dirty_background_ratio`:

* **`dirty_background_ratio`** → threshold when background flushing starts.
* **`dirty_ratio`** → hard limit where normal processes are forced to stop and flush data themselves (**synchronous flush**).

---

# 🔹 2. Default Value

* Default = **20% of total memory**.
* Example: If you have 16GB RAM → at most 3.2GB can be dirty pages.
* If you reach this limit:

  * Any new writes block until data is flushed → app threads do the flushing.
  * This is much slower, because the app itself is waiting on disk I/O.

---

# 🔹 3. Raising the Limit

* If you set `vm.dirty_ratio = 60` or `80`:

  * Now up to 60–80% of memory can be dirty pages.
  * More data can stay in RAM before being forced to disk.
  * This means **higher throughput** for write-heavy apps like Kafka, because they batch more writes in memory before hitting disk.

---

# 🔹 4. Risks

* **More unflushed data in RAM** = if the server crashes, more data is lost.
* **Longer I/O pauses** = if memory suddenly fills with dirty pages, the kernel will force a **big synchronous flush** → applications block until gigabytes of data are written out.
* These pauses are sometimes called “I/O storms” or “write cliffs.”

---

# 🔹 5. Why Mention Kafka Replication?

* Kafka brokers rely on disk writes for durability.
* If you allow too many dirty pages (high `vm.dirty_ratio`), and the machine crashes, all that unflushed data is lost.
* **Replication across brokers** ensures that even if one machine loses data, others have a copy.
* So the text is saying:
  👉 “If you increase `dirty_ratio` to improve throughput, you must rely on **replication** to stay safe against data loss.”

---

# 🔹 6. Analogy

* Imagine you’re taking notes (data) on paper (RAM) before typing them into the computer (disk).
* Rule 1: At 5 pages of notes → your friend (background flush) starts typing them up slowly.
* Rule 2: At 20 pages → you’re **not allowed to write more notes** until you type everything in yourself (synchronous flush).
* If you increase the limit to 60 pages:

  * You can keep writing more before being forced to stop.
  * But if you trip the limit, you’ll have to type 60 pages at once — long pause.
  * If you spill coffee (server crash), you lose a lot more notes.

---

✅ **In summary:**

* `vm.dirty_ratio` = maximum dirty memory before synchronous flush kicks in.
* Default = 20%. Increasing to 60–80% improves write throughput for Kafka, but:

  * Increases risk of data loss on crash.
  * Increases risk of long blocking flushes.
* That’s why Kafka clusters should use **replication** if you tune this aggressively.

---
