## 1. What bucketing does

When you write:

```python
df.write.bucketBy(10, "user_id").saveAsTable("users_bucketed")
```

Spark:

* Hashes `user_id`
* Assigns rows to 10 buckets
* Shuffles data so that rows with the same bucket go together
* Writes bucket files

So bucketing itself already involves a shuffle.

---

## 2. What happens without repartition

If you do not repartition:

* Input data may be unevenly distributed across partitions
* Some partitions may contain a lot of rows for the same key
* During the bucketing shuffle, some tasks become heavy (data skew)
* You may get:

  * Uneven task execution times
  * Poor parallelism
  * Many small or inconsistent files per bucket

---

## 3. Why repartition helps

When you do:

```python
df.repartition(10, "user_id") \
  .write.bucketBy(10, "user_id") \
  .saveAsTable("users_bucketed")
```

you are:

### a. Pre-distributing data

* Data is already shuffled by `user_id`
* Each partition contains a more balanced subset

### b. Aligning partitions with buckets

* Number of partitions = number of buckets
* Each partition roughly corresponds to one bucket

### c. Reducing skew

* Large keys are better distributed before writing

### d. Improving write efficiency

* More predictable file sizes
* Better utilization of executors

---

## 4. Important point

Even without `repartition`, Spark will still perform a shuffle for bucketing.

The difference is:

* Without repartition → Spark controls distribution (less predictable)
* With repartition → You control distribution (more efficient)

---

## 5. When to use repartition before bucketing

Use it when:

* Data is large
* There is skew on the bucketing column
* You want better control over number of tasks and files

Skip it when:

* Data is small
* Distribution is already uniform

---

## 6. Rule of thumb

```python
repartition(number_of_buckets, bucket_column)
```

This keeps partitioning and bucketing aligned and avoids unnecessary inefficiencies.

---

## Final summary

Bucketing already requires a shuffle.
Repartitioning before bucketing is done to control that shuffle, reduce skew, and improve performance.

Great — let’s look at a **skewed data example**, where repartition actually makes a big difference.

---

# Example Setup (Highly Skewed Data)

Assume:

* Number of buckets = **4**
* Column = **user_id**

Input data:

| Row | user_id |
| --- | ------- |
| 1   | 101     |
| 2   | 101     |
| 3   | 101     |
| 4   | 101     |
| 5   | 101     |
| 6   | 102     |
| 7   | 103     |
| 8   | 104     |

 Here:

* `101` is **heavily skewed** (dominates data)

---

# Case 1: Without Repartition

## Initial partitions (uneven + skewed)

| Partition | user_ids           |
| --------- | ------------------ |
| P1        | 101, 101, 101, 101 |
| P2        | 101                |
| P3        | 102, 103, 104      |

---

## During bucketing (shuffle)

Hash mapping:

| user_id | bucket |
| ------- | ------ |
| 101     | 1      |
| 102     | 2      |
| 103     | 3      |
| 104     | 0      |

---

## What happens internally

* All `101` rows must go to **bucket 1**
* Most of them are already in P1 → one task becomes huge

---

## Task load during write

| Task | Data processed          |
| ---- | ----------------------- |
| T1   | 101, 101, 101, 101, 101 |
| T2   | 102                     |
| T3   | 103                     |
| T4   | 104                     |

---

## Problem

* One task is **very heavy**
* Others are almost idle
* Slow job due to **data skew**

---

# Case 2: With Repartition Before Bucketing

## Step 1: Repartition by user_id

| Partition | user_ids                |
| --------- | ----------------------- |
| P0        | 104                     |
| P1        | 101, 101, 101, 101, 101 |
| P2        | 102                     |
| P3        | 103                     |

---

## Important insight

Even after repartition:

 All `101` still go to **same partition**
 Because hash(101) is fixed

So skew **still exists**

---

# Then why repartition helps?

Because in real scenarios:

### Without repartition:

* Skew + random distribution = worse imbalance
* Some partitions overloaded even before shuffle

### With repartition:

* At least:

  * Data is **predictably grouped**
  * Shuffle becomes **more structured**
  * Spark can schedule tasks better

---

# But the real limitation

 **Repartition alone cannot fix skew for a single key**

Because:

| user_id | bucket   |
| ------- | -------- |
| 101     | always 1 |

So:

* All `101` must go to **same bucket**
* One bucket will always be heavy

---

# How skew is actually handled (advanced insight)

To truly fix skew, you need:

### 1. Salting

| user_id | salt | new_key |
| ------- | ---- | ------- |
| 101     | 0    | 101_0   |
| 101     | 1    | 101_1   |

Now data spreads across buckets

---

### 2. Increasing number of buckets

More buckets → better distribution

---

### 3. Skew join optimization (Spark AQE)

Spark dynamically splits skewed partitions

---

# Final takeaway

| Concept       | What it does                  |
| ------------- | ----------------------------- |
| Repartition   | Improves overall distribution |
| Bucketing     | Fixes storage layout          |
| Skewed key    | Still goes to same bucket     |
| True skew fix | Needs salting or AQE          |

---

# One-line interview answer

Repartition helps organize data before bucketing, but it **cannot eliminate skew for a single heavily repeated key**, because bucketing is hash-based and deterministic.