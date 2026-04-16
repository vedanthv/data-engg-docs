## Spark DAG Stage Task Example

```python
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[5]") \
    .appName("testing") \
    .getOrCreate()
employee_df = spark.read.format("csv") \
    .option("header", "true") \
    .load("C:\\Users\\nikita\\Documents\\data_engineering.csv”)
print(employee_df.rdd.getNumPartitions())
employee_df = employee_df.repartition(2)
print(employee_df.rdd.getNumPartitions())
employee_df = employee_df.filter(col("salary") > 90000) \
    .select("id", "name", "age", "salary") \
    .groupby("age").count()
employee_df.collect()
input("Press enter to terminate")
```

* **Read CSV**

  * Partitions based on file splits (e.g., 4, 8, etc.)

* **repartition(2)**

  * Causes a **shuffle**
  * Output = exactly **2 partitions**

* **filter + select**

  * **Narrow transformations**
  * No data movement
  * Run with **2 tasks (1 per partition)**

* **groupBy("age").count()**

  * **Wide transformation → shuffle**
  * Data redistributed into **200 partitions (default)**
  * Runs with **200 tasks**
  * Some partitions may be **empty**

* **collect()**

  * Action → results sent to driver

---

## Core Concepts

### 1. Partition vs Task

* **Partition = data chunk**
* **Task = computation on that partition**
* **1 partition → 1 task**

---

### 2. Narrow vs Wide Transformations

* **Narrow (filter, select)**

  * No shuffle
  * Operate within same partition

* **Wide (repartition, groupBy)**

  * Require shuffle
  * Break stages

---

### 3. Stage Formation

* Each **shuffle creates a new stage**

So your job has:

* Stage 1 → repartition
* Stage 2 → filter + select
* Stage 3 → groupBy
* Stage 4 → collect

---

### 4. Partition Behavior

* After `repartition(2)` → **2 partitions**
* After `groupBy` → **200 partitions (default)**
* Previous partition count does **not matter after shuffle**

---

## Key Insight

You go from:

```text
2 partitions → 2 tasks  
        ↓
groupBy shuffle  
        ↓
200 partitions → 200 tasks
```

---

## Performance Takeaway

* You introduced **2 shuffles** (repartition + groupBy)
* This adds overhead and is often unnecessary
* Default 200 partitions can lead to many small or empty tasks