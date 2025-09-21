# Kafka Broker OS Tuning

## Virtual Memory Concepts

Ideally Linux virtual memory system will autoscale and adjust itself depending on workload. We can tweak and make adjustments on how swap space is handled to suite Kafka needs.

<img width="1116" height="238" alt="image" src="https://github.com/user-attachments/assets/aeeabf0f-8be3-4168-ac61-d7de59136cfc" />

---

1. **Swapping = bad**

   * When a machine runs out of RAM, the OS can “swap” memory pages out to disk.
   * Disk is way slower than RAM.
   * So if Kafka’s memory gets swapped, everything slows down badly.

2. **Kafka depends on page cache**

   * Kafka doesn’t keep all messages in JVM heap.
   * Instead, it relies on the **Linux page cache** (OS memory used to cache disk files).
   * This makes reading/writing logs super fast (like “RAM-speed disk”).

3. **If swapping happens**

   * It means RAM is too small.
   * Now the OS uses disk for memory → very slow.
   * And since RAM is busy with swapping, there’s **less room left for page cache**.
   * Result: Kafka loses its main performance advantage.

---

### 🔹 Simple analogy

Think of **RAM as a kitchen counter**:

* Kafka keeps its working tools and most-used ingredients on the counter (page cache).
* If the counter is too small, the chef (OS) starts moving things to the **basement (disk swap)**.
* Every time Kafka needs something, the chef has to run to the basement and back → huge slowdown.
* Plus, with stuff in the basement, there’s even **less room left on the counter** → workflow collapses.

---

✅ **In short:**
Swapping in Kafka is terrible because:

* It makes memory operations slow (disk instead of RAM).
* It steals memory from the OS page cache, which Kafka relies on for fast log access.

---

### RAM vs Disk vs Page Cache

---

## 🔹 1. RAM (Physical Memory)

* This is the **actual physical memory chips** installed in your machine.
* Super fast (nanoseconds).
* Used for active data — what your CPU is working on right now.

---

## 🔹 2. OS Memory

* When people say “OS memory,” they usually mean the **portion of RAM managed by the Operating System**.
* The OS decides:

  * Which processes get how much RAM.
  * What part of RAM to use for **page cache** (caching disk files).
  * Whether to swap out inactive memory pages to disk if RAM runs low.
* So **OS memory is not separate from RAM** — it’s RAM under the OS’s control.

---

## 🔹 3. Disk (Persistent Storage)

* Completely different from RAM.
* Much slower (milliseconds).
* Stores data permanently (files, logs, databases).
* Examples: HDD, SSD, NVMe.

---

## 🔹 How they relate

* **RAM** = fast but limited, wiped when machine restarts.
* **Disk** = big, slow, permanent.
* **OS memory management** = decides how to best use RAM + when to move (swap) stuff to disk if RAM runs out.

---

## 🔹 Analogy

* **RAM = desk space** where you keep the stuff you’re working on right now.
* **Disk = filing cabinet** in the basement where you store everything long term.
* **OS memory management = office manager** who decides what stays on your desk (RAM), what gets cached nearby (page cache), and what gets moved to the basement (swap).

---

✅ **In short:**

* **OS memory** is just RAM managed by the operating system.
* RAM and disk are very different: RAM = fast, temporary; Disk = slow, permanent.
* Swapping happens when the OS moves data from RAM to disk because RAM is full → that’s what hurts Kafka.

---

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/e45b9ba9-9f03-4448-8982-d8788e43f1a9" />

There can be lot of performance issues having pages swapped to disk. If the VM system is swapping to disk then there is not enough memory being allocated to page cache.

---

## 🔹 1. What is swap space?

* **Swap space** = a portion of your disk reserved to act like extra RAM.
* If RAM is full, the OS can “swap out” some memory pages (inactive ones) to this disk space.
* This frees up RAM for active work.

✅ Good: prevents crashes when memory is tight.
❌ Bad: disk is *way* slower than RAM → performance tanks if swapping happens.

---

## 🔹 2. Why swap is not required

* A system can run without swap configured at all.
* If RAM runs out and no swap exists → the OS has no choice but to kill processes (OOM Killer).
* This is safer for performance-critical apps like **Kafka**, because it avoids the slowdown from swapping.

---

## 🔹 3. Why some swap is still useful

* Swap acts as a **safety net**.
* If something unexpected happens (like a memory leak), instead of instantly killing Kafka, the OS can temporarily push some memory to disk.
* This may keep the system alive long enough for you to fix the issue.

---

## 🔹 4. What is `vm.swappiness`

* `vm.swappiness` = Linux setting that controls **how aggressively the OS uses swap**.
* Range: 0–100.

  * `0` → avoid swap as much as possible.
  * `100` → swap aggressively, even if RAM is free.
* For Kafka and other high-throughput apps, best practice is:

  * Keep swap configured (safety net).
  * But set `vm.swappiness=1` → OS will only swap as a **last resort**.

---

## 🔹 5. Analogy

* **RAM = your desk** (fast access).
* **Swap space = basement storage** (slow to reach).
* **Swappiness = how eager the office manager is to move stuff to the basement**.

  * High swappiness → manager keeps clearing desk too early (slow).
  * Low swappiness → manager only uses basement if the desk is *completely full*.

---

✅ **In short:**
Swap space is disk space used as backup RAM. You don’t have to configure it, but it’s a good safety net. In Kafka, you don’t want the OS to swap unless it’s absolutely necessary — that’s why the recommendation is to set `vm.swappiness=1`.

---

### Swap vs Page Cache Drop Trade Off?

---

## 🔹 1. Page cache refresher

* Kafka writes logs to disk files.
* Linux keeps **recently used file data in RAM** (this is the page cache).
* Page cache makes reads/writes much faster, because you don’t always go to disk.
* So: **more RAM for page cache = better Kafka performance**.

---

## 🔹 2. What `vm.swappiness` controls

* When RAM is running low, Linux has two choices:

  1. **Drop some page cache** (free up memory by forgetting cached file data).
  2. **Swap out memory pages** from applications to disk (push part of their memory into swap).

* `vm.swappiness` decides which strategy Linux prefers.

  * High value (e.g. 60, default) → Linux is more likely to **use swap**.
  * Low value (e.g. 1) → Linux is more likely to **drop page cache** instead of swapping.

---

## 🔹 3. Why dropping page cache is better than swapping

* **Dropping page cache**:

  * You lose some cached file data.
  * But next time you need it, you just fetch from disk again (slower than cache, but predictable).
* **Swapping memory to disk**:

  * Takes active memory pages (from Kafka or other processes) and moves them to disk.
  * If Kafka needs those pages back → huge stall (disk is thousands of times slower than RAM).
  * Causes unpredictable latency spikes → very bad for Kafka.

👉 So the recommendation: better to **reduce page cache** than to start using swap.

---

## 🔹 4. Simplified analogy

* Imagine RAM as your **desk space**.
* Page cache = **reference books** you keep on your desk for quick access.
* Kafka’s working memory = **active notes** you’re writing on.

When desk space runs low:

* **Option A (drop cache):** Put away a few reference books (page cache). If you need them again, you fetch them from the library (disk).
* **Option B (swap):** Force yourself to put away half-written notes (swap). When you need them again, you must slowly re-read and re-write them from storage.

👉 Option A (drop cache) slows you down a little.
👉 Option B (swap) can freeze you mid-sentence.

---

✅ **In short:**

* `vm.swappiness` controls whether Linux prefers to **swap memory to disk** or **drop page cache** when RAM is low.
* For Kafka, it’s always better to **drop page cache** than to use swap, because swapping makes performance unpredictable.

---

## Swap is controlled by Linuz

---

## 🔹 1. What swap actually does

* The Linux kernel decides which **memory pages** to swap out to disk when RAM is tight.
* It doesn’t only swap “unused” memory — it can also swap out memory from processes that *are still running*.
* If the process suddenly needs that page again → it has to **page fault** and reload it from disk.
* That reload can take **milliseconds** (vs nanoseconds from RAM) → a huge delay.

---

## 🔹 2. Why this is unpredictable

* The kernel’s swapping decision depends on heuristics (like least-recently-used pages), but it isn’t perfect.
* A page Kafka really needs (e.g., part of a producer buffer or replica fetcher state) might get swapped out.
* Kafka doesn’t control *which* memory is swapped — the OS does.
* So you can suddenly get a **latency spike** even though Kafka is “healthy” otherwise.

---

## 🔹 3. Impact on Kafka

* Producer → sends data → broker stalls (waiting for swapped memory). Producer sees high latency.
* Consumer → fetch request delayed because Kafka’s fetch buffer got swapped.
* GC (garbage collector) → if its metadata gets swapped, GC pauses are even worse.

👉 This is why in Kafka best practices:

* Swap is treated as a **last resort only** (swappiness = 1).
* Or completely disabled on dedicated Kafka brokers.

---

## 🔹 Analogy

It’s like your notes are on your desk (RAM).
The office manager (OS) decides, “I think you don’t need this notebook right now” → and puts it in the basement (swap).
When you actually *do* need it, you have to run to the basement, fetch it back, and only then continue → unpredictable stall.

---

Yes - even actively used memory pages can be swapped to disk, and when Kafka needs them back, performance stalls unpredictably.

---

### TLDR!!!
---

## 🔹 1. Page cache drop

* The OS discards cached **file data** from RAM.
* That data is still **on disk** already (Kafka log segments).
* If Kafka needs it again → just read from disk normally.
* **Cost**: one normal disk read.
* **Predictable**: performance hit is known (disk I/O latency).

---

## 🔹 2. Swap

* The OS *actively writes* process memory pages (e.g., Kafka’s JVM heap objects, control structures) to swap space on disk.
* Those pages **do not exist on disk already** — the kernel must write them out before freeing RAM.
* If Kafka needs them back → it has to pause until the kernel reloads them from swap.
* **Cost**: one disk write *and* one disk read.
* **Unpredictable**: Kafka may stall at random, because it doesn’t control which memory pages get swapped.

---

## 🔹 3. Why Kafka cares

* Kafka log data (page cache) → dropping it is okay, since the log is durable on disk.
* Kafka’s heap memory (swap) → swapping it causes random stalls, because suddenly the broker can’t access in-use objects until they’re paged back.

---

## 🔹 Analogy

* **Page cache drop** = You borrowed a reference book and left it on your desk (RAM). The office manager takes it away. If you need it again, you just check it out from the library (disk). No harm done.
* **Swap** = You’re actively writing in your notebook (heap). The office manager snatches it, boxes it, and sends it to the basement (swap). If you need it mid-thought, you’re frozen until it’s retrieved.

---

✅ **So the difference:**

* Dropping page cache = safe, predictable slowdown (just a disk read).
* Swapping = unsafe, unpredictable stalls (extra writes, random process freezes).

---
