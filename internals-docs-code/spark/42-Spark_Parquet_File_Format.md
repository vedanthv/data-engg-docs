# 1. What is Parquet?

**Apache Parquet** is a **columnar storage file format** designed for:

* Big data processing
* Analytical workloads (OLAP)
* Efficient compression and query performance

 Instead of storing data row by row, it stores data **column by column**

---

# 2. Row vs Column Storage (Core Idea)

## Row-based (CSV, JSON)

```
Row1: id, name, age
Row2: id, name, age
```

## Columnar (Parquet)

```
Column id   → [1, 2, 3]
Column name → [A, B, C]
Column age  → [20, 25, 30]
```

---

# 3. Why Columnar Matters

### 3.1 Reads only required columns

```python
df.select("name")
```

 Parquet reads only:

```
name column
```

NOT entire row

---

### 3.2 Better compression

* Same column → similar data
* Compression algorithms work better

Example:

```
age: 25, 25, 25, 25 → highly compressible
```

---

### 3.3 Faster aggregation

```sql
SELECT avg(age)
```

 Only `age` column scanned → faster

---

# 4. Parquet File Structure (Deep Dive)

A Parquet file is not just “data”; it has a hierarchical structure:

```
File
 ├── Row Groups
 │     ├── Column Chunks
 │     │     ├── Pages
 │
 └── Footer (Metadata)
```

---

## 4.1 Row Group

* Horizontal partition of data
* Contains multiple rows
* Typical size: 128 MB (configurable)

 Each row group is processed independently → parallelism

---

## 4.2 Column Chunk

Inside each row group:

* Data is stored **column-wise**

Example:

```
Row Group 1:
   id column chunk
   name column chunk
   age column chunk
```

---

## 4.3 Pages (smallest unit)

Each column chunk is split into pages:

* Data pages
* Dictionary pages

 This enables:

* Fine-grained reading
* Compression

---

## 4.4 Footer (Very Important)

Stored at the **end of the file**

Contains:

* Schema
* Column metadata
* Statistics (min, max, null count)
* Row group locations

 Spark reads footer first to decide:

* What to scan
* What to skip

---

# 5. Predicate Pushdown (Huge Advantage)

Example:

```python
df.filter("age > 30")
```

Parquet metadata contains:

```
RowGroup1: age min=10, max=20
RowGroup2: age min=25, max=60
```

 Spark skips RowGroup1 entirely

This is called:
 **Predicate Pushdown**

---

# 6. Encoding Techniques in Parquet

Parquet uses smart encoding before compression:

### 6.1 Dictionary Encoding

```
name column:
["A", "A", "B", "A"]

Dictionary:
A → 0
B → 1

Stored as:
[0, 0, 1, 0]
```

---

### 6.2 Run Length Encoding (RLE)

```
[25, 25, 25, 25] → (25, count=4)
```

---

### 6.3 Bit Packing

* Uses minimal bits for integers

---

 These reduce size before compression

---

# 7. Compression in Parquet

Common codecs:

* Snappy (default in Spark)
* Gzip
* LZO
* ZSTD

---

### Why compression works well:

* Columnar + encoding → highly compressible

---

# 8. How Spark Uses Parquet

## 8.1 Schema inference

```python
spark.read.parquet("path")
```

 No extra job needed
 Schema is in footer

---

## 8.2 Column pruning

```python
df.select("name")
```

 Only reads required columns

---

## 8.3 Predicate pushdown

```python
df.filter("age > 30")
```

 Uses footer stats → skips data

---

## 8.4 Partition pruning (directory level)

```
/data/year=2025/month=04/
```

 Spark skips entire folders

---

# 9. Why Parquet is Faster than CSV/JSON

| Feature            | CSV/JSON   | Parquet   |
| ------------------ | ---------- | --------- |
| Storage            | Row        | Column    |
| Compression        | Poor       | Excellent |
| Schema             | Not stored | Stored    |
| Column pruning     | No         | Yes       |
| Predicate pushdown | No         | Yes       |
| Read speed         | Slow       | Fast      |

---

# 10. Real Example (Spark Execution)

```python
df = spark.read.parquet("data")

df.filter("age > 30").select("name").show()
```

### What Spark actually does:

1. Reads footer
2. Identifies:

   * Only `name`, `age` needed
3. Applies:

   * Predicate pushdown on `age`
4. Skips unnecessary row groups
5. Reads only required column chunks

---

# 11. Key Interview Points

### 11.1 Why is Parquet columnar?

→ Improves read efficiency for analytics

---

### 11.2 What is Row Group?

→ Horizontal partition enabling parallel reads

---

### 11.3 What is stored in footer?

→ Schema + metadata + statistics

---

### 11.4 Why no inferSchema job?

→ Schema already stored

---

### 11.5 Why is Parquet efficient?

→ Column pruning + predicate pushdown + compression