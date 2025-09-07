## Spark Driver Out Of Memory

---

# TL;DR — When the driver goes OOM

The driver JVM runs out of **heap memory** (or the driver process runs out of OS memory). Typical causes:

* You **collect** too much data (e.g. `df.collect()`, `toPandas()`).
* Building a **broadcast** (Spark collects small table on driver first).
* Very **many tasks/partitions** (driver holds large task metadata / DAG).
* Too many **cached blocks / block metadata** tracked on driver.
* Large **accumulators/driver-side state** (job results, listeners, query progress).
* Driver running in a resource-constrained environment (client mode / small driver container).
* Streaming state / progress objects growing unbounded (structured streaming).
* Python driver process OOM (PySpark `collect()` or `toPandas()` can blow Python memory).
* Huge closure serialization or large objects kept accidentally in driver variables.

---

# 1) Where driver memory is used (what can fill the driver heap)

* **Result aggregation**: results of `collect()`, `take()` that are brought to driver.
* **Broadcast creation**: driver materializes & serializes broadcast data before sending to executors.
* **Metadata**: DAG, StageInfo, TaskInfo, JobInfo, SQL plan metadata held in driver.
* **BlockManagerMaster metadata**: mapping of blockId → locations for cached blocks (large when many blocks cached).
* **Driver-side data structures**: listeners, accumulators, job results, streaming query progress history.
* **Serialized closures**: driver holds references to closures until shipped.
* **Driver UI & metrics objects**: Web UI stores some in-memory structures.
* **Python objects (PySpark)**: Python driver process memory is separate and can OOM even if JVM is fine.

---

# 2) Concrete examples and log clues

### A. Broadcast join causing driver OOM

Stack trace hint:

```
java.lang.OutOfMemoryError: Java heap space
at org.apache.spark.broadcast.TorrentBroadcast.writeBlocks(...)
```

**Meaning:** Spark tried to collect the broadcast side to the driver (to serialize and slice it) and the dataset was too large.

**Fixes:**

* Don’t broadcast that table. Disable or lower broadcast threshold:

  ```conf
  spark.sql.autoBroadcastJoinThreshold=10MB  # default ~10MB; reduce it
  ```
* Use shuffle join (remove `broadcast()` hint), increase driver memory, or pre-aggregate/filter to make broadcast side small.

---

### B. `collect()` / `toPandas()` errors

Symptom: `java.lang.OutOfMemoryError: Java heap space` OR Python `MemoryError` (if using `toPandas()`).
**Meaning:** you pulled a lot of rows into driver memory (JVM or Python).

**Fixes:**

* Avoid `collect()`. Use `write.parquet(...)`, `foreachPartition()`, or `toLocalIterator()` (streams partitions; but still must not accumulate full result).
* For pandas usage, use `df.limit(n).toPandas()` only for small n or use chunked writes.

---

### C. Too many partitions / tasks → metadata explosion

Symptom: driver memory grows gradually; many small tasks; driver GC overhead.
**Cause:** driver stores Task/Stage info per task. If partitions >> millions, driver metadata map grows big.

**Fixes:**

* Reduce number of partitions before heavy actions: use `repartition()` (careful: shuffle) or consolidate upstream.
* Avoid tiny files and extremely high partition counts.

---

### D. Large number of cached blocks

Symptom: driver memory tied to BlockManagerMasterMetadata; `Storage` tab shows many blocks.
**Fixes:**

* Reduce caching, unpersist unused cached RDDs/DataFrames.
* Use `MEMORY_AND_DISK_SER` or `DISK_ONLY` for huge caches.
* Consider checkpointing rather than caching many small blocks.

---

### E. Structured Streaming and state blowup

Symptom: streaming query state grows (map of keys), driver shows many state snapshots. RocksDB helps on executors but driver still holds metadata.
**Fixes:**

* Tune watermarks & state TTL.
* Use RocksDB state store (`stateStore.rocksdb.enabled=true`) to reduce executor heap; ensure checkpointing.
* Monitor state size and prune old state.

---

# 3) Root causes in order of frequency

1. **Collecting huge result sets** (most common rookie error).
2. **Broadcast of a too-large dataset** (common when `autoBroadcastJoinThreshold` too high or broadcast hinted).
3. **Too many partitions / tasks or excessively large DAG** (scale-related).
4. **Large number of cached blocks** (storage metadata explosion).
5. **Driver-side programming bug** (storing big objects in driver variables/closures).
6. **Streaming / long-running app accumulating state**, listeners, progress logs.
7. **Python-side memory usage (PySpark)** — separate Python process OOM.
8. **Operating in client mode on a weak edge node** (driver has limited resources).

---

# 4) Diagnostics — what to check first (quick checklist)

* **Check logs/stack trace**: look for `OutOfMemoryError` stack frames (e.g., `TorrentBroadcast`, `ObjectOutputStream`, `BlockManager`).
* **Spark UI (Driver)**:

  * Storage tab: many blocks?
  * Executors tab: driver metrics?
  * SQL/Jobs tabs: huge number of tasks?
* **YARN / cluster manager logs** (if on YARN): `yarn logs -applicationId <app>` for driver container logs.
* **Is it JVM OOM or Python OOM?** Python OOM shows `MemoryError`; JVM OOM shows `java.lang.OutOfMemoryError`.
* **Check driver heap usage / GC logs**: increase log level, enable GC logs, capture heap dump (`jmap -dump`) or thread dump (`jstack`).
* **Look for actions** preceding OOM: `collect`, `broadcast`, `toPandas`, large `take`, `count` on big DF, many `.cache()` calls.
* **Check number of partitions**: `df.rdd.getNumPartitions()` or examine job shuffle partitions.

---

# 5) Remedies & practical fixes

### Immediate (quick) fixes

* Avoid `collect()` / `toPandas()`; use `limit()` or write out to storage.
* Reduce/disable broadcasting:

  ```python
  spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10MB")  # lower it
  ```
* Increase driver memory:

  * `spark-submit --driver-memory 8g` or `spark.driver.memory=8g` (or change driver node type in Databricks).
* Set `spark.driver.maxResultSize` to a safe limit (default \~1g). If result may exceed, either increase or avoid collecting so big results.

### Code-level patterns to avoid driver OOM

* Use `foreachPartition()` to process data on executors instead of collecting to driver.
* Use streaming writes to disk / object store rather than collecting.
* Use `df.write.format(...).mode("append").save(...)` to persist results.
* Use distributed joins/aggregations; avoid forcing data to driver.

### Cluster/config tuning

* Increase `spark.driver.memory` and `spark.driver.memoryOverhead` (on YARN set memoryOverhead accordingly).
* For broadcast issues: decrease `spark.sql.autoBroadcastJoinThreshold` or remove `broadcast()` hints.
* For many small partitions: coalesce to fewer partitions **before** actions (use `coalesce(n)` if decreasing, `repartition(n)` if rebalancing needed).
* If using structured streaming with large state: enable RocksDB and tune `stateStore.rocksdb.*` settings; increase checkpointing.

### For PySpark users

* Avoid `collect()` → `toPandas()` is especially dangerous for big datasets.
* Use `toLocalIterator()` to stream partition rows to Python without loading all at once — but process and discard them rather than accumulating.

---

# 6) Example scenarios & exact config suggestions

**Scenario A — Broadcast OOM**

* Symptom: OOM with `TorrentBroadcast.writeBlocks`.
* Fix:

  ```python
  spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "5MB")
  # or remove broadcast hint
  df.join(other_df, "key")  # let it shuffle join
  ```

**Scenario B — collect() blew driver**

* Symptom: OOM right after a `collect()` call.
* Fix: Use:

  ```python
  for part in df.toLocalIterator():
      process_and_write(part)   # stream, do not save all to list
  ```

  or write to file:

  ```python
  df.write.mode("overwrite").parquet("/tmp/output")
  ```

**Scenario C — Too many tasks**

* Symptom: driver memory climbs during scheduling; job has millions of tasks.
* Fix:

  * Reduce partitions: `df.repartition(1000)` (or `coalesce` if only reducing and you don’t need balanced).
  * Increase `spark.executor.cores` or adjust parallelism.

**Scenario D — Block metadata explosion**

* Symptom: Storage tab shows huge number of blocks; driver memory high.
* Fix: `df.unpersist()` unused caches, or reduce cache footprint and use serialized storage level:

  ```python
  df.persist(StorageLevel.MEMORY_AND_DISK_SER)
  df.unpersist()  # when done
  ```

---

# 7) How to debug step-by-step (practical workflow)

1. Reproduce with smaller job locally or with logging turned on.
2. Inspect Spark driver logs for stack trace.
3. Check Spark UI:

   * Storage (# blocks),
   * SQL/Jobs (number of tasks, task sizes),
   * Executors (memory usage).
4. If broadcast suspected, check `explain()` and physical plan (`df.explain(True)` — look for `BroadcastHashJoin`).
5. Dump driver heap (`jmap -dump`) and analyze with MAT if you can. Look for big retained objects: byte\[] arrays (serialized broadcasts) or HashMaps of block metadata.
6. Fix code/config and re-run.

---

# 8) Extra notes / gotchas

* **Client vs Cluster mode**: In client mode the driver runs where you launched `spark-submit` (edge node). If that node is small you’ll OOM easily. Prefer cluster mode in prod.
* **Driver vs Executor OOM**: Executors OOM during task processing; driver OOM usually due to driver responsibilities (collection, broadcast, metadata). Different fixes.
* **Off-heap memory**: Spark (Tungsten) can use off-heap memory. Driver JVM heap OOM is different from OS OOM. Check overall process RSS if native memory also grows.
* **Spark History / UI retention**: Long-running apps accumulate a lot of in-memory history/history server metadata — may increase memory usage.

---

# 9) Quick checklist (what to try first)

* Did I call `collect()`/`toPandas()`? If yes, remove/limit it.
* Is a broadcast happening? Check `df.explain(True)`. Lower `spark.sql.autoBroadcastJoinThreshold`.
* Are there millions of partitions/tasks? Repartition/coalesce.
* Are many DataFrames cached? Unpersist unused caches or change storage level.
* Increase `spark.driver.memory` if legitimately needed.
* For streaming, enable RocksDB for heavy state, and tune watermark/timeToLive.

---

# Example decision trees for common symptoms

**Symptom:** `java.lang.OutOfMemoryError` with `TorrentBroadcast` in stack.
→ Cause: broadcast too large.
→ Quick fix: `spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10MB")` or remove broadcast hint.

**Symptom:** OOM after calling `df.collect()` or `df.toPandas()`
→ Don’t collect entire dataset. Use streaming writes or `toLocalIterator()` + process.

**Symptom:** Driver memory slowly climbs during scheduling of a huge job (many tasks)
→ Reduce partitions; increase driver memory; break job into smaller batches.

---
