### Auto Loader Concept in Databricks

Auto Loader is a Databricks feature for incrementally and efficiently ingesting new data files from cloud storage (S3, ADLS, GCS) into Delta Lake tables.

It solves the problem of:

“How do I continuously load only the new files that arrive in my data lake, without reprocessing old files every time?”

**⚙️ How it works**

**New files detection**

Auto Loader uses file notification or directory listing to detect new files in cloud storage.

Each file is processed exactly once.

**Schema handling**

Auto Loader can infer schemas automatically and evolve them as new fields appear.

Supports schema evolution modes like:

addNewColumns → automatically adds new columns.

rescue → unexpected fields are captured in _rescued_data column instead of failing.

**Incremental state tracking**

Auto Loader stores state in a schema location checkpoint directory, so it knows which files are already ingested.

**Streaming or batch**

Auto Loader works as a Structured Streaming source but can also be triggered in a batch-like mode.

### 🔑 Key Features

Scalable ingestion: Handles billions of files.

Efficient: Processes only new/changed files, no need for full scans.

Schema evolution: Adapts to changing data over time.

Rescue data: Keeps unrecognized/mismatched fields safe for later analysis.

Integration: Works seamlessly with Delta Lake, Structured Streaming, and Databricks Workflows.

### 📊 Modes of schema evolution

none → no schema changes allowed.

addNewColumns → automatically add new columns to the table.

rescue → unexpected fields go into _rescued_data.

Manual → you evolve schema explicitly using ALTER TABLE.

When we run readStream cell for first time, then run writeStream it fails

<img width="762" height="271" alt="image" src="https://github.com/user-attachments/assets/93d2efcc-54b7-456f-9a23-e7f8035352d3" />

But when it fails, the new column State is added to the schemaLocation folder.

The next time we run readStream it reads using the new schema and now after running writeStream it runs.

<img width="767" height="165" alt="image" src="https://github.com/user-attachments/assets/1326ddec-b465-41bc-a280-1e6d9800d604" />

In rescue mode we have a new column added called _rescue_data that holds the records that dont match the schema.

<img width="1335" height="511" alt="image" src="https://github.com/user-attachments/assets/19661590-7489-4feb-99d6-30cc652d2cc7" />

In None mode, we dont see a rescue_column option, 

<img width="1335" height="511" alt="image" src="https://github.com/user-attachments/assets/33f8a8a0-aef0-4f19-9110-1499c78a6ef6" />

There is no failure but the new column data does not get added. There is no schema evolution.

**🔒 Why use Auto Loader instead of plain Structured Streaming?**

Without Auto Loader: you’d have to rescan directories and manually deduplicate files.

With Auto Loader: file discovery and state management are built-in → scalable & cost-efficient.

---

## 🔹 1. What checkpointing is in Autoloader

When you use **Autoloader** (`cloudFiles`), it’s powered by **Structured Streaming**.

* Spark Structured Streaming needs to **remember progress** (which files have been processed, offsets, watermark, etc.).
* That “memory” is kept in the **checkpoint location** (usually in cloud storage like `dbfs:/checkpoints/...`).
* Without checkpoints, a restart would re-read the same files.

---

## 🔹 2. State storage in Structured Streaming

When you do **stateful operations** (e.g., `dropDuplicates`, aggregations, joins with watermarks, etc.), Spark must maintain a **state store**.

* By default, Spark stores this in **HDFS-compatible storage** under your checkpoint directory.
* However, Spark also supports **RocksDB as the backend for state storage**. RocksDB is faster and memory-efficient because it keeps state on **local disk** (per executor) rather than only on JVM heap.

---

## 🔹 3. Using RocksDB with Autoloader

In Databricks, you can enable RocksDB for Autoloader pipelines with stateful ops:

```python
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .load("/mnt/raw/crypto")  # Autoloader source
  .withWatermark("event_time", "10 minutes")
  .groupBy("symbol", window("event_time", "5 minutes"))
  .agg(F.avg("price").alias("avg_price"))
  .writeStream
  .format("delta")
  .option("checkpointLocation", "dbfs:/checkpoints/crypto_autoloader")
  .outputMode("append")
  .option("stateStore.rocksdb.enabled", "true")  # enable RocksDB
  .start("/mnt/bronze/crypto"))
```

## 🔹 4. How it works

* **Checkpoint location**: still needed (to store metadata, offsets, etc.).
* **State store**: if RocksDB enabled → state is stored on **local disk of each executor** (backed by RocksDB), instead of pure JVM memory.

  * Each executor writes RocksDB files under its working directory.
  * Spark will still write **state snapshots** to the checkpoint location for recovery.

---

## 🔹 5. Why RocksDB helps

* Without RocksDB: state is stored in **hash maps in JVM heap** → can cause OOM for large joins/aggregations.
* With RocksDB: state spills efficiently to disk, uses compression, and avoids large JVM GC pressure.
* Works especially well in **Autoloader pipelines with deduplication or watermark joins**.

---

## 🔹 6. Things to remember

* You must use **Databricks Runtime 10.4+** for RocksDB state store.
* The option is:

  ```bash
  spark.sql.streaming.stateStore.providerClass=org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider
  ```

  (Databricks simplifies this with `stateStore.rocksdb.enabled`).
* Still need cloud **checkpointLocation** → otherwise recovery after restart won’t work.

---

✅ **So in summary:**

* Autoloader always needs a **checkpoint location**.
* If you’re doing stateful ops, you can choose between **default HDFS state store** vs **RocksDB**.
* With RocksDB, state is on executor local disk, but still backed up into the checkpoint folder for recovery.

---

For file notification mode use ```option(cloudFiles.useNotifications,True)```
