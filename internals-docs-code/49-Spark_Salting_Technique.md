# Salting in PySpark

Check below condition we get 15 records.

<img width="1262" height="924" alt="image" src="https://github.com/user-attachments/assets/6fce053f-2adb-433a-a184-547b3a087db5" />

The id=1 on left side is skewed and assume that the table2 is > 10 MB

Now salt the data, append a random number between 1-10 to the id on both the sides.

<img width="1590" height="739" alt="image" src="https://github.com/user-attachments/assets/5833dfc5-de2d-4546-aaa4-726ea548450c" />

All the salted keys go into different partitions and not just one like before.

<img width="1539" height="931" alt="image" src="https://github.com/user-attachments/assets/0ed11808-5990-41a3-9957-8e997c3b5856" />

Now there is an evident problem where we get only 3 records instead of the actual 15. So to tackle this on table2 we need to generate 10 salted keys for each id so that the join 
is possible.

**Before Salting**

<img width="1105" height="409" alt="image" src="https://github.com/user-attachments/assets/66342225-0131-4f27-9cc0-2ae87be0e42c" />

**After Salting**

<img width="1916" height="580" alt="image" src="https://github.com/user-attachments/assets/134f1d84-03aa-4b54-b60d-dddde674d822" />

## 🔑 2. Where Memory Comes Into Play

Salting helps with **shuffle balance**, but OOM can still happen depending on **join strategy**:

* **Broadcast Hash Join (BHJ)**

  * Spark broadcasts the smaller table to all executors.
  * ❌ If the **second table is large** (multi-GBs), broadcasting it will **OOM on driver/executors**.
  * Spark usually auto-switches to **Sort-Merge Join (SMJ)** if the table is bigger than `spark.sql.autoBroadcastJoinThreshold` (default \~10MB).

* **Sort-Merge Join (SMJ)**

  * Both tables are shuffled and sorted.
  * Salting works well here because it reduces shuffle skew.
  * ✅ No broadcast → less chance of OOM.
  * But if partitions are still unbalanced (or too wide), you can hit OOM during shuffle spill or sort buffer.

* **Shuffle Hash Join (rare)**

  * If memory per executor is low, hash table building can cause OOM.

---

## 🔑 3. So, If the Second Table is Large…

* **Yes, you can get OOM** if Spark mistakenly tries to broadcast it (or if you force broadcast with a hint).
* If Spark chooses **Sort-Merge Join**, OOM is less likely, but still possible if:

  * The salted distribution is still skewed (bad salt choice).
  * Shuffle partitions are too few (`spark.sql.shuffle.partitions` too low).
  * Executor memory is too small for sort buffers.

---

## 🔑 4. How to Avoid OOM in Large Second Table

✅ Best practices:

1. **Do not broadcast large table**

   * Check plan with `explain()`.
   * Disable broadcast for large tables:

     ```sql
     SET spark.sql.autoBroadcastJoinThreshold = -1;
     ```

2. **Use Sort-Merge Join + Salting**

   * Works best for large joins.

3. **Tune partitions**

   * Increase shuffle partitions (`spark.sql.shuffle.partitions`).
   * Repartition the large table on join key *before* join.

4. **Use Adaptive Query Execution (AQE)**

   * Spark 3+ can dynamically coalesce or split skewed partitions.
   * Enable:

     ```sql
     SET spark.sql.adaptive.enabled = true;
     SET spark.sql.adaptive.skewJoin.enabled = true;
     ```

5. **Check salt factor**

   * Too small → still skewed.
   * Too big → data explosion (Cartesian effect).
   * Rule of thumb: `salt_factor ≈ (skewed_key_rows / avg_rows_per_key)`.

---

✅ **Conclusion:**

* If the **second table is large**, Spark will **not** broadcast it by default (so no OOM in normal SMJ with salting).
* You’ll only hit **OOM** if:

  * You force broadcast on a large table, or
  * Shuffle/sort partitions are misconfigured.
* With **AQE + proper salting**, Spark can handle large second tables safely.
