## PySpark Internals for Large Scale Data Processing

### Internal Working and Architecture of Spark

#### High Level Overview 
![image](https://github.com/vedanthv/data-engg/assets/44313631/fc63ecce-41ce-477b-8964-86a4a4b86d20)

### Flow of the Logic
![image](https://github.com/vedanthv/data-engg/assets/44313631/a0091ce1-edaf-4dce-9754-caf5238f8506)

### Worker Node Architecture
![image](https://github.com/vedanthv/data-engg/assets/44313631/ea6e5e52-7b70-4550-8fef-8858691bbbd2)
- There are total of 64 cores, so 64 processes can execute parallelly and each executor will have 16 processes running.
- There can be partitions within each executor that can remain idle without any process running so we need to define a parameter to define how many min number of processes need to be run on each executor at once.
- To avoid having idle nodes we need to keep the number of partitions as a multiple of the core processor.

### Summary of Spark Application
![image](https://github.com/vedanthv/data-engg/assets/44313631/84d10017-7a63-49cc-97d6-0c9761d7ae47)

### Attributes of Spark
- Its Scalable.
- Its Fault Tolerant and follows lazy evaluation. First Spark makes logical plans to process the data, then it builds a DAG and hence if one worker node goes down we can still recover the data.
- Spark supports multiple programming languages like Python and Scala.
- Spark can handle streaming data also.
- Spark is known for its speed due to in memory computation model.
- Spark has rich libraries for ML and Data Processsing.

### Common Terminologies
![image](https://github.com/vedanthv/data-engg/assets/44313631/f3d39071-82b2-4d95-8bf0-69c5da259f36)

![image](https://github.com/vedanthv/data-engg/assets/44313631/de3e02ff-2580-433f-8183-935ac4b2feda)

Spark does not immediately process the data as mentioned above. When an action is called by the developer for storage or transformation purposes, it processes the data according to the DAG and return the output to the user.

![image](https://github.com/vedanthv/data-engg/assets/44313631/93110364-1dc5-443c-b6ad-9d89edcf7b46)

To store data in on heap memory we need to serialize the data.

### Stages and Tasks 
![image](https://github.com/vedanthv/data-engg/assets/44313631/0c913da4-73d2-4bf2-b844-05a6a38b2797)

### Libraries Suppoprted by Spark
- SQL
- Streaming
- MLLib
- SparkX

### Driver Node Architecture
![image](https://github.com/vedanthv/data-engg/assets/44313631/b1d68634-96f0-4354-9fb6-43c4c28f4265)

### Worker Node Architecture
![image](https://github.com/vedanthv/data-engg/assets/44313631/7ebf4dee-073a-46c3-8c8d-01f6f0ec30b1)

### On Heap Memory Architecture
![image](https://github.com/vedanthv/data-engg/assets/44313631/28abf5f6-c5f2-4a54-8094-5265a4f7fab9)

- Out of 32gb, around 300mb is used by spark for disaster recovery and cannot be used by the user or the processes.
- Of the remaining (32gb - 300mb) we allocate 40% of the heap memory as the user memory and then 60% of the heap memory as the unified memory.
- In unified memory 50% is used for scheduling and 50% of the memory is used for executing.

### API Architecture in Spark

![image](https://github.com/vedanthv/data-engg/assets/44313631/8624a26b-2757-44cf-8dfe-c62ad0bc3f40)

Dataset = Best of RDD + Best Of DataFrame
![image](https://github.com/vedanthv/data-engg/assets/44313631/03ca4c37-ea52-4a32-83ed-29c860ff0b7a)

- RDDs were always stored on the on heap memory but dataframes can be stored on the off heap memory also.

- All types of datasets here are immutable.

![image](https://github.com/vedanthv/data-engg/assets/44313631/81820aea-4e35-4844-b2dc-57d94bcf742d)

- Strong Typed feature ensures certain things like mismatch in the datatypes is detected in compile time.

### Transformations and Actions

![image](https://github.com/vedanthv/data-engg/assets/44313631/dd340e15-a52a-4bc1-8d74-cee5a2e33aad)

![image](https://github.com/vedanthv/data-engg/assets/44313631/9c0eaada-5429-481b-a639-2903571ff9a2)

### Lazy Evaluation and DAG Logic Flow

![image](https://github.com/vedanthv/data-engg/assets/44313631/83769424-47af-45a5-b47d-f4c1acf3aaa6)

### Narrow Transformation

Each and every executor can work independently on the data and don't require any dependency from the others.

![image](https://github.com/vedanthv/data-engg/assets/44313631/caddbaaf-39be-4907-9722-abc1dc609a14)

### Wide Transformation

This type of transformation involves the shuffling of data.

![image](https://github.com/vedanthv/data-engg/assets/44313631/0540bea6-e3b3-4f95-b111-9b035682af43)

```df.collect``` is used to perform action after various transformations have been applied to the data.

### On heap vs Off Heap Memory

**On Heap Memory Architecture**

Each and every executor has its own On Heap Memory
![image](https://github.com/vedanthv/data-engg/assets/44313631/36dfd2f0-bd1d-44e3-9c0d-2dc98ac14292)

**Off Heap Memory Architecture**

![image](https://github.com/vedanthv/data-engg/assets/44313631/94e2ed45-54e8-4cb1-9e26-053b9a8b77e0)

The Off Heap Memory is managed by the OS and shared by all the executors when the on heap memory runs out of space.

The performance can be hit when we use the On Heap Memory because in the middle of any process if the on heap memory is full, then the Garbage Colector has to scan theentire memory to check and remove the unwanted memory space and then resume the process again.

![image](https://github.com/vedanthv/data-engg/assets/44313631/b1c493c3-6071-4442-9133-50a799b29374)

### Clusters in PySpark

![image](https://github.com/vedanthv/data-engg/assets/44313631/0b23a605-1585-4cf2-83b0-117a41a45897)

- If multiple users are using All Purpose Clusters the resources are shared between them.

- It is used in notebooks where we have to check the output of every command after executing it.

- Job Clusters are used for schedulle jobs and the clusters are created duing runtime.

- Pools are used to create and combine multiple clusters where we can command how many clusters must be active all the time. So there is no bootup time and is used for cost cutting.

### Cluster Modes

![image](https://github.com/vedanthv/data-engg/assets/44313631/71d9774b-367c-48e3-bf67-b89f3693dafd)

### Spark Architecture Diagram

![image](https://github.com/vedanthv/data-engg/assets/44313631/3186a6a2-5521-481a-9de1-1853087a9031)

## Apache Spark Internals

![](https://snipboard.io/0KCWc4.jpg)

![](https://snipboard.io/SFokjG.jpg)

### How does Spark Execute Queries?

![](https://snipboard.io/RL7lNh.jpg)

### Spark Cluster Execution

![](https://snipboard.io/t3F1mQ.jpg)

- Executor is a JVM virtual machine that runs on the workers.
- The 625mb file is divided into memory partitions and then sent to the workers for execution.
- Its an automatic parallelism process.

### Hive Metastore

![](https://snipboard.io/bSnPkw.jpg)

### Parquet File Format

![](https://snipboard.io/dmtEkC.jpg)

- We prefer the parquet format because consider a dataset with 100 columns in it and we want to only fetch data of first three columns. We can use parquet format to do it faster compared to csv.

- Search for files with java in it with Linux
```%sh ps grep 'java'```

- How to read markdown files use bash
```%fs head /databricks-dataset/README.md```

- Display all mount points
```%fs mounts```

- Declare a python variable in the spark context which SQL commands can access.
```spark.sql(f"SET c.events_path = {events_path}")```

- Creating a table form the files and load it as a table
```sql
CREATE TABLE IF NOT EXISTS 
events
USING DELTA OPTIONS
{path "${c.events_path}"}
```
- Add notebook params as widgets

```SQL
CREATE WIDGET TEXT state default "KA"
```
```SQL
SELECT * FROM events WHERE state = getArgument("state")
```

### What is there in Spark SQL?

![](https://snipboard.io/QgEmFf.jpg)

### Lazy Evaluation

![](https://snipboard.io/wYCutU.jpg)

![](https://snipboard.io/saCl2z.jpg)

![](https://snipboard.io/i5CwNx.jpg)

### Explicit vs Implicit vs Infer Schema

![](https://snipboard.io/EgsMPk.jpg)

Fastest one is explicit since we don't need to read the data files.

![](https://snipboard.io/ZAEJHc.jpg)

### Query Execution Process

![](![query execution engine](https://files.training.databricks.com/images/aspwd/spark_sql_query_execution_engine.png)

### DataFrame Action 

![](https://snipboard.io/lA3W5s.jpg)

- anything we specify as options are actions.

### Inferring JSON Schema

```python
from pyspark.sql.types import ArrayType, DoubleType, IntegerType, LongType, StringType, StructType, StructField

  

user_defined_schema = StructType([

StructField("device", StringType(), True),

StructField("ecommerce", StructType([

StructField("purchaseRevenue", DoubleType(), True),

StructField("total_item_quantity", LongType(), True),

StructField("unique_items", LongType(), True)

]), True),

StructField("event_name", StringType(), True),

StructField("event_previous_timestamp", LongType(), True),

StructField("event_timestamp", LongType(), True),

StructField("geo", StructType([

StructField("city", StringType(), True),

StructField("state", StringType(), True)

]), True),

StructField("items", ArrayType(

StructType([

StructField("coupon", StringType(), True),

StructField("item_id", StringType(), True),

StructField("item_name", StringType(), True),

StructField("item_revenue_in_usd", DoubleType(), True),

StructField("price_in_usd", DoubleType(), True),

StructField("quantity", LongType(), True)

])

), True),

StructField("traffic_source", StringType(), True),

StructField("user_first_touch_timestamp", LongType(), True),

StructField("user_id", StringType(), True)

])

  

events_df = (spark

.read

.schema(user_defined_schema)

.json(events_json_path)

)
```

There are no jobs that are spanned while running the above code since we give all the data to infer that spark needs.

### Write Dataframes to tables

```python
events_df.write.mode("overwrite").saveAsTable("events")
```

### Reading Complex JSON and performing operations

```python
rev_df = (events_df

.filter(col("ecommerce.purchase_revenue_in_usd").isNotNull())
.withColumn("purchase_revenue", (col("ecommerce.purchase_revenue_in_usd") * 100).cast("int"))
.withColumn("avg_purchase_revenue", col("ecommerce.purchase_revenue_in_usd") / col("ecommerce.total_item_quantity"))

.sort(col("avg_purchase_revenue").desc())

)
display(rev_df)
```

![](https://snipboard.io/gkP7WZ.jpg)

### ```selectExpr()```

```sql
apple_df = events_df.selectExpr("user_id", "device in ('macOS', 'iOS') as apple_user")

display(apple_df)
```
![](https://snipboard.io/LXeRz0.jpg)

### Drop multiple columns

```sql
anonymous_df = events_df.drop("user_id", "geo", "device")
display(anonymous_df)
```
### Create New Columns

```sql
mobile_df = events_df.withColumn("mobile", col("device").isin("iOS", "Android"))
display(mobile_df)
```
### ```filter()``` to subset rows

```python
purchases_df = events_df.filter("ecommerce.total_item_quantity > 0")
display(purchases_df)	
```

```python
revenue_df = events_df.filter(col("ecommerce.purchase_revenue_in_usd").isNotNull())
display(revenue_df)
```

### ```sort``` vs ```order_by```

```sort``` will run on individual memory partitions and ```order_by``` will sort all the memory partitions together.

```python
revenue_df = events_df.filter(col("ecommerce.purchase_revenue_in_usd").isNotNull())
display(revenue_df)
```

```python
decrease_sessions_df = events_df.sort(col("user_first_touch_timestamp").desc(), col("event_timestamp"))
display(decrease_sessions_df)
```

### Aggregations

![](https://snipboard.io/6WrK7H.jpg)

### Group By Operations

```sql
df.groupBy("geo.state", "geo.city")
```

### How Group By Works?

![](https://files.training.databricks.com/images/aspwd/aggregation_groupby.png)

### Group Data Methods

![](https://snipboard.io/GeSnNc.jpg)

Average Purchase Revenue for each state

```sql
avg_state_purchases_df = df.groupBy("geo.state").avg("ecommerce.purchase_revenue_in_usd")
display(avg_state_purchases_df)
```
![](https://snipboard.io/0YE3h7.jpg)

Total Quantity and sum of purchase revenue and quantity for each combo of city and state

```sql
city_purchase_quantities_df = df.groupBy("geo.state", "geo.city").sum("ecommerce.total_item_quantity", "ecommerce.purchase_revenue_in_usd")
display(city_purchase_quantities_df)
```
![](https://snipboard.io/7pyXY3.jpg)

### List of Aggregation Functions

![](https://snipboard.io/Pzv9sI.jpg)

**Multiple Aggregate Functions**

```python
from pyspark.sql.functions import avg, approx_count_distinct
state_aggregates_df = (df
.groupBy("geo.state")
.agg(avg("ecommerce.total_item_quantity").alias("avg_quantity"),
approx_count_distinct("user_id").alias("distinct_users"))

)
display(state_aggregates_df)
```

### Unix Timestamps

![](https://snipboard.io/FpCJtM.jpg)

#### Datetime Functions 

Refer this [docs](https://www.databricks.com/blog/2020/07/22/a-comprehensive-look-at-dates-and-timestamps-in-apache-spark-3-0.html)

![](https://snipboard.io/Evl8Df.jpg)

**Add and Subtract Dates**

```sql
plus_2_df = timestamp_df.withColumn("plus_two_days", date_add(col("timestamp"), 2))
```

**String Built In Functions**

![](https://snipboard.io/pPeEyK.jpg)

![](https://snipboard.io/LXB2UF.jpg)

**Complex Data types**

![](https://snipboard.io/idbtZH.jpg)

**Review**

![](https://snipboard.io/3hfWuT.jpg)

#### Collection Functions

![](https://snipboard.io/iSJX8t.jpg)

```array_contains```

![](https://snipboard.io/IpGYTc.jpg)

```exlpode()```

![](https://snipboard.io/IhvlpO.jpg)

```element_at```

![](https://snipboard.io/KA0o7s.jpg)

```collect_set```

![](https://snipboard.io/rCvKbf.jpg)

Split to extract email address

```sql
display(df.select(split(df.email, '@', 0).alias('email_handle')))
```

#### Collection Functions Review

![](https://snipboard.io/dDvPzO.jpg)

Create a column for the size of mattress

```sql
mattress_df = (details_df
.filter(array_contains(col("details"), "Mattress"))
.withColumn("size", element_at(col("details"), 2)))
display(mattress_df)
```
![](https://snipboard.io/m5DHjX.jpg)

For each email, check what mattress type they purchased.

```sql
size_df = mattress_df.groupBy("email").agg(collect_set("size").alias("size options"))
display(size_df)
```
![](https://snipboard.io/pYMh9u.jpg)

#### Miscellaneous Functions

![](https://snipboard.io/bumgyI.jpg)

**Joins Demo**

![](https://snipboard.io/DukP6S.jpg)

**Handling Null Values**

![](https://snipboard.io/XhNu1S.jpg)

### How UDFs run in Scala and Python?

![](https://snipboard.io/MmIw1E.jpg)

- In case of Scala UDFs, it lies inside the executor so there is no inter process communication is required.
- But in case of Python UDF, we will have a driver program and an executor but the Python UDFs run outside the Executor.
- This means that the Spark DataFrame rows are deserialized, sent row by row to the python UDF that transforms it, serializes it row by row and sends it back to the executors.
- The UDFs are registered on Python Interpreters.

![](https://snipboard.io/GC5sfe.jpg)

#### Transform function execution

![](https://snipboard.io/N9KdTv.jpg)

- The custom UDF that was written took twice as long to execute due to the extra work involved. 
- The problem with UDFs is that if we write it in Python, there is extra overhead of converting it to Java bytecode and providing it to the executor.

#### How to register UDFs?

![](https://snipboard.io/i2W5lJ.jpg)

![](https://snipboard.io/DLviFg.jpg)

![](https://snipboard.io/EAw5Sl.jpg)

#### Python vs Pandas UDF

![](https://snipboard.io/rm9D6E.jpg)

#### SQL UDF

![](https://snipboard.io/3x6NvT.jpg)

### Apache Spark Architecture

![](https://snipboard.io/SE9xBF.jpg)

### Cluster Architecture

![](https://snipboard.io/ZV673F.jpg)

- Each worker will have only one executor

![](https://snipboard.io/4bl6h3.jpg)

There is one task for each memory partition.

![](https://snipboard.io/4KXOvo.jpg)

#### Driver's work 

![](https://snipboard.io/XvBOuq.jpg)

![](https://snipboard.io/AK8rFJ.jpg)

![](https://snipboard.io/D6i7ul.jpg)

![](https://snipboard.io/tYDE2C.jpg)

![](https://snipboard.io/6YaWFz.jpg)

The rest of the memory partitions do not have any cores to execute on and wait in the queue.

![](https://snipboard.io/lXwj34.jpg)

A,E,H and J have finished working. They are idle so worker node assigns the memory partitions 13,14,15 and 16 to them.

![](https://snipboard.io/nLl1s3.jpg)

Once all of them complete the work, the driver sends the answer set to the client.

![](https://snipboard.io/N1rqhp.jpg)

- The intermediate result sets mentioned as shuffle write and shuffle read are then sent to the worker node hard drives.

![](https://snipboard.io/JG2zWe.jpg)

#### Deep Dive Into Shuffle

![](https://snipboard.io/7KlhLM.jpg)

- The memory used went from 20mb to 560 bytes because we are only storing the key value pairs and not the entire data. The key value pairs indicate the color and the number of rows that they are part of. The data is written to the disk under shuffle write.

- In stage 2 we build shuffle partition with Green, Red and Yellow rows.

![](https://snipboard.io/sAFqK0.jpg)

![](https://snipboard.io/p1JsP2.jpg)

![](https://snipboard.io/akHOIW.jpg)

![](https://snipboard.io/R6sXt8.jpg)

![](https://snipboard.io/ufO1Gd.jpg)

#### Summary

![](https://snipboard.io/PYzwXI.jpg)

### Query Optimization

![](https://snipboard.io/AHCm8q.jpg)

- RDD is resilient distributed dataset that is just an array of data.

#### Example

![](https://snipboard.io/4dINXp.jpg)

#### Example 2

![](https://snipboard.io/cC73YN.jpg)

#### Adaptive Query Optimization

![](https://snipboard.io/z9T0Ok.jpg)

#### Shuffle Partitions : With and Without AQE

![](https://snipboard.io/rVH0Ls.jpg)

![](https://snipboard.io/XBdqHy.jpg)

#### Predicate Pushdown

![](https://snipboard.io/Ovah36.jpg)

- In this case, less RAM is used so query is faster.

![](https://snipboard.io/P84qKc.jpg)

- If we don't remove things from cache that is not needed, when there is only one core in the executor and a query is called in, then it will be given precedence and the cache will be evicted.

#### Memory Partitioning Guidelines

![](https://snipboard.io/hRP6b0.jpg)

![](https://snipboard.io/BuAK5W.jpg)

In the below example we have 8 memory partitions and 200 shuffle partitions.

![](https://snipboard.io/FnydDf.jpg)

Check the number of cores in the cluster

![](https://snipboard.io/7kLTAj.jpg)

Check the number of memory partitions

![](https://snipboard.io/er4WDd.jpg)

Repartitioning Dataset

![](https://snipboard.io/ychkz1.jpg)

Repartitioning is always a wide transformation.

### AQE and Shuffle Partitions

![](https://files.training.databricks.com/images/aspwd/partitioning_aqe.png)

We can set the ```spark.sql.shuffle.partitions``` based on the largest dataset that our application can process.