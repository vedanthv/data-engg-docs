## Lakeflow Declarative Pipelines Introduction

Here’s a clear introduction to **Lakeflow declarative pipelines** in Databricks:

---

### **1. What is Lakeflow?**

**Lakeflow** is a **declarative pipeline framework** by Databricks designed to simplify building and managing data pipelines over Delta Lake. Unlike traditional ETL pipelines where you imperatively write every transformation step, Lakeflow allows you to **declare the desired end state of your data** and lets Databricks handle the execution, orchestration, and dependency management.

Think of it like **“telling Databricks what you want, not how to do it”**.

---

### **2. Key Concepts**

| Concept                    | Description                                                                               |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| **Pipeline**               | A logical collection of transformations (like ETL jobs) defined declaratively.            |
| **Lakeflow Table**         | A Delta table managed by Lakeflow, which tracks lineage, schema, and dependencies.        |
| **Declarative Config**     | JSON/YAML-like specification describing sources, transformations, and targets.            |
| **State Management**       | Lakeflow keeps track of which data has been processed and ensures **idempotent updates**. |
| **Incremental Processing** | Automatically detects new/changed data and applies transformations incrementally.         |

---

### **3. How It Differs from Normal Pipelines**

| Feature               | Traditional ETL               | Lakeflow Declarative Pipeline                         |
| --------------------- | ----------------------------- | ----------------------------------------------------- |
| **Definition**        | Imperative: step-by-step code | Declarative: specify inputs, outputs, transformations |
| **Orchestration**     | Manual or Airflow/Scheduler   | Built-in, dependency-aware orchestration              |
| **Data Lineage**      | Requires extra tooling        | Automatic tracking of lineage between tables          |
| **Error Handling**    | Manual retries                | Automatic state management & retries                  |
| **Incremental Loads** | Developer writes logic        | Lakeflow detects changes & processes incrementally    |

---

### **4. Basic Pipeline Flow**

1. **Define sources**: Raw Delta tables, cloud storage, or external systems.
2. **Declare transformations**: For example, aggregations, joins, or enrichments.
3. **Specify targets**: Delta tables managed by Lakeflow.
4. **Run pipeline**: Databricks ensures only necessary transformations run, handles dependencies, and maintains consistency.

---

### **5. Advantages**

* **Less boilerplate code** → focus on business logic, not orchestration.
* **Automatic incremental updates** → avoids reprocessing all data.
* **Built-in lineage and auditing** → helps with compliance and debugging.
* **Easier pipeline management** → declarative config files version-controlled like code.

---

### **6. Example (Conceptual)**

```yaml
# Sample declarative pipeline config
pipeline_name: sales_pipeline
tables:
  - name: raw_sales
    source: s3://data/raw_sales
  - name: sales_summary
    depends_on: raw_sales
    transformations:
      - type: aggregate
        group_by: ["region", "category"]
        metrics:
          - name: total_sales
            operation: sum(amount)
```

Here, you **declare** the desired summary table, and Lakeflow automatically handles reading `raw_sales`, performing aggregation, and writing `sales_summary` incrementally.

Here’s a detailed breakdown of **Streaming Tables, Materialized Views, and Normal Views in Databricks DLT (Delta Live Tables)** and their typical usage:

---

## **1. Streaming Tables (aka Live Tables)**

**Definition:**
A **streaming table** in DLT is a Delta table that is continuously updated as new data arrives. It’s typically used for **real-time pipelines**.

**Key Characteristics:**

| Feature              | Description                                                           |
| -------------------- | --------------------------------------------------------------------- |
| **Data Ingestion**   | Continuous from streaming sources (Kafka, Event Hubs, cloud storage). |
| **Storage**          | Delta table on Databricks (supports ACID).                            |
| **Processing Mode**  | `Append` or `Upsert` (via `MERGE`).                                   |
| **Latency**          | Near real-time; updates as soon as micro-batches are processed.       |
| **Schema Evolution** | Supported, can evolve automatically or manually.                      |

**Use Case:**

* Real-time dashboards (e.g., sales, stock prices, payments).
* Event-driven pipelines (e.g., fraud detection, monitoring trades).

**Example in DLT (Python):**

```python
import dlt
from pyspark.sql.functions import *

@dlt.table
def streaming_sales():
    return (
        spark.readStream.format("cloudFiles")
             .option("cloudFiles.format", "json")
             .load("/mnt/sales/json")
             .withColumn("processed_time", current_timestamp())
    )
```

---

## **2. Materialized Views**

**Definition:**
A **materialized view** is a Delta table that stores the **precomputed results** of a query. In DLT, it is a table whose content is automatically refreshed based on its dependencies.

**Key Characteristics:**

| Feature          | Description                                               |
| ---------------- | --------------------------------------------------------- |
| **Data Storage** | Delta table with physical storage (unlike normal views).  |
| **Refresh**      | Incremental refresh based on upstream table changes.      |
| **Performance**  | Faster query since data is precomputed.                   |
| **Up-to-date**   | Always consistent with underlying tables (incrementally). |

**Use Case:**

* Aggregations (e.g., daily sales per region).
* Joins and transformations that are expensive to compute on demand.
* Serving layer for dashboards or ML pipelines.

**Example in DLT (Python):**

```python
import dlt
from pyspark.sql.functions import sum

@dlt.table
def sales_summary():
    sales = dlt.read("LIVE.streaming_sales")
    return sales.groupBy("region").agg(sum("amount").alias("total_sales"))
```

> Here `sales_summary` is materialized: it stores the aggregated totals physically and refreshes as new streaming data arrives.

---

## **3. Normal Views**

**Definition:**
A **normal view** in DLT is like a **virtual table**: it does **not store data physically**. Instead, it executes the underlying query each time you read it.

**Key Characteristics:**

| Feature                    | Description                                               |
| -------------------------- | --------------------------------------------------------- |
| **Data Storage**           | None; only query definition stored.                       |
| **Performance**            | Slower for large or complex queries (computed on-demand). |
| **Up-to-date**             | Always reflects the latest upstream data.                 |
| **Incremental Processing** | Not directly supported (since it’s virtual).              |

**Use Case:**

* Lightweight transformations that do not need storage.
* Ad-hoc analytics.
* Debugging or temporary transformations in pipelines.

**Example in DLT (Python):**

```python
import dlt

@dlt.view
def high_value_sales():
    sales = dlt.read("LIVE.streaming_sales")
    return sales.filter(sales.amount > 10000)
```

> `high_value_sales` is a **normal view**: it does not store any data and computes results on demand.

---

## **4. Quick Comparison**

| Feature         | Streaming Table     | Materialized View        | Normal View                                  |
| --------------- | ------------------- | ------------------------ | -------------------------------------------- |
| **Storage**     | Delta (persistent)  | Delta (precomputed)      | None                                         |
| **Latency**     | Near real-time      | Incrementally refreshed  | On-demand                                    |
| **Performance** | High for reads      | High (precomputed)       | Low for complex queries                      |
| **Use Case**    | Real-time ingestion | Aggregations, dashboards | Lightweight transformations, ad-hoc analysis |

---

✅ **Summary / Guidance:**

* **Use streaming tables** for continuous ingestion from sources.
* **Use materialized views** when you want precomputed results for fast reads and dashboards.
* **Use normal views** for on-the-fly filtering or temporary logical tables.

---
