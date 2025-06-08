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



