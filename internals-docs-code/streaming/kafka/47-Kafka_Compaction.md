# Compaction in Kafka

Normally, Kafka will store messages for a set amount of time and purge messages older than the retention period. However, imagine a case where you use Kafka to store shipping addresses for your customers. In that case, it makes more sense to store the last address for each customer rather than data for just the last week or year. 

This way, you don’t have to worry about old addresses, and you still retain the address for customers who haven’t moved in a while. Another use case can be an application that uses Kafka to store its current state. Every time the state changes, the application writes the new state into Kafka. 

When recovering from a crash, the application reads those messages from Kafka to recover its latest state. In this case, it only cares about the latest state before the crash, not all the changes that occurred while it was running. 

Kafka supports such use cases by allowing the retention policy on a topic to be delete, which deletes events older than retention time, or to be compact, which only stores the most recent value for each key in the topic. 

Obviously, setting the policy to compact only makes sense on topics for which applications produce events that contain both a key and a value. If the topic contains null keys, compaction will fail. Topics can also have a delete.and.compact policy that combines compaction with a retention period. 

Messages older than the retention period will be removed even if they are the most recent value for a key. This policy prevents compacted topics from growing overly large and is also used when the business requires removing records after a certain time period.

## In Depth Process of Compacting Events

---

### **What’s happening here:**

Kafka has a *log* for each partition.
This log contains a sequence of messages (records), and each message has:

* a **key** (used for identifying which record it belongs to)
* a **value** (the actual data)
* an **offset** (its position in the log)

When **log compaction** is enabled, Kafka removes old versions of messages that have the same key—keeping only the latest value for each key. This ensures that for every unique key, the log always contains the most recent state.

---

### **The split: Clean and Dirty sections**

Kafka divides each log into two portions:

1. **Clean section:**
   This part has *already been compacted*.
   It contains exactly one message per key — the latest value known at the last compaction.

   Think of it like the “cleaned shelves” in a library where only one copy of each book remains, nicely arranged.

2. **Dirty section:**
   This part contains *new messages* that were written **after** the last compaction.
   There may be multiple versions of the same key here (e.g., old updates that haven’t yet been cleaned).

   These are like the “newly arrived books” that haven’t yet been organized on the shelves.

---

### **How compaction works (step-by-step)**

When `log.cleaner.enabled=true`, Kafka runs background threads (called *log cleaner threads*) to perform compaction.

Here’s what happens internally:

1. **The cleaner thread selects a partition to compact**
   Each partition has a *ratio of dirty messages to total partition size*.
   The partition with the *highest ratio* (most unclean data) is chosen first.
   Essentially, Kafka asks: *“Which shelf has the most messy, duplicate books? Let’s clean that first.”*

2. **The cleaner reads the dirty section**
   It scans through all new messages written since the last compaction.

3. **It builds an in-memory map**
   This is where the interesting part begins.

---

### **Understanding the in-memory map (with analogy)**

The compaction thread creates an **in-memory map** while reading messages.
Each entry in this map represents one **unique key** seen in the dirty section.

Each entry contains:

* A **16-byte hash** of the message key (like a short fingerprint of the key)
* An **8-byte offset** (the position in the log of the *previous message* with the same key)

So each entry = **24 bytes total** (16 + 8).

---

### **Analogy: Library Shelf Cleaner**

Imagine Kafka’s log as a long shelf of books.

* Each **book** = a message
* The **book title** = message key
* The **content inside** = message value
* The **shelf position number** = message offset

Now, when new editions of the same book arrive (same key but new value), they’re added to the right end of the shelf (dirty section).
So you might have:

```
Offset 1: Book “A”, Edition 1
Offset 2: Book “B”, Edition 1
Offset 3: Book “A”, Edition 2
Offset 4: Book “C”, Edition 1
Offset 5: Book “A”, Edition 3
```

Now, “Book A” appears three times (old editions + latest edition).

When the **cleaner thread** comes by, it wants to keep *only the latest edition of each book* (each key).

---

### **How the map helps the cleaner**

As the cleaner scans through the dirty section:

* It writes an entry into the in-memory map saying:
  “I saw *Book A*, and the previous copy was at offset 3.”

* Later, when it sees another *Book A*, it updates that map entry:
  “Now the latest copy is at offset 5.”

This way, by the end of the scan, the map knows *where the latest version of each key is*.

So the map acts like a **catalog of latest editions**:

* Key → Latest known offset

Once the map is ready, the cleaner uses it to rewrite the log:

* It copies only the latest messages (one per key) to a new compacted segment (the new clean section).
* The older duplicates are skipped (the old editions are thrown away).

---

### **Memory efficiency explained**

Let’s say a segment is **1 GB** and each message is **1 KB**.

* That means there are **1,000,000 messages** in that segment.
* For each message, the cleaner might store **24 bytes** in memory.
* So total memory = **1,000,000 × 24 bytes = 24 MB**.

That’s very efficient — using just 24 MB of RAM to manage the compaction of a 1 GB log file.

And if some keys repeat (for example, 100 messages share the same key), the cleaner reuses the same entry in the map — reducing memory even further.

---

### **Summary Table**

| Concept              | What it means                                       | Analogy                                |
| -------------------- | --------------------------------------------------- | -------------------------------------- |
| **Clean section**    | Already compacted messages (latest version per key) | Organized shelf with one copy per book |
| **Dirty section**    | New un-compacted messages                           | Newly arrived messy books              |
| **Cleaner thread**   | Background worker doing compaction                  | Librarian cleaning the shelf           |
| **In-memory map**    | Tracks latest offsets for each key                  | Catalog of latest book editions        |
| **Hash (16 bytes)**  | Fingerprint of key                                  | Unique short ID for each book          |
| **Offset (8 bytes)** | Where the latest version sits                       | Shelf number of the latest edition     |

---

Excellent — this is the **second half** of the log compaction process:
how Kafka **allocates memory for compaction**, **decides what fits in memory**, and **rewrites compacted data** to disk safely.

Let’s unpack this carefully and use an analogy again (continuing with our *library* idea).

---

## **1. The Offset Map Memory Configuration**

Kafka uses an **in-memory offset map** for each cleaner thread during compaction.
This map is where it tracks the **latest offset for each key** (as we explained earlier).

However, memory is limited — so Kafka allows you to **configure how much total memory** all cleaner threads can use through:

```
log.cleaner.dedupe.buffer.size
```

This is a **global limit** shared among all cleaner threads.

### Example

If:

* You configure **1 GB** total for the cleaner offset map memory, and
* You have **5 cleaner threads** running,

then **each thread** will get **1 GB ÷ 5 = 200 MB** of memory for its own offset map.

---

## **2. Why this matters: fitting segments in memory**

Each thread needs enough memory to hold the offset map for at least **one segment** (the piece of the log file it’s compacting).

Each entry in that map = **24 bytes** (16-byte hash + 8-byte offset).
If a segment has 1 million messages (each 1 KB), that’s roughly **24 MB per map**.

So, if your 200 MB per thread can fit 8 such maps (8 × 24 MB ≈ 192 MB), that’s fine.

But if your segment is **huge**, say **20 GB**, and your map needs 480 MB, your 200 MB limit is too small —
Kafka will **log an error** saying it can’t compact that segment.

---

### **Analogy:**

Think of this as **how many library shelves you can clean at once**.

* Each cleaner (thread) has a **cart** with limited space (its offset map memory).
* The administrator gives the entire cleaning team **one big cart space budget** — 1 GB total.
* If there are 5 cleaners, each gets a **200 MB cart**.

Now:

* Each shelf (segment) must fit into one cleaner’s cart so they can organize it.
* If a shelf has *too many books* to fit, the cleaner can’t handle it — they leave it for later.
* The librarian (Kafka) will log an error and say:
  “Need bigger carts (more memory) or fewer cleaners (threads).”

---

## **3. Handling limited memory: which segments get compacted**

Kafka doesn’t need the **entire dirty section** to fit at once.
It only needs **at least one segment** to fit into memory.

If there’s room for more segments, Kafka will compact as many as fit — **starting with the oldest** ones first (like cleaning the oldest shelves first).

Any remaining segments stay “dirty” until the next compaction round, when more memory or threads become available.

---

### **Analogy:**

If your cleaners have carts that can only hold 2 shelves’ worth of books at once:

* They’ll start with the **oldest shelves**.
* Once done, they’ll go back later for the newer ones.

---

## **4. After the offset map is built — the actual compaction**

Once the in-memory map is built, the cleaner moves to the **compaction stage**.
Here’s the sequence:

### Step 1: Read through *clean segments* (starting from oldest)

The cleaner begins reading existing “clean” parts of the log (which contain previously compacted data).

For each message in those segments:

* It checks if the **key** is still in the **offset map**.

### Step 2: Check each message key

There are **two cases**:

1. **Key NOT in offset map:**

   * That means this message is *still the latest value* for that key.
   * The message is copied into the **replacement segment** (the new, compacted file).

2. **Key IS in offset map:**

   * That means the cleaner has already seen a **newer version** of this key later in the log.
   * The old message is **skipped** (not copied).
   * The key stays in the map so later duplicates can still be identified.

### Step 3: Write to a new replacement segment

As it filters, the cleaner writes the retained messages to a **new temporary segment** file.

Once the full segment is processed, Kafka:

* **Atomically swaps** the new compacted segment for the old one.
* Deletes the old un-compacted file.
* Moves on to the next segment.

This ensures **no data loss** even if Kafka crashes midway — it never overwrites the original file until the new one is fully written.

---

### **Analogy: Librarian cleaning the shelves**

Imagine the librarian (the cleaner thread) doing this:

1. They have their **cart (offset map)** filled with the latest edition of each book (latest offsets).
2. They go back to the **oldest shelf** and check every book:

   * If that title **is not in their cart**, it means no new edition has replaced it → keep it.
   * If the title **is in their cart**, it means a newer edition exists → skip this one.
3. They then place the kept books onto a **new clean shelf** (replacement segment).
4. When done, they swap the old shelf for the new one and move to the next.

By the end, there’s **only one copy per book**, and always the **latest edition**.

---

## **5. The end result**

After compaction:

* The **clean section** now contains one message per key — the most recent version.
* The **dirty section** will fill up again over time as new updates arrive.
* Cleaner threads will periodically repeat this process.

Kafka’s log thus becomes a **“stateful changelog”**, where the log always reflects the latest state per key.

---

### **Summary Table**

| Concept                            | Kafka Behavior                      | Analogy                                              |
| ---------------------------------- | ----------------------------------- | ---------------------------------------------------- |
| **log.cleaner.dedupe.buffer.size** | Total memory for all offset maps    | Total cart space for all cleaners                    |
| **Cleaner threads**                | Each gets a portion of total memory | Each librarian gets a cart                           |
| **At least one segment must fit**  | Otherwise compaction fails          | Each cleaner must be able to hold at least one shelf |
| **Compacts oldest segments first** | When memory is tight                | Start cleaning from oldest shelves                   |
| **Offset map lookup**              | Skip old keys, keep latest          | Keep only latest book editions                       |
| **Replacement segment**            | Written safely, then swapped        | Clean shelf replaces messy one                       |
| **Final state**                    | One message per key                 | One edition per book title                           |

---