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