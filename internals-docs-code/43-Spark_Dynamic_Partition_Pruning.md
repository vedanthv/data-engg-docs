# Dynamic Partition Pruning in Spark

---

# 🔹 1. The Core Problem

Imagine you have a **fact table** partitioned by `date` (billions of rows, thousands of partitions).

Example:

```sql
SELECT *
FROM sales
WHERE sales.date IN (SELECT promo_date FROM promotions);
```

* Here, `promo_date` values are **not known at query compile time** (because they come from another table).
* Spark **cannot prune partitions statically**.

Without DPP, Spark scans **all partitions of sales**, then filters — very expensive.

---

# 🔹 2. Why DPP Works (Internals)

Spark 3.x introduced a mechanism where:

1. **Query is split into two stages:**

   * Stage 1: Collect partition filter values (from `promotions`).
   * Stage 2: Push those values **at runtime** into the scan of `sales`.

2. **Broadcasting comes in:**

   * The **small dimension table (`promotions`)** is broadcast to all worker nodes.
   * This lets every executor know exactly **which partitions of `sales` to scan**.

3. **Dynamic Filter Expression:**

   * Spark inserts a `DynamicPruningExpression` node in the query plan.
   * This acts as a runtime filter for partition values.

---

# 🔹 3. Before vs After DPP

### ❌ Without DPP

Execution Plan (simplified):

```
Scan sales (ALL partitions)
   Filter: date IN (subquery(promotions))
```

* All partitions are scanned (huge I/O).
* Filtering happens *after* reading data.

---

### ✅ With DPP

Execution Plan (simplified):

```
BroadcastHashJoin
   Left: Scan sales (partition filters: date = dynamicpruning#...)
   Right: Broadcast(promotions)
```

* `promotions` table is **broadcasted** (small).
* Spark evaluates filter values at runtime.
* Only matching partitions are scanned.

You’ll see in `.explain(true)` something like:

```
:dynamicpruning#... (isnotnull(promotions.date))
```

---

# 🔹 4. Why Broadcasting Matters

* DPP relies on **dimension table being small enough** to broadcast.
* Broadcast ensures **all executors** get the filter values quickly.
* If the table is large, Spark may fallback to **non-broadcast mode** (still works, but slower).

---

# 🔹 5. Configs Controlling DPP

```sql
SET spark.sql.optimizer.dynamicPartitionPruning.enabled = true;   -- enable/disable DPP
SET spark.sql.optimizer.dynamicPartitionPruning.useStats = true; -- prune only if selectivity helps
SET spark.sql.optimizer.dynamicPartitionPruning.reuseBroadcastOnly = true; -- requires broadcast
SET spark.sql.optimizer.dynamicPartitionPruning.fallbackFilterRatio = 0.5; -- fallback if not selective
```

---

# 🔹 6. Real Example in Databricks

```sql
-- Fact table partitioned by date
CREATE TABLE sales (
  order_id STRING,
  amount DECIMAL,
  date DATE
)
USING delta
PARTITIONED BY (date);

-- Dimension table
CREATE TABLE promotions (promo_date DATE);

-- Query with DPP
SELECT s.order_id, s.amount
FROM sales s
JOIN promotions p
  ON s.date = p.promo_date;
```

* If `promotions` has only 3 dates, DPP ensures **only those 3 partitions of `sales` are read**.
* Without DPP → all partitions scanned.

---

# 🔹 7. Exact Reason DPP Improves Performance

* **Reduces I/O** → fewer partitions scanned.
* **Reduces shuffle** → only data from relevant partitions enters the join.
* **Pushdown at runtime** → avoids loading terabytes unnecessarily.

---

✅ **In summary:**

* DPP works because Spark can **delay partition pruning until runtime**.
* It collects filter values (from another query/dimension) → broadcasts them → applies as **partition filters** before scanning the fact table.
* This is why execution plans show `DynamicPruningExpression`.

---

<img width="1279" height="666" alt="image" src="https://github.com/user-attachments/assets/024789ae-57f8-4fbd-be9f-fda895b1c224" />

At runtime a subquery is sent to main table that looks like this:

```sql
select * from main_table where sales_date in (select dates from small_table)
```

So essentially to make this work, the main table should be partitioned and the smaller table should be broadcastable.
