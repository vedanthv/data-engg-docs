## Does the data output after all the execution on the executors is complete?

---

# 🔹 What Happens Inside the Executor

1. **Join Execution Starts**

   * Executor begins processing its partition (say, skewed table **B** against smaller **A**).
   * Table **A** (small) is buffered in memory.
   * Table **B** rows are streamed batch by batch (from memory and disk if spilled).

2. **Streaming Join Loop**

   * For each batch of rows from **B**, executor does the Cartesian product with **A**.
   * Emits output rows **immediately** (doesn’t wait to finish all batches).
   * If output rows themselves don’t fit in memory, they too can be spilled to temporary files (shuffle/disk spill).

3. **Completion of Task**

   * Executor keeps producing and spilling/streaming until **all rows for that partition are joined**.
   * When done, the results of that task are either:

     * Stored in shuffle files (if another stage depends on it).
     * Sent to the driver (if you requested `.collect()`).

---

# 🔹 What Happens at the Driver (for `.collect()`)

* The driver doesn’t wait for **all executors to finish globally** before receiving *anything*.
* Instead, each executor/task **sends its partition’s results** back as soon as they’re ready.
* Spark driver accumulates those partitions until the entire dataset is received.
* Only when **all partitions are received** does `.collect()` return the final Python list.

---

# 🔹 So to Your Question

> *“Does the executor show all data in `collect()` only when it finishes joining all batches of table B from disk?”*

✅ Yes, but **at the executor level**:

* Each executor must finish **its partition** (processing all batches of table B, including spills) before it can hand that partition’s results to the driver.
* The driver only gets **complete partitions** from executors, not row-by-row streaming.
* When all executors finish and send their partitions → driver merges them → `.collect()` returns.

---

# 🔹 Analogy (Apples Again 🍎)

* Executor = worker making apple pairs.
* Worker has one small bowl (A) and one giant truck (B).
* Worker processes crates from the truck one at a time, makes pairs with the bowl, and stacks results.
* Worker doesn’t hand over pairs to the boss (driver) **crate by crate** — he waits until **all his crates are processed** (partition done).
* Then he delivers his entire stack of results to the boss.
* Boss waits for all workers to deliver their stacks → only then shows you the final full list (`collect()`).

---

## ✅ Takeaway

* Executors **stream through skewed/spilled data batch by batch**.
* But the driver only receives results **partition by partition** (after executor finishes).
* `.collect()` blocks until *all executors* finish and return their partitions.
* That’s why `.collect()` can OOM the driver → it tries to hold the **entire dataset** at once.
