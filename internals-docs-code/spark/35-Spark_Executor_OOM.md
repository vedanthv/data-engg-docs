### Executor Memory OOM

![image](https://github.com/user-attachments/assets/939e11c4-90c2-4b29-a90c-0aa2d1a23742)

![image](https://github.com/user-attachments/assets/00f1004a-f0b4-4360-b1d1-fcaee996c126)

10 GB per executor and 4 cores

Expanding one executor

![image](https://github.com/user-attachments/assets/ad413e15-62ae-4b57-bb36-852ec1281d9c)

![image](https://github.com/user-attachments/assets/a1612bca-0cc2-4f0e-b876-4e9be2573f65)

Exceeding either 10GB or 1GB leads to OOM

![image](https://github.com/user-attachments/assets/418c7206-0f9e-442a-a918-4b82fc9c77a1)

#### How is 10GB divided?

![image](https://github.com/user-attachments/assets/e5a594f8-de1f-44a7-b09e-90c8c3f3db43)

#### What does each part of the user memory do?

1. Reserved Memory

Minimum 450mb must be our memory of executor.

![image](https://github.com/user-attachments/assets/66c06198-0763-41ea-b1e2-a24ffb0a8785)

2. User Memory 

![image](https://github.com/user-attachments/assets/46939ef5-5ea5-4036-8659-a7c05fb333f1)

3. Storage Memory Usage

![image](https://github.com/user-attachments/assets/fcb5e939-6743-483a-8fb1-a149ba15cab4)

4. Executor Memory Usage

![image](https://github.com/user-attachments/assets/eda22dc1-4827-46e1-a9de-37f1b5209cc2)

#### What does each part of the spark memory do?

![image](https://github.com/user-attachments/assets/ea6417e3-f87b-4d2f-b418-c3564f0f1f39)

⚙️ Background: Memory in Spark Executors

Each executor in Spark has a limited memory budget. This memory is split for:

- Execution Memory: used for joins, aggregations, shuffles

- Storage Memory: used for caching RDDs or DataFrames

- User Memory: everything else (broadcast vars, UDFs, JVM overhead)

🔄 1. Static Memory Manager (Old)

This was Spark's memory model before Spark 1.6.

🔧 How It Works:

- Fixed memory boundaries set in config.
- You manually allocate how much memory goes to:
- Storage (RDD cache)
- Execution (shuffles, joins)
- If storage fills up → cached blocks are evicted.
- No sharing between execution and storage.

Example fractions

```
spark.storage.memoryFraction = 0.6
spark.shuffle.memoryFraction = 0.2
```

🔄 2. Unified Memory Manager (Modern - Default)

Introduced in Spark 1.6+ and is default since Spark 2.0.

🔧 How It Works:

Combines execution + storage into a single unified memory pool.

Dynamic memory sharing: if execution needs more, storage can give up memory — and vice versa.

Much more flexible and efficient.

✅ Benefits:

- Less tuning needed
- Avoids wasted memory in one region while another needs more
- Better stability under pressure

**In bwlo case execution memory is empty so storage mmemory uses more of execution memory for caching**

![image](https://github.com/user-attachments/assets/c7619c3d-8095-4688-836f-22c76ba4c002)

Now executor does some work in blue boxes

![image](https://github.com/user-attachments/assets/923ba744-4f13-487e-a00b-0b472cedf1db)

Now entire memory is full, so we need to evict some data that has been cached. This happens in LRU fashion.

![image](https://github.com/user-attachments/assets/428545ed-0166-4206-a07c-5d515b35d4ef)

Now let's say executor has entire memory used 2.9 something gb... but it needs more memory.

![image](https://github.com/user-attachments/assets/fedc16a6-778f-41ed-9faa-4c907d03a9fb)

If the storage pool memory is free it can utilize that.

![image](https://github.com/user-attachments/assets/f49ddce2-99e4-4d7a-9835-a2239bb375a0)

If the storage pool is also full, then we get OOM!!!

#### When can we neither evict the data nor spill to disk?

Suppose we have two dataframes df1 and df2 and the key id = 1 is heavily skewed in both dataframes, and its 3GB

Since we need to get all the data from df1 and df2 with id = 1 onto the same executor to perform the join, we have just 2.9GB but the data is 3gb so it gives OOM.

![image](https://github.com/user-attachments/assets/d47407f0-ef69-4bd0-b212-4b892691d351)

![image](https://github.com/user-attachments/assets/b97b7abf-4acf-451c-8cc6-263dc620a747)

We can handle 3-4 cores per executor beyond that we get memory executor error.

**❓ When can Spark neither evict nor spill data from executor memory?**

This happens when both eviction and spilling are not possible, and it leads to:

💥 OutOfMemoryError in executors.

✅ These are the main scenarios:

**🧱 1. Execution Memory Pressure with No Spill Support**

Execution memory is used for:

- Joins (SortMergeJoin, HashJoin)
- Aggregations (groupByKey, reduceByKey)
- Sorts

Some operations (like hash-based aggregations) need a lot of memory, and not all are spillable.

🔥 Example:

```
df.groupBy("user_id").agg(collect_set("event"))
```
If collect_set() builds a huge in-memory structure (e.g., millions of unique events per user)

And that structure can’t be spilled to disk

And execution memory is full

👉 Spark can’t evict (no caching), and can’t spill (not supported for this op)
→ 💣 OOM

**🔁 2. Execution Takes Priority, So Storage Can't Evict Enough**

In Unified Memory Manager, execution gets priority over storage.

But sometimes, even after evicting all cache, execution still doesn’t get enough memory.

🔥 Example:
- You cached a large DataFrame.
- Then you do a massive join.

Spark evicts all cached data, but still can't free enough memory.

👉 No more memory to give → 💥

**User Code holding References**

🍕 Imagine Spark is a Pizza Party
Spark is throwing a pizza party. You and your friends (the executors) are each given a plate (memory) to hold some pizza slices (data).

The rule is:

“Eat your slice, then give your plate back so someone else can use it.”

😬 But You Keep Holding Your Plate
You finish your slice, but instead of giving the plate back, you say:

“Hmm… I might want to lick the plate later,”
so you hold on to it.

And you keep doing this with every plate 🍽️.

Now, you have 10 plates stacked up, all empty, but you're still holding them.

🍕 But There’s a Problem…
Spark wants to serve more pizza (more data), but now there are no plates left.
Even though you’re not using yours, Spark can’t take them back, because you’re still holding on.

💥 Result?
Spark gets frustrated and says:

“I’m out of plates! I can’t serve any more pizza!”

That’s when Spark crashes with a memory error (OOM) — because it can’t clean up the memory you're holding onto.

✅ What Should You Do?
Let go of the plates as soon as you're done eating (i.e., don’t store data in variables or lists forever).

That way, Spark can reuse memory and everyone gets more pizza. 🍕

```
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HoldingReferencesOOM") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

# Create a large DataFrame
df = spark.range(1_000_000)  # 1 million rows

# ❌ BAD: Holding all rows in a Python list
all_data = df.collect()  # Loads entire DataFrame into driver memory

# Still holding reference to a big object
# Spark can't clean this up because Python is holding it

# Do more operations
df2 = df.selectExpr("id * 2 as double_id")
df2.show()
```

Spark wants to free memory, but it can’t, because your code is still holding a reference to the list ```all_list``` is still a reference and even though we may not use it later Java GC doesnt know that. its like we finish playing with a teddy bear but still hold onto it, the teacher thinks we are still playing with it, so they cant take it back.

```
df = spark.range(1_000_000)

# ✅ Process data without collecting everything into memory
df.filter("id % 2 == 0").show(10)  # only shows first 10 rows
```
