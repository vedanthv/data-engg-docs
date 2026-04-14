# RDD in Spark — Summary

## What is RDD?

* **RDD (Resilient Distributed Dataset)** is a distributed data structure in Spark
* Data is split into **partitions across the cluster**
* **Resilient**: can be recomputed using lineage (DAG)
* **Immutable**: every transformation creates a new RDD

---

## Key Features

* Immutable
* Lazy execution
* Fault tolerance via lineage (DAG)
* Distributed across partitions
* Requires explicit control of transformations

---

## Advantages of RDD

* Full control over data processing (“how to do it”)
* Good for **unstructured data**
* Type safety (in Scala — compile-time checks)
* Strong fault tolerance

---

## Disadvantages of RDD

* No optimization (no query planner)
* Slower performance
* More complex and less readable code
* Requires manual handling of logic

---

## DataFrame / Dataset (Contrast)

* Work on **structured/semi-structured data** (CSV, JSON, Parquet)
* Provide automatic optimization via Catalyst Optimizer
* Easier to write and maintain
* Less control, but much better performance

---

## When to Use RDD

* Need **fine-grained control** over execution
* Working with **unstructured data**
* Complex transformations not supported in DataFrame API

---

## Why Not Use RDD (in most cases)

* No optimization → slower
* More complex code
* Poor readability
* DataFrame/Spark SQL usually performs better

---

## Final Takeaway

> **RDD = low-level, flexible, but slow and unoptimized**
> **DataFrame/Spark SQL = high-level, optimized, and preferred in production**
