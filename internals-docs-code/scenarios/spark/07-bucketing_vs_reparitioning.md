# Core Difference (in one line)

* **Repartitioning** = controls **how data is distributed during execution**
* **Bucketing** = controls **how data is stored on disk**

They solve **different problems**

---

# 1. Repartitioning (Execution-time concept)

Happens **before computation or write**

### What it does:

* Redistributes data across partitions
* Controls parallelism
* Helps avoid uneven workloads

### Think of it as:

> “How should I divide work across machines right now?”

---

### Example

| Partition | user_ids |
| --------- | -------- |
| P0        | 101, 102 |
| P1        | 103      |
| P2        | 104, 105 |

After repartition by `user_id`:

| Partition | user_ids |
| --------- | -------- |
| P0        | 101, 101 |
| P1        | 102, 102 |
| P2        | 103      |
| P3        | 104, 105 |

✔ Improves execution balance
✔ Used during transformations and writes

---

# 2. Bucketing (Storage-time concept)

 Happens **when writing table**

### What it does:

* Writes data into fixed number of **bucket files**
* Based on hash of a column

### Think of it as:

> “How should I organize data on disk for future queries?”

---

### Example (4 buckets)

| Bucket | user_ids |
| ------ | -------- |
| 0      | 104      |
| 1      | 101, 101 |
| 2      | 102, 102 |
| 3      | 103      |

✔ Used for **join optimization**
✔ Avoids shuffle in future queries

---

# 3. Why Bucketing is Powerful (even if it doesn't fix skew)

This is the key point you’re missing.

 Bucketing is **not for skew handling**

 It is for **avoiding shuffle later**

---

## Example: Join Without Bucketing

Two tables:

| Table A | user_id |
| ------- | ------- |
|         | 101     |
|         | 102     |

| Table B | user_id |
| ------- | ------- |
|         | 101     |
|         | 102     |

### What Spark does:

* Shuffle both tables
* Expensive

---

## Example: Join With Bucketing

Both tables:

* bucketed on `user_id`
* same number of buckets

Now:

 Bucket 1 of A joins with Bucket 1 of B
 No shuffle needed

---

# 4. Why Repartition + Bucketing Together

Now your original doubt:

> “If repartition doesn’t fix skew, why use it?”

Answer:

* Bucketing = final layout (mandatory for optimization)
* Repartition = helps write that layout efficiently

---

### Without repartition

* Messy input
* Heavy shuffle during write
* Slow job

---

### With repartition

* Cleaner distribution before write
* Better parallelism
* Faster write

---

# 5. Final Comparison Table

| Feature          | Repartition            | Bucketing             |
| ---------------- | ---------------------- | --------------------- |
| When applied     | During execution       | During write          |
| Purpose          | Distribute data evenly | Organize data on disk |
| Helps with skew  | Partially              | No                    |
| Helps joins      | No                     | Yes (major benefit)   |
| Persistent       | No                     | Yes                   |
| Shuffle involved | Yes                    | Yes                   |

---

# Final Mental Model

* Repartition = **how work is split now**
* Bucketing = **how data is stored for later**