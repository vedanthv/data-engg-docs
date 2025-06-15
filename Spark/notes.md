## Spark Concepts and Code

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
