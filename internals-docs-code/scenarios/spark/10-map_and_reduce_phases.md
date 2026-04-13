# Shuffle = Map Phase + Reduce Phase

```
MAP PHASE (Shuffle Write)        REDUCE PHASE (Shuffle Read)
---------------------------      ----------------------------
Process partitions               Fetch shuffled data
↓                                ↓
Local aggregation (optional)     Merge data from all mappers
↓                                ↓
Partition by key                 Group by key
↓                                ↓
Write shuffle files              Final aggregation
```

---

# 1. Map Phase (Shuffle Write)

Runs on executors where data already exists.

### Steps

### a. Process Input Partition

Example:

```python
("A",1), ("A",2), ("B",3)
```

---

### b. Local Aggregation (Map-Side Combine)

Only for operations like `reduceByKey`:

```python
("A",1), ("A",2) → ("A",3)
```

Important:

* Happens **within a single partition only**
* Reduces data before shuffle

---

### c. Partitioning

Spark decides which reducer gets which key:

```python
partition = hash(key) % numPartitions
```

---

### d. Write Shuffle Files

* Data written to disk
* Organized per target reducer

---

# 2. Reduce Phase (Shuffle Read)

Runs on executors responsible for final output.

---

### a. Fetch Data

Each reducer:

* Pulls its partition data from **all map tasks**
* This is where **network transfer happens**

---

### b. Merge + Group by Key

Example incoming data:

```python
("A",3), ("A",9)
```

Grouped as:

```python
("A", [3,9])
```

---

### c. Final Aggregation

```python
("A",3) + ("A",9) → ("A",12)
```

---

# Critical Question:

## If we already got ("A",3), why do we need reducer?

Because that `"A",3` is **not global**, it is only **local to one partition**.

---

## Example Across Partitions

### Partition 1

```python
("A",1), ("A",2) → ("A",3)
```

### Partition 2

```python
("A",4), ("A",5) → ("A",9)
```

---

## After Map Phase

```python
Partition 1 → ("A",3)
Partition 2 → ("A",9)
```

At this point:

* Same key exists in multiple partitions
* Results are **partial**

---

## Reducer’s Job

Bring all `"A"` values together:

```python
("A",3) + ("A",9) → ("A",12)
```

This requires:

* Shuffle (to co-locate keys)
* Reduce phase (to finalize aggregation)

---

# What If We Skip Reduce Phase?

You would get:

```python
("A",3)
("A",9)
```

Which is:

* Incorrect
* Not a true aggregation

---

# Key Insight

| Stage            | Scope             | Role                |
| ---------------- | ----------------- | ------------------- |
| Map-side combine | Within partition  | Partial aggregation |
| Reduce phase     | Across partitions | Final aggregation   |

---

# Why This Design Matters

### Map Phase

* Reduces data early
* Minimizes shuffle size

### Reduce Phase

* Ensures correctness
* Combines distributed partial results

---

# Final Takeaway

> Map-side aggregation reduces data locally, but reducers are required to combine results across partitions and produce the final correct output.