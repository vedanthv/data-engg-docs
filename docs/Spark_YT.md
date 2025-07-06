## Spark Concepts and Code.

### Lecture 1 : What is Apache Spark

![image](https://github.com/user-attachments/assets/ed862eae-aed7-4bd7-acfe-46fa117402bb)

#### Unified : 
![image](https://github.com/user-attachments/assets/8c33e885-bae7-4db0-983c-e84f1e5e0bfe)

#### Computing Engine:
![image](https://github.com/user-attachments/assets/5d93b97e-c545-4885-8b7a-88b31d048197)

Spark is not storage platform we can store the data in hdfs, rdbms etc...

Spark can process terabytes of data in distributed manner.

#### Compute Cluster:
![image](https://github.com/user-attachments/assets/1505275d-c247-435e-9db0-d1cfbb3cd9e9)

- each slave has 16 GB RAM, 1TB storage and 4 core CPU
- even master has some data and RAM
- the above cluster can compute 64 gb of data at a time.
- the master divides the data among the slave nodes and then slaves process the data.

### Lecture 2 : Why Apache Spark?

Different Databases
![image](https://github.com/user-attachments/assets/9a0002db-8eae-46be-8a54-97836d7f17ae)

new formats like video, audio, json,avro started coming in but rdms cannot handle it.

volume of data also increased. 

#### What is Big Data?
![image](https://github.com/user-attachments/assets/392ce5ec-a93a-4f9d-afc8-2fec1ed9d920)

Data Lake works on Extract Load Transform architecture

#### Issues with RDBMS

- Storage
- Processing - RAM and CPU

Enter Spark...

![image](https://github.com/user-attachments/assets/0af03559-6cae-45e9-9d6c-322bfe032efd)

#### Monolith vs Microservice Architecture
![image](https://github.com/user-attachments/assets/d3fb2d60-f182-4dbb-a8c6-e146e481a117)

### Lecture 3 : Hadoop vs Spark

#### Misconception:

- Hadoop is a database - its not a database just a filesystem (hdfs)
- Spark is 100 times faster than hadoop
- Spark processes data in RAM but Hadoop doesnt

#### Differences

##### Performance
![image](https://github.com/user-attachments/assets/80625bf5-1712-44f6-a30d-47490e526e4d)

Hadoop does lot of read write IO operations and sends data back and forth to the disk.
![image](https://github.com/user-attachments/assets/85eaa7f1-52b8-44a0-a283-4bd78e11b0a8)

But in spark each executor has its own memory.
![image](https://github.com/user-attachments/assets/8c313769-001a-4a1c-a16a-a33ea125a92a)

Where is there no difference?

When we have very less data like 10 GB, there is no difference because the hadoop cluster also doesnt write to the disk it fits first time in memory.

##### Batch vs Stream Processing
![image](https://github.com/user-attachments/assets/8f6b407c-d59c-457a-bbeb-09700b857b35)

##### Ease of Use
![image](https://github.com/user-attachments/assets/35254ae3-78dc-417c-aab5-02b018e3e11f)

Spark has both low level and high level API in Python which is easier than using Hive. Low level programming is on RDD level.

##### Security

- Hadoop has in built Kerberos Authentication via YARN whereas Spark doesnt have any security mechanism.

- The authentication helps create ACL lists at directory level in HDFS.

- Spark uses HDFS Storage so it gets ACL feature / ability and when it uses YARN it gets Kerberos Authentication.

##### Fault Tolerance

![image](https://github.com/user-attachments/assets/6a4f988b-06b6-4860-a5c0-5302a2bb6ccb)

Data Replication in Hadoop
![image](https://github.com/user-attachments/assets/2ef73e22-6288-44fb-8b2d-1ae974abbd95)

HDFS keeps track of which node / rack has the data from A B C and D

![image](https://github.com/user-attachments/assets/26741f86-2eaf-4dce-b3d8-f2b9957bbeb4)

**DAG in Spark**

- So Spark computes / transforms in multiple processes Process 1 -> Process 2 -> Process 3 ....
- After each process the data is stored in a data structure called RDD which is immutable. So even if there is a failure Spark engine knows how to reconstruct the data for a particular process from the RDD at that stage.

### Lecture 4 : Spark Ecosystem

![image](https://github.com/user-attachments/assets/1790b682-10ba-4c47-8594-d743fbe54650)

High Level API : We cna write any SQL queries in python,java etc... there are ML and GraphX librries also.

We can write code in many languages. Low Level API : we can make RDD's and work on them.

![image](https://github.com/user-attachments/assets/452c4dc0-20d7-45e3-89f6-fb53719f75b9)

#### Where does Spark run?

![image](https://github.com/user-attachments/assets/d2c11530-6dc3-485e-98c7-10e7bafac25b)

Spark Engine would need some memory for transformation.

- suppose it needs 4 worker nodes each 20 GB and a driver node of 20 gb.
- it goes to the cluster manager and asks for total 100 GB of memory, if available then the manager will assign that muuch storage.
- cluster manager is also called YARN, K8S, Standalone managers

### Lecture 5 : Read Modes in Spark

![image](https://github.com/user-attachments/assets/7ab22f33-3951-45d7-849e-83f693e5bf4b)

format -> data file format : csv,json,jdbc and odbc connection. Format is optional parameter, by default its parquet format
option -> inferschema, mode and header [**optional field**]
schema -> manual schema can be passed here
load -> path from where we need to read the data [**not optional**]

#### DataframeReader API

Access it using 'spark.read' in the spark session

![image](https://github.com/user-attachments/assets/0ba45b86-8921-41dc-8453-ebc4298184ab)

#### `mode` in Spark

![image](https://github.com/user-attachments/assets/8ef66ae0-5f09-4610-8ae4-120aa9ecd673)

### Lecture 6 : Spark Architecture

#### Spark Cluster

![image](https://github.com/user-attachments/assets/58ee64d9-0105-453c-97a6-9888b804c98a)

- 20 core per machine and 100 GB RAM / each machine
- Total Cluster : 200 cores and 1TB RAM

![image](https://github.com/user-attachments/assets/aaaca550-af99-41ba-bbd3-158a83941819)

- The master is controlled by Resource Manager and the workers are controlled by Node Manager.

#### What happens when user submits code?
![image](https://github.com/user-attachments/assets/1cea605b-f750-406a-ae44-819bc06ccea3)

- The user submits some Spark code for execution to the Resource Manager. It needs 20 GB RAM, 25 GB executor, 5 total executors and 5 CPU cores.
- So the manager goes to W5 and asks to create 20GB container as the driver node.

#### What happens inside the container?

##### Driver Allocation

Now this 20 GB driver is called Application Master
![image](https://github.com/user-attachments/assets/a85199e1-0036-4e51-842a-39faab13adab)

There are two main() functions inside the master, one is for PySpark and other is for JVM like Java,Scala etc...

The JVM main() is called Application Driver.

The Spark Core has a Java Wrapper and the Java Wrapper has a Python Wrapper.

When we write code in PySpark it gets converted to Java Wrapper.

The PySpark driver is not a requirement but the Java Wrapper is required to run any code.

##### Worker Allocation

![image](https://github.com/user-attachments/assets/6fccdb87-a254-4bc2-9c50-38c9a9d26a02)

- Now the Application master asks for the executors to be assigned and the resource manager allocates.

#### Executor Container

![image](https://github.com/user-attachments/assets/1ee66178-03be-474c-8b02-ec1cc8f73a01)

Each executor has 5 core CPU and 25GB RAM.

THe above is when we have pure Java code and dont use Python UDF.

But what if we use Python UDF functions?

![image](https://github.com/user-attachments/assets/69057cb6-f0f7-40c5-86ab-ab06689bcd08)
We need a Python worker inside the executor to be able to run the code.

### Lecture 7 : Schema in Spark

#### StructType and StructField
![image](https://github.com/user-attachments/assets/c5adae79-16fa-4643-80ea-88c538407c9d)

Example:

![image](https://github.com/user-attachments/assets/bb98a403-21d9-4721-9d48-442bc6bd5006)

![image](https://github.com/user-attachments/assets/a042b2de-561a-4863-a85e-6bf589c385c3)

How to skip the header row?

```python
df = spark.read.option("skipRows", 2).csv("file.csv")
```

### Lecture 8 : Handling Corrupter Records in Spark

![image](https://github.com/user-attachments/assets/addd14cb-62fd-4af2-a770-8092879a5f1b)

#### How many records in each mode?

![image](https://github.com/user-attachments/assets/a6396113-d14b-43a1-897d-a9f3eaedb022)

##### Permissive Mode
![image](https://github.com/user-attachments/assets/83e72541-f3b8-4eaa-a08d-81087a9f21b9)

##### DropMalformed
![image](https://github.com/user-attachments/assets/f20b5861-4bf1-4826-856d-2d6ae7680193)

#### How to Print Corrupted Records
![image](https://github.com/user-attachments/assets/74bc5cd8-b0bb-4701-869d-ab6a19aa62d8)

![image](https://github.com/user-attachments/assets/83aca551-1652-4fff-928b-bf0c22ef3d8d)

Output
![image](https://github.com/user-attachments/assets/b8779e7e-5dcd-44fe-bfc1-4d218fe4177c)

#### How to Store Corrupted Records
![image](https://github.com/user-attachments/assets/f9cbcb56-6f8d-47cb-8d3e-4c5427a0b27d)

The corrupted records are in json format
![image](https://github.com/user-attachments/assets/51982d15-67d4-4f1a-94b8-ab51cc8e3bba)

### Lecture 9 : Transformations and Actions in Spark

![image](https://github.com/user-attachments/assets/347c73e6-2cdb-491b-85b8-a98797df7b5f)

#### Types of Transformations

- Narrow Transformation
- Wide Transformation

![image](https://github.com/user-attachments/assets/7fa407aa-fe59-4b90-a5f4-d1cb969e06e0)

Example:
![image](https://github.com/user-attachments/assets/c7b44c1b-5e48-4728-9a24-93fe42762bf0)

Suppose data is of 200MB. 200MB / 128MB = 2 partitions

![image](https://github.com/user-attachments/assets/0c74472a-ec82-4241-a236-2ed3c2e35ea2)

Let's say both partitions go to separate executors.

Q1 : Filtering Records
![image](https://github.com/user-attachments/assets/5bbf61d7-1116-4d0d-b860-f5410f12c1b8)
There is no data movement here.

Q2: Find Total Income of each employee
![image](https://github.com/user-attachments/assets/3524bd45-9d80-43d7-a134-2a43460fae5b)

One id = 2 record is in one partition and the other is in the second partition so we need to do wide transformation
![image](https://github.com/user-attachments/assets/060eb0d1-a8fc-44b5-843e-738ebd87e42e)

Data needs to be shuffled and records with same id must be moved to same partition.

- filter,select,union etc are narrow transformations
- join,groupby,distinct

### Lecture 10 : DAG and Lazy Evaluation in Spark

![image](https://github.com/user-attachments/assets/b323161d-5dcf-4a01-ad70-05b11c4e811f)

- For every action there is a new job, here there are three actions : read,inferSchema,sum and show
- When used with groupBy().sum(): It is considered an action because it triggers computation to aggregate data across partitions and produce a result. This operation forces Spark to execute the transformations leading up to it, effectively creating a job.
- When used as a column expression df.select(sum("value")): It acts more like a transformation in Spark's context, especially if part of a larger query or pipeline that does not immediately trigger execution. In this case, it only defines the operation and does not create a job until an action (like show() or collect()) is called.

1. Job for reading file
![image](https://github.com/user-attachments/assets/c568a81e-dfa8-4637-bf22-637605286140)
Whole Stage Codegen - generate Java ByteCode

2. Inferschema
![image](https://github.com/user-attachments/assets/c79751a7-ea04-444a-8940-61eb0d144a5f)

3. GroupBy and Count
As explained above this is an action.

4. Show
Final action to display df

![image](https://github.com/user-attachments/assets/925397f9-c1e6-4662-ba01-a52d8bcc04ab)
After we read the csv and inferSchema there are no jobs created since filter and repartition both are transformations not actions.

When there are two filters on same dataset

![image](https://github.com/user-attachments/assets/a05bb675-508b-42bb-8128-f38a5e0d21fa)

This is the job
![image](https://github.com/user-attachments/assets/272cea9a-7570-4716-b831-1883472cc4be)

##### Optimizations on the Filter
Both the filters are on the same task
![image](https://github.com/user-attachments/assets/2682b8b3-3f31-4d5e-ba6a-b2ea32ea2246)
The optimizations can be applied because Spark is lazily evaluated.

### Lecture 11: Working with JSON Data in Spark

![image](https://github.com/user-attachments/assets/09ce5719-db12-446c-8247-9495ea979768)

Two types of JSON notation:

- Line Delimited JSON
![image](https://github.com/user-attachments/assets/95b248fd-491a-4083-963f-102489848154)

- Multi Line JSON
![image](https://github.com/user-attachments/assets/91f43e31-58a1-4443-a5c2-fc376ef61c38)

```json
[
{
  "name": "Manish",
  "age": 20,
  "salary": 20000
},
{
  "name": "Nikita",
  "age": 25,
  "salary": 21000
},
{
  "name": "Pritam",
  "age": 16,
  "salary": 22000
},
{
  "name": "Prantosh",
  "age": 35,
  "salary": 25000
},
{
  "name": "Vikash",
  "age": 67,
  "salary": 40000
}
]
```

Line Delimited JSON is more efficient in terms of performance because the compiler knows that each line has one JSON record whereas in multiline json the compiler needs to keept track of where the record ends and the next one starts.

#### Different number of keys in each line

![image](https://github.com/user-attachments/assets/8aeeeb0a-906f-44a5-b3a0-a7c5c8d28e31)

Here what happens is that the line with the extra key has the value while for the rest its null
![image](https://github.com/user-attachments/assets/1fc8a438-c9f8-4d7e-8fbb-82c8ec73f167)

#### Multiline Incorrect JSON

We dont pass a list here rather its just dictionaries
```json
{
  "name": "Manish",
  "age": 20,
  "salary": 20000
},
{
  "name": "Nikita",
  "age": 25,
  "salary": 21000
},
{
  "name": "Pritam",
  "age": 16,
  "salary": 22000
},
{
  "name": "Prantosh",
  "age": 35,
  "salary": 25000
},
{
  "name": "Vikash",
  "age": 67,
  "salary": 40000
}
```
When we process the json it just reads the first dictionary as a record and the rest is not processed.

![image](https://github.com/user-attachments/assets/6b25b6f2-8eda-466d-affc-08c0fed2f551)

#### Corrupted Records

We dont need to define ```_corrupted_record``` in the schema, it will add the column on its ownn

![image](https://github.com/user-attachments/assets/60f6c31e-6174-40ab-ba71-e3f0070a01fa)

### Lecture 12: Spark SQL Engine

![image](https://github.com/user-attachments/assets/ffb137d5-5a71-427d-b411-1493925ed6a4)

#### How is Spark Code compiled?


- The catalyst optimizer creates a plan and creates RDD lineage

#### Phases in Catalyst Optimizer

![image](https://github.com/user-attachments/assets/4dcb1108-768c-4c28-aa21-732e93fda646)

##### Workflow Diagram

- Unresolved Logical Plan : Bunch of crude steps to execute the SQL code
- Catalog : The table, files and database metadata information si stored in the catalog. Suppose we call read.csv on file that doesnt exist. The procedure that gives / throws the error is assisted via the catalog. In Analysis phase, we go through these steps. If some file/table is not found then we get **Analysis Exception** This error occurs when the Logical plan provided is not able to be resolved.
- Reoslved Logical Plan : This is the phase when we finished analysing the catalog objects.
- Logical Optimization: There are many examples. Suppose we need just two columns in select output, the spark engine does not fetch all the columns rather jsut fetches the two columns from memory that we need. Another example is when we use multiple filters on the same column in different lines of code. When we execute this code, we see that all of it is executed with **or** statements in one single line of code.
- Physical Plan: This involves taking decision like the type of join to use: Broadcast Join is one example. From the logical plan, we can build multiple physical plans.
Thebest Physical Plan is a set of RDDs to be run on different executors on the cluster.

![image](https://github.com/user-attachments/assets/7931f705-5d53-45d0-8bdc-407e2b3426a7)

### Lecture 13: Resilient Distributed Dataset

![image](https://github.com/user-attachments/assets/9f092749-7050-4067-9b9f-4e19e3527a18)

#### Data Storage of List
![image](https://github.com/user-attachments/assets/023e8304-b40a-40a6-8f61-516efe301635)

#### Data Storage in RDD

Suppose we have 500MB of data and 128MB partition, so we will have 4 partitions.

The data is scattered on various executors.
![image](https://github.com/user-attachments/assets/4c99e784-5366-4ee4-b1ac-c7baa0a49f34)

Its not in single contiguous location like elements of a list. The data structure used ot process this data is called RDD
![image](https://github.com/user-attachments/assets/99aac217-5141-4c6b-bcbe-0873e7a9bbbd)

![image](https://github.com/user-attachments/assets/01a10422-cb78-42a3-bb95-db643950b621)

Why is RDD recoverable?

- RDD is immutable. If we apply multiple filters each dataset after filtering is a different dataset
![image](https://github.com/user-attachments/assets/ff872b52-f89f-406e-b8e1-30edd48624cf)

- In below case if rdd2 fails then we can restore rdd1 because of the lineage.
![image](https://github.com/user-attachments/assets/9497cf7a-7646-4dc1-ba2b-790e524572f5)

#### Disadvantage of RDD

- No optimization done by Spark on RDD. The dev must specify explicitly on how to optimize RDD.

#### Advantage

- Works well with unstructured data where there are no columns and rows / key-value pairs
- RDD is type safe, we get error on compile time rather than runtime which happens with Dataframe API.

#### Avoiding RDDs

![image](https://github.com/user-attachments/assets/7dcd2caa-fac8-478f-9ba2-e99370c3fb44)

- RDD : How to do? Dataframe API: Just specify what to do?

![image](https://github.com/user-attachments/assets/a028ab4e-b35e-4ead-9c04-a5cdbbf7f228)
You can see in above case that we have a join and filter but we are specifically saying that first join then filter so it triggers a shuffle first and then filter which is not beneficial.

### Lecture 14 : Parquet File Internals

![image](https://github.com/user-attachments/assets/50def6a3-7bfa-4b14-881d-46710762a06b)

There are two types of file formats:

- Columnar Based and Row Based

#### Physical Storage of Data on Disk
![image](https://github.com/user-attachments/assets/76e40279-29f0-43b3-80ec-fd4c3e9e4894)

#### Write Once Read Many

The funda of big data is write once read many.

- We dont need all the columns for analytics of big data, so columnar storage is the best.
- If we store in row based format then we need to jump many memory racks to be able to get the data we need.

![image](https://github.com/user-attachments/assets/4fb9d3cc-541e-4b28-a818-5be35e211a8f)

- OLTP generally use row base4d file format.
- I/O should be reduced so OLAP uses columnar format.

#### Why Columnar format may not be the best?

![image](https://github.com/user-attachments/assets/94d7beb7-be65-4836-9fce-1ec86285d842)

In above case we can get col1 and col2 easily but for col10 we still need to scan the entire file.

To tackle this:

Let's say we have 100 million total rows.

We can store 100,000 records at a time, continuously in one row, then the next 100,000 records in next row and so on in hybrid format.

![image](https://github.com/user-attachments/assets/af359956-aa81-4f62-a692-b1492bc7ae0c)

#### Logical Partitioning in Parquet

![image](https://github.com/user-attachments/assets/d72060bc-6425-4b18-a1e8-3bd2e7b6376d)

Let's day we have 500mb data, each row group by default has 128 mb data, so we will have 4 row groups.
Each row group will have some metadata attached to it.

In our example let's say one row group has 100000 records.
The column is futher stored as a page.

#### Runlength Encoding and Bitpacking

![image](https://github.com/user-attachments/assets/5a0219f3-ea0f-4758-ab80-1f3513a5a79f)

Suppose we have 10 lakh records but there can be say 4 countries.

So parquet actually creates a dictionary of key value pair with key as int starting from 0 to 3 and then in the dictionary encoded data, we can see the keys being used insted of country name.

#### Demo

```parquet-tools inspect <filename>```

![image](https://github.com/user-attachments/assets/be572741-6fd9-470b-ad98-0f0d6c293a38)
![image](https://github.com/user-attachments/assets/e4fff36d-48ed-4ca8-9cbd-310f8b35a103)

Gives some file and brief column level metadata.

```parquet_file.metadata.row_group(0).column_group(0)```
![image](https://github.com/user-attachments/assets/ea81d74c-6fb3-4c80-bbbf-521f6c1a3be2)

Compression is GZIP
![image](https://github.com/user-attachments/assets/7d841a8d-fc8d-4f8c-8a42-da2b436a13fc)

Encoding is explained on top.

#### Bitpacking Advantage

- Bitpacking helps in compressing the bits so in above case we just have 4 unique values and hence we need just 2 bytes.
- Query in seconds for running select on csv,parquet etc..

![image](https://github.com/user-attachments/assets/7700c5a0-90b9-4ad1-b430-25ca7df99903)

#### Summary

![image](https://github.com/user-attachments/assets/e4a1bbe6-629b-4970-94bf-a6493f32146b)

- Here the actual data is stored in the pages and it has metadata like min,max and count.

- Let's say we need to find out people less than 18 years age

![image](https://github.com/user-attachments/assets/eb37e1e1-ddab-42da-872b-0de10dbf12f2)

Here when we divide data into row groups, we dont need to do any IO read operation on Row group 2, it saves lot of time and optimize performance.

The above concept is called **Predicate Pushdown**.

#### Projection Pruning

Projection Pruning means we dont read IO from columns that are not part of the select query or that arent required for any join.

### Lecture 15 : How to write data on the disk?

![image](https://github.com/user-attachments/assets/a22d1931-1b95-4515-9311-5c53883b47ba)

![image](https://github.com/user-attachments/assets/03f8e132-9ead-4ae4-9d59-ad339ebcf615)

#### Modes to write data

![image](https://github.com/user-attachments/assets/1ecedad1-043a-49d9-be96-d1ba66d062c3)

Create three files
![image](https://github.com/user-attachments/assets/5e28b1b7-af47-4cb6-ac24-45d0a64b03a7)

```python
  write_df = read_df.repartition(3).write.format("csv")\
    .option("header", "True")\
    .mode("overwrite")\  # Using .mode() instead of .option() for overwrite mode
    .option("path", "/FileStore/tables/Write_Data/")\
    .save()
```

### Lecture 16: Partitioning and Bucketing

![image](https://github.com/user-attachments/assets/48c965e1-ffe3-4cb8-b1cf-40d3135a8cc1)

In above data we cannot partition by any column because there is no similarity but we can bucket the data.

![image](https://github.com/user-attachments/assets/a6557580-ea42-442b-9167-2bc4e5c825e0)

![image](https://github.com/user-attachments/assets/637c53b2-5a96-4388-ab07-113e5917ce99)
In above data we can partition by the country, but again we might have more data in India partition and less data in Japan.

#### Example of Partitioning 

![image](https://github.com/user-attachments/assets/6fd554a4-5d68-41c5-bb7e-d2b59a5edd51)

![image](https://github.com/user-attachments/assets/c9f1a402-de99-4ae2-8842-c357b31e3636)

The advantage is that the entire data is not scanned and only few partitions are scanned based on the filters.

**Partitioning by Id**

![image](https://github.com/user-attachments/assets/ca71390e-bcd6-423e-9a0a-4a8f48abe967)

Here we can see that we have created partitions by ID and since ID is low cardinality column partitioning is not efficient and we need to use bucketing.

#### Partitioning by Address and Gender

![image](https://github.com/user-attachments/assets/9a1a1836-f740-4f74-a3a8-412d8b4c39c6)

#### Bucketing by Id

Dividing into 3 buckets
![image](https://github.com/user-attachments/assets/9c9446d5-a67a-4a7b-9816-a3dd5f87a6f1)

#### Tasks vs Buckets

![image](https://github.com/user-attachments/assets/28c545a4-74dd-4dc8-8406-f716a769b09b)

- If we have 200 partitions we will have 200 tasks and each task will create 5 buckets each, to tackle this we first repartition into 5 partitions and then bucketBy 5.

#### How does bucketing help with joins?

![image](https://github.com/user-attachments/assets/6db2b3d0-7a19-40dd-8f22-f0bb95b7df9e)

- Here we can see that since we have same column bucket on both tables the ids can be easily mapped and there is no shuffling.

#### Bucket Pruning

![image](https://github.com/user-attachments/assets/237d7bda-2c12-462c-9092-b71921c3321d)
Suppose we have 1M Aadhar Ids and we divide into 100,000 each bucket so when we divide the above aadhar id by 100000 then we get the exact bucket where the number lies in.

### Lecture 17 : Spark Session vs Spark Context

- Spark Session is entry point to the Spark cluster where we provide the parameters to create and operate our cluster.
- Spark session will have different context like one for SQL, PySpark etc...

![image](https://github.com/user-attachments/assets/c122f106-6b42-42d1-bd4a-201e8b482152)

### Lecture 18: Job, Stage and Tasks

![image](https://github.com/user-attachments/assets/f54725bf-2e81-4b73-a65c-97cb449887c7)

- One Application is created.
- One job is created per action.
- One stage is defined for every transformation like filter.
- Task is the actually activity on the data that's happening.

![image](https://github.com/user-attachments/assets/025a67b4-2ced-4ad9-a23a-eaa6d65f349c)

#### Example of Job,Action and Task

![image](https://github.com/user-attachments/assets/b232dc8d-ff27-4650-92ca-7c3b912b5132)

#### Complete flow diagram
![image](https://github.com/user-attachments/assets/4e07a77b-8885-46a7-8793-53d7dd3f5f59)

Every job has minimum one stage and one task.

![image](https://github.com/user-attachments/assets/96990346-8429-41e7-ac94-f11855baa9de)
Repartition to filter is one job because we dont hit an action in between.

Every wide dependency transformation has its own stage. All narrow dependency transformations come in one stage as a DAG.

![image](https://github.com/user-attachments/assets/d9c8d425-892c-4ac0-bb6e-930bc9f51a32)

#### How do tasks get created? [Read and Write Exchange]

![image](https://github.com/user-attachments/assets/4d47470c-a3bc-4656-9b1a-7f718edd2c47)

- The repartition stage actually is a wide dependency transformation and creates two partitions from one, its a Write exchange of data.
- Now the filter and select stage reads this repartitioned data(**Read exchange**) and filter creates two tasks because we have two partitions.
- Next we need to find out how many folks earn > 90000 and age > 25 so we need to do a groupby that's a wide dependency transformation and it creates another stage. By default there are 200 partitions created.
- So some partitions may have data and some wont.

![image](https://github.com/user-attachments/assets/ec5734b2-3985-4fdd-abc4-4933e890e080)

### Lecture 17: Dataframe Transformations in Spark Part 1

![image](https://github.com/user-attachments/assets/b3c9d9a3-b664-4cde-868f-d8d9c508ed9f)
Data gets stored in Row() format in the form of bytes

![image](https://github.com/user-attachments/assets/fccd78ab-d343-41dd-9a48-77122a4447d9)

Columns are expressions. Expressions are set of transformations on more than one value in a record.

#### Ways to select values / columns

![image](https://github.com/user-attachments/assets/3bb9ee25-d1d2-42e9-bb8b-22cb7c1030d3)

![image](https://github.com/user-attachments/assets/ccd538cb-5122-4ca4-ae8f-0e1d46a56996)

Column Manipulations

![image](https://github.com/user-attachments/assets/be26f027-5ef2-4475-8fd9-2e520be44dab)

Other methods
![image](https://github.com/user-attachments/assets/705819f1-fb56-4024-a3f1-4590706a58f7)

**selectExpr**
![image](https://github.com/user-attachments/assets/7ccf1d62-4834-43b8-84ae-7727a159eccc)

**Aliasing Columns**
![image](https://github.com/user-attachments/assets/e9710673-c2b4-476f-8296-fd1ee25681b5)

### Lecutre 18 : Dataframe Transformations in Spark Part II

#### ```filter()``` / ```where()``` no difference

![image](https://github.com/user-attachments/assets/ccdb523c-04bb-490a-bd54-e051dc0d221b)

![image](https://github.com/user-attachments/assets/19d178e5-086e-41c1-908f-689badb24df8)

#### Multiple filter conditions 

![image](https://github.com/user-attachments/assets/baa7134d-e151-404e-98d6-5dc8b010fc5d)

#### Literals in spark
Used to pass same value in all the columns
![image](https://github.com/user-attachments/assets/b96c60d9-754f-450d-bc46-7aaf6848c095)

#### Adding Columns
If the column already exists then it gets overwritten.
![image](https://github.com/user-attachments/assets/32f4d415-9685-4329-acfd-41ee7a7fd720)

#### Renaming Columns
![image](https://github.com/user-attachments/assets/6fa9577a-c0f3-4e54-b756-d24cb6fb6eda)

### Lecture 19: union vs unionAll()

![image](https://github.com/user-attachments/assets/3e649ae8-6b69-4fa9-b687-109e4ede5615)

We can see that here we have a duplicate id
![image](https://github.com/user-attachments/assets/3680c897-59c2-4f04-963d-3ce99981f3b4)

In PySpark union and unionAll behaves in the same way, both retain duplicates
![image](https://github.com/user-attachments/assets/041e31d1-017f-45f7-aa7e-3c7db513d617)

But in Spark SQL when we do union it drops the duplicate records
![image](https://github.com/user-attachments/assets/05af5b19-9963-4581-a71d-77fe42f739cf)

![image](https://github.com/user-attachments/assets/00fde583-6538-4cc3-b275-97d8c5d620b2)

#### Selecting data and unioning the same table

![image](https://github.com/user-attachments/assets/f9226608-4b77-40db-91e1-82072e8cd14b)

#### What happens when we change the order of the columns?

```wrong_manager_df``` actually has the wrong order of columns but still we get the union output but in a wrong column values.
![image](https://github.com/user-attachments/assets/3db3d2c8-3008-4930-b223-6f7bb31da477)

If we give different number of columns an exception is thrown.
![image](https://github.com/user-attachments/assets/ece32bd0-6ea3-45f1-8919-721ef783c65b)

If we use unionByName then the column names on both dfs must be the same.
![image](https://github.com/user-attachments/assets/fd3659ae-703f-42bc-bd4a-49c9c427cd9e)

### Lecture 19: Repartitioning and Coalesce

Suppose we have 5 partitions and one of them is skewed a lot 100MB, let's say this is the best selling product records. This partition takes lot of time to compute. So the other executors have to wait until this executor finishes processing.
![image](https://github.com/user-attachments/assets/2a5567b0-486c-4b8b-aa91-41d077281e91)

#### Repartitioning vs Coalesce

##### Repartitioning

Suppose we have the above partitions and total data is 100mb. let's say we do repartition(5) so we will have 5 partitions now for the data with 40mb per partition.

##### Coalesce

In case of coalesce there is no equal splitting of partition memory, rather the already existing partitions get merged together.
![image](https://github.com/user-attachments/assets/85f6803b-6905-49e4-b3b3-3a896cde668f)

There is no shuffling in coalesce but in repartitioning there is shuffling of data.

#### Pros and Cons in repartitioning

- There is evenly distributed data.
- Con is that IO operations are more, its expensive.
- Con of coalesce is that the data is unevenly distributed.

Repartitioning can increase or decrease the partitions but coalescing can only decrease the partitions.

#### How to get number of partitions?

```flight_df.rdd.getNumPartitions()``` gets the initial number of partitions and then we can repartition ```flight_df.repartition(4)```. Data is evenly distributed.

![image](https://github.com/user-attachments/assets/00bd0cfe-e61a-4826-b978-b6c02924a363)

**Repartitioning based on columns**

![image](https://github.com/user-attachments/assets/9d39f248-2be8-4520-a57a-4084bcfc297f)

Since we asked for 300 partitions and we have 255 records some partitions will have null record.
![image](https://github.com/user-attachments/assets/c59615d8-65c1-44e8-85c4-3e1833a4cb60)

#### Coalescing

![image](https://github.com/user-attachments/assets/210eb04d-80b3-4cce-a7dd-1b7757b3bd1c)
Suppose we have 8 partitions and we coalesce into 3 partitions. Coalesce has only one arg.

Uneven distribution of data in partitions.
![image](https://github.com/user-attachments/assets/bc136007-2ae3-4df1-90b4-625352a81809)

### Lecture 20 : Case when / if else in Spark

![image](https://github.com/user-attachments/assets/ee17eab0-640d-4fc5-ac03-f751a8a90831)

![image](https://github.com/user-attachments/assets/310da700-3caa-44c2-a508-5fa19ff1ef66)

#### Apply logic on one column then process if else logic

![image](https://github.com/user-attachments/assets/ba68a0f3-82d4-4db1-a879-fb977423f9dc)

#### Spark SQL Logic

![image](https://github.com/user-attachments/assets/b0fd9a4f-b452-4132-9b6b-ad543a0c7056)

### Lecture 21 : Unique and Sorted Records

![image](https://github.com/user-attachments/assets/bff40f32-fa87-4a64-b448-a72ca92bf1d2)

#### distinct()

Original Data
![image](https://github.com/user-attachments/assets/8417fe25-264b-4d03-910b-a28063b07186)

Distinct Data
![image](https://github.com/user-attachments/assets/95b4fe97-033f-4a28-87a7-d0a1ad37498b)

Distinct Based on certain columns
![image](https://github.com/user-attachments/assets/612a6833-011e-4631-b706-4df9f318d6e9)

⚠️ Distinct takes no arguments we need to select the columns first and then apply distinct.

#### Dropping duplicate records

Point to note is that the dataframe ```manager_df``` has no changes, it just shows the records after dups have been dropped.
![image](https://github.com/user-attachments/assets/b443755e-1fc8-4d30-95f8-9c73c3412c6d)

#### sort()

![image](https://github.com/user-attachments/assets/fc5d7b04-992a-4530-9660-a4f2ae7d82f9)

Descending order
![image](https://github.com/user-attachments/assets/3865f2de-b818-4d5c-84e0-193390ba4586)

**Sorting on multiple columns**

Here first the salary is srranged in desc order then we arrange the name in asc order from those records with same salary.
![image](https://github.com/user-attachments/assets/3fce7816-872f-414f-8bfb-8ad329d9ed73)

### Lecture 22 : Aggregate functions

#### Count as both Action and Transformation

![image](https://github.com/user-attachments/assets/d2cd9647-fc8a-4247-b04e-539a48331f76)

⚠️ When we are doing count on a single column and there is a null in it, its not considered in the count. But for all columns we have nulls in the count.
![image](https://github.com/user-attachments/assets/1ae8b278-3675-439c-9b12-8853064c9f3a)

Job created in first case and its not created in second case below.
![image](https://github.com/user-attachments/assets/8a771986-85e2-465d-a2c4-d4a2bd86dfca)

### Lecture 23: Group By In Spark

Sample Data

![image](https://github.com/user-attachments/assets/17c9a1dd-b003-4c67-8b1f-3f4e8fb6a556)

#### Questions

![image](https://github.com/user-attachments/assets/60d2d30b-c2c9-4e3f-9544-b8ab7eece55c)

Salary per department using groupBy()
![image](https://github.com/user-attachments/assets/b90a254d-1aac-46f1-8e2e-c66e8d99c0ad)

#### Where do we use window functions?

Suppose we need to find out the percentage of total salary from a particular dept that the person is earning. we can use window function to specify the total salary per department in the particular record itself like I've shown below.
![image](https://github.com/user-attachments/assets/6c328d14-bf1e-4059-83d5-618f6c7a0ec0)

This way we dont need to perform a join.

![image](https://github.com/user-attachments/assets/c6ababa6-3031-4147-887e-1b0b80a7fc13)

#### Grouping by two columns

![image](https://github.com/user-attachments/assets/0822535b-c50a-433a-bd1e-67b9ee6b9dcc)

### Lecture 24 : Joins in Spark part 1

![image](https://github.com/user-attachments/assets/442da83f-1447-4834-ba6b-6195fb5e775c)

Which customers joined platform but never brought anything?

![image](https://github.com/user-attachments/assets/9d0f578f-a02a-4da1-b8c4-3d88767b5fb7)

Whenever we need information from another table, we use joins and there should be some common column.

Join is a costly wide dependency operation.

#### How do joins work?

How many records do we get after inner joining the below two tables.
![image](https://github.com/user-attachments/assets/6e83fe11-578b-4590-9a89-43c98ca482a8)

We get a total of 9 records.
![image](https://github.com/user-attachments/assets/d706afb9-74bf-4c99-bceb-ed9327a2357d)

Sometimes data gets duplicated when we do joins, so we should use distinct() but remember distinct is wide dependency transform.

### Lecture 25 : Types of Join in Spark

![image](https://github.com/user-attachments/assets/e5e441c3-c64d-40ed-8646-89afcecc0be1)

#### Inner Join
![image](https://github.com/user-attachments/assets/641aa365-9493-46ff-9cb3-518805fda892)

#### Left Join
![image](https://github.com/user-attachments/assets/295cadda-2a97-41bb-a02d-997dfafd3a5b)
All records in left table + those that join with right table, whereever we dont get match on right table the columns become null.

#### Right Join
![image](https://github.com/user-attachments/assets/0e0c88d6-a290-42a7-901c-eae316262a44)

#### Full Outer Join
![image](https://github.com/user-attachments/assets/b49eb89d-829a-44f5-a30a-4ab08a89a289)

#### Left Semi Join 
![image](https://github.com/user-attachments/assets/acf7fb6a-d939-4b80-9bb7-7b411e43ac2e)

![image](https://github.com/user-attachments/assets/fc790260-df75-470a-8c91-795095ce72b2)

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LeftSemiJoinExample").getOrCreate()

# Left DataFrame: Orders
orders = spark.createDataFrame([
    (1, "iPhone"),
    (2, "Pixel"),
    (3, "OnePlus"),
    (4, "Nokia")
], ["customer_id", "product"])

# Right DataFrame: Valid Customers
valid_customers = spark.createDataFrame([
    (1,), (3,)
], ["customer_id"])

# Perform left semi join
filtered_orders = orders.join(valid_customers, on="customer_id", how="left_semi")
filtered_orders.show()
```

**Output**

```
+-----------+--------+
|customer_id|product |
+-----------+--------+
|          1|iPhone  |
|          3|OnePlus |
+-----------+--------+
```

#### Left Anti Join

![image](https://github.com/user-attachments/assets/108e662c-63c8-4115-8181-928f66a0665c)

Find out all customers who have never purchased any product.

#### Cross Join

Never use cross join!
![image](https://github.com/user-attachments/assets/4d9b51bd-9a07-476c-a53c-3166bceec0b8)

![image](https://github.com/user-attachments/assets/10038361-8d23-4adb-9b1c-23095ae05aab)

### Lecture 26 : Join Strategies in Spark

![image](https://github.com/user-attachments/assets/45d79335-9f31-43d8-9a04-93d48ec3a918)

Joins are expensive due to shuffling.

4 partitions are there in each dataframe.

![image](https://github.com/user-attachments/assets/cae9e337-7d63-4134-8df1-964847c351e4)

Executors in the cluster

![image](https://github.com/user-attachments/assets/267e6dd1-b981-441d-a2dd-693e2e013c7d)

Now we need to join employee and salary df to get the output but they are on different executors, so we need to do data shuffling.

Each executor has 200 partitions. Goal is to get all same keys in one executor.
![image](https://github.com/user-attachments/assets/80daa55e-8dce-4e3e-839d-8f6b2b2bee16)

![image](https://github.com/user-attachments/assets/e37dd852-daa4-4f1c-be91-83d01451cb57)

![image](https://github.com/user-attachments/assets/9266d9fb-9dee-486a-9e38-ffcd00658fcf)

- Since we want to get id for 1 we divide 1/200 = 1 and then send all the data to that executor 1.

![image](https://github.com/user-attachments/assets/69e73f9b-f7af-461e-8ac9-65f2d279a1c3)

Suppose we want to map the salary for id = 7 so the data from the employee df with id = 7 and also salary df with id=7 will come into the executor 7.

Similarly id = 201 will go into 201/200 = executor no 1.

#### Types of Join Strategies

![image](https://github.com/user-attachments/assets/58ea7594-9378-4fd6-b0f7-a16b77c88d4c)

![image](https://github.com/user-attachments/assets/9d1c2231-bc9a-41e2-8cbf-3137570acfe0)

Joins generally result in shuffling

There are two dataframes df1 and df2 each with 4 partitions.

![image](https://github.com/user-attachments/assets/fde4638b-d6a4-46d1-926b-fd7f20cabf2d)

We have two executors.

In join goal is to join with same keys.

![image](https://github.com/user-attachments/assets/12274ff6-b7a6-4e32-8cca-7d4409b5dd75)

We can see that red P1 has corresponding id for salary in the other executor.

![image](https://github.com/user-attachments/assets/6339f3f0-2e8e-4e48-aa22-69ce46a2ac5c)

We need to get same keys fetched from other executors.

When a dataframe is sent to executors by default 200 partitions are created per dataframe.

![image](https://github.com/user-attachments/assets/8465bc0e-5f80-4c19-8697-14f03e889c9f)

Now let's say we want to find salary for id = 1 we can divide 1/200 on blue = 1 and 1/200 on red = 1, so both data will come into executor 1 in the partition 1.

![image](https://github.com/user-attachments/assets/574fd6aa-aa86-49ab-a23c-28fa37c2f351)

Similarly for id = 7 also we will send the data on blue and red P7

But if id = 201 then 201/200 = 1 so this id will come into P1 only.

If we have id = 102 then 102/200 = 102 partition on 2nd executor.

![image](https://github.com/user-attachments/assets/d4e6056c-bb9f-4c9c-8e78-c19b3684e536)

The executors can be on different worker nodes also, we need to then move data across from one worker node to other.

### Strategies

![image](https://github.com/user-attachments/assets/22526c97-ddd0-4088-aefa-fbb29a599efb)

Broadcast nested loop join is costly because we dont do a straight join, rather its based on < an > conditions, its O(n^2)

#### Shuffle Sort Merge Join

![image](https://github.com/user-attachments/assets/3fb09974-e5a1-400c-9871-f0e748e65216)

TC : O(nlogn)

#### Shuffle Hash Join

The smaller table gets a hash table created with hashed keys in memory.

Now from df1 we checked which keys match with O(1) lookup using the hash table.

![image](https://github.com/user-attachments/assets/e2a95ff0-5c94-4871-830d-585cc23c868b)

### Broadcast Join

![image](https://github.com/user-attachments/assets/96982a15-f0dd-4b08-97ca-663ed9d63459)

The tables that are less than 100mb can be broadcast.

Scenario : Suppose one table is 1GB size so we will have 1000MB / 128MB = 8 partitions and there is another table of size 5mb.

So if we dont broadcast, then the df with 100gb should be shuffled around with 5mb data across executors for joining. Instead of that we will just send the small df in all the executors so that there is no shuffling.

![image](https://github.com/user-attachments/assets/20369a8d-d88f-42fb-8c33-3372c78d74ac)

The amount of data that can be broadcast depends on the memory of executor and driver. Make sure that there is no case where driver memory is 2GB and we are trying to broadcast 1GB data.

#### Demo

There are total 200 partitions when we join 

![image](https://github.com/user-attachments/assets/a426fb92-a489-4532-8184-56ffad0c77a6)

**Normal Sort Merge Join Execution Plan**

```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- == Initial Plan ==
   Project [sale_id#10484L, sale_date#10485, amount#10486L, country_name#10514]
   +- SortMergeJoin [country_id#10487L], [country_id#10513L], Inner
      :- ColumnarToRow
      :  +- PhotonResultStage
      :     +- PhotonSort [country_id#10487L ASC NULLS FIRST]
      :        +- PhotonShuffleExchangeSource
      :           +- PhotonShuffleMapStage
      :              +- PhotonShuffleExchangeSink hashpartitioning(country_id#10487L, 1024)
      :                 +- PhotonFilter isnotnull(country_id#10487L)
      :                    +- PhotonRowToColumnar
      :                       +- LocalTableScan [sale_id#10484L, sale_date#10485, amount#10486L, country_id#10487L]
      +- ColumnarToRow
         +- PhotonResultStage
            +- PhotonSort [country_id#10513L ASC NULLS FIRST]
               +- PhotonShuffleExchangeSource
                  +- PhotonShuffleMapStage
                     +- PhotonShuffleExchangeSink hashpartitioning(country_id#10513L, 1024)
                        +- PhotonFilter isnotnull(country_id#10513L)
                           +- PhotonRowToColumnar
                              +- LocalTableScan [country_id#10513L, country_name#10514]

== Photon Explanation ==
Photon does not fully support the query because:
		Unsupported node: SortMergeJoin [country_id#10487L], [country_id#10513L], Inner.

Reference node:
	SortMergeJoin [country_id#10487L], [country_id#10513L], Inner
```

**Spark UI Diagram**

![image](https://github.com/user-attachments/assets/e2f11398-cd8e-4020-8487-32d3d5bce576)

![image](https://github.com/user-attachments/assets/5a0406e0-6f35-4f57-8f3d-93dd3623bc31)

**Broadcast Join Execution Plan**

```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- == Initial Plan ==
   ColumnarToRow
   +- PhotonResultStage
      +- PhotonProject [sale_id#10484L, sale_date#10485, amount#10486L, country_name#10514]
         +- PhotonBroadcastHashJoin [country_id#10487L], [country_id#10513L], Inner, BuildRight, false, true
            :- PhotonFilter isnotnull(country_id#10487L)
            :  +- PhotonRowToColumnar
            :     +- LocalTableScan [sale_id#10484L, sale_date#10485, amount#10486L, country_id#10487L]
            +- PhotonShuffleExchangeSource
               +- PhotonShuffleMapStage
                  +- PhotonShuffleExchangeSink SinglePartition
                     +- PhotonFilter isnotnull(country_id#10513L)
                        +- PhotonRowToColumnar
                           +- LocalTableScan [country_id#10513L, country_name#10514]

== Photon Explanation ==
The query is fully supported by Photon.
```

![image](https://github.com/user-attachments/assets/116ece89-7dbc-43f2-9477-ceea6fe3238f)

### Window functions in Spark

#### Rank vs Dense Rank

![image](https://github.com/user-attachments/assets/73665356-9370-45b3-9499-d97cf200d464)

Dense rank does not leave any gaps between the ranks.

![image](https://github.com/user-attachments/assets/d25268ac-6ef9-4367-b151-08bcb14d320d)

#### Lead and Lag

![image](https://github.com/user-attachments/assets/60cc0b87-5d07-4873-ba7d-d1766d136dbb)

![image](https://github.com/user-attachments/assets/406bcb15-c4cd-4837-8ec9-694fe652b754)

#### Range and Row Between

![image](https://github.com/user-attachments/assets/2880cef0-ceee-4a15-a1e3-d80110fe0582)

Q1

![image](https://github.com/user-attachments/assets/7280b56c-aa7e-4521-8b0b-d4bb3c58efbd)

Using first and last functions let's try to acheive this.

Data:

![image](https://github.com/user-attachments/assets/249c83a8-5005-4faf-ab63-46e87f725819)

This solution is wrong, ideally we should get 111000 in all rows of ```latest_sales``` column.

![image](https://github.com/user-attachments/assets/79e31ba6-d7e2-4e9c-ae3b-d08b5f2502bc)

Let's look at explain plan.

We can see that the window here is ```unbounded preceeding and current row```

![image](https://github.com/user-attachments/assets/20a04927-9aeb-45bf-8458-9a8438ccfa9b)

What do these terms mean?

![image](https://github.com/user-attachments/assets/51dc44d0-ee2e-49ed-bcdf-2b0064e199fa)

- Unbounded preceeding : If i'm standing at a current row in a window I will return the result of any operation on the window from here to all the rows before me in the window.
- current_row : the row im standing at.
- Unbounded following : opposite of unbounded preceeding.
- rows_between(start_row,end_row) : basically the row we are currently at is 0, all rows before that are negative numbers and all rows after that is positive numbers.

![image](https://github.com/user-attachments/assets/ab7d0388-eff1-4780-835d-be88374a4807)

If we dont give anything then it just goes from current row to either unbounded preceeding (first row) of window or unbounded following (last row) of window.

Converting from string to unixtime when we have two fields date and time.

![image](https://github.com/user-attachments/assets/a1b00037-79e0-48be-b254-f8709e0c9616)

```emp_df = emp_df.withColumn("timestamp",from_unixtime(unix_timestamp(expr("CONCAT(date,' ',time)"),"dd-MM-yyyy HH:mm")))```

The timestamp column is a string.

![image](https://github.com/user-attachments/assets/b8767f27-92fc-4b03-bb70-2d1507ba368e)

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

### Lecture 27: Spark Submit

![image](https://github.com/user-attachments/assets/8e499b3f-7e55-420e-a94b-c5099948ff18)

Spark submit is a command line tool to run spark applications, it packages the spark code and runs on cluster.

The spark cluster can be standalone,local,K8s or YARN.

#### Spark Submit Command

![image](https://github.com/user-attachments/assets/d1074716-4dc8-4469-b126-1bfc949dc58d)

![image](https://github.com/user-attachments/assets/0cb56a47-03c2-4068-b6b8-69f97237225b)

![image](https://github.com/user-attachments/assets/e269e312-fcab-4f07-9a5b-2202ce1e785b)

Master can run on ```yarn```,```local``` or ```k8s```

```deploy-mode``` -> specifies where driver runs

```--class``` -> not required for python, just scala or java

```--jars``` -> my sql connector jar files

```spark.dynamicAllocation.enabled``` -> free's up some memory if we are not using it

![image](https://github.com/user-attachments/assets/a19795ba-4d5e-4012-90f8-db8d58a2a2e3)

We provide two arguments to ```main.py``` file. 

![image](https://github.com/user-attachments/assets/5c42be36-179e-44d4-a215-41e059c127ca)

We can provide syntax to generate log file.
![image](https://github.com/user-attachments/assets/9e162712-9fc4-42a9-a7e1-40a8da4d69c6)

The local system computer from where we run the command is called edge node.

### Lecture 28 : Deployment Modes in Spark

![image](https://github.com/user-attachments/assets/96b5edab-c2fe-4d71-898a-58193e94ff0f)

Below is the normal Spark Architecture

![image](https://github.com/user-attachments/assets/4360bf36-7807-4c69-9a9d-5adc87df9f3d)

Here we have a separate EC2 instance called edge node. Its configuration is not as much as the other nodes.

![image](https://github.com/user-attachments/assets/6a9e92f6-ac2e-4dbb-b6f9-d7f2df99e2cc)

User does not connect directly to the cluster rather connects to the edge node now.

They can login to the edge node and perform tasks. Kerberos is used for Authentication and Authorization.

Any data that needs to be submitted to cluster also goes through edge node.

The /bin/spark-submit folder is on the edge node, it contains hadoop client libaries YARN is not installed here.

![image](https://github.com/user-attachments/assets/6ed26628-b3c2-41fd-8d70-cd1b0c515cab)

#### client mode deployment

![image](https://github.com/user-attachments/assets/8a127c39-ec56-4d10-b751-8cb8598305f9)

Driver is made on the edge node.

#### cluster mode

![image](https://github.com/user-attachments/assets/64afeed7-0803-46b5-b748-6dd0ff9d5305)

In cluster mode, the driver is created on the cluster.

#### pros and cons of client mode

Pro : 

- The user can see the cluster logs on their own system.
  
Con : 

- Once the driver in the local system shuts down, the executors also go down.
- When we submit on client mode we will have network latency. Two way communication creates lot of delay.
  
![image](https://github.com/user-attachments/assets/0c4adda6-86ad-4b60-9deb-b14b0f6b2012)

In cluster mode, we are given an application id and using that we can see the spark ui details.

![image](https://github.com/user-attachments/assets/bbb7665c-960c-4b3c-bfd2-eaecab4611be)

### Lecture 29: Adaptive Query Execution

#### Features of AQE

![image](https://github.com/user-attachments/assets/6d312c6b-2983-4ebc-a3fb-9fef5647bced)

##### Dynamically Coalescing Shuffle Partitions

Sugar is best selling product it has highest data in the partition.

![image](https://github.com/user-attachments/assets/6302df14-6abb-4f8e-ac1a-63aee3154957)

Now there is a GroupBy / Shuffling of data. All the Sugar data comes to one partition.

![image](https://github.com/user-attachments/assets/419528eb-2d4a-4a90-b302-436c9ace1277)

By default there are 200 partitions, but 195 are empty.

The resources are getting wasted because these 195 partitions also need to be shuffled.

The 5 partitions become 5 tasks but Partition 1 takes lot of time to run.

![image](https://github.com/user-attachments/assets/60d3d490-b566-4f3d-a8eb-22d2c530197e)

Now AQE coalesces the partitions.

![image](https://github.com/user-attachments/assets/0cee3eda-96db-44fd-a000-a31ef5273174)

Two tasks are now reduced and also 2 cores become free.

But even after coalescing we may end up with data skew.

![image](https://github.com/user-attachments/assets/bffc1b5f-8afd-4557-9cc3-2f8b260771b0)

![image](https://github.com/user-attachments/assets/8a18642b-4448-455a-9a55-8a545930ae30)

Once we coalesce we end up with 2 partitions and 1/2 completes fast, the one with sugar takes time.

#### Data Splitting 

![image](https://github.com/user-attachments/assets/49399787-322c-452e-9e91-17d650a8b84c)

If median is 5MB and one partition is > 25MB then the data splits.

#### Dynamically Switching Join Strategy

![image](https://github.com/user-attachments/assets/48da944e-f024-4e2c-b31a-d79015f0d356)

By default spark does sort merge join.

Now if we compress table2 to become 10mb, even though sort merge join DAG is built, if AQE is enabled, we can check runtime statistics.

![image](https://github.com/user-attachments/assets/77901eba-47b2-4eec-b199-68deee0b3b3a)

Since data is only 10MB we can broadcast the data but shuffling still happens only sorting and merging is avoided.

#### Dynamically Optimizing Skew Join

![image](https://github.com/user-attachments/assets/aae53785-bad9-4399-8094-ba636234f4c3)

We are considering two tables where key = Sugar and just 128MB of data.

Let's show other partitions also

![image](https://github.com/user-attachments/assets/6d1eca97-aa29-4534-838b-8d177b868ab9)

Now when we do the Sort Merge Join and get all keys together the Sugar partition size increases.

![image](https://github.com/user-attachments/assets/f56d8ded-a4cc-495a-8606-176bda358233)

All tasks except the one with Sugar completes fast.

![image](https://github.com/user-attachments/assets/535c4cf4-c3b9-4076-8241-9133d673721a)

This leads to OOM error.

##### Solutions

- Salting
- AQE

AQE has ShuffleReader, it has statistics on the memory and size of each partition. This parttion gets automatically split in both tables.

![image](https://github.com/user-attachments/assets/77e35131-03a6-4ad0-898f-b705f935d2e4)

### Lecture 30 : Cache vs Persist

![image](https://github.com/user-attachments/assets/05c58f62-ef62-4736-a11b-01f4846176f0)

#### Spark Memory Management

![image](https://github.com/user-attachments/assets/df790f28-9d34-4cfd-9c20-20243300046a)

The Spark Memory is further expanded into Storage Memory Pool and Executor Memory Pool.

![image](https://github.com/user-attachments/assets/729e1214-7dac-48fe-98f8-2341192d7b42)

The cache is stored in Storage Memory Pool.

![image](https://github.com/user-attachments/assets/592f8810-e785-485f-8810-14f4e56e918d)

Not all the memory is stored in the executor. When df line code is run, df is removed from the executor, but in the subsequent step df is used to calculate df2. So in this case ideally df should be computed again, but if we have cache memory we can directly fetch from there.

![image](https://github.com/user-attachments/assets/fc019da5-0f98-47b4-9351-099ee4cecb42)

When we cache the data goes from executor short lived memory to the storage pool. The cache is based on LRU mechanism.

![image](https://github.com/user-attachments/assets/4534d33f-ccf1-49cd-ac1a-992ada1f26fd)

Now let's day we have 15 partitions but only 14.5 fit in storage memory, 1 partition does not get stored.

By default storage_level for ```df.cache()``` is ```MEMORY_AND_DISK``` if the data does not fit in MEMORY move it to disk, but the data takes time to read from disk so its not recommended.

If the partition gets lost during IO, the DAG will recalculate that.

```persist()``` gives us more flexibility.

![image](https://github.com/user-attachments/assets/d6ea7a42-f104-4710-a66a-148ab389de35)

```persist()``` -> when we pass MEMORY_AND_DISK to persist it becomes cache(). Cache is just a wrapper class on persist().

#### How many partitions get stored in cache?

When we use ```show()``` just one partition gets cached.

![image](https://github.com/user-attachments/assets/35cd42ac-f7e5-4d16-9180-ead9dcf3e5d4)

When we use ```count()``` all partitions get cached.

![image](https://github.com/user-attachments/assets/c57e9075-91ae-4454-bb8d-4a5452044652)

#### Storage Level in Persist

![image](https://github.com/user-attachments/assets/21a8e1cc-8eaa-4a90-b7ab-9d51594b02e1)

In ```MEMORY_AND_DISK``` the data is stored in disk after memory is full but its stored in serialized form, it should be deserialized before spark can process it and hence CPU utilization is high here.

![image](https://github.com/user-attachments/assets/b1127097-c5fa-4bdd-8095-338a24b5df71)

![image](https://github.com/user-attachments/assets/c6319ddf-79d8-4f39-9bba-ac6949c671f6)

**MEMORY_ONLY_2**

This data is replicated twice. Just to ensure that if we have complex computations and things fail, we dont need to do computations again.

```MEMORY_ONLY_SER``` and ```MEMORY_AND_DISK_SER``` works only in Scala and Java.
