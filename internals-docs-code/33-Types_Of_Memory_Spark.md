# Types of Memory in Spark

Great question 🚀 — Spark’s memory model is tricky but **very important for tuning and avoiding OOMs**. Let’s break it down.

---

# 🔹 Types of Memory in Spark

Broadly, Spark memory can be thought of at **two levels**:

1. **Execution vs Storage memory** (inside the JVM heap managed by Spark)
2. **Other JVM memory categories** (outside Spark’s unified memory)

---

## 1. **Execution Memory**

* **Used for:**

  * Shuffle operations (sort, join, aggregation)
  * Hash tables for joins and aggregations
  * Temporary buffers when spilling to disk
* **When it runs out:** Data is spilled to disk.

👉 Example:
When Spark does a `groupByKey` or `sortByKey`, it needs execution memory to build in-memory data structures.

---

## 2. **Storage Memory**

* **Used for:**

  * Caching/persisting RDDs/DataFrames (`df.cache()`, `rdd.persist()`)
  * Broadcast variables (e.g., in broadcast joins)
  * Unrolling RDD elements before caching

* **When it runs out:**

  * Cached blocks may be evicted (LRU).
  * Broadcast variables may spill.

👉 Example:
If you do:

```scala
val cachedDF = df.cache()
```

The DataFrame sits in **storage memory**.

---

## 3. **Unified Memory Management**

Since Spark 1.6+, **execution and storage memory share a unified pool** (`spark.memory.fraction`, default 60% of JVM heap).

* If execution needs more → it can borrow from storage (by evicting cached blocks).
* If storage needs more → it can borrow from execution, but only if execution isn’t using it.

---

## 4. **User Memory**

* **Used for:**

  * Data structures created by your Spark code inside UDFs, accumulators, custom objects, etc.
* Spark doesn’t manage this — it’s just regular JVM heap outside the unified pool.

👉 Example:
If you write a UDF that builds a big in-memory map, it goes into **user memory**.

---

## 5. **Reserved Memory**

* A fixed amount Spark reserves for internal operations (default \~300 MB per executor).
* Not configurable (except by changing Spark code).
* Ensures Spark doesn’t use 100% of JVM heap and leave nothing for itself.

---

## 6. **Off-Heap Memory**

* **Used for:**

  * Tungsten’s optimized binary storage format (off-heap caching)
  * When `spark.memory.offHeap.enabled=true`
* Managed outside JVM heap → avoids GC overhead.
* Configurable with `spark.memory.offHeap.size`.

👉 Example:
When you enable **off-heap caching**, Spark stores columnar data in native memory instead of the JVM heap for efficiency.

---

# 🔹 Spark Memory Layout (Executor JVM Heap)

```
+-------------------------------------------------------------+
| JVM Heap                                                    |
|                                                             |
|  Reserved Memory (~300MB, always kept aside)                |
|-------------------------------------------------------------|
| Unified Memory Region (spark.memory.fraction ~ 60%)         |
|   - Execution Memory  <---- shareable ----> Storage Memory  |
|-------------------------------------------------------------|
| User Memory (UDF objects, data structures, not Spark-managed)|
+-------------------------------------------------------------+
```

Outside JVM Heap:

* **Off-Heap Memory** (optional, managed by Spark)

---

# 🔹 Where They Are Used in Practice

* **Execution Memory** → Sorting, shuffling, joins, aggregations
* **Storage Memory** → Caching/persist, broadcast variables
* **User Memory** → UDFs, custom data structures, accumulators
* **Reserved Memory** → Spark internal bookkeeping
* **Off-Heap Memory** → Tungsten, columnar cache, avoids GC overhead

---

✅ **Summary:**

* Spark divides memory into **execution** (processing/shuffle) and **storage** (cache/broadcast).
* These share a **unified pool** for efficiency.
* **User memory** and **reserved memory** sit outside Spark’s control.
* **Off-heap memory** is optional but useful for performance.

---

# 🔹 1. Execution Memory

**Definition:**
Memory used for **processing computations** in Spark.

**What it stores:**

* Shuffle operations (sorts, aggregations, joins)
* Hash tables for joins and aggregations
* Temporary buffers for sorting, spilling data to disk

**Behavior:**

* Borrowable from storage memory if storage is not using all of its share (because Spark uses unified memory pool)
* If execution memory runs out, Spark **spills intermediate data to disk** to avoid crashing

**Example:**

```scala
df.groupBy("state").agg(sum("revenue"))
```

* Spark builds a hash map of states → **execution memory** is used.
* If too many states to fit in memory → spills to disk.

---

# 🔹 2. Storage Memory

**Definition:**
Memory used for **caching and storing data** in memory.

**What it stores:**

* Cached/persisted RDDs or DataFrames (`df.cache()`)
* Broadcast variables for joins
* Unrolled blocks before writing to cache

**Behavior:**

* Evictable (Spark uses LRU — least recently used blocks get removed if execution needs memory)
* Part of unified memory pool (`spark.memory.fraction`)
* Helps avoid recomputation or re-reading data from disk

**Example:**

```scala
val cachedDF = df.cache()
cachedDF.count()  // Storage memory used to keep DF in memory
```

---

# 🔹 3. Key Difference

| Feature           | Execution Memory                              | Storage Memory                                      |
| ----------------- | --------------------------------------------- | --------------------------------------------------- |
| Purpose           | For computations (shuffle, join, aggregation) | For caching/persisting data, broadcast variables    |
| Managed by Spark? | Yes (part of unified memory pool)             | Yes (part of unified memory pool)                   |
| Borrowable?       | Can borrow from storage if free               | Can be borrowed by execution if storage is not full |
| Eviction policy   | Spills to disk when full                      | LRU eviction to free memory for execution           |
| Examples          | groupBy, sort, join buffers                   | df.cache(), broadcast joins                         |

---

# 🔹 4. Unified Memory Pool

Spark >= 1.6 uses **unified memory management**:

```
+-----------------------------------------+
| Unified Memory Pool (spark.memory.fraction ~60%) |
|-----------------------------------------|
| Execution Memory   <------>  Storage Memory |
+-----------------------------------------+
```

* Execution can borrow from storage memory if needed.
* Storage can use free execution memory.
* Prevents fixed partitioning of memory and reduces OOMs.

---

✅ **In short:**

* **Execution Memory** → used **temporarily for computations** like shuffles, joins, sorts.
* **Storage Memory** → used to **store cached RDDs/DataFrames or broadcast variables** for reuse.
* Both share the **same unified memory pool**.

Perfect! Let’s visualize **Execution Memory vs Storage Memory** in Spark with a clear diagram and examples.

---

# 🔹 Spark Executor Memory Layout (Simplified)

```
Executor JVM Heap
+-----------------------------------------------------------+
| Reserved Memory (~300MB)                                  |
|-----------------------------------------------------------|
| User Memory (UDFs, accumulators, temp objects)           |
|-----------------------------------------------------------|
| Unified Memory Pool (~60% of executor memory)            |
|   +---------------------+  +--------------------------+ |
|   | Execution Memory    |  | Storage Memory           | |
|   |---------------------|  |--------------------------| |
|   | Used for:           |  | Used for:                | |
|   | - Shuffle buffers   |  | - Cached RDD/DataFrames  | |
|   | - Join/hash tables  |  | - Broadcast variables    | |
|   | - Aggregations      |  | - Unrolled blocks        | |
|   | If full -> spills   |  | If needed -> evict LRU   | |
|   +---------------------+  +--------------------------+ |
+-----------------------------------------------------------+
```

# 🔹 Examples of Memory Usage

| Operation / Action                        | Memory Used      | Notes                                                               |
| ----------------------------------------- | ---------------- | ------------------------------------------------------------------- |
| `df.groupBy("state").agg(sum("revenue"))` | Execution Memory | Hash map for aggregation stored here. If too large → spill to disk. |
| `df.sort("date")`                         | Execution Memory | Sort buffers stored in memory before writing or returning results.  |
| `df.cache()`                              | Storage Memory   | Cached DataFrame resides here for reuse.                            |
| `broadcast(df)`                           | Storage Memory   | Broadcasted DataFrame for joins stored here.                        |
| Temporary object inside a UDF             | User Memory      | Not managed by Spark’s unified memory.                              |

---

# 🔹 Unified Memory Behavior

* **Execution can borrow from storage** if storage has free space.
* **Storage can borrow from free execution memory** if execution isn’t using it.
* Helps prevent OOM errors and improves memory efficiency.

---

# 🔹 Quick Visual Summary

```
Execution Memory   <----> Storage Memory
 (shuffle, join)         (cache, broadcast)
      |                        |
      v                        v
  spills to disk           evict LRU
```

✅ **Key Takeaways:**

* **Execution Memory:** Temporary, computation-related, spills to disk if needed.
* **Storage Memory:** Persistent, caching/broadcast, evictable.
* **Unified Memory Pool:** Flexible sharing to reduce memory pressure.

---

When can we neither spill to disk or evict storage memory? [Link](https://vedanthv.github.io/data-engg-docs/Spark_YT/?h=spark+session#when-can-we-neither-evict-the-data-nor-spill-to-disk)

Would you like me to also give you **a real-world scenario of an executor OOM** and show *which type of memory* usually causes it (shuffle-heavy job vs cache-heavy job vs UDF-heavy job)?
