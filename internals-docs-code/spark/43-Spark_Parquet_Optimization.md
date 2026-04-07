# 1. File Size Optimization (Most Important)

## Problem: Small files

* Too many small Parquet files → too many tasks
* High scheduling overhead
* Poor I/O throughput

## Target

 **128 MB – 1 GB per file** (sweet spot for Spark)

---

## Fix

### Option 1: Repartition before write

```python
df.repartition(200).write.parquet("path")
```

### Option 2: Control file size directly

```python
spark.conf.set("spark.sql.files.maxRecordsPerFile", 5_000_000)
```

---

## Key Insight

* More files ≠ faster
* Balanced file sizes = optimal parallelism

---

# 2. Partitioning Strategy (Critical)

Partitioning = directory-level organization

```id="5z7r2w"
/data/year=2025/month=04/
```

---

## Good Partitioning

```python
df.write.partitionBy("year", "month").parquet("path")
```

### Works well when:

* Column used in filters
* Moderate cardinality

---

## Bad Partitioning

```python
partitionBy("user_id")  # high cardinality
```

Problems:

* Millions of folders
* Metadata explosion
* Slow queries

---

## Rule of Thumb

| Column Type | Use for Partition? |
| ----------- | ------------------ |
| Date        | Yes                |
| Region      | Yes                |
| User ID     | No                 |

---

# 3. Column Pruning Optimization

Always select only needed columns:

```python
df.select("name")
```

Why:

* Parquet reads only required columns
* Reduces I/O significantly

---

# 4. Predicate Pushdown

Write queries like:

```python
df.filter("age > 30")
```

Spark:

* Uses Parquet metadata (min/max)
* Skips entire row groups

---

## Important Tip

Avoid this:

```python
df.filter("cast(age as string) > '30'")
```

 Breaks pushdown

---

# 5. Compression Optimization

## Recommended codecs

| Codec  | Use Case                   |
| ------ | -------------------------- |
| Snappy | Default, fast              |
| Gzip   | Better compression, slower |
| ZSTD   | Best balance               |

---

## Set compression

```python
spark.conf.set("spark.sql.parquet.compression.codec", "zstd")
```

---

# 6. Row Group Size Tuning

Row groups affect:

* Parallelism
* Predicate pushdown efficiency

---

## Default

~128 MB

---

## Tune if needed

```python
spark.conf.set("parquet.block.size", 134217728)  # 128 MB
```

---

## Insight

* Larger row group → better compression
* Smaller → better skipping

---

# 7. Sorting Data Before Writing

Sorting improves:

* Compression
* Predicate pushdown efficiency

---

## Example

```python
df.sort("date").write.parquet("path")
```

Why:

* Values in column become clustered
* Min/max stats become more useful

---

# 8. Avoid Python UDF Before Writing

Bad:

```python
df.withColumn("x", my_udf("col")).write.parquet(...)
```

Why:

* Breaks optimization
* Slower execution

---

Better:

* Use Spark SQL functions

---

# 9. Merge Small Files (Compaction)

If data already exists:

```python
df = spark.read.parquet("path")
df.coalesce(50).write.mode("overwrite").parquet("path")
```

---

## Production approach

* Run periodic **compaction jobs**
* Especially in streaming pipelines

---

# 10. Partition Pruning (Query Side)

Query like:

```python
df.filter("year = 2025")
```

 Spark reads only:

```id="tgnxaz"
/year=2025/
```

---

Avoid:

```python
df.filter("year + 0 = 2025")
```

 Breaks pruning

---

# 11. Schema Optimization

## Use correct data types

Bad:

```python
age as string
```

Good:

```python
age as int
```

Why:

* Better compression
* Faster comparisons

---

# 12. Caching (When Reused)

```python
df.cache()
```

Use when:

* Same data reused multiple times

---

# 13. Advanced: Bucketing (Less common now)

```python
df.write.bucketBy(100, "user_id").saveAsTable("table")
```

Useful for:

* Joins

---

# 14. Real-World Optimization Example

### Bad pipeline

```python
df.write.parquet("path")
```

Problems:

* Small files
* No partitioning
* No compression tuning

---

### Optimized pipeline

```python
df = df.repartition(200)

df.write \
  .partitionBy("year", "month") \
  .option("compression", "zstd") \
  .parquet("path")
```

---

# 15. Key Interview Summary

If asked “How to optimize Parquet?”:

You can answer:

* Control file size (avoid small files)
* Use proper partitioning (low/moderate cardinality)
* Enable predicate pushdown
* Use column pruning
* Choose efficient compression (Snappy/ZSTD)
* Sort data before writing
* Avoid UDFs in pipeline
* Periodically compact files