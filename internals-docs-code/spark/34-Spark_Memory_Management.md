### Spark Memory Management

![image](https://github.com/user-attachments/assets/cc9afbc8-f2a0-45cb-8695-6b205fe70e5f)

If we do ```df.range(100000)``` and then do ```df.collect()``` on 1Gb driver we get OOM error

![image](https://github.com/user-attachments/assets/37dd4f71-e486-49b2-99b5-11c9f091ff7c)

**Spark Architecture**

![image](https://github.com/user-attachments/assets/210188a5-8832-4338-bbf1-2f839e1fe8e7)

Driver memory is of two types:

- spark.driver.memory
- spark.driver.memoryOverhead

![image](https://github.com/user-attachments/assets/26affc9c-885f-46a5-842c-d85ccaca1577)

With collect all records go into the driver.
But with show just one partition gets sent to the heap space.

**🎯 Think of the Spark Driver Like a Worker**

Imagine the Spark driver is a person doing a big task at a desk.

The desk = spark.driver.memory (main memory)

The room around the desk = spark.driver.memoryOverhead (extra space to move, store tools, use side tables)

🧠 Why Just the Desk Isn’t Enough

Let’s say the driver (person) is:

Writing on paper (standard Spark tasks)

Using a laptop (Python/PySpark or native code)

Holding tools and files (temporary data, buffers, network stuff)

Only giving them a desk (spark.driver.memory) isn't enough:

The laptop (native code, Python UDFs) might need space outside the desk

The tools (Spark internals, shuffle, serialization) don’t fit on the desk — they use off-heap memory

If you don’t give them enough room around the desk (memoryOverhead), they might trip over stuff and fail the task.

🧪 Real Spark Example
When you run PySpark like this:

```
df.withColumn("double", my_udf(df["col"]))
```

That Python UDF runs outside the JVM. It needs extra native memory, not regular Java memory.

Spark says:

“I’ll use driver.memory for my JVM, but I need some memoryOverhead for the native stuff.”

✅ Summary (in 1 line)

```
spark.driver.memory is for Spark's own work (Java),
spark.driver.memoryOverhead is for everything outside the JVM — like Python, shuffle, native code.
```

The memory overhead is ```max(384mb,10% of driver memory)```

![image](https://github.com/user-attachments/assets/18f48403-fcc7-4481-8d40-291af5fece66)

Let's say there is ```df1``` and we want to join it with two small tables ```df2``` and ```df3```.

We send both df2 and df3 to the driver.

![image](https://github.com/user-attachments/assets/72a16be0-c634-4ec8-abbe-90bcf8e6e45e)

Let's say we now give 5 dayasets worth 250 mb and the total driver space is 1G.

If rest 750mb is not enough for other processes then the driver will give OOM exception.

**💥 So… How Can GC Cause Out of Memory (OOM)?**

You’d think GC helps prevent OOMs — and it does! But in high-memory-pressure situations, it can actually cause or worsen them.

🚨 Here’s how it happens:
1. Too Many Objects / Too Much Data in Memory
You load huge datasets or perform wide transformations (e.g., groupBy, join).

Spark stores a lot of intermediate data in RAM (JVM heap).

👉 JVM tries to make space by running GC again and again.

2. GC Takes Too Long
If GC runs too often or too long (e.g., > 30s), the JVM thinks something’s wrong.

You get:

```
java.lang.OutOfMemoryError: GC overhead limit exceeded
```

This means:

“GC is using 98% of the CPU but only recovering 2% of memory — I give up.”

3. GC Can’t Free Anything
Some objects (like cached RDDs or references from your code) stay in memory.

GC runs but can't collect them because they're still "referenced".

Eventually, JVM runs out of space and crashes with:

```
java.lang.OutOfMemoryError: Java heap space
⚠️ Common Scenarios in Spark
Cause	Result
Large shuffles / joins	Too many objects in memory
Caching huge RDDs	Heap filled, GC can't recover
Improper partitions	Few tasks → huge memory per task
Memory leaks (bad code)	Uncollectable references
```

Example code

```
from pyspark.sql import SparkSession
from pyspark.storagelevel import StorageLevel
import random

spark = SparkSession.builder \
    .appName("OOM-GC-Demo") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

# Create a large DataFrame with few partitions (causes memory pressure)
data = [(i % 10, random.randint(1, 1000)) for i in range(10_000_000)]  # 10 million rows
df = spark.createDataFrame(data, ["group_id", "value"])

# Force a wide transformation + cache
result = df.groupBy("group_id").count().persist(StorageLevel.MEMORY_ONLY)

# Trigger action
result.count()
```

✅ How to Fix

Increase spark.executor.memory or spark.driver.memory

Use persist(StorageLevel.DISK_ONLY) if RAM is tight

Avoid huge wide transformations without enough partitions

Tune GC (G1GC is often better for large heaps)