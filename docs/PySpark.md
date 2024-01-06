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
