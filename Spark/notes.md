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




