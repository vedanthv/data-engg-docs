## Multi Version Concurrency Control in Liquid Clustering

**🔎 Why concurrent write failures still happen**

Delta uses Optimistic Concurrency Control (OCC) for all writes, even with Liquid Clustering:

Each writer reads a snapshot of the table (say version 5).

Both writers prepare their changes.

When committing:

Delta checks if the table’s latest version is still 5.

If yes → commit succeeds (new version 6).

If another writer already committed version 6 → your commit fails with a ConcurrentWriteException.

This ensures consistency. Without this, two writers could overwrite each other’s updates silently.

**💡 Liquid Clustering helps with performance, not concurrency**

Normally, clustering/partitioning means two writers updating the same partition can easily conflict (both touching the same small set of files).
With Liquid Clustering, rows are dynamically redistributed across files, so writers are less likely to clash on the exact same files.

But if two jobs still update overlapping rows (or even metadata) → OCC detects the conflict and one fails.

👉 So: Liquid reduces probability of collisions but does not eliminate them.

### Multi Version Concurrency Control

Two delivery guys arrive at the same time

Job A delivers pizzas for floor 5

Job B delivers pizzas for floor 5

With old mailboxes → they’d fight for the same mailbox. Chaos 😵

With liquid clustering + MVCC →

Each delivery guy puts pizzas into their own lockers (new files).

No overwrites. No conflicts.

The building’s delivery register (Delta Log)

Every delivery is recorded in the logbook at reception (Delta transaction log).

The log has versions:

Version 1: Deliveries from Job A

Version 2: Deliveries from Job B

So if you “replay the log,” you see all deliveries, in order.

Readers never see half-finished deliveries

If someone checks the log while Job A is writing, they still only see the previous version (Version 0).

Once Job A finishes, the log moves to Version 1.

Then readers see all of Job A’s pizzas atomically.

➝ This guarantees snapshot isolation = you only ever see a consistent view.

Concurrent jobs don’t lose pizzas

Even if Job A and Job B write at the same time, MVCC ensures:

Job A’s new files → recorded in Version 1

Job B’s new files → recorded in Version 2

Both sets of deliveries are preserved. ✅

**🧾 Real Delta Lake terms:**

Log = _delta_log JSON + Parquet files (transaction history).

New version = commit when a write finishes.

Readers always query a stable snapshot version, not files mid-write.

Concurrent writers: no overwrite, because each write creates new files, and old files are marked as removed in the log.

**💡 Takeaway:**

MVCC in Delta is like a time machine + logbook — every write creates a new version of the table, so no data is lost, no half-baked updates are visible, and readers/writers can happily work in parallel.

New files are created everytime we write to clustered delta table.

Delta Lake never updates files in-place (because they’re immutable in cloud storage).

Instead, on every write (insert, update, merge, etc.):

Delta writes new Parquet files with the updated data.

The Delta log (_delta_log) is updated with JSON/Checkpoint metadata pointing to the new set of files.

Old files are marked as removed, but not physically deleted until ```VACUUM```

**🧩 With Liquid Clustering**

Liquid Clustering’s job is to keep files balanced by row count (not by fixed partition values).

When you insert → Delta writes new files sized according to Liquid’s clustering strategy (e.g., ~1M rows per file).

When you update/merge/delete → Delta rewrites the affected rows into new files, distributed across existing clustering ranges.

The old files are marked as deleted in the log.

👉 Every commit adds new files and retires old ones.

### Demo

**🔹 Setup**

We’ll assume:

A Delta table with Liquid clustering enabled.

Target file size ~1M rows per file (for simplicity).

#### Step 1 : Create Empty Table

```sql
CREATE TABLE sales_liquid (
  order_id STRING,
  customer_id STRING,
  amount DECIMAL(10,2),
  date DATE
)
USING DELTA
CLUSTER BY (date);  -- Liquid Clustering on "date"
```

📂 At this point:

_delta_log/ has version 000000.json (empty schema).

No data files yet.

#### Step 2 : Insert First Batch

```sql
INSERT INTO sales_liquid SELECT ... 2M rows ...
```

📂 What happens:

Liquid clustering creates ~2 files of ~1M rows each.

_delta_log/000001.json records addFile for these.

File status:

```
file_0001.parquet (~1M)
file_0002.parquet (~1M)
```

#### Step 3 : Insert Second Batch

```sql
INSERT INTO sales_liquid SELECT ... 0.5M rows ...
```

📂 What happens:

New data → 1 new file of ~500k rows.

No rewrite of old files.

_delta_log/000002.json adds metadata.

```
file_0001.parquet (~1M)
file_0002.parquet (~1M)
file_0003.parquet (~0.5M)
```

#### Step 4 : Update 800k rows spread over files 1 and 2

```
UPDATE sales_liquid SET amount = amount * 1.05 WHERE date BETWEEN '2023-01-01' AND '2023-03-01';
```

📂 What happens:

Delta does not edit file_0001/0002 → marks them as removed.

Writes new replacement files (~800k rows redistributed).

```
file_0001 ❌ removed
file_0002 ❌ removed
file_0003.parquet (~0.5M)
file_0004.parquet (~0.4M)
file_0005.parquet (~0.4M)
```

#### Step 5 : Delete 100k rows

```
DELETE FROM sales_liquid WHERE customer_id = 'C123';
```

📂 What happens:

Affected rows come from file_0005.

File_0005 is removed, replaced with smaller rewritten file.

```
file_0003.parquet (~0.5M)
file_0004.parquet (~0.4M)
file_0006.parquet (~0.3M)
```
