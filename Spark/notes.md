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





